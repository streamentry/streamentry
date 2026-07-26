# Publication Verification Tests

## Overview

This folder owns focused regression tests for the builder, pilot scorer, and release gate. Release-verifier tests are split by evidence, PDF, EPUB, and end-to-end integration so each module stays small and each failure names one contract.

## Key Components

- `release_verifier_fixtures.py`: shared synthetic Markdown, PDFInfo, OPF, XHTML, and EPUB fixtures.
- `test_release_evidence.py`: visible-table parsing plus immutable hash and canonical-credit anchors.
- `test_release_pdf.py`: metadata, encryption, all-page size, and rotation regressions.
- `test_release_epub.py`: active-rootfile, fixed manifest/spine, passive XHTML, and TOC-target regressions.
- `test_release_verifier.py`: integration check against the tracked release candidate.
- `test_external_release_gates.py`: protocol-fingerprint, status, gate-specific evidence-role, evidence-binding, path-reuse, and permitted-claim regressions for the external release packet.
- Existing `test_beginner_pilot*.py` files retain the novice-cohort privacy and scoring contract.
- When an intentional chapter or layout change alters the tracked PDF extent, update the integration expectation only after rebuilding both artifacts and updating `release-evidence.md`; do not change synthetic parser fixtures merely to mirror the current book.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  F["Synthetic fixtures"] --> E["Evidence tests"]
  F --> P["PDF tests"]
  F --> U["EPUB tests"]
  F --> X["External gate tests"]
  R["Tracked release"] --> I["Integration test"]
  E --> G["Full test gate"]
  P --> G
  U --> G
  I --> G
```

### Component Diagram

```mermaid
flowchart TB
  X["release_verifier_fixtures.py"] --> E["test_release_evidence.py"]
  X --> P["test_release_pdf.py"]
  X --> U["test_release_epub.py"]
  V["verify_release.py"] --> I["test_release_verifier.py"]
  G["external_release_gates.py"] --> Q["role and gate-contract tests"]
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant T as Test runner
  participant F as Fixtures
  participant M as Release modules
  participant A as Tracked artifacts
  T->>F: Create bounded adversarial input
  T->>M: Parse or validate input
  M-->>T: Exact rejection or facts
  T->>A: Run integration contract
  A-->>T: Matching release evidence
  T->>M: Mutate a gate status or evidence binding
  M-->>T: Exact rejection
```

### State Machine

```mermaid
stateDiagram-v2
  [*] --> Prepared
  Prepared --> Exercised
  Exercised --> Failed: expected contract not enforced
  Exercised --> Passed: expected fact or rejection observed
  Failed --> [*]
  Passed --> [*]
```

### Data Flow Diagram

```mermaid
flowchart LR
  M["Markdown fixture"] --> E["Evidence parser"]
  P["pdfinfo fixtures"] --> D["PDF contract"]
  X["EPUB fixtures"] --> U["EPUB contract"]
  A["dist artifacts"] --> V["Release orchestrator"]
  E --> R["Test result"]
  D --> R
  U --> R
  V --> R
  G["Gate registry"] --> R
```
