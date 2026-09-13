from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPENDIX = ROOT / 'book/appendices/f-tu-soi-ba-kiet-su.typ'


class ThreeFettersChecklistTests(unittest.TestCase):
    """Structural/content regressions, not proof of doctrine or attainment."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = APPENDIX.read_text(encoding='utf-8')
        cls.sources = (ROOT / 'book/chapters/99-nguon.typ').read_text(encoding='utf-8')
        cls.chapter = (ROOT / 'book/chapters/10-nhap-luu.typ').read_text(encoding='utf-8')
        cls.audit = (ROOT / 'book/references/three-fetters-checklist-audit-2026-09-13.md').read_text(encoding='utf-8')

    def test_appendix_is_in_real_book_entry_point(self) -> None:
        main = (ROOT / 'book/main.typ').read_text(encoding='utf-8')
        target = '#include "appendices/f-tu-soi-ba-kiet-su.typ"'
        self.assertEqual(main.count(target), 1)
        self.assertLess(main.index(target), main.index('#include "chapters/99-nguon.typ"'))
        self.assertIn('#link(<tu-soi-ba-kiet-su>)', self.chapter)

    def test_twenty_cell_matrix_has_all_five_aggregates_and_four_columns(self) -> None:
        table = self.text.split('#table(', 1)[1].split('\n)\n', 1)[0]
        self.assertIn('table.header([Uẩn đang xét], [A], [B], [C], [D])', table)
        rows = re.findall(r'^  \[(Sắc|Thọ|Tưởng|Hành|Thức)\], \[\], \[\], \[\], \[\],$', table, re.M)
        self.assertEqual(rows, ['Sắc', 'Thọ', 'Tưởng', 'Hành', 'Thức'])
        for relation in ('Uẩn là tự ngã', 'Tự ngã có uẩn', 'Uẩn ở trong tự ngã', 'Tự ngã ở trong uẩn'):
            self.assertIn(relation, self.text)

    def test_observation_status_does_not_claim_eradication(self) -> None:
        for text in ('“Có”', '“?”', '“Chưa thấy” không có nghĩa “đã đoạn tận”', 'không có điểm đạt', 'chưa được thẩm định'):
            self.assertIn(text, self.text)
        self.assertIn('không cộng số ô', self.text)

    def test_seventeen_prompts_are_individually_sourced_as_editorial(self) -> None:
        sections = re.findall(r'=== ([THG]\d)\. (.*?)(?=\n===? |\Z)', self.text, re.S)
        self.assertEqual([code for code, _ in sections],
                         [f'T{i}' for i in range(1, 6)] +
                         [f'H{i}' for i in range(1, 7)] +
                         [f'G{i}' for i in range(1, 7)])
        for code, section in sections:
            with self.subTest(code=code):
                self.assertIn('#source-badge("BIÊN SOẠN"', section)
                self.assertRegex(section, r'#link\("https://[^\"]+"\)\[K\d{2}')
                self.assertIn(f'| {code} |', self.audit)

    def test_each_prompt_keeps_its_source_badge_on_the_same_printed_page(self) -> None:
        blocks = re.findall(
            r'#block\(breakable: false\)\[\n(=== [THG]\d\. .*?)\n\]',
            self.text,
            re.S,
        )
        self.assertEqual(len(blocks), 17)
        for block in blocks:
            self.assertIn('#source-badge("BIÊN SOẠN"', block)

    def test_all_source_codes_used_in_appendix_are_declared(self) -> None:
        used = set(re.findall(r'\bK\d{2}\b', self.text))
        declared = re.findall(r'#reference-item\(\s*\[(K\d{2})\]', self.sources)
        self.assertTrue(used <= set(declared), used - set(declared))
        self.assertEqual(len(declared), len(set(declared)))
        self.assertIn(f'*K01–K{max(int(code[1:]) for code in declared):02d}*', self.sources)

    def test_internal_links_resolve_and_new_anchors_are_unique(self) -> None:
        all_book = '\n'.join(p.read_text(encoding='utf-8') for p in (ROOT / 'book').rglob('*.typ'))
        definitions = re.findall(r'(?<!\()(?<!<)<([a-z0-9-]+)>', all_book)
        new_definitions = re.findall(r'(?<!\()<([a-z0-9-]+)>', self.text)
        for name in new_definitions:
            self.assertEqual(definitions.count(name), 1, name)
        for name in re.findall(r'#link\(<([a-z0-9-]+)>\)', self.text):
            self.assertIn(name, definitions)

    def test_mn16_four_doubts_are_not_mislabeled_five_doubts(self) -> None:
        self.assertIn('Đạo sư, Pháp, Tăng và sự học tập', self.text)
        self.assertIn('không phải một mục nghi thứ năm', self.text)
        self.assertIn('không trình bày một bài kiểm tra đầy đủ', self.text)
        self.assertIn('hễ chưa siêng tu là còn hoài nghi', self.text)

    def test_inquiry_and_faith_are_both_kept(self) -> None:
        self.assertIn('lòng tin có căn cứ', self.text)
        self.assertIn('không lấy mức tự tin làm bằng chứng', self.text)
        self.assertIn('còn nghi điều gì cũng được', self.text)
        self.assertIn('không khiến mọi niềm tin có căn cứ', self.text)

    def test_an378_has_correct_speaker_numbering_and_scope(self) -> None:
        self.assertIn('Tôn giả Ānanda phân biệt', self.text)
        self.assertIn('Đức Phật tán thành câu trả lời', self.text)
        self.assertIn('theo hệ số SuttaCentral', self.text)
        self.assertIn('không tự đồng nghĩa với toàn bộ thuật ngữ', self.text)
        self.assertIn('https://suttacentral.net/an3.78/en/sujato', self.sources)
        self.assertNotIn('dhammatalks.org/suttas/AN/AN3_78.html', self.text + self.sources)

    def test_precepts_and_practices_not_rejected_as_such(self) -> None:
        for phrase in ('không thể suy từ việc bỏ chấp thủ đến việc bỏ giới hạnh',
                       'Giữ đều một thời khóa cũng không tự là chấp thủ',
                       'không kết luận ai theo nghi thức khác mình đều chấp thủ'):
            self.assertIn(phrase.casefold(), self.text.casefold())

    def test_language_conceit_and_body_safety_are_distinguished(self) -> None:
        for phrase in ('đếm đại từ không phải phép thử', 'Tôn giả Khemaka',
                       'người đã đoạn năm hạ phần kiết sử', 'nhu cầu nghỉ',
                       'không yêu cầu một cảm giác kỳ lạ'):
            self.assertIn(phrase, self.text)

    def test_self_declaration_conditions_are_not_prohibited_or_reduced(self) -> None:
        for phrase in ('cho phép vị Thánh đệ tử tự tuyên bố',
                       'nguyên lý duyên khởi được thấy đúng bằng tuệ',
                       'không có nghĩa phải hết mọi cảm giác lo',
                       'không chứng nhận một ai từ phiếu tự khai'):
            self.assertIn(phrase, self.text)

    def test_no_internal_claim_ids_in_reader_facing_appendix(self) -> None:
        self.assertIsNone(re.search(r'\bC\d{2}\b', self.text))
        self.assertIn('Giữ ghi chép riêng tư', self.text)
        self.assertIn('Không thử gây đau, gây sợ hay tạo xung đột', self.text)

    def test_immutable_source_manuscript_is_unchanged(self) -> None:
        digest = hashlib.sha256((ROOT / 'con-duong-niem-xu-mahasi-hop-nhat.md').read_bytes()).hexdigest()
        self.assertEqual(digest, 'ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440')


if __name__ == '__main__':
    unittest.main()
