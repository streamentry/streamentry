---
name: streamentry-book
description: Maintain and publish the Vietnamese Typst handbook Hướng Đến Nhập Lưu with strict Buddhist source provenance and render-first verification.
---

# Streamentry Book

## Start Here

1. Read `AGENTS.md`.
2. Read `book/references/claim-ledger.md` before changing doctrinal prose.
3. Read the immediate chapter, its source codes, `book/components.typ`, and `book/theme.typ` before editing.
4. Preserve the original Markdown unchanged.

## Publication Credit

The canonical author string is `TS. Lê Việt Hồng - Cư Sĩ Chánh Niệm + ChatGPT`. Keep it synchronized across `book/main.typ`, the rendered cover, PDF metadata, and `README.md`.

## Print Contract

Use a white page background. Keep large surfaces neutral and pale so they remain legible in grayscale without consuming unnecessary ink. Verify the cover, dense cards, margins, page geometry, and final page in both color and grayscale before publishing.

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

## Build and Verify

```sh
typst compile --root /Volumes/SSD/streamentry book/main.typ dist/huong-den-nhap-luu.pdf
pdfinfo dist/huong-den-nhap-luu.pdf
pdftotext -layout dist/huong-den-nhap-luu.pdf build/huong-den-nhap-luu.txt
pdftoppm -png -r 144 dist/huong-den-nhap-luu.pdf build/page
```

Inspect the cover, contents, every chapter opener, dense appendix pages, source map, and final page. Search extracted text for missing glyphs, bad URLs, placeholder language, and unlabelled guarantees.
