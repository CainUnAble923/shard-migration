# cc-P273: status page refresh (judged rows, the port list, the numbers, the website feed)

## In plain words

- The status page (README and `dashboard.html`) has been re-checked row by row against main as of tonight. It says
  "Judgment reviewed 2026-10-25" now, and 6 of 16 port-list systems are in. None of the 11 "Playable?" gates changed
  yes or no (still 2 of 11), but what each one says is current.
- The test shard is on the build of 10-23 (version 2026.10.23.2). Main is 33 merges ahead (2026.10.25.7), so the
  playable tutorial lessons, the fishing second half and the 10-24 and 10-25 fixes are not on it yet. The page says
  so now.
- The website's Progress page still shows numbers from 09-29 (21 open defects, 230 of 570 files in reach). The fresh
  numbers are ready (52 open of 70 tracked, 894 of 1,186 files in reach, 75%). Putting them up means writing one file
  in the main checkout, which a Golem may not do, so the command is in "For Chase" below.
- For you: deploy main to the test shard; say which package is published; say which dungeon placement commands have
  been run on the test world; and run the one website-feed command, or tell the overseer to.

Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P273-status-page-refresh.md` (written 10-21, released to Iron 10-22). Run
2026-10-25 by the Iron Golem on `golem/Iron/P273`, both work copies clean at the start. Code copy at main `57924e6`,
version 2026.10.25.7. Not committed: the Golem commits after DONE.

The prompt names the prompts merged up to 10-21. By tonight main had moved on to P621. I judged against main as it is
now, not as it was on 10-21. The notes of every prompt the brief names were present (P188, P189, P192 to P198, P209,
P211, P212, P214, P225 to P231, P234, P235, P260, P267). The evidence below leans on their notes and on the code
repo's CHANGELOG, 2026.10.20.4 through 2026.10.25.7.

## 1. Every judged row: old, new, evidence

"Old" is `tools/progress-state.json` before this prompt (every row confirmed 2026-10-20; the backup is in the session
scratchpad). "New" is what `judge.py` wrote, dated 2026-10-25, through `judge.run()` called from a scratch script. The
full text is in the state file and on the page. Code paths are `server/customizations/` in the Iron code copy at
`57924e6`. Versions are CHANGELOG sections.

| Row | Old judgment | New judgment | Evidence |
|---|---|---|---|
| shard status | test shard only; main 2026.10.20.4; the deployed build and the package not visible | test shard only; it runs `sl-modernuo:latest` from `0f1871f` (2026.10.23.2), 33 merges behind main 2026.10.25.7; Play in the launcher goes to the test shard; the bot tests main nightly; the package still not visible | `docker image inspect sl-modernuo:latest`: label `sl.commit` `0f1871f`, `sl.dirty` 0, created 2026-10-23T13:43Z; `git show 0f1871f:VERSION`; `git log --merges 0f1871f..HEAD` (33); CHANGELOG 2026.10.24.2 |
| direction | port first, our systems after; Wrong, Covetous, Exodus, Blackthorn, Underworld, Eodon, fishing "claimed or queued" | same direction; the port-list sentence now reads 6 of 16 in, the rest most of the way. Re-confirmed, which clears the review-box line | The box's trigger, `notes/cc-P509-review-playtest-decisions-inbox.md` (10-23), is a code review of the decisions inbox, not a direction decision; README port list block |
| gate: shard runs and holds a world | **yes**; 1,430 tests at P208 | **yes**; the test shard is up and healthy on the 10-23 image; the merge Golem builds each branch and now retries a red build once; the bot boots main nightly | `docker ps` (`sl-modernuo-test` up 2 days, healthy); `http://192.168.1.58:8092/shards.json` (test up, 2026-10-26T00:11Z); `testing/bot-runs/2026-10-25-0130/report.md`; CHANGELOG 2026.10.24 |
| gate: player package installs on a clean PC | **yes**, needs confirm (which package is published) | **yes**, still needs confirm: more package changes since 10-20 have no recorded clean-PC pass (launcher art prep and logs, 29 MB of mounts, fog of war, appearance options, launcher fixes) | `testing/play-tests.json` T-049, T-020, T-021; CHANGELOG 2026.10.21.11, 2026.10.23.8, 2026.10.23.9, 2026.10.24.2, 2026.10.25.6 |
| gate: train without hitting a wall | **no**; rate 2 attempts and 1x, hook G | **no**; rate unchanged at `ClusterFSkillGain.cs:40-41`; new paths past 100: Arms Lore to 200, Appraisal on creatures, Remove Trap kits and traps, Old Haven quest speed-up; casting schools still excluded (`:24`); no result marked after 10-18 | `ClusterFSkillGain.cs:24, :40-41`; `notes/cc-P226-arms-lore-matters.md`; CHANGELOG 2026.10.20.8, .15, .16, .19, 2026.10.21.9, .17 |
| gate: a new character's first hour | **no**; stations placeholders, the Vault has no map | **no**; every lesson is playable, the farm is placed, graduation records the first loop, the Burrows are in the map; Test Center shards only (`ClusterFTutorial.cs:54-55`), fixes still landing 10-25, and the test shard's image predates the playable lessons | `Tutorial/ClusterFTutorial.cs:54-55, :107, :230, :330`; CHANGELOG 2026.10.20.16, 2026.10.21.18, .21, 2026.10.23.2, .5, .6, 2026.10.25.3, .5, .7; `notes/cc-P371-graduation-is-the-first-loop.md` |
| gate: levels and loops end to end | **no**; CompleteLoop a hook | **no**; graduation now records loop 1 (P371), but no level, skill reset or cap exists (`ResetLevelAndSkillsForF12` is empty) | `Tutorial/ClusterFLoops.cs:1-9, :34, :36-42`; `LootBoxes/ClusterFLootBoxes.cs:12, :18-19`; CHANGELOG 2026.10.21.10, .14 |
| gate: seen in a client | **no**; 418 items, 362 open; needs confirm (which build) | **no**; 1,246 items: 1,190 open, 43 pass, 4 fail, 8 later, 1 blocked; nothing marked since 10-18; the bot's 10-25 run passed 45 of 61 checks, but only Chase marks results. The build question is answered (10-23 image); the new needs-confirm asks Chase to deploy main and mark the bot's evidence | `testing/play-tests.json` (counted 2026-10-25 by status; latest `resultAt` 2026-10-18T19:35Z); `testing/bot-runs/2026-10-25-0130/report.md` |
| gate: somewhere to go | **no**; Wrong and Covetous claimed, four dungeons queued, 3 of 16 in | **no**; Wrong, Exodus and the Underworld are in, and Blackthorn (145 of 147 by hand), Covetous and Eodon most of the way: 6 of 16. The Burrows are in the map. But nothing is placed at boot, so each dungeon waits on its `[Gen` command, and none has a client pass. New needs-confirm: which `[Gen` commands have been run on the test world | `notes/port-list-2026-10-13.md` (recounted, below); the P188, P194 to P198 notes; CHANGELOG 2026.10.20.15, .16, .23, 2026.10.21.11, .24, 2026.10.24.4 |
| gate: things to fight | **no**; three batches, only Drelgor placed, 19 orphans unrecounted | **no**; many more spawners, nearly all placed by staff command (the 14 bestiary creatures, Eodon's 46 spawners and 345 creatures, Blackthorn's 44, Wrong's 38, the Void Pool, Exodus); the Halloween Sorcerer's Dungeon event runs by itself; P119's 29 are still on no spawner; **orphans recounted: 17** | CHANGELOG 2026.10.15.5, 2026.10.21.23, .24, 2026.10.22; `tools/spawn_orphans.py --dry-run` against the Iron copy (section 4) |
| gate: set mechanics fire | **no**; no caller outside the set files | **no**, unchanged; the one other grep hit, `Mobiles/Normal/DespiseCreature.cs:4`, is a comment | `grep -rln 'EpiphanyHelper\.\|BeastialSetHelper\.' server/customizations` at `57924e6` |
| gate: no live gap a player would call a bug | **no**; 65 rows, 41 mention fixed or built | **no**; 67 rows in section 1, highest D97, file last changed 10-21. Read the way the website feed reads it: 18 of 70 closed, 52 open, and 15 open-section rows read as fixed. D50, D89, D93 and D94 are still in section 1 | `docs/bug-list.md` (`awk` between "## 1." and "## 1b": 67 rows starting `\| **D`); `Build-MigrationStatus.ps1` run to the scratchpad and its misfiled warning |
| gate: fresh-world wipe ready | **no**; no single plan | **no**; same, plus a new item to gather: the list of placement commands a fresh world must run, since nothing new is placed at boot | CHANGELOG 2026.10.12, the `[Gen` and seeder lines of 2026.10.20.15 to 2026.10.25; `notes/decisions-2026-10-14.md` Tutorial 1 |
| task DEPLOY | todo; needs confirm (which build) | todo; the build is known (2026.10.23.2, 33 merges behind); the mark is cleared because the question is answered from Docker | as the shard status |
| task TUTORIAL | todo; stations placeholders | **in-progress**; lessons playable, farm, graduation as loop 1; left: a client pass, then live entry | as the first-hour gate |
| task WIPE | todo | todo; adds the placement-command list | as the wipe gate |
| task BUGS | todo; 65 rows | todo; 67 rows, 15 misfiled, the four owed moves | as the bug gate |
| task F-12 | todo; only the CompleteLoop hook | todo; graduation records loop 1; levels, resets and caps not built | `Tutorial/ClusterFLoops.cs:34, :36-42` |
| task F-37 | todo; nothing spends Renown | todo; commissions have not moved, but Renown is now spent (League Shop, Hall, Register goods), and the Register reaches bound guilds' contracts | CHANGELOG 2026.10.21.3, .14, .20 |
| section portlist | 2026-10-20 | confirmed 2026-10-25, with the recount below | section 2 |
| sections foundation, corrections | 2026-10-13, 2026-09-19 | **not re-confirmed**: the setup defects and the patch risk register were not re-read for this prompt | n/a |

Counts: 1 status, 1 direction, 11 gates, 6 tasks and 1 section judged, 20 rows in all. No gate's yes or no changed.
One task changed status (TUTORIAL, todo to in-progress). Needs-confirm marks: 3 now (the package, deploy and mark,
which `[Gen` commands have run), where there were 3 before (the package, the build, the DEPLOY build). DEPLOY's mark
cleared. The "Needs overseer review" box went from 5 lines to 4: the direction line cleared, and the
"play tests not sorted" line (756 items with no Who) is derived, and not this prompt's job.

## 2. The port list

`notes/port-list-2026-10-13.md` now has a "Done / files (10-25)" column for all 16 rows, and a dated paragraph under
the Port heading. That paragraph names, for each row the brief lists, every file the count still misses.
Method as the note says: `progress.py`'s `port_list()` over `tools/port-list.json`, reproduced row by row by a scratch
script that also lists the missing paths, with the shard at the Iron copy. Its numbers match the README's to the file.

| System | 10-13 | 10-25 | Left |
|---|---|---|---|
| Wrong (revamped) | 2 / 26 | 26 / 26 (in) | none |
| Covetous Void Spawn | 2 / 29 | 25 / 29 | HarvestMap, MagicFishFinder, SmeltersTalisman, WoodsmanTalisman (harvest and fishing hooks, cc-P194 section 6) |
| The Exodus Encounter | 1 / 38 | 38 / 38 (in) | none |
| Blackthorn Dungeon | 3 / 147 | 138 / 147, **145 by hand** | InvasionBeacon, InvasionController (attackable item, cc-P196 decision 1); the 7 `RobeBearingTheCrestOfBlackthorn .cs` (a space before `.cs` in ServUO's names) are ported: 7 files declare the class |
| Underworld + mini champions | 3 / 27 | 27 / 27 (in) | none by stem; merged as `e8f4b92` although P197's notes end PAUSED; P445 and P491 reviewed it, and their fixes shipped in 2026.10.25.5 |
| High Seas, fishing half | 4 / 59 | 53 / 59 | CorgulAltar, CorgulRegion (boats), MatchCord, Niter (cannons), Corgul's Handbook on Mysticism, FishQuestObjective |
| Eodon remainder (not in the brief's list, ported by P198) | 6 / 19 | 16 / 19 | not itemised |

One correction to P269's notes: they name `Fish.cs` as the sixth fishing file left. It is not a candidate, because
its stem is stock. The sixth is `Quests/ProfessionFishQuest/FishQuestObjective.cs`, a ServUO `BaseObjective`, and
pinned has no base for it. Ours carries the orders in `ProfessionalFisherQuest.cs` and `FishMonger.cs` instead, so
that row is 54 of 59 by hand.

## 3. The numbers

`SL_SHARD='D:\UO\golems\Iron\ShatteredLegacy' python tools/progress.py`, exit 0, on this game PC (the Golem, queue
and prompt paths exist here). It wrote `README.md`, `dashboard.html` (all 14 markers) and `tools/progress.json`.
Its counted line: 1,651 customization files, 168 patch files, 1,653 tests in 250 files. Header: "Judgment reviewed
2026-10-25. Shard version 2026.10.25.7. Golem on, 2 queued, latest done P621. Play tests: 1199 open, 4 failed,
43 passed." The 1,199 open is the page's own count: open plus later plus blocked, so 1,190 + 8 + 1.

## 4. Counted along the way

- **Spawn orphans.** `tools/spawn_orphans.py` hard-codes `D:\ShatteredLegacy`, so I ran its `main(['--dry-run'])`
  with its `SHARD` pointed at the Iron copy. It found **17**: the same 17 names as the file's own 2026-10-16 count.
  Eleven are Underworld NPCs (`post-uoml/termur/Underworld.json`); the rest are athialon, boatpainter, bodysculptor,
  dockmaster, escortablewanderinghealer and sphynx. The file was not rewritten: only its date line would change.
  The gate's old "19, unrecounted" was out of date.
- **Reachability**, for the website feed. `tools/content_index.py reach --ours <export>` ran on a `git archive HEAD
  server docker/uo/apply-patches.sh` export of the Iron copy, through a scratch wrapper. The wrapper adds a `\\?\`
  prefix, because a Blackthorn path is over Windows' 260 characters. Same scope as `notes/reachability-audit.md`
  1.1: content files under a subdirectory, with the costume files under `Items/Equipment/Suits` left out. That gives
  **1,186 files: 886 reached, 8 partly, 292 unreached**. Partly-reached files count as reachable, as the audit's 230
  did, so **894 of 1,186 (75.4%)**. On 09-29 it was 230 of 570 (40.4%).
  - **Unverified:** the audit set aside "32 staff costumes", and the path filter finds 34 files today, including
    `BaseCostume.cs`. I did not check whether that is two new costumes or a different cut.
- **Defects, as the site counts them.** `scripts/Build-MigrationStatus.ps1 -BugList <Iron docs copy> -OutFile
  <scratchpad> -PortedFiles 1186 -UnreachableFiles 292` wrote `{"defects": {"open": 52, "fixed": 18, "tracked": 70},
  "content": {"portedFiles": 1186, "reachableFiles": 894, "unreachableFiles": 292, "reachablePercent": 75.4}}`. It
  warned that 15 rows in open sections read as fixed.
  - The site's rule (FIXED or CLOSED in the row, or section 2 or 4) is stricter than the gate's old "mentions fixed
    or built", so its 18 closed is not comparable with the old 41.

## 5. The website (for the overseer)

What the site reads, served from this PC's `sl-uo-status` on 8092 (read with `curl`, nothing written):

- `migration.json` was generated **2026-09-29T18:16:30Z**: 21 open, 9 fixed, 30 tracked; 230 of 570 in reach. That
  is what the public Progress page shows.
- `shards.json` is fresh and lists the **test shard only**, up. So the top bar shows "Test up" and hides Live, as
  cc-P108 designed.
- `status.json` returns **503**. Only live wrote it, so the home page's live panel (players online, uptime, last
  save) has shown "offline" since 10-14.

**What the site should show instead of a live shard:**

1. **Replace the live panel with a "where we are" panel**: "The shard reopens as a fresh world; until then family
   and friends play on the test shard". Under it: the test shard's up or down from `shards.json`, which is already
   fresh and honest, and the build version and date. Never player names: the test shard's players are testers.
2. **The version and the latest patch notes**: the test shard's build version, which needs either the test shard
   writing `status.json` (`ShardStatusPublisher`, probably only a mount; I could not check the compose file, see
   Deviations) or a version field in `shards.json`, and a link to the wiki's patch notes page.
3. **The Progress page's numbers, refreshed**: the defects and reach above, and it could add the status page's two
   headlines, "Port list: 6 of 16 systems in, 833 of 983 files" and "Playable: 2 of 11 gates". Both are already
   in `tools/progress.json`, so they need not be hand-typed.
4. **Keep the stale-is-offline rule** (the passdown's section 3): a panel reading `shards.json` must treat an old
   `generatedAt` as "unknown", as the top bar already does.

**Making the refreshed migration.json live** is one command. It writes into the main checkout's
`server\lib\...\status` folder, which nginx serves, and a Golem may not write there:

```
powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\Build-MigrationStatus.ps1 -PortedFiles 1186 -UnreachableFiles 292
```

Its defaults read `D:\UO\shard-migration\docs\bug-list.md` and write the served file. The two numbers are tonight's
reach run (section 4). The script's own defaults (570 and 340) still date from 09-29. Teaching it to take them from
a `content_index.py reach --json` run, rather than by hand, is a small code prompt for later.

## For Chase

1. **Deploy main to the test shard.** It runs 2026.10.23.2, and main is 2026.10.25.7, 33 merges ahead. Shard
   Console: Test shard > Deploy built image. Then the gate "What is built is seen in a client" can move.
2. **Which player package is published**, and has one with our TazUO build passed a clean-PC install? (gate "The
   player package installs on a clean PC")
3. **Which dungeon commands have been run on the test world**: `[GenWrongRevamp`, `[SetupNewCovetous`,
   `[GenExodusEncounter`, `[GenBlackthorn`, `[GenEodon`. None runs by itself. (gate "Somewhere to go")
4. **Mark the overnight bot's evidence** on the play-test page. Nothing has been marked since 10-18, and the 10-25
   run passed 45 of 61 checks.
5. **The website's Progress page**: run the one command in section 5, or let the overseer run it, so it stops
   showing 09-29's numbers.

Each of 1 to 3 is a needs-confirm mark, so it sits in the page's "Needs overseer review" box with the `judge.py`
command that settles it.

## Deviations and decisions for Chase

- **Judged against tonight's main, not 10-21's.** The brief was written at 05:40 on 10-21; since then this repo's
  main has taken 302 merges (`git log --merges --since="2026-10-21 05:40" main`, counted 2026-10-25). Judging against the older main would have written stale rows on purpose.
- **One search was denied.** I wanted to grep `D:\UO\golems\Iron\ShatteredLegacy\docker` for `status` in
  `*compose*.yml`, to see whether the test shard mounts the status folder `ShardStatusPublisher` writes to (to say
  why `status.json` is 503 for the test shard). The guard hook asks for the test-shard lock on any command naming
  the compose files, and the Grep tool's permission prompt was auto-denied, since nobody was watching. So item 2 in
  section 5 says "probably only a mount", not verified.
- **I did not fetch get.shatteredlegacyuo.com** to see which package is published. It is served from Haven, and the
  standing rule is no connection to Haven unless the prompt says so. It stays a question for Chase.
- **`tools/spawn-orphans.txt` was not rewritten.** The recount matches it name for name; only the date would change.
- **The two unreviewed sections** (foundation, corrections) keep their dates, as P220 left them.
- **`testing/` machine output**: `progress.py` read it and did not change it. No play-test file is in this diff.

## Tests

- `SL_SHARD=<Iron copy> python -m unittest tools/tests/test_status_dashboard.py tools/tests/test_self_judging.py
  tools/tests/test_port_list.py`: **Ran 42 tests, OK**, after the refresh. `__pycache__` was cleared after each run.
- No code changed, so there is no new test and no red-first run. `judge.py` and `progress.py` ran unchanged.

## Changed files

- `tools/progress-state.json`: every row above, through `judge.run()`, plus one sentence of the direction body.
- `README.md`, `dashboard.html`, `tools/progress.json`: regenerated by `progress.py`.
- `notes/port-list-2026-10-13.md`: the 10-25 column and paragraph.
- `notes/cc-P273-status-page-refresh.md`: this file.

## Commit preflight

The Golem commits after DONE. Before that I checked `git status`. Five modified files and this note, all under
`README.md`, `dashboard.html`, `notes/` and `tools/`. Nothing in `docs/`. The code copy is untouched (it was only
read and archived to the scratchpad). The largest changed file is `tools/progress.json`, 88,629 bytes, far under 5 MB. The note is ASCII.

P273 DONE
