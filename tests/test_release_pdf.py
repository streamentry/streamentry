from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
TESTS_DIR = ROOT / "tests"
for directory in (SCRIPTS_DIR, TESTS_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from release_common import ReleaseVerificationError  # noqa: E402
from release_pdf import parse_pdfinfo, validate_pdf_contract  # noqa: E402
from release_verifier_fixtures import PDFINFO  # noqa: E402


class ReleasePdfTests(unittest.TestCase):
    def test_parses_pdfinfo_security_and_geometry_fields(self) -> None:
        facts = parse_pdfinfo(PDFINFO)
        self.assertTrue(facts.tagged)
        self.assertFalse(facts.suspects)
        self.assertFalse(facts.javascript)
        self.assertEqual(facts.pages, 123)
        self.assertEqual(facts.file_size, 1_021_520)

    def test_rejects_pdfinfo_with_a_missing_security_field(self) -> None:
        with self.assertRaisesRegex(ReleaseVerificationError, "missing fields"):
            parse_pdfinfo(PDFINFO.replace("JavaScript:      no\n", ""))

    def test_rejects_an_encrypted_pdf_contract(self) -> None:
        one_page = PDFINFO.replace("Pages:           123", "Pages:           1")
        facts = parse_pdfinfo(
            one_page.replace("Encrypted:       no", "Encrypted:       yes")
        )
        with self.assertRaisesRegex(ReleaseVerificationError, "encrypted"):
            validate_pdf_contract(facts)

    def test_rejects_a_rotated_pdf_page(self) -> None:
        one_page = PDFINFO.replace("Pages:           123", "Pages:           1")
        facts = parse_pdfinfo(
            one_page.replace("Page rot:        0", "Page rot:        90")
        )
        with self.assertRaisesRegex(ReleaseVerificationError, "page 1"):
            validate_pdf_contract(facts)

    def test_rejects_a_mixed_size_pdf(self) -> None:
        two_pages = PDFINFO.replace("Pages:           123", "Pages:           2")
        page_details = """\
Page    1 size:  419.528 x 595.276 pts
Page    1 rot:   0
Page    2 size:  612 x 792 pts
Page    2 rot:   0
"""
        facts = parse_pdfinfo(two_pages, page_details)
        with self.assertRaisesRegex(ReleaseVerificationError, "page 2"):
            validate_pdf_contract(facts)


if __name__ == "__main__":
    unittest.main()
