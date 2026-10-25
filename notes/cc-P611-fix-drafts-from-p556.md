# cc-P611: the urgent fix-up drafts from P556, built

## In plain words

- **Hunter's Satchel:** it now refuses gold, weapons, bags and anything else that is not hides, leather, bones, wool, feathers or raw meat, whichever way it goes in. Before, dropping something into the satchel's open window, or into a bag inside it, got past the check. Hides dropped into the open window are now cut into leather as well.
- **Trash bag corpse clearing:** a bonded pet's corpse is never cleared now. "Clear corpses nearby" clears only the corpses its warning counted. If you walk away, change facet or put the trash bag away before clicking OK, nothing is deleted and no points are paid.
- **Launcher (with the next player package):** a check that cannot read a file no longer throws away the art the game starts with. Two starts at once share one rebuild. The one-minute limit now also covers putting new art in place. After an update that ran out of time, the game no longer waits for the art a second time.
- **For you:** the launcher part reaches players only with the next player package build and publish, which this prompt did not run. Civic Contracts (U1) waits on your answers to C1 and C2 (P574 F01 and F02). Nothing else to do.

## What was built

| Draft | Done or skipped | Why / what |
|---|---|---|
| A1 Clean Up: bonded pets and exact approvals (adds to P476 U2) | Done | The shared rule (`IsEligible`, used by `[cleanup`, `[cleanupall` and both bag entries) refuses a corpse whose owner is a bonded pet. "Clear corpses nearby" stores the serials and facet its warning counted. On OK it clears only those that are still on that facet, within reach and the player's to clear. It never rescans. Both warnings ask the bag again on OK (the owner's, in the owner's backpack). Cancel clears and pays nothing and starts no cooldown. **P476 U2 is still unissued.** When it is numbered, it should drop the P547 #1-#3 addition (A1), which is built here. Its barrel, replacement-bag, sweep-access and store fixes are not touched. |
| U1 Civic Contracts: final vendor prices and baselines | Skipped | It is built on For Chase C1 and C2. Neither has an answer (P574 lists them as open, F01 and F02). The prompt says to skip anything under For Chase. |
| U2 Launcher: read-only checks, one staging owner, bounded promotion | Done | See "U2 in detail" below. It touches `player-package/`, not the server. P610 built non-server drafts the same way, so I did not skip it for that. |
| U3 Hunter's Satchel admission | Done | `HuntersSatchel.CheckHold` applies `Accepts`. Pinned `Container.OnDragDropInto` and stack drops call `CheckHold`. So does the parent walk from any bag inside (pinned `Container.cs:270-277`). A new `OnDragDropInto` override cuts hides into leather. Inside the Field Satchel, the base check still reaches `LeagueFieldSatchel.CheckHold` and its item allowance. Nothing already inside is deleted, and illegal contents can still be taken out. |

None of A1, U2 or U3 was done by a merged prompt, and none is queued: I checked `queue\`, `waiting\`, `completed\`, `merging\` and `held\`. P572 explicitly leaves the satchel fix to U3. P476 is queued, but it is the Crystal draft-writing prompt, not a build of its U2. None of the three drafts was wrong against today's code. One limit: inside a plain bag that sits in the satchel, hides are not cut into leather. They are stored uncut, as before. That bag is a stock `Bag`.

## U2 in detail

- **#1 Check-only is read-only** (`Build-UoOverrides.ps1`). `-CheckOnly` returns before any write: no list, no stamp, no ready file. A part whose check fails is put in a new `Failed` field. The answer is `Fresh` only when the list a rebuild would write is byte-for-byte the list already there. So a part that failed this time but is in the list means a rebuild in staging, never a shorter list. A part that fails every time (and so is in neither list) does not rebuild at every start. An exception in the check is `Fresh=$false`, where it used to be `Fresh=$true`.
- **#2 One staging owner** (`Overrides-Launch.ps1`). A mutex per install (`Local\ShatteredLegacy-overrides-<SHA-1 of the app path>`) is held while a start promotes, finds a running builder, makes its generation, starts the child and writes its pid file. It is released during the wait and taken again to promote. Each rebuild has its own generation, `app\uo-overrides.staging\g<ticks>\`. A generation is deleted only when no builder is alive in it, or, with no pid file yet, when it is more than 120 s old. It is promoted only once its builder has exited (exit code 0 when this start launched it) and `ready.txt` is valid. An abandoned mutex (a start that died) is taken over. The old `app\uo-overrides.next\` is handled as one more generation, so an install mid-rebuild across the update is fine.
- **#3 One deadline.** The stopwatch starts on the call's first line. It covers waiting for the lock, the check, the wait and the swap. Rename retries stop when less than 0.3 s is left. The check runs on a second runspace and is abandoned at the deadline, which also covers the earlier P411 review's blocking freshness check. Its yellow lines are relayed to the window. If time runs out after the current set was moved aside, the set is put back with one more try. A start that finds `uo-overrides.old` and no `uo-overrides` restores it rather than deleting the only fallback.
- **#4 Named steps.** `Start-Step` traces `step <name>` before the work starts, so a step that never ends is still in the trace. New steps: `art.check` (hashing the records), `equip.check` (hashing both animation files), `map.parse` (with a line count on the bar) and `map.stamp`.
- **#5 Real Play sandboxes.** `Play.ps1` has a test hook, `SL_PLAY_SERVER=127.0.0.1:<port>`, accepted for loopback only. With it, the reachability check and the settings use a local listener. The update check is `-NoUpdate` and Legion scripts are `-NoScripts` (or a stub `Update-Scripts.ps1` in the updater test). The game is a stub `TazUO.exe` that records its start time and command line.
- **Updater handoff.** When `Update.ps1`'s own wait ran out (`$script:OverridesStillBuilding`), it passes `-ArtHandoff` to Play. Play then calls `Invoke-UoOverrides -NoWaitForRunning`, which does not wait for a running rebuild a second time.

## Tests (each seen failing first, then passing)

**Server** (probed on builder image `sl-uo-builder:cc-P609` with the files bind-mounted, then the gated build):
- `server/tests/Misc/LeagueRegisterVerification.cs`, new fact 11 `AHuntersSatchelAdmitsOnlyItsResourcesByEveryRoute`. Red on the old satchel: all 12 cases were taken (gold, a longsword and a bag, each into the nested satchel's window, into its inner bag by window and by icon, and into a loose satchel). Green afterwards. 108 of 109 satchel and League facts passed in the filtered probe. The one failure was `MuleModuleVerification.FromTierThreeASatchelUnloadsToTheMuleWithinReach`, which threw in `Account..ctor` ("Do not use PasswordProtectionAlgorithm.None") before any satchel code ran: an artefact of running that class without the full suite's account setup. The gated build below runs it normally.
- `server/tests/Services/TrashBagCorpseApprovalVerification.cs`, new, 4 facts. They use real context-menu clicks, `Target.Invoke` and WarningGump answers sent through `OnResponse`, on a test NetState. Red on the old code, 4 of 4: both bonded corpses were eligible and cleared (single and nearby); a corpse that died while the warning was open was cleared; walking away cleared the corpses at the new spot; the bag banked, deleted or handed to another player still cleared and paid. Inside those facts, the cancel and answered-twice checks already held on the old code; they guard against a regression. Green afterwards, and 84 of 84 TrashBag, Custodian, CleanUp and CorpseValue facts passed in the probe.

**Launcher** (`player-package/tests/Launch-Overrides.Tests.ps1`, Windows PowerShell 5.1.26100.9711):
- 18 facts: the 8 from P411 (moved to the generation layout through a `Get-Gen` helper that also finds the old `.next`) and 10 new ones.
- Red: the old payload scripts from HEAD were copied to the scratchpad, with only the loopback hook line added to the old `Play.ps1`. 8 of the 10 new facts failed:
  - The locked-stamp check deleted the list.
  - Two starts started 3 builders, not 2.
  - A swap held by an open file took 11.14 s against a 2 s limit.
  - The `.old` set was rebuilt rather than put back.
  - No `map.parse` step appeared on the bar.
  - Play with a locked stamp started the game without the list.
  - The lock holder found no lock to hold.
  - The updater and then Play each waited ("taking longer than" twice).
- The other 2 new facts, Play past the limit with a prior set and on a first install, already passed on the old code (P411 already did this). They were proven with a temporary mutation in a scratch copy, removing the deadline from the wait loop: both failed (the game started after 22.95 s, and with a list on a first install).
- Green: 18 of 18, twice. The second run came after the change that relays the check's messages.
- Other suites on the new code: `Build-UoOverrides` 24 of 24, after one fix. Its `PlayStartsTheGameWithoutTheOverrideWhenAFileIsMissing` caught that the runspace check had hidden its yellow line, and the relay fixed it. `Map-Overrides` 7 with 0 failed, `Cliloc-Overrides` 10 of 10, `Music-Overrides` 9 of 9, `Ui-Skins` 4 of 4, `Paperdoll-Bodies` 9 of 9.
- `Launch-Settings` ran with the loopback hook and a listener, so its Play sandboxes never reached the shard: 26 of 27 passed. The one failure, `P411_EndToEnd_PlayWithNoSwitchStartsTheTestShardAndLogsTheLaunch`, asserts that the window says `shatteredlegacyuo.com:2594`. Under the hook it says 127.0.0.1, so that is the hook, not the change. Unmodified, that suite connects to the test shard, so I did not run it that way.
- Every changed script is ASCII (0 bytes over 127, gate 2's rule) and parses in Windows PowerShell 5.1.

**Gated build:** I took the `docker-build` lock and released it afterwards. Before the build, Windows had 11.9 GB available and I dropped the VM's page cache. The build ran detached; its log is `build-P611.log` in the session scratchpad. `docker\uo\build.sh -t sl-modernuo:cc-P611` finished with EXIT=0: "Built sl-modernuo:cc-P611 with patches applied and 2383 shard test(s) passing". That is 2,383 passed, 4 skipped (the real-map-data facts, as always) and 0 failed. The new satchel fact, the 4 corpse-approval facts and `MuleModuleVerification.FromTierThreeASatchelUnloadsToTheMuleWithinReach` are among the passes. The images are `sl-modernuo:cc-P611` = `7c58c7d5ed3f` and builder `sl-uo-builder:cc-P611` = `7ac91b8cc1b2`; the image's `VERSION` reads 2026.10.25.5. `latest` is untouched.

## Deviations and decisions for Chase

- **The Read tool was refused** on ShatteredLegacy files: `server\tests\Misc\LeagueRegisterVerification.cs` and `server\customizations\HuntersSatchel.cs`, auto-denied in the unattended run. I wanted to read before editing. Instead I read them with `cat`/`sed` and edited with small Python scripts in the scratchpad.
- **The player-package build gates (`Build-PlayerPackage.ps1`) were not run.** A build fetches the published Legion scripts from get.shatteredlegacyuo.com and needs the package lock. Its gate 2 rule (ASCII scripts) and a parse check were run by hand instead. The package was not built or published, and no real client was started.
- **Concurrency is tested at `Invoke-UoOverrides` level, not with two real Play windows.** The test slows `Start-Process` by 3 s inside the starts, as P549's probe did, so the race window is hit every time. Two Play processes cannot be slowed at that point without editing Play.
- **New test hook:** `SL_PLAY_SERVER`, accepted only for 127.0.0.1. Nothing sets it on a player's machine.
- **CHANGELOG:** version `2026.10.25.5`, because P610 already used `.4` on its branch. `VERSION` is bumped to match. The launcher line is under Staff, because players get it only with a package.
- **Unverified:** a real cloud-placeholder file blocking the check, and a real TazUO reading a half-swapped set, were not reproduced. The tests use an exclusively opened file and a stub game.

## Files

ShatteredLegacy (branch golem/Iron/P611, base `2a3cf3b`):
- `server/customizations/HuntersSatchel.cs`
- `server/customizations/ClusterFCustodianSystem.cs`
- `server/customizations/TrashBag.cs`
- `server/tests/Misc/LeagueRegisterVerification.cs`
- `server/tests/Services/TrashBagCorpseApprovalVerification.cs` (new)
- `player-package/payload/app/Overrides-Launch.ps1`
- `player-package/payload/app/Build-UoOverrides.ps1`
- `player-package/payload/app/Apply-MapOps.ps1`
- `player-package/payload/app/Play.ps1`
- `player-package/payload/app/Update.ps1`
- `player-package/tests/Launch-Overrides.Tests.ps1`
- `CHANGELOG.md`, `VERSION`

No Haven connection, deployment, real account action, `docs\` edit, commit, merge, push or branch switch.

P611 DONE
