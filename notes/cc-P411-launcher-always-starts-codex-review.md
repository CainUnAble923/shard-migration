# Codex review: P411

CC task P411: the launcher must always start the game (overrides rebuild: find the hang, time it, ti. Reviewed by Codex (`codex exec review`, read-only) after P411 DONE and before the Golem's commit, 2026-10-24 05:42.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The default test-shard routing and staged rebuild mechanism address much of the prompt, but blocking freshness checks, duplicate timeout waits, unsafe swap recovery and incomplete hang diagnostics remain. Tests and package gates were not executed during this read-only review.

- **high** [P1] Include freshness checks in the bounded child process (`player-package\payload\app\Overrides-Launch.ps1:114`)
  On a managed or cloud-backed PC, this synchronous `-CheckOnly` call can still block Play indefinitely before the timer, progress bar or trace starts. It does more than compare small stamps: `Build-EquipAnim` hashes the animation files and `Build-MapOverride` parses the entire map patch. Slow hydration or endpoint scanning during those reads therefore bypasses the requested 60-second safeguard. Run this work under the same bounded child-process mechanism.
- **medium** [P2] Record the active step before executing potentially blocking work (`player-package\payload\app\Build-UoOverrides.ps1:183`)
  If a step hangs indefinitely???for example, `cliloc.compile` blocks in `Add-Type`???the trace never names that step: `Start-Step` logs only the preceding completed step through `Stop-Step`. The active name exists only in the transient progress file, so sending Chase the requested `app\logs` files cannot identify where the work PC stalled. Write a step-start record before entering the work, while retaining the completion timing record.
- **medium** [P2] Recover the previous set before deleting the swap backup (`player-package\payload\app\Overrides-Launch.ps1:61`)
  If the process stops between the two directory renames, or both promotion and rollback fail because of a file lock, `uo-overrides.old` can be the only remaining last-good set. The next invocation unconditionally deletes it here before checking whether `uo-overrides` exists or whether staging can be promoted. A subsequent failed promotion then starts without overrides and permanently loses the fallback. Restore or retain `.old` whenever the live directory is absent, and delete it only after successful promotion.
- **medium** [P2] Avoid waiting a second time after the updater times out (`player-package\payload\app\Update.ps1:339`)
  When an update's rebuild exceeds 60 seconds, this call announces that the game will start and returns, but Update then launches Play normally. Play discovers the same running builder and waits another full 60 seconds in `Invoke-UoOverrides`. A hung rebuild therefore delays the game for approximately two minutes instead of the configured minute. Carry the timeout result into the immediate Play handoff so it uses the previous overrides without waiting again.

(1.5 minutes, 313,151 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.88). The only change in this repository is the P411 notes file, which covers the requested timings, work-PC diagnostics, stopgap retirement, limitations, and reported tests. No actionable defects were found in that file; the launcher implementation and reported test results are outside this diff and were not independently verified.

No findings.

(0.4 minutes, 98,589 tokens)
