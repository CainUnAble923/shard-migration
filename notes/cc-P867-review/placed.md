# cc-P867 placed list: P855's decor addons (fix-up of P864's review)

Nothing here is placed in the world by a seeder: every piece is a house addon a player places from a deed (or staff
with `[DecorAddon place`). Part 1 is one line per design file (P864 item 1). Part 2 is every piece the trainee
placed in the staged house (P864 items 2 and 3): item ID, location x,y,z, the design it belongs to and the wall.
No piece of any design was turned; a facing is a whole file.

## 1. The 30 designs (server/data/Decoration/Addons/*.cfg)

| File | Pieces | Facing | Where it stands in a house | Note |
|---|---|---|---|---|
| barbecue-east | 3 | east | free-standing grill (outdoor or a kitchen), cook side to the east |  |
| barbecue-south | 3 | south | free-standing grill (outdoor or a kitchen), cook side to the south |  |
| blue-couch-east | 17 | east | faces east; its back against a **west** wall |  |
| blue-couch-north | 17 | north | faces north; its back against a **south** wall (the camera-side wall) |  |
| blue-couch-south | 17 | south | faces south; its back against a **north** wall |  |
| blue-couch-west | 17 | west | faces west; its back against an **east** wall (the camera-side wall: the client draws that wall over it) |  |
| buffet-table-east-west | 10 | east-west | free-standing; the table's long side runs east-west |  |
| buffet-table-north-south | 10 | north-south | free-standing; the table's long side runs north-south |  |
| country-kitchen-east | 11 | east | faces east; its back against a **west** wall |  |
| country-kitchen-south | 12 | south | faces south; its back against a **north** wall |  |
| feasting-table-1 | 23 | style 1 | free-standing, style 1 |  |
| feasting-table-2 | 23 | style 2 | free-standing, style 2 |  |
| feasting-table-3 | 22 | style 3 | free-standing, style 3 |  |
| formal-dining-table-east-west | 12 | east-west | free-standing; the table's long side runs east-west |  |
| formal-dining-table-north-south | 12 | north-south | free-standing; the table's long side runs north-south |  |
| grey-fireplace-grand-east | 50 | east | faces east; its back against a **west** wall |  |
| grey-fireplace-grand-south | 50 | south | faces south; its back against a **north** wall |  |
| grey-fireplace-large-east | 55 | east | faces east; its back against a **west** wall |  |
| grey-fireplace-large-south | 55 | south | faces south; its back against a **north** wall |  |
| grey-fireplace-low-east | 25 | east | faces east; its back against a **west** wall |  |
| grey-fireplace-low-south | 25 | south | faces south; its back against a **north** wall |  |
| grey-fireplace-medium-east | 40 | east | faces east; its back against a **west** wall |  |
| grey-fireplace-medium-south | 41 | south | faces south; its back against a **north** wall |  |
| grey-fireplace-small-east | 20 | east | faces east; its back against a **west** wall |  |
| grey-fireplace-small-south | 20 | south | faces south; its back against a **north** wall |  |
| harpsichord-east | 7 | east | faces east; its back against a **west** wall | facing chosen by the converter from the art's name (tiledata "Harpsichord EAST", the download's file pianomodern2 names none); the render and shot agree: keyboard on its east side, bench east of it |
| harpsichord-south | 7 | south | faces south; its back against a **north** wall | facing chosen by the converter from the art's name (tiledata "Harpsichord SOUTH", file pianomodern); the render and shot agree: keyboard on its south side, bench south of it |
| holiday-fireplace | 28 | south | faces south; its back against a **north** wall | cc-P867: the download's own fieldstone wall box (post 0x001D, four 0x001C, two 0x001B) left out, so the hearth's stone surround stands against the house's own north wall (P864 item 3) |
| small-kitchen-northwest | 5 | northwest | an L counter in a room's **north-west corner**, against the north and west walls |  |
| small-kitchen-southeast | 5 | southeast | an L counter in a room's **south-east corner**, against the south and east walls (camera side) |  |

642 pieces in 30 files (P855 had 649: the holiday fireplace lost its 7 wall pieces).

## 2. Against real walls in main's New Haven (the shots)

Each wall-backed design stood by staff (`[DecorAddon place`, no house rules) inside a New Haven building on main
(SoS Trammel), at the spot `notes/cc-P867-tools/town867.py` found: every tile on the building's floor at one Z,
reached on foot, not protected (doors, NPC posts, spawners, seeded rows), nothing with height standing on it; the
back row against a full plain wall at that floor (no window); no tile in front of a window. The trainee stood
south-east of it in the same room for the shot (`shots/p867-<design>.jpg`, the default camera, roof hidden
inside); `town-<design>.jpg` is the isorender of the same spot (roofs cut). Staff cleared each before the next.
No piece was turned.


### grey-fireplace-small-east (faces east): faces east; against the building's west wall

- 0x0519, 3625,2572,0, grey-fireplace-small-east
- 0x0519, 3624,2573,0, grey-fireplace-small-east
- 0x0519, 3625,2573,0, grey-fireplace-small-east
- 0x0519, 3624,2575,0, grey-fireplace-small-east
- 0x0519, 3624,2572,0, grey-fireplace-small-east
- 0x0519, 3625,2575,0, grey-fireplace-small-east
- 0x0519, 3625,2574,0, grey-fireplace-small-east
- 0x0519, 3624,2574,0, grey-fireplace-small-east
- 0x071E, 3624,2572,5, grey-fireplace-small-east
- 0x071E, 3624,2572,0, grey-fireplace-small-east
- 0x071E, 3624,2575,5, grey-fireplace-small-east
- 0x071E, 3624,2575,0, grey-fireplace-small-east
- 0x07CD, 3624,2575,10, grey-fireplace-small-east
- 0x07CD, 3624,2574,10, grey-fireplace-small-east
- 0x07CD, 3624,2573,10, grey-fireplace-small-east
- 0x07CD, 3624,2572,10, grey-fireplace-small-east
- 0x0DE3, 3624,2574,0, grey-fireplace-small-east
- 0x0DE3, 3624,2574,4, grey-fireplace-small-east
- 0x0DE3, 3624,2573,0, grey-fireplace-small-east
- 0x0DE3, 3624,2573,4, grey-fireplace-small-east

### grey-fireplace-small-south (faces south): faces south; against the building's north wall

- 0x071E, 3622,2610,5, grey-fireplace-small-south
- 0x071E, 3622,2610,0, grey-fireplace-small-south
- 0x071E, 3619,2610,5, grey-fireplace-small-south
- 0x071E, 3619,2610,0, grey-fireplace-small-south
- 0x0519, 3622,2611,0, grey-fireplace-small-south
- 0x0519, 3621,2610,0, grey-fireplace-small-south
- 0x0519, 3621,2611,0, grey-fireplace-small-south
- 0x0519, 3622,2610,0, grey-fireplace-small-south
- 0x0519, 3620,2611,0, grey-fireplace-small-south
- 0x0519, 3619,2610,0, grey-fireplace-small-south
- 0x0519, 3620,2610,0, grey-fireplace-small-south
- 0x0519, 3619,2611,0, grey-fireplace-small-south
- 0x07C9, 3622,2610,10, grey-fireplace-small-south
- 0x07C9, 3621,2610,10, grey-fireplace-small-south
- 0x07C9, 3620,2610,10, grey-fireplace-small-south
- 0x07C9, 3619,2610,10, grey-fireplace-small-south
- 0x0DE3, 3621,2610,0, grey-fireplace-small-south
- 0x0DE3, 3621,2610,4, grey-fireplace-small-south
- 0x0DE3, 3620,2610,0, grey-fireplace-small-south
- 0x0DE3, 3620,2610,4, grey-fireplace-small-south

### grey-fireplace-low-east (faces east): faces east; against the building's west wall

- 0x071E, 3624,2574,0, grey-fireplace-low-east
- 0x071E, 3624,2570,0, grey-fireplace-low-east
- 0x071E, 3624,2570,5, grey-fireplace-low-east
- 0x071E, 3624,2574,5, grey-fireplace-low-east
- 0x07CD, 3624,2570,10, grey-fireplace-low-east
- 0x07CD, 3624,2571,10, grey-fireplace-low-east
- 0x07CD, 3624,2572,10, grey-fireplace-low-east
- 0x07CD, 3624,2573,10, grey-fireplace-low-east
- 0x07CD, 3624,2574,10, grey-fireplace-low-east
- 0x0519, 3625,2573,0, grey-fireplace-low-east
- 0x0519, 3625,2572,0, grey-fireplace-low-east
- 0x0519, 3625,2571,0, grey-fireplace-low-east
- 0x0519, 3625,2574,0, grey-fireplace-low-east
- 0x0519, 3625,2570,0, grey-fireplace-low-east
- 0x0519, 3624,2574,0, grey-fireplace-low-east
- 0x0519, 3624,2573,0, grey-fireplace-low-east
- 0x0519, 3624,2572,0, grey-fireplace-low-east
- 0x0519, 3624,2570,0, grey-fireplace-low-east
- 0x0519, 3624,2571,0, grey-fireplace-low-east
- 0x0DE3, 3624,2573,0, grey-fireplace-low-east
- 0x0DE3, 3624,2573,4, grey-fireplace-low-east
- 0x0DE3, 3624,2572,0, grey-fireplace-low-east
- 0x0DE3, 3624,2572,4, grey-fireplace-low-east
- 0x0DE3, 3624,2571,0, grey-fireplace-low-east
- 0x0DE3, 3624,2571,4, grey-fireplace-low-east

### grey-fireplace-low-south (faces south): faces south; against the building's north wall

- 0x07C9, 3585,2583,10, grey-fireplace-low-south
- 0x07C9, 3581,2583,10, grey-fireplace-low-south
- 0x07C9, 3582,2583,10, grey-fireplace-low-south
- 0x07C9, 3583,2583,10, grey-fireplace-low-south
- 0x07C9, 3584,2583,10, grey-fireplace-low-south
- 0x071E, 3585,2583,5, grey-fireplace-low-south
- 0x071E, 3585,2583,0, grey-fireplace-low-south
- 0x071E, 3581,2583,5, grey-fireplace-low-south
- 0x071E, 3581,2583,0, grey-fireplace-low-south
- 0x0519, 3581,2584,0, grey-fireplace-low-south
- 0x0519, 3585,2583,0, grey-fireplace-low-south
- 0x0519, 3585,2584,0, grey-fireplace-low-south
- 0x0519, 3581,2583,0, grey-fireplace-low-south
- 0x0519, 3582,2583,0, grey-fireplace-low-south
- 0x0519, 3582,2584,0, grey-fireplace-low-south
- 0x0519, 3584,2583,0, grey-fireplace-low-south
- 0x0519, 3584,2584,0, grey-fireplace-low-south
- 0x0519, 3583,2583,0, grey-fireplace-low-south
- 0x0519, 3583,2584,0, grey-fireplace-low-south
- 0x0DE3, 3584,2583,0, grey-fireplace-low-south
- 0x0DE3, 3584,2583,4, grey-fireplace-low-south
- 0x0DE3, 3583,2583,0, grey-fireplace-low-south
- 0x0DE3, 3583,2583,4, grey-fireplace-low-south
- 0x0DE3, 3582,2583,0, grey-fireplace-low-south
- 0x0DE3, 3582,2583,4, grey-fireplace-low-south

### grey-fireplace-medium-east (faces east): faces east; against the building's west wall

- 0x071E, 3624,2574,5, grey-fireplace-medium-east
- 0x071E, 3624,2571,0, grey-fireplace-medium-east
- 0x071E, 3625,2571,0, grey-fireplace-medium-east
- 0x071E, 3624,2572,0, grey-fireplace-medium-east
- 0x071E, 3624,2573,0, grey-fireplace-medium-east
- 0x071E, 3624,2574,0, grey-fireplace-medium-east
- 0x071E, 3625,2574,0, grey-fireplace-medium-east
- 0x071E, 3624,2571,5, grey-fireplace-medium-east
- 0x071E, 3624,2572,5, grey-fireplace-medium-east
- 0x071E, 3624,2573,5, grey-fireplace-medium-east
- 0x071E, 3625,2571,5, grey-fireplace-medium-east
- 0x071E, 3624,2571,11, grey-fireplace-medium-east
- 0x071E, 3624,2572,11, grey-fireplace-medium-east
- 0x071E, 3624,2574,11, grey-fireplace-medium-east
- 0x071E, 3624,2573,11, grey-fireplace-medium-east
- 0x071E, 3625,2574,5, grey-fireplace-medium-east
- 0x0519, 3624,2571,0, grey-fireplace-medium-east
- 0x0519, 3624,2572,0, grey-fireplace-medium-east
- 0x0519, 3624,2573,0, grey-fireplace-medium-east
- 0x0519, 3624,2574,0, grey-fireplace-medium-east
- 0x0519, 3625,2571,0, grey-fireplace-medium-east
- 0x0519, 3625,2572,0, grey-fireplace-medium-east
- 0x0519, 3625,2573,0, grey-fireplace-medium-east
- 0x0519, 3625,2574,0, grey-fireplace-medium-east
- 0x0519, 3626,2571,0, grey-fireplace-medium-east
- 0x0519, 3626,2572,0, grey-fireplace-medium-east
- 0x0519, 3626,2573,0, grey-fireplace-medium-east
- 0x0519, 3626,2574,0, grey-fireplace-medium-east
- 0x07CD, 3624,2571,10, grey-fireplace-medium-east
- 0x07CD, 3625,2574,10, grey-fireplace-medium-east
- 0x07CD, 3625,2573,10, grey-fireplace-medium-east
- 0x07CD, 3624,2572,10, grey-fireplace-medium-east
- 0x07CD, 3624,2573,10, grey-fireplace-medium-east
- 0x07CD, 3624,2574,10, grey-fireplace-medium-east
- 0x07CD, 3625,2571,10, grey-fireplace-medium-east
- 0x07CD, 3625,2572,10, grey-fireplace-medium-east
- 0x0DE3, 3625,2573,0, grey-fireplace-medium-east
- 0x0DE3, 3625,2573,4, grey-fireplace-medium-east
- 0x0DE3, 3625,2572,0, grey-fireplace-medium-east
- 0x0DE3, 3625,2572,4, grey-fireplace-medium-east

### grey-fireplace-medium-south (faces south): faces south; against the building's north wall

- 0x071E, 3618,2610,11, grey-fireplace-medium-south
- 0x071E, 3621,2610,11, grey-fireplace-medium-south
- 0x071E, 3620,2610,11, grey-fireplace-medium-south
- 0x071E, 3619,2610,11, grey-fireplace-medium-south
- 0x071E, 3619,2610,5, grey-fireplace-medium-south
- 0x071E, 3619,2610,0, grey-fireplace-medium-south
- 0x071E, 3618,2610,5, grey-fireplace-medium-south
- 0x071E, 3618,2610,0, grey-fireplace-medium-south
- 0x071E, 3621,2611,5, grey-fireplace-medium-south
- 0x071E, 3621,2611,0, grey-fireplace-medium-south
- 0x071E, 3621,2610,5, grey-fireplace-medium-south
- 0x071E, 3621,2610,0, grey-fireplace-medium-south
- 0x071E, 3618,2611,5, grey-fireplace-medium-south
- 0x071E, 3618,2611,0, grey-fireplace-medium-south
- 0x071E, 3620,2610,0, grey-fireplace-medium-south
- 0x071E, 3620,2610,5, grey-fireplace-medium-south
- 0x07C9, 3619,2611,10, grey-fireplace-medium-south
- 0x07C9, 3618,2611,10, grey-fireplace-medium-south
- 0x07C9, 3620,2611,10, grey-fireplace-medium-south
- 0x07C9, 3621,2611,10, grey-fireplace-medium-south
- 0x07C9, 3621,2610,10, grey-fireplace-medium-south
- 0x07C9, 3619,2610,10, grey-fireplace-medium-south
- 0x07C9, 3620,2610,10, grey-fireplace-medium-south
- 0x07C9, 3618,2610,10, grey-fireplace-medium-south
- 0x0519, 3619,2610,0, grey-fireplace-medium-south
- 0x0519, 3620,2610,0, grey-fireplace-medium-south
- 0x0519, 3621,2610,0, grey-fireplace-medium-south
- 0x0519, 3621,2610,0, grey-fireplace-medium-south
- 0x0519, 3618,2611,0, grey-fireplace-medium-south
- 0x0519, 3618,2612,0, grey-fireplace-medium-south
- 0x0519, 3619,2612,0, grey-fireplace-medium-south
- 0x0519, 3620,2612,0, grey-fireplace-medium-south
- 0x0519, 3621,2612,0, grey-fireplace-medium-south
- 0x0519, 3619,2611,0, grey-fireplace-medium-south
- 0x0519, 3620,2611,0, grey-fireplace-medium-south
- 0x0519, 3621,2611,0, grey-fireplace-medium-south
- 0x0519, 3618,2610,0, grey-fireplace-medium-south
- 0x0DE3, 3620,2611,0, grey-fireplace-medium-south
- 0x0DE3, 3620,2611,4, grey-fireplace-medium-south
- 0x0DE3, 3619,2611,0, grey-fireplace-medium-south
- 0x0DE3, 3619,2611,4, grey-fireplace-medium-south

### grey-fireplace-large-east (faces east): faces east; against the building's west wall

- 0x0519, 3626,2574,0, grey-fireplace-large-east
- 0x0519, 3626,2570,0, grey-fireplace-large-east
- 0x0519, 3626,2573,0, grey-fireplace-large-east
- 0x0519, 3626,2572,0, grey-fireplace-large-east
- 0x0519, 3626,2571,0, grey-fireplace-large-east
- 0x0519, 3625,2574,0, grey-fireplace-large-east
- 0x0519, 3624,2574,0, grey-fireplace-large-east
- 0x0519, 3624,2570,0, grey-fireplace-large-east
- 0x0519, 3625,2572,0, grey-fireplace-large-east
- 0x0519, 3625,2571,0, grey-fireplace-large-east
- 0x0519, 3625,2570,0, grey-fireplace-large-east
- 0x0519, 3625,2573,0, grey-fireplace-large-east
- 0x0519, 3624,2572,0, grey-fireplace-large-east
- 0x0519, 3624,2573,0, grey-fireplace-large-east
- 0x0519, 3624,2571,0, grey-fireplace-large-east
- 0x071E, 3624,2574,5, grey-fireplace-large-east
- 0x071E, 3625,2574,0, grey-fireplace-large-east
- 0x071E, 3624,2574,0, grey-fireplace-large-east
- 0x071E, 3625,2574,5, grey-fireplace-large-east
- 0x071E, 3625,2574,10, grey-fireplace-large-east
- 0x071E, 3624,2574,10, grey-fireplace-large-east
- 0x071E, 3624,2571,5, grey-fireplace-large-east
- 0x071E, 3624,2570,0, grey-fireplace-large-east
- 0x071E, 3624,2572,5, grey-fireplace-large-east
- 0x071E, 3624,2573,5, grey-fireplace-large-east
- 0x071E, 3624,2573,0, grey-fireplace-large-east
- 0x071E, 3624,2572,0, grey-fireplace-large-east
- 0x071E, 3624,2571,0, grey-fireplace-large-east
- 0x071E, 3624,2570,5, grey-fireplace-large-east
- 0x071E, 3625,2570,0, grey-fireplace-large-east
- 0x071E, 3625,2572,10, grey-fireplace-large-east
- 0x071E, 3625,2573,10, grey-fireplace-large-east
- 0x071E, 3625,2571,10, grey-fireplace-large-east
- 0x071E, 3625,2570,10, grey-fireplace-large-east
- 0x071E, 3624,2570,10, grey-fireplace-large-east
- 0x071E, 3625,2570,5, grey-fireplace-large-east
- 0x071E, 3624,2571,10, grey-fireplace-large-east
- 0x071E, 3624,2572,10, grey-fireplace-large-east
- 0x071E, 3624,2573,10, grey-fireplace-large-east
- 0x07CD, 3624,2574,15, grey-fireplace-large-east
- 0x07CD, 3625,2574,15, grey-fireplace-large-east
- 0x07CD, 3624,2573,15, grey-fireplace-large-east
- 0x07CD, 3624,2571,15, grey-fireplace-large-east
- 0x07CD, 3624,2572,15, grey-fireplace-large-east
- 0x07CD, 3625,2570,15, grey-fireplace-large-east
- 0x07CD, 3625,2571,15, grey-fireplace-large-east
- 0x07CD, 3624,2570,15, grey-fireplace-large-east
- 0x07CD, 3625,2572,15, grey-fireplace-large-east
- 0x07CD, 3625,2573,15, grey-fireplace-large-east
- 0x0DE3, 3625,2573,0, grey-fireplace-large-east
- 0x0DE3, 3625,2573,4, grey-fireplace-large-east
- 0x0DE3, 3625,2572,0, grey-fireplace-large-east
- 0x0DE3, 3625,2572,4, grey-fireplace-large-east
- 0x0DE3, 3625,2571,0, grey-fireplace-large-east
- 0x0DE3, 3625,2571,4, grey-fireplace-large-east

### grey-fireplace-large-south (faces south): faces south; against the building's north wall

- 0x07C9, 3585,2584,15, grey-fireplace-large-south
- 0x07C9, 3584,2584,15, grey-fireplace-large-south
- 0x07C9, 3585,2583,15, grey-fireplace-large-south
- 0x07C9, 3584,2583,15, grey-fireplace-large-south
- 0x07C9, 3583,2584,15, grey-fireplace-large-south
- 0x07C9, 3583,2583,15, grey-fireplace-large-south
- 0x07C9, 3582,2584,15, grey-fireplace-large-south
- 0x07C9, 3581,2583,15, grey-fireplace-large-south
- 0x07C9, 3581,2584,15, grey-fireplace-large-south
- 0x07C9, 3582,2583,15, grey-fireplace-large-south
- 0x071E, 3585,2583,10, grey-fireplace-large-south
- 0x071E, 3584,2583,10, grey-fireplace-large-south
- 0x071E, 3583,2583,10, grey-fireplace-large-south
- 0x071E, 3582,2583,10, grey-fireplace-large-south
- 0x071E, 3585,2584,10, grey-fireplace-large-south
- 0x071E, 3584,2584,10, grey-fireplace-large-south
- 0x071E, 3583,2584,10, grey-fireplace-large-south
- 0x071E, 3581,2583,0, grey-fireplace-large-south
- 0x071E, 3581,2583,5, grey-fireplace-large-south
- 0x071E, 3581,2583,10, grey-fireplace-large-south
- 0x071E, 3585,2584,5, grey-fireplace-large-south
- 0x071E, 3585,2583,5, grey-fireplace-large-south
- 0x071E, 3581,2584,0, grey-fireplace-large-south
- 0x071E, 3581,2584,5, grey-fireplace-large-south
- 0x071E, 3582,2583,0, grey-fireplace-large-south
- 0x071E, 3582,2583,5, grey-fireplace-large-south
- 0x071E, 3583,2583,0, grey-fireplace-large-south
- 0x071E, 3583,2583,5, grey-fireplace-large-south
- 0x071E, 3584,2583,0, grey-fireplace-large-south
- 0x071E, 3584,2583,5, grey-fireplace-large-south
- 0x071E, 3585,2583,0, grey-fireplace-large-south
- 0x071E, 3585,2584,0, grey-fireplace-large-south
- 0x071E, 3581,2584,10, grey-fireplace-large-south
- 0x071E, 3582,2584,10, grey-fireplace-large-south
- 0x0519, 3585,2584,0, grey-fireplace-large-south
- 0x0519, 3582,2584,0, grey-fireplace-large-south
- 0x0519, 3582,2583,0, grey-fireplace-large-south
- 0x0519, 3581,2584,0, grey-fireplace-large-south
- 0x0519, 3581,2583,0, grey-fireplace-large-south
- 0x0519, 3582,2585,0, grey-fireplace-large-south
- 0x0519, 3581,2585,0, grey-fireplace-large-south
- 0x0519, 3583,2585,0, grey-fireplace-large-south
- 0x0519, 3584,2585,0, grey-fireplace-large-south
- 0x0519, 3585,2585,0, grey-fireplace-large-south
- 0x0519, 3583,2583,0, grey-fireplace-large-south
- 0x0519, 3584,2583,0, grey-fireplace-large-south
- 0x0519, 3583,2584,0, grey-fireplace-large-south
- 0x0519, 3584,2584,0, grey-fireplace-large-south
- 0x0519, 3585,2583,0, grey-fireplace-large-south
- 0x0DE3, 3584,2584,0, grey-fireplace-large-south
- 0x0DE3, 3584,2584,4, grey-fireplace-large-south
- 0x0DE3, 3583,2584,0, grey-fireplace-large-south
- 0x0DE3, 3583,2584,4, grey-fireplace-large-south
- 0x0DE3, 3582,2584,0, grey-fireplace-large-south
- 0x0DE3, 3582,2584,4, grey-fireplace-large-south

### grey-fireplace-grand-east (faces east): faces east; against the building's west wall

- 0x0519, 3626,2574,0, grey-fireplace-grand-east
- 0x0519, 3626,2570,0, grey-fireplace-grand-east
- 0x0519, 3626,2573,0, grey-fireplace-grand-east
- 0x0519, 3626,2572,0, grey-fireplace-grand-east
- 0x0519, 3626,2571,0, grey-fireplace-grand-east
- 0x0519, 3625,2574,0, grey-fireplace-grand-east
- 0x0519, 3624,2574,0, grey-fireplace-grand-east
- 0x0519, 3624,2570,0, grey-fireplace-grand-east
- 0x0519, 3625,2572,0, grey-fireplace-grand-east
- 0x0519, 3625,2571,0, grey-fireplace-grand-east
- 0x0519, 3625,2570,0, grey-fireplace-grand-east
- 0x0519, 3625,2573,0, grey-fireplace-grand-east
- 0x0519, 3624,2572,0, grey-fireplace-grand-east
- 0x0519, 3624,2573,0, grey-fireplace-grand-east
- 0x0519, 3624,2571,0, grey-fireplace-grand-east
- 0x071E, 3624,2574,11, grey-fireplace-grand-east
- 0x071E, 3624,2574,5, grey-fireplace-grand-east
- 0x071E, 3625,2574,0, grey-fireplace-grand-east
- 0x071E, 3624,2574,0, grey-fireplace-grand-east
- 0x071E, 3625,2574,5, grey-fireplace-grand-east
- 0x071E, 3624,2573,11, grey-fireplace-grand-east
- 0x071E, 3624,2572,11, grey-fireplace-grand-east
- 0x071E, 3624,2571,11, grey-fireplace-grand-east
- 0x071E, 3624,2570,11, grey-fireplace-grand-east
- 0x071E, 3624,2571,5, grey-fireplace-grand-east
- 0x071E, 3624,2570,0, grey-fireplace-grand-east
- 0x071E, 3624,2572,5, grey-fireplace-grand-east
- 0x071E, 3624,2573,5, grey-fireplace-grand-east
- 0x071E, 3624,2573,0, grey-fireplace-grand-east
- 0x071E, 3624,2572,0, grey-fireplace-grand-east
- 0x071E, 3624,2571,0, grey-fireplace-grand-east
- 0x071E, 3624,2570,5, grey-fireplace-grand-east
- 0x071E, 3625,2570,0, grey-fireplace-grand-east
- 0x071E, 3625,2570,5, grey-fireplace-grand-east
- 0x07CD, 3625,2574,10, grey-fireplace-grand-east
- 0x07CD, 3624,2574,10, grey-fireplace-grand-east
- 0x07CD, 3625,2573,10, grey-fireplace-grand-east
- 0x07CD, 3625,2572,10, grey-fireplace-grand-east
- 0x07CD, 3625,2571,10, grey-fireplace-grand-east
- 0x07CD, 3625,2570,10, grey-fireplace-grand-east
- 0x07CD, 3624,2573,10, grey-fireplace-grand-east
- 0x07CD, 3624,2572,10, grey-fireplace-grand-east
- 0x07CD, 3624,2571,10, grey-fireplace-grand-east
- 0x07CD, 3624,2570,10, grey-fireplace-grand-east
- 0x0DE3, 3625,2573,0, grey-fireplace-grand-east
- 0x0DE3, 3625,2573,4, grey-fireplace-grand-east
- 0x0DE3, 3625,2572,0, grey-fireplace-grand-east
- 0x0DE3, 3625,2572,4, grey-fireplace-grand-east
- 0x0DE3, 3625,2571,0, grey-fireplace-grand-east
- 0x0DE3, 3625,2571,4, grey-fireplace-grand-east

### grey-fireplace-grand-south (faces south): faces south; against the building's north wall

- 0x071E, 3585,2583,11, grey-fireplace-grand-south
- 0x071E, 3584,2583,11, grey-fireplace-grand-south
- 0x071E, 3583,2583,11, grey-fireplace-grand-south
- 0x071E, 3582,2583,11, grey-fireplace-grand-south
- 0x071E, 3581,2583,11, grey-fireplace-grand-south
- 0x071E, 3581,2583,0, grey-fireplace-grand-south
- 0x071E, 3581,2583,5, grey-fireplace-grand-south
- 0x071E, 3585,2584,5, grey-fireplace-grand-south
- 0x071E, 3585,2583,5, grey-fireplace-grand-south
- 0x071E, 3581,2584,0, grey-fireplace-grand-south
- 0x071E, 3581,2584,5, grey-fireplace-grand-south
- 0x071E, 3582,2583,0, grey-fireplace-grand-south
- 0x071E, 3582,2583,5, grey-fireplace-grand-south
- 0x071E, 3583,2583,0, grey-fireplace-grand-south
- 0x071E, 3583,2583,5, grey-fireplace-grand-south
- 0x071E, 3584,2583,0, grey-fireplace-grand-south
- 0x071E, 3584,2583,5, grey-fireplace-grand-south
- 0x071E, 3585,2583,0, grey-fireplace-grand-south
- 0x071E, 3585,2584,0, grey-fireplace-grand-south
- 0x07C9, 3585,2584,10, grey-fireplace-grand-south
- 0x07C9, 3584,2584,10, grey-fireplace-grand-south
- 0x07C9, 3582,2584,10, grey-fireplace-grand-south
- 0x07C9, 3583,2584,10, grey-fireplace-grand-south
- 0x07C9, 3581,2584,10, grey-fireplace-grand-south
- 0x07C9, 3585,2583,10, grey-fireplace-grand-south
- 0x07C9, 3584,2583,10, grey-fireplace-grand-south
- 0x07C9, 3583,2583,10, grey-fireplace-grand-south
- 0x07C9, 3581,2583,10, grey-fireplace-grand-south
- 0x07C9, 3582,2583,10, grey-fireplace-grand-south
- 0x0519, 3585,2584,0, grey-fireplace-grand-south
- 0x0519, 3582,2584,0, grey-fireplace-grand-south
- 0x0519, 3582,2583,0, grey-fireplace-grand-south
- 0x0519, 3581,2584,0, grey-fireplace-grand-south
- 0x0519, 3581,2583,0, grey-fireplace-grand-south
- 0x0519, 3582,2585,0, grey-fireplace-grand-south
- 0x0519, 3581,2585,0, grey-fireplace-grand-south
- 0x0519, 3583,2585,0, grey-fireplace-grand-south
- 0x0519, 3584,2585,0, grey-fireplace-grand-south
- 0x0519, 3585,2585,0, grey-fireplace-grand-south
- 0x0519, 3583,2583,0, grey-fireplace-grand-south
- 0x0519, 3584,2583,0, grey-fireplace-grand-south
- 0x0519, 3583,2584,0, grey-fireplace-grand-south
- 0x0519, 3584,2584,0, grey-fireplace-grand-south
- 0x0519, 3585,2583,0, grey-fireplace-grand-south
- 0x0DE3, 3584,2584,0, grey-fireplace-grand-south
- 0x0DE3, 3584,2584,4, grey-fireplace-grand-south
- 0x0DE3, 3583,2584,0, grey-fireplace-grand-south
- 0x0DE3, 3583,2584,4, grey-fireplace-grand-south
- 0x0DE3, 3582,2584,0, grey-fireplace-grand-south
- 0x0DE3, 3582,2584,4, grey-fireplace-grand-south

### country-kitchen-east (faces east): faces east; against the building's west wall

- 0xA2A1, 3624,2570,2, country-kitchen-east
- 0x9A17, 3625,2573,2, country-kitchen-east
- 0x9A19, 3625,2570,2, country-kitchen-east
- 0x99C9, 3625,2571,2, country-kitchen-east
- 0x99C9, 3625,2572,2, country-kitchen-east
- 0x9D30, 3625,2572,11, country-kitchen-east
- 0xA2A2, 3624,2573,0, country-kitchen-east
- 0xA29D, 3624,2571,2, country-kitchen-east
- 0xA2A5, 3625,2574,2, country-kitchen-east
- 0x19AB, 3624,2571,6, country-kitchen-east
- 0xA269, 3624,2572,5, country-kitchen-east

### country-kitchen-south (faces south): faces south; against the building's north wall

- 0xA2A0, 3584,2583,0, country-kitchen-south
- 0xA29C, 3581,2583,1, country-kitchen-south
- 0xA29F, 3582,2583,1, country-kitchen-south
- 0x99C8, 3584,2584,2, country-kitchen-south
- 0x99C8, 3583,2584,2, country-kitchen-south
- 0x99C8, 3582,2584,2, country-kitchen-south
- 0x9A18, 3581,2584,2, country-kitchen-south
- 0x9D33, 3584,2584,11, country-kitchen-south
- 0x9D31, 3583,2584,11, country-kitchen-south
- 0xA2A9, 3585,2584,2, country-kitchen-south
- 0xA26D, 3583,2583,4, country-kitchen-south
- 0x19AB, 3582,2583,4, country-kitchen-south

### small-kitchen-northwest (faces northwest): an L counter in a room's north-west corner, against the north and west walls

- 0x99C8, 3668,2592,0, small-kitchen-northwest
- 0x99C8, 3668,2593,0, small-kitchen-northwest
- 0x99C8, 3668,2594,0, small-kitchen-northwest
- 0x9A15, 3666,2594,0, small-kitchen-northwest
- 0x99CB, 3667,2594,0, small-kitchen-northwest

### small-kitchen-southeast (faces southeast): an L counter in a room's south-east corner, against the south and east walls (camera side)

- 0x9A19, 3609,2579,0, small-kitchen-southeast
- 0x9A17, 3609,2578,0, small-kitchen-southeast
- 0x99C9, 3610,2577,0, small-kitchen-southeast
- 0x99C9, 3609,2577,0, small-kitchen-southeast
- 0x99C9, 3611,2577,0, small-kitchen-southeast

### harpsichord-east (faces east): faces east; against the building's west wall

- 0x63C9, 3624,2573,0, harpsichord-east
- 0x63C8, 3625,2573,0, harpsichord-east
- 0x63C7, 3625,2574,0, harpsichord-east
- 0x63C6, 3626,2573,0, harpsichord-east
- 0x63C5, 3626,2574,0, harpsichord-east
- 0x63C4, 3627,2574,0, harpsichord-east
- 0x63C3, 3627,2573,0, harpsichord-east

### harpsichord-south (faces south): faces south; against the building's north wall

- 0x63BC, 3621,2612,0, harpsichord-south
- 0x63BD, 3620,2612,0, harpsichord-south
- 0x63C2, 3621,2610,0, harpsichord-south
- 0x63C1, 3621,2610,0, harpsichord-south
- 0x63C0, 3620,2610,0, harpsichord-south
- 0x63BF, 3621,2611,0, harpsichord-south
- 0x63BE, 3620,2611,0, harpsichord-south

### blue-couch-east (faces east): faces east; against the building's west wall

- 0x13A5, 3625,2570,5, blue-couch-east
- 0x13A5, 3625,2574,5, blue-couch-east
- 0x163B, 3624,2571,5, blue-couch-east
- 0x163B, 3624,2573,5, blue-couch-east
- 0x163C, 3624,2572,5, blue-couch-east
- 0x13A4, 3624,2574,5, blue-couch-east
- 0x13A4, 3624,2570,5, blue-couch-east
- 0x0B2C, 3625,2573,0, blue-couch-east
- 0x0B2C, 3625,2572,0, blue-couch-east
- 0x0B2C, 3625,2571,0, blue-couch-east
- 0x0738, 3625,2574,0, blue-couch-east
- 0x0738, 3624,2574,0, blue-couch-east
- 0x0738, 3625,2570,0, blue-couch-east
- 0x0738, 3624,2570,0, blue-couch-east
- 0x0738, 3624,2571,0, blue-couch-east
- 0x0738, 3624,2573,0, blue-couch-east
- 0x0738, 3624,2572,0, blue-couch-east

### blue-couch-south (faces south): faces south; against the building's north wall

- 0x13A5, 3585,2583,5, blue-couch-south
- 0x13A5, 3581,2583,5, blue-couch-south
- 0x13A4, 3585,2584,5, blue-couch-south
- 0x13A4, 3581,2584,5, blue-couch-south
- 0x163C, 3583,2583,5, blue-couch-south
- 0x163B, 3584,2583,5, blue-couch-south
- 0x163B, 3582,2583,5, blue-couch-south
- 0x0B2D, 3584,2584,0, blue-couch-south
- 0x0B2D, 3583,2584,0, blue-couch-south
- 0x0B2D, 3582,2584,0, blue-couch-south
- 0x0738, 3585,2584,0, blue-couch-south
- 0x0738, 3585,2583,0, blue-couch-south
- 0x0738, 3584,2583,0, blue-couch-south
- 0x0738, 3583,2583,0, blue-couch-south
- 0x0738, 3582,2583,0, blue-couch-south
- 0x0738, 3581,2583,0, blue-couch-south
- 0x0738, 3581,2584,0, blue-couch-south

### holiday-fireplace (faces south): faces south; against the building's north wall

- 0x1E55, 3583,2585,0, holiday-fireplace
- 0x1E58, 3582,2587,0, holiday-fireplace
- 0x2BE0, 3582,2584,2, holiday-fireplace
- 0x32C9, 3584,2583,0, holiday-fireplace
- 0x32C9, 3581,2583,0, holiday-fireplace
- 0x32C9, 3583,2583,0, holiday-fireplace
- 0x2330, 3584,2584,5, holiday-fireplace
- 0x2BDB, 3582,2584,5, holiday-fireplace
- 0x1BDE, 3582,2583,0, holiday-fireplace
- 0x2331, 3581,2584,3, holiday-fireplace
- 0x0025, 3583,2583,11, holiday-fireplace
- 0x0025, 3582,2583,11, holiday-fireplace
- 0x2BDE, 3583,2584,2, holiday-fireplace
- 0x2BD9, 3583,2584,7, holiday-fireplace
- 0x2BDF, 3583,2584,2, holiday-fireplace
- 0x2BDD, 3582,2584,2, holiday-fireplace
- 0x1E56, 3582,2585,0, holiday-fireplace
- 0x1E57, 3582,2586,0, holiday-fireplace
- 0x1E5A, 3581,2586,0, holiday-fireplace
- 0x1E53, 3583,2587,0, holiday-fireplace
- 0x1E59, 3581,2587,0, holiday-fireplace
- 0x1E54, 3583,2586,0, holiday-fireplace
- 0x1E5B, 3581,2585,0, holiday-fireplace
- 0x0CB1, 3582,2584,16, holiday-fireplace
- 0x0CB1, 3583,2584,16, holiday-fireplace
- 0x29B0, 3581,2583,0, holiday-fireplace
- 0x29B0, 3584,2583,0, holiday-fireplace
- 0x19AB, 3582,2583,4, holiday-fireplace

## 3. Placed by the owner from a deed, in a house they own (run 4)

OSI's two-story stone and plaster house (multi 0x78, TwoStoryHouse) placed by staff on Felucca at 1228,1346,12
and handed to the trainee (Owner set). The trainee double-clicked each deed, picked the facing in the deed's
window and targeted the ground floor (Z 19) by the room's west wall: these three were placed (the deed used up;
`notes/cc-P867-tools/run4/walk.txt`):

- grey-fireplace-small-east, origin 1222,1349,19, faces east, against the west wall
- country-kitchen-east, origin 1222,1349,19, faces east, against the west wall
- blue-couch-east, origin 1222,1349,19, faces east, against the west wall

The rest of that run's tries were refused by pinned's house rules (unchanged), and the walk did not record which
rule. Known from the code and the data: the medium and grand fireplaces are 21 high, one more than a classic
storey, so they cannot stand under an upper floor 20 over theirs; and no piece may stand within a tile of a door.
That house's upper storey also kept the room covered from the camera, so the shots are section 2's.
