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

Có thể bạn tìm đến cuốn sách này vì muốn hiểu lời Phật hơn, muốn bớt bị những phản ứng quen thuộc cuốn đi, hoặc muốn biết người tại gia có thể bắt đầu tu tập thế nào. Bạn không cần hiểu hết thuật ngữ trước khi mở trang đầu. Ta sẽ đi từ những việc gần: học giữ giới, nhận biết thân tâm và đem điều đã hiểu vào đời sống.

Sách lấy các bài kinh trong kinh điển Pāli làm nền giáo lý, đồng thời giới thiệu cách thực hành Niệm xứ theo truyền thống Mahāsi. Lời kinh, phương pháp của một truyền thống và lời giải thích của chính cuốn sách được trình bày tách riêng. Đây là sách hướng dẫn có tham khảo nguồn, không phải một bản kinh mới, cũng không coi mọi chỉ dẫn trong sách là lời Phật trực tiếp.

#source-line("BIÊN SOẠN", [Ba ý cần nắm trước khi bắt đầu, được sách tóm lược từ #ten("K01"), sách _#ten("P01")_ của Thiền sư Mahāsi và #ten("K06")], [
  *Niệm xứ* nói đến việc tu tập chánh niệm đối với thân, thọ, tâm và pháp. Để dễ theo dõi, bạn có thể tạm hiểu: nhận biết thân; nhận biết cảm thọ dễ chịu, khó chịu hay trung tính; nhận biết trạng thái tâm; và xem xét kinh nghiệm theo những nhóm pháp được bài kinh nêu.

  *Mahāsi* là một truyền thống thiền Theravāda hiện đại. Sách giới thiệu các chỉ dẫn về chuyển động bụng, ghi nhận trong tâm và thiền hành từ nguồn của truyền thống ấy. Chúng được phân biệt với nguyên văn Kinh Niệm Xứ.

  *Nhập lưu* là quả vị (một thành quả tu tập) được kinh mô tả trong mối liên hệ với Bát Chánh Đạo và sự đoạn trừ ba kiết sử đầu (ba mối trói buộc đầu tiên). Đây không phải tên khác của một lúc yên tâm. Các chương sau sẽ giải thích từng phần; ở đây, chỉ cần biết hướng của cuốn sách.
])

Tên sách là *Hướng Đến Nhập Lưu*. “Hướng đến” nói rõ phạm vi: cùng học lời dạy và những điều kiện nâng đỡ việc tu. Sách không ấn định ngày chứng quả, không lấy thời lượng ngồi làm thước đo thành tựu, và không xác nhận thánh quả từ một trải nghiệm được kể lại.

#v(8pt)

#caution(
  [Giữ toàn bộ con đường trong tầm nhìn],
  [
    #source-badge("BIÊN SOẠN", refs: [Lời nhắc này được rút ra từ #nguon("K06")])
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
    + *Khi muốn hiểu Nhập lưu:* đọc Chương 10–12. Thuật ngữ chưa rõ có thể được tra lại; không cần vội dùng chúng để tự nhận định mình đã chứng đắc hay chưa.
    + *Với Chương 13:* nên có nền thực hành và hướng dẫn phù hợp trước khi đọc sâu các phân loại. Trong tháng đầu, có thể đọc #link(<ban-do-tue-la-gi>)[“Bản đồ tuệ là gì?”] rồi để phần chi tiết lại sau. Đây là gợi ý cách dùng sách, không phải thời hạn trong kinh.

    #link(<faq>)[Phụ lục C] giải đáp các câu hỏi thường gặp. Nếu một chỉ dẫn xung đột với an toàn, giới hoặc bổn phận thiết yếu, hãy dừng và kiểm tra lại thay vì cố hoàn thành lịch.
  ],
  label: [Bắt đầu ở đây: lộ trình đọc do sách gợi ý],
)

== Sáu dấu nguồn dùng trong sách

Các dấu dưới đây giúp trả lời một câu hỏi: “Điều mình đang đọc đến từ đâu?”. Một đoạn lời kinh, một cách giải thích về sau và một bài tập do sách đặt ra có vai trò khác nhau. Sự gần nhau trên trang không làm chúng trở thành cùng một loại nguồn.

Mỗi dấu gồm một biểu tượng nhỏ và một câu dẫn nguồn. Biểu tượng cho biết loại nguồn; câu đi kèm nói rõ bài kinh, tác phẩm hay tài liệu cụ thể, chẳng hạn “Theo #nguon("K01")”. Riêng biểu tượng cây bút đánh dấu phần do sách soạn: lời giải thích, ví dụ, bài tập và lịch thực hành. Sách không lặp lại chữ “biên soạn” ở từng chỗ, để việc đọc và nghe được liền mạch.

#source-line("KINH", [Kinh điển Pāli], [
  Nội dung từ bài kinh được nêu rõ tên bài, vị trí và ngữ cảnh, gồm những bài thuộc các bộ Nikāya và một số bài thuộc Tiểu Bộ. Trong kinh có lời của Đức Phật, lời của các vị đệ tử và phần kể chuyện. Dấu này không có nghĩa mọi câu đều do Đức Phật trực tiếp nói. Khi diễn ý, sách ghi đó là diễn ý; khi trích nguyên văn một bản dịch, cần giữ đúng lời và ghi tên dịch giả.
])

#v(7pt)
#source-line("LUẬN GIẢI", [Luận giải: A-tỳ-đàm và truyền thống chú giải], [Các cách phân tích, hệ thống hóa của truyền thống Theravāda. Chúng được phân biệt với lời trực tiếp trong các bài kinh, không được dùng để âm thầm thay nghĩa của kinh.])

#v(7pt)
#source-line("THANH TỊNH ĐẠO", [Thanh Tịnh Đạo (Visuddhimagga)], [Tác phẩm của ngài Buddhaghosa được dùng làm nguồn tham khảo riêng cho hệ thống tu tập và bản đồ tuệ. Sách không trình bày tác phẩm này như lời Phật trực tiếp.])

#v(7pt)
#source-line("MAHĀSI", [Truyền thống thiền Mahāsi], [Các chỉ dẫn về phồng xẹp, ghi nhận trong tâm, thiền hành và trình bày kinh nghiệm với người hướng dẫn. Khi dùng một chỉ dẫn cụ thể, sách nêu tài liệu tham khảo tương ứng.])

#v(7pt)
#source-line("Y TẾ & NGHIÊN CỨU", [Y tế và nghiên cứu hiện đại], [Nghiên cứu và hướng dẫn y tế phục vụ câu hỏi sức khỏe, an toàn. Chúng không được dùng như bằng chứng xác nhận nghiệp, tái sinh hay thánh quả.])

#v(7pt)
#source-line("BIÊN SOẠN", [Phần do sách soạn (biểu tượng cây bút)], [Lời giải nghĩa gần gũi, ví dụ gia đình hoặc công việc, lịch thực hành, câu hỏi nhìn lại và hướng dẫn an toàn hiện đại. Những phần này giúp người đọc sử dụng sách, không được coi là lời dạy nguyên văn hoặc công thức bảo đảm chứng quả.])

Các dấu nguồn không thay cho việc đọc kỹ. Khi một đoạn có cả nội dung kinh và ứng dụng mới, cần phân biệt hai phần. Ở chỗ còn nhiều cách hiểu, sách cần nói rõ điều đó, thay vì chọn cách dễ thuyết phục nhất rồi coi là kết luận chắc chắn.

== Tên bộ kinh và cách tìm lại nguồn <doc-ma-nguon>

#practice-card(
  [Tên bộ và số bài],
  [
    Kinh điển Pāli của Theravāda gồm năm bộ kinh. *Trường Bộ* (_Dīgha Nikāya_) gồm những bài kinh dài; *Trung Bộ* (_Majjhima Nikāya_) gồm những bài dài vừa; *Tương Ưng Bộ* (_Saṃyutta Nikāya_) xếp các bài theo chủ đề; *Tăng Chi Bộ* (_Aṅguttara Nikāya_) xếp các bài theo số pháp, từ một đến mười một. *Tiểu Bộ* gồm nhiều tập nhỏ, trong đó có Kinh Phật Tự Thuyết (_Udāna_), Kinh Phật Thuyết Như Vậy (_Itivuttaka_) và Kinh Pháp Cú (_Dhammapada_).

    Sách viết vị trí đầy đủ thay vì chữ viết tắt. “Trung Bộ, bài số 10” là bài thứ mười của Trung Bộ. “Tương Ưng Bộ, chương 55, bài số 5” là bài thứ năm trong chương 55. “Tăng Chi Bộ, chương Ba Pháp, bài số 88” là bài thứ tám mươi tám trong chương nói về các nhóm ba pháp. Không cần thuộc những con số này trước khi thực hành.

    Tài liệu học thuật thường dùng chữ viết tắt: *DN* là *Dīgha Nikāya*, Trường Bộ; *MN* là *Majjhima Nikāya*, Trung Bộ; *SN* là *Saṃyutta Nikāya*, Tương Ưng Bộ; *AN* là *Aṅguttara Nikāya*, Tăng Chi Bộ; *Ud* là *Udāna*, *Iti* là *Itivuttaka* và *Dhp* là *Dhammapada*. Ví dụ, Kinh Niệm Xứ thường được ghi là MN 10. Trong thân sách, vị trí luôn được viết đầy đủ; Bản đồ nguồn cuối sách giữ thêm chữ viết tắt để bạn tra cứu ở nơi khác.
  ],
  label: [Tra nhanh tên bộ và số bài kinh],
)

#v(7pt)

#practice-card(
  [Tìm lại nguồn trong Bản đồ nguồn],
  [
    Tên một bài kinh hay tài liệu trong các dấu nguồn thường là một liên kết. Bấm vào đó, hoặc mở #link(<ma-nguon-chi-tiet>)[Bản đồ nguồn] ở cuối sách, để thấy bản dịch đã dùng, giới hạn của nguồn và đường dẫn đến bản trực tuyến.

    Trong Bản đồ nguồn, mỗi mục còn có một mã tra ngắn do sách đặt. *K01, K02…* là các bài kinh; K01 không có nghĩa “kinh số 1”. *P01* và *P02* là hai sách của Thiền sư Mahāsi; *V01* là ấn bản Thanh Tịnh Đạo được tham khảo; *R01, R02…* là nguồn nghiên cứu, y tế và cơ quan chính thức. Chữ cái không xếp hạng độ tin cậy.

    Hai sách của Thiền sư Mahāsi là _Practical Insight Meditation_ (sách dịch tạm là _Thiền Minh Sát Thực Hành_) và _The Progress of Insight_ (_Tiến Trình Minh Sát_). Bản đồ nguồn ghi rõ ấn bản của từng tài liệu; *BPS* là _Buddhist Publication Society_, nhà xuất bản của một số tài liệu trong đó. Dẫn nguồn giúp kiểm tra; nó không chứng nhận rằng mọi lời giải thích đều đã đúng.
  ],
  label: [Tra nhanh cách tìm lại nguồn],
)

== Khi cần tìm lại bước kế tiếp

Trong lúc thực hành, có bốn lựa chọn: tiếp tục với đối tượng đang biết, chuyển sang điều nổi bật, hành động ngay, hoặc dừng. Nếu chưa rõ nên chọn cách nào, hãy mở #link(<ban-do-quyet-dinh>)[Bản đồ quyết định ở Phụ lục E]. Đó là thẻ nhắc do sách soạn; lời giải thích đầy đủ nằm ở các chương liên quan.

Khi trải nghiệm mạnh kéo dài, giấc ngủ xấu đi rõ, khả năng sinh hoạt giảm hoặc khó phân biệt thực tại, hãy dừng buổi hiện tại, không tiếp tục thực hành cường độ cao và tìm hỗ trợ theo #link(<ba-muc>)[Chương 9]. Không cần chờ biết tên trải nghiệm mới nhận hỗ trợ; cũng không cần xem việc dừng để chăm sóc mình là thất bại.

Bạn có thể trở lại một đoạn kinh nhiều lần. Đọc chậm, hỏi rõ điều chưa hiểu và thực hành một điều vừa sức là cách dùng cuốn sách này; không cần biến việc đọc thành cuộc chạy đua qua các tầng tuệ.

#pagebreak()

#heading(level: 1, outlined: true)[#edition.labels.toc]

#v(5mm)
#outline(title: none, depth: 1, indent: auto)

#pagebreak()

Đoạn mở đầu Kinh Niệm Xứ dưới đây là một điểm tựa để trở lại trong khi đọc. Chương 3 sẽ giải thích những từ còn lạ.

#source-line("KINH", [Diễn ý đoạn mở đầu #nguon("K01", doan: "đoạn 3.2 đến 3.5")], [
  Vị Tỷ-kheo sống quán thân nơi thân, nhiệt tâm, tỉnh giác, chánh niệm, chế ngự tham ưu đối với đời. Với thọ, tâm và pháp, bài kinh nêu cùng cách trình bày ấy.
])

#v(9mm)

#modern-note([
  Diễn ý giúp lời văn gần gũi hơn, nhưng không được thêm điều mà nguồn không nói. Những ví dụ và câu hỏi của sách chỉ có ích khi giúp người đọc trở lại lời dạy với sự hiểu biết rõ hơn.
])
