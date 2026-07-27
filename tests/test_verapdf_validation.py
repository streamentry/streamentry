from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from release_common import ReleaseVerificationError  # noqa: E402
from verapdf_validation import (  # noqa: E402
    VERAPDF_INSTALLER_SHA256,
    VERAPDF_INSTALLER_URL,
    VERAPDF_PROFILE,
    VERAPDF_VERSION,
    parse_verapdf_report,
)


def _valid_report(pdf_path: Path) -> dict[str, object]:
    return {
        "report": {
            "buildInformation": {
                "releaseDetails": [
                    {"id": "core", "version": VERAPDF_VERSION},
                    {"id": "validation-model", "version": VERAPDF_VERSION},
                    {"id": "apps", "version": VERAPDF_VERSION},
                ]
            },
            "jobs": [
                {
                    "itemDetails": {
                        "name": str(pdf_path.resolve()),
                        "size": pdf_path.stat().st_size,
                    },
                    "validationResult": [
                        {
                            "details": {
                                "passedRules": 106,
                                "failedRules": 0,
                                "passedChecks": 807_375,
                                "failedChecks": 0,
                                "ruleSummaries": [],
                            },
                            "jobEndStatus": "normal",
                            "profileName": VERAPDF_PROFILE,
                            "compliant": True,
                        }
                    ],
                }
            ],
            "batchSummary": {
                "totalJobs": 1,
                "outOfMemory": 0,
                "veraExceptions": 0,
                "failedEncryptedJobs": 0,
                "failedParsingJobs": 0,
                "validationSummary": {
                    "failedJobCount": 0,
                    "totalJobCount": 1,
                    "compliantPdfaCount": 1,
                    "nonCompliantPdfaCount": 0,
                    "successfulJobCount": 1,
                },
            },
        }
    }


class VeraPdfValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.pdf_path = Path(self.temporary_directory.name) / "candidate.pdf"
        self.pdf_path.write_bytes(b"%PDF-synthetic")
        self.report = _valid_report(self.pdf_path)

    def test_accepts_one_complete_pinned_pdfua1_report(self) -> None:
        facts = parse_verapdf_report(self.report, self.pdf_path)
        self.assertEqual(facts.version, VERAPDF_VERSION)
        self.assertEqual(facts.profile, VERAPDF_PROFILE)
        self.assertEqual(facts.passed_rules, 106)
        self.assertEqual(facts.passed_checks, 807_375)

    def test_ci_contract_pins_one_cli_only_installer(self) -> None:
        template = ROOT / "ci" / "verapdf-auto-install.xml"
        root = ET.fromstring(template.read_text(encoding="utf-8"))
        install_path = root.find(".//installpath")
        self.assertIsNotNone(install_path)
        assert install_path is not None
        self.assertEqual(install_path.text, "@INSTALL_PATH@")

        packs = root.findall(".//pack")
        self.assertEqual(len(packs), 5)
        self.assertEqual(
            [
                (
                    pack.attrib["index"],
                    pack.attrib["name"],
                    pack.attrib["selected"],
                )
                for pack in packs
            ],
            [
                ("0", "veraPDF GUI", "false"),
                ("1", "veraPDF Mac and *nix Scripts", "true"),
                ("2", "veraPDF Validation model", "false"),
                ("3", "veraPDF Documentation", "false"),
                ("4", "veraPDF Sample Plugins", "false"),
            ],
        )
        self.assertEqual(
            VERAPDF_INSTALLER_URL,
            "https://software.verapdf.org/releases/1.30/"
            f"verapdf-greenfield-{VERAPDF_VERSION}-installer.zip",
        )
        self.assertRegex(VERAPDF_INSTALLER_SHA256, r"\A[0-9a-f]{64}\Z")

    def test_rejects_noncompliance_profile_drift_and_failed_checks(self) -> None:
        defects = {
            "not PDF/UA-1 compliant": (
                ("report", "jobs", 0, "validationResult", 0, "compliant"),
                False,
            ),
            "PDF/UA-1 validation profile": (
                ("report", "jobs", 0, "validationResult", 0, "profileName"),
                "PDF/A-1b validation profile",
            ),
            "failed PDF/UA-1 checks": (
                (
                    "report",
                    "jobs",
                    0,
                    "validationResult",
                    0,
                    "details",
                    "failedChecks",
                ),
                1,
            ),
        }
        for message, (path, value) in defects.items():
            with self.subTest(message=message):
                report = copy.deepcopy(self.report)
                target: object = report
                for key in path[:-1]:
                    target = target[key]  # type: ignore[index]
                target[path[-1]] = value  # type: ignore[index]
                with self.assertRaisesRegex(ReleaseVerificationError, message):
                    parse_verapdf_report(report, self.pdf_path)

    def test_rejects_version_artifact_and_batch_drift(self) -> None:
        defects = {
            "version": (
                ("report", "buildInformation", "releaseDetails", 0, "version"),
                "1.30.1",
            ),
            "different PDF": (
                ("report", "jobs", 0, "itemDetails", "name"),
                str(self.pdf_path.with_name("other.pdf")),
            ),
            "failedParsingJobs": (
                ("report", "batchSummary", "failedParsingJobs"),
                1,
            ),
        }
        for message, (path, value) in defects.items():
            with self.subTest(message=message):
                report = copy.deepcopy(self.report)
                target: object = report
                for key in path[:-1]:
                    target = target[key]  # type: ignore[index]
                target[path[-1]] = value  # type: ignore[index]
                with self.assertRaisesRegex(ReleaseVerificationError, message):
                    parse_verapdf_report(report, self.pdf_path)


if __name__ == "__main__":
    unittest.main()
