# cc-P245: fix-up for P199 (port Base items remainder): its branch did not merge into main

Gold Golem, 2026-10-20. Original prompt `cc-P199-port-base-items-remainder.md`; its notes
`notes/cc-P199-port-base-items-remainder.md`.

## Headlines

- **P199 itself was not broken.** P199 merged with today's main passed its first full build (1716 tests: 1712 passed,
  4 skipped). The integrator's single red was an intermittent test. Its log tail did not name which one.
- **Reruns turned up three intermittent tests, none in P199's code.** Two are ones cc-P225 already fixed; those fixes
  are not in main yet, so this branch did not have them. The third is new, in the Wrong revamp from P194/P221.
- **Fixed here, all test-only:** P225's three test fixes brought over unchanged, plus one new fix to the Wrong test.
- **After the fixes: 11 full-suite runs in a row passed** (one full `build.sh -t sl-modernuo:cc-P245`, which built
  the image, plus 10 reruns of the test gate's exact command against `sl-uo-builder:cc-P245`).

## 1. The merge

`golem/Gold/P245` was already at `origin/main` (`356bfc6` in ShatteredLegacy, `490ff31` in shard-migration), and the
hand-off says not to switch branches. So I merged `golem/Gold/P199` into P245 with `--no-commit --no-ff`. The tree
is the same as merging main into P199. MERGE_HEAD is left in both repos for the Golem's commit.

ShatteredLegacy conflicts:

| File | Resolution |
| --- | --- |
| `VERSION` | Main's `2026.10.20.16` (the higher; P199 had `.10`). |
| `CHANGELOG.md` | P199's `2026.10.20.10` lines merged section by section into main's `## 2026.10.20.16`: its three Added lines after Rootdeep's, its three Changed lines after the town crier's, its three Staff lines after Rootdeep's two. P199's own `.10` heading is gone. Main's real `2026.10.20.10` entry (the Golem tab line) and every other entry are unchanged. A script checked that every bullet from both sides is present. |
| `docker/uo/apply-patches.sh` | Both kept: P194's `PlayerMobile-void-pool-context.patch`, then P199's `RemoveTrap-trap-training-kits`, `PuzzleChest-trap-training-kit` and `Enhance-forged-metal-of-artifacts` patches. They touch different files. |

shard-migration conflicts:

| File | Resolution |
| --- | --- |
| `testing/bot-triage.md` | Both tables kept: `### P194`, then `### P199`. |
| `testing/playtest-steps.json` | Both key runs kept: P194-1..7, then P199-1..7. Checked that the JSON parses and all 14 keys are present. |
| `README.md`, `dashboard.html`, `tools/progress.json`, `tools/expansion-coverage.json` | Generated files. I took main's side, then regenerated them from the merged trees with `python tools/expansion_coverage.py`, `python tools/progress.py` and `python tools/render_dashboard.py`. Port list now reads 4 of 16 systems, 602 of 983 files (61%): main's 524 plus P199's ports. |

## 2. The intermittent tests

1. **`PetTrainingVerification.SlotLoweringWorksAtTheTrainer`** (red 1 run in 8 here). This is P225's fix (trainer
   `CantWalk`, diagnostic message), brought over with
   `git checkout golem/Gold/P225 -- <file>`. Neither main nor P199 has touched the file since P225's base, so the
   file is byte-identical to P225's and the two branches will merge cleanly in either order.
2. **`CC6Batch2CreatureVerification.TheRestOfTheBatchKeepsItsServUOShape`** (red 1 in 8). P225's fix (the High
   Plains Boura's ControlSlots reads `SlotsLowered`), brought over the same way.
3. **`LootBoxFanfareVerification`** (not seen red here; red 1 in about 15 in P225). P225's fix (a merged stackable
   counts as handed over), brought over the same way.
4. **New: `WrongRevampedVerification.GenerateBuildsTheDungeonAndDeleteRemovesIt`** (red 1 in 8; expected
   `(5670, 550, 22)`, got `(5721, 550, 20)`). `BedrollSpawner` links each of the first three outside tunnels to a
   bedroll picked with `Utility.Random` over all 80 bedrolls (ServUO's code, `BedrollSpawner.cs:239-245`). About 4%
   of the time per spawner, two tunnels pick the same bedroll, and the later link overwrites that bedroll's way back.
   This is faithful to ServUO and harmless in play: the bedroll still leads out through a tunnel. So the game code
   stays as it is, and the test now expects the way back to name the last of the first three tunnels that leads to
   that bedroll.

Still not fixed (recorded in P225's notes): `WispOrbPossessionVerification` (ForestNymph vs Naba), an AI-driven
30-second fight that sometimes does not start. It did not fail here.

## Files changed beyond the merge

| File | Change |
| --- | --- |
| `server/tests/Services/PetTraining/PetTrainingVerification.cs` | = P225. |
| `server/tests/Mobiles/Normal/CC6Batch2CreatureVerification.cs` | = P225. |
| `server/tests/Misc/LootBoxFanfareVerification.cs` | = P225. |
| `server/tests/Services/Revamped Dungeons/WrongDungeon/WrongRevampedVerification.cs` | The back-link check allows two tunnels to share a bedroll. |

Test-only changes, so there is no CHANGELOG line (the file's own rules keep test detail out). VERSION stays
`2026.10.20.16`.

## Tests

- `docker/uo/build.sh -t sl-modernuo:cc-P245` before the fixes: green (1712 passed). Then 8 reruns: 3 red, as above.
- `docker/uo/build.sh -t sl-modernuo:cc-P245` on the final tree: 1716 tests, 1712 passed, 4 skipped, 0 failed; image
  built. Then 10 reruns: all green.
- The docker-build lock was taken before the first build and released after the last run.

P245 DONE
