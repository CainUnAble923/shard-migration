# cc-P17: playtest bug sweep 1

Date: 2026-09-30. Agent: Claude Code. Pinned ModernUO `7c9215d97`. Built in `D:\ShatteredLegacy`, **not committed**.
No world was changed: nothing placed, moved or removed on live or test; no shard deployed, restarted or recreated.
`sl-modernuo:latest` was not moved (`16b0f49e6828` before and after). Image: `sl-modernuo:cc-p17-bugs` = `5f1675b0f3a1`.

**Gate before starting.** `git --no-optional-locks status` in `D:\ShatteredLegacy` at `99d5273` was **not clean**: two
untracked files, `design/registrar-office/registrar.py` and `uorender.py`. I stopped and asked; Chase said to go ahead
("might have been another chat"). They are not mine, were not touched, and are still untracked. P16 has not run (no
`notes/cc-P16-mine-camp-tents.md`), so there is no mine camp to keep clear.

Save copies read offline (never the running shards): test `server/lib/uo/modernuo/Saves-test` (2026-09-30 12:00) and live
`.../Saves` (2026-09-29 13:50; live may have moved on since). Scripts: `notes/cc-P15-tools` plus an item decoder written
for this task (decodes all 197,708 items of the test copy per pinned `Item.Serialize`, `Item.cs:816-1080`).

> **Headlines**
>
> 1. **Built:** PT-05, PT-01 with PT-07, PT-03, PT-08. **293 tests pass** (15 new). Every new fact was watched red on a
>    break of its own (section 10).
> 2. **PT-01 and PT-07 are two faults, not one.** New Haven's forges, anvils and ankh are missing because **pinned has no
>    New Haven decoration at all**; the decorate step did run. The Healer is missing because **pinned's spawner import
>    ignores z when it dedupes** and deletes the Healer spawner under the HealerGuildmaster's. That importer bug loses
>    **136 Trammel spawners** shard-wide, not just New Haven's (section 1.4). ModernUO's to report.
> 3. **Live already has hand-placed forges, anvils and an ankh** in New Haven (staff, 2026-05-15 and 05-27). The new
>    seeder keeps anything of that kind already there, and never lets pinned's `FindItem` delete anything (it would:
>    section 1.3). Safe to run on live; dry-run first.
> 4. **PT-04's cause:** "no failure line in the journal" does not rule out a failed attempt. **A craft failure is never
>    written to the journal**; it is shown only in the craft gump's notice box. Reproduced in a test (section 7).
> 5. **PT-09 stopped** on its own stop condition: enforcing ServUO's rule would take two P15 starter-kit items off a
>    gargoyle (the Smiths' **half apron**, the Keepers' **cloak**). Chase decides (section 6).
> 6. **PT-08 is half built.** The 8 gargish **cloth armour** pieces are now tailorable (pinned had the types, never
>    registered them). The gargish **garments** (robe, fancy robe, sash, half apron, Robe of Rite) and the cloth wing
>    armour have **no item type in pinned or ours**: stopped and listed (section 4).
> 7. **PT-10 is faithful:** ServUO shows the same unlabeled pairs, from the same clilocs. Nothing changed; a label change is
>    proposed as an Ours deviation (section 5).
> 8. **PT-05's fix does not move live NPCs on its own.** Both shards run the New Haven seeder's world-load repair, which
>    would have moved all 18 at the next start. World load now accepts an NPC on its old tile; the move is
>    `[ClusterFSeedNewHaven repair`, Chase's command.

---

## 1. PT-01 and PT-07: New Haven decoration and healers

### 1.1 Facts, PT-01

1. **Pinned data and command.** Decoration is placed only by `[Decorate` (`Commands/Object Creation/Decorate.cs:23`,
   folders `:37-42`) or the AdminGump buttons (`Gumps/AdminGump.cs:2044`, `:2104-2129`). Nothing at startup. **Pinned has
   no New Haven set**: inside the New Haven region (x 3416-3545, y 2480-2648, `Distribution/Data/regions.json`) its data
   holds 3 `Static` (`Trammel/_haven additions.cfg`) and 1 `DaemonBloodChest` (`uzeraan turmoil quest.cfg`). Its
   `Trammel/haven.cfg` is pre-UOML Haven: all 17 forge/anvil entries are at x 3592 and east (`haven.cfg:265-334`), the
   ankh at 3606,2582,10 (`:2-3`).
2. **ServUO pub57** ships `Data/Decoration/Trammel/NewHaven.cfg` (122 entries; forges `:138-153`, anvils `:156-160`) and
   three New Haven lines in its own `haven.cfg`: `AnkhNorth` 3526,2516,25 (`:5`), `AnvilEastAddon` 3467,2540,36 (`:265`),
   `SmallForgeAddon` 3469,2535,41 (`:285`). Placed by `[Decorate` (`Scripts/Commands/Decorate.cs:23`, `:35-40`).
3. **The decorate step did run** on both worlds: every pinned Trammel entry is present on the test copy (2192/2192),
   created 2026-09-29 around 22:06 (who ran it: unknown). Top-level items, test world: New Haven region 135 (52 spawners,
   48 doors, 3 statics, board, chest; **no forge, anvil or ankh**); Britain about 2,930 per facet; Minoc about 830.
   Live: the same, plus hand-placed smithy items and an ankh (1.3).
4. **So: pinned has no New Haven set, and the step ran.** Not "both".
5. **Not one fault with PT-07** (1.2). `ClusterFOldHavenCleanup` is not a cause of either: it is a manual command, deletes
   spawners only, and has not run on the test world (its old-Haven Healer spawner is still there).

On a fresh world the only usable smithy in New Haven is the client statics in the Warrior's Guild Hall (forges
3523-3525,2535,20; anvil 3523,2537,22), which `DefBlacksmithy.CheckAnvilAndForge` accepts (`:66`). Its reachability was
not checked.

### 1.2 Facts, PT-07

1. **The HealerGuildmaster does not resurrect in pinned or ServUO.** Both derive it from `BaseGuildmaster : BaseVendor`
   (pinned `Mobiles/Vendors/NPC/Guildmasters/HealerGuildmaster.cs:7`, ServUO `Mobiles/NPCs/HealerGuildmaster.cs:5`).
   Resurrection is `BaseHealer`'s (pinned `Mobiles/Healers/BaseHealer.cs:127-149`, range 4; ServUO range 2). **Ours does**,
   by our patch `server/patches/HealerGuildmaster-resurrection.patch` (an Ours deviation already on the shard). Its
   trigger is the same as pinned's healers: a ghost that **steps into** the 4-tile range from outside it, not frozen, in
   line of sight, on a tile that passes `CanFit(16)` (patch lines 18-23). A ghost already inside the range, or one that
   arrives by teleport, is offered nothing. **Why it did not offer in Chase's case is unverified**; the likeliest reading
   is that he was already inside 4 tiles when he looked for it. Criminal and murderer are allowed on both shards
   (`clusterf.healerPolicy.*` all True), and nothing in the path checks war mode.
2. **What New Haven should have.** Pinned: a Healer spawner (count 2) at 3463,2558,35 and a HealerGuildmaster spawner at
   3463,2558,36 (`Distribution/Data/Spawns/post-uoml/trammel/Vendors.json:150`, `:166`); **no ankh item**. ServUO: a healer
   at 3462,2559,35, the guildmaster at 3464,2558, and `AnkhNorth` 3526,2516,25. **Actual, test world:** the
   HealerGuildmaster only; **0 Healers, 0 WanderingHealers, 0 ankh items** in New Haven. Live: the same, plus 5
   WanderingHealers on the island from the uoml wildlife data and the hand-placed ankh.
3. **Why the Healer is missing: pinned's spawner importer.** `ImportSpawnersCommand.cs:228-241` deletes existing
   spawners of the same type "at this location" through `GetItemsAt(Point3D)`, which ignores z
   (`Projects/Server/Maps/Map.ItemEnumerator.cs:31`). Pinned's data stacks spawners on one x,y at z, z+1, z+2, so each
   later one deletes the one before, and with it what it spawned (`BaseSpawner.cs:1428-1434`). On both world copies the
   last spawner in file order is the only survivor at every New Haven collision:

   | x,y | lost | kept |
   |---|---|---|
   | 3463,2558 | **Healer** (z35) | HealerGuildmaster (36) |
   | 3526,2536 | BlacksmithGuildmaster (20), IronWorker (21) | Miner (22) |
   | 3470,2519 | HairStylist (49) | Herbalist (48) |
   | 3461,2566 | Herbalist (36), Alchemist (37) | HairStylist (35) |
   | 3446,2606 | LeatherWorker (32), Furtrader (31) | Tanner (30) |

   Across pinned's post-uoml and shared data: Trammel 136 spawners lost of 2,137; Felucca 127 of 2,122; Ilshenar 27;
   Malas 13; Tokuno 39; Ter Mur 0. **ModernUO's to report.** This also answers P15 section 11's open question about the
   Warrior's-hall Blacksmith guildmaster and IronWorker. `notes/shard-console.md:586-589` calls this dedupe safe; it does
   not mention that it ignores z.
4. **Ordinary healers and ankhs do resurrect** by pinned's code: `BaseHealer.OnMovement` as above, `Healer.CheckResurrect`
   refuses criminals and murderers (`Healer.cs:43-62`, relaxed on this shard by `Healer-resurrection-policy.patch`), and
   `Ankhs.Resurrect` works at range 2 (`Items/Construction/Ankhs.cs:30-49`). **This was not tested in a client** (no client
   was run), so the brief's "fail anywhere, stop" check is by code and by the facts in 1.5, not by play. There is no
   sign of a shard-wide fault.

### 1.3 Built: `ClusterFNewHavenServicesSeeder`

New file `server/customizations/ClusterFNewHavenServicesSeeder.cs`.

- **Decoration:** ServUO's `NewHaven.cfg` entries plus its three New Haven `haven.cfg` lines, 125 in all, verbatim, one
  per line with its source line beside it. They are **embedded as text** because the build has no route for shipping a
  data file from our tree (`Dockerfile` copies `server/customizations` as code; `apply-patches.sh` mirrors `.cs` only).
  Each is read by pinned's own public `DecorationList.Read` and placed by `DecorationList.Generate`
  (`Decorate.cs:1308-1380`, `:1220-1292`), so construction and the duplicate check are pinned's.
- **Healer:** a Spawner for `Healer` with pinned's settings (count 2, 5-10 minutes, homeRange 0, walkingRange 4, respawned
  at once as the importer does, `ImportSpawnersCommand.cs:248-249`) at **ServUO's healer tile 3462,2559,35**, one tile off
  pinned's. Pinned's own tile would be deleted again by the next `[GenerateSpawners` of `Vendors.json` for the same reason
  as above. The tile fits (port of `Map.CanFit`, height 16). Skipped if any `Healer`, or a spawner of one, is already in New
  Haven.
- **Runs** only by `[ClusterFSeedNewHavenServices [dryrun]` (Administrator), or at world load if
  `clusterf.newHavenServices.seedOnWorldLoad` is True (default False; the server writes the default into `modernuo.json`
  on first start). The existing seeders run on every world load on live, so none of them could carry this.

**Departures from ServUO's files** (argued here as the fidelity rules ask):

1. `NewHaven.cfg:177-178`, `Static 0x F7B`, is left out. The item id does not parse (a space after `0x`), so ServUO places
   an item with id 0 there, which draws nothing. Leaving it out gives the same visible result without a junk item.
2. **An entry is kept out when pinned's `FindItem` would delete something to place it.** `FindItem` does more than find a
   match: it deletes what it takes for an out-of-date copy (`Decorate.cs:1122-1215`, the deletes at `:1212-1215`). That is
   any door on the tile within 8 z (`:1135-1168`), and, for a light source, a lit item at the same z with the same id and
   another light, or the same tile name (`:1170-1190`). Our worlds' doors came from elsewhere: 48 in New Haven on the test
   world, and **24 of ServUO's 76 New Haven doors share a tile with one of them at another facing** (13 more match exactly,
   39 have no door on or beside their tile). Live's hand-placed large forge has lit pieces on ServUO's forge-fire tile.
   So the seeder places nothing it would have to delete for.
3. **An entry is kept out when its kind is already there.** `FindItem` only sees an item of the same type and id on the
   same spot as a match. So a forge or anvil entry is kept out when an item Blacksmithy counts as one
   (`DefBlacksmithy.cs:45-46`) stands on the tile within 3 z, and the ankh when any ankh stands within 10 tiles. On
   **live**, staff placed `Forge`, `Anvil` and `LargeForgeEast` items one by one on 2026-05-15 at ServUO's smithy tiles,
   and an `AnkhNorth` at 3526,2511,65 on 2026-05-27, 5 tiles from ServUO's. Without this check the seeder would stack
   ServUO's addons on them and add a second ankh.

**Tests** (`server/tests/Misc/NewHavenServicesVerification.cs`, 4 facts): on an empty world every one of the 125 entries
is placed and nothing is kept out; a player at 3468,2540,36 has a forge and an anvil that
`DefBlacksmithy.CheckAnvilAndForge` accepts; a second run places nothing and adds no entity, and the dry run agrees; a door
on a ServUO door's tile, and one 5 z above another's, are kept and nothing is stacked or deleted; a hand-placed Anvil,
Forge and ankh as on live are kept and nothing is stacked beside them; after seeding, the Healer is at the spawner,
`CheckResurrect` accepts a ghost, and both the Healer's offer and the ankh's reach their last gate.

**What the test host cannot show:** it has no map files, so `Map.CanFit` is false on every tile there. That was probed:
range, line of sight and frozen state all passed and `CanFit` did not. The last gate of both offers is that `CanFit`
(`BaseHealer.cs:135-139`, `Ankhs.cs:40-47`), so in the test each ends with 502391 "Thou can not be resurrected there!"
where the shard, on a standable tile, sends the resurrect gump. The Healer tile, the ankh tile and the tiles beside them
were checked standable offline. **"A ghost can resurrect in New Haven" is therefore proven up to that gate and needs the
client check in section 12.**

### 1.4 Not built (report)

- **The importer bug itself.** The fix is one comparison in pinned `ImportSpawnersCommand.cs:228-241`: compare z too, or
  match on the spawner's guid. That would be a patch to a pinned file, and on an existing world a re-run of
  `[GenerateSpawners` would then add about 136 Trammel spawners. That is a shard-wide decision, bigger than this part, so
  it is left for Chase and the overseer, with ModernUO to be told.
- The other lost New Haven vendors (table in 1.2). They are not healers and have no playtest report, so they are not
  placed here.
- The HealerGuildmaster's own trigger is unchanged. It is ours already and behaves like pinned's healers.

---

## 2. PT-03: board and quest givers are interchangeable

### 2.1 Facts

1. **The board passes itself as the quest giver.** `NewHavenQuestBoard.OnPick` calls `quest.SendOffer(this, pm)`
   (`NewHavenQuestBoard.cs:236` before this task), so the instance's `Quester` is the board and its `QuesterType` is
   `NewHavenQuestBoard` (`MLQuestEntry.cs:26-31`). **Saved:** the quest, then the quester's **serial only**, then
   `ClaimReward` and the objectives (`MLQuestEntry.cs:514-529`); on load `QuesterType` is taken from whatever that serial
   resolves to (`:531-565`).
2. **Why the NPC refused.** `BaseCreature.OnDoubleClick` calls `MLQuestSystem.OnDoubleClick` (`BaseCreature.cs:2864-2867`),
   whose private `FindQuest` matches a held quest only if `instance.Quester == quester` or, for a non-escort quest,
   `instance.QuesterType == quester.GetType()` (`MLQuestSystem.cs:333-334`). A board quest matches neither.
   `RandomStarterQuest` also skips a quest the player is already doing (`:677`), so the trainer says 1080107 "I have
   nothing for you at this time". **This affects all 26 quests**: each is registered to exactly one NPC type
   (`Distribution/Data/MLQuests.cfg:236-261`), and none overrides the lookup. **The reverse was refused too, by our own
   code**: the board showed a trainer's quest as `TakenElsewhere` with "Take it back to them".
3. **The board already paid through the stock path** (`SendRewardOffer` -> `QuestRewardGump` -> `ClaimRewards`), so there
   was a payout path at either end. `ClaimRewards` guards only `ClaimReward` and `Removed` (`MLQuestEntry.cs:356`), then
   records the quest done and removes the instance (`:420-442`). The board and the trainers hold the **same** `MLQuest`
   object (`NewHavenQuestBoard.Register`), and a player holds one instance of it, so one payout closes both ends.
4. **P15:** `TakeStarterItem` cancels a held instance whoever gave it and calls `SetDoneQuest`
   (`ClusterFGuildStarterPath.cs:407-415`). Then `CanOffer` refuses the quest at either end.

### 2.2 The 26 quests and their NPC counterparts

Every quest has one. **None is board-only**, so the board needs no "board only" line (a fact now asserts it).

| # | Quest | Skill | NPC (pinned class) | Seeder line | Guild |
|---|---|---|---|---|---|
| 1 | CleansingOldHaven | Chivalry | Aelorn | :28 | warriors |
| 2 | TheRudimentsOfSelfDefense | Wrestling | Dimethro | :29 | warriors |
| 3 | CrushingBonesAndTakingNames | Macing | Churchill | :30 | warriors |
| 4 | SwiftAsAnArrow | Archery | Robyn | :31 | rangers |
| 5 | EnGuarde | Fencing | Recaro | :32 | warriors |
| 6 | TheArtOfWar | Tactics | Alden Armstrong | :33 | warriors |
| 7 | TheWayOfTheBlade | Swords | Jockles | :34 | warriors |
| 8 | ThouAndThineShield | Parry | Tyl Ariadne | :35 | warriors |
| 9 | DefyingTheArcane | Magic Resist | Alefian | :37 | arcane |
| 10 | StoppingTheWorld | Meditation | Gustar | :38 | arcane |
| 11 | ScribingArcaneKnowledge | Inscription | Jillian | :39 | arcane |
| 12 | TheMagesApprentice | Magery | Kaelynna | :40 | arcane |
| 13 | ScholarlyTask | Eval Int | Mithneral | :41 | arcane |
| 14 | TheRightToolForTheJob | Tinkering | Amelia Youngstone | :43 | tinkers |
| 15 | KnowThineEnemy | Anatomy | Andreas Vesalius | :44 | healers |
| 16 | BruisesBandagesAndBlood | Healing | Avicenna | :45 | healers |
| 17 | TheInnerWarrior | Focus | Sarsmea Smythe | :46 | warriors |
| 18 | TheArtOfStealth | Ninjitsu | Ryuichi | :48 | dojo |
| 19 | BecomingOneWithTheShadows | Hiding | Chiyo | :49 | thieves |
| 20 | WalkingSilently | Stealth | Jun | :50 | thieves |
| 21 | EyesOfARanger | Tracking | Walker | :51 | rangers |
| 22 | TheWayOfTheSamurai | Bushido | Hamato | :52 | dojo |
| 23 | TheAllureOfDarkMagic | Necromancy | Mulcivikh | :54 | keepers |
| 24 | ChannelingTheSupernatural | Spirit Speak | Morganna | :55 | keepers |
| 25 | **TheDeluciansLostMine** | **Mining** | **Jacob Waltz** | :56 | mining |
| 26 | ItsHammerTime | Blacksmithy | George Hephaestus | :57 | smithing |

Quest classes are in pinned `Engines/ML Quests/Definitions/NewHavenSkillTraining.cs`. The mining quest's only NPC is
Jacob Waltz (`:1775-1818`), which settles Chase's "which NPC" question from the code. The seeder line numbers are
`ClusterFNewHavenSeeder.cs` as it was before this task. No pinned spawn data places any of the 26.

### 2.3 Built

`Engines/ML Quests/Items/NewHavenQuestBoard.cs` and `Engines/ML Quests/Definitions/NewHavenTrainerGuildLines.cs`. Nothing
new is saved; no pinned file is patched.

- **NPC-taken, turned in at the board:** `GetRowState` treats a quest held from its own trainer as the board's
  (`IsInterchangeable`: not an escort, and the instance's `QuesterType` is the board or an NPC type registered for that
  quest). `TakenElsewhere` stays for anything else (none exists today). `OnPick` then runs the stock branch it already
  had: progress, report-back or reward.
- **Board-taken, turned in at the NPC:** each of the 26 trainers' double-click (P15's partial parts) now runs the stock
  double-click inside `NewHavenQuestBoard.TrainerDoubleClick`. That points a held board quest at the trainer for the length
  of the stock call, so the stock `FindQuest` step 1 matches it (pinned has no hook for the match; `FindQuest` is private,
  and it is the public `Quester` setter, `MLQuestEntry.cs:62-70`, that pinned itself uses on delivery at
  `MLQuestSystem.cs:585`). It then points the quest back at the board if it is still held. **Pointing it back** keeps the
  save exactly as it was, and keeps the quest off the trainer's deletion path (`MLQuestSystem.HandleDeletion(IQuestGiver)`,
  `:640-650`). A quest held before this change therefore turns in where it did, and at the other end too.
- **Paid once:** by the shared quest object and `ClaimRewards` (2.1.3), untouched. **A quest done through a P15 guild item
  pays at neither end:** it is done, so the board's row is `Done` and `CanOffer` refuses.
- Board tooltip line 5: "Turn them in here or to their trainer. You can carry 10 quests in all." (was "Bring them back to
  this board, not the trainer."). The picker tab is otherwise as P15 left it.
- Only the double-click path is covered. Pinned has no quest context-menu entry on these NPCs (`BaseCreature.cs:2864`
  is the only call), so there is no other way in.

**Tests changed** (they pinned the old refusal): `EachRowShowsTheStateTheStockPredicatesGive` (a trainer's quest is now
`InProgress` at the board); `AButtonIsJudgedByTheWorldAtTheClickNotByTheMenu` (the board now shows a trainer's quest's
progress, and the quest stays the trainer's); `AQuestTakenAtTheBoardIsNotTheTrainersToTakeBack` is renamed
`TheStockPathAloneDoesNotMatchABoardQuestToItsTrainer`, kept as a check on pinned. **New:**
`AQuestTakenAtTheBoardIsTurnedInToItsTrainerAndPaysOnce`, `AQuestTakenFromTheTrainerIsTurnedInAtTheBoardAndPaysOnce`
(the mining quest and Jacob Waltz), `EveryBoardQuestHasATrainerAtTheOtherEnd`,
`AQuestHeldBeforePT03KeepsTheQuesterItWasTakenFrom`, and in `GuildStarterPathVerification`,
`AQuestDoneThroughAGuildItemPaysAtNeitherEnd`.

**Serialization:** no new saved field, and the save shape is unchanged. The board's own save-shape fact still passes, and
a board quest's quester is the board again after every trainer visit. So the D40 rule's round-trip facts do not apply.

---

## 3. PT-05: NPCs sunk into floors

### 3.1 Facts

- **The Anatomy quest giver is Andreas Vesalius** (`KnowThineEnemy`, `MLQuests.cfg:250`). Only our
  `ClusterFNewHavenSeeder.cs:44` places him: 3458,2551, no z. No pinned spawn data places any of the seeder's types.
- **Cause.** An entry with no z took `Map.Trammel.GetAverageZ` (`ClusterFNewHavenSeeder.cs:270`; pinned
  `Projects/Server/Maps/Map.cs:243-285`). That is the **land** height, which lies under a building's floor. His tile is
  land 30, stone foundation 30, slate floor 35. He was at 30.
- **Pinned puts spawned NPCs on the floor.** `BaseSpawner.GetSpawnPosition` (`BaseSpawner.cs:549-640`) uses
  `Map.CanSpawnMobile` (`Map.cs:1137`, `:1191-1211`), which returns the lowest valid surface, static tops included. Our
  seeders call `MoveToWorld` with no fit check and set `CantWalk`, so a sunk NPC stays sunk.
- **Both shards set `clusterf.newHavenSeeder.seedOnWorldLoad` and `repairOnWorldLoad` to True**
  (`server/uo/modernuo/Configuration/modernuo.json:45-47`, `Configuration-test/modernuo.json:43-45`), and repair compares
  the full location, z included (`NeedsRepair`, `:185-195`). So correcting the entries alone **would have moved all 18 on
  live at its next start**.

### 3.2 Z table, reconciled with P15's 18

Every NPC our code places in New Haven was checked with the port of pinned `Map.CanFit` (height 16) against the client
map, the statics and pinned's New Haven decoration: 40 seeder entries, 5 institution-seeder entries, and 9 guild-hall
tiles. **The 18 sunk ones are exactly P15's 18**; the Artificers' Guildmaster in the water is the 19th, already handled by
`[ClusterFSeedGuildHalls repair`. The save column is the test world.

| NPC | Test save | Now | Change | Why |
|---|---|---|---|---|
| Asandos | 3504,2519,22 | 3504,2519,27 | z | inn floor |
| Clairesse | 3497,2551,15 | 3497,2551,20 | z | shop floor |
| Lowel | 3444,2638,22 | 3444,2638,28 | z | carpenters' floor |
| Hargrove | 3446,2640,22 | 3446,2640,28 | z | carpenters' floor |
| Lyle | 3487,2498,46 | 3487,2498,52 | z | Magery School main room |
| Nibbet | 3488,2568,15 | 3488,2568,20 | z | marble floor (the tile is in the bank, though the entry says Springs N Things) |
| **Andreas Vesalius** | 3458,2551,30 | 3458,2551,35 | z | Healer's Hall floor |
| Avicenna | 3461,2551,30 | 3461,2551,35 | z | Healer's Hall floor |
| Gustar | 3472,2492,66 | 3472,2492,71 | z | west wing floor |
| Alefian | 3468,2492,66 | 3469,2492,71 | x+1 | a brazier on the tile |
| Jillian | 3476,2492,66 | 3476,2493,72 | y+1 | a table on the tile |
| Kaelynna | 3480,2492,46 | 3479,2492,71 | x-1 | the tile is a brick wall |
| Mithneral | 3484,2492,46 | 3484,2493,52 | y+1 | an elven table on the tile |
| Sadrah | 3461,2567,30 | 3462,2567,35 | x+1 | inside a display case |
| Jun | 3426,2520,21 | 3420,2520,21 | x-6 | a lantern on the tile; moved inside the dojo |
| Walker | 3428,2520,21 | 3418,2520,21 | x-10 | no surface; moved inside the dojo |
| Norton | 3510,2603,-5 | 3507,2603,1 | x-3 | open water; nearest pier plank |
| Jacob Waltz | 3511,2744,0 | 3510,2745,0 | x-1,y+1 | impassable rock |

Every other entry fit already. The four entries that also had no z (Andric, Kashiel, Aelorn, Dimethro) now state 20, the
z they already resolved to, so they do not move. After the change all 40 entries fit, and no two share a tile.
Unverified: which Magery School floor is the ground floor was inferred from tile names and heights, not a render; and the
fit check reads the map and pinned's data, not items a world may have added since.

### 3.3 Built

`ClusterFNewHavenSeeder.cs`:
- **Every entry states its z.**
- **The 18 name the tile they used before** (`.WasAt(x, y[, z])`).
- **World-load repair accepts an NPC standing on its old tile**, so an existing world keeps them where they are until an
  Administrator runs `[ClusterFSeedNewHaven repair`, which moves them.
- **A fresh world places them on the floor.**

The command's help text says so. Entries, `Seed` and `NeedsRepair` are now `internal` for the facts.

**Tests** (`server/tests/Misc/NewHavenSeederFloorVerification.cs`, 2 facts):
- `EveryNewHavenSeederNpcStandsOnItsMeasuredFloor`: no entry takes the land height, and every entry is on its measured
  floor. The test host has no map files, so the floors are the offline measurements above, pinned in the fact.
- `WorldLoadLeavesAnNpcOnItsOldTileAndTheRepairCommandMovesIt`.

---

## 4. PT-08: gargish clothing not in the Tailoring menu

### 4.1 Facts

1. **Pinned `DefTailoring` has 17 gargish entries, all armour**, each inside `if (Core.SA)` with
   `SetNeededExpansion(SA)`, and with no race or recipe gate. There are 9 leather (`:541-560`) and 8 "studded"
   (`:612-629`). **It has no clothing line at all.** The clothing types do not exist in pinned or in ours: GargishRobe,
   GargishFancyRobe, GargishSash, GargoyleHalfApron, RobeofRite, GargishClothWingArmor. That is why leather shows and
   clothing does not. Pinned **does** have the 8 gargish cloth armour types (`Items/Armor/Cloth/GargishCloth{Arms,Chest,
   Kilt,Legs}Type{1,2}.cs`), but only as creation clothes (`CharacterCreation.cs:773-797`); no craft registers them.
2. **Pinned `DefBlacksmithy` has no gargish entries.** All gargish smithing is ours (`BlacksmithyCraftRegistrations.cs:
   76-92`, 15 entries). Pinned `DefMasonry` and `DefCarpentry` have none either.
3. **Expansion:** `Configuration/expansion.json:2` Id 11 "Endless Journey", `:23` SA true; `Configuration-test` is the same.
   Not the cause.
4. **ServUO pub57's gargish wearables by craft** (54, weapons excluded). Resources are Cloth (1044455), Leather (1044462)
   and IronIngot.

   | Craft (ServUO line) | Type | Resource x amount | Skill | Pinned type | Ours |
   |---|---|---|---|---|---|
   | Tailoring :361 | GargishRobe | Cloth 16 | 53.9-78.9 | **none** | none |
   | Tailoring :363 | GargishFancyRobe | Cloth 16 | 53.9-78.9 | **none** | none |
   | Tailoring :365 | RobeofRite (recipe) | Leather 6 + FireRuby, GoldDust, AbyssalCloth | 101.5-120 | **none** | none |
   | Tailoring :437 | GargoyleHalfApron | Cloth 6 | 20.7-45.7 | **none** | none |
   | Tailoring :438 | GargishSash | Cloth 4 | 4.1-29.1 | **none** | none |
   | Tailoring :543 | LeatherTalons | Leather 6 | 40.4-65.4 | none | ours, registered |
   | Tailoring :645-661 | GargishLeather Arms/Chest/Legs/Kilt, male and female, and Wing | Leather 6-12 | 53.9-95.5 | yes (Type1/Type2 by alias) | pinned registers them |
   | Tailoring :711-725 | GargishCloth Arms/Chest/Legs/Kilt Armor, male and female | Cloth 6-10 | 82.9-144.0 | **yes, never registered** | **registered here** |
   | Tailoring :727 | GargishClothWingArmor | Cloth 12 | 65.0-90.0 | **none** | none |
   | Blacksmithy :341-357, :425-435 | 8 plate, GargishAmulet, 6 shields | Iron 3-25 | various | none | ours, registered |
   | Masonry | 8 stone, LargeStoneShield, GargishStoneAmulet | Granite | | stone types yes | unregistered |
   | Carpentry | GargishWoodenShield | Board | | yes | unregistered |
   | Tinkering | necklace, bracelet, ring, earrings | Iron 3 | | | ours, registered |

   The pinned-vs-ServUO drift on the leather numbers is pinned's (for example, chest 12 leather where ServUO has 8).
5. **Overlap.** Q-064's seven recipe-gated garments are human garments: no overlap. P15's list: the Robe maps to
   GargishRobe/GargishFancyRobe and the HalfApron to GargoyleHalfApron, **neither of which exists**; ServUO has no crafted
   counterpart for the Cloak. As P15 found, by pinned's race rules a gargoyle can wear the human items anyway (section 6).

**Found in passing (pinned, not ours):** the 8 "gargish studded" tailoring entries use clilocs 1020643-1020650, which read
"gargish stone ...", and their classes use the stone art. So the tailor's Studded group lists "gargish stone" pieces made
from leather. ServUO has no gargish studded items. Left alone; ModernUO's to report if anyone cares.

### 4.2 Built, and where it stopped

- **Built:** ServUO's 8 cloth armour entries (`DefTailoring.cs:711-725`) in `Engines/Craft/TailoringCraftRegistrations.cs`:
  - on pinned's types, with ServUO's names (1021027/29/31/33), skills, cloth and message 1044287, in "Cloth Armor"
    (1111748);
  - `GargishCloth*Armor` is pinned's `Type1` and `FemaleGargishCloth*Armor` is `Type2`, by pinned's TypeAliases; the art
    matches piece for piece (ServUO `Items/Equipment/Armor/GargishClothArmor.cs`);
  - no `SetNeededExpansion`, as ServUO sets none.
- **Stopped** (item types missing): the 5 garments and the cloth wing armour. Porting them means porting 6 clothing item
  types, not adding craft entries. The list above is the deliverable. Without them a gargoyle still has no tailorable
  robe, sash or apron.
- **Test:** `TailoringCraftsServUOsEightGargishClothPiecesAndAGargoyleWearsOne` (`server/tests/Engines/Craft/
  CraftRegistrationsVerification.cs`):
  - all 8 rows carry ServUO's values;
  - a gargoyle tailor makes a chest from 8 cloth and wears it on InnerTorso (the tile row is seeded for the fact).
  - The pinned-tables fact now also asserts pinned's own table lacks two of the pieces.

---

## 5. PT-10: gargish platemail listed twice

1. **The pairs** are all ours: `BlacksmithyCraftRegistrations.cs:76-83` adds `FemaleGargishPlate{Arms,Chest,Legs,Kilt}` and
   `GargishPlate{...}` (art 0x307-0x30E). Pinned has no gargish plate type. It is **not an accidental duplicate**: it is a
   faithful copy of ServUO's male and female pairs.
2. **ServUO does not label them either.** `DefBlacksmithy.cs:341-355` uses one cliloc per pair: 1095336 "gargish
   platemail arms", 1095338 "chest", 1095342 "leggings", 1095340 "kilt". The made items take their names from their art
   (1020775-1020782), so the female and male pieces also have the same name on the item. ServUO does the same in Tailoring
   (leather and cloth) and Masonry.
3. **Either sex can wear either piece, the chest included.** Every one of the 8 classes sets only
   `RequiredRaces => AllowGargoylesOnly` (`GargishPlateArms.cs:19` and so on), and none overrides `AllowMaleWearer` or
   `AllowFemaleWearer`. Pinned's check is `BaseArmor.CanEquip` (`BaseArmor.cs:1100-1126`, defaults `:173-174`). ServUO is
   the same. Chase's observation holds for every piece. **Severity stays Low**: it is a menu clarity problem, not a trap.

**Changed: nothing** (faithful). The cloth pairs PT-08 added are unlabeled the same way.

**Proposed Ours deviation, for Chase to accept or decline:** give the female entries a text name, "gargish platemail arms
(female)" and so on, in Blacksmithy and Tailoring, with the male entries left on ServUO's cliloc. It is one line per entry
(a string name instead of the cliloc). If accepted, a fact asserts that each pair's two entries have different names. The
items themselves keep their art names either way.

---

## 6. PT-09: gargoyles wearing human armour (stopped)

### 6.1 Facts

1. **Pinned does not enforce it at all.** `Item.RequiredRaces` defaults to all races (`Projects/Server/Items/Item.cs:2110`),
   checked by `CheckRace` (`:2115-2146`) in `BaseArmor.CanEquip` (`BaseArmor.cs:1095`), `BaseWeapon.CanEquip`
   (`BaseWeapon.cs:1044`) and `PlayerMobile`'s re-validation (`PlayerMobile.cs:1374`, `:1399`). `BaseClothing` checks only
   its own `RequiredRace` (`BaseClothing.cs:178`, `:442`), which no pinned class sets, and `BaseJewel` checks nothing.
   Ringmail and Bascinet set nothing, so a gargoyle wears them. This is not tied to expansion, and our code bypasses
   nothing. **Enforcing is a deliberate deviation toward ServUO and away from pinned**, as the brief says.
2. **ServUO's rule**: a `CanBeWornByGargoyles` property, false by default on armour, clothing and weapons and true on
   jewellery, checked in each `CanEquip` (`BaseArmor.cs:2408-2451`, `BaseClothing.cs:461-506`, `BaseWeapon.cs:1033-1075`,
   `BaseJewel.cs:422-602`). There are 133 per-item overrides in 115 files.

   | Item class | ServUO pub57 | Pinned (our shard today) |
   |---|---|---|
   | human/elf body armour (ringmail, plate, leather) | no | yes |
   | helmets | no | yes (6 elf-only helms excepted) |
   | hats (clothing) | no | yes |
   | shields | no, except gargish shields and VirtueShield | yes |
   | weapons | no, except gargish weapons, pickaxes, crooks, hoe, whips | yes |
   | clothing | no, except gargish clothing and Robe and its variants | yes |
   | jewellery | yes, all | yes, all |
   | gargish items | yes | yes |

3. **What a gargoyle can get after PT-08.**
   - **Metal:** 15 (ours: 8 plate, amulet, 6 shields).
   - **Leather:** 9, plus talons, plus 8 "studded" (actually stone art).
   - **Cloth armour:** 8 (this task).
   - **Cloth garments:** 0.
   - **Buy:** nothing. `ClusterFGargoyleVendors.cs` sells the human vendors' stock.

### 6.2 Why it stopped

A gargish path now exists in cloth, leather and metal armour, so the first condition would allow enforcing. **The second
stop condition holds**: our `CharacterCreation.cs` (which P15's guild kits reuse) equips a gargoyle with items ServUO's rule
refuses and pinned allows:

- **HalfApron**: Blacksmithy (`:1036`), which is the Smiths' Fellowship kit. ServUO: denied (`Clothing/Waist.cs:40`), and
  ServUO gives gargoyles nothing instead (`Misc/CharacterCreation.cs:1038-1041`).
- **Cloak**: Spirit Speak (`:1295`), which is the Keepers of the Last Door kit. ServUO: denied (`Cloaks.cs:41`), nothing
  instead (`:1327-1330`).
- Also found, which P15 did not list: **SkinningKnife**, Tracking (`:1336`, equipped; ServUO puts it in the pack), and
  **BoneHelm**, the Necromancer profession (`:502`; ServUO gives it only to humans and elves).
- **Correction to P15 section 6:** the **Robe passes** ServUO's rule (`OuterTorso.cs:1256`); and all jewellery is
  gargoyle-wearable in ServUO, so the Gold and Silver bracelets and rings need no gargish version.

So enforcing would take two P15 kit items off a gargoyle, and PT-08 cannot give it a gargish apron or garment. **Chase's
to resolve.** The options: (a) enforce, and drop the apron, cloak and bone helm from gargoyle kits as ServUO does (and pack
the skinning knife); (b) enforce, and first port the gargish garments (PT-08's stopped half); (c) do not enforce, and keep
it recorded as pinned's behaviour. Size if enforced: about 45 lines of gate in 4 base classes, which are pinned files and
so need patches, plus the allow-list data. Pinned's `RequiredRaces` bitmask (`AllowHumanOrElves`, `Race.cs:40`, unused)
could express most of it without the ServUO property.

### 6.3 Items already worn on live, if it is enforced

| Choice | What happens | Cost |
|---|---|---|
| Unequip at login (ServUO's `ValidateMobile` does this for armour and clothing, `BaseArmor.cs:1480-1484`) | the piece goes to the pack when the gargoyle next logs in | a player loses a look or stats without warning; needs a login message; overweight packs drop to the ground in some code paths |
| Leave it on until removed | only a new equip is refused | inconsistent: two gargoyles, one in ringmail it can never put back on; hard to explain on a wiki |
| One-off command that unequips and mails or banks the piece | Chase runs it once | most work; clearest result |

Chase decides. Nothing was built.

**Found in passing (the other direction):** `MysticsGarb` (ours, a `Robe`) and our `GargishRing` and `GargishBracelet` set
`RequiredRaces` gargoyle-only, but sit on bases that never check it. So **a human or elf can wear them today**. Ours to fix
whenever the race gate is touched.

---

## 7. PT-04: Make X made one item

**The actual cause: most likely the second attempt failed its skill check.** Chase's observation does not rule that out,
because **a failed craft is never written to the journal.** `PlayEndingEffect` *returns* the cliloc rather than sending it
(for example `DefTinkering.cs:111`, `DefBlacksmithy.cs:139-146`). `CraftItem.cs:1354` takes it and `:1361` passes it as the
notice of a new CraftGump, drawn inside the gump (pinned `CraftGump.cs:113`). So "one item, the craft gump reopens with
'You failed to create the item...' in its notice box, nothing in the journal" is exactly the report.

The other stops after one success report the same way, in the gump only:
- missing materials, mana or stamina;
- a failed `CanCraft` (anvil or forge out of range, tool);
- a manual craft started mid-run.

**No path** in the code ends a run after one item with no gump and no journal line (the three silent branches cannot be
reached). If Chase saw **no gump reopen**, the code does not explain it. Check which build he was on: `docs/bug-list.md`
D25 and D29 say live runs an old, untracked image.

**Defect found (ours):** a run that ends on a pre-check failure (materials, mana, `CanCraft`) **leaves the repeat armed**
(`RepeatCount` 3 for "5 items"), because only `CraftItem.cs:1291` and `:1360` clear it. It is mostly hidden because every
manual start clears it and the count gump re-arms it. **Nothing tells the player that "Make 5" stopped early**, and the
success text between items is discarded (`:1286`). F-1's "summary line at the end" covers both. **Not fixed**; F-1 is
P18's.

**Tests** (`server/tests/Engines/Craft/MakeXRepeatVerification.cs`, 3 facts, through the real entry point: the count
gump's "5 items" button, and the real timer chain):
- at a skill that cannot fail, five rings and no craft gump between them;
- a failed second attempt ends the run after one ring, with 1044043 or 1044157 in the gump's notice and **not** on the
  wire as a message (the random source is pinned by swapping `BuiltInRng.Generator`);
- running out of ingots ends it after one ring and leaves `RepeatCount` at 3.

The host needed `AntiMacroSystem.Configure()`: a craft below its maximum skill runs the gain check, which reads those
settings.

---

## 8. PT-06: new character already in the Miner's Compact

**P15 covers what it set out to.**
- `ASecondCharacterOnTheSameAccountGetsItsOwnToolsAndItems` (`GuildStarterPathVerification.cs:243`): a second character
  gets its own tools, satchel, logbook, ledger and Jacob's Pickaxe, and the first cannot take a second.
- `AFreshCharacterWithNoSkillAndNoGoldJoinsAndGetsItsToolsOnce`: joining gives the items once.

**What is left, and it is a decision, not a bug:** membership is still **per account** (`ClusterFAccountData.JoinedGuilds`;
the only add is `ClusterFGuildSystem.Join`, `:413`). So a brand-new character on an account whose other character joined
the Compact **is** a member. It gets "Welcome back" and its own kit. A character on a new account is not a member
(`CanJoin` true in fact 1). That matches F-9's text, "Tracked per character, not per account, whatever F-4 and F-7 decide
about membership" (`docs/feature-queue.md:520`, about kits and items). Whether membership itself becomes per character
belongs to F-4/F-7. Not rebuilt.

---

## 9. What changed, file by file

All in `D:\ShatteredLegacy\server`. ASCII in every file touched. `server/patches/` untouched; no pinned file patched.

| File | Part | What |
|---|---|---|
| `customizations/ClusterFNewHavenServicesSeeder.cs` (new) | PT-01, PT-07 | ServUO's New Haven decoration (125 entries) through pinned's `DecorationList`; Healer spawner; `[ClusterFSeedNewHavenServices [dryrun]`; setting `clusterf.newHavenServices.seedOnWorldLoad` (default False) |
| `customizations/ClusterFNewHavenSeeder.cs` | PT-05 | every entry states its z; 18 corrected tiles with `WasAt` old tiles; world-load repair accepts the old tile |
| `customizations/Engines/ML Quests/Items/NewHavenQuestBoard.cs` | PT-03 | `IsInterchangeable`, `TrainerDoubleClick`; `GetRowState` accepts a trainer's quest; tooltip line |
| `customizations/Engines/ML Quests/Definitions/NewHavenTrainerGuildLines.cs` | PT-03 | the 26 trainers' stock double-click runs inside `TrainerDoubleClick` |
| `customizations/Engines/Craft/TailoringCraftRegistrations.cs` | PT-08 | 8 gargish cloth armour entries |
| `tests/Misc/NewHavenServicesVerification.cs` (new) | PT-01, PT-07 | 4 facts |
| `tests/Misc/NewHavenSeederFloorVerification.cs` (new) | PT-05 | 2 facts |
| `tests/Engines/Craft/MakeXRepeatVerification.cs` (new) | PT-04 | 3 facts |
| `tests/Engines/MLQuests/NewHavenQuestBoardVerification.cs` | PT-03 | 4 new facts, 3 changed (2.3) |
| `tests/Misc/GuildStarterPathVerification.cs` | PT-03 | 1 new fact |
| `tests/Engines/Craft/CraftRegistrationsVerification.cs` | PT-08 | 1 new fact; the pinned-tables fact lists two cloth types |

15 new facts: 278 before (P15), 293 now.

---

## 10. Red and green runs

All through `docker/uo/build.sh`. Breaks were applied by a script to backed-up copies, restored from the copies, checked
byte-identical by SHA-256 after every run, and grepped for markers: none left.

| Run | Breaks | Result |
|---|---|---|
| builds 1-3 | none | did not compile, three times: target-typed `new(...).WasAt` (C# has no target there), `Items.` resolving to the mobile's item list inside a trainer, pinned enumerators that are not `IEnumerable`; fixed |
| build 4 | none | 288/292: the seed count saw my own test smith; ghost move sent account features with no account; a skill-gain crash (`AntiMacroSystem.Settings` null in the host); a chest needing 25 strength |
| build 5-6 | none | 292/293: `Map.CanFit` false in the host (probed: range, LOS, frozen all true). The resurrect fact was rewritten to prove each gate up to CanFit |
| build 7 | none | **293 passed** |
| red A | a: Vesalius back on the land height; c: the trainer never borrows a board quest; f: every forge and anvil entry kept out; i: no cloth armour registered; j: a guild item leaves a held quest open; k-material: a materials failure clears the repeat; k-skill: a failed check leaves it armed | **284 passed, 9 failed**, every target hit: floor fact ("Andreas Vesalius: takes its z from the land height"); board-to-trainer ("Expected True"); smithy ("no anvil Blacksmithy accepts"); cloth (no matching entry), and the pinned-tables fact with it (expected, it lists the cloth types); guild fact (`Done` expected, `ReadyToTurnIn`), and P15 fact 3 with it (expected, its own break); skill failure (`RepeatCount` 0 expected, 3); materials (3 expected, 0) |
| red B | b: world load moves an NPC off its old tile; d: only board quests interchangeable; e: a borrowed quest never handed back; g: nothing already there keeps an entry out; h: a Healer already there never seen; k-control: a success never starts the next item | **281 passed, 12 failed**, every target hit: world-load fact; trainer-to-board, plus the two changed board facts that now expect it (expected); held-before-PT-03; door and hand-placed facts; smithy fact (a second Healer spawner); Make X control, plus the other two Make X facts (expected: none gets a second attempt) |
| build 8 | none, after the no-delete guard (1.3, departure 2) | **293 passed** |
| red C | the door guard back to 3 z; a probe printing what pinned called "already there" | 291 passed, 2 failed: the door fact (the door 5 z above was deleted), and the probe's deliberate failure. The probe showed the "7 already there" of earlier runs were the Necromancers' Hall doors, outside the New Haven box, **left by an earlier fact's cleanup** (test pollution, not data); the facts' cleanup box was widened to the seeder's whole extent, and a fact now asserts an empty world gets all 125 |
| final | none, restored and hash-checked | `docker/uo/build.sh -t sl-modernuo:cc-p17-bugs`: **293 passed**, "Built sl-modernuo:cc-p17-bugs with patches applied and 293 shard test(s) passing." |

The test log also carries "Item.Amount <= 0" errors for a Corpse from another fact. They are not from this task's facts,
and I did not chase them.

---

## 11. Proposed wiki text (for the overseer)

**New Haven training quests (PT-03, D-90):**
> Every New Haven training quest can be taken at the New Haven training board in the town square or from its trainer, and
> turned in at either. Take Recaro's quest at the board and hand it in to Recaro, or the other way round: same quest,
> same reward, paid once. If you already took the item from your guild, the quest counts as done at both.

**Resurrection in New Haven (PT-07; the guildmaster part is ours, via our patch):**
> New Haven has a healer in the Healer's Hall, west of the bank, and an ankh on the north side of the Warrior's Guild
> Hall. Walk up to the healer as a ghost (from a few steps away) and it offers to bring you back; at the ankh, stand next
> to it or use its menu. The Healer guildmaster there will also offer, the same way. If an offer does not come, step
> away and walk back in. Criminals and murderers are resurrected here too.

(Healer-hall and ankh locations as the seeder places them. The last sentence reflects `clusterf.healerPolicy` True on both
shards; drop it if that changes.)

PT-09 wiki text: not written, since the rule was not enforced.

---

## 12. Checklist for Chase

1. **Commit** with `D:\UO\Commit-ShardWork.ps1`. Not mine: the untracked `design/registrar-office/registrar.py` and
   `uorender.py` (they were there before this task started). Decide whether they go in the same commit. This task's files
   are the 11 in section 9.
2. **Rebuild the test shard** from the console ("Rebuild through the gates") and read the output: the gate should say 293
   passed. Note this build retags `sl-modernuo:latest`; `sl-modernuo:cc-p17-bugs` is this task's image.
3. **World state on the test shard** (item 4), then **on a fresh test character:**
   1. New Haven smithy (the "Forge and Anvil", around 3467-3477, 2535-2541): forges and anvils stand there. Smelt ore
      and make one item with Blacksmithy.
   2. Die in New Haven. As a ghost, walk into the Healer's Hall from outside and toward the Healer (around 3462,2559):
      the resurrect gump opens. Also try the ankh at 3526,2516. **This is the one thing the tests could not show**
      (section 1.3).
   3. Take the mining quest at the board; raise Mining to 50; double-click Jacob Waltz: he takes it and pays. Then take
      another quest from its trainer (for example Recaro) and turn it in at the board's Training quests tab. Each pays
      once.
   4. Andreas Vesalius (Healer's Hall) stands on the floor and can be clicked without ctrl+shift; so do the other 17 in
      section 3.2.
   5. As a gargoyle tailor: the Tailoring menu has a **Cloth Armor** group with 8 gargish pieces (two of each name, as in
      ServUO). Blacksmithy shows the plate pairs unchanged (section 5).
   6. PT-09 was not enforced: a gargoyle can still put on ringmail and a bascinet.
4. **World-state commands** (Administrator, in game; test first, then live if wanted):

   | Command | What it does | Re-run |
   |---|---|---|
   | `[ClusterFSeedNewHavenServices dryrun` | counts what would be placed; changes nothing | safe |
   | `[ClusterFSeedNewHavenServices` | places ServUO's New Haven decoration and a Healer spawner where missing; **moves and deletes nothing**. On **live** it keeps the hand-placed forges, anvils and ankh, and places no door where a door stands | safe: places nothing twice (verified by a fact) |
   | `[ClusterFSeedNewHaven dryrun` | counts the NPCs `repair` would move (all 18 on a world seeded before this change) | safe |
   | `[ClusterFSeedNewHaven repair` | **moves** the 18 New Haven NPCs of section 3.2 onto their floors; creates only missing ones | safe: creates nothing that exists, and a second run moves nothing |
   | `[ClusterFSeedGuildHalls repair` | (P15's) moves the Artificers' Guildmaster out of the water | safe |

   A fresh world: run the first two after the world setup list, or set `clusterf.newHavenServices.seedOnWorldLoad` to
   True in `modernuo.json` (it appears there, False, after the first start). **Suggest adding
   `[ClusterFSeedNewHavenServices` to the console's World setup list** (`scripts/Shard-Console.ps1:1230-1249`), after the
   `[GenerateSpawners` lines. The New Haven NPC seeder already places on the floor for a fresh world.
5. **Decisions for Chase:**
   - **PT-09:** enforce or not, and what happens to gargoyle kits (6.2) and to armour already worn on live (6.3).
   - **PT-10:** accept or decline the "(female)" label deviation (section 5).
   - **PT-08:** whether to port the 6 missing gargish clothing types (4.2); PT-09's option (b) depends on it.
   - **PT-07:** whether to patch pinned's spawner importer, which loses 136 Trammel spawners shard-wide (1.4), and whether
     to restore New Haven's other lost vendors.

Open, unverified:
- Why the HealerGuildmaster did not offer in Chase's case (1.2).
- The reachability of the Warrior's Guild Hall static smithy.
- Whether the live save copy (2026-09-29 13:50) is current.
- Who ran `[Decorate` and the spawner import on the test world.
- Nothing here was run in a client.
