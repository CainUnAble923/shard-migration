# cc-P837: placed pieces (P818's League lodge door, merged onto main with P817's bank and P823's eave fix)

cc-P837 placed nothing new. It brought P818's build onto current main and resolved the merge. The map patch
(`trammel.mapops`) now carries P818's 22 lodge lines exactly as P818 shipped them, on top of main. Checked: the diff of
the merged file against main is line for line the diff of P818's file against its own base, B lines aside. Main's P817 bank
moves and P823's ceiling removals are kept. `tools/tests/test_mapops.py` passes 14 of 14 against the merged code copy.

New renders of the merged map (bank and lodge together, server doors and signs drawn in by `notes/cc-P837-tools/view837.py`):
`bank-lodge-merged-isorender.jpg` (roofs on) and `bank-lodge-merged-cutaway.jpg` (statics above Z 19 left out). Every
other image and `walk-lodge.log` here is P818's own, copied from `notes/cc-P818-review/` (P826 reviewed them: PASS). The
TazUO shots were not taken again: the lodge's map lines and server spots are unchanged from P818.

## Pieces beside the lodge that come from main (not changed by cc-P837)

| Piece | Where (x,y,z) | Facing / note | From |
|---|---|---|---|
| 0xA854 banking lesson signpost (server, core.banking) | 6757,3982,0 | reads from the south; north of the road at the bank's south-west corner | cc-P817 |
| 0x09A8 strongbox (map) | 6762,3973,0 | on the bank's back wall | cc-P817 |
| 0x11CA potted plant (map) | was 6766,3978,0 | removed | cc-P817 |
| 0x049C slate ceiling (map) | was 6758,3973-3980,20 and 6778,3996-4003,20 | removed from the bank's and the lodge's west eave column | cc-P823 |
| Merrin, Banker (server) | the bank's counter | faces his counter's customer side | cc-P817 |

## From cc-P818 (unchanged by the merge)

Map 32 (the Fold) and every isle copy; isle coordinates (Trammel site A). "map" = a static in our map patch
(`player-package/vendor/shattered-legacy-map/trammel.mapops`), laid by the isle driver (`notes/cc-P662-tools/build_isle.py`,
`LODGE_DOOR`, and `isle-sets.json` interiors.lodge); "server" = an item or NPC the seed places and upgrades at every
world load (`TutorialCorePlacement.SeedOn`). The lodge: floor x 6778-6786, y 3996-4002; walls x 6777 and 6787, y 3995 and
4003; post at the north-west, L corner at the south-east (unchanged, OSI's stone shop set).

## Changed by cc-P818

| Piece | Where (x,y,z) | Facing / note | What |
|---|---|---|---|
| 0x06B3 DarkWoodDoor (server) | 6787,4000,0 | **NorthCW**, in the east wall's line; open it folds north onto 6787,3999 along the wall (render `door-test.png`, fact 1) | the lodge's door, moved from the north wall |
| (opening) east wall tile (map) | 6787,4000,0 | floor 0x04A9 stays; the run piece 0x0057 there is gone | the door's opening |
| 0x0058 stone wall, east-west run (map) | 6782,3995,0 | the north wall's run piece | where the old door was; its floor static 0x04A9 under the north row is gone (guide 2.2) |
| old DarkWoodDoor WestCCW (server) | 6782,3995,0 | - | taken away on load (`RemoveOldLodgeDoor`) |
| 0x0E31 brazier (map) | 6788,3999,0 | outside the east wall, north of the door's approach | the lit doorway |
| 0x0E31 brazier (map) | 6788,4001,0 | outside the east wall, south of the door's approach | the lit doorway |
| 0x0525-0x0528 sandstone bricks (map) | 6788,4000,0 and 6789,3990-4000,0 (12 tiles, variants by (x+y) mod 4) | flat floor statics on the grass | the walk from the road to the door; walked both ways at Z 0 (`walk-lodge.log`) |
| 0x0E31 brazier inside (map) | was 6786,4000,0 | - | removed: it stood on the new door's inside tile |
| 0x0B26 candelabra (map) | 6786,3999,0 (was 6786,3998) | - | off the floor tile of the east window 6787,3998 (guide 11.4), beside the door inside |
| 0x1589 League banner (map) | 6788,4002,8 (was 6788,4000,8) | flat on the east wall from outside (guide 3) | off the door's own tile; the other stays at 6788,3997,8 |
| 0xA854 "The League lodge" signpost (server) | 6788,3984,0 (was 6781,3989) | reads from the south | north of the road where the walk leaves it (road y 3985-3989 at x 6788-6789); moved on load (`MoveLodgeSign`) |
| 0xA854 "Lesson 8: The League of Extraordinary Citizens" (server, lesson marker) | 6789,3984,0 (was 6782,3989) | reads from the south | beside the lodge sign, north of the road at the walk's mouth; moved on load (`MoveOldMarkers`) |
| Elara Voss, LeagueRegistrar (server) | 6782,3999,0 | **East** (was North, at the old door) | faces the east door; turned on load (`TurnElara`) |
| lesson stop (server, `TutorialWorld.LodgeStop`) | 6789,4000 (was 6782,3994) | - | the walk's foot, east of the door; the arrow points at the door until the trainee is inside, then at Elara |

Window floor tiles of the east wall (guide 11.13): 6786,3998 empty now (was the candelabra), 6786,4001 empty. The door's
two-tile approach (6788,4000, 6789,4000) holds only the walk; the braziers stand beside it, not on it.

## Unchanged (cc-P720, cc-P751), rechecked in the renders and shots

Walls with windows 6779,3995, 6785,3995 (north), 6780,4003, 6784,4003 (south), 6787,3998, 6787,4001 (east), 6777,3999
(west); shingle roof with the stone gable on the south row; bookcases 0x0A98 on the north wall and 0x0A99 on the west
wall; writing tables 0x0B4A with book and scroll; the long table 0x0B90 with chairs; carpet; torches 0x0A0C (north wall)
and 0x0A07 (west wall); the League notice board 0x1E5E on the north wall inside (6780,3996, server). The west slope's
row of grey squares (the ceiling 0x049C on the west eave) is P821's finding, fixed by cc-P823, not on this branch.
