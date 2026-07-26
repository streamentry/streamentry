---
name: streamentry-book
description: Maintain and publish the Vietnamese Typst handbook Hướng Đến Nhập Lưu with strict Buddhist source provenance and render-first verification. Keep provenance badges above cited prose with clear spacing below each block.
---

# Streamentry Book

## Start Here

1. Read `AGENTS.md`.
2. Read `book/references/claim-ledger.md` before changing doctrinal prose.
3. Read `book/references/editorial-depth-audit.md` before expanding or compressing a chapter.
4. Read the immediate chapter, its source codes, `book/components.typ`, and `book/theme.typ` before editing.
5. Preserve the original Markdown unchanged.
6. For beginner validation, use `book/references/beginner-reader-kit.md` together with `book/references/beginner-validation-protocol.md`.

## Publication Credit

The canonical author string is `CS Chánh Niệm + ChatGPT`. Keep it synchronized across `book/main.typ`, the rendered cover, PDF metadata, and `README.md`.

## Dual-output Contract

`book/main.typ` is the single content entry point. Use `target()` in theme and shared components to keep the A5 PDF presentation separate from semantic HTML used by EPUB. Never package the print-oriented HTML fallback without target-aware components: ignored grids can silently remove content.

The EPUB must be reflowable. Preserve heading hierarchy, source badges, cautions, practice cards, navigation, external links, Vietnamese diacritics, canonical metadata, and cover credit. Do not reproduce A5 page breaks or worksheet blank space as fixed-layout ebook pages.

The builder fails on unexpected Typst HTML warnings, missing semantic body matter, heading jumps, broken navigation, lost dark-mode CSS, and non-reproducible ZIP metadata. A clean build and EPUBCheck result are necessary but do not prove behavior in Apple Books, Kindle, Kobo, or every assistive-technology stack.

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
- `NGHIÊN CỨU`: modern research used only for health and safety questions.
- `BIÊN SOẠN`: modern habit design, editorial synthesis, or safety guidance.

Never label modern schedules, percentages, diagnostic heuristics, or attainment promises as `KINH`. “The Pāli discourses state” is different from “empirical fact.” Keep that distinction explicit.

## Writing Contract

Write contemporary Vietnamese that is precise, calm, and public-facing. Use full paragraphs, exact verbs, and varied cadence. Avoid em dashes, motivational fog, sectarian claims, and invented certainty. Define Pāli terms at first use and retain them only when translation would conceal a meaningful distinction.

For beginner-facing prose, apply three gates before building:

1. No technical term survives more than one sentence without a plain-language gloss or an explicit local pointer.
2. Every chapter and major conceptual pivot says what it carries forward and why the next section follows.
3. Every dense list has an orientation before it and a synthesis, example, or action after it.

The glossary is a reference aid, not permission to leave the main reading path opaque.

## Build and Verify

```sh
typst compile --root /Volumes/SSD/streamentry book/main.typ dist/huong-den-nhap-luu.pdf
python3 scripts/build-epub.py
pdfinfo dist/huong-den-nhap-luu.pdf
pdftotext -layout dist/huong-den-nhap-luu.pdf build/huong-den-nhap-luu.txt
pdftoppm -png -r 144 dist/huong-den-nhap-luu.pdf build/page
```

Inspect the cover, contents, every chapter opener, dense appendix pages, source map, and final page. Search extracted text for missing glyphs, bad URLs, placeholder language, and unlabelled guarantees.

For EPUB, run the packaging script and then EPUBCheck when available. Inspect metadata, cover, table of contents, internal anchors, external links, font resizing, dark mode, and reading order in at least one standards-based reader. Structural checks are not proof of reader interoperability.

Before describing the book as validated for beginners, run `book/references/beginner-validation-protocol.md` with unassisted novice readers. Before making a comparative market claim, run a preregistered test against named alternatives. Internal editorial review is not independent expert endorsement.
