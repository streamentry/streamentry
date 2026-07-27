# Internal release evidence

Checked: 2026-07-27

## Status

**Internally verified release candidate.** This record identifies the candidate by the exact artifact hashes below. Any terminal external evidence must name a frozen ancestor commit that contains those exact PDF and EPUB bytes; the evidence and an updated copy of this record may live in a later descendant commit without changing the tested artifact identity.

- Candidate binding: **a frozen artifact commit containing the exact PDF and EPUB bytes below, plus any later descendant evidence commit**
- Machine-readable external gate registry: [`external-release-gates.json`](external-release-gates.json)
- Public redistribution rights: **OPEN** — the materials inventory identifies the source manuscript, contributors, adapted passages, licensed fonts, and third-party works, but no competent authority has supplied a candidate-bound grant or rights decision.
- Independent Theravāda review: **OPEN** — no signed report for this candidate exists.
- Independent clinical-safety review: **OPEN** — no signed report for this candidate exists.
- Five-reader beginner cohort: **OPEN** — no scored external cohort exists.
- Human EPUB reader-app smoke test: **OPEN** — no counted human reader-app record exists.
- Comparative evidence: **OPEN** — no preregistered result supports a market comparison.

## Artifact identity

| Item | Evidence |
|---|---|
| Edition contract SHA-256 | `c3786a74678316e5f2a16e3f21c03ada40c347d717b5ee6f57df62cd24d8ebf9` |
| Immutable source SHA-256 | `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440` |
| PDF SHA-256 | `f4155379dddb918d0a3869526ac0cd119f23967d457ff94914c2a7042704051e` |
| EPUB SHA-256 | `a6ed0f40e584c35843a5d9c81b4f2decbd1cbe501c21a135f54577c87121a8a6` |
| PDF extent | 172 A5 pages |
| PDF file size | 1,424,473 bytes |
| EPUB navigation | 170 nested content entries plus 1 cover entry |
| EPUB archive size | 178,855 bytes |
| Publication credit | `CS Chánh Niệm + ChatGPT` |

Any content, theme, component, builder, metadata, or edition-contract change invalidates these hashes and requires this record to be regenerated.

## Build environment

| Tool | Version or setting |
|---|---|
| Canonical command | `python3 scripts/build-epub.py` |
| Typst | 0.15.0 |
| PDF standard requested | `ua-1` |
| Deterministic creation timestamp | `1785024000`, rendered as `2026-07-26T00:00:00Z` |
| Cover renderer | Typst 0.15.0 PNG export, page 1 at 160 ppi |
| Local PDF inspection | Poppler 26.06.0 |
| EPUBCheck | 5.3.0 |
| DAISY Ace | 1.4.6 |
| Ruff | 0.15.20 |
| JSON Schema validator | `jsonschema` 4.26.0 |

The builder acknowledged 197 allowlisted Typst HTML-export warnings and rejected unexpected warning classes. The print build names only the exact embedded families plus Inter, and release CI supplies the official Inter 4.0 files while disabling system fonts. Typst renders the EPUB cover directly instead of delegating rasterization to Poppler. Two consecutive canonical builds on the current macOS ARM64 host were byte-identical for both PDF and EPUB. Publication CI independently repeats the pinned build and rejects any byte drift. The platform is part of the reproducibility contract; structurally valid builds on another operating system are not assumed to have the same hashes. Hosted CI obtains Poppler from Homebrew only for inspection, never artifact generation; the verifier fails closed unless the required stable fields and every page's geometry are present.

## Verification results

| Gate | Result | Exact boundary |
|---|---|---|
| Immutable manuscript hash | Pass | Matches the recorded source contract. |
| Builder structural checks | Pass | Strict edition schema, XML, manifest, resources, contract-derived language and labels, accessibility metadata, navigation, internal anchors, manuscript hash, required content, ZIP order, timestamp, and uncompressed mimetype. |
| Release-evidence verifier | Pass | Exact edition-contract, artifact, and source hashes plus byte sizes; contract-derived title, credit, and language; PDF tagging, suspects, JavaScript, encryption, metadata, and every page's size and rotation; the EPUB's single active package, fixed manifest and cover-then-book spine, passive XHTML, metadata, unique resolved TOC targets, and separate content/cover counts reproduce from the committed files. |
| EPUBCheck 5.3.0 | Pass | 0 fatals, 0 errors, 0 warnings. |
| DAISY Ace 1.4.6 | Pass | The pinned CLI completed with `--exiterror2`; no issues were found in `cover.xhtml`, `nav.xhtml`, `book.xhtml`, or `package.opf`. Its cached headless Chrome required an unsandboxed local launch; Publication CI is configured to repeat the same pinned check in its isolated runner. |
| Narrow-screen reflow | Pass | Headless viewport 320 × 568 CSS px, root font 24 px, dark mode on: root and body `scrollWidth` both 320; no rendered box crossed the viewport. |
| Dark-mode automated contrast | Pass | Minimum tested text contrast was 7.443:1. |
| PDF metadata and tagging | Pass | `pdfinfo` reports Vietnamese title metadata, canonical author, tagged structure, 172 unrotated A5 pages, no encryption, no JavaScript, and no suspects; embedded text extraction preserves the safe first-sit anchor, canonical restart route, Chapter 5's stay–switch–act decision, complete noting loop and explicit P01 pain-instruction conflict, the action-first feeling-to-craving drill, Chapter 7's three attention modes, collision loop, immediate-protection rule and post-error repair loop, the immediate safety shortcut, the object/basis/means explanation of the first three fetters, the not-self/identity-view bridge and exact Pāli formula, the meditation case, the 3–5–4 map, and the expanded insight-map foundations, region transitions, practice tasks, and evidential limits. |
| PDF visual QA | Pass internally | All 172 pages were inspected in nine contact sheets. Full-size checks covered the rewritten Chapter 7 pages 54–61, including its attention modes, hazardous-task caution, four anchors, complete collision case, household-duty source block, threat boundary, repair loop, work case, and final retrieval card. An initial page split left the collision case's last two lines alone on the next page; the prose was tightened and the final render keeps the case together. Earlier full-size checks covered Chapter 5 pages 40–48, the rewritten Chapter 12 pages 115–136, Chapter 11 pages 102–106, the Chapter 10 opening model and meditation case, the frontmatter route, first-sit safety boxes, restart card, feeling-to-craving exercise, safety shortcut, and appendix lookup. The final render has no clipping, overlap, truncated badges, accidental blanks, duplicate glossary entry, missing glyphs, or broken hierarchy. |
| Pilot schema, scorer, release verifier, and review packet | Pass internally | Both JSON Schema 2020-12 contracts meta-validate; all 133 focused tests pass; Ruff, Python compilation, and `git diff --check` pass. The edition tests reject malformed or ambiguous contracts, bind HTML head metadata and frozen artifact paths to the supplied edition, and prove alternate-locale EPUB labels and XML escaping. The scorer enforces the first five eligible completions among at most seven starts, terminal stopped-session sequencing, fixed stop reasons, distress-note erasure and vetoes, exact artifact and contract hashes, canonical-origin ancestry, recursive record discovery, reachable-history privacy, bounded likely-contact-data rejection, and strict retention bounds. External gate evidence must declare one typed role, exactly one current PDF and EPUB digest field, and machine-visible generated-report results consistent with a passed registry status; contradictory report bodies fail closed. The deterministic coordinator packet binds all six work orders to the exact clean commit and artifact hashes, includes the frozen attainment source audit and rights materials inventory, validates its manifest and checksum index, rejects unsafe member paths, and explicitly leaves every external gate unchanged. |
| Source-integrity re-audit | Pass internally | Every used K01–K40, P01–P02, V01, and R01–R09 code resolves in the source map. The load-bearing Chapter 10–11 claims were checked at segment level against Pāli roots and English translations frozen at SuttaCentral `bilara-data` commit `3af91efb1099190c74998247177f8ba6a076b8c0`. Chapter 5 claims C71–C72 were checked against P01's Basic Exercises I–IV. Chapter 7 claim C73 was checked against K01's ordinary clear-comprehension material, K15 DN 31:27.1–34.36 on reciprocal household duties, K18 SN 55.7:4.1–10.7 on harmful bodily and verbal conduct, and K19 AN 6.63:33.3–33.5 on intention and action; the attention, collision, repair, work, and retrieval loops remain visibly editorial rather than attributed to those passages. The Chapter 12 expansion is bounded to P02's foreword, method, sections 1–17 and notes 40–45 plus V01 XX.105–129, XXI.128–131, and XXII.1–21; its foundation–observation–task–transition frame is explicitly editorial and rejects fixed-dose or single-event diagnosis. No contradiction was found, and every editorial synthesis or evidential limit remains labeled. Independent internal passes on onboarding friction, habit re-entry, pacing, prose, and acute-risk wording found no remaining material defect after corrections. These are internal reviews, not a named external Theravāda or clinical-safety sign-off. |

The PDF was compiled with Typst's PDF/UA-1 enforcement and exposes the expected metadata, but no independent PDF/UA validator such as veraPDF was available. Therefore this record does **not** claim independent PDF/UA conformance.

The pilot scorer proves consistency of the files it receives. Its canonical-origin and ancestry check uses the local `origin/main` ref and cannot prove that ref was freshly fetched. Its likely-contact-data detection is bounded and heuristic. It also cannot authenticate the moderator, independently timestamp preregistration, or prove that a never-recorded attempt was not omitted. Those stronger claims require a fresh public-history check, human privacy review, and the external append-only registry specified by the pilot protocol. Passing the scorer is therefore not evidence that a real beginner cohort has passed.

## Open release gates

Use [`external-release-packet.md`](external-release-packet.md) as the operational handoff. The JSON registry is the machine-readable status source; this list explains the work.

1. Obtain the rights holder's explicit decision under `rights-decision-template.md` on copyright, licensing, source-text permissions, and allowed PDF/EPUB distribution. Do not infer a public redistribution grant from repository visibility.
2. Run the independent doctrinal review defined in `doctrinal-review-protocol.md` and the separately scoped review defined in `clinical-safety-review-protocol.md` against the frozen artifact commit and both hashes.
3. Run one five-reader unassisted beginner cohort using `beginner-validation-protocol.md`; verify the frozen artifact commit against fresh public canonical history, preregister through an external append-only registry, enumerate every started attempt, and publish only aggregate evidence in a descendant commit.
4. Run the required EPUB smoke test in a named standards-based reader at 150% text and dark mode. Automated Chromium reflow is useful evidence, not a substitute for this human reader-app gate.
5. Repeat failed reader gates with a fresh cohort after corrections.
6. Freeze and externally register `comparative-beginner-protocol.md`, then run it against the named panel before making even the narrower named-panel first-use outperformance claim. The current draft does not authorize “top choice,” “best,” or “number one.”

Until those gates close, the defensible description is: **a sourced, internally audited, dual-format candidate designed for Vietnamese beginners.**
