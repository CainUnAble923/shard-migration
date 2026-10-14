# cc-P108: Retire the live shard (greyed on the console, silent everywhere, test shard only)

2026-10-14. Prompt: `D:\UO\cc-prompts\cc-P108-retire-live.md`. Cleanup across `D:\ShatteredLegacy` scripts, compose files
and tests. Nothing named live was started, created or recreated.

## Headlines

- **One switch: `D:\ShatteredLegacy\scripts\live.json`, `"liveEnabled": false`**, read by one function,
  `Get-LiveSwitch` in the new `scripts\Live-Switch.ps1`. Used by the Shard Console, `Deploy-StatusPublisher.ps1`,
  `Publish-PatchNotes.ps1`, `Publish-GamePcSnapshot.ps1` and `docker\uo-status\Start-UoStatus.ps1` (which passes it to
  the probe as `SL_LIVE_ENABLED`). A missing or broken file, or a non-boolean value, reads as **retired** and says
  why: the safe side is never to touch live by accident.
- **Console, false:** one grey `LIVE: RETIRED` tile reading `retired 2026-10-14 (returns as a fresh 1.0 world)`. No
  docker read of `sl-modernuo`, no logs, no save or snapshot listing, no health line, no question, no email, no
  compose warning, no `== LIVE shard` section in `-Status`. Every live button is greyed and disabled with the tooltip
  `Live is retired: ...`, and so are the LIVE choices on Shard question and Snapshots (the test shard is picked).
  Every live action, from a button or `-Action`, refuses with `Live is retired (...)` before anything is read.
- **Console, true:** today's behaviour, unchanged. Every pre-P108 fact now runs with `liveEnabled` pinned true and
  passes, which is the proof.
- **Compose:** live's service moved out of `docker\uo\docker-compose.yml` into
  `docker\uo\retired\docker-compose.live.yml`, under `x-retired-live:` instead of `services:`, so compose finds **no
  service** there (proved: `docker compose -f retired/docker-compose.live.yml config --services` prints nothing). The
  old file was **not** moved whole: it also holds `sl-ddns`, the public DNS updater, which is running and stays. It now
  holds only `ddns-updater` (proved: `config --services` prints `ddns-updater`). So `docker compose up` in `docker\uo`,
  and `scripts\sl.ps1 up uo` (which adds `--build`), can no longer build an ungated image or recreate `sl-modernuo`.
- **Probe:** `shards.json` lists the test shard only (before: live listed as `"up": false`, which is "live is down").
  Recreated `sl-uo-status` and `sl-shard-probe` with `Start-UoStatus.ps1`; nothing else touched.
- **Test shard:** restarted healthy on the image it already ran (`-Down`, then `-Image sl-modernuo:good-61db33c`), same
  image id `527ac64a2177` before and after.
- **One test-shard button is now greyed too: Start fresh.** It seeded the new world's accounts from the live save,
  which the overseer deleted. Without them a new world blocks at the owner account prompt for ever (D19). It refuses
  and says to use Wipe test accounts. **Decision for Chase below.**
- Tests: **289 facts before, 302 after** (13 new `P108_*`, each seen failing against a mutant first). Numbers below.

## Every place that knew about live, before any change

Pattern `sl-modernuo([^-]|$)|uo-modernuo|2593|\blive\b|LIVE|Live|modernuo[\\/]Saves` over the 142 tracked text files
of `D:\ShatteredLegacy` outside `server/customizations`, `server/patches`, `client`, `branding`, `design`: **717
lines in 58 files**. Counted, not estimated; the overseer's "about 173 in Shard-Console.ps1, Check-Shard.ps1 and
Shard-Health.ps1" used a different pattern: mine finds 205 + 2 + 10 = 217 in those three, and `Check-Shard.ps1` has
only 2 (it was not a big one). shard-migration itself has no live-touching scripts (`tools/opsmirror.py`,
`tools/opsdata.py`: 0 hits).

Grouped by what the hit is:

| Group | Files (hits) |
|---|---|
| **Console and its tests** (live tile, buttons, actions, question, snapshots, deploy line, compose warning) | `scripts/Shard-Console.ps1` 205, `scripts/tests/Shard-Console.Tests.ps1` 251, `scripts/Shard-Health.ps1` 10, `scripts/fix-test-shard.json` 1 |
| **Deploys or publishes to live** | `scripts/Deploy-StatusPublisher.ps1` 11, `scripts/Publish-PatchNotes.ps1` 1, `scripts/Publish-GamePcSnapshot.ps1` 1 |
| **Status feed, probe, website, dashboard** | `docker/uo-status/probe.py` 1, `docker-compose.yml` 1, `Start-UoStatus.ps1` 1, `README.md` 3; `docker/website/html/index.html` 3, `migration.html` 3; `docker/dashboard/config/services.yaml` 5 |
| **Live compose** | `docker/uo/docker-compose.yml` 5 |
| **Test-shard isolation guards that name live in order to avoid it** | `docker/uo/docker-compose.test.yml` 16, `Start-TestShard.ps1` 24, `test-shard.sh` 18; `tools/playtest-bot/*` 31 (`Run-OvernightPlaytests.ps1` 10, `tests/test_bot.py` 7, `docker-compose.bot.yml` 4, `README.md` 4, `uobot/safety.py` 3, `report.py` 2, `notify.py` 1) |
| **The `sl-modernuo:*` image repository, which the test shard and the bot run from** | `Check-Docker.ps1` 2, `Check-Shard.ps1` 2, `docker/uo/build.sh` 4, fixtures `test-shard-inspect-*-2026-10-14.json` 6, `docker-system-df-images-2026-10-14.json` 1 |
| **Player package (points players at 2593)** | `player-package/payload/app/Launch-Settings.ps1` 7, `Play.ps1` 5, `Play-Lan.bat` 1, `tests/Launch-Settings.Tests.ps1` 9 |
| **History** | `docker/uo/SERVER.md` 22, `COMMANDS.md` 1, `CHANGELOG.md` 3, `roadmap.md` 1, `docs/cloudflare-setup.md` 2, `scripts/extract-server.ps1` 1 (a backup file name), `scripts/tests/fixtures/play-tests-2026-10-12.json` 30 |
| **Overview docs** | `README.md` 6, `AGENTS.md` 3 |
| **Another meaning of "live"** ("live copy of this folder", `aria-live`, "can live apart", "cannot live inside", "live status", "live map") | `docker/wiki/README.md` 3, `docker/website/README.md` 2, `docker/proxy/README.md` 2, `docker/dashboard/README.md` 1, `docker/downloads/README.md` 1, `docker/test-queue/README.md` 1, `docker/test-queue/html/index.html` 1, `docker/uo/apply-patches.sh` 3, `docker/uo/entrypoint.sh` 1, `scripts/haven-ops.json` 2, `docker/wiki/macros/scripts/SL_Mining.py` 1, `server/razor-scripts/ClusterFMiningRadar.py` 1, `player-package/clean-test/Start-CleanTest.ps1` 1 |

The full line list is not committed (717 lines); the command above reproduces it.

## What changed, with file:line (D:\ShatteredLegacy)

**New**
- `scripts/live.json`: the switch (`liveEnabled`, `retiredOn`, `returns`).
- `scripts/Live-Switch.ps1`: `ConvertFrom-LiveSwitchJson` (pure) and `Get-LiveSwitch`. Gives `Enabled`, `Line`
  (`retired 2026-10-14 (returns as a fresh 1.0 world)`), `Refusal` and `Problem`.
- `docker/uo/retired/docker-compose.live.yml`: the old service, verbatim, under `x-retired-live:`, with a header saying
  why, when, and why it cannot run.
- `docker/uo/README.md`: the one line that live returns as a fresh 1.0 world, and what is in the folder.

**Shard Console** (`scripts/Shard-Console.ps1`)
- :174 dot-sources `Live-Switch.ps1`. :245 `Test-LiveRetired`, :251 `Test-LiveActionKey` (live.*, or a snapshot or
  question action with the LIVE shard picked).
- :257 `Get-ConsoleConfig -LiveEnabled` (overrides the file; the facts use it). :278 the live shard carries
  `Retired`. It stays in `Shards` on purpose: `Test-PlanSafety` still names `sl-modernuo` and its save, so no plan can
  touch them whatever the switch says. :291 `Config.Live` and `Config.LiveEnabled`.
- :2721 `New-ConsoleState` reads a retired shard from nothing, even when a capture has its sections; its state has
  `Retired`. :2752 no compose warning while retired.
- :2917 `Get-ShardGlance`: the grey RETIRED tile. :4134 `Format-StatusReport`: no section for a retired shard.
- :3026 `Get-QuestionMails`: no email for a retired shard.
- :2893 the status publisher: live was `status.json`'s only writer, so "no writer" is grey and says so rather than red
  (`-Status`: `STATUS PUBLISHER : NOT PUBLISHING  no status.json; live, its only writer, is retired`). The old warning
  "only the TEST container has the status folder mounted ... not live" is suppressed while retired.
- :5077 `Get-DockerSections`: a retired shard is never read (no inspect, logs, logtail, saves, snapshots, asides), and
  the compose file is not read.
- :2230 `Get-ActionPlan`: every live action refuses first, with `Config.Live.Refusal`.
- :2285 Start fresh refuses while retired (see Deviations). :1781 the deploy confirmation drops its live sentence.
  :2177 prune protects only the test shard's image while retired (live has no container).
- :5985 `Get-LiveRetiredControls` and `Set-LiveRetiredLook` grey and disable the five live buttons, Start fresh, and the
  two LIVE radio buttons, with the tooltip. :7903 called after the tooltips are set. :7410 Shard question picks the
  test shard. :7373 and :7617 the Test shard and LIVE shard tab captions say live is retired.

**Other scripts**
- `scripts/Deploy-StatusPublisher.ps1:21`: refuses (exit 2) before building anything: `Live is retired (...) ...
  deploys only to live; nothing was built or restarted.` Its live code is kept.
- `scripts/Publish-PatchNotes.ps1:25`: `-Container sl-modernuo` refuses (exit 2); the default (test) is unchanged.
- `scripts/Publish-GamePcSnapshot.ps1:50`: does not report `sl-modernuo` while retired.
- `docker/uo-status/probe.py:21`: `targets(live_enabled)`; live only when `SL_LIVE_ENABLED` is 1/true/yes. Unset is
  retired. The loop moved into `main()` under `if __name__ == "__main__"` so the facts can import it.
- `docker/uo-status/docker-compose.yml:18`: `SL_LIVE_ENABLED: ${SL_LIVE_ENABLED:-0}`. `Start-UoStatus.ps1:6` sets it
  from `live.json`, and its probe-log line says test only.
- `docker/website/html/index.html:425`, `migration.html:240`: a shard `shards.json` does not list is hidden, so the
  Live dot disappears instead of reading "unknown". **Not deployed** (see For Chase).
- `docker/dashboard/config/services.yaml:7`: "UO Server" (`sl-modernuo`, 2593) and "UO Who's Online" (`status.json`,
  which only live wrote) replaced by one "UO Test Shard" tile (`sl-modernuo-test`). The dashboard's config folder is
  bind-mounted into the running `sl-dashboard`, so Homepage picks this up on its own.
- `docker/uo/docker-compose.yml`: only `ddns-updater` now, with a header.
- `README.md`, `docker/uo-status/README.md`: the live shard row says retired; the README block says how the switch works.
- `CHANGELOG.md` 2026.10.14.14 `### Staff`, `VERSION` 2026.10.14.14 (2026.10.14.13 was committed).

## Tests

`scripts/tests/Shard-Console.Tests.ps1` (the only suite that touches anything changed here).

| | facts | passed | failed |
|---|---|---|---|
| Before, HEAD `4f13018` in a scratch worktree | 289 | 287 | 2 |
| After, the working tree `D:\ShatteredLegacy` | 302 | 301 | 1 |

After, the one failure is the same P107 scheduled-task fact. All 13 `P108_*` pass, and so does every other fact,
P60 and P106 included.

Before, the two failures are not P108's: **P107_TheSnapshotSendsNothingBeforeTheCutoverAndDryRunPrintsItsJson** asserts
that no scheduled task `SL game PC snapshot` exists, and one is now registered on this PC (Chase installed it after
P107); it fails the same way in every run here. **P60_AMessageCrossesTheChildCommandLineUnchanged** failed only because
the baseline ran from a worktree path (`...\scratchpad\head-wt\...`); it passes in `D:\ShatteredLegacy`. (A first
"before" run in the real repo was contaminated: one P106 fact starts a child process, which read my already-edited
file. That is why the clean baseline used a worktree.)

How the old facts were kept: the test file wraps `Get-ConsoleConfig` so every pre-P108 fact pins `liveEnabled` true
(`Shard-Console.Tests.ps1:64`), which is also the proof that true restores today's behaviour. One old fact had to
change: **P106_EveryQuestionButtonRunHeadlessWithDryRunRunsNothing** runs the real script in a child, which reads the
real `live.json`, so it now drives the **test** shard's question (`-Shard test`, `logtail sl-modernuo-test`); it was
live's. Nothing else was removed or weakened.

New facts (`Shard-Console.Tests.ps1:4897` on), each **seen failing first**: a mutant copy of the tree had every guard
removed (the refusal, the docker-read skip, the state skip, the report skip, the mail skip, the UI greying, the Start
fresh refusal, the probe filter, the two script refusals), `live.json` set true and the live service put back in
compose. 11 of 13 failed; the other two (the switch parser, and "true shows live as before") each failed against their
own mutation (missing file reads as enabled; the retired tile always on). Real tree: 13 of 13 pass.

1. `P108_TheRepoFileSaysLiveIsRetired`
2. `P108_TheSwitchReadsTrueAndFalseAndAnythingElseIsRetired` (null, empty, not JSON, `{}`, `"true"`, `1` all retired)
3. `P108_RetiredLiveIsOneGreyTileAndNoChecks` (the report never names `sl-modernuo` nor says live is down/unknown)
4. `P108_LiveEnabledTrueShowsLiveExactlyAsBefore`
5. `P108_ARetiredLiveIgnoresWhatACaptureSaysAboutIt` (a live docker error is not a docker error while retired)
6. `P108_EveryLiveActionRefusesWhileRetired` (all 15: five live.*, four snapshot, six question)
7. `P108_StartFreshRefusesWhileRetiredBecauseItsAccountsCameFromLive`
8. `P108_NoQuestionEmailForARetiredLive` (enabled: 1 email for live at D94; retired: 0)
9. `P108_TheDockerReadNeverNamesARetiredLive` (shims `Invoke-DockerRead`; no docker, no network)
10. `P108_TheWindowGreysEveryLiveControlAndPicksTheTestShard` (both states, 8 controls)
11. `P108_TheProbeListsTheTestShardOnlyUnlessLiveIsEnabled` (imports `probe.py` with `python -I`)
12. `P108_NothingCanComposeTheOldLiveContainer`
13. `P108_TheLiveDeployAndPublishPathsRefuseWhileRetired` (copies of the two scripts beside a false `live.json`, so no
    build or `docker exec` can happen whatever the real file says)

## Proof

**`-Status` against the real Docker** (`Shard-Console.ps1 -Status`, 15:57):

```
LIVE             : RETIRED         retired 2026-10-14 (returns as a fresh 1.0 world)
TEST             : RUNNING         up 53s, listening on :2594, healthy; OLD IMAGE
STATUS PUBLISHER : NOT PUBLISHING  no status.json; live, its only writer, is retired; feed up, nothing to serve
```

and then `== TEST shard` and `== Status publisher` only. No `== LIVE shard`, no `LIVE COMPOSE FILE`. The only lines
saying "live" are the three above. (The TEST tile's OLD IMAGE is what it said before: it runs `good-61db33c`, not
`latest`.)

**The real window**, built from the real `live.json` and the real Docker by `New-ConsoleForm` (not shown), every live
control dumped:

```
window title: Shard Console - LIVE retired | TEST running | publisher not publishing
tile: LIVE: RETIRED | retired 2026-10-14 (returns as a fresh 1.0 world) | back ffeaeaea
live.client  Open a client     enabled=False fore=Gray tip="Live is retired: retired 2026-10-14 (returns as a fresh 1.0 world)."
live.restart Restart           enabled=False fore=Gray tip="Live is retired: ..."
live.start   Start             enabled=False fore=Gray tip="Live is retired: ..."
live.stop    Stop              enabled=False fore=Gray tip="Live is retired: ..."
live.tail    Tail the log      enabled=False fore=Gray tip="Live is retired: ..."
qLive        LIVE shard        enabled=False checked=False fore=Gray tip="Live is retired: ..."
qTest        Test shard        enabled=True  checked=True
snapLive     LIVE shard (...)  enabled=False checked=False fore=Gray tip="Live is retired: ..."
snapTest     Test shard        enabled=True  checked=True
test.fresh   Start fresh (new world, live accounts) enabled=False fore=Gray tip="Live is retired: ... Start fresh copied its accounts from the live save; Wipe test accounts makes a new admin instead."
LIVE shard tab caption: LIVE retired 2026-10-14 (returns as a fresh 1.0 world). Live is retired: every button here is greyed and nothing checks, probes or emails about live. scripts\live.json liveEnabled true brings this tab back as it was.
```

**Not seen on screen:** I did not open the console window and look at it (no screenshot). The dump is the same form
object, built by the same code path, but colours are as WinForms reports them, not as seen.

**The probe.** Before (`server\lib\uo\modernuo\status\shards.json`, 20:56:37Z): live `"up": false` and test. After
`Start-UoStatus.ps1` (it recreated only `sl-uo-status` and `sl-shard-probe`), through the feed
(`http://localhost:8092/shards.json`, 20:57:31Z):

```
{"schema": 1, "generatedAt": "2026-10-14T20:57:31Z", "shards": [{"id": "test", "name": "Test shard", "port": 2594, "up": true}]}
```

Probe log `2026-10-14T20:57:31Z test=up`; container env `SL_LIVE_ENABLED=0`.

**The test shard.** `Start-TestShard.ps1 -Down` then `-Image sl-modernuo:good-61db33c`: `healthy: tagged
sl-modernuo:good-61db33c`, exit 0. Image id `sha256:527ac64a2177...` before and after, health `healthy`, started
20:56:58Z.

## The grep after the change

Same pattern, all text files tracked or new (not ignored): **906 lines in 62 files** (the 58 from before plus the four new files). More than before because the
greyed live code is kept by design, plus the new switch, its comments, the retired compose file and 13 facts. Every
remaining hit falls in one of these, and none is live doing anything while the switch is false:

| What the hit is | Where |
|---|---|
| Live code kept behind the switch (refuses or is skipped while false) | `scripts/Shard-Console.ps1`, `Live-Switch.ps1`, `live.json`, `Deploy-StatusPublisher.ps1`, `Publish-PatchNotes.ps1`, `Publish-GamePcSnapshot.ps1`, `docker/uo-status/probe.py`, `docker-compose.yml`, `Start-UoStatus.ps1`, `docker/website/html/index.html`, `migration.html` |
| Tests for both states | `scripts/tests/Shard-Console.Tests.ps1` |
| The retired record and the notes saying it is retired | `docker/uo/retired/docker-compose.live.yml`, `docker/uo/README.md`, `docker/uo/docker-compose.yml` (header), `README.md`, `docker/uo-status/README.md`, `docker/dashboard/config/services.yaml` (comment), `CHANGELOG.md` |
| Test-shard and bot guards that name live (or 2593) to refuse it | `docker/uo/docker-compose.test.yml`, `Start-TestShard.ps1` (incl. "live shard: untouched" in its summary), `test-shard.sh`, `tools/playtest-bot/*`, `scripts/Shard-Health.ps1:258` (the fatal-question answer text, true of either shard) |
| The `sl-modernuo:*` image repository the test shard runs from | `Check-Docker.ps1`, `Check-Shard.ps1`, `docker/uo/build.sh`, `scripts/Shard-Health.ps1` (prune), test fixtures |
| History, kept as written | `docker/uo/SERVER.md`, `COMMANDS.md`, `roadmap.md`, `docs/cloudflare-setup.md`, `scripts/extract-server.ps1`, `play-tests-2026-10-12.json` fixture |
| Another meaning of "live" | as in the "before" table |
| **Not changed, and needs a decision** | `player-package/payload/app/Play.ps1`, `Launch-Settings.ps1`, `Play-Lan.bat` (and their tests): the player launcher still connects to `shatteredlegacyuo.com:2593`. See For Chase. `AGENTS.md:45-46` (shard repo) says `server/uo/modernuo/Configuration/` "is bind-mounted into the live container"; that is now stale. Listed for the overseer, not edited. |

## Deviations and decisions for Chase

1. **Start fresh is greyed too, not only live's buttons.** Its new world took its accounts from the live save, which
   is gone, so it would now make a world that blocks at the owner account prompt for ever (D19). It refuses with that
   reason and points at Wipe test accounts. **Decision:** if a fresh test world is wanted again, it needs an account
   source that is not live (seed from the newest test snapshot's `Accounts`, or make the owner account at start). A
   follow-up, not built here. `Start-TestShard.ps1 -Fresh` itself is unchanged; run by hand it would make that
   blocking world.
2. **`docker/uo/docker-compose.yml` was split, not moved.** It also holds `sl-ddns` (running, public DNS). Moving the
   file whole would have left `sl-ddns` with no compose file. The live service went to `retired/`; ddns stayed.
3. **Live's code was greyed, not deleted**, as the overseer's 14:25 call said; so the grep has more hits, not fewer.
4. **Old facts were kept by pinning true**, not removed. The prompt said "remove live facts, update the rest"; with
   the grey-out, those facts are the proof that true restores today's behaviour, so removing them would lose it.
5. **The status publisher tile is grey, not red,** when nothing writes `status.json`. Only live wrote it. The website's
   "who's online" panel will show the shard offline; giving the test shard the status mount would change what the
   public website shows, so it is not done here.
6. **Tooltips over disabled buttons:** WinForms does not show a tooltip over a disabled control. The tooltip is set
   (the facts read it back), and the LIVE shard tab's caption says the same words where it can be seen.
7. **`Get-ConsoleConfig.LiveCompose` still points at `docker\uo\docker-compose.yml`.** With `liveEnabled` true again,
   the console will warn that file has no modernuo service it can read, which will be true until a 1.0 service is
   written. That is the "apart from building the new world" in the prompt.

## Bug rows that only concern live (for the overseer to close; `docs\` not edited)

- **D94** live could not load its save (waited at "Delete the object and continue?"). The container and save are gone.
- **D50**, live's half: `stop_grace_period: 60s` for `sl-modernuo` "takes effect when live is next recreated". It now
  sits in `docker/uo/retired/docker-compose.live.yml`. The test half is unaffected.
- **D25** and **D29**: already MOOT with D40; both are about live's image and `docker/uo/docker-compose.yml`'s
  `build:`. D29's danger (compose up there rebuilding live) is now gone with the service.
- **D8** and **D9** (test relaying to live, compose mounting live's save): fixed history, now with no live behind them.

## For Chase

1. **Deploy the website change** (Shard Console > Websites > Deploy, or `scripts\Invoke-WebsiteDeploy.ps1`): until
   then the public site still shows a Live dot, reading "unknown" now that `shards.json` lists no live. Not deployed
   here (it is public).
2. **The player launcher still points at 2593** (`Play.ps1`, `Launch-Settings.ps1`, `Play-Lan.bat`, shipped in the
   player package). With live retired, a player who clicks Play reaches nothing. Whether to point it at the test shard
   (LAN only, 2594), or leave it until 1.0, is your call; it changes a published package.
3. **The router still forwards 2593** to this PC, to nothing now. Harmless; close it if you like.
4. `sl-dashboard` picks up the new `services.yaml` by itself (bind mount). If the tile does not change, restart
   `sl-dashboard`.
5. Nothing else to run: the status containers were already recreated with the switch, and the test shard is back up
   on the same image.
6. `notes/passdown-overseer-2026-10-14.md` appeared in shard-migration at 15:43, while this prompt ran (the
   overseer's). It is not mine; the commit after this DONE stages with `git add -A`, so it goes in with P108.

## Repo size

No pending file over 5 MB: the largest is `scripts/Shard-Console.ps1`, 496 KB. The only files over 5 MB under
`D:\ShatteredLegacy` changed today are the test world's save, backup and archive (the restart's autosave), all under
`server/lib/`, ignored (`git check-ignore -v`: `.gitignore:58:server/lib/`). Scratch (baselines, mutant tree, dumps)
was in the session scratchpad outside both repos; both scratch worktrees were removed (`git worktree list` shows only
the repo, `bot-shard/src` and `test-shard-src`, as before).

## Commit preflight

`D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: 20 files pending (the changes above). docs: this note and `notes/passdown-overseer-2026-10-14.md` (the
overseer's, see For Chase 6).

P108 DONE
