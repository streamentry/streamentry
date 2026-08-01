from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "book" / "chapters" / "13-tu-dieu-de-van-hanh.typ"
MAIN_PATH = ROOT / "book" / "main.typ"


class Chapter13ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chapter = CHAPTER_PATH.read_text(encoding="utf-8")
        cls.main = MAIN_PATH.read_text(encoding="utf-8")

    def test_chapter_is_included_after_the_existing_insight_map(self) -> None:
        self.assertIn(
            '#include "chapters/12-ban-do-tue.typ"\n'
            '#include "chapters/13-tu-dieu-de-van-hanh.typ"',
            self.main,
        )

    def test_four_truths_keep_their_source_bounded_tasks(self) -> None:
        for phrase in (
            "Khổ là điều cần được hiểu",
            "Tập, được bài kinh nêu là ái, cần được đoạn",
            "Diệt cần được trực chứng",
            "Đạo là Bát Thánh Đạo và cần được tu tập",
            "không phải bốn bước chứng ngộ",
        ):
            self.assertIn(phrase, self.chapter)
        self.assertIn("K05 · SN 56.11", self.chapter)

    def test_dependent_origination_has_both_scales_and_a_limit(self) -> None:
        for phrase in (
            "Năm nhịp nhìn một phản ứng",
            "không phải toàn bộ mười hai chi",
            "không phải “mắt xích dễ cắt nhất cho mọi người”",
        ):
            self.assertIn(phrase, self.chapter)
        full_chain = tuple(
            f"[{term}]"
            for term in (
                "Vô minh",
                "Hành",
                "Thức",
                "Danh sắc",
                "Sáu xứ",
                "Xúc",
                "Thọ",
                "Ái",
                "Thủ",
                "Hữu",
                "Sinh",
                "Già–chết + khối khổ",
            )
        )
        positions = [self.chapter.index(term) for term in full_chain]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("K26 · SN 12.2", self.chapter)

    def test_nearby_terms_are_distinguished_without_becoming_diagnoses(self) -> None:
        for phrase in (
            "Vô minh có phải là si?",
            "MN 9 dùng *moha* trong bộ ba gốc bất thiện",
            "cùng thuộc vùng mê mờ",
            "*Ái và tham:*",
            "*Sân và chấp thủ:*",
            "không biến một nhãn tâm lý thành kết luận về quả vị",
        ):
            self.assertIn(phrase, self.chapter)

    def test_visual_maps_are_reflowable_and_keep_the_source_boundaries(self) -> None:
        for phrase in (
            "Bản đồ một trang",
            "#concept-map(",
            "#flow-ribbon(",
            "bản đồ chức năng để học",
            "Vị trí trên trang giúp trí nhớ",
            "TUỆ · 2 CHI",
            "GIỚI · 3 CHI",
            "ĐỊNH · 3 CHI",
            "THẤY · HƯỚNG",
            "NÓI · LÀM · NUÔI",
            "RÈN · NHỚ-BIẾT · VỮNG",
        ):
            self.assertIn(phrase, self.chapter)

    def test_cessation_truth_is_named_as_nibbana_without_overclaiming(self) -> None:
        for phrase in (
            "Diệt đế có phải là Niết-bàn không?",
            "*Câu trả lời ngắn: có.*",
            "K43 · SN 38.1",
            "Một cứu cánh, hai góc nhìn",
            "một lần ái không được tiếp sức",
            "chưa phải đoạn tận",
        ):
            self.assertIn(phrase, self.chapter)

    def test_path_and_stream_entry_claims_do_not_collapse_into_one_method(self) -> None:
        for phrase in (
            "Tám chi với tám công việc",
            "AN 5.177 nói rõ một cư sĩ không nên buôn bán năm thứ",
            "một cách ghi nhận, một bài tập thở, một tư thế, một lịch ngồi",
            "không tự chứng minh quả Nhập lưu",
            "K02 · SN 55.50",
            "K11 · MN 2",
        ):
            self.assertIn(phrase, self.chapter)

    def test_translation_and_editorial_boundaries_are_visible(self) -> None:
        for phrase in (
            "phỏng dịch để đọc",
            "không phải bản dịch Việt xuất bản hay lời trích nguyên văn",
            "ứng dụng hiện đại của người biên soạn",
            "khung sư phạm, không phải công thức ba bước",
            "chưa có bằng chứng rằng tham ái đã đoạn tận",
        ):
            self.assertIn(phrase, self.chapter)

    def test_chapter_ends_with_closed_book_retrieval_and_safety_routing(self) -> None:
        for phrase in (
            "Gấp sách lại: tự kiểm bằng lời của mình",
            "Bốn câu không cần học thuộc",
            "Nếu trẻ sắp ngã, xe đang lao tới",
            "hãy bỏ bài tập và làm theo ngưỡng an toàn ở Chương 9",
        ):
            self.assertIn(phrase, self.chapter)


if __name__ == "__main__":
    unittest.main()
