from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from edition_contract import (  # noqa: E402
    EDITION,
    EditionContractError,
    load_edition_contract,
)


EDITION_PATH = ROOT / "book" / "edition.json"


class EditionContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(EDITION_PATH.read_text(encoding="utf-8"))

    def _assert_invalid(
        self,
        mutate: Callable[[dict[str, Any]], None],
        message: str,
    ) -> None:
        payload = copy.deepcopy(self.payload)
        mutate(payload)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "edition.json"
            path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(EditionContractError, message):
                load_edition_contract(path)

    def test_canonical_contract_has_the_exact_current_values(self) -> None:
        self.assertEqual(
            asdict(EDITION),
            {
                "schema_version": 1,
                "edition_id": "vi-2026",
                "title": "Hướng Đến Nhập Lưu",
                "author": "CS Chánh Niệm + ChatGPT",
                "language": "vi",
                "description": (
                    "Sổ tay Niệm xứ cho người tại gia theo truyền thống Mahāsi, "
                    "đối chiếu Kinh tạng Pāli và Thanh Tịnh Đạo"
                ),
                "keywords": (
                    "Niệm xứ",
                    "Mahāsi",
                    "Nhập lưu",
                    "Thiền Vipassanā",
                    "Thanh Tịnh Đạo",
                ),
                "subjects": (
                    "Niệm xứ",
                    "Duyên khởi",
                    "Thiền Vipassanā",
                ),
                "file_stem": "huong-den-nhap-luu",
                "identifier_seed": "https://streamentry.local/huong-den-nhap-luu",
                "epub_modified": "2026-07-27T00:00:00Z",
                "pdf_creation_timestamp": "1785110400",
                "source_path": "con-duong-niem-xu-mahasi-hop-nhat.md",
                "source_sha256": (
                    "ad7a886895cf8cd29b369fda89de5665"
                    "c96907d990f95dba8f028336bcbbd440"
                ),
                "cover_title_lines": ("Hướng Đến", "Nhập Lưu"),
                "cover_kicker": "Sổ tay Niệm xứ cho người tại gia",
                "cover_edition_label": "Ấn bản thực hành 2026",
                "cover_provenance_lines": (
                    "Kinh tạng Pāli · Thanh Tịnh Đạo",
                    "Chỉ dẫn thực hành Mahāsi",
                ),
                "author_label": "Tác giả",
                "chapter_label": "Chương",
                "practice_label": "Thực hành",
                "faq_label": "Giải đáp",
                "caution_label": "Giới hạn cần nhớ",
                "source_link_label": "Mở bản nguồn trực tuyến",
                "toc_label": "Mục lục",
                "introduction_label": "Lời dẫn",
                "cover_label": "Bìa",
                "content_label": "Nội dung",
                "landmarks_label": "Các điểm mốc",
                "cover_alt": "Bìa sách Hướng Đến Nhập Lưu",
                "accessibility_summary": (
                    "Ấn bản có mục lục điều hướng phân cấp, văn bản reflowable "
                    "và nhãn thay thế cho ảnh bìa."
                ),
                "semantic_required_text": (
                    "Duyên khởi ngay nơi thọ và ái",
                    "Có phải thọ đến ái là mắt xích dễ cắt nhất?",
                    "Đọc bản đồ theo bốn vùng",
                    "Bản đồ quyết định khi đang hành",
                    "Có việc phải bảo vệ ngay không?",
                ),
                "validation_locale": "vi-VN",
                "target_audience": (
                    "Người lớn Việt Nam mới bắt đầu thực hành thiền"
                ),
            },
        )
        self.assertEqual(
            EDITION.identifier,
            "urn:uuid:c72fa1d8-39be-5e0e-ac0f-1999dd06d83a",
        )
        self.assertEqual(
            EDITION.pdf_relative_path,
            Path("dist/huong-den-nhap-luu.pdf"),
        )
        self.assertEqual(
            EDITION.epub_relative_path,
            Path("dist/huong-den-nhap-luu.epub"),
        )

    def test_default_load_is_independent_of_the_process_working_directory(self) -> None:
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                loaded = load_edition_contract()
            finally:
                os.chdir(previous)
        self.assertEqual(loaded, EDITION)

    def test_rejects_duplicate_json_keys(self) -> None:
        raw = EDITION_PATH.read_text(encoding="utf-8").replace(
            '    "title": "Hướng Đến Nhập Lưu",',
            (
                '    "title": "Shadow title",\n'
                '    "title": "Hướng Đến Nhập Lưu",'
            ),
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "edition.json"
            path.write_text(raw, encoding="utf-8")
            with self.assertRaisesRegex(
                EditionContractError,
                "duplicate JSON key: title",
            ):
                load_edition_contract(path)

    def test_rejects_duplicate_array_values(self) -> None:
        self._assert_invalid(
            lambda payload: payload["metadata"]["subjects"].append("Niệm xứ"),
            "must not contain duplicate values",
        )

    def test_rejects_missing_and_unknown_keys(self) -> None:
        cases = (
            (
                lambda payload: payload["metadata"].pop("author"),
                r"edition\.metadata is missing keys: \['author'\]",
            ),
            (
                lambda payload: payload["labels"].update({"shadow": "Hidden"}),
                r"edition\.labels has unknown keys: \['shadow'\]",
            ),
        )
        for mutate, message in cases:
            with self.subTest(message=message):
                self._assert_invalid(mutate, message)

    def test_rejects_wrong_types_and_blank_strings(self) -> None:
        cases = (
            (
                lambda payload: payload["metadata"].update({"title": 7}),
                "edition.metadata.title must be a non-empty string",
            ),
            (
                lambda payload: payload["metadata"].update({"keywords": "Niệm xứ"}),
                "edition.metadata.keywords must be a non-empty array",
            ),
            (
                lambda payload: payload["metadata"].update({"author": ""}),
                "edition.metadata.author must be a non-empty string",
            ),
        )
        for mutate, message in cases:
            with self.subTest(message=message):
                self._assert_invalid(mutate, message)

    def test_rejects_non_nfc_text(self) -> None:
        self._assert_invalid(
            lambda payload: payload["metadata"].update(
                {"author": "CS Cha\u0301nh Niệm + ChatGPT"}
            ),
            "edition.metadata.author must use NFC Unicode normalization",
        )

    def test_rejects_unsupported_or_wrong_type_schema_versions(self) -> None:
        for value in (2, True, "1"):
            with self.subTest(value=value):
                self._assert_invalid(
                    lambda payload, value=value: payload.update(
                        {"schema_version": value}
                    ),
                    "edition.schema_version must be integer 1",
                )

    def test_rejects_invalid_or_mismatched_languages(self) -> None:
        cases = (
            (
                lambda payload: payload["metadata"].update({"language": "v"}),
                "edition.metadata.language must be a BCP 47 tag",
            ),
            (
                lambda payload: payload["scope"].update(
                    {"validation_locale": "vi_ VN"}
                ),
                "edition.scope.validation_locale must be a BCP 47 tag",
            ),
            (
                lambda payload: payload["scope"].update(
                    {"validation_locale": "en-US"}
                ),
                "validation locale must share the publication language",
            ),
        )
        for mutate, message in cases:
            with self.subTest(message=message):
                self._assert_invalid(mutate, message)

    def test_rejects_invalid_edition_and_file_slugs(self) -> None:
        cases = (
            (
                lambda payload: payload.update({"edition_id": "VI 2026"}),
                "edition.edition_id must be a lowercase slug",
            ),
            (
                lambda payload: payload["publication"].update(
                    {"file_stem": "Huong_Den_Nhap_Luu"}
                ),
                "edition.publication.file_stem must be a lowercase slug",
            ),
        )
        for mutate, message in cases:
            with self.subTest(message=message):
                self._assert_invalid(mutate, message)

    def test_rejects_cover_title_lines_that_do_not_reconstruct_the_title(self) -> None:
        self._assert_invalid(
            lambda payload: payload["cover"].update(
                {"title_lines": ["Hướng Đến", "Dòng Khác"]}
            ),
            "edition.cover.title_lines must reconstruct the metadata title",
        )

    def test_rejects_release_identity_and_source_inconsistencies(self) -> None:
        cases = (
            (
                lambda payload: payload["publication"].update(
                    {"identifier_seed": "http://example.test/book"}
                ),
                "identifier_seed must be an absolute HTTPS URL",
            ),
            (
                lambda payload: payload["publication"].update(
                    {"identifier_seed": "https:///missing-host"}
                ),
                "identifier_seed must be an absolute HTTPS URL",
            ),
            (
                lambda payload: payload["publication"].update(
                    {"epub_modified": "2026-07-28T00:00:00Z"}
                ),
                "must identify one instant",
            ),
            (
                lambda payload: payload["source"].update(
                    {"path": "../shadow.md"}
                ),
                "source.path must be a safe relative path",
            ),
            (
                lambda payload: payload["accessibility"].update(
                    {"cover_alt": "Generic cover"}
                ),
                "cover_alt must identify the edition title",
            ),
        )
        for mutate, message in cases:
            with self.subTest(message=message):
                self._assert_invalid(mutate, message)

    def test_rejects_an_epoch_outside_the_supported_datetime_range(self) -> None:
        self._assert_invalid(
            lambda payload: payload["publication"].update(
                {"pdf_creation_timestamp": "9" * 100}
            ),
            "pdf_creation_timestamp is outside the supported range",
        )


if __name__ == "__main__":
    unittest.main()
