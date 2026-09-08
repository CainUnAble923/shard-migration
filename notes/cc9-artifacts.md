# CC9 — Artifacts and equipment: batch 1, and the row re-costed

**Status: batch 1 ported, built green through `build.sh`, headless-verified. The row is NOT
"88% needs nothing built". Partial row with an honest boundary; next batch named in §11.**

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
family, the 81 / 10 / 44 S9 buckets are otherwise as S9 measured them** except that batch 1
plus ModernUO's gargish types satisfy the dependency of **53 of the 81 in-row files** (34
costumes on `BaseCostume`, 19 on gargoyle names — list in §12), so those are now plain ports.

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
| Headless start / save / shutdown, then reload | see §9 | |

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

The 617 → 621 / 90 → 91 growth is the ClusterF seeders, as in CC2 and CC3. Logs:
`headless-run1.log`, `headless-run2.log` in the task's work folder.

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

**Done:** 31 files / 34 types in `server/customizations/Items/`, green, reflected, headless
run in §9. `tools/progress-state.json` updated; `python tools/progress.py` run.

**Remaining in the row, by bucket (§4):** 189 − 20 = **169 plain** files not yet ported;
83 − 4 = **79 set-armour** re-parents; 13 + 17 = **30 carrier-blocked** (decision, §5);
the 81 in-row of which 53 are now unblocked; 10 co-port; 44 upstream/carrier as S9 listed.

**Next batch (CC9 batch 2), in this order, ~30 files, pre-flighted with the §3 method:**

1. The 34 costumes in `Items/Equipment/Suits/` — now plain, all `BaseCostume(body[, hue])`
   one-liners; check each `CostumeBody` value and the two that set `CostumeHue`.
2. The in-row artifacts that batch 1 unblocked: `BritchesOfWarding`, `CastOffZombieSkin`
   (from `GargishLeatherArmsType2`), `CuffsOfTheArchmage` (`GargishStoneArmsType1`),
   `GiantSteps` (`GargishStoneLegsType1`), `PillarOfStrength`, `BreastplateOfTheBerserker`,
   `StoneDragonsTooth`, `PetrifiedSnake` (`SerpentstoneStaff`), `DragonJadeEarrings`,
   `ObsidianEarrings`, `Glasses` → `NightEyes`, `CollectionsBritLibraryGlasses`,
   `VirtuososEarpieces`, `VirtuososNecklace`, `SpinedBloodwormBracers` (`GargishClothArmsType1`).
3. Then the plain `Items/Equipment/Weapons/Gargish*` (19 files, all the `GargishKatana` shape)
   and `Items/Equipment/Jewelry/*` (11 remaining), which are the cheapest files on the row.

Do **not** start the 30 carrier-blocked files or CC4 until Q-037 is answered.

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

### In-row files unblocked by batch 1 or by ModernUO's gargish types (53)

The 34 `Items/Equipment/Suits/*Costume.cs` (on `BaseCostume`), plus `BritchesOfWarding`,
`CastOffZombieSkin`, `CuffsOfTheArchmage`, `PillarOfStrength`, `BestialArms`*,
`BestialEarrings`*, `BestialNecklace`*, `VirtuososEarpieces`, `VirtuososNecklace`,
`SpinedBloodwormBracers`, `CollectionsBritLibraryGlasses`†, `Glasses`, `DragonJadeEarrings`,
`ObsidianEarrings`, `BreastplateOfTheBerserker`, `GiantSteps`, `PetrifiedSnake`,
`StoneDragonsTooth`, `VillainousEpiphany`‡. (* still need `BestialSetHelper`; † still needs
`Glasses`; ‡ still needs the Epiphany helper and two more gargish plate pieces.)

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
