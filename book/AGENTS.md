# Typst Book Module

## Overview

This module owns the A5 publication system for *Hướng Đến Nhập Lưu*. `main.typ` stays composition-only. Theme tokens and show rules belong in `theme.typ`; repeated visual patterns belong in `components.typ`; prose belongs in chapter or appendix files.

## Key Components

- `main.typ`: metadata, canonical author credit, cover, and include order.
- `theme.typ`: Libertinus Serif and Inter type system, print-safe white paper palette, A5 margins.
- `components.typ`: stable content blocks only. `source-line` and `modern-note` place badges on a separate line so prose retains the full reading measure.
- `chapters/`: narrative and instructional sequence.
- `appendices/`: printable tools and reference material.
- `references/`: doctrinal audit trail.

The canonical publication credit is `TS. Lê Việt Hồng - Cư Sĩ Chánh Niệm + ChatGPT`. Do not edit the visible cover credit without updating PDF metadata and the root README in the same change.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  T["Theme tokens"] --> M["Main composition"]
  C["Components"] --> M
  H["Chapters"] --> M
  A["Appendices"] --> M
  M --> P["A5 PDF"]
```

### Component Diagram

```mermaid
flowchart TB
  B["Source badge"] --> H["Chapter content"]
  P["Practice card"] --> H
  W["Caution block"] --> H
  H --> M["main.typ"]
  R["Reference item"] --> S["Source chapter"]
  S --> M
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant C as Chapter
  participant M as Main
  participant T as Theme
  participant P as PDF
  C->>M: Included content
  T->>M: Page and type rules
  M->>P: Typst compile
  P-->>C: Visual and text QA findings
```
