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
5. Read the immediate chapter, its source codes, `book/components.typ`, and `book/theme.typ` before editing.
6. Preserve the original Markdown unchanged.
7. For beginner validation, use `book/references/beginner-reader-kit.md` together with `book/references/beginner-validation-protocol.md`; freeze the cohort with `book/references/beginner-pilot-cohort-manifest.schema.json`, record every ordered attempt with `book/references/beginner-pilot-record.schema.json`, and pass only the manifest to `scripts/score-beginner-pilot.py`.
8. For independent doctrine review, use `book/references/doctrinal-review-protocol.md`; never convert an internal audit into external endorsement.

## Publication Credit

The canonical author string is `CS Chánh Niệm + ChatGPT`. Keep it synchronized across `book/main.typ`, the rendered cover, PDF metadata, and `README.md`.

## Dual-output Contract

`book/main.typ` is the single content entry point. Use `target()` in theme and shared components to keep the A5 PDF presentation separate from semantic HTML used by EPUB. Never package the print-oriented HTML fallback without target-aware components: ignored grids can silently remove content.

The EPUB must be reflowable. Preserve heading hierarchy, source badges, cautions, practice cards, navigation, external links, Vietnamese diacritics, canonical metadata, and cover credit. Do not reproduce A5 page breaks or worksheet blank space as fixed-layout ebook pages.

Under the pinned macOS 15 ARM64 publication tool and font environment, the builder compiles a byte-reproducible PDF/UA-1 candidate and fails on unexpected Typst HTML warnings, missing semantic body matter, heading jumps, broken navigation, lost dark-mode CSS, and non-reproducible ZIP metadata. Treat the operating system and architecture as part of that byte-reproducibility contract. A clean build, EPUBCheck result, and automated accessibility scan are necessary but do not prove behavior in Apple Books, Kindle, Kobo, or every assistive-technology stack.

After building, run `python3 scripts/verify_release.py`. It is the machine gate for the exact facts in `release-evidence.md`; do not hand-wave a stale hash, byte size, page count, credit, PDF tagging, suspects, JavaScript, encryption, per-page size or rotation, active EPUB metadata, navigation target, or navigation count. The hosted publication workflow must remain read-only, use `pull_request` rather than `pull_request_target`, pin actions and downloaded tools, disable system fonts, and never upload `build/` or raw pilot records.

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

For attainment language, keep the first three fetters, the full five lower fetters, the four fruits, and DN 2's broader discourse title distinct. Use Chapter 10, the glossary, and claim codes C41–C45 as the canonical project anchors.

## Writing Contract

Write contemporary Vietnamese that is precise, calm, and public-facing. Use full paragraphs, exact verbs, and varied cadence. Avoid em dashes, motivational fog, sectarian claims, and invented certainty. Define Pāli terms at first use and retain them only when translation would conceal a meaningful distinction.

For beginner-facing prose, apply three gates before building:

1. No technical term survives more than one sentence without a plain-language gloss or an explicit local pointer.
2. Every chapter and major conceptual pivot says what it carries forward and why the next section follows.
3. Every dense list has an orientation before it and a synthesis, example, or action after it.

The glossary is a reference aid, not permission to leave the main reading path opaque.

## Build and Verify

```sh
python3 scripts/build-epub.py
pdfinfo dist/huong-den-nhap-luu.pdf
pdftotext -layout dist/huong-den-nhap-luu.pdf build/huong-den-nhap-luu.txt
pdftoppm -png -r 144 dist/huong-den-nhap-luu.pdf build/page
```

Inspect the cover, contents, every chapter opener, dense appendix pages, source map, and final page. Search extracted text for missing glyphs, bad URLs, placeholder language, and unlabelled guarantees.

For EPUB, run the packaging script, EPUBCheck, and DAISY Ace when available. Inspect metadata, cover, table of contents, internal anchors, external links, font resizing, dark mode, and reading order in at least one standards-based reader. For PDF, confirm the PDF/UA metadata and tagged structure, but do not call it independently validated without a separate PDF/UA validator. Structural checks are not proof of reader interoperability.

Before describing the book as validated for beginners, run `book/references/beginner-validation-protocol.md` with unassisted novice readers and preserve a scorer-produced aggregate report tied to exact committed artifacts, contract hashes, and an ordered attempt manifest. A self-reported manifest timestamp is not independent preregistration evidence; use an external append-only registry when that claim matters. Before making a comparative market claim, run a preregistered test against named alternatives. Internal editorial review is not independent expert endorsement.

After the final build, update `book/references/release-evidence.md` with exact hashes and results. A dirty candidate record is not a release manifest and cannot be used as the artifact identity for human testing.
