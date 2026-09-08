# CC9 — Artifacts and equipment: batch 1, and the row re-costed

**Status: four batches ported (245 files, 251 types), each built green through `build.sh` (batch 4
after one failed cycle) and headless-verified. The row is NOT "88% needs nothing built". Partial row
with an honest boundary; batch 3 is §13, batch 4 is §14, what remains is §14.9.**

Task CC9 (`C6` in the status table). Brief: test S9's "320 drop straight in" claim with a real
build, batch the work, report the real per-batch cost, deliver the gargoyle files, cost
`ReforgedSuffix`, log deviations, and stop cleanly when context runs out.

---

## 1. The headline

**S9's static resolution was right about compilation and wrong about "nothing built".**

- **Batch 1: 31 ServUO files (34 types, 2,604 lines in, 1,324 lines out) compiled green on the
  first `build.sh` run.** Zero compiler failures. But that is because a pre-flight pass against
  `D:\UO\ModernUO-pinned` caught, before the build, **8 of the 31** that would not have compiled
  as a mechanical conversion, plus **3 more that S9 listed and I did not port at all** because
  ModernUO already ships them under other names. So the honest "drops straight in" rate on this
  sample is **20 of 34 (59%)**, not 100%.
- **18 of the 320 are not candidates.** ModernUO already declares the gargish cloth, leather
  and stone armour families as `Gargish<Material><Slot>Type1/Type2` (32 types, same item IDs,
  `Items/Armor/{Cloth,Leather,Stone,Studded}/`), and `SerpentstoneStaff` (lower-case *s*) is
  ServUO's `SerpentStoneStaff`. S9's filter matched names; these match by content. §4.
- **113 of the 320 need something built or re-parented**: 83 set-armour pieces must be
  re-parented onto S1's `BaseSetArmor` (a transformation, not a decision), 13 set pieces sit on
  bases that have no set carrier at all, and 17 assign absorption attributes onto bases that
  have no absorption carrier. The carrier family S1 and S6 both deferred is now the gate on 30
  files in this row, and the same family is the no-patch route for `ReforgedSuffix`. §5.
- **Corrected row picture: 455 candidates → 437 real; of those, 272 (62%) need nothing built
  (189 plain + 83 re-parented set armour), 30 need a carrier, and the rest are S9's other
  buckets unchanged.** §4. The brief's 88% is a name-count figure; this is a build-and-read figure.
- **A gated build cycle costs 86 seconds on this machine, not 266.** §8, with the log.
- **Docker Desktop would not start, twice, because of stale AF_UNIX socket files.** The fix is a
  two-folder rename before launch; 30 minutes of the task went to it. §10, and Q-036.

---

## 2. What was ported — batch 1 (31 files, 34 types)

All under `D:\ShatteredLegacy\server\customizations\Items\<ServUO-relative path>`. Every type
verified registered in the shipped `UOContent.dll` by reflection (§9): generated
`Serialize`/`Deserialize` and a `(Serial)` constructor on all 33 concrete-or-base types.

| Category | Files | Notes |
|---|---|---|
| Gargoyle wearables (the row's share of the cluster) | `GargishGlasses`, `GargishPlateChest`, `GargishPlateLegs`, `GargishEarrings`, `GargishNecklace` (+`GargishAmulet`, `GargishStoneAmulet`), `GargishGnarledStaff`, `GargishKatana`, `GargishDagger`, `LargeStoneShield` | 9 files. `RequiredRace => Race.Gargoyle` becomes ModernUO's `RequiredRaces => Race.AllowGargoylesOnly` on armour/weapons/shields (`Item.cs:2110`); `CanBeWornByGargoyles` dropped (D-2) |
| Consumables | `ElixirofAgapiteConversion`, `GobletOfCelebration`, `GrapeBunch`, `InfusedAlchemistsGem` | Goblet has real persisted state: `Full` via `[SerializableProperty(0)]`, refill time via `[DeltaDateTime] [SerializableField(1)]`, timer rebuilt in `[AfterDeserialization]` |
| Decorative | `BakeKitsuneStatue`, `CoffinPiece`, `CreepingVine` | trivial |
| Armour artifact | `AnimatedLegsoftheInsaneTinker` | derives from stock `PlateLegs`, unchanged |
| Clothing artifacts | `CloakOfDeath`, `TheScholarsHalo` | unchanged |
| Jewellery artifacts | `AmuletOfRighteousness`, `Venom` | Amulet implements ModernUO's `IUsesRemaining`; the uses line moves from ServUO's `AddUsesRemainingProperties` hook (absent) to `GetProperties`, where ModernUO's own charged items put it |
| Spellbook artifact | `ClaininsSpellbook` | unchanged |
| Weapon artifacts | `AxeOfAbandon`, `BansheesCall` | Axe loses `BattleLust` (D-3). Banshee's `Velocity` ports: ModernUO keeps it on `BaseRanged`, and `BaseThrown : BaseRanged` |
| Instrument artifact | `DreadFlute` | unchanged |
| Tool artifact | `XenrrFishingPole` | body-mod on equip ports; its two AOS attributes do not (D-4) |
| Set armour, Acolyte set | `GreymistArms/Chest/Gloves/Legs` | re-parented from stock `Leather*` onto `BaseSetArmor`, stock members reproduced (S1's TigerPelt shape) |
| Costume base | `BaseCostume` | `BaseShield` subclass with two persisted ints; unblocks the 34 costumes in the in-row bucket. Loses the knock-off-on-damage hook (D-5) |

Every file carries a header comment naming its ServUO source and any deviation.

### 2b. Batch 2 — 40 files, 41 types: the costumes and the artifacts batch 1 unblocked

| Category | Files | Notes |
|---|---|---|
| Costumes | the 33 `Items/Equipment/Suits/*Costume.cs` | One template: `CostumeBody`, one `CostumeHue` (`ShadowWyrm`), `CreatureName`, and a `LabelNumber` (31) or `DefaultName` (2: `DragonWolf`, `SabertoothedTiger`). Generated from the ServUO values by a 40-line script that refuses any file whose constructor or overrides differ from the template; it refused none. Values checked back against the ServUO grep in §12 |
| Artifacts on batch-1 or ModernUO gargish bases | `CastOffZombieSkin` (: `GargishLeatherArmsType2`), `CuffsOfTheArchmage` (+ `GargishCuffsOfTheArchmage` : `GargishStoneArmsType1`), `PillarOfStrength` (: `LargeStoneShield`), `BreastplateOfTheBerserker` (: `GargishPlateChest`), `GiantSteps` (: `GargishStoneLegsType1`), `Glasses`, `NightEyes` | `Glasses` drops ServUO's `[Alterable]` (no `AlterItem` in ModernUO, S9 §4) and `IRepairable`; its ML-client `CanEquip` check ports (`NetState.SupportsExpansion` exists, `NetState.ClientVersion.cs:92`) |

**Result: green on the first `build.sh` cycle, 95 s, 27 tests; `structured customizations
installed: 154 file(s)` (114 + 40); 41 of 41 types reflected with generated serialization;
headless fresh save and reload both clean (§9, runs 3 and 4).** Pre-flight for this batch was
the batch-1 findings applied: the two ModernUO parents renamed, `Alterable` and `IRepairable`
dropped, everything else standard.

---

## 3. The claim, tested: what "drops straight in" hid

The brief asked how many of the supposedly-clean files fail and why. **None failed the compiler,
because none reached it un-checked.** Here is what the pre-flight found, file by file, and what
each would have been at the compiler:

| File | What S9's name scan could not see | Would it have compiled? |
|---|---|---|
| `GargishClothArmor.cs` (8 types), `GargishLeatherArms.cs`, `GargishStoneChest.cs` | Already in ModernUO as `Gargish*Type1/Type2`, same item IDs | **Yes**, and produced duplicate items under second names. Not ported |
| `GreymistArms/Chest/Gloves/Legs` | `SetHue`, `SetAttributes`, `SetSelfRepair`, `Set*Bonus` are members of ServUO's `BaseArmor`; ModernUO's has none of them. S9 saw `SetID` and bucketed these as clean because S1's carrier exists — but the carrier is a *different parent* | **No**, 4 files. Re-parented |
| `XenrrFishingPole` | `Attributes` on ServUO's `FishingPole`; ModernUO's is a plain `Item` | **No**. Attributes dropped, D-4 |
| `AxeOfAbandon` | `WeaponAttributes.BattleLust`; not in ModernUO's `AosWeaponAttribute` | **No**. Dropped, D-3 |
| `GargishEarrings`, `GargishNecklace` | override `GetDurabilityBonus()` and `ApplyResourceResistances()`; neither is virtual in ModernUO | **No**, 2 files. Both overrides are inert here (Iron registers `CraftAttributeInfo.Blank`), dropped, D-6 |
| `GargishGlasses` | `IRepairable` / `RepairSystem`; ModernUO's `Repair.cs` dispatches on `BaseArmor` and has no such interface | **No**. Dropped, no behaviour change |
| `BaseCostume` | `OnDamaged` is called from ServUO's `AOS.Damage` (`AOS.cs:417`); ModernUO has no call site | Yes, silently inert. D-5 |
| the other 17 | standard conversion only | Yes |

So on a 34-type sample: **20 needed only the standard conversion, 8 needed a real change to
compile, 3 must not be ported, 3 compile but lose behaviour.** A mechanical pass over this
batch would have produced one failed 86-second build cycle with about nine distinct errors.

Two more the whole row shares, both handled once (D-1, D-2): **`IsArtifact`** (208 of the
320 files) and **`CanBeWornByGargoyles`** (70 of the 320). Zero readers of either in pinned
ModernUO, verified by grep over `Projects/`.

Pre-flight method, for the next batch: for every candidate, check (1) base class exists,
(2) every `override` name is declared `virtual`/`abstract` somewhere in the pinned tree,
(3) every `X.Y =` attribute member is in the matching `Aos*Attribute` enum in `Misc/AOS.cs`,
(4) the base ItemID is not already the base ItemID of a ModernUO type (`itemid_xcheck.py`,
reproduced in §12), (5) `SetID`/`AbsorptionAttributes` presence. Steps 1–3 took under a minute
for 31 files as greps; step 4 is a 20-line Python script.

---

## 4. The 320 "drops straight in", re-bucketed by reading

Counted, not described. File lists in §12.

| Bucket | Files | What it costs |
|---|---|---|
| **Already in ModernUO by content** | **18** | Nothing — remove from the row. 17 gargish cloth/leather/stone armour files (incl. the 8-type `GargishClothArmor.cs`) map to ModernUO's 32 `Gargish…Type1/Type2` classes; `SerpentStoneStaff` is `SerpentstoneStaff`. Their in-row dependants (`CastOffZombieSkin`, `CuffsOfTheArchmage`, `GiantSteps`, `BestialArms`, `PetrifiedSnake`, `SpinedBloodwormBracers`) derive from the ModernUO type instead — a name change, not a port |
| **Plain** | **189** | Standard conversion. Known holes inside it: `BattleLust` ×3, `ArmorAttributes.SoulCharge` ×2, `Attributes.LowerAmmoCost` on a bow ×1 (`RunedDriftwoodBow`; ModernUO keeps it on `BaseQuiver`) and on a belt ×1 (`FirstAidBelt`), `TalismanSkill` ×1 (`CollectionsBritLibraryTalismans`), attributes on `FishingPole` ×1. Each is a logged omission, not a block |
| **Set armour** | **83** | Re-parent onto `BaseSetArmor`, reproduce the stock parent's ~10 members. Transformation, ~10 extra lines and one stock-file lookup per file. 6 Initiation pieces also set `Attributes.Brittle`, which ModernUO's `AosAttribute` lacks — omission each |
| **Set pieces with no carrier** | **13** | Need `BaseSetJewel` (4: the Luck set rings and bracelets), `BaseSetClothing` (4: `HumilityCloak`, `SacrificeSollerets`, `SorcererHat`, `VirtuososCap`), `BaseSetWeapon` (2: `Evocaricus`, `Swiftflight`), `BaseSetQuiver` (1: `Feathernock`), a shield carrier (1: `MalekisHonor` — `BaseShield` is a `BaseArmor` but not a `BaseSetArmor`), plus `BeastialSetHelper` (a `Timer`, needs reading) |
| **Absorption users with no carrier** | **17** | S6 built `SAAbsorptionAttributes` and put it on `BaseSetArmor` only. These 17 are 8 non-set armour (re-parent onto `BaseSetArmor` works — it carries absorption already), 1 shield, 1 clothing, 2 jewellery, 4 weapons, 2 talismans (which S6 §4 says would not aggregate even on ServUO). Alternative: port with the line dropped, as S1 did for Aloron before S6 |

**Corrected: 455 → 437 real candidates. 272 need nothing built (62%), 30 need the carrier
family, the 81 / 10 / 44 S9 buckets are otherwise as S9 measured them** with one correction
to the in-row 81: batch 1 plus ModernUO's gargish types satisfy the *named* dependency of 53
of them (34 costumes on `BaseCostume`, 19 on gargoyle names), but reading the 19 shows that
**6 of them also assign `AbsorptionAttributes`** (`BritchesOfWarding`, `PetrifiedSnake`,
`StoneDragonsTooth`, `DragonJadeEarrings`, `ObsidianEarrings`, `SpinedBloodwormBracers`) and
**5 are set pieces on gargish jewellery** (`VirtuososEarpieces`, `VirtuososNecklace`, the three
`Bestial*`), so they join the carrier-blocked group. S9's in-row bucket never checked members
beyond the one that put the file there. **Truly unblocked: 34 costumes + 8 artifacts = 42**,
and 41 of those are batch 2 (§2b).

---

## 5. The carrier family, and `ReforgedSuffix` — one decision, costed, not taken

Three things in this row and one in CC4 all want the same four classes:

| Wants a carrier for weapons / jewellery / clothing / quivers | Files |
|---|---|
| Set pieces on non-armour bases (§4) | 13 here |
| Absorption on non-armour bases (§4, S6 §6's "31 one carrier away") | 9 here (17 minus the 8 armour that `BaseSetArmor` already covers) |
| `NegativeAttributes` (S9 §5.1) | 8 |
| **`ReforgedSuffix`** (S9 §5.2, CC4) | **110, or 141 with the gargoyle wearables** |

**What `ReforgedSuffix` is, from the source** (`ServUO Services/LootGeneration/RunicReforging/
RunicReforging.cs:31-52, 1704-1742`): a 19-value enum stored as one int on `BaseArmor`,
`BaseWeapon`, `BaseJewel` and `BaseClothing`, rendered in the name line. Twelve values render
through cliloc 1151758 (`~1_ITEM~ of ~2_SUFFIX~`) with a suffix cliloc from an 18-row table;
the six dungeon values (`Blackthorn` 1154548, `Minax` 1154507, `Kotl` 1156900, `Khaldun`
1158672, `Doom` 1155589, `EnchantedOrigin` 1157614) render through their own cliloc with the
item name as the argument. 136 of the 138 CC4 hits are `ReforgedSuffix = ReforgedSuffix.X;`
in a constructor; the two real uses are the reforging gump and `MysteriousWisp`, neither in
scope. **In this row: zero of the 320 reference it.**

Three routes, costed:

| Route | Cost | Frees | Patches / migrations |
|---|---|---|---|
| **A. Delete the line** | 0 | CC4's 136 port as plain files | none; **136 name-line deviations** logged once as a class ("dungeon artifacts lack their *of Blackthorn* suffix"). Player-visible: the wiki name has the suffix |
| **B. S9's patch route** | ~60 lines (enum + name table + two methods) + a field on 4 upstream base classes | 110 / 141 | **4 patches that bump upstream `[SerializationGenerator]` versions, 4 migrations.** This is exactly what S1 decided *not* to do for set state (`BaseSetArmor` exists because of it), so B contradicts a standing decision |
| **C. Carrier route** | ~60 lines of naming + a `_reforgedSuffix` field on **each carrier**: `BaseSetArmor` (exists, +1 field), `BaseSetWeapon`, `BaseSetJewel`, `BaseSetClothing`, `BaseSetQuiver` (new). Measured against `BaseSetArmor` at 394 lines including absorption, and with `SetHelper` and the AOS patch already dispatching on `ISetItem` / `BaseWeapon` / `BaseJewel` / `BaseClothing` / `BaseQuiver` (`SetItem.cs:62-78`, `AOS-set-attribute-aggregation.patch:10`), **~250 lines per carrier, ~1,000 total, 0 patches, 0 migrations** | 110 / 141 **plus the 30 carrier-blocked files here plus `NegativeAttributes`' 8** | none. Every reforged item derives from a carrier instead of its stock parent — the same re-parent transformation the 83 set-armour files need anyway |

**Recommendation to surface, not settle:** C is the only route consistent with S1 and S6, and
it is the same work three earlier tasks deferred. It is a subsystem task, not a content batch
(`docs/subsystem-policy.md`), and it needs a test per carrier that a set bonus and an eater
both fire through a weapon and a jewel. Do it as its own S-task before CC4, or take route A
for CC4 and accept the 136 logged names. **Not built here**, per the brief. Raised as Q-037.

---

## 6. The gargoyle wearables cluster, re-counted

S9 §6: "9 of the 14 gargoyle files are candidates in this row". Read against ModernUO:

| S9's nine | Status |
|---|---|
| `GargishGlasses`, `GargishPlateChest`, `GargishPlateLegs`, `GargishEarrings`, `GargishGnarledStaff`, `GargishKatana` | **Ported, batch 1** |
| `GargishClothArmor.cs`, `GargishLeatherArms`, `GargishStoneChest` | **Already in ModernUO** (`Gargish…Type1/2`). Not ported |
| S9's five extract donors (`Cloaks.cs`, `MiddleTorso.cs`, `OuterLegs.cs`, `Shirts.cs`, `Waist.cs`) | untouched; still 7 extracts (`GargishRobe`, `GargishFancyRobe`, `GargishClothKilt`, `GargoyleHalfApron`, `GargishClothWingArmor`, … ) |

Also ported alongside because in-row files need them: `GargishNecklace` (3 types), `GargishDagger`,
`LargeStoneShield`. **So the cluster is 6 ported + 3 already present + 7 extracts remaining**, and
the "+24 with the ReforgedSuffix carrier" overlap is reachable for the 7 extracts, as S9 said.

---

## 7. Deviations — for `docs/fidelity-principle.md`

Each: what a player notices, what reverses it.

| # | Deviation | Player notices | Reverses when |
|---|---|---|---|
| **D-1** | `IsArtifact => true` dropped from every file in this row (208 of 320 carry it) | Nothing. Zero readers in pinned ModernUO; every ServUO consumer (`BasePigmentsOfTokuno`, `NaturalDye`, `AlterItem`, `RunicReforging`, `ArcaneGem`) is absent | Pigments of Tokuno or `AlterItem` is ported |
| **D-2** | `CanBeWornByGargoyles => true` dropped (70 of 320). The race gate itself is kept via `RequiredRaces` | Nothing. Zero readers in ModernUO | never needed |
| **D-3** | `AxeOfAbandon` loses `WeaponAttributes.BattleLust = 1` | The axe's tooltip lacks Battle Lust and the effect never fires. Same will apply to `ClawsOfTheBerserker`, `StormCaller` | `BattleLust` is built into `AosWeaponAttribute` and `BaseWeapon.OnHit` (a patch) |
| **D-4** | `XenrrFishingPole` loses `SpellChanneling = 1`, `CastSpeed = -1` | Casting while holding it clears hands, as with a normal pole | Either an `AosAttributes` field on the pole **and** an `IAosItem` arm in `AosAttributes.GetValue` (`AOS.cs:505-575`, one patch, ~4 lines), or ModernUO gives `FishingPole` attributes |
| **D-5** | `BaseCostume` (and all 34 costumes) stays on when the wearer takes damage; ServUO knocks it into the backpack from `AOS.Damage` | A masked player keeps the mask through combat | One line at ServUO's call site in `AOS.Damage`; `AOS-damage-eater-hook.patch` already touches that method, so it is a +1 to an existing patch |
| D-6 | `GargishEarrings`/`GargishNecklace` drop two non-virtual overrides | Nothing: Iron's `CraftAttributeInfo` is `Blank`, so the resource terms they suppressed are zero | paper only |
| D-7 | `GreymistGloves` is not `IArcaneEquip` | Nothing: an artifact glove is never crafted arcane | paper only |
| D-8 | `GobletOfCelebration` clamps a negative refill delay to zero after a load; `DateTime.Now` → `Core.Now` | Nothing observable | paper only |
| D-9 | `BaseCostume.OnRemoved` calls `base.OnRemoved` once; ServUO calls it twice | Nothing | paper only |
| **D-10** | `GargishWarHammer` flips to `0x48C1`, not ServUO's `0x481` | Nothing a player would call wrong: `0x481` is a Prism of Light pillar graphic and every other gargish weapon flips to itemID+1, so ServUO's value is a typo that would have turned a flipped war hammer into a pillar | never; ServUO's is the bug |
| D-11 | `EvilOrcHelm` drops `UseIntOrDexProperty` / `IntOrDexPropertyValue` | Nothing: both are `BaseArmor` virtuals with zero readers in ServUO (grep over `Scripts/` finds only the declaration and this file). The -10 int-or-dex swap in `OnEquip`/`OnRemoved` is kept | paper only |
| D-12 | `OrcishBow` shows one durability line (1060410) where ServUO shows two | ServUO's `BaseWeapon.GetProperties` also emits 1151780 ("durability +~1_VAL~%") for `DurabilityBonus`; pinned ModernUO's emits nothing for weapons, so the bow's own `AddWeightProperty` line is the only one. One line instead of two saying the same thing | paper only |
| D-13 | `StaffRing` tests `AccessLevel == Player` instead of ServUO's `Mobile.IsPlayer()` | Nothing. **Stated cause corrected in batch 4 (Q-040):** ServUO's `IsPlayer()` is `AccessLevel <= AccessLevel.VIP` (`Server/Customs Framework/Utilities/Utilities.cs:51`), not `== Player`; the port is still exactly right because pinned ModernUO's `AccessLevel` enum has no `VIP` member (`Mobiles/Mobile.cs:135-144`), so `== Player` is the precise equivalent. Note the ring is not OSI content at all: a ServUO staff tool ("By Nerun") ported because it was on the list | paper only |

D-1 and D-2 are logged **once for the whole row**, per the brief; they will not be repeated per
file or per batch.

---

## 8. What a batch actually costs

Wall clock, 2026-09-08 local, this machine (Docker Desktop 4.75, engine 29.5.2, WSL2).

| Phase | Elapsed | Note |
|---|---|---|
| Orientation: `AGENTS.md`, `docs/README.md`, `fidelity-principle.md`, CC9 in `tasks.md`, S9 §1–9 and the appendix lists, `port-recipe.md`, existing ports | ~10 min | |
| Docker Desktop down, diagnosed, fixed (§10) | **~30 min**, overlapped | pre-flight and file writing ran during the waits, so the pure loss is nearer 10 min |
| Pre-flight for 34 types: base classes, overrides, enum members, item-ID cross-check, the 18 duplicates, the set/absorption buckets over all 320 | ~15 min | this is where the value was |
| Writing 31 files | ~15 min | ~30 s a file for the plain ones; the three with persisted state and the four re-parented set pieces took most of it |
| **`build.sh` gated cycle** | **86 s** | builder stage 41 s of which `dotnet publish` 27.3 s; tests 27 passed; runtime image. Log: `build-batch1.log` in the task's work folder. `[patches] structured customizations installed: 114 file(s)` (83 + 31) |
| Reflection over 33 types | ~1 min | |
| Headless start / save / shutdown, then reload | ~4 min | two fixed-sleep runs of ~100 s each |
| **Batch 2**: read 33 costumes + 15 in-row artifacts, write the generator, generate 33, hand-write 7 | ~15 min | the generator paid for itself on file 5 |
| **Batch 2 `build.sh`** | **95 s** | publish 28.5 s; 154 files mirrored |
| Batch 2 reflection + two headless runs | ~5 min | |

**So a 30-file batch is roughly 35 minutes of agent time plus 90 seconds of build, once Docker is
up.** The 266 s figure in the brief is not what this machine does today with a warm layer cache:
the whole three-step gate ran in 86 s, measured by the script's own `SECONDS`. Whether that
number is warm-cache luck (the `git clone` and SDK layers were cached) or a faster machine, the
brief's "batch of 20 is about an hour" is now pessimistic by about 2× rather than optimistic by 6×,
**provided the batch is pre-flighted.** Un-pre-flighted, add one failed cycle per ~9 compile errors.

---

## 9. Headless verification

Throwaway `--rm` container, loopback-only (`127.0.0.1:2593`, `serverListing.address
127.0.0.1`, `autosave.enabled False` — exactly the three settings CC3 says to change and no
others), scratch `Saves/` under the task's temp folder, no published ports, image
`sl-modernuo:cc9a`. Not the live stack. `sl-modernuo` (the live container name) was `Exited`
before, during and after, and was not touched.

| Run | Result |
|---|---|
| **1 — fresh scratch `Saves/`, start / `n` / `save` / `shutdown`** | `Loading world done (617 items, 90 mobiles) (0.14 seconds)`; `Listening: 127.0.0.1:2593` and `127.0.0.1:12000 (Pings)` only; `Saving world done (0.02 seconds)`; `Writing world save snapshot done (0.13 seconds)`; `Shutting down`. Zero errors, zero warnings in 58 log lines. Container exit 0 |
| **2 — reload run 1's save** | `Loading world done (621 items, 91 mobiles) (0.18 seconds)`, same listeners, `Saving world done (0.01 seconds)`, clean shutdown, exit 0. Zero errors |

| **3 — batch-2 image `sl-modernuo:cc9b`, fresh scratch `Saves/`** | `Loading world done (617 items, 90 mobiles) (0.11 seconds)`, loopback listeners, `Saving world done (0.01 seconds)`, clean shutdown, exit 0 |
| **4 — reload run 3's save** | `Loading world done (621 items, 91 mobiles) (0.23 seconds)`, save, clean shutdown, exit 0 |

The 617 → 621 / 90 → 91 growth is the ClusterF seeders, as in CC2 and CC3. Zero errors or
warnings in any of the four logs (`headless-run1..4.log` in the task's work folder).

Type registration, reflected over `/modernuo/UOContent.dll` inside the built image
(`reflect.cs`, same probe as CC2/CC3): **33 ok, 0 bad** — every type reports
`generated=[Deserialize Serialize]` and a `(Serial)` constructor, none of which is in the
source, so the generator ran for all of them. `GargishPlateChest/Legs` and
`AmuletOfRighteousness` additionally report the collapsed `(Int32)` constructor.

**Not verified headlessly, per the standing rule:** an *instance* of any of these surviving a
save/reload, appearance, the goblet's 24-hour refill, the costume body-mod, the Greymist set
bonus firing, and the fishing pole's body-mod. Batched for the client spot check.

---

## 10. Docker Desktop would not start — recipe

Not a shard problem, but it cost the task half an hour and will recur.

Docker Desktop 4.75 on this machine leaves two AF_UNIX socket files behind after any unclean
exit, and on the next launch fails to `remove` them and crashes with "The file cannot be
accessed by the system": `%LOCALAPPDATA%\Docker\run\dockerInference` and
`%LOCALAPPDATA%\docker-secrets-engine\engine.sock`. `del`, `Remove-Item` and
`fsutil reparsepoint delete` all fail on them. **Renaming the parent folder works**, and Docker
recreates it. What got the daemon up (`daemon up after 5s`), in order:

1. stop every `*docker*` process; `wsl --shutdown`
2. rename `%LOCALAPPDATA%\Docker\run` and `%LOCALAPPDATA%\docker-secrets-engine` to `*.stale-<time>`
3. launch Docker Desktop, poll `docker version`

Skipping step 1 or doing only one folder gets the "waiting for init control API" hang instead
(9+ minutes, engine never answers). Four parked folders now sit under `%LOCALAPPDATA%`; they
are empty apart from the dead sockets and can be deleted from an elevated prompt, or left.
Also observed: `sl-portainer` has a restart policy and came up with the daemon; the live
`sl-modernuo` container did not (it was stopped two months ago). Q-036.

---

## 11. What is done, what remains, and the next batch

**Done:** three batches, **120 files / 124 types** in `server/customizations/Items/`, each green
on its first `build.sh` cycle, all reflected, six clean headless runs (§9, §13). Three commits per
repo. `tools/progress-state.json` updated; `python tools/progress.py` run.

**Remaining in the row, by bucket (§4).** Counted 2026-09-08 after batch 3, not carried forward
from the sentence that used to be here (which said "~35 files" and "the 19 remaining" gargish
weapons; ServUO has 20 `Gargish*` weapon files, three were in batch 1 and `GargishTalwar` is
ModernUO's, so the honest number was 16, and the list was right while the count was wrong):

| Bucket | Left | Note |
|---|---|---|
| Plain, from the 320 | **120** | 189 − 20 (batch 1) − 49 (batch 3). All 49 of batch 3 are in S9's appendix and none is a set piece or absorption user itself |
| Set armour re-parents | **79** | 83 − the 4 Greymist. Batch 4 |
| In-row 81 | **40** | − 34 costumes − 7 artifact files; **11 of the 40 are carrier-blocked** (§4) |
| Carrier-blocked | **41** | 30 from the 320 + 11 from the in-row. S10 built the carriers; batch 4, after re-verifying the no-instance condition (Q-039, `docs/gap-register.md`) |
| Co-port 10, upstream/carrier 44 | as S9 | untouched |
| Not candidates | 18 | already in ModernUO (§12) |

**Next was CC9 batch 4**, and this paragraph used to say "the five Q-039 re-parents" and list four; Q-040
then measured every ported type's ServUO descendants and the list is **one** (`GargishDagger`).
Batch 4 is done: §14.

---

## 12. Appendix — lists

### Batch 1 (31 ServUO files)

```
Items/Artifacts/Equipment/Glasses/GargishGlasses.cs
Items/Equipment/Armor/GargishPlateChest.cs
Items/Equipment/Armor/GargishPlateLegs.cs
Items/Equipment/Jewelry/GargishEarrings.cs
Items/Equipment/Jewelry/GargishNecklace.cs            (3 types)
Items/Equipment/Weapons/GargishGnarledStaff.cs
Items/Equipment/Weapons/GargishKatana.cs
Items/Equipment/Weapons/GargishDagger.cs
Items/Equipment/Armor/LargeStoneShield.cs
Items/Artifacts/Consumables/ElixirofAgapiteConversion.cs
Items/Artifacts/Consumables/GobletOfCelebration.cs
Items/Artifacts/Consumables/GrapeBunch.cs
Items/Artifacts/Consumables/InfusedAlchemistsGem.cs
Items/Artifacts/Decorative/BakeKitsuneStatue.cs
Items/Artifacts/Decorative/CoffinPiece.cs
Items/Artifacts/Decorative/CreepingVine.cs
Items/Artifacts/Equipment/Armor/AnimatedLegsoftheInsaneTinker.cs
Items/Artifacts/Equipment/Clothing/CloakOfDeath.cs
Items/Artifacts/Equipment/Clothing/TheScholarsHalo.cs
Items/Artifacts/Equipment/Jewelry/AmuletOfRighteousness.cs
Items/Artifacts/Equipment/Jewelry/Venom.cs
Items/Artifacts/Equipment/Spellbooks/ClaininsSpellbook.cs
Items/Artifacts/Equipment/Weapons/AxeOfAbandon.cs
Items/Artifacts/Equipment/Weapons/BansheesCall.cs
Items/Artifacts/Equipment/Instruments/DreadFlute.cs
Items/Artifacts/Tools/XenrrFishingPole.cs
Items/Artifacts/Equipment/Armor/Sets/Acolyte/GreymistArms.cs
Items/Artifacts/Equipment/Armor/Sets/Acolyte/GreymistChest.cs
Items/Artifacts/Equipment/Armor/Sets/Acolyte/GreymistGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Acolyte/GreymistLegs.cs
Items/Equipment/Suits/BaseCostume.cs
```

### Batch 3 (49 ServUO files, 49 types; 9 on a carrier, marked)

```
Items/Equipment/Weapons/GargishAxe.cs                 Items/Equipment/Jewelry/BlueDiamondRing.cs
Items/Equipment/Weapons/GargishBardiche.cs            Items/Equipment/Jewelry/BrilliantAmberBracelet.cs
Items/Equipment/Weapons/GargishBattleAxe.cs   [BaseSetWeapon]   Items/Equipment/Jewelry/DarkSapphireBracelet.cs
Items/Equipment/Weapons/GargishBoneHarvester.cs       Items/Equipment/Jewelry/EcruCitrineRing.cs
Items/Equipment/Weapons/GargishButcherKnife.cs        Items/Equipment/Jewelry/FireRubyBracelet.cs
Items/Equipment/Weapons/GargishCleaver.cs             Items/Equipment/Jewelry/GargishBracelet.cs
Items/Equipment/Weapons/GargishDaisho.cs              Items/Equipment/Jewelry/GargishRing.cs
Items/Equipment/Weapons/GargishKryss.cs               Items/Equipment/Jewelry/PerfectEmeraldRing.cs
Items/Equipment/Weapons/GargishLance.cs               Items/Equipment/Jewelry/StaffRing.cs
Items/Equipment/Weapons/GargishMaul.cs                Items/Equipment/Jewelry/TurqouiseRing.cs
Items/Equipment/Weapons/GargishPike.cs                Items/Equipment/Jewelry/WhitePearlBracelet.cs
Items/Equipment/Weapons/GargishScythe.cs
Items/Equipment/Weapons/GargishTekagi.cs              Items/Equipment/Armor/GargishPlateArms.cs      [BaseSetArmor]
Items/Equipment/Weapons/GargishTessen.cs              Items/Equipment/Armor/GargishPlateKilt.cs      [BaseSetArmor]
Items/Equipment/Weapons/GargishWarFork.cs             Items/Equipment/Armor/GargishKiteShield.cs     [BaseSetShield]
Items/Equipment/Weapons/GargishWarHammer.cs           Items/Equipment/Armor/GargishChaosShield.cs
Items/Equipment/Weapons/OrcishBow.cs                  Items/Equipment/Armor/GargishOrderShield.cs
Items/Equipment/Weapons/PaladinSword.cs               Items/Equipment/Armor/LargePlateShield.cs
Items/Equipment/Weapons/Shortblade.cs                 Items/Equipment/Armor/MediumPlateShield.cs
Items/Equipment/Weapons/StoneWarSword.cs              Items/Equipment/Armor/SmallPlateShield.cs
Items/Equipment/Weapons/RandomWand.cs  (static helper, not an item)   Items/Equipment/Armor/AssassinsCowl.cs
                                                      Items/Equipment/Armor/ElegantCollar.cs
                                                      Items/Equipment/Armor/EvilOrcHelm.cs
                                                      Items/Equipment/Armor/MagesHood.cs
                                                      Items/Equipment/Armor/DragonTurtleHideArms.cs    [BaseSetArmor]
                                                      Items/Equipment/Armor/DragonTurtleHideBustier.cs [BaseSetArmor]
                                                      Items/Equipment/Armor/DragonTurtleHideChest.cs   [BaseSetArmor]
                                                      Items/Equipment/Armor/DragonTurtleHideHelm.cs    [BaseSetArmor]
                                                      Items/Equipment/Armor/DragonTurtleHideLegs.cs    [BaseSetArmor]
```

### Already in ModernUO by content (18) — remove from the row

```
Items/Equipment/Armor/GargishClothArmor.cs        -> GargishCloth{Arms,Chest,Legs,Kilt}Type1/Type2 (8 types)
Items/Equipment/Armor/GargishLeatherArms.cs       -> GargishLeatherArmsType2   (0x302)
Items/Equipment/Armor/GargishLeatherChest.cs      -> GargishLeatherChestType1  (0x304)
Items/Equipment/Armor/GargishLeatherKilt.cs       -> GargishLeatherKiltType1   (0x311)
Items/Equipment/Armor/GargishLeatherLegs.cs       -> GargishLeatherLegsType1   (0x305)
Items/Equipment/Armor/FemaleGargishLeatherArms.cs -> GargishLeatherArmsType1   (0x301)
Items/Equipment/Armor/FemaleGargishLeatherChest.cs-> GargishLeatherChestType2  (0x303)
Items/Equipment/Armor/FemaleGargishLeatherKilt.cs -> GargishLeatherKiltType2   (0x310)
Items/Equipment/Armor/FemaleGargishLeatherLegs.cs -> GargishLeatherLegsType1   (0x305)
Items/Equipment/Armor/GargishStoneArms.cs         -> GargishStoneArmsType1     (0x284)
Items/Equipment/Armor/GargishStoneChest.cs        -> GargishStoneChestType1    (0x286)
Items/Equipment/Armor/GargishStoneKilt.cs         -> GargishStoneKiltType1     (0x288)
Items/Equipment/Armor/GargishStoneLegs.cs         -> GargishStoneLegsType1     (0x28A)
Items/Equipment/Armor/FemaleGargishStoneArms.cs   -> GargishStoneArmsType2     (0x283)
Items/Equipment/Armor/FemaleGargishStoneChest.cs  -> GargishStoneChestType2    (0x285)
Items/Equipment/Armor/FemaleGargishStoneKilt.cs   -> GargishStoneKiltType2     (0x287)
Items/Equipment/Armor/FemaleGargishStoneLegs.cs   -> GargishStoneLegsType2     (0x289)
Items/Equipment/Weapons/SerpentStoneStaff.cs      -> SerpentstoneStaff         (0x906)
```

(ModernUO's `GargishStudded*Type1/2` share the stone item IDs; that is upstream's choice.)
Not duplicates despite an ItemID match, checked by reading: the four `CloakOf*` (elven robe
graphic), `ConjurersGarb` (robe), `SashOfMight`, `ObiDiEnse`, `ShroudOfTheCondemned`,
`DreadFlute`, `FNPitchfork`, `InfusedGlassStave`, `StaffRing`, the talismans, and the
decoratives sharing a statue graphic — all artifact variants with their own type and name.

### Absorption users, no carrier (17)

```
Items/Artifacts/Equipment/Armor/BasiliskHideBreastplate.cs      (DragonChest)
Items/Artifacts/Equipment/Armor/CrownOfArcaneTemperament.cs
Items/Artifacts/Equipment/Armor/DefenderOfTheMagus.cs
Items/Artifacts/Equipment/Armor/KelpWovenLeggings.cs
Items/Artifacts/Equipment/Armor/ProtectoroftheBattleMage.cs
Items/Artifacts/Equipment/Armor/ResonantShieldOfVengeance.cs    (shield)
Items/Artifacts/Equipment/Armor/WallOfHungryMouths.cs
Items/Artifacts/Equipment/Armor/WardedDemonboneBracers.cs
Items/Artifacts/Equipment/Clothing/WardensArmorOfAugmentation.cs
Items/Artifacts/Equipment/Jewelry/BraceletOfPrimalConsumption.cs
Items/Artifacts/Equipment/Jewelry/Lavaliere.cs
Items/Artifacts/Equipment/Weapons/DraconisWrath.cs
Items/Artifacts/Equipment/Weapons/JadeWarAxe.cs
Items/Artifacts/Equipment/Weapons/ResonantStaffOfEnlightenment.cs
Items/Artifacts/Equipment/Weapons/StaffOfResonance.cs
Items/Artifacts/Talismans/FrostguardTalisman.cs
Items/Artifacts/Talismans/JadeSnakeHead.cs
```

### Set pieces on bases with no carrier (13)

```
Sets/Bestial/BeastialSetHelper.cs      : Timer (read it)
Sets/Juggernaut/Evocaricus.cs          : VikingSword
Sets/Juggernaut/MalekisHonor.cs        : MetalKiteShield
Sets/Luck/EtoileBleue.cs               : GoldRing
Sets/Luck/LuneRouge.cs                 : GoldRing
Sets/Luck/NovoBleue.cs                 : GoldBracelet
Sets/Luck/SoleilRouge.cs               : GoldBracelet
Sets/Marksman/Feathernock.cs           : BaseQuiver
Sets/Marksman/Swiftflight.cs           : Bow
Sets/Sorcerers/SorcererHat.cs          : WizardsHat
Sets/Virtue/HumilityCloak.cs           : BaseClothing
Sets/Virtue/SacrificeSollerets.cs      : BaseClothing
Sets/Virtuosos/VirtuososCap.cs         : JesterHat
```

### In-row files whose named dependency batch 1 or ModernUO's gargish types satisfy (53), read

| Now plain (42) | The 34 `Items/Equipment/Suits/*Costume.cs`, `CastOffZombieSkin` (→ `GargishLeatherArmsType2`), `CuffsOfTheArchmage` (+ gargish variant → `GargishStoneArmsType1`), `PillarOfStrength`, `BreastplateOfTheBerserker`, `GiantSteps` (→ `GargishStoneLegsType1`), `Glasses`, `NightEyes`, `CollectionsBritLibraryGlasses` (unread) |
| Also need an absorption carrier (6) | `BritchesOfWarding` (random eater on `ChainLegs` + a gargish twin), `PetrifiedSnake` (→ `SerpentstoneStaff`), `StoneDragonsTooth`, `DragonJadeEarrings`, `ObsidianEarrings`, `SpinedBloodwormBracers` |
| Also need set-capable gargish jewellery (5) | `VirtuososEarpieces`, `VirtuososNecklace` (`GargishEarrings`/`GargishNecklace` would have to derive from `BaseSetArmor`), `BestialArms`, `BestialEarrings`, `BestialNecklace` (+ `BestialSetHelper`) |
| Still short of other things | `VillainousEpiphany` (Epiphany helper, `GargishPlateArms`, `GargishPlateKilt`) |

One cheap option worth Chase's eye, not taken here: **derive the ported gargish armour-class
jewellery (`GargishEarrings`, `GargishNecklace`) and `GargishPlateChest/Legs` from
`BaseSetArmor` instead of `BaseArmor`.** ServUO carries set and absorption state on every
`BaseArmor`, so for those four ported bases it is the *more* faithful parent, `SetID.None` is
inert, and it would free the 5 set pieces and the 4 armour-class absorption users above without
a new carrier. It costs nothing but a save-format decision on four brand-new types, which is why
it should be made once and before they reach the live save.

### The item-ID cross-check, for the next batch

```python
# cwd = D:\UO\ServUO-pub57\Scripts ; arg = file of ServUO-relative paths
# For every `class X : Y` whose ctor chains `: base(<itemID>)`, report any ModernUO or
# server/customizations type whose ctor chains the same literal. Matches are candidates for
# "already present under another name"; read each before believing it.
import re, sys
from pathlib import Path
mu = Path("D:/UO/ModernUO-pinned/Projects/UOContent"); cust = Path("D:/ShatteredLegacy/server/customizations")
num = lambda s: int(s, 16) if s.lower().startswith("0x") else int(s)
idx = {}
for base in (mu, cust):
    for p in base.rglob("*.cs"):
        t = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"class\s+(\w+)\s*:\s*(\w+)", t):
            b = re.search(r":\s*base\(\s*(0x[0-9A-Fa-f]+|\d+)\s*[,)]", t[m.end():m.end()+1500])
            if b: idx.setdefault(num(b.group(1)), []).append(m.group(1))
for f in (l.strip() for l in open(sys.argv[1]) if l.strip()):
    t = Path(f).read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"class\s+(\w+)\s*:\s*(\w+)", t):
        b = re.search(r":\s*base\(\s*(0x[0-9A-Fa-f]+|\d+)\s*[,)]", t[m.end():m.end()+2500])
        if b and num(b.group(1)) in idx:
            print(f, m.group(1), b.group(1), "==", ", ".join(idx[num(b.group(1))][:4]))
```

---

## 13. Batch 3 — the plain remainder, 49 files, 2026-09-08

**Result: green on the first `build.sh` cycle (101 s, 42 tests, `structured customizations
installed: 208 file(s)` = 159 + 49), 49 of 49 types reflected, headless fresh save and reload
both clean. 4,636 ServUO lines in, 1,740 out.** Files listed in §12; every one carries a header
comment naming its ServUO source and any deviation.

### 13.1 The count, checked before anything else

The brief said 49 (21 weapons, 11 jewellery, 17 armour and shields) and said the old §11 was
wrong. Both checked: all 49 present under `D:\UO\ServUO-pub57\Scripts\Items\Equipment\`, all 49
absent from `server/customizations` and from `tools/modernuo-stems.txt`, and all 49 present in
S9's appendix lists (grep, 49 of 49). ServUO has 20 `Gargish*` files in `Items/Equipment/Weapons`;
minus `GargishKatana`, `GargishDagger`, `GargishGnarledStaff` (batch 1) and `GargishTalwar`
(ModernUO's own, `Items/Weapons/Swords/GargishTalwar.cs`) leaves **16**, which is what the list
has. §11 is corrected above.

### 13.2 Pre-flight, the §3 method, and what it found

Run over all 49 before a line was written. Steps 1–3 as greps against `D:\UO\ModernUO-pinned`,
step 4 with the §12 script, step 5 as the descendant walk below.

| Check | Result |
|---|---|
| (1) Base class exists in ModernUO | 49 of 49. `BaseAxe`, `BasePoleArm`, `BaseSword`, `BaseKnife`, `BaseBashing`, `BaseSpear`, `Bow`, `GoldRing`, `GoldBracelet`, `BaseRing`, `BaseBracelet`, `BaseShield`, `BaseArmor`, `BaseHat`, `OrcHelm` all present |
| (2) Every override is virtual in the pinned tree | 47 of 49. The two misses are `EvilOrcHelm`'s `UseIntOrDexProperty` / `IntOrDexPropertyValue`: ServUO `BaseArmor` virtuals with **zero readers in ServUO itself** (`grep -rln` over `Scripts/` finds the declaration and this file), absent from ModernUO. Dropped, D-11 |
| (3) Every attribute member is in the matching `Aos*` enum | 49 of 49. `LowerManaCost`, `CastSpeed`, `CastRecovery`, `SpellDamage`, `LowerRegCost`, `RegenMana/Hits/Stam`, `EnhancePotions`, `BonusStr/Int/Dex`, `WeaponSpeed`, `WeaponDamage`, `NightSight`, `AttackChance` in `AosAttribute`; `DurabilityBonus` in `AosWeaponAttribute`; `Resistances.Cold/Fire/Poison` on `BaseJewel` |
| (4) Item-ID cross-check | one hit, `StaffRing` at `0x108A` = `GoldRing`, expected: it is a gold ring with a name, and §12 already lists it as not a duplicate. `0xA40F`–`0xA411` (collar, cowl, hood) and `0x782A`–`0x782E` (dragon turtle hide) collide with nothing |
| (5) Set / absorption presence, transitively | **9 bases need a carrier parent**, §13.3 |
| WeaponAbility names | all 14 used exist unchanged: `CrushingBlow`, `Dismount`, `ParalyzingBlow`, `BleedAttack`, `ConcussionBlow`, `MortalStrike`, `InfectiousStrike`, `Disarm`, `Feint`, `DoubleStrike`, `ArmorIgnore`, `DualWield`, `TalonStrike`, `WhirlwindAttack` |
| Other members | `BaseRunicTool.ApplyAttributesTo(BaseJewel, bool, int, int, int, int)` same arity (`BaseRunicTool.cs:938`); `IDyable` and `Dye(Mobile, DyeTub)` (`DyeTub.cs:10`); `Titles.AwardKarma(Mobile, int, bool)` (`Misc/Titles.cs:216`); `Item.AddWeightProperty(IPropertyList)` virtual (`Item.cs:1917`) and `IPropertyList.Add(int, string)`; `BaseClothing.StrRequirement` settable (`BaseClothing.cs:144`); `Loot.RandomWand()` (`Misc/Loot.cs:338`); `BasePoleArm.HarvestSystem` virtual (`BasePoleArm.cs:32`) |

Three things the name scan could not have seen, each caught here rather than at the compiler:

- **`RandomWand` is not an item.** It is a 10-line static class wrapping `Loot.RandomWand()`,
  called by two ServUO NPCs (`Braen.cs:98`, `Canir.cs:49`). Ported as the same static class so
  those NPCs port unchanged when their turn comes; it has no serialization and no `[Constructible]`.
- **`OrcishBow` shows a durability line ServUO shows twice** (D-12): ServUO's `BaseWeapon.GetProperties`
  emits 1151780 for `DurabilityBonus` and the bow adds 1060410 on top; pinned ModernUO's `BaseWeapon`
  emits neither (`grep 1060410\|1151780` over `Items/Weapons/` is empty), so the bow's override is
  the only line.
- **`GargishWarHammer` flips to `0x481` in ServUO** (D-10). Every other gargish weapon flips to
  itemID+1 and `0x481` is used in ServUO only as a Prism of Light pillar graphic
  (`Commands/DecorateDelete.cs:1282`), so it is a typo; `0x48C1` here.

Nothing else needed more than the standard conversion: `[Constructable]` pairs collapsed to one
optional parameter (`GargishPlateArms/Kilt(int hue = 0)`, `AssassinsCowl/MagesHood(int hue = 0)`),
`Weight = x` to `DefaultWeight => x`, `Race RequiredRace => Race.Gargoyle` to
`int RequiredRaces => Race.AllowGargoylesOnly`, `IsArtifact` / `CanBeWornByGargoyles` dropped per
D-1/D-2, `OnRemoved(object)` to `OnRemoved(IEntity)`, `Mobile.IsPlayer()` to
`AccessLevel == AccessLevel.Player` (D-13). Where ServUO leaves the weight commented out
(`Shortblade`, `StoneWarSword`, `GargishKiteShield`, `GargishOrderShield`, `MediumPlateShield`,
`GargishBracelet`, `GargishRing`) or unset (`LargePlateShield`) the port inherits the base default,
the `LargeStoneShield` precedent.

### 13.3 Nine carrier parents, not eight — verified, not taken from the brief

The rule (AGENTS.md, "Give a base its final parent the first time you port it"): grep ServUO for
`class \w+ : <Type>` and read the descendants. Done for all 49, then walked **transitively** (a
descendant's descendants too; the walk found no second-level subclasses), with the grep widened
from the five tokens in AGENTS.md to
`AbsorptionAttributes|SetAttributes|SetSelfRepair|SetID|ISetItem|SetHue|SetSkillBonuses|Set\w+Bonus|Pieces|BardMastery`.
41 direct descendants read.

| Port with parent | Type | Descendant that forces it, and the member |
|---|---|---|
| `BaseSetArmor` | `GargishPlateArms` | `VirtuososArmbands` (`Sets/Virtuosos/VirtuososArmbands.cs:11-29`): `SetID`, `Pieces`, `BardMasteryBonus`, `SetHue` |
| `BaseSetArmor` | `GargishPlateKilt` | `VoidInfusedKilt` (`:20`): `AbsorptionAttributes.EaterDamage = 10` |
| `BaseSetArmor` | `DragonTurtleHideArms`, `Bustier`, `Chest`, `Helm`, `Legs` | `DardensSleeves/Bustier/Tunic/Helm/Legs` (`Sets/Dardens Set/`): `SetID`, `Pieces`, `AbsorptionAttributes`, `SetAttributes`, `SetSelfRepair`, the five `Set*Bonus` |
| `BaseSetShield` | `GargishKiteShield` | `DragonHideShield` (`:13`): `AbsorptionAttributes.EaterFire = 20` |
| **`BaseSetWeapon`** | **`GargishBattleAxe`** | **`GargishPincer`** (`Items/Artifacts/Equipment/Weapons/Pincer.cs:60`): `SetSkillBonuses.SetValues(0, Lumberjacking, 10)`. Set-carrier state on ServUO's `BaseWeapon` (`BaseWeapon.cs:847, 4140, 4185`); on a `SetID.None` weapon it is inert on ServUO too, so porting `GargishPincer` faithfully means keeping it inert, which needs the member, which needs the carrier |

The ninth is the one the brief's token list could not find, and it is the reason the list should
grow (Q-040). The other 32 descendants (`GargishSmugglersEdge`, `HailstormGargoyle`,
`TheRedeemer`, `MocapotlsObsidianSword`, `BladeOfBattle`, `AbyssalBlade`, `GargishDupresSword`,
the Epiphany kilts and arms, `VvVGargishPlateArms`, `GargishKiltOfFeudalVise`,
`GargishSignOfChaos/Order`, `GargishHephaestus`, `CowlOfTheMaceAndShield`,
`ElegantCollarOfFortune`, `MagesHoodOfScholarlyInsight`, and the rest) touch none of the tokens;
their bases stay stock. `GargishBracelet` and `GargishRing` are `BaseJewel`s in ServUO, not
armour-class like the earrings and necklace, so the §12 `BaseSetArmor` option does not arise.

`SetID` defaults to `SetItem.None` on every carrier, so all nine are inert today; S10 §4 has the
serialization consequence and `TigerPeltAloneIsNotASetItem` is the proof that `None` is inert.
**The no-instance condition held at port time:** `sl-modernuo:latest` is still the 2026-09-07 02:49
image (predates CC9 batch 1), the live `sl-modernuo` container has been `Exited` for two months,
and these nine types did not exist before this batch. Nothing here was deployed.

### 13.4 Verification — read, not just compiled

1. **Value diff against ServUO, after writing.** A script parsed every `override X => V` from
   each ServUO file (getter blocks collapsed) and from its port, applied the expected renames
   (`RequiredRace` → `RequiredRaces`, `Weight` → `DefaultWeight`, `Name` → `DefaultName`,
   `IsArtifact`/`CanBeWornByGargoyles` dropped), and compared. **524 overrides compared, 0
   mismatches**; the ten lines it flagged were its own inability to read an expression-bodied
   constructor (`=> Layer = Layer.TwoHanded`) plus the intended D-10 flip. The 19 uniform weapons
   were generated from the ServUO source by a script (`gen_weapons.py`, in the task's work
   folder) that asserts every override name is one it knows; the five Dragon Turtle Hide pieces
   were transcribed from a table and are the ones the diff was for.
2. **`build.sh -t sl-modernuo:cc9c`**: exit 0 in 101 s, 15 patches applied, 208 structured
   customizations, **42 tests passed**, image built. Log `build-batch3.log` in the work folder.
3. **Reflection over `/modernuo/UOContent.dll` in the built image** (`reflect.cs`, the CC2 probe):
   **49 ok, 0 bad.** All 48 item types report `generated=[Deserialize Serialize]` and a `(Serial)`
   constructor; the four with a collapsed optional parameter report `(Int32)`; the nine carrier
   children report their carrier as `BaseType`; `RandomWand` is present and static. One trap:
   `dotnet run` on a file-based app restores from NuGet, so the probe container cannot take
   `--network=none` (it fails with NU1301); the runtime containers did.
4. **Headless run 5** (fresh scratch `Saves/`, S10's loopback `Configuration/`, `--network=none`,
   `--rm`): `Loading world done (618 items, 90 mobiles)`, `Listening: 127.0.0.1:2593` only,
   `Saving world done`, snapshot written, clean shutdown, exit 0, zero errors or warnings in 58 lines.
   **Run 6** on run 5's save: `Loading world done (622 items, 91 mobiles)`, save, clean shutdown,
   exit 0, 50 lines, zero errors.
   **618, not the 617 of every earlier run**: checked rather than assumed. The two saves'
   `SerializedTypes.db` differ only in stock NPC outfit types (`CompositeBow`/`QuarterStaff`,
   `FeatheredHat`/`FancyShirt`, …), so the seeders' vendor equipment is random and the count
   varies by one; no batch-3 type has an instance in either save, as expected, since nothing
   places one.

**Not verified headlessly, per the standing rule:** an instance of any of the 49 surviving a
save/reload, appearance of the EJ-era graphics (`0xA40F`–`0xA411`, `0x782A`–`0x782E`, the
`0x48xx` gargish weapons) in the client, the jewellery's random rolls, the `EvilOrcHelm` stat swap
and karma loss, the order shield's guild check. Batched for the client spot check.

### 13.5 What it cost

Wall clock 2026-09-08, this machine, Docker already up (no §10 recovery this time).

| Phase | Elapsed |
|---|---|
| Orientation: `AGENTS.md`, `docs/tasks.md`, this note, `port-recipe.md`, S10 §4–6, Q-038/Q-039, batch-1 reference ports | ~12 min |
| Pre-flight over 49 files: the 41-descendant grep and transitive walk, five §3 checks, ModernUO member lookups | ~10 min, overlapped with orientation |
| Writing: the weapon generator (19 files), the Dragon Turtle table (5), 25 by hand | ~6 min |
| Post-write value diff (524 overrides) | ~1 min |
| **`build.sh` gated cycle** | **101 s** |
| Reflection (one failed attempt on `--network=none`, then 9 s) | ~2 min |
| Two headless runs | ~3.5 min |
| Note, Q-040, progress | ~12 min |

**About 45 minutes for 49 files**, against §8's "roughly 35 minutes for 30". The generator is
why: the 16 gargish weapons plus three more are one shape, and a script that refuses any file
whose overrides it does not recognise is both faster and safer than 19 hand transcriptions.
One trap worth recording for the next agent: the shell tool here silently truncates a command
at about 8 KB, which turned two multi-file heredoc writes into "unexpected EOF" errors that
looked like quoting bugs. Keep each write under that, or write files from a Python script.

### 13.6 What batch 3 leaves

- **Q-040**, two decisions for Chase before `latest` is rebuilt: whether the 40 stock-parented
  files should be on carriers after all (Q-039's general wording says yes; `docs/tasks.md` and the
  brief said no, and no was done), and widening the AGENTS.md descendant-grep token list to
  include `SetSkillBonuses`, `SetHue`, `Set*Bonus` and `Pieces`, which is what found the ninth.
- **`StaffRing` is not OSI content** and is now in the tree because it was on the list. If the
  shard does not want a ServUO staff tool, deleting the file before deployment costs nothing.
- **Batch 4** as `docs/tasks.md` defines it, and nothing from it was started here: the 41
  carrier-blocked files, the Q-039 re-parents, the 79 set-armour re-parents, all after
  re-verifying the no-instance condition. `GargishPincer`, `HailstormGargoyle`,
  `GargishSmugglersEdge`, `DragonHideShield`, `VoidInfusedKilt`, `VirtuososArmbands` and the five
  Darden pieces now have the parent they need.

## 14. Batch 4 — the one re-parent, the 41 carrier-blocked, the set-armour bucket, 2026-09-08

**Result: 125 new files / 127 new types, 3 existing files corrected. One failed `build.sh` cycle (28 s,
one file, one inlined member the pre-flight did not cover), then green (99 s, 15 patches, 42 tests,
`structured customizations installed: 333` = 208 + 125). 130/130 types reflected, headless fresh save and
reload both clean. 10,062 ServUO lines in, 6,363 out. Every override and constructor value re-diffed against
ServUO: 126 files, 0 findings, and the diff was proved red first.** Work folder `D:\UO\cc9-batch4-work`
(generator, verifier, parents dump, logs); nothing in it is needed to rebuild.

### 14.1 The one re-parent: `GargishDagger` onto `BaseSetWeapon`, and how the window was checked

Q-040 collapsed the list to one type. Before touching it, the no-instance condition was **measured, not
assumed**, against every save artefact on this machine:

| Artefact | Checked how | Result |
|---|---|---|
| Live save `server/lib/uo/modernuo/Saves/` | newest file mtime; `SerializedTypes.db` read as a type table (1,468 `Server.*` names; positive control `Server.Items.Dagger` present) | last written **2026-07-06 13:25**; **no `Gargish*` type at all**, no `GargishDagger` |
| `Backups/Automatic/` (3 snapshots, 2026-07-01..03) | binary grep of every file | no match |
| `Archives/Daily` and `Archives/Hourly` (`.tar.zst`, newest 2026-07-04 and 2026-07-04-14) | no `zstd` on the machine; `pip install --user zstandard` (standing answer: small and local), stream-decompressed the two newest of each and read their `SerializedTypes.db` | 1,456–1,462 type names each, `Dagger` present, `GargishDagger` absent |
| `backups/uo-modernuo-premigration-full-20260531T130851Z.tar.gz` | by date only (3.5 GB) | 2026-05-31 predates the type by three months |
| Live container `sl-modernuo` | `docker inspect` | image created **2026-06-29**, `Exited (143)` since **2026-07-06**; the type first exists in `d4ce1ce` (2026-09-08) and `sl-modernuo:latest` is still the 2026-09-07 02:49 image |
| This batch's scratch save | `SerializedTypes.db` after run 2 | 163 types, none from batch 4 (nothing places one) |

So the window is open, and the check took about four minutes. The type table read is the decisive one: it
is what the server will consult on load, and it is a positive-controlled read, not a date argument.

`GargishDagger : BaseKnife` became `GargishDagger : BaseSetWeapon` with `BaseKnife`'s own members reproduced
(hit/miss sounds, the `BladedItemTarget` double-click, the pre-AOS poison-charge `OnHit`), because
`BaseSetWeapon` sits on `BaseMeleeWeapon` and skips `BaseKnife`. `StoneDragonsTooth : GargishDagger` then
ports as a plain derivation with its `AbsorptionAttributes.EaterPoison = 10` intact. `LargeStoneShield`,
`GargishKatana`, `GargishGnarledStaff` and batch 3's 40 were not touched.

**The carrier-member regex was regenerated from the six `BaseSet*.cs`** (serialized fields, virtuals and
interfaces) before the walk: it reproduces the AGENTS.md list exactly and adds only `IAbsorptionItem`, which
no ServUO file names. No carrier has gained a member since Q-040, so AGENTS.md was not edited.

### 14.2 Two corrections found on the way, both save-neutral today and neither after a deploy

- **`GargishBattleAxe` (batch 3) had lost `BaseAxe`.** Re-parenting it onto `BaseSetWeapon` without
  reproducing the stock members left it swinging one-handed with sword sounds (`Slash1H`, `0x23B`) and unable
  to chop wood. Batch 3's value diff could not see it because ServUO's file never states those members; they
  come from the parent. Reproduced now: sounds, `Axe` type, `Slash2H`, `HarvestSystem => Lumberjacking`, the
  harvest double-click and context menu, and `BaseAxe`'s two `IUsesRemaining` fields (150 uses, exceptional
  scaling), which adds two save-flag-guarded fields to a type with no instance anywhere (§14.1). Pinned
  `Engines/Harvest` never type-checks the tool, so the axe harvests exactly as a stock `BaseAxe` does.
- **`BaseSetWeapon` now derives from `BaseMeleeWeapon`, not `BaseWeapon`.** Every stock melee base sits on
  `BaseMeleeWeapon`, whose only member is `AbsorbDamage` (Attune Weapon absorption, plus Reactive Armor
  pre-AOS). S10 skipped it, so every carrier child silently lost that hook. `BaseMeleeWeapon` is not a generated
  type and its `Serialize`/`Deserialize` only call `base`, so the on-disk layout of every `BaseSetWeapon` child
  is byte-for-byte unchanged; verified by the 42 tests passing untouched and by reflection reporting
  `BaseSetWeapon : BaseMeleeWeapon` with the same generated pair. A ranged set weapon could never use this
  carrier anyway (§14.3, Q-041), so committing to the melee branch costs nothing.

Both are the same lesson as D-10 and D-11 in a new shape: **a stock parent's members are part of the port
when the parent changes**, and a diff against the ServUO child cannot see them. The generator below inlines
them from a dump of the pinned parents, and the reviewer of a carrier child should read the "Stock X members"
block against the pinned file, not against ServUO.

### 14.3 The 41 carrier-blocked: 40 ported, one declined pending Q-041

| Bucket (§12) | Files | Ported as |
|---|---|---|
| Absorption users, no carrier | 17 | 8 armour and `WardensArmorOfAugmentation` (a `BaseArmor` in both emulators despite its folder) on `BaseSetArmor`; `WallOfHungryMouths`, `DefenderOfTheMagus`, `ResonantShieldOfVengeance` (+`Human`) on `BaseSetShield`; `DraconisWrath`, `JadeWarAxe`, `ResonantStaffofEnlightenment`, `StaffOfResonance` on `BaseSetWeapon`; `BraceletOfPrimalConsumption`, `Lavaliere` on `BaseSetJewel`; **`FrostguardTalisman`, `JadeSnakeHead` on stock `BaseTalisman` with the eater line dropped (D-15)** |
| Set pieces, no carrier | 13 | `Evocaricus` (weapon), `MalekisHonor` (shield, with `MetalKiteShield`'s `IDyable`), the four Luck jewels, `Feathernock` (quiver), `SorcererHat` and `VirtuososCap` (clothing, hats inlined), `HumilityCloak` and `SacrificeSollerets` (clothing, ServUO already on `BaseClothing`), `BestialSetHelper` (§14.5); **`Swiftflight` not ported, Q-041** |
| In-row 11 | 11 | `BritchesOfWarding` (+ gargish twin), `PetrifiedSnake`, `DragonJadeEarrings`, `ObsidianEarrings`, `VirtuososEarpieces`, `VirtuososNecklace`, `BestialArms/Earrings/Necklace` all on or under a carrier; **`SpinedBloodwormBracers` is a `BaseClothing` in ServUO** (`Clothing/Arms.cs`, `GargishClothArms` 0x404), not the armour §4 assumed, so it is on `BaseSetClothing` with the same ID, layer, race and weight |

**Swiftflight.** `Bow : BaseRanged : BaseMeleeWeapon`; `BaseRanged` is generated with its own fields and
carries all of ranged combat. No carrier can sit above it and inlining it into one item would be a fork, not
a port. Declined for now, costed in Q-041 (~250 lines for a `BaseSetRanged`, zero patches; frees one file here
and the CC4 reforged bows). Until then Feathernock's set can never complete (D-17).

**Talismans.** ServUO stores an absorption block on `BaseTalisman` and never reads it:
`RunicReforging.GetSAAbsorptionAttributes` (`RunicReforging.cs`), the only aggregation path, returns the block
for `BaseArmor`, `BaseJewel`, `BaseWeapon` and `BaseClothing` and `null` for everything else. So a talisman
eater does nothing on ServUO either; only the tooltip line is lost here. S6 §4 said as much and this confirms
it from the call site. No talisman carrier, and this is the reason not to build one (D-15).

**Absorption aggregation reaches every other kind.** `SAAbsorptionAttributes.GetValue` here iterates
`IAbsorptionItem`, which all five absorbing carriers implement, so the 15 non-talisman absorbers aggregate
exactly as their ServUO originals do. Not verified at runtime (no client); the S6 tests cover the path.

### 14.4 The set-armour bucket: 85 files, of which 79 are set pieces and 6 are not

`docs/tasks.md` and §11 say 79. Counting S9's 320 list: **102** entries under `Sets/`, minus 4 Greymist
(ported) and 13 on non-armour bases (above) leaves **85**, not 79 and not batch 1's 83. The six extra are the
**Phoenix suit** (`PhoenixArms/Chest/Gloves/Gorget/Helm/Legs`): ServUO files it under `Sets/` but it has no
`SetID`, no set members, nothing but a hue, `LootType.Blessed` and a label. Not set pieces, so they stay on
their stock parents (`Ringmail*`, `StuddedGorget`, `NorseHelm`) as plain ports. **79 set pieces + 6 plain =
85 files, all ported.** The 79 is right; the bucket was mislabelled, and the six were never counted anywhere.

All 85 came out of one generator (`gen_batch4.py`) that refuses any constructor statement or override it does
not recognise; it refused two files (`BritchesOfWarding`, and originally `JadeWarAxe` for a member, below) and
those were hand-written. Per file it emits ServUO's own values, then a "Stock X members, reproduced because
the parent changed" block taken from a dump of the pinned parent (`parents.json`, 71 parents, 59 distinct ones
used), minus anything the child overrides itself. Three things the dump made visible:

- **`[Flippable]` is read with `inherit: false`** (`FlippableAttribute.cs:34`), so every re-parented piece
  whose stock parent flips had to have the attribute copied onto it; 12 of the 85 declared their own in ServUO
  and the rest carry the parent's. Batch 1's Greymist did this by hand; nothing in batch 1-3 says why.
- **Six gloves inherit `IArcaneEquip` machinery** (`LeatherGloves` ×5, `LeafGloves`): `Update`,
  `GetProperties`, `OnSingleClick`, `Flip`, and a serialized field. Not reproduced, per D-7 (an artifact glove
  is never crafted arcane). Logged once for the class.
- **The Darkwood six override `OnCraft`** (resource bonus on craft). ServUO's `ITool` is `BaseTool` here and
  `CraftItem.Resources` is a `List<CraftRes>`, so `GetAt(0)` becomes `[0]`. Pinned `WoodlandChest` has no
  `OnCraft` of its own, so the child's is the only one. `DarkwoodCrown` flips to `0x3169` in ServUO, which is
  the flipped **Vulture Helm** (`VultureHelm.cs` in both emulators); `RavenHelm` flips to `0x3168` in both.
  Corrected, same shape as D-10 (D-16).

The four Virtue pieces (`CompassionArms`, `HonestyGorget`, `HonorLegs`, `JusticeBreastplate`) derive from
`BaseArmor` directly in ServUO with their own `MaterialType`/`AosStrReq`, so they go straight onto
`BaseSetArmor` with nothing to inline. The note in §4 that "6 Initiation pieces also set `Attributes.Brittle`"
is wrong: grep over the 85 finds no `Brittle` anywhere.

### 14.5 Bestial: pieces ported, mechanic inert (D-14, Q-042)

`BestialSetHelper` (ServUO misspells the file `BeastialSetHelper.cs`; filename kept) drives the berserk rage
from two engine hooks: `OnDamage` from `AOS.Damage`, `OnHeal` from every heal path. Neither exists in pinned
ModernUO. The helper is ported whole (`Core.Now` for `DateTime.UtcNow`, `Timer(TimeSpan, TimeSpan)`,
pattern-matched `ISetItem { SetID: SetItem.Bestial }`), the three pieces call its `OnAdded`/`OnRemoved` as
ServUO does, and the two hook methods are present and uncalled. A full Bestial set gives its set bonus and
never rages. Same interim as `SetSelfRepair` on the S10 carriers; costed in Q-042. S10's D-2 (no berserk
tooltip line) stands.

### 14.6 Deviations added by this batch — for `docs/fidelity-principle.md`

| # | Deviation | Player notices | Reverses when |
|---|---|---|---|
| **D-14** | Bestial berserk mechanic inert: `BestialSetHelper.OnDamage`/`OnHeal` have no caller | A full Bestial set never enters a rage: no damage shrug, no heal block, no hue shift | +1 line to `AOS-damage-eater-hook.patch` and one call in each heal path (Q-042) |
| **D-15** | `FrostguardTalisman`, `JadeSnakeHead` lose `EaterCold = 5` / `EaterPoison = 5` | One tooltip line. **Behaviour identical**: ServUO never aggregates a talisman's absorption (§14.3) | a talisman carrier, which nothing else wants |
| D-16 | `DarkwoodCrown` flips to `0x3168`, not ServUO's `0x3169` | Nothing a player would call wrong: `0x3169` is the flipped Vulture Helm | never; ServUO's is the bug |
| **D-17** | `Swiftflight` not ported; Marksman set cannot complete | Feathernock shows "part of a set (2 pieces)" for a set with one obtainable piece | `BaseSetRanged` (Q-041) |
| D-18 | `SorcererHat`, `VirtuososCap` drop `BaseHat`'s `IsShipwreckedItem` field, its two shipwreck lines and its exceptional-craft bonus | Nothing: artifact hats are neither fished up nor crafted | paper only |
| D-19 | `JadeWarAxe` drops `BaseAxe`'s two `IUsesRemaining` fields | Nothing: `WarAxe.HarvestSystem => null`, so uses could never be consumed or shown | paper only |
| D-7 (extended) | `AssassinGloves`, `InitiationGloves`, `DeathGloves`, `SorcererGloves`, `VirtuososKidGloves`, `HunterGloves` are not `IArcaneEquip` | Nothing | paper only |
| D-13 (cause corrected) | see §7; the port was right, the stated reason was wrong (Q-040). `StaffRing`'s comment fixed in this batch | — | — |

Not a deviation but worth a line: `SpinedBloodwormBracers` is clothing here because it is clothing in ServUO,
while ModernUO's own stock `GargishClothArmsType1` (same 0x404) is armour. The artifact's resistances are its
own overrides either way; a player sees the same numbers.

### 14.7 Verification — read, not just compiled

1. **Pre-flight, scripted.** `preflight_sets.py` parsed all 85 set files and flagged anything outside the plain
   shape (methods, unknown overrides, unknown constructor statements, multi-class files, attributes): the
   Darkwood `OnCraft`, the four `BaseArmor`-direct Virtue pieces, 14 own `Flipable`s, and the six files without
   `SetID`. Every ModernUO API the 41 touch was grepped in the pinned tree before writing (`Resource` setter,
   `PhysicalBonus`, overridable `PhysicalResistance`, `Race.AllowAllRaces`, `StrRequirement` on armour and
   clothing, `WeightReduction`, `TypeAlias`, `BaseTalisman(int)`, `Timer(TimeSpan, TimeSpan)`,
   `SendLocalizedMessage(int, string, int)`, `CraftItem.Resources` as a list). **One thing it did not cover:**
   the pinned parents' members that the generator inlines. `WarAxe.HarvestSystem => null` is `BaseAxe`'s
   virtual, not `BaseWeapon`'s, and cost the one failed cycle (28 s, two `CS0246`/`CS0115` on one file). The
   fix was a one-name exclusion in the generator. Lesson: dump-and-inline needs its own pre-flight, that every
   inlined member exists on the carrier.
2. **Value diff, proved red.** `verify_values.py` compares every ServUO `override` and constructor assignment
   with its port after the expected renames (`RequiredRace`→`RequiredRaces`, `Weight`→`DefaultWeight`,
   `SAAbsorptionAttributes.`→`AbsorptionAttributes.`), plus the `Flippable` pair, over all 126 files (113
   generated, 13 hand-written or edited). **0 findings.** Then `AssassinArms` was mutated (one override value,
   one constructor value, one override deleted): **3 findings, exactly the three**, then 0 again after restore.
   2,061 comparisons over the generated files alone. It skips the random `switch` blocks in the five rolled
   items, which were read by eye against ServUO.
3. **`build.sh -t sl-modernuo:cc9d`**: failed cycle 28 s (above), then exit 0 in 99 s, 15 patches, 333
   structured customizations, 42 tests passed. Logs in the work folder.
4. **Reflection** over `/modernuo/UOContent.dll` in the built image (`reflect.cs`, the CC2 probe, resolved
   `Item` by walking `BaseType` names because a file-based app cannot reference `Server.dll`): **130 ok, 0
   bad**. Every item type reports `generated=[Deserialize Serialize]` and a `(Serial)` constructor;
   `GargishDagger` and `GargishBattleAxe` report `BaseSetWeapon`, `BaseSetWeapon` reports `BaseMeleeWeapon`,
   `BestialSetHelper` is static.
5. **Headless run 1** (fresh scratch `Saves/`, loopback-only copy of the live `Configuration/`, `--network=none`,
   `--rm`): `Loading world done (617 items, 90 mobiles)`, `Listening: 127.0.0.1:2593` only, save, snapshot,
   clean shutdown, exit 0, 59 lines. **Run 2** on run 1's save: `Loading world done (621 items, 91 mobiles)`,
   save, clean shutdown, exit 0, 51 lines. The same 617→621 / 90→91 seeder growth as every earlier batch.
   Three `WRN` lines in each, none about a type: the two standard account prompts, and `Command stats already
   registered to Stats_OnCommand` from `CommandSystem`, a registration collision that predates this batch
   (no batch-4 file registers a command; earlier notes did not list it but did not paste their warnings either).

**Not verified headlessly, per the standing rule:** any instance surviving a save/reload, any set bonus
firing through a weapon, jewel, clothing or quiver carrier (S10's tests cover the carriers with synthetic
pieces, not these), the random rolls, Darkwood's craft bonus, the Bestial hue handling, the axe harvesting.
Batched for the client spot check, which is now overdue by four batches.

### 14.8 What it cost

Wall clock 2026-09-08, this machine, Docker already up.

| Phase | Elapsed |
|---|---|
| Orientation: `AGENTS.md`, `tasks.md`, Q-037..040, this note, S10 §4, batch 1/3 reference ports | ~15 min |
| The no-instance check (§14.1), including the zstd detour | ~5 min |
| Pre-flight: 41 files read, 85 scripted, 71 pinned parents dumped, ~40 API lookups | ~20 min |
| Writing: generator (~330 lines) and 13 hand files; GargishDagger, GargishBattleAxe, BaseSetWeapon edits | ~15 min |
| Value diff and its red test | ~2 min |
| **`build.sh`**: one failed cycle 28 s + one green cycle 99 s | ~2.5 min |
| Reflection (one failed attempt on a `Server.Item` reference, then 130/130), two headless runs | ~5 min |
| Note, two questions, progress | ~15 min |

About **80 minutes for 125 files**, against batch 3's 45 for 49. The whole difference is reading: this batch
read 126 ServUO files and 71 pinned parents before writing, and every one of the seven findings above
(§14.2 ×2, Phoenix, Swiftflight, talismans, SpinedBloodworm, DarkwoodCrown) came out of that reading, not out
of the compiler. Two tool traps for the next agent: the shell truncates a command near 8 KB (write scripts
with the file tool), and Python cannot open a file under a ~250-character path (the session scratch folder;
use a short work folder such as `D:\UO\cc9-batch4-work`).

### 14.9 What batch 4 leaves

- **Q-041** (Swiftflight / `BaseSetRanged`) and **Q-042** (Bestial hooks), both non-blocking.
- **The 320 bucket is now resolved** except the **120 plain** files (189 − 20 − 49); set armour 0, carrier-
  blocked 0, not-candidates 18. **In-row 81: 29 left** (40 − 11), among them the five remaining Bestial pieces,
  `VirtuososArmbands`/`VirtuososKilt`, `VillainousEpiphany`. Co-port 10 and upstream/carrier 44 untouched.
- **The client spot check** has never happened and now covers 245 files across four batches.
- **The deploy that closes the window.** Everything re-parented in S10, batch 3 and batch 4 is free only
  until `sl-modernuo:latest` is rebuilt and deployed; after that, a re-parent costs a wipe of the type.
  `docs/gap-register.md` already carries this with Chase's name on it. Nothing in this batch changes that.

### 14.10 File list — batch 4 (125 new ServUO files, 3 edited)

Edited:
```
Items/Equipment/Weapons/GargishDagger.cs    re-parented BaseKnife -> BaseSetWeapon
Items/Equipment/Weapons/GargishBattleAxe.cs    BaseAxe members reproduced (14.2)
Items/Artifacts/Equipment/Armor/Sets/BaseSetWeapon.cs    parent BaseWeapon -> BaseMeleeWeapon (14.2)
```

Set-armour bucket (85: 79 set pieces + the 6 Phoenix):
```
Items/Artifacts/Equipment/Armor/Sets/Assassin/AssassinArms.cs
Items/Artifacts/Equipment/Armor/Sets/Assassin/AssassinChest.cs
Items/Artifacts/Equipment/Armor/Sets/Assassin/AssassinGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Assassin/AssassinLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodChest.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodCrown.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodGauntlets.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodLeggings.cs
Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodPauldrons.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleGauntlets.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleGreaves.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleTunic.cs
Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleVambraces.cs
Items/Artifacts/Equipment/Armor/Sets/Hunter/HuntersArms.cs
Items/Artifacts/Equipment/Armor/Sets/Hunter/HuntersGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Hunter/HuntersLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Hunter/HuntersTunic.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationArms.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationCap.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationChest.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsBascinet.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsCloseHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsFemalePlateChest.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsNorseHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateArms.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateChest.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Mage/LeafweaveChest.cs
Items/Artifacts/Equipment/Armor/Sets/Mage/LeafweaveGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Mage/LeafweaveLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Mage/LeafweavePauldrons.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonArms.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonBascinet.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonChest.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathArms.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathBoneHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathChest.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Necromancer/DeathLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinArms.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinChest.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Paladin/PaladinLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutArms.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutBustier.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutChest.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutCirclet.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutFemaleChest.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutSmallPlateJingasa.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererArms.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererChest.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererFemaleChest.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererSkirt.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/CompassionArms.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/HonestyGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/HonorLegs.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/JusticeBreastplate.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososCollar.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososKidGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososTunic.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixArms.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixChest.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixGloves.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixGorget.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixHelm.cs
Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixLegs.cs
```

Carrier-blocked (40 files; Swiftflight declined, Q-041):
```
Items/Artifacts/Equipment/Armor/BasiliskHideBreastplate.cs
Items/Artifacts/Equipment/Armor/CrownOfArcaneTemperament.cs
Items/Artifacts/Equipment/Armor/KelpWovenLeggings.cs
Items/Artifacts/Equipment/Armor/ProtectoroftheBattleMage.cs
Items/Artifacts/Equipment/Armor/WardedDemonboneBracers.cs
Items/Artifacts/Equipment/Armor/WallOfHungryMouths.cs
Items/Artifacts/Equipment/Clothing/WardensArmorOfAugmentation.cs
Items/Artifacts/Equipment/Jewelry/BraceletOfPrimalConsumption.cs
Items/Artifacts/Equipment/Jewelry/Lavaliere.cs
Items/Artifacts/Equipment/Weapons/DraconisWrath.cs
Items/Artifacts/Equipment/Weapons/JadeWarAxe.cs
Items/Artifacts/Equipment/Weapons/ResonantStaffOfEnlightenment.cs
Items/Artifacts/Equipment/Weapons/StoneDragonsTooth.cs
Items/Artifacts/Equipment/Armor/Sets/Juggernaut/Evocaricus.cs
Items/Artifacts/Equipment/Armor/Sets/Luck/EtoileBleue.cs
Items/Artifacts/Equipment/Armor/Sets/Luck/LuneRouge.cs
Items/Artifacts/Equipment/Armor/Sets/Luck/NovoBleue.cs
Items/Artifacts/Equipment/Armor/Sets/Luck/SoleilRouge.cs
Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererHat.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososCap.cs
Items/Artifacts/Equipment/Weapons/PetrifiedSnake.cs
Items/Artifacts/Equipment/Armor/Sets/Marksman/Feathernock.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/HumilityCloak.cs
Items/Artifacts/Equipment/Armor/Sets/Virtue/SacrificeSollerets.cs
Items/Artifacts/Equipment/Jewelry/DragonJadeEarrings.cs
Items/Artifacts/Equipment/Jewelry/ObsidianEarrings.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososEarpieces.cs
Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososNecklace.cs
Items/Artifacts/Equipment/Armor/BritchesOfWarding.cs
Items/Artifacts/Equipment/Armor/DefenderOfTheMagus.cs
Items/Artifacts/Equipment/Armor/ResonantShieldOfVengeance.cs
Items/Artifacts/Equipment/Armor/Sets/Juggernaut/MalekisHonor.cs
Items/Artifacts/Equipment/Weapons/StaffOfResonance.cs
Items/Artifacts/Equipment/Armor/SpinedBloodwormBracers.cs
Items/Artifacts/Talismans/FrostguardTalisman.cs
Items/Artifacts/Talismans/JadeSnakeHead.cs
Items/Artifacts/Equipment/Armor/Sets/Bestial/BeastialSetHelper.cs
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialArms.cs
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialEarrings.cs
Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialNecklace.cs
```
