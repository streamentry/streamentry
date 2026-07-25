# EPUB Build Module

## Overview

This folder owns deterministic EPUB 3 packaging. It converts the target-aware Typst HTML output into XML-conformant XHTML, generates navigation and package metadata, renders the synchronized PDF cover, creates the EPUB container, and fails loudly on structural defects.

## Key Components

- `build-epub.py`: recompiles PDF and HTML, verifies the immutable manuscript hash, removes the duplicate HTML cover, promotes Typst body headings from h2-h6 to h1-h5, creates namespaced XHTML and nested navigation, and checks semantics, accessibility metadata, manifest resources, anchors, warning classes, fixed ZIP timestamps, entry order, and uncompressed mimetype.
- `build/epub/`: ignored intermediate output.
- `dist/huong-den-nhap-luu.epub`: final artifact.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  T["book/main.typ"] --> P["Fresh PDF"]
  T --> H["Semantic HTML"]
  P --> C["Cover PNG"]
  H --> X["Cover removal, h1-h5 outline, and bodymatter"]
  X --> N["Nested semantic navigation"]
  N --> E["EPUB package"]
  C --> E
  E --> V["Structural validation"]
```

### Component Diagram

```mermaid
flowchart TB
  B["Builder"] --> M["mimetype and container"]
  B --> O["OPF metadata and manifest"]
  B --> N["Validated nested navigation"]
  B --> X["Book and cover XHTML"]
  M --> Z["EPUB ZIP"]
  O --> Z
  N --> Z
  X --> Z
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant U as Editor
  participant T as Typst
  participant B as EPUB builder
  participant V as Validator
  U->>B: Run build
  B->>T: Compile PDF and semantic HTML
  T-->>B: Current content and cover
  B->>B: Normalize namespaces, bodymatter, outline, and OPF
  B->>V: Validate archive and links
  V-->>U: Verified EPUB or exact failure
```

### State Machine

```mermaid
stateDiagram-v2
  [*] --> SourceChecked
  SourceChecked --> Compiled
  Compiled --> Packaged
  Packaged --> Rejected: warning, semantic, XML, link, or reproducibility defect
  Rejected --> Compiled
  Packaged --> Verified
  Verified --> [*]
```

### Data Flow Diagram

```mermaid
flowchart LR
  S["Typst source"] --> H["HTML"]
  S --> P["PDF"]
  H --> X["namespaced book.xhtml"]
  X --> N["h1-h5 outline"]
  P --> I["cover.png"]
  X --> Z["EPUB"]
  N --> Z
  I --> Z
  D["Metadata constants"] --> Z
```
