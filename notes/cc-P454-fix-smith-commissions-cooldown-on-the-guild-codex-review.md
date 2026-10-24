# Codex review: P454

CC task P454: smith commissions: cooldown on the guild book's abandon, Pre-Crafted for large commiss. Reviewed by Codex (`codex exec review`, read-only) after P454 DONE and before the Golem's commit, 2026-10-24 18:55.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.94). The changes close both guild-book abandon bypasses, enforce the shared cooldown for large requests, and credit completed large commissions toward Pre-Crafted. Tests cover book-button cooldowns and large turn-ins inside and outside the achievement window. The task notes record red-first tests and a successful full build; I did not independently rerun them.

No findings.

(0.6 minutes, 233,970 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.72). The only change in this repository is the new P454 notes file; no staged or unstaged tracked changes exist. The notes cover the requested fixes, shared-cooldown decision, red-first tests, build and changelog. No actionable defects were found, but the server implementation and reported test results cannot be verified from this docs-only diff.

No findings.

(0.3 minutes, 112,860 tokens)
