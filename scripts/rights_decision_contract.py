"""Validate the machine-readable summary in public rights evidence."""

from __future__ import annotations

import re
from pathlib import Path

from external_release_gate_files import sha256_file
from release_common import require
from rights_inventory_contract import RIGHTS_INVENTORY_PATH


PLACEHOLDERS = {
    "",
    "-",
    "n/a",
    "none recorded",
    "tbd",
    "to be determined",
    "unknown",
}
CAPACITIES = {
    "author",
    "rights_holder",
    "assignee",
    "publisher",
    "authorized_officer",
}
DISTRIBUTION_SCOPES = {
    "FREE_ONLY",
    "FREE_AND_PAID",
    "NOT_AUTHORIZED",
}
SOURCE_SCOPES = {
    "PUBLIC_REUSE_AUTHORIZED",
    "PUBLIC_READ_ONLY",
    "NOT_AUTHORIZED",
}
DERIVATIVE_SCOPES = {
    "AUTHORIZED",
    "AUTHORIZED_WITH_CONDITIONS",
    "NOT_AUTHORIZED",
}
RESOLUTION_STATUSES = {"RESOLVED", "UNRESOLVED"}
OVERALL_DECISIONS = {
    "APPROVE",
    "DECLINE",
    "AUTHORITY_NOT_ESTABLISHED",
}


def _field(markdown: str, name: str) -> str:
    matches = re.findall(
        rf"^{re.escape(name)}:\s*(\S(?:.*\S)?)\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        len(matches) == 1,
        f"rights decision must contain exactly one {name} line",
    )
    value = matches[0]
    require(len(value) <= 500, f"rights decision {name} is too long")
    return value


def _substantive_field(markdown: str, name: str) -> str:
    value = _field(markdown, name)
    require(
        value.casefold() not in PLACEHOLDERS and len(value) >= 3,
        f"rights decision {name} is unresolved or a placeholder",
    )
    return value


def _sha256_field(markdown: str, name: str) -> str:
    value = _field(markdown, name)
    match = re.fullmatch(
        r"(?:([0-9a-f]{64})|`([0-9a-f]{64})`)",
        value,
    )
    require(
        match is not None,
        f"rights decision {name} must be one lowercase SHA-256",
    )
    return match.group(1) or match.group(2)


def validate_rights_decision(
    root: Path,
    markdown: str,
    gate_status: str,
    source_sha256: str,
) -> None:
    """Reject incomplete, stale, or internally contradictory rights evidence."""

    require(
        _field(markdown, "Rights decision schema") == "1",
        "rights decision schema must be 1",
    )
    decision_id = _field(markdown, "Decision record ID")
    require(
        re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,63}", decision_id) is not None,
        "rights decision record ID is malformed",
    )
    _substantive_field(markdown, "Decision maker public identity")
    require(
        _field(markdown, "Decision maker capacity") in CAPACITIES,
        "rights decision maker capacity is unsupported",
    )
    _substantive_field(markdown, "Basis of authority")
    _substantive_field(markdown, "Public evidence of authority")
    _substantive_field(markdown, "Applicable jurisdiction")

    inventory_path = root / RIGHTS_INVENTORY_PATH
    require(
        inventory_path.is_file(),
        "rights decision materials inventory is missing",
    )
    require(
        _sha256_field(markdown, "Rights materials inventory SHA-256")
        == sha256_file(inventory_path),
        "rights decision materials inventory SHA-256 is stale",
    )
    require(
        _sha256_field(markdown, "Immutable manuscript SHA-256")
        == source_sha256,
        "rights decision immutable manuscript SHA-256 is stale",
    )

    source_scope = _field(markdown, "Repository source scope")
    pdf_scope = _field(markdown, "PDF distribution scope")
    epub_scope = _field(markdown, "EPUB distribution scope")
    print_scope = _field(markdown, "Print distribution scope")
    derivative_scope = _field(markdown, "Derivative editions scope")
    require(
        source_scope in SOURCE_SCOPES,
        "rights decision repository source scope is unsupported",
    )
    for name, value in (
        ("PDF distribution scope", pdf_scope),
        ("EPUB distribution scope", epub_scope),
        ("Print distribution scope", print_scope),
    ):
        require(
            value in DISTRIBUTION_SCOPES,
            f"rights decision {name} is unsupported",
        )
    require(
        derivative_scope in DERIVATIVE_SCOPES,
        "rights decision derivative editions scope is unsupported",
    )

    _substantive_field(markdown, "Territory")
    require(
        _field(markdown, "Languages") == "vi",
        "rights decision languages must bind the current vi edition",
    )
    _substantive_field(markdown, "Term")
    _substantive_field(markdown, "Attribution")
    _substantive_field(markdown, "Required third-party notices")
    contributor_status = _field(markdown, "Contributor chain status")
    third_party_status = _field(markdown, "Third-party materials status")
    require(
        contributor_status in RESOLUTION_STATUSES,
        "rights decision contributor chain status is unsupported",
    )
    require(
        third_party_status in RESOLUTION_STATUSES,
        "rights decision third-party materials status is unsupported",
    )
    unresolved_items = _field(markdown, "Unresolved rights items")
    overall_decision = _field(markdown, "Overall rights decision")
    require(
        overall_decision in OVERALL_DECISIONS,
        "rights decision overall result is unsupported",
    )
    _substantive_field(markdown, "Exact permitted public wording")

    if gate_status == "passed":
        require(
            overall_decision == "APPROVE",
            "passed rights evidence must record an APPROVE decision",
        )
        require(
            pdf_scope != "NOT_AUTHORIZED"
            and epub_scope != "NOT_AUTHORIZED",
            "passed rights evidence must authorize both PDF and EPUB distribution",
        )
        require(
            contributor_status == "RESOLVED",
            "passed rights evidence must resolve the contributor chain",
        )
        require(
            third_party_status == "RESOLVED",
            "passed rights evidence must resolve third-party materials",
        )
        require(
            unresolved_items == "NONE",
            "passed rights evidence cannot retain unresolved rights items",
        )
    else:
        require(
            overall_decision in {"DECLINE", "AUTHORITY_NOT_ESTABLISHED"},
            "failed rights evidence must decline or leave authority unestablished",
        )
