# cc-P691 placed: Blackthorn Dungeon on the Fold

Two kinds of placement. **Map** pieces come from the map patch (`trammel.mapops`): EA's own Blackthorn layout copied
cell for cell from stock Trammel, nothing redrawn. **Server items** are placed by `[GenBlackthorn`
(`BlackthornDungeon/Generate.cs`); every spot is ServUO's, moved with `BlackthornFold.Move`.

## Map (trammel.mapops, facet 1; drawn on Trammel, Felucca and the Fold alike)

| Piece | Stock Trammel | Offset | Where now | Land cells | Statics |
|---|---|---|---|---|---|
| The dungeon proper with its north corridor and north-west cave | 6177-6471, 2557-2803 | +40, +1248 | 6217-6511, 3805-4051 | 22,689 | 7,764 |
| The invasion block: eight town rooms round a central cave | 6248-6490, 2315-2587 | +656, +1480 | 6904-7146, 3795-4067 | 65,950 | 24,852 |

Ids, Z and hues are EA's, unchanged; every static keeps its cell inside its 8 x 8 block (both offsets are multiples
of 8). Not copied: the filler block at stock 6176-6303, 2752-2847 (land 0x0245 only, no statics). Both boxes were void
with no statics on the SoS + patch file, with a block of margin round each; the isle's box (6594-6865, 3905-4049) is
83 tiles from the dungeon and 39 from the invasion block.

## Server items: the Fold (map 32)

| Item | Where (x,y,z) | Facing / variant | What |
|---|---|---|---|
| DungeonHitchingPost | 6468,3925,0 | | at the landing (ServUO 6428,2677) |
| MetalDoor | 6449,3943,0 | WestCCW | landing hall, south pair (ServUO 6409,2695) |
| MetalDoor | 6450,3943,0 | EastCW | landing hall, south pair (6410,2695) |
| MetalDoor | 6449,3912,0 | WestCW | landing hall, north pair (6409,2664) |
| MetalDoor | 6450,3912,0 | EastCCW | landing hall, north pair (6410,2664) |
| MetalDoor | 6434,3928,0 | SouthCW | landing hall, west pair (6394,2680) |
| MetalDoor | 6434,3927,0 | NorthCCW | landing hall, west pair (6394,2679) |
| MetalDoor | 6465,3927,0 | NorthCW | landing hall, east pair (6425,2679) |
| MetalDoor | 6465,3928,0 | SouthCCW | landing hall, east pair (6425,2680) |
| Blocker x 16 | 7091,3901-3905,-5; 7088-7090,3901,-5; 7098,3901-3905,-5; 7099-7101,3901,-5 | | the New Magincia room's north side (ServUO 6432-6445, 2421-2425) |
| Teleporter x 15 "Blackthorn: the cave, north" | 6396-6410,3836,0 | to 7012-7026,4065,0 (same x order) | the dungeon corridor's north end into the invasion block's cave |
| Teleporter x 15 "Blackthorn: the corridor, south" | 7012-7026,4067,0 | to 6396-6410,3837,0 | the cave's south row back to the corridor |
| Teleporter x 5 "Blackthorn: the stairs, up to the castle" | 6480,3925-3929,20 | to Trammel 1521,1437,15 | the top of the landing's east stairs (ServUO's way out, 6440,2677-2681,20) |
| Spawner x 22 "Spawner_Blackthorn" | ServUO's 22 Trammel rows + (40, 1248), e.g. hell hounds 6403,3927,0 | | the dungeon proper |

## Server items: Trammel (the author's Blackthorn Castle, keep's south-west storeroom x 1513-1521, y 1432-1438)

| Item | Where (x,y,z) | Facing / variant | What |
|---|---|---|---|
| 0x3E65 Static "a cellar hatch" | 1519,1437,14 | | one below the floor (Z 15), its top (17) one step up |
| Teleporter "Blackthorn: the cellar hatch, down" | 1519,1437,17 | to the Fold 6472,3927,0 | on the hatch; lands at the foot of the landing's east stairs (ServUO 6432,2679) |
| Spawner "AgentOfTheCrown" | 1521,1434,15 | | the Agent of the Crown, the Minax turn-in (ServUO's stood at 1488,1473, the moat on SoS) |

Not placed any more: ServUO's Felucca copy (its 22 spawners, hitching post, doors, blockers, nine castle teleporters)
and its nine Felucca city Agents.
