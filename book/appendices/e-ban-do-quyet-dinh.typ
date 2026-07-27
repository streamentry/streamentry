#import "../components.typ": *

#pagebreak(weak: true)
#v(7mm)
#eyebrow([PHỤ LỤC E], fill: palette.saffron)
#v(4mm)
= Bản đồ quyết định khi đang hành <ban-do-quyet-dinh>

#text(font: fonts.sans, size: 9.5pt, fill: palette.muted)[
  Mở trang này khi bạn không nhớ nên giữ đối tượng, chuyển sang điều đang nổi bật, hành động ngay hay dừng buổi tập.
]

#v(7mm)

#source-line("BIÊN SOẠN", [C74–C76; dựa trên C46–C52 và C71–C73], [
  Sơ đồ dưới đây gom các quyết định đã giải thích trong chương 1, 5, 7 và 9. Nó không phải một bài kinh, một trình tự tâm, một cách chẩn đoán hay một đường tắt đi qua các tầng tuệ.
])

#let visual-node(label, title, body, accent: palette.forest) = block(
  width: 100%,
  fill: palette.surface-light,
  inset: 8pt,
  radius: 4pt,
  stroke: 0.7pt + accent.lighten(45%),
)[
  #set par(first-line-indent: 0em, justify: false, leading: 0.62em)
  #text(
    font: fonts.sans,
    size: 6.8pt,
    weight: 700,
    tracking: 0.06em,
    fill: accent,
  )[#upper(label)]
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
      #html.elem(
        "section",
        attrs: (
          class: "decision-node decision-wide",
          role: "group",
          aria-labelledby: "decision-safety-title",
        ),
      )[
        #html.elem("p", attrs: (class: "eyebrow"))[1 · CỔNG AN TOÀN]
        #html.elem("h3", attrs: (class: "card-title", id: "decision-safety-title"))[Có việc phải bảo vệ ngay không?]
        Có nguy hiểm cấp thời, thôi thúc tự hại hoặc hại người, mất liên hệ với thực tại, đau sắc, tê lan hay yếu chi? Nếu *có*, bỏ kỹ thuật, làm điều an toàn cần làm và dùng #link(<an-toan>)[chương 9]. Ở Việt Nam: *112* khi chưa rõ đầu mối, *115* cấp cứu y tế, *113* công an, *114* cứu hỏa. Nếu *không*, chọn đúng bối cảnh ở hàng kế tiếp.
      ]

      #html.elem(
        "section",
        attrs: (
          class: "decision-node",
          role: "group",
          aria-labelledby: "decision-formal-title",
        ),
      )[
        #html.elem("p", attrs: (class: "eyebrow"))[2A · BUỔI TẬP CÓ CẤU TRÚC]
        #html.elem("h3", attrs: (class: "card-title", id: "decision-formal-title"))[Giữ, chuyển hay hành động?]
        + Sự việc còn ở nền: giữ điểm tựa.
        + Sự việc đã chi phối chú ý: biết nó.
        + Nó lắng hoặc hết nổi bật: trở về điểm tựa.
        + Có nguy cơ hay bổn phận cấp thời: hành động trước.
      ]

      #html.elem(
        "section",
        attrs: (
          class: "decision-node",
          role: "group",
          aria-labelledby: "decision-daily-life-title",
        ),
      )[
        #html.elem("p", attrs: (class: "eyebrow"))[2B · ĐỜI SỐNG]
        #html.elem("h3", attrs: (class: "card-title", id: "decision-daily-life-title"))[Đặt chú ý ở đâu?]
        + Việc có rủi ro hoặc cần độ chính xác: chú ý trọn việc.
        + Phản ứng vừa dâng: biết thân, thọ và lực kéo; chọn hành động nhỏ nhất đủ đúng rồi trở lại hoàn cảnh.
        + Đã gây hại: dừng, gọi đúng việc, nhận trách nhiệm, sửa và đặt một chốt cho lần sau.
      ]

      #html.elem(
        "section",
        attrs: (
          class: "decision-node decision-wide",
          role: "group",
          aria-labelledby: "decision-after-practice-title",
        ),
      )[
        #html.elem("p", attrs: (class: "eyebrow"))[3 · SAU BUỔI TẬP]
        #html.elem("h3", attrs: (class: "card-title", id: "decision-after-practice-title"))[Giữ, giảm hay dừng?]
        Giấc ngủ, thân thể và sinh hoạt vẫn ổn: giữ nhịp. Chúng xấu đi: giảm về mức gần nhất từng ổn. Dấu hiệu cảnh báo mạnh, lặp lại hoặc kéo dài: dừng tăng cường độ và tìm hỗ trợ phù hợp. Không bù giờ, không dùng một hiện tượng lạ để tự chấm tầng tuệ. *Câu nhớ:* an toàn trước, đúng bối cảnh sau, rồi mới xét tiếp tục hay giảm.
      ]
    ]
  } else {
    block(width: 100%, breakable: false)[
      #visual-node(
        [1 · CỔNG AN TOÀN],
        [Có việc phải bảo vệ ngay không?],
        [
          Có nguy hiểm cấp thời, thôi thúc tự hại hoặc hại người, mất liên hệ với thực tại, đau sắc, tê lan hay yếu chi? Nếu *có*, bỏ kỹ thuật, làm điều an toàn cần làm và dùng #link(<an-toan>)[chương 9]. Ở Việt Nam: *112* khi chưa rõ đầu mối, *115* cấp cứu y tế, *113* công an, *114* cứu hỏa. Nếu *không*, chọn đúng bối cảnh ở hàng kế tiếp.
        ],
        accent: palette.clay,
      )

      #down-arrow

      #grid(
        columns: (1fr, 1fr),
        column-gutter: 7pt,
        align: top,
        [
          #visual-node(
            [2A · BUỔI TẬP CÓ CẤU TRÚC],
            [Giữ, chuyển hay hành động?],
            [
              • Còn ở nền: giữ điểm tựa.\
              • Chi phối chú ý: biết nó.\
              • Lắng hoặc hết nổi bật: trở về.\
              • Có nguy cơ hay bổn phận: hành động trước.
            ],
          )
        ],
        [
          #visual-node(
            [2B · ĐỜI SỐNG],
            [Đặt chú ý ở đâu?],
            [
              • Việc có rủi ro: chú ý trọn việc.\
              • Phản ứng vừa dâng: biết thân, thọ, lực kéo; chọn việc nhỏ nhất đủ đúng.\
              • Đã gây hại: dừng, nhận, sửa, đặt chốt.
            ],
            accent: palette.indigo,
          )
        ],
      )

      #down-arrow

      #visual-node(
        [3 · SAU BUỔI TẬP],
        [Giữ, giảm hay dừng?],
        [
          Giấc ngủ, thân thể và sinh hoạt vẫn ổn: giữ nhịp. Chúng xấu đi: giảm về mức gần nhất từng ổn. Dấu hiệu cảnh báo mạnh, lặp lại hoặc kéo dài: dừng tăng cường độ và tìm hỗ trợ phù hợp. Không bù giờ, không dùng một hiện tượng lạ để tự chấm tầng tuệ. *Câu nhớ:* an toàn trước, đúng bối cảnh sau, rồi mới xét tiếp tục hay giảm.
        ],
        accent: palette.saffron,
      )
    ]
  }
}
