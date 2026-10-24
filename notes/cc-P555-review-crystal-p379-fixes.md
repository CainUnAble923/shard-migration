# P555: review of P427, Crystal's P379 fixes

Reviewed 2026-10-24. No code changed.

P427 commit `fb9e9ebde7112db11bd5ceb25d92227031600fab` is an ancestor of local code `main`, reviewed at `1c9c5d8bbf9ab4d9a8dd288aace3afff549479dd`. The work-copy HEAD is that same commit. Notes HEAD was `96b8e4c1bddc0cbdc69f92c698b4b5e5cb9d060d`.

Read both work copies' AGENTS.md, the direction decision and task list, `cc-P427-fixes-from-crystal-p379.md`, and the original `cc-P379-crystal-review-10-21-merges.md`. No separate review of P427 was found beside its notes. Existing achievement issues assigned to P429/P457 are outside this review and are not repeated here.

## Finding

1. **risk: the new deletion-event guard lacks a regression test.** `server/tests/Misc/LevelGearVerification.cs:223` tests a wild creature's death, followed by controlled and summoned deaths, but never deletes a living wild creature with player damage recorded. `server/customizations/LevelGear/ClusterFLevelGear.cs:464` now supplies the only distinction between that ordinary deletion and a death; removing its `Hits <= 0` guard would pay gear XP for a despawn or staff deletion without being exercised by these cases. Add a case that damages a wild creature without killing it, calls `Delete()` while its hits remain positive, and asserts that the attacker's equipped gear gains no XP; demonstrate that it fails with the guard removed. The current guard is correct by inspection; this is a coverage gap, not a confirmed gameplay defect.

## Fixes checked

No remaining defect in the five P379 fixes, and no new runtime defect, was found in the reviewed code.

| P379 item | Review result and evidence |
| --- | --- |
| 1. Pet deaths granting gear XP | Fixed in the normal death path. `LevelGear/ClusterFLevelGear.cs:461` uses `CreatureDeletedEvent`, before pinned `BaseCreature.OnDelete` clears the master. `AwardDeath` at line 478 still excludes controlled creatures, summons, player masters and `NoKillAwards`. The changed test at `LevelGearVerification.cs:238` kills the controlled horse, verifies deletion and unchanged XP, then kills a summon. The wild-orc death case still checks an actual positive award. A bonded pet's death does not delete it, so it cannot reach this award handler. |
| 2. Craft deeds accepting bought weapons | Fixed. `Services/BulkOrders/CraftBOD.cs:218` calls the existing refusal policy before consuming the item. Read the fletching, carpentry and tinker overrides and `BODCombineContained.cs:84`: they reach this same method. `EndCombineLarge` accepts small deeds only. `BulkOrderCraftsVerification.cs:413` checks bought-item refusal, crafted-item acceptance and the disabled-setting behavior for all three crafts. Existing material and exceptional cases now mark their inputs crafted, so those checks remain meaningful. |
| 3. Healing erasing evidence of a creature's hit | Fixed for the reported case. `PlayerMobile-noted-damage-memory.patch:10` records the attacker from `PlayerMobile.OnDamage`; pinned `Mobile.Damage` invokes that hook before changing hits. `ClusterFNotedBySystem.cs:643` consults the new record as well as the damage list. Deletion checks the achievement before removing the record at line 589. `NotedBySystemVerification.cs:210` drives damage, healing to full, and the creature's lethal damage through the real paths, then checks both rejection and cleanup. It also checks an untouched creature still counts and a plain deletion clears its record. |
| 4. Released pets retained indefinitely | Fixed as P379 requested. `ClusterFNotedBySystem.cs:590` removes a deleted creature; lines 694-701 prune expired releases when another release arrives. `NotedBySystemVerification.cs:240` covers deletion and pruning after the window. With no later release, expired living entries can remain until deletion or taming; this is the requested lazy cleanup, not a newly discovered defect. |
| 5. Wrong registry hex value | Fixed. `player-package/vendor/shattered-legacy-art/registry.csv:55` now has `54783,0xD5FF`. The existing fact `EveryRegistryRowsHexIsItsId` at `player-package/tests/Build-UoOverrides.Tests.ps1:1081` checks each parsed row's decimal and hexadecimal values. |

Also read P427's CHANGELOG/VERSION changes and its `docker/uo/apply-patches.sh` registration. The new patch is registered by name in the build gate.

## Verification and limits

- Checked the death and deletion order, damage hook and XP difficulty calculation against read-only pinned ModernUO at `d4531cd94b739613155225c234900de9f47d2c88`, especially `Projects/Server/Mobiles/Mobile.cs:2489`, `:4762`, `:4899`, `:5983`, `:6009`, and `Projects/UOContent/Mobiles/BaseCreature.cs:3540`, `:3662`, `:3674`, `:3688`.
- Ran the existing registry fact alone in Windows PowerShell 5.1 by extracting its AST body and assertion functions. It passed. The surrounding package suite was not run, because its launch facts contact the test shard; this review made no service connections.
- `git apply --check` accepted `PlayerMobile-noted-damage-memory.patch` against the pristine pinned tree without modifying it. This does not verify the entire ordered patch stack.
- No C# build or server tests were run. P427's notes report its red runs and green build; those results were read, not independently reproduced here. Runtime and client behavior remain unverified by this review. No tests were added or changed.
- Ran `tools/progress.py --dry-run` with the work-copy paths. It completed, but still refreshed `tools/progress.json`; restored that generated file to its initially clean state so this task leaves only the requested notes. No Haven connection, deployment, commit, branch switch or code edit was made.

P555 DONE
