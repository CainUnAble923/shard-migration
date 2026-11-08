# Codex review: P817

CC task P817: character creation and isle start: humans only, no trade profession, Tutorial Island o. Reviewed by Codex (`codex exec review`, read-only) after P817 DONE and before the Golem's commit, 2026-11-07 17:14.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.8). The changes address the requested creation restrictions, brighter wake, lesson ordering, banker guidance and bank cleanup. No actionable defects were found in the staged, unstaged or untracked changes. Build and visual-proof results were documented in the task notes but were not independently rerun.

No findings.

(1.3 minutes, 670,103 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.9). The release diff substantially implements the requested changes and includes supporting tests and screenshots. However, the profession override introduces a repeat-rebuild regression for supported Prof.txt files that need no filtering.

- **medium** [P2] Cache the no-professions-removed result (`notes\cc-P817-tools\p817-release-isle-20261028.diff:167`)
  When a player's Prof.txt already lacks the removed professions, a normal build returns without writing a stamp, but `-CheckOnly` unconditionally marks that same file stale. Consequently, `Invoke-UoOverrides` starts another full override rebuild on every launch, even when nothing changed. Record and recognize the no-op result so these installations can pass the launcher's freshness check.

(2 minutes, 1,437,275 tokens)
