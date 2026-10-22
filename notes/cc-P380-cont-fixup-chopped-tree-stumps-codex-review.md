# Codex review: P380

CC task P380: fix-up for P359 (chopped tree stumps, by the Codex Golem Valorite): merge main and set. Reviewed by Codex (`codex exec review`, read-only) after P380 DONE and before the Golem's commit, 2026-10-22 03:52.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The conflict resolution preserves main's changes, adds the stump patch once, and retains the higher version. However, the imported implementation has two gameplay defects. The notes report a successful build and test run; those results were not independently rerun in this read-only review.

- **medium** [P2] Accept the shard's carrier-based lumber axes (`server\customizations\ClusterFLumberStumps.cs:120`)
  With an equipped `GargishBattleAxe` (or its descendants), targeting the stump incorrectly reports that the axe must be equipped. That existing weapon derives from `BaseSetWeapon`, not `BaseAxe`, but explicitly implements lumber harvesting, and `HarvestTarget` routes its stump targets to `OnChop`. Recognize these supported lumber axes rather than restricting the equipped-axe check to `BaseAxe`.
- **medium** [P2] Convert map-static target height back to the tree's base Z (`server\customizations\ClusterFLumberStumps.cs:23`)
  When harvesting a normal map-static tree, `StaticTarget` adds the tree's `CalcHeight` to its location Z, and `GetHarvestDetails` returns that elevated location unchanged. Passing it directly to `Mark` places the stump above the tree's base. Subtract that height for `StaticTarget` targets while preserving dynamic `Static` locations. The new tests only use dynamic trees and therefore miss this normal gameplay path.

(1 minutes, 187,220 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.92). The docs-repo changes import P359???s notes and review and add the requested P380 conflict-resolution and validation notes. No actionable defects were found in this diff; the server merge and reported build results cannot be independently verified from these documentation changes.

No findings.

(0.3 minutes, 64,707 tokens)
