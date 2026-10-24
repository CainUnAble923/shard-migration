# Codex review: P412

CC task P412: chopped trees: stump on the ground, and our TazUO hides the exhausted tree until it re. Reviewed by Codex (`codex exec review`, read-only) after P412 DONE and before the Golem's commit, 2026-10-24 06:24.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The implementation largely covers the requested server/client lifecycle and tool handling, but existing map trees with foliage below their trunk elevation will not disappear completely. Build results were documented by the implementer; this review did not rerun the builds or visually verify TazUO.

- **medium** [P2] Include tree foliage whose static Z is below the trunk (`server\customizations\ClusterFLumberStumps.cs:135`)
  Some existing map trees have foliage slightly below their trunk's base Z. For example, the shard's client data at Trammel (525, 816) contains walnut trunk 0x0CE0 at Z 1 and walnut leaves 0x0CE1 at Z 0. Exhausting that trunk excludes its leaves here, so TazUO hides the trunk but leaves the canopy floating above the stump. Resolve the tree's associated foliage without requiring its Z to be at least the trunk's, and add coverage with differing trunk and foliage elevations.

(2 minutes, 664,976 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.78). No actionable defects found in the new notes, proof scripts, or recorded results. This repository contains no server or client implementation changes, so this verdict covers the documentation and proof artifacts only; it does not independently establish that the implementation satisfies P412.

No findings.

(0.5 minutes, 128,726 tokens)
