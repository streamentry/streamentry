from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "book" / "chapters" / "12-ban-do-tue.typ"


class Chapter12ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chapter = CHAPTER_PATH.read_text(encoding="utf-8")

    def _stage(self, number: int) -> str:
        start = re.search(rf"^==== {number}\. ", self.chapter, re.MULTILINE)
        self.assertIsNotNone(start, f"missing heading for stage {number}")
        end = re.search(
            r"^==== \d+\. |^== ",
            self.chapter[start.end() :],
            re.MULTILINE,
        )
        stop = start.end() + end.start() if end else len(self.chapter)
        return self.chapter[start.start() : stop]

    def test_all_seventeen_stage_names_are_navigable_headings(self) -> None:
        headings = re.findall(r"^==== (\d+)\. ", self.chapter, re.MULTILINE)
        self.assertEqual(headings, [str(number) for number in range(1, 18)])

    def test_stages_one_to_eleven_keep_the_beginner_explanation_contract(
        self,
    ) -> None:
        required_labels = (
            "*Cách biết đổi.*",
            "*Nền trước và khi nào tên này có cơ sở.*",
            "*Trải nghiệm có thể như thế nào.*",
            "*Cách vun điều kiện và tiếp tục hành.*",
            "*Điều chưa đủ để kết luận.*",
        )
        for number in range(1, 12):
            with self.subTest(stage=number):
                stage = self._stage(number)
                for label in required_labels:
                    self.assertIn(label, stage)
                self.assertIn("*Vì sao bản đồ chuyển tiếp", stage)

    def test_one_object_walkthrough_covers_stages_one_to_eleven(self) -> None:
        section = self.chapter.split(
            "== Cùng một cơn đau được biết khác nhau qua mười một tuệ",
            maxsplit=1,
        )[1].split("== Tóm tắt đường đi", maxsplit=1)[0]
        for number in range(1, 12):
            self.assertRegex(section, rf"(?m)^\+ \*{number} · ")
        self.assertIn("C69 · minh họa đối chiếu P02 mục 1–11", section)

    def test_late_sequence_retains_source_and_non_diagnostic_boundaries(
        self,
    ) -> None:
        for number in range(12, 18):
            stage = self._stage(number)
            self.assertIn("*Tên này đang chỉ gì.*", stage)
        self.assertIn("P02 · mục 12–17; chú thích 40–45", self.chapter)
        self.assertIn("V01 · XXI.128–131; XXII.1–21", self.chapter)
        self.assertIn(
            "không thể trung thực biến chúng thành năm cảm giác",
            self.chapter,
        )


if __name__ == "__main__":
    unittest.main()
