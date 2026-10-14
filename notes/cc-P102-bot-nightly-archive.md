# cc-P102: the overnight bot on a nightly schedule, only when there is work, email before and after, 14-day archive

2026-10-14. Tooling. Prompt: `D:\UO\cc-prompts\cc-P102-bot-nightly-archive.md`. Code in
`D:\ShatteredLegacy\tools\playtest-bot\`, one small change in `D:\UO\shard-migration\tools\playtests.py`. Not committed
(autopilot commits after DONE). Both repos were clean at the start.

## Headlines

- **The runner now asks first whether the night has work** (`uobot/work.py`). Work means an **open** play-test item
  with a bot check that has not run against the code it would test. No work: one line in `D:\UO\bot-shard\overnight.log`,
  no email, exit 0, nothing built and no run folder. `-Force` runs anyway; `-Only` runs the named checks.
- **"The same code" is decided by git:** no change in `server/`, `docker/uo/` or `tools/playtest-bot/uobot/` between a
  run's commit and tonight's. So a docs-only commit is not work, but a server change or a change to the checks is.
- **Re-opened items needed a new field.** Re-opening an item on the play-test page cleared `resultAt` and left no
  trace. `tools/playtests.py` now writes `reopenedAt` when an item goes back to Open from a result. The play-test
  service picks this up only after a restart (For Chase, step 2).
- **Three emails, one mail path** (`Send-BotReport.ps1`, now with `-TextFile`):
  - "Overnight play tests starting: N checks on <commit>";
  - the existing summary, now with the report path and an archive line;
  - "Overnight play tests FAILED on <commit>: <reason>", with the last 40 lines of run.log.
  `-NoEmail` silences all three.
- **`Install-OvernightTask.ps1`** registers "SL overnight play tests" daily at 01:30. **Not registered:** Chase runs it once.
- **The 14-day archive** copies each old run's `transcripts\` to iCloud Drive and verifies it: file count, total
  bytes, and SHA-256 of every file. Only then does it remove the repo copy. A missing iCloud folder or a failed verify
  removes nothing, and the email says so.
- **Tests: 24 new bot facts and 3 new play-test-store facts, each seen failing first.** Final: bot 33 of 33, shard-migration
  Python tools 46 of 46, importer Pester 20 of 20.
- **Tonight, on the real data:** the work check finds **18 items** with work on 0b4cc29 (the server has changed since
  both earlier runs, 36c7ae9 and 10f4088). Estimate: about 166 minutes.
- **One thing I got wrong.** The first fail-first run started a real bot run (section "The stray run"). Rule 1 held:
  live and test were untouched, and no email went out. The scratch container `sl-modernuo-bot` is still up on 127.0.0.1:2595.

## What changed

### `D:\ShatteredLegacy\tools\playtest-bot\`

| File:line | Change |
|---|---|
| `Run-OvernightPlaytests.ps1:30` | `[CmdletBinding()]`, so an unknown parameter fails instead of being ignored (the cause of the stray run). New parameters: `-Force`, `-Config`, `-PlayTests`, `-ArchiveDrive`, `-MailOutbox` (tests: write mails to a folder) |
| `Run-OvernightPlaytests.ps1:143-169` | Step 0, the work check, before any build, container or repo write. A failed check (a bad `-Commit`) mails the crash text and exits 2 |
| `Run-OvernightPlaytests.ps1:171-180` | Run folder, the `work:` lines in run.log, the before email |
| `Run-OvernightPlaytests.ps1:183-313` | P91's steps 1 to 6, unchanged except: inside `try`; `Assert-Rule1` now runs after the before email (it changes nothing, so the order is safe); `$botStarted` (:274) records that this run started the scratch shard; `results.json` must exist after the checks |
| `Run-OvernightPlaytests.ps1:208,253` | `world.json` gets `commitSha` (the full commit), so the next night can compare code |
| `Run-OvernightPlaytests.ps1:314-341` | The crash path: stops `sl-uo-bot` only if this run started it, re-checks rule 1, runs the archive, mails the crash text, logs a night line, exits 3 |
| `Run-OvernightPlaytests.ps1:342-353` | Step 7: archive, report with `--archive-note`, after email, night line |
| `Run-OvernightPlaytests.ps1:92,106` | `Send-Mail` (the one place mail goes, so `-NoEmail` and `-MailOutbox` cover all three) and `Invoke-Archive` (never throws) |
| `uobot/work.py:90` `find_work` | The rule above. Old runs without `commitSha` are read from their `code` line (`run_sha` :40). An `ERROR` result is not a run. Re-open is compared with the run folder's stamp (local time, :48) in UTC |
| `uobot/work.py:124` `estimate_minutes` | 25 min build and boot + soak + each check's mean seconds from its newest run (60 s if never run) x `-Runs` |
| `uobot/notify.py:21,41` | The before and crash texts |
| `uobot/archive.py:56` `archive_old`, `:38` `verify` | The archive. Age is from the folder's `yyyy-MM-dd-HHmm` name. The drive is never created (missing = iCloud is not there); `Shattered Legacy\bot-runs` under it is. Leaves `transcripts-archived.json` (to, files, bytes, at) |
| `uobot/report.py:25,88` | `--archive-note`, one line in email.txt |
| `Send-BotReport.ps1:15,20` | `-TextFile` |
| `Install-OvernightTask.ps1` (new) | Register / `-Uninstall` / `-DryRun` |
| `overnight.json` (new) | taskName, scheduleTime 01:30, retentionDays 14, archiveDrive `D:\Cloud Drives\iCloudDrive`, archivePath `Shattered Legacy\bot-runs`, playTests |
| `tests/test_overnight.py` (new) | 24 facts, below |
| `README.md` | "Nightly (cc-P102)" section; layout table |

### `D:\UO\shard-migration\tools\`

| File:line | Change |
|---|---|
| `playtests.py:221` | `new_item` has `reopenedAt: ""`; `ordered_item` therefore adds it to every item on the next save (machine output in `testing\play-tests.json`) |
| `playtests.py:543-544` | `set_result`: Open on a non-Open item writes `reopenedAt = now_iso()`. Open on an Open item does not; a later Pass or Fail keeps it |
| `tests/test_playtests_reopen.py` (new) | 3 facts |

`D:\ShatteredLegacy\CHANGELOG.md`: new section **2026.10.14.9** (10-14.8 was committed), one `### Staff` line;
`VERSION` 2026.10.14.9. Wiki not published.

## Tests

`cd D:\ShatteredLegacy\tools\playtest-bot; python -m unittest discover -s tests` and
`python -m unittest tools/tests/test_playtests_reopen.py` in shard-migration.

- **Work check (11):** none when every open item ran on this code; items without a check and closed items never count;
  a new item counts; a run on older code counts but a docs-only commit does not; a change to `uobot/` counts; re-opened
  after the last run counts, before does not; ERROR is not a run; old runs read from their code line; `-Force` runs and
  says forced; a target commit is resolved; the estimate. Each works on a throwaway git repo.
- **Emails (4):** before (subject, ids with reasons, length, both stop commands, "all 20 checks"), before forced, crash
  (subject, exactly the last 40 lines, run folder, archive line), after (summary first line, report path, archive line).
- **Archive (5):** copied, verified, removed, report and results kept, pointer written, the 10-day run kept; a copy with
  an extra byte removes nothing; a same-size byte flip is caught by the hash and removes nothing; a missing root removes
  nothing and is not created; nothing old says so.
- **Scripts (4):** installer `-DryRun` prints one call per line and registers nothing (`schtasks /Query` fails); `-Uninstall
  -DryRun`; the runner with no work writes exactly one night line, no run folder, no mail, exit 0; the runner's crash
  (a Rule 1 refusal after the before email) sends the before mail and the crash mail, which has the reason, the log tail
  and "archive root missing", and a 30-day-old fixture run's transcript is still there.
- **Store (3):** new item has empty `reopenedAt`; Pass then Open records it and a later Fail keeps it; Open on Open is not a re-open.

Fail first:

- Bot: with the three modules as stubs that raise and no installer, **24 run, 22 errors, 2 failures, 0 passed**.
- Store: **3 errors** before the `playtests.py` change.
- After the change, 4 failed on the first real run: `$PSScriptRoot` is empty in a 5.1 parameter default (both scripts),
  and my crash test's fixture had nothing old to archive. Fixed: the default moved into the body, and an old fixture run added.
- The installer's dry run first printed its five lines as one, because the comma binds tighter than `+` in PowerShell.
  I saw it by eye, fixed it, and added a "one call per line" assertion.

Final: **bot 33 OK** (24 new + 9 P91), **shard-migration tools 46 OK** (reopen 3, dashboard, ideas, bug reports),
**Import-PlayTests Pester 20 passed, 0 failed**. The tests leave nothing in `%TEMP%`: the fixture cleanup clears git's
read-only flag. My earlier runs had left 44 `p102-*` folders, now removed.

By hand, read only, on the real setup:

- `python -m uobot.work` against `D:\ShatteredLegacy` and the real play-tests.json: 18 items, all "code changed
  since 36c7ae9" or "since 10f4088"; 166 minutes.
- `Install-OvernightTask.ps1 -DryRun`: user `CHASES-TOWER\ckfle`, 01:30, the five calls.
- `Send-BotReport.ps1 -TextFile ... -WhatIf`: "Would send: Overnight play tests starting: ...".

**Not verified:** a whole real night (build, checks, soak, archive, three real emails). That needs about 2.5 hours and
sends Chase mail. The task's first night does it. The success path after the checks (archive, report with the note,
the summary email, the night line) is the P91 code plus the parts tested above, but has not run end to end.

## The stray run (rule 1 held; this is what I got wrong)

My first fail-first run of the script tests ran against the **pre-P102** `Run-OvernightPlaytests.ps1`. That script had
no `[CmdletBinding()]`, so it accepted the unknown `-PlayTests` and `-MailOutbox` silently. `-RunsRoot` and
`-BotRoot` were real parameters and pointed at a temp fixture. So it started **a real run**: it built
`sl-modernuo:bot` from the working tree, made a scratch world in the temp folder, and started `sl-modernuo-bot` on
127.0.0.1:2595.

- **Rule 1 held:** it ran P91's own guards (compose file check, loopback only, bot project only). `sl-modernuo` and
  `sl-modernuo-test` were not touched by it.
- The test's 300-second timeout killed the PowerShell parent before the checks reached any email: **no mail was sent**
  and no run folder landed in `testing\bot-runs\`. It did rewrite `secrets.local.json` (git-ignored, regenerated every run).
- My attempt to kill it was blocked by the permission classifier. Its python child exited by itself. **The
  container is still up** (127.0.0.1:2595 only) with its world folder deleted under it. It is harmless, and the next
  real run stops it first (`compose down` before the scratch world is made).
- **So this cannot happen again:** the runner now has `[CmdletBinding()]`, so an unknown parameter is an error. And
  both runner tests use a bot root Assert-Rule1 refuses (`...\shard-migration-fixture\bot`), so even a wrong "work
  found" stops before any build or container.

## Deviations and decisions for Chase

1. **A night with work runs all checks**, not only the items with work. P64-2 reads P64-1's runs, and other checks share
   state (`SHARED` in checks.py), so a partial set could give false results. The before email lists the items with
   work and says all N checks run.
2. **`-Only` runs whatever the work check says**: a person typing `-Only` asked for those checks. It skips the work
   check the way `-Force` does.
3. **The no-work line goes to `D:\UO\bot-shard\overnight.log`**, outside both repos, so a quiet night leaves no commit.
   Every night with a run appends one line there too ("ran on ...", or "FAILED on ...").
4. **"Has run" ignores ERROR results** (the check could not be set up). FAIL and FLAKY count as runs: the evidence is
   there, and Chase marks.
5. **Re-opens are detected only from now on.** Before this change re-opening cleared `resultAt` and left no record, so an
   item re-opened before today is not seen as re-opened. It still counts as work if the code changed, which is true of all 18 tonight.
6. **The task runs only while you are logged on** (`-LogonType Interactive`). That way it needs no stored password,
   Docker Desktop is up, and the DPAPI mail credential can be read. If the PC is at the lock screen it still runs; if
   you are signed out, it waits (`StartWhenAvailable`) until you sign in.
7. **Wake from sleep** is `-WakeToRun`; whether Windows honours it is the power plan's "Allow wake timers".
8. **The expected length is rough:** a fixed 25 minutes for the build and boot, plus the soak, plus past check times.
9. **The archive's root is the iCloud sync folder** (`D:\Cloud Drives\iCloudDrive`, which exists). It is never
   created; `Shattered Legacy\bot-runs` under it is. Files may become online-only later; the verify reads them right
   after the copy, while they are local.
10. **Report links to archived transcripts break** in the repo copy of `report.md`. `transcripts-archived.json` in the
    run folder says where they went.

## For Chase

1. **Stop the leftover scratch container** from my stray run (the bot's own project only, never live or test):

       docker compose -p sl-uo-bot down -t 60

   Or leave it; tonight's run stops it first.
2. **Restart the play-test service** so the page writes `reopenedAt` (it imports `tools\playtests.py` at start):

       docker restart sl-play-tests

3. **Register the nightly task, once** (dry run first if you like):

       powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\tools\playtest-bot\Install-OvernightTask.ps1 -DryRun
       powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\tools\playtest-bot\Install-OvernightTask.ps1

   Remove it with `-Uninstall`. For wake from sleep: Power Options > Change plan settings > Advanced > Sleep >
   Allow wake timers = Enable.
4. Tonight should find work (18 items) and email "Overnight play tests starting: 18 checks on <commit>" at about 01:30.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

P102 DONE
