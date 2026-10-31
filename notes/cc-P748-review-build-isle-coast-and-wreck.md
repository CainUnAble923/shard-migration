# cc-P748: build review of P746 (the P741 isle round: coast, wreck, signs, farm, bank, League lodge)

Iron Golem, 2026-10-31. A review only: nothing was built, run or deployed, and no build file was edited. I read
`notes\guides\building-and-decorating.md` in full, fetched `origin/golem/Iron/P746` in both copies without changing my
branch, read its notes, its Codex review and the code diff (`git diff main...FETCH_HEAD`), and looked at every render and
TazUO shot I needed to check the items below.

## In plain words

- **The isle round is sent back for fixes.** It is not merged yet.
- **The rule failure:** P746 left no review folder of its own (`notes\cc-P746-review`). P746 was mostly a merge of P741,
  and P741's review folder came with it, so I reviewed that one.
- **What you would notice on the isle:** a grey chimney top poking through the farmhouse roof, an X-shaped stub at
  the farm fence's north-west corner, a farmhouse door that swings out, a League lodge with no name sign, and a still
  stepped shoreline south of the training yard.
- **Nothing for you to do.** The list below goes to the Iron Golem as a fix-up.

## What was looked at

- `notes/cc-P746-review/` does **not exist** on `origin/golem/Iron/P746` (`git ls-tree` finds nothing). P746 is a merge
  fix-up of P741, and the branch does carry P741's folder `notes/cc-P741-review/` (19 renders, 37 TazUO shots, README,
  `placed.md`, 501 lines). I reviewed that folder in full against the guide, so the fix-up has real work to do.
- Renders seen: whole isle, wreck, farm, farmhouse roof off, bank roof off, lodge roof off. Shots seen: coast-wreck,
  coast-yard-south, farm, farmhouse-inside, bank-front, lodge-front.
- Code checked: the door facings (`TutorialFarm.MakeIsleDoor` = `DarkWoodDoor(DoorFacing.WestCW)`;
  `TutorialCorePlacement.MakeDoor` = `WestCCW` for the bank and the lodge).

## What passes

- **Wreck:** both halves of OSI's Malas wreck (0x47B8-0x47D5 West, 0x48A4-0x490F East) draw whole in TazUO. One is in
  the shallows, one is up the beach, and they are broken open toward each other, with driftwood and break water
  between them.
- **Farmhouse shell:** light wood set by the corner rule: post 0x00A9 NW (6699,3972), 0x00A8 along the north row to
  the NE tile, 0x00A7 down the west column to the SW tile, L corner 0x00A6 SE (6705,3978). East windows 0x00B9 in the
  N-S walls. The thatch covers x 6700-6706, y 3973-3979 (one in from NW, one past SE). Gables 0x00C1 on the south
  row. The step 0x0751 (6702,3979,2) climbs north 5 to the floor at 7. The brass sign 0x0BD2 is two tiles east of the
  door.
- **Bank:** corners whole, torches 0x0A0C north and 0x0A07 west at Z 13 on plain wall, counter row with a gap at the
  east end, vault behind it. Carpet corners and edges are right (NW 0x0ACA, NE 0x0ACC, SW 0x0ACB, SE 0x0AC9, N 0x0ACE,
  S 0x0AD0). Sign on the 0x0B98 arm plus 0x0C0B at 6764,3981, two east of the door. Pitched shingle roof.
- **Lodge:** corners whole. Bookcases 0x0A98 on the north wall and 0x0A99 on the west wall face the room. Chairs are
  0x0B4F north of the table and 0x0B50 south of it. Banners 0x1589 hang on the east wall between its windows. Torches
  are on the north and west walls. Pitched roof.
- **Lesson signs:** standing signposts 0xA854, beside their paths, not on them. No rune markers.

## Verdict

BUILD REVIEW P746: FAIL

1. **No renders or placed list left for review.** `notes/cc-P746-review/` and its `placed.md` are missing from
   `golem/Iron/P746` (prompt rule 4; guide section 8). Leave `notes\cc-P746-review\` with `placed.md`, the renders and
   the shots of the fixed build. Copying P741's folder over and updating it for the fixes below is enough.
2. **Farm fence NW corner, 0x0835 at 6677,3967.** The L piece at the north-west makes the X of stubs the guide warns
   about. It shows plainly in `after-farm.jpg`. The guide (section 5, "One fence, one rule") wants the post **0x0838**
   there. Also the SE corner 6695,3983 is two pieces on one tile (0x0836 + 0x0837), but the guide wants **one piece per
   tile**, the L corner **0x0835**.
3. **Farmhouse fireplace 0x0959 + 0x0953 at 6700,3973-3974,7 (west wall).** The fireplace is 24 high, so it rises to
   Z 31 under the west eaves at Z 27. Its chimney comes through the thatch as a grey block at the roof's north-west
   corner (`tazuo-farm.jpg`, `after-farm.jpg`): Chase's "gray thing on the roof". It also stands in front of the west
   window 0x00B9 at 6699,3974, which the roof-off render no longer shows. The guide (11.3, 11.4) wants the hearth on the
   **north wall under the roof's high middle**, at x 6702-6703 below the ridge at 6703, using a south-facing stone
   fireplace. Never in front of a window. Then check in a shot that nothing shows on the roof.
4. **Farmhouse door, `DarkWoodDoor(DoorFacing.WestCW)` (0x06A5) at 6702,3978,7, south wall**
   (`TutorialFarm.MakeIsleDoor`). The guide (2.4) says WestCW in an east-west wall swings outside the wall line. It
   wants **`DoorFacing.WestCCW`** (0x06A9, open along the wall), as the bank and lodge already use. Upgrade the door
   in place on an existing world, and shoot it open.
5. **League lodge has no sign naming it** (door 6782,3995, north wall). `placed.md` lists no sign for the lodge. The
   only nearby sign is the core.league lesson signpost at 6782,3989, six tiles north. The guide (1.1, 2.5) wants a
   sign naming every building by its door. Use the 0x0B98 arm with a board, or a brass 0x0BD2. Put it **two tiles east
   of the door**, outside the north wall, and keep the door's two-tile approach clear.
6. **Walk proof missing.** The README cites `beach-walk.log`, but it is not in the folder or anywhere on the branch.
   Only the console log and frame shots are there, with no per-step Z. The README also says steps changed Z by "no
   more than 3", but the guide (4.1) allows at most **2**. No walk was left for the moved farmhouse step 0x0751
   (6702,3979,2) and door, or for the bank and lodge doors. Leave the per-step Z log of the beach walk, and real
   TazUO walks both ways through the farmhouse step and door, the bank door and the lodge door (guide 8, item 4).
   `tazuo-lodge-front.jpg` is taken from the south-east and does not show the lodge's north door. Add a shot from the
   door side.
7. **South coast by the training yard still saw-tooths.** `tazuo-coast-yard-south.jpg` shows the shoreline stepping
   tile by tile along the yard's south-west sand. The README nevertheless says "the near (west, south) coasts smooth".
   Either lay the surf pieces there by the shore rule (guide 5: 0x17A1/0x17A2 land south, 0x17AB SW diagonal, last sand
   0x17A5..0x17B2), or correct the README and notes to say this coast still steps. The guide says not to claim it is
   gone.

P748 DONE
