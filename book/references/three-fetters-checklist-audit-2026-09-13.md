# Đối chiếu bộ câu hỏi tự soi ba kiết sử đầu

Ngày biên tập: **2026-09-13**. Phạm vi: Phụ lục F mới, các liên kết và đoạn bổ sung ở Chương 10, tám mục nguồn K45–K52. Đây là hồ sơ biên tập nội bộ; **không phải phản biện độc lập hay bằng chứng xác nhận chứng quả**.

## 1. Bản gốc và phạm vi sửa

- `main` được kiểm tra qua GitHub: `6eb33b6ca4a6510ee61e12bfd1f6ac277d88d60d`.
- Cây nguồn: `701761035c07da03e5b5afe826080930c453e78d`.
- Nguồn làm việc lấy từ `source.zip` trong artifact GitHub Actions `10311377060`, run `34737831614`. Checkout tổng hợp của artifact là `d8ac17a8259753fa0d8ad85d6c102e5dbadd16ee`; API Git xác nhận checkout này và `main` có cùng cây nguồn nói trên.
- Tệp Markdown gốc `con-duong-niem-xu-mahasi-hop-nhat.md` không sửa. SHA-256: `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440`.
- Không sửa hồ sơ nguồn bất biến `attainment-source-audit.md`, edition, release evidence, quyền sử dụng, cổng phản biện hay bản phát hành `dist`.
- Gói bàn giao trước chưa được ghi lên GitHub. Trong lượt tích hợp hiện tại, nhánh `editorial/three-fetters-checklists-20260913` đã được tạo từ đúng commit `main` nêu trên bằng công cụ GitHub. Trạng thái PR, commit và kiểm tra tích hợp được ghi riêng trong `three-fetters-integration-2026-09-13.md`. Không dùng tình trạng của gói bàn giao cũ để mô tả trạng thái kho hiện tại.

## 2. Quy tắc biên tập

Khuôn hai mươi thân kiến có trong kinh; hình thức bảng ghi nhận là biên soạn. H1–H6 và G1–G6 không được gọi là danh mục chẩn đoán có sẵn trong kinh. “Có / ? / Chưa thấy” là trạng thái quan sát, không phải mức đạo quả. Các tình huống gia đình, việc làm, tụng kinh, thời khóa và cách ghi phiếu là ví dụ do sách dựng, không phải truyện trong kinh hay dữ liệu thực nghiệm.

Chứng cứ ngược chỉ có giá trị sau khi nhận diện đúng: kiết sử thực sự còn thì không tương hợp với đoạn tận; một cảm xúc hay hành vi bị gọi nhầm là kiết sử không đủ để kết luận. Không thấy biểu hiện lại không chứng minh đã đoạn cả tùy miên. AN 10.92 vẫn giữ khả năng tự tuyên bố khi đầy đủ điều kiện nguồn; không đổi sự thận trọng thành lời cấm tuyệt đối về tự biết.

## 3. Nguồn mới: đã đọc gì và không suy ra điều gì?

Các trang SuttaCentral giao diện động không được dùng làm bằng chứng rằng văn bản đã đọc đầy đủ khi bộ đọc chỉ nhận được giao diện. Với K46, K47, K49, việc đọc thực tế dùng các tệp JSON công khai của `suttacentral/bilara-data`, nhánh `published`. Blob SHA dưới đây định danh nội dung đã truy xuất; không giả định cả nhánh được đóng băng bằng một commit chưa kiểm tra. Với các trang dịch HTML, không tuyên bố đã đối chiếu Pāli khi chưa làm việc ấy trong lượt này.

| Mã | Bản thực tế đã đọc | Vị trí, người nói | Điều hỗ trợ; giới hạn |
|---|---|---|---|
| K45 | [SN 22.82, Ṭhānissaro](https://www.dhammatalks.org/suttas/SN/SN22_82.html) | Câu hỏi về có/không thân kiến; đoạn suy luận về tự ngã và quả hành động. Đức Phật trả lời. | Bốn quan hệ trên năm uẩn; không biến vô ngã thành vô trách nhiệm. Không có bảng tự chấm quả. |
| K46 | [MN 16, Pāli](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/mn/mn16_root-pli-ms.json), blob `dcd87c67be8057c04c8cd5d343df34a7ca7be00b`; [Sujato](https://github.com/suttacentral/bilara-data/blob/published/translation/en/sujato/sutta/mn/mn16_translation-en-sujato.json), blob `cb8d81b08c07cfa39d7d799d7ef65c89a9c65b31` | `mn16:3.2–7.4`, Đức Phật. | Bốn đối tượng nghi: Đạo sư, Pháp, Tăng, học tập. Trường hợp thứ năm là bất mãn với bạn đồng tu. Ngữ cảnh tâm hoang vu không tự thành định nghĩa thao tác đầy đủ của kiết sử hoài nghi. |
| K47 | [MN 47, Pāli](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/mn/mn47_root-pli-ms.json), blob `59554b8bbb2d3f7ae4f34ff0573ef7031530b793`; [Sujato](https://github.com/suttacentral/bilara-data/blob/published/translation/en/sujato/sutta/mn/mn47_translation-en-sujato.json), blob `7c07b0c25c641044661552ae287cc76b846e4d84` | Pāli `mn47:2.1–16.7`; phần kết `14–16` cũng đối chiếu Anh. Đức Phật. | Khảo sát Như Lai, nghe Pháp, lòng tin có căn cứ bắt rễ nơi thấy biết. Không suy mọi chất vấn đều thiện, hoặc đoạn hoài nghi nghĩa là không cần rõ điều gì. |
| K48 | [MN 95, Ṭhānissaro](https://www.dhammatalks.org/suttas/MN/MN95.html) | Phần năm căn cứ có thể đúng/sai, bảo hộ chân lý, khảo sát người dạy, nghe và thực hành; Đức Phật. | Phân biệt tin, suy xét, chứng biết. Không phủ nhận giá trị của tín hoặc suy luận trong lộ trình. |
| K49 | [AN 3.78, Pāli](https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/an/an3/an3.78_root-pli-ms.json), blob `30f9a520851565ab1952bd99986921e5d9224d6a`; [Sujato](https://github.com/suttacentral/bilara-data/blob/published/translation/en/sujato/sutta/an/an3/an3.78_translation-en-sujato.json), blob `a41c7ae1e73c0b47e2d96e68c60477fc3a32308e` | `an3.78:1.1–3.5`; Ānanda phân tích, Đức Phật tán thành tại `2.4`. | Giá trị thực hành xét qua thiện/bất thiện. Tên *Sīlabbata*, hệ số SuttaCentral. **Không dùng** trang `AN3_78.html` ở Dhammatalks làm liên kết tương đương vì đó là bài *Bhava (2)*. Không đồng nhất sīlabbata và sīlabbataparāmāsa. |
| K50 | [MN 78, Ṭhānissaro](https://www.dhammatalks.org/suttas/MN/MN78.html) | Đoạn bốn biểu hiện không làm ác, ví dụ trẻ nhỏ và tu tập đầy đủ hơn; Đức Phật. | Không lấy riêng sự chưa làm ác làm toàn bộ thành tựu cao nhất. Không nâng ghi chú dịch giả về `no ca sīla-mayo` thành lời Phật định nghĩa kiết sử. |
| K51 | [SN 1.25, Ṭhānissaro](https://www.dhammatalks.org/suttas/SN/SN1_25.html) | Đối thoại về vị A-la-hán dùng “tôi”; câu trả lời trong bài kinh. | Ngôn ngữ quy ước không tự là chấp. Không dùng ghi chú dịch giả như câu kinh. |
| K52 | [SN 22.56, Ṭhānissaro](https://www.dhammatalks.org/suttas/SN/SN22_56.html) | Các đoạn định nghĩa từng uẩn; Đức Phật. | Căn cứ cho chú giải đọc bảng. Thọ ba sắc thái đối chiếu MN 44. Không đồng nhất mọi từ hành với một chú giải tâm lý học. |

Nguồn cũ được đọc lại phục vụ phần bổ sung: [MN 2](https://www.dhammatalks.org/suttas/MN/MN2.html), [MN 44](https://www.dhammatalks.org/suttas/MN/MN44.html), [MN 64](https://www.dhammatalks.org/suttas/MN/MN64.html), [SN 22.59](https://www.dhammatalks.org/suttas/SN/SN22_59.html), [SN 22.89](https://www.dhammatalks.org/suttas/SN/SN22_89.html), [AN 10.92](https://www.dhammatalks.org/suttas/AN/AN10_92.html), bản [MN 57 của Ñāṇamoli](https://www.accesstoinsight.org/tipitaka/mn/mn.057.nymo.html). Khi bản dịch đọc bổ sung khác bản đứng trong bản đồ nguồn cũ, giữ phân biệt hai bản; không ngầm tuyên bố đã đọc lại bản cũ. AN 3.88 và hệ phân loại rộng được kế thừa từ hồ sơ hiện có, không tuyên bố đối chiếu mới toàn bộ.

## 4. Đối chiếu từng câu hỏi

| Câu | Căn cứ | Thao tác do sách biên soạn; không được suy quá |
|---|---|---|
| Bảng A–D × năm uẩn | K45, đối chiếu K20; chú giải uẩn K52 | Hai mươi quan hệ là khuôn kinh. Ba trạng thái ghi nhận, bảng in và việc chọn một sự kiện là biên soạn. Không thu hẹp thân kiến vào thân thể hay niềm tin linh hồn bất biến. |
| T1 | K45; K20 | Yêu cầu mô tả quan kiến cụ thể, không gán thân kiến từ nhu cầu được công nhận. |
| T2 | K45; K11 | “Người biết không đổi” là ví dụ biên soạn của cách chấp có thể gặp, không điều kiện bắt buộc của mọi thân kiến. |
| T3 | K35; K36 | Câu hỏi về quan sát khác thuộc lòng. Không biến một lần thấy thay đổi thành bằng chứng đoạn tận. |
| T4 | K51; K17; K36 | Đại từ, nhu cầu nghỉ, lo sức khỏe và một cảm xúc không tự xác định quan kiến. Đây là giới hạn suy luận, không phủ nhận phản ứng cần được tu sửa. |
| T5 | K45 | Áp dụng giới hạn suy luận của SN 22.82 vào trách nhiệm hiện tại; không thêm học thuyết về người nhận nghiệp. |
| H1 | K46; K47; K21 | Phân biệt đối tượng nghi; một người hay bản dịch không đại diện mọi phẩm chất của Pháp, Tăng. |
| H2 | K48 | Ghi loại căn cứ; không gọi suy luận là trực chứng, không coi tín vô ích. |
| H3 | K47; K48 | Cho phép khảo sát, không ép tin; cũng không hợp thức hóa mọi nghi chưa giải quyết thành đoạn nghi. |
| H4 | K21; K48 | Công thức bốn đôi tám hạng khác mọi cá nhân hiện tại. Không xác định quả vị của người khác. |
| H5 | K46; K48 | Chuyển một phân vân thành kế hoạch học tập là quy trình biên soạn, không tiêu chuẩn chứng quả. |
| H6 | K36; K47; K48; K21 | Không lấy xúc động, bình an hay tự tin làm xác chứng. Không diễn giải đoạn hoài nghi thành biết hết thông tin đời thường. |
| G1 | K49 | Làm rõ mục đích phương tiện. Học theo hướng dẫn chưa tự là chấp thủ. |
| G2 | K38; K50; K11 | Xét niềm tin gán sức bảo đảm cho riêng hình thức; không phủ nhận các điều kiện thực hành kinh thực sự nêu. |
| G3 | K21; K49 | Không dùng thủ tục thay dừng/sửa hành vi. Không tự thêm lý thuyết xóa nghiệp bằng hoặc không bằng nghi thức. |
| G4 | K49 | Ghi thay đổi thiện/bất thiện, phân biệt thấy rõ với tăng thêm. Không đánh đồng thoải mái với thiện, không áp ngưỡng số. |
| G5 | K49; K21 | Phân biệt điều chỉnh hình thức và bỏ giới; an toàn, bổn phận là giới hạn biên soạn. Không coi mọi nghiêm túc là chấp. |
| G6 | K48; K49; K50 | Kiểm tra tuyên bố độc quyền và điều kiện nguồn, không tấn công hoặc đánh đồng truyền thống. |

## 5. Những phép suy luận bị loại

- “Không tin linh hồn nên đã hết thân kiến”; “còn nói tôi nên còn thân kiến”; “còn ngã mạn nên chưa thể đoạn thân kiến”.
- “Còn hỏi là còn hoài nghi”; “tin mãnh liệt là đã đoạn hoài nghi”; “không có năng lượng thực hành chắc chắn là nghi”.
- “Giữ giới nghiêm, tụng kinh hoặc giữ thời khóa là giới cấm thủ”; “không chấp nghĩa là không cần giới”; “dễ chịu là thiện pháp”.
- “MN 16 cho bốn câu kiểm định kiết sử”, hoặc “AN 3.78 định nghĩa toàn bộ giới cấm thủ”.
- “Tất cả ô âm tính là đã đoạn”; “thầy hoặc AI có thể xác nhận quả vị từ phiếu”; “không ai có khả năng tự biết trong mọi trường hợp”.

## 6. Kiểm tra và giới hạn phát hành

`three-fetters-integration-2026-09-13.md` ghi kiểm tra và tình trạng tích hợp hiện tại. `KIEM-TRA.md` trong gói bàn giao trước chỉ mô tả lượt dựng phụ lục độc lập, không phải bằng chứng cho bản toàn sách mới. Các bài kiểm tra Python chỉ kiểm tra cấu trúc, liên kết, nguồn, lời giới hạn và việc không đổi bản gốc; chúng không chứng minh giáo lý đúng hay xác định chứng đạt.

Môi trường biên tập cục bộ không có Typst. Việc dựng toàn sách phải dùng quy trình preview đã có trên GitHub Actions; chỉ ghi thành công khi có artifact và nhật ký đúng commit. PDF 15 trang trong gói bàn giao trước là bản đọc riêng, không phải đầu ra của `book/main.typ` và không thay bản sách hoặc hồ sơ phát hành. Không coi kiểm tra nội bộ là phản biện độc lập, thử đọc người mới, thẩm định an toàn hoặc thông qua quyền sử dụng.

## 7. Kiểm tra lại khi tích hợp lên GitHub

- Đã đọc lại SN 22.82, MN 64, MN 95, MN 78 và AN 10.92 trên bản HTML của Ṭhānissaro; giữ lời chú giải dịch giả tách khỏi phần kinh.
- Đã đọc lại phần nghi ngờ và tâm hoang vu của MN 16 từ JSON bản dịch Sujato, blob `cb8d81b08c07cfa39d7d799d7ef65c89a9c65b31`; MN 47 từ JSON bản dịch Sujato trên Bilara. AN 3.78 được đọc lại cả bản Pāli và bản dịch; blob vẫn lần lượt là `30f9a520851565ab1952bd99986921e5d9224d6a` và `a41c7ae1e73c0b47e2d96e68c60477fc3a32308e`.
- Sửa diễn đạt quanh ba kiết sử đầu cho nhẹ nhàng; thêm giải nghĩa tại chỗ cho Pháp, Như Lai và tịnh tín bất động; đưa lời áp dụng về khảo sát ra ngoài khối nhãn KINH. Giữ nguyên 20 ô và 17 câu hỏi, không rút bớt căn cứ hoặc giới hạn.
- Việc kiểm tra lại trong lượt này không nâng các mục chỉ có bản dịch thành đối chiếu Pāli toàn văn.
