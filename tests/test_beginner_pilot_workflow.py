from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from _beginner_pilot_v2_fixtures import (
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


class BeginnerPilotWorkflowTests(unittest.TestCase):
    def test_init_freezes_candidate_without_claiming_participant_evidence(self) -> None:
        with workflow_artifact_repo() as ctx:
            result = run_workflow(
                ctx["repo_root"],
                "init",
                "--cohort-id",
                COHORT_ID,
                "--primary-format",
                "pdf",
                "--registered-at",
                REGISTERED_AT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            registration_path = (
                ctx["repo_root"]
                / "build"
                / "beginner-pilot"
                / COHORT_ID
                / "registration.json"
            )
            registration = json.loads(registration_path.read_text(encoding="utf-8"))
            self.assertEqual(
                registration["evidence_status"],
                "registration_only_not_participant_evidence",
            )
            self.assertEqual(
                registration["preregistration_status"],
                "local_timestamp_only_not_independent_preregistration",
            )
            self.assertEqual(
                registration["artifact"]["git_commit"],
                ctx["artifact"]["git_commit"],
            )
            self.assertEqual(
                {
                    key: registration["artifact"][key]
                    for key in ctx["artifact"]
                },
                ctx["artifact"],
            )
            self.assertFalse((registration_path.parent / "manifest.json").exists())
            self.assertIn("not participant evidence", result.stdout)

    def test_new_attempt_requires_explicit_consent_and_stays_invalid(self) -> None:
        with workflow_artifact_repo() as ctx:
            init = run_workflow(
                ctx["repo_root"],
                "init",
                "--cohort-id",
                COHORT_ID,
                "--primary-format",
                "pdf",
                "--registered-at",
                REGISTERED_AT,
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            refused = run_workflow(
                ctx["repo_root"],
                "new-attempt",
                "--cohort-id",
                COHORT_ID,
                "--started-at",
                "2026-07-02T09:00:00Z",
            )
            self.assertEqual(refused.returncode, 2)
            self.assertIn("only after explicit consent", refused.stderr)

            created = run_workflow(
                ctx["repo_root"],
                "new-attempt",
                "--cohort-id",
                COHORT_ID,
                "--started-at",
                "2026-07-02T09:00:00Z",
                "--consent-confirmed",
                "--include-epub-smoke",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            records_dir = (
                ctx["repo_root"]
                / "build"
                / "beginner-pilot"
                / COHORT_ID
                / "records"
            )
            paths = list(records_dir.glob("*.json"))
            self.assertEqual(len(paths), 1)
            draft = json.loads(paths[0].read_text(encoding="utf-8"))
            self.assertIn("_draft_only", draft)
            self.assertIsNone(draft["tasks"]["insight_map"]["first_answer"])
            self.assertIsNone(draft["session"]["prompts_displayed_in_writing"])
            self.assertIsNone(draft["session"]["prompt_rereading_allowed"])
            self.assertIsNone(draft["session"]["moderator_followup_cues_used"])
            self.assertIsNone(
                draft["eligibility"]["rubric_seen_before_first_answers"]
            )
            self.assertIsNone(
                draft["epub_smoke"]["criteria"]["vietnamese_diacritics"]
            )
            self.assertTrue(draft["consent_confirmed"])
            self.assertIn("intentionally schema-invalid", created.stdout)

    def test_finalize_normalizes_records_and_runs_both_public_reports(self) -> None:
        with workflow_artifact_repo() as ctx:
            init = run_workflow(
                ctx["repo_root"],
                "init",
                "--cohort-id",
                COHORT_ID,
                "--primary-format",
                "pdf",
                "--registered-at",
                REGISTERED_AT,
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            records_dir = (
                ctx["repo_root"]
                / "build"
                / "beginner-pilot"
                / COHORT_ID
                / "records"
            )
            payloads = [
                build_record(
                    f"reader-0{index}",
                    ctx["artifact"],
                    attempt_number=index,
                )
                for index in range(1, 6)
            ]
            materialize_records(records_dir, payloads)
            for path in records_dir.glob("*.json"):
                path.chmod(0o600)

            result = run_workflow(
                ctx["repo_root"],
                "finalize",
                "--cohort-id",
                COHORT_ID,
                "--closed-at",
                CLOSED_AT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            cohort_dir = records_dir.parent
            manifest = json.loads(
                (cohort_dir / "manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(len(manifest["attempts"]), 5)
            self.assertTrue((cohort_dir / "aggregate-report.md").is_file())
            self.assertTrue((cohort_dir / "reader-app-report.md").is_file())
            self.assertIn("Cohort result: PASS", result.stdout)
            normalized = json.loads(
                sorted(records_dir.glob("*.json"))[0].read_text(encoding="utf-8")
            )
            self.assertNotIn("_draft_only", normalized)
            self.assertEqual(normalized["delete_by"], "2026-08-05T12:00:00+00:00")

    def test_finalize_refuses_unfilled_draft_without_creating_manifest(self) -> None:
        with workflow_artifact_repo() as ctx:
            init = run_workflow(
                ctx["repo_root"],
                "init",
                "--cohort-id",
                COHORT_ID,
                "--primary-format",
                "pdf",
                "--registered-at",
                REGISTERED_AT,
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            for index in range(1, 6):
                created = run_workflow(
                    ctx["repo_root"],
                    "new-attempt",
                    "--cohort-id",
                    COHORT_ID,
                    "--started-at",
                    f"2026-07-0{index + 1}T09:00:00Z",
                    "--consent-confirmed",
                )
                self.assertEqual(created.returncode, 0, created.stderr)
            result = run_workflow(
                ctx["repo_root"],
                "finalize",
                "--cohort-id",
                COHORT_ID,
                "--closed-at",
                "2026-07-07T12:00:00Z",
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("is not of type", result.stderr)
            self.assertFalse(
                (
                    ctx["repo_root"]
                    / "build"
                    / "beginner-pilot"
                    / COHORT_ID
                    / "manifest.json"
                ).exists()
            )

if __name__ == "__main__":
    unittest.main()
