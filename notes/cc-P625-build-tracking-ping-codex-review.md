# Codex review: P625

CC task P625: build the Tracking Ping, stage 1. Reviewed by Codex (`codex exec review`, read-only) after P625 DONE and before the Golem's commit, 2026-10-25 22:37.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The change substantially implements stage 1 and supplies the remaining-stage drafts, but skill-delay sharing and overload refunds have actionable gaps. The notes report a green gated build; I did not independently rerun it.

- **medium** [P2] Refund the pulse when a refresh exceeds the overload ceiling (`server\customizations\ClusterFTrackingPing.cs:792`)
  If a pulse starts below the ceiling but eligible arrivals push a later refresh above it, this path ends the pulse without restoring stamina or clearing its cooldown. The design explicitly requires overload cancellation to refund both, but that behavior currently exists only implicitly for the initial scan before payment. Add an overload-specific refund path and cover crossing the ceiling during an active pulse.
- **medium** [P2] Bind the skill-delay exemption to the originating skill use (`server\customizations\ClusterFTrackingPing.cs:907`)
  A player can leave the Ping offer open, wait for Tracking's delay to expire, use another skill, then press Ping during that skill's delay. The button always calls `Begin(pm, true)`, bypassing `NextSkillTime` regardless of when the menu was issued. This violates the design's shared skill-delay checks. Associate the exemption with the originating Tracking use and reject it when a subsequent skill use has replaced that delay.

(1.4 minutes, 412,662 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.84). No actionable defects found in this repository's task notes and remaining-stage drafts. Server implementation and reported build results reside outside this diff and were not independently verified.

No findings.

(0.6 minutes, 159,779 tokens)
