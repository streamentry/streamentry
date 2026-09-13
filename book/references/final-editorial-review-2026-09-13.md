# Rà soát biên tập cuối toàn sách, 13 tháng 9 năm 2026

## Kết luận và trạng thái

Đã hoàn tất lượt biên tập nội bộ cuối và kiểm tra bản đọc thử tích hợp: **242 trang PDF**, EPUB được dựng từ cùng nguồn. Bản này giữ các chỉnh sửa của PR #62–63, các checklist của PR #65 và những sửa đổi cuối trong [PR #64](https://github.com/streamentry/streamentry/pull/64).

**Hoàn tất biên tập không đồng nghĩa đã xác minh phát hành hoặc được thẩm định độc lập.** PR #64 chưa được nhập vào `main`; PDF/EPUB mới không thay các tệp đang theo dõi trong `dist`. Không thay bản Markdown gốc, metadata ấn bản, hồ sơ phát hành cũ hoặc trạng thái thẩm định bên ngoài để làm kết quả kiểm tra thành đạt.

## Phạm vi thực tế

Lượt đầu của PR #64 bắt đầu từ `6eb33b6ca4a6510ee61e12bfd1f6ac277d88d60d`, sau PR #63: đọc lại 21 đơn vị dành cho độc giả và sửa 10 đơn vị. Khi tiếp tục công việc, PR #65 đã thêm Phụ lục F vào `main` tại `62ceb0b14e94807d350919ea1712ee5b3cefe632`. Nhánh `editorial/final-whole-book-polish-20260913` đã nhận các thay đổi ấy trước khi dựng bản cuối.

Bản tích hợp có **22 đơn vị văn bản**: lời dẫn, 13 chương, lời cuối, bản đồ nguồn và 6 phụ lục. Phần tiếp tục đã đọc Phụ lục F, kiểm tra các liên kết và sự nhất quán với phần thân sách; không viết lại những đoạn còn phù hợp chỉ để có thêm thay đổi. Chương 10, Phụ lục F, tệp ghép sách `book/main.typ` và hồ sơ đối chiếu checklist được kiểm tra là giữ nguyên từng byte so với gói nguồn PR #65 đã lấy về.

Đây là công việc biên tập có AI hỗ trợ. Đọc toàn văn và có mã nguồn không chứng minh mọi câu đã được xác minh mới bằng tất cả ấn bản gốc, cũng không thay phản biện độc lập của người có chuyên môn.

## Những sửa đổi về nghĩa và cách diễn đạt

| Phần | Nội dung đã xử lý |
|---|---|
| Chương 2 và 3 | Năm thủ uẩn là các uẩn hữu lậu, có thể bị chấp thủ; không thu nghĩa thành những lúc đang nhận thấy bám víu. Dẫn đúng K53/SN 22.48. |
| Chương 8 | Tách rõ hai lý do không đăng ký: thiếu điều kiện an toàn và hứa bảo đảm đạo quả. Sửa câu phủ định có thể bị đọc ngược thành yêu cầu khóa thiền phải bảo đảm chứng đắc. |
| Chương 9 | Đặt dấu hiệu cấp cứu trước bài tiếp đất hoặc ghi nhãn; không xếp dấu hiệu thần kinh vào mức xanh chỉ vì đã tự hết; làm rõ khi cần dừng buổi hiện tại. |
| Chương 12, tệp `13-tu-dieu-de-van-hanh.typ` | Đồng bộ nghĩa thủ uẩn với SN 22.48 và phân biệt các uẩn với dục, tham đối với chúng trong MN 44. |
| Chương 13, tệp `12-ban-do-tue.typ` | Giữ đủ 17 mục và chiều sâu. Phân biệt tâm thanh tịnh với chú ý thông thường, tuệ thấy đáng sợ với cơn hoảng, nhàm lìa với ly tham, chuyển tộc với đạo. Nhận xét về giới hạn ký ức được tách khỏi điều nguồn trực tiếp nói. |
| Phụ lục D | Thêm nghĩa năm thủ uẩn và nguồn K53; đặt dấu nguồn trước lời giải thích của các mục thuật ngữ. |
| Phụ lục E | Cấp cứu trước ghi nhãn hoặc tiếp đất; liên kết đến đúng cổng an toàn; không tự trở lại mức tập cũ sau dấu hiệu nguy cơ. |
| Lời cuối | Nhắc đủ bốn nhiệm vụ, gồm thực chứng sự chấm dứt khổ; không thu cứu cánh thành một chỉ số hành vi. |
| Bản đồ nguồn và sổ đối chiếu | Sửa xung đột mã do hai nhánh cùng thêm nguồn, giữ toàn bộ nguồn checklist và nguồn bổ sung của lượt cuối. |

Giữ những phân biệt đã sửa ở PR #62–63: kinh với lời đệ tử, luận giải và Mahāsi; SN 45.8 với MN 117; mong muốn thiện lành với tham ái; một trải nghiệm với tiêu chuẩn đạo quả; sự tự biết có điều kiện với việc tự phong từ hiện tượng. Giọng văn khuyến khích nhận biết, trở về và sửa sai, không hạ tiêu chuẩn giáo lý để người đọc dễ tự nhận thành tựu.

## Xử lý xung đột giữa PR #64 và PR #65

Hai nhánh từng dùng K45 cho hai bài khác nhau. Việc chỉ thấy một mã tồn tại sẽ không phát hiện được lỗi dẫn nhầm ấy. Bản tích hợp đã chuẩn hóa:

- **K45 vẫn là SN 22.82**, nguồn của bảng hai mươi cách thân kiến trong Phụ lục F.
- K46–K52 giữ nguyên các nguồn được PR #65 thêm.
- **K53 là SN 22.48**, dùng cho phân biệt năm uẩn và năm thủ uẩn. Đã sửa các chỗ dẫn trong Chương 2, 3, 12 và Phụ lục D.
- C81–C89 giữ nội dung kiểm chứng checklist. Các bổ sung của lượt cuối dùng **C90–C93**; riêng SN 22.48 là C91.

Danh mục có 53 mã K theo thứ tự và sổ đối chiếu có 93 mã C không trùng. Bốn kiểm tra mới trong `tests/test_source_registry_integrity.py` kiểm tra thứ tự, tính duy nhất, liên hệ đúng giữa K45/K53 và hai bài kinh, cùng việc mã được dùng trong văn bản độc giả có mục khai báo. Đây là kiểm tra cấu trúc truy nguồn, không phải chứng minh toàn bộ giáo lý bằng máy.

Việc nhận `main` mới được thực hiện bằng fast-forward nhánh biên tập đến một commit có cả hai nhánh làm cha; không force-push hoặc thay `main`.

## Nguồn đối chiếu và giới hạn

### Năm thủ uẩn

[SN 22.48, bản dịch Ṭhānissaro Bhikkhu](https://www.dhammatalks.org/suttas/SN/SN22_48.html) phân biệt các uẩn với các uẩn hữu lậu, có thể bị chấp thủ. Đọc cùng [MN 44](https://www.dhammatalks.org/suttas/MN/MN44.html) để không đồng nhất các uẩn với dục và tham đối với chúng. [SN 22.82](https://www.dhammatalks.org/suttas/SN/SN22_82.html) là nguồn khác, trình bày các quan hệ chấp tự ngã; không dùng hai mã thay nhau.

### Bản đồ tuệ

Đối chiếu các đoạn then chốt của [The Progress of Insight, Nyanaponika Thera dịch](https://www.accesstoinsight.org/lib/authors/mahasi/progress.html), nhất là tâm thanh tịnh, sợ hãi và chuỗi 12–17. Tác phẩm được giữ ở đúng tầng Mahāsi, không gán danh sách ấy thành lời Phật trực tiếp.

[Bản lưu The Path of Purification](https://archive.org/download/bpscom/BPS%20COM.rar/BPS%20COM%2FBP%20BOOKS%2Fbp207h_The-Path-of-Purification-%28Visuddhimagga%29.pdf) mang thông tin BPS Online Edition 2014, Bhikkhu Ñāṇamoli dịch. Trong lượt cuối đã đối chiếu văn bản XVIII.1–5, XXI.32–33 và XXII.1–11. Đây là kiểm tra các đoạn xác định, không phải kiểm mới toàn tác phẩm. Chưa xác lập tệp lưu đồng nhất từng byte với đường dẫn nhà xuất bản không tải được. Công cụ chụp PDF nguồn trả lỗi; không tuyên bố đã kiểm tra hình thức PDF nguồn. Việc kiểm tra bố cục sách biên tập ở phần dưới là công việc khác.

### An toàn

Các sửa đổi dựa vào [CDC về dấu hiệu đột quỵ](https://www.cdc.gov/stroke/signs-symptoms/index.html), [CDC về nhồi máu cơ tim](https://www.cdc.gov/heart-disease/about/heart-attack.html), [NIMH về psychosis](https://www.nimh.nih.gov/health/publications/understanding-psychosis) và [thông báo chính thức về 112](https://xaydungchinhsach.chinhphu.vn/tong-dai-so-112-tiep-nhan-24-7-cac-thong-tin-ve-su-co-thien-tai-tham-hoa-119250902150528929.htm). Không suy ra bảo đảm thời gian đáp ứng, không coi việc đọc thông báo là kiểm mới mọi văn bản pháp lý và không dùng các trang này thay thẩm định lâm sàng cho toàn sách. Giữ ngày và phạm vi riêng của R11.

## Bản dựng được kiểm tra

- Nhánh: `editorial/final-whole-book-polish-20260913`.
- Head chứa nội dung và kiểm tra: `a9d1581dd38d4af71c6e31d5603b1528c0883ab7`.
- Commit checkout thực tế của Actions: `af7662c3dc4f3d63b8903805de9f501ea392e814`.
- [Editorial preview, run 34744004992](https://github.com/streamentry/streamentry/actions/runs/34744004992).
- Artifact: `10313448522`, tên `editorial-preview-af7662c3dc4f3d63b8903805de9f501ea392e814`.
- Gói chứa source, PDF/EPUB, `build.log`, `tests.log`, `lint.log`, `source-commit.txt` và `SHA256SUMS.txt`. Bản báo cáo hoàn tất này được lưu sau bản dựng; không đổi nội dung sách đã kiểm tra.

| Thuộc tính | Kết quả thực tế |
|---|---|
| PDF | 242 trang A5, 1.844.003 byte |
| PDF SHA-256 | `caf58152289e0ce8ccb961d529d75cc4c4c5f027d905fc152ac21b58c27cef65` |
| EPUB | 250.749 byte; 278 mục điều hướng nội dung theo log bộ dựng |
| EPUB SHA-256 | `c6d06154a389b79cb16ac6723534205a7a3b531df80b168f7d14342dc3c1410f` |
| Bản Markdown gốc SHA-256 | `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440`, không đổi |
| Dựng PDF và EPUB | Thành công; 202 cảnh báo HTML thuộc nhóm bộ dựng hiện có cho phép. Không gọi đây là bản dựng không cảnh báo. |
| Bộ kiểm tra đầy đủ | 231 bài: 230 đạt, 1 lỗi tích hợp hồ sơ phát hành cũ |
| Ruff, compileall, `git diff --check` | Đạt theo `lint.log` của Actions |
| Kiểm tra liên kết EPUB bổ sung | 398 lượt tham chiếu nội bộ, không thiếu tệp/fragment; không trùng ID trong các tài liệu XML đã kiểm |
| Liên kết ngoài EPUB | Có 128 lượt liên kết ngoài; không tuyên bố đã kiểm tra khả năng truy cập mạng của toàn bộ các đích |
| Quét PDF toàn bộ | Không phát hiện hộp chữ vượt biên trang, ký tự thay thế U+FFFD, đích liên kết nội bộ không hợp lệ hoặc trang khác A5 trong phạm vi phép kiểm |

**Lỗi còn lại phải được giữ rõ:** `test_current_release_evidence_matches_dist_artifacts` dừng tại `PDF SHA-256 does not match release evidence`. Nội dung đã thay đổi nhưng hồ sơ phát hành theo dõi tệp cũ. Không bỏ bài kiểm tra, không tự đổi hồ sơ cũ thành chứng cứ cho tệp mới. Bộ xác minh dừng ở hash đầu tiên; không suy ra các cổng phía sau đều đạt hoặc chỉ còn duy nhất một vấn đề phát hành. Workflow xem trước có thể mang trạng thái thất bại do kiểm tra này dù bước dựng và lint đã thành công.

## Kiểm tra hình thức đúng bản 242 trang

Đã tạo và xem tổng quan **toàn bộ 242 trang**, chia thành 11 bảng ảnh. Sau đó xem chi tiết 12 trang PDF: **82, 85, 132, 155, 168, 174, 175, 217, 220, 225, 238 và 242**. Đây là số trang tệp, có tính bìa; số in dưới chân trang có thể khác.

Phạm vi chi tiết gồm cảnh báo chọn khóa thiền, cổng cấp cứu, nghĩa thủ uẩn, các đoạn bản đồ tuệ vừa sửa, bản đồ quyết định, bảng 20 ô, câu hỏi giới cấm thủ, mã K53 và trang góp ý. Không phát hiện chữ chồng, bị cắt hoặc khung vượt trang trong các trang đã xem. Phụ lục E vẫn gọn trong một trang; bảng thân kiến và các câu hỏi mẫu giữ được nguồn liên quan.

Xem ảnh tổng quan không tương đương đọc từng chữ ở độ phóng đại lớn; quét tọa độ không chứng minh trải nghiệm trên mọi máy đọc EPUB, chất lượng đọc bằng screen reader hoặc bản in thực tế. Không chuyển kết quả veraPDF, EPUBCheck, DAISY Ace hoặc thử đọc của một tệp cũ sang các hash trên.

## Những việc chưa được xác nhận

Chưa có phản biện giáo lý độc lập, duyệt an toàn lâm sàng cho toàn sách, kết quả người mới đọc không hỗ trợ, kiểm tra EPUB bằng người dùng trên ứng dụng cụ thể hoặc quyết định quyền sử dụng cho bản này. Chưa hoàn tất xác minh phát hành đối với chính cặp PDF/EPUB mới.

Lượt biên tập kết thúc ở bản có nội dung, nguồn dẫn, checklist và bố cục đã tích hợp như trên. Bước tiếp theo có giá trị là đọc phản biện độc lập và xử lý bộ hồ sơ phát hành cùng đúng artifact, không tiếp tục đổi câu chữ tốt chỉ để gọi thêm một lần nữa là “bản cuối”.
