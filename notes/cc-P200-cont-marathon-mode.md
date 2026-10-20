# cc-P200: marathon mode (use the whole week when we are on track to leave some unused)

2026-10-20. The Iron Golem (Opus, the integrator). Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P200-cont-marathon-mode.md`.
Builds on P160 (pacing), P162 (end-of-week spend), P156 (night shift), P183 (usage fallback), P184 (several Golems) and
P187 (the web console's parity rule). Not committed: the Golem commits after DONE. Both repos were clean at the start
apart from the overnight bot's machine output in `testing\`. No task-list tool is offered in this session, so progress
went to the chat. No server code changed, so there was no Docker build and no `sl-modernuo:cc-P200` image. No test
shard, Docker build, package or Haven action was run, so no lock was taken.

## Headlines

- **The projection.** Every scheduled watch (every 10 minutes) records one usage sample in
  `D:\UO\golem\usage-history.jsonl`. The week's burn rate is the change over this week's samples from the last 24 hours;
  with under 2 hours of samples it falls back to the week's average so far. Carried to the reset, that gives a line like
  "on track for 82% by Wed 4:00 PM (the week is at 60%, 0.5% an hour over the last 24 h; 3 enabled Claude Golems); the
  Fable week on track for 40%". It shows on:
  - the Shard Console's Golem tab (a new `week      :` line);
  - the web console's Golem page ("The week: ...");
  - `status.json` (`projection`);
  - the morning night-shift summary email.
- **Marathon mode** (`settings.json` `marathon`: `auto` by default, or `on` or `off`).
  - In `auto` it turns on when the projection falls short of `marathonTargetPct` (95) with more than `marathonMinHours`
    (6) left. It turns off when the projection reaches 95% or the week reaches `usageLimitPct`.
  - Each switch is logged and emailed once ("Marathon on: projected 71% by Wed 4:00 PM").
  - **While on:**
    - the watch wakes every awake, enabled Golem that has a prompt for its lane;
    - there is no rest after a Large prompt;
    - `maxPerRun` and `autoWakeMaxPerDay` are lifted;
    - pace runs as sprint (the week runs to `usageLimitPct`, with no even pace and no claude.ai warning);
    - the night shift runs at full (`usageLimitPct` instead of `nightSessionMaxPct`, and no reserves);
    - **the extra PCs may also claim during the day.** Their back-off still applies (owner using the PC, battery or
      heat, games). A Golem's `"noDaytimeMarathon": true` keeps it to its hours.
  - **The 5-hour window is still respected:** a Golem rests until it resets, then goes on.
- **The free reset.** When claude.ai offers a free full reset, the projection adds: "at this rate you reach 95% at
  <time>; press the free reset then and you have <h> hours to use it before the weekly reset". If the week will not get
  there, it says the reset is not needed this week. The Golem never presses it.
- **Keeping the queue fed.** While marathon is on and an awake Golem's lane has fewer than `marathonQueueMin` (6)
  prompts it could claim, the overseer address gets one email per Golem per spell ("queue running low for Bronze: 1
  Fable prompt left"). The Golem never writes prompts.
- **Buttons.**
  - Shard Console Golem tab: **Marathon: <mode> (set)** with an auto/on/off pick beside it; typed confirm
    `marathon <mode>`.
  - Web console: **Marathon on / auto / off** with the same words, through the console's own plan (P187's parity rule;
    twins added).
  - Command line: `Set-Marathon.ps1 -Mode auto|on|off`.
- **It is live already.** The real 12:26 watch on this PC ran the new code. It switched marathon **on** ("projected 11%
  by Wed 4:00 PM, short of the 95% target with 27.6 h left"), emailed Chase "Marathon on", and sent the low-queue email
  for Bronze (3 Fable prompts left; it went to Chase's address because `email.json` has no `overseer` yet). This is the
  feature working as asked (auto is the default), but it went live before this prompt was committed.
- **Tests.**
  - Golem: 8 new facts (58 checks), all seen failing first (38 checks failed against the unchanged Golem). Full suite:
    114 of 116 facts pass. The 2 failures are P184 facts broken by the overseer's own `parallelAreas` edit to
    `Golems.ps1` at 12:25 today, not by P200 (below).
  - Console: 3 new facts, seen failing first. Full suite: 418 of 424 pass, and the 6 failures were all there before the
    change.
  - Web console: 67 Python tests pass.
  - Mutations: 7 of 8 caught; the 8th is an equivalent mutant.

## What changed, with file:line

### `D:\UO\golem\` (outside the repos)

Backups: `golem.ps1`, `Golems.ps1`, `GolemPower.ps1`, `README.md`, `settings.json`, `golems.json` and
`tests\Golem.Tests.ps1`, each as `.bak-20261020-P200`.

`golem.ps1` (3,121 -> 3,443 lines):
- :132 header paragraph.
- :160, :193 `-Event MarathonSet` and `-Mode auto|on|off`.
- :218 `usage-history.jsonl`; :219 `marathon.json`.
- :299 `Send-Mail -To` (the overseer address).
- :352, :365 settings with defaults: `marathon` 'auto', `marathonTargetPct` 95, `marathonMinHours` 6,
  `marathonQueueMin` 6, `marathonHoldMinutes` 60.
- :612 `Get-PaceCheck`: marathon on runs as sprint. The 5-hour block is unchanged.
- :734 `Add-UsageSample`: one per watch, at most one per 9 minutes, last 300 kept.
- :758 `Read-UsageSamples`: one JSON parse for all lines.
- :773 `Get-WindowProjection`: 24 h of this week's samples (same reset time), restarting after a drop (a reset used
  mid-week); the week-so-far average under 2 h of samples; unknown in the first 3 h of a week; `reachAt`.
- :811 `Get-UsageProjection`: the text, the Fable week, the enabled Claude Golem count and the free reset advice.
- :841-:860 the marathon state, `Test-MarathonOn` and `Get-OverseerAddress` (`email.json` `overseer`).
- :867 `Update-Marathon`: the auto rule, the 60-minute hold (skipped at `usageLimitPct`), one log line and one email
  per switch.
- :911 `Send-QueueLow`: claimable per awake Golem (lane, Golem line, areas); once per Golem per spell; cleared when
  fed.
- :954 `Invoke-MarathonRound`.
- :1524 `Test-SelfWake`: the daily cap is lifted in marathon.
- :1545, :2049 `Get-ClaimCandidate` gets the marathon flag.
- :1701 `Test-NightUsage`: at full in marathon.
- :1748 the morning summary carries the projection, marathon and the reset advice.
- :1807, :1887 `status.json` `projection` and `marathon` (also in the aggregated `status.json` for several Golems);
  the cards get the marathon flag.
- :2035 the back-off gets `-Marathon`.
- :2077 the run cap is lifted in marathon (a long run's own cap still holds).
- :2124 no Large rest in marathon.
- :2668 `-Event MarathonSet`.
- :2760 the scheduled watch runs the marathon round once, before the per-Golem passes.
- :2859 marathon retries a pace-held wake now, but not one held by the 5-hour window.
- :2877 marathon wakes an awake idle Golem that has a prompt for its lane. It does not when: the Golem was rested by
  hand; it is winding down; it is resting for wrap up or a stopping point; or it opened a session in the last 10
  minutes.

Other files:
- `Golems.ps1`:
  - :89 validates `noDaytimeMarathon` (true or false).
  - :132 `Test-GolemHoursNow`; :137 `Test-GolemMarathonDay`.
  - :248, :253 `Get-ClaimCandidate -Marathon`.
  - :732, :784 the cards get `marathonDay` and `noDaytimeMarathon`.
  - The file is LF-only, as it was; I kept it that way.
- `GolemPower.ps1` :357 `Test-GolemBackOff -Marathon`: outside the hours no longer pauses it, and every other reason
  still does.
- `Set-Marathon.ps1` (new, CRLF): `-Mode auto|on|off` runs `golem.ps1 -Event MarathonSet`.
- `README.md`: the new "Marathon mode" section (including the daytime rule for the extra PCs), the Files table and
  the settings list.
- `golems.json`: one sentence in `_comment` about `noDaytimeMarathon`. No entry changed (checked against the backup).
- `tests\Golem.Tests.ps1` :2120-:2340: 8 facts.

### `D:\ShatteredLegacy`

`scripts\Shard-Console.ps1`:
- :239 `MarathonScript`.
- :1227 the action `golem.marathon` (Golem wake row).
- Tooltips for `golem.marathon` and `golem.marathonpick`.
- :3347 safety: `Set-Marathon.ps1` only with `-Mode auto|on|off`.
- :4178 the settings default (`marathon` auto); `ConvertFrom-AutopilotSettings` gains `Marathon`.
- :4252 the status gains `Projection` and `Marathon`.
- :4274 the card document gains `marathonDay`.
- :4393 the card line reads "hours 22:00-06:30 (all day now: marathon)" or "(kept: noDaytimeMarathon)".
- :4865 `Get-ProjectionLines`; :4872 `Get-MarathonLine`; both shown after the `end week` line.
- :5278 the web `when` kind `marathonNot`, plus the `marathon` input map.
- :5566 the plan: refuses the same or an unknown mode, phrase `marathon <mode>`, window `Set-Marathon.ps1 -Mode <m>`.
- :9283 the button text; the pick follows the setting.
- :9395 the web status document's `projection` and `marathon`.
- :10538 the pick into the facts.
- :11720 the pick control (`golem.marathonpick`).

Web console:
- `web-console\golem-actions.json` :42-:47: `marathon-on`, `marathon-auto`, `marathon-off` (fixed mode, `when`
  `marathonNot:<mode>`). They are the integrator's only, because marathon is one setting for the PC.
- `web-console\console-actions.json`: twins for `golem.marathon` and `golem.marathonpick`.
- `web-console\static\app.js` :172 the Golem page's "The week:", "Free reset:" and "Marathon:" lines; :223 the card's
  widened hours; :396 `marathonNot`.

Tests and patch notes:
- `scripts\tests\Shard-Console.Tests.ps1` :7920-:8000: 3 facts. In P131's wake-row fact, the expected order now
  includes `golem.marathon`.
- `CHANGELOG.md` and `VERSION`: a new `2026.10.20.2` with two Staff lines (2026.10.20 was already committed).

## Tests (each new one seen failing first)

**Golem.** `powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\Golem.Tests.ps1`

- **Baseline** (a frozen copy of the pre-change Golem): 108 facts, 596 checks, 0 failed.
- **Red:** the new tests against the unchanged Golem: 8 of 8 facts failed (14 checks passed, 38 failed).
- **Green:** after the change, all 8 pass (58 checks). Getting there took three fixes:
  - `[Math]::Max(0, x)` and `[Math]::Min(100, x)` pick PowerShell's integer overloads, which truncated rates and
    projections; I changed them to `0.0` and `100.0`.
  - In several-Golem mode the session name is "Golem Iron P101", so I fixed the fact's regex.
- **Full suite after the change:** 116 facts, 649 checks passed, 5 failed. The 5 failures are in two P184 facts:
  `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged` and `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly`.
  - They come from the overseer's edit to `Golems.ps1` at about 12:25 today (comment "overseer 10-20 (Chase 12:25)",
    `$script:GolemParallel` and `parallelAreas`), which made `server` and `server-patches` parallel areas.
  - The facts still expect two server prompts to overlap. `Test-AreasOverlap @('server') @('server','map')` is True on
    the pre-change copy and False now.
  - P200 did not touch that rule. I left it for whoever owns that change.

The new facts:
- `P200_Projection_MathOnRecordedSamples`:
  - 0.5% an hour gives 66% by the reset;
  - old samples and samples from another week are ignored;
  - a drop restarts the count;
  - 2% an hour caps at 100 and reaches 95% at 03:30;
  - the week-so-far fallback gives 0.35 an hour and 58.8%;
  - at the target, `reachAt` is now;
  - too early in the week is unknown.
- `P200_Projection_TheWatchRecordsSamplesAndStatusShowsIt`:
  - three watches record three samples (a fourth within 9 minutes is skipped);
  - `status.json` reads "on track for 86% by Wed 4:00 PM ...; the Fable week on track for 20%";
  - the free reset advice reads "reach 95% at Tue 6:30 PM ... 21.5 hours".
- `P200_Marathon_AutoTurnsOnBelowTargetWithHoursLeftAndOffAtTheTarget`:
  - on, with one email;
  - a second watch sends no email;
  - off at the target, with one email;
  - stays off with 5 h left;
  - off at once at `usageLimitPct` even inside the hold;
  - the hold keeps it on and logs why.
- `P200_Marathon_TheFiveHourWindowStillPauses`:
  - marathon hands a prompt despite the even pace and the claude.ai warning;
  - off, the same prompt is held;
  - the 5-hour window at 96% holds it, and so does the week at 96%;
  - a Golem held by the 5-hour window opens no session an hour on, and opens one after the window resets.
- `P200_Marathon_WakesEveryAwakeGolemOnItsLaneAndOpensDaytimeHours`:
  - with two Golems, Iron is woken for its Opus prompt and Bronze for its Fable one at 1 PM, outside Bronze's hours
    22:00-06:30;
  - the cards show Bronze `marathonDay`;
  - the low-queue email reads "queue running low for Bronze: 1 Fable prompt left";
  - `noDaytimeMarathon` keeps Bronze out;
  - with marathon off, nobody is woken;
  - `Test-GolemBackOff -Marathon`: the hours no longer pause it, battery still does, and `noDaytimeMarathon` still
    pauses it.
- `P200_Marathon_TheLowQueueEmailFiresOnce`:
  - one email, to the overseer address;
  - none on the next watch;
  - fed back to the minimum, there is no email and the flag clears;
  - low again, one more email;
  - with marathon off, none.
- `P200_Settings_DefaultAsStatedAndMarathonSetWritesOneKey`:
  - the defaults are auto, 95, 6, 6 and 60;
  - `-Event MarathonSet` on, off and auto write one key and keep the rest;
  - the switches are emailed once.
- `P200_Marathon_LiftsTheRunCapAndTheLargeRestAndRunsTheNightShiftAtFull`:
  - the run cap and the Large rest are lifted on and kept off;
  - the night shift with the session window at 60% and the week over its night pace is skipped when off and starts
    when on.

**Mutations** (a scratch copy, `-Only` the fact concerned):

| Mutation | Result |
|---|---|
| hold removed | caught |
| low-queue repeats | caught |
| daytime ignored | caught |
| noDaytimeMarathon ignored | caught |
| run cap kept | caught |
| night reserve kept | caught |
| a drop not restarting the rate | caught |
| 5-hour retry exclusion removed | missed, equivalent mutant |

The 5-hour mutation is equivalent: even when tried early, `Test-SelfWake` refuses at the 5-hour limit, so the
behaviour is the same.

**Console.** `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1`

- **Before the change**, with the new facts in: 424 facts, 414 passed, 10 failed.
  - Failing as expected: the 3 P200 facts and P131's wake row (red).
  - Already failing before P200: PlayerCommandsNeverAppearInTheWorldTab, P83 x2, P101 x2, P107.
- **After:** 417 passed, 7 failed. The 6 are the ones that already failed. The 7th was mine: P84's tooltip rule (at
  most three sentences); I shortened the Marathon tooltip.
  - A filtered rerun passes P84's tooltip fact, the 3 P200 facts, P131 and P187's twin rule (every new button and the
    pick have a web twin).
  - The two P84 look facts that fail in a filtered run fail the same way on the pre-change console (an ordering
    effect of filtering, not P200).
- `P182_WindowStepsRunInThisProcessForTheWebConsole` failed once in a filtered run while the Golem suite ran
  alongside. It passed alone and in the full run.

**Web console:** `python -m unittest discover -s tests` in `web-console`: 67 tests, OK.

## Deviations and decisions for Chase

- **There was no usage history to project from.** The Golem kept only the latest snapshot (`usage.json`,
  `plan-usage.json`), so I added `usage-history.jsonl` (one sample per watch). Until 2 hours of samples exist, the
  projection uses the week's average so far. Right now that **under-reads**: the week looks like it started this
  morning (1% at 10:24), but the average spreads 11% over the full 140 hours since the nominal week start. Today it
  reads "on track for 13%"; within 2 hours it switches to the real recent rate. It errs toward marathon on, which is
  the safe side for "use the week".
- **"With all enabled Golems counted".** The plan's usage is the account's, so every Claude Golem's use is already in
  the measured rate. The projection shows how many enabled Claude Golems there are. I did not model per-Golem rates;
  the 24-hour window covers both day and night patterns. Codex Golems are on ChatGPT and are not in it.
- **"Wake every enabled Golem".** It wakes Golems that are awake: their ENABLED file is present, they were not rested
  by hand, and they are not winding down or resting for wrap up or a stopping point. A Golem someone turned **off** is
  left off. Say if marathon should also turn OFF Golems on.
- **A 60-minute hold between switches** (`marathonHoldMinutes`) was added. Marathon's own burn raises the projection,
  which would switch it off, then the rate drops and it switches on again; the hold stops that flapping. At
  `usageLimitPct` it switches off at once.
- **6 hours or less before the reset**, auto does not turn marathon on, and if it is already on it stays on to the end.
- **`autoWakeMaxPerDay` is lifted in marathon** as well as `maxPerRun`. Otherwise the daily cap would stop the wakes.
  The 5-minute spacing still holds.
- **The overseer address.** `email.json` has no overseer address, so I added an optional `overseer` key. Without it the
  low-queue email goes to `to` (you) and says so. **Add `"overseer": "<address>"` to `D:\UO\golem\email.json`** to send
  these to the overseer.
- **Marathon is per PC.** Each PC's watch keeps its own samples and `marathon.json` from the same account-wide figures,
  so they agree as long as each PC has fresh usage readings. The remote PCs (Gold) need this new `golem.ps1`,
  `Golems.ps1` and `GolemPower.ps1` copied over (the join kit's usual update) before they widen their own hours.
- **Gold's hours.** The prompt says Gold is 22:00-07:00, but `golems.json` currently has `"hours": ""` for Gold (a
  `golems.json.bak-20261020-goldday` exists, so it was opened to the whole day earlier today). It already claims in
  the day either way. The Codex lanes Agapite and Verite are disabled, and Copper and Silver are disabled.
- **P162's code is missing from `golem.ps1`.** There is no `endOfWeekSpend` anywhere in `golem.ps1`, its backups, or
  `Golem.Tests.ps1`, though P162's notes describe it and the console still reads `endOfWeek`. It looks like it was
  lost when an earlier backup was restored on 10-17 or 10-18. Marathon's auto rule covers most of what it did (spend
  what is left when the week is short), but the console's `end week` line is now always empty. I did not restore it:
  that is outside this prompt.
- **The two P184 failures come from the overseer's `parallelAreas` edit** (above). Someone should update those two
  facts to the new rule.
- **It went live before the commit** (Headlines). To stop it before you review: `Set-Marathon.ps1 -Mode off` in
  `D:\UO\golem`, or Marathon off on either console.
- **The morning email's new lines are not seen by the tests.** `-NoMail` logs subjects only; I checked the body by
  reading the code.
- **Unattended permission denial.** The Read tool was denied for `D:\UO\golem\golem.ps1` (unattended run). I wanted to
  run `Read D:\UO\golem\golem.ps1 (offset 1200, limit 300)` to read the night shift and status code. I read it with
  `sed -n` in Bash instead, as the hand-off says, and made every edit with exact-match Python patch scripts from the
  scratchpad.

## For Chase

- **Where the projection shows:**
  - Shard Console, Golem tab: the `week      :` line (amber while under 95%), a `free reset:` line when one is on
    offer, and a `marathon  :` line (mode, ON or off, since when and why, who was told the queue is low).
  - Web console, Golem page: "The week: ...", "Free reset: ..." and "Marathon: ...".
  - The morning night-shift summary email.
  - `D:\UO\golem\status.json` (`projection`, `marathon`).
- **To force it on or off:**
  - Shard Console, Golem tab: pick auto, on or off beside **Marathon: <mode> (set)**, press it, and type
    `marathon on` (or off or auto).
  - Web console: **Marathon on / auto / off**, typing the same words.
  - Command line: `powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Set-Marathon.ps1 -Mode on`
    (`off`, `auto`). It prints "Marathon on: on now. The week: on track for ...".
  - `auto` is the default and turns itself on and off.
- **To keep one PC to its hours during marathon:** add `"noDaytimeMarathon": true` to that Golem's entry in
  `D:\UO\golem\golems.json`.
- **What the emails look like:**
  - "[Iron Golem] Marathon on: projected 71% by Wed 4:00 PM": why, the projection, what marathon does, when it turns
    off, the free reset advice if a reset is on offer, and how to force it.
  - "[Iron Golem] Marathon off: projected 96% by Wed 4:00 PM": why, and that pacing is back to normal.
  - "[Iron Golem] queue running low for Bronze: 1 Fable prompt left", to the overseer address (to you until
    `email.json` has `overseer`): how many prompts that Golem's lane could claim, the minimum, and the week's
    projection.
  - The morning summary ends with "The week: on track for ...", "Marathon: auto, on now." and, when on offer, "The free
    reset: at this rate you reach 95% at Tue 6:30 PM; press the free reset then and you have 21.5 hours to use it
    before the weekly reset (Wed 4:00 PM). The Golem never presses it."
- **Today:** marathon switched on at 12:26 on its own. You got the "Marathon on" email and a low-queue email for Bronze
  (3 Fable prompts left).
- **The web console** reads its pages fresh, but the installed server only picks up `app.js` changes after a reload of
  the page. No restart of the web console was done.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`:

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

P200 DONE
