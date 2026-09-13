# Tích hợp bộ câu hỏi tự soi ba kiết sử đầu

Ngày: **2026-09-13**. Đây là hồ sơ tích hợp nội dung, không phải giấy chứng nhận giáo lý hoặc bản phát hành đã thẩm định.

## Nguồn và phạm vi

- PR: [#65](https://github.com/streamentry/streamentry/pull/65).
- Nhánh: `editorial/three-fetters-checklists-20260913`.
- Bắt đầu từ `main` tại `6eb33b6ca4a6510ee61e12bfd1f6ac277d88d60d`, cây `701761035c07da03e5b5afe826080930c453e78d`.
- Phụ lục F nằm ở `book/appendices/f-tu-soi-ba-kiet-su.typ`, được đưa vào `book/main.typ` trước bản đồ nguồn.
- Chương 10 dẫn đến ba phần và giới hạn kết luận, không sao chép toàn bộ checklist vào chương.
- Bản đồ nguồn thêm K45–K52; claim ledger thêm C81–C89. Hồ sơ `three-fetters-checklist-audit-2026-09-13.md` ánh xạ từng câu hỏi đến nguồn và ghi giới hạn suy luận.
- Giữ đủ bảng 20 cách chấp và 17 câu hỏi: T1–T5, H1–H6, G1–G6. Không có điểm đạt, lịch bắt buộc hoặc cách tự tính quả vị.
- Không sửa bản Markdown gốc, hồ sơ đối chiếu bất biến, metadata ấn bản, `dist`, cổng quyền sử dụng hoặc bằng chứng phát hành cũ. Không sửa workflow hay dependencies trong PR này.

## Chỉnh câu chữ và dàn trang

Đã đọc lại các nguồn trọng yếu, giữ riêng kinh, lời đệ tử được tán thành và lời biên soạn. Giải thích thuật ngữ ngay tại chỗ; không dùng đại từ “tôi”, việc khảo sát nguồn hoặc giữ giới nghiêm làm dấu hiệu đủ để kết luận kiết sử. Không thấy biểu hiện cũng không chứng minh đoạn tận; khả năng tự tuyên bố có điều kiện trong AN 10.92 được giữ nguyên phạm vi.

Bản dựng đầu từ `afdc845092c37dee53c158f6f01650aa1ac2510d` phát hiện nhãn nguồn H2 bị tách sang trang sau và đoạn G5 bị chia trang. Commit `e6fae8cea1ac54ec3b223856fe14935f8fbe00c9` giữ từng câu hỏi, lời giải và nguồn trong một khối không ngắt trang, đồng thời thêm kiểm tra hồi quy. Không rút nội dung, giảm cỡ chữ hoặc thay cấu trúc giáo lý để xử lý dàn trang.

## Kiểm tra cục bộ

| Nhóm | Số kiểm tra | Kết quả |
|---|---:|---|
| `test_three_fetters_checklists.py` | 15 | Đạt |
| `test_source_code_legend.py` | 6 | Đạt |
| `test_chapter_10_contract.py` | 2 | Đạt |

Tổng cộng **23/23 kiểm tra liên quan trực tiếp đạt**. Các kiểm tra này bảo vệ cấu trúc, nguồn dẫn, ranh giới và tính toàn vẹn; không thay phản biện độc lập. Môi trường cục bộ không có Typst; bản toàn sách dưới đây được dựng trên GitHub Actions, không dùng PDF 15 trang của gói bàn giao trước làm bằng chứng thay thế.

## Bản dựng toàn sách đã kiểm tra

- Head chứa nội dung và kiểm tra: `e6fae8cea1ac54ec3b223856fe14935f8fbe00c9`.
- Checkout merge do GitHub tạo: `43a87046105835dc9828b5558161cd198d49a5fc`.
- [Editorial preview run 34741915769](https://github.com/streamentry/streamentry/actions/runs/34741915769).
- Artifact: `10312477021`, tên `editorial-preview-43a87046105835dc9828b5558161cd198d49a5fc`.
- Toàn bộ 9 tệp sửa hoặc thêm trong `source.zip` khớp blob nguồn làm việc đã kiểm tra; không có sai lệch do chuyển nội dung lên GitHub.

| Hạng mục | Kết quả thực tế |
|---|---|
| PDF | Dựng thành công, **240 trang**. Phụ lục F ở trang PDF **216–226**, tương ứng số in **215–225**. |
| EPUB | Dựng thành công, **249.060 byte**, **277 mục điều hướng**. |
| Kiểm tra EPUB cục bộ | **400 tham chiếu nội bộ**, không gặp đường dẫn hoặc fragment thiếu; không gặp ID trùng trong các tài liệu XML đã đọc. |
| Quét PDF | Đọc tọa độ chữ trên cả 240 trang; không phát hiện chữ vượt biên trang hoặc trang hoàn toàn rỗng. Đây không phải kiểm tra mọi dạng chồng lấn hay mọi trình đọc. |
| Xem ảnh | Đã xem toàn bộ 11 trang Phụ lục F sau sửa dàn trang. Nguồn của H2 không còn lẻ đầu trang; G5 cùng nội dung và nguồn trên một trang. Đã xem thêm các trang sửa của Chương 10 và các trang nguồn mới trong lượt dựng trước; trang K51–K52 cũng được xem trong bản cuối. |
| Hồi quy toàn kho | **222 kiểm tra: 221 đạt, 1 lỗi** ở `test_current_release_evidence_matches_dist_artifacts`: PDF mới không khớp SHA-256 trong hồ sơ phát hành cũ. |
| Lint và cú pháp | Ruff, compileall và `git diff --check` đạt. |
| Cảnh báo HTML | Build ghi nhận **200 cảnh báo đã được bộ dựng nhận diện**; không gọi đây là bản dựng không có cảnh báo. |

PDF SHA-256: `c5d008b42407464638c6354cd62d7af3544e0f25a37cffc85b9533e37af434a0`.

EPUB SHA-256: `409dc2e91bc30d63fdf5844eb015b318ca9cc306ffca381e2fe084415c848aad`.

SHA-256 bản Markdown gốc giữ nguyên: `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440`.

## CI chưa xanh và ranh giới phát hành

Không đổi hồ sơ phát hành cũ để khớp đầu ra mới. Verifier dừng tại hash PDF nên không coi các cổng phía sau đã đạt. Lỗi kiểu này đã xuất hiện ở bản biên tập trước; nó không được che bằng việc bỏ kiểm tra hoặc cập nhật chứng cứ giả.

Ngoài lỗi hash, [Publication CI run 34741577385](https://github.com/streamentry/streamentry/actions/runs/34741577385), job `103682055500`, dừng ở kiểm tra bảo mật dependencies trước các bước build/phát hành. Log đã đọc ghi **4 cảnh báo mức high** ở dependencies hiện có, bao gồm pip và setuptools. PR này không thay các tệp dependency hoặc workflow. Không tắt, hạ ngưỡng hoặc bỏ qua cổng ấy; việc cập nhật công cụ cần được xử lý và kiểm thử riêng.

Hồ sơ này ghi kết quả ở commit nội dung nêu trên. Commit chỉ bổ sung hồ sơ kiểm tra không thay tệp nguồn Typst, scripts, tests hoặc artifact đã dựng. Trạng thái merge chính thức phải kiểm tra trên PR; không ghi trước rằng đã merge khi chưa có kết quả API.

**Merge nội dung vào `main` không tự là phát hành PDF/EPUB mới đã được thẩm định.** Bản hiện tại là bản đọc để kiểm tra; chưa có phản biện độc lập cho checklist, thử đọc người mới, xác minh độc lập mức chứng đạt, hoặc bộ bằng chứng phát hành mới. Các tệp `dist` trong kho vẫn thuộc bản phát hành trước. Quy trình phát hành phải tạo bằng chứng gắn đúng artifact và hoàn tất các cổng của kho, không tái dùng hồ sơ cũ như chứng nhận cho nội dung mới.
