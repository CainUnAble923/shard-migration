# cc-P828: build review of P820 (the New Haven jail fix-up)

## In plain words

- **The four things the last review asked for are fixed.** The wall stub at the jail's front corner is gone, no
  torch hangs on a window, the orange patches on the roof are gone, and the marked crate now stands in plain view in
  the hall. Both versions (main and the isle release) match.
- **One new problem: the cell bars face the wrong way.** The iron bars across the three cell fronts are the
  north-south fence piece. From the camera they show as short stubs pointing into the hall, not a line of bars, so
  each cell front looks half open. Where each cell's side wall meets the bars there is also a one-tile gap.
  Prisoners cannot actually walk out (every one of those tiles blocks), but it looks wrong.
- **For you:** nothing. The jail goes back to the Iron Golem with the list below. It does not merge until a later
  review passes.

## What I checked

I read the guide in full. I fetched `origin/golem/Iron/P820` in both copies without changing branch and unpacked
`notes/cc-P820-review` (placed.md, four isorenders, two contact sheets, the corner before/after, and the main and
isle shot sets). I also read `notes/cc-P820-fixup-jail.md`, P815's review, and the code diff (`TutorialJail.cs` and the
generated `TutorialJailLayout.cs`). To check facing I rendered the bar, gate, bench, shackle, table and corner pieces
alone with `notes/cc-P724-tools/render_addons.py ids:...`, as guide 11.2 says to.

Layout coordinates below are (x, y) from the north-west post: main post 3702,2634 (floor Z 21), release post
3469,2597 (floor Z 11).

| Check | Result |
|---|---|
| Outer walls and corners (2.2) | Pass. Post 0x0036 NW, L 0x0033 SE, 0x0034 on the north row through the NE tile (10,0), 0x0035 down the west column through the SW tile (0,8). The south row starts at x 1, so P815's SW stub is gone (render and `sw-corner-before-after-main.jpg`). |
| Windows (2.2, 11.4, 11.13) | Pass. 0x003B in the south wall, 0x003C in the west and east walls. No furniture on any window's floor tile now that the two torches are gone. |
| Floor (2.2) | Pass. 0x0519 on x 1-10, y 1-8: inside the box and under the south row and east column only. |
| Roof (2.3) | Pass. Covers x 1-11, y 1-9. Eaves at floor + 19, rising 3 per course, ridge 0x05C2 on the middle column. Grey brick gable 0x0055 fills the south wall's row from floor + 20. Nothing on the roof in `1-outside-door-and-sign.jpg`, `1b-at-the-door.jpg` or `8-outside-after.jpg` (main and isle). |
| Door (2.4) | Pass. MetalDoor WestCCW at (5,8), in the south wall line, opens into the hall. Approach clear. |
| Sign (2.5, 6, 11.5, 11.12) | Pass. Hanger 0x0B98 + board 0x0BD2 "The New Haven Jail" outside the south wall, two tiles east of the door, Z floor - 2. Readable in the street shots. |
| Wall-mounted items (3) | Pass. No torches left. Candelabra 0x0B26 stands free at (2,4), 15 high, under the eave. Shackles 0x1262 hang on the north wall in two cells (seen in the hall shots). |
| Furniture facing (3) | Pass. Benches 0x0B2C run east-west along the bar row (rendered alone). Writing table 0x0B4A with the ledger and scroll at Z + 6. The crate is now at (7,4), in view. |
| Interior cell walls and bars | **Fail**: items 1 and 2 below. |
| Stairs, bridges, docks, shores, foliage | None placed. |
| What to use where (10) | Pass. Stock grey brick, shingles and pavers. Iron fence and gate are the right family for cell bars; only the facing is wrong. |

## Verdict

BUILD REVIEW P820: FAIL

1. **Cell bars 0x0821 placed in an east-west row face north-south.** The pieces are at layout (1,3), (4,3), (6,3)
   and (8,3): main 3703,2637,21 / 3706,2637,21 / 3708,2637,21 / 3710,2637,21, and release 3470,2600,11 /
   3473,2600,11 / 3475,2600,11 / 3477,2600,11. I rendered the art alone. 0x0821 runs north-south, like the "east"
   wall piece 0x0035. 0x0823 runs east-west, like the "south" piece 0x0034. The gate 0x0828 runs east-west, so the
   gates are right. In `shots-main/2-hall-window-open.jpg` and `shots-isle/2-hall-window-open.jpg`, each bar tile draws
   as a stub pointing into the hall, so the cell fronts read as open. Guide 3 says to face every piece to its wall
   line, and 11.2 says to read each facing from the art. Fix: in `notes/cc-P801-tools/gen_jail.py`, use the
   east-west iron fence **0x0823** on those four tiles. Render 0x0823 against a 0x0828 gate first and keep the one
   that draws a closed line. Regenerate `TutorialJailLayout.cs`. Add 0x0821 on those tiles to
   `TutorialJail.Retired` so a world already seeded with P801/P820's jail swaps them on load. Add a fact that no
   0x0821 stands in the bar row.
2. **One-tile gap where each cell side wall meets the bar row.** The partitions end in a plain "east" piece 0x0035 at
   layout (3,3) and (7,3): main 3705,2637,21 and 3709,2637,21, release 3472,2600,11 and 3476,2600,11. That piece
   closes only the tile's east edge. Its south edge, which is the bar line between the gate at (2,3) and the next
   cell, stays open. This is visible in the hall shots as floor between the west cell's gate and the middle
   partition, and between the middle cell's bars and the east partition. The tile itself blocks, so it is a look
   problem, not an escape. Guide 2.2 closes the south-east end of an east-piece run with the L corner. Fix: put the
   grey brick L corner **0x0033** on (3,3) and (7,3) in place of 0x0035, the same pattern as the outer SE corner.
   Retire the old 0x0035 on those two tiles on load (only that ID on those tiles). Show the closed fronts in a new
   hall shot on both builds. If the L reads badly against bars, stack an 0x0823 bar on the same tile instead, and
   show that.

Advice, not a fix: the candelabra at (2,4) stands right in front of the west cell's gate (2,3). It works, because
the gate is a locked static. If item 1's new shot shows it hiding the gate, (1,4) next to the warden is a cleaner
spot.

## State

Iron Golem, 2026-11-08, branch `golem/Iron/P828`, docs only. I did not edit or build P820's files. The only file
added is this note. The renders I made to check facing are in the session scratchpad, not the repo.

P828 DONE
