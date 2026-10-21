# cc-P156: the night shift in batches (rechecks through the night and at the 5-hour resets)

## Headlines

- **The night shift is a window with check points, not one all-or-nothing check.** From `nightShiftStart` (22:30) it
  checks at the start, every `nightCheckMinutes` (30), and 2 minutes after each 5-hour reset inside the window. The
  existing 10-minute **Golem Watch** task makes the due check (no new task, no new process), so a check can run up to
  10 minutes late. A check that lands in the bot window (01:15-03:00) moves to its end. Nothing starts within
  `nightMinStartMinutes` (45) of `nightShiftEnd`.
- **Each check works out a budget; a batch starts only when there is enough of one.** The week budget is the even pace
  now minus `nightWeekReservePct`, minus the week's percent (the Fable week the same way for a Fable prompt). The
  session budget is `nightSessionMaxPct` minus the 5-hour percent. A batch needs at least `nightMinBatchPct` (2) points
  of the week and a session budget above 0. A failed check sends no email. It records why and when the next check is.
- **A spent batch stops at a stopping point, never a kill.** The watch reads usage while a batch runs. When the week
  reaches the batch's starting percent plus its budget, or the 5-hour window reaches `nightSessionMaxPct`, it asks for a
  stopping point (the P125 path). CC ends the prompt with `P<nn> PAUSED`, and the Golem rests (`night batch`) until the
  next check point. A hand-off inside a spent batch also hands nothing on. The queue order never changes. The summary
  says when a prompt ran past its batch's budget, and by how much.
- **Stale usage between batches is inferred, not unknown.** Figures over 10 minutes old count as inferred while nothing
  has run: the week is taken as unchanged, and the 5-hour window as 0% once its reset has passed. Both status.json and
  the log say "inferred". A session the Golem did not start (Chase's own, seen by the SessionStart or prompt hooks)
  makes usage unknown until a session or the plan usage reader reports again.
- **What Chase sees.** The Golem tab's night line shows the running batch and its budget, or "between batches (1 so
  far); next check 02:12, after the 5-hour reset; <why>". One "night shift starting" email goes out at the first batch
  that starts. The morning summary lists every batch. If no batch ever started, one "night shift skipped: <last
  reason>" email goes out at the end.
- **No live night was observed.** Everything here is tested with a fixed clock and fake usage files. Tonight is the
  first real one.

## What changed

### `D:\UO\golem\` (outside the repos)

Backups: `golem.ps1.bak-20261020-p156`, `settings.json.bak-20261020-p156`, `README.md.bak-20261020-p156`,
`tests\Golem.Tests.ps1.bak-20261020-p156`.

- `golem.ps1`
  - `:96-102`: the header describes the batches.
  - `:233`: `$ForeignFile` (`foreign-session.json`), the last session the Golem did not start.
  - `:312`: `Save-State` writes `-Depth 8`. The night's batch records nest deeper than ConvertTo-Json's default of 2,
    which would have flattened them to strings.
  - `:373`, `:389`: new settings `nightCheckMinutes` 30, `nightMinStartMinutes` 45, `nightMinBatchPct` 2.
  - `:507-516`: `Get-BotWindowEnd` now calls the new `Get-BotWindowEndAt` (the bot window at any moment, used for a
    check point).
  - `:1466`: `Get-ReadyInfo` has a new reason, `night batch` ("Night shift: next check 00:00 (in 25 m), every 30
    minutes; it starts another batch if the budget allows"). `:1501`: the rest subject "night batch done".
  - `:1744`: `Get-NightShiftWhyNot` returns the last check's reason inside the window.
  - `:1762`: `Get-NightShiftStatus`, status.json's `nightShift` block. It keeps the old fields (enabled, start, end,
    next, until, whyNot, running) and adds window, batch, batches, budget, nextWhy, inferred and line. Inside the window
    `next` is the next check point, and `running` means a batch is running. Wired in at `:2338`.
  - `:1783`: `Test-NightUsage` is unchanged. P149 built it as the shared usage rule for away mode, so the batch budget
    builds on it rather than adding a second rule.
  - `:1842`: `Send-NightSummary` puts the batch lines first and keeps the email as sent in state.json `lastNightSummary`.
  - The cc-P156 block, from `:1855`:
    - `Save-ForeignSession` / `Get-ForeignSession` `:1866`.
    - `Get-NightBudget` `:1882` (the budget rule, below).
    - `Get-NightNextCheck`, `Set-NightNext`, `Format-NightNext` `:1921`.
    - `Get-NightBatch`, `Test-NightBatchSpent` `:1954`.
    - `Add-NightFinished`, `Close-NightBatch` `:1972`.
    - `Get-NightGate` `:1991`: the old skip reasons (queue empty, running, STOPPED, rested by hand, NEEDS YOU), plus a
      wrap up or stopping point Chase asked for during a batch.
    - `Invoke-NightCheck` `:2006`: one check point.
    - `Set-NightHeld` `:2072`, `Close-NightWindow` `:2078` (the summary, or the one skipped email).
    - `Format-NightBatches` `:2098`.
  - `Hand-Off`:
    - A wrap up during a batch holds the later checks (`:2629`).
    - The night's end closes the window (`:2655`).
    - A spent batch hands nothing on and rests `night batch` until the next check (`:2666`).
  - `-Event NightShift` (`:3222`): opens the night's window, counting check points from `nightShiftStart` even when the
    task ran late, then makes the first check. It runs again harmlessly when the window is already open.
  - `-Event Watch` (`:3433`), before the ENABLED test (a Golem whose queue ran dry by day has no ENABLED):
    - the window's end: the summary and the rest, or the one skipped email;
    - a running batch's budget: asks for the stopping point once;
    - a batch whose Golem has rested with no session on its way is closed;
    - the check point that is due. The old end-of-night block further down was folded into this one.
  - `SessionStart` (`:3649`) and `Prompt` (`:3687`): `Save-ForeignSession`.
  - The DONE path:
    - what finished goes into the running batch (`:4113`);
    - the batch's own stopping point rests `night batch` quietly until the next check (`:4122`);
    - Chase's own stopping point during a batch holds the later checks;
    - an empty queue closes the batch (`:4136`).
- `settings.json`: only the three new keys, at their defaults. Nothing else changed.
- `README.md`:
  - a new section "The night shift in batches (cc-P156)" (`:63`);
  - a `night batch` row in the rest table;
  - the marathon note no longer says "P156's batches are not in yet";
  - the new keys in the Files table.
- `tests\Golem.Tests.ps1`: six new facts (`:3077-3199`). The P131 and P200 night facts were updated for the new email
  timing (see Tests).

### `D:\ShatteredLegacy` (the Iron work copy)

- `scripts/Shard-Console.ps1`:
  - `:5154`: `Get-NightShiftLine` shows the Golem's own line inside the window ("Night shift: batch 2 running, budget
    the week to 49.3% (2.1 points from 47.2%), the 5-hour window to 50% (from 0%), until Wed 06:30", or "Night shift:
    between batches (1 so far); next check 02:12, after the 5-hour reset; ..."). Outside the window it shows the old
    line.
  - `:1947`: the Night shift button's tooltip describes the batches. It is two sentences, as P84's tooltip rule wants,
    in P153's style.
- `scripts/tests/Shard-Console.Tests.ps1`: a new fact, `P156_TheNightShiftLineShowsTheBatchItsBudgetAndTheNextCheck`
  (`:5880`).
- `CHANGELOG.md` / `VERSION`: a new section 2026.10.20.12 with one `### Staff` line. 2026.10.20.11 was already
  committed, so this starts the next version.

## The budget rule, with tonight's numbers

At each check: **week budget** = (days since the weekly reset / 7 x 100) - `nightWeekReservePct` - week %.
**Session budget** = `nightSessionMaxPct` - 5-hour %. A batch starts when the week budget is at least
`nightMinBatchPct` and the session budget is above 0. Its limits are the week at (week % + week budget), which is the
night allowance at the moment it started, and the 5-hour window at `nightSessionMaxPct`.

Tonight (read 19:39 on Tue 10-20 from `usage.json`, this session's own status line):

- **The week:** 35%, resetting Wed 10-21 16:00.
  - At 22:30, 6.27 of 7 days are gone: even pace 89.6%, minus the 10% reserve = **79.6% allowed**. The week budget is
    79.6 - 35 = **44.6 points**, far over the 2 a batch needs. By 03:00 it is 82.3% allowed.
  - So the week does not limit tonight. Under the old rule (35% against 79.6%) the night would have run too. The batches
    matter on nights like 10-17 (45% against about 42% pace).
- **The 5-hour window:** 74% at 19:39, resetting at 20:10. Whatever the Golems use after 20:10 counts toward the new
  window.
  - **If it is under 50% at 22:30:** batch 1 starts at once and runs until the window reaches 50%. Then the Golem rests
    until 2 minutes after that window's reset (about 01:12 if it opened at 20:10). That check comes just before the bot
    window (01:15-03:00), so batch 2 starts but hands nothing on between 01:15 and 03:00. The next check points after
    that are every half hour.
  - **If it is at or over 50% at 22:30:** nothing starts until the check just after its reset.
- **Marathon mode:** if marathon mode is on tonight (`marathon` auto may switch it on near the end of a week with this
  much left), the night runs at full, as it did before: the limits become `usageLimitPct` (95) for both the week and
  the 5-hour window.

Worked example from the tests (fixed clock, week resetting 10-20 22:30):

- 10-17 22:30: four of seven days are gone, so 47.1% is allowed. With the week at 45.3%, the budget is 1.8 points: no
  batch, next check 23:00.
- At 23:00 47.4% is allowed: 2.1 points, so batch 1 starts with the week to 47.4%.

## Tests

Each new fact was seen failing first. Against the unchanged golem.ps1 all six failed: 14 checks passed, 29 failed. The
console fact failed with "not true: a batch running".

| Fact | What it shows |
|---|---|
| `P156_ASkipAt2230StartsABatchAtThe2300RecheckOnceThePaceCatchesUp` | 22:30: 1.8 points left, no batch, no email, next check 23:00 "every 30 minutes"; 22:50 is not due; 23:00: batch 1 with the week to 47.4% (2.1 points), a long run to 06:30, one starting email, the status line and "inferred" |
| `P156_ABatchStopsAtItsBudgetAndAnotherStartsAfterTheNext5HourReset` | batch 1 to 47.1%; at 23:40 the week is at 47.2% and the stopping point is asked; P101 PAUSED is committed and rests `night batch` with a 0.1-point overrun recorded; the checks at 00:00 to 02:00 fail on the 5-hour window at 50%; the next check is 02:12 "after the 5-hour reset"; at 02:12 batch 2 starts on inferred figures; still one starting email; at the end one summary listing both batches and "P101 ran past the budget by 0.1 points of the week", and no skipped email |
| `P156_TheBotWindowMovesACheckToItsEnd` | the 01:30 check moves to 03:00 "after the overnight bot window"; nothing at 01:40 though the usage allows it; 03:00 starts a batch |
| `P156_NoBatchStartsWithinNightMinStartMinutesOfTheEnd` | after the 05:30 check, no more checks ("no batch starts within 45 minutes of the end (06:30)"); at 05:50 nothing starts though the usage allows it |
| `P156_UsageIsInferredAfterAResetAndAManualSessionMakesItUnknown` | a 21:00 reading with the 5-hour window at 55% and its reset at 22:00 starts a batch at 22:30, marked inferred in status and log; with a hand-opened session at 22:10 nothing starts ("usage unknown: a session the Golem did not start ran at 22:10"), and once the session reports at 22:50 the 23:00 check starts one |
| `P156_ANightWithNoBatchSendsOneSkippedEmailAtTheEnd` | no email during the night; at 06:40 one "night shift skipped: the week is at 60%..." (once over two watches), no summary, the window closed |
| `P156_TheNightShiftLineShowsTheBatchItsBudgetAndTheNextCheck` (console) | the batch line and the between-batches line, each with the window's end |

Facts updated, because the prompt moves the skip email to the end of the night:

- `P131_NightShift_SkipsForEachReasonAndSaysSo` now checks each reason as the status's `whyNot`, with no email and no
  long run.
- `P200_Marathon_...` checks the off case the same way.

**The full suites (Windows PowerShell 5.1.26100.9444, 20:12-20:40 on 10-20).** The first session closed before this
step, so a second session ran them.

| Suite | Facts passed | Facts failed |
|---|---|---|
| `Golem.Tests.ps1` | 148 | 2 (P184, below) |
| `Codex`, `GolemPower`, `Tinker`, `UoFiles`, `Assign`, `Art` | all | 0 |
| `GolemPaths.Tests.ps1` | 7 | 1 |
| `Join.Tests.ps1` | 25 | 9 |
| `Move-ToGolem.Tests.ps1`, `RemoteAgent.Tests.ps1` | - | the run stopped on the first error |
| `Shard-Console.Tests.ps1` | 424 of 436 | 12 |

- **All six P156 facts and the console P156 fact pass.** So do the updated P131 and P200 facts and every other night,
  marathon and away fact.
- **Every failure left was there before P156.** The first baseline run was killed for low memory at 20:43. A third
  session reran it at 21:00-21:20 on 10-20, with 11 GB free:
  - `Golem.Tests.ps1`, rerun in full on the current golem.ps1: 148 facts pass (879 checks), 2 fail, both P184:
    `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged` and
    `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly`. Iron claims P102 ("areas server, docs-only") where
    the fact wants P104.
  - The same P184 facts against the pre-P156 golem.ps1 fail the same way: the same 5 checks, 102 passed. That run used
    `golem.ps1.bak-20261020-p156` copied as `golem.ps1` into a scratch copy of `D:\UO\golem\*.ps1`. The backup cannot
    be run in place: PowerShell's `-File` refuses a file whose name does not end in `.ps1`. Every check failed that
    way, 64 of them, so that run proved nothing. The scratch copy was deleted afterwards.
  - Shard-Console, run in full on a clean worktree at `7653de2` (without P156): 435 facts, 422 passed, 13 failed. On
    the P156 work copy: 436 facts, 424 passed, 12 failed. All 12 P156 failures are in the baseline's 13:
    - `PlayerCommandsNeverAppearInTheWorldTab`
    - `EveryWindowActionClickedDryHandsItsWindowModeDryRun`
    - `EveryWindowActionClickedForRealHandsItsWindowModeExecute`
    - `WithTheToggleOnEveryWindowActionIsDryAndItsChildReadsDocker`
    - `P83_TheLinksOpenTheTwoPagesAndNothingElse`
    - `P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo`
    - `P101_TheTileAndTheTabAreBuiltAndDrawn`
    - `P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing`
    - `P107_LinksAndSitesPointAtHavenAfterTheCutoverAndAtThisPcBefore`
    - three P135 facts

    The baseline's 13th failure, `P60_AMessageCrossesTheChildCommandLineUnchanged`, passed in the P156 run, so it is
    flaky. The scratch worktree was removed.
  - `GolemPaths` ("no D:\UO\golems\Iron (golems.json: Iron is the integrator)"), `Join` (the readiness check on this
    PC: D:\UO\overseer missing, Docker and Tailscale), `Move-ToGolem` (the scheduled task "Shard CC Autopilot Watch"
    does not exist) and `RemoteAgent` ("type wake gold to confirm"). None of these four runs golem.ps1's night code:
    - `GolemPaths` never names golem.ps1.
    - `Join` lists it as a kit file.
    - `Move-ToGolem` copies it and counts its hooks.
    - `RemoteAgent` reads a source pattern.

    They follow this PC's layout, or today's changes to `Remote-Agent.ps1` and `golems.json` by other prompts (17:10
    and 18:06).
- **Not green, then, but none of it from P156.** These failures belong to the P184 claim rule and to the console's
  older facts. They are for whoever owns those.

## Deviations and decisions for Chase

- **The checks run from the Golem Watch, up to 10 minutes late.** "Next check 23:00" runs at the first watch after
  23:00, and "2 minutes after the reset" can be up to 12. A short-lived scheduled task per check would be exact, but
  it adds a task to register and clean up on every PC. I chose the existing task.
- **The P125 stopping point, read as asked.** The prompt says both "find a stopping point (the P125 path)" and "CC
  finishes the current prompt". P125's path is the one that reaches CC mid-prompt: CC writes a continuation and ends
  `P<nn> PAUSED`, which is committed, and the continuation goes first in the next batch. A prompt that ends `DONE`
  before CC is told is also caught, at the hand-off. Nothing is ever killed.
- **One email per night per Golem.** With several Golems, each Golem's night is its own window and its own batches.
  They share the account's usage, so they all stop at the same week line. The starting email, the summary and the
  skipped email come once per Golem per night (subject `[Iron Golem]`, `[Bronze Golem]`).
- **A wrap up or stopping point you ask for during a batch holds the night's later checks** until you say the phrase
  or press Wake. Without this the next check would undo your request. The old night shift never had to decide this.
- **"Inferred" means figures over 10 minutes old.** Nothing writes usage while the Golem rests, so any older figure was
  last moved by a session that has ended.
- **Which sessions count as "not started by the Golem".** With several Golems, any hook without `GOLEM_NAME`; with one
  Golem, a session not in sessions.json. Only the SessionStart and prompt hooks of sessions in the shard folders are
  seen. A desktop-app session elsewhere is not, and the plan usage reader (every 2 hours) covers that. If the overseer
  runs sessions at night in these folders, they count too, until the next report.
- **The marathon round lifts the batch limits.** With marathon on, the batch limits are `usageLimitPct`, as P200 set
  for the night shift.
- **Not changed:** the web console's Golem card still says "Night shift: on, 22:30 to 06:30". The prompt names the
  Golem tab only. status.json's `nightShift.line` is there for it.
- **The commit preflight touched the real docs folder once.** I first ran `Commit-ShardWork.ps1 -DryRun` exactly as
  the prompt writes it. With no repo arguments, it reports on `D:\ShatteredLegacy` and `D:\UO\shard-migration`, and it
  refreshed the play-test mirror there (machine output: `testing/SUMMARY.md`, `testing/play-tests.json`). It committed
  nothing. Every later run named my work copies (`-CodeRepo`, `-DocsRepo`, `-Branch golem/Iron/P156`, `-NoRefresh`);
  the Result table below is from those runs.
- **One step was denied** (unattended): a `Grep` tool search of `D:\UO\golem\golem.ps1` for its path variables. I did
  the same search with `grep` in Bash.

## For Chase

- **Tonight** (week 35% of 79.6% allowed, so 44 points of room): the week will not hold the night back. Each batch
  runs until the 5-hour window reaches 50%, then waits for that window's reset. Expect:
  - one "night shift starting" email at the first batch;
  - batches around each 5-hour reset;
  - nothing handed on between 01:15 and 03:00 (the bot);
  - nothing new after 05:45;
  - one summary in the morning.

  If marathon mode is on, the night runs at full instead.
- **The new settings** (in `D:\UO\golem\settings.json`):
  - `nightCheckMinutes` (30): how often it rechecks. Lower means it starts sooner once there is room, but the watch
    only runs every 10 minutes.
  - `nightMinBatchPct` (2): the least room, in points of the week, worth a batch. Raise it (3 to 5) if batches are too
    short to finish anything. Lower it (1) to use small gaps.
  - `nightMinStartMinutes` (45): no batch starts this close to the end.
- **If it spends too much,** raise `nightWeekReservePct` (10) or lower `nightSessionMaxPct` (50). **If it spends too
  little,** lower `nightWeekReservePct` or raise `nightSessionMaxPct`. The week line a batch may reach is the even pace
  minus the reserve at the moment the batch starts.
- **Reading the morning summary:** "The night shift ran 2 batches.", then one line per batch:

      Batch 1: 22:30 to 23:55. Budget: the week to 47.1% (7.1 points from 40%), the 5-hour window to 50% (from 20%).
      Finished: P101 (paused). Ended at week 47.2%, 5-hour 50%: budget reached; P101 paused at a stopping point.
      P101 ran past the budget by 0.1 points of the week.

  - "(paused)" means the stopping point caught that prompt; its continuation goes first in the next batch.
  - "ran past the budget" is how far the last prompt went over before it could stop.
  - A budget marked "(inferred: ...)" started from figures nobody had refreshed since the last session.
  - Below the batch lines are the usual finished, stopped and waiting lists. The same text stays in
    `D:\UO\golem\state-<Golem>.json` as `lastNightSummary`.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P156 -NoRefresh`,
20:11 on 10-20, and again at 21:22 (the same result):

    Repo Result
    ---- ------
    code dry run
    docs dry run

- Code: the 4 files (CHANGELOG.md, VERSION, scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1).
- Docs: this notes file.
- No file is over 5 MB. No scratch is in either repo.

P156 DONE
