#let palette = (
  ink: rgb("#211d18"),
  muted: rgb("#6f675e"),
  paper: rgb("#f8f3e9"),
  surface: rgb("#eee5d6"),
  surface-light: rgb("#fffdf8"),
  saffron: rgb("#a75d20"),
  forest: rgb("#315b4b"),
  clay: rgb("#8b4f3d"),
  indigo: rgb("#4f5572"),
  research: rgb("#3f6687"),
  rule: rgb("#d6c8b5"),
  inverse: rgb("#fffdf7"),
)

#let fonts = (
  display: ("Libertinus Serif", "PT Serif", "Charter"),
  body: ("Libertinus Serif", "PT Serif", "Charter"),
  sans: ("Inter", "Avenir Next", "Arial"),
  mono: ("DejaVu Sans Mono", "Menlo"),
)

#let space = (
  xs: 3pt,
  sm: 7pt,
  md: 12pt,
  lg: 20pt,
  xl: 32pt,
  xxl: 52pt,
)

#let apply-theme(body) = {
  set page(
    paper: "a5",
    fill: palette.paper,
    margin: (
      top: 16mm,
      right: 15mm,
      bottom: 19mm,
      left: 17mm,
    ),
    header: align(
      right,
      text(
        font: fonts.sans,
        size: 6.6pt,
        tracking: 0.12em,
        fill: palette.muted,
      )[HƯỚNG ĐẾN NHẬP LƯU],
    ),
    numbering: "1",
    number-align: center + bottom,
  )

  set text(
    font: fonts.body,
    size: 10.2pt,
    fill: palette.ink,
    lang: "vi",
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
