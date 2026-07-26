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
  [K05; K12; K25],
  [
    Sự ổn định và quy tụ của tâm. Trong công thức phân tích Bát Thánh đạo, K25 định nghĩa chánh định bằng bốn tầng thiền. Một phút dễ chịu hay không có ý nghĩ chưa đủ để gọi là chánh định; định còn phải đứng trong chánh kiến, giới và các chi đạo khác.
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
  [K01; K19],
  [
    Sắc thái dễ chịu, khó chịu hoặc trung tính sinh trên nền tiếp xúc. *Vedanā* không phải toàn bộ cảm xúc. Một cơn giận có thể gồm thọ khó chịu, nóng nơi thân, nhận diện một người, ký ức, ý nghĩ và ý muốn đáp trả.
  ],
)

#v(7pt)

#term-card(
  [khandha],
  [uẩn, nhóm kinh nghiệm],
  [K20],
  [
    Năm nhóm được kinh dùng để phân tích kinh nghiệm là sắc, thọ, tưởng, hành và thức. “Uẩn” không phải năm vật nằm tách rời trong người. Trong phần nói về thân kiến, điểm cần thấy là cách tâm nắm một uẩn như tự ngã, thuộc về tự ngã, nằm trong tự ngã hoặc chứa tự ngã.
  ],
)

#v(7pt)

#term-card(
  [saṃyojana],
  [kiết sử, trói buộc],
  [K11; K24],
  [
    Mối trói buộc bền chặt giữ hữu tình trong khổ, không phải tên chung cho mọi thói quen xấu. Chương 11 tập trung vào ba kiết sử gắn với Nhập lưu; K24 đặt chúng trong danh mục mười kiết sử rộng hơn.
  ],
)

#v(7pt)

#practice-card(
  [paṭiccasamuppāda · duyên khởi],
  [
    Sự sinh và diệt của khổ tùy thuộc điều kiện. K26 nêu chuỗi chuẩn từ vô minh đến già chết; K27 triển khai đoạn sáu cửa, xúc, thọ, ái và khổ. “Có điều kiện” không có nghĩa một nguyên nhân đơn độc tất định mọi việc, cũng không cho phép thu toàn bộ giáo lý thành vài mili-giây tâm lý.

    #v(6pt)
    #source-badge("KINH", refs: [K26; K27])
  ],
  label: [THUẬT NGỮ PĀLI],
)

#v(7pt)

#practice-card(
  [nīvaraṇa và bojjhaṅga · triền cái và giác chi],
  [
    *Năm triền cái* là những nhóm trạng thái cản sự sáng rõ: tham dục, sân, hôn trầm-thụy miên, trạo cử-hối và hoài nghi. *Bảy giác chi* là những phẩm chất cần nuôi và cân bằng: niệm, trạch pháp, tinh tấn, hỷ, khinh an, định và xả. Chúng không chỉ là “tâm xấu” và “tâm tốt”; MN 10 yêu cầu biết sự có mặt, vắng mặt, điều kiện sinh và cách phát triển hay đoạn trừ.

    #v(6pt)
    #source-badge("KINH", refs: [K01; K13])
  ],
  label: [CẶP THUẬT NGỮ],
)

#v(7pt)

#practice-card(
  [vāyo-dhātu · phong đại, yếu tố chuyển động],
  [
    Trong P02, đây là cách gọi truyền thống cho nét cứng đỡ, rung, đẩy, kéo và chuyển động được cảm nhận nơi bụng khi thở. Đối tượng là cảm giác chuyển động, không phải một luồng khí tưởng tượng và cũng không đồng nhất với chữ “phồng, xẹp”.

    #v(6pt)
    #source-badge("MAHĀSI", refs: [P02])
  ],
  label: [THUẬT NGỮ DÒNG THIỀN],
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
  [K02; K19],
  [
    *Cetanā* là tư hay ý định; K19 dùng từ này khi định nghĩa nghiệp. *Manasikāra* là sự hướng tâm hoặc tác ý; trong cụm *yoniso manasikāra*, nó chỉ như lý tác ý. Một số bản dịch Việt dùng “tác ý” cho cả hai, nhưng hai thuật ngữ không đồng nghĩa.
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
