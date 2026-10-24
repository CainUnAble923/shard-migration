# P545: Rootdeep anthill entrance review

Reviewed 2026-10-24. Notes only. P413 commit `902c651` is an ancestor of local `main`; the code work copy and local `main` are both at `82ba93fdd3e047646cdf63cb4f468b9a30b90270`.

Read P413's implementation note and Codex review, its listed server and map changes, W1 and W6 in `server/tests/Regions/RootdeepWayInVerification.cs`, V5 in `server/tests/Regions/RootdeepVaultVerification.cs`, the map tests, and P413's builder, private-shard harness, placement CSVs and saved walking reports. Also checked the related P425, P430 and P504 reviews to avoid repeating their findings. Paths below are relative to the code work copy unless prefixed with `shard-migration/` or `ModernUO-pinned/`.

## Findings

No new actionable bug, risk or nit found beyond the prior reviews. No additional opening tile without a down trigger, mound trap, pet or mount separation defect, or blocked ladder landing was identified by this review. This is a source review with limited checks, not a fresh runtime proof.

## Evidence

- The inclusive mouth bounds at `server/customizations/ClusterFRootdeepSeeder.cs:81` produce a down row for every coordinate at x 3617-3619, y 2617-2620 (`:100`). W1 independently lists those coordinates at `server/tests/Regions/RootdeepWayInVerification.cs:156`, checks every row and exercises its stock teleporter. The shipped map matches `shard-migration/notes/cc-P413-tools/statics-placed.csv`, including the sinkhole's dark core; map test 6 passed on this work copy. The old hole addition is absent.
- The ladder returns to `(3619,2623,0)` at `server/customizations/ClusterFRootdeepSeeder.cs:92`, outside the mouth and the mound footprint. The south-wall opening remains in the shipped patch. P413's saved `walk-result.json` records successful descent from each mouth coordinate and return to that landing each time. Its two interior mouth tiles required staff placement beside them before stepping across, as the original note explains. I inspected these records and the harness; I did not repeat that walk.
- The saved-world upgrade at `server/customizations/ClusterFRootdeepSeeder.cs:278` changes the known ladder's destination in place. W6 at `server/tests/Regions/RootdeepWayInVerification.cs:411` covers the old two-item entrance, dry run, upgrade without duplication, and a second unchanged run. No additional clean-world upgrade defect was found.
- `Creatures == false` prevents independent creature entry, but does not disable pet transport: `ModernUO-pinned/Projects/UOContent/Items/Misc/Teleporter.cs:236` calls `BaseCreature.TeleportPets`. At `ModernUO-pinned/Projects/UOContent/Mobiles/BaseCreature.cs:4092`, nearby controlled pets on Follow, Come or Guard orders move with their owner; pets outside three tiles or on other orders are outside that stock behavior. A ridden mount is internalized with its mount item equipped on the rider (`ModernUO-pinned/Projects/UOContent/Mobiles/Animals/Mounts/BaseMount.cs:77`), and these ordinary teleporters do not dismount the rider. No entrance-specific pet or mount loss was found by inspection. Live pet and mounted travel remain unverified.
- The existing W1/W6, V5 and map-test coverage was inspected for missing cases. Remaining movement, pet/ghost, damaged-item, map-availability and Young-warning coverage concerns already belong to the earlier reviews; this note adds no duplicate finding.

## Checks and limits

- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File player-package/tests/Map-Overrides.Tests.ps1`: all seven existing facts passed under Windows PowerShell 5.1.
- With `SL_SHARD_REPO` set to this code work copy, `python -B -m unittest tools.tests.test_mapops.Shipped.test_4_the_shipped_patch_is_the_burrows_and_the_way_in_only tools.tests.test_mapops.Shipped.test_6_the_burrow_replaced_the_hole`: both existing tests passed. The real-map scratch comparison was not run.
- Pinned ModernUO is clean at `d4531cd94b739613155225c234900de9f47d2c88`. C# fixtures were read, not executed. No new tests were added, so there is no new red/green claim. No Docker build, shard startup, client visual check, package build, real-map rebuild or save/reload probe was performed.
- The progress reporter completed against these work copies with its `progress.json` write suppressed in memory. No progress artifacts were changed. No code changes, commits, deployments or connections to Haven were made.

P545 DONE
