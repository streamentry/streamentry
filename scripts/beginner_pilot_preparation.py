"""Freeze one clean candidate and its beginner-pilot registration header."""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from beginner_pilot_artifact import committed_hash, sha256_file, verify_artifacts
from beginner_pilot_contract import (
    CANONICAL_ORIGIN_URLS,
    CANONICAL_REMOTE_REF,
    CONTRACT_PATHS,
    MAX_STARTED_ATTEMPTS,
    SELECTION_RULE,
    TARGET_COMPLETED,
)
from beginner_pilot_validation import default_now, parse_timestamp
from edition_contract import load_edition_contract


COHORT_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,63}$")
EPUB_SECTION_FINDING_PROMPT = (
    "Trong EPUB, hãy dùng mục lục hoặc liên kết để tìm mục "
    "“Ba kiết sử đầu: ba mối trói phải rơi” ở Chương 10, "
    "rồi chỉ ra nhãn nguồn của đoạn kinh đầu tiên ngay dưới mục ấy."
)
REGISTRATION_FILENAME = "registration.json"
MANIFEST_FILENAME = "manifest.json"


class WorkflowError(ValueError):
    """Raised when an operator action could weaken the pilot evidence."""


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _run_git(repo_root: Path, arguments: list[str], label: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise WorkflowError(f"{label}: Git command failed") from error
    return result.stdout.strip()


def verify_clean_canonical_candidate(repo_root: Path) -> str:
    root = repo_root.resolve(strict=True)
    if _run_git(root, ["status", "--porcelain", "--untracked-files=all"], "candidate"):
        raise WorkflowError("candidate worktree must be clean before pilot preparation")
    origin = _run_git(root, ["remote", "get-url", "origin"], "origin")
    if origin not in CANONICAL_ORIGIN_URLS:
        raise WorkflowError("repository origin is not canonical streamentry")
    head = _run_git(root, ["rev-parse", "--verify", "HEAD^{commit}"], "candidate")
    remote = _run_git(
        root,
        ["rev-parse", "--verify", f"{CANONICAL_REMOTE_REF}^{{commit}}"],
        "origin/main",
    )
    result = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", head, remote],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise WorkflowError("candidate commit is not in local canonical origin/main")
    return head


def _pdf_pages(path: Path, repo_root: Path) -> int:
    try:
        result = subprocess.run(
            ["pdfinfo", str(path)],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise WorkflowError("cannot read the candidate PDF page count") from error
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise WorkflowError("candidate PDF page count is missing")


def artifact_payload(repo_root: Path, commit: str) -> dict[str, Any]:
    edition = load_edition_contract(repo_root / "book" / "edition.json")
    pdf_path = (repo_root / edition.pdf_relative_path).resolve(strict=True)
    epub_path = (repo_root / edition.epub_relative_path).resolve(strict=True)
    metadata = {
        "git_commit": commit,
        "pdf_sha256": sha256_file(pdf_path),
        "epub_sha256": sha256_file(epub_path),
        "pdf_pages": _pdf_pages(pdf_path, repo_root),
    }
    verify_artifacts(metadata, repo_root, pdf_path, epub_path)
    return {
        **metadata,
        "pdf_path": str(pdf_path),
        "epub_path": str(epub_path),
    }


def contract_payload(repo_root: Path, commit: str) -> dict[str, Any]:
    hashes: dict[str, str] = {}
    for relative in CONTRACT_PATHS:
        current = sha256_file(repo_root / relative)
        if committed_hash(repo_root, commit, relative) != current:
            raise WorkflowError(f"uncommitted pilot contract drift: {relative}")
        hashes[relative] = current
    return {"git_commit": commit, "files": hashes}


def json_bytes(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode("utf-8")


def write_exclusive(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(json_bytes(payload))


def replace_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.{secrets.token_hex(4)}.tmp")
    try:
        write_exclusive(temporary, payload)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def cohort_dir(repo_root: Path, cohort_id: str) -> Path:
    if COHORT_ID_PATTERN.fullmatch(cohort_id) is None:
        raise WorkflowError(
            "cohort_id must be 3-64 characters using letters, digits, dot, dash or underscore"
        )
    return repo_root.resolve(strict=True) / "build" / "beginner-pilot" / cohort_id


def initialize_cohort(
    repo_root: Path,
    *,
    cohort_id: str,
    primary_format: str,
    registered_at: str,
    external_registry_reference: str | None,
) -> Path:
    if primary_format not in {"pdf", "epub"}:
        raise WorkflowError("primary_format must be pdf or epub")
    if parse_timestamp(registered_at, "registered_at") > default_now():
        raise WorkflowError("registered_at cannot be in the future")
    commit = verify_clean_canonical_candidate(repo_root)
    destination = cohort_dir(repo_root, cohort_id)
    if destination.exists():
        raise WorkflowError(f"cohort directory already exists: {destination}")
    records_dir = destination / "records"
    registration = {
        "workflow_schema_version": 1,
        "evidence_status": "registration_only_not_participant_evidence",
        "preregistration_status": (
            "external_reference_provided_but_not_authenticated"
            if external_registry_reference
            else "local_timestamp_only_not_independent_preregistration"
        ),
        "external_registry_reference": external_registry_reference,
        "schema_version": 2,
        "cohort_id": cohort_id,
        "registered_at": registered_at,
        "repo_root": str(repo_root.resolve(strict=True)),
        "records_dir": str(records_dir),
        "primary_format": primary_format,
        "target_completed": TARGET_COMPLETED,
        "max_started_attempts": MAX_STARTED_ATTEMPTS,
        "selection_rule": SELECTION_RULE,
        "epub_section_finding_prompt": EPUB_SECTION_FINDING_PROMPT,
        "artifact": artifact_payload(repo_root, commit),
        "contract": contract_payload(repo_root, commit),
    }
    records_dir.mkdir(parents=True)
    path = destination / REGISTRATION_FILENAME
    write_exclusive(path, registration)
    return path


def registration_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
