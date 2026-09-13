#import "../components.typ": *
#import "../edition.typ": edition

#context {
  if target() == "html" {
    html.elem("header", attrs: (class: "introduction-opener"))[
      #html.elem("p", attrs: (class: "eyebrow"))[#edition.labels.introduction]
      #heading(level: 1, outlined: true)[Cùng bắt đầu từ điều gần gũi]
    ]
  } else {
    align(center)[
      #v(12mm)
      #eyebrow(edition.labels.introduction, fill: palette.saffron)
      #v(6mm)
      #heading(level: 1, outlined: true)[Cùng bắt đầu từ điều gần gũi]
    ]
  }
}

#v(10mm)

Có thể bạn tìm đến cuốn sách này vì muốn hiểu lời Phật hơn, muốn bớt bị những phản ứng quen thuộc kéo đi, hoặc muốn biết người tại gia có thể bắt đầu tu tập thế nào. Bạn không cần hiểu hết thuật ngữ trước khi mở trang đầu. Ta sẽ đi từ những việc gần: học giữ giới, nhận biết thân tâm và đem điều đã hiểu vào đời sống.

Sách lấy các bài kinh trong kinh điển Pāli làm nền giáo lý, đồng thời giới thiệu cách thực hành Niệm xứ theo truyền thống Mahāsi. Phương pháp của một truyền thống, lời giải thích của người biên soạn và lời kinh được đặt riêng. Đây là sách hướng dẫn có tham khảo nguồn, không phải một bản kinh mới, cũng không coi mọi chỉ dẫn trong sách là lời Phật trực tiếp.

#source-line("BIÊN SOẠN", [ba cách hiểu để bắt đầu; đối chiếu K01 · P01 · K06], [
  *Niệm xứ* nói đến việc tu tập chánh niệm đối với thân, thọ, tâm và pháp. Để dễ theo dõi, bạn có thể tạm hiểu: nhận biết thân; nhận biết cảm thọ dễ chịu, khó chịu hay trung tính; nhận biết trạng thái tâm; và xem xét kinh nghiệm theo những nhóm pháp được bài kinh nêu.

  *Mahāsi* là một truyền thống thiền Theravāda hiện đại. Sách giới thiệu các chỉ dẫn về chuyển động bụng, ghi nhận trong tâm và thiền hành từ nguồn của truyền thống ấy. Chúng được phân biệt với nguyên văn Kinh Niệm xứ.

  *Nhập lưu* là quả vị được kinh mô tả trong mối liên hệ với Bát Chánh Đạo và sự đoạn trừ ba kiết sử đầu. Đây không phải tên khác của một lúc yên tâm. Các chương sau sẽ giải thích từng phần; ở đây, chỉ cần biết hướng của cuốn sách.
])

Tên sách là *Hướng Đến Nhập Lưu*. “Hướng đến” nói rõ phạm vi: cùng học lời dạy và những điều kiện nâng đỡ việc tu. Sách không ấn định ngày chứng quả, không lấy thời lượng ngồi làm thước đo thành tựu, và không xác nhận thánh quả từ một trải nghiệm được kể lại.

#v(8pt)

#caution(
  [Giữ toàn bộ con đường trong tầm nhìn],
  [
    #source-badge("BIÊN SOẠN", refs: [đối chiếu K06 · SN 55.5])
    #v(5pt)
    Chánh niệm nằm trong Bát Chánh Đạo, cùng với thấy đúng, ý hướng đúng, lời nói, hành động, cách nuôi sống, nỗ lực và định. Một cách ghi nhận có thể giúp tổ chức buổi thiền; việc học và tu những phần còn lại vẫn cần được chăm sóc. Bạn có thể bắt đầu từng chút mà không thu hẹp con đường vào một kỹ thuật.
  ],
)

== Lộ trình đọc cho người mới

Bạn có thể đọc theo nhu cầu, không cần đi hết sách từ đầu đến cuối mới được thực hành. Phần bản đồ tuệ ở cuối là tài liệu tham khảo về sau, không phải bài học phải hoàn thành trong những tuần đầu.

#practice-card(
  [Bắt đầu với phần cần dùng],
  [
    + *Tuần đầu:* mở Chương 1, đọc #link(<buoi-dau>)[“Trước buổi đầu tiên”], các hộp an toàn và thẻ Ngày 1. Có thể để #link(<nhan-tham-chieu>)[bảng nhãn ở Phụ lục B] bên cạnh. Nếu có dấu hiệu cảnh báo áp dụng cho mình, dừng ở đó và đọc #link(<an-toan>)[Chương 9] trước khi tiếp tục.
    + *Sau tuần đầu:* đọc Chương 2–7 và #link(<ngay-8-30>)[gợi ý ngày 8 đến ngày 30]. Khi muốn nối các ý đã học, dùng Chương 12 để ôn lại qua một tình huống đời thường.
    + *Trước khi tăng mạnh thời lượng, tập một mình dài ngày hoặc đi khóa:* đọc Chương 8–9, kiểm tra điều kiện sức khỏe, người hướng dẫn và quyền dừng hoặc rời khóa.
    + *Khi muốn hiểu Nhập lưu:* đọc Chương 10–12. Thuật ngữ chưa rõ có thể được tra lại; không cần vội dùng chúng để nhận định sự chứng đắc của mình.
    + *Với Chương 13:* nên có nền thực hành và hướng dẫn phù hợp trước khi đọc sâu các phân loại. Trong tháng đầu, có thể đọc #link(<ban-do-tue-la-gi>)[“Bản đồ tuệ là gì?”] rồi để phần chi tiết lại sau. Đây là gợi ý cách dùng sách, không phải thời hạn trong kinh.

    #link(<faq>)[Phụ lục C] giải đáp các câu hỏi thường gặp. Nếu một chỉ dẫn xung đột với an toàn, giới hoặc bổn phận thiết yếu, hãy dừng và kiểm tra lại thay vì cố hoàn thành lịch.
  ],
  label: [BẮT ĐẦU Ở ĐÂY · BIÊN SOẠN],
)

== Sáu dấu nguồn dùng trong sách

Các dấu dưới đây giúp trả lời một câu hỏi: “Điều mình đang đọc đến từ đâu?”. Một đoạn lời kinh, một cách giải thích về sau và một bài tập do sách đặt ra có vai trò khác nhau. Sự gần nhau trên trang không làm chúng trở thành cùng một loại nguồn.

#source-line("KINH", [kinh điển Pāli], [
  Nội dung từ bài kinh được nêu rõ mã nguồn và ngữ cảnh, gồm những bài thuộc các bộ Nikāya và các tập Tiểu Bộ được dẫn. Trong kinh có lời của Đức Phật, lời của các vị đệ tử và phần kể chuyện. Dấu này không có nghĩa mọi câu đều do Đức Phật trực tiếp nói. Khi diễn ý, sách ghi đó là diễn ý; khi trích nguyên văn một bản dịch, cần giữ đúng lời và ghi tên dịch giả.
])

#v(7pt)
#source-line("LUẬN GIẢI", [A-tỳ-đàm và truyền thống chú giải], [Các cách phân tích, hệ thống hóa của truyền thống Theravāda. Chúng được phân biệt với lời trực tiếp trong các bài kinh, không được dùng để âm thầm thay nghĩa của kinh.])

#v(7pt)
#source-line("THANH TỊNH ĐẠO", [Visuddhimagga], [Tác phẩm của ngài Buddhaghosa được dùng làm nguồn tham khảo riêng cho hệ thống tu tập và bản đồ tuệ. Sách không trình bày tác phẩm này như lời Phật trực tiếp.])

#v(7pt)
#source-line("MAHĀSI", [nguồn thực hành của truyền thống Mahāsi], [Các chỉ dẫn về phồng xẹp, ghi nhận trong tâm, thiền hành và trình bày kinh nghiệm với người hướng dẫn. Khi dùng một chỉ dẫn cụ thể, sách nêu tài liệu tham khảo tương ứng.])

#v(7pt)
#source-line("Y TẾ & NGHIÊN CỨU", [nguồn hiện đại], [Nghiên cứu và hướng dẫn y tế phục vụ câu hỏi sức khỏe, an toàn. Chúng không được dùng như bằng chứng xác nhận nghiệp, tái sinh hay thánh quả.])

#v(7pt)
#source-line("BIÊN SOẠN", [giải thích và ứng dụng của sách], [Lời giải nghĩa gần gũi, ví dụ gia đình hoặc công việc, lịch thực hành, câu hỏi nhìn lại và hướng dẫn an toàn hiện đại. Những phần này giúp người đọc sử dụng sách, không được coi là lời dạy nguyên văn hoặc công thức bảo đảm chứng quả.])

Các dấu nguồn không thay cho việc đọc kỹ. Khi một đoạn có cả nội dung kinh và ứng dụng mới, cần phân biệt hai phần. Chỗ nào còn nhiều cách hiểu cần được nói rõ, thay vì chọn cách dễ thuyết phục nhất rồi coi là kết luận chắc chắn.

== Đọc AN, SN, MN, DN và các mã P01, P02 thế nào? <doc-ma-nguon>

#practice-card(
  [Tên bộ và số bài],
  [
    *DN* là *Dīgha Nikāya*, Trường Bộ; *MN* là *Majjhima Nikāya*, Trung Bộ.

    *SN* là *Saṃyutta Nikāya*, Tương Ưng Bộ; *AN* là *Aṅguttara Nikāya*, Tăng Chi Bộ.

    *Ud* là *Udāna*, Kinh Phật Tự Thuyết; *Iti* là *Itivuttaka*, Kinh Phật Thuyết Như Vậy; *Dhp* là *Dhammapada*, Pháp Cú. Ba tập này thuộc Tiểu Bộ trong kinh điển Pāli Theravāda.

    *MN 10* chỉ bài 10 của Trung Bộ. *SN 55.5* chỉ bài 5 trong tương ưng 55. *AN 3.88* chỉ bài 88 trong chương Ba pháp của hệ đánh số đang dùng. Mã giúp tìm nguồn; không cần thuộc mã trước khi thực hành.
  ],
  label: [TRA NHANH · TÊN VÀ SỐ KINH],
)

#v(7pt)

#practice-card(
  [Các mã riêng của cuốn sách],
  [
    *K01, K02…* là mã tra do sách đặt: K01 không có nghĩa “kinh số 1”. Mở #link(<ma-nguon-chi-tiet>)[Bản đồ nguồn] để tìm bài, bản dịch và liên kết tương ứng.

    *P01* và *P02* là _Practical Insight Meditation_ và _The Progress of Insight_, hai tài liệu Mahāsi. *V01* là ấn bản Thanh Tịnh Đạo được tham khảo. *BPS* là _Buddhist Publication Society_, nhà xuất bản của những tài liệu được nêu trong bản đồ nguồn.

    *R01, R02…* chỉ nguồn nghiên cứu, y tế hoặc cơ quan chính thức. Mã R không có nghĩa mọi nguồn có cùng độ tin cậy hoặc cùng nhiệm vụ chứng minh.

    “K11 · MN 2” có nghĩa K11 là mã của sách, còn MN 2 là địa chỉ bài kinh. Những mã này hỗ trợ kiểm tra, không chứng nhận rằng mọi lời giải thích đều đã đúng.
  ],
  label: [TRA NHANH · QUY ƯỚC THƯ MỤC],
)

== Khi cần tìm lại bước kế tiếp

Trong lúc thực hành, nếu chưa rõ nên tiếp tục với đối tượng đang biết, chuyển sang điều nổi bật, hành động ngay hay dừng, hãy mở #link(<ban-do-quyet-dinh>)[Bản đồ quyết định ở Phụ lục E]. Đây là thẻ nhắc của sách; lời giải thích đầy đủ nằm ở các chương liên quan.

Khi trải nghiệm mạnh kéo dài, giấc ngủ xấu đi rõ, khả năng sinh hoạt giảm hoặc khó phân biệt thực tại, hãy dừng buổi hiện tại, không tiếp tục thực hành cường độ cao và tìm hỗ trợ theo #link(<ba-muc>)[Chương 9]. Không cần chờ biết tên trải nghiệm mới nhận hỗ trợ; cũng không cần xem việc dừng để chăm sóc mình là thất bại.

Bạn có thể trở lại một đoạn kinh nhiều lần. Đọc chậm, hỏi rõ điều chưa hiểu và thực hành một điều vừa sức là cách dùng cuốn sách này; không cần biến việc đọc thành cuộc chạy đua qua các tầng tuệ.

#pagebreak()

#heading(level: 1, outlined: true)[#edition.labels.toc]

#v(5mm)
#outline(title: none, depth: 1, indent: auto)

#pagebreak()

Đoạn mở đầu Kinh Niệm xứ dưới đây là một điểm tựa để trở lại trong khi đọc. Chương 3 sẽ giải thích những từ còn lạ.

#source-line("KINH", [K01 · MN 10:3.2–3.5, diễn ý], [
  Vị Tỷ-kheo sống quán thân nơi thân, nhiệt tâm, tỉnh giác, chánh niệm, chế ngự tham ưu đối với đời. Với thọ, tâm và pháp, bài kinh nêu cùng cách trình bày ấy.
])

#v(9mm)

#modern-note([
  Diễn ý giúp lời văn gần gũi hơn, nhưng không được thêm điều mà nguồn không nói. Những ví dụ và câu hỏi của sách chỉ có ích khi giúp người đọc trở lại lời dạy với sự hiểu biết rõ hơn.
])
