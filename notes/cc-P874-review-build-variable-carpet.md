# cc-P874: build review of P871 (the variable carpet, fixed up after P866)

## In plain words

- I checked the carpet deed's pictures and in-game shots against the building guide, and it passes. All six carpet
  styles go down with whole borders and closed corners, whether the carpet is long east-west or north-south.
- Once this branch comes in, the carpet deed (P857, fixed up by P871) can merge. You will notice nothing new until a
  store sells the deed.
- Nothing for you to do here. P857's open questions still stand: which store sells the deed, at what price, and
  whether 18 tiles a side is the right cap.

Iron Golem, fresh session, 2026-11-10. Docs copy `D:\UO\golems\Iron\shard-migration`, branch `golem/Iron/P874`;
P871 read from `origin/golem/Iron/P871` without switching branches. This was a review only: nothing was rebuilt and
no shard was started.

## What I read

- `notes\guides\building-and-decorating.md`, in full: the checklist, walls and corners, roofs, doors, signs and
  furnishing (the carpet rule in 2.5), facing, heights, land, markers, proof (section 8), the human-builder lessons
  (9.2 item 4: carpets from edge pieces), What to use where, and the P734 lessons (11.2: read facing from the art).
- `notes/cc-P871-review/` (archived to my scratchpad): `placed.md`, the 7 renders, the 13 shots (6 from P871, 7 from
  P857), `walk.txt` and `server-view.txt`.
- `notes/cc-P871-cont-fixup-variable-carpet.md`.
- The code diff, `git diff main...origin/golem/Iron/P871`: `server/customizations/Items/Addons/VariableCarpet.cs`
  and `server/tests/Items/Addons/VariableCarpetVerification.cs` (both new), plus `CHANGELOG.md` and `VERSION`.

## What P871 places

P871 places no world statics. It is a house addon: a deed lays one rectangle of stock carpet art, between 3 and 18
tiles a side, on the owner's floor. So most of the checklist (walls, doors, stairs, roofs, signs, shores, bridges,
docks, foliage) has nothing to check. What does apply: every carpet piece's facing (section 3; 11.2), the carpet built
from corner, edge and middle pieces (2.5; 9.2 item 4), the proof left for review (section 8), and the best piece on
disk (section 10).

## Checks, one by one

1. **Placed list and renders present** (section 8): yes. `placed.md` lists the six styles' nine pieces each, then every
   tile of all eight proof carpets with ID, x,y,z and role. Every image is under 1 MB.
2. **Corner and edge pieces, read from the code.** In `VariableCarpetStyle.ArtAt`, x == 0 is the map's west column
   and y == 0 the north row. The code's `NorthCorner`/`EastCorner`/`SouthCorner`/`WestCorner` are therefore the
   map's NW/NE/SE/SW tiles, and `NorthWestEdge`/`NorthEastEdge`/`SouthEastEdge`/`SouthWestEdge` are the W/N/E/S
   edges. The addon lays component (x, y) at offset (x, y), so width runs along x and height along y.
3. **The red set against the guide** (2.5: edges N 0x0ACE, S 0x0AD0, W 0x0ACD, E 0x0ACF; corners NW 0x0ACA, SE 0x0AC9,
   NE 0x0ACC, SW 0x0ACB): the style table matches exactly, for both red styles. The guide has no rule for the blue,
   blue-with-gold or gold sets, so I judged those by the art, below.
4. **Facing from the art** (11.2): `carpets-all-six.jpg` and the six per-style renders show each style twice, once
   long along x (5 by 3) and once long along y (3 by 5). I checked all twelve carpets: each fringe and border runs
   unbroken round all four sides, each corner closes, and no edge piece is turned on its side. A swapped pair of
   corners or edges would show up on a carpet that is not square, and none does.
5. **In game** (default camera, TazUO): the six P871 shots show each style laid by the Player-account trainee in their
   own house, alternately 5 by 3 and 3 by 4. All six draw whole, with the long axis the right way. `walk.txt` finds
   each corner's art on its own map-corner tile (20 of 20 PASS), and `server-view.txt` agrees on width and height.
   P857's two 4 by 4s (wine-hued red, and blue with gold) draw whole as well.
6. **Height:** every piece is at the floor's Z (7), flat, with no lip. A carpet is not a walkable join; the trainee
   walked in and out of the house over it.
7. **Nothing stray, doors clear:** each carpet was rolled up before the next was laid (`p857-rolled-up.jpg` shows the
   bare floor). The stock door-proximity check kept the 3 by 4 off row 2244 beside the door, and placement outside
   the house was refused (`p857-refused-outside.jpg`).
8. **What to use where** (section 10): the pieces are the stock carpet art 0x0ABD-0x0AF9 (corner, edge and middle sets),
   which is the right material for a carpet. No pack on disk offers a better stock carpet.

## Remarks (not failures)

- The P871 house is a stock deed house, and the stone yard in the renders is a test floor. Neither is part of this
  build, so I did not review them.
- In the gump's colour previews (`p857-gump-wine.jpg`) the "Wine" hue tints every preview the same dark red. That is
  how a hue works, not a placement fault.

BUILD REVIEW P871: PASS

P874 DONE
