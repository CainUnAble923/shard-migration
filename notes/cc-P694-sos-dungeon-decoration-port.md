# P694: Siege of Sosaria dungeon decoration port

2026-10-27. Data and notes only. Author credit: Zigholtul, Siege of Sosaria Trammel Map 3.0. Prepared for P683 (S6). Nothing loaded, built, deployed, or changed in the code repository.

## Result and inventory

The author file already uses the CFG syntax read by pinned ModernUO. No type or coordinate translation is needed. The complete Trammel version preserves every source line in order, with a credit and handling header added. The last MISC declaration has no placement, so it is retained as a comment. The Felucca version changes only MapDest to Felucca to keep travel within that facet. The read-only author file is unchanged.

Counted from `sos-author-data/SOS-Trammel-Dungeons.cfg`: 775 physical lines = 167 comment lines + 207 blank lines + 201 type headers + 200 placement lines. The 201 headers declare one type, Teleporter. There are 200 placed teleporters, no doors, and no props in this supplied file. Of 28 named dungeon sections, 25 contain placements and three are empty. MISC is a separate unfinished section. The tables and CSVs below publish the records behind these counts.

Source SHA-256: `40fe3e9260672436df655a885b3547eeef61c0956eb724da1a1f8df08bf1f2d4`.

All data files are under [cc-P694-tools](cc-P694-tools/):

| File | Purpose |
|---|---|
| [sos-dungeons.cfg](cc-P694-tools/sos-dungeons.cfg) | Complete Trammel reference, 200 active placements. Contains surface entrances. |
| [sos-dungeons-felucca.cfg](cc-P694-tools/sos-dungeons-felucca.cfg) | Complete Felucca reference, 200 active placements with MapDest=Felucca. |
| [sealed/sos-dungeons.cfg](cc-P694-tools/sealed/sos-dungeons.cfg) | S6 starting data for Trammel. All 70 surface entrances commented out, 130 exits and internal placements active. |
| [sealed/sos-dungeons-felucca.cfg](cc-P694-tools/sealed/sos-dungeons-felucca.cfg) | Same S6 exclusion for Felucca, with MapDest=Felucca. |
| [item-types.csv](cc-P694-tools/item-types.csv) | Complete type map, with source paths. |
| [teleporter-ends.csv](cc-P694-tools/teleporter-ends.csv) | All 200 directed placements, both XYZ ends, return IDs and destinations, source and output line numbers, and S6 exclusion list. |
| [teleporter-pairs.csv](cc-P694-tools/teleporter-pairs.csv) | 98 exact pairs and four shared-return entrance rows, with both ends and actual return destinations. |
| [source-lines.csv](cc-P694-tools/source-lines.csv) | All 775 author lines mapped to their line in each output CFG, with the transformation explained. |
| [manifest.json](cc-P694-tools/manifest.json) | Counts, empty sections, unplaced header, and SHA-256 and byte size for each data file. |

The four CFGs have the same eight-line preamble length. Original line N appears at line N+8 in each one. Every original comment and blank line remains. Commenting the unplaced MISC header makes its status explicit and creates no item. ModernUO would otherwise read that header as a list with zero entries.

## Loader and type evidence

Verified read-only `D:/UO/ModernUO-pinned` HEAD is `d4531cd94b739613155225c234900de9f47d2c88`, matching `ShatteredLegacy/docker/uo/Dockerfile:3`.

Paths below are under `D:/UO/ModernUO-pinned` unless labeled otherwise:

- `Projects/UOContent/Commands/Object Creation/Decorate.cs:37-39`: Decorate generates Britannia on both Trammel and Felucca, then each facet's own folder.
- `Decorate.cs:52-69`: Generate reads the immediate folder's `*.cfg` files and calls DecorationList.ReadAll, then Generate with the supplied maps. The command does not take a folder argument.
- `Decorate.cs:443-445`: ordinary types use their parameterless constructor.
- `Decorate.cs:959-978`: Teleporter reads PointDest with Point3D.Parse and MapDest with Map.Parse. `Decorate.cs:1028-1031` sets the requested item ID.
- `Decorate.cs:1231-1256`: Generate places each entry on each supplied source map. The source map comes from the folder/caller, not from MapDest.
- `Decorate.cs:1294-1388`: ReadAll/Read skip hash comments, resolve the type name, parse the item ID and semicolon properties, and read coordinate entries until a blank line or end of file. `Decorate.cs:1394-1420` parses XYZ.
- `Projects/UOContent/Items/Misc/Teleporter.cs:25-68`: Server.Items.Teleporter has a parameterless constructor, uses 0x1BC3, is immovable and invisible, defaults active, and defaults Creatures to false. These match `D:/UO/ServUO-pub57/Scripts/Items/Internal/Teleporter.cs:13-47`.
- `Teleporter.cs:220-254`: a non-null MapDest controls the destination facet. Therefore a Trammel declaration loaded on Felucca would send the player to Trammel.
- `ShatteredLegacy/docker/uo/Dockerfile:106-107`: the image receives pinned Distribution/Data. This task adds no Docker COPY and does not install these notes as runtime data.

No Decorate.cs or Teleporter.cs replacement was found in `server/patches`, and canonical `server/customizations` has no Teleporter class or replacement CFG loader. `ClusterFNewHavenServicesSeeder.cs:514-518` also uses the pinned DecorationList.Read entry point.

| ServUO type | ModernUO type | Declared headers | Placed items | Result |
|---|---|---:|---:|---|
| Server.Items.Teleporter | Server.Items.Teleporter | 201 | 200 | Exact match, item ID 0x1BC3, PointDest and MapDest supported. One header is unplaced. |

Types without a match: none in this file. No substitute Static items and no behavior loss are needed. Defaults for activity, visibility, movement, creatures, effects, sound and delay are left to the matched stock constructor.

## Dungeon inventory and sealed entrance list

A surface entrance means an author block labeled exactly `Entrance`. Level 1, 2 and 3 Entrance blocks are internal travel and remain included. The exclusion list is also encoded on every relevant row in teleporter-ends.csv and in each sealed CFG's comments. Empty sections are preserved without inventing travel or coordinates.

| Author section | Source heading line | All placements | Surface entrances excluded | Sealed active |
|---|---:|---:|---:|---:|
| Agurast Ascension | 6 | 12 | 6 | 6 |
| Amul Seketsi Royal Tomb | 47 | 16 | 2 | 14 |
| Azurite Caverns | 106 | 16 | 4 | 12 |
| Bharlim Passage | 161 | 8 | 2 | 6 |
| Black Widow Pit | 192 | 10 | 2 | 8 |
| Bleak Wind Tunnels | 229 | 6 | 3 | 3 |
| Boulder Tunnel | 252 | 0 | 0 | 0 |
| Dragons Den | 258 | 4 | 2 | 2 |
| Everstar Estuary | 275 | 8 | 2 | 6 |
| Fortress Calcifina | 306 | 6 | 3 | 3 |
| Fungully Grotto | 329 | 6 | 3 | 3 |
| Ghuul Sanctuary | 352 | 4 | 2 | 2 |
| Guardians Power Plant | 369 | 0 | 0 | 0 |
| Hammerhill Sewers | 375 | 2 | 1 | 1 |
| Iguana Cove | 386 | 10 | 4 | 6 |
| Kal-Berbesia | 423 | 0 | 0 | 0 |
| Mongbat Hideout | 429 | 16 | 2 | 14 |
| Murkmere Dwelling | 486 | 6 | 3 | 3 |
| Nimaku Lava Basin | 509 | 6 | 3 | 3 |
| Oboru Burial Grounds | 532 | 8 | 4 | 4 |
| Passage of Lost Souls | 561 | 16 | 4 | 12 |
| Seaspray Solitude | 616 | 12 | 3 | 9 |
| Sentinels Military Base | 659 | 3 | 2 | 1 |
| Skulker's Den | 673 | 4 | 2 | 2 |
| Stone Burrow Mines | 690 | 4 | 2 | 2 |
| Swampwater Solitude | 707 | 4 | 2 | 2 |
| Whispering Hollow | 724 | 10 | 5 | 5 |
| Wylarn Caverns | 759 | 3 | 2 | 1 |
| MISC | 773 | 0 | 0 | 0 |
| Total | | 200 | 70 | 130 |

Boulder Tunnel, Guardians Power Plant and Kal-Berbesia have empty Entrance sections. Source line 775 is `Teleporter 0x1BC3 (PointDest=(0, 0, 0); MapDest=Trammel)` with no coordinate line. These are author omissions, preserved and flagged for S6/S18 rather than guessed or filled in.

## Teleporter pairs and author asymmetries

The complete pairs are in teleporter-pairs.csv, with an exhaustive directed list in teleporter-ends.csv. Every one of the 200 destinations coincides with another source teleporter coordinate. There are 98 exact reciprocal pairs, covering 196 directed placements. Four additional surface entrances share those pairs' landing pads. They return to a neighboring entrance instead of the exact tile used to enter. No destination lacks a return teleporter, and no two placed teleporters share a source XYZ.

Both facets use the coordinates below, with travel staying on the same facet:

| Dungeon | Extra entrance header line | Entrance XYZ | Landing XYZ | Return destination XYZ | Actual return header line |
|---|---:|---|---|---|---:|
| Iguana Cove | 389 | 945, 1535, 60 | 7050, 2588, -31 | 946, 1535, 60 | 402 |
| Iguana Cove | 398 | 948, 1535, 60 | 7051, 2588, -31 | 947, 1535, 60 | 405 |
| Sentinels Military Base | 665 | 1483, 1293, -1 | 6520, 3007, 32 | 1482, 1293, -1 | 669 |
| Wylarn Caverns | 765 | 2642, 50, 40 | 6669, 746, 3 | 2642, 49, 38 | 769 |

These are authored many-to-one routes and have return ends. They are retained without adding extra exits. Actual arrival and return behavior remains for the S6 play check.

## S6 handoff

1. Start with the two files in `cc-P694-tools/sealed/`. They omit the supplied entry routes for all 25 populated dungeon sections by excluding all 70 surface entrance placements. Exits and internal level links remain available as the plan asks. Any other entrances from stock data or seeders still need S6 reconciliation.
2. For later packaging, the Trammel file belongs in the generated runtime `Data/Decoration/Trammel/` folder and the Felucca file in `Data/Decoration/Felucca/`. Do not put either facet-specific file in `Data/Decoration/Britannia/`, and do not load either on both maps. MapDest is explicit. The notes files are not automatically packaged.
3. S18 can open a dungeon by restoring only that dungeon's `# S6 SEALED: ` header and coordinate lines in both sealed files after its monsters are ready. The complete files at the tools root are reference copies for that step. Do not install full and sealed versions together. Do not treat the empty sections or MISC as completed entrances.
4. P683 must check every placement and landing on the actual SoS map, on both facets, including Z and approach tiles, plus conflicts with retained stock decoration and teleporters. This task proves data preservation and static loader compatibility only. It does not prove walkability, spawn readiness, entrance sealing against other data, or gameplay behavior.
5. `Decorate.cs:1192-1205` treats an existing teleporter with the same XYZ, item ID and exact type as present, without checking PointDest or MapDest. Reloading data does not repair an existing teleporter's destination. Use the approved scratch world and reconcile collisions in S6 before loading. The broad Decorate command also processes stock decoration folders; it is not a targeted import command.
6. S6 owns packaging, compilation/build gate, loading and a player travel check. No build or runtime command has been run for this notes-only task. No Haven connection, account operation, code change, or deployment occurred.

## Verification

Completed a one-off Python data audit against the unchanged author file. No test files or lane tests were added. Before checking the deliverables, the audit rejected four in-memory negative controls: an altered destination, a removed placement, a Trammel destination in a Felucca file, and an accidentally enabled sealed surface entrance. Then all four real CFGs passed.

The audit parsed the blank-delimited CFG blocks independently, compared every placed type, numeric item ID, property and XYZ against the author records, and checked the sealed inclusion list. It confirmed 783 lines in each CFG, all 775 source-line mappings, all 200 directed CSV records, coverage of every directed record in the 102 pair rows, all source/output line references, and manifest hashes. The source SHA-256 stayed unchanged. Every output was checked for the 5 MB limit and for em dashes. The largest data file is source-lines.csv at 45,320 bytes.

`python tools/progress.py --dry-run` completed with exit code 0, with SL_SHARD and SL_MIGRATE pointing at these work copies. The tool writes tools/progress.json inside build() even in dry-run mode. That generated refresh was restored to its initially clean HEAD contents to keep this task confined to its notes and data. No README or docs files changed. The shell was Windows PowerShell 5.1.26100.9711, running powershell.exe.

Static source compatibility is verified. The actual ModernUO reader was not executed, and no compilation, game server, client, map walkability, stock-content collision, or travel play check was run. Those checks remain for P683/S6. No code repository changes, commits, branch switches, pushes, or Haven access occurred.

P694 DONE
