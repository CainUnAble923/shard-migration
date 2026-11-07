# cc-P806: fix-up for P799 after its build review (P805) said FAIL

## In plain words

- **Rook's bench in New Haven is now one proper bench,** and on the testers' version Rook faces the yard and the square, not the Inn's wall. A world that already had the old bench swaps it by itself.
- **The theater music lesson now works where you can see it.** Both blue figures stand on the open stage, and the whole lesson was played through in the real game for the first time: calm, start the fight, the fight ends by itself, then discord.
- **The signs moved to the north side of their roads:** stables, mine and housing stop 1. Housing stop 1 itself moved onto the street beside its sign. The stall's bucket moved too, because a wall hid it from the camera.
- **For you:** please look at one spot. The stables sign is at 3520,2568, north of the street with a clear view of it, but the top of a high bank has dirt just north of it, so it misses the "no road north of the sign" rule by the letter. The alternatives are on top of that bank, which I think reads worse. The mine sign now keeps your rule, but it is out of sight from the gate until you are a few tiles down the road. Tell me if you want either moved. Otherwise nothing to do: the overseer ships `notes\cc-P806-tools\p806-release-isle-20261028.diff` after the review.

## State

Iron Golem, 2026-11-05, on `golem/Iron/P806` in both work copies, not committed by me. Release copy: `D:\UO\golems\Iron\p799-isle`, the detached worktree at `e8d210c`, with P799's change staged and P806's on top.

| Build | Image | Result |
|---|---|---|
| Isle release | `sl-modernuo:cc-p806-isle` | **EXIT=0, 2895 tests passing** (`cc-P806-tools\gated-build-isle.txt`) |
| Main | `sl-modernuo:cc-P806`, version 2026.11.05.3 | **EXIT=0, 3128 tests passing** (`cc-P806-tools\gated-build-main.txt`) |

**The release diff is new:** `notes\cc-P806-tools\p806-release-isle-20261028.diff` is the whole release change against `e8d210c` and replaces P799's `p799-release-isle-20261028.diff`.

**Step 1 was not done as written.** The prompt says to check out `golem/Iron/P799` and merge `main`; the hand-off says to stay on `golem/Iron/P806` and not merge or switch. `P806` was already at `main`, so I took P799's commit with `git cherry-pick --no-commit` in both repos. The end state is the same. The one conflict was `CHANGELOG.md`, because P795 had taken version 2026.11.05.2, so P799 and this fix-up are 2026.11.05.3.

## The reviewer's list

**1. Rook's bench: done.** 0x0B2D on both branches. `TakeAwayOldBench` removes the old 0x0B2C pieces at the bench's tiles, so a seeded world swaps them instead of keeping them underneath. `HavenSpots.cs` and `placed.md` are corrected. Fact: `ASeededWorldGetsTheJoinedBenchAndRookTurnsToTheSquare`.

**2. Rook's facing: done.** New `HavenSpots.RookFacing`: South on the release, used in `MoveRook` and on the `rookMissing` line. New `TurnRook` turns a Rook already on the bench, which `FindOldRook` skips. `AnOlderWorldsRookMovesToHisBenchByTheTavern` pins the literal direction. **Main stays North, on purpose:** a stone wall stands at y 2639 south of him, and the moongate exit and the square are north.

**3. Bard echoes: done, at the reviewer's tiles.** 3412,2604,60 and 3413,2603,60. Both are in view with the gump closed (`3-theater-both-echoes-gump-closed.jpg`). The lesson was played in the client, and the brawl is in `3-brawl-*.jpg`.

**4. Stables sign: moved, with a deviation for Chase.** 3520,2568,7, clear of the stock shop sign. See "Decisions for Chase".

**5. Mine sign: done, the reviewer's first way.** 3469,2624,14, 0xA854, north of the road running west at y 2627. Walked both ways. **It cannot be seen from the gate mouth** (`5-mine-sign-from-the-gate.jpg` does not show it): it comes into view only a few tiles down the road. See "Decisions for Chase".

**6. Housing stop 1: done, the stop and sign moved together.** The sign is at 3469,2589,10 and the stop at 3468,2591. The reviewer's check tested only grass; this tile is forest floor, which is why it found only the bank tile. It meets the rule: street level, road 2 tiles south, none north or beside. It stands in the flower bed by the statue. The stop's text now says the cottage is "across the street, south-west of here", and the next stop's text and two lesson names that still said "field south of the cottage" are corrected. The `HavenPieces` comment is rewritten and names the one blemish.

**7. Proof: done.**

- After renders: `renders\after-*.jpg` for the bench (both branches), the signs, the stage's two tiles (A and B) and the stall.
- Each of the four signs single-clicked, with its name over it: `4-stables-sign-read`, `5-mine-sign-read`, `6-stop1-sign-read`, `6-stop2-sign-read`.
- Walk logs saved as `.txt`: `shots-isle\walk.txt`, `shots-main\walk.txt`.
- **The bucket: I disagree with the review here, and moved it.** The review said the tile was right and asked for a shot from inside. No shot can show it: at 3535,2575 it sits behind the stall's east wall (x 3536) from the default camera. Two client shots from inside the stall failed to show it. It now stands at 3534,2574,8 on the straw, and shows in `7-bucket-from-the-stall.jpg`, just right of the character (water visible). Fact: `TheStallsBucketStandsWhereTheCameraSeesIt`.

## In TazUO

Real client, a fresh character on the Player account, on the private shard, 127.0.0.1:2596. The release's world was first seeded and saved by **P799's image**, so this is the upgrade: the log reads `placed 6 pieces (took away 6 from old spots), moved 1 Rook`, and the server then holds Rook as `Direction = South`. No exceptions in the decoded shard log.

- **Bard lesson:** "Finished" on all three steps, the fight started and stopped by itself, and "Lesson finished: Music and bard skills".
- **`walk.txt` has one false FAIL:** "FAIL Peacemaking on an echo". My script looked for different words from the game's. Line 55 of the same log has "Finished: Peacemaking: use on a blue training echo (1 of 3)", and the game's line "You play hypnotic music, calming your target".
- **Two earlier runs failed through my rig, not the shard.** One blessed the character, and pinned refuses a blessed mobile any harmful act, so every bard skill said "You cannot calm that!". Real trainees are not blessed. Those runs are not kept.
- **Main:** two 0x0B2D pieces, no 0x0B2C, Rook on the bench.

## Tests

- **Watched red** on the release's builder image, `cc-P806-tools\mutant-logs\`, 8 mutants, each a fix put back: old bench stays, Rook not turned, crosswise piece, Rook faces north, echo under the canopy, bucket behind the wall, mine sign at its old spot, stop 1 at its old spot.
- **`m4` first stayed green,** a real gap: the facts compared with `RookFacing` itself. The fact now pins the direction, and `m4b` is red. The mutants ran on the release only.

## Not proved

- **Main's upgrade in a client.** The bot world had no New Haven pieces yet (`placed 9 pieces (took away 0`), so main shows the new bench, not the swap. The fact covers it, and the code is the same as the release's.
- **Rook's count on main.** `[global get Direction` read `North (2)` there, so that world seems to hold a second Rook, perhaps out of `FindOldRook`'s range. I did not trace it. It was not on the release run, and nothing here adds one. Worth a look before main's next bot run.
- **The moongate setting a trainee down at the bench.** Still not played; P799 said the same.

## Decisions for Chase

- **Stables sign.** 3520,2568 has road directly south and none beside it, but dirt 2 tiles north, at 3520,2566. That dirt is on top of a bank, Z 20 against the sign's Z 7, and cannot be reached from this street. The tiles that meet the rule to the letter are on the bank top, 3517-3519,2564-2565, Z 20, about 15 above the road, where the board would face that strip and not the street. I chose the street. Say if you want the bank.
- **Mine sign.** It keeps your rule, but a walker leaving the gate does not see it at first, and the walking route to the mine (about x 3488 there) passes up to 19 tiles east of it, at the edge of the screen. The arrow still leads the way. The other way the review offered is the road's west shoulder near the gate with 0xA855, which reads from the east: seen sooner, but not north of the road. Say if you want that.
- **P799's three decisions still stand:** main has no theater, Rook's bench is by the Inn on the release, and the stock mine is an open ravine. So does its question about a young ghost being moved to a spot on main's town.

## Deviations

- **The bucket moved,** though the review passed its tile (item 7).
- **`stock-sites.md` in `cc-P799-tools` is now out of date** for the signs, the bucket and stop 1. `placed.md` here is the current record.
- **P799's local `gated-build-isle.log` was overwritten** by a first P806 build, through a path of mine, and is gone. It was git-ignored and never on the branch; P799's notes keep its result.
- **The harness stopped one wait loop for low memory** while idle. The build it watched was detached and finished. I did not restart the loop; later waits were bounded foreground checks.
- **Other P806 tools** are in `notes\cc-P806-tools\`. The shard's proof container and server name still say P799, as those scripts were copied.


P806 DONE
