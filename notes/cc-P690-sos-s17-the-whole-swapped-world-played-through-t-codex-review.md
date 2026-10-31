# Codex review: P690

CC task P690: The whole swapped world, played through (the 1.0 gate) (SoS swap S17). Reviewed by Codex (`codex exec review`, read-only) after P690 DONE and before the Golem's commit, 2026-10-31 13:03.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.95). The playthrough documents substantial evidence and actionable failures, but its treasure assertion can falsely pass and the required champion observation remains unperformed. These gaps weaken the claimed 1.0 gate.

- **medium** [P2] Observe a champion rather than only its altar (`notes\cc-P690-tools\tour.py:773`)
  The requested playthrough includes a Felucca champion seen, but this check only requires nearby items. The saved log and screenshot establish an altar, not a champion mobile, so this passes even if champion spawning is completely broken. Exercise the spawn until a champion is visible and record that evidence, or explicitly list this requirement as unverified with an owning prompt rather than counting the altar as completion.
- **medium** [P2] Require a newly dug treasure chest before reporting success (`notes\cc-P690-tools\tour.py:754`)
  This check accepts any nearby chest graphic, including an existing ordinary chest, while `dug` only means a target was sent and twelve seconds elapsed. The clean-run log actually reports success for `0xe40` with zero guardians; the separate staff probe identifies the real treasure chest as `0xa308` at a different location. Compare pre/post serials and verify the new chest belongs to this dig, then rerun the check. Otherwise a failed dig can satisfy the 1.0 gate. This also needs the negative confirmation required by [AGENTS.md:339-343](../../AGENTS.md#L339-L343).

(1.4 minutes, 537,494 tokens)
