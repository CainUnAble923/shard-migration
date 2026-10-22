# cc-P274: the Fable week tracked like the main week, and a marathon-only fallback

## In plain words

- claude.ai has stopped showing a separate Fable line on its usage page, so the reader cannot see the Fable week
  there. The Golem now has a second way to tell: when a Fable session hits a usage limit while the 5-hour window and
  the main week still have room, the Golem treats the Fable week as full until the weekly reset. On 10-21 it had no
  way to see that at all.
- Once the Fable week is full, Fable prompts wait for the Fable reset and Bronze rests. With marathon mode on, those
  prompts run on Opus instead, as long as the main week has room. The prompt files keep their Fable Model line.
- The Golem tab on the console and the web console show the Fable week with its reset time, or say why it is
  unknown. The usage projection now starts with both weeks, for example "week 14%, Fable unknown: on track for ...".
  The overseer posts that same line in check-ins. When the Fable week will run out early, the Claude Code status line
  shows "Fable out Mon 6:00 PM", and the Golem notifies you once.
- Nothing for you to do. Optional: if claude.ai ever shows a Fable line again, the reader already records it. I left
  a suggested two-line tweak to the reader's instructions below for the overseer.

## What was asked, what was done

| Part | Done | Where |
|---|---|---|
| 1. Read the Fable week | Golem side: `fableWeek` read as `{pct, resets}` or `{pct, resetsAt}`; usage.json `fable` as a second source (status line window naming Fable, or a Fable limit hit). The reader itself was **not changed** (see Deviations): the page shows no Fable line, which is said everywhere the Fable week appears | `D:\UO\golem\golem.ps1` (`Get-PlanUsage`, `Get-Usage`, `Set-FableLimitHit`, StatusLine) |
| 2. Pace | A Fable prompt holds at `usageLimitPct` of the Fable week (or a limit hit) until the Fable reset; ahead of its even pace as before (cc-P160). Projection text names both weeks. Warning once when Fable runs out before its reset | `Get-PaceCheck`, `Get-UsageProjection`, `Update-FableWarning`, StatusLine |
| 3. Fallback, marathon only | `Resolve-FableFallback`: Fable prompt, marathon on, Fable week full, the week allows Opus: Opus. At hand-off, self-wake and the night shift's model pick; logged once per Fable week; Model line never rewritten. Outside marathon: rests until the Fable reset | `golem.ps1` |
| 4. The console | Fable row from usage.json when the plan page has none (with its reset time and why); projection lines labelled `projection:` with a `Fable:` warning line; web console the same | `D:\ShatteredLegacy\scripts\Shard-Console.ps1`, `web-console\static\app.js` |
| 5. Overseer reports | `status.json` `projection.text` now starts "week N%, Fable M%: ..." (or "Fable unknown", "(limit hit)"); the overseer's check-ins read that line | `Get-UsageProjection` |
| 6. Undo the overnight edits | **Already done** by the overseer's 16:05 task on 10-21 (`golems.json.bak-20261021-1605`, prompts commit b51df3d). Checked 10-22 09:50: Bronze lane is `Fable`; no queued, claimed or handed prompt has a "was Fable" Model line (only this prompt mentions the words) | nothing changed |

## Evidence the page shows no Fable line

- `D:\UO\golem\plan-usage.json` (read 2026-10-22 08:37): `"fableWeek": null`.
- The reader's run of 10-22 13:37 UTC (`cse_01Caek5dpMyiGDkngNEqeWZ3`, routine `trig_01UtCQyHYGFQ7NNtLrdC4fiH`): the page
  text reads "Current session ... This week ... Resets Wednesday 4:00 PM, 13% used, Limit resets ..." and the run
  ends "Fable not shown".
- `usage-history.jsonl`: the Fable figure last appeared at 10-20 12:26 (10%) and is null from 10-20 14:26 on, so the
  line went away before the 10-21 05:00 outage.
- Claude Code's status line has no per-model window: `usage-raw.json` holds only `five_hour` and `seven_day`.
- The outage in the log: Bronze at 03:07 "pace: P237 handed; the Fable week is unknown (plan-usage.json has no Fable
  week), so not held for", then StopFailure "usage limit in P237". With this change, a second such stop (or one naming
  Fable) marks the Fable week full and the Golem holds Fable prompts to the reset.

## Design notes

- **Limit-hit rule.** A Fable session's `rate_limit` StopFailure counts as the Fable week only when usage.json shows the
  5-hour window and the week both under 99% (otherwise one of those explains it; the 10-21 03:07 stop happened while
  the 5-hour window was full and is correctly not counted). One alone is logged "possible Fable limit" and kept in
  `fable-limit-hits.json`. It is marked full if the error text names Fable or the week, or on a second stop 5 minutes
  to a day later. A passing 429 would otherwise rest a Fable lane for days.
- **Reset time for a limit hit**: the main week's reset. On 10-21 the overseer recorded both resetting at 16:00. If
  they ever differ, the mark ends at the week's reset and the next limit hit marks it again (unverified beyond 10-21).
- **"Warns once"**: read as one log line and one Windows notice per Fable week, the first time the projection says it
  runs out early. The Claude Code status line carries a short `Fable out <time>` segment while that holds.
- **Projection line**: the old line led with "on track for 86% by ..." and repeated "the week is at 34%". It now leads
  with both weeks and drops the repeat. The console label changed from `week      :` to `projection:` so it does not
  read "week: week 34%".

## Tests

Red first, then green. Each suite was run against the old code before the change.

**`D:\UO\golem\tests\Golem.Tests.ps1`**, four new facts plus one updated (P200's projection text). All run against a
scratch copy first, then the live file.

| Fact | Old golem.ps1 | New |
|---|---|---|
| `P274_Reader_TheFableWeekComesFromThePlanFileOrTheStatusLine` | FAIL | PASS |
| `P274_Pace_AFableLimitHitHoldsFablePromptsUntilTheReset` | FAIL | PASS |
| `P274_Fallback_MarathonRunsFableOnOpusOutsideItRests` | FAIL | PASS |
| `P274_Projection_NamesBothWeeksAndWarnsOnceWhenFableRunsOut` | FAIL | PASS |
| `P200_Projection_TheWatchRecordsSamplesAndStatusShowsIt` (new text) | FAIL | PASS |

The old script scored "6 checks passed, 22 failed" on `-Only P274`. The new one scores 28 passed, 0 failed, on both the
scratch copy and live `D:\UO\golem\golem.ps1` after the install.

Full suite on the new script: 1479 checks passed, 6 failed, in three facts:

- `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged` and `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly`
  **fail the same way on the untouched live script** (run 10-22 09:39 with `-Only`). They were failing before this
  change and are not caused by it. Worth a fix-up prompt.
- `P200_Marathon_WakesEveryAwakeGolemOnItsLaneAndOpensDaytimeHours` failed only because my scratch copy lacked
  `GolemPower.ps1`. After copying it, it passes (11 of 11).

**`D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1`**:

| Fact | Old console | New |
|---|---|---|
| `P274_UsageBarsShowTheFableWeekFromUsageJsonWhenThePlanPageHasNone` | FAIL | PASS |
| `P274_TheProjectionLinesNameBothWeeksAndTheFableWarning` | FAIL | PASS |
| `P200_TheGolemTabShowsTheProjectionMarathonAndWidenedHours` (label `projection:`) | FAIL | PASS |

The P125 and P160 usage-bar facts still pass. Full suite: 443 facts, 430 passed, 13 failed. The same 13 fail on
the committed (HEAD) console with my three files swapped back for the run, then restored and checked by md5. They
come from this work copy's environment and from other features (no `client-data\...\hues.mul` in a worktree, the
Haven links and site tiles, the player command list), not from this change:
`PlayerCommandsNeverAppearInTheWorldTab`, `RedMeansTestOnlyUnclassifiedOrAPlainRunThatDeletesAndNothingElse`,
`EveryWindowActionClickedDryHandsItsWindowModeDryRun`, `EveryWindowActionClickedForRealHandsItsWindowModeExecute`,
`WithTheToggleOnEveryWindowActionIsDryAndItsChildReadsDocker`, `P83_TheLinksOpenTheTwoPagesAndNothingElse`,
`P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo`, `P101_TheTileAndTheTabAreBuiltAndDrawn`,
`P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing`, `P107_LinksAndSitesPointAtHavenAfterTheCutoverAndAtThisPcBefore`,
`P135_TheFourArtChecksRunOnlyValidateArtReadOnlyAndReportExitOne`, `P135_TheChildLineCarriesTheVdFileBodyAndHuesFileAndOnlyDigitsForTheBody`,
`P135_EveryMapAndArtButtonRunHeadlessWithDryRunRunsNothing`.

**Web console**: `python -m unittest discover -s web-console/tests` style run of `test_web_console.py`: 24 tests OK
(1 skipped). No new test covers the two changed `app.js` lines (no JavaScript runner on this PC: `node` is not
installed). The change only renames "The week:" to "Projection:" and adds a "Fable:" line when `fableWarning` is set.

## Files changed

- `D:\UO\golem\golem.ps1` (backup `golem.ps1.bak-20261022-P274`), `README.md` (`.bak-20261022-P274`), `tests\Golem.Tests.ps1`
  (`.bak-20261022-P274`). `D:\UO\golem` is not a git repo, so these are live now and reach the other PCs with the
  Tinker's next kit snapshot. Before installing I checked that the live `golem.ps1` was byte-identical to the copy I
  started from (md5 2631...5c50). The install was a same-folder copy and rename.
- `D:\ShatteredLegacy\scripts\Shard-Console.ps1`, `scripts\tests\Shard-Console.Tests.ps1`, `web-console\static\app.js`
  (in this Golem's work copy, for the Golem's commit).
- New runtime files the Golem may write: `D:\UO\golem\fable-warning.json`, `fable-limit-hits.json`, and a `fable` key in
  `usage.json`.

## Deviations and decisions for Chase

1. **The plan usage reader was not edited.** It is the claude.ai routine "Golem plan usage reader". Its instructions
   already say to write `fableWeek` from a Fable line and null when there is none, so it will pick a Fable line up if
   the page shows one again. I did not change the routine because an update replaces its job configuration through an
   API whose merge rules I could not check. A wrong update would stop the reader, and every Golem paces on it. The
   Golem reads `resetsAt` as well as `resets`, so nothing on the Golem side waits for the reader. **Suggested tweak for
   the overseer** (optional; it only helps if the page ever shows Fable outside the first 1,500 characters):
   - step 1: read `t.slice(i,i+4000)` instead of `t.slice(i,i+1500)`;
   - step 3: after "If the Fable line is missing, set fableWeek to null." add: "Also write `\"fableShown\": true|false`
     (whether the page names Fable anywhere)."
2. **Part 6 needed nothing.** The overseer's 16:05 task reverted it on 10-21. That was checked again here.
3. **The limit-hit reset time is the main week's**, an assumption from 10-21 (both reset at 16:00).
4. **Two P184 facts fail on the live script before this change** (above). Not touched here.

P274 DONE
