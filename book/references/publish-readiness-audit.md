# Publish Readiness Audit

Checked: 2026-07-25

The 80-item scoring is a static content review adapted from a web-oriented benchmark. Release verification was then run against the same content: the PDF compiled to 83 A5 pages, the EPUB builder found 113 navigable headings, and EPUBCheck 5.3.0 reported no errors or warnings. Those build facts do not replace human-reader or expert review.

## Overview

- **Content**: *Hướng Đến Nhập Lưu*
- **Artifact**: standalone Vietnamese handbook, not a website
- **Audit scope**: book prose, references, frontmatter, chapter structure, appendices, and repo-level publication contract
- **Gate verdict**: **SHIP as an internally verified candidate; do not claim external beginner validation or market leadership**
- **Book-applicable score**: **88.4/100**
- **GEO analogue**: **93.8/100**
- **Observable EEAT score**: **68.3/100**; Authority is excluded because it lacks enough applicable artifact-level data
- **Veto status**: **No critical veto triggered**

## Veto Audit

| Check | Status | Evidence |
|---|---|---|
| C01 Intent alignment | Pass | `book/chapters/00-frontmatter.typ` says it is "một cuốn sổ tay, không phải giấy chứng nhận"; title and subtitle match that frame. |
| T04 Disclosure statements | Pass | No affiliate or sponsored commerce appears in `README.md`, `book/main.typ`, or the chapter text; source badges disclose provenance instead. |
| R10 Content consistency | Pass | `book/references/claim-ledger.md`, `book/chapters/11-nhap-luu.typ`, and `book/appendices/c-faq.typ` keep the same distinctions between sutta, commentary, Mahāsi, and editorial advice. |

## Weighting

Applied as a How-to Guide / handbook. Authority is excluded from the weighted total because all A items are site/organization-level signals and this artifact is a book, not a site.

| Dimension | Score | Weight used | Weighted |
|---|---:|---:|---:|
| C -- Contextual Clarity | 100 | 21.1% | 21.1 |
| O -- Organization | 100 | 21.1% | 21.1 |
| R -- Referenceability | 100 | 10.5% | 10.5 |
| E -- Exclusivity | 75 | 5.3% | 3.9 |
| Exp -- Experience | 45 | 5.3% | 2.4 |
| Ept -- Expertise | 80 | 21.1% | 16.8 |
| T -- Trust | 80 | 15.8% | 12.6 |
| A -- Authority | N/A | excluded | excluded |
| **Weighted total** |  |  | **88.4/100** |

Weights are the How-to Guide weights renormalized after excluding Authority, whose 10 items are all unavailable from the standalone artifact. The score is diagnostic, not a claim that the book is 88.4% “true” or 88.4% likely to be the best choice.

## Do not optimize blindly for 100

Several lost points are not defects that prose can honestly erase. Adding invented first-person testimony, decorative “proof,” unverifiable credentials, or testimonials would raise superficial checklist coverage while lowering trust. This web-oriented framework is useful for finding omissions; it is not a specification for a Buddhist handbook. External review and observed reader performance are the only legitimate way to close the material gaps.

## Dimension Scores

### C -- Contextual Clarity

| ID | Status | Evidence | N/A reason |
|---|---|---|---|
| C01 | Pass | `book/chapters/00-frontmatter.typ` frames the book as a handbook, not a proof of attainment. | None |
| C02 | Pass | The frontmatter gives the direct purpose: help lay readers start and sustain Mahāsi practice. | None |
| C03 | Pass | The book covers beginner use, doctrine, practice, safety, glossary, and FAQ. | None |
| C04 | Pass | `book/chapters/00-frontmatter.typ` defines the six source classes and keeps Pāli use explicit. | None |
| C05 | Pass | `book/references/claim-ledger.md` separates sutta, commentary, Mahāsi, research, and editorial claims. | None |
| C06 | Pass | The frontmatter targets lay readers and repeats that the book is for ordinary household life. | None |
| C07 | Pass | Chapter sequence is coherent: basics, path, sutta frame, dependent origination, method, safety, map, entry, appendices. | None |
| C08 | Pass | `book/chapters/00-frontmatter.typ` includes a reading path for first-time readers and later-stage readers. | None |
| C09 | Pass | Appendix C is a dedicated FAQ with 12 direct questions and answers. | None |
| C10 | Pass | Chapter 11 closes by rejecting attainment guarantees and returning to direction, practice, and verification. | None |

### O -- Organization

| ID | Status | Evidence | N/A reason |
|---|---|---|---|
| O01 | Pass | `book/theme.typ` defines chapter openers, headings, and target-aware layout rules. | None |
| O02 | Pass | `book/chapters/00-frontmatter.typ` provides a top-level orientation block and reading path card. | None |
| O03 | Pass | `book/references/claim-ledger.md` and the appendix tables use clear tabular structure. | None |
| O04 | Pass | The book uses headings, lists, check cards, caution boxes, and FAQ blocks consistently. | None |
| O05 | N/A | The artifact is a book, not a site; there is no schema/JSON-LD layer in the publication pipeline. | No web schema layer to audit. |
| O06 | Pass | Chapters are chunked into short, focused units with appendices reserved for reference material. | None |
| O07 | Pass | `book/theme.typ` and `book/components.typ` create a strong visual hierarchy for cover, chapters, cards, and citations. | None |
| O08 | Pass | The frontmatter includes an outline, and HTML target support preserves navigable structure. | None |
| O09 | Pass | The manuscript is dense without becoming unreadable; reference and safety material is separated from running prose. | None |
| O10 | N/A | The publication is text-led; there are no images, audio, or video assets to structure. | No multimedia assets in this handbook. |

### R -- Referenceability

| ID | Status | Evidence | N/A reason |
|---|---|---|---|
| R01 | Pass | `book/references/claim-ledger.md` records exact claim IDs, source IDs, URLs, and caveats. | None |
| R02 | Pass | The book cites sutta, commentary, Mahāsi, research, and editorial sources throughout, not just once in the back matter. | None |
| R03 | Pass | `book/chapters/00-frontmatter.typ` and `book/references/claim-ledger.md` keep a clear source hierarchy. | None |
| R04 | Pass | Claim-to-source mapping is explicit in the ledger and repeated in the chapter provenance badges. | None |
| R05 | Pass | The claim ledger includes a strength scale and caveat column, so methodology is visible. | None |
| R06 | Pass | `book/references/claim-ledger.md`, `book/references/editorial-depth-audit.md`, and `book/chapters/99-nguon.typ` are date-checked. | None |
| R07 | Pass | The book uses precise entity codes such as K01, P01, V01, R01, and R02 instead of vague source language. | None |
| R08 | Pass | Cross-references connect chapters, appendices, claim ledger, and source map. | None |
| R09 | Pass | `book/theme.typ` uses semantic HTML elements and bookmarks rather than decorative-only structure. | None |
| R10 | Pass | The manuscript keeps its own internal claims consistent, especially around stream-entry, safety, and source-tier boundaries. | None |

### E -- Exclusivity

| ID | Status | Evidence | N/A reason |
|---|---|---|---|
| E01 | Partial | The book adds an original editorial framework and reading path, but it does not present original empirical data. | None |
| E02 | Pass | The frontmatter creates a distinctive frame: handbook, not guarantee, with separate source tiers. | None |
| E03 | Fail | The book cites primary texts but reports no original primary research of its own. Using primary sources is not the same as conducting primary research. | None |
| E04 | Pass | Chapter 4 rejects the unsupported "easiest link" ranking and similar simplifications. | None |
| E05 | Fail | The publication is mostly text and tables; there are no proprietary visuals in the book artifact itself. | None |
| E06 | Pass | The book fills gaps with a felt-to-craving bridge, safety guidance, and reader-facing FAQ answers. | None |
| E07 | Pass | Practice cards, checklists, and the seven-day starter path are practical tools, not abstract doctrine. | None |
| E08 | Pass | The claim ledger and chapter 11 give depth that most generic meditation handbooks lack. | None |
| E09 | Pass | The book synthesizes early discourses, commentarial material, Mahāsi teaching, research, and editorial guidance. | None |
| E10 | Pass | Later chapters point forward to safety, self-checking, and reuse rather than ending in vague inspiration. | None |

### Exp -- Experience

| ID | Status | Evidence | N/A reason |
|---|---|---|---|
| Exp01 | Fail | The handbook does not use first-person testimony or field notes; it stays impersonal and instructional. | None |
| Exp02 | Pass | Appendix B gives concrete sensory labels such as `nóng`, `lạnh`, `căng`, `rung`, `tê`, and `đau`. | None |
| Exp03 | Pass | The frontmatter and appendices document step-by-step practice, not just principles. | None |
| Exp04 | Fail | There are no photos, screenshots, timestamped logs, or other tangible proof artifacts. | None |
| Exp05 | Fail | The schedule states recommended duration but gives no verified record of how long the authors or test readers used this exact edition. | None |
| Exp06 | Partial | Chapter 9 and Chapter 11 name pain, sleep disruption, self-misreading, and overreach as real failure modes. | None |
| Exp07 | Partial | The text contrasts before/after in practice logic, but not with lived case studies. | None |
| Exp08 | Partial | The book uses numbers and thresholds, but not outcome metrics from repeated field use. | None |
| Exp09 | Fail | There is no evidence of repeated user testing or longitudinal practice logging inside the artifact. | None |
| Exp10 | Pass | `book/references/claim-ledger.md` and `book/references/editorial-depth-audit.md` explicitly name limits and exclusions. | None |

### Ept -- Expertise

| ID | Status | Evidence | N/A reason |
|---|---|---|---|
| Ept01 | Partial | The credit is consistent, but `CS Chánh Niệm` is not accompanied by a verifiable identity, biography, or scoped responsibility statement. | None |
| Ept02 | Fail | The book does not display formal credentials, degrees, or teacher verification. | None |
| Ept03 | Pass | The prose uses Pāli terms carefully and keeps them distinct from Vietnamese glosses. | None |
| Ept04 | Pass | Chapters on dependent origination, insight map, and stream-entry show real technical depth. | None |
| Ept05 | Pass | The claim ledger gives a visible method: source code, tier, strength, and caveat. | None |
| Ept06 | Pass | Safety, pain, misreading, and attainment overclaim are all handled explicitly. | None |
| Ept07 | Pass | The book separates early discourses, later Theravāda commentary, Mahāsi lineage, and modern research. | None |
| Ept08 | Pass | Chapter 11 explains why isolated experiences do not prove stream-entry. | None |
| Ept09 | Pass | The book integrates canonical, commentarial, lineage, research, and editorial layers without collapsing them. | None |
| Ept10 | Partial | The repository shows a clear internal editorial process, but there is no independent editor or reviewer label. | None |

### A -- Authority

| ID | Status | Evidence | N/A reason |
|---|---|---|---|
| A01 | N/A | Backlink profile is not observable in a static book artifact. | Site-level signal. |
| A02 | N/A | Media mentions are outside the book and not auditable here. | Site-level signal. |
| A03 | N/A | Awards are not represented in the manuscript or book build. | Site-level signal. |
| A04 | N/A | Publishing record beyond this repository is not part of the artifact. | Site-level signal. |
| A05 | N/A | Brand recognition is not measurable from the manuscript alone. | Site-level signal. |
| A06 | N/A | Social proof is not present in the book content. | Site-level signal. |
| A07 | N/A | Knowledge graph presence cannot be inferred from a book repo. | Site-level signal. |
| A08 | N/A | Entity consistency exists internally, but authority scoring here requires site/org context. | Site-level signal. |
| A09 | N/A | Partnership signals are not exposed in the book artifact. | Site-level signal. |
| A10 | N/A | Community standing is not visible inside the handbook itself. | Site-level signal. |

### T -- Trust

| ID | Status | Evidence | N/A reason |
|---|---|---|---|
| T01 | N/A | Legal-compliance surface such as privacy or terms does not exist in a static book. | Not a service site. |
| T02 | Partial | The source chapter and README link a public correction channel, but no named contact or response commitment is supplied. | None |
| T03 | N/A | Security standards are not auditable for an offline handbook artifact. | Not a service site. |
| T04 | Pass | No affiliate or sponsored commerce is present; disclosure is handled through source provenance instead. | None |
| T05 | Partial | The source contract, claim ledger, and AGENTS files function like an editorial policy, but there is no separate public policy page. | None |
| T06 | Pass | `book/chapters/99-nguon.typ` carries the checked date, public issue channel, and rule that source changes update the ledger and both deliverables; `README.md` exposes the audit trail. | None |
| T07 | N/A | There are no ads or ad placements in the book artifact. | Not a service site. |
| T08 | Pass | `book/chapters/09-an-toan.typ`, `book/chapters/11-nhap-luu.typ`, and the FAQ warn against over-reading experiences and overclaiming attainment. | None |
| T09 | N/A | The book publishes no testimonials or customer reviews whose authenticity could be assessed. | No review corpus. |
| T10 | N/A | Customer-support operations and service levels are outside the standalone book artifact. | Site or organization-level signal. |

## Top five improvements by evidential value

1. Obtain a named, scoped doctrinal review from a qualified Theravāda teacher and publish what was checked, what was not checked, and every unresolved disagreement.
2. Run `beginner-validation-protocol.md` with five unassisted true beginners. Treat any safety, retreat, or insight-map failure as release-blocking.
3. Smoke-test the final EPUB in at least one standards-based reader at 150% text size and dark mode; record app, version, device, and defects.
4. Publish a verifiable author/editor biography and responsibility split, or keep the current explicit statement that no external credential has been established.
5. After repairing failures from the first novice test, repeat with new readers and publish the results. This is stronger evidence than adding testimonials or decorative claims.

## Conclusion

This is internally publish-ready as a handbook and dual-format package. It is not independently validated and not top-1 proven. The strongest remaining work is external evidence, not more unsourced prose.
