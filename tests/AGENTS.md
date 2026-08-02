# Publication Verification Tests

## Overview

This folder owns focused regression tests for the canonical edition loader,
builder, pilot scorer, and release gate. Release-verifier tests are split by
evidence, PDF, EPUB, and end-to-end integration so each module stays small and
each failure names one contract.

## Key Components

- `test_edition_contract.py`: schema-v1 strict-loading tests for duplicate, unknown, missing, malformed, unsafe, out-of-range, and cross-field-inconsistent edition data, plus the tracked Vietnamese contract.
- `test_epub_edition_contract.py`: alternate-locale HTML head metadata, navigation, cover, OPF, language, accessibility, XML-escaping, content-link, and repeated-card visible-title binding contract proof with no Vietnamese-label fallback.
- `test_release_identity.py`: table-driven PDF and EPUB title, credit, and language drift rejection against the loaded contract.
- `test_readme_gateway.py`: reader-first ordering, contract-derived download identity, relative-link integrity, missing-rights and open-gate boundaries, and rejection of drift-prone artifact counts in the public README.
- `test_editorial_policy.py`: public-policy, README and standalone-book reader surfaces, structured correction and external-review-interest forms, privacy boundaries, participant-intake exclusion, and honest T02/T05 audit regressions.
- `test_chapter_12_contract.py`: all seventeen stage headings, the six-part stages 1–11 explanation, the front-loaded four-level conclusion distinction, three-axis/non-numeric maturation model, worked hypothesis interview, one-object walkthrough, and late-sequence evidential limits.
- `test_chapter_10_contract.py`: the direct “who can attain?” answer, DN 16's monastic/lay and male/female examples, and the possibility-versus-guarantee boundary.
- `test_source_code_legend.py`: first-read expansion of DN/MN/SN/AN/Ud, separation of canonical locations from the book's K/P/V/R traceability codes, and the linked durable legend in the source map.
- `test_reader_trust_statement.py`: confirms that the removed frontmatter trust block does not reappear while the first-reading route remains intact; repository-level policy and Chapter 99 retain the public correction and evidence boundaries.
- Beginner-pilot runtime and CLI tests require written visible prompts, allowed rereading, no moderator follow-up cues, no pre-answer rubric exposure, and a scorer-level cohort rejection when either delivery or blinding is violated.
- `release_verifier_fixtures.py`: shared synthetic Markdown, PDFInfo, OPF, XHTML, and EPUB fixtures.
- `test_release_evidence.py`: visible-table parsing plus immutable hash and canonical-credit anchors against the explicitly supplied edition.
- `test_release_pdf.py`: metadata, encryption, all-page size, and rotation regressions.
- `test_verapdf_validation.py`: pinned component-version, exact artifact, forced PDF/UA-1 profile, compliance, zero-failure, and batch-summary report regressions.
- `test_release_epub.py`: active-rootfile, fixed manifest/spine, passive XHTML, TOC-target, broken-fragment, unlabelled-link, ambiguous external-label, and unsafe-scheme regressions.
- `test_release_verifier.py`: integration check against the tracked release candidate.
- `test_external_release_gates.py`: schema-v3 protocol-fingerprint, status, gate-specific evidence-role, contract-derived artifact-path, ancestor/exact-byte candidate binding, mandatory public fields, rights-scope and inventory binding, contact-data rejection, cohort/report hashes, path-reuse, and permitted-claim regressions.
- `test_rights_inventory_contract.py`: exact schema-v1 source/PDF/EPUB binding plus stale, duplicate, and malformed inventory regressions.
- `test_rights_decision_contract.py`: direct passed/failed rights-summary contract plus stale binding, unauthorized format, unresolved contributor/third-party, open-item, and contradictory-decision regressions.
- `rights_decision_fixtures.py`: one shared complete rights-summary fixture for direct and external-gate integration tests.
- `test_external_review_packet.py`: deterministic ZIP, candidate and assignment binding, three-step role startup, exact evidence-role outputs, required attainment-audit and rights-inventory handoffs, participant-only rubric warnings, Vietnamese coordinator guidance, explicit non-evidence boundary, checksum tamper detection, duplicate-path rejection, clean-worktree enforcement, and repository-path containment.
- Existing `test_beginner_pilot*.py` files retain the novice-cohort privacy and scoring contract, including dual scorer output: five counted hashes in the aggregate report and one matching hash in the `--epub-evidence-output` reader-app report.
- When an intentional chapter or layout change alters the tracked PDF extent, update the integration expectation only after rebuilding both artifacts and updating `release-evidence.md`; do not change synthetic parser fixtures merely to mirror the current book.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  C["Edition contract fixtures"] --> D["Strict loader tests"]
  F["Synthetic fixtures"] --> E["Evidence tests"]
  F --> P["PDF tests"]
  F --> U["EPUB tests"]
  F --> X["External gate tests"]
  F --> K["External packet tests"]
  R["Tracked release"] --> I["Integration test"]
  W["README gateway"] --> J["Reader-surface contract test"]
  H["Policy and correction form"] --> N["Editorial-policy contract test"]
  B["Chapter 12"] --> M["Insight-map contract test"]
  N --> G
  M --> G
  E --> G["Full test gate"]
  D --> G
  P --> G
  U --> G
  I --> G
```

### Component Diagram

```mermaid
flowchart TB
  C["book/edition.json"] --> D["test_edition_contract.py"]
  D --> L["edition_contract.py"]
  X["release_verifier_fixtures.py"] --> E["test_release_evidence.py"]
  X --> P["test_release_pdf.py"]
  X --> U["test_release_epub.py"]
  V["verify_release.py"] --> I["test_release_verifier.py"]
  W["README, edition, gates, evidence"] --> J["test_readme_gateway.py"]
  H["EDITORIAL_POLICY.md and correction.yml"] --> N["test_editorial_policy.py"]
  B["12-ban-do-tue.typ"] --> M["test_chapter_12_contract.py"]
  G["external_release_gates.py"] --> Q["role and gate-contract tests"]
  RI["rights_inventory_contract.py"] --> Q
  R["rights_decision_contract.py"] --> Q
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant T as Test runner
  participant C as Edition contract
  participant F as Fixtures
  participant M as Release modules
  participant A as Tracked artifacts
  T->>C: Mutate one schema or cross-field condition
  C-->>T: Exact rejection or immutable contract
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
  C["Edition JSON variants"] --> L["Strict edition loader"]
  M["Markdown fixture"] --> E["Evidence parser"]
  P["pdfinfo fixtures"] --> D["PDF contract"]
  X["EPUB fixtures"] --> U["EPUB contract"]
  J["veraPDF JSON fixture"] --> H["PDF/UA-1 report contract"]
  A["dist artifacts"] --> V["Release orchestrator"]
  E --> R["Test result"]
  D --> R
  U --> R
  H --> R
  V --> R
  G["Gate registry"] --> R
  L --> R
```
