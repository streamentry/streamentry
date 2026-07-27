from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from _beginner_pilot_v2_fixtures import MANIFEST_SCHEMA_FILE, RECORD_SCHEMA_FILE

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from beginner_pilot_contract import (  # noqa: E402
    ELIGIBILITY_FIELDS,
    EPUB_FIELDS,
    REPEAT_FIELDS,
    STOP_REASON_CODES,
    TASK_CRITERIA,
    TASK_FIELDS,
    TOP_LEVEL_FIELDS,
)


class BeginnerPilotV2SchemaParityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record_schema = json.loads(RECORD_SCHEMA_FILE.read_text(encoding="utf-8"))

    def test_manifest_schema_file_exists_at_the_contract_path(self) -> None:
        self.assertTrue(
            MANIFEST_SCHEMA_FILE.exists(),
            f"missing manifest schema file at {MANIFEST_SCHEMA_FILE}",
        )

    def test_record_schema_requires_v2_attempt_identity_fields(self) -> None:
        required = set(self.record_schema["required"])
        self.assertTrue({"cohort_id", "attempt_id", "attempt_number", "delete_by"} <= required)
        self.assertTrue({"cohort_id", "attempt_id", "attempt_number", "delete_by"} <= TOP_LEVEL_FIELDS)

    def test_record_schema_requires_v2_eligibility_history_fields(self) -> None:
        required = set(self.record_schema["$defs"]["eligibility"]["required"])
        self.assertIn("age_18_or_over", required)
        self.assertIn("participated_in_prior_book_pilot", required)
        self.assertIn("seen_tested_passages_before", required)
        self.assertIn("age_18_or_over", ELIGIBILITY_FIELDS)
        self.assertIn("participated_in_prior_book_pilot", ELIGIBILITY_FIELDS)
        self.assertIn("seen_tested_passages_before", ELIGIBILITY_FIELDS)

    def test_record_schema_requires_structured_stop_category(self) -> None:
        required = set(self.record_schema["$defs"]["session"]["required"])
        self.assertIn("stop_category", required)

    def test_record_schema_stop_reasons_match_fixed_privacy_codes(self) -> None:
        allowed = set(
            self.record_schema["$defs"]["session"]["properties"]["stop_reason"]["enum"]
        )
        self.assertEqual(allowed, set(STOP_REASON_CODES.values()))

    def test_task_contract_includes_explicit_outcome_state(self) -> None:
        required = set(self.record_schema["$defs"]["task"]["required"])
        self.assertIn("outcome", required)
        self.assertIn("outcome", TASK_FIELDS)

    def test_safety_contract_requires_the_vietnam_emergency_route(self) -> None:
        required = set(
            self.record_schema["$defs"]["criteria_safety"]["required"]
        )
        self.assertIn("finds_vietnam_emergency_route", required)
        self.assertIn(
            "finds_vietnam_emergency_route",
            TASK_CRITERIA["safety"],
        )

    def test_insight_map_contract_tests_definition_and_maturation(self) -> None:
        required = set(
            self.record_schema["$defs"]["criteria_insight_map"]["required"]
        )
        expected = {
            "explains_change_in_way_of_knowing",
            "distinguishes_maturation_from_stage_production",
            "distinguishes_phenomenon_glimpse_region_and_attainment",
        }
        self.assertTrue(expected <= required)
        self.assertTrue(expected <= set(TASK_CRITERIA["insight_map"]))

    def test_fetter_contract_rejects_status_and_gender_exclusivity(self) -> None:
        required = set(
            self.record_schema["$defs"]["criteria_fetters_and_fruits"]["required"]
        )
        criterion = "rejects_monastic_or_male_only_restriction"
        self.assertIn(criterion, required)
        self.assertIn(criterion, TASK_CRITERIA["fetters_and_fruits"])

    def test_epub_smoke_contract_includes_repeated_task_evidence_objects(self) -> None:
        required = set(self.record_schema["$defs"]["epub_smoke"]["required"])
        self.assertIn("repeated_tasks", required)
        self.assertIn("repeated_tasks", EPUB_FIELDS)

    def test_repeat_task_contract_tracks_passed_and_source_evidence(self) -> None:
        self.assertIn("epub_repeated_task", self.record_schema["$defs"])
        repeated = self.record_schema["$defs"]["epub_repeated_task"]
        self.assertEqual(set(repeated["required"]), REPEAT_FIELDS)


if __name__ == "__main__":
    unittest.main()
