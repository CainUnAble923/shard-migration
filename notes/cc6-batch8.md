# CC6 batch 8 — the Stygian Abyss boss tier (Q-052 answered yes)

This task closed **4 spawn names, 4 entries** in four parts: **Part A**, the creature half of B14 Instanced
Peerless without its engine — ServUO's `BasePeerless` (367 lines → 339) and `BaseSABoss` (190 → 212) with their
final parents, and `Putrefaction`, the one of `PackResources`' six ML resources pinned lacks; **Part C**, Navrey
Night-Eyes, a plain `BaseCreature` that batch 7 §9 had filed under Q-052 by mistake, with `EyeOfNavrey`, `Tangle1`
and `UntranslatedAncientTome`; **Part B**, the Slasher of Veils and the Stygian Dragon with `StygianDragonHead`,
`LifeSyphon` and `VampiricEssence`; **Part D**, Medusa with her clone, `UndeadGargoyle`, and her three resources.
`tools/spawn-orphans.txt` went **23 → 19** by the script. A+C were built and committed on their own (`339a9e9`)
before B touched the tree; B and D were built together and committed separately (§6 says which build proved what).

**Q-052 is answered: yes.** The answer is recorded verbatim in `notes/codex-questions.md` and the header flipped.
What it buys is the boss tier of the expansion this project exists to fill; what it costs is one accepted
difference, **D-79**, recorded once for the whole batch: no altar, no instancing, no teleporters, the bosses are
walk-up fights, and the three keys P9 ported (`ShatteredCrystals`, `DraconicOrb`, `SerpentFangKey`) are consumed by
nothing.

Three things this note corrects or adds, counted rather than described:

- **The altar coupling in `BasePeerless` is seven sites, not "3 references / 11 lines".** Batch 4 §8's two numbers
  are both literally right — `PeerlessAltar` appears 3 times (lines 10, 13, 163) and `m_Altar` on 11 lines (10, 17,
  21, 137, 138, 154, 163, 207, 208, 253, 254) — and both hide the shape: a field, a GameMaster property, a death
  hook, **both sides of serialization**, an all-helpers-dead check and a helper registration. §2 says what was done
  at each. The serialization pair is the one that mattered, because whatever is written there is the save format.
- **Navrey is not on this base.** `Navrey : BaseCreature` (`Mobiles/Bosses/Navery/Navrey.cs:9`); she was gated on
  nothing and could have been ported in any of the last five batches. She is here because she belongs with the
  Abyss tier. And she has **no parameterless constructor in ServUO** — only `Navrey(NavreysController)` — so
  ServUO's own spawner could never have built her from a `Navrey` entry either; ours gives her one.
- **The subclass rule holds at three levels.** `SlasherOfVeils : BaseSABoss : BasePeerless : BaseCreature`, each
  with its own generator attribute, its own `(Serial)` constructor and its own `Serialize` — pinned in the test by
  reflection and by a real `BufferWriter`/`BufferReader` round trip at every level.

## 1. The selection, from batch 7 §9's "bosses (Q-052)" row

| part | ServUO | lines | ours | closes |
|---|---|---|---|---|
| A | `Services/Peerless/BasePeerless.cs`, `Mobiles/Normal/BaseSABosses.cs` | 557 | same paths | nothing by itself; the base the next three need |
| C | `Mobiles/Bosses/Navery/Navrey.cs`, `EyeOfNavrey.cs`; `Items/Artifacts/Equipment/Clothing/Tangle1.cs`; `Items/Quest/SAQuestItems.cs` (one type) | 185 + 41 + 75 + ~40 | `NavreyNightEyes` (Q-056 provisional), the rest by name | `NavreyNightEyes`, 1 entry (Underworld [1053,861,-32]) |
| B | `Mobiles/Bosses/SlasherOfVeils.cs`, `StygianDragon.cs`; `LifeSyphon.cs`, `VampiricEssence.cs`; `SAQuestItems.cs` (one type) | 205 + 463 + 53 + 54 + ~40 | by name | `SlasherOfVeils` (Abyss [749,475,-17]), `StygianDragon` ([326,159,20]), 1 entry each |
| D | `Mobiles/Bosses/Medusa.cs` (Medusa, MedusaClone, AddCloneCommands); `Mobiles/Normal/UndeadGargoyle.cs`; `Items/Resource/Medusa{Light,Dark}Scales.cs`, `MedusaBlood.cs` | 809 + 90 + 47 + 47 + 50 | by name | `Medusa`, 1 entry ([818,927,-15]) |

`Niporailem` (the fourth `BaseSABoss`, one entry, `TerMur.json`) is now an ordinary port; §9.

## 2. The altar, site by site

`D:\UO\ServUO-pub57\Scripts\Services\Peerless\BasePeerless.cs`, re-read for this batch:

| lines | what ServUO does | what ours does |
|---|---|---|
| 10-23 | `private PeerlessAltar m_Altar;` and a `[CommandProperty]` `Altar` over it | gone. There is no altar type in either tree to point at; the test asserts `GetProperty("Altar")` is null and `FindTypeByName("PeerlessAltar")` is null |
| 137-138 | `OnDeath`: `if (m_Altar != null) m_Altar.OnPeerlessDeath();` — the altar's instance-teardown hook | gone; a comment marks the site |
| 148-164 | `Serialize` writes version 0 then `(Item)m_Altar`; `Deserialize` reads it back `as PeerlessAltar` | **gone. Version 0 carries nothing.** The generator's `Serialize` for `BasePeerless` is `base.Serialize(writer)` + its own version int; the test asserts the type declares no `[SerializableField]`. A future altar is a new field and a version bump on `BasePeerless` alone — an ordinary migration, because the parent chain does not move (AGENTS.md's final-parent rule is about ancestors, not fields) |
| 203-212 | `AllHelpersDead => m_Altar != null ? m_Altar.AllHelpersDead() : true` | the altar-less arm: `true` |
| 253-254 | `SpawnHelper`: `if (m_Altar != null) m_Altar.AddHelper(helper);` — the altar tracks helpers to delete them at reset | gone; a helper is placed with `Home`/`RangeHome` and not tracked. Medusa tracks her own in `_helpers` (ServUO does too) and deletes them in `OnAfterDelete`, so nothing leaks from the one boss here that spawns helpers |

And the rest of the file, which is creature-side and ported as written: `CanBeParagon` (dropped, D-81), `DropPrimer`
(kept as a virtual, its branch dropped, D-80), `GiveMLSpecial` with the 35-item ML special table (all 35 resolve: 2
pinned, 33 ours from CC9), `Unprovokable`, `ChangeCombatant`, the helper-wave machinery, `PackResources` (six ML
resources: five pinned, `Putrefaction` ported), `PackItems`, `PackTalismans`, `FireRing`.

**The save-format fact, tested rather than reasoned:** a `BasePeerless` with a name, hue, body, hits, strength and
`CurrentWave = 3` is written through `BufferWriter` and read into a fresh `new BasePeerless(serial)` through
`BufferReader`; name, hue, body, hits, strength, AI, location and map come back equal, and `CurrentWave` comes back
**0** — ServUO never serialized `m_CurrentWave` either, so a boss reloaded from a save has no helper waves left on
both emulators (a quirk copied, §5). The same round trip on a `SlasherOfVeils` (three levels) and a `Medusa` (with
her `LightScales` and her living helpers) is in §6.

## 3. Pre-flight: what the sixteen ServUO files needed, checked in `D:\UO\ModernUO-pinned` AND `server/customizations`

One grep for every `new X(`, `typeof(X)` and member over both trees, and this time also **what the stock tree does
with each type** (batch 7 §8's addition to the pre-flight).

| ServUO reference | pinned / ours | what was done |
|---|---|---|
| the 35 `GiveMLSpecial` items | `CrimsonCincture` pinned; `HumanFeyLeggings` + 32 set pieces + `Feathernock`, `Swiftflight` ours (CC9) | as written; 100 kills of a bare `BasePeerless` in the test drop only these |
| `SkillMasteryPrimer` | absent from pinned (no Skill Masteries: "mastery" occurs in a buff icon, a ConPVP ruleset and a book) | **D-80** |
| `MondainsLegacy.DropPeerlessMinor(c)` | no such method; pinned's `MondainsLegacy.Artifacts` is the same 21-type list as ServUO's `m_Artifacts` | reproduced inline: `Loot.Construct(Artifacts.RandomElement())` onto the corpse. ServUO also clears `ElfOnly` on the drop; pinned has no `ICanBeElfOrHuman` |
| `CanBeParagon` | no such virtual; `Paragon.CheckConvert` excludes by type list and `Paragon.Maps = { Ilshenar }` | **D-81** |
| `BaseCreature.GetSpawnPosition(int)` | absent | ServUO's static body reproduced on `BasePeerless` |
| `Blight`, `Scourge`, `Taint`, `Corruption`, `Muculent` / `Putrefaction` | pinned `Items/Resources/MiscMLResources.cs` / **absent** | ported `Items/Resource/Putrefaction.cs` (0x3186, hue 883, `ICommodity` as ServUO — note pinned's five siblings are not) |
| `Loot.RandomTalisman`, `SpellHelper.GetSurfaceTop(ref IPoint3D)`, `Effects.SendLocationEffect(Point3D, …)` | present | as written; `new Point3D(po)` after the surface-top |
| `[TypeAlias("Server.Mobiles.BaseSABosses")]` | ServUO's own earlier spelling of the abstract base | not reproduced: no save of ours ever carried it and an abstract type is never a saved type name |
| `DamageEntry.Damager/DamageGiven`, `GetDamageMaster`, `CheckHold(m, item, false)`, `TryDropItem`, `Loot.Construct(Type)`, `NoKillAwards` | present | as `BaseRenowned` (batch 5) already had them |
| `GetLootingRights()` (instance) | static `GetLootingRights(List<DamageEntry>, int)` | `GetLootingRights(DamageEntries, HitsMax)` |
| **Navrey**: `NavreysController` (`Services/Underworld/Navrey's Lair/`, 291 lines; 651 with the lair) | absent | the serialized `m_Spawner`, `OnNavreyKilled` and the spawner-taking constructor dropped; `UsedPillars` kept unserialized as ServUO has it. **D-83** |
| `PlayerMobile.Quests`, `GreenWithEnvyQuest`, `BaseQuest` | S5's engine (Q-025) | the eye hand-out dropped; `EyeOfNavrey` ported beside her. **D-84** |
| `SetSpecialAbility(Webbing)` | no `MonsterAbility` throws a web | **D-82** |
| `TeleportChance => 0` | no such virtual; `MageAI.cs:19,215` has its own 5% × Magery | **D-85** |
| `Loot.MysticismScrollTypes` / `RandomScroll(…, SpellbookType.Mystic)` | pinned ships the 16 Mysticism scrolls (`Items/Skill Items/Magical/Scrolls/Mysticism/`) but `Loot` has no array and routes `Mystic` to the regular list | ServUO's 16-type array carried on `NavreyNightEyes.MysticismScrollTypes`, `Loot.Construct<SpellScroll>(types, RandomMinMax(0, Length))` — one past the end packs nothing, as ServUO's does |
| `Poison.Parasitic` | ServUO's static is `GetPoison("DeadlyParasitic")`; pinned names the kinds individually | `Poison.DeadlyParasitic` (stock `ParasiticPotion.cs:11` uses it) |
| `ScrollOfTranscendence.CreateRandom(30, 30)` | `ScrollofTranscendence` (lower-case *of*), same `CreateRandom(min, max)` | renamed |
| `NightEyes`, `TatteredAncientScroll`, `LuckyCoin`, `DemonKnight.FindRandomPlayer` | ours / ours / ours / pinned | as written |
| `Tangle1 : HalfApron` with `[Alterable(DefTailoring, GargishTangle1)]`; `GargishTangle1 : GargoyleHalfApron` | `HalfApron` pinned; `[Alterable]` D-20; **no gargish half apron in pinned at all** | `Tangle1` ported; the gargish twin not (no base, and D-20 makes it `[add`-only) |
| `UntranslatedAncientTome`, `StygianDragonHead` (`SAQuestItems.cs`) | absent | ported, one type per file (the `LuckyCoin` precedent) |
| **Slasher**: `AngryFire`, `ManaDrain`, `TrueFear` | no `MonsterAbility` does any of the three (see D-82 for what they do) | **D-82** |
| `OnDamagedBySpell(Mobile)` | `(Mobile from, int damage)` | same body |
| `SetWeaponAbility(ParalyzingBlow)` | recipe | `GetWeaponAbility` |
| the 14 artifact types | all ours (CC9) | as written; the test constructs each |
| **Stygian Dragon**: `SetSpecialAbility(DragonBreath)` | `MonsterAbilities.FireBreath` (Q-054) | `GetMonsterAbilities`, the follow-up's shape. **A keyword hit, not a loss** |
| `SetWeaponAbility(Bladeweave)` + `(TalonStrike)` | recipe | `GetWeaponAbility`, `RandomBool` between the two |
| `DragonBlood => 48` | no property, no item (recipe; Q-049 open) | dropped, Q-049 cited, no new number |
| `ScreenLightFlash.Instance` / `Packet` / `NetState.Send` | no `Packet` class; `NetState.SendScreenEffect(ScreenEffectType.LightFlash)` (`OutgoingEffectPackets.cs:322`) | rewritten over `Map.GetClientsInRange(Location, Core.GlobalUpdateRange)` |
| `Movement.Movement.Offset`, `Utility.GetDirection(this, Combatant)`, `SpellHelper.AdjustField`, `Effects.SendMovingParticles` (14-arg with `EffectLayer`), `Mobile.MovingParticles` (12-arg), `FixedParticles` (7-arg), `Map.GetMobilesInBounds`, `Item.GetMobilesInRange(0)`, `AOS.Damage` 8- and 12-arg | all present; `GetDirection` takes two points | as written; `ColUtility.Free` dropped (a ServUO pool); `Timer.DelayCall(TimeSpan, TimerStateCallback, object[])` a lambda |
| `FireField.Serialize` writes nothing ("Unsaved") | the generator saves whole | `[AfterDeserialization(false)] Delete()`: a field caught by a save deletes itself on load. §5, a fix |
| `LifeSyphon : BloodBlade`, `VampiricEssence : Cutlass`; `WeaponAttributes.BloodDrinker = 1` | bases pinned; `AosWeaponAttribute` has no `BloodDrinker` and `BaseWeapon.OnHit` no branch for it (ServUO's is `BaseWeapon.cs:5822`) | **D-87** |
| `Paragon.ChestChance`, `ParagonChest(string, int)`, `HideType.Barbed`, `ScaleType`, `Tamable`, `AutoDispel`, `CanFlee` | present | as written |
| **Medusa**: `ICarvable.Carve` returns `bool` | `void` (`Interfaces.cs:16`); knives reach it through `BladedItemTarget.cs:34` | same body |
| `GorgonLenseCharges`, `GorgonLenseType`, `LenseType`, `GorgonLense.TotalCharges` on `BaseArmor`/`BaseClothing`/`BaseJewel` | **none of it exists in pinned** | `CheckBlockGaze` kept as a method returning `false`. **D-88** |
| `IFreezable.OnRequestedAnimation` → `UpdateStatueAnimation` | pinned's `PlayerMobile.CanSee` (:3340) asks only a `CharacterStatue`; the packet exists (`CharacterStatuePackets`) | dropped. **D-89** |
| `SetSpecialAbility(VenomousBite)` | no `MonsterAbility` poisons everyone within 3 tiles on a hit | **D-82** |
| `OnCarve(Mobile, Corpse, Item)`, `Corpse.Carved`, `OnGotMeleeAttack` (+`int`), `OnHarmfulSpell`, `IgnoreYoungProtection`, `AutoDispelChance`, `BaseCreature.Summon(creature, controlled, caster, p, sound, duration)`, `SolidHueOverride`, `Map.CanFit(x,y,z,16,false,false)`, `LootPack.SuperBoss`, `Blood(int)`, `EffectItem.Create` | present | as written |
| `BuffInfo.AddBuff(m, …)` / `RemoveBuff` | instance methods on `PlayerMobile` | `(target as PlayerMobile)?.AddBuff(new BuffInfo(BuffIcon.MedusaStone, 1153790, 1153825))`; `BuffIcon.MedusaStone` is pinned's |
| `m.Send(new RemoveMobile(clone))`, `MobileIncoming.Create` | `NetState.SendRemoveEntity(Serial)`, `SendMobileIncoming(beholder, beheld)` | rewritten |
| `m_Scales` (int) + the helper list, both serialized | the generator names a property after its field and `Scales` would hide `BaseCreature.Scales` | `[SerializableField(0)] _lightScales` → `LightScales`; `[SerializableField(1)] List<Mobile> _helpers` → `Helpers` (`ChampionSpawn._creatures` is the precedent); ServUO's "alive only" filter on read is an `[AfterDeserialization(false)]` prune |
| `OphidianWarrior`, `OphidianArchmage`, `WailingBanshee`, `OgreLord`, `Dragon` / `UndeadGargoyle` | pinned / **absent** | `UndeadGargoyle` ported (90 lines, body 722 is a `bodyTable.cfg` row, `GargoylesPickaxe` pinned) |
| `Slither`, `IronwoodCompositeBow`, `Venom`, `PetrifiedSnake`, `StoneDragonsTooth`, `MedusaFloorTileAddonDeed`, `SummonersKilt`, `MedusaStatue` | all ours (CC9) | as written; the test constructs each |
| `MedusaLightScales`, `MedusaDarkScales`, `MedusaBlood` | absent | ported (`Items/Resource/`) |
| **the stock tree's slayer lists**: ServUO `Abilities/SlayerGroup.cs` lists Medusa under Repond (:70), the Slasher under Exorcism (:320), Navrey under ArachnidDoom (:426) and SpidersDeath (:451), the Stygian Dragon under ReptilianDeath (:503) and DragonSlaying (:528) | pinned's six entries are static `typeof` lists (`SlayerGroup.cs:21, 175, 287, 303, 322, 361`) matched by `IsAssignableFrom`; none of ours derives from a listed type | **D-86**; the test pins all six as not slaying |
| the stock talisman list (`TalismanSlayer.cs`) | names none of the four in ServUO either | nothing |
| bodies 735, 741, 826, 728, 722 | all `bodyTable.cfg` rows | — |

**The final-parent walk.** The B5 carrier regex was run over `BasePeerless.cs`, `BaseSABosses.cs` and all eleven
ServUO descendants (7 ML bosses directly, 4 through `BaseSABoss`; none of the eleven has a descendant of its own,
grepped) and hit **nothing**. Both bases sit on stock `BaseCreature`, which is the normal answer, and the test asserts
neither exposes a set-item member.

## 4. The batch, and what each file needed

| # | file (ServUO → ours) | lines | notes |
|---|---|---|---|
| 1 | `Services/Peerless/BasePeerless.cs` → same | 367 → 339 | §2. Constructor mirrors pinned `BaseCreature`'s `(ai, mode = Closest, rangePerception = 16, rangeFight = 1)`: every descendant passes 10 (rewritten to 16 in ServUO) and dead speeds (Q-008) |
| 2 | `Mobiles/Normal/BaseSABosses.cs` → same | 190 → 212 | abstract; `_damageEntries` created at construction as `BaseRenowned` does so a test can drive `AwardArtifact`; `OnBeforeDeath` still replaces it |
| 3 | `Items/Resource/MiscMLResources.cs` (Putrefaction) → `Items/Resource/Putrefaction.cs` | ~45 → 31 | the `(amountFrom, amountTo)` constructor kept beside the collapsed one |
| 4 | `Mobiles/Bosses/Navery/Navrey.cs` → `NavreyNightEyes.cs` | 185 → 183 | body 735, sound 389, 30000-35000 hits, fame 24000, `AI_Mage`, `AlwaysMurderer`, `DeadlyParasitic` immune, lethal hit poison, meat 1, 1-3 Mysticism scrolls, `AosSuperBoss` ×3; death: tome 50%, transcendence scroll 10%, tattered scroll 10%, lucky coin 10%, `NightEyes`/`Tangle1` 2.5% to a random nearby player |
| 5 | `EyeOfNavrey.cs` → same path | 41 → 21 | 0x318D, hue 68, blessed, label 1095154; nothing produces it (D-84) |
| 6 | `Items/Artifacts/Equipment/Clothing/Tangle1.cs` → same | 75 → 26 | hue 506, +10 Int, 5% defend, +2 mana regen, label 1114784 |
| 7 | `Items/Quest/UntranslatedAncientTome.cs` (from `SAQuestItems.cs`) | ~45 → 22 | 0x0FF2, hue 2405, stackable, label 1112992 |
| 8 | `Mobiles/Bosses/SlasherOfVeils.cs` → same | 205 → 173 | body 741, 50000-65000 hits, 10000 mana, five 20% damage types, fame 35000, `ParalyzingBlow`, provokable and bardable (re-overridden `false` on the base's `true`), sounds 1589/1586/1588/1587, `AosSuperBoss` ×4 + `Gems` ×8; 50% blink to a spell's caster; 7 unique + 7 shared artifacts |
| 9 | `Mobiles/Bosses/StygianDragon.cs` → same | 463 → 453 | body 826, sound 362, 30000 hits, 431 stam, 50% fire damage, fame 15000, meat 19, 30 barbed hides, 7 red scales, `FireBreath`, `Bladeweave`/`TalonStrike`; every 30-60 s one of the crimson meteor, the stygian fireball (120-150 chaos after 11 × 200 ms) or the fire column (8 `FireField`s, a client light flash); the head every death, a level-5 paragon chest 10%; 8 unique + 4 shared |
| 10 | `Items/Quest/StygianDragonHead.cs` (from `SAQuestItems.cs`) | ~40 → 19 | 0x2DB4, stackable, label 1031700 |
| 11 | `Items/Artifacts/Equipment/Weapons/LifeSyphon.cs`, `VampiricEssence.cs` → same | 53 → 27, 54 → 27 | the two CC9 left for `BloodDrinker` (D-87); hits 255 |
| 12 | `Mobiles/Bosses/Medusa.cs` → same (Medusa, `MedusaClone`, `AddCloneCommands`) | 809 → 745 | §3's Medusa rows. Body 728, 60000 hits, fame 22000, `MortalStrike`, bard-immune, always auto-dispels, lethal immune, 80/20 deadly/lethal hit poison, an immovable Ironwood bow and 100-200 arrows, 8-9 light scales to harvest, `SuperBoss` ×8, statue 2.5%; 6 unique + 1 shared |
| 13 | `Mobiles/Normal/UndeadGargoyle.cs` → same | 90 → 69 | body 722, sound 372, 200-300 hits, cold/energy damage, necromancy, fame 3500, treasure map 1, a gargoyle's pickaxe 2.5% |
| 14 | `Items/Resource/MedusaLightScales.cs`, `MedusaDarkScales.cs`, `MedusaBlood.cs` → same | 47 → 21, 47 → 20, 50 → 22 | 9908 hue 1266 / 9908 hue 2223 (one label, 1112626) / 0x2DB6 label 1031702 `ICommodity` |

Range perception dropped (all pass 10), speeds dropped (Q-008), serialization by the generator, `this.` removed,
`DateTime.UtcNow` → `Core.Now`. One red compile in the whole batch (build E: two errors in `Medusa.cs`, one missing
`using Server.Engines.BuffIcons;`) — every other content file compiled the first time. Five red test facts across
four builds, all mine and all test-side (§6).

**Q-056's shape, followed provisionally.** `Navrey` is ServUO's name and `NavreyNightEyes` the spawn entry's. Batch 7's
recommendation (option 2: the type takes the spawn-data spelling, no alias) is followed, **not settled here**: the
file header carries the ServUO name for grep, the test asserts `FindTypeByName("Navrey")` is null and the type
carries no `[TypeAlias]`. If Q-056 says option 1, the class becomes `Navrey` with one alias line; no save exists.

## 5. Deviations — note-local numbering, for `docs/fidelity-principle.md`

Batch 7 ended at D-78. Every "reverses when" names a patch and its reach, measured from `D:\UO\ServUO-pub57\Scripts`,
and every loss below was proved by grepping pinned for what the thing *does* before it was numbered.

| # | Deviation | Player notices | Reverses when |
|---|---|---|---|
| **D-79** | **The Abyss bosses are walk-up fights.** `BasePeerless` has no altar: no `PeerlessAltar`, no instance, no `PeerlessTeleporter`, no key consumption, no helper tracking; the four bosses stand on their stock spawners in the open Abyss and Underworld, and the P9 keys (`ShatteredCrystals`, `DraconicOrb`, `SerpentFangKey`, and batch 7's `DragonFlameKey`) are inert | a party walks to the boss instead of unlocking a private copy of the room; the key items drop and do nothing; a boss's helpers are not cleared when it dies (only Medusa spawns any, and she deletes hers herself) | **never, by decision (Q-052):** B14 Instanced Peerless stays WON'T. If it ever were built, `BasePeerless` gains one `Item` field and a version bump — an ordinary migration, because no ancestor moves. One number for the batch, per the brief |
| **D-80** | `BasePeerless` drops no `SkillMasteryPrimer` on death | nothing here: `BaseSABoss` sets `DropPrimer => false`, so none of the four bosses would have dropped one on ServUO either. Reach is the 7 ML peerless bosses (`DropPrimer => Core.TOL`, true on this shard), none ported (Q-057) | the Skill Masteries system (ServUO `Spells/Skill Masteries/`, 158-line primer + the masteries); a subsystem row, not a hunk |
| **D-81** | `CanBeParagon => false` is not carried: pinned has no such virtual | nothing reachable: `Paragon.CheckConvert` runs only on `Paragon.Maps = { Ilshenar }` and all four spawn on Ter Mur. A `BasePeerless` a GM places on Ilshenar could convert | **1 hunk**: a `CanBeParagon` virtual on `BaseCreature` read in `Paragon.CheckConvert` (`Paragon.cs:176`, the type-list exclusion). Reach: ServUO overrides it on 32 files |
| **D-82** | Five Pet-Training special abilities dropped: **Navrey** `Webbing` (a `SpiderWebbing` item thrown at a random target within 12 on any melee exchange); **Slasher** `AngryFire` (30-40 60/20/20 fire burst on hit, 30 mana, message 1070823), `ManaDrain` (40-60 mana from everyone within 8 on hit, to the creature), `TrueFear` (on approach within 8, a freeze of `13 − MagicResist/10` seconds with the five 1080339-43 messages, cooldown 1-3 min); **Medusa** `VenomousBite` (her hit poison to everyone within 3 on hit, 30 mana) | Navrey never webs; the Slasher never burns, drains or freezes; Medusa poisons one target at a time. The fights are easier than OSI's | **P6** (Pet Training abilities), the batch 3/4/5 row; pinned's `MonsterAbility` set has none of the five (grepped by behaviour: no web item, no mana drain, no approach-freeze, no area poison on hit). Reach in ServUO: Webbing 3 files, AngryFire 8, ManaDrain 5, TrueFear 3, VenomousBite 5 |
| **D-83** | Navrey has no lair: `NavreysController` (the pillars, the web tunnels, `OnNavreyKilled`) is not ported; `UsedPillars` is a GM property nothing sets | she stands on her Underworld spawner with no pillar mechanic; on ServUO she is only ever spawned by the controller | `Services/Underworld/Navrey's Lair` (651 lines) ported: `NavreyNightEyes` gains an `Item` field and a version bump. Reach: 1 creature |
| **D-84** | The Green With Envy proof: ServUO gives an `EyeOfNavrey` to every looting-rights holder on Vernix's quest; here nothing produces the item | a player on the quest (there is no quest) gets no eye | **S5's engine** (Q-025) plus `Quests/Vernix.cs` (251 lines); then the dropped loop is 15 lines on `NavreyNightEyes.OnDeath`. Reach: 1 creature, 1 quest |
| **D-85** | Navrey teleports: ServUO's `TeleportChance => 0` has no pinned counterpart, and `MageAI.cs:19,215` casts Teleport at 5% × Magery for every mage-AI creature | she blinks toward her target as any pinned mage does; on ServUO she never does | **1 hunk**: a `TeleportChance` virtual on `BaseCreature` read at `MageAI.cs:215`. Reach: 2 ServUO files override it |
| **D-86** | None of the four is a slayer target: ServUO lists Medusa under **Repond**, the Slasher under **Exorcism**, Navrey under **ArachnidDoom** and **SpidersDeath**, the Stygian Dragon under **ReptilianDeath** and **DragonSlaying** | a demon-, spider-, reptile-, dragon- or repond-slayer does normal damage to them; ServUO's doubles it | **6 `typeof` lines** in pinned `Items/Weapons/SlayerGroup.cs` (:21, :175, :287, :303, :322, :361). The same row batch 7 §8 proposed for D-77/D-78; it now reaches 20 of our types |
| **D-87** | `LifeSyphon` and `VampiricEssence` lose `BloodDrinker = 1` | the bleed a `BloodBlade`/`Cutlass` inflicts is not doubled and does not heal the wielder | a `BloodDrinker` member on `AosWeaponAttribute` (`AOS.cs:635-`) and the branch at ServUO `BaseWeapon.cs:5822` in pinned `BaseWeapon.OnHit`. Reach: 4 ServUO files set it. The SA weapon-attribute row `notes/s9-backlog-remeasure.md` §220 sized |
| **D-88** | Nothing deflects Medusa's gaze: the Gorgon Lens (`GorgonLenseCharges`/`GorgonLenseType` on armour, clothing and jewellery; `GorgonLense.TotalCharges`; `LenseType` Enhanced 100% / Regular 50% / Limited 15%) does not exist in pinned | every gaze petrifies; on OSI a lens-wearer is deflected and the lens loses a charge | the Gorgon Lens system: the item, three charge/type property pairs on `BaseArmor`, `BaseClothing`, `BaseJewel` (three patches) and their serialization. A subsystem row. Reach: Medusa, and the lens crafting |
| **D-89** | A petrified `MedusaClone` does not animate as a statue: ServUO's `IFreezable.OnRequestedAnimation` sends `UpdateStatueAnimation`; pinned's `PlayerMobile.CanSee` (:3340) asks only a `CharacterStatue` | the copy stands still, hue 761, instead of the statue pose | **1 hunk**: `PlayerMobile.CanSee` checking an interface pinned would need to add. Reach: `Medusa.cs` is ServUO's only `IFreezable` implementer |

Not numbered: `DragonBlood => 48` on the Stygian Dragon (Q-049, open, the recipe's rule); `GargishTangle1` (no
`GargoyleHalfApron` in pinned, and D-20 covers the only route to it); ServUO's `[TypeAlias]` on `BaseSABoss`
(§3).

**Bugs, by kind:**

- *Ours:* none found.
- *ServUO's, copied faithfully (bug-list §3):* `BasePeerless.m_CurrentWave` is never serialized, so a reloaded boss
  has no helper waves left (the test pins 0 after the round trip); the `FireRing` gate reads
  `m_NextFireRing > Core.TickCount`, the cooldown backwards (no descendant here turns `HasFireRing` on; the Slasher's
  own `FireRing` call is commented out in ServUO); `BaseSABoss.AwardArtifact` sizes the roll on the eligible players
  and then walks the full table (batch 5's finding, same code); `BaseSABoss.OnDeath` builds a `toGive` list on
  Felucca and Ter Mur and uses it for nothing; Navrey's scroll loop re-rolls its bound each iteration and can index
  one past the array; Medusa's `ReleaseStoneMonster` sets each nearby player's `Combatant` to the player themself;
  her gaze and stone placement search a `Random(10) - 1` offset (−1..8), not the ±5 it reads as; and
  `BaseCreature.Summon` in both trees refuses a summon when `caster.Followers + ControlSlots > FollowersMax` — both
  trees give every `Mobile` a `FollowersMax` of 5 (ServUO `Mobile.cs:11135`, pinned `:7721`) **and both add a
  summon's `ControlSlots` to its `SummonMaster`'s `Followers`** (ServUO `BaseCreature.cs:3684`, pinned
  `AddFollowers`, `:2303`), so Medusa's "five stone monsters" is really **five slots** — a `Dragon` is three — and a
  refused stone is deleted by `Summon`, still added to her list, and dropped by the next `DefragHelpers`. A gaze clone
  competes for the same five slots: with them full, the target is petrified and no statue appears. Build G found the
  refused banshee at (0,0,0) asserting "exactly 5"; the test now pins the slot arithmetic instead.
- *ServUO's, fixed:* **the Stygian Dragon's `FireField` "Unsaved" serialization.** ServUO's `Serialize` writes
  nothing and `Deserialize` reads nothing, so a field that reaches a save comes back as a headless item with no
  location and no timer, forever. Here the generator saves it whole and `[AfterDeserialization(false)]` deletes it on
  the first timer slice after the load — the same lifetime it had before the save ended it. A bug that makes
  something *broken*, fixed (D-4's rule); the test round-trips one and watches it delete itself.
- *ModernUO's, to report:* none new. The `Item.Amount <= 0` lines a real kill logs in the test host (107 in build A's
  log for 140 kills; batch 7's logs carry 7 for 10 kills, batch 5's 2) are stock `Corpse` noise on the fixture's
  kill path, not asserted and not ours.

## 6. What was proved

| Gate | Result |
|---|---|
| **Build A** (A+C, `--tests-only`, the six pins deliberately left at 23) | **red as intended: Passed 111, Failed 6**, `BUILD FAILED … No image was built.` The six failures were exactly the count pins in batches 1-5 and 7 (`Expected: 23 / Actual: 22`, six times); all 8 new facts green. The gate is live |
| **Build B** (A+C, full, pins at 22) | green: 17 patches applied, **117 tests passed** (109 + 8), `structured customizations installed: 629` (622 + 7), image `sl-modernuo:cc6b8-ac` (62b71d258d39). Committed as `339a9e9` |
| **Build C** (B in the tree, full, pins at 20) | **red, one fact, mine**: all five B files compiled first time; `TheDragonsFireColumn…` asserted a deserialized `FireField` deleted inline. It is not: `[AfterDeserialization(false)]` is the deferred form and the generator schedules it with `Timer.DelayCall` (read off the generator's template strings, `ModernUO.Serialization.Generator.dll` 2.14.3; the core's own hooks use the bare attribute for the synchronous form). 123/124 |
| **Build D** (same, the fact advancing the clock one second first) | **red, one fact, mine**: the fireball did no damage — the dragon's AI had run through the 40 s advance and dropped its combatant. 123/124 |
| **Build E** (B+D in the tree, pins at 19) | **red at compile**: `Medusa.cs` missing `using Server.Engines.BuffIcons;` (CS0246, CS0103 ×2). The only red compile of the batch |
| **Build F** | **red, two facts, mine**: `Blood` deletes itself after 5 s so the splatter count was gone after the 61 s advances; `Mobile.Kill` returns on a blessed mobile, so a petrified stone cannot be killed until released. 127/129 |
| **Build G** | **red, one fact, mine, and the batch's one finding about the content**: "exactly five stones" is wrong on both emulators — `Summon` refuses a stone whose `ControlSlots` would pass the master's `FollowersMax` of 5, deletes it, and Medusa still lists it until the next defrag (a `WailingBanshee` at (0,0,0) in the output). The fact now pins the slot arithmetic (§5). 128/129 |
| **Build H** (B+D, full) | green: **129 tests passed** (117 + 12), `structured customizations installed: 639` (629 + 5 + 5), image `sl-modernuo:cc6b8-bd` (2b7e91f8d29c). Committed as `1eccd67` (B) and `2db7789` (D) |
| **Build I** (probe in the tree) | green: 129 passed, installed 640, image `sl-modernuo:cc6b8-probe` (4ef794e7c12a) |
| Test `CC6Batch8Verification` (21 facts) | **A**: `BasePeerless : BaseCreature` concrete and `BaseSABoss : BasePeerless` abstract, each with its own generator attribute and `(Serial)` constructor, no `Altar` property, no `PeerlessAltar` type by name or alias, no `[SerializableField]` on either, no set-item member; `AllHelpersDead`, `Unprovokable`, `GiveMLSpecial` true, `DropPrimer == Core.TOL`, Medium speed; **a `BasePeerless` round-trips through `BufferWriter`/`BufferReader`** with name, hue, body, hits, strength, AI, location and map equal and `CurrentWave` back at 0; `PackResources(60)` stacks only the six ML resources and includes `Putrefaction`, `PackTalismans(3)` gives 0-2; 100 real kills drop only the 35 ML-special types and at least one `HumanFeyLeggings`. **C**: Navrey's values (body 735, sound 389, 30000-35000 hits, fame 24000, `DeadlyParasitic` immune, lethal hit poison, 0-3 Mysticism scrolls from the 16), the spawn spelling and its lower case resolve, `Navrey` does not, no alias, own attribute and constructor, a round trip keeps her values and loses `UsedPillars` (unserialized, as ServUO); `Tangle1`, `EyeOfNavrey`, `UntranslatedAncientTome`, `Putrefaction` values; 40 kills: a tome at least once, never an eye; `DistributeArtifact` to a player's pack and deletion with nobody; a `Spawner` at [1053,861,-32] fills with her. **B**: both bosses' values, the Slasher's `ParalyzingBlow`, provokable/bardable, sounds, Spellweaving and DetectHidden, the dragon's `FireBreath`, both weapon abilities seen in 60 draws, 30 barbed hides, 7 red scales, `CanFlee` false, `Tamable` false; all 26 listed artifact types construct; `LifeSyphon`/`VampiricEssence` values; each of `BasePeerless`, `BaseSABoss`, `SlasherOfVeils`, `StygianDragon` declares its own `Serialize`; **a Slasher round-trips through all three levels** (name, body, hue, hits and max, location, map, wave 0, `DropPrimer` false) and so does a dragon (breath intact); `RegisterDamage` + `AwardArtifact` puts the artifact in the damager's pack; 60 real dragon kills with a damager: the head on every corpse, at least one artifact bestowed, every artifact from its lists, paragon chests logged; the fire column lays 8 immovable fields (0x398C/0x3996) that are all gone after 40 s on the clock; a field round-tripped through the buffers is alive after `Deserialize` and deleted after one timer slice; the stygian fireball hurts the combatant within 4 s; the Slasher blinks to a caster in 1-39 of 40 spell hits; none of the three is slain by the six pinned entries; spawners at [749,475,-17] and [326,159,20] fill. **D**: Medusa's values, `ICarvable`, `MortalStrike`, bard-immune, auto-dispel 1.0, young-protection ignored, both hit poisons seen in 40 draws, the immovable bow, 100-200 arrows, 8-9 light scales (and `Scales` still 0), all 7 artifact types construct, Repond does not slay her, `medusa` resolves; the three resources and the gargoyle's values; **the live harvest**: 2-3 scales per carve (never past the stock), a blood splatter each time, the same carve refused inside the minute, the stock exhausted in 3-5 carves and the sum in the player's pack; 20 corpse carves: 1-5 dark scales every time, `Carved` set, blood logged; **the gaze**: the player found as the target, frozen, blessed, hue 761, listed as affected, a `MedusaClone` summoned with her body and name, frozen, blessed, hue 761, `SummonMaster` Medusa; 11 s: the player released; 11 more: the clone released and murderous; a clone round-tripped through the buffers deletes itself on the next slice; deleting Medusa deletes it; **the menagerie**: 7 `SpawnStone` calls leave 2-5 living stones whose `ControlSlots` sum is her `Followers` and at most her `FollowersMax`, all frozen, blessed, hue 761, summoned, of the six types; `ReleaseStoneMonster` unfreezes exactly one and drops it from the list; **a Medusa round-trips** with `LightScales` 5 and every living helper, a released-then-killed helper pruned on the next slice; a spawner at [818,927,-15] fills with her. **The count**: every stock entry naming the four resolves (4 entries), and exactly 19 names remain (the run lists them) |
| `CC6Batch1..5CreatureVerification`, `CC6Batch7Verification` | their pinned orphan count moved 23 → 22 → 20 → 19 in step; **all six went red on the old figure first** (build A, `Expected: 23 / Actual: 22`) |
| **Headless run 1** (`sl-modernuo:cc6b8-probe`, fresh save; the probe imports `Abyss.json` and `Underworld.json` 3 s after start, reports at 93 s) | `Loading world done (618 items, 90 mobiles)`; `Generated 22 / 44 spawners (0 failures)`; **66 spawners, 173 entries, 13 entries flagged `InvalidType`** — exactly the 12 remaining orphans those two files carry (`Barreraak`, `ElderDugan`, `FiddlingTobin`, `Garamon`, `genericguard` ×2, `Gretchen`, `IronBeetle`, `Jaacar`, `NevilleBrightwhistle`, `QuartermasterFlint`, `Vernix`, `Xenrr`); 702 mobiles, 2,638 items. **4 of 4 live, each owned by its stock spawner, placed by the real map**: Navrey at (1058,871,−25) off her [1053,861,−32] spawner, 31197 hits; the Slasher at (752,475,−17), 53628 hits; the Stygian Dragon at (322,160,0) off [326,159,20]; Medusa at (804,938,−10) off [818,927,−15]. `Saving world done`, `Shutting down`; no warning but the usual three |
| **Headless run 2**, reload run 1's save | `Loading world done (2644 items, 703 mobiles)`; "4 spawners naming this batch present from save"; **0 entries flagged**; **every one of the four per-type lines identical to run 1, byte for byte** (`diff` empty). Save, shutdown, clean |
| **FINAL build** (probe deleted) | green: **129 tests passed**, image `sl-modernuo:cc6b8` (50dfb709cd49), tagged `sl-modernuo:latest`. The builder stage was fully cached (its context equals build H's), so the patches step printed no count; build H's 639 is the figure |
| **Headless run 3**, the final image, fresh save | `Loading world done (617 items, 90 mobiles)`, listeners on 127.0.0.1:2593 and :12000, `Saving world done`, `Shutting down`; **no `[cc6b8]` line**, no warning but the usual three |

Probe (`server/customizations/Probe/CC6Batch8Probe.cs`, deleted before FINAL, never committed): batch 7's shape,
importing through the real `[GenerateSpawners` as a Developer `PlayerMobile` (the import calls `Respawn()` on every
spawner it makes, `ImportSpawnersCommand.cs:177`, which is why the bosses stand within 90 s despite their 5-10 min
delays). Harness in `%LOCALAPPDATA%\Temp\cc6b8\` (`run.sh`, `conf` copied from batch 7's, the ten build logs, three
run logs, `saves`, `saves-final`).

**Every build here tarred the working tree, which carries 34 costume files and two docker files modified by someone
else (line-ending-only diffs on the costumes, 90 lines on `docker/dashboard/config/services.yaml`), not committed and
not touched.** The committed state without them was not built separately; the difference is whitespace and a dashboard
config the image does not read.

**Not verified, per the standing rule, and batched for the client spot check:** the four bodies (735, 741, 826, 728)
and hue 761 on a petrified player and clone; the light flash and the meteor and fireball particles; whether a knife on
a living Medusa reaches `Carve` from a client (the test calls it directly; `BladedItemTarget.cs:34` is the route); the
paperdoll on a frozen clone; whether the live world's Abyss and Underworld spawners are populated (Q-048 says
`shared/**` was generated, not read; these two files are `post-uoml/**`).

## 7. What it cost

| what | time |
|---|---|
| orientation: both `AGENTS.md`, batch 7 whole, batch 4 §2 and §8, the recipe, the orphan script and list, the Q-052/055/056 entries, batch 7's test | ~25 min |
| pre-flight: the seven ServUO files (Medusa read in full), every `new X(`/`typeof`/member against pinned and ours, the five special abilities' bodies, both slayer lists, the generator's deferral mechanism, `Summon` in both trees | ~55 min |
| Part A + C files, the test's 8 facts, the harness | ~25 min |
| build A 20:34 (tests-only, red on the pins as intended, 3 min) and build B 20:37 (full, green, 6 min); the A+C commit | ~10 min |
| Part B files (written while build A ran), 7 facts, pins | ~20 min |
| builds C 20:44, D 20:49 (red on my facts, 5 min each) | ~12 min |
| Part D files (Medusa 745 lines, written while builds C-D ran), 5 facts, pins | ~30 min |
| builds E 20:55 (red at compile, 1 min), F 20:56 (red on two facts, 2.5 min), G 20:58 (red on one, 4.5 min), H 21:03 (green, 2 min); the B and D commits | ~12 min |
| build I 21:05 (probe, 1.5 min), runs 1 (21:07, 3.5 min), 2 (21:11, 3 min), FINAL 21:14 (cached, <1 min), run 3 (21:15, 2 min) | ~11 min |
| this note, the Q-052 record, Q-057, the orphan list and progress | ~40 min |

## 8. Questions

- **Q-052**: answered yes; recorded verbatim in `notes/codex-questions.md`, header flipped.
- **Q-056** (open, Chase's): followed provisionally for `NavreyNightEyes` (§4); not settled here.
- **Q-057** (new, non-blocking, Chase's): the seven Mondain's Legacy peerless bosses now have their final parent in
  the tree and no stock spawner names any of them; port as GM-placed walk-ups, or leave. Best guess: leave.
- **For `docs/patch-backlog.md` (Chase adds rows):** D-86 extends batch 7's slayer-membership row to 20 types and
  six lists; D-87 is one attribute of the SA weapon-attribute row S9 sized; D-88 (Gorgon Lens) is a new
  subsystem-sized row; D-81 and D-85 are one-hunk virtuals on `BaseCreature` that could share a row with the earlier
  "hooks" rows.
- **For `docs/bug-list.md`:** the `FireField` save fix (§5), and the `Summon` followers-cap parity worth knowing
  before anyone ports a boss that summons a 5-slot creature.

## 9. What is left, honestly — the 19, re-cut by closure

| what closes it | names | entries | members | cost, measured |
|---|---|---|---|---|
| **the quest/escort engine** (S5, Q-025) | 12 | 14 | `athialon`, `Barreraak`, `Garamon`, `Gretchen`, `Jaacar`, `QuartermasterFlint`, `Xenrr`, `Vernix`, `ElderDugan`, `FiddlingTobin`, `NevilleBrightwhistle`, `escortablewanderinghealer` | unchanged from batch 7 §9; five are Q-056's shape |
| **an ordinary port on batch 8's base** | 1 | 1 | `Niporailem` (`Mobiles/Normal/Niporailem.cs`, 220 lines, `: BaseSABoss`) | counted from the file: its unique list names **24** Epiphany pieces, the 12 Villainous (ours, CC9, `Sets/Epiphany/VillainousEpiphany.cs`) and the 12 Virtuous (**not ours**: no `Virtuous` in the tree); its shared four (`BladeOfBattle`, `DemonBridleRing`, `GiantSteps`, `SwordOfShatteredHopes`) are all ours — batch 4 §8 had the sword as missing and the unique count as 14, both wrong; `NiporailemsTreasure` (dropped on death) is not ours, `SpectralArmour` is stock. **Batch 9's first row**: ~220 lines + the Virtuous set + one treasure item, no subsystem |
| **High Seas** | 2 | 4 | `dockmaster` (236 lines), `boatpainter` (42) | a subsystem question, unchanged |
| **`Sphynx`** | 1 | 1 | `Services/Malas/Sphynx/` (572 lines) | a leaf with its own service; unchanged |
| **P6** | 1 | 1 | `IronBeetle` | unchanged |
| **nothing to map: a spawn-data finding** | 2 | 4 | `genericguard`, `bodysculptor` | in the upstream report's last section; nothing to build |

12 + 1 + 2 + 1 + 1 + 2 = 19; 14 + 1 + 4 + 1 + 1 + 4 = 25. Q-057's seven ML bosses are not on this list because no
stock spawner names them; they are content only if Chase wants GM-placed bosses.
