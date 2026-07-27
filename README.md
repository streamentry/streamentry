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

The builder recompiles the PDF, asks Typst to render the same first page as the EPUB cover, compiles Typst's semantic HTML target, packages a reflowable EPUB 3 publication, and runs structural, XML, manifest, navigation, manuscript-hash, and required-content checks. Publication CI release builds use Typst 0.15.0, its embedded Libertinus Serif and DejaVu Sans Mono families, and the official Inter 4.0 OTF files with system-font discovery disabled.

The current internally verified candidate files are:

- [`dist/huong-den-nhap-luu.pdf`](dist/huong-den-nhap-luu.pdf)
- [`dist/huong-den-nhap-luu.epub`](dist/huong-den-nhap-luu.epub)

Source provenance is documented in [`book/references/claim-ledger.md`](book/references/claim-ledger.md). The EPUB is reflowable: it preserves source labels, cautions, practice cards, navigation, links, and Vietnamese text while intentionally omitting A5 page geometry.

The PDF uses an A5 print-safe white page background. Small neutral surfaces preserve hierarchy in grayscale without printing a full-page tint.

## Verify the release candidate

```sh
python3 scripts/verify_release.py
```

The verifier compares the human-facing release record against the actual immutable manuscript, PDF, and EPUB. It fails on stale hashes or sizes, wrong PDF title or credit, missing tags, suspect, encrypted, JavaScript-bearing, rotated, or non-A5 PDF pages, wrong active EPUB package, manifest, spine, or navigation document, active base or script elements, wrong EPUB title, creator or language, unresolved or duplicate TOC targets, and navigation-count drift.

Every pull request and push to `main` that can affect publication runs `.github/workflows/publication-ci.yml`. The workflow uses the canonical macOS 15 ARM64 builder with only a read-only ephemeral `GITHUB_TOKEN` and no repository or environment secrets. It pins GitHub Actions by commit, downloads the checksum-pinned official macOS ARM64 build of Typst 0.15.0 plus Inter 4.0 and EPUBCheck 5.3.0, installs hash-locked Python wheels and locked DAISY Ace 1.4.6 dependencies, rebuilds both formats with system fonts disabled, requires byte-identical tracked artifacts, and runs the complete automated Python, schema, EPUBCheck, and accessibility gates. It never uploads raw pilot records. Human reader-app, assistive-technology, and independent PDF/UA checks remain separate external evidence.

## Quality evidence and limits

- [`book/references/editorial-depth-audit.md`](book/references/editorial-depth-audit.md) checks every chapter for under-explained mechanisms, procedures, and limits.
- [`book/references/publish-readiness-audit.md`](book/references/publish-readiness-audit.md) records the adapted 80-item publication scorecard.
- [`book/references/release-evidence.md`](book/references/release-evidence.md) binds current hashes, tool versions, format checks, visual scope, and the exact external gates that remain open.
- [`book/references/external-release-packet.md`](book/references/external-release-packet.md) is the single operational handoff for rights, expert review, novice testing, human EPUB evidence, and bounded comparison.
- [`book/references/external-release-gates.json`](book/references/external-release-gates.json) is the machine-verified status, typed-evidence, and permitted-claims registry; terminal gates fail closed unless every required gate-specific evidence role is present and candidate-bound.
- [`book/references/rights-decision-template.md`](book/references/rights-decision-template.md) separates authority, third-party material, formats, channels, commercial scope, and allowed distribution.
- [`book/references/doctrinal-review-protocol.md`](book/references/doctrinal-review-protocol.md) defines the qualifications, scope, evidence record, and finding format for an independent Theravāda review.
- [`book/references/clinical-safety-review-protocol.md`](book/references/clinical-safety-review-protocol.md) defines the separate competence, scope, finding, and sign-off rules for safety and research claims.
- [`book/references/beginner-validation-protocol.md`](book/references/beginner-validation-protocol.md) defines unassisted comprehension, safety, navigation, and EPUB-reader gates.
- [`book/references/comparative-beginner-protocol.md`](book/references/comparative-beginner-protocol.md) records a preregistration draft for a fair, rights-safe comparison against a fixed panel of Vietnamese beginner books; it is not yet an external registration receipt.
- [`book/references/beginner-reader-kit.md`](book/references/beginner-reader-kit.md) gives the consent script, eight-task rubric, privacy rules, and EPUB smoke-test procedure.
- [`book/references/beginner-pilot-cohort-manifest.schema.json`](book/references/beginner-pilot-cohort-manifest.schema.json), [`book/references/beginner-pilot-record.schema.json`](book/references/beginner-pilot-record.schema.json), and [`scripts/score-beginner-pilot.py`](scripts/score-beginner-pilot.py) bind one ordered five-to-seven-attempt cohort to exact committed artifacts and a frozen scoring contract.
- Corrections can be reported through the [public issue tracker](https://github.com/streamentry/streamentry/issues).

The pilot scorer requires Python's `jsonschema` package and accepts only the authoritative manifest. Generate both public, privacy-coarsened evidence roles in the same scoring run:

```sh
python3 scripts/score-beginner-pilot.py build/beginner-pilot/<cohort-id>/manifest.json \
  --output build/beginner-pilot/<cohort-id>/aggregate-report.md \
  --epub-evidence-output build/beginner-pilot/<cohort-id>/reader-app-report.md
```

The aggregate report binds the cohort ID, manifest SHA-256, and exactly five counted-record SHA-256 values. The reader-app report binds the same cohort and manifest plus exactly one of those five record hashes. These deterministic reports establish consistency with the supplied private files; they do not authenticate participants or moderators, prove preregistration custody, or replace the required public-history, privacy-review, and external-registration evidence.

The current candidate is rebuilt and remeasured whenever the content changes; exact counts and hashes belong in the release evidence rather than this overview. The first-month route now continues explicitly from the seven-day start through days 8–30, but that bridge is visibly editorial and has not yet been validated for adherence. Structural checks establish source traceability and format validity. They do not establish spiritual attainment, clinical safety for every reader, proprietary-reader interoperability, independent expert endorsement, or a “number-one” market position. External reviews and reader tests target the frozen ancestor commit that contains the exact PDF and EPUB bytes; `release-evidence.md` and public evidence may be committed later without changing that tested identity.
