# cc-P875: build review of P872 (fix-up of P858: real-light lamps and the Festival Peddler's wagon)

## In plain words

- I checked the fix-up to the fortune teller's wagon beside the Festival stall in New Haven against the building
  guide.
- The roof is bare now: the four green symbols and the grey "vent" are gone in every picture.
- The black cat sits on the potion kegs on the porch, beside the door, where you see it as you climb the steps.
- Nothing for you to do: the wagon and lamps can merge.

Iron Golem, 2026-11-10. Reviewed `origin/golem/Iron/P872` in both copies (fetched, not checked out) against
`notes/guides/building-and-decorating.md`, read in full. Looked at `notes/cc-P872-review/placed.md` (207 parts),
`walk-log.txt`, both renders (`main-stall-wagon-3647-2632.jpg`, `main-wagon-cutaway.jpg`), all ten TazUO shots, the
notes `notes/cc-P872-cont-fixup-lamps-and-peddler-wagon.md`, the earlier review `cc-P868`, and the code diff
(`FestivalWagon/FortuneTellerWagon.cs`, `FortuneTellerWagonDesign.cs`, `ShardLamps.cs`, the stores, the facts).

BUILD REVIEW P872: PASS

## What I checked

- **P868's three fixes, one by one:**
  1. Rune glyphs 0x4862, 0x4856 (two) and 0x4844 at z 50-56: gone from the design file (no 0x48xx rows) and from
     `placed.md`. In the render and in `p872-stall-and-wagon.jpg`, `p872-porch.jpg` and `p872-stair-going-down.jpg`
     (enlarged crop) the shingles show nothing on them. The wagon keeps three lights (lantern 0x0A22, lamp stand
     0x4C53, stained glass 0xA5F8), and the night shot shows the porch lantern lit.
  2. Vent 0x2419 on the ridge: gone. The ridge reads clean in every shot.
  3. Black cat 0x4689: moved from the roof corner to 3646,2636,31 (offset -1,4,31), on top of the two potion kegs
     0x9E36 at z 21 and 26 on the porch's west side. In the cutaway and the porch shot (enlarged) it sits on the top
     keg, not floating, beside the door and clear of the walk at x 3647 (the walk log steps 3647,2637 -> 2636 -> 2635
     without a stop). Its line is kept.
- **Roof (guide 1.1, 2.3, 2.6):** from z 38 up only bark roofing 0x26F8-0x26FA, shingles 0x2C35 and the gable ends
  0x0443/0x299B in `placed.md`; nothing stray on top. Fact 6 checks the same.
- **Stair (4.1, 4.2), unchanged from P858 and passed by P868:** light wood north steps 0x0722 climbing north toward the
  porch, one per tile, 5 a step, blocks 0x0721 under the upper steps; walked for real both ways again (0, 0, 2, 7, 12,
  17, 21, 21, 19 and back), shots from the foot, on the way up and going down.
- **Walls, door, wall-mounted pieces:** unchanged from P858; the doorway 0x9B29 at 3647,2635 opens from the porch
  onto the carpet; the daemon mask on the west wall faces east into the room; the painting, stained glass and wheels
  hang outside the east wall facing the street. No piece turned; one variant only.
- **Signs, shores, bridges, docks, foliage:** none placed by this build (the stall keeps its own sign; the wagon is
  named by its painting, as P868 accepted).
- **Better pieces from What to use where:** no fit for this design; it is a ported stock-art addon kept whole.
- **Lamps:** store items, not placed in the world; eleven laid and lit on the proof shard, the lantern turned and
  stayed lit, the jack-o-lantern goes out on a second double-click.

## Seen, not part of the verdict

- The release's New Haven still has no spot for the stall or the wagon, and the prices are placeholders (P858's open
  questions, unchanged).
- Skeletons from pinned post-UOML spawners still walk New Haven's square in the shots (noted by P858).

P875 DONE
