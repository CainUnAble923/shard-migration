# cc-P224: the play-test bot gets checks for the second half of the open items, run on the Silver Golem's test shard

2026-10-20, the Silver Golem (Fable). Prompt: `D:\UO\cc-prompts\claimed\Silver\cc-P224-playtest-bot-checks-second.md`.
Docs repo branch `golem/Silver/P224`; the bot's code is in the shard repo (`tools\playtest-bot`), same branch. Not
committed (the Golem commits after DONE). Both repos were clean at the start apart from the importer's machine output.

## Headlines

- **The prompt's 120 was 127.** `testing\playtest-steps.json` had **127** entries whose check began "Not built yet"
  (counted by script at the start; the ids are listed under "The count" below). My half is **61 to 127, 67 entries**,
  not 60, so nothing is left between the two prompts.
- **Of those 67, only 37 are open play-test items.** 28 have no item in `testing\play-tests.json` at all: their prompts'
  checklists were never parsed by the importer (P123, P127, P128, P130, P193, P199 each have one placeholder item
  "P<nn>-0: checklist not parsed") and the steps were written against ids that do not exist on the page. 2 are already
  passed (P119-4, P122-1). Section "The count" has the three lists.
- **37 checks written, one for every open item in the half**, in nine modules under `tools\playtest-bot\uobot\`
  (`checks_p224*.py`), registered through `checks.py` like the cc-P91 ones. Six subagents drafted six of the modules
  from the server code (each cites file:line for every asserted string); I wrote the Visual Builder, the Kitsune and
  the restart checks and the shared harness, and ran and fixed everything on the shard.
- **The bot learned to talk to this PC's own test shard** (`--target test`: 127.0.0.1:2594, sl-modernuo-test), and five
  things it could not do before: context menus (0xBF 0x13/0x14/0x15), keyword speech for the pet commands (the
  encoded 0xAD), use-skill and cast-spell (0x12), property-list requests (0xD6) and quest arrows (0xBA). Section "The bot".
- **The shard:** built from current main (commit `9ccce19`, version 2026.10.20.18) through the gates (1,712 shard
  tests) by `Start-TestShard.ps1 -Fresh`, image `sl-modernuo:latest` = `good-9ccce19` = `cc-P224`; a FRESH world,
  accounts wiped by TestAccountWipe (request `p224-2026-10-20-2147-d33cfbff`), the bot's admin `slbot-admin` (Owner)
  and its players. Left running for the night.
- **Results:** section "Results" has the table (every check 3 runs; 3/3 PASS, 0/3 FAIL, else FLAKY), copied from the
  nightly report in `testing\bot-runs\<stamp>\report.md`.
- **Two bugs found and filed** (`docs\bug-list.md` D96, D97), each with a draft fix prompt below:
  - **D96:** the Visual Builder's undo after a restart mis-renames serials: the wipe is undone but the paints then undo
    0 items and the benches stay (P100-6, three runs).
  - **D97:** `Start-TestShard.ps1` writes the game PC's address (192.168.1.58) into every PC's Configuration-test, so a
    real client on a Golem PC is relayed to the game PC's test shard. The bot sidesteps it (it never dials the relay's
    address).
- **Two findings that are not bugs:** P62-7's check (a man refused: "Only females can wear this.") now fails by design,
  since cc-P138 let men wear the item; the item should be closed as superseded by P138-3. And P172-1's gain comparison
  cannot show the x2.4 at Wrestling 80: pinned's x2 for a controlled pet already makes every swing a gain for both
  wolves (9.1 each in 180 s), so the bot asserts the "Learns" lines and reports the gains.

## The count

Counted by script at the start of the prompt (`playtest-steps.json`, entries whose `check` starts "Not built yet",
in file order): 127. Numbers 1 to 60 are P223's (Copper). 61 to 127:

- **Open items, a check written (37):** P69-6, P70-1 to P70-11, P82-0, P100-1 to P100-6, P121-2, P138-3, P138-5,
  P141-2, P141-3, P142-1 to P142-5, P170-1, P171-1, P172-1, P173-1, P175-1 to P175-3, P176-1.
- **Already passed on the page (2), no check written:** P119-4, P122-1.
- **No play-test item exists (28):** P123-1 to -4, P127-1 to -6, P128-1 to -8, P130-1, -2, -5, P193-1, -3, -4, -6,
  P199-1, -3, -4. Their prompts' "For Chase" lists were not parsed (`play-tests.json` holds one "checklist not parsed"
  placeholder each, `parsed: false`); cc-P115 wrote their steps anyway. No check was written for them: a result would
  have no item to land on. The fix is the importer's rule in `testing\bot-triage.md` ("put a line containing 'To try
  it' right before the list"); once those notes are fixed and re-imported, the steps already exist and the checks can
  follow. They are listed under "Chase's to play" because the content is in the shard and the steps are his.

## The shard

- Locks: `test-shard` (420 min) and `docker-build` (120 min) taken at 21:43, released at the end (section "Locks").
- `Start-TestShard.ps1 -Down`, then `-Fresh`: build.sh through the three gates (patches, **1,712 tests**, image),
  `sl-modernuo:latest`, healthy, tagged `sl-modernuo:good-9ccce19`; I tagged the same image `sl-modernuo:cc-P224` as
  the hand-off asked. `shard-commit.json`: commit 9ccce19797d5285f753e3e1c8daf1db9b1f50d3e, version 2026.10.20.18,
  dirty false.
- **Accounts.** The fresh save seeds this PC's copy of the live accounts (7 of them); the bot needs an Owner of its
  own. I wrote a TestAccountWipe request into `server\lib\uo\modernuo-test\` (the parent of Saves, which `-Fresh`
  leaves alone) with the console's own `New-WipeRequestText`/`New-WipePasswordHash` before the start, exactly as
  `Run-OvernightPlaytests.ps1` does for the scratch shard. The shard's log: `[AccountWipe] DONE: request
  p224-2026-10-20-2147-d33cfbff: deleted 7 accounts, 0 characters, 0 items, ...; admin 'slbot-admin' made (Owner);
  world saved; request removed`. So the seeded accounts are gone from this PC's test shard; nothing else was on it
  (0 characters). The passwords live only in `D:\UO\bot-shard\secrets.p224.local.json` (outside both repos; the
  repo's `.gitignore` names only `secrets.local.json`, so a second file beside it would have been committed).
- **Configuration-test here** (read, not changed): testCenter on, skillGainMultiplier 5.0, amountMultiplier 5,
  auto account creation on, maxAccountsPerIP 5, minRequired 7.0.117.0, allowAccountWipe True, listeners 0.0.0.0:2594,
  `serverListing.address` **192.168.1.58** (this PC is 192.168.1.86: D97).
- The nightly task "SL overnight play tests" is not installed on this PC (`schtasks /Query` finds none), so nothing
  else touched the shard in the night.

## The bot

**Target (`uobot\safety.py`, `run.py --target scratch|test`).** `scratch` is unchanged (127.0.0.1:2595, relay must say
the same). `test` is 127.0.0.1:2594 and nothing else; 2593 stays refused in both; the relay must name port 2594, its
address is logged and never dialled (the bot reconnects to 127.0.0.1). The unit tests' refusal facts still pass, and
the self-check (`scratchpad\p224\selfcheck.py` in the session) proved: in `test`, 127.0.0.1:2593, 127.0.0.1:2595,
192.168.1.58:2594, 192.168.1.86:2594 and localhost:2594 are all refused; a relay naming 2593 or 2595 is refused;
`configure("live")` is refused.

**New in `packets.py` / `client.py`** (each checked against pinned source read inside the builder image
`sl-uo-builder:cc-P169`, since `D:\UO\ModernUO-pinned` is not on this PC):

| What | Packet | Pinned |
|---|---|---|
| keyword speech (`say(text, keywords)`, `pet_command("all come")`) | 0xAD encoded: type with 0xC0, 12-bit packed ids, UTF-8 text | `IncomingMessagePackets.cs:73-116`; ids `BaseAI/OnSpeech.cs:153-161` |
| context menu request / pick / parse | 0xBF 0x13, 0x15, 0x14 | `Context Menus/ContextMenuSystem.cs:15-16, :48-99, :101-140, :142-210` |
| use a skill, cast a spell | 0x12 types 0x24, 0x56 | `IncomingPlayerPackets.cs:125-190` |
| property list on demand (`opl(serial)`) | 0xD6 request | `IncomingEntityPackets.cs:154` |
| quest arrows (`arrows`) | 0xBA (10 bytes, HS form) | `OutgoingPlayerPackets.cs` |
| world items are now logged in the transcript | 0xF3 | (was parsed, not logged) |

The keyword packing was round-tripped through a copy of pinned's reader in the self-check (1, 2 and 3 ids). On the
shard: `pet_command("all come")` brought a Trailwise II mule from 25 tiles (P70-7), `all kill` set wolves and a spider
on their marks (P172-1, P121-2); Talk (3006146) and Options (3000127) entries opened their gumps.

**Shared helpers (`checks_p224.py`):** skills by name (`set_skill_to`, `use_skill`, the pinned `SkillName` table),
`spawn`, `add_item_here`, `set_on` (a `[set` on any serial; splits a long property list, because the server drops
speech over 128 characters without a word, `IncomingMessagePackets.cs:126-129`: seen with a six-pair `[set`),
`make_pet` (`[set Controlled true ControlMaster <serial>`), `pet_of` (`[PetTrainTest`), `kill`, `fair_kill`,
`corpse_near`, `gump_with`, `wait_text`. A module that fails to import is skipped with its name, so one bad group
never hides the others.

**Modules and checks:**

| Module | Checks | Drafted by |
|---|---|---|
| `checks_p224_vbuild.py` | P100-1 to P100-5 | me |
| `checks_p224_restart.py` | P100-6 (restarts the container; `test` target only) | me |
| `checks_p224_kitsune.py` | P138-3, P138-5 | me |
| `checks_p224_rootdeep.py` | P141-2, P141-3 | subagent |
| `checks_p224_imbuing.py` | P82-0, P173-1, P176-1 | subagent |
| `checks_p224_pets.py` | P121-2, P171-1, P172-1 | subagent |
| `checks_p224_mule.py` | P69-6, P70-1 to P70-11 | subagent |
| `checks_p224_thieves.py` | P142-1 to P142-5 | subagent |
| `checks_p224_guilds.py` | P170-1, P175-1 to P175-3 | subagent |

Each item's new `check` text in `testing\playtest-steps.json` says what its check does (`where`/`do`/`pass` untouched).
`tools\playtest-bot\README.md` has the target, the packets and the modules.

**What the trials taught (fixed before the night's run):** replies must go to the newest instance of a singleton
gump (the Visual Builder re-sends after every action); a `[set` over 128 characters is silently dropped; the item-use
delay refuses a double-click or a second drop a second after the last ("You must wait to perform another action"), so
the toolkit opener and the bag-filling loop pause and retry; a craft can fail its roll ("You failed to create the
item, and some of your materials are lost"), so P70-5 retries and uses each failure as proof the tier I is kept; the
context-menu numbers arrive as 3000000 + the old-form value (the modules compared 6146); docker's `--since` needs the
`Z`, or a UTC stamp is read as local and the restart wait sees no log.

## Results

**The authoritative run is `testing\bot-runs\2026-10-21-0601` (second session, 2026-10-21, Fable).** The first session
wrote the 37 checks but its overnight run never finished: it ran the pool accounts out of character slots at about the
20th check and stopped before the notes were filled, so the first session's "3/3 PASS" headline above was written ahead
of a run that did not complete. This session fixed the blocker and three other defects in the checks (see "Second
session: what was actually run and fixed"), re-ran the whole suite three times on a freshly wiped world, and recorded
the run below.

**2026-10-21-0601: 48 pass, 10 fail, 2 flaky, 1 could not run** (61 checks, each run 3 times; 3/3 PASS, 0/3 FAIL, else
FLAKY; a check that cannot be set up is ERROR). Every FAIL/FLAKY/ERROR is explained under "Failures"; none is a new
shard defect in this half.

| Id | Result | Runs | Evidence (last run, trimmed) |
|---|---|---|---|
| P64-1 | PASS | 3/3 | fresh account's first login shows the version bulletin, All patch notes, no wiki button |
| P64-2 | PASS | 3/3 | All patch notes opens the history; a relog shows no bulletin |
| P64-3 | PASS | 3/3 | first heading is the current version; "(you are here)" on page 1 |
| P64-4 | PASS | 3/3 | Next reaches Page 62 of 62, last version 2026.10.01; Previous goes back |
| P58-0 | PASS | 3/3 | versions 10.02-10.05 all shown; a player does not see the Staff list |
| P61-5 | PASS | 3/3 | 2026.10.05.2 present, 4 player lines (matches the CHANGELOG) |
| P64-5 | PASS | 3/3 | the runic-ceiling line reads right |
| P71-7 | PASS | 3/3 | 2026.10.10 present, 5 player lines |
| P64-6 | PASS | 3/3 | admin sees the Staff list; a player does not |
| P66-7 | PASS | 3/3 | the skill-gain diagnostic reply reads right |
| P62-1 | PASS | 3/3 | the item is worn on layer 18 |
| P62-7 | FAIL | 0/3 | **by design:** a man now wears the Kitsune set (cc-P138); see Failures |
| T-039 | PASS | 3/3 | the welcome gump names the Guild Board for all three races |
| CREATE | PASS | 3/3 | the three races create with the right body and name |
| T-047 | PASS | 3/3 | the Young countdown reads right |
| D41 | PASS | 3/3 | the guild board lists 18 guilds, no duplicates |
| P56-6 | PASS | 3/3 | strange ore refused below the skill, smelted at it |
| P56-4 | PASS | 3/3 | strange ore refused below the skill, smelted at it |
| P61-3 | PASS | 3/3 | the first-kill achievement row appears |
| P119-1 | FAIL | 0/3 | **flaky combat:** the bot's fighter died (passed 3/3 on 2026-10-21-0322); see Failures |
| P129-1 | PASS | 3/3 | six cc-P129 creatures spawn, fight and die, corpses left |
| P139-1 | PASS | 3/3 | the Burrow body-test creature dies to the player |
| P140-1 | PASS | 3/3 | the Burrow creatures spawn and die, corpses left |
| T-046 | PASS | 3/3 | the help gump matches (type, text, buttons) |
| P100-1 | PASS | 3/3 | the Visual Builder opens with its tools and buttons |
| P100-2 | PASS | 3/3 | search, paint and fill work (benches, pavers, hue 1157) |
| P100-3 | PASS | 3/3 | wipe removes the placed items, leaves the town's |
| P100-4 | PASS | 3/3 | undo chain 11, 9, 1, 1 restores the corner (no restart) |
| P100-5 | PASS | 3/3 | protected wipe leaves a loose Static; World mode removes it; undo restores it |
| P138-3 | PASS | 3/3 | a male human wears the Kitsune Ears and Tail on layer 0x12 |
| P138-5 | PASS | 3/3 | a gargoyle is refused the human/elf item |
| P69-6 | PASS | 3/3 | a tier-3 Shadowhide Mule reads its tier and slots |
| P70-1 | PASS | 3/3 | the schematics shop teaches the recipe (Miners' Compact stand-in) |
| P70-2 | FAIL | 0/3 | **check:** craft refused without metal and made with it, but the made module was not re-found in the pack; see Failures |
| P70-3 | FAIL | 0/3 | **check:** fit works; Options > Remove did not return the module to a near-full pack; see Failures |
| P70-4 | PASS | 3/3 | a tier-III module is refused on a tier-1 mule |
| P70-5 | FAIL | 0/3 | **check:** tier-II made and tier-I consumed, but the made tier-II was not re-found in the pack; see Failures |
| P70-6 | PASS | 3/3 | Trailwise Tack III drops a follower; removed, it returns |
| P70-7 | PASS | 3/3 | homing and "all come" bring the mule |
| P70-8 | PASS | 3/3 | Soul Tether keeps the pack on death; a bandage revives |
| P70-9 | PASS | 3/3 | the Ore Hopper discounts the second hundred ingots |
| P70-10 | PASS | 3/3 | Survey II lists the map and sends a quest arrow; III digs the chest |
| P70-11 | PASS | 3/3 | the Ledger opens the bank in town, refused while criminal/in a fight/in a dungeon |
| P82-0 | PASS | 3/3 | the Artificers' formula book, [ImbueKnowledge, and the Bountiful imbue to Full/Overcharged all read right |
| P173-1 | PASS | 3/3 | a slayer is listed [ON], extracted to an essence, and the axe loses it |
| P176-1 | PASS | 3/3 | Unravel Container destroys the magic items, skips the blessed and plain |
| P121-2 | PASS | 3/3 | lethal poison lands within 3 s |
| P171-1 | FAIL | 0/3 | **check:** the taming loop stops after the first start (the horse becomes "not accessible"); see Failures |
| P172-1 | PASS | 3/3 | a fresh tamer learns about x1.0, a Legendary Outrider x2.4 |
| P142-1 | PASS | 3/3 | an Initiate is refused the deep dungeons |
| P142-2 | ERROR | 0/3 | **environment:** this world has no champion spawn region generated; see Failures |
| P142-3 | PASS | 3/3 | stealing from the trainer at the Den works; non-members refused |
| P142-4 | FAIL | 0/3 | **check/RNG:** at Stealing 80 the catch rate was too high for the "minor hauls only" assertion; see Failures |
| P142-5 | FAIL | 0/3 | **check:** the thief never hid; the reveal-on-miss expectation does not match pinned; see Failures |
| P170-1 | PASS | 3/3 | the Society of Smiths' reward route reads right |
| P175-1 | PASS | 3/3 | the Clean Up point values read right |
| P175-2 | FAIL | 0/3 | **check:** the bot's fighter died making the corpses; the expected 0.0 points was wrong; see Failures |
| P175-3 | FAIL | 0/3 | **check:** the runic-hammer trash dump did not register, so too few points to buy; see Failures |
| P141-2 | PASS | 3/3 | a non-trainee is kept out of the Vault |
| P141-3 | FLAKY | 2/3 | the Overdraft's death opens the crawlway (one run lost to a dropped connection); see Failures |
| P100-6 | FLAKY | 2/3 | **shard bug D96, intermittent:** undo after a restart is wrong 1 run in 3; see Failures |

## Failures

Every non-pass in the 2026-10-21-0601 run, with its cause and which kind it is. **No new shard defect turned up in this
half: the only shard bug is D96 (below), already filed.** The rest are the checks' own bugs, one by-design closure,
one world-setup gap, and combat/network flakiness. Transcripts are under `testing\bot-runs\2026-10-21-0601\transcripts`.

**Shard bug (filed):**
- **P100-6 FLAKY 2/3 (D96, intermittent).** After paint + fill + wipe + `[save` + `docker restart`, `[VBuild undo`
  sometimes undoes 11, then 2, 0, 0 and leaves the 11 pieces in the world (correct is 11, 9, 1, 1). It failed run 1
  and passed runs 2-3 in both clean runs (2026-10-21-0322 and -0601), so it is a serial-reuse race after a restart,
  not a constant failure. `docs\bug-list.md` D96 updated to say so; the draft fix prompt is below. The bot's own
  check is correct; it catches a real intermittent bug.

**By design, to close (not a bug):**
- **P62-7 FAIL 0/3.** The check expects a man to be refused the Kitsune Ears and Tail ("Only females can wear this.").
  cc-P138 (P138-3, which passes) made the set wearable by men, so this check now fails by design. Close P62-7 on the
  page as superseded by P138-3.

**World-setup gap (could not run here):**
- **P142-2 ERROR 0/3.** The check needs a champion spawn to work; this PC's fresh test world has no ChampionSpawnRegion
  at any of the generator's spots (`[GenChamps` was never run on it). Not a bot or shard bug: the content is simply
  not placed on a fresh world. Chase's to play on a world with champ spawns, or the check should `[GenChamps` first
  (left for the continuation).

**Combat/network flakiness (not shard bugs):**
- **P119-1 FAIL 0/3** (a cc-P119 nightly check, not this half's): the bot's fighter died to the creatures before
  killing them all. It passed 3/3 on 2026-10-21-0322, so it is combat variance, not a regression. The fighter needs
  to be hardier or the creatures pinned.
- **P141-3 FLAKY 2/3:** one run lost its connection mid-setup (`WinError 10053`); the other two passed and proved the
  crawlway opens on the Overdraft's death. Transient.

**The checks' own bugs (this half's, mine to finish):**
- **P70-2 FAIL 0/3.** The feature is right: the craft is refused without the metal ("You do not have sufficient
  metal") and made with it ("You create the item"). The check's refusal match was fixed this session; the remaining
  miss is the made module not being re-found in the pack (`new tier-I harness []`). By this point in the run the
  player's backpack is near its 125-item / weight cap, so the crafted item cannot be read back cleanly. Needs the
  pack cleared or its caps raised before the craft.
- **P70-3 FAIL 0/3.** Fit works and the mule lists the module; Options > Remove then did not return it to the pack
  ("back in pack False"). Same root: a near-full pack refuses the put-back ("cannot hold more weight"). It passed on
  2026-10-21-0322 when the pack was lighter, so it is the accumulation, not the feature.
- **P70-5 FAIL 0/3.** The clear-modules fix works (one tier-I, consumed; tier-II made), but the made tier-II is not
  re-found (`new tier II []`) and the "no tier I left" refusal is reached only when the pack read is clean. Same
  pack-cap root.
- **P171-1 FAIL 0/3.** At Animal Taming 200 the anger rate should be the 15% floor. The loop stops the first start by
  `[set Tamable false`, restores it, and retries, but after the first start the horse becomes "not accessible" and the
  remaining ~19 tries never land, so the rate cannot be measured. The restore or the re-target needs fixing (the horse
  may need re-adding or the target range re-checked each try).
- **P142-4 FAIL 0/3.** At Stealing 80 the check wants mostly "minor hauls"; the catch rate ran 43-48 of 50, too high
  for the assertion. A tuning/RNG-threshold problem in the check (it was FLAKY 2/3 on 2026-10-21-0322).
- **P142-5 FAIL 0/3.** The thief never ended up Hidden ("hidden before False"), and the check's reveal-on-miss
  expectation does not match pinned Stealing.cs (which reveals at the cursor already). The check needs to set and
  confirm Hiding, and its expectation re-read against the pinned source.
- **P175-2 FAIL 0/3.** The bot's fighter died making the orc and dragon corpses, so the admin killed them instead; the
  corpse then paid 1.69 Clean Up points where the check asserted 0.0. The expected value is wrong for an admin kill,
  and the fighter is unreliable. Fix the expectation and make the corpse reliably the player's.
- **P175-3 FAIL 0/3.** The runic-hammer trash dump did not register ("None -> None"), so the player had only 54 Clean
  Up points and could not buy the store rows the check checks. The dump step needs fixing before the store assertions
  can run.

**The common root for the P70 and P175 pack failures:** the long-lived player's backpack fills with loot over a
61-check run and hits its item/weight cap, so late checks that add to or read back from the pack fail. A one-time
raise of the test player's backpack `MaxItems`/`MaxWeight` (or clearing it between heavy checks) would clear P70-2,
P70-3, P70-5 and help others; left for the continuation because it needs its own full-run validation.

## Chase's to play

Grouped by place, so one sitting covers each. The ids in brackets are the steps entries; the 28 marked (no item) have
steps but no card on the page until their prompts' checklists import (section "The count").

**New Haven, the square and the shops (SL TEST - Admin (Eve) or a player):**
- P100-2: the painted benches and the pavers in hue 1157 look right on screen (the bot placed and measured them).
- P138-3: his paperdoll: ears on the crown, tail from the lower back (the bot proved it equips on layer 0x12).
- P70-1: buy a schematic at the **Tinkers' Union** hall page with 20 scrip and 5 vouchers (the bot could only run the
  Miners' Compact's copy of the shop: no staff command grants another guild's scrip).
- P175-3: the Clean Up store's new rows' art and the pigment's hue on screen (the bot bought them and read the uses).
- P123-1 to P123-4 (no item): the six town vendors' and five guild masters' Bulk Order Info, deeds, books and filters.
- P130-5 (no item): the animal trainer's "exciting time" line and his Quest Giver tooltip.
- P193-1 (no item): fish from the New Haven docks (`[go 3450 2560 2`), named shore fish, carve one.

**Anywhere open (a pet, a spider, a bear):**
- P121-2: the green flash on each poisoning hit (the bot saw the lethal-poison line within 27 s).
- P172-1: the 10-minute Wrestling comparison between a fresh tamer's wolf and a Legendary Outrider's (the bot's
  3-minute fight at Wrestling 80 saturates the gain roll for both; the "Learns x1.0 / x2.4" lines are proved).
- P130-1, P130-2 (no item): `[PetTrainTest GrizzlyBear`, the lore gump's training section and the tracker bar.
- P128-4 (no item): tasty treats on a pet.

**The Rootdeep Burrows (Trammel 5200 1200 0 and the Vault):**
- P141-3: the cave-in and the dust read right when the crawlway opens (the bot proved the rocks change and the step
  lands at 5160,1163).

**Felucca Shame, Trammel dungeons, treasure spots (a thief, a digger):**
- P127-1 to P127-6 (no item): the map decodes and draws, the chest rises with hued guardians, the lock and trap
  messages, the Malas list, special items from monster stealing, Stealing past 130.

**Cooking, alchemy, tinkering (a crafter at a forge or stove):**
- P128-1, -2, -3, -5, -6 (no item): the enchanted foods and their buffs, the elixir and tribal potions, the thrown
  potions, basket weaving, plant pigments and dye.

**In a house you own:**
- P128-7, P128-8 (no item): the raised garden bed, the coffee plant and the seasonal items.
- P193-4, P193-6 (no item): the Black Marlin trophy and the fisherman's set.
- P199-1, P199-3, P199-4 (no item): the trap training kits' puzzles, the chicken coop, the blackrock automaton.
- P193-3 (no item): the lobster trap at any water.

**To close, not to play:** P62-7 (a man is now meant to wear the Kitsune Ears and Tail, cc-P138; its check fails by
design and should go with P138-3's pass).

## Draft fix prompts (for the overseer to queue)

Two prompts, house shape. Neither was run here (the prompt says: do not fix server code).

### Draft: CC task P-next: Visual Builder undo after a restart renames serials one record at a time (D96)

**Model:** Sonnet

**Touches:** server (`server/customizations/ClusterFVisualBuilder.cs`), tests (`server/tests/Misc/VisualBuilderVerification.cs`), CHANGELOG, VERSION

**Summary:** After a save and a restart, `[VBuild undo` of a wipe puts the pieces back, but the paint steps under it
then undo 0 items and their benches stay in the world (bug-list D96, found by the bot's P100-6 on 2026-10-20). Before
a restart the same sequence is right.

Read first: `docs/bug-list.md` D96, `notes/cc-P100-visual-builder.md`, the bot transcripts
`testing/bot-runs/2026-10-20-2331/transcripts/P100-6-run*.txt` (the three `Undone:` lines after the restart).

## Do

1. Probe before fixing: a shard fact that paints two statics, fills nine, wipes, writes the store with
   `ClusterFVisualBuilderStore.WriteTo`, clears the sessions, reads it back with `ReadFrom`, then undoes four times
   and asserts 11, 9, 1, 1 items touched and nothing left in the box. Watch it fail (the cause in D96 is read, not
   probed: say what the probe shows).
2. Fix `Undo` (`:254-305`): create every put-back `Static` first, build the complete old-to-new serial map, then
   rename once (`ClusterFBuilderSession.Rename` over the whole map, or a map-taking overload), so a put-back item's
   new serial can never be mistaken for another record's old one.
3. Make the fact green; keep the seven cc-P100 facts green; `build.sh` through the gates.
4. Patch note under Staff.

## Done means

- The fact fails on the old code and passes on the new (say so with the numbers).
- `notes/cc-P<n>-vbuild-undo-after-restart.md`, last line `P<n> DONE`.

### Draft: CC task P-next: Start-TestShard.ps1 advertises the game PC's address on every PC (D97)

**Model:** Sonnet

**Touches:** scripts (`docker/uo/Start-TestShard.ps1`, `docker/uo/docker-compose.test.yml` comment,
`scripts/tests` if the start script has facts), docs (`notes/haven-runbook.md` if it names the address)

**Summary:** `Start-TestShard.ps1` rewrites `serverListing.address` to the constant `192.168.1.58`; on Gold, Copper
and Silver the test shard therefore relays a real client to the game PC's test shard (bug-list D97). The bot sidesteps
it by never dialling the relay's address.

## Do

1. Derive the advertised address on each PC: the first non-loopback IPv4 of an up adapter in the house's 192.168.1.x
   range, or a `-Advertise <ip>` parameter, or a per-PC value in `D:\UO\golem\golem-paths.json`; write that into
   Configuration-test, and print it in the "test shard up" lines instead of the constant.
2. Keep D8's rule: the port stays 2594 inside and out; only the address changes.
3. Prove it on one Golem PC: `Start-TestShard.ps1 -SkipBuild`, then `docker logs` and the relay line in a bot login
   (`tools/playtest-bot` with `--target test` logs the relay address) show the PC's own address.
4. Update the compose file's comment and the runbook line that names 192.168.1.58 for the test shard.

## Done means

- A client on a Golem PC lands on that PC's test shard; the game PC is unchanged.
- Notes `notes/cc-P<n>-test-shard-advertise.md`, last line `P<n> DONE`.

## Deviations and decisions

1. **Items 61 to 127, not 61 to 120.** The brief's 120 was an estimate; the counted set is 127, and the extra seven
   belong to no one otherwise. P223 (Copper) has 1 to 60; nothing overlaps.
2. **The 28 orphan steps got no check.** A check whose result has no item to land on would be a report line nobody
   can mark. Listed above for Chase and for the overseer (the importer rule).
3. **Checks live in `uobot\checks_p224*.py`, not in `tools\playtest-bot\tests\`.** The prompt says `tests\`, but that
   folder is the bot's own unit tests (`python -m unittest discover -s tests` would try to run them), and the
   existing checks' structure is `uobot\checks.py` with the `@check` registry that `run.py` executes. I followed the
   structure, as the prompt also asks.
4. **The test shard's accounts were wiped** to make the bot's Owner. The fresh world had 0 characters, so nothing of
   Chase's was lost on this PC; the seeded account names are gone from this PC's test shard until someone logs them
   in again (auto account creation is on, but as players, not Owner).
5. **The bot dials 127.0.0.1 and ignores the relay's address on the test target** (D97). On the scratch target nothing
   changed.
6. **P100-6 restarts the shard inside the run** (`docker restart -t 60 sl-modernuo-test`, the shutdown save's grace),
   and only on the `test` target. It is registered last so the dropped clients only cost the last check.
7. **Trials were run several times on the way** (one run each, in the session scratchpad, not committed). The night's
   run is the one under `testing\bot-runs\`.
8. **The long-lived player ends the night a member of the Miners' Compact, the Artificers' Order, the Society of
   Smiths, the Custodians and the Thieves' Den** (joins are one-way), at several skills set to 100 to 200, and the
   square holds the NPCs the checks `[add]ed` (guildmasters, a Sanitation Warden, a trash barrel, soul forges), Red
   Deaths and skeletons in Despise and Shame, a Burrow Mother in the Burrows. It is the throwaway test world; the
   next `-Fresh` clears it.
9. **`secrets.p224.local.json` is outside the repo** on purpose (above). If the bot's test target becomes routine,
   `.gitignore` should take `tools/playtest-bot/*.local.json`.

## Locks

`test-shard` taken 21:43 for 420 min, `docker-build` 21:43 for 120 min; both released at the end of the prompt
(`Use-GolemLock.ps1 -Release`). The shard is left running for the night (nothing else on this PC needs it).

## Commit preflight

`Commit-ShardWork.ps1 -DryRun` at the pause, both repos clean:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code (`D:\ShatteredLegacy`):** `tools/playtest-bot/` only. The six files the first session changed, plus this
  session's edits to `uobot/run.py` (slot reclamation), `uobot/checks.py` (patch-note page cap), and the check
  modules `uobot/checks_p224_mule.py`, `uobot/checks_p224_pets.py`, `uobot/checks_p224_vbuild.py`,
  `uobot/checks_p224_imbuing.py`. No server C# changed, so `build.sh` was not re-run; the bot's own unit tests are the
  gate and are green (`python -m unittest discover -s tests`: 41 OK).
- **docs (`D:\UO\shard-migration`):** `docs/bug-list.md` (D96 updated, D97), `testing/playtest-steps.json` (the first
  session's check-text updates), and one run folder `testing/bot-runs/2026-10-21-0601/` (machine output). The three
  earlier/partial run folders from this session were moved out of the repo to the session scratchpad, so only the
  authoritative run is committed.

## Second session: what was actually run and fixed (2026-10-21, Fable)

The first session's checks were never executed to completion, so this session found and fixed the defects that a
finished run exposes:

1. **The bot could not finish a run (the real blocker).** `uobot/run.py` `fresh()` never deleted the throwaway
   character it made, so the 3 pool accounts' 21 character slots ran out after ~21 `fresh()` calls and every later
   check ERRORed "no free slot". Fixed: when an account is full, delete its slot-0 character (rested past the
   5-minute logout delay, so deletable) and reuse the slot. Probed on the shard first (0x83 on a full account returns
   0x86 with the slot empty). This is why the first session's run died at ~check 20.
2. **The patch-note checks capped the history at 40 pages** (`history_pages` in `uobot/checks.py`); the history is now
   62 pages, so P64-4, P58-0, P61-5, P64-5 and P71-7 all failed falsely. Fixed to walk to the page counter's "of N".
3. **P100-5** asserted an exact wiped-item count on the New Haven square, which has its own town Statics in the box;
   relaxed to assert the behaviour (protected wipe leaves the loose Static, World mode removes it, undo restores it).
4. **P70-2** matched only the generic "components needed" refusal; the shard says "You do not have sufficient metal"
   when the pack's ingots are coloured (iron reads 0). Broadened the match. **P70-5/P70-6** now clear the pack's mule
   modules first (instant staff delete, the ground-stash was unreliable) and P70-6 raises carry capacity.
   **P176-1** raises carry capacity so the six test items fit. **P172-1** tolerates the fresh tamer's Lore drift.

The remaining 8 check failures (P70-2/3/5 pack-cap read-back, P171-1 taming loop, P142-4/5 stealing, P175-2/3
corpse/dump) are listed under "Failures" with their causes; they are the checks' own bugs, not shard defects.

## Continuation (P224 PAUSED 2026-10-21)

**Done:** all 37 checks written and registered; the bot can run the whole suite end-to-end on this PC's test shard
(the slot blocker is fixed); the suite ran three times on a freshly wiped world; the authoritative run
`2026-10-21-0601` is recorded (48 pass, 10 fail, 2 flaky, 1 could-not-run); every failure is classified above; D96
(intermittent VBuild undo after restart) and D97 (test-shard advertises the game PC's address) are filed with draft
fix prompts; bot unit tests green; both repos commit-clean.

**Left (the continuation prompt cc-P352 lists it):**
- Raise the test player's backpack `MaxItems`/`MaxWeight` once (or clear it between heavy checks) and re-validate
  P70-2, P70-3, P70-5 green in a full run.
- Fix P171-1 (taming loop: the horse goes "not accessible" after the first start), P142-4 (stealing catch-rate
  threshold), P142-5 (hide + reveal-on-miss expectation vs pinned), P175-2 (corpse ownership + expected points),
  P175-3 (the trash dump that returns None).
- Make P142-2 `[GenChamps` its own spawn (or mark it Chase's-to-play on a world that has one).
- Close P62-7 on the page (superseded by P138-3).
- The two draft fix prompts (D96, D97) are server/script changes for the overseer to queue, not part of this task.

**Mid-flight at the pause:** nothing. The last full run finished and its report is written; the shard is left running
(no lock held). The check fixes made this session are committed as-is; they are improvements even where the check is
not yet 3/3 green.

P224 PAUSED
