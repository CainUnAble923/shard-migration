# cc-P85: Shard status dashboard (fresh judgment, its age, LAN serving, links)

Prompt: `D:\UO\cc-prompts\cc-P85-status-dashboard.md`. Builder; no shard build. Not committed (autopilot commits after
DONE). Both repos were clean at the start.

## Headlines

- **The judgment is rewritten from today's sources.** Before this, `tools/progress-state.json` had last been edited 2026-09-19.
  - The playable gates go from 7 to 11, and **2 of the 11 are met**. Every gate cites its sources and carries the date it was last confirmed.
  - The status line now says what runs: the test shard on the 2026.10.10 image, no live shard until the wipe, and P65 to P84 committed but not deployed.
  - The old "Settled: no fresh world" note is replaced by the current direction, with a date.
  - The 18 finished tasks are retired; 13 open ones remain, each with a date.
- **The page says how old it is.**
  - The header shows "Last updated <time>" beside "Judgment reviewed <date>" and the version. The review date turns amber after 7 days.
  - Each section whose own date differs from the header's shows "As of <date> (N days ago)".
- **Less depends on a person.** `progress.py` now derives these every run:
  - the CC queue: queued, running, done and stopped, from the queue folder, the autopilot's `state.json` and each prompt's notes
  - the play-test counts
  - VERSION
  - the latest DONE prompt
  - the review date
- **One line updates one item.** `tools/judge.py` changes or re-confirms a gate, task, status, direction or section and stamps the date. `tools/README.md` documents it.
- **Served on the LAN, at `http://192.168.1.58:8093/status`.**
  - It is one route on P83's `sl-play-tests` service, which reads the file on every request with `Cache-Control: no-store`. The service mounts the repo read-only.
  - **Not live yet:** P83's service itself was never deployed (port 8093 still runs the old `sl-test-queue`). The deploy steps are under For Chase.
- **Links everywhere.**
  - The dashboard header links to Play tests and Homepage. The links are built from the host the browser used, never localhost; opened as a file, they keep the LAN address.
  - The play-test page header gets "Status". Homepage gets a "Shard status" entry.
  - The Shard Console gets a **Status** button beside Play tests and Dashboard, in the PLAY TESTS tile and on the Autopilot tab. P84's theme is kept.
- **Proof:**
  - `progress.py` was run twice; only the time changed.
  - A scratch copy of the service served the page on the LAN address, identical to the file.
  - The dashboard tests pass 14 of 14 (they went red when the code was broken on purpose).
  - The console suite passes 195 of 195.

## What changed in the judgment, gate by gate

The sources are the overseer passdowns (newest 2026-10-05), `docs/feature-queue.md`, `docs/bug-list.md`, `docs/fidelity-principle.md`, `CHANGELOG.md`, the DONE notes P54 to P84, and `testing/play-tests.json`. A read-only research pass over them on 2026-10-13 also read the code, docker and the queue. Every gate below is confirmed 2026-10-13.

| Gate | Before (2026-09-19) | Now | Main sources |
|---|---|---|---|
| The shard runs and holds a world | yes, "49 tests" | **yes**: test shard on 2026.10.10; 1,133 / 1,133 tests (P82); no live shard until the wipe | cc-P82 section 7; passdown 10-05; docker |
| The player package installs on a clean PC | (new) | **yes**: T-049 clean sandbox, T-020 off-network, T-021 updater passed; the 10-13 zip is built but not uploaded | play-tests.json; cc-P81; D61 |
| A new character can train without hitting a wall | no, "ClusterFSkillGain runs 5x; New Haven quests lock at 50" | **no, largely built**. The guilds replaced the quests as the starter path. P66, P67 and P71 gave stalled skills a path to 200. Casting schools above ~120 and the content skills still need designs. 3 attempts and 5x amount are still the defaults | cc-P54, P66, P67, P71; f12-decisions 10-05; ClusterFSkillGain.cs:36-37 |
| A new character's first hour | (new) | **no**: the P80 framework is built, but its trials are TODOs with 8 decisions open; P79 is built; neither is deployed; T-040 failed (nothing points to the League) | cc-P79, cc-P80; T-040 / D41 |
| Levels and loops work end to end | (new) | **no**: F-12 is not built; `CompleteLoop` is only a hook; the research (P54, P72) and Chase's answers are done | ClusterFLoops.cs:1; cc-P54; cc-P72; f12-decisions |
| What is built is seen in a client | was "Ported content is verified in-world": yes | **no**: P46 to P57 passed in game on 10-04/05; P65 to P84 are not on the deployed image | passdown 10-05; play-tests.json |
| Somewhere to go | no | **no**: Despise is verified; Shame has never been in a client; the Burrows checks are open; extra facets are research only | client-check-backlog; cc4-shame; cc-P36; cc-P76 |
| Things to fight | no, "27 of 137" | **no**: no creature batch since 09-21; 19 spawn orphans; the old figure was not recounted | spawn-orphans.txt; cc-P50; cc-P65 |
| Set mechanics actually fire | no | **no, unchanged**: the hooks row is still unbuilt | gap-register A; patch-backlog P3 |
| No live gap a player would call a bug | no, "15 gap rows" | **no**. The bug list needs a pass itself: 60 open rows, 34 of which say fixed. Player-facing: D83-D85, D88, D32/D33, D14 | bug-list.md |
| The fresh-world wipe is ready | (new) | **no**: no single plan; the items (D34, D50, T-006, T-010, F-4, the tutorial greeting) are scattered; P73 is not deployed | bug-list; client-test-queue; cc-P73; cc-P80 |

The new gates the prompt asked for are levels and loops, the first hour, the package on a clean PC, and the fresh-world wipe.

**Tasks:**
- **Retired (18):** F1-F5, P1, P2, C1, C6, S1-S6, S8, S9, S10. They are kept as `tasks_retired`.
- **Kept and re-judged:** C2, C3, C4, C5, C7 and S7. S7 is now "partly superseded by P33's PointsSystem".
- **Added:** DEPLOY (P65-P84 to the test shard), F-12, TUTORIAL, WIPE, BUGS (the stale bug list), P83-DEPLOY, F-37.
- **The task IDs are not the numbering any more.** Day-to-day work now runs through the derived Queue section.

**Queue:**
- Read every run: P85 is running; P86 (console-vpn-disconnect) is queued; 35 prompts are finished, none stopped; the latest done is P84.
- After this DONE, P85 reads as done.

**Play tests:** 111 open, 1 failed, 18 passed (130 in all). These come from the file's own summary, in which "open" also counts later and blocked items. The section links to the page.

**Unchanged, with an as-of date:**
- The setup defects (still all resolved; re-confirmed today).
- The ported-content log (2026-09-21).
- The backlog, deferred and correction-log sections (2026-09-19).
- The upstream patch risk table (2026-09-19). Its counts above it are live.

## How freshness is shown

- **Header:**
  - "Last updated YYYY-MM-DD HH:MM": when `progress.py` ran.
  - "Judgment reviewed YYYY-MM-DD": the newest `confirmed` date in `progress-state.json`. Its hover text says how to update it.
  - The version.
- **Amber:** the review date turns amber, with "(stale)", once more than `STALE_DAYS = 7` days have passed. This is set when the page is rendered, and checked again in the browser on every open, so a page nobody re-rendered still turns amber.
- **Per section:** "As of <date> (N days ago)" in amber, shown only when the section's date differs from the header's date.
- **Per row:** each gate and task has a Confirmed column.

## Serving and links

- **`docker/test-queue/server.py`:** `GET /status` returns `--status-page` (env `STATUS_PAGE`). It is read from disk on every request and sent with `Cache-Control: no-store`.
- **`docker-compose.yml`:** adds `D:/UO/shard-migration:/data/site:ro`, a folder rather than a single file, because a single-file mount goes stale. It also sets `STATUS_PAGE`.
- **Why the play-test service and not a second web server:**
  - It is already the LAN-only service for this kind of page, bound to 192.168.1.58 and 127.0.0.1 and never routed through NPM.
  - It already sends no-store.
  - Adding the page there is one route and one read-only mount.
- **Links:**
  - The dashboard header has "Play tests" (:8093) and "Homepage" (:3000), built in the browser from `location.hostname`. As a file there is no host, so the LAN address stays.
  - The play-test page header has "Status" (`/status`, same origin).
  - Homepage `services.yaml` has a "Shard status" entry to `http://192.168.1.58:8093/status`.
  - The Shard Console has `links.status`, a "Status" button opening `http://localhost:8093/status`, consistent with its two existing links. The three link buttons in the PLAY TESTS tile size to their words to fit, and keep a small font in P84's UO theme.
- **Opening the file directly:** `file:///D:/UO/shard-migration/dashboard.html` still opens and renders on its own (checked in the browser).

## Proof

- **Before and after, header and gates.** Text dumps:
  - Before:
    `HEADER: Shard status Last updated 2026-10-13 03:27 Running on ModernUO Direction settled`
    with 7 gates, 2 met, and gate 5 reading "BLOCKED BY OUR OWN CHANGE. ClusterFSkillGain runs 5x ...".
  - After:
    `HEADER: Shard status Play tests Homepage Last updated 2026-10-13 07:07 Judgment reviewed 2026-10-13 Version 2026.10.13.6`
    with 11 gates, 2 met; the after table is in "What changed" above.
  - (The VERSION bump to .7 came after the dump.)
  - The full dumps are in the session scratch, `before-dump.txt` and `after-dump.txt`.
- **`progress.py` twice, 65 s apart.** I diffed README.md, dashboard.html, tools/progress.json and tools/expansion-coverage.json between the runs. The only differences are the `DATA:GENERATED` time and progress.json's `generated` field.
- **LAN service.** A scratch copy of `server.py` ran on `192.168.1.58:8095` with a temporary data folder, so the real `play-tests.json` was not touched. `GET /status` returned 200 with `Cache-Control: no-store`, and the body was byte-identical to `dashboard.html`. In the browser, the header links resolved to `http://192.168.1.58:8093/` and `http://192.168.1.58:3000/`. The scratch process was stopped. Nothing was deployed or restarted.
- **Tests:**
  - `python -m unittest tools/tests/test_status_dashboard.py`: **14 / 14**. They cover queue states, play-test counts, the review date, the stale rule (7 days is fresh, 8 is amber, never-reviewed is amber), as-of dates, the rendered queue and play tests, no localhost on the page, judge.py (gate, ambiguity refused, tasks add/retire, confirm) and the real state file (every gate dated and sourced, ASCII).
  - **Red:** four deliberate breaks made 3 tests fail: running counted as queued, a mismatched note number counted as done, a lax stale rule, and judge.py not stamping a gate. All restored `cmp`-identical.
  - Console: `scripts\tests\Shard-Console.Tests.ps1` **195 / 195**. Three P83 facts now include `links.status`.
  - The P84 timing fact failed once at 1,063 ms on a ~15 s build. It kept only the last of two builds per look; it now keeps the fastest, and passed at Plain 9,189 ms, UO 9,357 ms.

## Deviations and decisions for Chase

1. **The status page is not live until `sl-play-tests` is deployed.** P83 was never deployed; port 8093 still runs the old `sl-test-queue` nginx. I did not run compose or restart anything.
2. **The judgment found its own sources stale.** `docs/bug-list.md` lists 60 open rows, of which 34 say fixed. The BUGS task asks for a pass. Until then the "No live gap" gate reads from a list that overstates the open bugs.
3. **"Things to fight" was not recounted.** The research pass could not recount the old 27-of-137 figure today; the gate says so. A recount is cheap with `tools/content_index.py`.
4. **There is no fresh-world plan document.** The WIPE task proposes gathering the scattered items into one.
5. **The Console's Status link uses localhost,** as its Play tests and Dashboard links do (the console runs on this PC). Pages use the browser's host.
6. **The "Overall 27%" headline stays,** with its caveat. The direction is no longer porting ServUO content, so that percentage measures something the shard is no longer driving toward. Drop it or move it lower?
7. **The test count line** in the README ("751 tests in 141 files") counts `[Fact]`/`[Theory]` attributes. The gate cites the 1,133 cases the build runs. They differ by design (theories have several cases); the line was left as it was.

## For Chase

- **Deploy the status page** (on this PC, when you choose):
  ```
  docker stop sl-test-queue
  docker compose -f D:\ShatteredLegacy\docker\test-queue\docker-compose.yml up -d
  ```
  This is P83's own deploy; `docker\test-queue\README.md` and `Start-TestQueue.ps1` have the details. Then open `http://192.168.1.58:8093/status`.
- **Homepage** picks up its new "Shard status" entry from `services.yaml` on its next config reload or restart.
- **Keeping the judgment fresh:** `python tools/judge.py list` shows each item's date. `python tools/judge.py confirm gate "<name>"` re-confirms one; `gate`, `task` and `status` change one and stamp the date. The header's review date turns amber after 7 days with no confirmation.
- **The commit hook** (`Commit-ShardWork.ps1` runs `progress.py` before every commit) was not changed and works with the new state.
  - One run now also reads `D:\UO\cc-autopilot\state.json`, `ENABLED` and `D:\UO\cc-prompts\queue`. A missing one is read as off or empty, never as an error.
  - The run takes about the same time as before (the expansion coverage step dominates).

## Patch notes

`CHANGELOG.md` 2026.10.13.7 `### Staff`: one line. `VERSION` is 2026.10.13.7. Nothing was published.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

(The six non-ASCII characters in `dashboard.html` and one in `progress.py` were there before this task, in untouched lines; no added line has any.)

P85 DONE
