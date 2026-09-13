# Rà soát tính nhất quán sau merge, 13 tháng 9 năm 2026

## Phạm vi và trạng thái

Điểm bắt đầu là `main` tại `e28b9a7eca28f70d4fb1e386b73a66c2ca243daf`, sau khi PR #64 được nhập. Lượt này đọc lại 22 đơn vị dành cho độc giả: lời dẫn, 13 chương, lời cuối, bản đồ nguồn và sáu phụ lục. Không viết lại đoạn còn phù hợp chỉ để tạo thêm thay đổi.

Bốn đơn vị cần sửa là Chương 6, Phụ lục C, Phụ lục D và Bản đồ nguồn. README được sửa riêng để người tải sách không nhầm cặp tệp cũ trong `dist` với nội dung mới trong `book/`. Có bổ sung sổ đối chiếu và kiểm tra hồi quy. Phụ lục F, nội dung ba bộ checklist, bản đồ 17 tuệ và bản Markdown gốc không bị viết lại.

Đây là rà soát biên tập có AI hỗ trợ, không phải chứng nhận độc lập. Đọc toàn văn không đồng nghĩa đã kiểm mới mọi mệnh đề trong mọi ấn bản. Metadata, hồ sơ phát hành cũ, quyền sử dụng và các cổng thẩm định bên ngoài được giữ nguyên.

## Sửa đổi có căn cứ

| Vị trí | Vấn đề | Cách sửa |
|---|---|---|
| Chương 6, buồn ngủ | Lời diễn ý P01 bỏ mất bối cảnh nằm xuống để ngủ, dễ bị hiểu thành luôn ngồi chờ ngủ gật. | Khôi phục bối cảnh, nói rõ ghi nhận có thể xua buồn ngủ. Tách lời P01, kinh AN 7.61 và hướng dẫn áp dụng của sách. |
| Chương 6, dấu hiệu bất ổn | “Giảm hay dừng thực hành cường độ cao” có thể bị hiểu là vẫn tiếp tục buổi hiện tại dù có dấu hiệu cần hỗ trợ. | Đồng bộ với Chương 1 và 9: dừng buổi hiện tại, không tăng cường độ, tìm hỗ trợ phù hợp. |
| Phụ lục C, câu 11 | Câu về nghỉ vì sức khỏe quá rộng, chưa phân biệt bệnh thông thường đã hồi phục với dấu hiệu nguy cơ khi hành thiền. | Dẫn về cách khởi động lại của Chương 1 cho gián đoạn thông thường; giữ đường hỗ trợ riêng khi đã dừng vì dấu hiệu nguy cơ. Không bỏ chỉ dẫn điều trị đang có. |
| Phụ lục D | Thẻ “noting”, một từ tiếng Anh, nhận nhãn “THUẬT NGỮ PĀLI” từ hàm dùng chung. | Thêm nhãn tùy chọn cho thẻ, giải nghĩa tiếng Anh tại chỗ; các thẻ Pāli còn lại giữ nhãn đúng của chúng. |
| README | Liên kết tải trỏ vào bản cũ nhưng đoạn giới thiệu có thể khiến người đọc nghĩ đã nhận đủ bản biên tập mới và mọi kiểm tra nội bộ đã đạt. | Nêu rõ mã nguồn và tệp tải chưa đồng bộ; không chuyển kết quả kiểm tra của bản cũ sang bản mới. |

## Nguồn mới và giới hạn

**K54 / C94:** AN 7.61:2–9 theo hệ số SuttaCentral, Pāli trên [Bilara](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/an/an7/an7.61_root-pli-ms.json), được đối chiếu với bản dịch Ṭhānissaro Bhikkhu mang số [AN 7:58, Capala Sutta](https://www.dhammatalks.org/suttas/AN/AN7_58.html). Đã kiểm tra người nói và đoạn hướng dẫn: Đức Phật dạy Tôn giả Moggallāna các cách ứng xử kế tiếp khi cách trước chưa xua buồn ngủ; có cả nằm nghiêng phải, có niệm và ý định thức dậy. Hai địa chỉ dùng hệ đánh số khác nhau. Chương 6 chỉ diễn ý một số cách, không tự nhận đã chép đủ trình tự.

**C95:** đọc lại [P01 tại Aimwell](https://www.aimwell.org/practical.html), Basic Exercise III, các đoạn nằm xuống và ngủ. Không đồng nhất bản HTML đã đọc với bản PDF BPS từng không tải được. Không chuyển chỉ dẫn của Mahāsi thành lời Phật, không biến đoạn chuẩn bị ngủ thành chỉ dẫn chung cho mọi buổi ngồi.

Nghỉ khi thiếu ngủ hoặc kiệt sức, chọn điều chỉnh vừa sức và áp dụng ngưỡng an toàn là hướng dẫn biên soạn. Không gọi các lựa chọn ấy là toàn bộ trình tự kinh, một liều thực hành đã được kiểm chứng, hoặc phác đồ điều trị.

Các mã K01–K53 và C01–C93 được giữ nguyên. K45 vẫn là SN 22.82, K53 vẫn là SN 22.48; ba URL chính thức R10–R11 ở C93 vẫn được giữ đủ. Danh mục mới có 54 mã K và 95 mã C, không trùng.

## Kiểm tra trước bản dựng

- Bảy kiểm tra mới trong `tests/test_post_merge_consistency.py`: đạt trong workspace cục bộ.
- Mười kiểm tra thuộc nhóm `test_source*py`: đạt trong workspace cục bộ.
- Các kiểm tra mới bảo vệ bối cảnh, nhãn, nguồn và giới hạn câu chữ; không chứng minh giáo lý hoặc hiệu quả y khoa bằng máy.
- Bản dựng PDF/EPUB và bộ kiểm tra trên Actions chưa được ghi nhận trong bản báo cáo chuẩn bị này. Kết quả sẽ chỉ được bổ sung từ log và tệp thực tế, không kế thừa kết quả 242 trang của lượt trước.

## Ranh giới phát hành

Chưa thay các tệp theo dõi trong `dist`; chưa cập nhật hồ sơ phát hành cũ. Các điều kiện về phản biện giáo lý, an toàn lâm sàng, thử đọc người mới, ứng dụng đọc EPUB, khả năng tiếp cận và quyền sử dụng vẫn cần bằng chứng riêng. Một bản dựng xem trước không đóng những cổng đó.
