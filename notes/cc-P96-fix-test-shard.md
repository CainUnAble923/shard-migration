# cc-P96: "Fix test shard" on the Shard Console

2026-10-14. Console code, the test-shard deploy script and its compose file, in `D:\ShatteredLegacy`. Live
(`sl-modernuo`) was never started, stopped, restarted or rebuilt (checked at the end, see "Live untouched").

## Headlines

- **Part A, health. Proven both ways on the real test shard.** `docker-compose.test.yml` now has a Docker health
  check: healthy only when the kernel's socket table shows LISTEN on 2594. Started on this morning's broken image, the
  shard crashed at start and Docker read **`Up 2 minutes (unhealthy)`**. Started on HEAD (P95's fix), it read
  **`Up 46 seconds (healthy)`**. The tile says **`TEST : CRASHED AT START  Known bug D89. IndexOutOfRangeException ...`**
  in red against real Docker. `Check-Shard.ps1` prints and writes the health line.
- **Part B, the Fix test shard tab.** Diagnose, Restart, Roll back to last good, Rebuild a commit, Prune images. The four
  that change anything ask for a typed phrase, log what they ran, and honour `-DryRun`. **Run for real on the test shard:**
  Diagnose (named D89), Roll back (backed up the 28 MB save, verified, came up healthy), Restart (healthy). Rebuild and
  Prune were run for real only through `Start-TestShard.ps1 -Commit`, and as `-DryRun` against real Docker. **Prune
  removed nothing:** it offers 85 of 92 tags, at least 7.2 GB and up to 100.4 GB, which is Chase's call.
- **Part C, good tags. Proven.** After a healthy start `Start-TestShard.ps1` tags `sl-modernuo:good-<commit>`, from a
  new `sl.commit` label that `build.sh` puts on the image. Real runs: `healthy: tagged sl-modernuo:good-61db33c` (a
  `-Commit` build) and `healthy: tagged sl-modernuo:good-61db33c-dirty` (a working-tree build: `[label]
  sl.commit=61db33c... sl.dirty=1`). On a crash it tags nothing, prints the headline and exits 1.
- **The test shard is up again**, healthy on `sl-modernuo:good-61db33c` (HEAD with P95's fix). That was this morning's
  outage.
- **Facts: 244, all green** in the final run (225 before, 19 new; one existing fact changed for the new tab, one for a
  tab index). Each new fact was seen failing first. All 19 new facts and the changed tab-order fact failed before the
  console changes. Three facts were also watched catching a deliberate break of the behaviour they guard. Detail under
  Tests.

## What changed, with file:line

`D:\ShatteredLegacy`:

| File | What |
|---|---|
| `scripts/Shard-Health.ps1` (new) | The pure judgments both the console and `Start-TestShard.ps1` use: `Get-CrashReport` (:29), `Find-KnownCrash` (:79), `Get-HealthState` (:90), `Get-GoodTag`/`Get-GoodTagCommit` (:113, :122), `Get-LastGoodImage` (:129), `ConvertFrom-ImageSize` (:135), `Get-PruneSet` (:144), `Test-SaveNewerThanImage` (:185). |
| `scripts/fix-test-shard.json` (new) | The config: `knownCrashes` (signature to D-number; starts with `ImbueCatalogue..cctor` = D89), `keepGood` (5), `keepTags` ([]). |
| `docker/uo/docker-compose.test.yml` | `image: ${SL_TEST_IMAGE:-sl-modernuo:latest}` (:33), so a rollback runs a good tag without moving `latest`; the `healthcheck` (:62). |
| `docker/uo/build.sh` | Step 3 labels the image `sl.commit` and `sl.dirty` (:132-133). Labels only: no layer, no gate changed. |
| `docker/uo/Start-TestShard.ps1` | `-Image <sl-modernuo:tag>` and `-Commit <hash>` (:146: a detached worktree in `D:\UO\test-shard-src`, outside the repo, as the overnight bot does); the wait is now healthy-or-crashed (:193); Part C tags good and writes `server\lib\uo\modernuo-test\shard-commit.json` (:240, :271). |
| `Check-Shard.ps1` | A HEALTH section first (:13), with the crash's frames. |
| `scripts/Shard-Console.ps1` | Dot-sources Shard-Health (:157). The five actions (:864); `ConvertFrom-FixConfig` (:1766), `ConvertFrom-DockerDfImages` (:1797), `Get-FixDiagnosis` (:1819), `Get-FixPlan` (:1879); the safety check's one `docker rmi` shape (:2192) and `healthwait` only on the test container; the tile (`Get-ShardGlance`, :2604); `Get-FixFacts` (:4055), `Wait-TestShardHealth` (:4089), the `healthwait` step (:4527), `Show-CommitPicker` (:5818), the tab (:6364). Container health, image labels and image sizes are now parsed. |
| `scripts/tests/Shard-Console.Tests.ps1` | 19 facts (`P96_*`), `SL_FACT_FILTER` to run a subset, the Diagnostics tab found by name. |
| `scripts/tests/fixtures/` | 7 real captures, below. |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.3, one `### Staff` line. |

### The safety rules, as they now stand

- `docker rmi` is the one removal: one `sl-modernuo:<tag>` per step, never `-f` (so Docker itself refuses to remove an
  image a container uses), never `latest`, `rollback-*`, `pre-bump-*` or a `keepTags` tag. It needs the typed phrase,
  and the plan may name nothing live. Everything else on the forbidden list is unchanged.
- Prune never lists anything outside `sl-modernuo:`, so `uo-modernuo` (live's image name) cannot be offered. It also
  keeps every tag on the image the live or the test container runs.
- Rollback and Rebuild reach compose only through `Start-TestShard.ps1`, as every test action already did.

## How each button works

- **Diagnose** reads the following, then prints and logs. It changes nothing and asks for no phrase:
  - status and uptime;
  - health: Docker's check plus the log, and a crash outranks "starting";
  - image tags, id, build time and commit (from the label, or from a good tag);
  - the last good image;
  - which commit last wrote the save;
  - for a crash: the innermost type and message, the exception chain, the first 5 frames and the known bug.
- **Restart** (`restart test`): `docker restart -t 60 sl-modernuo-test`, then waits up to 300 s for healthy, and stops
  with the reason on a crash, unhealthy or a timeout.
- **Roll back to last good** (`roll back test`) runs these steps:
  1. `Start-TestShard.ps1 -Down`, then checks the container stopped.
  2. Copies the test save to `Snapshots\test\<time>_pre-rollback-<commit>` and verifies the copy. The path is in the
     confirmation text.
  3. Runs `Start-TestShard.ps1 -Image sl-modernuo:good-<commit>`.

  It warns when `shard-commit.json` names a newer commit than the image (`git merge-base --is-ancestor`), and says so
  when that is unknown.
- **Rebuild a commit** (`rebuild test`): a picker of HEAD, the last 15 commits and the last good commit. Then
  `Start-TestShard.ps1 -Commit <hash>`: it builds through `build.sh`'s gates in the worktree, tags `test-<commit>`,
  starts on it and waits for healthy or a crash.
- **Prune images** (`prune images`): lists each kept tag with its reason, and one `docker rmi` per removed tag. The space
  is given as a range: at least the removed images' unique sizes (`docker system df -v`), up to their full sizes.

## Tests (each new one seen failing first)

Runner: `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1`.

- **Baseline** before any change: `225 facts, 225 passed, 0 failed`.
- **Red**, with the 19 facts added and the console unchanged: `244 facts, 224 passed, 20 failed`. The 20 were the 19
  `P96_*` facts and `TheFormBuildsFromACaptureWithoutBeingShown`, whose tab list now includes Fix test shard.
- **First green attempt:** 237 of 244. The failures and their causes:
  - My local `$fixFacts` hid the click harness's `$FixFacts` through dynamic scope, since names ignore case. Renamed.
  - The new tab had no tooltip.
  - P86's fact found the Diagnostics tab by index 3. It now finds it by name.
  - One of my facts assumed a line number in the fixture.
- **Green:** `244 facts, 244 passed, 0 failed` (final run, after every change).
- **Watched failing on purpose.** Three behaviours broken by hand, then restored:
  - Prune ignoring the images containers run: the prune fact failed with `kept: same-as-live`.
  - The tile ignoring a crash: `expected [CRASHED AT START] but got [STARTING?]`, which is exactly what the console
    showed before this change.
  - A `docker rmi` allowed without the phrase: `refused without the phrase`.

  All three went red, and green again once restored.

The facts by what the prompt asked:

| Asked | Fact(s) |
|---|---|
| health parsing: listening, crashed, starting | `P96_HealthReadsListeningCrashedAndStarting`, `P96_TheRealInspectsGiveTheHealthDockerReported` (real healthy, unhealthy and pre-P96 inspects) |
| crash headline from this morning's D89 log | `P96_TheD89LogGivesItsInnermostExceptionAndFirstFiveFrames`, `P96_AHealthyStartIsNoCrashAndACrashAfterListeningIsNotAtStart` |
| known-bug matching | `P96_KnownBugD89IsMatchedFromTheConfigTable` |
| last-good selection | `P96_LastGoodIsTheNewestGoodTag` |
| prune keep-list (live image and uo-modernuo never listed) | `P96_PruneKeepsLatestGoodRollbackPreBumpNamedAndWhatContainersRun`, `P96_PrunePlanRemovesTagsOneByOneAfterThePhrase`, `P96_TheSafetyCheckAllowsOnlyAConfirmedRmiOfOneSlModernuoTag` |
| backup before rollback | `P96_RollbackBacksUpTheTestSaveBeforeItRunsTheLastGoodImage`, `P96_RollbackWarnsWhenTheSaveIsNewerThanTheImage`, `P96_RollbackRefusesWithNoGoodImage` |
| -DryRun for each button | `P96_EveryFixButtonClickedDryPrintsItsPlanAndRunsNothing` (the click path), `P96_EveryFixButtonRunHeadlessWithDryRunRunsNothing` (the real child process, all five), plus the existing all-window-action facts, which now include the four |
| the tile | `P96_TheTestTileSaysCrashedAtStartInRedWithTheKnownBug` |
| also | `P96_DiagnoseShows...`, `P96_RebuildBuildsAPickedCommitAndRefusesOthers`, `P96_RestartRestartsOnlyTheTestContainerAfterThePhraseThenWaits`, `P96_EveryFixButtonHasAPhraseExceptDiagnoseAndIsOnItsOwnTab` |

**Fixtures (all real, `scripts/tests/fixtures/`):**
- `test-shard-crash-d89-2026-10-14.txt`: the test container's own 07:07 log. The one line naming accounts was dropped
  with the console's `Remove-AccountLines`.
- `test-shard-start-healthy-2026-10-14.txt`: the bot's scratch shard on the P95 fix, up to its listeners. Account lines
  were dropped; its AccountWipe lines are counts only.
- `test-shard-inspect-{exited,unhealthy,healthy}-2026-10-14.json`: the test container's inspect at three moments.
- `docker-images-sl-modernuo-2026-10-14.txt`: the image listing, with sizes.
- `docker-system-df-images-2026-10-14.json`: trimmed to the 89 `sl-modernuo` rows. The other 70 rows, from 19 other
  repositories on this PC, were dropped because the repo is public.

**Not covered by a fact:** `Start-TestShard.ps1` itself (it needs Docker). It was proven by the real runs below instead.

## Real runs on the test shard (live untouched)

1. **Crash, Part A and C:** `Start-TestShard.ps1 -Image sl-modernuo:latest` (the 07:07 build) printed:

   ```
   THE TEST SHARD CRASHED AT START. Nothing was tagged good.
   IndexOutOfRangeException: Index was outside the bounds of the array. at Server.ImbueCatalogue.SkillRowName(SkillName skill)
   ```

   It showed five frames and exited 1. Polled after that: `08:34:16 running unhealthy`, and docker ps showed
   `sl-modernuo-test Up 2 minutes (unhealthy)`.
2. **Healthy, Part A and C:** `Start-TestShard.ps1 -Commit 61db33c` built in the worktree, then:
   - `docker ps` showed `sl-modernuo-test sl-modernuo:test-61db33c Up 46 seconds (healthy)`;
   - `good-61db33c` was tagged on `527ac64a2177`;
   - `shard-commit.json` was written.

   The health command inside the container is `awk '$4=="0A" && $2 ~ /:0A22$/ {f=1} END {exit !f}' /proc/net/tcp
   /proc/net/tcp6` (from inspect).
3. **Label path:** a plain `Start-TestShard.ps1` (working tree) printed `[label] sl.commit=61db33c5e527...
   sl.dirty=1`, then `healthy: tagged sl-modernuo:good-61db33c-dirty`.
4. **End to end, this morning's scenario replayed:**
   - `Start-TestShard.ps1 -Image sl-modernuo:cc-p82` crashed at start.
   - `Shard-Console.ps1 -Status` showed `TEST : CRASHED AT START  Known bug D89. ...`.
   - `-Mode Execute -Action fix.diagnose` printed the crash, the chain, five frames and
     `Known bug D89: the Imbuing catalogue read the skill table before SkillsInfo.Configure filled it; fixed by cc-P95.`
   - `-Action fix.rollback -ConfirmLive 'roll back test'` ran `-Down`, the stop check, the copy and verify of the save to
     `Snapshots\test\20261014-085953_pre-rollback-61db33c`, then `-Image sl-modernuo:good-61db33c`, and came up healthy.
   - `-Action fix.restart -ConfirmLive 'restart test'` ended `HEALTHY: listening on its game port (docker health check)`.
5. **Dry runs against real Docker:**
   - `fix.prune`: "removes 85 sl-modernuo tags and keeps 7, freeing at least 7.2 GB (layers only those images use) and
     up to 100.4 GB". It keeps `test-61db33c` (a container runs it), `good-61db33c`, `good-61db33c-dirty`, `latest`, two
     `pre-bump-*` and `rollback-live-20260927`.
   - `fix.rebuild -Commit HEAD`: `Start-TestShard.ps1 -Commit 61db33c5e527...`.

**Gate on the final tree:** `build.sh -t sl-modernuo:cc-p96 --tests-only`: `Total tests: 1135, Passed: 1135` (CHANGELOG and VERSION parse; the label build ran its own 1,135 earlier).

## Live untouched

`docker inspect sl-modernuo` at the end: running, started `2026-10-14T13:06:06.981602409Z`, image `uo-modernuo`
(`bc04a35bf344`). That is the same start time and image the P95 bot run recorded at 08:17, before this task began. The
console log `scripts\shard-console.log` shows only `fix.*` actions on `shard=test` today. Nothing was run against
live; the only reads were `docker inspect` and `docker images`.

## Deviations and decisions for Chase

- **Rollback runs the good image through `SL_TEST_IMAGE`; it does not move `latest`.** Deploy built image moves
  `latest`, and on 2026-10-05 the console's own deploy line noted that the next live recreate would pick up whatever
  `latest` is. Rollback stays out of that. The next plain Start or Start fresh goes back to `latest`.
- **Rebuild builds a commit, not the working tree.** It runs `Start-TestShard.ps1 -Commit` in `D:\UO\test-shard-src`, as
  the overnight bot does, so a picked commit is exactly that commit. The Test shard tab's "Rebuild through the gates and
  start" still builds the working tree.
- **A commit from before this change has no `sl.commit` label**, because its own `build.sh` writes none. Two fallbacks
  cover it:
  - `-Commit` uses the commit it was asked to build.
  - `-Image good-<c>` uses the commit in the tag.

  Diagnose says "commit unknown" for older images such as `cc-p82`.
- **"Last good" is the newest `good-*` by Docker's image creation time.** A fully cached rebuild keeps the older time:
  today `good-61db33c-dirty` shows 08:19 and `good-61db33c` 08:38, so Roll back picks `good-61db33c`. Both are 61db33c.
  Docker keeps no tag times, so a "most recently proven healthy" order would need a history file. I did not add one.
- **Diagnose asks for no phrase.** The prompt says every action confirms. Diagnose only reads, so it prints and logs like
  the existing read-only buttons; the four that change anything ask.
- **The health check reads `/proc/net/tcp` rather than connecting.** A connection every 10 s would be a login attempt in
  the shard's log. The start period is 120 s, so a crashed shard reads "starting" until then. The console and
  `Start-TestShard.ps1` read the crash from the log right away; Docker's own word turns unhealthy at about 2.5 minutes.
- **Restart waits for health.** The prompt only said restart; waiting tells you at once whether it helped.
- **Prune states the space as a range** rather than one number. Docker's image sizes count every shared layer again, so
  their sum (100.4 GB) badly overstates what would be freed.
- **Not built as part of Part B:** the "show which" wait for Rebuild is `Start-TestShard.ps1`'s, so its output goes to
  the action's window (or the output pane), not into a console status line.

## For Chase

The next time the test shard will not start:
1. Shard Console, **Fix test shard** tab, **Diagnose**. It names the crash and any known bug.
2. **Roll back to last good**, type `roll back test`. The save is backed up first, and the path is shown.
3. When a fix lands, use **Rebuild a commit**, pick it, and type `rebuild test`.
4. To add a known crash, put a line of its stack and its D-number in `scripts\fix-test-shard.json`.

One-time, and optional: **Prune images** would free at least 7.2 GB. The `sl-uo-builder:*` images are not in it:
each holds about 3.45 GB of its own (`docker system df -v`), and they may be the bigger saving, by hand. Nothing else to
run: the compose change took effect at the restarts above.

Repo size and the commit preflight are below.

## Commit preflight

No file over 5 MB: the largest new files are the fixtures, at most 26 KB (`docker-system-df-images`, trimmed), and
`Shard-Console.ps1` is under 500 KB. Scratch (logs, edit scripts) stayed in the session scratchpad, outside both repos.
The rollback's save backup is under `server\lib\` (ignored), and the worktree `D:\UO\test-shard-src` is outside both
repos.

`Commit-ShardWork.ps1 -DryRun`: code has 17 files pending (the table above plus the 7 fixtures), docs has 1 (this note).

```
Repo Result
---- ------
code dry run
docs dry run
```

P96 DONE
