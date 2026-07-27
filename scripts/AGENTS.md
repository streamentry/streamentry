# EPUB Build Module

## Overview

This folder owns deterministic PDF and EPUB publication checks. It loads the
sole canonical edition and locale authority from `book/edition.json`, converts
the target-aware Typst HTML output into XML-conformant XHTML, generates
navigation and package metadata, renders the synchronized cover directly
through Typst, creates the EPUB container, verifies the release record against
the contract and both binaries, and fails loudly on structural defects.

## Key Components

- `edition_contract.py`: strict schema-v1 loader and immutable Python view of `book/edition.json`. It rejects duplicate or unknown keys, missing or malformed fields, unsafe paths, invalid identifiers and tags, and broken cross-field invariants.
- `edition_contract_validation.py`: small strict-JSON primitives for duplicate keys, exact object shapes, NFC single-line text, unique non-empty text arrays, absolute HTTPS identifier seeds, and one shared UTC release instant.
- `build-epub.py`: recompiles PDF and HTML, renders page 1 directly to the EPUB cover PNG, verifies the immutable manuscript hash, removes the duplicate HTML cover, promotes Typst body headings from h2-h6 to h1-h5, creates namespaced XHTML and nested navigation, and checks contract-bound HTML head metadata, semantics, accessibility metadata, manifest resources, labelled content links, resolved local fragments, absolute HTTPS external URLs, distinct labels for different external destinations, resolved visible-title bindings and bounded `note`/`group` roles for repeated cards, warning classes, fixed ZIP timestamps, entry order, and uncompressed mimetype.
- `verify_release.py`: orchestrates the release contract and compares the immutable source plus exact binary identities.
- `release_evidence.py`: parses only the visible artifact table and anchors the immutable source hash and publication credit to the edition supplied by the release orchestrator.
- `release_pdf.py`: verifies PDF metadata, tagging, security flags, file size, and every page's A5 geometry and rotation.
- `verapdf_validation.py`: owns the stable veraPDF Greenfield version, archived installer URL, SHA-256, forced PDF/UA-1 profile, strict report parser, and subprocess boundary.
- `verify-verapdf.py`: candidate-aware CLI that runs the pinned executable, binds its JSON report to the canonical PDF, and writes only an ignored diagnostic report.
- `release_epub.py`: verifies the active package, exact manifest and spine, passive XHTML, metadata, resolved unique navigation, labelled content links, resolved local fragments, distinct external-destination labels, safe external-link schemes, and content/cover counts.
- `external_release_gates.py`: verifies the schema-v3 registry, protocol fingerprints, six external-gate states, gate-specific required evidence roles, contract-derived artifact paths, ancestor-plus-exact-artifact candidate binding, cohort/report bindings, release-evidence status agreement, and claims derived from passed gates.
- `external_release_gate_files.py`: contains the fail-closed JSON, repository-path, file-fingerprint, local-link, evidence-status, exact evidence-role, mandatory `Completed`, public-confirmation and scope-limit fields, public contact-data rejection, exact-once PDF/EPUB digest, cohort/manifest, and counted-record validators used by the external gate orchestrator.
- `rights_inventory_contract.py`: parses the inventory's single schema-v1 source/PDF/EPUB identity and rejects stale, duplicate, or malformed release bindings.
- `rights_decision_contract.py`: fail-closed parser for the public rights summary. It binds the current materials inventory and immutable source, enumerates distribution scopes, and rejects a passed record with unauthorized PDF/EPUB, unresolved contributors, unresolved third-party materials, or any open rights item. It cannot authenticate the signer or decide legal validity.
- `build-external-review-packet.py`: clean-checkout CLI for the ignored coordinator ZIP.
- `external_review_packet.py`: verifies the clean commit, exact committed source bytes, release candidate, edition contract, and gate registry before collection.
- `external_review_packet_content.py`: canonical gate order, assignment text, guide, manifest, immutable packet data structures, and the complete beginner-pilot runtime path set. The packet must let a coordinator run the frozen preparation CLI and scorer without fetching code from the network.
- `external_review_packet_archive.py`: deterministic ZIP writer and checksum, manifest, timestamp, assignment, and candidate validator.
- `beginner_pilot_contract.py`: fixed task ids, criteria, thresholds, allowed fields, cohort rules, and the exact ten-file scoring contract. The insight-map criterion points to Chapter 12 and requires the four-level phenomenon/glimpse/region/attainment distinction. The fetter task requires both the scenario-level rubric and rejection of monastic-only or male-only restrictions without treating canonical examples as a guarantee. Session fields bind written prompt display, rereading permission and the absence of moderator follow-up cues so the cohort measures open-book comprehension rather than one-shot prompt memory.
- `beginner_pilot_validation.py`: strict JSON, schema, consent, eligibility, task-state, fixed stop-reason, bounded contact-data detection, and retention validation.
- `beginner_pilot_artifact.py`: verifies hashes and page count against real files and committed Git blobs, plus a bounded EPUB container check.
- `beginner_pilot_manifest.py`: loads the only authoritative manifest, rejects direct or nested record additions and reachable Git-history exposure, enforces chronological first-five selection among at most seven starts, verifies canonical origin/main ancestry, and binds the running scorer to the committed contract.
- `beginner_pilot.py`: reusable scoring rules for one validated five-reader novice cohort.
- `score-beginner-pilot.py`: manifest-only CLI that applies fixed comprehension, EPUB, completeness, and distress-veto gates. `--output` emits an aggregate report bound to one cohort, one manifest hash, and five counted-record hashes; `--epub-evidence-output` emits a separate reader-app report bound to the same cohort and manifest plus one of those records. Neither output proves human identity or external custody.
- The pilot runtime requires Python's `jsonschema` package. A local manifest cannot independently prove its asserted registration time or that the moderator did not omit the terminal attempt; stronger custody needs an external append-only timestamped registry.
- Keep the OPF `dcterms:modified` value fixed within a release for reproducibility, but advance it when the published content changes to a new release date.
- `build/epub/`: ignored intermediate output.
- `dist/huong-den-nhap-luu.epub`: final artifact.

Do not reintroduce title, author, language, labels, accessibility copy, output
names, source identity, or release timestamps as independent Python constants.
Consumers may expose compatibility aliases only when their values come directly
from the loaded contract. A future locale requires a distinct edition identity
and separate rights, review, novice, and reader-app evidence; Vietnamese results
do not transfer.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  D["book/edition.json"] --> L["Strict edition loader"]
  D --> Y["book/edition.typ"]
  Y --> T
  L --> N
  L --> E
  L --> W
  T["book/main.typ"] --> P["Fresh PDF"]
  P --> U1["Pinned veraPDF PDF/UA-1 gate"]
  T --> C["Typst page-1 PNG"]
  T --> H["Semantic HTML"]
  H --> X["Cover removal, h1-h5 outline, and bodymatter"]
  X --> N["Nested semantic navigation"]
  N --> E["EPUB package"]
  C --> E
  E --> V["Builder structural validation"]
  U1 --> V
  E --> W["Separate release-evidence verifier"]
  W --> Q["Typed external gate registry"]
  RI["Artifact-bound rights inventory"] --> RD["Rights scope summary"]
  RD --> Q
  A["Frozen attainment source audit"] --> Q
  Q --> K["Candidate-bound external-review packet"]
  F["Frozen manifest and ordered attempts"] --> S["Deterministic cohort scorer"]
  S --> G["Aggregate and reader-app reports"]
```

### Component Diagram

```mermaid
flowchart TB
  D["Canonical edition contract"] --> L["Strict loader"]
  L --> B["Builder"]
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
  Q["External gate registry"] --> E["Candidate-bound public evidence"]
  R --> A["Aggregate report"]
  G --> A
  S --> E["Reader-app report"]
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant U as Editor
  participant D as Edition loader
  participant T as Typst
  participant B as EPUB builder
  participant V as Validator
  participant S as Pilot scorer
  U->>B: Run build
  B->>D: Load and validate edition.json
  D-->>B: Immutable contract or exact error
  B->>T: Compile PDF and semantic HTML
  T-->>B: Current content and cover
  B->>B: Normalize namespaces, bodymatter, outline, and OPF
  B->>V: Validate archive and links
  V-->>U: Verified EPUB or exact failure
  U->>V: Verify protocol hashes and external gate claims
  V->>V: Reject incomplete or stale rights scope evidence
  U->>S: Score one manifest with all ordered attempts
  S-->>U: Aggregate and reader-app reports or exact invalid-data error
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
  Verified --> ExternallyGated: candidate-bound public evidence
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
  D["book/edition.json"] --> L["Strict Python loader"]
  L --> H
  L --> P
  L --> Z
  T["Typst source"] --> H["HTML"]
  T --> P["PDF"]
  H --> X["namespaced book.xhtml"]
  X --> N["h1-h5 outline"]
  T --> I["Typst page-1 cover.png"]
  X --> Z["EPUB"]
  N --> Z
  I --> Z
  R["Manifest and pseudonymous attempt JSON"] --> C["Cohort scorer"]
  C --> A["Aggregate and reader-app reports"]
  A --> G["External gate registry"]
```
