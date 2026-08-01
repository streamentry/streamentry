#import "edition.typ": edition, stack-lines
#import "theme.typ": palette, fonts, space

#let semantic-region-counter = counter("semantic-region")

#let eyebrow(label, fill: palette.muted) = text(
  font: fonts.sans,
  size: 7.4pt,
  weight: 650,
  tracking: 0.15em,
  fill: fill,
)[#upper(label)]

#let divider(fill: palette.rule, height: 0.65pt) = rect(
  width: 100%,
  height: height,
  fill: fill,
)

#let cover(title, subtitle, author: none) = context {
  if target() == "html" {
    html.elem("section", attrs: (class: "cover"))[
      #html.elem("p", attrs: (class: "cover-kicker"))[#edition.cover.kicker]
      #html.elem("h1")[#title]
      #html.elem("p", attrs: (class: "cover-subtitle"))[#subtitle]
      #if author != none {
        html.elem("p", attrs: (class: "cover-author"))[#(edition.labels.author): #author]
      }
      #html.elem("p", attrs: (class: "cover-edition"))[#edition.cover.edition_label]
    ]
  } else {
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
    #eyebrow(edition.cover.kicker, fill: palette.forest)
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
      #eyebrow(edition.labels.author, fill: palette.saffron)
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
        )[#stack-lines(edition.cover.provenance_lines)]
      ],
      [#eyebrow(edition.cover.edition_label)],
    )
  ]

  pagebreak()
    counter(page).update(1)
  }
}

#let chapter(number, title, deck, provenance: none) = context {
  if target() == "html" {
    html.elem("header", attrs: (class: "chapter-opener"))[
      #html.elem("p", attrs: (class: "chapter-number"))[#(edition.labels.chapter) #number]
      #heading(level: 1, outlined: true)[#title]
      #html.elem("p", attrs: (class: "chapter-deck"))[#deck]
      #if provenance != none {
        html.elem("div", attrs: (class: "provenance"), provenance)
      }
    ]
  } else {
    pagebreak(weak: true)
    v(7mm)
    eyebrow([#(edition.labels.chapter) #number], fill: palette.saffron)
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
}

#let source-color(kind) = {
  if kind == "KINH" { palette.forest }
  else if kind == "THANH TỊNH ĐẠO" { palette.saffron }
  else if kind == "LUẬN GIẢI" { palette.indigo }
  else if kind == "MAHĀSI" { palette.clay }
  else if kind == "Y TẾ & NGHIÊN CỨU" { palette.research }
  else { palette.muted }
}

#let source-badge(kind, refs: none) = context {
  if target() == "html" {
    let kind-class = if kind == "KINH" { "source-kinh" }
      else if kind == "THANH TỊNH ĐẠO" { "source-thanh-tinh-dao" }
      else if kind == "LUẬN GIẢI" { "source-luan-giai" }
      else if kind == "MAHĀSI" { "source-mahasi" }
      else if kind == "Y TẾ & NGHIÊN CỨU" { "source-nghien-cuu" }
      else { "source-bien-soan" }
    html.elem("span", attrs: (class: "source-badge " + kind-class))[
      #kind
      #if refs != none [ · #refs]
    ]
  } else {
    let color = source-color(kind)
    box(
      fill: color.lighten(83%),
      stroke: 0.55pt + color.lighten(40%),
      radius: 3pt,
      inset: (x: 6pt, y: 3pt),
    )[
      #text(
        font: fonts.sans,
        size: 7pt,
        weight: 700,
        tracking: 0.08em,
        fill: color,
      )[#kind]
      #if refs != none [
        #h(4pt)
        #text(font: fonts.sans, size: 7pt, fill: color)[#refs]
      ]
    ]
  }
}

#let source-line(kind, refs, body) = context {
  if target() == "html" {
    html.elem("aside", attrs: (class: "source-line", role: "note"))[
      #source-badge(kind, refs: refs)
      #body
    ]
  } else {
    block(
      width: 100%,
      breakable: false,
      below: 5pt,
      inset: (left: 9pt),
      stroke: (left: 1.5pt + source-color(kind)),
    )[
      #set par(first-line-indent: 0em)
      #source-badge(kind, refs: refs)
      #v(4pt)
      #body
    ]
  }
}

#let scripture-quote(body, source) = context {
  if target() == "html" {
    html.elem("blockquote", attrs: (class: "scripture-quote"))[
      #body
      #html.elem("footer", attrs: (class: "quote-source"))[#source]
    ]
  } else {
    block(
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
  }
}

#let practice-card(title, body, label: edition.labels.practice) = context {
  if target() == "html" {
    semantic-region-counter.step()
    let title-id = "practice-card-title-" + str(semantic-region-counter.get().first())
    html.elem(
      "aside",
      attrs: (
        class: "practice-card",
        role: "note",
        aria-labelledby: title-id,
      ),
    )[
      #html.elem("p", attrs: (class: "eyebrow"))[#label]
      #html.elem("div", attrs: (class: "card-title", id: title-id))[#title]
      #body
    ]
  } else {
    block(
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
  }
}

#let faq-card(anchor, question, body) = context {
  if target() == "html" {
    html.elem("section", attrs: (class: "faq-card practice-card"))[
      #html.elem("p", attrs: (class: "eyebrow"))[#edition.labels.faq]
      #html.elem("h2", attrs: (class: "card-title"))[#question]
      #label(anchor)
      #body
    ]
  } else {
    block(
      width: 100%,
      breakable: false,
      fill: palette.surface-light,
      inset: 12pt,
      radius: 5pt,
      stroke: 0.7pt + palette.rule,
    )[
      #set par(first-line-indent: 0em)
      #eyebrow(edition.labels.faq, fill: palette.forest)
      #v(4pt)
      #text(font: fonts.display, size: 13pt, weight: 600)[#question]
      #label(anchor)
      #v(7pt)
      #body
    ]
  }
}

#let caution(title, body) = context {
  if target() == "html" {
    semantic-region-counter.step()
    let title-id = "caution-title-" + str(semantic-region-counter.get().first())
    html.elem(
      "aside",
      attrs: (
        class: "caution",
        role: "note",
        aria-labelledby: title-id,
      ),
    )[
      #html.elem("p", attrs: (class: "eyebrow"))[#edition.labels.caution]
      #html.elem("p", attrs: (class: "card-title", id: title-id))[#title]
      #body
    ]
  } else {
    block(
      width: 100%,
      breakable: false,
      fill: palette.clay.lighten(88%),
      inset: 12pt,
      radius: 5pt,
      stroke: 0.7pt + palette.clay.lighten(48%),
    )[
      #set par(first-line-indent: 0em)
      #eyebrow(edition.labels.caution, fill: palette.clay)
      #v(4pt)
      #text(font: fonts.display, size: 13pt, weight: 600)[#title]
      #v(7pt)
      #body
    ]
  }
}

#let concept-node(label, title, body, accent: palette.forest) = context {
  if target() == "html" {
    semantic-region-counter.step()
    let title-id = "concept-node-title-" + str(semantic-region-counter.get().first())
    html.elem(
      "section",
      attrs: (
        class: "concept-node",
        role: "group",
        aria-labelledby: title-id,
      ),
    )[
      #html.elem("p", attrs: (class: "eyebrow"))[#label]
      #html.elem("h3", attrs: (class: "card-title", id: title-id))[#title]
      #body
    ]
  } else {
    block(
      width: 100%,
      breakable: false,
      fill: palette.surface-light,
      inset: 9pt,
      radius: 4pt,
      stroke: (
        top: 2pt + accent,
        right: 0.65pt + palette.rule,
        bottom: 0.65pt + palette.rule,
        left: 0.65pt + palette.rule,
      ),
    )[
      #set par(first-line-indent: 0em, justify: false, leading: 0.62em)
      #text(
        font: fonts.sans,
        size: 6.8pt,
        weight: 700,
        tracking: 0.07em,
        fill: accent,
      )[#upper(label)]
      #v(3pt)
      #text(font: fonts.display, size: 11.2pt, weight: 650)[#title]
      #v(4pt)
      #text(size: 8.25pt)[#body]
    ]
  }
}

#let concept-map(columns: (1fr, 1fr), kind: none, ..nodes) = context {
  let cells = nodes.pos()
  if target() == "html" {
    let classes = if kind == none { "concept-map" } else { "concept-map " + kind }
    html.elem("div", attrs: (class: classes))[
      #for node in cells { node }
    ]
  } else {
    grid(
      columns: columns,
      column-gutter: 7pt,
      row-gutter: 7pt,
      align: top,
      ..cells,
    )
  }
}

#let flow-ribbon(..items) = context {
  let entries = items.pos()
  if target() == "html" {
    html.elem("ol", attrs: (class: "flow-ribbon"))[
      #for item in entries {
        html.elem("li")[#item]
      }
    ]
  } else {
    block(
      width: 100%,
      fill: palette.surface,
      inset: 8pt,
      radius: 4pt,
      stroke: 0.6pt + palette.rule,
    )[
      #set par(first-line-indent: 0em, justify: false, leading: 0.6em)
      #for (index, item) in entries.enumerate() {
        box(
          fill: palette.surface-light,
          inset: (x: 5pt, y: 3pt),
          radius: 3pt,
          stroke: 0.55pt + palette.rule,
        )[#text(font: fonts.sans, size: 7.2pt, weight: 600)[#item]]
        if index < entries.len() - 1 {
          h(3pt)
          text(font: fonts.sans, size: 8pt, weight: 700, fill: palette.saffron)[→]
          h(3pt)
        }
      }
    ]
  }
}

#let modern-note(body) = context {
  if target() == "html" {
    html.elem("aside", attrs: (class: "modern-note", role: "note"))[
      #source-badge("BIÊN SOẠN")
      #body
    ]
  } else {
    block(
      width: 100%,
      breakable: false,
      below: 5pt,
      inset: (left: 10pt),
      stroke: (left: 1.5pt + palette.muted),
    )[
      #set par(first-line-indent: 0em)
      #source-badge("BIÊN SOẠN")
      #v(4pt)
      #body
    ]
  }
}

#let day-card(day, title, duration, body) = context {
  if target() == "html" {
    semantic-region-counter.step()
    let title-id = "day-card-title-" + str(semantic-region-counter.get().first())
    html.elem(
      "section",
      attrs: (
        class: "day-card",
        role: "group",
        aria-labelledby: title-id,
      ),
    )[
      #html.elem("span", attrs: (class: "day-number"))[#day]
      #html.elem("span", attrs: (class: "day-title", id: title-id))[#title]
      #html.elem("span", attrs: (class: "day-duration"))[#duration]
      #body
    ]
  } else {
    block(
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
  }
}

#let check-row(label, body) = context {
  if target() == "html" {
    html.elem("div", attrs: (class: "check-row"))[*#label* #body]
  } else {
    grid(
      columns: (15pt, 1fr),
      column-gutter: 6pt,
      align: top,
      [#box(width: 8pt, height: 8pt, stroke: 0.7pt + palette.forest, radius: 1pt)],
      [
        #set par(first-line-indent: 0em)
        *#label* #body
      ],
    )
  }
}

#let reference-item(code, title, detail, url) = context {
  if target() == "html" {
    semantic-region-counter.step()
    let title-id = "reference-title-" + str(semantic-region-counter.get().first())
    html.elem(
      "section",
      attrs: (
        class: "reference-item",
        role: "group",
        aria-labelledby: title-id,
      ),
    )[
      #source-badge("KINH", refs: code)
      #html.elem("p", attrs: (class: "reference-title", id: title-id))[*#title*]
      #html.elem("p", attrs: (class: "reference-detail"))[#detail]
      #html.elem("p")[#link(url)[#edition.labels.source_link (#code)]]
    ]
  } else {
    block(
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
          #link(url)[#text(font: fonts.sans, size: 7pt)[#edition.labels.source_link (#code)]]
        ],
      )
    ]
  }
}
