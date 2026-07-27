"""Validate the release identity declared by the rights materials inventory."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from release_common import require


RIGHTS_INVENTORY_PATH = Path("book/references/rights-materials-inventory.md")


@dataclass(frozen=True, slots=True)
class RightsInventoryIdentity:
    schema: int
    source_sha256: str
    pdf_sha256: str
    epub_sha256: str


def _field(markdown: str, name: str) -> str:
    matches = re.findall(
        rf"^{re.escape(name)}:\s*(\S(?:.*\S)?)\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        len(matches) == 1,
        f"rights inventory must contain exactly one {name} line",
    )
    return matches[0]


def _sha256_field(markdown: str, name: str) -> str:
    value = _field(markdown, name)
    match = re.fullmatch(r"(?:([0-9a-f]{64})|`([0-9a-f]{64})`)", value)
    require(
        match is not None,
        f"rights inventory {name} must be one lowercase SHA-256",
    )
    return match.group(1) or match.group(2)


def parse_rights_inventory(markdown: str) -> RightsInventoryIdentity:
    """Parse the exact artifact identity used for a rights decision."""

    schema = _field(markdown, "Rights materials inventory schema")
    require(schema == "1", "rights materials inventory schema must be 1")
    return RightsInventoryIdentity(
        schema=1,
        source_sha256=_sha256_field(
            markdown,
            "Immutable manuscript SHA-256",
        ),
        pdf_sha256=_sha256_field(markdown, "Candidate PDF SHA-256"),
        epub_sha256=_sha256_field(markdown, "Candidate EPUB SHA-256"),
    )


def validate_rights_inventory(
    markdown: str,
    *,
    source_sha256: str,
    pdf_sha256: str,
    epub_sha256: str,
) -> RightsInventoryIdentity:
    """Reject an inventory that describes different publication bytes."""

    identity = parse_rights_inventory(markdown)
    require(
        identity.source_sha256 == source_sha256,
        "rights inventory immutable manuscript SHA-256 is stale",
    )
    require(
        identity.pdf_sha256 == pdf_sha256,
        "rights inventory candidate PDF SHA-256 is stale",
    )
    require(
        identity.epub_sha256 == epub_sha256,
        "rights inventory candidate EPUB SHA-256 is stale",
    )
    return identity
