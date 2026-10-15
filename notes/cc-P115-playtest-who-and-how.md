# cc-P115: Every play-test item says who tests it (Chase, the bot, or CC), what to do, and how

2026-10-15. Prompt: `D:\UO\cc-prompts\cc-P115-playtest-who-and-how.md`. The play-test data, service and page, plus a
re-sort of every open item. Nothing deployed: the running `sl-play-tests` needs a restart (For Chase). Not committed
(the Golem commits after DONE). Both repos were clean at the start, apart from the importer's machine output.

## Headlines

- **All 219 open and blocked items have exactly one Who** (218 open, 1 blocked; 2026-10-15). Before this, 56 had none.
  The prompt's "212 open" was the overseer's count at 20:11; seven more arrived since (P113, P114).

  | Who on the page | Bucket | Items |
  |---|---|---|
  | **You** | EYES 17 + DEPLOY 31 | **48** |
  | **Bot, then you** | BOT-PARTIAL | **17** |
  | **You decide** | DECISION | **14** |
  | **Bot** | BOT | **80** |
  | **CC** | CC (new) | **60** |
  | | **All** | **219** |

  - **Mine** (You + Bot, then you + You decide) is **79**. That is all that needs Chase.
  - The page's header counts were checked against the triage's own Counts table: they match.
- **Every item has plain steps**, kept beside the item's own what/expect, which are never changed:
  - **Chase's items** get **Where** (shard, desktop shortcut and character, console tab or web page), **Do** (at most
    four lines, staff commands typed exactly) and **Pass looks like**.
  - **Bot and CC items** get one **Check** line: what is looked at and where the result shows.
  - **Bot, then you** items get both: the bot's check, and Chase's half.
  - **"Steps unknown": none.** Every item's steps were worked out from its notes and the code.
- **Where Who lives: `testing/bot-triage.md`**, still the single source, now with a CC bucket and the new counts.
  - **The steps:** a new hand-written overlay, `testing/playtest-steps.json`, keyed by item id.
  - **The service merges both into `/api/items` on every read** (`tools/playwho.py`). It writes nothing back.
  - **The importer never writes either file:** proven by a test that runs it twice over a copy of the real notes.
  - Reasons for this design are below.
- **The page:**
  - every card has a **Who badge** beside its id (and beside P112's robot, which is unchanged);
  - a **How to test** line opens the steps in one click, and it already shows the Where;
  - the header has a count per Who, and clicking one opens its filter;
  - new **Mine**, **Bot** and **CC** filter chips beside "Bot tonight", all off by default;
  - **the default view is unchanged:** Open, every item, today's order, nothing hidden or greyed.
- **Re-sorted, not just topped up.** 35 of the 163 items sorted on 10-13 changed bucket, most of them DEPLOY to CC
  (the work had since been done and left evidence); the list is below. P87-1 left the list (it has a result now).
- **The stale note is gone.** The triage's "items from P82 on cannot be checked" is out of date: cc-P95 fixed the boot,
  and last night's run tested HEAD (68631cb). P82-0 stays BOT, with a check sketch.
- **Tests:**
  - 15 new facts, each seen failing first; two more break-and-restore proofs for the real-files and importer facts.
  - shard-migration `tools\tests` **98 of 98**.
  - The bot's suite: 37 of 38, the same known environmental failure as P112 (the nightly task is installed).
- **The page in a browser,** on a scratch service with a copy of today's data:
  - 219 cards, 219 badges, 219 step blocks;
  - header counts You 48, Bot then you 17, You decide 14, Bot 80, CC 60;
  - Mine 79, Bot 80, CC 60;
  - no console errors and no horizontal scroll at phone width.

## Why the triage plus an overlay

- **One source for Who.** The prompt asks for `bot-triage.md` to stay the single source. The overnight bot's plan
  already reads it (`uobot/tonight.py`, BOT and BOT-PARTIAL are "bot-checkable"). Putting Who anywhere else would give
  two answers that drift.
- **The steps do not fit a markdown table.** Up to five lines per item with Where, Do and Pass look unreadable in a
  table cell, so they live in a JSON overlay keyed by id. It is the "small overlay" the prompt allows, and it holds
  no Who. Missing steps never hide an item.
- **Safe from the importer by construction.** `tools/playtests.py` writes only `play-tests.json` and `SUMMARY.md`.
  Who and steps are merged in when the service reads, and `play-tests.json` never holds them (a service test asserts
  it). So no importer change could wipe them.
- **Edits show without a restart.** The triage and the steps are re-read when their modification time changes.
- **Haven mode:** the files are read from the notes clone first, where they are committed, and then from the data
  volume. On Haven, `testing/` is a separate volume seeded from the game PC.
- **The bot is unaffected.** Its row pattern lists the five old buckets, so CC rows are simply not bot-checkable. It
  reads **97** ids from the new triage, which is 80 + 17.

## What changed, with file:line

**shard-migration**

| File:line | Change |
|---|---|
| `testing/bot-triage.md` | rewritten for 2026-10-15: a bucket table with the page's Who for each, the CC bucket, the "single source" paragraph, the corrected "code under test" note, the counts, then 219 rows by prompt group. The "Checks built" and "Not built yet" sketch sections are kept as they were |
| `testing/playtest-steps.json` (new) | `{schema 1, about, items: {id: {where, do[], pass} or {check} or both}}`, 219 entries, ASCII |
| `tools/playwho.py` (new, 113 lines) | `BUCKETS` (bucket -> key, label, kind), `parse_triage`, `load_sources(roots)` (first root with each file; cached by mtime and size), `annotate(doc, triage, steps)` (who and steps on open, later and blocked items; `doc["who"]` with counts, mine, unsorted, buckets, labels; an open item missing from the triage is "Not sorted yet"; no triage means `available: false` and no badges) |
| `tools/tests/test_play_who.py` (new) | 15 facts, below |

**Shard repo (`D:\ShatteredLegacy`)**

| File:line | Change |
|---|---|
| `docker/test-queue/server.py:8` | docstring: what `/api/items` now carries |
| `docker/test-queue/server.py:107`, `:293-299` | `import playwho`; `/api/items` annotates the document from `[args.root, DATA]`. A failure there becomes `who.available: false`, never a 500 |
| `docker/test-queue/html/index.html:51-59` | CSS: `.who` badges (You solid blue, Bot then you outlined blue, You decide amber, Bot grey, CC neutral, Not sorted dashed), the header Who counts, the steps block |
| `docker/test-queue/html/index.html:121-123` | the Mine, Bot and CC filter buttons (off by default; `filter` still starts at `open`) |
| `docker/test-queue/html/index.html:216-224` | `MINE`, `whoKey`, and the three filters in `shown()`. Each shows open, later and blocked items only, as Open does |
| `docker/test-queue/html/index.html:249` | the Who counts appended to the header. `botCount();` is left exactly as P112 pinned it |
| `docker/test-queue/html/index.html:291-321` | `whoBadge` (tooltip: label, kind, the triage's reason), `whoCounts` (a count per Who; Not sorted shown only when there are any), `stepsHtml` (a closed `<details>`, "How to test: <Where>", then Steps unknown / Where / Do / Pass looks like / Check) |
| `docker/test-queue/html/index.html:325-326`, `:339` | the badge in each card's meta, first after the id; the steps after Expect |
| `docker/test-queue/html/index.html:520-522` | a click on a Who count opens Mine, Bot or CC |
| `CHANGELOG.md`, `VERSION` | 2026.10.15.2, one `### Staff` line (today's 2026.10.15 section was already committed with P114) |

## Tests

**`tools\tests\test_play_who.py`, 15 facts:**
- Who (`playwho`):
  1. every bucket maps to its Who; the counts table's `| BOT | 1 |` row is not taken for an item; EYES and DEPLOY say
     which kind of You;
  2. open and blocked items get who and steps; an item with a result is untouched; an unsorted open item says so;
     what/expect are never written over;
  3. counts per Who over open, later and blocked items; Mine is You + Bot, then you + You decide;
  4. no triage: unavailable, and no badges.
- Survives the importer:
  5. over a copy of the real notes, docs and testing, plus one new DONE prompt, two imports leave the triage and the
     steps byte for byte the same; an existing Who is still served afterwards; the new prompt's item shows Not sorted.
- Service (started on a free port with a scratch root):
  6. `/api/items` items carry who and steps; the document carries the counts; a passed item has no Who;
     `play-tests.json` never gets "who";
  7. an edited triage is served without a restart;
  8. Haven mode (`--data` elsewhere) reads the triage and the steps from the notes clone.
- Page (text):
  9. the badge markup in `card()` and the six badge classes;
  10. the steps `<details>` with its five labels;
  11. the three filters are extras, Open stays the default, P112's Bot tonight is still there, and Open still shows
      every open item;
  12. the header counts and their clicks;
  13. the source stays ASCII.
- **The real check** (the real files):
  14. every open and blocked item has a Who; the triage's Counts table equals what the service counts; the Who counts
      add up to the open total;
  15. every item has steps of the right shape: BOT and CC have a check; BOT-PARTIAL has a check and Chase's Do; You and
      You decide have where, do (at most 5 lines) and pass.

**Seen failing first:**
- Before `playwho.py` and the service and page changes: **14 of 15 failed**. The one that passed is "the source stays
  ASCII": the old page is ASCII too.
- Facts 5 and 14 failed then only because the module was missing, so each was also broken on purpose:
  - **Fact 14:** with P114-6's row removed from the triage, it failed: "Lists differ: [] != ['P114-6']". Restored, and
    `cmp` showed the file identical.
  - **Fact 5:** with `playtests.save` patched to also append to `bot-triage.md` (in a scratch runner, not in the repo),
    it failed on the hash. The real importer passes.
- With everything in place: **15 of 15**.

**Whole suites:**
- **shard-migration `tools\tests`: 98 of 98.**
  - On my first run, P112's `test_the_header_count_and_the_quiet_line` failed: it pins the literal `botCount();`, and I
    had written `botCount() + whoCounts();`.
  - I put P112's line back exactly and appended the Who counts on their own line (`index.html:249`), rather than change
    P112's test.
- **Bot suite (`tools\playtest-bot\tests`): 37 of 38.**
  - The one failure is `test_installer_dry_run_prints_the_call_and_registers_nothing`. It asserts the nightly task is
    not registered, and it is.
  - P112 recorded the same failure.

**Real check in a browser:**
- **Setup:** the new `server.py` on port 18095, with a copy of `notes`, `docs` and `testing` (not the live service,
  whose importer writes).
- **Default view:**
  - Open pressed;
  - 219 cards, 219 badges, 0 cards without one, 219 step blocks, all closed;
  - 97 robots (P112's, unchanged);
  - header `You 48`, `Bot, then you 17`, `You decide 14`, `Bot 80`, `CC 60` beside `Bot tonight: 0`.
- **Filters:**
  - Mine 79 (only You, You decide and Bot then you badges);
  - Bot 80 (only Bot);
  - CC 60 (only CC);
  - Open 219 again.
- Clicking `CC 60` opened the CC filter with 60 cards.
- A P56-7 card opened shows Where, Do (2 lines), Pass looks like, and Check.
- No console errors. At 375 px wide, no horizontal scroll.
- The scratch service was stopped and its copy deleted.

## Steps unknown

**None.** Every one of the 219 items has real steps or a real check line, worked out from its notes and the code.

## How the 219 were sorted

- **The work:** five sorting subagents, one per range of prompts, all on one written brief (bucket rules, step format,
  today's facts: live retired, HEAD boots, the shortcuts and characters, page URLs).
- **What they read:** each item's notes, the shard code and the bot's built checks.
- **My part:** I merged the five, validated them (219 of 219, each once, valid buckets, steps of the right shape),
  and read a sample against the notes.

**Bucket changes among the 163 sorted on 10-13 (35), and why:**
- **T-032** DEPLOY to CC: one startup log line on the bot's scratch shard proves the guard. No live and no client
  needed.
- **T-046** BOT to BOT-PARTIAL: the built check compares the two gumps only. Pressing each scope on a spare account is
  left to Chase, because it would wipe the bot's own characters.
- **P59-0** DECISION to CC: Chase answered P59's 8 decisions on 2026-10-05 (`notes/f35-evo-pets-handoff-2026-10-05.md`)
  and cc-P65 built from them.
- **P60-1 to P60-6, P63-1, P63-2, P63-3, P63-4, P63-6** DEPLOY to CC (11):
  - the console's own facts in `Shard-Console.Tests.ps1` prove them;
  - so do the saved window logs in `scripts\shard-console-output\` of real runs (14 commit runs ending pushed or
    clean; a build with GATE 4, 6 and 5 passed; a publish answered "no" then PUBLISHED).
  - P63-5 (Deploy built image) stays DEPLOY: it has never been run for real.
- **P73-2** DEPLOY to CC: the running test shard already logs `[AccountWipe] census:`.
- **P80-0** DECISION to CC: answered in `notes/decisions-2026-10-14.md`; decision 6 was built in cc-P103.
- **P83-1 to P83-7, P85-1, P85-2, P87-2, P87-3, P88-1, P88-2, P88-4, P90-1, P90-2, P90-4** DEPLOY to CC (17): the page,
  Homepage and the tests now show each.
  - **P83-6 is a good example:** P114's six items arrived at 11:51:05Z, from the service's own 60-second import, nine
    seconds after the commit.
  - **P87-2:** the Golem replaced cc-autopilot and handles quotes in titles (P111's committed).
- **P88-3 and P90-3** DEPLOY to EYES: nothing is left to deploy. The menu bar's look (phone too) and a real clipboard
  copy on a plain-http page are on screen.

**The 56 new items (P91 to P114):**
- CC 28, DEPLOY 9, EYES 7, DECISION 6, BOT 5 (P100's [VBuild steps), BOT-PARTIAL 1 (P100-2).
- One correction to a note. P101-1's note says public DNS gives 192.168.1.58. A DNS-over-HTTPS lookup today gives the
  house's public address, so the record is right. The steps send Chase to load the site on mobile data instead.

**Live retired:**
- T-014 and T-015 (the website panel's live heartbeat) stay **You** (DEPLOY), with steps that start "Cannot run while
  live is retired".
- T-011 and T-028 are re-pointed at the test shard where the same check works there (its own `status.json`;
  Stop/Start on the console's Test shard tab, then `docker logs sl-modernuo-test`).

**Things found while sorting (in the steps, flagged here):**
- **P64-1 and P64-2 FAILED last night, probably a setup cause, not a regression.** The newest CHANGELOG section at
  68631cb (2026.10.14.19) has only a `### Staff` list, and `ShardVersion.UnseenNotesFor` sends no bulletin when the
  current notes are empty (`server/customizations/ShardVersion.cs:309`).
  - Today's 2026.10.15 and 2026.10.15.2 are Staff-only too, so the next run will fail the same way.
  - The check lines say so.
- **Stale numbers in old items:** `[version` now shows 2026.10.14.19 on page 1 and runs to "Page 31 of 31"
  (P64-3, P64-4). P56-7's mule entry is "Breed" since P57.
- **P73-3 to P73-7 are the real test-account wipe.** Running them deletes Ringo, Eve, Garg and Elf Female, so the steps
  say Chase picks the moment.

## CC items, grouped for the overseer to queue (not run here)

**60 items in three groups.** I suggest two prompts: groups 1 and 2 together (about 1.5 h), then group 3 (about 1 h).
Each item's Check line on the page says exactly what to look at.

1. **Shard Console and package history** (Pester facts plus the saved window logs; about 45 min, most of it the
   console suite's run), 15 items:
   P60-1, P60-2, P60-3, P60-4, P60-5, P60-6, P63-1, P63-2, P63-3, P63-4, P63-6, P83-4, P83-7, P109-3, P110-3.
2. **Pages, services and the bot's night** (HTTP reads of the page and Homepage, `play-tests.json`, the tests, the
   2026-10-15 run's files; about 45 min), 22 items:
   P83-1, P83-2, P83-3, P83-5, P83-6, P85-1, P85-2, P88-1, P88-2, P88-4, P90-1, P90-2, P90-4, P91-0, P102-1, P102-2,
   P102-3, P102-4, P105-1, P108-3, P108-4, P112-1.
3. **Repo, notes and file claims** (git, grep, file reads; T-032 needs one scratch-shard start; about 1 h), 23 items:
   T-032, P59-0, P73-2, P80-0, P87-2, P87-3, P94-1, P94-2, P94-3, P95-1, P95-2, P95-3, P95-4, P99-0, P101-3, P103-1,
   P104-2, P105-2, P108-5, P111-5, P114-3, P114-4, P114-5.
   - **Two of these will fail until someone does the edit:**
     - **P95-1:** D89 is still in section 1 of `docs/bug-list.md`; the move is the overseer's.
     - **P104-2:** UORespawn's `SOURCE.txt` still says "0 .cs" and "TERMS: none stated".
   - **The CC prompt should report these, not mark them.**

## Deviations and decisions for Chase

1. **The steps are one click away, not open on the card.**
   - The prompt left it to me. Open, 219 cards with up to five step lines each would roughly double the page's length.
   - So each card shows a **How to test: <Where>** line, which already answers "where"; one click opens the rest.
   - The badge is always visible.
2. **What the filters show.**
   - **Mine:** open items whose Who is You, Bot then you, or You decide.
   - **Bot:** Who is Bot only, not Bot then you (those are in Mine, since they need you).
   - **CC:** Who is CC.
   - Like Open, they list open, later and blocked items. Bot tonight is unchanged.
3. **Many items are now CC because the work is already done.** About 40 of the 60 CC items are things that were
   built, deployed or answered since they were listed, and left evidence: logs, commits, a running page. A CC
   verification prompt can confirm each and tell you which to mark Pass. Until then they stay open on the page, as
   before.
4. **New items start as "Not sorted yet".** A prompt that says DONE adds items with no Who until its rows are added to
   `bot-triage.md` (and steps to `playtest-steps.json`). The header shows a "Not sorted yet" count only when there are
   any. A small follow-up would make each prompt's Finishing section add its own rows; I did not change the prompt
   template.
5. **P64-1 and P64-2 will keep failing in the bot** while the newest CHANGELOG section is Staff-only (above), this
   prompt's included. Whether a first-login bulletin should show when the newest notes have no player lines is your
   call. It is a behaviour question, not a test bug.
6. **P73-3 to P73-7 (the test-account wipe) delete your four test characters.** They are listed as You, with that
   warning in the steps.

## For Chase

1. **Restart the play-test page** so it serves the new code. It is still on the game PC; the Haven cutover has not
   happened:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\docker\test-queue\Start-TestQueue.ps1
   ```
   If you have cut over to Haven by then, use Shard Console > Websites > **Ops pages: deploy** instead.
2. **The badges in one line:** **You** (blue) is yours to do; **Bot, then you** (blue outline): the bot does the
   mechanics, you check the look; **You decide** (amber) is a choice; **Bot** (grey) the overnight bot settles it;
   **CC** Claude Code settles it from files, logs or tests. **How to test** under each card opens the steps.
3. To see only your work, press **Mine** (79 today).

## Repo size

- No pending file over 5 MB. The largest new one is `testing/playtest-steps.json`, 67 KB.
- Scratch (the sorting fragments, the scratch service's copy, now deleted) stayed in my session scratchpad, outside
  both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code:** `CHANGELOG.md`, `VERSION`, `docker/test-queue/server.py`, `docker/test-queue/html/index.html`.
- **docs:** `testing/bot-triage.md`, the new `testing/playtest-steps.json`, `tools/playwho.py`,
  `tools/tests/test_play_who.py`, this note, and the importer's `testing/SUMMARY.md` and `testing/play-tests.json`
  (machine output).

P115 DONE
