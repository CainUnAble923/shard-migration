# cc-P287: Golem hours by weekday, skip dates, and an idle check for a Golem in its owner's own account

## In plain words

- Stone (on your work PC) may now work all day on Saturday, Sunday and Monday, and keeps to its night hours
  (22:30-06:30) on the other days. Every other Golem is unchanged: night shift only, weekends included, unless marathon.
- Stone now backs off while you are using that PC: it works only while the screen is locked (or a screen saver is on),
  and stops at its next stopping point when you unlock it. Windows gives no "last keypress" time without a tool your
  work PC's security software would object to, so an unlocked screen counts as "in use" even if you walked away.
- When you work a Monday (or a weekend day), tell it so: the **Owner works (a date)** button on Stone's card in the web
  console, the same button on the Shard Console's Golem tab, or email `skip day stone 2026-10-26` (or `monday`). That
  day Stone keeps to its night hours. The cards now say "all day Sat, Sun, Mon" and any skipped dates.
- For you: let your work PC lock itself after a few minutes idle (or lock it when you leave), or Stone will wait all
  day. The console buttons arrive with the merge (restart the web console after it, as usual). One decision below:
  whether a real keyboard-idle reader is allowed on that PC.

## Status

The Iron Golem (Opus), 2026-10-23. Branch `golem/Iron/P287` of both repos; not committed (the Golem commits). The Golem
kit (`D:\UO\golem`, not a git repo) is **installed live** on the game PC, as P274 did: every changed file was checked
byte-identical to the copy I started from, backed up as `<file>.bak-20261023-P287`, then renamed into place; the Tinker
carries the kit and `golems.json` to the other PCs (Stone's included) within 10 minutes. No Docker, shard or Haven work.

| Part | Done | Where |
|---|---|---|
| 1. Weekday hours | `days { allDay, skip }` per Golem; an allDay weekday claims at any hour, a skip date falls back to `hours`; validated at every start; cards and the back-off verdict say it | `D:\UO\golem\Golems.ps1` (`Test-GolemDaysBlock`, `Test-GolemAllDayNow`, `Test-GolemSkipDate`, `Test-GolemHoursNow`, `Get-GolemCards`), `GolemPower.ps1` (the verdict's words) |
| 2. Same-account idle check | `backoff.selfIdle`, on by default when `windowsUser` is set and is not `golem`: pause and stop while the Golem's own session is in use. **No GetLastInputInfo** (see Decisions 1): lock screen, screen saver, a remote session's quser idle; an unlocked console counts as in use | `GolemPower.ps1` (`Get-GolemSelfActivity`, `Get-GolemPowerConfig`, `Test-GolemBackOff`) |
| 3. Skip a day from the consoles and email | **Owner works (a date)** on a Golem card (web console) for a Golem with all-day weekdays; **Owner works (Until box date)** on the Shard Console's Golem tab; email `skip day <Golem> <date>` (P149's commands are in main) | `Golems.ps1` `Add-GolemSkipDay`, new `Skip-Day.ps1`, `Away.ps1`; ShatteredLegacy `web-console\server.py`, `golem-actions.json`, `console-actions.json`, `static\app.js`, `scripts\Shard-Console.ps1`, `scripts\Invoke-WebConsoleAction.ps1` |
| 4. Stone's entry | `days.allDay` Sat, Sun, Mon (skip empty), `backoff.selfIdle` true; `hours` 22:30-06:30 and `noDaytimeMarathon` true kept | `D:\UO\golem\golems.json` |
| 5. Join-Golem fix | the Golem Watch and Remote Agent tasks run as the account `whoami` prints (DOMAIN\user) for any account but the local golem one; `<PC>\golem` as before | `Join-Golem.ps1` (`Get-JoinTaskUser`) |
| README, `_comment` | a section "All-day weekdays, skip dates and the same-account idle check (cc-P287)", the email command list, Files, Tests; the registry's `_comment` | `D:\UO\golem\README.md`, `golems.json` |

## How it behaves

**Days.** By the PC's calendar date. Stone on a skipped Monday: Sunday night's run may go on until 06:30 (its hours),
then nothing until 22:30. Marathon on: Stone still keeps to its hours on a normal or skipped day, because
`noDaytimeMarathon` is true. The back-off still holds on an all-day weekday. A bad block stops every hand-off with the
reason, like any registry error, for example `Stone: days.allDay: 'Funday' is not a weekday (Mon, Tue, Wed, Thu, Fri,
Sat, Sun)`. The Golem log line for a refused claim adds "today is a skip date, so not an all-day day".

**The idle check, and what it cannot see.** Stone runs in Chase's own login (`windowsUser` chase.fleming), so quser shows
only him and `ownerActive` (other users) never fires. `Get-GolemSelfActivity` reads the session the check runs in:

| The session | Read as |
|---|---|
| LogonUI.exe running in it (locked, or at the sign-in screen) | not in use: the Golem may work |
| a `.scr` process in it (screen saver) | not in use |
| a remote desktop session (quser `rdp-tcp#n`) | quser's idle minutes are the real last input there: in use under `idleMinutes` (10) |
| the PC's own screen, unlocked | **in use** (no input time is readable without a Windows API), unless quser itself shows an idle time of 10 minutes or more |
| no connected session of the account | not in use |

It cannot see: whether someone is at an unlocked screen (reading, a video, a game controller all count as in use: the
safe side); a remote session's input when quser's figure lags. **A PC left unlocked keeps Stone waiting.** On this PC at
01:00 the console was unlocked and quser said idle "none", which is exactly the gap: quser has no real idle time for the
console session. While in use it pauses claims and asks a running prompt for its stopping point (Stop), as `ownerActive`
does; the game PC's Golems have no `windowsUser`, so selfIdle is off for them and nothing changes there.

**Owner works.** One action, `Add-GolemSkipDay`: refused with the reason for a Golem with no all-day weekdays, a past date,
more than 60 days ahead, an unreadable date; a date that is not one of its all-day weekdays changes nothing and says so;
twice says "already". Past skip dates are dropped as the file is written; the result is validated with
`Read-GolemRegistry` (with the real folder's `mergeGolem` setting) before it replaces `golems.json`; the old file is kept
as `golems.json.bak-<time>-skipday`; a `SkipDay` line goes into `golem.log`.
- Web console: on the card of a Golem with all-day weekdays only (Stone today). A date box (the next free all-day date
  filled in); type `skip stone` to confirm (a typed word may hold no dashes, so the date is the box's). It is a new kind
  of button, `registry`: it changes `golems.json`, which lives on the game PC, so the server runs it **here** for any Golem,
  a remote one too, never through that PC's agent (otherwise Stone's own copy would be overwritten by the Tinker's next
  sync); the Golem's name comes from the card, never from the page; with no card it is refused.
- Shard Console: **Owner works (Until box date)** on the Golem tab's picker row; the picked Golem and the Until box's
  date (its time ignored); asks `skip <golem>`; `Skip-Day.ps1 -Golem <name> -Date <yyyy-MM-dd> -By console` in its own
  window, and the plan safety check allows that script with exactly those arguments.
- Email: `skip day <Golem> <date>` with `today`, `tomorrow`, a weekday or yyyy-MM-dd; on the command card.

## Tests

Red first, then green, every new test.

| Suite | Old code | New code |
|---|---|---|
| `D:\UO\golem\tests\GolemDays.Tests.ps1` (new, 8 facts: allDay noon claims, skip date does not, normal day keeps its hours; a bad days block stops validation with the reason; the verdict and cards; recent input backs off, old does not; selfIdle default on/off; lock screen, screen saver, remote, unlocked console; Owner works and Skip-Day.ps1; the email command) | 8 FAIL (13 checks passed, 19 failed) on the live kit before the install | 8 PASS, 53 checks, 0 failed (scratch kit, then the live kit after the install) |
| `tests\Join.Tests.ps1` `P287_Join_ADomainLoginsTasksRunAsWhoamiPrintsItTheGolemAccountAsBefore` (TEKCORP\chase.fleming; STEPHS-DESKTOP\golem) | FAIL: "only while chase.fleming is signed in" | PASS (scratch kit and live) |
| ShatteredLegacy `web-console\tests\test_remote_golems.py` `test_owner_works_runs_here_for_a_remote_golem_with_the_cards_name` | FAIL (the button did not exist) | PASS |
| ShatteredLegacy `scripts\tests\Shard-Console.Tests.ps1` `P287_OwnerWorksRunsSkipDayForTheGolemAndDateAndNothingElse` | FAIL | PASS |

The red runs on the consoles swapped the committed (HEAD) files in, ran, and copied mine back; md5 checked after each.

Regressions, each compared with the same suite on the old code:
- `GolemPower.Tests.ps1`: 133 passed, 0 failed (new and live).
- `Join.Tests.ps1` full: 4 failures, the same 4 on the untouched live kit (`P186_ARealRunDoes...`, `P186_TheReadinessCheck...`:
  this PC has no `D:\UO\overseer`, no Docker answer, an API key in the Machine environment). Not caused by this.
- `Golem.Tests.ps1` full on the new kit: **1,496 checks passed, 5 failed**, all in `P184_OverlappingTouchesNeverRunTogether...`
  and `P184_TouchesAreReadOrGuessed...`, which P274's notes record as already failing on the live script. The P149 and P157
  mail facts (the command card text changed) pass.
- Web console, all tests: 3 failures (`test_golem_glow` phone glow), the same 3 on the committed code. `test_actions.py`
  and `test_remote_golems.py`: 33 OK. I adapted `test_actions.py` (INPUTS, FLAGS, the word, and a registry button is
  refused without a card there).
- Shard Console, all facts: on the committed code 443 facts, 15 failed (missing `hues.mul` in a Golem work copy, Haven
  links, play-test tile counts, two timing facts). My first full run added 2 of mine (the tooltip was 4 sentences; the
  window button had no web twin in `console-actions.json`), both fixed; the final full run is below.

Shard Console, final full run on the finished code: **444 facts, 431 passed, 13 failed**, every one of the 13 also failing
on the committed code (above); the two timing facts that failed there (`P84_TheUOLookAddsUnderASecondToTheStart`,
`P154_TheRefreshNeverRunsOnTheWindowsThread`) passed this time. `P84_EveryTileState...` fails only when run alone
(it needs an earlier fact's setup) and passes in the full run, on both codes.

## Decisions for Chase

1. **No GetLastInputInfo.** The prompt asked for it; every kit script says "No Add-Type, no inline C#, no P/Invoke" (the
   SentinelOne rule in `GolemPaths.ps1`, `SENTINELONE-EXCLUSIONS.md`), and Stone's PC is a managed work PC, the place a
   compiled type in a script is most likely to be flagged. So the check reads the lock screen and screen saver instead,
   and an unlocked console counts as in use. If you want a true idle reader there (a small signed helper, or one Add-Type
   exception for that PC), say so; it is one detector in `Get-GolemSelfActivity` behind the same verdict.
2. **The work PC must lock when idle** for Stone to use the weekends: check its screen lock timeout (Settings, Accounts,
   Sign-in options, or your company's policy).
3. **Laptop power plans** (`Set-GolemPower.ps1`) still follow `hours` only; Stone is a desktop with no power block, so
   nothing changes for it. An all-day weekday on a laptop would need its power plan to follow `days` too: not done.

## Notes on the way

- `Add-GolemEntry.ps1` validates its temp file in `%TEMP%`, where `Read-GolemRegistry` finds no `settings.json` and so
  reads mergeGolem as off; with Shadow Iron as the merge Golem that would refuse a valid registry. `Add-GolemSkipDay`
  passes the real folder's setting. Add-GolemEntry is untouched; worth a one-line fix-up.
- The typed confirm on the web console allows letters, digits and spaces only, which is why the word is `skip <golem>`.

## Files

`D:\UO\golem` (live, backups `*.bak-20261023-P287`): `Golems.ps1`, `GolemPower.ps1`, `Away.ps1`, `Join-Golem.ps1`,
`golems.json`, `README.md`, `tests\Join.Tests.ps1`; new `Skip-Day.ps1`, `tests\GolemDays.Tests.ps1`.

`ShatteredLegacy`: `web-console\server.py`, `web-console\golem-actions.json`, `web-console\console-actions.json`,
`web-console\static\app.js`, `web-console\tests\test_actions.py`, `web-console\tests\test_remote_golems.py`,
`scripts\Shard-Console.ps1`, `scripts\Invoke-WebConsoleAction.ps1`, `scripts\tests\Shard-Console.Tests.ps1`.

`shard-migration`: this note.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P287`. Code: 9 files
pending (the consoles and their tests, listed under Files). Docs: 1 (this note). Neither is BLOCKED. The kit's files in
`D:\UO\golem` are outside both repos and installed already (Status).

```
Repo Result
---- ------
code dry run
docs dry run
```

P287 DONE
