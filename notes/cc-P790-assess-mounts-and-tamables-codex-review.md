# Codex review: P790

CC task P790: assess mounts and tamable creatures. Reviewed by Codex (`codex exec review`, read-only) after P790 DONE and before the Golem's commit, 2026-11-03 11:08.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The assessment covers all twelve downloads and supplies ranked recommendations, but two balance claims contradict the pinned implementation. The ethereal-slot error directly affects the rationale for the second-ranked rebuild.

- **medium** [P2] Compare beetle smelting against ore-size-dependent yields (`notes\cc-P790-assess-mounts-and-tamables.md:55`)
  Two ingots per ore does not universally double metal supply: pinned `Items/Resources/Blacksmithing/Ore.cs:215???230` already yields two for large ore, one for medium ore, and half an ingot per small ore. This download instead applies two universally and bypasses the skill check, so the actual yield exploit affects smaller piles (2?? medium and 4?? small), not ordinary large ore. Correct the economy assessment and repeated skip rationale so subsequent intake decisions use the real difference. See [AGENTS.md:58???60](../AGENTS.md#L58-L60) on checking claims against source.
- **medium** [P2] Correct the zero-slot premise for ethereal mounts (`notes\cc-P790-assess-mounts-and-tamables.md:72`)
  Pinned `Mobiles/Animals/Mounts/Ethereals.cs:69` defines `FollowerSlots => 1`; mounting adds that slot to the rider, and `Validate` rejects mounting above the follower cap (lines 162???166, 201???204). Simply subclassing it therefore does not provide the advertised zero-slot player mounts. Correct this claim here and in row 6, and distinguish any proposed companion-specific behavior from existing behavior before ranking the rebuild on slot savings. This also follows [AGENTS.md:58???60](../AGENTS.md#L58-L60), which requires verifying coverage against source rather than documentation.

(1.7 minutes, 568,000 tokens)
