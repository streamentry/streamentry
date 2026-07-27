# Independent clinical-safety review protocol

Checked: 2026-07-27

This protocol defines what must exist before the edition may say that its clinical-safety material received independent review. It does not establish clinical efficacy, universal safety, diagnosis, treatment, or fitness for a particular reader.

## Reviewer boundary

Record before review:

- full legal name and public name;
- current credential, licensing or professional-registration jurisdiction, specialty, and public verification source;
- years and setting of relevant practice;
- competence in meditation-related adverse experiences, if claimed;
- research-method competence, if empirical claims are in scope;
- declared scope for mental-health risk, medication, somatic or emergency medicine, and study-participant safety;
- financial, editorial, personal, organizational, or advocacy conflicts;
- fixed compensation and payer;
- topics explicitly outside competence.

A meditation teacher is not a clinician by title. A mental-health clinician is not automatically qualified to review stroke, myocardial infarction, seizure first aid, or every medication statement. A physician reviewing somatic emergencies is not automatically qualified to assess suicide-risk wording, psychosis, dissociation, trauma, or research methods. Use more than one reviewer when no single documented scope covers all mandatory checks.

For independence, a reviewer must not be an author or editor of this edition, must not control publication approval, and must not be paid contingent on a favorable result. Fixed payment for time is permitted when disclosed.

## Artifact identity

Every report must identify:

- full candidate Git commit;
- PDF SHA-256, EPUB SHA-256 and PDF page count;
- review start and completion dates;
- files and sections reviewed;
- source editions, guidance pages and research papers consulted;
- the exact professional scope accepted by each reviewer.

Any content or artifact change after sign-off invalidates coverage of changed material. A historical review may remain public but cannot silently cover a new edition.

## Mandatory checks

Mark each item `pass`, `needs correction`, `outside scope`, or `disputed`. Items 1–10 may be split across reviewers, but none may remain `outside scope` for the broad clinical-safety-review claim.

1. R01 and R02 are described within their sampling, heterogeneity, prevalence and causal limits.
2. The book does not present meditation as harmless, as treatment, or as a substitute for clinical care.
3. Panic, insomnia, derealization, impaired function, psychosis-like warning signs and altered-state language do not become self-diagnosis or proof of an insight stage.
4. Suicide and immediate-danger wording gives an appropriate urgent response without inventing a universal hotline or replacing a full risk assessment.
5. Medication wording does not instruct readers to stop, taper or change prescribed treatment outside qualified care.
6. Stroke, myocardial-infarction and seizure first-aid claims match the cited authoritative guidance and retain country-specific emergency-number limits.
7. Grounding and breath instructions are bounded, do not promise treatment, and provide a non-breath fallback when breath attention worsens distress.
8. Pain, posture and retreat advice do not reward endurance of injury, sleep deprivation, coercion or delayed care.
9. Role boundaries between meditation teachers and health professionals are accurate and usable.
10. The beginner study's consent, distress stop, privacy, withdrawal, retention and escalation rules do not create avoidable participant harm.
11. Local emergency planning tells readers to verify current official services rather than supplying an unverified universal contact.
12. Clinical and empirical statements remain distinct from Buddhist doctrine and editorial judgment.

If the research-method portion is outside every clinician's competence, obtain a separate methods review for items 1 and 12. Describe the resulting claim as a combined scoped review, not as one person's expertise.

## Priority material

At minimum inspect:

- Chapter 1, early stop route;
- Chapter 4, feeling-to-craving intervention and the handling of pain, hunger, danger and medical needs;
- Chapter 5, especially the explicit rejection of P01's broad no-harm assurance for unbearable pain and the stay–switch–act decision rule;
- Chapter 6, sleep, persistence and object-switching safety;
- Chapter 7, especially hazardous-task attention, the priority given to immediate protection, and the instruction not to remain in threatening or violent situations;
- Chapter 8, retreat screening, medication pressure, exit rights and coercion;
- Chapter 9 in full;
- Chapter 10, depersonalization and attainment-diagnosis cautions;
- Chapter 12, map language, sleep, medication and loss-of-reality alternatives;
- safety-related FAQ and glossary entries;
- Appendix A if it is used in a real seven-day study;
- Appendix E in full, especially its immediate-danger gate, somatic warning shorthand, restart boundary and reduction rule;
- `beginner-validation-protocol.md`, `beginner-reader-kit.md`, both pilot schemas and the public aggregate-report output;
- claim-ledger rows C17, C18, C46–C52 and C72–C74;
- source-map entries R01–R09.

The reviewer should check the exact cited editions and current wording rather than relying only on the book's summary.

## Finding record

Use one record per issue:

```text
Finding ID:
Severity: blocking | major | moderate | minor
Clinical or research domain:
File and section:
Exact wording:
Evidence checked:
Potential harm mechanism:
Problem:
Required correction:
Editorial response: accepted | revised | disputed | deferred
Resolution evidence:
Reviewer disposition after correction: resolved | unresolved | not rechecked
```

`Blocking` means the wording creates a plausible immediate or serious harm route, reverses emergency guidance, encourages stopping necessary care, or materially fabricates evidence. `Major` means a central safety rule or research claim exceeds the evidence. `Moderate` means wording could misdirect a careful reader without creating the same immediate risk. `Minor` covers local clarity, terminology or citation precision.

## Signed report

The public report must contain:

```text
Reviewer:
Public qualification evidence:
License or registration jurisdiction:
Conflicts:
Compensation and payer:
Scope reviewed:
Explicit exclusions:
Artifacts:
Sources checked:
Mandatory checks completed:
Blocking findings:
Other findings:
Corrections rechecked:
Unresolved disagreements:
What this review does not establish:
Review completed:
Signature or verifiable public confirmation:
```

The broad phrase *independently reviewed for clinical safety* is permitted only when public evidence verifies the reviewers' relevant competence, the complete mandatory scope is covered, the exact artifact is bound, and no blocking or major finding remains unresolved. A narrower review supports only wording that names the exact material and domain reviewed.

Never replace this wording with *clinically validated*, *clinically proven*, *safe for everyone*, *trauma-safe*, or *medical-grade*. This protocol reviews text and procedures. It is not a clinical trial.

## Disagreement and escalation

Do not average conflicting clinical judgments into vague advice. Record the disagreement, evidence and editorial decision. When a potentially serious harm mechanism remains unresolved, retain the narrower and safer wording or keep the gate open.

If a reviewer identifies an immediate danger in the distributed candidate, stop promotion of that candidate, preserve the finding, correct the material, rebuild both artifacts, and require recheck against the new hashes.
