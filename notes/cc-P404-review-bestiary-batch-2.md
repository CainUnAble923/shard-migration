# P404: Review of League bestiary batch 2 (P364)

Reviewed October 22, 2026. Findings only. No code, tests, or existing documentation changed.

## Findings

1. **bug** - `server/customizations/ClusterFLeagueBestiary.cs:174`: A kill finished by a pet, summon, or provoked creature never records the player's first encounter or displays the bestiary lines, because the hook accepts only a `PlayerMobile` as `LastKiller`; pinned `Mobile.cs:6018` keeps the actual attacker, and `BaseCreature.cs:3992` provides `GetDamageMaster(victim)` for these cases. Resolve the attacker through that method before checking for a player, and add death-event tests for controlled, summoned, and provoked attackers alongside the existing direct-player case.

2. **risk** - `server/tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs:302`: The tests check a broad level band, parts, and boss jewelry, but do not assert the documented stat ranges, damage types, resistances, weapon abilities, poison chances, movement speeds, or ordinary loot and resource amounts, so changes such as removing the Hollow Oak's fire weakness or the lurker's fish can pass. Add focused checks against P364's creature table, including loot beyond the signature part and jewel.

3. **risk** - `server/tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs:61`: This fixture never calls `ShardTestHost.EnsurePoisons()`, so running it alone can calculate levels with null hit poisons and immunities, while running after another fixture that registers poisons exercises different values; the wide bands accept both and no test exercises poisoning or immunity. Call the existing helper before construction and add checks that use registered poisons to exercise the crawler's, thornwisp's, and Hollow Oak's poisonous hits and the four immune creatures' resistance to poisoning.

4. **risk** - `server/tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs:352`: The spawn test checks each spawner's settings and a second seed run, but never checks its spawned population or repeated spawn attempts, so an empty population or a regression that exceeds `row.Count` would escape this suite. Add a map-backed check that fills a row, repeatedly calls its ordinary spawn path, verifies the cap, and verifies that killing one creature permits only one replacement.

5. **nit** - `notes/cc-P364-league-bestiary-batch-2.md:290`: The live-level correction accounts for poison immunity but omits hit poison, so the same Hollow Oak stats recorded as level 74 gain 14 levels with registered poisons, not 10; the crawler also gains 2 and the thornwisp gains 4. Recalculate the displayed estimates with poisons initialized and correct the note's Hollow Oak estimate of 84 to about 88, allowing for randomized stats.

## What matched

I found no constructor stat or loot mismatch against P364 section 3, and no batch-2 creature missing from `ClusterFLeagueBestiary.Entries` or its spawn data. The following is the complete reviewed lineup, counted from the creature declarations, entries, and spawn rows rather than the note's totals.

| Creature type | Body | League table | Signature part per kill | Spawn coordinates and caps, Trammel |
|---|---|---|---|---|
| HedgeSnatcher | 2072 | Culling | SnatcherEars x1 | 3430,2700 x3; 3545,2395 x2 |
| SnatcherOutrider | 2073 | Hunt | SnatcherEars x2 | 3410,2745 x1 |
| HornbackRaider | 2074 | Hunt | HornbackHorn x1 | 3570,2380 x2; 3640,2400 x2 |
| DitchCrawler | 2075 | Culling | CrawlerMandible x1 | 3395,2690 x3; 3460,2725 x2 |
| MireCroaker | 2076 | Hunt | CroakerTongue x1 | 1190,2885 x3; 2065,1000 x2 |
| BrineLurker | 2077 | Culling | LurkerGills x1 | 5445,2030 x3; 5440,2023 x2 |
| Moonmaw | 2078 | Culling | MoonmawPelt x1 | 1059,1166 x3; 960,910 x2 |
| Thornwisp | 2079 | Culling | ThornwispSpark x1 | 960,910 x2; 837,361 x2 |
| PaleDrifter | 2080 | Culling | DrifterEctoplasm x1 | 5170,678 x3; 5139,661 x2 |
| Slagheart | 2081 | Culling | SlagCore x1 | 5699,1302 x2; 5859,1341 x2 |
| Glasswarden | 2082 | Culling | GlasswardenShard x1 | 5731,176 x2; 5681,191 x2 |
| Tunnelmaw | 2083 | Hunt | TunnelmawClaw x1 | 5474,20 x1; 5649,101 x1 |
| TheSiegebreaker | 2084 | Hunt, mini-boss | SiegebreakerTusk x3 | 5577,2006 x1 |
| TheHollowOak | 2085 | Hunt, mini-boss | HollowOakHeartwood x3 | 1010,1250 x1 |

There are fourteen creatures, with six hunt entries including the two mini-bosses, eight culling entries, and twenty-five spawn rows, all listed above. Both bosses pack a gold jewel; the remaining resource and loot-pack calls agree with P364's table.

I found no uncapped automatic spawn path. `ClusterFLeagueBestiary.cs:301` passes each row's finite count to stock `Spawner`; pinned `Engines/Spawners/BaseSpawner.cs:287` sets the entry limit to that count, `:292` checks the total population, and `:850` checks both limits before spawning. None of these creatures creates additional creatures, and the seeder skips an existing named spawner within three tiles as P364 describes (`ClusterFLeagueBestiary.cs:265`, `:285`); the missing behavioral regression test is finding 4.

The League draft's section beginning at `notes/wiki-drafts/league.md:53` marks hunts, culls, rewards, and the broader job board as planned. This agrees with P364's data-only implementation: recording `EncounteredCreatures` is bestiary credit, not a Renown, XP, guild-standing, or job-completion award, so the absence of those awards is not a batch-2 defect.

## Sources and limits

Read both work-copy `AGENTS.md` files and the direction and task documents before reviewing. Primary review sources:

- `notes/cc-P364-league-bestiary-batch-2.md`
- `notes/wiki-drafts/league.md`
- `server/customizations/ClusterFLeagueBestiary.cs`
- `server/customizations/Mobiles/Bestiary/HavenHuntCreatures.cs`
- `server/customizations/Mobiles/Bestiary/CullingPackCreatures.cs`
- `server/customizations/Mobiles/Bestiary/BestiaryMiniBosses.cs`
- `server/customizations/Mobiles/Bestiary/BestiaryParts.cs`
- `server/customizations/Mobiles/Evo/ShardBodyTypes.cs`, especially entries at lines 75 through 88
- `server/tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs`

Related sources checked were `ClusterFCreatureLevels.cs`, `ClusterFAchievements.cs`, `Requisitions/RequisitionLeads.cs`, `server/tests/Route/ShardTestHost.cs`, and the relevant patches. `RequisitionLeads.cs:221` already resolves a pet's owner for Lead credit, while the new bestiary hook does not.

Pinned source was read from `D:\UO\ModernUO-pinned`, verified at `d4531cd94b739613155225c234900de9f47d2c88`, without changes. Finding 5 follows `ClusterFCreatureLevels.cs:143` and `:153`, pinned `Items/Skill Items/Musical Instruments/BaseInstrument.cs:245` and `:247`, and `Misc/PoisonKinds.cs:81`: immunity adds 100 before division by 10, and regular hit poison adds 40 before that division; these are source calculations, not live measurements.

No tests were added or run, as this task specifies no lane tests and requests review notes only. Runtime reproduction of the findings, actual map placement and spawn populations, client animation and corpse appearance, deployed state, and full player-package completion remain unverified; P364 itself records the interrupted package build. No Haven connection, deployment, build, or branch operation was made.

Ran `tools/progress.py --dry-run` with the local work-copy path overrides and filesystem writes suppressed in memory, because its `build()` otherwise writes `tools/progress.json` even in dry-run mode. It completed successfully; this review changes only this notes file.

P404 DONE
