# cc-P757: the night watch said "usage unknown" and never started work

Iron Golem, 2026-11-01. Kit changes in `D:\UO\golem` (not a git repo: scratch copy, red, green, md5, backup, install).
Docs copy `D:\UO\golems\Iron\shard-migration` and code copy `D:\UO\golems\Iron\ShatteredLegacy`, both on
`golem/Iron/P757`. Nothing committed, nothing deployed, Haven not touched.

## In plain words

- **The night shift no longer idles on an incomplete usage report.** Claude Code now reports only the week, and the
  claude.ai page shows no 5-hour figure either. Each night check said "usage unknown" and started nothing. Now it takes
  any missing figure from the plan usage page. When nobody reports a 5-hour figure, it goes by the week alone.
  golem.log says which source it used, for example
  `usage: the week from the status line, the 5-hour window not reported by the status line or the plan usage page`.
- **When both reports are out of date, it still runs one batch a night,** if the last known week figure is on pace.
  That batch's own session then reports fresh usage, and its budget is checked against that. The log line says
  `usage fallback: ...`.
- **A Golem always takes its own Run next pick.** On 11-01 at 03:27 Iron rested with P715 picked for it, because P715
  was marked for the Codex lane, and the Codex lane did not take it for two hours. Now the pick goes first.
- **Something to know:** the week is at 44% now, and the night pace allows 41.6% at 05:40. So a night check at this
  hour would still wait, correctly, for the pace. The log no longer calls that "usage unknown". Nothing for you to do.

## What happened on 11-01 (from golem.log and the two files)

- `D:\UO\golem\usage.json`, as the status line writes it now, has **only `sevenDay`**. Claude Code's `rate_limits` no
  longer carries a 5-hour window. `plan-usage.json` (04:24 read) has `"session": null` and a week of 44%.
- `Get-Usage` took windows only as a pair, from whichever file was newer. Either way `fiveHour` was `$null`, and
  `Test-NightUsage` refused on `-not $u.fiveHour -or -not $u.sevenDay`. So every check from 00:16 to 05:06 logged
  `no batch: usage unknown (usage.json has no 5-hour or 7-day window)`.
- So the brief's "fall back to plan-usage.json for the 5-hour figure" alone would not have helped: neither file had a
  5-hour figure. A missing 5-hour figure must not block the night.
- **03:27 (item 3).** P715 was Iron's Run next pick (RunNext 03:11). After P755 DONE, the hand-off's claim loop
  (`Get-ClaimCandidate`, `Golems.ps1`) skipped it: `claim: P715 is marked Codex OK and a Codex lane is on: left for it`.
  That rule is about a Codex Golem being enabled, not about a lane actually running. No other prompt was for Iron, so
  Iron rested ("queue empty after P755"). Verite skipped P715 every 10 minutes as "the Iron Golem's run next pick". Nobody
  took it until 05:13, when a new Run next (P756) replaced the pick. Resting was wrong: a Run next is a person's choice
  for that Golem, and it should win over the Codex-lane courtesy.

## What changed (kit, `D:\UO\golem`)

### 1. Each window from the source that has it (`golem.ps1`, `Get-Usage`)

- Windows still come from the newer file first, as before.
- New: a window the newer file lacks is taken from the plan page while that page is within `planUsageMaxAgeHours` (4).
  This covers usage.json with only `sevenDay`, and the plan page with `session: null`.
- New fields `fiveHourSource` and `sevenDaySource` (`status line`, `plan usage page`, or empty).

### 2. The night rule (`Test-NightUsage`, `Get-NightBudget`, `Invoke-NightCheck`)

- **No 5-hour figure anywhere:** the week decides. The 5-hour window is "not reported (not held for)", and the
  budget reads `the 5-hour window to 50% (its figure not known)`.
- **The source is logged.** On a started batch: `night batch 1 started (...): budget ...; usage: the week from the
  status line, the 5-hour window from the plan usage page`. On a refused check, `(usage: ...)` follows the reason. The
  batch record keeps it too (`usageSource`).
- **Neither file usable (item 2).** That means usage.json is missing or over `nightUsageMaxAgeHours` (24), and no plan
  page within 4 h has the week. Then:
  - The night check takes the last week figure either file holds, at any age, as long as its reset is still ahead
    (new `Get-LastKnownWeek`, the newer of the two).
  - It applies the usual night pace gate to that figure. If the figure passes, **one** batch starts, marked
    `usageFallback` in the batch record. Its log says `usage fallback: <why>; the week is the last known figure, 31%
    from the plan usage page at 16:30, the 5-hour window not known; one batch, its session reports fresh usage`.
  - A second check that night says `the one batch a night on the last known week figure has run (batch 1)`.
  - With no figure at all (no file, or the week has reset since), it is still "usage unknown", now with
    `; no week figure with its reset still ahead`.
- "Queued work for the Golem" is the existing gates: the queue is not empty, nothing STOPPED, not rested by hand. The
  self-wake then refuses when nothing in the queue is for this Golem, and in that case no fallback batch is recorded.
- Only the night budget takes the fallback (`Test-NightUsage -AllowFallback`). Away mode's all-day use of the same rule
  is unchanged.
- Once the batch's session runs, its status line writes fresh usage.json. Its budget (`Test-NightBatchSpent`) is then
  checked against real figures.

### 3. A Golem's own Run next pick (`Golems.ps1`, `Get-ClaimCandidate`)

- The claim loop reads this Golem's own RUN-NEXT (and `RUN-NEXT.after`).
- A prompt marked Codex OK that is this Golem's pick is taken, with the log line
  `claim: P715 is marked Codex OK, but it is Iron's own run next pick: taken, not left for the Codex lane`.
- Other Codex OK prompts are left for the lane as before.

## Tests

New facts in `D:\UO\golem\tests\Golem.Tests.ps1` (`-Only P757`, source `notes\cc-P757-tools\p757-facts.ps1`). Each
runs in a temp world with its own copies of usage.json and plan-usage.json, in the shapes the live files had on 11-01.
None reads the live files.

- `P757_1_TheNightCheckTakesTheWindowUsageJsonLacksFromThePlanPage`:
  - usage.json with only the week, plus a fresh plan page with a session: a batch starts, using the plan page's
    5-hour figure, and the source is logged;
  - a plan page 6 h old is not used;
  - the plan page alone (no usage.json) works.
- `P757_2_AFiveHourWindowNeitherSourceReportsIsNotHeldFor`:
  - the live shapes: a batch starts on the week alone;
  - the week at 60% still holds, with the source logged.
- `P757_3_NeitherSourceUsableStartsOneBatchWhenTheLastKnownWeekIsUnderPace`:
  - usage.json 30 h old and the plan page 6 h old: one batch on the newer figure, marked;
  - no second batch at the next check;
  - over pace: nothing starts;
  - no figure: still unknown;
  - only the night budget passes `-AllowFallback`.
- `P757_4_AGolemsOwnRunNextPickIsTakenEvenWhenMarkedCodexOk`:
  - Bronze, with RUN-NEXT-Bronze naming a Codex OK prompt while a Codex lane is enabled, takes it;
  - with no pick, it is left for the lane as before.
- P131's `usage old` case expected no batch for 25-hour-old figures still in their week. Those figures now get the
  fallback batch, so the case now uses a week that has reset since. P757_3 covers the fallback.

Results (files in `notes\cc-P757-tools\`):

- **Red** (the final facts against an unchanged copy of the kit): 2 checks passed, 20 failed, all four facts failed.
  Fact 1's log shows the exact 11-01 line. File: `red-golem-p757.txt`.
- **Green** on the installed kit: `-Only P757` 22 checks, 0 failed; `-Only P131_NightShift` 50 checks, 0 failed
  (`green-golem-p757-live.txt`).
- **The whole suites**, on scratch copies side by side (`golem-suites-summary.txt`):

  | Kit | Golem.Tests | Lane.Tests | Assign.Tests |
  |---|---|---|---|
  | Unchanged | 1665 passed, 25 failed | 65 passed | 3 passed |
  | Changed | 1682 passed, 8 failed | 65 passed | 3 passed |

  - Both kits fail the same 5 checks in P184's two Touches facts (P734 and P747 found them too).
  - The unchanged kit's other 20 are the new P757 facts.
  - The changed kit's other 3 are P131's old `usage old` case, updated as above (then 28 of 28).
- **Copies of the live files** (`live-copy-check.ps1`, output `live-copy-check.txt`). This copies today's usage.json
  and plan-usage.json to the scratchpad and runs the night rule from each kit at three clock times:
  - **Unchanged kit:** "usage unknown (usage.json has no 5-hour or 7-day window)" at 05:40 and 10:40, and "last
    reported 26 h ago" on 11-02 08:00.
  - **Changed kit, 05:40:** the week (44%) is ahead of the night pace (41.6%). The log says so, with the source.
  - **Changed kit, 10:40:** passes.
  - **Changed kit, 11-02 08:00 (both files stale):** passes on the fallback.

## Install

- I checked that the live files were unchanged since my pristine copy (md5), then backed them up as
  `golem.ps1.bak-20261101-P757`, `Golems.ps1.bak-20261101-P757` and `tests\Golem.Tests.ps1.bak-20261101-P757`.
- Each file was copied in as `.p757new`, md5-checked, then renamed over the live file.
- Installed md5s:
  - golem.ps1 `8C5615D5C0A2968344F6EE6097A9C68A`;
  - Golems.ps1 `D824276965DFA6BBEC4349FB009AA685`;
  - Golem.Tests.ps1 `D5FB05DAB7C9493B12CA0EED481B64BB`.
- The whole change is `notes\cc-P757-tools\p757.diff`.
- The other PC (Gold, Copper) gets the kit the usual way. I did not touch it.

## Code copy

- `CHANGELOG.md`: a Staff line under a new **2026.11.01** section.
- `VERSION`: 2026.11.01.
- Nothing else. P743/P755's unmerged 2026.10.31.11 is a different section, so these do not collide.

## Not verified

- Whether last night's week was on pace at 00:16-05:06. No log line records the week figure then, so I cannot say if
  a batch would have started. Now (05:40) the week at 44% is just over the night allowance.
- No live night check ran with the installed kit. The next one is tonight at 22:30. Its golem.log lines will show
  `usage:` or `usage fallback:`.

P757 DONE
