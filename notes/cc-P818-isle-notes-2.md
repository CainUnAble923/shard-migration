# cc-P818: Wakening Isle notes, batch 2 (the League lodge's hidden door)

## In plain words

- **The League lodge's door now faces you.** It used to be in the lodge's north wall, which the game's camera never
  shows. It is now in the east wall, which you see as you come along the road.
- **The way in is easy to spot.** A tan brick walk runs from the road straight to the door, with a brazier burning on
  each side. The lodge's two signposts stand where the walk meets the road. The lesson window says the door is on the
  east side, the arrow points at the door until you are inside, and Elara calls "In here! The lodge door is on the east
  side, between the two fires." if you wander outside. She now faces the door.
- **Existing worlds update by themselves:** the old door is taken away, the signs move and Elara turns when the
  server starts.
- **For you:** the isle release diff is `notes\cc-P818-tools\p818-release-isle-20261028.diff` (version
  2026.11.07.4). The new door and walk are map changes, so players need the next player package to see them.

Iron Golem, 2026-11-07. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P818`. Release copy `D:\UO\golems\Iron\p818-isle`, a detached worktree at `56f98af` (the
`release/isle-20261028` tip), with the change staged. Nothing committed; `latest` was not moved and nothing was
published.

## 1. The isle League building hides its door

**Chosen: move the door to the east wall** (the prompt's first option). I did not turn the whole building or add only
signs and a path round to the old door.

- **Why not keep the north door:** the camera looks from the south-east, so a north door is always behind the roof. A
  path round to it would end at a door nobody can see.
- **Why not turn the whole building:** the lodge stands on a small point with sand and sea to its south and west.
  Turning it would move its footprint and every piece inside, and rebuilding that part of the isle re-rolls the
  planting around it.
- **Why the east wall fits:** it faces the road's east stretch (the road runs from the bank past the lodge's north-east
  corner, then on east to the stones), and three tiles of grass lie between that wall and the sand. It is the face a
  player sees while walking that stretch (`lodge-walk-mouth-before.jpg`: the east wall with its banners, and no door).
- **I also did the second option:** a lit doorway (two braziers), a walk from the road to the door, the signs at the
  walk's mouth north of the road, and the lesson window and Elara both saying which side the door is on. All of it
  points at the visible door.

What changed, piece by piece, is in `notes\cc-P818-review\placed.md`.

- **Map (the isle driver):**
  - `notes/cc-P662-tools/build_isle.py` `LODGE_DOOR` is now (6363, 2008), the east wall at 6787,4000.
  - `isle-sets.json` (interiors.lodge, text edits only, so the file keeps its layout): the inside brazier went, the
    candelabra moved off the east window's floor tile, a banner moved off the door, and two braziers and a 12-tile walk
    of sandstone bricks 0x0525-0x0528 were added. The bricks match the tan of the bank's apron, and as floor statics on
    the grass they change no land, so nothing on the isle is re-rolled.
  - The driver run on unchanged main first reproduced the shipped isle exactly: every L and S+ line, with only the
    fingerprint (B) lines different because it builds on the stock base.
  - The run with the change differs from that baseline by exactly 22 lines: 5 dropped, 17 added, no land.
    `splice818.py` put that body under the shipped file's own header and B lines.
  - Every driver gate passed: no doubled wall tiles, every inner corner dressed, lesson signs north of their path, all
    25 server spots fit, the leg to Elara 7 steps.
  - A second run wrote the same patch byte for byte.
  - `statics-placed.csv`, `land-summary.csv` (unchanged), `walk-report.json`, `build-report.json` and `plan-cells.json`
    are the driver's own records of this layout. `plan-cells.json` was rewritten because the walls moved.
  - `tools/tests/test_mapops.py`: 14 tests OK, run with `SL_SHARD_REPO` set to the code copy.
- **The door's art, read from the art (guide 11.2):** `notes\cc-P818-review\door-test.png` draws the candidates in a
  stock-shop wall run.
  - DarkWoodDoor NorthCW (closed 0x06B3) stands flush in a north-south wall. Open (0x06B4, offset 0,-1), it lies along
    the wall line on the tile to the north, as WestCCW does in the bank's east-west wall (guide 2.4).
  - SouthCCW swings out across the room. WestCCW stands edge-on in a north-south wall.
- **Server:**
  - `TutorialWorld`: `LodgeDoor` is 6787,4000 and `LodgeStop` 6789,4000.
  - `TutorialCorePlacement`:
    - `MakeLodgeDoor` and `LodgeDoorClosedId` hang the new door; each door is rehung by its own closed art.
    - `RemoveOldLodgeDoor` takes away the north door at `OldLodgeDoor`.
    - `MoveLodgeSign` moves the name sign; the lesson sign moves by the existing `MoveOldMarkers`.
    - `TurnElara` and `ElaraFacing`: Elara faces East.
    - `LodgeFloor` and `InLodge` tell when the trainee is inside.
    - `LodgeWalkMouth` is the point the League sign stands near.
  - `TutorialCoreTrials`: the League hint names the east side. The arrow points at the door until the trainee is
    inside, then at Elara (as the bank's does). `CallFromLodge` has Elara tell a trainee outside, within 12 tiles, where
    the door is, every 25 s.
  - `OldLodgeDoor` lives in `TutorialCorePlacement`, not `TutorialWorld`, because the driver keeps every `TutorialWorld`
    point clear of walls. The old spot now holds a wall.
- **On an existing world:** the proof shard ran a copy of the overnight bot world, which was seeded with the north
  door. The load seed reported "1 doors" (the east one hung, the old one taken away). The after shots show the signs
  moved and Elara inside.

## Proof

All in `notes\cc-P818-review\`. Shots are TazUO from the default camera on the private proof shard (port 2596): before
on main's image `sl-modernuo:cc-P802` with main's map, after on `sl-modernuo:cc-P818` with this map.

- **Mockup:** `lodge-mockup.png` (the isorender with the server's door and signs drawn in), made from the driver's plan
  before the server build and the shots. Also `lodge-before-isorender.png` / `lodge-after-isorender.png`, the cutaways
  `lodge-before-cutaway.png` / `lodge-after-cutaway.png` (roof off), and `lodge-area-before-isorender.png`.
- **`lodge-road-west-before/after.jpg`:** coming from the bank. Before, only the roof shows. After, the end of the brick
  walk shows by the road's bend.
- **`lodge-walk-mouth-before/after.jpg`:** on the road at the walk's mouth.
  - Before: the east wall with its banners and no door.
  - After: the walk, the two braziers and the door at its end, and the two signposts north of the road.
- **`lodge-old-door-before/after.jpg`:** at the old north door's spot.
- **`lodge-door-step-before/after.jpg`:** at the walk's foot. After: the door between the fires.
- **`lodge-inside-after.jpg`:** inside: Elara behind the tables, the east door, the candelabra beside it.
- **`walk-lodge.log`:** a real character walked in TazUO from the road (6789,3988) down the walk, through the door
  (TazUO opens it) to 6784,4000, then back out and up to the road. Every step was at Z 0, with "ALL LEGS WALKED".
- **Not in the shots:** a shot of the lesson window and of Elara's call. `[Tutorial station` is a targeted GameMaster
  command the shot driver can't use. Facts 5 and 6 cover the hint, the arrow and the call.

## Tests and builds

- **New facts:** `server/tests/Tutorial/TutorialLodgeDoorVerification.cs`, 6 `P818_` facts:
  1. The door is in the east wall and folds along it.
  2. An old north door is taken away and the east door hung, once.
  3. The signs stand north of the road at the walk, and an old sign moves.
  4. Elara faces the door, and an old Elara is turned.
  5. The hint names the east side, and the arrow points at the door, then at Elara, then back at the door.
  6. Elara calls to a trainee outside, not to one inside or far off.
- **Changed facts:**
  - `TutorialIsleWalkFixes2Verification.TheBankAndLodgeDoorsFoldIntoTheWallAndAnOldDoorIsRehung`: the lodge's door now
    folds north.
  - `EveryLessonIsMarkedByANamedSignpostBesideItsStop`: the League sign is checked against the walk's mouth, as the
    travel sign is against the dock road's end.
  - `TutorialIsleReviewFixesVerification.TheLodgeHasANameSignBesideItsDoorOnce`: the sign is checked against the walk.
- **Red, then green** (`notes/cc-P818-tools/run-facts.sh` on main's builder `sl-uo-builder:cc-P802`):
  - **Red** (`red.log`): the new code with each fix switched off by one sed (mutants M1-M7: door and stop back north,
    door hung WestCCW, no upgrade pass, signs back, Elara north, the old hint and arrow, no call). All 6 P818 facts
    failed.
  - **Green** (`green.log`): 28 of 28 across the new file and the four suites around it.
- **Gated build of main:** `docker/uo/build.sh -t sl-modernuo:cc-P818` was **green**, 3,299 shard tests, EXIT=0
  (`notes/cc-P818-tools/green-gated-build.txt`).
- **Isle release:** `notes/cc-P818-tools/p818-release-isle-20261028.diff`, applied to the release tip `56f98af`. The
  code applied cleanly. The one conflict was `SOURCE.txt` (the release has its own map history there), resolved by
  adding only the cc-P818 entry. The release's `trammel.mapops` took the same 22 line changes by content
  (`patch_lines818.py`; its lodge lines were identical to main's). Gated build `sl-modernuo:cc-p818-isle`:
  **green**, 2,977 shard tests, EXIT=0 (`green-gated-build-isle.txt`). The saved diff matches the staged release copy
  (same md5).
- **Version:** `CHANGELOG.md` 2026.11.07.10 with the player line and `VERSION` 2026.11.07.10 (main had 2026.11.07.9
  from P802). The release diff carries 2026.11.07.4.

## Deviations and decisions for Chase

- **Release numbering:** P817 is not merged; its fix-up P823 is waiting for review. So this applies on the release tip
  `56f98af` alone, as 2026.11.07.4, after P817's .2 and P802's .3, which are not on the release yet either.
  - If P817 lands first, the overlap is small: both touch `TutorialCorePlacement.cs`, `TutorialCoreTrials.cs`,
    `CHANGELOG.md`, `VERSION`, `trammel.mapops` and `SOURCE.txt`.
  - P817's map lines are the bank's (x 6758-6766) and P823's are the bank's and the lodge's west column (x 6758, 6778).
    This change is at x 6782-6789, so the map lines should not collide; the overseer should still check
    `TutorialCorePlacement.SeedOn`, where P817 also turns Merrin.
- **The grey squares on the lodge's west roof slope** still show in these shots. That is the old ceiling flaw P823
  fixes; it is not on this branch.
- **The road's dip toward the old north door:** the road still bends down near the lodge's north-east corner (it is
  land laid by the driver's road). Re-laying it would re-roll the isle's land and planting. The walk starts from that
  bend, so the bend now leads to the walk.
- **Shot package:** the shots used P817's built package client with this branch's `trammel.mapops` dropped in (copies
  in `D:\UO\golems\Iron\p818-pkg`). No package was built or published.

P818 DONE
