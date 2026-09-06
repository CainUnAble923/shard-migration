# Eodon: what is actually there, and a correction to two earlier numbers

**Corrected 2026-09-06, twice. Read the methodology note at the bottom before trusting any
keyword-derived count in this repo, including this one.**

## The answer

Eodon separates from Myrmidex and Shadowguard, and the genuinely new Eodon-specific content
is **smaller and easier than any figure I gave earlier**.

The core set, ServUO files that are about Eodon, are absent from stock ModernUO, and touch no
missing subsystem:

| Area | Files | What |
|---|---|---|
| `Services/Expansions` | 6 | Allosaurus, Archaeosaurus, Dimetrosaur, Najasaurus, Saurosaurus, SilverbackGorilla |
| `Items/Artifacts` | 10 | the eight Aloron armour pieces, RaptorClaw, TOL decoration artifacts |
| `Quests/Eodon` | 3 | Creatures.cs, Items.cs, TigerCubEnclosure.cs (2,058 lines, the quest line) |
| `Mobiles/Normal` | 1 | Raptor.cs |
| `Items/Resource` | 1 | RaptorTeeth.cs |
| `Services/Expansions` | 1 | MoonstonePowerGenerator.cs |

**Roughly 22 files, about 4,000 lines** of core Eodon content. That is a weekend, not a project.

## The two corrections

**First error: "52 creature files."** My Eodon matcher included the keyword `Tribe`, which
matched every orc tribe reference in ServUO. **43 of those 52 were generic Britannia mobs**
that ModernUO already ships: Orc, Skeleton, Zombie, Lich, Pixie, Unicorn, Terathan, Ophidian.
Not Eodon content at all.

**Second error: "41 files, 16,625 lines."** The tightened query still swept in large shared
systems that merely mention a raptor or a moonstone: `Imbuing.cs` (2,078 lines),
`PetTrainingHelper.cs` (1,779), `UnloadMaps.cs` (1,785), `TreasureMapInfo.cs` (993),
`CleanUpBritanniaData.cs` (980), `DaviesLocker.cs` (859). Those are not Eodon content either;
they are systems with an Eodon-shaped mention inside them.

The earlier "83% dependent on Myrmidex" figure was also wrong in the other direction: it
measured the Myrmidex Invasion folder, not Eodon, and made the Valley look gated when it is not.

## What this means for the backlog

Eodon gets *cheaper*, not harder. Three of the corrections pointed the same way.

- **CC3 should be the ~22 core files**, not 52. Expect it to be quick.
- The Valley works with no Myrmidex Invasion and no Shadowguard.
- The dinosaurs are the visible payoff and there are only six of them.

## Methodology note, and it applies to this repo generally

Keyword matching over a source tree **systematically over-counts**. A file that mentions a
thing is not a file about that thing. I have now made this error three times in one day: a
name-collision check run against the build tree rather than pristine ModernUO, and these two
Eodon counts.

**Rules going forward, for any agent producing numbers here:**

1. A keyword hit is a candidate, not a result. Read the file list before quoting a total.
2. Always exclude what the target codebase already has, and check what you are excluding
   against is the pristine tree, not a build output containing copies of your own work.
3. Prefer directory structure and explicit gates (`Core.HS`, `Expansion.TOL`) over keywords.
   They are narrower and they mean something.
4. Publish the file list alongside the count so the count is checkable.
5. Dependency percentages measure coupling to *missing subsystems*, nothing else. They do not
   measure porting difficulty.

The expansion coverage figures in `README.md` carry the same caveat and say so.
