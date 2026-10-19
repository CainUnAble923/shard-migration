# cc-P174: P161's session closer kills the session the Golem just opened

2026-10-18. Opus. Prompt: `D:\UO\cc-prompts\cc-P174-cont-session-closer-fix.md`. Not committed (the Golem commits
after DONE). Both repos were clean at the start. Read first: P161's notes (`notes/cc-P161-close-finished-sessions.md`).

## Headlines

- **The cause:** on a new session's SessionStart, `Close-GolemSessions` (`golem.ps1`) also looked at the **new**
  session itself:
  - it was linked a moment before;
  - no session is newer than it;
  - it is not busy yet (no tool call or message recorded);
  - it has no `lastStopUtc`, because its first turn has not ended. `Get-AgeMin` reads a missing stamp as
    `[double]::MaxValue` minutes, "stopped long ago".
  So while the Golem rested, the new session passed every "finished: the Golem is resting" test and was closed, the
  same second it reported. That is golem.log 10-18 08:48:19 (P149) and 15:25:23 (P163, six seconds after the console's
  Wake opened it). The start phrase never ran, nothing was handed, and the Golem stayed resting.
- **The fix, two guards** in `Close-GolemSessions`:
  1. A session is finished only once it has a Stop on record (`lastStopUtc` present).
  2. A hook never closes the session it is running in.
  P161's rules are otherwise as they were: the previous session closes once the new one has reported, and a finished
  one closes `closeFinishedAfterMinutes` after its last turn while the Golem rests.
- **Reproduced red** with fake sessions.json, state and processes (P161's harness) against the unfixed script. In every
  resting kind the new session was stopped along with the old one, with "closed Golem P101 (process 5001, session
  sess-new): finished: the Golem is resting (run cap); a new session reported", the 15:25:23 line. The resting kinds:
  run cap, pace, usage limit, night shift ended, long run ended, winding, and Golem stopped.
- Model, context and bot-window rests did not show the bug; P161 does not count them as resting. They are in the new
  fact all the same.
- **`closeFinishedSessions` is back on** (`true`) in `D:\UO\golem\settings.json`, set after the suites passed. The
  overseer had turned it off at 15:27.

## What changed

All in `D:\UO\golem\` (outside both repos). Backups: `golem.ps1.bak-20261018-p174`, `settings.json.bak-20261018-p174`,
`tests\Golem.Tests.ps1.bak-20261018-p174`. The overseer's own `settings.json.bak-20261018-closeoff` is untouched.

| File | Change |
|---|---|
| `golem.ps1` (2,434 → 2,440 lines) | :129-130 header note for cc-P174. :860-862 the why, above `Close-GolemSessions`. :878 `if ($SessionId -and $sid -eq $SessionId) { continue }`, the hook's own session. :888 the resting branch requires `[string](Get-Prop (Get-Session $sid) 'lastStopUtc' '')` before it compares the age |
| `tests\Golem.Tests.ps1` (1,334 → 1,399 lines) | :1332-1397 the cc-P174 block: `New-RestWorld174`, `Invoke-NewSessionStart174` and three facts |
| `settings.json` | `closeFinishedSessions` false → **true**; nothing else changed (the key order and line endings are the overseer's) |

`D:\ShatteredLegacy`:
- `CHANGELOG.md`: new version `## 2026.10.18.15` with one `### Staff` line (2026.10.18.14 was committed with P173).
- `VERSION`: 2026.10.18.15.

`D:\UO\shard-migration`: this note.

## Tests

**Golem:** `powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\Golem.Tests.ps1`, Windows PowerShell
5.1.

The three new facts:
1. `P174_TheNewSessionSurvivesItsSessionStartInEveryRestAndTheOldOneClosesAfter`, for each of run cap, pace, usage
   limit, model, context, bot window, night shift ended, long run ended, winding, and the Golem stopped (no ENABLED):
   - the old P100 session (last turn ended 10 min ago) and a recorded, unreported P101;
   - a watch closes nothing;
   - P101's SessionStart links it and **never stops 5001 or its cmd.exe 5000**;
   - **only the old CLI 4001 is stopped**, "superseded by Golem P101";
   - a watch 10 minutes later still leaves P101 open (a long first turn with no tool call).
2. `P174_TheHookNeverClosesItsOwnSessionAndAFinishedOneStillCloses`:
   - the new session with no Stop yet is kept at 30 minutes;
   - after its first Stop and the delay, P161's "finished: the Golem is resting (run cap)" closes it, so nothing that
     should close stays open.
3. `P174_AManualWakeWhileRestingHandsTheNextPrompt`:
   - the run cap reached (runDone 2 of 2) and cc-P101 queued;
   - the woken session's SessionStart, then its start phrase;
   - P101 is handed in a new run (runDone 0), and the session holding it is open.

**Seen red first:**
- Against a `.ps1` copy of the unfixed script: **all three failed**, with the log lines quoted above (397 passed,
  31 failed in all).
- In the manual-wake fact the fake hook still logged "handed P101", because it cannot really die. The fact failed on
  "the session that holds it is open". In real life the session was already gone, which is why nothing was handed at
  15:25.

**After the fix: 427 passed, 1 failed.** The one failure is `P131_AUsageLimitRestSaysWhenItIsReadyAndNotifiesWhenItIs`.
It is P161's known clock fact: its reset 2 h 13 m ahead crosses midnight after about 21:47, and these runs were at
21:5x-22:2x. It failed the same way in the red run on the unfixed script. Not mine.

**Mutations,** each on a scratch copy, the whole suite:
- **Guard 1 removed** (finished without a Stop): `P174_TheNewSessionSurvives...` fails, at the 10-minute watch.
- **Guard 2 removed** (the hook's own session): nothing fails (427 / 1, P131 only). Guard 1 already covers every path
  that reaches the closer from a session's own hook:
  - SessionStart and the start phrase call it only right after `Register-HookSession` links a session;
  - a just-linked session has a new id, so it has no session file and no stop yet.
  So guard 2 is defence in depth, not separately pinned (Deviation 1).

One fix to my own fact on the way: the Stop hook stamps `lastStopUtc` with the real clock (`golem.ps1:2277`
`(Get-Date)`), not `-Now`. Fact 2 now records its first stop in test time with `Set-Session`, as P161's facts do. The
script was not changed for it, since in production the two clocks are the same.

**Console:** `D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1`: **365 passed, 6 failed.** None touch the Golem's
close rule.
- The 5 P161 recorded as failing before its change too: `P83_TheLinksOpenTheTwoPagesAndNothingElse`,
  `P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo` (live play-test data: "PLAY TESTS: 3 FAIL NOT LOGGED"),
  `P101_TheTileAndTheTabAreBuiltAndDrawn`, `P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing` and
  `P107_LinksAndSitesPointAtHavenAfterTheCutoverAndAtThisPcBefore`.
- `PlayerCommandsNeverAppearInTheWorldTab` (Deviation 3).

## Deviations and decisions for Chase

1. **Guard 2 cannot be seen red on its own.** It is kept because it is the direct statement of the rule (a hook is
   proof its session is alive), but no test path reaches it once guard 1 is in.
2. **Not done: `lastStopUtc` from the real clock.** It ignores the test clock (`-Now`). That is harmless in production;
   left as it was.
3. **A console failure from earlier work:** `PlayerCommandsNeverAppearInTheWorldTab` expects the player command list
   without `artificerrank`. That command came in with P145 (`db36221`,
   `server/customizations/Imbuing/ArtificerRankCommand.cs`); the fact's expected list was not updated then. A
   one-line fix in the console tests, for a later prompt; not P174's.
4. **The live Golem:** the fix is in the script the hooks run now, this session's included. No session was closed or
   opened by this work. The next Wake while resting is the real check (For Chase).
5. **No task-list tool exists in this session,** so per-step progress was not posted there; these sections follow the
   prompt's steps in order.

## For Chase

Nothing to do; the Golem keeps running. What changed: a session the Golem (or your Wake) opens while it is resting is
no longer closed the moment it starts, and closing finished sessions is switched back on.

## Repo size rule

No file over 5 MB in either repo. The only repo changes are two lines of `CHANGELOG.md` and `VERSION` in
ShatteredLegacy, and this note. The Golem files live outside both repos. Test logs and mutation copies stayed in the
session scratchpad.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun` (after `tools/progress.py`):

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

Code: `CHANGELOG.md`, `VERSION`. Docs: this note, `README.md`, `dashboard.html`, `tools\progress.json`, and the
importer's `testing\SUMMARY.md` and `testing\play-tests.json` (machine output, refreshed from Haven by the dry run).
Nothing BLOCKED. The Golem's own files are outside every repo the script commits.

P174 DONE
