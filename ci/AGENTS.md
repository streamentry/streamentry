# Publication CI Dependencies

## Overview

This folder contains only pinned dependency contracts for the ephemeral publication validator. It is not a runtime application and must not contain reader data, credentials, or generated reports.

## Key Components

- `requirements.txt`: exact Python versions and reviewed Linux x86-64 plus macOS ARM64 wheel hashes for JSON Schema validation and Ruff. The macOS ARM64 wheels serve the canonical hosted builder; the Linux hashes retain a reviewed local verification path.
- `package.json` and `package-lock.json`: DAISY Ace CLI 1.4.6 and its integrity-locked dependency graph.
- `verapdf-auto-install.xml`: minimal unattended veraPDF CLI installation template. The workflow substitutes only the ephemeral runner path; `scripts/verapdf_validation.py` owns the exact stable version, archive URL, and SHA-256.
- Use `npm ci`, never an unlocked install, in CI. The narrower `@daisy/ace-cli` package intentionally excludes the Ace HTTP server and Electron application.
- Fail the hosted build on high or critical npm advisories. Moderate upstream advisories remain visible in the log and require a threat-model review rather than an unsafe forced downgrade.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  P["Pinned manifests"] --> I["Ephemeral install"]
  K["veraPDF version, URL, and SHA-256"] --> I
  I --> G["Publication validation"]
  G --> X["Discard runner and diagnostic reports"]
```

### Component Diagram

```mermaid
flowchart TB
  R["requirements.txt"] --> P["Python verifier and tests"]
  N["package-lock.json"] --> A["DAISY Ace CLI"]
  X["verapdf-auto-install.xml"] --> V["veraPDF CLI"]
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant W as Workflow
  participant M as Dependency manifests
  participant T as Tool installers
  W->>M: Resolve exact versions
  M->>T: Verify package integrity
  T-->>W: Isolated validation tools
  W->>T: Force veraPDF ua1 on the canonical PDF
```

### State Machine

```mermaid
stateDiagram-v2
  [*] --> Locked
  Locked --> Installing: hashes and lockfile accepted
  Installing --> Rejected: integrity, engine, or advisory gate fails
  Installing --> Ready: exact dependency graph installed
  Rejected --> [*]
  Ready --> [*]
```

### Data Flow Diagram

```mermaid
flowchart LR
  P["requirements.txt and wheel hashes"] --> I["Python install"]
  N["package-lock.json integrity graph"] --> J["Node install"]
  I --> V["Verifier, schemas, Ruff"]
  J --> A["DAISY Ace"]
  V --> G["Publication CI"]
  A --> G
```
