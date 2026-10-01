# Architecture verdict: the reachability instrument (2026-10-01)

Architecture chat, first job from `passdown-architecture-2026-10-01.md`. Read only: `reachability-audit.md`,
`cc-P12-audit-correction.md`, `craft-registrations.md`, `cc-P7-pinned-waiting-drops.md` 2.7,
`backlog-remeasure-2026-09-28.md` 6, `tools/content_index.py`, and greps of `D:\UO\ModernUO-pinned`. Nothing built, run
or committed. No D or Q number taken. For the overseer to schedule.

## 0. The answer

**Do not build a precondition-following instrument.** Make the written A-D preflight the standard (cc-P12's standing
rule), repair the existing `reach` so a re-run tells the truth, and spec a narrow `--preflight` flag report that is
built only if three or more gates are about to be briefed together. It is validated against the nine built gates
before anyone trusts it.

One correction to the pass-down first: **`reach` already exists.** P2's proposal (backlog-remeasure 6.1) was built by
the audit (`content_index.py:544`, class `Reach`; `print_reach` at `:1046`; audit section 2). The open question is
only whether to teach it second hops.

## 1. Why not a second-hop closure

1. **Condition B is a property of a world, not of code.** The carrier that failed (Ilhenir) is a champion boss. Pinned
   places no champion spawn anywhere in source or data: no `new ChampionSpawn(` under `Projects`, and no champion
   entries in `Distribution/Data` (grep, 2026-10-01). A champion spawn exists only if staff placed one in a save. The
   same is true of every GM `[add` (audit 6, row 1) and of the 282 reached types that depend on which generators a
   world has had (audit 6, row 2). And the world that matters is not the live save: the test shard's world becomes
   live and a wipe is coming. No static tool can answer B until that world's manifest exists.
2. **Condition A is only half mechanical.** A recipe is an int. ToL hands out recipes 560-584 by a computed roll on
   Eodon kills (`TimeOfLegends.cs:98-133`, cc-P12 4.3). A tool can find `AddRecipe` on an entry; it cannot reliably
   say whether that id can drop.
3. **Condition C would not be caught at all.** Gate 3, the biggest miss (24 to 0), was "pinned has no such list", a
   hand-grouping error (cc-P12 4.1). Only reading pinned's chest finds it.
4. **The volume does not pay for it.** Of the 18 unbuilt gates, 20 is declined (Q-064) and most of 21-27 sit under
   "Not worth it" (audit 3). Realistic briefs: 8, 10, 11, 15, perhaps 14 and 16-19. At about an hour of reading each
   (cc-P12 5), that is less than building and validating a closure, and content remediation is not scheduled: the
   base game and F-12 come first.

## 2. A qualifier the pass-down needs: 340 is rules-exact, not exact

The 340 is exact against the tool's rules and confirmed 219 of 219 with no false orphans. But the rules have the same
one-hop blindness on **our** side, and known leaks run both ways:

- **Reach too generous:** our own `AddCraft` counts as reach whatever its recipe or resources
  (`craft-registrations` 4.2); a method nothing calls counts as live (`Putrefaction` through `PackResources`, 4.1);
  282 types assume generators were run.
- **Reach too stingy:** anything placed in a save (audit 6), 40 dynamic lookups in pinned not read, P7's two
  uncommented drops (section 3 below).

Both are small against 60 percent, so **"port no more content except decoration" stands.** The practical consequence:
a future registration of a recipe-gated or resource-gated entry would read as reached. craft-registrations avoided
that by hand. **Make it the rule: any new craft, drop or reward registration cites the source of its recipe, resources
and carrier in its notes, or it is not counted as delivered.**

## 3. Repair `reach` before anyone re-runs it (small, notes and tools only)

| Fault | Effect | Fix |
|---|---|---|
| Uncomment patches read as context (`content_index.py:621`; cc-P7 2.7) | gate 9 reads as 0 delivered on any re-run | **Index pinned with our patches applied** to a scratch copy, the way `docker/uo/apply-patches.sh` applies them, instead of pinned plus added lines. One code path, and the instrument then sees the same pinned the build does, which matters once F-12 adds about 30 patches |
| First resource in `AddCraft` read as a product (craft-registrations 4.1.1) | `--sources` invents sources (`CrystalShards`) | treat every `typeof` after the first in an `AddCraft` argument list as a read |
| Liveness per type, not per method (`Putrefaction`) | one false reach known | do not fix; record in audit 6 as a known over-reach |

Each with a fact watched red, per the tool's own convention. This task never opens `D:\ShatteredLegacy` (it reads an
export through `CONTENT_INDEX_OURS`), so it can run beside any builder.

## 4. The preflight spec, if the trigger is met

Trigger: three or more gates queued for briefing at once. Until then, A-D in writing per gate.

`content_index.py reach --preflight <gate>` emits, per ServUO source entry for each type in the gate, flags and not a
verdict:

| Flag | Level | Mechanical rule |
|---|---|---|
| D-absent | **fails** | another `typeof` or `new` in the same entry (same `AddCraft`, list row or statement) names a type in neither tree |
| D-twin | **fails** | the type has a twin pinned already reaches (existing `--twins`) |
| A-recipe | **fails** unless a source is cited | the entry has an `AddRecipe`; report whether any literal `RecipeScroll(<id>)` or known range covers it |
| A-resource | **fails** if unreached, **needs evidence** if pinned | each `AddRes` type's standing (ours reached, ours unreached, pinned, absent) |
| B-carrier | **needs world evidence** | the site's owner is a creature, champion, peerless or placed container; report any spawn-data row found |
| C-slot | **not checked** | always printed, so nobody reads silence as a pass |

**How we would know it is right.** The nine built gates are a labeled set: 135 files predicted, 70 delivered, 65 not,
each with its cause in a note. Pass criteria on the HEAD of 2026-09-29 export:

1. None of the 70 delivered files carries a **fails** flag.
2. Each of the 65 misses carries a **fails** or **needs world evidence** flag naming its recorded cause, except misses
   whose only cause is C (gate 3's list gap), which must show as **not checked**.
3. Each flag rule watched red: disable it and see the backtest break.
4. Then one held-out gate (8 or 10): write the preflight's prediction into notes before the build, compare after.

Fitting to the only labeled data is a real risk, which is why item 4 is the test that counts.

## 5. For the overseer

- Schedule the section 3 repair when convenient. It needs a cc-P number from you.
- Add the section 2 rule to whatever template briefs a content gate.
- No action on section 4 until the trigger.
