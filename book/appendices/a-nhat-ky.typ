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
  Ghi điều đã làm, điều đã nhận ra và việc cần điều chỉnh. Nhật ký giúp nhớ kinh nghiệm, không dùng để xác nhận tầng tuệ hoặc chấm giá trị của mình.
]

#source-line("BIÊN SOẠN", [nhắc nghĩa từ Chương 2], [
  *Năm giới* trong mẫu này là tránh sát sinh, lấy của không cho, tà hạnh trong dục, nói dối và chất say gây buông lung. Câu hỏi về giới hướng đến hành động cụ thể, không đòi một cảm giác “trong sạch”.
])

#v(8mm)

#practice-card(
  [Một trang cho mỗi ngày],
  [
    #context {
      if target() == "html" {
        html.elem("div", attrs: (class: "worksheet-fields"))[
          #html.elem("div", attrs: (class: "worksheet-field"))[*Ngày:*]
          #html.elem("div", attrs: (class: "worksheet-field"))[*Giờ:*]
          #html.elem("div", attrs: (class: "worksheet-field"))[*Thiền hành, phút:*]
          #html.elem("div", attrs: (class: "worksheet-field"))[*Thiền tọa, phút:*]
        ]
      } else [
        *Ngày:* ...........................................  *Giờ:* ........................

        #v(6pt)
        *Thiền hành:* ........ phút  |  *Thiền tọa:* ........ phút
      ]
    }

    #v(7pt)
    #check-row([Năm giới.], [Hôm nay giới đã đi vào việc nào? Có điều gì cần sửa?])
    #v(5pt)
    #check-row([Đề mục chính.], [Bụng, tư thế ngồi và xúc chạm, bước chân hoặc đề mục được hướng dẫn phù hợp.])
    #v(5pt)
    #check-row([Nhận ra phóng tâm.], [Khi đã nhận ra, tôi trở về như thế nào?])
    #v(5pt)
    #check-row([Giấc ngủ và sinh hoạt.], [Có thay đổi đáng chú ý hay dấu hiệu cần dùng Chương 9 không?])
  ],
)

#v(8pt)

*Trở ngại nổi bật là gì? Tôi đã đáp lại thế nào?*
#writing-lines(count: 3)

#v(7pt)

*Một điều tôi trực tiếp nhận ra; điều nào mới là suy đoán?*
#writing-lines(count: 3)

#v(7pt)

*Một phản ứng tôi nhận ra trước, trong hoặc sau khi nói hay làm; điều có thể sửa:*
#writing-lines(count: 2)

#pagebreak()

== Nhìn lại sau bảy ngày <ra-soat-tuan>

#check-row([Nhịp thực hành.], [Tôi đã thực hành ........ ngày trong 7 ngày. Buổi bỏ lỡ không cần bù.])
#v(6pt)
#check-row([Tính khả thi.], [Giờ và chỗ hiện tại có phù hợp với công việc, ngủ nghỉ và gia đình không?])
#v(6pt)
#check-row([Chú ý.], [Có điều gì tôi nhận ra rõ hơn? Khi nhận ra muộn, tôi đã trở về hoặc sửa ra sao?])
#v(6pt)
#check-row([Giới và trách nhiệm.], [Có hành vi nào cần được dừng hoặc sửa bằng một việc cụ thể không?])
#v(6pt)
#check-row([Quan hệ.], [Tôi có lắng nghe người gần mình và giữ những bổn phận cần thiết không?])

#v(8pt)

#practice-card(
  [Một điều giữ lại, một điều cần điều chỉnh],
  [
    *Giữ lại:*
    #writing-lines(count: 2)
    #v(5pt)
    *Điều chỉnh trong tuần tới:*
    #writing-lines(count: 2)
  ],
  label: [RÀ SOÁT TUẦN],
)

Nếu nhịp đã ngắt, dùng #link(<khoi-dong-lai>)[lối khởi động lại ở Chương 1]. Đã dừng vì dấu hiệu nguy cơ thì đọc #link(<an-toan>)[Chương 9] và tìm hỗ trợ phù hợp trước khi tiếp tục; không dùng nhật ký để tự cho phép tăng cường độ.

== Nhìn lại cuối tháng <ra-soat-thang>

#practice-card(
  [Bốn câu hỏi có ích],
  [
    + Thời khóa có phù hợp với giấc ngủ, sức khỏe và bổn phận không?
    + Trở ngại nào thường lặp lại, điều kiện nào đi trước? Chưa xác định được triền cái thì giữ mô tả bằng lời thường.
    + Giới, lời nói và cách cư xử có chuyển theo hướng ít gây hại hơn không?
    + Tôi cần giữ, giảm, dừng hoặc xin hướng dẫn ở điểm nào?
  ],
  label: [RÀ SOÁT THÁNG],
)

#v(8pt)

#caution(
  [Giữ trải nghiệm riêng với kết luận về đạo quả],
  [
    Có thể ghi cảm giác, hoàn cảnh, thời lượng và tác động lên sinh hoạt. Nếu có một cách giải thích, hãy ghi riêng đó là điều đang suy ra, không phải điều đã trực tiếp biết. Các phẩm chất Nhập lưu trong K03 không phải bảng điểm để tự chứng nhận sau một buổi thiền. Ghi chép cũng không thay thế đánh giá sức khỏe khi có dấu hiệu cần trợ giúp.
  ],
)

#v(8pt)

#source-line("BIÊN SOẠN", [mẫu theo dõi], [Nhật ký hỗ trợ nhìn lại điều kiện và hành vi. Nó không chẩn đoán đạo quả hoặc bệnh lý; một ngày chưa thuận không làm mất khả năng trở lại và sửa điều cần sửa.])
