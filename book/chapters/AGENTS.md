# Chapters

## Overview

Chapters carry the explanatory arc from a seven-day start through the full path, Mahāsi technique, daily life, safety, insight maps, and canonical descriptions of stream-entry. Keep each file below 300 lines.

## Key Components

- Begin with `chapter(...)`.
- Attach `source-badge(...)` or `source-line(...)` to non-obvious doctrinal claims.
- Use prose for argument and cards only for procedures, checks, or source boundaries.
- Never make a schedule or phenomenological map sound universal.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  A["Orientation"] --> B["Foundations"] --> C["Technique"] --> D["Integration"] --> E["Safety"] --> F["Attainment criteria"]
```

### Component Diagram

```mermaid
flowchart TB
  S["Source claim"] --> P["Prose paragraph"]
  E["Exercise"] --> C["Practice card"]
  R["Risk"] --> W["Caution block"]
  P --> H["Chapter"]
  C --> H
  W --> H
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant A as Author
  participant S as Source
  participant C as Chapter
  A->>S: Verify speaker, wording, and scope
  S-->>A: Source code and caveat
  A->>C: Write labelled prose
```
