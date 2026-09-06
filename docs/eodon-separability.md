# Eodon: what is actually there, and a correction to two earlier numbers

> **CORRECTED A THIRD TIME, 2026-09-06, by CC3, which ported it.**
>
> **The conclusion holds. The file table below does not.** Eodon does separate from Myrmidex
> and Shadowguard, and it is smaller than any earlier figure. That headline claim survived
> verification intact. What did not survive is the specific list.
>
> Verified by porting: **17 portable files, 12 declined.** Not 22.
>
> 1. **`MoonstonePowerGenerator.cs` is Myrmidex Invasion content.** It lives in
>    `Services/Expansions/Time Of Legends/Myrmidex Invasion/`, spawns `Zipactriotl` and
>    `IgnisFatalis`, and subclasses `DamageableItem`. It reached the list because "moonstone"
>    matched a keyword.
> 2. **`Quests/Eodon` is not 3 files.** `Valley of One Quest/` is 8 files and 3,870 lines. The
>    three named here reference types defined in the five that were left out, so they cannot
>    compile alone, and the whole thing rests on ServUO's Mondain's Legacy quest framework
>    (6,269 lines) while ModernUO ships a different quest engine. That is a subsystem port.
> 3. **The eight Aloron pieces rest on the armour set-bonus subsystem**, which ModernUO ships
>    zero files for, plus the TigerPelt set, a further eight unlisted files.
>
> **Read this document as: the separability finding is sound, the file table is unverified.**
> Errors 1 and 2 are exactly the failure mode the methodology note at the bottom describes,
> committed twice in the table directly above it. Rule 3 of that note, prefer directory
> structure over keywords, would have caught error 1 on its own: the directory is named
> `Myrmidex Invasion`.
>
> The verified list, the evidence for each decline, and eight further Eodon creatures this
> document omits (`Gallusaurus`, `Anchisaur`, `DragonTurtle`, `DragonTurtleHatchling`,
> `GreaterPhoenix`, `DesertScorpion`, `Infernus`, `BritannianInfantry`) are in
> `notes/cc3-eodon.md`.

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
