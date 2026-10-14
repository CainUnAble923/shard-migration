# cc-P97: Bug reports on the play-test page, and a reason required when declining

2026-10-14. Builder of the `sl-play-tests` service and page. No shard build; the live service was **not** restarted
(Chase deploys, below). Tested on a scratch copy of the service on `127.0.0.1:18093`, since removed.

## Found in passing, not P97: the live container is stuck at a world-load prompt

At about 09:15, while looking for a "deployed version", `shards.json` said live `up: false`. `docker logs sl-modernuo`
shows it started at 08:06 local, hit `***** Bad deserialize of Server.ClusterFAccountPersistence (0x40128E03) *****`
(`ArgumentOutOfRangeException` in `ReadDateTime`, from `WoodDiscoveryEntry..ctor`, then `ClusterFAccountData..ctor`),
and is waiting at `Delete the object and continue? (y/n/a)`. The same prompt appears in earlier starts in that log
(2026-09-29 and later).

- **Not touched:** answering it deletes account data, which is Chase's call. Read-only `docker logs` and
  `docker inspect` only. A push notification was sent at the time.
- **Possibly expected:** the status page's judgment says "there is no live shard until the fresh-world wipe". If live is
  not in use, this is known. If it is, it has been down since 08:06. I could not tell which, so I report rather than
  judge.

## Headlines

- **A Bugs tab on the play-test page**, next to Ideas, with a badge counting new reports. It has:
  - **quick add:** title (required), what happened, what you expected, steps, severity (`blocks play`, `wrong`,
    `annoying`, `looks wrong`), area (the Ideas list), linked play test, character, location;
  - the **shard version**, filled in by the server (never typed);
  - **up to 3 screenshots**, from a file pick or a paste.
- **"Bug from this"** sits on every play-test card, next to "Idea from this". **Marking a play test Fail** now asks
  "Report a bug for this?". Yes opens quick add with the play test linked and the Fail note as "What happened";
  Cancel skips it.
- **The list**, newest first, with Edit and the statuses:
  - `new`;
  - `taken`: "taken, pending number" until the overseer gives it a number, then **Became D-NN**, which stores it;
  - `duplicate`: of a D-number or another report, **required**;
  - `not a bug`: **reason required**;
  - `fixed`: set by hand, and keeps the D-number;
  - **Delete**, which needs a reason; the id is retired and never reused.
- **"Copy new bugs"** gives plain text, one block per report with every field, the linked play test's id and title,
  and each screenshot's full path on this PC. It then offers to mark them "taken, pending number".
- **Ideas (Part B):**
  - Declining or deleting needs a reason that is not empty and not only spaces, checked by the server and the page.
  - Deleted ideas keep their id, title and reason.
  - The card shows the reason, and an old declined idea with none shows "no reason recorded".
  - **"Copy new ideas" now lists what was declined or deleted since the last copy, with reasons.**
- **Counts (Part C), all small changes:**
  - `/api/summary` has `bugs_new`;
  - the Shard Console PLAY TESTS tile detail ends "...; 1 new idea; 1 new bug";
  - Homepage's Play tests widget has a "New bugs" field;
  - the shared menu's badge counts ideas plus bugs.
- **Tests:**
  - Python: **42 / 42** (16 new in `test_bug_reports.py`, plus P90's 12 and P85's 14);
  - Console: **245 / 245**, with 1 new fact.
  - All seen red first. Four guarded rules were also broken by hand and caught.
- **A small P90 bug fixed:** a hidden badge still showed "0". The `.badge { display: inline-block }` rule beat the
  `hidden` attribute. It showed on the new Bugs tab with no reports, and Ideas had the same latent bug.

## How to use it

- **Mid-session, from scratch:** open the **Bugs** tab, type a title (the rest is optional), add a screenshot (pick a
  file, or paste with Ctrl+V or a long-press), and tap Add bug.
- **From a play test:** tap **Bug from this** on its card. The tab opens with the play test linked and the cursor in
  the title.
- **From a Fail:** mark the play test Fail with its note, then answer **OK** to "Report a bug for this?". The note is
  already in "What happened". Cancel skips it.
- **Sending to the overseer:** on the Bugs tab, tap **Copy new bugs** and paste into the overseer chat. Answer OK to
  mark them taken. When the overseer gives a number, tap **Became D-NN** and type it, say `D93`.
- When a D-row closes, tap **Fixed**. For a repeat, tap **Duplicate** and give `D89` or `B-003`. For something that is
  not a bug, tap **Not a bug** with a one-line reason.

## What changed

`D:\UO\shard-migration`:
- `tools/bugs.py` (new): the store and rules, beside `ideas.py` and built like it.
  - Data is `testing\bug-reports.json`: `schema`, `nextId`, `copiedAt`, `bugs`, `deleted`, in a fixed key order;
    each report has a fixed key order too, including an empty `by` for later logins.
  - The stored counter never falls behind an existing or deleted id.
  - Writes go through the same `playtests.Lock` and temp-plus-rename.
  - Screenshots are checked by their bytes (PNG or JPG magic), never by name: at most 2 MB, 3 per report, named
    `B-001-1.png` and on.
  - Deleting a report deletes its screenshots.
- `tools/ideas.py`: delete needs a reason and keeps a `deleted` record; `copiedAt` is set when copied ideas are
  marked taken; the copy text adds the declined and deleted since then.
- `tools/tests/test_bug_reports.py` (new), and `tools/tests/test_feature_ideas.py` updated for the new keys and
  reasons.
- `README.md`, `dashboard.html`, `tools/progress.json`: `progress.py`, for the menu change in `nav.js`.

`D:\ShatteredLegacy`:
- `docker/test-queue/server.py`:
  - `/api/bugs`, `/copy`, `/file/<name>`, `/add`, `/edit`, `/status`, `/taken`, `/delete` and `/shot`;
  - `bugs_new` in the summary;
  - `/api/ideas/delete` takes a reason;
  - a 3 MB body limit for `/shot` only (16 KB elsewhere, unchanged).
- `docker/test-queue/html/index.html`: the Bugs tab, Bug from this, the Fail offer, the idea reasons, and the badge fix.
- `docker/test-queue/html/nav.js`: the menu badge counts both.
- `docker/test-queue/docker-compose.yml`: mounts the test world folder **read only** at `/data/testworld`, for
  `shard-commit.json`; adds `SHARD_DEPLOYED` and `PLAYTESTS_HOST_ROOT`.
- `docker/uo/Start-TestShard.ps1`: the record it writes after a healthy start (cc-P96) now has `version`, taken from
  the shard's own `[ShardVersion] Shattered Legacy <version>` start line.
- `docker/dashboard/config/services.yaml`: "New bugs".
- `scripts/Shard-Console.ps1`, its tests: `Get-NewBugCount` and the tile detail.
- `docker/test-queue/README.md`, `CHANGELOG.md` (2026.10.14.4, one `### Staff` line), `VERSION`.

## Tests

**Red first:**
- Python, with the new tests added, `ideas.py` at HEAD and `bugs.py` moved aside: `FAILED (failures=2, errors=2)`.
  The new file could not import `bugs`. P90's updated facts failed on the old `ideas.py` (no `deleted` key; `delete`
  takes no reason), and the service would not start.
- With `bugs.py` back and the page not yet built: `Ran 28 tests ... FAILED (failures=3)`, the three page facts.
- Console: `P97_NewBugsAreAddedToThePlayTestsDetailBesideTheIdeas` failed with `expected [... 18 passed; 1 new idea;
  1 new bug] but got [... 18 passed; 1 new idea]`.

**Green:**
- `python -m unittest tools/tests/test_bug_reports.py tools/tests/test_feature_ideas.py
  tools/tests/test_status_dashboard.py`: **Ran 42 tests, OK.**
- `Shard-Console.Tests.ps1`: **245 facts, 245 passed, 0 failed.**

**Broken on purpose, then restored and `cmp`-identical:**
- "not a bug" without a reason;
- ids counted without the deleted ones;
- the PNG/JPG check removed.

Four facts went red (status rules, retired id, screenshot types, the service route) and were green again once restored.

| The prompt asked for | Fact |
|---|---|
| add, edit | `test_add_fills_every_field_with_stable_pretty_json`, `test_bad_input_is_refused_and_nothing_is_written`, `test_edit_changes_only_what_is_given` |
| each status with its required field | `test_each_status_needs_what_it_says` |
| delete with reason, retired id not reused | `test_delete_needs_a_reason_keeps_it_and_retires_the_id` |
| screenshot too big, wrong type | `test_screenshots_png_and_jpg_only_2mb_at_most_three_per_report`, and over the API in `test_add_screenshot_copy_status_delete_and_count` |
| "Bug from this" link | `Page.test_bug_from_this_on_every_play_test_card` (wiring), and the browser run |
| the Fail prompt | `Page.test_marking_a_fail_offers_a_bug_report_prefilled` (wiring), and the browser run |
| Copy output | `BugCopyText.test_the_format_for_the_overseer` (byte for byte), and over the API |
| the Ideas reason rule | `IdeaReasons.test_declining_and_deleting_need_a_reason_that_is_not_only_spaces`, `ServiceRoutes.test_an_idea_delete_needs_a_reason_over_the_api` |
| old declined ideas without a reason | `IdeaReasons.test_the_copy_lists_what_was_declined_or_deleted_since_with_its_reason` (an old file, no `deleted` or `copiedAt` key, loads; prints "no reason recorded") |

**The page facts read the page as text**, so they check wiring, not behavior. Behavior was checked in the browser.

**In the browser** (the built-in browser, scratch service on a copy of the real `play-tests.json` and
`feature-ideas.json`):
- **375 px, dark:**
  - no console errors and no sideways scroll;
  - 174 "Bug from this" buttons beside 174 "Idea from this";
  - "Bug from this" on `P96-0` opened the Bugs tab with `P96-0` linked and the title focused below the sticky header
    (title top 353 px, header bottom 253 px);
  - a PNG made on a canvas and pasted through a real `paste` event went into the form;
  - Add bug saved B-001 with `B-001-1.png`, severity `wrong` and version `2026.10.14.2 (test shard, 61db33c)`;
  - the header read "1 new bug" and the tab badge 1.
- **Fail offer:** marking `P96-0` Fail showed "P96-0 marked Fail. Report a bug for this?". OK opened quick add with
  `P96-0` and the note "Smelting gave no ingots".
- **Reasons:**
  - "Not a bug" with only spaces: "'Not a bug' needs a reason." Nothing sent.
  - Became D-NN with `D93`: `taken D93`.
  - Delete with an empty reason: refused.
  - An idea's Delete with spaces: refused.
- **Copy new bugs:** gave the B-002 block (with "Linked play test: P96-0 (P96: checklist not parsed, read the
  notes)"), then marked it taken, pending its number.
- **375 px, light:** readable, every button at least 44 px tall. **Desktop:** the card with its screenshot thumbnail.

The Dashboard's "New bugs" widget field and the menu badge on `/status` are **not verified** until the service
restart.

## Repo size

- Screenshots are capped at 2 MB each by the server (a fact), well under 5 MB, and are committed with the reports by
  design.
- Lock and temp files are ignored: `git check-ignore -v` shows `testing/.gitignore:2:*.lock` for
  `bug-reports.json.lock`, and `testing/.gitignore:3:*.tmp` for `bug-reports.json.tmp` and
  `bug-reports/files/B-001-1.png.tmp`. A `.png` itself is not ignored.
- The scratch data copy (41 MB) was in the session scratchpad and has been deleted.

## Deviations and decisions for Chase

- **The server does not re-encode screenshots.** The service is standard-library Python (`python:3-alpine`), with no
  image library. So the **page** re-encodes: a PNG or JPG of 2 MB or less goes as it is; anything larger, or another
  format the browser can draw (a HEIC from an iPhone, say), is redrawn as a JPG at 85%, shrinking until it fits. The
  server checks the bytes and refuses anything that is not PNG or JPG or is over 2 MB.
- **"The shard version currently deployed"** means the **test shard's**: the version it printed at its last healthy
  start, with the commit, for example `2026.10.14.2 (test shard, 61db33c)`.
  - There is no other source: live publishes no `status.json` (the console says "NOT PUBLISHING").
  - It comes from `shard-commit.json`, which `Start-TestShard.ps1` now writes with the version.
  - To read it, the service mounts the test world folder **read only**. That folder also holds the test save, but no
    route serves anything from it except that one file.
  - Without a record, a report says "(unknown)".
- **The "taken" status covers both of the prompt's meanings:** "taken, pending number" (no D-number yet) and "became
  D-NN" (with the number), both under the one status `taken`.
- **Duplicate takes a D-number or a `B-NNN`**, and refuses itself.
- **A deleted report or idea keeps its id, title and reason** in the file under `deleted`. "Delete requires a reason" is
  only useful if the reason survives the delete. Its screenshots are deleted.
- **"Copy new ideas" with reasons:** only declined or deleted ideas changed since the last copy that was marked taken,
  so a reason is reported once, not on every copy.
- **The Fail offer uses the browser's own confirm box**, like the existing Fail note prompt: one tap to skip.
- **No camera button.** The file picker on a phone offers the camera roll and the camera itself; `capture` would force
  the camera and lose the roll.
- **`by` is recorded and empty**, as asked, until P89's login.
- **The menu badge counts ideas plus bugs**, with a tooltip naming both. One badge per menu entry is all `nav.js` has.

## For Chase

**Deploy (one step):**

```
cd D:\ShatteredLegacy\docker\test-queue; .\Start-TestQueue.ps1
```

This recreates only `sl-play-tests`, so the Bugs tab, the new mount and the routes go live. Homepage shows "New bugs" on
its next reload, and the Shard Console shows the count on its next refresh.

The test shard's version on reports comes from its last healthy start. It is there now (2026.10.14.2); a restart
through `Start-TestShard.ps1` or the console keeps it current.

**And the live container** (top of this note): it waits at `Delete the object and continue? (y/n/a)` since 08:06. Your
call: whether live is meant to be running, and how to answer.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`:
- code has 11 files pending (the list under "What changed");
- docs has 7 (`README.md`, `dashboard.html`, `tools/ideas.py`, `tools/progress.json`,
  `tools/tests/test_feature_ideas.py`, `tools/bugs.py`, `tools/tests/test_bug_reports.py`, plus this note once written).

```
Repo Result
---- ------
code dry run
docs dry run
```

P97 DONE
