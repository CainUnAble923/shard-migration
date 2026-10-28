# Codex review: P720

CC task P720: fixes from Chase's walk of Tutorial Island (round 2). Reviewed by Codex (`codex exec review`, read-only) after P720 DONE and before the Golem's commit, 2026-10-28 12:19.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The changes substantially address the requested visual fixes, with recorded build and client-walk evidence. However, replacing the rune breaks the existing bot's vision lesson, violating the explicit route-preservation requirement.

- **medium** [P2] Update the bot's vision target when replacing the rune (`server\customizations\Tutorial\TutorialCorePlacement.cs:314`)
  The existing bot route still searches for `0x1F14` in `shard-migration/notes/cc-P718-tools/isle.py:357-359`. Changing every marker to `SignpostId`, including saved markers, makes that lookup fail: the bot returns without starting the vision and cannot finish the tutorial. Update the bot's selector to find the new lesson sign and verify the route end to end, as the prompt explicitly requires keeping it working.

(2.8 minutes, 1,667,063 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.8). No blocking defects found in this repository's changes. The map tooling and recorded evidence cover the requested fixes, including upgrade checks and a real-character bridge walk in both directions. Server-code and packaged-map changes belong to the separate code repository and were not independently reviewed here.

No findings.

(1.3 minutes, 606,297 tokens)
