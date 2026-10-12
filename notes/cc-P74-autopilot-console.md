# cc-P74: Autopilot tab and glance tile in the Shard Console

Builder: Claude, in `D:\ShatteredLegacy`, run by the autopilot itself: the hook handed this prompt over at
2026-10-12 15:49:41, so this is also the autopilot's first real hand-off. Line numbers are in
`D:\ShatteredLegacy\scripts\Shard-Console.ps1` unless a file is named.

## Status: finished on 2026-10-12

Built and tested: 175 facts, all passing (157 before, 18 new). Every new button was dry-run. **Turn on and Send test
email were not run for real**, as the prompt said. Nothing was committed: the autopilot commits after the DONE line.

## Headlines

- **A fifth tile, AUTOPILOT**, after PUBLIC DNS. It says one of these:
  - `OFF` (grey)
  - `IDLE` (grey), e.g. `1 queued; send CC "go" to start`
  - `RUNNING` (green), e.g. `P74 for 42m 0s, 2 queued`
  - `NEEDS YOU` (amber), with the subject of the email the hook sent
  - `UNKNOWN` (grey)

  A failed email since the last hand-off turns it amber and adds `; email failing`. It is redrawn on every status
  refresh (every 30 s) and whenever the Autopilot tab is opened. `-Status` prints it as a fifth line after the three
  docker tiles, and so does the form's status panel.
- **An Autopilot tab** (just before LIVE shard), with six buttons: Turn on, Turn off, Email setup, Send test email,
  Open the queue folder and Open autopilot.log. Below them is a read-only panel. Each of the first four opens the
  autopilot's own script in a PowerShell window of its own, which stays open. Turn on is refused, with "Run Email setup
  first", while there is no `email.json`.
- **The judging is pure**, in CORE: `Get-AutopilotGlance` (`:2212`) takes the ENABLED flag, the text of state.json,
  the log tail and the queue listing, and returns the tile. The SHELL only gathers those four facts,
  in `Get-AutopilotFacts` (`:2999`). It reads the last 400 lines of the log, never the whole file.
- **The safety check now guards the autopilot's folder** (`:1616`). Nothing in `D:\UO\cc-autopilot` can run except its
  four scripts, each in a window of its own. Notepad opens only `autopilot.log`, and **the hook `cc-autopilot.ps1`
  is never run from the console**, because it commits and pushes.
- **New file outside the repo:** `D:\UO\cc-autopilot\Send-TestEmail.ps1`. It is ASCII and uses the hook's own SMTP
  code (`cc-autopilot.ps1:70-78`). It reads `email.json` and `smtp-cred.xml` and prints sent or the error. Exit codes:
  0 sent, 1 not set up, 2 failed.
- **The Commit tab caption** has one new line: while autopilot is on, it commits and pushes after each P<nn> DONE, so
  a manual commit is rarely needed. The refusal logic is unchanged.
- **I found three bugs in `cc-autopilot.ps1` and did not apply the fixes.** See "For Chase". The first means a
  prompt that stops early and is then finished is never committed.

## What the tile reads, and how it judges

### What it reads (SHELL, `Get-AutopilotFacts`, `:2999`)

| Fact | How | If it fails |
|---|---|---|
| ENABLED | `Test-Path` | recorded error, so the tile is UNKNOWN |
| state.json | `ReadAllText` | no file is `$null`, the hook's own default (`cc-autopilot.ps1:60`) |
| autopilot.log | `Get-Content -Tail 400` (`TailLines`, `New-AutopilotConfig` `:137`) | no file is no lines |
| queue\ | `Get-ChildItem -File`, names only | recorded error, so the tile is UNKNOWN |
| email.json, smtp-cred.xml | `Test-Path` only | never opened; a fact tests this with a credential file that would throw if opened |
| the four scripts | `Test-Path` | a missing one makes its button refuse and name it |

All paths come from one `Autopilot` block in `Get-ConsoleConfig`, built by `New-AutopilotConfig` (`:137`). That way the
facts can point the whole thing at a temp folder.

### How it judges (CORE)

- `ConvertFrom-AutopilotLog` (`:2111`) keeps only lines shaped like the hook's `Log` (`cc-autopilot.ps1:51`):
  `yyyy-MM-dd HH:mm:ss`, two spaces, the event, the text. Everything else is pasted Commit-ShardWork output and is
  skipped. The pattern is `$script:AutopilotLinePattern`, just above.
- `Get-AutopilotQueue` (`:2129`) reads the queue the way the hook does (`cc-autopilot.ps1:112-118`):
  - `cc-P<nn>-*.md` files run, sorted by the number, so P9 comes before P10.
  - Any other `.md` file is "ignored".
  - Files that are not `.md` are not prompts and are not listed.
- `ConvertFrom-AutopilotState` (`:2138`) reads state.json. No file gives the hook's default. An empty file, a file
  that is not JSON, or a lastHandled that is not a number throws, which makes the tile UNKNOWN.
- `Get-AutopilotView` (`:2166`) finds the last `handed P<nn>` line (`cc-autopilot.ps1:139`). Among the lines after it,
  if the newest `emailed:` line has a subject that is an alert, that subject is the alert. `Test-AutopilotAlert`
  (`:2160`) counts as alerts:
  - subjects starting `NEEDS YOU` (`:128`, `:166`, `:230`)
  - subjects containing `STOPPED` (`:182`)
  - subjects containing `COMMIT FAILED` (`:215`)

  Any `EMAIL FAILED` line after the hand-off sets "email failing".
- `Get-AutopilotGlance` (`:2212`) decides, in this order:
  1. ENABLED unknown: UNKNOWN.
  2. No ENABLED: OFF.
  3. On, but state.json or the queue could not be read: UNKNOWN.
  4. An alert: NEEDS YOU.
  5. `current` is set: RUNNING.
  6. Otherwise: IDLE.

  Then email failing makes the tile amber.
- **NEEDS YOU comes before RUNNING on purpose.** When CC stops mid-task, the hook emails but leaves `current` set
  (`cc-autopilot.ps1:228-231`), so RUNNING alone would hide the question. After STOPPED or a failed commit, the hook
  clears `current` (`:179`, `:210`), so IDLE alone would hide those too.
- **An alert is cleared by the next hand-off, or by a newer email that is not an alert.** For example, "Queue empty,
  P74 done and pushed" after Chase answered.
- `Format-AutopilotPanel` (`:2260`) draws the tab's panel:
  - on or off
  - the running prompt and for how long
  - the last prompt handled (said DONE or STOPPED)
  - any alert, and failing email
  - the queue in run order, with each ignored file named as IGNORED
  - the last 20 action lines of the log, without commit output

## The tab

`Get-AutopilotPlan` (`:2314`) builds every button's plan, from `Get-ActionPlan` like every other tab. The keys are in
`Get-ConsoleActions` (`:799-804`).

| Key | Plan | Refused when |
|---|---|---|
| `autopilot.on` | SAY, then WINDOW `powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\UO\cc-autopilot\Start-Autopilot.ps1`, then LOG | no `email.json` ("Run Email setup first"); script missing |
| `autopilot.off` | SAY (a running prompt still finishes; nothing is committed after it), WINDOW `Stop-Autopilot.ps1`, LOG | script missing |
| `autopilot.email` | SAY, WINDOW `Setup-Email.ps1` (it asks for the password in that window), LOG | script missing |
| `autopilot.test` | SAY, WINDOW `Send-TestEmail.ps1`, LOG | no `email.json` or no `smtp-cred.xml`; script missing |
| `autopilot.queue` | OPEN `explorer.exe D:\UO\cc-prompts\queue` | never |
| `autopilot.log` | OPEN `notepad.exe D:\UO\cc-autopilot\autopilot.log` | no log yet |

- **All six are `RunIn = 'here'`.** Each script runs in a window of its own as a `window` step: the same step
  "Tail the log" uses, with `-NoExit`, so the window stays open to be read. The console does not spawn its own
  child for them. Setup-Email needs a real console for `Read-Host -AsSecureString`, and a `window` step gives it one.
- **D37 still holds.** Headless with no `-Mode`, on, off, email and test are refused (exit 2). Queue and log only open,
  so they run.
- **The banner** for a headless run says `AUTOPILOT - autopilot.on (autopilot)`, not "acts on the shard".
- **The caption** says:
  - what autopilot does
  - that it commits AND PUSHES to GitHub on its own after every P<nn> DONE
  - that Turn off lets the running prompt finish
  - that numbers belong to the overseer: nothing here reorders or renumbers the queue.
- **`-Action list`** shows the six keys and one line about `-Mode Execute`. **`-Status`** prints the tile, read live
  from the folder even under `-DryRun`, because it is not docker.

## Test results

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1`: **175 facts, 175 passed,
0 failed.** The baseline before any change was 157 of 157.

Two existing facts had to change:
- `TheFormBuildsFromACaptureWithoutBeingShown`: its tab list now has Autopilot before LIVE shard.
- My own first draft of a fact assumed `Sort-Object` sorts in ordinal order. It does not, so the fact now compares the
  names without relying on order.

The 18 new facts:

| Fact | What it checks |
|---|---|
| `P74_OffIsGreyAndSaysTheQueue` | OFF |
| `P74_RunningIsGreenWithThePromptItsAgeAndTheQueue` | RUNNING, from the real state.json and log at hand-off |
| `P74_IdleSaysGoOnlyWhenSomethingIsQueued` | IDLE, including a missing state.json |
| `P74_AnUnnumberedFileIsNamedAsIgnored` | the real 15:30 case |
| `P74_TheQueueRunsInNumberOrderNotNameOrder` | P9 before P10 before P100 |
| `P74_NeedsYouWhenCcStoppedMidTask` | NEEDS YOU while RUNNING |
| `P74_NeedsYouAfterStoppedAndCommitFailed` | NEEDS YOU while state.json says idle |
| `P74_AFailedEmailTurnsTheTileAmber` | email failing |
| `P74_CommitOutputIsSkippedAndAHandOffClearsAnOldAlert` | pasted commit output, and an answered alert |
| `P74_AnythingUnreadableIsGreyUnknownNeverRed` | unreadable or empty state.json, ENABLED unknown, queue or log unreadable |
| `P74_AnEmptyLogIsNotAProblem` | an empty log |
| `P74_TheStatusReportListsTheAutopilotTileAfterTheThree` | the `-Status` and panel line |
| `P74_TurnOnIsRefusedUntilEmailIsSetUp` | the email refusal |
| `P74_EachButtonRunsItsOwnScriptInAWindowOfItsOwn` | every plan, and that each passes the safety check |
| `P74_TheSafetyCheckNeverRunsTheHookOrAnythingElseInItsFolder` | the hook, other files, the credential and Notepad elsewhere are refused |
| `P74_TurningOnOrOffNeedsAModeHeadless` | D37 and the banner |
| `P74_TheFactsTailTheLogAndOnlyCheckTheCredentialExists` | the real SHELL against a temp folder: tail of 50 out of 300, a credential that would throw if opened |
| `P74_TheTileAndTheTabAreBuiltAndDrawn` | the form, built and not shown |

**Fixtures** (`scripts\tests\fixtures`):
- `autopilot-log-2026-10-12.txt` and `autopilot-state-running-2026-10-12.json` are copies of the real files at
  hand-off.
- `autopilot-state-unreadable.json` is a cut-off copy of it.
- `autopilot-log-{needs-you,stopped,commit-failed,email-failed,commit-output}.txt` were built from the hook's own
  format strings (each cited by line in the test file), with the real output of `Commit-ShardWork.ps1 -DryRun` pasted
  in where the hook pastes it. **No real NEEDS YOU, STOPPED or failed email has happened yet, so those shapes are
  copied from the hook's code, not observed.**

**Dry runs**, `-Action autopilot.<key> -DryRun`, each printed the plan in the table above, ending `(dry run: nothing was
run)`. Headless `-Action autopilot.on` with no mode printed REFUSED and exited 2. `-Status -DryRun` printed
`AUTOPILOT : RUNNING  P74 for 9m 9s, 1 queued`, read live. The 1 queued was `cc-P83-play-test-queue.md`, which arrived
during this prompt.

**Not tested:** clicking in the shown form, or the four windows for real. Turn on and Send test email were not run,
as the prompt said.

## Deviations and decisions for Chase

1. **A missing state.json is not UNKNOWN.** The prompt said "missing or unreadable files are grey UNKNOWN". But the
   hook treats no state.json as "nothing running, nothing handled" (`cc-autopilot.ps1:56-61`), and that is the real
   state before the first hand-off. Today, ENABLED was there with no state.json and a numbered prompt queued, so the
   tile would have said UNKNOWN when IDLE was true. The same goes for a missing log, which is just nothing logged yet.
   Unreadable files, an empty or broken state.json, a queue that cannot be listed and ENABLED that cannot be checked
   are all UNKNOWN.
2. **IDLE is grey**, not blue. The tiles have no blue (`Get-TileColors`), and grey was allowed.
3. **The buttons open their scripts through a `window` step**, not the console's own child window (`RunIn 'here'`, see
   the tab section). The prompt asked for each script "in a window of its own", and this gives exactly that with the
   script's own output, plus a real console for Setup-Email's password prompt. Dry run prints the plan in the console
   instead of opening a DRY RUN window.
4. **The tile also counts unnumbered files**, as `; 1 unnumbered file(s) ignored`. That is the exact trap of
   2026-10-12 15:30, when the draft sat in the queue unnumbered.
5. **Send-TestEmail.ps1 does not write to autopilot.log.** Everything else in that folder is the hook's, so the test
   email shows in the window and in `shard-console.log` (LOG step) only.
6. **The prompt's line "Only `cc-P74-*.md` runs"** came from replacing every `P<nn>` when the draft was numbered. I
   followed the hook's real rule (`cc-P<nn>-*.md`).

## For Chase

**Bugs in `D:\UO\cc-autopilot\cc-autopilot.ps1` (reported, not applied, as the prompt says):**

1. **A prompt that stops early and is then finished is never committed, and the next prompt starts on top of its
   uncommitted work.**
   - STOPPED sets `lastHandled = n` (`:179`).
   - When you answer CC and it ends `P<nn> DONE`, the DONE branch sees `n -eq lastHandled` (`:188`) and takes the
     "already committed" path. That path does no commit and, because `current` is empty, hands off the next prompt
     (`:190`).
   - Fix: keep a separate `lastCommitted` field. Set it only after a successful commit (beside `:210`), and compare
     DONE against it at `:188`. STOPPED can keep setting `lastHandled` for its own check at `:178`.
2. **After STOPPED, a further stop without DONE starts the next prompt.**
   - STOPPED clears `current` (`:179`).
   - If you answer and CC asks you something else, the next Stop has no DONE and no current, so the idle branch
     (`:234-235`) hands over the next queued prompt while the stopped one is unfinished.
   - Fix: at `:179` leave `current` and `currentFile` set and add `stopped = true`. Clear them only on DONE (`:210`).
     The idle branch then never runs mid-prompt; the "stopped mid-task" branch (`:228`) emails instead. The AUTOPILOT
     tile reads `current`, so with this fix a stopped prompt would show RUNNING behind its NEEDS YOU, which is right.
3. **A `-DryRun` of the hook writes to the real autopilot.log.** `Log` always appends to `$LogFile` (`:52`). So a dry
   run with `_test\*.json` logs `handed P99 ...` (`:139`), which the tile reads as a real hand-off: it clears a real
   NEEDS YOU. Fix: when `$DryRun`, write only to stderr, or to `_test\dryrun.log`.

**Smaller things, no change needed:**
- The hook checks STOPPED before DONE, in the last 600 characters of CC's final message (`:172-174`). A final message
  that explains the protocol by quoting the stop marker would count as a stop. CC prompts should keep the marker out
  of the final message except for real.
- The commit message the hook builds comes from the prompt's first `#` heading (`:196-199`). This prompt's heading is
  still `cc-P-autopilot-console: ...` (the draft name), so the P74 commit will say that. The overseer could renumber
  the heading too when numbering a draft.
- `cc-P83-play-test-queue.md` arrived in the queue at 15:57 during this prompt. The hook will hand it over after this
  DONE.
- The console's existing form-building facts now also read the real `D:\UO\cc-autopilot` once, read-only, when they
  refresh the tile. They cannot fail on it (`Get-AutopilotViewNow` never throws).

**To try it:**
1. Launch the console.
2. Look at the fifth tile, then open the Autopilot tab.
3. Try Send test email, which is safe: it only sends one email.
4. Before you leave CC on autopilot, decide on bugs 1 and 2 above.

**Patch notes:** a new `## 2026.10.12.2` section with one `### Staff` line (the 2026.10.12 section was already
committed with P73). `VERSION` is bumped to `2026.10.12.2`. The wiki page was not published.

P74 DONE
