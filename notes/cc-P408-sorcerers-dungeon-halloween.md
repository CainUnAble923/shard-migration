# cc-P408: Treasures of Sorcerer's Dungeon (Jack the Pumpkin King) for Halloween

**Golem:** Iron. **Date:** 2026-10-22. **Branch:** `golem/Iron/P408` in both work copies. **Image:**
`sl-modernuo:cc-P408` = `86d02c1ae219` (builder `sl-uo-builder:cc-P408` = `9b4fbbbd6b65`).

## In plain words

- OSI's Halloween event, Treasures of Sorcerer's Dungeon, is now on the shard, ported from ServUO as written. From
  October 24 to November 2 it switches itself on: undead fill the rooms of Sorcerer's Dungeon in Ilshenar one after
  another, every 80 kills bring out a boss, and the ninth boss is Jack the Pumpkin King. After November 2 it switches
  itself off.
- While it runs, kills in the dungeon now and then put a piece of equipment "of Enchanted Origin" in the player's
  pack. A researcher by the dungeon entrance trades those for prizes: Jack's Bag of Tricks, a Jack in the Box toy, the
  Shackled Heart of the Pumpkin King, a Serpent's Jawbone, a Sterling Silver Ring, Boots or Talons of Escaping.
- Three of OSI's prizes are missing: the three title deeds ("Slayer of the Pumpkin King" and two more). The shard
  has no system for reward titles yet, so they are left out of the list rather than sold broken.
- For you: deploy this build before October 24 (nothing else to do; it starts itself and needs no player package).
  If you want to see it first, the staff checklist is in section 7. Decide later whether a reward-title system is
  worth a task (section 9).

## 1. What the event does on OSI (facts, from the ServUO files)

Source: `D:\UO\ServUO-pub57\Scripts\Services\Seasonal Events\TreasuresOfSorceresDungeon\`. **19 files, 2,278 lines**
(`wc -l`, every file; the brief said "about 2,400"): `Generate.cs` 125, `SorcerersDungeonData.cs` 151,
`SorcerersDungeonResearcher.cs` 118, `SorcerersDungeonRewards.cs` 34, `RewardGump.cs` 26, `Spawner.cs` 366,
`Creatures\` AbominableSnowman 77, GarishGingerman 75, HeadlessElf 83, JackInTheBox 85, JackThePumpkinKing 271,
NightmareFairy 76, RabidReindeer 92, StockingSerpent 75, TwistedHolidayTree 75, `Items\` Deeds 86, JackInTheBox 62,
JacksBagOfTricks 316, ShackledHeartOfThePumpkinKing 85. None of the 26 type names exists in `D:\UO\ModernUO-pinned`
or in the shard's `server\customizations` (grep of `class <Name>` and `TypeAlias` over both trees, and
`tools/modernuo-stems.txt`), except `SerpentsJawbone`, which the shard already has (`Items\Functional\SerpentsJawbone.cs`).

- **When.** ServUO's seasonal system lists it as `SorcerersDungeon`, Seasonal, from October 1 for 60 days
  (`Seasonal Events\SeasonalEventSystem.cs:68`), and turns it on and off on world load and world save, 30 seconds
  after a save (`Generate.cs:13-62`). It has no Christmas half (see section 8).
- **Where.** Ilshenar, the stock "Sorcerer's Dungeon" region (ServUO `Data\Regions.xml:2361`; pinned
  `Distribution\Data\regions.json:3323-3337`, the same five rectangles, entrance 546,455).
- **What it places** (`Generate.cs:64-115`): the researcher at 536,456,-53; three "Jumbo Pumpkin" statics (0x9D2B,
  0x9D2C, 0x9D2D) at 546,460,6 / 548,460,6 / 548,458,6; two flaming scarecrows (0x9F34) at 545,462,-53 and 550,462,-53;
  a pumpkin owl (0x9F28) at 545,463,-55 and a pumpkin rose (0x9F24) at 550,463,-55; the spawner. Each is skipped when
  already there. Turning off only stops the spawner (`Generate.cs:117-123`): the researcher and statics stay.
- **The spawner** (`Spawner.cs`): nine rooms in turn (`BuildEntries`, `:251-262`), each with 5 undead types (Zombie,
  Skeleton, Gargoyle, Lich, LichLord), up to 15 at a time, one every 3 to 8 seconds (`:142-152`); at 80 kills the
  room's boss appears (`:138-141`); when the boss is gone, after 1 to 3 minutes, the next room (`:125-137`, `:198-212`).
  The bosses in order: Nightmare Fairy, Jack in the Box, Headless Elf, Abominable Snowman, Twisted Holiday Tree, Rabid
  Reindeer, Garish Gingerman, Stocking Serpent, Jack the Pumpkin King. While it runs, the XmlSpawners in the nine rooms
  are reset (stopped, emptied) and are respawned when it ends (`:60-99`). `[TOSDSpawner` (Administrator) shows a gump
  of the rooms with a teleport button each (`:15-36`, `:284-364`).
- **The kill tally** (`SorcerersDungeonData.cs:37-96`): while enabled, a kill in the region by a living player adds
  fame / 4 x (1 + sqrt(luck) / 100) to that player's tally; the chance of an artifact is 0.000863316841 x 10 ^
  (0.00000425531915 x tally) (about 0.09% at first, 1% at a tally of 250,000); a hit makes a random weapon, armour,
  shield, jewel or hat through `RunicReforging.GenerateRandomItem` with the `EnchantedOrigin` suffix (hue 1171,
  `RunicReforging.cs:2067`; name cliloc 1157614, `:1730`), puts it in the pack (else bank, else at the feet) and empties
  the tally. The tally is saved.
- **The researcher** (`SorcerersDungeonResearcher.cs`): a `BaseTurnInMobile` "the Researcher", "Artifacts of Enchanted
  Origin Trader" (1157617); one point per artifact of Enchanted Origin turned in; "Claim Rewards" opens the reward gump.
  His pack holds the reward items for the gump's property display.
- **Rewards** (`SorcerersDungeonRewards.cs:13-27`), points: Jack's Bag of Tricks 75, Serpent's Jawbone 50, Jack in the
  Box 20, Shackled Heart of the Pumpkin King 20, Hero of the Unloved title deed 20, Savior of the Demented title deed
  30, Slayer of the Pumpkin King title deed 50, Sterling Silver Ring 50, Talons of Escaping 50, Boots of Escaping 50.
  - Jack's Bag of Tricks: once a day, in October only (staff any time): 10% a trick-or-treat treat, else one of six
    oddities (rancid reindeer meat, glass candy cane, an elf's severed ears with one of four elf names, a suspicious
    gift box, an insulting doll, spiked egg nog).
  - Jack in the Box: wind it (sound 1661), the jack pops out 9 s later for 5 s; once per 20 s.
  - Shackled Heart: you bleed harmlessly for about 10 s.
  - Sterling Silver Ring (ServUO's Treasures of Khaldun file): regen hits 3, regen mana 5, damage increase 75, 255
    durability, and a one-time choice of +20 in Archery, Fencing, Macing, Swords, Throwing or Wrestling.
  - Boots of Escaping (thigh boots) and Talons of Escaping (gargoyle talons), from Treasures of Kotl City's file:
    dexterity +4, stamina regen 1.
- **The bosses**, all 12,000 fame and -12,000 karma, murderers, `LootPack.UltraRich` x 2:

  | Boss | Body | Hits | Damage | AI | ServUO abilities |
  |---|---|---|---|---|---|
  | Nightmare Fairy | 176, hue 1910 | 8,000 | 21-27 | Mage | Life Leech, Life Drain |
  | Jack in the Box | 1428 | 8,000 | 21-27 | NecroMage | Armor Ignore / Bleed Attack |
  | Headless Elf | 31 | 8,000 | 21-27 | Mage (then Melee, see below) | Wrestling Mastery |
  | Abominable Snowman | 241, hue 1150 | 8,000 | 21-27 | Melee | Concussion / Crushing Blow, True Fear |
  | Twisted Holiday Tree | 47, hue 1175 | 8,000 | 21-27 | Mage | Explosive Goo |
  | Rabid Reindeer | 0xEA, hue 2707 | 8,000 | 22-29 | Melee | Venomous Bite; lethal poison |
  | Garish Gingerman | 14, hue 1461 | 8,000 | 21-27 | Mage | Magery Mastery |
  | Stocking Serpent | 0x509, hue 1459 | 8,000 | 22-29 | Melee | Vicious Bite; lethal poison |
  | Jack the Pumpkin King | 0x190 | 26,000 | 22-26 | NecroMage | every hit on him strikes back 8-20; 5% unholy pumpkins |

  Jack (`JackThePumpkinKing.cs:62-112`, "gleefully stolen from DemonKnight"): each blow he takes deals 8 to 20 physical
  back to the attacker with a thrown pumpkin; 5% of the time, a second later, 1 to 3 unholy pumpkins appear around the
  attacker, each hatching one of twelve undead after 5 to 10 seconds unless carved first (30%: 25-100 gold).
  The Headless Elf: ServUO's `AbilityProfile.AddMagicalAbility` sets the AI to Melee for any mastery up to
  WrestlingMastery (`Services\Pet Training\AbilityProfile.cs:408-414`), so on ServUO it fights as a melee creature
  despite `AI_Mage` in its constructor. The port keeps that (cc-P121 reproduces it; the fact asserts Melee).

## 2. The ModernUO APIs it leans on (all checked in `D:\UO\ModernUO-pinned`, d4531cd94)

| Need | Pinned API | Where |
|---|---|---|
| The kill hook (ServUO `EventSink.OnKilledBy`) | `CreatureEvents.CreatureDeathEvent` / `CreatureDeletedEvent`, `[OnEvent]` | `UOContent\Mobiles\CreatureEvents.cs:8`, `:11`; raised `BaseCreature.cs:3669`, `:3674` |
| Who killed it | `BaseCreature.GetLootingRights(DamageEntries, HitsMax)` | `BaseCreature.cs:3344` |
| A creature is deleted inside its own death | `Mobile.OnDeath` calls `Delete()` for non-players; `Delete` nulls Region, calls `OnDelete`, then nulls Map | `Server\Mobiles\Mobile.cs:4901`, `:2484`, `:2489`, `:2506` |
| Region at a point | `Region.Find(Point3D, Map)`, `Region.IsPartOf(string)` | `Server\Regions\Region.cs:545` |
| The stock region | "Sorcerer's Dungeon", DungeonRegion, Ilshenar | `Distribution\Data\regions.json:3323-3337` |
| Stock spawners (ServUO's XmlSpawner reset/respawn) | `BaseSpawner.Running`, `Reset()` (Stop + RemoveSpawns), `Start()`, `Respawn()` | `UOContent\Engines\Spawners\BaseSpawner.cs:330`, `:418`, `:769`, `:406` |
| Spawners in a room | `Map.GetItemsInBounds<T>(Rectangle2D)` | `Server\Maps\Map.ItemEnumerator.cs:83` |
| Spawn point checks | `Map.CanSpawnMobile(Point3D)`, `Map.GetAverageZ(x, y)` | `Server\Maps\Map.cs:1100`, `:237` |
| Timers | `Timer.DelayCall(delay, interval, Action)`, `Timer.StartTimer(delay, Action)` | `Server\Timer\Timer.DelayCall.cs:37`, `:60` |
| Gumps | `DynamicGump.BuildLayout`, `DynamicGumpBuilder.AddButton/AddHtml/AddHtmlLocalized/AddLabel`; `WarningGump(header, ..., Action<bool>)` | `UOContent\Gumps\Base\DynamicGump.cs:22`, `DynamicGumpBuilder.cs:69-135`, `UOContent\Gumps\WarningGump.cs:33` |
| Serialization | `[SerializationGenerator(0, false)]`, `[SerializableField]`, `[AfterDeserialization]`; `GenericPersistence` | e.g. `UOContent\Items\Misc\UnholyBone.cs` (the pinned twin of the unholy pumpkin) |
| Reflect damage | `AOS.Damage(m, from, dmg, phys, fire, cold, pois, nrgy)` | `UOContent\Misc\AOS.cs:34` |
| Ring skill bonus | `AosSkillBonuses.SetValues`, `GetLabel` | `AOS.cs:1408`, `:1312` |
| Treats | `HolidaySettings.RandomTreat` (`Server.Events.Halloween`) | `UOContent\Holiday Stuff\Halloween\HolidaySettings.cs:39` |
| Loot pool | `Loot.RandomArmorOrShieldOrWeaponOrJewelry(inTokuno, isMondain)`, `LootPack.GetLuckChanceForKiller` | `UOContent\Misc\Loot.cs:668`, `LootPack.cs:92` |
| Item overhead line to one player | `NetState.SendMessageLocalized(serial, graphic, type, hue, font, number, name, args)` | `Server\Network\Packets\OutgoingMessagePackets.cs:34` |
| Statics, blood | `Static(int itemID)`, `Blood(int itemID)` | `UOContent\Items\Misc\Static.cs:11`, `Blood.cs:15` |
| Race and body | `Mobile.Race` setter resets Body (then the creature sets its own) | `Server\Mobiles\Mobile.cs:395-411` |
| Console verbs | `ConsoleInputHandler.RegisterCommand(string[], desc, Action<string>)` | `Server\Console\ConsoleInputHandler.cs:37` |
| Start order | Configure, `World.Load`, Initialize | `Server\Main.cs:667-674` |

Shard pieces it stands on (already ported): the points framework (`Services\PointsSystems\PointsSystem.cs`, cc-P33),
`BaseTurnInMobile` and `BaseRewardGump` and `CollectionItem` (cc-P194, cc-P196), the Minax-artifact roll
(`MinaxArtifacts.cs`, cc-P196), the ability profile with ServUO's `SetSpecialAbility` / `SetMagicalAbility` /
`SetAreaEffect` (cc-P121), `SetWearable` (`Misc\WearableExtensions.cs`), `LeatherTalons`, and the seasonal switch
(`ClusterFSeasonalSwitch.cs`, cc-P267).

**The port corollary (step 7):** no missing subsystem blocks the event. One small one blocks three rewards: ServUO's
reward titles (`PlayerMobile.AddRewardTitle` and the title menu), which neither pinned nor the shard has (the BOD
rewards met the same gap, `Services\BulkOrders\BODRewardCollections.cs:10`). Section 9 sizes it.

## 3. The port

`server\customizations\Services\Seasonal Events\TreasuresOfSorceresDungeon\`, **19 files, 2,617 lines**, mirroring
ServUO's folder:

| File | What |
|---|---|
| `Generate.cs` | ServUO's Generate/Remove, the season switch, `[SorcerersDungeon` and the console `tosd` |
| `Spawner.cs` | `TOSDSpawner`, `TOSDSpawnEntry`, `[TOSDSpawner` and its gump |
| `SorcerersDungeonData.cs` | the points system, the kill tally and the kill hook; saves the spawner inside it, as ServUO |
| `EnchantedOriginArtifacts.cs` | the artifacts of Enchanted Origin (mark, registry, roll) and `[EnchantedOriginArtifact` |
| `SorcerersDungeonResearcher.cs` | the researcher |
| `SorcerersDungeonRewards.cs` | the reward list and the reward gump |
| `Creatures\*.cs` (9) | the nine bosses; `JackThePumpkinKing.cs` also holds `UnholyPumpkin` |
| `Items\JackInTheBox.cs`, `JacksBagOfTricks.cs` (+ six oddities), `ShackledHeartOfThePumpkinKing.cs` | rewards |
| `Items\EscapingAndSterlingRewards.cs` | `SterlingSilverRing`, `BootsOfEscaping`, `TalonsOfEscaping`, `ApplySkillBonusGump` |

Three small edits elsewhere: `ClusterFSeasonalSwitch.cs` (a switch may borrow another season's dates: `datesFrom`),
`PointsSystem.cs` (the `SorcerersDungeon` points type; the save writes names, so no renumbering),
`MinaxArtifacts.cs` (`ApplyProperties` made public, to reuse the roll). Plus `CHANGELOG.md` / `VERSION` (2026.10.22:
two player lines, one staff line) and three rows in `docker\uo\COMMANDS.md`.

Every saved type uses the source generator, version 0: the nine bosses, `UnholyPumpkin`, the researcher, and 11 items
(`JackInTheBox`, `JacksBagOfTricks` with `NextUse`, the six oddities with `NamedSeveredElfEars.ElfName`, the heart,
the ring, the boots, the talons). The points system and the artifact registry are hand-written and versioned like
their cc-P196 twins (`BlackthornData`, `MinaxArtifacts`); an unknown version fails loudly. No XmlSpawner anywhere.

## 4. Deviations (numbered; each with its reason)

1. **Dates.** ServUO: October 1 for 60 days, checked at load and at each save. Here: the Halloween season switch,
   `clusterf.seasonal.halloween.start` / `.end` (10-24 to 11-02, inclusive, shard-local date) and `.automatic`, checked
   at load and hourly, acting only when the season changes. The event's switch is named `sorcerersdungeon` and keeps
   its own saved state, so the decor's place/clear and the event's on/off never undo each other. The brief asked for
   exactly this.
2. **The three title deeds are not ported** and are not in the reward list or the researcher's pack: no reward-title
   system (section 9). Showing them and refusing, or selling a deed that does nothing, would be worse.
3. **`JackInTheBox` the creature is `JackInTheBoxMonster`.** ServUO has two classes called `JackInTheBox` (the boss,
   and the reward toy in `Server.Items`). Spawners and `[add` find a type by its short name, first match wins, so one
   would always shadow the other, and the shard's type-identity gate fails the build on it. The player sees the same
   "jack in the box".
4. **Artifacts of Enchanted Origin are marked, not suffixed.** Pinned has no reforging and no `ReforgedSuffix` on
   equipment. As cc-P196 did for Minax: the item gets ServUO's hue (1171), the name "<item> of Enchanted Origin" (the
   server's copy of the client text, not ServUO's cliloc line 1157614), and a saved registry the researcher checks. The
   property roll is ServUO's budget arithmetic over pinned's runic tables (`MinaxArtifacts.ApplyProperties`), the
   deviation cc-P196 already recorded. The cliloc text for 1157614 could not be read here (the client's `Cliloc.enu` is
   compressed and the reader returned nothing even for 1154507, Minax's), so "of Enchanted Origin" follows ServUO's
   table comment and the researcher's own clilocs; unverified against the client.
5. **XmlSpawner reset becomes stock-spawner pause.** The shard has pinned's spawners, not XmlSpawner. While the event
   runs, the stock spawners standing in the nine rooms that were running are `Reset()` (stopped, emptied); at the end
   exactly those are started and respawned. Unlike ServUO, a spawner staff had switched off stays off. Their serials are
   saved with the event. On the bot's world copy that is 14 spawners (section 6).
6. **Two ServUO bugs fixed** (the D-4 rule: a bug that makes something broken): the staff gump's teleport looped
   forever when a room had no open spot (now 50 tries and a message); a spawned creature deleted without dying (a staff
   `[delete`) stayed in the spawn list forever, so the room never refilled and the boss never came (now dropped on the
   next tick, not counted as a kill). Also a guard: a spawn timer that fires after the event was turned off spawns
   nothing.
7. **Off removes the standing boss too.** ServUO's Deactivate deletes the spawn list but leaves a boss standing in the
   world after the event. Here the boss goes with its spawner, as the brief's "force it off, check they are gone"
   expects.
8. **The kill hook finds the region at the death spot.** Pinned raises its creature death event after the creature is
   deleted (no Region, no Map), so the facet is taken from the creature-deleted event raised a moment earlier in the
   same call, and the region is found at the death location (section 2). Same result as ServUO's `bc.Region`. Found by
   the first probe of the facts, which failed until this was done.
9. **The Sterling Silver Ring's confirmation** is pinned's `WarningGump` with the skill's name as its header (ServUO's
   `GenericConfirmCallbackGump` does not exist in pinned); same text (1155611), same effect; "no" reopens the skill list.
10. **Boots and Talons of Escaping are `[Constructible]`** (ServUO's have no `[Constructable]`; only the reward gump
    makes them), so staff can `[add` them.
11. **Ours, added:** `boss <1-9>` on `[SorcerersDungeon` (raise a room's boss now: a staff and test aid, like
    `[MinaxArtifact`), `remove` (take down the researcher and entrance pieces it placed, by serial), the console
    `tosd`, `[EnchantedOriginArtifact`, and a `status` that reads the world. None changes what players meet.

Recipe transformations, not deviations: `AI_NecroMage` is `AI_Mage` (Q-050); the `0.2, 0.4` speeds are dropped
(dead in ServUO too, Q-008); `SetWeaponAbility` pairs are `GetWeaponAbility` drawing one of the two;
`[CorpseName]` is the `CorpseName` override; `RealLuck` is `Luck`; `DateTime.UtcNow` is `Core.Now`; `IsArtifact`
dropped (no pinned reader); `IsTokunoDyable` kept with no caller yet (pigments of Tokuno are not ported); ServUO's
`[TOSDSpawner` gump is a `DynamicGump`. Jack's Bag of Tricks keeps ServUO's calendar-October rule (its message says
"the Month of October"), so in the event's last two days (November 1-2) it works for staff only, as on ServUO.

## 5. Art (step 4)

Stock art only; nothing needs a player package. Every new ID checked in the players' client
(`D:\UO\UltimaOnlineVanilla`, the folder `Play-TazUO-Live.ps1:40` points at), tiledata names through the vseUOAware
reader: 0x9F85 "Bag of Tricks 1" (rendered), 0x9F74 "Serpent_Jaw_EAST", 0x9F64 / 0x9F65 "JackintheBox", 0x4A9C
"Shackled Heart SOUTH", 0x9D2B-0x9D2D "Jumbo Pumpkin A/B/C", 0x9F34 "Scarecrow_Flaming", 0x9F28 "Pumpkin_Owl",
0x9F24 "Pumpkin_Rose", 0x9DC3 "giant_candy_cane", 0x312D "severed elf ears", 0x48E2 present (named "ValanetinesDayPolarB":
ServUO's insulting doll is that polar-bear doll art). Bodies in `mobtypes.txt`: 1428 "JackintheBox", 1289 (0x509, the
Najasaurus the stocking serpent uses), 176, 241, 47, 234, 14, 31, 400. Older IDs (meat, egg nog, gift box, deed) are
classic art. Not checked: the server's own 7.0.117 client folder (`D:\ShatteredLegacy\client-data`, another Golem's
desk; the guard refuses it). The headless boot ran on the UOAlive 7.0.116.0 data and spawned on the real Ilshenar map.

## 6. Tests and builds

**Facts:** `server\tests\Services\Seasonal Events\TreasuresOfSorceresDungeon\SorcerersDungeonVerification.cs`, 11
facts, expected values written as ServUO's literals:

| Fact | Pins |
|---|---|
| TheBossesHaveServUOsStatsAndAbilities | name, body, hits, damage, AI, fame/karma, murderer, poison immunity declared, Jack's gear, the profile abilities, the weapon-ability pairs |
| JackHitsBackForEightToTwentyOnEveryBlow | the reflex lands on the attacker; the unholy pumpkin |
| TheSpawnerRotatesNineRoomsInsideTheDungeon | the nine rooms, bosses, 80 / 15, the undead list, every room inside the stock region; boss at 80 kills; next room when the boss is gone; wraps to room 1; a deleted spawn leaves without counting |
| TheStockSpawnersInTheRoomsPauseWhileItRunsAndOnlyThoseRestart | a running spawner in a room pauses and restarts; a stopped one stays stopped; one outside is untouched |
| OnPlacesOnceOffLeavesTheResearcherRemoveTakesExactlyWhatItPlaced | dry runs change nothing; on places the researcher and 7 pieces once; off removes spawn and boss, keeps the researcher; status reads the world; remove leaves a same-art lookalike on the same tile |
| TheBossVerbRaisesTheRoomsBossNow | `boss 9` raises Jack in his room once; the rotation carries on; the reward list in status |
| ItRunsOnTheHalloweenDatesWithItsOwnState | the Halloween keys; 10-24 to 11-02; first seen out of season left alone; up at the window, a staff off stands, down after |
| AKillInTheDungeonTalliesAndRollsAnArtifactOfEnchantedOrigin | through a real `Kill()`: the spawner's kill count and the tally (fame / 4); ServUO's chance curve; an artifact of hue 1171 in the pack; nothing when disabled or outside |
| TheResearcherTakesArtifactsForAPointAndSellsServUOsRewards | redeemable or not; one point; the reward list and prices; every reward constructs |
| TheRewardsBehaveAsInServUO | the bag's rules, the oddities, the ring's attributes and skill bonus, boots, talons, toy, heart |
| EverySavedTypeRoundTrips | every generated type; the points system with the spawner inside (boss, spawn, room, kills, paused spawners), the tallies and points; a save with no spawner; the artifact registry |

**Seen failing first** (the probe: `sl-uo-builder` with the port bind-mounted, `dotnet test` filtered, no lock needed):
ten deliberate breaks, one aimed at each fact, all ten facts red (Jack's hits 25000; the reflex removed; a room's kill
count 79; stock spawners not reset; Deactivate not deleting the boss; `datesFrom` dropped; fame / 2; a price 70; the
ring's damage 70; the spawner saving its room in place of its kill count). The round-trip fact tripped on the ring
break first, so its own break was re-run alone: red, `Expected: 42, Actual: 3`. The boss verb's fact: red with the
verb raising room 1's boss. The status world count: a first break (dropping `!m.Deleted`) did NOT turn it red, because
the world never lists a deleted mobile, so that check proves nothing and a real break was used (the boss filter
matching no type): red. All restored byte for byte (`cmp`), then green.

Two of my own first expectations were wrong and the probes caught them: the Headless Elf's AI (section 1: Melee on
ServUO too), and ServUO's random spawn point, which includes the room's far edge (the fact now checks the inclusive
room, as ServUO draws it). And one port bug: the kill hook (deviation 8).

**Gated builds** (`docker/uo/build.sh -t sl-modernuo:cc-P408`, under the docker-build lock; memory checked and the
Docker VM's page cache dropped first):

| Run | Tree | Result |
|---|---|---|
| 1 | the port and 10 facts | all 147 patches applied; 2165 shard tests passing (2169 total) |
| 2 | + the boss verb and its fact | 2166 passing (2170 total) |
| 3 | + the status world count | 2166 passing (2170 total), image `0483f2037c26` |
| 4 (final) | + changelog, COMMANDS.md, two comment citations, the boss line's spacing | all 147 patches applied; 2166 passing (2170 total; the 4 others are the suite's standing skips), exit 0, image `86d02c1ae219` |

**On a running server** (step 6, under the test-shard lock). The shared test shard is not this worktree's (it runs from
`D:\ShatteredLegacy`), so, as cc-P196 did, `sl-modernuo:cc-P408` was booted headless on a **copy** of the overnight
bot's world (`D:\UO\bot-shard\world\Saves`, 33 MB; the bot was idle), with the bot's configuration (listener moved to
127.0.0.1:2597 inside the container, no port published, autosave off), client data from UOAlive 7.0.116.0, and an
empty map overlay. The server turns its console off when stdin is not a terminal, so util-linux `script` (in the
image) gave it a pseudo-terminal and the `tosd` verbs were piped in. The image booted was run 3's (`0483f2037c26`);
run 4 changed only the changelog, the command table, two code comments and the spacing of the `boss` reply line (which
had printed "a nightmare fairy  in room 1", two spaces, for a boss with no title), all built and tested in run 4.
Lines from `boot-run3.log` (2026-10-22 14:30):

- Before: `Enabled: False. Researcher: none. Entrance pieces standing: 0 of 7.` `Spawner: not running.`
  `In the world: 0 event boss(es); 37 creature(s) inside the nine rooms.` and the reward list, 7 rows.
- `tosd on`: `Outside the dates (10-24 to 11-02): turning it on anyway.` `placed the researcher at (536, 456, -53)
  (Ilshenar).` `placed 7 of the 7 entrance pieces` `Started the spawner; paused 14 stock spawner(s) in its rooms.`
- 25 s later: `room 1 of 9 (NightmareFairy), 4/15 spawned` and `4 creature(s) inside the nine rooms` (the 37 stock
  creatures gone with their paused spawners; 4 event undead placed on the real map).
- `tosd boss 9`: `Raised jack the pumpkin king in room 9 at (300, 80, -27).` then `In the world: 1 event boss(es)
  (jack at (300, 80, -27)); 6 creature(s) inside the nine rooms.`
- `tosd off`: `Stopped the spawner: 6 creature(s) removed, 14 stock spawner(s) restarted.` `Disabled. The researcher
  stays` and then `In the world: 0 event boss(es); 34 creature(s) inside the nine rooms.` (the 34 are the restarted
  stock spawns).
- `tosd on` again: `The researcher already stands`, `placed 0 of the 7 entrance pieces (7 already there)`.
- `tosd remove`: `Removed 8 placed object(s)` and then `Researcher: none. Entrance pieces standing: 0 of 7.`

A restart with the event running (`boot-run4b`, `boot-run5b`): on, a boss raised, `save`, stop; then a fresh boot of
that save: `Enabled: True. Researcher: at (536, 456, -53)`, `Spawner: room 1 of 9 (NightmareFairy), 4/15 spawned ...
boss up at (340, 56, -28), 14 stock spawner(s) paused.`, and 20 s later `7/15 spawned` (the timer resumed after load).
`tosd remove` then cleaned up all of it. No exception in any boot; the only warnings are the shard's two standing ones
(`Command stats already registered`, the retired `testCenter.skillGainMultiplier`). Two harness slips, said plainly:
the first two boots ran the verbs into a console that was off (stdin not a terminal), and the first restart test
proved nothing (with `script` as the container's first process the stop signal never reached the server, so no
shutdown save); both were redone as above. The world copy was deleted after.

Not tested in a client (this PC has none): the researcher's context menu and gumps, the bag, the ring's gump, the
look of the entrance pieces.

## 7. Staff checklist for live use

Nothing is placed by deploying. The live world is touched only when the season opens (10-24, by itself) or by a staff
command. Admin commands, also on the server console as `tosd <verb>`:

| Command | What it does | Run twice? |
|---|---|---|
| `[SorcerersDungeon status` | date, season, enabled, researcher, spawner room and counts, what stands in the world, the reward list | read only |
| `[SorcerersDungeon on` | places the researcher (536,456,-53 Ilshenar) and the 7 entrance pieces, each only if missing; starts the spawner, pausing the stock spawners in its rooms; enables the kill tally. Works before the dates (it says so); stays on until `off` or the season next ends | places nothing twice |
| `[SorcerersDungeon off` | stops the spawner, removes its creatures and boss, restarts the paused stock spawners, disables the tally. Researcher and pieces stay | second run: "not running" |
| `[SorcerersDungeon remove` | `off`, then deletes the researcher and the pieces it placed (by serial; never a same-art item it did not place) | second run removes nothing |
| `[SorcerersDungeon boss 9` | raises a room's boss now (1-9; 9 is Jack); refuses while a boss is up | refuses the second |
| add `dryrun` to any of the above | prints what it would do, changes nothing | |
| `[TOSDSpawner` | ServUO's room gump; a button moves you into a room | |
| `[EnchantedOriginArtifact [budget]` (GM) | a test artifact in your pack | makes another |

On deploy, the log line to look for at start: none until 10-24 (the switch's first look sees out of season and leaves
the world alone); on 10-24 within the hour: `[SorcerersDungeon] 2026-10-24: the season has begun (10-24 to 11-02).`
and the `placed ...` lines. After 11-02: `the season is over`, and the spawner stops. To move the dates, edit the
Halloween settings (`clusterf.seasonal.halloween.start` / `.end`); they move the bank decor too.

## 8. The Christmas half

ServUO's event has none. Five of its nine bosses are winter-holiday creatures (snowman, holiday tree, reindeer,
gingerman, stocking serpent), but they are rooms in the same single rotation of the same October event (`Spawner.cs:
251-262`, one `EventType.SorcerersDungeon` entry, `SeasonalEventSystem.cs:68`). (How OSI itself scheduled it is
not checked here; the source has one event.)
So the whole file set is ported and all of it is wired to the Halloween season. ServUO's December content is a
different event, `KrampusEncounter` (December 1 for 60 days, `SeasonalEventSystem.cs:71`, its own folder); porting it
would be its own prompt, and it would sit on the existing winter switch (`clusterf.seasonal.winter.*`).

## 9. For Chase: the reward-title gap

The three deeds (20, 30 and 50 points) need ServUO's reward titles: `PlayerMobile.AddRewardTitle` and a saved list
of earned titles, plus the title choice in the paperdoll menu. Not sized here beyond that it is a PlayerMobile change
(a patch) plus a gump; the BOD reward title deeds (placeholder rows in `BODRewardCollections.cs`) and the
community collections' titles wait on the same thing. Worth a
research prompt if titles matter to players; otherwise these stay out.

## 10. Credits

ServUO (pub57), `Scripts/Services/Seasonal Events/TreasuresOfSorceresDungeon/` and the reward items from its Treasures
of Khaldun and Treasures of Kotl City folders (ServUO team and contributors). The event, its creatures and its rewards
are OSI's (Ultima Online, Treasures of Sorcerer's Dungeon).

## 11. Commit preflight

`D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -Branch golem/Iron/P408 -CodeRepo
D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration`, run after the final gate and the
last code edit, before this section was written: code 26 files pending (`CHANGELOG.md`, `VERSION`,
`docker/uo/COMMANDS.md`, the three edited customizations, the 19 port files, the facts file), docs 1 file (this note);
"dry run: would add, commit and push" for both; nothing BLOCKED. No play-test or bot files changed. Locks: docker-build
held for the four gates (released), test-shard held for the headless boots 14:20-14:49 (released); no package or haven
lock was needed. Nothing was placed in any live or shared world, and no live configuration was changed. Not committed:
the Golem commits.

P408 DONE
