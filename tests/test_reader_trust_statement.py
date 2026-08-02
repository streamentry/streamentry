from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = ROOT / "book" / "chapters" / "00-frontmatter.typ"


class ReaderTrustStatementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = FRONTMATTER.read_text(encoding="utf-8")

    def test_removed_trust_statement_is_not_in_frontmatter(self) -> None:
        for marker in (
            "<trach-nhiem-an-ban>",
            "Ai chịu trách nhiệm và điều gì chưa được xác lập?",
            "MINH BẠCH ẤN BẢN · BIÊN SOẠN",
            "Đọc giới hạn này trước khi dùng sách",
            "ChatGPT hỗ trợ cấu trúc",
            "không có giấy phép tái sử dụng",
        ):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.text)

    def test_frontmatter_keeps_the_reader_route(self) -> None:
        self.assertIn("<doc-ma-nguon>", self.text)
        self.assertIn("<buoi-dau>", self.text)


if __name__ == "__main__":
    unittest.main()
