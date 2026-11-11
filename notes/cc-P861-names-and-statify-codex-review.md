# Codex review: P861

CC task P861: port extra NPC name lists and [VBuild statify. Reviewed by Codex (`codex exec review`, read-only) after P861 DONE and before the Golem's commit, 2026-11-10 15:11.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The requested features, tests, version bump and proof artifacts are present, and the recorded gated build passed. However, the automatic sweep can rename fixed characters, and statify allows a managed fountain to reactivate behind its frozen copy. Tests were not rerun during this read-only review.

- **medium** [P2] Refuse managed fountains that can move themselves back (`server\customizations\StaffBuildTools\AddonStatify.cs:31`)
  A roaming `FountainOfYouthAddon` passes this refusal list and remains registered with `FountainOfYouthSystem` after being parked. That system's hourly `CheckMoveDue` does not exclude internalized fountains, so when its move becomes due it returns the live addon to the world while the frozen statics remain. Include this managed addon in the refusal policy so statify cannot leave both a frozen copy and an active fountain.
- **medium** [P2] Exclude fixed-identity NPCs before deduplicating names (`server\customizations\Names\ShardNames.cs:242`)
  When an older randomly named vendor shares Mara's name, this sweep can rename the fixed New Haven town steward. `ClusterFTownsfolk` explicitly assigns her the identity "Mara", but Mara also appears in pinned's female list, so `ListOf` incorrectly treats her name as randomly generated. Name-list membership cannot establish provenance; exclude fixed-identity NPCs and reserve their names before renaming ordinary townspeople.

(1.8 minutes, 662,280 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.82). No actionable defects found in this repository's notes, proof artifacts, or supporting tools. The artifacts support the reported successful tests and in-game checks; the server implementation and version changes reside in the separate code repository and are not verified by this review.

No findings.

(0.6 minutes, 287,321 tokens)
