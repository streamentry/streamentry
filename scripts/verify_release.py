#!/usr/bin/env python3
"""Verify that release evidence matches the committed PDF and EPUB."""

from __future__ import annotations

import sys
from pathlib import Path

from beginner_pilot_artifact import sha256_file
from release_common import ReleaseVerificationError, require
from release_epub import read_epub_facts
from release_evidence import (
    IMMUTABLE_SOURCE_SHA256,
    PUBLICATION_CREDIT,
    ReleaseEvidence,
    parse_release_evidence,
    validate_evidence_contract,
)
from release_pdf import read_pdf_facts, validate_pdf_contract


TITLE = "Hướng Đến Nhập Lưu"
LANGUAGE = "vi"


def verify_release(root: Path) -> ReleaseEvidence:
    evidence_path = root / "book" / "references" / "release-evidence.md"
    source_path = root / "con-duong-niem-xu-mahasi-hop-nhat.md"
    pdf_path = root / "dist" / "huong-den-nhap-luu.pdf"
    epub_path = root / "dist" / "huong-den-nhap-luu.epub"
    evidence = parse_release_evidence(evidence_path.read_text(encoding="utf-8"))
    validate_evidence_contract(evidence)
    pdf = read_pdf_facts(pdf_path, root)
    epub = read_epub_facts(epub_path)

    require(
        sha256_file(source_path) == IMMUTABLE_SOURCE_SHA256,
        "immutable source SHA-256 does not match the source contract",
    )
    require(
        sha256_file(pdf_path) == evidence.pdf_sha256,
        "PDF SHA-256 does not match release evidence",
    )
    require(
        sha256_file(epub_path) == evidence.epub_sha256,
        "EPUB SHA-256 does not match release evidence",
    )
    require(pdf.pages == evidence.pdf_pages, "PDF page count does not match evidence")
    require(
        pdf.file_size == evidence.pdf_size == pdf_path.stat().st_size,
        "PDF file size does not match evidence",
    )
    require(
        epub_path.stat().st_size == evidence.epub_size,
        "EPUB file size does not match evidence",
    )
    require(pdf.title == TITLE, "PDF title metadata is incorrect")
    require(pdf.author == PUBLICATION_CREDIT, "PDF author credit is incorrect")
    validate_pdf_contract(pdf)
    require(epub.title == TITLE, "EPUB title metadata is incorrect")
    require(epub.author == PUBLICATION_CREDIT, "EPUB creator credit is incorrect")
    require(epub.language == LANGUAGE, "EPUB language metadata must be vi")
    require(
        epub.content_entries == evidence.epub_content_entries,
        "EPUB content navigation count does not match evidence",
    )
    require(
        epub.cover_entries == evidence.epub_cover_entries == 1,
        "EPUB must expose exactly one cover navigation entry",
    )
    return evidence


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    try:
        evidence = verify_release(root)
    except (OSError, ReleaseVerificationError, ValueError) as error:
        print(f"Release verification failed: {error}", file=sys.stderr)
        raise SystemExit(2) from error
    print(
        "Verified release evidence: "
        f"PDF {evidence.pdf_pages} pages, "
        f"EPUB {evidence.epub_content_entries} content entries, "
        "hashes and metadata match."
    )


if __name__ == "__main__":
    main()
