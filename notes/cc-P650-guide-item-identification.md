# P650: player guide draft for item identification

Written October 26, 2026, by the Golem's Codex lane. Documentation only. The deliverable is [Item Identification: Appraisal and Arms Lore](wiki-drafts/item-identification.md).

The guide describes merged P627 stage 1, disabled by default. It distinguishes the test behavior from a live release, explains the two shared discovery tracks, targeting, effective-skill thresholds, difficulty and retries, maintenance, training, persistence, and unfinished routes. No code, configuration, saves, or services changed.

## Sources read

Work-copy revisions inspected: ShatteredLegacy `a3f017e279e29eed0ac12c506ef51e6310291583`; shard-migration `24b3ae392c7d37ebee9870ba666c6b672b30da51`. Pinned ModernUO HEAD was verified as `d4531cd94b739613155225c234900de9f47d2c88`.

In shard-migration:

- Both work copies' `AGENTS.md`, plus `docs/direction-decision.md` and `docs/tasks.md` for the working agreements and settled scope.
- `notes/cc-P607-item-identification-design.md`, especially the ownership tables, skill checks, services, persistence, rollout, and deferred work.
- `notes/cc-P627-build-item-identification.md`, including the build evidence and remaining-stage drafts.
- `notes/cc-P627-build-item-identification-codex-review.md` and `notes/cc-P639-review-build-item-identification.md` for previously identified limitations, checked against the current implementation where discussed below.
- `notes/wiki-drafts/tracking-ping.md` for the existing player-draft format.
- `tools/progress.py` for its read-only reporting route and unconditional snapshot write.

In ShatteredLegacy:

- `server/customizations/ClusterFItemKnowledge.cs`: constants and saved rows at lines 29-127; eligibility and creation at 163-199; property owners at 220-356; rendering at 397-480; difficulty and Appraisal at 497-580; Arms Lore at 584-602; staff command from 606 onward.
- `server/patches/Item-property-list-policy.patch`, `LootPack-unidentified-magic.patch`, `ItemIdentification-item-knowledge.patch`, `ArmsLore-item-knowledge.patch`, `ItemIdentification-appraisal.patch`, and `ArmsLore-field-maintenance.patch`.
- `server/tests/Items/ItemKnowledgeVerification.cs`, including the sample sword, thresholds, real skill targets, generated loot, switch behavior, and serialization assertions. These are existing tests read as evidence, not tests run in P650.
- `server/customizations/ClusterFArmsLore.cs`, especially field maintenance at 103-141 and its formulas at 93-97.
- Relevant sections of `server/customizations/ClusterFSkillGain.cs` (Arms Lore and ItemID routes), `ClusterFCreatureLevels.cs` (Appraisal rename, thresholds, creature handler), `Requisitions/RequisitionItems.cs` (property readers), and `Requisitions/Appraiser.cs` (existing quote and purchase UI).
- The `ClusterFItemKnowledge` call sites and registration comment in `docker/uo/apply-patches.sh`.

In pinned ModernUO:

- `Projects/UOContent/Skills/ItemIdentification.cs`: ordinary skill entry, eight-tile target, skill delay, and fallback identification check.
- `Projects/UOContent/Skills/ArmsLore.cs`: two-tile target, ordinary successful-inspection check, and coarse messages before the shard hooks.
- `Projects/UOContent/Misc/LootPack.cs`, the AOS mutation branch.
- `Projects/UOContent/Items/Shields/BaseShield.cs`, its `BaseArmor` inheritance.
- `Projects/UOContent/Items/Wands/IDWand.cs`, its direct legacy flag assignments without a discovery-stage update.

## Differences from design and build prose

1. **Availability and scope.** P607 describes the full proposal. Current code initializes the policy off and recognizes only `BaseWeapon` and `BaseArmor`. Only the patched AOS loot mutation route and deliberate staff concealment create rows. There is no adoption scan or default concealment of all new gear. Existing and crafted goods remain visible through absence of a row. The guide does not promise unknown loot-box contents or quest rewards.
2. **Shields already qualify by inheritance.** P627's stage-2 draft lists shields among later families, but `BaseShield : BaseArmor` and `IsSupported` already include them in stage 1. The guide includes eligible loot shields, without claiming a separate shield client or loot test.
3. **Thresholds, names, and requirements.** P607 proposes advanced hazards and an item card at 90. Code has only names at 30 and values at 60. Named slayers appear as the generic word `slayer`; the safe art name remains until both tracks complete. A Lower Requirements enchantment hides the effective strength requirement, rather than showing the base requirement proposed by P607.
4. **Difficulty uses incomplete readers.** The code rounds and clamps the catalog-derived formula. P639 identifies Use Best Weapon Skill as an enchantment the reader misses. The guide gives the actual formula with its reader limitation, rather than describing every enchantment as correctly counted. The sample sword's D=135, names chance of 18% at skill 59, values chance of 50% at 135, and certainty at 160 follow the implementation and P627 sample. No real loot distribution or new runtime sample was measured.
5. **One roll can make partial progress.** At 60 and above the loop checks names and values against the same roll. Failure at values can still name previously unidentified magic. The guide does not describe an unsuccessful top-stage attempt as necessarily learning nothing. The managed-item pause is per character, not P607's proposed per-account limit.
6. **Arms Lore training remains.** The customization's introductory comment says neither skill gains on a managed item. The patched Arms Lore handler still calls its original `CheckTargetSkill` before both maintenance and discovery, and the existing gain route still accepts gear. The guide follows that control flow: no managed-item Appraisal gain, existing Arms Lore training checks, no extra discovery gain roll. Actual gain frequency was not measured.
7. **Maintenance is still an active side effect.** Successful Arms Lore on owned damaged pack/worn gear calls field maintenance before discovery. Its ten-second maintenance cooldown can refuse maintenance without preventing discovery. The guide includes restoration and maximum-durability loss rather than presenting inspection as read-only.
8. **Services and other outputs remain unfinished.** No paid identification, blind-sale schedule, wand integration, hazard assessment, item card, or per-find gain allowance exists. Existing quote/purchase UI and the wand flag route remain separate. Known non-tooltip disclosure gaps are described as limits, without presenting planned fees as available services.
9. **Completion and lifecycle.** As P639 reports, completing both stages bypasses the catalog and restores the full stock tooltip, including unclassified extra lines. The guide says so. There is no property-revision invalidation. Serialization omits deleted rows from the saved payload but does not prune the live dictionary; P627's claim that rows are dropped at save is too broad. This internal cleanup issue is recorded here rather than expanded into player instructions.
10. **Test-only is intended scope, not a verified enforcement guarantee.** The earlier review notes that the command's test-only attribute is metadata without a runtime activation guard. The guide calls this a disabled test-stage feature and makes no claim that enabling it elsewhere is technically impossible. No staff activation instructions or live configuration change is part of P650.

## Verification and limits

This is a source-based player draft. Live enablement, the deployed revision, real tooltip refreshes, both clients, actual save/restart behavior, complete derived-item coverage, balance across real drops, and runtime skill-gain frequency remain unverified. P627's reported successful build and tests were not rerun. Lane tests are none; no new tests or gates were added.

No Haven connection, deployment, commit, merge, push, or branch switch was made. The generated `server/uo/` tree was not used. Only the requested guide and this note are intended deliverables.

The progress reporter completed with the work-copy path overrides and `--dry-run`. Its unconditional `tools/progress.json` write was intercepted with a process-local `Path.write_text` replacement; the suppressed snapshot target was observed. No progress, README, dashboard, or decision file changed. Existing reporter status prose was not treated as verification of the running shard.

Final content checks found no em dashes or trailing whitespace in either deliverable; both are below 5 MB. Both Git whitespace checks passed, the code work copy is clean, and the docs work copy contains only the requested new Markdown files. Verification commands used Windows PowerShell 5.1. No lane tests were required or run.

P650 DONE
