# cc-P848: fix-up of P838 (the New Haven jail) after its build review (P842) said FAIL

## In plain words

- **The housing lesson no longer sends players into the jail.** On the testers' New Haven (the isle release), the
  housing lesson's second stop and its signpost had ended up inside the new jail, right in front of a cell gate. The
  stop and its signpost now stand on the open lawn just outside the town wall, south of the jail and east of the south
  road. The lesson's words say how to get there.
- **The stray signpost in the jail hall is gone**, also from a world that already has it: it is removed by itself the
  next time the shard starts.
- **Main's New Haven is not affected.** Its housing stops were never near its jail. Main gets the jail itself (P801,
  P820 and P838, which were never merged) with this branch.
- **For you:** the overseer applies `notes\cc-P848-tools\p848-release-isle-20261028.diff` to the release branch, in
  place of P838's diff. Nothing to decide.

Iron Golem, 2026-11-08, on `golem/Iron/P848` in both copies, not committed.

The release copy is `D:\UO\golems\Iron\p848-isle`, a detached worktree at `8f6eb2e` (the tip of
`release/isle-20261028`, update 13, 2026.11.08.1) with the whole change staged. It is mine to remove after the merge.
Nothing went to the release branch and nothing was deployed. All play ran on the private proof shard,
127.0.0.1:2596, under the test-shard lock.

## Bringing P838 in

The prompt says to check out `golem/Iron/P838` and merge `main` into it. The hand-off says to stay on
`golem/Iron/P848`, and not to commit, merge or switch branches. P848 stood at main (`a2956ad` code, `5d1a17ba` docs),
so I ran `git merge --no-commit --no-ff golem/Iron/P838` in each copy. The end state is the same as P838 with main
merged in. Both copies hold an unfinished merge (MERGE_HEAD), so the Golem's commit records it as a merge of P838.
- Docs copy: merged cleanly.
- Code copy: two conflicts.
  - `VERSION`: main's `2026.11.08.2`, then bumped to **2026.11.08.3** for this branch.
  - `CHANGELOG.md`: P801/P820/P838's jail lines move to a new **2026.11.08.3** section, because the jail was never on
    main.
- **Last step, merging `main` again: not run, and safe to leave.** In the end, `origin/main` was 4 commits ahead in
  each copy (P223/P830, the play-test bot: `6638331` code, `3776dddd` docs).
  - A second merge cannot start while P838's merge is still uncommitted, and the hand-off says not to commit.
  - Those commits touch no file this branch changes: `tools/playtest-bot/`, `testing/`, `tools/progress.json` and
    their notes. Neither touches `CHANGELOG.md` or `VERSION`.
  - So the integrator's merge is clean.
- **Separate commits for the isle and main-only parts:** I do not commit (hand-off rule). The two parts are already
  apart: the main part is in the code copy, and the isle part is only the release diff, in the docs copy.

## The reviewer's item (P842)

**1. Housing stop 2 and its signpost stood inside the release jail: fixed, on the release branch only.**
- **Where they were.** P806 put stop 2 at 3474,2603 and its sign at 3474,2601, on a lawn. P801's jail (post 3469,2597
  to corner 3479,2605) was later built over that lawn. So the sign stood one tile in front of the middle cell's gate,
  and stop 2 was the jail lesson's own place.
- **How I chose the new spot.** I mapped the land, statics and walkable tiles round the jail
  (`before-housing-stop2.jpg`).
  - Inside the palisade, the only open ground is the jail's south yard, which is the approach to its door.
  - The grass between the cottage and the stone tower is a three-tile strip between two walls.
  - The lawn west of the south road is a slope (Z 13 to 35).
  - **The lawn east of the south road, south of the town wall, is flat at Z 10**, open, and has no trees.
- **Stop 2: 3482,2623, Z 10.** Its distances:
  - 7 rows south of the town wall and 17 south of the jail's south wall;
  - 7 tiles east of the road and 4 from the shore;
  - no tree within 10 (guide 5).
- **The sign 0xA854: 3481,2622.** It stands 1 tile north-west of the stop, north of the walk in from the road, on no
  map static (guide 6). Like every Haven signpost, it reads from the south.
- **The words.** Stop 1 now says "Next: follow the arrow to stop 2, the open lawn outside the town wall: south
  through the gate by the jail, then east off the road." The stop's label is "stop 2, the lawn outside the town wall".
  Stop 2's own lesson text did not change.
- **The sign table.** `HavenSignTileVerification.cs` was made again with `notes/cc-P814-tools/sign_statics.py` on the
  stock client copy. The new box is 3477,2618 to 3485,2626, with 7 statics in it and none on the sign's tile.
- **Older worlds.** `SeedHaven` already takes a named Haven piece away from any spot but its own (`StrayPieces`,
  within 30 tiles). The old sign is 21 tiles from the new one, so it goes on the next load, once.
  - Proven by a fact: `HavenHousingStopVerification.Stop2SignInTheJailHallIsTakenAwayOnLoadOnce`. A second seed takes
    nothing.
  - Proven on a real world: run B's `shard.log` reads `New Haven (cc-P743): placed 1 pieces (took away 1 from old
    spots)`.
- **Main is not touched.** Its stop 2 is 3704,2605 and its sign is 3704,2604, as the reviewer said.

**The facts (section 11 of `TutorialJailVerification`, in both copies):**
- `NoHavenPieceAndNoOtherLessonStopIsInsideTheJail` checks every fixed Haven piece and every other lesson's tour
  stops, place, arm spot, props and fixture. None may stand in the jail box or on its doorstep.
- `TheHousingLessonsSecondStopAndItsSignStandTogetherOutsideTheJail` checks that the sign is within 2 of the stop,
  never on it, and on its north side.
- Release only: `HavenHousingStopVerification` (the upgrade, and the new spot).

## Tests and builds

- **Red first.** I ran the new facts on the release builder (`sl-uo-builder:isle13-20261108`) with the old
  `NewHavenLessons.cs` and `TutorialTradeTrials.cs` (`red/release-stop-in-jail/`). **5 failed, 100 passed**
  (`red-isle.txt`): the two jail facts, the two housing-stop facts and the sign table.
- **Green.** Release **105 of 105** (`green-isle.txt`). Main on `sl-uo-builder:cc-P837`: **104 of 104**
  (`green-main.txt`).
- **Gated builds** (the docker\uo build script, through `both-builds.ps1`, under the docker-build lock):
  - **Main** `sl-modernuo:cc-p848`: **EXIT=0, 3346 passed, 6 skipped** (`gated-build.log`).
  - **Release** `sl-modernuo:cc-p848-isle` (update 13 plus the diff): **EXIT=0, 3047 passed, 5 skipped**
    (`gated-build-isle.log`).
- **The release diff.** `notes/cc-P848-tools/p848-release-isle-20261028.diff` (16 files, made against `8f6eb2e`)
  passes `git apply --cached --check` on `origin/release/isle-20261028`, which is still `8f6eb2e`. It **replaces
  P838's diff**, which no longer applies on update 13:
  - It brings P838's jail across. Five files needed the same hand merges as main: `TutorialTradeTrials.cs`,
    `TutorialWingTrials.cs`, `TutorialTradeTrialVerification.cs`, `CHANGELOG.md` and `VERSION`.
  - The old `reputation.wing` tour stays out, as on main.
  - It adds this fix.
  - Release changelog section **2026.11.08.2**: the jail lines plus "New Haven's housing lesson no longer sends you
    into the jail...". Release `VERSION` 2026.11.08.2.

## Proof in TazUO (`run848.ps1`)

- **Run A** used P838's release build `sl-modernuo:cc-P838-isle` on a fresh copy of the bot world. The trainee walked
  in at the real door, the walk log reads "BEFORE signposts at 3474,2601: 1", and the staff bot ran `[save`.
  - Run A's own shots (`shots-before\`) are covered by an achievement popup and the patch-notes window. So the
    before half of `hall-before-after-isle.jpg` is P838's own `shots-isle\2b-hall-window-closed.jpg`, which the
    reviewer cited.
- **Run B** used this build `sl-modernuo:cc-p848-isle` on **run A's saved world** (`-KeepWorld`). A fresh
  Player-account trainee took the housing lesson and walked on foot:
  - from Rook's square to stop 1;
  - down the garden west of the jail, through the yard and the town-wall gate, and east off the road to stop 2;
  - back in at the jail's door to the hall.
- **Result.** `walk-after.log`: **11 PASS, 0 FAIL**. The checks:
  - stop 1 reached, and its text names the lawn outside the town wall;
  - stop 2 reached ("You reached stop 2, the lawn outside the town wall"), and the window shows stop 2's lesson;
  - the signpost is at 3481,2622, and a click reads "Housing lesson, stop 2: where houses can be built";
  - inside the hall: no signpost at 3474,2601, and none anywhere in the jail.
- **Kit fixes on the way** (the failed runs' logs are in `run1-failed\`, `run2-after\`, `run3-after\`):
  - A switch does not pass through `powershell -File` as `-KeepWorld:$x`.
  - The new trainee's account had no active tutorial on the saved world, so the staff bot now runs `[Tutorial reset`
    and `enter` once the trainee is in its view.

## What is in `notes\cc-P848-review\`

- **`placed.md`:** the moved sign and stop, what an older release world loses, and P838's jail list again.
- **The isorenders** (`render848.py`): `before-housing-stop2.jpg` (the sign and stop 2 in the jail),
  `after-housing-stop2.jpg` and `after-housing-stop2-roofless.jpg`. They show the jail and the Haven signs drawn in,
  stops in red and the housing signs in blue.
- **`hall-before-after-isle.jpg`:** the jail hall, before and after.
- **`shots-after\`:** run B's walk. The new spot is clearest in `2b-stop2-sign-on-the-lawn.jpg`; the hall in
  `4-hall-no-signpost.jpg` and `4b-hall-by-the-cells.jpg`.
- **`shots-before\`:** run A (popups over the hall; see above).

## Files

- **Code copy:** P838's merge (P801, P820 and P838's jail), section 11 of `TutorialJailVerification.cs`, and
  `CHANGELOG.md`/`VERSION` 2026.11.08.3.
- **Release copy `D:\UO\golems\Iron\p848-isle`:**
  - P838's jail merged onto update 13;
  - `NewHavenLessons.cs` and `TutorialTradeTrials.cs` (the move);
  - `HavenSignTileVerification.cs` (regenerated);
  - `HavenHousingStopVerification.cs` (new);
  - `TutorialJailVerification.cs` section 11;
  - `CHANGELOG.md` and `VERSION`.
- **Docs copy:** P838's merge, `notes/cc-P848-tools/` (render, probes, the red mutant, build scripts and logs, the
  walk kit and logs, the release diff), `notes/cc-P848-review/` and this file.

P848 DONE
