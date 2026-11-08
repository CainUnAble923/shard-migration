# cc-P819: pause bot play testing while Chase plays other games

## In plain words

- **The night bots wait for your game to close.** On the game PC, the overnight play tests and the Play Test Goblin
  look first. If another game is running, they wait, checking every 10 minutes, and go on when it closes. If you are
  still playing at 06:30, they skip that night and write one line in their logs. If a game starts mid-run, the bot
  finishes the check it is on, closes its clients and waits the same way.
- **Golems never open a game client on the game PC while you play.** Proof shots, two-client tests and bot runs refuse
  with "waiting: Chase is playing <game>" and wait for it to close. Builds, tests and code go on, and other PCs are
  unaffected.
- **Our own UO clients never count.** TazUO, ClassicUO and the Enhanced Client are left out, and so is Wallpaper
  Engine, which runs all day from the Steam folder and would otherwise look like a game.
- **For you:** the web console's Golem page gets a **Game pause** line (on, and whether a game is running, plus anyone
  waiting) and a **Game pause on / off** button (type "game pause off" or "game pause on"). They show up once this
  branch merges and the web console and Shard Console restart. Pause is on by default.

Iron Golem, 2026-11-08. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P819`. Nothing committed.

## 1. One shared check (Golem kit)

New in the kit, `D:\UO\golem`:

- **`GamePause.ps1`** (a library, dot-sourced):
  - **`Test-GolemGameRunning`**: GolemPower's own detection (`Get-GolemOwnerActivity`: known game names, the
    registry's `backoff.games`, or a process under `steamapps\common`, Epic Games, EA Games, Riot Games or Battle.net
    folders; launchers left out), run on the process list with our own clients removed first. Left out: TazUO,
    ClassicUO, UOSA, anything under an Ultima Online, tazuo or ClassicUO folder or our UO folders; Wallpaper Engine and
    SteamVR helpers.
  - **`Get-GamePauseConfig`**: reads `settings.json` `gamePause` (default on) and `gamePausePc` (default
    `CHASES-TOWER`). On any other PC the pause never applies.
  - **`Get-GamePauseState`**: what a bot should do now, as one line ("waiting: Chase is playing eldenring", "no game
    running", "game pause off", "not the game PC").
  - **`Wait-GolemNoGame`**: waits, checking every interval, up to an optional end time. While it waits it keeps
    `game-wait-<who>.json` in the kit root, which is the consoles' status line, and removes it after.
- **`Test-GameRunning.ps1`** (the one call every bot uses):
  - Without `-Wait`: one line and an exit code. 0 means go on; 1 means a game is running.
  - With `-Wait [-Until HH:mm] [-IntervalSeconds n] [-Who x] [-What y]`: 0 when the game closes, 1 when the end time
    is reached first.
- **`Set-GamePause.ps1 -On|-Off`**: the switch, `settings.json` `gamePause`. Every other key is kept.
- **`LegionTest.ps1`**: `Test-LegionTarget`, the never-live guard that every TazUO shot and two-client driver calls
  before it opens a client (61 tool scripts call it), now also refuses while a game runs on the game PC. It names the
  game and how to wait. A new `-GameState` parameter is for facts.
- **Install:** following the kit's own way (the kit is not a git repo; memory rule P274/P287). Scratch copies, the suites
  run red on the live kit and green on the scratch copy, live files backed up as `*.bak-20261107-P819`
  (`LegionTest.ps1`, `tests\LegionScript.Tests.ps1`), installed by rename, md5 matched. The Tinker's next kit snapshot
  (`Kit.ps1 Get-KitFiles`: every top-level kit file) carries the new and changed files to the other PCs.
- **Copies in this repo:** `notes/cc-P819-tools/kit/` (and `LegionTest.ps1.diff`), for review.
- **A real finding while testing:** Wallpaper Engine's `wallpaperui` runs all day from
  `D:\SteamLibrary\steamapps\common\wallpaper_engine\bin\` and counted as a game. GolemPower's launcher list has only
  `wallpaper32`/`wallpaper64`. GamePause leaves the whole `wallpaper_engine` folder out. GolemPower itself was not
  changed (its back-off is off on the game PC anyway).

## 2. The night bots wait

- **`tools/playtest-bot/Run-OvernightPlaytests.ps1`**: new parameters `-GameCheck` (default the kit's
  `Test-GameRunning.ps1`), `-NightEnd 06:30`, `-GameIntervalSeconds 600` and `-NoGameWait`.
  - On a night with work, before anything is built or started, it runs the check with `-Wait -Until 06:30`. Each line
    goes into `overnight.log` as it happens ("game pause: waiting: Chase is playing ...", "the game closed: ... goes on").
  - Still playing at 06:30, it writes "skipped on <commit>: a game was running until 06:30; nothing built, no email" and
    exits 0.
  - A night with no work never looks.
  - A missing kit check (another PC, an older kit) means no pause.
- **Mid-run, in `uobot/run.py`** (new `--game-check`, `--game-until`, `--game-interval`; the runner passes them):
  - Before each check it looks again. On a game it closes the bot's long-lived clients cleanly (`Ctx.close_clients`;
    they reopen on the next use), waits the same way, then resumes.
  - Still playing at the night's end, the checks not yet run are **SKIPPED**.
  - **The soak** (`uobot/soak.py`) asks every minute. A game ends it early: each actor finishes its step and the clients
    close. Then it waits and runs the minutes left. The parts are merged into one record (`merge_soak`), so the report
    reads as before.
  - `results.json` has `gameWaits`. The report and the email list each wait and the skipped count.
- **`scripts/Run-PlayTestGoblin.ps1`**: the same parameters and wait at its start. Still playing at 06:30, it logs
  "Skipped this run: a game was running until 06:30." in `D:\UO\logs\playtest-goblin.log` and exits 0.
  - The Goblin itself drives no client, but it is on the prompt's list, so it waits too.

## 3. Golem playthroughs wait, other work goes on

- **TazUO shots and two-client tests:** every client-opening driver (P720's to P823's `shots*.ps1`, `isle-shots`,
  `Test-LegionScript.ps1`) calls `Test-LegionTarget` first. On the game PC with a game running it refuses: "waiting:
  Chase is playing <game>: no game client opens on the game PC while he plays. Wait with
  D:\UO\golem\Test-GameRunning.ps1 -Wait (in the background; it ends when the game closes), then run this again".
  - Waiting in the guard itself would not work: a Claude Code command is cut off at 10 minutes. So the Golem runs the
    wait in the background and is told when it ends.
- **The playtest bot run by a Golem** (`python -m uobot.run` without `--game-until`): it looks once at the start and,
  while a game runs, exits 4 with the same line.
- **The status line:** a wait with `-Who <Golem>` writes `game-wait-<Golem>.json`, which the web console shows on the
  Golem page ("Iron: waiting: Chase is playing ...").
- **Unaffected:** builds, tests and code (nothing else calls the check), and other PCs (`gamePausePc`).

## 4. The switch

- **`settings.json` `gamePause`:** default on, set by the kit's `Set-GamePause.ps1`.
- **Shard Console (`scripts/Shard-Console.ps1`):** a new action `golem.gamepause`.
  - Its button sits in the Golem wake row after Self-wake and reads "Game pause: on (turn off)" / "off (turn on)".
  - It has a tooltip and help text. The plan runs `Set-GamePause.ps1 -On|-Off` in its own window, and the safety check
    allows only those exact arguments.
  - The `when` condition `gamePause:on|off` is understood.
  - The status document gains `golem.gamePause`: on, the game PC, whether a game is running, its line, and every
    `game-wait-*.json`. This comes from `Get-GamePauseDocument`, which never throws.
- **Web console:** `console-actions.json` maps the console action to its web button (P187's rule), and `golem-actions.json` gets **Game pause on** (shown while off; typed word "game pause on") and **Game
  pause off** (shown while on; "game pause off"). `static/app.js` adds the Golem page's "Game pause: on, no game
  running." line (or "... waiting: Chase is playing X: bot play testing waits", or "off") and one line per wait.

## Tests, red then green, and the dry-run night

The fake game in every real fact: `ping.exe` copied as `FakeGame.exe` into a temp `...\Steam\steamapps\common\FakeGame`
folder, started and stopped by the fact. Each fact uses a temp kit root with its own `settings.json`, never the real one.

- **Kit:** `D:\UO\golem\tests\GamePause.Tests.ps1`, 9 facts (34 checks):
  - our clients and Wallpaper Engine are not games;
  - a steamapps game is seen and named;
  - the switch off and another PC mean no pause;
  - `Set-GamePause` keeps the other keys;
  - the wait goes on when the game closes and shows the status file meanwhile;
  - the wait gives up at 06:30;
  - the CLI sees the real fake game and not after it closes;
  - the CLI waits while it runs and exits 0 when it closes;
  - the Legion guard refuses while a game runs.

  **Red** on the live kit before install: all 9 failed. **Green** on the scratch copy and again after install: 34 passed,
  0 failed. `LegionScript.Tests.ps1` (the guard's game look turned off for its own facts) passed 51 of 51.
  `GolemPower.Tests.ps1` passed 133 of 133 (unchanged).
- **Bot:** `tools/playtest-bot/tests/test_gamepause.py`, 7 facts:
  - the check sees the fake game;
  - the runner waits while it runs and goes on when it closes;
  - the runner skips the night when the game outlasts `-NightEnd`;
  - `-NoGameWait`;
  - a check waits for a game started mid-run (clients closed first) and resumes;
  - checks left at the night's end are SKIPPED and the report says so;
  - a split soak reads as one.

  **Red** on main's code: the test module would not import (no `uobot.gamepause`). With only the new helper added,
  6 of 7 failed; the check-only fact needs no runner change. **Green:** 7 of 7.
- **Goblin:** `scripts/tests/test_gamepause_goblin.py`, 3 facts: it waits and goes on; it skips at the night's end;
  `-NoGameWait`. **Red** on main's script: 2 of 3 failed. **Green:** 3 of 3.
- **Shard Console:** `scripts/tests/Shard-Console.Tests.ps1`, 3 new `P819_` facts: the switch's plan and its exact
  arguments, default on; the two web buttons; the status document with a wait. The wake row's order fact now includes
  the switch. Green.
  - **Full suite:** 455 facts, 437 passed, 18 failed. 17 of those fail exactly the same on main (a clean worktree of
    7055d95: 452 facts, 17 failed; the same names, mostly website, inventory, art-check and window-mode facts that
    need this PC's services). The 18th was this prompt's: `P187_EveryConsoleButtonHasAWebTwin` asked for the new console
    button's web twin. It is now in `web-console/console-actions.json` (`golem.gamepause` -> `gamepause-on`), and P187
    and P819 then passed 11 of 11.
- **Whole suites:**
  - web console 125 tests OK;
  - scripts 88 OK;
  - playtest bot 76 tests, one failure that is not this prompt's: `test_installer_dry_run_prints_the_call_and_registers_nothing`
    fails the same on main (a clean worktree of 7055d95), because the real "SL overnight play tests" task is registered
    on this PC.
- **One night's dry run:** `notes/cc-P819-tools/dry-night.ps1`. It used the real runner, the installed kit check and
  a fake game for about 70 seconds, with the interval at 20 s. The bot root is inside a "shard-migration" path, so Rule
  1 stopped the run right after the resume: no build, no container, the shared test shard untouched, `-NoEmail`. Its
  `overnight.log` is `notes/cc-P819-tools/dry-night-overnight.log`:

      2026-11-08 00:03  game pause: waiting: Chase is playing FakeGame; the overnight play tests waits, looking again every 20 s until 06:30
      2026-11-08 00:04  game pause: the game closed: the overnight play tests goes on (waited 1 min)
      2026-11-08 00:04  FAILED on 7055d95: Rule 1 refused: the bot world would be inside a repo (...)

  The FAILED line is the dry run's intended stop, not a fault.
- **Image:** nothing under `server/` or `docker/uo/` changed, so there was no Docker build (`sl-modernuo:cc-P819` not
  built). No test shard was started.

## Deviations and decisions for Chase

- **When it takes effect:** the kit part (the check, the switch script, the Legion guard) is live on the game PC now,
  and on the other PCs after the Tinker's next round. The night bots' waits, the Shard Console switch and the web
  console line take effect when this branch merges into `D:\ShatteredLegacy` and the two consoles restart.
- **The hand-off hook:** the Golem hand-off text (`golem.ps1`) was not changed. The guard's refusal itself says how to
  wait.
- **An existing test-order problem:** `P182_WindowStepsRunInThisProcessForTheWebConsole` fails after the P131 facts
  (a disposed text box from P131's form). It fails the same on main and was left alone.

P819 DONE
