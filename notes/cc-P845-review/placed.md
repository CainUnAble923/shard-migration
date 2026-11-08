# cc-P845: what P726 placed, as main holds it now (P741 moved the farmhouse 12 tiles east), with P845's change

Read from `TutorialFarm.cs` and `TutorialCorePlacement.cs` in the code copy. The reviewer's (P835) coordinates were
P726's branch, before P741 moved the farmhouse (`TutorialFarm.HouseMovedX` = 12) and the healing sign. Facing is read
from the art (`bench-art-0x0B2C-0x0B2D.png`).

## The farmhouse, Pip's corner (east wall, wall pieces 0x00A7 at x 6705, floor boards end at x 6704)

- 0x0B2C wooden bench, 6704,3975,7, runs north-south, flush against the east wall, Pip sits here (was 0x0B2D, P845)
- 0x0B2C wooden bench, 6704,3976,7, runs north-south, joins the piece above (was 0x0B2D, P845)
- 0x122A blood, 6703,3975,7, floor beside the bench (west of Pip)
- 0x122D blood, 6703,3976,7, floor beside the bench
- 0x122C blood, 6703,3974,7, floor beside the bench
- TutorialWoundedHelper "Pip" (a mobile), 6704,3975,7, Direction West (into the room), RangeHome 0
- 0x0E21 bandages (TutorialTableBandages, P740), 6702,3975,13, on the farmhouse table beside Pip (unchanged)

## Outside the farmhouse door (door 6702,3978, steps 6701-6703,3979; road from y 3982 south)

- 0xA854 signpost "Lesson: Healing" (`TutorialCorePlacement.HealingSign`), 6701,3980,0, reads from the south: north of
  the road (road tiles at 6701,3982-3984, none north of the sign), beside the walk up to the steps, one column west of
  the door's line (x 6702), so the door's approach (6702,3979-3981) stays clear (unchanged since P741)
- 0x0B2C wooden bench (the farm layout's, not P726's), 6704,3980,0, one piece, two columns east of the door line
  (unchanged; listed because it shows in the outside shot)

## Taken away by the seeder on a world laid before

- 0x0B2D wooden bench at 6704,3975,7 and 6704,3976,7 (P726's crosswise pieces, carried here by P741): swapped for 0x0B2C
- P726's set where it stood before P741: 0x0B2D 6692,3975-3976,7 and the blood at 6691,3974-3976,7 (P741, now with the
  0x0B2D ID it really had)
