"""Shared synthetic documents for release-verifier tests."""

from __future__ import annotations

import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EVIDENCE = """\
## Artifact identity

| Item | Evidence |
|---|---|
| Edition contract SHA-256 | `dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd` |
| Immutable source SHA-256 | `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` |
| PDF SHA-256 | `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` |
| EPUB SHA-256 | `cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| PDF extent | 123 A5 pages |
| PDF file size | 1,021,520 bytes |
| EPUB navigation | 136 nested content entries plus 1 cover entry |
| EPUB archive size | 137,543 bytes |
| Publication credit | `CS Chánh Niệm + ChatGPT` |
"""

PDFINFO = """\
Title:           Hướng Đến Nhập Lưu
Author:          CS Chánh Niệm + ChatGPT
Tagged:          yes
Suspects:        no
JavaScript:      no
Encrypted:       no
Pages:           123
Page size:       419.528 x 595.276 pts (A5)
Page rot:        0
File size:       1021520 bytes
"""

NAV = b"""\
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:epub="http://www.idpf.org/2007/ops">
  <body>
    <nav epub:type="toc">
      <ol>
        <li><a href="cover.xhtml">Bia</a></li>
        <li><a href="book.xhtml#one">One</a></li>
        <li><a href="book.xhtml#two">Two</a></li>
      </ol>
    </nav>
  </body>
</html>
"""

PACKAGE = b"""\
<package xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Huong Den Nhap Luu</dc:title>
    <dc:creator>CS Chanh Niem + ChatGPT</dc:creator>
    <dc:language>vi</dc:language>
  </metadata>
</package>
"""

FULL_PACKAGE = b"""\
<package xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Huong Den Nhap Luu</dc:title>
    <dc:creator>CS Chanh Niem + ChatGPT</dc:creator>
    <dc:language>vi</dc:language>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml"
          media-type="application/xhtml+xml" properties="nav"/>
    <item id="cover-page" href="cover.xhtml"
          media-type="application/xhtml+xml"/>
    <item id="book" href="book.xhtml"
          media-type="application/xhtml+xml"/>
    <item id="cover-image" href="cover.png"
          media-type="image/png" properties="cover-image"/>
  </manifest>
  <spine>
    <itemref idref="cover-page" linear="yes"/>
    <itemref idref="book" linear="yes"/>
  </spine>
</package>
"""

COVER = b"""\
<html xmlns="http://www.w3.org/1999/xhtml"><body><p>Cover</p></body></html>
"""

BOOK = b"""\
<html xmlns="http://www.w3.org/1999/xhtml">
  <body><h1 id="one">One</h1><h2 id="two">Two</h2></body>
</html>
"""


def write_test_epub(
    path: Path,
    *,
    package: bytes = FULL_PACKAGE,
    nav: bytes = NAV,
) -> None:
    container = b"""\
<?xml version="1.0" encoding="utf-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/package.opf"
              media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "mimetype",
            b"application/epub+zip",
            compress_type=zipfile.ZIP_STORED,
        )
        archive.writestr("META-INF/container.xml", container)
        archive.writestr("EPUB/package.opf", package)
        archive.writestr("EPUB/nav.xhtml", nav)
        archive.writestr("EPUB/cover.xhtml", COVER)
        archive.writestr("EPUB/book.xhtml", BOOK)
        archive.writestr("EPUB/cover.png", b"not inspected by the release verifier")
