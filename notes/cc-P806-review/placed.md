# cc-P806 placed pieces

Stock New Haven (Trammel, the release branch) unless marked main. Seeded at world load. Signposts stand on the land's average Z at their tile.
Everything from P799 that this fix-up did not touch is in `notes\cc-P799-review\placed.md`, and is repeated here under its heading.

## League ankh (P799, unchanged)

- AnkhWest addon (0x0003 head, 0x0002 foot), 3464,2600,27 and 3464,2601,27, facing west, release: exactly over the map's own statics of the same art.
- AnkhWest addon (0x0003 head, 0x0002 foot), 3676,2562,0 and 3676,2563,0, facing west, main: by the League hall's south-east corner.

## Rook's bench

- 0x0B2D wooden bench, 3502,2530,22, runs east-west, Inn's south yard, Rook sits here (was 0x0B2C)
- 0x0B2D wooden bench, 3503,2530,22, runs east-west, joins the piece above (was 0x0B2C)
- Rook (NPC), 3502,2530,22, facing South: the yard, the moongate exit 3502,2532,22 and the square (was North, at the Inn's wall)
- 0x0B2D wooden bench, 3669,2636,0, runs east-west, main, Rook sits here (was 0x0B2C)
- 0x0B2D wooden bench, 3670,2636,0, runs east-west, main (was 0x0B2C)
- Rook (NPC), 3669,2636,0, main, facing North: checked, not turned. A stone wall stands to the south at y 2639, and the moongate exit 3669,2634,0 and the square are north of him.

## Signposts (release)

All four are 0xA854, the face that reads from the south, so each board faces the road to its south.

- 0xA854 signpost, 3469,2624,14, "To the mine: south along the road, then over the grass to the mountains", north of the road running west at y 2627 (moved from 3477,2617)
- 0xA854 signpost, 3520,2568,7, "The stables: the sick-bay stall is inside, in the north row", north of the street along the stables, road 1 tile south (moved from 3521,2573). **Deviation, see below.**
- 0xA854 signpost, 3469,2589,10, "Housing lesson, stop 1: a small house", north of the street, in the bed by the statue, road 2 tiles south (moved from 3464,2596)
- 0xA854 signpost, 3474,2601,10, "Housing lesson, stop 2: where houses can be built", the lawn, road directly south (P799, unchanged; P805 passed it)

## Stable props (release)

- 0x0FFA bucket of water, 3534,2574,8, in the sick-bay stall, on the straw (moved from 3535,2575,7, where the stall's east wall hid it from the default camera; the review had passed that tile and asked for a shot)

## Lesson stops and creatures, placed only during a lesson (release)

- Housing stop 1, 3468,2591, on the street beside its sign (moved from 3465,2596, so that "beside the stop" and "north of the path" both hold). Stop 2 unchanged, 3474,2603.
- Bard echoes, 3412,2604,60 and 3413,2603,60, on the stage's open planks (moved from 3410,2603,60 and 3411,2604,60, under the canopy)
- Injured horse, 3534,2575,7, sick-bay stall, seen only by its trainee
- Sparring echo, 3531,2541,20, Warrior Guild's yard
- Magery training echo, 3484,2497,52 and mage demo echo, 3488,2500,52, Magery School's south room

## Taken away on a world already seeded (seen in the shard log of a world P799's image saved)

- The two 0x0B2C bench pieces, the three signs and the bucket at their old tiles: "placed 6 pieces (took away 6 from old spots), moved 1 Rook". Rook turned South.
- P276's old tutorial farm at 3372-3401 x 2603-2619, by P743's ClearHaven, as on main.

## Deviation, for Chase

**Stables sign, 3520,2568.** The rule is "road within 3 tiles south of the sign, none north of it or beside it". This tile has road directly south and no road beside it, but a strip of dirt two tiles north at 3520,2566. That strip is on top of a bank, Z 20 against the sign's Z 7, so nobody on this street can walk onto it: the bank is a cliff here (see `after-stables-sign.jpg`). The sign plainly reads as standing on the north side of the street it marks.

The tiles that meet the rule to the letter are the bank top at 3517-3519,2564-2565, Z 20, about 15 above the road and further from the door, and there the board would face the strip of dirt, not the street to the stables. I did not use them.

**Stop 1 and the cottage.** The stop is now on the street, about 9 tiles from the cottage's door at 3459,2596, so it says "the thatched cottage across the street, south-west of here" and not "this cottage".
