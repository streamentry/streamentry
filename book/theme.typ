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
      .cover-edition { margin-top: 0.7rem; color: var(--muted); font-family: Arial, sans-serif; font-size: 0.8rem; }
      .introduction-opener { margin: 2.7rem 0 1.3rem; text-align: center; }
      .introduction-opener h1, .introduction-opener h2 { margin-top: 0.45rem; font-size: 1.8rem; }
      .chapter-opener { margin-top: 3.5rem; padding-top: 1rem; border-top: 0.2rem solid var(--saffron); }
      .chapter-opener h1, .chapter-opener h2 { margin-top: 0.45rem; }
      .chapter-deck { font-family: Arial, sans-serif; font-size: 0.98rem; max-width: 38rem; }
      .provenance { margin: 1rem 0 1.6rem; }
      .source-badge { display: inline-block; margin: 0.1rem 0.25rem 0.1rem 0; padding: 0.18rem 0.46rem; border: 0.06rem solid currentColor; border-radius: 0.22rem; font-family: Arial, sans-serif; font-size: 0.76rem; font-weight: 700; letter-spacing: 0.035em; }
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
    header: align(
      right,
      text(
        font: fonts.sans,
        size: 6.6pt,
        tracking: 0.12em,
        fill: palette.muted,
      )[#upper(edition.metadata.title)],
    ),
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
    spacing: 0.28em,
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
