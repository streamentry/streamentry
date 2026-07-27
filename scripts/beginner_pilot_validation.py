"""Strict JSON, schema, and semantic validation for beginner pilot v2."""

from __future__ import annotations

import json
import math
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as error:  # pragma: no cover - environment failure
    raise RuntimeError("beginner pilot v2 requires the 'jsonschema' package") from error

from beginner_pilot_contract import (
    EPUB_CRITERIA,
    RECORD_SCHEMA_PATH,
    STOP_CATEGORIES,
    STOP_REASON_CODES,
    TASK_CRITERIA,
    TASK_OUTCOMES,
)


EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:\+?\d[\d .()-]{7,}\d)(?![A-Za-z0-9])"
)


class InvalidRecord(ValueError):
    """Raised when pilot data cannot support a decision."""


def _reject_constant(value: str) -> None:
    raise InvalidRecord(f"JSON contains non-standard constant {value}")


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InvalidRecord(f"JSON contains duplicate key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_constant,
            object_pairs_hook=_reject_duplicate_pairs,
        )
    except InvalidRecord:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InvalidRecord(f"{path}: cannot read strict JSON: {error}") from error
    if not isinstance(data, dict):
        raise InvalidRecord(f"{path}: JSON root must be an object")
    return data


def validate_json_schema(
    value: dict[str, Any], schema_path: Path, label: str
) -> None:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        errors = sorted(validator.iter_errors(value), key=lambda item: list(item.path))
    except (OSError, json.JSONDecodeError, jsonschema.SchemaError) as error:
        raise InvalidRecord(f"{label}: cannot load valid schema: {error}") from error
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise InvalidRecord(f"{label}.{location}: {error.message}")


def parse_timestamp(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise InvalidRecord(f"{label}: invalid ISO 8601 timestamp") from error
    if parsed.tzinfo is None:
        raise InvalidRecord(f"{label}: timestamp requires a UTC offset")
    return parsed


def is_eligible(record: dict[str, Any]) -> bool:
    item = record["eligibility"]
    return (
        item["vietnamese_comfort"] in {"native", "fluent"}
        and item["age_18_or_over"] is True
        and 0 <= item["meditation_sessions_lifetime"] <= 5
        and item["retreats_completed"] == 0
        and item["knows_mahasi_vocabulary"] is False
        and item["read_book_before"] is False
        and item["participated_in_prior_book_pilot"] is False
        and item["seen_tested_passages_before"] is False
        and item["rubric_seen_before_first_answers"] is False
        and item["experienced_buddhist"] is False
        and item["is_editor"] is False
        and item["is_source_reviewer"] is False
    )


def _nonempty(value: str) -> bool:
    return bool(value.strip())


def _reject_possible_personal_data(value: str, label: str) -> None:
    if EMAIL_PATTERN.search(value) or PHONE_PATTERN.search(value):
        raise InvalidRecord(f"{label}: possible personal contact data detected")


def _validate_task(task: dict[str, Any], task_id: str, label: str) -> None:
    for field in ("first_answer", "source_locator", "notes"):
        _reject_possible_personal_data(
            task[field], f"{label}.{task_id}.{field}"
        )
    outcome = task["outcome"]
    if outcome not in TASK_OUTCOMES:
        raise InvalidRecord(f"{label}.{task_id}: invalid task outcome")
    elapsed = task["elapsed_seconds"]
    if not math.isfinite(elapsed):
        raise InvalidRecord(f"{label}.{task_id}: elapsed time must be finite")
    if set(task["criteria"]) != set(TASK_CRITERIA[task_id]):
        raise InvalidRecord(f"{label}.{task_id}: criterion fields do not match")
    if outcome == "answered":
        if not (
            task["completed"] is True
            and task["first_answer_recorded"] is True
            and _nonempty(task["first_answer"])
            and _nonempty(task["source_locator"])
        ):
            raise InvalidRecord(f"{label}.{task_id}: answered task lacks evidence")
        return
    expected_blank = (
        task["completed"] is False
        and task["first_answer_recorded"] is False
        and task["first_answer"] == ""
        and task["source_locator"] == ""
        and task["hint_used"] is False
        and not any(task["criteria"].values())
    )
    if not expected_blank:
        raise InvalidRecord(
            f"{label}.{task_id}: {outcome} task must not contain answer evidence"
        )
    if outcome == "not_reached" and elapsed != 0:
        raise InvalidRecord(f"{label}.{task_id}: not_reached elapsed time must be zero")


def _validate_repeat(item: dict[str, Any], name: str, label: str) -> None:
    for field in ("first_answer", "source_locator", "notes"):
        _reject_possible_personal_data(item[field], f"{label}.{name}.{field}")
    if item["outcome"] != "answered":
        return
    if not (
        item["first_answer_recorded"] is True
        and _nonempty(item["first_answer"])
        and _nonempty(item["source_locator"])
        and math.isfinite(item["elapsed_seconds"])
    ):
        raise InvalidRecord(f"{label}.{name}: repeated task lacks answer evidence")


def _validate_epub_smoke(smoke: dict[str, Any] | None, label: str) -> None:
    if smoke is None:
        return
    for field in ("device", "reader_app", "reader_app_version", "notes"):
        _reject_possible_personal_data(
            smoke[field], f"{label}.epub_smoke.{field}"
        )
    if set(smoke["criteria"]) != EPUB_CRITERIA:
        raise InvalidRecord(f"{label}.epub_smoke: criterion fields do not match")
    for name, item in smoke["repeated_tasks"].items():
        _validate_repeat(item, name, f"{label}.epub_smoke.repeated_tasks")


def validate_record(
    record: dict[str, Any],
    label: str,
    repo_root: Path,
    closed_at: datetime,
    now: datetime,
) -> None:
    validate_json_schema(record, repo_root / RECORD_SCHEMA_PATH, label)
    session = record["session"]
    started = parse_timestamp(session["started_at"], f"{label}.session.started_at")
    completed = parse_timestamp(
        session["completed_at"], f"{label}.session.completed_at"
    )
    delete_by = parse_timestamp(record["delete_by"], f"{label}.delete_by")
    if completed < started:
        raise InvalidRecord(f"{label}: completion precedes start")
    expected_delete_by = min(started + timedelta(days=90), closed_at + timedelta(days=30))
    if delete_by != expected_delete_by:
        raise InvalidRecord(
            f"{label}.delete_by must equal the protocol retention deadline "
            f"{expected_delete_by.isoformat()}"
        )
    if delete_by <= now:
        raise InvalidRecord(f"{label}.delete_by is overdue; raw data must be deleted")
    stopped = session["stopped_early"]
    category = session["stop_category"]
    if stopped != (category != "none") or category not in STOP_CATEGORIES:
        raise InvalidRecord(f"{label}: stopped flag and stop category disagree")
    if stopped and not _nonempty(session["stop_reason"]):
        raise InvalidRecord(f"{label}: stopped attempt requires a bounded reason")
    if not stopped and session["stop_reason"] != "":
        raise InvalidRecord(f"{label}: completed attempt cannot have a stop reason")
    if session["stop_reason"] != STOP_REASON_CODES[category]:
        raise InvalidRecord(
            f"{label}: stop_reason must use the fixed code for {category}"
        )
    for field in ("device", "reader_app", "reader_app_version"):
        _reject_possible_personal_data(
            session[field], f"{label}.session.{field}"
        )
    for task_id, task in record["tasks"].items():
        _validate_task(task, task_id, label)
    outcomes = [record["tasks"][task_id]["outcome"] for task_id in TASK_CRITERIA]
    if category == "distress":
        if any(outcome != "not_reached" for outcome in outcomes):
            raise InvalidRecord(f"{label}: distress record must erase task answers")
        if any(task["notes"] != "" for task in record["tasks"].values()):
            raise InvalidRecord(f"{label}: distress record must erase task notes")
    elif stopped:
        try:
            first_not_reached = outcomes.index("not_reached")
        except ValueError as error:
            raise InvalidRecord(
                f"{label}: stopped attempt requires a not_reached task"
            ) from error
        if any(
            outcome != "not_reached" for outcome in outcomes[first_not_reached:]
        ):
            raise InvalidRecord(
                f"{label}: task outcomes cannot resume after not_reached"
            )
    if category == "ineligible_after_start" and is_eligible(record):
        raise InvalidRecord(
            f"{label}: ineligible_after_start requires a failed eligibility rule"
        )
    if stopped and record["epub_smoke"] is not None:
        raise InvalidRecord(f"{label}: stopped attempt cannot contain EPUB smoke data")
    _validate_epub_smoke(record["epub_smoke"], label)


def load_records(paths: list[Path]) -> list[dict[str, Any]]:
    return [load_json(path) for path in paths]


def default_now() -> datetime:
    return datetime.now().astimezone()
