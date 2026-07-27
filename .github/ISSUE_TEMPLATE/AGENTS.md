# Public Issue Forms

## Overview

These forms expose bounded public entry points without collecting private
contact details, medical histories, participant data, or unpublished review
evidence.

## Key Components

- `correction.yml`: actionable public correction reports tied to a location and
  current wording or behavior.
- `external-review-interest.yml`: public expressions of interest from expert
  reviewers or study coordinators. It is not a participant-recruitment form,
  reviewer authentication, review evidence, or a passed external gate.

## Diagrams

### Flowchart

```mermaid
flowchart LR
  V["Public visitor"] --> C{"Purpose"}
  C -->|Report a defect| R["Correction form"]
  C -->|Offer qualified review work| I["Review-interest form"]
  R --> T["Public triage"]
  I --> Q["Qualification, scope, conflict and artifact checks"]
  Q --> P["Formal external protocol"]
```

### Component Diagram

```mermaid
flowchart TB
  R["README"] --> C["correction.yml"]
  R --> I["external-review-interest.yml"]
  C --> E["Editorial correction process"]
  I --> X["External-release packet"]
  X --> G["External gate registry"]
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant O as Offeror
  participant F as Public form
  participant M as Maintainer
  participant P as Formal protocol
  O->>F: Select role and provide public evidence
  F->>M: Open public expression of interest
  M->>M: Verify scope, conflicts and qualifications
  M->>P: Issue candidate-bound work order
  P-->>M: Return separately bound evidence
```
