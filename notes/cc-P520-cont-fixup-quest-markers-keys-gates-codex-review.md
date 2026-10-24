# Codex review: P520

CC task P520: fix-up for P363 (CC task P363: quest markers over NPCs, key items, and colored moongat. Reviewed by Codex (`codex exec review`, read-only) after P520 DONE and before the Golem's commit, 2026-10-23 23:35.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.95). The conflict resolutions preserve both sets of content, but the introduced keyed gates allow travel after the required key has been relinquished. Build and test results recorded in the task notes were not independently rerun during this read-only review.

- **medium** [P2] Recheck the key when the gate actually teleports the player (`server\customizations\ShardMoongates.cs:91`)
  For non-hub keyed gates, `MayPass` is checked only before starting the delay. Pinned ModernUO subsequently calls `DelayCallback`, optionally waits for a confirmation response, and reaches `UseGate` without checking the key again. A player can activate the gate, hand the key to another player, and still pass; the same key can therefore admit players who no longer carry it. Enforce the lock at the final teleport boundary and test losing the key between activation and travel.

(1.4 minutes, 735,719 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.85). No actionable defects found in the added notes and art-import helper. The P520 note documents conflict resolutions and test results, but the actual code-repository resolutions are outside this diff and were not independently verified.

No findings.

(0.4 minutes, 96,292 tokens)
