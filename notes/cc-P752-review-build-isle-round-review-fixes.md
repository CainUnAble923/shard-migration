# cc-P752: build review of P751 (the seven fixes from P748's review: isle coast, farm, farmhouse, lodge)

Iron Golem, 2026-10-31. Reviewed `origin/golem/Iron/P751` in both copies without switching branches. I read the guide
(`notes/guides/building-and-decorating.md`) in full, the notes, `placed.md`, the code diff, and looked at every render
and the TazUO shots. Nothing rebuilt, no shard started, no lock taken. Nothing in P751's own files edited.

## In plain words

- **P751 passes its build review.** The farm fence closes cleanly at both corners. The farmhouse fireplace now stands
  against the back wall under the middle of the roof, so nothing pokes through the thatch. The farmhouse door folds
  along its wall, and nothing stands in front of a window. The League lodge has its name sign by the road, and the
  beach below the training yard runs straight.
- **Two small things to tidy, neither blocking:**
  - One lodge picture is out of date: it still shows the sign at the spot P751 gave up on.
  - The walk log was never committed because of a file-type rule. I saved a copy with this review.
- Nothing for you to do. P751 can merge.

BUILD REVIEW P751: PASS

## Checked, item by item

The P748 list (P751's README "What to check"):

1. **Review folder:** present: `placed.md` (516 lines, grouped by building, walls named for the farmhouse pieces),
   13 renders (before and after), 37 TazUO shots. The walk log is missing from the branch (observation A).
2. **Fence corners:** the NW post is 0x0838 at 6677,3967. The SE L 0x0835 is at 6695,3983, one piece. The pen's
   T-join 0x0835 is at 6695,3973. An L at a T is right there: its south and east arms carry the pen's row and the
   fence above, and the tile below carries its own N-S piece. `after-fence-corners.jpg`,
   `tazuo-farm-fence-nw.jpg` and `-se.jpg` show whole corners, no stubs, and one piece per tile.
3. **Farmhouse:**
   - The wall box is x 6699-6705, y 3972-3978. The light wood set's 0x00A9 post is at NW, 0x00A8 at NE, 0x00A7 at
     SW and 0x00A6 at SE: the east/south rule holds. The north row is all 0x00A8, and the west and east columns are
     0x00A7 with E-windows 0x00B9.
   - Thatch roof: west 0x05A6 rising 27/30/33 to ridge 0x05A5 at 36, then east 0x05A4. It covers x 6700-6706 and
     y 3973-3979 (one in from NW, one past SE), with gable 0x00C1 in the south row.
   - Hearth: StoneFireplaceSouth (0x0967 + 0x0961, matching pinned's addon). It is at 6702-6703,3973 on the north
     wall. Its top is Z 31, under roof Z 33 and 36. Roof-on render and `tazuo-farmhouse-roof.jpg`: nothing on the
     thatch.
   - Windows: the inside tiles of all four windows (6700,3974; 6700,3977; 6704,3974; 6704,3977) are clear.
   - Furniture:
     - The bed is SmallBedEast (0x0A5D + 0x0A62, pinned's offsets), head on the west wall.
     - The torch 0x0A07 hangs on the west wall's plain piece at floor + 13.
     - The chairs face the table by the art: 0x0B4F north, 0x0B50 south.
4. **Farmhouse door:** `DarkWoodDoor(WestCCW)` 0x06A9 at 6702,3978 in the south wall line. The inside shot shows the
   open leaf folded west along the wall. The rehang of an old WestCW door is code plus a fact.
5. **Lodge sign:** 0xA854 "The League lodge" at 6781,3989, north of the road beside the League lesson sign.
   - It is readable in `tazuo-lodge-front.jpg`, `tazuo-lodge-door.jpg` and the roof-on render.
   - P751 moved it off P748's spot (6784,3994) because the north eave hid it there from the south-east camera. The
     two `-hidden-` shots prove that. I agree: guide 2.5 and 6 want a sign that names the building and reads from the
     approach, and the hidden spot fails that.
6. **Walk:** 19 of 19 legs and 292 steps, walked by the client's own steps. I read the log on this desk.
   - The farmhouse doorstep goes +4 then +3, in and out. That is the cottage's stone stair from P720. It is above the
     guide's "at most 2 per step", but a real character walks it both ways (observation C).
   - The moongate platform's +4 is the stock addon, untouched by P751.
7. **The yard's south-west beach:** straight runs at x 6718 and y 4014 with surf pieces.
   - TazUO `tazuo-coast-yard-west`, `-south` and `-corner`: smooth surf, no saw-tooth.
   - The whole-isle before and after differ only there. The stepped inner corner east of the yard and the beach
     south of the farm road are unchanged from P746, and P751 says so.

Also looked at, unchanged since P748's review: the lodge's walls, bookcases (0x0A99 on the west wall, 0x0A98 on the
north), carpet edges, torches at Z 13 and banners. The bank front shot was also checked.

## Observations (not blocking; for whoever next touches the isle)

A. **Walk log not on the branch.** `notes/cc-P751-review/isle-walk.log` matches `.gitignore`'s `*.log`, so the
   README's "Walk log" points at a file the branch lacks. I put a copy in `notes/cc-P752-tools/p751-isle-walk.txt`
   (332 lines, identical). Next time, name walk logs `.txt`.

B. **One stale render.** `after-lodge-inside.jpg` (roof off) still draws a signpost at 6784,3994, beside the north
   door. The roof-on render, the shots and the code put it only at 6781,3989. The world is right; only that picture
   is out of date.

C. **Farmhouse doorstep.** The cottage's stair climbs 0 → 4 → 7. Section 4.1 says at most 2 per step. The client
   walks it both ways (log lines 108-133). If the guide's number is meant strictly, it should say how a house stair
   (5-high step pieces) counts.

P752 DONE
