# cc-P225: fix-up for P190 (the Test Crystal): its branch did not merge into main

Gold Golem, 2026-10-20. Original prompt `cc-P190-cont-test-crystal.md`; its notes `notes/cc-P190-cont-test-crystal.md`.

## Headlines

- **P190 itself was not broken.** The integrator's red was an intermittent test, not the Test Crystal. The exact
  combination the integrator built (main at `058f488` + `golem/Gold/P190`, 1611 tests) passes when rebuilt here, and so
  does P190 merged with today's main (1633 tests).
- **The suite has intermittent tests, and any one of them can fail an integrator build.** Rerunning the full shard
  suite turned up four of them, none in P190's code. Three are fixed here (test-only changes; their causes are below).
  The fourth is recorded, not fixed.
- **After the fixes: 11 full-suite runs in a row passed** (one full `build.sh -t sl-modernuo:cc-P225`, which built the
  image, plus 10 reruns of the test gate's exact command against `sl-uo-builder:cc-P225`).
- The integrator's log tail did not name its failing test (the excerpt cut it off). It was most likely one of these
  four; nothing else failed in about 30 full-suite runs here.

## 1. The merge

The hand-off said not to switch branches, and `golem/Gold/P225` was already at `origin/main` (`77f59fb` in
ShatteredLegacy, `1c29697` in shard-migration). So instead of checking out P190 and merging main into it, I merged
`golem/Gold/P190` into P225 with `--no-commit --no-ff`. The resulting tree is the same. MERGE_HEAD is left in place
in both repos, so the Golem's commit records it as a merge of P190.

Conflicts resolved (ShatteredLegacy):

| File | Resolution |
| --- | --- |
| `VERSION` | Main's `2026.10.20.15` (the higher; P190 had `.7`). |
| `CHANGELOG.md` | P190's two Staff lines (the Test Crystal, `[GiveTestCrystal` and the retired `testCenter.skillGainMultiplier`) moved under main's `## 2026.10.20.15` / `### Staff`, ahead of P235's line. Every other main entry is unchanged. |
| `docker/uo/apply-patches.sh` | Both kept: P192's `BaseBoatDeed-fountain-sanctum.patch` then P190's `SkillCheck-test-crystal.patch`, before `BaseWeapon-trained-weapon-ability.patch`. They touch different files. |

shard-migration merged cleanly (it only adds `notes/cc-P190-cont-test-crystal.md`).

## 2. The intermittent tests

How I found them: I reran `dotnet test ... --filter FullyQualifiedName~ShatteredLegacy.Tests`, the command
`docker/uo/build.sh` runs, in the builder image, several times over.

1. **`PetTrainingVerification.SlotLoweringWorksAtTheTrainer`** (red 1 run in 3; 10 of 10 green when run alone).
   The greeting check walks the player up to the trainer 60 times, advancing 16 s each time: up to sixteen minutes
   of game time. During that time a live vendor's AI can wander it more than 8 tiles from the player, and a trainer
   that far away never greets. The fix is `CantWalk = true` on the trainer, the same way the file already freezes its
   WatchfulBears. That leaves only the coin flip being tested. The assert message now also reports the trainer and
   player locations, line of sight and the message count, so a future red names its cause. 0 reds in the 27 full runs
   after this fix. I never caught the trainer mid-wander, so the wander cause is inferred: it is the only part of the
   test that moves on its own, and freezing it stopped the reds.
2. **`CC6Batch2CreatureVerification.TheRestOfTheBatchKeepsItsServUOShape`** (red 1 run in 6). It asserted that the
   High Plains Boura's ControlSlots is always 2. But HighPlainsBoura is on `SlotLowerableNames`
   (`BaseCreature.PetTraining.cs:166`): when its construction rolls average at or under the threshold, the range
   drops by one and ControlSlots is 1. The assertion now reads the creature's `SlotsLowered` flag and expects 1 or 2
   to match. The Ruddy Boura is not on that list, so its fixed 2 is right.
3. **`LootBoxFanfareVerification.ContentsAreRolledAtEarnAndOpeningHandsOverExactlyThoseThenTheBoxIsGone`** (red 1
   run in about 15). Opening hands items over through the pack's `TryDropItem`
   (`ClusterFGuildPromotion.Deliver`). That merges a stackable item into a same-type stack already in the pack and
   deletes the incoming item. When the roll produced two stacks of the same thing, the test counted the merged one
   as "deleted". Now a deleted stackable passes if a stack of its type is in the pack or bank. Anything else must
   still be undeleted and inside the pack or bank.
4. **Not fixed: `WispOrbPossessionVerification.APossessedCreatureFightingNeverBecomesItsMastersCombatant(ForestNymph,
   Naba)`** (red 1 run in about 14; "the possessed creature never took the foe as its Combatant"). It is a 30-second
   AI-driven fight from 2026-10-03, and a Forest Nymph is a caster that does not always lock onto its foe in that
   window. Fixing it properly means working on the Despise creature AI or the fight's length, which is outside a merge
   fix-up. **Candidate for its own prompt**: lengthen the window, or assert engagement on aggression rather than
   Combatant.

## Files changed (beyond the merge)

| File | Change |
| --- | --- |
| `server/tests/Services/PetTraining/PetTrainingVerification.cs` | Trainer `CantWalk = true`; diagnostic assert message. |
| `server/tests/Mobiles/Normal/CC6Batch2CreatureVerification.cs` | High Plains Boura ControlSlots reads `SlotsLowered`. |
| `server/tests/Misc/LootBoxFanfareVerification.cs` | A merged stackable counts as handed over. |

Test-only changes, so there is no CHANGELOG line: the file's own rules keep test detail out. VERSION stays
`2026.10.20.15`.

## Tests

- `docker/uo/build.sh -t sl-modernuo:cc-P225` on the final tree: 1633 tests, 1629 passed, 4 skipped, 0 failed; image
  built. The docker-build lock was taken for each build and released at the end.
- 10 further full-suite reruns on the final tree: all green.
- Repro of the integrator's combination (scratch worktree, `sl-modernuo:cc-P225-repro`): green. I removed the worktree
  and both repro images afterwards.

P225 DONE
