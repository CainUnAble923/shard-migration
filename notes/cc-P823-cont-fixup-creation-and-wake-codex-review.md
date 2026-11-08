# Codex review: P823

CC task P823: fix-up for P817 (CC task P817: character creation and isle start: humans only, no trad. Reviewed by Codex (`codex exec review`, read-only) after P823 DONE and before the Golem's commit, 2026-11-07 22:32.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.86). The map changes remove the protruding ceiling tiles, and the replacement screenshots show unobstructed bank views. The accompanying review artifacts and notes address both requested fixes; no actionable regressions were identified. Tests and builds were not independently rerun.

No findings.

(1 minutes, 564,190 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The roof correction and unobstructed replacement screenshots address both numbered review items. However, the supplied replacement release diff still contains a repeat-rebuild regression in profession filtering. Documented build results were inspected but not independently rerun.

- **medium** [P2] Cache the no-op profession-filter result (`notes\cc-P823-tools\p823-release-isle-20261028.diff:167`)
  When a player's Prof.txt already lacks Blacksmith, this branch returns without writing a stamp, but `-CheckOnly` always marks the same file stale. Consequently, `Invoke-UoOverrides` starts another full override rebuild on every launch despite unchanged inputs. The replacement release diff retains this P817 defect; record and recognize the no-op result so these installations can pass the freshness check.

(1 minutes, 450,987 tokens)
