# P529: the New Haven dungeon design compared with main

Reviewed October 24, 2026. Notes only. Code HEAD and local main both point to
`f2853e86ca96c89d8f97a6c3a17c9fd2661ad41d`. The design and notes checkout and its
local main both point to `8512bdb0ff5d2161e329b23446e8a4ba4ef1a491`. No remote
refresh was attempted. These findings describe source in the supplied work copies,
not the installed map, published package, saved world, or running shard.

Rootdeep has its map patch, ordinary entrance, regions, creatures, material drops,
harvest selection rules, tutorial Vault, and floor traps. The largest unfinished
piece is P24's reward loop: dungeon set pieces, their upgrades, recipes spending
the parts, and the repeatable replacement quest. The Brood Pit is still a direct
boss spawn rather than a mini champion. P413's larger entrance is still queued.
The shipped map also adds no choppable tree tiles, so the promised giant-root
gathering path is missing despite the Rootwood harvest override and creature drops.

## Baseline and table conventions

Design inputs, in order of the decisions they record:

- `D:/UO/cc-prompts/completed/cc-P24-new-haven-dungeon-research.md`, especially
  "Why"; `notes/cc-P24-new-haven-dungeon-research.md`, sections 3 through 6.
- `notes/dungeon-decisions-2026-10-01.md`, including the later no-magical-entry
  settlement; completed P36, including its October 6 revisions; and
  `notes/cc-P36-dungeon-build-1.md`.
- `docs/feature-queue.md:3300` (F-45), P139/P140/P141, and
  `notes/cc-P141-rootdeep-burrows.md`. F-45 names the dungeon Rootdeep, renames
  the root zone the Tangle, adds the tutorial Vault, and selects the Queen's
  drider artwork. P24's earlier giant-spider appearance is superseded.
- `notes/cc-P188-cont-rootdeep-goes-in.md` and the shipped map patch, including
  later changes already on main. P188 implements local map patching instead of
  P24's initial proposal to distribute complete EA map files.
- `D:/UO/cc-prompts/queue/cc-P413-rootdeep-anthill-entrance.md`: Chase's October
  22 request for a mound with a wide opening. Its presence in the queue is not
  evidence of implementation.

The table form follows P515/P528: **Design item / Built or not / Where in code /
Gap / Size**. Built means the source and an entry path exist. Partial means the
implemented part and missing behavior are both identified. Unverified means this
review did not establish the installed or runtime result. Sizes estimate remaining
work: none, S (local change), M (several interacting paths), or L (substantial
system/content work). They are judgments, not schedules, and should not be added.

Source prefixes: `C/` = `ShatteredLegacy/server/customizations/`, `P/` =
`ShatteredLegacy/server/patches/`, `T/` = `ShatteredLegacy/server/tests/`, `M/` =
`ShatteredLegacy/player-package/`, and `D/` = `ShatteredLegacy/docker/uo/`.
`U/` = read-only `D:/UO/ModernUO-pinned/Projects/`, verified at
`d4531cd94b739613155225c234900de9f47d2c88`. Unprefixed notes paths belong to
shard-migration. The prohibited generated `server/uo/` tree was not read.

## Map, access, and starter materials

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| Real Trammel dungeon in candidate A, with Landing, Vault, Warren, Brood Pit, Tangle, Dawnseam, and Gloom | Built as map operations and placement data | `M/vendor/shattered-legacy-map/trammel.mapops`; `C/Regions/OldHavenBurrowsRegion.cs:38`; `C/ClusterFRootdeepSeeder.cs:99`; `notes/art/rootdeep-mockup/layout.json`; `notes/cc-P167-tools/plan-sets.json` | The patch contains actual land and static changes inside the approved rectangle. This is more than an empty region. Applied-map collision, every room connection, and visual quality in a client remain unverified here. P141/P188 renders and historical checks are evidence of earlier work, not a fresh walk. | none for map presence; M validation |
| Package and server use the dungeon edits; EA data floor follows to 7.0.117.0 | Built pipeline; installation and exact parity unverified | `M/Build-PlayerPackage.ps1:857`; `M/payload/app/Apply-MapOps.ps1:115`; `M/payload/app/Build-UoOverrides.ps1:750`; `M/payload/app/Play.ps1:333`; `M/payload/app/Setup.ps1:31`; `D/Build-MapOverlay.ps1:31`; `D/Start-TestShard.ps1:170`; `D/docker-compose.test.yml:54` | Both sides consume the same map operations using the same applier on local copies of EA files. The package ships edits, not complete EA maps or a pinned EA tiledata file. This is the later delivery method, not a missing copy of P24's initial full-file proposal. The same patch on different EA bases does not prove byte-identical results; publication, actual data directories, current server floor, and installed hashes were not checked. Error handling gaps are below. | M parity/release validation |
| Anyone can enter the ordinary Burrows through Old Haven's ruined Second Bank and leave by the ladder | Built for P188's single hole | `C/ClusterFRootdeepSeeder.cs:63`, `:70`, `:308`; `C/Regions/OldHavenBurrowsRegion.cs:46`; `M/vendor/shattered-legacy-map/trammel.mapops:11541`, `:12438` | Hole `(3619,2620,0)` goes to `(5193,1138,0)`; ladder-foot trigger `(5193,1132,0)` returns to `(3619,2621,0)`. The south-wall gap remains in the patch. The Vault is the tutorial-only exception. Following-pet, ghost, and actual approach movement need applied-map proof. | none for original entrance; M validation |
| P413 mound with a wide dark opening; every opening tile goes down | Not built; explicitly queued | Same entrance rows and map operations as above; queued P413, Do 1 through 5 | Main still draws the single `0x1B71` hole and seeds one down trigger. Add the mound, triggers for the whole opening, and a return landing outside it. Upgrade existing P188 teleporters without leaving old triggers active. Preserve the collapsed wall route, arrival, ladder foot, Old Haven spawn rules, and unrelated farm map operations. Update the region's entrance if moved. P188's old route report does not validate the new mound. | M; P413 |
| Dungeon rules: Young warning, monsters can attack Young, at most three hostiles per Young player, no housing | Built; broader regression coverage remains | `C/Regions/OldHavenBurrowsRegion.cs:32`, `:49`, `:128`; `U/UOContent/Regions/DungeonRegion.cs:21`; `U/UOContent/Regions/BaseRegion.cs:76`; `T/Regions/OldHavenBurrowsRegionVerification.cs:224` | The cap checks live hostile creatures, their current combatant, and unexpired aggression. Pets and player summons are excluded. The entry warning comes from the stock dungeon region. P433 requests slot-release and exemption assertions; P504 requests an actual Young entry-warning check. These are coverage gaps, not proof the existing warning or cap is absent. | S-M tests |
| No magical entry; recall out allowed; no linked gate out; flavored refusals | Built, with a disclosed coordinate limitation | `C/Regions/OldHavenBurrowsRegion.cs:87`; `C/Regions/RootdeepVault.cs:79`; `T/Regions/OldHavenBurrowsRegionVerification.cs` | RecallTo, GateTo, external TeleportTo, Mark, and GateFrom are refused in the intended cases; internal teleport within the ordinary Burrows is allowed. Staff bypass applies. This follows the later gate-out settlement. The callback supplies no destination map, so same-coordinate cross-facet destinations can be classified incorrectly. Client messages and a real travel session remain unverified. | S-M if resolving the edge |
| Dawnstone, Burrowhide, Rootwood, and cosmetic Gloomsilk; low material gates and modest bonuses | Built as resource and crafting definitions | `C/ClusterFStarterResources.cs:18`; `C/ResourceInfo.cs:401`, `:448`, `:525`, `:1171`; `C/ClusterFMiningExtension.cs:199`, `:245`; `C/ClusterFLumberjackingExtension.cs:312`, `:342`; `C/Engines/Craft/BurrowhideTailoringRegistration.cs:36` | Material selection gates are 45 where registered. Dawnstone and Burrowhide have the adopted attributes; Rootwood and Gloomsilk remain cosmetic. P36's F1 granite fix, F3 wood classification widening, and F4 Burrowhide satchel handling are present. A material gate is not proof every recipe succeeds at 45; Masonry retains its stock training and recipe requirements. Hue choices and client appearance remain unverified. | none for definitions; S-M validation |
| Region-only ore and wood selection at required/min/max 45/5/85, with stock fallback and depletion | Built selection rules; real harvest unverified | `C/Engines/Harvest/BurrowsRegionHarvest.cs:23`, `:31`, `:49`, `:57`; `T/Items/StarterResourcesVerification.cs:218`, `:246` | The overrides substitute a regional vein and delegate to stock selection, leaving the global bank/depletion machinery. They apply throughout the Burrows, not only beside visual crystals or roots. Existing tests directly call the selection path. Test real targets, skill outcomes, and bank depletion on the applied map. | M validation |
| Mine the cave walls for Dawnstone | Partial; mineable terrain exists | `P/Mining.cs:24`; `M/vendor/shattered-legacy-map/trammel.mapops:6541`, `:8407`, `:10105`; harvest override above | The landing is cave land `0x0245`, and a Dawnseam ring sample is mineable `0x0260`; the sampled Dawnseam interior tile is non-mineable `0x3868`. Visual crystal statics are not dedicated vein nodes. Actual reach, targeting, and output remain unverified. P430 already identified the need for a real harvesting check. | S-M validation |
| Chop giant roots for Rootwood | Partial overall; chopping targets missing from the shipped additions | `U/UOContent/Engines/Harvest/Lumberjacking.cs:11`, `:49`; `U/UOContent/Engines/Harvest/Core/HarvestDefinition.cs:188`; `C/Engines/Harvest/BurrowsRegionHarvest.cs:57`; `M/vendor/shattered-legacy-map/trammel.mapops`; map check below | No added static inside the Burrows matches the stock choppable list, and lumberjacking accepts no land tiles. The themed logs, vines, and root mounds do not become targets just because the harvest override exists. Supply reachable valid targets or deliberately extend the target rule. Rootling and Bramblehulk loot already provide Rootwood, so the resource itself is obtainable. Saved staff-placed trees were not inspected. | S-M map/harvest integration |
| Burrowhide carving and spider Gloomsilk drops; family material sources | Built | `C/Mobiles/Burrows/BurrowsCommon.cs:107`; `C/Mobiles/Burrows/FarmCreatures.cs:322`; `C/Mobiles/Burrows/WarrenCreatures.cs:61`; `C/Mobiles/Burrows/TangleDawnseamCreatures.cs:49`, `:187`, `:232`; `C/Mobiles/Burrows/GloomCreatures.cs:66`, `:115`, `:175`, `:234` | Carving creates Burrowhide; roots drop logs; stone creatures drop ore/ingots; spiders drop silk. These loot paths fulfill material acquisition independently of missing root chopping. Live earning rates, combat balance, and carving presentation remain unverified. | none for source paths; S balance checks |
| Keep starter resources out of progression orders and random material pools | Built with explicit exclusions | `C/ClusterFMetalTiers.cs`; `C/ClusterFWoodTiers.cs`; `C/ClusterFLeagueRanks.cs:121`; `C/Services/PointsSystems/CleanUpBritanniaData.cs:347`; `T/Items/StarterResourcesVerification.cs:452` | Dawnstone is excluded from the League metal ladder, and these resources are not intended as later-tier order currencies. The existing fixture checks BOD, commission, work-order, and random-pick tables. It was read, not executed in P529. | none identified |

## Creatures, Vault, and encounter systems

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| Rootdeep bestiary and increasing zone difficulty | Built creatures and seeder entries | `C/Mobiles/Burrows/WarrenCreatures.cs`; `C/Mobiles/Burrows/TangleDawnseamCreatures.cs`; `C/Mobiles/Burrows/GloomCreatures.cs`; `C/Mobiles/Burrows/VaultCreatures.cs`; `C/ClusterFRootdeepSeeder.cs:99`; `C/Mobiles/Evo/ShardBodyTypes.cs:47`; `M/vendor/shattered-legacy-art/registry.csv` | The family roster and named bosses are concrete types referenced by zone spawners. P139/P140 body registration is present; this review does not certify frames, sound, or visual quality. Rootling uses a stock bogling fallback documented by P140. Farm teaching creatures are additional content, not evidence that the dungeon reward quest exists. | none for roster; M playtest |
| Normal respawn independent of player loops | Built | `C/ClusterFRootdeepSeeder.cs:99`, `:179`, `:332` | Ordinary Spawner rows set pack size, home range, group behavior, and minute delays, and call Respawn on placement. Seeding is an Administrator command, not an automatic world-load placement. Whether anyone has run it in the current world is unverified. | none for implementation; operational check |
| Burrow Mother ends a mini champion with grub waves | Partial; boss and personal brood only | `C/Mobiles/Burrows/WarrenCreatures.cs:156`, `:220`; `C/ClusterFRootdeepSeeder.cs:123`; `C/Services/MiniChampionSystem/MiniChampType.cs:15`; `C/Services/MiniChampionSystem/MiniChampionSpawn.cs:100` | The seeder directly spawns her. Her personal brood has live and lifetime caps, not kill-count stages leading to a boss. P197 has since put a MiniChamp engine in main, but its table/generator does not include Rootdeep. P140's old explanation that the engine is absent is obsolete. Review the unfinished engine, add the Burrows entry and placement, reconcile her existing brood, and prove restart/completion behavior. P197's note remains PAUSED; no dedicated MiniChamp fixture was found in tracked tests. | M Rootdeep integration; broader engine validation separate |
| Gloom Queen as end boss; both dungeon bosses drop jewelry and a boss part | Built, using F-45's later appearance decision | `C/Mobiles/Burrows/GloomCreatures.cs:197`, `:261`; `C/Mobiles/Burrows/WarrenCreatures.cs:251`; `C/Mobiles/Burrows/BurrowsCommon.cs:153` | The Queen is a mage with melee poison and web behavior. Both bosses add a stock gold jewel and their respective part on death. The source satisfies the drop promise without a special jewelry recipe. Balance for a small group of graduates and multiplayer loot rights remain unverified. | none for drop paths; M playtest |
| Tutorial-only Vault next to the Landing, decoy chests, and fixed scripted loot | Built, with shared-loot limitations | `C/Regions/RootdeepVault.cs:38`, `:121`; `C/Mobiles/Burrows/VaultCreatures.cs:17`, `:87`, `:161`, `:241`, `:282`; `C/Tutorial/TutorialCreature.cs:33` | The region admits participants and their pets and refuses outsiders/graduates. Tutorial-only SafeDepositBox mimics teach the chest lesson. The Overdraft adds its fixed pouch, ingot, bandages, and trinket. Fixed corpse drops do not guarantee every credited trainee gets a looting lesson: P141 recorded the shared corpse/loot-rights issue, still unresolved here. | M per-participant lesson/reward handling |
| Kill the Overdraft, open a one-way crawlway, seal after leaving | Partial; basic path built, lifecycle defects remain | `C/Regions/RootdeepVault.cs:171`, `:205`, `:232`; `C/Mobiles/Burrows/VaultCreatures.cs:286`; `T/Regions/RootdeepVaultVerification.cs:207` | Boss death grants the saved clear key and opens the crawlway temporarily. Eligible living players and following pets can pass into the Warren. The key already bars reentry before departure, so reconnect/corpse recovery can fail; a player staying inside can repeat the boss rewards. Pet-deletion credit and a boss kited away from the crawlway are also unresolved. See P430 rows below. | M |
| Resurrection at the Landing and return after a tutorial death | Partial against F-45's landing-resurrection wording | `C/ClusterFRootdeepSeeder.cs:56`, `:201`; `C/Regions/OldHavenBurrowsRegion.cs:62`; `U/UOContent/Mobiles/PlayerMobile.cs:4065` | A working ankh is seeded at the Landing. Stock Young death handling chooses a configured death destination nearest the dungeon's exterior entrance, rather than placing the ghost at the Landing; P141 identifies the New Haven healer destination. The ankh therefore does not by itself deliver the proposed Young-death flow. P141 deliberately retained stock behavior for Chase to decide. Vault reentry after boss credit is a separate defect. | S-M if changing death routing; decision remains |
| Floor traps and a trap lesson in the Vault | Built beyond the original P36 scope | `C/ClusterFRootdeepSeeder.cs:87`, `:249`, `:278`; `C/Items/Traps/Deployable/TrapLesson.cs:23`, `:87`, `:113`; `T/Items/Traps/DeployableTrapsVerification.cs` | P275 adds stock floor hazards and a Stacks lesson with practice nets and rat capture credit. Calling traps wholly missing would ignore later main. These are not the missing Underworld puzzles or Tomb-style chambers. Real route difficulty and lesson play remain unverified. | none for placement/lesson code; M playtest |
| Underworld PuzzleRoom mechanics used inside Rootdeep | Not built in Rootdeep; reusable code exists elsewhere | `C/Services/Underworld/PuzzleRoom/PuzzleRoomTeleporter.cs:11`; `C/Services/Underworld/Generate.cs:39`; `C/ClusterFRootdeepSeeder.cs` | P197's key, puzzle-box, and teleporter code targets Underworld on Ter Mur. Rootdeep has no puzzle placement or reward wiring. P24 also offered stock circuit/mastermind/ticket alternatives, so another engine port is not automatically required. Choose and wire the actual Rootdeep lesson/room, then verify it. | M integration; content choice first |
| Tomb of Kings style chambers, levers, and group-clear progression | Not built as a Rootdeep encounter | `C/ClusterFRootdeepSeeder.cs:99`, `:332`; `U/UOContent/Engines/Khaldun/RaiseSwitch.cs`; `U/UOContent/Engines/Khaldun/RaisableItem.cs` | Rootdeep's group spawners support room-clear respawn but do not connect kills or levers to passage progression. No Rootdeep chamber controller or linked stock switch setup was found. P24 recommended stock equivalents first and advised against copying literal Ter Mur chamber coordinates. The Vault's boss crawlway is a distinct implemented event. | M room design/integration |

## P24's gear, parts, upgrades, and repeatable quest

These remain design backlog, rather than missed P36 deliverables: P36 explicitly
excluded the set, parts, upgrades, jewelry recipes, and quest. P140 later supplied
part drops. No later reviewed decision or implementation was found completing or
canceling this dungeon-specific reward loop.

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| Tradeable family parts and boss parts | Built as drops; spending not built | `C/Mobiles/Burrows/BurrowsCommon.cs:22`, `:37`, `:47`, `:57`, `:67`, `:77`, `:87`; family and boss death paths above | Burrower Claws, Rootheart Sap, Dawnstone Shards, Gloom Glands, Brood Mother's Mandible, and Gloom Queen's Fang are ordinary stackable items. They have no binding restriction. Searches of their consumers found drops, tests, and monster-stealing integration, not upgrade or crafting consumption. Loot is delivered; its promised economic purpose is missing. | none for items; M consumers |
| Dungeon starter set, with quest pieces and mini-champion completion | Not built | No matching set types or grant path in canonical customizations/patches; `C/Mobiles/Burrows/BurrowsCommon.cs:1`; `C/Engines/ML Quests/Items/NewHavenQuestBoard.cs:55` | Existing resource gear, guild starter kits, shop bands, and general levelable equipment do not implement this set. Define the dungeon pieces, family-to-piece grouping, base properties, set completion reward, and ordinary acquisition path. The board currently registers skill-training quests. | L combined set/reward work |
| Blessed owner-bound pieces, carried in any owner backpack bag or the owner's bank | Not built for the dungeon set | P24 section 5; `notes/dungeon-decisions-2026-10-01.md`, item 11; no dungeon set implementation | The accepted storage rule is broader than stock Nontransferable. Implement owner checks, safe bag/bank storage, equip and trade refusal, and death retention on the new pieces. Ordinary tradeable parts and boss jewelry should keep their separate policy. This is not solved by blessing a generic resource item. | M, shared with set |
| About three upgrade levels, family parts for matching pieces, boss parts for any piece | Not built | Part definitions above; no dungeon-part consumption or serialized dungeon upgrade-level field found | Implement costs, level state, recomputation from base, and the universal boss-part route. P24's proposed 30/50/70 thresholds remain draft numbers, not implemented balance. Do not describe the materials' 45 selection gate as a set upgrade level. | M, shared with set |
| Owner upgrades their own piece through a craft action and appropriate work site/tool | Not built; accepted route is known | `notes/dungeon-decisions-2026-10-01.md`, item 4; `U/UOContent/Engines/Craft/Core/CustomCraft.cs`; no Rootdeep craft registration | Owner-only CustomCraft was selected. Add recipes, target validation, skill and work-site checks, part consumption, and durable state updates. Owner-to-mentor consent was tabled; it is not a required missing feature of the selected first path. | M |
| Tradeable jewelry or other recipes using dungeon parts | Not built; stock boss jewelry does drop | `C/Mobiles/Burrows/BurrowsCommon.cs:153`; `C/ClusterFMiningExtension.cs:245`; `C/Engines/Craft/` registrations | Tinkering accepts Dawnstone, but that alone does not spend a family/boss part or define the proposed jewelry. Add explicit recipes and properties after deciding costs. Stock GoldRing/Bracelet/Earrings/Necklace drops satisfy only the boss-jewelry promise. | M |
| Repeatable quest replaces missing/broken pieces at base level, without duplicates | Not built | `C/Engines/ML Quests/Items/NewHavenQuestBoard.cs:55`, `:88`; no dungeon reward, ownership-scan, or replacement quest found | Build the repeatable objectives, missing-piece eligibility, reward filtering, binding, and base-level reset. The mini-champion completion award also needs its encounter hook. Preserve existing ML skill-training quests. | M after set and encounter work |
| Set survives wear/death or can be obtained again | Not built as a dungeon-set guarantee | No dungeon pieces; P24 sections 5.4 and 5.6 | Decide and test armor/weapon durability separately, death retention, and the replacement path. P24 explicitly warned that a weapon initialized with zero durability can be deleted on wear, unlike zero-durability armor. A generic blessed item does not complete the promised recovery contract. | S-M within set/replacement work |

Rootwood's combat bonus also needs an explicit reconciliation. The October 1
decisions initially kept it cosmetic; revised P36 says Chase wanted a later bow
bonus patch and table. P227 subsequently added extended-wood bonuses while
explicitly preserving cosmetic Rootwood (`C/ClusterFWoodBonuses.cs:8`, `:80`).
Current code has no Rootwood bonus row. Treat it as cosmetic in player guidance;
if the revised P36 promise is still desired, select its final row and test it.
The initial research's +20 Luck/+2 damage proposal is not a delivered property.

## Existing correctness and proof gaps still present in main

These are findings already recorded by P425, P430, P433, and P504, checked against
the corresponding current source branches. They are not fresh runtime
reproductions. A queued repair or an earlier green build is not a completed fix.

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| A saved entrance remains safe if the required map is unavailable | Partial | `C/ClusterFRootdeepSeeder.cs:179`, `:308`; `D/Start-TestShard.ps1:164`; `M/payload/app/Build-UoOverrides.ps1:782`; `M/payload/app/Setup.ps1:34`; reviews P425 #1 and P504 #1 | The seeder checks readiness when placing items; saved stock teleporters do not recheck it on use. Client map preparation failures are caught and launch continues. Refuse unsafe entry/startup or require successful map preparation. Verify both server-overlay loss and client-build failure with an already-seeded/saved character. | M |
| Seeder reruns repair or upgrade the entrance safely | Partial; clean unchanged rerun supported | `C/ClusterFRootdeepSeeder.cs:235`, `:318`; P425 #2/#3 | Lookup matches destination but not Active/source Z. A changed destination can leave an old active trigger and add another; a disabled/wrong-height exit can be counted as present. P413 needs an explicit old-world upgrade, conflict reporting, and repeat-run checks. | M, include in P413 |
| Vault seals after departure without losing loot, corpse recovery, or boss credit | Partial | `C/Regions/RootdeepVault.cs:152`, `:163`, `:177`, `:191`, `:234`; `C/Mobiles/Burrows/VaultCreatures.cs:282`; P430 #1 through #4 | Separate kill credit, reward eligibility, and departure. Use recorded responsible damage entries for a pet that died before the boss; resolve the canonical crawlway independently of where the boss died. Cover reconnect/death before looting and a second kill without leaving. Shared corpse loot rights are the additional P141 issue. | M |
| Reinforcement caps and cleanup survive repeated spawns and restart | Partial | `C/Mobiles/Burrows/VaultCreatures.cs:139`; `C/Mobiles/Burrows/WarrenCreatures.cs:162`, `:253`; P430 #5/#6 | Hoarding Rat reinforcements have no ownership cleanup. The Mother's brood references and lifetime counter are unsaved while her grubs persist as mobiles. Track/reconcile those populations and test repeated leader deaths and a save/reload mid-fight. The region's three-hostile combat cap is not a population cap. | M |
| Starter resource behavior matches ordinary craft/recycling routes | Partial | `C/ClusterFStarterResources.cs:119`; `C/SmithGuildSalvageBag.cs:77`; `P/CraftItem-shard-hooks.patch:17`; `T/Items/StarterResourcesVerification.cs:345`; P433 #1 through #4 | Goza-mat color retention does not accept Gloomsilk's subclass on the stock special path. Dawnstone's recycling gate differs by tool. Current material-consumption tests do not prove completed crafting or both new hide/board substitution pairs. Preserve stock Masonry prerequisites when improving the tests. | M |
| Applied-map route, warning, gathering, and encounter proof | Partial; existing unit checks cover narrower paths | `T/Regions/RootdeepWayInVerification.cs:109`, `:226`; `T/Regions/RootdeepVaultVerification.cs:317`; `T/Items/StarterResourcesVerification.cs:218`, `:246`; P425 #4/#5, P430 #7, P433 #5, P504 #2 | Several tests force map readiness, call OnMoveOver/MutateResource directly, or check rectangles. P188's helper also uses height math that differs from server movement. Add real movement across the final map, Young warning/protection transitions, pet/ghost travel, actual resource targeting/depletion, and saved-state encounter cases. Recheck P413's raised route with server movement. | M |

## Source checks and limits

The source search covered tracked canonical customizations, patches, tests,
build/placement wiring, package map operations, and the relevant pinned engine
paths. Absence claims were checked through consumers and entry points, not only
class names. In particular, all dungeon-part references were followed, the board's
quest registrations were read, MiniChamp's enum/table/generator were inspected,
and the Underworld generator's placement coordinates were checked. Generic
engines and existing guild/levelable equipment were not counted as Rootdeep
integration.

The map-target check ran as a read-only Python probe under Windows PowerShell
5.1. It parsed every `S+` record in
`player-package/vendor/shattered-legacy-map/trammel.mapops` and intersected IDs
inside Trammel x 5136-5247, y 1128-1263 with pinned Lumberjacking's actual
`m_TreeTiles` initializer. The matching operation list is empty. Repeating for
the Tangle x 5142-5188, y 1198-1228 gives the same empty list. Lumberjacking's
definition has empty LandTiles and uses that StaticTiles list; no shard change
extending that target list was found. `HarvestDefinition.Validate` and
`HarvestSystem` validate the target before the regional resource override can
help. The map look rules use fallen-log IDs `0x0CF3` through `0x0CF7`, vines, and
terrain root mounds; those additions do not supply choppable trees. This proves
the gap in the shipped additions, not the contents of an installed saved world.
P24 reported the original rectangle as void with no statics; that historical
base-map survey was not rerun against EA data here.

The same probe checked concrete map-operation samples: the south-wall removals,
single hole, ladder artwork, cave landing, and Dawnseam land IDs cited above.
It did not rebuild a real map or attempt harvesting. No aggregate feature
completion percentage or unmeasured creature count is asserted.

No code, tests, or `docs/` files changed. No new test or gate was written. Lane
tests are none, and no build, shard startup, client session, deployment, account
operation, or Haven connection was performed. Historical test results in P36,
P140, P141, P188, and P197 are not presented as P529 validation. Published package
contents, current saved spawners/teleporters, live balance, actual resurrection
flow, and persistence across a real restart remain unverified.

The first implementation priorities suggested by this comparison are safe map
failure handling and Vault recovery, then P413's entrance upgrade with real
movement proof. Rootwood needs an actual chopping target. The larger separate
content backlog is the dungeon set/parts/quest loop and Rootdeep encounter wiring.
This note schedules or changes none of them.

`tools/progress.py --dry-run` completed successfully with both work-copy path
overrides. Its attempted `tools/progress.json` write was intercepted in memory;
the file was verified byte-identical afterward. Global source totals were not
used as feature coverage. Source citation paths and line bounds, table columns,
local links, ASCII/no-em-dash formatting, whitespace, and file sizes were checked.
The code work copy is clean, and only this report and the lane note are new in
the migration work copy. Stop-request checks were made between steps.

Completion checks are also recorded in
[cc-P529-design-vs-build-new-haven-dungeon.md](cc-P529-design-vs-build-new-haven-dungeon.md).

P529 DONE
