# cc-P814: fix-up for P806 after its build review (P807) said FAIL

## In plain words

- **The first housing stop's sign in New Haven no longer stands through a park bench.** On the testers' version it now stands between the two benches by the statue, clear of both, and the stop moved with it. A world that already has the old sign swaps it by itself.
- **A new check caught a second sign.** On main, the stables sign stood under the barn's eave, so it moved one tile east. No fixed sign in New Haven can land on a map object again without a test failing.
- **The record is corrected,** and all the New Haven work from P799 and P806 now travels on this one branch.
- **For you:** the overseer applies `notes\cc-P814-tools\p814-release-isle-20261028.diff` to the release branch; it replaces P806's diff. Your open decisions from P799 and P806 still stand, and this adds none.

## State

Iron Golem, 2026-11-06, on `golem/Iron/P814` in both work copies, not committed by me. Release copy: `D:\UO\golems\Iron\p814-isle`, a detached worktree at `5816efe` (the release tip, which now includes P804) with the whole change staged; mine to remove after the merge. Nothing went to the release branch, nothing was deployed, and `latest` did not move. All play was on the private proof shard, 127.0.0.1:2596.

| Build | Image | Result |
|---|---|---|
| Main | `sl-modernuo:cc-p814`, version 2026.11.06.3 | **EXIT=0**, 3204 passed, 0 failed, 6 skipped, of 3210 (`gated-build.log`) |
| Isle release | `sl-modernuo:cc-p814-isle`, version 2026.11.06.4 | **EXIT=0**, 2971 passed, 0 failed, 5 skipped, of 2976 (`gated-build-isle.log`) |

**One earlier main run failed, not from this work.** `DeathHooksVerification.AKilledNonBondedPetPaysNoImbueKillEffect` threw "Cannot dynamically create an instance of type LavaSerpentCrust" inside `ClusterFImbueEffects.ButcherOn`, and the same build passed on the next run. `ButcherOn` seems to pick a type at random, and that type has no parameterless constructor, so it looks like a rare real bug and not just a test flake. I did not trace or fix it. The log is `gated-build-run1-deathhooks-flake.log`.

## Steps 1 and 5 were not done as written

The prompt says to check out `golem/Iron/P806` and merge `main`; the hand-off says to stay on `golem/Iron/P814` and not merge or switch. So I applied P806's whole change to the working tree of each copy, on top of main (`git diff main...golem/Iron/P806`, `git apply -3`). The Golem's commit carries it, and P806's own commit is not an ancestor of this branch. The docs copy has P799's and P806's notes the same way.

- Only `CHANGELOG.md` and `VERSION` conflicted; both sides are kept.
- Step 5: main did not move while I worked, in either copy, so there was nothing to bring in.
- `golem/Iron/P801` is pushed and not yet merged. Against this tree its diff conflicts only in `CHANGELOG.md` and `VERSION`. Its release diff was built on the older tip and on no P799, so its own notes on conflicts need rereading once this lands.
- "Keep isle and main-only parts in separate commits": I make no commits. The release change is only in the release copy and its diff. The main tree holds main's.

## The reviewer's list

**1. Stop 1's sign: done, at the reviewer's tiles.** Release only.

| | Was | Now |
|---|---|---|
| Sign 0xA854 | 3469,2589, on the stock bench 0x0B2C | **3471,2588,10** |
| Stop 1 | 3468,2591 | **3470,2590**, 2 tiles from the sign |

I read the map myself: the bench is at 3469,2589,10, and 3471,2588 and 3470,2590 hold no statics. "Across the street, south-west of here" still holds. A seeded world loses the old sign through `SeedHaven`'s existing stray rule (fact below).

**2. The record: done.** The `HavenPieces` comment names the old tile, why it left, and the bank dirt at 3469,2586. `RookFacing`'s doubled word is gone. `notes\cc-P814-review\placed.md` replaces P806's lines for these signs.

## Beyond the list

**The main stables sign moved, from 3608,2614 to 3609,2614.** The new fact failed on main: that tile holds a hay roof piece 0x26EC at Z 29, the barn's eave high above the sign. It was not a collision like the bench, but the rule reads "shares a tile". 3609,2614 has no statics, is still just north of the door path and off the door's approach line, and `NewHavenFixesVerification` is updated. I did not walk main's upgrade; a fact covers the swap.

## The new fact

The gate's test host loads no client files, so a fact there cannot read statics. `server/tests/Tutorial/HavenSignTileVerification.cs` holds a table of the map's own static tiles in a 9 by 9 box round each fixed sign, read by `notes\cc-P814-tools\sign_statics.py` from each branch's map, so the file differs between the branches. A sign moved outside its box fails `TheTableCoversEveryFixedSign` until the table is made again.

The limit: it is a snapshot. If the client map changes, the table needs making again. It covers `HavenPieces` signposts only, not the isle's lesson signs.

## Tests

Each fix put back in a throwaway container, on the final builder images (`notes\cc-P814-tools\red.txt`, 24 facts; the clean run passes all 24):

| Put back | Red |
|---|---|
| Release: stop 1 sign on the bench | `NoFixedSignSharesATileWithAStaticOfTheMap` |
| Release: old sign not taken away | `AStop1SignLeftAtItsOldSpotIsTakenAwayOnASeededWorld`, and P806's `ASeededPieceAtAnOldSpot...` |
| Release: stop 1 at its old tile, 3 from the sign | `TheHousingLessonHasThreeClearStopsWithSigns` |
| Main: stables sign under the eave | `NoFixedSignSharesATileWithAStaticOfTheMap`, and `TheMountainAndStableSignsStandOffTheRoad` |

P799's and P806's tests ran in both gated builds, and those filters are in the 24.

## In TazUO

A fresh Player-account character on each branch; a staff bot set it down and started the lesson. Logs: `notes\cc-P814-review\shots-isle\walk.txt` and `shots-main\walk.txt`, all PASS.

- **Release:** walked in from the street on foot. The lesson's stop 1 fired on arrival, the sign read "Housing lesson, stop 1: a small house", and the walk went past the sign and back.
- **Main:** the stables sign read "The stables: the sick-bay stall is inside, on the left".
- I looked at the shots. `stop1-sign-clear-of-both-benches.jpg` is a zoom of two of them, and the post stands clear between the benches. A townsperson happens to stand beside it there, which is a spawned NPC, not a piece of the build.
- Isorenders: `render-stop1-sign.jpg`, `render-main-stables-sign.jpg`.

**Not proved in a client:** the swap of an old sign on a world already seeded with it. The proof shards placed it fresh; the fact covers the swap, and the code is P806's stray rule, which P806 saw work on the release.

## Files

- **ShatteredLegacy:** P806's change, plus `CHANGELOG.md`, `VERSION`, `HavenSpots.cs`, `NewHavenLessons.cs`, `NewHavenFixesVerification.cs`, and `HavenSignTileVerification.cs` (new).
- **Release copy:** the same, on its own coordinates, in `p814-release-isle-20261028.diff`.
- **shard-migration:** P799's and P806's notes, this file, `notes\cc-P814-tools\`, `notes\cc-P814-review\`.

P814 DONE
