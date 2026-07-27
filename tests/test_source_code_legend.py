from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = ROOT / "book" / "chapters" / "00-frontmatter.typ"
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
        self.assertIn("*K01–K40*", text)
        self.assertIn("*P01–P02*", text)
        self.assertIn("*R01–R11*", text)
        self.assertIn("không phải số phân loại truyền thống", text)


if __name__ == "__main__":
    unittest.main()
