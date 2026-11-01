# Codex review: P755

CC task P755: fix-up for P743 (CC task P743: New Haven tutorial fixes (Echo's sparring, extra farm, . Reviewed by Codex (`codex exec review`, read-only) after P755 DONE and before the Golem's commit, 2026-11-01 03:26.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The placement fixes address the listed review issues, but the included horse lesson can become blocked through normal health regeneration. Build and client behavior were not independently executed during this read-only review.

- **medium** [P2] Keep the horse injured until the trainee bandages it (`server\customizations\Tutorial\NewHavenLessons.cs:589`)
  If the player takes roughly a minute to read the instructions or find bandages, the horse regenerates to full health: `RegenRates.cs` gives ordinary creatures one hit every two seconds. Regeneration does not set `Healed`, and pinned `BandageContext.BeginHeal` rejects an undamaged patient, so the horse remains untamable and the lesson cannot progress without restarting. Prevent natural regeneration from removing the required wound until the trainee has successfully treated it; the current tests call `Heal` directly and miss this scenario.

(1 minutes, 499,171 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The notes describe the requested placement fixes and a successful gated build, but the required live walks and failing-first evidence for the new checks are missing. Server implementation correctness was not independently verified in this docs-repository review.

- **medium** [P2] Demonstrate the new placement checks failing before the fix (`notes\cc-P755-cont-fixup-new-haven-tutorial-fixes.md:103`)
  The evidence records only passing results for the new off-road-sign fact and tightened housing-distance check. P743's existing mutants do not exercise either new placement constraint, so their previous failures cannot establish these checks detect the regressions. Run the new checks against the old placements, record their failures, then restore the fixes and record success, as required by [AGENTS.md:49](../../AGENTS.md#L49).
- **medium** [P2] Complete the required character walk before declaring completion (`notes\cc-P755-cont-fixup-new-haven-tutorial-fixes.md:119`)
  Task step 3 requires walking the changed locations with a real character, but the supplied scene specifications and proof log only teleport the Tester to screenshot positions. This does not verify approaching the relocated signs, entering the barn, or reaching the moved housing stop on foot. Perform and record those walks before marking the task complete; [AGENTS.md:44???46](../../AGENTS.md#L44-L46) prohibits emitting DONE before the required work is finished.

(0.7 minutes, 256,244 tokens)
