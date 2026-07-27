---
name: streamentry-book
description: Maintain and publish the Vietnamese Typst handbook Hướng Đến Nhập Lưu with strict Buddhist source provenance and render-first verification. Keep provenance badges above cited prose with clear spacing below each block.
---

# Streamentry Book

## Start Here

1. Read `AGENTS.md`.
2. Read `book/references/claim-ledger.md` before changing doctrinal prose.
3. Read `book/references/editorial-depth-audit.md` before expanding or compressing a chapter.
4. Read `book/references/release-evidence.md` before repeating or changing any verification claim.
5. Read `book/references/edition-contract.md` before changing any title, credit, language, output identity, cover string, navigation label, accessibility copy, semantic smoke text, or validation locale.
6. Read the immediate chapter, its source codes, `book/components.typ`, and `book/theme.typ` before editing.
7. Preserve the original Markdown unchanged.
8. For beginner validation, use `book/references/beginner-reader-kit.md` together with `book/references/beginner-validation-protocol.md`; freeze the cohort with `book/references/beginner-pilot-cohort-manifest.schema.json`, record every ordered attempt with `book/references/beginner-pilot-record.schema.json`, and pass only the manifest to `scripts/score-beginner-pilot.py`.
9. For independent doctrine review, use `book/references/doctrinal-review-protocol.md` together with the frozen segment map in `book/references/attainment-source-audit.md`; recheck the passages rather than inheriting the internal verdicts, and never convert an internal audit into external endorsement.
10. For release rights and all external gates, start with `book/references/external-release-packet.md`; use `rights-materials-inventory.md` before completing `rights-decision-template.md`, including its exact machine-readable public summary, and use `clinical-safety-review-protocol.md` for its separate scope. Recheck the inventory facts instead of treating them as legal conclusions. Terminal gates require the canonical evidence roles and mandatory public fields documented in `book/references/external-evidence/README.md`; do not substitute one generic report for a required bundle.
11. Build `scripts/build-external-review-packet.py` from a clean candidate when issuing work orders. Treat the resulting ignored ZIP as a deterministic handoff aid, never as evidence that a gate passed.

## Edition and Locale Contract

`book/edition.json` is the sole canonical authority for the active publication's
identity and locale. The current Vietnamese contract declares the author string
`CS Chánh Niệm + ChatGPT`. `book/edition.typ` is only the Typst access leaf;
`scripts/edition_contract.py` is the strict Python loader. Do not add fallback
or parallel constants to consumers.

Schema v1 supports the canonical Vietnamese line. Treat a future locale as a
separate publication, not a string substitution: assign a distinct edition and
output identity, localize every reader-facing field, make a locale-specific
rights decision, repeat independent doctrinal and safety review as applicable,
and run fresh novice and reader-app validation. Vietnamese evidence does not
validate translated wording.

## Dual-output Contract

`book/main.typ` is the single content entry point. It and the theme/components
consume locale data through `book/edition.typ`. Use `target()` in theme and
shared components to keep the A5 PDF presentation separate from semantic HTML
used by EPUB. Never package the print-oriented HTML fallback without
target-aware components: ignored grids can silently remove content.

The EPUB must be reflowable. Preserve heading hierarchy, source badges, cautions, practice cards, navigation, external links, Vietnamese diacritics, canonical metadata, and cover credit. Every content link needs a usable label; local fragments must resolve; external sources must use absolute HTTPS URLs; source-map link text must include its K, P, V, or R code when repeated labels would otherwise be indistinguishable. Do not reproduce A5 page breaks or worksheet blank space as fixed-layout ebook pages.

Under the pinned macOS 15 ARM64 publication tool and font environment, the builder compiles a byte-reproducible PDF/UA-1 candidate and fails on unexpected Typst HTML warnings, missing semantic body matter, heading jumps, broken navigation, broken or unlabelled content links, unsafe external-link schemes, lost dark-mode CSS, and non-reproducible ZIP metadata. Treat the operating system and architecture as part of that byte-reproducibility contract. A clean build, EPUBCheck result, and automated accessibility scan are necessary but do not prove behavior in Apple Books, Kindle, Kobo, or every assistive-technology stack.

The Python builder and verifier must load `book/edition.json` through
`scripts/edition_contract.py` before trusting any field. After building, run
`python3 scripts/verify_release.py`. It is the machine gate for the exact facts
in `release-evidence.md`; do not hand-wave a stale edition-contract hash,
artifact hash, byte size, page count, credit, PDF tagging, suspects, JavaScript,
encryption, per-page size or rotation, active EPUB metadata, navigation target,
or navigation count. The hosted publication workflow must remain read-only,
use `pull_request` rather than `pull_request_target`, pin actions and downloaded
tools, disable system fonts, and never upload `build/` or raw pilot records.

## Print Contract

Use a white page background. Keep large surfaces neutral and pale so they remain legible in grayscale without consuming unnecessary ink. Verify the cover, dense cards, margins, page geometry, and final page in both color and grayscale before publishing.

For the perfect-bound A5 edition, use `binding: left` and mirrored margins of 22 mm inside and 14 mm outside. Do not use a fixed larger left margin, because the inner edge alternates across facing pages.

Keep source and editorial badges on a line above their prose. Do not let a long badge compress only the first line of a paragraph or create a ragged wrap under it.

## Source Contract

Use one of six visible source classes:

- `KINH`: a named Nikāya discourse with speaker, context, translator, and edition checked.
- `LUẬN GIẢI`: Abhidhamma or later commentarial analysis.
- `THANH TỊNH ĐẠO`: claims specifically traceable to the *Visuddhimagga*.
- `MAHĀSI`: instructions traceable to a named Mahāsi work or lineage manual.
- `Y TẾ & NGHIÊN CỨU`: modern research and authoritative health guidance used only for health and safety questions.
- `BIÊN SOẠN`: modern habit design, editorial synthesis, or safety guidance.

Never label modern schedules, percentages, diagnostic heuristics, or attainment promises as `KINH`. “The Pāli discourses state” is different from “empirical fact.” Keep that distinction explicit.

For attainment language, keep the first three fetters, the full five lower fetters, the four fruits, and DN 2's broader discourse title distinct. Use Chapter 10 for the first three fetters, Chapter 11 for the wider 3–5–4 classification, the glossary for direct lookup, claim codes C41–C45 as the canonical project anchors, C66 for the bounded object/basis/means teaching model, and `attainment-source-audit.md` for the immutable passage-level audit. Never present that teaching model or its meditation case as a canonical 1–2–3 sequence.

For the insight map, Chapter 12 must define the map, `tuệ`, `các hành`, conditional maturation and the practice boundary before presenting the seven purifications or competing counts. Keep object, knowing, reaction and conclusion distinct, and preserve the beginner's direct route to the four-region explanation. Preserve the six-question explanation across stages 1–11: prior foundation, changed way of knowing, possible experience, appropriate practice, insufficient lookalikes and transition. The frame and ordinary-sitting loop are editorial scaffolding bound by C69. They are not canonical checklists, validated stage classifiers, fixed calendars, or exercises that mechanically produce named stages.

For ordinary-life practice, Chapter 7 owns the transfer contract. Keep task-first
attention, a brief response check, and formal practice distinct. Immediate
protection and essential duties come before introspection. The collision loop,
repair loop, timing labels, work case, and retrieval test are editorial tools
bound by claim C73; never present them as numbered instructions from MN 10,
DN 31, SN 55.7, or AN 6.63.

Appendix E owns the single visual retrieval map. Preserve its safety gate,
formal-practice and daily-life branches, and post-practice decision in that
order across PDF and semantic HTML. Its editorial structure is bound by C74;
the Vietnam 112–115 route is bound separately by C75–C76 and must retain its
country and checked-date limits. Never present the map as a canonical sequence,
diagnostic instrument, new meditation method, or substitute for the linked
chapters.

## Writing Contract

Write contemporary Vietnamese that is precise, calm, and public-facing. Use full paragraphs, exact verbs, and varied cadence. Avoid em dashes, motivational fog, sectarian claims, and invented certainty. Define Pāli terms at first use and retain them only when translation would conceal a meaningful distinction.

For beginner-facing prose, apply these gates before building:

1. No technical term survives more than one sentence without a plain-language gloss or an explicit local pointer.
2. Every chapter and major conceptual pivot says what it carries forward and why the next section follows.
3. Every dense list has an orientation before it and a synthesis, example, or action after it.
4. A first-use route must expose the next physical action, its local stop condition, and one direct fallback without forcing the reader through a distant chapter. Keep one canonical restart protocol and use short pointers elsewhere.
5. In safety and decision passages, give each observable trigger or action its own list item. Treat sentence length as a review signal, not an automatic defect; preserve a long paragraph when its source-bound explanation is coherent and each inference remains visible.
6. Close each explanatory chapter with either a short closed-book retrieval card or an explicit real-world decision block. Test the central distinction and next action, not vocabulary recall or attainment status. Repeat safety thresholds locally when a distant lookup could delay action.

The glossary is a reference aid, not permission to leave the main reading path opaque.

## README Contract

Keep `README.md` reader-first and Vietnamese-first. Before contributor build
details, it must expose the current PDF/EPUB choice, intended audience,
non-linear reading route, source-tier model, safety boundary, correction path,
candidate status, and the missing-rights warning. Public file access is not a
license. Read identity from `book/edition.json`, artifact status from
`release-evidence.md`, and external status from
`external-release-gates.json`; do not copy counts or claims that can drift.

## Build and Verify

```sh
python3 scripts/build-epub.py
pdfinfo dist/huong-den-nhap-luu.pdf
pdftotext -layout dist/huong-den-nhap-luu.pdf build/huong-den-nhap-luu.txt
pdftoppm -png -r 144 dist/huong-den-nhap-luu.pdf build/page
```

Inspect the cover, contents, every chapter opener, dense appendix pages, source map, and final page. Search extracted text for missing glyphs, bad URLs, placeholder language, and unlabelled guarantees.

For EPUB, run the packaging script, EPUBCheck, and DAISY Ace when available. Inspect metadata, cover, table of contents, internal anchors, external links, font resizing, dark mode, and reading order in at least one standards-based reader. For PDF, confirm the PDF/UA metadata and tagged structure, but do not call it independently validated without a separate PDF/UA validator. Structural checks are not proof of reader interoperability.

Before describing the book as validated for beginners, run `book/references/beginner-validation-protocol.md` with unassisted novice readers and preserve scorer-produced aggregate and reader-app reports tied to exact committed artifacts, contract hashes, and an ordered attempt manifest. A self-reported manifest timestamp is not independent preregistration evidence; use an external append-only registry when that claim matters. Before making a comparative market claim, run a preregistered test against named alternatives. Internal editorial review is not independent expert endorsement.

For external assignments, run
`python3 scripts/build-external-review-packet.py` after the candidate commit is
clean. The packet must carry the exact committed artifacts, protocol copies,
assignment sheets, manifest, and checksum index. Its construction does not
authenticate people, close gates, or permit stronger claims.

After the final build, update `book/references/release-evidence.md` with exact hashes and results. A dirty candidate record is not a release manifest and cannot be used as the artifact identity for human testing.

`book/references/external-release-gates.json` is the schema-v3 machine-readable status and permitted-claims registry. A frozen artifact commit is valid only when it is an ancestor of the evidence commit and contains the exact PDF and EPUB bytes named by the current release record; the release record and evidence may be added in a later commit. `scripts/verify_release.py` rejects stale protocol hashes, contradictory statuses, incomplete typed bundles, evidence-path reuse, role/header mismatches, missing completion, confirmation or scope-limit fields, duplicate artifact digests, stale evidence hashes, malformed cohort/report bindings, public contact data, or claims not derived from passed gates. Rights evidence additionally fails when its inventory/source binding is stale, PDF or EPUB is unauthorized, required distribution scopes are absent, contributor or third-party status is unresolved, or any rights item remains open. For the novice gates, generate both outputs with `--output` and `--epub-evidence-output`: the aggregate report carries five counted-record hashes, while the reader-app report carries one matching counted-record hash. Deterministic output does not authenticate signatures, rights ownership, legal validity, credentials, reviewer independence, participant identity, preregistration timing, or omitted-attempt completeness; those remain human and custody evidence.
