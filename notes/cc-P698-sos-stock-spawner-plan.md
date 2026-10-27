# P698: stock spawners on Siege of Sosaria land

2026-10-27. Plan for P681 (S9), with S7, S8, S10, S14, S18 and S19 handoffs. Map and place names credited to **Zigholtul, Siege of Sosaria Trammel Map 3.0**. Chase's choice to replace both Trammel and Felucca is the starting point. Data and notes only.

## What S9 should do

Keep stock populations where their purpose and footprint still fit. Move town services into the matching trade building in the same town. For wild encounters, wildlife, crops and reagents, search matching habitat within 20 tiles of the old home, then drop the placement if the search fails. Keep sea creatures in suitable water. Give new land to S10's coverage survey; hold closed land and new dungeons for S19 and S18.

This is a disposition plan, not an import file or verified destination coordinates. Every keep is provisional until S9 checks its full footprint. Every move names a search area and fallback. No destination tile was checked here.

Files:

- [spawner-plan.csv](cc-P698-tools/spawner-plan.csv): all stock records, sorted by area, facet, source and source array position, followed by new-area requests.
- [area-summary.csv](cc-P698-tools/area-summary.csv): stock keep, move and drop totals per area and facet.
- [source-summary.csv](cc-P698-tools/source-summary.csv): the full list of 68 source files beside their row counts, grades and dispositions. Paths are relative to pinned Distribution/Data.

## Counted scope and source evidence

The read-only source is D:/UO/ModernUO-pinned. Its HEAD and this code work copy's docker/uo/Dockerfile:3 both name d4531cd94b739613155225c234900de9f47d2c88. All 68 spawn JSON files in source-summary.csv were parsed in full. This is the shard's pinned spawn data, not server/uo/ or live-world contents.

| Facet | Raw stock records | Keep | Move | Drop |
|---|---:|---:|---:|---:|
| Trammel | 2,182 | 1,289 | 810 | 83 |
| Felucca | 2,122 | 1,308 | 813 | 1 |
| Both | 4,304 | 2,597 | 1,623 | 84 |

These count spawner records, not creatures or entries. A record may mix creatures and chests. Several records may legitimately share coordinates. Do not merge or delete by coordinates.

P669 inputs read under cc-P669-tools/out: geo-files.csv, geo-summary.csv, geo-points.csv, spots.csv, felucca-summary.csv, new-islands.csv, stock-regions.csv, areas.csv, places.csv, and the header/closure evidence in unfinished.csv. The requested file and summary exports were reconciled against the point export and source JSON. The author references were sos-author-data/Regions.xml, its location evidence through spots.csv, and SOURCE.txt. cc-P673-sos-swap-plan.md supplies S9's search rule, closure boxes and ownership.

P669 includes four legacy Trammel files that the shard does not import:

| Source under Spawns/uoml/trammel | Raw records |
|---|---:|
| Outdoors.json | 9 |
| TownsLife.json | 3 |
| Vendors.json | 21 |
| WildLife.json | 12 |
| Total | 45 |

server/customizations/ClusterFStockSpawnData.cs:17 defines ShardFolders as post-uoml and shared. Trammel therefore has 2,137 raw records in those sets. Existing hooks exclude 30 creature-only Despise records and the Old Haven crier. Two mixed Despise records keep chests only. That leaves 2,106 potentially imported Trammel containers and 2,122 Felucca containers before this plan's eight eligible-source drops. Import eligibility does not establish what exists in a save.

Of 84 drop rows, 76 preserve current policy: 45 legacy records and 31 hook exclusions. Eight are new recommendations: six Old Haven surface undead records and one spawner per facet in the proposed northeast snow closure. Keep/move candidates total 4,220 eligible-source containers.

## P669 evidence and its limits

cc-P669-tools/geo.py, Grader.grade, compares a home's tile and its 3 by 3 neighborhood. It does not check the whole spawn or walking range, current NPCs, paths, trades, fences, town safety or encounter purpose.

| Direct Trammel grade | Raw records | Meaning |
|---|---:|---|
| unchanged | 1,341 | Local land and statics match stock. Keep candidate unless purpose or import policy overrides it. |
| moves | 496 | Neighborhood changed and P669's home check passes. Inspect; final coordinates may remain the same. |
| rework | 345 | Water, void, impassable static or land Z change over 5. Search for a suitable home. The export does not distinguish the cause. |

The Trammel rows reproduce geo-summary.csv and every stock-spawner row in geo-files.csv. Plan decisions differ because population purpose and existing exclusions also matter.

**Felucca per-record grades are unverified.** felucca.py exported only an aggregate: 1,311 unchanged, 505 moves, 306 rework. It wrote no Felucca point file. No maps or graders were run here.

For 2,057 Felucca homes, P669 has a Trammel point at the same x,y. Their p669_basis is Trammel proxy. Proxy grades total 1,309 unchanged, 440 moves and 308 rework. These do not replace Felucca's grades: its stock baseline and Z may differ.

The remaining 65 say Felucca summary only and unverified, all in the move/survey queue:

| Source under Spawns/shared/felucca | Homes without a proxy |
|---|---:|
| Khaldun.json | 47 |
| Vendors.json | 15 |
| Graveyards.json | 1 |
| PaintedCaves.json | 1 |
| SeaLife.json | 1 |

Felucca keeps also need independent S9 movement and footprint checks. No per-record grade was inferred from an aggregate.

## Reading the spreadsheet

source plus source_row identifies the original JSON array element, starting at 1. guid, x,y,z, entries, home_range, walking_range and spawn_bounds are copied source values. Blank range means absent, not zero. effective_entries is filled only for the two mixed Trammel Despise records whose hook strips creatures. population_kind separates services, civic NPCs/props, animals, wild encounters, resources, sea life and dungeon content.

p669_csv_line counts the header in geo-points.csv. For Felucca it identifies Trammel proxy evidence; it is blank without a proxy. import_status distinguishes source eligibility from exclusions.

- Keep: retain source identity and purpose, pending home, range, Z and region checks.
- Move: inspect search_area. Author markers are places to look, not verified spawn points. For wild content use a maximum Chebyshev distance of 20 from the original home, with neither coordinate changing by more than 20. Do not chain several moves.
- Drop: leave this placement out of generation. Preserve existing hook/folder exclusions. New drops are recommendations for the swapped world, not live deletion instructions.

New-area rows have record_kind=new_area, decision=add and facet=Both. They request a coverage survey, not a fixed number of new spawners.

Area labels are planning groups. Dedicated dungeon files retain their dungeon identity. Civic groups use named stock town rectangles, then the nearest stock town within 500 tiles; Haven's old and new settlements form one group. Wild groups use author region rectangles, then stock bounds or broad sectors. Sea sectors are 1,024 by 1,024 tiles. area_basis exposes the method. A label establishes neither reachability nor final server-region membership.

## Area priorities

### Town services first

Find each trade's building and reachable floor. A dry point alone is insufficient. Preserve essential roles instead of dropping the only banker, healer, smith or provisioner. S9 must reconcile the stock roster with S7/S10's seeders.

- **Haven:** S7 moves the safe start into the author's living town. Search the Second Bank at 3628,2608,0, smithy at 3647,2617,0, docks at 3650,2653,0, A Stitch In Time at 3672,2602,0 and farm at 3722,2647,20. These are P669 author markers, not checked placements. Reconcile stock services with S7's custom NPCs. Keep legacy uoml out. Drop the first six records of post-uoml/trammel/Outdoors.json, the old ruin undead, from the surface plan. S7 must reconcile apprentice kill quests, Drelgor, the retired ruin population and Rootdeep access before applying this recommendation. ClusterFOldHavenSeeder.cs still names Drelgor and stock undead. Keep the excluded crier GUID excluded; S7 owns any new crier.
- **Moonglow:** search the bank at 4470,1177,8 and docks at 4406,1045,-2, then match each affected trade. Check the cemetery and any animal enclosure separately.
- **Magincia:** inspect rebuilt shops and floor heights. Bank 3730,2161,20 and docks 3675,2259,20 are search anchors.
- **Buccaneer's Den:** search bank 2731,2193,0, healer 2707,2153,0, smith 2635,2089,0 and provisioner 2745,2250,0. Preserve Felucca's unguarded rules.
- **Britain, Cove, Minoc and Vesper:** retain unchanged shop candidates, then inspect affected trades, doors, bridges and mines. Keep Vesper's island access in the review. Britain cemetery and the northern keeps are separate concerns.
- **Jhelom, Skara Brae, Trinsic, Serpent's Hold, Yew and Papua:** many keep candidates, still subject to full footprint and core-service checks.
- **Wind:** the Daemon, Lich/LichLord and Dragon/Drake entries in TownsLife.json are Wind cave encounters. Keep them in that encounter space, away from civic services.
- **The Heartwood and Sea Market:** reconcile existing stock first. Sea Market already has 34 post-uoml vendor records on each facet; its author-region request must not produce a second roster.

The complete area counts, including separate outskirts, fields, cemetery and island groups, are in area-summary.csv. The stock ledger lists every affected service by source and GUID.

### Wild land, farms, reagents and graveyards

The large rebuild queues include Britain Forest South, Yew Forest, Lost Lands Outskirts, Britain Forest North, Vesper Forest, Huntsman's Forest, Covetous Forest and Trinsic Jungle. Work the exact rows rather than replacing a whole forest.

Search matching terrain, elevation and encounter purpose within 20 tiles. Keep entry mix, count, probabilities, delays and range unless a measured placement constraint calls for a separate change. A dry roadside is not a substitute for forest, swamp, a faction camp or a cemetery. On search failure drop that stock placement; S10 fills wider new habitats separately.

Wild homes inside author settlement rectangles at Hammerhill, Kameron Kove, Elmhaven and Fort Yondall move even if local geometry might allow them. Look outside civic space within 20 tiles; drop on failure. S10 supplies the intended town population.

Keep crops in matching planted fields, livestock in pasture and reagents in their original habitat. Coordinate Haven's fields with S7. Do not change resource species just to pass a placement check.

Cemeteries have separate groups. Check Moonglow's containment. The graveyard-file home at 3407,2652 is on Haven island, not the distant Nujel'm cemetery. Search suitable cemetery ground outside civic space within 20 tiles, or drop it and hand the quest dependency to S7.

### Stock dungeons

Keep encounter and chest identities in the same dungeon. Search the same room or floor within 20 tiles. Coordinate missing rooms with S8; do not move old stock content into unrelated author caves.

- **Trammel Despise:** preserve ClusterFDespiseStockSpawns.Admit and ImportSpawners-despise-exclusion.patch. Of 43 raw records, 30 remain excluded, 11 are chest-only, and two mixed records retain only chests. The plan keeps six chest containers and moves seven. **Felucca Despise** retains all 43 classic records and full entries, with 27 keep candidates and 16 moves.
- **Destard:** three keep candidates and 25 moves on each facet. Prioritize rebuilt floors and dragon encounter space.
- **Covetous, Orc caves, Wrong, Solen hive and Terathan Keep:** check affected rooms, Z and range. S8 owns separate revamped generators and artifacts.
- **Shame, Hythloth, Ice, Deceit and other largely retained rooms:** keep candidates still need footprint checks. No custom generator changed here.
- **Khaldun:** all 47 Felucca records require direct survey because no per-home Felucca evidence or Trammel proxy was exported. Retain their Khaldun identity.
- **Blackthorn and author dungeons:** S8 owns the Blackthorn generator shutdown. The raw stock files here do not inventory that custom generator. S18 owns author dungeon populations. Keep those dungeons sealed until that work lands.

### Sea life and closed land

SeaLife.json contains 114 Trammel and 115 Felucca records. Each has 69 keep candidates; Trammel has 45 moves/surveys and Felucca 46. P669 uses dry-land grading, so rework does not prove invalid water. A sea keep also needs its much larger range checked against new shore.

Search connected suitable water within 20 tiles, clear of new land and working docks. Drop if suitable local water is gone; S10 supplies new coastline coverage. Validate each entry's movement needs rather than applying a universal dry-land assertion.

P673 proposes these S14 closure boxes, copied here as inclusive limits:

| Closure | x range | y range |
|---|---|---|
| Rooster island | 2840-3039 | 1324-1523 |
| Northeast snow isles | 4224-4479 | 256-767 |
| Bare land east of Haven | 3072-3199 | 2304-2559 |
| Echoback/Darkfathom edge cells | 4096-4223 | 2560-2815 |
| Glimmerwood seam cells | 2688-2943 | 2688-3071 |

One Outdoors.json home per facet falls in the northeast snow box: Trammel source record 282 and Felucca record 279. Both are dropped for 1.0. S19 can restore coverage after repair. These are proposed boxes, not verified implemented fences.

Ranges can cross closures even when homes are outside them. Such overlap is unverified here and must be checked by S9 with S14. Sea travel offshore does not authorize creatures leaking onto closed shore.

## New-area requests for S10

There are **107 requests**: 22 named wild coverage surveys, 14 settlement-region reconciliations, five keep surveys, 65 newly dry island components and one combined unfinished-snow/Haven-edge hold. They overlap. Do not add their areas or populations together. Clip actual region unions, subtract towns and fences, and subtract retained/moved stock coverage first.

The 14 settlement regions are Valunstead, Hammerhill, Kameron Kove, Elmhaven, Kettleburg, Fort Yondall, Elandrim Nur Shaz, Plunderers Peak, Red Baron Stronghold, Red Dagger Keep, Sea Market, Seraphim Peak, Skaddria Naddheim and Viligant Valley. The first six are P673's S10 town list. The others are author XML names needing a purpose and stock-coverage check, not evidence that all are new safe towns. Vendor suggestions are conditional on that review.

The five keep requests are Fort Whitestone, Castle Dunbain, Fort Stormhammer, Tigerclaw Fortress and Khalahandra Keep. Survey a small garrison or townsfolk roster consistent with P672/S10's quest allegiance. Keep generic hostiles out of civic paths.

Wild surveys prioritize Nujelm Desert and Moonglow Forest on the new continent, Glimmerwood, Dragonstorm Isle, Isle of Colossus, Isle of the Avatar and new island groups. The other named forest/Lost Lands requests cover gaps after stock changes; no request claims its entire region is empty.

### What the 65 island components mean

new-islands.csv has 65 rows with verdict new, totaling 465,664 dry tiles. Each has one request keyed by its P669 component id and box.

- **59 surface components, 429,744 dry tiles:** candidate S10 island surveys, including small components around keeps. Connected dry land does not prove a playable destination.
- **Six dungeon-strip components, 35,920 dry tiles:** ids 357, 370, 349, 365, 348 and 395, all with x at least 5120. Reserve for S18, not accessible sea-island populations.
- Surface components whose boxes intersect a proposed closure are held for S19. The CSV names the intersection. A box intersection is a conservative flag, not proof that every tile is fenced.
- An author dungeon entrance on an island needs an exterior population survey and an S18 seal handled separately. It does not authorize spawning inside.

P669 exported no per-island biome classification. Unnamed components therefore get conditional biome families instead of invented terrain labels.

### Creature families and level bands

These are S10 design suggestions, not measured difficulty or changes to creature stats. **B0** means noncombat fauna/civic life. **B1** targets early solo play, roughly 30-60 main combat skill; **B2** developing solo play, roughly 60-90; **B3** veteran play, roughly 90-120 with suitable equipment. Skill alone does not predict a fight. Tune placement and density in play while retaining stock behavior.

| Biome/use | B0 | B1 | B2 | B3, isolated from towns and travel |
|---|---|---|---|---|
| Forest/grass | Rabbit, Hind, GreatHart, Bird | TimberWolf, GiantSpider | Ettin, Troll, Corpser | Reaper after review |
| Jungle/swamp | Bird, BullFrog | Alligator, GiantToad | Lizardman, GiantSerpent | BogThing, SwampTentacle |
| Desert | DesertOstard in suitable safe habitat | Scorpion | GiantSerpent, Mummy | Efreet in remote pockets |
| Snow | Walrus; other fauna after behavior check | WhiteWolf | PolarBear, FrostTroll, IceSerpent | SnowElemental |
| Rock/lava | Only supported noncombat fauna | Outer encounters after survey | LavaLizard, LavaSerpent, HellHound | FireElemental |
| Ruins/graveyard | None in active combat space | Skeleton, Zombie | Ghoul, Wraith | Lich, LichLord |
| Sea/shore | Dolphin, SeaHorse | Safe coastal fauna, no default hostile | SeaSerpent | DeepSeaSerpent, Kraken away from docks |
| Settlements/keeps | Vendors, healers, guards, townsfolk | Low-risk wildlife outside civic paths | Quest-specific exterior only | No automatic veteran population |
| Lost Lands pockets | Suitable ostard habitat | Local outer wildlife | Stock Ophidian/Terathan families | Stronger stock tiers in matching remote camps |

Named creature examples above occur in the parsed stock spawn entries. This establishes stock data precedent, not runtime type resolution or successful spawning. Use existing Outdoors.json, WildLife.json, LostLands.json, Graveyards.json, Ice.json, Fire.json, SeaLife.json and matching dungeon mixes as templates after surveying terrain. Do not infer snow from latitude, swamp from a place name, or a boss arena from island size.

| Area | Suggested initial direction |
|---|---|
| Nujelm Desert | B0/B1 town approaches, B2 interior, sparse B3 only after route review |
| Moonglow Forest | B0/B1 roads and services, B2 wild pockets |
| Glimmerwood | B0/B1 edges, B2 interior; hold fenced seams; B3 only after access review |
| New snow isles | Hold unfinished paste; B0/B1 coast and B2 interior after S19 |
| Dragonstorm/unnamed islands | Survey biome first; sparse B0/B1, B2 inland if space supports it |
| Isle of Colossus/Stone Burrow exterior | B0/B1 travel and mine approach, B2 away from it; dungeon stays S18 |
| Isle of the Avatar | Survey forest/volcanic pockets; B1/B2 exterior, remote B3 where supported |
| Echoback/Darkfathom/Dunbarrow | Leave closed parts empty; choose coast/swamp/rock/lava only after survey |
| New towns/keeps | Core services and allegiance first; B0 civic space |

Do not transplant a full stock spawner count onto every island. S10 needs usable area and retained coverage, then a density comparison per 100 usable dry tiles against matching stock habitat. Neither usable area by biome nor safe density was measured here.

## S9 implementation handoff

1. Filter record_kind=stock. Preserve uoml exclusion and existing hooks. Match source and GUID, preserving stacked records and source settings.
2. Join S7's Haven roster and S10's settlements. Prove banker, healer, blacksmith and provisioner coverage at usable public locations for every stock town on each facet. A role can come from an owning seeder; avoid duplicates.
3. Inspect moves by area, services first. Verify trade, reachable floor and home. Walk the wild 20-tile search and record chosen coordinates or final drop reason. Keep a source-to-destination/drop ledger.
4. Check every keep/move with actual movement and item-fit rules over its intended spawn and walking footprint. Move rectangular spawn_bounds with the room/field, not x,y alone. Check Z, doors, habitat, guard/region rules, fences and seals. Aquatic and mixed item/mobile records need entry-specific checks.
5. Check Felucca independently, including all 65 homes without proxies. Preserve classic Despise and facet rules. Shared terrain does not authorize overwriting Felucca GUIDs or entry mixes with Trammel data.
6. Keep author dungeons sealed and closure interiors empty. Check range overlaps; give S10 retained coverage before adding new populations.
7. P681 owns executable facts and docker/uo/build.sh, with new tests seen failing first. This task adds no persistent tests or code.

## Verification and limits of this run

- All 4,304 raw records have one stock row with copied identity and footprint data. Trammel's 2,182 match P669's point sequence per file and its file/overall grade counts. Felucca's 2,122 were inventoried independently.
- Area/source summaries reconcile to the ledger. All 65 new-component ids and their boxes/dry counts are represented once each as island requests. Other coverage requests intentionally overlap them.
- Artifact validation was first observed failing because spawner-plan.csv did not exist, then passed after writing and reviewing it. Checks cover source identities, GUIDs, coordinates, entries and footprint copies; P669 point/file counts; dispositions; area/source totals; all 65 island requests; existing exclusions; aquatic validation wording; stock creature examples; file size and absence of em dashes. This checks data completeness, not game behavior. Lane tests: none; no server tests added.
- Unverified: actual map tiles, destination Z, paths, complete walkable ranges, island biome, building trade, implemented fences, live NPCs/saves, runtime type resolution and spawn success. No map files were read.
- Source behavior read in this code work copy: ClusterFStockSpawnData.cs, ClusterFDespiseStockSpawns.cs, ClusterFOldHavenStockSpawns.cs, ClusterFOldHavenCleanup.cs, ClusterFOldHavenSeeder.cs and ImportSpawners-despise-exclusion.patch. Custom generator edits remain S7/S8 work.
- tools/progress.py --dry-run ran with SL_SHARD set to this work copy. It reported 1,676 customization files, 176 patch files, and 1,801 tests in 264 files, plus existing review/play-test backlog entries. Despite its dry-run label, build() writes tools/progress.json before main() checks the flag. That incidental rewrite was restored byte for byte to the clean starting version. No progress-tool change is delivered in this notes-only task.
- No Haven connection, Docker operation, build, deployment, account action, commit, merge, push or branch change. The code work copy and docs/ are unchanged. Delivered files are below 5 MB. No scratch code is delivered.

P698 DONE
