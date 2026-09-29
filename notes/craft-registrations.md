# The four craft registrations: 50 files, not 90

2026-09-29, CC. Four additive hook files and one test file in `D:\ShatteredLegacy`. Nothing deployed, no container
started or stopped (only `build.sh`'s own throwaway test container), `docs/` not touched, nothing committed.
Read-only trees read, not edited.

---

## 0. The number you asked for

**Of the audit's 340 unreachable files, 50 are reachable when this lands, and 1 more is partly reachable.** Not
90. Predicted and actual, per gate:

| Gate | Audit predicted | Reached | Types registered | Where it broke |
|---|---|---|---|---|
| Blacksmithy | 33 | **33** | 34 | nowhere: the audit was exact |
| Tailoring | 26 | **1** | 1 | 25 of the 26 are recipe-gated, and nothing we have hands out the recipes |
| Tinkering | 17 | **14** | 15 | one resource nobody can get (`CrystalShards`); one Doom-recipe artifact; `CrystalShards` itself was never a craft product |
| Carpentry | 8 | **2** | 2 | the six Darkwood pieces need peerless ingredients that nothing drops |
| **Total** | **84 (90 as briefed; see §6)** | **50** | **52** | |

The partial file is `Items/Equipment/Jewelry/GargishNecklace.cs`: `GargishAmulet` (blacksmithy) and `GargishNecklace`
(tinkering) are now reached. Its third type, `GargishStoneAmulet`, is masonry (gate 11).

**On the live tree, which has grown since the audit:** ported content files **613**, unreachable **371 -> 320**,
partly reachable 1 -> 2. Content types reached **445 -> 497** (+52, one per registration). Of the audit's 340, one
(`VillainousEpiphany.cs`) was already reached before this task, through CC9 close's Niporailem. So of the 340: 339
unreachable before, 288 after, 51 reached, 1 partial.

**Which assumption broke.** One, three times over: **the audit counted an `AddCraft` as reach whether or not a player
can meet the entry's other conditions.** Its section 6 named this for recipes and sized it at 13 files (the Tiger Pelt
and Dragon Turtle pieces). It is 25 in tailoring alone, and the same gap covers resources: the instrument treats
`AddRes` as a read, correctly, but never asks whether the resource can be had. Blacksmithy survived exactly because
every one of its entries takes iron ingots. Section 4 has the detail and a tool fault that made one tinkering file look
craft-gated when it never was.

**What that says about gates 3, 5 and 9.** None of them is a craft table, so this failure does not carry over
directly. But the same question applies before trusting their counts: a treasure-chest or stealable-artifact entry is a
real source with no second condition, which is a good sign. Gate 9 (pinned's commented-out drops) should be checked the
same way: the drop code runs only if the boss is placed, and Ilhenir, for one, is a champion-spawn boss (section 4.3).

---

## 1. What landed

`server/customizations/Engines/Craft/`:

| File | Types | Guards | ServUO lines |
|---|---|---|---|
| `BlacksmithyCraftRegistrations.cs` | 34: gargish plate x8 (both genders), `GargishAmulet`, six shields (three gargish, three plate), 17 gargish blades, axes, polearms and maces including `Shortblade` and `GargishTessen`, `CrushedGlass`, `PowderedIron` | `Core.SA` | `DefBlacksmithy.cs` :340-357, :425-435, :643-663, :702-704, :752-760, :824-828, :912-915 |
| `TailoringCraftRegistrations.cs` | 1: `LeatherTalons` | `Core.SA` | `DefTailoring.cs:543` |
| `TinkeringCraftRegistrations.cs` | 15: `GargishNecklace`, `-Bracelet`, `-Ring`, `-Earrings`, `GargishCleaver`, `GargishButcherKnife`, `VoidOrb`, the eight ML gem jewels | `Core.SA`, `Core.ML` | `DefTinkering.cs` :209-215, :399-401, :619, :706-736 |
| `CarpentryCraftRegistrations.cs` | 2: `GargishGnarledStaff`, `AudChar` | `Core.SA` | `DefCarpentry.cs` :460, :604 |

`server/tests/Engines/Craft/CraftRegistrationsVerification.cs`: 6 facts (section 5).

**Arguments copied from ServUO entry by entry**: group, name, skill min and max, every resource with its name, amount
and message, second skills (`GargishTessen`'s Tailoring, `VoidOrb`'s Magery, `AudChar`'s Musicianship),
`ForceNonExceptional` on `VoidOrb`. **ServUO sets no `SetNeededExpansion` on any of these 52**, so none is set. Its
`if (Core.SA)` / `if (Core.ML)` guards are kept. (`IncubatorCarpentryRecipe.cs` does set `Expansion.SA` although its
ServUO line has none. Not touched here; noted, since it refuses the craft to a client without SA.)

**Three value decisions, all toward the pinned table, all display-only:**

1. **Group 1011078 (Platemail) for ServUO's 1111704**, for the eight gargish plate pieces and `GargishAmulet`. Pinned
   has no 1111704 group. ServUO folded ringmail, chainmail and platemail into it; pinned keeps the older split and files
   ServUO's other 1111704 entries from the same block, the samurai plate, under 1011078 (`DefBlacksmithy.cs:210-260`).
   Kept verbatim instead would have put gargish plate in a separate menu group beside Platemail.
2. **Group 1011173 kept verbatim** for `CrushedGlass` and `PowderedIron`. Pinned lacks it too, but has no group those two
   belong in (its nearest is 1053114, dragon-scale armour), so they appear as a new group at the end of the menu.
3. **`typeof(Log)`, 1044041, for ServUO's `typeof(Board)`** in carpentry, as both existing carpentry hooks already do.

`LeatherTalons` keeps ServUO's failure message 1044453 where pinned's leather entries use 1044463, because the brief asks
for messages verbatim and it changes nothing a player can do.

**Side effects of registering, all ServUO behaviour:** a type in a craft table is also found by pinned's salvage bag
(`SalvageBag.cs:61`, resmelt), our `SmithGuildSalvageBag.cs:128`, scissoring (`BaseArmor.cs:673`, `BaseClothing.cs:269`)
and repair. These types become resmeltable and repairable. ServUO does the same, because it uses the same lookups.

---

## 2. Left out, and why

**Type absent** (neither tree, so not this task): 10 blacksmithy, 39 tailoring, 55 tinkering, 70 carpentry entries,
listed by `parse_defs.py` in section 7. They include cannons and cannonballs, the Krampus pieces, the gargish robes and
sashes, Ter Mur furniture, and `ExodusSacrificalDagger`. Eighteen of the "absent" tailoring names are ServUO's gargish
cloth and leather armour, which pinned has as `Gargish*Type1/Type2` and **already crafts** (section 6).

**Resource absent or unobtainable:**

| Entry | Missing | Kind |
|---|---|---|
| `BritchesOfWarding`, `GlovesOfFeudalGrip` (smith), `CuffsOfTheArchmage` (tailor), `BraceletOfPrimalConsumption` (tinker) | `BloodOfTheDarkFather`, in neither tree | also recipe-gated (Doom) |
| `MaceBelt`, `SwordBelt`, `DaggerBelt`, three Crimson belts | `Lodestone`, in neither tree | also recipe-gated |
| `ElegantCollar`, `ElegantCollarOfFortune` | `FeyWings`, in neither tree | also recipe-gated |
| 8 Tiger Pelt, 5 Dragon Turtle Hide | `TigerPelt`, `DragonTurtleScute` (Q-066) | also recipe-gated (gate 8) |
| `ArcanicRuneStone` | `CrystalShards`: ours, but ServUO's only source is a Ter Mur lumberjacking bonus (`Services/Harvest/Lumberjacking.cs:111`) that pinned lacks | |
| `DarkwoodCrown`, `-Chest`, `-Gorget`, `-Pauldrons`, `-Gloves` | `LardOfParoxysmus`, `DiseasedBark`, `DreadHornMane`, `EyeOfTheTravesty`, `CapturedEssence`: declared by pinned (`Items/Resources/MiscMLResources.cs`), **dropped by nothing** in pinned or ours | pinned's own `DefBlacksmithy`, `DefBowFletching`, `DefTailoring`, `DefTinkering` and `DefInscription` use them too, so pinned has the same hole |
| `DarkwoodLegs` | has `GrizzledBones` (pinned `Ilhenir.cs:142`) but needs `Putrefaction`, whose only source is our `BasePeerless.PackResources`, **which nothing calls** | |

`WoodPulp` and `WorkableGlass`, which the brief named: neither appears in an entry for a type of ours. `WorkableGlass`
is used only by tinkering entries whose types are absent (the lamps, `KotlPowerCore`, the telescope, `DefTinkering.cs`
:461-471, :535, :659). No `WoodPulp` in the four tables.

**Recipe-gated with no recipe source.** `AssassinsCowl` and `MagesHood` have both resources (`VileTentacles` from
`MaddeningHorror`, `VoidCore` from `UnboundEnergyVortex`, both reached). Their recipes do not. In ServUO the six base
EJ recipes (1100-1103, 1108-1109) come only from `TreasureMapChest.GetRandomRecipe` (`TreasureMapChest.cs:523`) and
`TreasureMapInfo.cs:917`, and the six upgrades (1104-1107, 1110-1111) only from the Forsaken Foes event
(`Services/Seasonal Events/ForsakenFoes/Gumps.cs:53-58`). Pinned's chests make no recipe scrolls (Q-064 section 4).
Registering these with `AddQuestRecipe` would be correct and would still reach nobody, so they are not registered.
**The `AddQuestRecipe` decision (brief section 4) was therefore never exercised:** no entry here is recipe-gated. It is
written into `TailoringCraftRegistrations.cs`'s header for whoever builds the recipe source.

**Pinned types that ServUO crafts and pinned's table does not** (not ours, so out of scope, as `OrcMaskTailoringRecipe.cs`
already said of the four masks), found by the same script:
blacksmithy `DreadSword`, `GargishTalwar`, `BloodBlade`, `DualShortAxes`, `DualPointedSpear`, `DiscMace`, `Boomerang`,
`Cyclone`, `SoulGlaive`; tailoring `BearMask`, `DeerMask`, `TribalMask`, `HornedTribalMask` and 18 ML elven and hide
pieces (`ElvenShirt` ... `HideGorget`); tinkering `Pitchfork`, `BroadcastCrystal`; carpentry `Club`, `BlackStaff`,
`GargishWoodenShield`. By regex over pinned's `AddCraft(typeof(X)`; the 18 ML clothing pieces surprised me and I have
not checked them by hand. **Five of the nine smith ones are gargish throwing and dual weapons, so the "gargoyle
equipment" gap is not fully closed by this task.**

---

## 3. Every registered type reaches a player, and how

Each is a craft entry with its skill, a tool pinned ships, and resources a player can get:

| Resource | Source in pinned or ours |
|---|---|
| iron ingots, cloth, leather, logs, granite | mining, tailoring, lumberjacking as stock |
| `BlueDiamond`, `DarkSapphire`, `EcruCitrine`, `FireRuby`, `PerfectEmerald`, `Turquoise` | pinned `Mining.cs:206-217`, ML bonus harvest |
| `WhitePearl` | pinned `Fishing.cs:116`, bonus harvest |
| `BrilliantAmber` | pinned `Lumberjacking.cs:98`, bonus harvest |
| plain gems (`Amber`, `Ruby`, `Sapphire` ...) | stock loot and mining |
| `BlackPearl` | reagent vendors |
| **`GlassSword`** (5 per `CrushedGlass`) | **only character creation**: ours `CharacterCreation.cs:514`, `:551`, two gargoyle professions. ServUO also crafts it by glassblowing (`DefGlassblowing.cs:153`), which pinned's glassblowing lacks. **Reachable, barely**: five new gargoyle characters per crushed glass. Registered anyway because the entry is faithful and the resource does exist in play; it is the one weak link in the 52 |

---

## 4. The pinned craft systems, per system

**All four expose `CraftSystem` additively.** Checked in source and proven by the facts:

| System | Property | Set by | Append API |
|---|---|---|---|
| `DefBlacksmithy` | `public static CraftSystem CraftSystem { get; private set; }` (`:24`) | `Initialize()` (`:11`), private ctor | `AddCraft`, `AddRes`, `AddSkill`, `ForceNonExceptional` all public (`Core/CraftSystem.cs:126-293`) |
| `DefTailoring` | same (`:29`) | `Initialize()` (`:16`) | same |
| `DefTinkering` | same (`:38`) | `Initialize()` (`:25`) | same |
| `DefCarpentry` | same (`:21`) | `Initialize()` (`:8`) | same |

`private set` means a hook can append but never replace the table, which is the property we want. `Initialize` runs
by name at startup and `ServerStarted` fires after it, as the three earlier hooks already rely on. Nothing in ours
calls `Initialize` again. The fact in section 5 builds a **second, stock** instance through the private constructor
and shows it has none of these entries while the live one has all of them.

### 4.1 The audit's instrument, two faults found here

1. **`typeof` inside an `AddCraft` call counts as reach for every type in it, resources included.** `typeof_site`
   gives both the product and the first resource the site `AddCraft`. So ServUO's
   `AddCraft(typeof(ArcanicRuneStone), ..., typeof(CrystalShards), ...)` made tinkering look like a source of
   `CrystalShards`, and the audit listed it under gate 4. It is a resource there, and nothing in ServUO's craft tables
   makes one. `AddRes` is already a reader; the first resource needs the same treatment. **Not fixed here**: none of my
   four files has one of our types as a first resource, so today's numbers are unaffected. It would change the audit's
   `--sources` output. A later task should fix it with a fact and a watched red.
2. **A method nobody calls counts as live code.** `Putrefaction` is reported reached through
   `BasePeerless.PackResources` -> `SlasherOfVeils` -> `Abyss.json`. `SlasherOfVeils` is placed, but nothing in either
   tree calls `PackResources` (grep: its declaration is the only hit). Pinned's `Ilhenir` and `Meraktus` have their own
   `PackResources` without `Putrefaction`. So one "reached" type is not. This is the audit's section 6 "typeof at a
   site with no name" risk in another form: reach is decided per type, not per method.

### 4.2 Resources are outside the instrument

The reach rule treats a craft entry as reach and `AddRes` as a read. Both are right. But the instrument never asks
whether the resources can be had, and that question decided 30 of the 90 files. Worth a line in the audit's section 6
table.

### 4.3 World generation still applies

Every craft entry here needs only a player, a tool and resources, so none depends on a world having had a generator
run. The two conditional resources are `GrizzledBones` (Ilhenir, a Corrupt champion boss, relevant only to the excluded
Darkwood legs) and none of the registered 52.

---

## 5. Proof

**Facts** (`server/tests/Engines/Craft/CraftRegistrationsVerification.cs`):

1. `BlacksmithyCraftsServUOsThirtyFourGargishAndPlateEntries`: all 34 entries once each, with group, name, min, max,
   first resource and amount, `Expansion.None`, no recipe, and the type constructed the way `CompleteCraft` does
   (`ItemType.CreateInstance<Item>()`). Also the second skill and resource on Tessen, Crushed Glass and Powdered Iron,
   the six shields at the end of their group in ServUO's order, and both Doom pieces absent.
2. `TailoringCraftsLeatherTalonsAndNothingItsRecipesOrResourcesWouldStrand`: talons verbatim, including message
   1044453; all 26 excluded types absent.
3. `TinkeringCraftsGargishJewelleryUtensilsTheVoidOrbAndTheEightGemJewels`: 15 entries; `VoidOrb`'s Magery, pearls and
   non-exceptional flag; each gem jewel's 20 plain and 10 rare gems; the two exclusions absent.
4. `CarpentryCraftsTheGargishGnarledStaffAndTheAudCharButNoDarkwood`.
5. `PinnedsOwnTablesCraftNoneOfTheseTypesAndTheLiveTablesCraftAllOfThem`: **the "not craftable before" fact.** For
   each system, a fresh stock table (`Activator.CreateInstance(typeof(DefX), true)`) lacks 11 sample types and the live
   one has them.
6. `ATinkerWithThreeIngotsAndToolsMakesAGargishRing`: `CraftItem.CompleteCraft` end to end. A PlayerMobile with 120
   Tinkering, tinker tools and exactly three ingots ends with a `GargishRing` in the pack and no ingots.

**Red, watched, twice.** For the red runs each hook's `Register()` got a temporary `return;` straight after
`_registered = true;`, so the files compiled and registered nothing. `build.sh --tests-only`:

```
red 1:  Passed: 162  Failed: 6   BUILD FAILED: ShatteredLegacy.Tests tests did not pass. No image was built.
  Blacksmithy... / Tailoring... / Tinkering... / Carpentry...   Assert.Single() Failure: The collection did not contain any matching items
  ATinkerWithThreeIngotsAndToolsMakesAGargishRing                Assert.NotNull() Failure: Value is null
  PinnedsOwnTables...                                            System.Exception : Attempting to create recipe with preexisting ID.
```

**Five were red for the right reason and one was not.** Building a second stock table re-registers pinned's recipes
into the process-wide `Recipe.Recipes`, and `Recipe`'s constructor throws on a duplicate ID (`Core/Recipes.cs:18-20`).
That fact would have stayed red after the fix too. It now empties the registry while it builds the stock tables and
restores it exactly in a `finally`. Red again with the stubs:

```
red 2:  Passed: 162  Failed: 6
  PinnedsOwnTables...   Assert.NotNull() Failure: Value is null      (stock lacks them: passed; live lacks them: red)
  the other five as in red 1
```

**Green, full `build.sh`, all three stages**, stubs removed:

```
Total tests: 168
     Passed: 168
[tests] 168 test(s) passed.
Built sl-modernuo:latest with patches applied and 168 shard test(s) passing.
```

168 is the 162 that were already there plus these 6. The other 162 were green in both red runs, so nothing else
depended on these tables being without the new entries.

---

## 6. What the brief restated wrongly

1. **"A gargoyle player on this shard today cannot obtain a single piece of gargoyle-specific equipment."** Wrong.
   Pinned's tailoring crafts nine gargish leather and eight gargish studded pieces (`DefTailoring.cs:543-559`,
   `:614-628`). Our character creation gives gargoyles a `GlassSword` and gargish leather (`CharacterCreation.cs:514-518`).
   The audit's section 8.2 said something narrower and true: the gargish **plate**, weapons, shields and jewellery *in
   our tree* were in no player's reach. After this task those are craftable. Still out: gargish stone armour
   (masonry, gate 11), the gargish cloth pieces pinned may or may not craft (not checked), and the five pinned-declared
   gargish weapons pinned's blacksmithy omits (section 2).
2. **"Ninety files, four hooks."** The audit's own table sums to 33 + 26 + 17 + 8 = **84**. 90 is the audit's section 7
   item 5 figure ("90 files alone"), which does not match its table. Neither is what landed: 50.
3. **"The audit says the others [expose CraftSystem] too."** True for all four (section 4).
4. **"Gates 1 and 4 close it."** Gate 7 (carpentry) supplies `GargishGnarledStaff`, one of the audit's "21 gargish
   weapons", and gate 11 (masonry) the stone amulet. Minor.
5. **"The 13 Tiger Pelt and Dragon Turtle pieces ... are not in this task."** Right, and they are not the only
   recipe-gated tailoring entries: 12 more are, with no recipe source at all (section 2).
6. **"340 unreachable files."** Correct for the audit's HEAD. The live tree now has 613 ported content files and 371
   unreachable before this task. The 340 list itself is still a valid subset: all 340 files exist on the live tree.

---

## 7. Method, reproduction

- `parse_defs.py` (scratchpad): parses each ServUO `Def*.cs` `InitCraftList` into statements, attaches the
  `index`-using calls to their `AddCraft`, records the enclosing `if (Core.X)` blocks, and classifies each type and
  resource against a class index of pinned and ours. 196 / 198 / 157 / 223 entries; 36 / 28 / 17 / 14 ours-only.
  Every one of the 95 ours-only entries was then read by hand in context.
- Reach: `python tools/content_index.py reach --ours D:\ShatteredLegacy\server\customizations --json OUT`, before and
  after, diffed per file and against Appendix A of `reachability-audit.md` (340 files, parsed from the note).
- Resource sources: grep of pinned and ours for `new X(` and `typeof(X)` per resource, each hit read.

**Not done:** no commit (brief). `tools/progress.py` not run: it rewrites `README.md` and `progress.json`. Chase can
run it with the commit. `tools/content_index.py` not changed (section 4.1). No client check: nothing here was crafted
through a gump. No D-number or Q-number taken. The recipe-source gap (section 2) and the two tool faults are Q-shaped.
