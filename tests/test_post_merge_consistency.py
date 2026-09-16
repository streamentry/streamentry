"""Check targeted source/context regressions, not doctrinal truth or safety efficacy."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class PostMergeConsistencyTests(unittest.TestCase):
    def test_sleep_instruction_keeps_lying_down_context(self) -> None:
        text = read("book/chapters/06-trien-cai-giac-chi.typ")
        block = text.split('[P01 · Basic Exercise III,', 1)[1].split('])', 1)[0]
        self.assertIn("đã nằm xuống để ngủ", block)
        self.assertIn("có thể xua buồn ngủ", block)
        self.assertIn("không đổi thành lời dặn luôn ngồi chờ ngủ gật", block)

    def test_drowsiness_source_keeps_numbering_and_selected_scope(self) -> None:
        chapter = read("book/chapters/06-trien-cai-giac-chi.typ")
        sources = read("book/chapters/99-nguon.typ")
        entry = sources.split('[K54]', 1)[1].split('\n)', 1)[0]
        for marker in ("AN 7:58", "an7.61:2–9", "Moggallāna", "AN7_58.html"):
            self.assertIn(marker, entry)
        self.assertIn("diễn ý chọn lọc, không phải toàn bộ trình tự", chapter)
        self.assertIn("không buộc mình thử hết các cách", chapter)

    def test_warning_signs_stop_current_session(self) -> None:
        chapter = read("book/chapters/06-trien-cai-giac-chi.typ")
        readme = read("README.md")
        faq = read("book/appendices/c-faq.typ")
        for text in (chapter, readme, faq):
            self.assertRegex(
                text,
                r"dừng buổi hiện tại, không (?:tăng cường độ|tiếp tục thực hành cường độ cao)",
            )
        self.assertNotIn("hãy giảm hay dừng thực hành cường độ cao", chapter)

    def test_faq_separates_ordinary_restart_from_warning_signs(self) -> None:
        text = read("book/appendices/c-faq.typ")
        answer = text.split('"faq-thoi-luong",', 1)[1].split('#faq-card(', 1)[0]
        self.assertIn("bệnh thông thường đã hồi phục, không có dấu hiệu nguy cơ", answer)
        self.assertIn("#link(<khoi-dong-lai>)", answer)
        self.assertIn("Nếu đã dừng vì hoảng sợ lặp lại", answer)
        self.assertNotIn("Sau thời gian nghỉ vì sức khỏe, không tự động", answer)

    def test_english_noting_does_not_receive_pali_label(self) -> None:
        text = read("book/appendices/d-thuat-ngu.typ")
        term = text.split('#term-card([noting]', 1)[1].split('#v(8pt)', 1)[0]
        self.assertIn("từ tiếng Anh, không phải thuật ngữ Pāli", term)
        self.assertIn("term-label: [THUẬT NGỮ TIẾNG ANH]", term)
        self.assertIn("label: term-label", text)

    def test_download_gateway_bounds_what_the_artifact_checks_prove(self) -> None:
        # The tracked artifacts are now a fresh internal rebuild of the current
        # book, so the old "dist predates the source" wording no longer applies.
        # The guard now requires the README to name the exact checks that ran
        # and to keep the not-independently-validated boundary.
        text = read("README.md")
        section = text.split("## Đọc sách và phân biệt các phiên bản", 1)[1]
        section = section.split("## Nếu bạn mới bắt đầu", 1)[0]
        self.assertIn("dựng lại nội bộ từ `book/`", section)
        self.assertIn("kiểm tra định dạng đã ghim", section)
        self.assertIn("chưa phải bản được xác nhận độc lập", section)
        self.assertNotIn("đã vượt kiểm tra nội bộ", section)

    def test_new_claims_have_direct_sources_and_preserve_c93_urls(self) -> None:
        ledger = read("book/references/claim-ledger.md")
        rows = {line.split('|')[1].strip(): line for line in ledger.splitlines()
                if re.match(r'^\| C\d{2} \|', line)}
        self.assertIn("K54", rows["C94"])
        self.assertIn("/AN7_58.html", rows["C94"])
        self.assertIn("https://www.aimwell.org/practical.html", rows["C95"])
        self.assertIn("after lying down to sleep", rows["C95"])
        self.assertIn("congbaocdn.chinhphu.vn", rows["C93"])
        self.assertIn("xaydungchinhsach.chinhphu.vn", rows["C93"])
        self.assertIn("40179.htm", rows["C93"])


if __name__ == "__main__":
    unittest.main()
