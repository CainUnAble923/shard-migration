# P590: Sorcerer's Dungeon Halloween player guide

Date: October 25, 2026. Documentation only.

## Deliverables

- `notes/wiki-drafts/sorcerers-dungeon.md`: player guide covering the location, default season and duration, shared room progression, bosses, artifact awards, turn-ins, reward prices and uses, and what remains after the season.
- This file is the Golem handoff note at the path specified in the lane instructions.
- `notes/cc-P590-guide-sorcerers-dungeon.md` preserves the separate notes path requested in the embedded task and links here.

Read both work copies' AGENTS.md, the direction decision, and the task list. Read P408's implementation notes and Codex review, P461's source review, and the current event implementation. No code, published wiki page, or docs/ file was changed.

## Source evidence

Event paths below are relative to `ShatteredLegacy/server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/`.

| Guide claim | Source checked |
| --- | --- |
| Ilshenar location, Researcher placement, season linkage | `Generate.cs:44`, `Generate.cs:58`, and `Generate.cs:162`; pinned `D:/UO/ModernUO-pinned/Distribution/Data/regions.json:3324` gives entrance 546,455. |
| Default October 24 through November 2; local date; hourly automatic transition | `server/customizations/ClusterFHalloweenDecorSeeder.cs:34` and `:35`; `server/customizations/ClusterFSeasonalSwitch.cs`, `Clock`, `OnWorldLoad`, `SeasonWindow.Contains`, and `Sync`. Ten inclusive calendar days counted from October 24 through November 2. These are defaults, not a verified live schedule. |
| Nine rooms and listed bosses; 80 deaths per room; repeat rotation and delay | `Spawner.cs:369` lists all nine entries; `OnTick` at `:185`, `OnCreatureDeath` at `:273`, and `Reset` at `:283` implement progress and the one-to-three-minute delay. |
| Jack's retaliation, timed hatching, fallible carving | `Creatures/JackThePumpkinKing.cs`, `OnDamage`, `CreatePumpkin_Callback`, `UnholyPumpkin.Carve`, and `SpawnTimer`. |
| Looting rights, living-player eligibility, hidden tally, Luck and fame, delivery fallback | `SorcerersDungeonData.cs`, `OnCreatureDeath` and `ProcessKill` at `:127`; delivery at `:164`, reset at `:177`. `EnchantedOriginArtifacts.cs`, `CreateForKill`, `Create`, and `Mark`, establish the equipment award and marker. |
| Backpack top level, context-menu turn-in, consumption, one point | `server/customizations/Mobiles/NPCs/BaseTurnInMobile.cs`, `FindRedeemableItems`, `TurnInPoints`, `TurnInEntry`, and `TurnInGump.HandleButtonResponse`; `SorcerersDungeonResearcher.cs:78` and `:84`. |
| Seven offered rewards and prices | `SorcerersDungeonRewards.cs:33` through `:40`: JacksBagOfTricks 75, SerpentsJawbone 50, JackInTheBox 20, ShackledHeartOfThePumpkinKing 20, SterlingSilverRing 50, TalonsOfEscaping 50, BootsOfEscaping 50. The same list explicitly omits the three title deeds. |
| Ring, skill choices, footwear | `Items/EscapingAndSterlingRewards.cs:24`, `:37`, `:49`, `:78`, and `:91`; includes the client label spelling. |
| October-only bag, full-day cooldown, treat chance and six oddities | `Items/JacksBagOfTricks.cs`, `OnDoubleClick` at `:35`, especially `NextUse` at `:67`. |
| Toy and harmless heart | `Items/JackInTheBox.cs`, `OnDoubleClick`; `Items/ShackledHeartOfThePumpkinKing.cs`, `OnDoubleClick` and `InternalTimer.OnTick`. |
| Jawbone house placement and travel restrictions | `server/customizations/Items/Functional/SerpentsJawbone.cs`, `OnDoubleClick`, `Locations`, and `InternalGump.CheckTravel`. |
| Post-season turn-ins and spending; retained objects and points | `Generate.cs:218` (`Down`) leaves the Researcher and dressing; neither Researcher redemption nor reward access checks season state. `SorcerersDungeonData.Serialize` and `EnchantedOriginArtifacts.Serialize` retain balances and artifact registration. Reviewed item implementations have no seasonal deletion. |

## Limits and editorial decisions

This is a source-checked draft, not a claim of deployment or client verification. Running settings, actual event availability, entrance accessibility, client labels and animations, combat balance, and a purchase walkthrough remain unverified. No connection to Haven, deployment, Docker operation, or account action was made.

The existing published wiki source, `docker/wiki/content/pages/uo/world/sorcerers_dungeon.txt`, was read for context and left untouched. This draft avoids its blanket claim of unchanged OSI behavior. It states shard defaults and the missing title rewards directly.

P408 and P461 record unresolved cleanup, pet-victim eligibility, artifact-pool, purchase-confirmation, ring-confirmation, and timer-test concerns. This documentation task does not fix or retest them. The guide makes no promise that shutdown removes every enemy, that the artifact pool exactly matches OSI, or that pet deaths are excluded correctly. It describes the ring's intended single choice without offering the queued-confirmation loophole as a feature. No invented route from a moongate, special entry quest, guaranteed boss artifact, or additional reward was added.

## Validation

Lane tests: none requested. No new tests or gates were added, and no build or gameplay tests were run for this documentation-only change. Manually cross-checked the guide against the source evidence above, including all reward rows and the October-only bag restriction.

Ran the required progress reporter against the work copies through `tools/progress.py --dry-run`. Its unconditional `tools/progress.json` write was suppressed in memory, preserving the requested documentation-only scope. The reporter completed; its inventory remains a source inventory, not runtime evidence. No progress output file, README, or dashboard was changed.

Final checks: only the guide and the two requested notes paths are added; code work copy remains clean. Files are below 5 MB, use plain American English and no em dashes, and pass whitespace review. Completion markers are appended only after these checks finish.

P590 DONE
