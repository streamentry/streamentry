# Publication Automation and Correction Intake

## Overview

This folder owns read-only GitHub Actions validation and the public correction-intake form for the book. Pull requests and pushes to `main` rebuild and verify the exact PDF and EPUB on the canonical macOS 15 ARM64 runner with only a read-only ephemeral `GITHUB_TOKEN`, no repository or environment secrets, no write permissions, no release publication, and no raw pilot-data upload. The issue form is public and must not solicit direct contact or private medical data.

## Key Components

- `workflows/publication-ci.yml`: fixes the builder to macOS 15 ARM64; pins actions by full commit SHA; pins Typst, Inter, and EPUBCheck by version and checksum; installs locked Python and DAISY Ace dependencies; disables system fonts; rebuilds both formats; and requires the tracked artifacts, release record, tests, schemas, EPUBCheck, and Ace to pass.
- `ISSUE_TEMPLATE/correction.yml`: structured public intake for source, doctrine, safety, rights, accessibility, text, and layout corrections. Require a precise location, current wording, concern, and privacy acknowledgement; keep evidence optional for obvious production defects and never add a contact field.
- Keep PR execution on `pull_request`. Never combine PR-head checkout with `pull_request_target`, `workflow_run` privileges, secrets, or a write-capable token.
- Do not promote PR-built artifacts into a privileged publication job. Any future release job must rebuild from the trusted `main` SHA.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  P["Pull request or main push"] --> C["Read-only checkout"]
  C --> T["Controlled toolchain"]
  T --> B["PDF and EPUB rebuild"]
  B --> E["Release-evidence verifier"]
  E --> Q["Tests, schemas, EPUBCheck, Ace"]
  Q --> G["Required CI result"]
  I["Public correction form"] --> R["Issue with location, wording, concern and optional evidence"]
  R --> P
```

### Component Diagram

```mermaid
flowchart TB
  W["publication-ci.yml"] --> A["SHA-pinned GitHub actions"]
  W --> D["Checksum-pinned binaries"]
  W --> L["Locked Python and Node dependencies"]
  W --> R["Repository build and verification scripts"]
  F["correction.yml"] --> I["Privacy-bounded issue intake"]
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant G as GitHub
  participant R as Ephemeral runner
  participant B as Book builder
  participant V as Validators
  G->>R: Dispatch unprivileged candidate
  R->>B: Rebuild with isolated fonts
  B-->>R: PDF and EPUB
  R->>V: Compare evidence and run format checks
  V-->>G: One pass or exact failure
```

### State Machine

```mermaid
stateDiagram-v2
  [*] --> Dispatched
  Dispatched --> Installing: read-only checkout
  Installing --> Verifying: controlled tools ready
  Verifying --> Rejected: any build or validation defect
  Verifying --> Passed: every gate succeeds
  Rejected --> [*]
  Passed --> [*]
```

### Data Flow Diagram

```mermaid
flowchart LR
  C["Candidate commit"] --> R["Ephemeral runner"]
  M["Pinned manifests and checksums"] --> R
  R --> B["Rebuilt PDF and EPUB"]
  E["Committed release evidence"] --> V["Release verifier"]
  B --> V
  B --> F["EPUBCheck and Ace"]
  V --> G["CI result"]
  F --> G
```
