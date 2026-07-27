from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "EDITORIAL_POLICY.md"
ISSUE_FORM_PATH = ROOT / ".github" / "ISSUE_TEMPLATE" / "correction.yml"
README_PATH = ROOT / "README.md"
SOURCE_CHAPTER_PATH = ROOT / "book" / "chapters" / "99-nguon.typ"
AUDIT_PATH = ROOT / "book" / "references" / "publish-readiness-audit.md"

POLICY_URL = (
    "https://github.com/streamentry/streamentry/blob/main/EDITORIAL_POLICY.md"
)
CORRECTION_URL = (
    "https://github.com/streamentry/streamentry/issues/new?"
    "template=correction.yml"
)


class EditorialPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = POLICY_PATH.read_text(encoding="utf-8")
        cls.issue_form = ISSUE_FORM_PATH.read_text(encoding="utf-8")
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.source_chapter = SOURCE_CHAPTER_PATH.read_text(encoding="utf-8")
        cls.audit = AUDIT_PATH.read_text(encoding="utf-8")

    def test_reader_surfaces_link_the_policy_and_correction_form(self) -> None:
        self.assertIn(
            "[Chính sách biên tập và sửa sai](EDITORIAL_POLICY.md)",
            self.readme,
        )
        self.assertIn(CORRECTION_URL, self.readme)
        self.assertIn(POLICY_URL, self.source_chapter)
        self.assertIn(CORRECTION_URL, self.source_chapter)

    def test_policy_exposes_required_boundaries(self) -> None:
        headings = {
            "## Ai chịu trách nhiệm cho ấn bản",
            "## Cách một mệnh đề được đưa vào sách",
            "## An toàn và giới hạn y khoa",
            "## Minh bạch về AI",
            "## Cách báo một lỗi",
            "## Quy trình xử lý và lưu dấu",
            "## Quyền, lợi ích thương mại và ghi công",
            "## Bằng chứng còn thiếu",
        }
        for heading in headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, self.policy)

        self.assertIn("không có thời hạn phản hồi cố định", self.policy)
        self.assertIn("không phải thẩm quyền tôn giáo", self.policy)
        self.assertIn("Kho hiện không có giấy phép công khai", self.policy)
        self.assertIn("không chứng minh sách là lựa chọn số một", self.policy)

    def test_policy_relative_links_resolve_and_external_links_are_https(self) -> None:
        targets = re.findall(r"\]\(([^)]+)\)", self.policy)
        relative = [
            target
            for target in targets
            if not target.startswith(("https://", "#"))
        ]
        self.assertEqual(
            [target for target in relative if not (ROOT / target).is_file()],
            [],
        )
        self.assertFalse(any(target.startswith("http://") for target in targets))

    def test_issue_form_collects_actionable_data_without_contact_fields(self) -> None:
        self.assertTrue(self.issue_form.startswith("name: Báo lỗi sách hoặc nguồn\n"))
        for field_id in (
            "category",
            "format",
            "location",
            "current_text",
            "concern",
            "evidence",
            "public_report",
        ):
            with self.subTest(field_id=field_id):
                self.assertEqual(self.issue_form.count(f"id: {field_id}\n"), 1)

        self.assertNotIn("id: contact", self.issue_form)
        self.assertIn("Issue này sẽ công khai", self.issue_form)
        self.assertIn("thông tin y tế riêng", self.issue_form)
        self.assertIn("required: true", self.issue_form)

    def test_audit_improves_policy_without_inventing_accountability(self) -> None:
        self.assertRegex(
            self.audit,
            r"\| T02 \| Partial \| .*không có thời hạn phản hồi cố định",
        )
        self.assertRegex(
            self.audit,
            r"\| T05 \| Pass \| .*`EDITORIAL_POLICY\.md`",
        )


if __name__ == "__main__":
    unittest.main()
