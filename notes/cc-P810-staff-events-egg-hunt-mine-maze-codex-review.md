# Codex review: P810

CC task P810: staff events: egg hunt and landmine maze. Reviewed by Codex (`codex exec review`, read-only) after P810 DONE and before the Golem's commit, 2026-11-07 11:52.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The implementation covers both events and includes tests and documented proof, but the maze permits prize-winning without a living traversal and can reset or resurrect players below its floor. Build and client verification were not independently rerun during this read-only review.

- **high** [P1] Require a living traversal before awarding a maze prize (`server\customizations\StaffHub\StaffMineMaze.cs:171`)
  A player can enter the start row already dead, walk through every mine unharmed, resurrect near the finish using Sacrifice or another player's Resurrection spell, then step onto the finish row to win. Ghost entry is allowed, no revival timer is scheduled for an already-dead entrant, and winning checks no traversal history. Track a valid living attempt and invalidate it on death so bypassing the minefield cannot earn a prize.
- **medium** [P2] Resolve the start spot onto the maze's walkable floor (`server\customizations\StaffHub\StaffMineMaze.cs:75`)
  When staff place a maze on a static floor, bridge, or elevated platform, `GetAverageZ` returns the underlying land elevation rather than the walking surface. Both resurrection and reset consequently teleport players beneath the maze, potentially into impassable terrain. The saved corner Z is never used for an active map. Resolve a valid standing position on the intended floor before moving players there.

(3.5 minutes, 1,290,060 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.82). No blocking defects found in this repository???s new notes, proof artifacts, and supporting tools. The recorded gated build and client walkthrough support the completion report; the server implementation and version/changelog changes are outside this diff and remain unverified by this review.

No findings.

(0.7 minutes, 239,043 tokens)
