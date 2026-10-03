# cc-P41: companions (Squire + EvoMerc hybrid) port research, notes only

Written 2026-10-02 by CC from `D:\UO\cc-prompts\cc-P41-companions-research.md`. Notes only: nothing built, nothing
written to `D:\ShatteredLegacy`, nothing committed. Sources were extracted to the session scratchpad, never into a repo.

**Engine:** `git -C D:\UO\ModernUO-pinned --no-optional-locks rev-parse HEAD` =
`d4531cd94b739613155225c234900de9f47d2c88` (P38 had already re-checked it out). Every pinned citation below is as of
**d4531cd94**, paths relative to `D:\UO\ModernUO-pinned\Projects\`. P30's changed-file list is therefore not needed.
"Ours" = `D:\ShatteredLegacy\server\customizations` (or `\patches` where it says so). Squire paths are relative to the
extracted `Squire System\` folder.

**Numbering:** no clash. `cc-prompts` holds P40, P41 and P42; `notes\` has no other cc-P41 file.

**Read this before trusting the design side of these notes:** the design doc `claude/companions-squire-evo-research.md`
and `claude/companions-combo-lines.md` are claude.ai project docs, **not on disk** (searched `D:\UO` and the user
profile; the only on-disk reference is `notes\skills-design.md:1103`). I could not read them. The decided points
I honoured are the ones the brief itself states: companions use player caps and player skill math; Room attendant kept;
no stabling for companions; Healing removes resurrection skill loss (16:49); pets gain to the same cap as players
(P25). Anything below that looks like a design choice is a proposal, and **where it may touch a decision in the doc I
could not read, I say so**. The overseer should diff section 9 against the doc.

## Summary

| # | Question | Answer in one line | Biggest risk |
|---|---|---|---|
| 1 | API map | Most of the API maps directly. What is missing or reshaped: `AI_Paladin`, `TimerPriority`, Skill Masteries, VvV, `Say(format, ...)`, the gump `AddHtml` bools (188 calls), the context-menu and `CloseGump` signatures, and the Discordance internals (private in both trees). Sizes: Squire.cs L, SquireTargets L, SquireGump M, RoomAttendant M, Mercenary L, the rest S. | The source **does not compile on stock ServUO either**: it needs core edits to `Discordance` and `Corpse.IsCriminalAction`. Any port that "just converts" carries hidden core patches. |
| 2 | Player parity | Seven `SkillCheck` branches differ. The pet x2 chance and the 5-minute pet stat delay are inline with no virtual. Melee uses the creature's `SetDamage` over the weapon. Bushido is hard-blocked for non-players. ClusterFSkillGain skips creatures. Resurrection loss lives in 2 caller loops. | Exact parity needs about **4 small pinned patches** (SkillCheck x2 chance, pet stat delay, `SamuraiSpell.CheckExpansion`, the 2 resurrection-loss loops); the rest is ours. |
| 3 | AI per class | `AI_Paladin` does not exist (10 enum values). Melee, Archer and Mage fit. Healer, bard and stealth rogue have **no** pinned AI. Controlled creatures run `Obey()`, and only Guard or Attack reach the class AI. | A companion on "follow" **will not fight back even when attacked** (`PetOrders.cs:36-39`). Every class AI needs a custom `ForcedAI` to behave like a party member. |
| 4 | Party of followers | 9 native "all" commands and 12 name commands. Group and class commands go in our `OnSpeech` override with **no** pinned patch. Slot counting lives in one place (the `Master` setter). | Setting `e.Handled` in a companion swallows the command for every other companion: the speech event is shared. |
| 5 | Mounts | A companion can ride an ethereal or a real mount **only by code** (`Rider = companion`). The mount keeps its master. No region forces a dismount, and `CheckMountAllowed` waves every NPC through. | `ShrunkPet` cannot shrink a ridden or companion-mastered mount, and it has **2 defects of its own** (follow order and follower drift). |
| 6 | Rooms and pigeon | The source rooms by `SetControlMaster(null)` + `Internalize()` + forced `Controlled = true`. On pinned that is an accidental escape from the 3-day abandoned-pet delete. Use our own persisted registry that sets `IsStabled` on load. The pigeon has no owner, travel or cooldown check. | Reusing `PlayerMobile.Stabled` (the zero-code option) makes roomed companions **claimable at any Animal Trainer**, which contradicts "no stabling for companions". |
| 7 | Data tables | JSON through pinned `JsonConfig`, shipped in the image under `Data/ShatteredLegacy/companions/`, with a live override in the bind-mounted `Configuration/companions/` and a GM reload command. A shard test validates every row, so a bad row fails `build.sh`. | Pinned's precedent (`NameList.cs:49-52`) **throws at startup** on a bad file. A typo in a live override must log and keep the last good table, never take the server down. |
| 8 | Breeding readiness | Yes. Sex is already `Mobile.Female`. Parents and generation fit as `[SerializableField]` from build one. Pinned has **zero** creature breeding hooks. | A `Mobile` reference turns null and a raw `Serial` can be **reissued** once a parent is deleted. Lineage needs its own never-reused id. |

**Addendum 2026-10-03 (section 11, placed before section 9):** slot costs per companion rank and for the evo mount, set against F-33's target (16 slots at loop 11 with Trailwise Tack III, 17 at loop 21 without, for a party of 4); `party.json` now keys on loop count; where P41 touches the Compact Mule.

Counts in this note were made against the files; each list sits beside its count. Things I could not confirm are
marked **unverified**.

---

## 0. Sources, counts and safety sweep

### 0.1 What is in the downloads (counted)

| File | Brief says | Counted |
|---|---|---|
| `SquireSystem_2021-06.zip` | 35 .cs, about 21,900 lines | **33 .cs, 21,941 lines** (40 zip entries = 33 files + 7 folders). The brief's 35 is wrong; its line figure is right. |
| `EVO System.rar` | about 70 files | 70 files = 67 .cs + `Changelog.htm`, `ReadMe.htm`, `GuardianDustSpirit.cs.bak` |
| `Utilities.rar` | | 6 .cs: ConfigParser, findMobs, Interfaces, Misc, Replace, wipemobs |
| `Mercenary.cs` | incomplete | 665 lines. Missing `MercenarySpec` (needed at `Mercenary.cs:40`), `MercenaryEgg`, a Xanthos `HairstylistBuyGump(from, this)` (pinned has a different one, `Mobiles/Vendors/NPC/CustomHairstylist.cs:125`). |
| `Mercenary.7z` | older copy | not diffed (brief: ignore unless it matters; nothing here needed it). |

All were in `C:\Users\ckfle\Downloads\`; `D:\UO\sources\companions\` does not exist.

The 33 Squire files: Commands (4: Squire Room, Squire Skills, Squire Stats, Squire Switches), EC Squire Book (2),
Items (7: CarrierPigeon, RoomAttendantContract, SquireBook, SquireContract, SquireDeathShroud, SquireStatsSpyglass,
TrainingContracts), Mobiles (8: RoomAttendant, Squire, SquireBardingInstructor, SquireCombatInstructor,
SquireHealingInstructor, SquireRepresentative, SquireThievingInstructor, SS_InnKeeper), Other (5: SquireDialog,
SquireFunctions, SquireGump, SquireTargets, SquireTitle), Sell Buy (7).

### 0.2 Safety sweep (re-run on everything extracted)

Grepped for network, sockets, `System.IO`/File/Directory/streams, Process/Diagnostics, Reflection/Invoke/Activator/
`Type.GetType`, Registry/Win32, DllImport/unsafe, Account/Password, `Environment.`, `World.Mobiles`/`World.Items`,
command registration and AccessLevel.

**Clean in the kept parts:** 0 network, process, registry, DllImport, unsafe, password or account-credential hits in
any Squire, Evo or Mercenary file. `using System.Reflection` appears in 10 Squire files but **no Squire file calls
reflection** (the only `Invoke` hits are `Target.Invoke`, the engine's target API).

**New since the design chat's sweep (all in `Utilities.rar`, plus one in Evo):**
1. `Utilities\ConfigParser.cs:36-62` **reads a file**: `new XmlTextReader(filename)`, and `:298`, `:433` resolve
   **types from config text** with `Type.GetType`. No kept file calls ConfigParser (grep: 0 callers outside itself).
2. `Utilities\Misc.cs:33-56` reflection (`GetProperty("ArtifactRarity")`, `GetProperty("PlayerConstructed")`), and
   `:77-92` `InvokeParameterlessMethod` (GetMethod by string + Invoke). Called by `BaseEvoDeed.cs:79`,
   `BaseEvoEgg.cs:108` and by `Mercenary.cs:500-502`. Pinned needs none of it: `ArtifactRarity` is a virtual on the
   bases (`Items/Weapons/BaseWeapon.cs:231`, BaseArmor, BaseClothing, BaseJewel) and `Item.PlayerConstructed` is on
   Item (`Server/Items/Item.cs:798`).
3. `Utilities\Replace.cs`: GM command `ReplaceItem` (`:30`) walks `World.Items` (`:139`), constructs types by name
   through reflection (`:117-153`), copies every property by reflection (`:83`) and deletes the originals.
4. `Utilities\wipemobs.cs`: **Administrator** command (`:24`) that walks `World.Mobiles` and deletes mobiles and items
   (`:321`, `:359`), and prints account usernames (`:193`).
5. `Utilities\findMobs.cs`: GM command (`:91`) walking the world, printing account usernames (`:278`).
6. `EVO System\Commands.cs:21`: `EP` at **AccessLevel.Player**. Read-only (shows a pet's EP).

None of 1-6 should be ported. Gameplay surfaces that touch other players are in section 1.5.

---

## 1. API map

Full tables (every API with both sides' file:line) are condensed here to what changes. Everything not listed maps
one to one; the per-group "same" lists name what was checked.

### 1.1 Two facts that change the plan

1. **The Squire source does not compile on stock ServUO.** `SquireTargets.cs:924-991` uses `Discordance.m_Table`,
   `DiscordanceInfo` and `ProcessDiscordance`, private in ServUO (`Scripts\Skills\Discordance.cs:18/78/323`) and private
   in pinned (`UOContent/Skills/Discordance.cs:11/46/93`). `Squire.cs:4-34` tells the admin to hand-edit
   `Corpse.IsCriminalAction` so pets inherit looting rights; pinned's (`UOContent/Items/Misc/Corpses/Corpse.cs:750`) has
   no such clause. A rewrite uses the public `Discordance.DiscordanceTarget` (`Discordance.cs:119/123`) instead.
2. **Pinned has no paladin AI.** `AIType` (`UOContent/Mobiles/AI/BaseAI/AIType.cs:18-30`, verified) has 10 values and no
   `AI_Paladin`. The Squire's base AI (`Squire.cs:513`, `:4051`) becomes `AI_Melee` with chivalry in our own code.

### 1.2 Per group: what changes (pinned side cited)

**Serialization.** Hand `Serialize/Deserialize` (Squire v16, `Squire.cs:4469-4638`) becomes
`[SerializationGenerator(0, false)] partial` + `[SerializableField]` (BaseCreature itself is
`UOContent/Mobiles/BaseCreature.cs:137-138`). No saves exist, so start at version 0. `[Constructable]` ->
`[Constructible]` (`Server/Attributes.cs:105`). `CorpseName`: pinned has both the attribute
(`UOContent/Items/Misc/Corpses/CorpseNameAttribute.cs`) and a virtual (`BaseCreature.cs:873`); either works. Evo's
pregnancy timer re-created in Deserialize becomes `[DeserializeTimer]` (`BaseCreature.cs:751-753`). Drop the Squire's
`Say()` during Deserialize (`Squire.cs:4535-4539`).
Squire persisted fields: **52** (43 bool, 3 string, 6 Item), list in the scratch report; **12 of the 43 bools are
never read** by game logic (the Bushido and Necro auto-toggles other than VampiricEmbrace).

**Timers.** `Timer(TimeSpan)` and `OnTick` unchanged (`Server/Timer/Timer.cs:40`, `:175`). `TimerPriority` is **missing**
(14 sites in Squire, 1 in BaseEvo): delete the lines. `DelayCall<T>` takes `Action<T>`
(`Server/Timer/Timer.DelayStateCall.cs:32`). `DateTime.Now` -> `Core.Now` (`Server/Main.cs:281`). 12 of the Squire's 14
timer classes only delay a spell-target hand-off and collapse to `Timer.StartTimer(delay, ...)`
(`Server/Timer/Timer.DelayCall.cs:57-83`).

**Gumps.** Legacy `Gump` survives (`UOContent/Gumps/Base/Legacy/Gump.cs:25`); use `DynamicGump`
(`UOContent/Gumps/Base/DynamicGump.cs:22`). `OnResponse(NetState, in RelayInfo)` (`BaseGump.cs:74`). `AddHtml`'s 6th
parameter is a colour (`DynamicGumpBuilder.cs:81`), so the Squire's **188** `AddHtml(..., false, false)` calls do not
bind. `CloseGump(typeof(X))` -> `CloseGump<T>()` (`GumpSystem.cs:96`). `AddHtmlLocalized`, `AddButton`, `HuePicker`,
`Prompt` are compatible (`DynamicGumpBuilder.cs:113-129`, `:69`; `Server/HuePicker.cs:5`; `Server/Prompt.cs:3`).
**Security bug to fix, not copy:** the lore gump's `OnResponse` (`SquireGump.cs:396-1063`) never re-checks ownership,
and pinned validates button ids only for the legacy `Gump` (`GumpSystem.IncomingPackets.cs:55-80`), not DynamicGump.
A non-owner looking at an `Inspectable` squire through the spyglass could forge switch and skill-lock buttons.

**Speech and commands.** `HandlesOnSpeech`/`OnSpeech(SpeechEventArgs)` same shape (`Server/Mobiles/Mobile.cs:6972`,
`:6979`; `BaseCreature.cs:2874-2890`; args `Server/Events/SpeechEvent.cs:21`). **Missing:** `Say(string format, params
object[])` (pinned has `Say(ReadOnlySpan<char>)`, `Server/Mobiles/Mobile.Messages.cs:77-89`): use interpolation.
`Insensitive.Equals` -> `InsensitiveEquals` (`Server/Text/InsensitiveStringHelpers.cs:35`). Player-issued orders should
use `IssueOrder` (`BaseCreature.cs:1213`), not raw `ControlOrder =`. Squire live speech commands: **86** (87 keyword
strings including a blank placeholder; the 87th case, SacredJourney, is commented out). Mercenary: 16.

**AI.** Missing `AI_Paladin`, `UseSmartAI` (a no-op in ServUO too), `ChangeAIToDefault` (pinned: `AI =
AIType.AI_Use_Default`, `BaseCreature.cs:1066-1079`). BaseCreature ctor drops the speed arguments
(`BaseCreature.cs:807-812`; speeds from the npc-speeds table). `AIObject.MoveTo(m, run, range)` -> `MoveTo(Mobile, int)`
(`UOContent/Mobiles/AI/BaseAI/AIMovement.cs:611`). `AddCustomContextEntries` takes `ref PooledRefList`
(`BaseCreature.cs:2829`); `ContextMenuEntry.OnClick(Mobile, IEntity)` (`Server/ContextMenus/ContextMenuEntry.cs:89`).
`OnGaveMeleeAttack(Mobile, int)` (`BaseCreature.cs:2685`) and `Damage(int, Mobile, bool, bool)`
(`Server/Mobiles/Mobile.cs:5956`) changed signature (Evo).

**Targeting.** Unchanged: `Target(range, allowGround, flags)` (`Server/Targeting/Target.cs:12`), `OnTarget` `:216`,
`OnTargetFinish` `:263`, `Invoke` `:146`. The Squire's relay (squire casts, master picks, pick forwarded into the
squire's spell target) works in principle because pinned spells set `Caster.Target` (e.g.
`UOContent/Spells/Chivalry/CloseWounds.cs:96`); **unverified at runtime** (range and LOS run against the squire).

**Items and containers.** Same: `FindItemByType` (+ generic, `Server/Items/Container.cs:903-947`), `DropItem`,
`CheckHold`, `TryDropItem`, `Lift`/`Drop` (`Mobile.cs:5039`, `:5335`, `:5409`), `ConsumeTotal` (`Container.cs:796`),
`Banker.GetBalance/Withdraw` (`UOContent/Mobiles/Townfolk/Banker.cs:31/158`). `NextActionTime` is a `long` tick count
(`Mobile.cs:686`), so the Squire's `= 5` is a no-op in both trees. `BaseHouse.PlayerBarkeepers` is
`List<PlayerBarkeeper>` in pinned (`UOContent/Multis/Houses/BaseHouse.cs:522`), `List<Mobile>` in ServUO: the
RoomAttendant must derive from pinned `PlayerBarkeeper` to be counted and cleaned up with the house.
`BallOfSummoning.Charges = 2000` (`Mercenary.cs:126`) silently clamps to 20 in pinned (`BallOfSummoning.cs:43-50`).

**Mounts.** All present: `IMount`/`IMountItem` (`Server/Mobiles/IMount.cs:18-27`), `Mobile.Mount`/`Mounted`
(`Mobile.cs:1706-1730`), `BaseMount.Rider` (`UOContent/Mobiles/Animals/Mounts/BaseMount.cs:77-136`),
`EtherealMount.Rider` (`Ethereals.cs:76-110`), `MountItem` (`BaseMount.cs:315`). See section 5.

**Other (skills, spells, combat).** Present: all 9 live Chivalry spells, all 7 Necromancy spells, all 6 Bushido
spells and moves (`SpecialMove.SetCurrentMove`, `UOContent/Spells/Base/SpecialMove.cs:217`), `WeaponAbility`,
`BandageContext` (`UOContent/Items/Skill Items/Misc/Bandage.cs:169/454`), `BasePotion.Drink`, bard helpers on
`BaseInstrument`, lockpicking, poisoning, `PowerScroll.Use`, `AosAttributes.GetValue` (`UOContent/Misc/AOS.cs:621`).
**Missing:** Skill Masteries (`ToughnessSpell`, `InvigorateSpell`, `MasteryInfo`), `UraliTranceTonic`, Vice vs Virtue
(`VvVSigil`, `ViceVsVirtueSystem`), `Utility.RandomSkinHue` (use `Race.RandomSkinHue()`, `Server/Race.cs:86`).
Renamed: `DisguiseTimers` -> `DisguisePersistence` (`UOContent/Items/Skill Items/Thief/DisguisePersistence.cs:60`).

### 1.3 Port size per file (a rewrite that borrows behaviour)

| File | Lines | Size | Why |
|---|---|---|---|
| `Squire.cs` | 4638 | **L** | 86 command handlers plus a 280-line `OnThink` rules engine on a missing AI. Most handlers are the same "book? mana? skill? cooldown? cast" shape and collapse to one table-driven helper. |
| `SquireFunctions.cs` | 170 | S | 3 prompts, a pack-access check, 2 cosmetic timers. |
| `SquireTargets.cs` | 2455 | **L** (M if steal, poison and the copied bard internals are dropped) | 20 target classes, 12 relay timers that become one helper. |
| `SquireGump.cs` | 1963 | M | Mechanical, but all 188 `AddHtml` calls change, the 27 skill rows and 30 switches become loops, and the owner check must be added. |
| `SquireDialog.cs` | 1980 | S | Pure data: 150 situations x 6 lines (765 Say + 141 Emote). Becomes the speech table (section 7). 5 entries are never used. |
| `RoomAttendant.cs` | 1049 | M | Derive from `PlayerBarkeeper` (`UOContent/Mobiles/Vendors/Barkeeper/PlayerBarkeeper.cs:124`), which already has the rumours, tips, prompts and gump (about 850 source lines). New code is the room keyword, target, fee and storage; storage is the M part. |
| `RoomAttendantContract.cs` | 93 | S | Mirror pinned `BarkeepContract`. |
| `CarrierPigeon.cs` | 118 | S | One field plus a recall that needs checks the source lacks (section 6). |
| `TrainingContracts.cs` | 2108 | S | 26 copies of one class (one base with a `SkillName`, 26 thin subclasses for vendor rows). |
| 4 instructors + `SquireRepresentative` + 7 SB files | | S each | Plain `BaseVendor`s. |
| `Mercenary.cs` mount code | 665 total | S for the mount part | Needs nothing from Evo to mount (section 5). The whole file is L (Evo, missing spec, missing gump). |
| `BaseEvoSpec.cs` | 121 | S | Pure data: 21 spec fields, 28 stage fields. Borrow the stage table, skill min/max (max doubles as cap), `AbsoluteStatValues`, `MaxEvoResistance`, `CanAttackPlayers`. **Source bug, do not copy:** `DexMax` is ignored (`BaseEvo.cs:334`, `:342` call `SetDex(stage.DexMin, stage.DexMin)`); under the D-4 rule (it makes something broken) fix it, argued first. |

### 1.4 Name collisions

0 found in pinned for every type these files declare (Squire*, RoomAttendant*, CarrierPigeon, STrainingContract,
Mercenary, BaseEvo*, IEvoCreature, MountTarget, PregnancyTimer, SB*). Re-check with `tools/modernuo-stems.txt` at build.

### 1.5 Do not carry (touches other players, or ServUO-only)

- **Steal** (`SquireTargets.cs:1238-1645`): a random item from another player's backpack, target range 20, **zero
  cooldown** (`:1561`), VvV sigil theft. A remote thief proxy.
- **Peacemaking on a player** clears that player's combatant and war mode (`SquireTargets.cs:1199-1208`); area peace
  hits players in range (`:1110-1116`).
- **Poison target** accepts any item within 2 tiles (`:1790`, `:1847`); can poison food others may eat. Looks like a bug.
- **Looting:** Squire "loot all" ignores notoriety (`Squire.cs:873`); Mercenary "loot" lifts from **innocents'**
  corpses within 2 tiles and "grab" takes any movable item within 2 (`Mercenary.cs:303-304`, `:427-439`). Whether a
  creature lift flags anyone criminal: **unverified**. Looting rights need an explicit decision.
- **Lockpick** as a proxy on any `ILockpickable` in range, orderable from 20 tiles.
- **Pigeon as ownership token** (section 6).
- Dead or broken: SacredJourney remnants, hunger block behind `1 != 1` (`Squire.cs:3452`), `OnAfterResurrect` NRE with no
  shroud (`Squire.cs:4066-4067`), free loyalty with no food (`CheckFeedSelf`, `:3486-3519`), hard-coded resist max 80
  (`:4440-4465`), `Skills.Cap = 50000` and `StatCap = 450` (`:558-559`, superseded by section 2.5).

**Fidelity.** Companions are not OSI content. `docs\fidelity-principle.md` needs an entry for the system as a whole
when it is built (the overseer's call where; agents do not edit `docs\`).

---

## 2. Player parity (decided: player caps and player skill math)

### 2.1 Skill gain (`UOContent/Skills/SkillCheck.cs`)

Same chain for both until 7 branches (chance formula `:126-138`, `Gain` `:236-310`):

| # | Branch | Who | Line |
|---|---|---|---|
| 1 | Gain chance x2 | controlled `BaseCreature` | `:140-143` (verified) |
| 2 | Dead pet never gains | `IsDeadPet` | `:238-241` |
| 3 | Never gains Focus | any creature | `:243-246` |
| 4 | Anti-macro | `PlayerMobile` only | `:233` |
| 5 | Down-locked skill atrophy | `from.Player` only | `:259-271` |
| 6 | Scroll of Alacrity | `PlayerMobile` only | `:273-276` |
| 7 | Total cap enforced | `from.Player` only | `:278-281` |

Trap: the chance reads `Skills.Cap` and `Skills.Total` for creatures too (`:126`). The creature default `Skills.Cap` is
7000 (`Server/Skills.cs:463`), so a companion past 700.0 total falls to the 0.01 floor. **A companion needs the player's
`Skills.Cap`, not just per-skill caps.**

**Our ClusterFSkillGain** (`ClusterFSkillGain.cs`): replaces the four handlers at `[CallPriority(100)]` (`:35-46`); 3
attempts and x5 amount (`:22-30`); **players only**, `ShouldBoost` requires `from?.Player == true` (`:141-147`). So a
companion today gets 1 attempt, x1. The **test shard's x5** is `TestCenterSkillGain` multiplying every
`SkillInfo.GainFactor` (`TestCenter\TestCenterSkillGain.cs:31-80`), read at `SkillCheck.cs:133`, so it **does** reach
creatures. (Stale comment: `TestCenterSkillGain.cs:3` says `:119`.) Live and test json not read (they live under
`server\uo`); values from `docker\uo\SERVER.md:1037-1039`, **unverified**.

Companion needs:
1. Per-skill caps **and** `Skills.Cap` from its record (2.5).
2. Remove the pet x2: inline, no virtual. **Pinned patch** (exclude the companion type) or accept as a deviation.
3. `ShouldBoost` accepts a controlled, living companion; loop memory reads the companion's record. Ours, no patch.
4. Total cap: never enforced for creatures, but under F-12 it equals the sum of per-skill caps, so it cannot bind.
   No action (holds only while total = 58 x max level).
5. Anti-macro exemption: a companion is an unthrottled gain surrogate **if** anti-macro is on live (**unverified**).
6. Focus: needs the same kind of patch as 2 if Focus matters for companions.

### 2.2 Stat gain

Pinned **does** gain stats for creatures: Pub45 path inside `Gain` (`:284-309`, ML on). Two differences:
- **Delay:** a controlled creature uses `stats.petGainDelay`, default **5 minutes**, against the player's 3 seconds
  (`:26-27`, applied `:450/467/484`). Inline, no virtual: a pinned patch, or set `petGainDelay = gainDelay` (all pets;
  P25 decision 5 "pets follow players" may already cover it, Chase's call).
- **Total cap:** controlled creatures skip `StatCap` (`:355-361`) and stop only at `stats.statMax` (500). That already
  matches "no stat ceilings". `BaseCreature` has no effective-stat clamp either.

### 2.3 Melee damage

`BaseWeapon.GetBaseDamageRange` (`UOContent/Items/Weapons/BaseWeapon.cs:2428-2449`, verified) returns the creature's
`DamageMin/DamageMax` **whenever `DamageMin >= 0`, even with a weapon equipped** (`:2430-2437`). Default is -1
(`BaseCreature.cs:570-586`). **Rule: a companion never calls `SetDamage`.** Then weapon dice, Str/Tactics/Anatomy/DI
scaling (`:2519-2587`), weapon skill (`GetUsedSkill` `:1192-1196` substitutes Wrestling only for non-human bodies) and
swing speed are the player's. Remaining differences (9): damage **types** come from the creature's fields, not the
weapon (`:2345-2353`; copy the split on equip); weapon specials fire at random 0.4 (`:864-878`) not the player's toggle;
hit-spell Int/SDI bonus is `attacker.Player` only (`:2246`); Pack Instinct; Enemy of One, Honor and Perfection are
PlayerMobile only (`:1800-1854`); `CanEquip` skips Str and race checks for non-players (`:1005-1010`); creature pools are
`HitsMax = Str` (`BaseCreature.cs:1041-1051`) against the player's `Str/2 + 50 + HPI` (`PlayerMobile.cs:541-578`), so
override all three; `BonusPetDamageScalar` (default 1.0, no effect); monster ability hooks (inert).

### 2.4 Spells, bandages, potions, Chivalry, Bushido, Necromancy

| Use | Same path as a player? | Detail |
|---|---|---|
| Spells | Same `Spell.Cast`/`CheckSequence` (`UOContent/Spells/Base/Spell.cs:463`, `:736-800`) with creature branches | **No reagents** (`:260-263`), **cannot be disturbed** by damage (`:85-95`), no mantra. No clean seam to restore either for one type: pinned edit or accepted deviation. |
| Bandages | Real path works for any healer: `BandageContext.BeginHeal` (`Bandage.cs:454-546`); faction `GuardAI` already uses it (`Engines/Factions/Mobiles/Guards/GuardAI.cs:180`) | The **default** creature heal (`CanHeal`/`CanHealOwner`, `BaseCreature.cs:3897-3915`, `HealStart` `:5725-5818`) is a separate path: no bandage, fixed 6.5 s, own formula, gain capped at Healing 90. Use `BeginHeal`. |
| Potions | `BasePotion.Drink(Mobile)` takes any mobile (`BasePotion.cs:188`) | **No pinned AI drinks potions**; our AI must. |
| Chivalry | `PaladinSpell` spends `TithingPoints` with no player gate (`UOContent/Spells/Chivalry/PaladinSpell.cs:25-80`); points live on `Mobile` (`Mobile.cs:821`) | No pinned AI casts Chivalry. Needs a tithe source and our AI. |
| Bushido | **Blocked:** `SamuraiSpell.CheckExpansion` is `(from as PlayerMobile)?.NetState?...` (`UOContent/Spells/Bushido/SamuraiSpell.cs:28-29`, verified); same in `NinjaSpell.cs:28` | Confidence, Evasion, Counter Attack can never be cast by a creature without a **pinned patch**. Special moves the other way: `SpecialMove.Validate` returns true at once for non-players (`SpecialMove.cs:137-142`), skipping skill and mana. |
| Necromancy | Works through `MageAI` (`MageAI.cs:70`, `:252-310`); reagents free | Transformation spells by a creature: **unverified**. |

### 2.5 The per-character record, and where the companion record lives

- **No F-12 level record exists yet** (grep for MaxLevel/LoopCount/LoopMemory in customizations: 0). F-12 plans it in
  `ClusterFAccountData` keyed by serial, the `CharacterGuildData` pattern (`ClusterFAccountData.cs:121-140`,
  `:472-518`).
- `ClusterFAccountData` is keyed by **account username** (`:685-697`); a creature has no `Account`, so
  `GetOrCreateGuild(creature)` would throw on `account.Username` (`:693`, `:709`).
- `ClusterFSkillCaps.Apply(PlayerMobile)` (`ClusterFSkillCaps.cs:107-128`) writes each skill's cap and `Skills.Cap`,
  on `WorldLoad` and login.

**Proposal: the record lives on the companion as `[SerializableField]`s** (precedent: ours `PackMule.cs:41-47`), plus
a small global **lineage registry** for breeding (section 8). Reasons: no account to key on; it moves for free on a
transfer of ownership; it persists on `Map.Internal` (rooms); it dies with the creature, so nothing orphans; an owner's
loop reset must not reset the companion's levels (**assumption**, Chase to confirm).
Fields: `MaxLevel`, `CurrentLevel`, `LoopCount`, XP and reserve, per-skill peak (58 values, the loop-memory input).
Wiring: an `Apply(BaseCompanion)` overload with the same body reading `MaxLevel`, called on world load, at hire or
birth, and on every max-level change, and **after** any constructor `SetSkill` (which raises caps,
`BaseCreature.cs:5123-5131`). ClusterFSkillGain reads peak and loop count from whichever record the mobile has.
**May touch the design doc** (how a companion levels and loops): check it before building.

### 2.6 Resurrection skill loss (decided 16:49: Healing removes it)

- `BaseCreature.ResurrectPet` (`BaseCreature.cs:4126-4169`) applies **no** loss itself.
- The loss is in **2 caller loops**, permanent, from every skill:
  1. Bandage, healer is the master: `Base -= 0.1` (`Bandage.cs:268-276`, verified).
  2. `PetResurrectGump` (sent by Bandage when the healer is not the master, and by Gift of Life): `Base -= 0.1` if the
     **gump responder** is the master, else 0.2 (`UOContent/Gumps/PetResurrectGump.cs:74-81`, verified). The gump's
     constructor `from` (the healer) is never stored (`:13-17`).
- A humanoid companion is always resurrected with Healing, never Veterinary (`Bandage.cs:175-193`, chosen by the
  patient's body).
- **Hook:** the exact rule needs a **pinned patch** at both loops (`Bandage.cs:272-275`; `PetResurrectGump.cs:76-81`,
  storing the healer from `:13`). A patch-free fallback (snapshot skills in `OnBeforeResurrect`, restore after) cannot
  see who healed on the gump path, so it can only approximate the rule.

---

## 3. AI per class

`AI_Paladin` **does not exist** (section 1.1). Pinned's own `HirePaladin` runs plain `AI_Melee` (`BaseHire.cs:42`).

**The key fact:** the AI timer runs `Controlled ? Obey() : Think()` (`UOContent/Mobiles/AI/BaseAI/AITimer.cs:149`).
Only Guard-with-a-hostile (`PetOrders.cs:688`) and Attack (`:738`, `:768`) call the class `Think()`. Follow, Come and
Stay are stand-down orders; a following pet "will not attack anything, even if it is attacked" (`PetOrders.cs:36-39`).
While controlled, target picking is also overridden (`BaseAI.cs:872-874` -> `HandleControlled`).

10 `AIType` values: Use_Default, Melee, Animal, Archer, Healer, Vendor, Mage, Berserk, Predator (builds MeleeAI;
`PredatorAI.cs` is not wired, `BaseCreature.cs:2606-2608`), Thief. 4 more AIs are reachable only through
`protected virtual BaseAI ForcedAI` (`BaseCreature.cs:1063`): FamiliarAI, FactionGuardAI, SpellbinderAI, CloneAI.
**Ours already uses that hook:** `DespiseMeleeAI` overrides `Obey` and `OnSpeech`
(`Services/Revamped Dungeons/DespiseRevamped/AI.cs:22-29, :197`), installed by
`Mobiles/Normal/DespiseEvilCreatures.cs:37,60,83`. That is the companion pattern.

| Class | Pinned AI | Gap |
|---|---|---|
| Front-line melee | `MeleeAI` | None for basic play. |
| Archer | `ArcherAI` | Flees when no **`Arrow`** in pack (`ArcherAI.cs:71-78`): a crossbow companion with only bolts flees. Creatures never consume ammo (`BaseRanged.cs:164-188`, player only). |
| Mage | `MageAI` | **Never heals the master**: beneficial spells target self (`MageAI.cs:1062-1065`); on guard skips healing when controlled (`:836-842`). |
| Healer | none usable | `HealerAI` heals only `BaseCreature`s on the same `Team` (`HealerAI.cs:136-141`), never a player, and Team defaults to 0 for every creature, so it would heal wild monsters. Usable seam: `CanHealOwner` runs from `OnThink` under every order (`BaseCreature.cs:3897-3915`) but is the weak non-bandage path. Needs custom code using `BeginHeal`. |
| Bard | none | No AI uses Peacemaking, Provocation or Discordance (0 hits). Whether the skill handlers accept a creature user: **unverified**. |
| Stealth rogue | none | `ThiefAI` steals and disarms; no AI hides or stealths (0 hits). Stealth steps are handled only in `PlayerMobile.OnMove` (`PlayerMobile.cs:3408-3440`). Whether a hidden creature is revealed by moving: **unverified**. |

**Bow swap.** The Squire switches in `OnItemAdded`/`OnItemRemoved` (`Squire.cs:4029-4052`). Pinned: those virtuals fire on
equip (`Server/Mobiles/Mobile.cs:6649`, `:6659`); the `AI` setter calls public `ChangeAIType`
(`BaseCreature.cs:1066-1081`, `:2584-2612`); the current AI is saved when it differs from the default (`:271-273`) and
re-applied on load (`:2512`), so the Squire's re-set in Deserialize is unnecessary. Caveat: a `ForcedAI` wins over
the enum, so with a custom AI the swap must happen inside our AI (or `ForcedAI` must read state); `ForcedAI` is first
read from the base constructor (`:853`), before subclass fields exist.

---

## 4. Party of followers

- `Followers`/`FollowersMax` on Mobile (`Mobile.cs:836`, `:851`), default `FollowersMax = 5` (`:7827`), serialized
  per mobile. `Followers` is rebuilt at load from each pet (`BaseCreature.cs:2514`). Counting happens in one place, the
  `Master` setter (`BaseCreature.cs:1158-1179`).
- Cap checks relevant to companions (7): `SetControlMaster` (`BaseCreature.cs:3770`), taming
  (`Skills/AnimalTaming.cs:164`), transfer (`AI/BaseAI/TransferItem.cs:79`), hire (`Hireables/BaseHire.cs:168`),
  ethereal (`Ethereals.cs:201`, the **rider's** followers), auto-stable reclaim (`PlayerMobile.cs:3600`), trainer claim
  (`AnimalTrainer.cs:353`).
- `BaseHire` uses 2 slots (`BaseHire.cs:38`); the Squire 3. At `FollowersMax` 5 a player has 2 hirelings. Party size
  therefore comes from `FollowersMax` by max level (section 7.4) and the companion's slot cost.
- Native "all" keywords (9, `AI/BaseAI/OnSpeech.cs:137-204`): all come, all follow, all guard, all guard me, all stop,
  all kill, all attack, all follow me, all stay (speaker within 14). Name-addressed (12, `:205-293`): come, drop, follow,
  friend, guard, kill, attack, stop, follow me, release, transfer, stay. One cursor drives every pet given the same order
  (`BaseAI.cs:91-107`).
- **Guard** (`PetOrders.cs:668-715`, `FindGuardTarget` `:785-837`) defends only the master and the pet itself, and
  "guard me" equals "guard". A sibling companion under attack is not defended.

**What the proposed group commands need:**
1. "all follow", "all guard me", "all attack": native; nothing needed.
2. Class-aware ("healers, heal", "archers, attack"): override `OnSpeech` on the companion class, parse `e.Speech`
   (custom words carry no client keyword id), check `e.Mobile == ControlMaster`, match the class, act through
   `IssueOrder` or our action, then call `base.OnSpeech(e)`. **Never set `e.Handled`**: every hearer shares one args
   object, sorted by distance (`Server/Mobiles/Mobile.cs:5727-5745`), and `BaseCreature.OnSpeech` skips the AI once it is
   handled (`BaseCreature.cs:2886`).
3. Party-wide guard, and fighting back while following: override `DoOrderGuard`/`DoOrderFollow` in our `ForcedAI`
   (all public virtual, `PetOrders.cs:553-839`); `FindGuardTarget` is private, so reimplement its selection.
4. Healer heals while following: `OnThink` on the class.
Pinned patches required: **0**. Our existing `patches\BaseCreature-PlayerMobile-can-auto-stable.patch` (adds
`virtual bool CanAutoStable`) lets companions opt out of logout auto-stabling, which section 6 needs.
Raptor pack-friends code (`notes\reference\Raptor-ours-pre-upgrade-045b313.cs`): its target sharing (`:141-146`) works
only on uncontrolled creatures; only the spawn-location search (`:117-137`) and a 30 s group timer are reusable.

---

## 5. Mounts

1. **Ethereal ridden by a companion: yes, by code only.** Double-click mounts the clicker (`Ethereals.cs:210-216`).
   `Validate` (`:170-207`) has no PlayerMobile requirement. Setting `ethy.Rider = companion` works (`:76-110`) and moves
   the follower slot to the companion; unmounting drops the ethereal into the **companion's** pack (`:259-283`). The
   Squire does exactly this (`SquireTargets.cs:46-56`). Mount stamina is player only (`Misc/StaminaSystem.cs:291-298`).
2. **Real `BaseMount`:** the `Rider` setter (`BaseMount.cs:77-135`) internalizes the creature and gives the rider a
   `MountItem`; it does **not** touch control, so the mount keeps its own master and slots. On `Map.Internal` its AI
   stops (`AITimer.cs:197-210`). Mounting does not make an NPC rider faster (`AIMovement.cs:85`, `:97-108`). After
   dismount use `IssueOrder(Follow, null, master)`: a raw `ControlOrder = Follow` with no target drops to None next tick
   (`PetOrders.cs:638-644`).
3. **ShrunkPet** (ours `ShrunkPet.cs`, 119 lines): `TryShrink` rejects a mount on `Map.Internal` (`:42`, so never while
   ridden), and requires `ControlMaster == pm` (`:44`), so a mount assigned with the companion as master is refused.
   Dismounted and still mastered by the player, it shrinks and restores normally. **Two defects in ours, found by
   reading, not run:** (a) restore sets raw `ControlOrder = Follow` (`:100`) after `SetControlMaster` cleared the
   target, so the pet stops following; (b) `TryShrink` lowers `Followers` by hand (`:59`) but keeps `Master`, so after a
   restart the shrunk pet counts again and restore adds its slots twice. Flagged as a separate task (not this one).
4. **Following the owner and no-mount regions:** nothing in pinned dismounts a pet rider when the owner mounts or
   dismounts (8 `Dismount` call sites, none of them that). `BaseRegion.MountsAllowed` has **0** overrides, and
   `BaseMount.CheckMountAllowed` checks only `if (mob is PlayerMobile)` (`BaseMount.cs:283-309`, verified), so it always
   allows an NPC rider. No region forces a dismount. The Dismount weapon ability **does** knock a creature off
   (`Items/Weapons/Abilities/Dismount.cs:97-100`). "Mount when the owner mounts" and "dismount where the owner cannot
   ride" are therefore ours to write: a check on the owner's region and `Mounted` state from the companion's `OnThink`.
   Doom and Ter Mur restrictions beyond this grep: **unverified**.

---

## 6. Rooms and the pigeon

**What the source does.** Fee 300 gold once, pack or bank (`RoomAttendant.cs:599`). Then `RoomAFunctions.Room`
(`:1005-1048`): put a `CarrierPigeon` holding the squire in the owner's pack (or on the ground if full),
`SetControlMaster(null)`, `Internalize()`, `Controlled = true`. **No list on the attendant or the player**; the pigeon's
field is the only reference, and deleting the pigeon deletes the squire (`CarrierPigeon.cs:82-96`).

**How that maps to pinned.** Pinned's `SetControlMaster(null)` sets `Controlled = false` (`BaseCreature.cs:3750-3758`);
the source then forces it back true, leaving a controlled creature with no master. That only escapes pinned's
abandoned-pet sweep by accident: `AfterDeserialization` starts a **3-day delete** for any creature with an owner, not
controlled and not stabled (`BaseCreature.cs:2504-2507`, verified). `IsStabled` is **not saved**; it is rebuilt from
`PlayerMobile.Stabled` at load (`PlayerMobile.cs:3099-3108`). Do not copy the source pattern.

**Options:**
- (a) Reuse pinned stabling verbatim: `AnimalTrainer.EndStable` (`AnimalTrainer.cs:253-267`) to room and `DoClaim`
  (`:355-370`) to retrieve, including `pm.AddStabled`. Zero patches, survives restart, cleaned up when the character is
  deleted (`PlayerMobile.cs:3829-3836`). **But** roomed companions would share the stable count, appear in any Animal
  Trainer's claim list (claim has no body check; only `EndStable` rejects human bodies, `:211-213`), and could be pulled
  by a Ball of Summoning. **This conflicts with the decision "no stabling for companions".**
- (b) **Recommended:** our own registry, a `GenericPersistence` subclass (pattern:
  `ChampionTitleSystem.cs:9`, character-delete event `:28`, event raised `PlayerMobile.cs:3819-3820`) mapping owner to
  roomed companions. Room = `Internalize()` + `SetControlMaster(null)` + `IsStabled = true` + `StabledBy = owner`,
  record in the registry; on load, set `IsStabled`/`StabledBy` from the registry **before** the abandoned-pet check
  matters (an `[AfterDeserialization]` ordering question to probe in a test: **unverified** which runs first). Still no
  pinned patch. `IsStabled` also exempts the companion from the loyalty squatter sweep (`BaseCreature.cs:6030`) and
  spawner counts.
- Logout: with "no stabling", companions should **opt out of auto-stable** (`CanAutoStable => false`, our patch) and
  instead be roomed automatically or left in the world. **Not decided anywhere I could read**; Chase's call (it may be
  in the design doc).

**RoomAttendant** must derive from `PlayerBarkeeper` (section 1.2) and counts against the house barkeep cap
(`BaseHouse.cs:27`, `MaximumBarkeepCount = 2`).

**Room slots on the stable rule.** `AnimalTrainer.GetMaxStabled` (`AnimalTrainer.cs:58-99`, verified) is
`public static`, no hook, one caller (`:245`): base 2-5 from summed Taming + Lore + Veterinary, plus `(skill - 90) / 10`
for each of the three at 100 or more. F-12 ties stable slots to **max level** instead, which needs a patch to that
method (F-12's own item). Rooms are our code, so `CompanionRooms.MaxRooms(pm)` reads max level from the F-12 record
directly and needs **no patch**; if the F-12 stable patch lands, both read the same table row (section 7.4). Fidelity
note in passing: ServUO's version adds reward slots, +2 SA, +2 TOL and mastery slots (`ServUO-pub57
Scripts\Mobiles\NPCs\AnimalTrainer.cs:146-199`); pinned has none. 0 `AnimalTrainer` patches in `server\patches` (41
entries: 36 `.patch`, 5 `.cs`).

**The pigeon.** Recall (`CarrierPigeon.cs:28-81`): moves the squire to the user (`Location`, then `Map`), adds the user to
`Owners` (bypassing pinned `MaxOwners = 5`, `BaseCreature.cs:169`), `SetControlMaster(user)`, Follow, deletes the
pigeon. Checks: Movable, within 2 tiles, squire exists, user alive, followers. **No** owner check (anyone holding it
takes the squire), cost, cooldown, combat, travel or region check. A pinned version needs:
`MoveToWorld` (`Mobile.cs:2602`); the un-stable steps from `BallOfSummoning.SummonPet` (`BallOfSummoning.cs:216-250`);
an owner check (`StabledBy == from`); `SpellHelper.CheckTravel(from, map, loc, TravelCheckType.RecallTo, out msg)`
(`UOContent/Spells/Base/SpellHelper.cs:612`, consults `BaseRegion.CheckTravel`, `Regions/BaseRegion.cs:171`); and
`SpellHelper.CheckCombat` (`:203`). There is no `Region.AllowTravel` in either tree. Stock precedent for the refusals and
a 15 s cooldown: `BallOfSummoning.CastSummonPet` (`:161-214`, `PlayerMobile.LastPetBallTime` `:323`). Deleting the
pigeon must not delete the companion; with the registry the pigeon becomes a convenience, not the only reference.

---

## 7. Data tables

### 7.1 Where they live and how they load

- **Format: JSON**, read with pinned `JsonConfig.Deserialize<T>` (`Server/Json/JsonConfig.cs:62-71`). Its options allow
  `//` comments and trailing commas (`:33-40`), and read enums as strings (`JsonStringEnumConverter`) and types by name
  (`TypeConverterFactory`), so `"AI": "AI_Melee"` and `"Skill": "Healing"` are plain text. 22 UOContent files load data
  this way (e.g. `UOContent/Misc/NameList.cs:42-59`, `Gumps/Go/GoLocations.cs:59`).
- **Canonical copy, committed:** a new `server\data\companions\` folder in the shard repo, copied into the image at
  `/modernuo/Data/ShatteredLegacy/companions/` (the folder `ShardVersion.DataDirectory` already uses,
  `ShardVersion.cs:215`; Dockerfile precedent `docker\uo\Dockerfile:100`). Editing it is a data change and a rebuild,
  not a code change.
- **Live override:** `Configuration/companions/*.json`. `Configuration` is bind-mounted into the running container
  (`docker\uo\docker-compose.yml:18`; test `docker-compose.test.yml:39`), so Chase edits a line and runs a GM command
  `[CompanionData reload`. If an override file exists it wins for that table; the command reports which source each
  table came from. Override files are not committed (they sit under `server\uo`), so the habit is: try live, then copy
  the change into `server\data\companions\` and commit. (Precedent for a txt in `Configuration`:
  `ClusterFBulletin.cs:88`.)
- **Alternative rejected:** scalar `ServerConfiguration.GetOrUpdateSetting` keys (how ours does settings, e.g.
  `ClusterFPetMimicSettings.cs:33-96`). Fine for numbers, hopeless for line tables.

### 7.2 How a bad row fails

1. **Build time (the real gate):** a shard test (`server\tests`, run by `build.sh`) loads every shipped table and runs
   the same validator the server runs. Any invalid row fails the build with file, row and reason. Per AGENTS.md, the
   builder breaks one row on purpose, watches the build go red, and says so.
2. **Startup:** a shipped table that fails to parse **disables companions** (hiring and room retrieval refuse with a
   message, existing companions keep working on their last-known values) and logs loudly. It does **not** throw. Pinned's
   `NameList` precedent throws on a bad file (`NameList.cs:49-52`), which would take the server down for a typo.
3. **Reload:** row-level errors drop that row, log `file:row: reason`, and the rest loads. A file-level parse error
   keeps the **previous** table in memory and reports it to the GM. Never a half-loaded table.
4. **Cross-table checks:** every class's `PersonalityGate` names a real personality; every speech `Moment` is one the
   code fires (unused moments warn, missing required ones fail); weights are positive; level bands are contiguous.

### 7.3 Proposed shapes (first proposals, not decisions)

**`speech.json`** (personality x moment x gender). Lookup falls back `personality+gender` -> `personality+any` ->
`default+gender` -> `default+any`, so a new personality needs only the lines that differ. Tokens are a fixed list
(`{master}`, `{nickname}`, `{target}`, `{team}`), and an unknown token is a row error. SquireDialog's 150 situations
x 6 lines (765 Say + 141 Emote) is the seed content.

```json
{
  "Moments": {
    "HealedMaster": {
      "Gruff":   { "male": ["Hold still, {master}."], "any": ["Stop bleeding on me."] },
      "default": { "any": ["*bandages {master}*", "You will live, {master}."] }
    }
  },
  "EmotePrefix": "*"
}
```
A line starting with `*` is sent as an emote. `companions-combo-lines.md` (not read) presumably fits this table.

**`personality.json`** (roll by contract tier and weight):
```json
{ "Tiers": {
    "Common":  [ { "Personality": "Steady", "Weight": 60 }, { "Personality": "Gruff", "Weight": 30 }, { "Personality": "Zealous", "Weight": 10 } ],
    "Veteran": [ { "Personality": "Steady", "Weight": 30 }, { "Personality": "Zealous", "Weight": 40 }, { "Personality": "Cunning", "Weight": 30 } ] },
  "Personalities": [ { "Name": "Steady" }, { "Name": "Gruff" }, { "Name": "Zealous" }, { "Name": "Cunning" } ] }
```
The contract item carries its tier name; the roll happens once at hire and is saved on the record, so editing weights
never changes an existing companion.

**`classes.json`** (path, branch, skills, AI, gendered titles, personality gate):
```json
{ "Classes": [
  { "Id": "Squire", "Path": "Martial", "Branch": null, "AI": "Melee", "Skills": ["Swords","Tactics","Anatomy","Parry"],
    "Titles": { "male": "Squire", "female": "Squire" }, "PersonalityGate": [] },
  { "Id": "Templar", "Path": "Martial", "Branch": "Squire", "AI": "Melee", "Skills": ["Chivalry","Swords","Tactics","Parry"],
    "Titles": { "male": "Templar Knight", "female": "Templar Dame" }, "PersonalityGate": ["Zealous","Steady"] }
] }
```
`AI` names **our** companion AI roles (Melee, Archer, Mage, Healer, Bard, Rogue), not raw `AIType`, because three of the
six have no pinned AI (section 3). `Branch` must name an existing `Id`; cycles are a row error. Class-aware command words
("healers", "archers") come from a `CommandGroup` field per class, so they stay data too.

**`party.json`** (party size, slot costs and `FollowersMax`). **Superseded 2026-10-03:** the first draft (`FollowersMax`
5 rising to 8, keyed by max level) does not fit F-33's target. The slot costs and the shape now live in **section 11**;
the curve itself is P47's (question 6). The table keys on **loop count** (0 to 21), not max level, because the
2026-10-03 ladder makes max level a function of the loop (50, 100, then +5 per loop). Lookup takes the highest row at or
below the character's loop. It is applied wherever `ClusterFSkillCaps.Apply` runs (login, world load, loop change),
writing `FollowersMax` (serialized per mobile, property `Mobile.cs:851`).

---

## 8. Breeding readiness only

- **Pinned has no creature breeding hooks.** Grep of all `Projects\*.cs` for breed, mating, mate, PetBreeding,
  generation: 62 hits, **0** a creature mechanic (plant cross-breeding in `Engines/Plants` is the only genetics). No
  parent, gender or sex member on `BaseCreature`.
- **Sex already exists:** `Mobile.Female` (`Server/Mobiles/Mobile.cs:1178-1190`, serialized `:2429`). Use it.
- **Parents and generation fit as `[SerializableField]` from the first build.** Adding them later costs a version bump.
- **Types:** a `Mobile` reference deserializes to **null** once the parent is gone
  (`Server/Serialization/SerializationExtensions.cs:32-51`); a raw `Serial` can be **reissued** after a restart, since
  the next serial restarts from the highest live one (`Server/Serialization/GenericEntityPersistence.cs:615`,
  `:820-848`). So: a never-reused `LineageId` (`Guid` or a persisted `ulong` counter) on every companion,
  `Parent1Id`/`Parent2Id` as lineage ids, `Generation` as `int`, and the lineage registry (id -> name, sex, parents,
  generation) that outlives deletion. Ours has one small precedent: `PackMule` `_isMale`, `_nextBreedTime`
  (`PackMule.cs:41-47`).
- Evo's mating path was not sized, as asked. `Mercenary` returns no egg (`Mercenary.cs:43-46`), so its breeding is inert.

---

## 11. Addendum 2026-10-03: slot costs for the F-33 target, the new ladder, and the mule

Written after the features chat's update (`docs\feature-queue.md`, F-12 "Ladder and reserve" `:1144`, F-33 `:2319`).
**This is the companions side of P47 question 6:** P47 sets the `FollowersMax` curve and should read these costs from
here. (They belong in the design doc too, but that is a claude.ai project doc I cannot edit; the overseer should copy
11.2 into it.)

### 11.1 Correction to how F-33 quotes P41

F-33 (`feature-queue.md`, mule bullet "Requirement") says P41 proposes "a Squire costing 3 slots, rising with rank".
P41 did not propose that. The **source** Squire costs a flat 3 (`Squire.cs:520`), and its contract refuses unless 5
slots are free (`SquireContract.cs:48`). P41's `CompanionSlots` column was the **number** of companions (1 to 4), not a
cost. Both source numbers are dropped below.

### 11.2 Proposed slot costs (first proposal, for Chase)

| Follower | Slot cost | Basis |
|---|---|---|
| Companion, rank tier 1 (first third of the rank ladder) | **1** | A new player at `FollowersMax` 5 can run a companion beside a mule and an ordinary pet. |
| Companion, rank tier 2 (middle third) | **2** | Same as pinned `BaseHire` (`Hireables/BaseHire.cs:38`). |
| Companion, top rank tier | **3** | The source Squire's cost, kept only for the top tier. |
| Compact Mule | **1**, **0** with Trailwise Tack III | Decided (F-33). |
| Evolution mount beast, by stage (3 stages) | **2 / 3 / 4** | Final stage 4 is what every Evo mount spec uses at every stage (10 specs: Dragon, Cu Sidhe, Hellsteed, Kirin, Nightmare, Frenzied Ostard, Ridable Llama, Ridable Polar Bear, Unicorn, Hiryu; each sets 4 on all 3 stages) and matches stock top mounts (Hiryu 4, Cu Sidhe 4 in pinned; Nightmare, Kirin, Unicorn 2). Cheaper early stages are ours. |

Full party size: **4 companions**, my placeholder. The design doc may fix a different number; the formula below is what
P47 should recompute against.

**Budget at the target:** `party x top cost + mule + evo mount` = 4 x 3 + 1 + 4 = **17 without Tack III, 16 with it**.
So `FollowersMax` must be at least **16 at loop 11** (max level 150) and **17 at loop 21** (max level 200). Pinned's
default is 5 (`Mobile.cs:7827`).

One curve that meets it, as a check for P47, not a proposal over theirs: 5 at loop 0, +1 per loop to **16 at loop 11**,
then +1 at loops 16 and 21 (**18 at loop 21**, one spare slot). Sensitivity: each extra companion in the party adds 3
to both thresholds (party of 5 needs 19 and 20).

**Two things for the design doc to settle:** (1) where the three rank tiers fall. A companion cannot rank past its
owner's loops, so if the top tier opens after loop 11, the loop-11 test is about capacity only, since no top-rank party
can exist yet. (2) Whether the evo mount is a companion-system creature or Evo's own (its cost is listed either way).

### 11.3 Engine facts behind the budget (pinned d4531cd94)

- **A slot cost of 0 is safe:** pinned has no special case for 0 (the only checks are arithmetic,
  `BaseCreature.cs:2630`, `:2644`, `:3770`). `ControlSlots` defaults to 1 (`:509-513`).
- **Changing a cost on a controlled pet must re-count followers.** `ControlSlots` is a plain generated field
  (`BaseCreature.cs:505-509`) with no follower adjustment, and `RemoveFollowers` subtracts the **current** value
  (`:2625-2634`). A companion rank-up, an evo stage change, or installing Tack III must call `RemoveFollowers()`, set
  the value, then `AddFollowers()` (both public, `:2625`, `:2639`). Otherwise `Followers` drifts until the next restart
  rebuilds it (`:2514`). This is the same class of bug as ShrunkPet's (section 5 item 3).
- **How a mounted pet counts (P47 asks this):** a ridden `BaseMount` keeps its master **and its slots**; the `Rider`
  setter does not touch control (`BaseMount.cs:77-135`). So the mule and an evo mount cost their slots whether ridden or
  not, and whoever rides them. An ethereal is the opposite: its `FollowerSlots` move to whoever rides it
  (`Ethereals.cs:154-168`, checked against the rider at `:201`).
- **The new ladder changes nothing else in sections 2.5 or 7.** Per-skill cap = max level still holds. The companion
  record keeps its own `LoopCount`, capped at the owner's (Chase 2026-10-02), and `MaxLevel` follows from it on the same
  ladder. Owners now have 21 loops for companions to follow.

### 11.4 Where my plans touch the mule

- **Code fact first:** `PackMule.cs:88` sets `ControlSlots = 2` ("like a Nightmare"). The file's last commit was
  2026-05-31 (`9f5dc21`) and the shard repo shows no uncommitted change to it, so the 1-slot rule in F-33 is **not yet in
  the code**. The mule build must make it 1, and make Tack III take it to 0 with the re-count from 11.3.
- **Records: no double design.** P41 cited `PackMule` (`PackMule.cs:41-47`, `_isMale`, `_nextBreedTime`) only as
  precedent for keeping state on the creature as `[SerializableField]`. Nothing in P41 changes the mule. One
  recommendation for the breeding chat: **one lineage registry for every bred creature** (mule and companions alike),
  using never-reused ids as in section 8. Note that `PackMule` keeps its own `_isMale` where `Mobile.Female` already
  exists (`Mobile.cs:1178`).
- **Shared mechanisms, not shared designs.** Four of the 17 modules need the same engine work as companions, so build
  them once in a follower-behaviour layer:
  - Trailwise Tack "follows through gates and teleporters" is the companion follow rule (`TeleportPets`,
    `BaseCreature.cs:4092-4124`).
  - Arcane Ward III's emergency recall to the stable is the pigeon's travel-checked recall (section 6). Note the mule
    is **stabled**; companions are **roomed**.
  - Thieves' Shadow Cloak needs a creature that hides and stays hidden while moving, which pinned does not have
    (section 3, stealth rogue; **unverified**).
  - Field Medic Pack's self-heal is the `CanHeal` path or `BeginHeal` (section 2.4).
- ShrunkPet's two defects (section 5) also hit the mule if it is ever shrunk.

---

## 9. For the overseer: possible conflicts with the design doc I could not read

1. Section 6: reusing `PlayerMobile.Stabled` contradicts "no stabling for companions"; I recommend our own registry.
   What happens to companions at **logout** is open.
2. Section 2.5: the record on the creature means a companion's levels survive the owner's reset (assumption).
3. Section 11.2: party size (4 is my placeholder), where the three rank tiers fall, and the slot costs themselves.
4. Section 1.5: looting rights, steal, peacemaking on players and the pigeon-as-token are dropped or gated here; if the
   design kept any of them, it needs an explicit rule.
5. The exact parity list needs about 4 pinned patches (section 2). If the design accepts "near parity", each one becomes
   a recorded deviation instead.

---

## 10. Proposed build order (one builder per batch)

Each batch builds through `build.sh`, ships a test where it adds a gate, and leaves the shard working. Rough sizes in
brackets.

1. **B1 Companion base and record [M].** `BaseCompanion : BaseCreature` (partial, generated serialization): record
   fields (levels, loop, peaks, personality, class id, `LineageId`, parents, generation); player `HitsMax/StamMax/ManaMax`;
   never `SetDamage`; weapon element split on equip; `CanAutoStable => false`; slot-cost changes always re-count followers (11.3); `ClusterFSkillCaps.Apply` overload and
   `ShouldBoost` including companions. Tests: caps and `Skills.Cap` applied; an armed companion uses weapon dice; gain
   boost reaches a companion. One GM-spawnable test companion, no hiring yet.
2. **B2 Data tables [M].** Loader, validator, `[CompanionData reload`, the four tables with seed rows, the shard test
   that validates every shipped row (proven red on a broken row). Seed speech from SquireDialog's 150 situations.
3. **B3 Parity patches [S each, argued first].** Notes first per AGENTS.md (alternatives argued), then one patch each:
   SkillCheck pet x2 and pet stat delay (exclude companions), `SamuraiSpell.CheckExpansion`, resurrection loss at the 2
   loops with the Healing rule. Can run any time after B1; each is optional if Chase accepts the deviation.
4. **B4 Hiring and gumps [M].** Contract and representative vendor, slot rule from `party.json`, customize gump and lore
   gump as DynamicGumps with the owner check in `OnResponse`, equip-by-drop rules with our own Str and race checks.
5. **B5 Commands [M].** `OnSpeech` parser (owner; all / name / nickname / team / class-group prefixes; never
   `e.Handled`), native orders through `IssueOrder`, weapon sets, the safe subset of the 86 Squire commands.
6. **B6 Companion AI, part 1 [M].** `ForcedAI` with `Obey` overrides (fight back while following, party-wide guard);
   Melee and Archer (bolt fix, ranged swap inside our AI); Mage with master and party heals.
7. **B7 Companion AI, part 2 [L].** Healer with real bandages (`BeginHeal`) and potions; Chivalry with tithing. Probe tests
   first for the unverified bits (creature bandage healer, creature bard user, hidden creature moving), then Bard and
   Rogue, or decline either if the probes fail.
8. **B8 Mounts [S].** Mount and dismount by code, follow the owner's mounted state, dismount where the owner cannot ride,
   `IssueOrder(Follow)` after dismount. (ShrunkPet's two defects are a separate task.)
9. **B9 Rooms and pigeon [M].** Registry persistence with `IsStabled` restored on load (probe the abandoned-pet ordering
   first), `RoomAttendant : PlayerBarkeeper`, contract, room cap from `party.json`, pigeon with owner, travel, combat and
   cooldown checks; deleting a pigeon never deletes a companion.
10. **B10 Training contracts and instructors [S].** One contract base and 26 thin types; 4 instructors and 7 SB lists.
11. **Later, own chat:** breeding (record fields already present from B1), and any Evo stage tables.

---

## Unverified (collected)

1. The design doc and combo-lines doc (not on disk).
2. Live and test `modernuo.json` values (under `server\uo`, not read): skill-gain settings, `statMax`, anti-macro state.
3. A creature as user of: bandage healing (`BeginHeal`), bard skill handlers, hiding and stealth movement,
   transformation spells, a target `Invoke` relayed from the master.
4. Whether the abandoned-pet check or our registry's load hook runs first (section 6, option b).
5. Whether a creature lifting from an innocent corpse flags anyone criminal.
6. An AI swap's effect on the AI-side persistent order of a controlled pet.
7. Doom and Ter Mur mount rules beyond the `MountsAllowed`/`CheckMountAllowed` grep.
8. `MercenarySpec` contents (not in the download); the 4 Evo AI files and `BaseMountEvo.cs` were only skimmed.
9. 24 of the 26 training contracts were checked by grep for sameness, not read line by line.
