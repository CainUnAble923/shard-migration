# Patch backlog: what ModernUO is missing, and the patch that would close it

Every port that drops something records a **D-number** in its `notes/` file with a "reverses when"
column. That column is the workaround. This file is those columns gathered into one place and
ordered by leverage, so a thing we gave up is a scheduled patch rather than a loss.

**How a row gets here:** a port drops something because pinned ModernUO has no counterpart. The
note records the D-number. The D-number's "reverses when" names a patch. That patch lands here.
**Nothing is retired from this list by being forgotten** — a row leaves only as DONE or WON'T with
a reason.

**Two shapes, and the difference matters** (`AGENTS.md`, the layering pattern):

- **Additive** — a new file in `server/customizations`. No upstream file touched, no merge
  conflict on the next ModernUO bump. Cheap to own.
- **Patch** — a hunk in `server/patches` against a pinned upstream file. Every one is a thing that
  can break when upstream moves. `subsystem-policy.md` question 2 is about this, and S3's strongest
  decline (B12, Skill Masteries, 35 patch points) failed on it.

Ratio is deviations closed per patched upstream file. Sizes are **measured from the ServUO source**,
not estimated.

---

## Ranked

| # | Patch | Closes | Reach | Shape | Measured size | Status |
|---|---|---|---|---|---|---|
| **P1** | **The missing AI types.** ModernUO's `AIType` has 10 members (`Mobiles/AI/BaseAI/AIType.cs`); ServUO has nine more that creatures select. **Necromancy is not among them — see the correction below** | D-41, D-44, D-45 | **26 ServUO `Mobiles/Normal` files** | 1 patch (the enum) + N additive AI classes | 1,964 lines for the eight that are genuinely absent | unscheduled |
| **P2** | **Carve-yield hooks.** Two `BaseCreature` virtuals with no counterpart: `DragonBlood` and corpse-shear `Fur` | D-48, D-50 | 16 creatures (dragon's blood) + 5 (fur) | patch to the corpse-carve path + 2 virtuals | ~20 lines | **OPEN as Q-049** |
| **P3** | **The set-mechanic hooks row.** Eight additive patches that make ported set and artifact mechanics actually fire | D-5, D-14, D-21, D-24, D-27, D-28 | the CC9 artifact row, 123 set-bearing types | 8 patches | costed in the gap register | **AWAITING CHASE.** Q-038, Q-042, Q-043 |
| **P4** | **Attribute enum members and their hooks.** `AosArmorAttribute` has 4 members here against ServUO's larger set; `AosWeaponAttribute` likewise | D-3, D-21, D-22, D-49 | scattered artifacts | patch to `AOS.cs` (the file S6 already patches for B1) + a branch in `BaseWeapon.OnHit` | small per attribute | unscheduled |
| **P5** | **Carrier extensions.** `BaseSetRanged` and the quiver/talisman carriers | D-4, D-15, D-17, D-23 | completes the **Marksman set** (blocked on `Swiftflight`) | additive, the S10 family | S10 has the shape | **Q-041 open** |
| **P6** | **Pet Training, groups B2-B4** (`SpecialAbility`, `MagicalAbility`, `AreaEffect`). Not B5, which is the expensive half and buys almost nothing. **Its case is weaker than the raw file count suggests — see the two corrections below** | D-32, D-39, D-51 to D-54, D-57 (**not** D-55, D-56, D-62, D-68: those were wrong, Q-054) | 88 files nominally (53+18+17), but **34 of them want only `DragonBreath`, which pinned already has** | 6 patches + `AOS.Damage` | S3 measured it | **WAIT** since 2026-09-07 |
| **P7** | **`Services/PointsSystems`** | D-29, D-37 | 55 files; hard dependency of B9 and B13 | additive | 2,857 lines | **queued as S7** |
| **P9** | **`PeerlessKey` as an inert additive base.** 184 lines, `: Item`, its only external reference a `Timer`. No consumer, no patch. Porting it gives `ShatteredCrystals` and `DraconicOrb` their **final parent once**, which is the whole point — B14 Instanced Peerless stays WON'T | unblocks `CrystalHydra` and `FairyDragon` | 2 orphan names, 3 spawn entries | additive, 1 file | 184 lines, measured | **APPROVED (Q-051).** Take it in batch 4 |
| **P10** | **`IRepairableMobile`** (`Mobiles/MobileInterfaces.cs`, 3 members) plus the branch in `Engines/Craft/Core/Repair.cs:169`, which today special-cases `targeted is Golem` | D-64 | tinker-repairable constructs; `ClockworkScorpion` today, more later | 6-line additive interface **+ 1 patch** | 6 lines + a small hunk | unscheduled |
| **P11** | **`MeatType.Rotworm` and `RawRotwormMeat`.** ModernUO's enum is `Ribs`/`Bird`/`LambLeg` (`BaseCreature.cs:106`) | D-59 | cooking content; 1 creature today | 1 enum member **+ 1 patch** + 1 item | small | unscheduled, low value |
| **P12** | **`Incubator`** (ServUO `Items/Functional/Incubator.cs`, 158 lines) plus two one-line hunks, in `DefCarpentry.cs` and `Beverage.Pour_OnTarget` | D-69, D-70 | **makes `ChickenLizard` reachable at all** — 8 spawn entries, and `BattleChickenLizard` has no other source | 158 additive + 2 tiny patches | **APPROVED (Q-053).** Take it next |
| **P13** | **An `OnAfterTame(Mobile)` virtual** on `BaseCreature`, called from `AnimalTaming.cs:444` where it today calls the non-virtual `SetControlMaster` | D-71 | any tamed creature with post-tame state to settle; 1 today | 1 virtual + 1 small hunk | unscheduled, low value |
| **P14** | **`ParrotItem`** (ServUO `Items/Addons/Parrot.cs`, 112 lines, needs `PetParrot`, 199) plus un-commenting pinned `LootPack.cs:515-523`, which already carries the 10% pack inside a `/* TODO */` block | D-72 | 1 creature today | 311 additive + 1 hunk | unscheduled |
| **P8** | **Three standalone one-liners.** `WispOrb.CheckDrop` in `Container.DropToWorld` (D-31); a `ForceNotoriety` virtual plus two guards in `Notoriety.cs` (D-33); a `TreasureMapChance` virtual (D-42) | D-31, D-33, D-42 | 1 item, possessed creatures, 1 creature | 3 tiny patches | 1 to 5 lines each | D-42 **judged not worth a patch**; the other two unscheduled |

---

## P1 in detail, and the correction that shrank it

**Read this first: on 2026-09-20 the top of this row turned out not to exist.** It was written on
2026-09-19 claiming `AI_NecroMage` as the best slice on the board, 189 lines for 20 creatures,
sourced from CC6 batch 2's D-47. Checking pinned ModernUO's own `MageAI` instead of the note
shows **Necromancy is already built into it**: `IsNecromancer`, `UseNecromancy()`,
`GetRandomDamageSpellNecro()` and `GetRandomCurseSpellNecro()` (`Mobiles/AI/MageAI.cs:68-325`).

The spell sets are the same ones ServUO's `NecroMageAI` casts. Damage: Pain Spike, Poison Strike,
Strangle, Wither, four of four, plus Vengeful Spirit at Necromancy 100+. Curse: Corpse Skin, Evil
Omen, Blood Oath, Mind Rot, **four of four**. The mix differs only in how it is gated — ServUO
rolls a flat 50% and then gates the pick on current mana; ModernUO weights by skill,
`Random(magery + necro) >= magery`. For `SkeletalLich` at Magery 127.2 and Necromancy 100-120 that
is **about 44 to 48 percent Necromancy casts against ServUO's 50**.

So D-47's claim that the lich's "100-120 Necromancy is set and unused" is wrong, and the row it
justified is withdrawn. What is genuinely missing is small: `CurseWeapon` in the buff rotation, the
summon path, and mana-gating instead of skill-gating. Not a patch worth scheduling. See Q-050.

**The general lesson, which is the one that keeps costing this project:** a note saying ModernUO
lacks something is not evidence that it does. Check the pinned tree. This was caught before any
work was scheduled against it; the same claim also told CC6 batch 3 that `MaddeningHorror` needs an
AI port, and it does not.

## The eight that are genuinely absent

Measured from `D:\UO\ServUO-pub57\Scripts\Mobiles`. "Normal" is files in `Mobiles/Normal` that select
that AI; "all" includes `Named`, `Bosses` and the rest.

| ServUO AI | file | lines | Normal | all | Our deviation |
|---|---|---|---|---|---|
| ~~`AI_NecroMage`~~ | ~~`Magical AI/NecromageAI.cs`~~ | ~~189~~ | ~~20~~ | — | **WITHDRAWN.** Stock `MageAI` already casts Necromancy; D-47 is wrong (Q-050) |
| `AI_Mystic` | `Magical AI/MysticAI.cs` | **171** | 8 | 12 | **D-41** (`CrazedMage`, Shame) |
| `AI_Spellweaving` | `Magical AI/SpellweavingAI.cs` | **125** | 7 | 12 | none yet; will appear |
| `AI_OrcScout` | `OrcScoutAI.cs` | 329 | 3 | 4 | **D-44** (`GreenGoblinScout`, and `OrcScout` in batch 3) |
| `AI_Ninja` | `Magical AI/NinjaAI.cs` | 201 | 2 | 4 | none yet |
| `AI_Samurai` | `Magical AI/SamuraiAI.cs` | 128 | 2 | 4 | none yet |
| `AI_Necro` | `Magical AI/NecroAI.cs` | 106 | 2 | 4 | none yet |
| `AI_Paladin` | `Magical AI/PaladinAI.cs` | 85 | 2 | 4 | none yet |
| `AI_Spellbinder` | `Magical AI/SpellbinderAI.cs` | **819** | 2 | 3 | **D-45** (`Spellbinder`). Worst ratio here: the largest file for the smallest reach |

**The slice to buy first is now `AI_Mystic`: 171 lines for 8 creatures**, and it closes D-41, the
Shame `CrazedMage` that runs Magery in place of Mysticism. `AI_Spellweaving` is next at 125 lines
for 7, and closes nothing yet but will.

**The enum is the only upstream patch**, and it is additive in the safest sense: appending members
to `AIType` changes no existing member's value, so nothing in a save shifts. Every AI class beside
it is a new file. That is a 1-patch, N-file shape, which is the same shape as S1's armour sets, the
best-value thing this project has built.

**Order by ratio, not by appetite:** Mystic (8 creatures / 171 lines), Spellweaving (7 / 125),
OrcScout (3 / 329). Stop there. Ninja, Samurai, Necro and Paladin are two
creatures each and can wait for a batch that needs them. **Spellbinder is a decline** at 819 lines
for two creatures unless one of them turns out to matter.

---

## Two corrections that shrank P6, and the lesson under them

**On 2026-09-20 four D-numbers were retired as wrong** (Q-054). D-55 (`Slith`), D-56 (`ToxicSlith`),
D-62 (`FireDaemon`) and D-68 (`CrystalHydra`) each recorded `SetSpecialAbility(DragonBreath)` as a
Pet Training loss. **Pinned ModernUO has the ability**, as `MonsterAbilities.FireBreath` from
`BaseCreature.GetMonsterAbilities()` (`:1131`), with `Mobiles/Abilities/Fire Breath/FireBreath.cs`
carrying ServUO's fire numbers line for line and `ColdBreath : FireBreath` overriding
`ColdDamage => 100`, `FireDamage => 0`, `BreathEffectHue => 0x480`. CC4 had already used it. Those
four creatures should have shipped breathing, and **34 of the ServUO `Mobiles/Normal` files counted
into P6's 88 want only this**, so P6's real reach is materially smaller than the row's file count.

Earlier, batch 3 found the same shape three times in one task: `SetAreaEffect(AuraDamage)` is
pinned's `HasAura`/`AuraDamage()`, `HealChance` is `CanHeal` with the same 0.78 trigger, and a
`SetMagicalAbility(Poisoning)` that only ever ran inside a `Deserialize` version branch was never
live content at all.

**The lesson, since it has now cost this project five wrong D-numbers and one withdrawn patch row
(the `AI_NecroMage` withdrawal, Q-050):** ServUO calling something `X` and pinned ModernUO having no
`X` is evidence about the *name*, not about the *capability*. Before a D-number claims a loss, grep
pinned for what the thing **does** — the effect, the damage type, the trigger — not for what ServUO
calls it. `AGENTS.md` now asks for this explicitly.

## The `[TypeAlias]` trap, found in batch 5

**A name absent from pinned ModernUO may still resolve.** `AssemblyHandler` registers every
`[TypeAlias]` string in the same lookup as real type names (`AssemblyHandler.cs:251-263`), so
`FindTypeByName("GargishClothChest")` returns stock `GargishClothChestType1` even though no type is
declared under that name. Porting the ServUO type would have put **two types under one name**.

So a "missing" type needs the alias check as well as the name check, and this applies directly to
the gargish cloth family: pinned models ServUO's gargish cloth *clothing* and cloth *armour* as one
stock armour type per slot and gender. **Any later port deriving from `GargishClothArms/Chest/Kilt/
Legs` goes straight onto a carrier with the ServUO parent's members inlined**, never onto a ported
clothing base. This also retires CC9 §2b's listing of `GargishClothKilt` as an extract still to do.

## The partial-class trick, found in batch 3 and worth reusing

Adding a **marker interface to a stock ModernUO type needs no patch at all.** Every stock creature is
declared `partial` because the serialization generator requires it, so
`public partial class AcidElemental : IAcidCreature { }` in a new file under a non-colliding path
does the whole job additively. Batch 3 used this to plan `IAcidCreature` and `IBloodCreature` onto
stock `AcidElemental` and `BloodElemental` when the `Vernix` and `ATangledWeb` quests are ported.

This applies to any interface whose members the stock type already satisfies. It does **not** apply
when the interface needs a member the stock type lacks, and it is not a way around re-parenting: a
base class is still a base class.

## Not coming back, and why

Recorded so nobody re-opens them.

| D | What | Why it stays |
|---|---|---|
| D-2 | `CanBeWornByGargoyles` dropped | the race gate is kept through `RequiredRaces`; the flag has no other consumer |
| D-10 | `GargishWarHammer` flips to `0x48C1` | ServUO's value is the bug; ours is correct |
| D-34 | `SmartSpawning` has no counterpart | nothing to build, a note only |
| D-35 | Despise lower-level power rolls 4-8 | ServUO's XML read literally constructs nothing; two numbers, already chosen |
| D-43 | A timed-out Shame challenge clears the altar | ServUO leaves the altar permanently locked; ours is the better behavior |
| D-46 | `ShameWall` is visible on construction | ServUO's literal value is the bug (Q-046) |

---

## Keeping this file honest

- A new D-number with a "reverses when" that names a patch **belongs in the table above** the same
  day it is written. If it fits an existing row, add the D-number to that row's Closes column and
  update the reach.
- **Reach is what ranks a row**, and reach grows as batches land. P1 gained `MaddeningHorror` the
  moment batch 2's §9 named it. Re-read the reach column before scheduling, not once.
- Sizes are measured from the source. If a row carries an estimate, mark it as one.
- Agents may not edit `docs/`. A port that discovers a new patch candidate writes it in its
  `notes/` file with the D-number and the reverses-when, and it is promoted here in review.
