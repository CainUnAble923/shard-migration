# P526: mounts and reward mounts guide draft

Written October 24, 2026. Documentation only. Deliverable: [wiki draft](wiki-drafts/mounts.md). The prompt's shorter requested notes filename is also provided as [cc-P526-guide-mounts.md](cc-P526-guide-mounts.md).

## Scope and evidence

Read both work-copy AGENTS.md files, direction-decision.md, and tasks.md. Followed the current no-commit and notes-only rules over older commit instructions. No code, configuration, docs/ files, services, art, saves, or account data changed. No Haven connection, deployment, build, or client session.

Source snapshot:

- ShatteredLegacy work copy: `f2853e86ca96c89d8f97a6c3a17c9fd2661ad41d` before this task.
- shard-migration work copy: `f85a525b8db9e4d0b169b035ad9bfe0daa54f467` before this task.
- Read-only `D:\UO\ModernUO-pinned`: verified HEAD `d4531cd94b739613155225c234900de9f47d2c88`.
- Code paths below are relative to the ShatteredLegacy work copy. Upstream paths are relative to `D:\UO\ModernUO-pinned`. No reads from server/uo/.
- `rg` was unavailable. Used PowerShell file searches and Python to inspect source and parse spawn JSON.

The guide distinguishes implemented source behavior, proposed balance, and unverified running-world availability. It does not claim P277 or P365 is deployed. No outside wiki is used as evidence for this shard.

## Custom-mount sources

| Claim | Source |
|---|---|
| Red and colorable riding dragons remain staff-only, untamable, one slot, horse-level placeholders | `server/customizations/Mobiles/Mounts/RideableDragons.cs:1-15, 25-82`. Constructors require GameMaster access. Searched canonical customizations for both class names and found no player acquisition hook. P277 implementation notes independently agree. |
| P365 mount roster and routes | `server/customizations/Mobiles/Mounts/RewardMounts.cs:59-79`, literal Defs rows, read individually |
| P365 stats, no taming, one slot | `RewardMounts.cs:87-104` |
| Alive/capacity checks, owner, bond, follow order, world placement | `RewardMounts.cs:110-144` |
| Shop AP and prices | `RewardMounts.cs:57, 150-172`; actual shop spread `server/customizations/LeagueShop/LeagueShop.cs:122` |
| AP unlocks without being spent, Renown payment and backpack capacity | `LeagueShop.cs:132-212` |
| Shop boxes cannot give mount rows | `LeagueShop.cs:257-287`: maximum AP of the Gold pool is 1,000, below mount AP 1,750 |
| Tamer and Boss mount roll defaults and pools | `RewardMounts.cs:174-194`; actual calls in `server/customizations/LootBoxes/LootBoxRoller.cs:271-282` |
| Blessed, single-use statuette, backpack check, deletion only on successful summon | `server/customizations/Mobiles/Mounts/RewardMountStatuette.cs:25-63` |
| Food by mount type; moonlit unicorn has no ordinary unicorn gender override | `RewardMounts.cs:200-359`: reward base plus each concrete class |
| Achievements give their reward item directly and only on first account earn | `server/customizations/ClusterFAchievements.cs:1330-1380` |
| Achievement requirements, prerequisites, reward classes, hidden status | `ClusterFAchievements.cs:474-484, 612-620, 659-709, 1124-1133` |
| Exactly which facets the achievement checks | `ClusterFAchievements.cs:659-699, 1547-1557`: all VisitFacet definitions, Trammel before Felucca; no Ter Mur definition |
| Default box themes omit Tamer; Harrower has a tier-6 Boss mapping | `server/customizations/LootBoxes/ClusterFLootTable.cs:109-133, 148-181` |
| Automatic box sources and boss event wiring | `server/customizations/LootBoxes/ClusterFLootBoxes.cs:132-209`. The staff give command at 293 onward is not a player route. |
| Evo appearance does not confer riding | `server/customizations/Mobiles/Evo/EvoPet.cs:23`, derives from BaseCreature, not BaseMount; read alongside P365's new horse and lizard line notes |

Counted **18 P365 definitions**, in one roster file, `server/customizations/Mobiles/Mounts/RewardMounts.cs`. The complete roster beside that count:

| Route | Keys counted |
|---|---|
| League shop, 6 | chestnut-draft, bay-draft, grey-draft, palomino-draft, barded-warhorse, gilded-charger |
| Achievement, 4 | moonlit-unicorn, bonewalker-steed, emberhoof, war-wolf |
| Loot box, 8 | marsh-raptor, dusk-raptor, sky-raptor, bog-strider, riding-drake, riding-bear, riding-wolf, saddled-horse |

These are the source routes, not a count of mounts reachable by players today. The P365 notes explicitly call the routes, prices, and horse stats proposals, and report that the mounts were not seen in a client. P277 has scratch-client proof but leaves acquisition and rider seat height open. The guide reflects this by calling itself a draft, describing current source values, and keeping unverified box availability visible.

## Ordinary mounts and upstream sources

The guide's base taming numbers were read from the following files, not copied from a wiki. Unless a full path is shown, each is under `Projects/UOContent/Mobiles/Animals/Mounts/`:

| Mount | Source of base requirement and special rule |
|---|---|
| Horse | `Horse.cs:53-55`, 29.1 |
| Riding llama | `RidableLlama.cs:40-42`, 29.1 |
| Desert ostard | `DesertOstard.cs:36-38`, 29.1 |
| Forest ostard | `ForestOstard.cs:37-39`, 29.1 |
| Frenzied ostard | `FrenziedOstard.cs:40-42`, 77.1 |
| Ridgeback | `Ridgeback.cs:39-41`, 83.1 |
| Savage ridgeback | `SavageRidgeback.cs:39-41`, 83.1 |
| Swamp dragon | `SwampDragon.cs:43-45`, 93.9; barding properties at 56-100 |
| Giant beetle | `Beetle.cs:39-57`, 29.1, pack and subdue requirement |
| Fire beetle | `Projects/UOContent/Mobiles/Monsters/SE/FireBeetle.cs:42-60`, 93.9, Forge attribute at 8 |
| Nightmare | `Nightmare.cs:64-65`, 95.1 |
| Ki-rin | `Kirin.cs:46-53`, 95.1 and male-only riding |
| Unicorn | `Unicorn.cs:44-51`, 95.1 and female-only riding |
| Lesser hiryu | `LesserHiryu.cs:42-44, 100-125`, 98.7 and conditional Bushido control improvement |
| Hiryu | `Hiryu.cs:42-44`, 98.7 |
| Cu sidhe | `Projects/UOContent/Mobiles/Monsters/ML/Animal/CuSidhe.cs:54-56, 87-104`, 101.1 and Elf/Pads riding check |
| Reptalon | `Projects/UOContent/Mobiles/Monsters/ML/Misc/Melee/Reptalon.cs:39-41`, 101.1 |
| Fire steed | `FireSteed.cs:40-42`, 106.0; random construction in `Projects/UOContent/Items/Misc/DeceitBrazier.cs:30-59, 143-178` |
| Silver steed | `SilverSteed.cs:18-20`, 103.1; no acquisition claim |
| Scaled swamp dragon | `ScaledSwampDragon.cs:38-40`, 93.9; no acquisition claim |

Spawn locations were verified by parsing the `entries[].name` fields of upstream `Distribution/Data/Spawns/**/*.json`, then reading their map and location fields. Selected files supporting the places named in the guide, relative to `Distribution/Data/Spawns/`:

- `shared/trammel/WildLife.json`: horse.
- `shared/trammel/LostLands.json`: horse, RidableLlama, DesertOstard, ForestOstard, FrenziedOstard, SwampDragon.
- `shared/tokuno/WildLife.json`: horse, RidableLlama.
- `post-uoml/malas/South.json`: DesertOstard, Nightmare.
- `shared/ilshenar/Outdoors.json`: DesertOstard, ForestOstard, Ridgeback, Unicorn.
- `shared/ilshenar/Towns.json`: SavageRidgeback.
- `shared/trammel/SolenHive.json` and `shared/felucca/SolenHive.json`: Beetle.
- `shared/tokuno/YomutsoMines.json:53`: FireBeetle. The source filename spells it Yomutso; the guide uses the familiar Yomotsu Mines name.
- `shared/trammel/TerathanKeep.json`: Nightmare.
- `shared/ilshenar/Ankh.json`: Nightmare and Kirin.
- `shared/malas/North.json`: Unicorn.
- `shared/tokuno/Outdoors.json`: LesserHiryu and Hiryu.
- `shared/ilshenar/TwistedWeald.json`: CuSidhe.
- `shared/malas/Labyrinth.json`: Reptalon.

No FireSteed, SilverSteed, or ScaledSwampDragon entry was found in that upstream JSON tree. FireSteed does have the actual DeceitBrazier construction path, so the draft describes that path with unverified placement. A class existing or a spawn JSON entry existing does not establish a live spawn. Search results are not used to promise every possible mount or spawn route is cataloged.

Additional rules and routes:

- `Projects/UOContent/Mobiles/Vendors/SBInfo/SBAnimalTrainer.cs:14-18`: sells Horse, PackHorse, PackLlama as distinct purchases. `Mobiles/Animals/Misc/PackHorse.cs:10` and `PackLlama.cs:10` derive from BaseCreature, not BaseMount.
- `Projects/UOContent/Mobiles/Animals/Mounts/BaseMount.cs:207-340`: ownership, adjacent range, poison, dead pet, rider gender, transformation, trade, forbidden region, mount block, Gargoyle checks. The guide uses a client dismount action rather than promising a particular hotkey.
- `Projects/UOContent/Mobiles/Vendors/NPC/AnimalTrainer.cs:203-280`: stable ownership, living status, pack load, combat, capacity, fee, and claim instructions.
- `Projects/UOContent/Mobiles/BaseCreature.cs:1389-1397, 3520-3543, 4580-4613`: bonding and dead pet behavior. Bonded does not mean immortal.
- `server/customizations/Services/Pet Training/BaseCreature.PetTraining.cs:90-141, 192-279`, `PetTrainingHelper.cs:688-775`, and `server/patches/AnimalTaming-pet-training.patch`: stock constructor follower costs are not a reliable final table; trained requirements use CurrentTameSkill. The guide therefore gives base taming figures and directs players to Animal Lore for individual animals.
- `Projects/UOContent/Engines/Factions/Mobiles/FactionWarHorse.cs:7-8, 79-104`; `Mobiles/Vendors/FactionHorseVendor.cs:37-59`; `Gumps/HorseBreederGump.cs:48-104` within that Factions directory: 500 silver, 3,000 gold, matching faction, rank 2 to ride, follower capacity. No running faction vendor was checked.

## Other rewards

- Veteran reward table: `Projects/UOContent/Engines/Veteran Rewards/RewardSystem.cs:392-554`; enabled and 30-day defaults at 560-562; access/age checks at 72-104 and 178-237. Each level was read beside its entries, including the rideable polar bear at level 9.
- `Projects/UOContent/Mobiles/Animals/Mounts/Ethereals.cs:30-39, 80-123, 188-235, 267-310, 316-394`: blessed item, one follower slot, reusable mounting/dismounting, validation and interruptible casting. Read the concrete figurine classes too; do not apply living Unicorn, Kirin, or CuSidhe rider rules to them.
- `server/customizations/Mobiles/Mule/MuleErrand.cs:24-27, 47-73, 85-126` and `LeagueRegistrarGump.cs:146-152`: Dull Copper errand, ore/ingot amounts, collection. The larger progression stays linked to the existing companion guide.
- `server/customizations/Mobiles/Bosses/ChiefParoxysmus.cs:99-102` and `MonstrousInterredGrizzle.cs:109-112`: actual 5% statuette drops.
- `server/customizations/Items/Addons/ParoxysmusSwampDragonStatuette.cs:12-24` and `Mobiles/Normal/ParoxysmusSwampDragon.cs:13-30`: summon and DeleteOnRelease. Upstream `Projects/UOContent/Mobiles/Animals/Mounts/GrizzledMare.cs:16`: DeleteOnRelease.
- Upstream `Projects/UOContent/Items/Special/ML/BaseImprisonedMobile.cs:17-28`, `GrizzledMareStatuette.cs`, and `Gumps/ConfirmBreakCrystalGump.cs:14-55`: backpack, confirmation, control-master check, bond, and statuette consumption. This is distinct from both P365's immediate call and veteran reusable items.

## Open questions for publication

1. Which running shard build and published player package carry P277/P365? Not checked and not inferred from repository presence. P365 calls for actual riding checks, especially the drake, bear, riding wolf, and saddled horse. P277 also records the rider sitting low.
2. Does Chase approve P365's proposed routes, prices, and horse-level stats as final? The draft records implemented values without making that decision.
3. How should players earn tier 5/6 Tamer boxes? Default category mappings contain no Tamer entry. An explicit staff grant is not an unattended gameplay route. An administrator could customize mappings, but the running configuration was not inspected.
4. Does the Boss box award work in ordinary play now? [P263's Finding](cc-P263-noted-by-the-system-achievements.md) reports the event firing after deletion. The inspected source still calls `ClusterFLootBoxes.IsBoss` through `ClusterFRareSelfRepair.IsHighEndSource`, whose `Deleted: false` guard remains. This task did not reproduce the runtime failure or fix it. The guide flags the pool's availability instead of promising Harrower farming.
5. Should holders of the achievement before P365 receive a mount? `TryGrant` refuses already-earned keys before item delivery. No retroactive payout was found in the inspected mount/reward paths. No compensation or account changes were made.
6. What will the red riding dragon's player route and final abilities be? Both variants are still staff-only in inspected source.
7. Which upstream wild spawns, faction breeders, the Deceit brazier, and the two boss encounters are actually reachable? Source locations are given with an explicit live-world qualification. SilverSteed and ScaledSwampDragon acquisition remains unverified.
8. Are veteran rewards enabled at the 30-day default on the running shard? Year-based labels versus the shorter interval remain a presentation mismatch, already recorded in the companion guide.
9. The older achievement/shop and companion guides predate P365. Their missing mount rows are not evidence that P365's source routes are absent. This task adds the dedicated page and leaves those other pages unchanged.

These questions are nonblocking for a clearly labeled draft. No approval or player-facing balance decision is invented.

## Validation

Lane tests: none, as requested. No new tests or gates were added, so there is no failing-first test cycle. No code build was needed for Markdown-only changes. Shell reports Windows PowerShell 5.1.26100.9711.

Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE pointed at these work copies. Exit 0. Its shard-wide content counts are not used as mount-availability evidence.

Found an existing helper defect, ours to fix in a separate code task: despite its documented print-only behavior, dry-run writes `tools/progress.json`. Evidence: `tools/progress.py:722` writes inside build(), called at 732 before the dry-run return at 737. The generated timestamp and queue changes appeared in git diff immediately after the run. Restored that generated file to the initially clean HEAD content, then confirmed its diff was empty. No helper fix was made in this documentation task.

Reviewed the guide against the source tables and confirmed coverage of every P365 definition listed above. All relative Markdown links in the deliverables resolve. The files have no em dashes or trailing whitespace and are each below 5 MB. Both repositories pass git diff --check. The code repo is clean; the only docs-repo changes are the guide and the two P526 notes files named above.

P526 DONE
