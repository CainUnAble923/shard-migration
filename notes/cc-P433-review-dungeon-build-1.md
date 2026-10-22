# P433: Review of dungeon build 1 (P36)

Reviewed 2026-10-22 against ShatteredLegacy `7508639` and shard-migration `01a6984`. P36's implementation commit is `00d8dc7`; citations below refer to the current work copy unless marked pinned. Pinned means `D:\UO\ModernUO-pinned`, verified at `d4531cd94b739613155225c234900de9f47d2c88`.

Read both work copies' `AGENTS.md`, the direction decision, the task list, and `notes/cc-P36-dungeon-build-1.md`. No P36 Codex review was found beside that note. The already documented F1, F3, F4, cross-facet travel-coordinate limitation, provisional map checks, and package-handoff limitations are not repeated as findings.

## Findings

1. **Bug: Gloomsilk loses its color on the ordinary goza-mat crafting path.** `server/customizations/ClusterFStarterResources.cs:119`: this `Cloth` subclass is consumed by cloth recipes, but pinned `Projects/UOContent/Engines/Craft/DefTailoring.cs:52` accepts only the exact `Cloth` or `UncutCloth` type for goza-mat color retention, and those deeds do not qualify for the generic colored-item fallback in pinned `Projects/UOContent/Engines/Craft/Core/CraftItem.cs:96`, so ordinary crafting, including Craft X, produces an undyed deed from Gloomsilk. Extend that special color check to accept the subclass and add a test that consumes Gloomsilk and checks the resulting mat deed's hue, alongside a normal clothing recipe.

2. **Risk: Dawnstone's recycling skill gate depends on which recycling tool is used.** `server/customizations/SmithGuildSalvageBag.cs:77`: the guild bag requires 45 Mining for Dawnstone, while the ordinary recycle target and stock SalvageBag fall through to difficulty zero in pinned `Projects/UOContent/Engines/Craft/Core/Resmelt.cs:87` and `Projects/UOContent/Items/Containers/SalvageBag.cs:85`, allowing the same Dawnstone equipment to be recycled below 45 through those routes. Apply the intended Dawnstone requirement consistently and test the available routes at 44.9 and 45, or explicitly document why the guild bag alone is stricter.

3. **Risk: the starter crafting test overstates what it proves, especially for granite.** `server/tests/Items/StarterResourcesVerification.cs:383`: `EachCraftsAt45AndNotAt44Point9` calls only `ConsumeRes`, so its Masonry row passes at 45 without exercising pinned `Projects/UOContent/Engines/Craft/DefMasonry.cs:40`, which requires learned Masonry and at least 100 base Carpentry, or the StoneChair recipe's own minimum of 55. Rename this as a material-selection gate test and add actual crafting checks that preserve and explicitly verify the stock Masonry prerequisites rather than treating resource acceptance as a completed craft.

4. **Risk: the new hide and board equivalence pairs have no regression coverage.** `server/patches/CraftItem-shard-hooks.patch:17`: P36 adds Rootwood log/board and Burrowhide leather/hide substitutions, but `server/tests/Items/StarterResourcesVerification.cs:353` and `:355` stock only leather for the leather selection and logs for the log selection, so those rows do not exercise either new pair. Add consumption tests using only Burrowhide hides for a leather recipe and only Rootwood boards for a log recipe, and watch them fail with the corresponding patch entries removed before restoring them.

5. **Risk: the Young combat-cap test does not cover slots becoming available again.** `server/tests/Regions/OldHavenBurrowsRegionVerification.cs:224`: the test covers rejecting a fourth attacker, but never releases a slot through death, a changed combatant, or expired aggression, never exercises a player's summon, and only prints the tamed creature's final `CanBeHarmful` result at `:271`. Add explicit assertions for those transitions and exemptions so later changes cannot leave a Young player incorrectly capped or admit an extra hostile through an excluded creature.

These are shard integration bugs or risks, not requests to change ServUO behavior. The findings come from source paths; none was reproduced in a running shard during this review.

## Requested checks with nothing additional found

- **Spawns stacking without a cap:** nothing found in P36. Its region limits combat admission; P36 does not create spawners, summon timers, or a population controller. The later Rootdeep creatures and seeder belong to P140/P141/P188 and are not represented here as a reviewed spawn system.
- **Chests, loot timers, or repeatable dungeon rewards:** nothing found in P36. It adds material definitions and discovery integration, not dungeon chests or refill timers; the later Vault and creature loot are outside this review. The existing Clean Up Britannia material invariant and the P36 zero-rate entries were inspected, without finding an additional starter-material points loop.
- **Part A granite classes:** nothing additional found in `server/customizations/ClusterFExtendedOres.cs`, the granite entries in `ResourceInfo.cs`, or their mining and Masonry registration. The classes follow pinned `Items/Resources/Masonry/Granite.cs`; `ExtendedOreStoneMiningVerification.cs` checks the stone branch and registrations, and `StarterResourcesVerification.cs` includes their serialization round trips. Finding 3 concerns the crafting claim, not a missing granite class or a recurrence of F1.
- **Teleporters stranding players:** nothing found in P36 because it adds no teleporter. Its region allows recall out and supplies the dungeon entrance used by Young death handling; the physical hole and ladder teleporters were added later in `ClusterFRootdeepSeeder.cs`. Their placement and runtime usability are unverified here.
- **Client-data floor and test-shard mount:** no additional source finding in the P36 changes to `Setup.ps1`, `.env.example`, or `docker-compose.test.yml`. Installed data, server configuration, and the published package are unverified.

## Review scope and validation

Read the P36 changes and current canonical region, harvest, resource, crafting-registration, satchel, discovery, salvage, Clean Up Britannia, and Test Center paths listed in its implementation note, plus their relevant tests. Followed color retention, Masonry eligibility, recycling, and granite behavior into pinned ModernUO. Inspected later seeder declarations only to establish which work was outside P36.

No code or tests were added or changed. No lane tests were requested, and no tests, build, client session, deployment, account operation, or Haven connection was run. Historical green builds in the P36 note are not validation of this review.

Ran `tools/progress.py --dry-run` with both work-copy path overrides; it exited successfully but still rewrote `tools/progress.json`. Restored that generated file byte for byte from HEAD, leaving only this requested note as the deliverable.

P433 DONE
