# cc-P90: Feature ideas section on the play-test page

Prompt: `D:\UO\cc-prompts\cc-P90-feature-ideas.md`. Builder (the `sl-play-tests` service and page; no shard build).
Not committed (autopilot commits after DONE).

**Start state.** The code repo was clean. The docs repo had only `testing\SUMMARY.md` and `testing\play-tests.json`
modified: the live importer adding P89's entry after the P89 commit. That is machine output, so I went ahead.

**Changed by someone else during this task (not mine, not touched).** At about 10:48 local, the overseer edited:
- `docs\feature-queue.md` (4 lines: "faithful port comes first");
- `tools\progress-state.json`;
- and added `notes\passdown-overseer-2026-10-13.md`, `notes\port-list-2026-10-13.md` and `.json`.

**The autopilot will commit them with P90** unless Chase commits them first. The P85 tests I ran use temporary folders
only (`test_status_dashboard.py:30,125`), so none of those changes came from a test run.

## Headlines

- **An Ideas tab on the play-test page**, next to Open, Failed and All, with a badge counting new ideas. It has:
  - quick add: title (required), area pick list, optional linked play test, details;
  - an **"Idea from this"** button on every play-test card, which opens quick add with that item linked and the cursor
    in the title;
  - the list, newest first: status changes, edit, delete;
  - **"Copy new ideas"** for the features chat, which then offers to mark them taken;
  - the real feature queue below, read only, with a filter box.
  - Everything is tap-sized, checked at 375 px, in light and dark.
- **Storage:** `testing\feature-ideas.json`.
  - Ids `I-001` and on come from a **stored counter**, so a deleted id is never reused. (Play tests' own `M-NNN` uses
    "highest plus one", which would reuse a deleted last id; the ideas do not copy that.)
  - Pretty-printed with a fixed key order, temp file plus rename, under its own lock file, through the same `Lock` class
    as `play-tests.json`.
  - The rules are in `tools\ideas.py`, beside `playtests.py`, in the folder the service already mounts.
- **The F-NN parser on the real `docs\feature-queue.md`: 43 entries, 42 Open and 1 Dropped (F-2); 19 also listed as
  batched.**
  - Every one of the 42 `### F-NN:` headings is found, with a clean title and its added date.
  - **The prompt's "F-44 is the newest" is not what the file says.** F-43 is the newest entry, and the file says
    "Next free: F-44".
- **New-idea counts show in four places:**
  - the page header ("2 new ideas", tappable) and the Ideas badge;
  - **the shared menu**: a badge beside Play tests, on the play-test page, and on Shard status once served by the same
    service;
  - `/api/summary` `ideas_new`, and Homepage's Play tests widget ("New ideas");
  - the Shard Console PLAY TESTS tile detail ("...; 2 new ideas"). The tile's word and color are untouched.
- **Haven:** `feature-ideas.json` sits beside `play-tests.json`, is written by the same service with the same rules,
  and is read the same way. So whatever P89 decides for one covers both: Haven the only writer, mirrored into git at
  commit. P89's H1 must add it to `/api/export`.
- **Tests:**
  - **12 new Python facts**, all green;
  - the P85 suite green again (26 together);
  - Console **211 / 211**, with 1 new fact;
  - importer Pester **20 / 20**.
  - Every new fact went red when broken on purpose, **including the concurrent-write fact, which at first did not**
    (see Proof).
- **Fixed along the way, a P88 regression of mine.** `test_status_dashboard.py`
  `test_the_page_links_never_say_localhost` had been red since P88, because the inlined `nav.js` comment contained the
  word "localhost" and the old `data-port="3000"` header link was gone.
  - I reworded the comment, and updated the test to check the menu's Dashboard entry instead.
  - I had not run that suite in P88.
- **Nothing was restarted.** Tested on a scratch container (`192.168.1.58:18093`, a copy of the data), now removed.

## The Ideas section

**A tab rather than its own page,** because:
- it keeps "Idea from this" a single tap on the same page, mid-session on a phone, with no page load and no lost
  scroll;
- the menu stays three items;
- under P89's plan everything stays on one hostname behind one login.

| Part | What |
|---|---|
| Quick add | Title (140 characters, required), Area (crafting, combat, skills, guilds, League, companions, world, client/UI, staff tools, other, or none), From play test (`P71-3`, `T-012` or `M-001`; checked), Details (2,000 characters, line breaks kept). |
| Duplicate hint | While typing the title, "Similar:" lists up to 3 feature-queue entries or ideas sharing **2 or more significant words** with it, or **1** when the title has only 1 or 2 such words. Significant means 4+ letters, lowercased, not in a short stop list (with, that, from, idea, feature and so on). A feature-queue hit links to its row below. Example: "Mining boots for mountains" shows F-36 "Climbing boots, mining the unreachable mountain blocks". |
| Idea from this | On every play-test card. It opens the Ideas tab, fills From play test, and puts the cursor in the title, scrolled below the sticky header. |
| The list | Newest first. Each card shows id, area, date, status and a "from P71-3" link (back to that card on the All tab). Buttons: Taken to features chat, Became F-NN (asks the number; the card then links to that F entry), Declined (asks a one-line reason), Back to new, Edit (inline form), Delete (asks first; "its number is never reused"). |
| Copy new ideas | Fetches `/api/ideas/copy`, shows the text in a box, and copies it. The Clipboard API needs https, so on the LAN it uses the selected box with `execCommand('copy')`, and the box stays for a manual copy. Then: "Mark these N idea(s) as taken to the features chat?" |
| Feature queue | Every F entry under its section heading, with the added date and the batch prompts. A filter box filters by words or F-number. Each row has an anchor, `#f-36`. |
| Older service | Until `sl-play-tests` is restarted, the tab says "Ideas are not available: ... needs a restart (Start-TestQueue.ps1)". The rest of the page works as before. |

**Status keys:** `new`, `taken` ("taken to features chat"), `became` (needs `feature` `F-NN`), `declined` (needs a
`reason`). Back to `new` clears both.

**The copy text** (pinned by a test):

```
New feature ideas from the play-test page (2), for F-numbers or a decline:

I-001: Bare idea
Area: (none)
Linked play test: (none)
Description: (none)

I-002: Bank deposit from the pack
Area: crafting
Linked play test: P71-3 (Fill a BOD)
Description:
  Two lines
  of text
```

**Storage** (`testing\feature-ideas.json`):

```
{
  "schema": 1,
  "nextId": 3,
  "ideas": [ { "id", "title", "description", "area", "playtest", "status", "feature", "reason",
               "createdAt", "updatedAt", "statusAt" }, ... ]
}
```

On load, `nextId` is raised past any id in the file, so a hand edit cannot make it hand out an id twice. The file does
not exist until the first idea; the service and the Console treat a missing file as zero ideas.

**Routes** (`server.py`):
- `GET /api/ideas`;
- `GET /api/ideas/copy`;
- `POST /api/ideas/add`, `/edit`, `/status`, `/taken`, `/delete`;
- `/api/summary` gains `ideas_new`.

A bad input is a 400 with the reason. An unknown id is a 404.

## The F-NN parser

`ideas.parse_feature_queue` reads three shapes:
1. **`### F-NN: title (added YYYY-MM-DD)` headings,** under whichever `## ` heading holds them. The parenthesis goes
   from the title and its date becomes `added`. `(planned, added ...)` and `(added ..., was: ...)` are read the same
   way.
2. **The `## Batched` table:** every F-NN in a row's **first** cell is marked batched with that row's prompt. An F-number
   mentioned in the Notes column is not. F-8's row mentions F-21 to F-23 there, and they are correctly not marked.
3. **The `## Dropped` table:** an F-NN with no heading becomes an entry in section Dropped, titled with the first
   sentence of its reason.

**On the real file (2026-10-13, after the overseer's 10:48 edit; the result was unchanged by it):**

| Section | Entries |
|---|---|
| Open | 42 (F-1, F-3 to F-43) |
| Dropped | 1 (F-2) |
| **All** | **43**, of which **19** are also in the Batched table (F-1, 3, 5, 7, 8, 9, 11, 12, 15, 16, 17, 19, 22, 24, 27, 30, 31, 32, 33) |

Counted independently with `grep -c "^### F-[0-9]*:"`: 42 headings. Ids from the Batched table's first column match
the list above.

## Counts and where they show

| Where | What | How |
|---|---|---|
| Page header | "N new ideas" (tap: Ideas tab) | from `/api/ideas` |
| Ideas tab | badge N | the same |
| Shared menu | badge N beside **Play tests** | new `SLMenu.setBadge(key, n, title)` in `nav.js`. The play-test page sets it. Shard status, served by the same service, fetches `/api/summary` itself. Homepage, another origin, shows none (it would need CORS on the API) |
| `/api/summary` | `ideas_new` | `server.py` |
| Homepage Play tests widget | "New ideas" | `docker\dashboard\config\services.yaml`, a fourth mapping |
| Shard Console PLAY TESTS tile | detail "...; 2 new ideas" | `Get-NewIdeaCount` reads `feature-ideas.json` beside `play-tests.json`. The word and color stay the play tests' own. A missing or bad file adds nothing |

## Proof

**Python, `python -m unittest tools/tests/test_feature_ideas.py`: 12 facts.**
- **Behavior:** add, with stable JSON and no temp or lock file left; bad input refused with nothing written; edit;
  every status rule; mark taken only moves `new`; delete; **an id never reused**, even after deleting the last one,
  and even with a counter edited to fall behind.
- **Two writers at once:** two processes released together by an event, adding 80 ideas each. All 160 are kept, ids
  `I-001` to `I-160` in order, `nextId` 161.
- **Summary counts.**
- **The copy text format**, byte for byte.
- **The parser** on a sample of every shape, and **on the real file**.
- **The service routes:** `server.py` started on a free local port against a temporary root, with the real
  `feature-queue.md`. Add, a 400, a 404, list, copy, taken, `ideas_new` 1 then 0, became F-44, edit, delete, and the
  next id `I-002`.

**Red, on purpose** (a copy of `ideas.py` kept, then restored and `cmp`-identical). Four breaks:

| Break | Caught by |
|---|---|
| ids from "highest plus one" | `test_delete_and_an_id_is_never_reused`, `test_add_list_copy_and_count` |
| the title's "(added ...)" not stripped | both parser facts |
| the copy text's `: ` changed to ` - ` | `test_the_format_for_the_features_chat` |
| **the lock removed** | **not caught at first** |

- The first concurrency fact (2 x 15 adds) passed without the lock: the two processes barely overlapped.
- I rewrote it: both released by an event, 80 adds each. **Without the lock it failed on both runs** (a writer process
  died: exit code 1, not 0). With the lock it passed on 3 runs in a row.

**Console, `scripts\tests\Shard-Console.Tests.ps1`: 211 / 211** with the new
`P90_NewIdeasAreAddedToThePlayTestsDetailNeverToItsWord`.
- With `Get-NewIdeaCount` made to return 0, **210 / 211**, only that fact red ("expected [... 18 passed; 2 new ideas]
  but got [... 18 passed]").
- Restored, `cmp`-identical.

**Also:**
- the P85 suite, together with mine: **26 OK**;
- importer Pester (`Import-PlayTests.Tests.ps1`): **20 passed, 0 failed**;
- `progress.py` run: the menu block was refreshed with the badge code.

**In the browser** (the scratch service on the LAN address, the built-in browser):
- at **375 x 812, dark**:
  - the menu badge "2" and the Ideas badge "2";
  - "Idea from this" on a card filled the linked id, focused the title, and the title's top (301 px) sat below the
    sticky header's bottom (201 px);
  - typing "Mining boots for mountains" showed "Similar: F-36 Climbing boots, mining the unreachable mountain blocks
    (Open)";
  - 43 feature-queue rows;
  - Edit through the inline form saved a new title and area;
- **light, desktop**: readable;
- the page header showed "2 new ideas".

**Not verified:**
- the Shard status badge served by the same service: on the scratch port the menu's Play tests entry points at the
  live `:8093`, so it correctly did not fetch;
- Homepage's new widget field, until the service restart.

## Deviations and decisions for Chase

1. **"Edit or delete his own entries":** there is no login, so every entry can be edited or deleted by anyone on the
   page, as with play-test results today. P89's plan (Cloudflare Access, a `by` field per write) is where "own" becomes
   real.
2. **No menu badge on Homepage.** It would need the API to allow cross-origin reads (CORS). Its Play tests widget shows
   the count instead.
3. **The prompt said F-44 is the newest.** The file's newest entry is F-43, and F-44 is "Next free". Nothing depends on
   it.
4. **Delete is permanent** (the id is kept retired). If you would rather keep a trail, `declined` with a reason does
   that instead.
5. **The copy uses `execCommand('copy')` on plain http.** That is deprecated but works in current browsers. The text box
   is the fallback, and under P89's https the Clipboard API takes over by itself.

## For Chase

**Deploy (one step):**

```
cd D:\ShatteredLegacy\docker\test-queue; .\Start-TestQueue.ps1
```

This recreates only `sl-play-tests`, so the new routes go live. (It also brings P88's `/nav.js` live if not done yet.)
Homepage picks up the new widget field on reload. The Shard Console shows the count on its next refresh.

**How to use it:**
- **Mid-session:** on any play-test card, tap **Idea from this**, type a title, and tap Add idea. Or open the **Ideas**
  tab and add one from scratch.
- **Before adding,** glance at the "Similar:" line under the title, and the feature queue at the bottom (filter box).
- **For the features chat:** Ideas, then **Copy new ideas**, paste into the chat, and answer yes to mark them taken.
- When the chat assigns a number, tap **Became F-NN** and type it. Or tap **Declined** with a reason.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run after this notes
file was written:

```
=== code  (D:\ShatteredLegacy) ===
  9 file(s) pending: CHANGELOG.md, VERSION, docker/dashboard/config/services.yaml, docker/test-queue/README.md,
  docker/test-queue/html/index.html, docker/test-queue/html/nav.js, docker/test-queue/server.py,
  scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1
  dry run: would add, commit and push
=== docs  (D:\UO\shard-migration) ===
  14 file(s) pending: README.md, dashboard.html, docs/feature-queue.md, testing/SUMMARY.md, testing/play-tests.json,
  tools/progress-state.json, tools/progress.json, tools/tests/test_status_dashboard.py, notes/cc-P90-feature-ideas.md,
  notes/passdown-overseer-2026-10-13.md, notes/port-list-2026-10-13.json, notes/port-list-2026-10-13.md,
  tools/ideas.py, tools/tests/test_feature_ideas.py
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

**Pending files that are not mine:**
- `docs/feature-queue.md`, `tools/progress-state.json` and the three `notes/passdown-overseer-2026-10-13.md` and
  `notes/port-list-2026-10-13.*` files are the overseer's (see the top of these notes);
- `testing/*` is the live importer's.

Patch notes: `CHANGELOG.md` 2026.10.13.11 `### Staff` line (2026.10.13.10 was committed with P88), `VERSION`
2026.10.13.11. Wiki page not published.

P90 DONE
