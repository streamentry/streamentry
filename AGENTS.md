# Streamentry Typst Book

## Overview

This workspace turns `con-duong-niem-xu-mahasi-hop-nhat.md` into an A5 Vietnamese practice handbook. The source Markdown is preserved unchanged. The publication title is *Hướng Đến Nhập Lưu*, not a promise of attainment.

Accuracy has priority over continuity with the source. Keep early Pāli discourses, later Theravāda exegesis, the *Visuddhimagga*, Mahāsi instructions, and modern editorial or safety advice visibly separate.

## Key Components

- `con-duong-niem-xu-mahasi-hop-nhat.md`: immutable source manuscript. Recorded SHA-256: `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440`.
- `README.md`: public reader gateway. Put the Vietnamese reader's download choice, intended use, reading route, safety boundary, source model, correction path, candidate status, and missing-rights warning before contributor build details. Never let public file access imply a redistribution license or external validation.
- `book/edition.json`: sole canonical edition and locale authority for publication identity, output names, source binding, cover copy, interface labels, accessibility copy, semantic smoke text, and validation scope.
- `book/edition.typ`: thin Typst leaf that exposes `edition.json`; it must not introduce independent metadata or locale policy.
- `scripts/edition_contract.py`: strict schema-v1 Python loader used by build and verification. Unknown, missing, malformed, unsafe, or internally inconsistent values fail closed.
- `scripts/edition_contract_validation.py`: focused duplicate-key, exact-object, Unicode, and string-array validation primitives for the loader.
- `book/main.typ`: only Typst content entry point for both paged and HTML targets.
- `book/theme.typ`: A5 print rules plus reflowable HTML CSS selected through `target()`. Use left binding with mirrored 22 mm inside and 14 mm outside margins for the perfect-bound edition.
- `book/components.typ`: target-aware source badges, chapter openers, practice cards, cautions, and reference blocks. In semantic HTML, every repeated titled card must bind its visible title with a unique deterministic `aria-labelledby`; use `note` for practice/caution callouts and `group` for non-landmark collections. Keep source badges above, not inline with, cited prose; preserve a quiet gap below provenance blocks.
- `book/chapters/`: editorial chapters.
- `book/chapters/01-bay-ngay.typ`: safe first-sit route, seven-day start, explicitly editorial days 8–30 bridge, and the canonical restart path after ordinary interruption.
- `book/chapters/04-duyen-khoi.typ`: action-first feeling-to-craving drill followed by the source-bounded full twelve-link map; never collapse the latter into the former.
- `book/chapters/07-doi-song-tai-gia.typ`: ordinary-life transfer through task-first attention, brief response checks, formal-practice boundaries, an immediate collision loop, and a post-error repair loop. Their counts and timings are editorial; immediate protection and essential duties outrank introspection.
- `book/chapters/10-nhap-luu.typ`: focused beginner explanation of the first three fetters through separate source claims, a visibly editorial object/basis/means model, ordinary-life and meditation cases, and the canonical criteria surrounding Stream-entry.
- `book/chapters/11-ha-phan-va-sa-mon-qua.typ`: separate 3–5–4 map for the five lower fetters, four fruits, four pairs/eight persons, and DN 2.
- `book/chapters/12-ban-do-tue.typ`: later-reference insight map. Define the map before taxonomy, separate object/knowing/reaction/conclusion, and preserve the direct beginner route to the four-region explanation. Keep a navigable subheading and the six-question explanation (foundation, changed knowing, possible experience, practice, insufficient lookalikes, transition) consistent across stages 1–11, plus the one-object walkthrough that makes the changing way of knowing concrete. Explain stages 12–17 by system function and evidential limit, not as separately reproducible feelings. Never turn its editorial teaching aids into a self-diagnostic ladder or stage-production recipe.
- `book/appendices/`: reusable practice tools.
- `book/appendices/e-ban-do-quyet-dinh.typ`: original safety-first retrieval map for stay, switch, act, repair, reduce and stop decisions; its editorial synthesis is C74 and its current Vietnamese emergency-number route is bounded by C75–C76.
- `book/references/claim-ledger.md`: claim-to-source audit trail.
- `book/references/attainment-source-audit.md`: immutable segment-level audit for the attainment claims in Chapters 10–11.
- `book/references/editorial-depth-audit.md`: chapter-by-chapter test for harmful compression.
- `book/references/publish-readiness-audit.md`: adapted 80-item publication scorecard.
- `book/references/release-evidence.md`: exact candidate hashes, tool versions, verification scope, and open external gates.
- `book/references/edition-contract.md`: field ownership, canonical Vietnamese line, future-locale rules, build flow, and falsifiable limits of the edition contract.
- `book/references/external-release-packet.md`: single operational handoff for rights, expert review, novice testing, human EPUB evidence, and bounded comparison.
- `book/references/external-release-gates.json`: machine-readable external-gate, typed-evidence, and permitted-claims registry.
- `book/references/rights-decision-template.md`: authority, asset, format, channel, commercial-scope, and third-party-rights decision record with a mandatory machine-readable public summary.
- `book/references/rights-materials-inventory.md`: decision-support inventory for manuscript, contributor, adapted passage, third-party work, font, source-code, and format rights; facts only, not clearance.
- `book/references/clinical-safety-review-protocol.md`: independent clinical and research-safety reviewer contract.
- `book/references/beginner-validation-protocol.md`: external novice and reader-app acceptance gates.
- `book/references/comparative-beginner-protocol.md`: bounded comparison protocol for a fixed Vietnamese beginner panel.
- `book/references/beginner-pilot-cohort-manifest.schema.json`: frozen cohort contract and ordered attempt ledger.
- `book/references/beginner-pilot-record.schema.json`: structured, privacy-bounded novice-attempt record.
- `book/references/doctrinal-review-protocol.md`: operational contract for independent Theravāda review.
- `dist/huong-den-nhap-luu.pdf`: current internally verified print candidate.
- `scripts/build-epub.py`: deterministic EPUB 3 packaging and structural validation, including labelled content links, resolved local fragments, absolute HTTPS external sources, distinct labels for different external destinations, and resolved visible-title bindings for repeated cards.
- `scripts/verify_release.py`: small release-verification orchestrator.
- `scripts/build-external-review-packet.py`: clean-checkout CLI that creates one deterministic, candidate-bound ZIP for all six external work orders.
- `scripts/external_review_packet.py`, `scripts/external_review_packet_content.py`, and `scripts/external_review_packet_archive.py`: committed-source collection, canonical packet content, deterministic ZIP writing, and self-validation.
- `scripts/release_evidence.py`, `scripts/release_pdf.py`, and `scripts/release_epub.py`: fail-closed evidence-table, per-page PDF, and fixed-publication EPUB contracts. The EPUB verifier independently rejects broken or unlabelled content links and unsafe external-link schemes.
- `.github/workflows/publication-ci.yml`: read-only publication CI with SHA-pinned actions and checksum-pinned downloaded tools for deterministic rebuilds, tests, EPUBCheck, DAISY Ace, and forced-profile veraPDF PDF/UA-1 validation.
- `scripts/verapdf_validation.py` and `scripts/verify-verapdf.py`: pinned veraPDF installer contract plus fail-closed JSON, version, artifact, profile, rule, check, and batch validation.
- `ci/`: pinned Python and Node dependency contracts used only by publication CI.
- `scripts/score-beginner-pilot.py`: manifest-only first-five gate scoring with artifact and contract binding.
- `tests/test_edition_contract.py`: regression coverage for strict loading and cross-field invariants.
- `tests/test_epub_edition_contract.py` and `tests/test_release_identity.py`: alternate-locale XML/label escaping plus PDF/EPUB identity-drift regressions.
- `dist/huong-den-nhap-luu.epub`: current internally verified reflowable candidate.

`book/edition.json` is the only canonical source for the publication credit and
all other edition or locale values. The current Vietnamese contract declares
`CS Chánh Niệm + ChatGPT`; consume it through `book/edition.typ` or
`scripts/edition_contract.py` rather than copying it into production code.
README may describe the current value, but it is not an authority. It must read
edition identity from the contract, artifact identity from release evidence,
and external status from the gate registry rather than copying drift-prone
counts or claiming that public access grants redistribution rights.

Schema v1 has one canonical Vietnamese build line. A future locale is a separate
publication candidate with its own identity, localized labels, rights decision,
source and doctrinal review, safety review where applicable, novice
comprehension evidence, and reader-app evidence. Passing the Vietnamese
internal or external gates never transfers those results to a translation.

Beginner readability is a publication contract, not a style preference. Define technical terms at first use, connect each conceptual section to the prior one, orient and synthesize dense lists, and keep appendices usable when opened directly. Close every explanatory chapter with either a short closed-book retrieval card or an explicit real-world decision block; test the central distinction and next action, not terminology recall or attainment status. In safety and decision passages, give each observable trigger or action its own list item. Treat sentence length as a review signal, not an automatic defect; preserve a long paragraph when its source-bound explanation is coherent and each inference remains visible. The first-sit route must expose its local stop conditions and label lookup without forcing a full safety-chapter detour; the full safety chapter remains mandatory before intensification. Keep one canonical restart protocol in Chapter 1 and link to it briefly elsewhere. Internal editorial review may mark these gates complete, but only `book/references/beginner-validation-protocol.md` can support a claim of novice validation.

For running the novice test, start with `book/references/beginner-reader-kit.md` and use it together with the protocol. Freeze the artifacts and ten-file scoring contract before attempt one, enumerate every started attempt in one authoritative manifest, and count only the first five completed eligible attempts among at most seven starts. Raw records stay under ignored `build/beginner-pilot/`; only the privacy-coarsened aggregate and reader-app reports are publishable. A local manifest cannot independently prove its registration time or terminal-attempt completeness; use an external append-only registry for that stronger claim.

For external release work, start with `book/references/external-release-packet.md`. Treat schema-v3 `external-release-gates.json` as the status source and let `scripts/verify_release.py` check protocol hashes, required gate-specific evidence roles, path reuse, role/header agreement, mandatory completion, public-confirmation and scope-limit fields, exact-once PDF and EPUB digest fields, candidate binding, cohort/report bindings, cross-document status, public contact-data rejection, and permitted claim enums. A passed `rights_decision` must also bind the current materials-inventory and immutable-source hashes, authorize both PDF and EPUB, state source/print/derivative scopes, territory, language, term, attribution and notices, and resolve contributor and third-party status with no open rights item. The frozen candidate commit may precede the evidence commit, but it must be an ancestor of it and contain the exact recorded PDF and EPUB bytes; `release-evidence.md` and public evidence may be committed later. Machine verification cannot establish a signer's identity or authority, the legal validity of a grant, a reviewer's competence, participant identity, custody completeness, or the honesty of a study. Keep every gate open until that human evidence exists.

Run `python3 scripts/build-external-review-packet.py` only from a clean
checkout when issuing work orders. The ignored ZIP binds its protocol copies
and assignment sheets to the exact commit and artifact hashes. Packet creation
is logistics, not external evidence, and never changes a gate status.

When discussing attainment, use *the first three fetters*, not an invented standalone canonical list called “three lower fetters.” Keep that subset distinct from the full five lower fetters, the four fruits, and DN 2's broader discourse title. Chapter 10 explains the subset through the object, verified-basis, and means frame, explicitly labelled as editorial rather than a canonical 1–2–3 sequence. Chapter 11 supplies the wider classification.

Build from the workspace root:

```sh
python3 scripts/build-epub.py
python3 scripts/verify_release.py
python3 scripts/build-external-review-packet.py
```

Under the pinned macOS 15 ARM64 publication CI tool and font environment, the canonical builder emits a byte-reproducible PDF/UA-1 candidate and synchronized reflowable EPUB. The platform is part of the reproducibility contract because official Typst builds on different operating systems need not emit identical bytes. Publication CI disables system-font discovery and supplies the official checksum-pinned Inter 4.0 files so a missing or substituted local font cannot silently change the release. Repeated visual cards must expose their visible titles as machine-readable names without inflating the heading outline or landmark list. veraPDF must be the exact version, URL, and checksum declared by `scripts/verapdf_validation.py`, must be forced to `ua1`, and must return a normal, compliant, zero-failure report bound to the current PDF. Treat veraPDF, EPUBCheck, DAISY Ace, and browser accessibility-tree inspection as internal machine evidence; actual assistive-technology and reader-app use remain external gates.

Do not impersonate the Buddha, fabricate quotations, or turn a retreat schedule, noting technique, cessation experience, or teacher verdict into a canonical guarantee of stream-entry.

## Diagrams (Mermaid)

### Flowchart

```mermaid
flowchart LR
  A["Source manuscript"] --> B["Doctrinal claim audit"]
  B --> C["Six-class provenance"]
  C --> D["Chapter modules, including safe start and restart"]
  D --> E["Typst composition"]
  E --> F["PDF render, grayscale, and print QA"]
  E --> H["Semantic HTML target"]
  H --> I["EPUB packaging and validation"]
  F --> G["Print handbook"]
  I --> J["Reflowable handbook"]
  G --> K["Beginner and expert validation"]
  J --> K
```

### Component Diagram

```mermaid
flowchart TB
  D["book/edition.json"] --> Y["book/edition.typ"]
  D --> Z["scripts/edition_contract.py"]
  Y --> M["book/main.typ"]
  M["book/main.typ"] --> T["theme.typ"]
  M --> C["components.typ"]
  M --> H["chapters/*.typ"]
  M --> A["appendices/*.typ"]
  M --> E["Semantic HTML"]
  E --> P["scripts/build-epub.py"]
  Z --> P
  Z --> Q
  P --> U["EPUB 3"]
  R0["README reader gateway"] --> U
  R0 --> V["Tracked PDF"]
  R0 --> X
  M --> Q["Quality audits"]
  N["Frozen manifest and attempt records"] --> G["Deterministic dual-output pilot scorer"]
  G --> Q
  X["External gate registry"] --> Q
  R["Role-labelled rights and review evidence"] --> RC["Rights scope contract"]
  RC --> X
  Q --> W["Deterministic external-review packet"]
  H --> C
  A --> C
  H -. "claim codes" .-> L["references/claim-ledger.md"]
  L -. "source URLs" .-> S["Primary and authoritative editions"]
```

### Sequence Diagram

```mermaid
sequenceDiagram
  participant E as Editor
  participant D as Edition contract
  participant L as Claim ledger
  participant T as Typst
  participant Q as PDF QA
  participant P as EPUB packager
  participant R as External reviewers
  participant S as Pilot scorer
  E->>D: Change one schema-v1 edition or locale value
  D-->>E: Strict loader accepts it or names the defect
  E->>L: Verify doctrine, speaker, edition, and source tier
  L-->>E: Return source code and caveat
  E->>T: Compose source-labelled chapter
  T-->>Q: Compile A5 PDF
  T->>P: Compile semantic HTML
  P-->>E: Validate EPUB container, XML, manifest, and navigation
  Q-->>E: Report overflow, page rhythm, and text defects
  E->>R: Run novice comprehension and scoped expert review
  R->>S: Submit frozen manifest and all ordered attempts
  S-->>E: Return aggregate and reader-app evidence
  R-->>E: Return scoped expert findings
  E->>T: Correct and recompile
```

### State Machine

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Audited: claims classified and sourced
  Audited --> Composed: Typst modules assembled
  Composed --> Rendered: PDF and EPUB compile
  Rendered --> Audited: defect or unsupported claim found
  Rendered --> InternallyVerified: structural and visual QA pass
  InternallyVerified --> ReleasePacketReady: role-specific work orders frozen
  ReleasePacketReady --> ExternallyValidated: rights, novice and expert gates pass
  InternallyVerified --> PilotFailed: novice gate fails
  PilotFailed --> Audited: correct wording and recruit a fresh cohort
  InternallyVerified --> [*]: candidate only
  ExternallyValidated --> [*]
```

### Data Flow Diagram

```mermaid
flowchart LR
  ED["Canonical edition.json"] --> ET["Typst edition leaf"]
  ED --> EL["Strict Python loader"]
  SM["Source manuscript"] --> EW["Editorial rewrite"]
  PS["Primary texts and editions"] --> CL["Claim ledger"]
  CL --> EW
  EW --> TM["Typst chapter and appendix modules"]
  ET --> TM
  TM --> TC["Typst compiler"]
  TC --> PDF["A5 PDF"]
  TM --> HTML["Semantic HTML"]
  HTML --> EP["EPUB 3 packager"]
  EL --> EP
  EP --> EPUB["Reflowable EPUB"]
  PDF --> QA["Text, structure, and visual QA"]
  EPUB --> V["XML, manifest, navigation, and reader QA"]
  PDF --> B["Beginner validation"]
  EPUB --> B
  B --> R["Frozen manifest and pseudonymous attempt records"]
  R --> SC["Deterministic gate scorer"]
  SC --> AE["Aggregate and reader-app evidence"]
  AE --> X["Typed external gate registry"]
  ER["Role-labelled rights and signed reviews"] --> X
  QA -. "corrections" .-> EW
  V -. "corrections" .-> EW
  B -. "comprehension failures" .-> EW
```
