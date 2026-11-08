# cc-P803: placed pieces, the League field office in New Haven

Two towns, one office each: the **isle release** (what testers play; the ML New Haven house, walls x3453-3462,
y2596-2603, floor Z 18, door in the north wall at 3459,2596) and **main** (SoS Haven's hall, walls x3658-3674,
y2547-2562, floor Z 0, open arch in the south wall at 3667-3668,2562). Every piece is a server item seeded on load: the
three office addons (`ClusterFRegistrarOfficeSeeder`, design `design/registrar-office/layout.json`) and the League
requisitions board (`ClusterFRequisitionSeeder`). No map statics changed. Facings read from renders against a wall
(`board-facings.png`, `piece-facings*.png`).

## Isle release

### Changed by cc-P803

| Piece | Where (x,y,z) | Facing / wall | What changed |
|---|---|---|---|
| League requisitions board, art 0x1E5E | 3458,2598,18 | east face, on the office's west (dividing) wall x 3457 | was 3459,2596,18: on the front door's own tile, in the north wall line, behind the door; moved on load (same item) |
| 0xA854 signpost "League of Extraordinary Citizens" | 3463,2596,16 | reads from the south; grass by the north-east corner, road (y 2592-2595) north of it | replaces sign arm 0x0B97 + board 0x0BCF at 3463,2597,13, which hung from no wall, under the eave (guide 11.12) |
| 0x1589 League banner | 3463,2599,26 | flat on the east wall, outside, between the east windows (3462,2598 and 3462,2602) | new |
| 0x0A98 bookcase | 3461,2597,18 | faces south, north wall (plain piece 3461,2596) | was 0x0A99 (faces east) in that corner, its back to the room |
| 0x0B26 candelabra | 3461,2601,18 | - | was 3461,2602, the east window's floor tile |
| 0x11CA flowerpot | was 3460,2597,18 | - | removed: the north window's floor tile |
| 0x0E42 wooden chest | 3455,2598,18 | faces south, at the foot of the bed | was 3456,2597, the north window's floor tile |
| 0x0A9A bookcase | 3454,2599,18 | faces east, west wall (plain piece 3453,2599) | was 3454,2602, the west window's floor tile |

### Kept

| Piece | Where | Note |
|---|---|---|
| 0x11C9 potted tree | 3458,2595,15 | outside, west of the door's approach (3459,2595 stays clear) |
| 0x1E25 books, 0x1810 hourglass | 3458,2600,24 and 27 | on the desk (map table 0x0B83) |
| 0x2D61 inkwell, 0x2270 scroll | 3458,2601,24 | on the desk (map table 0x0B84) |
| 0x0A9A bookcase | 3458,2602,18 | faces east, office west wall (plain 0x0008 at 3457,2602) |
| 0x2272 scroll | 3454,2598,24 | on the quarters' table |
| map: bearskin rug, stretched hide 0x106B (3458,2597), desk and chair, bed, dresser, lantern; the ankh dais east of the house (P799's working ankh) | | not ours to move |

Window floor tiles, all eight, now hold no floor piece: 3456,2597; 3460,2597; 3454,2598 (map table only, scroll on top);
3461,2598; 3461,2602; 3456,2602; 3460,2602; 3454,2602.

## Main

### Changed by cc-P803

| Piece | Where (x,y,z) | Facing / wall | What changed |
|---|---|---|---|
| League requisitions board, art 0x1E5F | 3662,2548,0 | south face, on the north wall (plain 0x0034 at 3662,2547) | was 3662,2547,0 with art 0x1E5E: on the wall's own tile with the west-wall art; moved on load (same item) |
| 0x0B98 sign arm + 0x0BCF board "League of Extraordinary Citizens" | 3670,2563,0 | sticks out from the south wall, two tiles east of the arch | was 0x0B97 (lies along a wall) |
| 0x0A98 bookcase | 3660,2548,0 | faces south, north wall | was 0x0A99 (faces east) |
| 0x0A97 bookcase | 3661,2548,0 | faces south, north wall | was 0x0A9A (faces east) |
| 0x0A98 bookcase | 3670,2548,0 | faces south, north wall | was 0x0A9A (faces east) |

### Kept

| Piece | Where | Note |
|---|---|---|
| 0x11C9 potted tree | 3665,2563,0 | outside, west of the arch |
| 0x1E25 books, 0x2D61 inkwell, 0x2270 scroll, 0x1810 hourglass | 3661,2549,6 (hourglass 9) | on the map's counter 0x0B3F |
| 0x0B26 candelabra | 3659,2548,0 | north-west corner |
| 0x11CA flowerpot | 3663,2548,0 | north wall, beside the board |
| 0x0E42 wooden chest | 3672,2548,0 | faces south, north wall |
| 0x2272 scroll | 3672,2551,6 | on the long counter |
| the working ankh | 3676,2562-2563,0 | unchanged (cc-P678/P799) |

The hall's windows are the stained glass of the south wall (3661, 3662, 3664, 3665, 3670, 3673 at y 2562); none of
our pieces stands on their floor tiles (y 2561).
