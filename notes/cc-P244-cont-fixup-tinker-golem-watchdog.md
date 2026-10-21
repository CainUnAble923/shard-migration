# cc-P244: fix-up for P222 (the Tinker, a watchdog that unsticks the Golems and keeps every PC's kit in step)

Written 2026-10-20 by the Iron Golem (Opus), on branch golem/Iron/P244 of both repos. P222 finished on
golem/Iron/P222. The integrator could not merge it into main: CHANGELOG.md, VERSION and
scripts/tests/Shard-Console.Tests.ps1 conflicted with the work that reached main in between (P207's glow, P153's
facts, P199, P221 and others).

## Headlines

1. **Both repos hold the merge of golem/Iron/P222 and main, staged and uncommitted on golem/Iron/P244.**
   - golem/Iron/P244 was created at main: `bba762c` in ShatteredLegacy, `597ba20` in shard-migration.
   - "Check out P222 and merge main into it" and "merge P222 into P244" are the same two heads with the same merge
     base. I did the second (`git merge --no-commit --no-ff golem/Iron/P222`), because the hand-off forbids switching
     branches. This follows P202's fix-up.
   - `MERGE_HEAD` is left in place in both repos (`22d5991`, `34a2213`). The Golem's commit is therefore a proper merge
     with both parents, and P222's commit stays in history.
2. **Three conflicts in ShatteredLegacy, resolved so both sides survive.** shard-migration merged clean: P222 only adds
   its notes file there.
3. **Nothing P222 tests is red.**
   - Tinker: 132 checks, 0 failed.
   - Web console: 77 tests OK, 1 skipped (P222 had 69; main's work added the rest).
   - Console: `P222_TheTinkersButtonsRunTinkerPs1AfterTheirPhraseAndNothingElse` passes. The full console suite
     fails exactly what main fails.
   - Golem: P222's three facts pass.
   - No file under `server\` or `docker\uo\` changed, so there was no Docker build.
4. **Two small follow-ups I could not make.** The unattended run denied the Read tool on two files, and I was told not
   to retry another way. Neither one is P222's red. See Deviations.

## What changed

Nothing beyond the conflict resolution and this note. The merged content is P222's (see
`notes\cc-P222-tinker-golem-watchdog.md`, which arrives through the merge) on top of main:

- `scripts/Shard-Console.ps1`: the Tinker's Run now, Pause and Resume buttons (auto-merged).
- `web-console/console-actions.json`, `golem-actions.json`, `server.py`, `static/app.js`: the Tinker's card and the
  kit route (auto-merged).
- `web-console/tests/test_remote_golems.py`: the kit routes fact.
- The three resolved files below.
- `D:\UO\golem\` (Kit.ps1, TinkerLib.ps1, Tinker.ps1 and the rest) is outside the repos. It was deployed by P222 and
  needs no merge.

## The conflicts resolved

- **VERSION:** main `2026.10.20.17`, P222 `2026.10.20.10`. It takes the higher, `2026.10.20.17`, so the file is
  unchanged from main.
- **CHANGELOG.md:**
  - P222 had opened its own `## 2026.10.20.10` section with one `### Staff` line. Main already has a different
    `2026.10.20.10` section (P153's line), and sections up to `2026.10.20.17`.
  - As the prompt says, P222's line ("The Tinker, a watchdog on the game PC, ...") joins the newest section,
    `2026.10.20.17`, after P207's Staff line.
  - Main's `2026.10.20.10` to `.17` are kept as they are. The heading `2026.10.20.10` appears once.
- **scripts/tests/Shard-Console.Tests.ps1:** both sides appended facts at the end of the file:
  - main: P153's block, ending with `P153_TheStepLineAndTheEstimate`;
  - P222: `P222_TheTinkersButtonsRunTinkerPs1AfterTheirPhraseAndNothingElse`.

  Both are kept, P153's first. The P153 fact gets its closing brace back, then the P222 fact follows.
- Auto-merged, checked by eye: `app.js` adds P222's `isTinker`/`tinkerCard` next to P207's `portraitNode`. The JSON
  files parse. `node` is not on this PC, so `app.js` was not syntax-checked by a tool. The web-console tests load the
  page's routes, not the JS.

## Tests (Windows PowerShell 5.1, Python 3, 21:25-21:50 on 10-20)

| Suite | Result |
|---|---|
| `D:\UO\golem\tests\Tinker.Tests.ps1` | 132 checks passed, 0 failed |
| `web-console`: `python -m unittest discover -s tests` | 77 tests OK (1 skipped) |
| `scripts/tests/Shard-Console.Tests.ps1`, merged tree | 436 facts, 423 passed, 13 failed |
| the same suite on main (`bba762c`, scratch worktree, since removed) | 435 facts, 421 passed, 14 failed |
| `D:\UO\golem\tests\Golem.Tests.ps1` (run earlier this session, 21:10, on the live golem.ps1 that P222 deployed) | 148 facts passed, 2 failed (P184) |

- **The merged tree fails nothing that main does not.**
  - Its 13 failures are all among main's 14.
  - Main's 14th, `P60_AMessageCrossesTheChildCommandLineUnchanged`, passes on the merged tree; it is flaky (P156's
    notes saw the same).
- **The one failure not seen at P156's baseline (`7653de2`) is main's own:**
  `RedMeansTestOnlyUnclassifiedOrAPlainRunThatDeletesAndNothingElse`.
  - It expects a fixed list of red (deleting) commands. P221 (`5552804`) added `[DeleteCovetous` and
    `[DeleteWrongRevamp`, which really do delete, and the list was not updated.
- **The other 12 are the pre-existing console failures listed in the P156 notes.** Among them are the four World tab
  and window-mode facts, P83, P101, P107 and three P135 facts.
- **The two P184 Golem failures** are the claim rule. They fail the same way on the pre-P156 golem.ps1, as shown in the
  P156 notes.

## Deviations and decisions for Chase

- **Merged into P244 rather than checking out P222.** The hand-off forbids switching branches. The result is the same
  merge, and `MERGE_HEAD` keeps it a real merge commit.
- **Denied (unattended), not retried:** `Read` of `D:\UO\golems\Iron\ShatteredLegacy\web-console\static\app.js`
  (lines 265-275).
  - I wanted to make P222's new Tinker card use P207's `portraitNode(c, ...)` for its portrait, as `mergeCard` does. In
    `tinkerCard`, replace the five-line `if (c.portraitUrl) { var img = el('img', 'portrait'); ... }` with
    `if (c.portraitUrl) top.appendChild(portraitNode(c, (c.display || c.name)));`.
  - Without it, the Tinker's portrait has no glow. Cosmetic only; every other card glows.
- **Denied (unattended), not retried:** `Read` of `scripts\tests\Shard-Console.Tests.ps1` at line 891.
  - I wanted to add `[DeleteCovetous` and `[DeleteWrongRevamp` to the expected list in
    `RedMeansTestOnlyUnclassifiedOrAPlainRunThatDeletesAndNothingElse`.
  - That failure is on main since P221, not from P222, so the fix-up does not need it. Whoever owns P221's follow-up
    can take it.
- **Version heading.** P222's line went under main's newest heading, `2026.10.20.17`, as the prompt's rule says. If
  `2026.10.20.17` is already deployed or its patch notes published, move the line under a new heading and bump
  VERSION. It is a Staff line, so the login bulletin does not show it to players either way.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P244 -NoRefresh`,
21:52 on 10-20, before this note was written:

    Repo Result
    ---- ------
    code dry run
    docs dry run

- Code: the merge's 8 staged files.
- Docs: P222's notes (through the merge) and this note.
- No file is over 5 MB, and no scratch is in either repo.

P244 DONE
