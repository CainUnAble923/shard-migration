# Codex review: P869

CC task P869: fix-up for P856 (CC task P856: port a winter set for New Haven before December 1): its. Reviewed by Codex (`codex exec review`, read-only) after P869 DONE and before the Golem's commit, 2026-11-10 13:37.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.85). No actionable defects found in the staged and unstaged changes; there are no untracked files. The relocated layouts and accompanying review artifacts address the requested fixes. Build and gameplay evidence was inspected, but not independently rerun.

No findings.

(0.9 minutes, 531,279 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.92). The P869 placement fixes, renders, screenshots and walk evidence address the five requested review items. However, the included replacement release patch still reverses area-specific staff clears on restart. Main-repository implementation changes were outside this review's scope.

- **medium** [P2] Preserve area-specific staff clears across restarts (`notes\cc-P869-tools\p869-release-isle-20261028.diff:122`)
  During winter, clearing just the release train with `winter clear west` leaves other tracked decorations standing and `LastAutomatic` true. On the next restart, `TopUp()` recreates the deliberately cleared train because it cannot distinguish a staff clear from missing upgrade content. This unresolved P856 regression remains in the replacement release patch. Persist whether the set has already been introduced, or remember explicit clears, so replenishment does not undo staff actions.

(1.3 minutes, 689,594 tokens)
