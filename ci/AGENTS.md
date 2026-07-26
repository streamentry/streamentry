# Publication CI Dependencies

## Overview

This folder contains only pinned dependency contracts for the ephemeral publication validator. It is not a runtime application and must not contain reader data, credentials, or generated reports.

## Key Components

- `requirements.txt`: exact Python versions and reviewed Linux wheel hashes for JSON Schema validation and Ruff.
- `package.json` and `package-lock.json`: DAISY Ace CLI 1.4.6 and its integrity-locked dependency graph.
- Use `npm ci`, never an unlocked install, in CI. The narrower `@daisy/ace-cli` package intentionally excludes the Ace HTTP server and Electron application.
- Fail the hosted build on high or critical npm advisories. Moderate upstream advisories remain visible in the log and require a threat-model review rather than an unsafe forced downgrade.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  P["Pinned manifests"] --> I["Ephemeral install"]
  I --> V["Publication validation"]
  V --> X["Discard runner and reports"]
```

### Component Diagram

```mermaid
flowchart TB
  R["requirements.txt"] --> P["Python verifier and tests"]
  N["package-lock.json"] --> A["DAISY Ace CLI"]
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
