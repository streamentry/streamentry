# Rà soát lời văn và căn cứ Nikāya — 2026-09-13

## Trạng thái và phạm vi

Đây là bản ghi **biên tập nội bộ, chưa phải chứng nhận giáo lý hay bản phát hành**. Yêu cầu của người biên soạn: lời văn nhu nhuyến, dễ hiểu, có sức thuyết phục nhưng bám sát lời Phật.

- Bản nền: `9fb37506122144c74cb4a9e03abe260ed81a2f13` trên `main`.
- Nhánh: `editorial/nikaya-gentle-prose-20260913`.
- Đã đọc cấu trúc sách và các quy định nguồn; đã biên tập sáu tệp nội dung dưới đây.
- Chưa kiểm chứng từng mệnh đề của toàn bộ sách. Không được diễn đạt kết quả này thành “mọi ý trong toàn sách đã được xác nhận”.

| Tệp đã biên tập | Công việc chính |
|---|---|
| `book/chapters/00-frontmatter.typ` | Mở đầu gần gũi; giải thích nguồn Nikāya, phương pháp Mahāsi và phần biên soạn; giữ lối đọc và đường dẫn an toàn. |
| `book/chapters/02-dich-den-va-nen-tang.typ` | Viết lại phần nền tảng; sửa dẫn nguồn SN 56.11 và chánh nghiệp; phân biệt các nhiệm vụ, điều kiện, phẩm chất và thành tựu. |
| `book/chapters/03-tu-niem-xu-trong-kinh.typ` | Bỏ lời suy đoán về dụng ý sắp xếp của Đức Phật; sửa mô tả bộ phận thân; tách văn bản kinh khỏi giải thích và ví dụ. |
| `book/chapters/06-trien-cai-giac-chi.typ` | Giải thích trở ngại bằng giọng không kết án; phân biệt điều kinh nêu và cách áp dụng; giữ ngưỡng dừng và hỗ trợ sức khỏe. |
| `book/chapters/08-lo-trinh-thay-khoa-thien.typ` | Đặt lịch tháng đúng tầng biên soạn; giữ ranh giới MN 10 về bảy ngày; làm rõ tiêu chí chọn nơi thực hành và người hướng dẫn. |
| `book/chapters/loi-cuoi.typ` | Khuyến khích bước thực hành cụ thể mà không thu giải thoát thành sự dễ chịu hay một bảng điểm đạo đức. |

Không sửa bản Markdown gốc, danh tính ấn bản, các đoạn kiểm chứng chứng đắc đã đóng băng, chính sách biên tập, dữ liệu người đọc, hồ sơ quyền sử dụng hay tệp PDF/EPUB phát hành.

## Nhận xét chính

Bản nền có ưu điểm quan trọng: phân tầng nguồn và giữ nhiều giới hạn về chứng đắc, an toàn. Vấn đề không chỉ là câu dài hoặc nhiều thuật ngữ. Có đoạn mang dấu `KINH` nhưng ghép cả lời bình hiện đại vào cùng khối; người đọc dễ hiểu lời bình ấy là nội dung trực tiếp của nguồn.

Giọng văn cũng thường mở bằng một lời phủ định mạnh, chẳng hạn “không phải huy chương”, “không phải giấy chứng nhận”, “không phải lễ phong cấp”. Một số cảnh báo cần thiết, nhưng sự lặp lại có thể khiến người mới cảm thấy mình đang bị sửa lỗi trước khi được giúp hiểu. Hướng sửa là **nêu điều cần học trước, rồi đặt giới hạn cụ thể**, không bỏ giới hạn.

MN 58 là căn cứ tham khảo cho cách biên tập: lời chân thật, có ích và được nói đúng lúc không đồng nghĩa với chỉ nói điều người nghe thích. Việc vận dụng nguyên tắc đó vào viết sách là lựa chọn biên tập, không phải quy trình viết sách do MN 58 quy định.

Nguồn: [MN 58, bản dịch Ṭhānissaro Bhikkhu, phần lời nói chân thật/có ích/đúng thời](https://www.dhammatalks.org/suttas/MN/MN58.html).

## Các đối chiếu nguồn cụ thể

### 1. MN 10 và số bộ phận thân

Bản nền Chương 3 viết “ba mươi hai phần thân” trong khối gắn MN 10. Danh sách Pāli tại `mn10:10.2` của ấn bản Mahāsaṅgīti trên SuttaCentral được đọc trong lượt này có 31 mục, không có não. Bản sửa dùng **“các bộ phận của thân”** để mô tả đúng phạm vi bài kinh mà không đưa một con số thuộc danh sách khác vào nguồn này.

Không suy từ đây rằng truyền thống Phật giáo không có danh sách 32 phần thân.

Nguồn: [Pāli MN 10, `mn10:10.2`](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/mn/mn10_root-pli-ms.json).

### 2. SN 45.8 và MN 117 không dùng cùng một từ ở chánh nghiệp

Bản Pāli SN 45.8:6.2 đã đọc dùng `abrahmacariyā veramaṇī`; bản Sujato tương ứng dùng “unchastity”. MN 117:25.2 dùng `kāmesumicchācārā veramaṇī`, từ bỏ tà hạnh trong dục. Hai cách diễn đạt không được âm thầm thay cho nhau trong một lời diễn ý mang nguồn duy nhất SN 45.8.

Chương 2 nay dẫn **K23 · MN 117:25.2** cho dòng chánh nghiệp dành cho phần hướng dẫn cư sĩ, đồng thời nêu khác biệt với **K25 · SN 45.8**. Không biến giới kiêng quan hệ tình dục trong một bản kinh thành yêu cầu thường nhật của mọi cư sĩ mà không giải thích ngữ cảnh.

Nguồn:
- [Pāli SN 45.8, `sn45.8:6.2`](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/sn/sn45/sn45.8_root-pli-ms.json), blob `f114637d34c6054d03c83481be56cb03593be8d5`.
- [Sujato, SN 45.8, cùng đoạn](https://github.com/suttacentral/bilara-data/blob/published/translation/en/sujato/sutta/sn/sn45/sn45.8_translation-en-sujato.json), blob `62fd19a5b2b74d72447dc74c2a34e87e41dada00`.
- [Pāli MN 117, `mn117:23–27`](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/mn/mn117_root-pli-ms.json), blob `8c49c05c9f78200da4c7930e51b31d7935ce7d55`.

### 3. SN 56.11: theo đúng danh sách và nhiệm vụ của đoạn dẫn

Chương 2 trước đây bỏ “bệnh” nhưng đưa “sầu, bi, đau, ưu, não” vào câu diễn ý riêng cho SN 56.11. Bản sửa theo `sn56.11:4.2` đã đối chiếu: sinh, già, bệnh, chết; gặp điều không ưa; xa điều yêu; không được điều mong muốn; năm thủ uẩn.

Bốn nhiệm vụ vẫn được giữ: hiểu trọn khổ, từ bỏ nguồn gốc, chứng ngộ sự chấm dứt, tu tập con đường. Các ví dụ công việc không được dùng để đổi Niết-bàn thành một lúc phản ứng lắng xuống, hay đổi phi hữu ái thành mọi mong muốn hết khó chịu.

Nguồn: [Pāli SN 56.11, `4.1–4.10` và `5–10`](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/sn/sn56/sn56.11_root-pli-ms.json).

### 4. Người nói trong MN 44

Phần giải thích thân kiến nay gọi đúng Tỷ-kheo-ni Dhammadinnā là người trả lời, và nêu việc Đức Phật xác nhận lời giải thích ở cuối bài. Dấu `KINH` không đồng nghĩa mọi câu trong một bài kinh đều do Đức Phật trực tiếp nói.

Nguồn: [MN 44, cuộc đối thoại và lời xác nhận ở cuối, bản dịch Ṭhānissaro Bhikkhu](https://www.dhammatalks.org/suttas/MN/MN44.html).

### 5. Trở ngại, giác chi và giới hạn của ứng dụng

Chương 6 phân biệt lời kinh về điều nuôi tham dục, sân và hoài nghi với các ứng dụng đặt điện thoại xuống, điều chỉnh tư thế, khởi lời nguyện hoặc xin lỗi. Các ứng dụng mang dấu `BIÊN SOẠN`, không trở thành câu lệnh trực tiếp của SN 46.51.

Đã đối chiếu Pāli `sn46.51:13–17`, trong đó `14.2` có `mettācetovimutti`. Với SN 46.53, giữ khác biệt giữa nhóm nâng tâm trì trệ và nhóm làm lắng tâm xao động; không diễn thành việc bỏ hẳn một nhóm giác chi khỏi con đường.

Nguồn:
- [Pāli SN 46.51](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/sn/sn46/sn46.51_root-pli-ms.json), blob `612ed5b26bbbfeb54d76bd465033684b497a05b8`.
- [SN 46.53, bản dịch Ṭhānissaro Bhikkhu](https://www.dhammatalks.org/suttas/SN/SN46_53.html).
- [Pāli AN 10.1](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/an/an10/an10.1_root-pli-ms.json), blob `4a1ceb022de318c65426ffa479260efcf48d0074`.

### 6. Không sửa sự thận trọng thành phủ nhận nội dung kinh

Chương 2 nói rõ giới hạn của sách trong việc xác nhận thánh quả, nhưng không biến giới hạn ấy thành kết luận kinh cấm mọi sự tự biết hoặc tự tuyên bố. AN 10.92 có nêu tự tuyên bố khi các điều kiện được bài kinh trình bày đã đầy đủ. Chương 8 vì vậy phân biệt lời tự xưng với hành vi dùng danh hiệu để đòi lệ thuộc, trục lợi hoặc né trách nhiệm.

MN 10 ở đoạn bảy ngày nêu chánh trí hiện tại hoặc Bất lai; không phải lời bảo đảm Nhập lưu cho người tham dự một khóa hiện đại.

Nguồn: [AN 10.92](https://www.dhammatalks.org/suttas/AN/AN10_92.html); [MN 10, phần kết](https://www.dhammatalks.org/suttas/MN/MN10.html); [SN 55.5](https://www.dhammatalks.org/suttas/SN/SN55_5.html).

## Quy tắc lời văn dùng cho các lượt tiếp theo

1. Giải thích điều người đọc cần hiểu trước khi cảnh báo điều không được suy ra. Cảnh báo vẫn phải đặt trước hành động có nguy cơ.
2. Chỉ gắn `KINH` cho mệnh đề được nguồn trực tiếp nâng đỡ. Tách ví dụ, so sánh, cách hỏi và lịch tập sang `BIÊN SOẠN`.
3. Không suy đoán dụng ý Đức Phật để giải thích thứ tự một bài kinh, trừ khi có căn cứ cụ thể.
4. Không làm lời văn “thuyết phục” bằng cách tăng độ chắc chắn, hứa chứng quả hoặc bỏ các phần khó tin như tái sinh ra khỏi nội dung kinh. Trình bày đúng tầng bằng chứng.
5. Không biến pháp học thành tâm lý học thuần túy, việc làm lành thành bằng chứng đắc quả, hay một trạng thái tâm thành chẩn đoán bệnh.
6. Giữ lời mời thực hành cụ thể và vừa sức; giảm ẩn dụ trách móc, lời kết án người đọc và cảnh báo trùng lặp không thêm quyết định mới.
7. Một đoạn dễ đọc chưa tự động là một đoạn đã được người mới đọc hiểu. Cần kiểm chứng bằng việc người đọc tự kể lại đúng ý.

## Những việc còn mở, không được ghi là đã xong

**Đối chiếu xuyên sách:** tìm kiếm bản nền đã chỉ ra `book/chapters/13-tu-dieu-de-van-hanh.typ` cũng có đoạn định nghĩa tám chi gắn riêng SN 45.8. Tệp này chưa được sửa trong lượt hiện tại. Cần kiểm tra và đồng bộ cách dẫn chánh nghiệp với Chương 2 trước khi coi đợt sửa nguồn đã hoàn tất. Đây là việc còn mở có địa chỉ cụ thể, không phải xác nhận đã rà soát đầy đủ chương đó.

**Phạm vi còn lại:** các chương 1, 4, 5, 7, 9, 10, 11, bản đồ tuệ, chương tổng hợp Tứ Diệu Đế và các phụ lục chưa được biên tập từng câu trong lượt này. Không chuyển các đánh giá nội bộ cũ thành bằng chứng cho bản văn mới. Không rút ngắn các phần ba kiết sử và bản đồ tuệ bằng cách bỏ các phân biệt đã được thiết kế cho người mới.

**Nguồn ngoài Nikāya:** các mô tả P01 được giữ theo bản nền ở Chương 6 và 8; lượt này không kiểm chứng lại toàn bộ sách Mahāsi hay Thanh Tịnh Đạo. Phần an toàn vẫn là hướng dẫn hiện đại; không có chứng nhận chuyên môn mới. Đã tham khảo thêm [NCCIH: Meditation and Mindfulness — Effectiveness and Safety](https://www.nccih.nih.gov/health/meditation-and-mindfulness-effectiveness-and-safety) cho ranh giới không dùng thiền thay việc chăm sóc sức khỏe, không dùng nguồn này xác nhận giáo lý.

**Kiểm tra xuất bản:** đã kiểm tra danh sách tệp thay đổi so với commit nền: sáu tệp nội dung, không có thay đổi ngoài ý định tại thời điểm tạo báo cáo. Chưa chạy biên dịch Typst, kiểm tra PDF/EPUB, kiểm tra liên kết sau dựng, kiểm tra khả năng tiếp cận, kiểm thử người đọc mới hay thẩm định giáo lý độc lập. Chưa làm mới các số trang, mã băm hoặc bằng chứng phát hành.

Trước khi phát hành cần giải quyết các đối chiếu xuyên chương, dựng lại theo môi trường được ghim của dự án, chạy `python3 scripts/build-epub.py` và `python3 scripts/verify_release.py`, kiểm tra bản dựng bằng mắt và cập nhật hồ sơ tương ứng. Không thay mã băm hoặc kết quả kiểm tra chỉ để làm cho trạng thái trông đạt. Giữ nhánh ở trạng thái bản biên tập; chưa nhập `main` hay thay PDF/EPUB công khai.
