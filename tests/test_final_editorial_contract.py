"""Regression checks for the final editorial corrections, not doctrinal certification."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class FinalEditorialContract(unittest.TestCase):
    def test_retreat_warning_does_not_require_an_attainment_guarantee(self):
        text = read("book/chapters/08-lo-trinh-thay-khoa-thien.typ")
        self.assertNotIn("quyền rời khóa hoặc bảo đảm đạo quả", text)
        self.assertIn("Khóa thiền hứa bảo đảm đạo quả", text)
        self.assertIn("*Khóa thiền hứa bảo đảm đạo quả:* cũng chưa đăng ký", text)

    def test_emergency_route_precedes_grounding(self):
        text = read("book/chapters/09-an-toan.typ")
        self.assertLess(text.index('label("cap-cuu-ngay")'), text.index("[Nếu đang quá tải, làm ngay]"))
        self.assertIn("Dấu hiệu cấp cứu không thuộc mức xanh", text)
        self.assertIn("triệu chứng tự hết không phải lý do bỏ qua đánh giá khẩn", text)
        self.assertIn("dừng buổi hiện tại", text)
        appendix = read("book/appendices/e-ban-do-quyet-dinh.typ")
        self.assertIn("không chờ ghi nhãn hay thử tiếp đất", appendix)
        self.assertIn("link(<cap-cuu-ngay>)", appendix)

    def test_clinging_aggregate_gloss_has_a_traceable_source(self):
        source = read("book/chapters/99-nguon.typ")
        self.assertIn("[K53]", source)
        self.assertIn("SN22_48.html", source)
        for path in (
            "book/chapters/02-dich-den-va-nen-tang.typ",
            "book/chapters/03-tu-niem-xu-trong-kinh.typ",
            "book/chapters/13-tu-dieu-de-van-hanh.typ",
            "book/appendices/d-thuat-ngu.typ",
        ):
            text = read(path)
            self.assertIn("K53", text, path)
            self.assertIn("có thể bị chấp thủ", text, path)

    def test_insight_detail_and_source_distinctions_survive(self):
        text = read("book/chapters/12-ban-do-tue.typ")
        headings = re.findall(r"^==== (\d+)\.", text, re.MULTILINE)
        self.assertEqual(headings, [str(i) for i in range(1, 18)])
        self.assertIn("V01 · XVIII.1–5", text)
        self.assertIn("V01 · XXI.32–33", text)
        self.assertIn("V01 · XXII.1; 7–11", text)
        self.assertIn("không đồng nhất với đạo trí", text)
        self.assertNotIn("Nibbidā* ở đây gần với ly tham", text)
        self.assertIn("giới hạn suy luận của bản biên soạn", text)

    def test_closing_recalls_all_four_tasks(self):
        text = read("book/chapters/loi-cuoi.typ")
        for phrase in (
            "khổ cần được hiểu", "ái cần được từ bỏ",
            "sự chấm dứt khổ cần được thực chứng", "con đường cần được tu tập",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
