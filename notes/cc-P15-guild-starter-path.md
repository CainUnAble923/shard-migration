# cc-P15: guilds become the starter path (F-9)

Date: 2026-09-30. Agent: Claude Code. Pinned ModernUO `7c9215d97`. Brief: `D:\UO\cc-prompts\cc-P15-guild-starter-path.md`.
Spec: `docs/feature-queue.md` F-9. Built in `D:\ShatteredLegacy`, **not committed** (Chase runs `Commit-ShardWork.ps1`).
No world was changed: nothing placed, moved or removed, no shard deployed, restarted or recreated. `sl-modernuo:latest`
was not moved. Image: `sl-modernuo:cc-p15-guilds` (section 9).

**Gate before starting.** P13's four files (grove tracking) are in `d0a1782` ("Shard work, 2026-09-30 10:02"), and
`git --no-optional-locks status` in `D:\ShatteredLegacy` was clean, so this task did not build on uncommitted work.

> **Headlines**
>
> 1. **Built, all green, every new fact watched red first.** 278 shard tests pass (13 new). Three deliberate red runs,
>    each break aimed at one fact, restored byte-identical by hash (section 8).
> 2. **None of the three stop conditions held** (section 1). One thing the overseer should look at anyway: our own
>    achievements count done New Haven quests at login (`ClusterFAchievements.cs:1018-1029`), so **a starter item taken
>    from a guild counts toward `legacy.new_haven_1` and `_10`**, once, exactly as turning the quest in does. That is the
>    one ledger doing what F-9 asks, not a side effect of `SetDoneQuest` (which only records). Say if it should not count.
> 3. **Two F-9 premises did not hold.** Pinned **does** have a mystic spellbook (`MysticSpellbook`); and by pinned's race
>    rules **a gargoyle can use all 26 starter items and every creation-kit item**, human robes and cloaks included
>    (section 1.8). The list of items that would need a gargish equivalent on OSI's rules is in section 6, as asked.
> 4. **No existing seeder was safe to extend.** Both run on every world load on live and test, so a new entry would have
>    placed NPCs on live at its next start. The new placements are in a new seeder that runs only when Chase runs it
>    (section 4.4). The New Haven Artificers' Guildmaster left the institution seeder for the same reason.
> 5. **Found, not fixed (world state is Chase's):** 18 of the New Haven seeder's NPCs stand inside floors, tables or
>    walls, or on no surface (Norton and Jacob Waltz, like the Artificers' Guildmaster). Section 10.1.
> 6. **Found and fixed:** the League Registrar's "Find the Miners' Compact Liaison" arrow has never shown (section 10.2);
>    the Smiths' join consumed 10 ingots from anyone carrying them (section 4.2).

---

## 1. Part A: facts first

### 1.1 `SetDoneQuest`, and are the 26 `OneTimeOnly`

- **All 26 are `OneTimeOnly`.** Counted: 26 lines `OneTimeOnly = true` in pinned `Engines/ML Quests/Definitions/
  NewHavenSkillTraining.cs`, at :15, 38, 62, 86, 109, 133, 157, 181, 205, 229, 252, 276, 300, 323, 347, 371, 395, 419,
  442, 465, 488, 512, 535, 578, 602, 626, one per quest class.
- **`SetDoneQuest` only records.** `MLQuestContext.cs:151-168`: finds the quest's `MLDoneQuestInfo` and sets its
  `NextAvailable`, or appends one. No reward, no event, no objective call, no achievement. The done-record is saved only
  when `RecordCompletion` is true (`MLQuest.cs:71`, read back at `MLQuestContext.cs:298`), which `OneTimeOnly` makes true.
  Pinned calls it from outside the quest system itself at `Heritage.cs:424`.
- **What reads the record.** Stock: `MLQuest.CanOffer` refuses a done `OneTimeOnly` quest with 1075454 "I cannot offer
  you the quest again" (`MLQuest.cs:138-150`). Ours: the board's row state (`NewHavenQuestBoard.cs`, `GetRowState`) and
  **our achievements**: at login `ClusterFAchievements.cs:1018-1029` counts done quests over `AchievementsGump.NewHavenQuests`
  and grants `legacy.new_haven_1` (1), `legacy.new_haven_10` (10), `legacy.new_haven_all` (38); `:1840` shows each as done.
  So a guild item counts once toward those, as the quest would. Not a double count (the record is a set).
- **One thing `SetDoneQuest` does not do:** end a quest the character is carrying. `ClaimRewards` never checks
  `HasDoneQuest` (`MLQuestEntry.cs:354-443`), so a held instance would still pay after the guild marked it done. Taking an
  item therefore cancels a held instance first (`MLQuestInstance.Cancel`, `MLQuestEntry.cs:450-467`, which also ends the
  skill-gain acceleration through the objective's `OnQuestCancelled`). Fact 3 covers it.

**Stop condition 1 does not hold.**

### 1.2 What `TheAllureOfDarkMagic`'s `InternalReward` gives; blessed and insured

- `NewHavenSkillTraining.cs:552-570`: a private `ItemReward` of `NecromancerSpellbook` whose `CreateItem` sets
  `book.Content = (1ul << book.BookCount) - 1`. `BookCount` is 17 under SE (`NecromancerSpellbook.cs:14`), so content
  0x1FFFF. The fact read it back from a guild-made book: 17 spells (red run 1 printed `content 0x0` when broken).
- **No private code is copied.** Every reward is made through the quest's own public `BaseReward.AddRewardItems`
  (`ItemReward.cs:68-103`, `BaseReward.cs:20`), exactly as `ClaimRewards` does (`MLQuestEntry.cs:361-393`). The private
  `InternalReward` runs itself. **Stop condition 2 does not hold.**
- **Blessed: 24 of 26.** 23 of the 25 files in pinned `Items/New Haven Quest Rewards/` set `LootType.Blessed`; the two that
  do not are `BagOfNecromancerReagents` and `BagOfSmokeBombs` (bags of consumables). Our replacements are blessed too
  (`server/patches/JacobsPickaxe.cs:38`, `server/customizations/HammerOfHephaestus.cs:124`), and so is the spellbook
  (`Spellbook.cs:122`). **None is insured by default** (no `Insured` in that folder). So replacements should be rare:
  a blessed item survives death, and only trading, dropping or destroying loses one.

### 1.3 Which guildmasters the test world has in New Haven

Read **offline from a copy** of `Saves-test` (the 10:05 autosave; the running test shard was not touched), by decoding
`Mobiles.idx`/`.bin` against `SerializedTypes.db` (tool in `notes/cc-P15-tools/`). Box x 3400-3560, y 2400-2760, Trammel.

| Type | Where (test world) | Source |
|---|---|---|
| MageGuildmaster | 3496,2527,27 (the magic shop beside the inn, **not** the Magery School) | pinned spawn 3495,2527,27 |
| HealerGuildmaster | 3466,2559,35 | pinned spawn 3463,2558,36 |
| TailorGuildmaster | 3496,2551,20 | pinned spawn 3494,2551,20 |
| TinkerGuildmaster | 3459,2523,53 | pinned spawn 3458,2524,53 |
| BlacksmithGuildmaster | 3467,2536,41 (**one**) | pinned spawn 3469,2536,41 |
| ArtificersGuildmaster | 3490,2627,0 (in the water) | our institution seeder |
| OutridersGuildmaster, ForestersGuildmaster, MinersCompactLiaison, SanitationWarden | their seeded tiles | our institution seeder |

**Not there:** Warrior, Thief, Bard, Fisher, Merchant, Miner guildmasters, and **the second Blacksmith guildmaster**,
which pinned spawns in the Warrior's Guild Hall at 3526,2536,20 (`Distribution/Data/Spawns/post-uoml/trammel/Vendors.json`;
the same point also spawns an `IronWorker` and a `Miner`). The test world has the Miner there (3526,2535) and neither of
the other two. Why was not checked. **The live world was not read** (the brief allowed the test shard only), so PT-01
stands for live.

### 1.4 Mining: `MinerGuildmaster` versus `MinersCompactLiaison`

Resolved as **one NPC type per guild location**: the Miners' Compact's New Haven location names `MinersCompactLiaison`
(`GuildLocations`, `ClusterFGuildStarterPath.cs`), and the directory's arrow points at it. The `GuildDef` keeps
`MinerGuildmaster` as its type, so stock miner guildmasters in other towns still offer "Talk" into the Compact. The
registry now also maps every location's NPC type to its guild (the Liaison to mining). No New Haven `MinerGuildmaster`
exists (1.3), so the two cannot be confused there.

### 1.5 The Blacksmith guildmaster in the Warrior's Guild Hall

Pinned's spawner stays as it is (never edited). **The Warriors' Guildmaster stands at 3530,2537,20**, the middle of the
hall's courtyard, 4 tiles from that spawn point, whose walking range is 2. The directory's Smiths' Fellowship row points
at the **Forge and Anvil** spawn (3469,2536,41), where George Hephaestus trains. A Blacksmith guildmaster that does spawn
in the Warrior's hall still offers the Smiths' "Talk"; it is just not a directory row.

### 1.6 The reset (F-7)

`ClusterFDevTools.ExecuteReset`'s Account Data cleared Renown, rep, currency and the restoration registry only
(`ClusterFDevTools.cs:95-102` at `d0a1782`). **Fixed here**: it now also clears `JoinedGuilds`, the Apprentice marks, and
every character's guild starter record. Work orders, discoveries, commissions and encountered creatures are still not
cleared: F-7's own decision, not this task's. The starter item's other half is the quest's done-record, which is
**Quest History**, a separate checkbox (it clears the one character the reset names). Fact 9 shows both halves.

### 1.7 Every `AddSkillItems` case lands in one guild

Counted: 48 `case SkillName.` labels in `AddSkillItems`; the other 10 skills have none (Eval Int, Focus, Forensics,
Imbuing, Resist, Meditation, Remove Trap, Spellweaving, Stealth, Taste ID), and Mysticism's case is empty. 48 + 10 = 58,
all of pinned's `SkillName` (`Server/Skills.cs`, counted 58). Fact 5 asserts every `SkillName` is in exactly one guild,
so every case is too.

### 1.8 Gargoyles

- **Where our creation places a gargoyle: New Haven.** `ConstructAvailableStartingCities` offers only New Haven
  (`CharacterCreation.cs:129-136`), and under SA `GetStartLocation` returns the city the client chose from that list
  (`:298-301`). `StartingCitiesSA` (Royal City, `:119-122`) exists but is never offered. Confirmed by reading, not in a client.
- **The kits are race-aware** (`Robe(raceFlag)`, `SwordsWeapon(raceFlag)` and so on, `CharacterCreation.cs:872-914`, and
  the `raceFlag` switches in `AddSkillItems`). Fact 6 printed each guild's gargoyle kit (red run 1; section 6).
- **Stop condition 3 does not hold by pinned's rules.** Pinned gates by race in two places only: `Item.CheckRace`
  (`RequiredRaces`, `Item.cs:2110-2148`, used by `BaseWeapon.cs:1044`, `BaseArmor.cs:1095` and `PlayerMobile.cs:1374,1399`)
  and `BaseClothing.RequiredRace` (`BaseClothing.cs:178, 442`). No item a kit hands a gargoyle sets either against
  gargoyles. **But the creation path hands gargoyles human robes** (Alchemy, Anatomy, Animal Lore, Magery: `Robe()`
  falls to the default branch, `CharacterCreation.cs:872-878`) **and a cloak** (Spirit Speak, `:1257` before this task's
  edits). Pinned lets a gargoyle wear both; OSI does not, as far as I know (not verifiable in pinned). That is the
  creation path's existing behaviour, which the guild tools now repeat. Chase's call whether it matters.
- **Mysticism:** pinned **has** `MysticSpellbook` (`Items/Skill Items/Magical/MysticSpellbook.cs:6`, 16 spells, `:14`),
  so F-9's "no mystic spellbook type was found" is wrong. But pinned registers only 10 of the 16 Mysticism spells, **none
  of circles 1 and 2** (`Spells/Initializer.cs:183-199`: Nether Bolt, Healing Stone, Purge Magic, Enchant, Sleep, Spell
  Trigger, Mass Sleep and Rising Colossus commented out). The creation line pinned left commented, `MysticBook(0xAB)`,
  would hold spells 0, 1, 3, 5 and 7, three of them unregistered. **No mystic reagent bag exists** (pinned has
  `BagOfReagents`, `BagOfNecroReagents`, `BagOfAllReagents`, `BagOfNecromancerReagents`). **Not added**: a starter book
  whose first spells cannot be cast is a design choice. Options for Chase: a book of the registered spells only (Eagle
  Strike, Animated Weapon, Stone Form are circles 3-4), or nothing until pinned implements the low circles.

---

## 2. Placements for a fresh world

Picked by reading the client map (`client-data/classic-client`: `map1LegacyMUL.uop`, `statics1.mul`, `tiledata.mul`),
rendered with the mine-camp renderer and a height cut to see each floor, and **checked standable with a port of pinned
`Map.CanFit`** (`Projects/Server/Maps/Map.cs:925-1010`, with `GetAverageZ` `:243-285`, height 16) over the map, the statics
and pinned's New Haven decoration items. **The checker was validated against the test world first**: of 360 NPCs in New
Haven, all **341 that spawned or walked there fit**; the 19 that do not are all seeded (section 10.1). Each chosen tile
fits at its z and is not another NPC's tile. Tools: `notes/cc-P15-tools/`.

| Guild | NPC type | Tile (Trammel) | Hall | `[go` |
|---|---|---|---|---|
| Warriors' Brotherhood | `WarriorGuildmaster` (stock) | 3530,2537,20 | Warrior's Guild Hall, courtyard | `[go 3530 2537 20` |
| Arcane Society | `MageGuildmaster` (stock) | 3486,2494,52 | Magery School, main room (carpet floor z52) | `[go 3486 2494 52` |
| Thieves' Den | `ThiefGuildmaster` (stock) | 3495,2515,27 | Bountiful Harvest Inn, stone storeroom at the back | `[go 3495 2515 27` |
| Twin Paths Dojo | `TwinPathsDojoGuildmaster` (new) | 3420,2517,21 | Ninja Dojo | `[go 3420 2517 21` |
| Keepers of the Last Door | `KeepersOfTheLastDoorGuildmaster` (new) | 3551,2463,15 | Necromancers Guild Hall | `[go 3551 2463 15` |
| Maritime Brotherhood | `FisherGuildmaster` (stock) | 3507,2597,1 | New Haven docks, main pier | `[go 3507 2597 1` |
| Merchants' Exchange | `MerchantGuildmaster` (stock) | 3488,2567,20 | New Haven Bank | `[go 3488 2567 20` |
| Bards' Consortium | `BardGuildmaster` (stock) | 3410,2608,55 | Bardic Guild, tiled side room | `[go 3410 2608 55` |
| Artificers' Order (moved) | `ArtificersGuildmaster` | 3483,2501,52 | Magery School, entrance hall | `[go 3483 2501 52` |

- **Merchants: there is no provisioner in New Haven**, so the bank (the fallback) it is. Pinned spawns none; pinned's
  `Merchant` at 3481,2534 is an escortable townsperson (`Mobiles/Townfolk/Merchant.cs:7`, `: BaseEscortable`), not a shop;
  the map has no shop-sign statics in New Haven and pinned's New Haven decoration names no shops.
- **Thieves' Den:** "the back room" read as the inn's stone storeroom (barrels and shelves, 3493-3497, 2512-2519, z27).
  F-9's open question mentions "the fighting pit"; I found no pit in or by the inn. Say if the pit is somewhere else.
- **Arcane Society** was not in the brief's placement list, but F-9 Decision 1 puts it in the Magery School with its
  trainers, and pinned's only New Haven `MageGuildmaster` stands in the magic shop by the inn. So one is seeded in the
  Magery School; the spawned one keeps working.
- **Unchanged, found where they are** (directory rows only): Healers (spawn 3463,2558,36), Tinkers (3458,2524,53),
  Tailors (3494,2551,20), Smiths (3469,2536,41) from pinned's vendor spawns; Outriders (3524,2574,7, stays at the stables),
  Foresters (3441,2637,28), Miners' Compact Liaison (3510,2748,0), Sanitation Warden (3506,2560,21) and the Ter Mur
  Artificers (797,3431,-10) from our institution seeder.

---

## 3. Part B, what was built

### 3.1 Membership and joining (F-9 Decision 3)

Joining is free, one click, at a guildmaster, rank Initiate; `CanJoin` refuses only an account already in the guild.
Joining pays no reputation or scrip. The old skill-or-tribute task is the **Apprentice task**: at the guildmaster, a
member who meets it completes it, which pays the old join reputation and scrip (25 and 10; 5 scrip for the Custodians),
takes the tribute only if the skill half is not met (as the old join did), and raises the shown rank to the ladder's
second rank (Apprentice on the generic ladder; each custom ladder's own name, found by asking the ladder). Nothing is
consumed to join. The hall page says in one line, where the guildmaster is a stock guildmaster: "Separate from the stock
trade guild (say "join", 500 gold). One does not join the other." `BaseGuildmaster.OnGoldGiven` is untouched.

### 3.2 Two new guilds

- `dojo`, **Twin Paths Dojo**: "Bushido and Ninjitsu, taught side by side in the Ninja Dojo. Pick the path that suits you,
  or walk both." Apprentice task: Bushido 30.
- `keepers`, **Keepers of the Last Door**: "Necromancy, Spirit Speak and Forensics, taught in the old Necromancers Guild
  Hall. Dark work, done carefully." Apprentice task: Necromancy 30 or 10 Grave Dust.
- Generic rank ladder for both. Their guildmasters are new NPCs (`ClusterFStarterGuildmasters.cs`), since no stock
  guildmaster type fits. The pitches are mine, written plain, second person, after the website's voice; rewrite freely.

### 3.3 Skills per guild

F-9's table, one line per guild, in `GuildSkillTable` (`ClusterFGuildStarterPath.cs`). Fact 5 asserts every `SkillName`
(58, counted) is in exactly one guild, the table's guilds are the 17 registered, and each of the 26 starter items belongs
to exactly one guild that teaches its quest's skill.

### 3.4 Tools on joining

`CharacterCreation.GiveSkillItems(m, skill)` (new, public) calls the existing private `AddSkillItems` and returns what it
made; `AddSkillItems` is not copied. While a guild call runs, **nothing worn is deleted**: creation deletes worn pants
(Bushido, Ninjitsu) and shoes (Tracking), which at a join would destroy a player's own gear, so those three lines are
skipped and the new item goes to the pack. **No item type twice in one kit** is applied across skills; within one skill
the creation list is kept as it is (Cartography's four blank maps, Blacksmithing's two pickaxes). So the Warriors' kit
has one sword for Tactics and Swords. The existing join bonuses (satchels, logbooks, crook, bag) are handed with the
tools, per character. Instruments are four random types, so the Bards' kit can carry up to four instruments, as picking
those skills at creation would.

### 3.5 Starter items on request

At the guildmaster, **Starter items** lists the guild's quest rewards; one click takes one, once per loop per character
(a loop is a character). Taking one calls `SetDoneQuest` (and closes a held copy of the quest, 1.1); a quest done first
shows "Received from the trainer". The Necromancer spellbook is complete (fact 4). Jacob's Pickaxe and the Hammer of
Hephaestus come through their normal creation (their `OnAdded` runs: the pickaxe unlocks `legacy.jacobs_pickaxe`) and
show their own rule instead of a replacement ("the Liaison issues a new one", "the Smiths' Fellowship recharges it").
**Replacement for everything else: `ClusterFGuildStarter.ReplacementScrip = 10`** of that guild's scrip, only for a
character that has had the item and no longer owns one (worn, pack or bank). 10 because that is what the Apprentice task
pays, so every member can reach one replacement; the generic guilds have no other scrip source yet.

### 3.6 The per-character record (PT-06)

`GuildStarterRecord`, per character serial in `ClusterFAccountData`, **version 14**, following `_exploredChunks`: guild
keys whose tools were taken, quest names whose items were taken, and whether the welcome was shown. It carries its own
version (0) and fails loudly on another. Membership stays per account. A second character on a member account gets
"Welcome back" and its own tools, join bonus and items (fact 2). **Chosen:** the exploration pattern, as the brief
suggested; I found no reason not to.

### 3.7 The board's Guild Directory

The board is the same item at the same spot. Its double-click now opens the **Guild Directory**; the 26-quest picker is
its "Training quests" tab and is unchanged (its facts still pass through the tab). One row per guild **and per
guildmaster location** (18 rows: the Artificers have New Haven and Ter Mur): guild, hall, skills taught, Show me the
way, rank where joined, and Services and Contracts for members. A guildmaster that is not where the row says shows
"Guildmaster missing", and its arrow says "... is not at <hall> (x, y, map). Please tell a Game Master." `[guild` opens
the same gump (the old overview class `GuildProgressGump` now draws the directory, so every old caller gets it too), and
the League Registrar's Guild Referrals open it. The arrow is `GuildDirectionArrow`, generalizing
`MinersCompactDirectionArrow` (removed; 10.2). It follows a wandering guildmaster, stops on arrival or after ten minutes,
and right-click dismisses it.

**Changed from before:** `[guild` no longer lets a non-member open a guild's join screen remotely. F-9 says joining
happens at the guildmaster.

### 3.8 First-login welcome

Once per character, at login: one page ("Every skill has a guild in New Haven. Joining one is free ... The Guild Board in
the town square lists every guild ...") with **Show me the Guild Board**, which sets the arrow. The board is chosen per
starting town through `GuildWelcome.StartingBoardFor`, one row today (New Haven). **Existing characters see it once too**
on their next login; nothing tells an old character from a new one reliably.

### 3.9 Trainer lines

Each of the 26 trainers adds one line after its stock double-click, naming the guild whose hall it stands in. Where that
guild does not hand out the trainer's own item, the line also names the guild that does, e.g. Chiyo: "This Ninja Dojo
belongs to the Twin Paths Dojo. What I give, the Thieves' Den gives too." **This goes a step past the brief** (which
asks only for the hall's guild), because five trainers stand in a hall whose guild does not give their item (Robyn,
Chiyo, Jun, Walker, Sarsmea Smythe). No pinned file is patched: every trainer class is `partial` and none overrides
`OnDoubleClick`, so each gets a partial part (`NewHavenTrainerGuildLines.cs`) that calls the stock path first.

### 3.10 Placing them: a new seeder, run by Chase

`ClusterFGuildHallSeeder` places the rows marked Seeded. It runs at world load **only** if
`clusterf.guildHallSeeder.seedOnWorldLoad` is true (default false; the server writes the default into `modernuo.json`
on first start); otherwise by `[ClusterFSeedGuildHalls [dryrun|missing|repair]` (Administrator). A guildmaster of the
right type within 15 tiles of its tile, or of an old tile, counts as present, so re-running never duplicates; `repair`
also moves one standing elsewhere onto its tile. The New Haven Artificers' Guildmaster's old tile (3490,2627,0) is listed,
so `repair` moves it rather than placing a second.

**Why not the existing seeders:** `ClusterFInstitutionSeeder` seeds on every world load (`OnWorldLoad` -> `Seed`), and
`ClusterFNewHavenSeeder` does too with `clusterf.newHavenSeeder.seedOnWorldLoad`, which **both** `Configuration` and
`Configuration-test` set `True`. An entry added to either would have placed guildmasters on live at its next start, and
changing the Artificers' tile there would have placed a second one beside the Magery School (the old one is more than 15
tiles away, the institution seeder's own duplicate check). So that entry was removed from the institution seeder; the
Ter Mur one stays.

---

## 4. File by file

All in `D:\ShatteredLegacy`. ASCII only in every file touched: the eight existing files that carried non-ASCII had it
converted (U+2014 em dash and U+2500 box line to `-`, U+2192 to `->`, U+2022 to `*`; 2,754 characters, nearly all in
comment rules). That touches a few player-visible strings' punctuation (the dev reset's bullets, some Smiths' text).

### 4.1 New

| File | What |
|---|---|
| `server/customizations/ClusterFGuildStarterPath.cs` | `GuildSkillTable`, `GuildStarterItems`, `GuildLocation(s)`, `ClusterFGuildStarter` (tools, starter items, replacement, trainer line, Show me the way), `GuildDirectionArrow`, `GuildWelcome` and its gump, `GuildStarterItemsGump` |
| `server/customizations/ClusterFStarterGuildmasters.cs` | `StarterGuildmasterBase`, `TwinPathsDojoGuildmaster`, `KeepersOfTheLastDoorGuildmaster` (new serialized types; no instance exists anywhere) |
| `server/customizations/ClusterFGuildHallSeeder.cs` | the seeder and `[ClusterFSeedGuildHalls` |
| `server/customizations/Engines/ML Quests/Definitions/NewHavenTrainerGuildLines.cs` | 26 partial parts, one per trainer |
| `server/tests/Misc/GuildStarterPathVerification.cs` | 11 facts |

### 4.2 Changed

| File | What |
|---|---|
| `ClusterFAccountData.cs` | v14: per-character `GuildStarterRecord`s; `GuildStarterRecord` class; the reader refuses a version newer than it knows |
| `CharacterCreation.cs` (a replacement file) | `GiveSkillItems` (public, records what the kit made); the three worn-item deletions skipped during a guild call |
| `ClusterFGuildSystem.cs` | free join, `MeetsApprenticeTask` / `CompleteApprenticeTask`, the two guilds, `Join` hands per-character tools, `GiveJoinBonus` (the old join blocks, three messages no longer mention scrip), `EnsureRegistered`, `OpenGuildHall`, rank with Apprentice; `GuildProgressGump` is the directory; `GuildTaskDetailGump` is the hall page; `[ResetGuild` also clears the Apprentice mark and the caller's tools record |
| `SmithGuildmasterGump.cs` | **join no longer consumes 10 iron ingots** from a player carrying them (`HandleJoin`, the tribute block); join text says joining is free |
| `ClusterFDevTools.cs` | Account Data also clears `JoinedGuilds`, Apprentice marks, every character's starter record; its labels say so |
| `ClusterFInstitutionSeeder.cs` | the New Haven Artificers' entry removed (3.10) |
| `OutridersGuildmaster.cs`, `ForestersGuildmaster.cs`, `MinersCompactLiaison.cs` | double-click and Talk open the hall page; keyword speech still opens their own gumps; the hall page's Services opens them |
| `Engines/ML Quests/Items/NewHavenQuestBoard.cs` | double-click opens the directory; `OpenTrainingQuests` for its tab; property line 4 reworded. Save shape unchanged (its fact passes) |
| `LeagueRegistrarGump.cs` | Guild Referrals open the directory; "Where to go first" points at the board; `MinersCompactDirectionArrow` removed |
| `server/tests/Misc/AccountDataSerializerVerification.cs` | v14 records in the round trip; 2 new facts (8) |
| `server/tests/Engines/MLQuests/NewHavenQuestBoardVerification.cs` | `OpenMenu` goes through the directory's tab, pressed through the gump system |

`server/patches/` untouched. No pinned file needed to change.

---

## 5. D-92 (for the overseer to promote; `docs/` not edited)

P14 section 5's draft with F-9's answers filled in. Same columns as `docs/fidelity-principle.md`. Confirm the number is
still free when promoting; the quest-done half could be its own D-n if you prefer, since F-9 asks for it separately.

| # | What | Player-visible effect | Class | Source |
|---|---|---|---|---|
| D-92 | **The New Haven training quests' item rewards are also handed out by NPC guilds, and taking one counts the quest as done.** The 26 quests are stock ML (`NewHavenSkillTraining.cs`, pinned), each a `GainSkillObjective` to 50 with one `ItemReward` on completion and a 15-minute skill-gain acceleration on accept. On this shard gain runs at roughly 15x stock (`clusterf.skillGain.chanceAttempts` 3, `amountMultiplier` 5), so the skill half is overshot before it registers and the quest reduces to an item hand-out. Ten guilds hand out the 26 items between them (F-9 Decision 1), free, **once per loop per character** (a loop is a character until loops exist), on request at the guildmaster. Taking one marks the quest done for that character (`MLQuestContext.SetDoneQuest`) and closes a held copy, so each item is paid once by either route, and our New Haven quest achievements count it. The quests stay offered, at the trainers and on the board's Training quests tab. The guild route gives no acceleration buff. A lost item is replaced for 10 guild scrip, except Jacob's Pickaxe and the Hammer of Hephaestus, which keep their own reissue and recharge. | a player gets Recaro's Riposte, Jacob's Pickaxe and the other 24 by joining the matching guild and asking its guildmaster, rather than by reporting to the trainer, and the trainer then says "I cannot offer you the quest again". A wiki says "complete the trainer's quest"; here either way works, once. The items themselves are unchanged. | `ours` | `cc-P14-newhaven-guild-mapping` + `cc-P15-guild-starter-path` |

**Relation to D-90** (as P14 said): both rest on our gain rate; D-90's "reverses when" (stock gain rates) applies here.
The guild join itself (free, per character tools) is ours throughout and not a deviation from any stock system; the
stock NPC guild (`BaseGuildmaster`, 500 gold) is unchanged.

---

## 6. Gargoyles: kits, and the items that would need a gargish equivalent

**Kits, by pinned's rules all usable by a gargoyle (fact 6).** As printed by red run 1 (its extra `LeafGloves` was the
break, and its Warriors' line lacks Throwing's Boomerang because that run's other break removed Throwing):

| Guild | Gargoyle kit (plus join bonus) |
|---|---|
| warriors | DreadSword, DiscMace, BloodBlade, GargishLeatherArmsType1, GargishWoodenShield, BookOfChivalry, Boomerang |
| arcane | BagOfReagents, 3 scrolls, Spellbook, **Robe**, BlankScroll, BlueBook |
| healers | Bandage, Scissors, **Robe**, Bottle, MortarPestle |
| rangers | Arrow, SerpentstoneStaff, SkinningKnife, ShepherdsCrook, **Robe**, Bandage, Scissors, Bedroll, Kindling |
| keepers | BagOfNecroReagents, **Cloak** |
| smithing | Tongs, 2 Pickaxes, IronIngot, **HalfApron**, DreadSword (Arms Lore's weapon is random) |
| dojo | BookOfBushido, BookOfNinjitsu (the hakama and kasa are for humans and elves only) |
| foresters | DualShortAxes, Board, Saw, Feather, Shaft |
| maritime | FishingPole, 4 BlankMaps, Sextant, cooking goods |
| merchants | SerpentstoneStaff, GlassStaff |
| bards | three or four instruments |
| thieves | Lockpick, 2 LesserPoisonPotions |
| mining, tinkers, tailoring | Pickaxe; TinkerTools; BoltOfCloth, SewingKit |
| artificers, custodians | nothing from creation; their join bonus only |

In bold, human wear pinned lets a gargoyle wear (1.8).

**The 26 starter items: a gargoyle can use all 26 by pinned's rules** (fact 6 asserts none fails `CheckRace` /
`RequiredRace`). **On OSI's rules** (gargoyles wear only gargish armour, clothing and jewellery, and cannot use bows;
pinned itself refuses Archery to a gargoyle at creation, `CharacterCreation.cs:431`), these 19 would need a gargish
equivalent, read off each item's pinned base class in `Items/New Haven Quest Rewards/`:

- Armour and clothing (8): Bulwark Leggings (RingmailLegs), Gloves of Safeguarding (LeatherGloves), Arms of Armstrong
  (LeatherArms), Tunic of Guarding (LeatherChest), Healer's Touch (LeatherGloves), Twilight Jacket (LeatherNinjaJacket),
  Walker's Leggings (LeatherNinjaPants), Philosopher's Hat (WizardsHat).
- Shield (1): Escutcheon de Ariadne (MetalKiteShield).
- Jewellery (3): Bracelet of Resilience (GoldBracelet), Ring of the Savant (GoldRing), Clasp of Concentration
  (SilverBracelet).
- Weapons (7): Churchill's War Mace (WarMace), Recaro's Riposte (WarFork), Jockles' Quicksword (Longsword), Ember Staff
  (QuarterStaff), Silver Serpent Blade (Kryss), The Dragon's Tail (NoDachi), **Heartseeker (CompositeBow: a gargoyle
  cannot take Archery at all)**.

Not needing one (7): Hallowed Spellbook, the Necromancer spellbook, Bag of Smoke Bombs, Bag of Necromancer Reagents,
Amelia's Toolbox, Hammer of Hephaestus, Jacob's Pickaxe (tools, books, consumables). None were invented (as the brief says).

---

## 7. Facts

Numbered as the brief. All in `server/tests/Misc/GuildStarterPathVerification.cs` except 8.

| # | Fact | What it pins |
|---|---|---|
| 1 | `AFreshCharacterWithNoSkillAndNoGoldJoinsAndGetsItsToolsOnce` | no skill, no gold, carrying the old 25-bandage tribute: joins the Healers, gets Healing/Anatomy/Alchemy's kit with no type twice, keeps the tribute; a second join or tools request gives nothing |
| 2 | `ASecondCharacterOnTheSameAccountGetsItsOwnToolsAndItems` | PT-06: the second character is refused "Already a member.", then gets pickaxe, satchel, logbook, ledger and Jacob's Pickaxe; the first cannot take a second |
| 3 | `AnItemTakenFromTheGuildMarksItsQuestDoneAndTheReverse` | a held EnGuarde is closed, done, `CanOffer` false, a second take refused; a quest done first shows as received and pays nothing |
| 4 | `TheNecromancerSpellbookFromTheGuildHasEverySpell` | content `(1 << 17) - 1` |
| 5 | `EverySkillIsInExactlyOneGuild` | 58 skills, 17 guilds; 26 items, each in one guild that teaches its skill |
| 6 | `JoiningEachGuildAsAGargoyleHandsOverOnlyItemsAGargoyleCanUse` | all 17 kits; the 26 items listed as data |
| 7 | `TheDirectoryArrowResolvesToAGuildmasterThatExistsAndAMissingOneReportsIt` | every guild has a location and every location resolves to its guild; arrow on a present one, "is not at" on a missing one, no arrow across facets |
| 8 | `AccountDataSerializerVerification`: `AnAccountWithEveryCollectionNonEmptySurvivesAWriteAndARead` (now with two records), `AVersion13SaveFromTheBuildBeforeGuildStarterRecordsLoads`, `AnAccountRecordOrStarterRecordOfAnUnknownVersionFailsLoudly` | v14 round trip every field; v13 bytes from a **frozen copy of the d0a1782 writer** load whole and re-save as v14; unknown versions throw |
| 9 | `TheDevResetClearsJoinedGuildsAndEveryCharactersStarterRecord` | Account Data clears membership, both characters' records and the Apprentice mark, leaves `league.joined`; Quest History frees the item |
| + | `AGuildKitNeverDeletesWhatIsWorn`, `TheOldJoinTaskIsTheApprenticeTask`, `EveryTrainerNamesTheGuildWhoseHallItStandsIn` | worn pants and boots survive the Dojo and Rangers kits; Stealing 20 pays 25/10 and Apprentice once; every trainer's line names its hall's guild, Chiyo's also the Thieves' Den |

**Why a frozen writer for the v13 fact:** the real v13 blob in the test save is 912 KB (almost all exploration bits), too
big for a fixture, and bytes produced by the new writer would not prove anything about the old format. The copy is the
`Serialize` body at `d0a1782`, entry writers unchanged.

---

## 8. Red and green runs

All through `docker/uo/build.sh --tests-only`, except the last (full build, tagged). Breaks were applied by script to
copies' originals and restored from a saved copy each time; `sha256sum -c` confirmed all five files byte-identical
before each next step, and a grep found no `BREAK` marker left anywhere under `server/`.

| Run | Breaks (one line each) | Result |
|---|---|---|
| build 1 | none | test project did not compile (two errors in the new facts: a struct enumerator, a `params Item[]`); fixed |
| build 2 | none | **278 passed**, 0 failed |
| red 1 | a: tools never recorded; c: guild-made spellbooks emptied; d: reset keeps `JoinedGuilds`; e: Throwing dropped from the Warriors; f: an elf-only `LeafGloves` added to every gargoyle kit; g: `GuildLocation.Find` ignores type; k: account reader accepts any newer version; l: the Bushido pants guard removed; m: the Apprentice task pays no scrip; n: trainers never name the item's guild | **268 passed, 10 failed, exactly the 10 targets**: fact 1 ("Not found: healers" in ToolsTaken), 4 (content 131071 expected, 0), 9 (`["warriors","tinkers"]` not empty), 5 ("in no guild: Throwing"), 6 (LeafGloves in 17 kits), 7 ("Follow the arrow" where "is not at" was expected), unknown-version ("No exception was thrown"), never-deletes (pants deleted), Apprentice (scrip 10 expected, 0), trainer line (Chiyo's line without "Thieves' Den") |
| red 2 | h: every character's record keyed to one serial (per account, as before); j: v14 block read for version 13 | 274 passed, 4 failed: **fact 2** (second character's Jacob's Pickaxe: 1 expected, 0), **v13 load** (read 1127 bytes of 1123); facts 3 and 9 also fell to h (a shared record), expected, and have their own red runs |
| red 3 | b: `SetDoneQuest` removed from taking an item; i: the v14 block not written | 274 passed, 4 failed: **fact 3** (`HasDoneQuest` false), **round trip** (read 1127 of 1123); fact 9 fell to b and the v13 fact's re-save to i, expected |
| final | none, restored and hash-checked | section 9 |

So every new fact has been seen failing on a break of its own: 1, 4, 5, 6, 7, 9 and the three extras in red 1; 2 and
the v13 load in red 2; 3 and the round trip in red 3; unknown-version in red 1.

---

## 9. The image

`docker/uo/build.sh -t sl-modernuo:cc-p15-guilds` (full: builder, tests, runtime image), on the restored green tree:
**278 passed, 0 failed**, "Built sl-modernuo:cc-p15-guilds with patches applied and 278 shard test(s) passing."

- `sl-modernuo:cc-p15-guilds` = `f63d9e26e611`, created 2026-09-30 15:54:33Z.
- `sl-modernuo:latest` = `16b0f49e6828` (12:32:54Z), the same ID as at the start of the task: **not moved**.
- `build.sh` also retags its builder, `sl-uo-builder:latest`, every run; that is its normal behaviour.
- 278 = 13 new facts (11 in the new file, 2 in `AccountDataSerializerVerification`, counted from `[Fact]`) plus 265.
  The 265 is arithmetic, not a count from an earlier run.

---

## 10. Found in passing

### 10.1 The New Haven seeder puts NPCs inside floors (ours, not fixed: it would move live NPCs)

The checker (section 2) finds 19 New Haven NPCs on a tile they cannot stand on; every one is seeded, none spawned. 18
are `ClusterFNewHavenSeeder`'s: Alefian (z66 inside a brazier; floors there 91, 111), Gustar (z66, in blue tiles z71),
Jillian (z66, in a table), Kaelynna (z46, **inside a brick wall**; floor 91 there), Mithneral (z46, in a table), Lyle
(z46; floor 52), Andreas Vesalius and Avicenna (z30; floor 35), Asandos (z22; floor 27), Clairesse (z15; floor 20),
Nibbet (z15; floor 20), Hargrove and Lowel (z22; floor 28), Sadrah (z30, in a display case), Jun (z21, in a lantern),
Walker (z21; floor 18), **Norton (z-5, in the water at the docks)** and **Jacob Waltz (z0, no surface)**. The 19th is the
Artificers' Guildmaster (institution seeder, water). **Cause, by reading:** a `SeedEntry` without a z takes
`Map.GetAverageZ` (`ClusterFNewHavenSeeder.cs:268-272`), which is the land height and ignores building floors; Jacob
Waltz's explicit z 0 is simply wrong. They are `CantWalk`, so they stay sunk. **Not fixed:** correcting the z's would make
`repairOnWorldLoad` (true on both shards) move every one of them on live at its next start. Chase's call; the right z for
each is in `notes/cc-P15-tools` (`surfaces(x, y)`).

### 10.2 The Registrar's arrow never showed (ours, fixed by replacement)

`MinersCompactDirectionArrow` was built with `QuestArrow(m, t)`, which sets fields and sends nothing
(`QuestArrow.cs:8-13`; only the four-argument constructor calls `Update`), and it was never assigned to the player's
`QuestArrow`, so neither the client nor a right-click could reach it. `GuildDirectionArrow` uses the four-argument
constructor and is assigned; fact 7 checks it is the player's running arrow.

### 10.3 Smaller

- The spawned `MageGuildmaster` stands in the magic shop beside the inn, not the Magery School (1.3).
- `ClusterFGuildSystem`'s doc said "all 12 guilds"; there were 15, now 17 (fixed).
- The Registrar's Guild Referrals used to record "mining" as the player's first referral guild on opening; it no longer
  does. The Outriders', Foresters', Artificers' and Liaison's own gumps still record theirs.
- The console logger `build.sh` uses does not print a passing fact's output, so data printed by facts (kits, lines) came
  from the red runs. I did not run tests outside `build.sh`.

---

## 11. Not verified

- **Nothing here was run in a client.** Gump layouts (the directory is 760 wide), the arrow, the welcome, the hall page
  and the trainer line are verified by facts and by reading only. The test host has no tiledata, so no fact saw an item
  actually worn.
- The live world's guildmasters (PT-01). The directory will say "Guildmaster missing" for any row whose NPC is absent.
- Whether the Warrior's-hall `BlacksmithGuildmaster` and `IronWorker` are missing from the test world by spawner state
  or for another reason.
- Achievement side: `TryGrant` on join (`ClusterFLeagueSystem.OnGuildJoined`) ran in the facts without error; the
  achievements' own effects were not asserted.
- OSI's gargoyle equipment rules (section 6) are from knowledge of the game, not from pinned.

---

## 12. Checklist for Chase

1. **Commit** with `D:\UO\Commit-ShardWork.ps1`. **Not mine, and not part of P15:** `git status` also shows untracked
   `design/mine-camp-tents/camp.py`, `layout.json`, `v3_clean.png`, `v3_closeup.png`, `v3_labeled.png` (10:09-10:10) and
   `design/registrar-office/` (`r_noroof.png`, `r_overview.png`, 10:55). The tree was clean when this task started, so
   something else was writing in `D:\ShatteredLegacy` while it ran (the brief says nothing should). They are renders, not
   code, and did not affect the compile. If the commit script takes everything, they go in the same commit; decide
   first. P15's own files are the 18 in section 4.
2. **Rebuild the test shard** from the console (Test tab, "Rebuild through the gates") and read the output: the test gate
   should say 278 passed. Note this build retags `sl-modernuo:latest`; `sl-modernuo:cc-p15-guilds` is this task's image.
3. **World state on the test shard first** (item 6), then **on the test shard, in order:**
   1. Make a new character. **The welcome page opens.** Press "Show me the Guild Board"; an arrow appears.
   2. Follow it to the board by Sir Helper (3502,2573). Double-click the board: **the Guild Directory**; the "Training
      quests (26)" button opens the old picker, unchanged.
   3. In the directory, "Show me the way" on the Healers' Covenant (or any row). Follow the arrow; it says "You have
      found ..." on arrival.
   4. Talk to the guildmaster. **Join the guild** with no gold and no skill. The tools arrive (Healers: 50 bandages,
      scissors, a robe, 4 bottles, a mortar).
   5. **Starter items**: take one (e.g. Healer's Touch). Then double-click its trainer (Avicenna in the Healer's Hall):
      **"I cannot offer you the quest again"**, and the trainer's hall line.
4. **Second character, same account**: go to the same guildmaster. The page says **"Welcome back"**; "Take your tools"
   gives them; Starter items gives the item again for this character.
5. **A gargoyle character**: join the Warriors' Brotherhood (Warrior's Guild Hall) and the Arcane Society (Magery
   School). Expect the gargish weapons, shield, arms and a Boomerang from the Warriors; reagents, scrolls, a spellbook and
   **a human robe** from the Arcane Society (1.8).
6. **World-state commands** (Administrator, in game, on the world you mean; test first):

   | Command | What it does | Re-run |
   |---|---|---|
   | `[ClusterFSeedGuildHalls dryrun` | lists what would be placed or moved; changes nothing | safe |
   | `[ClusterFSeedGuildHalls repair` | places the 8 missing guildmasters (Warriors, Arcane, Thieves, Dojo, Keepers, Maritime, Merchants, Bards, section 2) and **moves the New Haven Artificers' Guildmaster** from 3490,2627,0 into the Magery School (3483,2501,52) | safe: a guildmaster of the right type within 15 tiles of its tile, or of the old Artificers tile, counts as present; nothing is placed twice |
   | `[ClusterFSeedGuildHalls` (= `missing`) | places missing ones only, never moves; reports an Artificers' Guildmaster still on its old tile and leaves it | safe |

   Then `[go` to each tile in section 2 and look. A fresh world gets them from the same command, or by setting
   `clusterf.guildHallSeeder.seedOnWorldLoad` to `True` in `modernuo.json` (it appears there, `False`, after the first
   start). The board needs nothing: it is the same item. The directory rows for Healers, Tinkers, Tailors and Smiths need
   pinned's vendor spawns (`[GenerateSpawners Data/Spawns/post-uoml/trammel/Vendors.json`, already in the console's
   World setup list).
7. To walk the path again on one account: `[ClusterFReset`, tick **Account Data** and **Quest History**.

Open for Chase or the overseer: the Mysticism starter book (1.8); whether gargoyles should keep human robes and cloaks
(1.8); whether guild-taken items should count toward the New Haven quest achievements (headline 2); the "fighting pit"
(section 2); the sunk New Haven NPCs (10.1); D-92 as one entry or two (section 5).
