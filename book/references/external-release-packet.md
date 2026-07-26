# Gói bàn giao phát hành và thẩm định bên ngoài

Checked: 2026-07-27

Đây là điểm bắt đầu duy nhất cho người điều phối quyền phát hành, phản biện chuyên môn và thử nghiệm người đọc của *Hướng Đến Nhập Lưu*. Gói này gom các yêu cầu rải rác thành sáu quyết định có thể kiểm toán. Bản thân gói tài liệu không làm cho bất kỳ cổng nào được thông qua.

Trạng thái chính thức nằm trong [`external-release-gates.json`](external-release-gates.json). Lệnh `python3 scripts/verify_release.py` kiểm tra sổ đăng ký, dấu vân tay của các giao thức, trạng thái tóm tắt trong `release-evidence.md` và hai tệp PDF/EPUB. Nếu ai đó đổi `open` thành `passed` mà không nộp bằng chứng gắn với đúng tệp phát hành, trình kiểm tra sẽ báo lỗi.

## 1. Khóa đúng ứng viên trước khi giao việc

Người điều phối phải ghi vào từng phiếu phân công:

- repository: `https://github.com/streamentry/streamentry`;
- full Git commit gồm 40 ký tự;
- PDF SHA-256, EPUB SHA-256 và số trang PDF lấy từ [`release-evidence.md`](release-evidence.md);
- ngày bắt đầu và thời hạn;
- người nhận việc, phạm vi, xung đột lợi ích và kênh trả hồ sơ;
- phạm vi được phép công bố tên, tư cách, nhận xét và báo cáo của người phản biện.

Trước khi gửi tệp:

```sh
git fetch origin main
git switch --detach <candidate-commit>
git status --porcelain
python3 scripts/verify_release.py
```

`git status --porcelain` không được trả về dòng nào. Không chép mã băm từ email, tin nhắn hay tên tệp. Chỉ dùng mã băm mà trình kiểm tra đọc từ bản checkout sạch.

## 2. Sáu cổng, sáu loại bằng chứng theo vai trò

| Cổng | Câu hỏi phải được quyết định | Giao thức hoặc biểu mẫu | Bằng chứng công khai tối thiểu | Câu được phép nói khi qua |
|---|---|---|---|---|
| `redistribution_rights` | Ai có quyền cho phép phát hành, ở định dạng và kênh nào? | [`rights-decision-template.md`](rights-decision-template.md) | Một quyết định ký tên với vai trò `rights_decision`, nêu căn cứ thẩm quyền, phạm vi PDF và EPUB, điều kiện và vật liệu bên thứ ba | Chỉ phạm vi phân phối được văn bản cho phép |
| `doctrinal_review` | Các tuyên bố Theravāda có đúng nguồn, đúng tầng và đúng giới hạn không? | [`doctrinal-review-protocol.md`](doctrinal-review-protocol.md) | Một báo cáo có vai trò `doctrinal_review_report`, có tên, năng lực công khai, phạm vi, phát hiện và kết quả kiểm tra lại; không còn lỗi `blocking` hoặc `major` | “Được phản biện độc lập về giáo lý” chỉ trong đúng phạm vi đã ký |
| `clinical_safety_review` | Khuyến nghị an toàn, y khoa và giới hạn nghiên cứu có phù hợp không? | [`clinical-safety-review-protocol.md`](clinical-safety-review-protocol.md) | Ít nhất một báo cáo có vai trò `clinical_safety_review_report`; có thể có nhiều báo cáo nếu cần để bao phủ sức khỏe tâm thần, thuốc, nguy cơ cấp thời và các giới hạn phương pháp | “Được phản biện độc lập về an toàn lâm sàng” trong đúng phạm vi đã ký |
| `beginner_cohort` | Năm người mới đầu tiên có tự tìm và dùng đúng sách không? | [`beginner-validation-protocol.md`](beginner-validation-protocol.md) và [`beginner-reader-kit.md`](beginner-reader-kit.md) | Bốn tệp công khai riêng biệt với bốn vai trò bắt buộc: `aggregate_report`, `preregistration_receipt`, `public_history_confirmation`, `privacy_review_confirmation` | “Đúng ứng viên này đã qua cổng năm người mới theo giao thức đã định” |
| `epub_reader_app` | EPUB có dùng được trong ứng dụng đọc thật ở cỡ chữ 150% và chế độ tối không? | Phần EPUB trong [`beginner-reader-kit.md`](beginner-reader-kit.md) | Một báo cáo môi trường EPUB với vai trò `reader_app_report`, nêu ứng dụng, phiên bản, loại thiết bị, cỡ chữ, chế độ tối, hai tác vụ lặp lại, tám kiểm tra hiển thị và các lỗi còn mở | “Đã qua cổng thử nghiệm bằng ứng dụng đọc đã ghi” |
| `comparative_evidence` | Ứng viên có tốt hơn các ấn bản được nêu trong lần sử dụng đầu tiên theo tiêu chí đã đăng ký trước không? | [`comparative-beginner-protocol.md`](comparative-beginner-protocol.md) | Hai tệp công khai riêng biệt với hai vai trò bắt buộc: `preregistration_receipt` và `comparative_results` | Chỉ kết luận hẹp về nhóm thử, dân số và kết quả đã đo |

Không cổng nào thay thế cổng khác. Quyền phát hành không chứng minh đúng giáo lý. Một báo cáo giáo lý không chứng minh an toàn lâm sàng. Một nhóm thử năm người không chứng minh ưu thế thị trường.

## 3. Phiếu phân công chung

Sao chép khối sau vào phiếu phân công riêng cho từng vai trò:

```text
Packet ID:
Gate ID:
Candidate commit:
PDF SHA-256:
EPUB SHA-256:
PDF pages:
Decision requested:
Reviewer or decision-maker:
Public qualifications or authority evidence:
Declared competence scope:
Conflicts:
Compensation and payer:
Start date:
Deadline:
Expected output:
Private return route:
Urgent escalation route:
May publish name and qualifications: yes | no | conditional
May publish findings/report: yes | no | conditional
Out-of-scope topics:
```

Không ghi địa chỉ, số điện thoại, email riêng hoặc dữ liệu người tham gia vào tệp công khai. Người điều phối giữ kênh liên hệ riêng bên ngoài kho mã.

## 4. Quyền phát hành

Người ký phải có thẩm quyền pháp lý đối với đúng tác phẩm hoặc nêu rõ thẩm quyền chưa xác lập. GitHub public không phải giấy phép. Dẫn nguồn không phải quyền tái phân phối.

Dùng [`rights-decision-template.md`](rights-decision-template.md) để:

1. xác định người hoặc pháp nhân đứng sau bút danh và chuỗi quyền của từng người đóng góp;
2. tách quyền đối với bản thảo, bản biên tập, mã nguồn, phông chữ, bản dịch, trích dẫn và tài sản bên thứ ba;
3. quyết định riêng cho kho mã nguồn, PDF, EPUB, bản in, việc bán thương mại, bản dịch, bản nói và các bản tiếp cận;
4. ghi rõ lãnh thổ, thời hạn, tính độc quyền, ghi công, hạn chế và cách xử lý phiên bản mới;
5. ký quyết định gắn với commit và mã băm của hai tệp phát hành.

Nếu thẩm quyền, ngoại lệ trích dẫn hoặc điều kiện giấy phép không rõ, trạng thái vẫn là `open`. Biểu mẫu này là hồ sơ quyết định, không thay thế tư vấn pháp lý theo thẩm quyền áp dụng.

## 5. Phản biện giáo lý

Gửi PDF, EPUB, sổ tuyên bố, bản đồ nguồn và [`doctrinal-review-protocol.md`](doctrinal-review-protocol.md). Người phản biện phải trả:

- thông tin năng lực và xung đột;
- mười kiểm tra bắt buộc về tầng nguồn;
- toàn bộ đoạn ưu tiên;
- một bản ghi cho mỗi phát hiện;
- kết luận xử lý sau khi sửa;
- báo cáo có chữ ký, gắn với commit và mã băm của các tệp phát hành.

Một review hẹp phải tạo ra câu mô tả hẹp. Không dùng uy tín chức danh để mở rộng phạm vi người ấy thật sự đã kiểm.

## 6. Phản biện an toàn lâm sàng

Gửi các chương, appendix, source map và protocol được nêu tại [`clinical-safety-review-protocol.md`](clinical-safety-review-protocol.md).

Không mặc định một người đủ năng lực bao phủ mọi miền. Nếu năng lực về sức khỏe tâm thần không bao phủ cấp cứu thân thể, hoặc ngược lại, hãy dùng hai người phản biện và công bố ranh giới của từng người. Phần phương pháp nghiên cứu cũng phải giao cho người đủ năng lực đánh giá thiết kế nghiên cứu nếu bác sĩ hoặc chuyên gia lâm sàng không nhận phạm vi ấy.

## 7. Cohort người mới và EPUB

Người điều phối phải dùng đúng lời xin đồng thuận, tám tác vụ, hai JSON Schema và chương trình chấm điểm hiện có. Tệp kê khai và bản ghi từng lần thử nguyên gốc nằm trong thư mục bị Git bỏ qua `build/beginner-pilot/`; không đưa chúng vào gói công khai.

Bằng chứng công khai chỉ gồm:

- mã băm của tệp kê khai riêng và biên nhận từ sổ đăng ký bên ngoài;
- báo cáo tổng hợp do chương trình chấm điểm tạo;
- xác nhận đã kiểm tra mới lịch sử chuẩn công khai;
- xác nhận con người đã rà soát riêng tư;
- môi trường EPUB đã làm sạch dữ liệu cá nhân: ứng dụng, phiên bản, loại thiết bị, cỡ chữ và chế độ tối;
- danh sách lỗi không chứa ảnh chụp hay siêu dữ liệu nhận diện người đọc.

Thử nghiệm EPUB dùng để xét cổng phải do một trong năm người đọc được tính thực hiện. Một chuyên gia EPUB riêng có thể tìm thêm lỗi, nhưng không thay thế tác vụ của người mới.

## 8. So sánh

[`comparative-beginner-protocol.md`](comparative-beginner-protocol.md) hiện chỉ là dự thảo đăng ký trước, chưa có biên nhận đăng ký và chưa cho phép đưa ra tuyên bố. Không dùng tệp kê khai của nhóm người mới để đóng cổng so sánh: điều kiện tham gia, cách phân nhóm ngẫu nhiên, kết quả đo và hợp đồng cỡ mẫu đều khác.

Ngay cả kết quả thuận lợi cũng chỉ hỗ trợ một kết luận hẹp về các ấn bản, dân số, định dạng và kết quả đã thử. Các câu “top choice”, “best” và “number one” vẫn bị cấm nếu dữ liệu không trực tiếp chứng minh đúng phạm vi ấy.

## 9. Nộp bằng chứng và đổi trạng thái

Bằng chứng được phép công khai đặt dưới `book/references/external-evidence/` theo hướng dẫn trong thư mục đó. Mỗi hồ sơ phải có đúng một dòng `Evidence role:`, một dòng `PDF SHA-256:` và một dòng `EPUB SHA-256:`; cả ba phải khớp với vai trò và ứng viên hiện hành. Mỗi vai trò singleton phải dùng một tệp riêng; không dùng một tệp chung để đóng nhiều vai trò. Mỗi hồ sơ phải có:

```text
Gate status: PASSED | FAILED
Evidence role: <canonical_role>
Candidate commit: <40 lowercase hex>
PDF SHA-256: <64 lowercase hex>
EPUB SHA-256: <64 lowercase hex>
Completed:
Signer or verifiable public confirmation:
What this evidence does not establish:
```

Sau đó:

1. thêm từng đường dẫn bằng chứng, `sha256` và `role` vào đúng cổng trong `external-release-gates.json`;
2. đổi trạng thái sang `passed` hoặc `failed`;
3. chỉ thêm mã tuyên bố mà trình kiểm tra suy ra từ các cổng đã qua;
4. cập nhật phần Status của `release-evidence.md`;
5. chạy `python3 scripts/verify_release.py`;
6. đưa thay đổi qua Publication CI.

Trình kiểm tra chỉ xác nhận tính toàn vẹn và việc bằng chứng gắn đúng tệp phát hành. Nó không xác thực chữ ký, thẩm quyền pháp lý, giấy phép hành nghề, năng lực chuyên môn hoặc sự trung thực của dữ liệu. Các điểm đó vẫn cần con người kiểm tra.

## 10. Câu mô tả hiện tại

Khi cả sáu cổng còn mở, câu duy nhất được sổ đăng ký cho phép là:

> Một ứng viên PDF và EPUB có nguồn, được kiểm toán nội bộ và được thiết kế cho người mới Việt Nam.

Không đổi câu này thành “đã được thẩm định”, “an toàn cho mọi người”, “được phép phát hành tự do”, “top choice” hoặc “giúp hàng triệu người” cho đến khi bằng chứng đúng phạm vi thật sự tồn tại.
