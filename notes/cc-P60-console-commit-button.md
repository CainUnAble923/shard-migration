# cc-P60: Commit shard work from the Shard Console

2026-10-05. Builder in `D:\ShatteredLegacy`, scripts only, no Docker build. Brief:
`D:\UO\cc-prompts\cc-P60-console-commit-button.md`, with one change from Chase: **Part B item 2 BLOCKS
`commit.run`, it does not just warn.** Each prompt and file is named, the preview still runs and shows them,
and there is no override button.

## Headlines

- The Shard Console has a **Commit** tab: **Preview commit** (`commit.preview`) and **Commit and push**
  (`commit.run`), plus a message box. Both run `D:\UO\Commit-ShardWork.ps1` as it is, in a window of their
  own that stays open (`-NoExit`), so its own table and OK/BLOCKED/FAILED lines are read there.
  Nothing of the script is reimplemented, and the script was not edited.
- `commit.run` asks for the typed phrase **`commit shard work`**, with "Both repos are PUBLIC on GitHub" said
  above it. It follows the console's mode and D37 rules: refused with no `-Mode`, printed under
  `-Mode DryRun` with `-Message` quoted.
- `commit.run` is **refused, with no override**, when the console runs as SYSTEM, when both repos are clean,
  when a CC notes file numbered P54 or above does not end `P<nn> DONE` or `P<nn> STOPPED: ...`, or when a
  file git would commit changed in the last 5 minutes. Every prompt and file is named. The preview is never
  refused for these: it names them as WARNING lines and runs.
- A commit message with quotes, `$`, `;`, `&`, `%` and `-NoPush` in it reaches the script unchanged. It
  crosses the child command line as base64 and reaches the script as a named parameter, in-process, so no
  quoting layer sees it.
- **Facts: 112, all green** (95 before plus 17 new). Each new gate was broken on purpose and went red, and
  the file was restored byte-identical (SHA-256 checked).
- **One real `commit.preview` ran** (the script's `-DryRun`), output below. Nothing was committed or pushed:
  both HEADs are unchanged (`2663209` code, `4d389b3` docs), no prompt was moved, and `shard-console.log`
  has no `commit.run` line.
- **Two deviations from the brief, both argued below:** the DONE check reads notes from P54 up only (all 46
  older notes would block every commit forever), and the "recently changed" check reads only files git would
  commit (the live save and status.json are rewritten every 30 s to 5 min and are gitignored).
- **Not mine, found in the working trees:** something else was writing in `D:\ShatteredLegacy` while I worked
  (`design/kitsune-ears-tail/`, 128 files: 127 new and 1 modified, all after my start check showed both
  repos clean), and `docs/client-test-queue.md` and `docs/feature-queue.md` are modified in the docs
  repo. I did not touch any of them. The new guard caught the first one on its own (section 5).
- **A near miss in my own gate-proving, fixed:** see section 4.

## 1. What changed

All in `D:\ShatteredLegacy`, uncommitted.

`scripts/Shard-Console.ps1` (+372 / -27, `git diff --numstat`):

- `:43` header: the commit script added to "IT CALLS THE EXISTING SCRIPTS".
- `:80-81` two parameters, `-CommitMessage` (for a person) and `-CommitMessageB64` (what a click passes).
- `:98` `$script:CommitPublicWarning`, the line said above the phrase.
- `:146-156` `Get-ConsoleConfig`: `CommitScript` (`D:\UO\Commit-ShardWork.ps1`), `CommitRepos` (the same two
  paths the script hard-codes in `$Repos`; change both together), `NotesFolder`, `NotesDoneFrom = 54`,
  `CommitQuietMinutes = 5`.
- `:519` `Get-ConfirmPhrase`: `commit.run` -> `commit shard work`.
- `:531` `Get-ConfirmPreface`: a plan that runs the commit script without `-DryRun` gets "BEFORE YOU TYPE:"
  plus the public warning, the way a stop gets D36's.
- `:555`, `:566` `Get-ChildArgumentLine`: `-Shard` only for test or live (the commit buttons name both repos),
  and the message as `-CommitMessageB64 <base64 of UTF-8>`.
- `:587-605` `Get-ModeBanner`: `commit.* (both repos)`; a PREVIEW banner for `commit.preview` run for real,
  so the preview's window does not say RUNNING FOR REAL; `commit.run` says it commits and pushes, and why
  that is final.
- `:638-639` `Get-ConsoleActions`: the two actions, Group `Commit`, Mutates false/true, RunIn window/window.
- `:650` `New-PlanStep`: a new step kind, `script`, with `Named` parameters.
- `:664-696` `ConvertTo-PsLiteral` (single-quoted, curly quotes doubled too), `Format-ScriptCall` (the line a
  plan prints, which pastes into PowerShell and does the same), `ConvertFrom-GitPorcelain` (read the way the
  commit script reads it).
- `:698` **`Get-CommitInFlight`**, the Part B item 2 check: two listings in (notes name + last non-empty line;
  pending files repo + path + LastWriteUtc), findings out. No file system.
- `:730` **`Get-CommitPlan`**: both buttons' plans, from facts only. Missing script -> refused for both.
  SYSTEM, in-flight -> refuse in `commit.run`, WARNING in the preview. Both repos clean -> refused in
  `commit.run` (so no phrase is asked for), said in the preview. A repo whose git status failed is a WARNING
  and is never counted as clean (D66).
- `:798` `Get-ActionPlan` hands `commit.*` to `Get-CommitPlan` before it touches any docker state.
- `:985` `Test-PlanSafety`: the only script run in-process is `CommitScript`, and never without `-DryRun`
  unless the plan has a typed confirmation.
- `:1031` `Format-PlanStep` prints a `script` step.
- `:1907` `Invoke-ToolRead`: `Invoke-DockerRead`'s body with the tool as a parameter; `Invoke-DockerRead`
  calls it with `docker`, unchanged otherwise.
- `:1929` **`Get-CommitFacts`** (shell, read-only): who is running (`WindowsIdentity.IsSystem`), each repo's
  `git -C <repo> --no-optional-locks status --porcelain --untracked-files=all` and each pending file's
  LastWriteTimeUtc, and the last non-empty line of every `notes\cc-P*.md`.
- `:2127` **`Invoke-ScriptStep`**: runs the script in this process with its parameters splatted by name. What
  it prints goes to the screen and to `scripts\shard-console-output\<time>_<action>_repos.log` (D38), its
  Write-Host colours kept, its `Format-Table` rendered whole. The result is its exit code.
- `:2188` `Invoke-Plan`: the refusal for a missing phrase no longer says "this is a live action".
  `:2218` runs a `script` step.
- `:2497` `Show-TypedConfirm` takes the dialog's subject; the commit dialog is "Commit and push: type to
  confirm".
- `:2580-2600` `Invoke-ConsoleButton`: `-CommitMessage`; a commit click reads `Get-CommitFacts`, never docker.
- `:2949-2985` the Commit tab: caption, message box, the two buttons. If the script is missing the caption
  says "NOT FOUND" and the buttons say so when clicked.
- `:3046`, `:3067-3086` entry: `-Action list` mentions the commit options; a headless `commit.*` decodes the
  message and reads `Get-CommitFacts` instead of docker.

`scripts/tests/Shard-Console.Tests.ps1` (+281 / -7): `New-CommitFacts` (`:79`), `Get-Plan` takes commit facts,
the form fact expects the Commit tab and its buttons (`:932`), `Invoke-ClickCapture` stubs `Get-CommitFacts`
and records phrase dialogs (`:976`), the window cases include both commit actions, and 17 `P60_` facts
(`:1371-1600`).

`CHANGELOG.md:63`, under the existing `## 2026.10.05` / `### Staff`: "Shard Console: a Commit tab previews the
shard's uncommitted work and commits and pushes it, after a typed confirmation." **VERSION not bumped, and
added to a committed section, against the brief's letter.** The 2026.10.05 section is committed (P58,
`2663209`), so the header's rule would make this `2026.10.05.2`. But `### Staff` is ignored by the parser
(`server/customizations/ShardVersion.cs:111-117` reads only Added/Changed/Fixed), so that version would be
empty, and an empty newest version shows no login bulletin (`ShardVersion.cs:292`, `:324`): every account that
has not yet seen 2026.10.05's notes would never be shown them. A staff line changes nothing a server reads, so
it went into the existing section. Wiki not published.

`D:\UO\Commit-ShardWork.ps1`: not edited. Suggestions in section 7.

## 2. The confirmation, exactly as shown

Rendered from the code (`Get-ConfirmPreface`, the confirm step, `Format-Plan`, as `Show-TypedConfirm` joins
them) on a sample with 3 code files, 1 docs file, nothing in flight and the message
`P60 console commit button`:

```
window title: Commit and push: type to confirm
BEFORE YOU TYPE: Both repos are PUBLIC on GitHub: a commit that is pushed cannot be taken back.

This commits and pushes both repos, D:\ShatteredLegacy and D:\UO\shard-migration.

This will run:
  1. CONFIRM  typed: you must type exactly 'commit shard work'. This commits and pushes both repos, D:\ShatteredLegacy and D:\UO\shard-migration.
  2. SAY      code (D:\ShatteredLegacy): 3 file(s) to commit.
  3. SAY      docs (D:\UO\shard-migration): 1 file(s) to commit.
  4. SAY      Commit message: P60 console commit button
  5. RUN      & 'D:\UO\Commit-ShardWork.ps1' -Message 'P60 console commit button'
         # Commit-ShardWork.ps1: add, commit and push both repos. Its own table at the end says pushed, clean, BLOCKED or FAILED for each.
  6. LOG      one timestamped line: commit.run
label: Type exactly:  commit shard work
```

With the DRY RUN box ticked the title is "DRY RUN - Commit and push: type to confirm (the window it opens only
prints)", as for the live buttons. The window it opens says, before anything else:

```
==============================================================================
  RUNNING FOR REAL  commit.run (both repos)
  This commits and pushes both repos. Both repos are PUBLIC on GitHub: a commit that is pushed cannot be taken back.
==============================================================================
```

The blockers never reach this dialog: a refused plan stops before the phrase is asked for, which is what "no
override" means here.

## 3. The guard wording

Each line goes to the Output box as `commit.run: <text>` and is a REFUSE step in the plan. In the preview the
same text is a `SAY WARNING: <text>` step and the preview runs.

- Wrong user: `This console is running as NT AUTHORITY\SYSTEM. Git refuses both repos for that account
  (dubious ownership) and it has no push credential. Run the console from your own Windows login.`
- A prompt still running: `P57 has not said DONE: cc-P57-batch-6.md ends "- still writing section 4".
  Committing now may publish half its work.` (the last line is cut at 70 characters; an empty file says
  "(the file is empty)").
- A file still changing: `code: CHANGELOG.md changed 10 s ago, inside the last 5 minutes. Something may still
  be writing it.`
- After any of those two: `Commit and push stays refused until every prompt above ends DONE or STOPPED and no
  pending file has changed for 5 minutes. Preview commit still runs.`
- Nothing to commit: `Nothing to commit: both repos are clean.`
- Script missing (both buttons): `D:\UO\Commit-ShardWork.ps1 is not there, so there is nothing to run. Its
  path is CommitScript in Get-ConsoleConfig.`
- git failed (a warning, not a block; the script itself then says FAILED there, D66): `WARNING: git status
  failed in code (D:\ShatteredLegacy): <git's first line>. Commit-ShardWork.ps1 will say FAILED there and
  commit nothing in it.`

**What counts as finished.** The last non-empty line, trimmed, must match `^P<nn> (DONE|STOPPED: .+)$`
case-sensitively, where `<nn>` is the number in the file name. `P57 done`, `P57 DONE.`, `**P57 DONE**`,
`P56 DONE` in P57's note and a bare `P57 STOPPED:` all count as not finished (fact
`P60_TheGuardPassesANoteEndingDoneOrStopped`).

**Deviation 1: only notes numbered 54 and up.** The brief says "any" `cc-P<nn>-*.md`. Counted on
2026-10-05: 53 notes match; the 46 numbered P4 to P53 all predate the finishing rule and **none of the 46**
ends in DONE or STOPPED; P54 to P59 all do. Read literally the check would refuse every commit forever, and
since it blocks with no override that would make the button dead. `NotesDoneFrom = 54` in the config is the
floor; it is a number, not a guess, and it is printed nowhere as a rule a note must follow.

**Deviation 2: "changed in the last 5 minutes" reads only the files git would commit** (the same
`--untracked-files=all` list the script reads), not every file in the working tree. The tree holds the live
and test saves, `status.json` (rewritten every 30 s) and logs, all gitignored. Counting them would refuse
every commit while a shard runs, and they cannot publish half of anything because they are never committed.
Deleted files have no time and are skipped.

## 4. Tests

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1`:
**112 facts, 112 passed, 0 failed** (95 before this task, all still green). The 17 new ones:

| Fact | What it holds |
|---|---|
| P60_TheTwoCommitActionsExistWithTheirGroupMutatesAndRunIn | Group Commit; preview Mutates false, run true; both RunIn window; the phrase |
| P60_WithNoModeCommitRunIsRefusedAndThePreviewRuns | D37: `Resolve-RunMode` refuses commit.run with no mode; any dry wins; the REFUSED banner |
| P60_TheRealChildGivenNoModeRefusesCommitRun | a real `powershell.exe` on the click's line minus the mode: exit 2, REFUSED, nothing past the banner |
| P60_TheDryRunPlanPrintsTheCommandLineWithTheMessageQuoted | the printed line, and PowerShell's own parser reads the message back from it unchanged |
| P60_AMessageCrossesTheChildCommandLineUnchanged | the click's real line run by a real dry child prints the exact `-Message '...'`; no docker call |
| P60_AMessageReachesTheScriptUnchanged | a stand-in commit script receives every character; `-NoPush` inside the message stays text; the preview passes `-DryRun`; blank passes no `-Message` |
| P60_TheCommitRunsOnlyWithThePhraseAndItsFailureIsAFailure | 5 wrong phrases run nothing; the script exiting 2 is a failure here, and the output file says so |
| P60_TheGuardFlagsANoteThatHasNotSaidDone | the exact wording; an empty note |
| P60_TheGuardPassesANoteEndingDoneOrStopped | `P57 DONE`, `P57 STOPPED: x` pass; six near misses do not; pre-P54 and non-prompt notes are not read |
| P60_TheGuardFlagsAFileChangedInTheLastFiveMinutes | 90 s flagged with its wording, 5 min 1 s not |
| P60_ANoteWithoutDoneBlocksCommitRunAndThePreviewNamesItAndRuns | refused, names the note and the file, no window, no phrase dialog; the preview warns and opens its window |
| P60_SystemRefusesCommitRunAndThePreviewSaysSo | one refusal with the wording; no window; the preview says the same and is not refused |
| P60_BothReposCleanSaysSoInsteadOfAskingForThePhrase | no phrase dialog, no window, the line; a git failure is not "clean" |
| P60_AMissingScriptMakesBothButtonsSaySoAndDoNothing | both buttons, no dialog, no window |
| P60_ACleanCommitAsksForThePhraseSaysPublicFirstAndOpensItsWindow | the phrase, `-NoExit`, `-Mode Execute ... -ConfirmLive "commit shard work"`, the preface; the preview asks nothing |
| P60_TheSafetyCheckRefusesARealCommitWithoutThePhraseOrAnotherScript | `Test-PlanSafety`'s new rule both ways |
| P60_PorcelainPathsAreReadAsTheCommitScriptReadsThem | modified, untracked with a space, renamed, quoted |

The existing D37 facts now also cover both commit actions (every window action, dry, real and toggled), and
`TheFormBuildsFromACaptureWithoutBeingShown` checks the Commit tab sits between Diagnostics and LIVE shard.

**Each gate watched failing.** Five breaks in one run, then the file restored and its SHA-256 compared:
the DONE regex made to pass everything, `commit.run` set to Mutates false, the message put raw on the child
line, the SYSTEM check skipped, the new `Test-PlanSafety` rule skipped. 9 facts went red, every break caught
by the facts meant for it. A second run broke Mutates and "any dry wins" together: 7 red, including both real-
child commit facts.

**The near miss.** In the first break run, with `commit.run` set to Mutates false, the fact that runs a real
child on the no-mode line ran `commit.run` **for real**: that line still carried `-ConfirmLive "commit shard
work"`, and there is no recorder for git as there is for docker. It was stopped only because this session's
own files were less than 5 minutes old, so the in-flight guard refused (exit 1). Checked straight after: both
HEADs unchanged, no `commit.run` in `shard-console.log`, no new output file. The two real-child facts now take
the phrase off the line first (`Remove-Phrase`), so a broken mode check makes `Invoke-Plan` refuse before any
step, whatever the guards say. Re-broken after the fix: both facts red, nothing ran. Any future fact that
starts a real child for `commit.run` must do the same.

## 5. The real preview

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\Shard-Console.ps1 -Mode Execute -Action
commit.preview -CommitMessage 'P60 preview check'`, which is the line the Preview button's window runs. Exit 0.
It ran while this note was a draft, so P60 itself is correctly listed as not DONE. Output, with the script's
40-line file list as it printed it:

```
==============================================================================
  PREVIEW  commit.preview (both repos)
  Commit-ShardWork.ps1 -DryRun: it lists what would be committed and changes nothing.
==============================================================================
== PLAN: commit.preview (repos) ===================================================
  1. SAY      code (D:\ShatteredLegacy): 131 file(s) to commit.
  2. SAY      docs (D:\UO\shard-migration): 3 file(s) to commit.
  3. SAY      WARNING: P60 has not said DONE: cc-P60-console-commit-button.md ends "Draft while the work is in progress.". Committing now may publish half its work.
  4. SAY      WARNING: code: CHANGELOG.md changed 56 s ago, inside the last 5 minutes. Something may still be writing it.
  5. SAY      WARNING: code: design/kitsune-ears-tail/prompt-design-chat.md changed 278 s ago, inside the last 5 minutes. Something may still be writing it.
  6. SAY      WARNING: code: scripts/Shard-Console.ps1 changed 11 s ago, inside the last 5 minutes. Something may still be writing it.
  7. SAY      WARNING: code: scripts/tests/Shard-Console.Tests.ps1 changed 201 s ago, inside the last 5 minutes. Something may still be writing it.
  8. SAY      WARNING: docs: notes/cc-P60-console-commit-button.md changed 7 s ago, inside the last 5 minutes. Something may still be writing it.
  9. RUN      & 'D:\UO\Commit-ShardWork.ps1' -DryRun -Message 'P60 preview check'
         # Commit-ShardWork.ps1 -DryRun: lists what would be committed in each repo and changes nothing.

[1/9] code (D:\ShatteredLegacy): 131 file(s) to commit.
[2/9] docs (D:\UO\shard-migration): 3 file(s) to commit.
[3/9] WARNING: P60 has not said DONE: ...  (steps 3 to 8 repeated as they run)
[9/9] Commit-ShardWork.ps1 -DryRun: lists what would be committed in each repo and changes nothing.
      > & 'D:\UO\Commit-ShardWork.ps1' -DryRun -Message 'P60 preview check'

=== code  (D:\ShatteredLegacy) ===
  131 file(s) pending:
    CHANGELOG.md
    design/kitsune-ears-tail/prompt-design-chat.md
    scripts/Shard-Console.ps1
    scripts/tests/Shard-Console.Tests.ps1
    design/kitsune-ears-tail/build_stage1.py
    design/kitsune-ears-tail/build_stage2.py
    design/kitsune-ears-tail/icon_44.png
    design/kitsune-ears-tail/icon_44_gray.png
    design/kitsune-ears-tail/icon_44_partialhue.png
    design/kitsune-ears-tail/icon_44_preview_4x.png
    design/kitsune-ears-tail/reference/8x/body-frames/run_dir0_f00_8x.png
    ... (run_dir0 to run_dir2 frames, 30 lines)
    ... and 91 more
  dry run: would add, commit and push

=== docs  (D:\UO\shard-migration) ===
  3 file(s) pending:
    docs/client-test-queue.md
    docs/feature-queue.md
    notes/cc-P60-console-commit-button.md
  dry run: would add, commit and push


Repo Result
---- ------
code dry run
docs dry run



=== prompts with a finished note ===
  archived: cc-P60-console-commit-button.md  (dry run, not moved)
commit.preview: done.
```

Kept in full in `D:\ShatteredLegacy\scripts\shard-console-output\20261005-093839_commit.preview_repos.log`
(gitignored). Afterwards: both HEADs unchanged, `D:\UO\cc-prompts\cc-P60-console-commit-button.md` still in
place.

**What it shows beyond the wiring.** Of the 131 code files, 3 are mine (`CHANGELOG.md` and the two scripts).
The other 128 are `design/kitsune-ears-tail/` (one modified, 127 untracked), written by something else in the
minutes I was working; they were not there at the start check. In the docs repo `docs/client-test-queue.md`
and `docs/feature-queue.md` are modified and are not mine. A commit right now would publish all of that with
this task; the new button would refuse it for the files still being written, which is the case it is for.

## 6. Unverified

- The tab and the dialogs were built in a test and driven through `Invoke-ConsoleButton` with the dialogs
  answered by stubs, never clicked by hand. The form fact builds the real tab without showing it.
- SYSTEM is judged by `WindowsIdentity.IsSystem`, tested with facts, not by running the console as SYSTEM.
- `commit.run` for real was never run, by the brief. The only proof it reaches the real script is the
  stand-in fact (same code path, a different script path) and the dry child.
- The output-box colours for the script's Write-Host lines are mapped from its ForegroundColor; seen on the
  headless run above (no colour in a text capture), not in the form.

## 7. What Commit-ShardWork.ps1 should change (described, not done)

1. **It archives a prompt whose task has not finished.** It moves `cc-prompts\<name>.md` to `completed\`
   whenever a note of the same name exists. The preview above would have archived P60 while its note was a
   draft. The script's own comment predicts this ("If a future task ever writes its note first and keeps
   working, this would archive a prompt mid-run"). Every prompt now writes its note as it goes. Suggest:
   archive only when the note's last non-empty line is `P<nn> DONE` or `P<nn> STOPPED: ...`, the same test
   as `Get-CommitInFlight`.
2. **A failed add, commit or push does not change its exit code.** Only a BLOCKED or FAILED repo exits 2. A
   failed push leaves "push failed" in the table and then reaches the end; the console only sees a non-zero
   code because the failed `git push` happens to be the last native command. Suggest `exit 1` when any row is
   `add failed`, `commit failed` or `push failed`.
3. Its two repo paths are hard-coded in `$Repos`, and the console's `CommitRepos` repeats them. If either
   moves, change both, or give the script a `-ListRepos` switch the console can read.

## For Chase

1. Commit P60 first the usual way; the button's guard will itself refuse while this session's files are
   less than 5 minutes old. Look at the 128 `design/kitsune-ears-tail/` files and the two `docs/*.md` files
   before that commit: they are not from this task.
2. Open the console: `.\scripts\Shard-Console.ps1`. A **Commit** tab sits between Diagnostics and LIVE shard.
3. With work pending, click **Preview commit**. A window opens with PREVIEW at the top, lists any WARNING
   lines, then the script's own `-DryRun` output, and stays open.
4. Type a message with a quote in it (`it's "a test"`), tick **DRY RUN**, click **Commit and push**. The dialog
   is titled "DRY RUN - Commit and push" with "BEFORE YOU TYPE" first; type `commit shard work`. The window
   says DRY RUN and prints `-Message 'it''s "a test"'`. Nothing runs.
5. Untick DRY RUN. With a CC prompt mid-run (or within 5 minutes of saving any file), **Commit and push**
   lists each prompt and file in the Output box and asks for nothing.
6. When everything has said DONE and nothing has changed for 5 minutes, **Commit and push**, type the phrase,
   and read the script's table in its window: `pushed` for each repo, or BLOCKED / FAILED and why.
7. From a SYSTEM remote shell (`-Action commit.run -Mode Execute`) it should refuse with the SYSTEM line.

P60 DONE
