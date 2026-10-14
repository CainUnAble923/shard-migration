# cc-P94: Autopilot tile and tab show run position, steps and last activity (2026-10-14)

## Headlines

- **The AUTOPILOT tile reads `D:\UO\cc-autopilot\status.json` first.** While a prompt runs, it shows two lines:
  `P94  1 of 10  14m` (prompt, run position, steps when CC has a task list, age), then the step and
  `last activity 2m ago` or `running Bash for 9m`. Checked live with `-Status` on the real file during this prompt.
- **Amber, never red**, for: NEEDS YOU, quiet past `stallMinutes` (`quiet for 52m`), status.json more than 15 min old
  while RUNNING (`status 40 min old; watch task not running?`), and failing email.
- **Fallback.** With no status.json, or one that is unreadable or not schema 1, the tile reads ENABLED, state.json and
  the log exactly as cc-P74 did; a fact proves the tile text is identical.
- **The Autopilot tab** adds status, run (`2 of 5, cap 6, 1 done, started ...`), steps, activity and settings lines,
  one new button **Open settings.json** (Notepad, nothing else), and a caption sentence on the run cap.
- **Tests: 14 new facts; the whole suite is green** (counts and the one changed P83 fact below).
- **Two hook bugs for Chase**, both with file:line and a fix under "For Chase". **The second one affects this prompt:
  autopilot will not commit P94 when it reads P94 DONE.**

## What the tile reads (file:line, `D:\ShatteredLegacy\scripts\Shard-Console.ps1`)

| What | Where |
|---|---|
| status.json and settings.json paths | `New-AutopilotConfig`, :170-171 |
| SHELL: read both files; a failed status read is kept apart from Errors so it falls back instead of UNKNOWN | `Get-AutopilotFacts`, :3772-3780 (function at :3751) |
| SHELL to CORE | `Get-AutopilotViewNow`, :3815 |
| Schema 1 parse: state must be OFF, IDLE, RUNNING or NEEDS YOU; times kept local or UTC as the hook writes them; a bare-string `queued` counts as one item | `ConvertFrom-AutopilotStatus`, :2655 (`ConvertFrom-AutopilotTime` just above) |
| settings.json with the hook's own defaults (6, 45, true) per missing key, never throws | `ConvertFrom-AutopilotSettings`, :2693 |
| Status preferred, else `StatusNote` says why and the four facts are judged as before | `Get-AutopilotView`, :2721 |
| The 15 minute stale limit | `$script:AutopilotStaleMinutes`, :2641 |
| Step, tool or last activity, quiet, stale | `Get-AutopilotActivity`, :2829 |
| The tile from status.json | `Get-AutopilotStatusGlance`, :2852, called from `Get-AutopilotGlance` :2786 |
| The tab panel's new lines | `Format-AutopilotPanel`, :2906 (status block from :2921) |
| The new button's plan | `Get-AutopilotPlan`, `'autopilot.settings'`, :3042; action row :851 |
| Safety: Notepad opens only autopilot.log or settings.json | `Test-PlanSafety`, :2003 |
| `-Status`: a two-line tile prints its second line indented | `Format-StatusReport`, :3121 |
| Caption | :6278 |

Time zones: the hook writes `startedAt`, `runStarted` and `generatedAt` in local time and the three activity times in
UTC (`cc-autopilot.ps1:206, 211, 215, 222-224`). The core keeps each one's kind and compares against `$Now` local or
`$Now.ToUniversalTime()`.

## Tests

`scripts\tests\Shard-Console.Tests.ps1`, under Windows PowerShell 5.1:

- First run: **225 facts, 224 passed, 1 failed** (8m 11s). The failure was `P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo`, which
  counted six Autopilot buttons (`P74's own six are unchanged`). There are seven now, so it asserts seven and says why.
  The cc-P74 form fact now lists `autopilot.settings` last and checks the caption's run-cap sentence.
- Final run: **225 facts, 225 passed, 0 failed**, exit 0.

The 14 new facts (lines 2878-3060). Fixtures are `scripts\tests\fixtures\autopilot-status-running-2026-10-14.json`
(the real status.json as P94 started) and `autopilot-settings-2026-10-14.json` (the real settings.json). Every other
shape is that file with fields changed by `Set-ApStatus`. Times are set relative to one clock, so the facts hold in
any time zone.

| Prompt asked for | Fact |
|---|---|
| the real file | `P94_TheRealStatusJsonReadsAsSchemaOne` |
| RUNNING with steps | `P94_RunningWithStepsSaysPositionStepAndAgeOverTheStepAndLastActivity` |
| RUNNING without steps | `P94_RunningWithoutStepsOmitsTheStepPart` |
| a tool running | `P94_ARunningToolIsNamedWithHowLongItHasRun` |
| quiet past stallMinutes | `P94_QuietPastStallMinutesTurnsTheTileAmber` (also: stallMinutes is read from settings.json) |
| NEEDS YOU | `P94_NeedsYouIsAmberWithTheHooksOwnWords` |
| a stale status.json | `P94_AStaleStatusWhileRunningIsAmberAndSaysWhy` (also: not flagged while IDLE) |
| a missing status.json | `P94_AMissingOrUnreadableStatusJsonFallsBackToTheOldReading` (missing, not JSON, schema 2, unknown state, read error) |
| `queued` with one and none | `P94_QueuedWithOneItemAndWithNone` (also OFF and runDone) |
| | `P94_FailingEmailStillTurnsTheStatusTileAmber` |
| the tab | `P94_ThePanelSaysTheRunTheStepsTheActivityAndTheSettings` |
| `-Status` | `P94_TheStatusReportIndentsTheTilesSecondLine` |
| the button | `P94_OpenSettingsOpensOnlySettingsJsonInNotepad` (also: Notepad on state.json, status.json, the credential or email.json is refused) |
| the shell | `P94_TheFactsReadStatusAndSettingsAndTheTileUsesThem` (temp folder, real files) |

`-Status` against the real folder, during this prompt:

```
AUTOPILOT        : RUNNING         P94  1 of 10  6m
                                   running Bash for 4s
```

`-Action autopilot.settings -DryRun`:

```
== DRY RUN: autopilot.settings (autopilot) ===========================================
  1. OPEN     C:\WINDOWS\notepad.exe D:\UO\cc-autopilot\settings.json
         # Opening settings.json in Notepad. A saved change counts from the hook's next event: progressEmails (true or false), maxPerRun (0 is no cap), stallMinutes.
   (dry run: nothing was run)
```

Not tested by hand: the tile drawn in the open GUI. The form fact builds it and checks the buttons, caption and
redraw, but nobody looked at a two-line tile at real size. For play tests:
- Open the console while a prompt runs: the AUTOPILOT tile shows two lines, and both are readable.
- Click Open settings.json on the Autopilot tab: Notepad opens settings.json.

## Deviations and decisions for Chase

- **The console is in the code repo, not shard-migration.** The prompt says "console code and tests in
  shard-migration", but `Shard-Console.ps1` and its tests live in `D:\ShatteredLegacy\scripts`. The work is there; only
  the notes are in shard-migration.
- **No task list.** The hand-off asks for one task per step. This session has no task-list tool (no TodoWrite or
  TaskCreate), so `stepsTotal` stayed 0 for P94. That is also why the live tile shows no step part.
- **P94 stopped twice before it started**, both times on the prompt's own "Before you start" rule.
  - First: 3 uncommitted files (the overseer pass-down, and P93's play-test import written by the play-test service 24
    seconds after P93's commit).
  - Second: Chase's commit had not landed and the overseer chat was still writing 9 files.
  - Chase committed, and it ran on the third hand-off.
- **Tile wording.** The prompt's example `P92  2 of 5  step 3/6  14m` is followed exactly. Under an hour the age is
  whole minutes (`14m`, not cc-P74's `14m 0s`), then `1h 5m`.
- **"Quiet" replaces "last activity"** on the second line rather than being added beside it. With a tool still running
  it reads `quiet for 52m (Bash still running)`.
- **NEEDS YOU comes from status.json** when it is there. The log's alert subjects are used only in the fallback. The
  log is still read for the panel and for "email failing".
- **Stale is RUNNING only**, as the prompt says. The watch task rewrites status.json while idle too
  (`cc-autopilot.ps1:306`), but only when ENABLED exists, so an old file while OFF is normal.
- **CHANGELOG**: a new `2026.10.14` section with one Staff line; VERSION bumped from 2026.10.13.13. If P95 also
  finishes today it should add to it while uncommitted, or start `2026.10.14.2`.

## For Chase

1. **Autopilot will not commit P94 (`cc-autopilot.ps1:423`).**
   - My first P94 STOPPED (06:01) set `lastHandled` to 94 (`:413`). P94 was then handed again (06:23), and Hand-Off
     (`:273-276`) does not reset `lastHandled`.
   - When this session ends with `P94 DONE`, `:423` sees `94 = lastHandled` and treats it as "already committed".
     `current` is still P94, so it does nothing: no commit, no hand-off, no email (`:425-426`). The queue stalls
     silently with P95-P103 waiting, and the tile will keep saying RUNNING P94.
   - **Do now:** commit P94 from the Console's Commit tab. Then either set `"lastHandled": 93` in state.json before
     P94 DONE is read, or clear `current` and say go to start P95.
   - **Fix** (one line in each branch): treat a prompt as already handled only when it is not the one running.
     - `:412`: `if ($n -eq [int]$state.lastHandled -and $state.current -ne "P$n") { exit 0 }`
     - `:423`: `if ($n -eq [int]$state.lastHandled -and $state.current -ne "P$n") {`
     - Or reset `lastHandled` in Hand-Off when it hands a number at or below it.
2. **P93's five false "NEEDS YOU: stopped mid-task" emails (`cc-autopilot.ps1:499-503`).**
   - **Cause, proven from P93's transcript** (`C:\Users\ckfle\.claude\projects\D--UO-shard-migration\c598dd1c-....jsonl`):
     at 22:14:36-22:15:38Z P93 started five subagents with `run_in_background: true`. It then ended its turn to wait
     for them at 22:16:34, 22:20:19, 22:21:05, 22:21:33 and 22:23:22Z. Each turn end fires the Stop hook. With no
     `P93 DONE` in the last message, `:499` reads it as a question and emails. The five stop_hook_summary times match
     the five log lines (17:16:33-17:23:21 local) one for one. The real DONE came at 22:29:16Z.
   - **Fix:** before the email at `:499`, check the transcript (already read by `Get-LastText`, `:118-127`) for
     background agents started since the hand-off with no `<task-notification>` naming their `tool-use-id` yet. If any
     are still out, log `P93 waiting on N background agent(s)`, write status `waiting on background agents`, and exit
     without email.
   - **Cheaper alternative:** add to the hand-off text (`:291-294`) "run subagents in the foreground
     (run_in_background: false)". This also helps the stall watch, which sees no tool use while CC waits.
3. **Play-test results make the start check fail.** The play-test service (`docker/test-queue/server.py:60`,
   `importer_loop`) and the play-test page both write `testing/play-tests.json` and `testing/SUMMARY.md` straight into
   shard-migration, after a commit or whenever a result is recorded. Any prompt whose "Before you start" rule stops on
   files that are not its own will stop on them, as P94 did at 06:01. Either:
   - prompts treat those two files as expected, or
   - autopilot runs the import right after its commit and commits the two files with the prompt.

## Preflight

`Commit-ShardWork.ps1 -DryRun` (06:49). Docs also lists `testing/play-tests.json` and `testing/SUMMARY.md`: the play-test service imported this notes file, as For Chase item 3 describes. Those two files are expected.

```
Repo Result
---- ------
code dry run
docs dry run
```

No file over 5 MB: the largest new file is the status fixture, about 1 KB. Nothing scratch is in either repo; the
test-edit script was in the session scratchpad.

P94 DONE
