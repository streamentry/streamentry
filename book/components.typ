#import "theme.typ": palette, fonts, space

#let eyebrow(label, fill: palette.muted) = text(
  font: fonts.sans,
  size: 7pt,
  weight: 650,
  tracking: 0.15em,
  fill: fill,
)[#upper(label)]

#let divider(fill: palette.rule, height: 0.65pt) = rect(
  width: 100%,
  height: height,
  fill: fill,
)

#let cover(title, subtitle, author: none, edition: [Ấn bản thực hành 2026]) = {
  set page(
    margin: 0mm,
    header: none,
    footer: none,
    numbering: none,
    fill: palette.paper,
  )

  block(
    width: 100%,
    height: 100%,
    inset: (x: 21mm, y: 24mm),
  )[
    #set par(justify: false, first-line-indent: 0em)
    #rect(width: 34mm, height: 3pt, fill: palette.saffron)
    #v(24mm)
    #eyebrow([SỔ TAY NIỆM XỨ CHO NGƯỜI TẠI GIA], fill: palette.forest)
    #v(8mm)
    #set par(leading: 0.95em)
    #text(
      font: fonts.display,
      size: 34pt,
      weight: 600,
      fill: palette.ink,
    )[#title]
    #v(7mm)
    #divider()
    #v(6mm)
    #set par(leading: 1.35em)
    #text(
      font: fonts.sans,
      size: 10.5pt,
      fill: palette.muted,
    )[#subtitle]
    #if author != none [
      #v(8mm)
      #eyebrow([TÁC GIẢ], fill: palette.saffron)
      #v(2.5mm)
      #text(
        font: fonts.sans,
        size: 9.5pt,
        weight: 600,
        fill: palette.forest,
      )[#author]
    ]
    #v(1fr)
    #grid(
      columns: (1fr, auto),
      column-gutter: 10pt,
      align: (left, bottom),
      [
        #set par(leading: 1.35em)
        #text(
          font: fonts.sans,
          size: 7.4pt,
          fill: palette.muted,
        )[
          Kinh tạng Pāli · Thanh Tịnh Đạo\
          Chỉ dẫn thực hành Mahāsi
        ]
      ],
      [#eyebrow(edition)],
    )
  ]

  pagebreak()
  counter(page).update(1)
}

#let chapter(number, title, deck, provenance: none) = {
  pagebreak(weak: true)
  v(7mm)
  eyebrow([CHƯƠNG #number], fill: palette.saffron)
  v(4mm)
  heading(level: 1, outlined: true)[#title]
  v(4mm)
  block(width: 78%)[
    #set par(first-line-indent: 0em, justify: false, leading: 0.72em)
    #text(font: fonts.sans, size: 10pt, fill: palette.muted)[#deck]
  ]
  if provenance != none {
    v(space.md)
    provenance
  }
  v(space.xl)
}

#let source-color(kind) = {
  if kind == "KINH" { palette.forest }
  else if kind == "THANH TỊNH ĐẠO" { palette.saffron }
  else if kind == "LUẬN GIẢI" { palette.indigo }
  else if kind == "MAHĀSI" { palette.clay }
  else if kind == "NGHIÊN CỨU" { palette.research }
  else { palette.muted }
}

#let source-badge(kind, refs: none) = {
  let color = source-color(kind)
  box(
    fill: color.lighten(83%),
    stroke: 0.55pt + color.lighten(40%),
    radius: 3pt,
    inset: (x: 6pt, y: 3pt),
  )[
    #text(
      font: fonts.sans,
      size: 6.5pt,
      weight: 700,
      tracking: 0.08em,
      fill: color,
    )[#kind]
    #if refs != none [
      #h(4pt)
      #text(font: fonts.sans, size: 6.5pt, fill: color)[#refs]
    ]
  ]
}

#let source-line(kind, refs, body) = block(
  width: 100%,
  breakable: false,
  inset: (left: 9pt),
  stroke: (left: 1.5pt + source-color(kind)),
)[
  #set par(first-line-indent: 0em)
  #source-badge(kind, refs: refs)
  #h(5pt)
  #body
]

#let scripture-quote(body, source) = block(
  width: 100%,
  breakable: false,
  fill: palette.surface,
  inset: 14pt,
  radius: 5pt,
  stroke: 0.6pt + palette.rule,
)[
  #set par(first-line-indent: 0em, justify: false, leading: 0.72em)
  #text(font: fonts.display, size: 13.5pt, style: "italic")[#body]
  #v(8pt)
  #divider()
  #v(6pt)
  #text(font: fonts.sans, size: 7.5pt, fill: palette.muted)[#source]
]

#let practice-card(title, body, label: [THỰC HÀNH]) = block(
  width: 100%,
  breakable: false,
  fill: palette.surface-light,
  inset: 12pt,
  radius: 5pt,
  stroke: 0.7pt + palette.rule,
)[
  #set par(first-line-indent: 0em)
  #eyebrow(label, fill: palette.forest)
  #v(4pt)
  #text(font: fonts.display, size: 13pt, weight: 600)[#title]
  #v(7pt)
  #body
]

#let caution(title, body) = block(
  width: 100%,
  breakable: false,
  fill: palette.clay.lighten(88%),
  inset: 12pt,
  radius: 5pt,
  stroke: 0.7pt + palette.clay.lighten(48%),
)[
  #set par(first-line-indent: 0em)
  #eyebrow([GIỚI HẠN CẦN NHỚ], fill: palette.clay)
  #v(4pt)
  #text(font: fonts.display, size: 13pt, weight: 600)[#title]
  #v(7pt)
  #body
]

#let modern-note(body) = block(
  width: 100%,
  breakable: false,
  inset: (left: 10pt),
  stroke: (left: 1.5pt + palette.muted),
)[
  #set par(first-line-indent: 0em)
  #source-badge("BIÊN SOẠN")
  #h(5pt)
  #body
]

#let day-card(day, title, duration, body) = block(
  width: 100%,
  breakable: false,
  inset: (y: 10pt),
)[
  #grid(
    columns: (24pt, 1fr),
    column-gutter: 10pt,
    [
      #circle(
        radius: 12pt,
        fill: palette.saffron,
      )[
        #align(center + horizon)[
          #text(font: fonts.sans, size: 8pt, weight: 700, fill: white)[#day]
        ]
      ]
    ],
    [
      #set par(first-line-indent: 0em)
      #text(font: fonts.display, size: 12.5pt, weight: 600)[#title]
      #h(5pt)
      #text(font: fonts.sans, size: 7pt, fill: palette.saffron)[#duration]
      #v(4pt)
      #body
    ],
  )
]

#let check-row(label, body) = grid(
  columns: (15pt, 1fr),
  column-gutter: 6pt,
  align: top,
  [#box(width: 8pt, height: 8pt, stroke: 0.7pt + palette.forest, radius: 1pt)],
  [
    #set par(first-line-indent: 0em)
    *#label* #body
  ],
)

#let reference-item(code, title, detail, url) = block(
  width: 100%,
  breakable: false,
  inset: (y: 5pt),
)[
  #set par(first-line-indent: 0em)
  #grid(
    columns: (32pt, 1fr),
    column-gutter: 8pt,
    [#source-badge("KINH", refs: code)],
    [
      *#title*\
      #text(size: 8.5pt, fill: palette.muted)[#detail]\
      #link(url)[#text(font: fonts.sans, size: 7pt)[Mở bản nguồn trực tuyến]]
    ],
  )
]
