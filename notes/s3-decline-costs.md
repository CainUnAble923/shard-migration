# S3 — Cost every remaining decline

**Measurement only. Nothing was ported. No file in `server/customizations` was touched.**
Run 2026-09-07 against `D:\UO\ServUO-pub57\Scripts` (6,144 `.cs`) and
`D:\UO\ModernUO-pinned\Projects` (3,991 `.cs`, detached at `7c9215d97`), both read-only.

The deliverable is a costed menu. **The decision is Chase's.** §10 ranks and recommends;
it does not decide.

---

## 1. The headline, before any table

Two counting errors were inflating every subsystem estimate on this project. Both are
mechanical, both are now measured, and correcting them changes several answers.

**Error 1 — "touches X" was being read as "blocked by X".** Already known; §2 states both
numbers separately for every row, always.

**Error 2, new and larger — "a ServUO file referencing X" was being read as "a file we would
gain".** It is not. **ModernUO already ships 3,134 of ServUO's 6,144 script files' primary
types.** A ServUO creature ModernUO already has is not unblocked by anything; porting it is a
duplicate-type build failure under the collision rule in `AGENTS.md`. It belongs in neither
column.

The single clearest case: **the "103 `Mobiles/Normal` files blocked by Pet Training" is real
as a count of references and wrong as a count of value.** 66 of those 103 are creatures
ModernUO already ships — `Dragon`, `Nightmare`, `Hiryu`, `GiantSpider`, `AncientWyrm`,
`Beetle`, `Phoenix` and 59 more. One more, `BaseCreature.cs`, is the base class itself and is
not portable content at all. **The number of `Mobiles/Normal` creatures Pet Training would
actually make available is 37.**

The same filter deflates every row below. It is applied everywhere and the file lists are in
the appendix so it can be checked.

### And the denominator was wrong too

CC6 computes its percentages against ServUO's 462 `Mobiles/Normal` files. **325 of those 462
are already in ModernUO.** The real creature backlog in that directory is **137 files**, not
462 and not "about 360". Every percentage in the CC6 section of `docs/tasks.md` is against the
wrong base. Counts and lists in the appendix.

---

## 2. Method, and what each column means

Six mechanical steps, all reproducible; the scripts are throwaway but the definitions are not.

1. **Type index of ModernUO.** Every `class`/`struct`/`interface`/`enum` declaration in the
   3,991 pinned files: **7,097 types**. Plus a full identifier index, so "absent" can be
   proven as *zero occurrences anywhere in the tree*, not merely "no declaration found".
2. **Type index of ServUO**: 11,363 types across 6,144 files.
3. **Cost to build** = the subsystem's own files and their line count, `find`-counted.
4. **Touches** = any file in the ServUO tree referencing a type the subsystem declares.
   Restricted to **public, namespace-level** type names, with an explicit blacklist for
   ServUO's ubiquitous private helper names (`InternalTarget`, `InternalTimer`,
   `InternalBuyInfo`, `Misc`, `City`, `Filter`, `Form`, …). Before that restriction City
   Loyalty measured 372 touches; 202 of them were the string `InternalTarget`. That number
   would have been wrong in exactly the way this project keeps being wrong.
5. **Already in ModernUO** = the referencing file's primary declared type exists in the
   ModernUO index. Cost, or nothing, never benefit.
6. **Unblocked** = touches minus already-in-ModernUO. **This is the only benefit column.**

**Every count has its file list in the appendix (§12).** Where a count here disagrees with a
count in `docs/`, the list is the evidence and the doc is wrong.

### Absence, verified in the pinned tree

Every "ModernUO does not have this" below is zero identifier occurrences across all 3,991
files, not an absence in our docs. Spot-verified with file and line where a positive citation
exists:

| Claimed missing | Occurrences in pinned ModernUO | Where the ModernUO equivalent lives, if any |
|---|---|---|
| `SetSpecialAbility`, `SetMagicalAbility`, `SetAreaEffect`, `PetTrainingHelper` | 0, 0, 0, 0 | none |
| `SpecialAbility`, `MagicalAbility`, `AreaEffect`, `AbilityProfile` | 0, 0, 0, 0 | none |
| `SAAbsorptionAttributes`, `SAAbsorptionAttribute`, `AbsorptionAttribute` | 0, 0, 0 | `BaseAttributes` **does** exist, so the class is additive |
| `BasePeerless`, `PeerlessAltar` | 0, 0 | none — see §8.8 |
| `VendorSearch`, `PlayerVendorSearch` | 0, 0 | none |
| `PointsSystem` | 0 | none |
| `ShadowguardController`, `TimeOfLegends` | 0, 0 | none |
| `GrayGoblin`, `GreenGoblin` | 0, 0 | none |
| `TribeType` | 0 | **`OppositionGroup`** — `UOContent/Mobiles/AI/OppositionGroup.cs:6`, used at `UOContent/Mobiles/BaseCreature.cs:512` and `:1316`. See §7.1. |
| ServUO's ML quest framework (`BaseQuest`, `MondainQuester`, …) | 0 | **`Engines/ML Quests`, 109 files, 18,110 lines, 240 quest classes.** See §5. |

---

## 3. The table

Ratio is **unblocked files : own files**. For rows marked *(cluster)* the ratio is the wrong
lens and §8 says why: the subsystem's own files *are* the content, so it delivers whether or
not anything else references it.

| # | Subsystem | Cost (files / lines) | Touches | Already in MUO | **Unblocked** | Ratio | Upstream files patched | Fits layering? |
|---|---|---|---|---|---|---|---|---|
| 1 | **`SAAbsorptionAttributes`** (minimal) | **1 / ~350** | 64 | 7 | **57** | **~57:1** | 1 damage hook (see §6) | **Yes** — S1 pattern exactly |
| 2 | Pet Training — `SpecialAbility` group | 4 / ~4,100 | 113 | 60 | **53** | ~13:1 | 6 + `AOS.Damage` | Yes, but see §4.3 |
| 3 | Pet Training — `MagicalAbility` group | slice of the above | 27 | 9 | **18** | — | same | Yes |
| 4 | Pet Training — `AreaEffect` group | +1 / 596 | 30 | 13 | **17** | — | same | Yes |
| 5 | Pet Training — gate, profiles, gumps | 6 / ~4,050 | 43 | 32 | **11** | **~2:1** | +`AnimalLore`, `AnimalTaming`, `Discordance`, `SkillCheck`, `BaseInstrument`, 6 weapon abilities | Yes, but poor value |
| 6 | *Pet Training, all four together* | *11 / 8,664* | *175* | *96* | ***79*** | *~7:1* | *17* | — |
| 7 | Myrmidex Invasion *(cluster)* | 6 / 2,197 | 11 | 2 | **9** | ~1.5:1 | 2 | Yes |
| 8 | Vendor Searching *(cluster)* | 4 / 2,545 | 10 | 5 | **5** | ~1.2:1 | 5 | Marginal — §8.7 |
| 9 | City Loyalty *(cluster)* | 28 / 8,177 | 26 | 11 | **15** | ~0.5:1 | 11 | Yes, wide |
| 10 | Skill Masteries *(cluster)* | 45 / 8,542 | 49 | 35 | **14** | ~0.3:1 | **35** | **No** — §8.3 |
| 11 | Shadowguard *(cluster)* | 14 / 11,222 | 12 | 4 | **8** | ~0.6:1 | 4 | Yes |
| 12 | Instanced Peerless *(cluster)* | 13 / 1,543 | 4 | 2 | **2** | ~0.15:1 | 2 | **No base to instance** — §8.8 |
| 13 | Vice vs Virtue *(cluster)* | 57 / 9,613 | 26 | 21 | **5** | ~0.1:1 | **21** | Marginal |
| 14 | Exploring the Deep *(cluster)* | 70 / 10,292 | 3 | 1 | **2** | ~0.03:1 | 1 | Yes |
| 15 | ServUO ML quest framework | 22 / 6,269 | 290 | 114 | **176** | ~8:1 | — | **Wrong question — §5** |
| — | *for comparison: armour sets, S1, built* | *1 / 387 + 3 patches* | *131* | *7* | *124 (111 without absorption)* | *~124:1* | *3* | *yes* |

Two corrections to figures in the brief and in `docs/`, both reported rather than adjusted to
fit:

- **The ML quest framework is 22 files and 6,269 lines, not 21 and 5,625.** The brief's figure
  counts `Services/MondainsLegacyQuests` and omits `Quests/BaseQuest.cs` (644 lines), the class
  every one of the 408 quests derives from. 5,625 + 644 = 6,269, which is the figure CC3
  already used. The brief undercounts its own subject by one file.
- **S1's `114` and the `124` in the comparison row are not the same measurement, and neither
  is quite right.** 131 files reference `SetID`. **7 are upstream base classes ModernUO
  already has**, so 124 are content ModernUO lacks. Of those 124, **13 also need
  `SAAbsorptionAttributes`**, leaving **111 that the armour-set system unblocks on its own**.
  S1's 114 is `131 − 17`: it subtracts the absorption overlap but not the upstream base
  classes, and since 4 of the 17 *are* base classes, three upstream files survive into the
  114. The like-for-like figures are **124** (unblocked by the set system, counting those that
  also want absorption) and **111** (unblocked by the set system alone). 114 is neither.
  The decision it justified holds comfortably at any of the three; the split is recorded so
  nobody reconciles them by guessing.

---

## 4. Pet Training, split by what each piece actually needs

### 4.1 What the four calls are

All four `Set*Ability` methods are two-line forwarders on `BaseCreature`
(`Mobiles/Normal/BaseCreature.cs:635-651`) into
`PetTrainingHelper.GetAbilityProfile(this, true).AddAbility(...)`. The ability *definitions*
and the ability *storage* are separable from everything a player touches. Confirmed by
reading, not inferred.

| Piece | ServUO file | Lines |
|---|---|---|
| `SpecialAbility` definitions | `Services/Pet Training/SpecialAbility.cs` | 2,688 |
| `AreaEffect` definitions | `Services/Pet Training/AreaEffects.cs` | 596 |
| `AbilityProfile` — the storage | `Services/Pet Training/AbilityProfile.cs` | 759 |
| `MagicalAbility` enum + `GetAbilityProfile` + ability tables | slice of `PetTrainingHelper.cs` | ~470 of 1,778 |
| `TrainingPoint` (return type of one call in `AbilityProfile`) | `TrainingPoint.cs` | 55 |
| **subtotal — the smallest thing a creature needs** | **5 files** | **≈4,570** |
| gumps players interact with | `Gumps.cs` | 1,918 |
| training gate, profiles, planning, title deed | 5 files | 870 |
| remainder of `PetTrainingHelper.cs` (training defs, localisations) | — | ~1,308 |
| **full system** | **11 files** | **8,664** |

The ~470 is region arithmetic on `PetTrainingHelper.cs`, not a written file: enums and class
header (1–125), `GetAbilityProfile` (196–205), the ability-array declarations (250–298), and
the Special Ability and Area Effect package tables (421–631, 633–678). The Creature Training
Defs region (680–825) and the Localizations region (1445–1706) are gate and gump data and are
not needed. Treat ≈4,570 as a floor with a real margin, not a quote.

### 4.2 What each piece unblocks

| Piece | Touches | Already in MUO | **Unblocked** |
|---|---|---|---|
| `SpecialAbility` | 113 | 60 | **53** |
| `AreaEffect` | 30 | 13 | **17** |
| `MagicalAbility` | 27 | 9 | **18** |
| gate / profiles / gumps machinery | 43 | 32 | **11** |
| **union of all four** | **175** | **96** | **79** |

**`SpecialAbility.cs` alone is not a buildable unit.** It calls
`PetTrainingHelper.GetAbilityProfile` at six sites and stores through `AbilityProfile`. The
smallest thing that compiles is the 5-file, ≈4,570-line subset in §4.1. The
`docs/subsystem-policy.md` row that prices `SpecialAbility.cs` at "2,688 lines" understates it
by about 70%.

### 4.3 The finding that should change the decision

**Pet Training blocks almost nothing from being ported. It only decides whether ported
creatures keep their abilities.**

Of the 103 `Mobiles/Normal` files that reference it:

- **1** is `BaseCreature.cs`, the base class, not content;
- **66** are creatures ModernUO already ships;
- **78** — including many of those 66 — carry their entire dependency in single-line
  `SetXAbility(SpecialAbility.Y);` statements. Delete the line and the file compiles. This is
  the `Saurosaurus` precedent, already accepted;
- **10 more** have their only remaining references inside ServUO's hand-written
  `Deserialize` version-upgrade blocks, which a ModernUO port discards outright. Effectively
  also one-line deletions: `ClockworkScorpion`, `CoralSnake`, `CorrosiveSlime`, `DreadSpider`,
  `GiantSpider`, `RuneBeetle`, `Scorpion`, `Slime`, `Snake`, `WolfSpider`;
- **14** are genuinely entangled outside `Deserialize` — `Beetle`, `CrimsonDrake`, `CuSidhe`,
  `FireBeetle`, `Hiryu`, `IronBeetle`, `LesserHiryu`, `Phoenix`, `PlatinumDrake`, `Ridgeback`,
  `SabertoothedTiger`, `SavageRidgeback`, `ScaledSwampDragon`, `SwampDragon`. **Eleven of
  those 14 are creatures ModernUO already has.**

So the count of `Mobiles/Normal` creatures that are in our backlog **and** cannot be ported at
all without Pet Training is **three**: `CrimsonDrake`, `PlatinumDrake`, `IronBeetle`.
Everything else is portable today at the cost of a logged deviation.

That does not make Pet Training worthless. It makes its value **fidelity, not throughput**:
79 files across the tree, 37 of them creatures in the `Mobiles/Normal` backlog, get the
abilities OSI gives them instead of a deviation line each. That is a real thing to want. It is
just not a 103-file wall, and it never was.

### 4.4 Layering and bump risk

Additive `.cs` for the definitions. The hooks are patches into files ModernUO has:

- **`Projects/UOContent/Misc/AOS.cs`, in `AOS.Damage`** — ServUO calls
  `SpecialAbility.CheckCombatTrigger(from, m, ref totalDamage, type)` at `Misc/AOS.cs:328`.
  This is the one that matters: without it no special ability ever fires.
- **`Projects/UOContent/Mobiles/BaseCreature.cs`** — the four `Set*Ability` forwarders and the
  `AbilityProfile` regen hooks at ServUO `BaseCreature.cs:392-411`.
- **Six weapon-ability files** (`Bladeweave`, `Block`, `Feint`, `FrenziedWhirlwind`,
  `NerveStrike`, `TalonStrike`) call `PetTrainingHelper.OnWeaponAbilityUsed`. Only needed for
  the trained-pet path; skip them and the definitions still work.
- **`AnimalLore`, `AnimalTaming`, `Discordance`, `SkillCheck`, `BaseInstrument`,
  `ConfirmMountStatuetteGump`, `MageAI`, `AnimalTrainer`** — all gate/profile, not
  definitions. Full list in the appendix.

`Server.DamageType` (Melee/Ranged/Spell/SpellAOE, ServUO `Misc/AOS.cs:26`) has no ModernUO
counterpart — 4 values, additive. `IElementalCreature`, `IAuraCreature` and `ElementType`
come from `Mobiles/MobileInterfaces.cs`, 37 lines total, additive.

**Bump risk: high, and the highest of anything here.** `docs/upstream-watch.md` records that
`BaseCreature` moved to the SerializationGenerator on `main` (#2611, `392c4e1`) and that
`SpeedClass` is an open behaviour change (#2592). Every hook above except the `AOS.Damage` one
lands on `BaseCreature` or on creature-adjacent skills. A bump that crosses #2611 is a
reconciliation on the exact class this subsystem patches. **This is the one to build after a
bump, never before one.**

---

## 5. The Mondain's Legacy quest framework — the unknown, resolved

The brief says "the unknown that decides it is how many quest lines across the whole backlog
sit on it". That number is **203**. But the number that actually decides it is a different
one, and it is not the one anybody was looking for.

**ModernUO already ships this system.** `Projects/UOContent/Engines/ML Quests` is **109 files,
18,110 lines**, with **240 quest classes** and 21 definition files: `Heartwood.cs`,
`Bedlam.cs`, `BlightedGrove.cs`, `Sanctuary.cs`, `Spellweaving.cs`, `Heritage.cs`,
`NewHavenSkillTraining.cs`, `TownEscorts.cs`, `TheAncientWorld.cs` and more.

It is the same OSI system, differently implemented:

| | ServUO `Services/MondainsLegacyQuests` | ModernUO `Engines/ML Quests` |
|---|---|---|
| namespace | `Server.Engines.Quests` | `Server.Engines.MLQuests` |
| quest base | `BaseQuest` (`Quests/BaseQuest.cs:7`) | `MLQuest` (`ML Quests/MLQuest.cs:19`) |
| objectives | `SlayObjective`, `ObtainObjective`, `DeliverObjective`, `EscortObjective`, `ApprenticeObjective`, `QuestionAndAnswerObjective` | `KillObjective`, `CollectObjective`, `DeliverObjective`, `EscortObjective`, `GainSkillObjective` |
| rewards | `BaseReward` | `BaseReward`, `ItemReward`, `DummyReward` |
| quest classes | **408** | **240** |

**205 of ServUO's 408 quests already exist in ModernUO by class name.** Verified individually,
not by stem-matching a filename: `Acob` at `Definitions/Heartwood.cs:3796`, `Aelorn` at
`Definitions/NewHavenSkillTraining.cs:25`, `Aeluva` at `Definitions/Spellweaving.cs:486`,
`Ahie` at `Definitions/Heartwood.cs:3162` and `Definitions/Sanctuary.cs:731`.

Porting ServUO's framework would put **two quest engines in the tree for one job**, which
`docs/subsystem-policy.md` names as a standing reason to decline, independently of ratio.

**So the decline holds, and for a much stronger reason than "6,269 lines".** But the
conclusion underneath it is the opposite of a decline:

> **The remaining 203 ML quests are not blocked by a missing subsystem at all. They are a
> translation job into an engine we already have.** ServUO's six objective kinds map onto
> ModernUO's five; only `QuestionAndAnswerObjective` has no counterpart, and it is used by
> **2 files**.

That converts the largest single "deferred" item in `docs/tasks.md` from a 6,269-line
subsystem build into ordinary per-quest content work with a known shape. It also means the
Valley of One quest line (7 quests) and the Myrmidex Threat line (10) — declined in CC3 as
"a subsystem port, not a content port" — are **content ports after all**, against ModernUO's
engine. That decline should be revisited.

Where the 203 sit, by area: `Mobiles/NPCs` 63, `Quests/` root 59, `TieredQuests` 20,
`Town Cryer` 18, **Eodon Myrmidex Threat 10, Eodon Valley of One 7**, `The Ritual` 5,
`CloakOfHumility` 5, Khaldun 4, `DiscoveringAnimalTraining` 4, Bard Mastery 3, others 5.
Full class list in the appendix.

**I have not verified that ModernUO's engine is behaviourally complete**, only that it exists,
is the same system, and carries 240 quests. Before any quest work starts, one quest should be
translated end to end as a spike, exactly as S1 spiked before committing. That is the next
task this finding implies, and it is not this one.

---

## 6. `SAAbsorptionAttributes` — the best ratio on the menu

**Cost: one additive file, ≈350 ServUO lines.** The enum `SAAbsorptionAttribute` is
`Misc/AOS.cs:2728-2751` (24 lines); the class `SAAbsorptionAttributes : BaseAttributes` is
`Misc/AOS.cs:2753-3058` (306 lines). `BaseAttributes` **exists in ModernUO**, so the class is
purely additive.

**Unblocked: 57 files.** 64 reference absorption; 7 are upstream base classes. Of the 57:
the 8 Aloron pieces already in `server/customizations` (this closes **D-1**), 5 Darden's set
pieces that also need S1's set system, and 44 more artifacts and equipment.

**The brief's dependency claim is confirmed, and it is smaller than it looks.**
`SAAbsorptionAttributes.GetValue` at `Misc/AOS.cs:2780` sums exactly three terms:

| Term | Line | What it actually costs |
|---|---|---|
| `Enhancement.GetValue(m, attribute)` | `Misc/AOS.cs:2790` | `Abilities/Enhancement.cs` is a `Dictionary<Mobile, List<EnhancementAttributes>>` of temporary bonuses. **With nothing registered it returns 0.** 318 lines if wanted; droppable. |
| `RunicReforging.GetSAAbsorptionAttributes(m.Items[i])` | `Misc/AOS.cs:2795` | **Not the reforging system.** `Services/LootGeneration/RunicReforging/RunicReforging.cs:2765-2780` is a **16-line type switch** returning the item's own `AbsorptionAttributes`. Inline it. |
| `SkillMasterySpell.GetAttributeBonus(m, attribute)` | `Misc/AOS.cs:2801` | `Spells/Skill Masteries/Core/SkillMasterySpell.cs:1174`. **Returns 0 with no mastery spell active.** Droppable on a shard without Skill Masteries. |

So the honest reading: **one of the three is 16 lines and the other two contribute zero on a
shard that has neither system.** Recorded as a deviation, not a behaviour change. If Skill
Masteries is ever built, the term is added back and the value it contributes appears.

**Layering — S1's pattern, verbatim.** The property must reach `BaseArmor`, `BaseWeapon`,
`BaseJewel`, `BaseClothing` and `BaseTalisman`. It should **not** be added as a
`[SerializableField]` on those upstream classes: that changes their serialized layout and
makes an upstream migration ours to maintain, which S1 explicitly and rightly avoided. Do it
the S1 way — an additive `IAbsorptionItem` interface, implemented by ported artifacts, with
the aggregation walking `m.Items` and testing `is IAbsorptionItem`. That is
`AOS-set-attribute-aggregation.patch` with a different type name, and its cost is one patch
into the damage path, not five into base classes. The consequence, stated plainly: **the eater
works on our ported items and not on stock ModernUO loot** — which is not a loss, because
ModernUO's loot generator has no absorption property to roll.

**One real gap.** The eater only reduces damage if something calls it. ServUO applies it in
`AOS.Damage` via `DamageEaterContext.CheckDamage(...)` at `Misc/AOS.cs:289` and `:291`, and
`DamageEaterContext` lives in `Abilities/SAPropEffects.cs` (768 lines, a `PropertyEffect`
framework). **Either that framework comes too, or the damage-eater reduction has to be
written into the patch, which is copied upstream logic and is against the standing rule in
`docs/subsystem-policy.md`.** Cost it as **≈350 + up to 768 lines and one patch into
ModernUO's damage path.** The 350-line figure alone buys the tooltips and the property, not
the effect. Say so before anyone quotes 57:1.

**Bump risk: low-to-moderate, and lower than Pet Training.** One patch into the damage path;
no upstream serialization version bumped; no upstream class gains a field. The failure mode is
a loud patch failure under `apply-patches.sh`, not silent drift — except for one thing worth
naming: **if the damage hook still applies but ModernUO has rerouted damage around it, the
build stays green and the eater silently stops working.** That is exactly the S4 test case.
Ship it with a regression test asserting that damage taken with an eater item equipped is
reduced.

---

## 7. Two things nobody asked for, both free

### 7.1 `TribeType` is a transformation, not a blocker — a second `SetWeaponAbility`

`TribeType` (ServUO `Mobiles/Normal/BaseCreature.cs:137`) has **zero occurrences in
ModernUO** and 53 `Mobiles/Normal` files reference it. It reads as a blocker. It is not.

ModernUO has **`OppositionGroup`** — `UOContent/Mobiles/AI/OppositionGroup.cs:6`, exposed as
`public virtual OppositionGroup OppositionGroup => null` at
`UOContent/Mobiles/BaseCreature.cs:512` and consumed in `IsEnemy` at `:1316`. It ships
`TerathansAndOphidians`, `SavagesAndOrcs` and `FeyAndUndead` — **three of ServUO's four tribe
pairs**, with the same semantics: ServUO's `IsTribeEnemy` switch at
`BaseCreature.cs:1193-1202` is pairwise opposition, which is what `OppositionGroup.IsEnemy`
computes.

`Tribe = TribeType.Terathan` ports to
`public override OppositionGroup OppositionGroup => OppositionGroup.TerathansAndOphidians;`

Only the **GrayGoblin/GreenGoblin** pair has no ModernUO group. That needs one additive static
of about 25 lines and **no patch**, since our creatures can reference a static on our own type.

Of the 53, 44 are creatures ModernUO already ships; 9 are real candidates, 6 of them goblins.
So the throughput gain is small — but it removes 52 entries from every "references a type
ModernUO lacks" count in this repo, including the 89. Recorded so it never inflates one again.

### 7.2 `Services/PointsSystems` is a better bet than two things on the list

Not on the decline list and it should be. **12 files, 2,857 lines**, zero occurrences of
`PointsSystem` in ModernUO. It touches 67 files, 12 of which ModernUO has, so it **unblocks
55** — Seasonal Events (26), Revamped Dungeons (8), Town Cryer, CleanUpBritannia, UltimaStore,
FireCasino and others.

**≈4.6:1, better than every cluster in the table**, and it is a hard dependency of both Vice
vs Virtue (3 types) and City Loyalty (3 types), so building either without it is not possible.
It is not the point-scoring UI; it is the persistence substrate several systems store through.
Worth its own row on a future menu. Not costed further here: out of S3's scope, and stating a
layering verdict without measuring it would repeat the mistake this task exists to fix.

---

## 8. The eight clusters, one paragraph each

For these, the unblock ratio is close to meaningless: **the subsystem's own files are the
content.** Exploring the Deep unblocks 2 files because nothing else in ServUO refers to it —
not because it delivers nothing, but because it delivers 70 files of its own. The ratio
measures leverage, and leverage near zero means "build it only if you want that specific
content". Cost, patch surface and blockers are the useful columns.

**8.1 Myrmidex Invasion — 6 files, 2,197 lines, unblocks 9.** Patches `BaseCreature` and
`Faction`. Its 9 are the Eodon Myrmidex Threat quest files and the Time of Legends tribal
creatures. **Name collisions: `BattleRegion` and `Allegiance` both exist in ModernUO**
(`Allegiance` at `UOContent/Mobiles/BaseCreature.cs:138` and
`UOContent/Engines/Factions/Core/Faction.cs:1124`) — rename on port or the build fails.
Cheapest cluster here, and it pairs with §5: with ModernUO's quest engine the Myrmidex Threat
line stops being a subsystem question. Confirms CC3's decline of `MoonstonePowerGenerator.cs`
was right for the right reason — it is genuinely part of this cluster.

**8.2 Shadowguard — 14 files, 11,222 lines, unblocks 8.** `Encounters.cs` 1,588,
`Artifacts.cs` 1,064, `Items.cs` 1,034, `Bosses.cs` 1,033, `Controller.cs` 899. Patches
`PlayerMobile`, `SlayerGroup`, `MonsterStatuette`, `RewardSystem`. No collisions. A smallest
useful subset is real here: Controller + Instance + Encounter + one encounter is roughly
2,600 lines and gives one playable room; the other four rooms and the artifact set are
additive after. **The most expensive thing on the menu per unit of anything.**

**8.3 Skill Masteries — 45 files, 8,542 lines, unblocks 14, and patches 35 upstream files.**
Weapon abilities, `BaseWeapon`, `Spellbook`, `AOS`, `RegenRates`, `SkillCheck`, `MageAI`,
`BaseCreature`, `PlayerMobile`, `Party`, `SpecialMove`, `SpellHelper`, nine Necromancy spells,
`AnimalForm`, `Dispel`, `MassDispel`, `ArcaneCircle`, `Confidence`, three bard skills. **35
patch points is more than eleven times S1's entire patch count, for one system**, and
`docs/upstream-watch.md` records upstream actively refactoring `BaseCreature`. This does not
fit the layering pattern. **Decline, and this is the strongest decline in the set.** It is
also the reason `SAAbsorptionAttributes` should drop its `SkillMasterySpell` term rather than
wait for it.

**8.4 Vice vs Virtue — 57 files, 9,613 lines, unblocks 5, patches 21.** Touches
`BaseArmor`, `BaseWeapon`, `BaseJewel`, `BaseClothing`, `BaseTalisman`, `BaseQuiver`,
`Spellbook`, `PlayerMobile`, `BaseCreature`, `Notoriety`, `TownRegion`, `Faction`, `Sigil`,
`Hiding`, `Stealing`, `RemoveTrap`, `AccountHandler`, two guild gumps. Needs
`Services/PointsSystems` (§7.2). `CityInfo` collides with `Server/CityInfo.cs:5`. Second-worst
cost-to-unblock ratio and a wide patch surface. **Decline.**

**8.5 City Loyalty — 28 files, 8,177 lines, unblocks 15, patches 11.** `Recall`,
`GateTravel`, `SacredJourney`, `PublicMoongate`, `Teleporter`, `SHTeleporter`, `BaseVendor`,
`PlayerMobile`, `ChampionSpawn`, `Bandage`, `AOS`. Also needs `PointsSystems`. Its 15 are
mostly Town Cryer and New Magincia. Coherent, self-contained, moderate patch surface.
**Decline on ratio, not on structure** — revisit if Town Cryer or New Magincia is ever wanted.

**8.6 Exploring the Deep — 70 files, 10,292 lines, unblocks 2, patches 1 (`PlayerMobile`).**
Structurally the cleanest thing on the menu and the worst value by ratio. It is a complete
self-contained quest line: 131 public types, one patch, no entanglement. **Collision:
`ExploringDeepCreaturesRegion` already exists at
`UOContent/Regions/ExploringDeepCreaturesRegion.cs:6`** and is registered in
`RegionJsonRegistration.cs:44` — ModernUO ships the region and none of the content. **Decline
on ratio; note that it would be an unusually safe build if the content is ever wanted.**

**8.7 Vendor Searching — 4 files, 2,545 lines, unblocks 5, patches 5.** `PlayerVendor`,
`BaseVendor`, `PlayerVendorGumps`, `PlayerMobile`, `Recall`. Zero occurrences of
`VendorSearch` in ModernUO. This is a **player convenience feature, not content**, so the
unblock ratio is the wrong test for it entirely and I will not pretend otherwise: it either is
or is not something Chase wants players to have. Cheap, contained, five patches. **The one row
here where the ratio should be ignored.**

**8.8 Instanced Peerless — 13 files, 1,543 lines, unblocks 2.** **Blocked at the root:
`BasePeerless` and `PeerlessAltar` have zero occurrences in ModernUO.** ServUO's
`Services/Peerless` is a further 6 files / 1,590 lines. Instanced Peerless is an optional
*variant* of a system ModernUO does not have, so the real cost is 19 files / 3,133 lines
before a single peerless boss exists — and the bosses are absent too (`Travesty`, `Medusa`,
`Navrey` all zero declarations). **Decline. Cost the base Peerless system first if peerless
content is ever wanted; instancing is a later question.**

---

## 9. Overlaps, handled explicitly

The instruction was to say what building two together frees beyond the sum, and not to
double-count. **The answer is: almost nothing, and that is itself the finding.** These sets
are near-disjoint, so they do not compound and there is no combined-build discount to hope
for.

Every non-empty pairwise intersection of the unblocked sets:

| Pair | Files in both |
|---|---|
| Armour sets (built) ∩ `SAAbsorptionAttributes` | **13** |
| ML quest framework ∩ Pet Training | 3 |
| ML quest framework ∩ Skill Masteries | 3 |
| ML quest framework ∩ Myrmidex Invasion | 2 |
| City Loyalty ∩ ML quest framework | 2 |
| Myrmidex Invasion ∩ Skill Masteries | 2 |
| six further pairs | 1 each |

The only overlap that matters is the first, and the brief's figure needs a correction:

**The armour-set ∩ absorption overlap is 17 referencing files, but 4 of those are upstream base
classes** (`BaseArmor`, `BaseClothing`, `BaseJewel`, `BaseWeapon`). **The content overlap is
13**: the 8 Aloron pieces, already ported in S1 and carrying deviation D-1, plus 5 Darden's set
pieces which need both systems and have neither.

So: **building `SAAbsorptionAttributes` completes 8 files already in our tree, unblocks 5 that
S1 could not finish, and unblocks 44 that need absorption alone.** 8 + 5 + 44 = 57, with
nothing counted twice.

And read the other way round: of the 124 files the armour-set system unblocks, **111 needed it
alone and 13 needed both.** Building absorption after sets adds those 13 to the sum rather
than double-counting them — which is the whole of the "beyond the sum" question here, and the
answer is 13 files, not a multiplier.

`PointsSystems` is the one genuine shared substrate, required by both Vice vs Virtue and City
Loyalty (§7.2). Building both would pay for it once — but both are declines, so the saving is
theoretical.

---

## 10. The re-counted 89

`docs/tasks.md` CC6 states: "**89 (19%) reference at least one type ModernUO does not have.**
This figure is CC2's and has never been independently re-counted."

**It has now, and it does not reproduce at any definition I can construct.** Method: for each
of the 462 `Mobiles/Normal` files, extract every referenced type (`new X(`, `typeof(X)`,
`X.member`, `: X`, `is X`), keep those that are ServUO-declared types absent from the
ModernUO index, and drop the file's own declarations.

| Definition | Count |
|---|---|
| Of 462, files referencing ≥1 ServUO type ModernUO lacks — **including** the Pet Training ability types | **206** |
| Same, **excluding** the Pet Training ability types (which are counted separately as the 103) | **135** |
| Restricted to the 137 files ModernUO does not already ship, including Pet Training types | **81** |
| **Restricted to the 137, excluding Pet Training types** | **65** |

None is 89. The nearest is 81, and it is not close enough to call a rounding difference.

**The number to use for planning is 65**: files ModernUO does not already have, blocked by
something other than Pet Training, i.e. genuinely needing a leaf dependency ported, declined,
or dropped. That is 47% of the real 137-file backlog, not 19% of an inflated 462.

**Sixteen of those 65 disappear on inspection** once §7.1 is applied — `TribeType` alone
accounted for 52 files in the raw scan. The commonest remaining blockers are ordinary leaf
items, which is the `LuckyCoin` precedent and not a decision at all: `LuckyCoin` 12 (already
ported in S2), `Yeast` 8, `ConfirmMountStatuetteGump` 7, `Fur` 6, `ParrotItem` 5, `FurType` 5,
`AncientPotteryFragments` 5, `TatteredAncientScroll` 4, `BouraSkin` 3, `SlithEye` 3, the
Gargish cloth pieces 2 each.

**Eight for eight.** Every count in this project stated without counting has been wrong, and
the 89 is the eighth. Two of the eight were the basis of a decision. The file list is in the
appendix; the number in `docs/tasks.md` should be replaced by 65 with the definition stated
beside it, and this note says so rather than editing `docs/` (`AGENTS.md` ground rule).

---

## 11. Ranked, with a recommendation

Ranked by ratio, then by whether the build is safe under the layering pattern.

| Rank | Item | Unblocked : cost | Verdict |
|---|---|---|---|
| 1 | **`SAAbsorptionAttributes`** | 57 : 1 file (≈350–1,120 lines) | **Build first** |
| 2 | **`TribeType` → `OppositionGroup`** | 9 : ~25 lines | **Free. Not a subsystem. Fold into the next creature batch.** |
| 3 | **203 ML quests onto ModernUO's engine** | 203 quests : 0 subsystem files | **Spike one, then it is content work** |
| 4 | `Services/PointsSystems` | 55 : 12 files | Cost properly on a future menu |
| 5 | Pet Training, ability-definition subset | 79 : 5 files / ≈4,570 lines | Defensible; build **after** the next bump |
| 6 | Myrmidex Invasion | 9 : 6 files | Only alongside Eodon quest work |
| 7 | Vendor Searching | n/a — a feature | Chase's call, ratio irrelevant |
| 8 | City Loyalty | 15 : 28 files | Decline, revisit with Town Cryer |
| 9 | Shadowguard | 8 : 14 files / 11,222 lines | Decline |
| 10 | Instanced Peerless | 2 : 19 files (with base Peerless) | Decline — no base to instance |
| 11 | Vice vs Virtue | 5 : 57 files, 21 patches | Decline |
| 12 | Exploring the Deep | 2 : 70 files | Decline on ratio; safest build if ever wanted |
| 13 | Skill Masteries | 14 : 45 files, **35 patches** | **Decline — does not fit the layering pattern** |
| 14 | ServUO ML quest framework | — | **Decline — two engines for one job.** Superseded by rank 3. |

**What I would build first, and why: `SAAbsorptionAttributes`.**

It is the only row that repeats S1's shape exactly. One additive file against a base class
ModernUO already has (`BaseAttributes`), one aggregation patch of a kind that already works in
this tree, no upstream field, no upstream serialization version, no upstream migration. It
closes an open deviation (D-1) rather than opening new ones, it finishes 8 files already
committed, and it has the best ratio on the menu by a factor of four. The honest caveat is in
§6: the ≈350-line figure buys the property and the tooltips, and the *effect* needs either
`SAPropEffects.cs` or a patch, so cost it at up to ~1,120 lines. Even then it is the best
value here.

**Second, and this is the recommendation I would press hardest: spike one ML quest onto
ModernUO's engine.** It is not a subsystem build at all, it is one session, and if it works it
converts the largest deferred block in `docs/tasks.md` — 203 quests including both Eodon
lines — from "blocked on a 6,269-line framework" into ordinary content work. The cost of
finding out is far below the value of the answer. This is the one item where the measurement
changed what the question is.

**What I would not build: Skill Masteries.** 35 upstream patch points, against a codebase
`docs/upstream-watch.md` shows is mid-refactor on `BaseCreature`, for 14 files. It fails
question 2 and question 3 of `docs/subsystem-policy.md` simultaneously.

---

## 12. What this survey did not do

Stated plainly rather than left implied.

- **No spike, no build, no compile.** Every layering judgment is from reading both trees. S1
  earned its answer with a spike; none of these has been spiked. The `SAAbsorptionAttributes`
  recommendation in particular assumes the S1 aggregation-patch pattern transfers, which is
  strongly indicated and not proven.
- **The ≈470-line `PetTrainingHelper` slice and the ≈350-line absorption file are region
  arithmetic, not written files.** Treat both as floors.
- **ModernUO's ML quest engine is verified to exist, to be the same system, and to carry 240
  quest classes. Its behavioural completeness is not verified.** §5 says so and names the
  spike that would settle it.
- **"Already in ModernUO" is decided by the referencing file's primary declared type.** It is
  right on every case checked by hand (`Dragon`, `Acob`, `Aelorn`, `Aeluva`, `Ahie`,
  `WolfSpider`, `Lion`, `Triton`, `ExploringDeepCreaturesRegion`) but it is a heuristic. A
  ServUO file whose primary type ModernUO has, but whose *other* types it lacks, is classified
  as "already in ModernUO" and slightly **under**-counts the unblock columns. It never
  over-counts them.
- **`Services/PointsSystems` is measured but not costed for layering** (§7.2).
- **Line counts are raw file lines**, including blanks and comments, consistent with how S1
  and S2 counted. Comparisons across rows are therefore fair; comparisons to a "lines of
  logic" figure from anywhere else are not.

---

## 13. Appendix — every file list behind every count

Paths are relative to `D:\UO\ServUO-pub57\Scripts`.

### Pet Training � SpecialAbility, files ModernUO lacks � 53 files
```
Mobiles/Bosses/CrimsonDragon.cs
Mobiles/Bosses/Medusa.cs
Mobiles/Bosses/MonstrousInterredGrizzle.cs
Mobiles/Bosses/Navery/Navrey.cs
Mobiles/Bosses/SlasherOfVeils.cs
Mobiles/Bosses/StygianDragon.cs
Mobiles/Bosses/Travesty.cs
Mobiles/NPCs/Vollem.cs
Mobiles/Named/Grim.cs
Mobiles/Named/SkeletalDragonRenowned.cs
Mobiles/Normal/BloodFox.cs
Mobiles/Normal/BloodWorm.cs
Mobiles/Normal/ColdDrake.cs
Mobiles/Normal/CrimsonDrake.cs
Mobiles/Normal/CrystalHydra.cs
Mobiles/Normal/DragonWolf.cs
Mobiles/Normal/FireDaemon.cs
Mobiles/Normal/FrostDragon.cs
Mobiles/Normal/GiantTurkey.cs
Mobiles/Normal/HighPlainsBoura.cs
Mobiles/Normal/Kepetch.cs
Mobiles/Normal/LowlandBoura.cs
Mobiles/Normal/MaddeningHorror.cs
Mobiles/Normal/MinionOfScelestus.cs
Mobiles/Normal/OsseinRam.cs
Mobiles/Normal/Rotworm.cs
Mobiles/Normal/RuddyBoura.cs
Mobiles/Normal/ShadowDweller.cs
Mobiles/Normal/Slith.cs
Mobiles/Normal/StoneSlith.cs
Mobiles/Normal/ToxicSlith.cs
Mobiles/Normal/Triton.cs
Mobiles/Normal/Viscera.cs
Mobiles/Normal/WildTiger.cs
Quests/Eodon/Valley of One Quest/Creatures.cs
Services/Expansions/Time Of Legends/Mobiles/DragonTurtle.cs
Services/Expansions/Time Of Legends/Mobiles/DragonTurtleHatchling.cs
Services/Expansions/Time Of Legends/Mobiles/Gallusaurus.cs
Services/Expansions/Time Of Legends/Mobiles/GreaterPhoenix.cs
Services/Expansions/Time Of Legends/Mobiles/Saurosaurus.cs
Services/ExploringTheDeep/Mobiles/ObsidianWyvern.cs
Services/ExploringTheDeep/Mobiles/RockMite.cs
Services/ExploringTheDeep/Mobiles/Shadowlord.cs
Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/Creatures.cs
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Abyss.cs
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Cora.cs
Services/Revamped Dungeons/Shame Revamped/Mobiles/Bosses.cs
Services/Revamped Dungeons/Shame Revamped/Mobiles/Creatures.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/BrigandCannibalMage.cs
Services/Seasonal Events/TreasuresOfSorceresDungeon/Creatures/AbominableSnowman.cs
Services/Seasonal Events/TreasuresOfSorceresDungeon/Creatures/NightmareFairy.cs
Services/Seasonal Events/TreasuresOfSorceresDungeon/Creatures/RabidReindeer.cs
Services/Seasonal Events/TreasuresOfSorceresDungeon/Creatures/StockingSerpent.cs
```

### Pet Training � AreaEffect, files ModernUO lacks � 17 files
```
Mobiles/Bosses/ChiefParoxysmus.cs
Mobiles/Bosses/LadyMelisande.cs
Mobiles/Normal/ColdDrake.cs
Mobiles/Normal/FireAnt.cs
Mobiles/Normal/FireDaemon.cs
Mobiles/Normal/FrostDragon.cs
Mobiles/Normal/FrostMite.cs
Mobiles/Normal/GiantTurkey.cs
Mobiles/Normal/Viscera.cs
Quests/Eodon/MyrmidexThreat/Mobiles/Creatures.cs
Services/Expansions/Time Of Legends/Mobiles/Dimetrosaur.cs
Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/Creatures.cs
Services/Revamped Dungeons/Covetous Void Spawn/Creatures/Cora.cs
Services/Revamped Dungeons/Shame Revamped/Mobiles/Bosses.cs
Services/Revamped Dungeons/Shame Revamped/Mobiles/Creatures.cs
Services/Revamped Dungeons/TheExodusEncounter/Mobiles/ClockworkExodus.cs
Services/Seasonal Events/TreasuresOfSorceresDungeon/Creatures/TwistedHolidayTree.cs
```

### Pet Training � MagicalAbility, files ModernUO lacks � 18 files
```
Mobiles/Normal/ClockworkScorpion.cs
Mobiles/Normal/CoralSnake.cs
Mobiles/Normal/CrimsonDrake.cs
Mobiles/Normal/DespiseEvilCreatures.cs
Mobiles/Normal/DespiseGoodCreatures.cs
Mobiles/Normal/Lion.cs
Mobiles/Normal/OsseinRam.cs
Mobiles/Normal/PlatinumDrake.cs
Mobiles/Normal/SabertoothedTiger.cs
Mobiles/Normal/StygianDrake.cs
Mobiles/Normal/Triceratops.cs
Mobiles/Normal/WolfSpider.cs
Services/Expansions/Time Of Legends/Mobiles/Dimetrosaur.cs
Services/Expansions/Time Of Legends/Mobiles/Najasaurus.cs
Services/Seasonal Events/KrampusEncounter/Mobiles/Krampus.cs
Services/Seasonal Events/TreasuresOfKhaldun/Creatures/KhalAnkur.cs
Services/Seasonal Events/TreasuresOfSorceresDungeon/Creatures/GarishGingerman.cs
Services/Seasonal Events/TreasuresOfSorceresDungeon/Creatures/HeadlessElf.cs
```

### Pet Training � gate/profile/gump machinery, files ModernUO lacks � 11 files
```
Gumps/ConfirmMountStatuetteGump.cs
Mobiles/Bosses/Travesty.cs
Mobiles/Normal/ClockworkScorpion.cs
Mobiles/Normal/CoralSnake.cs
Mobiles/Normal/CrimsonDrake.cs
Mobiles/Normal/IronBeetle.cs
Mobiles/Normal/PlatinumDrake.cs
Mobiles/Normal/SabertoothedTiger.cs
Mobiles/Normal/WolfSpider.cs
Services/New Magincia/Magincia Bazaar/Gumps/PetBrokerGumps.cs
Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/Creatures.cs
```

### Pet Training � the 103 Mobiles/Normal files, split: ModernUO already ships these 66 � 66 files
```
Mobiles/Normal/AncientWyrm.cs
Mobiles/Normal/AntLion.cs
Mobiles/Normal/BakeKitsune.cs
Mobiles/Normal/BaseCreature.cs
Mobiles/Normal/Beetle.cs
Mobiles/Normal/Betrayer.cs
Mobiles/Normal/BronzeElemental.cs
Mobiles/Normal/ChaosDragoon.cs
Mobiles/Normal/ChaosDragoonElite.cs
Mobiles/Normal/CorporealBrume.cs
Mobiles/Normal/CorrosiveSlime.cs
Mobiles/Normal/CuSidhe.cs
Mobiles/Normal/DeathWatchBeetle.cs
Mobiles/Normal/DeepSeaSerpent.cs
Mobiles/Normal/Dragon.cs
Mobiles/Normal/Drake.cs
Mobiles/Normal/DreadSpider.cs
Mobiles/Normal/EnslavedGargoyle.cs
Mobiles/Normal/EnslavedSatyr.cs
Mobiles/Normal/FanDancer.cs
Mobiles/Normal/FetidEssence.cs
Mobiles/Normal/FireBeetle.cs
Mobiles/Normal/FireGargoyle.cs
Mobiles/Normal/FireSteed.cs
Mobiles/Normal/GiantSpider.cs
Mobiles/Normal/Golem.cs
Mobiles/Normal/GreaterDragon.cs
Mobiles/Normal/HellCat.cs
Mobiles/Normal/HellHound.cs
Mobiles/Normal/HellSteed.cs
Mobiles/Normal/Hiryu.cs
Mobiles/Normal/Hydra.cs
Mobiles/Normal/IceElemental.cs
Mobiles/Normal/IceFiend.cs
Mobiles/Normal/Juggernaut.cs
Mobiles/Normal/Kappa.cs
Mobiles/Normal/KazeKemono.cs
Mobiles/Normal/LavaLizard.cs
Mobiles/Normal/LavaSerpent.cs
Mobiles/Normal/LavaSnake.cs
Mobiles/Normal/LesserHiryu.cs
Mobiles/Normal/Leviathan.cs
Mobiles/Normal/MantraEffervescence.cs
Mobiles/Normal/Nightmare.cs
Mobiles/Normal/Oni.cs
Mobiles/Normal/PestilentBandage.cs
Mobiles/Normal/Phoenix.cs
Mobiles/Normal/PlagueBeast.cs
Mobiles/Normal/PredatorHellCat.cs
Mobiles/Normal/Reptalon.cs
Mobiles/Normal/Ridgeback.cs
Mobiles/Normal/RuneBeetle.cs
Mobiles/Normal/SavageRidgeback.cs
Mobiles/Normal/ScaledSwampDragon.cs
Mobiles/Normal/Scorpion.cs
Mobiles/Normal/SeaSerpent.cs
Mobiles/Normal/SerpentineDragon.cs
Mobiles/Normal/ShadowWyrm.cs
Mobiles/Normal/SkeletalDragon.cs
Mobiles/Normal/Slime.cs
Mobiles/Normal/Snake.cs
Mobiles/Normal/SnowElemental.cs
Mobiles/Normal/Succubus.cs
Mobiles/Normal/SwampDragon.cs
Mobiles/Normal/TsukiWolf.cs
Mobiles/Normal/ValoriteElemental.cs
```

### Pet Training � the 103 Mobiles/Normal files, split: ModernUO lacks these 37 � 37 files
```
Mobiles/Normal/BloodFox.cs
Mobiles/Normal/BloodWorm.cs
Mobiles/Normal/ClockworkScorpion.cs
Mobiles/Normal/ColdDrake.cs
Mobiles/Normal/CoralSnake.cs
Mobiles/Normal/CrimsonDrake.cs
Mobiles/Normal/CrystalHydra.cs
Mobiles/Normal/DespiseEvilCreatures.cs
Mobiles/Normal/DespiseGoodCreatures.cs
Mobiles/Normal/DragonWolf.cs
Mobiles/Normal/FireAnt.cs
Mobiles/Normal/FireDaemon.cs
Mobiles/Normal/FrostDragon.cs
Mobiles/Normal/FrostMite.cs
Mobiles/Normal/GiantTurkey.cs
Mobiles/Normal/HighPlainsBoura.cs
Mobiles/Normal/IronBeetle.cs
Mobiles/Normal/Kepetch.cs
Mobiles/Normal/Lion.cs
Mobiles/Normal/LowlandBoura.cs
Mobiles/Normal/MaddeningHorror.cs
Mobiles/Normal/MinionOfScelestus.cs
Mobiles/Normal/OsseinRam.cs
Mobiles/Normal/PlatinumDrake.cs
Mobiles/Normal/Rotworm.cs
Mobiles/Normal/RuddyBoura.cs
Mobiles/Normal/SabertoothedTiger.cs
Mobiles/Normal/ShadowDweller.cs
Mobiles/Normal/Slith.cs
Mobiles/Normal/StoneSlith.cs
Mobiles/Normal/StygianDrake.cs
Mobiles/Normal/ToxicSlith.cs
Mobiles/Normal/Triceratops.cs
Mobiles/Normal/Triton.cs
Mobiles/Normal/Viscera.cs
Mobiles/Normal/WildTiger.cs
Mobiles/Normal/WolfSpider.cs
```

### Pet Training � upstream files that would need patching � 96 files
These are ServUO files whose ModernUO counterpart exists. They are cost, not benefit.
```
Abilities/Bladeweave.cs
Abilities/Block.cs
Abilities/Feint.cs
Abilities/FrenziedWhirlwind.cs
Abilities/NerveStrike.cs
Abilities/TalonStrike.cs
Items/Equipment/Instruments/BaseInstrument.cs
Misc/AOS.cs
Misc/SkillCheck.cs
Mobiles/AI/Magical AI/MageAI.cs
Mobiles/Bosses/Mephitis.cs
Mobiles/Bosses/Semidar.cs
Mobiles/Bosses/Serado.cs
Mobiles/NPCs/AnimalTrainer.cs
Mobiles/Named/Abscess.cs
Mobiles/Named/Gnaw.cs
Mobiles/Named/Guile.cs
Mobiles/Named/Ilhenir.cs
Mobiles/Named/Irk.cs
Mobiles/Named/RedDeath.cs
Mobiles/Named/Rend.cs
Mobiles/Named/SirPatrick.cs
Mobiles/Named/Spite.cs
Mobiles/Named/Swoop.cs
Mobiles/Named/Szavetra.cs
Mobiles/Normal/AncientWyrm.cs
Mobiles/Normal/AntLion.cs
Mobiles/Normal/BakeKitsune.cs
Mobiles/Normal/BaseCreature.cs
Mobiles/Normal/Beetle.cs
Mobiles/Normal/Betrayer.cs
Mobiles/Normal/BronzeElemental.cs
Mobiles/Normal/ChaosDragoon.cs
Mobiles/Normal/ChaosDragoonElite.cs
Mobiles/Normal/CorporealBrume.cs
Mobiles/Normal/CorrosiveSlime.cs
Mobiles/Normal/CuSidhe.cs
Mobiles/Normal/DeathWatchBeetle.cs
Mobiles/Normal/DeepSeaSerpent.cs
Mobiles/Normal/Dragon.cs
Mobiles/Normal/Drake.cs
Mobiles/Normal/DreadSpider.cs
Mobiles/Normal/EnslavedGargoyle.cs
Mobiles/Normal/EnslavedSatyr.cs
Mobiles/Normal/FanDancer.cs
Mobiles/Normal/FetidEssence.cs
Mobiles/Normal/FireBeetle.cs
Mobiles/Normal/FireGargoyle.cs
Mobiles/Normal/FireSteed.cs
Mobiles/Normal/GiantSpider.cs
Mobiles/Normal/Golem.cs
Mobiles/Normal/GreaterDragon.cs
Mobiles/Normal/HellCat.cs
Mobiles/Normal/HellHound.cs
Mobiles/Normal/HellSteed.cs
Mobiles/Normal/Hiryu.cs
Mobiles/Normal/Hydra.cs
Mobiles/Normal/IceElemental.cs
Mobiles/Normal/IceFiend.cs
Mobiles/Normal/Juggernaut.cs
Mobiles/Normal/Kappa.cs
Mobiles/Normal/KazeKemono.cs
Mobiles/Normal/LavaLizard.cs
Mobiles/Normal/LavaSerpent.cs
Mobiles/Normal/LavaSnake.cs
Mobiles/Normal/LesserHiryu.cs
Mobiles/Normal/Leviathan.cs
Mobiles/Normal/MantraEffervescence.cs
Mobiles/Normal/Nightmare.cs
Mobiles/Normal/Oni.cs
Mobiles/Normal/PestilentBandage.cs
Mobiles/Normal/Phoenix.cs
Mobiles/Normal/PlagueBeast.cs
Mobiles/Normal/PredatorHellCat.cs
Mobiles/Normal/Reptalon.cs
Mobiles/Normal/Ridgeback.cs
Mobiles/Normal/RuneBeetle.cs
Mobiles/Normal/SavageRidgeback.cs
Mobiles/Normal/ScaledSwampDragon.cs
Mobiles/Normal/Scorpion.cs
Mobiles/Normal/SeaSerpent.cs
Mobiles/Normal/SerpentineDragon.cs
Mobiles/Normal/ShadowWyrm.cs
Mobiles/Normal/SkeletalDragon.cs
Mobiles/Normal/Slime.cs
Mobiles/Normal/Snake.cs
Mobiles/Normal/SnowElemental.cs
Mobiles/Normal/Succubus.cs
Mobiles/Normal/SwampDragon.cs
Mobiles/Normal/TsukiWolf.cs
Mobiles/Normal/ValoriteElemental.cs
Services/Ethics/Evil/Mobiles/UnholySteed.cs
Services/Ethics/Hero/Mobiles/HolySteed.cs
Skills/AnimalLore.cs
Skills/AnimalTaming.cs
Skills/Discordance.cs
```

### SAAbsorptionAttributes � files ModernUO lacks � 57 files
```
Abilities/Enhancement.cs
Abilities/EnhancementTimer.cs
Abilities/SAPropEffects.cs
Items/Artifacts/DespiseArtifacts.cs
Items/Artifacts/Equipment/Armor/BasiliskHideBreastplate.cs
Items/Artifacts/Equipment/Armor/BritchesOfWarding.cs
Items/Artifacts/Equipment/Armor/CrownOfArcaneTemperament.cs
Items/Artifacts/Equipment/Armor/DefenderOfTheMagus.cs
Items/Artifacts/Equipment/Armor/DragonHideShield.cs
Items/Artifacts/Equipment/Armor/KelpWovenLeggings.cs
Items/Artifacts/Equipment/Armor/MantleOfTheFallen.cs
Items/Artifacts/Equipment/Armor/ProtectoroftheBattleMage.cs
Items/Artifacts/Equipment/Armor/ResonantShieldOfVengeance.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsBustier.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsLongSkirt.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsShorts.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsSkirt.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsTunic.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensBustier.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensSleeves.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensTunic.cs
Items/Artifacts/Equipment/Armor/SpinedBloodwormBracers.cs
Items/Artifacts/Equipment/Armor/SummonersKilt.cs
Items/Artifacts/Equipment/Armor/VoidInfusedKilt.cs
Items/Artifacts/Equipment/Armor/WallOfHungryMouths.cs
Items/Artifacts/Equipment/Armor/WardedDemonboneBracers.cs
Items/Artifacts/Equipment/Clothing/RangersCloakOfAugmentation.cs
Items/Artifacts/Equipment/Clothing/WardensArmorOfAugmentation.cs
Items/Artifacts/Equipment/Jewelry/BraceletOfPrimalConsumption.cs
Items/Artifacts/Equipment/Jewelry/DragonJadeEarrings.cs
Items/Artifacts/Equipment/Jewelry/Lavaliere.cs
Items/Artifacts/Equipment/Jewelry/ObsidianEarrings.cs
Items/Artifacts/Equipment/Weapons/DraconisWrath.cs
Items/Artifacts/Equipment/Weapons/JadeWarAxe.cs
Items/Artifacts/Equipment/Weapons/PetrifiedSnake.cs
Items/Artifacts/Equipment/Weapons/ResonantStaffOfEnlightenment.cs
Items/Artifacts/Equipment/Weapons/StaffOfResonance.cs
Items/Artifacts/Equipment/Weapons/StoneDragonsTooth.cs
Items/Artifacts/Talismans/FrostguardTalisman.cs
Items/Artifacts/Talismans/JadeSnakeHead.cs
Mobiles/NPCs/Mannequin/Property/AbsorptionAttributeProperty.cs
Services/Expansions/High Seas/Items/Artifacts/LeviathanHideBracers.cs
Services/Expansions/Time Of Legends/Shadowguard/Artifacts.cs
Services/LootGeneration/Imbuing/Core/Imbuing.cs
Services/LootGeneration/ItemPropertiesGump.cs
Services/LootGeneration/ItemPropertyInfo.cs
Services/LootGeneration/RunicReforging/RunicReforging.cs
Services/Revamped Dungeons/Covetous Void Spawn/Items/BraceletOfProtection.cs
Services/Vendor Searching/VendorSearch.cs
Services/Vendor Searching/VendorSearchCriteria.cs
Services/ViceVsVirtue/Items/Rewards/VvVChests.cs
Spells/Skill Masteries/Core/SkillMasterySpell.cs
```

### SAAbsorptionAttributes � upstream patch targets � 7 files
```
Items/Equipment/Armor/BaseArmor.cs
Items/Equipment/Clothing/BaseClothing.cs
Items/Equipment/Jewelry/BaseJewel.cs
Items/Equipment/Talismans/BaseTalisman.cs
Items/Equipment/Weapons/BaseWeapon.cs
Misc/AOS.cs
Spells/Base/Spell.cs
```

### SAAbsorptionAttributes x armour sets � the 17 overlap � 17 files
```
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsBustier.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsLongSkirt.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsShorts.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsSkirt.cs
Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsTunic.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensBustier.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensSleeves.cs
Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensTunic.cs
Items/Equipment/Armor/BaseArmor.cs
Items/Equipment/Clothing/BaseClothing.cs
Items/Equipment/Jewelry/BaseJewel.cs
Items/Equipment/Weapons/BaseWeapon.cs
```

### ServUO ML quest framework � files ModernUO already has � 114 files
```
Misc/Notoriety.cs
Misc/SkillCheck.cs
Mobiles/NPCs/Aelorn.cs
Mobiles/NPCs/Aeluva.cs
Mobiles/NPCs/Aernya.cs
Mobiles/NPCs/Ahie.cs
Mobiles/NPCs/AldenArmstrong.cs
Mobiles/NPCs/Alefian.cs
Mobiles/NPCs/Alejaha.cs
Mobiles/NPCs/AndreasVesalius.cs
Mobiles/NPCs/Andric.cs
Mobiles/NPCs/Andros.cs
Mobiles/NPCs/Aniel.cs
Mobiles/NPCs/AnimalTrainer.cs
Mobiles/NPCs/Anolly.cs
Mobiles/NPCs/Arielle.cs
Mobiles/NPCs/Asandos.cs
Mobiles/NPCs/Aulan.cs
Mobiles/NPCs/Aurelia.cs
Mobiles/NPCs/Avicenna.cs
Mobiles/NPCs/Belulah.cs
Mobiles/NPCs/Ben.cs
Mobiles/NPCs/Beotham.cs
Mobiles/NPCs/Braen.cs
Mobiles/NPCs/Bravehorn.cs
Mobiles/NPCs/Brinnae.cs
Mobiles/NPCs/Caelas.cs
Mobiles/NPCs/Cailla.cs
Mobiles/NPCs/Canir.cs
Mobiles/NPCs/Chiyo.cs
Mobiles/NPCs/Churchill.cs
Mobiles/NPCs/Ciala.cs
Mobiles/NPCs/Cillitha.cs
Mobiles/NPCs/Clairesse.cs
Mobiles/NPCs/Clehin.cs
Mobiles/NPCs/Cloorne.cs
Mobiles/NPCs/Dallid.cs
Mobiles/NPCs/Danoel.cs
Mobiles/NPCs/Darius.cs
Mobiles/NPCs/Dimethro.cs
Mobiles/NPCs/Drithen.cs
Mobiles/NPCs/Emerillo.cs
Mobiles/NPCs/Emilio.cs
Mobiles/NPCs/Enigma.cs
Mobiles/NPCs/Evan.cs
Mobiles/NPCs/Frederic.cs
Mobiles/NPCs/GeorgeHephaestus.cs
Mobiles/NPCs/Gervis.cs
Mobiles/NPCs/Gorrow.cs
Mobiles/NPCs/Gustar.cs
Mobiles/NPCs/Hamato.cs
Mobiles/NPCs/Hargrove.cs
Mobiles/NPCs/Huntsman.cs
Mobiles/NPCs/Jamal.cs
Mobiles/NPCs/Jelrice.cs
Mobiles/NPCs/Jillian.cs
Mobiles/NPCs/Jockles.cs
Mobiles/NPCs/Jun.cs
Mobiles/NPCs/Jusae.cs
Mobiles/NPCs/Kaelynna.cs
Mobiles/NPCs/Kashiel.cs
Mobiles/NPCs/Kia.cs
Mobiles/NPCs/Koole.cs
Mobiles/NPCs/Landy.cs
Mobiles/NPCs/Leon.cs
Mobiles/NPCs/Lissbet.cs
Mobiles/NPCs/Lohn.cs
Mobiles/NPCs/Lowel.cs
Mobiles/NPCs/Lyle.cs
Mobiles/NPCs/Mielan.cs
Mobiles/NPCs/Mithneral.cs
Mobiles/NPCs/Morganna.cs
Mobiles/NPCs/Mugg.cs
Mobiles/NPCs/Mulcivikh.cs
Mobiles/NPCs/Nedrick.cs
Mobiles/NPCs/Nibbet.cs
Mobiles/NPCs/Norton.cs
Mobiles/NPCs/Olla.cs
Mobiles/NPCs/Patricus.cs
Mobiles/NPCs/Recaro.cs
Mobiles/NPCs/Regina.cs
Mobiles/NPCs/Robyn.cs
Mobiles/NPCs/Ryuichi.cs
Mobiles/NPCs/Sadrah.cs
Mobiles/NPCs/Salaenih.cs
Mobiles/NPCs/Saril.cs
Mobiles/NPCs/SarsmeaSmythe.cs
Mobiles/NPCs/Sledge.cs
Mobiles/NPCs/Sleen.cs
Mobiles/NPCs/Strongroot.cs
Mobiles/NPCs/Synaeva.cs
Mobiles/NPCs/Tallinin.cs
Mobiles/NPCs/Tamm.cs
Mobiles/NPCs/Thalia.cs
Mobiles/NPCs/Thallary.cs
Mobiles/NPCs/Tholef.cs
Mobiles/NPCs/Tiana.cs
Mobiles/NPCs/Tillanil.cs
Mobiles/NPCs/TylAriadne.cs
Mobiles/NPCs/Unoelil.cs
Mobiles/NPCs/Vilo.cs
Mobiles/NPCs/Waelian.cs
Mobiles/NPCs/Walker.cs
Mobiles/NPCs/Yorus.cs
Mobiles/Normal/Sheep.cs
Mobiles/PlayerMobile.cs
Quests/BatteredBucket.cs
Services/Craft/Core/CraftItem.cs
Services/Expansions/High Seas/Regions/SeaMarket.cs
Services/Expansions/MondainsLegacy.cs
Services/Harvest/Fishing.cs
Skills/Discordance.cs
Skills/Peacemaking.cs
Skills/Provocation.cs
```

### ServUO ML quest framework � files ModernUO lacks � 176 files
```
Items/Consumables/ScrollofAlacrity.cs
Items/Containers/CraftsmanSatchel.cs
Items/Containers/JaacarBox.cs
Items/Containers/RewardBackpack.cs
Items/Containers/RewardBag.cs
Items/Containers/RewardBox.cs
Items/Functional/DespiseAnkh.cs
Items/Internal/CitadelTeleporters.cs
Items/Internal/TwistedWealdTeleporters.cs
Items/Quest/MapFragment.cs
Items/Quest/SAQuestItems.cs
Items/StoreBought/RaceChangeToken.cs
Misc/SpawnerPersistence.cs
Misc/Waypoints.cs
Mobiles/Bosses/Navery/Navrey.cs
Mobiles/NPCs/Acob.cs
Mobiles/NPCs/Agralem.cs
Mobiles/NPCs/Aliabeth.cs
Mobiles/NPCs/Amelia.cs
Mobiles/NPCs/Ansikart.cs
Mobiles/NPCs/Aurvidlem.cs
Mobiles/NPCs/Axem.cs
Mobiles/NPCs/Barreraak.cs
Mobiles/NPCs/Beninort.cs
Mobiles/NPCs/Brae.cs
Mobiles/NPCs/Broolol.cs
Mobiles/NPCs/Calendor.cs
Mobiles/NPCs/Cohenn.cs
Mobiles/NPCs/DenthesJournal.cs
Mobiles/NPCs/Dugan.cs
Mobiles/NPCs/Egwexem.cs
Mobiles/NPCs/Escortables.cs
Mobiles/NPCs/Fabrizio.cs
Mobiles/NPCs/FarmerNash.cs
Mobiles/NPCs/Frazer.cs
Mobiles/NPCs/FrightenedDryad.cs
Mobiles/NPCs/Gnosos.cs
Mobiles/NPCs/Gretchen.cs
Mobiles/NPCs/Ioseph.cs
Mobiles/NPCs/Jaacar.cs
Mobiles/NPCs/Jacob.cs
Mobiles/NPCs/Kodar.cs
Mobiles/NPCs/Laifem.cs
Mobiles/NPCs/Lefty.cs
Mobiles/NPCs/Lenley.cs
Mobiles/NPCs/Lucius.cs
Mobiles/NPCs/Maul.cs
Mobiles/NPCs/MysteriousWisp.cs
Mobiles/NPCs/Natalie.cs
Mobiles/NPCs/Naxatillor.cs
Mobiles/NPCs/Neil.cs
Mobiles/NPCs/Neville.cs
Mobiles/NPCs/Nillaen.cs
Mobiles/NPCs/Onallan.cs
Mobiles/NPCs/Oolua.cs
Mobiles/NPCs/Percolem.cs
Mobiles/NPCs/Petrus.cs
Mobiles/NPCs/QuartermasterFlint.cs
Mobiles/NPCs/Rollarn.cs
Mobiles/NPCs/Ryal.cs
Mobiles/NPCs/Sarakki.cs
Mobiles/NPCs/Siarra.cs
Mobiles/NPCs/Sliem.cs
Mobiles/NPCs/Szandor.cs
Mobiles/NPCs/Thepem.cs
Mobiles/NPCs/Tobin.cs
Mobiles/NPCs/Verity.cs
Mobiles/NPCs/Xenrr.cs
Mobiles/NPCs/Zhah.cs
Mobiles/NPCs/Zosilem.cs
Mobiles/Normal/Gregorio.cs
Mobiles/Normal/Rotworm.cs
Quests/ALittleSomething.cs
Quests/ATangledWeb.cs
Quests/AemaethQuests.cs
Quests/BadCompany.cs
Quests/Bard Mastery Quests/SirBerran.cs
Quests/Bard Mastery Quests/SirFelean.cs
Quests/Bard Mastery Quests/SirHareus.cs
Quests/Bedlam.cs
Quests/BlightedGrove.cs
Quests/CloakOfHumility/CloakOfHumilityQuest.cs
Quests/CloakOfHumility/CollectionsObjective.cs
Quests/CloakOfHumility/Mobiles/Gareth.cs
Quests/CloakOfHumility/Mobiles/HumilityQuestMobile.cs
Quests/Discipline.cs
Quests/DiscoveringAnimalTraining/DiscoveringAnimalTraining.cs
Quests/DoughtyWarriorsQuest.cs
Quests/ElfHeritage.cs
Quests/EndingtheThreat.cs
Quests/Eodon/MyrmidexThreat/Items/QuestItems.cs
Quests/Eodon/MyrmidexThreat/Items/Rewards.cs
Quests/Eodon/MyrmidexThreat/Items/Teleporter.cs
Quests/Eodon/MyrmidexThreat/Mobiles/Questers.cs
Quests/Eodon/MyrmidexThreat/Quests.cs
Quests/Eodon/Valley of One Quest/Creatures.cs
Quests/Eodon/Valley of One Quest/DragonTurtleNest.cs
Quests/Eodon/Valley of One Quest/Items.cs
Quests/Eodon/Valley of One Quest/Questers.cs
Quests/Eodon/Valley of One Quest/Quests.cs
Quests/Eodon/Valley of One Quest/TigerCubEnclosure.cs
Quests/EscortToDugan.cs
Quests/Escortables.cs
Quests/FriendsOfTheLibrary.cs
Quests/GatheringOfEvidence.cs
Quests/Gemkeepers.cs
Quests/GhostOfCovetous.cs
Quests/HonestBeggar.cs
Quests/HonorOfDeBoorsQuest.cs
Quests/HumanHeritage.cs
Quests/JourneyToTheAthenaeumIsleQuest.cs
Quests/KnowledgeoftheSoulforge.cs
Quests/Mad Scientist/Sutek.cs
Quests/Marauders.cs
Quests/MasteringtheSoulforge.cs
Quests/Missing.cs
Quests/MougGurrMustDie.cs
Quests/Ortlem.cs
Quests/PeptaQuest.cs
Quests/RatmenSanctuaryQuest.cs
Quests/Sacred Quest/QuestOfSingularity.cs
Quests/Sacred Quest/ShrineOfSingularity.cs
Quests/SecretsoftheSoulforge.cs
Quests/Spellweaving.cs
Quests/SummonFey.cs
Quests/SummonFiend.cs
Quests/The Ritual/Items.cs
Quests/The Ritual/Mobiles.cs
Quests/The Ritual/Puzzle.cs
Quests/The Ritual/Quests.cs
Quests/TheAncientWorld.cs
Quests/TieredQuests/PercolemTieredQuests.cs
Quests/TieredQuests/ThepemTieredQuests.cs
Quests/TieredQuests/ZosilemTieredQuests.cs
Quests/UnfadingMemories.cs
Quests/UnusualGoods.cs
Quests/Vernix.cs
Services/CommunityCollections/BaseCollectionItem.cs
Services/CommunityCollections/BaseCollectionMobile.cs
Services/CommunityCollections/CommunityCollectionGump.cs
Services/Expansions/High Seas/Quests/ProfessionFishQuest/FishMonger.cs
Services/Expansions/High Seas/Quests/ProfessionFishQuest/FishQuestHelper.cs
Services/Expansions/High Seas/Quests/ProfessionFishQuest/ProfessionalFisherQuest.cs
Services/Expansions/High Seas/Quests/ProfessionalBountyQuest/Items/BindingPole.cs
Services/Expansions/High Seas/Quests/ProfessionalBountyQuest/Mobiles/PirateCaptain.cs
Services/Expansions/High Seas/Quests/ProfessionalBountyQuest/Mobiles/SeaMarketOfficer.cs
Services/Expansions/High Seas/Quests/ProfessionalBountyQuest/ProfessionalBountyQuest.cs
Services/ExploringTheDeep/Items/Teleporter/Whirlpool.cs
Services/FireCasino/DiceGames.cs
Services/HuntmasterChallenge/HuntingSystem.cs
Services/Revamped Dungeons/Covetous Void Spawn/VoidPoolController.cs
Services/Revamped Dungeons/WrongDungeon/Mobile/WrongPrisoner.cs
Services/Revamped Dungeons/WrongDungeon/Quests/EscortToWrongEntrance.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/GoingGumshoeQuest.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/Items/DamagedHeadstone.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/Items/DustPile.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/Items/GumshoeForensicItems.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/Items/MysteriousBook.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/Items/TrapDoor.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/Mobiles/Cryptologist.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/Mobiles/GraveDigger.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/Mobiles/Jasper.cs
Services/Seasonal Events/TreasuresOfKhaldun/Quest/Mobiles/SageHumbolt.cs
Services/Town Cryer/Gumps/TownCryerCompleteQuestGump.cs
Services/Town Cryer/Gumps/TownCryerGump.cs
Services/Town Cryer/Gumps/TownCryerNewsGump.cs
Services/Town Cryer/Quests/APleaFromMinocQuest.cs
Services/Town Cryer/Quests/AVisitToCastleBlackthornQuest.cs
Services/Town Cryer/Quests/BuriedRichesQuest.cs
Services/Town Cryer/Quests/ExploringTheDeepQuest.cs
Services/Town Cryer/Quests/HuntmastersChallengeQuest.cs
Services/Town Cryer/Quests/PaladinsOfTrinsic.cs
Services/Town Cryer/Quests/QuestItems.cs
Services/Town Cryer/Quests/RightingWrongQuest.cs
Services/Town Cryer/Quests/WishesOfTheWispsQuest.cs
Services/Town Cryer/TownCryerSystem.cs
```

### ML quests ServUO has and ModernUO does not, by class name � 203 files
```
ABrokenVaseQuest
AForcedSacraficeQuest
AForcedSacraficeQuest2
ALittleSomething
APleaFromMinocQuest
ATangledWeb
ATinkersTaskQuest
AVisitToCastleBlackthornQuest
AWorthyPropositionQuest
AccessToTheStacksQuest
AemaethOneQuest
AemaethTwoQuest
AllThatGlitters
AmbushingTheAmbushersQuest
ArmorUp
BadCompany
BibliophileQuest
BigJobQuest
BlackOrderBadgesQuest
BoundToTheLandQuest
BouraBouraAndMoreBouraQuest
BouraBouraQuest
BureaucraticDelayQuest
BuriedRichesQuest
CatchMeIfYouCanQuest
ChillInTheAirQuest
ClearingCovetousQuest
ClockworkPuzzleQuest
CommunityServiceLibraryQuest
CommunityServiceMuseumQuest
CommunityServiceZooQuest
CowardsQuest
CrackingTheWhipQuest
CrystallineFragmentsQuest
Curiosities
DabblingontheDarkSide
DestructionOfZipactriotlQuest
DishBestServedColdQuest
DoneInTheNameOfTinkeringQuest
DoughtyWarriors2Quest
DoughtyWarriors3Quest
DoughtyWarriorsQuest
EmptyNestQuest
EndingtheThreat
EscortToBritainQuest
EscortToCoveQuest
EscortToDugan
EscortToJhelomQuest
EscortToMaginciaQuest
EscortToMinocQuest
EscortToMoonglowQuest
EscortToNujelmQuest
EscortToSerpentsHoldQuest
EscortToSkaraQuest
EscortToTrinsicQuest
EscortToVesperQuest
EscortToWrongEntrance
EscortToYewQuest
EvidenceQuest
ExploringTheDeepQuest
ExterminatingTheInfestationQuest
EyesOfRangerQuest
FathersGratitudeQuest
FeatherInYerCapQuest
FilthyLifeStealersQuest
FineFeastQuest
FirendOfTheFeyQuest
FreedomQuest
FriendsOfTheLibraryQuest
GatheringOfEvidence
GatheringProof
GentleBladeQuest
GettingEvenQuest
GhostOfCovetousQuest
GoingGumshoeQuest
GoingGumshoeQuest2
GoingGumshoeQuest3
GoingGumshoeQuest4
GreenWithEnvyQuest
GuiltyQuest
HeartOfIceQuest
HeroInTheMakingQuest
HiddenTreasuresQuest
HonorOfDeBoorsQuest
HuntmastersChallengeQuest
HuteCoutureQuest
ImpressivePlaidQuest
InTheBellyOfTheBeastQuest
InTheWeeds
IndoctrinationOfABattleRouserQuest
InsecticideAndRegicideQuest
IntoTheVoidQuest
IronWillQuest
ItMakesMeSickQuest
ItsAMadMadWorldQuest
ItsGhastlyJobQuest
JackTheVillainQuest
JourneyToTheAthenaeumIsleQuest
KnowledgeoftheSoulforge
KodarsRescueQuest
LastWordsQuest
LeadingIntoBattleQuest
MakingContributionHeartwoodQuest
MakingContributionSanctuaryQuest
MasteringtheSoulforge
MessageInBottleQuest
MetalHead
MisplacedQuest
Missing
MysticsJourneyQuest
NeedsOfManyHeartwoodQuest
NeedsOfManyPartHeartwoodQuest
NewHavenAlchemistEscortQuest
NewHavenBankEscortQuest
NewHavenBardEscortQuest
NewHavenBowyerEscortQuest
NewHavenCarpenterEscortQuest
NewHavenDocksEscortQuest
NewHavenFarmEscortQuest
NewHavenInnEscortQuest
NewHavenMageEscortQuest
NewHavenMapmakerEscortQuest
NewHavenTailorEscortQuest
NewHavenWarriorEscortQuest
NewSpinQuest
NiceShirtQuest
OfVorpalsAndLettacesTheGardnerQuest
PaladinsOfTrinsic
PaladinsOfTrinsic2
PeptaQuest
PerfectTimingQuest
PestControlQuest
PinkistheNewBlack
PrideOfTheAmbushQuest
PristineCrystalLotusQuest
ProfessionalBountyQuest
ProfessionalFisherQuest
ProtectorsEssenceQuest
PureValorite
PuttingThePiecesTogetherQuest
QuestOfSingularity
RaptorliciousQuest
ResponsibilityQuest
RevengeOfTheSlithQuest
RightingWrongQuest
RightingWrongQuest2
RightingWrongQuest3
RightingWrongQuest4
RockAndHardPlaceQuest
RumorsAboundQuest
SavedHonorQuest
ScalesOfADreamSerpentQuest
ScrapingtheBottom
SecretsoftheSoulforge
ShearingKnowledgeQuest
ShotAnArrowIntoTheAirQuest
SimpleBowQuest
SomethingFishy
SpecialDeliveryQuest
SpringCleaningQuest
StitchInTimeQuest
TaleOfTailQuest
TamingPetQuest
TastyTreats
TeachingSomethingNewQuest
TearsOfASoulbinderQuest
TheArisenQuest
TheBeaconOfHarmonyQuest
TheBrainyAlchemist
TheDreamersQuest
TheExchangeQuest
TheForbiddenFruit
TheGreatApeQuest
TheGreatHuntQuest
TheGreatVolcanoQuest
TheQuestionsQuest
TheSaltySeaQuest
TheSecretIngredientQuest
TheSlithWarsQuest
TheTreasureChaseQuest
TheZealotryOfZipactriotlQuest
ThievesBeAfootQuest
TimeIsOfTheEssenceQuest
ToTurnBaseMetalIntoVerite
TokenOfLoveQuest
ToolsOfTheTradeQuest
TrogAndHisDogQuest
UnfadingMemoriesOneQuest
UnfadingMemoriesThreeQuest
UnfadingMemoriesTwoQuest
UnitingTheTribesQuest
UntanglingTheWebQuest
UnusualGoods
UsingAnimalLoreQuest
WatchYourStepQuest
WeavingFriendshipsQuest
WeveGotAnAntProblemQuest
WhisperingWithWispsQuest
WhosMostHumbleQuest
WieldingTheSonicBladeQuest
WishesOfTheWispQuest
WondersOfTheNaturalWorldQuest
YeOldeGargishQuest
```

### Myrmidex Invasion � cost: its own files � 6 files
```
Services/Expansions/Time Of Legends/Myrmidex Invasion/AllegianceIdol.cs
Services/Expansions/Time Of Legends/Myrmidex Invasion/BattleFlag.cs
Services/Expansions/Time Of Legends/Myrmidex Invasion/BattleRegion.cs
Services/Expansions/Time Of Legends/Myrmidex Invasion/BattleSpawner.cs
Services/Expansions/Time Of Legends/Myrmidex Invasion/MoonstonePowerGenerator.cs
Services/Expansions/Time Of Legends/Myrmidex Invasion/System.cs
```

### Myrmidex Invasion � files ModernUO lacks that reference it � 9 files
```
Quests/Eodon/MyrmidexThreat/Generate.cs
Quests/Eodon/MyrmidexThreat/Items/Teleporter.cs
Quests/Eodon/MyrmidexThreat/Mobiles/Creatures.cs
Quests/Eodon/MyrmidexThreat/Quests.cs
Services/Expansions/Time Of Legends/Mobiles/BritannianInfantry.cs
Services/Expansions/Time Of Legends/Mobiles/EodonTribesman.cs
Services/Expansions/Time Of Legends/Mobiles/MyrmidexDrone.cs
Services/Expansions/Time Of Legends/Mobiles/MyrmidexLarvae.cs
Services/Expansions/Time Of Legends/Mobiles/MyrmidexWarrior.cs
```

### Myrmidex Invasion � upstream patch targets � 2 files
```
Mobiles/Normal/BaseCreature.cs
Services/Factions/Core/Faction.cs
```

### Shadowguard � cost: its own files � 14 files
```
Services/Expansions/Time Of Legends/Shadowguard/Addons/ArmoryAddon.cs
Services/Expansions/Time Of Legends/Shadowguard/Addons/BarAddon.cs
Services/Expansions/Time Of Legends/Shadowguard/Addons/BelfryAddon.cs
Services/Expansions/Time Of Legends/Shadowguard/Addons/FountainAddon.cs
Services/Expansions/Time Of Legends/Shadowguard/Addons/OrchardAddon.cs
Services/Expansions/Time Of Legends/Shadowguard/Artifacts.cs
Services/Expansions/Time Of Legends/Shadowguard/Bosses.cs
Services/Expansions/Time Of Legends/Shadowguard/Controller.cs
Services/Expansions/Time Of Legends/Shadowguard/Encounters.cs
Services/Expansions/Time Of Legends/Shadowguard/ExitEntry.cs
Services/Expansions/Time Of Legends/Shadowguard/Items.cs
Services/Expansions/Time Of Legends/Shadowguard/Mobiles.cs
Services/Expansions/Time Of Legends/Shadowguard/ShadowguardEncounter.cs
Services/Expansions/Time Of Legends/Shadowguard/ShadowguardInstance.cs
```

### Shadowguard � files ModernUO lacks that reference it � 8 files
```
Items/Artifacts/Equipment/Jewelry/AnkhPendant.cs
Services/22nd Anniversary/Items/CopperWings.cs
Services/Astronomy/Telescope.cs
Services/Expansions/Time Of Legends/Items/CardOfSemidar.cs
Services/Expansions/TimeOfLegends.cs
Services/LootGeneration/RandomItemGenerator.cs
Services/XmlSpawner/XmlSpawner Core/XmlUtils/XmlFind.cs
Spells/Skill Masteries/CommandUndead.cs
```

### Shadowguard � upstream patch targets � 4 files
```
Abilities/SlayerGroup.cs
Items/Decorative/MonsterStatuette.cs
Mobiles/PlayerMobile.cs
Services/VeteranRewards/RewardSystem.cs
```

### Skill Masteries � cost: its own files � 45 files
```
Spells/Skill Masteries/BardSpells/BardSpell.cs
Spells/Skill Masteries/BardSpells/Despair.cs
Spells/Skill Masteries/BardSpells/Perseverance.cs
Spells/Skill Masteries/BardSpells/Resilience.cs
Spells/Skill Masteries/BardSpells/Tribulation.cs
Spells/Skill Masteries/BardSpells/inspire.cs
Spells/Skill Masteries/BardSpells/invigorate.cs
Spells/Skill Masteries/BodyGuard.cs
Spells/Skill Masteries/CalledShot.cs
Spells/Skill Masteries/CombatTraining.cs
Spells/Skill Masteries/CommandUndead.cs
Spells/Skill Masteries/Conduit.cs
Spells/Skill Masteries/Core/MasteryInfo.cs
Spells/Skill Masteries/Core/SelectMasteryGump.cs
Spells/Skill Masteries/Core/SkillMasteryMove.cs
Spells/Skill Masteries/Core/SkillMasteryPrimer.cs
Spells/Skill Masteries/Core/SkillMasterySpell.cs
Spells/Skill Masteries/DeathRay.cs
Spells/Skill Masteries/ElementalFury.cs
Spells/Skill Masteries/EtherealBurst.cs
Spells/Skill Masteries/FistsOfFury.cs
Spells/Skill Masteries/FlamingShot.cs
Spells/Skill Masteries/FocusedEye.cs
Spells/Skill Masteries/HeightenSenses.cs
Spells/Skill Masteries/HolyFistSpell.cs
Spells/Skill Masteries/InjectedStrike.cs
Spells/Skill Masteries/ManaShield.cs
Spells/Skill Masteries/MysticWeapon.cs
Spells/Skill Masteries/NetherBlast.cs
Spells/Skill Masteries/Onslaught.cs
Spells/Skill Masteries/PassiveMastery.cs
Spells/Skill Masteries/Pierce.cs
Spells/Skill Masteries/PlayingTheOdds.cs
Spells/Skill Masteries/Rampage.cs
Spells/Skill Masteries/Rejuvinate.cs
Spells/Skill Masteries/Shadow.cs
Spells/Skill Masteries/ShieldBash.cs
Spells/Skill Masteries/Stagger.cs
Spells/Skill Masteries/SummonReaper.cs
Spells/Skill Masteries/Thrust.cs
Spells/Skill Masteries/Tolerance.cs
Spells/Skill Masteries/Toughness.cs
Spells/Skill Masteries/Warcry.cs
Spells/Skill Masteries/Whispering.cs
Spells/Skill Masteries/WhiteTigerForm.cs
```

### Skill Masteries � files ModernUO lacks that reference it � 14 files
```
Abilities/SAPropEffects.cs
Gumps/TitlesMenu.cs
Items/Equipment/Spellbooks/BookOfMasteries.cs
Quests/Bard Mastery Quests/SirBerran.cs
Quests/Bard Mastery Quests/SirFelean.cs
Quests/Bard Mastery Quests/SirHareus.cs
Quests/Eodon/Hawkwind/Hawkwind.cs
Quests/Eodon/Hawkwind/TimeForLegendsQuest.cs
Quests/Eodon/MyrmidexThreat/Mobiles/Creatures.cs
Services/Expansions/High Seas/Mobiles/Charybdis.cs
Services/Expansions/High Seas/Mobiles/OsiredonTheScalisEnforcer.cs
Services/Expansions/Time Of Legends/Mobiles/Anchisaur.cs
Services/Expansions/Time Of Legends/Mobiles/EodonTribesman.cs
Services/Peerless/BasePeerless.cs
```

### Skill Masteries � upstream patch targets � 35 files
```
Abilities/BleedAttack.cs
Abilities/InfectiousStrike.cs
Abilities/MortalStrike.cs
Abilities/WeaponAbility.cs
Items/Equipment/Spellbooks/Spellbook.cs
Items/Equipment/Weapons/BaseWeapon.cs
Misc/AOS.cs
Misc/RegenRates.cs
Misc/SkillCheck.cs
Mobiles/AI/Magical AI/MageAI.cs
Mobiles/Bosses/BaseChampion.cs
Mobiles/NPCs/AnimalTrainer.cs
Mobiles/Normal/BaseCreature.cs
Mobiles/PlayerMobile.cs
Services/Party/Party.cs
Skills/DetectHidden.cs
Skills/Discordance.cs
Skills/Peacemaking.cs
Skills/Provocation.cs
Spells/Base/SpecialMove.cs
Spells/Base/SpellHelper.cs
Spells/Bushido/Confidence.cs
Spells/Initializer.cs
Spells/Necromancy/BloodOathSpell.cs
Spells/Necromancy/CorpseSkin.cs
Spells/Necromancy/EvilOmen.cs
Spells/Necromancy/MindRot.cs
Spells/Necromancy/PainSpike.cs
Spells/Necromancy/PoisonStrike.cs
Spells/Necromancy/Strangle.cs
Spells/Ninjitsu/AnimalForm.cs
Spells/Seventh/MassDispel.cs
Spells/Sixth/Dispel.cs
Spells/Spellweaving/ArcaneCircle.cs
Spells/Spellweaving/ArcanistSpell.cs
```

### Vice vs Virtue � cost: its own files � 57 files
```
Services/ViceVsVirtue/CityInfo.cs
Services/ViceVsVirtue/GuildStats.cs
Services/ViceVsVirtue/Gumps/BattleStatsGump.cs
Services/ViceVsVirtue/Gumps/BattleWarningGump.cs
Services/ViceVsVirtue/Gumps/ConfirmSignupGump.cs
Services/ViceVsVirtue/Gumps/ExemptCityGump.cs
Services/ViceVsVirtue/Gumps/GuildLeaderboardGump.cs
Services/ViceVsVirtue/Gumps/LeaderboardGump.cs
Services/ViceVsVirtue/Gumps/RewardGump.cs
Services/ViceVsVirtue/Gumps/VvVBattleStatusGump.cs
Services/ViceVsVirtue/Items/Rewards/Banners/CompassionBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/CovetousBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/DeceitBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/DespiseBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/DestardBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/HonestyBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/HonorBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/HumilityBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/HythlothBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/JusticeBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/PrideBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/SacraficeBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/ShameBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/SpiritualityBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/ValorBanner.cs
Services/ViceVsVirtue/Items/Rewards/Banners/WrongBanner.cs
Services/ViceVsVirtue/Items/Rewards/CannonTurret.cs
Services/ViceVsVirtue/Items/Rewards/EssenceOfCourage.cs
Services/ViceVsVirtue/Items/Rewards/ForgedRoyalPardon.cs
Services/ViceVsVirtue/Items/Rewards/ManaSpike.cs
Services/ViceVsVirtue/Items/Rewards/MorphEarrings.cs
Services/ViceVsVirtue/Items/Rewards/Tiles/CovetousTile.cs
Services/ViceVsVirtue/Items/Rewards/Tiles/DeceitTIle.cs
Services/ViceVsVirtue/Items/Rewards/Tiles/DespiseTile.cs
Services/ViceVsVirtue/Items/Rewards/Tiles/DestardTile.cs
Services/ViceVsVirtue/Items/Rewards/Tiles/HythlothTIle.cs
Services/ViceVsVirtue/Items/Rewards/Tiles/PrideTile.cs
Services/ViceVsVirtue/Items/Rewards/Tiles/ShameTile.cs
Services/ViceVsVirtue/Items/Rewards/Tiles/WrongTile.cs
Services/ViceVsVirtue/Items/Rewards/VvVArms.cs
Services/ViceVsVirtue/Items/Rewards/VvVChests.cs
Services/ViceVsVirtue/Items/Rewards/VvVEpaulettes.cs
Services/ViceVsVirtue/Items/Rewards/VvVHairDye.cs
Services/ViceVsVirtue/Items/Rewards/VvVHats.cs
Services/ViceVsVirtue/Items/Rewards/VvVPotions.cs
Services/ViceVsVirtue/Items/Rewards/VvVRobe.cs
Services/ViceVsVirtue/Items/Rewards/VvVSteeds.cs
Services/ViceVsVirtue/Items/Rewards/VvVTrapKit.cs
Services/ViceVsVirtue/Items/Rewards/VvVTraps.cs
Services/ViceVsVirtue/Items/Rewards/VvVWands.cs
Services/ViceVsVirtue/Items/VvVAltar.cs
Services/ViceVsVirtue/Items/VvVSigil.cs
Services/ViceVsVirtue/Mobiles/SilverTrader.cs
Services/ViceVsVirtue/Mobiles/VvVPriest.cs
Services/ViceVsVirtue/ViceVsVirtueSystem.cs
Services/ViceVsVirtue/VvVBattle.cs
Services/ViceVsVirtue/VvVRewards.cs
```

### Vice vs Virtue � files ModernUO lacks that reference it � 5 files
```
Gumps/FacetGump.cs
Misc/Aggression.cs
Services/Factions/Items/Equipment/CollectionBox.cs
Services/Pet Training/PetTrainingHelper.cs
Services/PointsSystems/PointsSystem.cs
```

### Vice vs Virtue � upstream patch targets � 21 files
```
Accounting/AccountHandler.cs
Gumps/Guilds/New Guild System/GuildInfoGump.cs
Gumps/Guilds/New Guild System/GuildRosterGump.cs
Items/Equipment/Armor/BaseArmor.cs
Items/Equipment/Clothing/BaseClothing.cs
Items/Equipment/Jewelry/BaseJewel.cs
Items/Equipment/Quivers/BaseQuiver.cs
Items/Equipment/Spellbooks/Spellbook.cs
Items/Equipment/Talismans/BaseTalisman.cs
Items/Equipment/Weapons/BaseWeapon.cs
Items/Resource/Bandage.cs
Misc/CharacterCreation.cs
Misc/Notoriety.cs
Mobiles/Normal/BaseCreature.cs
Mobiles/PlayerMobile.cs
Regions/TownRegion.cs
Services/Factions/Core/Faction.cs
Services/Factions/Items/Sigil.cs
Skills/Hiding.cs
Skills/RemoveTrap.cs
Skills/Stealing.cs
```

### City Loyalty � cost: its own files � 28 files
```
Services/City Loyalty System/CityDefinition.cs
Services/City Loyalty System/CityLoyaltyEntry.cs
Services/City Loyalty System/CityLoyaltySystem.cs
Services/City Loyalty System/Election.cs
Services/City Loyalty System/Gumps.cs
Services/City Loyalty System/Items/Addons.cs
Services/City Loyalty System/Items/Banners.cs
Services/City Loyalty System/Items/BoxOfRopes.cs
Services/City Loyalty System/Items/CityMessageBoard.cs
Services/City Loyalty System/Items/CityStone.cs
Services/City Loyalty System/Items/GuardsmansRope.cs
Services/City Loyalty System/Mobiles/CityHerald.cs
Services/City Loyalty System/Mobiles/GuardCaptain.cs
Services/City Loyalty System/Mobiles/Raider.cs
Services/City Loyalty System/Setup.cs
Services/City Loyalty System/Trading/DonationCrate.cs
Services/City Loyalty System/Trading/Items/CityBooks.cs
Services/City Loyalty System/Trading/Items/ExpiredVoucher.cs
Services/City Loyalty System/Trading/Items/ForgedArtwork.cs
Services/City Loyalty System/Trading/Items/LittleBlackBook.cs
Services/City Loyalty System/Trading/Items/MysteriousNote.cs
Services/City Loyalty System/Trading/Items/RewardSign.cs
Services/City Loyalty System/Trading/Items/SlimsShadowVeil.cs
Services/City Loyalty System/Trading/Mobiles/Slim.cs
Services/City Loyalty System/Trading/Mobiles/TradeMinister.cs
Services/City Loyalty System/Trading/TradeCrate.cs
Services/City Loyalty System/Trading/TradeEntry.cs
Services/City Loyalty System/Trading/TradeSystem.cs
```

### City Loyalty � files ModernUO lacks that reference it � 15 files
```
Commands/CreateWorld.cs
Gumps/TitlesMenu.cs
Items/Consumables/EngravingTools.cs
Multis/HouseTeleporterTile.cs
Services/LoyaltySystem/LoyaltyRating.cs
Services/LoyaltySystem/LoyaltyRatingGump.cs
Services/PointsSystems/PlayerMobileProps.cs
Services/PointsSystems/PointsSystem.cs
Services/Seasonal Events/KrampusEncounter/KrampusEncounter.cs
Services/Seasonal Events/RisingTide/MaritimeCargo.cs
Services/Town Cryer/Gumps/CreateCityEntryGump.cs
Services/Town Cryer/Gumps/TownCryerGump.cs
Services/Town Cryer/TownCryerSystem.cs
Services/VeteranRewards/CrystalPortals/CorruptedCrystalPortal.cs
Services/VeteranRewards/CrystalPortals/CrystalPortal.cs
```

### City Loyalty � upstream patch targets � 11 files
```
Items/Addons/SHTeleporter.cs
Items/Functional/PublicMoongate.cs
Items/Internal/Teleporter.cs
Items/Resource/Bandage.cs
Misc/AOS.cs
Mobiles/NPCs/BaseVendor.cs
Mobiles/PlayerMobile.cs
Services/ChampionSystem/ChampionSpawn.cs
Spells/Chivalry/SacredJourney.cs
Spells/Fourth/Recall.cs
Spells/Seventh/GateTravel.cs
```

### Exploring the Deep � cost: its own files � 70 files
```
Services/ExploringTheDeep/Addons/CousteauPerronAddon.cs
Services/ExploringTheDeep/ExploringTheDeepQuestChain.cs
Services/ExploringTheDeep/Generate.cs
Services/ExploringTheDeep/Items/Decorate/CusteauPerronHouseDoor.cs
Services/ExploringTheDeep/Items/Decorate/IceCrystals.cs
Services/ExploringTheDeep/Items/Decorate/MasterThinkerContoller.cs
Services/ExploringTheDeep/Items/QuestItems/AquaGem.cs
Services/ExploringTheDeep/Items/QuestItems/AquaPendant.cs
Services/ExploringTheDeep/Items/QuestItems/BearingAssembly.cs
Services/ExploringTheDeep/Items/QuestItems/BootsOfBallast.cs
Services/ExploringTheDeep/Items/QuestItems/BrokenShipwreckRemains.cs
Services/ExploringTheDeep/Items/QuestItems/CanvassRobe.cs
Services/ExploringTheDeep/Items/QuestItems/FlyWheel.cs
Services/ExploringTheDeep/Items/QuestItems/IceWyrmScale.cs
Services/ExploringTheDeep/Items/QuestItems/LockerKey.cs
Services/ExploringTheDeep/Items/QuestItems/MercutiosCutlass.cs
Services/ExploringTheDeep/Items/QuestItems/NictitatingLens.cs
Services/ExploringTheDeep/Items/QuestItems/OrcishSchematics.cs
Services/ExploringTheDeep/Items/QuestItems/PowerCore.cs
Services/ExploringTheDeep/Items/QuestItems/SalvagerSuitPlans.cs
Services/ExploringTheDeep/Items/QuestItems/SorcerersRegs.cs
Services/ExploringTheDeep/Items/QuestItems/StorageLocker.cs
Services/ExploringTheDeep/Items/QuestItems/UnknownShipwreck.cs
Services/ExploringTheDeep/Items/QuestItems/WillemHartesHat.cs
Services/ExploringTheDeep/Items/QuestItems/WireSpool.cs
Services/ExploringTheDeep/Items/Scroll/CalculationsScroll.cs
Services/ExploringTheDeep/Items/Scroll/CaptainsLogScroll.cs
Services/ExploringTheDeep/Items/Scroll/CousteauPerronScroll.cs
Services/ExploringTheDeep/Items/Scroll/CusteauPerronNote.cs
Services/ExploringTheDeep/Items/Scroll/EliseTrentScroll.cs
Services/ExploringTheDeep/Items/Scroll/JosefSkimmonsScroll.cs
Services/ExploringTheDeep/Items/Scroll/JournalScroll.cs
Services/ExploringTheDeep/Items/Scroll/LedgerScroll.cs
Services/ExploringTheDeep/Items/Scroll/LiamDeFoeScroll.cs
Services/ExploringTheDeep/Items/Scroll/MadelineHarteScroll.cs
Services/ExploringTheDeep/Items/Scroll/MasterThinkerSchematics.cs
Services/ExploringTheDeep/Items/Scroll/SealedLettersScroll.cs
Services/ExploringTheDeep/Items/Scroll/SorcerersScroll.cs
Services/ExploringTheDeep/Items/Scroll/SuspicionsScroll.cs
Services/ExploringTheDeep/Items/Scroll/WillemHarteScroll.cs
Services/ExploringTheDeep/Items/SorcerersPlates.cs
Services/ExploringTheDeep/Items/SorcerersRewardChest.cs
Services/ExploringTheDeep/Items/SpecialSalvageHook.cs
Services/ExploringTheDeep/Items/Teleporter/ShipLadder.cs
Services/ExploringTheDeep/Items/Teleporter/ShipSign.cs
Services/ExploringTheDeep/Items/Teleporter/Whirlpool.cs
Services/ExploringTheDeep/Items/WinchAssembly.cs
Services/ExploringTheDeep/Items/WoodenKeyBarrel.cs
Services/ExploringTheDeep/Mobiles/DiabolicalSeaweed.cs
Services/ExploringTheDeep/Mobiles/Djinn.cs
Services/ExploringTheDeep/Mobiles/IceWyrm.cs
Services/ExploringTheDeep/Mobiles/MercutioTheUnsavory.cs
Services/ExploringTheDeep/Mobiles/ObsidianWyvern.cs
Services/ExploringTheDeep/Mobiles/OrcEngineer.cs
Services/ExploringTheDeep/Mobiles/Paralithode.cs
Services/ExploringTheDeep/Mobiles/RockMite.cs
Services/ExploringTheDeep/Mobiles/SalvageHookMonsters.cs
Services/ExploringTheDeep/Mobiles/SeaSnake.cs
Services/ExploringTheDeep/Mobiles/Shadowlord.cs
Services/ExploringTheDeep/Mobiles/ShipBat.cs
Services/ExploringTheDeep/Mobiles/ShipRat.cs
Services/ExploringTheDeep/Mobiles/TheMasterInstructor.cs
Services/ExploringTheDeep/Questers/ChampHuthwait.cs
Services/ExploringTheDeep/Questers/CusteauPerron.cs
Services/ExploringTheDeep/Questers/GipsyGemologist.cs
Services/ExploringTheDeep/Questers/HeplerPaulson.cs
Services/ExploringTheDeep/Questers/JosefSkimmons.cs
Services/ExploringTheDeep/Questers/MadelineHarte.cs
Services/ExploringTheDeep/Questers/SBHepler.cs
Services/ExploringTheDeep/Regions.cs
```

### Exploring the Deep � files ModernUO lacks that reference it � 2 files
```
Commands/DecorateSA.cs
Services/Pet Training/PetTrainingHelper.cs
```

### Exploring the Deep � upstream patch targets � 1 files
```
Mobiles/PlayerMobile.cs
```

### Vendor Searching � cost: its own files � 4 files
```
Services/Vendor Searching/VendorSearch.cs
Services/Vendor Searching/VendorSearchCriteria.cs
Services/Vendor Searching/VendorSearchGump.cs
Services/Vendor Searching/VendorSearchMap.cs
```

### Vendor Searching � files ModernUO lacks that reference it � 5 files
```
Services/Craft/Core/AlterItem.cs
Services/Expansions/High Seas/Gumps/BountyBoard.cs
Services/Expansions/Time Of Legends/AuctionSafe/AuctionMap.cs
Services/UltimaStore/UltimaStore.cs
Services/XmlSpawner/XmlSpawner Core/XmlUtils/XmlFind.cs
```

### Vendor Searching � upstream patch targets � 5 files
```
Gumps/PlayerVendorGumps.cs
Mobiles/NPCs/BaseVendor.cs
Mobiles/NPCs/PlayerVendor.cs
Mobiles/PlayerMobile.cs
Spells/Fourth/Recall.cs
```

### Instanced Peerless � cost: its own files � 13 files
```
Services/InstancedPeerless/ConfirmExitInstanceGump.cs
Services/InstancedPeerless/ConfirmJoinInstanceGump.cs
Services/InstancedPeerless/InstanceEnterGate.cs
Services/InstancedPeerless/InstanceExitGate.cs
Services/InstancedPeerless/InstanceRegion.cs
Services/InstancedPeerless/Medusa/MedusaPlatform.cs
Services/InstancedPeerless/Medusa/RareSerpentEgg.cs
Services/InstancedPeerless/PeerlessInstance.cs
Services/InstancedPeerless/PeerlessKeyBrazier.cs
Services/InstancedPeerless/PeerlessPlatform.cs
Services/InstancedPeerless/RejoinInstanceGump.cs
Services/InstancedPeerless/StygianDragon/DraconicOrb.cs
Services/InstancedPeerless/StygianDragon/StygianDragonPlatform.cs
```

### Instanced Peerless � files ModernUO lacks that reference it � 2 files
```
Items/Functional/SerpentNest.cs
Mobiles/Normal/FairyDragon.cs
```

### Instanced Peerless � upstream patch targets � 2 files
```
Commands/Decorate.cs
Services/Expansions/MondainsLegacy.cs
```

### TribeType � Mobiles/Normal files using it � 53 files
```
Mobiles/Normal/AncientLich.cs
Mobiles/Normal/BaseCreature.cs
Mobiles/Normal/Bogle.cs
Mobiles/Normal/BoneKnight.cs
Mobiles/Normal/BoneMagi.cs
Mobiles/Normal/Centaur.cs
Mobiles/Normal/EtherealWarrior.cs
Mobiles/Normal/Ghoul.cs
Mobiles/Normal/GrayGoblin.cs
Mobiles/Normal/GrayGoblinKeeper.cs
Mobiles/Normal/GrayGoblinMage.cs
Mobiles/Normal/GreenGoblin.cs
Mobiles/Normal/GreenGoblinAlchemist.cs
Mobiles/Normal/GreenGoblinScout.cs
Mobiles/Normal/Kirin.cs
Mobiles/Normal/Lich.cs
Mobiles/Normal/LichLord.cs
Mobiles/Normal/Mummy.cs
Mobiles/Normal/OphidianArchmage.cs
Mobiles/Normal/OphidianKnight.cs
Mobiles/Normal/OphidianMage.cs
Mobiles/Normal/OphidianMatriarch.cs
Mobiles/Normal/OphidianWarrior.cs
Mobiles/Normal/Orc.cs
Mobiles/Normal/OrcBomber.cs
Mobiles/Normal/OrcBrute.cs
Mobiles/Normal/OrcCaptain.cs
Mobiles/Normal/OrcChopper.cs
Mobiles/Normal/OrcScout.cs
Mobiles/Normal/OrcishLord.cs
Mobiles/Normal/OrcishMage.cs
Mobiles/Normal/Pixie.cs
Mobiles/Normal/RottingCorpse.cs
Mobiles/Normal/Satyr.cs
Mobiles/Normal/Savage.cs
Mobiles/Normal/SavageRider.cs
Mobiles/Normal/SavageShaman.cs
Mobiles/Normal/Shade.cs
Mobiles/Normal/SkeletalDragon.cs
Mobiles/Normal/SkeletalDrake.cs
Mobiles/Normal/SkeletalKnight.cs
Mobiles/Normal/SkeletalMage.cs
Mobiles/Normal/Skeleton.cs
Mobiles/Normal/Spectre.cs
Mobiles/Normal/TerathanAvenger.cs
Mobiles/Normal/TerathanDrone.cs
Mobiles/Normal/TerathanMatriarch.cs
Mobiles/Normal/TerathanWarrior.cs
Mobiles/Normal/Treefellow.cs
Mobiles/Normal/Unicorn.cs
Mobiles/Normal/Wisp.cs
Mobiles/Normal/Wraith.cs
Mobiles/Normal/Zombie.cs
```

### TribeType � of those, the ones ModernUO does not already ship � 9 files
```
Mobiles/Normal/GrayGoblin.cs
Mobiles/Normal/GrayGoblinKeeper.cs
Mobiles/Normal/GrayGoblinMage.cs
Mobiles/Normal/GreenGoblin.cs
Mobiles/Normal/GreenGoblinAlchemist.cs
Mobiles/Normal/GreenGoblinScout.cs
Mobiles/Normal/OrcChopper.cs
Mobiles/Normal/OrcScout.cs
Mobiles/Normal/SkeletalDrake.cs
```

### Re-count of the 89 � Mobiles/Normal files ModernUO lacks that are blocked by something other than Pet Training � 65 files
```
AcidSlug.cs
BaseSABosses.cs
BloodWorm.cs
ChickenLizard.cs
CoconutCrab.cs
CrimsonDrake.cs
CrystalHydra.cs
DespiseCreature.cs
DespiseEvilCreatures.cs
DespiseGoodCreatures.cs
DragonsFlameGrandMage.cs
EnragedEarthElemental.cs
Eowmu.cs
FairyDragon.cs
FireAnt.cs
FireRabbit.cs
FrostDrake.cs
GargishOutcast.cs
GargishRouser.cs
GrayGoblin.cs
GrayGoblinKeeper.cs
GrayGoblinMage.cs
GreaterPoisonElemental.cs
GreenGoblin.cs
GreenGoblinAlchemist.cs
GreenGoblinScout.cs
Gregorio.cs
Gremlin.cs
HighPlainsBoura.cs
HungryCoconutCrab.cs
IronBeetle.cs
Kepetch.cs
KepetchAmbusher.cs
Lasher.cs
LeatherWolf.cs
LowlandBoura.cs
Macaw.cs
MaddeningHorror.cs
Mimic.cs
MinionOfScelestus.cs
Niporailem.cs
OrcChopper.cs
OrcScout.cs
PlatinumDrake.cs
PutridUndeadGargoyle.cs
Raptor.cs
Rotworm.cs
RuddyBoura.cs
SentinelSpider.cs
SerpentsFangHighExecutioner.cs
SkeletalCat.cs
SkeletalDrake.cs
Slith.cs
StoneMonster.cs
StoneSlith.cs
TanglingRoots.cs
TheButcher.cs
TigersClawMaster.cs
ToxicSlith.cs
TreefellowGuardian.cs
Triton.cs
VoidManesfistation.cs
WildTiger.cs
Windrunner.cs
WolfSpider.cs
```
