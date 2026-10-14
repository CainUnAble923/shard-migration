# cc-P99: autopilot becomes the Golem, and D90, D91, D92 are fixed

2026-10-14. Tooling. Prompt: `D:\UO\cc-prompts\cc-P99-golem.md`.

## Headlines

- **`D:\UO\golem\` exists beside cc-autopilot** and does the same job under Golem names, plus three fixes:
  `golem.ps1` (the hook), `Start-Golem.ps1`, `Stop-Golem.ps1`, `Watch-Hidden.vbs`, `Setup-Email.ps1`,
  `Send-TestEmail.ps1`, `Move-ToGolem.ps1`, `README.md`, `tests\`. Emails start `[Golem]`. **It is not live yet:**
  the CC hooks and the scheduled task still point at cc-autopilot until Chase runs the cutover (For Chase, below).
- **The start phrase.** A `UserPromptSubmit` hook (`golem.ps1 -Event Prompt`): "Golem, please work on the shard tasks"
  or "Golem, work" (case, punctuation and spacing ignored) wakes the Golem and hands CC the lowest queued prompt as
  added context. "Golem, stop" rests it after the running prompt is committed. Any other message does nothing.
- **D90, D91 and D92 are fixed in both the Golem and cc-autopilot** (cc-autopilot minimally, so this run benefits).
  Each fix was watched failing against the pre-fix backup (`cc-autopilot.ps1.bak-20261014-golem`) and passing after.
  **These are verified against fixtures, not in a live run of the queue:** a real STOPPED-then-retried prompt and a
  real background-agent stop have not happened since.
- **The Shard Console says Golem**: GOLEM tile, Golem tab, Wake the Golem, Rest the Golem, Golem email setup, Golem log,
  Golem settings, Open Golem folder, Move to the Golem, window titles `GOLEM - ... - Shard Console`. `autopilot.*`
  keys still resolve as aliases. It reads `D:\UO\golem` once it is active (the cutover writes `ACTIVE`), else
  cc-autopilot, and says which on the tab.
- **`Move-ToGolem.ps1`** (`-DryRun`, `-Rollback`) does the cutover; tested forward and back against fixture folders and
  throwaway scheduled tasks. A dry run against the real setup, now, refuses because P99 is running (as it should).
- Console facts **252 of 252** pass (full run, below); Golem hook facts 77 of 77; cutover 39 of 39; cc-autopilot's
  three fixes 14 of 14; dashboard 15 of 15.
- No task-list tool was available in this CC session (no TodoWrite or TaskCreate), so Chase's remote step view shows
  no steps for P99. The steps are listed under "Steps" here instead.

## Steps (in place of the task list)

1. Read everything the prompt named. Done.
2. Part A, `D:\UO\golem\`. Done.
3. Part C, D90-D92 in the Golem and in cc-autopilot. Done.
4. Part D, `Move-ToGolem.ps1`. Done.
5. Part B, the Shard Console. Done.
6. Part E, words. Done.
7. Tests, patch notes, notes, preflight. Done.

## What I read, and where the hooks are

- `D:\UO\cc-autopilot\README.md`, `cc-autopilot.ps1` (all 508 lines), `Start-Autopilot.ps1`, `Stop-Autopilot.ps1`,
  `Watch-Hidden.vbs`, `settings.json`, `Setup-Email.ps1`, `Send-TestEmail.ps1`.
- Scheduled task `Shard CC Autopilot Watch`: Ready, `wscript.exe //B //Nologo "D:\UO\cc-autopilot\Watch-Hidden.vbs"`,
  time trigger repeating PT10M, InteractiveToken, IgnoreNew, 5 min limit (from `Export-ScheduledTask`).
- **The hooks are in `.claude\settings.local.json` in both repos** (`D:\UO\shard-migration\.claude\settings.local.json`
  and `D:\ShatteredLegacy\.claude\settings.local.json`), identical: Stop (timeout 600), Notification (matcher
  `permission_prompt|elicitation_dialog`), PreToolUse and PostToolUse (async, timeout 30), all calling
  `D:/UO/cc-autopilot/cc-autopilot.ps1`. Both files are git-excluded (`.git\info\exclude` lines 19 and 7). Nothing in
  `C:\Users\ckfle\.claude\settings.json` calls the hook.
- `docs\bug-list.md` D90-D92; `notes\cc-P94-autopilot-progress-console.md` "For Chase".

### Every reader of autopilot outside its folder

| Where | What it reads or says | Changed? |
|---|---|---|
| `D:\ShatteredLegacy\scripts\Shard-Console.ps1` | tile, tab, buttons, config, safety, CLI | yes (Part B) |
| `D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1` and its `fixtures\autopilot-*` | facts | yes; fixtures kept (history) |
| `D:\ShatteredLegacy\tools\playtest-bot\Send-BotReport.ps1` | `email.json` and `smtp-cred.xml` in cc-autopilot | yes: Golem's when its `email.json` is there, else cc-autopilot's |
| `D:\ShatteredLegacy\tools\playtest-bot\Run-OvernightPlaytests.ps1:18`, `README.md:36` | wording | yes |
| `D:\ShatteredLegacy\design\console-uo-skin\Take-ConsoleScreenshots.ps1:84` | `$script:ui.AutopilotTile` (a variable name) | no: the variable kept its name |
| `D:\ShatteredLegacy\CHANGELOG.md` | old Staff lines | no (history); a new line added |
| `D:\UO\shard-migration\tools\progress.py:22,237-261` | cc-autopilot's `state.json` and `ENABLED` | yes: `runner_folder()` reads the Golem once active; text says "Golem on/off" |
| `D:\UO\shard-migration\tools\render_dashboard.py:292,295` | wording | yes |
| `D:\UO\shard-migration\tools\tests\test_status_dashboard.py` | facts | one fact added |
| `D:\UO\shard-migration\README.md`, `dashboard.html`, `tools\progress.json` | generated by `progress.py` | regenerate at commit |
| `D:\UO\shard-migration\notes\shard-console.md` section 11 | the console notes | yes: a cc-P99 block on top |
| `D:\UO\Commit-ShardWork.ps1` | no autopilot reference (0 lines) | no |
| `status.json` readers | only the console | yes (reads `note`) |
| `D:\UO\cc-prompts\*.md` | old prompts | no (history) |
| `testing\bot-runs\...\transcripts`, `testing\play-tests.json`, `testing\bot-triage.md` | text in play-test items and transcripts | no (data) |

## Part A: `D:\UO\golem\`

`golem.ps1` started as a copy of `cc-autopilot.ps1` and keeps its behaviour and file shapes (state.json, progress.json,
status.json schema 1 plus one field, settings.json, the log line format). Differences, with lines in `golem.ps1`:

- Names: `$Root` `D:\UO\golem` (now a parameter, with `-PromptDir` and `-OldRoot`, so the tests use fixture folders),
  `golem.log`, subject prefix `[Golem]`, mutex `Local\ShardGolem`, log and email wording.
- `-NoMail` (tests): logs `test: would email: <subject>` instead of sending.
- **Start phrase**, `Test-GolemPhrase` :363 and the `Prompt` event :474. Lower-cases, turns every run of non-letters
  into one space, trims, then must equal `golem please work on the shard tasks` or `golem work` (start), or
  `golem stop` (stop). Start: `Invoke-Wake`, then the hand-off as `hookSpecificOutput.additionalContext`
  (`Write-HookText` :296), or "Pnn is already running: carry on", or "the queue is empty". Stop: sets
  `restAfterCurrent` in state.json, and `Hand-Off` :307 honours it after the next commit; with nothing running it
  rests at once. The cwd filter is the same as the other events (`D:\UO` or `D:\ShatteredLegacy`).
- **Wake and Rest events** (`Invoke-Wake` :403, `Invoke-Rest` :428), called by `Start-Golem.ps1`/`Stop-Golem.ps1` and
  the phrase. Wake: writes `golem.log`'s first line (pointing at `D:\UO\cc-autopilot\autopilot.log`, not copied),
  copies `state.json`, `settings.json`, `email.json`, `smtp-cred.xml` from cc-autopilot when missing, refuses without
  `email.json` (as Start-Autopilot did), and starts a new run from resting.
- Hand-off text `Get-HandOffText` :286 (the D91 and D92 sentences).
- status.json gains `note` (`Write-Status` :219): kept by the 10-minute watch, cleared by any other write.
- CC version: the hook output shape `{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":...}}`
  is the documented UserPromptSubmit output in this Claude Code. **Not verified in a live session:** the hook is not
  wired up until the cutover, and hooks load at session start, so the first real test is Chase's first phrase.

## Part C: D90, D91, D92

| Bug | Golem (`golem.ps1`) | cc-autopilot (`cc-autopilot.ps1`) |
|---|---|---|
| D90: "already handled" also requires that `P$n` is not `current`; Hand-Off lowers `lastHandled` to `num - 1` when it hands a number at or below it | :588, :600; Hand-Off after `startedAt` | :276, :415, :426 |
| D91: before the mid-task email, background agents launched since `startedAt` with no `<task-notification>` yet: log "waiting on N background agent(s), no email", no email | `Get-AgentsOut` :374, check :678; status `note` = `waiting on background agents` | inline, :503 (log only; status unchanged) |
| D91: the hand-off says "Run subagents in the foreground (run_in_background: false) unless the prompt says otherwise." | `Get-HandOffText` | :295 |
| D92: the hand-off says the two play-test files are machine output, committed with each prompt, not a reason to stop | `$MachineOutput` :96 | :296 |

How D91 detects an agent, from real transcripts (`c598dd1c...jsonl`, P93's session): a launch is a `user` line whose
`tool_result` text starts `Async agent launched`; its completion is a `<task-notification>` carrying the same
`<tool-use-id>` (as a `queue-operation` line and an `attachment` line). Only `Agent`/`Task` launches count. A
background `Bash` (a dev server) would never report back and would silence the email for the rest of the prompt, so
it is left out on purpose.

D92 "commit them with each prompt": already true. `Commit-ShardWork.ps1:156` stages with `git add -A`, so the two files
go into every commit. The fix is the hand-off sentence; a fact pins the `add -A` line so a change there is noticed.

cc-autopilot backup: `D:\UO\cc-autopilot\cc-autopilot.ps1.bak-20261014-golem` (taken before any edit). The diff is 29
lines, all three fixes; nothing else changed there.

## Part B: the Shard Console (`D:\ShatteredLegacy\scripts\Shard-Console.ps1`)

- `New-AutopilotConfig` :166 gains `-Kind golem|autopilot` (file names: golem.log or autopilot.log, Start-Golem.ps1 or
  Start-Autopilot.ps1, ...), plus `Kind`, `Name`, `Why`, `GolemRoot`, `AutopilotRoot`, `MoveScript`, `Hooks`,
  `WatchTask`, `LogName`.
- `Select-GolemKind` :205 (pure) and `Get-GolemConfig` :215: the Golem when `Start-Golem.ps1` and `ACTIVE` are both in
  `D:\UO\golem`, else cc-autopilot. Re-read on every refresh in `Update-AutopilotView` :5591.
- `Resolve-ActionAlias` :225: `autopilot.X` is `golem.X`. Called in `Get-ModeBanner`, `Resolve-RunMode`,
  `Get-ActionPlan`, `Get-AutopilotPlan`, `Invoke-ConsoleButton` and the CLI's `-Action`.
- Actions :944: group `Golem`, keys `golem.on/off/email/test/queue/log/settings/folder/move`, labels as the prompt asked.
  New: `golem.folder` (Explorer on the active folder) and `golem.move` (phrase `move to the golem` :729, plan :3431).
- Window titles :878 `GOLEM - golem.<key> (golem) - Shard Console`. Tile `GOLEM` :6358, tab `Golem` :6797, caption
  :6802 (with the start phrase), tooltips `golem.*`, `tile.GOLEM`, `tab.Golem`. Commit tab caption says Golem.
- Panel :3290: the start phrase line, then `active : the Golem (D:\UO\golem). ...` or `active : cc-autopilot
  (...), the Golem's predecessor. ... Move to the Golem ...`; the log heading uses the log's own name; `note`.
- Subjects :2946: `[Golem] ` and `[Shard CC] ` are both stripped before an alert is judged.
- Safety :2345-2355: both hooks refused by name; `Move-ToGolem.ps1` allowed in a window with exactly the five
  arguments (so never with `-Yes`); Explorer on the folder allowed.
- Function names (`Get-AutopilotGlance` and the rest) and `$script:ui.Autopilot*` kept their names, so the screenshot
  script and the older facts still work. The prompt left this to me.

## Part D: `D:\UO\golem\Move-ToGolem.ps1`

Steps exactly as the prompt lists them. Details worth knowing:
- Refuses (exit 3) when `current` is set in either folder's state.json, when `Commit-ShardWork.ps1` is running
  (`Win32_Process` command lines), or when either repo has `.git\index.lock`.
- Hook files are rewritten through JSON: every `D:/UO/cc-autopilot/cc-autopilot.ps1` becomes `D:/UO/golem/golem.ps1`,
  then a `UserPromptSubmit` hook `golem.ps1 -Event Prompt` (timeout 120) is added; other settings are kept. Old files go
  to `D:\UO\golem\cutover-backup\<repo>.settings.local.json` (outside both repos, so nothing new appears in git).
- The task: `Export-ScheduledTask` to `cutover-backup\old-task.xml`, re-registered as "Golem Watch" with the Golem's
  `Watch-Hidden.vbs`, then the old one unregistered. Rollback re-registers from the XML.
- Without `-DryRun` or `-Yes` it runs itself with `-DryRun` first and asks you to type `move` (or `rollback`).
- It never deletes `D:\UO\cc-autopilot`.

## Part E: words

Renamed in what agents may edit: the console and its facts, `notes\shard-console.md` section 11, `tools\progress.py`,
`tools\render_dashboard.py`, the play-test bot's mail and wording. `tools\README.md` has no autopilot mention (0 lines).

**`docs\` lines that say autopilot, for the overseer** (counted: `grep -rn -i autopilot docs/`, 3 lines):
- `docs\bug-list.md:89` D90, `:90` D91, `:91` D92: the three rows this prompt fixes. They can be marked fixed, with
  "verified against fixtures; not yet seen in a live run".
No other `docs\` file mentions it. `README.md:66` and `:233` say "Autopilot"/"autopilot" today and are generated by
`progress.py`; they read "Golem" from the next `progress.py` run (the commit runs it).

## Tests (each new one seen failing first)

### Golem hook, `D:\UO\golem\tests\Golem.Tests.ps1`

Fixture folders in %TEMP%, a stub commit, and `tests\fixtures\transcript-background-agents.jsonl` (lines shaped like the
real transcript lines above: one agent launched before the hand-off, two after, notifications for each).

- Final: **77 checks passed, 0 failed** (16 facts).
- Against the pre-fix cc-autopilot (`-Kind autopilot -Hook ...bak-20261014-golem`): **5 passed, 9 failed**: both D90
  facts, the D91 waiting fact, both hand-off text facts. (The two that pass on old code are the plain-question email
  and the `add -A` pin, which are guards, not fixes.) Against the fixed cc-autopilot: **14 passed, 0 failed**.
- The Golem-only facts against a mutant `golem.ps1` (phrase without "golem work", rest-after removed, first-start copy
  removed, `[Shard CC]` subject, Stop output for Prompt): **52 passed, 21 failed**; every Golem-only fact failed except
  `Golem_AnyOtherMessageDoesNothing` and the near-miss phrase fact, which that mutant could not break (it made the
  matcher stricter, not looser). **So those two were never watched failing.**
- My first run had 4 failures that were mine: the transcript fixture was invalid JSON (a missing `}`), and the log's
  first line was written after the copy lines. Both fixed.

### Cutover, `D:\UO\golem\tests\Move-ToGolem.Tests.ps1`

Fixture folders, both hook files built from the real one plus a permissions block, two throwaway scheduled tasks
created from the real task's XML (disabled) and always removed in `finally` (checked: none left).
- **39 passed, 0 failed** (6 facts: dry run changes nothing; refuses while a prompt runs; refuses on index.lock;
  forward; rollback restores the hook file byte for byte; without -Yes it shows the dry run and stops on a wrong word).
- Against a mutant (no UserPromptSubmit, no running-prompt refusal, old task not removed, no question): **16 passed,
  6 failed**, 4 of 6 facts red. The two that stayed green are the dry-run and index.lock facts, which that mutant did
  not touch.

### Console, `D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1`

Seven new facts: `P99_TheButtonsHaveTheGolemsLabels`, `P99_AutopilotKeysAreAliasesOfTheGolemsKeys`,
`P99_WindowTitlesSayGolem`, `P99_TheConsoleReadsTheGolemFirstAndFallsBackToTheAutopilot`,
`P99_MoveToTheGolemAsksAPhraseAndRunsTheCutoverInAWindow`, `P99_TheSafetyCheckNeverRunsEitherHook`,
`P99_TheTileSaysGolemAndShowsANote`. Updated: the P74, P83, P87 and P94 facts that pinned AUTOPILOT, Autopilot, the
seven buttons, the caption and `Run Email setup first`; the tab-order fact. The test file now pins
`$config.Autopilot` to cc-autopilot's folder, because after the cutover `Get-ConsoleConfig` would pick the Golem and
the older facts were written against cc-autopilot's paths.

- Fail-first: the seven P99 facts plus the two relabelled P74 facts against the console as it was (`git stash` of
  `Shard-Console.ps1` only, restored byte-identical after): **9 facts, 0 passed, 9 failed**.
- First full run: 2 failures, both mine: the tab-order fact still said Autopilot, and the `golem.on` tooltip had four
  sentences (the P84 rule is two). Fixed; both re-run green.
- Final full run: see "Final full run" below.

### Dashboard, `tools\tests\test_status_dashboard.py`

`test_the_golems_folder_is_read_once_it_is_active`. **15 OK**; against the old `progress.py`: 1 error (no
`runner_folder`).

### By hand

- `Shard-Console.ps1 -Action list`: the nine golem.* lines and the alias note.
- `-Action autopilot.settings -DryRun`: banner `DRY RUN golem.settings (golem)`, opens cc-autopilot's settings.json
  (cc-autopilot is the active one until the cutover).
- `-Action golem.move -DryRun`: `REFUSE A prompt is running (P99)`.
- `-Status -DryRun`: `GOLEM : RUNNING P99 4 of 11 20m`.
- `Move-ToGolem.ps1 -DryRun` against the real setup: refused for P99, then all seven steps printed; exit 3.
- Not done: the GUI at real size (the form facts build it and check labels, but nobody looked at it), and a live
  start phrase (needs the cutover and a new session).

## Deviations and decisions for Chase

1. **"Golem, stop" rests after the running prompt is committed**, as the prompt says. **Rest the Golem** (the button,
   `Stop-Golem.ps1`) rests at once, as Turn off did: the running prompt finishes but is not committed. Two ways on
   purpose; the tooltip says which is which.
2. **The phrase is strict.** "Golem, please work on the shard" or "Golem, please stop" do nothing. Only the three
   phrases match. Say if you want looser.
3. **When to cut over.** The cutover refuses while a prompt runs, and the Golem-to-be is handed prompts back to back,
   so there is rarely a gap. The natural one: this run hits its cap (`maxPerRun` 6) after P101 (runDone is 3 now; P99,
   P100, P101 make 6) and turns itself off with nothing running. Or let the queue empty, or wait for a STOPPED.
4. **The D91 check ignores background Bash commands** (they may never finish). Only agents count.
5. **cc-autopilot's D91 fix only logs**, it does not add status.json's `note` (the prompt asked for the minimal fix
   there). The Golem has the note.
6. The console's function names stay `*Autopilot*` (allowed by the prompt); every visible string is Golem.
7. `settings.json` in `D:\UO\golem` is not created now: the first wake copies cc-autopilot's (6, 45, true).

## For Chase

In order, after P99 is committed, at a moment when nothing is running (see decision 3):

1. Dry run: Shard Console, **Golem** tab, **Move to the Golem** (type `move to the golem`; its window shows the dry run
   and asks you to type `move`; type anything else to stop there). Or:

       powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Move-ToGolem.ps1 -DryRun

2. Run it: the same button and type `move`, or:

       powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Move-ToGolem.ps1

3. Open a **new** CC session in `D:\UO\shard-migration` (hooks load at start) and say:
   **Golem, please work on the shard tasks**

Rollback:

    powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Move-ToGolem.ps1 -Rollback

then a new CC session and "go". `D:\UO\cc-autopilot` stays, resting, until you delete it by hand.

## Patch notes

`D:\ShatteredLegacy\CHANGELOG.md`: new section **2026.10.14.6** (the 10-14.5 section was already committed), one
`### Staff` line; `VERSION` bumped to `2026.10.14.6`. Wiki not published.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: CHANGELOG.md, VERSION, scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1, and the three
tools/playtest-bot files. docs: notes/shard-console.md, tools/progress.py, tools/render_dashboard.py,
tools/tests/test_status_dashboard.py, this note. No file is near 5 MB (the largest, Shard-Console.ps1, is well under
1 MB). **`D:\UO\golem\` is in neither repo**, like `D:\UO\cc-autopilot\` before it, so the Golem's own files (hook,
scripts, README, tests) are not in this commit and are not backed up by git. Say if they should move into a repo.

## Final full run

`Shard-Console.Tests.ps1` under Windows PowerShell 5.1, after both fixes: **252 facts, 252 passed, 0 failed**, exit 0.
(The first full run was 252 facts, 250 passed, 2 failed, as described above.)

P99 DONE
