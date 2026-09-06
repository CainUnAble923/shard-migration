# Port recipe: ServUO to ModernUO

**Status: DRAFT by Claude from source study. Codex validates and corrects it during backlog
item P1.** Derived from a side-by-side of `Alligator.cs`, which exists in both trees, plus
ModernUO's `BaseCreature` constructor.

The headline: for simple content, porting is mostly **deleting boilerplate**. ModernUO's
source generator writes the serialization ServUO writes by hand.

## The mechanical transformation

| ServUO | ModernUO |
|---|---|
| `using System;` | `using ModernUO.Serialization;` |
| `public class X : BaseCreature` | `[SerializationGenerator(0, false)]`<br>`public partial class X : BaseCreature` |
| `[Constructable]` | `[Constructible]` |
| `[CorpseName("an alligator corpse")]` on the class | `public override string CorpseName => "an alligator corpse";` |
| `Name = "an alligator";` in the constructor | `public override string DefaultName => "an alligator";` |
| `public X(Serial serial) : base(serial) { }` | **delete it** — the generator provides it |
| `public override void Serialize(GenericWriter w)`<br>`public override void Deserialize(GenericReader r)` | **delete both** — the generator provides them |
| `public override int Meat { get { return 1; } }` | `public override int Meat => 1;` |

Note `partial` is required, and the `(0, false)` in `SerializationGenerator` is version 0 and
"not encoded". Use `0` for new content with no existing saves.

## Two fidelity traps, both easy to miss

These change behaviour silently and neither produces a compiler error.

### 1. Range perception defaults differ

ServUO creatures typically pass `10`. **ModernUO's `DefaultRangePerception` is `16`.**

```
// ServUO
base(AIType.AI_Melee, FightMode.Closest, 10, 1, 0.2, 0.4)

// WRONG - silently widens perception from 10 to 16
base(AIType.AI_Melee)

// RIGHT - carry the explicit value across
base(AIType.AI_Melee, FightMode.Closest, 10, 1)
```

**Always pass the ServUO value explicitly.** Do not rely on ModernUO's defaults matching.
Stock ModernUO content often omits it, which is ModernUO's own choice, not a licence for us
to change a ported creature's behaviour.

### 2. Speeds moved out of the constructor

ServUO's constructor takes six arguments; ModernUO's takes four. The last two, `activeSpeed`
and `passiveSpeed`, are gone. ModernUO derives them instead:

```
GetSpeeds(out var activeSpeed, out var passiveSpeed);   // -> NPCSpeeds.GetSpeeds(this, ...)
```

So **drop the two speed arguments** and let `GetSpeeds` derive them. If a ServUO creature has
genuinely unusual speeds that matter, override:

```
public override void GetSpeeds(out double activeSpeed, out double passiveSpeed)
{
    activeSpeed = 0.2;
    passiveSpeed = 0.4;
}
```

Under the fidelity principle, prefer the derived values unless the ServUO numbers are clearly
deliberate. Record any override you add.

## Also watch for

- **`Serial` is signed in ServUO, `uint` in ModernUO.** Any arithmetic or comparison against
  `-1` needs checking rather than find-and-replace.
- **`[SerializableField(n)]`** replaces hand-written field writes when a type has real
  persisted state. Simple creatures with no extra state need none.
- **Name collisions.** Before porting, check the stem against `tools/modernuo-stems.txt`.
  A collision means it becomes a routed replacement in `apply-patches.sh`, not an additive file.
- **`TextDefinition`, `PooledRefQueue`, `ValueStringBuilder`** are ModernUO idioms with no
  ServUO equivalent; going this direction you will rarely meet them, but ported code that
  builds strings in a loop is worth looking at.

## Worked example

`Alligator.cs`, ServUO 88 lines to ModernUO 40. Everything removed was boilerplate the
generator now writes: the `Serial` constructor, both serialization overrides, and the
property bodies. The only genuine content change is `CorpseName` and `DefaultName` moving
from an attribute and a constructor assignment to overrides.

## Open for Codex to confirm in P1

- Does `[SerializationGenerator(0, false)]` need a migration JSON for brand-new types? (Expected: no.)
- Where exactly does a ported file land, and does `apply-patches.sh` need any change for
  additive content? (Expected: `server/customizations/`, no change.)
- Confirm the built creature actually spawns and behaves.
