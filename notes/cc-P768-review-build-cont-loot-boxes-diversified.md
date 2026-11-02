# cc-P768: build review of P763 (loot boxes, more varied and more useful)

## In plain words

- P763 (the Iron Golem's loot box update) was sent for a building review only because one of its code files has
  "Decorative" in its name. It places nothing in the world: no buildings, walls, signs or decorations.
- By the review's own rule the verdict is FAIL, because P763 left no `cc-P763-review` folder with renders and a
  placed list. The fix is small: the Iron Golem adds a short placed list saying nothing was placed.
- Nothing for you to do. If you want the loot boxes merged sooner, the overseer's Skip-BuildReview.ps1 lets P763
  through without the fix-up.

Gold Golem, 2026-11-02. Docs copy `D:\UO\shard-migration` and code copy `D:\ShatteredLegacy`, both on `golem/Gold/P768`.
Reviewed `origin/golem/Iron/P763` (shard-migration 008bf6f9, ShatteredLegacy 144faea) against `origin/main`.

## What I checked

1. Read `notes/guides/building-and-decorating.md` in full (sections 1-11).
2. Fetched `origin/golem/Iron/P763` in both copies. `git ls-tree -r --name-only origin/golem/Iron/P763 --
   notes/cc-P763-review` lists **nothing**: the folder and its `placed.md` are absent. The branch has
   `notes/cc-P763-shots/` (7 TazUO shots of opened loot boxes plus `proof-log.txt`) and `notes/cc-P763-tools/` instead.
3. Read the code diff against `origin/main` (22 files, all loot-box code, tests, a migration and two patches):
   - `server/patches/SetToDecorativeGump-loot-box-herbalist.patch` is a one-line hook in ModernUO's plant gump
     (`SetToDecorativeGump.cs`). It awards a Herbalist box when a player sets a plant to decorative. "Decorative" there
     refers to plant status, not world decoration. That file name is what routed P763 to a build review.
   - `server/patches/Fishing-loot-box-firsts.patch` hooks fishing and SOS chests for the Fisher and Sailor boxes.
   - A search of the added lines for `MoveToWorld`, `Static`, `AddonComponent`, `Point3D` and decoration or mapops
     calls found only a treasure map item constructor and a test fixture moving a test mobile. Nothing is placed on a
     map.
4. Looked at the shots (for example `loot-06-spring-herbalist.jpg`). They show box contents in a gump, as P763's own
   proof intends. They show no building, wall, door, stair, sign, shore, foliage or wall-mounted item to check.

So no walls, corners, doors, stairs, wall items, roofs, signs, shores, bridges, docks or foliage were placed. There
was nothing to check against the checklist, and no better pieces from What to use where apply.

## Verdict

BUILD REVIEW P763: FAIL

1. No renders or placed list left for review: `notes/cc-P763-review/` and its `placed.md` are missing on
   `origin/golem/Iron/P763` (guide section 8; P768 prompt item 4). The guide wants a `placed.md` for every prompt that
   touches decoration. Here the fix is to add `notes/cc-P763-review/placed.md` that says P763 places no pieces in the
   world. It should also say that `SetToDecorativeGump-loot-box-herbalist.patch` is a plant-status hook awarding a
   Herbalist loot box, not map decoration. No renders are needed because nothing is built. The overseer's
   Skip-BuildReview.ps1 is the other way through. The integrator's classifier also matches "Decorative" in a patch
   name; a plant gump patch is a false positive.

P768 DONE
