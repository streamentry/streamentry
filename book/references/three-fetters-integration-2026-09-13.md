# Tích hợp bộ câu hỏi tự soi ba kiết sử đầu

Ngày: **2026-09-13**. Đây là hồ sơ tích hợp nội dung, không phải giấy chứng nhận giáo lý hoặc bản phát hành đã thẩm định.

## Nguồn và phạm vi

- Nhánh: `editorial/three-fetters-checklists-20260913`.
- Bắt đầu từ `main` tại `6eb33b6ca4a6510ee61e12bfd1f6ac277d88d60d`, cây `701761035c07da03e5b5afe826080930c453e78d`.
- Phụ lục F nằm ở `book/appendices/f-tu-soi-ba-kiet-su.typ`, được đưa vào `book/main.typ` trước bản đồ nguồn.
- Chương 10 dẫn đến ba phần và giới hạn kết luận, không sao chép toàn bộ checklist vào chương.
- Bản đồ nguồn thêm K45–K52; claim ledger thêm C81–C89. Hồ sơ `three-fetters-checklist-audit-2026-09-13.md` ánh xạ từng câu hỏi đến nguồn và ghi giới hạn suy luận.
- Giữ đủ bảng 20 cách chấp và 17 câu hỏi: T1–T5, H1–H6, G1–G6. Không có điểm đạt, lịch bắt buộc hoặc cách tự tính quả vị.
- Không sửa bản Markdown gốc, hồ sơ đối chiếu bất biến, metadata ấn bản, `dist`, cổng quyền sử dụng hoặc bằng chứng phát hành cũ.

## Kiểm tra cục bộ trước PR

Ba nhóm kiểm tra đã chạy trên nguồn làm việc sau chỉnh sửa câu chữ:

| Nhóm | Số kiểm tra | Kết quả |
|---|---:|---|
| `test_three_fetters_checklists.py` | 14 | Đạt |
| `test_source_code_legend.py` | 6 | Đạt |
| `test_chapter_10_contract.py` | 2 | Đạt |

Các kiểm tra này bảo vệ cấu trúc, nguồn dẫn, ranh giới và tính toàn vẹn; không thay phản biện độc lập. Môi trường cục bộ không có Typst. Bản PDF 15 trang của gói bàn giao trước không được dùng làm bằng chứng bản toàn sách đã dựng.

## Bản dựng và tình trạng GitHub

Tại commit mở PR, việc dựng toàn sách và kết quả CI còn chờ thực hiện qua workflow `editorial-preview.yml` đã có. Bản ghi này sẽ bổ sung mã run, commit, hash và kết quả thực tế sau khi đọc artifact. Không ghi trước rằng CI, merge hoặc phát hành đã hoàn tất.

Việc merge nội dung vào `main` không tự là phát hành PDF/EPUB mới. Quy trình phát hành phải tạo bằng chứng gắn đúng artifact và giữ nguyên các yêu cầu phản biện, quyền sử dụng và thử đọc của kho.
