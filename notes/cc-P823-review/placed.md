# cc-P823: placed pieces (fix-up of cc-P817 after P821's build review)

## Changed by cc-P823

| Piece | Where (x,y,z) | Facing | What changed |
|---|---|---|---|
| 0x049C slate ceiling (map), bank | was 6758,3973..3980,20 (8 tiles) | - | removed: the roof's west eave column, where the west slope 0x05C4 sits at Z 19, under the ceiling's 20, so the ceiling drew as grey squares on the slope (P821 item 1). The roof 0x05C4 at 6758,3973..3981,19 is unchanged and now shows plain. |
| 0x049C slate ceiling (map), League lodge | was 6778,3996..4003,20 (8 tiles) | - | removed for the same reason: the lodge is laid by the same builder code and had the same eight squares (`lodge-before-isorender.png`). Not on P821's list; same rule (guide 1 item 1, 2.3). |

Nothing else moved. The ceiling stays on every other column of both rooms (Z 20, under roof pieces at 22 or higher).
Both changes are in `trammel.mapops` (16 S+ lines gone), the driver (`notes/cc-P662-tools/build_isle.py` skips the
west eave column) and its record `notes/cc-P662-tools/statics-placed.csv`.

Everything below is P817's list, unchanged and still true.

# cc-P817: placed pieces (the Wakening Isle bank, item 7; NPC facings, item 6)

Map 32 (the Fold) and every isle copy; isle coordinates (Trammel site A). "map" = a static in our map patch
(`player-package/vendor/shattered-legacy-map/trammel.mapops`, and the driver's `notes/cc-P662-tools/isle-sets.json`);
"server" = a server item or NPC the seed places and upgrades on world load (`TutorialCorePlacement.SeedOn`).
Every other bank piece is unchanged from cc-P720 (listed below for the reviewer, as the map holds it).

## Changed by cc-P817

| Piece | Where (x,y,z) | Facing | What changed |
|---|---|---|---|
| 0x09A8 strongbox (map) | 6762,3973,0 | (south face, as before) | moved from 6766,3974 (by the east wall, apart from the chests) to the back wall, under the north torch, behind Merrin |
| 0x11CA potted plant (map) | was 6766,3978,0 | - | removed: it crowded the south-east corner beside the standing candelabra 0x0B26 (6766,3979) |
| 0x0E7C practice bank box (server, "practice bank box") | 6761,3973,0 | (south face) | moved from 6760,3975 (alone mid-floor behind the counter) to the back wall with the vault chests, clear of the north window's floor tile 6760,3973; the old one is removed on load (`MoveOldProps`) |
| 0xA854 bank lesson signpost (server, "Lesson 7: The bank") | 6757,3982,0 | reads from the south (guide 6) | moved from 6766,3981 (on the road at the apron's east end) to grass north of the road at the bank's south-west corner, off the apron and the door's line; moved on load (`TutorialStationMarker.MoveToSign`) |
| Merrin, Banker (server) | 6762,3976,0 | **South** | was North (no facing set: he faced the vault chests on the back wall); faces the counter's customer side, the carpet and the door; turned on load (`TutorialBankerVoice.FaceCounter`) |

## Bank, unchanged (cc-P720, as the map holds it; checked for doubles: none)

Walls, windows, roof: OSI's stone shop set (isle-sets.json wallsShop/pitched), door 0x06A9 DarkWoodDoor WestCCW at
6762,3980,0 (server), south wall y 3980, north wall y 3972, west x 6757, east x 6767; windows 6759,3980 6765,3980
6767,3975 6767,3978 6760,3972 6764,3972 6757,3976.

| Piece | Where | Facing / note |
|---|---|---|
| 0x0B40 counter x7 | 6758-6764,3977,0 | serving side south, gap at the east end (6765-6766) |
| 0x0EED gold coins | 6761,3977,6 | on the counter |
| 0x1852 scales | 6763,3977,6 | on the counter |
| 0x0E41 vault chest | 6758,3973,0 | back wall |
| 0x0E40 vault chest | 6759,3973,0 | back wall |
| 0x0E41 vault chest | 6766,3973,0 | back wall, north-east corner |
| 0x0B26 candelabra | 6765,3973,0 | north-east, beside the corner chest |
| 0x0B26 candelabra | 6766,3979,0 | south-east, by the counter's open end |
| 0x0A0C wall torch | 6762,3973,13 | north wall (south-facing art) |
| 0x0A07 wall torch | 6758,3975,13 and 6758,3978,13 | west wall (east-facing art) |
| 0x0B2C bench | 6758,3979,0 | south-west corner, for waiting |
| carpet 0x0ACA/0x0ACE/0x0ACC/0x0ACB/0x0AD0/0x0AC9 | 6759-6765,3978-3979,0 | NW, N edge, NE / SW, S edge, SE (guide 2.5) |
| 0x0B98 sign hanger + 0x0C0B bank sign | 6764,3981,10 | outside the south wall, two east of the door (guide 2.5) |
| 0x11CA potted plant | 6760,3981,0 | outside, west of the door on the apron |
| paved apron (land) | 6759-6765,3981-3982 | before the door |
| brass fountain (server addon, lagatha-brass-fountains) on its paved pad | 6767-6769,3983-3985 | unchanged; see the notes (kept, a proposal) |

## Other isle NPCs' facings (item 6), checked

| NPC | Where | Facing | Verdict |
|---|---|---|---|
| Tamsin, guide | 6640,3992 | West | faces the wake beach where trainees arrive: right |
| the pale rat (death lesson) | 6736,3998 | default | a creature in the open yard: no wall |
| Sera, healer | 6740,4000 | default (North) | in the open training yard: no wall in front (shot) |
| Merrin, banker | 6762,3976 | South (was North) | fixed |
| Elara Voss | 6782,3999 | default (North) | faces the lodge's north door: right |
| Wren, farmhand | the farm gate | East | faces the road and the gate: right |
| Tobin, vet | beside Wren | East | faces the road: right |
| Pip | 6704,3975 bench | West | faces into the farmhouse (P726): right |
