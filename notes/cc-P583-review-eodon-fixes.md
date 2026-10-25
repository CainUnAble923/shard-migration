# P583: review of the Eodon fix-up (P458)

Reviewed 2026-10-24. Notes only. P458 commit `53c73c256c9a503260793e30c8e1f464bee5d212` is an ancestor of local `main` and the reviewed code HEAD, `608d0b42485390f7963a713a28161d96e7618b63`.

Read `cc-P458-eodon-fixups.md`, the P407 review and its companion Codex review, and the relevant P428/P429 findings and fix instructions. No separate P458 review was present. The findings below do not repeat the earlier spawn-weight, missing-hook, fire-callback, or generation-lifecycle findings.

## Findings

1. **risk**: `server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs:701` and `CHANGELOG.md:49`. The new test requires unchanged skills after a release and successful re-tame, and the Staff line calls that the original behavior. ServUO instead applies its ordinary 10% skill reduction on every subsequent successful tame, including by the same owner (`Scripts/Skills/AnimalTaming.cs:432-435`); only the hatchling's extra 55% cut is first-tame-only. This is inherited ModernUO behavior, and P458 follows P429's explicit test instruction, so it is not a new production regression. Keep the extra cut first-tame-only, but either restore the source's ordinary re-tame loss for hatchlings and correct the test and Staff line, or record the retained ModernUO behavior as a deliberate fidelity deviation and correct the claim that it matches the original.

2. **risk**: `server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs:679`. The new tame test checks each skill's base and individual cap but never checks `SkillsCap`, the separate total training limit set at `Mobiles/DragonTurtleHatchling.cs:74`. Omitting that assignment would leave these assertions satisfied while retaining the larger constructor-time total cap instead of ServUO's post-normal-tame, pre-extra-cut total. Capture the expected fixed-point total after the ordinary 90% reduction and assert `SkillsCap` after the first tame and after re-taming, with the assertion seen failing when the assignment is removed.

## Results for the requested checks

- **Spawn weights:** no remaining mismatch found. `EodonSpawns.cs:151` supplies `MaxCount` as both weight and entry limit. ServUO's `XmlSpawner2.cs:8371-8408` and pinned ModernUO's `BaseSpawner.cs:860-893` both select among entries below their limits with those weights. Pinned `Respawn` also calls that selection path (`BaseSpawner.cs:406-415`). A white tiger's 1/25 is the draw from an empty Wildlife #4 row, not a fixed chance regardless of which entries are already full. Existing worlds needing a generator rerun is already disclosed by P458.
- **First-tame math:** no error found. The ordinary un-paralyzed tame leaves 90% of wild skill, then the hatchling retains 45% of that, approximately 40.5% of wild after fixed-point truncation. ServUO performs the same two steps (`AnimalTaming.cs:429`, `DragonTurtleHatchling.cs:66-67`). The unusual `Math.Max(100, Base - Base * 10)` expression is copied faithfully and resolves to 100 for positive skill values. The explicit first-tame argument correctly distinguishes a first tame from the same owner's re-tame and another owner's later tame; the default overload preserves existing one-argument overrides.
- **Climbing while held:** no remaining bug found in the requested states. `ClimbingVine.cs:42-45` returns before moving a paralyzed, frozen, or casting player. Its new fact exercises each state separately and a free climber. This deliberate ServUO deviation and the outstanding in-game walk-down verification are already disclosed by P458, not new findings here.
- **Tests:** the new facts cover generated entry weights, a real hatchling tame and same-owner re-tame, each blocked vine state, the Infernus combat callback/cooldown/stationary damage, and deletion of the prior generation's creatures. The total-cap gap above is new. Refill-to-cap and collection replacement after a save/reload remain the previously reported P407 gaps, explicitly acknowledged by P458; they are not repeated as new findings.

## Files reviewed

Paths are relative to the code work copy. The Eodon prefix is `server/customizations/Services/Expansions/Time Of Legends/`.

- `CHANGELOG.md` and `VERSION`, including their P458 diff.
- Eodon prefix + `EodonSpawns.cs`.
- Eodon prefix + `Mobiles/DragonTurtleHatchling.cs`.
- Eodon prefix + `Items/ClimbingVine.cs`.
- `server/customizations/Services/Pet Training/BaseCreature.PetTraining.cs`, including the overload and its existing base behavior.
- `server/customizations/Services/Pet Training/PetTrainingHooks.cs`, including the changed dispatcher and its callers.
- `server/customizations/Services/Pet Training/PetTrainingHelper.cs`, including the changed staff test command and ability-profile dispatch.
- `server/patches/AnimalTaming-pet-training.patch`, compared with both source taming pipelines.
- `server/tests/Misc/NotedBySystemVerification.cs`, the changed re-tame call sites and surrounding achievement test.
- `server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs`, including all added facts and the existing related coverage.

Also read the Eodon generator and Infernus implementation, the existing `PetTrainingVerification` hook integration test, and relevant pinned spawner, skill, and firebomb implementations. References: ModernUO `d4531cd94b739613155225c234900de9f47d2c88`; ServUO pub57 `d76bf4443cf76d081ddaf8f57c87ff33749256af`. Source paths and lines in the findings refer to these local read-only reference trees where marked ServUO or pinned.

## Verification and limits

No code or tests changed. No tests were added or run, and no image was built. P458's reported red/green runs were read as historical evidence, not independently rerun. Findings are based on source and assertion inspection; runtime re-tame behavior, actual training to the total cap, and client behavior remain unverified in this review. No Haven connection, deployment, account action, or read of `server/uo/` occurred.

Ran `tools/progress.py --dry-run` against these work copies successfully. It writes `tools/progress.json` even in dry-run mode, so that file's original bytes were preserved and restored. Only this review note is changed.

P583 DONE
