# Attainment source audit

Checked: 2026-07-27

## Purpose and boundary

This annex audits the load-bearing source claims in Chapters 10 and 11: the
first three fetters, the five lower fetters, the four fruits, the
four-pairs/eight-persons formula, and the wider use of “fruits of the ascetic
life” in DN 2. It is designed to let a reviewer test the book at passage level
without first reconstructing the claim map.

The audit uses the SuttaCentral `bilara-data` repository frozen at commit
[`3af91efb1099190c74998247177f8ba6a076b8c0`](https://github.com/suttacentral/bilara-data/tree/3af91efb1099190c74998247177f8ba6a076b8c0).
Segment IDs below refer to that immutable snapshot. The Pāli root and Bhikkhu
Sujato's English translation were checked together where both are listed. This
additional translation check does not replace the editions recorded in
`claim-ledger.md`.

This is an internal source audit. It can find textual mismatch and interpretive
overreach. It cannot establish attainment, authenticate a person's spiritual
status, settle every Theravāda interpretation, or replace the independent
review required by `doctrinal-review-protocol.md`.

## Verdict vocabulary

- **Direct · PASS:** the cited segments state the load-bearing proposition.
- **Editorial synthesis · PASS WITH BOUNDARY:** the book joins or explains
  source material in its own words and labels that move as editorial.
- **Evidential limit · PASS WITH BOUNDARY:** the sources support a narrower
  statement or fail to support a tempting stronger claim; the book preserves
  that limit.

## Segment-level matrix

| Question tested | Frozen source and segments | Claim class | Internal verdict | What the passage does not establish |
|---|---|---|---|---|
| Which three fetters are abandoned through vision? | [MN 2 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/mn/mn2_root-pli-ms.json), 11.1–11.4; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/mn/mn2_translation-en-sujato.json), 11.1–11.4 | Direct | **PASS.** The passage names identity view, doubt, and misapprehension of precepts and observances after wise attention to the four noble truths. | It does not define a checklist for diagnosing another person, nor say that memorizing the truths abandons the fetters. |
| What are the five lower fetters? | [AN 10.13 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/an/an10/an10.13_root-pli-ms.json), 1.3–2.3; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/an/an10/an10.13_translation-en-sujato.json), 1.3–2.3 | Direct | **PASS.** The first three are followed by sensual desire and ill will. Chapter 11 preserves one five-item group rather than inventing a separate canonical group called “the three lower fetters.” | A list alone does not show how to determine that a fetter has been eradicated. |
| How do the first three and five lower fetters map to the first three fruits? | [AN 3.88 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/an/an3/an3.88_root-pli-ms.json), 2.6–2.15; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/an/an3/an3.88_translation-en-sujato.json), 2.6–2.15 | Direct | **PASS.** Ending three fetters maps to Stream-entry; ending three while attenuating greed, hate, and delusion maps to Once-returning; ending five lower fetters maps to Non-returning. | A calm period is not eradication, one angry episode is not a complete attainment diagnosis, and attenuation is not identical with ending the five lower fetters. |
| What does identity view take as self or as related to self? | [MN 44 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/mn/mn44_root-pli-ms.json), 2.3–8.8; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/mn/mn44_translation-en-sujato.json), 2.3–8.8 | Direct | **PASS.** Bhikkhunī Dhammadinnā identifies the five clinging-aggregates as *sakkāya* and analyzes identity view by four relations to each aggregate. | Ordinary use of “I,” personality, responsibility, or a fleeting self-referential thought is not by itself the technical fetter. |
| Why is seeing not-self directly relevant to abandoning identity view? | MN 44 Pāli, 7.1–8.8; [SN 22.59 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/sn/sn22/sn22.59_root-pli-ms.json), 2.1–10.1; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/sn/sn22/sn22.59_translation-en-sujato.json), 2.1–10.1 | Direct plus bounded editorial inference | **PASS WITH BOUNDARY.** MN 44 defines the view by appropriation of each aggregate in four self-relations. SN 22.59 denies full command over the aggregates, points to impermanence and change, and instructs that all five be seen with right wisdom as not mine, not I, and not my self. Chapter 11 labels the incompatibility between these two modes of seeing as its explanatory bridge. | Neither passage says that intellectual agreement, formula repetition, a transient selfless state, denial of responsibility, or depersonalization proves eradication. MN 2 places the abandoning of all three fetters after wise attention to all Four Noble Truths. |
| Does ending identity view end every residue of “I am”? | [SN 22.89 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/sn/sn22/sn22.89_root-pli-ms.json), 5.8–5.9 and 11.1–12.13; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/sn/sn22/sn22.89_translation-en-sujato.json), same segments | Evidential limit | **PASS WITH BOUNDARY.** Khemaka does not regard an aggregate as self or owned by self, yet a residual “I am” conceit, desire, and tendency remain; the discourse explicitly speaks of this residue after the five lower fetters are ended. | Ending identity view cannot be inflated into the claim that every form of conceit or self-reference has ended at Stream-entry. |
| Is a latent tendency the same as a currently arisen fetter? | [MN 64 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/mn/mn64_root-pli-ms.json), 2.5–6.19; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/mn/mn64_translation-en-sujato.json), 2.5–6.19 | Direct | **PASS.** The discourse distinguishes underlying tendency from an arisen fetter that overcomes and enslaves the mind, and says that abandoning a lower fetter also abandons its underlying tendency. | The temporary absence of a thought does not prove eradication; an ordinary preference, irritation, or question does not automatically prove that a fetter is actively enslaving the mind. |
| Are the sense faculty and its object themselves the fetter? | [SN 41.1 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/sn/sn41/sn41.1_root-pli-ms.json), 4.10–4.18; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/sn/sn41/sn41.1_translation-en-sujato.json), 4.10–4.18 | Direct | **PASS.** The discourse locates the fetter in the desire and greed arising dependent on the pair, not in the faculty or object by itself. | Seeing, hearing, using a pleasant object, setting a safety boundary, or making a firm refusal does not by itself establish sensual desire or ill will as an eradication-level diagnosis. |
| Is the book's explanation of *sīlabbataparāmāsa* a quotation or a bounded gloss? | MN 2, 11.1–11.4; [MN 57 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/mn/mn57_root-pli-ms.json), 2.1–5.5; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/mn/mn57_translation-en-sujato.json), 2.1–5.5 | Editorial synthesis | **PASS WITH BOUNDARY.** Chapter 10 labels as editorial its working explanation: mistaking a precept, observance, ritual, austerity, or technique for a sufficient cause or guarantee of liberation. MN 57 supplies a bounded case of strenuous observance joined to wrong view. | Neither discourse gives the book's sentence as an exhaustive dictionary definition. Ethical precepts, useful ritual, and disciplined technique are not themselves the fetter. |
| Does canonical doubt mean every question or source check? | MN 2, 11.1–11.4; [DN 16 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/dn/dn16_root-pli-ms.json), 2.9.3–2.9.8 and 6.6.11–6.6.12; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/dn/dn16_translation-en-sujato.json), same segments | Evidential limit | **PASS WITH BOUNDARY.** DN 16 frames doubt around Buddha, teaching, Saṅgha, path, and practice and gives the mirror of Dhamma in terms of confirmed confidence and ethical qualities. The book therefore refuses to label every careful question as the fetter. | This negative limit does not make every question wise, nor does confidence by itself prove Stream-entry. |
| Does the three-level explanation turn the fetters into a canonical sequence or three separate techniques? | MN 2, 11.1–11.4; MN 44, 2.3–8.8; MN 57, 2.1–5.5 | Editorial synthesis | **PASS WITH BOUNDARY.** Chapter 10 labels its “object, basis, means” frame and meditation case as editorial. It explicitly says MN 2 does not present a 1–2–3 eradication sequence and returns the reader to wise attention to all Four Noble Truths and the whole Noble Eightfold Path. | The sources do not state the book's three-level wording, do not say knee pain causes the fetters, and do not authorize diagnosing eradication from handling one event well. |
| What is the path and what are its four fruits? | [SN 45.35 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/sn/sn45/sn45.35_root-pli-ms.json), 1.4–1.10; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/sn/sn45/sn45.35_translation-en-sujato.json), 1.4–1.10; [SN 45.36 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/sn/sn45/sn45.36_root-pli-ms.json), 1.4–1.10 | Direct plus editorial synthesis | **PASS WITH BOUNDARY.** SN 45.35 identifies the Noble Eightfold Path as the ascetic life and lists Stream-entry, Once-returning, Non-returning, and Arahantship as its fruits. SN 45.36 names ending greed, hate, and delusion as its goal. “One path with four result milestones” is visibly the book's synthesis. | The passages do not identify a noting method, breath exercise, retreat length, or unusual experience as the whole path or as proof of a fruit. |
| Are “practicing for a fruit” and “realizing a fruit” distinct? | [Ud 5.5 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/kn/ud/vagga5/ud5.5_root-pli-ms.json), 26.2; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/kn/ud/vagga5/ud5.5_translation-en-sujato.json), 26.2; [SN 48.18 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/sn/sn48/sn48.18_root-pli-ms.json), 1.3–1.6; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/sn/sn48/sn48.18_translation-en-sujato.json), 1.3–1.6 | Direct plus evidential limit | **PASS WITH BOUNDARY.** The sources distinguish each achiever from one practicing to realize that fruit; SN 48.18 places the distinction in a graded account of the five faculties. | Wanting a fruit, following the book, or calling oneself “on the way” does not establish the technical practicing category. These passages do not by themselves establish a later moment-by-moment theory of path and fruition consciousness. |
| Does the four-pairs/eight-persons formula have early-discourse support? | Ud 5.5, 26.2; [AN 10.92 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/an/an10/an10.92_root-pli-ms.json), 5.6–5.9; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/an/an10/an10.92_translation-en-sujato.json), 5.6–5.9 | Direct | **PASS.** AN 10.92 explicitly gives four pairs and eight individuals, while Ud 5.5 enumerates the eight positions. | The formula is not an invitation to rank living people from surface behavior. |
| Does “Sa-môn quả” in DN 2 mean only the standard four-fruit list? | [DN 2 Pāli](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/root/pli/ms/sutta/dn/dn2_root-pli-ms.json), 11.1–14.5 and 97.1–98.9; [translation](https://github.com/suttacentral/bilara-data/blob/3af91efb1099190c74998247177f8ba6a076b8c0/translation/en/sujato/sutta/dn/dn2_translation-en-sujato.json), same segments | Direct plus evidential limit | **PASS WITH BOUNDARY.** DN 2 asks about fruits of the ascetic life visible here and now, unfolds a broad progressive training, and culminates in ending the effluents and knowing liberation. Chapter 11 separates that discourse-wide use from SN 45.35's four-fruit classification. | The title of DN 2 is not a lexical proof that every benefit described there is one of the four noble fruits, nor that the phrase always means only those four. |
| Do the early discourses allow lay attainment and a bounded mirror for self-reflection? | DN 16, 2.7.2–2.9.8 and 6.6.11–6.6.12 | Direct plus evidential limit | **PASS WITH BOUNDARY.** DN 16 reports lay Stream-enterers, Once-returners, and Non-returners and presents the mirror of Dhamma. Chapter 10 uses that mirror as a source-bounded reflection, not a one-event test. | Lay status is not an obstacle in these passages, but a reader's self-report is not thereby authenticated and the mirror does not turn the editor into an attainment certifier. |

## Adversarial reading tests

The following substitutions would make Chapters 10–11 easier to market and
less accurate. The current text rejects each one:

1. **“I still use the word ‘I,’ so identity view cannot have ended.”** This
   confuses ordinary language and residual conceit with the twentyfold
   aggregate relation analyzed in MN 44.
2. **“I asked for evidence, so I have fetter-doubt.”** The sources do not equate
   every careful question with *vicikicchā*.
3. **“I keep precepts strictly, so I cling to rites and observances.”** The
   error is not ethical discipline itself but the misapprehension assigned to
   the means.
4. **“I felt no sensual desire or ill will during retreat, so the last two
   lower fetters ended.”** Temporary non-arising is not eradication.
5. **“I became angry once, so a claimed Stream-entry is disproved.”** Anger is
   relevant to the later fetters, but one episode alone does not test whether
   the first three have ended or determine the precise degree of attenuation.
6. **“I know the 3–5–4 chart, so I have entered the path.”** Classification
   knowledge is not one of the cited attainment criteria.
7. **“This meditation technique is the stream.”** SN 45.35 and the book identify
   the path as the whole Noble Eightfold Path, not one exercise.
8. **“I agree that everything is not-self, so identity view has been
   eradicated.”** Agreement with a proposition is not the right-wisdom seeing
   specified in SN 22.59 and does not establish the three-fetter result stated
   in MN 2.
9. **“A cessation, light, bliss, retreat duration, or teacher verdict proves a
   fruit.”** None of the audited passages supplies that sufficiency rule.

## Internal conclusion and open gate

No contradiction was found between the audited load-bearing claims and the
frozen passages. Chapters 10 and 11 correctly distinguish:

- the first three fetters from the complete five lower fetters;
- temporary absence, attenuation, and eradication;
- a person practicing for a fruit from one who has realized it;
- the standard four fruits from DN 2's broader discourse on fruits of the
  ascetic life;
- direct discourse claims from editorial explanation and evidential limits.

This conclusion is deliberately narrower than “doctrinally validated.” The
independent Theravāda review remains **OPEN** until a qualified, independent
reviewer checks the frozen artifacts, records findings and disputes, and signs
the candidate-bound report required by `doctrinal-review-protocol.md`.
