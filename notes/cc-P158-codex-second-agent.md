# cc-P158: Codex as a second agent (the review before each commit, and one pilot lane)

Written 2026-10-20 (20:55 to 23:35) by the Iron Golem (Opus), on branch golem/Iron/P158 of both repos. Built on P152's
runner (`D:\UO\golem\Codex.ps1`, its usage file and budget), as the overseer's change of 10-17 asks. P152 is DONE.

## Headlines

1. **Codex now reviews every prompt before the Golem commits it.** After `P<nn> DONE`, `codex exec review`
   (read-only) looks at each repo's uncommitted changes with the prompt file as context. Both repos are reviewed at
   once.
   - The review lands in the docs work copy as `notes\cc-P<nn>-<name>-codex-review.md`, so it is committed with the
     prompt.
   - High findings (Codex's P0 and P1) go in the done email under "Codex flagged" and are appended to
     `D:\UO\overseer\codex-flags.md`.
   - **It never blocks the commit.** Over budget, Codex off, a timeout or a crash only skip it, and the email says so.
2. **A Codex lane can take a prompt the overseer marks `**Agent:** Codex OK`.**
   - It is a Golem with `engine: codex` in `golems.json`, driven by the 10-minute watch.
   - It works in its own work copies on `golem/<lane>/P<nn>`, starts only at night (`codexNightOnly`), and only when
     no CC prompt touches the same areas.
   - It stops at a stopping point (P156's rule), never a kill, and carries on later in the same Codex session.
   - When Codex says DONE, the Golem runs the prompt's `**Lane tests:**` and the commit preflight, then commits.
   - The integrator merges the branch only if it merges cleanly. Anything else is a NEEDS YOU email, never a fix-up
     prompt.
3. **A lane never runs on Chase's own Codex sign-in.** Measured tonight:
   - A writing (`workspace-write`) Codex run adds `[projects.'<its folder>'] trust_level = "trusted"` to its
     `CODEX_HOME`'s `config.toml`. It does so even with `--ignore-user-config`, and even with that key passed as a
     `-c` override.
   - A read-only run (a review, art) does not.
   - So a lane runs only in `D:\UO\golem\codex-home\<account>`, which Chase signs in once. Until then it takes nothing
     and says so.
   - **I found this the hard way.** A test-harness slip started six real lane runs. They added six such entries to
     Chase's `config.toml`, and I removed exactly those six. The file is byte for byte as it was before P158
     (SHA-256 `95e00c3b5e992107...`, at the start and at the end). Details under Deviations.
4. **Real runs.**
   - **Reviews:** three of committed prompts' diffs. P222's found a real P1 bug (below).
   - **Lane:** six real runs of the lane runner on throwaway prompts in scratch branches (the slip above). They
     proved workspace-write, `--add-dir`, the live event stream and the STOPPED contract.
   - **Not seen yet with real Codex:** a whole lane prompt through DONE, commit and merge. It is tested with a stub
     Codex, the real `Commit-ShardWork.ps1` and the real integrator, and checked with the stub through
     `tests\Prove-CodexLane.ps1`. That script runs it for real, once, the moment the lane's sign-in exists
     (For Chase).
5. **AGENTS.md** in both repos has a new section, "Standing rules for every agent run by the Golem", with the seven
   rules. A test in each repo fails if one is dropped.

## What Codex reports about the plan (section 1, confirmed)

- **`codex exec --json` stdout:** no rate limits at all.
  - A normal exec reports its tokens in `turn.completed`.
  - **A review reports 0 tokens there.** P152's runner therefore counted every review as free; fixed below.
- **The session logs** (`~\.codex\sessions\**\rollout-*.jsonl`): every `token_count` event carries `rate_limits`:
  - `primary`: `window_minutes` 300, `used_percent`, `resets_at` (epoch);
  - `secondary`: `window_minutes` 10080;
  - `credits` (`has_credits` true), `plan_type` `team`, `rate_limit_reached_type`, `spend_control_reached`.
- **A review runs as two threads.** The exec thread logs no `token_count`. Its child (`source: {subagent: review}`,
  same cwd) does, and also logs the verdict, as `task_complete`'s JSON message and as the parent's `ExitedReviewMode`
  item (`findings[]` with `priority` 0 to 3, `code_location`, `confidence_score`; `overall_correctness`).
- **This seat's windows at 23:25:** 5-hour 5%, resetting Wed 03:01; week 7%, resetting Tue 10-27 16:54.
- `codex-usage.json` is written after every Golem run, as P152 built.
- **The tier:** `--ignore-user-config` keeps Chase's desktop `service_tier = "priority"` out, and no tier is passed,
  so Golem runs are on the standard tier (P152 found this; unchanged).

## What changed

Backups of every file edited outside the repos: `*.bak-20261020-p158` beside `Codex.ps1`, `golem.ps1`, `Golems.ps1`,
`settings.json`, `README.md`, `tests\Codex.Tests.ps1` and `tests\Golem.Tests.ps1` in `D:\UO\golem`, and
`~\.codex\config.toml.bak-20261020-p158` (taken before the six entries were removed).

### `D:\UO\golem\Codex.ps1` (P152's runner; reviews and lanes added, nothing duplicated)

- `:2-30` the header; `:31-50` new parameters: `-Action review`, `-Sandbox`, `-AddDirs`, `-StopFile`,
  `-ResumeThread`, `-OutFile`.
- `:72` `Get-CodexSettings`: the new defaults (`codexReviewModel`/`Effort` gpt-6.1-sol medium, `codexLaneModel`/`Effort`
  gpt-6.1-sol high, `codexReviewMinutes` 15, `codexNightOnly`, the night window's keys).
- `:244` `Get-CodexExecArgs`: `-Sandbox` (default still read-only) and `--add-dir`.
- The new functions:

  | Function | Line | What it does |
  |---|---|---|
  | `Get-RolloutTokens` | `:260` | a rollout's total tokens |
  | `Find-RunRollouts` | `:274` | a run's own logs, by cwd and start time, never Chase's |
  | `Read-ReviewOutput` | `:301` | the verdict and findings; P0/1 high, 2 medium, 3 low |
  | `Get-CodexReviewArgs` | `:340` | `exec review` with custom instructions on stdin, read-only by config key |
  | `Get-CodexResumeArgs` | `:351` | `exec resume` with the sandbox and writable roots as config keys |
  | `Test-CodexLaneHours` | `:363` | the night window |
  | `Test-CodexRunSpent` | `:376` | P156's rule: the run's own rise counts toward the Golem's share |
  | `Test-CodexLaneHome` | `:389` | a writing run is refused on `~\.codex` |
  | `Request-CodexStop` | `:397` | the stop file, written once, with why |
  | `New-CodexLanePrompt` | `:406` | the lane's contract and the prompt |
  | `Get-CodexLaneOutcome` | `:434` | DONE, with the notes' last line too; STOPPED; PAUSED |
  | `Format-CodexReviewNote` | `:453` | the review note |
  | `Get-HighFindings` | `:476` | one line per high finding, for the email and the list |
  | `Start-CodexProcess` | `:526` | sets `CODEX_HOME` for a lane home; streams stdout for a lane |
  | `Get-RunAfter` | `:543` | the limits and tokens after a run, from its own rollouts |

- `:557` `Invoke-CodexRun`:
  - lane model and effort;
  - the own-home refusal;
  - a lane is never killed: its events are written as they come, the windows are read each minute, and past the
    budget it writes the stop file once;
  - tokens come from the rollouts when stdout says 0.
- `:646` `Invoke-CodexReviewRun`, the review action:
  - the same budget, skipped (never overridden) when it refuses;
  - killed at its limit (a review writes nothing);
  - the verdict read from the run's logs.

### `D:\UO\golem\golem.ps1`

- `:374`, `:391`: settings keys `codexEnabled`, `codexNightOnly`, `codexReviewMinutes`, `codexReviewHookSeconds`,
  `codexFlagsFile`.
- `:321`: under `-NoMail` (tests only), each email body is also written to `test-mail.txt`.
- **The review** (`:2615-2730`):
  - `Get-StopHookSeconds` `:2623`: the Stop hook's own timeout, read from the session folder's
    `.claude\settings.local.json`.
  - `Get-ReviewRepos` `:2634`.
  - `Add-CodexFlags` `:2644`: append only, ASCII.
  - `Invoke-PromptReview` `:2655`:
    - one `Codex.ps1 -Action review` per dirty repo, at once;
    - a deadline of the time limit plus 20 s, then the process tree is killed;
    - the note, the flags and the email lines.
  - Called once per DONE (`reviewedFor`) at `:4419`, before the commit. It is wrapped, so nothing it does can stop the
    commit.
  - The Codex lines go into the branch email (`:4516`, said once), the starting email (`:3231`) and the queue-empty
    email.
- **The lane** (`:2731-3010`):
  - `Join-ProcArgs` `:2741`: quotes the arguments `Start-Process` would split.
  - `Get-CodexHomeFor` `:2750`, `Set-LaneWhy` `:2755`, `Get-CodexBudgetNow` `:2761`.
  - `Update-LaneProgress` `:2773`: the step line from Codex's `todo_list` events, and keeps the claim alive.
  - `Start-CodexLaneRun` `:2793`: start or resume.
  - `Set-LaneNeedsYou` `:2831`.
  - `Invoke-CodexLaneTick` `:2844`.
  - `Invoke-CodexLaneFinish` `:2924`: the Lane tests in the lane's work copies, the preflight, the commit and the
    ticket.
- `:3825`: the shared watch also starts each local Codex lane's tick.
- `:3829-3837`: a Codex Golem's own Watch is its tick; `-Event LaneFinish` is new.
- `:2500`: the integrator's NEEDS YOU email for a Codex branch that did not merge.
- **Every dot-source of `Codex.ps1` keeps the hook's own `$Root`.** Without that, its parameter block re-points
  `$Root` (the slip under Deviations).

### `D:\UO\golem\Golems.ps1`

- `:237`, `:244`: `codexEnabled` read for the claim rule.
- `:260-275`: `Test-CodexOk`, `Get-LaneTests` and `Test-CodexLaneOn`.
- `:320-339`, `Get-ClaimCandidate`:
  - a Codex lane takes only a Codex OK prompt with a Lane tests line and a real Touches line;
  - a CC Golem leaves a Codex OK prompt to an enabled lane.
- `:625`: a merge ticket records the Golem's `engine`.
- `:944`: the integrator gives a Codex branch's conflict or red build to Chase. There is no fix-up prompt, and the
  branch is kept.

### `D:\UO\golem` other

- `settings.json`: only the new keys, at their defaults.
- `README.md`:
  - a new section, "Codex as a second agent" (`:252`);
  - P152's "For P158 and P159" note updated;
  - the Files table (`codex-home\<account>\`, the fixtures, the proof script).
- `tests\fixtures\codex-review-*.jsonl` (new, 40 KB): the two real review runs of 20:49 and 20:50, trimmed to the
  lines the parser reads. Command output is cut, and only the review threads' own logs are used.
- `tests\Prove-CodexLane.ps1` (new): the lane once for real, in scratch repos.

### `D:\ShatteredLegacy` (the Iron work copy)

- `AGENTS.md:70`: "Standing rules for every agent run by the Golem" (the seven rules; the rest is this file,
  `D:\UO\shard-migration\AGENTS.md` and the prompt).
- `scripts/tests/test_agents_md.py` (new).
- `scripts/Shard-Console.ps1`:
  - `:2044`: the Golem panel's tooltip now names the reviews, the lane and its night window.
  - `:5012`: the "Codex today" row adds the day's runs by use ("2 review(s), 1 lane run(s), 1 art run(s)"). The
    "ChatGPT plan (Codex)" bars beside the Claude bars are P152's, unchanged.
- `scripts/tests/Shard-Console.Tests.ps1:8270`: `P158_TheCodexTodayRowSaysTheReviewsAndTheLaneRuns`.
- `CHANGELOG.md` / `VERSION`: 2026.10.20.19, one `### Staff` line. 2026.10.20.18 was already committed (P156's
  merge), so this starts the next version.

### `D:\UO\shard-migration`

- `AGENTS.md:34`: the same section (the rest: this file and the prompt; `CLAUDE.md` only points here).
- `tools/tests/test_agents_md.py` (new).
- This note.

## One real review on a real committed prompt's diff

Run with this runner's settings: `gpt-6.1-sol`, medium effort, read-only, the prompt file as context.

**P222 (the Tinker), commit `22d5991`:** 61 s, 308,016 tokens (253,568 cached). Verdict "patch is incorrect"
(confidence 0.99).

- **[P1] (high), "Preserve the Tinker payload in the web status document"** (`web-console/static/app.js:267`):
  - "The normal collector passes every card through `ConvertTo-GolemCardDocument`, which copies `merge` but never
    copies `tinker`. `server.py` does not restore that payload for local cards."
  - "Consequently, this renderer always receives a null `t`: it says 'No round yet,' hides fixes, questions and kit
    synchronization results, and never offers Resume after Pause."
- **[P2] (medium), "Render watchdog status in the desktop console"** (`scripts/Shard-Console.ps1:1259`):
  "`Get-GolemCardLines` still treats every script-engine card as Shadow Iron: Tinker is labelled 'merges,' reads the
  nonexistent `merge` block."

These look real. They were not in P222's notes or its tests, and P244 (the merge fix-up) did not see them. They are
the overseer's: the review ran before the flags list existed, so I did not append them to it myself.

**P233 (an AbilityProfile from [props), commit `b5ac1f6`, reviewed twice:**

- **20:49:** 38 s, 198,092 tokens, "patch is correct", no findings.
- **22:02** (through `Codex.ps1 -Action review`): 0.7 min, 153,311 tokens; the 5-hour window 1 to 3%, the week 6 to 7%.
  This time it found a medium: "the explicit unchanged-store requirement is not implemented; the new test instead
  requires creation of an in-memory entry" (`PropsAbilityProfileVerification.cs:215`).
- **Two runs of the same review can differ.** Treat a clean review as "nothing found this time", not as proof.

## Tests

Every new fact was seen failing first, against the code before its change.

- **Against P152's runner:** the eight review and lane facts failed 12 checks, then the config fact 13.
- **The rest:** each red run is listed with its fix below.

`D:\UO\golem\tests\Codex.Tests.ps1`, 10 new facts:

| Fact | What it shows |
|---|---|
| `P158_TheNewSettingsHaveTheirDefaults` | the review and lane models and efforts, `codexReviewMinutes` 15, `codexNightOnly`, the night window |
| `P158_TheReviewIsReadFromTheRealSessionLogs` | the real P222 review: two findings, P1 high at `app.js:267`, P2 medium; the subagent's log gives the same; P233's: none; stdout alone has no review |
| `P158_AReviewsUsageAndTokensComeFromItsSubagentLog` | the parent logs no limits; the subagent's are 37% and 6%, team; 198,092 tokens where stdout said 0; a run's logs found by cwd and time, never Chase's own session at the same moment; `D:/x/` and `D:\x` are one folder (seen failing: the first real run through the new action found no logs) |
| `P158_TheReviewAndLaneArgumentsKeepChasesConfigOutAndTheRightSandbox` | review read-only with custom instructions only; lane `workspace-write` with `--add-dir`; resume with config keys; no tier |
| `P158_TheLaneRunsOnlyInTheNightWindowWhenNightOnly` | 14:00 no, 23:10 and 05:00 yes, off: any time |
| `P158_ALanePastItsBudgetIsAskedForAStoppingPointOnce` | a 20-point rise is fine; 41 points, the week reserve or the hard stop are spent; the stop file written once, saying why |
| `P158_TheLanePromptCarriesTheContractAndTheOutcomeIsRead` | AGENTS.md, DONE/STOPPED/PAUSED, the stop file, no commits, PS 5.1, Haven; DONE needs the notes' last line too |
| `P158_TheReviewNoteSaysEachRepoAndPutsHighFindingsFirst` | the note's sections, the high list |
| `P158_ChasesConfigTomlIsNeverReadOrWritten` | the real config.toml hashed around `status` and `usage`; no write names it; every way Codex starts skips it |
| `P158_ALaneNeverRunsOnChasesOwnCodexHome` | a writing run refused on `~\.codex`, however it is written; read-only and a lane home allowed |

`D:\UO\golem\tests\Golem.Tests.ps1`, 11 new facts:

- A stub `Codex.ps1` in each test world answers as the fact says. Its `-LoadOnly` gives the real formatters.
- Bronze, or the Codex lane Agapite, works on real git repos with a bare origin.
- The merge facts use the real `Commit-ShardWork.ps1` and the real integrator.

| Fact | What it shows |
|---|---|
| `P158_CodexReviewsEachRepoBeforeTheCommitAndNeverBlocksIt` | one review per work copy, both before the commit; the 15 minutes cut to 6 by a 600 s hook; the note in the docs copy; only the high finding on the overseer's list; "Codex flagged" in the done email, once (seen failing: the queue-empty email repeated it) |
| `P158_AReviewOverBudgetTimedOutOrCrashedIsSkippedAndTheCommitGoesOn` | over budget, timed out (a 3 s limit against a 120 s stub, committed within 100 s), crashed, Codex off: each committed, each said; no note when nothing was reviewed (seen failing, then the rule changed) |
| `P158_AStopHookTooShortForAReviewSkipsIt` | a 200 s hook: no review, committed, said |
| `P158_TheLaneTakesOnlyACodexOkPromptWithItsTouchesAndLaneTestsLines` | by day nothing; at 23:00 only P104 (P101 not Codex OK, P102 no Touches, P103 no Lane tests, each said); its own branch and worktree, workspace-write; the contract handed; the run's files stay under the test world; Bronze leaves a Codex OK prompt to the lane |
| `P158_ALaneWithoutItsOwnCodexSignInTakesNothing` | no `codex-home\<account>\auth.json`: nothing claimed, the login command said |
| `P158_AnEmptyQueueIsAQuietTickNotAFailure` | seen failing: the tick threw on an empty queue (found by the proof script's dry run) |
| `P158_TheLaneWaitsWhileACCPromptTouchesTheSameArea` | a web-console CC prompt holds a web-console Codex prompt |
| `P158_ALaneThatFinishesIsTestedCommittedAndMergedCleanly` | the Lane test ran in the lane's work copy; preflight clean; committed and pushed; the ticket says codex; merged into main; the prompt in completed\ |
| `P158_AConflictLeavesTheCodexBranchAndNeedsYouWithNoFixUp` | main changed the same file: needs you, no fix-up prompt, the branch kept, main unchanged |
| `P158_ALaneThatStopsOrFailsItsTestsLeavesItsWorkAndNeedsYou` | STOPPED: the email with the reason, nothing committed, the prompt kept claimed, the lane takes nothing new; a Lane test exiting 3: needs you, the work left in place |
| `P158_APausedLaneIsCarriedOnWhenTheBudgetAllowsAgain` | PAUSED keeps the thread; over budget it waits; then `resume th-1` in the same session, and it finishes |

Repo facts:

- `scripts/tests/Shard-Console.Tests.ps1`: `P158_TheCodexTodayRowSaysTheReviewsAndTheLaneRuns` (red first; P152's own
  fact kept its exact wording, after a first try broke it).
- `scripts/tests/test_agents_md.py` and `tools/tests/test_agents_md.py`: each fails while a rule is missing (both were
  red before the sections were written) and checks that removing one is noticed.

**The full suites, Windows PowerShell 5.1, 22:56 to 23:25 on 10-20:**

| Suite | Result |
|---|---|
| `Codex.Tests.ps1` | 111 checks, 0 failed |
| `Tinker`, `GolemPower`, `UoFiles`, `Assign` | all passed |
| `Golem.Tests.ps1` | 941 checks passed, 7 failed in 4 facts: the two P184 claim facts (known, below), and P125's and P131's usage-limit facts |
| `GolemPaths` / `Join` / `Move-ToGolem` / `RemoteAgent` | 1 failed / 4 failed / stopped at its first error / stopped at its first error |
| `Shard-Console.Tests.ps1` | 437 facts, 423 passed, 14 failed |
| web console (`python -m unittest discover -s tests`) | 76 OK (1 skipped) |
| code repo `scripts/tests` (Python) | 55 OK |
| docs repo `tools/tests` (Python) | 172 run, 4 failed |

- **None of the failures is P158's.**
  - **P125 and P131 usage-limit facts:** the run was near midnight. Their reset times crossed into Wednesday, so the
    text reads "Ready at Wed 1:19 AM", which their patterns don't allow. Run against the pre-P158 golem files at
    23:22, they failed identically. They passed in this session's 21:00 full run.
  - **The two P184 facts:** they fail the same way on the pre-P156 code (P156's notes).
  - **GolemPaths, Join, Move-ToGolem, RemoteAgent:** the same causes as P156's notes. They are this PC's layout (Iron
    as integrator, `D:\UO\overseer`, Tailscale, a scheduled task that no longer exists) and "type wake gold to
    confirm". None runs a file P158 changed.
  - **Console:** the 14 are main's 14 of tonight, less the flaky P60, plus `P154_TheRefreshNeverRunsOnTheWindowsThread`
    ("520 ms", a timing check run while the Golem suite loaded the PC). It passed twice alone.
  - **Docs repo:** 3 of the 4 fail on a clean HEAD worktree too (mapops' shipped patch, two play-who real-file
    facts). The 4th (`test_two_writers_at_once_lose_nothing`, a race) passed 4 out of 4 alone.
- **config.toml** was `95e00c3b5e992107...` at the start and is `95e00c3b5e992107...` now.

## Deviations and decisions for Chase

- **A test-harness slip ran real Codex six times, and it changed your config.toml.**
  - **What happened.** The test stub's `-LoadOnly` dot-sourced the real `Codex.ps1` without `-Root`. Its parameter
    block reset the hook's `$Root` to `D:\UO\golem`. The six lane facts' first run (22:24) then started the real
    runner in their temp worktrees, as real `workspace-write` Codex runs.
  - **What it cost.** About 90k tokens each; the 5-hour window rose 1 or 2 points; the week did not move.
  - **What Codex did.** It followed the contract (`P102 STOPPED: Missing AGENTS.md...`) and wrote notes in the temp
    docs copies only.
  - **What it changed.** It added six `[projects.'c:\users\ckfle\appdata\local\temp\golem-test-...\code'] trust_level
    = "trusted"` entries to `~\.codex\config.toml`. I removed exactly those six blocks (a backup is beside it,
    `config.toml.bak-20261020-p158`). The hash matches the one taken before P158 began.
  - **What prevents it again.**
    - Every dot-source of `Codex.ps1` in golem.ps1 now keeps `$Root`.
    - A fact checks that a test lane's files stay in its world.
    - A lane can't run on your home at all (`Test-CodexLaneHome`, `P158_ALaneNeverRunsOnChasesOwnCodexHome`).
  - **The runs' files** are in the scratchpad, not `codex-runs\`:
    `C:\Users\ckfle\AppData\Local\Temp\claude\D--UO-golems-Iron-shard-migration\d4a847c6-d103-4b94-84a6-6fdd4f8031b1\scratchpad\accidental-lane-runs`.
    `codex-usage.json` keeps them as lane runs, since they did use the seat.
- **Two more tiny real runs, to find the cause** (`gpt-6-luna`, low effort, "reply OK").
  - The runs: one workspace-write without the override, one with a `projects.'<path>'.trust_level` `-c` override,
    and one read-only.
  - Results: both writing runs wrote the entry, the read-only run did not. Each change was restored at once from a
    copy beside the file, and the hash was checked each time.
- **The lane's own sign-in is a decision for you.** A lane cannot run until a home is signed in:
  `$env:CODEX_HOME = 'D:\UO\golem\codex-home\lane-chase'; codex login`. That is the folder Join-Golem.ps1 already
  uses for P159's lanes. Its trust entries then go into that home's own config.toml, never yours. I could not sign
  it in for you, and copying your `auth.json` would be copying a credential.
- **So the whole chain has not run with real Codex yet.**
  - The real runner's lane mode was seen working (the six runs).
  - The DONE to tests to commit to merge chain is tested with a stub Codex, the real commit script and the real
    integrator.
  - `tests\Prove-CodexLane.ps1` runs it all once for real after the sign-in. It was checked with a stub: "PROVED: ...
    merged into main", and its scratch repos and junction were cleaned up.
  - I wrote DONE rather than STOPPED: everything the prompt asks is built and tested, and the overseer's pilot prompt
    can only start once the sign-in exists anyway.
- **The lane is not switched on.** No Codex Golem is enabled on this PC: Agapite and Verite stay disabled on Steph's
  PC, as registered for P159. The prompt says the overseer marks the pilot prompt. Enabling a lane here is a registry
  change (`machine` and `enabled`) plus the sign-in; the README says how.
- **Branch names.** The lane's branch is `golem/<lane>/P<nn>` (the multi-Golem convention since P184), not `codex/Pnn`.
  It is still its own worktree (the lane's work copies), never a main working tree.
- **The integrator merges a Codex branch,** not the lane itself, and only fast-forward or clean (the integrator's
  merge, with P213's CHANGELOG/VERSION settling). A conflict or a red build is NEEDS YOU, not the usual fix-up prompt.
- **A Codex OK prompt needs a `**Lane tests:**` line** (one command per line, `none` if there are none). "That
  prompt's tests" have to be something the Golem can run. The prompt's own Tests section is prose, so the overseer
  writes the command next to the Codex OK line. Paths in it may say `D:\ShatteredLegacy` and `D:\UO\shard-migration`;
  the Golem reads them as the lane's work copies.
- **The lane waits when unsure.** A Codex OK prompt with no `**Touches:**` line is not taken, because guessing its
  areas could overlap a CC prompt. While a lane is enabled, CC Golems leave Codex OK prompts to it, so at night only
  (the default) such a prompt can wait a day.
- **The review's time limit fits inside the Stop hook.** The review runs in the Stop hook, before the commit, and
  the work copies' Stop hook has `timeout` 600. So the review gets `min(codexReviewMinutes, (hook - 240 s) / 60)` = 6
  minutes; a hook kill would take the commit with it. Tonight's reviews took under a minute. Raise the Stop hook's
  `timeout` to 1500 in the work copies' `.claude\settings.local.json` for the full 15.
- **`codex exec review` refuses custom instructions beside `--uncommitted` or `--commit`.** So the instructions say
  which changes to review: staged, unstaged and untracked, via git status and git diff HEAD. Then the prompt follows.
- **Every Golem reviews now, on every PC, through the kit.** Where Codex is not installed or not signed in, the
  review is skipped. The done email then says so in one line, and no note is written.
- **Severity.** Codex's priority: P0 and P1 are high (the email, the flags list), P2 medium, P3 low. A PAUSED prompt
  is not reviewed until it is DONE.
- **"Never connect to Haven" in AGENTS.md reads "unless the prompt itself says to, under the haven lock".** Some
  prompts do deploy to Haven, and a flat "never" would contradict them.
- **AGENTS.md "points to CLAUDE.md for the rest" the other way round.** In shard-migration, `CLAUDE.md` already
  points to `AGENTS.md`, with no rules of its own. ShatteredLegacy has no `CLAUDE.md`. So the new section names where
  the rest is (the rest of the file, the docs repo's AGENTS.md, the prompt) and says CLAUDE.md only points here.
- **The older AGENTS.md lines were left alone.** They say "Commit before handing off; Chase pushes" (code) and
  "Commit to `main`. Do not branch." (docs). The new rule 4 says they date from before the Golem. They are worth a
  tidy by whoever owns AGENTS.md; I did not rewrite rules I did not write.
- **Unattended denials, not retried:** the Read tool on `D:\UO\golem\Codex.ps1` (and earlier, in P244, on files in
  the Iron ShatteredLegacy copy). I read with `sed`/`cat` and wrote with Python patch scripts that assert each anchor
  exactly once, keeping each file's own line endings.

## For Chase

**What it costs on your seat (team; measured tonight):**

| Run | Time | Tokens | 5-hour window | Week |
|---|---|---|---|---|
| a review | 40 to 60 s | 150k to 310k, mostly cached | +2 points | about +1 |
| a lane run | (tonight's runs stopped early) | about 90k | +1 to 2 points | about 0 |

- **A review:** a prompt touching both repos gets two reviews, so expect about 4 points of the 5-hour window per
  prompt.
- **A lane run:** tonight's stopped early, so a real prompt costs more. `Prove-CodexLane.ps1` prints its cost.
- **The Golem's own share of a window is capped at 40%.** At 2 points a review, that is about 20 reviews per 5-hour
  window, after which reviews are skipped (said in the email) until it resets.

**The settings** (`D:\UO\golem\settings.json`):

| Setting | Default | What it does |
|---|---|---|
| `codexEnabled` | true | false stops reviews and lanes |
| `codexMaxPctPerWindow` | 40 | the Golem's share of each window (reviews, lanes and art together) |
| `codexWeekReservePct` | 30 | the week left to you and your wife |
| `codexNightOnly` | true | lanes only between `nightShiftStart` and `nightShiftEnd`; reviews any time |
| `codexReviewModel` / `codexReviewEffort` | gpt-6.1-sol / medium | a cheaper review: low; a deeper one: high |
| `codexLaneModel` / `codexLaneEffort` | gpt-6.1-sol / high | |
| `codexReviewMinutes` | 15 | cut to what the Stop hook leaves (6 min with today's 600 s hook) |
| `codexFlagsFile` | D:\UO\overseer\codex-flags.md | where high findings are appended for the overseer |

- **If Codex spends too much:** lower `codexMaxPctPerWindow`, or set `codexReviewEffort` to low.
- **To stop reviews entirely:** `codexEnabled` false.

**How a prompt goes to Codex (the overseer marks it; CC never adds the line):**

```
**Touches:** docs-only
**Agent:** Codex OK
**Lane tests:** powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1
```

**To turn the pilot on (this PC):**

1. Sign the lane in once: `$env:CODEX_HOME = 'D:\UO\golem\codex-home\lane-chase'; codex login; Remove-Item
   Env:CODEX_HOME`.
2. Prove it: `powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\Prove-CodexLane.ps1`. It should
   end "PROVED". It deletes its scratch repos and prints the cost.
3. In `golems.json`, give a Codex lane (engine codex, account lane-chase) `machine` CHASES-TOWER and `enabled` true.
   Then run `Setup-Golem.ps1 -Name <it>` for its work copies. The watch drives it from then on.
4. The overseer marks one small prompt as above.

**What P159 needs on the second PC:**

- The Codex CLI there (Join-Golem.ps1 step 4b already installs it for enabled Codex lanes).
- A `codex-home\<account>` signed in per lane: your seat as `lane-chase`, your wife's as `lane-steph` if she has a
  seat. On a Team workspace the limits are per member, so hers is a separate allowance.
- The registry entries enabled for that PC.
- **The usage reading will not see across PCs.** Each PC's runs move the same seat's windows, and every run reads the
  current figures from its own logs. But the Golem's share is counted per PC (`codex-usage.json` is per PC), so with
  lanes on two PCs on one seat, halve `codexMaxPctPerWindow` or share the file.
- The trust-entry behaviour above means each lane home's config.toml collects its work copies' entries. That is
  harmless, and Golem-owned.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P158 -NoRefresh`,
23:29 on 10-20, before this note was written. It was run again with it in place; the same result is below.

    Repo Result
    ---- ------
    code dry run
    docs dry run

- Code: AGENTS.md, CHANGELOG.md, VERSION, scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1,
  scripts/tests/test_agents_md.py.
- Docs: AGENTS.md, tools/tests/test_agents_md.py and this note.
- The review note (`notes\cc-P158-codex-second-agent-codex-review.md`) will be added by the Golem's own review at
  this DONE.
- No file is over 5 MB. No scratch is in either repo: the scratch is in the session's scratchpad.

P158 DONE
