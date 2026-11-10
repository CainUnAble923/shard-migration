# Codex review: P870

CC task P870: build review of P867 (CC task P867: fix-up for P855 (CC task P855: port a data-driven . Reviewed by Codex (`codex exec review`, read-only) after P870 DONE and before the Golem's commit, 2026-11-10 15:21.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The note supplies the required verdict and actionable fixes, but explicitly leaves most client shots unreviewed despite the task requiring exhaustive visual inspection.

- **medium** [P2] Inspect every client shot before completing the review (`notes\cc-P870-review-build-decor-addon-housing-furniture.md:18`)
  The note records inspecting all renders but only four TazUO shots, leaving the other designs' client views unchecked. Task step 3 explicitly requires every render and shot, and [the guide](notes/guides/building-and-decorating.md#L229) requires checking every piece from the default camera. Renders cannot substitute for that client-specific check. Inspect the remaining shots and update the findings before marking this review complete; otherwise the fix-up list may omit defects that only appear in the client.

(0.8 minutes, 332,242 tokens)
