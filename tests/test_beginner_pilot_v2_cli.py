from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
import zipfile

from _beginner_pilot_v2_fixtures import (
    CANONICAL_REMOTE_REF,
    COHORT_ID,
    base_task,
    build_record,
    run_cli,
    temp_artifact_repo,
    unanswered_task,
    write_json,
    write_manifest_case,
)


class BeginnerPilotV2CliTests(unittest.TestCase):
    def test_exits_zero_for_authoritative_manifest_with_first_five_eligible_completed(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record("reader-00", ctx["artifact"], attempt_number=1, eligible=False),
                build_record("reader-01", ctx["artifact"], attempt_number=2),
                build_record("reader-02", ctx["artifact"], attempt_number=3),
                build_record("reader-03", ctx["artifact"], attempt_number=4),
                build_record("reader-04", ctx["artifact"], attempt_number=5),
                build_record("reader-05", ctx["artifact"], attempt_number=6),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Verdict: **PASS**", result.stdout)
            self.assertNotIn("iPhone 15", result.stdout)
            self.assertIn("app `Books`", result.stdout)
            self.assertIn("version `19.0`", result.stdout)
            self.assertIn("text scale `150%`", result.stdout)
            self.assertIn("dark mode `on`", result.stdout)
            self.assertIn("iOS/iPadOS device", result.stdout)
            self.assertNotIn("reader-01", result.stdout)

    def test_output_write_failure_exits_two(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 6)
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(
                manifest_path,
                "--output",
                str(manifest_path.parent),
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid beginner-pilot data", result.stderr.lower())

    def test_exits_one_when_the_sixth_completed_record_would_rescue_the_first_five(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    "reader-01",
                    ctx["artifact"],
                    attempt_number=1,
                    task_overrides={
                        "safety": {"criteria": {"seeks_qualified_support": False}}
                    },
                ),
                build_record("reader-02", ctx["artifact"], attempt_number=2),
                build_record("reader-03", ctx["artifact"], attempt_number=3),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
                build_record(
                    "reader-06",
                    ctx["artifact"],
                    attempt_number=6,
                    started_at="2026-07-05T09:30:00Z",
                    completed_at="2026-07-05T11:00:00Z",
                ),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("Verdict: **FAIL**", result.stdout)

    def test_rejects_manifest_when_discovery_omits_a_listed_attempt(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(f"reader-0{index}", ctx["artifact"], attempt_number=index)
                for index in range(1, 6)
            ]
            manifest_path, attempt_paths, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            attempt_paths[-1].unlink()
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("manifest", result.stderr.lower())

    def test_rejects_manifest_when_an_unlisted_attempt_is_added(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(f"reader-0{index}", ctx["artifact"], attempt_number=index)
                for index in range(1, 6)
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            extra = build_record("reader-06", ctx["artifact"], attempt_number=6)
            extra_path = (
                ctx["repo_root"]
                / "build"
                / "beginner-pilot"
                / COHORT_ID
                / "records"
                / "06-attempt-06.json"
            )
            write_json(extra_path, extra)
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("manifest", result.stderr.lower())

    def test_rejects_manifest_when_attempt_order_is_rewritten(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(f"reader-0{index}", ctx["artifact"], attempt_number=index)
                for index in range(1, 6)
            ]
            manifest_path, attempt_paths, manifest = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            manifest["attempts"] = [manifest["attempts"][1], manifest["attempts"][0], *manifest["attempts"][2:]]
            write_json(manifest_path, manifest)
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("order", result.stderr.lower())

    def test_rejects_more_than_seven_started_attempts(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record("reader-01", ctx["artifact"], attempt_number=1, eligible=False),
                build_record("reader-02", ctx["artifact"], attempt_number=2, eligible=False),
                build_record("reader-03", ctx["artifact"], attempt_number=3, eligible=False),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
                build_record("reader-06", ctx["artifact"], attempt_number=6),
                build_record("reader-07", ctx["artifact"], attempt_number=7),
                build_record("reader-08", ctx["artifact"], attempt_number=8),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertTrue(
                "seven" in result.stderr.lower() or "too long" in result.stderr.lower()
            )

    def test_distress_stop_blocks_release_even_with_five_completed_records(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    "reader-stop",
                    ctx["artifact"],
                    attempt_number=1,
                    stopped=True,
                    stop_category="distress",
                ),
                build_record("reader-01", ctx["artifact"], attempt_number=2),
                build_record("reader-02", ctx["artifact"], attempt_number=3),
                build_record("reader-03", ctx["artifact"], attempt_number=4),
                build_record("reader-04", ctx["artifact"], attempt_number=5),
                build_record("reader-05", ctx["artifact"], attempt_number=6),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("stop", (result.stdout + result.stderr).lower())

    def test_skipped_task_counts_as_a_gate_failure(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    "reader-01",
                    ctx["artifact"],
                    attempt_number=1,
                    task_overrides={
                        "anchor_fallback": unanswered_task(
                            "anchor_fallback", "skipped"
                        )
                    },
                ),
                build_record("reader-02", ctx["artifact"], attempt_number=2),
                build_record("reader-03", ctx["artifact"], attempt_number=3),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("anchor_fallback", result.stdout)

    def test_not_reached_task_counts_as_a_gate_failure(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    "reader-01",
                    ctx["artifact"],
                    attempt_number=1,
                    task_overrides={
                        "fetters_and_fruits": unanswered_task(
                            "fetters_and_fruits", "not_reached"
                        )
                    },
                ),
                build_record("reader-02", ctx["artifact"], attempt_number=2),
                build_record("reader-03", ctx["artifact"], attempt_number=3),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("fetters_and_fruits", result.stdout)

    def test_epub_smoke_requires_repeated_section_finding_evidence_to_pass(self) -> None:
        with temp_artifact_repo() as ctx:
            weak_smoke = {
                "device": "iPhone 15, iOS 19",
                "reader_app": "Books",
                "reader_app_version": "19.0",
                "text_scale_percent": 150,
                "dark_mode": True,
                "repeated_tasks": {
                    "start_route": {
                        "outcome": "answered",
                        "first_answer_recorded": True,
                        "first_answer": "start route repeated answer",
                        "source_locator": "chapter 1",
                        "elapsed_seconds": 20,
                        "hint_used": False,
                        "passed": True,
                        "notes": "",
                    },
                    "section_finding": {
                        "outcome": "answered",
                        "first_answer_recorded": True,
                        "first_answer": "wrong section",
                        "source_locator": "none",
                        "elapsed_seconds": 45,
                        "hint_used": False,
                        "passed": False,
                        "notes": "",
                    },
                },
                "criteria": {
                    "reading_order": True,
                    "nested_toc": True,
                    "source_badges": True,
                    "cautions": True,
                    "links": True,
                    "vietnamese_diacritics": True,
                    "no_overlap_or_loss": True,
                    "no_color_only_meaning": True,
                },
                "notes": "",
            }
            payloads = [
                build_record(
                    "reader-01",
                    ctx["artifact"],
                    attempt_number=1,
                    epub_smoke=weak_smoke,
                ),
                build_record("reader-02", ctx["artifact"], attempt_number=2),
                build_record("reader-03", ctx["artifact"], attempt_number=3),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("epub", (result.stdout + result.stderr).lower())

    def test_rejects_non_zip_epub_even_when_hashes_match_metadata(self) -> None:
        with temp_artifact_repo() as ctx:
            ctx["epub_path"].write_bytes(b"this is not a zip archive")
            artifact = dict(ctx["artifact"])
            artifact["epub_sha256"] = hashlib.sha256(b"this is not a zip archive").hexdigest()
            payloads = [
                build_record(f"reader-0{index}", artifact, attempt_number=index)
                for index in range(1, 6)
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=artifact,
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("epub", result.stderr.lower())

    def test_rejects_epub_missing_container_xml(self) -> None:
        with temp_artifact_repo() as ctx:
            with zipfile.ZipFile(ctx["epub_path"], "w") as archive:
                archive.writestr("mimetype", b"application/epub+zip")
            artifact = dict(ctx["artifact"])
            artifact["epub_sha256"] = hashlib.sha256(ctx["epub_path"].read_bytes()).hexdigest()
            payloads = [
                build_record(f"reader-0{index}", artifact, attempt_number=index)
                for index in range(1, 6)
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=artifact,
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("container", result.stderr.lower())

    def test_rejects_recorded_artifact_hash_tampering(self) -> None:
        with temp_artifact_repo() as ctx:
            artifact = dict(ctx["artifact"])
            artifact["pdf_sha256"] = "0" * 64
            payloads = [
                build_record(f"reader-0{index}", artifact, attempt_number=index)
                for index in range(1, 6)
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=artifact,
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("hash", result.stderr.lower())

    def test_rejects_manifest_contract_hash_drift(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(f"reader-0{index}", ctx["artifact"], attempt_number=index)
                for index in range(1, 6)
            ]
            manifest_path, _, manifest = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            first_key = next(iter(manifest["contract"]["files"]))
            manifest["contract"]["files"][first_key] = "f" * 64
            write_json(manifest_path, manifest)
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("contract", result.stderr.lower())

    def test_rejects_manifest_when_preregistration_starts_after_first_session(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(f"reader-0{index}", ctx["artifact"], attempt_number=index)
                for index in range(1, 6)
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
                registered_at="2026-07-01T09:30:00Z",
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("registered_at", result.stderr.lower())

    def test_rejects_underage_reader(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    "reader-01",
                    ctx["artifact"],
                    attempt_number=1,
                    age_18_or_over=False,
                ),
                build_record("reader-02", ctx["artifact"], attempt_number=2),
                build_record("reader-03", ctx["artifact"], attempt_number=3),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("age", result.stderr.lower())

    def test_rejects_reader_who_participated_in_a_prior_book_pilot(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    "reader-01",
                    ctx["artifact"],
                    attempt_number=1,
                    participated_in_prior_book_pilot=True,
                ),
                build_record("reader-02", ctx["artifact"], attempt_number=2),
                build_record("reader-03", ctx["artifact"], attempt_number=3),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("prior", result.stderr.lower())

    def test_rejects_reader_who_has_seen_tested_passages_before(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    "reader-01",
                    ctx["artifact"],
                    attempt_number=1,
                    seen_tested_passages_before=True,
                ),
                build_record("reader-02", ctx["artifact"], attempt_number=2),
                build_record("reader-03", ctx["artifact"], attempt_number=3),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("passage", result.stderr.lower())

    def test_rejects_delete_by_beyond_completed_plus_ninety_days(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    "reader-01",
                    ctx["artifact"],
                    attempt_number=1,
                    completed_at="2026-07-01T10:00:00Z",
                    delete_by="2026-10-01T10:00:01Z",
                ),
                build_record("reader-02", ctx["artifact"], attempt_number=2),
                build_record("reader-03", ctx["artifact"], attempt_number=3),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("delete_by", result.stderr.lower())

    def test_rejects_nonstandard_json_constants(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record("reader-01", ctx["artifact"], attempt_number=1),
                build_record("reader-02", ctx["artifact"], attempt_number=2),
                build_record("reader-03", ctx["artifact"], attempt_number=3),
                build_record("reader-04", ctx["artifact"], attempt_number=4),
                build_record("reader-05", ctx["artifact"], attempt_number=5),
            ]
            manifest_path, attempt_paths, manifest = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            first_path = attempt_paths[0]
            first_payload = json.loads(first_path.read_text(encoding="utf-8"))
            first_payload["tasks"]["start_route"]["elapsed_seconds"] = float("nan")
            write_json(first_path, first_payload, allow_nan=True)
            manifest["attempts"][0]["record_sha256"] = hashlib.sha256(first_path.read_bytes()).hexdigest()
            write_json(manifest_path, manifest)
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("json", result.stderr.lower())

    def test_rejects_manifest_when_an_attempt_starts_after_fifth_eligible_completion(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record("reader-01", ctx["artifact"], attempt_number=1, completed_at="2026-07-01T10:00:00Z"),
                build_record("reader-02", ctx["artifact"], attempt_number=2, completed_at="2026-07-02T10:00:00Z"),
                build_record("reader-03", ctx["artifact"], attempt_number=3, completed_at="2026-07-03T10:00:00Z"),
                build_record("reader-04", ctx["artifact"], attempt_number=4, completed_at="2026-07-04T10:00:00Z"),
                build_record("reader-05", ctx["artifact"], attempt_number=5, completed_at="2026-07-05T10:00:00Z"),
                build_record(
                    "reader-06",
                    ctx["artifact"],
                    attempt_number=6,
                    started_at="2026-07-05T10:00:01Z",
                    completed_at="2026-07-05T11:00:00Z",
                ),
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("fifth", result.stderr.lower())

    def test_overlapping_sessions_are_selected_by_completion_not_start_order(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 5)
            ]
            payloads.extend(
                [
                    build_record(
                        "reader-05",
                        ctx["artifact"],
                        attempt_number=5,
                        started_at="2026-07-05T09:00:00Z",
                        completed_at="2026-07-05T12:00:00Z",
                    ),
                    build_record(
                        "reader-06",
                        ctx["artifact"],
                        attempt_number=6,
                        started_at="2026-07-05T09:30:00Z",
                        completed_at="2026-07-05T10:30:00Z",
                        task_overrides={
                            "safety": {
                                "criteria": {"seeks_qualified_support": False}
                            }
                        },
                    ),
                ]
            )
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("Verdict: **FAIL**", result.stdout)
            self.assertIn("safety", result.stdout)

    def test_rejects_fully_answered_moderator_abort(self) -> None:
        with temp_artifact_repo() as ctx:
            stopped = build_record(
                "reader-stop",
                ctx["artifact"],
                attempt_number=1,
                stopped=True,
                stop_category="moderator_abort",
            )
            stopped["tasks"] = {
                task_id: base_task(task_id) for task_id in stopped["tasks"]
            }
            payloads = [
                stopped,
                *[
                    build_record(
                        f"reader-0{index}", ctx["artifact"], attempt_number=index
                    )
                    for index in range(2, 7)
                ],
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("not_reached", result.stderr)

    def test_rejects_task_resumption_after_not_reached(self) -> None:
        with temp_artifact_repo() as ctx:
            stopped = build_record(
                "reader-stop",
                ctx["artifact"],
                attempt_number=1,
                stopped=True,
                stop_category="technical",
            )
            task_ids = list(stopped["tasks"])
            stopped["tasks"][task_ids[0]] = base_task(task_ids[0])
            stopped["tasks"][task_ids[2]] = base_task(task_ids[2])
            payloads = [
                stopped,
                *[
                    build_record(
                        f"reader-0{index}", ctx["artifact"], attempt_number=index
                    )
                    for index in range(2, 7)
                ],
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("cannot resume", result.stderr)

    def test_rejects_ineligible_after_start_when_reader_is_eligible(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    "reader-stop",
                    ctx["artifact"],
                    attempt_number=1,
                    stopped=True,
                    stop_category="ineligible_after_start",
                ),
                *[
                    build_record(
                        f"reader-0{index}", ctx["artifact"], attempt_number=index
                    )
                    for index in range(2, 7)
                ],
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("failed eligibility", result.stderr)

    def test_rejects_records_dir_outside_exact_private_cohort_path(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 6)
            ]
            manifest_path, _, manifest = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            manifest["records_dir"] = str(manifest_path.parent)
            write_json(manifest_path, manifest)
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("records_dir", result.stderr)

    def test_rejects_git_tracked_private_manifest(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 6)
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            subprocess.run(
                [
                    "git",
                    "add",
                    "-f",
                    str(manifest_path.relative_to(ctx["repo_root"])),
                ],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("must not be Git-tracked", result.stderr)

    def test_rejects_git_tracked_private_attempt_record(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 6)
            ]
            manifest_path, attempt_paths, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            subprocess.run(
                [
                    "git",
                    "add",
                    "-f",
                    str(attempt_paths[0].relative_to(ctx["repo_root"])),
                ],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("must not be Git-tracked", result.stderr)

    def test_rejects_nested_unlisted_attempt_record(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 6)
            ]
            manifest_path, attempt_paths, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            hidden_attempt = attempt_paths[0].parent / "archived" / "06-attempt-06.json"
            write_json(
                hidden_attempt,
                build_record("reader-06", ctx["artifact"], attempt_number=6),
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("must not contain subdirectories", result.stderr)

    def test_rejects_distress_record_with_retained_task_note(self) -> None:
        with temp_artifact_repo() as ctx:
            distress = build_record(
                "reader-00",
                ctx["artifact"],
                attempt_number=1,
                stopped=True,
                stop_category="distress",
            )
            first_task = next(iter(distress["tasks"].values()))
            first_task["notes"] = "reader disclosed panic details"
            payloads = [
                distress,
                *[
                    build_record(
                        f"reader-0{index}",
                        ctx["artifact"],
                        attempt_number=index + 1,
                    )
                    for index in range(1, 6)
                ],
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("must erase task notes", result.stderr)

    def test_rejects_possible_contact_data_in_answer(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 6)
            ]
            payloads[0]["tasks"]["start_route"]["first_answer"] = (
                "Liên hệ reader@example.com để hỏi thêm"
            )
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("possible personal contact data", result.stderr)

    def test_rejects_noncanonical_origin(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 6)
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            subprocess.run(
                [
                    "git",
                    "remote",
                    "set-url",
                    "origin",
                    "https://github.com/example/not-streamentry.git",
                ],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("origin is not canonical", result.stderr)

    def test_rejects_artifact_commit_outside_origin_main_history(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 6)
            ]
            manifest_path, _, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            tree = subprocess.run(
                ["git", "rev-parse", "HEAD^{tree}"],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            unrelated = subprocess.run(
                ["git", "commit-tree", tree, "-m", "unrelated canonical tip"],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            subprocess.run(
                ["git", "update-ref", CANONICAL_REMOTE_REF, unrelated],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("not in canonical origin/main history", result.stderr)

    def test_rejects_raw_record_that_appeared_in_git_history(self) -> None:
        with temp_artifact_repo() as ctx:
            payloads = [
                build_record(
                    f"reader-0{index}", ctx["artifact"], attempt_number=index
                )
                for index in range(1, 6)
            ]
            manifest_path, attempt_paths, _ = write_manifest_case(
                ctx["repo_root"],
                artifact=ctx["artifact"],
                pdf_path=ctx["pdf_path"],
                epub_path=ctx["epub_path"],
                payloads=payloads,
            )
            relative = str(attempt_paths[0].relative_to(ctx["repo_root"]))
            subprocess.run(
                ["git", "add", "-f", relative],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "accidentally track raw record"],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "rm", "--cached", relative],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "remove raw record from index"],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            subprocess.run(
                ["git", "update-ref", CANONICAL_REMOTE_REF, head],
                cwd=ctx["repo_root"],
                check=True,
                capture_output=True,
            )
            result = run_cli(manifest_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("appeared in Git history", result.stderr)


if __name__ == "__main__":
    unittest.main()
