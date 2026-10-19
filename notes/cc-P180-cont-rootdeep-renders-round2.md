# cc-P180: Rootdeep renders, round 2 (walls fixed, more variety)

2026-10-19. Prompt: `D:\UO\cc-prompts\cc-P180-cont-rootdeep-renders-round2.md`. Continues P167 (paused at its renders;
Chase 10-18 20:50: walls facing the wrong way and broken up, crystals, webs, textures and edges too repetitive).

## Headlines

- **The walls were wrong because P167 assumed a wall piece's art stands on its tile's north or west edge. It stands on
  the south or east edge.** Measured on six OSI buildings and five house designs, on the art itself and on the client's
  draw code, all three agreeing (`notes\uo-wall-orientation.md`, with the dumps in `notes\art\wall-research\`). The
  consequence: the piece that runs along x (0x00F9, 0x0241, 0x01D0) belongs on east-west rows, the one along y
  (0x00FA, 0x0242, 0x01D1) on north-south columns, the post on a room's north-west corner and the corner piece on its
  south-east. P167 had both swapped, so every run drew as a saw-tooth of short slabs. The Terathan stone set's corner
  piece exists: 0x01CF (P167 said there was none).
- **vseUOAware's isometric renderer drew every static half a tile too high** (art bottom at the land diamond's centre;
  the client puts it on the bottom, ClassicUO `View.cs:153-157`). That is why round 1's pictures and P167's art
  check could not settle the orientation. Fixed in our copy (`D:\UO\tools\vseUOAware\MODIFIED.md` item 7, built in
  `bin\P180\`; `bin\Release` was locked by two running servers and stays old until rebuilt). Round 2 is drawn by a new
  `notes\cc-P167-tools\isorender.py` (the client's layout, sloped land from the texmaps), so the cave rings no longer
  show black seams and walls sit on their lines.
- **Rebuilt and re-rendered**: `notes\art\rootdeep-build\index.html` (round 1 kept in `round1\`, the Vault shown side by
  side), with `walls-check.png` (a 5 x 5 and an L-shaped test room in each set beside OSI rooms of the same set and the
  same set as built) and `lair-mouth-check.png`. **The walkable floor, the 18 openings, the crawlway and all 1,614
  wall tiles are exactly P167's**: the builder compares its sets with the previous build's record and refuses to write
  if they differ (gate seen red, then green).
- **Variety**: every zone draws its floor from every stock variant of its texture by weight (one rng per zone, seeded in
  `plan-sets.json`), the cave rings and ramps from eight rock tiles each, and crystals, webs, stalagmites, hay, rubble,
  mushrooms, logs, vines and bones go down in seeded clusters with gaps, mixed sizes, random small Z where it fits, and
  never two identical pieces side by side. 1,397 statics of 106 distinct ids (round 1: 1,198 of 36); 44 distinct land
  ids. Rules (weights, cluster sizes, spacing, where) are data, not code.
- **Shown, not approved** (P167 s5 items 1, 2, 3, 5): the Stacks as bookcases, an arch and webs at the lair mouth
  (two ways), the cave rings as they are, the Vault doorway with no door. Each is in the index page with a crop.
- No server code changed, so no Docker build, no `sl-modernuo:cc-P180` image, no CHANGELOG entry. Both repos were
  clean at the start; `testing\` had nothing pending.

## 1. Section 0: the research

Written up as `notes\uo-wall-orientation.md` (rules, ASCII diagram, evidence tables with tile coordinates, the art
footprints, the client formula, what P167 did wrong, a checklist, what is unverified). Read there, not repeated here;
the short form:

| Case | Piece | Where it was seen |
|---|---|---|
| east-west run | 0x01D0 / 0x00F9 / 0x0241 | Keep row 3112; Nujel'm row 1234; Deceit row 535; tower multi 0x7A row -7 |
| north-south run | 0x01D1 / 0x00FA / 0x0242 | Keep column 5444; Nujel'm column 3687; Deceit column 5191; tower column -7 |
| NW corner | post | marble house 0x96 (-7,-7); tower (-7,-7); small stone house 0x64 (-3,-3); Deceit (5184,535) |
| NE corner | the east-west piece | marble house (0,-7); tower (8,-7); Deceit (5191,535) |
| SW corner | the north-south piece | marble house (-7,3); tower (-7,6) |
| SE corner, T from the west or south | the corner piece | marble house (0,3); tower (8,-2), (8,6), (-2,1); Deceit (5184,539); Keep (5431,3127) |
| doorway, N-S wall | 0x01D8 on the first open tile, open, 0x01D9 on the wall tile after | Keep 5431,3132-3134 and 5441,3127-3129 |
| doorway, E-W wall | 0x01D6, open, 0x01D7 | Keep 5436-5438,3131; tower -5..-3,1 |

Buildings read: small stone house (multi 0x64, plaster set), Terathan Keep (Trammel 5416-5479 x 3108-3147), the
tower house (multi 0x7A, the Terathan set), Nujel'm's marble hall and corridor (3672-3696 x 1231-1287, not a
rectangle), the large marble house (multi 0x96, interior wall) and the patio house (0x8C, interior wall), Deceit's
rooms (5178-5212 x 526-577), West Britain Bank's block for brick and wood. Renders of each in
`notes\art\wall-research\` (nine PNGs, 3.0 MB) with the letter grids (`*-grid.txt`) and `art-footprints.txt`; the
scripts that made them in `notes\cc-P167-tools\wall-research\`. vseUOAware was used for the role file, two
confirming reads (`inspect_map_coordinate 5184,539`, `get_item_tile 0x41CF`) and the offset test; the bulk dumps are
my scripts because the tool reads one tile a call. No map editor is on the PC (no UOFiddler, CentrED, Pandora), so the
house multis stand in for editor templates. `D:\UO\tools\vseUOAware\TileRoles.txt` (and both bin copies) now carry 25
DRAFT `wall-south | wall-east | wall-corner | wall-post | window-* | arch-*` rows with their source building.

## 2. What changed, with file:line

| File | Change |
|---|---|
| `notes\cc-P167-tools\build_burrows.py` | rewritten. `wall_pieces()` (:81) is the rule from the research; `walls_for()` (:100) builds any floor set's ring (used by the test rooms); `plan()` reads every look from `plan-sets.json`: weighted floors (:174), obstacle fills by kind (items / walls / mound, :186), rings and ramps by weight (:238), decor by `scatter()` (:383, clusters with spacing, `pick_unlike()` :368 for no identical neighbours), the proposals (:303); checks (:318): every floor tile free of anything but roomy decor, every obstacle blocked, walkable set equal to `plan-cells.json` (main, :531); `--fresh` restores the scratch files from the client copy and proves them pristine against `ORIGINAL-SHA256.txt` (:430); `test_room_scenes()` (:396) |
| `notes\cc-P167-tools\plan-sets.json` | **new meaning**: the rules (wall sets, per-zone seed, floor and ring weights, decor rules, obstacle fills, crawlway rocks, proposals). P167's output of that name (floor, opening and wall tile lists) is now `plan-cells.json`, which the builder reads back as the walkable-set record and rewrites |
| `notes\cc-P167-tools\isorender.py` | new: `Art` (art.mul, texmaps, tiledata), `Scene.from_map` / `from_multi`, `render()` with the client's offsets, stretched land with a normal shade, translucency for webs, `tile_px()` for crops |
| `notes\cc-P167-tools\render_burrows.py` | rewritten on isorender: radar overview, zones, proposal crops, `walls_check()`, `mouth_check()`, round 1 moved to `round1\`, the index with the side-by-side |
| `notes\cc-P167-tools\statics-placed.csv`, `land-summary.csv`, `plan-cells.json` | regenerated (1,397 rows; 60 land rows) |
| `notes\art\rootdeep-mockup\vse.py` | `Vse(exe=...)` to run another build of the MCP server (P141's helper, backward compatible) |
| `notes\art\rootdeep-build\` | eight zone renders, `overview.png`, `walls-check.png`, `lair-mouth-check.png`, three `proposal-*.png`, `index.html`; round 1's ten files in `round1\` |
| `notes\art\wall-research\`, `notes\cc-P167-tools\wall-research\` | the research renders, grids, footprints and scripts |
| `notes\uo-wall-orientation.md` | the research write-up |
| `D:\UO\tools\vseUOAware\Tools\MapEditorTools.cs:62`, `MODIFIED.md`, `TileRoles.txt`, `bin\P180\` | the offset fix (outside both repos), its record, the roles, the fixed build |

### 2.1 Variety, per zone (all stock EA tiles, no registry change)

| Zone | Floor (weights) | Ring / ramp | Decor rules (where; density per eligible tile; cluster) |
|---|---|---|---|
| Landing | cave 0x0245 50, 0246 20, 0247 15, 0248 10, 0249 5 | dungeon walls | none |
| Vault | marble 0x0486 55, 0487 20, 0488 15, 0489 10 | marble walls | cobwebs 0x0EE3-0EE6 (wallFace; 0.012; 1) |
| Warren | dirt 0x0071 40, 0072 20, 0075 15, 0076 10, 0073 5, 0074 4, 0077 3, 0078 3 | rock 0x025A 45, 025B 20, 025C 15, 025D 8, 025E 5, 025F 3, 0260 2, 0261 2 | stalagmites 0x08E1/E4/E5/E7/E9/EA/E3 (nearWall; 0.05; 1-3), rubble 0x1363-136D (nearWall; 0.02; 1-3), hay 0x0F34-0F36 (open; 0.012; 2-5), bones 0x1B09-1B10, 1B19-1B1A (any; 0.004; 1-3) |
| Brood Pit | as the Warren, pebbly ones heavier | as the Warren | stalagmites 0.05; hay 0.02 (3-7); bones 0.008 (1-4) |
| Tangle | cave, as the Landing with 0248/0249 heavier | rock 0x0266 45, 0267 20, 0268 15, 0269 8, 026A 5, 026B 3, 026C 2, 026D 2 | mushrooms 0x0D0C-0D19 (any; 0.02; 2-6), fallen logs 0x0CF3-0CF7 (any; 0.006; 1-2), vines 0x0CEB-0CF2 (wallFace; 0.03; 1-3) |
| Dawnseam | crystal 0x3867 50, 3868 25, 3869 15, 386A 10 | as the Warren | crystals small 0x2229-222C and 2224-2228 (open; 0.012; 1-4; z 0/0/0/1/2), big 0x2220-2222, 2224-2226 by the rock (nearWall; 0.03; 1-3), ice mushrooms 0x222E-2230 (any; 0.003) |
| Gloom | stone 0x0440 68, 0441 26, 043E 2, 043F 2, 043C 1, 043D 1 | stone walls | webs 0x0EE3-0EE6, 0x10D2-10D7 (nearWall; 0.035; 1-3), hanging webs 0x10B8-10BB (wallFace; 0.04; 1-2), bones (any; 0.006) |
| Gloom lair | stone 0x0440 64, 0441 30, light ones 6 | stone walls | webs (any; 0.04; 1-4), hanging webs (wallFace; 0.08; 1-3), egg cases 0x10D8 (nearWall; 0.012), bones and skulls (any; 0.012) |

Obstacles: Stacks rows as bookcases 0x0A97 40, 0A99 30, 0A9B 20, 0A9D 10 (south-facing variants, never two alike
beside each other); Strongroom pillars walled by the wall rule; root masses as before (rim at floor level, inside +12)
with the rock from the Tangle's ring table, logs on the rim (p 0.4) and brambles 0x0D3F/0D40 or vines on top (p 0.35);
crystal clusters from twelve crystals weighted to the big ones, z 0/0/1/2; web masses and pillars: 0x01DA every tile,
large webs 0x10B8-10BB at z 8/10/12 (p 0.6, 0.7), small webs at 0 (p 0.3). Every impassable decor piece stands on a
floor tile with three open orthogonal sides in a room at least 6 wide, off every spawner home, opening and crawlway
tile: **100** such tiles (round 1 had 61 stalagmites and loose crystals the same way); passable decor (hay,
mushrooms, webs, bones, logs, vines) can go anywhere not kept clear. "Cave edges continuous" (s1.5): the ring is the
8-neighbour ring as before, so closed; the gaps Chase saw were the renderer's flat diamonds at a Z step, which
isorender draws as slopes.

Section 1.3, diagonals: the layout is rectangles (floors and obstacles), its wall outline turns only at rectangle
corners and rectangle offsets of several tiles; the full-area grid (`wall-research\layout` check, done in session) has
no one-tile stair-step. Nothing to straighten.

### 2.2 Statics by reason (from `statics-placed.csv`, 1,397 rows)

```
  110 Vault wall ew     87 Vault wall ns     13 Vault wall corner    1 Vault wall post      1 Vault cobwebs
   49 Landing wall ew   43 Landing wall ns    5 Landing wall corner
  163 Gloom wall ew     67 Gloom wall ns      9 Gloom wall corner    1 Gloom wall post
   86 lair wall ew      34 lair wall ns       4 lair wall corner     2 lair mouth arch (proposal)  5 lair mouth webs (proposal)
   22 Stacks bookcases  72 crystal cluster   27 root mass logs       6 root mass brambles/vines   2 crawlway rocks
   44 web mass pillars  30 web mass webs      9 web mass small webs 18 web pillar pillars  13 web pillar webs  3 web pillar small webs
   26 Warren stalagmites 6 Warren rubble     48 Warren hay          10 Warren bones
    9 Brood Pit stalagmites                  49 Brood Pit hay       10 Brood Pit bones
   93 Tangle mushrooms  11 Tangle fallen logs 8 Tangle vines
   25 Dawnseam crystal  15 Dawnseam crystal by the rock  7 Dawnseam ice mushrooms
   27 Gloom webs        10 Gloom hanging webs 12 Gloom bones        76 lair webs  8 lair hanging webs  2 lair egg cases  19 lair bones
```

Land: 11,320 tiles written (the same tiles as round 1, every old value 0x0244 Z 0); rings 299 Warren, 100 Brood
Pit, 178 Tangle, 176 Dawnseam; 629 ramp tiles at +12; 462 void at +20. Build: `--fresh` restored the three scratch
files (hashes 872269bb, 2109d96b, d7ae4bfc as `ORIGINAL-SHA256.txt`), then `verify: land mismatches 0; statics
round-trip True (1397 read back)`.

## 3. The renders

`notes\art\rootdeep-build\index.html`, the question at the top, round 1 and round 2 of the Vault side by side, then
the walls check, the proposals, the overview and the eight zones (same names and rectangles as round 1).

| Picture | Tiles / what | KB |
|---|---|---|
| overview.png | 144 x 168 top-down, radar colours, 4 px a tile | 9 |
| landing, vault, warren-west, warren-east, tangle, dawnseam, gloom-west, gloom-east | the round 1 rectangles, isorender | 480-1,016 |
| walls-check.png | 3 sets x (5 x 5 test, L test, OSI map room, OSI house multi) + the built rooms in each set | 813 |
| lair-mouth-check.png | (a) 3 open with the arch halves at 1246 and 1249, (b) OSI's 2-tile doorway, the built mouth | 158 |
| proposal-stacks.png, proposal-doorway.png, proposal-cavering.png | crops from the zone renders | 55, 39, 132 |

OSI comparison rooms in walls-check: Deceit (Trammel 5184-5191 x 535-546, 5188-5200 x 556-570), Nujel'm
(3672-3696 x 1231-1247, roofed) and the large marble house multi 0x96 (roof left off), Terathan Keep (5467-5479 x
3128-3140, two storeys) and the tower house multi 0x7A (roof left off). The test rooms are built by the same
`wall_pieces()` as the map and look like the OSI rooms: continuous runs, the corner on the SE, the post on the NW.
The two renderers agree on OSI's Deceit room (vseUOAware's fixed build at `bin\P180` against isorender; its old build
is the one in `round1\`). Largest file in either repo: `terathan-keep-5424-5479.png`, 1.4 MB.

What the pictures still cannot show: lighting and hues (none in map statics here), and the land texture under a
flat tile is its art diamond, as the client draws it.

## 4. Tests and gates (each seen red first)

No shard code, so no xUnit tests and no `build.sh`. The gates that hold this work:

| Gate | Red | Green |
|---|---|---|
| vseUOAware static offset | 1 x 1 render of Trammel 3681,1234 with the old build: 44 x **226** px (the `sy + 22` formula's prediction) | fixed build: 44 x **204** (the client's layout) |
| walkable set unchanged (`build_burrows.main`) | one floor tile dropped from `plan-cells.json`: `unchanged: False`, `AssertionError: the walkable set changed: refusing to write` | restored: `unchanged: True` on every build |
| no floor tile blocked except roomy decor (`plan` :318) | the first run of the new builder failed it on 10+ Warren edge tiles (stalagmites) before the roomy/decor accounting was wired through | passes; 100 decor tiles reported |
| every obstacle tile blocked; pillar ring tiles carry a piece | not seen red (no change was made that would trip them) | pass |
| round trip of the written files (`verify`) | P167's gate, seen red by P167 | `land mismatches 0; statics round-trip True (1397)` |

## 5. Deviations and decisions for Chase

1. **The zone renders come from `isorender.py`, not vseUOAware's `render_map_region`.** The prompt names vseUOAware
   for the research and the renders; its renderer had the half-tile bug (fixed in source, section 4) and cannot
   draw slopes or regions over 96 tiles. vseUOAware was used for the roles, the confirming reads and the cross-check;
   the pictures Chase judges needed the client's layout. If he prefers the MCP tool's output, `render_burrows.py`
   could switch back once `bin\Release` is rebuilt.
2. **`bin\Release` of vseUOAware still has the old renderer.** Two running server processes held it locked during the
   build; the fix is in `bin\P180\`. Rebuild with `dotnet build -c Release` in `D:\UO\tools\vseUOAware` when no
   session has the server open (`.mcp.json` points at bin\Release).
3. **The lair arch over a 3-tile mouth** (proposal 2): OSI's stone doorway pair spans 2 tiles. Keeping the approved
   3-tile mouth open puts the jamb half one tile further south and leaves the arch top open in the middle (picture
   (a)); the OSI pattern (b) would close 5183,1248. The map carries (a); the choice is Chase's. The mockup's "arch"
   swatch 0x01E6 is impassable (an arcade pier), so it cannot be the mouth.
4. **Impassable decor on 100 floor tiles** (26 + 9 stalagmites, 6 rubble, 40 loose crystals, 7 ice mushrooms, 12
   fallen-log pieces...; round 1 had 61). Each has three open sides in a room at least 6 wide and is off every
   spawner home and path; the floor plan is unchanged. If "walkable tiles stay walkable" means none at all, set the
   impassable rules' density to 0 in `plan-sets.json` and rebuild.
5. **The light stone tiles 0x043C-0x043F in the Gloom** are the same "stone" family at 6 percent; the first render had
   them at 15 and they read as scattered pale squares, so they were cut. Weights are Chase's to tune.
6. **The visible room is one tile larger to the south and east than the walkable floor, and a pillar one tile smaller
   to the north and west**, for every UO wall ever built (rule 3 of the research). The Strongroom pillars therefore
   look 2 x 5 over a 3 x 6 block. Not a defect; said here so nobody "fixes" it.
7. **`plan-sets.json` changed meaning** (rules in, record out as `plan-cells.json`), because the prompt asked for the
   seeds and rules in that file. P167's note refers to the old meaning.
8. **CHANGELOG skipped**: no code a player or staff member runs changed (tools under `notes\`, a tool outside both
   repos). `tools\progress.py --dry-run` ran; counts unchanged (1094 customization files, 106 patches, 1012 tests).
9. The research write-up puts the evidence from house multis (`MultiData.LoadUOP` format, `MultiData.cs:88-116`)
   beside the map dumps; no ModernUO behaviour was changed or asserted.

## For Chase

1. Open `notes\art\rootdeep-build\index.html`. **Approve these renders, or say what to change.** Look first at the
   Vault side by side, then `walls-check.png` (our test rooms beside OSI's), then the four "shown, not approved" items:
   bookcases or counters in the Stacks; lair mouth arch (a), (b) or none; cave rings as they are; no door on the Vault
   doorway.
2. Weights, cluster sizes and seeds are in `notes\cc-P167-tools\plan-sets.json`; a rebuild is
   `python -P build_burrows.py D:\UO\cc-p167-work\scratch-client --fresh` then `python -P render_burrows.py <the same>`,
   about 20 seconds together.
3. When no Claude session is open, rebuild vseUOAware (`dotnet build -c Release` in `D:\UO\tools\vseUOAware`) so the
   MCP tool's renders stop drawing statics half a tile high.
4. After approval the `-cont-` prompt still does P167 sections 2 and 3: the way in from Old Haven, the skeleton and
   crier spawners, the real map write, the package and the test shard.

## Repo size

No file over 5 MB in either repo: the largest new file is `notes\art\wall-research\terathan-keep-5424-5479.png` at
1.4 MB; `notes\art\rootdeep-build\` is 13 MB over 26 files including round 1. Scratch (the 257 MB client copy,
renders in progress) stays in `D:\UO\cc-p167-work\` and the session scratchpad, outside both repos; `__pycache__`
folders deleted (ignored anyway, `.gitignore:20`).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo    Result
----    ------
code    clean
docs    dry run
scripts clean
```

The docs repo's pending files: the 16 modified or renamed files under `notes\` (the zone renders, index, builder,
renderer, CSVs, `vse.py`, `plan-sets.json` to `plan-cells.json`) and the new ones (`round1\`, `walls-check.png`,
`lair-mouth-check.png`, three proposal crops, `notes\art\wall-research\`, `notes\cc-P167-tools\wall-research\`,
`isorender.py`, the new `plan-sets.json`, `notes\uo-wall-orientation.md`, this note).

P180 PAUSED: renders for Chase
