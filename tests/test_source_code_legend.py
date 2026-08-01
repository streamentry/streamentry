from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = ROOT / "book" / "chapters" / "00-frontmatter.typ"
SAFETY_CHAPTER = ROOT / "book" / "chapters" / "09-an-toan.typ"
SOURCE_MAP = ROOT / "book" / "chapters" / "99-nguon.typ"


class SourceCodeLegendTests(unittest.TestCase):
    def test_frontmatter_expands_collection_abbreviations_at_first_read(self) -> None:
        text = FRONTMATTER.read_text(encoding="utf-8")
        for marker in (
            "*DN* là *Dīgha Nikāya*, Trường Bộ",
            "*MN* là *Majjhima Nikāya*, Trung Bộ",
            "*SN* là *Saṃyutta Nikāya*, Tương Ưng Bộ",
            "*AN* là *Aṅguttara Nikāya*, Tăng Chi Bộ",
            "*Ud* là *Udāna*",
        ):
            self.assertIn(marker, text)
        self.assertIn("<doc-ma-nguon>", text)

    def test_internal_codes_are_not_presented_as_canonical_numbering(self) -> None:
        text = FRONTMATTER.read_text(encoding="utf-8")
        self.assertIn("K01 không có nghĩa “kinh số 1”", text)
        self.assertIn("*P01* và *P02*", text)
        self.assertIn("*V01*", text)
        self.assertIn("*R01, R02…*", text)
        self.assertIn("#link(<ma-nguon-chi-tiet>)", text)

    def test_source_map_repeats_the_durable_lookup_contract(self) -> None:
        text = SOURCE_MAP.read_text(encoding="utf-8")
        self.assertIn("<ma-nguon-chi-tiet>", text)
        self.assertIn("*K01–K43*", text)
        self.assertIn("*P01–P02*", text)
        self.assertIn("*R01–R11*", text)
        self.assertIn("không phải số phân loại truyền thống", text)

    def test_health_agency_abbreviations_are_expanded_at_first_use(self) -> None:
        text = SAFETY_CHAPTER.read_text(encoding="utf-8")
        first_source_summary = text.index(
            "Quy trình ấy là khung biên soạn thận trọng"
        )
        first_detailed_source = text.index(
            '#source-line("Y TẾ & NGHIÊN CỨU", [R05]'
        )
        legend = text[first_source_summary:first_detailed_source]
        for marker in (
            "*WHO* là _World Health Organization_",
            "*NIMH* là _National Institute of Mental Health_",
            "*NHS* là _National Health Service_",
            "*CDC* là _Centers for Disease Control and Prevention_",
        ):
            self.assertIn(marker, legend)
        self.assertIn("A&E (_Accident and Emergency_)", text)

    def test_other_first_read_abbreviations_are_expanded(self) -> None:
        frontmatter = FRONTMATTER.read_text(encoding="utf-8")
        source_map = SOURCE_MAP.read_text(encoding="utf-8")
        self.assertIn("trí tuệ nhân tạo (AI)", frontmatter)
        self.assertIn("hồ sơ hiện không xác lập hai chữ *CS*", frontmatter)
        self.assertIn("EPUB là sách điện tử tự dàn", frontmatter)
        self.assertIn("Buddhist Publication Society (BPS)", source_map)


if __name__ == "__main__":
    unittest.main()
