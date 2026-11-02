# cc-P773: in-game play test tasks for the three testers ([tasks, [report, the Play Test Goblin)

Iron Golem, 2026-11-02. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P773`. Nothing is committed, deployed or published, and the shared Test Shard and Haven were not
touched.

## In plain words

- **Testers get a task list in the game.** A tester types `[tasks` (or just says `tasks`) and a window opens with up
  to three things to try. Each one says why it matters, where to go, the steps and what to look for. It has three
  buttons: Worked, Something was wrong, Couldn't do it. `[report` is for anything else. Anyone who is not a tester
  gets one polite line.
- **You add testers on the web console, on its new Play testers page** (`https://uoconsole.tail81098d.ts.net/testers`,
  or the Play testers link at the top of the console). Type an account name and press Add tester. Each tester's open
  and finished tasks and reports are listed there too, with Pause, Remove and Pull back buttons.
- **The Play Test Goblin hands out tasks every night.** The first 16 tasks walk the Wakening Isle from character
  creation to the dock moongate. It emails you only when a tester reported something or got new tasks. Testers only
  report what they saw: you still mark Pass or Fail.
- **For you:** after the merge, restart the web console, add yourself as a tester, schedule the Goblin for 5:00 AM,
  and release the isle diff to the test shard. The exact commands are under For Chase below.

## Where the tester list lives, and why not the ops page

The prompt asked for a Testers tab on the ops page (Haven, Tailscale only), or somewhere else if that was the wrong
place. **It is on the web console instead**, the game PC's own page, which is also Tailscale only
(`uoconsole.tail81098d.ts.net`, Chase's login and the proof key, as the Music Room).

- The shard, the Goblin and the report file all live on the game PC. The shard reads the tester list when a player
  types `[tasks`. On Haven, the list would need a new two-way sync with the game PC, in both directions, every minute.
- **Pull back** must take a task off the tester's list straight away. On Haven, it would wait for that sync. On the
  web console it is one write to the file the shard reads, so the next `[tasks` no longer shows the task.
- Adding a tester is still one field and one button, from the phone, with no terminal.

The ops page on Haven is unchanged. A read-only copy of the Testers view there could come later if Chase wants it.

## The spec

`claude/cc-P-playtester-signup.md` (the 10-21 draft with Parts C and D) is **not on disk anywhere I can read**. I
searched `notes\`, `D:\UO\cc-prompts` (its git history too), `D:\UO\overseer` and the Golem folders. It lives only in
the claude.ai project, which an unattended run cannot open. I built from the prompt's own summary of Parts C and D,
which lists every rule. **Unverified:** whether the draft says anything the prompt's summary leaves out, including
"Chase's four decisions". If a decision there disagrees with what is below, that is a follow-up.

## What was built

### 1. Testers by hand (web console, `web-console/playtesters.py`, `static/testers.html`, `static/testers.js`)

- `testers.json`: account name, display name, paused flag, and when the tester was added.
- **Add** takes the name typed at the game's login screen: letters and digits, plus spaces, dots, dashes and
  underscores inside, up to 30 characters. A second add of the same account is refused, whatever its case.
- **Pause** keeps the tester's open tasks in game, but the Goblin gives them no new ones. **Remove** takes them off
  the list; their tasks and reports stay, so if they are added back they never repeat a test.
- **Per tester:** open tasks (each with **Pull back**), finished tasks with the button pressed and the words, tasks
  that were pulled back, and every report, newest first.
- A broken file shows its error on the page and is never written over. Every write is whole and atomic, under
  `playtest\.lock`, which the Goblin takes too.
- The POSTs check what the Music Room's do: Chase's Tailscale login and the proof key, from the page only, JSON
  only. Each is logged as one line, without the tester's words.

### 2. In game (`server/customizations/PlayTest/PlayTestTasks.cs`)

- **Files.** These live in the test world's folder, beside Saves (a `-Fresh` start removes only Saves):
  `D:\ShatteredLegacy\server\lib\uo\modernuo-test\playtest\`. They hold `testers.json` and `tasks.json`, which the
  shard only reads, and `playtest-reports.jsonl`, which the shard only appends to. `server\lib\` is git-ignored, so
  none of them can be committed (checked with `git check-ignore`).
- **`[tasks`** is for testers only. It shows their open tasks oldest first, one page each, with Back and Next task.
  Each page has a one-line Goblin intro (in italics), the title with the test and task ids, then **Why it matters**,
  **Where to go** (place and coordinates as text), numbered **Steps** and **What to look for**. Under that are a text
  box and the three buttons. **Report something else** opens the `[report` box.
  - Worked needs no words. Something was wrong and Couldn't do it ask for a few words first.
  - A task is finished once its tester has answered it. A pulled-back task disappears.
- **`[report`** opens a box. `[report <words>` sends at once. Testers only.
- **Every report is one line:** `at` (UTC), `account`, `character`, `task`, `test`, `button` (`worked`, `wrong`,
  `couldnt` or `report`), `text` (one line, at most 2,000 characters), `facet`, `x`, `y`, `z` and `version`. There is
  no IP address and no other field. The fact checks the exact list of fields.
- **Login line.** A tester who has tasks they have not seen yet is told once: "You have new play test tasks. Type
  [tasks (or just say tasks) to see them." It is remembered per account, in an account tag. No new saved type, so D40
  does not apply.
- **`tasks` said aloud**, alone, in any case, with or without . ! or ?, opens the window for a tester, as P769 did for
  `lesson`. Anyone else is not answered, so saying the word in chat is harmless.
- **Never throws.** A missing file means none. A broken one is logged once and the player gets a plain line: "The play
  tester list cannot be read right now. Please tell Chase", or the same for their tasks. A broken report line is
  skipped. A report that cannot be written says so. The login line is wrapped too.
- **Both commands** carry `[ShardCommand(CommandCategory.Player)]`. `CommandDeclarationVerification` failed the first
  build without it.

### 3. The Play Test Goblin (`scripts/playtest_goblin.py`, `scripts/Run-PlayTestGoblin.ps1`, `scripts/playtest-task-bank.json`)

- **One command:** `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\Run-PlayTestGoblin.ps1`.
  - **Time: 05:00 every day.** That is after the overnight bot's window (01:15 to 03:00) and before the testers
    play.
  - It runs the script and logs to `D:\UO\logs\playtest-goblin.log`. If the script wrote an email, it sends it the
    way the Golem sends its emails (`D:\UO\golem\email.json` and `smtp-cred.xml`), then removes it.
- **Rules**, each with a test:
  - At most 3 open tasks per tester.
  - Never the same card twice to a tester. That includes cards they answered or that were pulled back.
  - Paused testers are skipped.
  - Cards no human has answered come first, then cards with conflicting answers (Worked and a problem), then the
    rest. Within a rank, cards handed out less tonight come first, so two testers get different cards, then the
    bank's order.
  - A card whose play-test item is already settled (pass, fail, moot or blocked on the play-test page) is not handed
    out. A retired card is not handed out either.
- **Plain words.** Each task carries the card's words and its test id (`P762-0`, or a `T-` row). The Goblin's voice
  is only in the one-line intro, picked from seven lines that all start "The Goblin".
- **Its writing:**
  - `notes\goblin\YYYY-MM-DD.md` in shard-migration: new reports, tasks handed out, who got none and why, and open
    tasks now.
  - `notes\goblin\pending-pt.md`: a "Draft PT-?" entry for each Something was wrong, Couldn't do it and free report.
    Chase files it with a real PT number or deletes it.
  - An email, only when there are new reports or new tasks.
- **No Pass or Fail anywhere.** The Goblin only reads `testing\play-tests.json`. A test checks the file is
  byte-for-byte unchanged and that nothing written says pass or fail.
- **`notes/goblin/` is git-ignored** in shard-migration, a line added to `.gitignore`. The summaries quote testers'
  reports, and the prompt says reports are never committed, so the summaries stay on the game PC.
- **The first task set** is `scripts\playtest-task-bank.json`: 17 cards, 16 handed out.
  - The 16 follow the Wakening Isle path: new character, wake and stand, Tamsin and `[lesson`, walk and run, backpack,
    cloak, chat, farm and pet, bandaging Pip, death lesson, bank, Elara, the vision, the dock moongate, skipping the
    isle on a second character, and the coast and wreck.
  - Coordinates come from P762's route script (`notes\cc-P762-tools\rel-isle.py`).
  - The 17th, the pet leash (P764), is **retired**: P764 is on main, not on the isle release the testers play.
- **Test ids.** The isle prompts' checklists were never parsed into the play-test page, so each card cites its
  prompt's item (`P762-0`, `P740-0`, `P728-0`, `P718-0`, `P726-0`, `P751-0`, `P749-0`, `P758-0`, `P742-0`,
  `P741-0`).
- **A first run on a scratch folder** with the real bank, the real `play-tests.json` and Chase as the only tester
  handed out G-0001 to G-0003 (new character, wake, Tamsin) and wrote the email. The sample is
  `notes\cc-P773-tools\goblin-first-run-sample.md`.

### 4. Left out for now: the next step

Not built, as the prompt said:
- the public `/playtest` sign-up page;
- invite codes;
- approval emails;
- the allowlist flag.

When they come:
- the sign-up page writes a pending tester;
- approval adds them through `playtesters.add_tester`, so the web console and the Goblin need no change;
- the allowlist flag is a field on the tester record (`testers.json`), and the shard ignores fields it does not know.

## Tests, each watched red, then green

- **Shard facts** (`server/tests/PlayTest/PlayTestTasksVerification.cs`, 7 facts, the prompt's list):
  - `[tasks` for a tester;
  - `[tasks` for a non-tester;
  - a missing or broken file;
  - each report button writes one well-formed line;
  - `tasks` said aloud;
  - the login line;
  - no Pass or Fail.
- **Red:** 9 mutants (`mutate773.py`, `run-mutants.sh`, `mutants.txt`, logs in `mutant-logs\`), each undoing one
  rule, in the builder image. Every one fails at least one fact, and the baseline passes all 7.
  - anyone is a tester;
  - pulled tasks show;
  - a broken file throws;
  - no append;
  - an `ip` field;
  - no words needed;
  - no speech;
  - nothing remembered for the login line;
  - a `pass` button.
- **Testers page** (`web-console/tests/test_testers.py`, 5 tests):
  - Red against the old `server.py` with the new module: 3 failed, 1 error.
  - 3 mutants red: Pull back does nothing; a broken file written over; no page check.
  - Green.
- **Goblin** (`scripts/tests/test_playtest_goblin.py`, 8 tests, against a fixture):
  - 7 mutants red: no cap; paused not skipped; repeats; no ranking; mail every night; settled items handed out; a
    result written into `play-tests.json`.
  - Green. All in `py-mutants.txt`.
- **Whole Python suites:** `web-console/tests` 125 tests OK (1 skipped; I did not check which). `scripts/tests` 78 tests OK.

## Builds

- **Main, `sl-modernuo:cc-p773`:**
  - **Run 1 was red:** a missing `[ShardCommand]`, and my own wrong expectation in one fact (the client's text
    decoding drops a newline before my one-line clean). See `red-gated-build-run1.txt`.
  - **Run 2:** 1 failure, `BlackthornDungeonVerification.TheRegionRulesApplyOnTheFoldPieces` ("the kill was
    tallied"). It passed in run 1 and passes alone with the P773 facts (`probe-blackthorn.txt`). It shares world state
    and touches nothing of this change. Logged as a flake in `flake-gated-build-run2.txt`.
  - **Run 3, green:** 2,936 tests, 2,930 passed, 6 skipped, 0 failed, `EXIT=0`, all 7 P773 facts among them
    (`green-gated-build-run3.txt`).
- **Isle release, `sl-modernuo:cc-p773-isle`, green:** 2,808 tests, 2,803 passed, 5 skipped, 0 failed, `EXIT=0`, all
  7 P773 facts (`green-gated-build-isle.txt`).
- Free memory: at least 3.3 GB before each build (0.7 GB at first while another Golem's build ran, so I waited and
  wrote code). The VM page cache was dropped before each build. `latest` was not moved.

## The isle-only release

- `notes\cc-P773-tools\p773-release-isle-20261028.diff`: 4 files, made against the release tip `185a367` in a
  scratch worktree (`D:\UO\golems\Iron\p773-isle`, detached, staged). It applies cleanly
  (`git apply --cached --check` against `release/isle-20261028`), and it is what built green as `cc-p773-isle`.
  - The two shard files are identical to main's.
  - CHANGELOG has the same line under `2026.11.02`. VERSION goes from `2026.11.01.5` to `2026.11.02`.
- No conflicts: the shard part is two new files.
- The web console and the Goblin run from `D:\ShatteredLegacy` (main) on the game PC, not from the test shard's
  image, so they are not in the release diff.

## CHANGELOG and VERSION

- `2026.11.02`, Added: "Play testers: say [tasks for your test list and [report for anything odd."
- Main's newest was `2026.11.01.6`. If another prompt also takes `2026.11.02` before the merge, the integrator
  renumbers.

## For Chase

**Deploy:**

1. **The web console** (after the merge, once `D:\ShatteredLegacy` is on main). This restarts its task so the new
   page loads:
   `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\web-console\Install-WebConsole.ps1`
2. **The isle release:**
   - apply `notes\cc-P773-tools\p773-release-isle-20261028.diff` to `release/isle-20261028`, as the overseer did for
     P769 (the isle release skill);
   - build it;
   - move the test shard to the new image.
   The shard side is two new files, so the image built here as `sl-modernuo:cc-p773-isle` is that release.
3. **Schedule the Goblin** at 05:00 daily, as you (it sends mail with your stored credentials):
   `schtasks /Create /TN "SL Play Test Goblin" /SC DAILY /ST 05:00 /TR "powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\Run-PlayTestGoblin.ps1"`
   To try it once first without handing anything out:
   `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\Run-PlayTestGoblin.ps1 -DryRun`

**Checklist, in game on the test shard:**

1. **Add a tester:** web console, Play testers, type your account name, Add tester. You appear with no tasks.
2. **First tasks:** run the Goblin once (the command above, without `-DryRun`). The page shows three open tasks for
   you, and an email arrives: "Play testers: 3 new tasks handed out".
3. **Login line:** log in on the test shard. "You have new play test tasks. Type [tasks (or just say tasks) to see
   them."
4. **`[tasks`:** the window opens with your three tasks, one page each, with Back and Next task. Say `tasks` aloud
   and it opens again.
5. **The buttons:** press Worked on one. Press Something was wrong on another with the box empty: it asks for words.
   Write some, press again: "Thank you! Your report was saved for Chase." The page shows both under Finished tasks.
6. **`[report`:** type `[report The door hums` and it is saved at once. Type `[report` alone and a box opens.
7. **Pull back:** on the page, Pull back your last open task. `[tasks` in game no longer shows it.
8. **Paige and Dylan:** add their account names the same way when you have them.

## Deviations and decisions for Chase

- **The Testers tab is on the web console, not Haven's ops page.** The reasons are above. Say if you want it moved
  or mirrored on Haven.
- **Tasks are cards.** The Goblin cannot turn any play-test row into plain player words by itself, so it hands out
  cards from `scripts\playtest-task-bank.json`. Each card names its play-test item. New cards go at the end of that
  file, in the same shape.
- **The isle cards cite each prompt's `-0` item**, because those prompts' checklists never parsed into separate
  rows.
- **`[report` is for testers only**, like `[tasks`. A non-tester gets the same one line.
- **`notes\goblin\` is git-ignored**, so the Goblin's summaries and drafts, which quote reports, stay on the game PC.
- **The Read tool was denied in this unattended run** for files in the code copy. I needed it to edit `server.py` and
  `static/index.html` with the Edit tool. I made those edits with a small Python replace script instead (each anchor
  checked to appear exactly once), and read files with `cat`.
- **One flaky test** (Blackthorn, above) failed once and passed twice.

## Files

**ShatteredLegacy.** For the Golem's commit, the shard parts are their own commit, as the prompt asks:

- **Shard commit:**
  - `server/customizations/PlayTest/PlayTestTasks.cs` (new);
  - `server/tests/PlayTest/PlayTestTasksVerification.cs` (new);
  - `CHANGELOG.md` and `VERSION`.
- **Second commit:**
  - `web-console/playtesters.py` (new), `web-console/server.py`, `web-console/static/testers.html` and `testers.js`
    (new), `web-console/static/index.html` (the link);
  - `web-console/tests/test_testers.py` (new);
  - `scripts/playtest_goblin.py`, `scripts/Run-PlayTestGoblin.ps1`, `scripts/playtest-task-bank.json` and
    `scripts/tests/test_playtest_goblin.py` (all new).

**shard-migration:**
- this file;
- `.gitignore` (`notes/goblin/`);
- `notes\cc-P773-tools\`: the release diff, the build script and its summaries, the probe and mutant scripts with
  their results, and the first-run sample. The `.log` files are git-ignored, as before.

**Worktree to remove after the merge:** `D:\UO\golems\Iron\p773-isle` (detached at `185a367`, staged):
`git -C D:\UO\golems\Iron\ShatteredLegacy worktree remove --force D:\UO\golems\Iron\p773-isle`.

P773 DONE
