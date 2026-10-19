# cc-P185: Rootdeep round 4 (junctions, wall ends, torches, arch gaps)

2026-10-19. Prompt: `D:\UO\cc-prompts\cc-P185-cont-rootdeep-round4.md`. Continues P181 (paused at its renders; Chase
10:08: "Vault looks better but... spaces next to arch ways, torches too low and bad corners in center of room", plus
the marked corners in the Landing, Warren east, Tangle, Dawnseam and both Gloom halves).

## Headlines

- **Every one of Chase's 20 marks is one of four things, and all four were rules, not tiles.** (1) Wall pieces were
  chosen from the floor beside a tile (P180's rule); OSI chooses them from the runs meeting at the tile. Measured on
  9,744 OSI wall tiles in nine dungeons and two towns, the floor rule agrees with OSI on 91.1 percent, the run rule
  on 98.0. The floor rule put a slab stub across every free end and a corner piece at every outline corner with
  floor on two sides: the tunnel mouths, the descent stubs, the lair's corners, the Strongroom blocks' corners, the
  pockets where the tunnel leaves the Landing. 23 wall tiles changed and nothing else about the walls did.
  (2) Wall torches sat at Z 0; every OSI dungeon torch stands on the floor tile in front of its wall at floor + 13
  (Deceit, Khaldun, Covetous) or + 15 (the Keep, Hythloth). Ours are at 13. (3) The marble arch rule put a pier on
  the wall tile before the gap too; a pier's base is on the far half of its tile, so half a tile of nothing showed
  between the run and the pier. OSI's bay is `wall, arch top on the first open tile, open, pier after`; that is the
  rule now, at all four Vault gaps. (4) The Strongroom blocks were rings of wall pieces with floor showing inside.
  Seven variants rendered; the walled ring with a marble floor at wall height on top reads as a solid plinth (how
  every UO building reads from above) and is built.
- **The rule, in one sentence** (`scripts\mapbuild\walls.py` `wall_role`, `notes\uo-wall-orientation.md` section 9):
  a wall tile with one wall neighbour takes its run's plain piece; two opposite, the run's piece; two adjacent, the
  corner they make (W+S ew, E+S post, N+E ns, N+W corner); three, the through run's piece plus the branch's slab
  only when the branch comes from the west or north; four, the corner. Cave rock, void and floor are not wall
  tiles. Sections 10-13 of that note cover wall ends, Ts, mixed sets, walls meeting rock, torches, arches, solid
  blocks and the junction sheet, each with the OSI tiles it rests on.
- **The junction sheet exists** (`scripts\mapbuild\junctions.py`): every wall end, L, T, cross, mixed-set join,
  wall-to-rock join and mounted torch, found from the wall layer and cropped from the scratch map with its
  coordinates, 48 to a sheet (`notes\art\rootdeep-build\junctions-1.png`, `-2.png`). 71 crops for the Burrows
  (L 27, T 8, ends 18, rock joins 8, mounts 8, mixed 2); I looked at every one before writing the page. Three new
  checklist checks fail on round 3's build and pass on this one (section 5).
- The playbook has four new mistake rows (junctions, torches, arch piers, solid blocks), three new checklist items
  and the junction sheet as item 12. No server code changed: no Docker build, no image, no CHANGELOG. The walkable
  floor, the 18 openings, the crawlway and all 1,614 wall tiles are exactly P167's (gate green). 1,595 statics of
  128 distinct ids (round 3: 1,559 of 123); the 36 new are the pillar tops; land unchanged.

## 1. Chase's marks, located (prompt: "find each red box or arrow on the map by coordinates")

The screenshots are the round 3 zone renders scaled to the window. I matched each one to its render (scale and
offset by grey-level matching, mean difference under 6 of 255 for the Vault and Landing, under 23 for the rest, where
the window cut the black border), found every red component, and converted its centre through the render's origin
and the client's layout (screen x = (x - y) * 22, y = (x + y) * 22 - 4z) to tiles; a box drawn round a wall top sits
about 1.8 tiles south-east of the floor estimate, so each candidate was checked against the wall layer and the crop.
Full-size crops of every mark, before and after, numbered as on the screenshots: `marks-<screenshot>.png`.

| Picture | Mark | Tiles | What was wrong | The fix |
|---|---|---|---|---|
| 1-vault | 1 | 5151-5153 x 1149-1154 | the west Strongroom block read as an open three-sided box | ring by the run rule (post 5151,1149; ew 5153,1149; ns 5151,1154; corner 5153,1154) and a marble floor at Z 20 on all 18 tiles |
| 1-vault | 2 | 5145,1143 | Deposit Hall to Strongroom gap: half a tile of nothing between the wall and the pier | 5145,1143 keeps 0x00F9; 0x0114 on 5146,1143; 0x0113 on 5149,1143 only |
| 1-vault | 3 | 5167-5169 x 1149-1154 | the east block, the same box | as mark 1 |
| 1-vault | 4 | 5155,1132 | Stacks to Deposit Hall gap: the pier stood half a tile off the north wall | 0x00FA at 5155,1132; 0x0116 at 5155,1133; 0x0115 at 5155,1135 |
| 1-vault | 5 | 5170,1132 | wall torch 0x0A0D at Z 0 | Z 13 |
| 1-vault | 6 | 5179,1136 | the Vault doorway: the north pier off the wall above it | 0x00FA at 5179,1136; 0x0116 at 5179,1137; 0x0115 at 5179,1139 |
| 1-vault | 7 (arrow) | 5180,1132 | the Landing torch 0x0A0C at Z 0 | Z 13 |
| 2-landing | 1 | 5191,1161 and 5196,1161 | corner pieces where the tunnel walls meet the Warren's rock: a slab stub across each end | run ends: 0x0242 (Wrong 5686,564; Khaldun 5440,1343) |
| 2-landing | 2 | 5179,1136 | the doorway pier from the Landing side | as 1-vault 6 |
| 2-landing | 3 | 5179-5180,1131 and 5180,1132 | the marble-to-dungeon join and the torch | the join is a T (walls W, E, S: ew) and was already right; the torch at Z 13 |
| 2-landing | 4 | 5191,1145 | the west stub of the tunnel mouth: a corner piece made a pocket | walls W and S: ew 0x0241 (Deceit 5215,535) |
| 2-landing | 5 | 5196,1145 | the east stub: a corner piece made a pocket | walls E and S: post 0x0244 (Deceit 5190,562) |
| 3-warren-east | 1 | 5191,1161 | the same tunnel mouth from the cave | run end, plain |
| 4-tangle | 1 | 5165,1229 and 5170,1229 | the descent's stone stubs ended in corner pieces: a slab across the top of each into the rock | run ends: 0x01D1 |
| 5-dawnseam | 1 | 5213,1229 and 5218,1229 | the same | 0x01D1 |
| 6-gloom-west | 1 | 5183,1257 | the lair's SW corner: a corner piece with a stub into the Gloom | walls N and E: ns 0x01D1 |
| 6-gloom-west | 2 | 5165/5170 x 1229, 5170,1233 | the descent's stubs at the rock and where it opens into the corridor | run ends plain; 5170,1233 (walls N, E) ns; 5165,1233 (walls N, W) keeps its corner |
| 6-gloom-west | 3 | 5183,1237 | the lair's NW corner: two stubs into the corridor and the west hall | walls E and S: post 0x01D2 (Deceit 5190,562; Khaldun 5392,1320) |
| 7-gloom-east | 1 | 5213/5218 x 1229, 5218,1233 | the Dawnseam descent's stubs | as 6-gloom-west 2 |
| 7-gloom-east | 2 | 5227,1237 | the lair's NE corner: a stub up into the corridor | walls W and S: ew 0x01D0 |

The 23 changed wall tiles (round 3 piece, round 4 piece): 5191,1145 0x0243 to 0x0241; 5196,1145 0x0243 to 0x0244;
5151,1149 and 5167,1149 0x00F8 to 0x00FB; 5153,1149 and 5169,1149 0x00F8 to 0x00F9; 5151,1154 and 5167,1154 0x00F8
to 0x00FA; 5191,1161 and 5196,1161 0x0243 to 0x0242; 5165, 5170, 5213, 5218 x 1229 and 5170, 5218 x 1233 0x01CF to
0x01D1; 5183,1237 0x01CF to 0x01D2; 5227,1237 0x01CF to 0x01D0; 5183,1257 0x01CF to 0x01D1; and the four tiles
before the Vault gaps (5145,1143; 5155,1132; 5169,1139; 5179,1136) got their run piece back in place of a pier.

## 2. Torches (prompt 1)

`mapbuild.survey` plus the map statics over Deceit, Covetous, Khaldun, the Keep, Shame, Hythloth, Despise and Wrong:
every wall torch, sconce and holder (0x09FB-0x0A0E; 150 on the map, 7 more from the decoration files) stands on a
floor tile, never on a wall tile (3 exceptions on wall tiles, all in doubled walls), facing a wall directly north
(0x0A0A, 0x0A0B, 0x0A0C, 0x0A0D, 0x0A0E, 0x0A01) or directly west (0x0A05, 0x0A07, 0x0A08, 0x0A09, 0x09FC). Z against
the land or paver under it, 16 measured: 13 at Deceit 5137,614 (-37 over -50), 5145,576, 5224,561, Khaldun 5456,1299,
5447,1320, 5479,1344, Covetous 5560,1847; 15 at Deceit 5160,564, 5167,560, the Keep 5424,3119 (-45 over -60),
5434,3132, 5433,3113, Hythloth 5912,187, 5917,80, 5960,172; 14 at Covetous 5560,1893; one Hythloth torch over a
raised cave floor. Ours: `corners.torch.z` 13 in every zone, the ids unchanged (north 0x0A0C/0x0A0D, west
0x0A07/0x0A09, both in OSI's lists). `torch-check.png`: ours before and after beside Deceit 5160,564, Khaldun
5456,1299 and 5447,1320.

## 3. Arch gaps (prompt 2)

The art (`isorender.Art`, lowest lit rows against the cell centre): 0x0113 base -11..3 (the east half of the south
edge; the full ew slab is -22..3), 0x0115 base -4..9 (the south half of the east edge; the ns slab is -4..21),
0x0114 and 0x0116 nothing in the bottom 40 rows (arch tops, passable by tiledata). Every use in Trammel (75 pieces:
Nujel'm 3675-3693 x 1231-1327 and 3732-3743, Magincia 3716-3725 x 2061-2070, 4544-4553 x 1300-1310, 6505-6515 x
178) reads `wall | arch top | open | pier` along the line, repeated for an arcade: Nujel'm row 1323: 0x0105 (3731),
0x0114 (3732), open, 0x0113 (3734), 0x0114, open, 0x0113, 0x0114, open, 0x0113 (3740); Magincia column 3716: 0x011B
(2061), 0x0116 (2062), open, 0x0115 (2064), 0x0116, open, 0x0115, 0x0116, open, 0x0115 (2070). P181 read the
Nujel'm row as `pier, arch, open, pier` because it started one tile in. `plan-sets.json` marble `frameEW.before`
and `frameNS.before` are null; the stone set already was. `arch-check.png`: both Vault gaps before and after beside
the Nujel'm row and the Magincia column.

## 4. The Strongroom blocks (prompt 3)

`pillar-check.png`, a 3 x 6 block in a marble test room seven ways: (a) round 3's ring (floor showing inside);
(b) the ring plus corner pieces on the inside tiles (a crate); (c) corner pieces on every tile (a lattice);
(d) marble columns 0x011B on every tile (a colonnade); (e) the ring over void land (a pit); (f) the ring by the run
rule with a marble floor 0x0495-0x0498 at Z 20 on every tile of the block; (g) columns on the ring with the floor
over them (a canopy). (f) is the only one where no floor shows and it is how a UO building reads from above (walls
with the next storey's floor on them; Nujel'm's hall has marble floors at Z 20 over its walls, Trammel 3681,1234).
Built: `obstacles."Strongroom pillar".top`, 36 tiles, drawn from their own seed so the Vault's corner dressing did
not re-roll (the first build re-rolled it: 7 torches and 5 candelabra instead of 6 and 7; fixed before anything was
rendered). OSI fills its own thick walls with pieces on every tile (Nujel'm 14 fully surrounded tiles of 0x0158 and
0x0167 posts; Khaldun 20 of run pieces and posts) and leaves dungeon wall interiors void; neither reads solid at
this size (variants b, c, e).

## 5. Junctions: the rule and its evidence (prompt 4)

`uo-wall-orientation.md` section 9 has the table. The measurement: for every wall tile of the dungeon, stone and
marble sets whose piece is ew, ns, corner or post in Deceit, Covetous, Khaldun, the Terathan Keep, Shame, Hythloth,
Despise, Wrong, Nujel'm and Magincia (9,744 tiles), classify each orthogonal neighbour as wall tile (carries a wall
piece within 10 Z), floor (not a wall tile, land not void or rock, or a surface over void) or other, and compare the
piece OSI placed with each rule's prediction. Floor rule (P180): 8,881 agree (91.1 percent); the misses are the
patterns in section 9. Run rule: 9,549 (98.0; Shame and Despise 100, Wrong 99.8, Hythloth 99.1, Covetous 98.9,
Nujel'm 98.7, Deceit 97.5, Khaldun 95.4, the Keep 88.3). By wall-neighbour pattern (N E S W): one wall 292 of 305;
N+S 3,986 of 4,004; E+W 4,064 of 4,067; W+S ew 175 of 182; E+S post 169 of 193; N+E ns 156 of 161; N+W corner 150
of 156; N+S+E ns 216 of 235; N+S+W corner 97 of 140; W+E+S ew 161 of 168; W+E+N corner 53 of 88; all four corner 28
of 36. The two weak T rows are branches that run between solids (inside Deceit's and Khaldun's thick walls, where
the branch's line is never seen: ns or ew there) and Khaldun's decorative posts; a branch with floor beside it is a
corner on both sides of the data, and ours all have floor beside them. I did not add that exception to the rule.

Wall ends into rock (section 10): 24 of 29 stone and dungeon run ends at rock or a cave edge end with the plain
piece (Wrong 5686,564 and 5694,563 with rock at Z 20-25 beside walls at Z 0; Khaldun 5440,1343; Despise's room cut
into rock at 5384-5389 x 678-693), three with a corner where the wall turns along the rock, two with Khaldun's
arcade posts. Mixed sets (section 11): OSI's map has 50 adjacent pairs of its two dungeon bricks in Deceit, always
run piece to run piece, and nothing like marble to dungeon; ours at 5179,1131 and 5179,1145 take the Vault's set on
the junction tile with the Landing's piece next to it and the lines meet (`junction-osi.png`, the T and L crops).

How it is applied: `build_burrows.py:188-209` builds `item_walls` (every ring tile of an item zone plus the walled
pillars; cave ring tiles are rock) and passes it to `W.wall_pieces(Wt, x, y, ws)`; `walls.walls_for` does the same
with its ring. The eight Ts and 27 Ls of the Burrows are listed in `junctions-1.png`.

## 6. The junction sheet and the new checks (prompt: the checklist gets a junction sheet)

`scripts\mapbuild\junctions.py:21` `find_junctions(wall_tiles, rock_tiles, statics)` and `:64` `sheets(...)`.
71 crops for this build: L 27, T 8, ends 18, wall-to-rock joins 8 (5159 and 5161 x 1160 at the crawlway, 5191 and
5196 x 1161, 5165/5170/5213/5218 x 1229), mounts 8, mixed 2. I reviewed all 71 (and the 24 "wall along a cave ring"
crops the first version listed, which were not junctions; the tool now lists a rock join only at a free end, an L or
a lone tile with rock on a side no wall continues to). What the review found: nothing left to fix; every end is the
plain piece, every L the right one of the four, the Ts ns / ew / corner by the branch, the torches on the floor
tile before their wall. The sheet is made by `render_burrows.py` from the plan's wall layer, so it is of the same
build as the pictures.

Checklist (`scripts\mapbuild\checklist.py:115-180`, driver `notes\cc-P167-tools\checklist.py`):

| Check | Round 3's build (git HEAD) | Round 4 |
|---|---|---|
| junctions by the run-topology rule (`junction_rule`) | FAIL: 19 wall tiles differ (6 marble corners on the pillars, 7 stone corners at the descents, 4 dungeon corners at the tunnel, the lair's 3 corners, 5165,1229) | PASS, 673 wall tiles |
| torches mounted on the wall (`torches_mounted`) | FAIL: all 8 at Z 0 | PASS, 8 at Z 13 |
| frames touch the wall (`frames_touch`) | FAIL: 4 piers on the tile before a gap, 4 tiles with no run piece | PASS, 5 framed gaps |

Both the old and new run of the full table:

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
| junctions by the run-topology rule | PASS | 673 wall tiles carry the run-topology piece |
| torches mounted on the wall | PASS | 8 wall torches on the floor tile before a north or west wall, 13-15 above it |
| frames touch the wall (run piece before, pier after) | PASS | 5 framed gaps: run piece before, arch top on the first open tile, pier after |
| junction sheet to review | PASS | 71 crops: L 27, T 8, end 18, mixed 2, mount 8, rock 8 |

The build: `--fresh` restored the three files (hashes 872269bb, 2109d96b, d7ae4bfc); `verify: land mismatches 0;
statics round-trip True (1595 read back)`. The diff of `statics-placed.csv` against round 3's is exactly: 23 wall
tiles re-pieced, 4 piers removed, 8 torches re-Z'd, 36 pillar tops added; nothing else moved. Round 3's scratch map
is kept at `D:\UO\cc-p167-work\scratch-round3\` (outside both repos) for the before crops.

## 7. The renders (prompt: renders for Chase)

`notes\art\rootdeep-build\index.html`: the question at the top, the mark table and a before-and-after sheet per
screenshot (`marks-1-vault.png` ... `marks-7-gloom-east.png`, 20 pairs), the junction sheets, `pillar-check.png`,
`torch-check.png`, `arch-check.png`, `junction-osi.png` (the OSI corners, Ts, rock ends and mixed joins the rule came
from), the Vault and the Landing round 3 beside round 4, then the checks and zones as before. Round 3's pictures
moved to `round3\` (17 files). Largest file `junctions-1.png`, 1,278 KB; `notes\art\rootdeep-build\` is 35 MB over
four rounds; nothing over 5 MB in either repo (`find -size +5M`: only the ignored `notes\cc-P34-tools\town.png`).

## 8. What changed, with file:line

| File | Change |
|---|---|
| `scripts\mapbuild\walls.py:36` `wall_role`, `:77` `wall_pieces(Wt, x, y, ws)`, `:85` `wall_pieces_p180` (the old rule, kept), `:118` `walls_for` | the run-topology rule; the module docstring |
| `scripts\mapbuild\junctions.py` (new) | `find_junctions`, `summary`, `sheets` |
| `scripts\mapbuild\checklist.py:115` `junction_rule`, `:140` `torches_mounted`, `:158` `frames_touch` | the three checks |
| `scripts\mapbuild\README.md` | the two rows |
| `notes\cc-P167-tools\build_burrows.py:188-216` | `item_walls`, `Wt`, `report['wall tiles']`, `report['rock tiles']`, the pillar top with its own seed; `:375` the torch Z |
| `notes\cc-P167-tools\plan-sets.json` | marble `frame*.before` null; `torch.z` 13 in four zones; the pillar `top`, `topZ`; the `_about` text |
| `notes\cc-P167-tools\checklist.py:47-50` | the four new rows |
| `notes\cc-P167-tools\render_burrows.py` | round 4: `MARKS` (:63), `marks_sheet` (:230), `pillar_check` (:240), `torch_check` (:286), `arch_check` (:296), `osi_junctions` (:306), the junction sheets in `main`, the page |
| `notes\cc-P167-tools\statics-placed.csv`, `build-report.json` | regenerated (1,595 rows) |
| `notes\uo-wall-orientation.md` | headline 2 amended, section 2.3's general sentence marked superseded, sections 9-13 |
| `notes\map-building-playbook.md` | four mistake rows, rule 2.1, the doorway table, checklist items 9-12, the tools table, the picture set |
| `notes\art\rootdeep-build\` | round 4 pictures and index; `round3\` |

## 9. Tests and gates

No shard code changed, so no xUnit tests and no `build.sh`. Gates that held this work, each seen red before green:
the three new checklist checks (red on round 3's statics from git HEAD, section 6), the walkable gate (green both
builds), `verify` after the write, the OSI agreement measurement itself (the floor rule's 91.1 percent is the "red"
the run rule's 98.0 replaces; both numbers come from the same script over the same 9,744 tiles). The mark locations
were cross-checked against the full-size crops (every box lands on a wall tile the diff later changed, a torch, a
pier or a pillar).

## 10. Deviations and decisions for Chase

1. **The run rule replaces the floor rule everywhere**, not just at the marked tiles: 23 tiles changed, all under a
   mark. Section 2.3's case table in `uo-wall-orientation.md` was right case by case; only its general sentence was
   wrong, and it is marked superseded rather than deleted.
2. **Torches at Z 13**, the Deceit, Khaldun and Covetous value; the Keep and Hythloth use 15. One number for all
   zones; the check accepts 13 to 15.
3. **The pillar top is a marble floor at Z 20** (variant f), not corner pieces on a 2 x 2 or 3 x 3 (variants b and
   c read as a crate and a lattice). The block stays 3 x 6, impassable, the walkable set unchanged. If a flat top
   is not what you want, (d) columns or (c) the lattice are one line in `plan-sets.json`.
4. **The marble arch bay is OSI's `wall, arch top, open, pier`**, so our 2-tile gaps read `run piece, 0x0116, open,
   0x0115` and the 3-tile gap `run piece, 0x0114, open, open, 0x0113`; the arch top only ever covers the first open
   tile, as it does in OSI's arcades.
5. **Chase's 2-landing mark 3** (the marble-to-dungeon join at 5179,1131) changed nothing but the torch beside it:
   the join was already a T with the right piece. If it still looks wrong, say so; the two sets differ in height
   (20 and 22) and that is what shows.
6. **The junction tool lists a rock join only where the run cannot continue** (a free end, an L or a lone tile
   with rock beside it); the first version listed every wall tile along a cave ring (24 identical crops of the
   Vault's south wall) and those are not junctions.
7. **The two T rows at 69 and 60 percent agreement** are not an exception in the rule (section 5); our builds have
   no branch running between solids.
8. **No task-list tool was available to this session** (as in P181); the steps and their state are in this note.
9. **CHANGELOG skipped**: no code a player or staff member runs changed. `tools\progress.py --dry-run`: 1094
   customization files, 106 patches, 1012 tests, unchanged.

## For Chase

1. Open `notes\art\rootdeep-build\index.html`. **Approve these renders, or say what to change.** Look first at the
   seven mark sheets (your boxes, before and after, numbered as on your screenshots), then the pillar variants
   (f is built), then the torch and arch checks beside OSI, then the junction sheets.
2. Rebuild and re-render: `python -P build_burrows.py D:\UO\cc-p167-work\scratch-client --fresh`, then
   `python -P checklist.py`, then `python -P render_burrows.py D:\UO\cc-p167-work\scratch-client` (about 7 minutes
   together; the before crops read `D:\UO\cc-p167-work\scratch-round3`).
3. After approval the next prompt does P167 sections 2 and 3: the way in from Old Haven, the skeleton and crier
   spawners, the real map write, the package and the test shard.

## Repo size

No file over 5 MB in either repo (`find -size +5M`: only the ignored `notes\cc-P34-tools\town.png`, `.gitignore:25`).
The scratch maps (rounds 2, 3 and 4, 115 MB each) stay in `D:\UO\cc-p167-work\`, outside both repos. The mark
analysis scratch (Chase's screenshots copied, the crops, the pillar variants) is in the session scratchpad, outside
both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo    Result
----    ------
code    clean
docs    dry run
scripts clean
```

The docs repo's pending files: the round 4 pictures and index (round 3's under `round3\`), `scripts\mapbuild\`
(walls, junctions, checklist, README), the six changed files in `notes\cc-P167-tools\`, the playbook, the wall note,
this note, and the machine output in `testing\`.

P185 PAUSED: renders for Chase
