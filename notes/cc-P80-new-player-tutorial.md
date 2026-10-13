# cc-P80: New player tutorial, framework pass

Run 2026-10-13 by Claude Code (autopilot hand-off after P79). Builder: Part A facts first (nothing blocked Part B),
then the framework.

- **Pinned:** `D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88`.
- **TazUO:** source `D:\UO\cc-p40-work\tazuo-3212623f` (commit 3212623f, v26.0909.63).
- **Code repo:** `D:\ShatteredLegacy`, built as `sl-modernuo:cc-p80`. Not deployed or committed; `latest` unchanged
  (8863156884f8).

**Provenance.** Two research subagents did the Part A reading; their citations are kept as given. I re-read pinned
`Account.RemoveYoungStatus` / `CheckYoung` (`Accounting/Account.cs:830-862`), the achievement trigger table, and the
New Haven plaza tiles (map tools, below).

Short names: **P** = pinned `Projects/UOContent`; **C** = `D:\ShatteredLegacy\server\customizations`.

## Part A: facts

### A.1 New Haven in pinned, and what we have

**Regions** (`Distribution/Data/regions.json`, Trammel):
- **"Haven Island"**: a NoHousingRegion, x 3314-3814, y 2345-3095 (:1499-1505).
- **"New Haven Moongate"**: a GuardedRegion, x 3446-3456, y 2674-2684 (:1507-1513).
- **"New Haven"**: a TownRegion, x 3416-3545, y 2480-2648, GoLocation 3503,2574,14 (:1515-1525), with NoHousing
  sub-regions for the Alchemist, Bard, Warriors, Tailor, Carpenter, Mapmaker, Mage, Inn and Docks (:1527-1658).

**Quests:**
- 26 skill quests (`P/Engines/ML Quests/Definitions/NewHavenSkillTraining.cs`, `GainSkillObjective(skill, 500,...)`
  plus an item each).
- 12 craft and collect quests (`NewHavenTraining.cs`).
- 12 escort quests (`NewHaven.cs`, `NewHavenEscort`, 500 gold).
- The quest-to-giver map is in `Distribution/Data/MLQuests.cfg:207-262`.

**Spawners** (`Spawns/post-uoml/trammel`):
- in town: 56 vendor spawners and 2 town-life spawners;
- around the island: undead at 3650,2509 and 3598,2450, an undead graveyard group at 3618-3651, 2591-2627, wildlife
  rings on every side, and brigand camps to the east.

**Young** in pinned: `Account.cs` (below), `YoungGumps.cs` (renounce), `NewPlayerTicket`,
`PlayerMobile.CheckYoungProtection` (:4021-4052), and `BaseRegion.YoungProtected`. **There is no companion
program.**

**Ours:**
- **`ClusterFNewHavenSeeder.cs`:** every quest giver and trainer, Sir Helper, the League Registrar at 3459,2601,18.
  Public `SpotOf`, `RegistrarAnchor`, and the seeding commands.
- **`ClusterFNewHavenServicesSeeder.cs`:** decoration, ankh, forge.
- **`NewHavenQuestBoard`** at 3502,2573,14, with the 26 quests on its second tab.
- **`CharacterCreation.cs`:** the only start, New Haven 3503,2574,14; Young set and a NewPlayerTicket given at
  :218-226.
- **`GuildWelcome`:** the first-login page, once per character (A.6).
- **The F-35 design, "The First Echo"** (`docs/feature-queue.md:2749-2918`):
  - the story steps;
  - the Echo as the System voice;
  - the west tutorial farm at 3381-3399, 2603-2619, with the farmhouse at 3377,2611 (approved), outside the guarded
    region;
  - Young protection opted out on tutorial creatures.

**Reuse versus build.**
- **Reuse:** the seeder pattern; the region data; the board and trainers (they stay as the second tab, per F-9);
  `GuildWelcome`; `JoinLeague`; `EvoPet.GivePet`; achievements, fanfare and loot boxes; the `OldHavenBurrowsRegion`
  template.
- **Build:** the tutorial record and state machine, the recruiter, the stations, the tutorial creatures, the loop
  signal and the vision. Later: the farm addon and its seeder, the Farmhand, and the trials themselves.

### A.2 F-5 Young as built, and the loop signal

- **Patches:**
  - `Account-young-duration.patch`: 336 hours through `ClusterFYoungPlayer.Duration`, and the login message.
  - `PlayerMobile-young-time-only.patch`: removes the skill-total-450 removal from `OnSkillChange`.
  - Both are registered at `apply-patches.sh:368-374` and tested by `YoungPlayerVerification`.
- **`C/ClusterFYoungPlayer.cs`:**
  - `Duration` 336 h (:29);
  - the "I want to grow up!" phrase opens the stock `RenounceYoungGump` (:32-45);
  - its header cites `CheckYoung` at :833-840, but the actual lines are 855-862. That is a stale citation, not
    changed here.
- **Where Young ends:** pinned `Account.RemoveYoungStatus(int message)` (`Account.cs:830-853`) is the single
  chokepoint. It clears the account flag and every character's `Young`, and sends 1019039 itself.
  - `CheckYoung` (:855-862) calls it when `TotalGameTime >= YoungDuration`, every minute and at load.
  - Murder (`PlayerMobile.OnKillsChange`) and renouncing also call it.
- **The loop system (F-12) is not built.** No document defines a loop event. The F-12 notes put a per-character record
  in `ClusterFAccountData` with `ClusterFSkillCaps.Apply` as the chokepoint (`notes/f12-levels-loops-caps.md:167-170`).
- **The placeholders disagree:** `ClusterFLootBoxes.LoopProvider` defaults to 1, `EvoPet.OwnerLoopsSource` to 0.
  F-12 must reconcile them.
- **Built here:** `ClusterFLoops.CompleteLoop(pm, loop)` is the one call the F-12 reset makes. It ends Young (no patch
  needed; Young is per account, so it ends for every character on it), then plays the loop's fanfare and box. The
  vision never calls it.

### A.3 Achievements, fanfare, System voice

- **Registering:** `Reg(key, title, desc, category, ap, renown, trigger, flavor, itemGumpId, hidden, prerequisiteKey,
  rewardItems, progressCounter, retired)` is private, called from `RegisterAll` (`C/ClusterFAchievements.cs:1021-1034`).
- **Hidden** exists (`AchievementDef.Hidden`, shown "[Secret]" once earned). There is no hidden category.
- **Categories:** Combat, Skills, Exploration, Mining, Crafting, Legacy, Discovery, Collection, League.
- **Granting:** `TryGrant(IAccount, key)` is public. It is **per account**, and now also fires the fanfare and the
  loot box (cc-P79).
- **Added here:** trigger kinds `TutorialSkipped` and `TutorialRemedial` with their Earned lines, and two League
  achievements:
  - **"Didn't Read the Manual"** (`tutorial.skipped`, 5 AP);
  - **"Read the Manual Eventually"** (`tutorial.remedial`, 10 AP, 25 Renown, needs the first).
- **Fanfare:** `ClusterFFanfare.Play(pm, level, pool, vars, tier, line, voiceKey)`. Free text works through `line`.
- **The System voice** is "System: ..." chat lines plus the fanfare's overhead line.

### A.4 League, evo pets, squire

- **League Registrar:** `C/LeagueRegistrar.cs`, "Elara Voss", placed at 3459,2601,18.
  - `ClusterFLeagueSystem.JoinLeague(pm)` is idempotent and grants `league.registered_citizen`.
  - `ShowTheWayToRegistrar`.
- **Evo pets:** `EvoPet.GivePet(Mobile, string line)` (`C/Mobiles/Evo/EvoPet.cs:469-492`).
  - It bonds the pet, sets it to follow, and opens the hue pick.
  - It returns null for an unknown line or no free follower slot.
  - Lines: dog, cat, fox, bird. The fox and bird have stages with pending art.
- **Squire: none in code.** It exists only in the design (`docs/companions/companions-squire-evo-research.md`;
  `notes/cc-P41-companions-research.md`).
- **Graduation hooks into:** `ClusterFLootBoxes.Award` and `EvoPet.GivePet`.

### A.5 What our TazUO lets a server trigger

- **No TazUO-only gump commands, no highlight, no toast, no "open my window" packet.** The gump parser
  (`Network/PacketHandlers/Helpers/GumpHelpers.cs`) accepts only standard commands. Of note:
  - `htmlgump` (its `<a href>` links open the browser when clicked; `HtmlControl.cs:308-327`);
  - `tooltip` (cliloc) and `itemproperty`;
  - `maparea` (a live map region; TazUO-only, so send it only to TazUO);
  - anything else logs "Invalid Gump Command" (:565).
- **Standard packets it honors:**
  - 0xA5 open URL (no confirmation; use it only on a button press);
  - 0xA6 tips;
  - sounds and music;
  - 0xBA quest arrow;
  - 0xE5 waypoints (only corpse and resurrection types show on the map);
  - closing gumps or the paperdoll.
- **Enhanced packet 0xCE** has only "enable" and DisableFeatures/TreeToStumps (`EnhancedPacketHandler.cs`). The client
  never says it is TazUO on our shard, unless it answers a 0xCE id 1.
- **Client commands** (`-optlink`, `-paperdoll`, `-marktile`, `-cast`, `-organizer`, Legion's `-playlscript`...) run
  only from chat, macros or Legion scripts. **A server cannot run them for the player.**
  - There is no command for the World Map, the Journal or the new options window.
  - `-optlink` opens the legacy options window.
- **`FeaturesBot.py:34-114`** (repo root) has ready-made one-line feature descriptions with wiki links: good tutorial
  wording.

**Recommendation: server-driven hints now, no client change.** Each station's gump:
- names the key, menu or "-command";
- links the tazuo.org page in htmlgump text;
- uses quest arrows, sounds and tips;
- for features the server cannot see, says "click Next when done".

**If buttons that open TazUO windows are wanted later,** the smallest client patch is about 30 lines:
1. 0xCE id 4, "ClientCommand", with a **whitelist** (optlink, paperdoll, marktile, radius, plus three new commands,
   worldmap, journal and options, calling `GameActions.OpenWorldMap`, `OpenJournal` and `OpenSettings`);
2. run through `CommandManager.Execute` behind the existing enhanced-packet opt-in.

Highlighting a TazUO control would need a new overlay: skip it. A launcher-shipped XmlGump or Legion script is a
no-patch fallback (the installed client already has `Data/XmlGumps` and `LegionScripts`).

### A.6 Making tutorial spawns engage only tutorial players

Pinned's hooks:
- **Target acquisition:**
  - `BaseAI.AcquireFocusMob` rejects a candidate that fails `CanSee` or, for a foe check, `IsEnemy` /
    `CanBeHarmful` (`BaseAI.cs:853`, :1045-1047, :1073-1075);
  - approach aggro needs `IsEnemy && CanBeHarmful` (`BaseCreature.cs:1353-1358`).
- **Overridable:**
  - `BaseCreature.IsEnemy(Mobile)` (:1684);
  - `CanBeHarmful(target, message, ignoreOurBlessedness)` (:3717);
  - `Damage(amount, from, ...)` (:1846);
  - `IgnoreYoungProtection` (:1313);
  - `NoKillAwards` (:1315).
- **Region:** `Region.AllowHarmful` (`Server/Regions/Region.cs:802`) is asked of the **attacker's** region only
  (`Mobile.cs:8366-8374`), so a region alone leaves a gap.
- **No instancing exists.**

**Chosen (no pinned patch): a `TutorialCreature` base class.**
- `IsEnemy` and `CanBeHarmful` are false for anyone not in the tutorial. The AI never acquires them and never strikes
  them.
- `Damage` from them is ignored, wherever the attacker stands, which closes the region gap.
- `NoKillAwards`, no loot.
- `IgnoreYoungProtection`, since tutorial players are Young.
- "In the tutorial" (`ClusterFTutorial.IsParticipant`): the account is in the core, the wings or remedial training,
  and this is the character doing it. A pet counts as its master.
- A tutorial region (`AllowHarmful`, the `OldHavenBurrowsRegion` pattern) can be added with the farm. It is not needed
  for the guarantee.

## Part B: what was built (`server/customizations/Tutorial/`)

| # | Item | Where |
|---|---|---|
| 1 | Per-account state: NotStarted, InCore, InWings, Graduated, Skipped, Remedial; the character doing it; stations done; skipped before; times. Saved in **`ClusterFAccountData` v19** (`TutorialRecord`, its own version) | `C/ClusterFAccountData.cs` |
| 2 | Entry: `[OnEvent(PlayerLoginEvent)]`. The first login of a character whose account has never started puts it in the core, with System lines and a quest arrow to the recruiter. The recruiter (**"Rook Hallowell, the League recruiter"**) opens the station page | `ClusterFTutorial.cs`, `TutorialRecruiter.cs`, `TutorialGumps.cs` |
| 2 | **Recruiter spot 3500,2572,14:** open plaza floor two tiles from the arrival point, clear of Sir Helper (3503,2574), the board (3502,2573) and the fountain (3504-3508, 2574-2578). Checked with the cc-P15 `Map.CanFit` port (`notes/cc-P80-tools/probe.py`: z14 all around). **Placed only by `[ClusterFSeedTutorial [dryrun]`** (or `tutorial.seedOnWorldLoad`, default false) | `TutorialRecruiter.cs` |
| 3 | **Skip:** two System-voice confirmations (`TutorialSkipGump` step 1, then step 2), then `Skip`, which grants "Didn't Read the Manual". **Remedial:** the recruiter offers it to a skipper; graduating from it grants "Read the Manual Eventually" and the normal rewards | `ClusterFTutorial.cs`, `TutorialGumps.cs` |
| 4 | **Young ends at the first real loop:** `ClusterFLoops.CompleteLoop` (F-12's call) runs `RemoveYoungStatus`, then the loop fanfare and box. **The vision** (`TutorialVision.RunLoopDemo`, the `core.loop` station) only sends lines and an effect; it never touches level, skills, loop count or Young | `ClusterFLoops.cs` |
| 5 | **Station framework:** 37 stations as data (9 core, 28 wing), each with its hands-on, covered and explained skills, TazUO features, tool and place. A trial is registered by key in `TutorialStations.Handlers`; a station without one runs the stub (a plan gump, then counted done). **Every trial is a TODO** except the loop vision | `TutorialStations.cs` |
| 6 | **Graduation** (core done): the first loot box (`ClusterFLootBoxes.Award`, source `tutorial:graduation`, an Explorer's tier 1; the System says to open it in town, which teaches the guard-zone rule), then the evo pet pick (dog, cat, fox, bird; `EvoPet.GivePet`; refused with no follower slot). `GraduationRewards` is a replaceable hook. The squire is not built; it comes from a League quest later | `ClusterFTutorial.cs`, `TutorialGumps.cs` |
| 7 | **Tutorial-only engagement:** `TutorialCreature`, plus the first stub `TutorialEcho` ("an echo of a rat", stock rat body 0xEE, hue 0x482) | `TutorialCreature.cs` |
| 8 | Patch notes 2026.10.13.3; `VERSION` | `CHANGELOG.md` |

**Also:**
- **Staff command:** `[Tutorial status|enter|station <key>|skip|remedial|graduate|reset` (DevTool, test shard,
  targets a player).
- **Setting:** `tutorial.enabled` (default true).

**The stations as registered:**
- **Core:** movement, paperdoll, backpack, chat, death and resurrection, banking, travel, the League, the loop vision.
- **Combat:** pick-your-weapon (Swords, Macing, Fencing, Archery, Throwing, Wrestling; covers Tactics, Anatomy,
  Parrying, Focus; explains Resisting Spells), healing.
- **Magic:** Magery (covers Meditation and Eval Int), Necromancy (covers Spirit Speak), Chivalry, Bushido, Ninjitsu,
  Mysticism (explains Spellweaving and its quest).
- **Gathering:** Mining, Lumberjacking, Fishing, Camping (explains Herbalism).
- **Crafting yard:** Blacksmithy (covers Arms Lore; explains Imbuing), Tailoring, Carpentry, Tinkering (covers Item
  ID), Alchemy (covers Taste ID), Fletching, Cooking, Inscription, Cartography.
- **Animals:** one trial (Taming, Lore, Veterinary, Herding).
- **Bard:** one trial.
- **Thieving and stealth:** one trial (ten skills; explains Forensic Evaluation).
- **Non-skill wings:** housing, travel, reputation, shard systems.
- **Every TazUO feature from the brief** is assigned to a station's list.

**Two things to know:**
- **Existing characters:** every account starts NotStarted, so any existing character is entered at its next login.
  On the coming fresh world that is everyone, as intended. On the live world today, veterans would be greeted too.
  Set `tutorial.enabled` false there until the wipe (decision 1).
- **The F-35 story** fits this framework: its steps become trials registered by key, and its farm becomes the
  gathering, animals and combat stations' place.

## Part C: art plan (notes only; nothing registered or shipped)

Nothing ships until:
- it is in `player-package\vendor\shattered-legacy-art\registry.csv`, with a slot from `scripts\find-free-art.py`;
- its SOURCE.txt terms are met.

DRC1K art: no modifications without his OK. In-game hues are fine.

**Stock art each station uses now (no new art needed for the framework):**
- **The recruiter:** a hued human in a Celestial-hue shirt and sash.
- **Stations:** gump text with background 9270 (not the gump art 3500 to 3508 that Fiddle-Me-This replaces).
- **The loop vision:** stock sparkles 0x376A in the Celestial hue.
- **The echo:** the stock rat body with a pale hue.

**Third-party pieces for a later art registration prompt.**

On disk (`D:\UO\third-party\`):

| Station | Folder, files | Terms |
|---|---|---|
| Combat wing camp | `orc-encampment\Orc encampment` (cage, meat hang, bonfire, rug, palisade, 3 tents, 4 directions; file names are Vrark's intended 0xB2xx IDs, check they are free; 6 BMPs to re-make from the PNG masters) | Vrark: "do with as you wish" |
| Death and resurrection | `drc1k-uoassets\Graveyard` (graves, tombstones 1 to 8, iron fences, lampposts, pillars, tendrils) | DRC1K |
| Dungeon intro (the cave-in step) | `drc1k-uoassets\Sewer_Assets` (pipes, sewer arches), `drc1k-uoassets\The Ultimate Dungeon Wall Set by-DRC1K` (54 files, stairs and walls) | DRC1K |
| Gathering wing (the farm) | `farm-carts\FarmCartGraphics` (Item_06784 to 06808 .tiff); `drc1k-uoassets\Halloween 2024 Assets` corn1 to 14, pumpkin1 to 12, scarecrow.bmp, corspe1 and 2 | Moonrose: none stated; DRC1K |
| Travel wing | `animated-runestone` (**already shipped**, 0x3C10 to 0x3C3B) | cleared |
| Paperdoll lesson (F-23) | `paperdoll-siege-of-sosaria` (never `MUL Files\`) | none stated; Chase's F-23 rules |
| Animals wing and echoes | `mobile-megapack\Mobile Pack`: Gronk, L_Boar, L_Fox (plus L_Bird for the bird line). **Not the Diablo packs** | Mobile Pack cleared by Chase 2026-10-05 |

Queued, **not on disk yet** (`download-queue.md`, all "todo" on 2026-10-13):

| Row | Piece | Planned folder | Station |
|---|---|---|---|
| 11 | Scarecrow Training Dummy and Pinata (.1346) | `training-dummy-pinata` | combat yard dummies; the pinata as a fanfare gag |
| 12 | Archery Buttes with Arrows and Bolts (.1054) | `archery-buttes` | combat yard, Archery and Throwing |
| 13 | Quest Markers (.1823) | `quest-markers` | "!" and "?" over the recruiter and station NPCs |
| 14 | NPC Shop Signs (.1749) | `npc-shop-signs` | New Haven and station signs |
| 15 | Humanoids (.974) | `humanoids` | echo monsters: kuo-toa fry, gnoll, bullywog |
| 16 | Gnolls (.2550) | `gnolls` | echo monsters |
| 17 | Kobold-Bow (.2532) | `kobold-bow` | a ranged echo enemy |
| 5 | Floating Crystals (.2317) | `floating-crystals` | cracked-time effects near the sword fragment |
| - | Spinning Moongates (.2309, .2310, .2312, .2313) | **not in the queue yet**; add rows | cracked-time effects near the sword fragment |

**Echo monsters on stock bodies, hued, until the new mobiles are registered** (pale echo hue 0x482, or the Celestial
0x8AF for the "cracked time" look):

| Echo | Stock body |
|---|---|
| Rat | rat 0xEE (built as `TutorialEcho`) |
| Giant rat | 0xD7 |
| Snake | 0x34 |
| Gnoll stand-in | ratman 0x2A, or orc 0x11 |
| Bullywog stand-in | frog 0x51, or giant toad 0x50 |
| Kuo-toa fry stand-in | lizardman 0x21 |
| Kobold archer stand-in | goblin, if the client has the SA goblin body; else a ratman archer 0x8F |
| Undead echo (the Old Haven beat) | skeleton 0x32, zombie 0x3 |
| Animals wing | stock goat, sheep, cow, chicken |

Verify every body number in a client before use (**unverified** here).

## Tests (red then green)

New: `server/tests/Misc/TutorialVerification.cs`, 6 facts.
1. **Entry and save:** a new character's login enters the core; a relog changes nothing; the account record
   round-trips the state, character and stations.
2. **Skip and remedial:**
   - the first confirmation alone skips nothing, and "no" at the second skips nothing;
   - "yes" at both skips and grants "Didn't Read the Manual"; a second grant is refused, and a skipped account cannot
     skip again;
   - remedial walks the core and graduates, granting "Read the Manual Eventually".
3. **Once per account:** a second character on the account is never entered and is not a participant; after
   graduation nobody on the account enters.
4. **The loop vision** leaves every skill, the level stand-in, the loop number and Young (account and character)
   unchanged. `ClusterFLoops.CompleteLoop` ends Young for both.
5. **Engagement:** an echo is an enemy to the tutorial player and not to a graduated veteran; it cannot harm the
   veteran; the veteran's damage does nothing while the participant's lands; no kill awards; Young protection
   ignored.
6. **The framework:** all 37 station keys registered (9 core); graduating early is refused; walking the core opens
   the wings; a wing station runs; graduation gives exactly one loot box and, without a skip, no remedial
   achievement.

**Changed:**
- `AccountDataSerializerVerification`: three version asserts, 18 to 19.
- `AchievementEarnedLineVerification`: 74 to 76 registered achievements, twice. Both new achievements have Earned
  lines, which that test checks.

| Run | Result |
|---|---|
| Builds 1 to 3 | missing `using Server.Gumps` (code and test) |
| Build 4 | 1 failed: the test set only the account's Young flag; the character's own `Young` must be set too. Also changed `CompleteLoop` to pass 0 to `RemoveYoungStatus`, which sends 1019039 itself, so the line is not doubled |
| Green, tests only | **1116 passed** |
| Red 1 | entry ignoring the account state; the first confirmation skipping; the vision resetting a skill and the real loop leaving Young; echoes engaging everyone; a station missing: **5 failed** (all but the save fact) |
| Red 2 | the record not saving its state: **1 failed** (the save fact) |
| Restore | backups copied back, `cmp` byte-identical |
| Green, full | **1116 passed**; "Built sl-modernuo:cc-p80 with patches applied and 1116 shard test(s) passing." |

## Decisions for Chase

1. **Existing characters:** every account starts NotStarted, so live veterans would be greeted at their next login.
   Turn `tutorial.enabled` off on live until the fresh world, or mark existing accounts Graduated?
2. **Recruiter:** "Rook Hallowell, the League recruiter", at 3500,2572,14 on the plaza. Or should Elara Voss (the
   Registrar) also play the recruiter? Placement waits for `[ClusterFSeedTutorial`.
3. **The System voice** is "System: ..." text; F-35 called it the Echo. Same voice?
4. **Achievement values:** "Didn't Read the Manual" 5 AP; "Read the Manual Eventually" 10 AP and 25 Renown. League
   category, not hidden.
5. **Graduation box:** an Explorer's tier 1 (Common). Pick another theme or tier?
6. **TazUO:** server-driven hints only for now. Want the about-30-line client patch (0xCE ClientCommand with a
   whitelist) so station buttons can open the World Map, Journal or options?
7. **The loop placeholders disagree** (loot boxes say loop 1, evo pets say 0). F-12 must reconcile them.
8. **Order of trials:** the F-35 story order (gather, craft, tame, fight, heal, spell, dungeon, travel, echo) versus
   this brief's core and wings. The framework takes either; the trial prompts decide.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, run 2026-10-13 before DONE:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **Code, 13 files:** CHANGELOG.md, VERSION, ClusterFAccountData.cs, ClusterFAchievements.cs, the two changed tests,
  the 6 files in Tutorial/, and TutorialVerification.cs.
- **Docs, 4 files:** this note and `notes/cc-P80-tools/` (fit.py, nhmap.py, probe.py).
- No file is near 5 MB; nothing BLOCKED.

P80 DONE
