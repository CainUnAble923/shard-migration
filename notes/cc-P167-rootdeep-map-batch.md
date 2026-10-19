# cc-P167: Rootdeep Burrows 4 of 4: the map batch (walls, floors, the way in from Old Haven)

2026-10-18. Prompt: `D:\UO\cc-prompts\cc-P167-cont-rootdeep-map-batch.md`. Continues P24 (batch 5), P36, P139 to P141.
Two sessions: the first built the scratch map and the renders and was closed before it wrote this file; the second
(this one) checked its work, moved the reference renders out of the repo, and wrote this.

## Headlines

- **Paused at the renders stop, as the prompt says.** The Burrows are built into a scratch copy of Trammel outside both
  repos; the real map and statics files are untouched. Chase's question is at the top of
  `notes\art\rootdeep-build\index.html`: approve the renders, or say what to change. Sections 2 and 3 of the prompt (the
  way in from Old Haven, the skeleton and crier spawners, the real map) wait for that answer and the `-cont-` prompt.
- **Built as P141's spec and the mockup's first set per zone, all stock EA tiles.** 8,559 floor tiles (the spec's
  8,555 plus the doorway's two and the crawlway's two, which the spec counted as wall), 1,614 wall tiles (1,618 minus
  those four), 272 solid tiles exactly, 11,320 land tiles written, 1,198 statics placed, 0 removed. Nothing new is
  registered in `registry.csv`: no third-party art, so P141-D5's terms were never exercised.
- **Verified by reading the files back**, not by trusting the writer: every planned land tile matches (0 mismatches),
  every placed static reads back once (1,198 of 1,198), and the touched blocks held no statics of EA's before (P24
  section 2 said the rectangle was void; now counted).
- **Nine renders for Chase** through vseUOAware from the scratch files: one top-down overview and eight isometric zone
  pictures (none over 63 x 43 tiles). 5.2 MB in all, largest file 825 KB; no file in either repo over 5 MB.
- No tests yet: the shard facts the prompt lists (region rectangles, both teleporter ends, the excluded skeleton
  spawner, the crier's source) all belong to sections 2 and 3 and are written after approval. Nothing was built in
  Docker this session; no `sl-modernuo:cc-P167` image exists.

## 1. What was built, and where

**Scratch folder** `D:\UO\cc-p167-work\` (outside both repos; not in any `.gitignore` because nothing under it is under
a repo):

| Path | What |
|---|---|
| `scratch-client\map1LegacyMUL.uop`, `statics1.mul`, `staidx1.mul` | the copies that were edited. `ORIGINAL-SHA256.txt` beside them holds the three hashes before editing (map `872269bb…`, statics `2109d96b…`, index `d7ae4bfc…`); after: map `e5545a85…`, statics `28c1960b…`, index `66326dd0…` |
| `scratch-client\art.mul`, `artidx.mul` | classic art unpacked from `artLegacyMUL.uop` by `tools\uop2art.py`, because vseUOAware's isometric renderer reads art.mul |
| `scratch-client\tiledata.mul`, `hues.mul`, `radarcol.mul` | copies for the renderers |
| `tools\tdump.py` | prints tiledata names and flags for item and land ids (used for the table in section 4) |
| `art-check\*.png`, `sheet.png` | every wall piece rendered alone, to read which edge each piece runs along (section 3) |
| `ref-renders\p167-ref-{dungeon,marble,stone}.png` | isometric renders of OSI rooms in the three item wall sets, for comparison. Moved out of `notes\cc-P167-tools\` this session (1.1 MB each, reference only). Which OSI rooms they show was not written down by the first session; unverified |
| `q-vault.png`, `q-gloom-east.png` | the first session's trial renders before quantising |

**In the repo** (`notes\cc-P167-tools\`, 297 KB): `build_burrows.py` (the builder; `--plan-only` writes the CSVs and
touches no map file), `render_burrows.py` (the renders and the index page), `statics-placed.csv` (every static: x, y,
z, id, why; 1,198 rows), `land-summary.csv` (land tiles by id and Z), `plan-sets.json` (the floor, opening and wall
tile sets the builder derived from the layout).

**Inputs** (unchanged): `notes\art\rootdeep-mockup\layout.json` (P141's approved floors and solid blocks),
`D:\ShatteredLegacy\server\customizations\ClusterFRootdeepSeeder.cs` (33 spawner points, the arrival 5193,1138, the
ankh 5206,1136) and `...\Regions\RootdeepVault.cs` (doorway 5179,1137; landing spot 5182,1137; crawlway mouth
5160,1159 and exit 5160,1163), read by `build_burrows.py:read_points`.

### The look per zone (the mockup's first set each, Chase 10-18 11:08, P141-D8)

| Zone | Set | Floor land | Walls | Decor |
|---|---|---|---|---|
| Landing | L-A dungeon stone cave | cave 0x0245-0x0249 | dungeon wall 0x0241 (west edge), 0x0242 (north edge), 0x0243 corner, 0x0244 post | none |
| Vault | V-A marble strongroom | marble 0x0486-0x0489 | marble wall 0x00F9 (west), 0x00FA (north), 0x00F8 corner, 0x00FB post | the Stacks' two shelf rows as counters 0x0B40 (22; tiledata name "counter", impassable surface, height 6: it draws as a low wooden table); the two Strongroom pillars as marble-walled blocks |
| Warren, Brood Pit | W-A dirt burrows | dirt 0x0071-0x0078 | cave-rock land 0x025A at floor level (impassable land, as OSI's Orc Cave walls are), then +12, then void 0x0244 at +20 | stalagmites 0x08E1/0x08E4/0x08E5/0x08E7 by the walls (25), hay 0x0F34 (46) |
| Tangle | T-A rooted cave | cave 0x0245-0x0249 | cave-rock land 0x0266 (Deceit, Covetous) the same way | five root masses as 0x0266 mounds (rim at floor level, inside +12) with fallen logs 0x0CF3 on the rim (18); mushrooms 0x0D0C-0x0D16 (65) |
| Dawnseam | D-A crystal seam | crystal 0x3867-0x386A | cave-rock land 0x025A | five crystal clusters as 0x2224-0x2228 on every tile (72); loose crystals (36) |
| Gloom | G-A Terathan dark stone | stone 0x0440/0x0441 | stone wall 0x01D0 (west), 0x01D1 (north), both at a corner, 0x01D2 post | three web masses as stone pillars 0x01DA (62) under webs 0x10B8 at Z 10 (31); webs and spiderwebs 0x0EE3 on the floor (27) |
| Queen's lair | Q-A | as the Gloom | as the Gloom | two web pillars the same way; more webs (84). **No arch at the mouth** (the mockup's Q-A card says "lair arch and webs"; see section 5) |
| Crawlway | C-A as built | dirt | the two tunnel tiles 5160,1160-1161 carry rocks 0x1367 (impassable, height 2); `RootdeepCrawlway` moves a credited player past them | |

Every floor is Z 0, so the Vault's doorway, landing spot and crawlway points in `RootdeepVault.cs` and the seeder's
`GetAverageZ` reads all land on Z 0. Openings (the three Vault gaps, the Thicket and Seam Heart gaps, the lair mouth,
the doorway, the crawlway: 18 tiles, listed in `plan-sets.json`) are floor with no wall piece on their neighbours
along the wall line, as a house door tile is.

### Counts against the spec (P141 section 3: 8,555 floor, 1,618 wall, 272 solid)

`python -P build_burrows.py <scratch> --plan-only` prints `stats {'floor': 8539, 'openings': 18, 'walls': 1614,
'obstacles': 272, 'land_tiles': 11320, 'statics': 1198}`. `floor` there excludes the 18 openings and the 2 crawlway
tiles, so the walkable floor set is 8,559: the spec's 8,555 plus the doorway (5179,1137-1138) and the crawlway
(5160,1160-1161), which `layout.json` holds as wall tiles and the builder makes floor land (the doorway) and rock-covered
floor land (the crawlway). The wall set is the 1,618 less those same four. Solid tiles match exactly. The statics by
reason, from the same run:

```
   299 Warren cave ring      100 Brood Pit cave ring     178 Tangle cave ring      176 Dawnseam cave ring
   629 cave ramp +12         462 void raised +20   (land, not statics; counted in land_tiles)
   130 Vault wall north edge  85 Vault wall west edge    17 Vault wall corner       1 Vault wall post
    48 Landing wall north     44 Landing wall west        4 Landing wall corner     1 Landing wall post
   163 Gloom wall north       67 Gloom wall west         18 Gloom wall corner       1 Gloom wall post
    86 lair wall north        35 lair wall west           8 lair wall corner
    22 Stacks counters        62 web mass pillars        31 web mass webs           2 crawlway rocks
    72 crystal cluster        36 Dawnseam crystal        18 root mass fallen log   65 Tangle mushrooms
    18 Warren stalagmites      7 Brood Pit stalagmites   31 Warren hay             15 Brood Pit hay
    27 Gloom webs             84 lair webs
```

Land written: 11,320 tiles, x 5140-5245, y 1131-1261, all east of the mockup's build line (x 5140) and inside the
area. `land-summary.csv` has the per-id figures (for example 0x0244 void at +20: 462; 0x025A at 0: 575 and at +12: 629).

### Statics removed: none

`write_statics` rewrites each touched block by appending the existing rows plus the new ones at the end of
`statics1.mul` and repointing `staidx1.mul`, keeping whatever a block already held. The read-back count of every static in the touched blocks
(1,198) equals the placed count, so those blocks held nothing of EA's before: nothing was kept or dropped. The old land
values are printed by the builder as it writes (void 0x0244 everywhere, per the first session's run; this session did
not rewrite, so that line is not reproduced here).

## 2. Verification (this session, from the files)

```
land mismatches 0 ; statics round-trip True ; statics read back in touched blocks 1198 ; planned 1198
spawners 33 ; land extent 5140-5245, 1131-1261
```

`build_burrows.verify` re-reads the UOP map through P36's `uodata.uop_by_name` (P134's fixed reader: cell order
`(y & 7) * 8 + (x & 7)` as pinned `TileMatrix.GetLandTile` reads it) and the statics through
`uodata.load_statics_index` / `block_statics`, and compares every planned tile.

## 3. Wall orientation (the art check)

Measured from the art, not assumed: a wall piece whose pixels fill the left half of its 44 px tile runs along the
tile's west edge (0x00F9, 0x0241, 0x01D0); one filling the right half runs along the north edge (0x00FA, 0x0242,
0x01D1); 0x00F8, 0x0243 fill both (outer corner); 0x00FB, 0x0244, 0x01D2 are posts. `notes\cc-P167-tools\wall-art-sheet.png`
shows the fifteen pieces side by side. The stone set has no single corner piece in 0x01D0-0x01D2, so a Gloom or lair
corner carries both 0x01D0 and 0x01D1 on one tile; the marble and dungeon sets have one (0x00F8, 0x0243). The rule
in `build_burrows.py:plan` step 3: a north-edge piece where the tile south or north is floor, a west-edge piece where
the tile east or west is floor, a corner where both, a post at an outside corner that touches floor only diagonally.
This is what the renders show (every room closed, every opening open). Unverified: how the client lights a corner tile
carrying two pieces; the Gloom's own OSI rooms (Terathan Keep) were not inspected for that pattern.

## 4. The renders

`notes\art\rootdeep-build\index.html`, with the question at the top. Made by `render_burrows.py` from the scratch
files through vseUOAware (`export_map_region_png` for the overview, radar colours, 4 px a tile, x 5120-5263, y 1112-1279;
`render_map_region` for the zones, classic art). Quantised to 256 colours (a third the size, flat art, no visible loss).

| Picture | Tiles | KB |
|---|---|---|
| overview.png | 144 x 168 top-down | 6 |
| landing.png | x 5174-5209, y 1128-1166 | 521 |
| vault.png | x 5138-5182, y 1128-1164 | 602 |
| warren-west.png | x 5140-5190, y 1158-1200 | 762 |
| warren-east.png | x 5182-5244, y 1158-1198 | 660 |
| tangle.png | x 5138-5196, y 1194-1236 | 805 |
| dawnseam.png | x 5190-5246, y 1194-1236 | 648 |
| gloom-west.png | x 5146-5201, y 1226-1264 | 659 |
| gloom-east.png | x 5190-5240, y 1226-1264 | 621 |

What the renderer cannot show, so Chase should not judge from the pictures: land textures (flat land is drawn as its
art diamond, which is also how the client draws flat land; slopes get the texture in the client), lighting, and the
slope between two land tiles of different Z. That last one is why the cave rings and the root mounds show a black
diamond-shaped seam between the floor and the +12 ring: in the client that seam is a drawn slope. The Dawnseam's
crystal land reads as pale blue ice in radar and art colours; in the client it is the Ice dungeon's crystal floor.

## 5. Deviations and decisions for Chase

1. **The Stacks' shelving is counters (0x0B40), which draw as low wooden tables.** The mockup proposed shelving; the
   spec's wording is "shelf rows". A bookcase or wooden shelf (0x0A97-0x0A9E: impassable, height 12, tiledata flags
   them as containers, so the server would need them placed as plain statics, which the map batch does) would read
   more like a vault's stacks; say which, or something else.
2. **No arch at the lair mouth.** The Q-A card says "lair arch and webs"; the mouth is three open tiles in the Gloom's
   stone wall. An arch needs a piece picked and its two sides tested in the client; it was left for the `-cont-`.
3. **The cave rings are impassable land, not items.** OSI's own caves do this (the Orc Cave reads floor Z 0 | cave 0x025A
   Z 0 | Z 10 | Z 19 | Z 26). It means no wall item to target and nothing for line-of-sight to stop except the land
   height, which the +12 and +20 rings provide beyond the first ring. If Chase wants the cave zones to block sight
   and spells like the item-walled zones do, the ring would need wall items added on top.
4. **Four tiles of floor the spec counted as wall** (the doorway and the crawlway): necessary for both to work; noted so
   the counts in P141 and here are reconciled rather than in disagreement.
5. **The Vault's doorway and the crawlway stay as P141 built them in code**: no door item, no gate. The mockup's V-A card
   mentions a metal door; nothing was placed. Say if the doorway should carry a door item (it would have to open for
   tutorial characters only, which the region already enforces at the tile).
6. **No third-party art** (P141-D5 permitted DRC1K's packs as made, and otimpyre's X-1 and X-6): the first sets are all
   stock, so none was needed and nothing is registered. X-6, the cave hole, is the natural piece for Old Haven's hole
   in section 2 of the prompt; it would be registered then as EA-derived patch records.
7. **The first session's reference renders are kept outside the repo** (`D:\UO\cc-p167-work\ref-renders\`): 3.1 MB of
   OSI rooms, reference only, and which rooms they are was not recorded. Not needed by anything in the repo.
8. **`GoLocation`** (P141-D6) is untouched; it moves with the map batch's real-map step if Chase says so.

## 6. Tests

None this session. The prompt's four shard facts (region rectangles match the built floors; the teleporter's both
ends; the skeleton spawner excluded on a fresh world; the crier's source gone) and the play-test items are the
`-cont-` prompt's, after approval; each will be seen red first then.

## 7. Repo size

No file over 5 MB in either repo. `notes\art\rootdeep-build\` is 5.2 MB over ten files, largest 825 KB
(`find ... -size +1M` finds nothing in the build or tools folders). The scratch map and statics (90 MB, 20 MB, 5.5 MB)
and the 149 MB art.mul are outside both repos in `D:\UO\cc-p167-work\`, so `git check-ignore` has nothing to prove.
`notes\cc-P167-tools\__pycache__` is ignored by `.gitignore:20` and was deleted anyway.

## For Chase

1. Open `notes\art\rootdeep-build\index.html`. **Approve these renders, or say what to change.** The things most worth
   a look: the Vault's counters-as-tables (5.1), the bare lair mouth (5.2), and whether each zone's look is what you
   pictured from the mockup. The black seams around the cave rings and root mounds are the renderer, not the map (4).
2. Once you answer, the `-cont-` prompt does the way in from Old Haven, the skeleton and crier spawners, the seeder run,
   the real map write, the package build and publish, the test shard rebuild, and the play tests.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after moving the reference
renders out and deleting `__pycache__`:

```
Repo    Result
----    ------
code    clean
docs    dry run
scripts clean
```

The docs repo's pending files: `testing\SUMMARY.md` and `testing\play-tests.json` (the play-test importer's machine
output), the ten files in `notes\art\rootdeep-build\`, the five in `notes\cc-P167-tools\`, and this note.

P167 PAUSED: renders for Chase
