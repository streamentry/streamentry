# Rà soát tính nhất quán sau merge, 13 tháng 9 năm 2026

## Kết luận và phạm vi

Đã hoàn tất lượt đọc và biên tập nội bộ sau PR #64, từ `main` tại `e28b9a7eca28f70d4fb1e386b73a66c2ca243daf`. Bản đọc thử mới có **243 trang PDF**, EPUB được dựng từ cùng nguồn. Các sửa đổi nằm trong [PR #66](https://github.com/streamentry/streamentry/pull/66), chưa nhập vào `main` và chưa thay các tệp đang theo dõi trong `dist`.

Lượt này đọc lại 22 đơn vị dành cho độc giả: lời dẫn, 13 chương, lời cuối, bản đồ nguồn và sáu phụ lục. Đã sửa có mục tiêu **7 đơn vị**: lời dẫn; Chương 5, 6, 9; Phụ lục C, D; Bản đồ nguồn. README, sổ đối chiếu, báo cáo và các bài kiểm tra được cập nhật riêng. Không viết lại đoạn còn phù hợp chỉ để tạo thêm thay đổi.

Phụ lục F, Chương 10, bản đồ 17 tuệ trong `12-ban-do-tue.typ` và `book/main.typ` giữ nguyên từng byte so với nguồn của bản tích hợp trước. Bản Markdown gốc và `book/edition.json` không đổi. Không rút gọn hoặc thay thế các checklist về ba kiết sử đầu.

Đây là rà soát có AI hỗ trợ, không phải chứng nhận độc lập. Đọc toàn văn không đồng nghĩa đã kiểm mới mọi mệnh đề bằng mọi ấn bản gốc. Metadata, hồ sơ phát hành cũ, quyền sử dụng và các cổng thẩm định bên ngoài được giữ nguyên.

## Các sửa đổi cụ thể

| Vị trí | Vấn đề | Cách sửa |
|---|---|---|
| Chương 6, buồn ngủ | Lời diễn ý P01 bỏ mất bối cảnh nằm xuống để ngủ, dễ bị hiểu thành luôn ngồi chờ ngủ gật. | Khôi phục bối cảnh và khả năng ghi nhận xua buồn ngủ; đặt riêng lời P01, kinh AN 7.61 và ứng dụng biên soạn. |
| Lời dẫn, Chương 5, 6 và FAQ 9 | Câu “giảm hay dừng” có thể làm người đọc tiếp tục buổi hiện tại dù đã gặp dấu hiệu cần hỗ trợ. | Nêu việc dừng buổi hiện tại; không tăng hoặc tiếp tục thực hành cường độ cao; tìm hỗ trợ theo Chương 9. Không biến một dấu hiệu thành tự chẩn đoán. |
| Chương 9 | Tóm tắt và tiêu đề mức vàng chưa rõ bằng chính lời hướng dẫn bên dưới. Liên kết khẩn cấp trỏ về cả ba mức thay vì đúng đoạn cần đọc. | Đồng bộ tóm tắt, tiêu đề và hành động; thêm đích `muc-vang`, `muc-do`; đưa liên kết khẩn cấp đến thẳng mức đỏ. Không thay các tiêu chuẩn cấp cứu đã có. |
| Phụ lục C, cả 13 câu | Nhãn nguồn đứng sau lời giải thích, khiến người đọc chỉ biết tầng nguồn sau khi đọc xong. | Chuyển đủ 14 nhãn lên trước phần tương ứng. Giữ riêng nghiên cứu R01–R02 với hướng dẫn biên soạn trong FAQ 9. |
| Phụ lục C, câu 9 | Có thể bị hiểu là cần chờ người dạy thiền trước khi tìm chăm sóc y tế. | Nói rõ không cần chờ buổi gặp người hướng dẫn; thêm đường dẫn trực tiếp đến mức vàng và trợ giúp khẩn cấp. |
| Phụ lục C, câu 11 | Câu về nghỉ vì sức khỏe quá rộng, chưa phân biệt bệnh thông thường đã hồi phục với dấu hiệu nguy cơ khi hành thiền. | Dẫn về khởi động lại ở Chương 1 cho gián đoạn thông thường; giữ đường hỗ trợ riêng khi đã dừng vì dấu hiệu nguy cơ. Giữ các chỉ dẫn điều trị đang có. |
| Phụ lục D | “Noting”, một từ tiếng Anh, nhận nhãn “THUẬT NGỮ PĀLI” từ hàm dùng chung. | Thêm nhãn tùy chọn, giải nghĩa tiếng Anh tại chỗ; các thẻ Pāli khác giữ nhãn của chúng. |
| README | Liên kết tải trỏ vào bản cũ nhưng lời giới thiệu có thể tạo ấn tượng đã nhận đủ nội dung mới và mọi kiểm tra đều đạt. | Nêu rõ mã nguồn và tệp tải chưa đồng bộ; kết quả kiểm tra chỉ áp dụng cho đúng tệp và phạm vi đã ghi. |

## Nguồn đối chiếu và giới hạn

**K54 / C94:** [AN 7.61:2–9, Pāli trên Bilara](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/an/an7/an7.61_root-pli-ms.json), đối chiếu bản dịch Ṭhānissaro Bhikkhu mang số [AN 7:58, Capala Sutta](https://www.dhammatalks.org/suttas/AN/AN7_58.html). Đã đọc lại đoạn Đức Phật hướng dẫn Tôn giả Moggallāna: khi cách trước chưa xua buồn ngủ, có những cách tiếp theo; có cả nằm nghiêng phải, có niệm, tỉnh giác và ý định thức dậy. Hai địa chỉ dùng hệ đánh số khác nhau. Chương 6 diễn ý chọn lọc, không tự nhận đã chép đủ trình tự.

**C95:** [P01 tại Aimwell](https://www.aimwell.org/practical.html), Basic Exercise III, đoạn nằm xuống và chuẩn bị ngủ. Không đồng nhất bản HTML đã đọc với bản PDF BPS từng không tải được. Không chuyển chỉ dẫn Mahāsi thành lời Phật hoặc biến đoạn chuẩn bị ngủ thành hướng dẫn chung cho mọi buổi ngồi. Các chỉ dẫn Basic Exercise I về ghi nhận trực tiếp, không tụng lặp từ, cũng được đối chiếu khi đọc phần phương pháp.

**R05 và quyết định dừng:** [NIMH, Understanding Psychosis](https://www.nimh.nih.gov/health/publications/understanding-psychosis) nêu các thay đổi về phân biệt thực tại, ngủ, tự chăm sóc và sinh hoạt, cùng việc tìm chăm sóc sức khỏe khi chúng tăng lên hoặc không biến mất. Nguồn không đưa ra một quy trình dừng thiền. Việc thống nhất câu chữ và đường chuyển đến Chương 9 là biên soạn, không phải khuyến cáo nguyên văn của NIMH, chẩn đoán cá nhân hay duyệt lâm sàng độc lập.

Các phân biệt giáo lý đã có về thân kiến, ngã mạn, câu hỏi chân thành và điều kiện đạo quả được đọc đối chiếu trong toàn văn; lượt này không tuyên bố kiểm mới toàn bộ sổ nguồn hoặc toàn bộ Thanh Tịnh Đạo. Nghỉ khi thiếu ngủ, chọn điều chỉnh vừa sức và áp dụng ngưỡng an toàn là hướng dẫn biên soạn, không phải toàn bộ trình tự kinh hoặc một liều thiền đã được kiểm chứng.

K01–K53 và C01–C93 giữ nguyên. K45 vẫn là SN 22.82, K53 vẫn là SN 22.48; ba URL chính thức R10–R11 trong C93 được giữ đủ. Thêm K54, C94–C95; danh mục có 54 mã K và 95 mã C không trùng.

## Bản dựng và nhận diện tệp

- Head chứa văn bản và kiểm tra: `8efdb214c021f56d065e702cd24db1f73de2ed3c`.
- Checkout thực tế trên Actions: `c96fd4efece9dc34fa3a748c05cfa53dae99cc61`.
- [Editorial preview, run 34750283264](https://github.com/streamentry/streamentry/actions/runs/34750283264).
- Artifact `10314929910`, tên `editorial-preview-c96fd4efece9dc34fa3a748c05cfa53dae99cc61`.
- Gói đã tải và đọc gồm source ZIP, hai tệp sách, `build.log`, `tests.log`, `lint.log`, `source-commit.txt` và `SHA256SUMS.txt`.
- Sáu tệp của commit hoàn tất, gồm bốn phần văn bản và hai tệp kiểm tra, khớp từng byte với source ZIP của Actions. Các sửa đổi K54, C94–C95, README và thuật ngữ của commit trước được giữ nguyên.
- Commit chứa bản báo cáo hoàn tất này không thay văn bản sách, công cụ hoặc artifact đã được kiểm tra.

| Thuộc tính | Kết quả thực tế |
|---|---|
| PDF | 243 trang A5; 1.851.993 byte |
| PDF SHA-256 | `eaeea4724472bf9e9f2797cef085f8f38892f6eb02eb2bfda6e1de08a712627f` |
| EPUB | 251.483 byte; 278 mục điều hướng nội dung theo log bộ dựng |
| EPUB SHA-256 | `ff7d92c20d771399ad7e1b64b05d64db253a4f162f6364c51fedad89e82b8a79` |
| Markdown gốc SHA-256 | `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440` |
| Dựng PDF và EPUB | Thành công; 201 cảnh báo HTML thuộc nhóm bộ dựng hiện có cho phép. Không gọi là không có cảnh báo. |
| Bộ kiểm tra đầy đủ trên Actions | 244 bài: 243 đạt, 1 lỗi hồ sơ phát hành cũ |
| Ruff, compileall, `git diff --check` | Đạt theo `lint.log` của bản dựng nêu trên |
| Kiểm tra EPUB bổ sung | 409 tham chiếu nội bộ, gồm 403 trong book/nav và 6 tham chiếu tài nguyên/gói; không thiếu tệp hoặc fragment, không trùng ID trong các XML đã kiểm |
| Liên kết ngoài EPUB | 129 lượt; không kiểm tra lại khả năng truy cập mạng của mọi đích |
| Quét toàn PDF | Không phát hiện hộp chữ vượt biên trang, ký tự thay thế U+FFFD, trang khác A5 hoặc đích không hợp lệ trong 35 liên kết GoTo được trích xuất |

## Kiểm tra hình thức và hồi quy

Đã xem ảnh tổng quan của toàn bộ 243 trang. Đã xem riêng ảnh chi tiết các trang PDF **7, 56, 61, 88, 89, 198, 199, 215, 238 và 243**: hướng dẫn dừng, buồn ngủ, mức vàng/đỏ, nhãn nguồn FAQ, khởi động lại, nhãn tiếng Anh, nguồn K54 và trang góp ý. Không thấy chữ bị cắt hoặc chồng lấn trong các trang được xem. Các khoảng trống do giữ nguyên khối thẻ vẫn còn; không coi ảnh tổng quan là kiểm từng chữ ở mọi cỡ phóng đại hoặc một lần thử in.

Bảy bài trong `test_post_merge_consistency.py` và sáu bài mới trong `test_post_merge_proofread.py` bảo vệ bối cảnh, nhãn, nguồn, đích điều hướng và quyết định dừng. Mười bài thuộc `test_source*py` và năm bài trong `test_final_editorial_contract.py` cũng được chạy cục bộ, đều đạt. Các kiểm tra này ngăn lỗi cấu trúc/câu chữ quay lại, không chứng minh giáo lý hay hiệu quả lâm sàng bằng máy.

## Lỗi còn mở và ranh giới phát hành

`test_current_release_evidence_matches_dist_artifacts` dừng tại **`PDF SHA-256 does not match release evidence`**. Đây là hồ sơ đang gắn với tệp phát hành cũ, trong khi kiểm tra xem trước đã dựng tệp mới. Không bỏ bài kiểm tra hoặc đổi kết quả cũ thành bằng chứng cho bản này. Bộ xác minh dừng ở hash đầu tiên, nên không suy ra các cổng phía sau đã đạt.

[Publication CI, run 34750283265](https://github.com/streamentry/streamentry/actions/runs/34750283265), job `103705479156`, dừng ở **Install pinned test dependencies**; các bước xác minh định dạng phía sau bị bỏ qua. Vì thế, không gọi toàn bộ CI là xanh. Không thay workflow, dependency hoặc bảo vệ nhánh trong lượt sửa câu chữ này.

Chưa thay `dist`, metadata, hồ sơ phát hành hoặc trạng thái thẩm định bên ngoài. Còn cần phản biện độc lập về giáo lý và an toàn, thử đọc người mới, thử ứng dụng EPUB/khả năng tiếp cận và xác lập quyền sử dụng. Bản này là **bản chốt của lượt biên tập nội bộ để đọc phản biện**, không phải chứng nhận mọi câu tuyệt đối đúng hoặc bản phát hành đã được xác minh đầy đủ.
