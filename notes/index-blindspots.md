# Index blind spots (D20, D24): the content index fixed, kept, and the artifacts row re-measured

**Measurement and tooling only. Nothing was ported. No file in `server/customizations`, `docs/`, either source
tree or the build changed.** The build compiles nothing this task touched, so no build was run and nothing was
tagged. That holds for both passes: D20 (Parts A to C) and D24 (Part D, 2026-09-27 overnight).

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

## Part D: D24, enum members and generated names (2026-09-27 overnight)

**Headline: 25 files change bucket across the five rows on today's tree, and 4 in the artifacts row on the
S9-era tree. Every one of them moved because of the enum fix. The generated-name fix moves no file in any row.**
A further 19 files keep their bucket but change which names they need. All of them are listed below by name.
`--legacy` did not move: 567 / 320 / 81 / 10 / 44, and 1,022 of 1,022 files in S9's bucket. Its JSON output
(names included) is **byte-identical** to the run before this change, for the artifacts row on both trees and for
cc4, cc7, cc7extra and cc5 on today's tree.

### What changed in `tools/content_index.py`

Both fixes are fixed-mode only. Legacy reads none of the new data.

**Fix 3, enum members are owned by the file declaring the enum.** Each ServUO Scripts enum's members are indexed
as `(enum, member) -> file`. A reference to a member resolves to that file **only where the referencing file writes
the member qualified by that enum**: `Alignment.Good`, `TalismanSlayerName.Goblin`. Outside the enum's own body,
that is the only way C# can name a member. ServUO Scripts has no `using static` (0 files), so there is no
unqualified form to miss. The resolved bucket follows the existing rules:

- enum file in the row: `in-row`;
- enum file not discarded: `elsewhere` (co-port);
- enum file discarded, and pinned or ours **declares the enum**: `upstream`, because pinned ships the enum and
  lacks the member, which means a patch to that enum or a rename;
- enum file discarded, and neither pinned nor ours declares the enum: `extract`, because the enum comes with the
  discarded file.

A file's **own** enum members count as its own under the same qualifier rule (see the tie below). The qualifier
scan blanks enum bodies, since a declaration is not a use, and drops `using`/`namespace` lines, since `using
Server.Spells.SkillMasteries;` is not a use of `SpellbookType.SkillMasteries`.

**Fix 4, `[SerializableField]` names.** Each pinned and ours field under `[SerializableField(...)]` adds its
generated property name to the resolving side, as a member (never a type). `generated_name()` is the mapping.

**Reporting, D24's third point.** `hidden` now says what the same-graphic check did, per item type: `twin`,
`none found` ("not found by this check") or `not run` (the graphic is not a hex literal in `: base(0x...)`, so
nothing was compared). The header counts all three. The check's logic is unchanged; see "Not fixed" below.

### How the generated name was established, not guessed

The generator is not in pinned. It ships as a NuGet analyzer, `ModernUO.Serialization.Generator` 2.14.3
(`Projects/UOContent/UOContent.csproj:53`), and only as a compiled DLL. Its metadata shows a
`SourceGeneration.GetPropertyName(String fieldName)`. **I loaded the DLL from the NuGet cache and invoked that method
directly** (PowerShell reflection; no build, nothing written anywhere but scratch) on every distinct field name in
pinned and ours: **603 of 603 agree with `generated_name()`, 0 disagree.** What the generator does:

| Field | Emits | Shape |
|---|---|---|
| `_recipeID` | `RecipeID` | leading underscore dropped, first letter capitalised, **the caps run kept** |
| `_bardingHP`, `_loginIPs`, `_multiID` | `BardingHP`, `LoginIPs`, `MultiID` | same: nothing after the first letter is touched |
| `_line1`, `_slayer2`, `_item2` | `Line1`, `Slayer2`, `Item2` | digits kept |
| `m_Hue`, `_max_hits` | `Hue`, `MaxHits` | `m_` dropped; inner underscores join with a capital. **Neither occurs in pinned** |
| `_a2b` | `A2b` | no capital after a digit. Does not occur |

**Shapes actually in pinned:** 928 `[SerializableField]` fields, **all** named `_camelCase`. Of their 563 distinct
names, 9 have a caps run and 5 a digit, and none has `m_` or an inner underscore. One is written without a space before its name
(`Dictionary<Mobile, int>_damageEntries;`, `ChampionSpawn.cs`), and the field regex allows that. **Attribute arguments do not
rename.** The annotation DLL's constructor parameters are `order`, `getter`, `setter` and `isVirtual`. Pinned uses
`(N)` 708 times, `setter: "private"` 147, `setter: "protected"` 6, `getter:, setter:` 42, positional
`"private", "private"` 24 and `isVirtual: true` once.
None changes the emitted name.

### Movement, per file, per name

`before` is fixed mode as it stood after D20; `after` is this change. Legacy is unchanged throughout.

| Row, tree | candidates | drops | in-row | co-port | extract | unknown | upstream | files moved |
|---|---|---|---|---|---|---|---|---|
| artifacts, S9-era (`b21bcd9`) | 436 | 309 → 309 | 77 → 77 | 10 → **12** | 6 → 6 | 6 → **2** | 28 → **30** | **4** |
| artifacts, today | 44 | 3 → 3 | 0 → 0 | 10 → 10 | 5 → 5 | 4 → **2** | 22 → **24** | **2** |
| cc4, today | 240 | 33 → 33 | 19 → 19 | 129 → 129 | 19 → 19 | 17 → **16** | 23 → **24** | **1** |
| cc7, today | 297 | 158 → **161** | 41 → **46** | 5 → **10** | 38 → **39** | 46 → **31** | 9 → **10** | **15** |
| cc7extra, today | 50 | 27 → 27 | 0 → 0 | 3 → **4** | 2 → **3** | 3 → **1** | 15 → 15 | **2** |
| cc5, today | 71 | 26 → **28** | 14 → **15** | 9 → **11** | 0 → 0 | 10 → **6** | 12 → **11** | **5** |

Candidate counts do not change. Neither fix touches step 1, which discards on types and alias names only.

**Every file that changed bucket (27 rows: 25 files on today's tree, plus the 2 Epiphany files that only exist
as candidates on the S9-era tree):**

| Row | File | Bucket | Resolved by | My read |
|---|---|---|---|---|
| artifacts (S9 tree) | `Armor/Sets/Epiphany/EpiphanyHelper.cs` | unknown → co-port | `Alignment.Good`, enum in `Mobiles/Normal/DespiseCreature.cs` | right. **Surprised me:** the Epiphany set's only outside need is an enum that lives in a Despise mobile file. The real work is extracting one enum. Ours has since ported `Alignment` itself (`EpiphanyHelper.cs:12`), which is why today's tree no longer lists the file |
| artifacts (S9 tree) | `Armor/Sets/Epiphany/VirtuousEpiphany.cs` | unknown → co-port | `Alignment.Good`, same | right, same |
| artifacts, both trees | `Talismans/ConjurersTrinket.cs` | unknown → upstream | `TalismanSlayerName.Undead`, enum in `Items/Equipment/Talismans/TalismanSlayer.cs` | right. Pinned's `TalismanSlayerName` is `None, Bear, Vermin, Bat, Mage, Beetle, Bird, Ice, Flame, Bovine` (`UOContent/Items/Talismans/TalismanSlayer.cs:7`). Patch the enum, and its type table |
| artifacts, both trees | `Equipment/Talismans/TalismanofGoblinSlaying.cs` | unknown → upstream | `TalismanSlayerName.Goblin`, same | right, same enum |
| cc4 | `Covetous Void Spawn/Creatures/Reptile.cs` | unknown → upstream | `AIType.AI_Necro`, enum in `Mobiles/AI/BaseAI.cs` | right. Pinned's `AIType` (`Mobiles/AI/BaseAI/AIType.cs:18`) has no `AI_Necro`, `AI_NecroMage`, `AI_Mystic`, `AI_Ninja`, `AI_Samurai`, `AI_Paladin` or `AI_Spellweaving`. **That is an AI port, not an enum patch**: each is a whole class in ServUO `Mobiles/AI/Magical AI/` (`NecroAI.cs`, `MysticAI.cs`, ...), and pinned has none of the seven. **Corrected 2026-09-28 (P2): wrong for `AI_NecroMage`.** Q-050 withdrew that one: pinned `MageAI` already casts Necromancy (`docs/patch-backlog.md:47-66`). It is a rename to `AI_Mage`, not a port. The other six stand. See `notes/backlog-remeasure-2026-09-28.md` §2a |
| cc7 | `Addons/DawnsMusicBox/RewardVersion/TrackInfo.cs` | unknown → drops | own enum `TrackRarity.UnCommon` | right |
| cc7 | `Addons/DolphinRug.cs` | unknown → in-row | `RugType.EastLarge`/`SouthLarge`, enum in `Addons/RoseRug.cs` | right |
| cc7 | `Addons/Harpsichord.cs` | unknown → extract | own enum `HarpsichordColor` (4 names, never used outside the enum) | right; its remaining need is the existing `AddonOptionGump`/`DirectionType` extract |
| cc7 | `Addons/KoiPond.cs` | unknown → drops | own enum `KoiPondSize.Large`/`Small` | right |
| cc7 | `Addons/PetParrot.cs` | unknown → upstream | `FoodType.FruitsAndVegies`, enum in `Mobiles/Normal/BaseCreature.cs` | **surprised me.** Pinned's `FoodType` has the member, spelt `FruitsAndVeggies` (`UOContent/Mobiles/BaseCreature.cs:72`). This is a one-word rename in the port, not a patch. The bucket is right by its definition and the work is smaller than it says |
| cc7 | `Addons/RoseRug.cs` | unknown → drops | own enum `RugType` | right |
| cc7 | `Addons/SkullRug.cs` | unknown → co-port | `RugType.*` now in-row; still needs `Siege`/`SiegeShard` outside | right |
| cc7 | `Decorative/DesCityWall.cs` | unknown → co-port | `ItemLevel.VeryEasy`, enum in `Items/Damageable/DamageableItem.cs` | right; the file already needed `DamageableItem.cs` |
| cc7 | `Decorative/SAShadowWall1.cs` | unknown → co-port | same | right |
| cc7 | `Decorative/SAStoneWall1.cs` | unknown → co-port | same | right |
| cc7 | `Decorative/SAStoneWall2.cs` | unknown → co-port | same | right |
| cc7 | `New Magincia/Distillation/CraftDefinition.cs` | unknown → in-row | `Liquor.Brandy`, enum in `DistillationSystem.cs` | right |
| cc7 | `New Magincia/Distillation/DistillationGump.cs` | unknown → in-row | `Liquor.Brandy`, `Group.WaterBased`/`WheatBased`, same file | right |
| cc7 | `New Magincia/Distillation/DistillationSystem.cs` | unknown → in-row | own enums `Liquor` and `Group` (the 11 names it had as unknown) | right |
| cc7 | `New Magincia/Magincia Bazaar/Core/MaginciaPlotAuction.cs` | unknown → in-row | own enum `BidType.Specific` | right |
| cc7extra | `BulkOrders/Items/FementationBarrel.cs` | unknown → extract | own enum `FruitType.Grape` | right. **The tie rule mattered here**: the file's own `FruitType` also has `Plum`, but the file writes the class `Plum` too, so the `Plum` extract is kept. My first draft dropped it |
| cc7extra | `BulkOrders/Items/SpecialNaturalDye.cs` | unknown → co-port | own enum `DyeType` (5 names) | right; still needs `BaseStatuette` |
| cc5 | `High Seas/Items/Cannons and Ammo/CannonDeed.cs` | unknown → co-port | own enum `CannonPower.Heavy` | right |
| cc5 | `High Seas/Items/Fish/FishPies.cs` | **upstream → in-row** | own enum `FishPieEffect` (14 names) | right, and **the most surprising move.** `HitsRegen`, `StamRegen` and `ManaRegen` are `FishPieEffect` members, always written `FishPieEffect.X`. Before, they matched same-named members of `Rampage.cs`, `RegenRates.cs` and a discarded file by coincidence, and that made the file look like patch work and pulled `Spells/Skill Masteries/Rampage.cs` in as a co-port |
| cc5 | `High Seas/Items/Resources/Niter.cs` | unknown → drops | own enum `NiterSize` | right |
| cc5 | `High Seas/Items/RuinedShipPlans.cs` | unknown → co-port | own enum `PlanType` (8 names, never used outside the enum) | right; still needs `OrcishGalleonDeed` |
| cc5 | `High Seas/Items/SmugglersLiquor.cs` | unknown → drops | own enum `SmugglersLiquorType` (23 names) | right |

**Files whose bucket held but whose needs changed (19):** artifacts `AnkhPendant.cs` (own `VirtueType.Sacrafice`
resolved; still `unknown` on `SpeechEventHandler`) and `BookOfMasteries.cs` (`SpellbookType.SkillMasteries` is
now `upstream`, and pinned's `SpellbookType` stops at `Mystic`, `Items/Skill Items/Magical/Spellbook.cs:16`). cc4
`Creatures.cs`, `Abyss.cs`, `ClockworkExodus.cs` and `BrigandCannibalMage.cs` (the `AIType.AI_*` members above,
unknown → upstream); `InvasionBeacon.cs` (`ItemLevel.Easy` → co-port); `InvasionController.cs` and
`VoidPoolController.cs` (own `InvasionType`/`VoidType` members resolved). cc7 `MusicBoxGears.cs`,
`DistillationContext.cs`, `LiquorBarrel.cs` (in-row enum members) and `MaginciaBizaar.cs` (own `Phase` members).
cc5 `Cannon.cs` and `ShipCannon.cs` (own `ShipPosition`; `SecurityLevel.Crewman/Officer/Passenger/Denied` →
co-port via `BaseGalleon.cs`; `DamageLevel.Pristine/Moderately/Heavily/Severely` → **extract** from
`Multis/Boats/BaseBoat.cs`, whose enum pinned does not declare), `Hooks.cs` (own `HookType`), `Trophies.cs`
(own `TrophyStyle`; **`Crab` and `Lobster` stop being in-row needs**, because the file only ever writes
`TrophyStyle.Crab`), `CorgulTheSoulbinder.cs` and `OsiredonTheScalisEnforcer.cs` (`AIType.AI_NecroMage`).

**Extra co-port files:** artifacts S9-tree 12 → 13 (+`Mobiles/Normal/DespiseCreature.cs`). cc5 23 → 22:
+`Multis/Boats/BaseBoat.cs` (the `DamageLevel` extract). −`Spells/Skill Masteries/Rampage.cs` (the `FishPies`
coincidence). −`Services/City Loyalty System/CityLoyaltySystem.cs`, which `ShipCannon.cs` and `BoatPaint.cs`
reached only because `Captain` sorted first among same-named members; they write `SecurityLevel.Captain`, which
is `BaseGalleon.cs`. Other rows are unchanged.

Every line above comes from a per-name diff of the before and after JSON, with the attribution checked against
`Index.enum_owners` and `Tree.generated_only`. Scripts: `moves2.py` in the session scratchpad, not kept.

### The enum-member-versus-type tie, and how it is broken

**The qualifier breaks it, per use.** A bare identifier set cannot say whether `Lion` means the enum member or the
mobile, but the text can. `HuntType.Lion` can only be the member. The index records every qualifier each name is
written with, and:

- **every use qualified by an enum that declares the name**: the enum's file is the **only** owner. Types and
  members of the same name are ignored. Example: `HuntingSystem.cs` writes `HuntType.Lion`, so it resolves to
  `HuntingTrophyInfo.cs`, not `Mobiles/Normal/Lion.cs` (legacy's answer). Whole tree, this applies to 223 name
  uses in non-discarded files where a same-named type or member exists. 34 of those would otherwise have hit a
  same-named *type*: the `HuntType` animals, `AmmunitionType.Cannonball` vs the `Cannonball` class,
  `Parts.PowerCore` vs `PowerCore`, `City.NewMagincia` and similar;
- **some uses enum-qualified, some not** (bare, `typeof(X)`, or behind a qualifier that is not such an enum): the
  enum's file is **added** to the type and member owners, not substituted. 19 such uses tree-wide, for example
  `ShipCannon.cs` writing both `AmmunitionType.Cannonball` and `typeof(Cannonball)`. The index cannot say which use
  is the missing one, so it keeps both. That is the conservative side: it can over-state a dependency, never hide
  one;
- **the file's own enum**: the member is the file's own only if every use outside the enum body is qualified by
  one of the file's own enums, or it is never used outside the body. `AmmoInfo.cs` declares
  `AmmunitionType.Cannonball` **and** writes `typeof(Cannonball)`, so `Cannonball` stays a need, resolving in-row
  to `CannonBall.cs`. `Trophies.cs` only writes `TrophyStyle.Crab`, so `Crab` is its own.

**Why this and not a precedence rule.** "Types win" would send `HuntType.Lion` to the mobile. "Enums win" would
send `typeof(Cannonball)` to an enum. My first draft had the own-file half as "own enum members are always own"
and it silently dropped `AmmoInfo.cs`'s `Cannonball` and `FementationBarrel.cs`'s `Plum` extract. The movement
review caught it before any number above was taken.

### The generated-name fix, measured: it moves nothing, and its five hits are coincidences

81 generated names were invisible to the index on today's tree, meaning no pinned or ours source spells them. Whole
ServUO tree, **5 name uses in 5 non-discarded files** now resolve through one, and **none of the five is in any
of the five rows**:

| ServUO file | Name | Generated by (pinned) | What the ServUO file actually means |
|---|---|---|---|
| `Items/Books/SpecialScrollBooks/RecipeBook/RecipeBookGump.cs` | `RecipeID` | `RecipeScroll.cs` | ServUO's own `RecipeScrollDefinition.RecipeID` (`RecipeBook.cs:30`) |
| `.../RecipeBook/RecipeBuyGump.cs` | `RecipeID` | same | same |
| `Services/Reports/Rendering/HtmlRenderer.cs` | `RenderMode` | `Items/Misc/EffectController.cs` | a report graph's `RenderMode` (`:363`) |
| `Services/Tomb of Kings/Chambers/Chamber.cs` | `Levers` | `Engines/Doom/LeverPuzzle/LeverPuzzleController.cs` | `ChamberLever.Levers` (`:34`) |
| `Services/XmlSpawner/XmlSpawner Core/XmlSpawner2.cs` | `ToDelete` | `Engines/Quests/Dark Tides/Mobiles/SummonedPaladin.cs` | a **local variable** (`:4357`) |

So **D24's own example does not occur in these trees.** No candidate file uses pinned's generated `RecipeID`. The
two that write `RecipeID` mean a ServUO class's property of the same name. The fix is still right for the index as
built. The resolving side is "every name pinned or ours exposes", and a generated property is one of those. But it
inherits the index's oldest limit: resolution is by name, not by whose member. It found no pinned equivalent for any
"absent" type. The D24 row's "a few absent types may have pinned equivalents" is **measured false for these five
rows**.

### Tests: 14 facts, each new one red without its fix

`python -m unittest tools/test_content_index.py`: **14 facts** (8 before, 6 new), about 12 s. New:

| Fact | Pins |
|---|---|
| `EpiphanyHelper.cs` on the S9-era tree: bucket co-port, needs `Good` from `DespiseCreature.cs`; legacy: `Good` unknown | fix 3, S9's own `unknown: Good` |
| `TalismanofGoblinSlaying.cs`: `Goblin` is missing and resolves upstream; legacy unknown | fix 3, member of an enum pinned ships |
| `HuntingSystem.cs`: `Lion` resolves to `HuntingTrophyInfo.cs` fixed, `Lion.cs` legacy; `Trophies.cs` owns `Crab`; `AmmoInfo.cs` still needs `Cannonball` | the tie-break, all three cases |
| `generated_name` on 8 fields, each pair produced by the generator itself; `DamageEntries` found despite the missing space | fix 4 mapping |
| `RecipeBookGump.cs` misses `RecipeID` legacy, not fixed; attributed to `RecipeScroll.cs` | fix 4 resolution |
| `hidden`: `MaleGargishClothKilt` twin, `GuildedKilt` none found, `HangingPlatemailArms` not run | the graphic check's reporting |

**Red then green, on scratch copies with each fix reverted in the source text** (control copy, nothing reverted:
all 14 pass):

| Reverted | Result |
|---|---|
| fix 3 (no enum owners, no own-enum rule) | 3 failures: the three fix-3 facts |
| the tie-break only (enum owners always added, own members always own) | 1 failure: the tie fact |
| fix 4 (generated names not added to the tree) | 1 failure: the resolution fact |
| fix 4's mapping (field name used as is) | 2 failures: mapping and resolution |
| graphic reporting (no `graphic_check`) | 1 error: the reporting fact |

The 8 D20 facts pass under every revert, including the file-for-file S9 reproduction.

### Not fixed: the same-graphic check itself

Measured on the artifacts row's 48 item-shaped hidden types: twin 5, **none found 18, not run 25**. Of the 25: 6
write the graphic as a **decimal** literal (`base(40681)`, the Doom decorations), 1 passes it as the **second**
argument (`GargishKiltOfMining`, `base(bonus, 0x030C)`), and 18 **inherit** it (`base(hue)`, `base()`: the
`ZooMember*`/`LibraryFriend*` rewards, the gargish artifact twins, `OdricsRobe`, `BaronLenshiresCloak`). Decimal
is a one-line change. Inheritance means walking both trees' chains to a constructor that sets a graphic, and that
is not trivial, so per the brief the logic is unchanged and only the report is. Whole tree: 136 item types, twin 22,
none found 48, not run 66.

---

## Part E: two small fixes during the P2 re-measure (2026-09-28)

Made while re-measuring the backlog (`notes/backlog-remeasure-2026-09-28.md`, which carries the numbers).
**`--legacy` unchanged:** 567 / 320 / 81 / 10 / 44, 1,022 of 1,022, and legacy row JSON byte-identical.

- **Fix 5, preprocessor lines.** `FileInfo.idents_code` is the name set with every `#...` line removed. Fixed mode
  reads it on both sides; legacy keeps `idents`. It moves 13 files across the five rows, all to cheaper buckets
  (9 gargoyle furniture addons were `unknown` on `#region Mondain's Legacy`).
- **Decimal graphics** in the same-graphic check (reporting only; no row changes).
- **Tests: 16 facts.** New: `test_preprocessor_lines_are_not_names_when_fixed` and
  `test_graphic_check_reads_decimal_literals_in_art_range`. Each is red with its fix reverted on a scratch copy.

---

## Is the fix bigger than 80 lines? Yes, about five times

**`tools/content_index.py` is 449 lines (379 non-blank, non-comment); the tests are 93.** The 80-line estimate was
right about what it measured, since the two scripts together were about 150 lines. It was wrong about what the fix
was. It assumed an index existed to patch. None did, so the fix had to be the whole index: parsing, S9's owner
buckets, the S9 reproduction, and a way to compare against a published appendix. The two D20 changes themselves
are a small part of that, roughly 40 lines by my reading, not counted.

---

## What the fixed index still cannot see

Rewritten after D24 (Part D). Enum members and generated names are no longer here. What is left, measured where it
could be:

- **ServUO's core (`ServUO-pub57/Server/`) owns nothing.** Only `Scripts/` files are owners, so a name declared in
  the core falls into `unknown` whatever it is: a type, a member or an enum member. **This is now most of what
  `unknown` means.** Across the five rows on today's tree, 54 distinct unknown names remain in 81 candidate files.
  32 of those names are core declarations: 13 types (`IPooledEnumerable`, `WorldSaveEventArgs`, `IDamageable`,
  `ColUtility`, `TimerPriority`, `ScriptCompiler`, ...), 14 members (`SpeechEventHandler`, `CurrentMastery`,
  `GetObjectsInRange`, `Dragable`, ...) and 5 enum members (`TimerPriority.FiftyMS`/`OneMinute`/...,
  `DeathMoveResult.RemainEquiped`). They need a bucket of their own, "ModernUO core renamed or lacks this", which is
  a different job from reading a Scripts file. The artifacts row's last two `unknown` files are both this:
  `ImprisonedDog.cs` (`IPooledEnumerable`, `RemainEquiped`) and `AnkhPendant.cs` (`SpeechEventHandler`).
- **Namespace segments, .NET names and attribute suffixes read as names.** Of the other 22 unknown names, by my
  reading: namespace segments written in qualified names (`Services`, `Spells`, `SkillHandlers`, `Targeting`,
  `Despise`, `TownCryer`, each a ServUO `namespace`), BCL names (`ToShortDateString`, `Distinct`, `Hashtable`), and
  `FlipableAddon`, which is `[FlipableAddon]` resolving to `FlipableAddonAttribute`, a suffix the index does not
  strip. The remaining dozen (`Authority`, `Bizaar`, `Lotto`, `MemberRange`, `Mondain`, `RiteRitual`,
  `SacrificalRitual`, `SelfDeleteTimer`, `Stall`, `Stuff`, `Vars`, `XmlSpawner2`) are **not** explained: read
  them. **2026-09-28 (P2): seven of the dozen were `#region` labels** (`Mondain`, `Authority`, `Bizaar`, `Lotto`,
  `Stall`, `Stuff`, `Vars`; also `Reward`, which had made `Hats.cs` and `Pants.cs` co-port). Fixed: fix 5 below.
  `MemberRange` is a capitalised local.
- **Resolution is by name, not by whose member.** Fix 4 shows it plainly: all five generated-name resolutions are
  same-named members of different classes, one of them a local variable (Part D). The same is true of every pinned
  identifier, and always was. An `upstream` or `drops` verdict can rest on a coincidence.
- **Capitalised local variables are read as names.** `XmlSpawner2.cs`'s local `ToDelete` was `unknown` until a
  pinned generated property of the same name hid it. `RE_MEMBER` sees declarations with modifiers, and locals have
  none. Not measured.
- **Near-miss spellings are not seen.** `PetParrot.cs` is `upstream` on `FruitsAndVegies`, and pinned has
  `FruitsAndVeggies`. A rename looks like a patch. Not measured beyond this one.
- **An enum member used in both an enum-qualified and some other way keeps every owner** (19 uses tree-wide, for
  example `ShipCannon.cs`'s `Cannonball`). That can over-state a dependency, never hide one. Deliberate: see the tie
  in Part D.
- **Generated names other than properties are not indexed.** The serialization generator also emits collection
  helpers (`AddTo{X}`, `RemoveFrom{X}`, `InsertInto{X}`, `ReplaceIn{X}`, `Clear{X}`, from its format strings) and
  `V{n}SaveFlag` enums, and pinned also references a second generator, `ModernUO.CodeGeneratedEvents`, which I did
  not examine. No unknown name in the five rows has a collection-helper shape. The rest is not measured.
- **The same-graphic check only reads a hex literal in `: base(0x...)`.** The report now says so per type: for the
  artifacts row's 48 item types it is twin 5, none found 18, **not run 25** (6 decimal literals, 1 second argument,
  18 inherited). **"None found" still means "not found by this check".** Decimal is a one-line fix; inheritance is
  not. Logic unchanged. **2026-09-28 (P2): decimal fixed** (first argument only, at least two digits, at most
  0xFFFF): twin 5 / none found 24 / not run 19. A later argument and inheritance are left, for the reasons in
  `notes/backlog-remeasure-2026-09-28.md` §5. Inheritance would "twin" `ZooMemberCloak` with `Cloak`, which is wrong
  in kind.
- **The same-graphic check never runs on absent types inside candidate files** (P2). Only hidden secondary types of
  discarded files are checked. A scratch run over the five rows found `MaleGargishClothLegs` (`Pants.cs`, same art as
  pinned `GargishClothLegsType1`), `OrcMask` and `AncientShipModelOfTheHMSCape` that way.
- **Reachability is not measured** (P2). The index says what a file needs, never what needs the file. Of the 290
  candidates portable as a group across the five rows, 97 are named in ServUO only by files pinned replaced (69 only
  by craft tables). See `notes/backlog-remeasure-2026-09-28.md` §4.
- **Recorded equivalents are not encoded** (P2). `SetWeaponAbility`, `SetSpecialAbility`, `SetAreaEffect`,
  `AI_NecroMage` (AGENTS.md known traps) and `FruitsAndVegies` still read as `upstream`. `EQUIV` is shared with
  legacy, so encoding them has to be fixed-mode only.
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
- **D24 (Part D):** fixed here; the row can close when promoted. Its successor is the first bullet of "What the
  fixed index still cannot see": **core declarations are not owners**, with the other bullets as its detail. No
  number is proposed for it. D29 is the highest D-row in `docs/` and `notes/` tonight, and two other tasks are
  writing notes concurrently, so take the next free one at promotion time. No D-number (deviation) and no
  Q-number taken.

## Reproducing this

```console
python -m unittest tools/test_content_index.py
python tools/content_index.py row artifacts                   # current tree, fixed
python tools/content_index.py hidden artifacts                # every secondary type in the row, classified
python tools/content_index.py hidden --all                    # the 509
python tools/content_index.py compare-s9 artifacts --ours <S9-era export>   # the three deltas
python tools/content_index.py row artifacts --legacy --ours <S9-era export>  # must print 320/81/10/0/0/44 of 455
```

The S9-era export: `git -C D:\ShatteredLegacy archive b21bcd9 server/customizations | tar -x -C <dir>`.
