#import "../components.typ": *

#let term-card(pali, vietnamese, refs, body, kind: "BIÊN SOẠN", term-label: [THUẬT NGỮ PĀLI]) = practice-card(
  [#pali · #vietnamese],
  [
    #source-badge(kind, refs: refs)
    #v(4pt)
    #body
  ],
  label: term-label,
)

#pagebreak(weak: true)
#v(7mm)
#eyebrow([PHỤ LỤC D], fill: palette.saffron)
#v(4mm)
= Thuật ngữ cốt lõi <thuat-ngu>

#text(font: fonts.sans, size: 9.5pt, fill: palette.muted)[
  Một từ Việt thường chưa giữ hết sắc thái của một từ Pāli. Các mục dưới đây là lời giải nghĩa để dùng sách, có nguồn đối chiếu; khi cần kết luận về giáo lý, hãy trở lại đúng bài và đúng ngữ cảnh.
]

#v(8mm)

== Tìm nhanh

#practice-card(
  [Bốn nhóm để tra cứu],
  [
    + #link(<thuat-ngu-dao-lo>)[*Đạo lộ và năng lực tâm:*] Tứ Thánh Đế, Bát Chánh Đạo, Năm giới, niệm, tỉnh giác, định và tuệ.
    + #link(<thuat-ngu-nhap-luu>)[*Nhập lưu, kiết sử và bốn quả:*] tịnh tín, ba kiết sử đầu, năm hạ phần, các quả và Sa-môn quả.
    + #link(<thuat-ngu-duyen-khoi>)[*Duyên khởi và kinh nghiệm:*] xúc, thọ, ái, thủ, năm uẩn và duyên khởi.
    + #link(<thuat-ngu-phuong-phap>)[*Phương pháp và các nhóm pháp:*] triền cái, giác chi, phong đại, niệm xứ, chỉ-quán, tư, tác ý và ghi nhận.

    Các định nghĩa hỗ trợ việc hiểu. Chúng không biến một tên Pāli thành phép xác nhận kinh nghiệm hoặc quả vị.
  ],
  label: [MỤC LỤC THUẬT NGỮ],
)

== Đạo lộ và năng lực tâm <thuat-ngu-dao-lo>

#term-card([cattāri ariyasaccāni], [Tứ Thánh Đế], [K05; K11], [
  Bốn sự thật: khổ, nguồn sinh khổ, sự chấm dứt khổ và con đường đưa đến chấm dứt khổ. SN 56.11 nêu bốn nhiệm vụ tương ứng: hiểu đầy đủ, đoạn trừ, thực chứng và tu tập. Đồng ý với bốn mệnh đề bằng lời chưa có nghĩa đã hoàn tất bốn nhiệm vụ.
])
#v(7pt)

#term-card([ariya aṭṭhaṅgika magga], [Bát Thánh Đạo, Bát Chánh Đạo], [K06; K23; K25], [
  Tám chi là chánh kiến, chánh tư duy, chánh ngữ, chánh nghiệp, chánh mạng, chánh tinh tấn, chánh niệm và chánh định. SN 55.5 gọi chính đạo lộ ấy là dòng. Một đề mục hay kỹ thuật có thể hỗ trợ việc tu, nhưng không thay thế cả con đường.
])
#v(7pt)

#term-card([pañca sīlāni], [Năm giới], [K09; K18], [
  Năm điều học căn bản của cư sĩ: tránh sát sinh, lấy của không cho, tà hạnh trong dục, nói dối và chất say gây buông lung. Trong công thức này, giới thứ tư là tránh nói dối; SN 55.7 nêu rộng hơn với bốn loại lời nói cần tránh. Giữ giới là điều cần được thực hành, không phải một nghi thức bảo đảm thanh tịnh tự động.
])
#v(7pt)

#term-card([sati · sammāsati], [niệm · chánh niệm], [K01; K12; K25], [
  *Sati* là niệm, có nghĩa liên quan đến ghi nhớ và không quên. Để dùng sách, có thể hiểu là nhớ điều cần được tu tập và giữ hướng nhận biết. Trong Niệm xứ, niệm đi cùng nhiệt tâm và tỉnh giác. *Sammāsati* là chánh niệm, một chi của đạo lộ; không nên gọi mọi lần chú ý hoặc nhớ một việc là đã đầy đủ chánh niệm theo kinh.
])
#v(7pt)

#term-card([sampajañña], [tỉnh giác, biết rõ], [K01], [
  Trong phần sinh hoạt thường ngày của MN 10, thuật ngữ gắn với biết rõ khi đi, về, nhìn, co, duỗi, ăn, uống và các hoạt động khác. Cách sách nói “biết việc đang làm và hoàn cảnh” là lời gợi ý để thực hành; tỉnh giác và niệm hỗ trợ nhau nhưng không chỉ là hai từ thay thế.
])
#v(7pt)

#term-card([samādhi], [định, tâm quy tụ], [K12; K23; K25], [
  Sự quy tụ, thu nhiếp của tâm. Riêng chánh định trong SN 45.8 được định nghĩa bằng bốn thiền; MN 117 trình bày chánh định có những chi đạo khác hỗ trợ. Tập trung làm việc, một phút dễ chịu hoặc ít suy nghĩ chưa tự đáp ứng định nghĩa ấy.
])
#v(7pt)

#term-card([paññā], [tuệ, trí thấy đúng], [K05; K17; K31], [
  Sự phân biệt và thấy đúng theo Pháp, nhất là về khổ, nguồn sinh, sự chấm dứt và con đường. Đây là cách giải nghĩa trong phạm vi sách; tuệ không đồng nhất với kiến thức thuộc lòng, trải nghiệm lạ hoặc khả năng kể về trạng thái thiền.
])
#v(7pt)

== Nhập lưu, kiết sử và bốn quả <thuat-ngu-nhap-luu>

#term-card([saṃyojana], [kiết sử, sự trói buộc], [K11; K24; K36], [
  Những mối trói được giáo lý phân tích, không phải tên chung cho mọi thói quen xấu. Chương 10 nói về ba kiết sử đầu; Chương 11 đặt chúng trong năm hạ phần và các quả. MN 64 giúp phân biệt khuynh hướng tiềm ẩn với sự biểu hiện; không thấy biểu hiện lúc này chưa chứng minh đã đoạn tận.
])
#v(7pt)

#practice-card(
  [Ba kiết sử đầu],
  [
    Thân kiến, hoài nghi và chấp thủ giới-tập tục là ba cái đầu trong nhóm năm hạ phần kiết sử. Thêm dục tham và sân thì đủ năm. Nhập lưu đoạn ba kiết sử đầu; Bất lai đoạn cả năm hạ phần. “Ba hạ phần” đôi khi là cách nói tắt, không phải một bảng độc lập khác.

    #v(6pt)
    #source-badge("BIÊN SOẠN", refs: [đối chiếu K10; K24])
  ],
  label: [BẢN ĐỒ THUẬT NGỮ],
)
#v(7pt)

#term-card([sakkāya-diṭṭhi], [thân kiến], [K20; K17], [
  Bốn cách nắm với mỗi uẩn: uẩn là tự ngã; tự ngã sở hữu uẩn; uẩn ở trong tự ngã; tự ngã ở trong uẩn. Năm uẩn và bốn cách thành hai mươi. Đại từ “tôi”, một nỗi lo sức khỏe hoặc chăm sóc bản thân không tự là thân kiến. Đoạn thân kiến cũng không đồng nghĩa đã đoạn ngã mạn “tôi là”.
])
#v(7pt)

#term-card([vicikicchā], [hoài nghi], [K11; K03; K08; K09], [
  MN 2 nêu thuật ngữ trong ba kiết sử đầu. Sách đọc cùng các đoạn về tịnh tín được xác chứng và thấy duyên khởi để giải thích nghi trên trục Phật, Pháp, Tăng và con đường. Đây không phải định nghĩa cho mọi ngữ cảnh của từ, và không đồng nhất với mọi câu hỏi cẩn trọng hoặc việc từ chối phục tùng mù quáng.
])
#v(7pt)

#term-card([aveccappasāda], [tịnh tín được xác chứng], [K03; K08; K09; K21], [
  Công thức kinh đặt tịnh tín nơi Phật, Pháp và cộng đồng Thánh đệ tử, bên cạnh giới hạnh được bậc Thánh quý trọng. Sách phân biệt điều ấy với một thoáng cảm hứng hoặc áp lực phải tin. Từ công thức không thể tự suy ra mọi tổ chức, người xuất gia hay người nhận mình là thầy đều đã được bảo chứng.
])
#v(7pt)

#term-card([sīlabbataparāmāsa], [giới cấm thủ, chấp thủ giới-tập tục], [K11; K08; K38], [
  Một cách giải nghĩa để đọc là nắm giới, tập tục hoặc lối thực hành như thể riêng hình thức ấy đủ đem đến thanh tịnh và giải thoát. Đây là lời giải thích có giới hạn của sách, không phải định nghĩa nguyên văn đầy đủ tại câu MN 2. Đoạn kiết sử này không có nghĩa bỏ giới; Gương Pháp vẫn nêu giới hạnh vững chắc.
])
#v(7pt)

#term-card([orambhāgiya-saṃyojana], [hạ phần kiết sử], [K10; K24], [
  Nhóm năm gồm thân kiến, hoài nghi, giới cấm thủ, dục tham và sân. Nhập lưu đoạn ba cái đầu; Nhất lai đoạn ba cái ấy và làm mỏng tham, sân, si; Bất lai đoạn cả năm. “Hạ phần” không có nghĩa đây là những lỗi nhẹ hoặc dễ bỏ.
])
#v(7pt)

#term-card([kāmacchanda · kāmarāga], [dục tham], [K24; K36; K37], [
  AN 10.13 và phần đầu MN 64 dùng kāmacchanda; MN 64 cũng dùng kāmarāga khi mô tả tâm bị chi phối. Sách giải thích các cách dùng này theo ngữ cảnh, không coi hai từ thay thế tuyệt đối ở mọi nơi. Một đối tượng giác quan hoặc thọ dễ chịu chưa tự là kiết sử; SN 41.1 đặt mối trói ở dục và tham nương sự gặp gỡ giữa căn với cảnh.
])
#v(7pt)

#term-card([byāpāda], [sân, ác ý], [K24; K36], [
  Chiều thù nghịch, ác ý trong nhóm hạ phần kiết sử. Thọ khó chịu, nhận ra nguy hiểm hoặc đặt ranh giới không gây hại chưa tự là byāpāda. Một hành vi mơ hồ cần được hiểu thêm; nhưng nếu ác ý thực sự còn có mặt thì không phù hợp với tuyên bố đã đoạn tận sân. Sự thận trọng không xóa tiêu chuẩn của giáo lý.
])
#v(7pt)

#term-card([magga · phala], [đạo · quả], [K32; K33; K39], [
  Theo nghĩa chung của Chương 11, đạo là đường tu và quả là thành tựu. SN 45.35 xác định Bát Chánh Đạo là đời sống Sa-môn rồi nêu bốn quả. Ud 5.5 và SN 48.18 phân biệt người thực hành để chứng một quả với người đã thành tựu. Phân tích đạo-quả theo chuỗi sát-na ở Chương 13 thuộc hệ thống luận giải; không tự động áp dụng nghĩa ấy cho mọi câu kinh có hai từ này.
])
#v(7pt)

#practice-card(
  [Tên quả khác tên người thành tựu],
  [
    Tên bốn quả là sotāpattiphala, sakadāgāmiphala, anāgāmiphala và arahattaphala.

    Tên người thành tựu lần lượt là sotāpanna, sakadāgāmī, anāgāmī và arahant. Phân biệt dạng từ giúp tra cứu; không tạo thêm bốn quả khác.

    #v(6pt)
    #source-badge("BIÊN SOẠN", refs: [đối chiếu K32; K33])
  ],
  label: [BẢN ĐỒ THUẬT NGỮ],
)
#v(7pt)

#term-card([sāmaññaphala], [Sa-môn quả], [K32; K34; K40], [
  Cụm từ được dùng theo ngữ cảnh. SN 45.35 nêu bốn quả giải thoát; SN 45.36 nói đích của đời sống Sa-môn là đoạn tham, sân, si. Trong DN 2, tên Kinh Sa-môn quả gắn với câu hỏi rộng về kết quả có thể thấy của đời sống xuất gia và tiến trình huấn luyện đến đoạn lậu hoặc. “Bốn quả Sa-môn” và tên bài DN 2 có liên hệ nhưng không đồng nghĩa hoàn toàn.
])
#v(7pt)

#term-card([sotāpanna], [bậc Nhập lưu, Dự lưu], [K03; K06; K08; K10], [
  Người đã vào dòng Thánh đạo, đoạn ba kiết sử đầu và có những phẩm chất được kinh nêu. Đây là thành tựu xác định trong giáo pháp, không phải tên gọi chung cho người mới tập, người sống bình tĩnh hơn hoặc người có kinh nghiệm mạnh.
])
#v(7pt)

#term-card([sakadāgāmī], [bậc Nhất lai], [K10; K32], [
  Người đã đoạn ba kiết sử đầu và làm mỏng tham, sân, si; theo khung tái sinh của kinh, trở lại thế giới này một lần nữa rồi chấm dứt khổ. Làm mỏng không đồng nghĩa đoạn dục tham và sân như ở Bất lai.
])
#v(7pt)

#term-card([anāgāmī], [bậc Bất lai, Bất hoàn], [K08; K10; K24; K32], [
  Người đã đoạn năm hạ phần kiết sử. Đoạn Ñātika trong DN 16 nói vị ấy hóa sinh, đạt giải thoát hoàn toàn tại đó và không trở lại từ cảnh giới ấy. Một thời gian tạm lắng của dục hoặc sân không đủ xác nhận thành tựu này.
])
#v(7pt)

#term-card([āsava], [lậu hoặc], [K11; K34], [
  Nhóm ô nhiễm cần được đoạn tận; MN 2 và DN 2 nêu dục, hữu và vô minh. MN 2 trình bày bảy cách đoạn: thấy, phòng hộ, thọ dụng, kham nhẫn, tránh né, trừ bỏ và tu tập. Đoạn tận lậu hoặc là tiêu chuẩn kinh dùng ở thành tựu A-la-hán, không đồng nghĩa chỉ đoạn đủ năm hạ phần kiết sử. Đây là hai hệ phân tích khác nhau.
])
#v(7pt)

#term-card([arahant], [bậc A-la-hán], [K10; K11; K32; K34], [
  Người đã đoạn tận các lậu hoặc, hoàn tất việc giải thoát trong khung giáo lý của kinh. Tên quả tương ứng là arahattaphala, quả A-la-hán, quả cuối trong bốn quả Sa-môn. Arahant chỉ người thành tựu, không phải tên Pāli của chính quả và không phải tên chung cho người hành thiền lâu năm.
])
#v(7pt)

== Duyên khởi và cấu trúc kinh nghiệm <thuat-ngu-duyen-khoi>

#term-card([phassa], [xúc, tiếp xúc], [K26; K27], [
  Sự gặp nhau của căn, cảnh tương ứng và thức. Chẳng hạn mắt, hình sắc và nhãn thức gặp nhau thì có nhãn xúc. Xúc làm duyên cho thọ; nó không chỉ là chạm da hoặc toàn bộ một cảm xúc.
])
#v(7pt)

#term-card([vedanā], [thọ], [K01; K19; K30], [
  Sắc thái dễ chịu, khó chịu hoặc không dễ chịu cũng không khó chịu. Thọ sinh do xúc, không phải toàn bộ cảm xúc. Một cơn giận có thể có thọ khó chịu, nóng nơi thân, sự nhận ra, ký ức, ý nghĩ và ý muốn đáp trả. Sāmisa và nirāmisa không đơn giản có nghĩa thọ ở thân và thọ ở tâm; xem Chương 3.
])
#v(7pt)

#term-card([taṇhā], [ái, tham ái], [K05; K26; K44], [
  SN 56.11 nêu tham ái đưa đến tái sinh, đi cùng thích thú và đắm trước, gồm dục ái, hữu ái và phi hữu ái. SN 12.2 còn phân theo sáu loại đối tượng. Ái liên hệ với thọ nhưng không đồng nhất với thọ, và không phải mọi mong muốn đều là ái.

  Muốn chữa bệnh, rời nơi bị hại hoặc kết thúc một việc khó chịu chưa đủ để gọi là phi hữu ái. Iti 49 giúp đọc ý muốn không hiện hữu trong bối cảnh rộng hơn, gồm quan điểm tự ngã bị hủy diệt sau khi chết. Chương 12 giải thích ba loại ái và phân biệt mong muốn thiện lành.
])
#v(7pt)

#term-card([upādāna], [thủ, chấp thủ], [K20; K26; K27], [
  SN 12.2 nêu bốn loại: dục thủ, kiến thủ, giới cấm thủ và ngã luận thủ. Nói gần nghĩa là sự nắm giữ dục, quan điểm, giới và lối thực hành, học thuyết về tự ngã. Sách dùng hình ảnh khát muốn và nắm chặt để phân biệt ái với thủ; không nói chúng luôn là hai khoảnh khắc dễ tách bằng đồng hồ.
])
#v(7pt)

#term-card([khandha], [uẩn, nhóm hiện tượng], [K20; K35], [
  Năm uẩn là sắc, thọ, tưởng, hành và thức. Không phải năm vật tách biệt nằm trong người. Để hiểu thân kiến, cần xem bốn quan hệ giữa mỗi uẩn với tự ngã trong MN 44, không chỉ việc một cảm giác có đổi hay không.
])
#v(7pt)

#term-card([pañcupādānakkhandhā], [năm thủ uẩn], [K53 · SN 22.48; K20 · MN 44], [
  Năm uẩn hữu lậu, có thể bị chấp thủ. “Hữu lậu” chỉ sự liên hệ với lậu hoặc, những ô nhiễm ràng buộc tâm. Thuật ngữ không chỉ những lúc ta đang nhận thấy mình bám víu. MN 44 còn phân biệt các thủ uẩn với dục và tham đối với chúng; một phút bình tĩnh không tự chứng minh chấp thủ đã đoạn tận.
])
#v(7pt)

#term-card([paṭiccasamuppāda], [duyên khởi], [K26; K27], [
  Sự sinh khởi tùy thuộc điều kiện; các bài được dẫn cũng trình bày chiều đoạn diệt. SN 12.2 nêu chuỗi từ vô minh đến già chết; SN 12.44 triển khai từ sáu cửa. Ví dụ phản ứng trong hiện tại chỉ làm rõ một phần, không thu hữu, sinh và già chết thành vài giây tâm lý.
])
#v(7pt)

== Nhóm pháp và phương pháp thực hành <thuat-ngu-phuong-phap>

#term-card([nīvaraṇa · bojjhaṅga], [triền cái · giác chi], [K01; K13; K22], [
  Năm triền cái: tham dục, sân, hôn trầm-thụy miên, trạo cử-hối và hoài nghi. Bảy giác chi: niệm, trạch pháp, tinh tấn, hỷ, khinh an, định và xả. MN 10 dạy biết có mặt, vắng mặt và những điều kiện liên hệ đến đoạn trừ hoặc phát triển. Chương 6 giúp đọc các từ khó; một ngày mệt hoặc một câu hỏi chưa tự xác định triền cái.
])
#v(7pt)

#term-card([vāyo-dhātu], [phong đại, yếu tố chuyển động], [P02], [
  P02 trình bày đề mục bụng theo những nét như sự nâng đỡ, căng và chuyển động được biết qua thân. Thuật ngữ thuộc hệ phân tích truyền thống, không phải lời khẳng định về một luồng khí vô hình. Cảm nhận đang có cần được phân biệt với chữ “phồng, xẹp” và điều mình tưởng tượng phải cảm thấy.
])
#v(7pt)

#term-card([satipaṭṭhāna], [niệm xứ], [K01], [
  Thường được diễn đạt là sự thiết lập hoặc nền tảng của chánh niệm đối với thân, thọ, tâm và pháp. MN 10 trình bày cụ thể từng lĩnh vực, cùng các điệp khúc về sinh, diệt và không chấp thủ. Niệm xứ không đồng nghĩa riêng kỹ thuật ghi nhãn.
])
#v(7pt)

#term-card([samatha · vipassanā], [chỉ · quán], [K16; V01; P02], [
  Chỉ liên quan đến tâm lắng dịu, ổn định; quán liên quan đến thấy rõ. AN 4.170 ghi lời Tôn giả Ānanda về những trình tự phát triển khác nhau. Cách nói này là lời giải nghĩa để đọc; phần hệ thống hóa trong Thanh Tịnh Đạo và Mahāsi cần được giữ đúng tầng nguồn.
])
#v(7pt)

#term-card([cetanā · manasikāra], [tư, ý định · tác ý], [K02; K19; K26], [
  Cetanā là tư hay ý định; AN 6.63 dùng từ ấy khi định nghĩa nghiệp. Manasikāra là hướng tâm, tác ý; yoniso manasikāra thường dịch là như lý tác ý. Một số bản Việt dùng “tác ý” cho cả hai, nên cần đối chiếu từ gốc và ngữ cảnh, không mặc nhiên xem chúng đồng nghĩa.
])
#v(7pt)

#term-card([noting], [ghi nhận trong tâm], [P01; Phụ lục B], [
  *Noting* là từ tiếng Anh, không phải thuật ngữ Pāli. Trong phương pháp Mahāsi được sách giới thiệu, nhãn ngắn như “phồng”, “nghe”, “nghĩ” hỗ trợ nhận biết. P01 dặn không đọc thành tiếng hay tụng lặp từ. Bảng nhãn Việt do sách biên soạn, không nằm nguyên dạng trong MN 10. Nhận ra muộn vẫn có thể trở về; không cần dựng lại trình tự chưa biết hoặc ghi nhãn trước khi xử lý nguy hiểm.
], term-label: [THUẬT NGỮ TIẾNG ANH])
#v(8pt)

#caution(
  [Khi chưa chắc tên, giữ mô tả gần điều đã biết],
  [
    Có thể ghi cảm giác, hoàn cảnh, thời lượng và tác động lên sinh hoạt bằng lời thường. Một thuật ngữ chỉ giúp khi dùng đúng nghĩa. Không cần nâng trải nghiệm thành một tên tuệ, cũng không cần tự kết án vì chưa biết gọi nó là gì.
  ],
)
