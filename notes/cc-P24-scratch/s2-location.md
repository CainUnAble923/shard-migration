# P24 section 2: location (dungeon interior space, entrance building, region type)

Read-only research, 2026-10-01. Nothing outside `notes/cc-P24-scratch/` was changed.
Scripts and renders: `notes/cc-P24-scratch/s2/` (16 PNGs, 19 .py, 6 .json; the large .npy grids were
deleted, rerun `t1.py`, `t2.py`, `t3.py`, `t5.py` in that order to regenerate them).

Versions read:
- 117 data: `D:\UO\UltimaOnlineVanilla` (map1LegacyMUL.uop, statics1.mul 20,393,786 B, staidx1.mul, tiledata.mul, radarcol.mul).
- 114 data: `D:\ShatteredLegacy\client-data\classic-client` (statics1.mul 20,516,244 B).
- Pinned ModernUO: `D:\UO\ModernUO-pinned` HEAD 7c9215d97 (2026-05-06).
- Shard: `D:\ShatteredLegacy` HEAD f49e693 (2026-10-01 05:02). Working tree has uncommitted
  `server/customizations/SmithGuildSalvageBag.cs` (M) and `server/tests/Items/SalvageBagIngotReturnVerification.cs` (??),
  neither touches New Haven or regions. P22 "thief at the pit" has NOT landed: no "lookout" / "3440, 2558" in
  `server/customizations` (grep, 0 hits). I read the P22 brief `D:\UO\cc-prompts\cc-P22-small-features-1.md:97-125`.

Method: own Python reader (`s2/uomap.py`). map1 UOP has 113 entries, 89,915,588 bytes = 458,752 blocks (7168x4096)
plus one trailing 196-byte block, ignored. Static counts: 117 = 2,913,398, 114 = 2,930,892 (counted from staidx/statics).
Void land tile = **0x0244** (tiledata flags 0x50 = Impassable+Wall); it is the most common land id at x >= 5120
(4,060,188 tiles in 117). 0x0002 ("NODRAW") is not the dungeon filler. Pinned `map-definitions.json` gives
Trammel 7168x4096.

---------------------------------------------------------------------------------------------------------------------
## 1. Unused Trammel space for the dungeon interior

"Empty" = land 0x0244 AND zero statics on the tile, in BOTH 117 and 114. Then excluded:
- every Trammel rectangle in pinned `Distribution/Data/regions.json` (337 rects, 128 names, all expansions, children
  included; I masked them regardless of Min/MaxExpansion, so this is conservative);
- every Trammel point in pinned `teleporters.json`, `Spawns/**/*.json` and `Decoration/Trammel` + `Decoration/Britannia`
  (28,584 points in all);
- every Trammel rect in ServUO `Data/Regions.xml` (480 rects with x/y/width/height; rects in other forms skipped, count
  not taken) as a forward risk, since content we port later brings those regions with it;
- the 114/117 changed zone plus 32 tiles (below);
- then whole 8x8 blocks only, with a further 16-tile (2-block) empty buffer on all sides.

Our shard adds regions only in code: one class, `DespiseRegion : BaseRegion`
(`server/customizations/Services/Revamped Dungeons/DespiseRevamped/Region.cs:33`), four instances registered at runtime
(`DespiseController.cs:178-181`), all inside the Despise dungeon (5377-5631 x 516-1022). No region JSON in the shard
(`find -iname "regions*.json"` outside client-data: 0), no patch touches regions.json (grep of `server/patches`: 0), and
the image copies pinned's Data folder unchanged (`docker/uo/Dockerfile:88`). No class deriving from any Region in
`server/` other than DespiseRegion (grep: 1 hit). None of the candidates below touches Despise.

**114 vs 117 difference** (counted, tile by tile): land differs on 189,288 tiles, static occupancy on 18,428.
Bounding box x 6450-6958, y 3041-3619 (189,561 tiles), plus a small separate patch at x 736-782, y 2127-2157 (599 tiles,
Britannia, irrelevant here). So the brief's "x 6144-7167, y 3072-3583" is close but not exact: it starts 31 rows higher
(3041) and ends 36 rows lower (3619). Every candidate below is >= 32 tiles clear of it.

Candidates (all inclusive coordinates, all verified 100% empty in both 114 and 117, zero region tiles):

| id | x range | y range | size | notes |
|----|---------|---------|------|-------|
| **A** | 5136-5247 | 1128-1263 | 112x136 | classic dungeon strip. 24 tiles W of Jail (5271-5312 x 1159-1192), ~20 N of the unregioned Orc Cave rooms at y~1280. West edge 16 tiles from x 5120 (the Britannia sea edge) |
| A2 | 5264-5359 | 1048-1135 | 96x88 | strip; 24 tiles N of Jail, 21 S of Destard's region (y<=1023) |
| **C** | 6160-6639 | 1832-2279 | 480x448 | east area. N: ServUO "Underwater World" (6251-6472 x 1613-1812, not in pinned). S: ServUO TOL "BlackthornDungeon" (6151-6563 x 2301-2839, not in pinned) |
| D | 6496-6815 | 1552-1815 | 320x264 | east, 24 tiles E of Underwater World |
| E1 | 6584-7151 | 2456-2991 | 568x536 | east; S edge 50 rows above the 114/117 changed box |
| E2 | 6176-7151 | 3672-4079 | 976x408 | south of the changed box (53 rows) |
| E3 | 6672-7151 | 776-1143 | 480x368 | E of Blighted Grove / Painted Caves |
| E4 | 6832-7151 | 1728-2087 | 320x360 | |

Before the strict filter (no ServUO mask, no buffer) the strip also had 5520-5623 x 1416-1527 (104x112): **rejected**,
it lies inside ServUO's Trammel "Khaldun" rect 5381-5627 x 1284-1508 (pinned has Khaldun on Felucca only,
regions.json:766). A first pass of C ran to y 2303, 3 rows into Blackthorn; the strict C above stops at 2279.

Ranking:
1. **A (5136-5247 x 1128-1263, 112x136)**. Big enough for a small-to-medium dungeon. Inside the classic x 5120-6143
   dungeon strip, where every other Trammel dungeon interior lives, and inside the shard's fog-of-war grid (see
   caveat below). Neighbours are a GM jail and unused void. Keep the built content >= ~20 tiles from x 5120 so
   nothing on the Britannia side edge can see it (unverified whether a boat can reach x 5100-5119 at all).
2. **C (6160-6639 x 1832-2279)**. Room for a 120x120 or even 200x200 layout in the middle, e.g. 6320-6479 x
   1980-2139, which keeps >= 120 tiles from both ServUO rects. Best if the dungeon may grow later.
3. **D (6496-6815 x 1552-1815)** or **E3 (6672-7151 x 776-1143)**: same properties as C, smaller margins to content.
4. A2: small (96x88) and squeezed between Jail and Destard.

Caveat for x >= 6144: `ClusterFExplorationManager.cs:31-38` (and `ClusterFExplorationSync.cs:33-36`) size Trammel as
6144x4096; `:73` skips chunks with cx >= 768, so nothing breaks, but a dungeon at x >= 6144 never registers as explored
on the shard's fog-of-war map. Candidate A (x < 6144) does. Not verified: how the custom client draws x >= 6144.

Renders: `s2/overview_strip_x5120.png` (x 5120-7167, empty = navy, 114/117 diff = magenta),
`s2/overview_candidates.png` (radar colours, pinned Trammel regions yellow, strict candidates green, changed box
magenta), `s2/cand_A_strict.png` (A and A2 with Jail, Destard, Orc Cave), `s2/cand_C_D_strict.png` (C, D, E4).

---------------------------------------------------------------------------------------------------------------------
## 2. Abandoned building in New Haven for the entrance hole

**New Haven proper has no abandoned building.** The ML town region "New Haven" is 3416-3545 x 2480-2648
(`regions.json:1516-1526`, MinExpansion ML), not "x 3400-3700" as briefed. Its statics (`s2/cat_newhaven.png`) are
intact buildings; "ruined wall" there is only 27 tiles on the pier (3496-3519 x 2580-2586) and a few single tiles.

The ruins are **Old Haven**, directly east (3572-3760). Its town region "Haven" is `MaxExpansion: SE`
(`regions.json:1670-1684`), and pinned registers JSON regions only when Core.Expansion is within Min/Max
(`Projects/Server/Regions/RegionJsonSerializer.cs:60`), so on our EJ shard Old Haven has **no town region**: only
"Haven Island" (`NoHousingRegion`, 3314-3814 x 2345-3095, `regions.json:1499-1506`), which also covers all of New Haven.
So: no house placement anywhere on the island (good: nobody can house over the entrance), not guarded, and Young
protected (it is a BaseRegion with YoungProtected true, see section 3).

How I found the ruins: tiledata names of all 57,651 statics in 3380-3800 x 2420-2780; 622 "ruin*" statics
(597 "ruined wall"), clustered within 4 tiles into 28 clusters (`s2/ruins.json`). The big ones are all in Old Haven
south, 3585-3681 x 2574-2656. Building renders are top-down category maps (red ruined wall, grey wall, green door,
tan floor static, brown hatch roof, radar land underneath; squares: cyan = pinned decoration item, yellow = pinned
spawner, magenta = coordinate named in shard code or notes).

What else sits in Old Haven (all counted from the files):
- Pinned post-UOML spawners (active on EJ): Skeleton x7 at 3635,2625 range 15; Skeleton x10 at 3651,2627 range 15;
  Zombie x10 at 3625,2594 and at 3649,2591, range 15; a Healer at 3618,2614 (`Spawns/post-uoml/trammel/Outdoors.json`).
  So Old Haven south is undead-haunted already.
- Pinned uoml `Vendors.json`: 10 vendor spawners in Old Haven (Banker/Minter 3620,2617 etc.). The shard's
  `ClusterFOldHavenCleanup.cs` (admin command) deletes those vendors/spawners and Uzeraan's hub (`:23-70`).
  Whether it has been run on the live world is **not verified** (no world access in this task).
- Pinned `Decoration/Trammel/haven.cfg`, `_haven additions.cfg`, `uzeraan turmoil quest.cfg`, `collector quest.cfg`:
  pre-UOML Haven deco (doors, signs, forges, the ankh at 3606,2582), placed only by [Decorate. Live state unverified.
- Shard `ClusterFOldHavenSeeder.cs`: OldHavenMage and Drelgor spawners in the NORTH half (3556-3645 x 2457-2540,
  ranges 6-12, `:29-80`). Nothing south of y 2552.

Candidates (refs = pinned deco/spawn/teleporter points plus shard code/notes coordinates inside the crop):

| id | building | room / footprint | 40x40 crop refs | verdict |
|----|----------|------------------|-----------------|---------|
| **B1** | ruined "Second Bank of Haven" | room 3616-3625 x 2610-2621, wooden-floor land 0x040D z0 | 32 (23 deco, 5 shard, 4 spawn) | **top pick** |
| B2 | ruined provisioner's (Last Chance) | 3665-3680 x 2587-2600 | 50 (44 deco) | 2nd: heavily decorated, zombie spawner edge |
| B3 | ruined blacksmith compound | yard 3641-3659 x 2604-2630 | 31 | reject: Skeleton x10 spawner at its centre, Blacksmith vendor spawner |
| B4 | south-east shore block (inn, Albatross) | 3663-3681 x 2624-2656 | 82 (72 deco) | reject: roofed, crowded |
| B5 | Uzeraan's mansion | 3572-3613 x 2567-2608 | 83 refs inside | reject: intact, teleporter at 3613,2592, ankh, quest deco |

**B1 detail** (`s2/bldg_B1_second_bank.png`, ASCII from `t16`/inline script): walls (impassable flag 0x40, ruined
wall 0x0277-0x027C height 5, stone wall 0x57/0x58 height 20) on x 3615 (y 2610-2622), y 2622 (x 3615-3631),
x 3626 (y 2614-2621) and y 2609 (x 3610-3623). The room is **open at its north-east** (3624-3626 x 2610-2613) and has a
pinned deco `BarredMetalDoor` at 3626,2621 (`_haven additions.cfg:36-38`). Land z 0 throughout. 114 and 117 identical
for 3616-3626 x 2611-2621 (land and statics). 12 of 121 tiles carry statics. Inside the room:
- pinned spawners: Healer 3618,2614 (post-uoml, range 4) and Banker/Minter 3620,2617 (uoml);
- shard cleanup targets at 3617,2614 / 3622,2615 / 3621,2618 (coordinates of NPCs to delete, not items);
- pinned deco: door 3626,2620-2621; MetalGoldenChest 3627,2618 (`haven.cfg:241-243`), just outside.
- 30 interior 3x3 spots with no static and no ref. **Suggested hole: centre 3619,2620** (3618-3620 x 2619-2621),
  or 3623-3624 x 2617-2619. Within reach of the Skeleton spawner at 3635,2625 (range 15 reaches x >= 3620) and
  ~15 tiles from the Zombie range; Young are protected there, older players meet low undead on the way: fits a
  "something below the ruins" story but say so to Chase.
- Walk from New Haven bank (~3485,2572) to B1: ~136 tiles east. Not verified in game; walkability of the NE gap and
  any [Decorate items actually present must be checked on the test shard.

Overlap checks (all distances from B1, all clear):
- P16 mine camp: `ClusterFMineCampLayout.cs` / Institution seeder coordinates 3490-3520 x 2740-2760: >130 tiles.
- P19 registrar office: signs 3460-3463 x 2595-2597 (`ClusterFRegistrarOfficeSeeder.cs:35`), registrar 3459,2601: >150.
- P17: New Haven services seeder (forges, ankh, healer 3462,2559; `ClusterFNewHavenServicesSeeder.cs:186-193`) is New
  Haven only (IsNewHaven 3416-3545); P17's only Old Haven reference is the pinned ankh 3606,2582 (`cc-P17...md:49-51`),
  30 tiles north of B1.
- P22 pit thief: stool 3440,2558 (brief only, not landed): ~180 tiles.
- Quest NPCs / board: `ClusterFNewHavenSeeder.cs`, quest board 3502,2573 (`NewHavenQuestBoard.cs:69`), reset stone
  3501,2575, guild starter path (`ClusterFGuildStarterPath.cs:206-222`, nearest 3551,2463): none within 60 tiles.
- `CharacterCreation.cs:83` keeps a pre-ML "Haven" start at 3677,2625 (Bountiful Harvest Inn, old Haven): 58 tiles
  east of B1, in B4. Not verified whether that entry is reachable on EJ (line 114 gives New Haven 3503,2574).
- Pinned regions over B1: only "Haven Island" (NoHousing). "the Second Bank of Haven" NoHousing child (3615-3631 x
  2609-2623) is itself MaxExpansion SE (`regions.json:1759`), so not registered on EJ.
1,403 coordinate refs on the island were scanned (`s2/island_points.json`); the per-building lists come from that.

Renders: `s2/newhaven_overview.png` (whole island, radar + region outlines), `s2/newhaven_points.png`,
`s2/cat_newhaven.png`, `s2/cat_oldhaven_south.png`, `s2/ruin_secondbank_mapmaker.png`, `s2/ruin_eastblock.png`,
`s2/bldg_B1..B5_*.png` (40x40 or 50x50 crops).

---------------------------------------------------------------------------------------------------------------------
## 3. Pinned DungeonRegion and what a new dungeon region needs

`Projects/UOContent/Regions/DungeonRegion.cs` (33 lines), class `DungeonRegion : BaseRegion` (:5):
- `YoungProtected => false` (:21). Effect: `PlayerMobile.CheckYoungProtection` returns false when the mobile's
  region is a BaseRegion with !YoungProtected (`Mobiles/PlayerMobile.cs:4341-4350`), and that is the only gate
  monsters face (`Misc/Notoriety.cs:214-218`). So **in a DungeonRegion, monsters attack Young players**.
  `BaseRegion.OnEnter` sends `YoungDungeonWarningGump` to Young players entering any !YoungProtected region
  (`Regions/BaseRegion.cs:76-81`).
- `Entrance` (:23): used by `YoungDeathTeleport` (`PlayerMobile.cs:4398-4403`): a Young who dies in the dungeon is
  moved relative to the Entrance (then to the nearest Trammel death destination). Set it to the hole in B1.
- `AllowHousing => false` (:25).
- Light: `global = LightCycle.DungeonLevel` (:27-30) = 26 (`Misc/LightCycle.cs:15`).
- Stuck menu allowed except on Felucca (:32).
- Travel: DungeonRegion does not override `CheckTravel`; BaseRegion delegates to its parent (`BaseRegion.cs:171-175`).
  `SpellHelper.CheckTravel` (`Spells/Base/SpellHelper.cs:648-687`) blocks dungeons only via `IsFeluccaDungeon` (:733-737,
  Felucca only) and `IsMLDungeon` (:836, a fixed name list, `Misc/MondainsLegacy.cs:79-88`). So a new **Trammel
  DungeonRegion allows recall/gate in and out and Mark**. To forbid travel use `NoTravelSpellsAllowedRegion :
  DungeonRegion` (`Regions/NoTravelSpellsAllowedRegion.cs:6`, CheckTravel false for players :23-27).
- Other DungeonRegion checks in pinned (grep, 9 call sites): no campfires (`Kindling.cs:57`), boats cannot be placed
  (`BaseBoatDeed.cs:154`, `BaseDockedBoat.cs:164`), Solen ball (`BallOfSummoning.cs:199`), mushroom traps
  (`MushroomTrap.cs:38`), Exorcism (`Exorcism.cs:138`), escort names (`BaseEscortable.cs:862`).
- Young also lose treasure-level loot from kills (`BaseCreature.cs:2952-2955`, any region). Creatures can opt out of
  Young protection with `IgnoreYoungProtection` (`BaseCreature.cs:881`).

How regions are defined in pinned: one file, `Data/regions.json` (`RegionJsonSerializer.cs:98`), polymorphic on
`$type`; types must be registered (`Regions/RegionJsonRegistration.cs:9` for DungeonRegion). Example Trammel dungeon
entry: "Orc Cave" `regions.json:2746-2759` (`$type`, `Entrance`, `Map`, `Name`, `Priority`, `Area` [{x1,y1,x2,y2}],
`GoLocation`, `Music`). Optional `MinExpansion`/`MaxExpansion`, `Parent`, `RuneName`. Code-created regions also work:
`new X(...)` + `Register()`.

How our shard adds a region today: only in code (DespiseRegion, above), never via regions.json. Its comment records a
pinned quirk worth reusing: every region, JSON ones included, is constructed with `Dynamic = true`
(`Projects/Server/Regions/Region.cs:159-165`), so at equal priority the tie falls to list order; Despise uses priority
51 (`DespiseRevamped/Region.cs:45-55`). For the void candidates nothing else overlaps, so priority 50 is fine.

What the new dungeon needs (options, not a decision):
1. **A region over the interior**, registered in code from a shard script (the Despise pattern; keeps
   `Distribution/Data` untouched), or a new patch adding one JSON object to regions.json (no precedent in
   `server/patches`). Name it, set Entrance = B1 hole, GoLocation = arrival tile, Music, Area = the built rectangle.
2. **Type decides Young:** plain `DungeonRegion` = standard OSI behaviour: Young are attacked and get the warning
   gump. A Young-safe dungeon needs a shard subclass overriding `YoungProtected => true` (still dungeon light, no
   housing). That is a deviation from OSI and would go in `docs/fidelity-principle.md`. Note the shard already
   lengthened Young to "2 weeks of play" and removed the 450-skill exit (`server/patches/Account-young-duration.patch`,
   `PlayerMobile-young-time-only.patch`, cc-P18), so many dungeon visitors will be Young.
3. **Travel**: decide DungeonRegion (recall allowed) vs NoTravelSpellsAllowedRegion.
4. Teleporters both ways (hole in B1 -> interior; exit -> B1). Pinned's are items/`teleporters.json`; not designed here.
5. The B1 end stays in "Haven Island" (NoHousing, Young protected). If the hole area should be guarded or named,
   that is a further child region.

---------------------------------------------------------------------------------------------------------------------
## Not verified
- Live world state: whether [Decorate, `ClusterFOldHavenCleanup` and `ClusterFOldHavenSeeder` have run; what items
  and NPCs actually stand in B1 today.
- Walkability of B1's NE gap and the route from New Haven (statics-only reasoning; no client test).
- Client behaviour at x >= 6144 (custom client fog-of-war, minimap) and whether players at sea near x 5119 can see
  candidate A.
- ServUO Regions.xml rects in non x/y/width/height form were skipped (not counted).
- Expansion fields of Old Haven child regions other than "Haven" and "the Second Bank of Haven" (both SE-only).
