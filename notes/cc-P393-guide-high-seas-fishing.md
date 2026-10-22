# P393: player guide to High Seas fishing and ships

Written October 22, 2026 in the Valorite-tower work copies. Docs-only draft work; no code, patches, configuration, tests, or deployment changed.

## Deliverables and scope

- `notes/wiki-drafts/high-seas-fishing.md`: new-player guide covering poles, catches, shore/deep/dungeon water, rare specimens and trophies, traps, bottles and wreck recovery, sea monsters, classic boats, proposed High Seas ships, training, achievements, and the Maritime Brotherhood.
- This note: source evidence, unresolved differences, verification limits, and checks.

Read both work-copy AGENTS.md files first. Also read the direction decision, task-list working agreement, governing-document index, P374/P390 model pages (`league.md`, `crafting-changes.md`), relevant feature-queue entries, P193, P209, and P268. Additional relevant notes consulted: P15, P54, P67, P70, P78, P123, P175, P283, and the current levels/loops design. The unrelated package-ships note P124 concerns distributing TazUO, not boats.

The page uses source behavior for its instructions and retains source differences in a separate Contradictions list. It does not settle the naval-combat decision, promise release dates, invent vendor access, or publish hidden-achievement triggers. Proposed ship phases are explicitly attributed to the assessment, rather than presented as an approved implementation schedule.

## Source conventions

`C/` below means the code work copy, `D:/UO/golems/Valorite-tower/ShatteredLegacy/`.
`M/` means the notes work copy, `D:/UO/golems/Valorite-tower/shard-migration/`.
`U/` means the read-only pinned tree, `D:/UO/ModernUO-pinned/Projects/UOContent/`.
`H/` means `C/server/customizations/Services/Expansions/High Seas/`.

Pinned HEAD was checked with `git rev-parse HEAD`: `d4531cd94b739613155225c234900de9f47d2c88`. No reading of `server/uo/` was used. `rg` is unavailable in this shell; searches used Python pathlib and PowerShell Select-String instead. No online research was needed because the requested evidence is local source and project decisions.

## Evidence for the guide

Line references are to files as read in this sitting. Ranges identify the relevant behavior, not just a name match.

| Player-facing claim | Source evidence |
|---|---|
| Fishermen sell poles; double-clicking a pole begins fishing | `U/Mobiles/Vendors/SBInfo/SBFisherman.cs:23`; `U/Items/Skill Items/Fishing/FishingPole.cs:16-29`. |
| Ordinary pole range, depleted water message, ordinary fish skill window | `U/Engines/Harvest/Fishing.cs:79-100`: range 4, depletion message, resource window 0..100. The general fishing prose avoids promising a timed recovery rate. |
| Guild home and membership | `C/server/customizations/ClusterFGuildStarterPath.cs:60` maps Fishing, Cartography, Cooking to maritime; `:224` places its guildmaster at New Haven docks. `C/server/customizations/ClusterFGuildSystem.cs:69-79` explains free joining and the later Apprentice task; `:205-213` defines Fishing 30 or 5 ordinary Fish. |
| Trade tools include a pole | `C/server/customizations/ClusterFGuildStarterPath.cs:284-325` gives character-creation tools once per character per guild; `C/server/customizations/CharacterCreation.cs:1124-1126` gives the Fishing pole. This is not an assertion that the trap is in the kit. |
| High Seas casts actually reach the fish table | `C/server/patches/Fishing-high-seas-fish.patch:4-29` preserves rare catches and hooks GetResourceType; `:32-44` signs, dates and weighs rare fish; `:47-75` adds catch messages. `C/docker/uo/apply-patches.sh:578,584-585` registers the clamp, fish, and taxidermy patches. |
| Shore 50, deep 80, dungeon 106 | `H/Items/Fish/FishInfo.cs:239-373`, especially `:250`, `:344-369`. Values are Fishing.Value; the page explicitly says base only where the code does. |
| Water definitions | `H/Items/Fish/FishInfo.cs:417-432` separates dungeon water from shore and ocean; `U/Items/Skill Items/Fishing/Misc/SpecialFishingNet.cs:323-375` validates the center and surrounding deep-water sample points. The guide does not turn that sampling into a claim that every tile in a radius is checked. |
| Example ordinary fish by pool | `H/Items/Fish/Fish.cs:39-63` lists the deep, shore, and dungeon pools. Examples on the page are read from these arrays. |
| Example rare-fish locations and exact skills | `H/Items/Fish/FishInfo.cs:50` AutumnDragonfish/Ilshenar/105.4; `:56` GiantKoi/Tokuno/deep/95.8; `:65` YellowtailBarracuda/Trammel/deep/81.9; `:68` AbyssalDragonfish/Destard/120; `:69` BlackMarlin/Felucca/deep/110.1; `:71` BlueMarlin/Trammel/deep/105.0. The location table is not proof those waters are reachable on the deployed world. |
| Fish carving and catch details | `H/Items/Fish/Fish.cs:17-32` defines common carving; `H/Items/Fish/RareFish.cs:18-48` stores fisher/date, displays them and supplies a special carved steak example. Weighing happens in the fishing patch, not merely in constructors. Trap stamping is `H/Items/LobsterTrap.cs:354-360`. |
| Trophies and consumed resources | `U/Items/Skill Items/Carpenter Items/TaxidermyKit.cs:39,88` checks base Carpentry 90; `C/server/patches/TaxidermyKit-fish-trophies.patch:6-12` invokes the custom branch; `H/Items/Fish/Trophies.cs:115-160` consumes 10 boards, fish and kit and creates the deed. `:202-260` checks backpack, house co-ownership and walls; `:395-418` restores the deed on chopping by a co-owner. |
| Trap use, range, timing and recovery | `H/Items/LobsterTrap.cs:161-221` deploys or dumps contents; `:223-270` validates range 6 and location, sets owner and buoy; `:272-305` starts the one-minute timer and recovers it; `:316-377` trains, checks loss and catches. `:393-411` deletes the lost trap. |
| Trap eligibility, player guild and Felucca | `H/Items/LobsterTrap.cs:413-456` checks owner, `from.Guild`, non-null party, then Felucca criminal taking. Shared professional-guild membership is not that `Guild` comparison. |
| Poles versus crustaceans; lava trap | `H/Items/Fish/FishInfo.cs:290-298` excludes crustaceans from poles and other fish from traps. `H/Items/LavaLobsterTrap.cs:13-39` uses the lava tile list. The current normal trap fallback can still make a plain crab or lobster; the page does not advertise specific lava-exclusive loot. |
| Bait-dependent Fisherman's set | `H/Items/Sets/FishermansSet.cs:28-180` defines the human hat, trousers, vest and gloves; `H/Items/Fish/FishInfo.cs:254-262` reads bait only from a trap and `:380-413` returns 1.0 before attire when bait does not match. `H/Mobiles/Charybdis.cs:110-114` includes those pieces in its unique rewards. Bait items and pole hooks remain deferred in `M/notes/cc-P193-port-high-seas-fishing.md`, section 5. No player means to bait a trap was found. |
| Base-skill special-find thresholds | `U/Engines/Harvest/Fishing.cs:13-18,172-190` requires deep water and base 80 for net/big fish, 90 for a map, 100 for a bottle. `C/server/patches/Fishing-deep-water-finds-osi.patch:8-10` and `C/server/customizations/ClusterFSkillClamps.cs:105-110` limit the growing find chance at skill 120. The guide gives requirements, not guaranteed rates. |
| Serpents carry special catches | `U/Engines/Harvest/Fishing.cs:324-371` creates a SeaSerpent or DeepSeaSerpent, packs the found map, bottle or net onto it, and warns the player. These checks are retained by the additive fish patch. |
| Bottle to SOS, ancient designation, reading coordinates | `U/Items/Skill Items/Fishing/Misc/MessageInABottle.cs:35-59` picks the level and replaces a carried bottle with an SOS; `U/Items/Skill Items/Fishing/Misc/SOS.cs:97-149` labels ancient at level 4 and displays the message/location. |
| Wreck recovery and mule caveat | `U/Engines/Harvest/Fishing.cs:237-323` searches the player's backpack, checks Trammel/Felucca and proximity, rolls wreckage or a chest, inserts a special/fabled net, unlocks and untraps the chest, and deletes the SOS on chest recovery. `M/notes/cc-P70-mule-modules.md:277-278` independently records why a mule's SOS is not used. |
| Nets summon monsters, and fabled still means Leviathan | `U/Items/Skill Items/Fishing/Misc/SpecialFishingNet.cs:83-165` uses a carried net and validates water/range; `:298-320` selects serpent, deep serpent, water elemental or kraken and deletes the net; `:399-418` defines FabledFishingNet and explicitly spawns Leviathan. The High Seas patches do not replace that override. |
| Champion combat and rewards, not an acquisition promise | `H/Mobiles/Charybdis.cs:132-175,237-295,297-444,446-542` covers tentacles, lightning, waves; `:110-117,545-567` covers rewards. `H/Mobiles/OsiredonTheScalisEnforcer.cs:133-221` covers water attacks and eels; `:110-113,264-276` covers rewards. `H/Mobiles/BaseSeaChampion.cs:130-187` awards artifacts to eligible damagers. `:227-265` moves boats without a hull-damage call. |
| Classic shipwright stock | `U/Mobiles/Vendors/SBInfo/SBShipwright.cs:17-22` lists SmallBoatDeed, SmallDragonBoatDeed, MediumBoatDeed, MediumDragonBoatDeed, LargeBoatDeed, LargeDragonBoatDeed. Prices are deliberately omitted. |
| Boat placement, planks and spoken sailing | `U/Multis/Boats/BaseBoatDeed.cs:35-160` places from a deed; `U/Multis/Boats/Plank.cs:128-276` handles boarding/disembarking and locks; `U/Multis/Boats/BaseBoat.cs:999-1225` dispatches sailing, turning, stop and anchor speech keywords. No staff command is included on the page. |
| Dry dock and required key | `U/Multis/Boats/BaseBoat.cs:590-631` requires alive, a carried key, anchor, empty hold and empty deck; `:633-710` confirms and creates the docked item; `U/Multis/Boats/TillerMan.cs:71-80` begins dry dock from outside. |
| Planned galleons and ship systems | `M/notes/cc-P268-high-seas-ships-assessment.md`, sections 2, 4-6. A declaration search of canonical customizations, patches and pinned UOContent found none of BaseGalleon, TokunoGalleon, GargishGalleon, OrcishGalleon, BritannianShip, Rowboat, ShipCannon. This is evidence of current port status, not approval of the recommendation. |
| Skill cap versus actual fishing gains | `C/server/customizations/ClusterFSkillCaps.cs:11-31` defaults individual cap to 200. `U/Engines/Harvest/Fishing.cs:100` plus `U/Engines/Harvest/Core/HarvestSystem.cs:146-149` still uses the rod's 0..100 resource window. `C/server/customizations/ClusterFSkillGain.cs:320-443` has no Fishing ceiling extension. `H/Items/LobsterTrap.cs:318-325` calls CheckSkill(0, skill.Cap) and requires base 75 on deep-water tiles. `M/notes/cc-P283-skill-gain-paths-research.md:94` records the same distinction. |
| Achievements and League connection | `C/server/customizations/ClusterFAchievements.cs:505-529` public any-skill milestones; `:1273-1297` checks Base skills; `:1339-1340` awards AP and Renown; `:1453-1461` checks skills on login; `:411-422` exposes the player command and TazUO button. No fishing-specific hidden achievement is described. |
| Levels remain design work | `M/notes/f12-levels-loops-caps.md`, current-rulings/status introduction, and `M/docs/feature-queue.md:926-944` distinguish character progression plans from existing skill behavior. The fish selection and trap code above do not award per-catch character XP. No XP number or loop promise is given. |
| Cooking orders/patterns versus Fishing deeds | `C/server/customizations/Services/BulkOrders/BulkOrderVendors.cs:500-510` accepts Cooking deeds at FisherGuildmaster; `C/server/customizations/Engines/Craft/ClusterFRecipeGate.cs:385-399` owns Cooking through maritime. `M/docs/feature-queue.md:1718-1734` decides Fishing deeds as future work; current bulk-order types do not add Fishing deeds. |
| Planned Ocllo hall | `M/docs/feature-queue.md:3394-3438`, F-49, keeps the chapter and selects Ocllo. P151 section 14 leaves facet/site proposals open; the page supplies no facet or travel directions to the proposed headquarters. |

## Contradictions kept, not resolved

The page's final list retains these pairs of evidence:

- `M/docs/content-menu.md:61-63` declines naval combat; P268 headlines and sections 5-6 recommend a phased port and request a recorded reversal. Neither source was edited.
- P193's headlines say players reach the port through a pole/trap and that champions fight and drop. Its For Chase section uses created test instances. The present implementation supplies their behavior, not a verified player acquisition chain. Searching `new LobsterTrap`, `typeof(LobsterTrap)`, corresponding lava forms, `new Charydbis`, and `new Osiredon` through canonical customizations and patches found no trap acquisition or champion spawning caller. The Charydbis FishInfo row is `cannotfishup`; CharydbisEffectSpawn is a wave visual, not the boss. Additional source read: stock SBFisherman and the fabled-net override. No live placement claim follows from this search.
- `M/notes/cc-P54-f12-xp-and-gain-paths.md:67,593` records Fishing's missing gain/content route. P283 `:94` and LobsterTrap's implementation add a cap-based route while leaving rods at 100. This historical mismatch remains explicit.
- `M/docs/feature-queue.md:3477-3479` names Black Pearl from shoreline/fishing in F-51's design. `U/Engines/Harvest/Fishing.cs:111-118` implements WhitePearl. Neither the High Seas fish hook nor trap code implements the designed Black Pearl route.
- `M/notes/cc-P175-cont-clean-up-britannia-finish.md:172,243-244` defers the fishing-set reward. P193 adds human pieces on Charybdis. Searching the current `C/server/customizations/Services/PointsSystems/CleanUpBritanniaData.cs` finds no Fisherman's-piece entry. The port is not advertised as completion of the older Clean Up shop reward.

## Existing tests read and verification limits

Read `C/server/tests/Services/HighSeasFishingVerification.cs`, including these existing facts:

| Fact | Location |
|---|---|
| EveryFishConstructsHasALabelAndRoundTrips | `:116` |
| TheTableHas36RowsAndKnowsItsIndexes | `:183` |
| ThePoleGivesShoreFishFromFiftyAndTheTrapGivesCrabs | `:215` |
| BaitStrengthIsTwoForTheBaitedFishAndAttireAddsItsBonus | `:316` |
| TheFishingPatchHandsOutHighSeasFishAndSignsARareOne | `:348` |
| TheTrapBobsCatchesCrabsAndIsLostByTheTwentiethBob | `:406` |
| TheKitMakesAFishTrophyDeedAndTheDeedBuildsTheAddon | `:495` |
| TheSeaChampionsConstructRoundTripSpawnAndAward | `:589` |
| TheArtifactsAndTheFishermansSetConstructAndRoundTrip | `:680` |

These tests explicitly lack real tile data (`:8-11`). They verify construction, persistence and selected hooks, not deployed access or every ocean tile. P193 records deliberately failing then passing tests; P209 records a later passing merged-tree build. Those are historical results, not tests rerun in P393.

No tests added or run, as specified by this docs-only prompt's lane tests. No build or container was needed. Unverified: deployed server version/configuration; actual vendor stock and world placements; a normal acquisition route for either trap; an encounter route to either High Seas champion; reachable dungeon/facet fishing water; client appearance and gameplay; galleon client data and future purchase rules. Those limits are reflected on the page. No Haven, SSH, remote API, Docker context, live stack or account action was used.

## Review and housekeeping

Work-copy status was clean at entry. STOP-REQUESTED was checked between research and writing steps and remained absent at those checks. PowerShell commands ran in Windows PowerShell 5.1; no PowerShell 7 syntax or new PowerShell test was introduced.

Ran `python tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` explicitly pointing at these work copies: exit 0. It printed the current fishing-half inventory and setup/port status. The output is a stem-coverage proxy and was not used to claim behavior or player access.

Existing tooling defect observed: despite the documented print-only behavior, `--dry-run` rewrote `tools/progress.json`. Its diff changed the generated timestamp and prompt-queue metadata. Source inspection shows that `build()` writes that JSON before `main()` returns for `--dry-run`. This is our tooling's defect, outside P393's guide scope. Restored only that generated file to its proven-clean entry content using `git show HEAD:tools/progress.json` bytes. README and dashboard were not modified. No tooling fix or new test was added.

Final review: both requested Markdown files have valid local link targets, no em dashes, short paragraphs and tables. The page ends with Sources and Contradictions, with file:line evidence confined to this work note. Reviewed numbers against the source gates and example rows above; excluded rates and catalogue totals that a new player does not need. Reviewed the page for staff commands, exploits and hidden-achievement spoilers: none included. Both new files are below 5 MB. Windows PowerShell reports version 5.1.26100.9444. `git diff --check` passes in both work copies; final status is limited to these requested notes files, with the code work copy clean.

P393 DONE
