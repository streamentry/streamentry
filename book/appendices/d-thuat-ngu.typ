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
= Thuật ngữ cốt lõi <thuat-ngu>

#text(font: fonts.sans, size: 9.5pt, fill: palette.muted)[
  Dịch một từ Pāli bằng một từ Việt có thể tiện, nhưng không bao giờ giữ trọn mọi sắc thái. Các định nghĩa dưới đây chỉ đủ dùng cho cuốn sổ tay này.
]

#v(8mm)

== Tìm nhanh

#practice-card(
  [Bốn nhóm để tra cứu],
  [
    + #link(<thuat-ngu-dao-lo>)[*Đạo lộ và năng lực tâm:*] Tứ Thánh Đế, Bát Chánh Đạo, Năm giới, chánh niệm, tỉnh giác, định và tuệ.
    + #link(<thuat-ngu-nhap-luu>)[*Nhập lưu, kiết sử và bốn quả:*] tịnh tín đã được xác chứng, ba kiết sử đầu, năm hạ phần kiết sử, Nhập lưu, Nhất lai, Bất lai, A-la-hán và nghĩa của Sa-môn quả.
    + #link(<thuat-ngu-duyen-khoi>)[*Duyên khởi và cấu trúc kinh nghiệm:*] xúc, thọ, ái, thủ, năm uẩn và duyên khởi.
    + #link(<thuat-ngu-phuong-phap>)[*Nhóm pháp và phương pháp thực hành:*] triền cái, giác chi, phong đại, niệm xứ, chỉ-quán, tư-tác ý và ghi nhận.

    Nếu một từ được dùng để tự xác nhận chứng đắc, hãy đọc lại cả định nghĩa, nguồn và câu giới hạn. Đừng chỉ lấy nhãn Pāli.
  ],
  label: [MỤC LỤC THUẬT NGỮ],
)

== Đạo lộ và năng lực tâm <thuat-ngu-dao-lo>

#term-card(
  [cattāri ariyasaccāni],
  [Tứ Thánh Đế, bốn sự thật của bậc Thánh],
  [K05; K11],
  [
    Bốn sự thật là khổ, nguồn gốc của khổ, sự chấm dứt khổ và con đường đưa đến chấm dứt khổ. K05 gắn bốn nhiệm vụ tương ứng: khổ cần được hiểu, nguồn gốc cần được đoạn, sự chấm dứt cần được chứng và con đường cần được tu. Đây không chỉ là bốn mệnh đề để đồng ý bằng trí nhớ.
  ],
)

#v(7pt)

#term-card(
  [ariya aṭṭhaṅgika magga],
  [Bát Thánh Đạo, Thánh đạo tám ngành],
  [K06; K25],
  [
    Con đường gồm chánh kiến, chánh tư duy, chánh ngữ, chánh nghiệp, chánh mạng, chánh tinh tấn, chánh niệm và chánh định. K06 gọi chính con đường này là “dòng” trong Nhập lưu. Một kỹ thuật ghi nhận hay một đề mục thiền chỉ có thể hỗ trợ vài chi, không tự thay thế toàn bộ đạo lộ.
  ],
)

#v(7pt)

#term-card(
  [pañca sīlāni],
  [Năm giới],
  [K09; K18],
  [
    Năm điều học căn bản của cư sĩ là tránh sát sinh, lấy của không cho, tà hạnh, nói dối và chất say gây buông lung. Chúng là nền bảo vệ hành vi và quan hệ, không phải nghi thức đủ để tự động thanh tịnh. K18 giúp phân biệt giới tránh nói dối với phạm vi chánh ngữ rộng hơn.
  ],
)

#v(7pt)

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

== Nhập lưu, kiết sử và bốn quả <thuat-ngu-nhap-luu>

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
  [sakkāya-diṭṭhi],
  [thân kiến],
  [K20; K17],
  [
    Cách nắm một trong năm uẩn là tự ngã, xem tự ngã sở hữu uẩn, xem uẩn nằm trong tự ngã hoặc xem tự ngã nằm trong uẩn. Đoạn thân kiến không đòi xóa mọi cách nói “tôi” trong đời thường và không đồng nghĩa đã tận diệt ngã mạn “tôi là”.
  ],
)

#v(7pt)

#term-card(
  [vicikicchā],
  [hoài nghi],
  [K11; K03; K09],
  [
    Kiết sử được MN 2 đặt cạnh thân kiến và chấp thủ giới-tập tục. Mặt đối ứng trong các kinh về Nhập lưu là tịnh tín đã được xác chứng và trí thấy duyên khởi. Nó không đồng nghĩa với mọi câu hỏi cẩn trọng, việc kiểm chứng nguồn hoặc sự từ chối phục tùng mù quáng.
  ],
)

#v(7pt)

#practice-card(
  [aveccappasāda · tịnh tín đã được xác chứng],
  [
    Công thức kinh điển đặt tịnh tín nơi các phẩm chất của Phật, Pháp và cộng đồng Thánh đệ tử, bên cạnh giới hạnh không rạn vỡ. Trong khung của sách, đây là lòng tin đứng trên thấy biết và biểu hiện trong cách sống, không phải sự sùng kính thoáng qua hay nghĩa vụ phục tùng.

    #v(6pt)
    #source-badge("KINH", refs: [K03; K08; K09; K21])

    #v(6pt)

    “Tăng” trong công thức ấy chỉ cộng đồng Thánh đệ tử được kinh mô tả. Từ đó không thể tự động suy ra rằng mọi tổ chức, người xuất gia hay lời tuyên bố tâm linh đều đã được bảo chứng. Đây là giới hạn suy luận do sách biên soạn.

    #v(6pt)
    #source-badge("BIÊN SOẠN", refs: [giới hạn suy luận])
  ],
  label: [THUẬT NGỮ PĀLI],
)

#v(7pt)

#term-card(
  [sīlabbata-parāmāsa],
  [chấp thủ giới-tập tục],
  [K11; K08],
  [
    Cách nắm giới, tập tục hoặc phương thức thực hành như thể hình thức tự nó đủ thanh tịnh và giải thoát. MN 2 chỉ nêu tên kiết sử ở đoạn này, nên lời giải thích ngắn không phải định nghĩa đầy đủ. Đoạn kiết sử không có nghĩa bỏ giới; Gương Pháp vẫn nêu giới hạnh không rạn vỡ.
  ],
)

#v(7pt)

#term-card(
  [saṃyojana],
  [kiết sử, trói buộc],
  [K11; K24],
  [
    Mối trói buộc bền chặt giữ hữu tình trong khổ, không phải tên chung cho mọi thói quen xấu. Chương 10 tập trung vào ba kiết sử đầu gắn với Nhập lưu; K24 đặt chúng trong danh mục mười kiết sử rộng hơn.
  ],
)

#v(7pt)

#term-card(
  [orambhāgiya-saṃyojana],
  [năm hạ phần kiết sử],
  [K10; K24],
  [
    Năm trói buộc gồm ba kiết sử đầu cộng với dục tham và sân. Nhập lưu đoạn ba cái đầu; Nhất lai làm mỏng tham, sân, si; Bất lai đoạn trọn năm. “Hạ phần” không có nghĩa đây là năm lỗi nhẹ hoặc dễ bỏ.
  ],
)

#v(7pt)

#term-card(
  [sakadāgāmī],
  [Nhất lai],
  [K10; K32],
  [
    Bậc đã đoạn ba kiết sử đầu và làm mỏng tham, sân, si; theo khung tái sinh của kinh, còn trở lại thế giới này tối đa một lần trước khi chấm dứt khổ. “Làm mỏng” không có nghĩa dục tham và sân đã được đoạn như ở Bất lai.
  ],
)

#v(7pt)

#term-card(
  [anāgāmī],
  [Bất lai, Bất hoàn],
  [K10; K24; K32],
  [
    Bậc đã đoạn năm hạ phần kiết sử nên không trở lại cõi dục theo vũ trụ quan kinh điển. Sự tạm lắng của dục hay sân trong định không đủ để xác nhận quả này.
  ],
)

#v(7pt)

#term-card(
  [arahant],
  [A-la-hán],
  [K10; K32],
  [
    Bậc đã đoạn tận các lậu hoặc và hoàn tất công việc giải thoát trong khung giáo lý của kinh. Đây là quả cuối trong bốn quả Sa-môn, không phải nhãn chung cho người ngồi thiền lâu năm.
  ],
)

#v(7pt)

#term-card(
  [sāmaññaphala],
  [quả của đời sống Sa-môn],
  [K32; K34],
  [
    SN 45.35 dùng số nhiều cho bốn quả: Nhập lưu, Nhất lai, Bất lai và A-la-hán. DN 2, thường gọi là Kinh Sa-môn quả, hỏi rộng hơn về những kết quả thấy được của đời sống xuất gia và trình bày cả một tiến trình huấn luyện. Hai cách dùng liên hệ nhưng không hoàn toàn thay thế nhau.
  ],
)

#v(7pt)

== Duyên khởi và cấu trúc kinh nghiệm <thuat-ngu-duyen-khoi>

#term-card(
  [phassa],
  [xúc, sự tiếp xúc],
  [K26; K27],
  [
    Sự gặp nhau của một căn, đối tượng tương ứng và thức biết đối tượng ấy. Chẳng hạn, mắt, hình ảnh và nhãn thức gặp nhau thì có nhãn xúc. Xúc là điều kiện cho thọ; nó không chỉ có nghĩa chạm da và cũng chưa phải toàn bộ cảm xúc.
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
  [taṇhā],
  [ái, khát ái],
  [K20; K26; K27; K31],
  [
    Sự khát muốn hướng tới khoái lạc giác quan, tiếp tục hiện hữu hoặc không hiện hữu; K26 cũng phân loại ái theo sáu loại đối tượng giác quan. Trong chuỗi thực hành, ái là lực nghiêng tới kéo dài điều dễ chịu, xua điều khó chịu hoặc giữ một kết quả. Nó sinh tùy duyên từ thọ nhưng không đồng nhất với thọ.
  ],
)

#v(7pt)

#term-card(
  [upādāna],
  [thủ, chấp thủ],
  [K26; K27; K29],
  [
    Sự nắm giữ được K26 chia thành bốn loại: chấp dục, chấp kiến, chấp giới-tập tục và chấp học thuyết về tự ngã. Nếu ái là lực khát muốn, thủ là lúc tâm bấu chặt và tổ chức kinh nghiệm quanh điều ấy. Đây là cách phân biệt làm việc để đọc chuỗi, không phải hai hiện tượng luôn tách thành hai khoảnh khắc dễ nhận ra.
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

== Nhóm pháp và phương pháp thực hành <thuat-ngu-phuong-phap>

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
