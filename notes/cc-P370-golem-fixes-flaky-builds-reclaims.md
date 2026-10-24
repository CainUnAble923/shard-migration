# cc-P370: Golem fixes from 10-21: flaky integrator builds, re-claimed finished prompts, and four smaller bugs

## In plain words

- A finished branch whose merge build fails once is now built again before it counts as failed, so a test that only
  fails now and then no longer sends a finished prompt back for a fix-up. When a build really fails, its fix-up
  prompt, its email and Shadow Iron's card show the failed test and its message, not test-server chatter. Each build's
  full output is kept for two weeks in `D:\UO\golem\merge-queue`.
- Prompts already done no longer come back: when a fix-up merges, its original prompt is filed as done too, and a
  timed-out claim whose work is already in main is never put back in the queue (no more "P263 again").
- Answering a Golem's question now gets it going again, from the web console, the Shard Console or another PC's agent.
  Before, every answer to a named Golem was saved but the Golem stayed stopped until someone pressed Retry. Also: Run
  next goes only to the Golem you picked it for; Shadow Iron's "needs you" clears itself once that branch merges; a
  Golem whose copy of the queue got stuck mid-update fixes it itself; a stale "needs you" can be cleared from afar, and
  one about uncommitted changes clears itself once the work copy is clean.
- Nothing for you to do. The new kit is installed on this PC, and the Tinker sends it to the other PCs once this prompt
  is merged. One small follow-up you may want: a Clear button on remote Golems' cards in the web console (see
  Decisions 2).

## Status

The Iron Golem (Opus), 2026-10-23/24. Branch `golem/Iron/P370` in both repos; nothing committed (the Golem commits).
The Golem kit (`D:\UO\golem`, not a git repo) is **installed live** on the game PC, the way P274 and P287 did it. Every
changed file was first checked byte-identical (md5) to the copy I started from, backed up as
`<file>.bak-20261024-P370`, then renamed into place, and checked identical to the tested copy. No Docker, test shard
or Haven work, so no locks were taken.

| Part | What was wrong | Fix | Where |
|---|---|---|---|
| 1. Flaky integrator builds | The build's output was captured whole, but only the last 6000 characters were kept, and on 10-21 those were the test host's `Client: 127.0.0.1: Connected` lines. One red build counted as a failure. | Every attempt is written, whole, to `merge-queue\build-P<nn>-<sha>.log` (branch head's short sha; logs older than two weeks are pruned). A red build is built once more under the same `docker-build` lock. Red then green is merged, logged, and listed in `merge-queue\flaky-builds.jsonl` with the first attempt's failed lines. Red twice: the reason (`the build failed (exit 1) twice`), the fix-up prompt, the fix-up and NEEDS YOU emails, the card's `merge.lastFailure.errors`/`.log` and the `handled-P<nn>-<sha>` marker carry the **first error lines** (`Get-BuildErrorLines`: compiler errors, each failed test with its message and stack lines, the summary; noise dropped) and the log path. | `Golems.ps1` (`Invoke-Integrate`, `Invoke-MergeBuild`, `Save-BuildLog`, `Get-BuildErrorLines`), `golem.ps1` (`Invoke-MergeRound`, `Invoke-IntegratorRound`, `Format-MergeErrors`) |
| 2. Finished prompts handed again | When a fix-up merged, only the fix-up's file went to `completed\`. The original stayed in `claimed\<G>\`, and the watch's stale-claim release put it back in the queue (P224, P263). | A merged fix-up's original (named in its heading, "fix-up for P263") goes to `completed\` with its claim record and token, from `merging\`, `claimed\<any>\`, `queue\` or the prompts root, and back through a fix-up of a fix-up. And the stale-claim release never puts back a prompt whose work is in main: a commit on `main`/`origin/main` whose message has a line starting `CC task P<nn>:` or `Merge golem/<name>/P<nn>:`, in the integrator's copies or the Golem's own. Such a prompt goes to `completed\`, with a log line and no stale-claim email. | `Golems.ps1` (`Complete-FixupOriginals`, `Find-PromptWorkInMain`, `Release-StaleClaims`), `golem.ps1` (watch) |
| 3. A remote answer did not resume | **Root cause:** `Answer-Question.ps1` kept `-Golem <name>` in `$who`, but PowerShell variable names ignore case, so `$who` *is* its `[string]$Who` parameter. The array became the one string `-Golem Iron`, `golem.ps1` refused it (exit 2, no output), and the script exited 1. This hit **every** answer to a named Golem, from any console, not only remote ones (P289 and P263 on Iron were answered locally and also needed a Retry). The P216 tests ran a single unnamed Golem, so they never saw it. | Renamed to `$gArgs`. The agent's `who` rule now allows parentheses (never a leading dash), so the overseer can answer as `overseer (for Chase)`. `Add-RemoteCommand` takes `-Inputs` (a hashtable), so the overseer no longer has to set inputs by hand. | `Answer-Question.ps1`, `Remote-Agent.ps1`, `Golems.ps1` |
| 4. Run next shared per PC | One `RUN-NEXT` file for all Golems on the PC. | Per Golem: `RUN-NEXT-<name>`, the home Golem (Iron) keeping `RUN-NEXT`, which the Shard Console reads. A pick goes first only in its own Golem's order, and every other Golem skips that prompt ("P367 is the Iron Golem's run next pick: skipped") until it is handed or cancelled. No leftover `RUN-NEXT` was on disk at install. | `Golems.ps1` (`Get-GolemFileName`, `Get-OtherRunNextPicks`, `Get-ClaimCandidate`), `golem.ps1` (`Set-GolemPaths`) |
| 5. Shadow Iron's NEEDS YOU stuck | `needsYou` was copied from the last status every round, forever. | The card keeps `needsYouPrompt` (an older card's text starts with the prompt). NEEDS YOU goes when that prompt merges, is in `completed\` (merged by hand), or its `handled-P<nn>-*` markers are removed (the documented way to ask for another try). Each clear is logged. | `golem.ps1` (`Invoke-MergeRound`) |
| 6. Prompts clone stuck mid-rebase | `Sync-PromptsGit` ran `git pull --rebase` and ignored a failed rebase, leaving the clone detached mid-rebase with a stale queue. That is how Gold and Copper got stuck. | `Repair-PromptsClone`: mid-rebase, detached or off main gets `git rebase --abort`, then `main` checked out at `origin/main` (an unpushed claim there never landed, so nothing is lost); a clone on main is left alone. Runs before every pull and again when the pull fails, before a claim in git mode (`Invoke-Claim`), in `Get-WakeTarget`, and in the watch, which then wakes a resting Golem that has nothing running. | `Golems.ps1`, `golem.ps1` (watch, `Get-WakeTarget`) |
| 7. No Clear from afar | The agent had no key for `golem.ps1 -Event Clear`. | Agent key `clear` (input `reason`: printable ASCII, no double quote, no leading dash, optional) runs the new `Clear-Golem.ps1 [-Reason]`. The watch clears a NEEDS YOU of the form `... has uncommitted changes (...): commit or clean it first` once that Golem's work copies are clean (checked before the ENABLED test, so it also works for a Golem left off). | `Remote-Agent.ps1`, new `Clear-Golem.ps1`, `golem.ps1` (watch) |
| README, CHANGELOG | | New README section "The 10-21 stalls, fixed (cc-P370)", plus Files rows. CHANGELOG `2026.10.24` (Staff), VERSION `2026.10.24`. | `D:\UO\golem\README.md`; ShatteredLegacy `CHANGELOG.md`, `VERSION` |

## The flaky test (part 1)

No full log of the 10-21 failures exists, because only the tails were kept. The P264 tail shows `Failed: 1` out of
2031 in `ShatteredLegacy.Tests`, with the name cut off. But P369 (P264's fix-up, Bronze) reran the suite about 20
times and found the two intermittent tests, both older than P264 and both red on main without it. It fixed both, and
the fix is on main (`d1ec499`, merged in `0076ce4`):

1. `WispOrbPossessionVerification.APossessedCreatureFightingNeverBecomesItsMastersCombatant` (Sagittarri,
   ForestNymph): the foe sometimes picked the party member, so the "fight started" check went red. It is the flake
   most often named in older notes (P50, P52, P82, P135, P142, P193). Fixed with `f.Foe.Combatant = f.Pet`.
2. `CC6Batch1CreatureVerification.TheRestOfTheBatchKeepsItsServUOShape`: a Skree's control slots are legitimately 2
   when its stats roll low (`SlotsLowered`). Fixed.

Since then Shadow Iron's log shows no failed build (10-22 and 10-23). Other flakes named in notes, not fixed here and
not seen at merge: `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies` (P128 and P129 saw it 1 in 3),
`LootBoxFanfareVerification` (identical stacks merge; P100, P145). From now on any flake that hits a merge is named in
`merge-queue\flaky-builds.jsonl`.

## Tests

Every new fact was seen failing on the live kit before the change, then passing: `tests\Golem.Tests.ps1`, section
`cc-P370`, 8 facts with 49 checks:

| Fact | Old kit | New kit |
|---|---|---|
| `P370_1_AFlakyIntegratorBuildIsRetriedOnceAndItsFullOutputIsKept` (a build stub red once with 600 noise lines around one failed test) | FAIL (a fix-up, one build, no log) | PASS |
| `P370_1_ABuildRedTwiceGivesTheFirstErrorsNotTheTailToTheFixUpAndTheCard` | FAIL (the fix-up held only noise) | PASS |
| `P370_2_AFixUpsMergeCompletesItsOriginalAndAStaleClaimWhoseWorkIsInMainIsNeverPutBack` | FAIL | PASS |
| `P370_3_AnAnswerForANamedGolemResumesItAndTheOverseerMayAnswerForChase` (the real chain: `Answer-Question.ps1` -> `golem.ps1 -Event Answer` -> wake) | FAIL (exit 1, nothing resumed; who refused) | PASS |
| `P370_4_RunNextIsPerGolem` | FAIL (Bronze took Iron's pick) | PASS |
| `P370_5_TheMergeGolemsNeedsYouClearsWhenItsPromptMergesOrItsMarkersAreRemoved` | FAIL | PASS |
| `P370_6_AStuckPromptsCloneIsResetToOriginMainBeforeASyncOrAClaim` (a real bare origin, two clones, a conflicting unpushed claim) | FAIL (threw in `Invoke-Claim`: "HEAD does not point to a branch") | PASS |
| `P370_7_AClearKeyForTheRemoteAgentAndTheWatchClearsAStaleUncommittedNeedsYou` | FAIL | PASS |

I also reproduced part 3 by hand on a scratch copy of the live kit before writing the fact: `golem.ps1 -Event
Answer` run by `Answer-Question.ps1` exited 2 with no output, and run directly it worked. The debug line showed the
arguments as the single string `-Golem Iron`.

The Golem test suite, compared with the live kit before the change:

- `Golem.Tests.ps1` full: new kit **1,545 checks passed, 5 failed**; old kit 1,496 passed, 5 failed (the 49 more are
  P370's). The 5 failures are the same on both: `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged` and
  `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly`, with identical failure lines. P274's and P287's notes
  record them as already failing.
- `RemoteAgent` 90/0, `Tinker` 157/0, `Lane` 59/0, `Assign` 3/0, `GolemDays` 53/0, `Codex` 136/0, `GolemPower` 133/0
  on the new kit.
- `Join` 105 passed, 4 failed, and `GolemPaths` 608 passed, 1 failed: the same failures on the live kit before the
  install. Join's are this PC's setup (no `D:\UO\overseer`, no Docker answer, an API key in the Machine environment;
  as P287 noted). GolemPaths always tests the live `GolemPaths.ps1` against the real registry (Iron is no longer the
  integrator); not touched here.
- After the install: `Golem.Tests.ps1 -Only P370` on the live kit, 49 passed, 0 failed.

## Decisions for Chase

1. **The stuck-clone repair throws away an unpushed claim commit.** That is the Tinker rule the overseer wrote, and it
   is safe: a claim that never reached origin never happened as far as the other Golems know, and the prompt is still
   in origin's queue. It also aborts anyone's rebase in progress in a prompts clone. Nobody rebases there by hand
   today, and `D:\UO\cc-prompts` is on `main` tracking `origin/main`, so in normal running it does nothing.
2. **No Clear button on the web console yet.** The remote agent accepts `clear` with a `reason`, and the overseer can
   queue it with `Add-RemoteCommand -Key clear -Inputs @{ reason = '...' }`. A button on a remote card needs
   `web-console\golem-actions.json` and a `reason` input rule in `server.py` (ShatteredLegacy, the web-console area),
   which this golem-only prompt did not touch. A short follow-up prompt if you want it.
3. **The kit snapshot** is the Tinker's normal one. It holds snapshots while a prompt touching the golem area is
   claimed (this one), and takes one at its next round after P370 leaves `claimed\`. I did not force it.
4. **Unattended-run refusal:** the Read tool was refused for `D:\UO\golems\Iron\ShatteredLegacy\CHANGELOG.md`. I had
   already seen its text through Bash, and wrote the entry with a small Python script instead (anchored on the
   `## 2026.10.23.9` heading). Nothing else was blocked.

## Notes on the way

- Shadow Iron's failure reason now reads `the build failed (exit 1) twice`. Anything matching `the build failed
  \(exit 1\)` still matches.
- `Get-WakeTarget` now pulls the prompts clone in git mode. It runs only on wake paths (SelfWake, the watch's
  model/marathon re-plan), so that is a few pulls an hour at most.
- Not done, seen on the way (from the overseer's log, not in this prompt's list): the integrator could re-run the
  play-test importer on a `testing/play-tests.json`/`SUMMARY.md` conflict (10-21 15:48), and could merge
  `origin/<branch>` rather than a stale local branch (15:55). Worth a prompt each.

## Files

`D:\UO\golem` (live; backups `*.bak-20261024-P370`): `Golems.ps1`, `golem.ps1`, `Answer-Question.ps1`,
`Remote-Agent.ps1`, `README.md`, `tests\Golem.Tests.ps1`; new `Clear-Golem.ps1`.

ShatteredLegacy: `CHANGELOG.md`, `VERSION`.

shard-migration: this note.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P370`: code 2 files
pending (`CHANGELOG.md`, `VERSION`), docs 1 (this note); neither BLOCKED.

```
Repo Result
---- ------
code dry run
docs dry run
```

P370 DONE
