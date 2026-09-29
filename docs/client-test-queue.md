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
| T-002 | ⬜ OPEN | **New character training** | Fresh character, take a New Haven training quest, gain skill | Skill gains and the quest completes | cc6 sheet 1.2. ClusterFSkillGain runs 5x and the 26 New Haven quests interact badly. **First thing a new family member hits** |
| T-003 | ⬜ OPEN | **Gargoyle equipment is obtainable** | On a gargoyle, craft gargish plate from a smith and gargish cloth from tailoring | The pieces can be made and worn | craft-registrations. Until the four gates landed, a gargoyle could obtain **no** gargoyle-specific equipment on a shard with SA on |
| T-004 | ⬜ OPEN | **The four new craft menus** | Blacksmithy, Tailoring, Tinkering, Carpentry: open each, find the newly registered entries | Entries appear at sane skill ranges, not 0 or 120 | craft-registrations, 90 files across 4 hooks |
| T-005 | ⬜ OPEN | **Craft entries with no resource** | Look for entries naming `WoodPulp` or `WorkableGlass` | **They should not be listed.** An entry whose resource is unported is one nobody can craft | craft-registrations flagged these; P2 flagged them first |
| T-006 | ⬜ OPEN | **Fresh world populates** | After `[GenerateSpawners` over the ten spawn files: gate to Ter Mur, the Abyss, the Underworld | Creatures visible in all three. Empty means the spawners did not take | Live-Deploy-Runbook 6b. Nothing spawns on a fresh world until these run |
| T-007 | ⬜ OPEN | **Shame and Despise** | `[GenerateNewShame` then `[SetupDespise`, then visit both | Populated. 41 types and 37 types respectively | Q-048: 282 of our reachable types exist **only** where these were run by hand |
| T-008 | ⬜ OPEN | **Eodon** | `[go 719 1863 40` | Decides whether Q-064's forty lines get written | Public moongate Eodon destination, `PublicMoongate.cs:275` |
| T-009 | ⬜ OPEN | **Gargoyle starts dressed** | Create a gargoyle, male and female, look at the paperdoll | A kilt, not leggings, and not underwear | D26. Verified once in a client; **re-verify on the fresh world** |
| T-010 | ⬜ OPEN | **D34 after a save round trip** | On the fresh world find a Royal City gargoyle alchemist, save, restart, look again | Still an alchemist, not a glassblower | type-identity. The probe passed **in this build**; CC called the ordering an accident, not a guarantee |
| T-011 | ⬜ OPEN | **Staff are not listed as playing** | Log in as admin, then load the website panel | Your character does **not** appear, and the count does not include you | cc-P6. `HighestListedAccessLevel = AccessLevel.Player`, a decision that can be flipped in one line |
| T-012 | ⬜ OPEN | **Petrified clone paperdoll** | Whatever a frozen clone's paperdoll renders as | Looks deliberate rather than broken | cc6 sheet, "still unchecked on the board" |
| T-013 | ⬜ OPEN | **Hybrid treasure chest** | Its crate graphic, lock and trap | Renders as a chest, locks, traps | cc6 sheet, same section |
| T-023 | ⬜ OPEN | **Stealing `LightInTheVoid`** | Find it on a dungeon spawn and try to steal it | It can actually be stolen | cc-P8 §6. The 58th stealable; it **passed its test only because the test host reads its tiledata weight as 0**, which is D27's trap. `Stealing.cs:256` refuses anything over weight 10, so if its real weight is higher, gate 5 delivered 54 and not 55 |

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
| T-020 | ✅ PASS | **Player package on a phone, on cell data** | Install from the download link on a phone off the home network | It installs and connects | **The last unproven claim on the project.** Everything else has been tested on the LAN |
| T-021 | ⬜ OPEN | **The updater updates** | Install an older package, run it, let it update | It fetches and applies without a reinstall | cc-P5 player-updater |
| T-022 | ✅ PASS | **Console: the dry-run tick box** | Launch the console normally (no `-DryRun`), tick the dry-run box, press Stop on live, type the phrase | Title and box turn DRY RUN; the window opens with the `DRY RUN` banner and live keeps running. Also: in the snapshot Delete yes/no, **No** is the default (Enter cancels) | D37 fix, notes/shard-console.md §6.1: "clicking it by hand is for the client pass"; §6 item 3 |

---

## Results

Newest first. One line each: ID, date, what happened. A `FAIL` names the bug-list row it produced.

- T-021, 2026-09-29: **partial, still OPEN.** `Play.ps1 -Update` on the outside computer, same version (2026.09.29.1331) both sides: offer, 76 MB download, unpack, wait-for-game and backup all worked; 0 files to add or replace, so **the replace path is unproven**. Settle it after the next package build and publish.
- T-020, 2026-09-29: **PASS.** From a computer **outside the home network** (not a phone), downloaded the package from the link and connected to **both test and live** in the client. The off-LAN claim is now proven; a phone on cell data specifically was not used.
- T-019, 2026-09-29: **PASS.** Copy on World setup pasted `[GenerateSpawners Data/Spawns/post-uoml/termur/Abyss.json` into Notepad, whole and exact.
- T-022, 2026-09-29: **PASS.** Delete yes/no has **No** as the highlighted default. With the tick box result below, all of T-022 is settled.
- T-022, 2026-09-29: **partial, still OPEN.** Console launched without `-DryRun`, box started unticked, Chase ticked it, Stop on live opened the `DRY RUN` window and ran nothing. Left: the Delete yes/no defaults to **No**.
- T-018, 2026-09-29: **PASS** after the D37 fix. Stop on live opened a window with the `DRY RUN` banner, printed the plan including the `stop live` confirm, and ran nothing. The phrase quoting through `Start-Process` was already proven by the 13:50 real stop. **Correction to the FAIL line below:** CC found a dry console never reached the phrase dialog in the old code, so that console was most likely **not** in `-DryRun`; the log did not record the mode (D37).
- T-017, 2026-09-29: **PASS on what it tests** (the selected row is what gets acted on). Delete named and deleted `20260929-142834_T-17` on test after the yes/no. Ran for real, not dry (D37), so re-confirm the printing after the D37 fix alongside T-018. Nothing lost: that snapshot's contents are the current test save, and the pre-restore snapshot is kept.
- T-018, 2026-09-29: **FAIL.** Pressed Stop on live in the console under `-DryRun`, typed the phrase, and **the live shard actually stopped.** The phrase quoting through `Start-Process` did work. Produced bug-list **D37**.
- T-017, 2026-09-29: **BLOCKED by D37 (Delete half).** Restore half good: it named the selected snapshot `20260929-142834_T-17` and restored it onto **test** (10/10 steps, pre-restore snapshot `20260929-143015_PRE-RESTORE_...` kept, old save moved to `Saves-test.aside-20260929-143015`). But it **ran for real** under `-DryRun` (D37). **Do not press Delete until D37 is fixed**, it would delete a real snapshot.
