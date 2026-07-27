from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from beginner_pilot_contract import (  # noqa: E402
    CANONICAL_ORIGIN_URLS,
    CANONICAL_REMOTE_REF,
    CONTRACT_PATHS,
    EPUB_CRITERIA,
    MANIFEST_SCHEMA_PATH,
    MAX_STARTED_ATTEMPTS,
    RECORD_SCHEMA_PATH,
    SELECTION_RULE,
    STOP_REASON_CODES,
    TARGET_COMPLETED,
    TASK_CRITERIA,
)

RECORD_SCHEMA_FILE = ROOT / RECORD_SCHEMA_PATH
MANIFEST_SCHEMA_FILE = ROOT / MANIFEST_SCHEMA_PATH
COHORT_ID = "cohort-v2-001"
SECTION_FINDING_PROMPT = (
    "Find the section that separates editorial guidance from canonical claims."
)
DEFAULT_MANIFEST_CLOSED_AT = "2026-07-06T12:00:00Z"


def dt(day: int, hour: int = 9, minute: int = 0) -> datetime:
    return datetime(2026, 7, day, hour, minute, tzinfo=timezone.utc)


def iso_at(day: int, hour: int = 9, minute: int = 0) -> str:
    return dt(day, hour, minute).isoformat().replace("+00:00", "Z")


def default_delete_by(started_at: str, closed_at: str = DEFAULT_MANIFEST_CLOSED_AT) -> str:
    started_value = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    closed_value = datetime.fromisoformat(closed_at.replace("Z", "+00:00"))
    delete_by_value = min(started_value + timedelta(days=90), closed_value + timedelta(days=30))
    return delete_by_value.isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdf_pages(path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise AssertionError("pdfinfo output did not include a page count")


def base_task(task_id: str) -> dict[str, Any]:
    return {
        "outcome": "answered",
        "completed": True,
        "first_answer_recorded": True,
        "first_answer": f"{task_id} first answer",
        "source_locator": f"{task_id} source locator",
        "elapsed_seconds": 30,
        "hint_used": False,
        "criteria": {name: True for name in TASK_CRITERIA[task_id]},
        "notes": "",
    }


def unanswered_task(task_id: str, outcome: str) -> dict[str, Any]:
    return {
        "outcome": outcome,
        "completed": False,
        "first_answer_recorded": False,
        "first_answer": "",
        "source_locator": "",
        "elapsed_seconds": 0,
        "hint_used": False,
        "criteria": {name: False for name in TASK_CRITERIA[task_id]},
        "notes": outcome,
    }


def base_repeat_task(label: str) -> dict[str, Any]:
    return {
        "outcome": "answered",
        "first_answer_recorded": True,
        "first_answer": f"{label} repeated answer",
        "source_locator": f"{label} repeated locator",
        "elapsed_seconds": 25,
        "hint_used": False,
        "passed": True,
        "notes": "",
    }


def base_smoke() -> dict[str, Any]:
    return {
        "device": "iPhone 15, iOS 19",
        "reader_app": "Books",
        "reader_app_version": "19.0",
        "text_scale_percent": 150,
        "dark_mode": True,
        "repeated_tasks": {
            "start_route": base_repeat_task("start_route"),
            "section_finding": base_repeat_task("section_finding"),
        },
        "criteria": {name: True for name in EPUB_CRITERIA},
        "notes": "",
    }


def build_record(
    reader_id: str,
    artifact: dict[str, Any],
    *,
    attempt_number: int,
    started_at: str | None = None,
    completed_at: str | None = None,
    eligible: bool = True,
    stopped: bool = False,
    stop_category: str = "none",
    delete_by: str | None = None,
    primary_format: str = "pdf",
    epub_smoke: dict[str, Any] | None = None,
    task_overrides: dict[str, dict[str, Any]] | None = None,
    age_18_or_over: bool = True,
    participated_in_prior_book_pilot: bool = False,
    seen_tested_passages_before: bool = False,
    rubric_seen_before_first_answers: bool = False,
) -> dict[str, Any]:
    started_at = started_at or iso_at(attempt_number, 9)
    completed_at = completed_at or iso_at(attempt_number, 10)
    delete_by = delete_by or default_delete_by(started_at)
    attempt_id = f"attempt-{attempt_number:02d}"
    eligibility = {
        "vietnamese_comfort": "native",
        "meditation_sessions_lifetime": 1,
        "retreats_completed": 0,
        "knows_mahasi_vocabulary": False,
        "read_book_before": False,
        "experienced_buddhist": False,
        "is_editor": False,
        "is_source_reviewer": False,
        "age_18_or_over": age_18_or_over,
        "participated_in_prior_book_pilot": participated_in_prior_book_pilot,
        "seen_tested_passages_before": seen_tested_passages_before,
        "rubric_seen_before_first_answers": rubric_seen_before_first_answers,
    }
    if not eligible:
        eligibility["experienced_buddhist"] = True

    session = {
        "primary_format": primary_format,
        "moderator_is_editor": False,
        "prompts_displayed_in_writing": True,
        "prompt_rereading_allowed": True,
        "moderator_followup_cues_used": False,
        "started_at": started_at,
        "completed_at": completed_at,
        "stopped_early": stopped,
        "stop_category": stop_category if stopped else "none",
        "stop_reason": (
            STOP_REASON_CODES[stop_category] if stopped else STOP_REASON_CODES["none"]
        ),
        "device": "iPhone 15, iOS 19",
        "reader_app": "Books",
        "reader_app_version": "19.0",
        "text_scale_percent": 150,
        "dark_mode": True,
    }

    tasks = {task_id: base_task(task_id) for task_id in TASK_CRITERIA}
    if stopped:
        tasks = {
            task_id: unanswered_task(task_id, "not_reached")
            for task_id in TASK_CRITERIA
        }
        for task in tasks.values():
            task["notes"] = ""
    elif task_overrides:
        for task_id, overrides in task_overrides.items():
            existing_criteria = dict(tasks[task_id]["criteria"])
            tasks[task_id].update(overrides)
            if "criteria" in overrides:
                existing_criteria.update(overrides["criteria"])
                tasks[task_id]["criteria"] = existing_criteria

    return {
        "schema_version": 2,
        "cohort_id": COHORT_ID,
        "attempt_id": attempt_id,
        "attempt_number": attempt_number,
        "delete_by": delete_by,
        "reader_id": reader_id,
        "consent_confirmed": True,
        "eligibility": eligibility,
        "artifact": artifact,
        "session": session,
        "tasks": tasks,
        "epub_smoke": None if stopped else (epub_smoke or base_smoke()),
    }


def write_json(path: Path, payload: dict[str, Any], *, allow_nan: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=allow_nan) + "\n",
        encoding="utf-8",
    )


def materialize_records(records_dir: Path, payloads: list[dict[str, Any]]) -> list[Path]:
    paths: list[Path] = []
    for payload in payloads:
        path = records_dir / f"{payload['attempt_number']:02d}-{payload['attempt_id']}.json"
        write_json(path, payload)
        paths.append(path)
    return paths


def _contract_hashes(repo_root: Path) -> list[dict[str, str]]:
    return {
        relative_path: sha256_file(repo_root / relative_path)
        for relative_path in CONTRACT_PATHS
    }


def write_manifest(
    path: Path,
    *,
    repo_root: Path,
    pdf_path: Path,
    epub_path: Path,
    artifact: dict[str, Any],
    attempt_paths: list[Path],
    registered_at: str = "2026-07-01T08:00:00Z",
    closed_at: str = DEFAULT_MANIFEST_CLOSED_AT,
    primary_format: str = "pdf",
) -> dict[str, Any]:
    records_dir = attempt_paths[0].parent
    attempts = []
    for index, attempt_path in enumerate(attempt_paths, start=1):
        attempts.append(
            {
                "attempt_number": index,
                "attempt_id": attempt_path.stem.split("-", 1)[1],
                "record_path": attempt_path.name,
                "record_sha256": sha256_file(attempt_path),
            }
        )
    manifest = {
        "schema_version": 2,
        "cohort_id": COHORT_ID,
        "registered_at": registered_at,
        "closed_at": closed_at,
        "repo_root": str(repo_root),
        "records_dir": str(records_dir),
        "primary_format": primary_format,
        "target_completed": TARGET_COMPLETED,
        "max_started_attempts": MAX_STARTED_ATTEMPTS,
        "selection_rule": SELECTION_RULE,
        "epub_section_finding_prompt": SECTION_FINDING_PROMPT,
        "artifact": {
            **artifact,
            "pdf_path": str(pdf_path),
            "epub_path": str(epub_path),
        },
        "contract": {
            "git_commit": artifact["git_commit"],
            "files": _contract_hashes(repo_root),
        },
        "attempts": attempts,
    }
    write_json(path, manifest)
    return manifest


def write_manifest_case(
    repo_root: Path,
    *,
    artifact: dict[str, Any],
    pdf_path: Path,
    epub_path: Path,
    payloads: list[dict[str, Any]],
    registered_at: str = "2026-07-01T08:00:00Z",
    closed_at: str = DEFAULT_MANIFEST_CLOSED_AT,
    primary_format: str = "pdf",
) -> tuple[Path, list[Path], dict[str, Any]]:
    cohort_dir = repo_root / "build" / "beginner-pilot" / COHORT_ID
    records_dir = cohort_dir / "records"
    attempt_paths = materialize_records(records_dir, payloads)
    manifest_path = cohort_dir / "manifest.json"
    manifest = write_manifest(
        manifest_path,
        repo_root=repo_root,
        pdf_path=pdf_path,
        epub_path=epub_path,
        artifact=artifact,
        attempt_paths=attempt_paths,
        registered_at=registered_at,
        closed_at=closed_at,
        primary_format=primary_format,
    )
    return manifest_path, attempt_paths, manifest


def run_cli(
    manifest_path: Path, *extra_args: str
) -> subprocess.CompletedProcess[str]:
    repo_root = manifest_path.parents[3]
    cli_path = repo_root / "scripts" / "score-beginner-pilot.py"
    return subprocess.run(
        [sys.executable, str(cli_path), str(manifest_path), *extra_args],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )


@contextmanager
def temp_artifact_repo() -> Any:
    with tempfile.TemporaryDirectory(dir=ROOT, prefix="tmp-pilot-v2-") as tmp:
        repo_root = Path(tmp)
        shutil.copy2(ROOT / ".gitignore", repo_root / ".gitignore")
        for relative_path in CONTRACT_PATHS:
            source = ROOT / relative_path
            target = repo_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        dist_dir = repo_root / "dist"
        dist_dir.mkdir(parents=True)
        pdf_path = dist_dir / "huong-den-nhap-luu.pdf"
        epub_path = dist_dir / "huong-den-nhap-luu.epub"
        shutil.copy2(ROOT / "dist" / "huong-den-nhap-luu.pdf", pdf_path)
        shutil.copy2(ROOT / "dist" / "huong-den-nhap-luu.epub", epub_path)

        subprocess.run(["git", "init"], cwd=repo_root, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.name", "Pilot Tests"],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "pilot-tests@example.com"],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
        subprocess.run(["git", "add", "."], cwd=repo_root, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "fixture artifacts and contracts"],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
        commit = (
            subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            )
            .stdout.strip()
        )
        canonical_origin = sorted(CANONICAL_ORIGIN_URLS)[0]
        subprocess.run(
            ["git", "remote", "add", "origin", canonical_origin],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "update-ref", CANONICAL_REMOTE_REF, commit],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
        artifact = {
            "git_commit": commit,
            "pdf_sha256": sha256_file(pdf_path),
            "epub_sha256": sha256_file(epub_path),
            "pdf_pages": pdf_pages(pdf_path),
        }
        yield {
            "repo_root": repo_root,
            "pdf_path": pdf_path,
            "epub_path": epub_path,
            "artifact": artifact,
        }
