# cc-P112: A robot icon on every play-test item the overnight bot will attempt tonight

2026-10-14. Prompt: `D:\UO\cc-prompts\cc-P112-playtest-bot-icon.md`. The play-test page and service, the bot's plan, and
the game PC snapshot. Nothing deployed: the running `sl-play-tests` needs a restart to show it (For Chase).

## Headlines

- **The page marks items; it hides nothing.** The default view is as before (Open, today's order). Marks:
  - a **robot** on each item tonight's run will attempt, tooltip "The overnight bot tries this tonight (about N min).
    Plan as of <time>.";
  - a **dim robot** on items the bot can check (BOT or BOT-PARTIAL in `testing/bot-triage.md`, or with a check) that
    have no work tonight;
  - no icon on EYES, DEPLOY and DECISION items.
- **After a run,** each item the bot checked shows a chip with its newest bot result ("bot: pass 2026-10-13"; pass,
  fail, flaky or could not run). The chip links to that run's `report.md`, opened at the item's row. The bot still
  never marks Pass or Fail.
- **A "Bot tonight" filter chip** sits beside the existing filters and is off by default. The header shows
  **"Bot tonight: 18"**, which opens that filter when clicked; its tooltip gives the whole run's length and the plan's
  time.
- **One rule, the runner's.** The plan is `uobot.work.find_work`, called exactly as `Run-OvernightPlaytests.ps1`'s
  step 0 calls it, by a new `uobot/tonight.py`. There is no second copy of the rule.
  **On today's data:** 18 items, the same 18 ids as the runner's work step, commit `b58ef94`, about 166 minutes.
- **How the service knows: a small file, refreshed on the game PC** (my call, why below).
  - The every-minute snapshot task (`Publish-GamePcSnapshot.ps1`) runs `uobot.tonight` at most every 5 minutes into
    `testing/bot-tonight.json` (git-ignored), in every mode.
  - After the Haven cutover it also sends the same plan inside the snapshot, as `botTonight`.
  - `GET /api/bot-tonight` reads the file (game PC) or the snapshot (Haven) and caches 5 minutes. It never runs git, a
    build or a container.
  - Anything missing or broken shows one quiet "Bot plan unavailable" in the header, never an error.
- **Tests:**
  - 5 bot facts and 12 service and page facts, new; each seen failing first.
  - A real check in a browser against a copy of today's data: 18 robots, 73 dim, `Bot tonight: 18`, the filter
    showing exactly those 18, report links opening on the row.
- **Two pinned expectations I broke in P110** (the menu's Dashboard host) are fixed here. Details under Tests.

## Why a file, not running the check in the service

- **The service cannot run the check.** `sl-play-tests` runs in `python:3-alpine` with no git, and neither the shard
  repo nor `D:\UO\bot-shard` is mounted (`docker/test-queue/docker-compose.yml`). `find_work` needs both (`git diff`
  over `server/`, `docker/uo/`, `tools/playtest-bot/uobot/`).
- **On Haven the bot's tree is not there at all.** So the work check runs on the game PC, where the runner runs.
- **It rides an existing scheduled task** (`SL game PC snapshot`, every minute, already installed), so there is no new
  task to register. `--max-age 300` makes most minutes a no-op.
- **The runner's own `work.json`** (`D:\UO\bot-shard\work.json`) is written only at 01:30, so it cannot answer "tonight"
  during the day.

## What changed, with file:line

**Shard repo (`D:\ShatteredLegacy`)**

| File:line | Change |
|---|---|
| `tools/playtest-bot/uobot/tonight.py` (new, 121 lines) | `plan()`: `find_work` and `estimate_minutes` exactly as the runner calls them (repo HEAD, the play-tests file, `testing/bot-runs`, 3 runs, 120-minute soak); `tonight` {id: reason, minutes for that item}; `checkable` (triage BOT and BOT-PARTIAL plus every check, minus tonight); `last` (each id's newest result in any run, ERROR included); a bad repo or commit gives `available: false` with the error. `main()` with `--max-age` (a fresh file is left alone). It writes only its out file |
| `tools/playtest-bot/uobot/work.py:124` | `check_seconds()` split out of `estimate_minutes` (no change in what it returns), so an item's minutes use the same per-check timing |
| `tools/playtest-bot/tests/test_tonight.py` (new) | 5 facts, below |
| `docker/test-queue/server.py:10` | docstring: the two new routes |
| `docker/test-queue/server.py:177`, `:187` | `bot_report_path` (a strict `yyyy-MM-dd-HHmm` stamp, looked up in `DATA/testing/bot-runs`, then the notes root's: on Haven that is the repo clone); `bot_tonight()`: the file, else the snapshot's `botTonight`, shaped by `bottonight.shape`, cached 300 s |
| `docker/test-queue/server.py:291`, `:293` | `GET /api/bot-tonight`; `GET /bot-runs/<run>/report[?item=<id>]` |
| `docker/test-queue/html/index.html:46` | CSS: `.robot`, `.robot.dim`, the result chips, the quiet count |
| `docker/test-queue/html/index.html:111` | the "Bot tonight" filter button (off by default; `filter` still starts at `open`) |
| `docker/test-queue/html/index.html:254-274` | `botInfo`, `robot` (the full or dim robot, `&#129302;`, and the result chip with its link), `botCount` (the header count, or "Bot plan unavailable"), and the robot in `card()` |
| `docker/test-queue/html/index.html:312`, `:464` | `load()` fetches `/api/bot-tonight` beside the others (a failure becomes the quiet line); a click on the count opens the filter |
| `scripts/Publish-GamePcSnapshot.ps1:18-35` | `-BotPlan`, `-NoBotPlan`; the plan refresh before the cutover check, so the game PC's own page has it in every mode; a failure never stops the snapshot |
| `scripts/Publish-GamePcSnapshot.ps1:88` | `botTonight` added to the snapshot as the file's own JSON on one line, only if valid and under 48 KB (Haven's limit is 64 KB; today's snapshot with the plan: 5.7 KB) |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.18, one `### Staff` line |

**shard-migration**

| File | Change |
|---|---|
| `tools/bottonight.py` (new, 93 lines) | `shape(plan, source, report_exists)`: the per-item state, tooltips, result labels and report links; `unavailable(why)`; `report_html` (the report's text with an anchor on each item row and the asked-for row marked). No rule, no git |
| `tools/tests/test_bot_tonight.py` (new) | 12 facts, below |
| `.gitignore` | `testing/bot-tonight.json` (proved: `.gitignore:30`) |
| `tools/tests/test_haven_h1.py`, `tools/tests/test_status_dashboard.py` | the Dashboard host pin, `192.168.1.58` to `192.168.1.61` (P110) |

**Tooltip wording, one deviation:** the prompt's dim tooltip is "Bot-checkable; already checked on this code". That is
true only for items with a built check and a result. A triage BOT item with no check built yet has never been checked,
so its tooltip says "Bot-checkable; no bot check is built for it yet, so tonight's run does not try it". Today, on the
page: 73 dim robots, none with a bot result (every item with a check has work tonight), and all 18 result chips are on
tonight's items, whose last runs (2026-10-13) were on older code.

## Tests

**Bot** (`tools\playtest-bot\tests\test_tonight.py`, on P102's throwaway git fixture):
1. tonight is exactly `find_work`'s items, minutes the runner's `estimate_minutes`, and the commit;
2. checkable is triage BOT and BOT-PARTIAL plus the checks, minus tonight; EYES, DEPLOY and DECISION never;
3. last is each item's newest result, ERROR included, with its run;
4. a bad commit, or no repo, gives `available: false`, not an exception;
5. the file is refreshed only when older than `--max-age`, and git's HEAD and status are unchanged.

**Service and page** (`tools\tests\test_bot_tonight.py`):
- Shape:
  - tonight gets the robot, checkable the dim robot, the rest nothing; the exact tooltips;
  - a result's label, and a report link only when that report exists;
  - missing plan, wrong schema, not JSON, or the work check's error: unavailable;
  - the report page anchors item rows and marks the asked one.
- Service (started on a free port with a scratch root):
  - the game PC file gives the items, a report link and the report page;
  - a rewrite within 5 minutes is not seen (the cache);
  - `../` and an unknown run are 404;
  - no plan is a 200 with `available: false`;
  - Haven mode (`--data`) reads the plan from the stored snapshot, with its "as of", and links reports from the notes
    root.
- Page (text):
  - the fetch is in `load()`'s `Promise.all`;
  - the full and dim robot markup, and the robot in `card()`;
  - the filter is an extra, and Open stays the default;
  - the header count, the quiet line, and the count's click;
  - the result chip's link;
  - the source stays ASCII.

**Seen failing first:**
- **Service and page:**
  - with `server.py` and `index.html` swapped back to HEAD, and `bottonight.shape` stubbed (every item "tonight", every
    report linked), **9 of 12 failed**;
  - the 3 that passed test what the stub left alone: the unavailable path, the report page, and "the source stays
    ASCII" (the old page has no emoji either);
  - restored, `cmp` identical: **12 of 12**.
- **Bot:**
  - with `tonight.py` stubbed (every check tonight, triage buckets ignored, only PASS kept as a result, `--max-age`
    ignored), **4 of 5 failed**;
  - the bad-commit fact passed (the stub did not touch it);
  - restored, `cmp` identical: **5 of 5**.

**Whole suites after the change:**
- **shard-migration `tools\tests`: 83 of 83.** This includes the two P110 pins fixed here:
  `test_haven_h1.Menu.test_nav_js_has_url_mode_and_lan_only_and_keeps_todays_rows` and
  `test_status_dashboard.Freshness.test_the_page_links_never_say_localhost`. Both still expected the menu's Dashboard on
  the game PC. **P110 moved it to Haven on purpose and I did not run these Python suites then. My miss.**
- **Bot suite: 37 of 38.** `test_overnight.Scripts.test_installer_dry_run_prints_the_call_and_registers_nothing` fails
  because it asserts the "SL overnight play tests" task is not registered, and it is (Chase installed it after P102). The
  same kind of environmental failure as P107's snapshot-task fact.
- **Console `P107_*`: 7 of 8.** The one failure is the known `P107_TheSnapshotSendsNothingBeforeTheCutover...`
  (scheduled task installed).
  - **My bug, caught by that fact:** at first it failed earlier, on parsing. It reads the dry run's JSON from one line,
    and my first splice put the plan's multi-line JSON in. The plan now goes in on one line, and the fact is back to
    its old failure only.

**Real check against today's data:**
- `uobot.tonight` gives **18 items on `b58ef94`, 166 minutes**.
- The runner's work step (`python -m uobot.work`, with the runner's arguments) gives **18 items on `b58ef94`, 166
  min**, the same 18 ids:
  P56-4, P56-6, P58-0, P61-3, P61-5, P62-1, P62-7, P64-1, P64-2, P64-3, P64-4, P64-5, P64-6, P66-7, P71-7, T-039, T-046,
  T-047.
- The new service and page, on port 18093 with a copy of `notes`, `docs` and `testing` (not the live service, whose
  importer writes), read in the browser pane:
  - header `Bot tonight: 18`; 18 robots, 73 dim robots; 18 result chips (`bot: pass 2026-10-13`, linking to
    `/bot-runs/2026-10-13-1428/report?item=...`);
  - the filter shows 18 cards, all with the robot; Open shows all 213 again; no errors;
  - a report link answers 200, with the item's row marked.
- That scratch service was stopped and the copy deleted.

**The scheduled refresh:** the installed `SL game PC snapshot` task runs this script from the working tree, so it began
refreshing the plan at once. My dry run wrote the file at 22:57:06Z. Without me, the task's 18:02:56 (local) run
rewrote it at **23:02:58Z** (LastTaskResult 0), the first minute it was over 300 s old: 18 items on `b58ef94`.

## Deviations and decisions for Chase

1. **What "attempt tonight" means:** the robot marks the items with work, which is what the runner's step 0 lists in the
   "starting" email. When the run goes ahead it actually runs **all 20 checks** (`uobot.run` without `-Only`), so the
   dim-robot items that have a check are re-checked too. They already have a result on this code, so they are safe to
   skip by hand.
2. **The dim tooltip's wording** (above): "no bot check is built for it yet" where that is the truth.
3. **The plan is refreshed by the snapshot task,** so if that task stops, the plan goes stale and the tooltip's "Plan as
   of" says so. It never turns into an error.
4. **`checkable` comes from `bot-triage.md` as it stands** (2026-10-13). Items added since are not in the triage until it
   is re-sorted, so they get no dim robot. They still get the full robot as soon as a check exists and has work.

## For Chase

1. Restart the play-test page so it serves the new code:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\docker\test-queue\Start-TestQueue.ps1
   ```
   If you have cut over to Haven (P107), use Shard Console > Websites > **Ops pages: deploy** instead. It restarts
   Haven's page on the new code, and the plan arrives with the game PC's snapshot within a minute.
2. **The icons in one line:** a robot means tonight's bot run tries it (skip it); a dim robot means the bot can check it
   but has nothing new to do tonight; the "bot: ..." chip is its last result, linked to the report.

## Repo size

No pending file over 5 MB; the largest new one is the test file, 205 lines. `testing/bot-tonight.json` (5 KB) is
git-ignored.

## Commit preflight

`D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: `CHANGELOG.md`, `VERSION`, the page, `server.py`, `Publish-GamePcSnapshot.ps1`, `uobot/work.py`, and the new
`uobot/tonight.py` and `tests/test_tonight.py`. docs: `.gitignore`, the two re-pinned tests, `tools/bottonight.py`,
`tools/tests/test_bot_tonight.py` and this note. `testing/bot-tonight.json` is not pending (`.gitignore:30`).

P112 DONE
