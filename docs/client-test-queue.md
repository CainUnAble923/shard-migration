# Client test queue

**The standing list of things only a person at a screen can settle.** Add to it as findings appear,
tick items off as they are run. It never "completes"; it drains and refills.

**Chase runs every one of these. No agent does, and no agent may.** There is no client in the
sandbox, and most of these need a server built from current source, which is a deploy decision and
his alone.

---

## How several chats share this file without wrecking it

This file is written by more than one chat. These rules exist because the alternative has already
bitten us: on 2026-09-29 an agent proposed a bug-list row numbered **D36 when D36 was taken**, and
nobody caught it until the row was read twice.

1. **IDs are `T-NNN`, assigned as highest-in-file plus one.** Read the file before you add. Never
   reuse an ID, never renumber, never reorder. A retired item keeps its number forever.
2. **Rows never move.** To settle an item you change its `Status` cell and add a line under
   **Results**. You do not cut the row out and paste it elsewhere. Moving rows means rewriting the
   whole file, which is exactly when one chat silently drops another chat's new item.
3. **Status is one of:** `⬜ OPEN`, `✅ PASS`, `❌ FAIL`, `⛔ BLOCKED`, `➖ MOOT`, always icon plus word, in the
   second column so a glance down it shows what is done. Anything not ⬜ is settled for now.
4. **Write the row so Chase never has to ask which chat added it.** `How` must be runnable as
   written and `Pass` must say what good looks like, in the client, not in the code.
5. **Every row cites where it came from.** A test with no origin cannot be retired when its reason
   disappears.
6. A `FAIL` gets a bug-list entry. The queue records that something broke; `bug-list.md` records
   what and why.

**Related files, so this does not become a fourth competing sheet:**
`client-check-backlog.md` is a finished run from 2026-09-19 kept for its method.
`client-test-sheet-cc6.md` is the CC6 batch sheet, its board section passed 2026-09-26.
`client-test-sheet.md` is older than both. **New items go here, not in those.**

---

## A. In the UO client

| ID | Status | Check | How | Pass | Source |
|---|---|---|---|---|---|
| T-001 | ⬜ OPEN | **MAKE X label** | Open any craft menu, look at the MAKE X entry | Text is visible | cc6 sheet 1.1. Fixed 2026-09-19, **never verified after a rebuild** |
| T-002 | ⬜ OPEN | **New character training** | Fresh character, take a New Haven training quest, gain skill | Skill gains and the quest completes | cc6 sheet 1.2. ClusterFSkillGain runs 5x and the 26 New Haven quests interact badly. **First thing a new family member hits**. **Caveat from cc-P9:** the test shard now runs `testCenter.skillGainMultiplier` at 5.0 **on top of** ClusterFSkillGain, and live will not. A pass here does not predict live; turn the multiplier off, or read this as a smoke test only |
| T-003 | ⛔ BLOCKED | **Gargoyle equipment is obtainable** | On a gargoyle, craft gargish plate from a smith and gargish cloth from tailoring | The pieces can be made and worn | craft-registrations. Until the four gates landed, a gargoyle could obtain **no** gargoyle-specific equipment on a shard with SA on |
| T-004 | ⬜ OPEN | **The four new craft menus** | Blacksmithy, Tailoring, Tinkering, Carpentry: open each, find the newly registered entries | Entries appear at sane skill ranges, not 0 or 120 | craft-registrations, 90 files across 4 hooks |
| T-005 | ⬜ OPEN | **Craft entries with no resource** | Look for entries naming `WoodPulp` or `WorkableGlass` | **They should not be listed.** An entry whose resource is unported is one nobody can craft | craft-registrations flagged these; P2 flagged them first |
| T-006 | ⬜ OPEN | **Fresh world populates** | After `[GenerateSpawners` over the ten spawn files: gate to Ter Mur, the Abyss, the Underworld | Creatures visible in all three. Empty means the spawners did not take | Live-Deploy-Runbook 6b. Nothing spawns on a fresh world until these run |
| T-007 | ⬜ OPEN | **Shame and Despise** | `[GenerateNewShame` then `[SetupDespise`, then visit both | Populated. 41 types and 37 types respectively | Q-048: 282 of our reachable types exist **only** where these were run by hand |
| T-008 | ⬜ OPEN | **Eodon** | `[go 719 1863 40` | Decides whether Q-064's forty lines get written | Public moongate Eodon destination, `PublicMoongate.cs:275` |
| T-009 | ✅ PASS | **Gargoyle starts dressed** | Create a gargoyle, male and female, look at the paperdoll | A kilt, not leggings, and not underwear | D26. Verified once in a client; **re-verify on the fresh world** |
| T-010 | ⬜ OPEN | **D34 after a save round trip** | On the fresh world find a Royal City gargoyle alchemist, save, restart, look again | Still an alchemist, not a glassblower | type-identity. The probe passed **in this build**; CC called the ordering an accident, not a guarantee |
| T-011 | ⬜ OPEN | **Staff are not listed as playing** | Log in as admin, then load the website panel | Your character does **not** appear, and the count does not include you | cc-P6. `HighestListedAccessLevel = AccessLevel.Player`, a decision that can be flipped in one line |
| T-012 | ⬜ OPEN | **Petrified clone paperdoll** | Whatever a frozen clone's paperdoll renders as | Looks deliberate rather than broken | cc6 sheet, "still unchecked on the board" |
| T-013 | ⬜ OPEN | **Hybrid treasure chest** | Its crate graphic, lock and trap | Renders as a chest, locks, traps | cc6 sheet, same section |
| T-023 | ⬜ OPEN | **Stealing `LightInTheVoid`** | Find it on a dungeon spawn and try to steal it | It can actually be stolen | cc-P8 §6. The 58th stealable; it **passed its test only because the test host reads its tiledata weight as 0**, which is D27's trap. `Stealing.cs:256` refuses anything over weight 10, so if its real weight is higher, gate 5 delivered 54 and not 55 |
| T-024 | ⬜ OPEN | **Miasma is actually spawned** | Labyrinth (Malas): confirm a spawner holds Miasma, kill it | It is there and killable. The 2.5% set-piece drop is not the point | cc-P7 §4. **This is the one assumption P7 could not verify from source**: the drop is patched in, but an unreachable carrier means an unreachable item |
| T-025 | ⬜ OPEN | **Lady Lissith is actually spawned** | Twisted Weald (Ilshenar), `TwistedWeald.json:15`: same shape as T-024 | She is there and killable | cc-P7 §4, same reasoning |
| T-026 | ⬜ OPEN | **Stealables spawn and can be stolen** | As GM on test: `[GenStealArties`, wait for the next 15-minute check, then TerMur 1134 1204 7 (`HalfEatenSupperArtifact`) | The artifact is there and stealing succeeds | cc-P8 §3. 58 entries added; see also T-023, where one entry's weight is unproven |
| T-027 | ⬜ OPEN | **Masks in random loot** | `[add TreasureMapChest 5` a few times, open as GM | Orc and tribal masks turn up among the magic items, roughly one per chest, with random properties | cc-P8 §4. This is the **only** change that moved treasure-chest odds: 1/118 to 1/120 per existing type |
| T-028 | ⬜ OPEN | **A live stop saves (D36)** | Only after the next live deploy. Console status: the live plan for Stop says "The shard saves on stop"; if it still says "A stop does not save", the image is older and this cannot pass yet. Then in game: `[add` something at a spot you will remember, or rename a pet, and do **not** `[save`. Stop live from the console, Start it, log back in | The change is still there. `docker logs sl-modernuo` shows `[SaveOnShutdown] ...saved in N ms` then `Shutting down` | cc-P10 Part B; `notes/cc-P10-updater-polish-and-d36.md` §B. Needs the compose stop timeout settled first (§B.5) |
| T-029 | ✅ PASS | **`[TCFill` restocks a bank** | On test as a character made before the Test Center was on: `[TCFill` | Pinned's Test Center fill plus our Test Kit land in the bank. A second run inside ten minutes is refused | cc-P9. `FillBankbox` only runs at character creation, so this is the only route for existing characters. The command should **not exist at all** on live |
| T-030 | ✅ PASS | **Test Kit at character creation** | Make a brand new character on test, open the bank | Our own resources are there beside pinned's fill | cc-P9 `TestCenterKitEntries.cs`. Entries register on live too but must never be placed there |
| T-031 | ⬜ OPEN | **The skill multiplier compounds safely** | On test, raise a skill from 0 and watch the rate | Gain is visibly faster, and ClusterFSkillGain's extra gains still happen on top | cc-P9 `TestCenterSkillGain.cs` scales `GainFactor`, read once at `SkillCheck.cs:119`. **ClusterFSkillGain's bonus gains call `SkillCheck.Gain` directly and never read GainFactor**, so the two stack rather than multiply. Worth confirming in play |
| T-032 | ⬜ OPEN | **The live guard actually shouts** | Set `testCenter.enable` true in a config on port 2593, start, read the log. Put it back | A loud startup error names the mistake | cc-P9 §4. **It logs and does not refuse to start.** After D40, a protection that only writes a log line is worth proving out loud at least once |
| T-033 | ✅ PASS | **Self-deletion is allowed on test only** | On test, delete your own character from the character screen | It works on test; on live the same attempt is refused | cc-P9 `AccountHandler-test-center-deletion.patch` makes `RestrictDeletion` a property so it is read at deletion time rather than frozen by Configure ordering |

| T-034 | ✅ PASS | **The console's new command tab** | Open the console, World setup tab | Every seeder is listed with its dry-run syntax, what it does, and whether re-running duplicates. Nothing shows as "unclassified" | cc-P21. **Do this first: it tells you what to run below and in what order** |
| T-035 | ✅ PASS | **Seeders run clean on an existing world** | Dry run each, read it, then run for real: NewHavenServices, GuildHalls, MineCamp, MoveMineCampNpcs | Each dry run matches what actually happens; running any of them twice adds nothing | cc-P15/P16/P17. **The test world is not fresh, so none of today's content exists until these run** |
| T-036 | ✅ PASS | **The 18 sunk New Haven NPCs** | `[ClusterFSeedNewHaven repair` | The Anatomy giver and the other 17 stand on the floor, clickable **without ctrl+shift** | cc-P17 PT-05. World load deliberately does not move them; this command does |
| T-037 | ✅ PASS | **New Haven has a smithy again** | Go to the smithing area, smelt ore and make something | Forge and anvil present and accepted by the craft | cc-P17 PT-01. Pinned ships no New Haven decoration at all; these 125 entries are ServUO's |
| T-038 | ✅ PASS | **A ghost can get up in New Haven** | Die, then find a healer or ankh without leaving town | Resurrection works | cc-P17 PT-07. There were **zero** healers and no ankh before this |
| T-039 | ⬜ OPEN | **A new character is pointed at the board** | Make a fresh character, read the first login message | It tells them where the board is, and the board is findable from where they stand | cc-P15 F-9. This is the whole first-minute experience |
| T-040 | ❌ FAIL | **Guild Directory and joining** | Board first page, pick a guild, use "Show me the way", join | Directory lists the guilds, the arrow points, joining is one click with no skill or gold | cc-P15 F-9 |
| T-041 | ⬜ OPEN | **Joining hands over the tools** | After joining, check the pack | The character-creation items for that guild's skills are there. **Joining the Smiths must not take your ingots** | cc-P15. The ingot bug was found and fixed by P15 |
| T-042 | ⬜ OPEN | **Starter item on request, once** | Take the guild's starter item, then try again | Given once; the matching quest shows as done; asking twice gives nothing | cc-P15 F-9, deviation D-92 |
| T-043 | ✅ PASS | **Board and NPC are interchangeable** | Take a quest at the board, turn it in at the matching NPC. Then the reverse | Both work, and the reward pays once whichever end you use | cc-P17 PT-03. Turning in at the NPC used to be refused |
| T-044 | ⬜ OPEN | **Gargish cloth armor is tailorable** | As a gargoyle, open Tailoring | The 8 cloth armor pieces are there and craftable. The **garments** (robe, sash, half apron) are still absent and that is expected | cc-P17 PT-08. Pinned had the types and never registered them |
| T-045 | ⬜ OPEN | **Second character is not already in a guild** | On an account that has joined a guild, make a second character | Not a member; joining gives that character its own items | cc-P18 F-7, fixes PT-06 |
| T-046 | ⬜ OPEN | **Reset stone and `[ResetMyAccount`** | Use both; try each scope (this character / all / account) | Same gump from both routes; each scope clears what it says, including joined guilds | cc-P18 F-7. The old reset did **not** clear joined guilds |
| T-047 | ⬜ OPEN | **Young by time played** | Check Young status and the countdown; try "I want to grow up!" | Countdown in days and hours against 336 hours of account game time; the confirm gump appears | cc-P18 F-5. No skill rule any more; murder rule kept |
| T-048 | ⬜ OPEN | **Mine camp tents** | Go to the New Haven mine camp | Two tents west of the existing one; Liaison and Survey Archivist at the tent openings | cc-P16 |
## B. Not the client, but still nobody's job but yours

Kept here because they are the same kind of work: a person looking at a screen, settling something
no build gate can see.

| ID | Status | Check | How | Pass | Source |
|---|---|---|---|---|---|
| T-014 | ⬜ OPEN | **Panel shows a live shard** | Start the shard with the publisher in it, load the site | "Online", a count, and character names | cc-P6 plus the website work |
| T-015 | ⬜ OPEN | **The heartbeat, which is the whole liveness design** | Stop the shard. Wait three minutes. Watch the page | It returns to **Offline on its own** | cc-P6. CC could not test the timer: the fixture never calls `Configure`/`Initialize`. **This is its first real run** |
| T-016 | ⬜ OPEN | **Atomic write across the bind mount** | Leave the shard running an hour, then check `docker logs sl-modernuo` | No `Shard status: could not write`, and `generatedAt` keeps advancing | cc-P6. Proven on the builder's Linux filesystem, **not** across Docker Desktop onto NTFS, which is where it matters |
| T-017 | ✅ PASS | **Console: snapshot Restore and Delete** | Take or fake a snapshot, select the row, press each in `-DryRun` | The printed command names **the snapshot you selected** | notes/shard-console.md §6. CC's own "most likely to be wrong" |
| T-018 | ✅ PASS | **Console: a live action's spawned window** | Press Stop on the live shard in `-DryRun`, type the phrase | Window opens and says `DRY RUN`; `-ConfirmLive "stop live"` survived `Start-Process` | notes/shard-console.md §6, never run for real by design |
| T-019 | ✅ PASS | **Console: Copy buttons** | World setup tab, press one, paste into Notepad | The whole command arrives. Clipboard needs STA | notes/shard-console.md §6 |
| T-020 | ✅ PASS | **Player package off the home network** | Install from the download link on a computer outside the home network | It installs and connects | Proven 2026-09-29. **The phone-on-cell-data part was dropped by Chase 2026-10-01: a phone cannot play the game, so there is nothing to prove** |
| T-021 | ⬜ OPEN | **The updater updates** | Install an older package, run it, let it update | It fetches and applies without a reinstall | cc-P5 player-updater. **Precondition: a published package whose files actually differ from the installed one.** Run this on the next package build and publish, not before |
| T-022 | ✅ PASS | **Console: the dry-run tick box** | Launch the console normally (no `-DryRun`), tick the dry-run box, press Stop on live, type the phrase | Title and box turn DRY RUN; the window opens with the `DRY RUN` banner and live keeps running. Also: in the snapshot Delete yes/no, **No** is the default (Enter cancels) | D37 fix, notes/shard-console.md §6.1: "clicking it by hand is for the client pass"; §6 item 3 |
| T-049 | ⬜ OPEN | **Clean PC first run in Windows Sandbox** | Build the package (do not publish), run `player-package\clean-test\Start-CleanTest.ps1 -Mode Build`, then follow the numbered steps in `player-package\clean-test\READ ME FIRST.txt` (it opens on the sandbox desktop). Windows Sandbox must be on first (Turn Windows features on or off, Windows Sandbox, restart). Bring back `baseline.txt` and `evidence.txt` from `D:\UO\clean-test-results\<run>\results\` | `baseline.txt` says CLEAN; `evidence.txt` shows `uo-path.txt` found and `client.exe` at 7.0.114.40 or newer, `TazUO.exe` running with `zlib.dll` and `VCRUNTIME140.dll` both loaded from the package's `app\tazuo\` and no load-failure event; a character walked in the world with paperdoll and backpack open | cc-P35 (notes/cc-P35-clean-machine-test.md). Does **not** settle T-021's precondition: that needs a new build to be **published**, and this run publishes nothing |

---

## Results

Newest first. One line each: ID, date, what happened. A `FAIL` names the bug-list row it produced.

- T-040, 2026-10-01: **FAIL, and it splits in two.** Joining a guild works. (a) **The Guild Directory
  lists the Artificers twice**, one row per guildmaster rather than per guild: **D41**. (b) **Nothing
  points a player to the League of Extraordinary Citizens** (the Registrar's organization, not the
  Rangers' League guild). F-9 only specified the Registrar showing the guild list, not the reverse, so
  (b) is a **design gap, not a cc-P15 defect**; recorded under F-9 for the features chat. Still to check:
  whether the Registrar does show the guild list, which would be a defect if it does not.
- T-043, 2026-10-01: **PASS.** Quest taken at the board, turned in to Jacob. The PT-03 refusal is gone.
- T-038, 2026-10-01: **PASS.** Healers present in New Haven.
- T-037, 2026-10-01: **PASS.** Forges present; New Haven can smith again.
- T-036, 2026-10-01: **PASS.** `[ClusterFSeedNewHaven repair` put the sunk NPCs on the floor.
- T-035, 2026-10-01: **PASS.** Every seeder ran.
- T-034, 2026-10-01: **PASS, with a defect.** All commands ran from the tab. **The command text and the
  dry-run button disagree**; sent back to CC to fix. The tab is usable; the mismatch is the kind that teaches
  someone to distrust the dry run, so it matters more than it looks.
- T-029, 2026-09-30: **PASS.** A second `[TCFill` inside ten minutes was refused and said how many minutes until the next restock; after ten minutes it restocked again. The command should still not exist on the next live.
- T-003, 2026-09-30: **BLOCKED by PT-08** (playtest tracker: gargish clothing not in the Tailoring menu, reported by Chase). Cloth half cannot pass until PT-08 is settled; gargish plate from a smith not yet reported.
- T-029, 2026-09-30: **partial, still OPEN.** `[TCFill` on an existing test character filled the bank. Left: a second run inside ten minutes is refused.
- T-009, 2026-09-30: **PASS.** New gargoyle characters on test start with a kilt, and it is wearable. D26 re-verified on the current image.
- T-033, 2026-09-30: **PASS on test.** Chase deleted new characters from the character screen. The live half (the same attempt is refused) could not be run, the old live being retired; check it on the next live alongside T-028.
- T-021, 2026-10-01: **still open, and it is waiting on a package, not on code.** The replace path cannot be exercised while both sides are the same version (0 files to add or replace, 2026-09-29). It becomes testable the first time a package is built and published with changed files. P22's F-15 part adds VERSION and CHANGELOG.md, so the build after that one is the natural moment: install the current package, publish the new one, then run the updater and confirm files are actually replaced and the version string moves.
- T-020, 2026-10-01: **closed.** Chase dropped the phone-on-cell-data requirement: a phone cannot run the client, so a phone install proves nothing. The off-LAN claim stands on the 2026-09-29 computer test and this row is done. T-021 (the updater replace path) is a separate row and stays open.
- T-020, 2026-09-30: **correction, still PASS.** D40 shows the old live shard served nothing after 14:16 on 2026-09-29, so the 15:05 "live" connection only reached Docker's port forwarder. The off-network proof stands on the **test** connection. Chase, 2026-09-30: the old live world is retired; test becomes the base for the next live, and live-only rows (T-011, T-014 to T-016, T-028) apply to that shard.
- T-030, 2026-09-30: pass. New character made on test; the Test Kit resources were in the bank. Confirms `testCenter.enable` is live in the running process and `TestCenterKitEntries` register and place at creation. The creation path only; `[TCFill` (T-029) is still unproven.
- T-021, 2026-09-29: **partial, still OPEN.** `Play.ps1 -Update` on the outside computer, same version (2026.09.29.1331) both sides: offer, 76 MB download, unpack, wait-for-game and backup all worked; 0 files to add or replace, so **the replace path is unproven**. Settle it after the next package build and publish.
- T-020, 2026-09-29: **PASS.** From a computer **outside the home network** (not a phone), downloaded the package from the link and connected to **both test and live** in the client. The off-LAN claim is now proven; a phone on cell data specifically was not used.
- T-019, 2026-09-29: **PASS.** Copy on World setup pasted `[GenerateSpawners Data/Spawns/post-uoml/termur/Abyss.json` into Notepad, whole and exact.
- T-022, 2026-09-29: **PASS.** Delete yes/no has **No** as the highlighted default. With the tick box result below, all of T-022 is settled.
- T-022, 2026-09-29: **partial, still OPEN.** Console launched without `-DryRun`, box started unticked, Chase ticked it, Stop on live opened the `DRY RUN` window and ran nothing. Left: the Delete yes/no defaults to **No**.
- T-018, 2026-09-29: **PASS** after the D37 fix. Stop on live opened a window with the `DRY RUN` banner, printed the plan including the `stop live` confirm, and ran nothing. The phrase quoting through `Start-Process` was already proven by the 13:50 real stop. **Correction to the FAIL line below:** CC found a dry console never reached the phrase dialog in the old code, so that console was most likely **not** in `-DryRun`; the log did not record the mode (D37).
- T-017, 2026-09-29: **PASS on what it tests** (the selected row is what gets acted on). Delete named and deleted `20260929-142834_T-17` on test after the yes/no. Ran for real, not dry (D37), so re-confirm the printing after the D37 fix alongside T-018. Nothing lost: that snapshot's contents are the current test save, and the pre-restore snapshot is kept.
- T-018, 2026-09-29: **FAIL.** Pressed Stop on live in the console under `-DryRun`, typed the phrase, and **the live shard actually stopped.** The phrase quoting through `Start-Process` did work. Produced bug-list **D37**.
- T-017, 2026-09-29: **BLOCKED by D37 (Delete half).** Restore half good: it named the selected snapshot `20260929-142834_T-17` and restored it onto **test** (10/10 steps, pre-restore snapshot `20260929-143015_PRE-RESTORE_...` kept, old save moved to `Saves-test.aside-20260929-143015`). But it **ran for real** under `-DryRun` (D37). **Do not press Delete until D37 is fixed**, it would delete a real snapshot.
