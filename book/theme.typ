#import "edition.typ": edition

#let palette = (
  ink: rgb("#211d18"),
  muted: rgb("#6f675e"),
  paper: white,
  surface: rgb("#f2f2f0"),
  surface-light: white,
  saffron: rgb("#a75d20"),
  forest: rgb("#315b4b"),
  clay: rgb("#8b4f3d"),
  indigo: rgb("#4f5572"),
  research: rgb("#3f6687"),
  rule: rgb("#c9c9c5"),
  inverse: white,
)

#let fonts = (
  display: "Libertinus Serif",
  body: "Libertinus Serif",
  sans: "Inter",
  mono: "DejaVu Sans Mono",
)

#let space = (
  xs: 3pt,
  sm: 7pt,
  md: 12pt,
  lg: 20pt,
  xl: 32pt,
  xxl: 52pt,
)

// Biểu tượng cho sáu tầng nguồn. Cùng một bộ hình được dùng cho PDF (ảnh SVG
// đánh dấu là artifact) và cho HTML/EPUB (ảnh nền CSS), nên chữ đọc được của
// nhãn chỉ còn là câu dẫn nguồn, không lặp lại tên loại nguồn.
#let source-icon-paths = (
  "source-kinh": "<circle cx='8' cy='8' r='6.1' fill='none' stroke='{c}' stroke-width='1.4'/><path d='M8 1.9v12.2M1.9 8h12.2M3.7 3.7l8.6 8.6M12.3 3.7l-8.6 8.6' stroke='{c}' stroke-width='0.9'/><circle cx='8' cy='8' r='1.7' fill='{c}'/>",
  "source-mahasi": "<circle cx='8' cy='3.1' r='2.1' fill='{c}'/><path d='M8 6.1c-2 0-3.2 1.6-3.6 4l-2.8 2.2c-.5.4-.2 1.3.5 1.3h11.8c.7 0 1-.9.5-1.3l-2.8-2.2c-.4-2.4-1.6-4-3.6-4z' fill='{c}'/>",
  "source-thanh-tinh-dao": "<path d='M8 3.6C6.3 2.4 4 2.1 1.5 2.5v10.3c2.5-.4 4.8-.1 6.5 1.1 1.7-1.2 4-1.5 6.5-1.1V2.5C12 2.1 9.7 2.4 8 3.6zM8 3.6v10.3' fill='none' stroke='{c}' stroke-width='1.3' stroke-linejoin='round'/>",
  "source-luan-giai": "<rect x='2.6' y='1.6' width='10.8' height='12.8' rx='1.5' fill='none' stroke='{c}' stroke-width='1.3'/><path d='M5.1 5.2h5.8M5.1 8h5.8M5.1 10.8h3.8' stroke='{c}' stroke-width='1.3' stroke-linecap='round'/>",
  "source-nghien-cuu": "<path d='M6.2 1.8h3.6v4.4h4.4v3.6H9.8v4.4H6.2V9.8H1.8V6.2h4.4z' fill='{c}'/>",
  "source-bien-soan": "<path d='M11.2 1.7l3.1 3.1-8.6 8.6-4 .9.9-4z' fill='none' stroke='{c}' stroke-width='1.3' stroke-linejoin='round'/><path d='M9.6 3.3l3.1 3.1' stroke='{c}' stroke-width='1.3'/>",
)

#let source-icon-svg(cls, color) = (
  "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'>"
    + source-icon-paths.at(cls).replace("{c}", color)
    + "</svg>"
)

#let _css-svg-url(cls, color) = {
  let svg = source-icon-svg(cls, color)
    .replace("%", "%25")
    .replace("#", "%23")
    .replace("<", "%3C")
    .replace(">", "%3E")
  "url(\"data:image/svg+xml," + svg + "\")"
}

#let _source-icon-css(colors) = {
  let rules = ()
  for (cls, color) in colors {
    rules.push("." + cls + " .source-icon { background-image: " + _css-svg-url(cls, color) + "; }")
  }
  rules.join("\n")
}

#let source-icon-css = (
  ".source-icon { display: inline-block; width: 1em; height: 1em; margin-right: 0.4em; vertical-align: -0.14em; background-position: center; background-repeat: no-repeat; background-size: contain; }\n"
    + _source-icon-css((
      "source-kinh": "#315b4b",
      "source-mahasi": "#7c4636",
      "source-thanh-tinh-dao": "#8c4e1b",
      "source-luan-giai": "#4f5572",
      "source-nghien-cuu": "#3f6687",
      "source-bien-soan": "#625b53",
    ))
    + "\n@media (prefers-color-scheme: dark) {\n"
    + _source-icon-css((
      "source-kinh": "#8bc5ad",
      "source-mahasi": "#dba08d",
      "source-thanh-tinh-dao": "#e7a367",
      "source-luan-giai": "#b7bddb",
      "source-nghien-cuu": "#91bce0",
      "source-bien-soan": "#c6beb5",
    ))
    + "\n}"
)

#let apply-theme(body) = context {
  if target() == "html" {
    set text(lang: edition.metadata.language)
    html.style("
      :root {
        color-scheme: light dark;
        --ink: #211d18;
        --muted: #625b53;
        --paper: #ffffff;
        --surface: #f2f2f0;
        --surface-light: #fafaf8;
        --saffron: #8c4e1b;
        --forest: #315b4b;
        --clay: #7c4636;
        --indigo: #4f5572;
        --research: #3f6687;
        --rule: #c9c9c5;
      }
      html { font-family: Georgia, 'Times New Roman', serif; line-height: 1.55; }
      body { margin: 0 auto; padding: 1.2rem; max-width: 46rem; color: var(--ink); background: var(--paper); }
      h1, h2, h3 { line-height: 1.2; page-break-after: avoid; break-after: avoid; }
      h1 { margin: 2.4rem 0 0.8rem; font-size: 2rem; }
      h2 { margin: 2rem 0 0.7rem; font-size: 1.38rem; }
      h3 { margin: 1.5rem 0 0.5rem; font-size: 1.05rem; color: var(--saffron); }
      p { margin: 0.72rem 0; }
      li { margin: 0.38rem 0; }
      a { color: var(--saffron); }
      .cover { min-height: 70vh; display: flex; flex-direction: column; justify-content: center; text-align: center; }
      .cover-kicker, .eyebrow, .chapter-number { font-family: Arial, sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
      .cover h1 { margin: 1rem 0; font-size: 2.6rem; }
      .cover-subtitle, .chapter-deck { color: var(--muted); }
      .cover-author { margin-top: 1.8rem; color: var(--forest); font-weight: 700; }
      .cover-epigraph { max-width: 24rem; margin: 2rem auto 0.8rem; padding: 0.15rem 0 0.15rem 1rem; border-left: 0.12rem solid var(--forest); text-align: left; }
      .cover-epigraph p { margin: 0; font-style: italic; line-height: 1.65; }
      .cover-epigraph cite { display: block; margin-top: 0.75rem; color: var(--muted); font-family: Arial, sans-serif; font-size: 0.76rem; font-style: normal; font-weight: 600; }
      .cover-edition { margin-top: 0.7rem; color: var(--muted); font-family: Arial, sans-serif; font-size: 0.8rem; }
      .introduction-opener { margin: 2.7rem 0 1.3rem; text-align: center; }
      .introduction-opener h1, .introduction-opener h2 { margin-top: 0.45rem; font-size: 1.8rem; }
      .chapter-opener { margin-top: 3.5rem; padding-top: 1rem; border-top: 0.2rem solid var(--saffron); }
      .chapter-opener h1, .chapter-opener h2 { margin-top: 0.45rem; }
      .chapter-deck { font-family: Arial, sans-serif; font-size: 0.98rem; max-width: 38rem; }
      .part-opener { margin-top: 4rem; padding-top: 1.25rem; border-top: 0.35rem solid var(--forest); }
      .part-deck { color: var(--muted); font-family: Arial, sans-serif; font-size: 0.98rem; max-width: 38rem; }
      .provenance { margin: 1rem 0 1.6rem; }
      .source-badge { display: inline; font-family: Arial, sans-serif; font-size: 0.8rem; font-weight: 600; line-height: 1.45; }
      .source-badge a { color: inherit; text-decoration-thickness: 0.06rem; }
      .source-line .source-badge, .modern-note .source-badge, .provenance .source-badge { display: block; margin: 0 0 0.45rem; }
      .eyebrow.card-label { text-transform: none; letter-spacing: 0.01em; font-weight: 650; }
      .source-kinh { color: var(--forest); }
      .source-mahasi, .source-caution { color: var(--clay); }
      .source-thanh-tinh-dao { color: var(--saffron); }
      .source-luan-giai { color: var(--indigo); }
      .source-nghien-cuu { color: var(--research); }
      .source-bien-soan { color: var(--muted); }
      .source-line, .modern-note { margin: 1.2rem 0; padding: 0.2rem 0 0.2rem 0.9rem; border-left: 0.18rem solid var(--forest); }
      .modern-note { border-left-color: var(--muted); }
      .practice-card, .caution, .scripture-quote { margin: 1.25rem 0; padding: 0.9rem 1rem; border: 0.06rem solid var(--rule); border-radius: 0.35rem; background: var(--surface-light); }
      .caution { border-color: #c7a79c; background: #f7efec; }
      .scripture-quote { background: var(--surface); font-style: italic; }
      .card-title { margin: 0.35rem 0 0.65rem; overflow-wrap: anywhere; font-size: 1.12rem; font-weight: 700; }
      .quote-source { margin-top: 0.8rem; overflow-wrap: anywhere; color: var(--muted); font-family: Arial, sans-serif; font-size: 0.78rem; font-style: normal; }
      .worksheet-fields { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem 0.8rem; margin: 0.8rem 0 1rem; }
      .worksheet-field { min-width: 0; padding-bottom: 0.3rem; border-bottom: 0.08rem solid var(--rule); overflow-wrap: anywhere; }
      .day-card { margin: 1rem 0; padding: 0.75rem 0; border-bottom: 0.06rem solid var(--rule); }
      .day-number { display: inline-block; min-width: 1.6rem; margin-right: 0.45rem; padding: 0.15rem; border-radius: 50%; color: var(--paper); background: var(--saffron); text-align: center; font-family: Arial, sans-serif; font-weight: 700; }
      .day-title { font-weight: 700; }
      .day-duration { margin-left: 0.45rem; color: var(--saffron); font-family: Arial, sans-serif; font-size: 0.8rem; }
      .check-row { margin: 0.55rem 0; padding-left: 1.25rem; }
      .check-row::before { content: '□'; margin-left: -1.25rem; margin-right: 0.35rem; color: var(--forest); }
      .reference-item { margin: 0.8rem 0; padding-bottom: 0.65rem; border-bottom: 0.06rem solid var(--rule); }
      .reference-title { margin-bottom: 0.15rem; }
      .reference-detail { margin-top: 0.15rem; color: var(--muted); }
      .decision-map { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.8rem; margin: 1.25rem 0; }
      .decision-node { min-width: 0; padding: 0.9rem 1rem; border: 0.06rem solid var(--rule); border-radius: 0.35rem; background: var(--surface-light); overflow-wrap: anywhere; }
      .decision-node:nth-child(1) { border-color: var(--clay); }
      .decision-node:nth-child(2) { border-color: var(--forest); }
      .decision-node:nth-child(3) { border-color: var(--indigo); }
      .decision-node:nth-child(4) { border-color: var(--saffron); }
      .decision-wide { grid-column: 1 / -1; }
      .concept-map { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.8rem; margin: 1.25rem 0; }
      .concept-map-three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
      .concept-node { min-width: 0; padding: 0.85rem 0.95rem; border: 0.06rem solid var(--rule); border-top-width: 0.22rem; border-radius: 0.35rem; background: var(--surface-light); overflow-wrap: anywhere; }
      .concept-node:nth-child(4n + 1) { border-top-color: var(--clay); }
      .concept-node:nth-child(4n + 2) { border-top-color: var(--saffron); }
      .concept-node:nth-child(4n + 3) { border-top-color: var(--forest); }
      .concept-node:nth-child(4n) { border-top-color: var(--indigo); }
      .concept-node .eyebrow { margin: 0 0 0.3rem; color: var(--muted); }
      .concept-node .card-title { margin-top: 0; }
      .flow-ribbon { display: flex; flex-wrap: wrap; align-items: center; gap: 0.45rem; margin: 1.1rem 0; padding: 0.75rem; border: 0.06rem solid var(--rule); border-radius: 0.35rem; background: var(--surface); list-style: none; }
      .flow-ribbon li { display: flex; min-width: 0; align-items: center; margin: 0; padding: 0.32rem 0.5rem; border: 0.06rem solid var(--rule); border-radius: 0.28rem; background: var(--surface-light); font-family: Arial, sans-serif; font-size: 0.82rem; font-weight: 700; overflow-wrap: anywhere; }
      .flow-ribbon li:not(:last-child)::after { content: '→'; margin-left: 0.55rem; color: var(--saffron); }
      nav[role='doc-toc'] { margin: 1.5rem 0; padding: 0.75rem 1rem; background: var(--surface-light); }
      @media (max-width: 30rem) {
        .worksheet-fields { grid-template-columns: minmax(0, 1fr); }
        .decision-map { grid-template-columns: minmax(0, 1fr); }
        .decision-wide { grid-column: auto; }
        .concept-map, .concept-map-three { grid-template-columns: minmax(0, 1fr); }
      }
      @media (prefers-color-scheme: dark) {
        :root {
          --ink: #eee9e2;
          --muted: #c6beb5;
          --paper: #171513;
          --surface: #262320;
          --surface-light: #211e1b;
          --saffron: #e7a367;
          --forest: #8bc5ad;
          --clay: #dba08d;
          --indigo: #b7bddb;
          --research: #91bce0;
          --rule: #59534d;
        }
        .caution { background: #2a1d19; border-color: #755247; }
      }
    ")
    html.style(source-icon-css)
    body
  } else {
    set page(
    paper: "a5",
    fill: palette.paper,
    binding: left,
    margin: (
      top: 16mm,
      bottom: 19mm,
      inside: 22mm,
      outside: 14mm,
    ),
    header: context {
      let n = counter(page).get().first()
      let phys = here().page()
      let here = here()
      let all-heads = query(selector(heading.where(level: 1)))
      let on-page = all-heads.filter(h => h.location().page() == phys)
      if on-page.len() > 0 {
        // Chapter, part and appendix opener pages carry their own large
        // title; a running header there would repeat or lag behind.
      } else {
        let heads = query(selector(heading.where(level: 1)).before(here))
        let parts = query(selector(<phan>).before(here))
        let ch = none
        for h in heads {
          let is-part = false
          for p in parts {
            if p.location() == h.location() {
              is-part = true
            }
          }
          if not is-part {
            ch = h
          }
        }
        let run(body) = text(
          font: fonts.sans,
          size: 6.6pt,
          tracking: 0.12em,
          fill: palette.muted,
        )[#body]
        if calc.odd(n) {
          if ch == none {
            align(right, run(upper(edition.metadata.title)))
          } else {
            align(right, run(upper(ch.body)))
          }
        } else {
          align(left, run(upper(edition.metadata.title)))
        }
      }
    },
    numbering: "1",
    number-align: center + bottom,
  )

  set text(
    font: fonts.body,
    size: 10.2pt,
    fill: palette.ink,
    lang: edition.metadata.language,
  )
  set par(
    justify: true,
    leading: 0.66em,
    spacing: 0.6em,
    first-line-indent: 1em,
  )
  set heading(numbering: none, bookmarked: true)
  set list(indent: 1.1em, body-indent: 0.55em, spacing: 0.38em)
  set enum(indent: 1.1em, body-indent: 0.55em, spacing: 0.38em)
  set quote(block: true)

  show heading.where(level: 1): it => block(
    breakable: false,
  )[
    #text(
      font: fonts.display,
      size: 25pt,
      weight: 600,
      fill: palette.ink,
    )[#it.body]
  ]

  show heading.where(level: 2): it => block(
    above: space.lg,
    below: space.sm,
    breakable: false,
  )[
    #text(
      font: fonts.display,
      size: 15.5pt,
      weight: 600,
      fill: palette.ink,
    )[#it.body]
  ]

  show heading.where(level: 3): it => block(
    above: space.md,
    below: space.xs,
    breakable: false,
  )[
    #text(
      font: fonts.sans,
      size: 9.2pt,
      weight: 650,
      tracking: 0.035em,
      fill: palette.saffron,
    )[#upper(it.body)]
  ]

  show link: set text(fill: palette.saffron)
  show footnote.entry: set text(size: 8pt)
  show raw: set text(font: fonts.mono, size: 8.6pt)
  show strong: set text(weight: 700)

    body
  }
}
