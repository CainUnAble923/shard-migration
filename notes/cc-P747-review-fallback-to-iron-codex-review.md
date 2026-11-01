# Codex review: P747

CC task P747: build reviews fall back to Iron after 2 hours. Reviewed by Codex (`codex exec review`, read-only) after P747 DONE and before the Golem's commit, 2026-11-01 00:04.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.95). The only changes are the CHANGELOG entry and VERSION bump; there are no untracked files or actionable defects in this diff. The Golem implementation and tests are outside this repository, so the fallback, fresh-session behavior, timeout gate, answered-prompt priority, and test results remain unverified.

No findings.

(0.3 minutes, 58,432 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The main fallback and timeout changes are implemented, but transient refusals can disable fallback permanently. Answer-priority and fresh-session enforcement also miss existing execution paths.

- **medium** [P2] Enforce review freshness on idle hand-offs too (`notes\cc-P747-tools\p747.diff:239`)
  This guard is inside `if ($finished)`, but both the start-phrase handler and idle Stop handler call Hand-Off without that argument. If Iron finishes the build while no review is available, its existing session can later claim the fallback review through either path, bypassing this guard and reviewing its own work in the same session. Check the receiving session's history rather than assuming every hand-off without `$finished` is fresh.
- **medium** [P2] Protect answers received before the prompt stops (`notes\cc-P747-tools\p747.diff:311`)
  If Chase answers before the session emits STOPPED, the existing Stop handler detects Get-PendingAnswers and calls `Invoke-RetryStoppedCore "P$n"` without `-Answered`. That path consequently creates no answered hold, so a subsequent fallback or Run next can still displace the resumed prompt???the same ordering defect this task requires fixing. Pass `-Answered` from that automatic retry path too and test this event ordering.
- **medium** [P2] Retry transient assignment refusals (`notes\cc-P747-tools\p747.diff:97`)
  When Assign-Prompt encounters a rejected git push or a busy claim token, it exits 2 even though the refusal is temporary. Returning a nonempty `refused:` value causes Invoke-BuildReviewGate to persist `fallback` and never attempt assignment again. An unrelated queue update can therefore permanently prevent the required Iron fallback. Retry transient refusals instead of marking fallback complete.

(0.9 minutes, 451,302 tokens)
