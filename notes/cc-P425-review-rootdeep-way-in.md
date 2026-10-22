# P425: Rootdeep Burrows way-in review

Reviewed 2026-10-22. Notes only; no code changes.

Read `cc-P188-cont-rootdeep-goes-in.md` and its listed entrance, seeder, spawn exclusion, region, map applier, package, overlay, status and test changes. No separate P188 Codex review was found beside that note or among the tracked review notes. Also read the queued P413 prompt and checked relevant behavior against pristine ModernUO at `d4531cd94b739613155225c234900de9f47d2c88`.

Paths below are relative to the code repo unless prefixed `shard-migration/` or `ModernUO-pinned/`. Runtime failure scenarios are source-based risks, not reproduced player incidents.

## Findings

1. **risk**, `server/customizations/ClusterFRootdeepSeeder.cs:179` and `:308`: `MapBuilt` gates seeding only, so after saving these active stock teleporters, starting the same world without the overlay leaves the down teleporter sending players to the unbuilt interior; `ModernUO-pinned/Projects/UOContent/Items/Misc/Teleporter.cs:245` moves them without checking the destination, and `docker/uo/Start-TestShard.ps1:164` explicitly supports an overlay-free start. Refuse entry or refuse that startup when the saved entrance exists but the required map is absent, and cover the seeded-world-to-missing-overlay transition with a test.

2. **risk**, `server/customizations/ClusterFRootdeepSeeder.cs:235` and `:318`: a saved teleporter with the old destination is not recognized after a destination change, so rerunning the seeder adds a second one at the same source tile and leaves the old one active; P413 must change the current return point if its wider opening covers `(3619,2621)`. Give P413 an explicit dry-run-capable upgrade of the known P188 items, and test an old seeded world followed by the upgrade and a second run, rather than only two runs of the new table.

3. **risk**, `server/customizations/ClusterFRootdeepSeeder.cs:316`: the lookup accepts an inactive teleporter or one at the wrong source Z as already present, so reseeding can report the only walking exit as present while it remains unusable; `ModernUO-pinned/Projects/Server/Maps/Map.ItemEnumerator.cs:55` discards Z for this range query. Validate the source height, active state and expected stock teleporter behavior, report conflicting items, and add disabled-exit and wrong-height cases to the seeder tests.

4. **bug**, `shard-migration/notes/cc-P188-tools/build_way_in.py:94` and `:109`: the route helper averages the minimum and maximum corner heights and uses full surface height, while `ModernUO-pinned/Projects/Server/Maps/Map.cs:282` averages the selected diagonal and `ModernUO-pinned/Projects/UOContent/Engines/Pathing/Movement.cs:323` uses `CalcHeight`, which halves bridges, so its route report can disagree with server movement on P413's raised mound. Use the pinned height and surface rules or prove the route with actual server movement; a read-only probe of the helper returned Z 2 for corner heights `(4,4,0,4)` where pinned's formula returns Z 4, enough to change a two-unit step decision.

5. **risk**, `server/tests/Regions/RootdeepWayInVerification.cs:116` and `:177`: W1 forces map readiness and calls `OnMoveOver` directly, so it can pass when the opening or ladder approach cannot actually be walked onto, and its player/skeleton checks leave following pets and ghosts uncovered. Add movement through the applied map from outside each opening tile and back out from the ladder, including a following pet and ghost, and verify that the return tile is walkable and outside every down trigger.

## What P413 must preserve

- Keep the collapsed south-wall passage at `(3618-3620,2622)` usable from New Haven, and recheck the entire mound and approach against the nearby undead walking boxes; the old report proves only the old route and hole.
- Keep the arrival at `(5193,1138,0)` and the return trigger at `(5193,1132,0)` accessible. The ladder artwork at `(5193,1131)` is a wall decoration, not the tile players step onto.
- Move the return landing outside the enlarged opening and mound obstructions. The existing `(3619,2621)` lies inside a three-by-three opening centered on the current hole; `TeleporterRow.At` and `.To` also hardcode Z 0 at `ClusterFRootdeepSeeder.cs:64`, so raised walking surfaces require an explicit height decision.
- Update `OldHavenBurrowsRegion.HoleEntrance` and its tests if the entrance moves. `OldHavenBurrowsRegion.cs:62` uses it for the dungeon entrance, including Young death routing, independently of the seeder's coordinates.
- Preserve every unrelated operation in the combined `player-package/vendor/shattered-legacy-map/trammel.mapops`, especially P276's farm tree removals at lines 11537-11540. Regenerating from a P188-only scratch map would drop those later changes; replace the old hole operation at line 11544 rather than stacking new artwork over it.
- Keep the Old Haven crier exclusion and the surviving skeleton spawner unchanged. Render and validate the same final map operations that both the player package and server overlay consume.

## Checks and limits

By source inspection, no duplicate placement was found for an unchanged, clean seeder rerun. No conflicting land writes or identical duplicate static operations were found in the current shipped map patch; the farm removals and entrance wall removals occupy separate locations. The saved-world upgrade and damaged-item cases above are not covered by W1 or V5.

- `player-package/tests/Map-Overrides.Tests.ps1`: all seven existing facts passed under Windows PowerShell 5.1.
- `shard-migration/tools/tests/test_mapops.py`: the three synthetic tests and shipped-patch scope test passed, including the Python/PowerShell byte comparison. The runner used this work copy's applier and patch through in-memory path overrides; Python's private temporary-directory permissions initially blocked nested writes, so the successful run used ordinary inherited permissions in ignored `player-package/dist/P425-review` (`git check-ignore` confirmed it).
- The slope probe executed the existing helper's `_avgz` method without importing its rendering dependencies; the comparison formula was read from pinned `Map.cs:282`. This proves the helper discrepancy, not a failure of the current flat entrance.
- No new tests were written. C# fixtures were read, not run; no Docker build, shard startup, saved-world probe, real-map rebuild, package build or client walk was performed. Player stranding, pet/ghost travel and the installed world's actual item state remain unverified.
- The progress reporter ran with this pair of work copies and file writes suppressed in memory, because even its dry-run path attempts to refresh `tools/progress.json`. This review leaves only this notes file as a tracked change.
- Ignored test scratch remains in `player-package/dist/P425-review`; the execution policy blocked its cleanup. It contains the small test report and empty directories from the failed permission setup.

P425 DONE
