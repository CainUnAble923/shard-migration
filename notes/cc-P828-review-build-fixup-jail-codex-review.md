# Codex review: P828

CC task P828: build review of P820 (CC task P820: overseer fix-up for P801 (Name Colors jail lesson). Reviewed by Codex (`codex exec review`, read-only) after P828 DONE and before the Golem's commit, 2026-11-08 03:18.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.9). The note supplies the required FAIL verdict and actionable fixes, but its closure instructions miss the same defect at the eastmost cell's junction with the outer wall.

- **medium** [P2] Include the eastmost cell's missing bar-line closure (`notes\cc-P828-review-build-fixup-jail.md:61`)
  The same gap also exists at layout (10,3), where `TutorialJailLayout.cs` places only 0x0035 beside the gate at (9,3). Fixing only (3,3) and (7,3) leaves the eastmost cell front incomplete on both builds. Include main (3712,2637,21) and release (3479,2600,11) in the fix-up instructions, with an appropriate south-edge closure and upgrade handling. The [guide's edge and corner rules](guides/building-and-decorating.md#L71-L73) apply to this junction too.

(1.1 minutes, 559,880 tokens)
