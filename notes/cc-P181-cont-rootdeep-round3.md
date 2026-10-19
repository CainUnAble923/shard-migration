# cc-P181: Rootdeep round 3 (bookcases lined up, corners detailed)

2026-10-19. Prompt: `D:\UO\cc-prompts\cc-P181-cont-rootdeep-round3.md`. Continues P180 (paused at its renders; Chase
05:54: "A looks the best. Needs another pass to line up all bookcases. Also have it spend more time on detailing
corners."; 05:56: take notes for the next dungeon so the same mistakes are not made again).

## Headlines

- **The Stacks' rows wandered because round 2 mixed two bookcase facings in one row.** 0x0A97, 0x0A98 and 0x0A9B
  have their back on the tile's north edge (they face south, for rows along x); 0x0A99, 0x0A9A and 0x0A9C have it on
  the west edge (they face east, for columns along y). P180 called all four "south-facing variants". Measured on the
  art footprints and confirmed on OSI's Lycaeum library (Moonglow, Trammel 4286-4293 x 962-999, from ModernUO's
  `Distribution/Data/Decoration/Britannia/moonglow.cfg`): its six east-west rows use exactly 0x0A97/0x0A98/0x0A9B,
  its north-south column exactly 0x0A99/0x0A9A/0x0A9C, and a candelabra stand (0x0B26) ends a row. Round 3 does the
  same: both rows south-facing only, every piece at Z 0, flush, a candelabra on each end tile (`stacks-check.png`).
- **Every inner corner is dressed** (62 by the builder's count: 16 Vault, 12 Warren, 9 Tangle, 9 Dawnseam, 4 each
  Landing, Brood Pit, Gloom, lair) by zone rules taken from OSI rooms surveyed with map statics plus ModernUO's
  decoration items: webs, bones and stains on the corner tile, a wall torch on the north or west wall at a third of
  them, rubble, a skull, a candelabra or an egg case on the visible wall strip beside the corner, a column or stone
  pillar at the south-east corner of the four big rooms; in the caves a stalagmite, root or crystal cluster on the
  rock round every inner corner and a piece on half the rock tips. Six corners before and after in `corners-check.png`.
- **Every opening is framed**: the four Vault gaps with OSI's marble pier-and-arch pattern (0x0113/0x0114 across an
  east-west wall, 0x0115/0x0116 along a north-south one), the lair mouth with (a) as approved, the Thicket and Seam
  Heart gaps with stalagmites or crystals on the rock either side, the crawlway exit with a rock either side. The
  Brood Pit mouth and the tunnels are passages between two floors (no wall line), left plain as OSI leaves run ends.
- **The general machinery moved to `scripts\mapbuild\`** (readers and writers, the wall rule, corners, frames,
  scatter, the renderer, the OSI survey, the slope audit, the checklist), proven identical to round 2 before any rule
  changed. **The playbook is `notes\map-building-playbook.md`**: the mistakes with their rules and checks, the
  rules of thumb with OSI densities, the tools, the pre-render checklist (run below, all nine PASS).
- **A bug in a shared reader**: P36's `uodata.load_land` swapped x and y inside every 8 x 8 block. It did not touch
  the map writes (the builder and `verify` use the per-cell offset), but every land-grid dump made with it since P24
  was scrambled within blocks, and a cave edge-tile rule I first derived from Khaldun came out with its sides swapped
  until vseUOAware disagreed. Fixed (`uodata.py`, one transpose) and cross-checked tile by tile against
  `inspect_map_region` and pinned `TileMatrix.cs:345`.
- **The cave rings stay as built** (Chase did not object). Khaldun's edge-tile foot was tried on the Tangle and
  dropped: on our one-tile sloped ring the texture's black wedge stretches into teeth (`cave-foot-check.png`). The
  slope audit finds no spread over 12 anywhere; vseUOAware's `diagnose_land_transitions` on a ring corner shows the
  expected 12 and 8 steps and `rank_transition_candidates` scores our ring tiles GOOD (ranks 4 of 41 at 5141,1197).
- No server code changed: no Docker build, no `sl-modernuo:cc-P181` image, no CHANGELOG entry. The walkable floor,
  the 18 openings, the crawlway and all 1,614 wall tiles are exactly P167's (the gate stayed on and green).
  1,559 statics of 123 distinct ids (round 2: 1,397 of 106); 11,320 land tiles, 44 distinct ids, unchanged.

## 1. The Stacks (prompt section 1)

1. **Why the rows wandered.** The art footprints (`scripts\mapbuild\isorender.py` on each piece, lowest lit pixels
   relative to the cell centre): 0x0A97/0x0A98/0x0A9B/0x0A9D lowest at +11..+16 (right of centre: the box's near
   edge runs from the right corner down, so the back is on the north edge and the piece faces south); 0x0A99/0x0A9A/
   0x0A9C/0x0A9E lowest at -15..-12 (back on the west edge, faces east). Round 2's table was 0x0A97, 0x0A99, 0x0A9B,
   0x0A9D, so a third of each row faced the wrong way and stood a third of a tile off the line.
2. **OSI's library, dumped and copied.** `python -P scripts\mapbuild\survey.py deco 4278 915 4302 1000` lists the
   Lycaeum's items: rows at y 962, 965, 968, 971, 990, 993 from x 4288 or 4289 to 4293, ids 2711/2712/2715 (0x0A97,
   0x0A98, 0x0A9B) mixed; the column at x 4286 from y 949 to 999 with 2713/2714/2716 (0x0A99, 0x0A9A, 0x0A9C);
   CandelabraStand 2854 (0x0B26) at 4286,962, 4286,978, 4286,990, 4288,920 and 4286,948: the ends of rows and
   columns. Rows three tiles apart (two floor tiles between). Rendered with its decoration items in `stacks-check.png`
   (right) and `osi-reference.png`. The map itself holds no bookcases anywhere in Trammel (seven 0x0A9E in Yew);
   OSI's furniture is server-side, which is why a map-only survey calls the Lycaeum empty.
3. **As built**: `plan-sets.json` `obstacles."Stacks shelving"`: ids 0x0A97 40, 0x0A98 30, 0x0A9B 30, never two alike
   side by side, `ends` 0x0B26 on both end tiles of each row; z [0]. North row x 5156-5166 y 1135, south row x
   5158-5168 y 1139 (P141's rects, unchanged): 9 bookcases and 2 candelabra each.
4. **Centred and even, within the approved footprint.** Both rows are 11 long; the aisle between them is 3 tiles
   (y 1136-1138) and each row stands 3 tiles from its wall (y 1132-1134 and 1140-1142), so the room is symmetric
   north to south. East to west the rows are offset by two tiles (the north row starts at the west wall, the south
   row ends at the east wall): that is P141's approved kite layout, and moving either row changes obstacle tiles and
   so the walkable set, which the gate forbids. Kept; said again under Deviations.
5. **Checked**: `checklist.rows_straight`: 2 rows contiguous, one Z, one facing each (PASS).

## 2. Corners (prompt section 2)

### 2.1 What OSI does (`scripts\mapbuild\survey.py corners`, map statics plus decoration cfg items)

| OSI block (Trammel) | Set | Floor tiles | Inner corners | Dressed within 1 tile | What is in the corners | Decor per 100 floor tiles (floors, roofs, water left out) |
|---|---|---|---|---|---|---|
| Deceit level 1, 5128-5250 x 526-640 | dungeon | 4,492 | 386 | 187 (48%) | bones 36, small web 25, rubble 25, garbage 24, wall torch 21, skeleton 18, skull 8 | 20.4 (rubble 3.7, bones 1.4, stone table 1.3, torch 1.0, garbage 1.0, skull 0.8, small web 0.6) |
| Deceit room block, 5178-5212 x 526-577 | dungeon | 561 | 53 | 25 (47%) | rubble 12, small web 4, bones, braziers 2, torches 2 | 26.9 (rubble 15.0) |
| Covetous, 5376-5631 x 1792-2036 | dungeon, cave | 25,912 | 247 | 162 (66%) | spiderweb 60, debris 39, skull 18, cot 16, blood 12, bones 12 | 13.4 (stalagmites 2.3, spiderweb 1.2, flowstone 0.9, hay 0.9, bones 0.8, skulls 0.8, debris 0.7, mushroom 0.7) |
| Khaldun, 5376-5567 x 1280-1407 | stone | 15,303 | 432 | 164 (38%) | rubble 132, brazier 41, skull 22, light 17, flowstone 15 | 5.6 (rubble 1.9, brazier 0.5) |
| Terathan Keep, 5416-5479 x 3108-3147 | stone | 2,098 | 98 | 58 (59%) | rubble 39, wall torch 19, small web 11, stain 4, web 3, cocoon 2 | 16.5 (rubble 7.1, leaves 1.4, torch 1.1, webs 0.9) |
| Hythloth level 1, 5900-6140 x 0-200 | dungeon | 11,398 | 195 | 64 (33%) | garbage 13, blood 12, chests 7, candelabra 7, debris 6, webs 6 | 5.0 |
| Nujel'm hall, 3672-3696 x 1231-1287 | marble | 1,109 | 59 | 24 (41%) | candelabra 13, flowerpot 4, chests 3, benches 2, sconces 2 | 15.2 (tables 2.9, candelabra 1.6) |

Torches: all 150 wall torches and sconces in those blocks hang on a wall directly north (0x0A0A, 0x0A0C, 0x0A0D,
0x0A0E, 0x0A01) or directly west (0x0A05, 0x0A07, 0x0A08, 0x0A09, 0x09FC) of their floor tile; none on a south or
east wall. Braziers (0x19BB, 0x0E31, 0x1F2B) stand free or by a wall. Non-wall items on wall tiles: Khaldun 207
(rubble 104, skulls 13, debris 8, braziers 5), Terathan Keep 68: OSI puts things on the visible strip.

### 2.2 The rules (`plan-sets.json` `zones.*.corners`; `build_burrows.py` step 7)

- An inner corner is a floor tile with a wall or ring tile straight north or south and straight east or west
  (`mapbuild.walls.concave_corners`); openings and the bookcase, crystal and web-pillar blocks do not count as walls.
- Item zones: on the corner floor tile, passable pieces only (cobwebs, bones, stains, a brazier 0x0E31 in the
  Gloom), each by its own probability; a wall torch by the zone's torch chance on the north wall (0x0A0C/0x0A0D) or
  west wall (0x0A07/0x0A09), never south or east; on the visible strip (`visible_strip_tiles`: the wall tiles south
  and east of the corner, whose top face shows because their slab is on the far edge) rubble 0x1363-0x136C, a
  skull, a candelabra 0x0B26 (Vault) or an egg case (lair), at most one of each kind per corner and never beside
  another of the same kind; a marble column 0x011B or stone pillar 0x01DA on the south-east corner tile of rooms at
  least 12 on both sides (Strongroom, Landing, Gloom west, the lair). If the dice left a corner bare, the builder
  places the first strip piece, else the first floor piece: no corner stays empty.
- Cave zones: a cluster of 2 or 3 of the zone's corner pieces on the ring tiles round the corner (the diagonal rock
  tile and its two neighbours along the ring; impassable rock already), and one piece on about half the rock tips the
  floor wraps round (`convex_corners`). Warren and Brood Pit: stalagmites and rocks; Tangle: stalagmites, fallen logs,
  a mushroom; Dawnseam: crystals.
- Cobwebs high: the hanging webs 0x10B8-0x10BB at 60 percent of Gloom corners and 85 percent of lair corners.

### 2.3 Per zone (from `build-report.json`; concave = inner corners, convex = rock or wall tips the floor wraps round)

| Zone | Inner corners | Changed | Convex | Changed | What went in |
|---|---|---|---|---|---|
| Landing | 4 | 4 | 4 | - | rubble 3, stain 3, torch 2, bones 1, cobweb 1, stone pillar 1 (SE) |
| Vault | 16 | 16 | 24 | - | candelabra 7, cobweb 7, torch 6, marble column 1 (Strongroom SE); 4 openings framed (12 pieces) |
| Warren | 12 | 12 | 22 | 8 | stalagmite and rock clusters 27 pieces; 8 stalagmites on tips |
| Brood Pit | 4 | 4 | 2 | 1 | stalagmite clusters 10; 1 on a tip |
| Tangle | 9 | 9 | 11 | 3 | roots and stones 20; 3 root tips; Thicket gap framed (2) |
| Dawnseam | 9 | 9 | 11 | 0 | crystal clusters 22; Seam Heart gap framed (2); no tip drawn this seed |
| Gloom | 4 | 4 | 10 | - | cobweb high 2, bones 2, skull 2, rubble 2 |
| Gloom lair | 4 | 4 | 2 | - | cobweb high 2, cobweb 2, rubble 2, egg case 1, skull 1, bones 1, stain 1, stone pillar 1 (SE); mouth frame (a) 2 pieces, mouth webs 5 |

Item walls: 1,614 wall tiles re-checked, one wall-flagged piece per tile (`check_wall_tiles`: none doubled), the same
pieces as round 2 except the 10 tiles where a frame jamb or pier replaced a run piece.

### 2.4 Cave corners and the transition tools (prompt 2.2)

UO has no cave-floor-to-rock corner tile: the cave edge tiles 0x024A-0x0259 go from cave floor to black (Khaldun
uses them at the flat foot of its rock mounds: 0x024E/0x024F/0x0253 rock to the south, 0x0250-0x0252 west,
0x0254-0x0256 east, 0x0257-0x0259 north, 0x024A-0x024D the two-sided corners; 2,058 tiles measured), and the rock-to-
black edges 0x0262-0x0265 are used 40 times in all of Trammel. Dirt and crystal floors have none. The Tangle (cave
floor) was built with the edge tiles at the ring (`ringEdge` in `plan-sets.json`, `EDGE_TILES` in the builder) and
rendered: because our ring's floor-level tile is itself the slope (floor 0, ring 0 with its far corners at 12, rock
12, void 20), the stretched texture shows its black wedge as teeth along the whole foot. Khaldun keeps that tile
flat and slopes the rock behind it, which needs one more tile of wall than P141's layout has. Turned off; the test
picture is kept (`cave-foot-check.png`) and the option documented. What the corners got instead is the clusters above.

Audit: `mapbuild.audit.slope_audit` over all 11,320 written tiles: no tile with a corner spread over 12 (the ring
tile is 12, the +12 ramp 8). vseUOAware on the scratch copy: `diagnose_land_transitions` at 5143,1173 (6 x 6, the
Crawl Den to Great Burrow wall): ring tiles spread 12, ramp tiles spread 8, flat floor, nothing else; at 5140,1158 the only spread of 20
is on void tiles beyond the ramp (black on black, outside the build line). `rank_transition_candidates` at 5141,1197
over all cave ids: the ring tile 0x0266 scores 22.2 GOOD, rank 4 of 41 (best 0x0269 at 20.3; all under 25).

### 2.5 Doorways and openings (prompt 2.3)

Measured first: `mapbuild.walls` docstring and the playbook table. Marble: Nujel'm row 1323 (0x0113 at 3737 and
3740, 0x0114 at 3738, open at 3739) and Magincia column 3716 (0x0115 at 2064, 2067, 2070; 0x0116 at 2065, 2068);
dungeon: Deceit row 535 (0x0245, 0x0247, 0x0247, 0x0249) and column 5183 (0x0248 on 541-542, 0x024A beside 0x0241
on 543). The builder groups opening tiles into straight gaps (`opening_groups`), finds the wall tiles before and
after, and applies the set's `frameNS`/`frameEW` (`frame_pieces`): 8 groups, 7 framed, 1 passage (the crawlway,
whose two ends are floor; it gets rocks either side instead). Round 2's hard-coded lair arch became the stone
set's rule and lands on the same two tiles. Test rooms with a marble gap each way, the OSI doorway, and every built
frame are in `frames-check.png`.

## 3. The module and the playbook (prompt section 4)

`scripts\mapbuild\` (README there): `uofiles.py`, `walls.py`, `scatter.py`, `isorender.py` (moved; the notes copy is
a shim), `survey.py`, `audit.py`, `checklist.py`. Proof of the move: the refactored builder, run with round 2's
`plan-sets.json`, produced `statics-placed.csv`, `land-summary.csv` and `plan-cells.json` identical to round 2's
(diff: only the two lair arch pieces, which the old proposal code had placed and the new frame rule places once
`frameNS` is in the rules). Rootdeep-specific code stayed in `notes\cc-P167-tools\build_burrows.py` (zones, ring Z
profile, decor and corner driver, points from the seeder and region files).

`notes\map-building-playbook.md`: section 1 the mistakes (walls swapped, the half-tile renderer, diagonal runs,
repetitive floors, wandering rows, bare corners, the four opening tiles, the land reader, the copied edge tile,
impassable decor on floors, trusting the writer), section 2 rules of thumb with the OSI numbers above, section 3 the
tools and what moved, section 4 the pre-render checklist and the picture set.

## 4. The pre-render checklist (playbook section 4), run before the renders

`python -P notes\cc-P167-tools\checklist.py`:

| Check | Result | Detail |
|---|---|---|
| walls against a test room | PASS | 3 wall sets, 5 x 5 rooms: corners post / ew / ns / corner, runs single pieces |
| no diagonal wall runs | PASS | 1614 wall tiles, none joined only diagonally |
| rows straight (the Stacks) | PASS | 2 rows contiguous, one Z, one facing each |
| every inner corner dressed | PASS | 62 inner corners, every one dressed |
| every opening framed or a passage | PASS | 8 opening groups, 8 framed or passages |
| variety: no identical decor side by side | PASS | 105 distinct decor ids in 35 categories, 0 identical pieces touching |
| transitions audited (slope spread <= 12) | PASS | no tile over the slope limit |
| one wall piece per tile | PASS | no doubled wall tiles |
| walkable-floor gate | PASS | walkable floor, openings and wall tiles equal the previous build |

Seen red first: corners dressed (Vault 15 of 16, before the no-empty-corner fallback), variety (hay clusters with
two usable ids put 0x0F34 beside 0x0F34 nine times, then two candelabra on adjacent strip tiles; fixed in
`pick_unlike` and the strip rule), and the gate (P180's test, unchanged). The build itself: `--fresh` restored the
three files (hashes 872269bb, 2109d96b, d7ae4bfc), `verify: land mismatches 0; statics round-trip True (1559 read back)`.

## 5. The renders (prompt section 3)

`notes\art\rootdeep-build\index.html`: the question at the top, the Vault and Gloom west round 2 beside round 3,
then the checks, the overview and the eight zones. Round 2's files moved to `round2\` (round 1 stays in `round1\`).

| Picture | What | KB |
|---|---|---|
| stacks-check.png | round 2 Stacks, round 3 Stacks, OSI's Lycaeum rows with their decoration items | 235 |
| corners-check.png | six corners before and after: Vault Strongroom SE and lair SE (item wall), Crawl Den NW and Tangle NW (cave), the Vault doorway and the Thicket gap (doorways) | 507 |
| frames-check.png | marble gap test rooms both ways, Nujel'm's doorway, the five built frames, the crawlway, the Brood Pit passage | 545 |
| cave-foot-check.png | rock foot (kept), edge-tile foot (rejected), Khaldun's mounds | 152 |
| walls-check.png, lair-mouth-check.png | as round 2 (the lair mouth now labelled (a) approved) | 810, 158 |
| osi-reference.png | Deceit room with its items, Terathan Keep's NW room, Khaldun, a Covetous cave | 358 |
| overview.png; landing, vault, warren-west, warren-east, tangle, dawnseam, gloom-west, gloom-east | as round 2's rectangles | 10; 481 to 1,019 |

Largest file in either repo: `tangle.png`, 1,019 KB; `notes\art\rootdeep-build\` is 22 MB over three rounds.
`notes\cc-P34-tools\town.png` (5.6 MB) is older and ignored (`.gitignore:25`, proven with `git check-ignore`).

## 6. What changed, with file:line

| File | Change |
|---|---|
| `scripts\mapbuild\uofiles.py` (new) | `MapFile` (:95, per-cell offsets), `load_land` (:138, the fixed transpose), `statics_in`, `write_land`, `write_statics`, `verify`, `restore_scratch`, `read_tiledata`, `same_cells` |
| `scripts\mapbuild\walls.py` (new) | `wall_pieces` (:36, P180's rule), `walls_for`, `concave_corners` (:76), `convex_corners`, `visible_strip_tiles` (:100), `opening_groups` (:118), `frame_pieces` (:146), `check_wall_tiles` |
| `scripts\mapbuild\scatter.py` (new) | `weighted`, `pick_unlike` (:14, with the clear-id fallback), `scatter` |
| `scripts\mapbuild\isorender.py` (moved from notes) | reads through `uofiles`; statics on one tile sort by Z then height (:270) |
| `scripts\mapbuild\survey.py`, `audit.py`, `checklist.py`, `README.md` (new) | the OSI survey, the slope audit, the checklist functions |
| `notes\cc-P167-tools\build_burrows.py` | rewritten on the module: Stacks ends (:160), frames (step 6, :300), corners (step 7, :330), checks and the audit (step 9, :420), `cave_test_scenes` (:520) |
| `notes\cc-P167-tools\plan-sets.json` | frames per wall set, corner rules per zone, `gapFrame`, `ringEdge` (off), the Stacks table and ends, the crawlway frame, proposals trimmed to the mouth webs |
| `notes\cc-P167-tools\checklist.py`, `build-report.json` (new) | the checklist driver and the build's corner, frame and audit report |
| `notes\cc-P167-tools\render_burrows.py` | round 3 pictures, round 2 moved to `round2\`, `--page-only` |
| `notes\cc-P167-tools\isorender.py` | now a shim onto the module |
| `notes\cc-P167-tools\statics-placed.csv`, `land-summary.csv` | regenerated (1,559 rows; land unchanged) |
| `notes\cc-P36-tools\uodata.py:109` | `load_land` transpose `(0, 3, 1, 2)` with the reason |
| `notes\map-building-playbook.md` (new) | the playbook |
| `notes\art\rootdeep-build\` | round 3 pictures and index; `round2\` |

## 7. Tests and gates

No shard code changed, so no xUnit tests and no `build.sh`. Gates that held this work, each seen red before green:
the refactor identity diff (red: the two lair arch rows, explained; green on every other row), the checklist rows
above, the builder's floor and obstacle asserts (P180's), the walkable gate, `verify` after the write. The surveys
were cross-checked where it mattered: the land reader against vseUOAware tile by tile at 5144-5155 x 1159-1162 (a
mismatch first, then equal after the fix), the bookcase facings against the Lycaeum's rows and columns, the marble
arch orientation against two OSI buildings, the Khaldun edge-tile rule re-derived after the reader fix (every id's
orientation changed sides, which is how the reader bug was caught).

## 8. Deviations and decisions for Chase

1. **The Stacks' two rows stay offset by two tiles east to west** (north row x 5156-5166, south row x 5158-5168):
   P141's approved kite layout, and the obstacle tiles are part of the walkable set the gate protects. They are
   straight, equal, evenly spaced north to south and flush. If you want them stacked exactly over each other, say
   so: it is a two-rect change in `layout.json`, a re-recorded `plan-cells.json`, and the spawner paths re-checked.
2. **Corner pieces on floor tiles are passable only** (webs, bones, stains, torches, a brazier); rubble, candelabra,
   egg cases and pillars stand on wall and ring tiles, and the cave corner clusters and tips on ring tiles. 118 floor
   tiles carry impassable decor from the scatter rules (round 2: 100): the same rules and densities, but the random
   sequence shifted (the Stacks' new table and the never-two-alike fallback consume draws differently), so different
   clusters landed on tiles that pass the roomy test. Every one has three open sides in a room at least 6 wide, off
   spawner homes, openings and paths; the builder asserts it.
3. **The Khaldun edge-tile foot was tried and rejected** (section 2.4). Kept as `ringEdge` for a build with room for
   a flat foot tile.
4. **Columns and pillars only at south-east corners** of rooms at least 12 x 12: on the other three corners the
   piece would stand behind its own wall slab (north and west ring tiles hide what is on them). Four in all.
5. **Torches only on north and west walls**, as every OSI torch in the surveyed blocks; a corner with walls only to
   the south and east gets none.
6. **The Brood Pit mouth and the tunnels are not framed**: they are passages between two floors with no wall line
   (OSI leaves a run's free end plain). The 18 openings in the record are all framed or (the crawlway) rock-flanked.
7. **`uodata.load_land` was fixed in place** (P36's shared reader). Scripts that used it before P181 (P24's
   `diff_land.py`, `land_clusters.py`, `render.py`; P36's `diff_land.py`; P180's `dump_walls.py` for its land line)
   read land scrambled within 8 x 8 blocks; P180's wall research read statics, not land, so its rules stand. Nothing
   in `docs\` rests on a land-grid dump that I can find; say if one should be re-run.
8. **Survey numbers in the playbook come from the fixed reader** and include ModernUO's decoration items; the first
   pass (broken reader, map only) gave different percentages and is not quoted anywhere.
9. **CHANGELOG skipped**: no code a player or staff member runs changed. `tools\progress.py --dry-run` ran: 1094
   customization files, 106 patches, 1012 tests, unchanged.
10. No task-list tool was available to this session, so the per-step progress Chase follows remotely could not be
    posted; the steps and their state are in this note instead.

## For Chase

1. Open `notes\art\rootdeep-build\index.html`. **Approve these renders, or say what to change.** Look first at the
   Stacks (before, after, OSI), then `corners-check.png` (six before-and-afters), then the Vault and Gloom west side
   by side, then the frames.
2. The one open layout question is item 1 above (the two-tile stagger between the bookcase rows).
3. Rebuild and re-render: `python -P build_burrows.py D:\UO\cc-p167-work\scratch-client --fresh`, then
   `python -P checklist.py`, then `python -P render_burrows.py D:\UO\cc-p167-work\scratch-client` (about 4 minutes
   together). Weights and probabilities are in `plan-sets.json`.
4. After approval the next prompt does P167 sections 2 and 3: the way in from Old Haven, the skeleton and crier
   spawners, the real map write, the package and the test shard.

## Repo size

No file over 5 MB in either repo (`find -size +5M`: only the ignored `notes\cc-P34-tools\town.png`). The scratch map
copies (round 2 and round 3, 115 MB each) stay in `D:\UO\cc-p167-work\`, outside both repos. `__pycache__` folders
deleted (ignored anyway).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo    Result
----    ------
code    clean
docs    dry run
scripts clean
```

The docs repo's pending files: the round 3 pictures and index (the proposal crops removed, round 2's files under
`round2\`), `scripts\mapbuild\`, the five changed or new files in `notes\cc-P167-tools\`, `uodata.py`, the playbook,
this note, and the machine output in `testing\` and `tools\progress.json`.

P181 PAUSED: renders for Chase
