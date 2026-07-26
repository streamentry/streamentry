from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
TESTS_DIR = ROOT / "tests"
for directory in (SCRIPTS_DIR, TESTS_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from release_common import ReleaseVerificationError  # noqa: E402
from release_evidence import (  # noqa: E402
    IMMUTABLE_SOURCE_SHA256,
    PUBLICATION_CREDIT,
    parse_release_evidence,
    validate_evidence_contract,
)
from release_verifier_fixtures import EVIDENCE  # noqa: E402


class ReleaseEvidenceParserTests(unittest.TestCase):
    def test_parses_exact_artifact_identity_rows(self) -> None:
        evidence = parse_release_evidence(EVIDENCE)
        self.assertEqual(evidence.pdf_pages, 123)
        self.assertEqual(evidence.pdf_size, 1_021_520)
        self.assertEqual(evidence.epub_content_entries, 136)
        self.assertEqual(evidence.epub_cover_entries, 1)
        self.assertEqual(evidence.epub_size, 137_543)

    def test_rejects_a_missing_required_row(self) -> None:
        with self.assertRaisesRegex(ReleaseVerificationError, "missing"):
            parse_release_evidence(
                EVIDENCE.replace("| PDF extent | 123 A5 pages |\n", "")
            )

    def test_rejects_a_duplicate_required_row(self) -> None:
        with self.assertRaisesRegex(ReleaseVerificationError, "duplicate"):
            parse_release_evidence(EVIDENCE + "| PDF extent | 123 A5 pages |\n")

    def test_rejects_malformed_navigation_counts(self) -> None:
        with self.assertRaisesRegex(ReleaseVerificationError, "navigation"):
            parse_release_evidence(
                EVIDENCE.replace(
                    "136 nested content entries plus 1 cover entry",
                    "137 entries",
                )
            )

    def test_rejects_an_artifact_table_hidden_in_an_html_comment(self) -> None:
        hidden = EVIDENCE.replace(
            "## Artifact identity\n\n",
            "## Artifact identity\n\n<!--\n",
        ) + "-->\n"
        with self.assertRaisesRegex(ReleaseVerificationError, "hidden"):
            parse_release_evidence(hidden)

    def test_rejects_preopened_or_html_hidden_evidence(self) -> None:
        wrappers = (
            ("<!--\n", ""),
            ("```markdown\n", ""),
            ("<div hidden>\n", "\n</div>"),
            ("<template>\n", "\n</template>"),
            ('<script type="text/plain">\n', "\n</script>"),
        )
        for prefix, suffix in wrappers:
            with self.subTest(prefix=prefix):
                with self.assertRaisesRegex(ReleaseVerificationError, "hidden"):
                    parse_release_evidence(prefix + EVIDENCE + suffix)

    def test_contract_anchors_the_immutable_source_hash(self) -> None:
        evidence = parse_release_evidence(EVIDENCE)
        anchored = replace(evidence, source_sha256=IMMUTABLE_SOURCE_SHA256)
        validate_evidence_contract(anchored)
        with self.assertRaisesRegex(ReleaseVerificationError, "source SHA-256"):
            validate_evidence_contract(replace(anchored, source_sha256="0" * 64))

    def test_contract_anchors_the_canonical_publication_credit(self) -> None:
        evidence = parse_release_evidence(EVIDENCE)
        anchored = replace(
            evidence,
            source_sha256=IMMUTABLE_SOURCE_SHA256,
            publication_credit=PUBLICATION_CREDIT,
        )
        validate_evidence_contract(anchored)
        with self.assertRaisesRegex(ReleaseVerificationError, "publication credit"):
            validate_evidence_contract(
                replace(anchored, publication_credit="Different author")
            )


if __name__ == "__main__":
    unittest.main()
