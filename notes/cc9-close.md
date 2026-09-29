# CC9 close: the reachability rule applied before the fact

2026-09-29. Brief: "close CC9. Eleven files, and one rule that decides what actually ships". Work is in
`D:\ShatteredLegacy`, **uncommitted, not deployed**, on top of P1's uncommitted D27/D28 files (not touched).

**Answer to the question you wanted measured, first:** of the **38** candidate types this batch named, **0** were
reachable in our tree as it stood. Not "half": none. That was always going to be literally true for unported types; the
question that matters is how many have a *near* path, and that is **27 of 38** (all through three gates: one boss and
two craft registrations). The other 11 are three collection rewards, two twins of pinned types (one found only by a
case-insensitive lookup), two with no source in any tree, three behind subsystems, and one extract whose only user is
among those.

**The systematic answer is worse, and it is not about this batch.** Reading the candidates turned up **18 types
already in our tree that no player can obtain**, on top of D32's thirteen: the whole Villainous Epiphany suite (12,
fixed here by its gate), five Virtue armour pieces, and `AudChar`. A rough tree-wide pass then found **219 item files
in `server/customizations` that no other file in our tree, pinned, our patches or the spawn data names** (§7). That is
an upper bound, and it needs reading, but 11 of 11 I sampled by hand are real orphans. **D32 was not an isolated miss.** It is
worth stopping to look at before batch 2.

---

## 1. The reachability table

"Our path" is what, in our tree today (after this batch where stated), puts the type in a player's hands. "ServUO
source" is every ServUO file that names the type other than its own, read, not counted from a tool.

| Type(s) | n | ServUO source | Our path | Outcome |
|---|---|---|---|---|
| `VirtuousEpiphany.cs`: Helm, Gorget, Breastplate, Arms, Gauntlets, Legs, Kilt, Earrings, GargishBreastplate, GargishArms, Necklace, GargishLegs `OfVirtuousEpiphany` | **12** | `Mobiles/Normal/Niporailem.cs:13-20` (`UniqueSAList`) and nothing else | **none before this batch.** Now: `Niporailem.UniqueSAList` (ours), spawned by pinned `Distribution/Data/Spawns/post-uoml/termur/TerMur.json:1252-1265` ("Spawner (602)" at [143,158,-20], 1 Niporailem), a file generated live (`docker/uo/SERVER.md:56`, Q-048) | **gated, small and near → ported with its gate** |
| `MysticBook` | 1 | `Misc/CharacterCreation.cs:1432`, `Mobiles/Normal/GargishRouser.cs:60`, `Services/Craft/DefInscription.cs:419`, `VendorInfo/SBMystic.cs:40,81` | **already reachable under another name**: pinned `MysticSpellbook` (`Items/Skill Items/Magical/MysticSpellbook.cs`) is the same class value for value (0x2D9D, OneHanded, `SpellbookType.Mystic`, offset 677, count 16) and pinned crafts it (`Engines/Craft/DefInscription.cs:457`) | **not ported: a twin.** CC9 batch 5 had already said so in `FallenMysticsSpellbook.cs:5-10` |
| `CorgulsHandbookOnMysticism` (ride-along) | 1 | `Services/Expansions/High Seas/Mobiles/Corgul/CorgulTheSoulbinder.cs`, `Services/PointsSystems/CleanUpBritanniaData.cs` | none; neither Corgul nor Clean Up Britannia is in either tree, and no spawn data names Corgul | **not ported: subsystem** (the High Seas Corgul encounter, or Clean Up Britannia). It would derive from `MysticSpellbook`, not `MysticBook`, when it comes |
| `NystulsWizardsHat`, `GypsyHeaddress` | 2 | `Services/CommunityCollections/MuseumDonationBox.cs:98-99` only (the Vesper Museum rewards) | none | **not ported: collection-gated.** The brief listed them as ports; they are exactly the Zoo/Library case |
| `JesterHatOfChuckles` | 1 | `MuseumDonationBox.cs:100` only | **already stock**: pinned `JesterHatofChuckles` (`Items/Special/Community Collection/`, lower-case "of"), same cliloc 1073256, luck 150, resists 12, 100 hits; `AssemblyHandler` resolves case-insensitively, so ServUO's name already resolves here | **not ported: a twin** (and collection-gated in ServUO) |
| `MalabellesDress` | 1 | `MuseumDonationBox.cs:70` only | none | **not ported: collection-gated.** Same |
| `OrcMask` | 1 | `Services/Craft/DefTailoring.cs:245`, `Misc/Loot.cs:411` (`HatTypes`) | **none before.** Pinned's `DefTailoring` crafts no mask at all, and pinned's `Loot.HatTypes` (`Misc/Loot.cs:313-319`) omits it. Now: tailoring, `Engines/Craft/OrcMaskTailoringRecipe.cs` | **gated, small and near → ported with its craft gate.** The loot half is not reproduced (§2) |
| `InstrumentedAddonComponent` (extract) + `CelloComponent/Deed/Addon`, `CowBellComponent/Deed/Addon`, `TrumpetComponent/Deed/Addon`, `WallMountedBell{South,East}{Deed,Addon}` | **14** | the four deeds: `Services/Craft/DefCarpentry.cs:613-636` only | **none before.** Pinned's carpentry has no King's Collection entries. Now: carpentry, `Engines/Craft/KingsCollectionCarpentryRecipes.cs` | **gated, small and near → ported with its craft gate** |
| `ShadowCloakOfRejuvenation`, `GargishShadowCloakOfRejuvenation` | 2 | **none.** No ServUO file names either type except its own (`[Alterable]` on itself) | none | **not ported: no source in any tree.** Porting it would be D32 exactly |
| `GargishClothWingArmor` (extract) | 1 | tailoring, `Mobiles/NPCs/Zhah.cs`, imbuing, two derived artifacts | its only reason to be in this batch was the cloak above | **not ported: no user in this batch.** It is a plain tailoring item on its own and belongs with the tailoring registration work (batch 2's "24 craft-only files") |
| `ImprisonedDog` | 1 | `Mobiles/Bosses/Travesty.cs:131`, `CleanUpBritanniaData.cs` | none; Travesty is Q-057's "leave" (no stock spawner, no altar) | **not ported: subsystem.** The optional core-API check (`IPooledEnumerable`, `RemainEquiped`) is moot |
| `AnkhPendant` | 1 | `Services/PointsSystems/VirtueArtifactsSystem.cs:22`, `CleanUpBritanniaData.cs`; its effect lives in ServUO `Misc/AOS.cs:860-891` (regen) | none | **not ported: subsystem** (a seasonal points system), plus an `AOS.cs` regen hook. `SpeechEventHandler` is moot |
| **Total** | **38** | | **0 reachable today; 27 with a near gate** | **27 ported, 11 not** |

Decided before I started, and confirmed rather than re-litigated: `MaleGargishClothLegs` (pinned
`GargishClothLegsType1`), `AncientShipModelOfTheHMSCape` (pinned `ShipModelOfTheHMSCape`), `ChefsToque` (Q-064), and
the five Zoo/Library types. A fact (`CC9CloseVerification`, Part D) now pins all of those, and the 11 above, as unported; the jester hat is pinned
as resolving to pinned's `JesterHatofChuckles`.

**The gates, and what they cost:**

| Gate | New files | Lines | What it reaches |
|---|---|---|---|
| `Niporailem` (`Mobiles/Normal/Niporailem.cs`) on batch 8's `BaseSABoss`, plus `NiporailemsTreasure` (`Items/Quest/`) | 2 | 242 + 77 | the 12 Virtuous **and the 12 Villainous already in our tree**, plus 4 shared artifacts already reachable elsewhere; fills one stock spawner that has been `InvalidType` since it was generated |
| `KingsCollectionCarpentryRecipes` (`Engines/Craft/`) | 1 | 82 | the four instrument deeds |
| `OrcMaskTailoringRecipe` (`Engines/Craft/`) | 1 | 59 | the orc mask, and through pinned's repair rule its tailor repair |

No patch. Both registrations use the additive pattern `IncubatorCarpentryRecipe.cs` established and argued
(`notes/cc6-followup-breath-incubator.md` §4b).

---

## 2. What was ported, gated, and left out

**Ported, 27 types in 7 files, plus 4 gate files (all under `server/customizations/`):**

- `Items/Artifacts/Equipment/Armor/Sets/Epiphany/VirtuousEpiphany.cs`: 12 pieces, generated from a table read off
  the ServUO file so the twelve bodies cannot drift. Bases are the ServUO bases (pinned `Plate*`, our `GargishPlate*`,
  `GargishEarrings`, `GargishNecklace`), the same parents ServUO uses, so **no re-parent and no final-parent question**:
  nothing here is a base class.
- `Items/Addons/InstrumentedAddonComponent.cs`, `Items/Equipment/Instruments/{Cello,Cowbell,Trumpet,WallMountedBell}.cs`.
  `InstrumentedAddonComponent` has three ServUO descendants (the three instrument components), none with a carrier
  member, so its parent is pinned's `AddonComponent`.
- `Items/Equipment/Clothing/OrcMask.cs`.
- Gates: `Mobiles/Normal/Niporailem.cs`, `Items/Quest/NiporailemsTreasure.cs`,
  `Engines/Craft/KingsCollectionCarpentryRecipes.cs`, `Engines/Craft/OrcMaskTailoringRecipe.cs`.
- Test: `server/tests/Items/CC9CloseVerification.cs`, 11 facts.

**Deviations and value decisions, each in its file's header:**

| Where | ServUO | Here | Why |
|---|---|---|---|
| `Niporailem` | `AI_NecroMage` | `AI_Mage` | Q-050 |
| `Niporailem` | `OnGotMeleeAttack(Mobile)` | `(Mobile, int)` | pinned's virtual; same body (Medusa's precedent) |
| `Niporailem` | `ColUtility.Free(Helpers)` | `Clear()` | ServUO's pooling helper; pinned has none |
| `NiporailemsTreasure.Link` | `AccessLevel.Decorator` | `GameMaster` | pinned has no Decorator (`Mobile.cs:135`); first build failed on it |
| instrument recipes | `typeof(Board)` | `typeof(Log)`, name 1044041 | the incubator's decision: every pinned wood entry does this, and `CraftItem` treats them alike |
| instrument recipes | `SetNeededThemePack(index, ThemePack.Kings)` | dropped | in ServUO only `CraftGumpItem.cs:107` reads it, to print one line; nothing refuses the craft. Pinned has no `ThemePack`. **Loss: one line of gump text** |
| orc mask recipe | cloth name 1044455 | 1044286 | what all 57 cloth entries in pinned `DefTailoring` use; label only |
| `OrcMask` | `IRepairable` / `RepairSystem` | dropped | pinned has no such interface; pinned repairs any clothing its craft system lists (`Repair.cs:407`), which the recipe now makes true |
| `OrcMask` | in `Loot.HatTypes` | **not in random hat loot** | pinned's `HatTypes` is a get-only static array that omits it (and `TribalMask`); extending it needs a patch to `Misc/Loot.cs`. Not done in a content batch: it changes a stock loot distribution. Reverses when a patch appends `OrcMask` to `Loot.HatTypes` (`Loot.cs:313-319`); reach: 1 item, in every random-hat drop on the shard |

**ServUO quirks copied, bug-list §3's kind (cosmetic, or behaviour ServUO has):**

- `EarringsOfVirtuousEpiphany` carries **1150262, the kilt's cliloc**; the Villainous earrings use their own (1150260).
- The four gargish Virtuous body pieces have **no `MageArmor`**; every Villainous piece does.
- `Niporailem.OnGotMeleeAttack` stops spawning spectral armour once **more than ten helpers are deleted** (not alive).
  His treasure timer and throw count are not saved.

---

## 3. Red, then green

Four `build.sh` runs before the final one, all `--tests-only` (`-t sl-modernuo:cc9-probe` / `cc9-red`), none of which
built an image. Logs `build1.log` to `build3.log`, `red.log`, `green.log` in the scratchpad `cc9/`.

- **Build 1**: builder stage red. `NiporailemsTreasure.cs(18,44): error CS0117: 'AccessLevel' does not contain a
  definition for 'Decorator'`. Fixed (§2's table).
- **Build 2**: production compiled; the test file did not (missing `using Server.Engines.Spawners`, four xUnit2031
  `Assert.Single(… .Where(…))`). Fixed.
- **Build 3**: 163 tests, 155 passed, **8 failed, and none of the 8 was a break I had made:**
  - **seven earlier facts** that pin the stock spawn-orphan count (`CC6Batch{1,2,3,4,5}CreatureVerification`,
    `CC6Batch7Verification`, `CC6Batch8Verification`): `Expected: 19 Actual: 18`. Niporailem left the unresolved list.
    They are built to move in step with each batch, so each now says 18 with a line saying why. That is these seven
    facts' red, watched: the count moved by exactly the one name this batch resolves.
  - **Part D**: `JesterHatOfChuckles resolves to a type`. A genuine finding, not a test bug: pinned ships
    `JesterHatofChuckles` (§5.4). The fact now asserts the name resolves to pinned's type.
- **Red run**: one deliberate break per fact, applied by a script from copies (`red.sh`), eleven facts expected red.
  **162 tests, 151 passed, 11 failed: exactly the eleven, each on its own break:**

```
  Failed CC9CloseVerification.TheTwelveVirtuousPiecesCarryServUOsValuesOnTheirStockBases
   Assert.Equal() Failure: Values differ  Expected: 1150262  Actual: 1150239        <- earrings' cliloc "fixed"
  Failed CC9CloseVerification.NiporailemConstructsWithServUOValuesAndNamesBothSuitesAsHisUniqueList
   Assert.Equal() Failure: Values differ  Expected: 24  Actual: 23                   <- one Virtuous piece off the list
  Failed CC9CloseVerification.EveryEpiphanyPieceComesOutOfNiporailemsUniqueRoll
   Assert.Equal() Failure: Values differ  Expected: 24  Actual: 23                   <- same break
  Failed CC9CloseVerification.ASpawnerWhereTheDataPlacesNiporailemFillsWithHim
   Spawn returned false with flags InvalidType, InvalidParams                        <- [Constructible] removed
  Failed CC9CloseVerification.NiporailemThrowsHisTreasureIntoTheCombatantsPackAndItTurnsToSandOutsideIt
   Assert.Equal() Failure: Values differ  Expected: 3823  Actual: 4586               <- turns to sand inside the pack
  Failed CC9CloseVerification.NiporailemsSpectralArmourIsHisSummonAndSurvivesASaveAndGoesWithHim
   Assert.True() Failure  Expected: True  Actual: False   (line 278, helper.Deleted) <- OnDelete forgets its helpers
  Failed CC9CloseVerification.TheFourInstrumentsAreCraftableUnderCarpentryInstrumentsWithServUOsCosts
   Assert.Equal() Failure: Values differ  Expected: typeof(Server.Items.Log)  Actual: typeof(Server.Items.Board)
  Failed CC9CloseVerification.EachInstrumentDeedBuildsItsAddonWhoseComponentPlaysItsSound
   Assert.Equal() Failure: Values differ  Expected: 1646  Actual: 1645               <- cowbell plays the cello's sound
  Failed CC9CloseVerification.AnInstrumentPlaysOnceASecondAndOnlyWithinTwoTiles
   Assert.True() Failure  Expected: True  Actual: False   (line 392, far player locked) <- range 3
  Failed CC9CloseVerification.TheOrcMaskIsTailoredUnderHatsAndIsNotTheOrcishKinMask
   Assert.Single() Failure: The collection did not contain any matching items        <- registration line removed
  Failed CC9CloseVerification.TheCandidatesThisBatchDeclinedResolveToNothing
   MysticBook resolves to a type                                                     <- the twin ported anyway
Total tests: 162   Passed: 151   Failed: 11
BUILD FAILED: ShatteredLegacy.Tests tests did not pass. No image was built.
```

  **One thing the red run shows that I did not set out to measure:** with `[Constructible]` removed, the seven
  orphan-count facts stayed green, because the name still resolves. A boss whose name resolves and who can never be
  spawned passes every earlier fact; only the new spawner fact catches it. The spawn-count facts measure names, not
  spawns.

  Restore: every file copied back from `final/`, `cmp` clean, and `grep -rn "CC9 RED" server/` empty before the green
  run.

**Green, the final files, full `build.sh`:**

```
[patches] structured customizations installed: 653 file(s).
[patches] shard tests installed: 31 file(s).
[patches] All 18 patches applied successfully.
Total tests: 162
     Passed: 162
Built sl-modernuo:latest with patches applied and 162 shard test(s) passing.
```

**162 = 151 + 11**: P1's 151 (`notes/test-host-truths.md`) plus this batch's 11 facts. The seven edited facts are among
the 151. No `sl-modernuo:cc9-probe` or `cc9-red` image exists afterwards (`docker images`), so every earlier run stopped
at its gate. The live `sl-modernuo` container is still on image `36cc709a82a6` and was not touched; the build moved
the `latest` tag only.

**Not proved here, the usual headless limits:** no instance was saved and reloaded by a running server (the round trips
go through `BufferWriter`/`BufferReader`, batch 8's shape), no client saw the gump lines, and the live world's
`TerMur.json` spawner was not read from the save (standing rule). Q-048 established the file was generated live; that
Spawner (602) specifically is in the save is inferred, not checked.

---

## 4. Does CC9 now hold only patch work? No.

Measured on the working tree after the port: `python tools/content_index.py row artifacts --ours
D:/ShatteredLegacy/server/customizations` gives **39 candidates** (the row was 44): 4 drops, 8 co-port, 1 extract,
2 unknown, 24 upstream. Then each file's absent types were reverse-looked-up in ServUO by hand (script and output in the
scratchpad, `reach.py`, `reach.txt`; every "source" below is a ServUO file I read, not a keyword hit). Effect-readers
such as `AOS.cs`, `BaseWeapon.cs`, `Rotworm.cs` are **not** sources and were set aside.

**Declined content, not work (7 files):** `MLDecorationArtifacts.cs` (the HMS Cape twin), `Hats.cs` (Zoo, Library and
museum rewards, `ChefsToque`, the jester twin), `Pants.cs` (Library and museum rewards, the `MaleGargishClothLegs`
twin), `MysticBook.cs` (twin), `ShadowCloakOfRejuvenation.cs` (no source), `ImprisonedDog.cs` and `AnkhPendant.cs`
(subsystem sources). Pinned by Part D's fact.

**Collection-gated (4 files):** `CollectionStatuettes.cs` (Royal Zoo), `MuseumStatues.cs` (Vesper), 
`CollectionsBritLibraryQuotes.cs` (the Library NPCs' collection), `MuseumWeapons.cs` (Vesper).

**The 24 `upstream` files are not "patch work" in the sense the brief means.** A patch would make them compile. It
would put **one** of them in a player's hands:

| What actually gates them | Files |
|---|---|
| Clean Up Britannia and/or the Virtue Artifacts points system | `LordBlackthornsExemplar`, `SentinelsGuard`, `DragonsEnd`, `JaanasStaff`, `KatrinasCrook` (both); `StaffOfShatteredDreams`, `ConjurersTrinket` (Clean Up only) |
| ServUO's treasure-chest artifact tables (pinned replaced `TreasureMapChest.cs`), plus Clean Up | `SurgeShield`, `RunedSashOfWarding`, `ManaPhasingOrb` |
| `AbyssalInfernal` (a boss neither tree has), plus Clean Up | `AbyssalBlade`, `DeathsHead` |
| Exploring the Deep's `Shadowlord` | `Craven`, `Equivocation`, `Pincer` |
| Gauntlet points / `Vrulkax` | `BowOfTheInfiniteSwarm`, `TheDeceiver` |
| a quest neither tree has | `VialofArmorEssence` (Zosilem tiered), `CandlewoodTorch` (`Missing`), `TalismanofGoblinSlaying` (`EscortToDugan`) |
| the Vesper museum | `MuseumWeapons` |
| Skill Masteries | `BookOfMasteries` |
| **nothing at all**: no ServUO file names it but `AOS.cs`, which reads it when worn | `SpellFocusingSash` |
| **carpentry** (`DefCarpentry.cs`, ServUO's SA block): a near gate, the same registration file as this batch's | `SnakeCharmerFlute` (plus its own charm patch) |

The co-port eight split the same way: 3 collection (above), `TragicRemainsOfTravesty` (Travesty, Q-057),
`Abhorrence`/`CaptainJohnesBlade` (Shadowlord), `AbyssReaver` (`Agralem`), `Glenda` (Gauntlet points).

**So what remains is:** 24 + 4 source-gated co-ports = **28 files whose blocker is a source first and a patch second**,
4 collection-gated files, 7 declined. For `docs/patch-backlog.md` that matters: if these move there ranked by how many
files each patch touches, the ranking will again be measuring compile-ability, not reach. `NegativeAttributes`/`NoRepair`
touches 6 files and reaches **none of them** without Clean Up Britannia or Virtue Artifacts. **Recommendation:** move the
tail, but carry the source column above with it, and rank by *patch plus source*.

**Clean Up Britannia is the single largest gate in sight.** It is named as a source by 12 of these 28, by
`ImprisonedDog` and `AnkhPendant`, by the Corgul handbook, and by 7 of the 11 orphans sampled in §7. It is the
subsystem to cost next by unblock ratio (`docs/subsystem-policy.md`). I have not costed it.

---

## 5. What §2 of the brief got wrong

P2 said its instrument could not see craft tables or loot, and it could not. Reading the files:

1. **`VirtuousEpiphany.cs` is 12 types, not 10.** Counted: 12 `class` lines, and Niporailem's list names 12.
2. **"Niporailem, which neither tree has" was true but pointed the wrong way.** It is not a subsystem: batch 8 §9 had
   already priced it as "an ordinary port on batch 8's base", and pinned's own spawn data places him. The bigger miss is
   that **our Villainous twelve share the gate** and were unreachable all along.
3. **`MysticBook` is not a port.** It is pinned's `MysticSpellbook` value for value, craftable in pinned, and CC9 batch 5
   had written exactly that in `FallenMysticsSpellbook.cs`. It "unblocks" nothing: Corgul's handbook would derive from
   `MysticSpellbook`, and the handbook is itself unreachable (Corgul).
4. **Three of the four hats are collection rewards, and the fourth is already stock.** `NystulsWizardsHat`,
   `GypsyHeaddress` and `JesterHatOfChuckles` are Vesper Museum rewards (`MuseumDonationBox.cs:98-100`), the Zoo/Library
   case exactly. And pinned already ships the jester hat as **`JesterHatofChuckles`** (lower-case "of",
   `Items/Special/Community Collection/`); `AssemblyHandler` ignores case, so ServUO's spelling already resolves on the
   shard. My own first case-sensitive grep missed it too; Part D's fact caught it in build 3 (§3).
5. **`MalabellesDress` is a museum reward too** (`MuseumDonationBox.cs:70`).
6. **`OrcMask` is a distinct item**, not a twin (header of `OrcMask.cs`). Its gate is a craft entry pinned's tailoring
   lacks, along with every other mask.
7. **The instruments' "drop source not checked"**: carpentry only, plus `SetNeededThemePack(ThemePack.Kings)`, which in
   ServUO is display-only.
8. **`ShadowCloakOfRejuvenation` has no source in ServUO at all**, so the `GargishClothWingArmor` extract had no reason
   to be in the batch.
9. **`ImprisonedDog` and `AnkhPendant`'s question was never the core API.** Their sources are Travesty, Clean Up
   Britannia and the Virtue Artifacts system.
10. **"After it, CC9 holds only patch work"**: not true, §4.
11. From batch 8 §9, not the brief: `NiporailemsTreasure` is not "dropped on death". It is thrown into an attacker's pack
    mid-fight.

**Net: the batch the brief sized as ~25 types from 11 files is 27 ported types (12 + 14 + 1) behind 3 gates.** It
shrank by the four museum items, the two twins and the cloak, and grew by the Virtuous count and the instruments'
13 addon types, which the brief counted as four files.

---

## 6. Found in passing: types already in our tree that no player can obtain

Each checked by grepping our tree, our patches, pinned and pinned's spawn data for the type name, then reading the
ServUO referrers.

| Types | n | ServUO source | Status |
|---|---|---|---|
| the 12 `*OfVillainousEpiphany` (ours since CC9 batch 5) | 12 | `Niporailem.cs` only | **fixed by this batch's gate.** Were unreachable for the whole time they have been in the tree |
| `CompassionArms`, `JusticeBreastplate`, `HonestyGorget`, `HonorLegs`, `SacrificeSollerets` | 5 | `VirtueArtifactsSystem.cs`, `CleanUpBritanniaData.cs` | **unreachable.** Pinned's own `SpiritualityHelm` and `ValorGauntlets` are reachable (pinned `HeritageTokenGump.cs`); our five are not in it |
| `AudChar` (ours since batch 5) | 1 | `DefCarpentry.cs` (SA block), `SBTinker.cs` | **unreachable.** One `AddCraft` line in `KingsCollectionCarpentryRecipes`'s shape would reach it. Not done: outside the brief |
| `LordBritishThroneAddon`/`Deed` | 2 | `MuseumDonationBox.cs` only | **collection-gated content already shipped**, the Q-064 rule's case |

That is **18 unreachable types found without looking for them** (12 now fixed), plus 2 collection-gated, beside D32's
13. Also, not an orphan but a gap of the same family: **pinned's tailoring crafts no mask at all**, while ServUO crafts
five and pinned declares the other four (`BearMask`, `DeerMask`, `TribalMask`, `HornedTribalMask`). Stock types;
`OrcMaskTailoringRecipe` is the place four more lines would go, if Chase wants the stock table to match.

---

## 7. The tree-wide measure: is D32 systematic?

A rough pass, not a finding (`orphans.py` in the scratchpad): every `.cs` file in `server/customizations` whose declared
types are named by **no other file** in customizations, `server/patches`, pinned `Projects`, or pinned
`Distribution/Data` (spawn JSON and configs), word match, case-insensitive.

- **263 of 768 files.** Removing what is obviously reached another way (the ten top-level `ClusterF*`/tools files,
  registered by `Configure`; the two ML quest files; the 32 staff costume `Suits`, GM-only by design) leaves
  **219 item files**. The list is `orphan-items.txt` in the scratchpad; by directory: `Items/Artifacts/Equipment` 132,
  `Items/Artifacts/Decorative` 28, `Items/Equipment/Weapons` 20, `Items/Equipment/Armor` 14, `Items/Equipment/Jewelry`
  11, consumables 6, other 8.
- **It is an upper bound.** It cannot see a type reached through a base-type pick, through reflection, or by a
  `typeof` list inside its own file. It does not count what pinned's random loot constructs.
- **But the sample says it is mostly real.** 11 picked by hand across the set, armour and decorative directories (not a
  random sample), sources read in ServUO: **11 of 11 have no source in our tree.** Knights, Scout, Sorcerer, Bestial and Luck set pieces: Clean Up Britannia rewards (7 of the
  11). Aloron's set: Time of Legends. Darkwood: carpentry (a near gate). `CuffsOfTheArchmage`: tailoring and a Ter Mur
  vendor. `WhiteTigerFigurine`: the stealable-artifacts spawner. `KelpWovenLeggings`: fishing, treasure chests, Clean Up.

**So D32 was not an isolated miss.** Up to 219 of 768 files (29%, an upper bound) may be in no player's reach, and the
largest single cause is one subsystem. This is the stop-and-look the brief asked about. The instrument P2 proposed
(`content_index.py reach`, backlog-remeasure §6.1, ~60 lines) is the right tool to make the 219 exact, and it should
run before batch 2 ships another 45 files.

---

## Files

`D:\ShatteredLegacy`, uncommitted:

- new, `server/customizations/`: `Items/Artifacts/Equipment/Armor/Sets/Epiphany/VirtuousEpiphany.cs`,
  `Mobiles/Normal/Niporailem.cs`, `Items/Quest/NiporailemsTreasure.cs`, `Items/Addons/InstrumentedAddonComponent.cs`,
  `Items/Equipment/Instruments/{Cello,Cowbell,Trumpet,WallMountedBell}.cs`, `Items/Equipment/Clothing/OrcMask.cs`,
  `Engines/Craft/KingsCollectionCarpentryRecipes.cs`, `Engines/Craft/OrcMaskTailoringRecipe.cs`
- new test: `server/tests/Items/CC9CloseVerification.cs` (11 facts)
- edited tests, one assertion and one comment line each, 19 to 18: `server/tests/Mobiles/Normal/CC6Batch{1,2,3,4,5}CreatureVerification.cs`,
  `CC6Batch7Verification.cs`, `server/tests/Mobiles/Bosses/CC6Batch8Verification.cs`
- P1's uncommitted D27/D28 files were in the tree before this task and were not opened for writing.

## Not done, and why

- **Not committed** (brief section 5). **Not deployed**; no container started, stopped or restarted.
- **`docs/` not touched.** For promotion: D32's row should gain section 6's 18 (12 fixed here); the CC9 row in
  `docs/tasks.md` should not close as "only patch work" (section 4); `docs/patch-backlog.md` should carry section 4's
  source column.
- **`tools/progress.py` not run**, for P1's reason: it rewrites `README.md` and `tools/progress.json`, both already
  modified in this working tree by other tasks. Run it once, by whoever commits.
- **Not ported although near:** `AudChar` (one carpentry line), the four stock masks' tailoring entries,
  `SnakeCharmerFlute` (carpentry plus a charm patch), `GargishClothWingArmor` (tailoring). All outside the brief.
- **`OrcMask` in random hat loot** needs a patch to pinned `Misc/Loot.cs` (section 2). Not argued here: a content batch
  should not change a stock loot distribution. It belongs with the section 4 patch-backlog move.

## Scratch

In this session's scratchpad (`...\scratchpad\`), not committed: `gen_virtuous.py`, `gen_instruments.py` (the
generators), `cc9/red.sh` and `cc9/final/` (the red breaks and the copies they were restored from),
`cc9/build{1,2,3}.log`, `cc9/red.log`, `cc9/green.log`, `cc9/row-after.txt` (the row), `cc9/reach.py`/`reach.txt`
(section 4), `cc9/orphans.py`/`orphans.txt`/`orphan-items.txt` (section 7).
