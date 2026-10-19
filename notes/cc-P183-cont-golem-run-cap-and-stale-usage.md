# cc-P183: Golem fixes: one phrase after a full run, self-wake when the plan reading is old, the right model, STOPPED cleared

2026-10-19. Opus. Prompt: `D:\UO\cc-prompts\cc-P183-cont-golem-run-cap-and-stale-usage.md` (handed by the Golem).
Not committed: the Golem commits after DONE. Both repos were clean at the start apart from the overnight bot's transcript.

## Headlines

- **Q-067 is fixed.** The start phrase now starts a new run whenever the run counter is full and nothing is running,
  whatever rest it clears. Before, only `run cap`, `night shift ended` and `long run ended` reset the counter. Covered:
  stopping point (P180's case), wrap up, context, model, usage limit, a STOPPED prompt, and a plain idle Golem. A long
  run keeps its own counter.
- **Every wake reads its target again.** That covers the watch, a rest's own wake, the console's Wake, the night shift
  and SelfWake. `Get-WakeTarget` takes the running prompt, or else the next queued one, with its `**Model:**` line at
  that moment. A planned target that changed is logged ("wake target re-read: planned P152 (Opus), the queue now says
  P181 (Fable)"). This morning's 06:45-07:00 sequence, replayed, now wakes Fable for P181.
- **The watch re-plans a model rest when the queue changes.** It compares the fresh target with `waitingFor` and
  `waitingForModel`, and logs "queue changed while resting (model): ..." when they differ. It then updates the pending
  wake, `state.json` and `status.json`, which gains `waitingForPrompt`. The console's Golem tab now says "Waiting for a
  Fable session for P181". The rest email already named the prompt and model, from the same fresh read in `Hand-Off`.
- **A wrong-model session hands over at once** (`-ModelFix`). It skips the 5-minute self-wake spacing but keeps the
  one-per-prompt-per-2-minutes rule. When a wake is refused only by that rule, it stays pending for the watch. The wrong
  session is told to end its turn; the P161 closer closes it when the new session reports.
- **SessionStart checks the model.** If the session runs another model than the Golem asked for (for example a
  fallback), the Golem logs it and wakes the asked model as above. It tries once per prompt and model, then emails you
  instead of looping.
- **A stale plan reading no longer blocks the self-wake.** The plan page reading counts while it is under
  `planUsageMaxAgeHours` (4 h) old. The status line's own numbers (`usage.json`) count under `usageUnknownMinutes`, and
  up to `nightUsageMaxAgeHours` (24 h) while nothing runs, because nothing has used the plan since the last session
  reported. A wake is refused only when neither reading is known, with both named ("usage unknown: the status line last
  reported 30 h ago and the plan reading is 14 h old"). The source used is logged. The paceMode rules are unchanged:
  `Get-PaceCheck` and the `usageLimitPct` bars still apply to whichever numbers are used.
- **A stale plan reading is emailed once a day**, in plain words: what the file is, when it was last written, that the
  Golem carries on from Claude Code's own numbers (but cannot see the Fable week), and the likely cause and fix.
- **Why the plan usage reader stopped** (step 2.1, for the overseer): see "Why the plan usage reader stopped" below. In
  short, the PC shut down at 17:34 on 10-18. After the Claude app restarted at 20:03, its built-in browser was not
  opened again until about 09:51 today, and each run until then had no page to read. It has written again since 10:24
  today.
- **A STOPPED prompt clears in one step.** Every wake (the console's Wake included) and the watch run
  `Resolve-StoppedPrompt` first:
  - If the stopped prompt is back in `queue\`, `stoppedPrompt` and `needsYou` are both cleared and `lastHandled` steps
    back so its DONE is committed.
  - If it stopped for "Chase commits first" (the reason is now kept in `stoppedWhy`) and both repos are committed
    (machine output aside), it is put back in the queue, picked to go next and cleared.
  - Otherwise the refusal says what is still uncommitted.
  - P182's Retry stopped prompt also clears `stoppedWhy`.

## Why the plan usage reader stopped

The reader is not a Windows scheduled task. It is a Claude app scheduled task (`trig_01UtCQyHYGFQ7NNtLrdC4fiH`, every
2 h at :23) that reads claude.ai/settings/usage in the app's built-in browser. The traces, from
`%LOCALAPPDATA%\Claude\Logs\main.log` and `in-app-browser.log`:

- 2026-10-18 16:24: `plan-usage.json` was written (its `readAt`).
- 17:34:26: `Windows session ending (shutdown) - quitting the app`. The 18:23 run never happened.
- 20:03:21: `Starting app`; the scheduled-task services initialize at 20:03:36-38.
- From 20:23 to 08:23 the runs "succeed" in about 5 s (the overseer's passdown) but write nothing.
  `in-app-browser.log` has no browser activity from the restart until 09:51 today.
- 09:51-09:55 today: the in-app browser shows activity (someone opened it). The 10:23 run wrote the file:
  `readAt` 2026-10-19T10:24:07, `error` empty.

So the reader needs the app's built-in browser pane to exist. After an app or PC restart it has nowhere to read until
the pane is opened again, and it still reports success. Two fixes for the overseer: have the task fail loudly (or write
an `error`) when the browser is not reachable, and open the browser pane at app start (or after a reboot). The Golem
side no longer depends on it (above), and its daily email says the same in plain words.

## What changed

D:\UO\golem (outside git; backups `golem.ps1.bak-20261019-P183`, `tests\Golem.Tests.ps1.bak-20261019-P183`):

| File | Change |
|---|---|
| `golem.ps1` | `-CleanRepos` :164 (the repos "Chase commits first" waits on; tests pass temp repos); `Test-SelfWake` :1133: `-ModelFix` skips only the spacing, the two usage readings :1152, the STOPPED refusal names what is still uncommitted; `Get-WakeTarget` :1197; `Test-ReposClean` :1209 (`git status --porcelain --untracked-files=all`, ignoring `testing/play-tests.json`, `testing/SUMMARY.md`, `testing/bot-runs/`); `Resolve-StoppedPrompt` :1228; `Invoke-SelfWake` :1266 (resolves a STOPPED prompt, re-reads the target, logs the usage source, keeps a model fix pending after the 2-minute rule :1307, returns `For`); `status.json` `waitingForPrompt` :1500 and the ready text names the prompt; `Invoke-KeepRest -ModelFix` and the end-your-turn text :1573; `Hand-Off`'s model rest sets `waitingFor` and wakes with `-ModelFix` :1722; SelfWake resolves first :2027 and prints the prompt it woke; the watch: resolve :2175, the stale plan email :2176, the model re-plan :2185, a pending model fix retried as one; SessionStart's model check :2287; the phrase's new run :2354; STOPPED keeps `stoppedWhy` :2547; RetryStopped clears it |
| `tests\Golem.Tests.ps1` | Nine `P183_*` facts (:1491-:1617); three older facts updated on purpose (below) |
| `README.md` | A cc-P183 section |

The live `golem.ps1` was replaced by a copy and a same-volume rename, after the full suite passed on the new copy.

D:\ShatteredLegacy:

| File | Change |
|---|---|
| `scripts\Shard-Console.ps1` | `ConvertFrom-AutopilotStatus` reads `WaitingForPrompt` :4211; the Golem tile and tab say "Waiting for a Fable session for P181" :4642 |
| `scripts\tests\Shard-Console.Tests.ps1` | `P183_TheGolemTabSaysWhichPromptAndModelItWaitsFor` :7492 |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.19.3`, four `### Staff` lines; 2026.10.19.3 (P182's 2026.10.19.2 is committed) |

No server code changed, so no build and no image.

## Tests

Each new fact was run against the old `golem.ps1` (and the old console) first and failed for the reason it pins.
Then it passed on the new one:

| Fact | Red on the old code because |
|---|---|
| `P183_Q067_OnePhraseAfterAStoppingPointRestWithAFullCounterHandsAPrompt` (also wrap up, usage limit, context) | the phrase cleared the rest, `Hand-Off` rested on run cap, nothing handed, runDone 12 |
| `P183_ASelfWakeWithAStalePlanFileUsesTheStatusLine` (06:42 replayed: plan 14 h, usage.json 316 min) | refused: "usage unknown for 316 min (over usageUnknownMinutes 30)" |
| `P183_ASelfWakeRefusesOnlyWhenBothReadingsAreUnknown` | the old refusal did not name both; a fresh plan reading with an old usage.json was refused |
| `P183_AStalePlanReadingIsEmailedOnceADayInPlainWords` | no email |
| `P183_ARenameWhileRestingOnModelWakesTheNewNextPromptsModel` (06:45-06:56 replayed; plus a context rest holding a stale target) | woke `--model opus --name "Golem P152"` |
| `P183_AWrongModelSessionWakesTheRightOneWithoutTheFiveMinuteWait` | refused: one per 5 min |
| `P183_ASessionThatStartsOnTheWrongModelWakesTheAskedOne` | no check at SessionStart |
| `P183_AStoppedPromptBackInTheQueueNoLongerBlocksAWake` (07:44 replayed) | refused: "P181 is STOPPED and waits for Chase" |
| `P183_ChaseCommitsFirstClearsOnceBothReposAreClean` (temp git repos: dirty refuses and says what; clean, with machine output, goes ahead) | `stoppedWhy` not kept, nothing re-checked |
| console `P183_TheGolemTabSaysWhichPromptAndModelItWaitsFor` | the line had no prompt |

Within the rename fact, the first draft asserted the wake's own "re-read" log in the model-rest case. The new watch
re-plans before the wake, so by then the target is already fresh and that line does not appear. The assertion moved to
a second case (a context rest holding a stale target), where the wake's own re-read is what changes the target. Both
parts are red on the old hook.

Full suites:

- **The Golem:** `tests\Golem.Tests.ps1` on the new hook: **480 checks, 0 failed** (see "Golem suite" below).
- **Console facts** `SL_FACT_FILTER='^(P183_|P125_|P131_)'`: 20 of 20 passed. The full console run is not repeated
  here: it dies silently partway at HEAD too (P182's notes), and P183's only console change is the one line above.

## Deviations and decisions for Chase

1. **The status line's reading counts for up to 24 h while nothing runs** (`nightUsageMaxAgeHours`), not only
   `usageUnknownMinutes`. The prompt said to fall back to `usage.json`. At 06:42 that file was itself 316 minutes old
   (the limit was 30 then, 240 now), so a plain fallback would still have refused. Nothing uses the plan while no
   session runs, so the figures still hold: the week only grows, and a passed 5-hour reset counts as 0. Your own
   sessions in these repos report too (the status line).
2. **The prompt's Model line wins over the console's model picker.** A wake for a prompt now uses that prompt's
   `**Model:**` line. If you pick Opus on the console for a Fable prompt, the session opens on Fable, and the log says
   the planned model differed. A prompt with no Model line keeps the picked model.
3. **A wrong-model hand-over can wait up to 2 minutes, plus the watch's 10.** The 2-minute rule stays, as the prompt
   says. A wake it refuses is kept pending, and the watch runs every 10 minutes. In this morning's case the wrong
   session's hand-off is no longer blocked by the 5-minute spacing, and the target is right.
4. **Line endings:** `golem.ps1` and its tests were LF before this prompt (the 10-18 backups too), although the prompt
   says CRLF. They are CRLF now; PowerShell 5.1 reads either.
5. **"Chase commits first" is the only stop reason re-checked automatically** (it matches "commit"). Other stop
   reasons still need the phrase, the console's Retry, or the prompt put back in `queue\`.

## For Chase

Nothing to do on the Golem side. For the plan usage reader: after the Claude app or the PC restarts, open the app's
built-in browser once (claude.ai/settings/usage is enough) so the 2-hourly reader has a page to read. Until then the
Golem carries on from Claude Code's own numbers and emails you once a day that the reading is old.

## Golem suite

The first full run on the new hook: 473 passed, 6 failed, in three older facts. Each failure was a behaviour P183
changes on purpose, so I updated those facts to pin the new behaviour:

- `P125_ADifferentModelRestsKeepsItQueuedAndEmailsOnce`: the rest email now names the prompt, "new session on Fable
  (for P101)".
- `P131_SelfWake_RefusesWhenUsageIsAtTheLimitOrUnknown`: a 40-minute-old status line reading with nothing running is
  now known (Deviation 1). The case is now 25 h old, and both refusals name both readings.
- `P131_TheConsoleWakeIgnoresAutoWakesLimitsButNeedsTheCliSignedIn`: the console picked Opus for a Fable prompt.
  The wake is now Fable, and the override is logged (Deviation 2).

Then `golem.ps1` and `tests\Golem.Tests.ps1` were converted to CRLF, as the prompt asks; they were LF before P183, like
the backups from 10-18. P182's three small scripts were converted too. The full suite ran again on exactly the file
that went live: **480 checks, 0 failed**.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

No file over 5 MB was added. Scratch (the patched copies, the suite outputs) is in the session scratchpad, outside both
repos. The Golem's files are outside git.

P183 DONE
