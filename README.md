# streamentry

Source and publication files for *Hướng Đến Nhập Lưu*, an A5 Vietnamese mindfulness handbook for lay readers. The book distinguishes early Pāli discourses, later Theravāda commentary, the *Visuddhimagga*, Mahāsi instructions, modern research, and editorial guidance.

The title describes a direction of practice, not a guarantee of spiritual attainment.

**Author:** CS Chánh Niệm + ChatGPT

## Build PDF

```sh
typst compile --root . book/main.typ dist/huong-den-nhap-luu.pdf
```

## Build EPUB 3

```sh
python3 scripts/build-epub.py
```

The EPUB builder recompiles the PDF for a synchronized cover, compiles Typst's semantic HTML target, packages a reflowable EPUB 3 publication, and runs structural, XML, manifest, navigation, manuscript-hash, and required-content checks. It requires Typst 0.15 or later and `pdftoppm`.

The verified deliverables are:

- [`dist/huong-den-nhap-luu.pdf`](dist/huong-den-nhap-luu.pdf)
- [`dist/huong-den-nhap-luu.epub`](dist/huong-den-nhap-luu.epub)

Source provenance is documented in [`book/references/claim-ledger.md`](book/references/claim-ledger.md). The EPUB is reflowable: it preserves source labels, cautions, practice cards, navigation, links, and Vietnamese text while intentionally omitting A5 page geometry.

The PDF uses an A5 print-safe white page background. Small neutral surfaces preserve hierarchy in grayscale without printing a full-page tint.

## Quality evidence and limits

- [`book/references/editorial-depth-audit.md`](book/references/editorial-depth-audit.md) checks every chapter for under-explained mechanisms, procedures, and limits.
- [`book/references/publish-readiness-audit.md`](book/references/publish-readiness-audit.md) records the adapted 80-item publication scorecard.
- [`book/references/beginner-validation-protocol.md`](book/references/beginner-validation-protocol.md) defines unassisted comprehension, safety, navigation, and EPUB-reader gates.
- Corrections can be reported through the [public issue tracker](https://github.com/streamentry/streamentry/issues).

The current build has an 83-page A5 PDF and a deterministic EPUB with 113 navigable headings. EPUBCheck 5.3.0 reports no errors or warnings. These checks establish source traceability and format validity; they do not establish spiritual attainment, clinical safety for every reader, proprietary-reader interoperability, independent expert endorsement, or a “number-one” market position. Those claims require the external reviews and reader tests named in the validation protocol.
