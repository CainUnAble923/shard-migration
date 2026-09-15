# When to build a missing subsystem instead of declining content

**Written 2026-09-06, replacing a rule that was costing us content.**

## The rule that was wrong

`AGENTS.md` said: "Decline anything resting on a missing subsystem. ModernUO ships zero
files for Skill Masteries, Shadowguard, Myrmidex Invasion, Vendor Searching, Instanced
Peerless. Content needing those is a subsystem build, not a port. Say so and stop."

That was written before we had any throughput data, as a guard against a project that had
not yet ported a single file. It has since been applied to things it should not have been,
because **it measures the wrong quantity**. "ModernUO ships zero files for X" says nothing
about what X costs or what it is worth.

## The rule that replaces it

Measure the **unblock ratio**: files freed per file built.

| Subsystem | Cost to build | Files it unblocks | Ratio |
|---|---|---|---|
| Armour set bonus | **1 file, 387 lines**, plus 3 small patches | **114** (see correction below) | ~114:1 |
| Fountain of Fortune cluster | **38 files, 2,292 lines**, 1 patch (measured by S2) | its own reward loop, `LuckyCoin`'s interaction across 12 creatures, and 35 Imbuing ingredient leaf items | low ratio, and the cost was 2.5x my estimate |
| Pet Training, full | 11 files, 8,664 lines | 103 creatures | ~9:1 |
| Pet Training, `SpecialAbility.cs` only | 2,688 lines | 67 of those creatures | unmeasured, likely much better |
| Mondain's Legacy quest framework | 21 files, 5,625 lines | the Eodon quest line, plus an unknown number of others | **unknown, and that unknown decides it** |

> **Correction, 2026-09-07, after S1 built it.** The 187 above was mine and it was wrong: a union
> of `SetItem`, `SetAttributes` and `AbsorptionAttributes`, which are **not one subsystem**.
> Re-counted: **131 files actually declare `SetID`**, of which **114 are unblocked by the armour
> set system alone**. 17 also need `SAAbsorptionAttributes`, the Stygian Abyss damage-eater system,
> which ModernUO also lacks and S1 did not build; 43 more use absorption without being set items.
> The decision was right and 114:1 is still the best ratio in the backlog. The number I argued it
> with was inflated by about 64%, in the same document that tells everyone else to measure
> properly. Raised by S1 as Q-017.
>
> **Four for four**: every keyword-derived count in this repo has been wrong. A keyword hit is a
> candidate, not a result. Publish the file list beside the count, including in this table.

> **Second correction, 2026-09-07, after S2 built it.** My "roughly 900 lines" was wrong in both
> directions. The *core* cluster is 465 lines across 4 files. The *whole* thing is 2,292 across 38,
> because `GemologistsSatchel` reads `Imbuing.IngredTypes`, a 42-entry table, and 35 of the 42 were
> missing from ModernUO. All 35 turned out to be dependency-free leaf items, so they were ported to
> the leaf per the `LuckyCoin` precedent and the ingredient table is complete and verbatim.
>
> **The lesson is not "estimate better", it is that a cheap-looking leaf can hide a table.** A
> dependency walk that stops at the file you are reading misses a `Type[]` one level down. Walk the
> arrays too.

A subsystem that frees one thing is bad value. A subsystem that frees 187 is the best value
in the backlog. The old rule treated those identically.

**Also measure the useful subset.** A creature needs ServUO's *ability definitions*; it does
not need the pet-training gate, gumps and profiles that players interact with. Costing the
whole system when content only needs part of it inflates every estimate.

## Two declines reversed

1. **The armour set-bonus system, and with it the eight Aloron pieces** (CC3) and a large
   share of the artifacts and equipment backlog.
2. **The Fountain of Fortune cluster**, and with it `LuckyCoin`'s `OnDoubleClick` (Q-010).
   The decline rested on a wrong belief that `EnchantedEssence` and `RelicFragment` drag in
   Imbuing. They do not; both are leaf items in `SAQuestItems.cs`, and Imbuing merely
   consumes them.

## The cost that is real, stated honestly

Every subsystem we build is code **ModernUO will not maintain for us**. Each future bump of
the pinned commit is our problem to reconcile, forever. That is the genuine argument against
building one, and it is the only one.

**It is not a fidelity argument, and an earlier version of this reasoning wrongly framed it
as one.** A faithfully rebuilt OSI subsystem is documented by UOGuide exactly like any other
OSI content, so `docs/fidelity-principle.md` *favours* building it. Building it wrong, or
building an approximation, is the fidelity risk. Building it faithfully is not.

So the test for a subsystem is three questions, in order:

1. **What is the unblock ratio**, and what is the ratio for the smallest useful subset?
2. **Can it live in the layering pattern** as additive `.cs` plus targeted patches, or does it
   require forking a ModernUO base class beyond what a patch can express?
3. **What breaks on the next pinned-commit bump**, and would we notice? A subsystem that
   patches four base classes is a bigger reconciliation burden than one that adds files.

A subsystem that answers those well gets built. One that does not gets declined **with its
ratio recorded**, so the decision can be revisited when the surrounding content changes.

## What still stands

Declining is still right when the ratio is poor, when the subsystem would mean two engines
coexisting for the same job, or when the content it frees is not content we want. Nothing
here says port everything regardless of cost. It says cost it properly first.

## Patching the ModernUO core project

S1 needed the first patch outside `Projects/UOContent`, into `Projects/Server/Mobiles/Mobile.cs`,
because `ComputeResistances()` lives in the core and that is where ServUO applies set resistances.

**Allowed, on this bar: no `UOContent` hook exists, and the alternative is copied upstream logic.**
Core patches are riskier on a pinned-commit bump than `UOContent` ones, so they are rare, they are
argued in `notes/` before being written, and they are the **first** thing re-verified when
`MODERNUO_COMMIT` moves.

**The standing rule underneath it generalises: a failing patch beats copied upstream logic.**
`apply-patches.sh` is a verification gate, and a copied method body routes around it. Sixty lines of
upstream logic living in our tree drifts silently on a bump; a patch that no longer applies stops
the build and names itself. Take the loud failure every time.

**And prefer a patch over a mechanism that does not persist.** S1 rejected expressing set bonuses as
`ResistanceMod`s, which was arithmetically identical and needed no patch, because ModernUO does not
appear to serialize them: the bonus would have vanished on save and reload until the player
re-equipped. Zero patches is not worth a silent fidelity bug.

## A ported subsystem needs a test; ported content does not

Ported content is checked by the compiler and by reading the ServUO source. A ported subsystem is
not. Nothing in a build would catch a bump that leaves every patch applying while the behaviour
quietly stops reaching the player. Every subsystem built from here ships with a committed
regression test, once S4 builds the route for one.

## Decisions of 2026-09-07

**Pet Training: wait, do not build.** Chase's call, and the reason is timing rather than value.
The three ability groups (B2-B4 in `docs/gap-register.md`) would close five of the ten
player-visible gaps for ~4,700 lines and 88 files unblocked, which is a defensible ratio. But
they patch six or seven upstream files including `AOS.Damage`, and `docs/upstream-watch.md`
records that ModernUO is **actively refactoring `BaseCreature` right now**, with `SpeedClass` an
open behaviour change in PR #2592. Patching heavily into a class being rewritten this week is the
worst available timing.

**Revisit when** the delta-saves project and the `BaseCreature` conversion have landed and
settled upstream. Nothing expires; the gaps stay logged in section A of the register meanwhile.

**This is a new kind of reason on this project and worth keeping:** a subsystem can pass the
ratio test and still be wrong to build *this week*. Add upstream churn to the three questions
above as a timing check, not a fourth gate.

**Upstream contributions: not now.** The `SetPassword` defect report and the offer of the armour
set-bonus system both stay available and neither expires. Recorded in section E of the register
so they are not forgotten rather than declined.

**2026-09-08, the carrier family: BUILD.** The mirror image of the Pet Training decision, and
worth keeping the pair together because the contrast is the lesson.

Pet Training was declined **on timing**: good ratio, but six or seven upstream patches while
upstream rewrites `BaseCreature`. The carriers are ~1,000 lines with **zero patches and zero
migrations**, so a pinned-commit bump cannot touch them, and the objection that stopped Pet
Training simply does not exist.

**Ratio was never the deciding factor in either case.** What decided both was what a bump would
have to reconcile. Add that to the three questions above as the first thing to check on a
subsystem that otherwise passes: **how much of it is patch, and how much is additive.**

**2026-09-15, a sixth carrier for ranged set weapons: NO, and this completes the set of three.**
`Swiftflight` is the only ranged type in all of ServUO carrying set or absorption state, and zero
ranged types use `ReforgedSuffix`, so a `BaseSetRanged` would free one file forever. It was also
unnecessary: the aggregation patch dispatches on `obj is ISetItem` and `SetHelper` tests
`is BaseWeapon` first, which a `Bow` satisfies. Ported as `Swiftflight : Bow, ISetItem` instead.

**Put the three decisions together, because the contrast is the whole method.** Pet Training:
good ratio, declined on **timing** (six or seven patches while upstream rewrites `BaseCreature`).
The carrier family: modest ratio, built because **zero patches** meant a bump could not touch it.
A ranged carrier: zero patches too, and declined anyway because **the mechanism already existed**
one level up, at the interface. So the questions, in order: what must a bump reconcile, is there
already a seam that does this, and only then how many files does it free.

**And a sixth abstract base is a sixth place to repeat a mistake.** Batch 4 had to correct
`BaseSetWeapon` because S10 missed `BaseMeleeWeapon.AbsorbDamage`. That cost is invisible when
you count lines and real every time a carrier changes.

The alternative here was free and was rejected on **fidelity**: deleting the `ReforgedSuffix` line
costs nothing and ships 136 items with wrong names, which is the exact failure
`docs/fidelity-principle.md` exists to prevent, arriving all at once.

**Outcome, same day: the prediction that mattered held, the size estimate did not.** Zero patches
and zero migrations, exactly as argued — `server/patches` is 15 files before and after. The line
count was **1,426 against ~1,000**, because a ModernUO shield is a `BaseArmor` but not a
`BaseSetArmor`, so the shield carrier is a full copy rather than a thin one. **That is the right
way round for this test to fail**: the question the policy asks is what a bump has to reconcile,
and it answered that correctly while being 40% off on volume.

