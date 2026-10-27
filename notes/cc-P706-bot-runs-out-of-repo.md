# cc-P706: overnight play-test transcripts no longer block docs commits

Iron Golem, 2026-10-27. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P706`. Two live Golem scripts were changed in place, with backups (see below).

## In plain words

- **The overnight bot's transcripts stay off GitHub.** A night's transcripts are 10 to 21 MB of text. The docs repo
  now ignores them; they stay on the game PC in the run folder until the 14-day archive moves them to iCloud, as
  before. Only the small summary is committed: report.md, results.json, email.txt and the like, about 170 KB a night.
- **A big leftover file in a bot run folder no longer stops merges.** Commit-ShardWork leaves it out of the commit
  with a yellow line naming it, and commits everything else. On 10-27 one 8.5 MB transcript blocked every docs merge
  (P663, P701).
- **When a commit is refused, the reason now names the file.** The Golem card, the fix-up prompt and the email say,
  for example, "BLOCKED docs: size notes/big.bin (20.0 MB, over the 5 MB cap)" instead of a bare "exit 2".
- Nothing for you to do. The overseer can move `D:\UO\overseer\bot-runs-holding\2026-10-27-0130\` back into
  `testing\bot-runs\` once this is on main: its transcripts will be ignored and the rest will commit.

## What changed

| Where | What |
|---|---|
| docs `.gitignore` | `testing/bot-runs/*/transcripts/`, beside the existing `*.log` rule. Tracked transcripts from older nights stay tracked; when `uobot/archive.py` removes them after 14 days, the deletion commits as before. |
| `D:\UO\Commit-ShardWork.ps1` (live; backup `.bak-20261027-P706`) | `Test-Safe` sorts its findings into refusals and left-out files. A file over the cap (`-MaxFileMB`, 5) under `testing/bot-runs/` is **left out**. It is named in a yellow "left out of this commit" line, unstaged after `git add -A` with `git reset -q -- <path>`, and kept on disk. Every other file over the cap, and every blocked pattern, still refuses the repo. If the left-out files were all that was pending, it says "nothing else to commit" and makes no empty commit. A refusal now ends with one `BLOCKED <repo>: <what>` line per path, after the "One or more repos were refused" line. A size line gives the size and the cap. The branch and git-status refusals print the same line. Exit codes are unchanged (2 refused, 1 git failed). |
| `D:\UO\golem\Golems.ps1` (live; backup `.bak-20261027-P706`) | New `Get-CommitRefusal`: the first three `BLOCKED` lines of Commit-ShardWork's output. The integrator appends them to its reason, "the commit after the merge failed (Commit-ShardWork.ps1 exit 2): BLOCKED docs: ...". That reason goes into the fix-up prompt, the email and the handled-marker. |
| code `tools/playtest-bot/Run-OvernightPlaytests.ps1` | Header only: the transcripts are git-ignored, and Commit-ShardWork leaves oversized files under bot-runs out of a commit. The run itself needed no change. It writes into the same folder, and the ignore rule keeps the transcripts out. |
| `D:\UO\golem\tests\CommitShardWork.Tests.ps1` (new) | The facts below. Each one builds throwaway repos under `%TEMP%` and passes `-NoArchive`, so the real prompt queue is never touched. |

golem.ps1's own commit-retry path needed nothing. It already picks the indented `size ...` lines out of the output,
and those lines now also carry the cap.

## Proof

`D:\UO\golem\tests\CommitShardWork.Tests.ps1`, 5 facts. Each fact runs a real Commit-ShardWork `-Merge` on a merge
left half done, as the integrator leaves it:

| Fact | Red | Green |
|---|---|---|
| `P706_A20MbStrayInTheBotRunFolderIsLeftOutAndTheMergeCommitsAndPushes`: 20 MB `testing/bot-runs/.../transcripts/soak.txt`, untracked and not ignored (the backstop). Both merges commit and push, `report.md` goes in, the transcript stays on disk, whole and untracked. | current script: exit 2 (`red-tests-on-current-csw.txt`) | yes |
| `P706_A20MbStrayElsewhereIsRefusedAndTheLastLineNamesItsPathSizeAndTheCap`: 20 MB `notes/big.bin` gets exit 2, nothing committed, last line `BLOCKED docs: size notes/big.bin (20.0 MB, over the 5 MB cap, -MaxFileMB)`, and the integrator's `Get-CommitRefusal` returns that line | current script: the last line was "One or more repos were refused."; current Golems.ps1: no `Get-CommitRefusal` (`red-integrator-reason-current-golems.txt`) | yes |
| `P706_ABlockedPatternIsNamedInTheSummaryToo` (`dist/pkg.txt`) | current script: no BLOCKED line | yes |
| `P706_OnlyAnOversizedBotFilePendingIsNothingToCommit` | current script: exit 2 | yes |
| `P706_TheDocsRepoIgnoresRunTranscriptsSoTheyAreNotEvenPending`: with the docs `.gitignore`, a 20 MB transcript is not even pending, and `results.json` commits | HEAD's `.gitignore` (`red-ignore-fact-head-gitignore.txt`) | yes |

Green on the scratch copies (`green-tests-new-csw.txt`), then again on the installed scripts (`green-installed.txt`).

**The held 10-27 run under the new rule:** its `transcripts\` is 20 MB and `run.log` 0.7 MB, both ignored. That
leaves 172,873 bytes to commit, the largest file `results.json` at 118 KB.

**The other Golem tests on the installed scripts:**
- `Lane.Tests.ps1`: 65 of 65 (`lane-tests.txt`).
- `Golem.Tests.ps1`: 1,603 checks passed and 5 failed (`golem-tests-full.txt`). All 5 are in two facts,
  `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged` and
  `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly`. Both failed before this change too (Iron claims P102
  "areas server, docs-only"), as recorded in P156's, P159's and later notes. They test claiming, not committing, and
  are not this task's.
- Golem.Tests' pin that Commit-ShardWork stages with `git add -A` still holds.

## Commit preflight

- Code copy: `tools/playtest-bot/Run-OvernightPlaytests.ps1` (header lines only).
- Docs copy: `.gitignore`, this file, `notes\cc-P706-tools\` (71 KB: the edit, install and test scripts, a copy of the
  test file, and the red and green logs).
- Outside both repos, installed live, with MD5 checked before and after (`install.txt`):
  - `D:\UO\Commit-ShardWork.ps1`: E1E10820... became 7871B784...; backup `D:\UO\Commit-ShardWork.ps1.bak-20261027-P706`.
  - `D:\UO\golem\Golems.ps1`: D65FC54A... became 9CCC2756...; backup `D:\UO\golem\Golems.ps1.bak-20261027-P706`.
  - New `D:\UO\golem\tests\CommitShardWork.Tests.ps1`.
- To undo, copy each backup over its live file.
- `Commit-ShardWork.ps1 -DryRun -Branch golem/Iron/P706` on both copies: "dry run" for code and docs. All edited files
  are ASCII. No locks were needed: no Docker, no shard, no package, no Haven. Nothing committed.

P706 DONE
