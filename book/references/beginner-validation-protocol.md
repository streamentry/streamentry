# Beginner validation protocol

Checked: 2026-07-25

This is the cheapest test that can disconfirm the claim that the handbook is ready for a true beginner. It tests comprehension and navigation, not spiritual attainment, clinical safety, or market leadership.

Pair this protocol with [`beginner-reader-kit.md`](beginner-reader-kit.md). The kit gives the facilitator script, record sheet, and EPUB smoke-test fields so the same test can be run again without rebuilding the session from scratch.

## Participants

- Recruit 5 Vietnamese readers who have completed no retreat and no more than 5 meditation sessions.
- Do not recruit the editor, source reviewers, experienced Buddhists, or people who already know the Mahāsi vocabulary.
- Test the exact release files. Record the Git commit, PDF page count, EPUB hash, device, and reader app.

Five readers are enough to expose obvious onboarding failures. They are not enough to establish “top 1,” population safety, or superiority over other books.

## Procedure

Give no oral teaching and do not point to a page. Ask each reader to use the book to complete these tasks:

1. Find where a complete beginner should start and describe the first seven days.
2. Explain what to do during a sitting when abdominal movement remains unclear.
3. Explain what to do if practice is followed by repeated panic, increasing insomnia, derealization, or impaired daily function.
4. Explain the difference between *thọ* and a complex emotion, then describe the transition from *thọ* to *ái* in one ordinary example.
5. Decide whether “thọ to ái is always the easiest link to cut” is a canonical claim.
6. Explain how a beginner should use Chapter 10 and whether one unusual event identifies an insight stage.
7. Use Chapter 8 to reject or accept a fictional retreat whose organizer will not disclose its exit policy and pressures participants to stop medication.

After each answer, ask: “Which sentence or section in the book led you there?” Record the first answer before prompting. A correct answer reached only after a hint is not an unassisted pass.

## Release thresholds

| Gate | Passing evidence | Failure action |
|---|---|---|
| Start route | At least 4 of 5 find Chapter 1 and the early safety instruction within 90 seconds. | Rewrite navigation and the opening route. |
| Anchor fallback | At least 4 of 5 keep one fallback anchor for the rest of the session rather than cycling objects. | Rewrite the decision rule. |
| Safety | All 5 stop intensification; none interprets severe or impairing symptoms as something to push through. | Block release until the wording is repaired and retested. |
| Feeling to craving | At least 4 of 5 distinguish hedonic tone from a complex emotion and give a plausible contact-feeling-craving sequence. | Simplify Chapter 4 and retest. |
| Evidential limit | At least 4 of 5 reject “universally easiest” as unsupported by the cited discourses. | Move the caveat earlier or make it more explicit. |
| Insight map | All 5 reject self-diagnosis from one event; at least 4 of 5 identify Chapter 10 as later reference material. | Strengthen the gate and frontmatter route. |
| Retreat decision | All 5 reject the fictional retreat without negotiating away the red flags. | Strengthen the no-go rule. |

Any failure in the safety, insight-map, or retreat gate is release-blocking for the tested version. A content fix requires a new unassisted test with readers who did not see the failed wording.

## EPUB-specific pass

Repeat the start-route and section-finding tasks in at least one standards-based EPUB reader with font size increased to 150% and dark mode enabled. Verify:

- the reading order remains coherent;
- the nested table of contents reaches the introduction, chapters, and subsections;
- source badges, cautions, links, and Vietnamese diacritics remain legible;
- no text overlaps, disappears, or becomes color-dependent.

EPUBCheck success is a prerequisite, not a substitute for this reader pass.

## What would be needed for a “top choice” claim

A market claim needs a separate, preregistered comparison. At minimum, test this book blind against named Vietnamese or translated beginner alternatives using the same tasks, completion times, comprehension questions, abandonment rate, and post-reading confidence calibration. Publish negative results as well as wins. Until that evidence exists, the defensible wording is “designed and audited for beginners,” not “the number-one beginner book.”
