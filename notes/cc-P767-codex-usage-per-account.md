# cc-P767: Codex usage tracking per account (each lane paces on its own account)

Iron Golem, 2026-11-01. Kit changes are installed live in `D:\UO\golem` (the kit is not a git repo). Each changed file
is backed up as `<file>.bak-20261101-P767`. The full diff and the test logs are in `notes\cc-P767-tools\`. Docs copy
`D:\UO\golems\Iron\shard-migration` on `golem/Iron/P767`, not committed. No sign-in, no `.env`, no `D:\UO\third-party`.
The hard stop and reserve settings are unchanged.

## In plain words

- **Steph's lane now reads Steph's own numbers.** Checking her lane's Codex usage used to show your account's numbers
  (the same session log). It now shows her own last reading: week 30%, from 10-27. That reading is marked "unknown"
  with its age, 5.4 days, because her account has had no Codex use since then. Your lane shows your own fresh numbers:
  5-hour 29%, week 53%.
- **Why the two usage files stopped on 10-27: the lanes have not run since.** Every watch since 10-27 found nothing
  they were allowed to take: every queued prompt names another Golem, or touches an area the lanes may not use. The
  files are written after each lane run, as before. Your lane's file now also refreshes whenever there is a newer
  reading of your account (it did at 22:49 tonight).
- **One line per lane shows both side by side.** `Codex.ps1 -Action lanes` (and the Sweep, and the `lanes` part of
  `-Action status`) gives each lane's 5-hour and week percent with reset times, whether the reading is fresh, runs
  today, and idle time today with the reasons.
- **The lane logs now say why a lane sits idle**, once per watch. For example: "Valorite idle: 7 prompts, 0 claimable:
  6 Golem line, 1 area golem". That is tonight's real line: the lanes are starved because the queue's prompts are all
  named for other Golems. To give the lanes work, queue prompts marked Codex OK with no Golem line (or "any"); nothing
  else is needed.

## 1. Per-account limits

**What was wrong.**
- `Codex.ps1 -Action status -CodexHome ...\codex-home\lane-steph` had no `-Account`, so it took the usage file
  `codex-usage.json`. That file is this PC's own, written by the CC Golems' pre-commit reviews on Chase's `~\.codex`.
- `Read-AccountRateLimits` takes the newest of all its readings, so Chase's 22:07 session log won.
- The lanes' own watches always passed `-Account`, so their budget checks were already per account. Only a status call
  given the home alone mixed the two up.
- The prompt's guess (`codexAccountHomes` listing only lane-chase) was not the cause, but lane-steph's entry is added
  as asked.

**The fix** (`Codex.ps1`):
- **The account comes from the home.** `Resolve-CodexAccount`: a home under `D:\UO\golem\codex-home\<login>` names its
  login when `-Account` is not given.
- **The home comes from the account.** `Resolve-CodexHomeFor`: `-Account lane-steph` given alone uses lane-steph's own
  home, never Chase's `~\.codex`.
- So a lane reads only its own home, the homes `codexAccountHomes` lists for its login, and its own
  `codex-usage-<login>.json`. It never reads another account's log or file.
- **Fresh or unknown.** `Get-LimitsFreshness`: a reading taken within `codexLimitsFreshMinutes` (a new setting, default
  300, the 5-hour window; not added to `settings.json`) is "fresh". An older one is "unknown", and the last good
  reading is kept and used, with its age.
- `status` now carries `account`, `codexHome`, `limitsState`, `limitsAgeMinutes` and `limitsNote`.
- **Settings.** `settings.json` `codexAccountHomes` now has `"lane-steph": ["D:\\UO\\golem\\codex-home\\lane-steph"]`.
  No other home on this PC is signed in to Steph's account; her own PC's `~\.codex` is on stephs-desktop.

**The real status calls** (read-only: no Codex run; they run `codex --version` and `codex login status`), 22:49:

| Lane | Source | Taken | 5-hour | Week | State |
|---|---|---|---|---|---|
| lane-chase | `rollout-2026-11-01T22-07-59-...` in `C:\Users\ckfle\.codex` | 11-01 22:08 | 29% | 53% | fresh, 41 min |
| lane-steph | `rollout-2026-10-27T14-27-09-...` (its own home) | 10-27 14:28 | 11% | 30% | unknown, 5.4 days |

Before the fix, the same lane-steph call showed lane-chase's `rollout-2026-11-01T22-07-59-...` and 29% / 53%.

## 2. The usage files

**Cause.** No lane has run since 10-27 14:17 (P709). `codex-runs\` has no lane run after `P709-lane-1.json` (10-27
14:26), and the logs have no "lane: Codex starts" after 14:17. The usage files are written at the end of each run
(`Update-CodexUsage` in `Invoke-CodexRun`), so they stopped there: 14:27 and 14:28. The writing itself was fine.
- What did run after 10-27 were the CC Golems' pre-commit reviews (`review-P7xx-*`). Those run on Chase's own
  `~\.codex` without an account, so they write `codex-usage.json`, which was updated at 22:08 tonight.
- Why the lanes did not run: every watch skipped every queued prompt. Tonight, 6 of 7 have a Golem line for another
  Golem, and P715 touches `golem`, which the lanes may not.

**What changed.**
- Lane runs write their own file as before (runs, tokens, before/after limits; nothing changed there).
- The lane's status call at each watch also rewrites the lane's file when its account has a newer reading than the
  file holds. So the file keeps the last good reading while the lane is idle, and only then.
- lane-chase's file updated at 22:49 (Chase's own Codex use moved the windows).
- lane-steph's has no newer reading to take. It updates on Steph's lane's next run, or the next time her account has a
  newer session log here.

## 3. Status and Sweep

- `Codex.ps1 -Action lanes` prints one line per Codex lane. `-Action status` carries the same as `lanes` (an object
  per lane), whichever lane it is asked about.
- `join\Sweep.ps1` prints them under "Codex lanes:". Tonight's lines:

```
Valorite (lane-chase): 5-hour 29% (resets Sun 23:39), week 53% (resets Wed 01:00); fresh: 49 min old (session log
  rollout-2026-11-01T22-07-59-... in C:\Users\ckfle\.codex); runs today 0; idle today 0 min: nothing claimable 0 min
Verite (lane-steph): 5-hour 0% (a new window: it reset after the reading), week 30% (resets Mon 05:49); unknown: no
  session log of this account in the last 5h 00m; the last good reading is 5.4 days old (session log
  rollout-2026-10-27T14-27-09-...); runs today 0; idle today 0 min: nothing claimable 0 min
```

- **Idle today** adds up the lane's idle lines from today in its own log (section 4):
  - each line counts until the next one, at most one watch (10 minutes); the last counts until now;
  - reasons are nothing claimable, budget, error, hours, backs off, queue empty, held, needs you, off;
  - the lines start with tonight's install (22:57), so tonight's totals are small; tomorrow's show the whole day.
- **A window whose reset has passed** shows 0% "a new window", as the budget already counts it.
- **Not run in full:** `Sweep.ps1` also copies the kit manifest to the other PCs over ssh and checks their drift, so I
  did not run it here. Its new line is the same `Codex.ps1 -Action lanes` call shown above.

## 4. The idle summary line

- **The skip tally.** `Golems.ps1`: `Get-ClaimCandidate` counts each skipped prompt by reason (`Add-ClaimSkip`): model,
  Golem line, run next pick, not Codex OK, no Lane tests, not for a lane, left for the Codex lane, no Touches,
  "area <areas>" (not allowed, busy or exclusive), outside its hours. The per-prompt log lines are unchanged.
- **One line per watch.** `golem.ps1`: the lane's watch logs `<Golem> idle: <reason>` once per watch when it runs
  nothing (`Write-LaneIdle`).
  - With prompts but none claimable, it logs the summary (`Get-ClaimSkipSummary`), counting prompts held behind a
    parked one too.
  - Otherwise it logs budget, error (no Codex.ps1, no sign-in, a status call with no answer), hours, backs off, queue
    empty, held, needs you or off.
- In the logs since the install:

```
golem-Valorite.log: 2026-11-01 22:57:10  Watch        Valorite idle: 7 prompts, 0 claimable: 6 Golem line, 1 area golem
golem-Verite.log:   2026-11-01 22:57:21  Watch        Verite idle: 7 prompts, 0 claimable: 6 Golem line, 1 area golem
```

## Tests

Following the kit's way (memory: scratch copies, red on the live kit, md5 check, back up, install by rename). New facts:

| Fact | Suite | On the live kit | On the changed copy |
|---|---|---|---|
| P767_ALaneHomeNamesItsAccountAndAnAccountAloneFindsItsHome | Codex | red | green |
| P767_LaneStephsStatusReadsOnlyItsOwnAccountAndSaysUnknownWithTheLastGoodReadingsAge | Codex | red | green |
| P767_TheLanesViewAddsUpTodaysIdleTimeByReason | Codex | red | green |
| P767_AFreshReadingIsWithinFiveHoursAndOlderIsUnknown | Codex | red | green |
| P767_ALaneThatSkipsEveryPromptSaysWhyInOneSummary | Lane | red | green |

What the status fact proves:
- lane-steph's status reads its own 5-day-old log, not the PC file's newer Chase reading;
- it says unknown with the age;
- it writes its own usage file and leaves `codex-usage.json` alone;
- lane-chase reads its own, fresh;
- the lanes part shows both.

Suites on the changed copy (logs in `notes\cc-P767-tools\`):
- `Codex.Tests.ps1`: 183 checks, 0 failed (`codex-green.txt`; red run `codex-red.txt`: the 4 new facts failed).
- `Lane.Tests.ps1`: 69 checks, 0 failed (`lane-green.txt`; red `lane-red.txt`).
- `Golem.Tests.ps1`: 1,684 passed, 6 failed (`golem-suite-changed.txt`).
  - The 6 are P131 (1: the "Ready at" countdown crosses midnight at this hour) and P184 (5: the overlap rule and the
    guessed-area log).
  - All 6 fail the same way on the live kit before the change (run with `-Only` against `D:\UO\golem\golem.ps1`). They
    are not caused by this change, and are worth a separate look: P184's "Iron takes P104, not the server prompts" is
    the overlap rule.

**Installed** after checking that the four live scripts' md5 still matched the copies the work started from:
- `Codex.ps1`, `golem.ps1`, `Golems.ps1`, `join\Sweep.ps1`, `tests\Codex.Tests.ps1`, `tests\Lane.Tests.ps1`, and
  `settings.json` (one entry added, with a text insert that keeps its layout, and a JSON check);
- each is backed up as `.bak-20261101-P767`;
- all are ASCII only;
- the next watches (22:57) ran on the new files with no errors.

## Deviations and decisions for Chase

- **The prompt's two causes were not the real ones.**
  - The shared session log came from the missing account on the status call, not from `codexAccountHomes`.
  - The usage files stopped because the lanes have had nothing to run since 10-27; they never failed to write.
  - Both are fixed or made visible anyway, as the prompt asked.
- **The lanes are starved by the queue.** All 7 queued prompts are named for other Golems or touch `golem`. To use
  more Codex, the overseer needs to queue prompts marked `**Agent:** Codex OK` with a Lane tests line, no Golem line
  (or `any`) and areas the lanes may use (docs-only, map, tazuo-scripts, server, server-patches).
- **The other PCs' copies of the kit:** the kit is copied to Gold, Copper and Silver by the usual kit sync. Until then
  the Sweep's drift check lists these 7 files as changed there.
- **A test-command slip, recorded:** my first post-install status calls from Git Bash passed `codex-home\$h` literally
  (`\\$h` in a double-quoted string), a folder that does not exist, and so looked unfixed. Called with a real path
  (PowerShell, or forward slashes from Bash), both lanes read their own accounts as shown.

## Files

- **D:\UO\golem** (live kit, backups `.bak-20261101-P767`): `Codex.ps1`, `golem.ps1`, `Golems.ps1`, `join\Sweep.ps1`,
  `tests\Codex.Tests.ps1`, `tests\Lane.Tests.ps1`, `settings.json`.
- **shard-migration:** this file and `notes\cc-P767-tools\`:
  - `p767-kit.diff`, the full change;
  - the edit scripts and fact sources;
  - the red and green test logs.

P767 DONE
