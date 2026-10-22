# Codex review: P405

CC task P405: servuo.dev code batch 10-22, research (notes only). Reviewed by Codex (`codex exec review`, read-only) after P405 DONE and before the Golem's commit, 2026-10-22 08:55.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The notes cover the requested folders and deliverables without changing code. However, the recommended archery-butte port overlooks nonvirtual engine methods, leaving its implementation approach and port cost materially incomplete.

- **medium** [P2] Account for the butte's missing extension hooks in the port cost (`notes\cc-P405-servuo-batch-1022.md:988`)
  The proposed small subclass cannot reuse pinned's firing logic while changing the facing and hit artwork: `ArcheryButteAddon.cs:34-38`, `:63` and `:93` define nonvirtual `FacingEast`, `Gather` and `Fire`, and the hit area is local to `Fire`. Storing another facing property in a subclass will not change the inherited firing checks. The assessment should explicitly budget either stock-file hooks or a replacement firing implementation, rather than presenting this as roughly 60 ID-swap lines with no stock edits. This follows the pinned-source dependency verification requirement in [AGENTS.md:143-147](../AGENTS.md#L143-L147).

(2 minutes, 908,398 tokens)
