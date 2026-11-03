# Codex review: P786

CC task P786: Halloween witch field boss. Reviewed by Codex (`codex exec review`, read-only) after P786 DONE and before the Golem's commit, 2026-11-03 07:37.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The core boss, rewards, encounter integration and tests are present, but configuration handling has actionable defects and the configuration requirement is incomplete. Build/test execution and the required P786 notes could not be verified in this review.

- **medium** [P2] Move the remaining gameplay numbers into configuration (`server\customizations\HalloweenWitch\HalloweenWitch.cs:60`)
  The task requires all numbers in a config file, but the witch's physical/cold/poison damage distribution remains hard-coded here. The Ouija board's interaction range and five-second cooldown are also fixed literals. Expose these gameplay tuning values in HalloweenWitchTable and consume them here rather than requiring a code rebuild to adjust them.
- **medium** [P2] Reconcile existing witches when configured spots change (`server\customizations\HalloweenWitch\HalloweenWitchSpawns.cs:102`)
  After staff removes or relocates a spot in the configuration and reloads it, Sync retains witches solely by their old numeric index. Removed spots therefore keep their witches, and relocated spots remain empty while the old witch lives elsewhere; these stale placements also survive restarts through the saved serial set. Reconcile tracked witches against the current spot definitions before filling vacancies.
- **medium** [P2] Reject null collections before accepting the configuration (`server\customizations\HalloweenWitch\HalloweenWitchTable.cs:349`)
  A configuration containing `"spots": null` passes validation because this loop substitutes an empty collection. `Reload` then installs that table and throws on `table.Spots.Count`; during startup this aborts Configure, and during a staff reload it leaves an unusable table active. Reject null collections and null rows before replacing Current so malformed configuration preserves the previous working table.

(3.2 minutes, 759,416 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The verification helper masks failures and can execute stale tests. This repository contains only notes and supporting tools; the boss implementation, serialization, CHANGELOG and version changes are outside this diff and could not be verified here.

- **medium** [P2] Propagate build and test failures from the probe (`notes\cc-P786-tools\probe.sh:20`)
  If compilation or a test fails, these pipelines can still return success because their exit status comes from `head` or `grep`, and semicolons run the tests even after a failed build. `red-probe.txt` demonstrates the resulting stale-assembly run: compilation fails, then the old assembly reports no matching tests. Make compilation failures stop execution and preserve test failure exit codes so this helper cannot falsely report successful verification.

(0.8 minutes, 143,832 tokens)
