"""Read and enforce the fixed reflowable EPUB release contract."""

from __future__ import annotations

import zipfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

from beginner_pilot_artifact import verify_epub_structure
from release_common import ReleaseVerificationError


XHTML_NS = "http://www.w3.org/1999/xhtml"
EPUB_NS = "http://www.idpf.org/2007/ops"
OPF_NS = "http://www.idpf.org/2007/opf"
DC_NS = "http://purl.org/dc/elements/1.1/"
CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"
PACKAGE_MEDIA_TYPE = "application/oebps-package+xml"
PACKAGE_PATH = "EPUB/package.opf"
NAV_PATH = "EPUB/nav.xhtml"
XML_BASE_ATTRIBUTE = "{http://www.w3.org/XML/1998/namespace}base"
EXPECTED_MANIFEST = {
    ("nav", "nav.xhtml", "application/xhtml+xml", frozenset({"nav"})),
    ("cover-page", "cover.xhtml", "application/xhtml+xml", frozenset()),
    ("book", "book.xhtml", "application/xhtml+xml", frozenset()),
    ("cover-image", "cover.png", "image/png", frozenset({"cover-image"})),
}
EXPECTED_SPINE = (
    frozenset({("idref", "cover-page"), ("linear", "yes")}),
    frozenset({("idref", "book"), ("linear", "yes")}),
)


@dataclass(frozen=True)
class EpubFacts:
    title: str
    author: str
    language: str
    content_entries: int
    cover_entries: int


def _required_text(root: ET.Element, path: str, namespaces: dict[str, str]) -> str:
    elements = root.findall(path, namespaces)
    if len(elements) != 1 or not (elements[0].text or "").strip():
        raise ReleaseVerificationError(f"EPUB metadata is missing: {path}")
    return (elements[0].text or "").strip()


def _reject_base_or_script(root: ET.Element, label: str, *, xhtml: bool) -> None:
    for element in root.iter():
        if XML_BASE_ATTRIBUTE in element.attrib:
            raise ReleaseVerificationError(f"{label} must not contain xml:base")
        local_name = element.tag.rsplit("}", 1)[-1].lower()
        if xhtml and local_name in {"base", "script"}:
            raise ReleaseVerificationError(
                f"{label} must not contain active {local_name} elements"
            )


def _link_label(link: ET.Element) -> str:
    return " ".join("".join(link.itertext()).split()) or link.get(
        "aria-label", ""
    ).strip()


def _validate_content_links(
    name: str,
    root: ET.Element,
    document_ids: dict[str, set[str]],
) -> None:
    external_labels: dict[str, str] = {}
    for link in root.findall(f".//{{{XHTML_NS}}}a"):
        href = link.get("href", "").strip()
        if not href:
            raise ReleaseVerificationError(
                f"EPUB content {name} contains a link without a target"
            )
        label = _link_label(link)
        if not label:
            raise ReleaseVerificationError(
                f"EPUB content {name} contains an unlabelled link: {href}"
            )
        if href.startswith("#"):
            fragment = unquote(href[1:])
            if not fragment or fragment not in document_ids[name]:
                raise ReleaseVerificationError(
                    f"EPUB content link does not resolve in {name}: {href}"
                )
            continue

        target = urlsplit(href)
        if (
            target.scheme != "https"
            or not target.netloc
            or target.username is not None
            or target.password is not None
        ):
            raise ReleaseVerificationError(
                "EPUB content links must use a local fragment or absolute "
                f"HTTPS URL: {href}"
            )
        label_key = label.casefold()
        previous = external_labels.setdefault(label_key, href)
        if previous != href:
            raise ReleaseVerificationError(
                "EPUB external links to different destinations require "
                f"distinct labels: {label}"
            )


def parse_epub_documents(
    nav_document: bytes,
    package_document: bytes,
    content_documents: dict[str, bytes] | None = None,
) -> EpubFacts:
    try:
        nav_root = ET.fromstring(nav_document)
        package_root = ET.fromstring(package_document)
    except ET.ParseError as error:
        raise ReleaseVerificationError(f"EPUB XML is malformed: {error}") from error
    _reject_base_or_script(nav_root, "EPUB navigation", xhtml=True)
    _reject_base_or_script(package_root, "EPUB package", xhtml=False)
    toc_matches = [
        nav
        for nav in nav_root.findall(f".//{{{XHTML_NS}}}nav")
        if nav.get(f"{{{EPUB_NS}}}type") == "toc"
    ]
    if len(toc_matches) != 1:
        raise ReleaseVerificationError("EPUB must contain exactly one TOC navigation")
    links = toc_matches[0].findall(f".//{{{XHTML_NS}}}a")
    hrefs = [link.get("href", "") for link in links]
    if not hrefs or any(not href for href in hrefs):
        raise ReleaseVerificationError("EPUB TOC contains an empty navigation target")
    if len(hrefs) != len(set(hrefs)):
        raise ReleaseVerificationError("EPUB TOC navigation targets must be unique")

    document_ids: dict[str, set[str]] = {}
    if content_documents is not None:
        roots: dict[str, ET.Element] = {}
        try:
            for name, document in content_documents.items():
                root = ET.fromstring(document)
                _reject_base_or_script(root, f"EPUB content {name}", xhtml=True)
                roots[name] = root
                document_ids[name] = {
                    element_id
                    for element in root.iter()
                    if (element_id := element.get("id"))
                }
        except ET.ParseError as error:
            raise ReleaseVerificationError(
                f"EPUB content document is malformed: {error}"
            ) from error

        for name, root in roots.items():
            _validate_content_links(name, root, document_ids)

        for href in hrefs:
            path, separator, fragment = href.partition("#")
            if path == "cover.xhtml" and not separator:
                continue
            if path != "book.xhtml" or not separator or not fragment:
                raise ReleaseVerificationError(
                    f"EPUB TOC target is outside the canonical content: {href}"
                )
            if fragment not in document_ids.get(path, set()):
                raise ReleaseVerificationError(
                    f"EPUB TOC target does not resolve: {href}"
                )

    cover_entries = sum(href == "cover.xhtml" for href in hrefs)
    namespaces = {"opf": OPF_NS, "dc": DC_NS}
    return EpubFacts(
        title=_required_text(package_root, "opf:metadata/dc:title", namespaces),
        author=_required_text(package_root, "opf:metadata/dc:creator", namespaces),
        language=_required_text(package_root, "opf:metadata/dc:language", namespaces),
        content_entries=len(links) - cover_entries,
        cover_entries=cover_entries,
    )


def _read_package(archive: zipfile.ZipFile) -> tuple[bytes, ET.Element]:
    container = ET.fromstring(archive.read("META-INF/container.xml"))
    rootfiles = container.findall(f".//{{{CONTAINER_NS}}}rootfile")
    if len(rootfiles) != 1:
        raise ReleaseVerificationError(
            "EPUB release must contain exactly one package rootfile"
        )
    rootfile = rootfiles[0]
    if (
        rootfile.get("full-path") != PACKAGE_PATH
        or rootfile.get("media-type") != PACKAGE_MEDIA_TYPE
    ):
        raise ReleaseVerificationError(
            "EPUB rootfile does not select the canonical package document"
        )
    package_document = archive.read(PACKAGE_PATH)
    package_root = ET.fromstring(package_document)
    _reject_base_or_script(package_root, "EPUB package", xhtml=False)
    return package_document, package_root


def _validate_manifest_and_spine(package_root: ET.Element) -> None:
    manifest_items = package_root.findall(
        f".//{{{OPF_NS}}}manifest/{{{OPF_NS}}}item"
    )
    actual_manifest = {
        (
            item.get("id", ""),
            item.get("href", ""),
            item.get("media-type", ""),
            frozenset(item.get("properties", "").split()),
        )
        for item in manifest_items
    }
    if (
        len(manifest_items) != len(EXPECTED_MANIFEST)
        or actual_manifest != EXPECTED_MANIFEST
    ):
        raise ReleaseVerificationError(
            "EPUB package manifest is not the canonical fixed publication set"
        )
    spine = package_root.find(f"{{{OPF_NS}}}spine")
    if spine is None or spine.attrib:
        raise ReleaseVerificationError(
            "EPUB package spine is missing or carries unexpected attributes"
        )
    spine_items = tuple(
        frozenset(item.attrib.items())
        for item in spine.findall(f"{{{OPF_NS}}}itemref")
    )
    if spine_items != EXPECTED_SPINE:
        raise ReleaseVerificationError(
            "EPUB package spine must contain only cover then book"
        )


def read_epub_facts(path: Path) -> EpubFacts:
    verify_epub_structure(path)
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise ReleaseVerificationError(
                    "EPUB archive contains duplicate entry names"
                )
            package_document, package_root = _read_package(archive)
            _validate_manifest_and_spine(package_root)
            return parse_epub_documents(
                archive.read(NAV_PATH),
                package_document,
                {
                    "cover.xhtml": archive.read("EPUB/cover.xhtml"),
                    "book.xhtml": archive.read("EPUB/book.xhtml"),
                },
            )
    except (KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        raise ReleaseVerificationError(
            f"EPUB release documents are missing or malformed: {error}"
        ) from error
