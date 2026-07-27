# Biểu mẫu quyết định quyền phát hành

Checked: 2026-07-26

Biểu mẫu này buộc người ra quyết định nói rõ họ kiểm soát quyền nào và cho phép hành vi nào đối với *Hướng Đến Nhập Lưu*. Nó không phải giấy phép mặc định và không tự xác lập quyền. Nếu thẩm quyền hoặc luật áp dụng chưa rõ, dùng trạng thái `authority not established` và tìm tư vấn phù hợp.

## 1. Danh tính và thẩm quyền

```text
Decision record ID:
Legal name:
Public or pen name:
Capacity: author | rights holder | assignee | publisher | authorized officer | other
Organization, if any:
Public evidence of capacity:
Basis of authority:
Contributors covered:
Prior grants, assignments, liens or restrictions:
Applicable jurisdiction:
Decision date:
```

Không công bố thông tin liên lạc riêng trong kho mã. Người phụ trách phát hành giữ thông tin liên lạc và bản gốc chữ ký ở kênh an toàn.

## 2. Artifact được quyết định

```text
Candidate commit:
Immutable manuscript SHA-256:
PDF SHA-256:
EPUB SHA-256:
PDF pages:
Publication credit:
```

Một quyết định không xác định đúng tệp phát hành chỉ là ý định chung. Khi nội dung, hình ảnh, ghi công hoặc mã băm thay đổi, phạm vi quyền phải được đánh giá lại.

## 3. Tóm tắt máy đọc bắt buộc

Hồ sơ công khai có vai trò `rights_decision` phải chứa đúng một dòng cho từng
trường dưới đây. Đây là lớp kiểm tra tính đầy đủ và nhất quán, không phải bằng
chứng rằng lời khai về quyền là đúng. Không giữ dấu ngoặc nhọn hoặc từ giữ chỗ
trong hồ sơ thật.

```text
Rights decision schema: 1
Decision record ID: <lowercase-stable-id>
Decision maker public identity: <public identity authorized for publication>
Decision maker capacity: author | rights_holder | assignee | publisher | authorized_officer
Basis of authority: <specific ownership, assignment, licence or office>
Public evidence of authority: <public confirmation mechanism>
Applicable jurisdiction: <jurisdiction>
Rights materials inventory SHA-256: <current inventory sha256>
Immutable manuscript SHA-256: <current immutable source sha256>
Repository source scope: PUBLIC_REUSE_AUTHORIZED | PUBLIC_READ_ONLY | NOT_AUTHORIZED
PDF distribution scope: FREE_ONLY | FREE_AND_PAID | NOT_AUTHORIZED
EPUB distribution scope: FREE_ONLY | FREE_AND_PAID | NOT_AUTHORIZED
Print distribution scope: FREE_ONLY | FREE_AND_PAID | NOT_AUTHORIZED
Derivative editions scope: AUTHORIZED | AUTHORIZED_WITH_CONDITIONS | NOT_AUTHORIZED
Territory: <territory>
Languages: vi
Term: <term>
Attribution: <required attribution>
Required third-party notices: <notices or NONE>
Contributor chain status: RESOLVED | UNRESOLVED
Third-party materials status: RESOLVED | UNRESOLVED
Unresolved rights items: NONE | <specific unresolved items>
Overall rights decision: APPROVE | DECLINE | AUTHORITY_NOT_ESTABLISHED
Exact permitted public wording: <one bounded sentence>
```

Một kết quả `PASSED` chỉ hợp lệ khi `Overall rights decision` là `APPROVE`, cả
PDF và EPUB được cho phép, chuỗi người đóng góp và vật liệu bên thứ ba đều
`RESOLVED`, và `Unresolved rights items` là `NONE`. Phạm vi `FREE_ONLY` không
cho phép bán; quyền PDF không tự chuyển sang EPUB, bản in, bản dịch hoặc source.
Một kết quả `FAILED` phải ghi `DECLINE` hoặc `AUTHORITY_NOT_ESTABLISHED`, không
được vừa thất bại vừa ghi `APPROVE`.

Trình kiểm tra còn buộc hai mã băm trên khớp với bảng kê và bản thảo hiện hành.
Nó không xác minh danh tính, chữ ký, thẩm quyền pháp lý, hiệu lực chuyển giao,
hay tính đúng của đánh giá ngoại lệ bản quyền. Người phụ trách phát hành phải
kiểm các điểm đó bằng hồ sơ gốc.

## 4. Chuỗi quyền

Đọc `rights-materials-inventory.md` trước khi điền bảng. Kiểm tra lại từng dữ
kiện theo commit và kênh phát hành thực tế; không kế thừa nhãn “đã xác minh” của
kiểm toán nội bộ như một kết luận pháp lý.

Lập một dòng cho mỗi tác phẩm hoặc phần đóng góp:

| Mã tài sản | Đường dẫn hoặc vị trí | Vật liệu chính xác | Nguồn gốc | Người giữ quyền | Căn cứ quyền | Bằng chứng | Hạn chế hoặc xung đột | Quyết định |
|---|---|---|---|---|---|---|---|---|
|  |  |  | nguyên bản, bản dịch, bản chuyển thể, được cấp phép, trích dẫn |  | sở hữu, chuyển nhượng, giấy phép, văn bản cho phép, ngoại lệ đã được đánh giá | hồ sơ có chữ ký hoặc bản lưu giấy phép |  | đã thông qua, phải thay, cần xin phép, cần tư vấn pháp lý |

Tối thiểu phải xét:

- bản thảo Markdown bất biến;
- toàn bộ bản biên tập Typst và phần văn xuôi mới;
- đóng góp của từng Git identity;
- bút danh và thông tin ghi công;
- bản dịch, trích dẫn và phần diễn đạt gần nguyên văn từ kinh, sách, nghiên cứu và hướng dẫn y tế;
- phông chữ Inter và Libertinus, bìa, bố cục và ảnh raster;
- mã nguồn, khung kiểm toán, giao thức và lược đồ;
- tài liệu so sánh của bên thứ ba.

Dẫn URL trong sổ tuyên bố không tự trả lời cột “Căn cứ quyền”.

## 5. Quyết định theo hành vi

Đánh dấu đúng một lựa chọn cho từng dòng: `authorized`, `authorized with conditions`, `not authorized`, hoặc `authority not established`.

| Hành vi | Quyết định | Kênh hoặc định dạng | Tình trạng thương mại | Điều kiện |
|---|---|---|---|---|
| Giữ source trong public Git repository |  | GitHub |  |  |
| Cho tải PDF miễn phí |  | website, direct link, store | free |  |
| Cho tải EPUB miễn phí |  | website, direct link, store | free |  |
| In bản giấy hoặc print-on-demand |  | printer, retailer | free hoặc paid |  |
| Bán PDF hoặc EPUB |  | named platforms | paid |  |
| Sửa đổi và phát hành ấn bản mới |  | mã nguồn, PDF, EPUB, bản in |  |  |
| Dịch sang ngôn ngữ khác |  | named languages |  |  |
| Làm bản chữ lớn, braille hoặc bản tiếp cận |  | các định dạng được nêu |  |  |
| Làm audiobook hoặc narration |  | audio platforms |  |  |
| Dùng excerpt để quảng bá |  | web, social, press |  |  |
| Cho distributor hoặc platform sublicense |  | named parties |  |  |

Quyền đối với mã nguồn, nội dung sách và các tệp đã biên dịch có thể khác nhau. Không gộp chúng vào một chữ `open`.

## 6. Phạm vi

```text
Territory:
Languages:
Term:
Exclusive or non-exclusive:
Transferable:
Sublicensable:
Attribution required:
Copyright or rights notice:
Required third-party notices:
Commercial restrictions:
Share-alike or no-derivatives conditions:
Version and update rule:
Revocation or termination rule:
Archive treatment after termination:
```

## 7. Vật liệu bên thứ ba

Với mỗi asset bên thứ ba, lưu:

- đúng ấn bản nguồn và ngày truy cập;
- tên và phiên bản giấy phép, kèm bản lưu hoặc văn bản cho phép;
- những hành vi giấy phép cho phép;
- cách ghi công và thông báo bắt buộc;
- hạn chế về thương mại, tác phẩm phái sinh, lãnh thổ hoặc nền tảng;
- phần không thuộc quyền của người ký;
- người kiểm và ngày kiểm.

Nếu dựa vào quyền trích dẫn, `fair dealing`, `fair use` hoặc ngoại lệ khác, ghi rõ ai đã đánh giá, theo pháp luật của thẩm quyền nào và trong phạm vi nào. Kho mã không được tự suy ra ngoại lệ ấy.

## 8. Kết luận

```text
Overall decision:
  approve exact PDF and EPUB distribution
  approve with listed conditions
  decline
  authority not established

Unresolved items:
Required replacements or permissions:
Exact permitted public wording:
What this decision does not authorize:
```

Cổng `redistribution_rights` chỉ được đánh dấu `passed` khi:

1. thẩm quyền đối với ấn bản được xác lập bằng bằng chứng;
2. PDF và EPUB đều có quyết định rõ cho các kênh định dùng;
3. không còn trở ngại chưa giải quyết đối với người đóng góp hoặc vật liệu bên thứ ba;
4. lãnh thổ, thời hạn, cách ghi công và phạm vi thương mại không bị bỏ trống;
5. quyết định gắn với commit và mã băm của các tệp phát hành.

## 9. Xác nhận

```text
Decision-maker:
Capacity:
Signature or verifiable public confirmation:
Signed date:
Independent legal review, if any:
Release steward verification:
Verification date:
```

Một chữ ký không làm cho các tuyên bố về giáo lý, an toàn, người mới hoặc ưu thế so sánh trở thành đúng. Mỗi cổng ấy đòi bằng chứng riêng.
