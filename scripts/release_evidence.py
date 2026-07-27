"""Parse and validate the machine-bound artifact table in release evidence."""

from __future__ import annotations

import re
from dataclasses import dataclass

from edition_contract import EDITION, EditionContract
from release_common import ReleaseVerificationError, require


PUBLICATION_CREDIT = EDITION.author
IMMUTABLE_SOURCE_SHA256 = EDITION.source_sha256
ARTIFACT_LABELS = {
    "Edition contract SHA-256",
    "Immutable source SHA-256",
    "PDF SHA-256",
    "EPUB SHA-256",
    "PDF extent",
    "PDF file size",
    "EPUB navigation",
    "EPUB archive size",
    "Publication credit",
}


@dataclass(frozen=True)
class ReleaseEvidence:
    edition_contract_sha256: str
    source_sha256: str
    pdf_sha256: str
    epub_sha256: str
    pdf_pages: int
    pdf_size: int
    epub_content_entries: int
    epub_cover_entries: int
    epub_size: int
    publication_credit: str


def _artifact_identity_table(markdown: str) -> list[str]:
    if re.search(
        r"<!--|-->|<![A-Za-z]|<\s*/?\s*[A-Za-z][^>]*>|^\s*(?:```|~~~)",
        markdown,
        flags=re.MULTILINE,
    ):
        raise ReleaseVerificationError(
            "release evidence must not contain hidden raw HTML or fenced blocks"
        )
    headings = list(
        re.finditer(r"^## Artifact identity[ \t]*$", markdown, flags=re.MULTILINE)
    )
    if len(headings) != 1:
        raise ReleaseVerificationError(
            "release evidence must contain exactly one Artifact identity section"
        )
    section_start = headings[0].end()
    next_heading = re.search(
        r"^## [^\n]+$", markdown[section_start:], flags=re.MULTILINE
    )
    section_end = (
        section_start + next_heading.start() if next_heading is not None else len(markdown)
    )
    lines = markdown[section_start:section_end].splitlines()
    header_indexes = [
        index
        for index, line in enumerate(lines)
        if line.strip() == "| Item | Evidence |"
    ]
    if len(header_indexes) != 1:
        raise ReleaseVerificationError(
            "Artifact identity must contain exactly one evidence table"
        )
    start = header_indexes[0]
    if start + 1 >= len(lines) or re.fullmatch(
        r"\|\s*-{3,}\s*\|\s*-{3,}\s*\|", lines[start + 1].strip()
    ) is None:
        raise ReleaseVerificationError("Artifact identity table separator is malformed")

    table = lines[start : start + 2]
    for line in lines[start + 2 :]:
        if not line.strip().startswith("|"):
            break
        table.append(line)
    return table


def _table_rows(markdown: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in _artifact_identity_table(markdown)[2:]:
        match = re.fullmatch(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if match is None:
            raise ReleaseVerificationError("Artifact identity table row is malformed")
        label, value = match.groups()
        if label not in ARTIFACT_LABELS:
            raise ReleaseVerificationError(
                f"unexpected release-evidence row: {label}"
            )
        if label in rows:
            raise ReleaseVerificationError(f"duplicate release-evidence row: {label}")
        rows[label] = value
    missing = sorted(ARTIFACT_LABELS - rows.keys())
    if missing:
        raise ReleaseVerificationError(f"missing release-evidence rows: {missing}")
    return rows


def _sha256_value(value: str, label: str) -> str:
    match = re.fullmatch(r"`([0-9a-f]{64})`", value)
    if match is None:
        raise ReleaseVerificationError(f"{label} must be one lowercase SHA-256")
    return match.group(1)


def _integer(value: str, pattern: str, label: str) -> int:
    match = re.fullmatch(pattern, value)
    if match is None:
        raise ReleaseVerificationError(f"cannot parse {label}: {value!r}")
    return int(match.group(1).replace(",", ""))


def parse_release_evidence(markdown: str) -> ReleaseEvidence:
    rows = _table_rows(markdown)
    navigation = re.fullmatch(
        r"(\d+) nested content entries plus (\d+) cover entr(?:y|ies)",
        rows["EPUB navigation"],
    )
    if navigation is None:
        raise ReleaseVerificationError(
            f"cannot parse EPUB navigation: {rows['EPUB navigation']!r}"
        )
    credit = re.fullmatch(r"`([^`]+)`", rows["Publication credit"])
    if credit is None:
        raise ReleaseVerificationError(
            "publication credit must be one code-delimited value"
        )
    return ReleaseEvidence(
        edition_contract_sha256=_sha256_value(
            rows["Edition contract SHA-256"],
            "edition contract SHA-256",
        ),
        source_sha256=_sha256_value(
            rows["Immutable source SHA-256"], "immutable source SHA-256"
        ),
        pdf_sha256=_sha256_value(rows["PDF SHA-256"], "PDF SHA-256"),
        epub_sha256=_sha256_value(rows["EPUB SHA-256"], "EPUB SHA-256"),
        pdf_pages=_integer(rows["PDF extent"], r"(\d+) A5 pages", "PDF extent"),
        pdf_size=_integer(
            rows["PDF file size"], r"([\d,]+) bytes", "PDF file size"
        ),
        epub_content_entries=int(navigation.group(1)),
        epub_cover_entries=int(navigation.group(2)),
        epub_size=_integer(
            rows["EPUB archive size"], r"([\d,]+) bytes", "EPUB archive size"
        ),
        publication_credit=credit.group(1),
    )


def validate_evidence_contract(
    evidence: ReleaseEvidence,
    edition: EditionContract,
) -> None:
    require(
        evidence.source_sha256 == edition.source_sha256,
        "release evidence redefines the immutable source SHA-256",
    )
    require(
        evidence.publication_credit == edition.author,
        "release evidence redefines the canonical publication credit",
    )
