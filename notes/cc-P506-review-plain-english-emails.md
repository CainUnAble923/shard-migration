# P506: Review of plain-English Golem emails (P157)

2026-10-23. Review only. No implementation changes.

## In plain words

- Routine updates can disappear when delivery fails or more than 30 updates have accumulated.
- Notes, questions, and bot errors can put paths and sensitive text into emails without filtering it.
- The morning bot email can say there is nothing to do even when its long-running activity check failed.
- For Chase: these are findings for a later fix prompt. No email was sent and no running service was changed.

## Scope

Read AGENTS.md in both work copies, the direction decision, the task-list working agreement, and `notes/cc-P157-plain-english-emails.md`. P157 commit `faded84371bb1a1c48c2ff36ff1c81fd1eb30537` is an ancestor of local main; the code work copy and main both pointed to `579ad58f8f478280b03b8cf80f1ee9a5b3001a27` at review time.

There was no separate P157 review beside its notes. Also read P472's review and its Codex review, plus P410's notes and Codex review, to distinguish later delivery changes and avoid repeating existing findings. The away-command error disclosure, repeated unknown replies, missing Tinker reply codes, and delayed delivery of failed bot reports are already recorded there and are not new findings here.

Reviewed these source files and relevant tests:

- `D:\UO\golem\GolemMail.ps1`: formatting, note extraction, sample messages, and routine-message batching.
- `D:\UO\golem\golem.ps1`: senders, completion notices, handoffs, rest notices, questions, and night summaries.
- `D:\UO\golem\Away.ps1`: digest and parked-prompt formatting and their send sites.
- `D:\UO\golem\TinkerLib.ps1`: question formatting and delivery; the P157 README section and `tests\fixtures\p157-mail-renders.txt`.
- `D:\UO\golem\tests\Golem.Tests.ps1`: P157 facts and their fixtures; `tests\Tinker.Tests.ps1`: the question-email assertions.
- Code work copy: `tools/playtest-bot/uobot/mailshape.py`, `notify.py`, `report.py`, and `tools/playtest-bot/tests/test_overnight.py`.
- Code work copy: `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`, and P157's `CHANGELOG.md` and `VERSION` changes.
- Delivery context: `D:\UO\golem\GolemOutbox.ps1`, relevant functions in `TinkerMail.ps1`, `tools/playtest-bot/Send-BotReport.ps1`, `Run-OvernightPlaytests.ps1`, and `uobot/soak.py`.

The Golem helpers are outside the repositories. They were read only; their current code includes later work, especially P410's Tinker routing. Findings 1 and 2 concern direct delivery when Tinker routing is disabled, unavailable, or fails to save an event.

Reviewed SHA256 values: `GolemMail.ps1` = `A846F59517B27A400C487097E1EFBDAC190FCC4A23D1B33BBBA37A3BA37EB57D`; `golem.ps1` = `E8C2C1A44184B74171AA87E1EA1641E033731E41A6A209733B0F2D581C702FA8`.

## Findings

1. **bug**, `D:\UO\golem\golem.ps1:373` and `D:\UO\golem\GolemMail.ps1:515`: The sender deletes the waiting routine updates before attempting delivery, so an SMTP failure permanently removes them even though no email arrived. Return a delivery result, keep the claimed batch until successful delivery, restore it on failure, and add a failed-send-then-retry test.

2. **bug**, `D:\UO\golem\GolemMail.ps1:516`: Reading a batch returns only its last 30 updates after deleting the entire file, so the oldest update in a 31-update batch never reaches any email. Preserve overflow for later delivery or summarize it explicitly, and add a test that accounts for every update across multiple batches.

3. **risk**, `D:\UO\golem\GolemMail.ps1:111`, `:137`, and `:335`: Markdown cleanup preserves full paths and token strings in note bullets and questions, allowing them above Details; a synthetic extensionless Windows path and `token=DEMO_SECRET_VALUE` also passed `Test-MailPlain`. Filter dynamic text before formatting, keep necessary path diagnostics under Details, redact credentials throughout the outgoing message, and test both old-note fallbacks and question bodies, including Tinker forwarding.

4. **risk**, `tools/playtest-bot/uobot/notify.py:51` and `:57`: The crash email copies an exception reason into its subject and opening, then includes raw log lines, so synthetic paths and token strings survived in the subject and synthetic credentials survived in the body. Use a short approved crash description above Details, redact sensitive values from all emailed diagnostics, and add cases with path-bearing exceptions and credential-bearing log lines.

5. **bug**, `tools/playtest-bot/uobot/report.py:101` and `:113`: If individual checks pass but the soak reports errors, the opening still says the checks passed and the action says "Nothing to do," leaving the failed long-running activity check only under Details. Include soak errors in the opening and action decision, and add a passing-checks-with-failed-soak case alongside the existing plain-email tests.

## Evidence and missing coverage

Isolated probes used the actual formatter and queue functions, synthetic notes, synthetic errors, and a sender stub that attempts delivery without reporting success. The PowerShell probe loaded only the sender function from the hook's parsed syntax tree; it did not execute the hook. The report probe replaced file reads and writes with memory-only fixtures.

| Probe | Observed result |
| --- | --- |
| Queue a routine update, then attempt a non-routine email without successful delivery | One send attempt; the pending file was absent and the queue returned zero updates afterward. |
| Queue updates named event-1 through event-31, then read the batch | Returned event-2 through event-31; the next read was empty. |
| Old-note Headlines fallback containing a synthetic path and token | Both remained above Details; the plain-text validator accepted the message. |
| Question containing the same synthetic path and token | Both remained above Details; the plain-text validator accepted the message. |
| Bot crash reason with a synthetic path and token, plus a log token | The path and token remained in the subject; the log token remained in the body. |
| Passing individual check plus a soak error | Opening said the check passed; action was "Nothing to do." |

The fixture renders and `Golem.Tests.ps1:3833` use handpicked clean facts. The routine-message fact at `:3923` checks sequential successful consumption and a two-update batch, but misses delivery failure, retries, and overflow. The note-fallback and question cases lack sensitive-input assertions. `tools/playtest-bot/tests/test_overnight.py:222` checks ordinary start, crash, pass, and failed-check messages, but omits sensitive diagnostics and soak-only failures. These gaps explain why the existing shape checks pass while the probes expose the findings.

## Verification and limits

- PowerShell probes ran with `powershell.exe -NoProfile`, Windows PowerShell **5.1.26100.9711**.
- Rendered every entry returned by `Get-MailSamples` in `D:\UO\golem\GolemMail.ps1`: 57 renders, zero failures under the sampled plain-text checks. This did not run the full Golem suite or claim its fixture comparison passed.
- Ran the existing `Emails` and `PlainEmails` classes in `tools/playtest-bot/tests/test_overnight.py`: eight tests passed. The first attempt passed five and hit three Windows temporary-directory permission errors; an isolated wrapper changed only temporary-directory creation to use inherited permissions in the ignored work-copy scratch folder, after which all eight passed.
- Ran `scripts/tests/Shard-Console.Tests.ps1` with `SL_FACT_FILTER=^P106_OneEmailPerQuestion$` under `powershell.exe`: one fact passed, zero failed. It covers question deduplication and the P157 opening.
- No permanent tests or fixes were added. The defect probes exposed the current behavior, so there is no claimed passing fix run.
- Ran `tools/progress.py --dry-run` with both work-copy path overrides, exit 0. It writes `tools/progress.json` despite dry-run mode; restored that generated file to its exact original bytes. Its content counts are outside this review's scope.

No additional double-send finding was established in the completion and question paths reviewed. Paths deliberately placed under Details are part of P157's design and are not counted as defects by themselves. No actual password, mailbox, or credential file was read; all sensitive markers above were synthetic. Actual secret exposure, SMTP acceptance and recovery, and concurrent-process behavior remain unverified. The full Golem, Tinker, bot, and console suites were not run.

Scratch probes stayed under `tools/playtest-bot/cache/p506/`, confirmed ignored by `git check-ignore`. No file over 5 MB was added. No commit, merge, push, branch switch, deployment, or Haven connection was performed. The only deliverable is this review note.

P506 DONE
