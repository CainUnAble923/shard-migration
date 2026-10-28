# Codex review: P723

CC task P723: fix-up for P721 (CC task P721: make the bandage wait clear to a new player on the isle. Reviewed by Codex (`codex exec review`, read-only) after P723 DONE and before the Golem's commit, 2026-10-28 12:26.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The conflict resolution appears to preserve both branches, and the recorded gated build passed. However, the resulting changes can strand the farm lesson after failed pitchfork delivery and implement the vision's approach with teleports rather than walking. Tests were not independently rerun during this read-only review.

- **medium** [P2] Move the Stranger using walking updates rather than teleports (`server\customizations\Tutorial\TutorialVisionScene.cs:301`)
  During the approach beats, `MoveToWorld` calls pinned ModernUO's `SetLocation(newLocation, true)`, sending teleport updates rather than ordinary walking movement. Setting `Direction.Running` does not change that, so the Stranger jumps between positions instead of visibly walking toward the Gem. Use normal mobile movement for these steps; the coordinate-only test does not detect this difference.
- **medium** [P2] Retry issuing the pitchfork after backpack delivery fails (`server\customizations\Tutorial\TutorialFarm.cs:581`)
  If the backpack is full when Guard is observed, `GivePitchfork` deletes the undelivered weapon, but `GuardKey` is still recorded. Subsequent checks skip this branch, and talking to Wren again does not retry delivery while the player has a pet. Consequently, making room as instructed cannot unblock the required pitchfork lesson. Retry the gift while the weapon step remains incomplete.

(1.6 minutes, 492,200 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.84). No actionable defects found in this repository's notes, helper scripts, and evidence. The P723 build log supports the reported successful test gate; server conflict resolutions are outside this diff and were not independently verified.

No findings.

(0.5 minutes, 238,010 tokens)
