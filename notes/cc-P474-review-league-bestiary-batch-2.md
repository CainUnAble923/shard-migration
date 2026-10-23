# P474: Second review of League bestiary batch 2 (P364)

Reviewed October 23, 2026. Notes only. Read P364's implementation notes and P404's review before checking the current source; the findings already in P404 are excluded here.

## Finding

1. **bug** - `server/customizations/Mobiles/Bestiary/HavenHuntCreatures.cs:85` and `server/customizations/Mobiles/Bestiary/BestiaryMiniBosses.cs:91`: The outrider's mounted pace and the Hollow Oak's lumbering pace change only the AI decision timers, while both inherit the same base movement intervals as a hedge snatcher, 0.45 seconds active and 1.05 seconds passive. Set `ActiveMoveSpeed` and `PassiveMoveSpeed` explicitly for each creature so the outrider moves faster than its pack and the Oak moves at the intended slower pace.

The movement finding follows pinned ModernUO at `d4531cd94b739613155225c234900de9f47d2c88`, whose working tree was clean. `Projects/UOContent/Mobiles/NPCSpeeds.cs:30` falls back to Medium for these unregistered types, and `Distribution/Data/npc-speeds.json:32` supplies nonzero movement intervals. `Projects/UOContent/Mobiles/BaseCreature.cs:825` loads those intervals during construction; `:1134` and `:1138` prefer them over the later `ActiveSpeed` and `PassiveSpeed` assignments. `Projects/UOContent/Mobiles/AI/BaseAI/AIMovement.cs:85` uses that movement value and `:117` schedules the next step. This is a concrete movement-setting defect, separate from P404's general test-coverage finding.

## Other checks and limits

I found no other new source-backed stat-range, loot, or spawn-location issue. Constructor ranges, damage splits, resistances, signature parts, ordinary resource amounts, and loot-pack calls agree with P364's proposal table. The bosses' Rich plus Average loot also matches pinned Cyclops loot, so that combination alone is not evidence of excessive payment. Actual farming income and group difficulty remain unverified.

Reviewed these canonical files and their related pinned implementations:

- `server/customizations/ClusterFLeagueBestiary.cs`
- `server/customizations/Mobiles/Bestiary/HavenHuntCreatures.cs`
- `server/customizations/Mobiles/Bestiary/CullingPackCreatures.cs`
- `server/customizations/Mobiles/Bestiary/BestiaryMiniBosses.cs`
- `server/customizations/Mobiles/Bestiary/BestiaryParts.cs`
- `server/customizations/Mobiles/Burrows/BurrowsCommon.cs` (`BurrowsLoot.RandomJewel`)
- `server/customizations/Mobiles/Evo/ShardBodyTypes.cs`
- `server/tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs`

Also checked the related body records in `player-package/vendor/shattered-legacy-art/registry.csv`, `records.json`, and `SOURCE.txt`, the presence and sizes of `anim-src/bodies/2072.vd` through `2085.vd`, and the body collision fact in `player-package/tests/Build-UoOverrides.Tests.ps1`. Spawn coordinates were compared with pinned `Distribution/Data/Spawns/shared/trammel/` data for Outdoors, Covetous, Deceit, Fire, Ice, and Shame. Stock spawn provenance does not prove current walkability or reachable populations; those, client animation, measured movement, deployed configuration, and full player-package completion remain unverified.

No code or tests changed. No tests or builds ran, as this prompt requests review notes only and specifies no lane tests. No Haven connection, deployment, commit, or branch operation was made. Ran `tools/progress.py --dry-run` with the work-copy path overrides and its `progress.json` write suppressed in memory; it completed successfully without changing generated files.

P474 DONE
