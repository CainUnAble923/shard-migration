# cc-P789: a readable tasks window, and no player-only tasks for staff accounts

## In plain words

- **The `[tasks` window is easier to read.** It now has a solid dark background with white text in the plain thin
  font, colored headings, and a blank line between sections. It is taller, so a whole card fits with no scroll bar.
  The title is just the task's name. No P numbers or test ids appear anywhere; the task number (G-0001) is in small
  gray text at the bottom. The `[report` box matches. Before and after pictures are in `notes\cc-P789-review\`.
- **Staff accounts no longer get player-only tasks.** Every Wakening Isle card is marked as needing a normal player
  account. The test shard now writes down which tester accounts are staff, and the Goblin reads that, so it cannot
  drift. Your `admin-chase` account will get no tasks until there are cards a staff account can do, and the Play
  testers page says why. If a staff account already holds a player-only card, the card says "This one needs a player
  account. Try it on your player character."
- **For you:** restart the web console, release the isle diff to the test shard, then run the one-time cleanup and the
  Goblin once. The exact commands are under For Chase below.

Iron Golem, 2026-11-03. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P789`. Nothing is committed, deployed or published. The shared Test Shard (2594), its files and
Haven were not touched: every shot was on a private proof shard (127.0.0.1:2596).

## 1. The readable window

`server/customizations/PlayTest/PlayTestTasks.cs` (`PlayTestStyle`, `PlayTestText`, `PlayTestTasksGump`,
`PlayTestReportGump`):

- **Background:** the dark stone frame with a solid black tile laid inside (gump 2624), and no alpha region, so nothing
  shows through. The HTML boxes have no background of their own, so there is no parchment.
- **Text:** near-white (`#F4F4F4`). Color is used only for the title and the four headings (yellow), the Goblin's
  line (pale blue, plain, not italic), the staff note (soft orange), and the three answer buttons (green, red, red).
- **Size:** 620 x 666 (it was 540 x 500). The text area is 572 x 420 (it was 236 tall). A blank line separates the
  sections. Every heading is on its own line.
- **Title:** the plain task title only. The task id is a small gray footer, "Task G-0001".
- **No ids:** `PlayTestText.Scrub` takes prompt numbers (`P762`, `cc-P773`, `P762-0`), play-test rows (`T-012`,
  `PT-4`) and task ids (`G-0001`) out of every line a tester sees, with any parenthesis that held one. Fact 8 feeds it
  a card stuffed with them and checks every piece of text the window shows.
- **Scroll bar:** only when a card is too long for the text area (`NeedsScroll`: about 90 characters a line and 26
  lines). I estimated all 16 isle cards: the longest (the new character card) is about 19 lines at that width, so
  none of them scrolls. The after shot shows the new character card, the one in Chase's screenshot, with no scroll
  bar.

### The font: what the server can and cannot do

- **TazUO never draws a server gump's HTML in its TTF fonts.** Its `HtmlControl` is a `RenderedText` on UO's own
  Unicode fonts (`unifont*.mul`). `GumpHelpers.cs` builds every `htmlgump` that way, and nothing in the gump packet
  selects a TTF font (TazUO 3212623f, our client's base, `D:\UO\tazuo-sl-build\src`). Only TazUO's own windows use
  TTF. Making server gumps use TTF would be a client change, which the prompt rules out.
- **The one server-side choice is `<BASEFONT SIZE=n>`** (`FontsLoader.cs:3092-3125`):
  - 0 or 4 picks font 1, the default: the bold pixel font Chase found hard to read;
  - 1 to 3 picks font 2: a plain, thin font;
  - 5 or more picks font 0: blackletter, worse. I found this the hard way: my first after shot used `SIZE=7`
    (`after-font0.jpg` in the review folder).
  - `cc-P789-tools/unifont-sample.png` renders the same line in all three, from the client's own files
    (`unifont-sample.py`).
- **So the body and the Goblin's line use font 2 (`SIZE=2`), and only the title and the headings use font 1
  (`SIZE=4`)**, where boldness helps. Plain labels (the button words, "What happened?") are drawn by the client in
  its label font; the server cannot change those.

### Shots (`notes\cc-P789-review\`)

All four are the same TazUO window (1280 x 800, the Golem's Player profile) on a private proof shard (127.0.0.1:2596,
a copy of the overnight bot world), made by `cc-P789-tools/tasks-shots.ps1`. The script writes one task, G-0001, from
the new character card (the card in Chase's screenshot, with its test id P762-0, as the Goblin hands it out), logs
Iron the Tester in, types `[tasks` into the client window, and captures it.
- `before.jpg`: `sl-modernuo:cc-p786`, P773's window, as Chase saw it:
  - pale text on parchment, in the bold pixel font, with the intro in italics;
  - "Make a brand new character (test P762-0, task G-0001)" as the title;
  - the scroll bar already needed at step 3;
  - the windows behind showing through.
- `after.jpg`: `sl-modernuo:cc-p789`, the same card:
  - a solid dark window and white text in the plain font;
  - yellow headings, each on its own line, with a blank line between sections;
  - no scroll bar, no P number and no test id;
  - "Task G-0001" small and gray at the bottom.
- `after-longest-card.jpg`: the longest card, Wren's farm and the pet. It also fits with no scroll bar, with about half
  the text area to spare.
- `after-font0.jpg`: my first after shot, with `SIZE=7`. That picks font 0, a blackletter font that is worse than the
  original. It is kept to show why the body uses font 2.
- Each shot has a `-log.txt` beside it.

## 2. Staff testers get staff-safe tasks only

- **The card field.** Each card in `scripts\playtest-task-bank.json` now has `"needsPlayer"`. It is `true` for all 16
  isle cards and the retired pet leash card. Each isle card starts from a new character waking on its own private
  copy of the isle, which a staff account does not get, so none of them is staff-safe. A card with no field counts
  as needing a player. The Goblin copies the field onto each task it hands out, and backfills it on tasks handed out
  before it existed.
- **Which testers are staff: read from the shard, not set by hand.** The shard writes `tester-accounts.json` next to
  `testers.json` (`PlayTestAccounts`). It lists each tester's account, whether it exists, its access level, and
  whether that is staff (Counselor or higher). Nothing else about the account is in it. It is written at start-up and
  every 5 minutes, whole and atomically, and only by the shard. A broken tester list leaves the last export alone.
  The Goblin and the Play testers page only read it.
  - **Not listed** (the shard has not written it yet): the account gets only staff-safe cards until it is listed.
    Better to wait a night than to hand a staff account a card it cannot do.
  - **Listed as "does not exist":** a player account. An account made at the login screen is a player account.
- **The Goblin** never gives a player-only card to a staff (or unlisted) tester, and still gives it to players. A
  staff tester with nothing staff-safe left gets none that night. The reason goes in the night's summary and in
  `goblin-state.json` (`why`, by account).
- **The Play testers page** shows a "staff (Owner)" badge and a line under each tester: "Staff account: gets only
  tasks that work on a staff account, never player-only ones". It also shows the Goblin's last word for that tester,
  for example "staff account (Owner): only tasks that work on a staff account, and none are left in the bank for them.
  Player-only tasks go to player accounts."
- **In game,** a staff account (Counselor or higher, on the account or the character) holding a card marked
  `needsPlayer` sees, at the top of the card in soft orange: "This one needs a player account. Try it on your player
  character." It can still be pulled back from the page as usual.
- **The one-time cleanup:** `playtest_goblin.py --pull-staff-player-only` (with `--dry-run` it only lists). It pulls
  back every open player-only task a staff tester holds, through the page's own Pull back (status `pulled`,
  `pulledAt`). Nothing is deleted, and answered tasks are left as they are. A second run finds nothing.
  - **I could not run it on the real files.** They are in the test world on Chase's desk
    (`D:\ShatteredLegacy\server\lib\uo\modernuo-test\playtest`), which a Golem may not read or write. The test
    `test_the_cleanup_pulls_back_staff_player_only_tasks_and_keeps_the_history` runs it on a copy of that situation
    (`admin-chase` holding G-0001 and others with no `needsPlayer` field yet). It is step 3 under For Chase below.
  - It needs the export, so the shard must be on the new image first: `admin-chase` is only known to be staff once the
    shard has listed it.

## Tests, each watched red, then green

- **Shard facts** (`server/tests/PlayTest/PlayTestTasksVerification.cs`, 3 new, 7 kept):
  - 8: no prompt, test or task ids in the window from a card stuffed with them, the footer "Task G-0001", no italics,
    and no scroll bar on a typical card (one when a card is far too long);
  - 9: the staff line on a player-only card held by a staff account, and not for a player or on a staff-safe card;
  - 10: the export, with exactly four fields per tester, reads back as written, including a missing account; a broken
    tester list keeps the last export.
  - Fact 1's body checks follow the new headings (no colons; each heading closes its own font tag).
  - **Red:**
    - against P773's code, the facts do not compile (`PlayTestText`, `PlayTestAccounts`, `IsStaff`, `StaffLine`,
      `NeedsPlayer`, `Shown`, `Footers` unknown: `red-probe.txt`);
    - one mutant per new fact (`mutants789.py`, `red-mutants.txt`): ids not scrubbed fails 8, no staff line fails 9,
      staff always false in the export fails 10. Each mutant failed only its own fact.
  - **Green:** 10 of 10 in the builder image (`probe789.sh`, `green-probe.txt`).
- **Goblin and page** (`scripts/tests/test_playtest_goblin.py`, 7 new, 8 kept; run from the repo root):
  - a staff tester never gets a player-only card, and a player still does;
  - a staff tester with only player-only cards left gets none, and the page's view says why (the Goblin's reason, the
    staff badge and the level);
  - an unlisted account gets only staff-safe cards, and an account listed as not made yet counts as a player;
  - the export round trip: the shard's shape (indented, with `writtenAt`) read by `PlayTestData.accounts()`;
  - the cleanup: pulls back only the open player-only tasks of the staff tester, keeps them with `pulledAt` (history),
    leaves answered, staff-safe and player tasks alone, and a second run does nothing;
  - old tasks get `needsPlayer` from the bank;
  - every isle card in the real bank says it needs a player account.
  - **Red:** the 7 new tests against P773's Goblin, page module and bank: 5 failed, 2 errors (`py-red.txt`).
  - **Green:** 15 of 15 (`py-green.txt`).
- **Whole Python suites:** `scripts/tests` 85 tests OK. `web-console/tests` 125 tests: 3 failures, all in
  `test_golem_glow.PhoneGlow.test_five_states_on_a_phone` (headless Chrome reads `animationName` "none" for the Golem
  glow). It imports nothing I changed, and the Golem glow page is not touched here, so I left it. **Unverified:**
  whether it also fails on main on this PC (I did not run main's copy).

## Builds

- **Main, `sl-modernuo:cc-p789`.** Run through the shard build script by `cc-P789-tools/gated-build.ps1`, under the
  `docker-build` lock, which I took and released. It ran three times, each `EXIT=0`, with 3,030 tests: 3,024 passed,
  6 skipped, 0 failed, all 188 patches applied, and the 10 play test facts among them.
  - Run 1 had the font 0 window (`green-gated-build-run1.txt`).
  - Run 2 had font 2 (`green-gated-build-run2.txt`).
  - Run 3 is the final code (`green-gated-build.txt`). It has the line limit measured from the after shot (22 lines,
    not 26), which changes nothing on any isle card.
- **Isle release, `sl-modernuo:cc-p789-isle`:** built from `D:\UO\golems\Iron\p789-isle`, which is the release tip
  `442a220` with the diff staged. `EXIT=0`, 2,871 tests: 2,866 passed, 5 skipped, 0 failed, all 176 patches applied,
  and all 10 play test facts (`green-gated-build-isle.txt`).
- **The release diff** is `cc-P789-tools/p789-release-isle-20261028.diff`. It applies cleanly to
  `release/isle-20261028` (`git apply --cached --check` against a fresh index of the release tip). Its two play test
  files are byte-for-byte main's. The release had P773's exact files, so there were no conflicts.
- **Memory:** 5.5 GB free before the first probe and 11.5 GB before the first gate. `latest` was not moved. The
  shared Test Shard was not touched.

## For Chase

Do these after the merge, in this order:

1. **Restart the web console** so the Play testers page shows the staff badges and the Goblin's reasons (once
   `D:\ShatteredLegacy` is on main):
   `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\web-console\Install-WebConsole.ps1`
2. **Release the isle diff to the test shard** (the isle release skill, as for P773 and P788):
   - apply `notes\cc-P789-tools\p789-release-isle-20261028.diff` to `release/isle-20261028`;
   - build it;
   - move the test shard to the new image.
   It is 4 files: the two play test files (identical to main's), CHANGELOG and VERSION (`2026.11.03.1`). It built
   green here as `sl-modernuo:cc-p789-isle`. A few minutes after the shard starts, `tester-accounts.json` appears in
   its `playtest` folder.
3. **The one-time cleanup, then the Goblin once.** First see what the cleanup would pull back:
   `python D:\ShatteredLegacy\scripts\playtest_goblin.py --pull-staff-player-only --dry-run`
   It should list `admin-chase`'s player-only tasks (G-0001 and any others still open). Then run it for real, and
   then run the Goblin:
   `python D:\ShatteredLegacy\scripts\playtest_goblin.py --pull-staff-player-only`
   `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\Run-PlayTestGoblin.ps1`
   On the Play testers page:
   - `admin-chase` shows "staff (Owner)" (or its level), its old tasks under Pulled back, and the Goblin's reason it
     got none;
   - your player account gets its new tasks as before.

**Checklist, in game on the test shard:**
1. On your player account, type `[tasks`. A dark window opens: white text, yellow headings, no scroll bar, and no
   "test P762-0" anywhere. "Task G-00xx" is small and gray at the bottom.
2. Type `[report`. The box matches: dark, white text.
3. Before the cleanup, if you like: on `admin-chase`, `[tasks` shows the orange line "This one needs a player account.
   Try it on your player character." on each isle card.

## Deviations and notes

- **The font is UO's plain Unicode font, not TTF.** TazUO cannot draw server gumps in TTF without a client change,
  which the prompt rules out. The details and the evidence are above.
- **Unlisted accounts get only staff-safe tasks.** A tester added minutes before the Goblin runs, while the shard is
  down, waits a night. The page says so.
- **Staff means Counselor or higher.** VIP is not staff, because it has no staff powers.
- **The cleanup is a command, not automatic.** The prompt asked for a one-time pull back through the normal path. The
  Goblin does not pull cards back by itself on later nights; the in-game line covers any held later.
- **The isle release version is `2026.11.03.1`** (the release is at `2026.11.03`). Main goes to `2026.11.03.10`
  (main is at `.9` after P787). The integrator may renumber.

## Files

**ShatteredLegacy.** For the Golem's commit, the shard parts are their own commit, as the prompt asks:
- **Shard commit:**
  - `server/customizations/PlayTest/PlayTestTasks.cs`;
  - `server/tests/PlayTest/PlayTestTasksVerification.cs`;
  - `CHANGELOG.md` and `VERSION`.
- **Second commit:**
  - `scripts/playtest_goblin.py`, `scripts/playtest-task-bank.json`, `scripts/tests/test_playtest_goblin.py`;
  - `web-console/playtesters.py`, `web-console/static/testers.js`.

**shard-migration:**
- this file;
- `notes\cc-P789-review\`: before and after shots, and their logs;
- `notes\cc-P789-tools\`:
  - the release diff;
  - the probe, mutant, gate and shot scripts, with their results;
  - the font sample and its script.

**Worktree to remove after the merge:** `D:\UO\golems\Iron\p789-isle` (detached at `442a220`, staged):
`git -C D:\UO\golems\Iron\ShatteredLegacy worktree remove --force D:\UO\golems\Iron\p789-isle`.

No tester list, task, report, save or secret is in either repo: the play test files are only in the private shard's
scratch copy, in this session's scratchpad.

P789 DONE
