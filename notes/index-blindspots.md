# Index blind spots (D20): the content index fixed, kept, and the artifacts row re-measured

**Measurement and tooling only. Nothing was ported. No file in `server/customizations`, `docs/`, either source
tree or the build changed.** The build compiles nothing this task touched, so no build was run and nothing was
tagged.

---

## Part A: the kilt recipes are not live. No defect, nothing jumps the queue

**Pinned ModernUO's tailoring does not carry recipes 562 to 564.** `ModernUO-pinned/.../Engines/Craft/DefTailoring.cs`
registers exactly five recipes, `AddRecipe(index, 501)` to `505` (the quivers, `:218-258`). The numbers 562 to 566
appear nowhere in pinned as a recipe, and nowhere in `server/customizations` or `server/patches`.

The only way a player learns a recipe is `RecipeScroll`, whose `Recipe` getter is `Recipe.Recipes.TryGetValue(_recipeID,
...)` (`Items/Skill Items/Misc/RecipeScroll.cs:28`). Scrolls reach players through `BaseCraftmansSatchel.AddRecipe`,
which takes its ID from `system.RandomRecipe()`, so only registered recipes can drop. **A tailor cannot learn a kilt
recipe here.** The one path to a 562 scroll is a GM typing `[add RecipeScroll 562`. That scroll shows no recipe name
and does nothing on double-click (`RecipeScroll.cs:64`, `r == null` returns). Staff-only and inert.

So `GuildedKilt`, `CheckeredKilt` and `FancyKilt` are ordinary absent content, and they appear in the corrected
row below with everything else. The same holds for their neighbours `JesterShoes` (560), `ChefsToque` (561,
in `Hats.cs`, a co-port candidate rather than a hidden type), `FloweredDress` (565) and `EveningGown` (566). That raises a real question about porting recipe-gated items at all:
**Q-064**.

---

## Part B: what changed in the index, and where it lives

### It is a tool now: `tools/content_index.py`, with `tools/test_content_index.py`

**The brief's premise needed one correction:** the two scripts were not in scratch. They were already in
`tools/index_blindspots/`, committed in `8b04d8f`. More importantly, **there was no index to fold them into.** S3
and S9 each rebuilt the index from a written method and threw the script away (S9 §11: "The scripts are throwaway,
as S3's were"). The two scripts measured the blind spots from outside. They could not produce a corrected row.

So the fix is the index itself, written from S9 §2 and §11 and kept:

- **`--legacy` is S9's method,** and it has to reproduce S9 before anything else is trusted. Against
  `server/customizations` as it stood when S9 ran (ShatteredLegacy `b21bcd9`, 198 `.cs`, S9's own figure),
  **legacy mode puts all 1,022 artifacts-row files in the same bucket S9 published**: 567 / 320 / 81 / 10 / 44
  exactly. That is the regression, and it is a test.
- **Fixed mode (the default)** adds the two D20 fixes and one label fix:
  1. **Alias strings are declarations.** A name inside `[TypeAlias("Server.Items.X", ...)]` in pinned or ours is
     indexed as a type, because `AssemblyHandler` resolves it in the same lookup (`AssemblyHandler.cs:251-263`). A
     ServUO file whose primary type is only an alias is now discarded, labelled `aliased`, with the pinned file named.
  2. **Every secondary type of a discarded file is reported** (`hidden`), each with a mechanical class. Nothing is
     summed as backlog.
  3. **`upstream` is split three ways.** Legacy `upstream` meant any name whose only ServUO owner is a discarded
     file. Fixed mode separates **`upstream`** (a *member* of a class ModernUO ships: a patch or carrier), **`extract`**
     (a *type* that lives inside a discarded file: ordinary content work) and **`unknown`** (nothing in ServUO
     Scripts declares it: read the file). This third fix is the kilts' mislabel. `GargishClothWingArmor` and
     `InstrumentedAddonComponent` are types, and S9's label sent them to "needs a patch".
- `tools/index_blindspots/` is **removed**. Everything it measured is a subcommand now (`filter` for the aliased
  files, `hidden` for the secondary types), and git keeps the originals.

**Why `tools/`, and one file:** `tools/progress.py` and `expansion_coverage.py` are the project's other kept
instruments and live there. The index has one job, and the tests need the same classes the CLI uses.

### The tests, and proof they test something

`python -m unittest tools/test_content_index.py`: 8 facts, about 8 s, read-only. The test exports the S9-era tree
itself with `git archive`, so it does not depend on anyone's scratch.

| Fact | What it pins |
|---|---|
| legacy step 1, pinned only, = 3,133 of 6,144 | the S3/S9 filter (see "3,134" below) |
| legacy artifacts row = S9's appendix, file by file | S9 reproduces |
| `GargishClothKilt` resolves when fixed, not when legacy | **the failure that produced the kilts** |
| `BestialKilt.cs` is not missing `GargishClothKilt` when fixed | same, at the file level |
| `GargishLeatherKilt.cs` is discarded as `aliased` | the 19 phantom candidates |
| `GuildedKilt` (in `OuterLegs.cs`) and `GargishKiltOfMining` (in `GlovesOfMining.cs`) are reported as items | **a known unreferenced secondary type is found** |
| `MaleGargishClothKilt` is flagged as sharing a graphic with pinned's `GargishClothKiltType1` | an equivalent is not reported as absent |
| `GargishClothWingArmor` is `extract` fixed and `upstream` legacy; `TempDamageAbsorb` stays `upstream` | the label fix, both ways |

**Each fix was reverted in memory and the suite rerun.** Aliases off: 3 failures. Extract folded back into
upstream: 1 failure. Hidden report emptied: 1 failure and 1 error. None of the three fixes can regress silently.

### Three defects in my own index, found by the reproduction, fixed before any number below

1. **The member regex consumed its delimiter.** The `;` ending one declaration was eaten, so the next member was
   invisible. `HarvestWait`, `BerserkHue` and `MaxLuckBonus` were reported as unknown names in their own files.
   Fixed with lookarounds.
2. **`GenericWriter` and `TimerCallback` were missing from CONVERT.** S9 §2 prints `GenericReader` and
   `TimerStateCallback`, and these are the same conversions. S9's appendix buckets their files as if applied, so
   S9 applied them without listing them.
3. **I had indexed enum members; S9 did not.** It prints `unknown: Good` and `unknown: Undead`. My version filed
   `Brittle` under `VendorSearch.cs`'s unrelated `Misc` enum. Removed, to keep one variable at a time. See "Still
   cannot see".

### Two figures the brief and the last note carried, now counted

- **"3,134 of 6,144" is a pinned-only figure.** S9 §2 describes the filter as "ModernUO (or our own tree)". Against
  the S9-era tree that definition discards **3,203**. Pinned alone gives **3,133**, which is S3's figure less the one
  file last task already recorded. **S9's rows did include our tree**: that is the only way the artifacts row gets
  567. So S9 ran its whole-tree regression and its rows on different definitions and printed one sentence for both.
  The tests pin each where it belongs.
- **The 482 from last task is 509 under this tool** (495 against the S9-era tree). This is a definition change, not
  drift. `secondary.py` discarded a file only when *pinned* declared its primary. This tool follows S9's row
  definition, which also discards on our tree and on aliases, so more files are discarded and more secondary types
  surface. **Neither figure is a backlog.** Whole-tree classification of the 509:

| Class | Types | Meaning |
|---|---|---|
| quest | 150 | ML quest classes declared inside the quest-giver NPC's file. Content, but quest-shaped: they wait for the quest row, not this one |
| item | 136 | chain reaches `Item`. Content-shaped, **not** verified portable |
| nested helper | 97 | declared inside another type (`UnBlessEntry`, `SetFlag`, refill entries) |
| support: enum / interface | 21 / 17 | not content by themselves |
| hair/beard | 19 | ModernUO models these differently |
| equivalent | 8 | S9's EQUIV table (`ITool`, `ItemQuality`, `TalismanSkill`, ...) |
| gump / context menu / region / timer | 7 / 4 / 3 / 1 | helpers |
| **unresolved** | **46** | **no mechanical class. Read them.** Listed by `hidden --all` |

---

## Part C: the artifacts row re-measured, and what changed

**Every delta is measured on one instrument against one tree:** legacy vs fixed, both against the S9-era
customizations. Legacy equals S9's appendix file for file, so "legacy vs fixed" *is* "S9 published vs fixed". Our
ports since S9 are not mixed into the delta.

| | raw | discarded | of which aliased | candidates | drops | in-row | co-port | extract | unknown | upstream |
|---|---|---|---|---|---|---|---|---|---|---|
| **S9 published** (= legacy, S9-era tree) | 1,022 | 567 | n/a | 455 | 320 | 81 | 10 | n/a | n/a | 44 |
| **Fixed, S9-era tree** | 1,022 | **586** | **19** | **436** | 309 | 77 | 10 | **6** | **6** | **28** |

### The three numbers

**1. Called blocked by S9, not blocked: 4 of S9's 54 blocked files** (upstream 44 + co-port 10).
`MantleOfTheFallen`, `VirtuososKilt` and `SummonersKilt` drop straight in. `BestialKilt` needs only an in-row file
(`BestialSetHelper`). Every one of the four was blocked on an alias name. Six more leave "blocked by a patch" for
`extract` (below), and 5 in-row files become straight drop-ins (`CastOffZombieSkin`, `CuffsOfTheArchmage`,
`SpinedBloodwormBracers`, `GiantSteps`, `PetrifiedSnake`, each in-row only because of an aliased base).

**2. Never seen by S9 at all: 52 types in 21 discarded files of this row.** The fixed index finds 59 secondary types
in the row's discarded files. S9 mentions 7 of them anywhere, including its §7 extract list (`GargishRobe`,
`GargishFancyRobe`, `GargishClothWingArmor`, `GargishSash`, `GargoyleHalfApron`, `Epaulette`, `TalismanSkill`). The
other 52 break down as **41 item-shaped**, 8 nested helpers and 3 interfaces. Of the 41 items, **5 share a graphic
with a pinned item**: the male/female gargoyle cloth kilt, arms and chest variants, which are the alias design
working, not lost. That leaves **36 item-shaped types with no twin found**, among them the six recipe
garments, four gargoyle artifact twins, `GargishKiltOfMining`, nine `ZooMember*` / `LibraryFriend*`
rewards, seven Doom decoration pieces, `OdricsRobe`, `BaronLenshiresCloak`, `OctopusNecklace` and
`CompleteNecromancerSpellbook`. The full list is from `python tools/content_index.py hidden artifacts`.

**3. Filed under "needs a patch" when they needed reading: 10 of S9's 44 upstream files, 23%.** This is the kilts'
failure:

| Went to | Files | Why the label was wrong |
|---|---|---|
| drops / in-row | `MantleOfTheFallen`, `VirtuososKilt`, `SummonersKilt`, `BestialKilt` | the "missing upstream member" was an alias, and it already resolves |
| **extract** | `ShadowCloakOfRejuvenation` (`GargishClothWingArmor`), `Tangle1` (`GargoyleHalfApron`), `Cello`, `Cowbell`, `Trumpet`, `WallMountedBell` (`InstrumentedAddonComponent`) | a *type* inside a discarded file, not a member. Copy the class, no patch |

Six more (`ImprisonedDog`, `EpiphanyHelper`, `VirtuousEpiphany`, `AnkhPendant`, `ConjurersTrinket`,
`TalismanofGoblinSlaying`) are now `unknown`. **I am not counting those as mislabelled.** S9's bucket name does say
"or reading". But its one-word shorthand, "upstream/carrier 44", is what CC9 batch 4 §14.9 carried forward, and it
dropped the "or reading". Splitting the bucket stops that happening again.

**And one error the other way, which the brief did not ask about and which is live today: 19 phantom candidates.**
S9 said 19 files "drop straight in" whose primary type pinned already resolves through an alias (the whole
`Gargish{Leather,Stone}{Arms,Chest,Kilt,Legs}` family and its female variants, `GargishClothArmor.cs`, `Arms.cs`,
`SerpentStoneStaff.cs`). **Run S9's method on today's tree and it still says 22 files drop straight in; 19 of those
are these.** Porting any one of them puts a second type under a name `AssemblyHandler` already resolves. CC9 and
batch 5 caught them by reading. Now the instrument does.

### The row for `docs/tasks.md`, ranked. **Current tree**, because this is what is left to plan against

Fixed index, `server/customizations` as of `f50f7a6`. Raw 1,022 → discarded 978 (19 aliased) → **44 candidates**.
CC9 has ported almost all of the row since S9. For comparison, legacy on today's tree reports 63 candidates and 22
drop-ins, and the difference is exactly the 19 phantoms.

| # | What | Files / types | Cost shape | Evidence |
|---|---|---|---|---|
| 1 | **Drops straight in** | 3 files: `MLDecorationArtifacts.cs`, `VirtuousEpiphany.cs`, `Spellbooks/MysticBook.cs` | conversion only. *Static claim, never compiled* | `row artifacts` |
| 2 | **Extracts**: `InstrumentedAddonComponent` (from `AddonComponent.cs`) unlocks 4 instruments; `GargishClothWingArmor` (from `Cloaks.cs`) unlocks `ShadowCloakOfRejuvenation` | 5 files + 2 extracted types | copy a class; no patch | `row artifacts`, `extract` |
| 3 | **Hidden item types, no twin found** | **43 types in the row's discarded files** (48 item-shaped, less 5 with a same-graphic twin) | per type: extract and read. **Two sub-groups have a catch.** The 6 recipe garments (`GuildedKilt`, `CheckeredKilt`, `FancyKilt`, `FloweredDress`, `EveningGown`, `JesterShoes`) are uncraftable here without recipes 560-566 (**Q-064**). The 9 `ZooMember*` / `LibraryFriend*` rewards have no collection system in pinned (zero `BaseCollection*` declarations), so they would exist only as NPC dress or GM items | `hidden artifacts` |
| 4 | **Co-port** | 10 files: `BaseStatuette` ×4, `ExtendedWeaponAttributes` ×3, collection `Reward` ×2, `InheritsItem` ×1 | +4 ServUO files (`BaseStatuette.cs`, `Enhancement.cs`, `EngravingTools.cs`, `BaseCollectionItem.cs`). `Enhancement.cs` and `BaseCollectionItem.cs` belong to subsystems pinned lacks | `row artifacts` |
| 5 | **Unknown: read** | 4 files: `ImprisonedDog`, `AnkhPendant`, `ConjurersTrinket`, `TalismanofGoblinSlaying` | S9 §10 read a sample of these as enum renames (`Undead`, `Goblin`, `Sacrafice`); unverified per file | `row artifacts` |
| 6 | **Upstream: genuine patch work** | 22 files: `NegativeAttributes`/`Brittle`/`NoRepair` ×10, SA weapon attributes (`BalancedWeapon`, `SplinteringWeapon`, `HitFatigue`, `HitManaDrain`, `HitCurse`, `HitSparks`, `HitSwarm`) ×9, `TempDamageAbsorb`, `CheckRemove`, `RandomSuperSlayerAOS`, charm, masteries | S9 §5.1 still holds: `NegativeAttributes` is additive on `BaseAttributes`; the weapon attributes are behavioural and unmeasured | `row artifacts` |

Rows 1, 2 and 3 are the cheap, content-shaped work that the old label hid. Row 3 is the one that must not be
quoted as one number: it is 43 types to read, not 43 items to port.

---

## Is the fix bigger than 80 lines? Yes, about five times

**`tools/content_index.py` is 449 lines (379 non-blank, non-comment); the tests are 93.** The 80-line estimate was
right about what it measured, since the two scripts together were about 150 lines. It was wrong about what the fix
was. It assumed an index existed to patch. None did, so the fix had to be the whole index: parsing, S9's owner
buckets, the S9 reproduction, and a way to compare against a published appendix. The two D20 changes themselves
are a small part of that, roughly 40 lines by my reading, not counted.

---

## What the fixed index still cannot see

- **Enum members as owners.** Deliberately left as S9 had it, to change one thing at a time. So `unknown: Good` still
  appears where `Good` is a ServUO enum member. The four `unknown` files probably resolve this way. Changing it is
  the next fix, and it will move files between `unknown` and `co-port`.
- **Source-generated names.** Pinned declares `[SerializableField] private int _recipeID;` and the generator emits
  `RecipeID`. A ServUO file using a generated property name sees it as missing. Not measured.
- **The same-graphic check only reads `: base(0x...)`.** It could run on 10 of the 36 no-twin item types; the rest
  set their graphic another way. **"No twin found" means "not found by this check", not "none exists".**
- **Classification is by inheritance chain, not reading.** `item` means "derives from `Item`", nothing more. 46
  whole-tree types are `unresolved`, and they are the honest part of the output.
- **The other four rows reproduce S9 to 94-99%, not 100%:** cc4 245/255, cc7 735/745, cc7extra 190/191, cc5
  71/78. Most differences are in-row or co-port files that my index files as upstream. The artifacts row, which is
  this task's, is exact. Rerun `compare-s9 <row> --s9-title "<title>"` before quoting another row's delta.
- **S3's blacklist is not fully recoverable.** It ends in an ellipsis, and the `Internal*` prefix rule stands in for
  the rest. It moved nothing in the artifacts row.
- **Nothing is compiled.** Every "drops straight in" is still a static claim about names (S9 §10).

---

## Numbering

- **D-numbers: none taken.** Nothing was ported, so there is no deviation from OSI behaviour to record. D-92 stays
  free.
- **Q-064** taken (recipe-gated garments). Verified free with `grep -rhoE "\b[DQ]-[0-9]+\b" notes docs | sort -u`:
  highest D-91, Q-063.
- **`docs/bug-list.md`:** D20's fix is done here, and the row can be closed when this is promoted. **Proposed D24**
  (next free, header verified) for the enum-member and generated-name limits above. Not written; `docs/` is not mine.

## Reproducing this

```console
python -m unittest tools/test_content_index.py
python tools/content_index.py row artifacts                   # current tree, fixed
python tools/content_index.py hidden artifacts                # every secondary type in the row, classified
python tools/content_index.py hidden --all                    # the 509
python tools/content_index.py compare-s9 artifacts --ours <S9-era export>   # the three deltas
```

The S9-era export: `git -C D:\ShatteredLegacy archive b21bcd9 server/customizations | tar -x -C <dir>`.
