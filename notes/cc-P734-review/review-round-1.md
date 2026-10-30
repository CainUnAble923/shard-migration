# P734 practice builds: build review, round 1

Reviewer: a second Claude, read-only. Checked against `notes/guides/building-and-decorating.md` (sections 1-10; the
contents list a section 11 that is not in the file). Evidence used: the six `placed-*.md` lists, the build cfgs, every
render and every TazUO shot in `notes/cc-P734-review/`, the seven walk logs (converted to relative coordinates by
subtracting each origin), tiledata read from `D:\UO\UltimaOnlineVanilla\tiledata.mul`, the stock art of the pieces in
question drawn with `scripts/mapbuild/isorender.py`'s `Art` class, and ModernUO's addon component tables.

## Findings that apply to more than one build

- **South-west corner piece is wrong in every building and in the garden fence.** The guide's table (2.2) puts the
  "east" piece (north-south run) at the south-west corner. Every build puts the "south" piece there. In every render and
  front shot the SW corner shows a wall stub sticking out one tile west past the west wall, poking up above the eaves
  (farmhouse, bank, lodge and two-story renders; bank-front and lodge-front shots), and the fence shows the same stub.
- **Chairs face the wrong way.** Drawn from the client art: 0x0B4E has its back on the west edge (it faces east),
  0x0B4F has its back on the north edge (faces south), 0x0B50 has its back on the south edge (faces north). So the
  "north of the table" chairs (0x0B4E) face east, and the "south of the table" chairs (0x0B4F) face south, away from the
  table. The farmhouse inside shot agrees: the chair south of the table has its back toward the table. North of a
  table use 0x0B4F; south of it use 0x0B50. (The guide's 3 and 2.5 lists 0x0B4E/0x0B4F and flags their facing as
  unverified. This review checks them, and they are wrong.)
- **The house signs hang on the door.** The sign is on the tile one east and one south of the door (x+1, y+1). In the
  farmhouse, bank, lodge and two-story front shots and renders, the sign board is drawn over the right half of the door
  leaf. Move each sign one more tile east (x+2, y+1) so it hangs on plain wall beside the door, then check the shot.
- **Wall decoration and furniture over windows.** Several torches, bookcases and fireplaces stand on the floor tile in
  front of a window piece (listed under each build).
- Gate, doors, bridge and stair: walks done both ways with no STUCK lines, and Z within 2 at every join except the
  stair top (17 to 20, the normal stair step, which the client accepted).

## farmhouse (origin 5700,1170)

Walls, windows, floor, roof courses (Z 20/23/26/29, x3-9, y3-8, gables 0x00C1 in the south row) and door are laid by
the rules. The door at 5,7 (WestCCW) is in the wall line. The walk went in and out through it at Z 0 both ways
(5,9 to 5,5 and back). The gate at 10,5 was walked both ways (9,5 to 12,5 and back). The bed (0x0A63 head at 7,3,
against the north wall) and the plate on the table are right. The fireplace faces east into the room.

BUILD REVIEW farmhouse: FAIL

1. 0x00A8 wall, 2,7,0 (SW corner): this is the "south" piece. It sticks out one tile west of the west wall, and the
   stub shows above the thatch at the SW corner in the render and the front shot. The guide (2.2) wants the "east"
   piece 0x00A7 at the SW corner.
2. StoneFireplaceEastAddon, 3,3,0 (0x0959 at 3,3, 0x0953 at 3,4): the fireplace is 24 high, but the thatch at x3 is
   at Z 20. Its top pokes through the roof as a grey stone lump at the NW corner (render, and the TazUO front shot).
   This is "a chimney standing apart" on the roof (2.3; P663's "small gray structure"). Either lower the piece or roof
   over it whole (for example, carry it up as a full chimney through the thatch), so nothing stray shows on the roof.
3. 0x00B9 window, 2,4,0: hidden behind the fireplace's 0x0953 at 3,4. The inside shot shows no west window. Move the
   window to 2,5,0 and put 0x00A7 at 2,4,0.
4. 0x0A0C wall torch, 6,3,13: it hangs on the window 0x00BA at 6,2. The inside shot shows the torch over the window
   frame. Move it to 5,3,13, in front of plain wall 0x00A8 at 5,2.
5. 0x0B4E chair, 5,3,0 faces east, and 0x0B4F chair, 5,5,0 faces south, away from the table. Use 0x0B4F at 5,3,0 and
   0x0B50 at 5,5,0 (3: chairs face the table).
6. 0x0B98 + 0x0BD2 sign, 6,8,5: the board is drawn over the door leaf (front and inside shots). Move it to 7,8,5.
7. 0x0835 "fence post", 10,3,0 (fence NW corner): 0x0835's art is an L corner (arms on the tile's south and east
   edges), not a post. At the NW corner it makes the two runs cross in an X, a stub poking north and one poking west.
   It is plain in the front shot. Remove it: the north run (south edges of y3) and the west run (east edges of x10)
   already meet at that point. Or use a true post piece, if one exists, after checking its art. The guide's fence row
   in the 2.2 table is wrong about 0x0835 and should be corrected.
8. 0x0836 fence, 10,8,0 (fence SW corner): this is the east-west piece, so the south run sticks out a tile west of the
   west run (visible in the front shot). Use 0x0837 there (the east/south rule, 2.2 and 5 "one fence, one rule").
9. 0x0E77 "water barrel", 9,7,0: 0x0E77 is a plain barrel in tiledata. If a water barrel is meant, What to use where
   (Farm) names 0x154D.

Could not judge: the `farmhouse-outside` shot is covered by TazUO's "Version History" window, so it shows nothing.
The barrel and flour at 3,6 and 4,6 are hidden behind the south wall in every view. The cabbage IDs 0x0C7B/0x0C7C are
both "head of cabbage" in tiledata, which is fine.

## bank (origin 5720,1170)

Walls, windows (0x005E in E-W walls, 0x005D in N-S walls), floor x3-10 y3-8, the shingle roof (x3-11, y3-9, Z 20-32,
ridge 0x05C2 on x7) and the gable 0x0069 rows are laid by the rules. The door at 6,8 (WestCCW) was walked both ways
at Z 0 (6,10 to 6,5 and back). The torches 0x0A0C at 5,3 and 7,3 hang on plain north wall, and 0x0A07 at 3,6 on
plain west wall. The counter row is at y4 with the vault chests behind it and a gap at 9,4.

BUILD REVIEW bank: FAIL

1. 0x0058 wall, 2,8,0 (SW corner): this is the stone shop set's east-west piece. A white stub sticks up at the SW
   corner past the eaves in the render, the bank-front shot and the bank-outside shot. Use the north-south piece
   0x0057 (2.2; this set reverses the pair).
2. No banker. The guide's accepted bank (2.5) has "the banker behind" the counter, and a bank without one does not
   read as a bank inside. Place a Banker behind the counter on a free tile (3,3, 5,3, 7,3 or 9,3), facing south.
3. Carpet edges are the wrong pieces. From the client art: 0x0ACE is the north edge (fringe to the north), 0x0AD0 the
   south edge, 0x0ACD the west edge and 0x0ACF the east edge. The build uses 0x0AD0 on the west and east edges (4,6,0
   and 8,6,0), which are strips running the wrong way, and 0x0ACE on the south row (5,7,0, 6,7,0, 7,7,0). The inside
   render shows border lines running through the carpet instead of a frame. Use 0x0ACD at 4,6,0, 0x0ACF at 8,6,0 and
   0x0AD0 at 5-7,7,0. Also check the corners against the art: 0x0AC9 draws at the tile's top (north-west) point and
   0x0ACA at its bottom (south-east) point, the reverse of what is placed (0x0ACA at 4,5 NW, 0x0AC9 at 8,7 SE).
4. 0x0B97 + 0x0C0B sign, 7,9,10: the round bank board is drawn over the door's right edge (bank-front shot). Move it
   to 8,9,10. Also, the 0x0B97 arm's art runs along x, so it lies flat along this south wall in the shot. The 0x0B98
   arm sticks out from a south wall (as on the other three houses). Check which of the two the shot wants.

Could not judge: whether 0x0B40 shows its serving front or its back toward the carpet. In the render the counter
reads as a long table on legs, with the legs on the carpet side. Compare with an OSI bank before keeping it. The
bench 0x0B2C at 9,6 cannot be seen in any view.

## lodge (origin 5740,1170)

Brick walls (0x0036 post, 0x0034/0x0035 runs, 0x0033 SE corner), windows 0x003B/0x003C on the right walls, floor
x3-12 y3-9, the shingle roof (x3-13, y3-10, Z 20-35, gable 0x0055) and the door at 7,9 are by the rules. The door was
walked both ways at Z 0 (7,11 to 7,8 and back). The fireplace faces south. Bookcases 0x0A98 on the north wall and
0x0A97 on the west wall face into the room. The banners 0x1589 hang on the outside of the east wall at Z 8.

BUILD REVIEW lodge: FAIL

1. 0x0034 wall, 2,9,0 (SW corner): this is the "south" piece, and the stub shows at the SW corner in the render and
   the lodge-front shot. Use 0x0035 (2.2).
2. 0x0A0C wall torch, 6,3,13: StoneFireplaceSouthAddon at 7,3 puts 0x0967 on 6,3, so the torch is inside the chimney
   (inside render and shot: the flame is half hidden in the stone). Move it to 8,3,13 (plain wall 0x0034 at 8,2).
3. 0x0A07 wall torch, 3,5,13: it hangs on the window 0x003C at 2,5, and the inside shot shows the torch on the window's
   edge. Move it to 3,3,13 (plain wall 0x0035 at 2,3).
4. Bookcases (12 high) in front of windows: 0x0A98 at 5,3,0 covers window 0x003B at 5,2, 0x0A98 at 9,3,0 covers window
   0x003B at 9,2, and 0x0A97 at 3,7,0 covers window 0x003C at 2,7 (inside render and shot: the window tops show above
   the cases). Move the windows to free wall (for example 3,2 and 11,2 on the north wall and 2,8 on the west wall,
   with plain 0x0034/0x0035 back where they were), or move the cases off the window tiles.
5. Chairs: 0x0B4E at 6,5, 7,5, 8,5 and 9,5 face east, and 0x0B4F at 6,7, 7,7, 8,7 and 9,7 face south, away from the
   table. Use 0x0B4F on the y5 row and 0x0B50 on the y7 row.
6. 0x0B98 + 0x0BD2 sign, 8,10,5: drawn over the door leaf (render, lodge-front shot). Move it to 9,10,5.

Could not judge: the carpet runner (5-9,8). It is not visible in the inside render or the inside shot (that row is
behind the cut-away south wall), so its look and edge pieces are unproven: show it. The book 0x0FEF at 7,6,6 cannot be
seen on the table in either view. The guide's accepted lodge also had a scroll and a notice board on the north wall;
neither is here, which is a suggestion, not a fault. The two `outside` shots (lodge, bank, farmhouse, two-story) are
taken from the north-west corner and show only the roof from the back; they prove nothing about the back walls.

## dock (origin 5700,1195)

Bridge heights pass. Walking east from 1,6: land Z 0 at 2,6, deck Z 2 from 3,6 to 16,6, land Z 0 at 17,6. Walking
west, the same in reverse. Both ends are within 2 and were walked both ways (4.1). Everything else about the pond and
the pier fails.

BUILD REVIEW dock: FAIL

1. The pond does not block. Water 0x1797-0x179A has height 0 in tiledata, and placed as statics at Z 0 on Z 0 grass
   it blocks nothing. The walk went from the bridge at 16,7,2 onto the pond tiles 16,8,0 (0x1797) and 16,9,0 (0x1798)
   and out to the bank. A player can walk across the water. Make it real water: water land under it, or the land
   lowered so the water is not standing ground. What to use where (Beach and coast) names `code\lake-fishing`, an
   inland lake of 0x1797 with shore pieces, as the piece for this.
2. The pond is a square of whole water tiles with hard edges on grass, no shore pieces. That is the look guide 5
   forbids ("real shore transitions, no sawtooth"). Edge it with the surf and shore pieces by which side the land is on
   (5; lake-fishing uses 0x179E-0x17AC).
3. 0x03A6 rope, 11,8,1 and 12,8,1: the south rail runs straight across the pier's mouth on top of the pier planks
   0x07CD at 11,8 and 12,8. The rope is impassable and 5 high, so it closes the pier off. The walk heading south from
   the bridge at 11,7 stuck there ("south step 2" repeats 5711,1202,2), slid east along the bridge, and left over the
   pond at 16,8. Leave a gap in the rail where the pier joins.
4. The pier (0x07CD at 11-12, 8-10, Z 1) was never walked. Neither end of it is proven (4.1, checklist 3). After
   fix 3, walk it from the bridge to its end and back, and take a shot from its far end.
5. 0x03A6 rope, 4-15,8,1 (south rail): it sits on the tile south of the deck, so in the render and the dock shots it
   floats on the water a tile away from the bridge's south edge. The north rail at y5 meets the deck edge. All rails
   are at deck Z (1). The guide (4.3) wants rope rails at deck + 5 and corner posts stacked 0x03AE (deck - 5), 0x03A5
   (deck), 0x03AB (deck + 5). Here the posts 0x03AB at 3,5, 16,5 and 13,8 are single pieces at deck Z, and the south
   rail has no end posts. Rebuild the rails to 4.3 on the deck's own edge. If a rail on row 7 would narrow the walk,
   widen the deck to three rows.
6. The pier runs from the bridge to the pond's south edge (y10 is the last water row; land at y11), so it is a second
   bridge, not a dock with its head over water. It has a rail on the east side only. Give it a free end over water and
   rails on both sides, or call and build it as a footbridge.
7. 0x0D08 lily pad, 13,8,0 shares its tile with the pier-head post 0x03AB at 13,8,1. Move the lily pad clear of the
   post (for example 14,9,0).

Could not judge: whether the lamp post 0x0B20 at 2,8 stands where the list says (in the render it reads as level with
the bridge's west end).

## market (origin 5722,1195)

The paved square (2-14, 2-11), the three stalls (counters at y4 with stock behind at y3) and the four lamp posts at
the corners are laid as listed and read as a market. The walk crossed the square both ways at Z 0.

BUILD REVIEW market: FAIL

1. 0xA854 signpost, 1,7,0: it stands in the middle of the square's west side, in the walked line. On the way back the
   walker stuck at 2,7 ("west step 14" repeats 5724,1202) and had to sidestep north to 2,6 to leave. The guide (6)
   wants the signpost beside the way, never on it. Move it off the entry line, for example to 1,4,0 or 0,2,0.
2. WaterTroughEastAddon (0x0B41 at 8,8, 0x0B42 at 8,9): a small animal trough as the square's centrepiece. It also
   blocked the walker's line at 8,9 (the walk detoured north at step 8). What to use where (Market) names a square
   fountain (`StoneFountainAddon` 0x1731-0x173E, or one of the two unused `lagatha-brass-fountains`) or a wishing well
   0xA300/0xA301. Use one of those and keep a clear walk round it.
3. Stall stock reads as nearly empty: one apple 0x09D0 per counter tile (3,4,6 and 4,4,6) and one pear 0x0994
   (5,4,6) show as single red or green specks in the render and shot. A hay sheave 0x100C (13,4,6, impassable, 3 high)
   stands on a counter. Use fuller produce piles, and hay 0x1036/0x1037 (What to use where: Market and Farm), so each
   stall's trade reads from the default camera.

Could not judge: whether 0x0B40 shows its serving front to the square (same doubt as the bank). The paver pattern
(0x0519-0x051E in a strict two-tile cycle per column) shows faint diagonal striping in the render, which is a
suggestion: mix the variants unevenly (9.1 floors).

## twostory (origin 5742,1195)

The ground walls, the door at 4,8, the upper storey at Z 20 on the lower walls, the floors at Z 0 and Z 20, and the
roof (x3-10, y3-9, Z 40-49, gable 0x014A) are by the rules. The stair passes on everything the walk can prove.
0x0739 steps at 8,7,0, 8,6,5, 8,5,10 and 8,4,15 climb north, 5 per step. The walk read Z 2, 7, 12 and 17 on the
steps, then 20 on the upper floor at 8,3, and the same back down, with no STUCK. Walking up under Z 20 proves the
floor is open over 8,4-8,7. The bed 0x0A63 head is at 3,3 against the north wall.

BUILD REVIEW twostory: FAIL

1. 0x0136 wall, 2,8,0 and 0x0136 wall, 2,8,20 (SW corner, both storeys): these are "south" pieces, and the stub shows
   at the SW corner in the render. Use the north-south piece 0x0137 (2.2).
2. StoneFireplaceEastAddon, 3,4,0 (0x0959 at 3,4, 0x0953 at 3,5): it is 24 high under an upper floor at Z 20, so its
   top pokes 4 above the upper floor at 3,4 and 3,5 (grey stone on the upper floor in the upper-floor render). The
   upstairs SmallBedSouthAddon at 3,3,20 puts its foot 0x0A5C on 3,4,20, the same tile as the fireplace top. Use a
   hearth no taller than 20 downstairs, or carry it up as a whole chimney through the upper floor and roof. Keep the bed
   off those tiles.
3. 0x013B window, 2,5,0: hidden behind the fireplace's 0x0953 at 3,5. The ground-floor render shows no west window.
   Move it to 2,6,0 or 2,7,0 and put 0x0137 at 2,5,0.
4. Chairs: 0x0B4E at 5,4,0 faces east, and 0x0B4F at 5,6,0 faces south, away from the table. Use 0x0B4F at 5,4,0 and
   0x0B50 at 5,6,0.
5. 0x0B98 + 0x0BD2 sign, 5,9,5: drawn over the door leaf (render, twostory-front shot). Move it to 6,9,5.

Could not judge: the stair's side fill. 0x0738 blocks (10 high) sit at 8,5,0 and 8,4,0 only, so the step at 8,4,15 has
an open 10-15 gap under it, and 8,6,5 has nothing under it. I could not see a gap in the stair-foot shot, so I am not
failing it. Guide 4.2 says to fill under with blocks where the side shows. The walls are 0x0136/0x0137, not the
guide's plaster pieces 0x0133/0x0134 (with post 0x012A and corner 0x0132). Tiledata names all of them "plaster wall",
and the render shows consistent trim, but I could not confirm from `walls.txt` that they are one set. The upper-floor
shot does not clearly show the stairwell opening; the walk proves it. The `twostory-outside` shot shows only the roof.

## Verdicts

BUILD REVIEW farmhouse: FAIL
BUILD REVIEW bank: FAIL
BUILD REVIEW lodge: FAIL
BUILD REVIEW dock: FAIL
BUILD REVIEW market: FAIL
BUILD REVIEW twostory: FAIL
