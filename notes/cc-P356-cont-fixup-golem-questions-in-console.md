# cc-P356: fix-up for P216 (Golems ask their questions on the console): its branch did not merge into main

**Golem:** Bronze. **Date:** 2026-10-21. **Branch:** `golem/Bronze/P356` in both work copies. **Touches:**
web-console and the Shard Console. No `server\` or `docker\` change, so no image build was needed.

## In plain words

- The console side of the Golems' questions (P216) can be merged now. It had clashed with this morning's
  test-account buttons (P215) and the Music Room (P367); now all three work side by side in the web console.
- After the merge, each Golem's card on the web console shows its open questions, with a button per answer, and
  the Shard Console's Golem tab has "Answer a Golem's question".
- I also fixed a small P216 bug in the Shard Console: refreshing the Golem tab could throw an error when the
  window had no Answer button.
- Nothing for you to do.

## Headlines

- **ShatteredLegacy:** `origin/main` (`59fb338`, which includes P264/P369 and P275) plus `origin/golem/Bronze/P216`
  (`b9b7d92`). Two files conflicted, `web-console\server.py` and `web-console\static\app.js`; both are resolved with
  every side kept.
- **shard-migration:** `origin/main` plus P216's docs branch (`8d3932a`: its notes and the staged Golem files).
  This merged without conflicts.
- **One real bug fixed** in P216's `scripts\Shard-Console.ps1` (below). The merge surfaced it as a red
  `P99_TheConsoleReadsTheGolemFirstAndFallsBackToTheAutopilot`.
- **Tests:**
  - web console: **109 of 109 pass**, 1 skipped. That includes P216's `test_questions.py`, P215's tests and my
    Music Room tests.
  - Shard Console: P216's own fact passes. The other failures were already on main (see Tests).

## The conflicts

| File | Main's side | P216's side | Resolution |
|---|---|---|---|
| `web-console\server.py`, the POST route list | the Music Room's two POSTs (P367) and `/api/golem-password` (P215) | `/api/answer` | Kept all four: the Music Room routes first, then `("/api/action", "/api/preview", "/api/golem-password", "/api/answer")`. |
| `web-console\server.py`, the handlers | P215's "copy password" handler | P216's `/api/answer` handler | Kept both, one after the other. Each returns on its own path. P216's `_read_json(16384 if /api/answer else 4096)` and main's `_not_this_page()` check (from P367) merged on their own, so both POSTs go through the same page checks. |
| `web-console\static\app.js`, a Golem card | P219's "Legion script tests" line and P215's test-account buttons | the card's question block (`questionBlock`) | Kept both: P219's and P215's lines first, then the questions. |

Main moved twice while I worked: P264/P369, P361 and P275 merged. Each time I aborted, fast-forwarded to the new main
and merged P216 again with the same resolutions, so the branch sits on the newest main (`59fb338`).

**A slip, undone.** The first docs-repo merge had no conflicts, and my `git merge --no-edit` committed it
(`e461bfc`). I reset that local, unpushed commit (`git reset --keep ORIG_HEAD`) and merged again with
`--no-commit`, so both repos are left mid-merge with everything staged for the Golem's commit.

## The bug fixed in P216's Shard Console code

In `scripts\Shard-Console.ps1`, the Golem tab's refresh (P216: "Answer lights while a Golem on this PC has an open
question") did this:

```powershell
if (@($script:ui.GolemAnswerButtons).Count) { ... foreach ($b in @($script:ui.GolemAnswerButtons)) { $b.Enabled = ... } }
```

In Windows PowerShell 5.1, `@($null).Count` is 1. So when the window has no Answer buttons, the guard passes and
the loop sets `Enabled` on `$null`. That throws "The property 'Enabled' cannot be found on this object". It happened
in `P99_TheConsoleReadsTheGolemFirstAndFallsBackToTheAutopilot`, which refreshes with an empty `$script:ui`, and it
could happen in any window built without that row.

The fix filters out nulls first (`@($script:ui.GolemAnswerButtons | Where-Object { $_ })`) and loops over what is
left. **Red, then green:**
- **Red:** P99 failed with that message in the full suite on the merge.
- **Green:** P99 passes after the fix, and P216's own fact still passes.

## Tests

- **Web console** (`python -m unittest discover -s web-console/tests`): **109 of 109 pass**, 1 skipped.
  - In the first run on the merge, the three `test_golem_glow` phone facts failed. They also fail against main's
    code (I saw that this morning in P367). They passed in the run after, so they are intermittent.
- **Shard Console** (`scripts\tests\Shard-Console.Tests.ps1`, the full suite, both runs on this PC):
  - **main** (a temporary detached worktree of `59fb338`, since removed): 440 facts, 427 passed, **13 failed**
  - **the merge, after the fix:** 441 facts, 426 passed, 15 failed
  - **The 13 failures in both** are window and environment facts: P83/P101/P107 links and sites, P135 map and art
    tools, the World tab's window-action facts and others. They are the same on main, so this change does not touch
    them.
  - **The 2 failures only on the merge are timing limits, not regressions.** I ran each in isolation 3 times on
    both trees:
    - `P84_TheUOLookAddsUnderASecondToTheStart` (under 1000 ms) **failed on main** once (1049 ms) and passed on the
      merge 3 times.
    - `P154_TheRefreshNeverRunsOnTheWindowsThread` (under 500 ms) passed 3 times on each.
    - Other Golems' builds were running on this PC at the time.
  - `P216_TheGolemTabShowsTheOpenQuestionsAndAnswerRunsAnswerQuestion`: **pass**.
- **Golem side:** P216's Golem tests (`D:\UO\golem\tests`) are not in either repo. P353 installed that side and is
  on main, and this fix-up changes nothing there.
- **No image build:** P216 changes nothing under `server\` or `docker\uo\`.

P356 DONE
