#!/usr/bin/env python3
"""Score one authoritative beginner-pilot v2 cohort manifest."""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from beginner_pilot import epub_smoke_passed, score
from beginner_pilot_contract import TASK_CRITERIA
from beginner_pilot_manifest import Cohort, load_cohort
from beginner_pilot_validation import InvalidRecord, parse_timestamp


def _device_class(value: str) -> str:
    lowered = value.lower()
    if "iphone" in lowered or "ipad" in lowered or "ios" in lowered:
        return "iOS/iPadOS device"
    if "android" in lowered or "pixel" in lowered or "galaxy" in lowered:
        return "Android device"
    if "kindle" in lowered:
        return "Kindle device"
    if "kobo" in lowered:
        return "Kobo device"
    if "mac" in lowered:
        return "macOS computer"
    if "windows" in lowered:
        return "Windows computer"
    if "linux" in lowered:
        return "Linux computer"
    return "Other device class"


def _reader_class(value: str) -> str:
    lowered = value.lower()
    for needle, label in (
        ("apple books", "Apple Books"),
        ("books", "Books-family reader"),
        ("kindle", "Kindle reader"),
        ("kobo", "Kobo reader"),
        ("adobe", "Adobe-family reader"),
    ):
        if needle in lowered:
            return label
    return "Other reader class"


def _environment_counts(records: list[dict[str, Any]]) -> Counter[tuple[str, str]]:
    return Counter(
        (
            _device_class(record["session"]["device"]),
            _reader_class(record["session"]["reader_app"]),
        )
        for record in records
    )


def _epub_environment_counts(
    records: list[dict[str, Any]],
) -> Counter[tuple[str, str, str, int, bool, bool]]:
    rows: Counter[tuple[str, str, str, int, bool, bool]] = Counter()
    for record in records:
        smoke = record["epub_smoke"]
        if not isinstance(smoke, dict):
            continue
        rows[
            (
                " ".join(smoke["reader_app"].split()),
                " ".join(smoke["reader_app_version"].split()),
                _device_class(smoke["device"]),
                smoke["text_scale_percent"],
                smoke["dark_mode"],
                epub_smoke_passed(record),
            )
        ] += 1
    return rows


def _failure_misses(records: list[dict[str, Any]]) -> list[tuple[str, int]]:
    misses: list[tuple[str, int]] = []
    for task_id, criteria in TASK_CRITERIA.items():
        nonanswers = sum(
            record["tasks"][task_id]["outcome"] != "answered" for record in records
        )
        if nonanswers:
            misses.append((f"{task_id}.not_answered", nonanswers))
        hinted = sum(
            record["tasks"][task_id]["hint_used"] is True for record in records
        )
        if hinted:
            misses.append((f"{task_id}.hint_used", hinted))
        for criterion in criteria:
            count = sum(
                record["tasks"][task_id]["criteria"][criterion] is False
                for record in records
            )
            if count:
                misses.append((f"{task_id}.{criterion}", count))
    slow = sum(
        record["tasks"]["start_route"]["elapsed_seconds"] > 90 for record in records
    )
    if slow:
        misses.append(("start_route.over_90_seconds", slow))
    return misses


def _month_range(records: list[dict[str, Any]]) -> str:
    dates = [
        parse_timestamp(record["session"]["started_at"], "session date")
        for record in records
    ]
    first = min(dates).strftime("%Y-%m")
    last = max(dates).strftime("%Y-%m")
    return first if first == last else f"{first} to {last}"


def _inline_code(value: str) -> str:
    return "`" + " ".join(value.split()).replace("`", "'") + "`"


def _completed_date(manifest: dict[str, Any]) -> str:
    return parse_timestamp(manifest["closed_at"], "manifest closed_at").date().isoformat()


def _external_header_lines(
    *,
    passed: bool,
    evidence_role: str,
    cohort: Cohort,
    manifest_sha256: str,
    limits: str,
) -> list[str]:
    return [
        f"Gate status: {'PASSED' if passed else 'FAILED'}",
        f"Evidence role: {evidence_role}",
        f"Candidate commit: {cohort.evidence.git_commit}",
        f"PDF SHA-256: {cohort.evidence.pdf_sha256}",
        f"EPUB SHA-256: {cohort.evidence.epub_sha256}",
        f"Completed: {_completed_date(cohort.manifest)}",
        "Signer or verifiable public confirmation: "
        "Deterministic scorer output bound to the frozen manifest and artifacts.",
        f"What this evidence does not establish: {limits}",
        f"Cohort ID: {cohort.manifest['cohort_id']}",
        f"Manifest SHA-256: {manifest_sha256}",
    ]


def _counted_entry(
    cohort: Cohort, record: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    attempt_number = record["attempt_number"]
    entry = next(
        (
            item
            for item in cohort.manifest["attempts"]
            if item["attempt_number"] == attempt_number
        ),
        None,
    )
    if entry is None:
        raise ValueError(f"counted manifest entry missing for attempt {attempt_number}")
    return entry, record


def _reader_app_report(
    cohort: Cohort,
    manifest_sha256: str,
) -> str:
    counted_pairs = [_counted_entry(cohort, record) for record in cohort.counted_records]
    passing_pairs = [
        (entry, record)
        for entry, record in counted_pairs
        if epub_smoke_passed(record)
    ]
    recorded_pairs = [
        (entry, record)
        for entry, record in counted_pairs
        if isinstance(record["epub_smoke"], dict)
    ]
    entry, record = (
        passing_pairs[0]
        if passing_pairs
        else recorded_pairs[0]
        if recorded_pairs
        else counted_pairs[0]
    )
    smoke = record["epub_smoke"]
    passed = any(epub_smoke_passed(item) for item in cohort.counted_records)
    lines = _external_header_lines(
        passed=passed,
        evidence_role="reader_app_report",
        cohort=cohort,
        manifest_sha256=manifest_sha256,
        limits=(
            "It does not prove reader identity, response accuracy beyond this one "
            "committed record, or behavior in other reader apps or devices."
        ),
    )
    lines.extend(
        [
            f"Counted record SHA-256: {entry['record_sha256']}",
            "",
            "# Public EPUB reader-app report",
            "",
        ]
    )
    if isinstance(smoke, dict):
        repeated_tasks = smoke["repeated_tasks"]
        lines.extend(
            [
                f"- Reader app class: `{_reader_class(smoke['reader_app'])}`",
                f"- Reader app version: `{' '.join(smoke['reader_app_version'].split())}`",
                f"- Device class: `{_device_class(smoke['device'])}`",
                f"- Text scale percent: `{smoke['text_scale_percent']}%`",
                f"- Dark mode: `{'on' if smoke['dark_mode'] else 'off'}`",
                f"- Repeated start-route status: `{'PASSED' if repeated_tasks['start_route']['passed'] else 'FAILED'}`",
                f"- Repeated section-finding status: `{'PASSED' if repeated_tasks['section_finding']['passed'] else 'FAILED'}`",
                f"- Display criteria status: `{'PASSED' if all(smoke['criteria'].values()) else 'FAILED'}`",
            ]
        )
    else:
        lines.extend(
            [
                "- Reader app class: `not recorded`",
                "- Reader app version: `not recorded`",
                "- Device class: `not recorded`",
                "- Text scale percent: `not recorded`",
                "- Dark mode: `not recorded`",
                "- Repeated start-route status: `NOT RECORDED`",
                "- Repeated section-finding status: `NOT RECORDED`",
                "- Display criteria status: `NOT RECORDED`",
            ]
        )
    lines.extend(
        [
            "",
            "## Limits",
            "",
            "This report intentionally omits reader IDs, exact device models, navigation excerpts, "
            "response content, and free-text notes. It is one committed smoke-check witness, not a "
            "population claim or a substitute for independent reader-app validation.",
        ]
    )
    return "\n".join(lines) + "\n"


def render(
    cohort: Cohort,
    rows: list[tuple[str, int, int, bool]],
    passed: bool,
    manifest_sha256: str,
) -> str:
    manifest = cohort.manifest
    records = cohort.counted_records
    editor_moderators = sum(
        record["session"]["moderator_is_editor"] is True for record in records
    )
    lines = _external_header_lines(
        passed=passed,
        evidence_role="aggregate_report",
        cohort=cohort,
        manifest_sha256=manifest_sha256,
        limits=(
            "It does not prove moderator identity, omitted-attempt completeness, or "
            "population-wide novice validation beyond this frozen cohort."
        ),
    )
    lines.extend(
        f"Counted record SHA-256: {_counted_entry(cohort, record)[0]['record_sha256']}"
        for record in records
    )
    lines.extend(
        [
            "",
            "# Beginner validation cohort result",
            "",
            f"- Verdict: **{'PASS' if passed else 'FAIL'}**",
            f"- Primary format: `{manifest['primary_format']}`",
            "- Repository lineage: canonical `streamentry/streamentry` origin; "
            "artifact commit is an ancestor of local `origin/main`",
            f"- PDF pages: `{cohort.evidence.pdf_pages}`",
            f"- Session month range: `{_month_range(cohort.records)}`",
            f"- Started attempts: `{len(cohort.records)}`; counted cohort: `5`",
            f"- Distress stops: `{cohort.distress_stops}`",
            f"- Editor-moderated counted sessions: `{editor_moderators}/5`",
            "",
            "## Gate results",
            "",
            "| Gate | Observed | Required | Result |",
            "|---|---:|---:|---|",
        ]
    )
    lines.extend(
        f"| {name} | {count} | {required} | {'Pass' if ok else 'Fail'} |"
        for name, count, required, ok in rows
    )
    lines.extend(["", "## Coarsened primary-format environments", ""])
    groups = _environment_counts(records)
    shown = [(key, count) for key, count in sorted(groups.items()) if count >= 2]
    suppressed = sum(count for count in groups.values() if count < 2)
    lines.extend(
        f"- `{count}/5` on `{device}` with `{reader}`"
        for (device, reader), count in shown
    )
    if suppressed:
        lines.append(
            f"- `{suppressed}/5` in environment cells suppressed because n < 2"
        )
    lines.extend(["", "## De-identified fixed failure themes", ""])
    misses = _failure_misses(records)
    if misses:
        lines.extend(
            [
                "| Fixed criterion | Counted readers missing it |",
                "|---|---:|",
                *(f"| `{name}` | {count}/5 |" for name, count in misses),
            ]
        )
    else:
        lines.append("No fixed task criterion was missed in first answers.")
    smoke_count = sum(epub_smoke_passed(record) for record in records)
    lines.extend(
        [
            "",
            "## EPUB evidence",
            "",
            f"- Passing EPUB repeated-task and display records: `{smoke_count}/5`",
            "- Frozen section-finding prompt: "
            + _inline_code(manifest["epub_section_finding_prompt"]),
        ]
    )
    for (
        app,
        version,
        device,
        scale,
        dark_mode,
        environment_passed,
    ), count in sorted(_epub_environment_counts(records).items()):
        lines.append(
            f"- `{count}` record(s): app {_inline_code(app)}, "
            f"version {_inline_code(version)}, device class {_inline_code(device)}, "
            f"text scale `{scale}%`, dark mode `{'on' if dark_mode else 'off'}`, "
            f"result `{'Pass' if environment_passed else 'Fail'}`"
        )
    lines.extend(
        [
            "",
            "The EPUB environment summary intentionally omits reader codes, exact device "
            "models, personalized device names, first answers, and free-text notes. A human "
            "privacy review remains required before publication.",
            "",
            "## Limits",
            "",
            "The verdict applies only to the frozen contract, exact committed artifacts, "
            "manifest-listed attempts, and first five completed eligible records. "
            "It does not authenticate the moderator, prove that local origin/main was "
            "freshly fetched, independently timestamp the asserted registered_at value, "
            "detect every kind of personal data, or prove that a terminal attempt was never omitted. "
            "Those guarantees require an external append-only registry.",
            "",
            "It does not establish clinical safety, spiritual attainment, sustained benefit, "
            "comparative superiority, population validity, or market leadership.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--epub-evidence-output", type=Path)
    args = parser.parse_args()
    try:
        if (
            args.output is not None
            and args.epub_evidence_output is not None
            and args.output.resolve() == args.epub_evidence_output.resolve()
        ):
            raise ValueError(
                "aggregate and EPUB evidence outputs must use different paths"
            )
        manifest_sha256 = hashlib.sha256(args.manifest.read_bytes()).hexdigest()
        cohort = load_cohort(args.manifest)
        rows, passed = score(cohort.counted_records, cohort.distress_stops)
        report = render(cohort, rows, passed, manifest_sha256)
        epub_report = (
            _reader_app_report(cohort, manifest_sha256)
            if args.epub_evidence_output
            else None
        )
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
        else:
            print(report, end="")
        if args.epub_evidence_output and epub_report is not None:
            args.epub_evidence_output.parent.mkdir(parents=True, exist_ok=True)
            args.epub_evidence_output.write_text(epub_report, encoding="utf-8")
    except (InvalidRecord, OSError, ValueError) as error:
        print(f"Invalid beginner-pilot data: {error}", file=sys.stderr)
        return 2
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
