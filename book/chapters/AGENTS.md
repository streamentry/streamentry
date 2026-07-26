# Chapters

## Overview

Chapters carry the explanatory arc from a seven-day start through the full path, dependent origination at feeling and craving, Mahāsi technique, daily life, safety, canonical descriptions of stream-entry, and the insight map as later reference. Prefer files below 300 lines, but do not compress sourced explanation merely to satisfy the line target.

## Key Components

- Begin with `chapter(...)`.
- Frontmatter must give a short non-linear reading route: first practice, early safety, foundations, retreat screening, then the insight map as later reference.
- Attach `source-badge(...)` or `source-line(...)` to non-obvious doctrinal claims.
- Use prose for argument and cards only for procedures, checks, or source boundaries.
- Never make a schedule, a “feeling to craving” intervention, or a phenomenological map sound universal.
- Put hard decision rules where a beginner first encounters the decision. Do not rely on a later safety or retreat chapter to repair ambiguous week-one instructions.
- Give every technical or Pāli term a plain-language gloss in the same paragraph or immediately adjacent block on first use. A rear glossary reinforces but does not rescue an opaque chapter.
- Open each chapter by carrying forward the minimum prior idea and naming the next problem. Before a dense list, orient the reader; after it, state the usable synthesis.
- Keep repeated warnings only when they add a threshold, decision rule, or source-boundary correction. Otherwise point to the full treatment.
- When explaining attainment, keep the first three fetters, the full five lower fetters, and the four fruits distinct. Stream-entry cuts the first three fetters; non-returning concerns the full five lower fetters; “sa-môn quả” names the four fruits, not one vague success state.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  A["Orientation"] --> B["Foundations"] --> C["Dependent origination"] --> D["Technique"] --> E["Integration"] --> F["Safety"] --> G["Attainment criteria"] --> H["Insight map as later reference"]
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
