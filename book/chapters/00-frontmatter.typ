#import "../components.typ": *

#context {
  if target() == "html" {
    html.elem("header", attrs: (class: "introduction-opener"))[
      #html.elem("p", attrs: (class: "eyebrow"))[LỜI DẪN]
      #heading(level: 1, outlined: true)[Một cuốn sổ tay, không phải giấy chứng nhận]
    ]
  } else {
    align(center)[
      #v(12mm)
      #eyebrow([LỜI DẪN], fill: palette.saffron)
      #v(6mm)
      #text(font: fonts.display, size: 24pt, weight: 600)[Một cuốn sổ tay, không phải giấy chứng nhận]
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
    1. *Trước buổi đầu:* đọc chương 1, rồi đọc các ngưỡng dừng ở chương 9. Thực hành lịch bảy ngày ở mức vừa sức.

    2. *Sau tuần đầu:* đọc chương 2 đến chương 7 để đặt kỹ thuật vào giới, Bát Chánh Đạo, Tứ Niệm Xứ, duyên khởi và đời sống tại gia.

    3. *Trước khi tăng mạnh thời lượng hoặc đi khóa:* đọc chương 8 và chương 9, kiểm tra sức khỏe, người hướng dẫn và quyền rời khóa.

    4. *Chương 10 để về sau:* trong những tuần hoặc tháng đầu, chỉ đọc hai phần đầu để biết nguồn và cách đếm, rồi dừng trước phần “Đọc bản đồ theo bốn vùng”. Đừng dùng tên tầng tuệ để tự phong cấp cho một trải nghiệm.

    Chương 11 và các phụ lục là nơi tra cứu khi cần. Nếu một chỉ dẫn trong sách xung đột với an toàn, giới hoặc bổn phận thiết yếu, hãy dừng và kiểm tra lại thay vì cố hoàn thành lịch.
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
#source-line("NGHIÊN CỨU", [hiện đại], [Nghiên cứu đương đại chỉ được dùng cho câu hỏi an toàn và sức khỏe. Nó không được dùng để chứng minh giáo lý, nghiệp, tái sinh hay thánh quả.])

#v(7pt)
#source-line("BIÊN SOẠN", [hiện đại], [Lịch thực hành, cách tạo thói quen, bảng tự kiểm và các nguyên tắc an toàn được biên soạn cho đời sống hôm nay.])

== Cách dùng cuốn sách

Nếu chưa từng hành thiền, hãy dùng lộ trình ở trên thay vì đọc tuyến tính. Nếu đã hành lâu, hãy đọc phần nguồn và an toàn trước khi dùng bản đồ tuệ. Khi có trải nghiệm mạnh, kéo dài hoặc làm suy giảm giấc ngủ và sinh hoạt, đừng tự gắn tên một tầng tuệ. Giảm cường độ và tìm người hướng dẫn đủ năng lực; khi cần, tìm hỗ trợ y tế.

Nếu bạn mới bắt đầu, hãy coi chương 10 là tài liệu tham khảo về sau, không phải nơi tự chẩn đoán trong những tuần đầu.

#pagebreak()

= Mục lục

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
