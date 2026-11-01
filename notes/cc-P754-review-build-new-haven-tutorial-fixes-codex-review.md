# Codex review: P754

CC task P754: build review of P743 (CC task P743: New Haven tutorial fixes (Echo's sparring, extra f. Reviewed by Codex (`codex exec review`, read-only) after P754 DONE and before the Golem's commit, 2026-11-01 00:09.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.95). The note provides the required FAIL verdict and identifies a valid mining-sign problem, but incorrectly passes two other sign placements against the required guide. Its one-item fix-up list is therefore incomplete.

- **medium** [P2] Flag the housing sign's distance from its lesson stop (`notes\cc-P754-review-build-new-haven-tutorial-fixes.md:30`)
  The listed sign at 3713,2591 is four tiles east and three north of stop 1 at 3709,2594, so it exceeds the guide's explicit requirement that a lesson sign be within two tiles of its stop ([guide](notes/guides/building-and-decorating.md#L325-L327)). The render confirms these separate positions. Include this in the fix-up list rather than passing it merely because it clears the cottage door.
- **medium** [P2] Include the stable sign's road obstruction in the fix-up list (`notes\cc-P754-review-build-new-haven-tutorial-fixes.md:28`)
  Both `render-stable-stall.jpg` and `stables-stall-player.jpg` show the signpost at 3610,2613 planted in the dirt road outside the barn. Clearing the doorway approach does not satisfy the separate requirement to keep impassable signposts off roads ([guide](notes/guides/building-and-decorating.md#L325-L332)). Mark this placement as failing and add its relocation to the numbered fixes; otherwise the integrator will merge this obstruction after only the mining sign is corrected.

(1.3 minutes, 347,316 tokens)
