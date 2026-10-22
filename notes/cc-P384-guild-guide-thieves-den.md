# P384: Thieves' Den player guide draft

Task date: October 21, 2026. Codex lane, Verite work copies. Documentation only.

## Deliverable and scope

Wrote [wiki-drafts/thieves-den.md](wiki-drafts/thieves-den.md), following the player-facing structure of P374's League draft. It covers joining, character ownership of membership and balances, all Den ranks, the Apprentice shortcut, standing income, the eight associated skills, monster stealing, Hiding and Stealth, Remove Trap, the eight deployable kits, stolen-material recipes, mule schematics, starter rewards, scrip, and the chapter and planned headquarters.

The page ends with separate Sources and Contradictions lists. File:line evidence belongs here. It contains no staff commands, exploit instructions, or hidden-achievement spoilers. Proposed Gilded Lockpicks, Shadow Cloak IV, speculative higher-rank stealing bonuses, and undecided recipe upgrades are not advertised as available rewards. The future headquarters and additional custom dungeon access are labeled (planned).

Only this note and the requested draft are deliverables. No source code, tests, docs/ files, services, or world state changed. No Haven connection, Docker operation, build, deployment, commit, merge, push, or branch switch.

## Reading inventory

Read both work-copy AGENTS.md files first, then migration `docs/README.md`, `docs/direction-decision.md`, and `docs/tasks.md`. Read `notes/wiki-drafts/league.md` as the page model. Read the relevant `docs/feature-queue.md` entries: F-9's starter items, membership decisions, skills and lookout; F-32's decided but future dungeon-chest currency; F-33's Shadow Cloak; F-47's requisitions; F-48's link to stealing family parts; F-49's headquarters. Also checked the incidental F-37 reference to Thieves and Infamy; no Infamy mechanics are promised by this page.

Searched top-level `notes/cc-P*.md` case-insensitively for `thiev.*den`, before creating this note. The 21 pre-existing matching files are enumerated below. Read their Den passages and surrounding relevant sections, with deeper implementation/design reading in P15, P22, P70, P142, P151, P201, and P275. This is a focused guild audit, not a claim to have audited the unrelated systems elsewhere in those files.

| Matching note | What was read for this task |
|---|---|
| `cc-P14-newhaven-guild-mapping.md` | Den mapping, Stealing 20, and original starter task. |
| `cc-P142-monster-stealing-shard-rules.md` | Built rank/location ladder, chance curve, retry, loot, components, recipes, gains, persistence, tests, proposals, and later Burrows adjustment. |
| `cc-P146-playtest-decisions-inbox.md` | P142 decisions ledger, including the ladder, curve, cooldown, loot, and proposed recipes. |
| `cc-P15-guild-starter-path.md` | Joining, Apprentice task, starter reward ledger, inn placement, trainer referrals, and verification. |
| `cc-P150-requisitions-and-leads.md` | Den item themes and requisition rewards. |
| `cc-P151-guild-halls-survey.md` | Survey-only scope, Den town, proposed Bath site/facet, and unresolved facet question. |
| `cc-P177-guild-menus-template-mockups.md` | Den uses the common hall page, without a separate guild menu. |
| `cc-P195-port-exodus-encounter.md` | Zealot special rewards, location exception, and its conflicting rank description. |
| `cc-P201-deployable-traps-design.md` | D1-D7, skill roles, rank perks, placement, visibility, traps, training proposal, and prerequisites. |
| `cc-P217-crystal-wiki-catch-up.md` | Monster stealing, guild, Wren, and Burrows availability snapshot and stealing references. |
| `cc-P22-small-features-1.md` | Wren, stool, referral behavior, placement policy, and tests. |
| `cc-P224-playtest-bot-checks-second.md` | Den membership and stealing fixtures in the disposable test-world account; not evidence of live deployment. |
| `cc-P26-animated-runestone.md` | Wren's name, stool wording, and source check. |
| `cc-P275-deployable-traps-build.md` | Built trap rules, every kit, rank perks, tutorial lesson, verification record, design differences, and undeployed status. |
| `cc-P378-playtest-plans-10-21.md` | P275 scenarios for crafts/gates, effects, presence, rank limits, concealment, salvage, decay, and practice nets. These are plans, not test passes. |
| `cc-P382-guild-guide-order-of-the-alembic.md` | Thief's Smoke Bomb has its own recipe, outside normal craft book/rotation counts. |
| `cc-P41-companions-research.md` | Earlier unverified concern about moving a hidden mule. |
| `cc-P47-league-research.md` | Den's generic scrip and Shadow Cloak craft/secondary skill proposal. |
| `cc-P49-dungeon-chests-research.md` | Earlier Apprentice-only scrip income, replacements, and proposed dungeon chest scrip. |
| `cc-P51-staff-hub-and-raptor-pack.md` | Seeder hall anchors exclude the lookout; no player travel service inferred from it. |
| `cc-P70-mule-modules.md` | Shadow Cloak effects/materials, crafting, schematic ranks/prices, and module prerequisites. |

`rg` is unavailable in this shell, so searches used PowerShell Select-String and Python pathlib/regular expressions. PowerShell reported version 5.1.26100.9444. No PowerShell 7 executable or syntax was used. A broad search for nested AGENTS.md encountered access-denied scratch-cache directories under notes/__pycache__; the requested notes and wiki-drafts directories were readable, with no additional AGENTS.md found on their ancestor paths.

## Source evidence for the page

Prefixes in this section: C = this prompt's ShatteredLegacy work copy; M = this prompt's shard-migration work copy; U = read-only `D:\UO\ModernUO-pinned`. Verified U HEAD is `d4531cd94b739613155225c234900de9f47d2c88`, the required pin. Custom source paths are canonical. Nothing under server/uo/ was read.

### Joining, ranks, starter rewards, and hall

| Claim | Source |
|---|---|
| Den definition, base Stealing 20 Apprentice task, 25 standing and 10 scrip | C `server/customizations/ClusterFGuildSystem.cs:165`, `:333`, `:382`, `:412`. |
| Free joining, tools, per-character membership and balances | C `server/customizations/ClusterFGuildSystem.cs:69`, `:309`, `:427`; `server/customizations/ClusterFGuildStarterPath.cs:271`. |
| Apprentice task raises rank without requiring 1,000 standing | C `server/customizations/ClusterFGuildSystem.cs:669`, `:690`; test `server/tests/Misc/GuildStarterPathVerification.cs:666`. |
| Generic rank thresholds/names: 0, 1,000, 5,000, 15,000, 50,000, 100,000 | C `server/customizations/ClusterFGuildSystem.cs:618`, `:749`. |
| Den is not a craft-owning guild, so its ladder is not subject to craft promotion skill caps | C `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:389`, `:423`; `server/customizations/ClusterFGuildPromotion.cs:101`. |
| Eight associated skills | C `server/customizations/ClusterFGuildStarterPath.cs:55`. |
| Joining gives creation items through the shared item routine | C `server/customizations/ClusterFGuildStarterPath.cs:284`, `:305`; `server/customizations/CharacterCreation.cs:708`. |
| Den starter quest mapping | C `server/customizations/ClusterFGuildStarterPath.cs:103`. |
| No starter skill gate, shared trainer/guild ledger, once per character/current life | C `server/customizations/ClusterFGuildStarterPath.cs:12`, `:335`, `:377`, `:405`, `:435`. |
| Both rewards exist and the quests make them | U `Projects/UOContent/Engines/ML Quests/Definitions/NewHavenSkillTraining.cs:437`, `:456`, `:460`, `:479`; `Projects/UOContent/Items/New Haven Quest Rewards/BagOfSmokeBombs.cs:6`; `Projects/UOContent/Items/New Haven Quest Rewards/TwilightJacket.cs:6`. |
| Ordinary smoke bombs require Ninjitsu 50 and 10 mana; jacket is blessed | U `Projects/UOContent/Items/Skill Items/Ninjitsu/SmokeBomb.cs:14`, `:21`, `:31`; `Projects/UOContent/Items/New Haven Quest Rewards/TwilightJacket.cs:11`. |
| Lost reward replacement costs 10 scrip and refuses an owned copy | C `server/customizations/ClusterFGuildStarterPath.cs:269`, `:442`, `:456`, `:494`, `:506`. |
| Inn and lookout coordinates/facet | C `server/customizations/ClusterFGuildStarterPath.cs:219`, `:242`. Inn: Trammel 3495,2515,27. Wren: Trammel 3440,2558,56. Coordinates are evidence here; page uses landmarks. |
| Wren's name, referral, and range | C `server/customizations/ThievesDenLookout.cs:26`, `:35`, `:64`, `:119`. |
| Talk, Join, starter, schematics, Apprentice, and requisition menu labels | C `server/customizations/ClusterFGuildSystem.cs:778`, `:1080`, `:1088`, `:1119`, `:1126`, `:1145`, `:1184`. |
| Directory points to a present guildmaster, not just an empty coordinate | C `server/customizations/ClusterFGuildStarterPath.cs:245`; test `server/tests/Misc/ThievesDenLookoutVerification.cs:83`. |
| NPC placement is explicit, not proof of live presence | C `server/customizations/ClusterFGuildHallSeeder.cs:13`, `:38`, `:70`. |
| Headquarters town decided, chapter retained; facet/building not decided | M `docs/feature-queue.md:3394`, `:3412`, `:3424`, `:3431`; survey M `notes/cc-P151-guild-halls-survey.md:194`, `:206`, `:365`. |

### Stealing, recipes, and standing income

| Claim | Source |
|---|---|
| Targeting a creature reaches the monster-reward handler after normal pack theft | C `server/patches/Stealing-monster-stealing.patch:1`; the hunk adds the BaseCreature/PlayerMobile call after the existing mobile pack branch. |
| Initiate/Felucca/champion/Burrows, Journeyman/other facets, Master/bosses | C `server/customizations/Services/Monster Stealing/Core/ThievesDenStealRules.cs:49`, `:104`, `:151`, `:193`. |
| Future custom dungeon set is empty | C `server/customizations/Services/Monster Stealing/Core/ThievesDenStealRules.cs:67`. No built destination invented for that rank slot. |
| Exclusions, including creatures in the Vault | C `server/customizations/Services/Monster Stealing/Core/ThievesDenStealRules.cs:173`. |
| No ordinary wilderness access at Master; Exodus zealot exception | C `server/customizations/Services/Monster Stealing/Core/ThievesDenStealRules.cs:193`, `:200`, `:207`; `StealingHandler.cs:123` gives a zealot ritual keys rather than the normal special table. The exception is recorded here and in Contradictions, without expanding this guild guide into the Exodus walkthrough. |
| Skill 60 floor, 100 special tier, curve through 200, fame bonus | C `server/customizations/Services/Monster Stealing/Core/StealingHandler.cs:52`, `:167`, `:182`, `:239`, `:254`. |
| One successful reward per creature; miss timer, reveal, aggro; gain on legal attempts | C `server/customizations/Services/Monster Stealing/Core/StealingHandler.cs:137`, `:206`, `:215`, `:222`, `:296`. The page distinguishes the creature retry timer from the ordinary skill delay. |
| Minor rewards, 1-3 scrip, special pools, component progression, family parts | C `server/customizations/Services/Monster Stealing/Core/StealLootTables.cs:31`, `:107`, `:115`, `:158`, `:190`, `:217`, `:247`; special consumables enumerated by `StealingHandler.cs:35`. |
| Den recipe scrolls and Shadow Cloak I-III can be stolen | C `server/customizations/Services/Monster Stealing/Core/StealLootTables.cs:47`, `:190`; `server/customizations/Engines/Craft/ClusterFRecipeTable.cs:98`. |
| All three craft minima 100, materials and own recipe IDs | C `server/customizations/Engines/Craft/ThievesDenCraftRegistrations.cs:27`, `:31`, `:60`, `:68`, `:77`. IDs: 9400 cloak, 9401 bomb, 9402 charm. |
| Cloak +5 Stealth/+3 Hiding; charm +5 Stealing/+5 Snooping; bomb Hiding 50/10 mana/combat override | C `server/customizations/Services/Monster Stealing/Items/ThievesDenRecipeItems.cs:18`, `:33`, `:48`, `:57`. |
| Own recipes and books are distinct; Den owns no craft skill | C `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:10`, `:389`. No Den pattern-book shop or promotion grants invented. |
| Ordinary Hiding can be blocked by combat; Stealth needs hiding and is affected by armor | U `Projects/UOContent/Skills/Hiding.cs:53`, `:73`; `Projects/UOContent/Skills/Stealth.cs:71`, `:89`. |
| Den requisition themes | C `server/customizations/Requisitions/RequisitionTable.cs:294`. |
| Turn-in consumes item and awards standing, Renown, gold, not scrip | C `server/customizations/Requisitions/RequisitionSystem.cs:218`, `:245`, `:249`, `:252`. |

The page avoids converting creature Fame to player-facing numeric component thresholds. P142's round-number examples do not precisely match the integer-truncated FameLevel formula (`StealingHandler.cs:290`); only the checked qualitative ordering is used.

### Mule schematics

| Claim | Source |
|---|---|
| Shadow Cloak is a Den mule module, distinct from the wearable cloak | C `server/customizations/Mobiles/Mule/MuleModuleData.cs:101`; wearable `server/customizations/Services/Monster Stealing/Items/ThievesDenRecipeItems.cs:15`. |
| Buy ranks 1/2/4, costs 20/50/120 scrip plus 5/10/25 Mining Vouchers | C `server/customizations/Mobiles/Mule/MuleModuleGumps.cs:475`, `:479`, `:483`, `:539`. |
| Schematics teach account recipe knowledge; requirements apply to purchase | C `server/customizations/Mobiles/Mule/MuleModuleGumps.cs:492`, `:562`; stolen keys in `StealLootTables.cs:47`. |
| Tailoring 50/70/90, Hiding 30/50/70, previous tier required for upgrade craft | C `server/customizations/Mobiles/Mule/MuleModule.cs:168`, `:213`, `:265`, `:293`. |
| Effects, owner proximity, walking/unmounted condition, III's 30-second cooldown | C `server/customizations/Mobiles/Mule/MuleModules.cs:423`, `:438`, `:597`. |
| Fit requires ownership, mule tier, and free slot | C `server/customizations/Mobiles/Mule/MuleModules.cs:122`. |

### Deployable traps

| Claim | Source |
|---|---|
| Eight kinds and skill gates | C `server/customizations/Items/Traps/Deployable/DeployableTraps.cs:37`, `:81`, `:202`. The eight page rows enumerate the whole AllKinds list at `:51`. |
| Tinkering registers each kit, with stock craft ceiling 130 | C `server/customizations/Engines/Craft/TinkeringCraftRegistrations.cs:121`, `:137`, `:161`. |
| Loading gas/blast/darts, Poisoning check and potion consumed on failure | C `server/customizations/Items/Traps/Deployable/DeployableTrapKit.cs:68`. |
| Ground target range 2, mounted/flying/skill/town/house/occupied checks | C `server/customizations/Items/Traps/Deployable/DeployableTraps.cs:65`, `:355`, `:410`. |
| Double-click backpack kit, target, arming canceled by movement/death | C `server/customizations/Items/Traps/Deployable/DeployableTrapKit.cs:261`, `:338`, `:364`, `:370`. |
| Hidden placement 1 second, stealth step/check, concealment +20 | C `server/customizations/Items/Traps/Deployable/DeployableTraps.cs:209`, `:231`; `DeployableTrapKit.cs:328`, `:379`. |
| First trigger ambush condition and rolled damage bonus | C `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:223`, `:368`. No unintended bypass or farming behavior is explained on the page. |
| Per-owner trap limit, Journeyman extra, spent traps counted; area cap | C `server/customizations/Items/Traps/Deployable/DeployableTraps.cs:206`, `:340`, `:398`, `:434`. |
| Monsters by default on every facet; owner presence, alive/login/map and 12 tiles; alarm distance exception | C `server/customizations/Items/Traps/Deployable/DeployableTraps.cs:59`, `:253`, `:277`. Page says default rules because the optional PvP setting exists, without telling players how to enable it. |
| Flyers/incorporeal restrictions, Master boss gate, alarm exception | C `server/customizations/Items/Traps/Deployable/DeployableTraps.cs:186`, `:266`, `:298`. Alarm returns before the boss rank check. |
| Trap effects and gain on firing | C `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:240`, `:355`. |
| Boss rolled damage and hold halved | C `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:368`, `:389`. This does not claim all poison/bleed effects are halved. |
| Owner/party visibility, Detect Hidden reveal | C `server/customizations/Items/Traps/Deployable/DeployableTraps.cs:328`; `DeployedTrap.cs:119`, `:450`, `:460`. |
| Spent and armed decay 2/30 minutes, reset by hand/payload, gains | C `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:113`, `:133`, `:473`, `:496`, `:522`. |
| Owner packs kit; stranger skill check, Grandmaster guaranteed salvage | C `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:538`, `:561`. |
| Endless Journey removes old 50 Lockpicking/50 Detect Hidden prerequisites | C `server/patches/RemoveTrap-trap-training-kits.patch:1`; its two guarded prerequisites use !Core.EJ and its interface forwards deployable targets. |
| Two tutorial nets, participant/rat lesson, temporary art | C `server/customizations/Items/Traps/Deployable/TrapLesson.cs:68`, `:84`, `:104`; `DeployableTraps.cs:154`. |

## Contradictions retained

The page records the following differences without editing the older notes or making a new design decision. Its playable descriptions are restricted to checked implementation; a source conflict is not permission to change the code.

1. **Joining:** M P14 `:135` describes Stealing 20 in the original join mapping. F-9 `docs/feature-queue.md:710`, P15's starter-path account, and C `ClusterFGuildSystem.cs:313`, `:382` separate free Initiate joining from the later Apprentice task.
2. **Missing starter rewards:** M P142 `:198` says both Den starter items do not exist and no jacket type exists. C `ClusterFGuildStarterPath.cs:103` maps the Den to the quests, and U NewHavenSkillTraining `:456` and `:479` construct both rewards. Their definitions and loot properties are cited above. No missing reward is invented or marked planned on the guide.
3. **Bosses anywhere:** M P142 `:104` uses that phrase. C `ThievesDenStealRules.cs:207` refuses uncovered places even for Masters. Its zealot exception at `:200` substitutes FacetDungeon, not universal boss access.
4. **Exodus rank:** M P195 `:311` says the zealot's first-rank rule holds because its rank is 0. C `ThievesDenStealRules.cs:200` assigns the uncovered-location zealot to FacetDungeon, which requires Journeyman at `:157`. C `StealingHandler.cs:123` then gives ritual keys on a special-tier steal. The page makes no Initiate zealot promise.
5. **Tier III schematic rank:** M P70 `:105` puts tier III at Master and flags the earlier recipe design's different rank. C `MuleModuleGumps.cs:477` uses index 4; C `ClusterFGuildSystem.cs:615`, `:749` make that Grandmaster for the Den.
6. **Scrip sources/spenders:** M P49 `:430` says Apprentice-only income and `:443` replacement-only spending. C `StealLootTables.cs:115` pays scrip; C `MuleModuleGumps.cs:479`, `:558` spends it on schematics. This is source history, not a claim the proposed dungeon chest system is built.
7. **Trap prerequisites/Apprentice perk:** M P201 `:80` retains the pre-EJ 50/50 prerequisites, `:110` also says Remove Trap 30 is enough generically, and `:115` describes an Apprentice hover. C RemoveTrap-training-kits.patch removes the prerequisites under EJ, C DeployableTraps `:86` permits a snare at Remove Trap 0, and M P275 `:208` records the hover as unbuilt. Party visibility is unconditional, C DeployableTraps `:328`.
8. **Grandmaster perk chronology:** M P142 `:105` says Grandmaster/Legendary open nothing more. M P201 `:121`, P275 `:52`, and C DeployedTrap `:561` add guaranteed Grandmaster disarm/salvage. No separate Legendary perk was found in these Den systems.
9. **Trap recipe and arming details:** P201's design folds payloads into craft, has damage interrupt arming (`:131`), and plans Tinkering to 160. M P275 `:201`, `:208`, `:223` records separate loading, omitted damage interruption, and the 130 craft ceiling. C DeployableTrapKit `:370` checks movement/death, and TinkeringCraftRegistrations `:134` caps the range.
10. **Shackle trigger:** M P275 `:70` describes the snare's skill-grown trigger reach. C DeployableTraps `:131`, `:182`, `:212` use the shackle's fixed area radius 1. The page simply calls it an area hold and does not choose a new trigger design.
11. **Headquarters:** F-49 `:3431` leaves facet/building open. M P151 `:194`, `:206`, `:365` propose Buccaneer's Bath on Felucca and ask for a facet decision. C GuildLocations, in ClusterFGuildStarterPath `:219`, lists the New Haven post. The page marks the headquarters planned and makes no Felucca/Bath travel promise.
12. **Availability snapshots:** M P217 `:56` calls monster stealing live, while `:58` calls the Burrows map unbuilt. M P275 `:35` says the map landed, and `:15` says no deployment occurred in that task. No live checks were made here. The opening draft notice preserves that limit.

Additional source discrepancies noted during reading, without adding extra mechanics to the page:

- M P142 `:158`, `:209` gives fame 7,500/15,000/22,500 as exact level 10/20/30 examples. C StealingHandler `:290` truncates the mapped result, making those examples inexact. The guide uses no invented fame cutoff.
- M P142 `:384` through `:387` says the own recipes can enter a general box recipe pool. C `server/customizations/LootBoxes/LootBoxRoller.cs:400` only selects stock recipe IDs below 9000 there; Den recipe IDs start at 9400. The guide claims monster stealing as a source without promising these scrolls from boxes.
- M P142 `:396` describes Balm of Protection as inert pending Grizzle or region consumers. A current C consumer exists at `server/customizations/Mobiles/Bosses/MonstrousInterredGrizzle.cs:269`. The page lists possible consumables without repeating the obsolete blanket claim of no damage reduction or promising general-purpose protection.

## Verification and limits

Read implementation bodies rather than relying on comments, names, or matching keywords. The source file lists accompanying the eight skills, eight trap kinds, and three recipe results are enumerated in the tables above and on the guide; no unmeasured content coverage totals are claimed.

Existing verification sources inspected:

- C `server/tests/Misc/GuildStarterPathVerification.cs:666`: free Den join, no join payout, base Stealing 20, Apprentice payout once. Also read the fixture's starter ledger/character ownership descriptions and reward checks.
- C `server/tests/Misc/ThievesDenLookoutVerification.cs:41`, `:83`, `:122`: placement, arrow, and non-trainer behavior.
- C `server/tests/Services/Monster Stealing/MonsterStealingVerification.cs:165`, `:192`, `:236`: place checks, reward attempts, and higher Stealing gains. Read its consumable and persistence test descriptions too.
- C `server/tests/Services/Monster Stealing/MonsterStealingShardRulesVerification.cs:150`, `:227`, `:293`, `:332`, `:372`, `:453`, `:539`, `:662`, `:694`: membership/rank/places, exclusions, odds, loot, recipe knowledge, misses, one success, and save flag. The guaranteed Grandmaster trap disarm is established by its implementation, not a claim of a dedicated assertion in these stealing tests.
- C `server/tests/Items/Traps/DeployableTrapsVerification.cs:200`, `:248`, `:287`, `:341`, `:408`, `:451`, `:485`, `:524`, `:560`, `:600`, `:678`, `:708`: defaults/PvP switch, presence, credit, reset/decay, skill use, rank limits, exclusions, placement, lesson, floor hazards, recipe gates, serialization. Test bodies and named assertions were checked for the guide's relevant behavior.
- C `server/tests/Mobiles/Mule/MuleModuleVerification.cs:78`, `:100`, `:137`, `:179`, `:312`, `:344`: module data/craft/attach/purchase behavior and hiding. Purchase ranks were verified against current source, not P70's older prose.

No tests were added or run. Lane tests are explicitly none, and this task changes only prose. Prior P142/P275 red/green records were read as history, not reported as tests run by P384. No claim of client verification, live deployment, live NPC placement, current configured overrides, or a full saved-world boot is made. Custom trap art appearance remains unverified here.

Ran the standing progress command as `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE pointing to these work copies: exit 0, report produced. Inspection showed that even dry-run writes tools/progress.json. Preserved its original bytes in memory and restored them afterward, verified byte-identical, so it is not part of the documentation deliverable and no README update was made.

Final review: both Markdown files have valid relative links, no em dashes, no trailing whitespace, and consistent table column counts. Full-path file:line citations resolve to existing files and valid line numbers. The guide has no file:line citations and its only gameplay command is the player-facing Guild Directory command. Read back the completed page, corrected source filename/line references, and kept numeric claims tied to the evidence tables above.

Both files are below 5 MB: the guide was 17,106 bytes at final review; this note is approximately 25 KB. Both repositories' tracked diffs were empty. Code git status was clean; docs git status listed only the two requested new notes files. No unrelated generated progress artifact remains. The stop-request flag was checked between research, drafting, review, and completion steps; absent at the final check.

## Timing

First recorded clock: 2026-10-22 02:10:04 UTC, October 21 at 9:10:04 PM CDT. Final review clock: 2026-10-22 02:25:17 UTC, October 21 at 9:25:17 PM CDT. Recorded research, writing, and review span: 15 minutes 13 seconds; total run approximately 15 minutes, including this closing note.

P384 DONE
