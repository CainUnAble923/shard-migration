# P734 practice builds: build review, round 3

Reviewer: a second Claude, read-only. I did not make these builds and I wrote neither earlier round. I checked the
work against `notes/guides/building-and-decorating.md` (sections 1-11, with What to use where).

## What I looked at

The farmhouse, bank and lodge were regenerated and placed again after round 2, so I reviewed those three again in
full, not only round 2's items. For each I used:

- `placed-<build>.md`, checked line by line against `practice-<build>.cfg` (they agree);
- `render-<build>.jpg`, `render-<build>-inside.jpg` and the new shots `<build>-outside/front/inside.jpg`;
- the walk logs.

I also made my own isorender drawings, in my scratch area only:

- each of the three cfgs with the south wall row and the east wall column cut away, at 1.6-2x;
- each with its roof on;
- a 3x zoom of the lodge's north-west corner;
- pieces drawn alone on a tile grid at 2-3x:
  - a light wood north wall and east wall with SmallBedSouth one tile in from the east wall;
  - 0x0B4F and 0x0B50 north and south of a 0x0B90 table;
  - the 5x3 carpet both ways (NW 0x0ACA / SE 0x0AC9, and swapped);
  - the runner 0x0ACD + 0x0AC8 x3 + 0x0ACF;
  - 0x0A99 x3 and 0x0A97 against a 0x0035 west wall run.

The dock, market and twostory `.cfg` files did not change since round 2. I spot-checked them against round 2's
description: the stair 0x0739 is at 8,7,0 to 8,4,15, the upstairs bed is at 3,3,20, and the fountain is at 9,8,0.
Their shots and walk logs are the same files round 2 read. I repeat round 2's verdicts for them.

## Facts I checked from the art

- **Carpet corners.** Round 1 and round 2 disagreed here, so I drew both ways myself.
  - With NW 0x0ACA and SE 0x0AC9, the 5x3 frame closes whole.
  - Swapped (NW 0x0AC9, SE 0x0ACA), each of those two corners draws a loose tuft one tile past the carpet's north
    and south points, and the frame is notched there.
  - Round 2 is right, and the bank now follows it.
- **Runner.** 0x0ACD, 0x0AC8, 0x0AC8, 0x0AC8, 0x0ACF along x draws one whole runner with a fringe at the west and
  east ends.
- **Bookcases.** 0x0A99 drawn against a 0x0035 west wall run stands flat on the wall, with its books facing east into
  the room. 0x0A97 on the next tile stands edge-on to that wall: it faces south, as round 2 said. So 0x0A99 is the
  right west-wall case.
- **Chairs.** 0x0B4F north of the table has its back on its north edge and faces the table. 0x0B50 south of the
  table has its back on its south edge and faces the table. Both agree with guide 3.
- **Where an "east" wall piece stands.** I drew 0x00A7 on a tile grid: its base runs along the tile's east edge, from
  the right corner to the bottom corner, as guide 2.2 says. So the wall tile of an east column is the wall's own tile,
  and its floor shows west of the wall line.

## Round 2, item by item

**farmhouse:**

1. The bed floated mid-room. Fixed, but **not as written**, and I accept the change (reasons below).
   - Round 2 asked for the bed at 8,3. The bed is now SmallBedSouthAddon at 7,3,0: head 0x0A63 at 7,3, foot 0x0A5C
     at 7,4.
   - The east window 0x00B9 moved from 8,3 to 8,5 as asked, and 8,3 is now plain 0x00A7.
   - Why 7,3 is right:
     - 8,3 holds the east wall piece itself, an impassable wall tile, so a bed there would share the tile with the
       wall.
     - The bed's head is now on the north wall line. In my cut-away the headboard touches the north wall 0x00A8 at
       7,2, beside the hearth.
     - Its long side runs north-south, one tile in from the east wall line. The only thing between it and that line
       is the east wall's own tile (8,3 and 8,4), where nothing can stand.
     - This is exactly how the isle farmhouse has it, which Chase accepted (guide 2.5, "Furnishing that worked"). In
       `TutorialIsleFarmLayout.cs` the east wall column is x 6693 and the north wall row is y 3972. The bed 0x0A63 is at
       6692,3973 and 0x0A5C at 6692,3974: one tile in from the east column, head on the north wall.
   - Guide 3 says "the bed's head against a wall (SmallBedSouth along an east wall)", and the bed now meets it.
   - Rule 11.4 (furniture in front of windows): the bed's tiles 7,3-7,4 are not the floor tile of any window. The
     east window 8,5 has 7,5 in front of it, and 7,5 is clear.

**bank:**

1. Carpet corners swapped. Fixed: 0x0ACA is at 4,5,0 (NW) and 0x0AC9 at 8,7,0 (SE).
   - My render of the cfg shows the frame closed with no tufts.
   - Guide 2.5 now reads NW 0x0ACA, SE 0x0AC9.

Round 2's two notes are unchanged:

- The bench 0x0B2C at 9,6,0 stands one tile in from the east wall line, the same as the bed above.
- The torch 0x0A0C at 5,3,13 hangs over the banker's spawn tile.

Neither is a failure.

**lodge:**

1. West-wall bookcases edge-on. Fixed: the cases at 3,4,0, 3,6,0 and 3,7,0 are now 0x0A99.
   - My cut-away and its 3x corner zoom show all three flat on the west wall, facing east.
   - So do `lodge-inside.jpg` and the lodge's west wall in `bank-inside.jpg` and `bank-front.jpg`.
   - Guide 2.5 and 3 now name 0x0A99 for a west wall.
2. Runner a fringe strip. Fixed: 0x0ACD at 5,8,0, 0x0AC8 at 6,8,0 to 8,8,0, and 0x0ACF at 9,8,0.
   - My cut-away shows one whole runner with fringed ends and no loose corner.

## farmhouse (origin 5700,1170)

Walls:

- Light wood walls, x2-8 by y2-7:
  - post 0x00A9 at 2,2;
  - 0x00A8 along the north row from 3,2 to the NE tile 8,2, and along the south row;
  - 0x00A7 down the west column from 2,3 to the SW tile 2,7, and down the east column 8,3-8,6;
  - L corner 0x00A6 at 8,7.
- Nothing is missing or doubled. The four corners are clean in my cut-away and in the front shot.

Windows:

- 0x00BA at 4,2 and 7,7 in the east-west walls; 0x00B9 at 2,4 and 8,5 in the north-south walls.
- The tile in front of each window is clear: 4,3, 7,6, 3,4 and 7,5.

Door:

- DarkWoodDoor WestCCW (0x06A9) at 5,7, in the south wall line.
- `walk-farmhouse.log` (new) goes 5,9 to 5,5 through it and back, all at Z 0, with no STUCK.

Floor and roof:

- The floor 0x04A9-0x04AC covers x3-8, y3-7.
- Thatch 0x05A6 / 0x05A4 at 20, 23 and 26, with the ridge 0x05A5 at 6 at Z 29, covers x3-9, y3-8.
- The gables 0x00C1 are on the south row.
- Nothing sits on the roof. The hearth's top is 24, under thatch at 26 (x5) and 29 (x6); the front and outside shots
  show nothing through the roof.

Inside:

- StoneFireplaceSouthAddon is at 6,3, on the north wall under the ridge.
- The bed is at 7,3-7,4, as above.
- The table 0x0B90 is at 4,5, with 0x0B4F north and 0x0B50 south, both facing it, and a plate on it at Z 6.
- The barrel is at 3,3 and the flour at 3,6.
- The torch 0x0A07 is at 3,5,13, on the plain west wall at 2,5.

Sign and yard:

- The sign is 0x0B98 + 0x0BD2 "Practice farmhouse" at 7,8,5, two tiles east of the door. The front shot shows it
  beside the door, not over it.
- The fence ring follows the rule:
  - post 0x0838 at 10,3;
  - 0x0836 along the north row to the NE tile 16,3, and along the south row;
  - 0x0837 down the west column to the SW tile 10,8, and down the east column;
  - L corner 0x0835 at 16,8;
  - one LightWoodGate at 10,5.

BUILD REVIEW farmhouse: PASS

Could not judge:

- In TazUO the bed shows only as a sliver of bedding beside the hearth (`farmhouse-inside.jpg`). The east wall hides
  the rest from the default camera, so I judged its place from my cut-away.
- The gate's walk (`walk-farmgate.log`, 9,5 to 12,5 and back at Z 0) dates from before this placement. The fence and
  gate lines in the cfg are the ones round 2 described, so I take it as still valid.
- `farmhouse-outside` (from the north-west) shows only the roof.

## bank (origin 5720,1170)

Walls:

- Stone shop walls, x2-10 by y2-8:
  - post 0x005A at 2,2;
  - 0x0058 along the north row to the NE tile 10,2, and along the south row;
  - 0x0057 down the west column to the SW tile 2,8, and down the east column;
  - L corner 0x0059 at 10,8.
- Nothing is missing or doubled.

Windows:

- 0x005E at 4,2, 8,2, 3,8 and 9,8 in the east-west walls; 0x005D at 2,5 and 10,5 in the north-south walls.

Door:

- WestCCW 0x06A9 at 6,8, in the south wall line.
- `walk-bank.log` goes 6,10 to 6,5 and back at Z 0.

Floor and roof:

- The floor 0x049C covers x3-10, y3-8.
- Shingles 0x05C4 / 0x05C3 at 20-29 cover x3-11, y3-9, with the ridge 0x05C2 on x7 at 32.
- The gables 0x0069 are on the south row. Nothing sits on the roof, in my render and in `bank-front.jpg`.

Inside:

- The counter 0x0B40 runs along y4 from x3 to x8, with a gap at 9,4.
- The Spawner (Banker) is at 5,3, and the banker stands behind the counter in `bank-inside.jpg`.
- The vault chests 0x0E41 / 0x0E40 / 0x0E41 are at 4,3, 6,3 and 8,3.
- The candelabras 0x0B26 are at 3,7 and 9,7, and the bench 0x0B2C at 9,6.
- The torches: 0x0A0C at 5,3,13 and 7,3,13 on the plain north wall at 5,2 and 7,2; 0x0A07 at 3,6,13 on the plain
  west wall at 2,6.
- The 5x3 carpet at x4-8, y5-7 has the right corners, edges and centre (see above). It lies between the counter and
  the door, for the queue.

Sign:

- 0x0B98 + 0x0C0B "Practice Bank" at 8,9,5, two tiles east of the door. The arm sticks out from the wall, and the
  board is clear of the door leaf in `bank-front.jpg`.

BUILD REVIEW bank: PASS

Notes, not failures:

- **Chests by the north windows.** The low vault chests at 4,3 and 8,3 stand in front of the north windows 4,2 and
  8,2. Rule 11.4 names bookcases, hearths, beds and torches, and the chests are below the sills; my cut-away shows
  both windows whole above them.
- **Candelabras by the south windows.** The candelabras at 3,7 and 9,7 stand inside the south windows 3,8 and 9,8.
  They are thin and do not hide the windows from outside in `bank-front.jpg`. Moving them one tile in (to 3,6 and
  9,5) would keep 11.4 to the letter.

Could not judge:

- The carpet's south half is behind the south wall in TazUO, so I judged it from my render.
- `walk-bank.log` dates from before this placement, but the door tile (6,8) did not change.

## lodge (origin 5740,1170)

Walls:

- Grey brick walls, x2-12 by y2-9:
  - post 0x0036 at 2,2;
  - 0x0034 along the north row to the NE tile 12,2, and along the south row;
  - 0x0035 down the west column to the SW tile 2,9, and down the east column;
  - L corner 0x0033 at 12,9.
- Nothing is missing or doubled.

Windows:

- 0x003B at 3,2, 11,2, 4,9 and 10,9 in the east-west walls; 0x003C at 2,5, 2,8 and 12,6 in the north-south walls.
- The tile in front of each window is clear of furniture: 3,3 has only the west-wall torch (see the note), and 11,3,
  4,8, 10,8, 3,5, 3,8 and 11,6 are empty.

Door:

- WestCCW 0x06A9 at 7,9, in the south wall line.
- `walk-lodge.log` goes 7,11 to 7,8 and back at Z 0.

Floor and roof:

- The floor 0x04FC-0x04FF covers x3-12, y3-9.
- Shingles at 20-32 cover x3-13, y3-10, with the ridge 0x05C2 on x8 at 35.
- The gables 0x0055 are on the south row. Nothing sits on the roof.
- The hearth (top 24) is under roof at 29 (x6) and 32 (x7).

Inside:

- StoneFireplaceSouthAddon is at 7,3, on the north wall.
- Bookcases:
  - 0x0A98 at 4,3, 5,3, 9,3 and 10,3, flat on the plain north wall and facing south;
  - 0x0A99 at 3,4, 3,6 and 3,7, flat on the plain west wall and facing east.
- The long table 0x0B90 runs 6-9,6, with 0x0B4F chairs on y5 and 0x0B50 chairs on y7, all facing it, and the book
  0x0FEF on the table at 7,6,6.
- The candelabra 0x0B26 is at 11,4.
- The torches: 0x0A0C at 8,3,13 on the plain north wall at 8,2; 0x0A07 at 3,3,13 on the plain west wall at 2,3.
- The runner is at y8, x5-9.

Outside:

- The banners 0x1589 at 13,4,8 and 13,7,8 hang flat on the outside of the east wall (round 2 drew the art; my roof
  render and `lodge-front.jpg` agree).
- The sign is 0x0B98 + 0x0BD2 "Practice League lodge" at 9,10,5, two tiles east of the door.

BUILD REVIEW lodge: PASS

Notes, not failures:

- **The corner torch.** The west-wall torch 0x0A07 at 3,3,13 is on the floor tile in front of the north window 3,2.
  It hangs on the plain west wall at 2,3, and my 3x zoom shows the window whole beside it, not covered. If you want
  rule 11.4 kept to the letter, use 3,4,13 (plain 2,4) instead, which puts it above the 0x0A99 case there.
- **Through the south window.** The red seen through the south window 10,9 in `lodge-front.jpg` and in my roof
  render is the runner's east end 0x0ACF at 9,8, directly behind that window on screen. It is not a stray piece.
- **Stale gallery line.** The gallery (`notes/cc-P734-practice/gallery.md`, lodge row) still says "bookcases 0x0A98
  north / 0x0A97 west". It should say 0x0A99 west.
- **Guide 2.5's lodge line.** It still opens "bookcases 0x0A97 along the west wall" before its own correction in
  brackets. It would read better as "0x0A99 along the west wall".

Could not judge:

- The runner and the y8 row are behind the south wall in `lodge-inside.jpg`, so I judged them from my cut-away.
- `walk-lodge.log` dates from before this placement, but the door tile (7,9) did not change.

## dock (origin 1550,612, a real lake)

The `.cfg`, shots and walk logs are unchanged since round 2, and I repeat round 2's verdict:

- the bridge joins are walked both ways at bank Z 1 and deck Z 2;
- the pier is walked at Z 6 from end to end;
- the rails and posts follow 4.3;
- the shore is real.

BUILD REVIEW dock: PASS

## market (origin 5722,1195)

The `.cfg` and evidence are unchanged since round 2, and I repeat round 2's verdict. Round 2's suggestions still
stand: a fourth lamp at the NE corner, the hay moved by the flour stall, and more fish on the fish stall.

BUILD REVIEW market: PASS

## twostory (origin 5742,1195)

The `.cfg` and evidence are unchanged since round 2, and I repeat round 2's verdict. Round 2's could-not-judge on
the under-stair fill still stands: a 0x0738 block at 8,4,10 would close the open 10-15 band.

BUILD REVIEW twostory: PASS

## Verdicts

BUILD REVIEW farmhouse: PASS
BUILD REVIEW bank: PASS
BUILD REVIEW lodge: PASS
BUILD REVIEW dock: PASS
BUILD REVIEW market: PASS
BUILD REVIEW twostory: PASS
