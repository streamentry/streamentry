from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from edition_contract import EDITION  # noqa: E402
from release_common import ReleaseVerificationError  # noqa: E402
from release_epub import EpubFacts  # noqa: E402
from release_pdf import PdfFacts  # noqa: E402
from verify_release import validate_release_identity  # noqa: E402


PDF = PdfFacts(
    title=EDITION.title,
    author=EDITION.author,
    tagged=True,
    suspects=False,
    javascript=False,
    encrypted=False,
    pages=1,
    file_size=1,
    page_facts=(),
)
EPUB = EpubFacts(
    title=EDITION.title,
    author=EDITION.author,
    language=EDITION.language,
    content_entries=1,
    cover_entries=1,
)


class ReleaseIdentityTests(unittest.TestCase):
    def test_accepts_identity_derived_from_the_canonical_contract(self) -> None:
        validate_release_identity(PDF, EPUB, EDITION)

    def test_rejects_each_cross_format_identity_mismatch(self) -> None:
        cases = (
            (replace(PDF, title="Wrong"), EPUB, "PDF title"),
            (replace(PDF, author="Wrong"), EPUB, "PDF author"),
            (PDF, replace(EPUB, title="Wrong"), "EPUB title"),
            (PDF, replace(EPUB, author="Wrong"), "EPUB creator"),
            (PDF, replace(EPUB, language="en"), "EPUB language"),
        )
        for pdf, epub, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ReleaseVerificationError, message):
                    validate_release_identity(pdf, epub, EDITION)


if __name__ == "__main__":
    unittest.main()
