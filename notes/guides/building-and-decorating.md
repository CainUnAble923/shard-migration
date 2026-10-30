# Building and decorating guide

Every prompt that places buildings, decoration, addons, map statics or mapops reads this first, and the build reviewer
checks the work against it. Written by cc-P734 (2026-10-29) from what Chase actually corrected on the Wakening Isle
(P718, P720, P721, P724, P725, P726, P728, P732, and the overseer's log for 10-27 and 10-28), from OSI's own house
multis and town decoration, and from what human UO decorators do. Each rule names where it came from.

Contents:

1. [The short checklist](#1-the-short-checklist)
2. [Buildings](#2-buildings)
3. [Facing](#3-facing)
4. [Heights: walkable joins](#4-heights-walkable-joins)
5. [Land](#5-land)
6. [Markers and props](#6-markers-and-props)
7. [Lessons and the existing world](#7-lessons-and-the-existing-world)
8. [Proof: renders, shots and what to leave for the reviewer](#8-proof-renders-shots-and-what-to-leave-for-the-reviewer)
9. [Learned from human builders](#9-learned-from-human-builders)
10. [What to use where](#10-what-to-use-where)
11. [Lessons from the P734 practice builds](#11-lessons-from-the-p734-practice-builds)

Item IDs are hex item (static) IDs, as `[add static 0x...` takes them. "Verified" means read from the client's
tiledata, an OSI multi, our code, or two agreeing sources; "unverified" means check it before you rely on it.

## 1. The short checklist

Before DONE, every build passes all of these. The reviewer checks them one by one.

1. Every building has four walls with **whole corners** (post at the north-west, L-corner at the south-east), a **roof
   that sits on the walls**, a **door hung in the wall line** that opens onto its own room, **windows**, a **sign that
   names it**, and a **furnished inside** that fits what it is for. Nothing stray on the roof.
2. Every wall-mounted item hangs on **its** wall, facing the walk side. Doors, beds, tables, chairs, counters and
   stairs face their room. Multi-part addons use the variant that fits the coast or path.
3. Every walkable join (bridge, dock, ramp, stair, doorstep) is **within one step at both ends**, proven by a **real
   character walking both directions**, not by the bot's teleports or the server walker alone.
4. Shores use **real surf transitions**, never a stepped sawtooth. Foliage grows in **clusters**, denser inland, and
   keeps **paths, signs, doors and NPCs clear**.
5. Places are marked with **signs**, never rune markers. Props tell their story (a hurt NPC on a bench with blood).
6. Lesson text never says "0 more"; every step **ends with the next step said plainly**.
7. Anything new **appears on an existing world by itself** (seeded on load, idempotent, upgrade in place).
8. You leave **renders, off-screen shots and `placed.md`** in `notes\cc-P<nn>-review\` (section 8).
9. You checked **What to use where** before choosing pieces, and used the best-fitting piece on disk.

## 2. Buildings

### 2.1 Place a building whole, at one base Z

**Rule:** lay a building as a whole multi (or a whole generated layout) at one base Z on flat ground. Never move it
piece by piece keeping each piece's height above the old ground.

*Why (Chase 10-28 09:15, "house is jacked up"):* P663 moved OSI's thatched cottage (house multi 0x006E) tile by tile
with `max(0, z - ground)`, so on flat ground the stone walls came out at Z 3-12, wood walls 10-19 and thatch 29-42: the
roof overhung, walls did not meet, the chimney stood apart and a chicken coop (0x4514) sat on the roof as a "small gray
structure". P720 regenerated the whole house from the multi (`notes/cc-P720-tools/gen_isle_farm.py` ->
`TutorialIsleFarmLayout.cs`): foundation 0, walls, windows and floor 7, thatch 27 and up.

Classic house levels (verified, ServUO `HouseFoundation.GetLevelZ`, and OSI multis): foundation at base, **floor at
+7**, each storey **+20** (+7, +27, +47, +67). Wall pieces are 20 high (tiledata, verified: 0x0006-0x0009, 0x0057-0x005A
all height 20). A roof starts at the top of the last wall course.

### 2.2 Walls and whole corners: the east/south rule

Verified twice: `notes/uo-wall-orientation.md` (measured on OSI buildings and TazUO's `View.cs`), and
`notes/cc-P734-tools/stair-survey.txt` (every classic house multi 0x60-0x9F read by `stair_survey.py`).

A wall set has four pieces. In OSI's house multis they always stand like this:

| Corner of the building | Piece | What it shows |
|---|---|---|
| North-west | **Post** (small pillar) | closes the gap where the two back runs start |
| The north row from the post to the **north-east corner tile**, and the south row between the corners | **"South" piece** (runs east-west, stands on the tile's south edge) | |
| The west column from the post to the **south-west corner tile**, and the east column between the corners | **"East" piece** (runs north-south, stands on the tile's east edge) | |
| South-east | **Corner** (L-shaped, both arms) | closes the front corner |

The two corner tiles people get wrong: the **north-east tile takes the "south" piece** and the **south-west tile
takes the "east" piece** (P734's first practice builds put the "south" piece at the south-west and every building
showed a stub there; the reviewer caught it). So the **post goes at the north-west and the L-corner at the south-east** (RunUO names them `NWCornerPost` and
`SECorner`; the survey found every corner piece of every multi it read in exactly those places; the one exception is a log house,
which stands a log post 0x0093 at the south-east as well). A building closed any other way shows a gap or a
doubled piece at a corner. Never place a wall diagonally. The visible room is the floor plus the south row and east
column of wall tiles; the camera looks from the south-east, so the north and west walls are the ones a player sees from
inside.

Stock sets (verified from the survey and ServUO's `walls.txt`; the order inside a set differs, so **look each ID up,
never add an offset**):

| Material | Post (NW) | South piece (E-W run) | East piece (N-S run) | Corner (SE) | Window S / E |
|---|---|---|---|---|---|
| Dark wood | 0x0009 | 0x0007 | 0x0008 | 0x0006 | (see walls.txt) |
| Light wood | 0x00A9 | 0x00A8 | 0x00A7 | 0x00A6 | 0x00BA / 0x00B9 |
| Fieldstone (thin stone) | 0x001D | 0x001C | 0x001B | 0x001A | 0x0022 / 0x0023 |
| Grey brick | 0x0036 | 0x0034 | 0x0035 | 0x0033 | |
| Light stone (stone shop) | 0x005A | **0x0058** | **0x0057** | 0x0059 | 0x005E / 0x005D |
| Weathered stone | 0x01D2 | 0x01D0 | 0x01D1 | 0x01CF | |
| Plaster | 0x012A | 0x0133 | 0x0134 | 0x0132 | |
| Sandstone | 0x0161 | 0x0159 | 0x015A | 0x0158 | |
| Marble | 0x00FB | 0x00F9 | 0x00FA | 0x00F8 | |
| Log | 0x0093 | 0x0097 | (0x0096 / 0x0091) | 0x0090 | |
| Fence (wooden) | 0x0838 | 0x0836 | 0x0837 | 0x0835 (an L, not a post) | |

The stone shop set (OSI multi 0x00A0) reverses the usual pair order: 0x0058 is the east-west piece and 0x0057 the
north-south one. The bank and lodge on the isle use it (P720).

In the dark wood set, `walls.txt`'s South1/South3 and East1/East3 "variants" (0x000A-0x000D) are door frames. Use the
plain pieces for a plain run.

**Floor:** at the wall Z, the floor tiles lie inside the box **and under the south row and east column of walls**,
never under the north row or west column (all 8 small house multis, `notes/cc-P734-tools/roof-survey.txt`).

**Windows by wall** (`notes/cc-P734-tools/window-survey.txt`, every house multi 0x60-0xA3; window tiles counted in brackets): in an
east-west (north or south) wall use 0x013A plaster (26), 0x01D3 weathered stone (43), 0x005E light stone (4), 0x003B
grey brick (2), 0x0209 sandstone-plaster (6), 0x015C sandstone (4), 0x0154 plaster (2), 0x0102 marble (6); in a
north-south (west or east) wall use 0x013B (23), 0x01D4 (44), 0x005D (4), 0x003C (12), 0x020A or 0x0208 (12), 0x015D
(2), 0x0155 (4), 0x0103 (8), 0x00B9 light wood (8), 0x0023 fieldstone (4), 0x000F dark wood (4), 0x0099 log (6). The
light wood set's window for an east-west wall never appears in a multi; 0x00BA is the candidate (unverified, P734 used
it and checked the render).

Half and quarter walls, arches and windows are their own pieces with the same four roles (dark wood half wall
0x0010-0x0013, quarter 0x0014-0x0017; grey brick arches from 0x0045). A window or arch replaces the run piece on its
tile and must match the run's facing (an "S" window in a north or south wall, an "E" window in a west or east wall).

### 2.3 Roofs sit on the walls

**Rule:** the roof's lowest course sits on the top of the walls (floor + 20), covers the whole wall box, and has
nothing on it: no props, no chimney standing apart, no flowers.

*Why (Chase 10-28 09:20-09:21):* the practice bank was "a plain stone box" with a flat grey roof, and the League lodge
"an empty roofless box". A flat roof also vanishes in the client when a player stands inside, so the building reads as
roofless. P720 rebuilt both after OSI's stone shop: shingle roof pitched along y (0x05C4 west slope, 0x05C2 ridge,
0x05C3 east slope), eaves at floor + 19, rising 3 per tile, a stone gable 0x0069 on the south end from floor + 20,
checked by `build_isle.check_pitched_roof()` against the shop multi's 54 roof pieces.

**Where the roof goes** (verified on the 8 small house multis, `notes/cc-P734-tools/roof-survey.txt`): the lowest
course sits at **wall Z + 20** and covers **x0+1 .. x1+1, y0+1 .. y1+1** of a wall box x0..x1, y0..y1: one tile in
from the north-west corner and one past the south-east one (the 20 Z of height moves it on screen so it lands on the
walls). A roof pitched along y has the west slope piece on the first column, the east slope piece on the last, rising
3 Z per course inward, and the ridge on the middle column; the gable pieces fill the **south wall's row** between the
slopes at each course. Each material has its own gable piece: plaster 0x014A or 0x020B, light wood 0x00C1, grey brick
0x0055, dark wood and fieldstone 0x0018, light stone 0x0069. Pieces from house multis: thatch west 0x05A6 / east
0x05A4 / ridge 0x05A5; shingles 0x05C4 / 0x05C3 / 0x05C2; tile 0x05B5 / 0x05B4 / 0x05B3. Some multis (0x0074, 0x0076)
pitch along x instead: take all roof pieces from one multi pitched the way you build.

Custom-house roof pieces (verified, ServUO `roof.txt`): each style has four slopes (N, E, S, W), two ridges (N-S and
E-W), four dents (inside corners), four T pieces and one X. Thatch 0x2C51-0x2C5F, wooden shingles 0x2C33-0x2C41,
tile 0x2C24-0x2C32, log 0x2C42-0x2C50, stone 0x2C6F-0x2C7D. Roof pieces are 3 high (tiledata). When in doubt, copy the
roof of the OSI multi the building is modelled on, whole.

### 2.4 Doors hang in the wall line

**Rule:** a door replaces the wall piece on its wall tile, and its open position folds back along the wall, not out
across the path and not onto the carpet.

*Why (Chase 10-28 09:20, the bank's inside shot):* "the open door swings outside the wall line". In an east-west wall
use `DarkWoodDoor(DoorFacing.WestCCW)` (closed art 0x06A9; open offset -1,0, along the wall). `WestCW` (0x06A5) swings
outside; `EastCW` swings in onto the carpet (`TutorialCorePlacement.cs:178-186`, compared by render in P720).
The free-standing "door piece beside a wall gap" on the lodge was a WestCW door standing open.

Gates: one `LightWoodGate` per gap (`DoorFacing.NorthCCW` in a north-south fence), never two halves: every wooden gate
art 0x0841-0x0848 is impassable open or shut, and pinned ModernUO swings a gate in a north-south fence one tile east,
so two halves blocked both tiles (P718).

Keep a door's approach line clear for two tiles: a signpost two tiles in front of the bank door made TazUO slide the
walker along the wall (P722).

### 2.5 Windows, a sign, a furnished inside

**Rule:** every building has windows in its walls, a sign naming it outside its door, and an inside furnished for its
purpose, so a player knows what it is from outside and from inside.

- **Shop sign:** the hanger **0x0B98** (the arm that sticks out from a south wall; **0x0B97 lies along the wall**,
  P734 review) and its board (0x0C0B for a bank, 0x0BD2 brass for a house) on the tile just outside the south wall,
  **two tiles east of the door** (OSI multi 0x0064: door 3,3, sign 5,4, Z 5 over a floor at 7). One tile east draws the
  board over the door leaf (P734 review). 0x0B97 alone on the ground reads as a stick of debris (P718). The isle's
  bank sign is 0x0B97 + 0x0C0B (P720): worth a look in a shot.
- **House sign:** brass sign 0x0BD2 by the door, named ("Wren's farmhouse").
- **Signpost on open ground:** stock 0xA854, named so a single click reads it (section 6).
- **Furnishing that worked (Chase accepted, P720/P722):**
  - Farmhouse: fireplace 0x0959 + 0x0953 on the west wall (StoneFireplaceEast), bed 0x0A63 + 0x0A5C along the east
    wall (SmallBedSouth), table 0x0B90 with chairs (P720 used 0x0B4E north and 0x0B4F south of it; by the art the
    north chair should be 0x0B4F and the south one 0x0B50, section 3), barrel 0x0E77,
    wooden box 0x0E7D, wall torch 0x0A0C on the north wall at floor + 13.
  - Bank: counter 0x0B40 in a row with the banker behind it and a gap at one end; vault chests 0x0E41/0x0E40 behind;
    candelabras 0x0B26; torches 0x0A0C (north wall) and 0x0A07 (west wall) at Z 13; a bench 0x0B2C for waiting; a red
    carpet built from corners, edges and centre 0x0AC8. By the art (P734 reviews, both ways rendered): edges **north
    0x0ACE, south 0x0AD0, west 0x0ACD, east 0x0ACF**; corners **NW 0x0ACA, SE 0x0AC9**, NE 0x0ACC, SW 0x0ACB (P720's
    corners were right; it used 0x0ACE/0x0AD0 for both pairs of edges, worth a look in a shot). A one-row runner is
    0x0ACD, centre pieces, 0x0ACF.
  - Lodge: writing tables 0x0B4A with a book 0x0FEF and scroll 0x0E34 on them, bookcases along the west wall (the isle used 0x0A97; use 0x0A99, below)
    and 0x0A98 along the north wall, table and chairs, candelabras, torches, carpet, a notice board on the north wall,
    and two League banners 0x1589 outside the east wall at Z 8. (P734 review: 0x0A97 faces south like 0x0A98, so on
    a west wall it stands edge-on; the east-facing case for a west wall is **0x0A99** (also 0x0A9A, 0x0A9C). The isle's
    lodge uses 0x0A97 there: worth a look.)

### 2.6 Nothing stray

No props on roofs, no flowers within 2 tiles of a road (a grass-flowers bush 0x0C86 on the path read as "a red
animal-like object", P720), no leftover pieces of an older version under or beside the new one (P718's two overlapping
fences). When you replace a building or a fence, remove the old one in the same seed (`TutorialFarm.IsCurrent` swaps
any farm that is not exactly the current layout).

## 3. Facing

Chase 10-28 12:13/12:16: "make sure Golems place items with the correct facing". Chase 10-29 10:14: "still wrong
decoration directions, walls, stairs". The rules:

- **Wall-mounted items** (signs, torches, sconces, banners, shelves, paintings) sit on the floor tile in front of
  **their** wall and face the walk side. Wall art comes in two facings only: the "east" facing hangs on a **west**
  wall, the "south" facing on a **north** wall (OSI town decoration; `uo-wall-orientation.md` section 12, 150 torches
  surveyed). So wall decoration goes on north and west walls, which are also the walls the camera shows.
  - Torches: on the floor tile, Z = floor + 13. North wall 0x0A0C (also 0x0A0A, 0x0A0B, 0x0A0D, 0x0A0E); west wall
    0x0A07 (also 0x0A09, 0x0A05, 0x0A08).
  - Bookcases: **0x0A99** (or 0x0A9A, 0x0A9C) along a west wall, facing east; 0x0A98 along a north wall, facing
    south. 0x0A97 also faces south (P734 review, rendered against a wall run), so it is a north-wall case too.
  - Banners 0x1589: flat on an east wall from outside, Z 8 (P720 lodge).
- **Doors** open onto their own room and fold along the wall (section 2.4).
- **Beds, tables, chairs, counters:** the bed's head against a wall (SmallBedSouth along an east wall); chairs face the
  table. By the art (P734 review): **0x0B4E faces east, 0x0B4F faces south, 0x0B50 faces north**, so a chair north
  of a table is 0x0B4F and one south of it 0x0B50 (and one west of it 0x0B4E); a counter's
  serving side toward the door, the keeper behind it.
- **Stairs** climb toward the floor they serve (section 4.2); the bottom step faces the room or door it is entered from.
- **Multi-part addons:** pick the **variant** that fits the place instead of turning pieces: the shipwreck's West
  variant on a west-facing beach, bow to the sea (P724). Add-on deeds in UO come as East and South versions; an
  east-facing add-on spreads south from its target tile and a south-facing one spreads east (uo.com, section 9).
- **Check every piece from the default camera** in the shots and list any piece you turned in `placed.md`.

## 4. Heights: walkable joins

### 4.1 Within one step, both ends, walked for real

**Rule:** every walkable join (bridge, dock, ramp, stair, doorstep, frame step) changes the standing height by **at
most 2 per step** where a player walks onto and off it, and a **real character walks it both ways** in TazUO.

*Why (Chase 10-28 09:23-09:25 and 12:19-12:20, "the bridge tiles are too high", "the bridge by the moongate is one
way"):* the shore's first sand ring was dropped to -7 under the dock's end, which pulled the last beach tile's averaged
height to -5 against a first plank at -2: a 3-step the client refuses. A real character walking east stuck at
6820,3991,-5 for 30 steps. The server walker allowed it (it starts from the land's top) and the bot teleports, so
neither saw it. P720 kept the wet sand at -3 in the dock's rows and added the `build_isle.dock_steps` gate.

Proof: a Legion walk script (P720's `IsleBridgeWalk.py`, P724's `WalkFrame.py`) that steps the client across and back,
logging each step's Z, and a shot at the far end both ways.

### 4.2 Stairs

Verified from the client's tiledata and OSI's house multis (`notes/cc-P734-tools/stair-survey.txt`):

- A **step** piece is 5 high; a **block** is 10 high. Four steps climb one 20-high storey.
- A step named for a direction **climbs toward that direction**: walking north up a "north" stair. In the multis,
  every "north" piece (0x0751, 0x076D, 0x0789) has the next step 5 higher to its north; "east" pieces (0x073C, 0x0754,
  0x0770) rise east; "west" pieces (0x070B, 0x078A) rise west.
- Place a straight flight as one step per tile, each 5 higher than the last, with blocks under the upper steps if the
  side shows (OSI fills under with blocks).
- The top step's top must equal the upper floor's Z, and the upper floor must be open above the stair (no floor tile
  over the stair's tiles: "Stairs require open floor tiles on the floor above", uo.com). Remove the floor tiles over
  the stairwell.
- Corner pieces (squared and rounded) turn a flight; use the corner piece of the same material.

Stock stair sets (ServUO `stairs.txt`, verified for the IDs that appear in OSI decoration):

| Material | Block | North | East | South | West | Squared corners | Rounded corners |
|---|---|---|---|---|---|---|---|
| Dark wood | 0x0738 | 0x0739 | 0x073C | 0x073B | 0x073A | 0x0740 / 0x073E | 0x0746 / 0x0745 |
| Light wood | 0x0721 | 0x0722 | 0x0725 | 0x0724 | 0x0723 | 0x0729 / 0x0727 | 0x072C / 0x072B |
| Grey stone | 0x07A3 | 0x07A4 | 0x07A7 | 0x07A6 | 0x07A5 | 0x07AB / 0x07A9 | none |
| Weathered stone | 0x0788 | 0x0789 | 0x078C | 0x078B | 0x078A | 0x0790 / 0x078E | 0x0793 / 0x0792 |
| Granite | 0x071E | 0x071F | 0x0749 | 0x0737 | 0x0736 | 0x074D / 0x074B | none |
| Tan marble | 0x0709 | 0x070A | 0x070D | 0x070C | 0x070B | 0x0711 / 0x070F | 0x0714 / 0x0713 |
| Sandstone | 0x03EE | 0x03EF | 0x03F2 | 0x03F1 | 0x03F0 | 0x03F6 / 0x03F4 | 0x03F9 / 0x03F8 |
| Sandstone brick | 0x076C | 0x076D | 0x0770 | 0x076F | 0x076E | 0x0774 / 0x0772 | 0x0777 / 0x0776 |
| Light stone | 0x0750 | 0x0751 | 0x0754 | 0x0753 | 0x0752 | 0x0758 / 0x0756 | 0x075B / 0x075A |

(`stairs.txt`'s "Multi" columns, 0x1DB0 and up, are house-tool multi numbers, not item IDs: as items those numbers are
body parts and a barrel.)

### 4.3 Docks and bridges

Dock pieces that read right (P720, from an OSI survey): deck at one Z, planks 0x07C9/0x07CD, rope rails 0x03A6 along x
and 0x03A9 along y at deck + 5, corner posts stacked 0x03AE (deck - 5), 0x03A5 (deck), 0x03AB (deck + 5). The land end
of a dock or bridge sits within 2 of the deck; lower the deck or raise the bank, never leave a lip.

## 5. Land

- **Real shore transitions, no sawtooth.** Chase 10-28 11:47: "island needs shore tiles". Laying OSI's whole water
  diamond 0x1797 on each first sand tile steps along every non-axis coast. Use the surf pieces chosen by which side the
  land is on (P725, `notes/cc-P662-tools/shore-rule.json`): land east of the sea cell 0x179D/0x179E, south
  0x17A1/0x17A2, both 0x17A7, north 0x179F/0x17A0, west 0x17A3/0x17A4, north and west 0x17A6/0x17AF; single diagonals
  0x17A9 (NE), 0x17AB (SW), 0x17AC (NW); last sand tile small surf 0x17A5, 0x17A8, 0x17AD, 0x17AE, 0x17B0, 0x17B2.
  First sand ring at -4, then -3, -1, 0; sea land at -5 (OSI's -15 makes every coast a cliff). The north and south
  shores still show a small stepped edge (P733): fully hiding it needs new art, so do not claim it is gone.
- **Foliage in clusters, denser inland.** Seeded round clumps (about 1 per 28 land tiles, radius 2.5-5.5), not a grid
  and not an even sprinkle; tiers by distance from the sand: beach (sparse, low), edge, middle, deep (trees). Multi-tile
  trees are laid as OSI's whole compositions (the jungle trees 0x0D41-0x0D93 along the north-east diagonal, P725).
- **Keep clear:** trees 3 tiles from a road, stops, server items and landmarks, 4 from buildings, yards and squares;
  undergrowth 2 from a road; no flowers within 2 of a road; nothing within 4 of a spawn or wake spot. Paths, signs,
  doors, gates and NPCs must stay reachable and visible.
- **One fence, one rule:** a fence is one closed ring laid by the wall rule (post 0x0838 NW, L corner 0x0835 SE,
  E-W 0x0836 along the north row to the NE tile and the south row, N-S 0x0837 down the west column to the SW tile and
  the east column; 0x0835 at the NW makes an X of stubs, P734 review), one
  piece per tile, one Z), with its only opening the gate. Two overlapping fences made stubs, gaps and mixed posts that
  Chase called "weird" (10-28 09:18).

## 6. Markers and props

- **Signs, not rune markers.** Chase 10-28 09:18-09:20 did not like lesson stops marked with runes (0x1F14) on the
  ground. Use the standing signpost 0xA854, named ("Lesson 3: Healing"), **beside** the stop (within 2, never on it),
  off the walked route, the road, door lines and gates. A signpost is impassable. When you change a marker's art,
  update every tool that finds it by art ID (the bot's route still searched for 0x1F14, Codex P720).
- **A hurt NPC on a bench with blood.** Chase 10-28 12:24-12:26: the injured farmhand "sits or lies on a bench with
  blood on the ground around". Pip: bench 0x0B2D against the farmhouse's east wall, blood decals 0x122A, 0x122D, 0x122C
  (stock 0x122A-0x122E) around it, NPC facing into the room, `RangeHome = 0`. (The bench's art facing and the seated
  look are unverified in a shot: check yours.)
- **Containers appear for a player when an item is handed over.** Chase 10-28 15:23: "the cloak comes in a chest that
  appears". A personal chest (0x0E43) appears on a table with a sparkle (0x376A) and sound (0x1F5), only its player can
  open it, nothing can be dropped in, and it vanishes once the item is taken. Make it **Movable but refuse its own
  lift**: ModernUO lets nothing be lifted out of an immovable container (P728 probe).
- **Every NPC the story needs is placed.** "Pip is missing" (Chase 10-28 15:28): the farm boy was only placed by a
  command nobody re-ran. Seed every NPC (section 7).
- **Lived-in props:** a few, on surfaces, telling what the room is for (plates and mugs on a tavern table, books on a
  desk), not a sprinkle on the floor.

## 7. Lessons and the existing world

- **Never "0 more".** Name what is still missing; when the count reaches zero, say what is done and what to do next.
  "The cabbage rows are clear! Go back to Wren at the farm gate and double-click her." (P728, Chase 10-28 15:27).
- **Every step ends with the next step said plainly**, over the NPC, over the player, in the System window and at the
  top of a reopened lesson window, with the arrow on the next signpost.
- **Anything new appears on an existing world by itself.** Seed missing pieces at every world load, idempotently,
  only what is missing, adding each to the copy's reset list, and log a count (`tutorial.seedMissingOnLoad`, P728).
  Run it **after** the load: `EventSink.WorldLoad += () => Timer.DelayCall(TimeSpan.Zero, ...)`; an item made inside
  `World.Load` reaches `World.Items` only after the load, so an in-load check counts nothing (P726). Upgrade in place:
  rehang old doors, move old markers to signs, replace a farm that is not the current layout.

## 8. Proof: renders, shots and what to leave for the reviewer

**Never on the shared test shard.** Use a private shard (port 2596 under the `test-shard` lock), a private copy of the
world, or a spare test plot; never move or swap the Chases-Tower 2594 shard's characters.

Tools (command lines from the tools' headers; P720-P732 used them):

- **isorender.py** (`scripts/mapbuild/isorender.py` in shard-migration; client-correct statics, unlike vseUOAware's
  renderer, which draws statics half a tile high):
  `python -P scripts/mapbuild/isorender.py map <folder> <facet> x1 y1 x2 y2 out.png` and
  `python -P scripts/mapbuild/isorender.py multi <multiId> <zmax> out.png`.
  Set `PYTHONPATH=scripts`, `MAPBUILD_CLIENT=D:\UO\tool-trials\client-data-copy`, `MAPBUILD_ART` to the art folder.
- **render_addons.py**: `D:\UO\overseer\render_addons.py` (the overseer's sheet of the shipwreck addons) and the general
  `notes/cc-P724-tools/render_addons.py <out.jpg> <title=path.cs> ...` (also `ids:0xA62B,...`), which reads addon
  component tables and renders them on sand. `plan_render.py` (same folder) places addons on the built map and prints
  the land under each piece.
- **Private shard:** `notes/cc-P720-tools/proof-shard.ps1 -Work <scratch> [-Image sl-modernuo:cc-P<nn>] [-Port 2596]
  [-KeepWorld] [-Down]`.
- **TazUO shots off-screen:** `isle-shots.ps1 -Spec shots.json -Out <folder> -Port 2596` (it defaults to 2594: always
  pass `-Port 2596`). Each spec entry moves the tester with `[global set Map ...`, `[global set Location (x,y,z)` (no
  spaces) and `LogoutMap`/`LogoutLocation`, then settles and shoots from the **default camera**.
- **Real walks:** a Legion script started by TazUO that steps the client (no teleport) and logs each step's Z
  (`notes/cc-P720-tools/IsleBridgeWalk.py`, `notes/cc-P724-tools/WalkFrame.py`).

**What a build prompt leaves** in `notes\cc-P<nn>-review\` in the docs copy (the build reviewer reads exactly this;
keep each image under 1 MB, JPEG is fine):

1. `placed.md`: one line per placed piece or addon: item ID (or addon name), location x,y,z, facing or variant, and
   what it is ("0x06A9 door, 6764,3980,7, WestCCW, bank south door"). Group by building.
2. One **isorender** of each building or area, top-down enough to read every wall corner.
3. **TazUO shots** from the default camera: outside each building (door side), inside each room, each stair from
   below and above, each bridge or dock from both ends, each sign readable.
4. The **walk logs** of every stair, bridge, dock and door, both ways.
5. A before shot where something was replaced.

The integrator holds a map or decoration prompt's merge until a second Claude Golem's review says PASS (cc-P734). A
FAIL comes back as a fix-up with the reviewer's numbered list.

## 9. Learned from human builders

Chase 10-29 10:10-10:11: decoration directions, walls and stairs still come out wrong; learn from Stratics and other
player sites, for ideas and techniques, never to copy a house piece for piece.

**What could be reached (2026-10-29).** Stratics (uo.stratics.com, uo2.stratics.com, community.stratics.com), forum.uo.com
and forums.uo.com, uoex.net and MassivelyOP all answered 403 to the fetch tool, and the Wayback Machine was refused, so
their threads (Better Homes & Castles, Custom Staircases, Spiral Stairs 101, Echo Deco Tips & Tricks, the Summer Garden
Deco Contest) were seen only as search snippets, marked [snippet] below. The precise material came from the data the
in-game house tool itself uses (ServUO's `Data/Components` tables), RunUO's wall scripts and OSI's own town decoration
files, uo.com's official decorating articles, UOGuide and two player blogs. Every point below has its link.

### 9.1 Walls, corners, stairs, roofs and floors

- Each wall material is one set: South pieces, East pieces, one L-shaped Corner, one Post, plus window pieces per
  facing; half, quarter and roof-edging walls are their own sets
  (https://raw.githubusercontent.com/ServUO/ServUO/master/Data/Components/walls.txt). RunUO names the white stone set
  `EastWall 0x57, SouthWall 0x58, SECorner 0x59, NWCornerPost 0x5A`
  (https://raw.githubusercontent.com/runuo/runuo/master/Scripts/Items/Construction/Walls/WhiteStoneWall.cs). Our own
  survey of OSI's multis agrees (section 2.2). A Stratics guide warns that the "tricky southeast and northwest corners"
  are the two to plan for [snippet] (https://uo2.stratics.com/?p=7229).
- Raph Koster on why: the wall tileset was "the most efficient tileset we could make for the sake of networking
  traffic", and it "prevented players from standing in a corner that occluded them entirely"; every wall shares one
  height so the next floor sits on it (https://www.raphkoster.com/?p=38092).
- The order of pieces inside a set is not the same across materials (dark wood: Corner, South, East, Post; thin stone:
  Corner, East, South, Post), so never compute an ID by offset
  (https://raw.githubusercontent.com/runuo/runuo/master/Scripts/Items/Construction/Walls/ThinStoneWall.cs).
- Stairs: each material has a block, four directional steps, squared and rounded corner steps
  (https://raw.githubusercontent.com/ServUO/ServUO/master/Data/Components/stairs.txt); OSI's towns use exactly these
  (granite 0x071E/0x071F/0x0737 at Buccaneer's Den, weathered stone 0x0788-0x078F at the Chaos shrine,
  https://raw.githubusercontent.com/runuo/runuo/master/Data/Decoration/Britannia/bucs.cfg and shrines.cfg).
- Custom-house floors are at +7, +27, +47, +67 (https://www.servuo.dev/threads/housefoundation-cs-question.16000/post-94159).
  "Stairs require open floor tiles on the floor above"; blocked stair exits turn orange
  (https://uo.com/?p=6540). Builders lay the upper floor, then remove the tiles over the stairs [snippet]
  (https://uo2.stratics.com/?p=1862). Keep raised floor tiles "one click lower than the top of the stairs" for
  headroom; stone blocks "can be stacked for decorative effects or an outside staircase" (https://uo.com/?p=10716).
- Gaps where a new wall meets an old one are plugged by a closed, locked crafted door (https://uo.com/?p=36450).
- Roofs: four slopes, two ridges, four dents, four T pieces, one X per style
  (https://raw.githubusercontent.com/ServUO/ServUO/master/Data/Components/roof.txt). Classic statics: slate 0x0596,
  thatch 0x05A4, shingles 0x05C3-0x05C5 (https://raw.githubusercontent.com/runuo/runuo/master/Data/Decoration/Britannia/britain.cfg).
- Floors: each floor set has up to 16 patterned variants (borders, plain, cracked); mix them so a big floor does not
  tile visibly (https://raw.githubusercontent.com/ServUO/ServUO/master/Data/Components/floors.txt). Grey pavers
  0x0519-0x0524, sandstone bricks 0x0525-0x0536, dark wood 0x04AD-0x04B4, light wood 0x04CC-0x04D3.

### 9.2 Decorating techniques

1. **Order of work:** rugs and carpets first, then furniture, then small items on the furniture
   (https://www.uotavern.com/wiki/playing/decorating/).
2. **Raise small items onto surfaces** (books on a desk, a candle on a mantel, plates on a table): place beside, then
   raise onto the top (same link). For us: set the item's Z to the surface's top (a table 0x0B8F is 6 high).
3. **Invisible risers:** players raise goza mats or floor tiles as hidden supports and stack items on them, and use
   lowered gozas to split a multi-tile add-on ("The Long Bar") (https://uo.com/?p=6572;
   https://kirthag.blogspot.com/2019/06/falling-through-floors.html). For us: give the item the Z directly; a riser
   is only needed where a player must be able to target or stand on it.
4. **Carpets from edge pieces:** square centre pieces fill any size, edge and corner pieces frame them; a hallway uses
   only the fringed ends (https://uo.com/?p=5957). Tuck rugs partly under furniture; use large items to hide the seam
   where wall meets floor; carpets and floor tiles define zones in an open room (uotavern link above).
5. **One palette:** a matched hue across furniture, rugs and banners reads as intended (uotavern link above).
6. **Facing of add-ons:** east and south versions; east-facing add-ons spread south from the target tile, south-facing
   ones spread east (https://uo.com/?p=6572; https://www.uoguide.com/Scarecrow).
7. **What shows from the default camera:** the camera looks from the south-east, and wall art exists only in the two
   facings that hang on west and north walls, so wall decor, shelves, banners and tall furniture go against the north
   and west walls with open floor toward the south-east. (Reasoned from the facing rules above and confirmed by OSI's
   torches, section 3; no page says it outright.)
8. **Lighting as dressing:** sconces 0x09FD/0x0A02, torches 0x0A07/0x0A0C, candles 0x0A0F/0x0A26, lantern 0x0A18,
   hanging lanterns 0x0A1A/0x0A1D, lantern post 0x0A20; Britain's lamp posts 0x0B20/0x0B24 and candelabra stands
   0x0A29/0x0B26 (bucs.cfg, britain.cfg above).
9. **Lived-in clutter, on surfaces:** plate 0x09D7, plate of food 0x09DB, silverware 0x09BD/0x09D4, pitcher 0x09D6, mug
   0x09EE, ale 0x09A0, wine 0x09C7; bedrolls 0x0A55-0x0A57 on the floor; crates 0x0E3C-0x0E3F, 0x0E7E and barrels 0x0E77
   as working clutter (bucs.cfg, britain.cfg above).
10. **Many small rooms beat one big box**: more walls to hang things on, more corners to tuck pieces into; terraces,
    fountains and gardens; mix symmetry and asymmetry [snippet]
    (https://massivelyop.com/2020/07/09/working-as-intended-decorating-mmorpg-houses-in-swg-legends-and-beyond/).
    UOGuide's tip: "Don't build a Borg cube" (https://www.uoguide.com/Customize).

### 9.3 Example layouts (ideas, described in words)

Inspiration only: take the idea, make our own design. Most player-tour pages were unreachable, so most examples are
built from OSI's town dressing and decorating guides; each says what it draws on.

1. **Farmhouse kitchen and yard.** Log walls (0x0090-0x0097) under thatch (0x2C51-0x2C5F); a stone fireplace on the
   north or west wall (0x0959 set) and an oven (StoneOvenEast 0x092C) with a flour sack 0x1039 and an open sack 0x103A
   beside it; out back hay sheaves 0x100C/0x100D, hay piles 0x1036/0x1037 and a scarecrow facing the field; a wooden
   chest 0x0E43 (Britain tags one `ContentType=Farm`). britain.cfg; https://www.uoguide.com/Scarecrow.
2. **Orchard.** Rows of apple, peach and pear trees (0x0D94-0x0DAA) with flower clumps (0x0C83) in the gaps and a water
   barrel 0x154D at the row end. britain.cfg.
3. **Bank or vault.** Brick or marble walls, metal doors (0x0675-0x0681), a counter row with the tellers behind it,
   strongboxes 0x09A8/0x0E80 and gold chests 0x0E40/0x0E41 behind them, candelabra stands 0x0B26 at each end, a rug
   zone in front of the counter for the queue. Assembled from britain.cfg's door and container IDs [layout unverified].
4. **Keep or guild hall ("Stronghold").** A bottleneck entrance into a courtyard, a small open stable off it, stairs up
   to the main hall with pavers at the top, a catwalk round the courtyard, a peaked roof with skylights, rooftop reached
   by granite stairs. https://kirthag.blogspot.com/2019/06/stronghold.html.
5. **Lodge or trophy hall.** Mounted trophies, statues and guild banners; display cases; clear sightlines from the door.
   https://www.uotavern.com/wiki/playing/decorating/.
6. **Tavern.** Long tables and benches, kegs and bottles on the bar, a hearth, lanterns, a chalkboard menu, open floor;
   mugs 0x09EE, ale 0x09A0, plates 0x09D7/0x09DB, stools 0x0A2A/0x0A2B, hanging lanterns 0x0A1A. uotavern; bucs.cfg.
7. **Library.** Bookshelves 0x0A97-0x0A9C against the walls, reading desks with quills and tomes, a globe, a few chairs,
   muted rugs. uotavern; britain.cfg.
8. **Dock or harbour front.** Pavers 0x051E-0x0520 stepping down to the water by granite stairs (0x071E, 0x071F,
   0x0737); rope coils 0x14F8/0x14FA, barrels 0x0E77, a water barrel 0x154D, a large crate 0x0E3D, small fish
   0x0DD6/0x0DD7; lantern posts 0x0A20 along the edge. bucs.cfg; britain.cfg [layout unverified].
9. **Market square.** Grey pavers 0x0519-0x0524, variants mixed, round a central feature; stalls of crates and barrels
   with flour 0x1039, hay 0x1036, fish 0x0DD6, a forge 0x19A2 at the smith's corner; lamp posts 0x0B20/0x0B24 at the
   corners. britain.cfg; floors.txt [layout unverified].
10. **Chaos-style shrine.** An ankh (0x0003 west, 0x0004 north) on a raised dais of weathered stone stairs
    (0x0788-0x078F), two candelabra stands 0x0B26 flanking it. shrines.cfg.
11. **Spirituality-style shrine.** A tan marble platform (0x070A-0x0711) reached by steps on every side, the corner
    steps turning each corner. shrines.cfg.
12. **Re-themed shrine.** One prop changes a whole site: the bloodied ankh 0x1E5D at Sacrifice. shrines.cfg.
13. **Garden.** A picnic-blanket zone, a pond with an edge, potted plants 0x11CA-0x11CC softening corners [snippet:
    the Summer Garden Deco Contest, https://forums.uo.com/discussion/12850/summer-garden-deco-contest-entries-and-winners].
14. **Rooftop terrace.** The top level as an open terrace with fountains and plants, only part of it roofed [snippet:
    MassivelyOP above].
15. **Mage tower.** A tall narrow shell, spellbooks, crystal balls, candelabra and alchemy tables below, an observatory
    upstairs. uotavern.

## 10. What to use where

A pick list for dressing ten kinds of place. For each place it gives:

- stock UO item IDs that fit;
- packs on disk in `D:\UO\third-party` that fit, tagged by what they cost to use;
- a "do not use here" list.

Read the pack's own `SOURCE.txt` before you commit to it. Nothing ships until it is in `registry.csv` and its terms
are met (see `ART-LIBRARY.md`).

### How to read this section

**Two tags for packs**

- **Server addon from stock art (usable now).** The pack ships only placement data that points at art every client
  already has:
  - a ServUO addon script (`.cs`, in `code\`);
  - a UO Architect design (`.uoa`);
  - a multi export (`.txt`).
  We port or convert it to a ModernUO addon on the server, and no client update is needed. P724's four isle pieces
  went this way.
  - `.cs` scripts are reference only: port them, never build them from `third-party`.
  - `.uoa` files need a convert step to an addon or to statics. A converter is queued (Q#854).
- **Needs new client art (client-package prompt first).** The pack ships pictures or bodies: `.bmp`, `.png`, `.tif`,
  `.psd`, `.vd` or `.mul`. Each picture needs:
  - a new item ID (never over stock art);
  - a row in `registry.csv` and its record in `records.json`;
  - a player package release.
  Only after that can the server place it. P725's draft "tropical art" prompt is the model for this.
- **How I decided.** I counted file extensions per folder (`find | sed 's/.*\.//'`) and read each `SOURCE.txt`:
  - a folder with only `.cs`, `.uoa` or multi `.txt` (plus zips and previews) is stock;
  - a folder with any image or `.vd` that is meant to be placed is new art.
  - Packs marked "EA-derived" are still new art. They are edited stock pictures that need new IDs. Ship them as
    patch records only.

**Stock IDs**

- **"verified (code)"**: read from our code or ModernUO:
  - `D:\UO\golems\Iron\ShatteredLegacy\server\customizations` (Tutorial isle and farm, Alembic hall, traps);
  - `D:\UO\ModernUO-pinned\Projects\UOContent` (Farmable crops, Ankhs, fountain, trough, fishing net and scarecrow
    addons).
- **"verified (tiledata)"**: the name as read from `D:\UO\UltimaOnlineVanilla\tiledata.mul` with the vseUOAware
  `find_item_id_by_name` tool. That tool prints IDs plus 0x4000; the IDs here are item IDs with the 0x4000 taken off.
- **"unverified"**: from memory of the stock art. Check the ID in the client before you use it.
- **High IDs (above about 0x8000) are newer expansion art.** They are in the vanilla client's tiledata. Before you rely
  on one, check that our player client draws it.

**Terms**

Almost every pack states no terms. `SOURCE.txt` then says "treat as community work":

- credit the author;
- ship only inside the player package or the private repo;
- do not repost.

I write that as **"community terms"** below. Anything stricter or looser is quoted.

### Already on our shard (do not re-add)

- **Wakening Isle (P724, merged; in isle release 3 by P733).** `server/customizations/Tutorial/TutorialIsleAddons.cs`,
  credits in `Tutorial/IsleAddons-SOURCE.txt`. All four are stock art:
  - `celestial-shipwrecks` (West variant, 20 pieces) on the wake beach;
  - `new-lighthouse` (3 pieces) by the dock;
  - `moongate-structure` (88 pieces and 3 lanterns) round the dock's gate;
  - `lagatha-brass-fountains` (art 0xA62A/0xA62B) on the bank square.
- **Isle shore and tropical planting (P725).** Stock map statics only:
  - the surf pieces 0x179D-0x17B2;
  - palms, ferns and the jungle trees listed under "Tropical isle" below.
- **Tutorial farm fences (`TutorialFarmLayout.cs`).** Stock wooden fence 0x0835-0x0837.
- **Alembic guild hall (`ClusterFAlembicGuild.cs`).** Stock art only. Third-party pieces wait for an art prompt.
- **Registered new art.** `animated-runestone` (0x3C10-0x3C3B) and `animated-mimic` are REG.
- **Looked at and not placed.** P724 looked at these and did not place them (reasons in
  `notes\cc-P724-isle-addons.md`); they are free for other places:
  - `dock-addon`;
  - `olorin-market-tents`;
  - `celestial-cave-entrances`;
  - `sparring-dummy` (needs ServUO's `DamageableItem`, not in ModernUO);
  - `training-weapons`, `lockpicking-chest-trainer`, `da-training-hall`.

---

### Farm

**Stock IDs**

| ID | What | Check |
|---|---|---|
| 0x0835, 0x0836, 0x0837 | wooden fence (as the tutorial farm uses) | verified (code) |
| 0x03B3-0x03B5, 0x0821-0x0823, 0x0849-0x084B (iron), 0x085C-0x0865, 0x0877-0x0878, 0x088A-0x088B | more fences: wooden, and iron for a manor farm | verified (tiledata) |
| 0x0F34, 0x0F35, 0x1036, 0x1037, 0x1A92-0x1A96 | hay (piles and bales) | verified (tiledata) |
| 0x0F36 sheaf of hay; 0x100C, 0x100D hay sheave | sheaves | verified (code + tiledata) |
| 0x0C55-0x0C58 wheat; 0x0DAE-0x0DAF picked wheat | crop | verified (code, `FarmableWheat`) |
| 0x0C51-0x0C54 | cotton plants | verified (code, `FarmableCotton`) |
| 0x1A99-0x1A9D | flax | verified (code, `FarmableFlax`) |
| 0x0C5E-0x0C60, 0x0C6A-0x0C6C | pumpkin vines, ripe pumpkins | verified (code, `FarmablePumpkin`) |
| 0x0C76-0x0C78 carrots; 0x0C6D-0x0C6F onions; 0x0C61-0x0C63, 0x0D39-0x0D3A turnips; 0x0C70-0x0C71 lettuce; 0x0C7B cabbage | vegetable rows | verified (code, `Farmable*`) |
| 0x0C7D, 0x0C7E corn stalk; 0x0C7F-0x0C82 ears of corn | corn | verified (code + tiledata) |
| 0x1E34, 0x1E35 | scarecrow (`ScarecrowAddon`) | verified (code) |
| 0x0B41-0x0B44 | water trough E/S (`WaterTrough*Addon`, a water source) | verified (code) |
| 0x154D water barrel; 0x0E77 barrel; 0x0E7D wooden box; 0x0E3C-0x0E3F crates | farmyard clutter | verified (code + tiledata) |
| 0x0E87 | pitchfork | verified (code) |
| 0x091A | beehive | verified (tiledata) |
| 0x4514 chicken coop (south); 0x4C5A cowbell | yard props | verified (code); high ID, check the client |
| 0x05A4-0x05A6 | thatch roof (as the tutorial farmhouse uses) | verified (code) |

Also on our farm: the farmable crop classes (`Items/Farming/Farmable*.cs`) can be picked, and the crop IDs above come
from them.

**Packs**

- **New client art:**
  - `laoth-wooden-crates`: 20 BMP. Fruit and vegetable crates and empty ones. P725 rated it "Yes, for the farm".
    Community terms, credit Laoth.
  - `irrigation-ditch`: 16 BMP. A farming ditch. Community terms, credit Horian.
  - `mrriots-storage-crates`: 20 BMP. "Use them as you wish and edit them as you wish"; credit MrRiots; do not repost
    the raw files.
  - `home-supply-crates`: 25 BMP, labelled crates. Community terms. Credit the original servuo.dev author: the account
    shows as "[REDACTED 815]", resource 1278.
  - `hestia-barrels-crates`: 104 BMP. Community terms, credit Hestia. FLAG: redraws of stock barrels; any EA-derived
    tile ships as patch records only.
  - `hestia-water-barrel`: 9 BMP, an animated water barrel. Community terms, credit Hestia.
  - `hank-stumps-saplings`: 347 BMP. Stumps and saplings for a woodlot. Community terms, credit Hank. EA-derived:
    patch records only.
  - `mrriots-misc-3`: 113 BMP, has a beehive. "Edit and use them as you please"; credit MrRiots; EA-derived.
- **No terms known:** `farm-carts` has **no SOURCE.txt** (author and terms unknown). Do not use it until it is
  sourced.
- **Stock-art design:** `milva-pond-bridge` (1 `.uoa`, a large pond with a bridge, fishable). Community terms, credit
  Milva.

**Do not use here**

- `african-trees`, `african-savana-tree`: savanna trees.
- `hallow-trees`: Terraria fey glade.
- `purple-grass-dirt`, `purplegrass-to-dirt`: purple grass.
- `mrriots-halloween-*`, `archaaz-halloween` (skull trees, scarecrows): holiday art.
- Holiday art belongs in a seasonal swap, not on a working farm.

### Beach and coast

**Stock IDs**

| ID | What | Check |
|---|---|---|
| 0x179D-0x17B2 | surf and shore water pieces (P725's learned shore rule) | verified (notes, P725) |
| 0x14F7, 0x14F9 anchor; 0x14F8, 0x14FA rope with it | beached anchor | verified (tiledata; `GhostShipAnchor` uses 0x14F7) |
| 0xA32B-0xA32E | stockless anchor, four facings | verified (tiledata); high ID, check the client |
| 0x0DC8-0x0DCB, 0x0DD0-0x0DD5 | fishing nets (0x0DC8 used by our snare trap) | verified (code + tiledata) |
| 0x1EA3-0x1EA6 | net (`SmallFishingNetAddon` uses 0x1EA3/0x1EA4) | verified (code) |
| 0x3D8E, 0x3D8F | large fishing net (`LargeFishingNetAddon`) | verified (code) |
| 0x0FC4 conch shell; 0x0FC5-0x0FCC shells; 0x0FCD-0x0FD4 strings of shells | beach finds | verified (tiledata) |
| 0x1E2A oars; 0x1E19 fish heads | wreck and fisher clutter | verified (code) |
| 0x1357-0x135C | OSI's tall grey boulders (P687 uses them at cliff seams) | verified (notes, P687) |
| 0x0C95 coconut palm, 0x0C96 date palm, 0x0C99-0x0C9D small palms | warm-coast trees | verified (tiledata + P725) |
| 0x44CB-0x44D4 | lobster buoy, cage, lobster | verified (tiledata); high ID, check the client |

**Packs**

- **Usable now (stock-art server addons):**
  - `code\celestial-shipwrecks`: 3 `.cs`, East, West and North wrecks. The West one is on the isle; East and North
    are free. Community terms, credit Celestial.
  - `code\shipwreck-addon-70`: 1 `.cs`, a replica beach wreck: hull pieces (0x0C2D, 0x1FBC, 0x1FC5, 0x3492...) with shore water tiles 0x179E-0x17A8 under it. Community terms,
    credit Zero.
  - `code\new-lighthouse`: 1 `.cs`, 3 pieces (0x4724, 0x472F, 0x4730). Used on the isle; reuse it on another point.
    Community terms, credit Milva.
  - `code\lake-fishing`: 1 `.cs`, a lake of water tile 0x1797 (126 of them) with shore pieces 0x179E-0x17AC. Inland lakes only. Community
    terms, credit Lagatha.
- **New client art:**
  - `beach-trees`: 4 BMP, broad shade trees, two mirrored pairs. P725 rated it "Yes". Community terms, credit
    ParanoiaPhD; may need cleanup.
  - `transparent-water`: 28 BMP, see-through water tiles. Community terms, credit abu.
  - `otimpyre-under-the-sea`: 121 BMP, coral, rocks, sea floor.
  - `otimpyre-flooded-illusion`: 13 BMP, water-depth illusion.
  - `waterplants`: 19 BMP, algae and kelp. Community terms, credit Horian.
  - `mermaid-statues` (12 BMP) and `mini-mermaid-statues` (8 BMP), by Archaaz. Community terms. EA-derived: patch
    records only.
  - `treasure-items`: 30 BMP, amphorae and shipwreck treasure. Community terms, credit Horian.
- **Needs Chase's call** (new art):
  - `seagulls`: 5 `.vd`, 4 `.wav`, 1 `.cs`. FLAG: "IE" in the file names, so likely Infinity Engine rips; the sound
    source is not stated.
  - `sea-creatures`: 5 `.vd`. Community terms, credit Vert-I-Go. For a sea area, not for the shore.

**Do not use here**

- `arctic-pack`, `winter-holiday`, `mrriots-winter`, `rooster-animated-snow`, `xmas-community-tree`: snow and ice.
  The stock snow hedge 0xA600-0xA603 is out too.
- `verdant-autumn-trees`, `tall-trees`, `kevsurcu-big-trees`, `new-tree-art`: temperate or autumn trees on sand.
- `atlantis-tiles`: a sunken-dungeon set, for under the sea and not for a beach.
- `butterflies`: flagged rip, "Legend of Zhao Yun".

### Dock

**Stock IDs**

| ID | What | Check |
|---|---|---|
| 0x07CD | dock plank (the tile `dock-addon` repeats 96-128 times) | read from `dock-addon` .cs (1997); name unverified |
| 0x03AE | dock post or edge piece (`dock-addon`, 4-7 per dock) | read from `dock-addon` .cs (942); name unverified |
| 0x03A5, 0x03AA-0x03B0 pier; 0x03A6-0x03A9 rope | pier posts and rope rails | verified (tiledata) |
| 0x04A9-0x04B4 | wooden boards (as the isle's dock and floors use) | verified (code) |
| 0x14F7/0x14F9 anchor; nets 0x0DC8-0x0DD5; 0x1E2A oars | dock clutter | verified |
| 0x0E3C-0x0E3F crate; 0x0E77 barrel; 0x1940 keg | cargo | verified (code + tiledata) |
| 0xA2C4, 0xA2C5 | maritime trade crate | verified (tiledata); high ID |
| 0x0B97, 0x0B9A wooden signpost; 0x0BD2 brass sign | harbor signs | verified (code) |
| boats | `SmallDockedBoat`, `MediumDockedBoat`, `LargeDockedBoat` and the dragon versions | verified (code, ModernUO multis) |

**Packs**

- **Usable now:**
  - `code\dock-addon`: 4 `.cs` (East, North, South, West), each about 15x16. Too big for the isle; fine for a town
    harbor. Community terms, credit +Qwerty.
  - `catamarans`: 8 multi `.txt` plus previews. "Feel free to add these to your shard"; credit Huntress. Built from
    stock tiles: ship as multi records only.
  - `vertigo-long-dragon-boat`: multi `.txt` exports. Community terms, credit Vert-I-Go.
  - `vertigo-cannon` and `vertigo-ballista` (multi `.txt`) for a harbor battery. Community terms.
- **New client art:**
  - `kevsurcu-raft`: 39 BMP, all directions. Community terms, credit Kevsurcu.
  - `kevsurcu-chinese-boat`: 197 BMP. FLAG: "free exclusively to ServUO" (normally sold); use only inside our
    package, never repost.
  - `kevsurcu-chinese-cargo-ship` (18 BMP) and `kevsurcu-3-chinese-boats` (71 BMP). Community terms.
  - `dream-boat`: 177 BMP. Community terms, credit otimpyre; recoloured boat art (EA).
  - `partial-hue-ships`: 162 BMP. Credit Vert-I-Go and the unknown artist. EA-derived: patch records, new IDs.
  - `odin-jolly-roger` (20 BMP; credit Odin and Dramoor) and `odin-swan-ship` (8 PNG). Community terms.
  - `bridge-support-beam`: 6 BMP, NS and EW beams for a pier underside. "License: none stated", credit gollin.

**Do not use here**

- `orc-encampment`, `valorian-wooden-wall` (palisade): wrong for a trade dock.
- Snow packs, unless it is a northern port.

### Bank

**Stock IDs**

| ID | What | Check |
|---|---|---|
| 0x0B3D-0x0B40 | counter (bank teller counter) | verified (tiledata) |
| 0xA2DA | counter | verified (tiledata); high ID |
| 0x0EED | gold coins (a pile on the counter) | verified (code) |
| 0x1852 | scales | verified (code, Alembic hall) |
| 0x0B1D-0x0B1F, 0x0B26-0x0B28 | candelabra | verified (tiledata) |
| 0x0BD2 brass sign; 0x0BCF wooden sign | sign posts | verified (code) |
| 0x1E5E bulletin board, east face; 0xA0C5 standing bulletin board | notices | verified (code) |
| 0x0A0C | wall torch | verified (code) |
| 0x8B8F, 0x8B90 wall safe; 0x9C18, 0x9C19 safe | vault dressing | verified (tiledata); high IDs |
| 0x0E7C (silver chest), 0x0E40-0x0E43 (metal or golden chests) | vault chests | unverified |
| 0xA62A, 0xA62B | brass fountain, outside the door (as on the isle's bank square) | verified (code) |

**Packs**

- **Usable now:**
  - `code\lagatha-brass-fountains`: three brass fountains (one used). Community terms, credit Lagatha.
  - `code\knives-town-houses`: a system, not decor (rent paid from the bank). Reference only.
- **New client art:**
  - `hestia-misc-3` closed vault doors and `hestia-doors-walls-roofs` open vault doors (ART-LIBRARY;
    `SOURCE.txt` not re-read here).
  - `display-cases`: 18 BMP. Community terms; credit RedRooster and add him to the shard credits.
  - `npc-shop-signs`: 52 BMP. "Feel free to switch out any you don't like or modify this in any manner you like"; credit
    Castiel. They replace stock IDs as shipped: register as new IDs.
  - `marble-walls`: 5 BMP, EA-derived, patch records. `marble-railings`: 72 PNG, no licence file ("check the page's
    terms before shipping").

**Do not use here**

- `otimpyre-465-expansion`: FLAG, the soda machine shows a real brand.
- Torture and dungeon props (`chains`, `caged`).
- Holiday toppers outside an event (`mrriots-christmas`, Halloween bank topper Q#862).

### Guild hall

**Stock IDs**

| ID | What | Check |
|---|---|---|
| 0x2DD4 alchemist table; 0x0E9B mortar and pestle; 0x182A flask; 0x1852 scales; 0x0A9D shelf; 0x0C41 dried herbs; 0x0975 cauldron; 0x184A heating stand; 0x185D vials | the Alembic hall set | verified (code, `ClusterFAlembicGuild.cs`) |
| 0x1586-0x15F5, 0x160F-0x1633 | banner (many crests and colours); 0x158F, 0x1626 banner hanger | verified (tiledata) |
| 0x0426-0x042F | tattered banner (fallen guild) | verified (tiledata) |
| 0x0E31-0x0E33, 0x19AA, 0x19BB | brazier | verified (tiledata) |
| 0x0B1D-0x0B28 candelabra; 0x0A0C wall torch | light | verified |
| 0x0B2C wooden bench; 0x0B4E/0x0B4F chair; 0x0B90 table | seating | verified (code) |
| 0x0972 crossed swords; 0x0953/0x0959 fireplace | hall trim | verified (code) |
| 0x1E5E bulletin board | guild notices | verified (code) |
| 0x4037, 0x4038 gargoyle banner; 0x9FAC-0x9FB3 cult banners (fire, air, earth, water) | themed banners | verified (tiledata); high IDs |

**Packs**

- **Usable now (stock-art designs, `.uoa`):**
  - `argonious-buildings`: 28 `.uoa` (great hall, castles, temples, Elf City). Community terms, credit Argonious.
  - `peoharen-mithril-hall`: a dwarven hall, for the Smiths. IP look: rename. Community terms.
  - `large-castle`, `milva-small-castle`, `milva-3-new-designs`, `stone-building`, `maxus-uoar-designs`. Community
    terms, credit Milva or Maxus; "stock UO tiles: placement data only".
  - `uoar-buildings-package` (188 `.uoa`) and `uoar-database` (1,052 `.uoa`): multi-author. Credit the listed
    builders and the compiler (Hank, MoreBeer).
  - `uoar-structures` (682 `.uoa`): has ripped stock town layouts (EA), so placement data only.
- **New client art:**
  - `god-banners`: 69 BMP, D&D god symbols. Rename the gods. Community terms, credit Vert-I-Go.
  - `walls-new-windows`: 294 BMP. Community terms, credit Carl Hamilton.
  - `hestia-statues-more`: 36 BMP. Community terms.
  - `archin-bust-statues`: 32 BMP. EA-derived.
  - `plated-statues` and `trophies-heads` (Archaaz): EA-derived, patch records only.
  - `hestia-trophies`: 44 BMP. Check each trophy for EA creature art.
  - `display-cases`: credit RedRooster in the shard credits.
  - `archaaz-marble-pieces`: 2 BMP. Credit Archaaz and the Grafikportal artist.
  - `colossus`: 2 PNG. Community terms, credit Odin.
  - For the Artificers: `floating-crystals` (19 BMP, "Use them as you please", credit MrRiots) and `star-tiles`
    (credit RedRooster).

**Do not use here**

- `orc-encampment`, `milva-orc-forts`: an enemy camp look.
- `minecraft-uo`: the kids' dungeon only.
- `otimpyre-465-expansion` soda art (IP).
- `drc1k-uoassets` anywhere we take donations: its terms make donations "commercial use" (see Dungeon entrance).

### Market

**Stock IDs**

| ID | What | Check |
|---|---|---|
| 0x01F0-0x01F9, 0x0230-0x0239, 0x02DE-0x02EC, 0x0368-0x0371 | tent walls; 0x036B tent pole | verified (tiledata) |
| 0x05FF-0x062A, 0x0633-0x0636, 0x0648-0x0651, 0x065E-0x0674 | tent roof (striped stall roofs) | verified (tiledata) |
| 0x0E3C-0x0E3F crate; 0x09A9, 0x0E7E small crate; 0x0E77 barrel; 0x1940 keg | stock on show | verified |
| 0x0C7B cabbage; 0x0C6A pumpkins; 0x0C76 carrots; 0x0C7F-0x0C82 corn; 0x09C9 ham; 0x1E19 fish heads | produce on tables | verified (code + tiledata) |
| 0x0B90 table; 0x0B3D-0x0B40 counter | stalls | verified |
| 0x1852 scales | weighing | verified (code) |
| 0x0BD2, 0x0BCF signs; 0x0B97/0x0B9A, 0xA854 signposts | stall signs | verified (code) |
| 0x1731-0x173E (`StoneFountainAddon`), 0x19C3+ (`SandstoneFountainAddon`) | square fountain | verified (code) |
| 0xA300, 0xA301 | wishing well E/S | verified (tiledata + code "wishing"); high ID |

**Packs**

- **Usable now:**
  - `code\olorin-market-tents`: 8 `.cs`, 8x14 tents (red, blue, green, magenta, ranger, smith, equipment). They use
    stock IDs 0x057B and 0x0521 (55 each), the counter 0x0B3F plus 0x411B and 0xAC31 (check the client draws those two).
    P724 marked them "worth keeping for New Haven's market". Community terms, credit Olorin.
  - `code\lagatha-brass-fountains`: the two unused fountains, for the square.
  - Designs: `peoharen-ville-1`, `peoharen-ville-7`, `large-village-sandstone` (desert market), `city-of-the-sun`.
    `.uoa`, community terms.
- **New client art:**
  - `laoth-wooden-crates`: fruit, veg and fish crates; the best stall fill.
  - `mrriots-storage-crates`, `home-supply-crates`, `hestia-barrels-crates` (see Farm).
  - `ems-picnic-pack`: 8 BMP. Community terms, credit Ems.
  - `satchel`: 3 BMP. No licence file: "check the page's terms before shipping".
  - `npc-shop-signs`: 52 BMP. Register as new IDs.
  - `kevsurcu-royal-carriage`: 8 BMP. Community terms.
  - `farm-carts`: no SOURCE.txt; blocked until sourced.

**Do not use here**

- `drc1k-guillotine-pillory`, `chains`, `caged`: a market is not a gallows square unless the story says so.
- Holiday packs outside their season.

### Shrine

**Stock IDs**

| ID | What | Check |
|---|---|---|
| 0x0002, 0x0003 | ankh, west facing (`AnkhWest`, resurrects) | verified (code) |
| 0x0004, 0x0005 | ankh, north facing (`AnkhNorth`) | verified (code) |
| 0x1D97/0x1D98, 0x1E5C/0x1E5D | bloodied ankh, or ankh of sacrifice | verified (code + tiledata) |
| 0x120E-0x1216 | altar | verified (tiledata) |
| 0x0E31-0x0E33, 0x19AA, 0x19BB | brazier | verified (tiledata) |
| 0x0B1D-0x0B28 | candelabra | verified (tiledata) |
| 0x0C37/0x0C38, 0x0C45-0x0C4E flowers; 0x0C83-0x0C8C campion, foxglove, white flowers | offerings and beds | verified (tiledata) |
| 0x0C8F, 0x0C90 hedge; 0x0DB8, 0x0DB9 hedge | enclosure | verified (tiledata) |
| 0xB02B-0xB02E | ankh vines, floral ankh | verified (tiledata); high ID |
| 0xA4F1-0xA4FA | fountain set B (`B_Fountain_*`) | verified (tiledata); high ID |

Our guild menu already uses 0xE21 (bandage) as the Healers' ankh icon: an icon only, not a placed item.

**Packs**

- **Usable now:** `argonious-buildings` temples (`.uoa`), and the wedding venue `peoharen-wedding` (`.uoa`, stock) for
  a garden shrine. Community terms.
- **New client art:**
  - `god-banners` (rename the gods);
  - `star-tiles` (animated star floor; credit RedRooster in the shard credits);
  - `floating-crystals`;
  - `rooster-aztec-floor` (60 BMP, an Aztec temple floor; community terms);
  - `enchanted-rose` (5 BMP, RedRooster);
  - `sword-in-stone` (8 BMP, otimpyre). FLAG: its lamp post and crystal ball are EA edits.

**Do not use here**

- `otimpyre-fountain-of-blood`, `skeleton-rising`, `chains`, `caged`, `drc1k-uoassets` graveyard: a virtue shrine is
  holy ground. Keep these for an evil shrine or a crypt.
- `minecraft-uo`.

### Garden

**Stock IDs**

| ID | What | Check |
|---|---|---|
| 0x1731-0x173E | stone fountain (`StoneFountainAddon`, 14 pieces) | verified (code) |
| 0x19C3+ | sandstone fountain (`SandstoneFountainAddon`) | verified (code) |
| 0x090D-0x0910, 0x1731-0x175A, 0x19C3-0x19EC | fountain pieces (several stock fountains) | verified (tiledata) |
| 0x11C8, 0x11C9 potted tree; 0x11CA-0x11CC potted plant | pots | verified (code, `PottedTrees` / `PottedPlants`) |
| 0x0C8F, 0x0C90 hedge; 0x0C91, 0x0C92 untrimmed hedge; 0x0DB8, 0x0DB9 hedge | hedges and borders | verified (tiledata) |
| 0x0C37, 0x0C38, 0x0C45-0x0C4E, 0x0D29-0x0D36 flowers; 0x0C83-0x0C8C, 0x0CC0-0x0CC1 named flowers | flower beds | verified (tiledata) |
| 0x4B22-0x4B27, 0xA30D-0xA31B | flower bed corners | verified (tiledata); high ID |
| 0x0CE0, 0x0CE1 walnut tree and leaves; 0x0CE6, 0x0CE7 willow tree and leaves | garden trees (as the isle meadow used) | verified (code) |
| 0x0B2C | wooden bench | verified (code) |
| 0x0E9C-0x0E9F | birdbath | unverified |

**Packs**

- **Usable now:**
  - `milva-pond-bridge` (`.uoa`, a large pond with a bridge, fishable);
  - `code\lake-fishing` (a lake);
  - `peoharen-wedding` (`.uoa`, garden venue);
  - `code\lagatha-brass-fountains`.
  All community terms.
- **New client art:**
  - `azaleas` (3 BMP), `ph-flowers` (4 BMP) and `hanging-baskets` (13 BMP), all by RedRooster. Community terms; he
    asks to be in the shard credits.
  - `garden-statues`: 6 BMP. Community terms, credit Ems; original art.
  - `hestia-garden-items` (25 BMP), `hestia-walls-hedges` (93 BMP: round-top hedges) and `hestia-anim-hedge`
    (108 BMP, animated). Community terms, credit Hestia.
  - `mrriots-spring-plants`: 40 BMP. "Feel free to use and edit them as you wish"; EA-derived: patch records.
  - `mrriots-misc-items-2`: 13 BMP, potted and growing plants. "Use and edit as you wish."
  - `pottery`: 26 BMP. Community terms, credit otimpyre. FLAG: built from EA planter art.
  - `fireflies`: 5 BMP, animated; P725 "Yes, small". Original art, credit Ems; renumber from 0x357F-0x3583.
  - `hestia-misc-1`: 143 BMP, has birdbaths. Community terms.
  - `verdant-autumn-trees`: 36 BMP, **CC0** ("free to redistribute, no attribution required"; credit CorvaeOboro
    anyway). Verdant ones only for a summer garden.
  - `tree-stump-floor`: 16 BMP. Community terms, credit Valorian-Aeternum.
- **Needs Chase's call:**
  - `osi-plants` (82 BMP) and `plants-set-2` (100 BMP), by Thagoras. FLAG: the author says they come from an older,
    abandoned game, likely EA-owned.
  - `butterflies`: flagged rip.

**Do not use here**

- `giant-blue-mushrooms`, `red-giant-mushrooms`: underground light.
- `hallow-trees`: Terraria fey glade only.
- `purple-grass-dirt`.
- `archaaz-halloween` skull trees, except in October.

### Dungeon entrance

**Stock IDs**

| ID | What | Check |
|---|---|---|
| 0x08E0-0x08E9 | stalagmites (the base of `celestial-cave-entrances`) | read from the addon .cs; names verified (tiledata) |
| 0x054A, 0x054C, 0x2166, 0x2167 | cave mouth and rock pieces (same addon) | read from the addon .cs; names unverified |
| 0x1357-0x135C | tall grey boulders | verified (notes, P687) |
| 0x08E0, 0x08E1, 0x08E4, 0x08E5, 0x08E7, 0x08E9, 0x08EA | stalagmites | verified (tiledata) |
| 0x0A0C wall torch; 0x0E31-0x0E33 brazier | lit mouth | verified |
| 0x119A, 0x11A0 | floor spikes (our deployable trap) | verified (code) |
| 0x0026 | fire (red) | verified (code) |
| 0x0426-0x042F | tattered banner | verified (tiledata) |
| 0xB017, 0xB018 | crypt fence S/E | verified (tiledata); high ID |
| 0x0821-0x0823, 0x0849-0x084B | iron fence (gated crypt mouth) | verified (tiledata) |
| 0x08A5, 0x08A6 rope ladder | a pit or shaft way down | verified (tiledata) |

**Packs**

- **Usable now:**
  - `code\celestial-cave-entrances`: 2 `.cs` (East, South) "built for custom instances", stock cave walls. P724
    passed on it, so it is free. Community terms, credit Celestial.
  - `code\svdungeon` and `svdungeon-0.7.0`: procedural interiors behind the mouth (credit appreciated).
- **New client art:**
  - `otimpyre-cave-entrances`: 8 BMP. Community terms.
  - `custom-caves`: 28 BMP. Community terms.
  - `holes`: 20 BMP, pit holes in 5 terrains. Likely from EA solen-hive art: patch records.
  - `hestia-ramps`: 24 BMP. Community terms.
  - `aged-gatedoor`: 6 BMP, one facing. Community terms, credit golfin.
  - `chains` (4) and `caged` (9), by otimpyre. Community terms.
  - `skeleton-rising`: 24 BMP, animated. Credit Archaaz (and Eri for the idea).
  - `otimpyre-fountain-of-blood`: 42 BMP. Community terms.
  - `giant-blue-mushrooms` (29) and `red-giant-mushrooms` (7), by Thagoras. RIP (allowed); rename.
  - `ore-stalagmites` and `hued-orestones`, for mine mouths (ART-LIBRARY).
  - `drc1k-uoassets`: 424 BMP. Dungeon wall set, gray rocks, sewer, blue stone, graveyard. Its terms are the strictest
    on disk:
    - "Non-commercial use only. Commercial use INCLUDES SOLICITING DONATIONS";
    - "NO MODIFICATIONS without his permission";
    - shipping inside the client is allowed; reposting is not.

**Do not use here**

- `star-tiles`, `floating-crystals`, `rainbow-sign`, `hallow-trees`: too bright and festive for a threat at the door.
  Fine for a fey or sky dungeon.
- `farm-carts`, market crates.
- Snow packs, unless the dungeon is in the north.

### Tropical isle

**Stock IDs** (P725 counted these on Buccaneer's Den and planted the Wakening Isle with them; all verified in
`notes\cc-P725-isle-shore-tiles.md`, and the palms again in tiledata)

| ID | What |
|---|---|
| 0x0C95 coconut palm, 0x0C96 date palm | tall palms (beach tier) |
| 0x0C99-0x0C9D | small palms |
| 0x0CA6 | ponytail palm |
| 0x0C9F-0x0CA4 | ferns (the commonest undergrowth) |
| 0x0C97 elephant ear, 0x0C98 fan plant, 0x0C93 blade plant, 0x0C9E o'hii, 0x0CA9 snake plant, 0x0CC4 pampas | jungle plants |
| 0x0CA8, 0x0CAA, 0x0CAB | banana trees |
| 0x0D41-0x0D93 | OSI's jungle trees. Lay them whole along the NE diagonal, e.g. D45, D46, D41+D47, D42+D48, D43+D49, D44+D4A, D4B (`jungle-trees.json`) |
| 0x0587-0x0594, 0x0586/0x05D1-0x05EC | palm fronds; palm-frond roof (huts) |
| 0x179D-0x17B2 | surf pieces on the shore |
| shells, nets, anchors, wreck | see Beach and coast |

Tiers that worked on the isle (P725):

- **Beach:** sparse coconut, date and small palms.
- **Edge:** palms, pampas, ferns.
- **Middle:** banana, o'hii, ferns, fan and elephant-ear plants.
- **Deep:** jungle trees and dense ferns.

Keep 3 tiles clear of roads and stops, and 4 round buildings.

**Packs**

- **Usable now (already placed on the isle):**
  - `celestial-shipwrecks` (West);
  - `new-lighthouse`;
  - `moongate-structure` (credit Carl Hamilton);
  - `lagatha-brass-fountains`.
  `celestial-shipwrecks` East and North, and `shipwreck-addon-70`, are spares for other isles.
- **New client art** (P725's draft client-package prompt lists exactly these):
  - `beach-trees`: broad shade trees for the beach and edge tiers. Credit ParanoiaPhD.
  - `bamboo`: 31 BMP. Clumps 01-16 and the tall stem-plus-leaf pairs 20a/b-25a/b, for the middle and deep tiers.
    Community terms, credit Thagoras; "register in the art registry before use".
  - `laoth-wooden-crates`: banana and orange crates by the farmhouse.
  - `mrriots-firepit`: 8 BMP, animated, for the camp. "Use and edit as you wish."
  - `fireflies`: night ambience. Renumber.
  - `african-trees`: only the aloe (`Aloe a/b`) and lovegrass (`Lovegrass a1-a3, b1-b2`) for the beach edge.
    "Feel free to modify for your own purposes."
- **Later / Chase's call:**
  - `seagulls` (flagged rip);
  - `otimpyre-under-the-sea` and `waterplants` for shallows;
  - `sea-creatures` for the sea around it.

**Do not use here**

- `african-trees` savanna trees (dry and rainy season acacias) and `african-savana-tree`: a dry savanna look. Only the
  aloe and lovegrass are allowed.
- `verdant-autumn-trees` (autumn leaves), `tall-trees`, `kevsurcu-big-trees`, `new-tree-art`: big temperate trees.
  P725 said "No": "a landmark tree would fight the jungle look". `tall-trees` also replaces stock IDs.
- `hank-stumps-saplings`: temperate stumps; also EA-derived.
- `arctic-pack`, `winter-holiday`, `mrriots-winter`, `rooster-animated-snow`, `xmas-community-tree`, and stock snow
  hedge 0xA600-0xA603: snow on a tropical beach.
- `purple-grass-dirt`, `purplegrass-to-dirt`, `altered-lands` snow and dune sets: wrong land. `altered-lands` is also
  EA paintover land.
- `hallow-trees`: Terraria, a fey look.
- `butterflies`: flagged rip.
- `dock-addon`: its 15x16 platforms would cover P720's dock.
- `da-training-hall` (96x45 tiles): no room on the isle.
- `farm-carts`: no SOURCE.txt.

---

### Packs looked at (139)

I read `SOURCE.txt` (or saw it was missing) and counted the file types for each pack below. `D:\UO\third-party` holds
406 folders at the top (with `_ec-preview`, `_scout` and `code`) and 66 under `code\`. The rest are creatures, gear,
UI, audio and holiday packs that fit none of these ten places.

- **`code\` addons (11):** celestial-shipwrecks, shipwreck-addon-70, new-lighthouse, dock-addon,
  lagatha-brass-fountains, olorin-market-tents, lake-fishing, celestial-cave-entrances, moongate-structure,
  sparring-dummy, knives-town-houses.
- **Plants, farm, garden (30):** beach-trees, bamboo, african-trees, african-savana-tree, laoth-wooden-crates,
  mrriots-firepit, fireflies, seagulls, sea-creatures, farm-carts, irrigation-ditch, hank-stumps-saplings,
  verdant-autumn-trees, tall-trees, kevsurcu-big-trees, new-tree-art, osi-plants, plants-set-2, azaleas, ph-flowers,
  hanging-baskets, pottery, garden-statues, hestia-walls-hedges, hestia-anim-hedge, hestia-garden-items,
  mrriots-spring-plants, mrriots-misc-items-2, hallow-trees, butterflies.
- **Coast, dock, market (31):** transparent-water, atlantis-tiles, mini-mermaid-statues, mermaid-statues,
  otimpyre-under-the-sea, waterplants, otimpyre-flooded-illusion, catamarans, partial-hue-ships, odin-jolly-roger,
  odin-swan-ship, kevsurcu-raft, kevsurcu-chinese-boat, kevsurcu-chinese-cargo-ship, kevsurcu-3-chinese-boats,
  dream-boat, treasure-items, vertigo-long-dragon-boat, mrriots-storage-crates, home-supply-crates, satchel,
  ems-picnic-pack, valorian-wooden-wall, orc-encampment, kevsurcu-royal-carriage, bridge-support-beam, npc-shop-signs,
  hestia-barrels-crates, hestia-water-barrel, mrriots-misc-3, hestia-misc-1.
- **Bank, guild, shrine, dungeon (33):** god-banners, marble-railings, marble-walls, archaaz-marble-pieces,
  hestia-statues-more, archin-bust-statues, display-cases, walls-new-windows, otimpyre-465-expansion, dragon-mailbox,
  plated-statues, trophies-heads, hestia-trophies, colossus, argonious-buildings, otimpyre-cave-entrances, holes,
  custom-caves, drc1k-uoassets, giant-blue-mushrooms, red-giant-mushrooms, chains, caged, aged-gatedoor,
  otimpyre-fountain-of-blood, skeleton-rising, hestia-ramps, star-tiles, floating-crystals, rooster-aztec-floor,
  otimpyre-halloween-fountain, sword-in-stone, enchanted-rose.
- **Designs, land and seasonal (34):**
  - Designs: milva-pond-bridge, milva-tree-house-village, milva-small-tree-village, tree-house, peoharen-ville-1,
    peoharen-ville-7, peoharen-wedding, peoharen-mithril-hall, city-of-the-sun, large-village-sandstone,
    akhentef-sandstone-castle, milva-orc-forts, milva-small-castle, large-castle, stone-building, wooden-building,
    milva-3-wood-building, milva-3-new-designs, uoar-database, uoar-structures, uoar-buildings-package,
    maxus-uoar-designs.
  - Siege multis: vertigo-ballista, vertigo-cannon.
  - Snow and holiday: arctic-pack, winter-holiday (no SOURCE.txt), mrriots-winter, rooster-animated-snow,
    xmas-community-tree, archaaz-halloween, mrriots-spring-easter.
  - Land: altered-lands, purple-grass-dirt, tree-stump-floor.

**Stock-art packs (usable now), 37 of the 139:**

- the 11 `code\` addons (2 of them are systems rather than decor: sparring-dummy, knives-town-houses);
- the 22 `.uoa` designs;
- 4 multi exports: catamarans, vertigo-long-dragon-boat, vertigo-ballista, vertigo-cannon.

Every other pack listed ships images or `.vd` files and needs new client art.

## 11. Lessons from the P734 practice builds

Six practice builds (farmhouse, bank, League lodge, bridge and pier, market corner, two-story house) were laid by
this guide's rules on a private shard, walked, shot and reviewed by a second Claude. The gallery is
`notes/cc-P734-practice/gallery.md`; the builds are `[PlaceBuild practice-<name>` files. What the first review round
caught, and the rule each one became:

1. **The corner tiles.** Every building and the fence had the wrong piece at the south-west corner. Write the corner
   rule as code (post NW, "south" piece to the NE tile, "east" piece to the SW tile, L corner SE) and check the four
   corner tiles of every box in the cut-away render.
2. **Read every facing from the art, not from a name or an older build.** The chairs, the carpet edges, the sign arm
   (0x0B97 lies along a wall, 0x0B98 sticks out) and the fence's L corner (0x0835) were all wrong in P734's first
   round, some copied from the isle's own layout. Before using a piece whose facing matters, render it alone
   (`render_addons.py ids:0x...`) and look. A reviewer's facing claim is checked the same way: round 1 swapped the
   carpet's corner pieces from the art, round 2 drew both versions side by side and the swap was wrong. When two
   readings disagree, render both and keep the one that draws whole.
3. **Tall pieces against roofs and floors.** A stone fireplace is 24 high: against a side wall under a pitched roof its
   chimney comes through the low eaves (Chase's "gray thing on the roof"), and under a floor 20 above it comes through
   that floor. Put hearths on the north wall under the roof's high middle, or upstairs under the roof.
4. **Furniture and windows.** Do not stand a bookcase, hearth or bed in front of a window, or hang a torch on a window
   tile; check each window tile's floor neighbour in `placed.md`.
5. **Signs beside, not on, the door.** A sign one tile east of a south door draws over the door leaf; two tiles east
   (as OSI's houses do) clears it.
6. **Water statics are not water.** Water statics on dry land at their own Z block nothing, so a walker strolls across
   a fake pond. A dock or bridge needs a real shore (land water or water statics at the sea's -5 over land at -15); if
   the place has none, choose another place or make the shore with a map change first.
7. **Start a deck on flat bank, not on the edge tile.** The last land tile before deep water is a steep slope (its
   corners run from the bank's Z down to the lake bed), so its standing Z is far below the bank's; a bridge that
   began beside it stuck the walker there (round 2). Lay the first plank on the edge tile itself, at a Z one above the
   flat bank behind it, and walk it.
8. **Rails on the deck's outer rows, never across a join.** OSI's docks put rope rails on the outer rows and columns
   of the deck at deck + 5 and stack the posts (0x03AE -5, 0x03A5 0, 0x03AB +5); a rail across the mouth where a
   pier meets a bridge blocked the walk.
9. **Walk routes are not straight lines.** A walker that hits a table drifts a tile and then cannot line up with the
   door again; route the walk round furniture and count no progress along the leg as stuck. TazUO opens a door or
   gate walked into (its auto-open option), as a player's client does.
10. **NPCs in a build file.** A decoration file can keep an NPC with a spawner line, for example
   `Spawner (Spawn=Banker; Count=1; HomeRange=0; WalkingRange=0)` on the keeper's tile.
11. **What a reviewer needs:** the cut-away renders (roof off, each storey), the outside shot from the door side (the
    north-west view shows only roofs), `placed.md` with the wall each piece hangs on, and the walk logs.
