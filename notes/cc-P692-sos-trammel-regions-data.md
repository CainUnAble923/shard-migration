# P692: SoS Trammel region data for P676 (S3)

Prepared 2026-10-27. Data and notes only. Credit: Siege of Sosaria Trammel Map 3.0 by Zigholtul. The region geometry and go-menu points come from his supplied server data. Stories and gameplay additions are not part of this task.

The candidate dataset is [cc-P692-tools/trammel-regions.json](cc-P692-tools/trammel-regions.json). It uses pinned ModernUO's flat region array, with native `$type`, `Map`, `Name`, `Priority`, `Area`, `Parent`, `Music`, `Entrance`, `GoLocation`, `RuneName`, `NoLogoutDelay` and `GuardsDisabled` properties where applicable. It is handoff data for P676, not a verified replacement for the running regions file. No server file was changed.

## Scope and measured inventory

The output has 198 records and 1,182 rectangles: 150 author Trammel records, one proposed New Haven town record, and 47 stock candidates. All 150 author records, including unnamed children, have a row in the mapping below. No nonempty author Trammel region was dropped. Five zero-area acid-river rectangles were removed because they contain no tiles; their original attributes and indices are in [omitted-properties.json](cc-P692-tools/omitted-properties.json).

The 198 records classify as 50 town, 58 dungeon and 90 wild records. The town count includes inn children, not 50 distinct settlements. `TownRegion` supplies guards, so there are no separate `kind: guarded` records yet. The author supplied no Trammel `GuardedRegion` entries. Moongate guard regions await S4's approved destinations.

The input and output file lists for these counts are:

| File | What it accounts for |
|---|---|
| `sos-author-data/Regions.xml`, Trammel facet | 150 author records, 1,128 source rectangles |
| `cc-P692-tools/trammel-regions.json` | All 198 proposed native records and their provenance |
| `cc-P692-tools/author-mapping.csv` | Every author Trammel record, 150 rows |
| `cc-P692-tools/stock-mapping.csv` | Every pinned Trammel record, 145 rows, in the same order as P669 stock-regions.csv |
| `cc-P692-tools/sosaria-mapping.csv` | Every record of the separate Sosaria facet, 132 rows |
| `cc-P692-tools/locations-review.csv` | All 410 go-menu points, with candidate containing regions |
| `cc-P692-tools/areas-review.csv` | All 73 P669 connected-change boxes and candidate intersecting regions |
| `cc-P692-tools/geometry-review.json` | Source go-point discrepancies and peer town overlap intersections |
| `cc-P692-tools/omitted-properties.json` | Five removed zero-area rectangles and two entrances with unknown Z |
| `cc-P692-tools/source-inventory.json` | Exact input file list, byte sizes and SHA-256 fingerprints |

There are 85 records with known music and 45 with an entrance point. Missing music is explicitly marked unknown in `review`. Missing entrances remain absent, rather than being guessed. A recorded entrance or go point is an author reference, not a proof that a player can stand there.

## Native format and behavior

The source tree is `D:/UO/ModernUO-pinned`, verified at `d4531cd94b739613155225c234900de9f47d2c88`. Relevant source files are:

- `Distribution/Data/regions.json`: the existing flat array, including Trammel's 145 records.
- `Projects/Server/Regions/RegionJsonSerializer.cs:58` and `:98`: registers each deserialized region and loads `Data/regions.json`.
- `Projects/Server/Json/Converters/RegionByNameConverter.cs:75`: resolves Parent by an already registered name and map. Parents precede children in this file.
- `Projects/UOContent/Regions/RegionJsonRegistration.cs`: all output runtime types are registered here.
- `Projects/Server/Regions/Region.cs:126`: priority 50 is the normal default; MinZ is -128 and MaxZ is 128. `CompareTo` at line 231 sorts by priority, then child depth.
- `Projects/Server/Json/Converters/Rectangle3DConverter.cs:152`: an omitted Z range becomes -128 through exclusive 127, not 128. Author rectangles therefore have explicit Z endpoints.
- `Projects/UOContent/Regions/TownRegion.cs:5` and `GuardedRegion.cs:33`: TownRegion inherits GuardedRegion, and GuardsDisabled controls guard response.
- `Projects/UOContent/Regions/DungeonRegion.cs:21`: dungeon rules remove young protection, prevent housing and set dungeon light. They do not themselves refuse travel.
- `Projects/UOContent/Regions/BaseRegion.cs:171`: CheckTravel delegates to a parent or allows travel.
- `Projects/UOContent/Regions/NoTravelSpellsAllowedRegion.cs:26`: MondainRegion's parent blocks player travel spells. It is broader than a recall-in-only restriction.
- `Projects/UOContent/Spells/Base/SpellHelper.cs:639`: checks both current and destination region travel rules.

ServUO's `Server/Region.cs:1284` and `:1658` establish the XML conversion: zrange defaults to -128 through exclusive 128, per-rectangle zmin/zmax override it, and x2 = x + width, y2 = y + height. No extra tile is added to XML endpoints. P673's inclusive New Haven envelope is separately converted by adding one to its east and south edges.

`kind`, `source`, `provenance` and `review` are handoff metadata. `kind` is town, guarded, dungeon or wild; `$type` is the real registered class. `source` is author, stock kept or ours. Per-field provenance records the cases where author geometry uses stock music or our class/priority policy. P676 should strip those four metadata properties when preparing the upstream JSON patch. Keep `$type` first in every record. Preserve the metadata in this notes artifact for credit and review.

Guard rules are explicit `GuardsDisabled: false` for author towns and their town inn children. Buccaneer's Den and its inn have `true`, preserving the author's unguarded town. The native Trammel default guard is WarriorGuard; AllowReds follows Core.AOS. No custom guard NPC, patrol policy, murderer rule or Felucca rule is invented here. The existing shard GuardedRegion witness patch remains a separate concern.

Native BaseRegion inn children would mask some direct guard behavior. Town inn children therefore use TownRegion, matching the shape of pinned's inn data. The two generic children inside the Palace of Paroxysmus use MondainRegion to preserve their parent's dungeon light and travel restrictions. Named parents make those relationships explicit.

Wild parent regions use priority 10 so their large forest and island boxes do not mask towns or dungeons at 50. Stock cave, field and entrance-fence candidates use 20. Stock farm TownRegion entries become independent BaseRegion entries: they keep a name for consumers, but cannot extend an obsolete guard zone through a parent link. Town guards still take precedence where the new town actually covers a field. These are our proposed policies and need P676 review.

Special damage areas map to the registered PoisonedTreeRegion, AcidRiverRegion, CrystalFieldRegion and IcyRiverRegion classes at priority 60. Those pinned classes still have TODO damage-boost implementations. Converting their geometry does not implement those effects. CrystalField's XML spawning entry, object 1001 CrystalFieldTele, has no equivalent region JSON spawning property and is not converted into a region property. P676 and S6 must account for the object separately.

The surface Swamp of Desolation uses NoHousingRegion, classified wild, instead of the author's DungeonRegion. That preserves a housing fence while avoiding underground light and a dungeon young-player warning in a surface swamp. JailRegion and GreenAcresRegion retain their actual specialized classes even though their broad taxonomy is wild. Sea Market retains the author's guarded TownRegion; pinned SeaMarketRegion is a TODO BaseRegion and would lose those rules.

## Name mapping and Haven

These native names are preserved for existing consumers:

| Author name | Output name | Reason |
|---|---|---|
| Heartwood | The Heartwood | Pinned name |
| Painted Caves | The Painted Caves | Pinned name |
| Prism of Light | The Prism of Light | Pinned name |
| Palace of Paroxysmus | The Palace of Paroxysmus | Pinned name |
| Haven | Haven Island | The author's ten rectangles cover an island, not just a guarded town |
| The Albatross Bar and Grill | The Albatross Bar and Grill in Haven | Pinned named shop, with author geometry and New Haven as parent |
| No author guarded Haven town | New Haven | Separate proposed TownRegion from P673 S7's 3614-3722, 2516-2657 town envelope |

The proposed New Haven envelope is provisional. It must be traced against the real buildings, road approaches and docks in P676/S7 before guards are enabled. The entire author Haven island must never become a town guard rectangle. No new character start is guessed; S7 supplies it through HavenSpots. The author's island GoLocation 3627,2606,0 stays an island reference.

Old stock Haven was capped at SE and is folded into active New Haven here. It is not reintroduced as a duplicate guarded town. All stock shop/training names, including ones not currently active, remain in the stock disposition table. S7 must rebind the active shop names to actual buildings; copying old shops into forest or broadly aliasing every shop to the whole town would change gameplay. In particular, do not carry Haven's old MaxExpansion SE cap onto the new town.

There are 35 deferred stock records, 59 replaced, 47 stock candidates and four retired. The exhaustive [stock-mapping.csv](cc-P692-tools/stock-mapping.csv) is the disposition list, including unnamed records. The candidates are not a claim that stock rectangles survived. Each carries its measured P669 percentChanged and a map-review requirement. P676 must retain, redraw or retire them deliberately, including farm and mining-region consumers.

## Catch-all regions and the extra Sosaria facet

The catch-alls named in the prompt are not in the XML Trammel facet. They are in a separate `<Facet name="Sosaria">`. Its Britain town is around 2884-3050,888-1119, whereas the Trammel Britain region and go menu are around 1495,1629. That is evidence against treating the whole facet as an additional Trammel region list. Dropping its unmatched geometry is the conservative mapping, not a claim that its names have no value on its intended map.

| Author entry or group | Mapping for Trammel | Reason |
|---|---|---|
| Sosaria / Orc Territory, four rectangles | Drop | No matching Trammel record; spread over unrelated Trammel locations |
| Sosaria / some Old Ruins, seven rectangles | Drop | Different facet, generic disconnected catch-all, no supported Trammel footprint |
| Sosaria / some Farmlands, an Abandoned Home, a Cemetary, an Old Fortress | Drop | Same wrong-facet issue; do not give them town, dungeon or housing behavior here |
| Sosaria / Death Gulch, Devil Guard, Moon, Grey, Montor, Fawn, Pirate Isle, Dawn and their children | Drop | Another geography; never import as new Trammel guard zones |
| Sosaria / Tarnithok Fortress | Drop pending map identification | Dungeon geometry exists only in that facet, no Trammel go-menu identity; P676 can revisit after a map check |
| Sosaria records with identical Trammel name and exact rectangle list | Music reference only | Only a valid pinned MusicName is reused; no additional region is registered |
| Trammel / Britain Forest North and South, the named forests, deserts, islands, Khalahandra Keep and Poultry Paradise | Wild BaseRegion | Keep author footprints and names; no guards or invented dungeon light |
| Trammel / Cove Orc Fort, Britain Graveyard, Vesper Graveyard | Wild NoHousingRegion | Preserve author housing fences without guards |
| Trammel / Misc Dungeons | Keep DungeonRegion, but review each of six boxes | It is a real Trammel record, not the other facet's catch-all. Its own GoLocation is outside all six boxes |

Every one of the 132 Sosaria records has a disposition in [sosaria-mapping.csv](cc-P692-tools/sosaria-mapping.csv). Shared music is accepted only on exact rectangle-list matches and valid enum spelling. For example, Sosaria's Kameron Kove music is `FayaxionAndTheSix`, while pinned's enum spells it `FayaxionAndTheSix`. Unknown or invalid names are omitted, never silently accepted as runtime enum values.

## Author Trammel mapping table

Rows follow depth-first XML order. Synthetic names make unnamed children addressable without changing their rectangles. A parent link is recorded in the JSON, not inferred from this table. The exhaustive per-record reason is also in author-mapping.csv.

| XML row | Author name | Author type | Native name | Native type | Class | Rectangles |
|---|---|---|---|---|---|---|
| 1 | Lord British Castle | TownRegion | Lord British Castle | TownRegion | town | 3 |
| 2 | Britain | TownRegion | Britain | TownRegion | town | 19 |
| 3 | (unnamed) | BaseRegion | Britain / subregion 1 | TownRegion | town | 13 |
| 4 | Britain Graveyard | NoHousingRegion | Britain Graveyard | NoHousingRegion | wild | 2 |
| 5 | Buccaneer's Den | TownRegion | Buccaneer's Den | TownRegion | town | 1 |
| 6 | (unnamed) | BaseRegion | Buccaneer's Den / subregion 1 | TownRegion | town | 4 |
| 7 | Cove | TownRegion | Cove | TownRegion | town | 5 |
| 8 | Delucia | TownRegion | Delucia | TownRegion | town | 5 |
| 9 | (unnamed) | BaseRegion | Delucia / subregion 1 | TownRegion | town | 1 |
| 10 | Elandrim Nur Shaz | TownRegion | Elandrim Nur Shaz | TownRegion | town | 1 |
| 11 | Elmhaven | TownRegion | Elmhaven | TownRegion | town | 1 |
| 12 | Fort Yondall | TownRegion | Fort Yondall | TownRegion | town | 3 |
| 13 | Hammerhill | TownRegion | Hammerhill | TownRegion | town | 1 |
| 14 | Haven | NoHousingRegion | Haven Island | NoHousingRegion | wild | 10 |
| 15 | The Albatross Bar and Grill | BaseRegion | The Albatross Bar and Grill in Haven | TownRegion | town | 2 |
| 16 | Heartwood | TownRegion | The Heartwood | TownRegion | town | 1 |
| 17 | Jhelom Islands | NoHousingRegion | Jhelom Islands | NoHousingRegion | wild | 4 |
| 18 | Jhelom | TownRegion | Jhelom | TownRegion | town | 3 |
| 19 | (unnamed) | BaseRegion | Jhelom / subregion 1 | TownRegion | town | 4 |
| 20 | Kameron Kove | TownRegion | Kameron Kove | TownRegion | town | 2 |
| 21 | Kettleburg | TownRegion | Kettleburg | TownRegion | town | 2 |
| 22 | Magincia | TownRegion | Magincia | TownRegion | town | 17 |
| 23 | (unnamed) | BaseRegion | Magincia / subregion 1 | TownRegion | town | 2 |
| 24 | Minoc | TownRegion | Minoc | TownRegion | town | 13 |
| 25 | (unnamed) | BaseRegion | Minoc / subregion 1 | TownRegion | town | 3 |
| 26 | Moonglow | TownRegion | Moonglow | TownRegion | town | 2 |
| 27 | The Scholar's Inn | BaseRegion | The Scholar's Inn | TownRegion | town | 6 |
| 28 | Nujel'm | TownRegion | Nujel'm | TownRegion | town | 7 |
| 29 | (unnamed) | BaseRegion | Nujel'm / subregion 1 | TownRegion | town | 13 |
| 30 | Papua | TownRegion | Papua | TownRegion | town | 2 |
| 31 | (unnamed) | BaseRegion | Papua / subregion 1 | TownRegion | town | 1 |
| 32 | Plunderers Peak | TownRegion | Plunderers Peak | TownRegion | town | 9 |
| 33 | Red Baron Stronghold | TownRegion | Red Baron Stronghold | TownRegion | town | 10 |
| 34 | Red Dagger Keep | TownRegion | Red Dagger Keep | TownRegion | town | 20 |
| 35 | Sea Market | TownRegion | Sea Market | TownRegion | town | 1 |
| 36 | Seraphim Peak | TownRegion | Seraphim Peak | TownRegion | town | 5 |
| 37 | Serpent's Hold | TownRegion | Serpent's Hold | TownRegion | town | 4 |
| 38 | (unnamed) | BaseRegion | Serpent's Hold / subregion 1 | TownRegion | town | 3 |
| 39 | Skaddria Naddheim | TownRegion | Skaddria Naddheim | TownRegion | town | 4 |
| 40 | Skara Brae | TownRegion | Skara Brae | TownRegion | town | 16 |
| 41 | (unnamed) | BaseRegion | Skara Brae / subregion 1 | TownRegion | town | 5 |
| 42 | Trinsic | TownRegion | Trinsic | TownRegion | town | 11 |
| 43 | (unnamed) | BaseRegion | Trinsic / subregion 1 | TownRegion | town | 6 |
| 44 | Valunstead | TownRegion | Valunstead | TownRegion | town | 2 |
| 45 | Vesper | TownRegion | Vesper | TownRegion | town | 18 |
| 46 | (unnamed) | BaseRegion | Vesper / subregion 1 | TownRegion | town | 6 |
| 47 | Viligant Valley | TownRegion | Viligant Valley | TownRegion | town | 2 |
| 48 | Wind | TownRegion | Wind | TownRegion | town | 11 |
| 49 | (unnamed) | BaseRegion | Wind / subregion 1 | TownRegion | town | 7 |
| 50 | Yew | TownRegion | Yew | TownRegion | town | 10 |
| 51 | (unnamed) | BaseRegion | Yew / subregion 1 | TownRegion | town | 1 |
| 52 | Agurast Ascension | DungeonRegion | Agurast Ascension | DungeonRegion | dungeon | 3 |
| 53 | Amul Seketsi Royal Tomb | DungeonRegion | Amul Seketsi Royal Tomb | DungeonRegion | dungeon | 1 |
| 54 | Azurite Caverns | DungeonRegion | Azurite Caverns | DungeonRegion | dungeon | 3 |
| 55 | Bharlim Passage | DungeonRegion | Bharlim Passage | DungeonRegion | dungeon | 3 |
| 56 | Black Widow Pit | DungeonRegion | Black Widow Pit | DungeonRegion | dungeon | 3 |
| 57 | Bleak Wind Tunnels | DungeonRegion | Bleak Wind Tunnels | DungeonRegion | dungeon | 8 |
| 58 | Blighted Grove | MondainRegion | Blighted Grove | MondainRegion | dungeon | 1 |
| 59 | (unnamed) | PoisonedTree | Blighted Grove / PoisonedTree 1 | PoisonedTreeRegion | dungeon | 1 |
| 60 | Boulder Tunnel | DungeonRegion | Boulder Tunnel | DungeonRegion | dungeon | 1 |
| 61 | Britain Sewers | DungeonRegion | Britain Sewers | DungeonRegion | dungeon | 1 |
| 62 | Covetous | DungeonRegion | Covetous | DungeonRegion | dungeon | 2 |
| 63 | Deceit | DungeonRegion | Deceit | DungeonRegion | dungeon | 1 |
| 64 | Delucia Passage | DungeonRegion | Delucia Passage | DungeonRegion | dungeon | 6 |
| 65 | Despise | DungeonRegion | Despise | DungeonRegion | dungeon | 1 |
| 66 | Destard | DungeonRegion | Destard | DungeonRegion | dungeon | 1 |
| 67 | Dragons Den | DungeonRegion | Dragons Den | DungeonRegion | dungeon | 3 |
| 68 | Everstar Estuary | DungeonRegion | Everstar Estuary | DungeonRegion | dungeon | 1 |
| 69 | Fire | DungeonRegion | Fire | DungeonRegion | dungeon | 1 |
| 70 | Fortress Calcifina | DungeonRegion | Fortress Calcifina | DungeonRegion | dungeon | 2 |
| 71 | Fungully Grotto | DungeonRegion | Fungully Grotto | DungeonRegion | dungeon | 2 |
| 72 | Ghuul Sanctuary | DungeonRegion | Ghuul Sanctuary | DungeonRegion | dungeon | 1 |
| 73 | Guardian's Power Plant | DungeonRegion | Guardian's Power Plant | DungeonRegion | dungeon | 2 |
| 74 | Hammerhill Sewers | DungeonRegion | Hammerhill Sewers | DungeonRegion | dungeon | 1 |
| 75 | Haven Catacombs | DungeonRegion | Haven Catacombs | DungeonRegion | dungeon | 2 |
| 76 | Hythloth | DungeonRegion | Hythloth | DungeonRegion | dungeon | 1 |
| 77 | Ice | DungeonRegion | Ice | DungeonRegion | dungeon | 3 |
| 78 | Iguana Cove | DungeonRegion | Iguana Cove | DungeonRegion | dungeon | 1 |
| 79 | Kal Berbessia | DungeonRegion | Kal Berbessia | DungeonRegion | dungeon | 2 |
| 80 | Khaldun | DungeonRegion | Khaldun | DungeonRegion | dungeon | 1 |
| 81 | Mongbat Hideout | DungeonRegion | Mongbat Hideout | DungeonRegion | dungeon | 8 |
| 82 | Murkmere Dwelling | DungeonRegion | Murkmere Dwelling | DungeonRegion | dungeon | 2 |
| 83 | Nimaku Lava Basin | DungeonRegion | Nimaku Lava Basin | DungeonRegion | dungeon | 3 |
| 84 | Oboru Burial Ground | DungeonRegion | Oboru Burial Ground | DungeonRegion | dungeon | 2 |
| 85 | Orc Cave | DungeonRegion | Orc Cave | DungeonRegion | dungeon | 3 |
| 86 | Painted Caves | MondainRegion | The Painted Caves | MondainRegion | dungeon | 1 |
| 87 | Palace of Paroxysmus | MondainRegion | The Palace of Paroxysmus | MondainRegion | dungeon | 1 |
| 88 | (unnamed) | AcidRiver | The Palace of Paroxysmus / AcidRiver 1 | AcidRiverRegion | dungeon | 154 |
| 89 | (unnamed) | BaseRegion | The Palace of Paroxysmus / subregion 2 | MondainRegion | dungeon | 2 |
| 90 | (unnamed) | BaseRegion | The Palace of Paroxysmus / subregion 3 | MondainRegion | dungeon | 1 |
| 91 | Passage of Lost Souls | DungeonRegion | Passage of Lost Souls | DungeonRegion | dungeon | 3 |
| 92 | Prism of Light | MondainRegion | The Prism of Light | MondainRegion | dungeon | 1 |
| 93 | CrystalField | CrystalField | CrystalField | CrystalFieldRegion | dungeon | 1 |
| 94 | IcyRiver | IcyRiver | IcyRiver | IcyRiverRegion | dungeon | 7 |
| 95 | Sanctuary | MondainRegion | Sanctuary | MondainRegion | dungeon | 1 |
| 96 | Seaspray Solitude | DungeonRegion | Seaspray Solitude | DungeonRegion | dungeon | 1 |
| 97 | Sentinels Military Base | DungeonRegion | Sentinels Military Base | DungeonRegion | dungeon | 1 |
| 98 | Shame | DungeonRegion | Shame | DungeonRegion | dungeon | 2 |
| 99 | Skulker's Den | DungeonRegion | Skulker's Den | DungeonRegion | dungeon | 2 |
| 100 | Solen Hives | DungeonRegion | Solen Hives | DungeonRegion | dungeon | 1 |
| 101 | Stone Burrow Mines | DungeonRegion | Stone Burrow Mines | DungeonRegion | dungeon | 2 |
| 102 | Swampwater Solitude | DungeonRegion | Swampwater Solitude | DungeonRegion | dungeon | 1 |
| 103 | Terathan Keep | DungeonRegion | Terathan Keep | DungeonRegion | dungeon | 2 |
| 104 | Whispering Hollow | DungeonRegion | Whispering Hollow | DungeonRegion | dungeon | 2 |
| 105 | Wrong | DungeonRegion | Wrong | DungeonRegion | dungeon | 1 |
| 106 | Wylarn Caverns | DungeonRegion | Wylarn Caverns | DungeonRegion | dungeon | 1 |
| 107 | Misc Dungeons | DungeonRegion | Misc Dungeons | DungeonRegion | dungeon | 6 |
| 108 | Blackthorn Castle | TownRegion | Blackthorn Castle | TownRegion | town | 3 |
| 109 | Britain Forest North | BaseRegion | Britain Forest North | BaseRegion | wild | 19 |
| 110 | Britain Forest South | BaseRegion | Britain Forest South | BaseRegion | wild | 75 |
| 111 | Buccaneers Jungle | BaseRegion | Buccaneers Jungle | BaseRegion | wild | 5 |
| 112 | Hedge Maze | BaseRegion | Hedge Maze | BaseRegion | wild | 1 |
| 113 | Trinsic Jungle | BaseRegion | Trinsic Jungle | BaseRegion | wild | 23 |
| 114 | Swamp of Desolation | DungeonRegion | Swamp of Desolation | NoHousingRegion | wild | 8 |
| 115 | Compassion Desert | BaseRegion | Compassion Desert | BaseRegion | wild | 43 |
| 116 | Covetous Forest | BaseRegion | Covetous Forest | BaseRegion | wild | 46 |
| 117 | Glimmerwood | BaseRegion | Glimmerwood | BaseRegion | wild | 7 |
| 118 | Huntsman's Forest | BaseRegion | Huntsman's Forest | BaseRegion | wild | 27 |
| 119 | Moonglow Forest | BaseRegion | Moonglow Forest | BaseRegion | wild | 73 |
| 120 | Nujelm Desert | BaseRegion | Nujelm Desert | BaseRegion | wild | 103 |
| 121 | Cove Orc Fort | NoHousingRegion | Cove Orc Fort | NoHousingRegion | wild | 4 |
| 122 | Vesper Graveyard | NoHousingRegion | Vesper Graveyard | NoHousingRegion | wild | 1 |
| 123 | Yew Forest | BaseRegion | Yew Forest | BaseRegion | wild | 31 |
| 124 | Isle of the Avatar | BaseRegion | Isle of the Avatar | BaseRegion | wild | 1 |
| 125 | Isle of Colossus | BaseRegion | Isle of Colossus | BaseRegion | wild | 3 |
| 126 | Poultry Paradise | BaseRegion | Poultry Paradise | BaseRegion | wild | 1 |
| 127 | Khalahandra Keep | BaseRegion | Khalahandra Keep | BaseRegion | wild | 1 |
| 128 | Skypoint Islands | BaseRegion | Skypoint Islands | BaseRegion | wild | 1 |
| 129 | Dunbarrow Fissure | BaseRegion | Dunbarrow Fissure | BaseRegion | wild | 1 |
| 130 | Echoback Estuary | BaseRegion | Echoback Estuary | BaseRegion | wild | 1 |
| 131 | Darkfathom Hollow | BaseRegion | Darkfathom Hollow | BaseRegion | wild | 1 |
| 132 | Dragonstorm Isle | BaseRegion | Dragonstorm Isle | BaseRegion | wild | 1 |
| 133 | Vesper Forest | BaseRegion | Vesper Forest | BaseRegion | wild | 28 |
| 134 | Shrine of Chaos | BaseRegion | Shrine of Chaos | BaseRegion | wild | 1 |
| 135 | Shrine of Compassion | BaseRegion | Shrine of Compassion | BaseRegion | wild | 1 |
| 136 | Shrine of Honesty | BaseRegion | Shrine of Honesty | BaseRegion | wild | 1 |
| 137 | Shrine of Honor | BaseRegion | Shrine of Honor | BaseRegion | wild | 1 |
| 138 | Shrine of Humility | BaseRegion | Shrine of Humility | BaseRegion | wild | 1 |
| 139 | Shrine of Justice | BaseRegion | Shrine of Justice | BaseRegion | wild | 1 |
| 140 | Shrine of Sacrifice | BaseRegion | Shrine of Sacrifice | BaseRegion | wild | 1 |
| 141 | Shrine of Spirituality | BaseRegion | Shrine of Spirituality | BaseRegion | wild | 2 |
| 142 | Shrine of Valor | BaseRegion | Shrine of Valor | BaseRegion | wild | 1 |
| 143 | Bravehorn's drinking pool | BaseRegion | Bravehorn's drinking pool | BaseRegion | wild | 1 |
| 144 | Paroxysmus Exit | MondainRegion | Paroxysmus Exit | MondainRegion | dungeon | 1 |
| 145 | Sanctuary Entrance | MondainRegion | Sanctuary Entrance | MondainRegion | dungeon | 1 |
| 146 | Jail | Jail | Jail | JailRegion | wild | 1 |
| 147 | Green Acres | GreenAcres | Green Acres | GreenAcresRegion | wild | 1 |
| 148 | Lost Lands Outskirts | BaseRegion | Lost Lands Outskirts | BaseRegion | wild | 11 |
| 149 | Papua Desert | BaseRegion | Papua Desert | BaseRegion | wild | 10 |
| 150 | Ice Island | BaseRegion | Ice Island | BaseRegion | wild | 4 |

## Open questions and required map checks for P676

1. Confirm the new Haven placement with S7's final HavenSpots and trace guards around its buildings and docks. Recreate all active New Haven shop, bank, inn, guild and training names at the right footprints. The proposed town envelope cannot substitute for individual shops. The ten-rectangle Haven Island fence implements blanket ModernUO no housing; ServUO smartNoHousing has no matching JSON switch. Confirm that stricter fence is desired.
2. Walk the edge of every author TownRegion, including Plunderers Peak, Red Baron Stronghold, Red Dagger Keep, Seraphim Peak, Skaddria Naddheim and Viligant Valley. Their author classes request guards, even where a place's name sounds hostile. Confirm each settlement's intended status, walls, gates and road approaches. Buccaneer's Den remains unguarded. Names retain author spelling, including Viligant.
3. Resolve the equal-priority overlaps Lord British Castle/Britain and Kettleburg/Skara Brae. Blackthorn Castle intentionally has priority 51 over Britain's 50, but its geometry and doorway still need checking. Exact intersection rectangles are in geometry-review.json. Also check all wild, town, cave and dungeon overlaps and Z boundaries on the map, especially Yew's explicit 0-39 range and Britain's -10 override.
4. Inspect the 14 GoLocations outside their own footprints listed in geometry-review.json. Some shrine approach points can intentionally be outside a tiny altar box. Everstar Estuary's author Main Hall point 6366,3730,-16 is outside the author's Estuary footprint. Ice's go point lies outside its boxes, Murkmere Dwelling's first interior point does too, and Misc Dungeons' point is outside all six boxes. Do not widen a region merely to contain a bad reference point. Check source, doorway and each level, then correct either the region or the staff point with evidence.
5. Check every known entrance against the doorway and teleporter data in S4/S6. Where the XML entrance and go-menu entrance differ, the go-menu point was chosen and the record says so. Fire's primary go-menu entrance is on the Lost Lands surface; the XML names a different approach by Serpent's Hold. Preserve both access routes in the teleporter work. Terathan Keep's listed entrance is inside its own footprint. Khaldun's 5882,3819 entrance and Blackthorn Castle's 1522,1504 entrance lack Z and are withheld in omitted-properties.json. Boulder Tunnel, Britain Sewers, Delucia Passage, Guardian's Power Plant, Kal Berbessia and Solen Hives have no verified external entrance in this handoff.
6. Preserve ordinary DungeonRegion rules for the normal dungeons. This data does not add a recall-in-only switch, since the pinned JSON classes have none. Existing MondainRegion records retain their stronger all-travel-spell restriction. P676 must compare the intended stock travel behavior, including coordinate checks in SpellHelper, before deciding whether a new dungeon needs an additional rule. Classifying every new dungeon as MondainRegion would also block recall out and mark, so that is not done.
7. Seal the new dungeon approaches through S14 until S18 supplies encounters. Region data alone does not close teleporters or doors. Check every level against its own dry floor and Z, not just the region's bounding box. Britain Sewers, Delucia Passage, Haven Catacombs and the named new dungeons remain candidates even without an external entrance. The acid, ice, crystal and poisoned-tree classes do not implement their TODO damage effects.
8. Redraw Moongates and New Haven Moongate after S4 finalizes the actual destinations. This artifact deliberately does not leave stock guard boxes at moved gate coordinates. Check the author's town docks too. Known dock points appear in locations-review.csv, but the source provides no separate dock rectangles. A guessed radius around a dock or moongate is not a wall survey.
9. Review all stock candidates against stock-mapping.csv and P669's change percentages. The 73 areas.csv boxes are connected map-change clusters, sometimes joining entire forests and sea. They are not town boundaries. The author does not supply names or exact no-housing boundaries for every new island. Unnamed islands stay ordinary default wild terrain unless P676 has a map-based reason to define a region. S14, not this dataset, must produce fences for unfinished land.
10. Review point-only landmarks in locations-review.csv. Fort Whitestone, Castle Dunbain, Fort Stormhammer, Tigerclaw Fortress, Cherrygrove Bliss, Mistveil Ruins, camps and guardposts have go-menu points but no standalone authored region rectangles. Their containing forest or town region is listed where the point is inside one. Do not turn P669's screenshot-sized boxes or a single point into a guessed guard zone. The Britain Forest North South point and Glimmerwood West point fall outside every candidate footprint; trace those edges. No dedicated region is fabricated for a point-only landmark.
11. Preserve existing consumers by auditing names in P676's build. The stable names covered here do not prove all script lookups still work. Search customizations, patches and pinned sources, especially New Haven training, farm harvesting, mining, town houses and name-based achievements. Missing shop names are explicit deferred work, not passed facts.
12. Keep runtime custom regions separate. `server/customizations/Fold/FoldRegions.cs` still guards old void C and will collide with Passage of Lost Souls until S2 moves its mirror. `Regions/OldHavenBurrowsRegion.cs`, `Regions/RootdeepVault.cs`, `Regions/ApprenticeTraining.cs` and the revamped-dungeon region classes also register in code. Do not duplicate them with unregistered JSON class names. S2, S7 and S8 own those moves and must land with S3 as P673 describes. The roaming fountain region is also runtime-owned. This file is Trammel only; S13 must make its own Felucca decisions.

## Verification and limits

Read both work-copy AGENTS.md files, direction-decision.md, tasks.md, P669's assessment, P673's swap plan and the source files listed above. Used canonical customizations and the pinned source tree. Did not read the stale server/uo build tree.

Windows PowerShell 5.1.26100.9711 also parsed the region JSON with ConvertFrom-Json and reported 198 records. An initial nested-shell quoting attempt failed before parsing the file; the corrected invocation succeeded. Performed one-time data inspections, not a new test suite or gate: parsed every JSON and CSV artifact, compared source record order and stock grade rows, checked registered runtime type names and MusicName values, checked unique output names and parent-before-child references, and checked positive, in-map rectangle dimensions and Z ranges. All output records have the requested source and classification. The source-to-output rectangle comparison accounts for the five zero-area omissions. The record inventory and native-property audit are captured in validation-summary.json.

No lane tests were requested and no test was added. No build or runtime region loading was claimed. No SoS tile, static, flood-fill, screenshot, player walk, guard response, boat approach or live state was verified in this task. The geometry review reports source discrepancies without guessing terrain fixes. P676 must run the build, region lookup facts, map-overlay render and player checks required by S3.

Ran the repository progress reporter in dry-run mode against these work copies. Used dry-run because this task authorizes data and notes only. The reporter unexpectedly wrote tools/progress.json even in dry-run: tools/progress.py:722 writes the snapshot before the dry-run return at line 737. Restored that unrelated file to its exact initial HEAD bytes, and left the reporter unchanged. This is an existing reporter defect, not part of P692. No code, docs directory, map, account, save or service file changed. No Haven connection, deploy, build, commit, push, merge or branch switch. All output files are below 5 MB. The Golem owns the commit.

P692 DONE
