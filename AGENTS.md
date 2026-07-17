# Streamentry Typst Book

## Overview

This workspace turns `con-duong-niem-xu-mahasi-hop-nhat.md` into an A5 Vietnamese practice handbook. The source Markdown is preserved unchanged. The publication title is *Hướng Đến Nhập Lưu*, not a promise of attainment.

Accuracy has priority over continuity with the source. Keep early Pāli discourses, later Theravāda exegesis, the *Visuddhimagga*, Mahāsi instructions, and modern editorial or safety advice visibly separate.

## Key Components

- `con-duong-niem-xu-mahasi-hop-nhat.md`: immutable source manuscript. Recorded SHA-256: `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440`.
- `book/main.typ`: only publication entry point.
- `book/theme.typ`: A5 page, type, print-safe white paper palette, and global show rules.
- `book/components.typ`: source badges, chapter openers, practice cards, cautions, and reference blocks.
- `book/chapters/`: editorial chapters.
- `book/appendices/`: reusable practice tools.
- `book/references/claim-ledger.md`: claim-to-source audit trail.
- `dist/huong-den-nhap-luu.pdf`: verified deliverable.

The canonical publication credit is `TS. Lê Việt Hồng - Cư Sĩ Chánh Niệm + ChatGPT`. Keep the cover, PDF metadata, and README synchronized.

Build from the workspace root:

```sh
typst compile --root /Volumes/SSD/streamentry book/main.typ dist/huong-den-nhap-luu.pdf
```

Do not impersonate the Buddha, fabricate quotations, or turn a retreat schedule, noting technique, cessation experience, or teacher verdict into a canonical guarantee of stream-entry.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  A["Source manuscript"] --> B["Doctrinal claim audit"]
  B --> C["Six-tier provenance"]
  C --> D["Chapter modules"]
  D --> E["Typst composition"]
  E --> F["PDF render, grayscale, and print QA"]
  F --> G["Public handbook"]
```

### Component Diagram

```mermaid
flowchart TB
  M["book/main.typ"] --> T["theme.typ"]
  M --> C["components.typ"]
  M --> H["chapters/*.typ"]
  M --> A["appendices/*.typ"]
  H --> C
  A --> C
  H -. "claim codes" .-> L["references/claim-ledger.md"]
  L -. "source URLs" .-> S["Primary and authoritative editions"]
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant E as Editor
  participant L as Claim ledger
  participant T as Typst
  participant Q as PDF QA
  E->>L: Verify doctrine, speaker, edition, and source tier
  L-->>E: Return source code and caveat
  E->>T: Compose source-labelled chapter
  T-->>Q: Compile A5 PDF
  Q-->>E: Report overflow, page rhythm, and text defects
  E->>T: Correct and recompile
```

### State Machine

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Audited: claims classified and sourced
  Audited --> Composed: Typst modules assembled
  Composed --> Rendered: PDF compiles
  Rendered --> Audited: defect or unsupported claim found
  Rendered --> Verified: structural and visual QA pass
  Verified --> [*]
```

### Data Flow Diagram

```mermaid
flowchart LR
  S["Source manuscript"] --> E["Editorial rewrite"]
  P["Primary texts and editions"] --> L["Claim ledger"]
  L --> E
  E --> T["Typst chapter and appendix modules"]
  Y["Theme and components"] --> T
  T --> C["Typst compiler"]
  C --> D["A5 PDF"]
  D --> Q["Text, structure, and visual QA"]
  Q -. "corrections" .-> E
```
