from __future__ import annotations

import hashlib
from pathlib import Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rights_decision_lines(
    root: Path,
    source_sha256: str,
    *,
    status: str,
    overrides: dict[str, str] | None = None,
) -> list[str]:
    fields = {
        "Rights decision schema": "1",
        "Decision record ID": "rights-vi-2026-001",
        "Decision maker public identity": "Public rights holder",
        "Decision maker capacity": "rights_holder",
        "Basis of authority": (
            "Original authorship plus recorded contributor assignments"
        ),
        "Public evidence of authority": (
            "Signed public confirmation bound to this decision record"
        ),
        "Applicable jurisdiction": "Vietnam",
        "Rights materials inventory SHA-256": _sha256(
            root / "book/references/rights-materials-inventory.md"
        ),
        "Immutable manuscript SHA-256": source_sha256,
        "Repository source scope": "PUBLIC_READ_ONLY",
        "PDF distribution scope": "FREE_ONLY",
        "EPUB distribution scope": "FREE_ONLY",
        "Print distribution scope": "NOT_AUTHORIZED",
        "Derivative editions scope": "NOT_AUTHORIZED",
        "Territory": "Worldwide",
        "Languages": "vi",
        "Term": "Perpetual for the frozen candidate",
        "Attribution": "CS Chánh Niệm + ChatGPT",
        "Required third-party notices": (
            "Retain named source and embedded-font notices"
        ),
        "Contributor chain status": (
            "RESOLVED" if status == "passed" else "UNRESOLVED"
        ),
        "Third-party materials status": (
            "RESOLVED" if status == "passed" else "UNRESOLVED"
        ),
        "Unresolved rights items": (
            "NONE" if status == "passed" else "Authority evidence incomplete"
        ),
        "Overall rights decision": (
            "APPROVE" if status == "passed" else "AUTHORITY_NOT_ESTABLISHED"
        ),
        "Exact permitted public wording": (
            "The frozen Vietnamese PDF and EPUB may be redistributed free "
            "of charge worldwide with attribution."
        ),
    }
    fields.update(overrides or {})
    return [f"{name}: {value}" for name, value in fields.items()]
