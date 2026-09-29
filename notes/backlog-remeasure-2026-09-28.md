# Backlog re-measure on the fixed index (P2, 2026-09-28)

**Measurement and a proposal. Nothing was ported, nothing built, nothing committed.** No file in
`D:\ShatteredLegacy`, `docs/` or either source tree changed. The shard tree was read only through `git archive` of
ShatteredLegacy `8a52998` (HEAD) into scratch, because P1 is working in the live tree. Its one uncommitted
customizations change, a single line in `BestialArms.cs`, moves nothing: live tree and `8a52998` give identical rows.

Two small changes went into `tools/content_index.py`, both covered by tests and both **fixed-mode only for the rows**:
decimal graphics in the same-graphic check, and preprocessor lines no longer read as names (§5). **`--legacy` did not
move: 567 / 320 / 81 / 10 / 44, 1,022 of 1,022 files in S9's bucket**, and legacy row output is byte-identical to the
run before either change.

Every number below is **this instrument's answer**, not ground truth. Where a number comes from a scratch analysis
built *on* the instrument (closure, reachability, what-ifs), it says so. Where a proposal rests on something the
instrument cannot see, it says so at that point.

---

## 0. The number you asked for

**How much of the remaining backlog was only ever waiting on a name the index could not resolve?**

**Small: 41 of 725 files, 5.7%.** On today's tree the S9 method (`--legacy`) reports 725 candidates across the
five rows, 264 of them drop-ins and 461 blocked. Tonight's instrument (D20 + D24 + tonight's P2 fix) changes the
answer to *is there work here at all* for 41 of them:

| | Files | What they were |
|---|---|---|
| Blocked by legacy, drop straight in now | **18** | 4 co-port, 14 upstream (patch). Named in §2 |
| Not work at all: pinned already has them under an alias | **23** | 19 of which legacy calls **drop-ins** (the artifacts phantoms), 4 upstream (cc7 spinning wheels) |

So the fraction that was *only* a name is 18 of 461 blocked files (3.9%), and 23 more are work that must not be
done. **That on its own does not change what we do next.**

**What does change it is the label on the work that remains.** Legacy calls 229 files "needs an upstream member":
patch or carrier work. On the fixed instrument **only 84 of the 229 still say so, and 145 (63%) never needed a
patch**:

| Legacy `upstream` 229 → | Files | Meaning |
|---|---|---|
| `extract` | 66 | copy a type out of a discarded ServUO file. Content work |
| `unknown` | 45 | **44 of 45 are ServUO *core* API names** (scratch what-if, §4): conversions, not patches. 1 is a capitalised local |
| `in-row` / `elsewhere` | 16 | co-port work |
| `drops` | 14 | nothing needed |
| `aliased` | 4 | already in pinned |
| still `upstream` | 84 | **of which 7 are recorded renames** (`AI_NecroMage`→`AI_Mage` per Q-050, `SetSpecialAbility`, `SetAreaEffect`, `FruitsAndVegies`) or `TimerPriority.OneSecond`. ~77 genuine patch files |

**Two further measures, scratch analyses on the instrument's own answers** (§4):

- **Portable as a group** (every need resolves inside the group): **290 of 702** candidates, 41%. 321 if core-API
  conversions count. The count by instrument version: D20 **271** → D24 **279** → P2 **290**.
- **Reachable once ported:** of those 290, **97 are named in ServUO only by files pinned replaced** (craft, loot,
  reward and vendor tables). **69 of the 97 are craft-table entries** (`DefCarpentry` alone names 43). 126 are named
  only by other *unported* content, 64 by no `.cs` file at all.

**So my read: the backlog is mostly real work, but far less of it is patch work than we planned.** The binding
constraint on the cheap end is not dependencies, it is **reachability**, and the instrument cannot see that at all.
It answers "what does this file need", never "what needs this file". The batches in §3 are shaped around that.

---

## 1. The delta, row by row

Five instruments on one tree (`8a52998`), plus S9's published appendix. Candidates exclude discarded files.
`aliased` = discarded because pinned resolves the primary type only through `[TypeAlias]`.

| Row | Instrument | cand. | drops | in-row | co-port | extract | unknown | upstream | aliased |
|---|---|---|---|---|---|---|---|---|---|
| **artifacts** | S9 published (S9-era tree) | 455 | 320 | 81 | 10 | — | — | 44 | — |
| | legacy, today | 63 | 22 | 0 | 10 | — | — | 31 | — |
| | D20 fixed (CC9 remainder row) | 44 | 3 | 0 | 10 | 5 | 4 | 22 | 19 |
| | D24 fixed | 44 | 3 | 0 | 10 | 5 | **2** | **24** | 19 |
| | **P2 fixed (tonight)** | 44 | **5** | 0 | **8** | 5 | 2 | 24 | 19 |
| **cc4** | S9 published | 255 | 31 | 25 | 140 | — | — | 59 | — |
| | legacy, today | 240 | 32 | 19 | 130 | — | — | 59 | — |
| | D20 | 240 | 33 | 19 | 129 | 19 | 17 | 23 | 0 |
| | D24 | 240 | 33 | 19 | 129 | 19 | **16** | **24** | 0 |
| | **P2** | 240 | 33 | 19 | 129 | 19 | 16 | 24 | 0 |
| **cc7** | S9 published | 303 | 159 | 50 | 5 | — | — | 89 | — |
| | legacy, today | 301 | 158 | 41 | 5 | — | — | 97 | — |
| | D20 | 297 | 158 | 41 | 5 | 38 | 46 | 9 | 4 |
| | D24 | 297 | **161** | **46** | **10** | **39** | **31** | **10** | 4 |
| | **P2** | 297 | **170** | **48** | 10 | 39 | **20** | 10 | 4 |
| **cc7extra** | S9 published | 57 | 33 | 0 | 5 | — | — | 19 | — |
| | legacy, today | 50 | 27 | 0 | 3 | — | — | 20 | — |
| | D20 | 50 | 27 | 0 | 3 | 2 | 3 | 15 | 0 |
| | D24 | 50 | 27 | 0 | **4** | **3** | **1** | 15 | 0 |
| | **P2** | 50 | 27 | 0 | 4 | 3 | 1 | 15 | 0 |
| **cc5** | S9 published | 77 | 31 | 17 | 12 | — | — | 17 | — |
| | legacy, today | 71 | 25 | 14 | 10 | — | — | 22 | — |
| | D20 | 71 | 26 | 14 | 9 | 0 | 10 | 12 | 0 |
| | D24 | 71 | **28** | **15** | **11** | 0 | **6** | **11** | 0 |
| | **P2** | 71 | 28 | 15 | 11 | 0 | 6 | 11 | 0 |
| **all five** | legacy, today | 725 | 264 | 74 | 158 | — | — | 229 | — |
| | D20 | 702 | 247 | 74 | 156 | 64 | 80 | 81 | 23 |
| | D24 | 702 | 252 | 80 | 164 | 66 | 56 | 84 | 23 |
| | **P2** | 702 | **263** | **82** | **162** | 66 | **45** | 84 | 23 |

How to read the lines:

- **S9's cc7 heading says 297**, but its appendix lists 303 files in these four buckets. I did not investigate.
- **S9 published → legacy today** is ports done since S9 (tree drift), not instrument change. The artifacts row
  collapsed because CC9 ported it. S9's non-artifacts rows reproduce only 94-99% under `--legacy`
  (`notes/index-blindspots.md`, "still cannot see"), so treat those two lines as approximate for cc4, cc7,
  cc7extra and cc5.
- **legacy today → P2** is instrument change only, same tree.
- **D20 → D24 → P2** is the fix history. **D20 is the instrument the CC9 remainder row in `docs/tasks.md` was
  measured with**, and the D20 line reproduces that row exactly (3 / 5 / 10 / 4 / 22 of 44).
- The D24 lines are identical to last night's Part D table in `notes/index-blindspots.md`. **Nothing has been ported
  into these rows since**, so today's tree gives the same answer.

**The CC9 remainder row as it now stands:** 44 candidates. 5 drop straight in (was 3), 8 co-port (was 10), 5
extract, 2 unknown (was 4), 24 upstream (was 22). **Hidden item types with no twin found: still 43** (48 item-shaped,
5 twins). The same-graphic check now reads 6 more of them (§5), none of them twins.

---

## 2. Every file that moved, by name

### 2a. The D24 fix: 25 files changed bucket, 19 changed names only

Re-derived tonight from a per-name diff of D20 against D24 on `8a52998`. It matches Part D file for file. **21 of
the 25 moved to a cheaper or clearer bucket. 4 moved from `unknown` to `upstream`**, the direction the brief asked me
to call out. **No file moved from a resolved bucket into `unknown`.**

| Row | File | Move | Resolved by | My read |
|---|---|---|---|---|
| artifacts | `Talismans/ConjurersTrinket.cs` | **unknown → upstream** | `TalismanSlayerName.Undead` | right. Pinned's enum stops at `Bovine` (`Items/Talismans/TalismanSlayer.cs:7`) |
| artifacts | `Talismans/TalismanofGoblinSlaying.cs` | **unknown → upstream** | `TalismanSlayerName.Goblin` | right, same enum |
| cc4 | `Covetous Void Spawn/Creatures/Reptile.cs` | **unknown → upstream** | `AIType.AI_Necro` | right: `NecroAI.cs`, 106 lines, genuinely absent (`docs/patch-backlog.md:83`) |
| cc7 | `Addons/PetParrot.cs` | **unknown → upstream** | `FoodType.FruitsAndVegies` | **bucket right, work wrong.** Pinned spells it `FruitsAndVeggies` (`Mobiles/BaseCreature.cs:72`): a rename. Its real remaining need is the co-port (`ParrotItem`, P14) |
| cc7 | `DawnsMusicBox/RewardVersion/TrackInfo.cs` | unknown → drops | own `TrackRarity.UnCommon` | right |
| cc7 | `Addons/KoiPond.cs` | unknown → drops | own `KoiPondSize` | right |
| cc7 | `Addons/RoseRug.cs` | unknown → drops | own `RugType` | right |
| cc7 | `Addons/DolphinRug.cs` | unknown → in-row | `RugType.*` in `RoseRug.cs` | right |
| cc7 | `Distillation/CraftDefinition.cs` | unknown → in-row | `Liquor.Brandy` in `DistillationSystem.cs` | right |
| cc7 | `Distillation/DistillationGump.cs` | unknown → in-row | `Liquor.*`, `Group.*`, same | right |
| cc7 | `Distillation/DistillationSystem.cs` | unknown → in-row | own `Liquor`, `Group` (11 names) | right. **This file and the two above are the D24 dividend in §3, batch 3** |
| cc7 | `Magincia Bazaar/Core/MaginciaPlotAuction.cs` | unknown → in-row | own `BidType.Specific` | right |
| cc7 | `Addons/SkullRug.cs` | unknown → co-port | `RugType.*` in-row; still needs `Siege` | right |
| cc7 | `Decorative/DesCityWall.cs`, `SAShadowWall1.cs`, `SAStoneWall1.cs`, `SAStoneWall2.cs` | unknown → co-port (×4) | `ItemLevel.VeryEasy` in `Items/Damageable/DamageableItem.cs` | right. Mis-filed co-port all along |
| cc7 | `Addons/Harpsichord.cs` | unknown → extract | own `HarpsichordColor` | right; its extract is `AddonOptionGump` |
| cc7extra | `BulkOrders/Items/FementationBarrel.cs` | unknown → extract | own `FruitType.Grape` | right; `Plum` extract kept by the tie rule |
| cc7extra | `BulkOrders/Items/SpecialNaturalDye.cs` | unknown → co-port | own `DyeType` (5 names) | right; needs `BaseStatuette` |
| cc5 | `Items/Fish/FishPies.cs` | **upstream → in-row** | own `FishPieEffect` (14 names) | right, and **the only move out of `upstream`**. `HitsRegen`/`StamRegen`/`ManaRegen` matched unrelated members by coincidence |
| cc5 | `Items/Resources/Niter.cs` | unknown → drops | own `NiterSize` | right |
| cc5 | `Items/SmugglersLiquor.cs` | unknown → drops | own `SmugglersLiquorType` (23 names) | right |
| cc5 | `Cannons and Ammo/CannonDeed.cs` | unknown → co-port | own `CannonPower.Heavy` | right (CC8 content) |
| cc5 | `Items/RuinedShipPlans.cs` | unknown → co-port | own `PlanType` | right; needs `OrcishGalleonDeed` (CC8) |

Same bucket, needs changed (19): artifacts `AnkhPendant.cs` (`Sacrafice` own), `BookOfMasteries.cs`
(`SkillMasteries` unknown → upstream). cc4 `Creatures.cs`, `Abyss.cs`, `ClockworkExodus.cs`,
`BrigandCannibalMage.cs` (`AI_*` unknown → upstream), `InvasionBeacon.cs` (`ItemLevel.Easy` → co-port),
`InvasionController.cs`, `VoidPoolController.cs` (own enums). cc7 `MusicBoxGears.cs`, `DistillationContext.cs`,
`LiquorBarrel.cs` (in-row enum members), `MaginciaBizaar.cs` (own `Phase`). cc5 `Cannon.cs`, `ShipCannon.cs`,
`Hooks.cs`, `Trophies.cs` (own enums; `Crab`/`Lobster` stop being needs), `CorgulTheSoulbinder.cs`,
`OsiredonTheScalisEnforcer.cs` (`AI_NecroMage`).

**One correction to last night's reads (Part D), which surprised me.** Part D says of `AIType` that pinned has none
of the seven members and "that is an AI port, not an enum patch". **For `AI_NecroMage` that is wrong, and the project
already knew it.** Q-050 withdrew it: pinned `MageAI` already casts Necromancy (`docs/patch-backlog.md:47-66`,
AGENTS.md "Known traps"). So `BrigandCannibalMage.cs` (`AI_NecroMage` + `SetSpecialAbility`, both recorded
transformations) is **not patch work**, and `CorgulTheSoulbinder` / `OsiredonTheScalisEnforcer` are blocked by
`IsSoulbound`, not by their AI. The other six (`AI_Necro`, `AI_Mystic`, `AI_Ninja`, `AI_Samurai`, `AI_Paladin`,
`AI_Spellweaving`) are genuinely absent, as the patch backlog costs them. I have corrected Part D in
`notes/index-blindspots.md`.

### 2b. Tonight's P2 fix: 13 files changed bucket, 4 changed names only

The instrument read `#region` labels as names (§5). Every one of these moved to a cheaper bucket.

| Row | File | Move | The "name" it was waiting on |
|---|---|---|---|
| artifacts | `Equipment/Clothing/Hats.cs` | **co-port → drops** | `Reward`, from `#region Reward Clothing`. It dragged in `Services/CommunityCollections/BaseCollectionItem.cs`, a subsystem file pinned lacks |
| artifacts | `Equipment/Clothing/Pants.cs` | **co-port → drops** | same |
| cc7 | `Addons/GargishCotEastAddon.cs`, `GargishCotSouthAddon.cs`, `GargishCouchEastAddon.cs`, `GargishCouchSouthAddon.cs`, `GargishLongTableEastAddon.cs`, `GargishLongTableSouthAddon.cs`, `LargeGargoyleBedEastAddon.cs`, `LargeGargoyleBedSouthAddon.cs`, `Decorative/GargoyleShortTableAddon.cs` | **unknown → drops** (×9) | `Mondain`, from `#region Mondain's Legacy` |
| cc7 | `Housing Lotto/Core/MaginciaHousingPlot.cs` | unknown → in-row | `Lotto`, `#region Lotto Info` |
| cc7 | `Magincia Bazaar/Core/MaginciaBizaarPlot.cs` | unknown → in-row | `Stall`, `#region Stall Style Multis` |

Names only: cc4 `Level3Spawner.cs` (`Stuff`), cc7 `HitchingPost.cs` (`Mondain`), `Utensils.cs` (`Vars`),
`MaginciaBizaar.cs` (`Authority`, `Bizaar`). Extra co-port files: artifacts 10 → 9 (`BaseCollectionItem.cs`
gone). No other row's extras changed.

### 2c. Legacy → P2, every file whose answer to *is there work* changed (41)

- **Aliased, already in pinned (23):** artifacts `FemaleGargish{Leather,Stone}{Arms,Chest,Kilt,Legs}` (8),
  `Gargish{Leather,Stone}{Arms,Chest,Kilt,Legs}` (8), `GargishClothArmor.cs`, `Arms.cs`, `SerpentStoneStaff.cs`
  (all legacy **drops**); cc7 `ElvenSpinningwheel{East,South}Addon.cs`, `Spinningwheel{East,South}Addon.cs` (legacy
  upstream). All D20.
- **Blocked, now drops (18):** D20: cc4 `GargishBracersofAlchemicalDevastation.cs`, cc5 `FishermansSet.cs`. D24:
  cc7 `TrackInfo.cs`, `KoiPond.cs`, `RoseRug.cs`; cc5 `Niter.cs`, `SmugglersLiquor.cs`. P2: artifacts `Hats.cs`,
  `Pants.cs`; the nine gargoyle furniture files above.

---

## 3. The next three batches, in order

The order is: finish the row that says START HERE, then the largest cheap block, then the system D24 freed. **None
of it is started.**

### Batch 1: close CC9. 11 files, about 25 types, 2 extracted types

| Part | What | Notes, including what the instrument cannot see |
|---|---|---|
| drops | `Sets/Epiphany/VirtuousEpiphany.cs` (10 types) | our `VillainousEpiphany.cs` and `EpiphanyHelper.cs` are its twins, so take their bases. Its only ServUO referrer is `Niporailem.cs`, which pinned and ours lack, so the **drop source is unverified** |
| drops | `Spellbooks/MysticBook.cs` (1 type) | also unblocks cc5's `CorgulsHandbookOnMysticism.cs` (in the group, ride it along). Pinned's `CharacterCreation.cs:1347` has `// PackItem(new MysticBook(0xAB));` commented out. Ours replaces that file, so noted, not proposed |
| drops | `Clothing/Hats.cs`: **5 of its 8 absent types** | port `JesterHatOfChuckles`, `NystulsWizardsHat`, `GypsyHeaddress`, and `OrcMask` after reading it: it shares 0x141B with pinned `OrcishKinMask`, and ServUO reaches it through `DefTailoring.cs:245` and `Loot.cs:411`, both replaced by pinned. `ChefsToque` per **Q-064** (recipe 561). **Leave** `ZooMemberBonnet`, `ZooMemberFloppyHat`, `LibraryFriendFeatheredHat` (Q-064's rule: no collection system) |
| drops | `Clothing/Pants.cs`: **1 of 4** | `MalabellesDress`. Leave the two `LibraryFriend*`. **Do not port `MaleGargishClothLegs`:** same graphic 0x40A as pinned `GargishClothLegsType1`, the kilt pattern again |
| drops, decide | `Decorative/MLDecorationArtifacts.cs` | **`AncientShipModelOfTheHMSCape` is pinned's `ShipModelOfTheHMSCape` with a different name**: same art 0x14F3, hue 0x37B, cliloc 1063476. ServUO reaches it only through `TreasureMapChest.cs`/`TreasureMapInfo.cs`. Port it with a treasure-chest hook, or skip it. I would skip |
| extract | `InstrumentedAddonComponent` from `Items/Addons/AddonComponent.cs` → `Cello`, `Cowbell`, `Trumpet`, `WallMountedBell` | copy a class; drop source not checked |
| extract | `GargishClothWingArmor` from `Clothing/Cloaks.cs` → `ShadowCloakOfRejuvenation` | copy a class |

**Unblocks:** after it, CC9 holds **only patch work** (24 `upstream`: `NegativeAttributes`/`Brittle`/`NoRepair`
~10, SA weapon attributes 9, the two talisman slayer members, charm, masteries, `TempDamageAbsorb`, `CheckRemove`,
`RandomSuperSlayerAOS`), the 2 core-API files (`ImprisonedDog`, `AnkhPendant`), and collection-gated content. The row
can close and its tail belongs in `docs/patch-backlog.md`. Optional: add `ImprisonedDog`/`AnkhPendant` if their core
conversions (`IPooledEnumerable`, `DeathMoveResult.RemainEquiped`, `SpeechEventHandler`) check out in pinned. **I
have not verified them.**

**Cheaper because of D24: no.** D24 moved nothing in this batch, and it made two talismans read honestly as patch
work. **Cheaper because of P2: yes.** `Hats.cs`/`Pants.cs` stop needing a co-port of `BaseCollectionItem.cs`,
from a subsystem pinned lacks.

**The instrument's blind spot that matters here:** the same-graphic check runs only on *hidden* types of discarded
files, never on absent types inside candidate files. `MaleGargishClothLegs`, `OrcMask` and
`AncientShipModelOfTheHMSCape` were found by a scratch run of the same check over candidate files. Across the five
rows that run covers 1,050 absent item types: 96 same-graphic hits, 252 none found, 702 not run. Most are shared generic art (every deed is
0x14F0, every small fish 0x9CC), so a hit means **read it**, never "equivalent". Tonight's decimal fix made
`EtherealTiger` a twin of our `WhiteTigerFigurine`, which it plainly is not.

### Batch 2: CC7 furniture that carpentry and masonry make. 45 files, ~3,100 source lines, no patch

Every group-portable file whose **only** ServUO referrer is `DefCarpentry.cs` or `DefMasonry.cs`: 37 carpentry,
8 masonry. Fancy/plush couches and loveseats (10), shelves (4), long/wooden/metal tables (10), rustic benches,
display cases, plant tapestries, Ter Mur dressers, `UpholsteredChair`, `GargishBanner` (carpentry); gargish cots,
large gargoyle beds, `RitualTableAddon`, `GargishSculpture`, `GargoylePainting`, `GargoyleVase` (masonry);
`GargishCouch{East,South}Addon` (carpentry). `SoulForge.cs` is on the list (`DefCarpentry.cs:933`) and needs a
decision, because pinned has no imbuing, so it would be decoration only.

**The hook is not a patch.** `server/customizations/Engines/Craft/IncubatorCarpentryRecipe.cs` (P12, Q-053) already
appends to `DefCarpentry.CraftSystem` from `EventSink.ServerStarted`, argued in
`notes/cc6-followup-breath-incubator.md` §4. Pinned `DefMasonry` exposes the same `CraftSystem` property
(`Engines/Craft/DefMasonry.cs:22`). So the batch is the 45 types plus **two registration files**, one per craft
system, each `AddCraft` line copied from the ServUO table.

**Unblocks:** the registration file per craft system is what the other **24 craft-only files** reuse. They are named by
`DefTinkering` (13 of them), ServUO's `CraftItem.cs` (6; ours replaces that file), glassblowing, alchemy,
cartography, cooking, inscription, blacksmithy and tailoring. Some files are named by more than one. Without a hook, "drops straight in" ships items nobody can make, which is
exactly the shape P12 exists to prevent.

**Cheaper because of D24: no, none of the 45 moved. Because of P2: 6 of the 45** (gargish cots, couches, large
beds) were `unknown` on `#region Mondain's Legacy` and are drop-ins now.

**What the instrument cannot see here:** everything that makes this batch cost what it costs. "Named only by a
craft table" comes from a scratch reverse lookup, not the index. The index never read the `AddCraft` lines, so
their resources, skills, recipes and `SetNeededExpansion` gates are unwalked, and some may name resources that are
themselves unported (`WoodPulp`, `WorkableGlass` are in the craft-only 69). Walk the arrays before the first build.
`GargishLongTable*` and `GargoyleShortTableAddon` are drop-ins P2 freed but **no ServUO `.cs` names them**, so their
drop source is unknown and they are not in this batch.

### Batch 3: craft addons and distillation (New Magincia). 19 files, ~2,600 lines. The D24 dividend

`Items/Addons/Craft Addons/` (`CraftAddon`, `CraftAddonDeed`, `AddonToolComponenet`, `AlchemyStation`, `BBQSmoker`,
`FletchingStation`, `SewingMachine`, `SmithingPress`, `SpinningLathe`, `WritingDesk`), `Distillery.cs`, and the
whole of `Services/New Magincia/Distillation/`: `DistillationSystem`, `CraftDefinition`, `DistillationGump`,
`DistillationContext`, `BottleOfLiquor`, `LiquorBarrel`, `MetalKeg`, `WheatWort`.

**Why this one:** it is a whole small crafting system, and **D24 is the reason it is visible as one**. On the D20
instrument, 4 of its 7 distillation files were `unknown` on the system's own enum members (`Liquor.Brandy`,
`Group.WheatBased`, 11 names in all). That read as "open each file and find out". On D24 they are `in-row`, and the
group closes with **two remaining outside names, both ServUO core API**: `WorldSaveEventArgs`
(`DistillationContext.cs`) and `ToShortDateString` (`LiquorBarrel.cs`, a .NET `DateTime` method the index does not
know). `CraftAddon.cs` adds `Gumps` (a core member).

**Cheaper because of D24:** from "4 files to read before costing" to "portable as a group but for one save-event
conversion". I cannot put a line count on the saving. The honest statement is that D20 could not have proposed
this batch at all.

**Unblocks:** nothing further in these rows. It completes a system rather than feeding one.

**What the instrument cannot see here:** this batch is in the group **only if core-API names count as
conversions** (variant B in §4). Before the first build, confirm pinned's equivalent of
`EventSink.WorldSave`/`WorldSaveEventArgs` and of `Gumps`. `MetalKeg` is named only by `DefBlacksmithy`/`DefTinkering`
(batch 2's hook covers it), and `WheatWort` by `DefCooking`. How a player obtains a `Distillery` depends on the
craft-addon deeds' own craft entries, which have not been walked.

### Not proposed, and why

- **CC5 fishing is not cheap, and D24 did not change that.** `FishPies.cs` lost a false patch label, but the fishing
  core is still not portable as a group, even with core conversions and after simulating the loss of `Fish.cs`'s two
  guard branches (the `Caddellite` socket transfer, `Fish.cs:33-35`, and the `ShippingCrate` carve check, `:23`;
  pinned has neither item sockets nor the fisher quest). **The cluster reaches CC8's galleons**: `FishInfo.cs:57`
  registers `Charydbis` in the fish table, `Charybdis` derives from `BaseSeaChampion`, and that checks
  `boat is BritannianShip` (`BaseSeaChampion.cs:226`). It also needs `HookUses` and `LavaTiles`, members of pinned's
  own fishing classes (patches), and the harvest hook that makes rare fish catchable lives in ServUO's `Fishing.cs`,
  which pinned replaced. **`docs/tasks.md`'s "0% dependency" for CC5 is not true under this instrument.** It is a
  proposal-first job: three cuts, each a logged deviation, plus one patch to argue.
- **CC4 got no cheaper and is not one-dungeon-shaped yet.** D24 moved one cc4 file, towards `upstream` (`Reptile`,
  `AI_Necro`). 33 of 240 cc4 files are group-portable (42 with core conversions), spread across Exodus 12, Wrong 11,
  Covetous 8 and Blackthorn 2. `docs/tasks.md` wants one complete dungeon at a time, and none is complete.
- **The `BaseStatuette` hub** unblocks 15 cc7 statuettes (12 directly, 3 more through `ShimmeringEffusionStatuette`),
  `SpecialNaturalDye` and 4 artifacts files, which is the best unblock ratio of any one file in these rows. But
  reachability is poor. Four statuettes are named only by `ShimmeringEffusion.cs` (a peerless pinned lacks), eleven
  by no `.cs` file, `SpecialNaturalDye` only by BOD
  `Rewards.cs`, and 2 of the 4 artifacts files are Zoo/Library collection rewards that Q-064's rule keeps absent.
  Worth doing when the peerless are.
- **D24's rug and pond dividend** (`RoseRug`, `DolphinRug`, `KoiPond`) is veteran-reward content. It is named only
  by ServUO's `RewardSystem.cs`, which pinned replaced, so it needs a reward-table hook. Whether that can be additive
  like the craft hook is **not verified**.

### Already done, or not to be done, that the re-measure revealed

- **23 files already exist in pinned under an alias** (§2c). Four are new since the CC9 row: the cc7 spinning wheels.
- **`MaleGargishClothLegs`** (inside `Pants.cs`): pinned `GargishClothLegsType1`, same art. Do not port.
- **`AncientShipModelOfTheHMSCape`**: a renamed copy of pinned `ShipModelOfTheHMSCape`, reachable only from treasure
  chests.
- **Collection rewards**: `CollectionStatuettes.cs`, `CollectionsBritLibraryQuotes.cs`, and 5 types inside `Hats.cs`
  and `Pants.cs`. Q-064's rule keeps them absent.
- **`AI_NecroMage` is not a port** (Q-050), whatever Part D said.

---

## 4. The scratch analyses, and how far to trust them

None of these are the instrument. Each is a short script over its output, run tonight and not kept (P2 owns no new
tool files). The method is stated here so it can be rebuilt, and **§6 proposes folding the first two into the tool**.

- **Closure (portable as a group).** Start from all 702 candidates across the five rows. Repeatedly remove any file
  with an `extract`, `upstream` or `unknown` need, or an `in-row`/`elsewhere` need none of whose owners is still in the
  set. What survives: **290**. Variant B also lets through `unknown` names that ServUO *core* (`ServUO-pub57/Server`)
  declares, and 11 namespace/BCL names that Part D already read as such. It still blocks `AttachSocket`,
  `HasSocket` and `SpeedControlType`, which are subsystems, not conversions. Variant B gives **321**. By instrument:
  D20 271 / 292, D24 279 / 310, P2 290 / 321. D24 added `TrackInfo`, `DolphinRug`, `KoiPond`, `RoseRug`,
  `SpecialNaturalDye`, `Niter`, `SmugglersCache` and `SmugglersLiquor`, and removed none.
- **Reachability (reverse lookup).** For each of the 290, collect every ServUO file whose code names one of its
  absent types. The result: 97 named only by discarded files, 126 by a non-discarded file outside the group, 64 by
  nothing, 3 only inside the group. **Blind to non-`.cs` references** (`Data/` decoration and spawn files), so
  "named by nothing" is not "unreachable".
- **`unknown` what-if.** Of 45 `unknown` files on P2, 44 have only core, BCL or namespace names left. They would be
  13 drops, 11 co-port and 20 in-row if those names were conversions. The last one is `ExodusTomeAltar.cs`, whose
  `MemberRange` is a local variable. **That core names are conversions is a claim about each name, and I have not
  verified one of them in pinned.** Item sockets alone already show that some are not.
- **`upstream` what-if.** Of 84, 7 carry only recorded renames or `TimerPriority.OneSecond`: `Cora.cs`,
  `RobeofRite.cs`, `WrongBarredMetalDoor.cs`, `GooeyMaggots.cs` and `BrigandCannibalMage.cs` (cc4),
  `EnchantedGraniteCart.cs` and `PetParrot.cs` (cc7).

---

## 5. What changed in the tool, and the five `--legacy` numbers

**`--legacy`, re-confirmed after both changes, against the S9-era tree (ShatteredLegacy `b21bcd9`, 198 `.cs`):**
raw 1,022 → discarded **567** → candidates 455: drops **320**, in-row **81**, co-port **10**, upstream **44**.
**1,022 of 1,022 files in S9's bucket** (`compare-s9 artifacts`). Every legacy and pre-D24 row output on `8a52998`
is byte-identical to the run before the changes (JSON compared with `cmp`).

**Fix 5, preprocessor lines (fixed mode only).** `#region Mondain's Legacy` put `Mondain` into the file's names, and
nothing declares it. `FileInfo.idents_code` is the name set with every `#...` line removed. Fixed mode reads it on
both sides, ServUO and pinned/ours, and legacy keeps S9's `idents`. Effect: the 13 moves in §2b. On the
resolving side, 14 names exist in pinned/ours only inside preprocessor lines (`Stygian`, `Meteor`, `Helpers`,
`DEBUG`, ...). None changes a row. `Helpers` still resolves, through Medusa's generated `_helpers`: by name, as ever.

**Same-graphic check, decimal literals.** It now reads a first `: base(...)` argument written in decimal
(`base(40681)`), when that argument is the literal alone, at least two digits, and within the art range. So
`base(1)` (an amount) and `base(1094954)` (a cliloc; my first draft read three item types' clilocs as art) are not read. **It is
reporting only**, and no row changes. Artifacts hidden items: twin 5 / none found **24** / not run **19** (was 18 /
25). Whole tree: twin **25** / none found **57** / not run **54** (was 22 / 48 / 66). The three new whole-tree twins
are `BarrelOfBarley`/`ClosedBarrel`, `FlintsLogbook`/`ForestersLogbook` and `EtherealTiger`/`WhiteTigerFigurine`.
The last is plainly not an equivalent.

**The rest of the graphic check, left alone because it is not small:**

- **A later argument** (`GargishKiltOfMining`, `base(bonus, 0x030C)`): which argument is the graphic is a fact about
  the *parent's* constructor, not the call. Reading the first hex literal anywhere would misread
  `CompleteNecromancerSpellbook`'s `base((ulong)0x1FFFF)` (spell bits) as art. It needs parent constructors parsed
  and the `itemID` parameter located.
- **Inherited graphics** (18 artifacts types: `ZooMember*`, `LibraryFriend*`, the gargish artifact twins,
  `OdricsRobe`): walking the chain is mechanical, but **the answer would be wrong in kind.** `ZooMemberCloak`
  inherits `Cloak`'s graphic, so it would "twin" pinned's `Cloak`, and that says nothing about whether the named
  reward exists. For derived named variants, same art is the normal case, not evidence. Doing this right means
  comparing named leaf types against named leaf types, which the alias and type-name check already does.

**Tests:** 16 facts (14 before), about 15-35 s. The new facts are `test_preprocessor_lines_are_not_names_when_fixed`
and `test_graphic_check_reads_decimal_literals_in_art_range`. The D24 graphic fact now asserts two genuinely
not-run cases in place of the decimal one. **Each new fact goes red with its fix reverted on a scratch copy** (1
failure each), and is green with it.

---

## 6. What the instrument still cannot see, where it bears on the proposal

In order of how much it bears on §3:

1. **Reachability.** The index resolves what a file needs, never what needs the file. This is the largest gap for
   planning. 97 of the 290 group-portable files are orphans without a hook into a table pinned replaced. Batch 2's
   whole cost is here. **Proposed next instrument work:** a `reach` subcommand (the reverse lookup of §4) and a
   `closure` subcommand. Both are about 60 lines on existing data.
2. **Core declarations own nothing.** Unchanged from Part D, and now almost all of `unknown`: 44 of 45 files.
   Batch 3 rests on two of these names.
3. **Twins inside candidate files are never checked.** Batch 1's three read-before-port types were found by hand.
4. **Recorded equivalents are not encoded.** `EQUIV` holds S9's list. AGENTS.md's known traps (`SetWeaponAbility`,
   `SetSpecialAbility`, `SetAreaEffect`, `AI_NecroMage`) and `FruitsAndVegies` still read as `upstream`. Adding them
   would have to be fixed-mode only, since `EQUIV` is shared with legacy.
5. **Resolution is by name, not by owner.** `Helpers` (above), and Part D's five generated-name coincidences.
6. **Graphic check:** a later argument, and inheritance (§5).
7. **Capitalised locals** (`MemberRange`), and **BCL names** (`ToShortDateString`, `Distinct`, `Hashtable`) read as
   missing.
8. **Non-artifacts rows reproduce S9 at 94-99%**, so their S9 comparison lines are approximate.
9. **Nothing is compiled.** Every "drops straight in" is a static claim about names.

---

## Numbering

No D-number or Q-number taken. The correction to Part D's `AI_NecroMage` read is made in
`notes/index-blindspots.md`, with a pointer here.

## Reproducing this

```console
python -m unittest tools/test_content_index.py
python tools/content_index.py row <artifacts|cc4|cc7|cc7extra|cc5> --ours <export of 8a52998>/server/customizations
python tools/content_index.py row artifacts --legacy --ours <export of b21bcd9>/server/customizations   # 320/81/10/0/0/44
python tools/content_index.py compare-s9 artifacts --ours <export of b21bcd9>/server/customizations     # 1022 of 1022
python tools/content_index.py hidden artifacts                                                          # 5 / 24 / 19
```

The exports: `git -C D:\ShatteredLegacy archive <rev> server/customizations | tar -x -C <dir>`. The pre-D24
instrument is `git show af2e807:tools/content_index.py`. The D24-only instrument is the current file with
`use_code_idents=False` and `missing()` reading `f.idents`, which reverts fix 5 and nothing else.
