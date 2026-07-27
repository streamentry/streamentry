# Independent doctrinal review protocol

Checked: 2026-07-26

This protocol turns “reviewed by a Theravāda expert” into a claim that can be audited. It does not manufacture endorsement. Until a named reviewer completes and signs the report for exact artifact hashes, the book must continue to say that no independent doctrinal review has been established.

## Reviewer boundary

Record all of the following before review:

- full name and the public name to be printed;
- current role, lineage or institutional affiliation, and years of relevant study or teaching;
- languages used to check sources;
- any financial, editorial, personal, or institutional conflict;
- whether the reviewer is evaluating source fidelity, Theravāda orthodoxy, pedagogy, or all three;
- topics explicitly outside the reviewer's competence.

A respected meditation teacher is not automatically a Pāli textual specialist. A Pāli scholar is not automatically qualified to assess clinical safety. Publish the scope actually reviewed, not the larger status suggested by a title.

For a review to count as *independent*, the reviewer must not be an author or editor of this edition, must not have approval power over its publication, and must not receive compensation contingent on a favorable verdict. Fixed compensation for review time is allowed only when its amount and payer are disclosed. A close financial, organizational, or personal stake in the book disqualifies the broad independence claim; the person's comments may still be published as attributed consultation.

For the broad phrase *independently doctrinally reviewed*, public evidence must verify relevant Theravāda doctrinal competence and sustained work with the early discourses or their source languages. A narrower qualification supports only a narrower claim, such as “Chapter 10 reviewed for Pāli terminology.” Name, prestige, ordination, or years of meditation alone do not satisfy this gate.

## Artifact identity

The report must identify:

- full Git commit;
- PDF SHA-256 and page count;
- EPUB SHA-256;
- review start and completion dates;
- chapters and appendices reviewed;
- source editions or translations consulted.

Any content change after sign-off creates a new artifact. The old report may still be cited as historical review, but it cannot silently cover changed claims.

## Required source-tier checks

The reviewer must mark each item `pass`, `needs correction`, `outside scope`, or `disputed`:

1. Early discourse claims are supported by the cited passage, speaker, and context.
2. Later Theravāda exegesis is not presented as a verbatim early discourse.
3. *Visuddhimagga* claims are attributed to the text rather than to the Buddha.
4. Mahāsi instructions are traceable to P01 or P02 and are not universalized to all Theravāda practice.
5. Editorial schedules, examples, decision rules, and safety advice remain visibly editorial.
6. Modern research is used only within the study design's evidential limits.
7. The twelve links are not reduced without notice to a purely momentary psychological model.
8. The insight map is not described as a numbered list spoken by the Buddha.
9. The first three fetters, five lower fetters, four fruits, and DN 2's broader title remain distinct.
10. No isolated cessation, light, bliss, teacher verdict, or retreat duration is treated as sufficient evidence of Stream-entry.

Items 1–5 and 7–10 are mandatory for the broad doctrinal-review claim and may not be marked `outside scope`. Item 6 may be outside a doctrinal reviewer's competence, but that limit must remain prominent and the research and clinical-safety claims need their own qualified review before any broader expert-validation claim. A partial review may still be useful; describe it by exact chapter and question instead of using the broad phrase.

## Priority passages

At minimum, review:

- Chapter 2, the canonical frame for Stream-entry;
- Chapter 3, the treatment of the four establishments of mindfulness;
- Chapter 4, all twelve links and the feeling-to-craving intervention;
- Chapter 5, the boundary between MN 10 and Mahāsi technique, the editorial operationalization of “salient,” and the accurate disclosure of P01's internally different pain instructions;
- Chapter 7, the boundary between ordinary clear comprehension, lay duties, ethical restraint, and the book's editorial attention, collision, and repair loops;
- Chapter 8, the seven-day passage and retreat claims;
- Chapter 10, the first three fetters and mirror of Dhamma;
- Chapter 11, the five lower fetters, four fruits, four-pairs/eight-persons formula, and DN 2 distinction;
- Chapter 12, the seven purifications and progress-of-insight map;
- Appendix C, because direct answers are likely to be quoted without surrounding caveats;
- Appendix D, because glossary definitions can harden an editorial gloss into an apparent doctrine;
- the complete claim ledger and source map.
- the frozen passage matrix in `attainment-source-audit.md`, checking its
  segment selections against the cited editions rather than treating the
  internal verdicts as external findings.

## Finding record

Use one record per finding:

```text
Finding ID:
Severity: blocking | major | moderate | minor
File and section:
Exact claim:
Source checked:
Problem:
Required correction:
Editorial response: accepted | revised | disputed | deferred
Resolution evidence:
Reviewer disposition after correction: resolved | unresolved | not rechecked
```

`Blocking` means the published text materially misattributes, fabricates, or reverses a load-bearing doctrinal claim. `Major` means a central claim outruns its source or collapses source tiers. `Moderate` means wording can mislead a careful beginner but does not reverse the doctrine. `Minor` covers terminology, translation preference, or local clarity.

## Signed report

The public report must contain:

```text
Reviewer:
Qualifications and public evidence:
Conflicts:
Scope reviewed:
Artifacts:
Sources and languages:
Blocking findings:
Other findings:
Corrections rechecked:
Unresolved disagreements:
What this review does not establish:
Review completed:
Signature or verifiable public confirmation:
```

The phrase “independently doctrinally reviewed” is permitted only when all of the following are true: qualifications are publicly verifiable; the independence gate above passes; the exact artifact is identified; every mandatory source-tier check and priority passage is completed; and no blocking or major finding remains unresolved. Any narrower scope requires equally narrow wording that names what was checked. The phrase does not mean clinically safe, suitable for every Buddhist tradition, guaranteed to produce attainment, independently tested with beginners, or superior to other books.

## Disagreement rule

Do not average conflicting interpretations into vague prose. Record the disagreement, the sources each side relies on, and the editorial choice. Prefer narrower wording when the evidence does not settle the issue. If a central claim remains genuinely disputed, keep the disagreement visible in the report and avoid advertising the passage as settled doctrine.
