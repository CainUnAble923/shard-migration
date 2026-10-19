# Map-building playbook

Read this first before any map, dungeon, building or hole prompt. It turns cc-P167, P180 and P181 (the Rootdeep
Burrows, three rounds of renders) into rules, so the next build gets them right the first time. Five minutes; the
evidence is in the long notes it links. ASCII only, as everything in this repo.

Long notes: `notes/uo-wall-orientation.md` (walls, measured on OSI), `notes/cc-P180-cont-rootdeep-renders-round2.md`
(variety, the renderer bug), `notes/cc-P181-cont-rootdeep-round3.md` (rows, corners, frames, the OSI surveys),
`notes/cc-P167-rootdeep-map-batch.md` (the map files, the write and verify path), `scripts/mapbuild/README.md` (the tools).

## 1. Mistakes made, and the rule that prevents each

| Mistake | How it showed | Cause | Rule | Check |
|---|---|---|---|---|
| Wall pieces swapped (the along-x piece on north-south runs and vice versa), corner and post on the wrong corners | every run a saw-tooth of short slabs; rooms looked broken up (round 1) | assumed a piece's art stood on its tile's north or west edge; it stands on the SOUTH or EAST edge | a piece runs along x when it sits on the south edge, along y on the east edge; a room's NW corner takes the post, NE the east-west piece, SW the north-south piece, SE the corner piece; `notes/uo-wall-orientation.md` section 2 | build a 5 x 5 test room with `mapbuild.walls.walls_for` and render it beside an OSI room of the same set (`walls-check.png`); `checklist.walls_against_test_room` |
| The renderer drew every static half a tile too high | walls off their lines even where the piece was right, so the pictures could not settle the wall question | vseUOAware anchored art at the land diamond's centre (`sy + 22 - height`); the client anchors at its bottom | render with `scripts/mapbuild/isorender.py` (the client's layout, sloped land) or vseUOAware's fixed build (`bin\P180`, MODIFIED.md item 7); never judge walls from radar-colour pictures | a 1 x 1 render of Trammel 3681,1234 must be 204 px tall, not 226 |
| Diagonal wall runs | stair-stepped outlines | a layout drawn as diagonals | OSI never steps a wall diagonally: axis-aligned runs with a corner or post at every turn; draw layouts as rectangles | `checklist.no_diagonal_runs` (no wall tile joined only diagonally) |
| Repetitive single-tile floors and grid-placed decor | tiled wallpaper look; crystals, webs and stalagmites in neat ranks (round 1) | one tile id per floor, decor on fixed offsets | every floor draws from every stock variant of its texture by weight; decor goes down in seeded clusters with gaps, mixed sizes, random small Z where it fits, never two identical pieces side by side (`mapbuild.scatter`) | `checklist.variety`: distinct ids per category, zero identical pieces touching |
| Bookcase rows that wander | pieces stepping out of line, gaps and overlaps in the Stacks (round 2) | two facings mixed in one row: 0x0A97/0x0A98/0x0A9B have their back on the north edge (south-facing, for rows along x); 0x0A99/0x0A9A/0x0A9C on the west edge (east-facing, for columns along y) | one facing group per row, one Z, flush end to end; variety only among pieces of the same size and facing; finish the ends (OSI's Lycaeum: a candelabra stand 0x0B26); measure a piece's facing from its art footprint, not its name | `checklist.rows_straight` |
| Bare corners and wall ends | empty inner corners, plain gaps (round 2) | nothing placed where the floor meets two walls; openings cut without frames | every inner corner gets at least one thing by its zone's corner rule (section 2.2); every doorway in a wall line gets the set's frame (section 2.3) | `checklist.corners_dressed`, `checklist.frames_all`; six corners before and after in `corners-check.png` |
| The spec counted doorway and crawlway tiles as wall (P141) | counts in the spec and the build disagreed by four tiles | a 2-tile doorway and a 2-tile crawlway are floor the player crosses, drawn through a wall line | openings are floor tiles that demand no slab from their neighbours; count them as floor and list them (`plan-cells.json` opening) | the gate: floor, opening and wall sets equal the record |
| A land reader that swapped x and y inside every 8 x 8 block (P36's `uodata.load_land`) | grid dumps that looked plausible but put tiles in the wrong cells; a rule derived from Khaldun came out with N/S and E/W swapped until vseUOAware disagreed | `reshape(bw, bh, 8, 8).transpose(0, 2, 1, 3)`; the cell index is `(y & 7) * 8 + (x & 7)` (pinned `TileMatrix.cs:345`), so the right transpose is `(0, 3, 1, 2)` | read land with `mapbuild.uofiles` (fixed, cross-checked against vseUOAware `inspect_map_region`); cross-check one known tile with a second reader before trusting any dump | `uofiles.MapFile.get(x, y)` against vseUOAware on one tile |
| Khaldun's cave edge tile copied onto a one-tile sloped ring | black teeth along the foot of every cave wall (tried in P181, dropped) | OSI keeps the edge tile flat and slopes the rock behind it; our ring slopes the foot tile itself, so the texture's black wedge stretches | copy an OSI pattern with its Z profile, not just its tile ids; test one room and render before applying it to a zone | `cave-foot-check.png` |
| Impassable decor on floor tiles | nothing visible, but the walk changes | a stalagmite is a wall to the pathing | impassable pieces only where the tile has 3 open orthogonal sides in a room at least 6 wide, off spawner homes, openings and paths; corner decor on floor tiles is always passable; rubble and pillars go on wall or ring tiles | the builder's floor check (asserts) and the walkable gate |
| Trusting a green build of the map | a verify step that compared the plan with itself | | write, re-read the files with a second code path, compare every tile; keep a SHA-256 of the pristine files and restore from them (`--fresh`) so a rebuild never stacks | `uofiles.verify`, `restore_scratch` |

## 2. Rules of thumb

### 2.1 Walls (full rules and evidence: `notes/uo-wall-orientation.md`)

- Wall tiles are the 8-neighbour ring of non-floor tiles round the floor, on all four sides. Floor north or south of
  a wall tile: the east-west piece (first id after the corner in every set). Floor east or west: the north-south
  piece. Both: the corner piece. Only floor to the south-east: the post.
- The visible room is the walkable floor plus the south ring row and the east ring column (their slabs stand on the
  far edge). Size the floor for the walk, not the look; a pillar looks one tile smaller to the north and west.
- Floor land under every wall tile. One wall-flagged piece per tile. A run's free end is the plain piece.
- Sets used here: dungeon 0x0241-0x0244, marble 0x00F8-0x00FB, Terathan stone 0x01CF-0x01D2 (corner 0x01CF exists).

### 2.2 Corners (P181 section 2; the OSI numbers from `survey_corners` over Deceit, Covetous, Khaldun, Terathan Keep)

OSI puts something within one tile of a third to two thirds of its inner corners (Deceit level 1 48 percent of 386:
bones, small webs, rubble, garbage, torches; Covetous 66 percent of 247: spiderwebs, debris, skulls, cots; Khaldun 38
percent of 432: rubble, braziers, skulls; Terathan Keep 59 percent of 98: rubble, torches, webs, a cocoon; Hythloth 33
percent of 195). Our rule is stricter: every inner corner gets at least one thing, most two or three.

- Item-walled rooms: on the corner floor tile only passable pieces (webs, bones, stains, a brazier 0x0E31); a wall
  torch on about a third of corners, on the north wall (0x0A0C, 0x0A0D) or the west wall (0x0A07, 0x0A09), never
  south or east (OSI: 150 of 150 torches hang on a north or west wall); on the visible strip (the wall tiles south
  and east of the corner) rubble 0x1363-0x136C, a skull, a candelabra 0x0B26 (marble) or an egg case; a column
  (marble 0x011B) or stone pillar (0x01DA) on the south-east corner tile of rooms at least 12 on both sides.
- Caves: a cluster of two or three stalagmites, rocks, roots or crystals on the ring tiles round the inner corner,
  one piece on about half the rock tips the floor wraps round. The ring stays rock at the foot; only the pieces change.
- Cobwebs high (0x10B8-0x10BB) in the Gloom and lair corners, small webs (0x0EE3-0x0EE6, 0x10D2-0x10D7) elsewhere.

### 2.3 Doorways and openings (measured on OSI, P181 section 2.3)

| Set | Gap along y (north-south wall) | Gap along x (east-west wall) | Where seen |
|---|---|---|---|
| stone | 0x01D8 on the first open tile, 0x01D9 on the wall tile after the gap | 0x01D6, then 0x01D7 on the wall tile after | Terathan Keep column 5431 y 3132-3134, row 3131 x 5436-5438 |
| marble | 0x0115 pier on the wall tile each side, 0x0116 on the first open tile | 0x0113 piers each side, 0x0114 on the first open tile | Magincia column 3716 y 2064-2070; Nujel'm row 1323 x 3737-3740 |
| dungeon | 0x0248 on the open tiles, 0x024A beside the run piece on the wall tile after | 0x0245, lintels 0x0247, 0x0249 on the wall tile after | Deceit column 5183 y 541-543, row 535 x 5209-5212 |
| cave | a stalagmite or crystal on the rock tile either end of the gap | the same | our rule (OSI caves have no door lines) |

A passage between two floors with no wall line (a tunnel mouth) is not a doorway: leave the run ends plain, as OSI does.
`plan-sets.json` `wallSets.*.frameNS / frameEW` hold these; `mapbuild.walls.opening_groups` and `frame_pieces` apply them.

### 2.4 Decor density per 100 floor tiles (OSI, decoration items included; `mapbuild.survey.survey_corners`)

| OSI room block | Set | Pieces per 100 floor tiles (floors, roofs, water left out) | What |
|---|---|---|---|
| Deceit level 1, 5128-5250 x 526-640 | dungeon | 20 (10 without the stone tables and racks) | rubble 3.7, bones 1.4, stone table 1.3, wall torch 1.0, garbage 1.0, skull 0.8, small web 0.6, skeleton 0.4 |
| Covetous, 5376-5631 x 1792-2036 | dungeon and cave | 13 | stalagmites 2.3, spiderweb 1.2, flowstone 0.9, hay 0.9, bones 0.8, skulls 0.8, debris 0.7, mushroom 0.7 |
| Khaldun, 5376-5567 x 1280-1407 | stone | 6 | rubble 1.9, brazier 0.5, skulls, sarcophagi |
| Hythloth level 1, 5900-6140 x 0-200 | dungeon | 5 | garbage 1.2, blood 0.5, chests, crates |
| Terathan Keep, 5416-5479 x 3108-3147 | stone | 17 (half of it rubble) | rubble 7.1, leaves 1.4, wall torch 1.1, webs 0.9, ferns, a cocoon |

The Burrows sit at 6 to 12 per 100 by zone (lair highest). Keep a new zone inside 5 to 12; above that reads as clutter.

### 2.5 Rows and furniture

One facing group per row, pieces touching, one Z, ends finished; rows parallel to the nearest wall with even aisles
(OSI's Lycaeum: rows three tiles apart, two floor tiles between). Measure facing from the art: a piece whose lowest
lit pixels sit right of centre has its back on the north edge (faces south); left of centre, on the west edge (faces
east). `rows_straight` in `mapbuild.checklist` holds the two bookcase groups.

### 2.6 Variety weights

Floors: the common variant 45 to 65 percent, the rest spread over every stock variant. Rings: OSI uses 0x025A for
92 percent of its rock and the variants for the rest; our rings use 45 percent plus seven variants, Chase's call for
more variety. Decor tables: three or more ids wherever a cluster can exceed two pieces (with two ids the never-two-alike
rule cannot hold), weights favouring the plain pieces 3:1 over the striking ones. One `random.Random` per zone, seeded in
the rules file; change the seed for a new layout, keep it for the same one, so a rebuild is the same map.

### 2.7 Cave rings and transitions

Floor at 0, ring rock at 0 (sloped), rock at +12, void 0x0244 at +20; the ring is the 8-neighbour ring so it is closed
at corners; the +12 and +20 rings follow at Chebyshev distance 2 and 3 (no diagonal gaps, no spikes). Audit with
`mapbuild.audit.slope_audit` (spread over 12 is a defect) and confirm a corner with vseUOAware `diagnose_land_transitions`;
`rank_transition_candidates` scores a ring tile against its neighbours (ours rank GOOD, under 25). Dirt and crystal
floors have no OSI edge tile to rock; cave floor has (0x024A-0x0259, Khaldun) but only on a flat foot (section 1).

## 3. The tools and how to use them

| Tool | General or Rootdeep | Use |
|---|---|---|
| `scripts/mapbuild/uofiles.py` | general | `MapFile(folder, facet).get(x, y)`, `load_land`, `statics_in`, `write_land`, `write_statics`, `verify`, `restore_scratch` (SHA-256 gate), `same_cells` (the walkable gate), `read_tiledata` |
| `scripts/mapbuild/walls.py` | general | `walls_for(floor, openings, wallSet)`, `concave_corners`, `convex_corners`, `visible_strip_tiles`, `opening_groups`, `frame_pieces`, `check_wall_tiles` |
| `scripts/mapbuild/scatter.py` | general | `scatter(rng, rule, eligible, ...)`, `pick_unlike` |
| `scripts/mapbuild/isorender.py` | general (needs art.mul unpacked, `MAPBUILD_ART`) | `Scene.from_map`, `Scene.from_multi`, `render`, `tile_px`, `save`; `python -P isorender.py map <folder> 1 x1 y1 x2 y2 out.png` |
| `scripts/mapbuild/survey.py` | general | `survey_corners` (OSI corner and density numbers, map plus ModernUO decoration cfg), `land_grid`, `decoration` |
| `scripts/mapbuild/audit.py` | general | `slope_audit(land)` |
| `scripts/mapbuild/checklist.py` | general | the checks of section 4 |
| `notes/cc-P167-tools/build_burrows.py` | Rootdeep | the driver: zones, rings, decor, corners, frames, the gate, `--fresh`, `--plan-only`; copy its shape for the next build, import the module |
| `notes/cc-P167-tools/plan-sets.json` | Rootdeep (the shape is general) | seeds, wall sets with frames, floor and ring weights, decor rules, corner rules, obstacle fills, proposals |
| `notes/cc-P167-tools/plan-cells.json` | Rootdeep | the walkable record the gate compares against; the first build of a new layout writes it, every later build must match it |
| `notes/cc-P167-tools/render_burrows.py`, `checklist.py` | Rootdeep | the picture set and the checklist driver |
| vseUOAware (MCP) | general; read-only tools are safe | `inspect_map_region` and `inspect_map_coordinate` (the second reader for any dump), `get_item_tile` (flags), `diagnose_land_transitions`, `rank_transition_candidates`, `test_transition_fit`, `find_tile_usage`; `render_map_region` only from the fixed build (`bin\P180`; `bin\Release` draws statics half a tile high until rebuilt). Never `set_uo_directory` at the shard's folder with a write tool in the same session |
| `D:\UO\ModernUO-pinned\Distribution\Data\Decoration\*.cfg` | general | OSI's furniture, torches and bookcases are server items, not map statics: read these before saying a room is bare |

Moved into the module by P181 (from `build_burrows.py` and P36's `uodata.py`): the uop and statics readers and writers,
the wall rule and ring, scatter and pick_unlike, the renderer, the test-room builder's wall half, plus new general
code: corners, frames, the survey, the audit, the checklist. Left in `build_burrows.py`: the zones, the ring Z
profile, the decor and corner driver, the proposals, the Rootdeep points read from the seeder and region files.

## 4. Before showing Chase anything

Run the checklist and paste its table in the notes (`python -P notes/cc-P167-tools/checklist.py`, or the next build's driver):

1. Walls against a test room: a 5 x 5 and an L in every set render beside an OSI room of that set, corners post / ew / ns / corner.
2. No diagonal runs.
3. Rows straight: one facing, one Z, contiguous, ends finished.
4. Every inner corner dressed; every doorway framed or a passage.
5. Variety: distinct ids per category, zero identical pieces touching.
6. Transitions audited: slope audit clean, one vseUOAware diagnose on a ring corner.
7. One wall piece per tile.
8. The walkable gate green (floor, openings, walls equal the record), the written files verified by re-reading.

The picture set Chase always gets, in `notes/art/<build>/index.html` with the previous round side by side: the
top-down overview; every zone; the test rooms beside OSI (`walls-check.png`); close-ups of each kind of corner and
each framed opening, before and after when there is a before; every piece of furniture in a row (the Stacks); the OSI
rooms the rules came from; and the question at the top: approve, or say what to change.
