# P799: site survey of the stock (ML) New Haven

Read-only survey. Nothing was edited; no shard or Docker run.

- **Stock client:** `D:\UO\tool-trials\client-data-copy`, Trammel. **Decoration and spawns:** pinned `Distribution/Data`.
  The release has no Decoration overlay (`p799-isle/server/data` holds only `townsfolk-talk.json`).
- **Tools:** `notes\cc-P799-tools\stock\`.
  - `move.py`: a line-for-line Python port of pinned `Movement.cs` (CheckMovement, Check, IsOk, GetStartZ).
  - `spots.py`: the check of every spot below. Rerun it from that folder with `PYTHONPATH` set to it (first run about 1 min).
  - `r.py`: the renderer. `P799_CLIENT` and `P799_DATA` switch it to the SoS client.
- **Renders:** `notes\cc-P799-review\renders\` (all JPEG, all under 1 MB).

## How "standable" and "steps" were checked

Every spot marked "steps" was reached at that exact Z by an 8-way BFS from the start 3503,2574,14 using the Movement.cs
port: the player's diagonal rule, PersonHeight 16 clearance, step height, land and static impassable flags.

- **Second BFS:** run with the new pieces in place (four signs) and the release's pieces in the way: the Fountain of Youth,
  market carts, reset stone, quest board, mine forge and anvil, mine camp tents. Every spot stayed reachable, at most 2
  steps longer.
- **Doors** count as passable (the client opens them). **Mobiles** are ignored.
- **Not checked:** nothing here was walked in a client. The line-of-sight check is a rough one of mine (walls and
  impassable statics at eye height), not pinned's `Map.LineOfSight`.

## The table

| Use | Tile x,y,z | Steps from start | Note |
|---|---|---|---|
| **Theater** player arm spot | 3414,2602,55 | 89 | front of the audience floor, in the aisle, facing the stage |
| Bard echo A | 3410,2603,60 | 93 | on the stage |
| Bard echo B | 3411,2604,60 | 92 | on the stage, diagonal to A (the same offset as main's 3668,2530 / 3669,2531) |
| **Stables** arrival | 3534,2577,7 | 32 | aisle in front of the sick stall |
| Sick stall (horse) | 3534,2575,7 | 33 | east stall; left side as you walk in |
| Bucket of water (P743 piece) | 3535,2575,7 | 33 | same stall; stock hay already lies at 3534-3535,2574 |
| Stables sign (0xA854) | 3521,2573,5 | ground reached at 19 | see section 2 |
| **Mine** arm spot | 3512,2747,-1 | 179 | first dirt in the ravine, past the camp |
| Mine sign (0xA854) | 3477,2617,10 | ground reached at 46 | see section 3 |
| **Warrior yard** player | 3529,2544,20 | 34 | open dirt inside the Warrior's Guild Hall walls |
| Sparring echo | 3531,2541,20 | 37 | 3 tiles from the player, as P743's yard |
| **Magery** player | 3486,2501,52 | 74 | just inside the south door |
| Training echo | 3484,2497,52 | 78 | same room, 4 from the player |
| Mage demo | 3488,2500,52 | 75 | same room, 4 from the echo |
| **Rook** (west bench tile) | 3502,2530,22 | 45 | Inn's south yard, see section 6 |
| Second bench tile | 3503,2530,22 | 45 | |
| Moongate exit | 3502,2532,22 | 43 | in front of the bench, 2 tiles south (as P743) |
| **Housing** stop 1 | 3465,2596,13 | 38 | by the thatched cottage's north-east corner |
| Stop 1 sign | 3464,2596,14 | ground reached at 39 | 5 from the door 3459,2596 |
| Housing stop 2 | 3474,2603,10 | 32 | flat lawn east of the cottage |
| Stop 2 sign | 3474,2601,10 | ground reached at 30 | |

Twelve mining tiles (section 3) are listed there.

Sign and bench Z values are `GetAverageZ`. The sign is impassable and 6 high (0xA854), so each sign tile was checked as
open ground and then treated as blocked in the second BFS. The bench (0x0B2C) is not impassable and not a surface: Rook
stands at the floor Z, as on main.

## 1. Theater: yes, it is a stage

Render: `stock-theater.jpg`.

**It is a real theater.**
- Plank stage (0x04D4) at z60, x3410-3413, y2599-2605, on stone. Back wall of marble at x3409.
- Marble arches with curtains at 3411,2600 and 3411,2605. Wooden stairs at both ends of the stage.
- Audience floor of sandstone 0x0529 at z55, with 18 stone benches (0x045C) in two blocks of 3 by 3, x3415-3417,
  y2599-2601 and y2603-2605. The benches are not impassable, so they do not block; only the aisle y2602 reads as open.
- Stock `Actor` spawn at 3412,2602,60 (Vendors.json, home range 0). Pinned region "the Bardic Guild in New Haven" is this
  building, and the release's bard guildmaster stands in its back room at 3410,2608,55, 4 tiles from echo B.
- The release's two bard paintings hang on the wall at 3415,2598 and 3417,2598.

**Doors:** there are no door items. The main way in is the open doorway 3420,2601-2603 (z55), reached up the stone stairs
3421,2601-2603 (z52), 83 steps from the start. The second way is south, stairs 3412-3413,2612 into the back room (red
tile, z55, x3408-3413, y2607-2610), which joins the stage's south stairs.

**Open floor at z55:** x3414-3419, y2598-2605, plus x3420 at y2601-2603. Stage stairs at z57: rows y2598 and y2606, x3410-3413,
and 3413,2599 and 3413,2605.

Stage line of sight: player to both echoes is clear on the rough check. The stage is only 5 above the floor.

**No other building on the island has a stage.** Curtains appear only here, among statics of 3370-3770 x 2430-2830.

## 2. Stables

Render: `stock-stables.jpg`.

- **The building:** 3522-3536 x 2573-2579, plank land (0x0297) at z7, thatch roof, stock `AnimalTrainer` at 3527,2576,7.
  The release's Outriders guildmaster stands at 3524,2574,7 and `VetSpot` is 3526,2578,7, both in the west room.
- **Doorway:** open, 3522,2576-2577, no door item, 20 steps from the start.
- **Stalls:** three on the north side of the aisle y2576-2577: 3529,2574-2575 (one wide), 3531-3532,2574-2575,
  3534-3535,2574-2575. Hay statics lie in all three.
- **Troughs:** none in stock; no water trough static or decoration. The hay stands in for them.
- **Why the east stall:** tiles 3534,2575 and 3535,2575 are bare, and the sign's text "on the left" still holds.
- **Sign:** 3521,2573,5. Dirt shoulder at the building's north-west corner, north of the door path (y2576), off the cobbles,
  which end at x3520. A low grass tuft shares the tile. Exactly 3 tiles from the doorway.

## 3. Mine

Renders: `stock-mine.jpg`, `stock-mine-sign.jpg`.

**It is a mountain mine, not a cave.** There is no roof. Two dirt ravines run into the rock from the camp: a south arm
(x3510-3515, y2750-2765) and an east arm (x3512-3519, y2746-2752) that runs on to a pocket (x3520-3531, y2753-2759, z10-14).
Iron ore statics dot them, purely as decoration.

**Mining tile IDs:**
- Floor: dirt land 0x0076 (some 0x0077, 0x0071, 0x0082, 0x0083, 0x0089). **Not mineable**: these are outside pinned's
  `_mountainCaveTiles`.
- Walls, mineable: rock land 0x022C-0x022F, 0x0236-0x0238 (in 543-579) and edge land 0x00DC-0x00E2, 0x00E5-0x00E7 (in 220-231).
  Note tiledata names 0x00DC-0x00E2 "dirt", but they are impassable mountain edge.
- There are **no cave floor tiles here**. Pinned's static list is 0x053B-0x054F only, and no such static exists at the
  mine. The only ones on the island are 3573-3583 x 2593-2602, a floor inside the ruined Uzeraan's Mansion wall, not a mine.
- **So the lesson text must change:** "click the dark cave floor" fails here. Say "click the rock wall beside you". MaxRange
  is 2.

**Twelve lesson tiles.** All are standable dirt with mineable rock in the next tile, and all fall in one 8x8 ore bank
(439,343), so a single `FreshBank` covers them:

    3512,2746,-1  3513,2746,-1  3513,2747,0   3514,2747,0
    3515,2747,1   3516,2747,1   3517,2747,1   3512,2748,1
    3513,2748,1   3514,2748,2   3515,2748,2   3517,2748,2

Steps 179-184. 3516,2747 carries a stock ore static (passable).

**Arm spot:** 3512,2747,-1, 179 steps. The release's camp stands just west of it (Jacob Waltz 3510,2745; anvil 3510,2746;
forge 3508,2746; Mugg 3507,2747; Gervis 3505,2749); the ravine stays open past them.

**Route, 179 steps either way:**
- By the south gate (the town wall's opening 3469-3476 x 2612-2615): 3491,2586 > 3482,2595 > the gate > 3479,2619 >
  3482,2631 > 3479,2643 > 3477,2667 > 3485,2691 > 3497,2715 > 3505,2739 > 3512,2747. This is the one to describe.
- The BFS's own shortest goes by the shore strip x3487, y2595-2620, below the wall. Same length, but it clips a cliff
  edge (3488,2625,-8). It is legal but ugly, and an arrow may lead players that way.
- The road ends near 3466,2657; the last 90 tiles are open grass, so the sign has no road to mark after the gate.

**Sign:** 3477,2617,10, on grass just east of the road, immediately south of the gate. **Does not fit the brief exactly:**
the road here runs north-south, so it has no north side. It stands on the east shoulder, north-east of the line the walk
then takes, and is the first thing seen leaving the gate.

## 4. Warrior yard

Render: `stock-warrior.jpg`.

The hall's open dirt court, z20, about x3523-3539, y2531-2552, inside stone walls. Player 3529,2544,20; echo 3531,2541,20.
Both clear of the release's NPCs by 3 tiles or more (Jockles 3535,2544; warriors' guildmaster 3530,2537; Alden 3535,2537;
Aelorn, Dimethro and the smith at y2536). Line of sight clear.

**No training dummies in stock:** one archery butte at 3538,2529,20 only. If the lesson wants dummies they must be placed.

## 5. Magery

Render: `stock-magery.jpg`.

Pinned "the New Haven Mage" (3464-3491 x 2488-2504) is the release's **New Haven Magery School**: three floors (z52, z71,
z91), with the arcane guildmaster and the mage trainers. The small shop at 3493-3497 x 2527-2534 is where the stock
`Mage` and `MageGuildmaster` spawns stand.

South room, z52 carpet, x3483-3488, y2497-2502, 6 by 6. South door 3485-3486,2503 (72 steps).
Player 3486,2501,52; training echo 3484,2497,52; mage demo 3488,2500,52. Line of sight clear on all three.

- **Tight:** P743's distances were 5 and 6; here they are 4 and 4. The room holds Lyle (3487,2498,52) and the Artificers'
  guildmaster (3483,2501,52) too; the demo is 2 tiles from Lyle. Stairs and the guildmaster's room lie north through 3485,2496.
- Tile 3484,2497 also holds a wall banner static (0x158E, not impassable).

## 6. Rook's bench

Render: `stock-rook.jpg`.

**There is room, by the Inn, not by a tavern proper.**

- **Recommended:** the Bountiful Harvest Inn's south yard, 45 steps north of the start. It is the town's dining house
  (stock Cook, Waiter, InnKeeper). Bench 3502-3503,2530,22, against its rail, Rook on 3502; moongate exit 3502,2532,22. Three
  tiles from the porch stairs 3506,2529. The cobble yard is 5 rows deep, so the bench blocks nothing. Bench tiles sit
  under the Inn's roof overhang (slate at z70+), so a client's roof hiding may trim the eave while standing there; the
  exit tile is clear.
- **Rejected:** the real tavern (Barkeeper 3434,2568,53) stands on z53 decks 79 steps from the start, at the far west of town; I
  did not look for bench tiles there.
- **Fallback:** Rook stays on the plaza at 3500,2572,14. Stock benches stand about 5 tiles away round the memorial (0x0B2D at
  3505,2575, 3507,2575, 3505,2577, 3507,2577, z18-19), and a stool deck at 3500-3506 x 2558-2564, z21, but neither is a
  tavern. Moving him is a choice for Chase: the plaza is closer to the start and nothing about it is broken.

## 7. Housing stops

Render: `stock-housing.jpg`.

- **Stop 1:** 3465,2596,13; sign 3464,2596,14. The building is the thatched cottage 3453-3462 x 2596-2603, which is **the
  League office**, the most house-like small building near the tour centre 3460,2590 (I did not check every building's use).
  Doors 3459,2596 (street) and 3457,2599 (inner). The stop is outside on the grass, beside the ankh garden.
- **Stop 2:** 3474,2603,10; sign 3474,2601,10. Flat z10 grass, x3469-3482, y2597-2611, the flattest open ground in town.
- **Text changes needed:** `HousingStop1`'s "the field just south of here" and the tour's "the field south of the cottage"
  must say **east**. The field south of the cottage (3440-3462 x 2616-2630) is hilly, z14-40, so it reads badly as house
  ground. "This cottage is a small house" should allow for the Registrar living in it. "East of the square" must
  also change: the cottage is west of it.
- `TourCentre` (3460,2590) is already right for the release. Stop 3 (bank) needs no change.

## 8. Reachability

Every spot above is reachable on foot from the start; steps are in the table. Closest: stables doorway 20. Farthest: mine 184.

## Main's SoS map

Renders: `main-bardic-guild.jpg`, `main-league-door.jpg` (client `p708-work\sosclient`, decoration
`ShatteredLegacy\server\data`).

- **Bardic Guild hall (3655-3679 x 2528-2544): no stage, not a theater.** P743's note "its long hall with the stage" is wrong.
  An L-shaped stone hall at z0: a long west-east room with a blue carpet (3658-3662 x 2530-2533) and, at the west end, a glass
  **display case** (3656-3658 x 2529-2534, 0x0B0F-0x0B18, impassable) holding a lute, drum and tambourines. That case is
  what looks like a stage. The north-south wing has a long table with bamboo chairs (x3674-3675). Harps and music stands stand
  along the north wall (decoration).
- **No theater elsewhere on the SoS Haven (3600-3760 x 2440-2800).** No stone benches, podiums, arches or platforms. The
  only curtain is 3737,2579,40 at the Proving Grounds, with its rod.
- **Ankh by the League hall street door 3667-3668,2562: nothing near the door, but there is one by the building.** No ankh
  static stands there; the render shows bare grass and road. However `ClusterFAnkhs.cs` line 60 on main places an **item**,
  AnkhWest (0x0003 with its 0x0002 half), at **3676,2562,0**, "ours, Chase 2026-10-16; cc-P678 by the new office". That is 8
  tiles east of the door, round the building's south-east corner, and items never show in a statics scan. A render cannot show
  it either, and whether a given world has it depends on `[ClusterFSeedAnkhs` having run.
- **Decoration ankhs in Haven: none.** `server/data/Decoration` has 14 ankh entries (shrines 9, Despise 2, Destard, Magincia,
  Yew), none inside the island bounds 3314-3813 x 2345-3094.

## Port notes

- `ClusterFAnkhs` already has the stock ankh over the statics at 3464,2600,27 on the release. Keep that line in the port;
  main's 3676,2562 is an SoS spot and should not come across.
- The pieces the lessons reserve on the release stay clear of all these spots: `Yard` 3411,2617 is about 5 tiles south of the theater
  wall; `TradesYard` 3426,2626 is far from everything here.
- Old stock farm 3372-3401 x 2603-2619: P743 removes it at seed; unaffected by this survey.
