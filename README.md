# streamentry

Source and publication files for *Hướng Đến Nhập Lưu*, an A5 Vietnamese mindfulness handbook for lay readers. The book distinguishes early Pāli discourses, later Theravāda commentary, the *Visuddhimagga*, Mahāsi instructions, health and research evidence, and editorial guidance.

The title describes a direction of practice, not a guarantee of spiritual attainment.

**Author:** CS Chánh Niệm + ChatGPT

## Build synchronized PDF and EPUB

```sh
python3 scripts/build-epub.py
```

The canonical builder creates both deliverables from the same Typst entry point. To compile only the PDF with the same deterministic PDF/UA-1 settings:

```sh
typst compile --root . --creation-timestamp 1785024000 --pdf-standard ua-1 book/main.typ dist/huong-den-nhap-luu.pdf
```

The builder recompiles the PDF for a synchronized cover, compiles Typst's semantic HTML target, packages a reflowable EPUB 3 publication, and runs structural, XML, manifest, navigation, manuscript-hash, and required-content checks. It requires Typst 0.15 or later and `pdftoppm`.

The current internally verified candidate files are:

- [`dist/huong-den-nhap-luu.pdf`](dist/huong-den-nhap-luu.pdf)
- [`dist/huong-den-nhap-luu.epub`](dist/huong-den-nhap-luu.epub)

Source provenance is documented in [`book/references/claim-ledger.md`](book/references/claim-ledger.md). The EPUB is reflowable: it preserves source labels, cautions, practice cards, navigation, links, and Vietnamese text while intentionally omitting A5 page geometry.

The PDF uses an A5 print-safe white page background. Small neutral surfaces preserve hierarchy in grayscale without printing a full-page tint.

## Quality evidence and limits

- [`book/references/editorial-depth-audit.md`](book/references/editorial-depth-audit.md) checks every chapter for under-explained mechanisms, procedures, and limits.
- [`book/references/publish-readiness-audit.md`](book/references/publish-readiness-audit.md) records the adapted 80-item publication scorecard.
- [`book/references/release-evidence.md`](book/references/release-evidence.md) binds current hashes, tool versions, format checks, visual scope, and the exact external gates that remain open.
- [`book/references/doctrinal-review-protocol.md`](book/references/doctrinal-review-protocol.md) defines the qualifications, scope, evidence record, and finding format for an independent Theravāda review.
- [`book/references/beginner-validation-protocol.md`](book/references/beginner-validation-protocol.md) defines unassisted comprehension, safety, navigation, and EPUB-reader gates.
- [`book/references/comparative-beginner-protocol.md`](book/references/comparative-beginner-protocol.md) preregisters a fair, rights-safe comparison against a fixed panel of current Vietnamese beginner books.
- [`book/references/beginner-reader-kit.md`](book/references/beginner-reader-kit.md) gives the consent script, eight-task rubric, privacy rules, and EPUB smoke-test procedure.
- [`book/references/beginner-pilot-cohort-manifest.schema.json`](book/references/beginner-pilot-cohort-manifest.schema.json), [`book/references/beginner-pilot-record.schema.json`](book/references/beginner-pilot-record.schema.json), and [`scripts/score-beginner-pilot.py`](scripts/score-beginner-pilot.py) bind one ordered five-to-seven-attempt cohort to exact committed artifacts and a frozen scoring contract.
- Corrections can be reported through the [public issue tracker](https://github.com/streamentry/streamentry/issues).

The pilot scorer requires Python's `jsonschema` package and accepts only the authoritative manifest:

```sh
python3 scripts/score-beginner-pilot.py build/beginner-pilot/<cohort-id>/manifest.json \
  --output build/beginner-pilot/<cohort-id>/aggregate-report.md
```

The current candidate is rebuilt and remeasured whenever the content changes; exact counts and hashes belong in the release evidence rather than this overview. Structural checks establish source traceability and format validity. They do not establish spiritual attainment, clinical safety for every reader, proprietary-reader interoperability, independent expert endorsement, or a “number-one” market position. The release candidate is identified by the enclosing Git commit plus the hashes in `release-evidence.md`; external reviews and reader tests must target that exact commit.
