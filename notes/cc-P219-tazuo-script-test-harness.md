# cc-P219: a home Golem can run a Legion script in TazUO on the test shard and report on it

2026-10-21. The Iron Golem (Opus), on the game PC (CHASES-TOWER). Prompt:
`D:\UO\cc-prompts\claimed\Iron\cc-P219-tazuo-script-test-harness.md`. Work copies `D:\UO\golems\Iron\ShatteredLegacy`
and `D:\UO\golems\Iron\shard-migration`, branch `golem/Iron/P219`, both clean at the start. P215 is in main (merge
`b5028f7` in the code repo, `00787fb` in the docs repo), so the prompt's gate passed. Not committed: the Golem commits
after the DONE line.

## In plain words

- A Golem can now test a Legion script for real: one command opens TazUO on this PC's test shard, logs in that Golem's
  own Player character, runs the script, and writes a pass or fail report with screenshots.
- The first real test passed: SL_Mining made Iron's character a miner at the Minoc mine, it dug five times and got iron
  and dull copper ore, in about a minute. The report is in `testing\legion\SL_Mining-20261021-1135-Iron.md`.
- The harness only ever connects to the test shard on the same PC; the live shard's port is refused from anywhere.
- Each Golem's card on the web console will say whether its PC can run these tests, once this branch is merged and you
  restart the web console. Nothing else for you to do.

## Headlines

- **`D:\UO\golem\Test-LegionScript.ps1`** (with `LegionTest.ps1` and `LegionTestRunner.py`): `-Script SL_Mining.py
  -Plan <plan>` [`-Golem`, `-Branch`, `-TargetHost`, `-Port`]. In order: the never-live guard, the plan, the
  `test-shard` lock, this PC's check, the test shard up (started if stopped), the Admin's setup, a client of its own
  that logs in the Golem's Player and starts the runner, screenshots, the client closed, the password cleared, the lock
  released (on every way out), the report. It is in `D:\UO\golem` because it uses the Golem's lock, accounts and kit;
  the plans and the Admin's setup are in the code repo (`tools\legion-test\plans\`, `tools\playtest-bot\uobot\legionsetup.py`).
- **The real run on the tower passed** (twice; the second, on the installed harness, is the report kept): `SL_Mining`,
  the plan in `tools\legion-test\plans\SL_Mining.json`. Every step passed: stands at the Minoc mine spot (2553, 479),
  mines five times (5 digs: dull copper, iron), ore in the backpack. 69 s from the lock to the release.
- **The Admin's setup works through `[global ... where playermobile Name == "<Golem> the Tester"`**, proved on the
  test shard: Mining 100 and Str 100, a pickaxe in the pack, and the logout spot (`LogoutMap Trammel LogoutLocation
  "(2553, 479, 8)"`), so the logged-out character comes in at the mine. Only the Golem's own Admin, only on the test
  shard (the bot's `check_test_target`).
- **The runner** is a Legion script of the harness's own: TazUO starts it by itself in the world (`lscript.json`
  `GlobalAutoStartScripts` in the test client's own `Data`), it starts the script under test (`API.PlayScript`), copies
  the journal, judges the plan's steps (`journal`, `items`, `at`), and stops on the time limit, `failOn`, a failed
  step or every step passed.
- **The never-live guard** (`Test-LegionTarget`): this PC's own name or address and ports 2594 to 2599 only; 2593 is
  refused from any host, and the live shard's and Haven's names always. The client's settings ignore relay redirects.
- **Where it can run:** the readiness check (`Test-GolemReady.ps1`) now says so (an INFO line and `legionTests` in
  `ready-<name>.json`), and the web console's card shows "Legion script tests: can run here" or why not. It never
  changes the READY verdict. Iron's real check: "this PC can run Legion script tests".
- **A test prompt is told** in its hand-off (a prompt whose Touches name `tazuo-scripts`) to run the harness and link
  the report in its notes.
- **Tests:** `tests\LegionScript.Tests.ps1` (10 facts, 51 checks: the guard and the lock among them), a Golem fact, a
  Join fact, two web console tests and five bot tests, each seen failing first.

## What changed

**`D:\UO\golem`** (not a repo; each edited file backed up as `<name>.bak-20261021-p219`):

| File | Change |
|---|---|
| `Test-LegionScript.ps1` (new) | the harness (above) |
| `LegionTest.ps1` (new) | `Test-LegionTarget` (the guard), `Get-LegionOwnHosts`, `Get-LegionCapability` (what the PC needs), `ConvertTo-CuoPassword` (TazUO's own obfuscation of the saved password: ClassicUO.Utility.Crypter, keyed on the PC's name), `Read-LegionPlan`, `Set-LegionOverrides`, `New-LegionSettings`, `Get-LegionLines`, `Save-LegionShot` (PrintWindow, JPEG), `Format-LegionReport` |
| `LegionTestRunner.py` (new) | the Legion side (above) |
| `golem.ps1` | `Get-LegionHandOffText`: a `tazuo-scripts` prompt's hand-off names the harness and asks for the report in the notes |
| `Test-GolemReady.ps1` | the `legionTests` probe, its INFO line, `legionTests` in the readiness file (not a check, so not in the verdict) |
| `README.md` | section "Legion script tests (cc-P219)", the Files row |
| `tests\LegionScript.Tests.ps1` (new), `tests\Golem.Tests.ps1`, `tests\Join.Tests.ps1` | the facts (Tests) |
| `legion-test\<Golem>\` (new, per PC, not in the kit) | each Golem's own test client (a copy of `D:\UO\tazuo-sl-build\client`, 247 MB, kept between runs and mirrored each time) and its run folders (plan, journal, results, runner log, the Admin's transcript) |

**`D:\UO\golems\Iron\ShatteredLegacy`**:

| File | Change |
|---|---|
| `tools\legion-test\plans\SL_Mining.json` (new) | the SL_Mining plan |
| `tools\playtest-bot\uobot\legionsetup.py` (new) | the Admin's setup: logs in `<golem>-admin`, types each command with `{player}` filled in, keeps the answers, logs out; test shards only |
| `tools\playtest-bot\tests\test_legionsetup.py` (new) | five tests |
| `web-console\panels.py` | `ready_summary` passes `legionTests` through when the file has it |
| `web-console\static\app.js` | the card's "Legion script tests" line |
| `web-console\tests\test_remote_golems.py` | the summary and the phone card with the new line |

**`D:\UO\golems\Iron\shard-migration`**: `testing\legion\SL_Mining-20261021-1135-Iron.md` and its two screenshots
(156 KB and 168 KB).

## What was learned on the way (TazUO)

- A Legion script whose name starts with `_` is never loaded (`LegionScripting.cs` `HandleScriptsInDirectory`), so the
  runner is `LegionTestRunner.py`.
- `autologin` alone does not log in on the first start: `LoginScene.Load` only connects when the login step is past
  Main or with `-skiploginscreen` (`LoginScene.cs:127`). The harness passes `-skiploginscreen -skipserverselect
  -lastcharactername "<Golem> the Tester"`.
- Global autostart scripts are matched by file name (`AutoPlayGlobal`), read from `Data\lscript.json` beside the exe.
- In a PowerShell script, `$plan` and the `-Plan` parameter are the same variable, and `@()` around a
  `List[object]` throws "Argument types do not match" in Windows PowerShell 5.1: both hit and fixed.

## Where it can run (part 4)

| PC | Golems | Can run it | How known |
|---|---|---|---|
| CHASES-TOWER (game PC) | Iron, Bronze | yes | the real run; Iron's readiness check: "this PC can run Legion script tests" |
| STEPHS-DESKTOP | Gold (Valorite, Verite: Codex, off) | not known from here | its own readiness check says, on its card, once the kit and this branch reach it |
| AINSLEYS-LAPTOP, ELLIES-LAPTOP | Copper, Silver | not known from here | the same |
| TEK-DIRECTOR | Stone | not known from here | the same |

`golems.json` was **not** changed (Deviation 1): `tazuo-scripts` is already an area of Iron (`*`), Bronze, Gold,
Copper, Silver, Stone, Valorite and Verite.

## The real run (Done means)

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Test-LegionScript.ps1 -Golem Iron -Script SL_Mining.py
-Plan D:\UO\golems\Iron\ShatteredLegacy\tools\legion-test\plans\SL_Mining.json -CodeRepo D:\UO\golems\Iron\ShatteredLegacy
-DocsRepo D:\UO\golems\Iron\shard-migration`, exit 0, report
`testing\legion\SL_Mining-20261021-1135-Iron.md` (PASS). The plan: make a miner (Mining 100, Str 100, a pickaxe), stand
at a mine spot (the Minoc mine, where `SL_Mining.log` showed a dig at every swing on 10-18; its tile and height read from
the map files: land 0x0005 at z 8, rock 0x022C beside it), mine five times, see ore. The overrides turn off the control
window, wandering, forge trips and looping (the script's own CONFIG lines), so it starts at once and stays put.

The report also shows two things for SL_Mining's owner (not part of this prompt): TazUO warns "Script 'SL_Mining.py'
contains an unbounded 'while' loop. Change it to while API.StopRequested", and with the control window off the script
still tries to open something that says "Not here. Open it in a guarded town, or in a house where you are an owner,
co-owner or friend." It mined regardless.

Five earlier tries on the way: the plan variable bug and the list bug (no report), the login screen and the `_` name
(two FAIL reports, deleted), and the first pass on the working copy (report deleted: the final run on the installed
harness is the one kept). The test character now has five pickaxes (my setup probe and each setup since) and new veins
in its logbook; it is the test shard's.

## Tests

Windows PowerShell 5.1. Each new test was seen failing first:

| Test | Before | After |
|---|---|---|
| `tests\LegionScript.Tests.ps1`: 10 facts (the guard allows only this PC's test ports; refuses 2593 from any host, the live and Haven names, another machine, other ports, no host; the harness refuses those before any lock; takes and releases the lock; a lock held by another Golem means exit 3 and no run, its lock untouched; the lock is released when a run stops partway; a bad plan is refused before the lock; the client's settings ignore relays and keep no plain password; overrides; the report) | against the Golem folder before P219 (no harness): 7 checks passed, 19 failed, all 10 facts red. Mutations: no port check (1 fact red), any host allowed (2 red), no lock (1 red), the release replaced by a second take (2 red) | 51 checks passed, 0 failed (installed) |
| `tests\Golem.Tests.ps1` `P219_ATazuoScriptsPromptIsToldToTestItsLegionScriptAndAttachTheReport` | FAIL on the pre-P219 golem.ps1 | PASS; with it, the D9, Golem_ and P157 facts pass on the installed hook (23, 39, 425 checks) |
| `tests\Join.Tests.ps1` `P219_TheReadinessSaysWhetherThisPCCanRunLegionScriptTestsWithoutChangingTheVerdict` | FAIL on the old Test-GolemReady.ps1 | PASS |
| `web-console\tests\test_remote_golems.py`: the summary (`test_the_readiness_summary_is_compact`) and the phone card (`test_every_golems_card_and_its_buttons_on_a_phone`) | both FAIL on HEAD's panels.py and app.js | PASS (13 tests OK) |
| `tools\playtest-bot\tests\test_legionsetup.py` (5 tests) | ERROR without `legionsetup.py` | OK |

Full suites:
- `LegionScript.Tests.ps1` 51/0. `Join.Tests.ps1` 102 passed, 4 failed, in two facts
  (`P186_ARealRunDoesEachStepOnceAndARerunSkipsThem`, `P186_TheReadinessCheckReportsEachFailureByNameAndWritesTheFile`)
  that fail the same way with the pre-P219 files (98 passed, 4 failed).
- Web console (`python -m unittest discover -s web-console/tests`): 83 tests, 3 failures, all
  `test_golem_glow.PhoneGlow.test_five_states_on_a_phone` (glow-pulse/glow-soft instead of none), the same with HEAD's
  panels.py and app.js.
- Play-test bot: 55 tests, 1 failure, `test_installer_dry_run_prints_the_call_and_registers_nothing`, as on HEAD (the
  real nightly task is registered on this PC; P157's notes).
- `Golem.Tests.ps1` was not run in full (a full run was stopped for low memory in P157); the facts that read the
  hand-off (D9*, Golem_*, P157_*, P219_*) were, on the installed hook.

Commit preflight (`Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration`):

```
Repo Result
---- ------
code dry run
docs dry run
```

## Deviations and decisions for Chase

1. **`golems.json` was not changed.** The prompt says to add `tazuo-scripts` to a Golem's areas only where its PC can
   run the harness. It is already in the areas of Bronze, Gold, Copper, Silver, Stone, Valorite and Verite (and Iron's
   `*`), since before this prompt, where it routes every TazUO-script prompt (editing scripts too, not only testing
   them). Taking it from PCs that may lack the client data would change what they can claim, which is your call. Each
   PC's card now says whether it can run the tests, from its own readiness check. If you want it narrowed, say which.
2. **The Read tool was denied** (unattended run) on `docker\uo\Start-TestShard.ps1`, and then the Grep tool on
   `scripts\Shard-Console.ps1` when I looked for how it is called. I did not retry either. The harness uses the shard
   when it is up (it was), starts the existing container with `docker start` when it is stopped, and runs
   `Start-TestShard.ps1` with no arguments only when there is no container at all; **that last branch was not run**.
   What I wanted to run: Read of `Start-TestShard.ps1` lines 1 to 90 (its parameters), and Grep of `Start-TestShard`
   in `Shard-Console.ps1`.
3. **The installed web console** shows the new card line only after this branch is merged and you restart it (as
   P187's For Chase says); I did not restart it.
4. **The character's pack grows** by a pickaxe a run (the plan adds one); harmless on the test shard. A plan can add
   a `[global ... delete ...]` line if it matters.
5. **The window:** TazUO opens a 1280 x 800 window on the PC's desktop for about a minute; the screenshots are of it
   (PrintWindow, so another window on top does not spoil them).

## For Chase

- Try it: `powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Test-LegionScript.ps1 -Golem Iron -Script
  SL_Mining.py -Plan D:\ShatteredLegacy\tools\legion-test\plans\SL_Mining.json` (after the merge). A new script needs a
  plan next to `SL_Mining.json`; the README section "Legion script tests" says what goes in one.
- Decide Deviation 1 if you want `tazuo-scripts` only on PCs that can test.

P219 DONE
