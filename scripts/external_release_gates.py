"""Verify the machine-readable external release-gate registry."""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any

from external_release_gate_files import (
    evidence_artifact_sha256,
    evidence_cohort_binding,
    evidence_completed,
    evidence_counted_record_sha256s,
    evidence_generated_report_passed,
    evidence_limit,
    evidence_public_confirmation,
    evidence_role,
    evidence_status,
    exact_keys,
    load_registry,
    reject_public_contact_data,
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
COHORT_BOUND_ROLES = {"aggregate_report", "reader_app_report"}
FROZEN_ARTIFACT_PATHS = {
    "PDF": "dist/huong-den-nhap-luu.pdf",
    "EPUB": "dist/huong-den-nhap-luu.epub",
}

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


def _current_clean_git_head(root: Path) -> str:
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
            "external evidence requires a readable Git checkout"
        ) from error
    commit = commit_result.stdout.strip()
    require(
        re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
        "current Git candidate is not one full lowercase commit",
    )
    require(
        not status_result.stdout.strip(),
        "external evidence verification requires a clean worktree",
    )
    return commit


def _is_git_ancestor(root: Path, candidate_commit: str, head_commit: str) -> bool:
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "merge-base",
                "--is-ancestor",
                candidate_commit,
                head_commit,
            ],
            check=False,
            capture_output=True,
        )
    except OSError as error:
        raise ReleaseVerificationError(
            "cannot inspect the frozen artifact commit ancestry"
        ) from error
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    raise ReleaseVerificationError(
        "cannot inspect the frozen artifact commit ancestry"
    )


def _git_blob_sha256(root: Path, commit: str, relative: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "show", f"{commit}:{relative}"],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ReleaseVerificationError(
            f"frozen artifact commit does not expose {relative}"
        ) from error
    return hashlib.sha256(result.stdout).hexdigest()


def _validate_frozen_candidate(
    root: Path,
    candidate_commit: str,
    head_commit: str,
    release: ReleaseEvidence,
) -> None:
    require(
        re.fullmatch(r"[0-9a-f]{40}", candidate_commit) is not None,
        "external evidence Candidate commit is malformed",
    )
    require(
        _is_git_ancestor(root, candidate_commit, head_commit),
        "external evidence Candidate commit is not an ancestor of the evidence commit",
    )
    expected = {
        "PDF": release.pdf_sha256,
        "EPUB": release.epub_sha256,
    }
    for artifact, relative in FROZEN_ARTIFACT_PATHS.items():
        require(
            _git_blob_sha256(root, candidate_commit, relative)
            == expected[artifact],
            f"frozen Candidate commit does not contain the recorded {artifact}",
        )


def _validate_evidence(
    root: Path,
    item: dict[str, Any],
    gate_id: str,
    status: str,
    release: ReleaseEvidence,
    label: str,
) -> tuple[
    str,
    str,
    str,
    tuple[str, str] | None,
    frozenset[str] | None,
]:
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
    reject_public_contact_data(markdown)
    require(
        evidence_status(markdown) == status,
        f"{label} Gate status contradicts the registry",
    )
    require(
        evidence_role(markdown) == role,
        f"{label} Evidence role contradicts the registry",
    )
    evidence_completed(markdown)
    evidence_public_confirmation(markdown)
    evidence_limit(markdown)
    generated_report_passed = evidence_generated_report_passed(markdown, role)
    if generated_report_passed is not None:
        require(
            generated_report_passed == (status == "passed"),
            f"{label} machine-visible report verdict contradicts the registry",
        )
    commit_matches = re.findall(
        r"^Candidate commit:\s*`?([0-9a-f]{40})`?\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        len(commit_matches) == 1,
        f"{label} must bind exactly once to one frozen Candidate commit",
    )
    require(
        evidence_artifact_sha256(markdown, "PDF") == release.pdf_sha256,
        f"{label} does not bind the current PDF SHA-256",
    )
    require(
        evidence_artifact_sha256(markdown, "EPUB") == release.epub_sha256,
        f"{label} does not bind the current EPUB SHA-256",
    )
    cohort_binding = (
        evidence_cohort_binding(markdown)
        if role in COHORT_BOUND_ROLES
        else None
    )
    counted_records = None
    if role == "aggregate_report":
        counted_records = evidence_counted_record_sha256s(markdown, 5)
    elif role == "reader_app_report":
        counted_records = evidence_counted_record_sha256s(markdown, 1)
    return (
        relative,
        role,
        commit_matches[0],
        cohort_binding,
        counted_records,
    )


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
    require(registry["schema_version"] == 3, "unsupported gate registry version")
    require(
        registry["candidate_binding"]
        == "frozen_artifact_commit_ancestor_plus_release_evidence",
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
    head_commit: str | None = None
    frozen_candidate: str | None = None
    validated_candidates: set[str] = set()
    cohort_bindings: dict[str, list[tuple[str, str]]] = {}
    counted_record_bindings: dict[str, list[frozenset[str]]] = {}
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
            role_counts: dict[str, int] = {}
            for index, item in enumerate(gate["evidence"]):
                (
                    relative,
                    role,
                    candidate_commit,
                    cohort_binding,
                    counted_records,
                ) = _validate_evidence(
                    root,
                    item,
                    gate_id,
                    gate["status"],
                    release,
                    f"gate {gate_id} evidence {index + 1}",
                )
                if head_commit is None:
                    head_commit = _current_clean_git_head(root)
                if candidate_commit not in validated_candidates:
                    _validate_frozen_candidate(
                        root,
                        candidate_commit,
                        head_commit,
                        release,
                    )
                    validated_candidates.add(candidate_commit)
                if frozen_candidate is None:
                    frozen_candidate = candidate_commit
                require(
                    candidate_commit == frozen_candidate,
                    "all external evidence must bind the same frozen Candidate commit",
                )
                if cohort_binding is not None:
                    cohort_bindings.setdefault(role, []).append(cohort_binding)
                if counted_records is not None:
                    counted_record_bindings.setdefault(role, []).append(
                        counted_records
                    )
                require(
                    relative not in used_evidence,
                    "one evidence path may appear only once in the registry",
                )
                used_evidence.add(relative)
                role_counts[role] = role_counts.get(role, 0) + 1
            _validate_gate_roles(gate_id, role_counts)

    terminal_statuses = {"failed", "passed"}
    require(
        gates["epub_reader_app"]["status"] not in terminal_statuses
        or gates["beginner_cohort"]["status"] in terminal_statuses,
        "the EPUB reader-app gate requires one terminal counted beginner cohort",
    )
    if gates["epub_reader_app"]["status"] in terminal_statuses:
        aggregate_bindings = cohort_bindings.get("aggregate_report", [])
        reader_bindings = cohort_bindings.get("reader_app_report", [])
        require(
            len(aggregate_bindings) == 1 and len(reader_bindings) == 1,
            "the counted beginner and EPUB reports need one cohort binding each",
        )
        require(
            aggregate_bindings[0] == reader_bindings[0],
            "the EPUB report does not bind the counted beginner manifest",
        )
        aggregate_records = counted_record_bindings.get("aggregate_report", [])
        reader_records = counted_record_bindings.get("reader_app_report", [])
        require(
            len(aggregate_records) == 1 and len(reader_records) == 1,
            "the counted beginner and EPUB reports need record commitments",
        )
        require(
            reader_records[0] <= aggregate_records[0],
            "the EPUB report is not committed as one of the five counted records",
        )
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
