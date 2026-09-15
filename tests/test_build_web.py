from __future__ import annotations

import importlib.util
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from edition_contract import load_edition_contract  # noqa: E402


def _load_web_module():
    spec = importlib.util.spec_from_file_location(
        "streamentry_build_web", SCRIPTS_DIR / "build-web.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


WEB = _load_web_module()


class WebHelpersTests(unittest.TestCase):
    def test_slugify_keeps_vietnamese_readable(self) -> None:
        self.assertEqual(
            WEB.slugify("Đích đến và nền đất"),
            "dich-den-va-nen-dat",
        )
        self.assertEqual(WEB.slugify("Tứ Niệm Xứ"), "tu-niem-xu")

    def test_slugify_never_returns_empty(self) -> None:
        self.assertEqual(WEB.slugify("!!! ???"), "trang")

    def test_search_normalization_removes_diacritics(self) -> None:
        self.assertEqual(WEB.normalize_search("Duyên khởi"), "duyen khoi")
        self.assertEqual(WEB.normalize_search("NHẬP LƯU"), "nhap luu")
        self.assertEqual(WEB.normalize_search("được"), "duoc")
        self.assertEqual(WEB.normalize_search("Đích đến"), "dich den")

    def test_relative_page_links_use_directory_form(self) -> None:
        self.assertEqual(
            WEB.relative_page("chuong-01-bay-ngay-bat-dau", "gioi-thieu"),
            "../gioi-thieu/index.html",
        )
        self.assertEqual(WEB.relative_page(None, "gioi-thieu"), "gioi-thieu/index.html")


class WebBuildTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("typst"), "typst is not on PATH")
    def test_full_build_is_linked_accessible_and_site_chrome_complete(self) -> None:
        edition = load_edition_contract(ROOT / "book" / "edition.json")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "web"
            WEB.build(ROOT, output, edition, "https://example.test/streamentry")

            pages = {
                path.relative_to(output).as_posix(): path.read_text(encoding="utf-8")
                for path in output.rglob("*.html")
            }
            self.assertIn("index.html", pages)
            self.assertIn("gioi-thieu/index.html", pages)

            anchors = {
                name: set(re.findall(r'\sid="([^"]+)"', html))
                for name, html in pages.items()
            }
            for name, html in pages.items():
                base = os.path.dirname(name)
                for href in re.findall(r'href="([^"]+)"', html):
                    if href.startswith(("#", "http", "mailto:")):
                        continue
                    if href.startswith(("assets/", "../assets/")):
                        continue
                    target, _, fragment = href.partition("#")
                    resolved = os.path.normpath(os.path.join(base, target))
                    self.assertIn(resolved, pages, f"{name}: broken link {href}")
                    if fragment:
                        self.assertIn(fragment, anchors[resolved], f"{name}: stale {href}")

            landing = pages["index.html"]
            for badge in (
                "source-kinh",
                "source-luan-giai",
                "source-thanh-tinh-dao",
                "source-mahasi",
                "source-nghien-cuu",
                "source-bien-soan",
            ):
                self.assertIn(badge, landing)
            self.assertIn("115", landing)
            self.assertIn("correction.yml", landing)
            self.assertIn("chưa có giấy phép công khai", landing)
            self.assertIn("https://streamentry.github.io/kinh-tang-pali/", landing)

            chapter = pages["chuong-01-bay-ngay-bat-dau/index.html"]
            self.assertIn("chapter-opener", chapter)
            self.assertIn("../assets/site.js", chapter)
            self.assertIn("data-base=\"../\"", chapter)
            self.assertIn("https://streamentry.github.io/kinh-tang-pali/", chapter)

            index = (output / "assets" / "search-index.json").read_text(encoding="utf-8")
            self.assertIn('"entries"', index)
            self.assertTrue((output / ".nojekyll").exists())
            self.assertTrue((output / "sitemap.xml").exists())
            self.assertTrue((output / "robots.txt").exists())
            self.assertTrue((output / "404.html").exists())


if __name__ == "__main__":
    unittest.main()
