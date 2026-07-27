from __future__ import annotations

import importlib.util
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from edition_contract import EDITION  # noqa: E402


def _load_epub_builder() -> ModuleType:
    path = SCRIPTS_DIR / "build-epub.py"
    spec = importlib.util.spec_from_file_location("edition_contract_epub_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load EPUB builder from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


EPUB = _load_epub_builder()
XHTML = {"xhtml": EPUB.XHTML_NS}
OPF = {"opf": "http://www.idpf.org/2007/opf"}
DC = {"dc": "http://purl.org/dc/elements/1.1/"}
OLD_VIETNAMESE_NAVIGATION_LABELS = (
    "Mục lục",
    "Lời dẫn",
    "Bìa",
    "Nội dung",
    "Các điểm mốc",
)

SENTINEL = replace(
    EDITION,
    edition_id="zz-2030",
    title='Sentinel & <Edition> "One"',
    author="Author & <Name>",
    language="zz-Latn",
    description="Description & <details>",
    subjects=("Subject & One", "Subject <Two>"),
    identifier_seed="https://example.test/sentinel-edition",
    epub_modified="2030-01-02T03:04:05Z",
    toc_label="Sentinel & Contents",
    introduction_label="Opening & Orientation",
    cover_label="Jacket & Cover",
    content_label="Main <Content>",
    landmarks_label="Waypoints & Places",
    cover_alt='Cover of "Sentinel" & <edition>',
    accessibility_summary="Text & navigation <summary>",
)


def _parse(document: str) -> ET.Element:
    return ET.fromstring(document)


class EpubEditionContractTests(unittest.TestCase):
    def test_book_head_metadata_is_bound_to_the_supplied_contract(self) -> None:
        head = ET.Element(EPUB._qname(EPUB.XHTML_NS, "head"))
        ET.SubElement(head, EPUB._qname(EPUB.XHTML_NS, "title")).text = (
            SENTINEL.title
        )
        for name, content in {
            "description": SENTINEL.description,
            "authors": SENTINEL.author,
            "keywords": ", ".join(SENTINEL.keywords),
        }.items():
            ET.SubElement(
                head,
                EPUB._qname(EPUB.XHTML_NS, "meta"),
                {"name": name, "content": content},
            )

        EPUB._validate_head_metadata(head, SENTINEL)
        for field in ("title", "description", "authors", "keywords"):
            with self.subTest(field=field):
                changed = ET.fromstring(ET.tostring(head))
                if field == "title":
                    title = changed.find(EPUB._qname(EPUB.XHTML_NS, "title"))
                    assert title is not None
                    title.text = "Wrong"
                else:
                    meta = next(
                        node
                        for node in changed.findall(
                            EPUB._qname(EPUB.XHTML_NS, "meta")
                        )
                        if node.attrib.get("name") == field
                    )
                    meta.set("content", "Wrong")
                with self.assertRaisesRegex(ValueError, field):
                    EPUB._validate_head_metadata(changed, SENTINEL)

        duplicate = ET.fromstring(ET.tostring(head))
        ET.SubElement(
            duplicate,
            EPUB._qname(EPUB.XHTML_NS, "meta"),
            {"name": "authors", "content": SENTINEL.author},
        )
        with self.assertRaisesRegex(ValueError, "authors"):
            EPUB._validate_head_metadata(duplicate, SENTINEL)

    def test_navigation_uses_only_the_supplied_labels_and_language(self) -> None:
        headings = [
            EPUB.Heading(1, "intro", "Original introduction"),
            EPUB.Heading(2, "detail", "Detail & <One>"),
            EPUB.Heading(1, "next", 'Next "Section"'),
        ]
        document = EPUB.nav_xhtml(headings, "intro", SENTINEL)
        root = _parse(document)

        self.assertEqual(root.attrib["lang"], SENTINEL.language)
        self.assertEqual(
            root.attrib[f"{{{EPUB.XML_NS}}}lang"],
            SENTINEL.language,
        )
        self.assertEqual(
            root.findtext("xhtml:head/xhtml:title", namespaces=XHTML),
            SENTINEL.toc_label,
        )

        toc = EPUB._find_nav(root, "toc")
        self.assertEqual(toc.attrib["aria-label"], SENTINEL.toc_label)
        self.assertEqual(
            toc.findtext("xhtml:h1", namespaces=XHTML),
            SENTINEL.toc_label,
        )
        toc_links = [
            ("".join(link.itertext()), link.attrib["href"])
            for link in toc.findall(".//xhtml:a", XHTML)
        ]
        self.assertEqual(
            toc_links,
            [
                (SENTINEL.cover_label, "cover.xhtml"),
                (SENTINEL.introduction_label, "book.xhtml#intro"),
                ("Detail & <One>", "book.xhtml#detail"),
                ('Next "Section"', "book.xhtml#next"),
            ],
        )

        landmarks = EPUB._find_nav(root, "landmarks")
        self.assertEqual(
            landmarks.attrib["aria-label"],
            SENTINEL.landmarks_label,
        )
        landmark_links = [
            ("".join(link.itertext()), link.attrib["href"])
            for link in landmarks.findall(".//xhtml:a", XHTML)
        ]
        self.assertEqual(
            landmark_links,
            [
                (SENTINEL.cover_label, "cover.xhtml"),
                (SENTINEL.content_label, "book.xhtml#bodymatter"),
            ],
        )

        self.assertIn("Sentinel &amp; Contents", document)
        self.assertIn("Detail &amp; &lt;One&gt;", document)
        for old_label in OLD_VIETNAMESE_NAVIGATION_LABELS:
            self.assertNotIn(old_label, document)

    def test_cover_uses_supplied_language_title_alt_and_xml_escaping(self) -> None:
        document = EPUB.cover_xhtml(SENTINEL)
        root = _parse(document)
        image = root.find(".//xhtml:img", XHTML)

        self.assertEqual(root.attrib["lang"], SENTINEL.language)
        self.assertEqual(
            root.attrib[f"{{{EPUB.XML_NS}}}lang"],
            SENTINEL.language,
        )
        self.assertEqual(
            root.findtext("xhtml:head/xhtml:title", namespaces=XHTML),
            SENTINEL.title,
        )
        self.assertIsNotNone(image)
        assert image is not None
        self.assertEqual(image.attrib["alt"], SENTINEL.cover_alt)
        self.assertIn("Sentinel &amp; &lt;Edition&gt; &quot;One&quot;", document)
        self.assertIn(
            'alt="Cover of &quot;Sentinel&quot; &amp; &lt;edition&gt;"',
            document,
        )

    def test_content_links_require_labels_resolved_fragments_and_https(self) -> None:
        root = ET.fromstring(
            f"""\
<html xmlns="{EPUB.XHTML_NS}">
  <body>
    <main id="bodymatter">
      <p id="target">Target</p>
      <a href="#target">Local target</a>
      <a href="https://example.test/source">External source</a>
    </main>
  </body>
</html>
"""
        )
        EPUB._validate_content_links(root)

        defects = {
            "does not resolve": '<a href="#missing">Missing</a>',
            "accessible label": '<a href="https://example.test/source"></a>',
            "absolute HTTPS": '<a href="http://example.test/source">Source</a>',
            "non-empty href": "<a>Missing href</a>",
            "distinct labels": (
                '<a href="https://example.test/one">Same source</a>'
                '<a href="https://example.test/two">Same source</a>'
            ),
        }
        for message, link in defects.items():
            with self.subTest(message=message):
                broken = ET.fromstring(
                    f"""\
<html xmlns="{EPUB.XHTML_NS}">
  <body><main id="bodymatter"><p id="target">Target</p>{link}</main></body>
</html>
"""
                )
                with self.assertRaisesRegex(ValueError, message):
                    EPUB._validate_content_links(broken)

    def test_opf_uses_supplied_metadata_subjects_and_accessibility_summary(self) -> None:
        document = EPUB.package_opf(SENTINEL)
        root = _parse(document)
        metadata = root.find("opf:metadata", OPF)
        self.assertIsNotNone(metadata)
        assert metadata is not None

        self.assertEqual(
            root.attrib[f"{{{EPUB.XML_NS}}}lang"],
            SENTINEL.language,
        )
        expected = {
            "identifier": SENTINEL.identifier,
            "title": SENTINEL.title,
            "creator": SENTINEL.author,
            "language": SENTINEL.language,
            "description": SENTINEL.description,
        }
        for name, value in expected.items():
            with self.subTest(name=name):
                self.assertEqual(
                    metadata.findtext(f"dc:{name}", namespaces=DC),
                    value,
                )
        self.assertEqual(
            [
                node.text
                for node in metadata.findall("dc:subject", DC)
            ],
            list(SENTINEL.subjects),
        )
        accessibility = [
            node.text
            for node in metadata.findall("opf:meta", OPF)
            if node.attrib.get("property") == "schema:accessibilitySummary"
        ]
        self.assertEqual(accessibility, [SENTINEL.accessibility_summary])

        self.assertIn("Author &amp; &lt;Name&gt;", document)
        self.assertIn("Description &amp; &lt;details&gt;", document)
        self.assertIn("Subject &amp; One", document)
        self.assertIn("Subject &lt;Two&gt;", document)
        self.assertIn("Text &amp; navigation &lt;summary&gt;", document)


if __name__ == "__main__":
    unittest.main()
