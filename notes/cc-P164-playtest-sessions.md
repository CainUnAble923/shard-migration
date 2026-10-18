# cc-P164: Play-test page "Sessions" view: what to test, in small chunks

2026-10-18. Opus. Chase, 11:18: "the play test page is still intimidating, it would be nice for it to show what i need
to test in a similar fashion on how you give it to me in digestible chunks". Seeded from the overseer's
`D:\UO\overseer\playtest-plan-2026-10-18.md`. All three repos were clean at the start (P163 was committed). **CC never
connected to Haven**: everything ran on this PC, against scratch copies of the service.

## Headlines

- **The page opens on "Up next"**: one session at a time.
  - Each session shows its title, a one-line why, a progress line ("3 of 9 done") and a **Before you start** box.
  - Each item is a big card: the line to do, its **Pass** line, where it is done, and Pass / Fail / Later buttons.
  - Fail asks for its one line in the card itself, not a pop-up.
  - The id sits small under the card, never in the main line.
  - **Previous** and **Next** buttons move between sessions, and **All sessions** lists each with its count. A finished
    session collapses to one line with its date.
  - One line says what the bot and CC still owe ("Not yours: the overnight bot still owes 94 and CC 80").
  - **All items**, one tap away, is the old full list with its filters, unchanged (it remembers its last filter).
- **Phone first**, checked in headless Chrome at a 390 px wide viewport (iPhone width):
  - no sideways scroll;
  - every card button at least 52 px tall;
  - no tables.
- **`testing\sessions.json` is the overseer's file**, like `decisions-overlay.json`; nothing writes it. It is seeded with
  the 10-18 plan:
  - seven sessions (the plan's six, with its session 4 split into "Achievements button, [achievements and [version"
    and "Kitsune ears and tail refit", so each stays at 12 or fewer);
  - the "Probably stale" list with a reason for each;
  - `superseded: P62` (replaced by P138).
- **Every other open item of Chase's goes into automatic sessions**, so nothing is lost:
  - grouped by Where (Admin, then Player by character, then Outside);
  - then whole prompts, newest first, at most 12 a session; a prompt is split only when it alone has more than 12.
  - Bot, CC and question items never show in any session, whatever the file says.
- **Today, on the real data** (a scratch copy, with the real deploy record):
  - 15 sessions: 7 seeded, 7 automatic, and Probably stale;
  - 140 items, each in exactly one session;
  - Up next is **Rootdeep Burrows and the tutorial**, 0 of 9 done;
  - Bulk orders reads 5 of 8 done and Creatures 3 of 7, from Chase's own marks today;
  - Probably stale has 27 items: the 8 listed, P62-2 to P62-6, the rest from the rules.
- **The "needs:" tags.**
  - **"needs: rebuild test shard"**: an in-game item whose prompt was imported after the test shard was last deployed.
  - **"needs: newest player package"**: an item that names the player package or Build package. A package record can
    clear it, but none exists yet (Deviation 3).
  - Today no item needs a rebuild: the 16:20 deploy is newer than every import.
  - **On Haven** the page had no deploy record at all. The game PC's every-minute snapshot now carries it
    (`testShard`), and the service reads it there. That also fixes the "(unknown)" version on bug reports made on Haven.
- **Probably stale**: one tap marks an item Later with its reason ("probably stale: ..."); **Mark all Later** does the
  whole group in one write. The rules are:
  - the prompt is superseded in the overseer's file;
  - a "checklist not parsed" placeholder;
  - the steps name the game PC's old page addresses (`192.168.1.58:8093` or `:3000`);
  - the overseer's own list.
- **Tests**:
  - 14 new facts in `tools/tests/test_playsessions.py`, one of them a real browser test (Selenium, headless Chrome,
    390 px) that is now part of the suite;
  - every one seen failing first;
  - seven targeted breaks of the builder, each caught.
  - Three older pins of "Open is the default" were updated to the new default.

## What changed

D:\UO\shard-migration (uncommitted):

| File | Change |
|---|---|
| `tools/playsessions.py` (new, 321 lines) | The builder. `load` :56 (the sessions file, notes clone first); `load_package` :71; `is_chase` :89; `steps_fit` :105 (the hand-written steps go on a card only when they fit the item: see Deviation 2); `words` :119; `needs` :146; `stale_reason` :158; `session_item` :169; `finish` :182 (progress, finished, date); `auto_sessions` :205; `annotate` :256 (seeded, then Probably stale, then automatic; Up next; owed). `MAX = 12` :42 |
| `testing/sessions.json` (new) | The seed: 7 sessions, the stale list, `superseded` |
| `tools/playtests.py` | `set_later_many` :560: several items Later, each with its own note, in one write under the lock; every id must exist or nothing changes |
| `tools/tests/test_playsessions.py` (new) | 14 facts (below) |
| `tools/tests/test_bot_tonight.py`, `test_decisions.py`, `test_play_who.py` | Their pin `var filter = 'open';` (and Open pressed) is now `var listFilter = 'open';` and Open not pressed: the full list's default is still Open, and the page opens on Up next |
| `notes/haven-runbook.md` | The game PC section: the snapshot also carries the test shard's deploy record |

D:\ShatteredLegacy (uncommitted):

| File | Change |
|---|---|
| `docker/test-queue/server.py` | Header :19-21; `import playsessions` :124 and in `MODULES` :127 (code reload); `deployed_record` :244 (the file, else the snapshot's `testShard`), which `deployed_version` now uses; `/api/items` adds `sessions` :359-363 (a failure leaves the page on its full list); `POST /api/sessions/later` :466 |
| `docker/test-queue/html/index.html` | CSS :121-160; the **Up next** and **All items** buttons :174-176; opens on Up next :259; `sessionCard` :559, `renderNext` :581, `sessionClick` :617; the filter click and the list click :668, :674. ASCII |
| `docker/test-queue/README.md` | `POST /api/sessions/later`, and `testing/sessions.json` in "Where the data is" |
| `scripts/Publish-GamePcSnapshot.ps1` | `-TestShardRecord` :20; `testShard` (commit, version, at from `server\lib\uo\modernuo-test\shard-commit.json`, or null) :115-121, :130 |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.18.9`, one `### Staff` line; VERSION 2026.10.18.8 -> 2026.10.18.9 (the .8 section was committed with P163) |

## Tests

**`tools/tests/test_playsessions.py`, 14 facts, all pass:**

| Class | Fact |
|---|---|
| Builder | a seeded session keeps its order and never shows Bot or CC; a finished item leaves Up next, and a finished session collapses with its date; automatic sessions cap at 12, keep prompts together, newest first, lose nothing; needs: rebuild only after the deploy and only in game, no guess without a record, package cleared by a newer record; the stale rules (superseded, unparsed, old address, listed; not the Haven address, not a seeded or Bot item; never Up next while a real session is open); card words use the steps only when they fit; no sessions file still gives automatic sessions; several items Later in one write, or none |
| Service | `/api/items` carries the sessions (seeded order, the Bot item left out, stale, automatic, the rebuild tag, owed, the deploy record); `/api/sessions/later` (200, 404 for an unknown id, 400 for none); a stale group finishes; Pass moves the progress |
| ServiceOnHaven | no test world: the deploy record comes from the game PC snapshot, and a bug report carries the version |
| Browser | headless Chrome at **390 px**: Up next opens even when the last filter was All; title, Before you start, "0 of 3 done"; no sideways scroll; Where chips hidden; no id in the main line, id under the card; buttons at least 44 px; the owed line; **Pass on a card is recorded** in `play-tests.json` and the progress reads "1 of 3 done"; the Fail box waits for Fail, then saves its note; Next goes to the next session (with its rebuild tag); All items shows the full list |
| Page | opens on Up next, ASCII |
| RealFiles | the seed names real items, once each, 6 to 12 a session; it is the 10-18 plan |

**Seen failing first:**
1. With `playsessions.py` moved aside and the old `server.py`, `index.html` and `playtests.py` in place: **14 of 14
   failed**, all on the "playsessions.py does not exist" guard. Everything was restored and SHA-256 checked OK.
2. With the new builder but the old service, page and `playtests.py`: **5 failed for their own reasons**:
   - `set_later_many` missing;
   - `KeyError: 'sessions'` (twice);
   - "timed out waiting for the session" in the browser;
   - `var filter = 'next';` not found.

   Everything was restored and SHA-256 checked OK.
3. **Seven targeted breaks** of the builder, each run against the fact aimed at it, file restored byte-identical
   (checked):

   | Break | Result |
   |---|---|
   | cap 13 | FAILED |
   | Bot and CC kept in seeded sessions | FAILED |
   | Later not counted as done | FAILED |
   | rebuild before the deploy | FAILED |
   | no superseded rule | FAILED |
   | steps always fit | FAILED |
   | oldest prompts first | FAILED |
4. The **first green run** failed 4 facts on real bugs of mine:
   - the placeholder and package rules read only `text`, but items also carry their words in `what`;
   - a stale group vanished once all its items were Later, instead of collapsing.

   Both were fixed in the module.
5. The real-data look (below) found that the **Fail note box showed on every card**: my `display: flex` beat the
   `hidden` attribute. I added an assertion first, saw it fail on the old CSS ("the note box waits for Fail"), then
   fixed the CSS.

**Full suites:**
- **shard-migration `tools/tests`: 165 tests, 2 failures.** Both are `test_play_who.RealFiles`, on the real data:
  `M-001`, a manual item added at 16:59 today, has no Who in `bot-triage.md` and no Where. That is data, not this
  prompt's code (Deviation 5).
- Importer Pester `Import-PlayTests.Tests.ps1`: **20 of 20**.
- Bot suite `D:\ShatteredLegacy\tools\playtest-bot\tests`: **40 of 41**. The failure is the known environmental
  `test_installer_dry_run_prints_the_call_and_registers_nothing` (the nightly task is installed), as P112, P115 and P146
  recorded.
- Console facts that read the snapshot script (filter `Snapshot|P107_|P112_|P133_`): **25 facts, 24 pass**.
  `P133_TheSnapshotReports...` and `P107_TheSnapshotSendsNothing...` pass. The failure is
  `P107_LinksAndSitesPointAtHaven...`, the known Haven-mode one (P133's and P163's notes).
- The whole console suite was not run again: nothing else in it reads the files this prompt changes.

**Real data, in a real browser** (`<scratchpad>\p164_real.py`):
- **Setup:** the new service on a scratch copy of today's `notes`, `docs` and `testing`, port 18164, with the real deploy
  record.
- **Results:** the session counts in the Headlines; `innerWidth` 390 and `scrollWidth` 390; 9 cards on Rootdeep; the
  console shows only the old `/favicon.ico` 404.
- **Screenshots, in the scratchpad (not in either repo):**
  - `C:\Users\ckfle\AppData\Local\Temp\claude\D--UO-shard-migration\b5d55b25-7f92-4308-96ef-424474cfe47f\scratchpad\p164-phone-top.png`
  - `C:\Users\ckfle\AppData\Local\Temp\claude\D--UO-shard-migration\b5d55b25-7f92-4308-96ef-424474cfe47f\scratchpad\p164-phone-cards.png`
  - `C:\Users\ckfle\AppData\Local\Temp\claude\D--UO-shard-migration\b5d55b25-7f92-4308-96ef-424474cfe47f\scratchpad\p164-phone-stale.png`
  - `C:\Users\ckfle\AppData\Local\Temp\claude\D--UO-shard-migration\b5d55b25-7f92-4308-96ef-424474cfe47f\scratchpad\p164-pc.png`
- The scratch service was stopped.

## Deviations and decisions for Chase

1. **"The prompt's commit date" is the prompt's import time.** The service on Haven has no git (python:3-alpine), so it
   cannot ask when a prompt was committed. The importer picks a prompt up within a minute of its DONE, and the Golem
   commits right after, so `importedAt` stands in. An in-game item whose prompt was imported after the test shard's
   deploy record (`at`) gets "needs: rebuild test shard". Outside items never get it.
2. **P140's hand-written steps are one item off.**
   - `testing/playtest-steps.json` numbers P140 the way its notes do, which the importer cut one short (P146 noted
     P140-8 never imported). So P140-6's steps describe P140-5's item, and so on.
   - The cards use the steps only when they share words with the item (or the item is a "not parsed" placeholder).
     Otherwise they use the notes' own words. A fact pins it.
   - **For the overseer:** the same shift probably puts P140's Who and Where rows in `bot-triage.md` one off too.
     Worth fixing in the triage and the steps (not done here: both are hand-written files, and this prompt did not own
     them).
3. **No record of the published player package exists**, so "needs: newest player package" goes by the item's own
   words. The builder already reads `testing/package-published.json` (`{version, at}`) if something writes it, and a
   newer package clears the tag. Having Publish write it is a small later step.
4. **Probably stale is not capped at 12.** It is a group to clear with one tap ("Mark all Later"), not a sitting, and
   today it holds 27. Each item's reason is saved as its Later note ("probably stale: ...").
5. **`M-001` (added by hand at 16:59 today) has no Who or Where**, so two real-file facts fail (P115's and P146's).
   Someone needs to add a row for it to `testing/bot-triage.md` (its text is P122-3's tailor check, so EYES, Player).
   It also stays out of sessions until it has one.
6. **The snapshot change is already live on the game PC.** The installed `SL game PC snapshot` task runs
   `Publish-GamePcSnapshot.ps1` from the working tree, so it began sending `testShard` the next minute. Haven's
   current service stores the extra field and ignores it until it pulls the new code. I checked the script's dry run;
   P133's and P107's snapshot facts pass.
7. **Seeded sessions keep their finished items** (Bulk orders reads 5 of 8, with the done ones as compact cards), so a
   session shows its whole sitting. Items marked Later count as done in a session and stay in All items.
8. **No task list for Chase.** This session had no task-list tool (ToolSearch found none), as P146 also recorded.
9. **The Read tool** was not needed on any denied file this time. I patched the shard-repo files by script files
   (each replacement asserted to match once), as the memory notes advise.

## For Chase

**After Haven pulls it** (within a few minutes of the Golem's push; P137 reloads the code by itself), open
`http://haven.tail81098d.ts.net:8093/`.

On the **iPhone**:
- the page opens on **Up next: Rootdeep Burrows and the tutorial, 0 of 9 done**;
- above the cards is a **Before you start** box (rebuild the test shard; log in as Admin, then a fresh tutorial
  character);
- then nine big cards, each with one line to do and its **Pass** line;
- tap **Pass**, **Fail** (type one line, then Save Fail) or **Later**; the card shrinks to one line and the count
  moves;
- **Next** and **Previous** walk the sessions: Bulk orders, Creatures and combat, Achievements button, Kitsune,
  Legion scripts, Staff tools, then the automatic ones;
- at the bottom: the line about what the bot and CC owe, and **All sessions** with their counts;
- **All items** at the top is the full list, exactly as before.

On the **PC** it is the same page in one column.

The last session is **Probably stale** (27). Read each; **Later: stale** saves it with its reason, or **Mark all ...
Later** does them all.

**How the overseer adds a session:** edit `D:\UO\shard-migration\testing\sessions.json` and commit.
- Add an entry to `sessions`:

  ```
  { "id": "a-short-id", "title": "...", "why": "one line", "before": ["...", "..."],
    "items": ["P150-1", "P150-2"] }
  ```

  with 6 to 12 item ids in order. The first session that lists an item gets it.
- An item goes stale with `"stale": {"items": [{"id": "...", "reason": "..."}]}`, or a whole prompt with
  `"superseded": {"P70": "why"}`.
- The page reads the file on every load. Items in no session keep turning up in the automatic ones, so nothing is
  missed.
- The fact `RealFiles` checks the ids exist, each appears once, and each session has 6 to 12 items.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

- No repo BLOCKED.
- `code`: this prompt's 6 files.
- `docs`: this prompt's 8 files and these notes, plus `testing/SUMMARY.md` and `testing/play-tests.json`. Those two
  are the mirror refresh from Haven, machine output.
- No file over 5 MB. All scratch is in the session scratchpad, outside both repos.

P164 DONE
