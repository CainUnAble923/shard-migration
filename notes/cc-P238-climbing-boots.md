# cc-P238: climbing boots for the unreachable mountain ore (F-36)

Copper Golem, 2026-10-21. Server only. Branch `golem/Copper/P238` in both repos. Image `sl-modernuo:cc-P238`. Nothing was
run against any world.

## Headlines

- **A quarter of the ore banks cannot be mined today.** Counted from the client map:
  - Felucca: 11,748 of 47,071 ore banks (25.0%) have no walkable tile within Mining's reach of 2; on the mainland
    (x < 5120), 7,330 of 20,768.
  - Trammel: 13,124 of 48,799 (26.9%); on the mainland, 9,264 of 23,326.

  The tool is `notes/cc-P238-tools/unreachable_banks.py`. The count is a floor, because ledge height is ignored.
- **Three climbing boots**, sold by the Miners' Compact Liaison in the satchels' pattern:
  - Surveyor's: hop 4.
  - Delver's: hop 8, half the stamina.
  - Deepwarden's: hop 12, plus ledge memory (one hop back to the last climbed tile from within 30).

  They are blessed, bound to the account (unbound staff-made boots bind to their first wearer), recoverable at the
  Liaison, and use the stock Boots graphic 0x170B. They are gated on Compact rank, Mining (120 / 150 / 180) and blocks
  mined (100 / 300 / 600), and priced in vouchers, gold and ingots. Every number is a setting.
- **The hop.** It lands only within range and only on mountain or walkable ground, at the map's own z. It never lands
  inside a static, and never in a town, dungeon, house or no-teleport place. Stamina grows with the climb, and there is
  a 2.5 s cooldown. Followers are told to stay on the way up and to follow on the way down; none is released or moved.
- **On a climbed tile** a player can mine, prospect and hop, and nothing else: no attacks or harmful spells, no taming,
  no Mark, no house placement. A monster's harm still reaches them. This takes two small patches: four hook lines in
  `PlayerMobile` and `HousePlacement`.
- **Prospector's Logbook: blocks mined.** One record per 8 x 8 bank (facet, bank, first mined, ores found), counted in the
  logbook header and on the Liaison's boots page. It is account data v22, round-trip tested, and records the *targeted*
  tile's bank, not the miner's.
- **Tests:** 10 new facts in `server/tests/Misc/ClimbingBootsVerification.cs`, each seen failing first. The full suite is
  green through `docker/uo/build.sh`: 1,901 tests, 1,897 passed, 0 failed, 4 skipped, and the image was built.
- **cc-P192:** the Fountain of Youth's "climbing" access kind is now available (details in Part 7).

## Part 1: facts

**Sources.** `D:\UO\ModernUO-pinned` is not on this PC. Pinned was read from the builder images (`sl-uo-builder:cc-P229`
for reading, `cc-P231` for the patch base), the patched build tree at d4531cd9.

**A mobile on impassable land** (all read in pinned):
- `MoveToWorld` places a mobile anywhere and does not check the tile.
- At logout the location is kept, and at login `LogoutLocation` is restored with no check (`Server/Mobiles/Mobile.cs:
  1320-1323`). A climber who logs out on a peak logs back in on it.
- Movement from there: `Movement.GetStartZ` (`UOContent/Engines/Pathing/Movement.cs:487-578`) treats impassable land as
  no footing. With nothing else under the mobile, `zLow = zTop = loc.Z` (`:572-575`), the mobile's own z. The next
  step is checked by `CheckMovement` like any other: impassable land refuses it (`landBlocks`, `:254-257`, `:437`), and
  a walkable neighbour within a step's height accepts it.

  So a climber cannot walk across the mountain, but can step off its edge onto ground about level with them. The client
  checks tile flags too and will not send a move onto impassable land (F-36's own note), which is why this is a hop and
  not a walk.
- **Land z versus the player's z:** the landing z is the land's average z (`Map.GetAverageZ`), the same z pinned's
  `CanFit` tests impassable land at. The hop never takes z from the target.
- **A hop into a static can be refused cleanly** by `Map.CanFit(x, y, z, 16, checkBlocksFit: false, checkMobiles: true,
  requireSurface: false)` (`Server/Maps/Map.cs`, the last `CanFit`). On impassable land at its own average z it passes,
  since `avgZ > z` is false. But any static or item, surface or impassable, overlapping the 16-high body refuses it, and
  so does another mobile there. Fact 3 proves the item half in the test host with a real stone-wall tile row.

**The count.** `notes/cc-P238-tools/unreachable_banks.py` uses cc-P151's reader (`notes/cc-P151-tools/uomap.py`) over the
client files in `D:\ShatteredLegacy\client-data\classic-client`, about 20 s per facet:
- An ore bank is an 8 x 8 map block with at least one tile our Mining can dig: the land ranges `_mountainCaveTiles` and
  the static ranges `_mountainCaveStaticTiles`, `server/patches/Mining.cs:24-55`, inclusive pairs.
- A bank is unreachable when none of its mineable tiles is within 2 (Chebyshev) of a walkable tile.
- Walkable means passable dry land or a floor static, with no blocking static. Heights are ignored, so the count is a
  floor.

Spot check: the first unreachable mainland bank, x 272 to 279 at y 1384 on Trammel, sits in the western mountains. There
the last walkable tile is x 269, three tiles from the bank (land rendered from the same reader).

| Facet | Ore banks | Unreachable | Mainland (x < 5120) | East of 5120 (dungeons, Green Acres) |
|---|---|---|---|---|
| Felucca | 47,071 | 11,748 (25.0%) | 7,330 of 20,768 | 4,418 of 26,303 |
| Trammel | 48,799 | 13,124 (26.9%) | 9,264 of 23,326 | 3,860 of 25,473 |

**What TazUO draws for a player on mountain land is a client check for Chase** (For Chase, item 2).

## What changed

ShatteredLegacy repo:

| File | What |
|---|---|
| `server/customizations/ClusterFClimbing.cs` (new) | Terrain seam `IClimbTerrain` `:54`. `MapClimbTerrain` `:60`: walkable means passable land or a surface static that fits; mountain means impassable land on Mining's list (`OreAndStone.Validate`) with `CanFit` at its average z. Settings and `DefaultTiers` `:138`, `Configure` `:145` (`clusterf.climbing.*`). `IsOnClimbedTile` `:187`. The patches' hooks `RefusesHarm` `:196`, `RefusesSkill` `:212`, `RefusesSpell` `:224`. `StaminaCost` `:255`, `MayLandAt` `:276`, `TryHop` `:293`, `TryLedgeReturn` `:312`, `Land` `:355`, `OrderPets` `:412`. The sale: `Requirements` `:469`, `BuyNext` `:487`, `Recover` `:540`. |
| `server/customizations/ClimbingBoots.cs` (new) | `ClimbingBoots : BaseShoes` `:28` (abstract; the type name P192 checks). Bound account and ledge memory are serialized fields; binding as `BoundCosmeticSash`'s, with an unbound pair binding to its first wearer (`Owns` `:132`, `OnEquip` `:161`). Use, then target: a tile to hop, yourself for the ledge. `SurveyorsClimbingBoots` `:158`, `DelversClimbingBoots` `:174`, `DeepwardensClimbingBoots` `:190`. |
| `server/customizations/ClusterFMinedBlocks.cs` (new) | `Mining.MutateType` override `:23` notes the targeted tile. `OnGive` `:63` records the block from `Mining.Give`; `Record` `:74`. |
| `server/customizations/ClusterFAccountData.cs` | `MinedBlocks` `:227`; v22 read `:467`; `CurrentVersion = 22` `:503`; written last `:618`; `MinedBlockRecord` `:1340` (its own version 0, refuses an unknown one). |
| `server/customizations/CompactOreSatchelRoutingHook.cs` | `:95`, `ClusterFMinedBlocks.OnGive` before the extended-ore gate swaps the ore for iron. |
| `server/customizations/ProspectorsLogbookGump.cs` | `:87`, "Blocks mined: N" in the header (the footer has no room beside Field Report). |
| `server/customizations/MinersCompactLiaisonGump.cs` | Dashboard "Climbing Boots" `:327` (button 40). `DrawClimbingBoots` `:472`: blocks mined, the boots on hand, the next tier's requirements (cc-P169 `RequirementList`), or recovery. Buttons 92 (buy or upgrade) and 93 (recover) `:782`. |
| `server/patches/PlayerMobile-climbed-tile-rules.patch` (new) | Three hooks: `CanBeHarmful` (attacks and harmful spells, `target != this`), `AllowSkillUse` (taming), and a new `CheckSpellCast` override (Mark). |
| `server/patches/HousePlacement-climbed-tile.patch` (new) | `HousePlacement.Check` returns `BadRegion` for a climber. |
| `docker/uo/apply-patches.sh` | The two `apply_patch` lines, last, with their reason. |
| `server/tests/Misc/ClimbingBootsVerification.cs` (new) | 10 facts. |
| `server/tests/Route/TestTileRows.cs` | `TileRows.StoneWall`: row 0x0080, read from the client `tiledata.mul` field for field as `TileData.Load` reads it (flags 0x4006050, weight 255, height 22). |
| `server/tests/Misc/AccountDataSerializerVerification.cs`, `RequisitionsVerification.cs`, `LeagueShopVerification.cs` | The version bump, as cc-P150 and cc-P229 did it: "current version" asserts 21 to 22. The hand-built old saves also trim the empty v22 tail (8 bytes), and LeagueShop's future-version probe moves 8 bytes earlier. |
| `server/tests/Misc/FountainOfYouthVerification.cs` | R1 pins "climbing" unavailable for its own run (Part 7). |
| `CHANGELOG.md`, `VERSION` | New section 2026.10.21.5 (Added, Staff); VERSION bumped from 2026.10.21.4, whose section was already committed. |

**The patches, argued (AGENTS.md: alternatives first).**
- **A region** would be the stock route for "no combat here": `Region.AllowHarmful` and friends. But the climbable tiles
  are tens of thousands of scattered mountain tiles, not areas. Registering them as regions would mean hundreds of
  thousands of rectangles, and a region also changes music, guards and rules for whoever stands inside it.
- **An event:** pinned raises none before an attack, a skill use or a cast.
- **Wrapping the taming skill callback in Configure** was possible for taming alone, but it depends on `Initialize`
  order and covers neither attacks nor Mark.
- **Overriding through a subclass** is impossible: every player is a `PlayerMobile`.

So: three lines in `PlayerMobile`, which several of our patches already touch, and one in
`HousePlacement.Check`, each asking `ClusterFClimbing`. Harm done **to** a climber is the attacker's own `CanBeHarmful`
and is untouched, so a monster's spell still lands (fact 4 checks `orc.CanBeHarmful(pm)`).

## Part 2: the logbook per block

- **Where the bank comes from.** The record keys on the **targeted** tile's bank, tile / 8 as pinned's
  `HarvestDefinition.GetBank` keys it. The routing hook's existing depletion check (`BroadcastDepletionIfEmptied`) uses
  the miner's own tile, which can sit in the next bank over, because a miner reaches 2 tiles. `Mining.Give` never sees
  the target, so a `MutateType` override (`FinishHarvesting` calls it with the target just before making the ore) notes
  it, and `Give` records it. Fact 9 mines from x 807 (bank 100) at x 809 and gets bank 101.
- **What it records:** facet, bank x and y, the first time, and every ore type found there (Iron included, keyed as
  "Iron", "Copper", ...).
- **Account data v22.** A save from before reads with no blocks, so everyone starts at 0: mining from before this build
  is not counted (Deviation 2).
- Reaching a gate count (100, 300, 600) prints one line.

## Part 3 and 6: the boots and the sale

| Tier | Boots | Rank (standing) | Mining | Blocks | Hop | Price (placeholders, every one a setting) | Hue |
|---|---|---|---|---|---|---|---|
| 1 | Surveyor's | Surveyor (15,000) | 120 | 100 | 4 | 75 vouchers, 20,000 gold, 100 Platinum ingots | Verite |
| 2 | Delver's | Master Delver (40,000) | 150 | 300 | 8, half stamina | 150 vouchers, 50,000 gold, 150 Frost ingots | Valorite |
| 3 | Deepwarden's | Deepwarden (80,000) | 180 | 600 | 12, half stamina, ledge memory | 250 vouchers, 100,000 gold, 200 Mythril ingots | Platinum |

- **Ingots** are a metal the tier's Mining can work (`ClusterFMetalTiers`: Platinum 112.5, Frost 150, Mythril 175).
- **Hues** are the satchel of the same rank's (Surveyor's, Deepdelver's and Master Expedition Satchels), through
  `CraftResources.GetHue`.
- **Rank names** come from `MinersCompactLiaisonGump.GetRankName`.
- **Upgrades and recovery:** each upgrade consumes the boots worn or carried. The registry key
  `compact.climbing_boots_t{n}` records ownership, and lost boots are recovered for 5 vouchers (as the satchels are).
- **Settings:** `clusterf.climbing.t{1,2,3}.{hopRange,rankStanding,mining,blocksMined,vouchers,gold,ingots}`, plus
  `clusterf.climbing.{cooldownMs,staminaBase,staminaZPerPoint,maxClimbZ,ledgeRange,petRange,restoreVouchers}`.

## Part 4 and 5: the hop and the climbed tile

- **Range:** Chebyshev distance 1 to the tier's range.
- **Stamina:** 5, plus 1 per 4 z climbed; half (rounded up) from Delver's. A level or downward hop costs 5. The highest
  climb in one hop is 60 z.
- **Cooldown:** 2.5 s.
- **Refused into:** `TownRegion`, `DungeonRegion`, `HouseRegion`, any spot `BaseHouse.FindHouseAt` finds, and anywhere
  `SpellHelper.CheckTravel(TeleportTo)` refuses. A hop is also refused from where `TeleportFrom` refuses.
- **Climbed tile** = standing on mountain land with no walkable surface under you. Staff are never held to it.
- **Pets:** the hop up orders the climber's controlled creatures within 15 to Stay; the hop down orders those within 15
  of the landing to Follow. Nothing is released, moved or stabled.
- **Ledge memory:** Deepwarden's boots save the last climbed tile on the item. From the ground on the same facet, within
  30 tiles, targeting yourself hops back to it (the usual checks and cost).

## Part 7: register the deviation, and cc-P192

**For `docs/fidelity-principle.md`** (agents do not edit `docs/`; wording for promotion):

> **Climbing boots (cc-P238, F-36). Ours, not OSI.** OSI has no climbing. The Miners' Compact sells three tiers of boots
> that hop a player onto impassable mountain tiles (4, 8 or 12 tiles) to mine ore banks no walkable tile can reach.
> While standing on a climbed tile a player can only mine, prospect and hop: no attacks, harmful spells, taming, Mark or
> house placement, though hostile spells still reach them. Pets are ordered to stay below. Implemented in
> customizations ClusterFClimbing/ClimbingBoots and two patches (PlayerMobile-climbed-tile-rules, HousePlacement-climbed-tile).

**To cc-P192's owner (the Gold Golem; Fountain of Youth):** your "climbing" access kind can now be checked. The type
`ClimbingBoots` exists, so `FountainPool.AccessAvailable("climbing")` is true from this build on (fact 1 asserts it), and
the two climbing-only pool entries are used:
- `peak-kendall`, Trammel 2576, 360;
- `peak-serpent`, 1680, 600 (`FountainOfYouth/FountainPool.cs:317-318`).

Their coordinates were marked "to check in game". With boots in game, someone can now stand on them. Your fact R1
asserted the climbing peak is never used; with boots in the build that is no longer the shard's default, so R1 now pins
climbing off for its own run, which keeps what it tests (an unavailable kind is never used).

## Tests

`server/tests/Misc/ClimbingBootsVerification.cs`, 10 facts. Most give `ClusterFClimbing` a terrain grid (the test host has
no map); fact 3 uses the real `MapClimbTerrain`.

1. `AHopLandsOnlyWithinRangeOnAnAllowedTile`:
   - Refused: the own tile, 5 tiles with range 4, a blocked tile, a 100 z climb.
   - Accepted: a mountain 3 away, landing at its own z 30, after which the player counts as climbed; a hop down to
     walkable ground.
   - Boots carried, not worn, refuse.
   - Unbound (`[add`) boots bind to their first wearer, and another account then cannot wear them.
   - P192's "climbing" is available.
2. `AHopIsRefusedIntoATownADungeonAndAHouse`: registered `TownRegion` and `DungeonRegion`, and a test house. Nothing
   moves and no stamina is taken; open country is fine.
3. `TheRealTerrainRefusesALandingInsideAStatic`: with the real stone-wall row seeded, the real terrain gives walkable at
   the land's z, then Blocked once a wall stands there, and the hop says "no footing".
4. `OnAClimbedTileOnlyMiningProspectingAndHoppingAreLeft`:
   - On the ground, attack, taming and Mark are allowed.
   - Climbed, `CanBeHarmful`, taming, Mark and `HousePlacement.Check` are refused, while Mining is allowed and the orc
     can still harm the climber.
   - Staff are exempt, and back down everything is allowed again.
5. `PetsAreToldToStayAndThenToFollowAndNoneIsLost`: a horse is ordered to Stay on the hop up and to Follow on the hop
   down. It stays controlled by the same master and is never moved.
6. `StaminaCostGrowsWithTheClimbAndTheCooldownApplies`:
   - A 32 z climb costs 13, a level hop 5, and half rounded up from Delver's.
   - The cooldown still refuses at 2.4 s and allows at 2.6 s (`ShardTestClock`).
   - A player too tired to pay is refused and keeps their stamina.
7. `LedgeMemoryReturnsWithinThirtyTilesAndNotBeyond`: the ledge return works at 30 tiles and is refused at 31; there is
   none before any climb, and Delver's boots remember nothing.
8. `TheGatesRefuseOneShortOfEachAndTheUpgradeConsumesTheBootsBefore`:
   - One short of rank, Mining, blocks, vouchers, gold or ingots is refused, with nothing taken.
   - Every gate met: bought, the exact price taken, blessed, bound, registered, Verite hue.
   - The Delver's upgrade is refused one rank short, then consumes the Surveyor's.
   - Lost boots are recovered once for 5 vouchers.
   - The Liaison page shows the block count.
9. `TheLogbookRecordsTheTargetedBlockOnceAndCountsIt`: through `Mining.MutateType` and `Mining.Give`:
   - The targeted bank (101) is recorded, not the miner's (100).
   - The same bank twice is one record with both ores; the next bank makes 2.
   - An ore with no swing behind it is not counted.
   - The logbook header shows "Blocks mined: 2".
10. `TheAccountsBlocksRoundTripThroughASave`: blocks, first dates and ores round-trip through `ClusterFAccountData`, and
    an unknown `MinedBlockRecord` version is refused.

**Seen failing first.** I saved `ClusterFClimbing.cs`, `ClusterFMinedBlocks.cs` and `ClusterFAccountData.cs`, applied ten
marked breaks (`P238-BREAK`), ran `docker/uo/build.sh -t sl-modernuo:cc-P238 --tests-only`, and copied the three files
back (`cmp` identical, no marker left). Result: 1,901 tests, **10 failed, exactly the 10 new facts**, each at its own
assertion:

| Fact | Break | Line | Failure |
|---|---|---|---|
| 1 | range plus 1 | `:196` | "Expected TooFar, Actual Hopped" |
| 2 | towns allowed | `:232` | "Expected Forbidden, Actual Hopped" |
| 3 | `CanFit` skipped | `:258` | "Expected Blocked, Actual Walkable" |
| 4 | `RefusesHarm` always false | `:287` | |
| 5 | no Stay order | `:320` | "Expected Stay, Actual Follow" |
| 6 | stamina ignores z | `:346` | "Expected 87, Actual 95" |
| 7 | ledge range `>=` | `:385` | |
| 8 | no blocks gate | `:460` | the one-short loop |
| 9 | the miner's tile recorded | `:537` | |
| 10 | ores not saved | `:573` | "Expected [Copper, Iron], Actual []" |

The binding assertion added to fact 1 afterwards was shown failing on its own: with the bind-on-equip line removed, fact 1
failed at `:223` ("Expected p238..., Actual \"\""), 1 failed of 1,901. The file was then restored, `cmp` identical to the
one that built green.

**Real code runs:**
- **Run 1:** `LRReason` needed `using Server.Network`.
- **Run 2:** 8 failed:
  - 5 version asserts (21 to 22);
  - Fountain R1 (now "climbing");
  - my fact 8 (`PlatinumIngot` has only an optional-argument constructor, so pinned's `CreateInstance`, not
    `Activator`);
  - my fact 2 (`Rectangle3D` takes x, y, z, width, height, depth).
- **Run 3:** LeagueShop's future-version probe offset.
- **Run 4:** `CovetousVoidSpawnVerification.SetupPlacesTheControllersThePoolTheSpawnersAndThePaths` failed once ("an
  angered spirit at (5500, 1801, 0)" outside its bounds). It passed in run 3 and in every full run since, with no change
  of mine near it: an existing random flake, not this prompt's.
- **Full runs, green:**
  - "Total tests: 1901, Passed: 1897, Skipped: 4" and "Built sl-modernuo:cc-P238 with patches applied and 1897 shard
    test(s) passing", after the seen-failing run.
  - After the binding change, one more red run: a fresh test character has Str 0, which clothing's `CanEquip` refuses,
    so the test gives it strength.
  - Then green again, same totals. That is the state on disk.

`CHANGELOG.md` and `VERSION` were edited after; no test reads them.

## Deviations and decisions for Chase

1. **Hop, not walk.** As F-36 recommends: the client will not send a move onto impassable land, so walking would need a
   TazUO change.
2. **Blocks mined starts at 0 for everyone.** Mining before this build was never recorded by bank, so the 100 / 300 /
   600 gates count from now on.
3. **Surefoot carries up.** Deepwarden's boots keep Delver's half stamina (F-36 lists each tier's new feature; I read the
   tiers as cumulative).
4. **"The same range" for ledge memory is distance only:** same facet, within 30 tiles, and standing on the ground.
   Telling mountain ranges apart would need a flood fill of the map at run time.
5. **The highest one-hop climb is 60 z.** F-36 says "z checked" without a number.
6. **Pets in range** means 15 tiles: from the start of the hop going up, from the landing coming down. A pet farther away
   keeps its order, and none is ever released, moved or stabled.
7. **Staff are exempt** from the climbed-tile rules.
8. **What counts as mountain** is impassable land whose tile id is on our Mining's mountain list. Cave floors and
   ordinary rock statics are not climbable; a static floor on top of a mountain is ordinary walkable ground.
9. **Line of sight from a climbed tile is not touched.** Whether mining a neighbouring mountain tile passes pinned's LOS
   check is a client test (For Chase, item 3).
10. **`D:\UO\ModernUO-pinned` and `D:\UO\ServUO-pub57` are missing on this PC** (also noted in cc-P230 and cc-P231).

## For Chase (test shard)

Run nothing on live. These are commands for the test shard; each read-only check is a dry run of the next step.

1. **Kit a tester** (a test character on a test account), Administrator:
   - **Dry run first:** `[props` on the character, and check Mining, Compact standing and vouchers.
   - **Then:** `[add DeepwardensClimbingBoots`. Hand them over; the first wearer binds them.
   - To try the Liaison purchase instead, open the Liaison, Member Dashboard, then Climbing Boots. The page lists every
     gate met or not, with the buy button only when all are met.
2. **TazUO on a mountain:** wear the boots, use them, and target a mountain tile within 12. Does the character draw
   standing on the slope at the right height, or sunk or floating? Log out and back in: you should still be there. Try to
   walk across the mountain (refused) and off its edge onto ground (should work if level).
3. **Mine on the peak:** with a pickaxe, target a mountain tile next to you. It should mine (Line of sight is the open
   question). Then open the Prospector's Logbook: "Blocks mined" in the header grows by one for each new 8 x 8 block.
4. **The rules:** on the peak, try to attack a monster, cast Magic Arrow at it, tame an animal, and cast Mark: each is
   refused with a line. Have a monster cast at you: it lands.
5. **Pets:** with a pet following, hop up: it stays below. Hop down: it follows again.
6. **Refusals:** try to hop into Britain, into a dungeon entrance region and into a house: "Your boots will not take you
   there."
7. **Ledge memory (Deepwarden's):** hop up, hop down, walk away (within 30), use the boots and target yourself: back on
   the ledge.
8. **P192:** the Fountain of Youth's climbing-only peaks (`peak-kendall` Trammel 2576, 360; `peak-serpent` 1680, 600) are
   now in its pool. Worth standing on them to confirm a fountain can sit there.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, 2026-10-21:

```
Repo Result
---- ------
code dry run
docs dry run
```

Neither repo is BLOCKED. Code: 18 files (3 new customizations, 4 changed customizations, 2 new patches,
`apply-patches.sh`, 1 new and 5 changed test files, `CHANGELOG.md`, `VERSION`). Docs: this note and
`notes/cc-P238-tools/unreachable_banks.py`. No file in either repo is over 5 MB; the pinned and patch scratch is in the
session scratchpad, outside both repos.

P238 DONE
