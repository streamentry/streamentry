from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from _beginner_pilot_v2_fixtures import (
    CANONICAL_REMOTE_REF,
    COHORT_ID,
    build_record,
    materialize_records,
)
from _beginner_pilot_workflow_fixtures import workflow_artifact_repo


REGISTERED_AT = "2026-07-01T08:00:00Z"
CLOSED_AT = "2026-07-06T12:00:00Z"


def run_workflow(repo_root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "prepare-beginner-pilot.py"),
            *arguments,
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )


def initialize(repo_root: Path) -> subprocess.CompletedProcess[str]:
    return run_workflow(
        repo_root,
        "init",
        "--cohort-id",
        COHORT_ID,
        "--primary-format",
        "pdf",
        "--registered-at",
        REGISTERED_AT,
    )


def records_dir(repo_root: Path) -> Path:
    return repo_root / "build" / "beginner-pilot" / COHORT_ID / "records"


def materialize_private_records(
    destination: Path, artifact: dict[str, object]
) -> list[Path]:
    paths = materialize_records(
        destination,
        [
            build_record(
                f"reader-0{index}",
                artifact,
                attempt_number=index,
            )
            for index in range(1, 6)
        ],
    )
    for path in paths:
        path.chmod(0o600)
    return paths


class BeginnerPilotWorkflowAdversarialTests(unittest.TestCase):
    def test_finalize_refuses_candidate_commit_drift(self) -> None:
        with workflow_artifact_repo() as ctx:
            init = initialize(ctx["repo_root"])
            self.assertEqual(init.returncode, 0, init.stderr)
            destination = records_dir(ctx["repo_root"])
            materialize_private_records(destination, ctx["artifact"])
            drift_file = ctx["repo_root"] / "candidate-drift.txt"
            drift_file.write_text("new candidate\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", "candidate-drift.txt"],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "create another candidate"],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            new_head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            subprocess.run(
                ["git", "update-ref", CANONICAL_REMOTE_REF, new_head],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )

            result = run_workflow(
                ctx["repo_root"],
                "finalize",
                "--cohort-id",
                COHORT_ID,
                "--closed-at",
                CLOSED_AT,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("candidate commit changed", result.stderr)
            self.assertFalse((destination.parent / "manifest.json").exists())

    def test_finalize_refuses_world_readable_raw_record(self) -> None:
        with workflow_artifact_repo() as ctx:
            init = initialize(ctx["repo_root"])
            self.assertEqual(init.returncode, 0, init.stderr)
            destination = records_dir(ctx["repo_root"])
            paths = materialize_private_records(destination, ctx["artifact"])
            paths[0].chmod(0o644)

            result = run_workflow(
                ctx["repo_root"],
                "finalize",
                "--cohort-id",
                COHORT_ID,
                "--closed-at",
                CLOSED_AT,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("readable by group or others", result.stderr)
            self.assertFalse((destination.parent / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
