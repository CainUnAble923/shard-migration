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
3. **Status is one of:** `OPEN`, `PASS`, `FAIL`, `BLOCKED`, `MOOT`.
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

| ID | Check | How | Pass | Status | Source |
|---|---|---|---|---|---|
| T-001 | **MAKE X label** | Open any craft menu, look at the MAKE X entry | Text is visible | OPEN | cc6 sheet 1.1. Fixed 2026-09-19, **never verified after a rebuild** |
| T-002 | **New character training** | Fresh character, take a New Haven training quest, gain skill | Skill gains and the quest completes | OPEN | cc6 sheet 1.2. ClusterFSkillGain runs 5x and the 26 New Haven quests interact badly. **First thing a new family member hits** |
| T-003 | **Gargoyle equipment is obtainable** | On a gargoyle, craft gargish plate from a smith and gargish cloth from tailoring | The pieces can be made and worn | OPEN | craft-registrations. Until the four gates landed, a gargoyle could obtain **no** gargoyle-specific equipment on a shard with SA on |
| T-004 | **The four new craft menus** | Blacksmithy, Tailoring, Tinkering, Carpentry: open each, find the newly registered entries | Entries appear at sane skill ranges, not 0 or 120 | OPEN | craft-registrations, 90 files across 4 hooks |
| T-005 | **Craft entries with no resource** | Look for entries naming `WoodPulp` or `WorkableGlass` | **They should not be listed.** An entry whose resource is unported is one nobody can craft | OPEN | craft-registrations flagged these; P2 flagged them first |
| T-006 | **Fresh world populates** | After `[GenerateSpawners` over the ten spawn files: gate to Ter Mur, the Abyss, the Underworld | Creatures visible in all three. Empty means the spawners did not take | OPEN | Live-Deploy-Runbook 6b. Nothing spawns on a fresh world until these run |
| T-007 | **Shame and Despise** | `[GenerateNewShame` then `[SetupDespise`, then visit both | Populated. 41 types and 37 types respectively | OPEN | Q-048: 282 of our reachable types exist **only** where these were run by hand |
| T-008 | **Eodon** | `[go 719 1863 40` | Decides whether Q-064's forty lines get written | OPEN | Public moongate Eodon destination, `PublicMoongate.cs:275` |
| T-009 | **Gargoyle starts dressed** | Create a gargoyle, male and female, look at the paperdoll | A kilt, not leggings, and not underwear | OPEN | D26. Verified once in a client; **re-verify on the fresh world** |
| T-010 | **D34 after a save round trip** | On the fresh world find a Royal City gargoyle alchemist, save, restart, look again | Still an alchemist, not a glassblower | OPEN | type-identity. The probe passed **in this build**; CC called the ordering an accident, not a guarantee |
| T-011 | **Staff are not listed as playing** | Log in as admin, then load the website panel | Your character does **not** appear, and the count does not include you | OPEN | cc-P6. `HighestListedAccessLevel = AccessLevel.Player`, a decision that can be flipped in one line |
| T-012 | **Petrified clone paperdoll** | Whatever a frozen clone's paperdoll renders as | Looks deliberate rather than broken | OPEN | cc6 sheet, "still unchecked on the board" |
| T-013 | **Hybrid treasure chest** | Its crate graphic, lock and trap | Renders as a chest, locks, traps | OPEN | cc6 sheet, same section |

## B. Not the client, but still nobody's job but yours

Kept here because they are the same kind of work: a person looking at a screen, settling something
no build gate can see.

| ID | Check | How | Pass | Status | Source |
|---|---|---|---|---|---|
| T-014 | **Panel shows a live shard** | Start the shard with the publisher in it, load the site | "Online", a count, and character names | OPEN | cc-P6 plus the website work |
| T-015 | **The heartbeat, which is the whole liveness design** | Stop the shard. Wait three minutes. Watch the page | It returns to **Offline on its own** | OPEN | cc-P6. CC could not test the timer: the fixture never calls `Configure`/`Initialize`. **This is its first real run** |
| T-016 | **Atomic write across the bind mount** | Leave the shard running an hour, then check `docker logs sl-modernuo` | No `Shard status: could not write`, and `generatedAt` keeps advancing | OPEN | cc-P6. Proven on the builder's Linux filesystem, **not** across Docker Desktop onto NTFS, which is where it matters |
| T-017 | **Console: snapshot Restore and Delete** | Take or fake a snapshot, select the row, press each in `-DryRun` | The printed command names **the snapshot you selected** | PASS | notes/shard-console.md §6. CC's own "most likely to be wrong" |
| T-018 | **Console: a live action's spawned window** | Press Stop on the live shard in `-DryRun`, type the phrase | Window opens and says `DRY RUN`; `-ConfirmLive "stop live"` survived `Start-Process` | FAIL | notes/shard-console.md §6, never run for real by design |
| T-019 | **Console: Copy buttons** | World setup tab, press one, paste into Notepad | The whole command arrives. Clipboard needs STA | OPEN | notes/shard-console.md §6 |
| T-020 | **Player package on a phone, on cell data** | Install from the download link on a phone off the home network | It installs and connects | OPEN | **The last unproven claim on the project.** Everything else has been tested on the LAN |
| T-021 | **The updater updates** | Install an older package, run it, let it update | It fetches and applies without a reinstall | OPEN | cc-P5 player-updater |

---

## Results

Newest first. One line each: ID, date, what happened. A `FAIL` names the bug-list row it produced.

- T-017, 2026-09-29: **PASS on what it tests** (the selected row is what gets acted on). Delete named and deleted `20260929-142834_T-17` on test after the yes/no. Ran for real, not dry (D37), so re-confirm the printing after the D37 fix alongside T-018. Nothing lost: that snapshot's contents are the current test save, and the pre-restore snapshot is kept.
- T-018, 2026-09-29: **FAIL.** Pressed Stop on live in the console under `-DryRun`, typed the phrase, and **the live shard actually stopped.** The phrase quoting through `Start-Process` did work. Produced bug-list **D37**.
- T-017, 2026-09-29: **BLOCKED by D37 (Delete half).** Restore half good: it named the selected snapshot `20260929-142834_T-17` and restored it onto **test** (10/10 steps, pre-restore snapshot `20260929-143015_PRE-RESTORE_...` kept, old save moved to `Saves-test.aside-20260929-143015`). But it **ran for real** under `-DryRun` (D37). **Do not press Delete until D37 is fixed**, it would delete a real snapshot.
