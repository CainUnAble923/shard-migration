# Codex review: P359

CC task P359: chopped trees show a stump when their wood runs out. Reviewed by Codex (`codex exec review`, read-only) after P359 DONE and before the Golem's commit, 2026-10-21 15:57.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The implementation otherwise covers the requested lifecycle, settings, tests, changelog and decision notes, but normal map-static targeting can place stumps at the wrong elevation. The Docker build and shard tests were not run in this review.

- **medium** [P2] Convert static target height back to the tree's base Z (`server\customizations\ClusterFLumberStumps.cs:23`)
  When a player targets a map-static tree with nonzero height, pinned `StaticTarget` adds `TileData.ItemTable[ItemID].CalcHeight` to its location Z, and `GetHarvestDetails` returns that elevated location unchanged. Passing it directly to `Mark` therefore places the stump above the tree's base rather than on the ground. Subtract that height for `StaticTarget` targets while preserving the existing base location for dynamic `Static` items. The tests currently use only dynamic `Static` trees, so they miss the normal map-static targeting path.

(0.8 minutes, 322,421 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.91). The only change in this repository is the requested notes file, which includes the client-option decision, whole-bank marking assessment, and explicit verification limits. No actionable defects were found in that file; server implementation, tests, and CHANGELOG changes are outside this diff and could not be validated.

No findings.

(0.4 minutes, 89,794 tokens)
