#import "../components.typ": *

#let term-card(pali, vietnamese, refs, body, kind: "BIÊN SOẠN") = practice-card(
  [#pali · #vietnamese],
  [
    #body
    #v(6pt)
    #source-badge(kind, refs: refs)
  ],
  label: [THUẬT NGỮ PĀLI],
)

#pagebreak(weak: true)
#v(7mm)
#eyebrow([PHỤ LỤC D], fill: palette.saffron)
#v(4mm)
= Thuật ngữ cốt lõi

#text(font: fonts.sans, size: 9.5pt, fill: palette.muted)[
  Dịch một từ Pāli bằng một từ Việt có thể tiện, nhưng không bao giờ giữ trọn mọi sắc thái. Các định nghĩa dưới đây chỉ đủ dùng cho cuốn sổ tay này.
]

#v(8mm)

#term-card(
  [sati],
  [chánh niệm],
  [K01; K12],
  [
    Khả năng giữ điều cần được biết trong tầm chú ý, không quên nhiệm vụ quan sát và nhận ra khi tâm đã rời nó. Trong Niệm xứ, *sati* đi cùng nhiệt tâm và tỉnh giác. Nó không chỉ là thư giãn, cũng không phải thái độ chấp nhận mọi ý nghĩ là đúng.
  ],
)

#v(7pt)

#term-card(
  [sampajañña],
  [tỉnh giác, biết rõ],
  [K01],
  [
    Sự biết rõ việc đang làm và tình huống hiện tại. Nếu *sati* giúp không quên nhiệm vụ quan sát, *sampajañña* giúp biết rõ mình đang đi, đứng, co hay duỗi. Hai năng lực hỗ trợ nhau nhưng không đồng nghĩa.
  ],
)

#v(7pt)

#term-card(
  [samādhi],
  [định, tâm thu nhiếp],
  [K05; K12; K26],
  [
    Sự ổn định và quy tụ của tâm. Trong công thức phân tích Bát Thánh đạo, K26 định nghĩa chánh định bằng bốn tầng thiền. Một phút dễ chịu hay không có ý nghĩ chưa đủ để gọi là chánh định; định còn phải đứng trong chánh kiến, giới và các chi đạo khác.
  ],
)

#v(7pt)

#term-card(
  [paññā],
  [tuệ, trí thấy đúng],
  [K05; K17],
  [
    Năng lực phân biệt và thấy đúng thực tại theo Pháp, nhất là khổ, nguyên nhân, sự chấm dứt và con đường. *Paññā* không đồng nghĩa với kiến thức thuộc lòng, trải nghiệm lạ hay khả năng diễn giải trạng thái thiền.
  ],
)

#v(7pt)

#term-card(
  [sotāpanna],
  [bậc Nhập lưu, Dự lưu],
  [K03; K06; K08; K10],
  [
    Người đã bước vào dòng Thánh đạo, đoạn tận ba kiết sử đầu và có những phẩm chất được kinh mô tả về tịnh tín cùng giới hạnh. Đây là một thành tựu xác định trong giáo pháp, không phải tên đẹp cho người mới hành thiền, người sống bình tĩnh hơn hay người vừa có một kinh nghiệm mạnh.
  ],
)

#v(7pt)

#term-card(
  [vedanā],
  [thọ],
  [K01; K20],
  [
    Sắc thái dễ chịu, khó chịu hoặc trung tính sinh trên nền tiếp xúc. *Vedanā* không phải toàn bộ cảm xúc. Một cơn giận có thể gồm thọ khó chịu, nóng nơi thân, nhận diện một người, ký ức, ý nghĩ và ý muốn đáp trả.
  ],
)

#v(7pt)

#practice-card(
  [satipaṭṭhāna · niệm xứ],
  [
    Sự thiết lập hay nền tảng của chánh niệm trên bốn lĩnh vực: thân, thọ, tâm và pháp. K01 mô tả từng lĩnh vực và điệp khúc quán sự sinh, diệt. “Niệm xứ” không đồng nghĩa với riêng kỹ thuật ghi nhãn.

    #v(6pt)
    #source-badge("KINH", refs: [K01])
  ],
  label: [THUẬT NGỮ PĀLI],
)

#v(7pt)

#practice-card(
  [samatha và vipassanā · chỉ và quán],
  [
    *Samatha* chỉ sự lắng dịu, ổn định của tâm. *Vipassanā* chỉ sự thấy rõ đặc tính và điều kiện của kinh nghiệm. K16 cho thấy nhiều cách hai mặt tu tập này được phát triển. Không nên dựng chúng thành hai phe loại trừ nhau.

    #v(6pt)
    #source-badge("KINH", refs: [K16])
  ],
  label: [CẶP THUẬT NGỮ],
)

#v(7pt)

#term-card(
  [cetanā và manasikāra],
  [tư, ý định và tác ý],
  [K02; K20],
  [
    *Cetanā* là tư hay ý định; K20 dùng từ này khi định nghĩa nghiệp. *Manasikāra* là sự hướng tâm hoặc tác ý; trong cụm *yoniso manasikāra*, nó chỉ như lý tác ý. Một số bản dịch Việt dùng “tác ý” cho cả hai, nhưng hai thuật ngữ không đồng nghĩa.
  ],
)

#v(7pt)

#practice-card(
  [noting · ghi nhận trong tâm],
  [
    Quy ước nhận biết ngắn như “phồng”, “nghe” hoặc “nghĩ” để hỗ trợ bám sát hiện tượng. P01 dạy ghi nhận trong tâm nhưng dặn không đọc thành tiếng hay nghĩ về “phồng, xẹp” như những từ cần lặp. Kỹ thuật này nổi bật trong dòng Mahāsi; bảng nhãn tiếng Việt ở Phụ lục B do sách biên soạn, không nằm nguyên dạng trong K01 hay P01.

    #v(6pt)
    #source-badge("MAHĀSI", refs: [P01])
    #h(4pt)
    #source-badge("BIÊN SOẠN")
  ],
  label: [PHƯƠNG PHÁP],
)

#v(8pt)

#caution(
  [Đừng dùng thuật ngữ để nâng cấp kinh nghiệm],
  [
    Một trải nghiệm chỉ nên mang tên Pāli khi định nghĩa và bối cảnh thật sự khớp. Nếu chưa chắc, hãy mô tả điều đã xảy ra bằng ngôn ngữ thường: cảm giác, thời lượng, điều kiện trước đó và ảnh hưởng lên hành vi.
  ],
)
