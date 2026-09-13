# Rà soát biên tập cuối toàn sách, 13 tháng 9 năm 2026

## Phạm vi và trạng thái

Lượt này bắt đầu từ `6eb33b6ca4a6510ee61e12bfd1f6ac277d88d60d`, sau khi PR #63 đã được nhập vào main. Nhánh làm việc: `editorial/final-whole-book-polish-20260913`.

Đã đọc lại 21 đơn vị dành cho độc giả: lời dẫn, 13 chương, lời cuối, bản đồ nguồn và 5 phụ lục. Sửa 10 đơn vị, giữ những phần còn phù hợp thay vì viết lại chỉ để đổi văn phong. Ngoài ra cập nhật sổ nguồn, một tệp kiểm tra hiện có và thêm năm kiểm tra hồi quy.

Đây là lượt biên tập nội bộ có AI hỗ trợ. Không phải thẩm định độc lập, xác nhận đạo quả, duyệt y khoa, thử nghiệm người đọc hoặc quyết định về quyền phát hành. Đọc toàn văn không đồng nghĩa đã xác minh mới từng câu bằng tất cả ấn bản gốc.

Không thay bản Markdown gốc, metadata ấn bản, hồ sơ phát hành cũ, trạng thái các cổng thẩm định hoặc PDF/EPUB trong `dist`. Bản dựng mới dùng để đọc thử và kiểm tra, không kế thừa kết quả chứng nhận của một tệp cũ.

## Nội dung đã sửa

| Phần | Sửa đổi có ý nghĩa |
|---|---|
| Chương 2 và 3 | Làm rõ năm thủ uẩn là các uẩn hữu lậu, có thể bị chấp thủ, không chỉ lúc đang nhận thấy bám víu; dẫn K45 |
| Chương 8 | Sửa câu có thể đọc ngược thành yêu cầu khóa thiền phải bảo đảm đạo quả; tách rõ thiếu quy trình an toàn với đưa ra bảo đảm chứng đắc |
| Chương 9 | Đưa cổng cấp cứu lên trước bài tiếp đất; loại dấu hiệu cấp cứu khỏi mức xanh dù thoáng qua; làm rõ mức vàng cần dừng buổi hiện tại; lời văn ít quy kết hơn |
| Chương 12, tệp `13-tu-dieu-de-van-hanh.typ` | Đồng bộ nghĩa thủ uẩn với SN 22.48 và phân biệt chúng với dục, tham đối với chúng trong MN 44 |
| Chương 13, tệp `12-ban-do-tue.typ` | Giữ đủ 17 mục và chiều sâu; đối chiếu lại tâm thanh tịnh, tuệ đáng sợ, nhàm lìa/ly tham và chuyển tộc/đạo; tách nhận xét về giới hạn ký ức khỏi lời nguồn |
| Phụ lục D | Thêm mục năm thủ uẩn; đặt dấu nguồn trước lời giải thích để dễ nhận ranh giới |
| Phụ lục E | Cấp cứu trước ghi nhãn hoặc tiếp đất; liên kết đến cổng an toàn đầu chương; không tự trở lại mức tập cũ sau dấu hiệu nguy cơ |
| Lời cuối | Nhắc đủ bốn nhiệm vụ, gồm thực chứng sự chấm dứt khổ |
| Bản đồ nguồn | Bổ sung K45; ghi rõ bản lưu V01 và những đoạn được đối chiếu; không khẳng định toàn ấn bản đã được kiểm mới |

Các phần giữ nguyên sau khi đọc: lời dẫn, Chương 1, 4, 5, 6, 7, 10, 11 và Phụ lục A, B, C. Giữ những phân biệt đã sửa ở PR #62–63: kinh với luận giải và Mahāsi; SN 45.8 với MN 117; mong muốn thiện lành với tham ái; một trải nghiệm với tiêu chuẩn đạo quả; sự tự biết có điều kiện với tự phong từ hiện tượng.

## Đối chiếu nguồn then chốt

### Năm thủ uẩn

- [SN 22.48, Ṭhānissaro Bhikkhu](https://www.dhammatalks.org/suttas/SN/SN22_48.html): các thủ uẩn hữu lậu và có thể bị chấp thủ.
- [MN 44](https://www.dhammatalks.org/suttas/MN/MN44.html): đọc cùng để không đồng nhất các uẩn với dục và tham đối với chúng.
- Thêm K45 trong danh mục độc giả và C82 trong sổ nguồn.

### Bản đồ tuệ, nguồn về sau

- [The Progress of Insight, Nyanaponika Thera dịch](https://www.accesstoinsight.org/lib/authors/mahasi/progress.html): đọc các phần về tâm thanh tịnh, sợ hãi và chuỗi 12–17; giữ đúng phạm vi truyền thống Mahāsi.
- [Bản lưu The Path of Purification](https://archive.org/download/bpscom/BPS%20COM.rar/BPS%20COM%2FBP%20BOOKS%2Fbp207h_The-Path-of-Purification-%28Visuddhimagga%29.pdf): có thông tin BPS Online Edition 2014, Bhikkhu Ñāṇamoli dịch. Đã đối chiếu văn bản XVIII.1–5, XXI.32–33 và XXII.1–11; không coi đó là đọc kiểm mới toàn bộ tác phẩm. Không xác lập tệp này đồng nhất từng byte với đường dẫn nhà xuất bản không tải được. Công cụ chụp trang trả lỗi, nên không tuyên bố kiểm tra hình thức PDF nguồn.
- [SN 22.59](https://www.dhammatalks.org/suttas/SN/SN22_59.html): giữ nhàm lìa và ly tham là những từ có quan hệ trong mạch giải thoát, không coi đồng nghĩa hoàn toàn.
- V01 và P02 được dẫn riêng cho các mệnh đề thực sự thuộc từng nguồn. Việc hồi tưởng một khoảng trống không đủ xác định từng sát-na là giới hạn suy luận của sách, không phải phép đo đã được các nguồn kiểm chứng.

### An toàn

- [CDC, dấu hiệu đột quỵ](https://www.cdc.gov/stroke/signs-symptoms/index.html): dấu hiệu đột ngột, không tự lái xe và triệu chứng tự hết không loại nhu cầu đánh giá khẩn.
- [CDC, nhồi máu cơ tim](https://www.cdc.gov/heart-disease/about/heart-attack.html): các dấu hiệu cần gọi cấp cứu.
- [NIMH, Understanding Psychosis](https://www.nimh.nih.gov/health/publications/understanding-psychosis): suy giảm chức năng, nhận biết thực tại và nhu cầu được đánh giá.
- [Thông báo chính thức về 112](https://xaydungchinhsach.chinhphu.vn/tong-dai-so-112-tiep-nhan-24-7-cac-thong-tin-ve-su-co-thien-tai-tham-hoa-119250902150528929.htm): đọc lại phạm vi đầu số; không có bảo đảm đáp ứng và không coi đây là kiểm mới mọi văn bản pháp lý sau đó. Giữ ngày và phạm vi riêng của R11.

## Kiểm tra trước bản dựng

- Năm kiểm tra mới trong `test_final_editorial_contract.py`: đạt tại bản làm việc.
- Sáu kiểm tra mã nguồn và 18 kiểm tra hợp đồng nội dung chương: đạt tại bản làm việc. Tổng cộng 29 kiểm tra chọn lọc.
- Python compileall: đạt tại bản làm việc.
- Bản Markdown gốc giữ SHA-256 `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440`.
- Chưa ghi kết quả bộ kiểm tra đầy đủ hoặc bản dựng mới tại thời điểm tạo báo cáo này. Những kết quả ấy chỉ được bổ sung từ log và artifact thực tế; không lấy kết quả bản 227 trang trước đó làm kết quả lượt này.

## Điều kiện kết thúc lượt biên tập

Chốt nội dung sau khi sửa các lỗi đã xác định, dựng lại và kiểm tra bản đọc thử. Không tiếp tục viết lại những đoạn tốt chỉ để có thêm thay đổi. Những việc cần con người độc lập, như phản biện giáo lý, an toàn lâm sàng, thử đọc, ứng dụng EPUB và quyền sử dụng, vẫn là các công việc riêng trước phát hành; một lượt AI tự rà nữa không thay được chúng.
