# cc-P865: build review of P856 (New Haven winter set)

## In plain words

- I checked the new holiday pieces for New Haven: the Christmas train, the snow globe, the Santa bench and the snowman
  bench. The verdict is **FAIL**. The pieces are built fine, but four of them stand too close to trees, and one stands
  too close to an existing Christmas tree.
- What you would see: on main, a tree hides part of the snowman bench and a fir stands in front of the Santa bench.
  The town's big decorated Christmas tree and a snow pile stand right at the front of the snow globe. On the testers'
  (release) town, a tree grows beside the train's engine.
- The release benches and snow globe on the harbour look right.
- Nothing for you to do. The Iron Golem gets the numbered list below as a fix-up, which moves four pieces and retakes
  the shots.

Reviewer: Iron Golem, fresh session, 2026-11-10. Read-only: nothing in P856's files was changed.

## What was checked

- Guide read in full: `notes/guides/building-and-decorating.md` in the docs copy. That covers sections 1-11, including
  the keep-clear rules in 5, visibility in 1 and 6, and What to use where in 10.
- From `origin/golem/Iron/P856`, both copies fetched:
  - `notes/cc-P856-review/`: `placed.md` (784 parts), `pieces.jpg`, `main-park.jpg`, `rel-harbour.jpg`,
    `rel-train.jpg`, and the 8 TazUO shots in `shots/`;
  - the notes `notes/cc-P856-new-haven-winter-set.md`;
  - the code diff (`WinterSet/` 3 files, the seeder, `FestivalStore.cs`, tests).
- Every image looked at.
- The footprint of each piece comes from `placed.md`:
  - main: train 3610-3615 x 2529-2549; snowman bench 3617-3619 x 2541-2550; Santa bench 3610-3617 x 2554-2555;
    globe 3637-3642 x 2555-2560;
  - release: train 3546-3551 x 2513-2533; snowman bench 3502-3504 x 2592-2601; Santa bench 3500-3507 x 2588-2589;
    globe 3517-3522 x 2590-2595.
- The trees within 3 tiles of each footprint were read from the map statics:
  - main (SoS) with P678's `sosbase.py`;
  - release (vanilla Trammel) with P856's own `rel/nhbase.py`, through a scratch script.
- P678's winter rows near the globe were read from `ClusterFWinterDecorLayout.cs`.

| Guide item | Applies? | Result |
|---|---|---|
| Walls, corners, roofs, doors, windows, stairs | No buildings placed | n/a |
| Wall-mounted items, facing | Each design is placed whole "as made" and no part is turned (placed.md). The renders (`pieces.jpg`) draw whole, and the train runs along y on its rails. | ok |
| Signs | None placed. Seasonal props are not places that need a sign. | n/a |
| Shores, bridges, docks | Nothing built on them. The release pieces stand on the existing pier and boardwalk, flat within 2 (validate-release.txt). | ok |
| Heights | Every tile is reached on foot and is flat within 2, and the town walk is intact (validate-main.txt, validate-release.txt) | ok |
| Nothing stray, keep clear, visible (1.4, 5 "Keep clear", 6) | Trees and another winter row stand against four pieces | **FAIL**, items 1-4 |
| Shots show the piece (8) | Both train shots cut the engine off at the frame's bottom edge | item 5 |
| What to use where | Stock art only; no pack fits better. The packs are the downloads' own designs. | ok |

The release harbour pieces pass. These are the snowman bench at 3503,2596,1, the Santa bench at 3503,2588,16 and the
globe at 3519,2592,1. No tree stands near them. The only foliage near any of them is an o'hii plant at 3498,2586, two
tiles off the Santa bench's west end, behind it from the camera. The shots show each of them whole and clear.

## Verdict

BUILD REVIEW P856: FAIL

1. **Main snowman bench** (`set-snowman-bench`, origin 3618,2545,0; tiles 3617-3619 x 2541-2550).
   - What is wrong: two map trees stand against its west side. One is the tree 0x0CD3 with leaves 0x0CD4 at
     3616,2547,0. The other is the oak 0x0CDD with leaves 0x0CDE at 3616,2550,0. Both draw after the bench's
     neighbouring parts, so in `shots/p856-main-snowman-bench.jpg` and `main-park.jpg` a canopy covers the bench's
     middle and its garland.
   - What the guide wants: trees stay 3 tiles from server items and landmarks, and props stay visible (section 5,
     "Keep clear", and checklist 1.4).
   - Fix: move the bench to open grass with no tree within 3 tiles of any tile it covers.
2. **Main Santa bench** (`set-santa-bench`, origin 3613,2554,0; tiles 3610-3617 x 2554-2555).
   - What is wrong: two cedars 0x0CD6 and 0x0CD8 stand against it, one on each side. The first is at 3612,2553,0, on
     the north. The second is at 3612,2556,0, on the south, the camera side, so it draws over the bench. In
     `shots/p856-main-santa-bench.jpg` a fir covers Santa's west lamp post and a leafy tree covers the garland.
   - What the guide wants: the same as item 1.
   - Fix: move the bench clear of trees by 3 tiles.
3. **Main large snow globe** (`set-snow-globe`, origin 3639,2557,0; tiles 3637-3642 x 2555-2560).
   - What is wrong, east side: two of P678's own winter rows stand one or two tiles off its open front. The decorated
     Christmas tree `road-main-w` (0x3393) is at 3643,2560,0, diagonal to the globe's south-east corner. The snow pile
     `road-main-snow-w` (0x08E2) is at 3644,2557,0. In `shots/p856-main-snow-globe.jpg` the tree stands across the
     globe's front candy canes and entrance, and the white snow pile stands beside it. Two pieces of decor compete for
     one spot.
   - What is wrong, west side: the map walnut 0x0CE3 with leaves 0x0CE4 at 3636,2556,0 is against the globe's west
     wall.
   - What the guide wants: nothing stray, and the piece reads from the default camera (2.6, 5 "Keep clear", 6). The
     prompt's own camera rule (nothing on the 3 tiles south or east) should cover other decor as well as buildings.
   - Fix: move the globe so that no tree and no other winter row is within 3 tiles. Do not move P678's rows.
4. **Release Christmas train** (`set-train`, origin 3548,2523,14; tiles 3546-3551 x 2513-2533).
   - What is wrong: the sapling 0x0CEA at 3551,2533,14 is inside its outline, and the walnut tree 0x0CE0 with leaves
     0x0CE1 is at 3552,2532,14, beside the engine. In `rel-train.jpg` the tree draws over the engine end. A second
     sapling 0x0CE9 is at 3554,2535.
   - What the guide wants: the same keep-clear rule as item 1.
   - Fix: move the train north or west on the open grass until no tree is within 3 tiles. `rel-train.jpg` shows clear
     grass north of it. Then re-check that the walk is intact.
5. **Shots and the finder** (section 8: the reviewer must see each piece whole).
   - What is wrong: `shots/p856-main-train.jpg` and `shots/p856-release-train.jpg` cut off the engine at the frame's
     bottom edge.
   - Fix: after moving the pieces, retake the shots with the trainee standing far enough north-west that each piece is
     whole in frame.
   - Fix: add the missing rule to `find856.py` and `rel/findrel.py`, so that the next search catches this by itself:
     no tree (map static) and no other winter row within 3 tiles of any tile a piece covers. Then re-render
     `main-park.jpg`, `rel-train.jpg` and the main globe area, and update `placed.md`.

P865 DONE
