# S9 — Re-measure the remaining content backlog

**Measurement only. Nothing was ported. No file in `server/customizations` changed.**

Four rows were named in `docs/tasks.md` as the biggest unmeasured items left:
Revamped Dungeons at 255, Artifacts and equipment at 466, Decoration/housing/crafting at
297, High Seas cheap half at ~78. None had ever had the S3 filter applied.

They have now. Every count below has its file list in the appendix.

---

## 1. The headline, before any table

**The brief's premise was wrong, and so were three of the four figures it quoted.**

The brief says "every remaining content row is still an unfiltered ServUO file count".
Three of the four are not raw counts at all — they are counts that had *already* been
filtered once, by a weaker filter, in `docs/content-menu.md` on 2026-09-06. That document
compared ServUO against **ModernUO's 3,565 `UOContent` type names**; S3 later built the
real index of **7,093 types across the whole pinned tree**. So the rows sit between the
raw number and the S3 number, and nobody could tell which by looking.

| Row | Figure in `docs/tasks.md` | What it actually is | Raw ServUO | **Candidates after the S3 filter** |
|---|---|---|---|---|
| CC4 Revamped Dungeons | 255 | already weak-filtered; the weak filter removed nothing | 255 | **255** |
| Artifacts and equipment | 466 | already weak-filtered (318 + 148) | **1,022** | **455** |
| CC7 Decoration/housing | 297 | already weak-filtered (169 + 88 + 40) | **745** | **303** |
| CC5 High Seas cheap half | ~78 | genuinely raw (57 Items + 21 Mobiles) | 78 | **77** |

Two consequences.

**The artifacts row is not 466 and never was.** The raw directories hold **1,022** files;
**567 of them are types ModernUO already declares**. The real candidate count is **455** —
close to the quoted 466 by coincidence, from a different denominator, and 55% of the raw
tree is duplicate-type build failures.

**The decoration row is not 297 either.** Raw 745, **442 duplicates**, **303 candidates**.
And `docs/tasks.md`'s CC7 text lists five directories (`Addons`, `Decorative`,
`New Magincia`, `Items/Resource`, `BulkOrders`) while the 297 covers only the first three.
The two extra directories add **57** more candidates from 191 raw. Measured both ways below.

**`docs/tasks.md` also disagrees with itself on CC4.** The S9 section says 255; the CC4
section on the same page says "150 candidate files". Neither is sourced. The answer is
**255**: `Services/Revamped Dungeons` contains 255 `.cs` and **not one of them** has a
primary type ModernUO declares. It is the only row of the four where the filter removes
nothing at all.

**Eleven counts on this project have now moved under scrutiny.** Three of these four rows
make twelve, thirteen and fourteen.

---

## 2. Method

### Step 1 — the filter, reproduced exactly

A ServUO file whose **primary type** ModernUO (or our own tree) already declares is a
duplicate-type build failure, not a porting candidate. Primary type = the type whose name
matches the filename stem, else the first type declared in the file.

That definition, run against a fresh index of both trees, gives **3,134 of ServUO's 6,144
files** — S3's figure to the file. Two other plausible definitions give 3,040 and 2,821, so
the definition is doing real work and is stated here rather than assumed.

Index sizes, rebuilt for this task: ModernUO pinned `7c9215d97` — 3,991 files, **7,093
types**; ServUO pub57 `Scripts` — 6,144 files, **11,352 types**; our
`server/customizations` — 198 files, 409 types. (`AGENTS.md` says 7,097 and 11,363; the
2–11 file difference is comment- and string-stripping, and the filter output is identical.)

### Step 2 — resolve, because a reference count is an upper bound

For each surviving candidate, collect every identifier it uses that **neither pinned
ModernUO nor `server/customizations` contains anywhere**, then ask who owns each name:

| Bucket | Meaning | What it costs |
|---|---|---|
| **drops straight in** | nothing missing at all | the conversion only |
| **in-row** | owned by another candidate in the same row | port them together |
| **elsewhere** | owned by a ServUO file ModernUO also lacks | co-port, +N extra files |
| **upstream** | a *member* of a base class ModernUO **does** have | a carrier and usually a patch |
| **unknown** | nothing in `ServUO/Scripts` declares it | read it |

Three sets are subtracted first, each verified by reading **both** implementations rather
than matching a name:

- **EQUIV** — ModernUO does the same thing under a different name (§3).
- **CONVERT** — ServUO API whose ModernUO counterpart every port already writes:
  `GenericReader`→`IGenericReader`, `Constructable`→`Constructible`,
  `ReadItem`/`ReadMobile`→`ReadEntity<T>`, `IsPlayer`→`Player`,
  `UpdateProperties`→`InvalidateProperties`, `GetEnumeratedMobiles`→`GetMobilesInRange`,
  `TimerStateCallback`→`Timer.DelayCall`. Counting these as blockers means counting the
  port itself as a blocker.
- **DELETABLE** — a one-line flag with **zero consumers anywhere in pinned ModernUO** (§4).

S3's blacklist of ServUO's ubiquitous private helper names (`InternalTarget`,
`InternalTimer`, `Misc`, `City`, …) is applied unchanged.

### What I got wrong on the way, and fixed

Three defects in my own instrument, all found before publishing and all of the shapes this
project keeps hitting:

1. **`namespace` lines counted as type references.** `NewMagincia` looked like a 28-file
   blocker; **26 of the 28 were the line `namespace Server.Engines.NewMagincia`**. Same
   defect inflated `VoidPool` from 4 to 11. This is `InternalTarget` again with a different
   token. Fixed by stripping `using`/`namespace` directives before scanning.
2. **A type-name-only scan cannot see property-level dependencies.** `SetID`,
   `SetAttributes`, `SetSkillBonuses` and `SetSelfRepair` are *properties* on ServUO's
   `BaseArmor`, not types. My first pass therefore reported set-armour files as clean.
   Fixed by indexing member declarations too — which is what produced the `upstream`
   bucket, the most useful column in this survey.
3. **A mangled string-literal regex** was leaking string contents into the identifier sets,
   giving ModernUO ~1,900 identifiers it does not have and so *hiding* blockers. Rewritten;
   the filter still reproduces 3,134 exactly, which is the regression check.

### And one method that failed outright — worth recording

I built a transitive closure: follow each candidate's dependencies through ServUO until
they reach a subsystem ModernUO has zero files for. It produced clean-looking numbers
(193 / 17 / 61 / 16 / 35 hard-blocked) and **every one of them is an artefact.**

The giveaway was uniformity — nearly every row reported the same count against every
subsystem. Probing it: **`Items/Artifacts/Equipment/Armor/LordBlackthornsExemplar.cs`, one
artifact breastplate, pulls in 758 files and reaches all thirteen subsystems.** The path
runs through hub files (`ItemInterfaces.cs` → `RewardOptionGump.cs` → the New Magincia
lotto → everything).

**A transitive closure over "mentions" is not a resolution method.** It says everything is
blocked by everything. The numbers are not published, and the direct resolution below —
S3's and S6's method — is what is published. This is the "touches X is not blocked by X"
error at tree scale, and it is much harder to see there than in a single file.

---

## 3. Equivalents hiding under different names — a third `SetWeaponAbility`

`AGENTS.md` records two of these, each of which cost real content. Here is a third, and it
is the largest yet.

### `FlipableAttribute` is `FlippableAttribute`. One letter.

| | ServUO | ModernUO |
|---|---|---|
| Declaration | `Items/Internal/FlipableAttribute.cs:63` | `UOContent/Items/Misc/FlippableAttribute.cs:54` |
| Constructor | `FlipableAttribute(params int[] itemIDs)` | `FlippableAttribute(params int[] itemIDs)` |
| `Flip(Item)` | reflects a `Flip()` method when `ItemIDs` is null, else cycles `ItemID` | **the same, statement for statement** |

Zero occurrences of `FlipableAttribute` in pinned ModernUO. **86 files across three of the
four rows looked blocked by it.** None is.

The full equivalents table, each entry checked by opening both files:

| ServUO name | Files affected | What ModernUO does instead |
|---|---|---|
| `FlipableAttribute` / `Flipable` | **86** | `FlippableAttribute`, identical body |
| `ITool` | **23** | `BaseTool`; ModernUO's `ICraftable.OnCraft` takes `BaseTool` where ServUO takes `ITool`. 20 of the 23 hits are that one parameter |
| `IFlipable` | 16 | `FlippableAttribute` reflects a `Flip()` method; `OnFlip(Mobile)` renames to `Flip()` |
| `ItemQuality` | 15 | `ArmorQuality` / `WeaponQuality` / `ClothingQuality` / `ToolQuality` — same three values, `Normal`→`Regular`. ServUO unified them; ModernUO did not |
| `IRepairable` | 12 | **nothing is needed.** `Repair.cs:236/310/380` already dispatches on `BaseWeapon`, `BaseArmor` and `BaseClothing`, and all 12 derive from one of those. ModernUO's own source carries `// TODO: Make an IRepairable` at `Repair.cs:163` |
| `IChopable` | 6 | `BaseAddon.OnChop(Mobile)` virtual, `BaseAddon.cs:92` |
| `IQuality` / `IResource` | 5 | concrete `Quality`/`PlayerConstructed` and `CraftResource Resource` members (`BaseArmor.cs:259`) |
| `TalismanSkill` | 3 | `BaseTalisman` exists (11 files); ModernUO expresses the bonus with `SkillName` |
| `SimpleContextMenuEntry` | 3 | `ContextMenuEntry` (86 files) plus a 20-line callback subclass |

**169 file-references, none of them a block.** ServUO refactored a group of concrete members
into interfaces; ModernUO did not. That is a per-file transformation of one token, not a
subsystem.

---

## 4. `IsArtifact` — 280 files, worth nothing, and the reason matters

Once member-level names were indexed, `IsArtifact` became the second-largest apparent
blocker in the survey: **280 files in the artifacts row and 153 in Revamped Dungeons**, each
carrying `public override bool IsArtifact => true;` against a virtual pinned ModernUO does
not have.

It reads like a real gap. It is worth nothing, and only reading the consumers shows why.
Every reader of `IsArtifact` in ServUO is in a system we have not ported:
`BasePigmentsOfTokuno.cs:141`, `ArcaneGem.cs:186`, `AlterItem.cs:359/377/388/402`,
`NaturalDye.cs:154`, `SpecialNaturalDye.cs:198`, and one commented-out line in
`BaseVendor.cs:2526`. **Pinned ModernUO contains zero occurrences of the name at all**, so
there is nothing to feed.

**Delete the line. Nothing observable changes.** Log it so it can be restored if Pigments of
Tokuno or `AlterItem` is ever ported. The same is true of `CanBeWornByGargoyles` (83 hits),
`Alterable`, `ExcludeDeedHue` and `SetWearable`.

This is the `AbsorptionAttributes` lesson again: **a name is a hypothesis about behaviour.**
`IsArtifact` sounds like it does something. It is a flag nobody reads.

---

## 5. The four rows, measured

Candidate = survives step 1. Buckets are §2. Full lists in the appendix.

| Row | Raw | Filtered out | **Candidates** | Lines | Drops in | +row file | +co-port | Upstream/carrier |
|---|---|---|---|---|---|---|---|---|
| **CC4 Revamped Dungeons** | 255 | 0 | **255** | 28,763 | 31 | 25 | 140 | 59 |
| **Artifacts + equipment** | 1,022 | **567** | **455** | 45,230 | **320** | 81 | 10 | 44 |
| **CC7 Decoration/housing (the 297)** | 745 | **442** | **303** | 39,801 | 159 | 50 | 5 | 89 |
| **CC7 extra** (`Resource`, `BulkOrders`) | 191 | 134 | **57** | 6,440 | 33 | 0 | 5 | 19 |
| **CC5 High Seas cheap half** | 78 | 1 | **77** | 16,940 | 31 | 17 | 12 | 17 |

### 5.1 Artifacts and equipment — the best row on the backlog

**455 candidates, of which 401 (88%) need nothing built at all**: 320 drop straight in, 81
more need only another file from the same two directories. The co-port bucket is **10 files
needing 14 extra ServUO files**. Only 44 need an upstream member.

That 44 is dominated by three small things, not by subsystems:

- **`NegativeAttributes` (6) and its members `Brittle`/`NoRepair` (10)** — a `BaseAttributes`
  subclass, 137 lines including the enum. ModernUO **has** `BaseAttributes`
  (`UOContent/Misc/AOS.cs:1349`), so this is additive in exactly the S1/S6 shape, plus a
  serialized property on the four equipment base classes. Every use in these rows is a
  one-line assignment (`NegativeAttributes.Antique = 1;`).
- **SA weapon attributes** — `BalancedWeapon`, `SplinteringWeapon`, `BloodDrinker`,
  `HitFatigue`, `HitManaDrain`, `HitCurse`. 13 references. ModernUO's `AosWeaponAttribute`
  lacks these values. Unlike the two above these are *behavioural*: the property alone does
  not make the proc fire, so deleting the line loses a real effect on ~13 items.
- **The gargoyle wearables** (§6).

**The 567 filtered out are the finding worth repeating.** More than half of ServUO's
artifact and equipment tree is types ModernUO already ships. Any plan built on 466, or on
1,022, was planning against the wrong denominator in opposite directions.

### 5.2 CC4 Revamped Dungeons — 255 real candidates, and one cosmetic line

CC4 is the only row where the filter removes nothing: **255 raw, 255 candidates, 0
duplicates.** Places to go and things to fight really are absent from ModernUO.

But the resolution is dominated by a single token. **138 of the 255 reference
`ReforgedSuffix`, and 136 of them use it exactly once**, as:

```csharp
ReforgedSuffix = ReforgedSuffix.Blackthorn;
```

That is a name decoration: it makes the item read "… of Blackthorn". Only **two** files use
it structurally — `InvasionController.cs` reads it back to identify Blackthorn drops, and
`AgentoftheCrown.cs` calls `RunicReforging.GenerateRandomItem`.

`ReforgedSuffix:138` is the `ReforgedSuffix` trap in its purest form, and it is the same
error that made 132 creature files look like a 100% decline rate when the real rate was
about 14%. **Two options, both cheap:**

- **Delete one line per file.** Zero cost. 136 artifacts lose a name suffix. A visible,
  bounded fidelity deviation on cosmetics only.
- **Build the minimal carrier.** *Not* `RunicReforging.cs` (3,391 lines) — only the naming
  subset: the `ReforgedSuffix` enum (18 values), the 18-row cliloc `NameTable`,
  `GetSuffixName` and `AddSuffixName` (`RunicReforging.cs:1699-1741`). **About 100 additive
  lines.** Then a serialized `ReforgedSuffix` property plus an `AddNameProperty` hook on
  `BaseClothing`, `BaseArmor`, `BaseWeapon` and `BaseJewel`.

**The carrier frees 110 files, confirmed by two independent counterfactuals.** Not 138 —
28 of the 138 have other blockers too, which is exactly why a reference count is an upper
bound.

**The honest cost is the patches, not the lines.** All four seams exist and are in
`UOContent`, not the core: `AddNameProperty(IPropertyList)` is already overridden at
`BaseArmor.cs:1221`, `BaseClothing.cs:672` and `BaseWeapon.cs:2854` (`BaseJewel` has
`GetProperties` at `:254` and would need the override added). But these are
`[SerializationGenerator]` partials — `BaseClothing` is at version 7 — so adding a
`[SerializableField]` means bumping the version and writing a migration JSON, four times.
That is the same shape as S1's `BaseArmor-set-self-repair.patch`, and it is real work.

**I did not try to build it and I am not recommending it blind.** The one-line delete is
available at zero cost and loses only a suffix in an item name.

### 5.3 CC7 Decoration/housing — one 71-line shim is a third of the row

**745 raw, 442 duplicates, 303 candidates.** The `upstream` bucket is 89, and **74 of those
are two names**:

- **`DirectionType` — 41 files.** A five-value enum, `Items/Internal/ItemInterfaces.cs:71`.
  Seven lines.
- **`AddonOptionGump` — 33 files.** `Services/VeteranRewards/RewardOptionGump.cs:81`, **64
  lines**. ModernUO already ships `RewardOptionGump`, `RewardOptionList`, `RewardOption` and
  `IRewardOption` (`UOContent/Engines/Veteran Rewards/RewardOptionGump.cs`). ServUO's class
  is a variant of that gump for addon deeds that are not veteran rewards.

Together: **about 71 additive lines, no patch, and they free 34 files.** That is the best
ratio measured anywhere in this survey — roughly **34 files freed per 71 lines**, against
the armour-set system's celebrated 114:387.

This is what S6's "31 files one small carrier class away" looks like when the carrier is
finally costed. It had not been.

### 5.4 CC5 High Seas cheap half — the ~78 is the one honest figure

**78 raw, 1 duplicate, 77 candidates, 16,940 lines.** The only row whose published number
survives contact.

Its structure is different from the others: 31 drop in, 17 need another file from the same
two directories, and **12 need naval files the row explicitly excludes.** `BaseGalleon` (7),
`GalleonHold` (4), `SecurityLevel` (3), `BritannianShip` (3) — the CC8 boundary. `docs/tasks.md`
says "skip anything referencing `BaseGalleon`, `ShipCannon` or `Cannon`"; the measured cost
of that instruction is **12 of 77 files**, and the list is in the appendix so the skip is a
decision rather than a surprise.

Two more sit behind Skill Masteries (`SkillMasteryPrimer` on `Charybdis` and
`OsiredonTheScalisEnforcer`) and a handful behind Corgul's regions.

### 5.5 CC7's extra two directories

`Items/Resource` and `Services/BulkOrders`: **191 raw, 134 duplicates, 57 candidates.** 33
drop straight in. The `BulkOrders` half is the awkward part — six `*RewardCalculator`
classes live inside `Services/BulkOrders/Rewards/Rewards.cs`, whose primary type ModernUO
already has, so they are extracts rather than ports (§7). They gate 11 files.

Whether these two directories belong in CC7 is a `docs/` question I have not answered; both
counts are given so either reading is costed.

---

## 6. Overlaps, and what building two things together buys

Handled explicitly, per `AGENTS.md`.

| Pair | Together | Sum of the two alone | Extra |
|---|---|---|---|
| **ReforgedSuffix carrier + gargoyle wearables** | **141** | 110 + 7 = 117 | **+24** |
| Addon direction/option shim + the small gump shims | 58 | 34 + 22 | +2 |
| `NegativeAttributes` + `ExtendedWeaponAttributes` | 14 | 8 + 5 | +1 |
| `DamageableItem` + naval | 14 | 5 + 8 | +1 |

Only the first is large enough to change a decision, and it was invisible to every
single-subsystem count.

**The gargoyle wearables are a cluster nobody has named.** Sixteen gargoyle equipment types
ModernUO does not ship — `GargishRobe`, `GargishFancyRobe`, `GargishEarrings`,
`GargishGlasses`, `GargishClothKilt`, `GargoyleHalfApron`, `GargishPlateChest`,
`GargishGnarledStaff`, `GargishKatana` and seven more — spread across **9 whole ServUO files
and 7 extracts from files ModernUO already has**, about **1,641 ServUO lines**.

On its own it frees 7 files. Built alongside the ReforgedSuffix carrier it frees **24 more**,
because the Blackthorn and Exodus loot sets are gargoyle variants of the same garments.
Neither costing alone would have shown that.

**And it is not a separate piece of work at all.** All fourteen of those ServUO files sit
inside the artifacts-and-equipment row: **9 are already candidates in it**
(`GargishGlasses.cs`, `GargishClothArmor.cs`, `GargishLeatherArms.cs`,
`GargishPlateChest.cs`, `GargishPlateLegs.cs`, `GargishStoneChest.cs`,
`GargishEarrings.cs`, `GargishGnarledStaff.cs`, `GargishKatana.cs`) and the other 5 are the
extract donors of §7 (`Cloaks.cs`, `MiddleTorso.cs`, `OuterLegs.cs`, `Shirts.cs`,
`Waist.cs`).

So **doing recommendation #1 delivers 9 of the 14 as ordinary row content**, and the
gargoyle cluster stops being a decision and becomes 7 extracts left over. That in turn
means the +24 overlap with the ReforgedSuffix carrier is nearly free *after* #1 and is not
free before it — which is a sequencing argument, not just a value one.

---

## 7. A caveat on the filter itself, which S3 established and nobody has stated

The step-1 filter discards a file when ModernUO declares its **primary** type. ServUO files
often declare several. When the primary type collides and a *secondary* one does not, the
filter throws away a type the row still needs.

A name can also be both: `GargishPlateLegs.cs` is itself a clean candidate in the artifacts
row *and* the thing a Blackthorn loot file in CC4 is blocked on. That is not a
contradiction — it is what "co-port" means, and it is why §6's overlaps matter.

**149 blocked-file references across the four rows resolve to 28 such types, sitting inside
18 files the filter discarded.** Examples: `AddonOptionGump` inside `RewardOptionGump.cs`,
`DirectionType` and `ItemQuality` inside `ItemInterfaces.cs`, `NegativeAttributes` and
`ExtendedWeaponAttributes` inside `AOS.cs`, `GargishRobe` inside `Cloaks.cs`, `Plum` inside
`Fruits.cs`, six `*RewardCalculator` classes inside `Rewards.cs`.

**These are extracts, not ports** — usually 20 to 60 lines each — and they are cheaper than
the filter's output suggests, not more expensive. But they are invisible to any count
phrased as "files ModernUO lacks", including every count in this note's own summary table.
The full list is in the appendix.

---

## 8. What S1, S5 and S6 made newly free — much less than the brief expected

The brief asks what is now free because the armour set bonuses, the ML quest engine and the
Stygian Abyss absorption system have shipped. I measured it by re-running the whole filter
with `server/customizations` excluded and diffing.

**Ten files, across all four rows.**

| Row | Newly clean | Already ported by us, so no longer candidates |
|---|---|---|
| Artifacts + equipment | **9** | 20 |
| CC5 High Seas cheap half | **1** | 0 |
| CC4, CC7, CC7-extra | 0 | 33 |

The nine: `DespiseArtifacts.cs`, `SpinedBloodwormBracers.cs`,
`RangersCloakOfAugmentation.cs`, `AxeOfAbandon.cs`, `BladeOfBattle.cs`,
`ClawsOfTheBerserker.cs`, `StormCaller.cs`, `FrostguardTalisman.cs`, `JadeSnakeHead.cs`.
Plus `SmilingMoonBlade.cs` in High Seas.

**This is not evidence that S1, S5 and S6 were poor value.** It is evidence about where
their value landed: the 114 files the armour-set system unblocked are overwhelmingly *set
armour*, which lives in `Items/Artifacts/Equipment/Armor/Sets` and was **already counted as
portable in this row before those tasks shipped** — the set files reference `SetID` and
`SetAttributes`, and until my second pass those were invisible to a type-name scan (§2).
S1's benefit is real and was banked in the artifacts row's 455; it is not a further
reduction on top of it.

**S6's note said 31 files were one small carrier class away and the carrier had not been
costed. It has now** — but the carrier that matters most for *these* rows is not S6's. It is
the 71-line addon direction/option shim in §5.3, which frees 34, and the ~100-line
ReforgedSuffix naming carrier, which frees 110.

---

## 9. Ranked, with a recommendation

Ranked by what it costs against what it delivers. **The decision is Chase's; nothing here
has been acted on.**

| # | Do | Cost | Delivers | Why |
|---|---|---|---|---|
| **1** | **Artifacts and equipment, the 320 that drop straight in** | conversion only, no new subsystem, no patch | **320 files** | Highest volume of finished content per hour on the whole backlog, and the only row where the majority needs nothing built. Batch it. |
| **2** | **The addon direction/option shim, then CC7's 159** | **~71 lines, 0 patches** | 34 files, then 159 that drop in | Best ratio measured anywhere here. `DirectionType` is 7 lines; `AddonOptionGump` is 64 and models a gump ModernUO already ships. |
| **3** | **CC5 High Seas cheap half, skipping the 12 naval files** | conversion only | 48 of 77 | The one row whose published figure was right. Self-contained, visible, and the CC8 boundary is now an enumerated list rather than a guess. |
| **4** | **CC4, with `ReforgedSuffix` deleted rather than built** | conversion + 136 logged cosmetic deviations | up to 166 | Dungeons are the best *content* on the backlog. Deleting the line costs an item-name suffix and nothing else. |
| 5 | The gargoyle wearables cluster | ~1,641 ServUO lines — but **9 of its 14 files are already inside #1** | 7 alone, **+24 with #6** | Mostly delivered by #1. Do not schedule it separately before #1; after #1 it is 7 extracts. |
| 6 | The `ReforgedSuffix` naming carrier | ~100 additive lines **+ 4 serialization patches and 4 migrations** | 110, or **141 with #5** | Good ratio, real reconciliation cost. Do it only if the lost suffixes in #4 turn out to matter. |
| 7 | `NegativeAttributes` carrier | ~137 lines + property on 4 base classes | 8 | Additive over ModernUO's existing `BaseAttributes`. Marginal alone; nearly free next to #6, which patches the same four classes. |
| — | SA weapon attributes (`BalancedWeapon`, `SplinteringWeapon`, …) | unmeasured — needs combat hooks | 13 | **Not costed here.** Unlike the others these are behavioural, and I did not measure the hook cost. Do not schedule it on this note. |
| — | CC7's `Resource` + `BulkOrders` | — | 33 drop-ins, 11 behind extracts | Take the 33; leave `BulkOrderSystem.cs` until the six reward calculators are extracted. |

### What I would do first, and why

**Artifacts and equipment (#1).** Not because it is the largest row — CC7 raw is larger —
but because it is the only one of the four where **88% of the candidates need nothing
built**, and 320 of them need nothing at all beyond the standard conversion. There is no
subsystem decision embedded in it, no patch, no migration, and no fidelity deviation to log.
It is the lowest-risk large batch available.

**And it is the row whose number was most wrong.** It was carried as 466 against a raw tree
of 1,022, of which 567 are duplicate-type build failures. Both numbers were misleading in
opposite directions, and neither told anyone that this is the cheapest row on the plan.

**Second, the 71-line shim (#2)**, because it is small enough to do in the same sitting as a
CC7 batch and turns 34 blocked files into portable ones.

**#1 first also sequences #5 and #6 correctly**, per §6: it delivers 9 of the 14 gargoyle
files as ordinary content, so the gargoyle-plus-ReforgedSuffix overlap that frees 141
becomes reachable for the cost of 7 extracts instead of a 1,641-line cluster. Doing #5 or
#6 before #1 pays for content #1 was going to bring anyway.

**I would not build the `ReforgedSuffix` carrier yet.** The ratio is good and the delete is
free. Port CC4 with the line removed, see whether anyone misses "of Blackthorn", and decide
with that information instead of before it.

---

## 10. What this survey did not do

- **It did not port anything, and it did not build anything.** No file outside `notes/` and
  `tools/progress-state.json` changed.
- **It did not compile a single candidate.** Every "drops straight in" is a static claim
  about names, not a build result. The first batch will find things this method cannot see:
  signature changes, generic-arity mismatches, sealed base classes.
- **It did not measure the SA weapon attributes** (`BalancedWeapon`, `SplinteringWeapon`,
  `BloodDrinker`, `HitFatigue`, `HitManaDrain`, `HitCurse`). They are behavioural, they need
  combat hooks, and the hook cost is unmeasured. 13 references. Do not plan against them.
- **It did not resolve the `unknown` bucket file by file.** These are mostly enum members of
  enums ModernUO names differently (`VeryEasy`, `EastLarge`, `Mondain`, `AI_Mystic`,
  `Crewman`, `Pristine`). They are conversion-shaped rather than subsystem-shaped on every
  sample I read, but I read a sample, not all of them. The full list is in the appendix.
- **It did not re-measure CC6.** S3 did that and its 137 stands unchallenged here.
- **It did not touch `docs/`.** Everything above is a `notes/` finding awaiting promotion.
  `docs/tasks.md`, `docs/content-menu.md`, `docs/workstreams.md`, `docs/backlog.md` and
  `docs/gap-register.md` all still carry figures this note contradicts.

### Numbers in this note I would not bet on

- The **line counts** for carriers are ServUO lines. ModernUO's source-generated
  serialization makes ported code shorter; treat them as upper bounds.
- The **member-ownership index** is a regex, not a C# parser. It answers "which file owns
  this name" well enough to bucket, and it will misfile some names.
- The **`in-row` bucket** assumes a row is ported as a batch. Port one file alone and its
  in-row dependencies become co-port cost.
- **`docs/content-menu.md`'s `dep%` column is not reproduced here** and I did not check it.
  Given that its file counts turned out to be weak-filtered rather than raw, its percentages
  deserve the same scrutiny and have not had it.

---

## 11. Reproducing this

The scripts are throwaway, as S3's were; the definitions are not. In order: index all three
trees (types, members, identifiers, comment- and string-stripped, `using`/`namespace` lines
removed); filter each row's directories by primary type; bucket the residual names by owner;
subtract EQUIV, CONVERT and DELETABLE with a citation for each. The regression check is that
the filter must return **3,134 of 6,144** before anything else is trusted.

Row directory definitions used, so the next measurement can disagree precisely:

| Row | `ServUO-pub57/Scripts/…` |
|---|---|
| CC4 | `Services/Revamped Dungeons` |
| Artifacts + equipment | `Items/Artifacts`, `Items/Equipment` |
| CC7 (the 297) | `Items/Addons`, `Items/Decorative`, `Services/New Magincia` |
| CC7 extra | `Items/Resource`, `Services/BulkOrders` |
| CC5 | `Services/Expansions/High Seas/Items`, `Services/Expansions/High Seas/Mobiles` |

---
## Appendix — every file list behind every count

Paths are relative to `D:\UO\ServUO-pub57\Scripts`. Buckets are defined in §2.


### CC4 Revamped Dungeons

Prefixes: `Services/Revamped Dungeons`  
raw 255 → filtered out 0 → candidates 255  
drops straight in 31 · needs another row file 25 · co-port 140 · upstream/carrier 59


#### CC4 Revamped Dungeons — drops straight in (31 files)

```
Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/InvasionDefinition.cs
Services/Revamped Dungeons/BlackthornDungeon/Items/BlackthornPainting.cs
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Common.cs
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/CovetousCreature.cs
Services/Revamped Dungeons/Covetous Void Spawn/Items/CauldronOfTransmutation.cs
Services/Revamped Dungeons/Covetous Void Spawn/Items/HarvestMap.cs
Services/Revamped Dungeons/Covetous Void Spawn/Items/MagicFishFinder.cs
Services/Revamped Dungeons/Covetous Void Spawn/Items/SmeltersTalisman.cs
Services/Revamped Dungeons/Covetous Void Spawn/Items/TemporaryForge.cs
Services/Revamped Dungeons/Covetous Void Spawn/Items/WoodsmanTalisman.cs
Services/Revamped Dungeons/Covetous Void Spawn/WaveInfo.cs
Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusAlterAddon.cs
Services/Revamped Dungeons/TheExodusEncounter/Loot/Asclepius.cs
Services/Revamped Dungeons/TheExodusEncounter/Loot/BracersofAlchemicalDevastation.cs
Services/Revamped Dungeons/TheExodusEncounter/Loot/ClockworkLeggings.cs
Services/Revamped Dungeons/TheExodusEncounter/Loot/HygieiasAmulet.cs
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/ExodusZealot.cs   [deletable: SetWearable]
Services/Revamped Dungeons/TheExodusEncounter/Resources/GoldDust.cs
Services/Revamped Dungeons/TheExodusEncounter/Resources/NexusCore.cs
Services/Revamped Dungeons/TheExodusEncounter/Resources/SmallPieceofBlackrock.cs
Services/Revamped Dungeons/WrongDungeon/Items/MysteriousTunnel.cs
Services/Revamped Dungeons/WrongDungeon/Items/Soap.cs
Services/Revamped Dungeons/WrongDungeon/Items/WrongMazeWall.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/Archmage.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/BrigandCannibal.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/CaveTrollWrong.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/HungryOgre.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/LizardmanDefender.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/LizardmanSquatter.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/PrisonRat.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/SavagePackWolf.cs
```


#### CC4 Revamped Dungeons — portable once other files in this row come with it (25 files)

```
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Elementals.cs  <- CovetousCreature
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Repond.cs  <- CovetousCreature
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Undead.cs  <- CovetousCreature
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Vela.cs  <- BlightOfTheTundra, BraceletOfProtection, GargishBlightOfTheTundra, GargishHephaestus, Hephaestus, VoidPoolRewardGump
Services/Revamped Dungeons/Covetous Void Spawn/Items/BestWaveBoard.cs  <- BestWave, InstanceFel, InstanceTram, ScoreType, ScoresGump, VoidPoolController
Services/Revamped Dungeons/Covetous Void Spawn/Region.cs  <- CovetousCreature, DropRandomArtifact, OnCreatureKilled, OnGoing, VoidPoolController, VoidPoolRewards, VoidSpawn
Services/Revamped Dungeons/Covetous Void Spawn/VoidPoolStats.cs  <- CurrentScore, InstanceTram, VoidPoolController, Wave
Services/Revamped Dungeons/Shame Revamped/Items/CorrosiveAsh.cs  <- CursedOilstone, QuartzGrit, WhetstoneOfEnervation
Services/Revamped Dungeons/Shame Revamped/Items/CursedOilstone.cs  <- CorrosiveAsh, QuartzGrit, WhetstoneOfEnervation
Services/Revamped Dungeons/Shame Revamped/Items/QuartzGrit.cs  <- CorrosiveAsh, CursedOilstone, WhetstoneOfEnervation
Services/Revamped Dungeons/Shame Revamped/ShameTeleporter.cs  <- ShameWall
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/DupresChampion.cs  <- ExodusChest, ExodusSacrificalDagger, ExodusSummoningAlter, ExodusSummoningRite, GiveRituelItem, RobeofRite
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/DupresKnight.cs  <- ExodusChest, GiveRituelItem
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/DupresSquire.cs  <- ExodusChest, GiveRituelItem
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/ExodusArchZealot.cs  <- ExodusSacrificalDagger, ExodusSacrificalGargishDagger
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/ExodusDrone.cs  <- ExodusChest, GiveRituelItem
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/ExodusJuggernaut.cs  <- ExodusChest, GiveRituelItem
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/ExodusMinionLord.cs  <- ExodusSacrificalDagger, ExodusSummoningAlter, ExodusSummoningRite, RobeofRite
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/ExodusSentinel.cs  <- ExodusChest, GiveRituelItem
Services/Revamped Dungeons/TheExodusEncounter/Region.cs  <- VerLorRegController
Services/Revamped Dungeons/WrongDungeon/Items/BedrollSpawner.cs  <- EnchantedHotItem, MysteriousTunnel, SpawnChests, WrongBedrollBase, WrongBedrollEast, WrongBedrollSouth
Services/Revamped Dungeons/WrongDungeon/Items/StinkingCauldron.cs  <- GooeyMaggots
Services/Revamped Dungeons/WrongDungeon/Items/WrongBedrolls.cs  <- MysteriousTunnel, MysteriousTunnels, Soap
Services/Revamped Dungeons/WrongDungeon/Mobile/Fezzik.cs  <- StinkingCauldron
Services/Revamped Dungeons/WrongDungeon/Mobile/WrongPrisoner.cs  <- EscortToWrongEntrance
```


#### CC4 Revamped Dungeons — needs ServUO files from outside this row (140 files)

```
Services/Revamped Dungeons/BlackthornDungeon/BlackthornRewards.cs  <- CollectionItem
Services/Revamped Dungeons/BlackthornDungeon/Generate.cs  <- DungeonHitchingPost
Services/Revamped Dungeons/BlackthornDungeon/Gumps.cs  <- BaseRewardGump, Blackthorn, DeductPoints, PointsSystem
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/EpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/FancyDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/FemaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/GargishEpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/GildedDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/HoodedRobeBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/MaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/PlainDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/RobeBearingTheCrestOfBlackthorn .cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/EpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/FancyDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/FemaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/GargishEpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/GildedDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/HoodedRobeBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/MaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/PlainDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/RobeBearingTheCrestOfBlackthorn .cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/EpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/FancyDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/FemaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/GargishEpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/GildedDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/HoodedRobeBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/MaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/PlainDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/RobeBearingTheCrestOfBlackthorn .cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/EpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/FancyDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/FemaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/GargishEpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/GildedDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/HoodedRobeBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/MaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/PlainDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/RobeBearingTheCrestOfBlackthorn .cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/EpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/FancyDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/FemaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/GargishEpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/GildedDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/HoodedRobeBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/MaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/PlainDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/RobeBearingTheCrestOfBlackthorn .cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CrimsonCinctureBase/LeatherNinjaBeltBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CrimsonCinctureBase/ObiBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CrimsonCinctureBase/WoodlandBeltBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/BandanaBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/BascinetBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/CircletBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/FeatheredHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/GargishEarringsBearingTheCrestOfBlackthorn.cs  <- Blackthorn, GargishEarrings, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/GargishGlassesBearingTheCrestOfBlackthorn.cs  <- Blackthorn, GargishGlasses, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/JesterHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/NorseHelmBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/PlateHelmBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/RoyalCircletBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/SkullcapBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/TricorneHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/FoldedSteelBase/WizardsHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/BandanaBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/BascinetBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/CircletBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/FeatheredHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/GargishEarringsBearingTheCrestOfBlackthorn.cs  <- Blackthorn, GargishEarrings, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/GargishGlassesBearingTheCrestOfBlackthorn.cs  <- Blackthorn, GargishGlasses, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/JesterHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/NorseHelmBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/PlateHelmBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/RoyalCircletBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/SkullcapBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/TricorneHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MaceAndShieldBase/WizardsHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/EpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/FancyDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/FemaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/GargishEpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/GildedDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/HoodedRobeBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/MaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/PlainDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/RobeBearingTheCrestOfBlackthorn .cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/BandanaBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/BascinetBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/CircletBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/FeatheredHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/GargishEarringsBearingTheCrestOfBlackthorn.cs  <- Blackthorn, GargishEarrings, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/GargishGlassesBearingTheCrestOfBlackthorn.cs  <- Blackthorn, GargishGlasses, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/JesterHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/NorseHelmBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/PlateHelmBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/RoyalCircletBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/SkullcapBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/TricorneHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/NightEyesBase/WizardsHatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/QuiverOfInfinityBase/CloakBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RoyalBritannianBase/DoubletBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RoyalBritannianBase/SurcoatBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RoyalBritannianBase/TunicBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RuneBeetleCarapaceBase/ChainmailTunicBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RuneBeetleCarapaceBase/DragonBreastplateBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RuneBeetleCarapaceBase/GargishPlatemailChestBearingTheCrestOfBlackthorn.cs  <- Blackthorn, GargishPlateChest, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RuneBeetleCarapaceBase/GargishStoneChestBearingTheCrestOfBlackthorn.cs  <- Blackthorn, GargishStoneChest, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RuneBeetleCarapaceBase/PlatemailTunicBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RuneBeetleCarapaceBase/RingmailTunicBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/EpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/FancyDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/FemaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/GargishEpauletteBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/GildedDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/HoodedRobeBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/MaleKimonoBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/PlainDressBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/RobeBearingTheCrestOfBlackthorn .cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/TangleBase/LeatherNinjaBeltBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/TangleBase/ObiBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/TangleBase/WoodlandBeltBearingTheCrestOfBlackthorn.cs  <- Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/Covetous Void Spawn/Generate.cs  <- DoRespawn, SpawnObject, SpawnObjects, WeakEntityCollection, XmlSpawner
Services/Revamped Dungeons/Covetous Void Spawn/Gumps.cs  <- BaseRewardGump, CollectionItem, DeductPoints, PointsSystem, VoidPool
Services/Revamped Dungeons/Covetous Void Spawn/Items/PrismaticLenses.cs  <- GargishGlasses, Glasses
Services/Revamped Dungeons/Covetous Void Spawn/Items/VoidPoolRewards.cs  <- CollectionItem
Services/Revamped Dungeons/Shame Revamped/Generate.cs  <- DoRespawn, WeakEntityCollection, XmlSpawner
Services/Revamped Dungeons/Shame Revamped/Items/WhetstoneOfEnervation.cs  <- TimesImbued
Services/Revamped Dungeons/Shame Revamped/ShameAltar.cs  <- DeductPoints, PointsSystem, ShameCrystals
Services/Revamped Dungeons/Shame Revamped/ShameCrystal.cs  <- PointsSystem, ShameCrystals
Services/Revamped Dungeons/Shame Revamped/ShameWall.cs  <- WeakEntityCollection
Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusSummoningAltar.cs  <- BaseDecayingItem
Services/Revamped Dungeons/TheExodusEncounter/Items/ExoticToolkit.cs  <- BaseDecayingItem, NexusComponent
Services/Revamped Dungeons/TheExodusEncounter/Items/KeypunchReader.cs  <- NexusAddonDeed
Services/Revamped Dungeons/TheExodusEncounter/Items/MechanicalComponent.cs  <- BaseDecayingItem
Services/Revamped Dungeons/TheExodusEncounter/Items/PunchCard.cs  <- BaseDecayingItem
Services/Revamped Dungeons/TheExodusEncounter/Loot/GargishAsclepius.cs  <- GargishGnarledStaff
Services/Revamped Dungeons/TheExodusEncounter/Loot/GargishBracersofAlchemicalDevastation.cs  <- GargishLeatherArms
Services/Revamped Dungeons/TheExodusEncounter/Loot/GargishClockworkLeggings.cs  <- GargishPlateLegs
Services/Revamped Dungeons/WrongDungeon/Generate.cs  <- XmlSpawner
Services/Revamped Dungeons/WrongDungeon/Quests/EscortToWrongEntrance.cs  <- AddReward, BaseQuest
```


#### CC4 Revamped Dungeons — needs an upstream member, a carrier, or reading (59 files)

```
Services/Revamped Dungeons/BlackthornDungeon/Creatures/AgentoftheCrown.cs  <- upstream: Epaulette | also needs: BaseTurnInMobile, Blackthorn, PointsSystem, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/Creatures.cs  <- upstream: IsCursed, SetAreaEffect | unknown: AI_Mystic, AI_NecroMage, AI_Ninja, AI_Paladin, AI_Samurai, AI_Spellweaving | also needs: AbilityProfile, AreaEffect, AuraOfEnergy, SpecialAbility
Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/InvasionBeacon.cs  <- unknown: Easy | also needs: ItemLevel
Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/InvasionController.cs  <- upstream: IsStygian, RealLuck | unknown: Dragons, Elemental, GetRandomSpawnPoint, Undead, XmlSpawner2 | also needs: AttachTo, Destroyed, GenerateRandomItem, NewMagincia, ReforgedPrefix, ReforgedSuffix, RunicReforging, WolfSpider, XmlAttach, XmlData
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/GargishFancyBearingTheCrestOfBlackthorn.cs  <- upstream: GargishFancyRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfDeathBase/GargishRobeBearingTheCrestOfBlackthorn.cs  <- upstream: GargishRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/GargishFancyBearingTheCrestOfBlackthorn.cs  <- upstream: GargishFancyRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfLifeBase/GargishRobeBearingTheCrestOfBlackthorn.cs  <- upstream: GargishRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/GargishFancyBearingTheCrestOfBlackthorn.cs  <- upstream: GargishFancyRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfPowerBase/GargishRobeBearingTheCrestOfBlackthorn.cs  <- upstream: GargishRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/GargishFancyBearingTheCrestOfBlackthorn.cs  <- upstream: GargishFancyRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CloakOfSilenceBase/GargishRobeBearingTheCrestOfBlackthorn.cs  <- upstream: GargishRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/GargishFancyBearingTheCrestOfBlackthorn.cs  <- upstream: GargishFancyRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ConjurersGarbBase/GargishRobeBearingTheCrestOfBlackthorn.cs  <- upstream: GargishRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/CrimsonCinctureBase/GargishHalfApronBearingTheCrestOfBlackthorn.cs  <- upstream: GargoyleHalfApron | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/DecorativeShardShields.cs  <- unknown: Dragable
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/GargishFancyBearingTheCrestOfBlackthorn.cs  <- upstream: GargishFancyRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/MysticsGarbBase/GargishRobeBearingTheCrestOfBlackthorn.cs  <- upstream: GargishRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/QuiverOfInfinityBase/GargishClothWingArmorBearingTheCrestOfBlackthorn.cs  <- upstream: GargishClothWingArmor | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/RoyalBritannianBase/GargishSashBearingTheCrestOfBlackthorn.cs  <- upstream: GargishSash | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/GargishFancyBearingTheCrestOfBlackthorn.cs  <- upstream: GargishFancyRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/ShroudOfTheCondemnedBase/GargishRobeBearingTheCrestOfBlackthorn.cs  <- upstream: GargishRobe | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Items/TangleBase/GargishHalfApronBearingTheCrestOfBlackthorn.cs  <- upstream: GargoyleHalfApron | also needs: Blackthorn, ReforgedSuffix
Services/Revamped Dungeons/BlackthornDungeon/Region.cs  <- upstream: Allured | also needs: AVisitToCastleBlackthornQuest, FellowshipData, PointsSystem
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Abyss.cs  <- upstream: SetSpecialAbility | unknown: AI_Necro | also needs: AngryFire, SpecialAbility
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Cora.cs  <- upstream: SetAreaEffect, SetSpecialAbility | unknown: AnimationType, Despise, Services, TownCryer | also needs: AreaEffect, ArtifactChance, DespiseBoss, DragonBreath, IAuraCreature, IElementalCreature, Siege, SiegeShard, SpecialAbility, TownCryerSystem, UnderMysteriousPotionEffects
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Reptile.cs  <- unknown: AI_Necro
Services/Revamped Dungeons/Covetous Void Spawn/Items/BlightOfTheTundra.cs  <- upstream: NegativeAttributes
Services/Revamped Dungeons/Covetous Void Spawn/Items/BraceletOfProtection.cs  <- upstream: NegativeAttributes
Services/Revamped Dungeons/Covetous Void Spawn/Items/Brightblade.cs  <- upstream: SplinteringWeapon | also needs: GargishKatana
Services/Revamped Dungeons/Covetous Void Spawn/Items/Hephaestus.cs  <- upstream: NegativeAttributes | also needs: LargePlateShield
Services/Revamped Dungeons/Covetous Void Spawn/Level3Spawner.cs  <- unknown: GetRandomSpawnPoint, Stuff
Services/Revamped Dungeons/Covetous Void Spawn/VoidPoolController.cs  <- upstream: NoLootOnDeath, RemoveSpawned | unknown: Elemental, Reptile, Undead | also needs: AForcedSacraficeQuest, CompleteQuest, GetQuest, PointsSystem, QuestHelper, VoidPool, XmlSpawner
Services/Revamped Dungeons/DespiseRevamped/AI.cs  <- unknown: Defensive | also needs: Aggression, Aggressive, Alignment, Anchor, DespiseBoss, DespiseCreature, GetAnchorActual, GetLeashLength, Orb
Services/Revamped Dungeons/DespiseRevamped/DespiseController.cs  <- unknown: Good, LoginEventHandler, OnEnterRegionEventArgs, Stuff | also needs: AdrianTheGloriousLord, Alignment, Anchor, AndrosTheDreadLord, Conscripted, ConvertFromOldSystem, DespiseBoss, DespiseCreature, DespiseCrystals, DoRespawn, GateTeleporter, Login, Neutral, Orb, Orbs, PointsSystem, SpawnObjects, WeakEntityCollection, WispOrb, XmlSpawner
Services/Revamped Dungeons/DespiseRevamped/Region.cs  <- unknown: Good | also needs: Alignment, CorruptedWisp, DespiseBoss, DespiseCreature, EnsorcledWisp, MaxPower, Neutral, Orb, Orbs, Progress, PutridHeart, TeleportPet, WhisperingWithWispsQuest, WispOrb
Services/Revamped Dungeons/DespiseRevamped/Setup.cs  <- unknown: Good | also needs: Alignment, DespiseAnkh, DespiseTeleporter, GateTeleporter, MysteriousWisp, WeakEntityCollection
Services/Revamped Dungeons/Shame Revamped/Mobiles/Bosses.cs  <- upstream: SetAreaEffect, SetSpecialAbility | also needs: AreaEffect, DragonBreath, IAuraCreature, SpecialAbility
Services/Revamped Dungeons/Shame Revamped/Mobiles/Creatures.cs  <- upstream: SetAreaEffect, SetSpecialAbility, SetWeaponAbility | unknown: AI_Mystic, BodyValue | also needs: AreaEffect, BlackPowder, Charcoal, ColossalRage, DragonBreath, IAuraCreature, LifeLeech, Potash, Saltpeter, SearingWounds, SpecialAbility, StickySkin, VoidCore
Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusChest.cs  <- upstream: IRevealableItem, RandomEssence
Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusNexus.cs  <- unknown: TwoFiftyMS | also needs: NexusAddon
Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusSacrificalDagger.cs  <- upstream: OneSecond, UseSummoningRite
Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusSummoningRite.cs  <- upstream: UseSummoningRite | also needs: BaseDecayingItem
Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusTomeAltar.cs  <- unknown: Dragable | also needs: BaseDecayingItem
Services/Revamped Dungeons/TheExodusEncounter/Items/RobeofRite.cs  <- upstream: OneSecond
Services/Revamped Dungeons/TheExodusEncounter/Loot/DupresSword.cs  <- upstream: HitManaDrain
Services/Revamped Dungeons/TheExodusEncounter/Loot/GargishDupresSword.cs  <- upstream: HitManaDrain | also needs: StoneWarSword
Services/Revamped Dungeons/TheExodusEncounter/Loot/ScrollofValiantCommendation.cs  <- upstream: HasValiantStatReward
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/ClockworkExodus.cs  <- upstream: SetAreaEffect, SetWeaponAbility | unknown: AI_Mystic | also needs: AreaEffect, AuraOfEnergy
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/DeathVortex.cs  <- unknown: IsStaff, OneMinute
Services/Revamped Dungeons/TheExodusEncounter/VerLorRegController.cs  <- unknown: WriteMobile
Services/Revamped Dungeons/WrongDungeon/EnchantedHotItem.cs  <- upstream: AssassinHoned | unknown: AttachSocket | also needs: EnchantedHotItemSocket, ExtendedWeaponAttributes, GenerateRandomItem, RunicReforging
Services/Revamped Dungeons/WrongDungeon/Items/Artifacts/BlanketOfDarknessArtifact.cs  <- upstream: BlanketOfDarknessLogout
Services/Revamped Dungeons/WrongDungeon/Items/Artifacts/TortureRackArtifact.cs  <- unknown: IArtifact
Services/Revamped Dungeons/WrongDungeon/Items/WrongBarredMetalDoor.cs  <- upstream: OneSecond | also needs: IMageUnlockable
Services/Revamped Dungeons/WrongDungeon/Mobile/BrigandCannibalMage.cs  <- upstream: SetSpecialAbility | unknown: AI_NecroMage | also needs: LifeLeech, SpecialAbility
Services/Revamped Dungeons/WrongDungeon/Mobile/DemonicJailor.cs  <- unknown: Hashtable, SpeedControlType
Services/Revamped Dungeons/WrongDungeon/Mobile/GooeyMaggots.cs  <- upstream: OneSecond | unknown: FiveSeconds, IsStaff, SelfDeleteTimer, SpeedControlType
Services/Revamped Dungeons/WrongDungeon/Region.cs  <- unknown: IDamageable
```


#### CC4 Revamped Dungeons — extra ServUO files the co-port bucket pulls in (80 files)

```
Abilities/Enhancement.cs
Gumps/BaseRewardGump.cs
Gumps/Traps/CircuitTrap.cs
Items/Addons/DungeonHitchingPost.cs
Items/Addons/NexusAddon.cs
Items/Artifacts/Equipment/Armor/Sets/Epiphany/VillainousEpiphany.cs
Items/Artifacts/Equipment/Armor/Sets/Epiphany/VirtuousEpiphany.cs
Items/Artifacts/Equipment/Glasses/GargishGlasses.cs
Items/Artifacts/Equipment/Glasses/Glasses.cs
Items/Damageable/DamageableItem.cs
Items/Equipment/Armor/GargishLeatherArms.cs
Items/Equipment/Armor/GargishPlateChest.cs
Items/Equipment/Armor/GargishPlateLegs.cs
Items/Equipment/Armor/GargishStoneChest.cs
Items/Equipment/Armor/LargePlateShield.cs
Items/Equipment/Jewelry/GargishEarrings.cs
Items/Equipment/Weapons/GargishGnarledStaff.cs
Items/Equipment/Weapons/GargishKatana.cs
Items/Equipment/Weapons/StoneWarSword.cs
Items/Functional/BaseDecayingItem.cs
Items/Functional/CircuitTrapTrainingKit.cs
Items/Functional/DespiseAnkh.cs
Items/Internal/DespiseTeleporter.cs
Items/Internal/ItemSockets/EnchantedHotItem.cs
Items/Quest/PutridHeart.cs
Items/Quest/WispOrb.cs
Items/Resource/VoidCore.cs
Misc/Aggression.cs
Misc/Siege.cs
Misc/WeakEntityCollection.cs
Mobiles/Bosses/DespiseBosses.cs
Mobiles/Event/BaneDragon.cs
Mobiles/MobileInterfaces.cs
Mobiles/NPCs/BaseTurnInMobile.cs
Mobiles/NPCs/MysteriousWisp.cs
Mobiles/Normal/DespiseCreature.cs
Mobiles/Normal/WolfSpider.cs
Quests/BaseQuest.cs
Quests/Eodon/Valley of One Quest/TigerCubEnclosure.cs
Quests/The Ritual/Items.cs
Services/BulkOrders/BulkOrderSystem.cs
Services/City Loyalty System/CityLoyaltySystem.cs
Services/CommunityCollections/CollectionItem.cs
Services/Expansions/High Seas/Items/Resources/BlackPowder.cs
Services/Expansions/High Seas/Items/Resources/Charcoal.cs
Services/Expansions/High Seas/Items/Resources/Potash.cs
Services/Expansions/High Seas/Items/Resources/SaltPeter.cs
Services/Expansions/High Seas/Quests/ProfessionalBountyQuest/Mobiles/BaseShipCaptain.cs
Services/Expansions/High Seas/Quests/ProfessionalBountyQuest/Mobiles/MerchantCaptain.cs
Services/LootGeneration/Imbuing/Core/Imbuing.cs
Services/LootGeneration/RandomItemGenerator.cs
Services/LootGeneration/RunicReforging/RunicReforging.cs
Services/MondainsLegacyQuests/Helpers/QuestHelper.cs
Services/MondainsLegacyQuests/TierQuest.cs
Services/Pet Training/AbilityProfile.cs
Services/Pet Training/AreaEffects.cs
Services/Pet Training/Gumps.cs
Services/Pet Training/SpecialAbility.cs
Services/PointsSystems/DespiseCrystals.cs
Services/PointsSystems/FellowshipData.cs
Services/PointsSystems/PlayerMobileProps.cs
Services/PointsSystems/PointsSystem.cs
Services/PointsSystems/ShameCrystals.cs
Services/PointsSystems/VoidPool.cs
Services/RemoteAdmin/Packets.cs
Services/Spawner/SpawnObject.cs
Services/Town Cryer/Quests/APleaFromMinocQuest.cs
Services/Town Cryer/Quests/AVisitToCastleBlackthornQuest.cs
Services/Town Cryer/Quests/BuriedRichesQuest.cs
Services/Town Cryer/Quests/ExploringTheDeepQuest.cs
Services/Town Cryer/Quests/PaladinsOfTrinsic.cs
Services/Town Cryer/Quests/RightingWrongQuest.cs
Services/Town Cryer/Quests/WishesOfTheWispsQuest.cs
Services/Town Cryer/TownCryerSystem.cs
Services/Underworld/ExperimentalRoom/ExperimentalGem.cs
Services/Underworld/PuzzleRoom/MazePuzzleItem.cs
Services/XmlSpawner/XmlSpawner Core/XmlAttach/XmlAttach.cs
Services/XmlSpawner/XmlSpawner Core/XmlAttachments/XmlData.cs
Services/XmlSpawner/XmlSpawner Core/XmlSpawner2.cs
Spells/Third/Unlock.cs
```


#### CC4 Revamped Dungeons — filtered out at step 1: ModernUO or our tree already declares the primary type (0 files)

```
```


### Artifacts + equipment

Prefixes: `Items/Artifacts`, `Items/Equipment`  
raw 1022 → filtered out 567 → candidates 455  
drops straight in 320 · needs another row file 81 · co-port 10 · upstream/carrier 44


#### Artifacts + equipment — drops straight in (320 files)

```
Items/Artifacts/Consumables/ElixirofAgapiteConversion.cs
Items/Artifacts/Consumables/ElixirofGoldConversion.cs
Items/Artifacts/Consumables/ElixirofMetalConversion.cs
Items/Artifacts/Consumables/ElixirofValoriteConversion.cs
Items/Artifacts/Consumables/ElixirofVeriteConversion.cs
Items/Artifacts/Consumables/GobletOfCelebration.cs
Items/Artifacts/Consumables/GrapeBunch.cs
Items/Artifacts/Consumables/InfusedAlchemistsGem.cs
Items/Artifacts/Decorative/BakeKitsuneStatue.cs
Items/Artifacts/Decorative/ChangelingStatue.cs
Items/Artifacts/Decorative/CoffinPiece.cs
Items/Artifacts/Decorative/CollectionsBritLibraryMisc.cs
Items/Artifacts/Decorative/CreepingVine.cs
Items/Artifacts/Decorative/FerretImprisonedInCrystal.cs
Items/Artifacts/Decorative/FigureheadOfBmvArarat.cs
Items/Artifacts/Decorative/GildedStatue.cs
Items/Artifacts/Decorative/KingsPainting.cs
Items/Artifacts/Decorative/LargeFishingNet.cs
Items/Artifacts/Decorative/LordBritishThroneAddon.cs
Items/Artifacts/Decorative/MLDecorationArtifacts.cs
Items/Artifacts/Decorative/MapOfTheKnownWorld.cs
Items/Artifacts/Decorative/MedusaStatue.cs
Items/Artifacts/Decorative/MedusasFloorTileAddon.cs
Items/Artifacts/Decorative/MummifiedCorpse.cs
Items/Artifacts/Decorative/PolarBearStatue.cs
Items/Artifacts/Decorative/QuagmireStatue.cs
Items/Artifacts/Decorative/ReptalonStatue.cs
Items/Artifacts/Decorative/SADecorationArtifacts.cs
Items/Artifacts/Decorative/SantaStatue.cs
Items/Artifacts/Decorative/ShipsBellOfBmvArarat.cs
Items/Artifacts/Decorative/SnakeStatue.cs
Items/Artifacts/Decorative/SternAnchorOfBmvArarat.cs
Items/Artifacts/Decorative/TenthAnniversarySculpture.cs
Items/Artifacts/Decorative/WolfStatue.cs
Items/Artifacts/Equipment/Armor/AnimatedLegsoftheInsaneTinker.cs
Items/Artifacts/Equipment/Armor/BasiliskHideBreastplate.cs
Items/Artifacts/Equipment/Armor/BronzedArmoroftheValkyrie.cs
Items/Artifacts/Equipment/Armor/CrownOfArcaneTemperament.cs
Items/Artifacts/Equipment/Armor/DefenderOfTheMagus.cs
Items/Artifacts/Equipment/Armor/GauntletsOfAnger.cs
Items/Artifacts/Equipment/Armor/HumanFeyLeggings.cs
Items/Artifacts/Equipment/Armor/HumanSignOfChaos.cs
Items/Artifacts/Equipment/Armor/HumanSignOfOrder.cs
Items/Artifacts/Equipment/Armor/KelpWovenLeggings.cs
Items/Artifacts/Equipment/Armor/LightsRampart.cs
Items/Artifacts/Equipment/Armor/MuseumArmor.cs
Items/Artifacts/Equipment/Armor/MysticsGuard.cs
Items/Artifacts/Equipment/Armor/ProtectoroftheBattleMage.cs
Items/Artifacts/Equipment/Armor/ResonantShieldOfVengeance.cs
Items/Artifacts/Equipment/Armor/RoyalZooLeatherArmor.cs
Items/Artifacts/Equipment/Armor/RoyalZooPlateArmor.cs
Items/Artifacts/Equipment/Armor/RoyalZooStuddedArmor.cs
Items/Artifacts/Equipment/Armor/Sets/Acolyte/GreymistArms.cs
Items/Artifacts/Equipment/Armor/Sets/Acolyte/GreymistChest.cs
Items/Artifacts/Equipment/Armor/Sets/Acolyte/GreymistGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Acolyte/GreymistLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Assassin/AssassinArms.cs
Items/Artifacts/Equipment/Armor/Sets/Assassin/AssassinChest.cs
Items/Artifacts/Equipment/Armor/Sets/Assassin/AssassinGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Assassin/AssassinLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Bestial/BeastialSetHelper.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodChest.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodCrown.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodGauntlets.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodLeggings.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodPauldrons.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleGauntlets.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleGreaves.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleTunic.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleVambraces.cs
Items/Artifacts/Equipment/Armor/Sets/Hunter/HuntersArms.cs
Items/Artifacts/Equipment/Armor/Sets/Hunter/HuntersGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Hunter/HuntersLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Hunter/HuntersTunic.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationArms.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationCap.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationChest.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Juggernaut/Evocaricus.cs
Items/Artifacts/Equipment/Armor/Sets/Juggernaut/MalekisHonor.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsBascinet.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsCloseHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsFemalePlateChest.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsNorseHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateArms.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateChest.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Luck/EtoileBleue.cs
Items/Artifacts/Equipment/Armor/Sets/Luck/LuneRouge.cs
Items/Artifacts/Equipment/Armor/Sets/Luck/NovoBleue.cs
Items/Artifacts/Equipment/Armor/Sets/Luck/SoleilRouge.cs
Items/Artifacts/Equipment/Armor/Sets/Mage/LeafweaveChest.cs
Items/Artifacts/Equipment/Armor/Sets/Mage/LeafweaveGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Mage/LeafweaveLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Mage/LeafweavePauldrons.cs
Items/Artifacts/Equipment/Armor/Sets/Marksman/Feathernock.cs
Items/Artifacts/Equipment/Armor/Sets/Marksman/Swiftflight.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonArms.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonBascinet.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonChest.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathArms.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathBoneHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathChest.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinArms.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinChest.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixArms.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixChest.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutArms.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutBustier.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutChest.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutCirclet.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutFemaleChest.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutSmallPlateJingasa.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererArms.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererChest.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererFemaleChest.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererHat.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererSkirt.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/CompassionArms.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/HonestyGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/HonorLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/HumilityCloak.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/JusticeBreastplate.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/SacrificeSollerets.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososCap.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososCollar.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososKidGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososTunic.cs
Items/Artifacts/Equipment/Armor/ShroudOfDeciet.cs
Items/Artifacts/Equipment/Armor/TongueoftheBeast.cs
Items/Artifacts/Equipment/Armor/ValkryieArmor.cs
Items/Artifacts/Equipment/Armor/WallOfHungryMouths.cs
Items/Artifacts/Equipment/Armor/WardedDemonboneBracers.cs
Items/Artifacts/Equipment/Clothing/AnniversaryRobe.cs
Items/Artifacts/Equipment/Clothing/AntiqueWeddingDress.cs
Items/Artifacts/Equipment/Clothing/CloakOfDeath.cs
Items/Artifacts/Equipment/Clothing/CloakOfLife.cs
Items/Artifacts/Equipment/Clothing/CloakOfPower.cs
Items/Artifacts/Equipment/Clothing/CloakOfSilence.cs
Items/Artifacts/Equipment/Clothing/ConjurersGarb.cs
Items/Artifacts/Equipment/Clothing/ConjurersGarbHarbringer.cs
Items/Artifacts/Equipment/Clothing/MagicalDoor.cs
Items/Artifacts/Equipment/Clothing/MarkOfTravesty.cs
Items/Artifacts/Equipment/Clothing/MysticsGarb.cs
Items/Artifacts/Equipment/Clothing/ObiDiEnse.cs
Items/Artifacts/Equipment/Clothing/RoyalGuardInvestigatorCloak.cs
Items/Artifacts/Equipment/Clothing/SashOfMight.cs
Items/Artifacts/Equipment/Clothing/ShroudOfTheCondemned.cs
Items/Artifacts/Equipment/Clothing/TheScholarsHalo.cs
Items/Artifacts/Equipment/Clothing/WardensArmorOfAugmentation.cs
Items/Artifacts/Equipment/Glasses/GargishGlasses.cs
Items/Artifacts/Equipment/Glasses/LegendaryMapmakersGlasses.cs
Items/Artifacts/Equipment/Instruments/DreadFlute.cs
Items/Artifacts/Equipment/Jewelry/AmuletOfRighteousness.cs
Items/Artifacts/Equipment/Jewelry/BarreraakRing.cs
Items/Artifacts/Equipment/Jewelry/BraceletOfPrimalConsumption.cs
Items/Artifacts/Equipment/Jewelry/BurningAmber.cs
Items/Artifacts/Equipment/Jewelry/CrystallineRing.cs
Items/Artifacts/Equipment/Jewelry/DemonBridleRing.cs
Items/Artifacts/Equipment/Jewelry/JadeArmband.cs
Items/Artifacts/Equipment/Jewelry/Lavaliere.cs
Items/Artifacts/Equipment/Jewelry/MuseumJewlery.cs
Items/Artifacts/Equipment/Jewelry/NecklaceofDiligence.cs
Items/Artifacts/Equipment/Jewelry/PetrifiedMatriarchsTongue.cs
Items/Artifacts/Equipment/Jewelry/TokenofHolyFavor.cs
Items/Artifacts/Equipment/Jewelry/TorcOfTheGuardians.cs
Items/Artifacts/Equipment/Jewelry/Venom.cs
Items/Artifacts/Equipment/Spellbooks/ClaininsSpellbook.cs
Items/Artifacts/Equipment/Spellbooks/ConjurersGrimoire.cs
Items/Artifacts/Equipment/Spellbooks/FallenMysticsSpellbook.cs
Items/Artifacts/Equipment/Spellbooks/ScrappersCompendium.cs
Items/Artifacts/Equipment/Weapons/AxeOfAbandon.cs
Items/Artifacts/Equipment/Weapons/AxesOfFury.cs
Items/Artifacts/Equipment/Weapons/BansheesCall.cs
Items/Artifacts/Equipment/Weapons/CavalrysFolly.cs
Items/Artifacts/Equipment/Weapons/ChannelersDefender.cs
Items/Artifacts/Equipment/Weapons/ClawsOfTheBerserker.cs
Items/Artifacts/Equipment/Weapons/DemonHuntersStandard.cs
Items/Artifacts/Equipment/Weapons/DraconisWrath.cs
Items/Artifacts/Equipment/Weapons/DreadsRevenge.cs
Items/Artifacts/Equipment/Weapons/EternalGuardianStaff.cs
Items/Artifacts/Equipment/Weapons/FNPitchfork.cs
Items/Artifacts/Equipment/Weapons/InfusedGlassStave.cs
Items/Artifacts/Equipment/Weapons/IronwoodCompositeBow.cs
Items/Artifacts/Equipment/Weapons/JadeWarAxe.cs
Items/Artifacts/Equipment/Weapons/LightInTheVoid.cs
Items/Artifacts/Equipment/Weapons/Mangler.cs
Items/Artifacts/Equipment/Weapons/ResonantStaffOfEnlightenment.cs
Items/Artifacts/Equipment/Weapons/RunedDriftwoodBow.cs
Items/Artifacts/Equipment/Weapons/ScepterOfTheChief.cs
Items/Artifacts/Equipment/Weapons/StaffOfResonance.cs
Items/Artifacts/Equipment/Weapons/StandardOfChaos.cs
Items/Artifacts/Equipment/Weapons/StandardOfChaosG.cs
Items/Artifacts/Equipment/Weapons/StoneSlithClaw.cs
Items/Artifacts/Equipment/Weapons/StormCaller.cs
Items/Artifacts/Equipment/Weapons/ValkyriesGlaive.cs
Items/Artifacts/Equipment/Weapons/WindOfCorruption.cs
Items/Artifacts/Talismans/FrostguardTalisman.cs
Items/Artifacts/Talismans/JadeSnakeHead.cs
Items/Artifacts/Tools/XenrrFishingPole.cs
Items/Equipment/Armor/AssassinsCowl.cs
Items/Equipment/Armor/DragonTurtleHideArms.cs
Items/Equipment/Armor/DragonTurtleHideBustier.cs
Items/Equipment/Armor/DragonTurtleHideChest.cs
Items/Equipment/Armor/DragonTurtleHideHelm.cs
Items/Equipment/Armor/DragonTurtleHideLegs.cs
Items/Equipment/Armor/ElegantCollar.cs
Items/Equipment/Armor/EvilOrcHelm.cs
Items/Equipment/Armor/FemaleGargishLeatherArms.cs
Items/Equipment/Armor/FemaleGargishLeatherChest.cs
Items/Equipment/Armor/FemaleGargishLeatherKilt.cs
Items/Equipment/Armor/FemaleGargishLeatherLegs.cs
Items/Equipment/Armor/FemaleGargishPlateArms.cs
Items/Equipment/Armor/FemaleGargishPlateChest.cs
Items/Equipment/Armor/FemaleGargishPlateKilt.cs
Items/Equipment/Armor/FemaleGargishPlateLegs.cs
Items/Equipment/Armor/FemaleGargishStoneArms.cs
Items/Equipment/Armor/FemaleGargishStoneChest.cs
Items/Equipment/Armor/FemaleGargishStoneKilt.cs
Items/Equipment/Armor/FemaleGargishStoneLegs.cs
Items/Equipment/Armor/GargishChaosShield.cs
Items/Equipment/Armor/GargishClothArmor.cs
Items/Equipment/Armor/GargishKiteShield.cs
Items/Equipment/Armor/GargishLeatherArms.cs
Items/Equipment/Armor/GargishLeatherChest.cs
Items/Equipment/Armor/GargishLeatherKilt.cs
Items/Equipment/Armor/GargishLeatherLegs.cs
Items/Equipment/Armor/GargishOrderShield.cs
Items/Equipment/Armor/GargishPlateArms.cs
Items/Equipment/Armor/GargishPlateChest.cs
Items/Equipment/Armor/GargishPlateKilt.cs
Items/Equipment/Armor/GargishPlateLegs.cs
Items/Equipment/Armor/GargishStoneArms.cs
Items/Equipment/Armor/GargishStoneChest.cs
Items/Equipment/Armor/GargishStoneKilt.cs
Items/Equipment/Armor/GargishStoneLegs.cs
Items/Equipment/Armor/LargePlateShield.cs
Items/Equipment/Armor/LargeStoneShield.cs
Items/Equipment/Armor/MagesHood.cs
Items/Equipment/Armor/MediumPlateShield.cs
Items/Equipment/Armor/SmallPlateShield.cs
Items/Equipment/Clothing/Arms.cs
Items/Equipment/Clothing/DaggerBelt.cs
Items/Equipment/Clothing/FirstAidBelt.cs
Items/Equipment/Clothing/Gargoyle Accessories.cs
Items/Equipment/Clothing/LeatherTalons.cs
Items/Equipment/Clothing/MaceBelt.cs
Items/Equipment/Clothing/PlateTalons.cs
Items/Equipment/Clothing/SwordBelt.cs
Items/Equipment/Instruments/AudChar.cs
Items/Equipment/Jewelry/BlueDiamondRing.cs
Items/Equipment/Jewelry/BrilliantAmberBracelet.cs
Items/Equipment/Jewelry/DarkSapphireBracelet.cs
Items/Equipment/Jewelry/EcruCitrineRing.cs
Items/Equipment/Jewelry/FireRubyBracelet.cs
Items/Equipment/Jewelry/GargishBracelet.cs
Items/Equipment/Jewelry/GargishEarrings.cs
Items/Equipment/Jewelry/GargishNecklace.cs
Items/Equipment/Jewelry/GargishRing.cs
Items/Equipment/Jewelry/PerfectEmeraldRing.cs
Items/Equipment/Jewelry/StaffRing.cs
Items/Equipment/Jewelry/TurqouiseRing.cs
Items/Equipment/Jewelry/WhitePearlBracelet.cs
Items/Equipment/Spellbooks/MysticBook.cs
Items/Equipment/Suits/BaseCostume.cs
Items/Equipment/Talismans/CollectionsBritLibraryTalismans.cs
Items/Equipment/Talismans/Slither.cs
Items/Equipment/Weapons/GargishAxe.cs
Items/Equipment/Weapons/GargishBardiche.cs
Items/Equipment/Weapons/GargishBattleAxe.cs
Items/Equipment/Weapons/GargishBoneHarvester.cs
Items/Equipment/Weapons/GargishButcherKnife.cs
Items/Equipment/Weapons/GargishCleaver.cs
Items/Equipment/Weapons/GargishDagger.cs
Items/Equipment/Weapons/GargishDaisho.cs
Items/Equipment/Weapons/GargishGnarledStaff.cs
Items/Equipment/Weapons/GargishKatana.cs
Items/Equipment/Weapons/GargishKryss.cs
Items/Equipment/Weapons/GargishLance.cs
Items/Equipment/Weapons/GargishMaul.cs
Items/Equipment/Weapons/GargishPike.cs
Items/Equipment/Weapons/GargishScythe.cs
Items/Equipment/Weapons/GargishTekagi.cs
Items/Equipment/Weapons/GargishTessen.cs
Items/Equipment/Weapons/GargishWarFork.cs
Items/Equipment/Weapons/GargishWarHammer.cs
Items/Equipment/Weapons/OrcishBow.cs
Items/Equipment/Weapons/PaladinSword.cs
Items/Equipment/Weapons/RandomWand.cs
Items/Equipment/Weapons/SerpentStoneStaff.cs
Items/Equipment/Weapons/Shortblade.cs
Items/Equipment/Weapons/SkullGnarledStaff.cs   [deletable: Alterable]
Items/Equipment/Weapons/SkullLongsword.cs   [deletable: Alterable]
Items/Equipment/Weapons/StoneWarSword.cs
```


#### Artifacts + equipment — portable once other files in this row come with it (81 files)

```
Items/Artifacts/Decorative/GrapeVine.cs  <- GrapeBunch
Items/Artifacts/DespiseArtifacts.cs  <- GargishWarFork, LeatherTalons
Items/Artifacts/Equipment/Armor/BritchesOfWarding.cs  <- GargishPlateLegs
Items/Artifacts/Equipment/Armor/CastOffZombieSkin.cs  <- GargishLeatherArms
Items/Artifacts/Equipment/Armor/CuffsOfTheArchmage.cs  <- GargishStoneArms
Items/Artifacts/Equipment/Armor/DragonHideShield.cs  <- GargishKiteShield
Items/Artifacts/Equipment/Armor/GargishSignOfChaos.cs  <- GargishChaosShield
Items/Artifacts/Equipment/Armor/GargishSignOfOrder.cs  <- GargishOrderShield
Items/Artifacts/Equipment/Armor/GlovesOfFeudalGrip.cs  <- GargishPlateKilt
Items/Artifacts/Equipment/Armor/PillarOfStrength.cs  <- LargeStoneShield
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialArms.cs  <- BestialSetHelper, GargishLeatherArms
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialEarrings.cs  <- BestialSetHelper, GargishEarrings
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialGloves.cs  <- BestialSetHelper
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialGorget.cs  <- BestialSetHelper
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialHelm.cs  <- BestialSetHelper
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialLegs.cs  <- BestialSetHelper
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialNecklace.cs  <- BestialSetHelper, GargishNecklace
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensBustier.cs  <- DragonTurtleHideBustier
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensHelm.cs  <- DragonTurtleHideHelm
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensLegs.cs  <- DragonTurtleHideLegs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensSleeves.cs  <- DragonTurtleHideArms
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensTunic.cs  <- DragonTurtleHideChest
Items/Artifacts/Equipment/Armor/Sets/Epiphany/VillainousEpiphany.cs  <- EpiphanyHelper, GargishEarrings, GargishNecklace, GargishPlateArms, GargishPlateChest, GargishPlateKilt, GargishPlateLegs, GetFrequency, IEpiphanyArmor, SurgeType
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationBag.cs  <- InitiationArms, InitiationCap, InitiationChest, InitiationGloves, InitiationGorget, InitiationLegs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixTicket.cs  <- PhoenixArms, PhoenixChest, PhoenixGloves, PhoenixGorget, PhoenixHelm, PhoenixLegs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososArmbands.cs  <- GargishPlateArms
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososEarpieces.cs  <- GargishEarrings
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososNecklace.cs  <- GargishNecklace
Items/Artifacts/Equipment/Armor/SpinedBloodwormBracers.cs  <- GargishClothArms
Items/Artifacts/Equipment/Armor/VoidInfusedKilt.cs  <- GargishPlateKilt
Items/Artifacts/Equipment/Clothing/RangersCloakOfAugmentation.cs  <- WardensArmorOfAugmentation
Items/Artifacts/Equipment/Glasses/CollectionsBritLibraryGlasses.cs  <- GargishGlasses, Glasses
Items/Artifacts/Equipment/Glasses/Glasses.cs  <- GargishGlasses
Items/Artifacts/Equipment/Glasses/NightEyes.cs  <- Glasses
Items/Artifacts/Equipment/Jewelry/DragonJadeEarrings.cs  <- GargishEarrings
Items/Artifacts/Equipment/Jewelry/ObsidianEarrings.cs  <- GargishEarrings
Items/Artifacts/Equipment/Weapons/BladeOfBattle.cs  <- Shortblade
Items/Artifacts/Equipment/Weapons/BreastplateOfTheBerserker.cs  <- GargishPlateChest
Items/Artifacts/Equipment/Weapons/GiantSteps.cs  <- GargishStoneLegs
Items/Artifacts/Equipment/Weapons/PetrifiedSnake.cs  <- SerpentStoneStaff
Items/Artifacts/Equipment/Weapons/StoneDragonsTooth.cs  <- GargishDagger
Items/Artifacts/Equipment/Weapons/TheRedeemer.cs  <- PaladinSword
Items/Equipment/Armor/CowlOfTheMaceAndShield.cs  <- AssassinsCowl
Items/Equipment/Armor/CrimsonDaggerBelt.cs  <- DaggerBelt
Items/Equipment/Armor/CrimsonMaceBelt.cs  <- MaceBelt
Items/Equipment/Armor/CrimsonSwordBelt.cs  <- SwordBelt
Items/Equipment/Armor/ElegantCollarOfFortune.cs  <- ElegantCollar
Items/Equipment/Armor/MagesHoodOfScholarlyInsight.cs  <- MagesHood
Items/Equipment/Suits/BloodwormCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/CentaurCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/CyclopsCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/DragonWolfCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/DrakeCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/DreamWraithCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/EtherealWarriorCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/ExodusMinionCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/FireElementalCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/GazerCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/GiantPixieCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/GiantToadCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/GoreFiendCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/LadyOfTheSnowCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/MaddeningHorrorCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/MinotaurCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/MongbatCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/OniCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/OphidianMatriarchCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/OphidianWarriorCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/PixieCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/SabertoothedTigerCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/SatyrCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/ShadowWyrmCostume.cs  <- BaseCostume, CostumeBody, CostumeHue
Items/Equipment/Suits/SkeletonCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/SkitteringHopperCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/SolenWarriorCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/TerathanWarriorCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/TitanCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/VoidWandererCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/WispCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/WolfSpiderCostume.cs  <- BaseCostume, CostumeBody
Items/Equipment/Suits/ZombieCostume.cs  <- BaseCostume, CostumeBody
```


#### Artifacts + equipment — needs ServUO files from outside this row (10 files)

```
Items/Artifacts/Decorative/CollectionStatuettes.cs  <- BaseStatuette
Items/Artifacts/Decorative/CollectionsBritLibraryQuotes.cs  <- BaseStatuette
Items/Artifacts/Decorative/MuseumStatues.cs  <- BaseStatuette
Items/Artifacts/Decorative/TragicRemainsOfTravesty.cs  <- BaseStatuette
Items/Artifacts/Equipment/Weapons/Abhorrence.cs  <- ExtendedWeaponAttributes
Items/Artifacts/Equipment/Weapons/AbyssReaver.cs  <- InheritsItem
Items/Artifacts/Equipment/Weapons/CaptainJohnesBlade.cs  <- ExtendedWeaponAttributes
Items/Artifacts/Equipment/Weapons/Glenda.cs  <- ExtendedWeaponAttributes
Items/Equipment/Clothing/Hats.cs  <- Reward
Items/Equipment/Clothing/Pants.cs  <- Reward
```


#### Artifacts + equipment — needs an upstream member, a carrier, or reading (44 files)

```
Items/Artifacts/Consumables/VialofArmorEssence.cs  <- upstream: TempDamageAbsorb
Items/Artifacts/Decorative/ImprisonedDog.cs  <- unknown: RemainEquiped
Items/Artifacts/Equipment/Armor/BouraTailShield.cs  <- upstream: ReactiveParalyze
Items/Artifacts/Equipment/Armor/CandlewoodTorch.cs  <- upstream: CheckRemove, SwarmContext
Items/Artifacts/Equipment/Armor/LordBlackthornsExemplar.cs  <- upstream: NegativeAttributes, NoRepair
Items/Artifacts/Equipment/Armor/MantleOfTheFallen.cs  <- upstream: GargishClothChest
Items/Artifacts/Equipment/Armor/SentinelsGuard.cs  <- upstream: NegativeAttributes, NoRepair
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialKilt.cs  <- upstream: GargishClothKilt
Items/Artifacts/Equipment/Armor/Sets/Epiphany/EpiphanyHelper.cs  <- unknown: Good
Items/Artifacts/Equipment/Armor/Sets/Epiphany/VirtuousEpiphany.cs  <- unknown: Good
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososKilt.cs  <- upstream: GargishClothKilt
Items/Artifacts/Equipment/Armor/SummonersKilt.cs  <- upstream: GargishClothKilt
Items/Artifacts/Equipment/Armor/SurgeShield.cs  <- upstream: Brittle
Items/Artifacts/Equipment/Clothing/RunedSashOfWarding.cs  <- upstream: Brittle
Items/Artifacts/Equipment/Clothing/ShadowCloakOfRejuvenation.cs  <- upstream: GargishClothWingArmor
Items/Artifacts/Equipment/Clothing/SpellFocusingSash.cs  <- upstream: Brittle, NegativeAttributes
Items/Artifacts/Equipment/Clothing/Tangle1.cs  <- upstream: GargoyleHalfApron
Items/Artifacts/Equipment/Jewelry/AnkhPendant.cs  <- unknown: Sacrafice
Items/Artifacts/Equipment/Weapons/AbyssalBlade.cs  <- upstream: HitFatigue, HitManaDrain
Items/Artifacts/Equipment/Weapons/BowOfTheInfiniteSwarm.cs  <- upstream: HitSwarm | also needs: ExtendedWeaponAttributes
Items/Artifacts/Equipment/Weapons/Craven.cs  <- upstream: BalancedWeapon
Items/Artifacts/Equipment/Weapons/DeathsHead.cs  <- upstream: HitFatigue
Items/Artifacts/Equipment/Weapons/DragonsEnd.cs  <- upstream: NegativeAttributes, NoRepair
Items/Artifacts/Equipment/Weapons/Equivocation.cs  <- upstream: BalancedWeapon, Brittle, HitCurse
Items/Artifacts/Equipment/Weapons/JaanasStaff.cs  <- upstream: NegativeAttributes, NoRepair
Items/Artifacts/Equipment/Weapons/KatrinasCrook.cs  <- upstream: NegativeAttributes, NoRepair
Items/Artifacts/Equipment/Weapons/LegacyOfDespair.cs  <- upstream: HitCurse
Items/Artifacts/Equipment/Weapons/LifeSyphon.cs  <- upstream: BloodDrinker
Items/Artifacts/Equipment/Weapons/MuseumWeapons.cs  <- upstream: RandomSuperSlayerAOS
Items/Artifacts/Equipment/Weapons/Pincer.cs  <- upstream: BalancedWeapon
Items/Artifacts/Equipment/Weapons/StaffOfShatteredDreams.cs  <- upstream: SplinteringWeapon
Items/Artifacts/Equipment/Weapons/SwordOfShatteredHopes.cs  <- upstream: SplinteringWeapon
Items/Artifacts/Equipment/Weapons/TheDeceiver.cs  <- upstream: HitSparks | also needs: ExtendedWeaponAttributes
Items/Artifacts/Equipment/Weapons/TheImpalersPick.cs  <- upstream: HitManaDrain
Items/Artifacts/Equipment/Weapons/VampiricEssence.cs  <- upstream: BloodDrinker
Items/Artifacts/Talismans/ConjurersTrinket.cs  <- unknown: Undead
Items/Equipment/Instruments/Cello.cs  <- upstream: InstrumentedAddonComponent
Items/Equipment/Instruments/Cowbell.cs  <- upstream: InstrumentedAddonComponent
Items/Equipment/Instruments/SnakeCharmerFlute.cs  <- upstream: BeginCharm, CharmMaster | also needs: CoralSnake
Items/Equipment/Instruments/Trumpet.cs  <- upstream: InstrumentedAddonComponent
Items/Equipment/Instruments/WallMountedBell.cs  <- upstream: InstrumentedAddonComponent
Items/Equipment/Spellbooks/BookOfMasteries.cs  <- upstream: GetMasteryFocusLevel | unknown: CurrentMastery, SkillMasteries | also needs: GetLocalization, MasteryInfo, MasterySelectionGump
Items/Equipment/Talismans/ManaPhasingOrb.cs  <- upstream: Brittle
Items/Equipment/Talismans/TalismanofGoblinSlaying.cs  <- unknown: Goblin
```


#### Artifacts + equipment — extra ServUO files the co-port bucket pulls in (14 files)

```
Abilities/Enhancement.cs
Items/Consumables/EngravingTools.cs
Items/Consumables/TastyTreat.cs
Items/Containers/FurnitureContainer.cs
Items/Decorative/BaseStatuette.cs
Items/Decorative/Utensils.cs
Mobiles/Normal/CoralSnake.cs
Services/CommunityCollections/BaseCollectionItem.cs
Services/CommunityCollections/BaseCollectionMobile.cs
Services/Expansions/Time Of Legends/Shadowguard/Controller.cs
Services/LootGeneration/Imbuing/Core/ImbuingDefinition.cs
Services/Pet Training/PetTrainingHelper.cs
Spells/Skill Masteries/Core/MasteryInfo.cs
Spells/Skill Masteries/Core/SelectMasteryGump.cs
```


#### Artifacts + equipment — filtered out at step 1: ModernUO or our tree already declares the primary type (567 files)

```
Items/Artifacts/Consumables/AdmiralsHeartyRum.cs
Items/Artifacts/Consumables/BasePigmentsOfTokuno.cs
Items/Artifacts/Consumables/Bleach.cs
Items/Artifacts/Consumables/HangoverCure.cs
Items/Artifacts/Decorative/AcademicBooks.cs
Items/Artifacts/Decorative/ArtifactLargeVase.cs
Items/Artifacts/Decorative/ArtifactVase.cs
Items/Artifacts/Decorative/BaseDecorationArtifact.cs
Items/Artifacts/Decorative/CandelabraOfSouls.cs
Items/Artifacts/Decorative/DemonSkull.cs
Items/Artifacts/Decorative/DirtPatch.cs
Items/Artifacts/Decorative/DoomDecorationArtifacts.cs
Items/Artifacts/Decorative/EvilIdolSkull.cs
Items/Artifacts/Decorative/Futon.cs
Items/Artifacts/Decorative/GhostShipAnchor.cs
Items/Artifacts/Decorative/GoldBricks.cs
Items/Artifacts/Decorative/LavaTile.cs
Items/Artifacts/Decorative/PhillipsWoodenSteed.cs
Items/Artifacts/Decorative/Pier.cs
Items/Artifacts/Decorative/SEDecorationArtifacts.cs
Items/Artifacts/Decorative/SeahorseStatuette.cs
Items/Artifacts/Decorative/ShipModelOfTheHMSCape.cs
Items/Artifacts/Decorative/SkullPole.cs
Items/Artifacts/Decorative/SwampTile.cs
Items/Artifacts/Decorative/TOLDecorationArtifacts.cs
Items/Artifacts/Decorative/TatteredAncientMummyWrapping.cs
Items/Artifacts/Decorative/WallBlood.cs
Items/Artifacts/Decorative/WaterTile.cs
Items/Artifacts/Decorative/Web.cs
Items/Artifacts/Decorative/WindSpirit.cs
Items/Artifacts/Equipment/Armor/Aegis.cs
Items/Artifacts/Equipment/Armor/AegisOfGrace.cs
Items/Artifacts/Equipment/Armor/ArcaneShield.cs
Items/Artifacts/Equipment/Armor/ArmorOfFortune.cs
Items/Artifacts/Equipment/Armor/ArmsOfArmstrong.cs
Items/Artifacts/Equipment/Armor/BrambleCoat.cs
Items/Artifacts/Equipment/Armor/BulwarkLeggings.cs
Items/Artifacts/Equipment/Armor/DupresShield.cs
Items/Artifacts/Equipment/Armor/EscutcheonDeAriadne.cs
Items/Artifacts/Equipment/Armor/FeyLeggings.cs
Items/Artifacts/Equipment/Armor/GargishWoodenShield.cs
Items/Artifacts/Equipment/Armor/GauntletsOfNobility.cs
Items/Artifacts/Equipment/Armor/GladiatorsCollar.cs
Items/Artifacts/Equipment/Armor/GlovesOfMining.cs
Items/Artifacts/Equipment/Armor/GlovesOfSafeguarding.cs
Items/Artifacts/Equipment/Armor/GlovesOfThePugilist.cs
Items/Artifacts/Equipment/Armor/HealersTouch.cs
Items/Artifacts/Equipment/Armor/HeartOfTheLion.cs
Items/Artifacts/Equipment/Armor/HelmOfInsight.cs
Items/Artifacts/Equipment/Armor/HelmOfSwiftness.cs
Items/Artifacts/Equipment/Armor/HolyKnightsBreastplate.cs
Items/Artifacts/Equipment/Armor/InquisitorsResolution.cs
Items/Artifacts/Equipment/Armor/IronwoodCrown.cs
Items/Artifacts/Equipment/Armor/JackalsCollar.cs
Items/Artifacts/Equipment/Armor/LeggingsOfBane.cs
Items/Artifacts/Equipment/Armor/LeggingsOfEmbers.cs
Items/Artifacts/Equipment/Armor/MidnightBracers.cs
Items/Artifacts/Equipment/Armor/OrcChieftainHelm.cs
Items/Artifacts/Equipment/Armor/OrcishVisage.cs
Items/Artifacts/Equipment/Armor/OrnateCrownOfTheHarrower.cs
Items/Artifacts/Equipment/Armor/SamuraiHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsBustier.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsLongSkirt.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsShorts.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsSkirt.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsTunic.cs
Items/Artifacts/Equipment/Armor/Sets/DaemonBone/DaemonArms.cs
Items/Artifacts/Equipment/Armor/Sets/DaemonBone/DaemonChest.cs
Items/Artifacts/Equipment/Armor/Sets/DaemonBone/DaemonGloves.cs
Items/Artifacts/Equipment/Armor/Sets/DaemonBone/DaemonHelm.cs
Items/Artifacts/Equipment/Armor/Sets/DaemonBone/DaemonLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Ranger/RangerArms.cs
Items/Artifacts/Equipment/Armor/Sets/Ranger/RangerChest.cs
Items/Artifacts/Equipment/Armor/Sets/Ranger/RangerGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Ranger/RangerGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Ranger/RangerLegs.cs
Items/Artifacts/Equipment/Armor/Sets/SetItem.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/SpiritualityHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/ValorGauntlets.cs
Items/Artifacts/Equipment/Armor/ShadowDancerLeggings.cs
Items/Artifacts/Equipment/Armor/ShieldOfInvulnerability.cs
Items/Artifacts/Equipment/Armor/SongWovenMantle.cs
Items/Artifacts/Equipment/Armor/SpellWovenBritches.cs
Items/Artifacts/Equipment/Armor/StitchersMittens.cs
Items/Artifacts/Equipment/Armor/TunicOfFire.cs
Items/Artifacts/Equipment/Armor/TunicOfGuarding.cs
Items/Artifacts/Equipment/Armor/TwilightJacket.cs
Items/Artifacts/Equipment/Armor/VioletCourage.cs
Items/Artifacts/Equipment/Armor/VoiceOfTheFallenKing.cs
Items/Artifacts/Equipment/Armor/WalkersLeggings.cs
Items/Artifacts/Equipment/Clothing/ANecromancerShroud.cs
Items/Artifacts/Equipment/Clothing/AcidProofRobe.cs
Items/Artifacts/Equipment/Clothing/BurglarsBandana.cs
Items/Artifacts/Equipment/Clothing/CaptainJohnsHat.cs
Items/Artifacts/Equipment/Clothing/CrimsonCincture.cs
Items/Artifacts/Equipment/Clothing/CrownOfTalKeesh.cs
Items/Artifacts/Equipment/Clothing/DetectiveBoots.cs
Items/Artifacts/Equipment/Clothing/DivineCountenance.cs
Items/Artifacts/Equipment/Clothing/DreadPirateHat.cs
Items/Artifacts/Equipment/Clothing/EmbroideredOakLeafCloak.cs
Items/Artifacts/Equipment/Clothing/HatOfTheMagi.cs
Items/Artifacts/Equipment/Clothing/HoodedShroudOfShadows.cs
Items/Artifacts/Equipment/Clothing/HuntersHeaddress.cs
Items/Artifacts/Equipment/Clothing/LieutenantOfTheBritannianRoyalGuard.cs
Items/Artifacts/Equipment/Clothing/PadsOfTheCuSidhe.cs
Items/Artifacts/Equipment/Clothing/PhilosophersHat.cs
Items/Artifacts/Equipment/Clothing/PolarBearMask.cs
Items/Artifacts/Equipment/Clothing/RobeOfTheEclipse.cs
Items/Artifacts/Equipment/Clothing/RobeOfTheEquinox.cs
Items/Artifacts/Equipment/Clothing/SamaritanRobe.cs
Items/Artifacts/Equipment/Clothing/SolesOfProvidence.cs
Items/Artifacts/Equipment/Clothing/SpiritOfTheTotem.cs
Items/Artifacts/Equipment/Clothing/TheMostKnowledgePerson.cs
Items/Artifacts/Equipment/Clothing/TheRobeOfBritanniaAri.cs
Items/Artifacts/Equipment/Glasses/AnthropomorphistGlasses.cs
Items/Artifacts/Equipment/Glasses/ArtsGlasses.cs
Items/Artifacts/Equipment/Glasses/BrightsightLenses.cs
Items/Artifacts/Equipment/Glasses/FoldedSteelGlasses.cs
Items/Artifacts/Equipment/Glasses/LightOfWayGlasses.cs
Items/Artifacts/Equipment/Glasses/LyricalGlasses.cs
Items/Artifacts/Equipment/Glasses/MaritimeGlasses.cs
Items/Artifacts/Equipment/Glasses/NecromanticGlasses.cs
Items/Artifacts/Equipment/Glasses/PoisonedGlasses.cs
Items/Artifacts/Equipment/Glasses/TradeGlasses.cs
Items/Artifacts/Equipment/Glasses/TreasureTrinketGlasses.cs
Items/Artifacts/Equipment/Glasses/WizardsGlasses.cs
Items/Artifacts/Equipment/Instruments/GwennosHarp.cs
Items/Artifacts/Equipment/Instruments/IolosLute.cs
Items/Artifacts/Equipment/Jewelry/AlchemistsBauble.cs
Items/Artifacts/Equipment/Jewelry/BraceletOfHealth.cs
Items/Artifacts/Equipment/Jewelry/BraceletOfResilience.cs
Items/Artifacts/Equipment/Jewelry/ClaspOfConcentration.cs
Items/Artifacts/Equipment/Jewelry/DjinnisRing.cs
Items/Artifacts/Equipment/Jewelry/EarringsOfProtection.cs
Items/Artifacts/Equipment/Jewelry/EssenceOfBattle.cs
Items/Artifacts/Equipment/Jewelry/LuckyNecklace.cs
Items/Artifacts/Equipment/Jewelry/OrnamentOfTheMagician.cs
Items/Artifacts/Equipment/Jewelry/PendantOfTheMagi.cs
Items/Artifacts/Equipment/Jewelry/ReginasRing.cs
Items/Artifacts/Equipment/Jewelry/ResillientBracer.cs
Items/Artifacts/Equipment/Jewelry/RingOfTheElements.cs
Items/Artifacts/Equipment/Jewelry/RingOfTheSavant.cs
Items/Artifacts/Equipment/Jewelry/RingOfTheVile.cs
Items/Artifacts/Equipment/Quivers/QuiverOfBlight.cs
Items/Artifacts/Equipment/Quivers/QuiverOfElements.cs
Items/Artifacts/Equipment/Quivers/QuiverOfFire.cs
Items/Artifacts/Equipment/Quivers/QuiverOfIce.cs
Items/Artifacts/Equipment/Quivers/QuiverOfInfinity.cs
Items/Artifacts/Equipment/Quivers/QuiverOfLightning.cs
Items/Artifacts/Equipment/Quivers/QuiverOfRage.cs
Items/Artifacts/Equipment/Spellbooks/HallowedSpellbook.cs
Items/Artifacts/Equipment/Spellbooks/OssianGrimoire.cs
Items/Artifacts/Equipment/Spellbooks/Runebook.cs
Items/Artifacts/Equipment/Weapons/AdventurersMachete.cs
Items/Artifacts/Equipment/Weapons/AncientWildStaff.cs
Items/Artifacts/Equipment/Weapons/ArcanistsWildStaff.cs
Items/Artifacts/Equipment/Weapons/ArcticDeathDealer.cs
Items/Artifacts/Equipment/Weapons/AssassinsShortbow.cs
Items/Artifacts/Equipment/Weapons/AxeOfTheHeavens.cs
Items/Artifacts/Equipment/Weapons/BarbedLongbow.cs
Items/Artifacts/Equipment/Weapons/BladeDance.cs
Items/Artifacts/Equipment/Weapons/BladeOfInsanity.cs
Items/Artifacts/Equipment/Weapons/BladeOfTheRighteous.cs
Items/Artifacts/Equipment/Weapons/BlazeOfDeath.cs
Items/Artifacts/Equipment/Weapons/BlightGrippedLongbow.cs
Items/Artifacts/Equipment/Weapons/BoneCrusher.cs
Items/Artifacts/Equipment/Weapons/Bonesmasher.cs
Items/Artifacts/Equipment/Weapons/Boomstick.cs
Items/Artifacts/Equipment/Weapons/BowOfTheJukaKing.cs
Items/Artifacts/Equipment/Weapons/BraveKnightOfTheBritannia.cs
Items/Artifacts/Equipment/Weapons/BreathOfTheDead.cs
Items/Artifacts/Equipment/Weapons/ButchersWarCleaver.cs
Items/Artifacts/Equipment/Weapons/Calm.cs
Items/Artifacts/Equipment/Weapons/CaptainQuacklebushsCutlass.cs
Items/Artifacts/Equipment/Weapons/CavortingClub.cs
Items/Artifacts/Equipment/Weapons/ChargedAssassinSpike.cs
Items/Artifacts/Equipment/Weapons/ChurchillsWarMace.cs
Items/Artifacts/Equipment/Weapons/ColdBlood.cs
Items/Artifacts/Equipment/Weapons/ColdForgedBlade.cs
Items/Artifacts/Equipment/Weapons/CorruptedRuneBlade.cs
Items/Artifacts/Equipment/Weapons/DarkglowScimitar.cs
Items/Artifacts/Equipment/Weapons/DiseasedMachete.cs
Items/Artifacts/Equipment/Weapons/EmberStaff.cs
Items/Artifacts/Equipment/Weapons/EnchantedTitanLegBone.cs
Items/Artifacts/Equipment/Weapons/FaerieFire.cs
Items/Artifacts/Equipment/Weapons/FangOfRactus.cs
Items/Artifacts/Equipment/Weapons/FierySpellblade.cs
Items/Artifacts/Equipment/Weapons/FleshRipper.cs
Items/Artifacts/Equipment/Weapons/Frostbringer.cs
Items/Artifacts/Equipment/Weapons/FrozenLongbow.cs
Items/Artifacts/Equipment/Weapons/GlacialStaff.cs
Items/Artifacts/Equipment/Weapons/GuardianAxe.cs
Items/Artifacts/Equipment/Weapons/HardenedWildStaff.cs
Items/Artifacts/Equipment/Weapons/Heartseeker.cs
Items/Artifacts/Equipment/Weapons/HolySword.cs
Items/Artifacts/Equipment/Weapons/IcyScimitar.cs
Items/Artifacts/Equipment/Weapons/IcySpellblade.cs
Items/Artifacts/Equipment/Weapons/JocklesQuicksword.cs
Items/Artifacts/Equipment/Weapons/KnightsWarCleaver.cs
Items/Artifacts/Equipment/Weapons/LeafbladeOfEase.cs
Items/Artifacts/Equipment/Weapons/LegacyOfTheDreadLord.cs
Items/Artifacts/Equipment/Weapons/LongbowOfMight.cs
Items/Artifacts/Equipment/Weapons/Luckblade.cs
Items/Artifacts/Equipment/Weapons/LuminousRuneBlade.cs
Items/Artifacts/Equipment/Weapons/LunaLance.cs
Items/Artifacts/Equipment/Weapons/MacheteOfDefense.cs
Items/Artifacts/Equipment/Weapons/MagekillerAssassinSpike.cs
Items/Artifacts/Equipment/Weapons/MagekillerLeafblade.cs
Items/Artifacts/Equipment/Weapons/MagesRuneBlade.cs
Items/Artifacts/Equipment/Weapons/MelisandesCorrodedHatchet.cs
Items/Artifacts/Equipment/Weapons/MischiefMaker.cs
Items/Artifacts/Equipment/Weapons/MysticalShortbow.cs
Items/Artifacts/Equipment/Weapons/NightsKiss.cs
Items/Artifacts/Equipment/Weapons/NoxRangersHeavyCrossbow.cs
Items/Artifacts/Equipment/Weapons/OblivionsNeedle.cs
Items/Artifacts/Equipment/Weapons/OrcishMachete.cs
Items/Artifacts/Equipment/Weapons/OverseerSunderedBlade.cs
Items/Artifacts/Equipment/Weapons/Pacify.cs
Items/Artifacts/Equipment/Weapons/PhantomStaff.cs
Items/Artifacts/Equipment/Weapons/PixieSwatter.cs
Items/Artifacts/Equipment/Weapons/Quell.cs
Items/Artifacts/Equipment/Weapons/RaedsGlory.cs
Items/Artifacts/Equipment/Weapons/RangersShortbow.cs
Items/Artifacts/Equipment/Weapons/RaptorClaw.cs
Items/Artifacts/Equipment/Weapons/RecarosRiposte.cs
Items/Artifacts/Equipment/Weapons/RighteousAnger.cs
Items/Artifacts/Equipment/Weapons/RoyalGuardSurvivalKnife.cs
Items/Artifacts/Equipment/Weapons/RuneBladeOfKnowledge.cs
Items/Artifacts/Equipment/Weapons/RuneCarvingKnife.cs
Items/Artifacts/Equipment/Weapons/Runesabre.cs
Items/Artifacts/Equipment/Weapons/SapphireMace.cs
Items/Artifacts/Equipment/Weapons/SerpentsFang.cs
Items/Artifacts/Equipment/Weapons/ShaminoCrossbow.cs
Items/Artifacts/Equipment/Weapons/ShardTrasher.cs
Items/Artifacts/Equipment/Weapons/SilvanisFeywoodBow.cs
Items/Artifacts/Equipment/Weapons/SilverSerpentBlade.cs
Items/Artifacts/Equipment/Weapons/SingingAxe.cs
Items/Artifacts/Equipment/Weapons/SlayerLongbow.cs
Items/Artifacts/Equipment/Weapons/SoulSeeker.cs
Items/Artifacts/Equipment/Weapons/SpellbladeOfDefense.cs
Items/Artifacts/Equipment/Weapons/StaffOfPower.cs
Items/Artifacts/Equipment/Weapons/StaffOfTheMagi.cs
Items/Artifacts/Equipment/Weapons/Subdue.cs
Items/Artifacts/Equipment/Weapons/TalonBite.cs
Items/Artifacts/Equipment/Weapons/TheBeserkersMaul.cs
Items/Artifacts/Equipment/Weapons/TheDragonSlayer.cs
Items/Artifacts/Equipment/Weapons/TheDragonsTail.cs
Items/Artifacts/Equipment/Weapons/TheDryadBow.cs
Items/Artifacts/Equipment/Weapons/TheNightReaper.cs
Items/Artifacts/Equipment/Weapons/TheTaskmaster.cs
Items/Artifacts/Equipment/Weapons/ThornedWildStaff.cs
Items/Artifacts/Equipment/Weapons/ThunderingAxe.cs
Items/Artifacts/Equipment/Weapons/TitansHammer.cs
Items/Artifacts/Equipment/Weapons/TrueAssassinSpike.cs
Items/Artifacts/Equipment/Weapons/TrueLeafblade.cs
Items/Artifacts/Equipment/Weapons/TrueRadiantScimitar.cs
Items/Artifacts/Equipment/Weapons/TrueSpellblade.cs
Items/Artifacts/Equipment/Weapons/TrueWarCleaver.cs
Items/Artifacts/Equipment/Weapons/TwinklingScimitar.cs
Items/Artifacts/Equipment/Weapons/WildfireBow.cs
Items/Artifacts/Equipment/Weapons/Windsong.cs
Items/Artifacts/Equipment/Weapons/WoundingAssassinSpike.cs
Items/Artifacts/Equipment/Weapons/WrathOfTheDryad.cs
Items/Artifacts/Equipment/Weapons/ZyronicClaw.cs
Items/Artifacts/TOTGreaterArtifacts.cs
Items/Artifacts/TOTLesserArtifacts.cs
Items/Artifacts/Tools/AmeliasToolbox.cs
Items/Artifacts/Tools/JacobsPickaxe.cs
Items/Equipment/Armor/ArmorEnums.cs
Items/Equipment/Armor/Bascinet.cs
Items/Equipment/Armor/BaseArmor.cs
Items/Equipment/Armor/BaseShield.cs
Items/Equipment/Armor/BoneArms.cs
Items/Equipment/Armor/BoneChest.cs
Items/Equipment/Armor/BoneGloves.cs
Items/Equipment/Armor/BoneHelm.cs
Items/Equipment/Armor/BoneLegs.cs
Items/Equipment/Armor/BronzeShield.cs
Items/Equipment/Armor/Buckler.cs
Items/Equipment/Armor/ChainChest.cs
Items/Equipment/Armor/ChainCoif.cs
Items/Equipment/Armor/ChainHatsuburi.cs
Items/Equipment/Armor/ChainLegs.cs
Items/Equipment/Armor/ChaosShield.cs
Items/Equipment/Armor/Circlet.cs
Items/Equipment/Armor/CloseHelm.cs
Items/Equipment/Armor/DecorativePlateKabuto.cs
Items/Equipment/Armor/DragonArms.cs
Items/Equipment/Armor/DragonChest.cs
Items/Equipment/Armor/DragonGloves.cs
Items/Equipment/Armor/DragonHelm.cs
Items/Equipment/Armor/DragonLegs.cs
Items/Equipment/Armor/FemaleLeafChest.cs
Items/Equipment/Armor/FemaleLeatherChest.cs
Items/Equipment/Armor/FemalePlateChest.cs
Items/Equipment/Armor/FemaleStuddedChest.cs
Items/Equipment/Armor/FemaleWoodlandChest.cs
Items/Equipment/Armor/GargishLeatherWingArmor.cs
Items/Equipment/Armor/GemmedCirclet.cs
Items/Equipment/Armor/HeaterShield.cs
Items/Equipment/Armor/HeavyPlateJingasa.cs
Items/Equipment/Armor/Helmet.cs
Items/Equipment/Armor/HideChest.cs
Items/Equipment/Armor/HideFemaleChest.cs
Items/Equipment/Armor/HideGloves.cs
Items/Equipment/Armor/HideGorget.cs
Items/Equipment/Armor/HidePants.cs
Items/Equipment/Armor/HidePauldrons.cs
Items/Equipment/Armor/LeafArms.cs
Items/Equipment/Armor/LeafChest.cs
Items/Equipment/Armor/LeafGloves.cs
Items/Equipment/Armor/LeafGorget.cs
Items/Equipment/Armor/LeafLegs.cs
Items/Equipment/Armor/LeafTonlet.cs
Items/Equipment/Armor/LeatherArms.cs
Items/Equipment/Armor/LeatherBustierArms.cs
Items/Equipment/Armor/LeatherCap.cs
Items/Equipment/Armor/LeatherChest.cs
Items/Equipment/Armor/LeatherDo.cs
Items/Equipment/Armor/LeatherGloves.cs
Items/Equipment/Armor/LeatherGorget.cs
Items/Equipment/Armor/LeatherHaidate.cs
Items/Equipment/Armor/LeatherHiroSode.cs
Items/Equipment/Armor/LeatherJingasa.cs
Items/Equipment/Armor/LeatherLegs.cs
Items/Equipment/Armor/LeatherMempo.cs
Items/Equipment/Armor/LeatherNinjaHood.cs
Items/Equipment/Armor/LeatherNinjaJacket.cs
Items/Equipment/Armor/LeatherNinjaMitts.cs
Items/Equipment/Armor/LeatherNinjaPants.cs
Items/Equipment/Armor/LeatherShorts.cs
Items/Equipment/Armor/LeatherSkirt.cs
Items/Equipment/Armor/LeatherSuneate.cs
Items/Equipment/Armor/LightPlateJingasa.cs
Items/Equipment/Armor/MetalKiteShield.cs
Items/Equipment/Armor/MetalShield.cs
Items/Equipment/Armor/NorseHelm.cs
Items/Equipment/Armor/OrcHelm.cs
Items/Equipment/Armor/OrderShield.cs
Items/Equipment/Armor/PlateArms.cs
Items/Equipment/Armor/PlateBattleKabuto.cs
Items/Equipment/Armor/PlateChest.cs
Items/Equipment/Armor/PlateDo.cs
Items/Equipment/Armor/PlateGloves.cs
Items/Equipment/Armor/PlateGorget.cs
Items/Equipment/Armor/PlateHaidate.cs
Items/Equipment/Armor/PlateHatsuburi.cs
Items/Equipment/Armor/PlateHelm.cs
Items/Equipment/Armor/PlateHiroSode.cs
Items/Equipment/Armor/PlateLegs.cs
Items/Equipment/Armor/PlateMempo.cs
Items/Equipment/Armor/PlateSuneate.cs
Items/Equipment/Armor/RavenHelm.cs
Items/Equipment/Armor/RingmailArms.cs
Items/Equipment/Armor/RingmailChest.cs
Items/Equipment/Armor/RingmailGloves.cs
Items/Equipment/Armor/RingmailLegs.cs
Items/Equipment/Armor/RoyalCirclet.cs
Items/Equipment/Armor/SmallPlateJingasa.cs
Items/Equipment/Armor/StandardPlateKabuto.cs
Items/Equipment/Armor/StuddedArms.cs
Items/Equipment/Armor/StuddedBustierArms.cs
Items/Equipment/Armor/StuddedChest.cs
Items/Equipment/Armor/StuddedDo.cs
Items/Equipment/Armor/StuddedGloves.cs
Items/Equipment/Armor/StuddedGorget.cs
Items/Equipment/Armor/StuddedHaidate.cs
Items/Equipment/Armor/StuddedHiroSode.cs
Items/Equipment/Armor/StuddedLegs.cs
Items/Equipment/Armor/StuddedMempo.cs
Items/Equipment/Armor/StuddedSuneate.cs
Items/Equipment/Armor/TigerPeltBustier.cs
Items/Equipment/Armor/TigerPeltChest.cs
Items/Equipment/Armor/TigerPeltCollar.cs
Items/Equipment/Armor/TigerPeltHelm.cs
Items/Equipment/Armor/TigerPeltLegs.cs
Items/Equipment/Armor/TigerPeltLongSkirt.cs
Items/Equipment/Armor/TigerPeltShorts.cs
Items/Equipment/Armor/TigerPeltSkirt.cs
Items/Equipment/Armor/VultureHelm.cs
Items/Equipment/Armor/WingedHelm.cs
Items/Equipment/Armor/WoodenKiteShield.cs
Items/Equipment/Armor/WoodenShield.cs
Items/Equipment/Armor/WoodlandArms.cs
Items/Equipment/Armor/WoodlandChest.cs
Items/Equipment/Armor/WoodlandGloves.cs
Items/Equipment/Armor/WoodlandGorget.cs
Items/Equipment/Armor/WoodlandLegs.cs
Items/Equipment/Clothing/BaseClothing.cs
Items/Equipment/Clothing/Cloaks.cs
Items/Equipment/Clothing/LeatherNinjaBelt.cs
Items/Equipment/Clothing/MiddleTorso.cs
Items/Equipment/Clothing/OuterLegs.cs
Items/Equipment/Clothing/OuterTorso.cs
Items/Equipment/Clothing/Shirts.cs
Items/Equipment/Clothing/Shoes.cs
Items/Equipment/Clothing/Waist.cs
Items/Equipment/Glasses/ElvenGlasses.cs
Items/Equipment/Instruments/BambooFlute.cs
Items/Equipment/Instruments/BaseInstrument.cs
Items/Equipment/Instruments/Drums.cs
Items/Equipment/Instruments/FireHorn.cs
Items/Equipment/Instruments/Harp.cs
Items/Equipment/Instruments/LapHarp.cs
Items/Equipment/Instruments/Lute.cs
Items/Equipment/Instruments/Tambourine.cs
Items/Equipment/Instruments/TambourineTassel.cs
Items/Equipment/Jewelry/BaseJewel.cs
Items/Equipment/Jewelry/Beads.cs
Items/Equipment/Jewelry/Bracelet.cs
Items/Equipment/Jewelry/Earrings.cs
Items/Equipment/Jewelry/Necklace.cs
Items/Equipment/Jewelry/Ring.cs
Items/Equipment/Light/BaseEquipableLight.cs
Items/Equipment/Light/Candle.cs
Items/Equipment/Light/Lantern.cs
Items/Equipment/Light/Torch.cs
Items/Equipment/Light/TwilightLantern.cs
Items/Equipment/Quivers/BaseQuiver.cs
Items/Equipment/Quivers/ElvenQuiver.cs
Items/Equipment/Spellbooks/BookOfBushido.cs
Items/Equipment/Spellbooks/BookOfChivalry.cs
Items/Equipment/Spellbooks/BookOfNinjitsu.cs
Items/Equipment/Spellbooks/NecromancerSpellbook.cs
Items/Equipment/Spellbooks/Spellbook.cs
Items/Equipment/Spellbooks/SpellweavingBook.cs
Items/Equipment/Suits/BaseSuit.cs
Items/Equipment/Suits/DeathShroud.cs
Items/Equipment/Suits/DupreSuit.cs
Items/Equipment/Suits/LordBlackthorneSuit.cs
Items/Equipment/Suits/LordBritishSuit.cs
Items/Equipment/Talismans/BaseTalisman.cs
Items/Equipment/Talismans/BloodwoodSpirit.cs
Items/Equipment/Talismans/RandomTalisman.cs
Items/Equipment/Talismans/TalismanAttribute.cs
Items/Equipment/Talismans/TalismanSlayer.cs
Items/Equipment/Talismans/TalismanSummons.cs
Items/Equipment/Talismans/Talismans.cs
Items/Equipment/Talismans/TotemOfVoid.cs
Items/Equipment/Weapons/AssassinSpike.cs
Items/Equipment/Weapons/Axe.cs
Items/Equipment/Weapons/Bardiche.cs
Items/Equipment/Weapons/BaseAxe.cs
Items/Equipment/Weapons/BaseBashing.cs
Items/Equipment/Weapons/BaseKnife.cs
Items/Equipment/Weapons/BaseMeleeWeapon.cs
Items/Equipment/Weapons/BasePoleArm.cs
Items/Equipment/Weapons/BaseRanged.cs
Items/Equipment/Weapons/BaseSpear.cs
Items/Equipment/Weapons/BaseStaff.cs
Items/Equipment/Weapons/BaseSword.cs
Items/Equipment/Weapons/BaseThrown.cs
Items/Equipment/Weapons/BaseWand.cs
Items/Equipment/Weapons/BaseWeapon.cs
Items/Equipment/Weapons/BattleAxe.cs
Items/Equipment/Weapons/BlackStaff.cs
Items/Equipment/Weapons/BladedStaff.cs
Items/Equipment/Weapons/BloodBlade.cs
Items/Equipment/Weapons/Bokuto.cs
Items/Equipment/Weapons/BoneHarvester.cs
Items/Equipment/Weapons/BoneMachete.cs
Items/Equipment/Weapons/Boomerang.cs
Items/Equipment/Weapons/Bow.cs
Items/Equipment/Weapons/Broadsword.cs
Items/Equipment/Weapons/ButcherKnife.cs
Items/Equipment/Weapons/Cleaver.cs
Items/Equipment/Weapons/Club.cs
Items/Equipment/Weapons/ClumsyWand.cs
Items/Equipment/Weapons/CompositeBow.cs
Items/Equipment/Weapons/CrescentBlade.cs
Items/Equipment/Weapons/Crossbow.cs
Items/Equipment/Weapons/Cutlass.cs
Items/Equipment/Weapons/Cyclone.cs
Items/Equipment/Weapons/Dagger.cs
Items/Equipment/Weapons/Daisho.cs
Items/Equipment/Weapons/DiamondMace.cs
Items/Equipment/Weapons/DiscMace.cs
Items/Equipment/Weapons/DoubleAxe.cs
Items/Equipment/Weapons/DoubleBladedStaff.cs
Items/Equipment/Weapons/DreadSword.cs
Items/Equipment/Weapons/DualPointedSpear.cs
Items/Equipment/Weapons/DualShortAxes.cs
Items/Equipment/Weapons/ElvenCompositeLongbow.cs
Items/Equipment/Weapons/ElvenMachete.cs
Items/Equipment/Weapons/ElvenSpellblade.cs
Items/Equipment/Weapons/EmeraldMace.cs
Items/Equipment/Weapons/ExecutionersAxe.cs
Items/Equipment/Weapons/FeebleWand.cs
Items/Equipment/Weapons/FireballWand.cs
Items/Equipment/Weapons/FireworksWand.cs
Items/Equipment/Weapons/Fists.cs
Items/Equipment/Weapons/Fukiya.cs
Items/Equipment/Weapons/GargishTalwar.cs
Items/Equipment/Weapons/GlassStaff.cs
Items/Equipment/Weapons/GlassSword.cs
Items/Equipment/Weapons/GnarledStaff.cs
Items/Equipment/Weapons/GreaterHealWand.cs
Items/Equipment/Weapons/Halberd.cs
Items/Equipment/Weapons/HammerPick.cs
Items/Equipment/Weapons/HarmWand.cs
Items/Equipment/Weapons/Hatchet.cs
Items/Equipment/Weapons/HealWand.cs
Items/Equipment/Weapons/HeavyCrossbow.cs
Items/Equipment/Weapons/HeavyOrnateAxe.cs
Items/Equipment/Weapons/HitLower.cs
Items/Equipment/Weapons/IDWand.cs
Items/Equipment/Weapons/JukaBow.cs
Items/Equipment/Weapons/Kama.cs
Items/Equipment/Weapons/Katana.cs
Items/Equipment/Weapons/Kryss.cs
Items/Equipment/Weapons/Lajatang.cs
Items/Equipment/Weapons/Lance.cs
Items/Equipment/Weapons/LargeBattleAxe.cs
Items/Equipment/Weapons/Leafblade.cs
Items/Equipment/Weapons/LightningWand.cs
Items/Equipment/Weapons/LightweightShortbow.cs
Items/Equipment/Weapons/Longsword.cs
Items/Equipment/Weapons/Mace.cs
Items/Equipment/Weapons/MagicArrowWand.cs
Items/Equipment/Weapons/MagicWand.cs
Items/Equipment/Weapons/MagicalShortbow.cs
Items/Equipment/Weapons/ManaDrainWand.cs
Items/Equipment/Weapons/Maul.cs
Items/Equipment/Weapons/NinjaWeapons.cs
Items/Equipment/Weapons/NoDachi.cs
Items/Equipment/Weapons/Nunchaku.cs
Items/Equipment/Weapons/OrnateAxe.cs
Items/Equipment/Weapons/Pickaxe.cs
Items/Equipment/Weapons/Pike.cs
Items/Equipment/Weapons/Pitchfork.cs
Items/Equipment/Weapons/QuarterStaff.cs
Items/Equipment/Weapons/RadiantScimitar.cs
Items/Equipment/Weapons/RepeatingCrossbow.cs
Items/Equipment/Weapons/RubyMace.cs
Items/Equipment/Weapons/RuneBlade.cs
Items/Equipment/Weapons/Sai.cs
Items/Equipment/Weapons/Scepter.cs
Items/Equipment/Weapons/Scimitar.cs
Items/Equipment/Weapons/Scythe.cs
Items/Equipment/Weapons/SerratedWarCleaver.cs
Items/Equipment/Weapons/ShepherdsCrook.cs
Items/Equipment/Weapons/ShortSpear.cs
Items/Equipment/Weapons/SilverEtchedMace.cs
Items/Equipment/Weapons/SkinningKnife.cs
Items/Equipment/Weapons/SoulGlaive.cs
Items/Equipment/Weapons/Spear.cs
Items/Equipment/Weapons/Tekagi.cs
Items/Equipment/Weapons/Tessen.cs
Items/Equipment/Weapons/Tetsubo.cs
Items/Equipment/Weapons/ThinLongsword.cs
Items/Equipment/Weapons/TribalSpear.cs
Items/Equipment/Weapons/TwoHandedAxe.cs
Items/Equipment/Weapons/VikingSword.cs
Items/Equipment/Weapons/Wakizashi.cs
Items/Equipment/Weapons/WandTarget.cs
Items/Equipment/Weapons/WarAxe.cs
Items/Equipment/Weapons/WarCleaver.cs
Items/Equipment/Weapons/WarFork.cs
Items/Equipment/Weapons/WarHammer.cs
Items/Equipment/Weapons/WarMace.cs
Items/Equipment/Weapons/WeaknessWand.cs
Items/Equipment/Weapons/WeaponEnums.cs
Items/Equipment/Weapons/WildStaff.cs
Items/Equipment/Weapons/Yumi.cs
```


### CC7 Decoration/housing (the 297)

Prefixes: `Items/Addons`, `Items/Decorative`, `Services/New Magincia`  
raw 745 → filtered out 442 → candidates 303  
drops straight in 159 · needs another row file 50 · co-port 5 · upstream/carrier 89


#### CC7 Decoration/housing (the 297) — drops straight in (159 files)

```
Items/Addons/AdvancedTrainingDummy.cs
Items/Addons/Aquarium/AquariumFishingNet.cs
Items/Addons/CodexOfVirtue.cs
Items/Addons/Craft Addons/CraftAddonDeed.cs
Items/Addons/Crystal Furniture Set/CrystalAltar.cs
Items/Addons/Crystal Furniture Set/CrystalBrazier.cs
Items/Addons/Dressform.cs
Items/Addons/ElvenWashbasinEastAddonWithDrawer.cs
Items/Addons/ElvenWashbasinSouthAddonWithDrawer.cs
Items/Addons/FancyCouchEast.cs
Items/Addons/FancyCouchNorth.cs
Items/Addons/FancyCouchSouth.cs
Items/Addons/FancyCouchWest.cs
Items/Addons/FancyLoveseatEast.cs
Items/Addons/FancyLoveseatNorth.cs
Items/Addons/FancyLoveseatSouth.cs
Items/Addons/FancyLoveseatWest.cs
Items/Addons/FancyWoodenShelfEast.cs
Items/Addons/FancyWoodenShelfSouth.cs
Items/Addons/GardenShed.cs
Items/Addons/GeoffreyCampAddon.cs
Items/Addons/GoblinTopiary.cs
Items/Addons/JollyHolidayTree.cs
Items/Addons/LlamaTopiary.cs
Items/Addons/LongMetalTableEast.cs
Items/Addons/LongMetalTableSouth.cs
Items/Addons/LongTableEastAddon.cs
Items/Addons/LongTableSouth.cs
Items/Addons/LongWoodenTableEast.cs
Items/Addons/LongWoodenTableSouth.cs
Items/Addons/MedusaNest.cs
Items/Addons/MetalTableEast.cs
Items/Addons/MetalTableSouth.cs
Items/Addons/MiniSoulForge.cs
Items/Addons/NexusAddon.cs
Items/Addons/OstardTopiary.cs
Items/Addons/PlainWoodenShelfEast.cs
Items/Addons/PlainWoodenShelfSouth.cs
Items/Addons/PlantTapestryEast.cs
Items/Addons/PlantTapestrySouth.cs
Items/Addons/PlushLoveseatEast.cs
Items/Addons/PlushLoveseatSouth.cs
Items/Addons/PosedGoblinTopiary.cs
Items/Addons/RitualTableAddon.cs
Items/Addons/RoyalSoulForge.cs
Items/Addons/RusticBenchEast.cs
Items/Addons/RusticBenchSouth.cs
Items/Addons/Shadow Furniture Set/GlobeOfSosaria.cs
Items/Addons/Shadow Furniture Set/ObsidianPillar.cs
Items/Addons/Shadow Furniture Set/ObsidianRock.cs
Items/Addons/Shadow Furniture Set/ShadowFirePit.cs
Items/Addons/Shadow Furniture Set/ShadowPillar.cs
Items/Addons/Shadow Furniture Set/SpikeColumn.cs
Items/Addons/SheepStatue.cs
Items/Addons/SkullTiledFloor.cs
Items/Addons/SmallDisplayCaseEast.cs
Items/Addons/SmallDisplayCaseSouth.cs
Items/Addons/SmallSoulForge.cs
Items/Addons/SoulForge.cs
Items/Addons/SouthEastPlacementGump.cs
Items/Addons/StoneAnvilEastAddon.cs
Items/Addons/StoneAnvilSouthAddon.cs
Items/Addons/TerMurDresserEastAddon.cs
Items/Addons/TerMurDresserSouthAddon.cs
Items/Addons/TheKingsCollection/BirdLamp.cs
Items/Addons/TheKingsCollection/CactusSponge.cs
Items/Addons/TheKingsCollection/DragonLantern.cs
Items/Addons/TheKingsCollection/FluffySponge.cs
Items/Addons/TheKingsCollection/KoiLamp.cs
Items/Addons/TheKingsCollection/ShelfSponge.cs
Items/Addons/TheKingsCollection/TallLamp.cs
Items/Addons/VendorMallAddon.cs
Items/Addons/WeatheredBronzeArcherSculpture.cs
Items/Addons/WeatheredBronzeFairySculpture.cs
Items/Addons/WeatheredBronzeGlobeSculpture.cs
Items/Addons/WeatheredBronzeManOnABench.cs
Items/Addons/WoodenTableEast.cs
Items/Addons/WoodenTableSouth.cs
Items/Addons/goldcarpetAddon.cs
Items/Decorative/AcidWall.cs
Items/Decorative/AcidWall1.cs
Items/Decorative/AncientWeapons.cs
Items/Decorative/ArtisanFestivalRewards/LanternBrokenShield.cs
Items/Decorative/ArtisanFestivalRewards/LanternHand.cs
Items/Decorative/ArtisanFestivalRewards/LanternHeart.cs
Items/Decorative/ArtisanFestivalRewards/LanternUnevenScales.cs
Items/Decorative/ArtisanFestivalRewards/PaintingAnkh.cs
Items/Decorative/ArtisanFestivalRewards/PaintingAxe.cs
Items/Decorative/ArtisanFestivalRewards/PaintingMasks.cs
Items/Decorative/ArtisanFestivalRewards/PaintingSword.cs
Items/Decorative/ArtisanFestivalRewards/PillowChalice.cs
Items/Decorative/ArtisanFestivalRewards/PillowMoon.cs
Items/Decorative/ArtisanFestivalRewards/PillowSkull.cs
Items/Decorative/ArtisanFestivalRewards/PillowTear.cs
Items/Decorative/ArtisanFestivalRewards/SculptureWoodCanes.cs
Items/Decorative/ArtisanFestivalRewards/SculptureWoodCoin.cs
Items/Decorative/ArtisanFestivalRewards/SculptureWoodEven.cs
Items/Decorative/ArtisanFestivalRewards/SculptureWoodScept.cs
Items/Decorative/BaseSliding.cs
Items/Decorative/BaseStatuette.cs
Items/Decorative/Bridle.cs
Items/Decorative/ButcherBlock.cs
Items/Decorative/Countertop.cs
Items/Decorative/CrystalBall.cs
Items/Decorative/CrystalSkull.cs
Items/Decorative/DecorativeHourglass.cs
Items/Decorative/DecorativeStableSet/ChickenStatue.cs
Items/Decorative/DecorativeStableSet/CowPie.cs
Items/Decorative/DecorativeStableSet/CowStatue.cs
Items/Decorative/DecorativeStableSet/Feedbag.cs
Items/Decorative/DecorativeStableSet/HorseStatue.cs
Items/Decorative/DecorativeVine.cs
Items/Decorative/DoveCage.cs
Items/Decorative/DragonLamp.cs
Items/Decorative/Easle.cs
Items/Decorative/ElvenAlchemyTable.cs
Items/Decorative/EnchantedWheelbarrow.cs
Items/Decorative/FlamingScarecrow.cs
Items/Decorative/GargishBanner.cs
Items/Decorative/GargishSculpture.cs
Items/Decorative/GargoyleCandelabra.cs
Items/Decorative/GargoyleChair.cs
Items/Decorative/GargoyleEndTable.cs
Items/Decorative/GargoyleFloorMirror.cs
Items/Decorative/GargoylePainting.cs
Items/Decorative/GargoyleVase.cs
Items/Decorative/GargoyleWallMirror.cs
Items/Decorative/GypsyWagonLamp.cs
Items/Decorative/HolidayWallArt.cs
Items/Decorative/HolidaysSign.cs
Items/Decorative/HornAbyssalInferno.cs
Items/Decorative/JadeSkull.cs
Items/Decorative/KepetchWax.cs
Items/Decorative/Lever.cs
Items/Decorative/Lodestone.cs
Items/Decorative/MusicStand.cs
Items/Decorative/ObsidianSkull.cs
Items/Decorative/OrderChaosBanners.cs
Items/Decorative/Poinsettias.cs
Items/Decorative/PumpkinCarvingKit.cs
Items/Decorative/SilverSaplingReplica.cs
Items/Decorative/SingingBall.cs
Items/Decorative/SpikeHead.cs
Items/Decorative/StaghornFern.cs
Items/Decorative/StainedGlassLamp.cs
Items/Decorative/StoneWallAndVineAddon.cs
Items/Decorative/TallDoubleLamp.cs
Items/Decorative/TatteredWallMap.cs
Items/Decorative/TerMurStyleCandelabra.cs
Items/Decorative/UltimaBanner.cs
Items/Decorative/UpholsteredChair.cs
Items/Decorative/ValentinesDayTableSet.cs
Items/Decorative/Wreath.cs
Services/New Magincia/Distillation/Items/MetalKeg.cs
Services/New Magincia/Distillation/Items/WheatWort.cs
Services/New Magincia/Distillation/Items/Yeast.cs
Services/New Magincia/Housing Lotto/Core/NewMaginciaMessage.cs
Services/New Magincia/Magincia Bazaar/Items/Containers.cs
Services/New Magincia/Magincia Bazaar/Items/StallMultis.cs
```


#### CC7 Decoration/housing (the 297) — portable once other files in this row come with it (50 files)

```
Items/Addons/CorporealBrumeStatuette.cs  <- ShimmeringEffusionStatuette
Items/Addons/Craft Addons/AddonToolComponenet.cs  <- CraftAddon, OnCraftComponentLoaded, OnCraftComponentUsed
Items/Addons/Craft Addons/AlchemyStation.cs  <- AddCraftComponent, AddonToolComponent, CraftAddon, CraftAddonDeed, SouthEastGump, ToolDropComponent
Items/Addons/Craft Addons/BBQSmoker.cs  <- AddCraftComponent, AddonToolComponent, CraftAddon, CraftAddonDeed, SouthEastGump, ToolDropComponent
Items/Addons/Craft Addons/CraftAddon.cs  <- AddonToolComponent, SetCraftSystem
Items/Addons/Craft Addons/FletchingStation.cs  <- AddCraftComponent, AddonToolComponent, CraftAddon, CraftAddonDeed, SouthEastGump, ToolDropComponent
Items/Addons/Craft Addons/SewingMachine.cs  <- AddCraftComponent, AddonToolComponent, CraftAddon, CraftAddonDeed, SouthEastGump, ToolDropComponent
Items/Addons/Craft Addons/SmithingPress.cs  <- AddCraftComponent, AddonToolComponent, CraftAddon, CraftAddonDeed, SouthEastGump, ToolDropComponent
Items/Addons/Craft Addons/SpinningLathe.cs  <- AddCraftComponent, AddonToolComponent, CraftAddon, CraftAddonDeed, SouthEastGump, ToolDropComponent
Items/Addons/Craft Addons/WritingDesk.cs  <- AddCraftComponent, AddonToolComponent, CraftAddon, CraftAddonDeed, SouthEastGump, ToolDropComponent
Items/Addons/Distillery.cs  <- DistillationGump
Items/Addons/DreadHornStatuette.cs  <- BaseStatuette
Items/Addons/DreadSpiderStatuette.cs  <- BaseStatuette
Items/Addons/FetidEssenceStatuette.cs  <- ShimmeringEffusionStatuette
Items/Addons/MantraEffervescenceStatuette.cs  <- ShimmeringEffusionStatuette
Items/Addons/MinotaurStatuette.cs  <- BaseStatuette
Items/Addons/OphidianArchMageStatuette.cs  <- BaseStatuette
Items/Addons/OphidianKnightStatuette.cs  <- BaseStatuette
Items/Addons/OphidianMageStatuette.cs  <- BaseStatuette
Items/Addons/OphidianWarriorStatuette.cs  <- BaseStatuette
Items/Addons/Parrot.cs  <- PetParrot
Items/Addons/PlagueBeastStatuette.cs  <- BaseStatuette
Items/Addons/RedDeathStatuette.cs  <- BaseStatuette
Items/Addons/ShimmeringEffusionStatuette.cs  <- BaseStatuette
Items/Addons/SlimeStatuette.cs  <- BaseStatuette
Items/Addons/TheKingsCollection/TheTokenBox.cs  <- AlchemistsBookshelfDeed, BarrelSpongeDeed, BirdLampDeed, BullTapestryDeed, CactusSpongeDeed, CastlePaintingDeed, DragonLanternDeed, EmbroideredTapestryDeed, FifteenthAnniversaryLithographDeed, FirePaintingDeed, FluffySpongeDeed, FourPostBedDeed, GoldenTableDeed, HorsePaintingDeed, KoiLampDeed, MarbleTableDeed, MonasteryBellDeed, OrnateBedDeed, ShelfSpongeDeed, ShipPaintingDeed, TallLampDeed
Items/Addons/TormentedMinotaurStatuette.cs  <- BaseStatuette
Items/Decorative/AllegiancePouch.cs  <- ChaosBanner, OrderBanner
Items/Decorative/DungeonWallAndVineAddon.cs  <- MagicVinesComponent
Items/Decorative/SecretSlidingWalls.cs  <- BaseSliding
Services/New Magincia/Command.cs  <- LottoTrackingGump, MaginciaBazaar, MaginciaLottoSystem, Plots
Services/New Magincia/Distillation/Items/BottleOfLiquor.cs  <- DistillationSystem
Services/New Magincia/Housing Lotto/Core/MaginciaHousingPlot.cs  <- AutoResetLotto, GetPlotStoneLoc, IsRegisteredPlot, LottoDuration, MaginciaLottoSystem, MaginciaPlotStone, NewMaginciaMessage, Plot, PlotWinnerGump, Plots, WritExpirePeriod, WritOfLease
Services/New Magincia/Housing Lotto/Gumps/LottoTrackingGump.cs  <- GoldSink, Identifier, LottoOngoing, LottoPrice, MaginciaHousingPlot, MaginciaLottoSystem, Plots
Services/New Magincia/Housing Lotto/Gumps/NewMaginciaMessageGump.cs  <- GetMessages, HasMessageInQueue, MaginciaLottoSystem, MessageQueue, NewMaginciaMessage, RemoveMessageFromQueue
Services/New Magincia/Housing Lotto/Gumps/PlotWinnerGump.cs  <- GetWinnerGump, Identifier, MaginciaHousingPlot, MaginciaLottoSystem, Writ, WritOfLease
Services/New Magincia/Housing Lotto/Items/MaginciaPlotStone.cs  <- Identifier, LottoOngoing, MaginciaHousingPlot, MaginciaLottoGump, MaginciaLottoSystem, UnregisterPlot
Services/New Magincia/Housing Lotto/Items/WritOfLease.cs  <- MaginciaHousingPlot, MaginciaLottoSystem, UnregisterPlot, WritExpirePeriod
Services/New Magincia/Magincia Bazaar/Core/BrokerEntries.cs  <- BankBalance, CommodityBroker
Services/New Magincia/Magincia Bazaar/Core/MaginciaBizaarPlot.cs  <- AuctionEnd, Auctioners, BaseBazaarBroker, BaseBazaarMulti, ChangeAuctionTime, CommodityBroker, CommodityStyle1, CommodityStyle2, CommodityStyle3, Fillers, GetShortAuctionTime, IsActivePlot, MaginciaBazaar, MaginciaPlotAuction, PetBroker, PetStyle1, PetStyle2, PetStyle3, Plot, PlotSign
Services/New Magincia/Magincia Bazaar/Core/MaginciaPlotAuction.cs  <- AwardPlot, DeductReserve, GetBidMatching, GetShortAuctionTime, HasActiveBid, HasTempMulti, MaginciaBazaar, MaginciaBazaarPlot, MaginciaLottoSystem, NewAuction, NewMaginciaMessage, NextAvailable, PlotDef, RemoveTempPlot, Reserve
Services/New Magincia/Magincia Bazaar/Core/StorageEntry.cs  <- BankBalance, BaseBazaarBroker, BrokerEntries, CommodityBroker, CommodityBrokerEntry, CommodityEntries, CommodityType, PetBroker, PetBrokerEntry, Stock
Services/New Magincia/Magincia Bazaar/Gumps/BaseBazaarGump.cs  <- CommodityTargetGump
Services/New Magincia/Magincia Bazaar/Items/PlotSign.cs  <- Auction, AuctionEnd, BaseBazaarGump, MaginciaBazaarPlot, PlotDef, ShopRecallRuneGump, StallLeasingGump
Services/New Magincia/Magincia Bazaar/Mobiles/BaseBizaarBroker.cs  <- AddInventoryToWarehouse, DefaultComissionFee, MaginciaBazaar, MaginciaBazaarPlot
Services/New Magincia/Magincia Bazaar/Mobiles/CommodityBroker.cs  <- BankBalance, BaseBazaarBroker, BuyPricePer, ComissionFee, CommodityBrokerEntry, CommodityBrokerGump, CommodityInventoryGump, CommodityType, MaginciaBazaarPlot, Plot, SellPricePer, Stock
Services/New Magincia/Magincia Bazaar/Mobiles/WarehouseSuperintendent.cs  <- BazaarInformationGump, CommodityTypes, Funds, GetStorageEntry, MaginciaBazaar, MatchBidGump, RemoveCommodity, RemoveFromStorage, RemovePet, StorageEntry
Services/New Magincia/MaginciaPlants/GardeningContract.cs  <- ContractTime, IsContract, MaginciaPlantItem
Services/New Magincia/MaginciaPlants/MaginciaPlantItem.cs  <- MaginciaPlantSystem, OnPlantDelete
Services/New Magincia/MaginciaPlants/MaginciaPlantSystem.cs  <- MagHousingZones, MaginciaLottoSystem, MaginciaPlantItem
```


#### CC7 Decoration/housing (the 297) — needs ServUO files from outside this row (5 files)

```
Items/Addons/ParoxysmusSwampDragonStatuette.cs  <- ParoxysmusSwampDragon
Items/Addons/TheKingsCollection/BarrelSponge.cs  <- ExplodingTarPotion, FearEssence, ShatterPotion
Items/Decorative/CustomizableRoundedDoorMat.cs  <- AddCustomizableMessageGump, EditSign, ICustomizableMessageItem
Items/Decorative/CustomizableWallSign.cs  <- AddCustomizableMessageGump, EditSign, ICustomizableMessageItem
Items/Decorative/ValentineBear.cs  <- AddCustomizableMessageGump, ICustomizableMessageItem
```


#### CC7 Decoration/housing (the 297) — needs an upstream member, a carrier, or reading (89 files)

```
Items/Addons/BlueMarbleFireplace.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/BuffetTable.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/ClawFootTub.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/Craft Addons/EnchantedSculptingTool.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/Craft Addons/GlassKiln.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/Crystal Furniture Set/CrystalBeggarStatue.cs  <- upstream: DirectionType
Items/Addons/Crystal Furniture Set/CrystalBullStatue.cs  <- upstream: DirectionType
Items/Addons/Crystal Furniture Set/CrystalRunnerStatue.cs  <- upstream: DirectionType
Items/Addons/Crystal Furniture Set/CrystalSupplicantStatue.cs  <- upstream: DirectionType
Items/Addons/Crystal Furniture Set/CrystalTable.cs  <- upstream: DirectionType
Items/Addons/Crystal Furniture Set/CrystalThrone.cs  <- upstream: DirectionType
Items/Addons/DawnsMusicBox/RewardVersion/MusicBoxGears.cs  <- upstream: AddSong | unknown: UnCommon
Items/Addons/DawnsMusicBox/RewardVersion/TrackInfo.cs  <- unknown: UnCommon
Items/Addons/DolphinRug.cs  <- unknown: EastLarge, SouthLarge
Items/Addons/DungeonHitchingPost.cs  <- upstream: Allured | unknown: Insensitive
Items/Addons/ElvenSpinningwheelEastAddon.cs  <- unknown: TwoFiftyMS
Items/Addons/ElvenSpinningwheelSouthAddon.cs  <- unknown: TwoFiftyMS
Items/Addons/EnchantedGraniteCart.cs  <- upstream: AddonOptionGump, DirectionType, OneSecond
Items/Addons/EnormousVenusFlytrap.cs  <- unknown: Distinct, FlipableAddon | also needs: AppraiseforCleanupTarget, AwardPoints, CleanUpBritannia, CleanUpBritanniaData, CleanupArray, GetPoints, PointsSystem
Items/Addons/FormalDiningTable.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/GadgetryTable.cs  <- upstream: AddonOptionGump, DirectionType | also needs: IRepairableMobile
Items/Addons/GargishCotEastAddon.cs  <- unknown: Mondain
Items/Addons/GargishCotSouthAddon.cs  <- unknown: Mondain
Items/Addons/GargishCouchEastAddon.cs  <- unknown: Mondain
Items/Addons/GargishCouchSouthAddon.cs  <- unknown: Mondain
Items/Addons/GargishLongTableEastAddon.cs  <- unknown: Mondain
Items/Addons/GargishLongTableSouthAddon.cs  <- unknown: Mondain
Items/Addons/GoldMarbleFireplace.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/GreenMarbleFireplace.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/Harpsichord.cs  <- upstream: AddonOptionGump, DirectionType, StopMusic | unknown: DarkPurple, DarkRed | also needs: Brown
Items/Addons/HitchingPost.cs  <- upstream: Allured | unknown: Insensitive, Mondain
Items/Addons/KoiPond.cs  <- unknown: Large, Small
Items/Addons/LargeGargoyleBedEastAddon.cs  <- unknown: Mondain
Items/Addons/LargeGargoyleBedSouthAddon.cs  <- unknown: Mondain
Items/Addons/LighthouseAddon.cs  <- upstream: BoatItem | also needs: BaseGalleon, GalleonHold, GetEntitiesOnBoard, IsClassicBoat, IsComponentItem, OnDryDock
Items/Addons/PetParrot.cs  <- unknown: FruitsAndVegies | also needs: ParrotWafer
Items/Addons/PicnicBlanket.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/RepairBench.cs  <- upstream: AddonOptionGump, DirectionType, RepairSkill
Items/Addons/RoastingPigOnASpit.cs  <- upstream: AddonOptionGump, DirectionType, PulledPorkPlatter, PulledPorkSandwich
Items/Addons/RoseRug.cs  <- unknown: EastLarge, SouthLarge
Items/Addons/Shadow Furniture Set/FireDemonStatue.cs  <- unknown: FlipableAddon
Items/Addons/Shadow Furniture Set/ShadowAltar.cs  <- upstream: DirectionType
Items/Addons/Shadow Furniture Set/ShadowBanner.cs  <- upstream: DirectionType
Items/Addons/Shadow Furniture Set/SpikePost.cs  <- unknown: FlipableAddon
Items/Addons/SkullRug.cs  <- unknown: EastLarge, SouthLarge | also needs: Siege, SiegeShard
Items/Addons/SpinningwheelEastAddon.cs  <- unknown: TwoFiftyMS
Items/Addons/SpinningwheelSouthAddon.cs  <- unknown: TwoFiftyMS
Items/Addons/TheKingsCollection/15thAnniversaryLithograph.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/AlchemistsBookshelf.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/BullTapestry.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/CastlePainting.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/EmbroideredTapestry.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/FirePainting.cs  <- upstream: AddonOptionGump, DirectionType | also needs: ScrollOfTranscendence
Items/Addons/TheKingsCollection/FourPostBed.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/GoldenTable.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/HorsePainting.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/MarbleTable.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/MonasteryBell.cs  <- upstream: AddonOptionGump, DirectionType, InstrumentedAddonComponent
Items/Addons/TheKingsCollection/OrnateBed.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/TheKingsCollection/ShipPainting.cs  <- upstream: AddonOptionGump, DirectionType | also needs: HeavyPowderCharge
Items/Addons/TinkerBench.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/WashBasin.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/WaterWheel.cs  <- upstream: AddonOptionGump, DirectionType
Items/Addons/WoodStove.cs  <- upstream: AddonOptionGump, DirectionType
Items/Decorative/CraftableFurniture.cs  <- upstream: TitleName | unknown: PeekInt
Items/Decorative/CustomizableSquaredDoorMat.cs  <- upstream: AddonOptionGump, DirectionType | also needs: EditSign, ICustomizableMessageItem
Items/Decorative/DecorativeCarpet.cs  <- upstream: Carpets
Items/Decorative/DecorativeStableSet/MetalTub.cs  <- upstream: AddonOptionGump, DirectionType
Items/Decorative/DesCityWall.cs  <- unknown: VeryEasy | also needs: DamageableItem, ItemLevel
Items/Decorative/Fur.cs  <- unknown: LightBrown | also needs: Brown, FurType
Items/Decorative/GargoyleShortTableAddon.cs  <- unknown: Mondain
Items/Decorative/SAShadowWall1.cs  <- unknown: VeryEasy | also needs: DamageableItem, ItemLevel
Items/Decorative/SAStoneWall1.cs  <- unknown: VeryEasy | also needs: DamageableItem, ItemLevel
Items/Decorative/SAStoneWall2.cs  <- unknown: VeryEasy | also needs: DamageableItem, ItemLevel
Items/Decorative/SpikedEggNog.cs  <- unknown: TwoFiftyMS
Items/Decorative/Utensils.cs  <- upstream: TitleName | unknown: Vars
Services/New Magincia/Distillation/CraftDefinition.cs  <- unknown: Brandy
Services/New Magincia/Distillation/DistillationContext.cs  <- unknown: WheatBased
Services/New Magincia/Distillation/DistillationGump.cs  <- unknown: Brandy, WaterBased, WheatBased
Services/New Magincia/Distillation/DistillationSystem.cs  <- unknown: Akvavit, Brandy, Spirytus, WaterBased, WheatBased
Services/New Magincia/Distillation/Items/LiquorBarrel.cs  <- unknown: Akvavit, Spirytus
Services/New Magincia/Housing Lotto/Core/MaginciaLottoSystem.cs  <- unknown: LoginEventHandler, OneMinute | also needs: Login
Services/New Magincia/Housing Lotto/Gumps/MaginciaLottoGump.cs  <- unknown: TextRelay
Services/New Magincia/Magincia Bazaar/Core/MaginciaBizaar.cs  <- unknown: OneMinute
Services/New Magincia/Magincia Bazaar/Gumps/BizaarSignGump.cs  <- unknown: TextRelay
Services/New Magincia/Magincia Bazaar/Gumps/CommodityBrokerGump.cs  <- unknown: TextRelay
Services/New Magincia/Magincia Bazaar/Gumps/PetBrokerGumps.cs  <- unknown: SkillHandlers, TextRelay | also needs: NewAnimalLoreGump, PetTrainingHelper
Services/New Magincia/Magincia Bazaar/Mobiles/PetBroker.cs  <- unknown: OneMinute
Services/New Magincia/MaginciaPlants/Hoe.cs  <- unknown: AnimationType
```


#### CC7 Decoration/housing (the 297) — extra ServUO files the co-port bucket pulls in (49 files)

```
Gumps/AddCustomizableMessageGump.cs
Gumps/BaseRewardGump.cs
Items/Consumables/ExplodingTarPotion.cs
Items/Consumables/FearEssence.cs
Items/Consumables/ParrotWafer.cs
Items/Consumables/ScrollofTranscendence.cs
Items/Consumables/ShatterPotion.cs
Items/Containers/BaseTrash.cs
Items/Damageable/DamageableItem.cs
Misc/Siege.cs
Mobiles/MobileInterfaces.cs
Mobiles/NPCs/BaseTurnInMobile.cs
Mobiles/Normal/HighPlainsBoura.cs
Mobiles/Normal/Kepetch.cs
Mobiles/Normal/KepetchAmbusher.cs
Mobiles/Normal/LowlandBoura.cs
Mobiles/Normal/ParoxysmusSwampDragon.cs
Mobiles/Normal/RuddyBoura.cs
Services/BulkOrders/BulkOrderSystem.cs
Services/BulkOrders/Rewards/RewardsGump.cs
Services/CleanUpBritannia/Gumps.cs
Services/Expansions/High Seas/Items/Cannons and Ammo/PowderCharge.cs
Services/Expansions/High Seas/Multis/BaseGalleon.cs
Services/Expansions/High Seas/Multis/GalleonHold.cs
Services/Expansions/High Seas/Multis/Rowboat.cs
Services/HuntmasterChallenge/HuntMasterRewardGump.cs
Services/Pet Training/Gumps.cs
Services/Pet Training/PetTrainingHelper.cs
Services/PointsSystems/CleanUpBritanniaData.cs
Services/PointsSystems/PointsSystem.cs
Services/RemoteAdmin/Packets.cs
Services/Revamped Dungeons/BlackthornDungeon/Creatures/AgentoftheCrown.cs
Services/Revamped Dungeons/BlackthornDungeon/Gumps.cs
Services/Revamped Dungeons/Covetous Void Spawn/Gumps.cs
Services/Seasonal Events/ForsakenFoes/Gumps.cs
Services/Seasonal Events/ForsakenFoes/Items/PumpkinRowboat.cs
Services/Seasonal Events/RisingTide/BlackMarketMerchant.cs
Services/Seasonal Events/RisingTide/RewardsGump.cs
Services/Seasonal Events/TreasuresOfDoom/Mobiles/Carey.cs
Services/Seasonal Events/TreasuresOfDoom/RewardGump.cs
Services/Seasonal Events/TreasuresOfKhaldun/Gumps.cs
Services/Seasonal Events/TreasuresOfKhaldun/KhaldunResearcher.cs
Services/Seasonal Events/TreasuresOfKotlCity/Mobiles/Hal.cs
Services/Seasonal Events/TreasuresOfKotlCity/RewardGump.cs
Services/Seasonal Events/TreasuresOfSorceresDungeon/RewardGump.cs
Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonResearcher.cs
Services/Underworld/ExperimentalRoom/ExperimentalGem.cs
Services/ViceVsVirtue/Gumps/RewardGump.cs
Services/XmlSpawner/XmlSpawner Core/XmlQuest/XmlQuestPoints.cs
```


#### CC7 Decoration/housing (the 297) — filtered out at step 1: ModernUO or our tree already declares the primary type (442 files)

```
Items/Addons/AbbatoirAddon.cs
Items/Addons/AddonComponent.cs
Items/Addons/AddonContainerComponent.cs
Items/Addons/AlchemistTableEastAddon.cs
Items/Addons/AlchemistTableSouthAddon.cs
Items/Addons/AnkhOfSacrifice.cs
Items/Addons/AnvilEastAddon.cs
Items/Addons/AnvilSouthAddon.cs
Items/Addons/AppleTrunk.cs
Items/Addons/Aquarium/Aquarium.cs
Items/Addons/Aquarium/AquariumFood.cs
Items/Addons/Aquarium/AquariumGump.cs
Items/Addons/Aquarium/AquariumState.cs
Items/Addons/Aquarium/Fish/AlbinoCourtesanFish.cs
Items/Addons/Aquarium/Fish/AlbinoFrog.cs
Items/Addons/Aquarium/Fish/BritainCrownFish.cs
Items/Addons/Aquarium/Fish/FandancerFish.cs
Items/Addons/Aquarium/Fish/GoldenBroadtail.cs
Items/Addons/Aquarium/Fish/Jellyfish.cs
Items/Addons/Aquarium/Fish/KillerFrog.cs
Items/Addons/Aquarium/Fish/LongClawCrab.cs
Items/Addons/Aquarium/Fish/MakotoCourtesanFish.cs
Items/Addons/Aquarium/Fish/MinocBlueFish.cs
Items/Addons/Aquarium/Fish/NujelmHoneyFish.cs
Items/Addons/Aquarium/Fish/PurpleFrog.cs
Items/Addons/Aquarium/Fish/RedDartFish.cs
Items/Addons/Aquarium/Fish/Shrimp.cs
Items/Addons/Aquarium/Fish/SmallMouthSuckerFin.cs
Items/Addons/Aquarium/Fish/SpeckledCrab.cs
Items/Addons/Aquarium/Fish/SpinedScratcherFish.cs
Items/Addons/Aquarium/Fish/SpottedBuccaneer.cs
Items/Addons/Aquarium/Fish/VesperReefTiger.cs
Items/Addons/Aquarium/Fish/YellowFinBluebelly.cs
Items/Addons/Aquarium/FishBowl.cs
Items/Addons/Aquarium/Reward Fish/BrineShrimp.cs
Items/Addons/Aquarium/Reward Fish/Coral.cs
Items/Addons/Aquarium/Reward Fish/FullMoonFish.cs
Items/Addons/Aquarium/Reward Fish/SeaHorse.cs
Items/Addons/Aquarium/Reward Fish/StrippedFlakeFish.cs
Items/Addons/Aquarium/Reward Fish/StrippedSosarianSwill.cs
Items/Addons/Aquarium/Rewards/AquariumMessage.cs
Items/Addons/Aquarium/Rewards/CaptainBlackheartsFishingPole.cs
Items/Addons/Aquarium/Rewards/CraftysFishingHat.cs
Items/Addons/Aquarium/Rewards/FishBones.cs
Items/Addons/Aquarium/Rewards/IslandStatue.cs
Items/Addons/Aquarium/Rewards/Shell.cs
Items/Addons/Aquarium/Rewards/ToyBoat.cs
Items/Addons/Aquarium/Rewards/WaterloggedBoots.cs
Items/Addons/Aquarium/VacationWafer.cs
Items/Addons/ArcaneBookshelfEastAddon.cs
Items/Addons/ArcaneBookshelfSouthAddon.cs
Items/Addons/ArcaneCircleAddon.cs
Items/Addons/ArcanistStatueEastAddon.cs
Items/Addons/ArcanistStatueSouthAddon.cs
Items/Addons/ArcheryButteAddon.cs
Items/Addons/AwesomeDisturbingPortrait.cs
Items/Addons/BallotBox.cs
Items/Addons/Banner.cs
Items/Addons/BaseAddon.cs
Items/Addons/BaseAddonContainer.cs
Items/Addons/BaseAddonContainerDeed.cs
Items/Addons/BaseAddonDeed.cs
Items/Addons/BearRugs.cs
Items/Addons/BedOfNails.cs
Items/Addons/BloodPentagram.cs
Items/Addons/BloodyPentagram.cs
Items/Addons/BlueDecorativeRug.cs
Items/Addons/BlueFancyRug.cs
Items/Addons/BluePlainRug.cs
Items/Addons/BoneCouch.cs
Items/Addons/BoneTable.cs
Items/Addons/BoneThrone.cs
Items/Addons/Brazier.cs
Items/Addons/BrokenArmoire.cs
Items/Addons/BrokenBed.cs
Items/Addons/BrokenBookcase.cs
Items/Addons/BrokenChestOfDrawers.cs
Items/Addons/BrokenCoveredChair.cs
Items/Addons/BrokenFallenChair.cs
Items/Addons/BrokenVanity.cs
Items/Addons/Cannon.cs
Items/Addons/CherryBlossomTree.cs
Items/Addons/CherryBlossomTrunk.cs
Items/Addons/CinnamonFancyRug.cs
Items/Addons/ColoredAnvil.cs
Items/Addons/ContestMiniHouse.cs
Items/Addons/CreepyPortrait.cs
Items/Addons/Curtains.cs
Items/Addons/DartBoard.cs
Items/Addons/DawnsMusicBox/DawnsMusicBox.cs
Items/Addons/DawnsMusicBox/DawnsMusicGear.cs
Items/Addons/DawnsMusicBox/DawnsMusicInfo.cs
Items/Addons/DawnsMusicBox/RewardVersion/DawnsMusicBox.cs
Items/Addons/DecorativeShield.cs
Items/Addons/DisturbingPortrait.cs
Items/Addons/ElvenBedEastAddon.cs
Items/Addons/ElvenBedSouthAddon.cs
Items/Addons/ElvenDresserEastAddon.cs
Items/Addons/ElvenDresserSouthAddon.cs
Items/Addons/ElvenForgeAddon.cs
Items/Addons/ElvenLoveseatEastAddon.cs
Items/Addons/ElvenLoveseatSouthAddon.cs
Items/Addons/ElvenStoveEastAddon.cs
Items/Addons/ElvenStoveSouthAddon.cs
Items/Addons/ElvenWashbasinEastAddon.cs
Items/Addons/ElvenWashbasinSouthAddon.cs
Items/Addons/FancyElvenTableEastAddon.cs
Items/Addons/FancyElvenTableSouthAddon.cs
Items/Addons/FireColumnAddon.cs
Items/Addons/FlamingHead.cs
Items/Addons/FlourMillEastAddon.cs
Items/Addons/FlourMillSouthAddon.cs
Items/Addons/FlowerTapestries.cs
Items/Addons/Fountain.cs
Items/Addons/FountainOfFortune.cs
Items/Addons/FountainOfLife.cs
Items/Addons/FruitTrees.cs
Items/Addons/GiantWebs.cs
Items/Addons/GingerBreadHouseDeed.cs
Items/Addons/GoldenDecorativeRug.cs
Items/Addons/GozaMats.cs
Items/Addons/GrayBrickFireplaceEastAddon.cs
Items/Addons/GrayBrickFireplaceSouthAddon.cs
Items/Addons/Guildstone.cs
Items/Addons/Guillotine.cs
Items/Addons/GuillotineComponent.cs
Items/Addons/HagCauldron.cs
Items/Addons/HagStew.cs
Items/Addons/HangingAxes.cs
Items/Addons/HangingSkeleton.cs
Items/Addons/HangingSwords.cs
Items/Addons/HauntedMirror.cs
Items/Addons/HavenCannon.cs
Items/Addons/HearthOfHomeFire.cs
Items/Addons/HolidayPottedPlant.cs
Items/Addons/HolidayTree.cs
Items/Addons/HouseLadder.cs
Items/Addons/IronMaiden.cs
Items/Addons/JackOLantern.cs
Items/Addons/LargeBedEastAddon.cs
Items/Addons/LargeBedSouthAddon.cs
Items/Addons/LargeFishingNet.cs
Items/Addons/LargeForgeEastAddon.cs
Items/Addons/LargeForgeSouthAddon.cs
Items/Addons/LargeStoneTableEastAddon.cs
Items/Addons/LargeStoneTableSouthAddon.cs
Items/Addons/LoomEastAddon.cs
Items/Addons/LoomSouthAddon.cs
Items/Addons/MediumStoneTableEastAddon.cs
Items/Addons/MediumStoneTableSouthAddon.cs
Items/Addons/MiniHouses.cs
Items/Addons/MiningCart.cs
Items/Addons/MinotaurStatue.cs
Items/Addons/MountedPixieBlue.cs
Items/Addons/MountedPixieGreen.cs
Items/Addons/MountedPixieLime.cs
Items/Addons/MountedPixieOrange.cs
Items/Addons/MountedPixieWhite.cs
Items/Addons/OrnateElvenChestEastAddon.cs
Items/Addons/OrnateElvenChestSouthAddon.cs
Items/Addons/OrnateElvenTableEastAddon.cs
Items/Addons/OrnateElvenTableSouthAddon.cs
Items/Addons/ParrotPerchAddon.cs
Items/Addons/PeachTrunk.cs
Items/Addons/PentagramAddon.cs
Items/Addons/PickpocketDips.cs
Items/Addons/PinkFancyRug.cs
Items/Addons/PlayerBulletinBoards.cs
Items/Addons/PottedCactus.cs
Items/Addons/PyramidAddon.cs
Items/Addons/RedPlainRug.cs
Items/Addons/RejuvinationAnkhs.cs
Items/Addons/SHTeleporter.cs
Items/Addons/SacrificialAltar.cs
Items/Addons/SandstoneFireplaceEastAddon.cs
Items/Addons/SandstoneFireplaceSouthAddon.cs
Items/Addons/SandstoneFountainAddon.cs
Items/Addons/Scarecrow.cs
Items/Addons/SerpentPillarAddon.cs
Items/Addons/ShrineOfWisdomAddon.cs
Items/Addons/SkullPileAddon.cs
Items/Addons/SmallBedEastAddon.cs
Items/Addons/SmallBedSouthAddon.cs
Items/Addons/SmallFishingNet.cs
Items/Addons/SmallForgeAddon.cs
Items/Addons/SolenAntHole.cs
Items/Addons/SquirrelStatueEastAddon.cs
Items/Addons/SquirrelStatueSouthAddon.cs
Items/Addons/StandingBrokenChair.cs
Items/Addons/Statue.cs
Items/Addons/StoneAnkh.cs
Items/Addons/StoneFireplaceEastAddon.cs
Items/Addons/StoneFireplaceSouthAddon.cs
Items/Addons/StoneFountainAddon.cs
Items/Addons/StoneOvenEastAddon.cs
Items/Addons/StoneOvenSouthAddon.cs
Items/Addons/StretchedHides.cs
Items/Addons/SuitOfGoldArmor.cs
Items/Addons/SuitOfSilverArmor.cs
Items/Addons/TableWithBlueCloth.cs
Items/Addons/TableWithOrangeCloth.cs
Items/Addons/TableWithPurpleCloth.cs
Items/Addons/TableWithRedCloth.cs
Items/Addons/TallElvenBedEastAddon.cs
Items/Addons/TallElvenBedSouthAddon.cs
Items/Addons/TapestryOfSosaria.cs
Items/Addons/Telescope.cs
Items/Addons/TrainingDummies.cs
Items/Addons/TreeStump.cs
Items/Addons/UnmadeBed.cs
Items/Addons/UnsettlingPortrait.cs
Items/Addons/WallBanner.cs
Items/Addons/WallTorch.cs
Items/Addons/WarriorStatueEastAddon.cs
Items/Addons/WarriorStatueSouthAddon.cs
Items/Addons/WaterTroughEastAddon.cs
Items/Addons/WaterTroughSouthAddon.cs
Items/Addons/WaterVat.cs
Items/Addons/WoodenCoffin.cs
Items/Addons/Wreath.cs
Items/Decorative/AngelDecoration.cs
Items/Decorative/ArrowShafts.cs
Items/Decorative/BaseImprisonedMobile.cs
Items/Decorative/BaseLight.cs
Items/Decorative/BasePaintedMask.cs
Items/Decorative/BasePiece.cs
Items/Decorative/BaseSign.cs
Items/Decorative/BaseWall.cs
Items/Decorative/Benchs.cs
Items/Decorative/Blood.cs
Items/Decorative/BottlesOfLiquor.cs
Items/Decorative/Brazier.cs
Items/Decorative/BrazierTall.cs
Items/Decorative/BrokenChair.cs
Items/Decorative/Candelabra.cs
Items/Decorative/CandelabraStand.cs
Items/Decorative/CandleLarge.cs
Items/Decorative/CandleLong.cs
Items/Decorative/CandleShort.cs
Items/Decorative/CandleSkull.cs
Items/Decorative/Cards.cs
Items/Decorative/Cards2.cs
Items/Decorative/Cards3.cs
Items/Decorative/Cards4.cs
Items/Decorative/Cards5.cs
Items/Decorative/ChairInAGhostCostume.cs
Items/Decorative/Chairs.cs
Items/Decorative/Checkers.cs
Items/Decorative/Checkers2.cs
Items/Decorative/Chessmen.cs
Items/Decorative/Chessmen2.cs
Items/Decorative/Chessmen3.cs
Items/Decorative/ClownMask.cs
Items/Decorative/ColoredSmallWebs.cs
Items/Decorative/CrossbowBolts.cs
Items/Decorative/CupidStatue.cs
Items/Decorative/DaemonMask.cs
Items/Decorative/DarkSource.cs
Items/Decorative/DarkWoodWall.cs
Items/Decorative/DecoBlackmoor.cs
Items/Decorative/DecoBloodspawn.cs
Items/Decorative/DecoBrimstone.cs
Items/Decorative/DecoCrystalBall.cs
Items/Decorative/DecoDeckOfTarot.cs
Items/Decorative/DecoDeckOfTarot2.cs
Items/Decorative/DecoDragonsBlood.cs
Items/Decorative/DecoDragonsBlood2.cs
Items/Decorative/DecoEyeOfNewt.cs
Items/Decorative/DecoFlower.cs
Items/Decorative/DecoFlower2.cs
Items/Decorative/DecoGarlic.cs
Items/Decorative/DecoGarlic2.cs
Items/Decorative/DecoGarlicBulb.cs
Items/Decorative/DecoGarlicBulb2.cs
Items/Decorative/DecoGinseng.cs
Items/Decorative/DecoGinseng2.cs
Items/Decorative/DecoGinsengRoot.cs
Items/Decorative/DecoGinsengRoot2.cs
Items/Decorative/DecoGoldIngot.cs
Items/Decorative/DecoGoldIngot2.cs
Items/Decorative/DecoGoldIngots.cs
Items/Decorative/DecoGoldIngots2.cs
Items/Decorative/DecoGoldIngots3.cs
Items/Decorative/DecoGoldIngots4.cs
Items/Decorative/DecoHay.cs
Items/Decorative/DecoHay2.cs
Items/Decorative/DecoHorseDung.cs
Items/Decorative/DecoIronIngot.cs
Items/Decorative/DecoIronIngot2.cs
Items/Decorative/DecoIronIngots.cs
Items/Decorative/DecoIronIngots2.cs
Items/Decorative/DecoIronIngots3.cs
Items/Decorative/DecoIronIngots4.cs
Items/Decorative/DecoIronIngots5.cs
Items/Decorative/DecoIronIngots6.cs
Items/Decorative/DecoMagicalCrystal.cs
Items/Decorative/DecoMandrake.cs
Items/Decorative/DecoMandrake2.cs
Items/Decorative/DecoMandrake3.cs
Items/Decorative/DecoMandrakeRoot.cs
Items/Decorative/DecoMandrakeRoot2.cs
Items/Decorative/DecoNightshade.cs
Items/Decorative/DecoNightshade2.cs
Items/Decorative/DecoNightshade3.cs
Items/Decorative/DecoObsidian.cs
Items/Decorative/DecoPumice.cs
Items/Decorative/DecoRock.cs
Items/Decorative/DecoRock2.cs
Items/Decorative/DecoRocks.cs
Items/Decorative/DecoRocks2.cs
Items/Decorative/DecoRoseOfTrinsic.cs
Items/Decorative/DecoRoseOfTrinsic2.cs
Items/Decorative/DecoRoseOfTrinsic3.cs
Items/Decorative/DecoSilverIngot.cs
Items/Decorative/DecoSilverIngot2.cs
Items/Decorative/DecoSilverIngots.cs
Items/Decorative/DecoSilverIngots2.cs
Items/Decorative/DecoSilverIngots3.cs
Items/Decorative/DecoSilverIngots4.cs
Items/Decorative/DecoSilverIngots5.cs
Items/Decorative/DecoSpittoon.cs
Items/Decorative/DecoTarot.cs
Items/Decorative/DecoTarot2.cs
Items/Decorative/DecoTarot3.cs
Items/Decorative/DecoTarot4.cs
Items/Decorative/DecoTarot5.cs
Items/Decorative/DecoTarot6.cs
Items/Decorative/DecoTarot7.cs
Items/Decorative/DecoWyrmsHeart.cs
Items/Decorative/DecorativeShield.cs
Items/Decorative/DecorativeTopiary.cs
Items/Decorative/DecorativeWeapon.cs
Items/Decorative/ElvenPodium.cs
Items/Decorative/EmptyJars.cs
Items/Decorative/EmptyPots.cs
Items/Decorative/EmptyToolKit.cs
Items/Decorative/EmptyToolKit2.cs
Items/Decorative/EternallyCorruptTree.cs
Items/Decorative/EvilJesterMask.cs
Items/Decorative/ExcellentIronMaiden.cs
Items/Decorative/ExecutionersCap.cs
Items/Decorative/FestiveCactus.cs
Items/Decorative/Floors.cs
Items/Decorative/FullJars.cs
Items/Decorative/GiantReplicaAcorn.cs
Items/Decorative/GlassItems.cs
Items/Decorative/GlobOfMonstreousInterredGrizzle.cs
Items/Decorative/Globe.cs
Items/Decorative/GrimWarning.cs
Items/Decorative/GrizzledSkullCollection.cs
Items/Decorative/HalfEmptyJars.cs
Items/Decorative/HalloweenGuillotine.cs
Items/Decorative/HalloweenPumpkin.cs
Items/Decorative/HangingLantern.cs
Items/Decorative/HeatingStand.cs
Items/Decorative/HolidayBell.cs
Items/Decorative/HoveringWisp.cs
Items/Decorative/Icecicles.cs
Items/Decorative/IcyPatch.cs
Items/Decorative/LampPost1.cs
Items/Decorative/LampPost2.cs
Items/Decorative/LampPost3.cs
Items/Decorative/LightOfTheWinterSolstice.cs
Items/Decorative/LightSource.cs
Items/Decorative/LocalizedSign.cs
Items/Decorative/Lockpicks.cs
Items/Decorative/MangledHeadOfDreadhorn.cs
Items/Decorative/MeltedWax.cs
Items/Decorative/MinotaurHedge.cs
Items/Decorative/Mistletoe.cs
Items/Decorative/MonsterStatuette.cs
Items/Decorative/MonsterousInterredGrizzleMaggots.cs
Items/Decorative/MountedDreadHorn.cs
Items/Decorative/Obelisk.cs
Items/Decorative/Origami.cs
Items/Decorative/PKHolidayStuff.cs
Items/Decorative/PaintingPortraits.cs
Items/Decorative/PaperLantern.cs
Items/Decorative/ParoxysmusCorrodedStein.cs
Items/Decorative/ParoxysmusDinner.cs
Items/Decorative/PileOfGlacialSnow.cs
Items/Decorative/PlagueMask.cs
Items/Decorative/PlayingCards.cs
Items/Decorative/PlayingCards2.cs
Items/Decorative/PorcelainMask.cs
Items/Decorative/PottedCactus.cs
Items/Decorative/PottedPlants.cs
Items/Decorative/PottedTrees.cs
Items/Decorative/PumpkinScarecrow.cs
Items/Decorative/Rares.cs
Items/Decorative/RarewoodChest.cs
Items/Decorative/RedHangingLantern.cs
Items/Decorative/RockingHorse.cs
Items/Decorative/RoseInAVase.cs
Items/Decorative/RoundPaperLantern.cs
Items/Decorative/RuinedItemSingle.cs
Items/Decorative/RuinedTapestry.cs
Items/Decorative/Screens.cs
Items/Decorative/ShipwreckedItem.cs
Items/Decorative/ShojiLantern.cs
Items/Decorative/Sign.cs
Items/Decorative/SkullsOnPike.cs
Items/Decorative/SnowGlobes.cs
Items/Decorative/SnowPile.cs
Items/Decorative/SnowPiles.cs
Items/Decorative/SnowStatue.cs
Items/Decorative/Snowflakes.cs
Items/Decorative/Snowman.cs
Items/Decorative/SnowyTree.cs
Items/Decorative/Static.cs
Items/Decorative/Statues.cs
Items/Decorative/Stools.cs
Items/Decorative/StringOfPartsOfParoxysmusVictims.cs
Items/Decorative/SubtextSign.cs
Items/Decorative/SweatOfParoxysmus.cs
Items/Decorative/Tables.cs
Items/Decorative/TaintedMushroom.cs
Items/Decorative/Tapestry.cs
Items/Decorative/ThickGrayStoneWall.cs
Items/Decorative/ThinBrickWall.cs
Items/Decorative/ThinStoneWall.cs
Items/Decorative/ThorvaldsMedallion.cs
Items/Decorative/Thrones.cs
Items/Decorative/TombstoneOfTheDamned.cs
Items/Decorative/ToolKit.cs
Items/Decorative/TormentedChains.cs
Items/Decorative/TravestysCollectionOfShells.cs
Items/Decorative/TravestysFineTeakwoodTray.cs
Items/Decorative/TravestysSushiPreparations.cs
Items/Decorative/Tray2.cs
Items/Decorative/Trays.cs
Items/Decorative/UnfinishedBarrel.cs
Items/Decorative/ValentinesCard.cs
Items/Decorative/Vase.cs
Items/Decorative/Vines.cs
Items/Decorative/WallSconce.cs
Items/Decorative/WallTorch.cs
Items/Decorative/WhiteHangingLantern.cs
Items/Decorative/WhiteStoneWall.cs
Items/Decorative/WindChimes.cs
Items/Decorative/WritingTable.cs
Services/New Magincia/Housing Lotto/Core/Region.cs
```


### CC7 as written (+Resource, +BulkOrders)

Prefixes: `Items/Resource`, `Services/BulkOrders`  
raw 191 → filtered out 134 → candidates 57  
drops straight in 33 · needs another row file 0 · co-port 5 · upstream/carrier 19


#### CC7 as written (+Resource, +BulkOrders) — drops straight in (33 files)

```
Items/Resource/AbyssalCloth.cs
Items/Resource/AnimalPheromone.cs
Items/Resource/Blackrock.cs
Items/Resource/BloodOfTheDarkFather.cs
Items/Resource/DragonBlood.cs
Items/Resource/EssencePersistence.cs
Items/Resource/EtherealSand.cs
Items/Resource/FeyWings.cs
Items/Resource/HotGoo.cs
Items/Resource/IGem.cs
Items/Resource/LiveRock.cs
Items/Resource/MedusaBlood.cs
Items/Resource/MedusaDarkScales.cs
Items/Resource/MedusaLightScales.cs
Items/Resource/OceanSapphire.cs
Items/Resource/PolishedMeteorite.cs
Items/Resource/PrimalLichDust.cs
Items/Resource/SilverSerpentVenom.cs
Items/Resource/SlithEye.cs
Items/Resource/SmallFish.cs
Items/Resource/ToxicVenomSac.cs
Items/Resource/VileTentacles.cs
Items/Resource/VoidCore.cs
Items/Resource/VoidEssence.cs
Items/Resource/WoodPulp.cs
Items/Resource/WorkableGlass.cs
Services/BulkOrders/Items/GuaranteedSpellbookImprovementTalisman.cs
Services/BulkOrders/Items/MasterChefsApron.cs
Services/BulkOrders/Items/MasterCraftsmanTalisman.cs
Services/BulkOrders/Items/PowderOfFortKeg.cs
Services/BulkOrders/Items/RockHammer.cs
Services/BulkOrders/LargeBODs/LargeBODTarget.cs
Services/BulkOrders/SmallBODs/SmallBODTarget.cs
```


#### CC7 as written (+Resource, +BulkOrders) — portable once other files in this row come with it (0 files)

```
```


#### CC7 as written (+Resource, +BulkOrders) — needs ServUO files from outside this row (5 files)

```
Items/Resource/PlantClippings.cs  <- IPlantHue
Services/BulkOrders/Items/BODRewardTitleDeed.cs  <- BaseRewardTitleDeed
Services/BulkOrders/Items/DrSpectorsLenses.cs  <- Glasses
Services/BulkOrders/Items/KotlBlackRod.cs  <- GargishGnarledStaff
Services/BulkOrders/Rewards/ConfirmBankPointsGump.cs  <- ConfirmCallbackGump
```


#### CC7 as written (+Resource, +BulkOrders) — needs an upstream member, a carrier, or reading (19 files)

```
Items/Resource/FocusingGemOfVirtueBane.cs  <- upstream: Brittle, NegativeAttributes | also needs: ExtendedWeaponAttributes
Items/Resource/ScouringToxin.cs  <- upstream: BasketWeaving | also needs: DryReeds, SoftenedReeds
Services/BulkOrders/BulkOrderSystem.cs  <- upstream: AlchemyRewardCalculator, BuyPrices, CarpentryRewardCalculator, CookingRewardCalculator, FletchingRewardCalculator, GetRacialSkillBonus, InscriptionRewardCalculator, RewardCollection, TinkeringRewardCalculator | also needs: CollectionItem, EnchantedApple, MetalContainerEngraver
Services/BulkOrders/Items/FementationBarrel.cs  <- upstream: Plum | also needs: ConfirmCallbackGump, GrapeBunch, Yeast
Services/BulkOrders/Items/PlumTreeAddon.cs  <- upstream: Plum
Services/BulkOrders/Items/SpecialNaturalDye.cs  <- unknown: DullRuby, PoppieWhite, UmbranViolet, WindAzul, ZentoOrchid | also needs: BaseStatuette
Services/BulkOrders/LargeBODs/LargeAlchemyBOD.cs  <- upstream: AlchemyRewardCalculator, LargeExplosive, LargeGreater, LargeLesser, LargeRegular, LargeToxic
Services/BulkOrders/LargeBODs/LargeCarpentryBOD.cs  <- upstream: CarpentryRewardCalculator, LargeArmoire, LargeCabinets, LargeChests, LargeElvenWeapons, LargeInstruments, LargeWeapons, LargeWoodFurniture
Services/BulkOrders/LargeBODs/LargeCookingBOD.cs  <- upstream: CookingRewardCalculator, LargeBarbeque, LargeDough, LargeFruits, LargeMiso, LargeSushi, LargeSweets, LargeUnbakedPies
Services/BulkOrders/LargeBODs/LargeFletchingBOD.cs  <- upstream: FletchingRewardCalculator, LargeAmmunition, LargeElvenBows1, LargeElvenBows2, LargeHumanBows1, LargeHumanBows2
Services/BulkOrders/LargeBODs/LargeInscriptionBOD.cs  <- upstream: InscriptionRewardCalculator, LargeBooks, LargeCircle1, LargeCircle1and2, LargeCircle4, LargeCircle5, LargeCircle7, LargeCircle8, LargeNecromancy1, LargeNecromancy2, LargeNecromancy3
Services/BulkOrders/LargeBODs/LargeTinkerBOD.cs  <- upstream: LargeDining, LargeJewelry, LargeKeyGlobe, LargeTools, TinkeringRewardCalculator
Services/BulkOrders/Rewards/RewardsGump.cs  <- upstream: BODCollectionItem | also needs: BaseRewardGump, CollectionItem
Services/BulkOrders/SmallBODs/SmallAlchemyBOD.cs  <- upstream: AlchemyRewardCalculator, AlchemySmalls, GraphicHue
Services/BulkOrders/SmallBODs/SmallCarpentryBOD.cs  <- upstream: CarpentryRewardCalculator, CarpentrySmalls, GraphicHue
Services/BulkOrders/SmallBODs/SmallCookingBOD.cs  <- upstream: CookingRewardCalculator, CookingSmalls, CookingSmallsRegular, GraphicHue
Services/BulkOrders/SmallBODs/SmallFletchingBOD.cs  <- upstream: FletchingRewardCalculator, FletchingSmalls, FletchingSmallsRegular, GraphicHue
Services/BulkOrders/SmallBODs/SmallInscriptionBOD.cs  <- upstream: GraphicHue, InscriptionRewardCalculator, InscriptionSmalls
Services/BulkOrders/SmallBODs/SmallTinkerBOD.cs  <- upstream: GraphicHue, SmithyHammer, TinkeringRewardCalculator, TinkeringSmalls, TinkeringSmallsRegular
```


#### CC7 as written (+Resource, +BulkOrders) — extra ServUO files the co-port bucket pulls in (14 files)

```
Abilities/Enhancement.cs
Gumps/BaseRewardGump.cs
Gumps/ConfirmCallbackGump.cs
Items/Artifacts/Consumables/GrapeBunch.cs
Items/Artifacts/Equipment/Glasses/Glasses.cs
Items/Consumables/BaseRewardTitleDeed.cs
Items/Consumables/EnchantedApple.cs
Items/Consumables/EngravingTools.cs
Items/Decorative/BaseStatuette.cs
Items/Equipment/Weapons/GargishGnarledStaff.cs
Services/BasketWeaving/MiscSAResources.cs
Services/BasketWeaving/PlantPigmentHue.cs
Services/CommunityCollections/CollectionItem.cs
Services/New Magincia/Distillation/Items/Yeast.cs
```


#### CC7 as written (+Resource, +BulkOrders) — filtered out at step 1: ModernUO or our tree already declares the primary type (134 files)

```
Items/Resource/Amber.cs
Items/Resource/Amethyst.cs
Items/Resource/ArcaneGem.cs
Items/Resource/ArcanicRuneStone.cs
Items/Resource/Arrow.cs
Items/Resource/Axle.cs
Items/Resource/AxleGears.cs
Items/Resource/Bandage.cs
Items/Resource/BarrelParts.cs
Items/Resource/BaseFish.cs
Items/Resource/BatWing.cs
Items/Resource/Beeswax.cs
Items/Resource/BigFish.cs
Items/Resource/BlackPearl.cs
Items/Resource/BlankScroll.cs
Items/Resource/Bloodmoss.cs
Items/Resource/Board.cs
Items/Resource/BolaBall.cs
Items/Resource/Bolt.cs
Items/Resource/BoltOfCloth.cs
Items/Resource/Bone.cs
Items/Resource/Bottle.cs
Items/Resource/BottleIchor.cs
Items/Resource/ChagaMushroom.cs
Items/Resource/Citrine.cs
Items/Resource/ClockFrame.cs
Items/Resource/ClockParts.cs
Items/Resource/ClockworkAssembly.cs
Items/Resource/Cloth.cs
Items/Resource/Cotton.cs
Items/Resource/CrushedGlass.cs
Items/Resource/CrystalShards.cs
Items/Resource/CrystallineBlackrock.cs
Items/Resource/DaemonBlood.cs
Items/Resource/DaemonBone.cs
Items/Resource/DaemonClaw.cs
Items/Resource/DeadWood.cs
Items/Resource/DelicateScales.cs
Items/Resource/Diamond.cs
Items/Resource/ElvenFletchings.cs
Items/Resource/Emerald.cs
Items/Resource/EnchantedSwitch.cs
Items/Resource/EssenceAchievement.cs
Items/Resource/EssenceBalance.cs
Items/Resource/EssenceControl.cs
Items/Resource/EssenceDiligence.cs
Items/Resource/EssenceDirection.cs
Items/Resource/EssenceFeeling.cs
Items/Resource/EssenceOrder.cs
Items/Resource/EssencePassion.cs
Items/Resource/EssencePrecision.cs
Items/Resource/EssenceSingularity.cs
Items/Resource/FaeryDust.cs
Items/Resource/Feather.cs
Items/Resource/FertileDirt.cs
Items/Resource/Fish.cs
Items/Resource/Flax.cs
Items/Resource/Garlic.cs
Items/Resource/Gears.cs
Items/Resource/Ginseng.cs
Items/Resource/GoblinBlood.cs
Items/Resource/Granite.cs
Items/Resource/GraveDust.cs
Items/Resource/Hides.cs
Items/Resource/Hinge.cs
Items/Resource/HollowPrism.cs
Items/Resource/Ingots.cs
Items/Resource/JeweledFiligree.cs
Items/Resource/LavaSerpenCrust.cs
Items/Resource/Leathers.cs
Items/Resource/Log.cs
Items/Resource/MagicFish.cs
Items/Resource/MandrakeRoot.cs
Items/Resource/MiscMLResources.cs
Items/Resource/Nightshade.cs
Items/Resource/NoxCrystal.cs
Items/Resource/OilFlask.cs
Items/Resource/Ore.cs
Items/Resource/PigIron.cs
Items/Resource/PotionKeg.cs
Items/Resource/PowderedIron.cs
Items/Resource/PowerCrystal.cs
Items/Resource/RaptorTeeth.cs
Items/Resource/RecallRune.cs
Items/Resource/ReflectiveWolfEye.cs
Items/Resource/Ruby.cs
Items/Resource/RunedPrism.cs
Items/Resource/Sand.cs
Items/Resource/Sapphire.cs
Items/Resource/Scales.cs
Items/Resource/Seed.cs
Items/Resource/SeedRenewal.cs
Items/Resource/SextantParts.cs
Items/Resource/Shaft.cs
Items/Resource/SilverSnakeSkin.cs
Items/Resource/SlithTongue.cs
Items/Resource/SpiderCarapace.cs
Items/Resource/SpidersSilk.cs
Items/Resource/Springs.cs
Items/Resource/StarSapphire.cs
Items/Resource/SulfurousAsh.cs
Items/Resource/Tourmaline.cs
Items/Resource/TribalBerry.cs
Items/Resource/UncutCloth.cs
Items/Resource/UndyingFlesh.cs
Items/Resource/UnholyBone.cs
Items/Resource/VialOfVitriol.cs
Items/Resource/VoidOrb.cs
Items/Resource/Wool.cs
Items/Resource/YarnsAndThreads.cs
Items/Resource/ZoogiFungus.cs
Services/BulkOrders/Books/BOBFilter.cs
Services/BulkOrders/Books/BOBFilterGump.cs
Services/BulkOrders/Books/BOBGump.cs
Services/BulkOrders/Books/BOBLargeEntry.cs
Services/BulkOrders/Books/BOBLargeSubEntry.cs
Services/BulkOrders/Books/BOBSmallEntry.cs
Services/BulkOrders/Books/BODBuyGump.cs
Services/BulkOrders/Books/BODType.cs
Services/BulkOrders/Books/BulkOrderBook.cs
Services/BulkOrders/BulkMaterialType.cs
Services/BulkOrders/LargeBODs/LargeBOD.cs
Services/BulkOrders/LargeBODs/LargeBODAcceptGump.cs
Services/BulkOrders/LargeBODs/LargeBODGump.cs
Services/BulkOrders/LargeBODs/LargeBulkEntry.cs
Services/BulkOrders/LargeBODs/LargeSmithBOD.cs
Services/BulkOrders/LargeBODs/LargeTailorBOD.cs
Services/BulkOrders/Rewards/Rewards.cs
Services/BulkOrders/SmallBODs/SmallBOD.cs
Services/BulkOrders/SmallBODs/SmallBODAcceptGump.cs
Services/BulkOrders/SmallBODs/SmallBODGump.cs
Services/BulkOrders/SmallBODs/SmallBulkEntry.cs
Services/BulkOrders/SmallBODs/SmallSmithBOD.cs
Services/BulkOrders/SmallBODs/SmallTailorBOD.cs
```


### CC5 High Seas cheap half

Prefixes: `Services/Expansions/High Seas/Items`, `Services/Expansions/High Seas/Mobiles`  
raw 78 → filtered out 1 → candidates 77  
drops straight in 31 · needs another row file 17 · co-port 12 · upstream/carrier 17


#### CC5 High Seas cheap half — drops straight in (31 files)

```
Services/Expansions/High Seas/Items/Artifacts/CorgulsEnchantedSash.cs
Services/Expansions/High Seas/Items/Artifacts/CorgulsHandbookOnTheUndead.cs
Services/Expansions/High Seas/Items/Artifacts/EnchantedBlade.cs
Services/Expansions/High Seas/Items/Artifacts/EnchantedCoralBracelet.cs
Services/Expansions/High Seas/Items/Artifacts/EnchantedVortex.cs
Services/Expansions/High Seas/Items/Artifacts/HelmOfVengence.cs
Services/Expansions/High Seas/Items/Artifacts/LeviathanHideBracers.cs
Services/Expansions/High Seas/Items/Artifacts/RingOfTheSoulbinder.cs
Services/Expansions/High Seas/Items/Artifacts/RuneEngravedPegLeg.cs
Services/Expansions/High Seas/Items/Artifacts/WandOfThunderingGlory.cs
Services/Expansions/High Seas/Items/Cannons and Ammo/FuseCord.cs
Services/Expansions/High Seas/Items/Cannons and Ammo/Ramrod.cs
Services/Expansions/High Seas/Items/Cannons and Ammo/SpecialAmmo.cs
Services/Expansions/High Seas/Items/Cannons and Ammo/Swab.cs
Services/Expansions/High Seas/Items/IslandMap.cs
Services/Expansions/High Seas/Items/Resources/BlackPowder.cs
Services/Expansions/High Seas/Items/Resources/Charcoal.cs
Services/Expansions/High Seas/Items/Resources/MatchCord.cs
Services/Expansions/High Seas/Items/Resources/Potash.cs
Services/Expansions/High Seas/Items/Resources/SaltPeter.cs
Services/Expansions/High Seas/Items/SOS Artifacts/YellowPolkaDotBikini.cs
Services/Expansions/High Seas/Items/SeaMarketBuoy.cs
Services/Expansions/High Seas/Items/SmugglersLiquor.cs
Services/Expansions/High Seas/Mobiles/Corgul/BoundSoul.cs
Services/Expansions/High Seas/Mobiles/Corgul/SoulboundApprenticeMage.cs
Services/Expansions/High Seas/Mobiles/Corgul/SoulboundBattleMage.cs
Services/Expansions/High Seas/Mobiles/Corgul/SoulboundPirateCaptain.cs
Services/Expansions/High Seas/Mobiles/Corgul/SoulboundPirateRaider.cs
Services/Expansions/High Seas/Mobiles/Corgul/SoulboundSpellSlinger.cs
Services/Expansions/High Seas/Mobiles/Corgul/SoulboundSwashbuckler.cs
Services/Expansions/High Seas/Mobiles/Vendors/GargoyleShipwright.cs
```


#### CC5 High Seas cheap half — portable once other files in this row come with it (17 files)

```
Services/Expansions/High Seas/Items/Cannons and Ammo/AmmoInfo.cs  <- BaseShipCannon, Cannonball, FlameCannonball, FrostCannonball, Grapeshot, HeavyCannonball, HeavyFlameCannonball, HeavyFrostCannonball, HeavyGrapeshot, IShipCannon, LightCannonball, LightFlameCannonball, LightFrostCannonball, LightGrapeshot
Services/Expansions/High Seas/Items/Cannons and Ammo/Matches.cs  <- CanLight, IShipCannon, LightFuse
Services/Expansions/High Seas/Items/Fish/Bait.cs  <- BaitUses, BaseCrabAndLobster, EnhancedBait, FishInfo, FishInfos, GetFishHue, GetFishLabel, GetTypeFromIndex, LobsterTrap
Services/Expansions/High Seas/Items/Fish/CrabsAndLobsters.cs  <- BaseHighseasFish, FishInfo, GetCrabID, GetFishHue, GetLobsterID
Services/Expansions/High Seas/Items/Fish/LegendaryFish.cs  <- FishInfo, GetFishHue, RareFish
Services/Expansions/High Seas/Items/Fish/RareFish.cs  <- BaseHighseasFish, FishInfo, GetFishHue
Services/Expansions/High Seas/Items/LobsterTrap.cs  <- Crab, DateCaught, FishInfo, GetFishLabel, GetIndexFromType, GetSpecialItem, GetTypeFromIndex, LavaLobsterTrap, Lobster, RareCrabAndLobster
Services/Expansions/High Seas/Items/Resources/Cooking Ingrediants.cs  <- OracleOfTheSea
Services/Expansions/High Seas/Items/SmugglersCache.cs  <- GetRandom, SmugglersLiquor
Services/Expansions/High Seas/Mobiles/Vendors/BoatPainter.cs  <- SBBoatPainter
Services/Expansions/High Seas/Mobiles/Vendors/CrabFisher.cs  <- SBCrabFisher
Services/Expansions/High Seas/Mobiles/Vendors/DocksAlchemist.cs  <- SBDocksAlchemist
Services/Expansions/High Seas/Mobiles/Vendors/SBInfos/SBAlchemist.cs  <- Saltpeter
Services/Expansions/High Seas/Mobiles/Vendors/SBInfos/SBBoatPainter.cs  <- BoatPaint, BoatPaintRemover, LobsterTrap
Services/Expansions/High Seas/Mobiles/Vendors/SBInfos/SBCrabFisher.cs  <- AppleCrab, BloodLobster, BlueCrab, BlueLobster, BlueLobsterMeat, CrustyLobster, DreadLobster, DungeonessCrab, FredLobster, HummerLobster, KingCrab, LobsterTrap, RockCrab, RockLobster, ShovelNoseLobster, SnowCrab, SpiderCrab, SpiderCrabMeat, SpineyLobster, StoneCrab, StoneCrabMeat, TunnelCrab, VoidCrab, VoidLobster
Services/Expansions/High Seas/Mobiles/Vendors/SBInfos/SBSeaMarketTavernKeeper.cs  <- DarkTruffle, MentoSeasoning, SamuelsSecretSauce
Services/Expansions/High Seas/Mobiles/Vendors/SeaMarketTavernKeeper.cs  <- SBSeaMarketTavernKeeper
```


#### CC5 High Seas cheap half — needs ServUO files from outside this row (12 files)

```
Services/Expansions/High Seas/Items/Artifacts/CorgulsHandbookOnMysticism.cs  <- MysticBook
Services/Expansions/High Seas/Items/BoatPaint.cs  <- BaseGalleon, Captain, FindGalleonAt, GetSecurityLevel, SecurityLevel, TryPaintBoat, TryPermanentPaintBoat
Services/Expansions/High Seas/Items/BoatPaintRemover.cs  <- BaseGalleon, RemovePaint
Services/Expansions/High Seas/Items/Cannons and Ammo/CannonBall.cs  <- Replacer
Services/Expansions/High Seas/Items/Cannons and Ammo/GrapeShot.cs  <- Replacer
Services/Expansions/High Seas/Items/Cannons and Ammo/PowderCharge.cs  <- Replacer
Services/Expansions/High Seas/Items/CorgulAltar.cs  <- CorgulRegion, CorgulWarpRegion
Services/Expansions/High Seas/Items/Fish/FishInfo.cs  <- AntiqueWeddingDress, GrapeVine, HasSchool, KelpWovenLeggings, LargeFishingNet, MagicalFishFinder, RunedDriftwoodBow, ValkyrieArmor
Services/Expansions/High Seas/Items/OracleOfTheSea.cs  <- CharydbisSpawner, SpawnInstance, TrySpawnCharybdis
Services/Expansions/High Seas/Items/Sets/FishermansSet.cs  <- GargishClothKiltArmor, GargishEarrings, GargishLeatherArms, GargishPlateChest
Services/Expansions/High Seas/Items/ShippingCrate.cs  <- BaseGalleon, GalleonHold
Services/Expansions/High Seas/Mobiles/Vendors/DockMaster.cs  <- BaseGalleon, GalleonHold, GetBoat
```


#### CC5 High Seas cheap half — needs an upstream member, a carrier, or reading (17 files)

```
Services/Expansions/High Seas/Items/Artifacts/CullingBlade.cs  <- upstream: HitFatigue, HitManaDrain
Services/Expansions/High Seas/Items/Artifacts/SmilingMoonBlade.cs  <- upstream: HitManaDrain
Services/Expansions/High Seas/Items/Cannons and Ammo/Cannon.cs  <- upstream: GetMobilesOnBoard, OnTakenDamage | unknown: AftPort, AftStarboard, AmidShipPort, AmidShipStarboard, BowPort, BowStarboard, Crewman, Heavily, Moderately, Officer, Passenger, Pristine, Severely | also needs: BaseGalleon, BritannianShip, CannonDamageMod, FindGalleonAt, GalleonHold, GetSecurityLevel, RemoveCannon, SecurityLevel, TryAddCannon, ZSurface
Services/Expansions/High Seas/Items/Cannons and Ammo/CannonDeed.cs  <- unknown: Heavy | also needs: BaseGalleon, FindGalleonAt, TryAddCannon
Services/Expansions/High Seas/Items/Cannons and Ammo/ShipCannon.cs  <- upstream: OnTakenDamage | unknown: AnimationType, Crewman, Denied, GetGump, GetObjectsInRange, GraphicalEffect, Heavily, Heavy, IDamageable, Moderately, Officer, Pristine, Severely | also needs: BaseGalleon, BritannianShip, CanDamage, CannonDamageMod, CannonIDs, Captain, DamageableItem, GalleonHold, GetEntitiesOnBoard, GetSecurityLevel, RemoveCannon, SecurityLevel, ZSurface
Services/Expansions/High Seas/Items/Fish/Fish.cs  <- unknown: AttachSocket, HasSocket | also needs: Caddellite, CheckCarve, ShippingCrate
Services/Expansions/High Seas/Items/Fish/FishPies.cs  <- upstream: ManaRegen | unknown: CastFocus, DefChance, HitChance, WeaponDam | also needs: HitsRegen, StamRegen
Services/Expansions/High Seas/Items/Fish/Hooks.cs  <- upstream: HookUses | unknown: Dredging, JunkProof, Lava | also needs: OriginalHue
Services/Expansions/High Seas/Items/Fish/Trophies.cs  <- upstream: TrophyInfos
Services/Expansions/High Seas/Items/LavaFishItems.cs  <- unknown: MovementEventHandler | also needs: IsTrapped, SpiderWebbing
Services/Expansions/High Seas/Items/LavaLobsterTrap.cs  <- upstream: LavaTiles | also needs: Harvest
Services/Expansions/High Seas/Items/Resources/Niter.cs  <- unknown: Large, Small
Services/Expansions/High Seas/Items/RuinedShipPlans.cs  <- unknown: Eight, Five, Four, One, Seven, Six, Three, Two | also needs: OrcishGalleonDeed
Services/Expansions/High Seas/Mobiles/BaseSeaChampion.cs  <- upstream: OnTakenDamage | also needs: BritannianShip
Services/Expansions/High Seas/Mobiles/Charybdis.cs  <- upstream: GetMobilesOnBoard, IsSoulbound, IsSoulboundEnemies, OnTakenDamage | unknown: FiftyMS | also needs: CharydbisSpawner, CheckPrimerDrop, OnCharybdisKilled, SkillMasteryPrimer, SpawnInstance
Services/Expansions/High Seas/Mobiles/Corgul/CorgulTheSoulbinder.cs  <- upstream: IsSoulbound, IsSoulboundEnemies | unknown: AI_NecroMage, FiftyMS | also needs: CorgulRegion, EtherealSand
Services/Expansions/High Seas/Mobiles/OsiredonTheScalisEnforcer.cs  <- upstream: IsSoulbound, IsSoulboundEnemies | unknown: AI_NecroMage | also needs: CheckPrimerDrop, MiniSoulForgeDeed, SkillMasteryPrimer
```


#### CC5 High Seas cheap half — extra ServUO files the co-port bucket pulls in (41 files)

```
Items/Addons/MiniSoulForge.cs
Items/Artifacts/Decorative/GrapeVine.cs
Items/Artifacts/Decorative/LargeFishingNet.cs
Items/Artifacts/Equipment/Armor/KelpWovenLeggings.cs
Items/Artifacts/Equipment/Armor/ValkryieArmor.cs
Items/Artifacts/Equipment/Clothing/AntiqueWeddingDress.cs
Items/Artifacts/Equipment/Weapons/RunedDriftwoodBow.cs
Items/Damageable/DamageableItem.cs
Items/Decorative/EnchantedWheelbarrow.cs
Items/Equipment/Armor/GargishClothArmor.cs
Items/Equipment/Armor/GargishLeatherArms.cs
Items/Equipment/Armor/GargishPlateChest.cs
Items/Equipment/Jewelry/GargishEarrings.cs
Items/Equipment/Spellbooks/MysticBook.cs
Items/Functional/SpiderWebbing.cs
Items/Internal/ItemSockets/Caddellite.cs
Items/Resource/EtherealSand.cs
Misc/Replacer.cs
Quests/The Ritual/Puzzle.cs
Regions/DamagingRegion.cs
Services/City Loyalty System/CityLoyaltySystem.cs
Services/Expansions/High Seas/Multis/BaseGalleon.cs
Services/Expansions/High Seas/Multis/BritannianShip.cs
Services/Expansions/High Seas/Multis/GalleonHold.cs
Services/Expansions/High Seas/Multis/GargishGalleon.cs
Services/Expansions/High Seas/Multis/OrcishGalleon.cs
Services/Expansions/High Seas/Multis/Rowboat.cs
Services/Expansions/High Seas/Multis/TokunoGalleon.cs
Services/Expansions/High Seas/Persistence.cs
Services/Expansions/High Seas/Quests/ProfessionFishQuest/FishQuestHelper.cs
Services/Expansions/High Seas/Quests/ProfessionFishQuest/ShippingCrate.cs
Services/Expansions/High Seas/Quests/ProfessionalBountyQuest/ProfessionalBountyQuest.cs
Services/Expansions/High Seas/Regions/CorgulRegion.cs
Services/Expansions/High Seas/Regions/WarpRegion.cs
Services/Expansions/High Seas/Spawners/CharybdisSpawner.cs
Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/InvasionBeacon.cs
Services/Revamped Dungeons/Covetous Void Spawn/Items/MagicFishFinder.cs
Services/Seasonal Events/ForsakenFoes/Items/PumpkinRowboat.cs
Services/Seasonal Events/RisingTide/PlunderBeacon.cs
Spells/Skill Masteries/Core/SkillMasteryPrimer.cs
Spells/Skill Masteries/Rampage.cs
```


#### CC5 High Seas cheap half — filtered out at step 1: ModernUO or our tree already declares the primary type (1 files)

```
Services/Expansions/High Seas/Items/WhiteClothDyeTub.cs
```

