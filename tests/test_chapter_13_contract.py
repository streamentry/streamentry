from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "book" / "chapters" / "13-tu-dieu-de-van-hanh.typ"
MAIN_PATH = ROOT / "book" / "main.typ"


class Chapter13ContractTests(unittest.TestCase):
    """Text regressions protect distinctions, not a claim of doctrinal validation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.chapter = CHAPTER_PATH.read_text(encoding="utf-8")
        cls.main = MAIN_PATH.read_text(encoding="utf-8")
        cls.plain = re.sub(r"\s+", " ", cls.chapter)

    def assert_markers(self, *markers: str) -> None:
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.plain)

    def test_chapter_is_included_before_the_insight_map(self) -> None:
        self.assertLess(
            self.main.index('#include "chapters/13-tu-dieu-de-van-hanh.typ"'),
            self.main.index('#include "chapters/12-ban-do-tue.typ"'),
        )

    def test_four_truths_keep_their_source_bounded_tasks(self) -> None:
        self.assert_markers(
            "Khổ cần được hiểu đầy đủ",
            "nguồn sinh khổ cần được đoạn trừ",
            "sự chấm dứt khổ cần được thực chứng",
            "con đường cần được tu tập",
            "không phải bốn bước chứng ngộ",
            "K05 · SN 56.11",
            "mười hai phương diện",
        )

    def test_dependent_origination_has_both_scales_and_a_limit(self) -> None:
        self.assert_markers(
            "Năm nhịp nhìn một phản ứng",
            "không phải năm sát-na tâm hay năm chi của duyên khởi",
            "không gọi đó là mắt xích dễ cắt nhất cho mọi người",
            "không thu toàn bộ duyên khởi",
            "K26 · SN 12.2",
        )
        chain = (
            "Vô minh", "Hành", "Thức", "Danh sắc", "Sáu xứ", "Xúc",
            "Thọ", "Ái", "Thủ", "Hữu", "Sinh", "Già–chết và khối khổ",
        )
        positions = [self.chapter.index(f"[{term}]") for term in chain]
        self.assertEqual(positions, sorted(positions))

    def test_nearby_terms_are_distinguished_without_becoming_diagnoses(self) -> None:
        self.assert_markers(
            "Vô minh có phải là si?",
            "*moha*, si",
            "*avijjā*, vô minh",
            "Ái, tham, sân và thủ không phải một nhãn",
            "Từ chối hành vi gây hại cũng không nhất thiết là sân",
            "Thọ không phải toàn bộ cảm xúc",
        )

    def test_visual_maps_are_reflowable_and_keep_the_source_boundaries(self) -> None:
        self.assert_markers(
            "Bản đồ một trang", "#concept-map(", "#flow-ribbon(",
            "Đây là sơ đồ giúp học", "Những câu hỏi trong sơ đồ do sách đặt ra",
            "TUỆ · 2 CHI", "GIỚI · 3 CHI", "ĐỊNH · 3 CHI",
            "THẤY · HƯỚNG", "NÓI · LÀM · NUÔI", "RÈN · NHỚ-BIẾT · VỮNG",
            "K20 · MN 44",
        )

    def test_cessation_truth_is_named_as_nibbana_without_overclaiming(self) -> None:
        self.assert_markers(
            "Diệt đế có phải là Niết-bàn không?", "K43 · SN 38.1",
            "Tôn giả Sāriputta", "Diệt đế là sự thật về Niết-bàn",
            "chưa phải đoạn tận", "không cần được nâng thành lời xác nhận",
            "Tạm lắng:", "Suy yếu:", "Đoạn tận:",
        )

    def test_path_and_stream_entry_claims_do_not_collapse_into_one_method(self) -> None:
        self.assert_markers(
            "Tám chi với tám công việc", "K42 · AN 5.177",
            "vũ khí, sinh vật, thịt, chất say và chất độc",
            "không đồng nhất một cách ghi nhận, một tư thế hay một lịch ngồi",
            "chưa đủ để xác nhận Nhập lưu",
            "K02 · SN 55.50", "K11 · MN 2",
        )

    def test_translation_and_editorial_boundaries_are_visible(self) -> None:
        self.assert_markers(
            "Sách diễn ý bốn nhiệm vụ", "Không phải trích nguyên văn một bản dịch Việt",
            "là việc áp dụng của người biên soạn",
            "không phải những mục cổ đã được liệt kê sẵn",
            "Đây là minh họa biên soạn", "không phải kết luận đã chứng Diệt đế",
        )

    def test_chapter_ends_with_closed_book_retrieval_and_safety_routing(self) -> None:
        self.assert_markers(
            "Gấp sách lại: tự kiểm bằng lời của mình", "Bốn câu không cần học thuộc",
            "Nếu trẻ sắp ngã, xe đang lao tới", "hãy làm việc an toàn trước",
            "Sáu mươi giây chỉ là gợi ý", "không ở một mình khi có nguy cơ tự hại tức thì",
            "Các hướng dẫn đầy đủ nằm ở Chương 9",
        )

    def test_right_action_and_concentration_keep_exact_source_distinctions(self) -> None:
        self.assert_markers(
            "K23 · MN 117", "K25 · SN 45.8",
            "*abrahmacariyā veramaṇī*", "đây là yêu cầu tiết dục",
            "không phải chỉ tránh tà hạnh", "giữ riêng sự khác nhau giữa hai đoạn",
            "chánh định được định nghĩa bằng bốn tầng thiền",
            "nghe hết một câu không tự nó là định nghĩa chánh định",
        )

    def test_craving_is_not_every_wish_to_end_discomfort(self) -> None:
        self.assert_markers(
            "K44 · Iti 49", "không dùng câu", "làm định nghĩa đầy đủ của phi hữu ái",
            "Mong chữa bệnh, rời nơi bị bạo hành",
            "không tự nó chứng minh có phi hữu ái",
            "không đồng nhất mọi mong muốn với tham ái cần đoạn trừ",
            "tham ái đưa đến tái sinh",
        )


if __name__ == "__main__":
    unittest.main()
