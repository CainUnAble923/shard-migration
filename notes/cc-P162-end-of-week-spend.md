# cc-P162: Use it or lose it at the end of the week

2026-10-17, Claude Code (Opus 5.5), handed by the Golem straight after P161 in the same session ("Golem P161",
process 27908). Prompt: `D:\UO\cc-prompts\cc-P162-cont-end-of-week-spend.md`. Both repos were clean at the start
(P161 committed as `2382843`). Read first: P160's notes. P156 (night shift batches) and P157 (plain-English emails) are
still queued, not DONE, so the night shift has no batches to use and the emails are in the Golem's usual style.

## Headlines

- **New window (`endOfWeekSpend`, on by default):** for the last `endOfWeekHours` (24) before the weekly reset, the
  Golem spends what is left of the week.
- **Inside the window, whatever `paceMode` says:**
  - hand-offs stop only at `100 - endOfWeekReservePct` (**97%**) of the week, or at the 5-hour window's
    `usageLimitPct` (95);
  - a Fable prompt also needs the Fable week under 97%, judged by the Fable week's own reset time;
  - claude.ai's pace warning is ignored.
- **Outside the window nothing changes**, in either paceMode.
- **Night shift:** inside the window it runs without its even-pace skip, and its session check is `usageLimitPct`
  instead of `nightSessionMaxPct`. There are no batches yet (P156 is not DONE).
- **Waking:** when the window opens while the Golem rests for pace, the 10-minute watch opens a session itself. After
  each 5-hour reset inside the window it wakes again if it had stopped for the 5-hour limit.
- **Fable:**
  - When the week is full but the Fable week is not, the rest reason says so: "the Fable week still has N% left, but
    every model counts toward the week, so it cannot be used".
  - The window email says whether any Fable prompt is queued.
  - The after-reset summary says when none was queued, so more prompts can be tagged Fable next week.
- **Shown:**
  - The Golem tab's new `end week  :` line: "End of week: spending what is left until Wed 4:00 PM (week 80%, 17% left;
    Fable week 45%, 52% left)", or when it opens next, or that it is off.
  - One email when the window opens; one summary after the reset ("End of week: what went unused").
- **Still never** uses a free limit reset or usage credits. P160's code paths for those are unchanged.
- **This week:** the week resets **Wed 10-21 4:00 PM**, so the window opens **Tue 10-20 4:00 PM**. The week was at 54%
  tonight.
- **Tests:**
  - Golem **421 of 423**. The 2 failures are clock-dependent facts from P125 and P131 that fail the same way on the
    pre-P161 script when run late in the evening (below).
  - 7 new P162 facts (50 checks), all seen failing against the pre-change script, plus 10 mutations each caught.
  - Console **380 facts, 375 passed, 5 failed**: the same 5 failures as before, plus 1 new P162 fact, seen failing
    first.

## What changed

### `D:\UO\golem\` (outside the repos; backups `golem.ps1.bak-20261017-p162`, `settings.json.bak-20261017-p162`, `README.md.bak-20261017-p162`, `tests\Golem.Tests.ps1.bak-20261017-p162`)

`golem.ps1` (2,434 -> 2,571 lines):
- :130 header paragraph. :268, :280 the settings `endOfWeekSpend` (true), `endOfWeekHours` (24) and
  `endOfWeekReservePct` (3). `paceMode` and the overseer's sprint lines are unchanged.
- :514 `Test-InEndWindow`: the setting is on, and the reset is in the future and no more than `endOfWeekHours` away.
- :518 `Get-EndOfWeek`: Active, Until, OpensAt, FableActive, FableUntil, Cap, WeekPct, FablePct. A stale plan read
  means the Fable week is not known.
- :533 `Format-Left`.
- `Get-PaceCheck`:
  - :556 inside the window, the week's allowance is the cap and blocks at >= 97%, back at the reset; otherwise it
    is cc-P160's rule unchanged.
  - :583 the Fable week, by its own reset.
  - :601 the warning is skipped inside the window (and said in a note).
  - :604 the Fable room note.
  - :605 `EndOfWeek` in the result.
- `Test-SelfWake`:
  - :1185 inside the window, a usage-limit rest gets the same allowance for older usage figures as a pace rest
    (nothing has run).
  - :1190 its own per-window `usageLimitPct` loop skips a week that is in its window; the pace check handles it.
- :1269 `Invoke-EndOfWeekWatch`: state.json `endOfWeek` (until, openedMailed, lastWeekPct, lastFablePct, fableUntil,
  fableQueued, summarySent). One email when the window opens; a self-wake ('end of week') while resting for pace or
  'usage limit'; the summary once the reset has passed. :2116 the watch calls it.
- :1349 `Test-NightUsage`: inside the window, the session is checked against `usageLimitPct` and the week and the
  Fable week against the cap.
- :1523 `status.json` gains `endOfWeek`: on, hours, cap, active, until, fableActive, fableUntil, opensAt, weekPct,
  fablePct.

Other files in `D:\UO\golem\`:
- `settings.json`: the three keys added; every other key kept.
- `README.md`: "Use it or lose it at the end of the week (cc-P162)" and the settings row.
- `tests\Golem.Tests.ps1` :1332-1465: the P162 facts.

### `D:\ShatteredLegacy`
- `scripts\Shard-Console.ps1`:
  - :4048 the status parser carries `EndOfWeek`.
  - :4428 `Get-EndOfWeekLine`: green while spending, gray when it opens next or is off.
  - :4697 the Golem tab's `end week  :` line.
- `scripts\tests\Shard-Console.Tests.ps1` :6978 `P162_TheGolemTabSaysWhenTheEndOfWeekWindowSpendsWhatIsLeft`.
- `CHANGELOG.md`: new version 2026.10.17.11 with three `### Staff` lines (2026.10.17.10 went out with P161).
  `VERSION` is 2026.10.17.11. The wiki page was not published.

## Tests (each new one seen failing first)

The P162 facts use a fixed clock: the week resets Wed 10-21 16:00, "outside" is Tue 15:00 (25 h before) and
"inside" is Tue 18:00 (22 h before). They use P160's fake usage.json and plan-usage.json and the CLI stub.
- `P162_EndOfWeek_OutsideTheWindowNothingChangesForEitherPaceMode`: five cases, each with the setting on and off and
  the same result each time, with no end-of-week wording:
  - pace at 89% held, at 85% handed, at 50% with the warning held;
  - sprint at 96% held, at 94% with the warning handed.
  Status shows the window off and opening at Tue 16:00.
- `P162_EndOfWeek_InsideAPaceHeldGolemHandsOffStopsAt97AndIgnoresTheWarning`:
  - 93% (pace would allow 89.9%) is handed; sprint at 96%, over usageLimitPct, is handed;
  - 97% is held "at the end-of-week cap ... until it resets; back at about Wed 4:00 PM";
  - 93% with the warning is handed;
  - a 96% 5-hour window still holds it.
- `P162_EndOfWeek_TheFableWeekGatesFablePromptsTheSameWay`:
  - a Fable prompt at a 93% Fable week is handed, and at 97% held;
  - a full week with the Fable week at 40% says "57% left ... cannot be used";
  - with the setting off, 93% is held as cc-P160.
- `P162_EndOfWeek_WakesWhenTheWindowOpensAndAfterEach5HourReset`:
  - held for pace at 15:00: no session at 15:50; one session and one email at 16:05;
  - a usage-limit rest with the 5-hour window resetting at 17:00: none at 16:30, one at 17:10, still one window email;
  - the same rest outside the window: no wake, no email.
- `P162_EndOfWeek_TheSettingOffRestoresP160`: 93% is held "ahead of pace (89.9% allowed now)" and the warning holds.
  No email, no wake, status not active.
- `P162_EndOfWeek_TheNightShiftRunsInsideTheWindow` (Tue 22:30):
  - a 92% week and a 60% session start the night shift inside the window;
  - with the setting off it is skipped for the 60% session, as before;
  - at 97% it is skipped at the cap.
- `P162_EndOfWeek_TheSummaryAfterTheResetSaysWhatWentUnused`: the window email at 15:00, then exactly one summary after
  16:00: "ended at about 88%: 12% went unused", "Fable week ... 40% ... 60% unused", "No Fable prompt was queued ...".

Seen failing first:
- All seven fail against the pre-change script (`golem.ps1` as P161 left it): 20 of their checks fail. In the outside
  and setting-off facts, what fails is the new status field and the absent wake and emails, as expected for "nothing
  else changes".
- Mutations (`scratchpad\mutate162.py`), each run against its own fact. All 10 were caught: the setting ignored; the
  window 48 h wide; no cap; the warning not ignored; no Fable window; no Fable note; no watch wake; usage-limit figures
  too old to wake; the night shift keeping its pace; no summary.

Golem full suite: **421 passed, 2 failed.** The failures are `P125_AUsageLimitEmailsOnceKeepsThePromptAndSaysWhenItResets`
("resets at 00:25 Sun") and `P131_AUsageLimitRestSaysWhenItIsReadyAndNotifiesWhenItIs` ("Ready at Sun 1:06 AM").
Both put a reset 1.5 to 2.2 h ahead of the real clock, and after about 21:47-22:30 that reset crosses midnight and gains a
day name. Both fail the same way on the pre-P161 and pre-P162 scripts (checked at 22:55). They are not caused by this
work and pass in the daytime.

Console (`D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1`): **380 facts, 375 passed, 5 failed.**
- The failures are `P83_TheLinksOpenTheTwoPagesAndNothingElse`, `P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo`,
  `P101_TheTileAndTheTabAreBuiltAndDrawn`, `P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing` and
  `P107_LinksAndSitesPointAtHavenAfterTheCutoverAndAtThisPcBefore`. They are the same five as before P161 (Haven vs
  this-PC links, and the live play-test count).
- The new P162 fact failed with the pre-change console ("expected 1 but got 0": no line) and passes now. The original
  file was swapped back in for one run, then restored.

## Deviations and decisions for Chase

- **Cap versus usageLimitPct:** inside the window the week runs to 97% even with `usageLimitPct` 95 (sprint stops the
  week at 95). The prompt says the week stops at `100 - endOfWeekReservePct`, and `usageLimitPct` applies to the 5-hour
  window.
- **Night shift session check:** inside the window it uses `usageLimitPct` (95), not `nightSessionMaxPct` (50), so a
  half-used 5-hour window does not skip it. I read "no even-pace skip" that way.
- **The window email goes out at the first watch inside the window**, so within 10 minutes of it opening, and only
  while the Golem is on (the watch does nothing while it is off). If the Golem is off then, there is no window email
  and no wake.
- **The summary uses the last figures read inside the window** (usage.json and plan-usage.json). After the reset the
  old window counts as 0, so the final percent is "about", not exact.
- **The Fable window:** in the plan file today the Fable week resets at the same time as the week. The code still keys
  the Fable window to its own reset time, as asked, but no test uses a different Fable reset time.
- **P156 batches:** not done, because P156 is still queued. The night shift has no batches to use.
- **P157 style:** the emails are in the Golem's current plain style; P157 has not run.
- **No task-list tool** was available in this session, so Chase could not follow steps through it. Progress went in
  short chat lines.

## For Chase

- **When it opens this week:** **Tue 10-20 at 4:00 PM**, 24 hours before the Wed 4:00 PM reset. From then until the
  reset the Golem:
  - keeps handing on prompts until the week is at 97%, whatever paceMode says;
  - ignores claude.ai's "you'll run out" warning;
  - runs the night shift without its pace check;
  - wakes itself when the window opens and after each 5-hour reset.
  You get an email when it opens and a summary of what went unused after the reset. The Golem tab shows
  `end week  : End of week: spending what is left until Wed 4:00 PM (...)`.
- **The settings** (`D:\UO\golem\settings.json`):
  - `endOfWeekSpend` (true): false turns it off and restores P160's pacing to the end of the week;
  - `endOfWeekHours` (24): raise it to start spending earlier, for example 36 for Tuesday 4:00 AM;
  - `endOfWeekReservePct` (3): raise it to keep more of the week's last hours for yourself, for example 10 to stop at
    90%; lower it to 0 to use everything.
- It never uses the free full reset or usage credits. Those stay your call, as in P160.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun` (23:0x):

```
Repo Result
---- ------
code dry run
docs dry run
```

Code: CHANGELOG.md, VERSION, scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1. Docs:
testing/SUMMARY.md, testing/play-tests.json (machine output), and this notes file. No file over 5 MB. All scratch is in
the session's scratchpad, outside both repos.

P162 DONE
