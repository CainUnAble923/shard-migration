# Codex review: P633

CC task P633: build weapon procs at the levelable gear milestone, stage 1. Reviewed by Codex (`codex exec review`, read-only) after P633 DONE and before the Golem's commit, 2026-10-26 03:22.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The playable slice is implemented, with deferred work and build evidence documented in the sibling notes. However, the test-only boundary is not enforced and the purchased-effect tooltip is disconnected. The reported Docker build was not independently rerun during this read-only review.

- **high** [P1] Enforce the test-shard restriction at runtime (`server\customizations\LevelGear\LevelGearProcs.cs:39`)
  On the live shard, a GM typing `[LevelGearProcs on` directly enables purchases and combat effects. `ShardCommand(TestOnly)` is metadata enforced by the Staff Hub, not by direct command dispatch, and this handler never checks `TestCenter.Enabled`. The `Enabled` property also accepts the configuration switch on any shard. Gate feature enablement on the actual test-shard setting so this incomplete slice cannot run live.
- **medium** [P2] Connect the milestone tooltip to item property generation (`server\customizations\LevelGear\LevelGearProcs.cs:416`)
  After purchasing a proc, the weapon never displays its milestone tooltip: this method has no callers and is never subscribed to `Item.ExtraProperties`. The existing subscription invokes only `ClusterFLevelGear.AddTooltip`, which does not delegate here. Register this handler or call it from the existing handler so the permanent purchased effect is visible on the weapon.

(2.1 minutes, 589,939 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.86). The only change in this repository is the P633 notes file. It records the implementation scope, red/green evidence, gated build result, deferred work, remaining-stage prompt drafts, and required completion marker. No actionable defect was found in this docs-only change; the server implementation and reported build results were not independently verified.

No findings.

(0.5 minutes, 115,973 tokens)
