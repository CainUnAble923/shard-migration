# cc-P849 placed pieces: the League requisitions board turned to the art that hangs flat on its wall (P836 review of P827)

Only the board's art changes; no piece moves. The rest of the office is P827's layout, listed again below.

## Release (`release/isle-20261028`, stock New Haven, the office in the ML house)

- 0x1E5F (was 0x1E5E), 3458,2602,18, faces east; frame runs north-south, flat on the dividing wall x3457, south of the desk. League requisitions board (RequisitionsBoard, IsLeagueBoard, seeded by `ClusterFRequisitionSeeder`).

## Main (SoS New Haven, the hall)

- 0x1E5E (was 0x1E5F), 3663,2548,0, faces south; frame runs east-west, flat on the hall's north wall y2547, between the bookcases (3660-3661) and the free tile 3664. League requisitions board.

## On an existing world (on load, idempotent)

- A League board already on its spot with the other art is turned to `OfficeBoardItemID`, the same item: `ClusterFRequisitionSeeder.Seed` logs "League board: art turned from 0x.... to 0x....". Fact: `ABoardWithTheEdgeOnArtIsTurnedOnLoadOnceAndStaysTheSameItem` (a second seed turns nothing).
- A League board on one of P803's old spots still moves to the spot and takes the new art (P803/P827; both after runs' `shard.log`: "League board: moved from (3459, 2596, 18) to (3458, 2602, 18)" on the release, "moved from (3662, 2547, 0) to (3663, 2548, 0)" on main).

## The office (unchanged from P827)


Two towns, one office each, as in `notes/cc-P803-review/placed.md`: the **isle release** (the ML New Haven house, walls
x3453-3462, y2596-2603, floor Z 18, front door in the north wall at 3459,2596; the office is x3458-3461 behind the
dividing wall x3457, whose doorway is 3457,2599) and **main** (SoS Haven's hall, walls x3658-3674, y2547-2562, floor Z 0,
open arch in the south wall at 3667-3668,2562). Every piece is a server item seeded on load: the three office addons
(`ClusterFRegistrarOfficeSeeder`, design `design/registrar-office/layout.json`) and the League requisitions board
(`ClusterFRequisitionSeeder`). No map statics changed. Map pieces were read with `notes/cc-P803-tools/office_statics.py`
(release: `D:\UO\tool-trials\client-data-copy`; main: `D:\UO\golems\Iron\p735-work\patched`).

### Isle release

### Changed by cc-P827

| Piece | Where (x,y,z) | Facing / wall | What changed (P824 item) |
|---|---|---|---|
| League requisitions board, art **0x1E5F** (cc-P849; P827 had 0x1E5E, edge-on) | 3458,2602,18 | east face, on the office's west (dividing) wall, plain piece 0x0008 at 3457,2602 | was 3458,2598, where its art drew over the map's stretched hide 0x106B on 3458,2597 (item 1). 3458,2602 is the west wall's only other tile with a wall behind it: 3457,2599 is the quarters' doorway and 3458,2600-2601 the map's desk. Moved on load (same item). `release-board-desk-before-after.png`: the corner without and with the board |
| 0x0A9A bookcase | was 3458,2602,18 | - | removed: it gave its tile to the board. The office keeps its north-wall case 0x0A98 at 3461,2597 |
| 0x2D61 inkwell, 0x2270 scroll | 3458,2600,24 | on the desk's north end (map table 0x0B83) | were on 3458,2601,24, the desk's south end, which the board's art now reaches over |
| 0xA854 signpost "League of Extraordinary Citizens" | 3460,2591,20 | reads from the south: on the flat verge just north of the road (road y 2592-2595), facing it; one tile east of the door's line x 3459 | was 3463,2596,16, south of the road with its back to the street (item 2). The tile is flat (land corners 20, 20, 20, 19), at the foot of the bank north of the road |

### Kept from cc-P803

| Piece | Where (x,y,z) | Facing / wall |
|---|---|---|
| 0x11C9 potted tree | 3458,2595,15 | outside, west of the door's approach (3459,2595 clear) |
| 0x1589 League banner | 3463,2599,26 | flat on the east wall, outside, between the east windows |
| 0x1E25 books, 0x1810 hourglass | 3458,2600,24 and 27 | on the desk |
| 0x0A98 bookcase | 3461,2597,18 | faces south, north wall (plain 3461,2596) |
| 0x0B26 candelabra | 3461,2601,18 | off the east window's tile |
| 0x0E42 wooden chest | 3455,2598,18 | faces south, at the foot of the bed |
| 0x0A9A bookcase | 3454,2599,18 | faces east, quarters' west wall (plain 3453,2599) |
| 0x2272 scroll | 3454,2598,24 | on the quarters' table |

The board's two neighbours along its wall: 3458,2601 (the desk's south end, no prop on it now) and 3458,2603 (the south
wall's row). The map's hide on 3458,2597 stands alone again. Window floor tiles (3456,2597; 3460,2597; 3454,2598;
3461,2598; 3461,2602; 3456,2602; 3460,2602; 3454,2602) still hold no floor piece of ours.

### Main

### Changed by cc-P827

| Piece | Where (x,y,z) | Facing / wall | What changed (P824 item) |
|---|---|---|---|
| 0x0B98 sign arm + 0x0BCF board "League of Extraordinary Citizens" | 3671,2563,0 | sticks out from the south wall, plain piece 0x0034 at 3671,2562; three tiles east of the arch | was 3670,2563, hanging on the stained-glass window 3670,2562 (item 3). Rendered at 3671 and 3672 (`main-sign-3671-vs-3672.png`): at 3672 the arm touches the window at 3673; at 3671 it clears both windows |
| League requisitions board, art **0x1E5E** (cc-P849; P827 had 0x1E5F, edge-on) | 3663,2548,0 | south face, north wall, plain 0x0034 at 3663,2547 | was 3662,2548, where its art covered the bookcase 0x0A97 on 3661,2548 (item 4). Its neighbours 3662,2548 and 3664,2548 are both empty |
| 0x11CA flowerpot | 3673,2548,0 | north wall, north-east corner, beside the chest | was 3663,2548, the board's new tile |

### Kept from cc-P803

| Piece | Where (x,y,z) | Facing / wall |
|---|---|---|
| 0x11C9 potted tree | 3665,2563,0 | outside, west of the arch |
| 0x1E25 books, 0x2D61 inkwell, 0x2270 scroll, 0x1810 hourglass | 3661,2549,6 (hourglass 9) | on the map's counter 0x0B3F |
| 0x0A98 bookcase, 0x0A97 bookcase | 3660,2548,0 and 3661,2548,0 | face south, north wall |
| 0x0B26 candelabra | 3659,2548,0 | north-west corner |
| 0x0E42 wooden chest | 3672,2548,0 | faces south, north wall |
| 0x0A98 bookcase | 3670,2548,0 | faces south, north wall (beside the map's fish trophy 3671: there before cc-P803, left as P824 noted) |
| 0x2272 scroll | 3672,2551,6 | on the long counter |

The map's own pieces on the north wall's row: bookcases 3665, 3667, 3669, flowerpots 3666, 3668, the fish trophy 3671.
The hall's windows are the stained glass of the south wall (3661, 3662, 3664, 3665, 3670, 3673 at y 2562); none of our
pieces stands on their floor tiles (y 2561), and the sign arm hangs from none of them.

### Checked by facts

`server/tests/Misc/LeagueOfficeDecorVerification.cs` in each copy (cc-P827 section 6):
`TheBoardHasItsStretchOfWallToItself` (no office piece and none of the map's wall pieces on the tile each side of the
board along its wall), and `TheSignArmHangsFromAPlainWallClearOfTheWindowsAndTheArch` (main) or
`TheSignpostStandsNorthOfTheRoadOffTheDoorsLine` (release). Each went red with the cc-P803 spots put back
(`notes/cc-P827-tools/red-main.txt`, `red-release.txt`).
