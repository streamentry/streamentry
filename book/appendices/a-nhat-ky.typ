#import "../components.typ": *

#let writing-lines(count: 2) = {
  for i in range(count) {
    v(7pt)
    divider(fill: palette.rule, height: 0.45pt)
  }
}

#pagebreak(weak: true)
#v(7mm)
#eyebrow([PHỤ LỤC A], fill: palette.saffron)
#v(4mm)
= Nhật ký thực hành

#text(font: fonts.sans, size: 9.5pt, fill: palette.muted)[
  Ghi điều đã làm và điều đã thấy. Đừng dùng nhật ký để phong cho mình một tầng tuệ.
]

#v(8mm)

#practice-card(
  [Một trang cho mỗi ngày],
  [
    *Ngày:* ...........................................  *Giờ:* ........................

    #v(6pt)
    *Thiền hành:* ........ phút  |  *Thiền tọa:* ........ phút

    #v(7pt)
    #check-row([Năm giới.], [Hôm nay tôi nhớ và giữ giới bằng hành động cụ thể.])
    #v(5pt)
    #check-row([Đề mục chính.], [Bụng, hơi thở ở mũi, bước chân hoặc đề mục do thầy chỉ.])
    #v(5pt)
    #check-row([Biết lúc tâm đi xa.], [Tôi nhận ra phóng tâm và trở về mà không tự trách.])
    #v(5pt)
    #check-row([Đem niệm ra khỏi chỗ ngồi.], [Tôi đã biết rõ ít nhất một việc thường ngày.])
  ],
)

#v(8pt)

*Trở ngại nổi bật nhất là gì? Tôi đã đáp lại thế nào?*
#writing-lines(count: 3)

#v(7pt)

*Một điều tôi trực tiếp nhận ra về thân, thọ, tâm hoặc pháp:*
#writing-lines(count: 3)

#v(7pt)

*Một phản ứng trong đời sống mà tôi đã kịp thấy trước khi nói hoặc làm:*
#writing-lines(count: 2)

#pagebreak()

== Nhìn lại sau bảy ngày

#check-row([Mạch thực hành.], [Tôi đã hành ........ trong 7 ngày. Không cộng thời gian để che một ngày đã bỏ.])
#v(6pt)
#check-row([Tính khả thi.], [Giờ và chỗ hiện tại có phù hợp với công việc, giấc ngủ và gia đình không?])
#v(6pt)
#check-row([Chất lượng chú ý.], [Tôi có nhận ra phóng tâm sớm hơn, dù chỉ đôi lần không?])
#v(6pt)
#check-row([Đời sống đạo đức.], [Có giới nào đang sứt mẻ và cần một hành động sửa chữa rõ ràng không?])
#v(6pt)
#check-row([Quan hệ.], [Tôi có bớt phản ứng máy móc với người gần mình không?])

#v(8pt)

#practice-card(
  [Một điều giữ lại, một điều điều chỉnh],
  [
    *Giữ lại:*
    #writing-lines(count: 2)
    #v(5pt)
    *Điều chỉnh trong tuần tới:*
    #writing-lines(count: 2)
  ],
  label: [RÀ SOÁT TUẦN],
)

== Nhìn lại cuối tháng

#practice-card(
  [Bốn câu hỏi có ích],
  [
    + Tôi có giữ được thời khóa thực tế, không lấy mất giấc ngủ hay bổn phận gia đình không?
    + Triền cái nào lặp lại nhiều nhất? Điều kiện nào thường đi trước nó?
    + Giới, lời nói và cách cư xử có thay đổi theo hướng ít gây hại hơn không?
    + Tôi cần tiếp tục, giảm cường độ, đổi tư thế hay xin hướng dẫn ở điểm nào?
  ],
  label: [RÀ SOÁT THÁNG],
)

#v(8pt)

#caution(
  [Không ghi “tôi đã đắc”],
  [
    Nhật ký dễ biến kinh nghiệm thoáng qua thành một câu chuyện chắc chắn. Hãy mô tả dữ kiện: cảm giác gì, kéo dài bao lâu, ảnh hưởng ra sao, giới và hành vi có đổi không. Các phẩm chất của bậc Nhập lưu trong K03 không phải bảng điểm để tự chứng nhận sau một buổi thiền.
  ],
)

#v(8pt)

#source-line("BIÊN SOẠN", [mẫu theo dõi], [Nhật ký này đo tính đều đặn, điều kiện thực hành và tác động lên đời sống. Nó không phải một phương tiện chẩn đoán đạo quả.])
