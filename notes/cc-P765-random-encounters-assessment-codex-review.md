# Codex review: P765

CC task P765: assess Random Encounters for Shattered Legacy. Reviewed by Codex (`codex exec review`, read-only) after P765 DONE and before the Golem's commit, 2026-11-01 22:07.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The assessment covers the requested sections, but misstates two source behaviors. In particular, the unsupported loot-deletion claim is repeatedly used to justify the recommendation.

- **medium** [P2] Describe the sqrt picker's actual selection count (`notes\cc-P765-random-encounters-assessment.md:58`)
  The picker is broken, but it does not move every candidate across: its loop increments `i` while removing one entry from `candidateMobiles`, so the shrinking loop bound selects `ceil(N/2)` candidates, not all N. For example, four candidates produce two checks. Correct this behavior description so the assessment accurately represents encounter frequency and load, consistent with [AGENTS.md](../AGENTS.md#L58-L60)'s source-verification requirement.
- **medium** [P2] Correct the claim that cleanup deletes players' loot (`notes\cc-P765-random-encounters-assessment.md:78`)
  For ordinary movable loot, `DeleteTimer.OnTick` walks the item's parent chain and, upon reaching a Mobile, queues `{ xmlDate, null }`, removing only the attachment and preserving the item. The deletion block cited here only deletes objects previously queued for deletion. Consequently, the backpack/bank deletion claim???and its repetitions in the summary, recommendation and intake row???is unsupported and incorrectly strengthens the case against porting. Describe the actual ownership protection and distinguish the separate immovable-item path. This follows the source-verification requirement in [AGENTS.md](../AGENTS.md#L58-L60).

(0.9 minutes, 287,182 tokens)
