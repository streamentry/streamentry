#!/usr/bin/env python3
"""Build and structurally validate a deterministic EPUB 3 edition."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from html import escape as xml_escape
from pathlib import Path
from xml.etree import ElementTree as ET

from edition_contract import EDITION, EditionContract, load_edition_contract


XHTML_NS = "http://www.w3.org/1999/xhtml"
EPUB_NS = "http://www.idpf.org/2007/ops"
XML_NS = "http://www.w3.org/XML/1998/namespace"
PACKAGE_PREFIXES = (
    "dcterms: http://purl.org/dc/terms/ "
    "marc: http://id.loc.gov/vocabulary/ "
    "schema: http://schema.org/"
)
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
VOID_ELEMENTS = ("area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr")

TYPST_HTML_WARNING_HEADERS = (
    re.compile(r"warning: html export is under active development and incomplete"),
    re.compile(r"warning: (?:align|h|pagebreak|rect|v) was ignored during HTML export"),
)
TYPST_HINT_LINE = re.compile(r"\s*= hint: .+")
TYPST_DIAGNOSTIC_LINE = re.compile(r"(?:\s*┌─ .+:\d+:\d+|\s*(?:\d+\s+)?│.*)")

ET.register_namespace("", XHTML_NS)
ET.register_namespace("epub", EPUB_NS)


@dataclass(frozen=True)
class Heading:
    level: int
    anchor: str
    label: str


@dataclass
class NavNode:
    heading: Heading
    children: list["NavNode"]


def _qname(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


def _classes(element: ET.Element) -> set[str]:
    return set(element.attrib.get("class", "").split())


def _label(element: ET.Element) -> str:
    return " ".join("".join(element.itertext()).split())


def validate_stderr(
    stderr: str,
    allowed_warning_headers: tuple[re.Pattern[str], ...] = (),
) -> int:
    """Reject stderr unless every line belongs to an explicitly known Typst warning."""
    if not stderr.strip():
        return 0
    if not allowed_warning_headers:
        raise RuntimeError(f"unexpected stderr:\n{stderr.rstrip()}")

    warning_count = 0
    warning_kind: str | None = None
    for line in stderr.splitlines():
        if line.startswith("warning:"):
            if not any(pattern.fullmatch(line) for pattern in allowed_warning_headers):
                raise RuntimeError(f"unexpected warning: {line}")
            warning_count += 1
            warning_kind = "experimental" if "active development" in line else "ignored"
        elif not line.strip():
            continue
        elif warning_kind == "experimental" and TYPST_HINT_LINE.fullmatch(line):
            continue
        elif warning_kind == "ignored" and TYPST_DIAGNOSTIC_LINE.fullmatch(line):
            continue
        else:
            raise RuntimeError(f"unexpected stderr line: {line}")
    return warning_count


def run(
    command: list[str],
    cwd: Path,
    allowed_warning_headers: tuple[re.Pattern[str], ...] = (),
) -> None:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if completed.returncode:
        sys.stderr.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        raise SystemExit(completed.returncode)
    warning_count = validate_stderr(completed.stderr, allowed_warning_headers)
    if warning_count:
        print(f"Acknowledged {warning_count} known Typst HTML-export warnings.")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _close_html_void_elements(document: str) -> str:
    tags = "|".join(VOID_ELEMENTS)
    return re.sub(
        rf"<({tags})(\b[^<>]*?)(?<!/)>",
        r"<\1\2 />",
        document,
        flags=re.IGNORECASE,
    )


def _apply_xhtml_namespace(element: ET.Element) -> None:
    if isinstance(element.tag, str):
        if element.tag.startswith("{"):
            namespace = element.tag[1:].split("}", 1)[0]
            if namespace != XHTML_NS:
                raise ValueError(f"unexpected HTML element namespace: {namespace}")
        else:
            element.tag = _qname(XHTML_NS, element.tag)
    for child in element:
        _apply_xhtml_namespace(child)


def _parse_html(
    raw_html: str,
    edition: EditionContract = EDITION,
) -> ET.Element:
    document = re.sub(r"^\s*<!DOCTYPE html>\s*", "", raw_html, count=1, flags=re.IGNORECASE)
    try:
        root = ET.fromstring(_close_html_void_elements(document))
    except ET.ParseError as error:
        raise ValueError(f"Typst HTML is not convertible to XML: {error}") from error
    if root.tag != "html":
        raise ValueError(f"expected an html root, found {root.tag!r}")

    _apply_xhtml_namespace(root)
    root.set("lang", edition.language)
    root.set(_qname(XML_NS, "lang"), edition.language)
    return root


def _prepare_body(root: ET.Element) -> None:
    head = root.find(_qname(XHTML_NS, "head"))
    body = root.find(_qname(XHTML_NS, "body"))
    if head is None or body is None:
        raise ValueError("XHTML requires exactly one head and body")

    for style in list(body.findall(_qname(XHTML_NS, "style"))):
        body.remove(style)
        head.append(style)

    direct_mains = [child for child in body if child.tag == _qname(XHTML_NS, "main")]
    if direct_mains:
        if len(direct_mains) != 1 or len(body) != 1:
            raise ValueError("an existing main element must be the sole body child")
        main = direct_mains[0]
    else:
        main = ET.Element(_qname(XHTML_NS, "main"))
        for child in list(body):
            body.remove(child)
            main.append(child)
        body.append(main)

    covers = [child for child in list(main) if "cover" in _classes(child)]
    if len(covers) != 1:
        raise ValueError("expected exactly one direct HTML cover before EPUB normalization")
    main.remove(covers[0])

    duplicate = [
        element
        for element in root.iter()
        if element is not main and element.attrib.get("id") == "bodymatter"
    ]
    if duplicate:
        raise ValueError("bodymatter id is already used by another element")
    main.set("id", "bodymatter")
    main.set(_qname(EPUB_NS, "type"), "bodymatter")


def _promote_body_headings(root: ET.Element) -> None:
    """Promote Typst's h2-h6 content after removing its print-cover h1."""
    body = root.find(_qname(XHTML_NS, "body"))
    if body is None:
        raise ValueError("XHTML body is missing")
    for element in body.iter():
        match = re.fullmatch(rf"\{{{re.escape(XHTML_NS)}\}}h([2-6])", str(element.tag))
        if match:
            element.tag = _qname(XHTML_NS, f"h{int(match.group(1)) - 1}")


def _assign_missing_heading_ids(root: ET.Element) -> None:
    used = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
    sequence = 1
    for element in root.iter():
        if not re.fullmatch(rf"\{{{re.escape(XHTML_NS)}\}}h[1-6]", str(element.tag)):
            continue
        if element.attrib.get("id"):
            continue
        while f"epub-heading-{sequence:03d}" in used:
            sequence += 1
        anchor = f"epub-heading-{sequence:03d}"
        element.set("id", anchor)
        used.add(anchor)
        sequence += 1


def _extract_headings(
    root: ET.Element,
    *,
    include_toc: bool = False,
    edition: EditionContract = EDITION,
) -> list[Heading]:
    headings: list[Heading] = []
    anchors: set[str] = set()
    for element in root.iter():
        match = re.fullmatch(rf"\{{{re.escape(XHTML_NS)}\}}h([1-6])", str(element.tag))
        if not match:
            continue
        anchor = element.attrib.get("id", "")
        label = _label(element)
        if not anchor or not label:
            raise ValueError(f"every h1-h6 requires an id and visible label: {label!r}")
        if anchor in anchors:
            raise ValueError(f"duplicate heading id: {anchor}")
        anchors.add(anchor)
        if include_toc or label != edition.toc_label:
            headings.append(Heading(int(match.group(1)), anchor, label))
    if not headings:
        raise ValueError("no navigable h1-h6 headings found")
    if headings[0].level != 1:
        raise ValueError("the first navigable heading must be h1")
    for previous, current in zip(headings, headings[1:]):
        if current.level > previous.level + 1:
            raise ValueError(
                f"heading hierarchy jumps from h{previous.level} to h{current.level}: {current.label}"
            )
    return headings


def _intro_heading(root: ET.Element) -> Heading:
    candidates: dict[str, Heading] = {}
    for container in root.iter():
        if "introduction-opener" not in _classes(container):
            continue
        for element in container.iter():
            match = re.fullmatch(rf"\{{{re.escape(XHTML_NS)}\}}h([1-6])", str(element.tag))
            if match and element.attrib.get("id"):
                heading = Heading(int(match.group(1)), element.attrib["id"], _label(element))
                candidates[heading.anchor] = heading
                break
    if len(candidates) != 1:
        raise ValueError("expected one real heading inside .introduction-opener")
    return next(iter(candidates.values()))


def _validate_head_metadata(
    head: ET.Element,
    edition: EditionContract = EDITION,
) -> None:
    titles = head.findall(_qname(XHTML_NS, "title"))
    if len(titles) != 1 or _label(titles[0]) != edition.title:
        raise ValueError("book XHTML title does not match the edition contract")

    expected = {
        "description": edition.description,
        "authors": edition.author,
        "keywords": ", ".join(edition.keywords),
    }
    for name, expected_content in expected.items():
        metas = [
            meta
            for meta in head.findall(_qname(XHTML_NS, "meta"))
            if meta.attrib.get("name") == name
        ]
        if (
            len(metas) != 1
            or metas[0].attrib.get("content") != expected_content
        ):
            raise ValueError(
                f"book XHTML {name} metadata does not match the edition contract"
            )


def _validate_semantics(
    root: ET.Element,
    edition: EditionContract = EDITION,
) -> tuple[list[Heading], Heading]:
    head = root.find(_qname(XHTML_NS, "head"))
    body = root.find(_qname(XHTML_NS, "body"))
    if head is None or body is None:
        raise ValueError("XHTML head or body is missing")
    if root.attrib.get("lang") != edition.language or root.attrib.get(
        _qname(XML_NS, "lang")
    ) != edition.language:
        raise ValueError("book XHTML language does not match the edition contract")
    _validate_head_metadata(head, edition)
    mains = body.findall(_qname(XHTML_NS, "main"))
    if len(mains) != 1 or len(body) != 1:
        raise ValueError("body must contain exactly one main element")
    main = mains[0]
    if main.attrib.get("id") != "bodymatter":
        raise ValueError("main must expose the bodymatter anchor")
    if main.attrib.get(_qname(EPUB_NS, "type")) != "bodymatter":
        raise ValueError("main must carry epub:type=bodymatter")
    if any("cover" in _classes(element) for element in main.iter()):
        raise ValueError("book.xhtml must not duplicate the dedicated EPUB cover")
    children = list(main)
    if not children or "introduction-opener" not in _classes(children[0]):
        raise ValueError("bodymatter must begin with the semantic introduction opener")
    if body.findall(f".//{_qname(XHTML_NS, 'style')}"):
        raise ValueError("style elements must be in head, not body")
    ids = [element.attrib["id"] for element in root.iter() if "id" in element.attrib]
    if len(ids) != len(set(ids)):
        raise ValueError("all XHTML ids must be unique")

    css = "\n".join("".join(style.itertext()) for style in head.findall(_qname(XHTML_NS, "style")))
    if "color-scheme" not in css or not re.search(
        r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)", css
    ):
        raise ValueError("reflowable CSS must retain color-scheme and dark-mode rules")

    headings = _extract_headings(root, edition=edition)
    intro = _intro_heading(root)
    if headings[0] != intro:
        raise ValueError("the introduction must be the first navigable h1")

    required_text = (*edition.semantic_required_text, edition.author)
    body_text = " ".join("".join(main.itertext()).split())
    missing = [text for text in required_text if text not in body_text]
    if missing:
        raise ValueError(f"semantic HTML is missing required content: {missing}")
    return headings, intro


def to_xhtml(
    raw_html: str,
    edition: EditionContract = EDITION,
) -> tuple[str, list[Heading], str]:
    root = _parse_html(raw_html, edition)
    _prepare_body(root)
    _promote_body_headings(root)
    _assign_missing_heading_ids(root)
    headings, intro = _validate_semantics(root, edition)
    document = ET.tostring(root, encoding="unicode", method="xml", short_empty_elements=True)
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n' + document,
        headings,
        intro.anchor,
    )


def _heading_tree(headings: list[Heading]) -> list[NavNode]:
    roots: list[NavNode] = []
    stack: list[tuple[int, list[NavNode]]] = [(0, roots)]
    for heading in headings:
        while stack[-1][0] >= heading.level:
            stack.pop()
        if heading.level != stack[-1][0] + 1:
            raise ValueError(f"cannot nest h{heading.level} after h{stack[-1][0]}")
        node = NavNode(heading, [])
        stack[-1][1].append(node)
        stack.append((heading.level, node.children))
    return roots


def _render_nav_nodes(
    parent: ET.Element,
    nodes: list[NavNode],
    intro_anchor: str,
    edition: EditionContract,
) -> None:
    for node in nodes:
        item = ET.SubElement(parent, _qname(XHTML_NS, "li"))
        link = ET.SubElement(
            item,
            _qname(XHTML_NS, "a"),
            {"href": f"book.xhtml#{node.heading.anchor}"},
        )
        link.text = (
            edition.introduction_label
            if node.heading.anchor == intro_anchor
            else node.heading.label
        )
        if node.children:
            nested = ET.SubElement(item, _qname(XHTML_NS, "ol"))
            _render_nav_nodes(nested, node.children, intro_anchor, edition)


def nav_xhtml(
    headings: list[Heading],
    intro_anchor: str,
    edition: EditionContract = EDITION,
) -> str:
    html_root = ET.Element(
        _qname(XHTML_NS, "html"),
        {
            "lang": edition.language,
            _qname(XML_NS, "lang"): edition.language,
        },
    )
    head = ET.SubElement(html_root, _qname(XHTML_NS, "head"))
    ET.SubElement(head, _qname(XHTML_NS, "title")).text = edition.toc_label
    body = ET.SubElement(html_root, _qname(XHTML_NS, "body"))
    toc = ET.SubElement(
        body,
        _qname(XHTML_NS, "nav"),
        {
            _qname(EPUB_NS, "type"): "toc",
            "id": "toc",
            "role": "doc-toc",
            "aria-label": edition.toc_label,
        },
    )
    ET.SubElement(toc, _qname(XHTML_NS, "h1")).text = edition.toc_label
    outline = ET.SubElement(toc, _qname(XHTML_NS, "ol"))
    cover_item = ET.SubElement(outline, _qname(XHTML_NS, "li"))
    ET.SubElement(
        cover_item,
        _qname(XHTML_NS, "a"),
        {"href": "cover.xhtml"},
    ).text = edition.cover_label
    _render_nav_nodes(outline, _heading_tree(headings), intro_anchor, edition)

    landmarks = ET.SubElement(
        body,
        _qname(XHTML_NS, "nav"),
        {
            _qname(EPUB_NS, "type"): "landmarks",
            "role": "navigation",
            "aria-label": edition.landmarks_label,
            "hidden": "hidden",
        },
    )
    landmark_list = ET.SubElement(landmarks, _qname(XHTML_NS, "ol"))
    cover = ET.SubElement(landmark_list, _qname(XHTML_NS, "li"))
    ET.SubElement(
        cover,
        _qname(XHTML_NS, "a"),
        {_qname(EPUB_NS, "type"): "cover", "href": "cover.xhtml"},
    ).text = edition.cover_label
    content = ET.SubElement(landmark_list, _qname(XHTML_NS, "li"))
    ET.SubElement(
        content,
        _qname(XHTML_NS, "a"),
        {_qname(EPUB_NS, "type"): "bodymatter", "href": "book.xhtml#bodymatter"},
    ).text = edition.content_label

    document = ET.tostring(html_root, encoding="unicode", method="xml", short_empty_elements=True)
    return '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n' + document


def cover_xhtml(edition: EditionContract = EDITION) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="{XHTML_NS}" xmlns:epub="{EPUB_NS}" lang="{edition.language}" xml:lang="{edition.language}">
  <head>
    <title>{xml_escape(edition.title)}</title>
    <style>html, body {{ margin: 0; padding: 0; text-align: center; }} img {{ max-width: 100%; height: auto; }}</style>
  </head>
  <body epub:type="cover">
    <img src="cover.png" alt="{xml_escape(edition.cover_alt, quote=True)}" />
  </body>
</html>
"""


def package_opf(edition: EditionContract = EDITION) -> str:
    subjects = "\n".join(
        f"    <dc:subject>{xml_escape(subject)}</dc:subject>"
        for subject in edition.subjects
    )
    return f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="{edition.language}" prefix="{PACKAGE_PREFIXES}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">{edition.identifier}</dc:identifier>
    <dc:title>{xml_escape(edition.title)}</dc:title>
    <dc:creator id="creator">{xml_escape(edition.author)}</dc:creator>
    <meta refines="#creator" property="role" scheme="marc:relators">aut</meta>
    <dc:language>{edition.language}</dc:language>
    <dc:description>{xml_escape(edition.description)}</dc:description>
{subjects}
    <meta property="dcterms:modified">{edition.epub_modified}</meta>
    <meta property="schema:accessMode">textual</meta>
    <meta property="schema:accessModeSufficient">textual</meta>
    <meta property="schema:accessibilityFeature">tableOfContents</meta>
    <meta property="schema:accessibilityFeature">readingOrder</meta>
    <meta property="schema:accessibilityFeature">structuralNavigation</meta>
    <meta property="schema:accessibilityFeature">displayTransformability</meta>
    <meta property="schema:accessibilityHazard">none</meta>
    <meta property="schema:accessibilitySummary">{xml_escape(edition.accessibility_summary)}</meta>
    <meta name="cover" content="cover-image" />
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />
    <item id="cover-page" href="cover.xhtml" media-type="application/xhtml+xml" />
    <item id="book" href="book.xhtml" media-type="application/xhtml+xml" />
    <item id="cover-image" href="cover.png" media-type="image/png" properties="cover-image" />
  </manifest>
  <spine>
    <itemref idref="cover-page" linear="yes" />
    <itemref idref="book" linear="yes" />
  </spine>
</package>
"""


def container_xml() -> str:
    return """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
"""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _toc_links(outline: ET.Element, depth: int = 1) -> list[tuple[str, str, int]]:
    links: list[tuple[str, str, int]] = []
    for item in outline.findall(_qname(XHTML_NS, "li")):
        link = item.find(_qname(XHTML_NS, "a"))
        if link is None:
            raise ValueError("each EPUB navigation item requires a direct link")
        links.append((link.attrib.get("href", ""), _label(link), depth))
        nested = item.find(_qname(XHTML_NS, "ol"))
        if nested is not None:
            links.extend(_toc_links(nested, depth + 1))
    return links


def _find_nav(root: ET.Element, epub_type: str) -> ET.Element:
    matches = [
        nav
        for nav in root.findall(f".//{_qname(XHTML_NS, 'nav')}")
        if nav.attrib.get(_qname(EPUB_NS, "type")) == epub_type
    ]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {epub_type} navigation element")
    return matches[0]


def _validate_navigation(
    nav: ET.Element,
    headings: list[Heading],
    intro_anchor: str,
    edition: EditionContract = EDITION,
) -> None:
    if nav.attrib.get("lang") != edition.language or nav.attrib.get(
        _qname(XML_NS, "lang")
    ) != edition.language:
        raise ValueError("navigation language does not match the edition contract")
    toc = _find_nav(nav, "toc")
    if toc.attrib.get("aria-label") != edition.toc_label:
        raise ValueError("table-of-contents label does not match the edition contract")
    toc_heading = toc.find(_qname(XHTML_NS, "h1"))
    if toc_heading is None or _label(toc_heading) != edition.toc_label:
        raise ValueError("table-of-contents heading does not match the edition contract")
    outline = toc.find(_qname(XHTML_NS, "ol"))
    if outline is None:
        raise ValueError("EPUB table of contents requires an ordered list")
    actual = _toc_links(outline)
    expected = [("cover.xhtml", edition.cover_label, 1)]
    expected.extend(
        (
            f"book.xhtml#{heading.anchor}",
            (
                edition.introduction_label
                if heading.anchor == intro_anchor
                else heading.label
            ),
            heading.level,
        )
        for heading in headings
    )
    if actual != expected:
        raise ValueError("EPUB navigation does not match the complete h1-h6 outline")
    if any(heading.level > 1 for heading in headings) and len(
        toc.findall(f".//{_qname(XHTML_NS, 'ol')}")
    ) < 2:
        raise ValueError("subheadings must be represented by nested ordered lists")

    landmarks = _find_nav(nav, "landmarks")
    if landmarks.attrib.get("aria-label") != edition.landmarks_label:
        raise ValueError("landmarks label does not match the edition contract")
    landmark_labels = [
        _label(link)
        for link in landmarks.findall(f".//{_qname(XHTML_NS, 'a')}")
    ]
    if landmark_labels != [edition.cover_label, edition.content_label]:
        raise ValueError("landmark link labels do not match the edition contract")
    bodymatter_links = [
        link
        for link in landmarks.findall(f".//{_qname(XHTML_NS, 'a')}")
        if link.attrib.get(_qname(EPUB_NS, "type")) == "bodymatter"
    ]
    if len(bodymatter_links) != 1 or bodymatter_links[0].attrib.get("href") != "book.xhtml#bodymatter":
        raise ValueError("landmarks must target the semantic bodymatter anchor")


def validate_package(
    epub_path: Path,
    edition: EditionContract = EDITION,
) -> None:
    with zipfile.ZipFile(epub_path) as archive:
        names = archive.namelist()
        if not names or names[0] != "mimetype":
            raise ValueError("mimetype must be the first EPUB entry")
        if archive.read("mimetype") != b"application/epub+zip":
            raise ValueError("invalid EPUB mimetype")
        if archive.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
            raise ValueError("mimetype must be stored without compression")
        if any(info.date_time != ZIP_TIMESTAMP for info in archive.infolist()):
            raise ValueError("every EPUB ZIP entry must use the fixed reproducible timestamp")

        xml_files = (
            "META-INF/container.xml",
            "EPUB/package.opf",
            "EPUB/nav.xhtml",
            "EPUB/cover.xhtml",
            "EPUB/book.xhtml",
        )
        roots = {name: ET.fromstring(archive.read(name)) for name in xml_files}

        package = roots["EPUB/package.opf"]
        opf_ns = {"opf": "http://www.idpf.org/2007/opf"}
        dc_ns = {"dc": "http://purl.org/dc/elements/1.1/"}
        if package.attrib.get("prefix") != PACKAGE_PREFIXES:
            raise ValueError("package vocabulary prefixes do not match EPUB 3.3 mappings")
        if package.attrib.get(_qname(XML_NS, "lang")) != edition.language:
            raise ValueError("package language does not match the edition contract")
        metadata = package.find("opf:metadata", opf_ns)
        if metadata is None:
            raise ValueError("package metadata is missing")

        def metadata_text(name: str) -> str:
            values = metadata.findall(f"dc:{name}", dc_ns)
            if len(values) != 1:
                raise ValueError(f"package requires exactly one dc:{name}")
            return (values[0].text or "").strip()

        expected_metadata = {
            "identifier": edition.identifier,
            "title": edition.title,
            "creator": edition.author,
            "language": edition.language,
            "description": edition.description,
        }
        for name, expected_value in expected_metadata.items():
            if metadata_text(name) != expected_value:
                raise ValueError(f"dc:{name} does not match the edition contract")
        subjects = [
            (node.text or "").strip()
            for node in metadata.findall("dc:subject", dc_ns)
        ]
        if subjects != list(edition.subjects):
            raise ValueError("dc:subject values do not match the edition contract")
        resources = {
            item.attrib["href"]
            for item in package.findall("opf:manifest/opf:item", opf_ns)
        }
        missing = [href for href in resources if f"EPUB/{href}" not in names]
        if missing:
            raise ValueError(f"manifest resources missing from archive: {missing}")

        metadata_values: dict[str, list[str]] = {}
        for meta in package.findall("opf:metadata/opf:meta", opf_ns):
            property_name = meta.attrib.get("property")
            if property_name:
                metadata_values.setdefault(property_name, []).append((meta.text or "").strip())
        if metadata_values.get("schema:accessMode") != ["textual"]:
            raise ValueError("the only required access mode must be textual")
        if metadata_values.get("schema:accessModeSufficient") != ["textual"]:
            raise ValueError("the sufficient access mode must be textual")
        if metadata_values.get("schema:accessibilitySummary") != [
            edition.accessibility_summary
        ]:
            raise ValueError(
                "accessibility summary does not match the edition contract"
            )

        book = roots["EPUB/book.xhtml"]
        headings, intro = _validate_semantics(book, edition)
        nav = roots["EPUB/nav.xhtml"]
        _validate_navigation(nav, headings, intro.anchor, edition)
        cover = roots["EPUB/cover.xhtml"]
        if cover.attrib.get("lang") != edition.language or cover.attrib.get(
            _qname(XML_NS, "lang")
        ) != edition.language:
            raise ValueError("cover language does not match the edition contract")
        cover_image = cover.find(f".//{_qname(XHTML_NS, 'img')}")
        if cover_image is None or cover_image.attrib.get("alt") != edition.cover_alt:
            raise ValueError("cover alt text does not match the edition contract")

        anchors = {element.attrib["id"] for element in book.iter() if "id" in element.attrib}
        bad_targets = [
            link.attrib.get("href", "")
            for link in nav.findall(f".//{_qname(XHTML_NS, 'a')}")
            if "book.xhtml#" in link.attrib.get("href", "")
            and link.attrib["href"].split("#", 1)[1] not in anchors
        ]
        if bad_targets:
            raise ValueError(f"navigation targets are missing: {bad_targets}")


def _zip_info(name: str, compression: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
    info.compress_type = compression
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


def write_epub(work: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    excluded = {"mimetype", "book.html", "cover-render.png"}
    resources = [
        path
        for path in sorted(work.rglob("*"))
        if path.is_file() and path.name not in excluded
    ]
    with zipfile.ZipFile(output, "w") as archive:
        archive.writestr(
            _zip_info("mimetype", zipfile.ZIP_STORED),
            b"application/epub+zip",
        )
        for path in resources:
            archive.writestr(
                _zip_info(path.relative_to(work).as_posix(), zipfile.ZIP_DEFLATED),
                path.read_bytes(),
                compresslevel=9,
            )


def build(
    root: Path,
    output: Path,
    edition: EditionContract | None = None,
) -> None:
    edition = edition or load_edition_contract(root / "book" / "edition.json")
    source = root / edition.source_path
    if file_sha256(source) != edition.source_sha256:
        raise ValueError("immutable source manuscript hash changed")

    work = root / "build" / "epub"
    if work.exists():
        shutil.rmtree(work)
    epub_dir = work / "EPUB"
    epub_dir.mkdir(parents=True)

    run(
        [
            "typst",
            "compile",
            "--root",
            str(root),
            "--creation-timestamp",
            edition.pdf_creation_timestamp,
            "--pdf-standard",
            "ua-1",
            str(root / "book" / "main.typ"),
            str(root / edition.pdf_relative_path),
        ],
        root,
    )

    html_path = work / "book.html"
    run(
        [
            "typst",
            "compile",
            "--features",
            "html",
            "--root",
            str(root),
            "--creation-timestamp",
            edition.pdf_creation_timestamp,
            str(root / "book" / "main.typ"),
            str(html_path),
        ],
        root,
        TYPST_HTML_WARNING_HEADERS,
    )
    xhtml, headings, intro_anchor = to_xhtml(
        html_path.read_text(encoding="utf-8"),
        edition,
    )

    cover_path = work / "cover-render.png"
    run(
        [
            "typst",
            "compile",
            "--root",
            str(root),
            "--creation-timestamp",
            edition.pdf_creation_timestamp,
            "--pages",
            "1",
            "--ppi",
            "160",
            str(root / "book" / "main.typ"),
            str(cover_path),
        ],
        root,
    )
    shutil.copyfile(cover_path, epub_dir / "cover.png")

    write_text(work / "META-INF" / "container.xml", container_xml())
    write_text(epub_dir / "book.xhtml", xhtml)
    write_text(
        epub_dir / "nav.xhtml",
        nav_xhtml(headings, intro_anchor, edition),
    )
    write_text(epub_dir / "cover.xhtml", cover_xhtml(edition))
    write_text(epub_dir / "package.opf", package_opf(edition))

    write_epub(work, output)
    validate_package(output, edition)
    try:
        output_label = output.relative_to(root)
    except ValueError:
        output_label = output
    print(f"Built {output_label}")
    print(f"Navigation entries: {len(headings)}")
    print(f"Size: {output.stat().st_size} bytes")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    edition = load_edition_contract(root / "book" / "edition.json")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=edition.epub_relative_path,
    )
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else root / args.output
    build(root, output, edition)


if __name__ == "__main__":
    main()
