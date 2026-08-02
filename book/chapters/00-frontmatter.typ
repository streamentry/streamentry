#import "../components.typ": *
#import "../edition.typ": edition

#context {
  if target() == "html" {
    html.elem("header", attrs: (class: "introduction-opener"))[
      #html.elem("p", attrs: (class: "eyebrow"))[#edition.labels.introduction]
      #heading(level: 1, outlined: true)[Một cuốn sổ tay, không phải giấy chứng nhận]
    ]
  } else {
    align(center)[
      #v(12mm)
      #eyebrow(edition.labels.introduction, fill: palette.saffron)
      #v(6mm)
      #heading(level: 1, outlined: true)[Một cuốn sổ tay, không phải giấy chứng nhận]
    ]
  }
}

#v(10mm)

Cuốn sách này có một mục đích thực tế: giúp người tại gia bắt đầu và duy trì pháp hành Niệm xứ theo truyền thống Mahāsi, đồng thời biết rõ điều nào đến từ kinh sớm, điều nào thuộc hệ thống luận giải, điều nào là chỉ dẫn của một dòng thiền hiện đại.

Vì vậy, sách đi theo một nhịp khá rõ: trước hết là cách bắt đầu cho người mới, sau đó là nền giáo lý tối thiểu, rồi mới đến các chủ đề dễ làm người đọc lẫn nếu gặp quá sớm.

#source-line("BIÊN SOẠN", [ba nghĩa làm việc, đối chiếu K01; P01; K06], [
  Để bắt đầu, chỉ cần giữ ba nghĩa ngắn. *Niệm xứ* là học cách biết rõ thân, sắc thái dễ chịu hay khó chịu, trạng thái tâm và những khuôn mẫu được lời dạy chỉ ra. *Mahāsi* là một dòng thiền hiện đại trong truyền thống Theravāda, truyền thống Phật giáo dùng kinh tạng Pāli làm nền; phương pháp dùng chuyển động bụng, ghi nhận trong tâm và thiền hành để tổ chức việc quan sát. *Nhập lưu* là sự bước vào Bát Thánh đạo theo tiêu chuẩn của kinh, không phải tên khác của cảm giác yên hay một buổi ngồi sâu. Các chương sau sẽ mở từng nghĩa ra; người mới chưa cần thuộc thuật ngữ ngay ở đây.
])

Tên sách dùng cụm từ *hướng đến nhập lưu*. Đây là giới hạn có chủ ý. Kinh điển mô tả Nhập lưu là một chuyển đổi xác định trong thấy biết và đời sống đạo đức. Không thời khóa, kỹ thuật hay trải nghiệm đơn lẻ nào cho phép một cuốn sách hứa chắc kết quả ấy.

#v(8pt)

#caution(
  [Đừng thu hẹp con đường thành một kỹ thuật],
  [
    Chánh niệm chỉ là một phần của Bát Chánh Đạo, tức toàn bộ con đường tu. Con đường ấy còn đòi thấy đúng, sống có giới, nỗ lực đúng, làm tâm vững và học với người đáng tin. Bạn chưa cần nhớ tên từng chi ở đây. Chỉ cần đừng lầm một kỹ thuật ghi nhận với cả con đường, hoặc lầm việc lặp nhãn với tuệ giác và thánh quả.
  ],
)

== Lộ trình đọc cho người mới

Phần này cố tình đọc chậm hơn phần thực hành. Người mới không cần hiểu hết ngay; chỉ cần biết phải đọc chương nào trước, chương nào sau, và đoạn nào nên để lại làm tài liệu tham chiếu.

#practice-card(
  [Đọc theo nhu cầu, không cần nuốt trọn từ đầu đến cuối],
  [
    1. *Trước buổi đầu:* mở #link(<buoi-dau>)[“Trước buổi đầu tiên”] ở chương 1. Đọc hai hộp an toàn và thẻ Ngày 1; để #link(<nhan-tham-chieu>)[bảng nhãn ở Phụ lục B] bên cạnh nếu các từ ghi nhận còn lạ. Nếu hai hộp không nêu điều đang xảy ra với bạn, hãy bắt đầu buổi ngồi ngắn. Nếu một dấu hiệu cảnh báo áp dụng, dừng ở đó và đọc #link(<an-toan>)[chương 9] trước khi tiếp tục.

    2. *Sau tuần đầu:* dùng #link(<ngay-8-30>)[cầu nối ngày 8 đến ngày 30] trong chương 1, đồng thời đọc xong chương 2 đến chương 7 để đặt kỹ thuật vào giới, Bát Chánh Đạo, Tứ Niệm Xứ, duyên khởi và đời sống tại gia. Khi cần gom các phần ấy vào một phản ứng thật, đọc Chương 13; đây là bản đồ truy hồi, không phải một phương pháp mới. Sau đó đọc chương 10 theo thẻ “Đường đọc lần đầu”. Nếu ba kiết sử đầu còn lẫn vào nhau, hãy dừng ở chương 10 và dùng phần thuật ngữ hoặc FAQ để đọc lại. Chương 11 chỉ mở rộng bản đồ sang năm hạ phần kiết sử và bốn quả; nó không phải kỳ thi, cũng không phải bảng tự phong cấp.

    3. *Trước khi tăng mạnh thời lượng, tập một mình dài ngày hoặc đi khóa:* đọc chương 8 và đọc trọn #link(<an-toan>)[chương 9], kiểm tra sức khỏe, người hướng dẫn và quyền rời khóa.

    4. *Chương 12 để về sau:* trong những tuần hoặc tháng đầu, chỉ đọc #link(<ban-do-tue-la-gi>)[phần “Bản đồ tuệ là gì?”], ba mức kết luận, ranh giới “làm sao đạt” và lối đọc ba lượt; rồi dừng trước phần bảy thanh tịnh. Khi cần tra cứu với người hướng dẫn, mới đọc tiếp từng vùng. Đừng dùng tên tầng tuệ để tự phong cấp cho một trải nghiệm.

    Phần còn lại của chương 12, #link(<faq>)[FAQ] và #link(<thuat-ngu>)[bảng thuật ngữ] là nơi tra cứu khi cần. Nếu một chỉ dẫn trong sách xung đột với an toàn, giới hoặc bổn phận thiết yếu, hãy dừng và kiểm tra lại thay vì cố hoàn thành lịch.
  ],
  label: [BẮT ĐẦU Ở ĐÂY · BIÊN SOẠN],
)

== Sáu dấu nguồn dùng trong sách

Mỗi đoạn mang tính giáo lý hoặc kỹ thuật sẽ được đặt gần một dấu nguồn. Dấu nguồn không xếp hạng giá trị tinh thần; nó ngăn người đọc gán lời của một thiền sư hay người biên soạn cho Đức Phật.

#source-line("KINH", [MN 10; SN 55], [Các bài kinh thuộc Nikāya Pāli, gồm lời được truyền thống quy về Đức Phật và lời của các vị Thánh đệ tử. Mã kinh xác định ai nói và trong ngữ cảnh nào; dấu này không có nghĩa mọi câu trong kinh đều là lời Phật trực tiếp.])

#v(7pt)
#source-line("LUẬN GIẢI", [A-tỳ-đàm và chú giải], [Các hệ thống phân tích được hình thành và phát triển trong truyền thống Theravāda về sau.])

#v(7pt)
#source-line("THANH TỊNH ĐẠO", [Vism], [Tác phẩm tổng hợp của ngài Buddhaghosa, khoảng thế kỷ V. Sách có ảnh hưởng lớn nhưng không phải lời Phật trực tiếp.])

#v(7pt)
#source-line("MAHĀSI", [thế kỷ XX], [Chỉ dẫn về phồng xẹp, ghi nhận hiện tượng trong tâm, thiền hành chậm và trình pháp theo dòng truyền thừa Mahāsi. P01 dặn không đọc thành tiếng hay tụng lặp các từ ghi nhận.])

#v(7pt)
#source-line("Y TẾ & NGHIÊN CỨU", [hiện đại], [Nghiên cứu đương đại cùng hướng dẫn chính thức của các cơ quan y tế chỉ được dùng cho câu hỏi an toàn và sức khỏe. Chúng không được dùng để chứng minh giáo lý, nghiệp, tái sinh hay thánh quả.])

#v(7pt)
#source-line("BIÊN SOẠN", [hiện đại], [Lịch thực hành, cách tạo thói quen, bảng tự kiểm và các nguyên tắc an toàn được biên soạn cho đời sống hôm nay.])

== Đọc AN, SN, MN, DN và các mã P01, P02 thế nào? <doc-ma-nguon>

#practice-card(
  [Một phút để đọc mã nguồn],
  [
    + *DN* là *Dīgha Nikāya*, Trường Bộ; *MN* là *Majjhima Nikāya*, Trung Bộ.
    + *SN* là *Saṃyutta Nikāya*, Tương Ưng Bộ; *AN* là *Aṅguttara Nikāya*, Tăng Chi Bộ.
    + *Ud* là *Udāna*, thường gọi là Kinh Phật Tự Thuyết.
    + Số sau chữ viết tắt chỉ vị trí bài kinh trong bộ sưu tập đang dùng. Chẳng hạn, *MN 10* là bài số 10 của Trung Bộ; *SN 55.5* là bài số 5 trong nhóm 55 của Tương Ưng Bộ; *AN 3.88* là bài số 88 trong chương Ba pháp của Tăng Chi Bộ.
    + *K01, K02…* là số hồ sơ nguồn kinh do chính cuốn sách này đặt để nối một mệnh đề với đúng liên kết, bản dịch và ghi chú ở #link(<ma-nguon-chi-tiet>)[Bản đồ nguồn]. K01 không có nghĩa “kinh số 1” trong Tam tạng.
    + *P01* và *P02* là hai tài liệu Mahāsi được sách khóa: _Practical Insight Meditation_ và _The Progress of Insight_. *V01* là ấn bản _The Path of Purification_, tức _Thanh Tịnh Đạo_, được dùng trong sách.
    + *R01, R02…* là nguồn nghiên cứu, y tế hoặc cơ quan chính thức dùng cho các mệnh đề an toàn. Chữ R không biến một nghiên cứu thành giáo lý và cũng không có nghĩa mọi nguồn R mạnh như nhau.

    Khi gặp hai mã cạnh nhau, chẳng hạn “K11 · MN 2”, hãy đọc thế này: K11 là hồ sơ truy nguyên của sách; MN 2 là địa chỉ bài kinh trong Trung Bộ. Mở Bản đồ nguồn để xem tên bài, bản dịch, liên kết và giới hạn của cách dùng.
  ],
  label: [TRA NHANH · QUY ƯỚC THƯ MỤC],
)

== Cách dùng cuốn sách

Nếu chưa từng hành thiền, hãy dùng lộ trình ở trên thay vì đọc tuyến tính. Nếu đã hành lâu, hãy đọc phần nguồn và an toàn trước khi dùng bản đồ tuệ. Khi có trải nghiệm mạnh, kéo dài hoặc làm suy giảm giấc ngủ và sinh hoạt, đừng tự gắn tên một tầng tuệ. Giảm cường độ và tìm người hướng dẫn đủ năng lực; khi cần, tìm hỗ trợ y tế.

Khi đang hành mà không nhớ nên giữ đối tượng, chuyển sang điều đang nổi bật, hành động ngay hay dừng, mở #link(<ban-do-quyet-dinh>)[Bản đồ quyết định ở Phụ lục E]. Đây là thẻ gợi nhớ; phần giải thích đầy đủ vẫn nằm trong các chương liên quan.

Nếu bạn mới bắt đầu, hãy coi chương 12 là tài liệu tham khảo về sau, không phải nơi tự chẩn đoán trong những tuần đầu.

#pagebreak()

#heading(level: 1, outlined: true)[#edition.labels.toc]

#v(5mm)
#outline(title: none, depth: 2, indent: auto)

#pagebreak()

Câu kinh sau là trục của toàn sách. Nếu các từ “thân, thọ, tâm, pháp” hoặc “nhiệt tâm, tỉnh giác, chánh niệm” còn lạ, cứ đọc để nhận mặt; chương 3 sẽ giải thích từng phần bằng ngôn ngữ thực hành.

#scripture-quote(
  [Có bốn nền tảng chánh niệm: quán thân nơi thân, quán thọ nơi thọ, quán tâm nơi tâm và quán pháp nơi pháp, với nhiệt tâm, tỉnh giác và chánh niệm, sau khi chế ngự tham ưu đối với đời.],
  [Phỏng dịch sát ý từ Kinh Niệm xứ, MN 10, đoạn mở đầu. Xem nguồn K01.],
)

#v(9mm)

#modern-note([
  Bản dịch trong sách ưu tiên diễn ý rõ ràng và luôn nêu mã kinh. Khi trích nguyên văn bản dịch đã xuất bản, sách ghi tên dịch giả. Thuật ngữ Pāli chỉ được giữ lại khi nó ngăn một hiểu lầm quan trọng.
])
