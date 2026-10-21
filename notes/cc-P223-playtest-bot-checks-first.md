# cc-P223: the play-test bot gets checks for the first half of the "Not built yet" items

The Gold Golem, on the Gold PC, branch `golem/Gold/P223` in both repos. Two sessions:
- **2026-10-20 night (Fable):** the first 26 checks (`uobot/checks_p223.py`, `checks_p223b.py`). Kept as a WIP commit when
  P177 was claimed.
- **2026-10-21 (Opus):** the other 31, fixes to the first 26, and the runs.

The code under test is main at **`62c675d`**. The branch's own server tree is older (`83b1f97`), so the shards were built
from main's commit, and the bot's files are the only change on this branch. Pinned is `D:\UO\ModernUO-pinned` at
`d4531cd94`. **Paused at Chase's request at 13:05**, during the final three-run pass. The continuation is
`cc-P359-cont-playtest-bot-checks-first.md`.

## Headlines

- **57 of my 60 items now have a bot check.** My 60 are the first 60 of the 127 items that said "Not built yet" on
  2026-10-20 (file order); the other 67 are P224's.
  - Each check is in `tools\playtest-bot\uobot\checks_p223*.py` (eight modules, a..h), and its `check` text in
    `testing\playtest-steps.json` says what the bot does.
  - Not built: T-031, P69-4 and P69-5 (section 6).
- **Each check has passed at least once against main**, except the eight whose last fix has not run yet (section 3: seven fixed but not rerun, and P71-2, which never ran on a clean pool).
- **One shard bug found: D96.** `[RemoveStealArties` throws once any stealable artifact has been stolen, and the
  server drops the staff member. It is in pinned ModernUO code, and a one-line patch fixes it. The draft fix prompt is
  in section 7.
- **Five existing nightly checks were failing because of the bot:** P64-4, P58-0, P61-5, P64-5 and P71-7.
  - The `[version` walk stopped at page 41, and the history is now 74 pages long.
  - Fixed; all five pass 3/3 in `testing\bot-runs\2026-10-21-1234`.
- **P62-7 is a stale play test:** P138 made the Kitsune Ears and Tail wearable by men on purpose. Its
  "men are refused" pass line needs Chase (section 5).
- **The bot itself got sturdier**, which every later night needs:
  - pattern gate and pack hygiene (`roomy`, `learn_all`);
  - deleting a pool character when a pool account is full;
  - reading the server's own hits updates (0xA1), status flags and effects;
  - sending weapon abilities and spells;
  - a restart helper for its own container.
- **The final three-run pass is not done.** It was started twice and stopped twice: once to fix the history and pool
  bugs, once at the pause. The second got through the 19 existing nightly checks (18 pass, P62-7 fails). P359 runs it.

## 1. The shard (part 1)

- I took the `test-shard` lock (and renewed it before the final run), and the `docker-build` lock for the build. Both
  are released.
- **This PC's test shard:**
  - It runs main `62c675d`: `Start-TestShard.ps1 -Commit 62c675d` built it through the gates (1,989 shard tests
    passing), and it came up healthy, tagged `sl-modernuo:good-62c675d` and `sl-modernuo:cc-P223`. **Left running.**
  - Deviation from the prompt: not `-Fresh`. The script refuses `-Fresh` with `-Commit`, and the first session had run
    `-Fresh` the night before, so the save was already a fresh one.
- **Where the bot ran:** the bot's own scratch shard, `sl-modernuo-bot` on 127.0.0.1:2595, from the same image (tagged
  `sl-modernuo:bot`).
  - Its world is a copy of the test world's newest automatic backup with the accounts wiped. Its server data comes from
    a worktree of `62c675d` (`Run-OvernightPlaytests.ps1 -Commit 62c675d -SkipBuild`).
  - The prompt's "this PC's own test shard (127.0.0.1, the test port)" was read as the bot's Rule 1, as the first
    session did: the bot refuses 2594 and 2593 (`uobot/safety.py`).
  - Every run recorded both real shards before and after. Rule 1 held in each: live absent, the test shard unchanged
    (`real-shards-*.json`).
- **The scratch shard is stopped** (`docker stop`, its own container only).

## 2. The checks (part 2)

One function per play-test id, the existing shape: setup as admin, the action as a player, an assertion on what the
server sent back, `(passed, evidence)`. Each check cites the code it reads its expectations from. The research behind
the 31 new ones was five read-only agents over `origin/main` and pinned, each fact with file and line, and the checks
were then corrected against the live scratch shard.

| Module | Items |
|---|---|
| `checks_p223.py`, `checks_p223b.py` (night one, fixed today) | T-001, T-003, T-004, T-005, T-013, T-024, T-025, T-027, T-041, T-042, T-044, T-045, T-048, P56-7, P57-5, P61-1, P61-4, P66-1, P66-2, P66-4, P67-1, P67-2, P67-3, P67-4, P71-4, P71-5 |
| `checks_p223c.py` | P56-5 (satchel Smelt Ore), P57-7 (stolen stack cap), T-026, T-023 (stealable artifacts), P66-3 (caught rate) |
| `checks_p223d.py` | P56-1, P56-2, P56-3, P57-1, P57-2, P57-4, P61-2, P67-5 (Society of Smiths, bulk orders, Seals) |
| `checks_p223e.py` | P65-0 (evo dog), P69-1 (the Compact's mule), P69-2 (Civic Mule Exchange), P69-3 (Breed) |
| `checks_p223f.py` | T-002 (Chiyo's quest), T-006 (Ter Mur spawners), T-007 (Shame, Despise), T-010, P62-8, P71-6 (across a restart), P66-6, P67-7, P71-2, P71-3 |
| `checks_p223g.py` | P67-6 (explosion trap), P57-3 (Platinum vein) |
| `checks_p223h.py` | P71-1 (Nerve Strike), P66-5 (Parry with Evasion) |

Fixes to the night-one checks:
- T-004, P61-1, P67-1, P67-2 and P67-4 learn every pattern first. Main's pattern gate (cc-P78) hides plate and the
  rest until the band is learned ("13 more patterns: Society of Smiths, rank Apprentice").
- The long-lived player's pack is emptied (`roomy`). Earlier checks left her overloaded (1,795 of 1,510 stones) and
  full (125 items), and tools and steals stopped working.
- T-044 retries its craft. At Tailoring 100 against 87.1 a single try can fail.
- T-024 and T-025 kill the boss with the admin's `[kill`. Five player fights in the dungeon all ended with the fighter
  dead (the other spawns, and the boss answers whatever its FightMode is).

New in the bot (`tools\playtest-bot\uobot\`):
- `client.py`:
  - the player's own hits from 0xA1 (a fight sends no 0x11, so her hits stood still);
  - every mobile's status flags (0x77/0x78), so a paralyse is seen;
  - graphical effects (0x70/0xC0), so a parry is seen;
  - her own body from 0x77, so a resurrection is seen.
  - All of it is in one hook at the top of `_handle`, away from the lines main changed.
- `packets.py`: `weapon_ability` (0xD7, 0x19) and `cast_spell` (0x12 0x56).
- `run.py`: a full pool account deletes its first character before creating. The pool's 3 accounts x 7 slots are fewer
  than a night's fresh characters.
- `checks.py`: the `[version` walk goes to 200 pages, not 40.

Two things learned the hard way, both now in the code's comments:
- Speech over 128 characters is dropped unanswered, so a long `[AddToPack ... set ...` silently did nothing.
- `[Global Delete` asks for confirmation (button 1).

## 3. The run (part 3): pass / fail

The final three-run pass did not finish (see Headlines). So the table gives, for each of my 57 checks, the **latest
single run** against main `62c675d` on the scratch shard. The first triage pass of the 26 night-one checks is a full
nightly-format run in `testing\bot-runs\2026-10-21-0845` (report.md, transcripts). The dev runs after it went to the
session's scratchpad, and their evidence is quoted here.

| Id | Last result | Evidence (shortened) | Note |
|---|---|---|---|
| T-001 | PASS | MAKE X on the tinker and smith item pages | 0845 |
| T-002 | PASS | Chiyo's quest accepted (1049019); Hiding 49.5 -> 51.1; rank message 1078171; reward | |
| T-003 | PASS | gargish plate and cloth arms made and worn (layer 19) | 0845 |
| T-004 | FAIL | 42 of our entries read on 678 items; 'leather talons' (Tailoring) and 'gargish butcher knife' (Tinkering) not listed | 0845; now learns every pattern first, **not rerun** |
| T-005 | PASS | 678 items and their materials: no WoodPulp, no WorkableGlass | 0845 |
| T-006 | PASS | 22, 65 and 44 spawners, 0 failures; creatures in range at the Abyss, the Underworld and Ter Mur | |
| T-007 | PASS | Shame 25 of 25 types in the world; Despise 47 spawners, 16 of 16 types | see section 5 on 41/37 |
| T-010 | PASS | both alchemists GargoyleAlchemist by serial before and after [save and a restart; Global Count 2 and 2 | D34's question, answered for today's build |
| T-013 | PASS | locked to the player; trap 55 -> 49 hits; loot inside | 0845 |
| T-023 | PASS | Light in the Void stolen into the pack | the run also hit D96 |
| T-024 | PASS | Miasma on its spawner, [kill, corpse | |
| T-025 | PASS | Lady Lissith on its spawner, [kill, corpse | |
| T-026 | PASS | the half eaten supper at 1134 1204 7, stolen at 120 first try | |
| T-027 | PASS | 5 level-5 chests: 4 masks, each with properties | 0845 |
| T-041 | PASS | 'The Society of Smiths hands you the tools of its trade: 6 items.'; ingots kept | 0845 |
| T-042 | PASS | starter item once; the second ask gives nothing | 0845 |
| T-044 | FAIL | 2 of each of the 4 gargish cloth entries after learning; the one craft failed its roll | 0845; retries now, **not rerun** |
| T-045 | PASS | the second character is offered Join | 0845 |
| T-048 | PASS | Liaison and Survey Archivist at the tents | 0845 |
| P56-1 | PASS | 'Society of Smiths: +50 standing, +52 Smithing Seals banked.'; Seals 0 -> 52 | |
| P56-2 | PASS | non-member at a Blacksmith: NPC 1157204, deed taken, the points gump 1157076 (buttons 1, 2) | |
| P56-3 | PASS | Ask each time: 'Bank: about 52 Smithing Seals'; closing keeps the deed | |
| P56-5 | PASS | 112.4: '1 pile: 0 smelted ... 1 left unsmelted.'; 112.5: smelted, ingots in the satchel | |
| P56-7 | PASS | trash bag, pet mimic, pack mule: entries and what they open | 0845 |
| P57-1 | PASS | Sturdy Shovel 150, Mining Gloves +5 1,800, Salvage Bag 750, Valorite Runic Hammer 45,000; iron deed +52 | |
| P57-2 | PASS | Celestial exceptional 20: +600 standing, +1,443 Seals (1,407-1,525) | |
| P57-3 | PASS | 112.4: 5 iron; 112.5: 10 iron and 2 Platinum; the shard logged "New Platinum vein logged: Mt Kendall, Trammel (2588, 421)" | the bank empties if run back to back |
| P57-4 | PASS | the choice gump's lines and buttons; no deed handed out | |
| P57-5 | PASS | Breed, Smelt Ore, Metal Familiarity entries; the panel opens | 0845 |
| P57-7 | PASS | 150 in the bag; the thief got 47 (at most 100) | |
| P61-1 | FAIL | 'no item platemail (tunic)' | 0845: the pattern gate; learns all now, **not rerun** |
| P61-2 | PASS | 8 orders, all Frost, 7 different items | |
| P61-4 | PASS | the post-Valorite line on Platinum, Frost and Celestial deeds | 0845 |
| P62-8 | PASS | the same serial on layer 18 before and after a restart; nothing on the beard layer | |
| P65-0 | PASS | 217 > 739 > 1547 > 277 > 1410 with each Echo line; reset kept it; stabled and claimed; killed and resurrected at stage 5 | |
| P66-1 | PASS | refused at 5 tiles, hides at 10, base past 100 | 0845 |
| P66-2 | PASS | nothing on an empty spot, finds the hider, [trapped] | 0845 |
| P66-3 | PASS | 50 of 50 stolen; the admin saw 16 caught (3 to 17 accepted, 9.7 expected) | the 16 is high; P359 pools 3 runs |
| P66-4 | PASS | 119.9 -> 120.9 | 0845 |
| P66-5 | FAIL | with Evasion 3 blocked, 4 hit; without 5/4; at 120 5/1: too few swings (7 < 8) | lengthened to 240 s, **not rerun** |
| P66-6 | PASS | ring worn, Tactics value 200, base 185 -> 200 in 75 s | the bot config's 5x gain amount |
| P67-1 | ERROR | the saw opened no craft gump | 0845: she was overloaded; fixed, **not rerun** |
| P67-2 | PASS | bows: 150 -> 155; kindling: no rise | 0845 |
| P67-3 | PASS | Platinum to Celestial listed; scissors gain and stop | 0845 |
| P67-4 | FAIL | 'no item platemail (tunic)' | 0845: the pattern gate, **not rerun** |
| P67-5 | PASS | teaching on: 6 of 6 Frost; off: 40 orders with stock and post-Valorite metals | |
| P67-6 | PASS | power 180 and 108, level 12 at both; 228-252 damage; Remove Trap 200 fails some | |
| P67-7 | PASS | LJ 100, 148, 100, 148: 1205, 1177, 1197, 1221; ratio 1.00 | rules out a large bonus only |
| P69-1 | PASS | the whole errand, the bonded 1-slot mule, 'You have your mule.', Replace after release | |
| P69-2 | FAIL | as a member the Liaison opens the hall page, not its menu | route fixed ('Guild services'), **not rerun** (pool full on the dev world) |
| P69-3 | PASS | 'Both mules are male' refused; one of each: 'The mules seem quite taken with each other ...' | |
| P71-1 | PASS | Bushido 200: 19 of 20 paralysed; 120: 17 of 20 | |
| P71-2 | ERROR | a pool account had no free slot | pool fixed, **never ran clean** |
| P71-3 | PASS | at 120 [95, 84, 98, 111, 98]; at 200 [104, 124, 106, 110, 104]; ratio 1.13 | single blasts over the formula's bounds: section 5 |
| P71-4 | PASS | 35 quiet steps at 200, 25 at 120 | 0845 |
| P71-5 | PASS | heals 67-68 | 0845 |
| P71-6 | PASS | 34 steps at the setting 34; 30 after setting 30 and a restart; put back | |

The existing nightly set, three runs each (`testing\bot-runs\2026-10-21-1234`, report.md): **18 pass, 1 fail**.
- P64-1 to P64-6, P58-0, P61-5, P71-7, P66-7, P62-1, T-039, CREATE, T-047, D41, P56-6, P56-4 and P61-3 pass 3/3.
- P62-7 fails 0/3 (section 5).
- The run was stopped after these; the soak was skipped.

## 4. Failures (part 4)

- **D96, new in `docs\bug-list.md`.** Found by T-026 then T-023.
  - **What:** `[RemoveStealArties` throws `NullReferenceException` once any artifact has been stolen, and the
    server drops the staff member.
  - **Repro:** `[GenStealArties`; a player at Stealing 120 steals the half eaten supper at Ter Mur 1134 1204 7;
    `[RemoveStealArties`.
  - **Bot output:** `admin DISCONNECTED: the server closed the connection`; shard log `System.NullReferenceException ...
    at Server.Engines.Stealables.StealableArtifacts.RemoveStealableArtifacts()`.
  - **Cause:** pinned `StealableArtifacts.cs:40-46`; `si.Item` is null for a stolen entry.
  - **Effect:** the loop also stops at that entry, so the un-stolen artifacts after it stay and the next
    `[GenStealArties` doubles them. Staff only.
- **The remaining fails are the checks' own** (setup, timing, the pattern gate). They were fixed in the checks, as
  section 2 says, and no row was filed. The eight not yet rerun are in P359.

## 5. Chase's to play, by place

Only the halves the bot cannot see. Every item below also has a bot check for its mechanics.

**New Haven: the Society of Smiths' hall (3469 2536 41), and any town smith**
- P57-4: Bulk Order Info's Small/Large gump is solid, and the Completed orders line ends inside the frame.
- P56-2: hand a filled deed to a town Blacksmith as a non-member: does the gold show as account gold or as a pile in
  the bank box? (`Banker.Deposit` goes to account gold first on this expansion.)
- T-001: a craft gump's item page: the MAKE X label draws.
- P61-4: a Platinum to Celestial small deed in a client started **without** the launcher shows a blank line.
- P57-5, P56-7: the context entries (Breed, Smelt Ore, Metal Familiarity, Clean Up Britannia ...) read as words in our
  client.

**New Haven's mine camp, and the Compact's tents (3494 2744)**
- T-048: the two tents look right on the ground.
- P69-2: `[add PackMule 3`, `4`, `5` side by side: each tier's hue looks right on the mule.

**Anywhere, as staff**
- P65-0: an evo dog through its bodies (`[EvoPet give dog`, then xp): each body's swing, flinch, fall and idle; the door
  stays shut; the 10 decisions on the page (P65-D1 to D10).
- P66-5: Parry 200, Bushido 120, Evasion, a two-hander, against a strong monster: some hits get through (the bot counts
  them, but how the fight feels is yours).
- T-013: the three treasure crate graphics draw as proper crates.
- P67-7: the axe's bonus past Lumberjacking 100. The bot rules out a big bonus; the few percent between ours and
  pinned's is inside its noise. A careful damage log over many hits would settle it, or leave it.

**After 24 hours (no way to shorten it)**
- P69-3, P69-4, P69-5: breed two mules (Breed on the male, target the female); a day later the foal deed is in the bank;
  read its tooltip (sex, tier 1, generation, family line, qualities, bloodline); trade it to another character, who
  uses it and gets a mule with those genes. `DeliverAt` is read-only and gestation is a fixed 24 hours, so neither the
  bot nor a restart can bring it sooner.

**Play tests that need your word, not your eyes**
- **P62-7 is out of date.** It says a man is refused the Kitsune Ears and Tail ("Only females can wear this."). P138 made
  men able to wear it on purpose (`notes/cc-P138-kitsune-paperdoll-refit.md` item 6: "Men can wear it; gargoyles
  cannot."), and the bot sees exactly that, 3/3. Close P62-7, or restate it as "a gargoyle is refused".
- **T-031 cannot be tested as written.** Its multiplier (`testCenter.skillGainMultiplier`) does nothing since cc-P190;
  the Test Crystal replaced it. Restate it against the Test Crystal (Off against 5x, from skill 30), and a later night
  can check it.
- **T-007's 41 and 37** are the reachability audit's counts of content *types* each command reaches (creatures, items,
  altars, walls, chests), not creature types. The bot checks every creature type the two spawn tables name: 25 for
  Shame (24 plus the walls' CaveTroll) and 16 for Despise, all present.
- **P71-3's single blasts** went past the formula's bounds (111 at 120, 124 at 200, where the formula gives at most 100
  and 110), but the ratio is right (1.13; pinned would be about 2.3). Something adds a little that the formula as read
  leaves out; the bot reports it and asserts only the ratio.

## 6. Not built, and why

| Id | Why |
|---|---|
| T-031 | its multiplier is retired (cc-P190); the item needs restating against the Test Crystal (section 5) |
| P69-4 | needs a delivered foal deed: 24 hours after breeding, and `DeliverAt` is read-only |
| P69-5 | the same |

A staff command that delivers a pending foal deed now (a GM `[DeliverFoal`, test shard only) would make P69-3 to P69-5
fully bot-checkable. That is an idea for the overseer, not a fix.

## 7. Draft fix prompts

```
# CC task P<next>: [RemoveStealArties no longer throws after a theft (bug list D96)

**Model:** Sonnet

**Touches:** server

**Summary:** One null check in pinned StealableArtifacts.RemoveStealableArtifacts, as a patch, with a fact.

Bug list D96 (found by the play-test bot, cc-P223): pinned UOContent/Engines/Stealables/StealableArtifacts.cs:40-46
reads si.Item.Deleted for every entry, and an entry whose artifact was stolen has no item, so [RemoveStealArties
throws NullReferenceException, the staff member is disconnected, and every entry after it is left in the world (the
next [GenStealArties doubles them).

1. A patch in server/patches/ (the house shape, applied by apply-patches.sh): `if (item?.Deleted == false && ...)`.
2. A fact in server/tests: generate, mark one entry stolen (its Item null, as the steal does), remove; assert no throw
   and every un-stolen artifact deleted.
3. build.sh green; then on the test shard: [GenStealArties, steal the supper at Ter Mur 1134 1204 7, [RemoveStealArties:
   no disconnect, "Stealable artifacts spawner removed.".
4. Patch notes: a Staff line. Report upstream (bug list section 5).
```

## 8. Files changed

Code repo (`D:\ShatteredLegacy`, `tools\playtest-bot\`):
- `uobot/checks_p223c.py` to `checks_p223h.py`: new.
- `uobot/checks_p223.py`, `uobot/checks_p223b.py`: the fixes in section 2; the imports of c to h.
- `uobot/client.py`, `uobot/packets.py`, `uobot/run.py`, `uobot/checks.py`: section 2.
- The unit tests pass: `python -m unittest discover -s tests`, 42 of 42.
- No server code changed.

Docs repo (`D:\UO\shard-migration`):
- `testing\playtest-steps.json`:
  - 31 `check` texts from "Not built yet" to what the bot does;
  - 7 night-one texts updated (T-004, T-024, T-044, P61-1, P67-1, P67-2, P67-4, each for the pattern gate, the retry
    or the admin kill).
  - `where`, `do` and `pass` untouched.
- `testing\bot-triage.md`: the cc-P223 checks listed under "Checks built"; P67-7 is now BOT-PARTIAL.
- `docs\bug-list.md`: D96; the next free number is now D97.
- `testing\bot-runs\2026-10-21-0845` (the triage pass, 26 checks x 1) and `2026-10-21-1234` (the nightly set x 3,
  stopped at the pause; its report written and its after-state recorded by hand).
- This note.

`tools/tests/test_play_who.py` fails 2 tests before and after these edits, on other prompts' open items (M-001,
P163-0 ... have no Who or Where). Nothing of P223's.

## Continuation

- **Done:**
  - parts 1 and 2 (shard, all 57 checks written, check texts);
  - the single-run results above;
  - the five history checks fixed and passing 3/3;
  - D96 filed with its draft fix prompt;
  - the Chase list;
  - locks released.
- **Left:**
  - the full three-run pass of every check on a fresh scratch world;
  - the seven checks whose last fix has not run (T-004, T-044, P61-1, P67-1, P67-4, P66-5, P69-2, plus P71-2 on a
    clean pool);
  - bug rows for whatever that run finds;
  - T-004's two missing entries and P66-3's caught rate settled.
  - That is `D:\UO\cc-prompts\queue\cc-P359-cont-playtest-bot-checks-first.md`.
- **Mid-flight:** nothing.
  - The scratch shard is stopped; the next run makes a fresh world.
  - The test shard runs main `62c675d`.
  - No lock held.
  - The bot's code imports and its unit tests pass.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\ShatteredLegacy -DocsRepo D:\UO\shard-migration -Branch golem/Gold/P223 -NoRefresh`.
It commits nothing; neither repo is BLOCKED:

```
Repo Result
---- ------
code dry run
docs dry run
```

- code: 12 files under `tools/playtest-bot/uobot/` (6 changed, 6 new).
- docs: this note, `docs/bug-list.md`, `testing/bot-triage.md`, `testing/playtest-steps.json`, and the two run folders
  `testing/bot-runs/2026-10-21-0845` and `2026-10-21-1234` (105 files in all).
- Outside both repos: `D:\UO\cc-prompts\queue\cc-P359-cont-playtest-bot-checks-first.md` (the continuation).

P223 PAUSED
