# cc-P866: build review of P857 (the variable carpet)

## In plain words

- The carpet deed from P857 looks right in the game: both carpets the Golem laid have a whole border on every side and
  closed corners, and all six patterns show up whole in the colour-and-style window.
- It still fails review on paperwork: P857 never left the review folder (`notes\cc-P857-review\`) with a list of what
  it placed. Without that folder the build rules call it a FAIL.
- The Iron Golem gets a short fix-up: add the folder and the list, plus shots of a carpet that is longer than it is
  wide. No game code needs to change.
- Nothing for you to do.

Iron Golem, 2026-11-10. Reviewed `golem/Iron/P857` (docs `7f1c30dd`) against `notes\guides\building-and-decorating.md`,
read in full. Fresh session; I did not build P857.

## What was there

- `git ls-tree -r --name-only origin/golem/Iron/P857 -- notes/cc-P857-review` lists nothing, and `git archive` of that
  path fails ("did not match any files"). No `placed.md` exists anywhere on the branch. Step 4 of the review prompt
  makes this a FAIL.
- The proof P857 did leave is in `notes/cc-P857-shots/main/` (TazUO shots on the private 2596 shard) and
  `notes/cc-P857-variable-carpet.md`. I looked at all of it anyway, so the fix-up is small.
- Code diff (`ShatteredLegacy`, `main...origin/golem/Iron/P857`): `server/customizations/Items/Addons/VariableCarpet.cs`
  (new), its tests, `CHANGELOG.md`, `VERSION`. It adds no buildings, walls, doors, stairs, roofs, signs, shores or
  foliage. The only placed art is the stock carpet set, laid by a player's deed inside their own house.

## Checks

| Check | Result |
|---|---|
| Carpet corners and edges against the guide (2.5, the P734 render-checked carpet: corners NW 0x0ACA, NE 0x0ACC, SE 0x0AC9, SW 0x0ACB; edges N 0x0ACE, S 0x0AD0, W 0x0ACD, E 0x0ACF) | **Match.** `ArtAt` names its corners by screen (north = map NW). The red style maps NorthCorner 0xACA -> NW, EastCorner 0xACC -> NE, SouthCorner 0xAC9 -> SE, WestCorner 0xACB -> SW, NorthWestEdge (x = 0) 0xACD -> W, NorthEastEdge (y = 0) 0xACE -> N, SouthEastEdge 0xACF -> E, SouthWestEdge 0xAD0 -> S. Middles 0xAC8 plain, 0xAC7 patterned. |
| `p857-carpet-laid.jpg` (4 by 4 red, wine hue) | Whole: border on all four sides, all four corners closed, middle filled, flat on the floor at Z 7. |
| `p857-carpet-blue-gold.jpg` (4 by 4 blue with gold) | Whole, the same way. |
| `p857-gump.jpg`, `p857-gump-wine.jpg` (3 by 3 previews of all six styles) | All six draw as whole framed carpets: blue patterned, blue plain, blue with gold, red patterned, red plain, gold. |
| Doors | The carpet stops one tile short of the house door (stock `DoorTooClose`); the door is the house multi's own and is untouched. |
| `p857-refused-outside.jpg`, `p857-remove-confirm.jpg`, `p857-rolled-up.jpg` | Refused outside the house, deed kept; confirm asked; carpet gone, plain floor left, nothing stray. |
| Walls, stairs, roofs, signs, wall-mounted items, shores, bridges and docks, foliage | None placed by P857 (the house is a stock deed the trainee placed for the test). |
| What to use where | Stock carpet art 0x0ABD-0x0AF9 is the right choice for a house carpet; nothing better is on disk for this use. |

The build itself reads right. It fails only on the missing review proof.

BUILD REVIEW P857: FAIL

1. No renders or placed list left for review: `notes\cc-P857-review\` and its `placed.md` are missing on
   `golem/Iron/P857`. Guide section 8 and checklist item 8 want them. Add the folder with a `placed.md`: one line per
   style (six), giving the corner, edge and middle item IDs as `ArtAt` lays them (map NW/NE/SE/SW corners, N/S/W/E
   edges, middle). Add one line for each carpet laid in the shots (style, hue, location 1984,2240,7, size). Copy or
   move the current shots in, each under 1 MB.
2. Every laid carpet in the proof is a 4 by 4 square, so a width/height or x/y swap would not show. Add one render
   (`render_addons.py ids:` or `isorender.py` of the laid carpet), or one TazUO shot, of each of the six styles laid
   non-square (for example 5 by 3, inside a house wide enough). Each must show the border whole on all four sides and
   the corners closed, as guide 11.2 asks ("render it alone and look"). If you shoot in TazUO, use the default camera
   on the private 2596 shard.

No game code change is asked for. P857's own files are untouched by this review.

P866 DONE
