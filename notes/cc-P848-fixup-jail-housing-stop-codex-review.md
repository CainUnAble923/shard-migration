# Codex review: P848

CC task P848: overseer fix-up for P838 (jail lesson): its build review said FAIL. Reviewed by Codex (`codex exec review`, read-only) after P848 DONE and before the Golem's commit, 2026-11-08 11:46.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The release artifact implements the requested housing-stop relocation and includes upgrade tests and proof artifacts. However, the jail code introduced into this repository has a stale-window regression and can duplicate its entrance door on load. Build logs were inspected; tests were not rerun.

- **medium** [P2] Recognize an existing jail door in its open position (`server\customizations\Tutorial\TutorialJail.cs:181`)
  If the world is saved with the jail door open, pinned ModernUO restores it at its offset location and starts a 20-second closing timer. This immediate load-time check searches only the closed tile, misses that door, and creates another one. The original subsequently closes onto the replacement, leaving overlapping doors. Check each nearby door's closed position before creating one, preserving the required idempotent seeding behavior.
- **medium** [P2] Refresh the jail-specific window after each completed step (`server\customizations\Tutorial\TutorialTradeTrials.cs:689`)
  When a player clicks a jail person, returns the pouch, or reads the ledger, `Step` calls `Refresh`, which always sends `TutorialWingTrialGump` rather than updating `TutorialJailGump`. Consequently, the jail window retains its old checklist and next instruction while a second, generic window appears. Route these updates through the jail-specific rendering path so players see the next action without manually reopening the lesson.

(1.3 minutes, 706,924 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.86). The release diff moves the housing stop and sign outside the jail, uses existing load-time cleanup to remove the old sign, and adds regression coverage. The supplied build logs and client evidence support the fix. The final main merge remains explicitly deferred to the integrator; I did not independently rerun builds.

No findings.

(0.7 minutes, 335,783 tokens)
