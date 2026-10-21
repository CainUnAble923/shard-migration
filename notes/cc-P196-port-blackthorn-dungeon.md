# cc-P196: port Blackthorn Dungeon (revamped)

Written 2026-10-20 by the Bronze Golem (Fable), on branch golem/Bronze/P196 of both repos. Prompt:
`cc-prompts/claimed/Bronze/cc-P196-port-blackthorn-dungeon.md`. Both repos were clean at the start. Not committed: the
Golem commits after DONE. Pinned paths are relative to `D:\UO\ModernUO-pinned\Projects` (d4531cd9); ServUO paths to
`D:\UO\ServUO-pub57\Scripts`; "ours" is `server\customizations\Services\Revamped Dungeons\BlackthornDungeon` unless
said otherwise. One sitting, 2026-10-20 from 21:30 to 23:35 (Central).

## Headlines

1. **The row moves from 4 of 147 to 138 of 147 by the stem proxy, 145 of 147 counted by hand** (section 9). The
   "3 of 147" the port list opened with (4 by the time this prompt started) was never Blackthorn work: the proxy
   matched `Region`, `Generate`, `Gumps` and `Creatures` to Shame's, Despise's, Covetous's and Wrong's files of those
   names. Counted at the start: 0 of 147 were ported. The nine the proxy still reads as missing are the two invasion
   files (below) and the seven `RobeBearingTheCrestOfBlackthorn .cs` files, whose ServUO file name carries a space
   before `.cs`: ours are named without it, so the stem proxy never matches them. They are ported.
2. **Everything but the invasion is in.** The dungeon's 44 spawners and the 10 Agent of the Crown spawners
   (ServUO's two XmlSpawner files as a data table), the hitching post, the invasion-room doors, the New Magincia
   blockers and the Felucca castle teleporters (one command, `[GenBlackthorn`, and `[DeleteBlackthorn`); the two
   regions (the dungeon's reveal, gas-cloud throw and recall ban; the castle's spell, mount and pet rules); the
   Blackthorn points system on P33's framework with its kill tally and Minax artifact roll; the Agent of the Crown
   (a turn-in NPC: the base is a leaf port) with his turn-in gump and reward gump; the 132-row reward list; the 136
   crest items (generated from ServUO's sources by script, section 1.3), the two paintings and the Decorative Shard
   Shield deed with its picker and placement; and the invaders and invader captains as creatures. Six leaf
   dependencies ServUO keeps elsewhere came with it: the Epaulette, Gargish Fancy Robe, Gargish Sash, Gargish Cloth
   Wing Armor and Gargoyle Half Apron clothing types, the Dungeon Hitching Post and the turn-in NPC base.
3. **Left for the next prompt: the invasion itself** (`InvasionController.cs`, `InvasionBeacon.cs`; section 6).
   Minax's Beacon is a ServUO `DamageableItem`, an item players attack, and pinned ModernUO has no attackable item:
   `IDamageable` has zero definitions, `Mobile.Combatant` is a `Mobile`, and every weapon swing and spell targets a
   Mobile. That is a core seam, not a content port, and it needs Chase's decision (section 4, decision 1). The
   invasion's creatures, its definitions and the Minax artifact it awards are in, so the next prompt is the
   controller, the beacon and the hook already marked in `Region.cs`.
4. **Where the port met the shard's rules and what ServUO has that pinned lacks** (section 4): no reforging, so the
   crest items name themselves through an `AddNameProperty` override that writes exactly ServUO's cliloc line, and
   the Minax artifacts are a registry plus the Minax hue and a Name string, with ServUO's budget arithmetic reproduced
   over pinned's runic property tables (F-27's Self Repair rule holds because it is the shard's random-loot path);
   thirteen hats lose Hit Lower Defense 30 (pinned armour and clothing carry no weapon attributes); the invaders'
   eight AIs fold onto pinned's two; the Town Cryer hooks (Fellowship, A Visit To Castle Blackthorn) are dropped.
   Nothing touches the 200 skill cap, loops, guild skills, loot boxes, Clean Up or the Bestiary.
5. **Client check: nothing blocked** (section 5). Every item id the row uses is named in the client's tiledata, and
   both facets' dungeon rectangle and the Trammel castle carry their Publish 86 statics in the client map data.
6. **Deviations** (section 4, proposed D-157 onward): the thirteen Hit Lower Defense hats; the Minax artifact's
   properties and name; the invaders' AIs, stealth and aura cadence; the Fellowship and castle-quest hooks; no
   `SmartSpawning`; the shard-shield deed's `CanBeWornByGargoyles`-style drops. Two ServUO values corrected rather
   than copied, each argued: a return teleporter's z and a duplicate re-run.
7. **The gate is green and the image is built** (section 3): the suite is 1,753 tests, 1,749 passed, 4 skipped
   (pinned's), 0 failed (cycles 5 and 8); cycle 7 (the red proof, all six breaks at once) turned exactly the six new
   facts red and nothing else; cycle 8 built `sl-modernuo:cc-P196` through all three gates; two headless boots on a
   scratch copy of the bot world loaded and saved clean (section 7). The first red proof (cycle 6) caught two facts
   of mine comparing against the port's own constants and one flaky count; all expected values are literals now.
8. **For the integrator:** `CHANGELOG.md` gains `## 2026.10.20.21` above main's committed `## 2026.10.20.20` and
   VERSION becomes 2026.10.20.21. P195 (Exodus, branch golem/Bronze/P195, not yet in main) carries `2026.10.20.17`;
   if it lands first this section takes the next number and VERSION follows; nothing else in it depends on the
   number. `Services/PointsSystems/PointsSystem.cs` gains one enum member (`Blackthorn`), the one shared file touched.

## 1. What was ported, with file:line

All under `server\customizations\Services\Revamped Dungeons\BlackthornDungeon\` at ServUO's own paths unless said
otherwise, so apply-patches.sh mirrors them into `Projects/UOContent/Services/Revamped Dungeons/BlackthornDungeon/...`.
Line counts are the ported files'.

### 1.1 The dungeon

| ServUO file | Ours | What, and what changed |
|---|---|---|
| `Region.cs` (231) | `Region.cs` (350) | `BlackthornRegions` registers both at Initialize (the P194 shape: pinned's regions.json has neither; checked, no region touches the dungeon rectangle on either facet, and Britain's Trammel TownRegion (1416,1498 to 1740,1777) meets the castle's southern strip, which is why ServUO's castle is priority 51). `BlackthornDungeon : DungeonRegion` (6151,2301 413x539, both facets, priority 50): every five seconds a hidden player is revealed and a player south of y 2575 idle two minutes is thrown to one of eight spots in a gas cloud (lethal poison, 500855, the nearby idle creatures set on them); `CheckTravel` allows TeleportFrom/To only; `OnDeath` of a creature hands every damager with looting rights to the points system (:216) and marks where the invasion controller's hook goes. `BlackthornCastle : GuardedRegion` (Trammel, three rectangles, priority 51): no spell or ability (502629 / 1062075 / 1062938), riders dismounted with a 30-second remount block (1153052), pets auto-stabled (1153050) or sent outside (1153053). `GetEnumeratedMobiles` is `GetMobiles`; `AIObject.MoveTo` is `(mobile, range)`; `PlayerMobile.Stabled` is a HashSet made by `AddStabled`; the tick is a `DelayCallTimer` the registry stops on Unregister |
| `Generate.cs` (117) | `Generate.cs` (150) | `[GenBlackthorn` / `[DeleteBlackthorn` (`GenerateBlackthornDungeon`, `ShardCommand` WorldGeneration Replaces / WorldRemoval): per facet the `DungeonHitchingPost` at 6428,2677, eight `MetalDoor`s, sixteen `Blocker`s; on Felucca the nine `Teleporter`s (five in, four back); then the spawners. Tagged "blackthorn" in `WeakEntityCollection`; the command deletes its earlier run first (ServUO's doubles on a re-run). The Trammel castle teleporters are stock: pinned `Data/teleporters.json` carries both directions (castle 1477,1471-1475,-8 to 6432,2677-2681,0; landing 6440,2677-2681,20 back), the "create world teleporter section" ServUO's comment relies on |
| `RevampedSpawns/BlackthornDungeonCreature.xml` (1,850) + `BlackthornDungeonAgent.xml` (422) | `BlackthornSpawns.cs` (new, 150) | the 54 rows as `Definition`s, generated by script (`gen_spawns.py`, `gen_spawn_file.py`): 44 dungeon rows (22 per facet, the same multiset, 60-150 s delays, SmartSpawning on all), 10 Agent rows (nine Felucca cities, one in the Trammel castle, 5-10 minutes); 208 creatures requested, 208 possible (104 a facet, the test derives it); every type stock pinned (21) plus the Agent. `Generate()` builds plain `Spawner`s with `WalkingRange`, `SpawnLocationIsHome`, one entry per type, and respawns them |
| `Gumps.cs` (29) | `Gumps.cs` (25) | `BlackthornRewardGump` on the shard's `BaseRewardGump` (cc-P194), title 1154516, paying with `BlackthornData.Instance` |
| `BlackthornRewards.cs` (186) | `BlackthornRewards.cs` (180) | the 132 `CollectionItem` rows copied by script (`gen_rewards.py`): the shield deed and two paintings at 10, 129 crest items at 25/50/75/100 in ServUO's order. The seven Robe crest items are not in ServUO's list though the Agent displays them: copied as ServUO has it (Q-1, section 4). `IsTokunoDyable` kept |
| `Creatures/AgentoftheCrown.cs` (670) | same (240) | `AgentOfTheCrown : BaseTurnInMobile`: ServUO's four clilocs, the body, the clothes (our `SetWearable` extension), one of each crest item packed unmovable (a `Type[]` of 136 generated from ServUO's `InitOutfit` by `gen_agent.py`; ServUO writes 408 lines of `new X(); Movable = false; PackItem`), 1154517, `IsRedeemableItem` is `MinaxArtifacts.IsMinax`, `AwardPoints` to the points system and out of the registry. He wears a real `Epaulette` (leaf port) |
| `Services/PointsSystems/BlackthornData.cs` (115) | `server\customizations\Services\PointsSystems\BlackthornData.cs` (200) | on P33's framework, one more subclass: `PointsType.Blackthorn` added to `PointsSystem.cs:28-30`; the turn-in message 1154518; `DungeonPoints` saved after the base (version 0, own count); `ProcessKill` as ServUO's (fame / 2 x (1 + sqrt(luck) / 100) into the tally; chance A x 10^(B x tally); the artifact to pack, bank or feet with 1062317 / 1079730 / 1072523; the tally emptied); `OnCreatureDeath` walks pinned's `GetLootingRights` for the region hook (ServUO reaches it through `EventSink.OnKilledBy`, raised per damager with rights, BaseCreature.cs:6361-6420; pinned has no such event, and `CreatureDeathEvent` fires after `base.OnDeath`, while the region hook runs first, Mobile.cs:4872) |
| (ServUO `RunicReforging.GenerateRandomItem` with `ReforgedSuffix.Minax`) | `Items/MinaxArtifacts.cs` (new, 300) | section 2.2. Also the `[MinaxArtifact [budget]` staff command (ours) |
| `InvasionSpawner/InvasionDefinition.cs` (21) + the `InvasionType` enum of `InvasionController.cs` | `InvasionSpawner/InvasionDefinition.cs` (40) | the ten invasion kinds and the city definition record |
| `InvasionSpawner/Creatures.cs` (615) | same (560) | `Invader` and `InvaderCaptain`, section 2.3 |

### 1.2 The items

| ServUO file | Ours | What, and what changed |
|---|---|---|
| `Items/<15 Base dirs>/*.cs` (136 files, 6,870 lines) | same paths, same names (136 files, about 30 lines each) | generated by `gen_crest.py` (section 1.3): the recipe's transformation, `IsArtifact` dropped, `ReforgedSuffix.Blackthorn` replaced by `AddNameProperty => BlackthornCrest.AddName`, the version-0 Deserialize branches dropped (save upgrades); 7 `[Flipable]` to `[Flippable]`; 7 `IRepairable`/`RepairSystem` dropped (pinned Repair dispatches on BaseClothing); 7 `CanBeWornByGargoyles` dropped (pinned gates by RequiredRace alone, the cc-P129 reading); 13 `WeaponAttributes.HitLowerDefend = 30` dropped (D-157). Bases: pinned's Cloak, Robe, PlainDress, FancyDress, GildedDress, MaleKimono, FemaleKimono, BaseOuterTorso, Bandana, SkullCap, FeatheredHat, JesterHat, TricorneHat, WizardsHat, Bascinet, Circlet, RoyalCirclet, NorseHelm, PlateHelm, ChainChest, RingmailChest, PlateChest, DragonChest, Doublet, Surcoat, Tunic, Obi, WoodlandBelt, LeatherNinjaBelt, `GargishStoneChestType1` (ServUO's `GargishStoneChest`, 0x286; the recipe's gargish-stone note); the shard's GargishPlateChest, GargishEarrings, GargishGlasses (CC9) and GargishRobe (cc-P129); and the four leaf ports below |
| `Items/BlackthornCrest.cs` (new, 30) | | ServUO's `RunicReforging.AddSuffixName` for the Blackthorn suffix: one line, cliloc 1154548 with the name string (`#LabelNumber`, or the Name when set), as `BaseClothing.AddNameProperty` writes it (BaseClothing.cs:1016-1030 there) |
| `Items/BlackthornPainting.cs` (67) | same (30) | the two paintings, 1023744 |
| `Items/DecorativeShardShields.cs` (357) | same (300) | the shield (an `IAddon` and `IChoppable` house addon; re-deeded by the owner through pinned's `RewardDemolitionGump.DisplayTo`) and the deed (1153729, blessed) with the 27-shard picker (tooltips 1104344-1104370), the wall target, the east-or-south facing gump; `BaseHouse.Addons` is a `List<Item>` here. ServUO's picker condition accepts every shard button and is copied as written (its first half can never be true) |
| `Items/Equipment/Clothing/OuterTorso.cs` Epaulette; `Cloaks.cs` GargishFancyRobe, GargishClothWingArmor; `MiddleTorso.cs` GargishSash; `Waist.cs` GargoyleHalfApron | `server\customizations\Items\Equipment\Clothing\Epaulette.cs`, `GargishFancyRobe.cs`, `GargishClothWingArmor.cs`, `GargishSash.cs`, `GargoyleHalfApron.cs` (new, about 20 each) | five leaf clothing types pinned lacks (no clothing at 0x9985, 0x4002, 0x45A4, 0x46B4, 0x50D8; checked); the collapsed constructor pair; `CanBeWornByGargoyles` dropped as cc-P129 did. Carrier check (AGENTS.md): their only descendants are the crest items, none with a set or absorption member, so stock BaseClothing / BaseWaist is the final parent |
| `Items/Addons/DungeonHitchingPost.cs` (412) | `server\customizations\Items\Addons\DungeonHitchingPost.cs` (330) | the stable-and-claim post (30 gold, the trainer's refusals, Stable and Claim All entries, the stable and claim keywords, the claim list gump); `Allured` has no pinned member (the refusal is dropped: an allured pet is an ML charm, not on this shard); `PlayerMobile.Stabled`, `AddStabled`, `RemoveStabled` |
| `Mobiles/NPCs/BaseTurnInMobile.cs` (186) + `ShrineHealer.cs` (110) | `server\customizations\Mobiles\NPCs\BaseTurnInMobile.cs` (230) | the turn-in NPC base on pinned `BaseHealer`: Turn In (enabled while redeemable items are in the pack) and Claim entries, the shrine healer's Resurrect, Lock Karma and Tithe entries, no resurrection on approach; `TurnInGump` on pinned's `BaseImageTileButtonsGump` with its `ItemTileButtonInfo` (`HandleButtonResponse`: award, delete, reopen; `HandleCancel`: the cancel line). Pinned has no `OnClickDisabled`, so the disabled Turn In entry says nothing (D-166) |
| `server/tests/Services/Revamped Dungeons/BlackthornDungeon/BlackthornDungeonVerification.cs` (new, 6 facts) | | section 3 |
| `CHANGELOG.md`, `VERSION` | | `## 2026.10.20.21` (Added x6, Staff x2); VERSION 2026.10.20.21 |

Every `new X(`, base class and overridden member was checked against pinned before the first build (the recipe's
dependency check; the full creature and item name sweep is in the session transcript); the 152 new type names were
collision-checked against pinned and ours (all absent; `GargoyleHalfApron` and `Epaulette` are ServUO's own names).
Absent from pinned and resolved: `XmlSpawner` (pinned `Spawner`), `ReforgedSuffix`/`RunicReforging` (section 2.2),
`IDamageable`/`DamageableItem`/`Beacon` (section 6), `City` (CityLoyalty, only the controller needs it), `ShrineHealer`
(folded into the base), `ItemTileButtonInfo`/`BaseImageTileButtonsGump` (pinned's, in the Treasures of Tokuno),
`Allured`, `OnClickDisabled`, `UseSmartAI`, `CanStealth`, `AbilityProfile`/`SpecialAbility.Heal` (`CanHeal`),
`SetAreaEffect(AuraOfEnergy)` (`HasAura`), the six missing AIs (`AI_Melee`/`AI_Mage`), `CurseWeaponSpell.IsCursed`
(`BaseWeapon.Cursed`), `Map.GetRandomSpawnPoint` (not needed this sitting), `Utility.RandomSkinHue`
(`Race.RandomSkinHue`), `Insensitive.Equals` (`InsensitiveEquals`), `RealLuck` (`Luck`), `ColUtility`,
`Mobile.Stabled` (`PlayerMobile.Stabled`), `IsArtifact`.

### 1.3 The generator for the 136 crest items

`gen_crest.py` (session scratchpad) reads each ServUO file under `Items/*Base/`, takes the class name and base, the
`[Flipable]` attribute, the constructor's statements (dropping `ReforgedSuffix = ...`, `this.`, and the
`WeaponAttributes` line) and every `public override ... { get { return ...; } }` (dropping `IsArtifact`,
`RepairSystem`, `CanBeWornByGargoyles`), and writes the ModernUO file with the recipe's header, the `[Constructible]`
constructor (keeping a `: base(0x2683)` call where ServUO has one), the overrides as expression members, and the
`AddNameProperty` override. 136 in, 136 out; 109 files needed no drop, 27 had one (the seven robes' `IRepairable`, the
seven gargish epaulettes' `CanBeWornByGargoyles`, the thirteen Mace and Shield hats' `HitLowerDefend`). Six were read
by eye against their sources (an epaulette, the hooded robe, a Mace and Shield bandana, the gargish stone chest, a
Cloak of Silence robe, the doublet), a value diff over all 136 (every constructor assignment, skill bonus and
override value in the ServUO file found verbatim in ours, except the five dropped member names: 917 of 917), and
the test reads a sample of values from each base kind (section 3, fact 3).

## 2. How a player reaches it

### 2.1 The dungeon

Through Castle Blackthorn in Britain: on Trammel the rebuilt castle (1503,1377 and 1466,1407) whose stock teleporters
at 1477,1471-1475 drop into the dungeon landing at 6432,2677-2681 (and back from 6440,2677-2681); on Felucca the old
castle's 1517,1417-1420, whose teleporters `[GenBlackthorn` places. Pets cannot enter the Trammel castle (section 1.1,
the castle region), so the hitching post at the landing stables them for 30 gold. The landing opens onto the ruined
city rooms (the invasion rooms north of y 2575, each a city: Moonglow, Britain, Jhelom, Yew, Minoc, Trinsic, Skara
Brae, New Magincia, Vesper) and the dungeon proper to the south, where the 44 spawners stand: brigands in the western
rooms, hell hounds, skeletons and Exodus minions in the middle, liches, a balron, evil mages, giant spiders and golden
elementals east, the dragon room (dragons, drakes, a greater dragon) at 6405,2750, golems and their controllers, frost
oozes and snow elementals, rotting corpses, earth elementals, and giant rats and vampire bats at the south end.

### 2.2 The Minax artifacts and the Agent of the Crown (ServUO BlackthornData, AgentOfTheCrown, reproduced)

Every kill in the dungeon by a player with looting rights adds fame / 2 x (1 + sqrt(luck) / 100) to that player's
tally, and the chance that the kill hands over an artifact bearing the crest of Minax is 0.000863316841 x
10^(0.00000425531915 x tally): 0.09 percent at zero, one percent at 250,000, doubling every 70,700. A hit gives a
random weapon, armour piece, shield, jewel or hat (pinned's equipment pool draws hats, as ServUO's does) with a
Minax-sized roll of properties, hued 1157, and empties the tally.
The Agent of the Crown (in the Trammel castle at 1488,1473 and in Britain, Skara Brae, Magincia, Trinsic, Minoc,
Moonglow, Vesper, Yew and Jhelom on Felucca) takes them one at a time for one Blackthorn point each (1154518) and sells
the 132 rewards for 10 to 100 points through the reward gump, which shows the real properties of each reward from the
copy he carries.

**What ServUO's reforging did and what stands in for it.** ServUO builds the artifact with
`RunicReforging.GenerateRandomItem(item, killer, budget, luck, None, ReforgedSuffix.Minax)` (RunicReforging.cs:1893-2070):
a budget from the creature's difficulty (fame / 29, clamped 150..700; 700-800 for the invasion), a divisor, a
luck-weighted spread up to 500 above, 100 more on Felucca, the "powerful" threshold at 550 deciding the property
count (`GetProperties(5)` or 4..10 with the 2080-2160 weights) and the two intensity bounds; then its own loot tables
lay the properties on and a negative property may be added; the Minax suffix hues it 1157 and names it
"~1_ITEM~ of Minax" (1154507). `Items/MinaxArtifacts.cs` reproduces the arithmetic line for line (`Roll`, with the
divisor, `GetProperties` and the bounds as public statics the test reads) and lays the properties on with pinned's
`BaseRunicTool.ApplyAttributesTo` (the shard's random-loot path, so F-27's Self Repair rule holds); the item is hued
1157, remembered in a registry saved through `GenericPersistence` "BlackthornMinax" (a turned-in or deleted item leaves
it at the next save), and named "<Cliloc text> of Minax" when the server has the client's Cliloc text (pinned
`Localization`; the test host has none, so there the name stays the type's). The Agent asks `IsMinax(item)` where
ServUO reads the suffix off the four equipment bases. D-158 and D-159.

### 2.3 The invaders (ServUO Invader, InvaderCaptain)

Thirteen specialties (Swords, Fencing, Macing, Archery, Magery, Mysticism, Spellweaving, Bushido twice, Ninjitsu,
Chivalry, Necromancy, Poisoning) decide the AI, the race (elves for Archery and Spellweaving, otherwise three in four
human), the title ("the Swordsman", "the Swordswoman", "the wizard", "the sampire" for half the samurai), 120-170
strength, 800-1,250 hits, skills 100-120, resists 10-20 and the gear (ServUO's weapon lists per style, plate for the
paladin, chain for fighters, hat and robe for casters, the samurai's leather set with a lifeleech-100 blade for a
sampire, the ninja's poisoned belt and fukiyas, the assassin's lethal blade). A caster blasts everyone within four
tiles for 80-90 chaos damage under rings of black explosions one think in ten, at most every 30-60 seconds; a sampire
keeps Vampiric Embrace up and curses its weapon; all wear an aura of energy and their invasion's name (1154196 + type).
The captain: 250 strength, 8,000-12,000 hits, 48,000 fame, skills 105-130, resists 20-30, super boss loot, and two
Minax artifacts to the two highest damagers with rights within twenty tiles (1154530) when he dies. Pinned's AIs are
`AI_Melee` and `AI_Mage` (the recipe's standard substitution): `SpellCaster` is decided from the specialty, so stats,
gear and the special keep ServUO's split (D-160). `HasAura` carries the aura of energy with ServUO's numbers (30 s,
range 5, 20-30 energy, the 1072073 line, particles and sound) gated on the combatant within 3 (D-161).

## 3. Tests

One fact file, `server\tests\Services\Revamped Dungeons\BlackthornDungeon\BlackthornDungeonVerification.cs`, run
through the gate (`docker/uo/build.sh -t sl-modernuo:cc-P196`, `--tests-only` for the compile cycles), the docker-build
lock held throughout and released after. Logs `build-P196-cycle1.log` onward in the session scratchpad. Free memory
before cycle 1: 4.7 GB of 32 GB, the Docker VM holding 7.5 GB of page cache; the cache was dropped
(`docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'`) and Windows read 8.9 GB
available for the cycles. Every cycle was started detached (PowerShell `Start-Process` of `run-cycle.sh`) with its log
on disk, which paid off once: the harness stopped the session's waiting shell during cycle 7 ("the system is
running low on memory": 2.2 GB available, the Docker VM holding 12.4 GB of page cache again after six builds), the
build itself ran on, the cache was dropped a second time and the log was read when it finished.

1. **GenerateBuildsTheDungeonAndDeleteRemovesIt**: `Generate()` places 2 hitching posts at 6428,2677, 8 doors a facet
   at ServUO's spots, 16 blockers a facet, the 9 Felucca teleporters with their destinations (the corrected z 20, and
   none on Trammel), 54 spawners at their centres with ServUO's count, delays, walking range and home flag, each full
   (104 creatures a facet, derived from the table), every spawn on its facet inside its rectangle and of an allowed
   type with the entry's count, 22 types seen; 10 Agents (9 Felucca) titled, invulnerable, with the 136 display items
   unmovable in the pack and the 1154517 line; a second run replaces rather than doubles; Delete takes it all down,
   spawn included.
2. **TheRegionsRevealTheHiddenThrowTheIdleBanRecallAndTallyKills**: both dungeon regions and the Trammel castle
   register (idempotent), are found at their spots and not the castle on Felucca, priority 51, guarded; recall, gate
   and mark refused and teleport allowed in both, staff pass; a hidden player is revealed and an idle one south of
   y 2575 is thrown to one of the eight spots, lethally poisoned, with the move time stamped, while an idle one north
   of it stays; a rider stepping into the castle is dismounted and the horse and a pet are stabled into the player's
   set; Magic Arrow and Close Wounds are refused, staff cast; a Lich killed in the dungeon by a player with rights
   tallies fame / 2, the chance formula reads 0.0863 percent at zero and one percent at 250,000, a forced roll hands a
   hued, registered weapon, armour or jewel to the pack and empties the tally, a kill outside tallies nothing, and
   the points system round-trips its reward points and tally through `PointsSystemPersistence.WriteAll` / `ReadAll`.
3. **TheCrestItemsAndRewardsConstructRoundTripAndBearTheCrest**: all 136 display types construct, are hued, are
   clothing or armour, show the 1154548 line with `#LabelNumber` and not the plain name, and round-trip hue, id and
   layer; fourteen sampled values across the bases (the epaulette's graphic, layer, hue and 3/3/3; the gargish
   epaulette's race; the bandana's 45 strength, 20 physical, 255 hits, night sight; the doublet's 150 hits; the stone
   chest on `GargishStoneChestType1` with mage armor and lower requirements 100; the Cloak of Silence robe's Stealth
   10; the hooded robe's graphic and name; the sash, half apron, wing armor, fancy robe and earrings); the Epaulette
   leaf; the 132 reward rows (distinct, ServUO's first three and last, the five prices, 129 crest rows, the seven
   robes the only display types outside the list, `IsTokunoDyable`), each constructing; the paintings, the shield
   deed (blessed, 1153729, south id +27, 27 shards), the shield's facing and re-deed.
4. **TheAgentTakesMinaxArtifactsAndSellsTheCrest**: his context menu (Resurrect disabled alive, Lock Karma, Tithe,
   Turn In disabled with nothing to turn in, Claim); a Minax artifact is redeemable, a katana and a crest cloak are
   not; Turn In enables; the turn-in gump deletes the item, banks one point and drops it from the registry; too far
   away nothing happens; ten points buy the painting through `OnConfirmed` and leave none; 25 buy a crest tunic that
   bears the crest; an overdraft is refused; the Agent round-trips.
5. **TheMinaxArtifactRollFollowsServUOAndTheRegistrySaves**: the divisor and powerful threshold; `GetProperties`
   within its bounds over 300 rolls; 300 invasion-budget rolls each powerful (4-10 properties, 100 high, 50-70 low,
   budget 375-1250); 300 smallest-budget rolls within bounds; the Felucca bonus; the difficulty formula; fifty
   artifacts each a weapon, armour or jewel, hued 1157, registered, at least 45 carrying a property; the registry
   round-trips and forgets a deleted item; Mark and Remove.
6. **TheInvadersConstructRoundTripAndTheCaptainDropsTheCrestOfMinax**: 120 invaders (every type x every specialty)
   with the saved specialty and type, aura, heal and ability chance per style, the folded AI, a human or elven body,
   a title, 800-1,250 hits, skills 100-120, a weapon, boots, fame, the invasion line, elves where ServUO says, a
   weapon ability off the weapon, and a round trip of all three saved fields; the ninja's belt (20/20, greater) and
   two fukiyas and Stealth 100; the paladin's shield, plate, Parry 120 and bandages; the assassin's lethal blade with
   100 charges; the wizard's title, hat, caster flag, Magery and no bandages; the samurai's leather do and Parry 120;
   a sampire (title, Necromancy, Spirit Speak, lifeleech 100) and a swordswoman within 200 rolls; the captain's hits,
   fame, strength, skill floor, resists, type and round trip; killed by a player with rights, two Minax artifacts in
   the player's pack.

| Cycle | Tree | Result |
|---|---|---|
| 1 (`--tests-only`) | the port as first written | builder stage red, 1 compile error in 148 new UOContent files: `TithingGump` takes one argument here (ServUO's takes two). The fix had been written but a failed `&&` chain in the session skipped it |
| 2 | | UOContent compiles whole; the test project red on one line: a lambda over a `PooledRefList` (a ref struct) in the Agent fact; rewritten as a loop |
| 3 | | compiles; **1,753 tests, 1,748 passed, 5 failed, all five mine**, each a finding: two host traps (D27: the host has no tile data, so a weapon, shield or armour piece sits on `Layer.Invalid` and `Mobile.Weapon` is Fists; the invader fact now reads the items by type), one wrong assumption of mine (ServUO's 700-800 roll spreads down to half the base, so some rolls land under the powerful threshold and take 1-5 properties; the fact now branches on `IsPowerful`), one wrong sample (the Night Eyes earrings set no strength requirement; the Folded Steel ones do), and two older facts my files tripped: `SmithGuildNameVerification` scans every customization source for the smith guild's old name and found it in a Region.cs comment about ServUO's Town Cryer event (reworded), and `CC9CloseVerification` asserts the names CC9 declined still resolve to nothing, one of them `GargishClothWingArmor`, now a leaf port with a path (its row moved to a comment saying so, as the fact's own note asks) |
| 4 | the five fixes | 1,753 tests, 1,747 passed, 2 failed, both my facts and both one assumption: pinned's `Loot.RandomArmorOrShieldOrWeaponOrJewelry` draws hats (a Tricorne Hat and a Wizard's Hat came up), as ServUO's does; `MinaxArtifacts` already lays properties on a `BaseHat`, so the two type checks and the texts now say hat too |
| 5 | the two type checks | **green: 1,753 tests, 1,749 passed, 4 skipped (pinned's), 0 failed** (`build-P196-cycle5.log`) |
| 6 | the six breaks of `p196_breaks.py` (no Felucca teleporters; the idle throw at twenty minutes; the crest cliloc off by one; two points a turn-in; the Minax hue off by one; one captain drop) | **4 of 6 red, and a finding about the facts**: the crest and idle-throw breaks stayed green because those two facts compared against the port's own constants (`BlackthornCrest.BearingTheCrestOfBlackthorn`, `BlackthornDungeon.IdleMilliseconds`), which moved with the break; and the Minax fact went red on the wrong line, a count of powerful rolls I had floored at 200 of 300 when the true mean is 199 (two thirds of 750-base rolls reach 550; measured over 200,000 rolls of ServUO's arithmetic, sd 8). Every expected value in the fact file is now a literal, and the count is bounded six sigmas either way (150-248) |
| 7 | the six breaks again, on the literal-valued facts | **exactly the six new facts red**, 1,743 passed, each on its own assertion: the crest line read `1154547:#1025397` (fact 3), two points a turn-in (fact 4), the idle player still at the entrance (fact 2), one captain drop (fact 6), zero Felucca teleporters (fact 1), hue 1158 (fact 5). Restored from the pristine copies, `check` ALL PRISTINE, the folder untracked-only against the index |
| 8 (the full build, `-t sl-modernuo:cc-P196`) | the pristine tree | **green through all three gates: 1,753 tests, 1,749 passed, 4 skipped, 0 failed; `sl-modernuo:cc-P196` built** (`build-P196-cycle8.log`) |

## 4. Deviations and decisions for Chase

The register ends at D-122 in `docs\fidelity-principle.md`; D-123 to D-140 are proposed in cc-P66, P67, P71, P150 and
P193, D-141 to D-156 in cc-P194. These are proposed as D-157 onward; agents do not edit `docs\`.

| D | What | Why | Reverses when |
|---|---|---|---|
| D-157 | The thirteen Mace and Shield crest hats (Bandana, Bascinet, Circlet, Feathered Hat, Gargish Earrings, Gargish Glasses, Jester Hat, Norse Helm, Plate Helm, Royal Circlet, Skullcap, Tricorne Hat, Wizard's Hat ...2) have no Hit Lower Defense 30 | ServUO sets `WeaponAttributes.HitLowerDefend` on hats and helms through `BaseClothing.WeaponAttributes` / `BaseArmor.WeaponAttributes`; pinned's clothing and armour carry no weapon attributes | an `AosWeaponAttributes` on BaseArmor and BaseClothing (a patch and a save-layout change) |
| D-158 | A Minax artifact's properties are pinned's runic tables at ServUO's property count and intensity, never a negative property (antique, brittle, cursed) | pinned has no reforging; `BaseRunicTool.ApplyAttributesTo` is the shard's random-loot path (F-27) | RunicReforging |
| D-159 | A Minax artifact is named by a Name string ("katana of Minax") when the server has Cliloc text, and shows only the Minax hue (1157) when it has not (the test host); ServUO shows the 1154507 line | a stock weapon, armour or jewel has no additive hook on its name line, and the registry cannot write a property line | RunicReforging's suffix on the equipment bases, or a name hook on Item |
| D-160 | Invaders of the Ninjitsu, Bushido and Chivalry styles fight with pinned's `AI_Melee` (no stealth, no Bushido or Chivalry casting from the AI); the Mysticism, Spellweaving and Necromancy styles with `AI_Mage` (MageAI casts Necromancy from skill, Q-050; no Mysticism or Spellweaving spells) | pinned's `AIType` has no Ninja, Samurai, Paladin, NecroMage, Spellweaving or Mystic AI; `UseSmartAI` and `CanStealth` have no pinned member | the AIs |
| D-161 | An invader's aura of energy fires every 30 seconds while its combatant is within three tiles, on everyone within five (ServUO: an `AreaEffect` triggered from OnThink with a 30-second cooldown, so at most that often, and a one-in-ten think roll before the 30-60 s special) | pinned's aura is `HasAura` on `AuraInterval` | the Pet Training area effects |
| D-162 | The dungeon's gas-cloud tick runs whether or not the Fellowship event is on (ServUO skips it while `FellowshipData.Enabled`) | a Town Cryer event (F-15), not on this shard | Town Cryer |
| D-163 | Stepping north of y 1485 in the Trammel castle does not advance A Visit To Castle Blackthorn | a Town Cryer quest, not on this shard | Town Cryer quests |
| D-164 | No `SmartSpawning`: the 44 dungeon spawners run whether or not anyone is near | D-34's shape (pinned Spawner has no idle) | the same |
| D-165 | The Agent of the Crown's reward gump does not show his items' properties in the test host (no tile data); in the world it does, as ServUO's | D27, a host difference, not a shard one | never |
| D-166 | Clicking the greyed Turn In entry says nothing (ServUO speaks the cancel line, 1154519) | pinned `ContextMenuEntry` has no `OnClickDisabled` | the hook |
| D-167 | The hitching post accepts an allured pet (ServUO refuses, 1048053) | `Allured` has no pinned member and no allured creature exists on the shard | never |
| D-168 | The gargish crest robes, epaulettes, sash, half aprons and wing armor refuse humans and elves by `RequiredRace` alone (ServUO also sets `CanBeWornByGargoyles`) | pinned BaseClothing gates wear by RequiredRace alone (cc-P129's reading) | never |

Two ServUO values corrected rather than copied (the D-4 rule, a bug that makes something broken is fixed), each argued:

- **The fourth Felucca return teleporter's z.** ServUO's `Generate.cs:86` sends 1517,1420 to 6440,2680 at z 12; its
  three neighbours land at z 20 and the five inbound teleporters stand at z 20 on those very tiles (:63-75), so z 12
  would set the player eight below the landing floor at one tile of four. Ours lands at z 20 (`Generate.cs`, the
  header and the row's comment).
- **Re-running the generator.** ServUO's `[GenBlackthorn` places a second post, second doors and second spawners on
  a re-run; ours deletes its earlier placement first (the collection tag), as the Wrong and Covetous ports do.

One ServUO reading copied as it is and raised as a question:

- **Q-1 (the seven Robe crest items).** ServUO's `BlackthornRewards` lists 129 crest items and leaves out the seven
  `RobeBearingTheCrestOfBlackthorn1-7` (the Robe of each robe set), though `AgentOfTheCrown.InitOutfit` packs them
  for display and the files exist. Copied as ServUO has it: 132 rewards, the robes constructible by staff only. Say
  if you want them sold (their prices would be their set's: 25, 50, 75, 75, 75, 75, 100).

Decisions for Chase:

1. **The Minax Beacon, and so the invasion** (section 6). Three ways, costed:
   (a) An `IDamageable` seam in pinned: ServUO's `IDamageable` is implemented by Mobile and `DamageableItem`,
   `Mobile.Combatant` is an `IDamageable`, and `BaseWeapon.OnSwing/OnHit`, `Spell` targets, `AOS.Damage` and the
   AI's target selection all take it; a core patch of several hundred lines across Server and UOContent, the kind
   `docs/subsystem-policy.md` says to argue first. It would unblock every ServUO damageable (the Beacon, the Kotl
   doors, the Khaldun and Doom props, the siege engines).
   (b) A creature standing in for the beacon: a `BaseCreature` named "lighthouse" with the lighthouse statics placed
   around it, invulnerable until the captains fall (ServUO's `BeaconVulnerable`), 50/85/99/99/70 resists and the
   ItemLevel hits; players attack a mobile where ServUO's players attack an item. About a day, additive, and the
   invasion plays as ServUO's does except that the beacon has a health bar and a body (an invisible or a stone body
   would be the choice). The shard's own wiki would carry the difference.
   (c) Leave the invasion out: the dungeon, the tally and the Agent stand on their own, and the Minax artifacts come
   from kills alone (and `[MinaxArtifact` for staff).
   The continuation prompt in section 6 is written for (b) and takes (a) or (c) as a one-line change.
2. **Admit the Blackthorn spawners to the stock-spawn seam?** `ClusterFDespiseStockSpawns.Admit` knows Despise only;
   pinned's stock spawn files place nothing inside the dungeon rectangle (checked: zero spawners there on either
   facet in `Distribution/Data/Spawns`), so a re-import never touches it. No change needed; noted so nobody looks.
3. **The seven robes** (Q-1).

## 5. Client check

vseUOAware's `set_uo_directory` refused the UOAlive copy twice this session (a generic error; its saved directory is the
shard's 7.0.117.0 client data on another desk), so the check was done two ways: `inspect_map_coordinate` against the
tool's saved directory for one tile, and `tilecheck.py` (session scratchpad) reading the UOAlive 7.0.116.0 copy's
`tiledata.mul`, `staidx1.mul`/`statics1.mul` and `staidx0.mul`/`statics0.mul` directly (`D:\UO\UOAlive\UOAlive
7.0.116.0`, the newest client data this desk may read; the shard's 7.0.117.0 is one build newer and the Pub 86 content
predates both by a decade).

- **Items:** every id named in tiledata: the epaulettes 0x9985/0x9986 ("Epaulets Human/Gargoyle"), the paintings
  0x4C62-0x4C65 ("Landscape L/S 02"), the 27 shard shields 0x6380-0x639A ("AOL Legends Shield E" .. "Yamato Shield
  EAST") and their south twins 0x639B-0x63B5, the wing armor 0x45A4, earrings 0x4213, glasses 0x4644, half apron
  0x50D8, sash 0x46B4, the gargish robes 0x4000/0x4002, circlets 0x2B6E/0x2B6F, the chests 0x286, 0x30A, 0x2641,
  0x13BF, 0x13EC, 0x1415, the cloak 0x1515, the hooded shroud 0x2683/0x2684, the dresses and kimonos 0x1F01, 0x230E,
  0x1F00, 0x2783, 0x2782, the hats 0x1540, 0x140C, 0x171A, 0x171C, 0x140E, 0x1412, 0x1544, 0x171B, 0x1718, the
  doublet, surcoat and tunic 0x1F7B, 0x1FFD, 0x1FA1, the belts 0x2790, 0x27A0, 0x2B68, the deeds 0x14EF/0x14F0, the
  hitching post 0x14E7/0x14E8, the blocker 0x21A4, the lighthouse 18212/18223 and its damaged states 39299/39300 (for
  the next prompt), the rubble 632-635, 6571, 3118, 14732, 14742, the effects 14120, 4518, 14133, 14000, 14013,
  0x3709, 0x36CB. Every hue the row uses (2019, 1773, 1766, 2527, 1150, 2075, 0xE8, 2130, 2106, 1775, 1157, 1154,
  1166, 2018, 2498, 66) is below hues.mul's 3000.
- **Map:** the dungeon rectangle (6151,2301 413x539) holds 32,616 statics on Trammel and 32,589 on Felucca (stone
  walls, water, planks, shingles: the ruined cities); the Trammel castle rectangle holds 24,801 (the rebuilt castle:
  pavers, water, walls) against the Felucca old castle's 5,910; the landing tile 6430,2678 on Trammel is land 0x436
  at z 0 with no static (where ServUO's region puts its go point). The Publish 86 map is in the client. No multi is
  used.
- **Clilocs** could not be read by tool (the compressed Cliloc.enu, as cc-P195 found); every number is ServUO's and
  the play tests list the texts for the bot to confirm: 1154516-1154520, 1154530, 1154548, 1154571, 1154572, 1154507,
  1154517, 1154518, 1154196-1154205, 1153729, 1153050, 1153052, 1153053, 1104344-1104370, 1062075, 1062938, 502629,
  500855, 1072073, 1062317, 1079730, 1072523, 1123325, 1029863, 1023744, 1049780-1049784, 1042558-1042565, 1049668,
  1049677, 1049612, 502671-502679.

**Blocked on client data: nothing.**

## 6. Left for the next prompt

| Piece | ServUO files | Why not this sitting | Cost |
|---|---|---|---|
| The city invasions | `InvasionSpawner/InvasionController.cs` (647), `InvasionSpawner/InvasionBeacon.cs` (66) and their leaf dependency `Items/Damageable/Beacon.cs` (346) over `Items/Damageable/DamageableItem.cs` (664) | Minax's Beacon is an attackable item; pinned has no `IDamageable` seam (section 4, decision 1) | a day with the creature stand-in (b); a core patch for (a) |

Everything else of the row is in. Ready continuation prompt, written for decision (b):

> **CC task: Blackthorn Dungeon, the city invasions (cc-P196 sitting 2).** Port
> `Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/InvasionController.cs` and `InvasionBeacon.cs` onto
> `server\customizations\Services\Revamped Dungeons\BlackthornDungeon\InvasionSpawner\`, the Minax Beacon as a
> `BaseCreature` stand-in (Chase's decision (b), cc-P196 notes section 4): one controller item per facet at 6359,2570
> (`InvasionController.Initialize` makes them when absent), rolling a city (the nine `InvasionDefinition`s of
> `Initialize`, each four or five spawn rectangles and a beacon spot; the `City` enum's nine members are a leaf
> port, `Services/City Loyalty System/CityLoyaltySystem.cs:15-26`) and an `InvasionType` (never the last of either),
> placing the beacon, shuffling the zones, and spawning two waves of 8-10 creatures of the type's table plus three
> `Invader`s and a blessed `InvaderCaptain` per zone (`SpawnWave`; `Map.GetRandomSpawnPoint` is a local helper as
> Covetous's `RandomPointIn`; the New Magincia zone at 6444,2446 spawns at z -2 unchecked); the beacon invulnerable
> while a captain lives (`BeaconVulnerable`), surging at half damage into a second wave (1154551), 2 percent of hits
> blasting everyone within eight for 80-90 energy (1154552), its rubble statics at half and quarter hits, and on
> destruction the end of the invasion: 15 percent of damagers with rights within twelve get a Minax artifact
> (`MinaxArtifacts.CreateForInvasion`, 1154554), two minutes later a new invasion. `BlackthornDungeon.OnDeath`
> (Region.cs) already marks where `OnDeath(bc)` goes: a captain's death ends the wave when no captain lives
> (1154550), a soldier's death unblesses its captain when its list is empty. Saved: the city, the type, the beacon,
> the wave, the zones, and the captain-to-soldiers map (clean the dead thirty seconds after a save as ServUO does).
> The beacon stand-in: body and name "lighthouse", the two lighthouse statics (18212 and 18223 west of it) placed
> and removed with it, 50/85/99/99/70 resists, `ItemLevel.Easy` hits (100 + 100 x 5 = 600 at Easy), unattackable
> while a captain lives. Tests: a fact per piece, seen failing first; the invasion from BeginInvasion to the
> destroyed beacon on the test clock; round trips. Deviation rows for the stand-in and for anything the creature
> cannot do that the item did. Then `[GenBlackthorn` places the two controllers too. Read cc-P196's notes first.

## 7. Headless boot

**Done, two boots, both clean** (23:29 to 23:30, under the test-shard lock; the nightly bot was idle). `boot.sh <n>` in the
session scratchpad runs `sl-modernuo:cc-P196` on a 29 MB copy of the overnight bot's scratch world
(`D:\UO\bot-shard\world\Saves`, with empty Backups and Archives beside it, the world folder mounted whole as
`/var/lib/uo/modernuo`, as the test compose file mounts it, cc-P37) and a copy of the bot's Configuration with
`listeners 127.0.0.1:2596`, `serverListing.address 127.0.0.1`, `autosave.enabled False` (pingServer left on, the CC3
trap), client data from the UOAlive 7.0.116.0 folder, no port published; it waits for `Loading world done`, stops the
container with a 90-second grace (the D36 shutdown save) and keeps the log.

- Boot 1 (`boot-P196-run1.log`): client 7.0.116.0 detected, `[ShardVersion] Shattered Legacy 2026.10.20.21 (123
  version(s) in the changelog)`, `Loading world done (210942 items, 35148 mobiles) (2.47 seconds)`, listening on
  127.0.0.1:2596, `Saving world done (0.08 seconds)`, `Writing world save snapshot done (0.90 seconds)`,
  `[SaveOnShutdown] ...saved in 992 ms`, `Shutting down`.
- Boot 2 on that save (`boot-P196-run2.log`): `Loading world done (212995 items, 35335 mobiles) (2.15 seconds)`,
  saved and shut down the same way (906 ms).
- Zero `Exception` and zero `ERR` lines in either log; the one WRN in each (`Command stats already registered to
  Stats_OnCommand`, ClusterFStatInspect.cs against pinned's) is the shard's standing warning since cc-P21. Nothing in
  that world is a type of this port (nothing is placed at boot), so the load proves the assembly and the new types'
  registration; the facts prove the generate, the round trips and the save shapes. `[GenBlackthorn` on the test
  shard is P196-1.
- Three earlier attempts (`boot-P196-run*-badmount*.log`) mounted Saves, Backups and Archives as three separate
  volumes: the world loaded and the save ran, but the snapshot could not replace the Saves folder (`Cannot create
  '/var/lib/uo/modernuo/Saves' because a file or directory with the same name already exists`: the server renames
  Saves aside and recreates it, which a mount point refuses), so the second boot found an empty world and died on
  the account prompt. The world copy was reset from the bot's each time; the bot's own world was never touched.
  The lesson is in boot.sh's header and in P194's note already; this note repeats it.
- The scratch world copy was deleted after; the boot container was removed; the lock released at 23:30.

## 8. For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these. Then, as admin: `[GenBlackthorn` once
(the test world is built by the importer first; the command deletes an earlier run of itself and nothing else). To try
it in game:

1. **The dungeon:** `[go 6430 2678 0` (the landing, Trammel). The hitching post is two tiles west (say `stable` with
   a pet; `claim` brings it back). South and east are the ruined city rooms with their spawn; the dragon room is
   `[go 6405 2750 0`, the liches `[go 6405 2595 0`, the balron `[go 6456 2709 0`. Recall and Mark refuse; hide and
   you are revealed within five seconds; stand still two minutes and you are thrown into a gas cloud elsewhere.
2. **The castle:** `[go 1529 1520 0` and walk north onto a horse with a pet: dismounted at the door, the pet to the
   stables, no spells inside. The Agent of the Crown stands at `[go 1488 1473 1`.
3. **The Agent and the rewards:** `[MinaxArtifact` a dozen times (staff), then his context menu: Turn In Minax
   Artifacts (the tile gump; each click banks a point, "You have turned in N artifacts bearing the crest of Minax"),
   Claim Blackthorn Artifacts (the reward gump, 132 rows with the real properties under each; a painting for 10, the
   crest items from 25). A bought crest item reads "<name> bearing the crest of Blackthorn".
4. **The crest items by eye:** `[add EpauletteBearingTheCrestOfBlackthorn6`, `[add HoodedRobeBearingTheCrestOfBlackthorn1`,
   `[add GargishStoneChestBearingTheCrestOfBlackthorn`, `[add BlackthornPainting1`; in a house,
   `[add DecorativeShardShieldDeed` and double-click it for the 27-shield picker.
5. **The invaders:** `[add Invader Dragons`, `[add InvaderCaptain Undead` in a field; the captain's death gives the
   two top damagers a Minax artifact each.
6. **Test world boot:** done by CC on a scratch copy (section 7).

## Play-test items added

Through the For Chase list above; Who and steps in `testing/bot-triage.md` (P196 group) and `testing/playtest-steps.json`:
P196-1 BOT-PARTIAL (the dungeon, the post, the recall ban), P196-2 BOT (the gas cloud), P196-3 BOT-PARTIAL (the castle),
P196-4 BOT-PARTIAL (the Agent, turn-in and rewards), P196-5 EYES (the crest items and the shard shield in a house),
P196-6 BOT-PARTIAL (the invaders), P196-7 CC (test world boot, done: section 7). `tools/tests/test_play_who.py`
(18 tests) has the same two pre-existing failures P194 recorded (73 older items with no Who or Where: M-001, P163-0,
P164-0, P165-1 and on, none of them P196's); the P196 rows and steps are in both files and parse.

## 9. Port-list numbers

`SL_SHARD=D:/UO/golems/Bronze/ShatteredLegacy python tools/progress.py` (the stem proxy): Blackthorn Dungeon (revamped)
4 of 147 before, 138 of 147 after; the port list goes from 602 to 736 of 983 files (4 of 16 systems in, unchanged). Counted by hand (every `.cs` under the ServUO prefix
against ours, by stem): 147 candidates, 145 ported, 2 left (the two invasion files). The seven the proxy misses are
the `RobeBearingTheCrestOfBlackthorn .cs` files (a space before `.cs` in ServUO's name, so their stem ends in a space
and never matches ours); the overseer may want `progress.py` to strip stems, or the list's twin to name them.

## Repo size rule

No new file over 5 MB: the largest is `BlackthornSpawns.cs` at about 15 KB and the test at about 45 KB. Scratch (the
generators, the tile check, the break script and pristine copies, the boot world copy and logs, the build logs) is in
the session scratchpad, outside both repos.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun` (the three main checkouts: code clean, docs dry run on the play-test importer's and
the overnight bot's three machine-output files, scripts clean) and `Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive
-Branch golem/Bronze/P196 -CodeRepo D:\UO\golems\Bronze\ShatteredLegacy -DocsRepo D:\UO\golems\Bronze\shard-migration`
(this prompt's worktrees), both run at 2026-10-20 23:31 after the final edit of every file but this note's closing lines. Neither repo BLOCKED.
No file over 5 MB in either repo (`find -size +5M`: none). Every file this prompt wrote is ASCII (scanned by script:
157 .cs files, the notes, the two play-test files, the changelog and the edited CC9 fact). The docker-build lock was
held from 22:50 to 23:24 and the test-shard lock from 23:24 to 23:30 for the boots (section 7); no package or haven lock was needed;
nothing was placed in any world and no live config was changed. The docs repo's README.md, dashboard.html,
expansion-coverage.json and progress.json are progress.py's output (`SL_SHARD` at the Bronze copy).

```
=== code  (D:\UO\golems\Bronze\ShatteredLegacy) ===
  161 file(s) pending:
    CHANGELOG.md
    VERSION
    server/customizations/Services/PointsSystems/PointsSystem.cs
    server/tests/Items/CC9CloseVerification.cs
    server/customizations/Items/Addons/DungeonHitchingPost.cs
    server/customizations/Items/Equipment/Clothing/{Epaulette,GargishClothWingArmor,GargishFancyRobe,GargishSash,GargoyleHalfApron}.cs
    server/customizations/Mobiles/NPCs/BaseTurnInMobile.cs
    server/customizations/Services/PointsSystems/BlackthornData.cs
    server/customizations/Services/Revamped Dungeons/BlackthornDungeon/... (148 .cs)
    server/tests/Services/Revamped Dungeons/BlackthornDungeon/BlackthornDungeonVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\golems\Bronze\shard-migration) ===
  7 file(s) pending:
    README.md
    dashboard.html
    testing/bot-triage.md
    testing/playtest-steps.json
    tools/expansion-coverage.json
    tools/progress.json
    notes/cc-P196-port-blackthorn-dungeon.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

P196 DONE
