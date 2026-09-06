# Port recipe: ServUO to ModernUO

**Status: VALIDATED against a real build and a running client, 2026-09-06 (backlog P1 / CC1).**
The draft that preceded this was written from source study. Both of its "fidelity traps" were
wrong — one of them exactly backwards — and are corrected below. Evidence and method are in
`notes/cc1-p1-runtime-validation.md`.

Reference port: `PlagueRat.cs`, ServUO `Mobiles/Normal` → `server/customizations/Mobiles/Normal/`.
88 lines to 55. Built in Docker from pinned ModernUO `7c9215d97`, spawned with `[add PlagueRat`,
inspected with `[global get`, saved, server restarted, reloaded intact.

The headline still holds: for simple content, porting is mostly **deleting boilerplate**.
ModernUO's source generator writes the serialization ServUO writes by hand.

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
- `MinTameSkill`, `Fame`, `Karma`, `VirtualArmor`, `BaseSoundID`, `Hides`, `Meat`,
  `FavoriteFood`, `LootPack.Rich`, `AddLoot`, and the single- and two-argument
  `SetStr/SetDex/SetInt/SetHits/SetMana` overloads all exist unchanged.

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

**This is a shard-wide decision, not a per-file one, and it is open.** See Q-008 in
`notes/codex-questions.md`. Three defensible targets:

- **ModernUO Medium (do nothing).** Consistent with ModernUO's own roster; a ported creature
  moves like its nearest stock peer. PlagueRat is a re-hued `GiantRat`, and stock `GiantRat` is
  Medium — so for this one file, doing nothing is arguably the *most* faithful choice.
- **`SpeedLevel.Fast` (0.2/0.4).** Matches the ServUO constructor literal, which is what a reader
  of ServUO source would expect — but not what ServUO runs.
- **Dex-derived per creature.** Matches ServUO's actual runtime, requires a `GetSpeeds` override
  per creature and abandons ModernUO's table.

**PlagueRat was ported with no override (Medium), and that assumption is recorded here.** Do not
copy it blindly onto CC3+ until Q-008 is answered.

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

Carried over from the draft. **Not exercised by this port** — PlagueRat has no persisted state,
no `Serial` arithmetic and no string building. Treat as still unverified:

- **`Serial` is signed in ServUO, `uint` in ModernUO.** Any arithmetic or comparison against
  `-1` needs checking rather than find-and-replace.
- **`[SerializableField(n)]`** replaces hand-written field writes when a type has real persisted
  state. Simple creatures with no extra state need none — PlagueRat needed none.
- **`TextDefinition`, `PooledRefQueue`, `ValueStringBuilder`** are ModernUO idioms with no ServUO
  equivalent.

**Name collisions** are verified: check the stem against `tools/modernuo-stems.txt` before
porting. `PlagueRat` is absent from it, and the structured mirror's overwrite check independently
confirmed no collision at build time.

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
