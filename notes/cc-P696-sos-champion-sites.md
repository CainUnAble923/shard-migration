# P696: Felucca champion sites on Siege of Sosaria

2026-10-27. Proposal for P685, S12 of [P673's swap plan](cc-P673-sos-swap-plan.md). Map and place names credit: **Siege of Sosaria Trammel Map 3.0 by Zigholtul**. All proposed placements are on **Map.Felucca**, using the SoS terrain chosen for both main facets.

Recommend retaining 14 altar locations, inspecting the three graded `moves`, and relocating LL06, LL07, and LL11 to option A below. Each relocation has an option B. Also replace LL08's ejection point, even though its altar can stay. These are proposed placements for P685 to validate in a private world. No server, map, spawn data, or live world was changed here.

## Evidence and meaning of the grades

Read the requested [geo-files.csv](cc-P669-tools/out/geo-files.csv) and [spots.csv](cc-P669-tools/out/spots.csv). `geo-files.csv` reports Trammel and our literals; it contains no `GenChamps.cs` row. The Felucca champion totals actually live in [felucca-summary.csv](cc-P669-tools/out/felucca-summary.csv). `felucca.py` grades the first Point3D of each generator entry, not its ejection point or whole spawn area. `spots.csv` supplies dungeon and town landmarks, not a named list of Lost Lands champion sites.

The working shard inherits pinned ModernUO's generator. No replacement for `GenChamps.cs`, `ChampionGenerator`, `ChampionSpawn`, `LLChampionSpawn`, or `DungeonChampionSpawn` was found under canonical `server/customizations/` and `server/patches/`. The miniature champion system is separate.

Source files read under `D:\UO\ModernUO-pinned`, verified at commit `d4531cd94b739613155225c234900de9f47d2c88`:

- `Projects/UOContent/Engines/CannedEvil/GenChamps.cs:31-54`: the 12 Lost Lands and five dungeon entries listed below, including ejection points.
- `Projects/UOContent/Engines/CannedEvil/GenChampEntry.cs:35-49`: an entry without a type randomizes it. LL01 through LL11 remain random. LL12 remains ForestLord. A proposed terrain theme does not assign a different boss.
- `Projects/UOContent/Engines/CannedEvil/ChampionSpawnInfo.cs`: the five dungeon types map to Neira, Barracoon, Rikktor, Semidar, and Mephitis; ForestLord maps to Lord Oaks.
- `Projects/UOContent/Engines/CannedEvil/ChampionSpawn.cs:190-193,819-842,1019-1070`: initial spawn rectangle, spawn sampling, and movement of platform and altar. The platform is at controller Z minus 20; the altar is at controller Z minus 15.
- `Projects/UOContent/Engines/CannedEvil/ChampionPlatform.cs:32-62`: the platform occupies a 5 by 5 footprint.
- `Projects/Server/Geometry/Rectangle2D.cs` and `Projects/Server/Maps/Map.cs:243-295`: rectangle bounds and average land Z. The initial rectangle is `[X-24,X+24)` by `[Y-24,Y+24)`, or 2,304 tiles.

The author's [Regions.xml](sos-author-data/Regions.xml) is reference data, not ModernUO configuration. Its **Trammel** facet has the SoS regions; its Felucca facet retains stock definitions. This proposal uses Trammel's SoS rectangles as the reference for future Felucca towns. Relevant regions include Ice Island, Papua Desert, Lost Lands Outskirts, Papua, Delucia, and the five stock dungeons. P669's go-spots confirm that Deceit, Despise, Destard, Fire, and Terathan Keep still exist; the Terathan champion-room spot is graded stock.

I reread the local map data through P481's data-only SoS copies at `D:\UO\shard-migration\notes\cc-P481-tools\scratch\sos\`, with vanilla Felucca and tiledata at `D:\UO\UltimaOnlineVanilla`. No third-party scripts were run. Sparse reads used the existing `scripts/mapbuild/uofiles.py` readers and P669 `geo.py` rules. The per-site result reproduces **11 unchanged, three moves, and three rework**.

- **Unchanged:** the land ID, land Z, and static sets in the surrounding 3 by 3 match stock Felucca. Retain the stock controller coordinates, subject to P685's normal runtime checks.
- **Moves:** something in that neighborhood changed, but the center passes P669's dry, static obstruction, and height checks. It can potentially stay at the stock spot. The word does not itself require relocation.
- **Rework:** the stock placement cannot be carried over as written. All three affected altars are still over dry ground, but the terrain height changed substantially.

The row lists behind every total are [stock-sites.csv](cc-P696-data/stock-sites.csv), 17 generator entries, and [candidate-sites.csv](cc-P696-data/candidate-sites.csv), six alternatives. Only these two CSVs and this note are deliverables.

## Complete placement table for P685

IDs follow source order separately within `LLLocations` and `DungeonLocations`. XYZ is the **invisible ChampionSpawn controller**, as stored in `GenChamps.cs`, not the visible altar or bare ground. Keep the existing spawn class, boss type, randomization, and activation rules.

`Open` is a conservative terrain screen over the initial 48 by 48 rectangle: dry tiles with neither impassable land nor an impassable non-surface static anywhere in the column. It is not a `CanSpawnMobile` result. All 17 stock altar centers have a screened-open 5 by 5 footprint. Dungeon rectangles naturally include walls and void; a low open count alone is not evidence that the altar should move.

| ID | Stock controller XYZ | Type and SoS setting | P669 grade | Stock spot usable? Proposal | Open / 2,304 |
|---|---|---|---|---|---:|
| LL01 | 5511,2360,42 | Random; western Ice Island | unchanged | Yes. Retain. | 1,925 |
| LL02 | 6038,2401,47 | Random; eastern Ice Island | unchanged | Yes. Retain; check the shoreline within the spawn rectangle. | 1,305 |
| LL03 | 5549,2640,16 | Random; Papua Desert | unchanged | Yes. Retain. | 1,611 |
| LL04 | 5636,2916,37 | Random; Papua Desert | unchanged | Yes. Retain; confirm the area remains outside Papua's final guard zone. | 1,509 |
| LL05 | 6035,2943,50 | Random; eastern Lost Lands, outside the author's named wilderness rectangles | unchanged | Yes. Retain. | 1,954 |
| LL06 | 5265,3171,105 | Random; Lost Lands Outskirts | rework | No at stock Z. Raw ground changed from 87 to -5. Use A: **5432,3220,19**; B below. | 1,353 |
| LL07 | 5282,3368,50 | Random; Lost Lands Outskirts | rework | No at stock Z. Raw ground changed from 28 to -60. Use A: **5324,3428,15**; B below. | 1,630 |
| LL08 | 5207,3637,20 | Random; Lost Lands Outskirts, beside the author's Delucia Orc Fort go-spot | moves | Yes, provisionally. Ground average is 0 and controller Z is 20. Retain altar; replace ejection point as below. Inspect fort access and props. | 1,975 |
| LL09 | 5954,3475,25 | Random; Lost Lands Outskirts southeast of Papua | unchanged | Yes. Retain; inspect the changed ejection neighborhood. | 2,008 |
| LL10 | 5982,3882,20 | Random; southeastern Lost Lands Outskirts | unchanged | Yes. Retain. | 1,810 |
| LL11 | 5724,3991,41 | Random; southern Lost Lands Outskirts | rework | No at stock Z. Raw ground changed from 22 to 0. Use A: **5768,4024,20**; B below. | 2,126 |
| LL12 | 5559,3757,21 | ForestLord / Lord Oaks; Lost Lands Outskirts | unchanged | Yes. Retain the fixed ForestLord type and woodland setting. | 2,094 |
| D1 | 5179,709,20 | UnholyTerror / Neira; Deceit | unchanged | Yes. Retain in Deceit. Inspect its surface ejection point. | 883 |
| D2 | 5557,827,65 | VerminHorde / Barracoon; Despise | moves | Yes, provisionally. Ground remains 45. Retain; verify the rebuilt room's usable floor and approach. | 571 |
| D3 | 5259,837,64 | ColdBlood / Rikktor; Destard | moves | Yes, provisionally. Ground remains 39. Retain; verify slopes and the changed surface exit. | 1,816 |
| D4 | 5815,1352,5 | Abyss / Semidar; Fire | unchanged | Yes. Retain in Fire. Inspect its surface ejection point. | 956 |
| D5 | 5190,1607,20 | Arachnid / Mephitis; Terathan Keep | unchanged | Yes. Retain in the stock champion room. | 1,251 |

Town checks are especially relevant for LL04 and LL09. Their centers are respectively 179 and 158 tiles from the nearest author Papua town rectangle. Their initial spawn rectangles have conservative gaps of at least 155 and 134 tiles. Dungeon-cell distances to towns elsewhere in the packed map are not travel distances and are not used as placement reasons.

## Two alternatives for each unusable stock placement

Option A is preferred for each row. Alternatives are mutually exclusive for that site. All six have 2,304 dry tiles in the initial spawn rectangle, a screened-open 25-tile platform footprint, and no overlap with an author TownRegion or GuardedRegion rectangle. They remain on the existing Lost Lands landmass, outside P673 S14's listed unfinished-area fences, and do not require opening an author's sealed dungeon.

Town distance is the smallest Chebyshev distance from the center to an occupied tile of any author Trammel TownRegion or GuardedRegion rectangle. The nearest town is Papua for LL06 and LL07, Delucia for LL11. `Area gap` subtracts 24 for a conservative clearance of the whole spawn rectangle. These are geometric distances, not measured walking routes or final S13 guard boundaries.

The suggested controller Z is the source-equivalent land average plus 20, so the platform origin sits at the local average ground height. P685 must inspect the assembled platform on slopes before accepting that Z.

| Site / option | Proposed controller XYZ | Author region and terrain | Open / 2,304 | Ground Z across area | Town distance / area gap | Reason and tradeoff |
|---|---|---|---:|---|---|---|
| LL06 A | **5432,3220,19** | Lost Lands Outskirts; dirt | 2,015 (87.5%) | -4 to 16 | 207 / 183 | Prefer this nearby open shelf, 167 tiles east of the old center. It keeps a wilderness encounter west of Papua and avoids the much deeper rebuilt terrain under the old altar. The platform footprint varies by 5 Z; check its seating and the route onto the shelf. |
| LL06 B | **5436,2868,54** | Papua Desert; sand | 1,827 (79.3%) | 27 to 47 | 227 / 203 | A dry desert alternative, 303 tiles from the old center, clear of town. The random encounter can keep its stock type selection here. It changes the local setting and has less open ground than A; use only if A's approach fails. |
| LL07 A | **5324,3428,15** | Lost Lands Outskirts; grass | 2,019 (87.6%) | -5 to 15 | 315 / 291 | Prefer this grassy shelf only 60 tiles from the old center, with a flat 5 by 5 core. It preserves the western wilderness setting and gives the spawn substantial separation from Papua. Check the surrounding terrace crossings. |
| LL07 B | **5416,3412,57** | Lost Lands Outskirts; grass | 1,954 (84.8%) | 34 to 52 | 223 / 199 | Another grassy shelf, 134 tiles east of the old center, with ample town clearance. It keeps a land encounter rather than moving the random site into a dungeon. Its 6 Z platform-footprint variation makes A the better first choice. |
| LL11 A | **5768,4024,20** | Lost Lands Outskirts; grass | 2,117 (91.9%) | 0 to 0 | 456 / 432 | Prefer the flat southern clearing, only 44 tiles from the old center. It keeps the remote southern wilderness setting and is far from Delucia. The spawn rectangle ends at y=4047, within the map. |
| LL11 B | **5640,4020,20** | Lost Lands Outskirts; grass | 2,077 (90.1%) | 0 to 0 | 328 / 304 | A second flat southern clearing, 84 tiles west of the old center. It has slightly less open ground and is closer to Delucia than A, but still has a large town buffer. |

The three preferred spawn rectangles are mutually disjoint and do not overlap another retained champion's initial rectangle. Their exact half-open bounds are in the candidate CSV. Open counts allow rocks, trees, and other blocked tiles around the clearing; they do not claim that every tile in the rectangle can spawn a mobile.

## Ejection points travel with the proposal

P669 did not include these second coordinates in its champion total. Regrading all 17 ejection points gives **nine unchanged, six moves, and two rework**, listed beside their original XYZ in the stock CSV. One rework point belongs to LL07, whose altar is already being relocated. The other belongs to LL08, whose altar can stay.

Use the following proposed ejection XYZ when selecting an alternative. Each has a screened-open 3 by 3 neighborhood and is outside its own proposed spawn rectangle. EjectMap stays Felucca. Their routes back to the altar remain unverified.

| Site / option | Proposed ejection XYZ |
|---|---|
| LL06 A | 5423,3183,-3 |
| LL06 B | 5465,2869,34 |
| LL07 A | 5296,3428,-5 |
| LL07 B | 5454,3402,37 |
| LL11 A | 5768,3996,0 |
| LL11 B | 5640,3992,0 |
| LL08, retained altar | **5209,3609,0** |

LL08's old eject point is `5263,3687,0`. Its SoS raw land Z is -20 and average Z is -19, so carrying over the old coordinate would leave it above the new ground. The proposed replacement has flat ground at 0, an open 3 by 3, lies outside LL08's rectangle, and is 323 tiles from the author's Delucia town bounds.

For retained altars, inspect the six `moves` ejection points: LL06, LL09, LL11, D1, D3, and D4. LL06 and LL11 receive replacements above. The others can provisionally retain their stock XYZ: LL09 `6013,3529,0`, D1 `4111,432,5`, D3 `1176,2637,0`, and D4 `2923,3406,8`. D4's eject point falls inside the author's Serpent's Hold town region. This is an exit into town, not a champion spawn inside a guard zone; verify a safe landing without moving the Fire encounter into town.

## What P685 still needs to prove

This proposal establishes coordinates, terrain screens, themes, and town separation. It does not establish runtime walkability. P685 should:

1. Retain the 14 stock altar coordinates and apply the three option A relocations, their ejection points, and LL08's ejection replacement. Use B only if the corresponding A fails the checks below. Preserve class, boss selection, stock initial area size, and activation behavior.
2. Verify each assembled 5 by 5 platform, visible altar, and ejection landing against actual SoS map data. Confirm access onto the platform, particularly the sloping LL06 and LL07 candidates. Do not treat a dry tile or this note's Z as a runtime collision proof.
3. Sample actual spawn locations using `Map.CanSpawnMobile` and check that the reachable floor supports the encounter. `GetSpawnLocation` tries 20 random tiles and then falls back to the controller location, so a dry center alone does not prove a usable spawn area. Pay particular attention to Despise's confined room, Destard's slopes, and the Lost Lands terraces.
4. Check every spawn area against S13's final Felucca guard zones and S14 fences, not just this proposal's author rectangles. Check non-overlap again after any fallback or adjustment. Do not enlarge a dungeon spawn rectangle into adjacent packed cells.
5. Walk the approaches and ejection return routes in the throwaway private world, then run S12's altar facts and normal build gate. Coordinate the Despise and Destard room checks with S8. S15 owns the broader world connectivity proof.

No code tests or build were needed for this notes-and-data task, and no tests were added. No runtime, client, final guard-zone, path connectivity, or completed encounter verification was performed. Haven was not contacted; no containers were built or started; no branch, commit, merge, or push operation was performed. No file over 5 MB was created.

Final review: all 17 source entries appear once in the placement table and stock CSV; each of the three rework entries has exactly two alternatives. The candidate CSV matches the proposed coordinates and measurements. Preferred spawn rectangles do not overlap one another or a retained site's rectangle. All six candidate rectangles have no author town/guard intersection; all six proposed exits are outside their own rectangle. Relative links resolve, there are no em dashes, and `git diff --check` is clean. The code work copy is unchanged; the only final additions are this note and its two CSVs, each below 16 KB.

Ran the standing progress report with this work copy's path overrides and `--dry-run` under Windows PowerShell 5.1. It completed. An unrelated tooling issue, ours: `tools/progress.py:722` writes `tools/progress.json` inside `build()` before `main()` honors `--dry-run` at line 737. That changed the snapshot despite the flag. The work copy started clean, so I restored that generated file to its starting contents and verified the final status contains only this task's notes and data. The tool was not changed in this proposal task.

P696 DONE
