# Port recipe: ServUO to ModernUO

**Status: VALIDATED against a real build and a running client, 2026-09-06 (backlog P1 / CC1),
then re-exercised headlessly on a second creature (CC2).** The draft that preceded this was
written from source study. Both of its "fidelity traps" were wrong — one exactly backwards — and
are corrected below. Evidence and method are in `notes/cc1-p1-runtime-validation.md` and
`notes/cc2-timed-port.md`.

Reference ports, both to `server/customizations/<ServUO-relative-path>/`, both built in Docker
from pinned ModernUO `7c9215d97`:

- **`PlagueRat.cs`**, 88 lines to 55. Spawned with `[add PlagueRat`, inspected with
  `[global get`, saved, restarted, reloaded intact. (CC1, with a client.)
- **`GreaterPoisonElemental.cs`**, 123 lines to 80, plus `LuckyCoin.cs` as a forced dependency
  port. Built, started, world saved and reloaded, type registration proven by reflection. (CC2,
  headless.) Adds coverage of `PackItem`, multi-`AddLoot`, an `OnDeath` override, `AI_Mage` and
  the two-argument stat overloads.
- **CC3, 17 files in four batches, zero failed builds.** Six Eodon dinosaurs, `Raptor`,
  `RaptorClaw`, `RaptorTeeth`, six TOL decorations and two forced leaf dependencies. Adds coverage
  of `[SerializableField]` + `[AfterDeserialization]` (`Raptor`), `GetWeaponAbility`, an inner
  `Timer`, `Item` ports, and the collapsed optional-parameter `[Constructible]`. Corrections and
  new absent-member tables are below; timings and declines in `notes/cc3-eodon.md`.

**Before you transform anything, read "Check dependencies first" below.** It is the step whose
absence cost CC2 a whole build cycle, and it is the cheapest thing in this document.

The headline still holds: for simple content, porting is mostly **deleting boilerplate**.
ModernUO's source generator writes the serialization ServUO writes by hand.

## Check dependencies first

**Added by CC2, which learned this the expensive way.** The mechanical transformation is easy.
The thing that actually fails a build is a type the ServUO file references and ModernUO does not
have. `GreaterPoisonElemental` drops a `LuckyCoin`; ModernUO has no `LuckyCoin`; that cost a full
build cycle to discover and a decision to resolve.

### The pinned ModernUO source is on this machine, inside the Docker builder image

There is **no ModernUO source tree on disk**. `AGENTS.md` says `server/uo/modernuo/` holds "a full
ModernUO checkout" — it does not; it holds `Configuration/` and `Projects/UOContent/Misc/`, 161
`.cs` files, all of them ours. But the *builder stage* of the Docker image clones ModernUO at the
pinned commit and keeps it at `/build/modernuo`, and that image is still on disk:

```bash
docker run --rm --entrypoint sh sl-uo-buildertest:latest -c 'grep -rn "class FountainOfFortune" /build/modernuo/Projects'
```

Use it to answer, in seconds and with no build cycle:

- does this type exist at all
- what shape is this interface (`ICommodity` differs between the emulators — see below)
- does `BaseCreature` really have this virtual
- what are the `LootPack` member names
- what constructor overloads does this item have

Dump the whole type universe once per session and grep it locally:

```bash
docker run --rm --entrypoint sh sl-uo-buildertest:latest \
  -c 'grep -rhoE "\b(class|struct|enum|interface|record)[[:space:]]+[A-Za-z_][A-Za-z0-9_]*" /build/modernuo/Projects/Server /build/modernuo/Projects/UOContent --include=*.cs | awk "{print \$2}" | sort -u' \
  > mu-types.txt
```

That is 7,058 types at `7c9215d97`. Check every `new X(` in the ServUO file against it, plus the
115 stems under `server/customizations`.

### `tools/modernuo-stems.txt` is NOT a dependency checker

It is a list of **filename stems**. It is correct for its one stated job — collision-checking the
ported type's own name — and wrong for anything else. It reports `ICommodity`, `TextDefinition`,
`Ribs`, `ThighBoots` and `IronOre` as absent when all five exist, because they are defined inside
files named something else. Do not reuse it for dependency checking; use `mu-types.txt` above.

### How often this bites, measured across all 462 `Mobiles/Normal` files

| | files | share |
|---|---|---|
| Reference at least one type ModernUO lacks | 89 | **19%** |
| Call `SetWeaponAbility` / `SetSpecialAbility` / `SetMagicalAbility` / `PetTrainingHelper` | 132 | **29%** |
| **Clean on both checks** | **275** | **60%** |

**Screen a batch against both lists before starting it.** The 29% group is a design decision, not
a port. Full method and the missing-type frequency table are in `notes/cc2-timed-port.md`.

### When the missing type is a leaf item, port it too — unless it drags in a subsystem

`LuckyCoin` is a 60-line stackable item, so it was ported alongside the creature to
`server/customizations/Items/Quest/LuckyCoin.cs`, mirroring its ServUO path even though ServUO
keeps it inside the multi-type `SAQuestItems.cs`. **One extracted type per file.**

Its `OnDoubleClick` throws the coin into a `FountainOfFortune`, an SA addon ModernUO lacks whose
own port pulls in `EnchantedEssence`, `GemologistsSatchel`, `RelicFragment` and
`SolesOfProvidence`. That is a subsystem, so it was declined and the coin ported without the
interaction. **The deviation is in the item, not the creature** — the creature's loot table stays
faithful, which is what a player checks against UOGuide. Recorded as Q-010. Twelve
`Mobiles/Normal` creatures drop `LuckyCoin`, so this decision is reused, not re-litigated.

## The mechanical transformation

All of these were exercised and compile.

| ServUO | ModernUO |
|---|---|
| `using System;` | `using ModernUO.Serialization;` |
| `public class X : BaseCreature` | `[SerializationGenerator(0, false)]`<br>`public partial class X : BaseCreature` |
| `[Constructable]` | `[Constructible]` |
| `[CorpseName("a plague rat corpse")]` on the class | `public override string CorpseName => "a plague rat corpse";` |
| `Name = "a plague rat";` in the constructor | `public override string DefaultName => "a plague rat";` |
| `public X(Serial serial) : base(serial) { }` | **delete it** — the generator provides it |
| `public override void Serialize(GenericWriter w)`<br>`public override void Deserialize(GenericReader r)` | **delete both** — the generator provides them |
| `public override int Meat { get { return 1; } }` | `public override int Meat => 1;` |
| `this.SetStr(59);` etc. | drop the `this.` — ServUO's content is full of it |

`partial` is required. The first argument to `SerializationGenerator` is the version; use `0`
for new content with no existing saves. **The meaning of the second argument was not verified** —
all 2921 in-tree usages pass `false`, and the attribute itself lives in the `ModernUO.Serialization`
NuGet package rather than the source tree. Copy `false` and move on.

## Enum and API renames that bite

Compiler errors, not silent, but they cost a build cycle each:

- **`FoodType.FruitsAndVegies` (ServUO) → `FoodType.FruitsAndVeggies` (ModernUO).** Two g's.
- **`SetWeaponAbility(...)` / `SetSpecialAbility(...)` do not exist on ModernUO's `BaseCreature`.**
  Any ServUO creature that calls them needs a decision, not a translation. PlagueRat was chosen
  partly because it calls neither. A large share of `Mobiles/Normal` does — check before
  committing to a batch.

  **CORRECTED BY CC3: this is right about three of the four methods and wrong about the fourth.**
  ServUO has four, all routing into `PetTrainingHelper.GetAbilityProfile(...).AddAbility(...)`
  (`ServUO Scripts/Mobiles/Normal/BaseCreature.cs:635-651`). Only three of them are blocked.

  **`SetWeaponAbility` translates faithfully.** ModernUO's `BaseCreature` has
  `public virtual WeaponAbility GetWeaponAbility() => null;` (`BaseCreature.cs:1312`) plus
  `WeaponAbilityChance => 0.4` (`:439`), and **49 stock creatures override it** — including the
  multi-ability form that matches several ServUO `SetWeaponAbility` calls:

  ```csharp
  // ServUO                                        // ModernUO
  SetWeaponAbility(WeaponAbility.MortalStrike);     public override WeaponAbility GetWeaponAbility() =>
  SetWeaponAbility(WeaponAbility.Dismount);             Utility.RandomBool()
                                                            ? WeaponAbility.MortalStrike
                                                            : WeaponAbility.Dismount;
  ```

  For three or more, use a `Utility.Random(n)` switch — the shape stock `DemonKnight.cs:202` uses.
  Every `WeaponAbility` name CC3 needed exists in ModernUO unchanged: `ArmorPierce`,
  `CrushingBlow`, `Disarm`, `BleedAttack`, `TalonStrike`, `MortalStrike`, `Dismount`,
  `ConcussionBlow`.

  **`SetSpecialAbility`, `SetMagicalAbility` and `SetAreaEffect` stay blocked.** `SpecialAbility`,
  `MagicalAbility` and `AreaEffect` have zero definitions in the pinned tree. These are a
  decision, not a translation.

  **So the "132 files / 29% Pet Training cohort" figure is not a decline rate.** CC3 hit it on
  6 of 7 candidate creatures and ported 6 of 7 anyway, because `SetWeaponAbility` was the only
  one of the four most of them called. Split the 132 by method before sizing a CC6 batch off it.
  Raised as Q-013.

  One more trap CC3 met twice: a `Set*Ability` call can sit inside the **`Deserialize` version
  upgrade path** rather than the constructor (`Najasaurus`, `Dimetrosaur`). New content starts at
  version 0 and never runs it, so those are no-ops — read where the call is before treating the
  file as blocked.
- **`ICommodity` has different members in the two emulators.** ServUO:
  `TextDefinition Description { get; }` + `bool IsDeedable { get; }`. ModernUO:
  `int DescriptionNumber { get; }` + `bool IsDeedable { get; }`. Written as explicit-interface
  expression members, matching stock `Items/Resources/Arrows/Shaft.cs`:

  ```csharp
  int ICommodity.DescriptionNumber => LabelNumber;
  bool ICommodity.IsDeedable => true;
  ```

- **ModernUO collapses `[Constructable]` overload pairs into one optional parameter.** ServUO's
  `public X()` + `public X(int amount)` pair becomes a single
  `[Constructible] public X(int amount = 1)`. One attribute, not two. Stock ModernUO does this
  everywhere; `Shaft.cs` is the canonical shape.

- `MinTameSkill`, `Fame`, `Karma`, `VirtualArmor`, `BaseSoundID`, `Hides`, `Meat`,
  `FavoriteFood`, `LootPack.Rich`, `AddLoot`, and the single- and two-argument
  `SetStr/SetDex/SetInt/SetHits/SetMana` overloads all exist unchanged.

**Confirmed unchanged by CC2, so port them literally** (all checked against
`Projects/UOContent/Mobiles/BaseCreature.cs` at the pinned commit and then compiled):
`OnDeath(Container c)`, `BleedImmune`, `PoisonImmune`, `HitPoison`, `HitPoisonChance`,
`TreasureMapLevel`, `SetStam`, `PackItem`, `SetDamageType`, `SetResistance`, and
`SkillName.Poisoning` / `.EvalInt` / `.Meditation` / `.DetectHidden`. Several `AddLoot` calls in
one `GenerateLoot` is fine, and `LootPack.FilthyRich` and `LootPack.MedScrolls` both exist
(`Rich`, `FilthyRich`, `Poor`, `Meager`, `Average` are expansion-switching properties over the
`Se*`/`Aos*` tables, so they resolve to the right era automatically).

## Two fidelity traps — both of the draft's claims were wrong

### 1. Range perception: do NOT carry the ServUO value across

The draft said ServUO passes `10`, ModernUO defaults to `16`, so you must pass `10` explicitly
or you silently widen perception. **That is backwards.**

ServUO's `BaseCreature` constructor rewrites the value on the way in
(`ServUO-pub57/Scripts/Mobiles/Normal/BaseCreature.cs:2353-2377`):

```csharp
public const int DefaultRangePerception = 16;   // :2353
public const int OldRangePerception     = 10;   // :2354
...
if (iRangePerception == OldRangePerception)
{
    iRangePerception = DefaultRangePerception;   // 10 becomes 16
}
```

So a ServUO creature that passes `10` **runs at 16**, which is exactly ModernUO's
`DefaultRangePerception` (`BaseCreature.cs:161`). The two emulators already agree.

**476 of ~493** constructor calls under ServUO `Scripts/Mobiles` pass `10`. For all of them the
faithful port is to **drop the argument** and take ModernUO's default. Passing `10` through
literally — what the draft demanded — would have narrowed perception from 16 to 10 on nearly the
entire roster.

```csharp
// ServUO
base(AIType.AI_Melee, FightMode.Closest, 10, 1, 0.2, 0.4)   // runs at 16

// RIGHT
base(AIType.AI_Melee)                                        // 16; FightMode.Closest and
                                                             // iRangeFight 1 are the defaults too

// WRONG - silently narrows perception from 16 to 10
base(AIType.AI_Melee, FightMode.Closest, 10, 1)
```

**Carry the value across only when ServUO passes something other than 10.** The exceptions are
rare: 15 (x9), 22 (x2), 18 (x2), 14 (x1), 2 (x2), 1 (x1). Note `2` and `1` are below
`OldRangePerception`, so they pass through untouched and must be preserved.

Measured on the ported PlagueRat with the argument dropped: `RangePerception : 16 [0x10]`.

### 2. Speeds: ServUO ignores the two constructor arguments too

The draft framed this as "ModernUO derives them, so drop them and prefer the derived values."
Dropping them is right, but the reason matters, because the derived values are **not** what
ServUO runs.

ServUO's constructor immediately overwrites both arguments
(`Scripts/Mobiles/Normal/BaseCreature.cs:2388`):

```csharp
SpeedInfo.GetSpeeds(this, ref dActiveSpeed, ref dPassiveSpeed);
```

and `SpeedInfo.UseNewSpeeds` is hardcoded `true` (`Scripts/Mobiles/AI/SpeedInfo.cs:74`), so it
always routes to `GetSpeedsNew`, which derives speed **from Dex**:

```
maxDex   = IsMonster ? 150 : 190
dex      = clamp(bc.Dex, 25, maxDex)
min, max = IsMonster ? (0.4, 0.8) : (0.1, 0.5)
active   = max - (max - min) * (dex / maxDex)
passive  = active * 2
```

It is recomputed again once the derived constructor runs `SetDex`, via
`OnRawDexChange -> AdjustSpeeds` (`:5310-5327`, gated on `Core.ML`, which this shard has on).

**The two speed literals in ServUO source are dead parameters.** 437 of ~490 creatures pass
`0.2, 0.4`; none of them runs at `0.2, 0.4`.

ModernUO instead uses a type table, `Data/npc-speeds.json`, keyed by `SpeedClass` then by type,
falling back to `SpeedLevel.Medium` for anything unlisted (`NPCSpeeds.cs:31-38`). A ported type is
by definition unlisted, so **every port silently lands on Medium = 0.25 / 0.5** unless you say
otherwise.

Measured on the ported PlagueRat: `ActiveSpeed : 0.25`, `PassiveSpeed : 0.5` — the Medium
fallback. ServUO would have run the same creature (Dex 51, `IsMonster` true, so maxDex 150 and
min/max 0.4/0.8) at `0.8 - 0.4 * (51/150) = 0.664` active, `1.328` passive. Slower than ModernUO's
Medium, not faster.

The lever in ModernUO is **`SpeedClass`, not `GetSpeeds`**:

```csharp
public override SpeedLevel SpeedClass => SpeedLevel.Fast;   // 0.2 / 0.4
```

The table's levels are VerySlow 0.4/0.8, Slow 0.3/0.6, Medium 0.25/0.5, Fast 0.2/0.4,
VeryFast 0.125/0.3. Overriding `GetSpeeds` with raw doubles works but takes the creature out of
the data-driven table for no benefit; prefer `SpeedClass`.

**ANSWERED — Q-008 is closed. Do nothing; accept ModernUO's `Medium` fallback.** This is a
standing rule for all ~490 ported creatures and does not need re-asking per file.
**Do not add a `SpeedClass` override to match a ServUO constructor literal** — that option is
ruled out permanently, because it matches neither emulator while looking faithful in a diff. A
per-creature `GetSpeeds` override stays available on documented evidence (UOGuide/Stratics says
the creature's speed is distinctive *and* `Medium` visibly contradicts it), logged in
`docs/fidelity-principle.md` as a deliberate deviation. A hunch that something feels slow is not
evidence. `GreaterPoisonElemental` was ported with no override, per this rule.

The reasoning, kept because it explains why the answer is not "match ServUO". Three targets were
on the table:

- **ModernUO Medium (do nothing).** Consistent with ModernUO's own roster; a ported creature
  moves like its nearest stock peer. PlagueRat is a re-hued `GiantRat`, and stock `GiantRat` is
  Medium — so for this one file, doing nothing is arguably the *most* faithful choice.
- **`SpeedLevel.Fast` (0.2/0.4).** Matches the ServUO constructor literal, which is what a reader
  of ServUO source would expect — but not what ServUO runs.
- **Dex-derived per creature.** Matches ServUO's actual runtime, requires a `GetSpeeds` override
  per creature and abandons ModernUO's table.

`PlagueRat` and `GreaterPoisonElemental` were both ported with no override, which is now the
rule rather than an assumption in force.

## Where a ported file goes

Answered by building it. **`server/customizations/<ServUO-relative-path>/<File>.cs`.**
`apply-patches.sh` needs **no change** for additive content.

- Anything in a **subdirectory** of `server/customizations/` is mirrored to
  `Projects/UOContent/<same relative path>`, creating directories as needed. PlagueRat went to
  `server/customizations/Mobiles/Normal/PlagueRat.cs` ->
  `Projects/UOContent/Mobiles/Normal/PlagueRat.cs`.
  Build log: `[patches] Structured customizations installed: 1 file(s).`
- Anything at the **top level** of `server/customizations/` is flattened into
  `Projects/UOContent/Misc/`. That still compiles, but do not use it for ported content — it
  throws away the origin path and reintroduces the basename collisions that
  `docs/flat-namespace-problem.md` describes.
- The mirror **fails the build** if the destination already exists upstream. That is the name
  collision check doing its job; a collision means the file is a routed replacement, not an
  addition.
- Mirroring ServUO's own layout (`Mobiles/Normal/`) rather than ModernUO's
  (`Mobiles/Animals/Rodents/`) keeps "where did this come from" answerable during a 360-file
  batch. That is a judgement call, applied consistently from here.

**This port was the first thing ever to use the structured path** — the count went from 0 to 1.
It works.

## Serialization migration JSONs: not needed

Answered by building, saving and restarting.

- No `Server.Mobiles.PlagueRat.v0.json` was generated anywhere in the build tree, and the build
  succeeded. `UOContent.csproj:56` consumes `Migrations/*.v*.json` as `AdditionalFiles` — they are
  **inputs** to the generator, not outputs of a normal build.
- The world was saved with two PlagueRats in it, the container was restarted, and the world
  reloaded clean (`Loading world done (634 items, 94 mobiles)`, no errors). Both rats came back
  with identical `Name`, `RangePerception`, `ActiveSpeed`, `PassiveSpeed`, `Hue` and `Body`.
- For context: stock ModernUO *does* commit a `.v0.json` for every serialized type
  (`Server.Mobiles.GiantRat.v0.json` and 567 other `Server.Mobiles.*` files exist). Ours does not
  have one and it makes no difference at version 0. It would start to matter the first time a
  ported type's version is bumped — at that point generate the migration properly rather than
  hand-writing it.

## Also watch for

Carried over from the draft and **still unverified after two ports.** Neither `PlagueRat` nor
`GreaterPoisonElemental` has persisted state, `Serial` arithmetic or string building. These three
are the recipe's remaining blind corners, and any one of them could dominate the cost of a batch:

- **`Serial` is signed in ServUO, `uint` in ModernUO.** Any arithmetic or comparison against
  `-1` needs checking rather than find-and-replace.
- **`[SerializableField(n)]`** replaces hand-written field writes when a type has real persisted
  state. Simple creatures with no extra state need none — neither reference port needed one.
  **CC3 exercised it.** `Raptor` has one persisted `bool`, and the shape that compiled and
  generated correctly is stock ModernUO's (`Mobiles/Monsters/Ants/BlackSolenQueen.cs:9`):

  ```csharp
  [SerializableField(0, setter: "private")]
  private bool _isFriend;              // generator emits the public IsFriend property

  // ServUO's "if (m_IsFriend) Delete();" at the end of Deserialize becomes:
  [AfterDeserialization(false)]
  private void AfterDeserialization() { if (_isFriend) Delete(); }
  ```

  The field must be `_camelCase`. Reflection over the built assembly confirmed the generator
  emitted `Serialize`/`Deserialize` and both constructors. An *instance* round-trip is still
  unverified — that needs a client.
- **`TextDefinition`, `PooledRefQueue`, `ValueStringBuilder`** are ModernUO idioms with no ServUO
  equivalent. CC2 met `TextDefinition` only indirectly, via `ICommodity` (see above), where
  ModernUO uses a plain `int` instead.

Also still unverified: **the second argument to `[SerializationGenerator(0, false)]`.** The
attribute lives in the `ModernUO.Serialization` NuGet package, not the source tree, and all 2,921
in-tree usages pass `false`. Copy `false` and move on.

**Name collisions** are verified: check the stem against `tools/modernuo-stems.txt` before
porting. `PlagueRat` and `GreaterPoisonElemental` are both absent from it — note stock
`PoisonElemental` *is* present, and the "Greater" variant is an addition, not a collision — and
the structured mirror's overwrite check independently confirmed no collision at build time.
**That is the only thing the stems file is good for; see "Check dependencies first".**

## Worked example

`PlagueRat.cs`, ServUO 88 lines to ModernUO 55.

```csharp
using ModernUO.Serialization;

namespace Server.Mobiles
{
    [SerializationGenerator(0, false)]
    public partial class PlagueRat : BaseCreature
    {
        [Constructible]
        public PlagueRat() : base(AIType.AI_Melee)
        {
            Body = 0xD7;
            Hue = 1710;
            BaseSoundID = 0x188;

            SetStr(59);
            SetDex(51);
            SetInt(17);
            SetHits(92);
            SetMana(0);
            SetDamage(4, 8);
            SetDamageType(ResistanceType.Physical, 100);
            SetResistance(ResistanceType.Physical, 35, 40);
            SetResistance(ResistanceType.Fire, 20, 25);
            SetResistance(ResistanceType.Cold, 25, 35);
            SetResistance(ResistanceType.Energy, 35, 40);
            SetSkill(SkillName.MagicResist, 25.1, 30.0);
            SetSkill(SkillName.Tactics, 34.5, 40.0);
            SetSkill(SkillName.Wrestling, 40.5, 45.0);

            Fame = 300;
            Karma = -300;
            VirtualArmor = 38;
        }

        public override string CorpseName => "a plague rat corpse";
        public override string DefaultName => "a Clan Ribbon Plague Rat";

        public override int Meat => 1;
        public override int Hides => 6;

        public override FoodType FavoriteFood =>
            FoodType.Fish | FoodType.Meat | FoodType.FruitsAndVeggies | FoodType.Eggs;

        public override void GenerateLoot()
        {
            AddLoot(LootPack.Rich);
        }
    }
}
```

Everything removed was boilerplate: the `Serial` constructor, both serialization overrides, and
the property bodies. The only genuine content moves are `CorpseName` and `DefaultName`, from an
attribute and a constructor assignment to overrides. The only behavioural decisions are the two
dropped argument groups, both covered above.

`DefaultName` is `"a Clan Ribbon Plague Rat"` because that is what ServUO's `PlagueRat` sets, odd
as it reads next to `[CorpseName("a plague rat corpse")]`. Ported unchanged per the fidelity
principle. In-game the creature announces itself as `a Clan Ribbon Plague Rat`.

### Second example, the parts PlagueRat did not cover

From `GreaterPoisonElemental.cs`, 123 lines to 80. Everything here compiled unchanged from the
ServUO source apart from the property-body-to-expression rewrite:

```csharp
[Constructible]
public GreaterPoisonElemental() : base(AIType.AI_Mage)   // non-default AI; FightMode.Closest
{                                                        // and iRangeFight 1 are still defaults
    // ...
    SetStr(700, 771);          // two-argument overloads throughout
    SetStam(300, 322);         // SetStam exists

    PackItem(new Nightshade(4));         // quantity constructor
    PackItem(new LesserPoisonPotion());
}

public override bool BleedImmune => true;
public override Poison PoisonImmune => Poison.Lethal;
public override Poison HitPoison => Poison.Lethal;
public override double HitPoisonChance => 0.75;
public override int TreasureMapLevel => 5;

public override void GenerateLoot()
{
    AddLoot(LootPack.FilthyRich);      // several AddLoot calls in one GenerateLoot is fine
    AddLoot(LootPack.Rich);
    AddLoot(LootPack.MedScrolls);
}

public override void OnDeath(Container c)
{
    base.OnDeath(c);

    if (Utility.RandomDouble() < 0.03)
    {
        c.DropItem(new LuckyCoin());
    }
}
```

`LuckyCoin` is the dependency that failed the first build. The companion item, showing the
`ICommodity` shape and the collapsed constructor pair:

```csharp
[SerializationGenerator(0, false)]
public partial class LuckyCoin : Item, ICommodity
{
    [Constructible]
    public LuckyCoin(int amount = 1) : base(0xF87)   // ServUO's X() + X(int) pair, collapsed
    {
        Stackable = true;
        Amount = amount;
        Hue = 1174;
    }

    public override int LabelNumber => 1113366; // lucky coin

    int ICommodity.DescriptionNumber => LabelNumber;   // ServUO: TextDefinition Description
    bool ICommodity.IsDeedable => true;
}
```

## How to check a port at runtime

`[global get <props> where <Type>` reads every instance without needing to click a wandering
creature, which is the single biggest time sink:

```
[global get name rangeperception activespeed passivespeed currentspeed dex where PlagueRat
```

`[global set <prop> <value> where <Type>` and `[global bringtopack where <Type>` are the same
idea and save just as much time.

Standing up a local client against a throwaway build is written up in
`notes/cc1-p1-runtime-validation.md`, including three obstacles that will hit anyone repeating it:
the relay address, a ModernUO account-creation bug, and staff immunity from creature AI.

## How to check a port with no client at all

**Added by CC2.** A batch of 20 will never get a client session, so this is the normal path and
the client is the exception. Everything below runs against a throwaway `--rm` container with no
published ports and a scratch `Saves/`.

### What you can prove headlessly

1. **It compiles.** The build is the real gate and the only complete dependency check.
2. **The server starts and the world loads.** Watch for `Loading world done (N items, N mobiles)`
   with no errors. Note the world is *not* empty on a fresh `Saves/` — the ClusterF seeders build
   617 items and 90 mobiles at load, so there is real content to exercise.
3. **The world saves and reloads.** Console `save`, then restart the container on the same scratch
   `Saves/` and watch for a clean `Loading world done`.
4. **The type is registered, with generated serialization.** Reflect over the shipped assembly
   with a .NET 10 file-based app inside the container — the SDK is present in the runtime image:

   ```csharp
   // reflect.cs
   var asm = System.Reflection.Assembly.LoadFrom("/modernuo/UOContent.dll");
   var t = asm.GetType("Server.Mobiles.GreaterPoisonElemental");
   // list DeclaredOnly Serialize/Deserialize methods and the constructors
   ```

   ```bash
   docker run --rm -v "C:/path/to/reflect.cs:/tmp/reflect.cs:ro" --entrypoint sh <image> \
     -c 'cd /tmp && cp /modernuo/*.dll /tmp/ && dotnet run reflect.cs'
   ```

   A correctly generated type reports
   `generated=[Serialize(IGenericWriter) Deserialize(IGenericReader)] ctors=[() (Serial)]` —
   none of which is in your source, so it is direct evidence the generator ran. The assembly is
   the one the server loads, which the ClusterF seeders prove independently by running at world
   load from the same DLL.

### What you cannot prove headlessly

**Putting an instance of the new type into the world.** The container console registers exactly
three commands — `save`, `shutdown`, `restart` (`Projects/UOContent/Console/ConsoleCommands.cs`).
There is no console spawn, `Saves/SerializedTypes.db` records only types that have live instances
(stock `PlagueRat` and `GiantRat` are absent from it too on a world that has neither), and
`UOContent.Tests` ships no serialization round-trip harness.

So an *instance* surviving save and reload needs a client or a spawn scaffold. **Leave it
unverified and batch it into a five-creature client spot check** rather than working around it.
The residual risk is bounded: at version 0 with no `[SerializableField]`, the creature adds no
persisted state beyond what `BaseCreature` already round-trips, and CC1 proved that shape.

### Three traps in the headless harness

1. **Bind-mount paths must be Windows-style.** A Git-Bash `/c/Users/...` path mounts *empty*
   under Docker Desktop with no error; the server then falls through to its interactive
   client-data prompt and hangs. Use `C:/Users/...`.
2. **Startup eats stdin before the console handler exists.** On a world with no accounts,
   ModernUO asks `Do you want to create the owner account now? (y/n)` and holds stdin for about
   65 seconds. A piped command sequence must answer `n` first or the next command is swallowed.
3. **`shutdown` does not save.** Send `save`, wait for `Saving world done`, then `shutdown`.

Working invocation:

```bash
( sleep 12; echo n; sleep 35; echo save; sleep 30; echo shutdown; sleep 20 ) | docker run -i --rm --name <name> -v "$S/Saves:/var/lib/uo/modernuo/Saves" -v "$S/Backups:/var/lib/uo/modernuo/Backups" -v "$S/Archives:/var/lib/uo/modernuo/Archives" -v "$S/Configuration:/modernuo/Configuration" -v "D:/ShatteredLegacy/client-data/classic-client:/var/lib/uo/client-data/classic-client:ro" --security-opt seccomp=unconfined -e TZ=America/Chicago <image>
```

Edit the scratch `Configuration/modernuo.json` to `listeners: ["127.0.0.1:2593"]`,
`serverListing.address: "127.0.0.1"` and `autosave.enabled: "False"` so the throwaway server is
loopback-only and does not save on a timer behind your back.

## `BaseCreature` members ModernUO does not have (CC3)

Checked against `D:\UO\ModernUO-pinned` at `7c9215d97`. Each of these compiles in ServUO and is a
compiler error in ModernUO. Grep a candidate for them before writing anything.

| ServUO member | ModernUO | What to do |
|---|---|---|
| `AttacksFocus` | absent entirely | drop; normal `FightMode` targeting applies |
| `DragonBlood` | no property **and** no item | drop the carving yield |
| `OnAfterTame(Mobile)` | no hook at all | drop. `StatLossAfterTame => true` gives `AnimalTaming`'s `ScaleStats(0.50)`, which is the nearest thing |
| `IsChampionSpawn` (creature flag) | only `ChampionSpawn.IsChampionSpawn(Mobile)`, a method on the spawn | collapse a `GenerateLoot` branch to its non-champion arm |
| `SetToChampionSpawn()` | nothing calls back into the creature | drop |
| `FoodType.FruitsAndVegies` | `FruitsAndVeggies` | rename, two g's (already noted above) |

Confirmed **present and unchanged**, so port them literally: `CanAngerOnTame`,
`StatLossAfterTame`, `MinTameSkill`, `PackInstinct` (with `Ostard`), `HideType` (with `Horned`,
`Spined`), `PackGold`, `OnActionCombat`, `OnCombatantChange`, `OnBeforeDeath`, `AIObject`,
`ActionType.Combat`, `Map.CanFit(x,y,z,height,checkBlocksFit,checkMobiles)` (same argument order),
`Map.GetAverageZ`, `AOS.Damage(m, from, dmg, phys, fire, cold, pois, nrgy)`, the 13-argument
`Mobile.MovingParticles(..., EffectLayer, int)`, `Region.IsPartOf(string)`, `LootPack.UltraRich`,
and all the `Get*Sound` overrides. `DateTime.UtcNow` becomes `Core.Now`.

## Items: two more differences (CC3)

- **`IsArtifact` is ServUO-only.** It is a `Server.Item` virtual, and every consumer
  (`BasePigmentsOfTokuno`, `NaturalDye`, `AlterItem`, `RunicReforging`, `ArcaneGem`) is also
  ServUO-only. Dropping the override has **zero** readers in ModernUO. Not a deviation worth
  recording per item.
- **`BaseDecorationArtifact` differs.** ServUO gates the artifact-rarity property line on a
  `ShowArtifactRarity` virtual; ModernUO's base adds it unconditionally and has no such virtual.
  For an item that sets `ShowArtifactRarity => false`, deriving from ModernUO's base *adds* a
  property line ServUO suppresses. The faithful move is to derive from `Item` and reproduce the
  three members the base contributes — `DefaultWeight => 10.0`, `ForceShowProperties => true`,
  plus the item's own `DisplayWeight` — since nothing in ModernUO branches on the base type.
  CC3 did this for six TOL decorations.

## Headless harness: change exactly three settings

Added by CC3, which lost a run to this. In the scratch `Configuration/modernuo.json`, change only:

```
listeners                  -> ["127.0.0.1:2593"]
serverListing.address      -> "127.0.0.1"
autosave.enabled           -> "False"
```

**Do not also disable `pingServer`.** Stock `PingServer.Shutdown()`
(`Projects/Server/Network/PingServer.cs:145`) null-dereferences if the server was never started,
so `pingServer.enabled=False` turns every `shutdown` into an unhandled exception and a crash
report. The save completes first, so it does not corrupt anything — it just wastes a cycle and
makes the log look like the port broke something. The scratch config is not a place to tidy.
