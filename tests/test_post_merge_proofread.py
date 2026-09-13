"""Guard reader-facing corrections without certifying doctrine or clinical safety."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAQ_PATH = "book/appendices/c-faq.typ"
SAFETY_PATH = "book/chapters/09-an-toan.typ"


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def faq_blocks() -> dict[str, str]:
    blocks = read(FAQ_PATH).split("#faq-card(")[1:]
    return {re.search(r'^\s*"([^"]+)"', block).group(1): block for block in blocks}


class PostMergeProofreadTests(unittest.TestCase):
    def test_warning_passages_require_stopping_current_session(self) -> None:
        passages = {
            "introduction": read("book/chapters/00-frontmatter.typ").split(
                "== Khi cần tìm lại bước kế tiếp", 1
            )[1],
            "method": read("book/chapters/05-phuong-phap-mahasi.typ").split(
                "[Khi cần hướng dẫn riêng trước khi tăng cường độ]", 1
            )[1].split("== Gấp sách lại", 1)[0],
        }
        for name, passage in passages.items():
            with self.subTest(passage=name):
                self.assertIn("dừng buổi hiện tại", passage)
                self.assertIn("không tiếp tục thực hành cường độ cao", passage)
                self.assertIn("hỗ trợ", passage)
                self.assertNotIn("giảm hay dừng", passage)
                self.assertNotIn("giảm hoặc dừng", passage)

    def test_yellow_summary_heading_and_action_agree(self) -> None:
        text = read(SAFETY_PATH)
        self.assertIn("*vàng* là dừng buổi hiện tại và tìm hỗ trợ sớm", text)
        self.assertIn(
            "=== Mức vàng: dừng buổi hiện tại, tìm hỗ trợ sớm <muc-vang>", text
        )
        yellow = text.split("=== Mức vàng:", 1)[1].split("=== Mức đỏ:", 1)[0]
        self.assertIn("Hãy dừng buổi hiện tại", yellow)
        self.assertIn("không tiếp tục thực hành cường độ cao", yellow)
        self.assertIn("không lắng", yellow)
        self.assertIn("giảm rõ", yellow)

    def test_emergency_links_go_directly_to_red_level(self) -> None:
        text = read(SAFETY_PATH)
        self.assertIn("=== Mức đỏ: xử lý như tình huống cấp cứu <muc-do>", text)
        self.assertEqual(text.count("#link(<muc-do>)[mức đỏ]"), 2)
        self.assertNotIn("#link(<ba-muc>)[mức ba]", text)
        self.assertNotIn("#link(<ba-muc>)[mức đỏ]", text)
        self.assertIn("#link(<muc-do>)[trợ giúp khẩn cấp]", faq_blocks()["faq-bat-an"])

    def test_all_thirteen_faq_anchors_remain(self) -> None:
        expected = [
            "faq-bao-dam", "faq-phong-xep", "faq-ghi-nhan", "faq-chi-quan",
            "faq-muoi-sau-tue", "faq-tam-tat", "faq-cam-giac-toi", "faq-dau",
            "faq-bat-an", "faq-doi-song", "faq-thoi-luong", "faq-nguoi-thay",
            "faq-kiet-su",
        ]
        self.assertEqual(list(faq_blocks()), expected)
        self.assertEqual(read(FAQ_PATH).count("#source-badge("), 14)

    def test_faq_source_badges_precede_their_prose(self) -> None:
        for anchor, block in faq_blocks().items():
            with self.subTest(anchor=anchor):
                self.assertRegex(
                    block,
                    r'^\s*"[^"]+",\s*\[[^\n]+\],\s*\[\s*#source-badge\(',
                )
                for match in re.finditer(r"#source-badge\([^\n]+\)", block):
                    following = block[match.end():]
                    self.assertRegex(following, r"^\s*#v\(5pt\)\s+\S")
                    self.assertNotRegex(following, r"^\s*(?:#v\(5pt\)\s*)?\],")

    def test_faq_keeps_research_separate_from_meditation_advice(self) -> None:
        block = faq_blocks()["faq-bat-an"]
        research, editorial = block.split('#source-badge("BIÊN SOẠN"', 1)
        self.assertIn('refs: [R01; R02]', research)
        self.assertNotIn("dừng buổi hiện tại", research)
        self.assertIn("hướng dẫn dừng thiền là phần biên soạn", editorial)
        self.assertIn("Không cần chờ buổi gặp người hướng dẫn", editorial)



if __name__ == "__main__":
    unittest.main()
