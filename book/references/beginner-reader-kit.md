# Beginner reader kit

Checked: 2026-07-26

This packet turns the validation protocol into a usable test session. It is not a second theory document. Its job is to make the unassisted beginner test repeatable, sparse, and hard to game.

## What this kit is for

- Run one session per reader.
- Keep the reader unassisted until the first answer is recorded.
- Record what the reader actually found, not what the facilitator hoped to hear.
- Keep the data set small enough that a failed gate can be read, discussed, and retested.

This kit does not prove spiritual attainment, market leadership, or clinical safety for every reader. It only helps disconfirm obvious onboarding failures.

## Materials

- The exact release PDF or EPUB.
- A stopwatch or phone timer.
- A blank scoring sheet.
- One line of device metadata: device, reader app, app version, and text size.
- One line of reader metadata: language comfort, previous meditation exposure, and whether the reader has ever been on retreat.

Do not ask for a full identity profile unless you need it for consent or contact. Pseudonyms are enough for the record.

## Before the session

1. Open the exact release file.
2. Set the reader app to at least 150% text size for EPUB testing.
3. For EPUB, turn on dark mode if the app supports it.
4. Tell the reader that hints will come only after the first answer is recorded.
5. Tell the reader that a wrong answer is still useful evidence if it is their first unassisted answer.

If the reader already knows the book or the Mahāsi vocabulary, do not use that session as proof of beginner comprehension.

## Facilitator script

Use this script verbatim or very close to it:

> “Please read the book by yourself. I will not point to pages or explain terms while you work. After each task, I will ask what sentence or section led you to that answer. I want your first answer, not your repaired answer.”

Do not add teaching, commentary, or hints until the first response is written down.

## What to record

For each reader, record:

- the exact file and commit hash;
- start time and finish time;
- device, app, version, and text size;
- first answer;
- whether the answer was unassisted;
- whether a hint was needed;
- what section or sentence the reader cited;
- any confusion point or safety concern;
- whether the EPUB layout, links, or reading order caused friction.

## Scoring sheet

Use one row per task. A simple five-state result is enough:

| State | Meaning |
|---|---|
| Pass | The reader answered correctly on the first unassisted try. |
| Partial | The reader found the right area but needed help or drifted off the question. |
| Fail | The reader gave the wrong answer or could not find the needed section. |
| Block | The reader showed a safety issue or a refusal condition that stops the session. |
| N/A | The task was not run, with a reason. |

Treat hints as evidence of a weaker pass, not as a clean pass.

## Suggested result template

```md
Reader:
Device:
App:
Version:
Text size:
File:
Commit:

1. Start route — Pass / Partial / Fail / Block
   First answer:
   Cited section:
   Notes:

2. Safety gate — Pass / Partial / Fail / Block
   First answer:
   Cited section:
   Notes:

3. Feeling to craving — Pass / Partial / Fail / Block
   First answer:
   Cited section:
   Notes:

4. Insight map — Pass / Partial / Fail / Block
   First answer:
   Cited section:
   Notes:

5. Retreat decision — Pass / Partial / Fail / Block
   First answer:
   Cited section:
   Notes:
```

## EPUB-specific check

Run the same start-route and section-finding tasks in at least one EPUB reader with dark mode on and font size increased. Record whether:

- the reading order stays coherent;
- headings remain reachable from the table of contents;
- source badges, cautions, and links remain legible;
- no line disappears, overlaps, or depends on color alone.

If the EPUB fails this smoke test, fix the file before claiming the book is ready for beginners.

## Reporting rule

Publish both the successes and the failures. A failed task is still useful if it shows exactly where a beginner got lost.
