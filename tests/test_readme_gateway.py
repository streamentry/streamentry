from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
EDITION_PATH = ROOT / "book" / "edition.json"
GATES_PATH = ROOT / "book" / "references" / "external-release-gates.json"
EVIDENCE_PATH = ROOT / "book" / "references" / "release-evidence.md"


class ReadmeGatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.edition = json.loads(EDITION_PATH.read_text(encoding="utf-8"))
        cls.gates = json.loads(GATES_PATH.read_text(encoding="utf-8"))
        cls.evidence = EVIDENCE_PATH.read_text(encoding="utf-8")
        cls.reader_section, cls.contributor_section = cls.readme.split(
            "## Dành cho người biên tập và kiểm định",
            maxsplit=1,
        )

    def test_reader_gateway_precedes_contributor_details(self) -> None:
        metadata = self.edition["metadata"]
        stem = self.edition["publication"]["file_stem"]

        self.assertTrue(self.readme.startswith(f"# {metadata['title']}\n"))
        self.assertIn(metadata["author"], self.reader_section)
        self.assertIn(f"](dist/{stem}.pdf)", self.reader_section)
        self.assertIn(f"](dist/{stem}.epub)", self.reader_section)
        self.assertIn("## Nếu bạn mới bắt đầu", self.reader_section)
        self.assertIn("## An toàn và phạm vi", self.reader_section)

    def test_every_relative_markdown_link_resolves(self) -> None:
        targets = re.findall(r"\]\(([^)]+)\)", self.readme)
        relative_targets = (
            target
            for target in targets
            if not target.startswith(("http://", "https://", "#"))
        )

        missing = [
            target
            for target in relative_targets
            if not (ROOT / target).exists()
        ]
        self.assertEqual(missing, [])

    def test_rights_and_external_status_are_not_overclaimed(self) -> None:
        open_gates = [
            name
            for name, gate in self.gates["gates"].items()
            if gate["status"] == "open"
        ]
        numbered_gates = re.findall(
            r"^\d+\. ",
            self.contributor_section.split("### Hợp đồng edition", maxsplit=1)[0],
            flags=re.MULTILINE,
        )

        self.assertIn("Việc tệp có thể tải xuống không tự tạo quyền", self.reader_section)
        self.assertIn("chưa phải bản được xác nhận độc lập", self.reader_section)
        self.assertEqual(len(open_gates), 6)
        self.assertEqual(len(numbered_gates), len(open_gates))

    def test_drift_prone_artifact_counts_stay_in_release_evidence(self) -> None:
        pdf_pages = re.search(r"\| PDF extent \| (\d+) A5 pages \|", self.evidence)
        epub_entries = re.search(
            r"\| EPUB navigation \| (\d+) nested content entries",
            self.evidence,
        )
        self.assertIsNotNone(pdf_pages)
        self.assertIsNotNone(epub_entries)
        self.assertNotIn(f"{pdf_pages.group(1)} trang", self.readme)
        self.assertNotIn(f"{epub_entries.group(1)} mục", self.readme)


if __name__ == "__main__":
    unittest.main()
