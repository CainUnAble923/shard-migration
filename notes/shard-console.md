# Shard-Console.ps1: a GUI console for the test and live shards

2026-09-29. Built `D:\ShatteredLegacy\scripts\Shard-Console.ps1`: one PowerShell 5.1 file, WinForms, with a
status panel, test / live / snapshot / world-setup / diagnostics tabs, and `-DryRun`. Facts in
`scripts/tests/Shard-Console.Tests.ps1`, **44, all green**, run under Windows PowerShell 5.1. Exercised end to end on the
**test** shard for real. **Nothing was done to the live shard**: no live container started, stopped or restarted, no live
snapshot, no compose on the live file. Read-only calls against it only: `docker inspect sl-modernuo`,
`docker logs --since <StartedAt> sl-modernuo`, and a file listing of the live `Saves` folder. **Not committed.**

Files (all new, all in `D:\ShatteredLegacy`):

```
scripts/Shard-Console.ps1                                     the tool (core, shell, form)
scripts/tests/Shard-Console.Tests.ps1                         44 facts
scripts/tests/fixtures/console-capture-2026-09-29.txt         real capture, both shards (60 KB)
scripts/tests/fixtures/console-capture-probe-2026-09-29.txt   real owner-prompt capture (18 KB)
```

Run the facts:

    powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1

A desktop shortcut, if wanted (I did not create one; it is outside the repo):
target `powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "D:\ShatteredLegacy\scripts\Shard-Console.ps1"`.
Drop `-WindowStyle Hidden` for a console behind it.

---

## 1. Where it lives, and why

**`D:\ShatteredLegacy\scripts\`.** It already holds `sl.ps1`, the operator's service manager across all containers, and
`extract-server.ps1`. The console is operator tooling spanning both shards, which is that folder's job. The alternatives:

- `docker/uo/`, beside `Start-TestShard.ps1`: that folder is the build and compose definition for the image. A GUI
  there sits next to `build.sh` and invites being read as part of the build.
- The repo root, beside `Check-Docker.ps1` and `Check-Shard.ps1`: those write their output to `$PSScriptRoot`, so the
  root is where their `check-*.txt` / `shard-*.txt` land, and it is already crowded.

**Two things about that folder a reader should know.** `.gitignore` ignores `shard-*.txt` and `check-*.txt` anywhere in the
repo, so a fixture named `shard-...` would have been silently left out of every commit; the fixtures are named
`console-capture-*` for that reason. And the action log, `scripts/shard-console.log`, is ignored by `*.log`, which is
correct: it names who pressed what.

**Snapshots go in `server/lib/uo/modernuo/Snapshots/<test|live>/<yyyyMMdd-HHmmss>_<name>/`**, beside the saves, on the
same volume, and ignored by `server/lib/`. They contain `Accounts`, so they must never be committed; `git check-ignore`
confirms they are not reachable. Moved-aside saves sit beside the save they came from: `Saves-test.aside-<time>`,
`Saves.aside-<time>`.

## 2. How it is built

**Core and shell, as asked.** The core, top half of the file, takes strings and returns objects: parse `docker inspect`
and `docker image inspect`, parse logs for the listener and the owner prompt, compute drift, summarise a save listing,
name and validate snapshots, and **build every button as a plan**, a list of steps. The shell gathers the strings from
docker and the disk, and runs a plan or, under `-DryRun`, prints it. So **what `-DryRun` prints is the same list of steps
that runs**; there is no second description to drift out of date.

**`Test-PlanSafety` checks every plan before anything runs, dry or not**, and refuses one that would:
run `docker compose` itself (compose is reached only through `Start-TestShard.ps1`, which names the test file); run
`docker build|rm|rmi|run|create|commit|kill|system|volume|image|container|prune`; call `build.sh` directly; pass `-Fresh`;
name `sl-modernuo` or open the live client without a typed confirmation step; delete anything that is not exactly one
snapshot folder, or anything inside a save; or move anything but a save to `<save>.aside-<time>`.

**It calls the existing scripts.** Test start, stop and rebuild are `Start-TestShard.ps1 -SkipBuild`, `-Down`, and no
switches; the gates are only ever `build.sh`, only through that script. Diagnostics are `Check-Docker.ps1` and
`Check-Shard.ps1` unchanged. Live start, stop and restart are `docker start|stop -t 60|restart -t 60 sl-modernuo` on the
existing container, **never compose**: `docker/uo/docker-compose.yml` still has `build:` and no `image:` (D29, checked
2026-09-29 11:25), so the tool cannot build through it, and a named-container `docker` command cannot reach `sl-ddns`.

**Buttons that change anything run in a console window of their own**, as `Shard-Console.ps1 -Action <key>`, so each
step is printed as it happens ("Stopping sl-modernuo-test so nothing writes the save...", then the copy, then the
verify) and the form stays responsive through a multi-minute rebuild. That headless path is also how I tested
everything without clicking. `-NoExit` keeps the window open after the script's `exit`; checked.

### One decision I made rather than silently solved: "start fresh"

`Start-TestShard.ps1 -Fresh` **deletes** `Saves-test` (`Remove-Item $testSaves -Recurse -Force`). The brief asks for a
"start fresh" button **and** says no button deletes a world save. So the console's Start fresh stops the test shard
(`-Down`), **moves `Saves-test` aside**, and runs `Start-TestShard.ps1 -SkipBuild` without `-Fresh`. The script then finds
no `Saves-test` and runs exactly the seeding `-Fresh` runs (accounts and `SerializedTypes.db` from the live save, D19);
the only thing not reused is the one line that deletes. Verified for real below: it came up listening, not at the owner
prompt. It does not rebuild; Rebuild is its own button. If you would rather Start fresh also rebuild, it is one line.

## 3. The facts, red then green

The fixtures are real (the file header in the facts says how each was made). `-Capture` wrote the main one from the
running Docker; its only edit is `Remove-AccountLines`, which drops log lines naming accounts or client IPs because the
repo is public. The owner prompt could not be captured from either shard without breaking one, so I ran
`sl-modernuo:latest` once in a throwaway container: `--network none`, no published port, an empty scratch save, a copy of
`Configuration-test`. It stopped at the prompt, I captured it, and removed the container. That is shard AGENTS rule 6's
"throwaway loopback-only container with a scratch save directory".

**First run: red, 40 of 42, and the red was a real bug.**

```
  FAIL  TheSafetyCheckRejectsDeletingAWorldSave
        expected [0] but got [1]. one snapshot is fine
  FAIL  EveryRealPlanPassesTheSafetyCheck
        expected [0] but got [1]. test.start test : System.String[]
42 facts, 40 passed, 2 failed
```

`Test-PlanSafety` returned its result as `, $v.ToArray()`. When the list was empty, the caller's `@(...)` produced a
one-element array holding an empty array, so **every clean plan had one phantom violation and would have been refused.**
Worse, the three "rejects X" facts were passing *on that phantom*. Fixed the returns (three functions used the idiom),
and changed those facts to assert the **reason** a plan is refused, not a count of reasons.

**Then the gates, each broken on purpose** (AGENTS: a gate nobody has watched fail is not a gate). One behaviour broken at a
time in the real file, facts run, file restored and checked byte-identical by hash:

```
== BREAK A: judge drift by the NAME the container was created from
  FAIL  DriftComparesImageIdsNotTagNames
        expected [DRIFTED] but got [CURRENT].
  FAIL  TheTestContainerSaysTheTagMovedUnderIt
42 facts, 40 passed, 2 failed

== BREAK B: read the listener from a --tail instead of from StartedAt
  FAIL  TheLogIsReadFromStartedAtNotFromATail
        not true: reads from --since
42 facts, 41 passed, 1 failed

== BREAK C: restore deletes the current save instead of moving it aside
  FAIL  ARestoreStopsThenSnapshotsThenMovesAsideThenCopies
  FAIL  ARestoreNeverDeletesAnything
  FAIL  EveryRealPlanPassesTheSafetyCheck
        ... deletes a world save: D:\ShatteredLegacy\server\lib\uo\modernuo\Saves-test
42 facts, 39 passed, 3 failed

== BREAK D: live actions without the typed confirmation
  FAIL  ARestoreStopsThenSnapshotsThenMovesAsideThenCopies
  FAIL  ASnapshotOfARunningContainerStopsItAndStartsItAgain
  FAIL  EveryLiveActionBeginsWithATypedConfirmation
  FAIL  EveryRealPlanPassesTheSafetyCheck
        ... touches sl-modernuo without a typed confirmation: docker stop -t 60 sl-modernuo
42 facts, 38 passed, 4 failed

restored, hash identical: True
```

In C and D the plan facts **and** the independent safety check both go red, so either alone would have caught it.

**Two facts added after the end-to-end run found things**, each watched red before green:

- `TheExecutorRunsNothingWithoutTheTypedPhraseOrTheYes`. The plan facts prove a live plan *contains* a confirmation;
  this proves the executor *enforces* it. The step it guards writes a marker file, not a docker command, so a bug leaves
  evidence and touches nothing. Wrong phrases tried: none, empty, `Stop live`, `yes`, `stop`.
- `AnOldSaveIsOnlyStaleOnceTheServerHasHadTimeToSave`. See section 5. Red without the fix:
  `FAIL AnOldSaveIsOnlyStaleOnceTheServerHasHadTimeToSave / not true: just started: no warning`.

**Green:**

```
44 facts, 44 passed, 0 failed
```

The 44 cover: inspect parsing for both containers, nine-digit docker timestamps, year-1 "never", a missing container, an
image gone from the store; drift by ID not name, the moved tag, the live three-way ambiguity, a current container; the
listener on the game port not the ping port, an exited container, the wrong port, the owner prompt, the log read from
`StartedAt`; the save summary; snapshot names, round trip, pre-restore naming, last-snapshot warning; every plan's
shape (restore order, no deletes, stop-only-what-runs, typed confirmation on every live action, no compose, live start
refusing when the container is gone, start fresh never passing `-Fresh`, start skips the build and rebuild does not);
the safety check's refusals by reason; the executor; the D29 compose parse; redaction; the checklist against the pinned
tree; ASCII-and-no-BOM on both files; a clean parse under 5.1; and the form building from a capture without being shown.

## 4. The `-DryRun` transcript of every button

Produced by `Shard-Console.ps1 -DryRun -Action <key> -StatusFrom <capture>`, one call per button, from the committed
real capture: test container **exited**, live **running**, so both halves of "stop only what is running" show. **Two
lines were added to a copy of that capture**: one example snapshot per shard, because restore and delete need
something to act on and a real live snapshot would mean stopping live. The second `live.start` uses a copy **edited to
say live is stopped**, only so you can see what Start would run; as captured, live is running and Start refuses.
Timestamps in names are the capture time. `<repo>` is `D:\ShatteredLegacy\`.

In the form, a live button shows this same plan inside the typed-confirmation dialog before it will run.

```
== DRY RUN: test.start (test) ========================================================
  1. SAY      Start the test shard on the image already tagged sl-modernuo:latest: no build, no gates. Start-TestShard.ps1 recreates the container if that image has changed, then waits for the listener and reports the owner prompt if the world has no accounts.
  2. RUN      powershell.exe -NoProfile -ExecutionPolicy Bypass -File <repo>\docker\uo\Start-TestShard.ps1 -SkipBuild
         # docker/uo/Start-TestShard.ps1 -SkipBuild
  3. LOG      one timestamped line: test.start

== DRY RUN: test.fresh (test) ========================================================
  1. SAY      Start fresh. Start-TestShard.ps1 -Fresh would DELETE Saves-test, and no button here deletes a world save, so instead: stop the test shard, move Saves-test aside, and start without -Fresh. Start-TestShard.ps1 then finds no Saves-test and seeds a new one exactly as -Fresh does (accounts and SerializedTypes.db from the live save, D19). No build.
  2. RUN      powershell.exe -NoProfile -ExecutionPolicy Bypass -File <repo>\docker\uo\Start-TestShard.ps1 -Down
         # docker/uo/Start-TestShard.ps1 -Down
  3. CHECK    docker inspect says sl-modernuo-test is not running; stop here if it is
  4. MOVE     <repo>\server\lib\uo\modernuo\Saves-test  ->  <repo>\server\lib\uo\modernuo\Saves-test.aside-20260929-112207   (if it exists)
         # Moving the test save aside (if there is one). It is kept, not deleted.
  5. RUN      powershell.exe -NoProfile -ExecutionPolicy Bypass -File <repo>\docker\uo\Start-TestShard.ps1 -SkipBuild
         # docker/uo/Start-TestShard.ps1 -SkipBuild
  6. LOG      one timestamped line: test.fresh, old save moved to <repo>\server\lib\uo\modernuo\Saves-test.aside-20260929-112207

== DRY RUN: test.stop (test) =========================================================
  1. RUN      powershell.exe -NoProfile -ExecutionPolicy Bypass -File <repo>\docker\uo\Start-TestShard.ps1 -Down
         # docker/uo/Start-TestShard.ps1 -Down: compose down on the sl-uo-test project only (D22). A stop does not save: play since the last autosave (every 5 minutes) is lost. [save in game first if that matters.
  2. LOG      one timestamped line: test.stop

== DRY RUN: test.rebuild (test) ======================================================
  1. SAY      Rebuild through the gates, then start. build.sh runs the patch gate, then the shard tests, then builds the image; if a gate fails nothing is started. This takes minutes.
  2. RUN      powershell.exe -NoProfile -ExecutionPolicy Bypass -File <repo>\docker\uo\Start-TestShard.ps1
         # docker/uo/Start-TestShard.ps1 (no switches: build.sh, then start)
  3. LOG      one timestamped line: test.rebuild

== DRY RUN: test.tail (test) =========================================================
  1. WINDOW   a new PowerShell window running: docker logs -f --tail 200 sl-modernuo-test
         # Following the sl-modernuo-test log in its own window. Read-only; close the window to stop.

== DRY RUN: test.client (test) =======================================================
  1. OPEN     D:\UO\Play-SL-Admin-TEST.bat
         # Opening a client for the TEST shard.

   (as captured: live is running)
== DRY RUN: live.start (live) ========================================================
  1. CONFIRM  typed: you must type exactly 'start live'. This acts on the LIVE shard (sl-modernuo).
  2. REFUSE   sl-modernuo is already running. Nothing to do.

   (EDITED capture: live stopped)
== DRY RUN: live.start (live) ========================================================
  1. CONFIRM  typed: you must type exactly 'start live'. This acts on the LIVE shard (sl-modernuo).
  2. RUN      docker start sl-modernuo
         # docker start on the existing container: the same container and the same image it had. Never compose (D29).
  3. LOG      one timestamped line: live.start

== DRY RUN: live.stop (live) =========================================================
  1. CONFIRM  typed: you must type exactly 'stop live'. This acts on the LIVE shard (sl-modernuo).
  2. RUN      docker stop -t 60 sl-modernuo
         # docker stop, waiting up to 60 seconds for a save in progress to finish. A stop does not save: play since the last autosave (every 5 minutes) is lost. [save in game first if that matters. Players are disconnected.
  3. LOG      one timestamped line: live.stop

== DRY RUN: live.restart (live) ======================================================
  1. CONFIRM  typed: you must type exactly 'restart live'. This acts on the LIVE shard (sl-modernuo).
  2. RUN      docker restart -t 60 sl-modernuo
         # docker restart: the same container and the SAME IMAGE. It deploys nothing and the drift line will not change. A stop does not save: play since the last autosave (every 5 minutes) is lost. [save in game first if that matters. Players are disconnected.
  3. LOG      one timestamped line: live.restart

== DRY RUN: live.tail (live) =========================================================
  1. CONFIRM  typed: you must type exactly 'tail live'. This acts on the LIVE shard (sl-modernuo).
  2. WINDOW   a new PowerShell window running: docker logs -f --tail 200 sl-modernuo
         # Following the sl-modernuo log in its own window. Read-only; close the window to stop.

== DRY RUN: live.client (live) =======================================================
  1. CONFIRM  typed: you must type exactly 'open live client'. This acts on the LIVE shard (sl-modernuo).
  2. OPEN     D:\UO\Play-SL-Admin.bat
         # Opening a client for the LIVE shard.

== DRY RUN: snapshot.create (test) ===================================================
  1. SAY      sl-modernuo-test is exited, so nothing is writing the save. It stays stopped.
  2. COPY     <repo>\server\lib\uo\modernuo\Saves-test  ->  <repo>\server\lib\uo\modernuo\Snapshots\test\20260929-112207_before-gargoyle-fix   (refuses if the target exists)
         # Copying the TEST save, accounts included, to the snapshot.
  3. VERIFY   <repo>\server\lib\uo\modernuo\Snapshots\test\20260929-112207_before-gargoyle-fix has the same file count and bytes as <repo>\server\lib\uo\modernuo\Saves-test; stop here if not
  4. LOG      one timestamped line: snapshot.create test -> <repo>\server\lib\uo\modernuo\Snapshots\test\20260929-112207_before-gargoyle-fix

== DRY RUN: snapshot.create (live) ===================================================
  1. CONFIRM  typed: you must type exactly 'snapshot live'. This acts on the LIVE shard (sl-modernuo).
  2. RUN      docker stop -t 60 sl-modernuo
         # Stopping sl-modernuo so nothing writes the save while it is copied. It is started again at the end. A stop does not save: play since the last autosave (every 5 minutes) is lost. [save in game first if that matters. Players are disconnected.
  3. CHECK    docker inspect says sl-modernuo is not running; stop here if it is
  4. COPY     <repo>\server\lib\uo\modernuo\Saves  ->  <repo>\server\lib\uo\modernuo\Snapshots\live\20260929-112207_before-deploy   (refuses if the target exists)
         # Copying the LIVE save, accounts included, to the snapshot.
  5. VERIFY   <repo>\server\lib\uo\modernuo\Snapshots\live\20260929-112207_before-deploy has the same file count and bytes as <repo>\server\lib\uo\modernuo\Saves; stop here if not
  6. RUN      docker start sl-modernuo
         # Starting sl-modernuo again, as it was before. Same container, same image.
  7. LOG      one timestamped line: snapshot.create live -> <repo>\server\lib\uo\modernuo\Snapshots\live\20260929-112207_before-deploy

== DRY RUN: snapshot.create (test) ===================================================
  1. REFUSE   Snapshot name 'my pre-restore': use letters, digits, dot, dash and underscore, starting with a letter or digit

== DRY RUN: snapshot.list (test) =====================================================
  1. SAY      20260929-101500_before-gargoyle-fix  2026-09-29 10:15:00  764 KB  21 files  accounts

== DRY RUN: snapshot.list (live) =====================================================
  1. SAY      20260929-101500_before-deploy  2026-09-29 10:15:00  32.6 MB  20 files  accounts

== DRY RUN: snapshot.restore (test) ==================================================
  1. SAY      Restoring 20260929-101500_before-gargoyle-fix onto the TEST shard. The current save is snapshotted first, then moved aside. Nothing is deleted.
  2. SAY      sl-modernuo-test is exited, so nothing is writing the save. It stays stopped.
  3. COPY     <repo>\server\lib\uo\modernuo\Saves-test  ->  <repo>\server\lib\uo\modernuo\Snapshots\test\20260929-112207_PRE-RESTORE_before-restoring-20260929-101500_before-gargoyle-fix   (refuses if the target exists)
         # The automatic pre-restore snapshot of the current save.
  4. VERIFY   <repo>\server\lib\uo\modernuo\Snapshots\test\20260929-112207_PRE-RESTORE_before-restoring-20260929-101500_before-gargoyle-fix has the same file count and bytes as <repo>\server\lib\uo\modernuo\Saves-test; stop here if not
  5. MOVE     <repo>\server\lib\uo\modernuo\Saves-test  ->  <repo>\server\lib\uo\modernuo\Saves-test.aside-20260929-112207
         # Moving the current save aside. It is kept, not deleted.
  6. COPY     <repo>\server\lib\uo\modernuo\Snapshots\test\20260929-101500_before-gargoyle-fix  ->  <repo>\server\lib\uo\modernuo\Saves-test   (refuses if the target exists)
         # Copying 20260929-101500_before-gargoyle-fix in as the save.
  7. VERIFY   <repo>\server\lib\uo\modernuo\Saves-test has the same file count and bytes as <repo>\server\lib\uo\modernuo\Snapshots\test\20260929-101500_before-gargoyle-fix; stop here if not
  8. LOG      one timestamped line: snapshot.restore test <- 20260929-101500_before-gargoyle-fix; pre-restore <repo>\server\lib\uo\modernuo\Snapshots\test\20260929-112207_PRE-RESTORE_before-restoring-20260929-101500_before-gargoyle-fix; old save <repo>\server\lib\uo\modernuo\Saves-test.aside-20260929-112207

== DRY RUN: snapshot.restore (live) ==================================================
  1. CONFIRM  typed: you must type exactly 'restore live'. This acts on the LIVE shard (sl-modernuo).
  2. SAY      Restoring 20260929-101500_before-deploy onto the LIVE shard. The current save is snapshotted first, then moved aside. Nothing is deleted.
  3. RUN      docker stop -t 60 sl-modernuo
         # Stopping sl-modernuo so nothing writes the save while it is copied. It is started again at the end. A stop does not save: play since the last autosave (every 5 minutes) is lost. [save in game first if that matters. Players are disconnected.
  4. CHECK    docker inspect says sl-modernuo is not running; stop here if it is
  5. COPY     <repo>\server\lib\uo\modernuo\Saves  ->  <repo>\server\lib\uo\modernuo\Snapshots\live\20260929-112207_PRE-RESTORE_before-restoring-20260929-101500_before-deploy   (refuses if the target exists)
         # The automatic pre-restore snapshot of the current save.
  6. VERIFY   <repo>\server\lib\uo\modernuo\Snapshots\live\20260929-112207_PRE-RESTORE_before-restoring-20260929-101500_before-deploy has the same file count and bytes as <repo>\server\lib\uo\modernuo\Saves; stop here if not
  7. MOVE     <repo>\server\lib\uo\modernuo\Saves  ->  <repo>\server\lib\uo\modernuo\Saves.aside-20260929-112207
         # Moving the current save aside. It is kept, not deleted.
  8. COPY     <repo>\server\lib\uo\modernuo\Snapshots\live\20260929-101500_before-deploy  ->  <repo>\server\lib\uo\modernuo\Saves   (refuses if the target exists)
         # Copying 20260929-101500_before-deploy in as the save.
  9. VERIFY   <repo>\server\lib\uo\modernuo\Saves has the same file count and bytes as <repo>\server\lib\uo\modernuo\Snapshots\live\20260929-101500_before-deploy; stop here if not
 10. RUN      docker start sl-modernuo
         # Starting sl-modernuo again, as it was before. Same container, same image.
 11. LOG      one timestamped line: snapshot.restore live <- 20260929-101500_before-deploy; pre-restore <repo>\server\lib\uo\modernuo\Snapshots\live\20260929-112207_PRE-RESTORE_before-restoring-20260929-101500_before-deploy; old save <repo>\server\lib\uo\modernuo\Saves.aside-20260929-112207

== DRY RUN: snapshot.delete (test) ===================================================
  1. ASK      yes/no: Delete the snapshot 20260929-101500_before-gargoyle-fix of the TEST shard (764 KB)? This is the LAST snapshot of the TEST shard. After this there are none.
  2. DELETE   <repo>\server\lib\uo\modernuo\Snapshots\test\20260929-101500_before-gargoyle-fix
         # Deleting the snapshot folder. A snapshot, never a world save.
  3. LOG      one timestamped line: snapshot.delete test 20260929-101500_before-gargoyle-fix

== DRY RUN: snapshot.delete (live) ===================================================
  1. CONFIRM  typed: you must type exactly 'delete live snapshot'. This acts on the LIVE shard (sl-modernuo).
  2. ASK      yes/no: Delete the snapshot 20260929-101500_before-deploy of the LIVE shard (32.6 MB)? This is the LAST snapshot of the LIVE shard. After this there are none.
  3. DELETE   <repo>\server\lib\uo\modernuo\Snapshots\live\20260929-101500_before-deploy
         # Deleting the snapshot folder. A snapshot, never a world save.
  4. LOG      one timestamped line: snapshot.delete live 20260929-101500_before-deploy

== DRY RUN: diag.docker (test) =======================================================
  1. RUN      powershell.exe -NoProfile -ExecutionPolicy Bypass -File <repo>\Check-Docker.ps1
         # Check-Docker.ps1: writes check-HHmmss.txt in D:\ShatteredLegacy

== DRY RUN: diag.shard (test) ========================================================
  1. RUN      powershell.exe -NoProfile -ExecutionPolicy Bypass -File <repo>\Check-Shard.ps1
         # Check-Shard.ps1: writes shard-HHmmss.txt in D:\ShatteredLegacy. It reads the TEST container only.

== DRY RUN: diag.folder (test) =======================================================
  1. OPEN     explorer.exe D:\ShatteredLegacy
         # Opening the folder the diagnostics write to.
```

## 5. End to end on the test shard, for real

Headless, through the same `-Action` path the buttons spawn. Every step printed, every mutating step logged.

| Step | What happened |
|---|---|
| `-Status` before | Test: exited 255, **DRIFTED** (running `2e7dcae65e54`, gone from the store; `sl-modernuo:latest` moved to `8304d4a24fd2`). Live: listening on 2593, DRIFTED, ambiguous (below) |
| `test.start` | `Start-TestShard.ps1 -SkipBuild`. Compose printed **`Recreate`**: it recreated the container on the new image, so the advice line ("Start recreates it, a docker restart does not") is true. Status: **CURRENT, LISTENING on 127.0.0.1:2594, 172.27.0.2:2594** |
| `snapshot.create console-e2e-before` while running | `docker stop -t 60`, stopped-check, copy, verify **21 files 782,574 bytes both sides**, `docker start`. Came back up |
| `test.fresh` | `-Down`, move `Saves-test` to `Saves-test.aside-20260929-112645`, `-SkipBuild`. The script seeded 3 files (accounts, type table) and the shard came up **LISTENING, not at the owner prompt** |
| `snapshot.restore` while running | stop, check, PRE-RESTORE snapshot (3 files, verified), move aside, copy the snapshot in (21 files 782,574 bytes, verified), start. LISTENING |
| `snapshot.delete` without `-Yes` | **refused**, snapshot still there |
| `snapshot.delete` PRE-RESTORE, with `-Yes` | the question said "It is an automatic pre-restore snapshot". Deleted |
| `snapshot.delete` the last one | the question said **"This is the LAST snapshot of the TEST shard. After this there are none."** Deleted |
| `test.stop` | `-Down` |
| `diag.docker` | ran `Check-Docker.ps1`, which wrote `check-112956.txt` |

**What it found.** Right after the restore, the panel said **"NOT SAVING? nothing written for 1d 0h"** thirteen seconds
after the start. A copied save keeps its files' old timestamps until the first autosave. The warning now needs the
container to have been up past the threshold too, with a fact.

**And from rendering the form** (below): the close handler called `$timer.Stop()` on a variable local to the function
that built the form, so **closing the window threw** once that function had returned, which is how the real entry point
calls it. Now `$script:ui.Timer`.

The action log from the run, `scripts/shard-console.log`:

```
2026-09-29 11:25:20 ckfle START test.start shard=test
2026-09-29 11:25:39 ckfle DONE  test.start
2026-09-29 11:25:59 ckfle START snapshot.create shard=test
2026-09-29 11:26:33 ckfle DONE  snapshot.create test -> ...\Snapshots\test\20260929-112559_console-e2e-before
2026-09-29 11:26:45 ckfle START test.fresh shard=test
2026-09-29 11:27:55 ckfle DONE  test.fresh, old save moved to ...\Saves-test.aside-20260929-112645
2026-09-29 11:28:12 ckfle START snapshot.restore shard=test
2026-09-29 11:28:19 ckfle DONE  snapshot.restore test <- 20260929-112559_console-e2e-before; pre-restore ...; old save ...\Saves-test.aside-20260929-112812
2026-09-29 11:29:31 ckfle START snapshot.delete shard=test
2026-09-29 11:29:31 ckfle DONE  snapshot.delete test 20260929-112812_PRE-RESTORE_before-restoring-20260929-112559_console-e2e-before
2026-09-29 11:29:36 ckfle START snapshot.delete shard=test
2026-09-29 11:29:36 ckfle DONE  snapshot.delete test 20260929-112559_console-e2e-before
2026-09-29 11:29:51 ckfle START test.stop shard=test
2026-09-29 11:29:53 ckfle DONE  test.stop
```

**What it left behind, deliberately:**

- **`Saves-test` is the world it was before**: 21 files, 782,574 bytes, restored from the snapshot.
- **`sl-modernuo-test` no longer exists.** It was an exited container on a stale image; `test.stop` is compose down,
  which removes it. The next Start creates it on the current `sl-modernuo:latest`.
- **Two moved-aside saves, not deleted, because nothing here deletes a save**:
  `Saves-test.aside-20260929-112645` (21 files, a duplicate of the restored world) and
  `Saves-test.aside-20260929-112812` (3 files, the fresh seeded one). Delete them in Explorer if you do not want them.
  The panel lists asides so they do not pile up unseen.
- An empty `Snapshots\test\`, `scripts/shard-console.log`, and `check-112956.txt`. The last two are gitignored.

## 6. What I could not test without a GUI, named honestly

**Rendered and looked at, not clicked.** I showed the form in `-DryRun`, screenshotted my own window per tab and closed
it, which is how the close bug was found. I also opened the typed-confirmation dialog for `live.stop` and set its
text box programmatically: **"Do it" stayed disabled for `Stop live` and enabled only for `stop live`**, and the dialog
returned false on Cancel. One dry-run button was driven through `Invoke-ConsoleButton`, the same function a click calls.
**Please check by hand:**

1. **Every button click.** Handlers were attached and the form built (a fact), but no click was made. Most likely to be
   wrong: the snapshot tab's Restore and Delete reading the selected row.
2. **The spawned window's arguments.** For a live action the form starts
   `powershell -NoExit -File Shard-Console.ps1 -Action live.stop -Shard live -ConfirmLive "stop live"`. The headless side
   was run for real only for test actions; **the quoting of `-ConfirmLive "stop live"` through `Start-Process` has not been
   run**, because running it means stopping live. If the quoting were wrong, the executor refuses (the phrase will not match),
   which fails safe. Worth one `-DryRun` click to see the window say `DRY RUN`.
   **Wrong, and it cost a live stop (bug-list D37).** Under the code as written, a `-DryRun` click never opened a window
   at all: the parent printed the plan and returned before the dialog. And the argument line it would have built carried
   no mode, so a child it did open ran for real. The "one dry-run button driven through `Invoke-ConsoleButton`" above was
   a button that runs in the console, which never builds that line. See 6.1.
3. **The yes/no box for deleting a snapshot**, and that "No" is the default button (it is set to Button2).
4. **The Copy buttons** on World setup (clipboard needs STA; `powershell.exe` 5.1 is STA by default).
5. **The 30-second auto-refresh.** It runs about eight docker calls on the UI thread; expect the form to hitch for a second
   or so each time. Untick it if that annoys.
6. **Tail the log and Open a client** were not launched (`D:\UO\Play-SL-Admin-TEST.bat`, `D:\UO\Play-SL-Admin.bat`).
7. **Rebuild through the gates** was not run for real: it is `Start-TestShard.ps1` with no switches, the same path the
   existing desktop shortcut runs, and running it would have retagged `sl-modernuo:latest` for no reason. Dry run only.
8. **`diag.shard`** was not run for real (`diag.docker` was).
9. **Every live action**: none run for real, by the rule. The live snapshot and restore plans are the test ones with the
   container name and a confirmation changed, and those were run for real on test. `docker start|stop|restart` on
   `sl-modernuo` are unexercised by this tool.
10. **High-DPI scaling.** Screenshots were at this machine's scaling only.

### 6.1 D37, 2026-09-29: the mode is explicit and a missing one fails safe

**What happened.** T-018 pressed Stop on live and typed the phrase, and `sl-modernuo` stopped. T-017 created, restored and
deleted a test snapshot for real. `scripts/shard-console.log` has `live.stop` at 13:50:52 and the snapshot runs at
14:28-14:33.

**What I found, and what I could not.** The child's argument line never carried `-DryRun`, as reported. But in the
committed code a dry console could not reach it: `Invoke-ConsoleButton` printed the plan and returned *before* the phrase
dialog and `Start-Process` when `$script:dry` was set. I checked that the click handler sees the flag with a small
WinForms repro run with `-File`: the handler read `dry=True`. So **the console that showed the phrase dialog was not in
`-DryRun`**. The log does not record the mode, and I cannot tell how the console came to be live. Whatever the cause, the
child did whatever its command line said, and that is what is fixed.

**What changed** (`D:\ShatteredLegacy\scripts\Shard-Console.ps1`):

1. **The parent always names the mode.** `Get-ChildArgumentLine` (`:488`) builds the line and puts `-Mode DryRun` or
   `-Mode Execute` straight after `-File`. `Invoke-ConsoleButton` (`:1685`) calls it with `-DryRun:$script:dry`.
2. **The child refuses without one.** `Resolve-RunMode` (`:507`): `-DryRun` or `-Mode DryRun` gives `dry` and wins over
   `Execute`; `-Mode Execute` gives `execute`; no mode gives `refuse` for any action marked `Mutates` and for an unknown
   key, and `execute` only for the read-and-open actions (`diag.*`, tail, client, list). The headless entry decides this
   first and exits 2 before reading any state (`:2023-2028`). **Headless use is now `-Mode Execute -Action ...`.**
   Nothing in either repo called it any other way (grepped).
3. **Every spawned window says its mode first.** `Get-ModeBanner` (`:519`) prints a four-line banner, `DRY RUN`,
   `RUNNING FOR REAL` or `REFUSED`, before any state is read, and sets the window title to the same word.
4. **A dry click now takes the real path.** For a window action, a dry console prints the plan and then goes on through
   the same phrase dialog and yes/no box and opens the window, which prints and exits. That is what T-018 expected. The
   dialogs carry `DRY RUN` in their titles, the yes/no box is now `Show-YesNo` (`:1642`) so it can be stubbed, and a dry
   run that ever reaches `Invoke-Plan` from the form throws (`:1690`). Actions that run in the console still only print.
5. **D36, the related one.** The typed confirmation now opens with `BEFORE YOU TYPE: A stop does not save...` for every
   plan that stops a shard (`Get-ConfirmPreface`, `:472`). I did not make the console send `[save`: I have not worked
   out or tested a way to put a command into the server console inside the container.

**The facts** (`scripts/tests/Shard-Console.Tests.ps1:633-820`; 53 before, 63 now, 63 green under 5.1):

- `Invoke-ClickCapture` runs `Invoke-ConsoleButton`, the function a click calls, with the dialogs answered yes, the
  state given, and `Start-Process` and `Invoke-Plan` replaced by recorders. It covers **every `RunIn = 'window'` action on
  every shard it can act on, 13 cases**, dry and real: exactly one window, `-Mode DryRun` or `-Mode Execute` and never the
  other, nothing run in the console. `live.start` gets a copy of the capture with live stopped, because on the capture it
  correctly refuses ("already running") and opens nothing. A named fact pins the three that hit D37: `live.stop` with
  `-ConfirmLive "stop live"`, `snapshot.restore` with the selected `-Snapshot`, `snapshot.delete` with `-Snapshot` and `-Yes`.
- **Then the real child.** A `docker.exe` compiled by the facts, which appends its arguments to a file and exits 1, goes
  first on PATH. It is an `.exe` because `Invoke-DockerRead` uses `ProcessStartInfo`, which does not find `.cmd`. Before
  any child runs, both `Get-Command` and `where.exe` must resolve to it, or no child is launched. For `live.stop`,
  `snapshot.restore` and `snapshot.delete` on live, `powershell.exe` runs on the captured line: dry, it exits 0, the
  banner's second line is `DRY RUN  <action>`, the plan prints, **zero docker calls**; given the old line with the mode
  removed, it exits 2, says `REFUSED`, **zero docker calls**.

**Each gate watched failing**, one break at a time in the real file, facts run, file restored and checked
byte-identical by hash:

| Broken | Red |
|---|---|
| parent drops `-Mode` (the D37 shape) | 4: both click facts, the named three, the dry child (it refused) |
| parent always passes `Execute` | 3: dry click, named three, dry child (**4 docker calls, all to the recorder**) |
| child runs when no mode is given | 2: the mode fact, the old-line child (**4 docker calls, all to the recorder**) |
| child prints no banner | 2: both real-child facts |

My first try at the second break used a replacement string that also matched two `Get-ConsoleState` calls, so it was
wider than one line, and the form fact made read-only `docker inspect` calls against real docker. I re-ran it against
only the spawn line and the table shows that run.

**Not verified:** the change in a client. The facts stop at `Start-Process`'s argument string and at `powershell.exe`
run with `-NoNewWindow`. A real click opens a real window through `Start-Process` with no redirection, which is
T-017 and T-018. Those are Chase's to re-run, and they stay as they are in the queue.

### 6.2 A DRY RUN toggle in the form, 2026-09-29

Asked for after 6.1. A checkbox by Refresh, **DRY RUN: buttons print, nothing runs**, flips the buttons at runtime.

**One flag became two.** `$script:dry` now means only "buttons print". `$script:fromCapture` means "the status panel
reads a capture file", and only launching with `-DryRun` sets it. So:

- **Launched normally**, the box starts off. Ticked, every button behaves as it does under `-DryRun`: here-actions print,
  window actions go through the real dialogs and open a window that prints. **The status stays live from docker.** The
  window title and the box both turn DRY RUN, and the output pane logs each change.
- **Launched with `-DryRun`**, the box is ticked and greyed out, labelled locked. A plan built from a capture file must
  never run for real. `Set-ConsoleDryRun` (`scripts/Shard-Console.ps1:1652`) will not turn it off. Behind the lock,
  `Invoke-ConsoleButton` refuses outright if the status is a capture and dry is off (`:1685`).
- **A dry child spawned from a docker-status console** gets `-StatusFromDocker`, a new switch, so it builds its plan from
  the same docker state the parent showed, not from the capture fixture. It still decides its mode and prints its banner
  before reading anything. A real child is never given the switch.

**Facts** (68 now, all green): the toggle over all 13 window cases gives `-Mode DryRun` and `-StatusFromDocker`; a
capture console with dry off opens and runs nothing, in all 13; a form built with docker status (state stubbed) starts off
and usable, ticking flips `$script:dry` and the title, and the status reads stayed non-dry throughout; a `-DryRun` form's
box is ticked, disabled, and cannot be turned off from code. **End to end**, the real child of a toggled `live.stop`, with
the recording `docker.exe`, exits 0 with the DRY RUN banner, reads docker, and makes no call whose verb changes anything.

**Watched failing**, one break at a time, restored byte-identical each time: the toggle not reaching `$script:dry` (the form
fact red), the lock removed (the lock fact red), the guard behind it removed (the capture fact red), the child not told
`-StatusFromDocker` (2 red), and `-Mode DryRun` no longer honoured (4 red).

**Not proven:** the "no mutating verb" filter in that end-to-end fact has never been seen failing. The recorder answers
every call with exit 1, so the child sees live as missing and its plan stops before any stop step. I checked the regex
separately against `stop -t 60 sl-modernuo` and `restart ...` (match) and the read verbs (no match). And a slip of mine:
the first version of that regex held a literal backspace instead of `\b`, so it matched nothing, and the fact passed
anyway. The ASCII-only fact caught the byte. **Rendered, not clicked:** I drew the real form with the box ticked. The
title read `Shard Console - DRY RUN - ...` and the box showed amber and bold. Clicking it by hand is for the client pass.

## 7. Section 3 of the brief: what `docker inspect` and the logs can and cannot give

Everything asked for is shown. Where it comes from, and the limits:

| Asked for | Source | Limit |
|---|---|---|
| name, state, uptime | `docker inspect`: `.Name`, `.State.Status/Running/StartedAt/FinishedAt/ExitCode` | none. Timestamps have nine fractional digits, which .NET will not parse unaided (a fact covers it) |
| image each container runs vs `sl-modernuo:latest` | `.Image` (the ID) against `docker image inspect sl-modernuo:latest` `.Id` | **once the running image is untagged, `docker image inspect <that ID>` says "No such image"**, so its ID is known and its build date is not. True right now of **both** containers' images (the test one until I restarted it) |
| the tag it was started from | `.Config.Image` | this is the **string** used at creation. Docker keeps nothing saying what that string meant then, beyond `.Image` itself |
| listener open | the server's own `Listening: <addr>:<port>` line (`NetState.Network.cs:138`), read with `docker logs --since <StartedAt> --until <StartedAt+15m>` | **a `--tail` cannot see it**: after a day of autosaves it is over a thousand lines back (1,410 lines in the live log since its start, captured). The ping listener on 12000 writes the same words and is excluded by port and `(Pings)`. **In real logs the colour codes sit between address and port on the ping lines**, which an invented fixture would not have had. The line proves the listener opened at start; nothing short of a real client proves it is open now, since Docker's forwarder answers any port probe |
| owner-account prompt | `Do you want to create the owner account now? (y/n):` (`AccountPrompt.cs:15`), captured from the probe | none. A prompt with no later `Listening` line, in a running container, reads OWNER PROMPT |
| newest save file and time | the file system, not docker | **a restored or freshly seeded save carries old timestamps until the first autosave** (section 5). Handled |
| snapshot count and newest | the file system | none |

### The drift check is ambiguous, as the brief expected, and it shows everything rather than picking

The live container is the case. As of 2026-09-29:

```
running    : 36cc709a82a6  (no longer in the image store: untagged or removed since)
created as : 'uo-modernuo', which now means bc04a35bf344  <- the name has moved since this container was created
latest     : 8304d4a24fd2 = sl-modernuo:latest, built 2026-09-29 06:53:29
AMBIGUOUS  : created from 'uo-modernuo', not sl-modernuo:latest. ...
AMBIGUOUS  : the name 'uo-modernuo' and the image this container runs no longer agree. ...
```

Three different images, three names for them, and none of them is what the container runs according to its tag. The
verdict line says **DRIFTED** because the running ID is not `sl-modernuo:latest`'s ID, which is the comparison the brief
defined. But **"drifted from what you meant" has no single answer here**: someone who means "the tag the live shard was
set up with" gets `bc04a35b`, and someone who means "what we build now" gets `8304d4a2`. The panel prints the tag, what
the tag resolves to now, the running ID, and latest, and says AMBIGUOUS in two ways, without choosing.

The test container had the smaller version of the same thing before I restarted it: created from `sl-modernuo:latest`,
running `2e7dcae6`, while `sl-modernuo:latest` meant `8304d4a2`. **A check on the name would have called it current.**
Fact `DriftComparesImageIdsNotTagNames` exists for that, and break A shows it failing when the check uses the name.

## 8. World setup

A read-only checklist with a Copy button per line, in the order to run them. Syntax from `docker/uo/SERVER.md:355-357`
(`[GenerateSpawners <pattern relative to Distribution>`). Access levels from the source that registers each command.

**The brief said ten spawn files. `notes/reachability-audit.md` section 5 lists twelve paths** (nine distinct file names;
Sanctuary, PrismOfLight and Vendors each appear for two facets). I counted them in pinned
`Distribution/Data/Spawns` and **all twelve exist**; a fact checks that on every run while the pinned tree is present.

```
[GenerateSpawners Data/Spawns/post-uoml/termur/Abyss.json       Developer
[GenerateSpawners Data/Spawns/post-uoml/termur/TerMur.json      Developer
[GenerateSpawners Data/Spawns/post-uoml/termur/Underworld.json  Developer
[GenerateSpawners Data/Spawns/shared/malas/Citadel.json         Developer
[GenerateSpawners Data/Spawns/shared/malas/Labyrinth.json       Developer
[GenerateSpawners Data/Spawns/shared/trammel/Sanctuary.json     Developer
[GenerateSpawners Data/Spawns/shared/felucca/Sanctuary.json     Developer
[GenerateSpawners Data/Spawns/shared/trammel/PrismOfLight.json  Developer
[GenerateSpawners Data/Spawns/shared/felucca/PrismOfLight.json  Developer
[GenerateSpawners Data/Spawns/post-uoml/trammel/Vendors.json    Developer
[GenerateSpawners Data/Spawns/post-uoml/felucca/Vendors.json    Developer
[GenerateSpawners Data/Spawns/post-uoml/trammel/Outdoors.json   Developer
[GenerateNewShame                                               Administrator
[SetupDespise                                                   GameMaster
[save                                                           Administrator
```

Three things read from source while building it, none acted on:

- **`[GenerateSpawners` needs AccessLevel Developer**, not Administrator
  (`ModernUO-pinned/Projects/UOContent/Engines/Spawners/Commands/ImportSpawnersCommand.cs:23`, registered as
  `ImportSpawners` with `GenerateSpawners` as an alias at `:27`). An Administrator account cannot run it.
- **`SERVER.md:362` says repeated runs "may duplicate decorations or spawners". For JSON spawn files the pinned code does
  not duplicate**: before placing each spawner it deletes spawners of the same type at the same location
  (`ImportSpawnersCommand.cs:228-241`) and any with the same GUID (`:251-253`). Re-running a spawn file replaces and
  respawns. Decorations are a different command and I did not read it. The checklist says "re-running replaces"; SERVER.md
  is Chase's to correct or not.
- **Both generators are safe to re-run**: `[SetupDespise` returns "Despise appears to already be setup" when the controller
  exists (`customizations/Services/Revamped Dungeons/DespiseRevamped/Setup.cs`, `SetupDespise()`), and
  `[GenerateNewShame` skips altars and walls already present (`Shame Revamped/Generate.cs`, `CheckForAltar` in `PlaceAltar`
  and `PlaceWall`) and generates spawners only if none exist (`ShameSpawns.AnyPresent()`).

The ticks are for the session and are not saved, on purpose: whether a world has had these is a fact about that save,
and a tick that survived a restore or a Start fresh would be a confident wrong answer. The audit's section 5 says the same
thing about itself.

## 9. Found in passing, written down, not acted on

1. **A `docker stop` does not save.** ModernUO's shutdown path (`ModernUO-pinned/Projects/Server/Main.cs:333-348`,
   `HandleClosed`) waits for a write already in progress and saves nothing; the two `EventSink.Shutdown` handlers in pinned
   (`Misc/Broadcasts.cs:8`, which broadcasts "The server has shut down.", and `AdvancedSearchGump.cs:38`, which stops its search threads) do not save either, and nothing in `server/customizations` or `server/patches` registers a shutdown or process-exit handler or calls `World.Save(`. **Every stop, restart, snapshot and restore loses up to
   five minutes of play.** Every such plan says so, and suggests `[save` first. The tool uses `-t 60` so a write in flight can
   finish; the longest world-snapshot write in the captured live log is 1.00 s, so the default 10 s would usually do.
2. **The test container has no `Backups` or `Archives` mount** (`docker-compose.test.yml`), but its log shows
   `Created backup at /var/lib/uo/modernuo/Backups/Automatic/...` every five minutes. Those land in the container's own layer
   and disappear on every `-Down`. Harmless for a throwaway, and the reason snapshots are the test shard's only backups.
3. **`Start-TestShard.ps1` seeds a fresh test save by copying `Accounts` and `SerializedTypes.db` out of the live `Saves`
   while live is running**, so a copy can coincide with a live autosave. The captured log shows the save itself takes
   0.01 s, so the window is small. Not changed; the console calls that script as it is.
4. **`sl-modernuo:rollback-live-20260927` exists** (created 2026-09-28 07:20), so D29's "capture the running image first" has
   happened per `notes/deploy-readiness.md:229`. **The compose half of D29 has not**: `build:` and no `image:` still, so the
   panel warns. I did not verify what the rollback image contains.
5. **Other work changed `D:\ShatteredLegacy` during this session**: `docker/uo/docker-compose.yml` gained
   `RESOLVER_ADDRESS` on `sl-ddns` (D23) at 11:21, plus wiki, website, player-package and `Engines/Craft` files. None of it is
   mine and I touched none of it. The D29 state was re-read after that edit and is unchanged.

## 10. What a reader should not trust

- **Section 6 in full.** The form was built, rendered and inspected, but not clicked.
- **The "what to do" advice for a drifted test shard** was verified once: compose recreated on an image change. That is
  compose behaviour, not ours, and could change with a compose version (this was 5.1.3).
- **The 15-minute log window** assumes the listener or the prompt appears within 15 minutes of the container starting.
  Measured on live, 192,047 items: the listener line came 11 s after the entrypoint started. A world that took longer to load would read NOT LISTENING while it loaded, and
  keep reading it after. `LogWindowMinutes` in `Get-ConsoleConfig` if that ever happens.
- **The live paths** (section 6 item 9).
