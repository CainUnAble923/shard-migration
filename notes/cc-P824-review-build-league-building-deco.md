# cc-P824: build review of P803 (New Haven League building: the board and a decoration review)

## In plain words

- **P803 is sent back for a small fix-up, not merged yet.** Most of it is right: the League board now hangs on a wall
  and faces the room, the bookcases face the room, nothing stands in front of a window, and the banner sits on the
  outside wall.
- **What still reads wrong in the pictures:** on the testers' town the board now hangs over the stretched bear hide
  beside it, and the new League signpost faces away from the street. On main, the board covers one bookcase, and the
  sign by the door hangs over a stained-glass window.
- **Main's new sign and bookcases were never seen in the game client.** The test world used for main's shots kept its
  office furniture in the other house, so only the overhead renders show them.
- Nothing for you to do. The Iron Golem gets the numbered list below as a fix-up.

## What was reviewed

Branch `origin/golem/Iron/P803` in both copies (fetched, not checked out). Read in full: guide
`notes/guides/building-and-decorating.md`, `notes/cc-P803-review/placed.md`, `notes/cc-P803-league-building-deco.md`,
and the code diff (`design/registrar-office/layout.json`, the generated layout, seeder and `Appraiser.cs` board move).
Looked at every render (release and main, before and after, outside and cutaway), `board-facings.png`,
`piece-facings*.png`, and the TazUO shots in `shots-release-before/after(-run1)` and `shots-main-before/after(-run1)`,
zooming crops of the board, signs and bookcases (crops in the P824 scratchpad, not kept).

P803 placed no walls, doors, stairs, roofs, shores, bridges, docks or foliage: both buildings are map buildings and
every change is a seeded server item. So the checks that apply are wall-mounted items, signs, facings, window tiles,
crowding, and the proof.

### Passes

- **Release board** 0x1E5E at 3458,2598,18: east-facing art on the floor tile in front of the dividing wall x3457, faces
  the room, off the door's tile and swing (guide 3, 2.4). One board in the office after the duplicate fix.
- **Release bookcases**: 0x0A98 at 3461,2597 faces south on the north wall; 0x0A9A at 3454,2599 faces east on the
  plain west wall (guide 3). Both read right in the cutaway and the inside shots.
- **Release window tiles**: the flowerpot is gone and the chest, bookcase and candelabra moved off the four window floor
  tiles; all eight window tiles are clear in the cutaway (11.4, 11.13).
- **Release banner** 0x1589 at 3463,2599,26 (floor + 8): flat on the east wall from outside, between the two east
  windows, as the P720 lodge (guide 3). Reads right in the outside shots.
- **Main bookcases**: 0x0A98, 0x0A97, 0x0A98 face south on the north wall (guide 3, P734 review: 0x0A97 is a
  north-wall case).
- **Main sign arm** is now 0x0B98 (sticks out from a south wall), two tiles east of the arch (2.5).
- **Main board** art 0x1E5F (north-wall face) on 3662,2548, in front of the north wall, off the wall's own tile.
- The old release sign (arm 0x0B97 hanging from no wall, under the eave) is gone, as guide 11.12 wants.

BUILD REVIEW P803: FAIL

1. **Release board 0x1E5E, 3458,2598,18, hangs over the stretched hide 0x106B at 3458,2597.** In
   `render-release-after-cutaway.jpg` and `shots-release-after/after-inside-office.jpg` the board's frame is drawn
   across the hide's frame, so two wall pieces overlap and the hide is half hidden (before, the hide stood alone). The
   guide wants each wall-mounted item on its own stretch of wall, reading clearly from the room (3; 9.4 "enough, not
   everything"). Fix: give the board a free tile of the dividing wall (for example 3458,2599 if it is clear of the
   walk line from the door, or a tile south of the desk), or the hide's tile if the hide is moved; render both and
   check neither overlaps.
2. **Release signpost 0xA854 "League of Extraordinary Citizens", 3463,2596,16, stands south of the road with its face
   to the south, its back to the street.** The road (y 2592-2595) is north of it, so a player walking the street sees
   the back of the board (zoom of `after-outside-door-side.jpg`: the face points south-east at the ankh garden). The
   guide wants every sign **north of its path, facing it**, and a building south of the road gets its sign **across
   the road on the north side** (6; Chase 10-30 "all signs should be north of path"). Fix: 0xA854 on the north verge
   of the road opposite the door (about x 3460-3462, y 2591), off the door's approach line x 3459; if that verge is the
   cliff, put it on the nearest flat tile north of the road and prove it in a door-side shot that shows the board's
   face from the road.
3. **Main sign arm 0x0B98 and board 0x0BCF, 3670,2563,0, hang on the stained-glass window at 3670,2562.** In
   `render-main-after-outside.jpg` the board is drawn over the window glass. The guide says nothing hangs on a window
   tile (11.4) and the hanger needs a plain wall to its north (11.12). Fix: move arm and board to 3671,2563 or
   3672,2563 (plain south-wall pieces; the windows are 3661, 3662, 3664, 3665, 3670 and 3673), still at least two tiles
   east of the arch (2.5).
4. **Main board 0x1E5F, 3662,2548,0, covers the bookcase 0x0A97 at 3661,2548.** In `render-main-after-cutaway.jpg`
   only the bookcase's red base shows below the board; before P803 both bookcases at 3660 and 3661 read whole. Fix:
   leave a free tile between the board and the bookcases (move the board east to a clear plain north-wall tile, or
   drop the 3661 bookcase), then check the cutaway shows every piece whole.
5. **Main's changed decor has no TazUO shot.** The main after run's world kept the office decor in the other house
   (the notes say the upgrade rightly left it alone), so `shots-main-after/after-outside-door-side.jpg` shows no
   League sign and no potted tree by the arch, and the inside shots show the board but not the bookcases. Guide 8
   wants the outside door-side shot and each room from the default camera. Fix: after items 3 and 4, seed main's
   office on the private shard (`[ClusterFSeedRegistrarOffice` on a world without the old decor) and reshoot the door
   side and the north wall.

Not fix items, for the record: the release door-side shot is half covered by the journal (worth closing the journal
before the shot), and main's bookcase at 3670,2548 touches the map's wall fish trophy; both were there before P803.

P824 DONE
