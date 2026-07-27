from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from release_common import ReleaseVerificationError  # noqa: E402
from rights_inventory_contract import (  # noqa: E402
    parse_rights_inventory,
    validate_rights_inventory,
)


SOURCE_SHA256 = "a" * 64
PDF_SHA256 = "b" * 64
EPUB_SHA256 = "c" * 64


def _inventory(
    *,
    schema: str = "1",
    source_sha256: str = SOURCE_SHA256,
    pdf_sha256: str = PDF_SHA256,
    epub_sha256: str = EPUB_SHA256,
) -> str:
    return "\n".join(
        (
            f"Rights materials inventory schema: {schema}",
            f"Immutable manuscript SHA-256: `{source_sha256}`",
            f"Candidate PDF SHA-256: `{pdf_sha256}`",
            f"Candidate EPUB SHA-256: `{epub_sha256}`",
        )
    )


class RightsInventoryContractTests(unittest.TestCase):
    def test_accepts_one_exact_release_identity(self) -> None:
        identity = validate_rights_inventory(
            _inventory(),
            source_sha256=SOURCE_SHA256,
            pdf_sha256=PDF_SHA256,
            epub_sha256=EPUB_SHA256,
        )
        self.assertEqual(identity.schema, 1)
        self.assertEqual(identity.source_sha256, SOURCE_SHA256)
        self.assertEqual(identity.pdf_sha256, PDF_SHA256)
        self.assertEqual(identity.epub_sha256, EPUB_SHA256)

    def test_rejects_unsupported_schema(self) -> None:
        with self.assertRaisesRegex(
            ReleaseVerificationError,
            "schema must be 1",
        ):
            parse_rights_inventory(_inventory(schema="2"))

    def test_rejects_stale_source_pdf_or_epub_identity(self) -> None:
        defects = {
            "immutable manuscript": {"source_sha256": "d" * 64},
            "candidate PDF": {"pdf_sha256": "d" * 64},
            "candidate EPUB": {"epub_sha256": "d" * 64},
        }
        for message, replacements in defects.items():
            with self.subTest(message=message):
                with self.assertRaisesRegex(ReleaseVerificationError, message):
                    validate_rights_inventory(
                        _inventory(**replacements),
                        source_sha256=SOURCE_SHA256,
                        pdf_sha256=PDF_SHA256,
                        epub_sha256=EPUB_SHA256,
                    )

    def test_rejects_duplicate_or_malformed_identity_fields(self) -> None:
        defects = {
            "exactly one Candidate PDF": (
                _inventory() + f"\nCandidate PDF SHA-256: `{PDF_SHA256}`"
            ),
            "one lowercase SHA-256": _inventory(epub_sha256="NOT-A-HASH"),
        }
        for message, markdown in defects.items():
            with self.subTest(message=message):
                with self.assertRaisesRegex(ReleaseVerificationError, message):
                    parse_rights_inventory(markdown)


if __name__ == "__main__":
    unittest.main()
