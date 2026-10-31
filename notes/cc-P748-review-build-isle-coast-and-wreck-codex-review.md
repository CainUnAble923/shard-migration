# Codex review: P748

CC task P748: build review of P746 (CC task P746: fix-up for P741 (CC task P741: isle coast, shipwre. Reviewed by Codex (`codex exec review`, read-only) after P748 DONE and before the Golem's commit, 2026-10-31 15:06.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The required FAIL verdict and hand-off format are present, and the missing P746 review artifacts are correctly identified. However, the review omits explicit farmhouse chair-facing violations visible in the placed list and source.

- **medium** [P2] Include the farmhouse's incorrect chair facings in the fix list (`notes\cc-P748-review-build-isle-coast-and-wreck.md:81`)
  The farmhouse chairs were missed: P746's `TutorialIsleFarmLayout.cs` and `placed.md` put 0x0B4E at (6702,3974,7) north of the table and 0x0B4F at (6702,3976,7) south of it. These face east and south respectively, rather than toward the table. The applicable [guide](guides/building-and-decorating.md#L216-L219) requires 0x0B4F north and 0x0B50 south. Add this to the numbered fixes so the fix-up does not retain the facing defects this review was tasked to catch.

(0.7 minutes, 262,398 tokens)
