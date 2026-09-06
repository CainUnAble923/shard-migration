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
| Armour set bonus | **1 file, 387 lines**, plus base-class plumbing | **187** | ~187:1 |
| Fountain of Fortune cluster | ~5-8 files, ~900 lines | its own reward loop, and `LuckyCoin`'s interaction | low, but so is the cost |
| Pet Training, full | 11 files, 8,664 lines | 103 creatures | ~9:1 |
| Pet Training, `SpecialAbility.cs` only | 2,688 lines | 67 of those creatures | unmeasured, likely much better |
| Mondain's Legacy quest framework | 21 files, 5,625 lines | the Eodon quest line, plus an unknown number of others | **unknown, and that unknown decides it** |

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
