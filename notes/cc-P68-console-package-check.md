# cc-P68: Check package, a cancelled publish, a shorter commit wait with a countdown, and Force

2026-10-05. Builder in `D:\ShatteredLegacy`, scripts only, no Docker build. Brief:
`D:\UO\cc-prompts\cc-P68-console-package-check.md`.

## Headlines

- **First attempt stopped.** The tree held about 60 uncommitted files that were not mine, so I wrote
  `P68 STOPPED`. Chase then committed (`29a8f5a`, 16:23) and said to continue. The tree was clean when I started.
- **Check selected** (`package.check`, Group Player package, Mutates false, RunIn window) runs
  `Build-PlayerPackage.ps1 -CheckZip '<selected zip>'` in a window that stays open. It shows every GATE line and
  ends with `PASSED: ...` or `FAILED: ...`. It works on any zip in `dist\`. With no `version.json`, gate 5 fails
  and says so: `-CheckZip` itself skips gate 5 in that case, so the console adds the failure. It is not refused on
  a dirty tree. It says in one line when the working tree's `Build-PlayerPackage.ps1` differs from HEAD's.
- **Publish exit codes:** 0 means `Published: Publish-PlayerPackage.ps1 exited 0.` 3 means
  **`Publish cancelled. Nothing was published.`** The log line says CANCELLED, the window exits 3, and there is no
  FAILED and no "done". Any other code means `FAILED at step N: Publish failed: ... exited with <code>.`
- **Commit wait:** `CommitQuietSeconds = 60` in `Get-ConsoleConfig` replaces the fixed 5 minutes. The refusal
  quotes the configured window ("60 seconds", or "5 minutes" at 300). The Commit tab has a live line, for example
  `Commit allowed in 0:42 (waiting on design/x.png)`. It names the newest blocking file, ticks every second and
  re-reads both repos every 5 s (`CommitPollSeconds`), so a new change restarts it. Then it shows `Ready to commit`,
  or what still blocks (`Not ready: P65 has not said DONE (...)`, SYSTEM, or both repos clean). It reads nothing
  while another tab is showing.
- **Force box (Chase in chat, 2026-10-05):** it skips **only** the recent-file wait. The not-DONE check, the SYSTEM
  refusal, the clean-tree refusal and the typed phrase all stay. When Force is ticked, the confirmation names
  each file and how long ago it changed. The box applies to one commit: it unticks itself after each Commit and push
  click, and the preview is never forced.
- **Facts: 142, all green** (130 before plus 12 new). Three breaks made on purpose turned the matching three
  facts red (section 3). The file was restored byte-identical.
- **Real check:** `package.check` on the newest zip, `ShatteredLegacy-2026.10.05.1606.zip`, PASSED (section 4).
  Nothing was published or committed, and no tag was moved.

## 1. What changed (file:line)

`git diff --numstat`: `scripts/Shard-Console.ps1` +247 / -37, `scripts/tests/Shard-Console.Tests.ps1`
+253 / -8, `CHANGELOG.md` +3. `Publish-PlayerPackage.ps1` is not edited.

`scripts/Shard-Console.ps1`:

- Header (`:43-56`): the quiet window, the countdown, Force, Check selected.
- `:94` the `-CommitForce` parameter. `:176` `CommitQuietSeconds = 60`, plus `CommitPollSeconds = 5`.
- `Get-ChildArgumentLine`: `-CommitForce` crosses to the child, which rebuilds the plan, so it skips the same
  wait the dialog named.
- `:677` the CHECKING banner. `:725` the action. `New-PlanStep`: a new step kind, `gatecheck`.
- `:784` `Get-CommitInFlight -Seconds` (default 60; the boundary is now exclusive, so at exactly the window the
  file is quiet, which matches the countdown reaching 0:00). Each file row carries `Path`, `LastWriteUtc` and `Ago`.
- `:817` `Format-QuietWindow`, `Format-Countdown` (m:ss, rounded up), `:831` `Get-CommitCountdown`.
- `:857` `Get-CommitPlan -Force`: the confirm text names the files whose wait is skipped, a `FORCE: not waiting
  on ...` say step per file, and the summary refusal when something else still blocks.
- `:1013` the `package.check` plan: refusals (no script, nothing chosen, not in `dist\`), the HEAD-differs note,
  "gate 5 will fail" when there is no `version.json`, then the `gatecheck` step. `:1046` `Get-PublishOutcome`.
  The old "read the script's own last line (it exits 0 when the answer is not yes)" step is gone.
- `:1323` `Test-PlanSafety`: a `gatecheck` runs only the build script, on a `.zip` under `dist\`. `:1397`
  `Format-PlanStep`.
- `:2405` `Get-PackageFacts.BuildDiff`: `git diff --quiet HEAD -- player-package/Build-PlayerPackage.ps1`. A git
  failure is said as such, never treated as "same" (D66).
- `:2691` `Invoke-Plan`: publish exit codes. `:2703` the `gatecheck` executor (a gate that throws is shown in
  red, then PASSED or FAILED as the last line).
- `:3154` `Update-CommitCountdown`. `:3616` the Force box and countdown label. `:3683` the Check selected
  button (between Refresh list and Publish selected). `:3734` the 1 s countdown timer, plus a re-read when the
  tab changes.
- `:3836` the entry exits 3 for a cancelled publish. `-Action list` describes `package.check` and `-CommitForce`.

`scripts/tests/Shard-Console.Tests.ps1`: `New-PackageFacts -BuildDiff`. `Invoke-ClickCapture -CommitForce`
records the confirm text and gives `package.check` a default zip. The form fact expects the third package button,
the Force box and the countdown. P60's five-minute fact now passes `-Seconds 300`. 12 `P68_` facts are at
`:2040-2290`.

`CHANGELOG.md:40`: a `### Staff` line in `## 2026.10.05.3`. **This repeats P60's and P63's deviation.** The
section is today's but already committed (`29a8f5a`). The header's rule would make a `2026.10.05.4` with only
Staff in it, which shows players nothing and would need a VERSION bump, and VERSION is outside my scope. VERSION
is not bumped and the wiki is not published.

## 2. Wording, as shown

- Force confirmation: `This commits and pushes both repos, D:\ShatteredLegacy and D:\UO\shard-migration. FORCE is
  ticked: this skips the wait for files to be unchanged for 60 seconds, for code: CHANGELOG.md (changed 10 s
  ago), docs: notes/cc-P68-console-package-check.md (changed 25 s ago). Something may still be writing them.`
- Force with a prompt still running: `Commit and push stays refused until every prompt above ends DONE or STOPPED.
  Force skips only the wait for recently changed files. Preview commit still runs.`
- Without Force: `code: design/x.png changed 30 s ago, inside the last 60 seconds. ...` and `... no pending file has
  changed for 60 seconds. Preview commit still runs.`
- Countdown while Force is ticked: `Commit allowed in 0:42 (waiting on design/x.png). Force is ticked: Commit and
  push skips this wait`. With a prompt still running: `... . Also blocked: P65 has not said DONE (cc-P65-x.md)`.
- Check HEAD note: `Note: the working tree's player-package\Build-PlayerPackage.ps1 differs from HEAD's (<head>),
  and it is the script doing this check.`

## 3. Tests

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1`:
**142 facts, 142 passed, 0 failed.**

| Fact | Holds |
|---|---|
| P68_TheCheckActionExistsNotMutatingInAWindow | Group, Mutates false, RunIn window, runs with no mode, CHECKING banner, no phrase, one `-NoExit` window with `-PackageZip` |
| P68_TheCheckPlanNamesCheckZipAndTheSelectedZipQuoted | `CHECK & '<build>' -CheckZip '<dist>\...'` for a name containing `'`, `$` and `;`, parsed back to the full path; passes safety |
| P68_TheCheckIsNotRefusedOnADirtyTreeAndSaysWhenTheBuildScriptDiffersFromHead | dirty: no refusal; the differs line; nothing said when it matches HEAD; a git failure is said |
| P68_TheCheckSaysGate5WillFailWithNoVersionJsonAndRefusesWhatItCannotCheck | the gate-5 line in the plan; nothing chosen, not in dist, no script |
| P68_ACheckShowsEachGateLineThenPassedOrFailed | stand-in build script: GATE 4/6/5 lines and PASSED last; no json gives GATE 5 failed and FAILED; a throwing gate shows its own words and FAILED; dist unchanged |
| P68_TheSafetyCheckKeepsTheCheckToTheBuildScriptAndDist | another script, a zip outside dist, a non-zip |
| P68_ThePublishScriptsThreeExitCodesReadAsTheyMean | `Get-PublishOutcome` for 0, 3, 1, 2, 255; the real executor with a stand-in exiting 3 (cancelled, logged CANCELLED, no FAILED), 0 and 1 |
| P68_TheQuietWindowComesFromConfigAndTheRefusalQuotesIt | default 60; 30 s ago is refused at 60 and passes at 20; 300 reads "5 minutes" |
| P68_AFileChanged30sAgoBlocksAt60AndNotAt20 | the guard itself, plus the exact-boundary case |
| P68_TheCountdownTextForAGivenAge | 18 s gives `0:42`, the newest of two files, ticks to 0:41, rounds up to 0:01, then Ready; a 90 s window; clean; Force |
| P68_TheNotDoneBlockStillWinsAtZero | "Also blocked" while counting; `Not ready: P65 ...` at zero, with Force too; SYSTEM |
| P68_ForceSkipsOnlyTheRecentFileWaitAndTheConfirmationNamesTheFiles | 3 refusals without Force, 0 with; the phrase first; the exact confirm text; a not-DONE prompt and SYSTEM still refused; the child line ends `-CommitForce`; the preview is never forced; no phrase runs nothing |

**Each new guard was broken on purpose and the facts caught it.** In one run with three breaks (Force lifting
every block, exit 3 not meaning cancelled, the HEAD-differs line never said), exactly the three matching facts
went red (139/142). The file was restored and its SHA-256 compared equal.

## 4. The real check

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\Shard-Console.ps1 -Action
package.check -PackageZip ShatteredLegacy-2026.10.05.1606.zip` (the newest zip in `dist\`). No `-Mode` was
given, and it ran because it only reads. Exit 0:

```
==============================================================================
  CHECKING  package.check (player package)
  Build-PlayerPackage.ps1 -CheckZip: it reads the zip and changes nothing.
==============================================================================
== PLAN: package.check (package) ==================================================
  1. CHECK    & 'D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1' -CheckZip 'D:\ShatteredLegacy\player-package\dist\ShatteredLegacy-2026.10.05.1606.zip'
         # Build-PlayerPackage.ps1 -CheckZip on ShatteredLegacy-2026.10.05.1606.zip: gates 4 and 6 on the zip, and 5 on its version.json. It reads the zip and changes nothing.

[1/1] Build-PlayerPackage.ps1 -CheckZip on ShatteredLegacy-2026.10.05.1606.zip: gates 4 and 6 on the zip, and 5 on its version.json. It reads the zip and changes nothing.
      > & 'D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1' -CheckZip 'D:\ShatteredLegacy\player-package\dist\ShatteredLegacy-2026.10.05.1606.zip'
  GATE 4 passed: D:\ShatteredLegacy\player-package\dist\ShatteredLegacy-2026.10.05.1606.zip
  gate 6: 123 native files checked, 172 skipped (IL-only .NET, non-Windows, excepted)
  GATE 6 passed: D:\ShatteredLegacy\player-package\dist\ShatteredLegacy-2026.10.05.1606.zip
  GATE 5 passed: D:\ShatteredLegacy\player-package\dist\ShatteredLegacy-2026.10.05.1606.version.json
PASSED: ShatteredLegacy-2026.10.05.1606.zip passed gates 4, 6 and 5.
package.check: done.
```

The build script matched HEAD, so there was no differs line. I also ran it on the oldest zip,
`ShatteredLegacy-2026-09-26.zip` (it has no version.json). It exited 1: gate 4's own list (no
`app/package-version.txt`, no `app/Update.ps1`, and others), then `GATE 5 failed: there is no
ShatteredLegacy-2026-09-26.version.json beside the zip, so launchers could not be told about it.`, then `FAILED:
ShatteredLegacy-2026-09-26.zip did not pass the package gates (2 problem(s) above).`

## 5. Unverified

- The Force box, the countdown and the Check button were built in the form fact and driven through
  `Invoke-ConsoleButton` with stubs. Nobody has clicked them by hand or watched the countdown tick live.
- A real child exiting 3 was not run: there is no stand-in publish path through a child. The executor half is a
  fact (`PlanCancelled`), and the `exit 3` line in the entry is two lines read by eye.
- **Not mine, seen while working:** `design/kitsune-ears-tail/build_stage4_walk_remaining.py` and
  `design/kitsune-ears-tail/stage4/` appeared untracked during this session. I left them alone. A commit now
  would include them.

## For Chase

1. Open the console and go to **Commit**. Under the buttons a line counts down (`Commit allowed in 0:42 (waiting
   on ...)`) and then reads `Ready to commit`. Tick **Force** while it is counting and click **Commit and push**:
   the dialog names the files whose wait it skips and still wants `commit shard work`.
2. Go to **Player package**, select any zip and click **Check selected**. A window shows the GATE lines and ends
   with PASSED or FAILED. Pick `ShatteredLegacy-2026-09-26.zip` to see a FAILED.

P68 DONE
