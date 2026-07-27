#!/usr/bin/env python3
"""Verify that release evidence matches the committed PDF and EPUB."""

from __future__ import annotations

import sys
from pathlib import Path

from beginner_pilot_artifact import sha256_file
from edition_contract import EditionContract, load_edition_contract
from external_release_gates import verify_external_release_gates
from release_common import ReleaseVerificationError, require
from release_epub import EpubFacts, read_epub_facts
from release_evidence import (
    ReleaseEvidence,
    parse_release_evidence,
    validate_evidence_contract,
)
from release_pdf import PdfFacts, read_pdf_facts, validate_pdf_contract
from rights_inventory_contract import (
    RIGHTS_INVENTORY_PATH,
    validate_rights_inventory,
)


def validate_release_identity(
    pdf: PdfFacts,
    epub: EpubFacts,
    edition: EditionContract,
) -> None:
    require(pdf.title == edition.title, "PDF title metadata is incorrect")
    require(pdf.author == edition.author, "PDF author credit is incorrect")
    require(epub.title == edition.title, "EPUB title metadata is incorrect")
    require(epub.author == edition.author, "EPUB creator credit is incorrect")
    require(
        epub.language == edition.language,
        f"EPUB language metadata must be {edition.language}",
    )


def verify_release(root: Path) -> ReleaseEvidence:
    edition_path = root / "book" / "edition.json"
    edition = load_edition_contract(edition_path)
    evidence_path = root / "book" / "references" / "release-evidence.md"
    source_path = root / edition.source_path
    pdf_path = root / edition.pdf_relative_path
    epub_path = root / edition.epub_relative_path
    evidence = parse_release_evidence(evidence_path.read_text(encoding="utf-8"))
    validate_evidence_contract(evidence, edition)
    pdf = read_pdf_facts(pdf_path, root)
    epub = read_epub_facts(epub_path)

    require(
        sha256_file(edition_path) == evidence.edition_contract_sha256,
        "edition contract SHA-256 does not match release evidence",
    )
    require(
        sha256_file(source_path) == edition.source_sha256,
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
    rights_inventory_path = root / RIGHTS_INVENTORY_PATH
    validate_rights_inventory(
        rights_inventory_path.read_text(encoding="utf-8"),
        source_sha256=edition.source_sha256,
        pdf_sha256=evidence.pdf_sha256,
        epub_sha256=evidence.epub_sha256,
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
    validate_release_identity(pdf, epub, edition)
    validate_pdf_contract(pdf)
    require(
        epub.content_entries == evidence.epub_content_entries,
        "EPUB content navigation count does not match evidence",
    )
    require(
        epub.cover_entries == evidence.epub_cover_entries == 1,
        "EPUB must expose exactly one cover navigation entry",
    )
    verify_external_release_gates(root, evidence, edition)
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
