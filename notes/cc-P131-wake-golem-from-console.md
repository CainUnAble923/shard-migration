# cc-P131: Wake the Golem from the console (Claude Code CLI), self-wake, and a night shift

2026-10-16. Prompt: `D:\UO\cc-prompts\cc-P131-wake-golem-from-console.md` (handed by the Golem after P130, in a fresh
desktop session). Both repos were clean at the start. P125 finished DONE (its note's last line), so every part was done.
**Model:** the prompt asks for Opus; this session ran Fable (the Golem's model routing saw no model for a desktop session
and handed it anyway, as P125 designed).

## Headlines

- **The Claude Code CLI is installed** on this PC from Anthropic's documented Windows installer (`irm https://claude.ai/install.ps1
  | iex`, https://code.claude.com/docs/en/setup): native build **2.1.301** at `C:\Users\ckfle\.local\bin\claude.exe`,
  Authenticode signature **Valid, "Anthropic, PBC"**. **Not signed in** (`claude auth status`: `loggedIn: false`, exit 1):
  that is Chase's step, below. The folder is on the user PATH now (the installer left it off).
- **The Golem's hooks apply to CLI sessions.** Verified, not assumed: `claude --init-only --debug-file` in
  `D:\UO\shard-migration` logged `Hooks: SessionStart:startup [powershell.exe ... D:/UO/golem/golem.ps1 -Event SessionStart]
  finished with status 0` with no sign-in at all, so the repo's `.claude\settings.local.json` (the Golem's hooks and status
  line) loads in the CLI exactly as in the desktop app. The unattended deny hook (`D:\UO\unattended-permission.ps1`,
  `D:\UO\unattended-denials.log`) is a `PermissionRequest` hook in `C:\Users\ckfle\.claude\settings.json`, the user
  scope, which the CLI loads for every project; the docs say the same events fire "in the terminal, IDE extensions, the
  Desktop app, and cloud sessions" (https://code.claude.com/docs/en/hooks).
- **Wake the Golem (CC session)** on the console's Golem tab, with a Fable/Opus picker that follows the next prompt's
  Model line: a visible terminal window running `claude --model <alias> --permission-mode auto --name "Golem P<nn>"
  "Golem, please work on the shard tasks."` in `D:\UO\shard-migration` (the documented `--model`, `--permission-mode`,
  `--name` flags and the `claude "query"` form, https://code.claude.com/docs/en/cli-reference). Refused, each with its
  reason, while a prompt runs in a live session, when the queue is empty, when the CLI is missing or not signed in, or
  when the Golem is off. Phrase `wake the golem`; START/DONE in the action log.
- **Self-wake** (`autoWake`, on): after a context rest, a model wait or the run cap the Golem opens the next session
  itself, with the rules the prompt lists (never after a STOPPED or NEEDS YOU, never in the bot window, never past a
  long run's end, never when usage is at 95% or unknown for over 30 minutes, one per 5 minutes, 20 a day) and an email
  per wake. A refusal that clears by itself is kept and the 10-minute watch tries again.
- **Night shift** (scheduled task "Golem Night Shift", 22:30, registered and Ready): a long run until 06:30 through the
  self-wake, when the queue has prompts, nothing runs or is STOPPED, the CLI is signed in, and the usage leaves room
  (session window under 50%, the week at or under its even pace minus 10%). Unknown usage is a skip, said in the email.
  Emails "night shift starting ..." / "night shift skipped: <why>", and a summary when it ends. The bot window holds.
- **Resting, said plainly.** Every rest has a reason code, `readyAt` and `readyHow` in status.json; the state word is
  RUNNING, RESTING, STOPPED or OFF; the email subject leads with it ("[Golem] Resting: session full after P128. Ready now:
  new session, then the phrase"; "[Golem] Resting until 4:00 PM (usage limit), 15 queued"); the tile and tab show the
  reason and "ready now" or "ready in 2h 14m (4:00 PM)" counting down; a Windows toast says it on this PC. A CC "STOPPED"
  whose reason is the session's context (P129's, 10-16 09:31) is a rest: the prompt goes back to the front of the queue.
- **D95 fixed:** a turn that ends while a background command, a Monitor or an agent CC started is still out (the real
  `tool_result` texts: "Command running in background with ID:", "Monitor started (task", "Async agent launched"), or
  whose last words say it is waiting, is "RUNNING: waiting on ...", no email. A real mid-task stop emails **once per
  prompt** (today's twelve "NEEDS YOU: P129/P130 stopped mid-task" emails would have been two).
- **The two small fixes:** the start phrase takes its obvious variants ("golem please resume working on the shard
  tasks", the one that missed today at 15:55), still needing "golem" first and "shard task"; after a DONE a prompt whose
  Kind line says Large rests the session when no context figure is known (the desktop app reports none).
- **Tests:** Golem **292 of 292** (22 new P131 facts, all seen failing against the pre-change backup); console
  **336 facts, 331 passed, 5 failed**, the five being the pre-existing Haven-cutover facts (below) (9 new P131 facts, all 9 seen failing against the stashed pre-change script). No real wake was run:
  the CLI is not signed in, so the one on a dry-run prompt was not run.

## The install and its source

- Source: the native installer in Anthropic's documentation (https://code.claude.com/docs/en/setup, "Native Install
  (Recommended)", Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`), run in a scratch folder. Nothing from
  any other site or package.
- Result: `C:\Users\ckfle\.local\bin\claude.exe`, `claude --version` -> `2.1.301 (Claude Code)`;
  `Get-AuthenticodeSignature`: Status Valid, signer `CN="Anthropic, PBC", O="Anthropic, PBC", L=San Francisco, ...`
  (the docs' "Platform code signatures" check). `claude doctor`: "No installation issues found", "Not signed in to
  claude.ai". Auto-updates show as disabled by `DISABLE_AUTOUPDATER` in this session's environment only (the desktop app
  sets it for its children); a plain terminal is not affected.
- PATH: the installer said the folder was not on PATH; I added `C:\Users\ckfle\.local\bin` to the **user** PATH
  (`[Environment]::SetEnvironmentVariable('Path', ..., 'User')`), so new terminals find `claude`. The Golem does not rely
  on PATH: it uses the full path (settings.json `cliPath` overrides it).
- Credentials: none handled. `claude auth status` was read for its exit code and its `loggedIn` field only.

## What changed

### `D:\UO\golem\` (outside the repos; backups `golem.ps1.bak-20261016-p131`, `tests\Golem.Tests.ps1.bak-20261016-p131`, `settings.json.bak-20261016-p131`, `README.md.bak-20261016-p131`)

- `golem.ps1` (1,067 -> 1,776 lines):
  - `:109-111` events `SelfWake`, `NightShift`, `AutoWake`, `NightShiftSet`, `CliCheck`; params `-Model`, `-Manual`, `-On`,
    `-Off`, `-Start`, `-End`, `-Cli` (tests: a stub), `-Repo`.
  - `Get-Settings` (`:227`): the new keys and their defaults (`autoWake` true, `autoWakeMinMinutes` 5, `autoWakeMaxPerDay`
    20, `usageLimitPct` 95, `usageUnknownMinutes` 30, `cliPath` '', `cliPermissionMode` auto, `defaultModel` Opus,
    `nightShiftEnabled` true, `nightShiftStart` 22:30, `nightShiftEnd` 06:30, `nightSessionMaxPct` 50,
    `nightWeekReservePct` 10, `nightFableReservePct` 10, `nightUsageMaxAgeHours` 24, `restAfterLarge` true,
    `notifications` true); `Set-Setting` writes one key and keeps the rest.
  - The cc-P131 block after `Get-BotWindowEnd` (`:344-706`): `Get-Usage` (usage.json as a snapshot; a window past its
    documented `resets_at` counts 0), `Get-WeekAllowance` (the pace math), `Get-Cli`, `Get-CliLaunch`, `Test-CliSignedIn`
    (`claude auth status`, 20 s, answer kept in `cli.json`), `Get-CliArgs` / `Start-CliSession` (the command line; a new
    console window through `Start-Process`), `Send-Notice` (a WinRT toast under PowerShell's own app id; best effort),
    `Format-In` / `Format-Clock`, `Get-NightShiftTimes`, `Get-ReadyInfo` (readyAt and readyHow per reason),
    `Format-RestSubject`, `Test-SelfWake` (the rules, in the prompt's order), `Invoke-SelfWake`, `Get-NightShiftWhyNot`,
    `Test-NightUsage`, `Send-NightSummary`.
  - `Write-Status` (`:720`): state words RESTING and STOPPED; `readyAt`, `readyHow`, `stoppedPrompt`, `autoWake`, `wakePending`,
    `lastSelfWake`, `nightShift` {enabled, start, end, next, until, whyNot, running}, `cli` {path, signedIn, checkedUtc,
    note}. Schema stays 1 (fields added, none changed).
  - `Invoke-KeepRest` (`:836`): the subject is built from the reason and the readiness; a context, model or run-cap rest tries the
    self-wake first (`-WakeFor`), so the email says whether a session is on its way; one notification per rest.
  - `Hand-Off` (`:869`): the run cap rests with ENABLED kept (`restReason` 'run cap'); a night shift's long run ending rests
    'night shift ended' with the summary; a manual long run ending rests 'long run ended' (see Deviations); the Large
    rule; the bot window is a rest with `restUntil` (the idle stop after CC's wait hands on as before); the model wait
    emails once per prompt through `-Quiet`.
  - `Test-GolemPhrase` (`:1019`): the variants. `Get-TasksOut` (`:1033`, was `Get-AgentsOut`): commands and monitors too, by the same
    `<tool-use-id>` notification match; `Format-TasksOut`; `Test-SaysWaiting`.
  - The Stop handler (`:1621`, mid-task `:1739`): a context STOPPED is a rest (the prompt file moves back to `queue\`); a real STOPPED sets
    `stoppedPrompt`, emails "P<nn> STOPPED, needs you: <reason>" and notifies; the mid-task email is once per prompt
    (`midTaskEmailedFor`); the DONE line is logged on every path (the summary and the console read it).
  - The Prompt handler (`:1433`): after a run cap, a night shift or a long run the phrase starts a new run; a session told "already
    running" is also told what to do when it is a new session (the old one closed): read the prompt and its notes, carry
    on, nothing skipped.
  - `Watch` (`:1320`): ends a night shift whose end has passed (summary, rest), retries a pending self-wake, says once when a usage
    limit's reset time has passed (a toast).
  - `StopFailure` (usage limit): the subject "Resting until <time> (usage limit), N queued", a toast.
  - The events `SelfWake` (`:1203`), `NightShift` (`:1227`), `AutoWake`, `NightShiftSet`, `CliCheck` (`:1286-1319`).
  - `Invoke-Rest` / "Golem, stop" set `stoppedByHand` (the night shift does not wake a Golem rested by hand); the phrase
    and `Invoke-Wake` clear it.
  - Found while here: locals named `$until`, `$end` and `$on` are also this script's `[string]`/`[switch]` parameters,
    so a DateTime assigned to them silently became a string (`Get-LongRun`'s `$until` had been one since P125 and only
    worked by luck). Renamed to `$endAt` / `$isOn` with a comment at each.
- New: `Wake-Golem.ps1 -Model Fable|Opus|Sonnet` (the console's wake), `Set-AutoWake.ps1 -On|-Off`,
  `Set-NightShift.ps1 -On -Start HH:mm -End HH:mm | -Off` (writes the settings and registers or removes the scheduled
  task "Golem Night Shift": daily at the start time, `wscript //B NightShift-Hidden.vbs`, interactive logon, 10-minute
  limit), `NightShift-Hidden.vbs`, `Check-Cli.ps1` (writes `cli.json`).
- `settings.json`: the new keys added with their defaults (nothing else changed). The task "Golem Night Shift" is
  registered (Ready, 22:30 daily, user ckfle, Interactive).
- `README.md`: the new sections. `tests\fixtures\transcript-background-tasks.jsonl`: a background build and its Monitor,
  shaped like the real lines from today's transcript.

### `D:\ShatteredLegacy`

- `scripts/Shard-Console.ps1`:
  - Actions `:1113-1117` (group `Golem wake`): `golem.resume` "Wake the Golem (CC session)", `golem.autowake`,
    `golem.nightshift`, `golem.clicheck`. Phrases `:864-865` (`wake the golem`, `night shift on`). Tooltips `:1367-1374`
    (and `golem.model`, `golem.nightstart`, `golem.nightend`).
  - `New-AutopilotConfig` `:220-225`: `WakeScript`, `AutoWakeScript`, `NightShiftScript`, `CliCheckScript`, `CliFile`.
  - `ConvertFrom-AutopilotStatus`: RESTING and STOPPED; `ReadyAt`, `ReadyHow`, `StoppedPrompt`, `AutoWake`, `WakePending`,
    `LastSelfWake`, `NightShift`, `Cli`. `ConvertFrom-AutopilotSettings`: `AutoWake`, `NightShiftEnabled`,
    `NightShiftStart`, `NightShiftEnd`.
  - `Get-WindingLine`: the new reasons; `Get-ReadyLine` (`:3854`, the live countdown from `readyAt`); `Get-NightShiftLine` (`:3869`).
  - `Get-AutopilotStatusGlance` (`:4008-4023`): STOPPED (amber, the reason) and RESTING (grey; amber for a usage limit); the ready line
    under the winding line. `Format-AutopilotPanel`: `ready`, `night`, `self-wake` and `cli` lines; the settings line's
    second row.
  - `Get-AutopilotFacts`: the four scripts' presence, `CliInfo` (cli.json). `Get-ClaudeCliFacts` (`:5566`, SHELL): the CLI's path
    and, with `-Check`, `claude auth status` (15 s, kept 60 s); run only when Wake the Golem is pressed, and never on a
    dry run (that would run something).
  - `Get-AutopilotPlan` (`:4193`; `-Now` added, from `Get-ActionPlan`): `golem.resume` with its five refusals (a prompt whose
    session has gone quiet past stallMinutes is handed again, said so), the confirm text with the exact command line,
    the window `Wake-Golem.ps1 -Model X`; `golem.autowake`, `golem.nightshift` (the phrase only when turning on; the two
    time boxes), `golem.clicheck`.
  - `Test-PlanSafety`: the four scripts, each only with its exact arguments (`-Model Fable|Opus|Sonnet`; `-On|-Off`;
    `-Off` or `-On -Start HH:mm -End HH:mm`; bare). The hook and `claude.exe` are still never run from the console.
  - The tab (`:8671`): a model picker, the `Golem wake` row, the night shift's two boxes; `Test-GolemWakeReady` (`:7144`, pure) lights the
    wake button; `Update-GolemRunControls` relabels the toggles from settings.json and follows the next prompt's Model
    line until Chase picks one himself. `Invoke-ConsoleButton`: `WakeModel`, `NightStart`, `NightEnd`, `CliCheck`.
- `scripts/tests/Shard-Console.Tests.ps1`: 9 P131 facts; the two P125 facts that pinned the grey "needs P131" button
  updated; `$p125Facts.Present` gains the four scripts.
- `CHANGELOG.md` 2026.10.16.5 `### Staff`; `VERSION` 2026.10.16.5.

### Config changed outside the repos

- The user PATH (above). `D:\UO\golem\settings.json` (new keys). The scheduled task "Golem Night Shift" (new).
- Nothing in either repo's `.claude\settings.local.json` changed: the P125 hooks already cover CLI sessions.

## Tests (each new one seen failing first)

### Golem, `D:\UO\golem\tests\Golem.Tests.ps1`

- 22 P131 facts (the phrase variants; the Large rule; a context STOPPED as a rest; a real STOPPED; D95 with the new
  fixture, including once-per-prompt; the run cap as a rest and the new run; self-wake: the command line on the prompt's
  model, model wait and run cap, never after STOPPED, the bot window and the watch's retry, usage at the limit and
  unknown, spacing, daily cap and the toggle, never past a long run's end, the console's manual wake and its sign-in
  need; the night shift: the pace math from a fixed clock, the start, each skip reason, the end with the summary, the bot
  window; the usage-limit readiness and the ready toast; the two toggle events).
- Against the backup `golem.ps1.bak-20261016-p131` (`-Only P131`): **0 checks passed, 22 failed** (every P131 fact red).
- The CLI in tests is a `.cmd` stub (`New-CliStub`): "auth status" answers from a marker file, any other call is written
  to `cli-calls.txt`. `Get-Cli` returns nothing under `-NoMail` unless `-Cli` is given, so a test never reaches the real
  `claude.exe` (before that guard, one run did: the real `auth status`, exit 1).
- Seven P125 facts pinned the old subjects ("P100 done, context 72% full", "next is P101, wants Fable: ...",
  "paused: usage limit", ...) and D91's note wording; updated to the new ones (the prompt's section 6 supersedes them).
- Full suite: **292 checks passed, 0 failed** (PowerShell 5.1).
- `Move-ToGolem.Tests.ps1`: untouched (it fails at load since the old scheduled task went at the cutover, as P125 noted).

### Console, `D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1`

- 9 P131 facts: the wake's phrase and command line (and the model from the prompt), each refusal with its reason (and
  the quiet-session hand-again), the safety check's exact arguments (and nine refusals), the status parse, the tile for
  each rest reason with the countdown from a fixed clock and STOPPED, the night shift line, when the wake button lights,
  the toggles' arguments and phrase, the tab's wake row and labels.
- Against the pre-change console (`git stash` of the script only): **9 facts, 0 passed, 9 failed**.
- Full suite: **336 facts, 330 passed, 6 failed** in the last full run, the sixth being
  `P125_WrapUpAndStoppingPointAskThePhraseAndToggleToCancel`, whose fixture (`$p125Facts`) had no `Enabled` or
  `QueueNames`, so the new wake refused for the wrong reason; the fixture was given both and that fact, the other two
  P125 Golem facts and all nine P131 facts were rerun together: **12 facts, 12 passed, 0 failed**. So 331 of 336, with
  the five below the only red ones.
- Five facts fail before and after this change, so they are not P131's: `P83_TheLinksOpenTheTwoPagesAndNothingElse`,
  `P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo`, `P101_TheTileAndTheTabAreBuiltAndDrawn`,
  `P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing`, `P107_LinksAndSitesPointAtHavenAfterTheCutoverAndAtThisPcBefore`:
  each expects the play-test links and sites on this PC and gets Haven (the ops cutover, P107), e.g. "expected
  [http://localhost:8093/] but got [http://192.168.1.61:8093/]". For the overseer: those facts pin the pre-cutover
  default and need an ops-mode pin like P108's `-LiveEnabled`.
- Player-package suites: no package file changed, not rerun.

### Verified by hand

- The toast: the same WinRT code run from a non-interactive PowerShell 5.1 returned without error ("toast shown without
  error"); whether it drew on the desktop I could not see from here.
- The CLI's hooks: the `--init-only --debug-file` run above.
- The night-shift task: `Get-ScheduledTask`: Ready, trigger daily 22:30, principal ckfle Interactive.

## Play-test items

None: staff tooling only, nothing in game.

## Deviations and decisions for Chase

- **Sign-in is yours** (the prompt's rule): nothing of yours was read, copied or stored. Until you sign in, Wake the Golem
  refuses with "not signed in", self-wake refuses the same way, and tonight's night shift at 22:30 will email
  "night shift skipped: the Claude Code CLI is not signed in" (or "usage unknown": see next). Steps under For Chase.
- **The first CLI session has to be opened by hand.** Self-wake and the night shift read the plan usage from
  `usage.json`, which only Claude Code's status line writes, and only in a CLI session (P125 found the desktop app never
  feeds it; today's `D:\UO\golem` has no `usage.json` at all). So the first time, press Wake the Golem (CC session) on the
  console (it does not check usage) or say the phrase in a CLI session; from then on the figures exist.
- **"Unknown for over 30 minutes" bites after any idle spell.** The prompt's self-wake rule refuses when the usage
  figure is older than 30 minutes, and it goes stale whenever no session has been active for that long, so a self-wake
  the watch retries after the bot window (ends 03:00) will usually find it stale. I kept the rule as written and made the
  minutes a setting (`usageUnknownMinutes`); raise it (a stale figure is an upper bound: usage only falls while idle) if
  the log shows refusals "usage unknown for N min". The night shift, where the prompt gave no minutes, accepts a figure up
  to `nightUsageMaxAgeHours` (24) old for the same reason, and a window whose documented `resets_at` has passed counts as
  0% (Claude Code drops such a window itself).
- **Permission mode of a woken session: auto** (`--permission-mode auto`, settings.json `cliPermissionMode`). The prompt
  named no mode; your user settings carry an `autoMode` environment, so your desktop sessions run in auto, and an
  unattended CLI session in the default mode would hit a permission prompt on its first write and have it denied by the
  unattended hook. Change the key if you want another mode.
- **A long run that reaches its end time now rests** ("long run ended", ready now; the phrase starts a new run under
  maxPerRun) instead of P125's "back to maxPerRun in the same session": the prompt says a self-wake never happens past a
  long run's end, and the same session carrying on past it would have been the same thing by another door. A night
  shift's end rests "night shift ended" (next night shift 22:30, or the phrase).
- **The run cap now rests with ENABLED kept** (RESTING, "ready now") instead of going OFF, so it can be a reason with a
  readiness like the others and the Golem can wake the next session itself; the phrase starts a new run as before.
- **Email subjects changed** for every rest (section 6 of the prompt), so the P125 facts that pinned them were updated.
- **The night shift's wake skips the 30-minute usage rule** (it has just checked the usage by its own, stricter rule);
  every other self-wake rule applies to it.
- **The console's Wake button does not check usage** (the prompt lists four refusals; it is you pressing it) and does not
  count toward the self-wake limits; its wake is not emailed.
- **What a closed window does:** the Golem's state keeps the prompt as running. The console's Wake button refuses while
  the status is a live RUNNING; once the session has been quiet past `stallMinutes` (45) it lights again and the new
  session is told to carry on with that prompt from its file and notes (the hand-off text says so); never skipped. The
  Golem's own wake does the same at a rest.
- **Notification through P143's remote console:** not built (P143 does not exist yet); the toast is local to this PC.
- **D95's detection reads undocumented transcript text** (the `tool_result` wording of background commands and
  Monitors, as D91 did for agents), checked against today's real transcript; if Claude Code rewords them the fallback
  is CC's own last words ("waiting on ..."). The fixture carries the exact strings.
- **Five pre-existing console facts fail** (the Haven cutover, above). Not touched: the prompt says each new test fails
  first and the suites are green under 5.1; these five are not this prompt's and were red before it.
- **Not mine, riding in this commit:** `docs/feature-queue.md` (the overseer's F-50, written 15:55, after this prompt
  started) and the play-test mirror (`testing/SUMMARY.md`, `testing/play-tests.json`, refreshed from Haven by the
  preflight). I did not edit `docs\`.
- **Found by this prompt, for the bug list:** the `$until` parameter collision in `golem.ps1` (above); and the P125
  `Get-LongRun` returned its end as a string, which the comparisons tolerated.

## For Chase

1. **Sign in once** (your account; the Golem never sees it): open a terminal (Windows PowerShell is fine, a new one so
   PATH has the folder), run `claude auth login`, finish in the browser, then on the console's Golem tab press
   **Check CLI sign-in** (or run `D:\UO\golem\Check-Cli.ps1`) so the tab reads "cli: ..., signed in".
2. **Wake the Golem (CC session):** pick Fable or Opus (it starts on what the next prompt asks for), press the button,
   type `wake the golem`. A terminal window opens, says the phrase and takes the next prompt. It is refused with the
   reason on screen when a prompt is running, the queue is empty, the CLI is missing or not signed in, or the Golem is
   off (then press the old Wake the Golem first). Closing the window ends that session; the prompt it was on is handed
   again at the next wake.
3. **Self-wake** is on. The Golem tab's "Self-wake: on (turn off)" button toggles it (Set-AutoWake.ps1). The tab's
   `self-wake` line shows a pending wake and the last one; emails say "[Golem] woke a Fable session for P132".
4. **Night shift** is on, 22:30 to 06:30: the two boxes beside "Night shift: on (turn off)" set the times (turning it on
   asks `night shift on`); the tab's `night` line says when the next run is and why it would not run as things stand.
   Expect "[Golem] night shift starting: P132 to P151 queued, usage S% session, W% week" at 22:30 when everything allows
   it, "night shift skipped: <why>" when not, and "night shift summary: ..." at breakfast. Tonight, until you sign in and
   a CLI session has reported usage, it will say skipped.
5. **Resting:** the GOLEM tile says RESTING with the reason and "ready in 2h 14m (4:00 PM)" or "ready now ...", or
   STOPPED with what CC needs from you; the same email subject leads with it, and a Windows notification pops when it
   starts resting and when a usage limit has reset. Self-wake usually means you need not do anything.
6. The new settings are in `D:\UO\golem\settings.json` (Golem settings button): `autoWake`, `autoWakeMinMinutes`,
   `autoWakeMaxPerDay`, `usageLimitPct`, `usageUnknownMinutes`, `cliPath`, `cliPermissionMode`, `defaultModel`, the
   `nightShift*` keys, `restAfterLarge`, `notifications`.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
=== code  (D:\ShatteredLegacy) ===
  4 file(s) pending: CHANGELOG.md, VERSION, scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1
  dry run: would add, commit and push

=== docs  (D:\UO\shard-migration) ===
  4 file(s) pending: docs/feature-queue.md, testing/SUMMARY.md, testing/play-tests.json, notes/cc-P131-wake-golem-from-console.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

P131 DONE
