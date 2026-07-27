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
| Edition contract SHA-256 | `a4144f260984e363d58b2eaa83c8cb6efcc3ddfc3f5ff7a8702232912b7b52f6` |
| Immutable source SHA-256 | `ad7a886895cf8cd29b369fda89de5665c96907d990f95dba8f028336bcbbd440` |
| PDF SHA-256 | `6a3ef16d2b317940e1c4ff1c60079ca8cdacfce362f915f02e212e5a0a3e79cd` |
| EPUB SHA-256 | `cde454048f64d185ba8ccc7c5183d0a582c2d9d6c496b5437b6e2d0baece78dd` |
| PDF extent | 197 A5 pages |
| PDF file size | 1,646,380 bytes |
| EPUB navigation | 203 nested content entries plus 1 cover entry |
| EPUB archive size | 200,744 bytes |
| Publication credit | `CS Chánh Niệm + ChatGPT` |

Any content, theme, component, builder, metadata, or edition-contract change invalidates these hashes and requires this record to be regenerated.

## Build environment

| Tool | Version or setting |
|---|---|
| Canonical command | `python3 scripts/build-epub.py` |
| Typst | 0.15.0 |
| PDF standard requested | `ua-1` |
| Deterministic creation timestamp | `1785110400`, rendered as `2026-07-27T00:00:00Z` |
| Cover renderer | Typst 0.15.0 PNG export, page 1 at 160 ppi |
| Local PDF inspection | Poppler 26.06.0 |
| PDF/UA validator | veraPDF Greenfield 1.30.2, forced `ua1` profile |
| EPUBCheck | 5.3.0 |
| DAISY Ace | 1.4.6 |
| Ruff | 0.15.20 |
| JSON Schema validator | `jsonschema` 4.26.0 |

The builder acknowledged 205 allowlisted Typst HTML-export warnings and rejected unexpected warning classes. The print build names only the exact embedded families plus Inter, and release CI supplies the official Inter 4.0 files while disabling system fonts. Typst renders the EPUB cover directly instead of delegating rasterization to Poppler. Two consecutive canonical builds on the current macOS ARM64 host were byte-identical for both PDF and EPUB. Publication CI independently repeats the pinned build and rejects any byte drift. The platform is part of the reproducibility contract; structurally valid builds on another operating system are not assumed to have the same hashes. Hosted CI obtains Poppler from Homebrew only for inspection, never artifact generation; the verifier fails closed unless the required stable fields and every page's geometry are present.

## Verification results

| Gate | Result | Exact boundary |
|---|---|---|
| Immutable manuscript hash | Pass | Matches the recorded source contract. |
| Builder structural checks | Pass | Strict edition schema, XML, manifest, resources, contract-derived language and labels, accessibility metadata, navigation, every content-link label, all 211 local-fragment links, all 57 absolute HTTPS source links, distinct labels for different external destinations, all 238 repeated-card visible-title bindings, bounded `note`/`group` roles, manuscript hash, required content, ZIP order, timestamp, and uncompressed mimetype. |
| Release-evidence verifier | Pass | Exact edition-contract, artifact, and source hashes plus byte sizes; contract-derived title, credit, and language; PDF tagging, suspects, JavaScript, encryption, metadata, and every page's size and rotation; the EPUB's single active package, fixed manifest and cover-then-book spine, passive XHTML, metadata, unique resolved TOC targets, labelled content links, distinct external-destination labels, safe external-link schemes, and separate content/cover counts reproduce from the committed files. |
| Reader gateway | Pass internally | README presents the Vietnamese reader's PDF/EPUB choice, intended use, non-linear reading route, source model, safety boundary, public editorial policy, structured correction form, candidate status and missing-rights warning before contributor build details. Chapter 99 repeats the two correction routes and the privacy boundary. All relative links resolve to tracked files. These surfaces copy no artifact counts, do not call public access a license, and do not claim a named accountable individual, response SLA, external validation or market leadership. |
| veraPDF 1.30.2 PDF/UA-1 | Pass internally | The checksum-pinned Greenfield release was forced to the `ua1` profile and returned a normal compliant result bound to the current PDF: 106 passed rules, 847,613 passed checks, 0 failed rules, and 0 failed checks. The fail-closed wrapper also requires one exact artifact, one exact version across the core, validation-model, and apps components, no parse/encryption/memory/exception failure, and a successful one-job batch. veraPDF documents this as machine-verifiable PDF/UA checking; it does not prove human checkpoints or assistive-technology interoperability. |
| EPUBCheck 5.3.0 | Pass | 0 fatals, 0 errors, 0 warnings. |
| DAISY Ace 1.4.6 | Pass | The pinned CLI completed with `--exiterror2`; no issues were found in `cover.xhtml`, `nav.xhtml`, `book.xhtml`, or `package.opf`. Its cached headless Chrome required an unsandboxed local launch; Publication CI is configured to repeat the same pinned check in its isolated runner. |
| Chromium accessibility tree | Pass internally | Structural XHTML inspection exposes 238 visibly titled repeated cards: 151 practice notes, 36 caution notes, 7 day groups, 40 reference groups, and 4 decision groups. Every title target resolves and the builder enforces the matching `note` or `group` role. This proves the machine-visible XHTML binding only, not usability in a named screen reader or EPUB app. |
| Narrow-screen reflow | Pass | Headless viewport 320 × 568 CSS px, root font 24 px, dark mode on: root and body `scrollWidth` both 320; no rendered box crossed the viewport. |
| Dark-mode automated contrast | Pass | Minimum tested text contrast was 7.443:1. |
| PDF metadata and tagging | Pass | `pdfinfo` reports Vietnamese title metadata, canonical author, tagged structure, 197 unrotated A5 pages, no encryption, no JavaScript, and no suspects. Embedded text extraction preserves the first-sit and restart routes, source-code legend, source and safety boundaries, the first-three/five-lower/four-fruit distinctions, Chapter 10's canonical “who can attain?” cases, Chapter 12's beginner-first insight model, Appendix E's decision map, and the closing editorial-policy links. |
| PDF visual QA | Pass internally | The unchanged 179-page baseline was inspected in nine contact sheets, and later Chapter 12 revisions were rendered in full at 120–144 ppi. For this 197-page candidate, the introduction and source-map neighborhoods at PDF pages 6–13 and 187–190 were rendered at 144 ppi; the two new legends were also inspected full-size. No clipping, overlap, broken hierarchy, missing glyph, orphaned heading or spacing regression was found. Earlier inspections remain applicable to unchanged content. |
| Pilot schema, scorer, release verifier, and review packet | Pass internally | Both JSON Schema 2020-12 contracts meta-validate; all 186 tests pass; Ruff, Python compilation, issue-form YAML parsing, and `git diff --check` pass. The beginner contract requires the four-level insight conclusion model and rejects monastic-only or male-only restrictions on Stream-entry while preserving the possibility-versus-guarantee boundary. It binds written prompt display, unrestricted rereading and the absence of moderator follow-up cues. It also records pre-answer rubric exposure and excludes a contaminated attempt from the counted cohort. The Vietnamese packet guide and assignments keep the full ZIP, schemas, scorer, rubric, prior records and results on the operator side. The scorer still enforces the first five eligible completions, no-hint criteria, distress veto, exact artifact and contract hashes, canonical ancestry, privacy and retention rules. Source-legend regressions require first-read expansion of DN/MN/SN/AN/Ud and keep canonical locations separate from K/P/V/R traceability codes. EPUB, veraPDF, rights, edition, public-evidence and coordinator-packet regressions remain fail-closed. |
| Source-integrity re-audit | Pass internally | Every used K01–K40, P01–P02, V01, and R01–R11 code resolves in the source map. The load-bearing Chapter 10–11 claims were checked at segment level against Pāli roots and English translations frozen at SuttaCentral `bilara-data` commit `3af91efb1099190c74998247177f8ba6a076b8c0`. Chapter 5 claims C71–C72 were checked against P01's Basic Exercises I–IV. Chapter 7 claim C73 was checked against K01's ordinary clear-comprehension material, K15 DN 31:27.1–34.36 on reciprocal household duties, K18 SN 55.7:4.1–10.7 on harmful bodily and verbal conduct, and K19 AN 6.63:33.3–33.5 on intention and action. Appendix E claim C74 only compresses those already sourced decisions and the bounded Chapter 9 safety rules. Vietnam emergency claims C75–C76 are limited to the official 112 legal/operational record and the 113–115 numbering assignment; the book states the country, checked date, and lack of coverage or response-time guarantee. The Chapter 12 expansion is bounded to P02's foreword, introduction, method, sections 1–17 and notes 40–45 plus V01 XX.105–129, XXI.128–131, and XXII.1–21. A direct recheck confirmed P02's intended advanced audience, the ethical and concentration foundation, direct rather than merely reasoned discrimination, conditional maturation, stage-four subsidiary phenomena, dissolution-to-distressing-knowledge sequence, equanimity, and compressed late sequence. P02 does not supply a validated duration, count or concentration cutoff; the front-loaded progression, four-level attainment distinction, three-axis model, five-part evidential frame, worked interview, distinction between controllable conditions and emergent knowing, six-question frame, ordinary-sitting loop, single-object walkthrough, retrieval exercise and conclusion thresholds remain visibly editorial rather than canonical or clinically validated. Stages 12–17 reproduce P02's system functions and described aftermath while explicitly refusing to invent separately memorable feelings or a stage-production recipe. No contradiction was found in the direct P02 recheck. Independent internal passes on onboarding friction, habit re-entry, pacing, prose, acute-risk wording and insight-map explanation found no remaining material defect after corrections. These are internal reviews, not a named external Theravāda or clinical-safety sign-off. |

The PDF was compiled with Typst's PDF/UA-1 enforcement and separately passed veraPDF 1.30.2's machine-verifiable PDF/UA-1 profile. This supports the bounded statement that the exact PDF passes that validator profile. It does **not** prove the human checkpoints excluded from automated PDF/UA validation, the quality of navigation or reading order in a particular task, or interoperability with VoiceOver, NVDA, JAWS, or any other assistive-technology stack.

The pilot scorer proves consistency of the files it receives. Its canonical-origin and ancestry check uses the local `origin/main` ref and cannot prove that ref was freshly fetched. Its likely-contact-data detection is bounded and heuristic. It also cannot authenticate the moderator, independently verify that rubric blinding was respected, independently timestamp preregistration, or prove that a never-recorded attempt was not omitted. Those stronger claims require a fresh public-history check, human privacy review, and the external append-only registry specified by the pilot protocol. Passing the scorer is therefore not evidence that a real beginner cohort has passed.

## Open release gates

Use [`external-release-packet.md`](external-release-packet.md) as the operational handoff. The JSON registry is the machine-readable status source; this list explains the work.

1. Obtain the rights holder's explicit decision under `rights-decision-template.md` on copyright, licensing, source-text permissions, and allowed PDF/EPUB distribution. Do not infer a public redistribution grant from repository visibility.
2. Run the independent doctrinal review defined in `doctrinal-review-protocol.md` and the separately scoped review defined in `clinical-safety-review-protocol.md` against the frozen artifact commit and both hashes.
3. Run one five-reader unassisted beginner cohort using `beginner-validation-protocol.md`; verify the frozen artifact commit against fresh public canonical history, preregister through an external append-only registry, enumerate every started attempt, and publish only aggregate evidence in a descendant commit.
4. Run the required EPUB smoke test in a named standards-based reader at 150% text and dark mode. Automated Chromium reflow is useful evidence, not a substitute for this human reader-app gate.
5. Repeat failed reader gates with a fresh cohort after corrections.
6. Freeze and externally register `comparative-beginner-protocol.md`, then run it against the named panel before making even the narrower named-panel first-use outperformance claim. The current draft does not authorize “top choice,” “best,” or “number one.”

Until those gates close, the defensible description is: **a sourced, internally audited, dual-format candidate designed for Vietnamese beginners.**
