# CC task P373: finish the Codex Golems (Valorite on the tower, Verite ready on Steph's PC)

Iron, 2026-10-24 (03:00 to 04:45). Branch golem/Iron/P373 in both work copies. The Golem kit changes are in
`D:\UO\golem` itself (installed after their tests passed on a scratch copy), as for P158 and P159.

## In plain words

- When someone sits down at a PC where a Codex helper is working, the helper now gets 2 minutes to stop, and then
  it is stopped for certain. What it had done is saved on its own branch and the prompt goes back in the queue, so
  any Golem can finish it. You get a short "went back to the queue" note.
- **Send to the second PC** on the Shard Console's Golem tab now works for a Codex helper on another PC (it used to
  refuse); the web console's button already did.
- Valorite and Verite on the game PC: their cards no longer say OFF while they work, Run next and Find a stopping
  point work for them like for the Claude Golems, and a newly signed-in Codex login no longer refuses to start for
  lack of usage readings. Valorite has its own test-shard accounts now.
- **For you:** the Tinker on the game PC has been stuck since 23:47 last night on one connection to Silver's laptop,
  so Golem emails are waiting; ending that one process (number 75780) frees it ("For Chase" 3). Verite still runs on
  the game PC, as you chose on 10-21; moving it to Steph's PC needs her for a 2-minute sign-in (steps in "For Chase").

## What the prompt asked, and what changed since it was written

The prompt was written 10-21 at 14:25. Within 25 minutes you changed the plan (overseer decisions 10-21 14:37 to 14:48):

- Valorite was enabled on the game PC at 14:37, after you saw P374 (item 6 says the overseer enables it after that:
  done before this prompt ran, so I left it on).
- Verite moved to the game PC too (14:34), Steph signed its Codex home in herself there (14:48), and it was enabled.
  It has run beside Valorite since, on her own seat. So items 8 to 10 ("prepare on Steph's PC, keep it off") now mean
  "get her PC ready for when Verite moves there". I did not turn Verite off: that is your live choice, and her usage
  is spent by your decision of 10-21.

| Item | Done |
|---|---|
| 1 Bounded stop | Yes: 2 minutes after asking, the whole Codex process tree is ended and each process checked gone. Tests. |
| 2 Publish partial work | Yes: WIP commit in both work copies, push, claim released, prompt back in the queue with where the work is. Tests. |
| 3 Remote send | Yes: the Shard Console's button now reaches a lane on another PC through its agent; the web console already did (its test passes). Tests. |
| 4 Valorite on the tower, no special casing | Yes: the status, Run next, Find a stopping point; the budget reads any home of the same login; a reset window counts as new. Tests. |
| 5 Valorite's test-accounts key | Yes: `test-accounts-valorite.key` on the game PC, `golem-accounts.json` rewritten (18 accounts). |
| 6 Do not enable it | Already enabled by the overseer on 10-21; left as is. |
| 7 SSH port | Nothing ever moved it: port 22 throughout. Details below. Docs say so. |
| 8 Verite's sign-in on Steph's PC | **Not started**, on purpose: see Deviations 1. |
| 9 Verite's work copies, hooks, key on her PC | Checked: work copies and key are there; hooks do not apply to a Codex lane; its agent and the Codex CLI are missing. Listed. |
| 10 Verite off; what turning it on would take | Left as you set it (on, on the game PC); the move list is in `D:\UO\golem\lane\SETUP.md` and below. |

## What changed

Backups of every file changed in `D:\UO\golem`: `<name>.bak-20261024-P373`.

### `D:\UO\golem\Codex.ps1` (items 1 and 4)

- `Get-LaneBackOffStep` now says `end`, not `idle`, once `laneStopGraceMinutes` (2) have passed since the ask.
- New `Get-ProcessTreeIds` (a process and everything under it, found from the root even after the root has ended),
  `Stop-LaneProcessTree` (ends them, looks again for a child started meanwhile, waits up to 15 s, returns ended / gone /
  left) and `Invoke-LaneBackOffCheck` (one look: ask, then end; it records `ownerBack`, `endedAt` and `ended` in the
  run's result).
- The lane run's loop uses it. The end comes on time (the next look is set to the ask plus the grace, not up to 30 s
  later), and the loop stops waiting for output 10 s after the tree ended, so a straggler holding the pipe cannot keep
  the run open. The result's `why` says how many processes ended and whether all are gone.
- The lane prompt tells Codex the run ends 2 minutes after a "PC is in use" stop file, and what happens to its work.
- Item 4's budget: new `Read-AccountRateLimits` gives the newest limits from the home's own session logs, any other home
  the new setting `codexAccountHomes` names for the same login, and the login's usage file (`Get-LimitsTime` orders
  them). Status, run, review and the usage refresh all use it. `Test-CodexBudget` counts the Golem's share of a window
  whose reset has passed as 0 (10-21 19:30: no session log after the reset, and the old window's 102% share refused
  both lanes).

### `D:\UO\golem\golem.ps1` (items 2 and 4)

- New `Publish-LanePartial`: a WIP commit ("WIP: P<nn> partial work by the Codex lane <name>, published when its PC's
  owner came back") in each work copy that has changes, a push of `golem/<lane>/P<nn>` where it has commits that
  origin/main lacks, the prompt back to `queue\` with a "## Partial work from the Codex lane" section (the branch, the
  commits, "git fetch / git merge origin/golem/<lane>/P<nn> first"), the claim file and token removed, the prompts repo
  pushed in git mode, the lane freed, and the routine email `lane-gave-back`. If the commit or push fails the claim
  stays (`publishPending` on the lane) and the next watch tries again, whatever the hours or the back-off.
- `Invoke-CodexLaneFinish`: a result with `ownerBack` and a PAUSED or no final line goes to `Publish-LanePartial`
  (an ended run logs its why first). A pause for the budget is unchanged (claim and session kept).
- `Write-Status`: a Codex lane is ON by its `golems.json` `enabled` (it has no `ENABLED-<name>` file); it showed OFF
  while running (overseer, 10-21 14:57).
- The lane's claim uses up its Run next pick (`RUN-NEXT-<name>`), as Hand-Off does. It was already honoured, never
  cleared.
- `-Event StopPoint` for a Codex lane writes its run's own stop file ("Chase asked for one") and sets `winding`
  stopping-point; the lane tick then holds the lane ("held at the stopping point you asked for in P<nn>") instead of
  carrying on at the next watch. `-Cancel` clears it (and the stop file, if no run is alive). Before, it wrote the
  CC Golems' STOP-REQUESTED, which no Codex run reads.

### Other `D:\UO\golem` files

- `GolemMail.ps1`: the routine mail `lane-gave-back` ("P<nn> went back to the queue": stopped because someone sat down
  at its PC, its work saved on its branch) and its sample.
- `Lane-Now.ps1` (item 3): a lane whose `golems.json` machine is another PC gets the command queued for that PC's agent
  (`lanenow` or `lanenow-cancel`, through `Add-RemoteCommand`, the web console's own format), and says where it went.
  That agent runs `Lane-Now.ps1` there, which then writes the file as before.
- `GolemPower.ps1`: `webwallpaper64` joins the all-day Steam tools that are not games (Wallpaper Engine on the game PC
  was read as a game on 10-21 21:10). One word in a list; no test of its own.
- `settings.json`: `codexAccountHomes` = `{ "lane-chase": [ "C:\\Users\\ckfle\\.codex" ] }` (your own Codex app's home,
  the same login: the overseer seeded lane-chase from it on 10-21). Read only, its session logs.
- `golem-accounts.json`, `test-accounts-valorite.key` (item 5), made with `GolemTestAccounts.ps1 -New -Golem Valorite`
  and `-Write`. The test shard seeds the accounts at its next start (`Start-TestShard.ps1` copies the file); not
  restarted by me.
- `README.md` (the Codex lane section) and `lane\SETUP.md` (where the lanes are now, port 22, the owner-back behaviour,
  the budget's other homes, and "Moving Verite to her PC").
- Tests: `tests\Codex.Tests.ps1`, `tests\Golem.Tests.ps1`, `tests\Lane.Tests.ps1`, `tests\fixtures\p157-mail-renders.txt`
  (regenerated with `-UpdateMailRenders`: the one new kind).

### Code repo (ShatteredLegacy, golem/Iron/P373)

- `scripts/Shard-Console.ps1` (item 3): `Get-GolemPickRows` rows carry `Remote` and `Engine`;
  `Get-GolemActionConfig` lets `golem.lanenow` through for an enabled Codex lane on another PC (that lane's scoped
  config and name; the plan runs `Lane-Now.ps1 -Golem <it>` here, which queues it for the agent). Every other button
  for another PC still refuses with "the web console queues its buttons". The refusal text names Valorite, Verite.
- `scripts/tests/Shard-Console.Tests.ps1`: `P373_SendToTheSecondPcReachesACodexLaneOnAnotherPc`.
- `CHANGELOG.md` 2026.10.24.1, four `### Staff` lines. `VERSION` 2026.10.24.1.
- The web console needed no change: `server.py` already queues a Codex-lane button for a remote lane's agent
  (`queue_remote`), and `test_a_codex_lanes_card_says_its_line_and_send_to_the_second_pc_reaches_its_agent` covers it.

## Item 7: the SSH port to Steph's PC

- SSH to `golem@stephs-desktop` works on port 22 today (03:45, `OpenSSH_for_Windows_9.5`, key `golem-remote`).
- Her `C:\ProgramData\ssh\sshd_config` was last written 2024-03-31; its `Port` line is commented out (the default, 22).
- No Golem script names a port for her PC: the Tinker (`TinkerLib.ps1` `Invoke-TinkerSsh`) and
  `GolemTestAccounts.ps1 -Deliver` both run ssh.exe with its default port, and no `~\.ssh\config` entry on the game PC
  names stephs-desktop.
- The only "443" for her PC is one line in the overseer's 10-21 passdown ("Gold's SSH runs over port 443"), which the
  overseer corrected at 14:25. The 443s in the records are GitHub over 443 on Copper's laptop (10-20 12:20, the
  Tinker's `ssh-443` fix) and the web console's Tailscale Serve port. So no change moved her SSH; the passdown mixed
  them up. The 10-20 21:08 "connection reset" (port 22) is the only failure on record, unexplained, and gone by 10-21
  14:25. I could not read her sshd's own log (the golem account may not).
- I did not edit the overseer's passdown (his file, and history); `lane\SETUP.md` now states port 22.

## Tests

Every new fact was seen failing first against the live kit (or, for the console, HEAD's Shard-Console.ps1), then
passing on the changed copy.

| Suite | Red first (before the change) | Now |
|---|---|---|
| `tests\Codex.Tests.ps1` | the 5 P373 facts and the changed P159 fact fail: "137 checks passed, 7 failed" | **161 checks, 0 failed** (copy, then live) |
| `tests\Golem.Tests.ps1 -Only P373_` | 4 facts fail: "1 passed, 17 failed" (the three owner-back facts), "5 passed, 5 failed" (status, Run next, stopping point) | **45 checks, 0 failed** |
| `tests\Lane.Tests.ps1` | the P373 fact fails: "59 passed, 5 failed" | **65 checks, 0 failed** (copy, then live) |
| `scripts/tests/Shard-Console.Tests.ps1`, P373 fact | with HEAD's Shard-Console.ps1: "1 facts, 0 passed, 1 failed" | passes |

The new facts:

- Codex: `P373_TwoMinutesAfterAskingTheRunsWholeProcessTreeIsEndedAndGone` (a real parent and child process: asked,
  not ended at 90 s, both gone at 2 minutes, the result says so), `P373_ATreeWhoseRootEndedFirstIsStillFoundAndEnded`,
  `P373_TheLanePromptSaysTheRunEndsTwoMinutesAfterThePcIsInUse`,
  `P373_ABrandNewHomeReadsItsLoginsLimitsFromAnotherHomeOfTheSameLogin`,
  `P373_AfterAWindowResetsTheGolemsRunsInTheOldOneNoLongerCount` (it failed with 10-21's very message: "the Golem has
  used 102% of the 5-hour window").
- Golem (the Codex stub gained `ownerback` and `ownerended` modes): `P373_OwnerBackAndCodexPausedThePartialWorkIsPushedAndThePromptGoesBack`,
  `P373_OwnerBackAndTheRunWasEndedThePartialWorkIsPushedAndThePromptGoesBack`,
  `P373_APushThatFailsKeepsTheClaimAndTheNextWatchTriesAgain` (each reads the pushed commit and files from the test
  world's bare origin), `P373_ALaneShowsOnAndTakesItsOwnRunNextAndStoppingPoint`.
- Lane: `P373_SendToTheSecondPcForALaneOnAnotherPcGoesThroughItsAgent`.
- Console: `P373_SendToTheSecondPcReachesACodexLaneOnAnotherPc`.
- Changed on purpose: P159's back-off fact (`end` for `idle`), P157's routine kinds (`lane-gave-back` added), the mail
  renders fixture (one new kind, nothing else moved).

Full suites:

| Suite | Result |
|---|---|
| `Golem.Tests.ps1` (full, on the copy) | 1595 checks passed, 7 failed, all in four P184 facts. Run again with `-Only P184_`: the copy and the live kit fail the same two (`P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged`, `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly`: 102 passed, 5 failed each), the two P159 and the overseer (10-22 09:08) recorded. The other two: `P184_LocksAreASignUpSheetAndStaleOnesExpire` threw because I passed the hook as a relative path, which its background job cannot find; `P184_ARaceForOnePromptGivesItToExactlyOneGolem` failed under load and passed in the rerun |
| `Codex`, `Lane`, `Tinker`, `GolemPower` | 161, 65, 157 and 133 checks, 0 failed |
| `Shard-Console.Tests.ps1` (full) | 451 facts, 437 passed, 14 failed. 13 fail the same with HEAD's console. The 14th, `P154_TheRefreshNeverRunsOnTheWindowsThread` ("the window could not answer: 858 ms"), ran while the full Golem suite loaded the PC; alone it passes twice on my version |
| web console (`python -P -m unittest discover -s tests`) | 114 tests OK (1 skipped) |

Live after the install: Valorite's real budget reads its own newest session log and refuses on the real 98% hard stop,
as before; a poke of its watch now writes `RUNNING`, `enabled: true` (it said OFF, false).

## Deviations and decisions for Chase

1. **Item 8, Verite's device-code sign-in on Steph's PC, was not started.** Three reasons, each enough:
   - Steph already signed Verite's Codex home in herself, on the game PC (10-21 14:48), and it runs there by your choice.
   - The golem account on her PC has no Codex CLI (only her own winget install, which the golem account cannot run),
     so `codex login --device-auth` cannot run there yet. Installing it would be the first unattended software
     install on her PC; I left it for you to say.
   - A device code expires in about 15 minutes, and you are away until Monday, so a code put in front of you now
     would be dead before Steph could type it.
   The command, ready for when she is at hand, is in "For Chase" and in `lane\SETUP.md`.
2. **Item 2 reverses P159's decision 2** (pause and keep the claim when she sits down), as the prompt asks. A pause for
   the budget still keeps the claim and the session: the prompt asks for publishing only on owner activity.
3. **No new test for `webwallpaper64`**: a one-word list change. The P159 fact
   `P159_WhenSheSitsDownMidRunTheRunAsksForAStoppingPointThenLowersItself` now expects `end` where it expected `idle`
   (its name kept; the change is the prompt's).
4. **The back-off is still off for both lanes on the game PC** (the overseer removed their `backoff` blocks 10-21 21:10
   for Wallpaper Engine). So items 1 and 2 act there only if you add a block back. They act on any lane with one, as
   Verite will have on her PC.
5. **`openai-usage.json` is not read for Codex limits.** The prompt offered it as a source. It holds the workspace's
   plan page (members, seats, credits) and has said "signed out" since 10-23 08:26; it has no Codex windows per login.
   The other homes of the same login are the source instead.
6. **Not built: the overseer's 10-21 note "replace Lane-Build.ps1 with a proper Golem step".** He retired Lane-Build at
   16:22 the same day (the integrator builds and tests every merge), so there is nothing left to replace.

## For Chase

1. Nothing needs doing now. Both lanes keep running on the game PC as before.
2. **When you want Verite on Steph's PC** (nights Gold is off), with Steph at hand for step b, about 20 minutes:
   a. As the golem account on her PC: install the Codex CLI for that account (`winget install --id OpenAI.Codex --scope user`), check `codex --version`.
   b. `$env:CODEX_HOME = 'D:\UO\golem\codex-home\lane-steph'; codex login --device-auth`; **Steph** opens the address it
      prints and types the code herself.
   c. Mint Verite's agent secret on the game PC and register its agent task on her PC (`lane\SETUP.md` step 2).
   d. Ask the overseer to move Verite's `golems.json` entry (machine, work copies, hours, back-off block, her MAC) while
      Verite is idle, and to have the night rotation turn Verite on exactly the nights Gold is off.
   The whole list, with what her PC has today, is "Moving Verite to her PC" in `D:\UO\golem\lane\SETUP.md`.
3. **The Tinker has been stuck since 23:47 last night** (see "Kit snapshot"): Golem emails wait until it moves. End
   process 75780 (`Stop-Process -Id 75780`, the hung ssh to Silver's laptop) or ask the overseer to.
4. If you want the 2-minute stop and the publish on the game PC too (for example while you game on it), say so and the
   overseer adds a `backoff` block (with `webwallpaper64` no longer a game, Wallpaper Engine will not trip it).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P373 -NoRefresh`:
both repos "dry run" (would add, commit and push), neither BLOCKED. Code: CHANGELOG.md, VERSION, scripts/Shard-Console.ps1,
scripts/tests/Shard-Console.Tests.ps1. Docs: this notes file. No file over 5 MB; no scratch in either repo.

## Kit snapshot

`New-KitSnapshot` (Kit.ps1, what the Tinker calls): kit **bcbbffe27bac**, 2026-10-24 04:36, 80 files, in `kit\current`.
The agents on the other PCs fetch it from the web console within 10 minutes. It carries the new `codexAccountHomes`
key to their settings.json (harmless there: no lane runs on them, and the path is the game PC's).

I took it directly because **the Tinker is stuck**: a round started 10-23 23:47 (process 17224) has waited since then
on one `ssh.exe` to Silver's laptop (process 75780, a cleanup `Remove-Item` of its `tinker-run` script). Its last log
line is 23:38. While it hangs, no Tinker round runs, so no kit resync from it, no fixes, and, since P410, **no Golem
email goes out** (the Tinker is the only sender). I was not allowed to end that ssh process (the auto mode classifier
refused it as interfering with a workload), so it is still there. Ending process 75780 lets the round finish; the
lasting fix is a time limit on the Tinker's ssh calls (`Invoke-TinkerSsh` has a connect timeout and keep-alives, but
no limit on a remote command that never returns). For the overseer.

P373 DONE
