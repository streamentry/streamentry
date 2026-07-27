"""Score the frozen first-five beginner cohort selected by a v2 manifest."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from beginner_pilot_contract import TASK_CRITERIA, TASK_THRESHOLDS


def _task_unassisted(task: dict[str, Any]) -> bool:
    return (
        task["outcome"] == "answered"
        and task["completed"] is True
        and task["first_answer_recorded"] is True
        and task["hint_used"] is False
    )


def _task_passed(task: dict[str, Any], task_id: str) -> bool:
    criteria_pass = all(
        task["criteria"][name] is True for name in TASK_CRITERIA[task_id]
    )
    within_time = task_id != "start_route" or task["elapsed_seconds"] <= 90
    return _task_unassisted(task) and criteria_pass and within_time


def _criterion_count(
    records: Iterable[dict[str, Any]], task_id: str, criterion: str
) -> int:
    return sum(
        _task_unassisted(record["tasks"][task_id])
        and record["tasks"][task_id]["criteria"][criterion] is True
        for record in records
    )


def _repeat_passed(item: dict[str, Any], *, timed: bool) -> bool:
    return (
        item["outcome"] == "answered"
        and item["first_answer_recorded"] is True
        and bool(item["first_answer"].strip())
        and bool(item["source_locator"].strip())
        and item["hint_used"] is False
        and item["passed"] is True
        and (not timed or item["elapsed_seconds"] <= 90)
    )


def epub_smoke_passed(record: dict[str, Any]) -> bool:
    smoke = record["epub_smoke"]
    if not isinstance(smoke, dict):
        return False
    repeated = smoke["repeated_tasks"]
    return (
        smoke["text_scale_percent"] >= 150
        and smoke["dark_mode"] is True
        and all(smoke["criteria"].values())
        and _repeat_passed(repeated["start_route"], timed=True)
        and _repeat_passed(repeated["section_finding"], timed=False)
    )


def prompt_delivery_passed(record: dict[str, Any]) -> bool:
    session = record["session"]
    return (
        session["prompts_displayed_in_writing"] is True
        and session["prompt_rereading_allowed"] is True
        and session["moderator_followup_cues_used"] is False
    )


def score(
    records: list[dict[str, Any]], distress_stops: int = 0
) -> tuple[list[tuple[str, int, int, bool]], bool]:
    rows: list[tuple[str, int, int, bool]] = []
    for task_id, threshold in TASK_THRESHOLDS.items():
        count = sum(
            _task_passed(record["tasks"][task_id], task_id) for record in records
        )
        rows.append((task_id, count, threshold, count >= threshold))
    insight_reject = _criterion_count(
        records, "insight_map", "rejects_stage_diagnosis"
    )
    rows.append(
        ("insight_map_rejects_self_diagnosis", insight_reject, 5, insight_reject == 5)
    )
    complete_evidence = sum(
        all(task["outcome"] == "answered" for task in record["tasks"].values())
        for record in records
    )
    rows.append(
        (
            "all_tasks_answered",
            complete_evidence,
            5,
            complete_evidence == 5,
        )
    )
    prompt_delivery_count = sum(prompt_delivery_passed(record) for record in records)
    rows.append(
        (
            "written_prompt_delivery_without_followup_cues",
            prompt_delivery_count,
            5,
            prompt_delivery_count == 5,
        )
    )
    supplied_smoke = [
        record for record in records if isinstance(record["epub_smoke"], dict)
    ]
    epub_count = sum(epub_smoke_passed(record) for record in supplied_smoke)
    epub_required = len(supplied_smoke) or 1
    rows.append(
        (
            "epub_smoke",
            epub_count,
            epub_required,
            bool(supplied_smoke) and epub_count == len(supplied_smoke),
        )
    )
    rows.append(("distress_stop_veto", distress_stops, 0, distress_stops == 0))
    return rows, all(row[3] for row in rows)
