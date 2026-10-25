# cc-P597: fix-up for P479 (the Tinker's Docker prune): its branch did not merge into main

## In plain words

- Nothing needed fixing: P479's work (the Tinker cleaning up old Docker images, the time limit on its remote calls,
  fewer emails) is already in main in both repos. A later merge pass got it in after the first one was refused.
- Why the first merge was refused: the overnight bot's soak transcript for 2026-10-25 was still growing while
  Golems committed it (0, then 2.4, then 3.9 MB), and by 05:40 it was 8.5 MB, over the 5 MB rule for these public repos.
- P479's own tests pass again on today's main. Thirteen older web-console checks fail, but they failed the same way
  before P479, so they are not from this work.
- For you: nothing to deploy. If you see the same "REFUSING to commit ... soak.txt" again, the soak transcript needs a
  size cap or an ignore rule (a small follow-up; see Decisions).

## Status

Done. The Iron Golem (Opus), branch `golem/Iron/P597` of both repos, not committed (the Golem commits). No Docker
build: nothing under `server\` or `docker\uo\` changed. No shard, package or Haven touched.

## 1. The merge

`git fetch origin`, then compared. Both work copies are level with `origin/main` and already contain P479:

| Repo | HEAD = main = origin/main | P479's commit | P479's merge into main |
|---|---|---|---|
| ShatteredLegacy | `8b0ccb8` | `1036325` | `8b0ccb8` (pushed by the failed run itself: the code side went through) |
| shard-migration | `995251a` | `f359608` (the note) | `3346006` (a later integrator pass) |

So merging main into P479's work gives main itself: **no conflicts, nothing to resolve**, no CHANGELOG or VERSION
change (P479 touched neither). I did not check out `golem/Iron/P479` (the hand-off forbids switching branches);
`golem/Iron/P597` is main, which holds it.

**The refusal itself:** `Commit-ShardWork.ps1` refused the docs repo for `testing/bot-runs/2026-10-25-0130/transcripts/
soak.txt` (8.5 MB). Its history in main: added empty at 04:01 (P590's merge), 2,393,743 bytes at 04:21 (P591),
3,926,633 at 04:41 (P592). The 01:30 soak was still writing it while three merges committed it, and at 05:40 the main
checkout's copy had grown past 5 MB. Main's tracked copy is the 3.9 MB one, under the limit, so nothing is pending here.

## 2. Tests

| File | Result |
|---|---|
| `scripts\tests\Shard-Console.Tests.ps1` (code copy) | 452 facts, 439 passed, 13 failed. P479's `P479_TheSettingsShowMailModeAndAnUnknownValueIsAll` passes |
| The same file at `db4c85b` (main just before P479, a scratch worktree, removed after) | 451 facts, 438 passed, **the same 13 failed** |
| `D:\UO\golem\tests\Tinker.Tests.ps1` | **199 checks passed, 0 failed** (9 `P479_` facts) |
| `D:\UO\golem\tests\Golem.Tests.ps1` | 1,603 checks passed, 5 failed: all 5 in the two P184 facts, the same as P479 recorded against the original golem.ps1. Both `P479_` facts pass |

The 13 Shard-Console failures predate P479 and are not in its scope: P83, P101, P107 and P135 facts (play-test
tile and links, website and art buttons) and three window-action facts, plus `PlayerCommandsNeverAppearInTheWorldTab`,
whose expected list lacks the player commands added since (Accessories, artificerrank, FishMongerStatus, requisitions,
ShardMusic). Some read this PC's live state (the P83 tile expected "PLAY TESTS: 111 OPEN" and read "3 FAIL NOT
LOGGED"). I did not change them.

## Decisions for Chase

1. **The soak transcript can block a commit again.** Every Golem that finishes between 01:30 and the end of the soak
   commits a growing `soak.txt`; once it passes 5 MB, every commit of the docs repo is refused until someone
   intervenes. Two small fixes, either is a follow-up prompt: the bot caps or rotates the soak transcript under 5 MB,
   or `.gitignore` keeps `testing/bot-runs/*/transcripts/soak.txt` out (the report and results stay in git).
2. **The 13 red Shard-Console facts on main** want their own fix-up (stale expected lists and live-state reads).

## Files changed

`shard-migration`: this note. `ShatteredLegacy`: none.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P597`: code
"nothing to commit"; docs 1 file pending (this note), "dry run: would add, commit and push". Nothing BLOCKED.

P597 DONE
