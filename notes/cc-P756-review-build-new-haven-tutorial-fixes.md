# cc-P756: build review of P755 (fix-up of P743, New Haven tutorial fixes)

## In plain words

- I checked the three things P755 moved in New Haven against the building guide, using its pictures and its list.
- The mountain-path signpost, south of town, now stands on the grass just north of the dirt road. It was in the road.
  It now reads well from the road.
- The stables signpost now stands on the barn's porch by the hitching post, beside the barn door. It used to block the
  lane. The first housing stop is now right beside its signpost.
- Nothing for you to do. The review passed, so P743 and P755 can merge.

## What was reviewed

- **The guide:** `notes/guides/building-and-decorating.md`, read in full: sections 1 to 11, with the wall, stair and
  roof rules, the sign rules (section 6) and What to use where.
- **The work:** `origin/golem/Iron/P755`, fetched in both copies without switching branches.
  - Docs: `notes/cc-P755-review/`, with `placed.md`, `proof-log.txt`, 4 renders and 3 TazUO shots. I copied them to
    the scratchpad with `git archive` and looked at each one.
  - Notes: `notes/cc-P755-cont-fixup-new-haven-tutorial-fixes.md`.
  - Code: `git diff main...origin/golem/Iron/P755`, which is P743 plus the fix-up. P755's own change to P743 is
    `NewHavenLessons.cs`: two `HavenPieces` spots and `HousingStop(0)`.
  - `TutorialCorePlacement.cs` has the same seeding hooks as P743 (the Rook move and `SeedHaven`). P754 already reviewed
    them, and P755 did not change them.
- **P754's list:** P754's FAIL had one item, the mountain-path sign in the road. P755 also fixed the Codex review's two
  flags: the stables sign in the lane, and housing stop 1 four tiles from its sign.

## Checks, piece by piece

No walls, doors, stairs, roofs, wall-mounted items, shores, bridges, docks or foliage were placed or changed by P755.
The building items on the checklist do not apply. The pieces below are all stock signposts 0xA854 (a sign, not a rune
marker; section 6), plus one lesson stop.

1. **0xA854 "The mountain path: …", 3702,2742 (was 3702,2745).**
   - `render-mountain-sign.jpg`: the post's foot is on grass at the forest edge. The dirt band runs about 2 tiles south
     of it. There is no road north of it or beside it.
   - Nearest trees: 3696-3698, about 4 tiles off. A small fern stands at the edge but does not hide the board.
   - `mountain-path-sign-player.jpg` (the Tester on the road at 3703,2746): the post stands clear above the road's
     north edge, the board faces south toward the road, and the road is clear.
   - Passes section 6 (north of its path, facing it, off the road) and section 5 (keep clear).
   - P754's item 1 is fixed. The seeder's `StrayPieces` step takes away an old post at 3702,2745.
2. **0xA854 "The stables: …", 3608,2614 (was 3610,2613).**
   - Both renders: the post stands on the barn's porch strip (column 3608) between the map's hitching post at
     3608,2613 and the door path 3608-3609,2615-2616.
   - The door is in the barn's east wall (3607,2615-2616). The sign is beside the door's approach line, not on it, so
     the line stays clear for two tiles (section 2.4). It is out of the dirt lane.
   - The board (0xA854 reads from the south) faces the east-west walk into the door, and the sign is north of that
     walk.
   - The literal test (no road beside it) cannot hold anywhere on a north-south lane. P755 says so, and the porch strip
     is the reasonable fit. I accept it.
   - `stables-sign-player.jpg`: readable under the eave beside the hitching posts, the lane clear. With the roof on
     (`render-stable-sign-roofs.jpg`), the board stays visible below the eave.
3. **Housing stop 1, 3712,2593 (was 3709,2594). Its sign 0xA854 at 3713,2591 is unchanged.**
   - The stop is 1 tile west and 2 tiles south of the sign. That is within 2 and not on it (section 6).
   - The cottage door (3707,2591) is 5 tiles west, so the stop is off the door line.
   - The lamp post at 3711,2592 is diagonal to the stop, not on it.
   - `housing-stop1-player.jpg`: the Tester stands one tile south of the stop. The signpost is at the cottage's
     south-east corner beside him, the lamp post next to him, and nothing is blocked.
   - The sign still stands north of the dirt yard it marks.
4. **Unchanged pieces** (Rook's bench, the stall props, housing stop 2's sign, the old farm's removal) were not
   re-shot. They are as P754 reviewed and passed them in `notes/cc-P743-review/`.
5. **Proof:**
   - `placed.md` lists every piece with ID, location, facing and purpose.
   - The proof log shows the private shard on 2596, so not the shared shard (section 8).
   - The world load seeded the pieces at the new spots ("placed 0 pieces" on the re-run, so the seeding is
     idempotent).

No better piece from What to use where applies: 0xA854 is the guide's own choice for a standing sign on open ground.

BUILD REVIEW P755: PASS

## Files

- This file only. I did not edit the build's own files.

P756 DONE
