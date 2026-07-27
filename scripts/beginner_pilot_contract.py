"""Frozen field, rubric, and manifest constants for beginner pilot v2."""

from __future__ import annotations

TASK_CRITERIA = {
    "start_route": (
        "found_chapter_1",
        "described_seven_day_route",
        "found_early_safety_instruction",
    ),
    "anchor_fallback": (
        "selected_allowed_fallback",
        "kept_one_anchor",
        "rejected_object_cycling",
    ),
    "safety": (
        "stops_intensification",
        "rejects_pushing_through",
        "seeks_qualified_support",
        "finds_vietnam_emergency_route",
    ),
    "feeling_to_craving": (
        "distinguishes_tone_from_emotion",
        "gives_contact_feeling_craving_sequence",
        "keeps_feeling_and_craving_distinct",
    ),
    "evidential_limit": (
        "rejects_universal_easiest_claim",
        "identifies_editorial_intervention_point",
        "finds_chapter_4_caveat",
        "uses_source_badge_boundary",
    ),
    "insight_map": (
        "explains_change_in_way_of_knowing",
        "distinguishes_maturation_from_stage_production",
        "rejects_stage_diagnosis",
        "chapter_12_is_later_reference",
        "names_alternative_or_longitudinal_context",
    ),
    "retreat_decision": (
        "rejects_retreat",
        "identifies_missing_exit_policy",
        "identifies_medication_and_coercion",
    ),
    "fetters_and_fruits": (
        "names_first_three_fetters",
        "distinguishes_first_three_from_five_lower",
        "maps_stream_entry_and_non_returning",
        "distinguishes_four_fruits_from_dn2_title",
    ),
}

TASK_THRESHOLDS = {
    "start_route": 4,
    "anchor_fallback": 4,
    "safety": 5,
    "feeling_to_craving": 4,
    "evidential_limit": 4,
    "insight_map": 4,
    "retreat_decision": 5,
    "fetters_and_fruits": 4,
}

EPUB_CRITERIA = {
    "reading_order",
    "nested_toc",
    "source_badges",
    "cautions",
    "links",
    "vietnamese_diacritics",
    "no_overlap_or_loss",
    "no_color_only_meaning",
}

TOP_LEVEL_FIELDS = {
    "schema_version",
    "cohort_id",
    "attempt_id",
    "attempt_number",
    "delete_by",
    "reader_id",
    "consent_confirmed",
    "eligibility",
    "artifact",
    "session",
    "tasks",
    "epub_smoke",
}
ELIGIBILITY_FIELDS = {
    "vietnamese_comfort",
    "age_18_or_over",
    "meditation_sessions_lifetime",
    "retreats_completed",
    "knows_mahasi_vocabulary",
    "read_book_before",
    "participated_in_prior_book_pilot",
    "seen_tested_passages_before",
    "experienced_buddhist",
    "is_editor",
    "is_source_reviewer",
}
ARTIFACT_FIELDS = {"git_commit", "pdf_sha256", "epub_sha256", "pdf_pages"}
SESSION_FIELDS = {
    "primary_format",
    "moderator_is_editor",
    "started_at",
    "completed_at",
    "stopped_early",
    "stop_category",
    "stop_reason",
    "device",
    "reader_app",
    "reader_app_version",
    "text_scale_percent",
    "dark_mode",
}
TASK_FIELDS = {
    "outcome",
    "completed",
    "first_answer_recorded",
    "first_answer",
    "source_locator",
    "elapsed_seconds",
    "hint_used",
    "criteria",
    "notes",
}
EPUB_FIELDS = {
    "device",
    "reader_app",
    "reader_app_version",
    "text_scale_percent",
    "dark_mode",
    "repeated_tasks",
    "criteria",
    "notes",
}
REPEAT_FIELDS = {
    "outcome",
    "first_answer_recorded",
    "first_answer",
    "source_locator",
    "elapsed_seconds",
    "hint_used",
    "passed",
    "notes",
}

TARGET_COMPLETED = 5
MAX_STARTED_ATTEMPTS = 7
SELECTION_RULE = "first_five_completed_eligible"
STOP_CATEGORIES = {
    "none",
    "distress",
    "withdrawal",
    "technical",
    "ineligible_after_start",
    "moderator_abort",
}
TASK_OUTCOMES = {"answered", "skipped", "not_reached"}
STOP_REASON_CODES = {
    "none": "",
    "distress": "distress_stop",
    "withdrawal": "reader_withdrew",
    "technical": "technical_failure",
    "ineligible_after_start": "eligibility_rule_failed",
    "moderator_abort": "moderator_aborted",
}

CANONICAL_ORIGIN_URLS = {
    "https://github.com/streamentry/streamentry.git",
    "git@github.com:streamentry/streamentry.git",
    "ssh://git@github.com/streamentry/streamentry.git",
}
CANONICAL_REMOTE_REF = "refs/remotes/origin/main"

RECORD_SCHEMA_PATH = "book/references/beginner-pilot-record.schema.json"
MANIFEST_SCHEMA_PATH = (
    "book/references/beginner-pilot-cohort-manifest.schema.json"
)
CONTRACT_PATHS = (
    "book/references/beginner-validation-protocol.md",
    "book/references/beginner-reader-kit.md",
    RECORD_SCHEMA_PATH,
    MANIFEST_SCHEMA_PATH,
    "scripts/beginner_pilot_contract.py",
    "scripts/beginner_pilot_validation.py",
    "scripts/beginner_pilot_artifact.py",
    "scripts/beginner_pilot_manifest.py",
    "scripts/beginner_pilot.py",
    "scripts/score-beginner-pilot.py",
)
