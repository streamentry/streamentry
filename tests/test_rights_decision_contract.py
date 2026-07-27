from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from release_common import ReleaseVerificationError  # noqa: E402
from rights_decision_contract import validate_rights_decision  # noqa: E402
from tests.rights_decision_fixtures import rights_decision_lines  # noqa: E402


SOURCE_SHA256 = "a" * 64


def _decision(status: str, overrides: dict[str, str] | None = None) -> str:
    return "\n".join(
        rights_decision_lines(
            ROOT,
            SOURCE_SHA256,
            status=status,
            overrides=overrides,
        )
    )


class RightsDecisionContractTests(unittest.TestCase):
    def test_accepts_complete_terminal_decisions(self) -> None:
        for status in ("passed", "failed"):
            with self.subTest(status=status):
                validate_rights_decision(
                    ROOT,
                    _decision(status),
                    status,
                    SOURCE_SHA256,
                )

    def test_rejects_stale_inventory_or_source_binding(self) -> None:
        cases = (
            (
                {"Rights materials inventory SHA-256": "0" * 64},
                "materials inventory SHA-256 is stale",
            ),
            (
                {"Immutable manuscript SHA-256": "0" * 64},
                "immutable manuscript SHA-256 is stale",
            ),
        )
        for overrides, expected_error in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(
                    ReleaseVerificationError,
                    expected_error,
                ):
                    validate_rights_decision(
                        ROOT,
                        _decision("passed", overrides),
                        "passed",
                        SOURCE_SHA256,
                    )

    def test_rejects_each_contradictory_terminal_decision(self) -> None:
        cases = (
            (
                "passed",
                {"PDF distribution scope": "NOT_AUTHORIZED"},
                "authorize both PDF and EPUB",
            ),
            (
                "passed",
                {"EPUB distribution scope": "NOT_AUTHORIZED"},
                "authorize both PDF and EPUB",
            ),
            (
                "passed",
                {"Contributor chain status": "UNRESOLVED"},
                "resolve the contributor chain",
            ),
            (
                "passed",
                {"Third-party materials status": "UNRESOLVED"},
                "resolve third-party materials",
            ),
            (
                "passed",
                {"Unresolved rights items": "P01 permission remains open"},
                "cannot retain unresolved rights items",
            ),
            (
                "passed",
                {"Overall rights decision": "AUTHORITY_NOT_ESTABLISHED"},
                "must record an APPROVE decision",
            ),
            (
                "failed",
                {"Overall rights decision": "APPROVE"},
                "must decline or leave authority unestablished",
            ),
        )
        for status, overrides, expected_error in cases:
            with self.subTest(status=status, overrides=overrides):
                with self.assertRaisesRegex(
                    ReleaseVerificationError,
                    expected_error,
                ):
                    validate_rights_decision(
                        ROOT,
                        _decision(status, overrides),
                        status,
                        SOURCE_SHA256,
                    )


if __name__ == "__main__":
    unittest.main()
