from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = ROOT / "book" / "chapters" / "00-frontmatter.typ"


class ReaderTrustStatementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = FRONTMATTER.read_text(encoding="utf-8")

    def test_frontmatter_discloses_unverified_human_credentials_and_ai_scope(self) -> None:
        self.assertIn("<trach-nhiem-an-ban>", self.text)
        self.assertIn(
            "chưa công bố tiểu sử, bằng cấp hay sự chuẩn nhận giảng dạy",
            self.text,
        )
        self.assertIn("ChatGPT hỗ trợ cấu trúc", self.text)
        self.assertIn("không có kinh nghiệm hành thiền", self.text)
        self.assertIn("không phải bác sĩ", self.text)

    def test_frontmatter_names_open_external_evidence_without_overclaiming(self) -> None:
        for boundary in (
            "chưa có quyết định quyền tái phân phối đủ thẩm quyền",
            "phản biện Theravāda độc lập",
            "phản biện an toàn lâm sàng",
            "nhóm thử nghiệm năm người mới",
            "thử EPUB bằng người thật",
            "chưa phải ấn bản được xác nhận độc lập",
        ):
            self.assertIn(boundary, self.text)

    def test_frontmatter_exposes_rights_and_correction_routes(self) -> None:
        self.assertIn("không có giấy phép tái sử dụng", self.text)
        self.assertIn("không tự cấp quyền sao chép", self.text)
        self.assertIn("EDITORIAL_POLICY.md", self.text)
        self.assertIn("correction.yml", self.text)


if __name__ == "__main__":
    unittest.main()
