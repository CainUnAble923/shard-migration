# cc-P194: port Wrong (revamped) and the Covetous Void Spawn

Written 2026-10-20 by the Bronze Golem (Fable), on branch golem/Bronze/P194 of both repos. Prompt:
`cc-prompts/claimed/Bronze/cc-P194-port-wrong-and-covetous-void.md`. Both repos were clean at the start. Not committed:
the Golem commits after DONE. Pinned paths are relative to `D:\UO\ModernUO-pinned\Projects` (d4531cd9); ServUO paths to
`D:\UO\ServUO-pub57\Scripts`; "ours" is `server\customizations\Services\Revamped Dungeons` unless said otherwise.

**Two sittings.** The first (2026-10-20, 12:11 to 15:43) wrote the port and stopped when the harness reported build
cycle 7 killed for low memory; the overseer committed its tree as WIP (`8c4f7bd` in ShatteredLegacy, `433e6fe` here)
and reset the branch to main for the retry. The second sitting (2026-10-20 from 15:45; this file's final state)
cherry-picked both WIP commits back onto the rebased branch without committing (`git cherry-pick --no-commit`, then
`--quit`), resolved the two conflicts (CHANGELOG.md and VERSION: main had reached 2026.10.20.3 with P203, so this
prompt's section is `## 2026.10.20.4`; the docs repo's README, dashboard and progress.json are progress.py output
and were regenerated), found that cycle 7 had in fact finished (section 3), fixed the one red fact (a test-ordering
trap, D16) and one ServUO off-by-one the gate then exposed, ran the green gate, the red proof, the tagged image and
the headless boots. Memory at the start of the second sitting: 1.3 GB free of 31.7 (1.9 GB available), the Docker
VM holding 14.6 GB of which 13.3 GB was page cache; `sync; echo 3 > /proc/sys/vm/drop_caches` in a privileged
alpine container (no container or state touched) gave it back and Windows read 8.5 to 10 GB available for the rest
of the sitting. Every build cycle was started as a detached process (PowerShell `Start-Process` of `run-cycle.sh` in
the session scratchpad) with its log on disk, so a harness reap cannot take the build with it.

## Headlines

1. **Both rows move: Wrong (revamped) from 2 of 26 to 26 of 26 (in), Covetous Void Spawn from 2 of 29 to 25 of 29**
   (progress.py, stem proxy, `SL_SHARD` at the Bronze copy; the port list goes from 478 to 501 of 983 files).
   **The "2 done" each row started with was never Wrong or Covetous work:** the stem proxy matched `Generate`,
   `Region` and `Gumps` to Shame's, Despise's and Pet Training's files of those names. Counted at the start: 0 of 26
   and 0 of 29 were ported. The four Covetous files left are the rewards that hook harvesting (section 6).
2. **Wrong, whole:** the 38 spawners of `RevampedSpawns/WrongRevamped.xml` as a data table (68 creatures on both
   facets), the 290-piece level-3 maze of `Data/Decoration/Wrong/WrongMaze.cfg` as a data table (224 self-revealing
   walls, 34 lockpickable doors, 31 statics), the two regions (the level-3 jailor's capture-and-resurrect and the
   peaceful jail), the bedroll spawner with its 80 bedrolls and 5 mysterious tunnels, the seven hot-item chests and
   the hot-item curse, 16 teleporters, 13 creatures (Executioner is stock pinned), the prisoner's escort quest on
   pinned's ML quest engine, soap, the stinking cauldron, the Blanket of Darkness and the Torture Rack. One command
   each way: `[GenWrongRevamp` (deletes the old dungeon's spawners, teleporters, doors and sparkles first, as ServUO
   does) and `[DeleteWrongRevamp`. **No map, statics or art change is needed:** the revamp is items on the stock map.
3. **Covetous, the core:** the Void Pool controller (one per facet; the battle, waves, waypoints, score, the lost
   walls, points), its region (priority 51, the Despise rule), the level-3 spawner as an item of its own, the wave
   and stats records (the scoreboards save through GenericPersistence), the three gumps and the reward gump base
   (`Gumps/BaseRewardGump.cs`, `Services/CommunityCollections/CollectionItem.cs`, two leaf ports), the 25 void
   creatures, the four retyped level 1-2 creatures, Cora the sorceress (fire breath, mana aura, teleport, the
   mana-drain cracks) and Vela the reward vendor, the Void Pool points system on the P33 framework, the five void
   artifacts (plus the gargish Blight), the Cauldron of Transmutation and the Temporary Forge, the best-wave board,
   and `[SetupNewCovetous` / `[DeleteCovetous`. One patch, `PlayerMobile-void-pool-context.patch`: the one line
   ServUO's PlayerMobile has for "The Void Pool" in a player's own context menu inside the region (section 2.4).
4. **Where the port met the shard's rules:** Hephaestus keeps its fixed Self Repair 5 (F-27 keeps Self Repair out
   of random loot; a named artifact's value is OSI's). Void Pool points are the shard's P33 `PointsSystem`, one more
   subclass as that file was written for. The Cauldron of Transmutation turns Verite into Valorite and Bloodwood into
   Frostwood on the shard's `ResourceInfo` order, which keeps OSI's up to there (the shard's own tiers sit after).
   Nothing in either row touches the 200 skill cap, loops, guild skills, loot boxes, Clean Up or the Bestiary.
5. **Client check: nothing blocked.** Every item id both rows use and every body is named in the client data
   (section 5); the two rows need no map or multi.
6. **Deviations** (section 4, proposed D-141 to D-156): the hot-item curse has no property lines and no return to
   the trunk (pinned has no item sockets and no drop hook); the Unlock spell does not open a maze door; Fezzik keeps
   his Three Tiered Cake recipe (the shard has no such recipe); Cora's aura fires every tick, not 40% of them; no
   Antique, SplinteringWeapon, gargish Katana, Plate Shield or Glasses; no Town Cryer quest hooks; LesserOni's
   AngryFire; the escort rewards' shape. Four ServUO bugs fixed rather than copied, each argued.
7. **The gate is green and the image is built:** the suite is 1,571 tests, 1,567 passed, 4 skipped (pinned's), 0
   failed (cycles 10 and 13); cycle 11 (the red proof, all ten breaks at once) turned exactly the ten new facts red
   and nothing else; cycle 13 built `sl-modernuo:cc-P194` through all three gates; two headless boots on a scratch
   copy of the bot world loaded and saved clean (section 7). The one red fact after the first sitting was the
   battle fact, and the cause was the test, not the port: `PacketTestUtilities.CreateTestNetState` resets
   `Core.Now` to real time (D16, documented in `server/tests/Route/ShardTestClock.cs`), and the fact made its
   NetState after the controller had computed its first battle time on the advanced clock, so the next battle
   read twenty minutes ahead instead of fifteen. The NetState is now made first. Cycle 12 then caught a flake that
   is a fifth ServUO bug: the hot-item chest's scroll roll runs one past the scroll table (section 4), so one chest
   in 65 had no scroll; fixed with `Length - 1` (section 3, cycles 8-13).
8. **For the integrator:** `CHANGELOG.md` gains `## 2026.10.20.4` above main's committed `## 2026.10.20.3` (P203)
   and VERSION becomes 2026.10.20.4 (the second sitting renumbered them from .2 when it rebased onto main). If
   another branch lands a `## 2026.10.20.4` first, this section takes the next number and VERSION follows; nothing
   else in the section depends on the number. `Services/PointsSystems/PointsSystem.cs` gains one enum member
   (`VoidPool`) and `docker/uo/apply-patches.sh` one `apply_patch` line at its end; nothing else overlaps.

## 1. What was ported, with file:line

All under `server\customizations\Services\Revamped Dungeons\<row>\` at ServUO's own paths, so apply-patches.sh
mirrors them into `Projects/UOContent/Services/Revamped Dungeons/...`. Line counts are the ported files'.

### 1.1 Wrong (revamped), `WrongDungeon\`

| ServUO file | Ours | What, and what changed |
|---|---|---|
| `Generate.cs` (117) | `Generate.cs` (170) | `[GenWrongRevamp` / `[DeleteWrongRevamp` (`WrongGenerator`). `DeleteOldWrong` deletes every spawner (pinned `BaseSpawner`, where ServUO deletes `XmlSpawner`), `Teleporter`, sparkle 0x375A, `BarredMetalDoor`, `SecretDungeonDoor` in the dungeon rectangle on both facets, plus `BedrollSpawner` (ServUO misses its own and lays a second set of bedrolls on a re-run; D-4 rule). `Generate` places the spawners, the maze, a bedroll spawner per facet, the chests, the 16 teleporters; everything is tagged "newwrong" so Delete can take it down |
| `RevampedSpawns/WrongRevamped.xml` (1,597) | `WrongSpawns.cs` (new, 130) | the 38 rows as `Definition`s, generated by script (`gen_wrong.py` in the session scratchpad): 19 per facet, same multiset; names `#WrongRevamped` (28) and `WrongPrisoner` (10); 126 requested, 68 possible (every row but two asks for more than its entries allow, as on ServUO: XmlSpawner2.cs:9008-9014 caps per entry, `SpawnerEntry.IsFull` here); no constructor arguments; 20 rows SmartSpawning (no counterpart, D-34's shape). `Generate()` builds plain `Spawner`s with `WalkingRange`, `SpawnLocationIsHome`, the delays in minutes, one entry per type, and respawns them |
| `Data/Decoration/Wrong/WrongMaze.cfg` (338) | `WrongDecoration.cs` (new, 370) | the 290 pieces as `Piece`s (type, id, x, y, z, facing), generated by script (`gen_deco.py`): 224 `WrongMazeWall`, 34 `WrongBarredMetalDoor`, 1 `BarredMetalDoor`, 31 `Static`. Placed the way pinned `Decorate` places them (Commands/Object Creation/Decorate.cs: a door built with its Facing then given the cfg's id, :1057-1059; a tile already holding that id at that z is skipped, :1203-1206). Carried as code because apply-patches.sh installs .cs files only (the P193 and S5 finding) |
| `Region.cs` (64) | `Region.cs` (150) | `WrongLevel3` (dies in level 3: to the cell, resurrected once, "You are captured by the jailor...") and `WrongJail` (`AllowHarmful` false), registered at `Initialize` by `WrongRegions` on both facets, parented to the static "Wrong" region (Main.cs loads regions.json before Initialize), priority 51 and 52 (Despise's rule). ServUO's are Regions.xml children; pinned's regions.json is data the build does not carry. `AllowHarmful` takes `(Mobile, Mobile)` here |
| `EnchantedHotItem.cs` (184) + `Items/Internal/ItemSockets/EnchantedHotItem.cs` (160) | `EnchantedHotItem.cs` (270) | `HotItemChest` (92 Lockpicking, a scroll plus 1-3 magic pieces hued 1258; a pick restocks ten minutes later; found unlocked at load, locks in five) and the curse as a saved registry (item to chest, one three-second timer, `GenericPersistence` "EnchantedHotItem"): 10-13 fire a tick in Wrong, "Ouch!" one in five, lifted when the holder is outside (by the tick, not ServUO's OnEnterRegion event). D-141, D-142, D-143 |
| `Items/BedrollSpawner.cs` (344) | same (330) | the 80 bedroll entries and the five tunnels; relays ten seconds after placement and every two hours; the next run saved and rebuilt after a load; generator lists for the bedrolls and tunnels |
| `Items/WrongBedrolls.cs` (209) | same (130) | `WrongBedrollBase` (a destination opens a tunnel; else the trap, the soap one in a hundred, or nothing), `WrongBedrollSouth` 0xA56, `WrongBedrollEast` 0xA55 |
| `Items/MysteriousTunnel.cs` (59) | same (40) | moves a player and pets to its destination |
| `Items/Soap.cs` (41) | same (22) | stackable, collapsed constructor pair |
| `Items/StinkingCauldron.cs` (57) | same (75) | bursts into 1-2 Gooey Maggots ten seconds in; `Map.GetSpawnPosition(center, range)` has no pinned helper, so a local one |
| `Items/WrongBarredMetalDoor.cs` (143) | same (115) | `ILockpickable` (pinned's: LockLevel, Locked, Picker, MaxLockLevel, RequiredSkill, LockPick) and `ITelekinesisable` re-implemented (pinned `BaseDoor.OnTelekinesis` is not virtual, BaseDoor.cs:107); picked or telekinesed at 100 Magery for ten seconds; loads locked. `IMageUnlockable` has no pinned caller: D-144 |
| `Items/WrongMazeWall.cs` (61) | same (45) | invisible until someone stands beside it; `LabelTo` for ServUO's AsciiMessage |
| `Items/Artifacts/BlanketOfDarknessArtifact.cs` (139) | same (140) | a bedroll hued 2076, rarity 8; sets pinned's `PlayerMobile.BedrollLogout`, the one flag pinned reads where ServUO reads `BedrollLogout || BlanketOfDarknessLogout` (PlayerMobile.cs:6179 there, :4013 here); the logout gump reproduced (pinned keeps Bedroll's private) |
| `Items/Artifacts/TortureRackArtifact.cs` (163) | same (95) | the two addons and deeds, rarity 10 per piece; `IArtifact` and `ShowArtifactRarity` have no pinned reader |
| `Mobile/Archmage.cs` (91) | same (90) | |
| `Mobile/BrigandCannibal.cs` (65) | same (50) | on stock `Brigand` |
| `Mobile/BrigandCannibalMage.cs` (66) | same (60) | on stock `EvilMage`; `AI_NecroMage` is pinned's `AI_Mage` (MageAI casts Necromancy from skill, Q-050); `SetSpecialAbility(LifeLeech)` is `MonsterAbilities.DrainLifeAttack` (D-40's mapping) |
| `Mobile/CaveTrollWrong.cs` (85) | same (55) | |
| `Mobile/DemonicJailor.cs` (181) | same (165) | range perception 15 carried; the hit that returns the victim to the cell, the walk-speed paralyze on casters, the terror freeze; `OnGaveMeleeAttack` / `OnDamagedBySpell` take a damage argument here; `SendSpeedControl` is NetState's |
| `Mobile/Fezzik.cs` (110) | same (95) | the cauldron on half the hits and spells; the recipe drop is D-145 |
| `Mobile/GooeyMaggots.cs` (175) | same (150) | slime on every tile left (not on the first placement, D-4), 3-minute life, 10-second slime, the walk-speed slow |
| `Mobile/HungryOgre.cs`, `LizardmanDefender.cs`, `LizardmanSquatter.cs`, `PrisonRat.cs`, `SavagePackWolf.cs` | same | the recipe's transformation; the wolf keeps `FightMode.Weakest` and its `TypeAlias` |
| `Mobile/WrongPrisoner.cs` (59) | same (50) | on pinned `BaseEscortable` with `ConstructQuestList` fixed to the one quest; `IsPrisoner` is BaseCreature's on both |
| `Quests/EscortToWrongEntrance.cs` (74) | same (45) | `BaseEscort` + `EscortObjective(QuestArea "Wrong Entrance")` + `ItemReward(1062577, Gold, 500)` on pinned's ML quest engine (the S5 route); registered at Configure against `WrongPrisoner`. The destination is the stock "Wrong Entrance" region of regions.json (both facets) |
| `Executioner` (2 XML rows) | stock pinned | `Mobiles/Monsters/Humanoid/Melee/Executioner.cs` |

### 1.2 Covetous Void Spawn, `Covetous Void Spawn\`

| ServUO file | Ours | What, and what changed |
|---|---|---|
| `Generate.cs` (402) | `Generate.cs` (280) | `[SetupNewCovetous` (refuses a second run) / `[DeleteCovetous`: the two controllers, the 7x7 pool (98 statics), the Cora spawner (home range 5, 1-1.5 h) and the Vela spawner in Cove, the two waypoint paths (9 and 10 points, linked), `ConvertSpawners` (the stock level 1-2 spawners in 5383,1845 125x115: gazer and gazer larva to StrangeGazer, headless one to HeadlessMiner, harpy to DazzledHarpy, stone harpy to VampireMongbat, through `SpawnerEntry.SpawnedName`, then respawn). All twenty waypoints tagged (ServUO forgets two; D-4) |
| `VoidPoolController.cs` (774) | same (640) | the battle (section 2.1). Saved: Active, RespawnMin/Max, the two waypoint lists, the level-3 spawner by reference. `Active`'s setter work is `ApplyActive`, run from the field's change hook and again after a load. `NoLootOnDeath` has no pinned member (a void spawn's loot is already nothing); `AForcedSacraficeQuest` is a Town Cryer quest (D-146). Also `VoidPoolGate`, `VoidPoolContextMenu` (the patch's target) and `VoidPoolInfo` (ServUO keeps the last in its points file) |
| `Region.cs` (137) | same (160) | `VoidPoolRegion : BaseRegion` at priority 51: the messages, the kill credit and the void artifact roll (0.1% + 0.1% a wave past ten), no loot on a void corpse, dungeon light, no stuck menu, no recall/gate/mark in. `CheckTravel` is BaseRegion's with the out message; `GetEnumeratedMobiles` is `GetPlayers` / `GetMobiles` |
| `Level3Spawner.cs` (359) | same (330) | an invisible item implementing pinned's `ISpawner` (which is an `IEntity`, Server/Interfaces.cs:56), held by the controller: the nine entries (rectangles, 8 or 15), rolled a void type, levels 5-15, re-rolled 2-5 minutes after emptying; kills split fame / 998 into the looters' overall totals. One generator list of creatures, each remembering its entry (`CovetousCreature.Level3Entry`) |
| `WaveInfo.cs` (22) | same (25) | |
| `VoidPoolStats.cs` (331) | same (300) | per-controller scoreboards and the record wave, saved through `GenericPersistence` "VoidPoolStats" (version 1 only: fresh content). `CheckAddTop20` copied as ServUO wrote it, see Q-1 in section 4 |
| `Gumps.cs` (251) | same (260) | `VoidPoolGump`, `ScoresGump`, `VoidPoolRewardGump`; a hued reward is built with its `CraftResource` when its type has that constructor (ServUO goes by index 0-23 over a list this port has trimmed) |
| `Gumps/BaseRewardGump.cs` (247), `Services/CommunityCollections/CollectionItem.cs` (138) | `server\customizations\Gumps\BaseRewardGump.cs` (230), `Services\CommunityCollections\CollectionItem.cs` (70) | two leaf ports the reward gump needs (ServUO's community collections, Clean Up and Huntmaster use them too): the paged reward list and its confirmation (`ConfirmRewardGump` over pinned `BaseConfirmGump`); the row record. `CollectionTitle`, `CollectionTreasureMap` and `CollectionSpellbook` belong to the community collections and come with them. Bounds from pinned `ItemBounds.Bounds`, 44x44 when there are none (ServUO measures the art) |
| `Creatures/CovetousCreature.cs` (250) | same (260) | the base: Level, VoidSpawn and Level3Entry saved; `SetPower` half a second in; the waypoint teleport; `GivesFameAndKarmaAward => false` reproduced by zeroing Fame and Karma around `base.OnDeath` (Titles.ComputeKillAwards reads them, BaseCreature.cs:3548; the region's OnDeath, which reads Fame for the score, runs first, Mobile.cs:4872-4873) |
| `Creatures/Abyss.cs`, `Repond.cs`, `Reptile.cs`, `Undead.cs`, `Elementals.cs` (206, 185, 187, 199, 192) | same | the 25 void creatures, each with the plain and the (level, voidSpawn) constructor. `AI_Necro` (DaemonMongbat, CovetousWyrm, plain constructor) is `AI_Mage`; LesserOni's `AngryFire` is D-147; the revenant's shroud and boots through our `SetWearable` extension |
| `Creatures/Common.cs` (185) | same (130) | DazzledHarpy, VampireMongbat, HeadlessMiner, StrangeGazer on their stock bases |
| `Creatures/Cora.cs` (362) | same (420) | section 2.3; `CoraManaDrainItem` top level for the generator |
| `Creatures/Vela.cs` (105) | same (70) | range perception 2 carried; the reward gump on double-click within five tiles |
| `Items/VoidPoolRewards.cs` (76) | same (60) | the reward list (13 rows of ServUO's 31: section 6) and `DropRandomArtifact` |
| `Items/BestWaveBoard.cs` (41) | same (35) | |
| `Items/BraceletOfProtection.cs` (64) | same (65) | on `BaseSetJewel` (the shard's carrier for `AbsorptionAttributes`; the final-parent rule) with `GoldBracelet`'s one member inlined. D-148 (Antique) |
| `Items/Brightblade.cs` (86) | same (40) | on `Katana`. D-149 (SplinteringWeapon), D-150 (gargish) |
| `Items/BlightOfTheTundra.cs` (115) | same (80) | on `CompositeBow`; the gargish one on `SoulGlaive`. D-148 |
| `Items/Hephaestus.cs` (115) | same (50) | on `HeaterShield`. D-148, D-150 |
| `Items/PrismaticLenses.cs` (93) | same (45) | on pinned `ElvenGlasses`, which is ServUO's `Glasses` base member for member (0x2FB8, the weapon attributes and their lines): the "already in ModernUO under another name" case. D-150 |
| `Items/CauldronOfTransmutation.cs` (387) | same (330) | the addon and deed; `VoidPoolDecay.Announce` is the smoke-and-message block ServUO repeats per reward |
| `Items/TemporaryForge.cs` (342) | same (330) | the addon and deed; `TreasureMap.ValidateLocation` has no pinned helper, so `IsOpenGround` reads the land and static tiles the same way |
| `Services/PointsSystems/VoidPool.cs` (72) | `Services\PointsSystems\VoidPool.cs` (35) | the points system on P33's framework (`Instance`, AutoAdd, the 1152649 message); `PointsType.VoidPool` added to `PointsSystem.cs:21-27` (the save writes names, so no renumbering) |
| `Mobiles/PlayerMobile.cs:2418-2429` | `server/patches/PlayerMobile-void-pool-context.patch` (new) | one hook line (section 2.4); registered at `docker/uo/apply-patches.sh:687-693` |
| `Server/Mobile.cs` SetWearable | `server\customizations\Misc\WearableExtensions.cs` (new, 30) | ServUO's `SetWearable(item, hue, dropChance)` as an extension; pinned Mobile has none |
| `server/tests/Services/Revamped Dungeons/WrongDungeon/WrongRevampedVerification.cs` (new, 6 facts), `.../Covetous Void Spawn/CovetousVoidSpawnVerification.cs` (new, 4 facts) | | section 3 |
| `CHANGELOG.md`, `VERSION` | | `## 2026.10.20.2` (Added x4, Staff x1); VERSION 2026.10.20.2 |

Every `new X(`, base class and overridden member was checked against pinned before the first build (the recipe's
dependency check); the 90 new type names were collision-checked against pinned and ours (all absent; `Hephaestus` is
not the shard's `HammerOfHephaestus`). Absent from pinned and resolved: `XmlSpawner` (pinned `Spawner`), `Decorate`'s
data files (a table), `WeakEntityCollection` (ours, CC4), `PointsSystem` (ours, P33), `ItemSocket` (a registry),
`IMageUnlockable`, `BaseEscort`/`BaseQuest`/`EscortObjective`/`BaseReward` (pinned's ML quest engine), `SetWearable`
(an extension), `Map.GetSpawnPosition` and `Map.GetRandomSpawnPoint` (local helpers), `TreasureMap.ValidateLocation`
(a local check), `BaseRewardGump`/`CollectionItem` (ported), `AI_Necro`/`AI_NecroMage` (`AI_Mage`), `SetSpecialAbility`
(DragonBreath is `FireBreath`, LifeLeech is `DrainLifeAttack`, AngryFire is dropped), `SetAreaEffect(AuraDamage)` +
`IAuraCreature` (`HasAura` + an `AuraDamage` override for the direct damage), `TeleportsTo` and its three siblings
(Cora's own `TryTeleport`), `IElementalCreature`, `NoLootOnDeath`, `GivesFameAndKarmaAward`, `IsStaff`,
`NegativeAttributes.Antique`, `SplinteringWeapon`, `[Alterable]`, `GargishKatana`, `LargePlateShield`,
`GargishGlasses`, `TownCryerSystem`, `Siege`, `RunicReforging`, `ExtendedWeaponAttributes`, `Mobile.Animate(AnimationType)`
(the classic six-argument call pinned Spell.cs makes).

## 2. How a player reaches it

### 2.1 The battle for the Void Pool (ServUO VoidPoolController, reproduced)

A controller per facet owns the Void Pool region (5383,1960 236x80 and 5429,1948 12x10), a one-second timer and the
level-3 spawner. Fifteen minutes after activation (and after every lost battle), while a player is in the region, a
battle begins: a void type is rolled (abyss, repond, undead, reptile, elemental) and waves of ceil(max(5, 2 sqrt(wave))
x 1.5) creatures, built at the wave's level, pour from the gates at 5592,2012 and 5466,2007 one every 0.75 s, each
homed on the pool with the nearest waypoint as its path. Wave two comes 10 s after wave one, later waves after 30-70 s
that shorten as the waves climb. A creature on the pool walls (5495,1993 10x10) has a 3 in 4 chance a second to hit
them, each hit a coin's chance of costing the pool one of 15 hits; at zero the battle is lost: the stats are tallied,
each player's credited waves become points (the stage, doubled on Felucca; the stage is wave / 5, at least 1 from wave
2), everyone credited is told waves and score (1152650), the survivors burn away, and the clock restarts. Score: a
kill is fame / 998 to everyone with looting rights (a pet's master counts); a cleared wave is stage x 125 to everyone
credited who is still in the region. A void spawn's death rolls the void artifact at 0.1% (+0.1% a wave past ten).

### 2.2 Covetous itself

`[SetupNewCovetous` retypes the stock level 1-2 spawners (section 1.2) and the controller empties and stops the
stock spawners in its region and in level 3 (5501-5627 x 1799-1927; ServUO `ResetLevel3Spawners`), whose population
the level-3 spawner replaces (nine entries, 8 or 15 each, levels 5-15, re-rolled after a wipe). A level-3 kill is worth
fame / 998 split between the looters, into the overall total. Cora spawns every 1-1.5 hours at 5457,1808; her death
hands a void artifact to a random damager three times in ten.

**Not done by this prompt, for Chase (section 8):** pinned's spawn import (`[GenerateSpawners`) would put the stock
Covetous and Wrong spawners back after a re-run, because `ClusterFDespiseStockSpawns.Admit` only excludes Despise. The
same seam can learn Wrong and Covetous when Chase decides; until then the generators are run after the import, as
the test world is built.

### 2.3 Cora

Fire breath (`GetMonsterAbilities => FireBreath`, the CC4 mapping); the aura: ServUO's `AuraDefinition` for Cora is
5 s, range 3, 10 damage, 100% direct (AreaEffects.cs AuraDefinition.Initialize) and her `IAuraCreature.AuraEffect`
drains a random share of the victim's mana (1153114); pinned's `AuraDamage` has no direct slot, so Cora overrides it
and deals the damage through `AOS.Damage`'s direct argument, then `AuraEffect`. Teleport: ServUO BaseCreature's
`TryTeleport` (BaseCreature.cs:7280-7362) brought over for Cora alone (every 30-60 s, always, players and pets within
16). The mana drain: every 15-120 s four cracks run north, west, south and east along a found path, each tile emptying
the mana of any player or pet it lands on or that steps on it, red for five seconds then gone.

### 2.4 The context-menu patch (`PlayerMobile-void-pool-context.patch`)

ServUO adds "The Void Pool" (1152531) to a player's own context menu while the player stands in the region
(PlayerMobile.cs:2418-2429), which is the only way to the scoreboards and the help text. Pinned `PlayerMobile`
overrides `GetContextMenuEntries` (PlayerMobile.cs:1857); a region has no context-menu hook and a partial class cannot
reach an override, so one line after `base.GetContextMenuEntries` calls `VoidPoolContextMenu.AddEntries(this, ref list)`
in customizations, which does the region test and adds `VoidPoolInfo`. Alternatives weighed, per
`docs/subsystem-policy.md`:

1. **No entry; reach the gump another way** (a command, or the best-wave board). A `[voidpool` player command is a
   wiki difference, and the board shows the record wave only. Rejected: the gump is how a player learns the rules.
2. **A context entry on the controller item or the pool statics.** The controller is invisible; the pool tiles are
   statics with no menu. Rejected.
3. **Patching the whole entry into PlayerMobile.** More patch surface than the hook. Rejected.
4. **The one-line hook (chosen).** Four added lines (three comments), after `BaseWeapon-trained-weapon-ability.patch`
   so its context is the fully patched tree; applied clean in every cycle of section 3.

## 3. Tests

Two fact files, run through the gate (`docker/uo/build.sh -t sl-modernuo:cc-P194`, `--tests-only` for the compile
cycles), the docker-build lock held throughout and released after. Logs `build-P194-cycle1.log` onward in the session
scratchpad. Free memory before cycle 1: 9.9 GB of 31.7 GB (the 2026-10-19 memory-kill rule).

`server\tests\Services\Revamped Dungeons\WrongDungeon\WrongRevampedVerification.cs`, six facts:

1. **GenerateBuildsTheDungeonAndDeleteRemovesIt**: a stock spawner (and its spawn), teleporter, barred door and sparkle
   in the rectangle are removed by DeleteOldWrong and one outside is not; Generate makes 38 spawners (19 per facet,
   10 prisoner rows), 126 requested, 68 capacity, every spawner full, every spawn the right type inside its rectangle
   on its facet, homed per the XML's IsHomeRangeRelative, every prisoner a WrongPrisoner; all 12 type names spawn
   (10 prisoners, 2 Fezziks, 6 jailors); every one of the 290 maze pieces stands on both facets, 224 invisible walls
   and 34 locked doors each; the two bedroll spawners lay 80 bedrolls and 5 tunnels eleven seconds in, the first
   three tunnels and their bedrolls linked both ways, the other two aimed at a room; 7 locked chests per facet at
   ServUO's tiles (92 Lockpicking, lock 82-91) each with a scroll and 1-3 hot pieces hued 1258; the 16 teleporters at
   their spots; a second run (delete, then generate) doubles nothing; DeleteWrongRevamp removes it all.
2. **Level3ReturnsTheDeadToTheirCellAndTheJailIsPeaceful**: the registered regions nest (jail in level 3 in Wrong,
   so the jail IsPartOf("Wrong")); the jail forbids harm, level 3 allows it; a dead player in level 3 is moved to the
   cell and resurrected once, a second death in a row is not, and leaving the region clears the memory.
3. **HotItemsBurnInWrongAndCoolOutsideAndTheChestRestocks**: a hot piece in the pack burns 10-13 on the tick inside
   Wrong and keeps its curse; outside, the next tick burns nothing, lifts the curse and the hue; the registry survives
   a save; a picked chest is open, then locked and restocked (old loot deleted, new loot hot) ten minutes later; the
   chest round-trips locked.
4. **TheCreaturesConstructRoundTripAndKeepTheirTricks**: the 13 creatures construct and round-trip (name, body,
   hue); Fezzik's name and title, the troll's name, the rat's hue, the jailor's perception 15, the wolf's Weakest and
   its TypeAlias, the cannibal mage's DrainLifeAttack and 94 Necromancy; maggots leave slime where they stood (gone in
   ten seconds) and die at three minutes; Fezzik drops one cauldron (not two within two minutes) that bursts into 1-2
   maggots beside him; the jailor's hit puts a player in the cell; his paralyze lasts fifteen seconds.
5. **TheItemsConstructRoundTripAndWork**: a bedroll with a destination round-trips, opens a tunnel on its tile and is
   gone; the tunnel moves the player and round-trips; a plain bedroll is torn, a far one refused; soap stacks; the
   maze door is locked (80/110/100), opens for ten seconds to a pick or to Telekinesis at 100 Magery, round-trips
   locked; the maze wall shows itself beside a player and hides again; every kind of decoration piece builds with its
   id; the blanket unrolls and rolls and keeps its hue; the torture rack is three labelled pieces with deeds each way.
6. **ThePrisonerOffersTheEscortToTheWrongEntrance**: the quest is registered, activated, an escort, with ServUO's
   five clilocs, one EscortObjective to the "Wrong Entrance" region and one 500-gold reward; a prisoner is a prisoner,
   invulnerable, titled, in plate, offers exactly that quest, and round-trips a prisoner.

`server\tests\Services\Revamped Dungeons\Covetous Void Spawn\CovetousVoidSpawnVerification.cs`, four facts:

1. **SetupPlacesTheControllersThePoolTheSpawnersAndThePaths**: two active controllers at 5605,1998,10 (60/90), the
   Void Pool region winning over the static Covetous region at the pool and in the alcove, 98 pool tiles (the corner
   1886 hued 1954, a centre star unhued, all at z 5), Cora and Vela on each facet from their spawners (1-1.5 h), the
   two paths at ServUO's points linked in order (9 and 10), the stock spawner's Gazer entry now StrangeGazer and
   respawned, the four name conversions; 86 leveled level-3 creatures (8 x 7 + 15 x 2) a second and a half in, each
   on the spawner, level 5-15, not void, inside the bounds, homed where it stands at range 20, each entry one void
   type and its creatures stamped with its index; a kill by a player (fame 5000) leaves the entry at 7 and credits 5
   to the overall total; an emptied entry is refilled with a different type after five minutes; the spawner
   round-trips active with its controller; DeleteCovetous removes it all and the static region returns.
2. **TheBattleSendsWavesScoresKillsAndEndsWhenTheWallsFall**: a controller with its paths and a player in the region;
   the context menu gets "The Void Pool" inside and nothing outside; fifteen minutes in, the battle starts: wave 1,
   two gates, then 8 void creatures of the rolled type at level 1 homed on the pool with waypoints, gates gone; wave 2
   ten seconds later; a kill (fame 1996) credits the wave, scores 2, gives the player no fame, leaves an empty corpse
   the region refuses to open; a creature on the walls brings PoolHits from 1 to 0 within two minutes: the battle
   ends, the clock restarts, the player has 1 point, the record wave is 2, best single and overall total are 2, the
   void spawn is gone; the three gumps build; the scoreboards round-trip through SerializeAll/DeserializeAll; the
   controller round-trips with its spawner, paths and settings.
3. **TheVoidCreaturesConstructGrowWithTheirLevelAndRoundTrip**: 25 distinct void types, each plain (level 60) and by
   (7, true), round-tripping Level, VoidSpawn and Level3Entry; a stage-12 creature is raised half a second in
   (Wrestling 123-133, physical 67-77, hits 2395-2400, strength 319-329, fame 8500); a void spawn gives no fame and
   an empty corpse, a level-3 one gives loot; the four retyped creatures; Vela blessed, invulnerable, perception 2,
   with her display pieces; Cora 35,000 hits, aura range 3, fire breath, the wild staff, the aura drains mana, the
   teleport pulls a player to her side and makes it her combatant, the mana drain lays cracks that are gone in
   eleven seconds.
4. **TheRewardsAndArtifactsAreSoldDroppedAndSaved**: 13 reward rows (8 cauldron deeds, Bronze first at 100, the
   gargish Blight last at 2515); 200 artifact rolls give all five types; Hephaestus (hue, Self Repair 5, physical 15,
   Parry 10, antique 250 / 255) round-trips; the bracelet has exactly one eater at 15 and keeps it; the Blight has a
   slayer, 100% fire, cold 15, and its glaive twin; Brightblade; the lenses; 400 points buy a Bronze cauldron deed
   (hued, 24 h) and a forge deed through the gump, leaving 50; the deeds round-trip and build their addons; an
   expired deed is gone within ten seconds; the best-wave board.

| Cycle | Tree | Result |
|---|---|---|
| 1 (`--tests-only`) | the port as first written | builder stage red, 5 compile errors: Vela.cs lacked `using Server.Mobiles`; pinned `ISpawner` also has `IsInSpawnBounds`; the generator emits public `WaypointsA`/`WaypointsB` and `Bedrolls`/`MysteriousTunnels` from the list fields, clashing with hand-written wrappers (the wrappers went); pinned `BaseDoor.OnTelekinesis` is not virtual (the door re-implements `ITelekinesisable`). The patch applied clean |
| 2 | | red, 9 more errors the first layer had hidden: `SetWearable` is our extension (`this.`); pinned `AOS.Damage` with direct damage is the `ignoreArmor` overload; `Movement.Offset` is `Server.Movement.Movement.Offset`; `BaseSetJewel` wants a Layer; `SendGump` is an extension in `Server.Gumps`; inside the `Server.Engines.VoidPool` namespace `VoidPool.Instance` names the namespace (`Engines.Points.VoidPool`) |
| 3 | | UOContent compiles; the test project red: a pattern over an unrelated type, and `Assert.Equal(0x190, Body)` picking the DateTime overload (`Body.BodyID`) |
| 4 | | the test project red on xUnit's analyzers: `Assert.Empty(x.Where(...))` is `Assert.DoesNotContain(x, ...)` (16 places) and `Assert.Single(x.Where(...))` takes the predicate (1) |
| 5 | | compiles; **1,559 tests, 1,547 passed, 8 failed, all eight mine**, each a finding: pinned `IsPrisoner` is not a saved field (restored after a load); the ten prisoner rows are 0x0 rectangles pinned bounds cannot hold (one tile); a void spawn's pack holds the gold `BaseCreature` packs in its own constructor, before `VoidSpawn` is set (emptied as it dies, what ServUO's `NoLootOnDeath` does); `Region.GetPlayerCount` counts connected players (the fact gives its player a test NetState); the level-3 creatures had already stepped off their spawn tile (homed within three); the `TypeAlias` is not resolved by `FindTypeByName` in the host; the hot-item tick asks `Player`; the hued cauldron deed came back `None` (probed in cycle 6) |
| 6 | | 1,559 tests, 1,548 passed, 7 failed: six mine, one the known `LootBoxFanfareVerification` flake (cc-P100, cc-P145). Mine: the generator's `fieldChanged` hook never ran the controller's Active work in the host (Active is now an explicit property over a plainly saved field); the level-3 kill points were computed in `Spawner.Remove`, which pinned `Mobile.OnDelete` reaches after the damage entries are gone (awarded from `OnDeath`); pinned `BaseAddonDeed` does not save its Resource (the deed saves its own); Cora's teleport and the region's player count both want a player (`Player = true` in the facts); the bedroll table is 80 rows, not 78 (counted in ServUO: my 78 was a guess); the maggots' first move left a slime from the round-trip spot |
| 7 | the six fixes | the harness reported the shell killed ("the system is running low on memory") at `#18 exporting layers`, and the first sitting stopped on that; **the log on disk shows the run finished**: 1,559 tests, 1,554 passed, 1 failed, the battle fact at a bare `Assert.True` |
| 8 (second sitting) | the WIP tree on the rebased branch (main at a1ed5f0, with P203 and P208) | 1,571 tests, 1,566 passed, 1 failed: the same battle fact, same bare assert (the Release PDB puts it at the fact's first line, so the line number named nothing) |
| 9 | messages on the fact's bare asserts and a state trace | the message named it: "the first battle is at most fifteen minutes ahead"; the trace read `next=21:18:44 now=20:58:39`, twenty minutes, with `players=1`. The controller is built on the test clock (five minutes ahead of real time after the first fact's advances), then `CreateTestNetState` sets `Core._now = DateTime.UtcNow` (D16) |
| 10 | the NetState made before the controller (a test-order fix; the port is unchanged) | **green: 1,571 tests, 1,567 passed, 4 skipped, 0 failed** (`build-P194-cycle10.log`) |
| 11 | the ten breaks of `p194_breaks.py` applied at once | **exactly the ten new facts red**, 1,557 passed, each on its own assertion: maggots "live three minutes" (W4), "the door locks again ten seconds after the pick" (W5), "the first death in level 3 is a resurrection in the cell" (W2), the hot-item tick InRange 10-13 got 0 (W3), spawn capacity expected 68 got 86 (W1), the quest title 1152096 got 1152097 (W6), the pool corner 1886 got 1885 (C1), wave one 8 creatures got 10 (C2), a void spawn's fame award 0 got 14 (C3), Self Repair 5 got 4 (C4). Restored from the pristine copies, `check` ALL PRISTINE, `git diff` of the folder empty against the cherry-picked index |
| 12 | the pristine tree, `-t sl-modernuo:cc-P194` (the full build) | red at the test gate, 2 failed, both the hot-item chest: `Assert.Contains(chest.Items, i => i is SpellScroll)` found `[Bonnet, RingmailGloves]` and a fresh chest's count InRange 2-4 got 1. Random: ServUO's `Loot.RandomScroll(0, RegularScrollTypes.Length, ...)` (EnchantedHotItem.cs:117) takes an inclusive maximum, so index 64 of a 64-entry table one roll in 65, and `Construct` returns null out of range on both engines (pinned Loot.cs:800-808, ServUO Loot.cs:1046-1054): a chest with no scroll. Fourteen chests a generate made it a one-in-five flake. Fixed: `Length - 1` (ours :240-244) |
| 13 | the scroll fix, `-t sl-modernuo:cc-P194` | **green through all three gates: 1,571 tests, 1,567 passed, 4 skipped, 0 failed; `sl-modernuo:cc-P194` built** (7629c2ce7647, 1.29 GB, label sl.commit=a1ed5f0 sl.dirty=1, 16:05 to 16:10; `build-P194-cycle13.log`) |

**Red proof: cycle 11.** Every one of the ten facts was first seen red in cycles 5 to 9 on its own assertions, and
then on its deliberate break (the table in `p194_breaks.py`, copied to the second sitting's scratchpad: a spawn entry
allowed one more, no resurrection in level 3, the curse burning outside, maggots living thirty minutes, a door open a
hundred seconds, the quest title swapped, the wrong pool corner, a wave a third larger, a void spawn giving fame,
Hephaestus repairing at 4), ten facts red and 1,557 green in one run, then green again on the restored tree.

## 4. Deviations and decisions for Chase

The register ends at D-122 in `docs\fidelity-principle.md`; D-123 to D-140 are proposed in cc-P66, P67, P71, P150 and
P193. These are proposed as D-141 onward; agents do not edit `docs\`.

| D | What | Why | Reverses when |
|---|---|---|---|
| D-141 | A stolen hot item shows no "Enchanted Hot Item" / "(Escape from dungeon to remove spell)" lines; its hue 1258 is the mark | pinned has no item sockets and no hook on a stock item's properties | item sockets, or a property hook on Item |
| D-142 | A stolen hot item dropped anywhere but the thief's pack stays where it is dropped (ServUO: "The stolen item magically returns to the trunk where you found it") | ServUO hooks Container.OnDragDrop and the four equipment types' OnRemoved; nothing additive reaches them | a drop hook, four patches |
| D-143 | The hot-item curse lifts within three seconds of leaving Wrong (ServUO: the instant of the region change) | the tick detects it; pinned has no enter-region event (the Despise finding) | an OnExit on the static Wrong region |
| D-144 | The Unlock spell does not open a Wrong maze door (ServUO: at 100 Magery, for ten seconds); Telekinesis at 100 Magery and lockpicking do | pinned Unlock.cs targets LockableContainers only (:45); `IMageUnlockable` has no pinned reader | an Unlock hunk for `ILockpickable` doors |
| D-145 | Fezzik does not drop the Three Tiered Cake recipe (ServUO: RecipeScroll 603, one death in ten) | neither pinned nor the shard's CookingCraftRegistrations has that recipe; a scroll for it would be a scroll for nothing | the 2016 cooking recipes land |
| D-146 | A lost battle does not complete "A Forced Sacrifice" | a Town Cryer quest (F-15, P64 design source), not on this shard | Town Cryer quests |
| D-147 | LesserOni (the plain level-60 one) has no AngryFire | Pet Training's `SetSpecialAbility(AngryFire)`, only in its plain constructor; no pinned ability | an AngryFire `MonsterAbility` |
| D-148 | The antique copies of the Bracelet of Protection, the Blight of the Tundra and Hephaestus (Vela's) have 250 maximum hit points and nothing else marks them antique | `NegativeAttributes.Antique` has no pinned or shard member | NegativeAttributes |
| D-149 | Brightblade has no SplinteringWeapon 20 | no pinned weapon attribute | the attribute exists |
| D-150 | No Gargish Brightblade, Gargish Hephaestus or Gargish Prismatic Lenses (so Vela sells no Gargish Hephaestus); the Gargish Blight of the Tundra is in | pinned has no GargishKatana, LargePlateShield or GargishGlasses; `[Alterable]` has no counterpart | the three bases |
| D-151 | Cora's aura fires every five seconds (ServUO: 40% of the ticks, `AuraDamage.TriggerChance`) | pinned `AuraDamage` has no chance | a chance virtual, a patch |
| D-152 | Cora's mana-drain cracks are not resisted by a Town Cryer mysterious potion | not on this shard | Town Cryer |
| D-153 | Cora's Siege-shard artifact roll (`OnKilledBy`) is absent | the shard is not Siege | never |
| D-154 | The escort's compassion is pinned's `HumanInNeed` award (400 for a prisoner) rather than ServUO's `BaseReward("Compassion")`; the reward list shows "500 Gold" (1062577) as the one row | pinned's BaseEscort shape; the gain is the same virtue | never |
| D-155 | The hot-item chest's loot is plain magic loot: no RunicReforging roll, no AssassinHoned | the D-38 shape (Shame's chests); no pinned member | RunicReforging |
| D-156 | Void Pool points have no loyalty-gump title (ServUO: 1152531) | P33's framework has no loyalty gump | the gump lands |

Five ServUO bugs fixed rather than copied (the D-4 rule: a bug that makes something broken is fixed), each one line:
`DeleteOldWrong` also removes a `BedrollSpawner`, so a second `[GenWrongRevamp` does not lay a second set of bedrolls;
Gooey Maggots leave no slime at the map corner on their first placement; all twenty Void Pool waypoints are tagged
for `[DeleteCovetous` (ServUO forgets two); a void spawn still waiting at its gate when the battle ends is dropped;
the hot-item chest's scroll roll stops at the last scroll instead of one past it (one chest in 65 had no scroll).
One ServUO reading copied as it is and raised as a question:

- **Q-1 (CheckAddTop20).** ServUO's top-twenty table, when a finished battle beats one of the twenty, removes the lowest
  of the twenty and adds the one it beat back, never the new battle (VoidPoolStats.cs:200-215 there; ours :90-108).
  No gump reads the top twenty. Copied, not fixed; say if you want the new battle stored instead.
- **Q-2 (the gate spawn point).** ServUO's `SpawnWave` picks each creature's spot as `start.X + RandomMinMax(start.X - 4,
  start.X + 4)` (VoidPoolController.cs:253-254 there, ours :344-345): twice the gate's coordinate, off the map, so
  `CanSpawnMobile` always refuses and every creature stands exactly on its gate. Copied as written (nothing is
  broken by it: the creatures spawn and march); say if you want the eight-tile scatter ServUO evidently meant.

Decisions for Chase:

1. **The stock spawners after a re-import** (section 2.2): extend `ClusterFDespiseStockSpawns.Admit` to Wrong and
   Covetous, or keep running the generators after `[GenerateSpawners`.
2. **The Blanket of Darkness and the Torture Rack drop nowhere yet** (ServUO puts them in Wrong's loot through files
   outside this row). Say where they should drop, or leave them to a loot prompt.
3. **The four harvest rewards** (section 6) are the second sitting; they decide whether Vela's list is complete.

## 5. Client check

Every tile id both rows use was read from the 7.0.116.0 UOAlive copy's tiledata (`D:\UO\UOAlive\UOAlive 7.0.116.0`,
the newest client data this desk may read; the shard's 7.0.117.0 is another desk; `tilecheck.py` in the session
scratchpad): the bedrolls 0xA55-0xA57, the maze walls and arches 0x241-0x24A, the barred metal doors 0x685-0x693, the
tunnel 0x1B71, soap 0x1422, the cauldron 0x142A, the torture rack 0x4AA0-0x4AAD, the chests 3648-3649, the sparkle
0x375A, the wall 0x31A, the spawner and controller gravestones 3796 and 3803, the slimes 0x1645 and 0x122A-0x122F,
the pool's stairs 1873-1888 and stars 8511-8516, the gate 0xF6C, the waypoint 0x1F14, the board 7774, the reward
pictures 0x9ED, 0x14EC, 0x2F5A-0x2F5B, 0xFB1, 5366, 0x1086, 0x1B76, 0x4204, 0x26C2, 0x090A, 0x2FB8, the cracks
6913-6920, the shroud 0x2683, the hairs 0x2045 and 0x203C, the effects 0x36BD, 0x113A, 0x3728, 0x3779, 0x376A: all
named. Every body (319, 125-126, 53-54, 238, 225, 400-401, 1, 35-36, 39, 4, 777, 241, 9, 13-16, 162, 17, 42, 76, 202,
206, 60-62, 106, 3, 147, 154, 24) is in mobtypes.txt. The Wrong revamp is decoration items on the stock map and the
Void Pool is statics; neither row needs a map, statics or multi change. **Blocked on client data: nothing.**

## 6. Left for the next prompt

| Piece | ServUO files | Why not this sitting | Cost |
|---|---|---|---|
| Harvest Maps | `Items/HarvestMap.cs` (302) + `Data/HarvestLocs/*.cfg` (12 files, 220 KB of coordinates) | a hook in Mining's and Lumberjacking's `GetResourceType` (ServUO Lumberjacking.cs:221) and the location tables as data the build cannot carry | medium: two pinned patches, the tables as code |
| Smelter's Talisman | `Items/SmeltersTalisman.cs` (158) | a hunk in ore smelting (ServUO Ore.cs:319: a hued talisman on the Talisman layer eases the smelt) | small: one patch |
| Woodsman's Talisman | `Items/WoodsmanTalisman.cs` (177) | a hunk in `HarvestSystem.FinishHarvesting` (ServUO HarvestSystem.cs:194: 2-5 extra boards) | small: one patch |
| Magical Fish Finder | `Items/MagicFishFinder.cs` (280) | the schools and the "school" bonus in the High Seas `FishInfo` (P193's D-133), which is on branch P193, not on main yet | small, after P193 merges |

Each is a Void Pool reward (eight maps, eight talismans, the finder: 17 of ServUO's 31 rows) and each would cost
points and do nothing without its hook, so the reward list carries the 13 rows that work (section 1.2). Nothing else
of the two rows is left: Wrong is whole.

## 7. Headless boot

**Done, two boots, both clean** (second sitting, 16:11 to 16:12, under the test-shard lock). Prepared in the first
sitting's scratchpad and run from there: a 29 MB copy
of the overnight bot's scratch world (`boot/world/Saves`, Backups and Archives beside it so the save can rename
over the parent as the compose file mounts it, cc-P37), a copy of the bot shard's `Configuration` set to
`listeners 127.0.0.1:2595`, `serverListing.address 127.0.0.1`, `autosave.enabled False` (pingServer left on, the
CC3 trap), and `boot.sh <n>`, which runs `sl-modernuo:cc-P194` on them with the 7.0.116.0 UOAlive client folder,
loopback only, no port published, waits for `Loading world done`, stops with `docker stop -t 90` (the D36 shutdown
save) and greps the log. Boot 1 (fresh, `boot-P194-run1.log`): client 7.0.116.0 detected, `[ShardVersion] Shattered
Legacy 2026.10.20.4 (106 version(s) in the changelog)`, `Loading world done (210942 items, 35148 mobiles) (3.47
seconds)`, listening on 127.0.0.1:2595, `Saving world done (0.09 seconds)`, `[SaveOnShutdown] ...saved in 1012 ms`,
`Shutting down`. Boot 2 on boot 1's save (`boot-P194-run2.log`): `Loading world done (212779 items, 35335 mobiles)
(2.28 seconds)`, saved in 1154 ms, shut down. Zero `Exception` and zero `Error` lines in either log; the one WRN in
each (`Command stats already registered to Stats_OnCommand`, ClusterFStatInspect.cs:18 against pinned's) is the
shard's standing warning since cc-P21, not this port's. Both containers were removed; the lock was released at
16:13. Nothing in that world is a type of this port; the one patched stock type (PlayerMobile) gains no field, so no
migration JSON is needed.

## 8. For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these. Then, as admin: `[GenWrongRevamp` and
`[SetupNewCovetous` once each (the test world is built by the importer first; both commands clear the stock spawners
they replace). To try it in game:

1. **Wrong, the maze:** `[go 5703 639 0` (the level-3 cell, Trammel). Walk the corridors: the walls appear as you
   come beside them and vanish behind you; the barred doors say "It appears to be locked" until you pick one (100
   Lockpicking, the lock is 80-110) or cast Telekinesis at 100 Magery, and lock again ten seconds later. The Demonic
   Jailor's hit returns you to the cell ("You are captured by the jailor and returned to your cell"); die in level 3
   and you wake in the cell once.
2. **Wrong, the cells and bedrolls:** `[go 5651 555 20` (the upper cell block). Double-click bedrolls: most tear
   ("You tear the bedroll to pieces but find nothing"), half of those set off a trap (40 fire), one in a hundred gives
   soap, and three to five of the 80 open a mysterious tunnel to the outside; the five holes outside the blocks
   (`[go 5670 550 22`) lead back in. The prisoners offer "We Who Are About To Die": escort one to the entrance
   (`[go 2042 226 0`) for 500 gold.
3. **Wrong, the hot items:** `[go 5707 662 0`. Pick a chest (92 Lockpicking), take a hued piece: every three seconds
   it burns 10-13 ("Ouch! These stolen items are hot!" now and then) until you step out of the dungeon ("The curse is
   removed from the item you stole!" and the hue goes). Fezzik the Ogre Cook (`[go 5690 534 0`) drops a stinking
   cauldron when hit; it bursts into Gooey Maggots that leave slowing slime.
4. **Covetous, the Void Pool:** `[go 5500 1998 5` (the pool, Trammel). Your own context menu has "The Void Pool":
   the facet, the next battle's minutes, three scoreboards and the rules. Wait there fifteen minutes: "The battle for
   the Void Pool is beginning now!", gates open at both ends of the cave and waves march the paths to the pool. Kill
   what you can; when the walls fall ("Cora's forces have destroyed the Void Pool walls") you are told your waves and
   score and get your points ("For your participation in the Battle for the Void Pool on Trammel, you have received
   N reward points"). A void corpse cannot be opened ("There is no loot on the corpse").
5. **Covetous, level 3 and Cora:** `[go 5574 1859 0`: leveled void creatures of one type per room, Rich loot; Cora at
   `[go 5457 1808 0` (35,000 hits): fire breath, a mana aura ("Cora drains N points of your mana!"), she pulls you to
   her side, and cracks run across the floor that empty your mana.
6. **Vela:** `[go 2254 1207 0` (Cove, Trammel). Double-click her: the reward gump with your points; `[add
   BraceletOfProtection` and the other artifacts to see them; a Cauldron of Transmutation deed placed in a house
   turns three bronze ingots into one gold (target them within three tiles); a Temporary Forge deed builds a forge
   outside a house that you can chop.
7. **Test world boot:** done by CC on a scratch copy (section 7).

## Play-test items added

Through the For Chase list above; Who and steps in `testing/bot-triage.md` (P194 group) and `testing/playtest-steps.json`:
P194-1 BOT-PARTIAL (the maze), P194-2 BOT-PARTIAL (bedrolls and the escort), P194-3 BOT (hot items, Fezzik), P194-4 BOT
(the battle), P194-5 EYES (level 3 and Cora), P194-6 BOT-PARTIAL (Vela and the rewards), P194-7 CC (test world boot, done:
section 7). `tools/tests/test_play_who.py` has two pre-existing failures (open items M-001, P163-0, P164-0,
P165-1 and others with no Who, none of them P194's); the P194 rows and steps are in both files.

## Repo size rule

No new file over 5 MB: the largest is `WrongDecoration.cs` at about 25 KB. Scratch (the two generators, the tile
check, the break script, the pristine copies, the patch work tree, the build logs) is in the session scratchpad,
outside both repos.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -Branch golem/Bronze/P194 -CodeRepo D:\UO\golems\Bronze\ShatteredLegacy
-DocsRepo D:\UO\golems\Bronze\shard-migration`, run last at 2026-10-20 16:13 (second sitting), after the final edit of
every file. Neither repo BLOCKED. No file over 5 MB in either repo (find -size +5M: none). Every file this prompt
wrote is ASCII (scanned by script, both sittings); README.md and dashboard.html, progress.py's output, carry the
non-ASCII lines that HEAD already has. The docker-build lock (15:50 to 16:10) and the test-shard lock (16:10 to
16:13) were released; the first sitting's locks were released at its end; no package or haven lock was needed;
nothing was placed in any world and no live config was changed. The docs repo's README.md, dashboard.html,
expansion-coverage.json and progress.json are progress.py's output (`SL_SHARD` at the Bronze copy; port list 501 of
983, the two rows 26/26 and 25/29).

```
=== code  (D:\UO\golems\Bronze\ShatteredLegacy) ===
  64 file(s) pending:
    CHANGELOG.md
    VERSION
    docker/uo/apply-patches.sh
    server/customizations/Services/PointsSystems/PointsSystem.cs
    server/customizations/Gumps/BaseRewardGump.cs
    server/customizations/Misc/WearableExtensions.cs
    server/customizations/Services/CommunityCollections/CollectionItem.cs
    server/customizations/Services/PointsSystems/VoidPool.cs
    server/customizations/Services/Revamped Dungeons/Covetous Void Spawn/... (26 .cs)
    server/customizations/Services/Revamped Dungeons/WrongDungeon/... (26 .cs)
    server/patches/PlayerMobile-void-pool-context.patch
    server/tests/Services/Revamped Dungeons/WrongDungeon/WrongRevampedVerification.cs
    server/tests/Services/Revamped Dungeons/Covetous Void Spawn/CovetousVoidSpawnVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\golems\Bronze\shard-migration) ===
  7 file(s) pending:
    README.md
    dashboard.html
    testing/bot-triage.md
    testing/playtest-steps.json
    tools/expansion-coverage.json
    tools/progress.json
    notes/cc-P194-port-wrong-and-covetous-void.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

## 9. What the second sitting ran

The finishing commands the first sitting left are done, in this order, from `D:\UO\golems\Bronze\ShatteredLegacy`
with the docker-build lock (15:50 to 16:10) and then the test-shard lock (16:10 to 16:13):

1. Cycles 8 to 10, `build.sh --tests-only` (cycle 8 untagged, 9 and 10 `-t sl-modernuo:cc-P194` so the builder
   image is `sl-uo-builder:cc-P194`, nobody else's): the battle fact's trap found and fixed; green at cycle 10.
2. The red proof, cycle 11: `python -I p194_breaks.py break`, the gate, `restore`, `check` ALL PRISTINE.
3. The full build, cycles 12 and 13 (`build.sh -t sl-modernuo:cc-P194`): the scroll flake found and fixed at 12,
   the image at 13.
4. The two headless boots, `boot.sh 1` and `boot.sh 2`, section 7.
5. `SL_SHARD=D:/UO/golems/Bronze/ShatteredLegacy python tools/progress.py` in the docs repo (port list 501 of 983,
   4 of 16 systems in; Wrong 26 of 26, Covetous 25 of 29; the main the branch now sits on has the same totals the
   first sitting measured), `tools/tests/test_play_who.py` (18 tests, the same two pre-existing failures, M-001 and
   the P163 to P165 items with no Who or Where, none of them P194's), the dry run above, and this file.

What changed in the tree between the two sittings, all of it in files the first sitting wrote: the battle fact
makes its NetState before the controller (and its bare asserts carry messages and a state trace), and
`EnchantedHotItem.SpawnLoot` rolls the scroll with `Length - 1`. CHANGELOG.md and VERSION carry `2026.10.20.4`.

P194 DONE
