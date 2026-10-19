# How UO walls are oriented: the rules, measured on OSI buildings

cc-P180, 2026-10-19. Written for every future build (Old Haven's hole, guild halls, the dungeon) so walls come out
right the first time. Everything here was measured on the stock client files (`D:\ShatteredLegacy\client-data\classic-client-7.0.117.0`:
Trammel's map and statics, tiledata.mul, MultiCollection.uop, art) and checked against the client's draw code
(TazUO, `D:\UO\cc-p40-work\tazuo-3212623f\src`). Nothing here comes from memory or a forum. The dumps and the scripts
that made them are in `notes\cc-P167-tools\wall-research\` and `notes\art\wall-research\` (ASCII grids, per-tile
listings, art footprints, renders of each building).

## Headlines

1. **A wall piece's art stands on its own tile's near edges: the south edge or the east edge**, never the north or
   west. The piece whose art fills the left half of its 44 px cell stands on the south edge and runs along x (east-west);
   the one filling the right half stands on the east edge and runs along y (north-south). Measured on the art of 25
   pieces (section 4) with the client's draw offsets (section 5), and it is the only reading that agrees with where
   OSI puts each piece (section 2).
2. **So a room's walls are**: the east-west piece on the ring row north of the floor and on the ring row south of it;
   the north-south piece on the ring column west and on the ring column east; a **post** on the north-west corner tile;
   the **east-west piece** on the north-east corner tile; the **north-south piece** on the south-west corner tile; the
   **corner piece** (both slabs) on the south-east corner tile. The same four pieces close T-junctions and L-shapes
   (section 3). Every OSI building and house design read here does exactly this, including the four corners.
3. **The visible room is the walkable floor plus the south ring row and the east ring column.** Those tiles carry the
   wall items (impassable) but their slabs stand on their far side, so the player sees floor there and cannot step on
   it. Every UO house has this strip along its south and east walls; a solid block (a pillar) comes out one tile
   narrower and shorter than its impassable footprint for the same reason.
4. **P167's builder did two things wrong**, both from one assumption (that the art sat on the north and west edges): it
   used the east-west piece on north-south runs and vice versa, which draws every run as a saw-tooth of short slabs,
   and it put the corner piece on the north-west corner and the post on the south-east, the reverse of OSI. Its ring
   logic (which tiles carry a piece) was right.
5. **vseUOAware's isometric renderer drew every static half a tile too high** (art bottom at the land diamond's centre
   instead of its bottom), which is why round 1's renders and P167's "art check" could not settle the question. Fixed
   in our copy (`D:\UO\tools\vseUOAware\MODIFIED.md` item 7); `notes\cc-P167-tools\isorender.py` draws with the client's
   layout and sloped land.
6. The piece ids for our three sets, confirmed on OSI buildings:

   | Set | east-west (south edge) | north-south (east edge) | corner (both) | post | window E-W / N-S | doorway arch E-W / N-S |
   |---|---|---|---|---|---|---|
   | dungeon | 0x0241 | 0x0242 | 0x0243 | 0x0244 | - | 0x0245 + 0x0246, lintels 0x0247 / 0x0248 (passable), jambs 0x0249, 0x024A |
   | marble | 0x00F9 | 0x00FA | 0x00F8 | 0x00FB | 0x00FC / 0x00FD | marble arches 0x0113-0x0116 (not read in detail) |
   | Terathan stone | 0x01D0 | 0x01D1 | **0x01CF** | 0x01D2 | 0x01D3 / 0x01D4 | 0x01D6 + 0x01D7 / 0x01D8 + 0x01D9 (section 3.4) |
   | plaster (small stone house) | 0x0203 (0x0205, 0x0200 variants) | 0x0204 (0x0206, 0x0201) | 0x01FF | 0x0202 | 0x0208 (N-S) | - |

   P167 said the stone set had no corner piece; it is 0x01CF, one id below the run. These are recorded as DRAFT roles
   in `D:\UO\tools\vseUOAware\TileRoles.txt` (and the bin copies) so the tool and later sessions know them.

## 1. What was read

Six buildings on the stock map plus five house designs, every static dumped (id, x, y, z) with P134's fixed map
reading (`uodata.py`: UOP chunks by name, cell order `(y & 7) * 8 + (x & 7)`), the wall-flagged pieces drawn as a
letter grid, and each rendered. Terathan Keep and Deceit were also read through vseUOAware (`inspect_map_coordinate
5184,539 facet 1`: land 0x0244, static 0x0243 Z 0; `get_item_tile 0x41CF`: "stone wall", Wall|Impassable|NoShoot),
and the piece flags through `get_item_tile`; the full dumps are my scripts because the tool prints one tile at a time.

| Role in the brief | Building | Where | Set | Files |
|---|---|---|---|---|
| small house | small stone house, house multi 0x0064 (7 x 7, 5 x 5 floor) | MultiCollection.uop | plaster 0x01FF-0x0208 on a stone foundation | `house-small-stone-0x64.png`, `house-multis-grid.txt` |
| large stone building | Terathan Keep | Trammel 5416-5479, 3108-3147 (two storeys, walls at Z -60 and -40) | stone 0x01CF-0x01EB | `terathan-keep-5424-5479.png`, `terathan-keep-grid.txt` |
| large stone building, house | tower, multi 0x007A (16 x 14, interior walls, two arched doorways, two doors) | MultiCollection.uop | stone, the same set | `house-tower-0x7A.png` |
| L-shaped / not a rectangle | Nujel'm's marble hall with its south corridor and lower hall | Trammel 3672-3696, 1231-1287 | marble 0x00F8-0x0116 | `nujelm-marble-3672-3696.png`, `nujelm-grid.txt` |
| interior wall | large marble house, multi 0x0096 (west room walled off at x 0); large patio house, multi 0x008C (interior N-S wall at x 1) | MultiCollection.uop | marble; plaster 0x0133-0x013B | `house-large-marble-0x96.png`, `house-large-patio-0x8C.png` |
| dungeon room | Deceit, the room at 5184-5191 x 535-546 and the rooms around it | Trammel 5178-5212, 526-577 | dungeon 0x0241-0x024A | `deceit-room-5184-5191.png`, `deceit-rooms-5178-5212.png`, `deceit-grid.txt` |
| marble building | Nujel'm (above) and the marble house multi | | marble | as above |
| Terathan Keep room | the Keep's north-west room, floor 5425-5443 x 3113-3119 at Z -60 | Trammel | stone | as above |
| extra: brick and wood | West Britain Bank and the houses round it | Trammel 1415-1474, 1680-1724 | brick 0x0033-0x0043, wood 0x0006-0x0019, 0x00A6-0x00C1 | `britain-bank-1420-1456.png`, `britain-grid.txt` |

No map editor is on this PC (no UOFiddler, CentrED or Pandora's Box under Program Files or D:\UO), so their wall
templates were not read; the house multis stand in for them, which is better evidence anyway (they are OSI's own
templates).

## 2. The rules as observed, with the evidence

Coordinates are tile x,y; "row" means constant y (an east-west line), "column" constant x (north-south).

### 2.1 Which piece goes on which line

| Where | Piece | Evidence |
|---|---|---|
| a row (east-west run) | 0x01D0 | Terathan Keep row 3112, x 5425-5440 (Z -60); the tower multi row y -7, x -6..8, all 0x01D0 |
| a column (north-south run) | 0x01D1 | Keep column 5444, y 3113-3119; the tower multi column x -7, y -6..6, all 0x01D1 |
| a row | 0x00F9 | Nujel'm row 1234, x 3675-3682; the marble house multi row y -7, x -6..0 (with 0x00FC windows) |
| a column | 0x00FA | Nujel'm column 3687, y 1232-1235; the marble house column x -7, y -6..6 (with 0x00FD windows) |
| a row | 0x0241 | Deceit row 535, x 5185-5191; row 528, x 5170-5208 |
| a column | 0x0242 | Deceit column 5191, y 536-546; column 5184, y 536-538 |
| a row / a column | 0x0203 / 0x0204 | the small stone house multi: rows y -3 and 3 are 0x0203 and 0x0205, columns x -3 and 3 are 0x0204 and 0x0206 |
| a row / a column | 0x0007 / 0x0008 (wood), 0x0034 / 0x0035 (brick) | Britain: `xgggtggggt` rows and `e` columns in `britain-grid.txt` |

So the first id of each pair (0x00F9, 0x0241, 0x01D0, 0x0007, 0x0203) is the **east-west** piece and the second the
**north-south** piece. In every set the order is corner, east-west, north-south, post (marble 0x00F8-0x00FB, dungeon
0x0241-0x0244, stone 0x01CF-0x01D2, plaster 0x01FF-0x0204 with its variants in between).

### 2.2 Which side of the floor the pieces sit on: all four sides, on the ring tiles

The Keep's north-west room: floor x 5425-5443, y 3113-3119 (dark pavers at Z -60). Pieces on **row 3112** (north
ring), **row 3120** (south ring), **column 5424** (west ring) and **column 5444** (east ring). Deceit: floor x
5185-5190, y 536 down; pieces on row 535, column 5184 and column 5191. The small stone house: floor x -2..2, y -2..2;
pieces on rows -3 and 3 and columns -3 and 3. The wall tiles are the ring of non-floor tiles touching the floor, on
every side. (That part P167 had right.)

Which edge of its tile a piece's art stands on decides how the room looks, not which tile gets a piece. Section 4
measures it: **south and east edges**. So the north ring row's slabs stand at the floor's north edge, the west ring
column's at the floor's west edge, the south ring row's one tile beyond the floor's south edge and the east ring
column's one tile beyond its east edge. The visible room is floor plus the south row plus the east column.

```
      x0-1  x0 ........ x1  x1+1            . floor      # wall tile      = slab on the tile's south edge
y0-1    P   =  =  =  =  =   =               | slab on the tile's east edge
y0      |   .  .  .  .  .   #|              P post (the NW corner tile; its slabs would be outside the room)
 .      |   .  .  .  .  .   #|
y1      |   .  .  .  .  .   #|              visible room: x0 .. x1+1 by y0 .. y1+1
y1+1    |   #= #= #= #= #=  #=|             walkable:     x0 .. x1   by y0 .. y1
```

### 2.3 Corners, posts, line ends, T-junctions

| Case | Piece | Evidence |
|---|---|---|
| north-west outer corner | post | marble house (-7,-7) 0x00FB; tower (-7,-7) 0x01D2; small stone house (-3,-3) 0x0202; Deceit (5184,535) 0x0244 and (5169,528); Keep (5424,3112) carries 0x01D0 instead (a stub, harmless) |
| north-east outer corner | the east-west piece | marble house (0,-7) 0x00F9; tower (8,-7) 0x01D0; small stone house (3,-3) 0x0200 (an E-W variant with the end face drawn); Deceit (5191,535) 0x0241; Keep (5479,3112) 0x01D0 |
| south-west outer corner | the north-south piece | marble house (-7,3) 0x00FA; tower (-7,6) 0x01D1; small stone house (-3,3) 0x0201 (an N-S variant); Deceit column 5184 continues as 0x0242 |
| south-east outer corner | the corner piece | marble house (0,3) 0x00F8; tower (8,6) and (8,-2) 0x01CF; small stone house (3,3) 0x01FF; Nujel'm (3673,1316) 0x00F8; Keep (5431,3127) 0x01CF |
| an interior N-S wall meeting the north wall from below | the east-west piece on the junction tile (the north run continues) | tower (-2,-7) 0x01D0 above its column of 0x01D1; patio house (1,-7) 0x0133 (a corner variant, same geometry) |
| an interior E-W wall meeting the west wall | the north-south piece on the junction tile (the west run continues) | tower (-7,-2) and (-7,1) 0x01D1; Keep (5424,3120) |
| an interior E-W wall meeting the east wall | the corner piece | tower (8,-2) 0x01CF; Deceit (5184,539) 0x0243 where row 539 arrives from the west at column 5184 |
| an interior N-S wall meeting the south wall, or an L's inner corner | the corner piece | tower (-2,1) 0x01CF; marble house (0,3) 0x00F8 |
| a run's free end | the plain piece, nothing added | Keep row 3120 ends at 5479 in the N-S column; Deceit rows end in posts or corners only where another line meets |
| a doorway (a gap in a run) | the flanking tiles keep the plain run piece | Keep column 5431: 0x01D1, 0x01D1, [doorway], 0x01CF; Deceit row 543 around its arch |

The general rule behind all of these, in terms of the two slabs: a solid tile needs its **south slab** when floor
lies directly north or south of it, or at an outer corner diagonal (floor to the SW or NW with none west or on that
side); it needs its **east slab** when floor lies directly east or west, or floor to the NE or NW with none north.
Both slabs: corner piece. Neither, with floor to the SE: post. That is `wall_pieces()` in
`notes\cc-P167-tools\build_burrows.py`, and the test rooms in `notes\art\rootdeep-build\walls-check.png` are built
by it next to the OSI rooms.

### 2.4 Doorways and windows

- Windows are plain run pieces with a window drawn: 0x00FC on rows, 0x00FD on columns (Nujel'm column 3675, y
  1235-1244; the marble house row -7), 0x01D3 on rows, 0x01D4 on columns (Keep).
- A Terathan stone doorway is two pieces over a **two-tile gap**: east-west `0x01D6, open, 0x01D7` reading west to
  east (Keep 5436-5438, 3131; tower -5..-3, 1); north-south `0x01D8, open, 0x01D9` reading north to south (Keep column
  5431, y 3132-3134 and column 5441, y 3127-3129). The first piece (passable by tiledata) sits on the first open
  tile and draws the arch's near half; the second (impassable) sits on the wall tile after the gap and is the jamb
  with the far half. 0x01E6 and 0x01E7 (the mockup's "arch") are both impassable: an arcade pier, not a doorway.
- A dungeon doorway is wider: `0x0245, 0x0247, 0x0247, 0x0246` across row 543 in Deceit, the middle lintels passable
  (no Impassable flag, no art in the bottom 44 rows), so a dungeon arch can span any width.
- Doors (0x0675, 0x0677, 0x06A5...) sit on the wall tile of the run, in place of the run piece (the small stone house
  (0,3); the tower (3,-2), (0,6), (1,6)).

### 2.5 A building that is not a rectangle

Nujel'm's hall (`nujelm-grid.txt`, rows 1231-1255): the main hall x 3672-3696 is closed by rows 1231 and 1247 and
columns 3672 and 3696; its south corridor x 3683-3687 continues through the south wall, which simply stops at 3682 and
restarts at 3688 (row 1247 `************fff**********`: the f's are 0x0105 pieces of the corridor's own north wall
turn), the corridor's columns 3683 and 3687 run on south, and the lower hall opens from it. Every line is a run along
one axis; where the outline turns, the tile where two runs meet takes the corner piece or the post by the table above.
**No OSI wall steps diagonally**: a diagonal outline is drawn as axis-aligned runs with a corner at every turn. (P141's
layout is all rectangles, so the Burrows have no such turn to straighten; checked on the layout grid.)

## 3. Tiledata, and how house designs place walls

Every piece in the three sets is `Wall|Impassable|NoShoot|ArticleA`, height 20 (marble, stone) or 22 (dungeon); the
corners and posts add `Unknown3`. Windows add `Window|LightSource`, drop NoShoot. Passable arch halves lack
Impassable. Tiledata says nothing about the edge: the art and the usage do.

The house multis (MultiCollection.uop, read as pinned `MultiData.LoadUOP` does: `Projects/Server/Client/MultiData.cs:88-116`,
records of id, x, y, z, flags, cliloc count) place walls by exactly the rules above; the tables in section 2 cite
them tile by tile. `house-multis-grid.txt` holds the five designs as letter grids per Z level.

## 4. The art footprints (which edge the slab stands on)

`art-footprints.txt`, made by `art_measure.py` from the unpacked art.mul: for each piece, the leftmost and rightmost
lit pixel per row from the bottom, relative to the cell's centre column. Every static's art is drawn centred on its
tile and with its bottom row on the land diamond's bottom corner (section 5), so the bottom rows of the art say
where the base sits:

| Piece | rows 4, 12, 24 from the bottom (left..right, centre 0) | base runs | edge |
|---|---|---|---|
| 0x00F9, 0x0241, 0x01D0, 0x0007, 0x0203 | -5..+4, -13..+3, -22..+3 | from the bottom corner up-left to the left corner | south |
| 0x00FA, 0x0242, 0x01D1, 0x0008, 0x0204 | -4..+4, -4..+12, -4..+21 | from the bottom corner up-right to the right corner | east |
| 0x00F8, 0x0243, 0x01CF, 0x01FF, 0x0006 | -5..+4, -13..+12, -22..+21 | both | south and east |
| 0x00FB, 0x0244, 0x01D2, 0x0202 | -4..+3 all the way up | a post on the bottom corner | the SE corner point |

The diamond's bottom corner is the tile's south-east corner point (x+1, y+1); its left corner is (x, y+1) and its
right corner (x+1, y). A base from the bottom corner to the left corner is the edge y+1, the south edge; to the
right corner, the edge x+1, the east edge. P167 read the same halves but placed them on the far edges (left half =
west edge), which is the one assumption all its errors came from.

## 5. The client's layout, and the renderer bug

TazUO (`src/ClassicUO.Client/Game/GameObjects/Views/View.cs:137-157`): `TILE_CENTER_OFFSET = 22`,
`TILE_HEIGHT_OFFSET = 44`; a static is drawn at `x - (width / 2 - 22)`, `y - (height - 44)`, and land at `(posX, posY)`
with its 44 x 44 diamond (`LandView.cs:93`). So the art's bottom row lands on the diamond's bottom corner.
vseUOAware (`Tools/MapEditorTools.cs:62`) used `sy + 22 - height`: half a tile high. Proof: a 1 x 1 render of Trammel
3681,1234 (land Z 0; 0x00F9 at Z 20, a marble floor at 20, a roof at 40) came out **226 px** tall, the number the
`+22` formula predicts; the client's layout gives **204**, and the fixed build (`bin\P180\`) renders exactly 204.
That bug is why P167's reference renders and its own art check could not be trusted, and why round 1's walls looked
wrong even where the piece was right. `isorender.py` uses the client's formula and also draws sloped land from the
texmaps, so cave rings no longer show black seams.

## 6. What P167's builder did wrong, and why the saw-tooth

1. It defined its "W" piece (0x00F9, 0x0241, 0x01D0) as "fills the left half, so stands on the west edge, so goes
   where floor is east or west", and its "N" piece the other way round. Left half means the **south** edge, so every
   north-south run got the east-west piece: each tile drew a short slab along x, stepped one tile along y from the
   next: the saw-tooth in `round1\vault.png`. Every east-west run got the north-south piece, the same saw-tooth the
   other way.
2. Its corner rule put the corner piece where both conditions held, which with the swapped pieces and its diagonal
   clauses landed on the **north-west** corner, and the post where only the NW diagonal was floor, the **south-east**
   corner: the reverse of OSI.
3. It gave the stone set no corner (it used both run pieces on one tile); the corner is 0x01CF.

The fix is one function (`wall_pieces`) and the piece table in `plan-sets.json`; the ring logic and the land under
the walls stayed.

## 7. Checklist for any builder

1. Wall tiles are the ring of non-floor tiles touching the floor (8 neighbours), on all four sides. Openings are
   floor tiles that demand no slab from their neighbours.
2. Floor north or south of the tile: the **east-west** piece (first id after the corner). Floor east or west: the
   **north-south** piece (next id). Both: the **corner**. Only floor to the south-east: the **post**. Outer corners:
   NE takes the east-west piece, SW the north-south piece, SE the corner, NW the post.
3. Expect the room to look one tile wider to the east and one deeper to the south than it walks; expect a pillar to
   look one tile smaller to the north and west than its impassable block. Size the floor rect for the walk, not the look.
4. Put floor land (or floor statics) under every wall tile; the south and east ring tiles show it.
5. Doorways: a 2-tile gap for the stone or marble arch pairs (passable half on the first open tile, jamb on the wall
   tile after); any width for the dungeon arch with its passable lintels; a door item replaces the run piece.
6. Render with `isorender.py` (or vseUOAware's fixed build) before showing anyone; the old vseUOAware build and
   radar-colour pictures cannot show whether a wall is right.
7. Never a diagonal: step the outline in axis-aligned runs with a corner or post at each turn.

## 8. Not verified here

- No client was run this session; the rules rest on the art, the client's draw formula and OSI's own placement, all
  three agreeing. A walk through the test shard after the map lands will show the "visible strip" of item 3 directly.
- The marble arch pieces (0x0113-0x0116) and the dungeon jambs (0x0249, 0x024A) were seen in use but their exact
  doorway pattern was not reduced to a rule.
- The Keep's outer NW corners carry 0x01D0 rather than a post; both draw a closed corner, OSI itself is not uniform there.
