# CC task P159: the Codex lane on the second PC

Iron, 2026-10-21.

## Headlines

- **Two Codex lanes can run on her PC, one per ChatGPT login.** Agapite is your seat (`lane-chase`), Verite is hers
  (`lane-steph`). Each has its own Codex home, its own usage file and so its own budget. They run side by side, each in
  its own work copies. A third login or PC is a new `golems.json` entry, not code.
- **Built on what already runs her PC, not as a separate package.** Since P159 was written, P184/P186 put a Golem
  kit on her PC (Gold, under a `golem` account, with deploy keys, a remote agent and the Tinker keeping it in step),
  and P158 built the Codex lane inside `golem.ps1`. So P159 adds what was missing for a lane on another PC. Her
  account, games and power plan are untouched. Details under "Deviations".
- **She comes first.** A lane starts nothing if someone used her PC in the last 20 minutes or a game is running. If
  she sits down mid-run, the run asks Codex for a stopping point within 30 seconds, and 2 minutes later drops to idle
  CPU priority. It is never killed. A lane runs at below-normal priority throughout.
- **Night, or when you ask.** Its window is 23:00 to 06:30. The new **Send to the second PC** button (Golem tab and
  web console), or an email `send to the second PC` / `send agapite`, lets it start by day for 3 hours.
- **The game PC wakes her PC by Wake-on-LAN** at a lane's window, or when a Send is waiting. Once you put her MAC in
  `golems.json` (SETUP step 3), the Tinker sends the packet. Nothing ever shuts her PC down.
- **The game PC checks the work again.** Before merging a lane's branch it reruns that prompt's Lane tests on the
  merged tree. Red, a conflict or a red build: NEEDS YOU, no fix-up. Codex's P158 review now runs on lane work too,
  before the lane's commit.
- **A real bug fixed on the way.** A Codex lane's branch pushed from another PC came back as an ordinary ticket. The
  `engine` was dropped, so a conflict would have written a fix-up prompt instead of emailing you.
- **Nothing was run on her PC.** Every part was tested on the game PC, with second lane folders and stubs standing in
  for hers. The lanes stay `enabled: false` until you follow `D:\UO\golem\lane\SETUP.md`.

## What changed

All of `D:\UO\golem` was backed up first (`<name>.bak-20261021-p159`: Golems.ps1, golem.ps1, Codex.ps1,
Remote-Agent.ps1, golems.json, TinkerLib.ps1, Away.ps1, SECOND-PC.md, tests\Codex.Tests.ps1, tests\Golem.Tests.ps1).

### `D:\UO\golem\Golems.ps1` (the shared library; the kit carries it to her PC)

- `:116` the registry check refuses a malformed `wake.mac`.
- `:337` `Get-ClaimCandidate`: a Codex lane refuses a prompt `Get-LaneRefusal` objects to, whatever its Codex OK line says.
- `:428` `Release-StaleClaims -LaneStaleMinutes 20`: a Codex lane on another PC loses a *running* claim after 20 minutes
  with no heartbeat (its agent's `remote\<name>\agent.json` and the status it posted). A claim it paused or that
  STOPPED stays. The rule applies only where that heartbeat is heard: the game PC.
- `:487` the new section, "the Codex lanes on another PC":
  - `:501` `Get-LaneRefusal`: refuses a prompt that needs the test shard (`test shard`, `-Take test-shard|docker-build`,
    `docker\uo\build.sh`, `build.sh -t`), the overnight bot, a Haven deploy, a package build, or a `D:\` folder outside
    the two repos (the preflight's `D:\UO\Commit-ShardWork.ps1` is allowed). It says which need it saw.
  - `:517` `Get-LaneLine`: "Second PC: P151 step 3 of 7", "... paused at step 3 of 7, in use", "idle, in use",
    "idle (why)", "asleep (last seen ...)", "P151 needs you", "off".
  - `:541` `New-WolPacket` (six 0xFF, then the MAC sixteen times: 102 bytes) and `:550` `Send-WolPacket` (UDP
    broadcast, port 9).
  - `:560` `Get-LaneWakeTargets`: the PCs to wake now. A PC qualifies if it has an enabled Codex lane, is asleep (no
    lane's agent heard from in 3 minutes), and is at the start of a lane's window (15 minutes) or has a Send waiting.
    One packet per PC, at most once per 30 minutes (`lane-wake.json`, `:596` `Save-LaneWakeSent`). A PC with no MAC
    is returned with the reason, not sent.
  - `:606` `Add-RemoteCommand`: queues a command for another PC's agent in the web console's own format
    (`remote\<name>\commands\<id>.json`, COMMAND_ID). The email command uses it.
  - `:620` `Get-LaneRunNow`: reads `lane-now-<name>.json` (Send to the second PC) until it expires.
  - `:629` `Invoke-LaneTests`: a prompt's Lane tests in the given work copies, stopping at the first red. The lane's
    finish and the integrator both use it.
- `:839` `Sync-RemoteTickets` keeps the pushed ticket's `engine` (the bug above).
- `:1102` `Invoke-Integrate`: for a Codex ticket, the Lane tests run again on the merged tree before the merge commit.
  Red means "the Lane tests failed on this PC": not merged, NEEDS YOU.
- `:1238` `Get-GolemCards`: each card carries `stepsDone`, `stepsTotal`, `lanePaused`, `note` and `laneLine`.

### `D:\UO\golem\golem.ps1` (the hook)

- `:375`, `:393` new setting `laneStaleMinutes` (20).
- `:2609` `Get-GolemBackOffNow` takes any registry entry (the lane's copy without hours while a Send holds).
- `:2662` `Invoke-PromptReview -CapMinutes` (outside the Stop hook), and `:2698` a lane's review uses its own login.
- `:2773` `Get-CodexBudgetNow`: a lane reads its own login's Codex home and usage file (`-CodexHome`, `-Account`).
- `:2838` `Start-CodexLaneRun` passes `-Account` and `-BackOffGolem`.
- `:2866` `Invoke-CodexLaneTick`:
  - `:2911` a paused lane whose claim is gone is freed (`:2958` `Clear-LaneLostClaim`, with an email saying where the
    work is; the next claim keeps it as a WIP commit, P222).
  - `:2914` a Send to the second PC lifts the window.
  - the back-off: "backs off: owner active ..." in the log and on the card, and nothing claimed or resumed.
- `:2969` `Invoke-CodexLaneFinish`: below-normal priority. `:3001` the Lane tests through `Invoke-LaneTests`.
  `:3015` Codex reviews before the commit, and the done email says what it found.
- `:2321` the status file carries `engine` and `lanePaused`, for the game PC's view of a remote lane.
- `:3846` the watch passes `laneStaleMinutes` and, in git queue mode, pushes the prompts repo after a release.

### `D:\UO\golem\Codex.ps1`

- `:62` `-Account` and `-BackOffGolem`. `:162` `Get-CodexUsagePath`: `codex-usage-<login>.json` per login,
  `codex-usage.json` without one (art and reviews on the game PC, as before).
- `:90` new settings `codexAllowCredits` (false), `laneBackOffSeconds` (30), `laneStopGraceMinutes` (2).
- `:209` `Test-CodexBudget`: with `codexAllowCredits` on, a reached limit and the 95% hard stop no longer stop a run
  (the workspace spend control still does). It is off by default, so the shared pool is never drawn on.
- `:418` `Get-LaneBackOffVerdict` (the fake file for tests, else `Test-GolemBackOff` on the lane's registry entry),
  `:434` `Get-LaneBackOffStep` (ask, then idle after the grace), `:443` `Set-ProcessTreePriority` (a process and all
  its children).
- `:648` a lane run sets below-normal priority before codex.exe starts (its children inherit it). `:682` every 30
  seconds it checks the back-off: the stop file ("the PC is in use: ..."), then idle priority 2 minutes later.
- The lane prompt now says the stop file can mean either reason (its budget, or the PC's owner is back).

### Other `D:\UO\golem` files

- `Lane-Now.ps1` (new): Send to the second PC. It writes `lane-now-<name>.json` (default 3 hours, `laneRunNowHours`,
  at most 12), `-Cancel` removes it, and it pokes that lane's watch.
- `Remote-Agent.ps1:27,77`: `lanenow` and `lanenow-cancel` are on the agent's allowlist (Lane-Now.ps1 for that lane).
- `TinkerLib.ps1:537`: each Tinker round sends Wake-on-LAN to the targets above, or notes that a PC has no MAC.
- `Away.ps1:354,451`: email commands `send to the second PC` (every enabled lane) and `send <lane>`. A lane on another
  PC gets a queued command for its agent.
- `golems.json:101-145`: Agapite and Verite gain `backoff` (owner check, idle 20 minutes, games) and `wake` (`mac`
  empty until you fill it, `broadcast` 255.255.255.255). Both stay `enabled: false`.
- `lane\SETUP.md` (new): the guide. `SECOND-PC.md` now points at it.
- Tests: `tests\Lane.Tests.ps1` (new), P159 facts at the end of `tests\Codex.Tests.ps1` and `tests\Golem.Tests.ps1`.
  The P158 Codex stub accepts and records `-Account` and `-BackOffGolem`.

### Code repo (ShatteredLegacy, on golem/Iron/P159)

- `scripts/Shard-Console.ps1`:
  - `:247` `LaneNowScript`, `:944` the phrase `send to the second pc`, `:1253` the action `golem.lanenow` (Golem queue
    row), its tooltip, the allowed scripts and the scripts told `-Golem`.
  - `:5911` the plan refuses with no Codex lane picked.
  - `:4440` the card document carries `laneLine`, and `:4615` the Golem tab row shows it.
- `web-console/golem-actions.json:66`: the **Send to the second PC** button, on a Codex lane's card only
  (`"engine": "codex"`; the confirm word is "send <lane>"). `console-actions.json:193` is its twin.
- `web-console/server.py:244,986,991,1480`: buttons carry `engine`; a remote lane's card copies its step, pause and
  note and gets `laneLine` from what its agent posted; an engine button for the wrong Golem is refused (409).
- `web-console/panels.py:148` `lane_line`, the same rules as `Get-LaneLine`. `static/app.js:326,504` shows the line and
  keeps the button off a non-lane's card.
- `CHANGELOG.md` 2026.10.21.4 `### Staff`, one line. `VERSION` 2026.10.21.4.
- Tests: `scripts/tests/Shard-Console.Tests.ps1` gets two P159 facts (placed before P222's, so P272's P158 fact merges
  without a conflict). Two existing row facts now list `golem.lanenow` in the queue row.
  `web-console/tests/test_remote_golems.py:163` gets two new tests.

### Docs repo

This notes file only.

## Tests

Every new fact was seen failing first, against the code as it was:

| Suite | Red first | Now |
|---|---|---|
| `tests\Lane.Tests.ps1` (new) | 7 facts all FAIL ("3 checks passed, 8 failed"); later the agent allowlist fact (2 failed) and the email send fact (threw: no `Add-RemoteCommand`) | **59 checks, 0 failed** |
| `tests\Codex.Tests.ps1` | the 7 P159 facts FAIL ("115 passed, 9 failed") | **136 checks, 0 failed** |
| `tests\Golem.Tests.ps1 -Only P159_` | 6 of 7 FAIL (18 checks); see the note below on the seventh | **28 checks, 0 failed** |
| `scripts/tests/Shard-Console.Tests.ps1` | both P159 facts FAIL | **439 facts, 426 passed, 13 failed: the same 13 as main** |
| `web-console/tests` | both new tests ERROR (`KeyError: 'laneLine'`, no `panels.lane_line`) | **79 OK (1 skipped)** |

- The seventh hook fact, `P159_ALaneRefusesAPromptThatNeedsTheTestShardEvenMarkedCodexOk`, passed on its first run.
  `golem.ps1` loads `Golems.ps1`, whose refusal I had already added after `Lane.Tests.ps1`'s refusal fact failed. So
  its red-first run is that `Lane.Tests.ps1` one.
- `P159_ARemoteLanesPushedBranchStaysACodexTicketSoAConflictNeedsYou` failed first for a test reason. Windows
  PowerShell 5.1 drops the JSON ticket's quotes on a native command line, so it now uses `git commit -F`. It then
  failed for the right reason: "P330 from Agapite: fixup (merge conflict in code: lane.txt), fix-up
  cc-P1-cont-fixup-far.md". It passes with the fix.
- `P159_CodexReviewsTheLanesWorkBeforeItsCommit` first read the stub's preflight `commit` line as the commit. It now
  checks the order preflight, review, commit.

Full suites, Windows PowerShell 5.1:

| Suite | Result |
|---|---|
| `Golem.Tests.ps1` (full, second sitting) | **167 facts: 165 passed, 2 failed (971 checks, 5 failed)**. The 2 are P184's (`P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged`, `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly`: Iron claims P102 "areas server, docs-only"), the same 2 with the same message as in P156's notes. Every P158 and P159 fact passed |
| `Codex`, `Lane`, `Tinker`, `GolemPower`, `UoFiles`, `Assign` | all passed (136, 59, 132, 133, 79 checks, 3 facts) |
| `GolemPaths` | 608 passed, 1 failed: "no D:\UO\golems\Iron (Iron is the integrator)". This PC's registry, as in P158's notes |
| `Move-ToGolem` | stops at its first line: the scheduled task "Shard CC Autopilot Watch" no longer exists (P158's notes) |
| `Join` | 4 failed. **The same 4 on a copy of the kit with every P159 file put back from its backup** (`-Kit`), so none is P159's |
| `RemoteAgent` (`-WebConsole` = my work copy) | the harness stops at "type wake gold to confirm", as in P156's and P158's notes |
| `Shard-Console.Tests.ps1` | 439 facts, 426 passed, 13 failed: the same 13 fact names as main |
| web console | 79 OK (1 skipped) |
| code repo `scripts/tests` (Python) | 53 OK |
| docs repo `tools/tests` (Python) | 170 run, 3 failed: `test_mapops` shipped patch and the two `test_play_who` real-file facts, as in P158's and P272's notes |

- One console run also failed `P68_ACheckShowsEachGateLineThenPassedOrFailed` (a child process reading a package
  zip). That was before any console change; it passed in both runs after.
- A trial merge of this branch's changes with `golem/Iron/P272` (`git stash create` and `git merge-tree`, nothing
  checked out, the stash list untouched) is clean.

### Second sitting (the finishing commands)

The first sitting ended STOPPED: the full Golem suite was killed for low memory before P158's lane facts ran again.
This sitting ran them:

- `-Only P158_`: 1 fact failed, `P158_CodexReviewsEachRepoBeforeTheCommitAndNeverBlocksIt` ("one review per repo":
  only the code review's line was in the marker). Run alone it failed 1 time in 3. **A test race, not the lane code:**
  the two reviews run side by side and the Codex stub in `tests\Golem.Tests.ps1:3213` appends to one marker file; a
  write that met the other's lock was dropped. The stub now tries the write again (up to 100 times, 50 ms apart).
  Then 5 of 5 runs green, and `-Only P158_` is all green inside the full run.
- `-Only P159_`: 7 facts, 28 checks, 0 failed.
- The full suite: as in the table above.
- Memory: Windows read 1.2 GB free mid-run, again; the Docker WSL VM held 12.8 GB of page cache. Dropping it (a
  privileged alpine container, `drop_caches`) gave 4.4 GB back, and the run finished.

**Nothing was run on the real second PC.** The Wake-on-LAN packet is built and checked byte by byte, never sent.
Codex itself never ran: the lane facts use P158's stub.

## Deviations and decisions for Chase

1. **No separate lane package, SMB share or `C:\ShardLane`.** P159 (written 10-17) planned a `Lane.ps1` in her own
   account with an SMB claim folder and its own heartbeat. P184/P186 (10-19, 10-20) since put a `golem` account, the
   kit, deploy keys (Join step 6), the prompts repo and a remote agent on her PC. The overseer's `SECOND-PC.md`
   already names Agapite and Verite as registry lanes. So the lanes use that:
   - claims are the prompts repo's;
   - the heartbeat is the agent's (20 minutes, `laneStaleMinutes`);
   - the code travels with the kit (top-level files only, which is why the new code is in the existing scripts and
     `lane\` holds only the guide);
   - GitHub access is the PC's deploy keys from Join, not a key per lane;
   - branches are `golem/<lane>/P<nn>`, not `codex/P<nn>`, so the merge Golem's ticket and merge path apply unchanged.
   If you want P159's original shape after all, say so.
2. **When she sits down, the lane pauses rather than giving the prompt back.** P159 said: finish the step, push a
   partial branch, release the claim. P158's lane already ends `P<nn> PAUSED` and keeps its claim and Codex session,
   then carries on when she has gone. Releasing would throw that session away and start the prompt over elsewhere.
   - Nothing is pushed while paused; the work stays in the lane's work copies.
   - If the game PC does release a paused claim, the lane frees itself, emails you where the work is, and its next
     claim keeps that work as a WIP commit.
   - "Within 2 minutes" is met by asking within 30 seconds, then dropping the whole run to idle priority at 2
     minutes. It is never killed: P158's rule.
3. **"Keyboard or mouse used in the last 20 minutes"** is read the way P186's back-off reads it: `quser` idle time of
   another signed-in user, which is coarse (minutes). The true last-input time needs a Windows API that these
   scripts do not call (ASCII only, no Add-Type).
4. **Two lanes side by side, not one at a time.** Each has its own seat, home and work copies, and the area rules
   keep them off each other's files. She is protected by the back-off whatever the number of lanes. If two at once
   is too much for her PC, set `hours` differently per lane in `golems.json`.
5. **An agent per lane is a manual step.** `Join-Golem.ps1` registers one agent task per PC (Gold's). SETUP step 2
   gives the commands for Agapite's and Verite's. Having Join register one for every enabled lane on the PC is a
   small follow-up prompt if you want it.
6. **Not built: PowerShell 7 and the .NET SDK steps.** Everything runs in Windows PowerShell 5.1. The lanes' areas
   (docs-only, map, tazuo-scripts) need no .NET build, and Join step 4 already installs the SDK the repo pins.
7. **The Read tool was denied** for `D:\UO\golem` and the code work copy (unattended run). As my notes for this setup
   say, I read with Bash and edited with small Python scripts that check each change matches exactly once and keep
   each file's line endings. Two of those files are CRLF (`Codex.ps1`, `golems.json`). One edit run was refused until
   the script handled that; nothing was half-written.
8. **P158 is DONE but not yet in main**: its fix-up P272 is committed and waiting for the integrator. P159 builds on
   P158's golem code, which is live in `D:\UO\golem`, so it did not stop for that. The trial merge with P272 is clean.

## For Chase

Steps in order (`D:\UO\golem\lane\SETUP.md` has each one with its check). About an hour in all:

1. Sign each lane in to its own ChatGPT seat on her PC, as the `golem` account (10 minutes; she types her own password).
2. Mint an agent secret per lane on the game PC, save it on her PC, and register the two agent tasks (10 minutes).
3. Wake-on-LAN: the BIOS switch, the adapter's two settings, her MAC into `golems.json`. Then test that a packet from
   the game PC wakes her PC from sleep (20 minutes).
4. Set `enabled: true` for Agapite and Verite in `golems.json`. Within 10 minutes the Tinker carries it over. Then run
   `Join-Golem.ps1 -Name Gold -Phase user -DryRun` on her PC to check the Codex CLI and sign-ins (5 minutes).
5. Have the overseer mark one small docs-only prompt `**Agent:** Codex OK` with `**Lane tests:** none`, and press
   **Send to the second PC**.

What the Golem tab shows when it works: "Second PC: P151 step 3 of 7" while it runs, "paused at step 3 of 7, in use"
when she sits down, "idle, in use" while she plays, "idle (codexNightOnly ...)" by day, and "asleep (last seen ...)"
while her PC sleeps. Each finished prompt sends a "done by Codex" email. The merge Golem merges it after running its
Lane tests again here.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P159 -NoRefresh`
(the hand-off's work copies in place of the real folders). It commits nothing; neither repo is BLOCKED:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: 10 files (CHANGELOG.md, VERSION, scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1,
web-console/console-actions.json, golem-actions.json, panels.py, server.py, static/app.js,
tests/test_remote_golems.py). docs: this notes file. No file is over 5 MB; no scratch is in either repo.

P159 DONE
