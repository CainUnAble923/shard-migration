# cc-P873: build review of P869 (New Haven winter set, fix-up of P856)

## In plain words

- I checked the moved holiday pieces for New Haven: the Christmas train, the snow globe, the Santa bench and the
  snowman bench. The verdict is **PASS**. Every fault the last review found is fixed.
- On main, all four pieces now stand round the little garden with the pond, just south-east of the square. No tree
  stands near any of them, and every piece shows whole from the normal camera. On the testers' (release) town, the
  train now stands on open grass on the west hill. The harbour pieces look as before.
- Two small things you may notice on main. The Santa bench's east end stands right against a flower bed's wooden edge.
  The snow globe's front-left foot sits on the corner of a glowing rune paving square. Neither hides anything.
- Nothing for you to do. P869 can merge.

Reviewer: Iron Golem, fresh session, 2026-11-10. I only read P869's work; nothing in its files was changed.

## What was checked

- The guide: `notes/guides/building-and-decorating.md` in the docs copy, read in full (sections 1-11, including 2.6
  "Nothing stray", 3 Facing, 5 "Keep clear", 6, 8 Proof, and 10 What to use where).
- From `origin/golem/Iron/P869` (both copies fetched; the branch was not switched):
  - `notes/cc-P869-review/`: `placed.md` (784 parts); the renders `main-garden.jpg`, `main-old-park-empty.jpg`,
    `rel-harbour.jpg` and `rel-train.jpg`; the 8 TazUO shots in `shots/`; and the walk logs;
  - the notes `notes/cc-P869-cont-fixup-new-haven-winter-set.md`;
  - the code diff `main...origin/golem/Iron/P869` (`WinterSet/` 3 files, the seeder, `FestivalStore.cs`, the facts,
    `CHANGELOG.md`, `VERSION`). On main the layout rows are `ClusterFWinterSetLayout.cs` (4 rows, area `garden`).
- I looked at every image, and zoomed into the main globe, the Santa bench and the garden.
- Each piece's footprint, worked out from `placed.md`:
  - main: train 3650-3655 x 2585-2605; snowman bench 3640-3642 x 2596-2605; Santa bench 3619-3626 x 2596-2597;
    globe 3629-3634 x 2601-2606;
  - release: train 3434-3439 x 2604-2624 (z 43-81); snowman bench 3502-3504 x 2592-2601; Santa bench 3502-3509 x
    2589-2590 (z 16); globe 3516-3521 x 2589-2594.
- **My own check of the map, not P869's tool.** A scratch script (`near873.py`, `near873b.py`, using P678's
  `sosbase.py`) listed every non-floor map static within 3 tiles of each footprint and under it, on SoS Trammel for
  main and vanilla Trammel for release. It also listed the doors and pinned spawners within 4 tiles. I also read P678's
  winter rows near the garden from `ClusterFWinterDecorLayout.cs`.

| Guide item | Applies? | Result |
|---|---|---|
| Walls, corners, roofs, doors, windows, stairs | No buildings placed | n/a |
| Facing, wall-mounted items | Each design is placed whole "as made", with no part turned (`placed.md`). The designs are the same as P856's, which P865 passed. In the shots, the benches face the camera and the train runs along y on its rails. | ok |
| Signs | None placed; seasonal props need no sign | n/a |
| Shores, bridges, docks, heights | Release pieces stand on the existing pier and boardwalk. Every piece's walk passes: 16/16 PASS, one tile a step, z within 2 (`walk-main.txt`, `walk-release.txt`). The town walk is intact (`placed.md`). | ok |
| Keep clear of trees (5), visible from the camera (1.4, 6), P865 items 1-4 | No tree within 3 tiles of any piece in either town, by my own map read. The only foliage near any piece is juniper bushes 0x0CC8 (3634,2600 and 3639,2600) and campion flowers and snowdrops in the garden beds, all on the north or west side, behind the pieces from the camera. | ok |
| Other winter rows (P865 item 3) | The nearest P678 rows are sq-snowman (3624,2590), snow-1 (3630,2591) and post-6 bell (3646,2607); the closest is 4 tiles away (post-6, from the snowman bench). | ok |
| Doors and approaches (2.4) | No door within 4 tiles of any piece. Main train: the hanging sign and lantern post at 3658,2584-2585 are 3 tiles east, so the approach is clear. | ok |
| Shots show each piece whole (8, P865 item 5) | All 8 shots show the whole piece, both trains included. | ok |
| Finder rule (P865 item 5) | `keepclear.py` is used by `find856.py` and `rel/findrel.py`. It was shown failing on P856's old spots (all P865 items, plus main's train) and passing on the new ones. | ok |
| What to use where (10) | Stock art only; no pack fits better | ok |
| Old pieces left behind (2.6) | `main-old-park-empty.jpg` shows the park clear. P856 never merged, so no world holds the old rows. | ok |

## Notes that do not block the merge

1. **Main Santa bench, east end** (origin 3622,2596,0). The garden's flower bed edging is map wooden bench 0x0B2D at
   3626,2596 and 3627,2596, and 0x0B2C at 3625,2594-2595. The 3626,2596 piece lies inside the bench's outline, in the
   gap between its east lamp post (0x0B20 at 3625,2596) and its candy cane (0x9E1B at 3626,2597). In
   `shots/p869-main-santa-bench.jpg` the lamp post and candy cane hug the bed's corner. The bench reads whole and
   nothing covers it; it just looks a little cramped. P856's finder says it refuses "any standing static under a piece
   (a garden bench)", but it seems to check only the tiles the parts stand on (inferred from this case; I did not read the finder), so a static in a gap inside the outline gets
   through. A later finder could test the whole outline.
2. **Main snow globe, corners** (origin 3631,2603,0). Two map glowing runes 0x0E68 (3630,2605 and 3630,2606) lie under
   its south-west corner. They are flat floor marks of the brick path's corner squares. A rune glyph shows at the
   globe's front-left foot in `shots/p869-main-snow-globe.jpg`. Campion flowers 0x0C83 at 3634,2601 lie in its
   outline's north-east corner, where no part stands. Neither hides the globe.
3. **Undead spawns.** Pinned post-UOML zombie spawners stand at 3649,2591, 1 tile west of the main train, and at
   3625,2594, 2 tiles north of the Santa bench. The shots show zombies round both. These spawners were there before
   (P858 saw them too). The guide's "nothing within 4 of a spawn" line is in its foliage list and is about the isle's
   player spawn and wake spots, so I do not count it against this build. Whoever handles the SoS undead in the square
   should know the set stands there.

## Verdict

BUILD REVIEW P869: PASS

P873 DONE
