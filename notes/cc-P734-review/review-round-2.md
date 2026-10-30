# P734 practice builds: build review, round 2

Reviewer: a second Claude, read-only. I did not make these builds and I did not write round 1. I checked the work
against `notes/guides/building-and-decorating.md` (sections 1-11).

Evidence I used:

- the six `placed-*.md` lists, checked against the six `practice-*.cfg` files (same dates, same pieces);
- every render and every TazUO shot in `notes/cc-P734-review/`;
- the eight walk logs, converted to relative coordinates by subtracting each origin;
- tiledata from the client copy;
- my own isorender renders, made in my scratch area and not in the repo:
  - each build's cfg, with the south row and east column cut away, at 1.5x;
  - the pieces whose facing matters, alone at 2-4x: the chairs, the sign arms, 0x0B40, the bookcases 0x0A97-0x0A9E,
    the carpet corners, the banner 0x1589, the rope 0x14F8 and the rope rails;
- the water statics of the dock's lake, read from the overlay map.

## Round 1, item by item

**farmhouse:**

1. SW corner: done. 0x00A7 is at 2,7,0, and the corner is clean in the render and the front shot.
2. Fireplace through the roof: done. StoneFireplaceSouthAddon is at 6,3,0 on the north wall. Its pieces are 24 high
   (top Z 24); the thatch over them is at Z 26 (x5) and 29 (x6). Nothing shows through the roof in the render or the
   front and outside shots.
3. West window hidden: done. The fireplace left the west wall, and window 2,4 has a clear floor tile at 3,4.
4. Torch on a window: done. 0x0A07 is at 3,5,13, on the plain 0x00A7 at 2,5.
5. Chairs: done. 0x0B4F is at 4,4 and 0x0B50 at 4,6. I drew both from the art, and each faces the table.
6. Sign: done. It is at 7,8,5, two tiles east of the door; the front shot shows it beside the door, not on it.
7. Fence NW: done. 0x0838 is at 10,3; drawn alone, it is a plain post.
8. Fence SW: done. 0x0837 is at 10,8,0.
9. Water barrel: done. 0x154D is at 9,7,0.

**bank:**

1. SW corner: done. 0x0057 is at 2,8,0.
2. Banker: done. A Spawner line at 5,3 makes the banker, and he stands behind the counter in `bank-inside.jpg`.
3. Carpet:
   - The edges are done: west 0x0ACD, east 0x0ACF, north 0x0ACE, south 0x0AD0.
   - The corners are **not** fixed. They now follow round 1's corner advice, and that advice was wrong (bank fix 1
     below).
4. Sign: done. 0x0B98 + 0x0C0B are at 8,9,10, clear of the door. The arm sticks out from the wall.

**lodge:**

1. SW corner: done. 0x0035 is at 2,9,0.
2. Torch in the chimney: done. It is at 8,3,13, on plain 0x0034 at 8,2.
3. Torch on a window: done. It is at 3,3,13, on plain 0x0035 at 2,3.
4. Bookcases over windows: done. The windows moved to 3,2, 11,2, 2,5 and 2,8, and no case stands on a window's floor
   tile. But the west-wall cases are the wrong piece (lodge fix 1).
5. Chairs: done. 0x0B4F is on the y5 row and 0x0B50 on the y7 row.
6. Sign: done. It is at 9,10,5.

**dock:**

1. Water that blocks: done. The build moved to a real lake. Its water statics (0x1797-0x179C, 0x17A3, 0x17AB, 0x17B0
   and others) are Impassable|Wet at -5 over land at -15.
2. Shore: done. The lake has shore pieces: the surf pieces 0x17A3/0x17A4/0x17A8/0x17AB/0x17AD/0x17AE/0x17B0 sit along
   its edges, and the shots show sand and grass banks.
3. Rail across the pier mouth: done (moot). The pier no longer joins the bridge.
4. Pier walked: done. `walk-pier.log` walks 16,23 to 16,16 and back at Z 6 throughout.
5. Rails and posts as 4.3: done.
   - The rails are at deck + 5, on the deck's outer rows (y6 and y8) and outer columns (x15 and x17).
   - Every post is stacked 0x03AE (deck - 5), 0x03A5 (deck), 0x03AB (deck + 5).
6. A real pier: done. Its free north end stands over water, with rails on both sides and a rope across the end.
7. Lily pad: done (removed).

**market:**

1. Signpost: done. It moved to 0,13, and the walk along y10 has no stall.
2. Centrepiece: done. A StoneFountainAddon fills 7-10, 6-9.
3. Stall stock: done.
   - What is on the counters: a fruit basket 0x0993 with a peach and grapes; a fish steak and two small fish; two
     flour sacks and a ham. The hay is now on the ground behind the stalls.
   - Zoomed in, `market-square.jpg` shows each stall's trade.

**twostory:**

1. SW corner: done. 0x0137 is at 2,8,0 and 2,8,20.
2. Fireplace through the upper floor: done.
   - The hearth is now upstairs: StoneFireplaceSouthAddon at 6,3,20 (top Z 44), under roof courses at 46 (x5) and
     49 (x6).
   - The bed moved off the hearth's tiles, to 3,3,20.
3. West window hidden: done. Window 2,5 has a clear floor tile at 3,5.
4. Chairs: done. 0x0B4F is at 5,4 and 0x0B50 at 5,6.
5. Sign: done. It is at 6,9,5.

## Findings that apply to more than one build

- **Carpet corners: round 1 swapped them, and the guide (2.5) repeats the swap.**
  - I laid the bank's 5x3 carpet both ways in isorender. With NW 0x0AC9 and SE 0x0ACA (as built, and as guide 2.5
    now says), each of those two corners draws a small detached tuft out past the carpet's point. The carpet body
    has a notch at the north and south points.
  - With **NW 0x0ACA and SE 0x0AC9** (what P720's isle survey read), the frame closes whole.
  - The edges (N 0x0ACE, S 0x0AD0, W 0x0ACD, E 0x0ACF) and the NE 0x0ACC and SW 0x0ACB corners are right.
  - The guide's line in 2.5 should go back to NW 0x0ACA, SE 0x0AC9.
- **0x0A97 is not a west-wall bookcase.**
  - Drawn alone, 0x0A97 and 0x0A98 are the same orientation: long axis east-west, books on the south face, so both
    hang on a north wall.
  - The east-facing cases (long axis north-south, books on the east face) are 0x0A99, 0x0A9A and 0x0A9C. I drew them
    against a 0x0035 wall run and they sit flat on it.
  - Guide sections 2.5 and 3 ("0x0A97 along a west wall") are wrong.
- Wall corners, doors and signs: these now pass in every building.
  - Every box has the post at NW, the "south" piece to the NE tile, the "east" piece to the SW tile and the L corner
    at SE. Each storey checks out the same way, and so does the fence.
  - Every door is a WestCCW 0x06A9 in its south wall. The walks went through every door and the gate both ways at
    Z 0 (TazUO opens them).
  - Every sign is 0x0B98 two tiles east of its door.

## farmhouse (origin 5700,1170)

What passes:

- Walls x2-8, y2-7 are whole, and the floor lies at x3-8, y3-7.
- The thatch roof covers x3-9, y3-8 at Z 20/23/26/29, with the ridge on x6 and the 0x00C1 gables on the south row.
- The hearth stands on the north wall under the ridge. The table and chairs are right. The barrel and flour are in
  the corners, and the torch is on plain west wall.
- The fence ring follows the rule, with one gate. Walked: door 5,9 to 5,5 and back; gate 9,5 to 12,5 and back; all
  at Z 0.

BUILD REVIEW farmhouse: FAIL

1. SmallBedSouthAddon (0x0A63 head at 7,5,0, 0x0A5C foot at 7,6,0) stands free in the room.
   - Its head is two tiles from the north wall, and a tile of floor (x8) lies between it and the east wall. My
     cut-away shows it floating mid-floor.
   - The guide (3) wants "the bed's head against a wall (SmallBedSouth along an east wall)".
   - Fix: move the east window 0x00B9 from 8,3,0 to 8,5,0, and put plain 0x00A7 at 8,3,0. Then place the bed at
     8,3,0 (head 8,3 against the north wall, foot 8,4, along the east wall). Check that no window's floor tile is
     under it (rule 11.4).

Could not judge:

- The bed and the flour sack are hidden behind the south and east walls in both TazUO shots.
- `farmhouse-outside` (from the NW) shows only the roof.

## bank (origin 5720,1170)

What passes:

- Walls x2-10, y2-8 with the stone shop set (0x0057 N-S, 0x0058 E-W). Windows: 0x005E in the E-W walls and 0x005D in
  the N-S walls.
- The grey slate floor is at x3-10, y3-8.
- The shingle roof covers x3-11, y3-9 at Z 20-32, with the ridge on x7 from y3 to y9 and the 0x0069 gables on the
  south row.
- The counter 0x0B40 runs along y4 from 3 to 8, with a gap at 9. I drew it alone: it is a symmetric legged board with
  no back or front, so its facing is not a question.
- The vault chests and the banker are behind the counter. The candelabras stand in the SW and SE corners.
- The torches hang on plain wall (5,2, 7,2, 2,6).
- The sign 0x0B98 + 0x0C0B is at 8,9,10.
- Walked: 6,10 through the door to 6,5 and back, at Z 0.

BUILD REVIEW bank: FAIL

1. Carpet corners: 0x0AC9 at 4,5,0 (NW) and 0x0ACA at 8,7,0 (SE) are swapped.
   - In my render of the cfg, each draws a detached tuft beyond the carpet's north and south points, and the frame
     shows a notch there. `render-bank-inside.jpg` shows the same.
   - Fix: put 0x0ACA at 4,5,0 and 0x0AC9 at 8,7,0. The other 13 pieces are right.
   - Also correct guide 2.5's carpet line (NW 0x0ACA, SE 0x0AC9). Round 1 caused this change.

Notes, not failures:

- The bench 0x0B2C at 9,6,0 is listed "along the east wall", but a floor tile (x10) separates it from that wall.
- The torch 0x0A0C at 5,3,13 hangs over the banker's spawn tile, which is harmless.

## lodge (origin 5740,1170)

What passes:

- Brick walls x2-12, y2-9 are whole. Windows: 0x003B in the N/S walls and 0x003C in the W/E walls, with no furniture
  or torch on a window's floor tile.
- The floor is at x3-12, y3-9.
- The shingle roof covers x3-13, y3-10 up to Z 35, with the ridge on x8 and the 0x0055 gables.
- The hearth is on the north wall, with its top (24) under the roof (29 at x6, 32 at x7).
- The north-wall bookcases 0x0A98 face south, and the torches hang on plain wall.
- The long table has 0x0B4F chairs on y5 and 0x0B50 chairs on y7, all facing it.
- The banners 0x1589 at 13,4,8 and 13,7,8 hang off the east wall's outside. I drew the art: the pole's bracket is at
  its west end, so it hangs on an east wall from outside.
- The sign is clear of the door.
- Walked: 7,11 through the door to 7,8 and back, at Z 0.

BUILD REVIEW lodge: FAIL

1. The bookcases 0x0A97 at 3,4,0, 3,6,0 and 3,7,0 stand edge-on to the west wall, like fins sticking out into the
   room.
   - 0x0A97 is a south-facing case, the same orientation as 0x0A98. The art, my cut-away, `render-lodge-inside.jpg`,
     `lodge-inside.jpg` and the lodge's west wall in `bank-front.jpg` all show it.
   - The guide (3) wants wall pieces "backed against the walls, facing in".
   - Fix: use an east-facing bookcase, 0x0A99 (or 0x0A9A / 0x0A9C), on those three tiles. I rendered these flat
     against a west wall run.
   - Also correct guide 2.5 and 3.
2. The carpet runner (0x0AC9 at 5,8,0, 0x0ACE at 6-8,8,0, 0x0ACC at 9,8,0) does not read as a rug.
   - It is the north fringe of a carpet with no body and no south edge: a thin fringed strip.
   - The 0x0AC9 corner draws as a detached tuft beside it (see the bank's fix).
   - Fix: lay it as a hallway runner, as guide 9.2.4 says ("a hallway uses only the fringed ends"): 0x0ACD at 5,8,0,
     0x0AC8 at 6,8,0 to 8,8,0, and 0x0ACF at 9,8,0. I rendered that, and it draws as a whole runner with fringed
     ends.

Could not judge: the runner, the book 0x0FEF at 7,6,6 and the y8 row in TazUO. They sit behind the south wall in the
inside shot.

## dock (origin 1550,612, a real lake)

Bridge:

- Planks 0x07C9/0x07CD run x4-22, rows 6-8, at Z 1, over impassable water.
- Rope rails 0x03A6 run along rows 6 and 8 at Z 6, with posts stacked -4/1/6 at the four ends. The walk row 7 is open.
- `walk-dock.log` reads bank Z 1 at x2-3, deck Z 2 from x4 to x22, bank Z 1 at x23-25, and the same coming back. Each
  join is one step, walked both ways (4.1).
- `dock-west-end.jpg` and `dock-east-end.jpg` show both ends meeting the bank at the shore.

Pier:

- Planks run x15-17, y15-20, at Z 5. Rails 0x03A9 run along columns 15 and 17 at Z 10, with a rope 0x03A6 across the
  free end at 16,15,10 and stacked posts at its four corners.
- `walk-pier.log` reads bank Z 6 at 16,21-23 and deck Z 6 from 16,20 to 16,16, both ways.
- Its head stands over open water (`dock-pier.jpg`).
- The coil of rope 0x14F8 at 15,17,11 draws as a coil sitting on the west rail, which is fine.

Signs and props:

- The signposts stand beside each approach.
- The barrel and crate are on the south bank, and the lamp post is beside the west end, all off the walked lines.

BUILD REVIEW dock: PASS

Could not judge:

- The black wedges along the lake's edge in `render-dock.jpg` are isorender gaps where the land slopes; TazUO draws a
  clean shore there, so I did not count them.
- The shore was there before this build (the branch's map), and I did not review it as part of this build.

## market (origin 5722,1195)

What passes:

- The paved square has three counter stalls at y4. Each has a crate and a barrel behind it and its goods on the
  counter.
- The stone fountain fills 7-10, 6-9, and the lamp posts stand at 2,2, 2,12 and 14,12. The stacked crates are at
  13,7, and the signpost at 0,13 is off the square.
- `walk-market.log` crosses the square along y10, from x0 to x15 and back, at Z 0 with no stall.

BUILD REVIEW market: PASS

Suggestions, not failures:

- The square's NE corner (14,2) has no lamp post, so only three corners are lit.
- The two hay piles (0x1036 at 13,2, 0x1037 at 14,3) read as faint litter at that corner in `market-square.jpg`.
  Either put them by the flour stall's barrel or give the corner its fourth lamp.
- The fish stall is the thinnest of the three. A second small-fish pile or a crate of fish would help.

## twostory (origin 5742,1195)

Ground storey:

- Plaster walls 0x0136/0x0137 (post 0x012A, L 0x0132) are whole on both storeys, x2-9, y2-8.
- The floors are at Z 0 (x3-9, y3-8) and Z 20, with the Z 20 floor left open over 8,4-8,7.
- The shingle roof covers x3-10, y3-9, Z 40-49, with 0x014A gables on the south row. It is 8 wide, so its two top
  slopes meet without a ridge piece, and the front shot shows a clean ridge.
- The table has 0x0B4F north and 0x0B50 south of it, both facing it. The torches hang on plain wall, and a keg and
  barrel stand in the corners.

Stair:

- 0x0739 steps at 8,7,0, 8,6,5, 8,5,10 and 8,4,15 climb north, 5 per step. The top step's top (20) meets the upper
  floor, and the floor is open above the stair.
- `walk-twostory.log` reads 2, 7, 12, 17, then 20 on 8,3, and back down, with no STUCK.

Upper storey:

- The hearth is on the north wall under the roof's high middle. The bed 3,3-3,4 has its head on the north wall, along
  the west wall. The bookcase 0x0A98 is on the north wall, and the torch on plain west wall.
- No furniture stands on a window's floor tile.
- The sign is at 6,9,5, and the walk went through the door both ways.

BUILD REVIEW twostory: PASS

Could not judge:

- Under-stair fill. Only 8,5 and 8,4 have 0x0738 blocks (0-10), so the step at 8,4,15 has an open 10-15 band under
  it and 8,6,5 has nothing under it. In my cut-away the step art draws its own riser, and I see no hole from the
  default camera. Guide 4.2 still says to fill under the steps; a block at 8,4,10 would close the band.
- The stairwell opening shows plainly only in my Z 20 cut-away. In the TazUO upper shot it cannot be told apart from
  the floor; the walk proves it.
- `twostory-outside` shows only the roof.

## Verdicts

BUILD REVIEW farmhouse: FAIL
1. SmallBedSouthAddon at 7,5,0 (0x0A63 7,5 / 0x0A5C 7,6) floats mid-room: its head is not against a wall (guide 3).
   Move window 0x00B9 from 8,3,0 to 8,5,0 (0x00A7 at 8,3,0), then put the bed at 8,3,0 (head on the north wall,
   along the east wall).

BUILD REVIEW bank: FAIL
1. Carpet corners are swapped: 0x0AC9 at 4,5,0 and 0x0ACA at 8,7,0 draw detached tufts and notch the frame. Put
   0x0ACA at 4,5,0 and 0x0AC9 at 8,7,0, and correct guide 2.5 to say NW 0x0ACA, SE 0x0AC9.

BUILD REVIEW lodge: FAIL
1. Bookcases 0x0A97 at 3,4,0, 3,6,0 and 3,7,0 face south and stand edge-on to the west wall. Use an east-facing case
   (0x0A99, or 0x0A9A / 0x0A9C) there, and correct guide 2.5 and 3.
2. The runner (0x0AC9 5,8,0; 0x0ACE 6-8,8,0; 0x0ACC 9,8,0) is a fringe strip with a detached corner tuft. Lay it as
   0x0ACD 5,8,0 + 0x0AC8 6-8,8,0 + 0x0ACF 9,8,0 (guide 9.2.4).

BUILD REVIEW dock: PASS
BUILD REVIEW market: PASS
BUILD REVIEW twostory: PASS
