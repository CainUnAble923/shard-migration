# Codex review: P757

CC task P757: night watch says 'usage unknown' and never starts work. Reviewed by Codex (`codex exec review`, read-only) after P757 DONE and before the Golem's commit, 2026-11-01 06:15.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.93). The repository changes only add the P757 changelog entry and update VERSION consistently; no actionable defects were found. The Golem implementation, tests, and task notes are outside this diff, so the requested behavioral fixes and green gates could not be verified.

No findings.

(0.4 minutes, 58,357 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The recorded change addresses missing-window fallback and the Run next handoff, but its stale-data fallback bypasses known Fable limits and remains unreachable after a foreign session. Runtime probes were blocked by the sandbox's constrained PowerShell language mode; these findings follow from the recorded patch and surrounding implementation.

- **medium** [P2] Allow the fallback past the foreign-session freshness guard (`notes\cc-P757-tools\p757.diff:135`)
  If a foreign session ran after the stale usage report, `Get-NightBudget` returns `usage unknown` before reaching this new fallback call. Thus, with both reports stale, queued work and a last-known week below pace, the watch can still idle all night instead of starting the requested single batch. Apply the foreign-session guard to ordinary inferred budgets without making the explicitly bounded fallback unreachable, and cover this scenario in the tests.
- **medium** [P2] Preserve known Fable limits during a usage fallback (`notes\cc-P757-tools\p757.diff:150`)
  When both reports are stale but usage.json still contains an unexpired Fable limit marker, the fallback discards `$u.fable` and explicitly omits `FableLimit`. A Fable batch can therefore start despite a known exhausted model-specific week. `Invoke-SelfWake -UsageChecked` skips the normal limit checks, and `Test-NightBatchSpent` cannot enforce a null Fable limit. Preserve unexpired model-specific limits independently of the fallback for the overall week.

(1.1 minutes, 417,040 tokens)
