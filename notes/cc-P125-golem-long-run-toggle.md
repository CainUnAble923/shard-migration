# cc-P125: a long-run toggle for the Golem

## Headlines

- The Golem can do a long run: a temporary cap (a number, or "all" for until the queue is empty) and an end time, after which it drops back to `maxPerRun` on its own. Start and end it from the console's Golem tab; the tile shows "long run: N of M, until <time>".
- It now rests, keeping ENABLED, and emails once, when: a usage limit hits (StopFailure `rate_limit`), a prompt stalls (`stallMinutes`), the session's context passes `contextLimitPct` (60%) or has been compacted, the next prompt's `**Model:**` line wants a different model than the session runs, or Chase pressed "Wrap up after this task" / "Find a stopping point". The prompt stays queued in every case.
- "Find a stopping point" reaches CC mid-task at its next tool use; CC writes a continuation prompt (`cc-P<next>-cont-<topic>.md`), ends `P<nn> PAUSED`, the Golem commits it and rests. Continuations jump the queue.
- The overnight bot builds `D:\ShatteredLegacy`'s working tree, so it cannot safely share it with a running prompt. New setting `botWindow` "01:15-03:00": a prompt finishing in that window is committed, then the next one waits until the window ends.
- The Golem tab shows plan usage from Claude Code's documented status line only (current session, this week), a "Fable this week" row marked not reported (no such field exists), a labelled local token estimate when nothing is reported, each queued prompt's title and model with a preview, and the last ten finished prompts with their notes headlines.

## What changed

### `D:\UO\golem\` (outside the repos; backups `golem.ps1.bak-20261015`, `tests\Golem.Tests.ps1.bak-20261015`, `settings.json.bak-20261015-p125`)

- `golem.ps1:89` new events StatusLine, SessionStart, StopFailure, Compact, Nudge, LongRun, EndLongRun, WrapUp, StopPoint; new params `-Cap`, `-Until`, `-Cancel` (and `-Now` for tests).
- `golem.ps1:191` settings `contextLimitPct` (60), `compactionsBeforeFresh` (1), `botWindow` ('' in code, "01:15-03:00" in settings.json).
- `golem.ps1:230` `Sort-Queue`: continuations (`cc-P<n>-cont-*`) first.
- `golem.ps1:241-300` `Get-Session`/`Save-Session` (`sessions\<sid>.json`: model, context %, compactions), `Get-ModelFamily`, `Get-PromptModel`, `Get-LongRun`, `Get-BotWindowEnd`.
- `golem.ps1:402-420` `Invoke-KeepRest` / `Clear-Rest`: resting keeps ENABLED, sets `restReason`, emails once; the start phrase clears it.
- `golem.ps1:~440-520` the hand-off checks, in order: wrap up, long-run/maxPerRun cap (an expired long run is cleared and logged), context (after a DONE only), bot window, model routing (an unknown model hands on with a log note, never blocks).
- `golem.ps1:629-700` LongRun / EndLongRun / WrapUp / StopPoint (each with `-Cancel`).
- `golem.ps1:737-860` StatusLine (prints a one-line status, writes `usage.json` and the session file), SessionStart, Compact, Nudge (tells CC once to find a stopping point, via PostToolUse `decision:block` + reason), StopFailure (`rate_limit` pauses and emails "paused: usage limit, resets at HH:mm").
- `P<nn> PAUSED` is matched beside DONE, committed, then rests. status.json (schema 1) gains `winding`, `stopTold`, `restReason`, `restAfter`, `waitingForModel`, `longRun{cap,until,done,active}`.
- `golem-nudge.cmd` (new): exits in ~30 ms unless `STOP-REQUESTED` exists, so PostToolUse does not start PowerShell on every tool call.
- `Add-GolemHooks.ps1` (new, idempotent, `-DryRun`): adds statusLine, SessionStart, StopFailure, PostCompact and PostToolUse to both repos' `.claude\settings.local.json` (git-ignored); backups in `cutover-backup\`. It has been run.
- Button scripts (new): `Start-LongRun.ps1 -Cap -Until`, `End-LongRun.ps1`, `Wrap-Up.ps1 [-Cancel]`, `Find-StoppingPoint.ps1 [-Cancel]`, each one event.
- `settings.json`: `contextLimitPct` 60, `compactionsBeforeFresh` 1, `botWindow` "01:15-03:00" added (the rest unchanged).

### `D:\ShatteredLegacy`

- `scripts/Shard-Console.ps1:3648-3800` pure helpers: `Get-PromptInfo`, `Get-NotesHeadline`, `Get-FinishedPrompts`, `Format-ResetIn`, `Format-UsageBar`, `Get-UsageBars` (stale after 10 min), `Get-LongRunLine`, `Get-WindingLine` ("Tree clean, safe to package" at rest).
- `scripts/Shard-Console.ps1:1101-1110` actions in a new "Golem run" group: `golem.longrun` (phrase "start long run"), `golem.endlongrun`, `golem.wrapup` ("wrap up golem"), `golem.stoppoint` ("find a stopping point"), `golem.resume` (refused, needs P131; the hook point is commented), `golem.openprompt`, `golem.opennotes`. Tooltips at `:1350`. `Test-PlanSafety` allows only these scripts with these arguments.
- `scripts/Shard-Console.ps1:5379` `Get-GolemExtra` and `:5420` `Get-UsageEstimate` (local token count, cached 5 min, labelled as an estimate); git is read for "tree clean" only at rest.
- `scripts/Shard-Console.ps1:6932` `Update-GolemRunControls`; the tab gains a run row (cap and until boxes, the four run buttons, a disabled "Resume Golem (needs P131)", Open prompt / Open notes) and a split below the panel with the queue list, a read-only preview and the finished list.
- Tile: title and model on the running line, the long-run line, the winding/rest line.
- `scripts/tests/Shard-Console.Tests.ps1`: 10 P125 facts.
- `CHANGELOG.md` 2026.10.15.10 `### Staff`; `VERSION` 2026.10.15.10.

## Documented sources used (no credentials, tokens, undocumented endpoints or claude.ai scraping)

- Status line JSON: https://code.claude.com/docs/en/statusline (`rate_limits.five_hour` / `seven_day`: `used_percentage`, `resets_at`; `model.id`; `context_window.used_percentage`; `session_id`). Rate limits are present for Pro/Max after the first API response.
- Hooks: https://code.claude.com/docs/en/hooks (SessionStart's `model`; StopFailure's `error` = `rate_limit`; PostCompact's `trigger`; PostToolUse `decision:block` + `reason` reaching Claude).
- Settings: https://code.claude.com/docs/en/settings (`statusLine` and `hooks` in `.claude/settings.local.json`).
- The transcript JSONL format is undocumented, so it feeds only the labelled estimate row, never a percentage.

## Tests

- Golem: 22 P125 facts added; before the change 19 failed, and the 3 that passed pin existing behaviour (context below the limit or unknown hands on, same model hands on, no Model line hands on). Full suite now: **152 checks passed, 0 failed** (PS 5.1).
- Console: 10 P125 facts added; before the change 9 failed (the one that passed guards that the console never runs `golem.ps1` directly). Full suite result: see below.
- Fixed while here: Golem fact D92's regex (it failed before P125: the list gained "anything under testing/bot-runs/" on 10-14).
- `Move-ToGolem.Tests.ps1` fails at load because the old "Shard CC Autopilot Watch" scheduled task is gone (removed at the cutover). Pre-existing and not touched.
- Player-package suites: no package file changed in P125, not rerun.

Console full suite under PS 5.1: **327 facts, 327 passed, 0 failed** (the P84 tile fact that failed in a filtered run is the known "Unable to find type [Drawing.Color]" filter artefact; it passes in the full run).

## Play-test items

None: staff tooling only, nothing in game.

## Deviations and decisions for Chase

- **No Fable weekly bar.** Claude Code's status line reports the 5-hour and 7-day windows only; there is no per-model weekly field anywhere documented. The row says "not reported" rather than guessing.
- **Desktop app and the status line: unverified.** The docs describe the status line for the terminal CLI and do not mention the desktop app. When I checked, no `sessions\` or `usage.json` had appeared from this desktop session, so in the desktop app the usage bars may stay "unknown" (the estimate row then shows), and the context check and model routing fall back to SessionStart's model and PostCompact counts. If that holds, the context-% check only works from a CLI session (P131's console wake is CLI).
- **Your context ask** ("take into account the context limit when knowing when to stop and start a new session"): folded in. After a DONE, if the session's context is ≥ `contextLimitPct` (60) or it has been compacted `compactionsBeforeFresh` (1) times, the Golem commits, rests and emails "P<n> done, context NN% full: start a new CC session" instead of handing the next prompt into a crowded session. Set either to 0 to turn it off.
- **Stopping point mid-task** is delivered by a PostToolUse hook (`golem-nudge.cmd`), since hooks cannot interrupt a turn otherwise. It costs ~30 ms per tool call while nothing is requested.
- **Resting keeps ENABLED**, as asked; "Golem, stop" still removes it as before. Resuming is the usual phrase until P131 adds the console button.
- **Bot and Docker:** the overnight bot (`Run-OvernightPlaytests.ps1`, 01:30) builds the working tree by default, so a prompt mid-edit could give it a half-done build. `botWindow` "01:15-03:00" keeps new prompts out of that window; a prompt already running at 01:15 is not interrupted (it finishes, is committed, then the Golem waits). Widen or clear the window in `settings.json`.
- **Config changed outside the repos:** both repos' `.claude\settings.local.json` (hooks and statusLine, git-ignored; backups in `D:\UO\golem\cutover-backup\`) and `D:\UO\golem\settings.json`.

## For Chase

- **Long run:** Golem tab, set "Long run: cap" (a number, or `all`) and "until" (defaults to next Monday 06:00), press Start long run, type `start long run`. The tile shows "long run: N of M, until Mon 06:00". It ends by itself at the cap or the time (back to `maxPerRun` 12), or press End long run.
- **Wrap up after this task:** the running prompt finishes normally, is committed and pushed, then the Golem rests and emails "P<n> done, resting (wrap up)". Press again to cancel.
- **Find a stopping point:** CC is told at its next tool use to finish its step, leave both repos green, write a continuation prompt and end PAUSED. The Golem commits, rests and emails "P<n> paused at a stopping point, P<cont> queued". The continuation runs first next time.
- **At rest** the tile reads e.g. "Resting after P125 (wrap up). Tree clean, safe to package". To go again, say "Golem, please work on the shard tasks" in a CC session (on the model the email names, if it was a model rest).
- **Emails** come once per rest: wrap up, stopping point, context full or compacted, model wanted, usage limit (with the reset time), and no progress for 45 min.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: `CHANGELOG.md`, `VERSION`, `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`. docs: this note and the importer's `testing/SUMMARY.md` and `testing/play-tests.json`. The `D:\UO\golem\` changes are outside both repos.

P125 DONE
