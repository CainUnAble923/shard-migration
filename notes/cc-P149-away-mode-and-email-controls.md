# P149: Away mode and email controls

## Headlines

- **Away mode is built and tested, but off.** You start it from:
  - the Golem tab (Away mode on, with the time in the Until box) or the web console's Away mode button;
  - `D:\UO\golem\Set-Away.ps1 -Until "Sunday 18:00"`;
  - the email command `away until Sunday 18:00`.

  While it is on:
  - **Around the clock, within usage.** The run cap, the rest after a Large prompt and the self-wake daily cap are
    lifted, and self-wake is on.
  - **Never ahead of the week's pace.** Every hand-off and wake must also pass the night shift's usage rule, so a
    weekend away never spends next week. Unknown usage means rest and check again in 30 minutes, never a blind run.
  - **A STOPPED prompt is parked, not left waiting.** Its work so far is committed and pushed on
    `golem/<name>/P<nn>-parked`, the prompt goes to `cc-prompts\parked\`, and the next prompt that cannot depend on it
    is handed.
  - **A reboot loses nothing.** The interrupted prompt is handed again and carries on in its own unfinished work.
  - **A morning digest**, and an email when away mode ends.
- **Email commands are built and tested but not live.** They need a Gmail app password, which only Chase can create.
  No real round trip by email was run. See "For Chase".
  - The commands are an allowlist of eleven.
  - A command is obeyed only from ckfleming@gmail.com, with Gmail's own DKIM and DMARC pass on top, a one-time code
    (48 hours), and under the rate limit.
  - Only the first line Chase wrote counts. Anything else is rejected silently and logged.
- **Tests:** nine new `P149_*` facts (82 checks) in `D:\UO\golem\tests\Golem.Tests.ps1`, and one Shard Console fact.
  Every new Golem fact was seen failing first: run against the pre-P149 copies, all nine failed (30 failed checks).
  - Full Golem suite: 799 checks pass. Only the two P184 facts known to fail before this prompt fail.
  - Web console: 68 tests OK.
  - Shard Console: 414 of 426 pass. The 12 failures are listed under Tests.
- **P148 is held** (the Today tab, the Needs-you inbox, the timeline and the safe renumber were never built). So:
  - `run next` uses P182's Run next (`RUN-NEXT`, nothing renamed);
  - the "inbox" is the Golem tab's away lines (both consoles), and there is no timeline to add to.

## What changed

**`D:\UO\golem`** (not a repo; backups `*.bak-20261020-P149`)

- `Away.ps1` (new, dot-sourced by golem.ps1):
  - Away mode:
    - `Test-AwayOn` :43; `ConvertTo-AwayUntil` :51 ("Sunday 18:00", "sun 6pm", "tomorrow 9:00", a date; future,
      at most 14 days); `Set-AwayMode` :78.
    - Parking: `Move-ToParked` :117, `Remove-ParkedDependents` :149, `Invoke-ParkStopped` :181.
    - The digest and the end: `Update-AwayMode` :230.
  - Email commands:
    - Codes: `Use-MailCodes` :253 (a named mutex around `mail-codes.json`), `New-MailCode` :266, `Use-MailCode` :275.
    - Reading a message: MIME and quoted-printable decoding, `Get-MailFirstLine` :337, the allowlist
      `Get-MailCommand` :347, all checks in `Test-MailCommand` :364.
    - Doing it: `Invoke-MailMessage` :474.
    - IMAP over TLS (Gmail, no Add-Type): `Invoke-Imap` :503, `Invoke-ImapPoll` :544.
- `golem.ps1`:
  - New events `AwaySet` and `MailPoll` (:160, :2896, :2903); `-MailFile` (:194) for tests.
  - `Send-Mail` puts a code in the subject and the command card in the body when mailCommands is on (:305).
  - Settings `mailCommands`, `mailCommandFrom`, `mailCommandsPerHour` (:358, :373).
  - The away usage rule inside `Get-PaceCheck` (:669). Self-wake on while away (:1485).
  - The dependents filter in the self-wake target, `Get-NextQueued` and `Hand-Off` (:1560, :2092, :2177).
  - Run cap and Large rest lifted while away (:2207, :2253).
  - `status.json` gains `away` and `mailCommands` blocks (:1894).
  - `Update-AwayMode` at each watch (:2956). Parking in the STOPPED path (:3444). A `finished` event at DONE (:3620).
- `Golems.ps1`: `Reset-GolemBranch` carries on (does not refuse) when the copy is dirty on the very branch being
  handed (:554), so a prompt interrupted by a reboot resumes on its own work.
- New `Set-Away.ps1`, `Mail-Commands.ps1` (`-SaveCredential`, `-Register`, `-On`, `-Off`, `-Unregister`, or one poll),
  `Mail-Hidden.vbs`.
- `README.md`: new section "Away mode and email controls (cc-P149)".

**`D:\ShatteredLegacy`** (branch `golem/Iron/P149`)

- `scripts\Shard-Console.ps1`:
  - New actions `golem.away` (the time from the Until box, at most 14 days) and `golem.awayoff`. They run
    `Set-Away.ps1` with exactly `-Until <yyyy-MM-dd HH:mm>` or `-Off`, which `Test-PlanSafety` allows and nothing else.
  - `Get-AwayLines` on the Golem tab: away until when, each parked prompt, the IMAP password missing, the last five
    email commands.
  - The status document carries `away` and `mailCommands`.
- `web-console\golem-actions.json`: Away mode on / off are live (they were placeholders waiting for P149).
  `console-actions.json` has the twins. `static\app.js` shows the away block under the Golem cards.
- Tests: new fact `P149_AwayModeButtonsAndTheGolemTabLines`. The P182 fact that expected Away to be refused "until
  P149" now expects it to ask for its end time.
- `CHANGELOG.md` 2026.10.20.5 (Staff) and `VERSION`.

## Security design, and how each rule was proved

| Rule | Where | Proved by |
|---|---|---|
| Allowlist only: the 11 commands, a whole line, no arguments but a time or P<nn> | `Get-MailCommand` | `P149_TheReaders...`: `deploy haven`, `status; resume`, `run next P151 && rm -rf`, `git push`, `skip everything`, `resume all now` are not commands; `P149_AnUnknownCommand...`: the card back, nothing done |
| Sender must be ckfleming@gmail.com exactly (one From header) | `Test-MailCommand` | spoofed `ckfleming@gmail.co`: rejected silently |
| The **topmost** Authentication-Results is Gmail's (`mx.google.com;`), with `dkim=pass` for gmail.com and `dmarc=pass header.from=gmail.com` | `Test-MailCommand` | dkim=fail, dmarc=fail, a forged header above Gmail's, and no header at all: each rejected silently |
| A current one-time code (48 h, unused) in the subject or the line | `Use-MailCodes` / `Use-MailCode` | no code, an expired code (49 h, also pruned), an unknown code, and the same mail sent twice (the second rejected) |
| Rate limit (mailCommandsPerHour, 6) | `Test-MailCommand` | the third command with the limit at 2: rejected |
| Only the first line Chase wrote | `Get-MailFirstLine` | a `status` reply whose quoted history says `away until...` and `resume`: neither acted on |
| Rejections are silent and logged; every command is answered with a fresh code | `Invoke-MailMessage` | no "would email" after any reject; "done: status (code ...)" with a new code |
| The credential stays in `imap-cred.xml` (DPAPI, Chase's user) and is never printed or logged | `Mail-Commands.ps1`, `Invoke-Imap` | read only by `Import-Clixml`. An IMAP error message names LOGIN without its arguments |
| What a command can do | `Invoke-MailCommandNow` | each maps to an existing hook event (SelfWake -Manual, WrapUp, StopPoint, NightShiftSet, RunNext) or to away/park; no deploy, publish, commit, shell or other setting |

## Tests

New `P149_*` facts in `D:\UO\golem\tests\Golem.Tests.ps1`. Each was seen failing first: run against copies of the
pre-P149 `golem.ps1` and `Golems.ps1`, all nine fail (7 checks passed, 30 failed).

| Fact | What it shows |
|---|---|
| `TheReadersAwayTimesCommandsAndTheFirstLine` | the time forms, the 14-day limit, the allowlist, the first line |
| `AValidCommandIsDoneAnsweredWithAFreshCodeAndTheCodeWorksOnce` | quoted history ignored; a replay is rejected |
| `ASpoofedSenderAFailedDkimAForgedHeaderAMissingOrExpiredCodeAreRejectedSilently` | eight bad messages, none answered, no code spent |
| `EachCommandDoesItsOneThing` | away until, away off, night shift on (a quoted-printable multipart message) and off, run next, skip, unpark, wrap up, resume (status is in the first fact) |
| `AnUnknownCommandGetsTheListAndTheRateLimitHolds` | the card back for an unknown line; the rate limit |
| `AwayModeRunsPastTheCapWithinTheNightUsageRule` | fixed usage: past the cap at 20% of the week; held at 80% with 3 days left (paceMode sprint does not lift it); unknown usage rests; self-wake on |
| `AwayModeParksAStoppedPromptSavesItsWorkAndSkipsWhatMayDependOnIt` | two Golems on real git repos: P101's work committed on `golem/Iron/P101-parked`; P102 (Depends on P101) and P103 (same area) skipped and kept; P104 handed; the email; status.json lists it |
| `AfterARebootTheInterruptedPromptIsHandedAgainOnItsOwnWork` | a three-hour-old claim with no session: the watch releases it, and the next hand-off carries on on `golem/Iron/P101` with the unfinished file |
| `TheMorningDigestOnceADayAndTheEndEmail` | no digest the day it was set; one at 07:10 the next day, not again at 07:20; the end email at the end time; the digest's text |

Suites, under Windows PowerShell 5.1:

- `Golem.Tests.ps1`: 799 checks pass, 5 fail. Those 5 checks are the two P184 facts that fail the same way on the
  pre-P208 code (the overseer made `server` a parallel area on 10-20).
- Assign 3/3, Codex 39/39, GolemPower 133/133.
- RemoteAgent stops at a web console confirm-word assert (`type wake gold`, P187's rule). Move-ToGolem stops on
  `Export-ScheduledTask` of a task missing here. Neither touches this prompt's code.
- Web console: 68 tests OK (1 skipped).
- `Shard-Console.Tests.ps1`: 414 of 426 pass; my new fact passes. Of the 12 failures:
  - 6 are tied to live data: the Haven cutover links, the play-test count, the `artificerrank` and `requisitions`
    commands. They fail on main too.
  - 6 need `client-data\classic-client-7.0.117.0\hues.mul`, which is git-ignored and absent from Iron's worktree:
    `EveryWindowActionClicked...` x2, `WithTheToggleOn...`, and `P135_*` x3.

## Deviations and decisions for Chase

- **Not built: parking a commit that was refused.** A build that will not pass is parked: the agent ends STOPPED, and
  STOPPED is parked. A commit refused after its retries still emails NEEDS YOU, as before. Its work could not be
  saved anywhere safe without the commit that was just refused.
- **Not parked: a STOPPED in the integrator's own folders (main).** It still waits for you. Every claiming Golem now
  works on its own branch, so this only happens with the switch back off.
- **Away mode keeps an extra PC to its hours** (the girls' laptops and their back-off). Only marathon widens those.
- **Codes are per PC.** A reply to an email that Gold or Copper sent from its own PC has no code the game PC knows;
  reply to a game-PC email or to the morning digest instead.
- **The usage rule while away is the night shift's, whatever paceMode says.** You have `paceMode: sprint` set today.
  Away mode is stricter on purpose (never ahead of the week's pace), unless marathon is on.
- **One check was denied by the unattended permission rule:** Grep for `restart:` in
  `D:\UO\golems\Iron\ShatteredLegacy\docker\uo`. I wanted to see which service is `restart: "no"`. A Bash count of
  the whole `docker\` folder already showed 16 `unless-stopped` and 1 `"no"`.

## For Chase

### Before you leave (the game PC)

1. **Docker Desktop: "Start Docker Desktop when you sign in" is off.** (`AutoStart: false` in its settings.) Turn it
   on (Settings, General). Without it, after a reboot the test shard, the web console's sidecar and the merge builds
   stay down until someone starts Docker.
2. **BIOS: "Restore on AC power loss" = Power On** (often under Power Management or APM). After a power cut the PC then
   starts by itself. I did not change it.
3. **Windows automatic sign-in for your account.** Every Golem task (Golem Watch, Shadow Iron, Golem Mail, the night
   shift, the overnight play tests) runs "only when you are signed in". Without sign-in after a reboot, nothing runs.
   Options:
   - Sysinternals Autologon for `ckfle` (the password is stored encrypted);
   - or turn off "For improved security, only allow Windows Hello sign-in" and use `netplwiz`.

   I did not change sign-in settings.
4. **Windows Update:** set Active hours to your waking hours and keep "Notify me when a restart is required" on. A
   restart is then survivable:
   - the PC signs in;
   - the tasks start at their next interval;
   - the watch releases the interrupted prompt after `claimStaleMinutes` (90) and hands it again on its own work;
   - the containers with `restart: unless-stopped` come back once Docker starts. One service is `restart: "no"`, likely
     the throwaway test shard; it stays down until its next use;
   - the overnight bot runs at its next 01:30.

### The app password (once)

1. In a browser signed in as shatteredlegacyuo@gmail.com: Google Account, Security, 2-Step Verification (on), App
   passwords. Make one named "Golem IMAP".
2. On the game PC, in PowerShell: `D:\UO\golem\Mail-Commands.ps1 -SaveCredential`. Paste the 16 letters as the
   password. It is kept in `D:\UO\golem\imap-cred.xml`, readable only by your Windows user.
3. `D:\UO\golem\Mail-Commands.ps1 -Register`, then `D:\UO\golem\Mail-Commands.ps1 -On`.
4. Try it: reply `status` to the next Golem email. The answer comes within about 2 minutes.

### Away mode

On the Golem tab, type the end time in the Until box (`2026-10-25 18:00`) and press Away mode on. Or use the web
console's Away mode on, or `Set-Away.ps1 -Until "Sunday 18:00"`, or email `away until Sunday 18:00`.
To end it: `away off` (email or button), or it ends by itself.

### The command card

Reply with **one** line; the code is already in the subject.

| Command | What it does |
|---|---|
| `status` | every Golem's state, the queue, usage, what is parked |
| `resume` | wakes every Golem on this PC that is not running |
| `wrap up` | the running prompt finishes, is committed, then the Golem rests |
| `stopping point` | the running prompt pauses cleanly and is committed |
| `away until Sunday 18:00` | away mode until then (at most 14 days) |
| `away off` | away mode ends |
| `night shift on` / `night shift off` | the night shift |
| `run next P151` | that queued prompt goes next |
| `skip P151` | park a queued prompt |
| `unpark P151` | put a parked prompt back in the queue |

Anything else gets this card back. A message that fails a check gets no answer at all; the Golem tab shows it.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration
-Branch golem/Iron/P149 -NoRefresh -NoArchive`. These are my own copies: the real folders are Shadow Iron's, and the
guard keeps me out of them. Result table (run after these notes were written):

```
Repo Result
---- ------
code dry run
docs dry run
```

No file over 5 MB was added; there is no scratch in either repo.

P149 DONE
