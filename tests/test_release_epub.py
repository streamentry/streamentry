from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
TESTS_DIR = ROOT / "tests"
for directory in (SCRIPTS_DIR, TESTS_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from release_common import ReleaseVerificationError  # noqa: E402
from release_epub import parse_epub_documents, read_epub_facts  # noqa: E402
from release_verifier_fixtures import (  # noqa: E402
    FULL_PACKAGE,
    NAV,
    PACKAGE,
    write_test_epub,
)


class ReleaseEpubTests(unittest.TestCase):
    def test_counts_cover_and_content_navigation_separately(self) -> None:
        facts = parse_epub_documents(NAV, PACKAGE)
        self.assertEqual(facts.cover_entries, 1)
        self.assertEqual(facts.content_entries, 2)
        self.assertEqual(facts.language, "vi")

    def test_rejects_multiple_toc_navigation_elements(self) -> None:
        duplicate = NAV.replace(b"</body>", b"<nav epub:type=\"toc\" /></body>")
        with self.assertRaisesRegex(ReleaseVerificationError, "exactly one"):
            parse_epub_documents(duplicate, PACKAGE)

    def test_rejects_duplicate_toc_targets(self) -> None:
        duplicate = NAV.replace(
            b'<li><a href="book.xhtml#two">Two</a></li>',
            b'<li><a href="book.xhtml#one">Two</a></li>',
        )
        with self.assertRaisesRegex(ReleaseVerificationError, "unique"):
            parse_epub_documents(duplicate, PACKAGE)

    def test_rejects_an_inactive_canonical_epub_package(self) -> None:
        container = b"""\
<?xml version="1.0" encoding="utf-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/active.opf"
              media-type="application/oebps-package+xml"/>
    <rootfile full-path="EPUB/package.opf"
              media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "multiple-renditions.epub"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(
                    "mimetype",
                    b"application/epub+zip",
                    compress_type=zipfile.ZIP_STORED,
                )
                archive.writestr("META-INF/container.xml", container)
                archive.writestr(
                    "EPUB/active.opf",
                    PACKAGE.replace(b"Huong Den Nhap Luu", b"Wrong active title"),
                )
                archive.writestr("EPUB/package.opf", PACKAGE)
            with self.assertRaisesRegex(ReleaseVerificationError, "one package"):
                read_epub_facts(path)

    def test_rejects_a_noncanonical_epub_spine_order(self) -> None:
        wrong_spine = FULL_PACKAGE.replace(
            b"""\
    <itemref idref="cover-page" linear="yes"/>
    <itemref idref="book" linear="yes"/>""",
            b"""\
    <itemref idref="book" linear="yes"/>
    <itemref idref="cover-page" linear="yes"/>""",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong-spine.epub"
            write_test_epub(path, package=wrong_spine)
            with self.assertRaisesRegex(ReleaseVerificationError, "spine"):
                read_epub_facts(path)

    def test_rejects_epub_spine_presentation_overrides(self) -> None:
        overridden_spine = FULL_PACKAGE.replace(
            b'<itemref idref="book" linear="yes"/>',
            b'<itemref idref="book" linear="yes" '
            b'properties="rendition:orientation-landscape"/>',
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "overridden-spine.epub"
            write_test_epub(path, package=overridden_spine)
            with self.assertRaisesRegex(ReleaseVerificationError, "spine"):
                read_epub_facts(path)

    def test_rejects_xhtml_base_redirection(self) -> None:
        redirected_nav = NAV.replace(
            b"<body>",
            b'<head><base href="shadow/"/></head><body>',
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "redirected-nav.epub"
            write_test_epub(path, nav=redirected_nav)
            with self.assertRaisesRegex(ReleaseVerificationError, "base"):
                read_epub_facts(path)


if __name__ == "__main__":
    unittest.main()
