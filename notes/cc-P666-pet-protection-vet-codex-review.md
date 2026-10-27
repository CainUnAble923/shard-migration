# Codex review: P666

CC task P666: Pets on the isle, and every vet brings pets back (P481 F6). Reviewed by Codex (`codex exec review`, read-only) after P666 DONE and before the Golem's commit, 2026-10-27 14:36.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The change largely implements the requested resurrection behavior and dialogue, but corpse recovery incorrectly equips carried inventory. The reported green build was not independently rerun during this read-only review.

- **medium** [P2] Restore carried equipment to the backpack, not onto the pet (`server\customizations\Tutorial\TutorialPetCare.cs:55`)
  When a Young owner's bonded pack animal dies carrying weapons, armor or jewelry, those cargo items retain their `Layer` values. This check therefore equips them onto the animal instead of returning them to its backpack, making cargo inaccessible through the pack and potentially granting equipment bonuses (for example, `BaseArmor.OnAdded` applies skill bonuses). Use the corpse's `EquipItems` list to distinguish previously worn items from carried inventory, and restore the latter to the pack.

(2.4 minutes, 962,221 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.88). This repository contains only new task notes, helper scripts, and test summaries; no actionable defects were found in those changes. The gameplay implementation and claimed build results reside in the separate code repository and cannot be verified from this diff.

No findings.

(0.5 minutes, 110,499 tokens)
