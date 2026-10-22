# cc-P405: servuo.dev code batch 10-22, research

## In plain words

- We looked at the 15 servuo.dev downloads from 10-22 (companions, bosses, levelable gear, New Haven NPCs and Town
  Houses). Nothing was installed or changed; this is a report, and nothing in game is different yet.
- Only one is worth porting as code: the archery butte that shows where your arrow hit. It needs new item art in
  the player package first, so it waits on the art route (F-8 / F-21).
- Six are good ideas we would rebuild our own way: a "rest" at the New Haven inn, talking townsfolk, a boss token
  for staff events, a Halloween rider boss, gear "charms" that proc, and sockets (we recommend no sockets). The
  other eight are reference only or skip: the shard already has better versions (companions, levelable gear, Stygian
  Dragon) or the code is broken or unsafe.
- For you to decide: the open questions near the end. The time-sensitive one is Halloween (the season switch opens
  10-24): port OSI's own Pumpkin King event first, build a custom "Hollow Rider", both, or neither this year.

## Scope and method

Prompt: `cc-prompts\claimed\Iron\cc-P405-servuo-batch-1022-research.md`. Research only: nothing was built, run,
installed or extracted, every `_zips` archive stayed zipped, and no shard or docs file was edited. `CODE-INTAKE.md`
was not edited; the summary for its Overseer column is at the end.

- **Engine authority:** `D:\UO\ModernUO-pinned` at d4531cd94; engine paths are under `Projects\`.
- **ServUO reference:** `D:\UO\ServUO-pub57`.
- **Shard paths:** `D:\ShatteredLegacy\server\customizations\`. Sections write it as `cust\`, `SL\customizations\` or,
  in the companions and bosses sections, as bare paths such as `Companions/BaseCompanion.cs` or `Mobiles\Bosses\`.
  Read on the Iron Golem's work copy of it, branch golem/Iron/P405.
- **Third-party paths:** `D:\UO\third-party\code\<folder>\`.
- **Counts:** made for this note with `find` and `wc -l`, file lists beside them. The folder lists exclude `_zips\`.
  "(unverified)" marks what was not checked. Statements came from four parallel readers (one per area), and the key
  claims were spot-checked by hand: the Quetzalcoatl body (1289, `DQDante.cs:15`, not the Stygian Dragon's 826,
  `Mobiles\Bosses\StygianDragon.cs:46`), the innkeeper double charge (`SpecializedInnKeeper.cs:87-92`), pinned's butte
  facing (`UOContent\Items\Addons\ArcheryButteAddon.cs:36`), the Townsperson `BeginInvoke` (`Townsperson.cs:884`), and
  the missing `Tamingcoins` (`HeadlessHorseman.cs:211`).
- **Client data was not opened** for body, item or hue ids (the client lives under `D:\ShatteredLegacy\client-data`);
  ids are checked against pinned, ServUO and shard code that already uses them.

**Corrections to the brief and to CODE-INTAKE.md (counted):**

| Item | Brief or intake says | Counted |
|---|---|---|
| quetzalcoatl-armor-mob body | Stygian Dragon body | body 1289, the Najasaurus (`DQDante.cs:15`; shard `Mobiles\Normal\Najasaurus.cs:11`) |
| squire-system author | intake: rhasce | SOURCE.txt agrees (rhasce, archive 1355); P41 read unblest's 2021-06 build, which counts the same 33 .cs, 21,941 lines |
| squire-system Ser | intake: 42 Ser | 42 Serialize + 42 Deserialize (84 overrides) |
| squire-system AddHtml | P41: 188 | 737 in the folder (507 in SquireTitle, which the design cuts; 188 in SquireGump) |
| level-system-3 | intake: 84 .cs, 19k, 72 files XmlSpawner | 84 .cs, 19,287 lines; 71 of 84 in the XmlSpawner2 namespace |
| specialized-innkeeper | intake: 1 .cs, 293 lines | 1 .cs, 292 lines (`wc -l`); the `_zips\` copy is byte-identical |
| conversational-townsperson | intake: 9 .cs, 8.5k | 4 server .cs (1,613 lines) + 5 editor .cs (6,868); the "VB" editor is C# WinForms |
| headless-horseman | intake: 526 lines | 522 (`wc -l`) |

## Summary

| Area | Folder | Verdict | Size |
|---|---|---|---|
| Companions | squire-system | reference only | L |
| Companions | pet-experience-scroll | borrow the idea | S |
| Bosses | headless-horseman | borrow the idea | S |
| Bosses | quetzalcoatl-armor-mob | skip | S |
| Bosses | world-boss-in-a-box | borrow the idea | S |
| Bosses | summoning-system-v2 | reference only | L |
| Levelable gear | level-system-3 | reference only | L |
| Levelable gear | xmlsockets | borrow the idea | M |
| Levelable gear | passive-item-system | borrow the idea | S |
| Levelable gear | equipment-level-requirements | skip | S |
| New Haven | conversational-townsperson | borrow the idea | M |
| New Haven | specialized-innkeeper | borrow the idea | S |
| New Haven | skill-trainer-npc | skip | S |
| New Haven | archery-butte-hits | port (art-gated) | S |
| Buildings | knives-town-houses | reference only | L |

No license is stated on any of the 15 (each SOURCE.txt): credit the authors, private repo only, do not repost, and
take design rather than code wherever a verdict allows.

## Companions

### squire-system

**License:** none stated (SOURCE.txt). Squire System by rhasce on the classic squire system (several contributors),
servuo.dev archive 1355, posted 2020-03-31, updated 2022-10-26, downloaded 2026-10-22. Credit rhasce and the original
squire authors; private repo only; do not repost.

**1. What it does.** Hireable, bondable human followers ("squires") that fight, follow, heal, loot, ride and cast
(Chivalry, plus Bushido and Necromancy in this version), with a big lore and command gump, 86 speech commands, skill
training contracts, instructor vendors, an inn "room attendant" that stores squires, and a carrier pigeon that calls one
back. It serves the companions feature (the Squire half of the Squire plus EvoMerc hybrid).

**2. Overlap.** Already mined in full: `notes/cc-P41-companions-research.md` (713 lines) is the engine read of this
exact source, and the design's "Squire System extras: keep or cut" table
(`docs/companions/companions-squire-evo-research.md:269-288`) already decided each extra. The shard has its own
companion code, written for ModernUO and not ported from this:

- `Companions/BaseCompanion.cs` (316 lines): source-generated record on the creature (lineage id, path, branch,
  personality, loop, rank, level, XP, breeding fields, skill peaks; `:39-108`), player skill caps and player hit math.
- `Companions/CompanionParty.cs` (266): follower math, logout with owner, `[CompanionMake` and `[CompanionSet` staff
  commands (`:29-30`). Hiring is B4 and rooms are B9 (header `:8`, `:167`), neither built.
- `Companions/CompanionSettings.cs` (138): F-12 ladder (`:75-78`, `:100-107`), slot cost by rank (`:81`, `:113`).
- `Companions/CompanionLineage.cs` (69): never-reused ids (P41 section 8).
- Also relevant: `ShrunkPet.cs` (166), `ClusterFPetGainSpeed.cs` (104), the ported pet training under
  `Services/Pet Training/` (15 files, 8,581 lines).

Ours is better on structure (source-generated saves, player parity, owner gate, settings-driven numbers). What this
download still offers is behavior to borrow for later steps: the auto-heal, auto-potion, ammo pickup, flee and
auto-loot toggles, the voice-command list, the lore gump layout, and the room and pigeon flows. That is idea and
reference only; P41 already says a straight conversion carries hidden core patches.

**3. Port cost (counted).**

- **33 .cs, 21,941 lines** (matches P41 `:48`; SOURCE.txt's "33 .cs, about 22k" is right). Files: Commands (4: Squire
  Room 128, Squire Skills 63, Squire Stats 63, Squire Switches 63), EC Squire Book (2: ECSquireBook 44,
  ECSquireBookGump 158), Items (7: CarrierPigeon 118, RoomAttendantContract 93, SquireBook 358, SquireContract 67,
  SquireDeathShroud 40, SquireStatsSpyglass 71, TrainingContracts 2,108), Mobiles (8: RoomAttendant 1,049, Squire 4,638,
  SquireBardingInstructor 47, SquireCombatInstructor 76, SquireHealingInstructor 59, SquireRepresentative 61,
  SquireThievingInstructor 55, SS_InnKeeper 265), Other (5: SquireDialog 1,980, SquireFunctions 170, SquireGump 1,963,
  SquireTargets 2,455, SquireTitle 5,403), Sell Buy (7: SBRoomAttendant 35, SBSquireBardingInstructor 37,
  SBSquireCombatInstructor 47, SBSquireHealingInstructor 38, SBSquireRepresentative 36, SBSquireThievingInstructor 37,
  SBSS_InnKeeper 116).
- **Serialize/Deserialize overrides: 84** (42 `Serialize` + 42 `Deserialize`). Each becomes
  `[SerializationGenerator]` fields, as pinned BaseCreature does (`UOContent/Mobiles/BaseCreature.cs:137`). No saves
  exist, so version 0.
- **Dependencies:** no XmlSpawner or XmlAttach (0 hits for "xml" in any file). Other: `Discordance` internals
  (`Other/SquireTargets.cs:911`, `:990` use `Discordance.m_Table` and `DiscordanceInfo`), private in pinned
  (`UOContent/Skills/Discordance.cs:11`); the public route is `Discordance.DiscordanceTarget` (`:119`). 14
  `TimerPriority` uses (missing in pinned, P41 `:118`). 111 Bushido, Necromancy, Masteries or VvV mentions to sort.
- **Core or stock-file edits:** two that the source itself assumes. `Mobiles/Squire.cs:4-34` asks the admin to hand-edit
  `Corpse.IsCriminalAction`; pinned's (`UOContent/Items/Misc/Corpses/Corpse.cs:750`) has no clause for a pet's master.
  The Discordance access above. P41 adds about 4 small pinned patches for exact player parity (P41 summary row 2).
- **Gumps to rewrite: 5** (`ECSquireBookGump` ECSquireBookGump.cs:9, `RoomAttendantGump` RoomAttendant.cs:705,
  `SquireCustomizeGump` SquireGump.cs:20, `SquireLoreGump` SquireGump.cs:329, `SquireTitleGump` SquireTitle.cs:27).
  **737 `AddHtml(` calls** (SquireTitle 507, SquireGump 188, RoomAttendant 38, ECSquireBookGump 4). P41's "188" counts
  SquireGump only; the design already cuts SquireTitle (`companions-squire-evo-research.md:288`), so 230 remain for a
  port. Pinned DynamicGump's `AddHtml` 6th parameter is a color (`UOContent/Gumps/Base/DynamicGumpBuilder.cs:81-83`), so
  the ServUO `(..., false, false)` form does not bind.
- **Art or client data:** stock item graphics only (0x14F0 deed x29, 0x14F5, 0x204E, 0xFF2), stock gump backgrounds
  (5054, 9250, 311), human bodies 0x190 and 0x191 (`Mobiles/Squire.cs:565-567`). Stock-ness against our client is
  (unverified); none looks custom.
- **ServUO types it derives from, checked in pinned:** `BaseCreature` (`UOContent/Mobiles/BaseCreature.cs:138`), `Item`,
  `Target` (`Server/Targeting/Target.cs:12`), `Timer` (`Server/Timer/Timer.cs:22`), `Gump` (legacy,
  `UOContent/Gumps/Base/Legacy/Gump.cs:25`; use `DynamicGump`, `DynamicGump.cs:22`), `Prompt` (`Server/Prompt.cs:3`),
  `ContextMenuEntry` (`Server/ContextMenus/ContextMenuEntry.cs:24`), `BaseVendor`
  (`UOContent/Mobiles/Vendors/BaseVendor.cs:29`), `SBInfo` (`UOContent/Mobiles/Vendors/SBInfo/SBInfo.cs:5`),
  `GenericSellInfo` (`UOContent/Mobiles/Vendors/GenericSell.cs:7`), `TanBook` (`UOContent/Items/Books/TanBook.cs:6`),
  `BaseOuterTorso` (`UOContent/Items/Clothing/OuterTorso.cs:9`), `HuePicker` (`Server/HuePicker.cs:5`). All exist.
  **Missing:** `AI_Paladin` (`UOContent/Mobiles/AI/BaseAI/AIType.cs:18-30` has 10 values, no paladin). Pinned does
  have `HealerAI` (`UOContent/Mobiles/AI/HealerAI.cs:10`, wired at `BaseCreature.cs:2603`), but P41 `:342` found it
  heals only same-Team creatures, never a player, so it is unusable for a companion.
- Per-file sizes for a rewrite are in P41 section 1.3 (Squire.cs L, SquireTargets L, SquireGump M, RoomAttendant M).

**4. Risk.**

- Save compatibility: none to keep (no Squire saves exist); a straight port would add a second companion class family
  beside `BaseCompanion`, which is the real risk (two save formats for one feature).
- Global touches: the corpse edit changes looting rights for every pet's master (loot and notoriety, global). Exact
  parity needs pinned `SkillCheck` changes (pinned's controlled-creature x2 is at `UOContent/Skills/SkillCheck.cs:140-143`)
  that would touch every pet's skill gain. Discordance access touches combat.
- Exploits P41 already found and the design must not copy: the lore gump's `OnResponse` never re-checks ownership
  (P41 `:129-130`; pinned validates button ids only for legacy gumps); the pigeon has no owner, travel or cooldown check;
  rooming by `SetControlMaster(null)` escapes the abandoned-pet delete (P41 summary row 6); training contracts set a skill
  outright (the design reworked them into Drill Orders, `companions-squire-evo-research.md:283`).
- Movement: none global; the companions follow and ride through stock order and mount code (P41 section 5).

**5. Verdict: `reference only`, L as a port.** The shard already has its own ModernUO companion base and P41 holds the
engine read; keep the folder as the behavior reference for B2 onward (toggles, commands, rooms, pigeon), never convert it.

**Candidate in-game renames.**

| Source name | Why | Suggestion |
|---|---|---|
| Squire (mobile) | design ranks start at "Squire" (`BaseCompanion.cs:64`), so the name is already ours as rank 0 | keep as rank title only |
| Squire Contract | hiring deed | Companion's Writ (League) |
| Training Contract | reworked by decision | Drill Orders (design `:283`) |
| Room Attendant / Room Attendant Contract | kept by decision | Innkeeper's Ledger, Room Steward |
| Carrier Pigeon | kept, reworked | keep "Carrier Pigeon" (generic) |
| Squire Care Book / EC Squire Book | kept as League guide | Companion's Handbook |
| Squire Stats Spyglass, Squire Death Shroud, Squire Title gump | cut by decision | none needed |
| Squire Combat/Healing/Barding/Thieving Instructor | reworked as path trainers | Blade, Bow, Arcane, Support, Rogue Trainer (League) |

### pet-experience-scroll

**License:** none stated (SOURCE.txt). Pet Experience Scroll by Kirito (readme and file header credit Lucifer, "UO
Extinction"), servuo.dev archive 1257, posted and updated 2019-06-12, downloaded 2026-10-22. Credit Kirito and
Lucifer; private repo only; do not repost.

**1. What it does.** Six deed items that, when used on your own tamed pet, add a fixed lump of pet XP (10,000; 25,000;
50,000; 100,000; 250,000; 500,000) to a pet level system. It requires FS-ATS Gen 2's `Exp` and `NextLevel` fields on
BaseCreature. It would serve the evo pets and companions XP track.

**2. Overlap.** Shard XP tracks a deed could feed:

- **Evo pets:** `Mobiles/Evo/EvoPet.cs:39-40` (`_xp`), earned only from kills the pet damaged (`:241-258`,
  `OnCreatureDeath`), added through `AwardXp` (`:261-270`), which then calls `TryEvolve` and still respects the loop,
  Bond Trial and pick gates (`BlockFor`, `:273-291`). Stage totals 500 / 3,000 / 13,000 / 53,000
  (`Mobiles/Evo/EvoPetData.cs:215`). Staff already have `[EvoPet xp <amount>` (`EvoPetCommands.cs:17`, `:41`;
  `EvoPet.StaffAddXp`, `EvoPet.cs:401`).
- **Companions:** `Companions/BaseCompanion.cs:73-76` (`_xp`, "the leveling step writes it") and `:70-71` (`_level`).
  No code writes companion XP yet (grep finds only the field). The design says the climb to 100 is earned and each step
  above 100 costs a player's level scroll (`docs/companions/companions-squire-evo-research.md:171-172`), and it turned
  skill-setting contracts into Drill Orders that speed a re-climb without skipping it (`:283`).
- **Ordinary pets:** no XP or level. They have the ported pet training progress bar
  (`Services/Pet Training/TrainingProfile.cs:42` `TrainingProgress`, filled in battle by `CheckProgress` `:245`), which
  excludes EvoPet and PackMule (`Services/Pet Training/PetTrainingHelper.cs:154`), and the gain-speed multiplier
  (`ClusterFPetGainSpeed.cs`, 104 lines). Whether a `BaseCompanion` gets a training profile is (unverified).
- `PetMimic.cs` (1,686 lines) grows by feeding gems (`:70`), not XP; no overlap.

**Pinned has no pet XP or level.** `UOContent/Mobiles/BaseCreature.cs` (6,061 lines) has no `Exp`, `Experience`,
`NextLevel`, `TrainingProfile` or `PetTraining` (grep, 0 hits); `ControlSlots` is a plain saved field
(`:505-513`). The only "Experience" in UOContent is the dueling ladder (`UOContent/Engines/ConPVP/DuelContext.cs:886-897`).
The pet training the shard has is our port of ServUO's, not pinned's (`BaseCreature.PetTraining.cs` header).

Ours is far better: every target system already has its own award path with gates. This download is idea only.

**3. Port cost (counted).**

- **6 .cs, 720 lines** (120 each): PetEXPDeed10000.cs, PetEXPDeed25000.cs, PetEXPDeed50000.cs, PetEXPDeed100000.cs,
  PetEXPDeed250000.cs, PetEXPDeed500000.cs. `diff` shows they differ only in the class name, the amount and the label:
  one class with an amount field replaces all six.
- **Serialize/Deserialize overrides: 12** (6 + 6), each just a version int; becomes `[SerializationGenerator(0)]` with
  one `[SerializableField]` for the amount.
- **Dependencies:** FS-ATS Gen 2 (`c.Exp`, `c.NextLevel` on BaseCreature, `PetEXPDeed10000.cs:104`, `:111`). Neither
  exists in pinned (above). No XmlSpawner or XmlAttach. Unused `using Server.Menus`, `Server.Menus.Questions`.
- **Core or stock-file edits:** none needed for a rewrite; it would call `EvoPet.AwardXp` (shard) or a future companion
  award method. The original needs the FS-ATS BaseCreature edits, which we would not make.
- **Gumps: 0.** Art: stock deed graphic 0x14F0, hue 1050 (stock-ness unverified against our client).
- **ServUO types used, checked in pinned:** `Item` with `IsChildOf(IEntity)` (`Server/Items/Item.cs:4191`),
  `GetWorldLocation()` (`:4035`), `GetProperties(IPropertyList)` (`:874`; the ServUO `ObjectPropertyList` parameter
  becomes `IPropertyList`, `Server/PropertyList/IPropertyList.cs:22`); `Target(int, bool, TargetFlags)`
  (`Server/Targeting/Target.cs:12`) with `OnTarget(Mobile, object)` (`:216`); `Mobile.Target` (`Server/Mobiles/Mobile.cs:867`),
  `InRange(Point3D, int)` (`:3076`), `PlaySound` (`:6853`), `SendLocalizedMessage(int, ...)`
  (`Server/Mobiles/Mobile.Messages.cs:192`); `BaseCreature.ControlMaster` (`BaseCreature.cs:1184`), `Controlled`
  (field `:438`), `Summoned` (field `:487`). **Missing:** `Mobile.BodyValue` (0 hits in pinned); use `Body.IsHuman`
  (`Server/Mobiles/Body.cs:79`). `[Constructable]` becomes `[Constructible]` (`Server/Attributes.cs:105`).
- Rewrite size: about 60 lines, plus a fact.

**4. Risk.**

- **Exploit: it hands out progress, and it is tradeable.** Any deed is a free, sellable lump of XP. Against our evo
  table, the smallest deed (10,000) is worth twenty times stage 2's 500 and would take a fresh pet most of the way to
  stage 4 (13,000), although the loop gates in `BlockFor` would still hold it at stage 3 until the owner loops. On
  companions it would buy the climb the design says is earned (`:171-172`). On the F-12 ladder XP is the main currency,
  so a sold XP item is a gold-to-level shortcut.
- **Source bugs (do not copy):** operator precedence at `PetEXPDeed10000.cs:92`
  (`BodyValue == 400 || BodyValue == 401 && Controlled == false`) blocks every male human body even when controlled and
  only uncontrolled females, so it would refuse male companions and accept female ones. Another player's controlled pet
  falls through every branch with no message (`:96`, `:108`). The backpack check runs only at double-click (`:34`), never
  at target time, and `OnTarget` never checks `m_Deed.Deleted`. No dead or ghost check (a bonded ghost would take XP). The
  "NextLevel <= amount" guard (`:104`) refuses a deed whenever the pet is closer than its amount to a level, so big deeds
  are unusable near a level (FS-ATS semantics, unverified).
- **Who it targets:** the source checks only "your own controlled BaseCreature", so on our shard it would also hit
  companions, the Pack Mule and mimics if they shared a field. A rewrite must target one type (`EvoPet`) by design.
- Save compatibility, movement, combat, loot, skill gain: none touched by a rewrite that calls `AwardXp`; the original's
  FS-ATS fields would change BaseCreature's save.

**5. Verdict: `borrow the idea`, S.** The code is a 6x copy of one 120-line deed bound to FS-ATS; if Chase wants an XP
item at all, write one 60-line, owner-bound, gated deed that calls `EvoPet.AwardXp`, never the ServUO six.

**Candidate in-game renames.**

| Source name | Why | Suggestion |
|---|---|---|
| Pet Experience Scroll (all six, one name, told apart only by a property line) | generic and says nothing of evo pets; six identical names | one item: "Tamer's Tonic" or "Bond Draught" with the amount in the name, for example "Bond Draught (minor)", "(major)" |
| (companion variant, if wanted) | design already names the speed item | Drill Orders (design `:283`), not an XP lump |

## Bosses

### headless-horseman

**License.** None stated; original author unknown (uploaded by manwitch, 2020-04-22, "This is not my script"), last
used on RunUO 2.6. Provenance unclear: private repo only, credit the unknown author, do not repost.

**Files counted** (`wc -l`): HeadlessHorseman.cs 236, HessianSword.cs 56, PumpkinBomb.cs 119, PumpkinLantern.cs 111.
Total 4 files, 522 lines (SOURCE.txt says 526).

1. **What it does.** A mounted melee boss ("Ichabod Crane", 5,000 to 7,000 hits) on a Nightmare, in hued plate, who
   hits back for 5 to 15 on every damage he takes and, 5% of the time, throws 1 or 2 exploding pumpkins that blow up
   after 2 to 6 seconds for 5 to 15 fire around them. Drops a 1-in-20 Sword of the Hessian or Pumpkin Lantern.
   It serves a seasonal Halloween event (ClusterFSeasonalSwitch / the Halloween decor lane), or a F-30 Events tab boss.

2. **Overlap.**
   - Pinned has Halloween content already: `UOContent\Holiday Stuff\Halloween\2011\Mobiles\PumpkinHead.cs` (killer
     pumpkin, body 1246/1247, line 15), `2006\Engines\TrickOrTreat.cs`, `2012\Engines\PlayerZombies.cs`,
     `HolidaySettings.cs`. No Headless Horseman in pinned (grep "Horseman" finds nothing) or in ServUO pub57.
   - The shard has the season machinery: `ClusterFSeasonalSwitch.cs` (one switch per season, Halloween default
     10-24 to 11-02), `ClusterFHalloweenDecorSeeder.cs`, `Items\Decorative\PumpkinCarvingKit.cs`.
   - **The faithful option exists in ServUO and not on the shard:** OSI's Treasures of Sorcerer's Dungeon seasonal
     event, `ServUO-pub57\Scripts\Services\Seasonal Events\TreasuresOfSorceresDungeon\` (Jack the Pumpkin King 271
     lines, Headless Elf, plus spawner, researcher and reward gump). Neither pinned nor the shard has
     `JackThePumpkinKing` (grep). Under docs\fidelity-principle.md that is the first lane for an OSI Halloween boss.
   - The pumpkin bomb is a small idea worth keeping for a custom boss; the rest (a stat block on plate armor) is
     plain. Ours is not "better" here; we simply have no Halloween boss yet.

3. **Port cost.**
   - 4 .cs, 522 lines; **5 Serialize/Deserialize pairs** (HeadlessHorseman, HessianSword, PumpkinBomb, PumpkinLantern,
     PumpkinLantern.InternalItem) to source-generated serialization. No XmlSpawner, no core or stock-file edits, no
     gumps.
   - Missing type: `Tamingcoins` (`PackItem(new Tamingcoins(1000))`, HeadlessHorseman.cs) is not in the download;
     drop it.
   - API mapping, all present in pinned: `Timer.DelayCall<T>(TimeSpan, Action<T>, T)`
     (`Server\Timer\Timer.DelayStateCall.cs:28`) for `TimerStateCallback`; the `PumpkinTimer` subclass becomes
     `Timer.StartTimer(delay, callback, out TimerExecutionToken)` (`Server\Timer\Timer.DelayCall.cs:87`) or a
     DelayCall; `ICarvable.Carve(Mobile, Item)` (`Server\Interfaces.cs:16-19`) matches; `AOS.Damage(Mobile, Mobile,
     int, ...)` (`UOContent\Misc\AOS.cs:34`); `BaseMount.Rider` (`UOContent\Mobiles\Animals\Mounts\BaseMount.cs:77`);
     `Nightmare` (`UOContent\Mobiles\Animals\Mounts\Nightmare.cs:7`); `Lantern` (`UOContent\Items\Lights\Lantern.cs:7`);
     `LootPack.UltraRich` (`UOContent\Misc\LootPack.cs:507`).
   - Art: body 185 is the male Savage Rider body (pinned `UOContent\Mobiles\Monsters\Humanoid\Melee\SavageRider.cs:21`),
     so the "headless" rider has a head and war paint unless hue 0x4001 hides it (unverified; check in game). Items
     0xC6A/0xC6B are stock pumpkins (pinned `Holiday Stuff\Halloween\2006\Items\HalloweenPumpkin.cs`), 0x1647 a stock
     light source (pinned `UOContent\Items\Lights\LightSource.cs`). Sounds 0x47F to 0x486, 0x48F, 0x491, 0x44A are
     un-named in the script (unverified which creature they belong to). Hues 1345, 1175, 0x497, 0x4001 (unverified).

4. **Risk.**
   - Save compatibility: new types only; no change to existing saves.
   - Combat: `OnDamage` reflects 5 to 15 physical to *any* attacker (pets, summons, spells) on every hit, guarded
     by a `static bool`; fine for one boss, but it is a hidden rule players cannot look up (custom lane, wiki entry).
   - Gold faucet: carving a live pumpkin bomb gives 25 to 100 gold 30% of the time. Bombs only appear while the boss
     is being hit, so the faucet is small, but a tank-and-carve loop is possible; drop the gold.
   - Loot balance: the Sword of the Hessian is far above OSI artifacts (45 DI, 25 SSI, 50 Hit Fireball, 40 Hit Fire
     Area, 40 HLA, 50 HLD, 20 HCI, SC, 255 durability, self repair) at 1-in-20. Rebalance or replace before use.
   - Bug: PumpkinLantern keeps a second `InternalItem` (a pumpkin) that follows the lantern's location and map; when
     the lantern sits in a backpack the follower is likely placed in the world at container coordinates (unverified,
     reading of `OnLocationChange`/`OnMapChange`). Redesign as one light item.
   - Name: corpse "the corpse of Ichabod Crane" and Name "Ichabod Crane" are the wrong character (Ichabod is the
     schoolteacher in Irving's 1820 story, public domain; the rider is unnamed there).

5. **Verdict: `borrow the idea`, S.** A good shape for a custom seasonal boss (rider + pumpkin bombs on the Halloween
   switch), but the code is a 500-line stat block with a bad sword and a buggy lantern; a native rewrite is about the
   same cost as a port. Ask Chase first whether the OSI Pumpkin King event should come first (fidelity lane).

**Rename candidates.** "Ichabod Crane" to **the Hollow Rider** (or **the Lantern Rider**, **the Hessian of Yew**);
corpse "the Hollow Rider's remains". "Sword of the Hessian" to **Hollow Rider's Blade**. "Exploding Pumpkin Head" is
fine. "Pumpkin Lantern" collides in spirit with stock jack-o'-lanterns; **Rider's Lantern**.

---

### quetzalcoatl-armor-mob

**License.** None stated. Candy Apple, 2019-12-21. Community work: credit Candy Apple, private repo only. Items made
with "Gizmo's Uo Quest Maker" (file headers).

**Files counted** (`wc -l`, folder `DeityQuetzalcoatlArmor\`): DQChest 70, DQClaw 58, DQDante 217, DQDeity 59, DQFang
81, DQFChest 69, DQHead 69, DQLegs 68, DQScales 65. Total 9 files, 756 lines (SOURCE.txt says 757).

1. **What it does.** One boss, "Deity Quetzalcoatl Dante" (120,000 hits, mage AI, fire breath, two timed AoE
   abilities, pets deal 1/2 to 1/7 damage), on `BaseSABosses` with SA artifact lists, plus eight unique gear pieces
   (chain chest, female plate chest, plate legs, plate gorget, leather cap, gold bracelet, gold earrings, scimitar)
   hued 2499, meant to be placed as XmlSpawner loot. SOURCE.txt calls it a levelable armor tier; nothing in the code
   levels, and there is no set bonus.
   It would serve a boss with an armor reward (F-40 boss boxes, League hunts F-24).

2. **Overlap.**
   - **Body correction:** the boss is not on the Stygian Dragon body. `DQDante.cs` sets `Body = 1289`, which is the
     Najasaurus (Time of Legends) body: ServUO `Services\Expansions\Time Of Legends\Mobiles\Najasaurus.cs:16` and the
     shard's own port `Mobiles\Normal\Najasaurus.cs:11` (`Body = 1289`, `BaseSoundID = 219`, the same sound DQDante
     uses). The Stygian Dragon body is 826 (shard `Mobiles\Bosses\StygianDragon.cs:46`, noted there as a bodyTable.cfg
     row). The shard already ships a Najasaurus on 1289, so the client draws it (unverified against the client files,
     but the shard creature is in use).
   - The shard's ported StygianDragon (`Mobiles\Bosses\StygianDragon.cs`, on `BaseSABoss`,
     `Mobiles\Normal\BaseSABosses.cs:25`) already does the same job faithfully: crimson meteor (`:130`, `:153`),
     stygian fireball, fire column, SA artifact drops. DQDante is a reskinned, 4x-hit-point copy of it. **Ours is
     better; this is not even an idea worth taking.**
   - Boss gear rewards: F-40 boss boxes (feature-queue F-40, "box gear is always weaker than exceptional crafted gear
     ... and never levelable") and `LootBoxes\` cover the reward lane with explicit balance rules this set breaks.

3. **Port cost.**
   - 9 .cs, 756 lines; **9 Serialize/Deserialize pairs**. No gumps. XmlSpawner only as the intended drop placement (no
     code reference; grep finds none).
   - Missing dependencies (not in the download, not in pinned or the shard by grep): `Ability.FlameCross` and
     `Ability.CrimsonMeteor` (no `FlameCross` in ServUO pub57 either; a third-party helper), `EvolutionDragon`,
     `EvoMerc`, `EvolutionTree`, `EvolutionTiger`, `EvolutionDaemon` (in `AlterMeleeDamageFrom`), `QLPoints` (ServUO
     Queen's Loyalty). `BaseSABosses` maps to the shard's `BaseSABoss`.
   - Art: body 1289 (see above), item bases stock. Hue 2499 (unverified).

4. **Risk.**
   - Loot balance is the whole problem: Quetzalcoatls Fang is a scimitar with 13 hit effects (HitDispel 100, five
     area effects at 50, three spell procs at 50, 75 HLL), Luck 1000, 25 RPD, HCI 25 / DCI 35; the cap has +20
     Spellweaving and +20 Resist, Luck 1000, 35 RPD. Each piece is beyond any OSI artifact; one piece breaks PvP and
     PvM balance and the luck ceiling.
   - The pet-damage nerf hard-codes custom evo pet types.
   - Save compatibility: new types only.

5. **Verdict: `skip`, S.** The boss is a copy of our faithful StygianDragon on the wrong body, and the gear violates
   F-40's stated balance rule. Nothing to keep beyond "a Najasaurus-bodied Eodon boss" as a bare idea.

**Rename candidates (if ever used).** Quetzalcoatl is a real Mesoamerican deity, still revered; do not name a
killable monster after it. The body is Eodon's, so an Eodon name fits: **Xal'teca the Plumed Wyrm**, **the Feathered
Serpent of Eodon**, or **Coatl Rex**. Item names "Fangs Of A Deity", "Scales Of A Deity", "QuetzalcoatlsClaw" (no space)
would follow the boss name.

---

### world-boss-in-a-box

**License.** None stated. Tailean, 2019-01-21, made for the "Arth Legacy" shard's month-long event. Community work:
credit Tailean, private repo only.

**Files counted** (`wc -l`, folder `Arth Legacy Event\`): EventWorldBossSummoner.cs 72, RubyDragon.cs 113,
TameableRubyDragon.cs 113, WeaversTribalMask.cs 168. Total 4 files, 466 lines (SOURCE.txt says 468).

1. **What it does.** Staff put a "World Boss Summoner" crystal on monsters; whoever loots it double-clicks it to spawn
   "an ancient ruby red dragon" (Ancient Wyrm body 46, 9,500 to 10,000 hits, 8x UltraRich) at their feet. The dragon
   drops a Spellweaving mask 10% and a crystal for a tameable copy of itself 30%.
   It serves the F-30 Staff Hub Events tab (GM-run events with a named boss) and F-24's "investigation spawns a
   temporary mini boss".

2. **Overlap.**
   - F-30 Events tab (feature-queue F-30 point 4): surges with "a named boss with adds", every creature flagged as
     event spawn, End deletes leftovers, restart cleans up. That design is already more complete than this item.
   - F-24 (confirmed 2026-10-03): the dive "investigation" mini boss spawns for the job holder's party and despawns if
     not engaged; same mechanic with the safety this item lacks.
   - PORT-ASSESSMENT.md (P93): Invasions "borrow the idea only", Apex Hunt "port later as the F-24 hunt skeleton";
     a world-boss token sits beside both and adds only the "player carries the trigger" twist.
   - The boss itself is pinned's AncientWyrm stats raised (`UOContent\Mobiles\Monsters\Reptile\Magic\AncientWyrm.cs:11`,
     `Body = 46`). **Ours (the designed F-30/F-24 mechanics) is better; this is idea only.**

3. **Port cost.**
   - 4 .cs, 466 lines; **4 Serialize/Deserialize pairs** (the mask saves `Charges` and `ChargeTime`). No XmlSpawner in
     code, no core edits, no gumps.
   - **Does not compile as shipped:** `TameableRubyDragonCrystal` is referenced (RubyDragon.cs:74) and defined nowhere
     in the folder.
   - API: `GiftOfRenewalSpell(Mobile, Item)` exists (pinned `UOContent\Spells\Spellweaving\GiftOfRenewal.cs:19`);
     `Timer.DelayCall(TimeSpan, TimeSpan, TimerCallback)` maps to `Timer.StartTimer(..., out TimerExecutionToken)`
     (`Server\Timer\Timer.DelayCall.cs:91`); `World.AddMobile` plus setting Location/Map becomes `MoveToWorld`.
   - Art: summoner item id 40123 = 0x9CBB (used by ServUO `Quests\Eodon\MyrmidexThreat\Items\Rewards.cs` and the
     Ultima Store, so a 7.0.x art tile; unverified in our client); mask 0xA1C7 is OSI's Mask of Khal Ankur (ServUO
     `Services\Seasonal Events\TreasuresOfKhaldun\Items\MaskOfKhalAnkur.cs`; unverified in our client). Hues 1964,
     2498 (unverified).

4. **Risk.**
   - **Spawn anywhere:** the backpack and range checks are commented out, so the crystal works from the ground, at a
     bank, in a house, in New Haven; it also always prints "That is too far away" after summoning (the `else` block is
     unconditional). An AlwaysMurderer 10k-hit dragon dropped in a guard zone or on a crowd is griefing.
   - **Farming/hoarding:** the crystal is a normal movable item, so it can be hoarded, traded and chained (boss drops
     tameable crystals 30%); nothing ties it to an event window.
   - Pets: the tameable copy has `ControlSlots = 6` while pinned's default FollowersMax is 5 (`Server\Mobiles\Mobile.cs:6442`);
     only a loop-raised FollowersMax (`Companions\CompanionParty.cs:81`) could hold it. Its corpse says "a black dragon
     corpse".
   - Mask bugs: `OnDoubleClick` casts Gift of Renewal even when not equipped and while on cooldown (the checks fall
     through), never spends a charge, and decrements ChargeTime on each click; +30 Spellweaving and 30 SDI on a hat.
     It also returns OSI's label 1158701 "Mask of Khal Ankur" (overridden by Name, but a clash).
   - Save compatibility: new types only.

5. **Verdict: `borrow the idea`, S.** "A boss token found in the world that a player uses to call an event boss" is a
   fun F-30 Events option (staff-issued or event-dropped, bound to the event, usable only in set places, the boss
   flagged event spawn). The code itself is broken in three places and adds nothing the F-30 design lacks.

**Rename candidates.** "an ancient ruby red dragon" is fine as a custom name (OSI has no ruby dragon) but the tameable
copy must not share it: **a ruby drakeling** or **a ruby wyrmling**. "Weavers Tribal Mask" should drop the Khal Ankur
label: **Ruby Weaver's Mask**. "World Boss Summoner" to **Ruby Call Crystal**. "Arth Legacy" is another shard's name;
drop it.

---

### summoning-system-v2

**License.** None stated. TwilightRaven, 2018-10-06, "beta, desperately needs testing", the enemy summoner unfinished.
Community work: credit TwilightRaven, private repo only. Two `.lnk` shortcuts in the folder, not opened.

**Files counted** (`find -name *.cs`, `wc -l`): 93 .cs, 24,922 lines.

| Folder (under `Summoning v2.0\`) | Files | Lines |
|---|---|---|
| top level: BaseCreature.cs 7,852; SpellHelper.cs 1,688; Spellbook.cs 1,410; Initializer.cs 284; Reagent.cs 274; SpellRegistry.cs 185 | 6 | 11,693 |
| `Mobiles\`: SummonerAI.cs 463, EvilSummoner.cs 165 | 2 | 628 |
| `Summoner\`: SummonerCommandList.cs 475, SummonerSpellbook.cs, SummonerSpellbookGump.cs | 3 | 638 |
| `Summoner Scrolls\` (one per summon, e.g. StygianDragonScroll.cs) | 26 | 1,172 |
| `Summoner Spells\` (26 spells, SummonerSpell.cs, SummoningSpell.cs) | 28 | 3,289 |
| `Summoner Spells\Creatures\` (26 Summoned* creatures, largest SummonedMedusa.cs 818) | 26 | 7,364 |
| `Vendor\`: SummonerVendor.cs, SBSummonerVendor.cs | 2 | 138 |

Sampled, not read line by line: SummonerSpell.cs, SummoningSpell.cs, StygianDragonSpell.cs, StygianDragonScroll.cs,
SummonedStygianDragon.cs, SBSummonerVendor.cs, the command list, EvilSummoner and SummonerAI headers, the spellbook
gump, plus a diff of the six stock files against ServUO pub57.

1. **What it does.** "Final Fantasy" summons: 26 scrolls/spells (ids 800 to 825) each call a copy of a famous boss
   (Stygian Dragon, Medusa, Dread Horn, Lady Melisande, Ancient Wyrm, Serado, ...) next to the caster to fight for it.
   Scrolls are sold by a Summoner vendor at 1,500 gold each and a 60,000-gold Summoner's Spellbook; players can also
   cast by `.SummonX` commands. An unfinished EvilSummoner NPC with a SummonerAI is meant to use them against players.
   It would serve a League rank reward (F-24) or an event power-up.

2. **Overlap.**
   - The shard already has faithful ports of 9 of the 26 bosses it copies: `Mobiles\Bosses\` ChiefParoxysmus,
     CrimsonDragon, LadyMelisande, Medusa, MonstrousInterredGrizzle, SlasherOfVeils, StygianDragon; `Mobiles\Named\`
     SkeletalDragonRenowned, Tempest. Pinned has 13 more (LordOaks, Silvani, Meraktus, Serado, Rikktor, Neira,
     Barracoon, Mephitis, Malefic, ServantOfSemidar, SirPatrick, ShadowKnight, AncientWyrm; e.g.
     `UOContent\Mobiles\Special\Serado.cs`). The other 4 (DreadHorn, PrimevalLich, AbyssalInfernal,
     ShimmeringEffusion) are in neither (grep). The 26 `Summoned*` files are stale copies of those with loot left on.
   - Pinned's summon API covers what the spells need: `BaseCreature.Summon(creature, controlled, caster, p, sound,
     duration[, onUnsummon])` (`UOContent\Mobiles\BaseCreature.cs:3808-3830`), which refuses past FollowersMax.
   - Shard follower slots already run through `Companions\CompanionParty.cs` (companions and pets share FollowersMax).
   - **Ours is better on every creature; the only new thing is the idea of a timed boss summon as a reward.**

3. **Port cost.**
   - 93 .cs, 24,922 lines, of which **11,693 lines (6 files) are whole replacements of ServUO stock files**:
     BaseCreature.cs (2,653 differing lines vs pub57 `Scripts\Mobiles\Normal\BaseCreature.cs`, an older ServUO copy
     with XmlSpawner2 attachments at :17, :1260, :1404), SpellHelper.cs (717), Spellbook.cs (183, adds
     `SpellbookType.Summoning` and also Druid), SpellRegistry.cs (array 745 to 817), Initializer.cs (registers Druid
     spells 301 to 320 and summons 800 to 825), Reagent.cs (adds 8 Druid reagent types). None of these can be
     dropped onto ModernUO; each change would be a hand edit of a pinned stock file (pinned's registry is
     `new Type[700]`, `UOContent\Spells\Base\SpellRegistry.cs:8`, so ids 800+ need a stock edit; pinned's
     `SpellbookType` enum has no free custom entry, `UOContent\Items\Skill Items\Magical\Spellbook.cs:16-26`).
   - **61 Serialize/Deserialize pairs** (57 files; SOURCE.txt's 61 matches). 1 gump (SummonerSpellbookGump) to
     rewrite to pinned's gump API.
   - **Hidden dependency:** every spell `using Server.Spells.Druid;` and the stock-file edits reference a Druid spell
     system that is not in the download.
   - XmlSpawner2 (in the replaced BaseCreature only). Global command change: `SummonerCommandList.Initialize` sets
     `CommandSystem.Prefix = "."` for the whole server (pinned default "[" at `Server\Commands.cs:154`).
   - Art: Summoned Stygian Dragon on body 826 (as the shard's own, a bodyTable.cfg row per shard
     `StygianDragon.cs:2`); scroll 0x1F4D, book 0xEFA, stock (unverified in our client); hues 0x58B, 1419, 1164
     (unverified).

4. **Risk.**
   - **Exploit, loot from summons:** 25 of 26 summoned creatures keep `GenerateLoot` and/or an `OnDeath` drop
     (SummonedStygianDragon: 4x AosSuperBoss plus 8x Gems, and an unconditional `StygianDragonHead` in OnDeath). Pinned
     skips kill-time loot for summons (`!Summoned` at `BaseCreature.cs:3241` and `:3283`) but still runs
     `GenerateLoot(true)` at construction (`:864`) for spawn-time pack items, and OnDeath overrides run regardless; a
     friend killing your 30,000-hit summon could farm boss trophies (unverified end to end).
   - **Balance:** each spell is a First-circle MagerySpell costing 2 follower slots for a 30,000-hit boss with
     Bladeweave and meteor AoE; duration is hard-coded 20 seconds (the computed `duration` is ignored), scrolls cost
     1,500 gold from a vendor. It turns any mage into a boss-killer and trivializes every encounter it is used in.
   - Book holds only 16 of 26 spells (`BookCount 16`, offset 800); ids above 816 overflow the edited registry.
   - Global edits: the replaced BaseCreature/SpellHelper would silently revert dozens of ServUO fixes (the diff shows
     removed VvV, Virtues, LockDirection, FurType, Aggression code), i.e. it touches combat, loot and skill gain
     globally. Command prefix change breaks every staff habit and our docs.
   - Save compatibility: new types plus the Spellbook/BaseCreature edits would change stock serialization.

5. **Verdict: `reference only`, L.** Keep the idea ("call a short-lived boss echo as a reward") for Chase to decide;
   the code is a beta built on replaced stock files, a missing Druid system and XmlSpawner, and every creature it
   summons already exists on the shard or in pinned. If wanted, a native version is one item plus one wrapper creature
   (S to M), not a port.

**Rename candidates (if the idea is used).** A summoned copy must not share the real boss's name or players will
read "Stygian Dragon" kills and drops wrong: **Echo of the Stygian Dragon**, **Shade of Medusa**, **Spectral Serado**
(pattern: "Echo of X"). "Summoner's Spellbook" clashes with OSI's Summoner's Kilt and the Spellweaving summons;
**Tome of Echoes**. "Evil Summoner" / "Watcher of the Summoners" to **Echo-Caller**.

---

## Levelable gear

#### Engine facts used below (pinned, verified)

- **No XmlSpawner attachment engine.** A grep of `Projects\` for `XmlAttach|XmlSpawner|XmlAttachment` hits one file,
  `UOContent\Engines\Spawners\Commands\ImportSpawnersCommand.cs`, which imports XmlSpawner's spawner XML files
  (`:86`, `:112`, `System.Xml`). There is no `XmlAttach`, no `XmlAttachment`, no `XmlAttach.CheckCanEquip`.
- **No imbuing engine.** `Imbuing` appears only as a skill name (`Server\Skills.cs:75`, `:764`) and its cliloc
  (`UOContent\Misc\AOS.cs:1338`). The shard's own imbuing is `SL\customizations\Imbuing\` (6 files) plus
  `SL\patches\Imbue-custom-property-hooks.patch`.
- **No socket or augment system.** A grep for `Augment` in pinned `.cs` returns nothing; `Socket` hits only networking
  (`Server\Events\SocketConnectionEvent.cs`, `UOContent\Misc\ServerList.cs`, and so on).
- **Equip gate.** `Item.CanEquip(Mobile)` is virtual at `Server\Items\Item.cs:2251`; `Mobile.EquipItem` calls it at
  `Server\Mobiles\Mobile.cs:7800-7802`. Overrides: `UOContent\Items\Armor\BaseArmor.cs:1055`,
  `UOContent\Items\Weapons\BaseWeapon.cs:1005`, `UOContent\Items\Clothing\BaseClothing.cs:413`. `BaseJewel`
  (`UOContent\Items\Jewels\BaseJewel.cs:22`) has no override and inherits Item's.
- **Damage hook.** `Mobile.OnDamage(int amount, Mobile from, bool willKill)` at `Server\Mobiles\Mobile.cs:5950`, called
  from `Damage` at `:6009`. Overridden in `UOContent\Mobiles\PlayerMobile.cs:2347` and `UOContent\Mobiles\BaseCreature.cs:1941`.
- **Death event.** `CreatureEvents.CreatureDeathEvent` fires at `UOContent\Mobiles\BaseCreature.cs:3540` and `:3669`.
- **Tooltips.** `Item.GetProperties(IPropertyList)` at `Server\Items\Item.cs:874`, `AddNameProperties` at `:2029`
  (ServUO's `ObjectPropertyList` signatures do not compile here). `Item.ExtraProperties` is **not** pinned; the shard adds
  it in `SL\patches\Imbue-custom-property-hooks.patch`.
- **EventSink.** Pinned has no `OnItemObtained`, `ItemCreated` or `OnItemUse` events (grep: 0 hits). Login is the
  generated `PlayerLoginEvent` (`UOContent\Mobiles\PlayerMobile.cs:1234-1235`).
- **Other APIs the ports would call:** `BaseCreature.Summon` overloads (`UOContent\Mobiles\BaseCreature.cs:3808-3821`),
  `SpellHelper.Heal(int, Mobile, Mobile, bool)` (`UOContent\Spells\Base\SpellHelper.cs:1044`), `GenericPersistence`
  (`Server\Serialization\GenericPersistence.cs:23`).

#### What the shard already has (shared context)

- **Levelable gear, built** (cc-P261, cc-P285): `SL\customizations\LevelGear\ClusterFLevelGear.cs` (791 lines),
  `LevelGearGump.cs` (112), `LevelGearCreatureResistances.cs` (15), `SmithsSealDeed.cs` (72). Crafted gear only
  (`WhyNot`, `ClusterFLevelGear.cs:341`), no field on any stock item (state by serial in `LevelGearStore : GenericPersistence`,
  `:222`), XP at creature death split by damage (`OnCreatureDeath`, `:455-456`, on pinned's `CreatureDeathEvent`),
  bonuses bought within imbuing ceilings and sharing imbuing's slot count (`:570`, `:586`), tooltip through
  `Item.ExtraProperties` (`:240`), every number a `clusterf.levelGear.*` setting. Design: `notes\cc-P72-level-items-research.md`.
- **Player levels (F-12) are not built.** `SL\customizations\Tutorial\ClusterFLoops.cs` records loops only;
  `ResetLevelAndSkillsForF12` is an empty hook. Creature levels and con colors exist (`SL\customizations\ClusterFCreatureLevels.cs`),
  with a provisional player level (best combat skill) behind `IPlayerLevelSource` (`:41`, `:98`).
- **No level gate on any gear.** `SL\customizations\ClusterFRequirements.cs` is the shared met / not-met gump style for
  upgrade menus (cc-P169), not an equip gate. `CanEquip` overrides in the shard are item-specific (ToeRings, ClimbingBoots,
  Glasses, BarreraakRing, PetMimic).
- **Rules that bind any port:** level requirements on **our** gear only, never OSI items; the newbie Tier 1 set has no
  requirement (`notes\f12-levels-loops-caps.md:112-115`). F-26 b gear attunement: Arms Lore lets a character use gear
  +5 levels above their current level at 100, +10 at 200 (`docs\feature-queue.md:2154`, approved at `:2166`).
  cc-P72 C.4 recommends item level kept, higher bonuses dormant, item always wearable. Only crafted gear is levelable
  (`docs\artificers-imbuing-design.md:101`).
- **Sockets in the shard:** only the mule's Imbued Barding Socket module (`SL\customizations\Mobiles\Mule\MuleModules.cs:238`,
  `:286`); nothing for player gear.
- **Earlier ruling:** P93 (`D:\UO\third-party\code\PORT-ASSESSMENT.md:328-341`) and F-12 (`docs\feature-queue.md:940`)
  rated Level System Extreme, the same author's later version of `level-system-3`, "borrow the idea only".

---

### level-system-3

**Source.** Level System 3 Rerelease, by Kamras. https://www.servuo.dev/archive/level-system-3-rerelease.1088/ Posted
2019-01-08, updated 2020-07-17; superseded by the author's Level System Extreme. Needs XmlSpawner and a ServUO older
than 2020-02-01.
**License: none stated.** Credit Kamras, private repo only, do not repost.

1. **What it does.** Player and pet levels with XP from kills, skill gains and bulk order turn-ins, stat and skill points
   spent in a stat-sheet gump, reset tokens, XP coins, level gates and tiles, vendors that only sell to a level, and
   equipment level requirements (either a per-type list or a "battle rating" computed from every property on the item).
   Serves F-12 and, for the gear gate, F-26 b.
2. **Overlap.** Levelable *items* are not in it; the shard's player-level work is designed (F-12, P282) but not built.
   Its gear gate is the only part the shard lacks. The F-12 entry already took the design from Level System Extreme, which
   is this package's successor with more features (P93 counted 55 files, 24,100 lines there); this older copy adds nothing
   new. Ours is better where it exists (LevelGear) and the rest is already reference material. Idea only.
3. **Port cost.**
   - **84 .cs, 19,287 lines** (file list below), plus `Core\Titles.cs.modified` (583 lines, a whole replacement of stock
     Titles.cs) and two text files.
   - **65 Serialize and 65 Deserialize overrides** to convert to source-generated serialization.
   - **XmlSpawner depth: total.** 71 of 84 files use the `Server.Engines.XmlSpawner2` namespace, 53 call `XmlAttach.*`,
     24 are `XmlAttachment` subclasses. The player's level, XP and points live in `XMLPlayerLevelAtt` (699 lines), pets in
     `XMLPetLevelAtt`, gear gates in `LevelEquipXML` / `LevelEquipXMLDynamic`. Nothing to keep without rewriting storage.
   - **Stock-file edits (11 files)** per `SetupInstructions - version 4-1.txt`: PlayerMobile.GetProperties (level line);
     BaseCreature.ApplyNameSuffix and a new GetProperties (creature and pet level); CraftItem (XP on craft); Titles.cs
     (paperdoll level, shipped as a whole file); SkillCheck.cs (XP on every skill gain, and `DisableSkillGain` returns before
     any gain for players); BaseVendor.UpdateBuyInfo (40 percent discount by vendor type); ConfirmBankPointsGump (BOD XP);
     BaseArmor, BaseWeapon, BaseJewel (`XmlAttach.AddAttachmentProperties`); BaseClothing (properties plus
     `XmlAttach.CheckCanEquip` in CanEquip). It also uses ServUO EventSink events pinned lacks (`OnItemObtained`,
     `ItemCreated`, `OnItemUse` in `Core\XMLItemlevelReq.cs:13-15` and `Core\LevelEquipXMLDynamicAttachToEquipment.cs:13-15`).
   - **Gumps to rewrite: 4** (`ExpBar`, `PetLevelGump` 713 lines, `PlayerLevelGump` 3,071 lines, `SkillResetGump` inside
     `Items\PlayerSkillResetToken.cs`).
   - **Art or client data:** none found; stock item IDs and gump art.
4. **Risk.**
   - **Save compatibility:** all player progress in attachments; no migration path to a ModernUO save.
   - **Global hooks:** XP on every kill (`XMLPlayerLevelAtt.OnKill`, `:494-524`, calling `LevelHandler.Set`); XP on every
     skill gain and an optional switch that turns skill gain off for every player (SkillCheck edit); a `CanEquip` check on
     every weapon, armor, clothing and jewel once the dynamic attachment is on (it attaches to all gear on create, obtain
     or use, "EVEN RARES", `Configuration\ConfiguredEquipment.cs`); a vendor price change.
   - **Bugs read in the code:** a player without the level attachment can equip nothing that carries the gate
     (`LevelEquipXMLDynamic.cs:168-172` returns false); the level 9 weapon tooltip prints the level 1 requirement
     (`LevelEquipXMLDynamic.cs:105`); a `new Configured()` is allocated on every tooltip, equip and kill.
   - **Design conflicts:** point-buy skills and stats, XP tokens and coins, and level vendors run against F-12's rules
     (P93 point 5); gating all gear breaks "our gear only".
5. **Verdict: `reference only`, L.** Same author and design as Level System Extreme, already ruled "borrow the design";
   the one useful extra is the battle-rating gate shape (see the open questions).

**Ideas worth writing down** (each needs our own code): the battle rating as a weighted sum of item properties
(`LevelEquipXMLDynamic.cs:612` onward, for example skill bonus x4, stat bonus x4, hit chance x2, cast recovery x10) mapped
by a threshold table to a required level (`ConfiguredEquipment.cs`, ten bands per item class); a mount level requirement;
a level gate tile (`Items\LevelReqTile.cs`, `Items\LevelGate.cs`).

**Files (84 .cs, 19,287 lines)**, under `Level_3_Master\`:
- `CommandsGumps\` (3, 3,896): ExpBar 112, PetLevelGump 713, PlayerLevelGump 3,071.
- `Configuration\` (6, 748): Configuration 181, ConfiguredEquipment 96, ConfiguredSkills 100, ConfiguredSkillsEXP 83,
  PetConfiguration 170, PlayerStatsConfig 118.
- `Core\` (6, 2,496): ExpTables.CS 424, LevelCore 629, LevelEquipXMLDynamicAttachToEquipment 75, LevelHandler 857,
  LevelHandlerPet 436, XMLItemlevelReq 75. (Not counted: `Titles.cs.modified`, 583.)
- `Equipment Example\` (13, 1,916): ChainCoifLevel 144, ChaosShieldLevel 134, KatanaLevel 173, RingmailArmsLevel 153,
  RingmailChestLevel 153, RingmailGlovesLevel 154, RingmailLegsLevel 151; `PlaceHolderEquipment\` Axe 126, Bow 163,
  Broadsword 140, Cutlass 138, Dagger 147, Longsword 140.
- `Items\` (11, 2,346): ExpCoin 147, ExpPowerHourToken 160, LevelGate 88, LevelReqTile 96, LevelSheet 120,
  PetLevelSheet 121, PlayerSkillResetToken 1,170, RaiseMaxLevelScroll.CS 95, SetLevelToken 143, SkillCoin 88,
  StatPointReset 158.
- `Utilities\` (1, 48): XMLDeleteLevelAttOnLogin.
- `Vendors\` (17, 2,686): LevelVendor10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 230, 250, 158 lines each.
- `XMLAttachments\` (27, 5,151): ExpPowerHour 59, LevelEquipXML 321, LevelEquipXMLDynamic 1,314, PlayerAttloop 101,
  PlayerAttloopDeleteOnLogin 36, XMLNewPlayer 93, XMLNewPlayerOnLogin 52, XMLPetAttacksBonus 593, XMLPetLevelAtt 644,
  XMLPlayerLevelAtt 699, XMLPlayerLevelAttOnLogin 45; `BonusStatFromPets\` 16 files (BonusStatAtt, 10, 20 ... 200, 201;
  73, 73, then 72 each; 1,154 total).

---

### xmlsockets

**Source.** XmlSockets v1.08a, by ArteGordon (2005, for XmlSpawner 3.26), uploaded by Dan.
https://www.servuo.dev/archive/xmlsockets.1070/ Posted 2018-10-31.
**License: none stated.** Credit ArteGordon, private repo only, do not repost.

1. **What it does.** Adds sockets to items and creatures and lets players fill them with augment items (71 augment
   classes: gems, crystals, runes, skulls, woods, stones) that raise item attributes, with player-added sockets gated by
   skill and resources (default Blacksmithy 100 and 50 valorite), a hammer to recover augments, and a Box of
   Transmutation with recipes. Serves no queued feature directly; SOURCE.txt suggests gem sockets on levelable gear.
2. **Overlap.** The shard's gear customization is imbuing (`SL\customizations\Imbuing\`, slot count in
   `ImbuingTable.Current.BaseSlots`) and levelable gear, which deliberately shares imbuing's slots
   (`ClusterFLevelGear.cs:570`, `:586`). Sockets would be a third parallel property channel. Transmutation recipes reroll
   power scrolls and BODs (`XmlSocketItems\BoxOfTransmutation.cs:62-79`), which collides with the shard's power scroll
   ladder (P282) and BOD systems. Pinned has no socket or augment system. Idea only, and only if Chase wants sockets.
3. **Port cost.**
   - **25 .cs, 11,293 lines** (list below).
   - **82 Serialize and 82 Deserialize overrides** (per file: Crystals 15, Radiantcrystals 14, Stones 10, Runeaugments 7,
     each of the other eight gem files 3, the rest 1).
   - **XmlSpawner depth: the core.** All 25 files are in the `Server.Engines.XmlSpawner2` namespace; the socket state is two
     attachments (`XmlSockets : XmlAttachment`, `Attachments\XmlSockets.cs:16`; `XmlSocketable`, `Attachments\XmlSocketable.cs:10`);
     5 files call `XmlAttach.*`.
   - **Stock-file edits (4)** per `XmlSockets Install NEW.txt`: BaseArmor, BaseWeapon and BaseJewel constructors call
     `XmlSockets.ConfigureRandom(this, 2.0, 0.1, 0.5, 3.0, 15.0, 50.0)`; BaseCreature.OnBeforeSpawn does the same for
     tamables (Veterinary 100, 30 emeralds).
   - **Gumps to rewrite: 2** (`SocketsGump` in `XmlSockets.cs:1210`, `TransmuteGump` in `BaseTransmutationContainer.cs`).
   - **Art:** stock only (augment icons gump 0x9A8 on 18 classes, item 0x2203 on 3).
4. **Risk.**
   - **Global loot:** the constructor edit runs on every weapon, armor and jewel ever constructed (loot, vendor stock,
     crafted), and on every tamable spawn: a 2 percent socket roll on everything.
   - **Save compatibility and item integrity:** augments write straight into the item's attributes (`+=` on augment, `-=`
     on recover, for example `XmlSocketItems\Augments\Rubies.cs:61-167`). If the attachment is lost or the numbers change,
     the bonus stays and recovery subtracts the wrong amount. This is the pattern cc-P72 B.1 rejected for LevelGear.
   - **Caps:** augments stack past imbuing ceilings and item intensity (for example `HitFireArea += 40`); the shard caps
     properties through the imbuing table.
   - **Creatures:** sockets on tamables alter pet stats outside the pet training work.
5. **Verdict: `borrow the idea`, M** for a native rebuild. If wanted, build sockets as a LevelGear-style registry by item
   serial, with augments read at aggregation time (the `AOS-level-gear-attribute-aggregation.patch` path), inside imbuing's
   ceilings and slot count, on crafted gear only, and no constructor roll.

**Files (25 .cs, 11,293 lines)**, under `XmlSockets\`: `Attachments\` XmlSocketable 241, XmlSockets 1,376;
BaseSocketAugmentation 156; BaseTransmutationContainer 444; `XmlSocketItems\Augments\` Amethysts 356, Crystals 1,650,
Diamonds 380, Emeralds 359, IAugments 22, Keyaugment 188, Radiantcrystals 1,544, Rubies 453, Runeaugments 517,
sapphires 360, Skulls 361, Stones 858, Tourmalines 359, Woods 238; `XmlSocketItems\` BagOfResources 163,
BoxOfTransmutation 809, ExceptionalSocketHammer 127, HammerOfRecovery 82, MagicBasket 99, SocketHammer 82,
TestSocketedWeapon 69.

---

### passive-item-system

**Source.** Passive Item System, by Natfoth. https://www.servuo.dev/archive/passive-item-system.1039/ Posted 2018-09-04.
**License: none stated.** Credit Natfoth, private repo only, do not repost.

1. **What it does.** Backpack items that fire an effect on a chance (default 5 percent, out of 10,000) with a cooldown
   when their holder deals or takes damage: summon a blade spirit or a dragon spirit, heal 15 to 39, call a lightning
   bolt, or drop 10 to 409 gold. Serves accessory or charm procs (no queued feature names it; a fit for accessories or
   levelable-gear rewards).
2. **Overlap.** The shard has accessory slots (`SL\customizations\Accessories\`, 7 files, `PlayerMobile-accessory-hooks.patch`)
   and pet abilities (`BaseCreature-pet-ability-hooks.patch`), but no carried-item proc system. Nothing does the same job;
   the code is small but incomplete (point 3), so take the idea.
3. **Port cost.**
   - **8 .cs, 941 lines** (list below). 8 Serialize and 8 Deserialize overrides. No XmlSpawner.
   - **The dispatcher is missing.** Nothing in the package calls `OnDamageGiven` or `OnDamageReceived`
     (grep: only the declarations and overrides), and ServUO-pub57 has no such call either (grep `Scripts`, `Server`: 0
     hits). The author's damage hook that scans the backpack was not shipped. A port needs one: the natural place is
     pinned's `Mobile.OnDamage` (`Server\Mobiles\Mobile.cs:5950`, called at `:6009`), which means a patch to the
     `PlayerMobile` (`:2347`) and `BaseCreature` (`:1941`) overrides, or a line in the shard's existing
     `SL\patches\AOS-damage-eater-hook.patch` site in `AOS.Damage`.
   - **Stock-file edits:** none shipped; one needed (above).
   - **Gumps:** 0. **Art:** stock (item 0xE73, hues).
   - Cooldowns use `System.Diagnostics.Stopwatch` (`BasePassiveItem.cs:17`, `:113-136`), which does not survive a restart
     correctly; rebuild on `Core.Now` timestamps. `BaseCreature.Summon` and `SpellHelper.Heal` exist in pinned
     (`BaseCreature.cs:3808-3821`, `SpellHelper.cs:1044`) but signatures differ from the ServUO calls (unverified per call).
4. **Risk.**
   - **Combat, global:** the hook runs on every damage event for every carrier, and items stack (each has its own
     cooldown; no per-mobile limit in the code). Lightning has a 10 second cooldown (`LightningImpPassiveItem.cs:54`).
   - **Gold faucet:** `GoldFinderPassiveItem` pays 10 to 409 gold (`Utility.Random(10, 400)` is from plus
     count, `ServUO-pub57\Server\Utility.cs:905-913`) on a 60 second cooldown (`GoldFinderPassiveItem.cs:53`, `:94`), on damage given or taken; in steady combat that is about one payout a minute per item (unverified rate).
   - **Summons:** the dragon spirit (796-825 Str, 478-495 hits, `PassiveDragonSpirit.cs:13-19`) has meat, hides and scales
     and no `DeleteCorpseOnDeath`, so killing your own summon may leave a carvable dragon corpse (unverified in pinned's
     summon death path). Summons check `SpellHelper.CheckTown` only.
   - "Not set up for PvP" per SOURCE.txt.
   - **Save compatibility:** new item types only; nothing stock changes.
5. **Verdict: `borrow the idea`, S.** Rebuild as a small proc framework on one damage hook, with a per-character cap,
   no gold proc, summons with `DeleteCorpseOnDeath`, and the procs data-driven if they become levelable-gear or accessory rewards.

**Files (8 .cs, 941 lines)**, under `PassiveItems\`: BasePassiveItem 161, BladeSpiritPassiveItem 90, DragonPassiveItem 88,
GoldFinderPassiveItem 106, HealingDruidPassiveItem 94, LightningImpPassiveItem 129, PassiveBladeSpirits 141,
PassiveDragonSpirit 132.

---

### equipment-level-requirements

**Source.** Equipment level requirements, by 13440130. https://www.servuo.dev/archive/equipment-level-requirements.1339/
Posted 2020-02-02. Shipped as whole replacements of BaseArmor, BaseWeapon and BaseJewel.
**License: none stated.** Credit 13440130, private repo only, do not repost.

1. **What it does.** Gives every weapon, armor and jewel a required player level computed from its properties (the
   "Colored Equipment Names" item score divided by 7 for armor and jewelry, 9 for weapons), refuses the equip below it, and
   shows "Level Need" in the tooltip (in Chinese). Serves F-26 b gear attunement and the F-12 gear-gate rule.
2. **Overlap.** Nothing in the shard gates gear by level yet (F-12 not built). The same idea is in `level-system-3`'s
   `LevelEquipXMLDynamic` in a more complete form (configurable bands per item class). Idea only, and the idea is
   already on file.
3. **Port cost.**
   - **3 .cs, 12,012 lines**, nearly all stock: BaseArmor 3,711 (pub57: 3,628), BaseJewel 1,576 (1,535), BaseWeapon 6,725
     (6,686). 3 Serialize and 3 Deserialize overrides, all stock.
   - **The files are not pub57.** A whitespace-insensitive diff against `D:\UO\ServUO-pub57\Scripts\Items\Equipment\Armor\BaseArmor.cs`,
     `...\Jewelry\BaseJewel.cs` and `...\Weapons\BaseWeapon.cs` gives +224/-141 lines in 39 hunks (armor), +102/-61 in 24
     (jewel), +257/-218 in 68 (weapon). Most is base drift: the author's files predate pub57's `IQuality`,
     `AosWeaponAttributes` on armor (pub57 armor save version 15, author 14), SearingWeapon-as-socket (pub57 weapon version 19,
     author 18), `LastParryChance`, `HitExplosion`, `EnchantedHotItemSocket`. Those are not the author's additions.
   - **The author's hunks** (line numbers in the author's files), identified by the add-on types they use:
     | # | File:line | Added |
     |---|---|---|
     | 1 | BaseJewel.cs:7 | `using Server.Engines.XmlSpawner2;` (armor and weapon already had it in stock) |
     | 2 | BaseArmor.cs:341-348, BaseJewel.cs:121-129, BaseWeapon.cs:803 area | context menu `LevelInfoEntry` when an `XmlLevelItem` attachment is present |
     | 3 | BaseArmor.cs:2359, BaseJewel.cs:537 | constructor `XmlAttach.AttachTo(this, new XmlSocketable(0))` (XmlSockets) on every armor and jewel |
     | 4 | BaseJewel.cs:554-582 | a commented-out 35 percent random `XmlLevelItem` roll in the constructor |
     | 5 | BaseArmor.cs:2419-2428, BaseJewel.cs:596-605, BaseWeapon.cs:1026-1035 | **the gate**: inside `CanEquip`'s `if (from.IsPlayer())`, `levelvalue = ItemNameHue.<Kind>ItemProps.Check<Kind>(this) / 7` (weapon `/ 9`), `PlayerMobile pm = (PlayerMobile)from; if (pm.Level < levelvalue) { SendMessage("等級不夠，無法裝備."); return false; }` ("level too low to equip") |
     | 6 | BaseArmor.cs:2687 onward, BaseWeapon.cs equivalent; BaseJewel.cs:803-824 | stock `AddNameProperty` commented out and replaced (resource name prefix computed but unused for armor; reforged prefix and suffix names dropped), a Colored Equipment Names prerequisite edit (unverified) |
     | 7 | BaseArmor.cs:2877-2895, BaseJewel.cs:847-865, BaseWeapon.cs:5521-5540 | new `GetProperties`: rarity line `list.Add(1042971, ItemNameHue...RarityLevelMod(this))`, and `XmlLevelItem` level/max and XP lines |
     | 8 | BaseArmor.cs:2961-2965, BaseWeapon.cs:5628-5632 | "未曾鑒定過的" ("unidentified") line when `!m_Identified` |
     | 9 | BaseArmor.cs:3106-3112, BaseJewel.cs:1041-1047, BaseWeapon.cs:6216-6222 | **the tooltip**: `list.Add("<BASEFONT COLOR=#FF00FF>等級需求:{0}...", levelvalue)` ("level requirement"), guarded by `if (levelvalue != null)`, which is always true for an int |
     | 10 | BaseJewel.cs:400, :407 | `InitMinHits` / `InitMaxHits` 0 to 80 / 130 (jewelry durability; authored or drift, unverified) |
     | 11 | CanEquip messages | three stock `SendLocalizedMessage(1071936)` replaced by English strings; likely drift (pub57 armor uses the same strings at `BaseArmor.cs:1501`, `:1510`), unverified |
     The level feature proper (hunks 5 and 9) is about 60 lines across the three files.
   - **Dependencies, none in the package and none in pinned:** XmlSpawner (`XmlAttach`), the XmlLevelItem add-on
     (`XmlLevelItem`, `LevelInfoEntry`, `LevelItems`; not in pub57, per cc-P72 A.0 an add-on from the ruaduck xmlspawner
     repository), XmlSockets (`XmlSocketable`), Colored Equipment Names v0.57.2 (`ItemNameHue`), and the Serbo level
     system (`PlayerMobile.Level`).
   - **Gumps:** 0. **Art:** none.
4. **Risk.**
   - **Equip, global:** the gate runs on every equip of every weapon, armor and jewel, OSI items included, which breaks
     the F-12 "our gear only" rule.
   - **Crash:** `IsPlayer()` in ServUO is `AccessLevel <= VIP` (`ServUO-pub57\Server\Customs Framework\Utilities\Utilities.cs:51-54`),
     true for creatures, and `Mobile.EquipItem` calls `CanEquip` (`ServUO-pub57\Server\Mobile.cs:11062`), so equipping any
     of these items on a non-PlayerMobile throws `InvalidCastException` at the cast in hunk 5.
   - **Save compatibility:** hunk 3 attaches an XmlSocketable to every new armor and jewel; replacing whole base files
     also replaces their serialization versions (armor 14, weapon 18 versus pub57's 15 and 19).
5. **Verdict: `skip`, S.** About 60 useful lines riding on five missing add-ons, with a crash; the same gate is better
   described by `level-system-3` and will be ours under F-26 b.

---

## New Haven and buildings

### conversational-townsperson

**Source.** David's Conversational Townsperson 1.1a, by David (RunUO), uploaded by Zavreyon,
https://www.servuo.dev/archive/davids-conversational-townsperson.1116/ , posted 2019-03-05, updated 2021-07-18.
**License: none stated**; credit David and Zavreyon, private repo only, do not repost. The `.rar` holds a
`Speech Rules Editor.exe` that stays zipped and is never run.

1. **What it does.** A `Townsperson` NPC (a `BaseCreature`) that, when a player speaks within 3 tiles, stops, faces
   them and answers from an XML "speech rules" database: a rule has trigger words and many responses, and a response
   is picked at random among those whose filters match (NPC attitude, NPC or player gender, time of day, region, NPC
   name, title or a free-text `Tag`, and whether the player carries a named item). A response can also animate, make
   the NPC attack, flee, turn criminal, hide, die or delete itself, give the player an item (or spawn a mobile), and
   consume a "quest object". Each NPC rolls a random wealth (poor, normal, rich) that picks a color-coordinated
   outfit, and normal or rich ones can teach one or two random skills. Serves: F-35's living New Haven, talking
   townsfolk and tutorial flavor.

2. **Overlap.**
   - Pinned has speech-driven NPCs but no general keyword-dialog database: `Mobile.HandlesOnSpeech` /
     `Mobile.OnSpeech` (`Server\Mobiles\Mobile.cs:6972`, `:6979`), `BaseCreature.OnSpeech`
     (`UOContent\Mobiles\BaseCreature.cs:2874`, `:2878`), `SpeechEventArgs` (`Server\Events\SpeechEvent.cs:21`), the
     player-set keyword topics of `PlayerBarkeeper` (`UOContent\Mobiles\Vendors\Barkeeper\PlayerBarkeeper.cs`), and
     NPC skill teaching (`BaseCreature.CanTeach` `:1464`, `CheckTeachSkills` `:4673`, `Teach` `:4808`).
   - The shard's NPC talk today is per NPC and gump-led: guildmaster speech triggers and the "Talk" entry
     (`cust\ClusterFGuildmasterExtension.cs:13-19`, through a `BaseGuildmaster` hook patch), the guild starter
     path (`cust\ClusterFGuildStarterPath.cs`), the tutorial recruiter and station gumps (`cust\Tutorial\TutorialRecruiter.cs`,
     `TutorialStations.cs`, `TutorialGumps.cs`), the New Haven ML quest givers placed by `cust\ClusterFNewHavenSeeder.cs`
     (19 entries), and the bulletin (`cust\ClusterFBulletin.cs`). Only 10 shard files override `OnSpeech`.
   - So the *idea* (one data file that lets many townsfolk answer "name", "job", "rumors", "time" with filtered,
     tagged responses) is new to us. Our gump-led tutorial is better for teaching; this is flavor on top.

3. **Port cost.**
   - Server code: **4 .cs, 1,613 lines**: `Townsperson.cs` 1,208, `SpeechDataHandlers.cs` 214, `ReplyList.cs` 95,
     `Logging.cs` 96 (all in `Townsperson_1.1a\Scripts\Custom\Townsperson\`).
   - Editor (reference only, not server code): **5 .cs, 6,868 lines** in `SpeechRulesEditor VB Source\SpeechRulesEditor\`:
     `SpeechRules.Designer.cs` 4,792, `Rules.cs` 1,662, `Response.cs` 347, `AssemblyInfo.cs` 58, `SpeechRules.cs` 9.
     Despite the folder name it is **C#, not Visual Basic**: a VS2005 WinForms project (`SpeechRulesEditor.csproj`,
     `ProductVersion 8.0.50727`, `OutputType WinExe`); there are no `.vb` files. Not built or opened.
   - Data: `Data\Rename.SpeechRules.xml` (2,386 lines; identical to the editor's `bin\Debug\Data\SpeechRules.xml`):
     **8 rules, 35 triggers, 113 responses**, generic chatter (rules: Default, Hello, GoodBye, AskedName, ToldName,
     Rumors, Occupation, Time); one response gives a candle. `EmptySpeechRules.xml` 344 lines (schema only).
   - Serialize/Deserialize: **1 pair** (`Townsperson.cs:997`, `:1009`, version 3: tag, weapon, staff, criminal flag,
     attitude, wealth) to convert to `[SerializationGenerator]`.
   - Dependencies: no XmlSpawner. `System.Data.DataSet.ReadXml` with an inline schema (`SpeechDataHandlers.cs:37`);
     `SpawnerType.GetType` for item names (pinned has `AssemblyHandler.FindTypeByName`, `Server\AssemblyHandler.cs:189`;
     no `SpawnerType` class in pinned).
   - **Blocker:** the lookup runs through `Delegate.BeginInvoke` (`Townsperson.cs:884`) and
     `System.Runtime.Remoting.Messaging.AsyncResult` (`:9`, the callback). Pinned targets `net10.0`
     (`Directory.Build.props:7`); delegate `BeginInvoke` is not supported on modern .NET and Remoting does not exist
     there (general .NET fact, not tested here). The worker also `Thread.Sleep`s up to 1.1 s
     (`SpeechDataHandlers.cs:204`) and the callback then calls `Say`, `AddToBackpack`, `Activator.CreateInstance`,
     `Kill` and `Delete` off the main thread. All of that has to become a synchronous lookup plus a
     `Timer.DelayCall` for the pause (`Server\Timer\Timer.DelayCall.cs:34`). With 35 triggers the lookup is trivial.
   - Gumps: **0**. Core or stock edits: **none**. Art or client data: **none**.
   - Logging is hard-wired to `Debug` (`Townsperson.cs:68`): every speech event writes a line to
     `Logs\Townsperson\<date>.log`.

4. **Risk.**
   - Save compatibility: new type, nothing to migrate.
   - Global: none (it only answers speech near itself), but it is `AI_Thief, FightMode.Closest` (`:193`) and fights
     back with a packed weapon.
   - **Exploit, reward race:** the "has the quest object" filter is checked when the request starts (on the worker),
     the reward is granted about 1.1 s later, and the consume result is ignored
     (`Backpack.ConsumeTotal(type, 1, true)`, `Townsperson.cs:979`). A player who drops or trades the item in that
     window still gets the reward. Any port must check and consume first, then reward, in one tick.
   - Data can name **any** type as a reward, including a mobile spawned at the NPC (`:930-946`): staff-only data,
     but no allow-list.
   - The "Hide" reaction sets the NPC's `AccessLevel` to GameMaster for 5 minutes (`:1100`).
   - Skill teaching: pinned's `CheckTeachSkills` refuses below 20.0 taught (`BaseCreature.cs:4690-4700`, base / 3);
     at our ~15x gain (F-9) a few points from a townsperson are harmless.

5. **Verdict: `borrow the idea`, M.** Write our own small "townsfolk talk" table (JSON in the shard's data, keyed by
   NPC tag and New Haven region, synchronous, our System/Echo voice rules) and reuse the rule model and filters; do
   not port the threaded DataSet code or the editor. The 113 starter lines are generic and would need rewriting for
   the shard's voice anyway.

**Rename candidates.** `ClusterFTownsfolk` (NPC), `ClusterFTalkRules` (data), `TownsfolkTag` for `Tag`.

---

### specialized-innkeeper

**Source.** Specialized Innkeeper, by Zigholtul, https://www.servuo.dev/archive/specialized-innkeeper.1324/ , posted
and updated 2019-12-23. **License: none stated**; credit Zigholtul, private repo only, do not repost.

1. **What it does.** A copy of the stock innkeeper that, when a player says exactly "rest", prices a full restore
   (missing hits + missing stamina + 2 x missing mana), asks the player to target someone within 12 tiles, takes the
   gold and sets that player's hits, stamina and mana to full with a sparkle effect. A context-menu entry opens a
   decorative gump that just says "Rest". Serves: the New Haven inn, and in spirit F-44 (the Inn as a place of rest).

2. **Overlap.**
   - Pinned's stock `InnKeeper` is 29 lines and only sells (`UOContent\Mobiles\Vendors\NPC\InnKeeper.cs:7-27`,
     `SBInnKeeper`). New Haven already gets one: pinned's post-UOML spawn data puts an `InnKeeper` spawner at
     3501,2517,27 in the Bountiful Harvest Inn (`Distribution\Data\Spawns\post-uoml\trammel\Vendors.json:662`, `:671`;
     the inn's region is 3493-3510, 2513-2530 per `notes\new-haven-quest-board.md:78`). The shard subclasses it once
     (`cust\ClusterFGargoyleVendors.cs:172`).
   - Healing services: the shard's Healer spawner (`cust\ClusterFNewHavenServicesSeeder.cs:193-200`).
   - Nothing in the shard heals for gold. The script adds one idea only; the vendor itself is identical to stock.

3. **Port cost.** **1 .cs, 292 lines** (`SpecializedInnKeeper.cs`; the `_zips\` copy is byte-identical).
   Serialize/Deserialize: **1 pair**. Gumps: **1** (90 `AddImage` calls of border art plus one HTML line, no
   function). No dependencies, no core edits, no art. A port is about 40 lines: a `partial` or subclass of pinned's
   `InnKeeper` with a speech hook and a confirm gump.

4. **Risk.**
   - **Double charge bug:** it consumes the fee with `pack.ConsumeTotal(typeof(Gold), toConsume)` and then again with
     `FindItemByType(typeof(Gold)).Consume(toConsume)` (`SpecializedInnKeeper.cs:87`, `:92`); pinned's `Item.Consume`
     deletes the whole pile when it holds less (`Server\Items\Item.cs:4402-4411`).
   - Operator precedence: only mana is doubled (`:58`), the comment talks of "3".
   - It refuses unless **all three** pools are below max (`:87`), then says "not enough gold".
   - **Combat exploit:** it full-heals any `PlayerMobile` within 12 tiles for gold, with no combat, aggressor or
     criminal check (`:69`, `:81-95`). Next to a town brawl or a guard-zone PvP spot that is an instant full heal plus
     full mana on demand. A port must refuse anyone in combat or recently aggressed, and self only.
   - Save compatibility: new type; nothing touches movement, loot or skill gain.

5. **Verdict: `borrow the idea`, S.** If Chase wants "rest at the inn", add it to the stock New Haven innkeeper (or
   a shard innkeeper type) with a fixed, sane price, a combat check and self-only; the code here is not worth
   carrying.

**Rename candidates.** "Rest" as a context entry on `InnKeeper`; `ClusterFInnRest`.

---

### skill-trainer-npc

**Source.** Skill Trainer NPC 1.3, by ImaNewb (file header credits "Delphi", v1.2),
https://www.servuo.dev/archive/skill-trainer-npc.1019/ , posted 2018-07-21, updated 2018-07-22. **License: none
stated**; credit ImaNewb, private repo only, do not repost.

1. **What it does.** A blessed, immobile NPC; say "train" within 12 tiles and it opens two gumps that let the player
   type any value 0-100 into any skill and 0-100 into Str, Dex or Int, checked only against a total of 700 skill and
   the stat cap. Charging 10,000 gold is commented out (`SkillTrainer.cs:80-101`), so as shipped it is free. Serves:
   play tester setup.

2. **Overlap.** Pinned already has staff commands `[SetSkill`, `[GetSkill`, `[SetAllSkills` at GameMaster
   (`UOContent\Commands\Skills.cs:10-12`); `[props` sets stats. The shard runs about 15x skill gain (F-9,
   `docs\feature-queue.md:586`) and the New Haven trainers and board (`cust\Engines\ML Quests\Definitions\NewHavenTrainerGuildLines.cs`,
   `notes\new-haven-quest-board.md`). Ours is better; nothing here is needed.

3. **Port cost.** **1 .cs, 457 lines** (`Skill Trainer\SkillTrainer.cs`). Serialize/Deserialize: **1 pair**.
   Gumps: **3** (`SkillTrainerGump`, `EditTrainerGump`, `StatTrainerGump`). No dependencies, no core edits, no art.

4. **Risk.**
   - As a player feature it is a free skill and stat editor: anyone who says "train" gets it.
   - The gumps are not closable (`:146`, `:422`) and never re-check distance to the trainer or that the trainer still
     exists, so a player can walk away with a working skill editor.
   - The 700 cap is hard-coded (`:263`) instead of the player's own skills cap; the list hides the last three skills
     (`:173-175`).
   - Changing skills directly bypasses skill gain, so it would flatten everything the guild path and the tutorial
     teach.

5. **Verdict: `skip`, S.** Play testers get `[SetSkill` / `[SetAllSkills` from staff, or a staff-only test command
   if that is too slow.

---

### archery-butte-hits

**Source.** Archery Butte that Shows Where Arrows and Bolts Hit, by Archaaz,
https://www.servuo.dev/archive/archery-butte-that-shows-where-arrow-and-bolts-hit-script-and-graphics.1340/ ,
posted 2020-02-04, updated 2020-02-05. **License: none stated**; credit Archaaz, private repo only, do not repost.
**FLAG: the art is EA's archery butte redrawn**: ship only as our own new item IDs in the player package.

1. **What it does.** A replacement `ArcheryButteAddon.cs` where each shot swaps the butte's item ID to a picture of
   the butte with one arrow or bolt in the ring that was hit (bullseye, inner, middle, outer, or stuck in the frame on
   a miss), for both facings; gathering the ammo switches it back. It shows only the latest shot, not all of them.
   Everything else (skill check -25 to +25, 4 to 6 tiles, lined up, scores, split arrows) is the stock butte. Serves:
   F-35's combat wing (P80 decided melee *and* ranged, F-44 notes), the New Haven training yard.

2. **Overlap.**
   - **Pinned already has it**: `ArcheryButte : AddonComponent` with `ArcheryButteAddon` and `ArcheryButteDeed`
     (`UOContent\Items\Addons\ArcheryButteAddon.cs:9`, `:298`, `:310`), source-generated, with the same practice rules
     (`:93-271`), plus a throwing-weapon branch the download lacks (`:55`). It does not change art.
   - Pinned decoration already places buttes in many towns, including two in `Distribution\Data\Decoration\Trammel\_haven additions.cfg:2-4`
     at 3744,2576,40 and 3747,2576,40 (whether that is inside New Haven's town region is unverified). The shard sells
     the deed as a Clean Up Britannia reward (`cust\Services\CleanUpBritannia\CleanUpBritanniaRewards.cs:186`).
   - A sibling art pack by the same author is already on disk: `D:\UO\third-party\archery-buttes\` (28 bmp,
     arrow1-14 and bolt1-14, P80 row 12, `notes\cc-P80-new-player-tutorial.md:256`). Pick one set.

3. **Port cost.**
   - Code: **1 .cs, 464 lines** (`Archery Butte\ArcheryButteAddon.cs`); the real delta from pinned is about 60 lines
     (the ID swaps). Serialize/Deserialize: **3 pairs** (butte, addon, deed); in a port they disappear (pinned's are
     generated). Gumps: 0. No dependencies.
   - **Do not replace the stock file.** Pinned's `FacingEast` is `ItemID == 0x100A` (`ArcheryButteAddon.cs:36`), so
     swapping the item ID would flip the butte's facing logic after the first shot. A port is a subclass (or a new
     component type) that stores its facing and its display state, so the stock butte and its saves stay untouched.
   - **Art, 24 bmp, 24-bit, black background** (the 20 butte frames are 66x81, the four loose sprites 44x33 or 44x32):
     - Arrows, east: `Arrow East Bullseye`, `Arrow East Inner`, `Arrow East Middle`, `Arrow East Outer`,
       `Arrow East Total Miss` (script IDs 0x7898-0x789C).
     - Arrows, south: `Arrow South Bullseye`, `Arrow South Inner`, `Arrow South Middle`, `Arrow South Outer`,
       `Arrow South Total Miss` (0x789D-0x78A1).
     - Bolts, east: `Bolt East Bullseye`, `Bolt East Inner`, `Bolt East Middle`, `Bolt East Outer`,
       `Bolt East Total Miss` (0x78A2-0x78A6).
     - Bolts, south: `Bolt South Bullseye`, `Bolt South Inner`, `Bolt South Middle`, `Bolt South Outer`,
       `Bolt South Total Miss` (0x78A7-0x78AB).
     - Loose sprites, not referenced by the script (the author's paste-in pieces): `East Arrow`, `South Arrow`,
       `East Bolt`, `South Bolt`.
     These are client art: every player needs them in the package, each with a tiledata entry copied from the stock
     butte (0x100A: "archery butte", Impassable; checked in `D:\UO\UltimaOnlineVanilla\tiledata.mul` with vseUOAware).
     The script's IDs 0x7898, 0x78A1 and 0x78AB have blank tiledata in that client (checked); the other 17 were not
     checked, and the shard should assign its own free IDs anyway.

4. **Risk.** Save compatibility is fine if it is a new type (pinned's butte saves are untouched). Skill gain is the
   stock butte's own `CheckSkill` window (`ArcheryButteAddon.cs:185`), unchanged. No exploit beyond stock: ammo comes
   back only on a non-split hit, as stock. Visual only: one arrow drawn, so two archers on one butte see only the last
   shot.

5. **Verdict: `port`, S (code) once the art route exists.** A subclass of pinned's butte with 20 new art IDs; it
   depends on F-8/F-21 proving that the updater ships new item art, and on choosing this set or the
   `third-party\archery-buttes` one.

**Rename candidates.** `ClusterFScoringButte` / `TrainingYardButte`.

---

### knives-town-houses

**Source.** Knive's Town Houses 3.01, by Knives (updated by Vorspire; SOURCE.txt says "Voxpire", the manual says
"Vorspire"), https://www.servuo.dev/archive/knives-town-houses.1277/ , posted 2019-09-09, updated 2022-10-09.
**License: none stated**; credit Knives and Vorspire, private repo only, do not repost. `Read.doc` is an RTF file;
read as text.

1. **What it does.** Staff use `[TownHouses` to turn any area (one or more rectangles, a Z range) into a house: a
   `TownHouseSign` stands for sale or rent with price, lockdowns, secures, ban spot, sign spot, buyer requirements
   (skill, total skills, young only, murderers) and an option to sell the decorations inside. A buyer gets a real
   `BaseHouse` subclass (`TownHouse`) over that area: the existing doors become house doors, lockdowns, secures,
   friends, bans and vendors work as in a house; rent is taken from the bank daily, weekly or monthly (rent-to-own
   optional) and on non-payment the belongings go to the bank in a bag. Owners can also sublet part of any house with
   a `RentalContract` ("create rental contract"). Serves: server-placed buildings sold or rented as player homes;
   asked about for F-44 (inn rooms) and F-49 (guild halls).

2. **Overlap.**
   - Pinned housing: `BaseHouse` (`UOContent\Multis\Houses\BaseHouse.cs:21`), `HouseRegion`
     (`UOContent\Regions\HouseRegion.cs:10`), `HouseFoundation` (custom houses, with a per-instance component list,
     `HouseFoundation.cs:117`), vendor rental contracts, `Banker.Withdraw` / `Deposit`
     (`UOContent\Mobiles\Townfolk\Banker.cs:158`, `:209`).
   - Shard: server-placed buildings are built from layouts by idempotent seeders (`cust\ClusterFRegistrarOfficeLayout.cs`
     and `...Seeder.cs`, `ClusterFGuildHallSeeder.cs`, `ClusterFMineCampLayout.cs`, `TutorialFarmLayout.cs` and 14 more
     `*Seeder.cs` / `*Layout.cs`), with staff tools planned from P93 (Visual Builder, Building Duplicator,
     `notes\cc-P98-building-duplicator.md`, `notes\cc-P100-visual-builder.md`), and `cust\Items\Functional\HouseCraftables.cs`
     for house items. P151 picked 14 stock buildings for guild halls (`notes\cc-P151-guild-halls-survey.md:43-63`). Custom
     regions exist (`cust\Regions\RootdeepVault.cs`, `cust\FountainOfYouth\FountainSanctumRegion.cs`).
   - None of ours makes a static building **player-owned**. That is the only thing Town Houses adds.
   - F-44 wants an **instanced** room reached through any Inn, one per character, weekly rent, no growth, closed when a
     real house is placed (`docs\feature-queue.md:3256-3276`). Town Houses claims a fixed world area, one owner, and
     counts as the account's house. It does not fit F-44 as is.
   - F-49 halls are guild headquarters run by NPCs, "server-placed buildings from existing UO tiles first"
     (`docs\feature-queue.md:3394-3428`). They are not player-owned, so no house system is needed; our seeders fit.

3. **Port cost.**
   - **25 .cs, 6,554 lines**: `Gumps\Error Reporting\` `Errors.cs` 83, `ErrorsGump.cs` 64, `ErrorsNotifyGump.cs` 25;
     `Gumps\Gumps Plus Light\` `BackgroundPlus.cs` 22, `ButtonPlus.cs` 50, `GumpPlusLight.cs` 280, `HTML.cs` 16,
     `HtmlPlus.cs` 22, `InfoGump.cs` 31; `Gumps\TownHouse Gumps\` `ContractConfirmGump.cs` 143,
     `ContractSetupGump.cs` 669, `TownHouseConfirmGump.cs` 75, `TownHouseSetupGump.cs` 1,186, `TownHousesGump.cs` 241;
     `Items\` `RentalContract.cs` 422, `RentalContractCopy.cs` 47, `RentalLicense.cs` 67, `SignHammer.cs` 316,
     `TownHouse.cs` 337, `TownHouseSign.cs` 1,872; `Misc\` `CommandInfo.cs` 38, `DecoreItemInfo.cs` 63,
     `General.cs` 247, `GumpResponse.cs` 132; `RUOVersion.cs` 106.
   - Serialize/Deserialize: **7 pairs** (`RentalContract`, `RentalContractCopy`, `RentalLicense`, `SignHammer`,
     `TownHouse`, `TownHouseSign`, `VersionHouse` in `RUOVersion.cs`). Pinned's `BaseHouse` still serializes by hand
     (version 15, `BaseHouse.cs:2910`, `:3004`), so a subclass can be generated or manual.
   - Gumps to rewrite: **9** (`ErrorsGump`, `ErrorsNotifyGump`, `InfoGump`, `ContractConfirmGump`, `ContractSetupGump`,
     `TownHouseConfirmGump`, `TownHouseSetupGump`, `TownHousesGump`, `SignHammerGump`) plus the `GumpPlusLight` base
     and its four helpers (about 2,700 lines of gump code in all).
   - Dependencies: no XmlSpawner, no Vita-Nex. `EventSink.Speech`, `ServerStarted`, `WorldSave` exist in pinned
     (`Server\Events\SpeechEvent.cs:62`, `Server\Events\EventSink.cs:42`, `Server\World\WorldEvents.cs:24`); the login
     hook becomes `PlayerLoginEvent` (pinned's pattern, `HouseRegion.cs:34`). `ScriptCompiler.FindTypeByFullName` becomes
     `AssemblyHandler.FindTypeByFullName` (`Server\AssemblyHandler.cs:186`).
   - **BaseHouse or HouseRegion edits?** The manual says none are required ("patches are optional"), and every member
     `TownHouse` overrides is virtual or abstract in pinned: `Area` (`BaseHouse.cs:336`), `BaseBanLocation` (`:337`),
     `IsInside(Point3D, int)` (`:1513`), `GetAosMaxSecures` (`:677`), `GetAosMaxLockdowns` (`:689`),
     `GetNewVendorSystemMaxVendors` (`:774`), `GetDeed` (`:3610`), `UpdateRegion` (`:1645`). But three things break on
     pinned and need our own code (read from source, not run):
     - **Shared component list.** `TownHouse` resizes `House.Components` (`TownHouse.cs:142-143`,
       `TownHouseSign.cs:797-798`), and pinned's `BaseMulti.Components` is `MultiData.GetComponents(ItemID)`
       (`Server\Items\BaseMulti.cs:88`), one cached list per multi ID (`Server\Client\MultiData.cs:52-53`). Every town
       house shares ID 0x1DD6, so each purchase rewrites the footprint of all of them. Fix: override `Components` with a
       per-instance `MultiComponentList` (`MultiData.cs:189`, `:637`), as `HouseFoundation.cs:117` does.
     - **Region area.** `RUOVersion.UpdateRegion` edits `Region.Area[i]` in place then re-registers
       (`RUOVersion.cs:47-58`); pinned's `Area` is a get-only array (`Server\Regions\Region.cs:212`). It compiles, but
       the clean route is overriding `BaseHouse.UpdateRegion`.
     - **No guard zone inside.** `HouseRegion` is built with no parent (`HouseRegion.cs:18`), and guards and town
       checks walk the parent chain (`Region.GetRegion<T>`, `Server\Regions\Region.cs:458`; used at
       `UOContent\Mobiles\PlayerMobile.cs:1811`, `BaseCreature.cs:3108`). A town house inside Britain would be outside
       the guarded region. Keeping town rules inside needs a `HouseRegion` change or a region of our own: a stock-file
       edit or a deeper rewrite (unverified in game).
   - Art or client data: none (uses stock sign and hanger IDs).

4. **Risk.**
   - **Decoration duplication.** With "keep items" on, buying with items makes the building's decorations movable
     lockdowns of the owner (`TownHouseSign.cs:903-909`); when the house is cleared, `RecreateItems` rebuilds every
     recorded decoration (`:1000-1032`). An owner who releases and carries off the decorations gets a fresh set back in
     the building and keeps the originals each cycle.
   - **Refunds from House.Price.** Pinned's demolish gump deposits `House.Price` (`UOContent\Gumps\Houses\ConfirmDemolishHouseGump.cs:103-108`)
     and the pack-up drops a bank check for it (`TownHouseSign.cs:1199`). For a bought house that is the price paid;
     for a rental it is 1; but staff (Counselor and up) buy without paying (`:738`, `:745`) and still get
     `House.Price = c_Price` (`:816`), and changing `Price` on an owned sign is allowed. Gold can be minted by any path
     where `House.Price` exceeds what was paid.
   - **Sublet deposits.** `RentalContract.DepositTo` creates new `Gold(Price)` (`RentalContract.cs:100`) as the
     returned deposit, and `Delete` can call `PackUpHouse`, which deletes the house, whose `OnDelete` clears the sign,
     which calls `Delete` again (`RentalContract.cs:250-258`, `:330-385`, `TownHouse.cs:268-286`): a possible double
     deposit (unverified).
   - **One house per account bypass.** Purchase checks no account house limit (no such check in `TownHouseSign.cs`),
     so a player can hold several town houses; a town house then blocks a normal placement through the stock check
     (unverified which wins).
   - **Global hooks.** A global speech handler runs `BaseHouse.FindHouseAt` on every line anyone says
     (`General.cs:27`, `:72-114`), and a world-save hook re-checks every sign (`:47-60`).
   - **Save compatibility.** New types, but they live inside the house lists (`BaseHouse.AllHouses`), so a later
     removal needs a cleanup command; a broken deserialize takes houses down with it.
   - Movement: `HouseRegion` ban and access rules apply inside the claimed area (`HouseRegion.cs:95-128`), which in a
     busy town building can trap or eject passers-by if the rectangles are drawn loosely.

5. **Verdict: `reference only`, L.** The setup flow (rectangles, Z range, sign and ban spots, buyer requirements,
   price suggestion from area) is a good reference if Chase ever wants player-owned town buildings; the code needs a
   near rewrite on pinned and has duplication and refund holes. It is not the right base for F-44 or F-49.

**Rename candidates.** `ClusterFLeasehold` (the house), `LeaseSign`, `[Leaseholds` (command).

---

## Ranked shortlist

Nothing here is a faithful-port item, so all of it sits in the custom lane behind the port list
(`notes\port-list-2026-10-13.md`), except 1a, which is OSI content.

1. **Halloween boss (time-sensitive; the season switch opens 10-24).**
   a. Faithful first: OSI's Treasures of Sorcerer's Dungeon (Jack the Pumpkin King, Headless Elf) is in
      `ServUO-pub57\Scripts\Services\Seasonal Events\TreasuresOfSorceresDungeon\` and in neither pinned nor the shard.
      It is a port-list candidate, not part of this batch; a separate assessment prompt if Chase wants it.
   b. Custom: the "Hollow Rider" built natively from headless-horseman's idea (mounted rider, pumpkin bombs, no gold
      from carving, a rebalanced sword), on `ClusterFSeasonalSwitch.cs`. S.
2. **New Haven townsfolk, one build prompt (S + M):** paid self-only "rest" on the stock New Haven `InnKeeper` (combat
   check, sane price) plus a small data-driven talk table for New Haven NPCs in the System / Echo voice (synchronous,
   JSON, keyed by NPC tag and region). Both are independent of F-12 and give the tutorial town life cheaply. The rest
   is about 40 lines; the talk table is the M part.
3. **Event boss token, folded into the F-30 Events tab build (S):** an event-bound, place-limited token that calls a
   flagged event boss, from world-boss-in-a-box's idea. The Hollow Rider (1b) can be the first boss it calls, so 1b and
   3 can share one prompt.
4. **Scoring archery butte (S code), once F-8 / F-21 prove new item art ships:** a subclass of pinned's
   `ArcheryButte`, 20 new art ids. Could ride with the F-35 combat wing build. Pick this set or the sibling
   `D:\UO\third-party\archery-buttes\` set first.
5. **Gear, design only for now:** write the F-26 b attunement gate as cc-P72 C.4 recommends (item level on our
   levelable gear, bonuses above the wearer's level plus attunement go dormant), and note level-system-3's "gear score"
   as an option. It needs F-12 levels to exist, so it is a design note for the F-12 build, not a prompt today.
6. **Only if Chase says yes:** passive charms in accessory slots (S, per-character cap, no gold proc); sockets (M
   native rebuild inside imbuing's slots and ceilings; recommended no); a pet XP item (S, bound, evo pets only;
   recommended no).

**Shared prompts:** (A) New Haven townsfolk: inn rest + talk table, later the butte. (B) F-30 events: boss token +
Hollow Rider. (C) F-12 build notes: attunement gate formula, gear score, level gate tile and mount requirement.

Not taken at all: squire-system (stays the behavior reference for companions B2 onward, `notes\cc-P41-companions-research.md`),
quetzalcoatl-armor-mob, summoning-system-v2 code, level-system-3 code, equipment-level-requirements, skill-trainer-npc,
knives-town-houses code.

## Open questions for Chase

1. **Halloween boss: which lane?** (a) OSI's Pumpkin King event first, faithful (overseer lean); (b) the custom Hollow
   Rider; (c) both, the OSI event as the dungeon and the Hollow Rider as a roaming event boss; (d) neither this year.
2. **Boss summon tokens.** (a) Staff only: the F-30 Events tab spawns the boss, no player item; (b) an event-bound token
   that drops during a running event, usable only at marked spots, expiring with the event; (c) a League reward that
   lets a party call a set mini boss once (the F-24 dive "investigation").
3. **Summons as a player power** (summoning-system idea). (a) No (lean: it trivializes bosses and duplicates existing
   summon schools); (b) event-only consumable inside the event area; (c) a high League rank reward: one weak "Echo",
   no loot, long cooldown, normal follower cost.
4. **Squires: hired help or a companion tier?** The companions design already decided a companion tier ("Squire" is
   rank 0, `Companions/BaseCompanion.cs:64`; bought from the League or a candidate board). (a) Keep that, squire-system
   stays reference only (recommended); (b) also a cheap hired squire (no rank, no loop) as a day-rate helper from the
   League.
5. **A pet XP item at all?** (a) No: evo XP stays kills-only, companions use Drill Orders and level scrolls
   (recommended); (b) evo pets only, bound, as a quest or achievement reward, sized as a percent of the next stage and
   never crossing a stage; (c) also sold (makes XP a gold item).
6. **Gear level gate (F-26 b), which formula?** (a) item level of our levelable gear only, item stays wearable, extra
   bonuses go dormant (cc-P72 C.4, recommended); (b) a required level from a gear score on our crafted and dropped
   gear; (c) both.
7. **Sockets?** (a) No: imbuing plus levelable gear is enough (recommended); (b) a native rebuild inside imbuing's slot
   count and ceilings, crafted gear only; (c) only mule barding (already built) and companions.
8. **Passive procs?** (a) No; (b) accessory-slot charms with a per-character cap, no gold proc; (c) a milestone purchase
   on levelable gear.
9. **Level gate tiles and mount level requirements** (level-system-3): (a) add both to F-12's level-gates list; (b) leave out.
10. **Talking townsfolk.** (a) Small keyword-chat table for New Haven NPCs, our voice (recommended, after the tutorial
    core lands); (b) flavor lines on click only; (c) not now.
11. **Inn rest.** (a) Paid, self only, combat check, on the New Haven innkeeper (flat fee or by missing points?);
    (b) free for Young or tutorial characters only; (c) none.
12. **Scoring archery butte.** (a) This set, after F-8 proves new item art; (b) the sibling `third-party\archery-buttes`
    set (28 frames); (c) stock butte only. Also: New Haven yard only, or a craftable or reward deed too?
13. **Town Houses: rentals?** (a) No player-owned town buildings (default, nothing to port); (b) staff-placed
    leaseholds, sale only, no sublets, no decoration sale; (c) also rentals and sublets. If (b) or (c): may one sit
    inside a guarded town (needs a `HouseRegion` change, `UOContent\Regions\HouseRegion.cs:18` has no parent), and does
    it count as the account's one house?
14. **Town Houses for F-44 inn rooms or F-49 halls?** (a) No to both: F-44 stays instanced, F-49 halls are guild-run and
    placed by our seeders (recommended); (b) fixed rooms on each inn's upper floor for F-44; (c) borrow only its
    "claim a building by rectangles and Z range" setup as a staff region tool.
15. **Skill trainer for testers.** (a) Staff runs `[SetSkill` / `[SetAllSkills` as today (recommended); (b) a staff-only
    command that applies a named skill template.

## Rename list

Only for what we would build; names follow the borrowed idea, not the download.

| Download name | Problem | New name (suggested) |
|---|---|---|
| Ichabod Crane (Headless Horseman) | wrong character (Ichabod is the schoolteacher) and has a head (body 185, Savage Rider) | the Hollow Rider |
| Sword of the Hessian | tied to the old name; over-powered | Hollow Rider's Blade |
| Pumpkin Lantern | clashes in spirit with stock jack-o'-lanterns | Rider's Lantern |
| Deity Quetzalcoatl Dante | real, still-revered deity on a killable monster | (skipped) if ever used: Xal'teca the Plumed Wyrm |
| World Boss Summoner | generic, another shard's event | Ruby Call Crystal |
| an ancient ruby red dragon (tameable copy) | tame shares the boss name | a ruby drakeling |
| Weavers Tribal Mask | returns OSI's Mask of Khal Ankur label (1158701) | Ruby Weaver's Mask |
| Summoned Stygian Dragon and the other 25 | share real bosses' names | Echo of the Stygian Dragon (pattern "Echo of X") |
| Summoner's Spellbook | clashes with OSI's Summoner's Kilt and Spellweaving | Tome of Echoes |
| Pet Experience Scroll (six, one name) | six identical names | Bond Draught (minor / major) |
| Squire Contract, Training Contract, Squire Care Book | design already renamed or reworked | Companion's Writ, Drill Orders, Companion's Handbook |
| Battle Rating; Level Need | match F-26 b wording | Gear Score; Attunement Level |
| XmlSockets augments; Box of Transmutation | only if sockets are wanted | Inlays; an Artificers' Order bench |
| Passive items | only if procs are wanted | Bound Charms |
| Townsperson | ours | Townsfolk (`ClusterFTownsfolk`) |
| Specialized Innkeeper "Rest" | ours | Rest (a context entry on the stock InnKeeper) |
| Town House / sign | only if leaseholds are wanted | Leasehold, Lease Sign |
| Archery butte that shows hits | ours | Scoring Butte |

## For the overseer: CODE-INTAKE.md Overseer column

One line per folder, ready to paste.

- code/squire-system: reference only (P405): ours is `Companions\`; P41 already read it; behavior reference for B2+.
- code/pet-experience-scroll: idea only (P405): FS-ATS-bound and tradeable XP is an exploit; bound evo-only deed only if Chase wants one.
- code/headless-horseman: idea only (P405): native "Hollow Rider" Halloween boss if wanted; OSI Pumpkin King first (fidelity).
- code/quetzalcoatl-armor-mob: skip: reskinned copy of our StygianDragon on the Najasaurus body (1289); gear breaks F-40.
- code/world-boss-in-a-box: idea only (P405): event-bound boss token for the F-30 Events tab; code does not compile.
- code/summoning-system-v2: reference only (P405): replaces 6 stock files, needs Druid and XmlSpawner; summons farmable.
- code/level-system-3: reference only (P405): older Level System Extreme, all XmlSpawner; gear-score idea noted for F-12.
- code/xmlsockets: idea only (P405): XmlSpawner core, rolls sockets on all loot; native rebuild only if Chase wants sockets.
- code/passive-item-system: idea only (P405): dispatcher never shipped, gold faucet; accessory charms only if wanted.
- code/equipment-level-requirements: skip: ~60 authored lines on five missing add-ons, gates OSI gear, crashes on NPCs.
- code/conversational-townsperson: idea only (P405): our own synchronous New Haven talk table; threaded code will not run on net10.
- code/specialized-innkeeper: idea only (P405): paid self-only rest on the stock InnKeeper; code double-charges, heals others mid-fight.
- code/skill-trainer-npc: skip: free skill and stat editor; staff [SetSkill covers testers.
- code/archery-butte-hits: port (art-gated, P405): subclass of pinned ArcheryButte with 20 new art ids after F-8/F-21.
- code/knives-town-houses: reference only (P405): fits neither F-44 nor F-49; shared multi components, no guard zone, dupe and refund holes.

P405 DONE
