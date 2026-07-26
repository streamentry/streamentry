"""Verify the machine-readable external release-gate registry."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from external_release_gate_files import (
    evidence_artifact_sha256,
    evidence_role,
    evidence_status,
    exact_keys,
    load_registry,
    safe_file,
    sha256_file,
    validate_hashed_file,
)
from release_common import ReleaseVerificationError, require
from release_evidence import ReleaseEvidence


REGISTRY_PATH = "book/references/external-release-gates.json"
RELEASE_EVIDENCE_PATH = "book/references/release-evidence.md"
EVIDENCE_PREFIX = Path("book/references/external-evidence")
BASE_CLAIM = "internally_verified_dual_format_candidate"
ALLOWED_STATUSES = {"open", "in_progress", "failed", "passed"}

EXPECTED_PROTOCOLS = {
    "external_release_packet": "book/references/external-release-packet.md",
    "rights_decision": "book/references/rights-decision-template.md",
    "doctrinal_review": "book/references/doctrinal-review-protocol.md",
    "clinical_safety_review": (
        "book/references/clinical-safety-review-protocol.md"
    ),
    "beginner_validation": "book/references/beginner-validation-protocol.md",
    "beginner_reader_kit": "book/references/beginner-reader-kit.md",
    "comparative_beginner": (
        "book/references/comparative-beginner-protocol.md"
    ),
    "public_evidence_policy": "book/references/external-evidence/README.md",
}

EXPECTED_GATES = {
    "redistribution_rights": ("rights_decision",),
    "doctrinal_review": ("doctrinal_review",),
    "clinical_safety_review": ("clinical_safety_review",),
    "beginner_cohort": ("beginner_validation", "beginner_reader_kit"),
    "epub_reader_app": ("beginner_reader_kit",),
    "comparative_evidence": ("comparative_beginner",),
}

STATUS_LABELS = {
    "redistribution_rights": "Public redistribution rights",
    "doctrinal_review": "Independent Theravāda review",
    "clinical_safety_review": "Independent clinical-safety review",
    "beginner_cohort": "Five-reader beginner cohort",
    "epub_reader_app": "Human EPUB reader-app smoke test",
    "comparative_evidence": "Comparative evidence",
}

CLAIM_BY_GATE = {
    "redistribution_rights": "public_redistribution_authorized",
    "doctrinal_review": "independently_doctrinally_reviewed",
    "clinical_safety_review": "independently_clinical_safety_reviewed",
    "epub_reader_app": "human_epub_reader_app_gate_passed",
}

GATE_EVIDENCE_RULES = {
    "redistribution_rights": {
        "allowed_roles": {"rights_decision"},
        "required_singletons": {"rights_decision"},
        "required_at_least_one": set(),
    },
    "doctrinal_review": {
        "allowed_roles": {"doctrinal_review_report"},
        "required_singletons": {"doctrinal_review_report"},
        "required_at_least_one": set(),
    },
    "clinical_safety_review": {
        "allowed_roles": {"clinical_safety_review_report"},
        "required_singletons": set(),
        "required_at_least_one": {"clinical_safety_review_report"},
    },
    "beginner_cohort": {
        "allowed_roles": {
            "aggregate_report",
            "preregistration_receipt",
            "public_history_confirmation",
            "privacy_review_confirmation",
        },
        "required_singletons": {
            "aggregate_report",
            "preregistration_receipt",
            "public_history_confirmation",
            "privacy_review_confirmation",
        },
        "required_at_least_one": set(),
    },
    "epub_reader_app": {
        "allowed_roles": {"reader_app_report"},
        "required_singletons": {"reader_app_report"},
        "required_at_least_one": set(),
    },
    "comparative_evidence": {
        "allowed_roles": {"preregistration_receipt", "comparative_results"},
        "required_singletons": {
            "preregistration_receipt",
            "comparative_results",
        },
        "required_at_least_one": set(),
    },
}


def _current_git_candidate(root: Path) -> str:
    try:
        commit_result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        status_result = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ReleaseVerificationError(
            "external evidence requires a readable Git candidate"
        ) from error
    commit = commit_result.stdout.strip()
    require(
        re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
        "current Git candidate is not one full lowercase commit",
    )
    require(
        not status_result.stdout.strip(),
        "external evidence candidate binding requires a clean worktree",
    )
    return commit


def _validate_evidence(
    root: Path,
    item: dict[str, Any],
    gate_id: str,
    status: str,
    release: ReleaseEvidence,
    candidate_commit: str,
    label: str,
) -> tuple[str, str]:
    require(isinstance(item, dict), f"{label} must be one object")
    exact_keys(item, {"path", "sha256", "role"}, label)
    relative = item["path"]
    require(isinstance(relative, str), f"{label} path must be text")
    role = item["role"]
    require(isinstance(role, str), f"{label} role must be text")
    rules = GATE_EVIDENCE_RULES[gate_id]
    require(
        role in rules["allowed_roles"],
        f"{label} role is unsupported for gate {gate_id}",
    )
    path_parts = Path(relative).parts
    require(
        path_parts[: len(EVIDENCE_PREFIX.parts)] == EVIDENCE_PREFIX.parts
        and Path(relative) != EVIDENCE_PREFIX / "README.md",
        f"{label} must live under {EVIDENCE_PREFIX.as_posix()}",
    )
    path = safe_file(root, relative, label)
    require(
        isinstance(item["sha256"], str)
        and re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is not None,
        f"{label} SHA-256 is malformed",
    )
    require(
        sha256_file(path) == item["sha256"],
        f"{label} SHA-256 is stale",
    )
    markdown = path.read_text(encoding="utf-8")
    require(
        evidence_status(markdown) == status,
        f"{label} Gate status contradicts the registry",
    )
    require(
        evidence_role(markdown) == role,
        f"{label} Evidence role contradicts the registry",
    )
    commit_matches = re.findall(
        r"^Candidate commit:\s*`?([0-9a-f]{40})`?\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        commit_matches == [candidate_commit],
        f"{label} must bind exactly once to the current clean Git candidate",
    )
    require(
        evidence_artifact_sha256(markdown, "PDF") == release.pdf_sha256,
        f"{label} does not bind the current PDF SHA-256",
    )
    require(
        evidence_artifact_sha256(markdown, "EPUB") == release.epub_sha256,
        f"{label} does not bind the current EPUB SHA-256",
    )
    return relative, role


def _validate_gate_roles(gate_id: str, role_counts: dict[str, int]) -> None:
    rules = GATE_EVIDENCE_RULES[gate_id]
    singleton_roles = rules["required_singletons"]
    repeated = sorted(
        role for role in singleton_roles if role_counts.get(role, 0) > 1
    )
    require(
        not repeated,
        f"gate {gate_id} has duplicate singleton roles: {repeated}",
    )
    missing_singletons = sorted(
        role for role in singleton_roles if role_counts.get(role, 0) != 1
    )
    missing_at_least_one = sorted(
        role
        for role in rules["required_at_least_one"]
        if role_counts.get(role, 0) < 1
    )
    missing = missing_singletons + missing_at_least_one
    require(
        not missing,
        f"gate {gate_id} is missing required evidence roles: {missing}",
    )


def _validate_status_summary(markdown: str, gates: dict[str, Any]) -> None:
    status_heading = re.search(r"^## Status\s*$", markdown, flags=re.MULTILINE)
    require(status_heading is not None, "release evidence lacks a Status section")
    next_heading = re.search(
        r"^## [^\n]+$",
        markdown[status_heading.end() :],
        flags=re.MULTILINE,
    )
    end = (
        status_heading.end() + next_heading.start()
        if next_heading is not None
        else len(markdown)
    )
    section = markdown[status_heading.end() : end]
    for gate_id, label in STATUS_LABELS.items():
        matches = re.findall(
            rf"^- {re.escape(label)}:\s*\*\*(OPEN|IN PROGRESS|FAILED|PASSED)\*\*",
            section,
            flags=re.MULTILINE,
        )
        require(
            len(matches) == 1,
            f"release evidence must summarize {label} exactly once",
        )
        expected = gates[gate_id]["status"].replace("_", " ").upper()
        require(
            matches[0] == expected,
            f"release evidence status for {label} contradicts the registry",
        )


def _derived_claims(gates: dict[str, Any]) -> list[str]:
    claims = {BASE_CLAIM}
    for gate_id, claim in CLAIM_BY_GATE.items():
        if gates[gate_id]["status"] == "passed":
            claims.add(claim)
    if (
        gates["beginner_cohort"]["status"] == "passed"
        and gates["epub_reader_app"]["status"] == "passed"
    ):
        claims.add("defined_beginner_gate_passed")
        if gates["comparative_evidence"]["status"] == "passed":
            claims.add("named_panel_first_use_outperformance")
    return sorted(claims)


def verify_external_release_gates(
    root: Path,
    release: ReleaseEvidence,
) -> dict[str, Any]:
    registry = load_registry(root / REGISTRY_PATH)
    exact_keys(
        registry,
        {
            "schema_version",
            "candidate_binding",
            "release_evidence",
            "protocols",
            "gates",
            "permitted_claims",
        },
        "external release registry",
    )
    require(registry["schema_version"] == 2, "unsupported gate registry version")
    require(
        registry["candidate_binding"]
        == "enclosing_clean_git_commit_plus_release_evidence",
        "external gate registry candidate binding is not canonical",
    )

    release_path = validate_hashed_file(
        root,
        registry["release_evidence"],
        RELEASE_EVIDENCE_PATH,
        "release evidence record",
    )

    protocols = registry["protocols"]
    require(isinstance(protocols, dict), "protocols must be one object")
    exact_keys(protocols, set(EXPECTED_PROTOCOLS), "protocol registry")
    for protocol_id, expected_path in EXPECTED_PROTOCOLS.items():
        validate_hashed_file(
            root,
            protocols[protocol_id],
            expected_path,
            f"protocol {protocol_id}",
        )

    gates = registry["gates"]
    require(isinstance(gates, dict), "gates must be one object")
    exact_keys(gates, set(EXPECTED_GATES), "gate registry")
    candidate_commit: str | None = None
    used_evidence: set[str] = set()
    for gate_id, expected_protocols in EXPECTED_GATES.items():
        gate = gates[gate_id]
        require(isinstance(gate, dict), f"gate {gate_id} must be one object")
        exact_keys(gate, {"status", "protocols", "evidence"}, f"gate {gate_id}")
        require(
            gate["status"] in ALLOWED_STATUSES,
            f"gate {gate_id} has unsupported status",
        )
        require(
            gate["protocols"] == list(expected_protocols),
            f"gate {gate_id} protocol set is incomplete or reordered",
        )
        require(
            isinstance(gate["evidence"], list),
            f"gate {gate_id} evidence must be one list",
        )
        if gate["status"] in {"open", "in_progress"}:
            require(
                not gate["evidence"],
                f"gate {gate_id} cannot claim evidence before a terminal result",
            )
        else:
            require(
                bool(gate["evidence"]),
                f"gate {gate_id} needs public evidence for a terminal result",
            )
            if candidate_commit is None:
                candidate_commit = _current_git_candidate(root)
            role_counts: dict[str, int] = {}
            for index, item in enumerate(gate["evidence"]):
                relative, role = _validate_evidence(
                    root,
                    item,
                    gate_id,
                    gate["status"],
                    release,
                    candidate_commit,
                    f"gate {gate_id} evidence {index + 1}",
                )
                require(
                    relative not in used_evidence,
                    "one evidence path may appear only once in the registry",
                )
                used_evidence.add(relative)
                role_counts[role] = role_counts.get(role, 0) + 1
            _validate_gate_roles(gate_id, role_counts)

    require(
        gates["beginner_cohort"]["status"] != "passed"
        or gates["epub_reader_app"]["status"] == "passed",
        "the beginner cohort cannot pass without its counted EPUB reader-app gate",
    )
    require(
        registry["permitted_claims"] == _derived_claims(gates),
        "permitted claims do not follow from the recorded gate statuses",
    )
    _validate_status_summary(release_path.read_text(encoding="utf-8"), gates)
    return registry
