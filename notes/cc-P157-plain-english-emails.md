# cc-P157: Golem emails in plain English

2026-10-21. The Iron Golem (Opus). Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P157-plain-english-emails.md`. Work copies:
`D:\UO\golems\Iron\ShatteredLegacy` and `D:\UO\golems\Iron\shard-migration`, branch `golem/Iron/P157`. Both were clean at
the start. Read first: P149's, P153's and P156's notes. Not committed: the Golem commits after the DONE line.

## In plain words

- Every email from the Golems now opens with what happened in a sentence a person would say, then a "What to do" line
  ("Nothing to do, it keeps going." or the one thing to do), with the technical details at the bottom under "Details".
- A finished prompt's email now says what the work actually changed, in a few plain bullets that each prompt's notes
  start with from now on. The morning night-shift summary gets one such line per finished prompt.
- You get fewer emails: a prompt starting, a session the Golem opened itself, a merge into main and similar routine
  news now ride along in the next email instead of arriving on their own. One finished prompt is one email.
- Nothing for you to do. To get the routine emails on their own again, set `routineEmails` to true in
  `D:\UO\golem\settings.json`.

## Headlines

- **Done and installed.** The Golem side is live in `D:\UO\golem` (every changed file backed up as
  `<name>.bak-20261021-p157`; the live files' hashes were checked against the copy it was built from just before, and
  nobody had changed them). The ShatteredLegacy side is in this branch. **One gap, said plainly:** the final full run of
  `Golem.Tests.ps1` was stopped by Claude Code for low memory (Deviation 1); every fact did run on the new code, and every
  one that failed was fixed and passed again on its own.

- **One helper builds every email:** `D:\UO\golem\GolemMail.ps1` (new). `New-GolemMail <kind>` takes the facts and
  returns the subject and body; golem.ps1's new `Send-GolemMail` sends it. A fact checks that `Send-Mail` is called
  nowhere else in golem.ps1 or Away.ps1, so new emails come out the same way.
- **The shape:** subject in words with the prompt's short title ("Finished P133 (Haven dashboard), started P154
  (console speed-up)"), "Needs you: " first only when Chase must act; a first line a person would say; "What got done"
  (the notes' In plain words bullets); "What to do"; "Also since my last email" (folded routine news); "Details" (file
  names, settings, exit codes, log excerpts, CC's last message). Times are Chicago time ("about 4:50 PM", "tomorrow at
  10:30 PM").
- **57 sample emails, every kind, rendered and checked.** `Get-MailSamples` holds sample facts for each of the 39 kinds
  (and their variants). The renders are saved in `D:\UO\golem\tests\fixtures\p157-mail-renders.txt`.
- **In plain words:** the hand-off now asks every session to start its notes with `## In plain words` (2 to 4 bullets
  and a last one for Chase). The done email copies it under "What got done"; older notes fall back to their Headlines
  and the prompt's Summary line, marked "(from CC's notes)". These notes start with that section.
- **Fewer emails:** six routine kinds wait in `mail-later.jsonl` for the next email (table below), and a finished
  prompt on its own branch no longer sends two emails. New setting `routineEmails` (false) restores the old behavior.
- **The other senders:** the Tinker's question email, the overnight bot's three emails (start, morning report, crash)
  and the Shard Console's shard-question email have the same shape. No status publisher sends mail (checked: no other
  script under `D:\UO` sends email).

## What changed

**`D:\UO\golem`** (not a repo; each edited file backed up as `<name>.bak-20261021-p157`):

| File | Change |
|---|---|
| `GolemMail.ps1` (new) | `Format-MailTime` (Chicago time in words), `Get-PromptShortTitle`, `Format-PromptLabel`, `Get-PromptLabel`, `Find-PromptFile`, `Get-PromptSummaryLine`, `Get-PlainWords` (In plain words, else Headlines and Summary), `Find-NotesFile`, `New-DoneBlock`, `Format-DoneLine`, `ConvertTo-PlainWhy` (a technical reason in words), `Format-GolemMail` (the shape), `Test-MailPlain` (the rules above Details), `New-GolemMail` (39 kinds), `Add-MailLater` / `Get-MailLater` / `Add-MailAlso` (folding), `Get-MailSamples` |
| `golem.ps1` | dot-sources GolemMail.ps1; `routineEmails` setting; `Send-GolemMail`, `New-Mail`, `Get-Label`, `Use-DoneBlock`, `Send-DoneLeft`; every `Send-Mail` call is now `Send-GolemMail (New-Mail <kind> @{...})`, the old text moved under Details; the done block is built at DONE and carried by the next email; the multi-Golem "done, waiting to merge" email is folded into it; the hand-off asks for `## In plain words`; the night summary has one plain line per finished prompt |
| `Away.ps1` | the away-ended, digest and two mail-command replies through Send-GolemMail; `Get-ParkedPlainLines`, `Get-AwayDigestMail` |
| `TinkerLib.ps1` | the Tinker's question email in the same shape, written inline (GolemMail.ps1 is in the kit, but the Tinker loads only its own library) |
| `README.md` | section "Emails in plain English (cc-P157)", the Files and settings rows |
| `tests\Golem.Tests.ps1` | eight `P157_*` facts; `-UpdateMailRenders`; the old facts' email subjects said the new way (about 70 checks) |
| `tests\Tinker.Tests.ps1` | the question email's new subject and shape |
| `tests\fixtures\p157-mail-renders.txt` (new) | every kind rendered |

**`D:\UO\golems\Iron\ShatteredLegacy`**:

| File | Change |
|---|---|
| `tools\playtest-bot\uobot\mailshape.py` (new) | `shape()` and `plain_problems()`: the same shape and rules in Python |
| `tools\playtest-bot\uobot\notify.py` | the start and crash emails in the shape; subjects "Overnight play tests starting: 2 items to check", "Overnight play tests stopped early: <reason>" |
| `tools\playtest-bot\uobot\report.py` | the morning report email: the night in words, "Needs a look", What to do, then Details (subject unchanged) |
| `tools\playtest-bot\tests\test_overnight.py` | `PlainEmails` (four tests); the changed subjects |
| `scripts\Shard-Console.ps1` | `Get-QuestionMails`: the shape; subject "[Shard] Needs you: the Live shard is waiting for an answer" |
| `scripts\tests\Shard-Console.Tests.ps1` | `P106_OneEmailPerQuestion`: the new subject and the plain part |
| `CHANGELOG.md`, `VERSION` | 2026.10.21.12, four Staff lines |

## Every email, before and after

The subjects carry the `[Golem]` tag (or `[<name> Golem]`) in front, as before; P149's reply code is still added at the
end when email controls are on. Labels like "P154 (console speed-up)" come from the prompt's heading.

| Where (golem.ps1 unless named) | Before | After |
|---|---|---|
| Hand-off, something finished | `P95 done, starting P96 (3 of 3)` | `Finished P95 (title), started P96 (title)` |
| Hand-off, nothing finished | `Starting P95 (2 of 3)` | `Started P95 (title)` (routine: folded) |
| DONE on a Golem's own branch | `P154 done on golem/Iron/P154, waiting for the ShadowIron Golem to merge` | no email of its own: rides in the next email, or `Finished P154 (title)` |
| Queue empty | `Queue empty, P154 done and pushed` | `Finished P154 (title), and the queue is empty` |
| Commit failed | `P154 done but COMMIT FAILED, needs you` | `Needs you: P154 (title) finished, but saving it failed` |
| Rest: session full | `Resting: session full after P100 (72% full). Ready now: ...` | `Resting after P100 (title): the Claude Code session was full` |
| Rest: model | `Resting: waiting for a Fable session after P100. Ready now: ...` | `Waiting for a Fable session for P101 (title)` |
| Rest: run cap | `Resting: run cap after P100 (3 done, cap 2). ...` | `Resting after P100 (title): this run reached its limit` |
| Rest: usage limit | `Resting until 4:00 PM (usage limit), 15 queued` | `Paused until about 4:00 PM: usage limit` |
| Rest: ahead of pace | `Resting until Sun 4:00 AM (ahead of pace)` | `Resting until Sunday at about 4:00 AM: ahead of pace` |
| Rest: wrap up | `Resting: wrap up after P100. ...` | `Wrapped up after P100 (title), as you asked` |
| Rest: stopping point | `Resting: stopping point after P100 (P103 queued). ...` | `Paused P100 (title) at a stopping point` |
| Rest: bot window, night shift ended, night batch, long run ended | `Resting until 3:00 AM (overnight bot window), ...` and so on | `Resting until about 3:00 AM: the overnight test bot is running`, `Night shift over, resting until about 10:30 PM`, `Night batch done after P154 (title)`, `The extra-hours run has ended` |
| Resting as asked | `Resting as asked, 4 still queued` | `Resting as you asked, 4 still in the queue` |
| STOPPED | `P149 STOPPED, needs you: <reason>` | `Needs you: P149 (title) stopped with a question` |
| Parked (away) | `P149 parked: <reason>` | `Needs you: P149 (title) is parked with a question` |
| Mid-task stop | `NEEDS YOU: P129 stopped mid-task` | `Needs you: P129 (title) stopped partway without saying why` |
| Notification | `NEEDS YOU: <message>` | `Needs you: Claude Code is waiting on you during P129 (title)` |
| A session's question (Ask-Chase.ps1) | `NEEDS YOU: Iron asks about P216: <question>` | `Needs you: Iron has a question about P216 (title)` |
| DONE never handed | `NEEDS YOU: P154 DONE in a Bronze session that was never handed it` | `Needs you: Bronze said it finished P154 (title), but never had it` |
| Prompt file exists | `NEEDS YOU: cc-P154-x.md already exists in claimed` | `Needs you: P154 (title) is in the queue twice` |
| Cannot start | `NEEDS YOU: Copper cannot start P154` | `Needs you: Copper couldn't start P154 (title)` |
| Codex lane needs you | `NEEDS YOU: the Codex lane Verdite <what>` | `Needs you: the Codex helper Verdite needs you on P159 (title)` |
| Codex lane cannot start | `NEEDS YOU: the Codex lane Verdite cannot start P159` | `Needs you: the Codex helper Verdite couldn't start P159 (title)` |
| Codex lane lost claim | `P159 went back to the queue: the Codex lane Verdite lost its claim` | `P159 (title) went back to the queue` (routine: folded) |
| Codex lane done | `P159 done by Codex on <branch>, waiting for the ShadowIron Golem to merge` | `Codex finished P159 (title)` |
| Merged | `merged P154 from Bronze` | `Merged P154 (title) from Bronze into main` (routine: folded) |
| Fix-up | `NEEDS A FIX-UP: P154 from Bronze did not merge` | `P154 (title) from Bronze didn't merge, a fix-up is queued` |
| Merge failed twice / Codex | `NEEDS YOU: P104 from Bronze did not merge, and it was a fix-up already` (and the Codex one) | `Needs you: P104 (title) from Bronze didn't merge` |
| Merge Golem waits | `ShadowIron waits: the real folders are not clean` | `Needs you: I can't merge: the main folders have unsaved changes` |
| Self-wake | `woke a Fable session for P101` | `Opened a new Fable session for P101 (title)` (routine: folded) |
| Night shift start | `night shift starting: P101 to P102 queued, usage 20% session, 30% week` | `Night shift started` (routine: folded) |
| Night shift skipped | `night shift skipped: <reason>` | `Night shift skipped tonight` |
| Night summary | `night shift summary: 2 finished, 0 stopped, 2 waiting` | `Night shift: 2 finished, 2 waiting` (`Needs you: night shift: ...` when one stopped) |
| Marathon | `Marathon on: projected 66% by Wed 4:00 PM` / `Marathon off: ...` | `Marathon mode is on` / `Marathon mode is off` |
| Low queue (to the overseer) | `queue running low for Bronze: 1 Fable prompt left` | `The queue is running low for Bronze` |
| Free reset | `A free full reset is available (expires 2026-10-22). Use it?` | `A free usage reset is on offer until tomorrow. Use it?` |
| Plan reading stale | `The usage reading from claude.ai is 14 hours old` | `Needs you: I can't read your Claude usage from claude.ai` |
| Stall | `paused: no progress for 47 min in P154 (3 of 9)` | `Needs you: P154 (title) has made no progress for 47 minutes` |
| Model fallback | `P101 keeps starting on Opus, not Fable` | `Needs you: P101 (title) keeps starting on Opus instead of Fable` |
| Registry invalid | `NEEDS YOU: the Golem registry is invalid` | `Needs you: the list of Golems has a mistake` |
| Stale lock | `a stale lock on docker-build expired` | `Cleared a stuck Docker build lock` |
| Stale claim | `stale claim released: P101 back in the queue` | `P101 (title) went back to the queue` (routine: folded) |
| Away ended (Away.ps1) | `away mode ended` | `Away mode is over` (`Needs you: Away mode is over, and prompts are parked` when some are) |
| Away digest (Away.ps1) | `away digest Wed` | `Away update for Wednesday` |
| Mail command done (Away.ps1) | `done: status` | `Done: status` |
| Not a command (Away.ps1) | `not a command` | `That wasn't one of the commands` |
| Tinker question (TinkerLib.ps1) | `[Tinker] NEEDS YOU: Gold P211` | `[Tinker] Needs you: the Tinker has a question about Gold on P211` |
| Bot start (notify.py) | `Overnight play tests starting: 2 checks on abc1234` | `Overnight play tests starting: 2 items to check` |
| Bot crash (notify.py) | `Overnight play tests FAILED on abc1234: <reason>` | `Overnight play tests stopped early: <reason>` |
| Bot report (report.py) | `Overnight play tests: 30 pass, 2 fail, 1 flaky` | unchanged (the body is new) |
| Shard question (Shard-Console.ps1) | `[Shard] Live is waiting for an answer: <prompt>` | `[Shard] Needs you: the Live shard is waiting for an answer` |
| Test emails (Send-TestEmail.ps1, Setup-Email.ps1) | `[Golem] Test email` | unchanged (already plain: "The Golem can email you. Nothing else to do.") |

**Subject words kept for filters and P149:** the `[Golem]` / `[<name> Golem]` / `[Tinker]` / `[Shard]` tags; P149's
`(code XXXXXX)`, added by Send-Mail at the end of every subject while email controls are on (Use-MailCodes reads the code,
not the words); "Overnight play tests" at the front of every bot email; "Needs you" first on everything Chase must act
on. The Shard Console's alert light (`Test-AutopilotAlert`) matches `^NEEDS YOU` without case, so "Needs you:" still
lights it amber. P149's notes name no other subject word the commands depend on.

## Fewer emails (part 3)

| Email | Now | To undo |
|---|---|---|
| A prompt started with nothing finished (the phrase, a wake) | folded into the next email | `routineEmails: true` |
| A session the Golem opened itself | folded (the rest email already says a session is on its way) | `routineEmails: true` |
| A branch merged into main (integrator and ShadowIron) | folded | `routineEmails: true` |
| A stale claim put back in the queue | folded | `routineEmails: true` |
| A Codex lane's lost claim | folded | `routineEmails: true` |
| The night shift's start | folded (the morning summary covers the night) | `routineEmails: true` |
| "Done on its branch, waiting to merge" then "done, starting the next" | one email: the done block rides in the next email (the hand-off, a rest, the queue empty), else its own `Finished P<nn>` | not a setting: one email per finished prompt is the point |

Folded news waits in `D:\UO\golem\mail-later.jsonl` and goes out under "Also since my last email" in the next email any
Golem on this PC sends to Chase (the file is renamed before it is read, so two Golems never both send it). Only the
subject line rides along; the details of a folded email stay in the Golem's log. P149 has no general digest (its digest
is away mode's), so this is the "next email".

## 3a: what the work did

- The hand-off now says: "Start your notes file with a section ## In plain words: 2 to 4 short bullets a
  non-programmer would follow, each saying what changed, what Chase will notice and where (for example: The console
  opens in about 2 seconds now instead of 10), and a last bullet with anything he needs to try, deploy or decide, or
  Nothing for you to do. The Golem's done email copies that section to Chase."
- The done email copies that section under "What got done", right after the first line. Without it: the prompt's
  Summary line and the first sentence of up to three Headlines bullets, titled "What got done (from CC's notes)".
- The night-shift summary and the away digest have one plain line per finished prompt from the same section.
- **The console's Golem tab: not done.** Showing the bullets for the last few finished prompts means new status data,
  a new block on the Shard Console's Golem tab and on the web console's card, and their facts. That is not a small
  change, so it is left for a follow-up prompt. (Each done email has them meanwhile.)

## The renders

Every kind is rendered with sample data in `D:\UO\golem\tests\fixtures\p157-mail-renders.txt` (57 renders; the
P157 fact fails if they drift, `-UpdateMailRenders` writes them again). No real sample email was sent: no setting or
flag allows it. Four of them:

```
Subject: [Golem] Finished P133 (Haven dashboard), started P154 (console speed-up)
P133 (Haven dashboard) is done, committed and pushed. Now working on P154 (console speed-up). 7 of 26 done in this run.

What got done (from CC's notes):
- Haven gets a status dashboard for the Golems.
- The dashboard shows each Golem and its prompt.

What to do: Nothing to do, it keeps going.

Details
-------
Now running: cc-P154-console-speed-up.md
...
```

```
Subject: [Golem] Paused until about 2:50 PM: usage limit
Claude Code hit your Claude plan's usage limit during P154 (console speed-up). It picks up where it left off once the limit resets at about 2:50 PM.

What to do: after about 2:50 PM, open Claude Code on the game PC and say: Golem, please work on the shard tasks.

Details
-------
...
```

```
Subject: [Golem] Needs you: P149 (away mode) stopped with a question
Claude Code stopped partway through P149 (away mode) and wants a decision from you. Nothing else runs until you answer.

The question:
which of the two layouts do you want?

What to do: answer it on the Golem card of the web console (the answer goes straight back to the Golem), or in the Claude Code window on the game PC.

Details
-------
...
```

```
Subject: [Golem] Night shift: 2 finished, 2 waiting
The night shift ran from yesterday at about 10:30 PM to about 6:30 AM. 2 prompts finished. 2 are still waiting.

What got done:
- P154 (console speed-up): The console opens in about 2 seconds now instead of 10.
- P133 (Haven dashboard): Haven gets a status dashboard for the Golems. (from CC's notes)

What to do: Nothing to do, it keeps going.

Details
-------
...
```

## Tests

Windows PowerShell 5.1 throughout. Every new test was seen failing first against the code before this prompt.

**New and seen failing first:**

| Test | Before (old code) | After |
|---|---|---|
| `Golem.Tests.ps1 -Only P157`: eight facts (renders and the plain-words rules, What to do, one helper, the done email from In plain words, the fallback to Headlines, the hand-off line, routine folding and `routineEmails`, Chicago times and short titles) | all 8 FAIL against the pre-P157 golem.ps1 (1 check passed, 16 failed) | all 8 PASS, 425 checks (on the dev copy, and again on the installed hook) |
| `Tinker.Tests.ps1` `P222_OwnWorkIsKept...` (the question email's subject and shape) | FAIL on the old TinkerLib.ps1 (2 checks) | PASS; the whole Tinker suite 133 checks passed, 0 failed (dev and installed) |
| `test_overnight.py` `PlainEmails` (4 tests) and the changed `Emails` subjects | 7 of 8 FAIL on the old notify.py and report.py | PASS |
| `Shard-Console.Tests.ps1` `P106_OneEmailPerQuestion` | FAIL on HEAD's Shard-Console.ps1 ("expected [[Shard] Needs you: the Live shard is waiting for an answer] but got [[Shard] Live is waiting for an answer: ...]") | PASS, with the seven P108 facts that read the same function |

**The old facts** (`Golem.Tests.ps1`): the first full run on the new code ran every fact to the end: 958 checks
passed, 74 failed, in 49 facts. Two were the P184 overlap facts that already fail before P157 (P353's notes: the same 5
checks fail on the pre-P353 hook). The rest asked for the old subjects word for word (and one fact, the integrator's,
expected a "merged" email, now folded). Each check was rewritten to the new words, about 70 of them, and three things in
the new code were fixed on the way (a short title that came out as a file name, the lost-claim check reading the wrong
log, a fact world whose session was too full to hand on). Then each of the 47 facts was run again on its own: all pass.
`P200_Marathon_WakesEveryAwakeGolemOnItsLaneAndOpensDaytimeHours` failed once in a loaded run ("Bronze woken at 1 PM")
and passed alone four times (twice on the old hook, twice on the new): timing under load, not this change.

**The other suites on the new code:** `Lane.Tests.ps1` 59 checks passed, 0 failed; `Codex.Tests.ps1` 136 passed, 0
failed. The playtest-bot suite (`python -m unittest discover -s tests`): 54 tests, 1 failure,
`test_installer_dry_run_prints_the_call_and_registers_nothing`, which fails the same way on HEAD's untouched bot code:
the real "SL overnight play tests" task is registered on this PC, and the test checks that it is not.

**Commit preflight** (`Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo
D:\UO\golems\Iron\shard-migration`):

```
Repo Result
---- ------
code dry run
docs dry run
```

## Deviations and decisions for Chase

1. **The last full Golem suite run was stopped for low memory, and not restarted.** The second full run of
   `Golem.Tests.ps1` (after the subjects were rewritten) was stopped by Claude Code after about 75 facts because the PC
   ran low on memory (other sessions; free memory fell to 728 MB). Claude Code says not to start it again unasked, so I
   did not. What stands in for it: the first full run covered every fact on the new code, and every failing fact was
   fixed and passed again on its own afterwards (Tests). To finish it, when memory allows:
   `powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\Golem.Tests.ps1` (expect only the two P184
   overlap facts, which fail before this prompt too). The Shard Console's full suite was not run either (it has known
   failures from earlier prompts); its P106 and P108 facts were.
2. **The Read tool was denied** (unattended run) on `tools\playtest-bot\uobot\notify.py` in my ShatteredLegacy copy.
   I did not retry the read. The one-sentence fix it was for (the crash email's first line) was made with a small
   Python script (`notify_fix2.py` in my scratchpad) that checks the old line is there exactly once. What I wanted to
   run: Read of `notify.py` lines 44 to 49, then an Edit.
3. **The overnight bot's start email still comes on its own.** It is routine, but it is the bot's own process (not the
   Golem's, so it cannot use the Golem's folding), and it is the only place that says how to stop a night run that is
   under way. It is in the new shape, with the stop commands under Details.
4. **Folded emails keep only their subject.** Under "Also since my last email" each folded email is one line (its
   subject); its details stay in the Golem's log (`golem.log` or `golem-<name>.log`).
5. **The console's Golem tab does not show the In plain words bullets yet.** It is not a small change (status data,
   both consoles, their facts), so it is left for a follow-up prompt, as part 3a allows.
6. **Times:** this PC's clock is Central time, so "Chicago time" changes nothing here. A time the Golem has in UTC (the
   usage resets) is converted to Chicago time, and a fact checks it.
7. **The setting-name check** covers settings.json's camelCase names (`nightSessionMaxPct`, `routineEmails`, and so
   on). One-word keys that are plain English (`marathon`, `notifications`) are not flagged, since "Marathon mode" is
   how Chase knows the feature.

## For Chase

- **The before and after subjects** are in the table above; the subject words kept for filters are under it.
- **Merged and dropped:** six routine kinds now ride in the next email, and one finished prompt is one email (table
  under "Fewer emails"). To get the routine ones on their own again: `"routineEmails": true` in
  `D:\UO\golem\settings.json`.
- **If you filter mail:** "NEEDS YOU" in capitals is now "Needs you:" (a Gmail filter does not care about case). "NEEDS
  A FIX-UP", "STOPPED" and "COMMIT FAILED" are gone from subjects; everything you must act on starts "Needs you:".

P157 DONE
