# Beginner validation protocol

Checked: 2026-07-27

This is the cheapest test that can disconfirm the claim that the handbook is ready for a true beginner. It tests comprehension and navigation, not spiritual attainment, clinical safety, or market leadership.

Pair this protocol with [`beginner-reader-kit.md`](beginner-reader-kit.md). The kit gives the consent script, fixed rubric, privacy and distress rules, manifest procedure, and EPUB smoke-test procedure. Record every started attempt against [`beginner-pilot-record.schema.json`](beginner-pilot-record.schema.json), enumerate it in a cohort manifest conforming to [`beginner-pilot-cohort-manifest.schema.json`](beginner-pilot-cohort-manifest.schema.json), and score only that manifest with [`../../scripts/score-beginner-pilot.py`](../../scripts/score-beginner-pilot.py).

## Participants

- Recruit up to 7 Vietnamese adults to obtain the first 5 completed eligible attempts. Do not handpick a better five after seeing results, and do not begin another attempt after the fifth eligible completion.
- Eligible readers have completed no retreat and no more than 5 meditation sessions. They have not joined an earlier pilot of this book or seen the tested passages and prompts.
- Do not recruit the editor, source reviewers, experienced Buddhists, or people who already know the Mahāsi vocabulary.
- Test the exact release files. Record the Git commit, both PDF and EPUB SHA-256 hashes, PDF page count, device, and reader app.
- Use one primary format per five-reader cohort. Do not pool PDF and EPUB comprehension results without reporting format-specific cohorts.

Five readers are enough to expose obvious onboarding failures. They are not enough to establish “top 1,” population safety, or superiority over other books.

Before attempt one, freeze the artifact and all ten contract files in one Git commit on canonical `streamentry/streamentry` history, fetch `origin/main`, record the fixed cohort rules and EPUB section-finding prompt, and set `registered_at`. Prefer an external append-only timestamped registry. At closure, enumerate every started attempt in order with its record hash. The local scorer can verify canonical origin configuration, ancestry against local `origin/main`, internal chronology and exact discovery, but it cannot prove that the remote ref was freshly fetched; a self-reported JSON timestamp also cannot independently prove preregistration or rule out omission of the terminal attempt.

## Procedure

Give no oral teaching and do not point to a page. Ask each reader to use the book to complete these eight tasks:

1. Find where a complete beginner should start and describe the first seven days.
2. Explain what to do during a sitting when abdominal movement remains unclear.
3. Explain what to do if practice is followed by repeated panic, increasing insomnia, derealization, or impaired daily function.
4. Explain the difference between *thọ* and a complex emotion, then describe the transition from *thọ* to *ái* in one ordinary example.
5. Decide whether “thọ to ái is always the easiest link to cut” is a canonical claim and identify the source badge that settles the boundary.
6. Explain how a beginner should use Chapter 12 and whether one unusual event identifies an insight stage.
7. Use Chapter 8 to reject or accept a fictional retreat whose organizer will not disclose its exit policy and pressures participants to stop medication.
8. Explain the difference between the first three fetters, the full five lower fetters, and the four fruits; identify which fruit ends the first three and which ends all five; then apply the distinctions to the four fixed scenarios in the reader kit.

After each answer, ask: “Which sentence or section in the book led you there?” Record the first answer before prompting. A correct answer reached only after a hint is not an unassisted pass.

For tasks 2 and 3, also record whether the reader independently opens Appendix E and whether the map leads to the correct detailed section. Do not name the appendix, point to it or count this observation as a substitute for any existing pass criterion. This exploratory field tests retrieval value without changing the preregistered comprehension thresholds.

## Release thresholds

Every counted pass below must be unassisted: the first answer is recorded, no hint is used, and every listed criterion is true.

| Gate | Passing evidence | Failure action |
|---|---|---|
| Start route | At least 4 of 5 find Chapter 1, describe the seven-day route, find the early safety instruction, and finish within 90 seconds. | Rewrite navigation and the opening route. |
| Anchor fallback | At least 4 of 5 choose an allowed fallback, keep one anchor, and reject needless object-cycling. | Rewrite the decision rule. |
| Safety | All 5 stop intensification, reject pushing through, and seek qualified support. | Block release until the wording is repaired and retested. |
| Feeling to craving | At least 4 of 5 distinguish hedonic tone from complex emotion, give a plausible contact-feeling-craving sequence, and keep feeling distinct from craving. | Simplify Chapter 4 and retest. |
| Evidential limit | At least 4 of 5 reject the universal “easiest” claim, identify the intervention as editorial, find the Chapter 4 caveat, and use the source badge to explain the boundary. | Move the caveat earlier or make it more explicit. |
| Insight map | All 5 reject self-diagnosis from one event; at least 4 of 5 also place Chapter 12 as later reference material and name an alternative explanation or the need for longitudinal context. | Strengthen the gate and frontmatter route. |
| Retreat decision | All 5 reject the retreat, identify the missing exit policy, and identify medication pressure and coercive authority. | Strengthen the no-go rule. |
| Fetters and fruits | At least 4 of 5 name and explain the first three fetters, distinguish them from the full five lower fetters, map the sets to Stream-entry and Non-returning, keep the four fruits distinct from DN 2's broader title, and correctly handle at least 3 of the 4 fixed scenarios. | Repair Chapters 10–11 and their reading-route handoff, then retest. |

Any failure in the safety, insight-map, or retreat gate is release-blocking for the tested version. Any distress stop is also a veto, not a replaceable missing reader. A content fix requires a new unassisted test with readers who did not see the failed wording.

The deterministic scorer selects the first five completed eligible attempts, enforces the numeric thresholds and distress veto, recursively rejects hidden record additions, verifies the exact manifest discovery and chronology, binds both artifacts and ten contract files to one canonical-history commit, checks current and reachable-history Git privacy, scans free text for likely contact data, checks retention, eligibility, consent, and the no-hint rule, and reports de-identified stop counts. That frozen artifact commit must later be an ancestor of the public-evidence commit and must itself contain the exact tested PDF and EPUB bytes; the release-evidence record may be committed later.

Run the scorer with both `--output` and `--epub-evidence-output`. The aggregate report binds `Completed`, the cohort ID, manifest SHA-256, and exactly five counted-record hashes. The reader-app report binds the same cohort and manifest plus exactly one of those five hashes. Both carry explicit public-confirmation and “does not establish” fields. These deterministic outputs do not authenticate the reader or moderator, prove that the local remote ref is fresh, independently authenticate preregistration time, or prove terminal-attempt completeness. The public gate also rejects likely private contact data, but bounded patterns cannot detect every identifier. Require human privacy review, preserve the first answer and source locator for authorized audit, and use an external registry for stronger custody evidence. A sixth reader cannot rescue a miss among the first five.

## EPUB-specific pass

With at least one of the same five counted readers, repeat the start-route task and the exact section-finding prompt frozen in the manifest. Use a standards-based EPUB reader with font size increased to 150% and dark mode enabled. Store the first answers, source locators, timings, hint states, and display checks in that reader's record. Verify:

- the reading order remains coherent;
- the nested table of contents reaches the introduction, chapters, and subsections;
- source badges, cautions, links, and Vietnamese diacritics remain legible;
- no text overlaps, disappears, or becomes color-dependent.

The scorer's bounded EPUB container check, EPUBCheck, and DAISY Ace are prerequisites, not substitutes for this reader pass.

## What would be needed for a “top choice” claim

A market claim needs a separate, preregistered comparison. At minimum, test this book blind against named Vietnamese or translated beginner alternatives using the same tasks, completion times, comprehension questions, abandonment rate, and post-reading confidence calibration. Publish negative results as well as wins. Until that evidence exists, the defensible wording is “designed and audited for beginners,” not “the number-one beginner book.”
