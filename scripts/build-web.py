#!/usr/bin/env python3
"""Build a static, byte-reproducible reading website from the Typst book source.

The site is a pure consumer of the existing publication pipeline: it compiles
``book/main.typ`` to semantic HTML with the pinned Typst toolchain, normalizes it
through the same contract used by the EPUB builder, then splits the single
document into clean, linkable pages with a hierarchical sidebar, per-page table
of contents, client-side search, and dark mode.

No independent metadata or locale policy is introduced here. Every reader-facing
string that already lives in ``book/edition.json`` is read through the strict
edition contract; the few editorial strings the website needs (navigation
labels, safety boundary) are kept in this file and are clearly site chrome.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
import shutil
import sys
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html import escape as html_escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
WEB_SOURCE = ROOT / "web"
sys.path.insert(0, str(SCRIPTS))

from edition_contract import load_edition_contract  # noqa: E402

XHTML_NS = "http://www.w3.org/1999/xhtml"
OPENER_KINDS = {
    "introduction-opener": "intro",
    "part-opener": "part",
    "chapter-opener": "chapter",
}
TEXT_TAGS = {"p", "li", "td", "th", "dd", "dt", "figcaption", "blockquote", "cite"}
CORRECTION_URL = (
    "https://github.com/streamentry/streamentry/issues/new"
    "?template=correction.yml"
)
REPO_RAW = "https://raw.githubusercontent.com/streamentry/streamentry/main"


@dataclass(frozen=True)
class Anchor:
    level: int
    anchor: str
    label: str


@dataclass
class Unit:
    kind: str
    slug: str
    title: str
    kicker: str | None
    number: str | None
    nodes: list[ET.Element]
    headings: list[Anchor] = field(default_factory=list)
    part_slug: str | None = None


@dataclass
class NavNode:
    label: str
    slug: str
    number: str | None = None
    children: list["NavNode"] = field(default_factory=list)


def _load_epub_module():
    spec = importlib.util.spec_from_file_location(
        "streamentry_build_epub", SCRIPTS / "build-epub.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/build-epub.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


EPUB = _load_epub_module()


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------

def slugify(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.casefold())
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    stripped = stripped.replace("đ", "d").replace("Đ", "d")
    stripped = re.sub(r"[^a-z0-9]+", "-", stripped)
    return stripped.strip("-") or "trang"


def normalize_search(value: str) -> str:
    # "đ" does not decompose under NFD, so map it to "d" before stripping marks.
    folded = value.casefold().replace("đ", "d")
    decomposed = unicodedata.normalize("NFD", folded)
    ascii_only = (
        "".join(ch for ch in decomposed if not unicodedata.combining(ch))
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    return " ".join(ascii_only.split())


def label_of(element: ET.Element) -> str:
    return " ".join("".join(element.itertext()).split())


def local_name(tag: object) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.split("}", 1)[1] if "}" in tag else tag


def strip_namespaces(element: ET.Element) -> ET.Element:
    if isinstance(element.tag, str):
        element.tag = local_name(element.tag)
    for attribute in list(element.attrib):
        if attribute.startswith("{"):
            del element.attrib[attribute]
    for child in element:
        strip_namespaces(child)
    return element


def to_html(element: ET.Element) -> str:
    return ET.tostring(element, encoding="unicode", method="html")


# --------------------------------------------------------------------------
# Document preparation
# --------------------------------------------------------------------------

def compile_book_html(edition, work: Path) -> str:
    html_path = work / "book.html"
    EPUB.run(
        [
            "typst",
            "compile",
            "--features",
            "html",
            "--root",
            str(ROOT),
            "--creation-timestamp",
            edition.pdf_creation_timestamp,
            str(ROOT / "book" / "main.typ"),
            str(html_path),
        ],
        ROOT,
        EPUB.TYPST_HTML_WARNING_HEADERS,
    )
    return html_path.read_text(encoding="utf-8")


def compile_cover_png(edition, work: Path) -> Path:
    cover_path = work / "cover.png"
    EPUB.run(
        [
            "typst",
            "compile",
            "--root",
            str(ROOT),
            "--creation-timestamp",
            edition.pdf_creation_timestamp,
            "--pages",
            "1",
            "--ppi",
            "200",
            str(ROOT / "book" / "main.typ"),
            str(cover_path),
        ],
        ROOT,
    )
    return cover_path


def main_element(xhtml: str) -> ET.Element:
    document = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", xhtml, count=1)
    document = re.sub(r"^\s*<!DOCTYPE html>\s*", "", document, count=1)
    root = ET.fromstring(document)
    main = root.find(f"{{{XHTML_NS}}}body/{{{XHTML_NS}}}main")
    if main is None:
        raise ValueError("normalized book HTML has no bodymatter main element")
    return main


def opener_kind(element: ET.Element) -> str | None:
    if local_name(element.tag) != "header":
        return None
    classes = element.attrib.get("class", "").split()
    for css_class, kind in OPENER_KINDS.items():
        if css_class in classes:
            return kind
    return None


def chapter_number(header: ET.Element) -> str | None:
    for element in header.iter():
        if "chapter-number" in element.attrib.get("class", "").split():
            text = label_of(element)
            match = re.search(r"([0-9]+|[^\s]+)\s*$", text)
            return match.group(1) if match else None
    return None


def first_heading(element: ET.Element) -> ET.Element | None:
    if re.fullmatch(r"h[1-6]", local_name(element.tag)):
        return element
    for child in element.iter():
        if re.fullmatch(r"h[1-6]", local_name(child.tag)):
            return child
    return None


def is_bare_kicker(element: ET.Element) -> bool:
    if local_name(element.tag) != "p" or element.attrib:
        return False
    if len(list(element)):
        return False
    text = label_of(element)
    return bool(text) and len(text) <= 48 and text == text.upper()


def unique_slug(base: str, used: set[str]) -> str:
    candidate = base
    suffix = 2
    while candidate in used:
        candidate = f"{base}-{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def split_units(main: ET.Element) -> list[Unit]:
    children = list(main)
    starts: list[int] = []
    current_kind = "intro"
    for index, child in enumerate(children):
        kind = opener_kind(child)
        if kind is not None and (index == 0 or kind != "intro"):
            starts.append(index)
            current_kind = kind
        elif local_name(child.tag) == "h1" and current_kind in {"part", "chapter", "back"}:
            starts.append(index)
        # The generated in-book table of contents lives inside the introduction.
    if not starts or starts[0] != 0:
        raise ValueError("book content must begin with the introduction opener")

    bounds = starts + [len(children)]
    used_slugs: set[str] = set()
    units: list[Unit] = []
    part_counter = 0

    for begin, end in zip(bounds, bounds[1:]):
        block = children[begin:end]
        kind = opener_kind(block[0]) or "back"
        kicker = take_trailing_kicker(units) if kind == "back" else None

        if kind == "part":
            part_counter += 1
            heading = first_heading(block[0])
            title = label_of(heading) if heading is not None else f"Phần {part_counter}"
            slug = unique_slug(f"phan-{part_counter}", used_slugs)
            number = None
        elif kind == "chapter":
            heading = first_heading(block[0])
            title = label_of(heading) if heading is not None else "Chương"
            raw_number = chapter_number(block[0])
            if raw_number and raw_number.isdigit():
                number = f"{int(raw_number):02d}"
                slug = unique_slug(f"chuong-{number}-{slugify(title)}", used_slugs)
            else:
                number = None
                slug = unique_slug(slugify(title), used_slugs)
        elif kind == "intro":
            heading = first_heading(block[0])
            title = label_of(heading) if heading is not None else "Lời dẫn"
            slug = unique_slug("gioi-thieu", used_slugs)
            number = None
        else:
            heading = next(
                (element for element in block if local_name(element.tag) == "h1"),
                first_heading(block[0]),
            )
            title = label_of(heading) if heading is not None else "Phần cuối"
            anchor = heading.attrib.get("id", "") if heading is not None else ""
            if anchor and not anchor.startswith("loc-"):
                slug = unique_slug(anchor, used_slugs)
            else:
                slug = unique_slug(slugify(title), used_slugs)
            number = None

        units.append(
            Unit(
                kind=kind,
                slug=slug,
                title=title,
                kicker=kicker,
                number=number,
                nodes=[strip_namespaces(copy.deepcopy(element)) for element in block],
            )
        )
    return units


def take_trailing_kicker(units: list[Unit]) -> str | None:
    if not units or not units[-1].nodes:
        return None
    if is_bare_kicker(units[-1].nodes[-1]):
        return label_of(units[-1].nodes.pop())
    return None


def attach_part_slugs(units: list[Unit]) -> None:
    part_slug: str | None = None
    for unit in units:
        if unit.kind == "part":
            part_slug = unit.slug
        elif unit.kind == "back":
            part_slug = None
        elif unit.kind == "chapter" and part_slug is None:
            unit.part_slug = None
        else:
            unit.part_slug = part_slug


def collect_anchor_pages(units: list[Unit]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for unit in units:
        for node in unit.nodes:
            for element in node.iter():
                anchor = element.attrib.get("id")
                if anchor:
                    mapping[anchor] = unit.slug
    return mapping


def rewrite_links(units: list[Unit], anchor_pages: dict[str, str]) -> None:
    for unit in units:
        for node in unit.nodes:
            for element in node.iter():
                if local_name(element.tag) != "a":
                    continue
                href = element.attrib.get("href", "")
                if not href.startswith("#"):
                    continue
                anchor = href[1:]
                target = anchor_pages.get(anchor)
                if target is None:
                    raise ValueError(f"internal link does not resolve: {href}")
                element.set("href", f"{relative_page(unit.slug, target)}#{anchor}")


def relative_page(from_slug: str | None, to_slug: str) -> str:
    if from_slug is None:
        return f"{to_slug}/index.html"
    return f"../{to_slug}/index.html"


def collect_headings(unit: Unit) -> list[Anchor]:
    headings: list[Anchor] = []
    primary_seen = False
    for node in unit.nodes:
        elements = [node] + list(node.iter())
        for element in elements:
            match = re.fullmatch(r"h([1-6])", local_name(element.tag))
            if not match:
                continue
            anchor = element.attrib.get("id", "")
            label = label_of(element)
            if not anchor or not label:
                continue
            if not primary_seen and int(match.group(1)) == 1:
                primary_seen = True
                continue
            headings.append(Anchor(int(match.group(1)), anchor, label))
    return headings


def unit_deck(unit: Unit) -> str | None:
    """Return the short deck paragraph that introduces a unit, if present."""
    for node in unit.nodes:
        classes = node.attrib.get("class", "").split()
        if "chapter-deck" in classes or "part-deck" in classes:
            return label_of(node)
    return None


# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------

def build_nav(units: list[Unit]) -> list[NavNode]:
    nav: list[NavNode] = []
    part: NavNode | None = None
    appendix: NavNode | None = None
    for unit in units:
        if unit.kind == "intro":
            nav.append(NavNode(unit.title, unit.slug))
            part = None
        elif unit.kind == "part":
            part = NavNode(unit.title, unit.slug)
            nav.append(part)
        elif unit.kind == "chapter":
            node = NavNode(unit.title, unit.slug, number=unit.number)
            if part is not None:
                part.children.append(node)
            else:
                nav.append(node)
        else:
            node = NavNode(unit.title, unit.slug)
            kicker = (unit.kicker or "").strip()
            if kicker.upper().startswith("PHỤ LỤC"):
                if appendix is None:
                    appendix = NavNode("Phụ lục & tra cứu", "")
                    nav.append(appendix)
                node.number = kicker.replace("PHỤ LỤC", "").strip() or None
                appendix.children.append(node)
            else:
                nav.append(node)
            part = None
    return nav


def render_nav(nav: list[NavNode], current: str | None) -> str:
    def link(node: NavNode, group: bool = False) -> str:
        href = relative_page(current, node.slug) if node.slug else ""
        number = (
            f'<span class="toc-num" aria-hidden="true">{html_escape(node.number)}</span>'
            if node.number
            else ""
        )
        label = f'<span class="toc-label">{html_escape(node.label)}</span>'
        if href:
            return (
                f'<a class="toc-link{" toc-group-link" if group else ""}" '
                f'href="{html_escape(href)}" data-slug="{html_escape(node.slug)}">'
                f"{number}{label}</a>"
            )
        return f'<span class="toc-group-label">{number}{label}</span>'

    def items(nodes: list[NavNode]) -> str:
        out = ['<ol class="toc-sublist">']
        for node in nodes:
            if node.children:
                out.append(
                    '<li class="toc-group" data-group="%s"><details open>'
                    "<summary>%s"
                    '<span class="toc-chevron" aria-hidden="true"></span>'
                    "</summary>%s</details></li>"
                    % (
                        html_escape(node.slug or node.label),
                        link(node, group=True),
                        items(node.children),
                    )
                )
            else:
                out.append(f'<li class="toc-item">{link(node)}</li>')
        out.append("</ol>")
        return "".join(out)

    return (
        '<nav class="toc" aria-label="Mục lục sách">'
        f'<div class="toc-scroll">{items(nav)}</div></nav>'
    )


def nav_sequence(nav: list[NavNode]) -> list[NavNode]:
    sequence: list[NavNode] = []
    for node in nav:
        sequence.append(node)
        sequence.extend(node.children)
    return sequence


# --------------------------------------------------------------------------
# Rendering helpers
# --------------------------------------------------------------------------

ICO_MENU = (
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
)
ICO_SEARCH = (
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/>'
    '<path d="m16 16 4 4"/></svg>'
)
ICO_THEME = (
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a7 '
    '7 0 0 0 9.8 9.8Z"/></svg>'
)
ICO_CLOSE = (
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round"><path d="m6 6 12 12M18 6 6 18"/></svg>'
)
ICO_ARROW_L = (
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 6l-6 6 6 6"/></svg>'
)
ICO_ARROW_R = (
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M10 6l6 6-6 6"/></svg>'
)
ICO_DOWNLOAD = (
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 4v11m0 0 4-4m-4 4-4-4M5 19h14"/></svg>'
)

THEME_BOOT = (
    "<script>(function(){try{var t=localStorage.getItem('hdb-theme');"
    "if(t==='light'||t==='dark'){document.documentElement.dataset.theme=t;}"
    "if(localStorage.getItem('hdb-sidebar')==='collapsed'){"
    "document.documentElement.dataset.sidebar='collapsed';}}catch(e){}})();</script>"
)


def render_sidebar(nav: list[NavNode], current: str | None, edition, home_href: str) -> str:
    pdf = f"{REPO_RAW}/{edition.pdf_relative_path}"
    epub = f"{REPO_RAW}/{edition.epub_relative_path}"
    return (
        '<div class="sidebar-head">'
        f'<a class="brand" href="{html_escape(home_href)}" '
        'aria-label="Về trang chủ">'
        '<span class="brand-mark" aria-hidden="true"><span></span></span>'
        f'<span class="brand-text"><strong>{html_escape(edition.title)}</strong>'
        f'<small>{html_escape(edition.cover_kicker)}</small></span></a>'
        '<button class="icon-btn sidebar-close" type="button" '
        f'data-action="close-sidebar" aria-label="Đóng mục lục">{ICO_CLOSE}</button>'
        "</div>"
        f'<div class="sidebar-body">{render_nav(nav, current)}</div>'
        '<div class="sidebar-foot">'
        f'<a class="side-download" href="{html_escape(pdf)}">{ICO_DOWNLOAD} PDF</a>'
        f'<a class="side-download" href="{html_escape(epub)}">{ICO_DOWNLOAD} EPUB</a>'
        '<a class="side-download side-download-quiet" '
        f'href="{relative_page(current, "ban-do-nguon")}">Bản đồ nguồn</a>'
        "</div>"
    )


def render_page_toc(unit: Unit) -> str:
    if not unit.headings:
        return ""
    items = []
    for heading in unit.headings:
        if heading.level > 4:
            continue
        items.append(
            f'<li class="ptoc-item ptoc-l{heading.level}">'
            f'<a href="#{html_escape(heading.anchor)}">{html_escape(heading.label)}</a></li>'
        )
    return (
        '<aside class="page-toc" aria-label="Trong trang này">'
        '<p class="ptoc-title">Trong trang</p>'
        f'<ol class="ptoc-list">{"".join(items)}</ol></aside>'
    )


def render_pager(sequence: list[NavNode], index: int, current: str) -> str:
    if index < 0:
        return ""
    previous = sequence[index - 1] if index > 0 else None
    following = sequence[index + 1] if index + 1 < len(sequence) else None
    cells = []
    if previous is not None and previous.slug:
        cells.append(
            f'<a class="pager-link pager-prev" href="{relative_page(current, previous.slug)}">'
            f'{ICO_ARROW_L}<span><small>Trước</small>'
            f"<strong>{html_escape(previous.label)}</strong></span></a>"
        )
    if following is not None and following.slug:
        cells.append(
            f'<a class="pager-link pager-next" href="{relative_page(current, following.slug)}">'
            f'<span><small>Sau</small>'
            f"<strong>{html_escape(following.label)}</strong></span>{ICO_ARROW_R}</a>"
        )
    if not cells:
        return ""
    return f'<nav class="pager" aria-label="Chuyển chương">{"".join(cells)}</nav>'


def render_footer(edition) -> str:
    pdf = f"{REPO_RAW}/{edition.pdf_relative_path}"
    epub = f"{REPO_RAW}/{edition.epub_relative_path}"
    return f"""<footer class="site-foot">
  <div class="foot-grid">
    <div>
      <p class="foot-brand">{html_escape(edition.title)}</p>
      <p class="foot-note">{html_escape(edition.description)}</p>
    </div>
    <div>
      <p class="foot-head">Đọc offline</p>
      <a href="{html_escape(pdf)}">PDF · bố cục A5</a>
      <a href="{html_escape(epub)}">EPUB 3 · chữ tự dàn</a>
    </div>
    <div>
      <p class="foot-head">Tin cậy</p>
      <a href="{html_escape(CORRECTION_URL)}">Gửi góp ý hoặc sửa sai</a>
      <a href="https://github.com/streamentry/streamentry">Mã nguồn và bằng chứng</a>
    </div>
  </div>
  <p class="foot-fine">
    Đây là bản biên tập, chưa được xác nhận độc lập. Kho chưa có giấy phép công khai;
    tệp có thể tải xuống không tự tạo quyền sao chép, tái phân phối hay dịch.
    {html_escape(edition.cover_edition_label)}.
  </p>
</footer>"""


def render_search_dialog() -> str:
    return (
        '<dialog class="search-dialog" id="search-dialog" aria-label="Tìm trong sách">'
        '<form method="dialog" class="search-form">'
        f'<span class="search-icon" aria-hidden="true">{ICO_SEARCH}</span>'
        '<label class="visually-hidden" for="search-input">Từ khóa</label>'
        '<input id="search-input" type="search" autocomplete="off" spellcheck="false" '
        'placeholder="Tìm chương, thuật ngữ, câu hỏi…">'
        f'<button class="icon-btn search-close" type="button" data-action="search-close" '
        f'aria-label="Đóng tìm kiếm">{ICO_CLOSE}</button></form>'
        '<div class="search-results" id="search-results" role="listbox" '
        'aria-label="Kết quả"></div>'
        '<p class="search-hint">Gõ không dấu cũng được. Kết quả nhảy tới đúng mục.</p>'
        "</dialog>"
    )


def render_shell(
    *,
    edition,
    head_title: str,
    description: str,
    base: str,
    body_class: str,
    content: str,
    sidebar: str,
    page_toc: str = "",
    pager: str = "",
    topbar_title: str = "",
) -> str:
    return f"""<!doctype html>
<html lang="{html_escape(edition.language)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{html_escape(head_title)}</title>
<meta name="description" content="{html_escape(description)}">
<meta property="og:type" content="book">
<meta property="og:site_name" content="{html_escape(edition.title)}">
<meta property="og:title" content="{html_escape(head_title)}">
<meta property="og:description" content="{html_escape(description)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;0,7..72,600;1,7..72,400&display=swap">
<link rel="stylesheet" href="{base}assets/site.css">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
{THEME_BOOT}
</head>
<body class="{body_class}" data-base="{base}">
<a class="skip-link" href="#main">Bỏ qua điều hướng</a>
<div class="reading-progress" aria-hidden="true"><span id="progress-bar"></span></div>
<div class="layout">
  <aside class="sidebar" id="sidebar">{sidebar}</aside>
  <div class="page">
    <header class="topbar">
      <button class="icon-btn topbar-menu" type="button" data-action="open-sidebar" aria-label="Mở mục lục">{ICO_MENU}</button>
      <a class="topbar-home" href="{base}index.html" aria-label="Trang chủ">{ICO_ARROW_L}<span>{html_escape(edition.title)}</span></a>
      <span class="topbar-title">{html_escape(topbar_title)}</span>
      <div class="topbar-actions">
        <button class="icon-btn" type="button" data-action="search" aria-label="Tìm trong sách">{ICO_SEARCH}</button>
        <button class="icon-btn theme-toggle" type="button" data-action="theme" aria-label="Đổi chế độ sáng tối">{ICO_THEME}</button>
      </div>
    </header>
    <main id="main" class="content">{content}</main>
    {pager}
    {render_footer(edition)}
  </div>
  {page_toc}
</div>
<div class="scrim" data-action="close-sidebar" hidden></div>
{render_search_dialog()}
<script src="{base}assets/site.js" defer></script>
</body>
</html>
"""


def render_reading_page(
    unit: Unit,
    edition,
    *,
    base: str,
    sidebar: str,
    page_toc: str,
    pager: str,
    extra: str = "",
) -> str:
    body: list[str] = []
    if unit.kicker and unit.kicker.casefold() != unit.title.casefold():
        body.append(f'<p class="eyebrow kicker">{html_escape(unit.kicker)}</p>')
    for node in unit.nodes:
        body.append(to_html(node))
    body.append(extra)
    return render_shell(
        edition=edition,
        head_title=f"{unit.title} · {edition.title}",
        description=unit_deck(unit) or edition.description,
        base=base,
        body_class=f"page page-{unit.kind}",
        content=f'<article class="prose">{"".join(body)}</article>',
        sidebar=sidebar,
        page_toc=page_toc,
        pager=pager,
        topbar_title=unit.title,
    )


# --------------------------------------------------------------------------
# Landing page
# --------------------------------------------------------------------------

START_ROUTE = (
    ("1", "Bắt đầu với một buổi ngồi an toàn", "chapter", "01"),
    ("2", "Giữ nhịp bảy ngày và đọc nền giáo lý gần nhất", "chapter", "02"),
    ("3", "Tra nhãn khi đang hành, ghi ngắn mỗi ngày", "kicker", "PHỤ LỤC B"),
    ("4", "Trước khi tăng thời lượng hoặc đi khóa, đọc an toàn", "chapter", "09"),
)

SOURCE_LEGEND = (
    ("source-kinh", "KINH", "Kinh điển Pāli Nikāya, kèm mã nguồn và ngữ cảnh."),
    ("source-luan-giai", "LUẬN GIẢI", "A-tỳ-đàm và chú giải Theravāda về sau."),
    ("source-thanh-tinh-dao", "THANH TỊNH ĐẠO", "Hệ thống Visuddhimagga, không giả làm lời Phật."),
    ("source-mahasi", "MAHĀSI", "Chỉ dẫn thực hành của truyền thống Mahāsi."),
    ("source-nghien-cuu", "Y TẾ & NGHIÊN CỨU", "Nguồn hiện đại, chỉ cho câu hỏi sức khỏe."),
    ("source-bien-soan", "BIÊN SOẠN", "Giải thích, ví dụ và lịch do sách tổng hợp."),
)


def render_landing(units: list[Unit], nav: list[NavNode], edition, cover_size: tuple[int, int]) -> str:
    by_slug = {unit.slug: unit for unit in units}
    safety_slug = next(
        (u.slug for u in units if u.kind == "chapter" and u.number and int(u.number) == 9),
        "gioi-thieu",
    )
    pdf = f"{REPO_RAW}/{edition.pdf_relative_path}"
    epub = f"{REPO_RAW}/{edition.epub_relative_path}"
    width, height = cover_size or (0, 0)
    size_attrs = f' width="{width}" height="{height}"' if width else ""
    title_html = " ".join(
        html_escape(line) if index == 0 else f"<em>{html_escape(line)}</em>"
        for index, line in enumerate(edition.cover_title_lines)
    )

    def card(node: NavNode) -> str:
        unit = by_slug.get(node.slug)
        deck = unit_deck(unit) if unit is not None else None
        number = (
            f'<span class="chapter-card-num">{html_escape(node.number)}</span>'
            if node.number
            else '<span class="chapter-card-num chapter-card-num-empty" aria-hidden="true"></span>'
        )
        deck_html = (
            f'<span class="chapter-card-deck">{html_escape(deck)}</span>' if deck else ""
        )
        return (
            f'<a class="chapter-card" href="{relative_page(None, node.slug)}">'
            f"{number}"
            f'<span class="chapter-card-text"><strong>{html_escape(node.label)}</strong>'
            f"{deck_html}</span></a>"
        )

    groups: list[str] = []
    for node in nav:
        if node.children:
            heading = (
                f'<a class="chapter-group-title" href="{relative_page(None, node.slug)}">'
                f"{html_escape(node.label)}</a>"
                if node.slug
                else f'<span class="chapter-group-title">{html_escape(node.label)}</span>'
            )
            groups.append(
                f'<section class="chapter-group">{heading}'
                f'<div class="chapter-grid">{"".join(card(child) for child in node.children)}</div>'
                "</section>"
            )
        else:
            groups.append(
                f'<section class="chapter-group chapter-group-single">'
                f'<div class="chapter-grid">{card(node)}</div></section>'
            )

    by_number = {
        unit.number: unit.slug for unit in units if unit.number and unit.kind == "chapter"
    }
    by_kicker = {
        (unit.kicker or "").strip().upper(): unit.slug for unit in units if unit.kicker
    }

    route_items = []
    for number, text, kind, key in START_ROUTE:
        slug = by_number.get(key) if kind == "chapter" else by_kicker.get(key)
        href = relative_page(None, slug) if slug else "gioi-thieu/index.html"
        route_items.append(
            f'<li class="route-step"><a class="route-link" href="{html_escape(href)}">'
            f'<span class="route-num">{number}</span>'
            f"<span>{html_escape(text)}</span></a></li>"
        )
    route = "".join(route_items)

    legend = "".join(
        f'<li class="legend-item"><span class="source-badge {css}">{html_escape(label)}</span>'
        f"<span>{html_escape(gloss)}</span></li>"
        for css, label, gloss in SOURCE_LEGEND
    )

    content = f"""<section class="hero">
  <div class="hero-visual">
    <div class="book">
      <img src="assets/cover.png" alt="{html_escape(edition.cover_alt)}"{size_attrs}>
    </div>
  </div>
  <div class="hero-copy">
    <p class="eyebrow">{html_escape(edition.cover_edition_label)}</p>
    <h1>{title_html}</h1>
    <p class="hero-lede">{html_escape(edition.description)}</p>
    <p class="hero-author">{html_escape(edition.author_label)} · {html_escape(edition.author)}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="gioi-thieu/index.html">Bắt đầu đọc</a>
      <a class="btn btn-ghost" href="{html_escape(pdf)}">{ICO_DOWNLOAD} PDF</a>
      <a class="btn btn-ghost" href="{html_escape(epub)}">{ICO_DOWNLOAD} EPUB</a>
    </div>
  </div>
</section>

<section class="epigraph-band" aria-label="Đề từ">
  <blockquote>
    <p>{"<br>".join(html_escape(line) for line in edition.cover_epigraph_lines)}</p>
    <cite>{html_escape(edition.cover_epigraph_source)}</cite>
  </blockquote>
</section>

<section class="section start-here">
  <h2 class="section-title">Bắt đầu ở đây</h2>
  <p class="section-lede">Không cần đọc tuần tự như một giáo trình. Bốn bước dưới đưa bạn từ trang đầu đến một buổi ngồi an toàn.</p>
  <ol class="route">{route}</ol>
</section>

<section class="section chapters">
  <h2 class="section-title">Nội dung sách</h2>
  <p class="section-lede">Mỗi chương mở trên một trang riêng, có mục lục trong trang, nút chuyển chương và tìm kiếm toàn sách.</p>
  {"".join(groups)}
</section>

<section class="section sources">
  <h2 class="section-title">Sáu dấu nguồn</h2>
  <p class="section-lede">Mỗi nhận định gắn với một dấu nguồn. Dấu giữ cho lời kinh, lời giải thích về sau, chỉ dẫn thực hành và lời biên soạn không bị trộn thành một giọng.</p>
  <ul class="legend">{legend}</ul>
</section>

<section class="section boundary">
  <h2 class="section-title">An toàn, giới hạn và quyền</h2>
  <div class="boundary-grid">
    <div class="boundary-card boundary-safety">
      <p class="eyebrow">An toàn trước</p>
      <p>Nếu có dấu hiệu nguy cơ hoặc suy giảm sinh hoạt, dừng buổi hành và tìm hỗ trợ sớm thay vì cố hoàn thành lịch. Trường hợp cấp cứu ở Việt Nam gọi <strong>115</strong>.</p>
      <a class="link-arrow" href="{relative_page(None, safety_slug)}">Đọc Chương 9 về an toàn {ICO_ARROW_R}</a>
    </div>
    <div class="boundary-card">
      <p class="eyebrow">Trạng thái</p>
      <p>Đây là bản biên tập chưa được xác nhận độc lập. Quyền tái phân phối, phản biện giáo lý, phản biện an toàn lâm sàng, thử độc giả mới và thử ứng dụng đọc vẫn còn mở.</p>
    </div>
    <div class="boundary-card">
      <p class="eyebrow">Quyền</p>
      <p>Kho chưa có giấy phép công khai. Tệp có thể tải xuống không tự tạo quyền sao chép, tái phân phối, in bán hay dịch.</p>
    </div>
    <div class="boundary-card">
      <p class="eyebrow">Sửa sai</p>
      <p>Phát hiện lỗi nguồn, câu chữ hoặc an toàn, hãy gửi kèm vị trí và đề xuất cụ thể.</p>
      <a class="link-arrow" href="{html_escape(CORRECTION_URL)}">Mở biểu mẫu góp ý {ICO_ARROW_R}</a>
    </div>
  </div>
</section>"""

    sidebar = render_sidebar(nav, None, edition, "index.html")
    return render_shell(
        edition=edition,
        head_title=f"{edition.title} · {edition.cover_kicker}",
        description=edition.description,
        base="",
        body_class="page page-landing",
        content=content,
        sidebar=sidebar,
        topbar_title=edition.cover_kicker,
    )


def render_not_found(edition) -> str:
    content = (
        '<article class="prose not-found">'
        '<p class="eyebrow">404</p>'
        "<h1>Không tìm thấy trang</h1>"
        '<p>Đường dẫn này không tồn tại. Trở về trang chủ hoặc mở mục lục để tìm chương.</p>'
        '<p><a class="btn btn-primary" href="index.html">Về trang chủ</a></p>'
        "</article>"
    )
    return render_shell(
        edition=edition,
        head_title=f"Không tìm thấy · {edition.title}",
        description="Trang không tồn tại.",
        base="",
        body_class="page page-back",
        content=content,
        sidebar="",
        topbar_title="404",
    )


# --------------------------------------------------------------------------
# Search index
# --------------------------------------------------------------------------

def build_search_entries(units: list[Unit]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for unit in units:
        current_anchor: str | None = None
        current_title = ""
        text: list[str] = []

        def flush() -> None:
            if current_anchor is None:
                return
            snippet = " ".join(" ".join(text).split())[:420]
            entries.append(
                {
                    "p": unit.slug,
                    "a": current_anchor,
                    "t": current_title,
                    "d": snippet,
                    "n": normalize_search(f"{current_title} {snippet}"),
                }
            )

        for node in unit.nodes:
            for element in node.iter():
                name = local_name(element.tag)
                if re.fullmatch(r"h[1-6]", name):
                    flush()
                    current_anchor = element.attrib.get("id") or ""
                    current_title = label_of(element)
                    text = []
                elif name in TEXT_TAGS and not len(list(element)):
                    value = " ".join((element.text or "").split())
                    if value:
                        text.append(value)
        flush()
    return entries


def png_size(path: Path) -> tuple[int, int]:
    try:
        data = path.read_bytes()[:24]
    except OSError:
        return (0, 0)
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return (0, 0)
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def write_page(output: Path, slug: str, html: str) -> None:
    directory = output / slug
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "index.html").write_text(html, encoding="utf-8")


def build(root: Path, output: Path, edition, base_url: str) -> None:
    source = root / edition.source_path
    if EPUB.file_sha256(source) != edition.source_sha256:
        raise ValueError("immutable source manuscript hash changed")

    work = root / "build" / "web-src"
    work.mkdir(parents=True, exist_ok=True)

    raw_html = compile_book_html(edition, work)
    cover_png = compile_cover_png(edition, work)
    xhtml, _headings, _intro = EPUB.to_xhtml(raw_html, edition)
    units = split_units(main_element(xhtml))
    attach_part_slugs(units)
    rewrite_links(units, collect_anchor_pages(units))
    for unit in units:
        unit.headings = collect_headings(unit)

    nav = build_nav(units)
    sequence = [node for node in nav_sequence(nav) if node.slug]
    sequence_index = {node.slug: index for index, node in enumerate(sequence)}

    if output.exists():
        shutil.rmtree(output)
    (output / "assets").mkdir(parents=True)
    shutil.copyfile(cover_png, output / "assets" / "cover.png")
    for asset in sorted((WEB_SOURCE / "assets").iterdir()):
        shutil.copyfile(asset, output / "assets" / asset.name)

    for unit in units:
        base = "../"
        page_toc = render_page_toc(unit)
        pager = render_pager(sequence, sequence_index.get(unit.slug, -1), unit.slug)
        extra = ""
        if unit.kind == "part":
            part_node = next((node for node in nav if node.slug == unit.slug), None)
            if part_node and part_node.children:
                links = "".join(
                    f'<a class="part-index-link" href="{relative_page(unit.slug, child.slug)}">'
                    f'<span class="toc-num" aria-hidden="true">{html_escape(child.number or "")}</span>'
                    f"<span>{html_escape(child.label)}</span></a>"
                    for child in part_node.children
                )
                extra = (
                    '<nav class="part-index" aria-label="Các chương trong phần này">'
                    f"{links}</nav>"
                )
        html = render_reading_page(
            unit,
            edition,
            base=base,
            sidebar=render_sidebar(nav, unit.slug, edition, "../index.html"),
            page_toc=page_toc,
            pager=pager,
            extra=extra,
        )
        write_page(output, unit.slug, html)

    landing = render_landing(units, nav, edition, png_size(cover_png))
    (output / "index.html").write_text(landing, encoding="utf-8")
    (output / "404.html").write_text(render_not_found(edition), encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")

    index = {"v": 1, "entries": build_search_entries(units)}
    (output / "assets" / "search-index.json").write_text(
        json.dumps(index, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
        encoding="utf-8",
    )

    urls = [f"{base_url}/"] + [f"{base_url}/{node.slug}/" for node in sequence]
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{html_escape(url)}</loc></url>" for url in urls)
        + "\n</urlset>\n"
    )
    (output / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (output / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml\n", encoding="utf-8"
    )

    try:
        label = output.relative_to(root)
    except ValueError:
        label = output
    print(f"Built web edition into {label}")
    print(f"Reading pages: {len(units)}")
    print(f"Search entries: {len(index['entries'])}")
    print(f"Navigation groups: {len(nav)}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    edition = load_edition_contract(root / "book" / "edition.json")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("build/web"))
    parser.add_argument("--base-url", default="https://streamentry.github.io/streamentry")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else root / args.output
    build(root, output, edition, args.base_url.rstrip("/"))


if __name__ == "__main__":
    main()

