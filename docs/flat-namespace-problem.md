# Structured content cannot be ported into a flat directory

**Found 2026-09-06 while prepping CC4. Needs a decision before Revamped Dungeons starts.**

## The problem

`server/customizations/` is a **flat** directory, and `apply-patches.sh` installs from it with:

```
find "$CUSTOMIZATIONS" -maxdepth 1 -type f -name '*.cs' ... -exec cp '{}' 'Projects/UOContent/Misc/' \;
```

Flat source, flat destination, `-maxdepth 1`. That has been fine because every one of our 111
customizations has a unique name.

ServUO's structured content does not. In `Services/Revamped Dungeons` alone:

| Basename | Appears in |
|---|---|
| `Generate.cs` | Shame, Wrong, Blackthorn, Covetous |
| `Region.cs` | Wrong, Despise, Blackthorn, Covetous |
| `Creatures.cs` | Shame/Mobiles, Blackthorn/InvasionSpawner |

**32 duplicate basenames covering 137 of the 255 files.** Flattening them means each `cp`
silently overwrites the last. Four dungeons would end up sharing one `Generate.cs`, the build
might even succeed, and three dungeons would quietly not generate.

## Scope

| Area | New files | Duplicate basenames | Files affected |
|---|---|---|---|
| Services/Revamped Dungeons | 255 | 32 | **137** |
| Services/Expansions (HS + TOL) | 176 | 1 | 2 |
| Mobiles/Normal | 138 | 0 | 0 |
| Items/Artifacts | 325 | 0 | 0 |

Flat content (creatures, artifacts) is unaffected. **CC3 (Eodon) and CC6 (creatures) are safe
as planned.** The problem is specific to structured, multi-directory content, which is
everything from CC4 onward.

## Options

**1. Preserve subdirectories (recommended).** Let `server/customizations/` contain
subdirectories, and have `apply-patches.sh` mirror the tree into
`Projects/UOContent/` rather than flattening into `Misc/`. Matches how both ServUO and
ModernUO actually organise content, and keeps ported files recognisable against their source.
Costs one change to the installer and a rule that top-level `.cs` still means "additive into
`Misc/`" so existing behaviour is preserved.

**2. Rename on port.** `ShameGenerate.cs`, `WrongGenerate.cs`, and so on. No installer change,
but it obscures provenance, breaks any internal partial-class or file-name assumptions, and
makes diffing a ported file against its ServUO original harder forever. Not recommended.

**3. One flat folder per dungeon.** A middle path, but it still needs the installer to recurse,
so it has option 1's cost without its tidiness.

## Recommendation

Option 1, and **do it as part of F2** rather than later. Claude Code is rewriting
`apply-patches.sh` right now to make it a verification gate. Adding recursive install while
that file is already open is far cheaper than reopening it during CC4, and the strictness work
it is doing (checking that a destination exists before copying) is exactly the machinery that
makes a recursive install safe.

If it lands later, the risk is that someone ports a dungeon first, gets a green build, and
discovers three dungeons missing at runtime.
