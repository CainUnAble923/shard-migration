# cc-P829: build review of P194 (port Wrong (revamped) and Covetous Void Spawn)

## In plain words

- The Bronze Golem's P194 (the revamped Wrong dungeon and the Covetous Void Pool) was checked before it merges. It
  **fails the review**: it left no pictures and no list of what it placed, so the reviewer had nothing to look at.
- Nothing in the game changes from this review. P194 stays unmerged until the Bronze Golem adds the pictures and the
  list (the fix list below) and a second review passes it.
- The work itself looks like a faithful copy of OSI's/ServUO's own layout (the Wrong level-3 maze and a 7x7 pool), so
  this is about missing proof, not a known bad build.
- Nothing for you to do.

## What was checked

Reviewed 2026-11-08 by the Iron Golem (fresh session; did not build P194), against
`notes/guides/building-and-decorating.md` (read in full).

- `git fetch origin golem/Bronze/P194` in both copies: branch head f9861593 (docs) and the matching ShatteredLegacy
  head.
- `git ls-tree -r --name-only origin/golem/Bronze/P194 -- notes/cc-P194-review` in the docs copy: **empty**. The only
  P194 file under `notes/` is `notes/cc-P194-port-wrong-and-covetous-void.md`. `git archive` of the review folder fails
  ("pathspec did not match"). So there are no renders, no TazUO shots, no walk logs and no `placed.md`.
- Read the P194 notes and the diff (`git diff main...origin/golem/Bronze/P194`, 64 files in ShatteredLegacy) for what
  is placed in code:
  - `WrongDungeon/WrongDecoration.cs`: the 290 pieces of ServUO's `Data/Decoration/Wrong/WrongMaze.cfg` (224
    `WrongMazeWall` 0x0242/0x0248 and others, 34 `WrongBarredMetalDoor`, 1 `BarredMetalDoor`, 31 statics), level 3 of
    Wrong around 5690-5720, 620-650, on Trammel and Felucca, placed by `[SetupWrongRevamp`-style setup.
  - `Covetous Void Spawn/Generate.cs:96-147`: the 7x7 Void Pool at 5497-5503, 1995-2001, Z 5, both facets: the edge
    rows are light stone stair pieces 0x0751 (north row), 0x0752 (west column), 0x0753 (south row), 0x0754 (east
    column), hue 1954; the corners are 0x075D-0x0760 (1885-1888); the centre is random 0x213F-0x2144, unhued.
  - Spawners, waypoints and the two controllers, which are not decoration.
- The P194 notes say "no map, statics or art change is needed" and "nothing was placed in any world", which is why no
  proof was made; but the prompt is marked Touches map and the guide's section 8 asks every decoration build for the
  review folder. P194 was written 2026-10-20, before the guide (2026-10-29) and the build-review rule (cc-P734) existed.

Step 4 of the review prompt: with no `notes/cc-P194-review` folder and no `placed.md`, the verdict is FAIL.

## Verdict

BUILD REVIEW P194: FAIL

1. No renders or placed list left for review: `notes/cc-P194-review/` does not exist on `golem/Bronze/P194`. Leave it
   as the guide's section 8 asks: `placed.md` (one line per piece: item ID, x,y,z, facing, what it is, grouped by
   area: the Wrong level-3 maze and the Covetous Void Pool), an isorender of each area, and TazUO shots from the
   default camera on a private shard (port 2596 under the `test-shard` lock, never 2594).
2. Wrong level-3 maze (`WrongDecoration.cs`, 290 pieces, about 5690-5720, 620-650, Trammel and Felucca): render the
   whole maze top-down after the setup command (`isorender.py map ...`, roof-free), with the maze walls shown (they are
   hidden until a player stands beside them; render them visible, or shoot both states). The reviewer needs to see
   that the cfg's walls 0x0242/0x0248 meet the stock dungeon walls with no gap or doubled piece and that no piece
   lands on a stock static at the same tile (Decorate's skip rule only checks the same ID).
3. Wrong's 35 doors (34 `WrongBarredMetalDoor` + 1 `BarredMetalDoor`, cfg facings): list each with its facing in
   `placed.md` and show a shot of a few opened, so the reviewer can check each hangs in its wall line and folds back
   along it (guide 2.4), not across the corridor.
4. Covetous Void Pool (`Generate.cs:96-147`, 5497-5503, 1995-2001, Z 5): the edges are light stone **stair** pieces
   (0x0751 N row, 0x0752 W column, 0x0753 S row, 0x0754 E column) and the corners 0x075D-0x0760, which are not the
   guide's light stone corner steps (0x0758/0x0756 squared, 0x075B/0x075A rounded, guide 4.2). Render the pool alone
   (`render_addons.py ids:...` or an isorender after `[SetupNewCovetous`) and a TazUO shot from the default camera, to
   show each edge step climbs away from the pool (outward) and the four corners close the ring with no stub; if
   0x075D-0x0760 draw wrong, use the matching corner pieces of the same set. Also show the pool's Z 5 against the
   cave floor around it: a stair edge at Z 5 over a floor at 0 must not leave a lip a player cannot step (guide 4.1),
   and walk onto and off the pool both ways with a real character, logging each step's Z.
5. Signs and markers: none placed, which is fine; if any sign or marker is added for the Void Pool or Wrong's entrance
   in the fix-up, it is a named signpost 0xA854 north of the path (guide section 6), not a rune.
6. Before shots: the setup converts Covetous's stock level 1-2 spawners and adds the pool where the stock cave is
   bare; leave one before shot of the pool spot and one of the Wrong level-3 maze area before the setup (guide 8,
   item 5).

P829 DONE
