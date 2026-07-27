"""Create intentionally invalid drafts, then finalize only valid pilot evidence."""

from __future__ import annotations

import hashlib
import secrets
import stat
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from beginner_pilot_contract import (
    ARTIFACT_FIELDS,
    EPUB_CRITERIA,
    MAX_STARTED_ATTEMPTS,
    TARGET_COMPLETED,
    TASK_CRITERIA,
)
from beginner_pilot_manifest import load_cohort
from beginner_pilot_preparation import (
    MANIFEST_FILENAME,
    REGISTRATION_FILENAME,
    WorkflowError,
    artifact_payload,
    cohort_dir,
    contract_payload,
    json_bytes,
    replace_json,
    verify_clean_canonical_candidate,
    write_exclusive,
)
from beginner_pilot_validation import (
    default_now,
    is_eligible,
    load_json,
    parse_timestamp,
    validate_record,
)


def _blank_task(task_id: str) -> dict[str, Any]:
    return {
        "outcome": None,
        "completed": None,
        "first_answer_recorded": None,
        "first_answer": None,
        "source_locator": None,
        "elapsed_seconds": None,
        "hint_used": None,
        "criteria": {name: None for name in TASK_CRITERIA[task_id]},
        "notes": None,
    }


def create_attempt_draft(
    repo_root: Path,
    *,
    cohort_id: str,
    started_at: str,
    consent_confirmed: bool,
    include_epub_smoke: bool,
) -> Path:
    if not consent_confirmed:
        raise WorkflowError(
            "create a started-attempt record only after explicit consent"
        )
    started = parse_timestamp(started_at, "started_at")
    if started > default_now():
        raise WorkflowError("started_at cannot be in the future")
    destination = cohort_dir(repo_root, cohort_id)
    registration = load_json(destination / REGISTRATION_FILENAME)
    registered = parse_timestamp(registration["registered_at"], "registered_at")
    if registered >= started:
        raise WorkflowError("attempt must start after cohort registration")
    if (destination / MANIFEST_FILENAME).exists():
        raise WorkflowError("cohort is already finalized")
    existing = sorted((destination / "records").glob("*.json"))
    eligible_completions = 0
    for path in existing:
        prior = load_json(path)
        try:
            completed = parse_timestamp(
                prior["session"]["completed_at"], f"{path.name}.completed_at"
            )
            if (
                completed <= started
                and prior["session"]["stopped_early"] is False
                and is_eligible(prior)
            ):
                eligible_completions += 1
        except (AttributeError, KeyError, TypeError, ValueError):
            continue
    if eligible_completions >= TARGET_COMPLETED:
        raise WorkflowError(
            "do not start another attempt after five eligible completions"
        )
    attempt_number = len(existing) + 1
    if attempt_number > MAX_STARTED_ATTEMPTS:
        raise WorkflowError("cohort already has seven started attempts")
    token = secrets.token_hex(4)
    attempt_id = f"attempt-{attempt_number:02d}-{token}"
    reader_id = f"reader-{secrets.token_hex(6)}"
    draft = {
        "_draft_only": (
            "NOT EVIDENCE. Fill every null from the real session; finalize strips "
            "this marker only after strict validation."
        ),
        "schema_version": 2,
        "cohort_id": cohort_id,
        "attempt_id": attempt_id,
        "attempt_number": attempt_number,
        "delete_by": None,
        "reader_id": reader_id,
        "consent_confirmed": True,
        "eligibility": {
            "vietnamese_comfort": None,
            "age_18_or_over": None,
            "meditation_sessions_lifetime": None,
            "retreats_completed": None,
            "knows_mahasi_vocabulary": None,
            "read_book_before": None,
            "participated_in_prior_book_pilot": None,
            "seen_tested_passages_before": None,
            "experienced_buddhist": None,
            "is_editor": None,
            "is_source_reviewer": None,
        },
        "artifact": {
            field: registration["artifact"][field] for field in ARTIFACT_FIELDS
        },
        "session": {
            "primary_format": registration["primary_format"],
            "moderator_is_editor": None,
            "prompts_displayed_in_writing": None,
            "prompt_rereading_allowed": None,
            "moderator_followup_cues_used": None,
            "started_at": started_at,
            "completed_at": None,
            "stopped_early": None,
            "stop_category": None,
            "stop_reason": None,
            "device": None,
            "reader_app": None,
            "reader_app_version": None,
            "text_scale_percent": None,
            "dark_mode": None,
        },
        "tasks": {task_id: _blank_task(task_id) for task_id in TASK_CRITERIA},
        "epub_smoke": empty_epub_smoke_template() if include_epub_smoke else None,
    }
    path = destination / "records" / f"{attempt_number:02d}-{attempt_id}.json"
    write_exclusive(path, draft)
    return path


def _retention_deadline(started_at: str, closed_at: str) -> str:
    started = parse_timestamp(started_at, "session.started_at")
    closed = parse_timestamp(closed_at, "closed_at")
    deadline = min(started + timedelta(days=90), closed + timedelta(days=30))
    return deadline.isoformat()


def _require_private_file(path: Path) -> None:
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        raise WorkflowError(
            f"{path.name}: raw pilot files must not be readable by group or others"
        )


def finalize_cohort(
    repo_root: Path,
    *,
    cohort_id: str,
    closed_at: str,
    now: datetime | None = None,
) -> Path:
    clock = now or default_now()
    closed = parse_timestamp(closed_at, "closed_at")
    if closed > clock:
        raise WorkflowError("closed_at cannot be in the future")
    destination = cohort_dir(repo_root, cohort_id)
    manifest_path = destination / MANIFEST_FILENAME
    if manifest_path.exists():
        raise WorkflowError("cohort manifest already exists; finalization is one-way")
    registration_path = destination / REGISTRATION_FILENAME
    _require_private_file(registration_path)
    registration = load_json(registration_path)
    commit = verify_clean_canonical_candidate(repo_root)
    if commit != registration["artifact"]["git_commit"]:
        raise WorkflowError("candidate commit changed after cohort registration")
    if artifact_payload(repo_root, commit) != registration["artifact"]:
        raise WorkflowError("candidate artifacts changed after cohort registration")
    if contract_payload(repo_root, commit) != registration["contract"]:
        raise WorkflowError("pilot contract changed after cohort registration")

    records_dir = destination / "records"
    if any(path.is_dir() for path in records_dir.iterdir()):
        raise WorkflowError("records directory must not contain subdirectories")
    record_paths = sorted(records_dir.glob("*.json"))
    if not TARGET_COMPLETED <= len(record_paths) <= MAX_STARTED_ATTEMPTS:
        raise WorkflowError("finalization requires five to seven started attempts")

    normalized: list[tuple[Path, dict[str, Any]]] = []
    attempts: list[dict[str, Any]] = []
    for expected_number, path in enumerate(record_paths, start=1):
        _require_private_file(path)
        record = load_json(path)
        record.pop("_draft_only", None)
        if (
            record.get("cohort_id") != cohort_id
            or record.get("attempt_number") != expected_number
        ):
            raise WorkflowError(f"{path.name}: cohort identity or order is wrong")
        record["delete_by"] = _retention_deadline(
            record["session"]["started_at"], closed_at
        )
        validate_record(record, str(path), repo_root, closed, clock)
        serialized = json_bytes(record)
        normalized.append((path, record))
        attempts.append(
            {
                "attempt_number": expected_number,
                "attempt_id": record["attempt_id"],
                "record_path": path.name,
                "record_sha256": hashlib.sha256(serialized).hexdigest(),
            }
        )

    manifest = {
        key: registration[key]
        for key in (
            "schema_version",
            "cohort_id",
            "registered_at",
            "repo_root",
            "records_dir",
            "primary_format",
            "target_completed",
            "max_started_attempts",
            "selection_rule",
            "epub_section_finding_prompt",
            "artifact",
            "contract",
        )
    }
    manifest["closed_at"] = closed_at
    manifest["attempts"] = attempts
    for path, record in normalized:
        replace_json(path, record)
    write_exclusive(manifest_path, manifest)
    try:
        load_cohort(manifest_path, now=clock)
    except Exception:
        manifest_path.unlink()
        raise
    return manifest_path


def empty_epub_smoke_template() -> dict[str, Any]:
    """Return the exact EPUB smoke shape for operators who need one."""
    repeated = {
        "outcome": None,
        "first_answer_recorded": None,
        "first_answer": None,
        "source_locator": None,
        "elapsed_seconds": None,
        "hint_used": None,
        "passed": None,
        "notes": None,
    }
    return {
        "device": None,
        "reader_app": None,
        "reader_app_version": None,
        "text_scale_percent": None,
        "dark_mode": None,
        "repeated_tasks": {
            "start_route": dict(repeated),
            "section_finding": dict(repeated),
        },
        "criteria": {name: None for name in sorted(EPUB_CRITERIA)},
        "notes": None,
    }
