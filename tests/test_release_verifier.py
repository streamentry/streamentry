from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from verify_release import verify_release  # noqa: E402


class CurrentReleaseIntegrationTests(unittest.TestCase):
    def test_current_release_evidence_matches_dist_artifacts(self) -> None:
        evidence = verify_release(ROOT)
        self.assertEqual(evidence.pdf_pages, 126)
        self.assertEqual(evidence.epub_cover_entries, 1)


if __name__ == "__main__":
    unittest.main()
