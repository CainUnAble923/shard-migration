# cc-P276: the tutorial farm (F-35): map patch, farmhouse, Farmhand and the evo pet picks

## In plain words

- **Current main does not start a shard.** It crashes at boot in ModernUO's virtual check code. This is not from this
  prompt: the build from this morning's main, without any farm code, crashes the same way. Yesterday's last good
  image still starts. The live shard would crash the same way on its next deploy from main, so hold deploys until
  this is fixed.
- The tutorial farm is built: the fenced field with crops and a pen, the thatched farmhouse with its porch onto the
  field, and Wren Tallow, the farmhand at the gate. With her, a trainee picks a dog or a cat to keep, clears the rats
  out of the crops with it, then patches up with her bandages.
- The client map update removes the two trees that stood inside the farm's fence. That reaches players with the next
  player package build.
- **Paused at Chase's request before the test-shard step.** The farm is not placed on the test world and there are
  no screenshots: the test shard would not start (first bullet). A continuation prompt, P372, holds the rest.

2026-10-21, the Silver Golem (Opus), branch golem/Silver/P276 of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Silver\cc-P276-tutorial-farm-build.md`. Chase approved the map patch for the two trees and
the recommended evo stages ("Sounds good"). Not committed (the Golem commits after the last line). Both repos were
clean at the start. Nothing deployed; no package built.

## Headlines

- **Part 1, the map patch: done and checked.** Built by the playbook's route (`notes/map-building-playbook.md`
  section 6) with `notes\cc-P276-tools\build_farm_map.py`:
  1. It applies the shipped patch to scratch copies of the pristine 7.0.117.0 Trammel files.
  2. It removes exactly the four statics: willow 0x0CE6 and leaves 0x0CE7 at 3388,2607 z19; walnut 0x0CE0 and
     leaves 0x0CE1 at 3396,2616 z38. It first checks that those tiles hold nothing else, and that they are the only
     impassable statics inside the fence.
  3. It diffs the patch again and runs `check`: drifted 0, missing 0, land identical, 0 blocks differing.

  The new `trammel.mapops` is the old one plus 6 lines: 2 block fingerprints and 4 `S-` lines; `F 1 211` becomes
  `F 1 213`. `SOURCE.txt` records it.
- **Part 2, the farm addon and seeder: done.**
  - `TutorialFarmAddon` holds all 330 pieces of the approved v3 layout at their exact tiles and Z.
    `TutorialFarmLayout.cs` is generated from `design\tutorial-farm\west_v3_layout.json` by
    `notes\cc-P276-tools\gen_farm_layout.py`.
  - The door is a real `DarkWoodDoor` (SouthCW, the layout's art 0x06AD) in the east wall.
  - Two spawners: the field's pests (3, range 3) and the pen's stock goat, sheep, cow and chicken (4, range 2).
  - `[ClusterFSeedTutorialFarm [dryrun | force]` places what is missing and is idempotent. It refuses on anything but
    the test shard (`ClusterFStaffHub.IsTestShard`; `clusterf.tutorialFarm.allowLive` lifts that), and refuses
    while the server's map still holds the trees, unless `force`.
  - **Not placed on the test world** (Continuation).
- **Part 3, the Farmhand: done.** Wren Tallow, "the League farmhand", stands at the gate (3400,2614). She runs the
  station `animals.taming` in three steps, F-35's order:
  1. Pick a dog or a cat (`EvoPet.GivePet`: bonded at once, the hue pick follows).
  2. Kill three pests (tutorial-only farm rats, field rats and grass snakes) that the player or the pet damaged.
     This completes `animals.taming`.
  3. Use her bandages: a successful Healing or Veterinary use completes `combat.healing`.

  An account that took its pet at the farm gets no second pet pick at graduation.
- **Part 4, the evo dog and cat: already in main as recommended** (P65's `EvoPetData`). A new fact pins all ten
  stage bodies to Chase's picks; P65's own facts pinned six.
- **Part 5, screenshots: not done** (Continuation). This PC has no TazUO build and no vanilla client data, so
  P219's screenshot harness cannot run here. The plan was the headless play-test bot (`uobot`, this Golem's
  `silver-admin` test account) to run the seeder and read back what the shard sends, then an `isorender` picture.
  The test shard would not start on current main.
- **Tests:** 5 new facts (`server\tests\Tutorial\TutorialFarmVerification.cs`), all seen red, then green. The full
  gate is green: 2,034 tests, 2,030 passed, 4 skipped, 0 failed. `test_mapops.py` fact 4 was seen red on the new
  patch, then updated.

## The site and the pieces

- Field fence x 3381-3399, y 2603-2619 (outside the guarded region, as F-35 recorded). The farmhouse is centred at
  3377,2611 with base Z 15; its walls are x 3374-3380, y 2608-2614, and its east porch replaces five fence tiles
  (x 3381, y 2609-2613).
- The gate is the east fence gap at x 3399, y 2614-2615, with the sign at 3401,2613. The pen is x 3393-3398,
  y 2604-2608, inside its own fence, with a gap on its west side.
- **The porch steps** were flagged in F-35 as a placeholder (0x0725 drew as a flat plank in the mockup). ModernUO's
  house-design table `Data/Components/stairs.txt` (Light Wood set) gives North 1826, **East 1829 = 0x0725**,
  South 1828, West 1827. So the mockup's piece is OSI's east stair, the one for steps descending east, and it stays.
  The flat look was the renderer. A fact pins it.
- Z values are the client land the mockup was drawn on. The farm's land is unpatched; the patch only removes the
  trees.

## Tests

`server\tests\Tutorial\TutorialFarmVerification.cs`:

| Fact | What it checks | Red (the break) |
|---|---|---|
| `TheSeederRefusesOnLiveAndUnpatchedAndPlacesTheFarmOnce` | refused off the test shard and with the trees; the dry run places nothing; the first run places the addon (330 components equal to the layout, tile for tile), the 0x06AD dark wood door, the Farmhand and both spawners (count, range, types); the second run places nothing | the live refusal removed: "Assert.True() Failure" |
| `TheLayoutIsTheApprovedFarmAndTheMapEditIsThePatchs` | 330 pieces inside the farm; the anchor; three porch steps, all 0x0725; no door piece; the four removed statics; no fence on the tree tiles | one step 0x0722: "Item: Tuple (1826, 3382, 2611, 17)" |
| `TheFarmhandRunsPetPestsAndHealing` | a stranger turned away; the pick (no fox; a dog, bonded and controlled; no second pet); an untouched pest does not count; three pests the pet damaged; bandages; a failed heal does not count, a Veterinary success does; the station handler | the pet key not saved: "Not found: farm.pet" |
| `GraduationOffersNoSecondPetAfterTheFarm` | no pick gump after the farm pet; the pick gump otherwise | the skip removed: "Assert.False() Failure" |
| `TheEvoDogAndCatStagesAreChasesPicks` | all ten stages' bodies, none art pending, the loop gates 0, 0, 0, 1, 5 | cat stage 2 1310: "Collections differ (pos 1)"; P65's two body facts also went red |

- The red run used `notes\cc-P276-tools\redbreak.py`: one build of the builder stage, the five breaks at once, and
  the focused filter (TutorialFarm, Tutorial, Evo, Rootdeep: 32 tests). All five went red, each on its own
  assertion.
- The code was then restored and checked byte for byte by SHA-256.
- Green focused run: 32 of 32.
- **Full gate:** `docker\uo\build.sh -t sl-modernuo:cc-P276`, twice:
  - Cycle 1 was green: 2,034 tests, 2,030 passed, 4 skipped.
  - Cycle 2 was the same, after moving the farm's registration from `Configure` to `Initialize`.
  - The image `26a65a3ec9c9` carries VERSION 2026.10.21.17.
  - The one edit after cycle 2 is a comment in `TutorialFarm.cs` (no code).
- The test host never runs `Configure` or `Initialize`, so the fact class calls `TutorialFarm.EnsureHooks()`. It
  was red before that: the heal hook was missing.
- `tools\tests\test_mapops.py` (docs repo):
  - Fact 4 now allows exactly the four farm removals, inside x 3381-3399, y 2603-2619.
  - Fact 5 compares P167's scratch build against the patch without them (`without_farm`): 211 blocks and 3 removals,
    as before.
  - Red on the new patch first: "(3388, 2607, '0xce6')". Then 5 tests OK, 1 skipped: fact 5 needs P167's scratch
    folder, which this PC lacks.
- `player-package\tests\Map-Overrides.Tests.ps1`: 7 of 7.
- **numpy and Pillow were not installed on this PC**, and the map tools need them; I installed both for the user
  (`pip install --user`).

## The test shard: current main does not start

The shard was up and healthy on `good-9ccce19` (2026.10.20.18). Under the test-shard lock:

1. `Start-TestShard.ps1 -Image sl-modernuo:cc-P276` failed at once. It rebuilds the map overlay before stopping the
   running container, and the container holds `map1LegacyMUL.uop` open. **`Start-TestShard.ps1` should stop the old
   container first;** `-Down`, then start, works around it.
2. On the P276 image the shard crashed at start:
   `NullReferenceException: GumpActivator at Server.Items.VirtualCheck.Configure() (VirtualCheck.cs:34)`.
   - Pinned's `VirtualCheck.Configure` throws when `virtualChecks.useEditGump` is on (the default at TOL) and
     `VirtualCheckGump.Configure` has not run yet.
   - `AssemblyHandler.Invoke` sorts every `Configure` by `CallPriority` with `List.Sort`, which is unstable. So
     the order of equal-priority `Configure` methods can change whenever the set of `Configure` methods changes.
   - That is my reading of the code; unverified.
3. **The control, `sl-modernuo:cc-P275`** (main as of this morning, no farm code), **crashes the same way.** So the
   cause is in main between `9ccce19` and this morning, not in P276. I first suspected my own `Configure` and moved
   it to `Initialize`; the crash stayed, and the control settled it.
4. The shard was stopped, then restarted on `good-9ccce19` (healthy) and left as I found it. Its overlay now carries
   the tree removal; no other change.

This crash would also hit the live shard on its next deploy from main. A likely small fix, unverified: our own
`Configure` with a low `CallPriority` that calls `VirtualCheckGump.Configure()` first, or a patch giving it one. It
is not built here: it is outside this prompt, and the pause came first.

## Deviations and decisions for Chase

1. **The farm pet moved from graduation to the farm** for dog and cat (F-35: "the player chooses a dog or a cat", given
   at the Farmhand's pen; P65 notes: "the Farmhand will call `EvoPet.GivePet(player, "dog" or "cat")`"). Graduation
   still offers the four-line pick (dog, cat, fox, bird) to anyone who did not take a farm pet. **P371 ("graduation is
   the first loop") is in the queue** and touches graduation; it should keep this skip.
2. **The pest count is in memory**: a restart in the middle of step 2 starts the count again. The step keys are saved.
3. **The farm is outside the guarded region** (as F-35 decided). Trainees are Young and the pests are tutorial-only.
   The stock wildlife spawner at 3403,2572 (range 30) still reaches the field's north edge. F-35 said to move or trim
   it; that is not done here.
4. **The seeder is test shard only** until Chase says the farm goes live (`clusterf.tutorialFarm.allowLive`).
5. The Farmhand's and the Echo's lines are placeholders for Chase's eye (`TutorialFarm` constants).

## Continuation

**Done:**
- Part 1: the map patch, checked, and the package and docs map tests updated.
- Parts 2 and 3: the addon, the door, the Farmhand, the pests, the steps and the seeder.
- Part 4: verified, with a fact.
- The tests (red, then green), the full gate, the CHANGELOG (2026.10.21.17) and VERSION.

**Left:**
- Part 5:
  1. Start the test shard on the P276 build once main starts again (the VirtualCheck crash above).
  2. Run `[ClusterFSeedTutorialFarm dryrun`, then `[ClusterFSeedTutorialFarm`, as `silver-admin`, through the
     play-test bot or in game.
  3. Walk the Farmhand's steps once on the shard.
  4. The screenshots, or an `isorender` picture from what the shard sends, on a PC without TazUO.
- One full gate after the comment edit.

**Mid-flight:** nothing. Both repos build; the code is the cycle-2 code plus one comment. The test shard is back on
`good-9ccce19` and healthy, and no lock is held.

Continuation prompt: `D:\UO\cc-prompts\queue\cc-P372-cont-tutorial-farm-test-shard.md`.

## Repo size

The largest new file is `TutorialFarmLayout.cs` (17,749 bytes); `trammel.mapops` went from 251,905 to 252,049 bytes.
Nothing near 5 MB. Scratch (the map copies, logs, the pinned source extract) is in the session scratchpad.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\ShatteredLegacy -DocsRepo D:\UO\shard-migration -Branch golem/Silver/P276`. Code: 8 files pending (CHANGELOG.md, VERSION,
the map patch and its SOURCE.txt, ClusterFTutorial.cs, the two new farm files, the new test). Docs: 5 (test_mapops.py,
this note and the three tools in `notes\cc-P276-tools\`). Neither is BLOCKED. The continuation prompt is outside both
repos, in `D:\UO\cc-prompts\queue\`.

```
Repo Result
---- ------
code dry run
docs dry run
```

P276 PAUSED
