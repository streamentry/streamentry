from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "book" / "chapters" / "10-nhap-luu.typ"


class Chapter10ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chapter = CHAPTER_PATH.read_text(encoding="utf-8")

    def test_who_can_attain_section_uses_all_four_canonical_examples(self) -> None:
        section = self.chapter.split(
            "== Ai có thể đạt Nhập lưu theo lời kinh?",
            maxsplit=1,
        )[1].split("== Đi về phía dòng", maxsplit=1)[0]
        for expected in (
            "*Tỳ-kheo:*",
            "*Nam cư sĩ:*",
            "*Nữ cư sĩ:*",
            "*Tỳ-kheo-ni:*",
            "Sujātā",
            "Nandā",
            "K08 · DN 16, đoạn Ñātika và lời dạy cuối",
        ):
            self.assertIn(expected, section)

    def test_who_can_attain_section_keeps_possibility_bounded(self) -> None:
        required_boundaries = (
            "đời sống tại gia và giới tính nữ không tự loại trừ",
            "mọi người chắc chắn sẽ chứng trong đời này",
            "không cung cấp thống kê hiện đại",
            "KHẢ NĂNG KHÔNG PHẢI BẢO ĐẢM",
        )
        for boundary in required_boundaries:
            self.assertIn(boundary, self.chapter)


if __name__ == "__main__":
    unittest.main()
