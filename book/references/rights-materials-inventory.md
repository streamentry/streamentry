# Bảng kê vật liệu và khoảng trống quyền phát hành

Checked: 2026-07-28

## Phạm vi

Tài liệu này gom các dữ kiện cần thiết để người có thẩm quyền hoàn thành
`rights-decision-template.md`. Nó không phải giấy phép, ý kiến pháp lý hay bằng
chứng rằng người ký thật sự nắm quyền. Mọi kết luận về sở hữu, ngoại lệ bản
quyền, tác phẩm phái sinh và phạm vi thương mại phải được đưa ra theo pháp luật
áp dụng bởi người đủ thẩm quyền.

Ảnh chụp lịch sử dùng cho kiểm tra người đóng góp:

- `main` đến commit
  `459e090872ae2a472faeca7b0f0d0e308827a264`.

Commit trên chỉ là mốc đã đọc lịch sử quyền, không phải commit tự xác nhận quyền
của artifact. Danh tính byte dùng cho quyết định được ghi riêng dưới đây:

```text
Rights materials inventory schema: 1
Immutable manuscript SHA-256: `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440`
Candidate PDF SHA-256: `08f0d67a400f2528e7318c5060dcd3b87f68597192f606db8e67d2abf77e0c45`
Candidate EPUB SHA-256: `73397650340d5af624062d838e6b9ef70ebf4eb8af422737d44149d93d92d941`
```

`scripts/verify_release.py` từ chối bảng kê nếu một trong ba mã băm trên lệch
khỏi bản thảo bất biến hoặc hai artifact của hồ sơ phát hành. Kiểm tra này ngăn
giao nhầm bản; nó không xác lập quyền. Người ra quyết định vẫn phải lấy commit
ứng viên từ gói điều phối, kiểm lại mã băm, lịch sử và trạng thái bên ngoài ngay
trước khi ký. Kho công khai có thể thay đổi sau ngày kiểm toán.

## Những gì đã xác minh

1. Kho `streamentry/streamentry` đang ở chế độ **PUBLIC**. Truy vấn GitHub trả
   `licenseInfo: null`, và cây Git không chứa `LICENSE`, `LICENSE.md` hay
   `LICENSE.txt`. Công khai không đồng nghĩa đã cấp một giấy phép tái sử dụng.
2. Lịch sử Git hiển thị hai giá trị tên tác giả commit: `j` và `Stream Entry`.
   Mọi commit một cha tạo hoặc sửa nội dung quan sát được đều mang định danh
   `j`; các commit mang `Stream Entry` đều là merge commit hai cha do GitHub tạo
   khi nhập pull request. Vì vậy, lịch sử hiện không cho thấy một người sáng tác
   thứ hai đứng sau `Stream Entry`. Nó vẫn không xác định người hoặc pháp nhân
   đứng sau `j`, quyền của họ, hay một chuyển giao quyền hợp lệ.
3. Bản thảo Markdown bất biến xuất hiện từ commit đầu
   `1eded40` dưới định danh `j`. Kho không có tuyên bố nguồn gốc, hợp đồng,
   chuyển nhượng hay giấy phép riêng cho bản thảo ấy.
4. Tín dụng xuất bản hiện là `CS Chánh Niệm + ChatGPT`. Tín dụng biên tập không
   tự xác lập chuỗi quyền giữa người dùng tài khoản, người sửa bản thảo, chủ thể
   đứng sau các Git identity và nhà phát hành.
5. Không có ảnh, SVG, phông hay tài sản raster của bên thứ ba được theo dõi
   trong cây Git. Bìa EPUB và sơ đồ quyết định ở Phụ lục E đều được tạo từ
   chính chữ, màu, CSS và bố cục của dự án.
6. PDF nhúng các subset của Inter và Libertinus Serif. EPUB chỉ chứa XHTML,
   ảnh bìa được tạo, điều hướng, metadata và CSS; nó không nhúng tệp phông.
7. Có bốn khối trình bày như lời kinh và đều được ghi là *phỏng dịch*: phần mở
   đầu MN 10 xuất hiện hai lần, Tứ Thánh Đế từ SN 56.11, và công thức duyên khởi
   từ SN 12.2 cùng SN 12.44. Phần còn lại chủ yếu là diễn giải, tóm tắt, thuật
   ngữ ngắn và dẫn nguồn, không phải bản sao toàn văn.
8. Chương 11 chép một công thức Pāli ngắn từ SN 22.59:7.1–10.1 theo đúng nguồn
   Bilara K35 đã khóa ở commit
   `3af91efb1099190c74998247177f8ba6a076b8c0`. Câu Việt đặt ngay dưới được
   ghi rõ là bản dịch sát nghĩa do sách thực hiện, không phải câu chữ lấy từ
   một bản dịch Việt hiện đại. Dữ kiện này làm rõ riêng khối mới; nó không tự
   đóng các khoảng trống RM01–RM09.

## Bảng kê tài sản

| Mã | Vật liệu | Dữ kiện hiện có | Khoảng trống phải đóng | Trạng thái trước quyết định |
|---|---|---|---|---|
| RM01 | `con-duong-niem-xu-mahasi-hop-nhat.md` | Bản thảo có SHA-256 cố định và xuất hiện ở commit đầu dưới Git identity `j`. | Danh tính pháp lý của tác giả hoặc chủ quyền, nguồn hình thành bản thảo, đóng góp có trước Git, chuyển nhượng và các cam kết đã cấp trước đây đều chưa có hồ sơ. | **authority not established** |
| RM02 | Văn xuôi, cấu trúc và phụ lục Typst | Mọi commit một cha tạo nội dung trong lịch sử hiện tại mang Git identity `j`; `Stream Entry` chỉ xuất hiện ở merge commit hai cha của GitHub. Bản hiện tại được biên tập sâu sau khi nhập bản thảo. | Cần ánh xạ `j` sang người hoặc tổ chức chịu trách nhiệm, xác nhận phạm vi đóng góp và văn bản cho phép xuất bản, sửa đổi, dịch và cấp phép lại. Không cần coi định danh merge `Stream Entry` là một tác giả thứ hai nếu lịch sử vẫn giữ cấu trúc này. | **authority not established** |
| RM03 | Đầu ra do ChatGPT hỗ trợ | Việc dùng ChatGPT được công bố trong sách. [Điều khoản OpenAI hiện hành](https://openai.com/policies/terms-of-use/) nói rằng giữa người dùng và OpenAI, trong phạm vi pháp luật cho phép, người dùng sở hữu đầu ra và OpenAI chuyển giao quyền của mình nếu có. | Phải xác định tài khoản và điều khoản thực sự áp dụng khi từng phần được tạo. Câu “trong phạm vi pháp luật cho phép” không giải quyết khả năng được bảo hộ, quyền của bên thứ ba, tính không duy nhất của đầu ra hoặc quyền của các cộng tác viên con người. | **contract provenance not recorded** |
| RM04 | Bốn khối *phỏng dịch* lời kinh | Vị trí được xác định trong `00-frontmatter.typ`, `02-dich-den-va-nen-tang.typ`, `03-tu-niem-xu-trong-kinh.typ` và `04-duyen-khoi.typ`. | Cần ghi rõ mỗi câu được dịch độc lập từ Pāli công cộng, được phép từ một bản dịch, hay dựa vào ngoại lệ đã được đánh giá. Chỉ thay nhãn “phỏng dịch” không sửa được nguồn gốc câu chữ. | **source-expression basis unresolved** |
| RM04A | Công thức vô ngã Pāli và câu Việt mới ở Chương 11 | Pāli được chép từ SN 22.59:7.1–10.1 trong K35 đã khóa; câu Việt được ghi tại chỗ là bản dịch sát nghĩa do sách thực hiện. | Cần lưu người chịu trách nhiệm cho bản dịch độc lập và đưa nó vào quyết định quyền cuối cùng. Hồ sơ rõ hơn không thay thế thẩm quyền pháp lý. | **expression path documented; authority still open** |
| RM05 | K01–K41 và các diễn giải kinh Nikāya | [SuttaCentral](https://suttacentral.net/licensing) xác nhận văn bản gốc Pāli và các ngôn ngữ cổ thuộc phạm vi công cộng; nội dung do SuttaCentral tự tạo được hiến tặng theo CC0. Trang này cũng nói nhiều bản dịch cũ thuộc quyền của dịch giả hoặc nhà xuất bản và dùng giấy phép riêng. | Sổ nguồn dùng cả bản dịch SuttaCentral mới lẫn các bản của Minh Châu, Bodhi và Suddhaso. Cần phân biệt câu chữ nào dịch trực tiếp từ Pāli, câu nào dựa trên bản dịch hiện đại và điều khoản riêng của đúng ấn bản. Câu K41 trong chương 10 được sách dịch trực tiếp từ Pāli; bản Buddharakkhita chỉ dùng để đối chiếu. | **mixed source terms; review required** |
| RM06 | V01, *The Path of Purification* | BPS Online Edition 2014 ghi bản dịch © BPS, cho tái bản và tác phẩm phái sinh khi được phát hành miễn phí, không hạn chế, và được đánh dấu rõ là phái sinh. Sách hiện tóm tắt và dẫn đoạn, không đóng gói bản PDF nguồn. | Nếu phát hành có thu tiền, phải xác định các diễn giải hiện tại có dựa vào quyền được phép, ngoại lệ hợp lệ hay cần xin phép. Pháp luật và kênh thương mại chưa được chọn. | **free-distribution terms identified; commercial basis unresolved** |
| RM07 | P01, *Practical Insight Meditation* | Bản PDF BPS ghi `Copyright © Buddhist Publication Society 1971`; trang đầu không nêu giấy phép tái sử dụng. Sách hiện tóm tắt phương pháp và dẫn nguồn. | Cần đánh giá mức độ gần câu chữ, căn cứ trích dẫn hoặc diễn giải, và xin phép nếu phạm vi dự định vượt căn cứ hợp lệ. | **permission or legal basis unresolved** |
| RM08 | P02, *The Progress of Insight* | [Trang Access to Insight](https://www.accesstoinsight.org/lib/authors/mahasi/progress.html) ghi ©1994 BPS. Giấy phép tại trang cho phép sao chép và tác phẩm phái sinh khi phát hành miễn phí, phải nêu nguồn và kèm toàn văn giấy phép; bản in lại bị giới hạn tối đa 50 bản. | Chương 12 diễn giải sâu cấu trúc P02. Cần quyết định liệu phần ấy là diễn giải độc lập, trích dẫn, hay tác phẩm phái sinh theo luật áp dụng. Không được suy từ quyền phát hành miễn phí sang quyền bán hoặc in không giới hạn. | **free-only source terms; commercial and print basis unresolved** |
| RM09 | R01–R11, nguồn nghiên cứu, y tế và đầu số khẩn cấp chính thức | Sách dẫn bài nghiên cứu, cơ quan y tế, Nghị định 200/2025/NĐ-CP và quy hoạch kho số viễn thông; chỉ tóm tắt mệnh đề hẹp và không sao chép hình, bảng hay ảnh của họ. | Cần kiểm lần cuối để loại câu quá gần nguyên văn, ghi đúng nguồn, kiểm tra lại đầu số sau ngày chốt ấn bản và xem xét điều khoản của đúng tài liệu nếu phát hành thương mại hoặc dịch sang ngôn ngữ khác. | **citation use inventoried; legal review open** |
| RM10 | Bố cục, bìa, ảnh bìa EPUB và sơ đồ quyết định | Bố cục cùng sơ đồ Phụ lục E nằm trong Typst và CSS của dự án; ảnh bìa được sinh từ trang đầu. Không có ảnh minh họa nhập từ ngoài. | Quyền đối với mã, bố cục và sơ đồ vẫn phụ thuộc RM02. Cần xác nhận bút danh, logo nếu thêm về sau, và phạm vi dùng bìa hoặc sơ đồ trong quảng bá. | **authority follows contributor chain** |
| RM11 | Inter 4.0 trong PDF | PDF nhúng subset Inter. [Giấy phép Inter](https://github.com/rsms/inter/blob/master/LICENSE.txt) là SIL OFL 1.1; giấy phép cho phép dùng và nhúng phông, và nói giấy phép phông không áp vào tài liệu được tạo. | Lưu đúng phiên bản, nguồn, checksum và giấy phép trong hồ sơ phát hành. Không bán riêng phông hoặc dùng tên chủ thể quyền để ngụ ý chứng thực. | **license identified; release record still required** |
| RM12 | Libertinus Serif trong PDF | PDF nhúng subset Libertinus Serif từ bộ phông tích hợp của Typst. [Dự án Libertinus](https://github.com/alerque/libertinus) phát hành phông theo SIL OFL 1.1; hướng dẫn OFL của SIL cho phép nhúng toàn bộ hoặc subset trong PDF. | Cần ghi phiên bản phông chính xác đi cùng Typst 0.15.0 hoặc lưu thông báo giấy phép từ gói nhị phân đã dùng. | **license family identified; exact bundled version unresolved** |
| RM13 | DejaVu Sans Mono | Theme khai báo phông này, nhưng `pdffonts` không thấy nó trong PDF hiện tại và EPUB không nhúng phông. | Nếu nội dung mới khiến phông được nhúng hoặc phông được phân phối riêng, phải mở lại kiểm toán và lưu giấy phép DejaVu. | **not present in current artifacts** |
| RM14 | Typst, Python, Node và công cụ kiểm định | Công cụ tạo hoặc kiểm tra artifact không được đóng gói trong PDF/EPUB. Typst công bố giấy phép Apache-2.0; các dependency khác có metadata giấy phép trong lockfile hoặc gói của chúng. | Phát hành source, container, bộ cài hoặc tool bundle là hành vi khác với phát hành sách và cần bảng notices riêng. Không suy quyền đối với sách từ giấy phép công cụ. | **tooling not bundled in current book artifacts** |
| RM15 | Kho mã, giao thức, lược đồ và script | Kho đang công khai nhưng không có giấy phép cấp quyền dùng lại. | Chủ thể có thẩm quyền phải chọn hoặc từ chối giấy phép cho source. Giấy phép source, giấy phép nội dung sách và quyền phân phối PDF/EPUB có thể khác nhau. | **no repository license recorded** |
| RM16 | PDF, EPUB, bản in, bản dịch và audiobook tương lai | Đây là các tác phẩm tổng hợp hoặc phái sinh từ những dòng trên. | Mỗi định dạng, ngôn ngữ, lãnh thổ, kênh, thời hạn và tình trạng thương mại phải được quyết định riêng. Bằng chứng của bản Việt không tự chuyển sang bản dịch. | **authority not established** |

## Ma trận hành vi hiện tại

Không dòng nào dưới đây được xem là đã cho phép chỉ vì kho có thể truy cập.

| Hành vi | Trạng thái hiện tại | Bằng chứng còn thiếu |
|---|---|---|
| Giữ source trong kho GitHub công khai | `authority not established` | Chuỗi quyền của RM01–RM03 và quyết định giấy phép source. |
| Cho tải PDF miễn phí | `authority not established` | Người có thẩm quyền, phạm vi lãnh thổ và xử lý RM04–RM12. |
| Cho tải EPUB miễn phí | `authority not established` | Như trên; EPUB không nhúng phông nhưng vẫn chứa toàn bộ văn xuôi và bìa. |
| In hoặc print-on-demand miễn phí | `authority not established` | Quyền in, số lượng, lãnh thổ và giới hạn của nguồn có điều khoản riêng. |
| Bán bản in, PDF hoặc EPUB | `authority not established` | Căn cứ thương mại cho RM04–RM09 cùng chuỗi quyền nội bộ. |
| Dịch, làm audiobook hoặc bản tiếp cận | `authority not established` | Quyền tạo tác phẩm phái sinh và bằng chứng riêng cho ngôn ngữ hoặc định dạng mới. |
| Dùng trích đoạn để quảng bá | `authority not established` | Độ dài, câu chữ, nguồn, nền tảng, phạm vi thương mại và ghi công. |
| Cho distributor hoặc platform cấp phép lại | `authority not established` | Quyền sublicensing rõ ràng từ mọi chủ thể liên quan. |

## Hồ sơ tối thiểu để đóng cổng

Thứ tự này giảm chi phí kiểm tra sai hướng:

1. Xác định người hoặc pháp nhân sẽ ký, thẩm quyền, pháp luật áp dụng và kênh
   định phát hành.
2. Lấy tuyên bố nguồn gốc cùng quyền sở hữu hoặc văn bản chuyển giao cho bản
   thảo RM01.
3. Ánh xạ Git identity tạo nội dung `j` sang người hoặc tổ chức thật; xác nhận
   các merge commit mang `Stream Entry` chỉ là thao tác nhập pull request; lấy
   xác nhận về đóng góp, quyền sửa đổi, phát hành, dịch và cấp phép lại.
4. Ghi loại tài khoản OpenAI và bản điều khoản áp dụng; không dùng tín dụng
   `ChatGPT` thay cho người chịu trách nhiệm pháp lý.
5. Giải quyết bốn khối phỏng dịch trước. Phương án có thể là chứng minh bản dịch
   độc lập từ Pāli công cộng, thay bằng câu chữ mới được kiểm tra, xin phép, hoặc
   dựa vào ngoại lệ đã được luật sư đánh giá. Người biên tập không tự chọn ngoại
   lệ pháp lý.
6. Kiểm riêng V01, P01 và P02 cho đúng mô hình miễn phí, thương mại và số lượng
   in dự kiến. Điều khoản “free distribution” không được kéo sang bán sách.
7. Lưu phiên bản, nguồn, checksum và notice của Inter cùng Libertinus. Mở lại
   kiểm toán nếu EPUB bắt đầu nhúng phông hoặc xuất hiện tài sản hình ảnh mới.
8. Chọn giấy phép hoặc tuyên bố giữ toàn quyền cho source, nội dung và artifact
   như ba quyết định riêng.
9. Điền đủ `rights-decision-template.md`, gắn quyết định vào đúng commit, PDF,
   EPUB, lãnh thổ, thời hạn, thương mại, ghi công và quyền cấp phép lại.
10. Đưa bằng chứng công khai, không chứa dữ liệu liên lạc riêng, vào đúng vai
    trò `rights_decision`; sau đó mới đổi cổng máy đọc từ `open` sang `passed`.

## Kết luận kiểm toán

Kiểm toán đã làm rõ vật liệu, không làm phát sinh quyền. Hai điểm chặn đầu tiên
là chuỗi quyền của bản thảo và đóng góp con người; điểm chặn kế tiếp là căn cứ
cho bốn khối phỏng dịch cùng các diễn giải dựa trên V01, P01 và P02. Phông của
PDF có giấy phép cho phép nhúng, nhưng hồ sơ phiên bản vẫn phải được lưu.

Trạng thái đúng của cổng `redistribution_rights` vẫn là **OPEN**. Thay đổi nó
trước khi có quyết định có thẩm quyền sẽ biến một bảng kê trung thực thành một
tuyên bố pháp lý không có bằng chứng.
