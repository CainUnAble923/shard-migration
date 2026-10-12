# cc-P83: Interactive play-test queue (port 8093 fills itself from every DONE prompt, plus dashboard metrics)

Builder: Claude. The autopilot handed this prompt over at 2026-10-12 16:08:06, right after P74. Before I started,
both repos were clean (`git status --short` empty in each), so nothing of anyone else's was pending.

## Status: finished on 2026-10-12

Built and tested. **Not deployed:** port 8093 still serves the old read-only `sl-test-queue`, because the prompt
said not to run docker compose or restart anything. Chase's deploy steps are under For Chase. The real backlog
(P56 to P74, plus the 49 old T-rows) is already imported into `testing\play-tests.json`.

## Headlines

- **One page, interactive:** `sl-play-tests` (python:3-alpine, standard library only) replaces `sl-test-queue` on
  port 8093.
  - Every waiting play-test is grouped by prompt, newest first.
  - Each shows what to do, what should happen, and the version it needs.
  - Buttons: **Pass**, **Fail** (asks for a one-line note) and **Later**, plus Reopen.
  - Filters: Open, Failed, All. Counts at the top.
  - Items can be added by hand (`M-001`...).
  - Works on a phone, in light and dark mode.
- **It fills itself.** The service runs the importer on start and every 60 s. A notes file that ends `Pnn DONE`
  is on the page within a minute with nobody doing anything. Proved on a copy: a new DONE file dropped at
  16:21:57 was on the page at 16:22:02.
- **One parser.** `D:\UO\shard-migration\tools\playtests.py` holds every rule. The service imports it (read-only
  mount), and `tools\Import-PlayTests.ps1` runs it on the host.
- **The overseer reads `testing\play-tests.json`:** its `summary` block at the top has the counts and every Fail
  with its note, prompt, time and bug id. `testing\SUMMARY.md` has the same and is rewritten on every write.
- **Console:** a sixth tile, **PLAY TESTS**, shows the open count. It turns amber when a Fail is not yet logged in
  the bug list. **Play tests** and **Dashboard** buttons sit inside it, and the same two are on the Autopilot tab.
- **Dashboard:** a **Play tests** entry in Homepage links to the page and shows Open, Failed and Passed through
  `customapi`. Homepage picked it up with no restart. The public status feed (8092) was left alone: it is
  player-facing.
- **Tests:**
  - Importer: 20 Pester (3.4) tests, all passing.
  - Console: 181 facts, all passing (175 before, 6 new).
  - Service: proved on a scratch port against a copy of the data.

## The extraction rules (`tools\playtests.py`, top of the file)

1. **Only DONE prompts import:** the last non-blank line must be exactly `Pnn DONE`. A file ending
   `Pnn STOPPED: ...`, or with no DONE line, is skipped, and each run says so.
2. **Only P56 and later** (`FIRST_PROMPT = 56`): that is the backlog the prompt named. P54 and P55 are DONE but
   older; see the decisions.
3. **The checklist is the list under the `For Chase` heading,** exactly that heading. "Decisions for Chase" and
   "Deviations and decisions for Chase" are not checklists, and neither is any list under Headlines.
4. **Inside For Chase, a line that is not a list item is a marker,** and it decides what the items after it are:
   - **in-game**: it says in-game, in game, checklist, to try it, to run, how to use, or in the client.
   - **deploy**: it says deploy, package first, commit, build, publish, or restart the test shard.
   - **anything else** (`**If it goes wrong:**`, `**Promote to docs:**`, `**Bugs in ...**`): its items are
     not play-tests.
5. **List items before any marker count as tests, flagged "unmarked".** P60, P63 and P68 start straight with
   console checks; the page shows them as "from For Chase, no in-game heading".
6. **Whatever the marker said, a step that is a deploy, commit or docs step is never a play-test.** That means a
   step that:
   - starts with Commit, Push, Promote, Deploy, Build the package, Publish, Get it onto, Put `sl-modernuo`,
     Package first, Decide, Before you leave, or To undo; or
   - names `docker tag`, `Start-TestShard.ps1`, `Build-PlayerPackage.ps1`, `Publish-PlayerPackage.ps1` or
     `Commit-ShardWork.ps1`; or
   - says "promote to docs".
7. **Code blocks are skipped.** An indented line (a continuation, or a nested list) belongs to the step above it.
8. **Ids are the prompt plus the step's place among the play-tests** (`P71-3`), not the notes' own step number.
   P67's tests are notes steps 2 to 8 and come in as `P67-1` to `P67-7`.
9. **What and Expect** are split at the first `: ` that is not inside backticks, quotes or parentheses. A short
   lead-in with no command in it, up to 4 words (`Hiding:`, `Stable slots:`), becomes the step's label. The whole
   original step is kept as `text`, so a bad split loses nothing.
10. **Version** is the first `` `[version` shows X `` or `[ShardVersion] Shattered Legacy X` in the notes,
    applied to all of that prompt's items.
11. **Nothing parsed:** a DONE prompt with no checklist gets one item, `Pnn: checklist not parsed, read the notes`
    (id `Pnn-0`).
12. **Re-import:** a notes file whose hash has not changed is not read again.
    - If it changed, each position is compared. Changed text keeps the result, sets `textChanged` and keeps
      `previousText`.
    - New steps are added at the end. A step that disappeared is kept and flagged `removedFromNotes`.
    - Nothing is ever renumbered, reordered or reset.
13. **The T-rows of `docs\client-test-queue.md` are imported once,** recorded under `imports.clientTestQueue`.
    - They keep their T-NNN ids and status: OPEN to open, PASS or PASSED to pass, FAIL to fail, BLOCKED and
      MOOT as they are.
    - A FAIL takes its note and bug id from the Results lines, including wrapped lines. T-040 comes in as fail,
      logged as D41.
    - The .md file is never written.

## Parse table, P56 to P74 (the real import, 2026-10-12)

| Prompt | Play-tests | Skipped (deploy, docs, other) | Version | Note |
|---|---|---|---|---|
| P56 | 7 | 4 | - | 3 deploy steps, 1 promote |
| P57 | 7 | 6 | - | commit, build, publish, check copy, deploy, promote |
| P58 | 1 | 0 | - | **not parsed**: no For Chase section (a patch-notes catch-up) |
| P59 | 1 | 0 | - | **not parsed**: Decisions for Chase only (research) |
| P60 | 6 | 1 | - | console checks, unmarked |
| P61 | 5 | 5 | 2026.10.05.2 | |
| P62 | 8 | 4 | - | `- [ ]` checklist under "In-game checklist (test shard):" |
| P63 | 6 | 1 | - | console checks, unmarked |
| P64 | 6 | 0 | 2026.10.05.3 | deploy in a code block, skipped as code |
| P66 | 7 | 0 | 2026.10.06 | |
| P67 | 7 | 2 | - | deploy is step 1 and promote is step 9 of the same numbered list |
| P68 | 2 | 0 | - | console checks, unmarked |
| P71 | 7 | 0 | 2026.10.10 | |
| P72 | 1 | 0 | - | **not parsed**: Decisions for Chase only (research) |
| P73 | 7 | 4 | - | 3 deploy steps and "To undo" skipped; steps 1 and 2 are preconditions and do come in |
| P74 | 3 | 8 | - | the bug reports and "decide on bugs" skipped |

There are no notes files for P65, P69 or P70. With the 49 T-rows that makes **130 items: 111 open (including 1
blocked), 1 failed (T-040, logged as D41), 18 passed.**

## The service and the page

- `D:\ShatteredLegacy\docker\test-queue\server.py`: a `ThreadingHTTPServer`.
  - `GET /`: the page.
  - `GET /api/items`: the whole document.
  - `GET /api/summary`: counts for the dashboard.
  - `POST /api/result`: pass, fail, later or open. A fail with no note is a 400.
  - `POST /api/bug`: marks a Fail as logged.
  - `POST /api/manual`: adds an item.
  - `POST /api/import`: imports now.
  - An unknown id is a 404 and an unknown status a 400.
- **Writes:** every change runs under a lock file (`play-tests.json.lock`, created exclusively, taken over after
  30 s if stale). It is read, changed, written to a temp file and renamed. The lock works across processes, so the
  host importer and the container never interleave. `testing\.gitignore` keeps the lock and temp files out of git.
- **JSON:** pretty-printed, keys in a fixed order, items in the order they were added, ASCII
  (`ensure_ascii`).
- **Compose:**
  - The service is called `play-tests` and the container `sl-play-tests`.
  - It publishes `192.168.1.58:8093` and `127.0.0.1:8093` only: this PC's LAN address and localhost, not every
    interface.
  - It is not in NPM or DNS. **There is no login:** anyone on the home network can mark results.
  - Mounts, all folders (single files go stale):
    - the test-queue folder at `/app/svc` (read-only)
    - shard-migration `tools` (read-only), `notes` (read-only) and `docs` (read-only)
    - `testing` (read-write)
  - The network name `sl-test-queue-net` is kept.
- **Page:** `docker\test-queue\html\index.html`. One file, no CDNs, light and dark through
  `prefers-color-scheme`, 44 px tap targets.
  - It refreshes every 30 s, but not while a text box has focus.
  - A Fail asks for its note in a prompt dialog, and the Bug id button asks the same way.
  - The **Dashboard** link is built from `window.location.hostname` plus `:3000`. Reached at
    `http://192.168.1.58:18093/` in the proof, it pointed at `http://192.168.1.58:3000/`, and that address
    answered 200 from this PC.
- **Dashboard** (`docker\dashboard\config\services.yaml`, group Shattered Legacy, before Wiki):
  - href `http://192.168.1.58:8093/`, the LAN address the dashboard itself uses (its other entries use it, and
    `HOMEPAGE_ALLOWED_HOSTS` lists it).
  - Widget `customapi`, url `http://192.168.1.58:8093/api/summary`, `refreshInterval: 60000`, mappings `open`,
    `failed` and `passed` with `format: number`.
  - Syntax checked against the running Homepage, **v1.13.1** (`/app/package.json` in `sl-dashboard`, image
    created 2026-05-11), and gethomepage.dev's customapi page: `field`, `label`, `format` (`number` is a listed
    format), `refreshInterval` in ms.
  - The widget is fetched by Homepage's server inside `sl-dashboard`, on network `sl-dashboard-net`. Proved:
    `docker exec sl-dashboard wget http://192.168.1.58:18093/api/summary` returned the counts.
  - **No restart needed:** `GET http://localhost:3000/api/services` listed "Play tests" right after the edit.
    The widget's proxy returns 404 until the new service runs, because today's nginx on 8093 has no
    `/api/summary`.
- **Public status page (8092): left alone.** `docker\uo-status\README.md` says it is what the website reads,
  through NPM's `/api/` route, and that it "is not an admin feed". Test counts are not for players.

## Proof

- **Real import** (this repo, `testing\play-tests.json`): the first run said
  `written: 130 items, 111 open, 1 failed (0 not logged), 18 passed`. Running it again said `no change`, and the
  table above is the result.
- **Service, on a copy at port 18093** (`python server.py --root <copy> --port 18093 --import-seconds 10`):
  - P71-1 pass.
  - P71-2 fail with no note: 400. Then fail with "the 24th pet was accepted": saved.
  - Manual item `M-001` added. Unknown id: 404. Status "maybe": 400.
  - **20 results posted at once** (20 curl calls in parallel): 20 of 20 saved, and the summary said 20 later.
  - **A new DONE prompt arrives with nobody doing anything:** a `cc-P95-...md` file ending `P95 DONE` was
    imported 5 s later (10 s cycle on the copy).
  - **The page,** in the browser pane at 375 px wide, in dark and light mode:
    - grouping, counts, filters, the fail note and the "not logged yet" chip all showed;
    - a real click on Later for M-001 saved (`later`, with a timestamp);
    - from `http://192.168.1.58:18093/` the Dashboard link was `http://192.168.1.58:3000/`.
  - **Restart:** stopped the process and started it again on the same data. P71-1 was still pass, P71-2 still
    fail with its note, M-001 later and P56-1 later. The start import and a forced `POST /api/import` left the
    file byte for byte the same (hash `584a5359f8e9ceba` before and after): **re-import adds nothing.**
- **One bug found and fixed in the proof:** a filter clicked before the first load left the page on "Loading..."
  (`render()` ran with no data). `render()` now waits for the data.
- **Pester** (`Invoke-Pester tools\tests\Import-PlayTests.Tests.ps1`): **20 passed, 0 failed.** The fixtures in
  `tools\tests\fixtures\playtests\` cover:
  - a P71-style numbered list after a deploy code block;
  - a P67-style list with deploy and promote steps in it;
  - a STOPPED file;
  - an unparseable DONE file;
  - three T-rows in the real file's format, including a wrapped Results line with D41.

  The tests check:
  - `-WhatIf` writes nothing;
  - re-import with no change does not even rewrite the file;
  - a pass and a fail survive a re-import after the notes change;
  - the changed step is flagged with its old text, the new step goes at the end and nothing is reordered;
  - the Fail is in the summary block and SUMMARY.md.
- **Console** (`scripts\tests\Shard-Console.Tests.ps1`): **181 facts, 181 passed.** The six new facts:
  - `P83_PlayTestsCountsTheRealBacklog`: the real file as fixture, `111 OPEN`, grey.
  - `P83_AFailNotYetLoggedTurnsItAmber`
  - `P83_LaterAndBlockedStillCountAsOpenAndNothingOpenIsGreen`
  - `P83_NoFileOrABadOneIsGreyUnknownNeverRed`
  - `P83_TheLinksOpenTheTwoPagesAndNothingElse`
  - `P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo`: P74's six Autopilot buttons unchanged.

  `-Status -DryRun` prints `PLAY TESTS : 111 OPEN  111 open, 1 failed, 18 passed`, and
  `-Action links.playtests -DryRun` prints `OPEN explorer.exe http://localhost:8093/`.
- **Patch notes:** a new `## 2026.10.12.3` with one `### Staff` line (2026.10.12.2 was committed with P74).
  `VERSION` is 2026.10.12.3. The wiki page was not published.

## Deviations and decisions for Chase

1. **The parser is Python, and the PowerShell importer runs it.** The service has to be Python (python:3-alpine,
   no PowerShell in it), and the prompt wants one source of parsing logic. So `Import-PlayTests.ps1` is a thin
   wrapper over `tools\playtests.py`, and it needs Python 3 on PATH (it is: 3.12.10). The alternative, the
   importer in PowerShell only, would need a host-side trigger (a scheduled task) and would not run while the PC
   sits at the login screen.
2. **The console's tile facts are in the console's own harness, not Pester.** `Shard-Console.Tests.ps1` explains
   why it avoids Pester 3.4. The importer's tests are Pester, as asked.
3. **The service is `sl-play-tests`, a new name,** not `sl-test-queue`, so a stale container cannot be mistaken for
   it. `Start-TestQueue.ps1` removes the old one.
4. **Port binding:** `192.168.1.58:8093` and `127.0.0.1:8093` instead of every interface. That is the "LAN only"
   the prompt asked for. **Not proven under Docker Desktop**, because nothing was started (see For Chase).
5. **Console checks count as play-tests.** P60, P63 and P68 are console prompts whose "For Chase" lists are checks
   at a screen, not in game. The rule takes them and flags them unmarked, so they can be told apart. P73's steps 1
   and 2 are preconditions ("Run the Console from your own Windows login"); they come in and can be marked Pass or
   Later.
6. **P58, P59 and P72 each have one "not parsed" item,** as the prompt said. They are a patch-notes catch-up and
   two research prompts with decisions, not tests. Mark them Later or Pass.
7. **The backlog starts at P56.** P54 and P55 are DONE too. P55 has a checklist (its steps 4 to 12 are in game). Lowering
   `FIRST_PROMPT` to 54 in `playtests.py` imports them, and nothing else changes.
8. **A Fail is "logged" when it has a bug id.** The overseer sets it with the page's Bug id button,
   `POST /api/bug`, or by editing the JSON. The tile is amber only while a Fail has none.
9. **Result statuses:** open, pass, fail and later can be set. Blocked and moot exist only for imported T-rows.
   Open, later and blocked count as open.
10. **`docs\client-test-queue.md`:**
    - Proposal: freeze it, with one line at the top: "Frozen 2026-10-12: new items and results go on the
      play-test page (http://192.168.1.58:8093/, `testing/play-tests.json`)."
    - The rows stay as history. Its rules about T-NNN ids are still right for the 49 imported rows.
    - Agents never edit docs, so this is yours.

## For Chase

**Deploy (Windows PowerShell, after the autopilot's commit):**

1. Run `D:\ShatteredLegacy\docker\test-queue\Start-TestQueue.ps1`. It:
   1. stops and removes the old `sl-test-queue` (`docker stop sl-test-queue`, then `docker rm sl-test-queue`);
   2. runs `docker compose up -d --force-recreate play-tests` in that folder;
   3. checks `/` and `/api/summary` on localhost.
2. If compose says it **cannot bind 192.168.1.58:8093**, Docker Desktop does not accept a host address there.
   Change the two `ports:` lines in `docker\test-queue\docker-compose.yml` to the single line `"8093:8000"` and run
   it again. That is what the old page did.
3. `docker logs sl-play-tests` should show `serving 0.0.0.0:8000` and no `import FAILED`.
4. The dashboard needs nothing. Its Play tests entry starts showing counts within a minute of the service
   starting.

**How to use the page:**

1. On your phone (home Wi-Fi) or this PC, open `http://192.168.1.58:8093/`.
2. Open (the default view) shows everything waiting, newest prompt first. Each card shows:
   - what to do, and "Expect:" with what should happen;
   - "needs 2026.10.10" when the notes name a version: deploy that first.
3. Press **Pass**, **Fail** (one line on what happened) or **Later**. **Reopen** undoes any of them.
4. **Failed** lists the failures. After the overseer logs one in the bug list, its **Bug id** button records the
   number and the console tile stops being amber.
5. "Add an item by hand" at the bottom adds your own `M-001`, `M-002`...
6. New prompts appear on their own: when a notes file ends `Pnn DONE`, its checklist is on the page within a minute.
7. In the console, the **PLAY TESTS** tile shows the count; its two buttons open this page and the dashboard.

**To check from a second device:** on your phone, open `http://192.168.1.58:8093/`, tap **Dashboard**, and
Homepage opens at `http://192.168.1.58:3000/`. On Homepage, Play tests opens the page again.

**Promote to `docs\`:** the client-test-queue freeze line (decision 10), and a line in the workstreams or runbook
saying play-tests live in `testing\play-tests.json`.

P83 DONE
