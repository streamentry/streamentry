"""Load and verify the authoritative beginner-pilot v2 cohort manifest."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import subprocess
from typing import Any

from beginner_pilot_artifact import (
    ArtifactEvidence,
    ArtifactVerificationError,
    committed_hash,
    sha256_file,
    verify_artifacts,
)
from beginner_pilot_contract import (
    ARTIFACT_FIELDS,
    CANONICAL_ORIGIN_URLS,
    CANONICAL_REMOTE_REF,
    CONTRACT_PATHS,
    MANIFEST_SCHEMA_PATH,
    MAX_STARTED_ATTEMPTS,
    SELECTION_RULE,
    TARGET_COMPLETED,
)
from beginner_pilot_validation import (
    InvalidRecord,
    default_now,
    is_eligible,
    load_json,
    parse_timestamp,
    validate_json_schema,
    validate_record,
)


@dataclass(frozen=True)
class Cohort:
    manifest: dict[str, Any]
    records: list[dict[str, Any]]
    counted_records: list[dict[str, Any]]
    evidence: ArtifactEvidence
    distress_stops: int
    stopped_counts: dict[str, int]


def _resolve_inside(path_text: str, base: Path, root: Path, label: str) -> Path:
    candidate = Path(path_text)
    if not candidate.is_absolute():
        candidate = base / candidate
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as error:
        raise InvalidRecord(f"{label}: path must exist inside repo_root") from error
    return resolved


def _verify_canonical_repo(root: Path, artifact_commit: str) -> None:
    try:
        origin_result = subprocess.run(
            ["git", "-C", str(root), "remote", "get-url", "origin"],
            check=True,
            capture_output=True,
            text=True,
        )
        remote_result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "rev-parse",
                "--verify",
                f"{CANONICAL_REMOTE_REF}^{{commit}}",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        ancestry_result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "merge-base",
                "--is-ancestor",
                artifact_commit,
                remote_result.stdout.strip(),
            ],
            check=False,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise InvalidRecord(
            "cannot verify the canonical origin/main lineage; fetch origin first"
        ) from error
    if origin_result.stdout.strip() not in CANONICAL_ORIGIN_URLS:
        raise InvalidRecord("repository origin is not canonical streamentry")
    if ancestry_result.returncode == 1:
        raise InvalidRecord("artifact commit is not in canonical origin/main history")
    if ancestry_result.returncode != 0:
        raise InvalidRecord("cannot verify artifact commit ancestry")


def _verify_contract(manifest: dict[str, Any], root: Path) -> None:
    contract = manifest["contract"]
    artifact_commit = manifest["artifact"]["git_commit"]
    if contract["git_commit"] != artifact_commit:
        raise InvalidRecord("manifest contract and artifact commits must match")
    if set(contract["files"]) != set(CONTRACT_PATHS):
        raise InvalidRecord("manifest contract file set is incomplete or unexpected")
    executing_root = Path(__file__).resolve().parents[1]
    for relative in CONTRACT_PATHS:
        expected = contract["files"][relative]
        frozen_path = root / relative
        running_path = executing_root / relative
        if not frozen_path.is_file() or sha256_file(frozen_path) != expected:
            raise InvalidRecord(f"contract hash mismatch: {relative}")
        if not running_path.is_file() or sha256_file(running_path) != expected:
            raise InvalidRecord(f"running scorer contract mismatch: {relative}")
        try:
            frozen_hash = committed_hash(root, contract["git_commit"], relative)
        except ArtifactVerificationError as error:
            raise InvalidRecord(str(error)) from error
        if frozen_hash != expected:
            raise InvalidRecord(f"committed contract hash mismatch: {relative}")


def _discover_attempt_paths(
    manifest: dict[str, Any], manifest_path: Path, root: Path
) -> tuple[Path, list[Path]]:
    records_dir = _resolve_inside(
        manifest["records_dir"], manifest_path.parent, root, "records_dir"
    )
    expected_cohort_dir = (
        root / "build" / "beginner-pilot" / manifest["cohort_id"]
    )
    expected_records_dir = expected_cohort_dir / "records"
    expected_manifest_path = expected_cohort_dir / "manifest.json"
    if records_dir != expected_records_dir.resolve(strict=True):
        raise InvalidRecord(
            "records_dir must be build/beginner-pilot/<cohort-id>/records"
        )
    if manifest_path.resolve(strict=True) != expected_manifest_path.resolve(strict=True):
        raise InvalidRecord(
            "manifest must be build/beginner-pilot/<cohort-id>/manifest.json"
        )
    listed: list[Path] = []
    for entry in manifest["attempts"]:
        path = _resolve_inside(
            entry["record_path"], records_dir, root, "manifest attempt record"
        )
        try:
            path.relative_to(records_dir)
        except ValueError as error:
            raise InvalidRecord("manifest record must be inside records_dir") from error
        if path.parent != records_dir or path.suffix.lower() != ".json":
            raise InvalidRecord("manifest records must be direct JSON children")
        listed.append(path)
    descendants = list(records_dir.rglob("*"))
    directories = [path for path in descendants if path.is_dir()]
    if directories:
        raise InvalidRecord("records_dir must not contain subdirectories")
    discovered = {path.resolve() for path in descendants if path.is_file()}
    if discovered != set(listed):
        missing = set(listed) - discovered
        extra = discovered - set(listed)
        detail = f"missing={len(missing)}, additions={len(extra)}"
        raise InvalidRecord(f"manifest record discovery mismatch: {detail}")
    _verify_private_paths(root, [manifest_path, *listed])
    return records_dir, listed


def _verify_private_paths(root: Path, paths: list[Path]) -> None:
    relative_paths = [str(path.resolve(strict=True).relative_to(root)) for path in paths]
    for relative in relative_paths:
        try:
            ignored = subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "check-ignore",
                    "--no-index",
                    "--quiet",
                    "--",
                    relative,
                ],
                check=False,
                capture_output=True,
            )
        except OSError as error:
            raise InvalidRecord("cannot verify private pilot paths with Git") from error
        if ignored.returncode == 1:
            raise InvalidRecord(
                f"private pilot path is not covered by Git ignore rules: {relative}"
            )
        if ignored.returncode != 0:
            raise InvalidRecord("cannot verify private pilot paths with Git")
    try:
        tracked = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-files",
                "--cached",
                "-z",
                "--",
                *relative_paths,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise InvalidRecord("cannot verify whether pilot data is Git-tracked") from error
    tracked_paths = [item for item in tracked.stdout.split("\0") if item]
    if tracked_paths:
        raise InvalidRecord(
            "raw pilot manifest and attempt records must not be Git-tracked"
        )
    try:
        history = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "log",
                "--all",
                "--name-only",
                "--format=",
                "--",
                "build/beginner-pilot",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise InvalidRecord("cannot inspect Git history for raw pilot data") from error
    if any(line.strip() for line in history.stdout.splitlines()):
        raise InvalidRecord(
            "raw beginner-pilot data appeared in Git history; discard this cohort"
        )


def _load_attempts(
    manifest: dict[str, Any],
    paths: list[Path],
    root: Path,
    closed_at: datetime,
    now: datetime,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    starts: list[datetime] = []
    for expected_number, (entry, path) in enumerate(
        zip(manifest["attempts"], paths), start=1
    ):
        if entry["attempt_number"] != expected_number:
            raise InvalidRecord("manifest attempt order must be contiguous from one")
        if sha256_file(path) != entry["record_sha256"]:
            raise InvalidRecord(f"manifest record SHA-256 mismatch: {path.name}")
        record = load_json(path)
        validate_record(record, str(path), root, closed_at, now)
        if (
            record["cohort_id"] != manifest["cohort_id"]
            or record["attempt_id"] != entry["attempt_id"]
            or record["attempt_number"] != expected_number
        ):
            raise InvalidRecord("record identity does not match manifest order")
        if record["session"]["primary_format"] != manifest["primary_format"]:
            raise InvalidRecord("record primary format differs from manifest")
        metadata = {field: manifest["artifact"][field] for field in ARTIFACT_FIELDS}
        if record["artifact"] != metadata:
            raise InvalidRecord("record artifact metadata differs from manifest")
        starts.append(
            parse_timestamp(record["session"]["started_at"], f"{path}.started_at")
        )
        records.append(record)
    if starts != sorted(starts):
        raise InvalidRecord("record start times contradict manifest attempt order")
    attempt_ids = [entry["attempt_id"] for entry in manifest["attempts"]]
    if len(attempt_ids) != len(set(attempt_ids)):
        raise InvalidRecord("manifest attempt_id values must be unique")
    return records


def load_cohort(manifest_path: Path, now: datetime | None = None) -> Cohort:
    clock = now or default_now()
    manifest = load_json(manifest_path)
    attempts = manifest.get("attempts")
    if isinstance(attempts, list) and len(attempts) > MAX_STARTED_ATTEMPTS:
        raise InvalidRecord("manifest cannot enumerate more than seven started attempts")
    executing_root = Path(__file__).resolve().parents[1]
    validate_json_schema(
        manifest, executing_root / MANIFEST_SCHEMA_PATH, str(manifest_path)
    )
    root = Path(manifest["repo_root"]).resolve(strict=True)
    if root != executing_root:
        raise InvalidRecord("repo_root must be the repository running this scorer")
    if (
        manifest["target_completed"] != TARGET_COMPLETED
        or manifest["max_started_attempts"] != MAX_STARTED_ATTEMPTS
        or manifest["selection_rule"] != SELECTION_RULE
    ):
        raise InvalidRecord("manifest cohort rules differ from the frozen contract")
    if not TARGET_COMPLETED <= len(manifest["attempts"]) <= MAX_STARTED_ATTEMPTS:
        raise InvalidRecord("manifest must enumerate five to seven started attempts")
    registered_at = parse_timestamp(manifest["registered_at"], "manifest.registered_at")
    closed_at = parse_timestamp(manifest["closed_at"], "manifest.closed_at")
    if closed_at > clock:
        raise InvalidRecord("manifest.closed_at cannot be in the future")
    _verify_canonical_repo(root, manifest["artifact"]["git_commit"])
    _verify_contract(manifest, root)
    _, record_paths = _discover_attempt_paths(manifest, manifest_path, root)
    records = _load_attempts(manifest, record_paths, root, closed_at, clock)
    starts = [
        parse_timestamp(record["session"]["started_at"], "record.started_at")
        for record in records
    ]
    completions = [
        parse_timestamp(record["session"]["completed_at"], "record.completed_at")
        for record in records
    ]
    if registered_at >= starts[0]:
        raise InvalidRecord("manifest registered_at must precede attempt one")
    if closed_at < max(completions):
        raise InvalidRecord("manifest closure precedes a recorded attempt")
    eligible_completed = sorted(
        (
            record
            for record in records
            if is_eligible(record) and record["session"]["stopped_early"] is False
        ),
        key=lambda record: (
            parse_timestamp(
                record["session"]["completed_at"], "eligible completion"
            ),
            record["attempt_number"],
        ),
    )
    if len(eligible_completed) < TARGET_COMPLETED:
        reasons: set[str] = set()
        for record in records:
            if is_eligible(record):
                continue
            item = record["eligibility"]
            if item["age_18_or_over"] is not True:
                reasons.add("age_18_or_over")
            if item["participated_in_prior_book_pilot"] is not False:
                reasons.add("prior pilot participation")
            if item["seen_tested_passages_before"] is not False:
                reasons.add("seen tested passages")
            if not reasons:
                reasons.add("other eligibility rule")
        detail = ", ".join(sorted(reasons))
        raise InvalidRecord(
            f"cohort has fewer than five completed eligible attempts; {detail}"
        )
    counted = eligible_completed[:TARGET_COMPLETED]
    fifth = counted[-1]
    fifth_completion = parse_timestamp(
        fifth["session"]["completed_at"], "fifth completion"
    )
    if any(start > fifth_completion for start in starts):
        raise InvalidRecord("an attempt started after the fifth eligible completion")
    reader_ids = [record["reader_id"] for record in records]
    if len(reader_ids) != len(set(reader_ids)):
        raise InvalidRecord("reader_id values must be unique across all attempts")
    artifact = manifest["artifact"]
    try:
        evidence = verify_artifacts(
            {field: artifact[field] for field in ARTIFACT_FIELDS},
            root,
            _resolve_inside(artifact["pdf_path"], root, root, "PDF"),
            _resolve_inside(artifact["epub_path"], root, root, "EPUB"),
        )
    except ArtifactVerificationError as error:
        raise InvalidRecord(str(error)) from error
    stopped_counts = {
        category: sum(
            record["session"]["stop_category"] == category for record in records
        )
        for category in {
            record["session"]["stop_category"] for record in records
        }
        if category != "none"
    }
    return Cohort(
        manifest=manifest,
        records=records,
        counted_records=counted,
        evidence=evidence,
        distress_stops=stopped_counts.get("distress", 0),
        stopped_counts=stopped_counts,
    )
