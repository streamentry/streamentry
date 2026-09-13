#import "../components.typ": *

#pagebreak(weak: true)
#v(7mm)
#eyebrow([PHỤ LỤC E], fill: palette.saffron)
#v(4mm)
= Bản đồ quyết định khi đang hành <ban-do-quyet-dinh>

#text(font: fonts.sans, size: 9.5pt, fill: palette.muted)[
  Dùng trang này để tìm lại lựa chọn: giữ đối tượng, biết điều đang nổi bật, hành động ngay hay dừng buổi tập.
]

#v(7mm)

#source-line("BIÊN SOẠN", [đối chiếu Chương 1, 5, 7 và 9], [
  Sơ đồ gom các hướng dẫn trong sách, không phải một bài kinh, trình tự tâm, cách chẩn đoán hay đường đi qua các tầng tuệ. Khi cần bảo vệ an toàn, hành động trước việc ghi nhãn.
])

#let safety-body = [
  Đột ngột yếu một bên, nói khó, có dấu hiệu cấp cứu cơ thể hoặc nguy cơ tự hại, hại người tức thời: dừng và tìm trợ giúp khẩn cấp; không chờ ghi nhãn hay thử tiếp đất. Dấu hiệu thần kinh tự hết vẫn cần đánh giá khẩn. Đau tăng, tê lan hoặc khó khăn tăng dần: dừng để chọn mức xử lý theo #link(<cap-cuu-ngay>)[Chương 9]. Ở Việt Nam: *115* cấp cứu y tế, *113* công an, *114* cứu hỏa; *112* tiếp nhận tình huống khẩn khi chưa rõ đầu mối. Nếu không có dấu hiệu cần dừng, chọn đúng bối cảnh bên dưới.
]

#let after-body = [
  Ngủ nghỉ, thân thể và sinh hoạt vẫn ổn: giữ nhịp phù hợp. Lịch chỉ quá bận: giảm yêu cầu. Có mất ngủ tăng, hoảng sợ lặp lại, đau tăng hoặc suy giảm sinh hoạt: dừng buổi hiện tại, xem #link(<an-toan>)[Chương 9] và tìm hỗ trợ phù hợp; không tự trở lại mức cũ chỉ vì từng chịu được. Không bù giờ hoặc tự chấm tầng tuệ. *Câu nhớ:* an toàn trước, đúng bối cảnh, rồi chọn bước tiếp theo.
]

#let visual-node(label, title, body, accent: palette.forest) = block(
  width: 100%,
  fill: palette.surface-light,
  inset: 8pt,
  radius: 4pt,
  stroke: 0.7pt + accent.lighten(45%),
)[
  #set par(first-line-indent: 0em, justify: false, leading: 0.62em)
  #text(font: fonts.sans, size: 6.8pt, weight: 700, tracking: 0.06em, fill: accent)[#upper(label)]
  #v(2.5pt)
  #text(font: fonts.display, size: 10.5pt, weight: 650)[#title]
  #v(3pt)
  #text(size: 8.2pt)[#body]
]

#let down-arrow = align(center)[
  #text(font: fonts.sans, size: 12pt, weight: 700, fill: palette.saffron)[↓]
]

#context {
  if target() == "html" {
    html.elem("div", attrs: (class: "decision-map"))[
      #html.elem("section", attrs: (class: "decision-node decision-wide", role: "group", aria-labelledby: "decision-safety-title"))[
        #html.elem("p", attrs: (class: "eyebrow"))[1 · CỔNG AN TOÀN]
        #html.elem("h3", attrs: (class: "card-title", id: "decision-safety-title"))[Có việc phải bảo vệ ngay không?]
        #safety-body
      ]
      #html.elem("section", attrs: (class: "decision-node", role: "group", aria-labelledby: "decision-formal-title"))[
        #html.elem("p", attrs: (class: "eyebrow"))[2A · BUỔI TẬP CÓ CẤU TRÚC]
        #html.elem("h3", attrs: (class: "card-title", id: "decision-formal-title"))[Giữ, chuyển hay hành động?]
        + Hiện tượng còn ở hậu cảnh: giữ điểm tựa.
        + Hiện tượng đã chi phối: nhận biết nó.
        + Không còn nổi bật: trở về điểm tựa.
        + Cần an toàn hoặc có bổn phận khẩn: hành động trước.
      ]
      #html.elem("section", attrs: (class: "decision-node", role: "group", aria-labelledby: "decision-daily-life-title"))[
        #html.elem("p", attrs: (class: "eyebrow"))[2B · ĐỜI SỐNG]
        #html.elem("h3", attrs: (class: "card-title", id: "decision-daily-life-title"))[Đặt chú ý ở đâu?]
        + Việc có rủi ro: chú ý trọn việc và hoàn cảnh.
        + Có điều kiện dừng: biết phản ứng, chọn hành động phù hợp rồi trở lại nhiệm vụ.
        + Đã gây hại: dừng, nhận trách nhiệm, sửa cụ thể và chuẩn bị để bớt lặp lại.
      ]
      #html.elem("section", attrs: (class: "decision-node decision-wide", role: "group", aria-labelledby: "decision-after-practice-title"))[
        #html.elem("p", attrs: (class: "eyebrow"))[3 · SAU BUỔI TẬP]
        #html.elem("h3", attrs: (class: "card-title", id: "decision-after-practice-title"))[Giữ, giảm hay dừng?]
        #after-body
      ]
    ]
  } else {
    block(width: 100%, breakable: false)[
      #visual-node([1 · CỔNG AN TOÀN], [Có việc phải bảo vệ ngay không?], safety-body, accent: palette.clay)
      #down-arrow
      #grid(
        columns: (1fr, 1fr), column-gutter: 7pt, align: top,
        [
          #visual-node([2A · BUỔI TẬP CÓ CẤU TRÚC], [Giữ, chuyển hay hành động?], [
            • Còn ở hậu cảnh: giữ điểm tựa.\
            • Đã chi phối: nhận biết nó.\
            • Hết nổi bật: trở về điểm tựa.\
            • Cần an toàn hoặc có bổn phận khẩn: hành động trước.
          ])
        ],
        [
          #visual-node([2B · ĐỜI SỐNG], [Đặt chú ý ở đâu?], [
            • Việc có rủi ro: chú ý trọn việc.\
            • Khi có thể dừng: biết phản ứng, chọn hành động rồi trở lại nhiệm vụ.\
            • Đã gây hại: dừng, nhận trách nhiệm, sửa cụ thể và phòng lặp lại.
          ], accent: palette.indigo)
        ],
      )
      #down-arrow
      #visual-node([3 · SAU BUỔI TẬP], [Giữ, giảm hay dừng?], after-body, accent: palette.saffron)
    ]
  }
}
