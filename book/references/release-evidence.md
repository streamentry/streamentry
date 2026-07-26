# Internal release evidence

Checked: 2026-07-27

## Status

**Internally verified release candidate.** This record is valid only when read from the clean Git commit that contains it and when the artifact hashes below reproduce. The enclosing commit SHA is external metadata and is intentionally not embedded in this self-referential record.

- Candidate binding: **the enclosing clean Git commit plus the exact artifact hashes below**
- Independent Theravāda review: **NOT YET PERFORMED**
- Independent clinical-safety review: **NOT YET PERFORMED**
- Five-reader beginner cohort: **NOT YET PERFORMED**
- Human EPUB reader-app smoke test: **NOT YET PERFORMED**
- Comparative “top choice” evidence: **NOT ESTABLISHED**
- Public redistribution rights: **NOT DOCUMENTED; the public repository has no explicit license or rights statement**

## Artifact identity

| Item | Evidence |
|---|---|
| Immutable source SHA-256 | `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440` |
| PDF SHA-256 | `1eabab5e96d4efeeca81d95c37fbaf2e2731f30bcb3a3c5ef5c089bd4bd8daa6` |
| EPUB SHA-256 | `b38aaa386051f77dc811c46f2698a9797074093ef394db623e0aba8d421c2412` |
| PDF extent | 123 A5 pages |
| PDF file size | 1,021,520 bytes |
| EPUB navigation | 136 nested content entries plus 1 cover entry |
| EPUB archive size | 137,543 bytes |
| Publication credit | `CS Chánh Niệm + ChatGPT` |

Any content, theme, component, builder, or metadata change invalidates these hashes and requires this record to be regenerated.

## Build environment

| Tool | Version or setting |
|---|---|
| Canonical command | `python3 scripts/build-epub.py` |
| Typst | 0.15.0 |
| PDF standard requested | `ua-1` |
| Deterministic creation timestamp | `1785024000`, rendered as `2026-07-26T00:00:00Z` |
| Poppler | 26.06.0 |
| EPUBCheck | 5.3.0 |
| DAISY Ace | 1.4.6 |
| Ruff | 0.15.20 |
| JSON Schema validator | `jsonschema` 4.26.0 |

The builder acknowledged 176 allowlisted Typst HTML-export warnings and rejected unexpected warning classes. Two consecutive canonical builds after the final content and safety corrections were byte-identical for both PDF and EPUB.

## Verification results

| Gate | Result | Exact boundary |
|---|---|---|
| Immutable manuscript hash | Pass | Matches the recorded source contract. |
| Builder structural checks | Pass | XML, manifest, resources, navigation, internal anchors, manuscript hash, required content, ZIP order, timestamp, and uncompressed mimetype. |
| EPUBCheck 5.3.0 | Pass | 0 fatals, 0 errors, 0 warnings. |
| DAISY Ace 1.4.6 | Pass | No issues in `cover.xhtml`, `nav.xhtml`, `book.xhtml`, or `package.opf`. |
| Narrow-screen reflow | Pass | Headless viewport 320 × 568 CSS px, root font 24 px, dark mode on: root and body `scrollWidth` both 320; 0 overflow offenders. |
| Dark-mode automated contrast | Pass | Minimum tested text contrast was 7.443:1. |
| PDF metadata and tagging | Pass | `pdfinfo` reports Vietnamese title metadata, canonical author, tagged structure, 123 A5 pages, no JavaScript, and no suspects; embedded text extraction preserves the new Chapter 10 headings and clarification. |
| PDF visual QA | Pass internally | All 123 pages were inspected in contact sheets, with full-size checks on the expanded Chapter 10, the new Chapter 9 safety card, glossary additions, and closing pages. No clipping, overlap, truncated badges, accidental blanks, duplicates, or broken hierarchy were found. |
| Pilot schema and scorer | Pass internally | Both JSON Schema 2020-12 contracts meta-validate; 43 focused tests pass; Ruff and Python compilation pass. The scorer enforces the first five eligible completions among at most seven starts, terminal stopped-session sequencing, fixed stop reasons, distress-note erasure and vetoes, exact artifact and contract hashes, canonical-origin ancestry, recursive record discovery, reachable-history privacy, bounded likely-contact-data rejection, and strict retention bounds. |
| Source-integrity re-audit | Pass internally | Every used K01–K37, P01–P02, V01, and R01–R09 code resolves in the source map. Independent sub-agent adversarial reviews of doctrine, provenance, beginner clarity, code, and pilot privacy found no remaining material internal defect after corrections. These are internal reviews, not a named external Theravāda or clinical-safety sign-off. |

The PDF was compiled with Typst's PDF/UA-1 enforcement and exposes the expected metadata, but no independent PDF/UA validator such as veraPDF was available. Therefore this record does **not** claim independent PDF/UA conformance.

The pilot scorer proves consistency of the files it receives. Its canonical-origin and ancestry check uses the local `origin/main` ref and cannot prove that ref was freshly fetched. Its likely-contact-data detection is bounded and heuristic. It also cannot authenticate the moderator, independently timestamp preregistration, or prove that a never-recorded attempt was not omitted. Those stronger claims require a fresh public-history check, human privacy review, and the external append-only registry specified by the pilot protocol. Passing the scorer is therefore not evidence that a real beginner cohort has passed.

## Open release gates

1. Obtain the rights holder's explicit decision on copyright, licensing, source-text permissions, and allowed PDF/EPUB distribution. Do not infer a public redistribution grant from repository visibility.
2. Run the independent doctrinal review defined in `doctrinal-review-protocol.md` against the enclosing commit and both hashes, plus a separately scoped review of research and clinical-safety claims by a qualified reviewer.
3. Run one five-reader unassisted beginner cohort using `beginner-validation-protocol.md`; verify the enclosing commit against fresh public canonical history, preregister through an external append-only registry, enumerate every started attempt, and publish only aggregate evidence.
4. Run the required EPUB smoke test in a named standards-based reader at 150% text and dark mode. Automated Chromium reflow is useful evidence, not a substitute for this human reader-app gate.
5. Repeat failed reader gates with a fresh cohort after corrections.
6. Run `comparative-beginner-protocol.md` against the fixed named panel before using “top choice,” “best,” or “number one.”

Until those gates close, the defensible description is: **a sourced, internally audited, dual-format candidate designed for Vietnamese beginners.**
