# EPUB Build Module

## Overview

This folder owns deterministic PDF and EPUB publication checks. It converts the target-aware Typst HTML output into XML-conformant XHTML, generates navigation and package metadata, renders the synchronized cover directly through Typst, creates the EPUB container, verifies the release record against both binaries, and fails loudly on structural defects.

## Key Components

- `build-epub.py`: recompiles PDF and HTML, renders page 1 directly to the EPUB cover PNG, verifies the immutable manuscript hash, removes the duplicate HTML cover, promotes Typst body headings from h2-h6 to h1-h5, creates namespaced XHTML and nested navigation, and checks semantics, accessibility metadata, manifest resources, anchors, warning classes, fixed ZIP timestamps, entry order, and uncompressed mimetype.
- `verify_release.py`: orchestrates the release contract and compares the immutable source plus exact binary identities.
- `release_evidence.py`: parses only the visible artifact table and anchors the immutable source hash and publication credit.
- `release_pdf.py`: verifies PDF metadata, tagging, security flags, file size, and every page's A5 geometry and rotation.
- `release_epub.py`: verifies the active package, exact manifest and spine, passive XHTML, metadata, resolved unique navigation, and content/cover counts.
- `beginner_pilot_contract.py`: fixed task ids, criteria, thresholds, allowed fields, cohort rules, and the exact ten-file scoring contract.
- `beginner_pilot_validation.py`: strict JSON, schema, consent, eligibility, task-state, fixed stop-reason, bounded contact-data detection, and retention validation.
- `beginner_pilot_artifact.py`: verifies hashes and page count against real files and committed Git blobs, plus a bounded EPUB container check.
- `beginner_pilot_manifest.py`: loads the only authoritative manifest, rejects direct or nested record additions and reachable Git-history exposure, enforces chronological first-five selection among at most seven starts, verifies canonical origin/main ancestry, and binds the running scorer to the committed contract.
- `beginner_pilot.py`: reusable scoring rules for one validated five-reader novice cohort.
- `score-beginner-pilot.py`: manifest-only CLI that applies fixed comprehension, EPUB, completeness, and distress-veto gates and emits a privacy-coarsened aggregate report without first answers or notes.
- The pilot runtime requires Python's `jsonschema` package. A local manifest cannot independently prove its asserted registration time or that the moderator did not omit the terminal attempt; stronger custody needs an external append-only timestamped registry.
- Keep the OPF `dcterms:modified` value fixed within a release for reproducibility, but advance it when the published content changes to a new release date.
- `build/epub/`: ignored intermediate output.
- `dist/huong-den-nhap-luu.epub`: final artifact.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  T["book/main.typ"] --> P["Fresh PDF"]
  T --> C["Typst page-1 PNG"]
  T --> H["Semantic HTML"]
  H --> X["Cover removal, h1-h5 outline, and bodymatter"]
  X --> N["Nested semantic navigation"]
  N --> E["EPUB package"]
  C --> E
  E --> V["Builder structural validation"]
  E --> W["Separate release-evidence verifier"]
  R["Frozen manifest and ordered attempts"] --> S["Deterministic cohort scorer"]
  S --> G["Aggregate gate report"]
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
  S["Pilot scorer"] --> R["Manifest, contract, eligibility, and committed-artifact checks"]
  S --> G["Eight task gates"]
  R --> A["Aggregate report"]
  G --> A
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant U as Editor
  participant T as Typst
  participant B as EPUB builder
  participant V as Validator
  participant S as Pilot scorer
  U->>B: Run build
  B->>T: Compile PDF and semantic HTML
  T-->>B: Current content and cover
  B->>B: Normalize namespaces, bodymatter, outline, and OPF
  B->>V: Validate archive and links
  V-->>U: Verified EPUB or exact failure
  U->>S: Score one manifest with all ordered attempts
  S-->>U: Aggregate gate report or exact invalid-data error
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
  [*] --> PilotFrozen
  PilotFrozen --> PilotRecorded: every start added in order
  PilotRecorded --> PilotRejected: invalid evidence, distress, or failed gate
  PilotRecorded --> PilotPassed: first five satisfy all fixed thresholds
  PilotRejected --> [*]
  PilotPassed --> [*]
```

### Data Flow Diagram

```mermaid
flowchart LR
  T["Typst source"] --> H["HTML"]
  T --> P["PDF"]
  H --> X["namespaced book.xhtml"]
  X --> N["h1-h5 outline"]
  T --> I["Typst page-1 cover.png"]
  X --> Z["EPUB"]
  N --> Z
  I --> Z
  D["Metadata constants"] --> Z
  R["Manifest and pseudonymous attempt JSON"] --> C["Cohort scorer"]
  C --> A["Aggregate report"]
```
