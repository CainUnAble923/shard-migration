# cc-P864: build review of P855 (data-driven decor addon, housing furniture batch)

## In plain words

- P855's new house furniture (grey fireplaces, the blue couch, kitchens, the barbecue, the harpsichord, the holiday
  fireplace and the League's dining tables) did not pass its building review yet. The pieces themselves look right in
  the game shots, but the build left no review folder and no list of placed pieces, and the house rule says a build
  without them cannot pass.
- The fix is small: the Iron Golem leaves that folder and list, plus a few shots of the pieces standing against a
  wall inside a house. P855 then merges, and the furniture shows up in the stores.
- Nothing for you to do. The integrator sends the list below to the Iron Golem as a fix-up.

Reviewer: the Iron Golem, in a fresh session that did not build P855. 2026-11-10. Docs copy
`D:\UO\golems\Iron\shard-migration`, code copy `D:\UO\golems\Iron\ShatteredLegacy`, both on `golem/Iron/P864`.
P855 was fetched as `origin/golem/Iron/P855` (commit 9343547c) without changing branch. Nothing was rebuilt.

## What I looked at

- `notes/guides/building-and-decorating.md`, read in full (sections 1-11, What to use where included).
- `git ls-tree -r --name-only origin/golem/Iron/P855 -- notes/cc-P855-review`: **no such folder.** No `placed.md`
  anywhere on the branch (`git ls-tree -r origin/golem/Iron/P855 | grep -i placed`: nothing). Prompt item 4 applies.
- What the branch has instead: `notes/cc-P855-decor-addon-housing-furniture.md`,
  `notes/cc-P855-shots/` (30 TazUO shots, one per design, each standing on open ground east of the League hall, plus
  the store and deed shots under `player/`), and the 30 `server/data/Decoration/Addons/*.cfg` files in the code diff.
- All 30 design shots, on contact sheets and in full-size crops, and the cfg data for every paired facing.

## What the shots and data show

Nothing in P855 is placed in the world: every piece is a house addon a player places from a deed, and the staff
`[DecorAddon place` is a tool. So the guide's building checks (walls and corners, doors, roofs, stairs, signs, shores,
bridges, docks, foliage) have no subject here. What can be checked:

- **Every design draws whole** from the default camera, all 30, with no missing or floating piece (lit fires, the
  couch hues, the feast tables' braziers, the bear rug).
- **Facings match their names.** For example, `grey-fireplace-small-east` has its stone back and mantel in column x 0
  and its hearth pavers out to x 1, so it faces east and stands against a **west** wall. The `-south` sets face south
  against a **north** wall. Both are the two walls the camera shows (guide 3, 9.2 item 7). The couch's four facings
  really differ (seat row x 1 east, x 0 west, y 1 south, y 0 north), as do the buffet, the formal dining table and the
  harpsichord pairs. Their thumbnails look alike, but the data does not.
- **The holiday fireplace** (one facing, "as made") carries its own fieldstone wall box: post 0x001D at -2,-2, south
  pieces 0x001C along y -2 to the north-east tile 2,-2, east pieces 0x001B at -2,-1 and 2,-1. The corners follow the
  east/south rule (guide 2.2). The hearth faces south with the rug at y 1-3, so it is a north-wall piece. But no shot
  shows it against a house wall, where it would stand a second fieldstone wall one row in front of the house's own.
- **Lights and flames** are kept as the authors made them (the notes say so). The country kitchen's stove fire uses
  the `ArchedWindowEast` light shape, which is odd but harmless. The barbecue's flame is the animated explosion
  0x36BD, which reads as a large fireball over a grill in `p855-barbecue-east.jpg`. These are taste points for Chase,
  not guide failures.

Because nothing is shown against a wall, the guide's facing check, "every wall-mounted item hangs on its wall, facing
the walk side" (sections 1.2 and 3), cannot be completed from these shots.

BUILD REVIEW P855: FAIL

1. No renders or placed list left for review: `notes/cc-P855-review/` and its `placed.md` are missing on
   `golem/Iron/P855` (guide section 8, checklist item 8). Leave `notes/cc-P855-review/placed.md` with one line per
   design: file name, piece count, facing, which house wall it is meant to stand against (for example
   "grey-fireplace-small-east, 21 pieces, faces east, against a west wall"), and any piece whose facing was chosen
   by the converter rather than the author (the two harpsichord files, named from their art). Put the shots (or
   copies) in the same folder.
2. All 30 designs, `p855-<design>.jpg`, at 3677,2570,0 on open grass: wall-backed pieces are never shown against a
   wall, so their facing cannot be checked against their wall (guide 3, 11.2). Place each wall-backed design inside a
   staged house, against the wall its facing names, and shoot it from the default camera. Cover at least one
   fireplace of each facing (`grey-fireplace-*-east` on a west wall, `-south` on a north wall), `country-kitchen-east`
   and `-south`, `small-kitchen-northwest` and `-southeast`, and `harpsichord-east` and `-south`. This also proves the
   player placement path in a house, which the notes say was not shown.
3. The holiday fireplace (`holiday-fireplace.cfg`; fieldstone 0x001D at -2,-2, 0x001C along y -2, 0x001B at -2,-1 and
   2,-1) brings its own wall box. Shoot it against a house's north wall, from inside, and say in `placed.md` whether
   its fieldstone row doubles the house wall or stands one tile in front of it. If it doubles the wall, or reads as a
   stray wall stub in a house of another material (guide 2.6, "nothing stray"), offer it without those wall pieces.

P864 DONE
