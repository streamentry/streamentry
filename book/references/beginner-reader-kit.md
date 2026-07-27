# Beginner reader test kit

Checked: 2026-07-26

This kit operationalizes [`beginner-validation-protocol.md`](beginner-validation-protocol.md). It tests whether true beginners can find and correctly use the book without oral teaching. It does not test attainment, clinical efficacy, comparative market leadership, or whether every reader can practice safely.

Use the exact committed release files. One cohort tests one primary format so format effects are not silently pooled. To claim both formats pass comprehension, run a separate cohort for each format. The minimum release gate remains the first five completed eligible attempts in one cohort, plus an EPUB smoke test performed by one of those same five readers and stored in that reader's record.

## Files

- Cohort-manifest schema: [`beginner-pilot-cohort-manifest.schema.json`](beginner-pilot-cohort-manifest.schema.json)
- Attempt-record schema: [`beginner-pilot-record.schema.json`](beginner-pilot-record.schema.json)
- Deterministic scorer: [`../../scripts/score-beginner-pilot.py`](../../scripts/score-beginner-pilot.py)
- One cohort directory: `build/beginner-pilot/<cohort-id>/`, which is ignored by Git
- Direct record children only: `build/beginner-pilot/<cohort-id>/records/*.json`
- Final manifest: `build/beginner-pilot/<cohort-id>/manifest.json`

All completed and stopped attempts go in the same `records/` directory and in one exact manifest order. Do not use separate optional folders or globs: that would reopen an omission path. Do not commit raw participant records. Publish only the scorer-produced aggregate and reader-app reports with artifact hashes, bounded cohort bindings, gate results, limitations, and privacy-coarsened environment evidence. Raw free text requires separate human privacy review before any narrative theme is published.

## Roles and materials

Prefer a moderator who did not write the tested passages. If an editor moderates, record that limitation. The moderator needs:

- the exact release PDF and EPUB;
- the Git commit, both SHA-256 hashes, and PDF page count;
- a timer;
- a device and reader app whose name and version can be recorded;
- one JSON attempt record per person who starts after consent;
- Python with the `jsonschema` package for final validation and scoring.

Record only a non-personal device model or class plus operating-system version, such as `iPhone 15, iOS 19`. Never copy a personalized device name, account name, hostname, or owner name into `device`, `reader_app`, or `reader_app_version`.

The moderator must not explain Buddhist terms, point to pages, complete an answer, praise a direction, or signal that an answer is correct. A neutral request for the sentence or section used is part of the task, not a hint.

## Freeze the cohort before attempt one

Before recruitment:

1. Commit the exact source, PDF, EPUB, both schemas, protocol, reader kit, scorer, and scoring modules to the canonical `streamentry/streamentry` repository. Fetch `origin/main`; the scorer requires the artifact commit to be in that local canonical history and rejects another `repo_root`. The later public-evidence commit may differ, but this frozen artifact commit must remain its ancestor and must itself contain the exact tested PDF and EPUB bytes.
2. Choose a cohort ID, one primary format, `target_completed: 5`, `max_started_attempts: 7`, and `selection_rule: first_five_completed_eligible`.
3. Freeze this EPUB section-finding prompt in the manifest header:

   > Trong EPUB, hãy dùng mục lục hoặc liên kết để tìm mục “Ba kiết sử đầu: ba mối trói phải rơi” ở Chương 10, rồi chỉ ra nhãn nguồn của đoạn kinh đầu tiên ngay dưới mục ấy.

4. Record `registered_at`, artifact identity, the Git commit, and the SHA-256 hash of each of the ten contract files named by the schema. Prefer an external append-only timestamped registry or signed timestamp for this header.
5. Do not start attempt one until the header is frozen.

At closure, add every started attempt in chronological order with its record path and SHA-256, set `closed_at`, and retain the frozen header unchanged. A local JSON timestamp alone cannot prove that the header existed before recruitment or that the final attempt was not omitted. The scorer reports this limit; an external append-only registry is required for stronger custody evidence.

## Eligibility

Count a reader only if all are true:

- the reader is at least 18 years old;
- Vietnamese reading comfort is native or fluent;
- no retreat has been completed;
- lifetime meditation exposure is no more than five sessions;
- the reader has not read this edition;
- the reader has not participated in an earlier pilot of this book;
- the reader has not seen the tested passages or prompts;
- the reader does not already know Mahāsi vocabulary;
- the reader is not an experienced Buddhist practitioner, editor, or source reviewer.

Screen before testing. If a person is ineligible, thank them and do not include their session in the five-reader cohort.

## Consent and privacy script

Read this before collecting data:

> Chúng tôi đang kiểm tra cuốn sách, không kiểm tra kiến thức hay khả năng tu tập của bạn. Bạn sẽ tự tìm câu trả lời trong sách. Câu trả lời sai vẫn có ích vì cho thấy sách cần sửa ở đâu. Bạn có thể bỏ qua câu hỏi hoặc dừng bất cứ lúc nào, không cần nêu lý do. Phiên này không yêu cầu bạn thiền và không cung cấp chẩn đoán hay lời khuyên y khoa. Chúng tôi chỉ lưu mã người đọc, điều kiện tuyển chọn, câu trả lời và dữ liệu thiết bị; không lưu tên, số điện thoại, địa chỉ hay tài khoản cá nhân. Nếu bạn dừng sau khi bắt đầu, chúng tôi chỉ giữ bản ghi ẩn danh tối thiểu cần để không xóa dấu vết một lần thử; khi có đau khổ hoặc bạn yêu cầu rút câu trả lời, nội dung trả lời và ghi chú sẽ bị xóa. Kết quả công bố chỉ ở dạng tổng hợp và ẩn danh. Bạn có đồng ý tiếp tục không?

Record only an explicit yes. Refusal before collection is not a started attempt and creates no record. After a consenting reader starts, any stop creates a minimal attempt record so the cohort cannot silently erase a failure. If the person requests full deletion rather than answer erasure, comply; the missing attempt invalidates that cohort, and a fresh cohort must use a new manifest.

Use a random reader code. Do not put names, contact details, health histories, workplace names, exact addresses, or account identifiers in answers or notes. The validator rejects likely email addresses and phone numbers, but that bounded pattern check cannot detect every name, address or sensitive disclosure; the moderator must still review raw text before closure. Delete each raw pseudonymous record within 90 days of collection or 30 days after the final aggregate report, whichever comes first. Keep only the two public scorer reports and artifact hashes.

## Stop categories and task states

Use exactly one structured `stop_category`: `none`, `distress`, `withdrawal`, `technical`, `ineligible_after_start`, or `moderator_abort`. Each of the eight tasks must have one explicit outcome:

Use only the matching fixed `stop_reason` code: empty for `none`; `distress_stop`; `reader_withdrew`; `technical_failure`; `eligibility_rule_failed`; or `moderator_aborted`. Never place a narrative, diagnosis or disclosure in `stop_reason`.

- `answered`: preserve the first answer, source locator, elapsed time, hint state, and fixed criteria;
- `skipped`: keep answer and source fields blank and record only a bounded non-identifying reason;
- `not_reached`: keep answer, source, hint, and criteria evidence blank or false, with zero elapsed time.

This is a reading test, not a meditation exercise. Do not ask the reader to reproduce altered states or disclose trauma. Stop immediately if the reader becomes distressed or confused about reality. Do not probe for details. Set `stopped_early: true`, use `stop_category: distress`, erase all task answers and notes by marking every task `not_reached`, and set `epub_smoke` to `null`.

Any distress attempt is a release veto for that candidate. Do not recruit a later reader to rescue it. Repair the material, rebuild to new hashes, and use a fresh cohort. Other stopped or ineligible attempts remain in manifest order, do not count toward the five, and consume one of the maximum seven started attempts.

## Opening script

Read this verbatim:

> Bạn hãy dùng cuốn sách để trả lời tám tình huống. Tôi sẽ không chỉ trang hoặc giải thích thuật ngữ trước khi câu trả lời đầu tiên được ghi lại. Sau mỗi câu, tôi sẽ hỏi câu hoặc mục nào trong sách đã dẫn bạn đến câu trả lời ấy. Chúng tôi đang tìm lỗi của sách, không chấm điểm bạn.

Start the timer only after the task is read. Record the first answer before any follow-up.

## Eight tasks and fixed rubric

### 1. Start route

Prompt:

> Một người chưa từng thiền nên bắt đầu ở đâu, bảy ngày đầu làm gì, và chỉ dẫn an toàn sớm nhất nằm ở đâu?

Pass criteria:

- finds Chapter 1;
- describes the seven-day route without inventing a retreat schedule;
- finds the early safety instruction;
- completes the search within 90 seconds;
- uses no hint.

### 2. Anchor fallback

Prompt:

> Trong lúc ngồi, chuyển động bụng vẫn không rõ. Sách bảo làm gì tiếp theo? Sau khi chọn phương án thay thế, có nên đổi liên tục sang đối tượng khác không?

Pass criteria:

- selects one fallback anchor allowed by the book;
- keeps that anchor for the rest of the sitting unless safety requires stopping;
- rejects cycling through objects merely because clarity is imperfect;
- uses no hint.

### 3. Safety

Prompt:

> Sau vài ngày tăng thời lượng, một người bị hoảng sợ lặp lại, mất ngủ nặng dần, cảm giác môi trường không thật và khó làm việc. Sách bảo họ làm gì?

Pass criteria:

- stops intensifying practice;
- does not reinterpret impairing symptoms as a stage to push through;
- seeks appropriate qualified support and uses the book's urgent-safety boundary;
- uses no hint.

Any reader who recommends pushing through fails the release-blocking safety gate.

### 4. Feeling to craving

Prompt:

> “Thọ” khác một cảm xúc phức hợp thế nào? Hãy dùng một ví dụ đời thường để kể chuỗi xúc, thọ, ái.

Pass criteria:

- identifies *thọ* as pleasant, painful, or neutral tone rather than the whole emotion;
- gives a plausible contact-to-feeling-to-craving sequence;
- keeps craving distinct from the initial feeling;
- uses no hint.

### 5. Evidential limit

Prompt:

> Có thể nói “thọ đến ái luôn là mắt xích dễ cắt nhất” là lời kinh hay chân lý áp dụng cho mọi người không? Dấu nguồn nào trong sách giúp bạn phân biệt lời kinh với đề nghị biên soạn?

Pass criteria:

- rejects the universal “easiest” claim;
- identifies the exercise as an editorially useful intervention point rather than a canonical ranking;
- cites the caveat in Chapter 4;
- uses the `BIÊN SOẠN` badge or the source-tier legend to explain why the exercise is not attributed to the Buddha;
- uses no hint.

### 6. Insight map

Prompt:

> Một người có ánh sáng mạnh, hỷ lạc và một khoảng trống ký ức trong một buổi thiền. Chương 12 có cho phép họ xác định mình đang ở tuệ nào hoặc đã chứng quả không? Người mới nên dùng chương này vào lúc nào?

Pass criteria:

- rejects stage or attainment diagnosis from one event;
- treats Chapter 12 as later reference material, not the beginner's first route;
- names at least one alternative explanation or the need for longitudinal context;
- uses no hint.

The release gate separately requires all five to reject self-diagnosis. At least four must also place Chapter 12 correctly and name an alternative explanation or the need for longitudinal context.

### 7. Retreat decision

Prompt:

> Một khóa thiền không công bố cách rời khóa, gây áp lực buộc người tham dự ngừng thuốc và nói rằng nghi ngờ người hướng dẫn là chướng ngại phải vượt. Theo Chương 8, có nên tham dự không?

Pass criteria:

- rejects the retreat without negotiating away the red flags;
- identifies the missing exit policy;
- identifies medication pressure and coercive authority as no-go signals;
- uses no hint.

Any acceptance fails the release-blocking retreat gate.

### 8. Fetters and fruits

Prompt:

> “Ba kiết sử đầu”, “năm hạ phần kiết sử” và “bốn quả Sa-môn” khác nhau thế nào? Vì sao thấy vô ngã liên hệ trực tiếp với thân kiến, và chỉ đồng ý câu “vô ngã” có đủ chứng minh thân kiến đã đoạn không? Quả nào đoạn ba kiết sử đầu, quả nào đoạn đủ năm? *Kinh Sa-môn quả* DN 2 có chỉ là một bảng bốn tên ấy không?

Sau câu trả lời đầu tiên, đưa nguyên văn bốn tình huống này và hỏi mỗi tình huống cho thấy điều gì, không cho thấy điều gì:

1. Một người yêu cầu xem nguồn kinh và kiểm tra năng lực của người dạy trước khi làm theo.
2. Một người giữ giới nhưng tin rằng chỉ cần hoàn tất đúng nghi thức thì giải thoát chắc chắn xảy ra.
3. Một người rời tình huống bị bạo hành và đặt ranh giới rõ, nhưng không muốn trả đũa hay làm hại.
4. Một người xem ký ức và quan điểm của mình là một lõi bất biến phải bảo vệ bằng mọi giá.

Pass criteria:

- names identity view, doubt, and clinging to precepts-observances as the first three fetters, explains each in plain language, and correctly handles at least 3 of the 4 fixed scenarios;
- explains that identity view appropriates the five aggregates as self or as related to self, while seeing them as not mine, not I, and not my self directly opposes that view; rejects intellectual agreement, formula repetition, or a transient selfless state as proof of eradication;
- distinguishes the three levels in its own words: what is appropriated as self, whether the path has a verified basis, and whether a means has been mistaken for a sufficient cause; rejects treating them as three surface habits or three sequential tricks;
- explains that sensual desire and ill will complete the five lower fetters;
- maps the first three to Stream-entry and all five to Non-returning;
- distinguishes the four fruits from DN 2's broader discourse title and training sequence;
- uses no hint.

For the frozen record, mark `names_first_three_fetters` true only when the first bullet, including the 3-of-4 scenario requirement, passes. Preserve the response to each scenario in the first-answer field; do not replace it with a moderator summary.

## Recording rule

For every task, record:

- whether the first answer was recorded;
- the first answer itself;
- the section or sentence the reader used;
- elapsed seconds;
- whether a hint was used;
- each fixed criterion as true or false;
- a short, non-identifying note.

A hinted answer is not an unassisted pass. A correct answer without a source locator is not a full pass. Do not repair the first-answer field after discussion.

The counted cohort is not a handpicked set. It is the first five chronologically completed eligible attempts among no more than seven total starts. Do not start another attempt after the fifth eligible completion. A `skipped` or `not_reached` task prevents the all-tasks-answered release gate from passing; a sixth completion cannot rescue a miss among the first five.

## EPUB smoke test

Run this on at least one of the five counted readers in a standards-based EPUB reader at 150% or greater text size with dark mode enabled. Store the result in that reader's `epub_smoke` field. With the same reader, repeat the start-route task and the manifest-frozen section-finding prompt. Record the first answer, source locator, elapsed time, hint state, and pass decision for both repeats. The repeated start route must remain unassisted and finish within 90 seconds.

Also record app, version, device, text scale, and whether:

- reading order remains coherent;
- the nested table of contents reaches the introduction, chapters, and subsections;
- source badges, cautions, links, and Vietnamese diacritics remain legible;
- no text overlaps or disappears;
- no meaning depends on color alone.

The scorer performs a bounded ZIP, mimetype, container, and package check. EPUBCheck and DAISY Ace are still prerequisites, not substitutes for this human-reader pass.

## Scoring and release decision

After closure, set each record's `delete_by` to the earlier of 90 days after that attempt started or 30 days after `closed_at`. Hash every record, add all five to seven attempts to the manifest in chronological order, and run only the manifest:

```sh
python3 scripts/score-beginner-pilot.py build/beginner-pilot/<cohort-id>/manifest.json \
  --output build/beginner-pilot/<cohort-id>/aggregate-report.md \
  --epub-evidence-output build/beginner-pilot/<cohort-id>/reader-app-report.md
```

The aggregate output records `Completed`, a scope-limit statement, the cohort ID, manifest SHA-256, and exactly five unique counted-record hashes. The `--epub-evidence-output` file carries the same cohort and manifest binding plus exactly one of those five record hashes. Both include a deterministic public-confirmation line, but neither authenticates a human signer.

The scorer refuses a drifting contract, an unexpected repository or origin, an artifact commit outside local `origin/main` history, uncommitted or mismatched artifacts, record additions or omissions, nested record directories, raw pilot data found in current Git tracking or reachable Git history, contradictory order, more than seven starts, a start after the fifth eligible completion, duplicate readers, overdue raw records, likely contact data, ineligible counted readers, missing consent, malformed EPUB structure, or invalid task states. It exits `0` for a valid PASS, `1` for a valid but failed cohort, and `2` for invalid evidence. Public gate verification also rejects likely private email addresses or phone numbers in submitted evidence. The public reports never include first answers or free-text notes; the aggregate report suppresses environment cells smaller than two.

Passing this cohort supports only: “This exact committed artifact passed the defined first-five beginner gate under the recorded local manifest.” The local origin and ancestry checks do not prove that `origin/main` was freshly fetched; verify the reported commit against public canonical history. Without an external append-only registry, the result also does not independently prove preregistration time or terminal-attempt completeness. It does not support “safe for everyone,” “clinically validated,” “best book,” or “number one.” A content fix invalidates the tested hashes and requires a fresh cohort whose readers did not see the failed wording.

## Seven-day follow-up

If the book is later tested for use rather than comprehension alone, invite readers to complete Appendix A for seven days and preregister the outcome measures before recruitment. Keep those results separate from this release gate. A comprehension pass is not evidence of sustained practice or benefit.
