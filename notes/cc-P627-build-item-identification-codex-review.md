# Codex review: P627

CC task P627: build item identification, stage 1. Reviewed by Codex (`codex exec review`, read-only) after P627 DONE and before the Golem's commit, 2026-10-25 23:30.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The implementation supplies the intended first-stage policy, registry, tests, and remaining-stage drafts, but its test-only restriction is not enforced and its tooltip filtering hides public protection and restriction information. Build success is recorded in the notes; it was not independently rerun during this review.

- **medium** [P2] Preserve public restriction and protection labels (`server\customizations\ClusterFItemKnowledge.cs:228`)
  While either knowledge track is incomplete, the allowlist drops the ordinary blessed/cursed, insured, quest-item, blessed-for, and house-lockdown labels emitted by `Item.AddNameProperties`. For example, insuring a newly concealed loot weapon no longer shows its insurance status until both skills finish identifying it. These are public ownership/death/access facts, not hidden magic stats; retain them independently of discovery, as the design requires.
- **medium** [P2] Enforce the test-shard restriction before enabling the policy (`server\customizations\ClusterFItemKnowledge.cs:617`)
  An administrator can run `[ItemKnowledge on` on the live shard: `ShardCommandAttribute` is descriptive metadata, not a runtime restriction, and this handler never checks the world rules. That enables automatic concealment despite the explicitly test-only scope and the acknowledged unfinished disclosure routes. Guard activation and concealment with the actual test-shard world rules rather than relying on the attribute.

(1.3 minutes, 533,733 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.87). The only change in this repository is the P627 notes file. It records stage-1 scope, red/green tests, the successful build, known limitations, and remaining-stage prompt drafts, ending with P627 DONE. No actionable defect was found in this file; the implementation and build claims cannot be independently verified from this docs-only diff.

No findings.

(0.7 minutes, 214,939 tokens)
