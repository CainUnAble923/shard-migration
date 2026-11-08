# cc-P836: build review of P827 (the League field office in New Haven, fix-up of P803)

## In plain words

- **The League notice board still stands sideways, in both towns.** It now hangs in an empty spot in both towns. But
  the board picture used for each wall is the wrong one. In the testers' version it sticks straight out of the office
  wall, beside the desk. On main it sticks straight out of the hall's back wall, beside the bookcases. The two board
  pictures need swapping.
- **Everything else P827 fixed looks right.** The testers' signpost now stands north of the road, facing the street.
  On main the hanging sign is on plain wall, clear of the stained glass. The hide, bookcases and desk items are no
  longer covered.
- **For you:** nothing. The fix goes back to the Iron Golem as a fix-up (one change in each town, plus a check).

Iron Golem, fresh session, 2026-11-08, on `golem/Iron/P836`. Looked at `origin/golem/Iron/P827` in both copies
without changing branch. I read the building guide in full, and P827's `placed.md`, notes and code diff
(`layout.json`, `Appraiser.cs` `OfficeBoard`/`OfficeBoardItemID`, the seeder and the facts). I looked at all 4 isorenders, the 2
comparison renders and the 16 TazUO shots (`shots-*-after/`, main and release).

BUILD REVIEW P827: FAIL

1. **League requisitions board 0x1E5E, release, 3458,2602,18, on the office's west (dividing) wall x3457. The art
   faces the wrong way: it stands edge-on, sticking out of the wall into the room.**
   - **What the renders show.** In the TazUO shot `shots-release-after/after-board-from-the-room.jpg` and the
     isorender `release-board-desk-before-after.png` (right half), the board's frame runs east-west. It lines up with
     the north-wall bookcase 0x0A98 at 3461,2597 (a south-facing piece), not with the wall x3457 behind it.
   - **So it does not hang on its wall.** It draws on the north edge of its tile, as a partition between the desk's
     south end (3458,2601) and the board's tile, at right angles to the dividing wall. That is also why P827 saw the
     board's art "reach over the desk's south end".
   - **What the guide wants (section 3).** A wall-mounted item faces the walk side. On a west wall that is the
     "east" facing, whose plane runs north-south along the wall.
   - **The fix.** Use the other board art, **0x1E5F**, at 3458,2602,18. Render it against the wall before you rely on
     it (11.2). If 0x1E5F draws flat on x3457, keep it there. The desk and hide then stay clear: the board draws on its
     tile's west edge.
2. **League requisitions board 0x1E5F, main, 3663,2548,0, on the hall's north wall y2547. The art faces the wrong way:
   it stands edge-on, sticking out from the north wall.**
   - **What the renders show.** In the TazUO shot `shots-main-after/after-inside-hall-north-wall.jpg` and the
     isorender `render-main-after-cutaway.jpg`, the frame runs north-south. It is at right angles to the bookcases
     0x0A98/0x0A97 beside it at 3660 and 3661, which lie flat along the wall.
   - **What it looks like.** A partition between 3662 and 3663, not a notice on the wall.
   - **The fix.** Use **0x1E5E**, the south-facing art that hangs on a north wall (guide section 3), at 3663,2548,0.
     Change `Requisitions/Appraiser.cs` `OfficeBoardItemID` in each copy. The load-time retag
     (`board.ItemID != OfficeBoardItemID`) then turns boards already placed on existing worlds.
   - **Also update** `LeagueOfficeDecorVerification.cs` (`BoardArt == 0x1E5E ? post.X == room.WestX + 1 : ...`) and
     the release diff `notes/cc-P827-tools/p827-release-isle-20261028.diff`.
   - **Prove it** with a fact that the board's art matches its wall, and a new TazUO shot of each board.
3. **Where the swap came from (to stop it coming back).** P803 chose the art from `board-facings.png`
   (`notes/cc-P803-tools/boards.json`), and the guide's Bank table calls 0x1E5E "east face". Both in-place renderers
   (isorender and TazUO, in both towns) draw 0x1E5E as the east-west (south-facing) board and 0x1E5F as the
   north-south (east-facing) one.
   - **The fixer:** render both IDs side by side against one west wall and one north wall, as guide 11.2 says ("when
     two readings disagree, render both and keep the one that draws whole"). Then correct the Bank and Guild hall
     rows in `notes/guides/building-and-decorating.md` section 10 to whatever that render shows.

## What passed

- **Release signpost 0xA854 at 3460,2591,20.** It stands north of the road on flat verge, reading from the south
  toward the street (guide 6), off the door's line. The walk log climbs at most 2 per step. `after-outside-door-side.jpg`
  and `after-outside-sign-from-the-street.jpg` show it. The front door in the north wall is hidden under the thatch
  eave in the door-side shot. That is the map's house and P803's known case (guide 11.12), not new in P827.
- **Main sign arm 0x0B98 + board 0x0BCF at 3671,2563,0.** It is the arm that sticks out (not 0x0B97), hangs from the
  plain south-wall piece 0x0034 at 3671,2562, and is clear of the stained glass at 3670 and 3673. It is three tiles east
  of the arch (`main-sign-3671-vs-3672.png`, `after-outside-door-side.jpg`).
- **Covered pieces from P824.** The release hide 0x106B on 3458,2597 stands alone. The main bookcase 0x0A97 on 3661 is
  whole. The inkwell 0x2D61 and scroll 0x2270 moved to the desk's north end, on the surface at Z 24. The main flowerpot
  0x11CA moved to 3673,2548 beside the chest, on no window tile.
- **Bookcases.** Main 0x0A98/0x0A97 lie flat on the north wall facing south. Release 0x0A98 at 3461,2597 is on the
  north wall, and 0x0A9A at 3454,2599 is on the quarters' west wall (the east-facing set from guide 3).
- **Window floor tiles.** No piece of ours stands on one, in either town. I checked against placed.md's list and the
  cutaways.
- **Walls, doors, roofs, stairs.** The walls, doors and roofs are the map's own buildings. P827 placed no walls, doors,
  stairs, roof pieces, shore, bridge, dock or foliage, and changed no map statics. Nothing stray is on either roof.
  The grey stone wall piece floating at the edge of both outside isorenders is a neighbouring map building cut by the
  render box.
- **Not ours.** The release TazUO shots show a bear rug on the office floor. It is not in the isorender or in
  placed.md, so it is a world item on the proof world copy, not part of this build. Worth a glance on the next run.

P836 DONE
