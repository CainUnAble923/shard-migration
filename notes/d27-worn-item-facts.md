# D27: the facts that assert on worn items, audited

2026-09-27. Bug-list **D27**. Work is in `D:\ShatteredLegacy`, uncommitted, not deployed.

- The guard: `server/tests/Route/TestHostTileData.cs`, one fact.
- Nothing else in `server/tests/` changed. No production code changed.

**The headline: bucket A is zero.** Of 147 facts (148 test cases), none is a false pass because
of D27. That is not because the facts were careful about layers. It is because, apart from D26's
fact, **no fact goes through a path that checks a layer at all**. Every other fact puts items on a
mobile with `Mobile.AddItem`, which never looks at the layer, and every layer or weight a fact
asserts belongs to an item that sets it in its own code.

The audit found one real defect instead, which D27 had been hiding: **`BestialArms` is on the
chest layer on the live shard, not the arms layer.** Section 4. And it found that the brief's
explanation of why the set facts never tripped over D27 is not quite right. Section 1.

---

## 1. The brief's §1, checked

| Claim | Checked against | Result |
|---|---|---|
| `TileData`'s static constructor returns early under `Core.IsRunningFromXUnit` | pinned `Server/TileData.cs:293-301` | **true** |
| only `Load` sets `MaxItemValue`, at `:381` | same file | **true, line is `:382`**. `:381` sets `MaxLandValue`. The land table is skipped by the same early return, which is the half the spawner facts already document |
| `Item.ItemData` is `ItemTable[m_ItemID & TileData.MaxItemValue]` | pinned `Server/Items/Item.cs:732` | **true** |
| `BaseArmor` takes its layer from `ItemData.Quality` | pinned `UOContent/Items/Armor/BaseArmor.cs:166` | **true, and incomplete**: `BaseWeapon` does the same at `UOContent/Items/Weapons/BaseWeapon.cs:199`. Those are the only two in pinned (`grep ItemData.Quality`). So every weapon that does not set its own layer is also `Invalid` here: a `Dagger`, a `Longsword`, a `CompositeBow`. `Bow` sets `TwoHanded` itself (`Bow.cs:13`), as do most two-handers |
| `Item.CanEquip` rejects `Invalid` | pinned `Server/Items/Item.cs:2150` | **true**. `BaseArmor.CanEquip`, `BaseClothing.CanEquip` and `BaseWeapon.CanEquip` all end in `base.CanEquip`, so the rule reaches every kind |
| "every armour piece built in a test is on `Layer.Invalid`" | the above | **true unless the class sets its own layer**. `GargishEarrings` and `GargishNecklace` are `BaseSetArmor` and set `Layer` in their constructors, so they are on real layers in the host |
| "The existing armour-set facts sidestep it by setting `item.Layer` by hand, which is why four months of work never tripped over it" | the set system and a probe (section 3.2) | **not the reason**. They would never have tripped over it anyway. They put pieces on with `Mobile.AddItem` (`Server/Mobiles/Mobile.cs:6616`), which has no layer check, and `SetHelper` finds pieces by walking `Mobile.Items` (`SetItem.cs:236-430`), not by layer. **With all nine hand-set layers deleted, all 18 set facts still pass.** The hand-set layer protects nothing they assert. What it does do is hide the layer the item really gets, and that is how `BestialArms` got through |

And one item in the brief's §2 scope list: **`Bounds` is not an `ItemData` member.** The struct has
`Name`, `Flags`, `Weight`, `Quality`, `Animation`, `Quantity`, `Value`, `Height` and `CalcHeight`,
plus flag-derived booleans (`TileData.cs:37-107`). A container's `Bounds` comes from its gump data,
and a spawner's `SpawnBounds` from the spawner. I treated "Bounds" as covered by the spawner facts'
map placement, which is the land half and not D27 (section 2, bucket D).

---

## 2. The audit

147 facts in 28 files, 148 test cases (the D26 theory has two). Counted from
`grep -rn -E '^\s*\[(Fact|Theory)' server/tests`; the build's own count before this task was 148.
**Every fact was read.** The in-scope search started from greps for `Layer`, `ItemData`,
`FindItemOnLayer`, `.Items`, `EquipItem`, `AddItem`, `Weight`, `Flags`, `Height`, `TileData`,
`Backpack`, `Corpse`, `CanEquip`, `.Weapon`, `AwardArtifact`, `GiveArtifact`, `ClaimRewards`,
`TryDropItem` and `OnDragDropInto`, and then each hit was read in its fact, and each production path
it drives was read in the customizations or pinned.

Two facts about the host decide most of the table, so they are stated once here:

- **`Mobile.AddItem` is layer-blind** (`Mobile.cs:6616-6661`): no `CanEquip`, no `CheckEquip`, no
  conflict check. Every creature outfit in the customizations is put on this way (48 `AddItem` calls
  under `Mobiles/`); only `CharacterCreation.cs` and `PetMimic.cs` call `EquipItem`. So "the creature
  carries a Sai" is true in the host whatever layer the Sai is on, and would be true live.
- **Every item weighs 0 unless its class says otherwise** (`Item.DefaultWeight`, `Item.cs:448-466`,
  returns 0 for an ID above `MaxItemValue`). So a fact asserting a non-zero weight can only pass if
  the weight is in code, and no container weight limit ever refuses anything here.

### Bucket A: false passes. **0**

None. The candidates that most looked like one, and why each is not:

- Negative assertions on equipment: `DoesNotContain(melee.Items, BaseWeapon)` (Batch 7 `:382`),
  `Null(masked.FindItemOnLayer(Helm))` (Batch 3 `:260`), "no legs anywhere" (D26 `:161`). None can be
  made true by D27: the first two rest on `AddItem`, which D27 does not touch, and the third searches
  worn and packed items together.
- Layer assertions: every one (`Layer.Gloves` on three kilts, `InnerTorso` on the mantle, `Helm` on the
  kin mask, `TwoHanded` on bows, `OuterTorso` on the burning mage's robe) is on clothing, a jewel, a
  quiver or a `Bow`, all of which set their own layer. None is on an item whose layer comes from tile
  data, which is the only way D27 could have supplied the expected value.
- Weight assertions: all nine expect a non-zero weight, which D27 can only make fail, not pass.

### Bucket B: works around it. **19 facts, 20 test cases**

Two workarounds exist, and only one of them is load-bearing.

| # | Fact | Workaround |
|---|---|---|
| B1 | `Engines/CharacterCreation/GargoyleStartingClothesVerification.cs:115` `AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs` (×2) | **Seeds six real rows and sets `MaxItemValue = 0xFFFF` by reflection**, restoring both in `finally`. The only fact that drives an `EquipItem` path, and so the only one where the workaround matters. Its worn-and-layer assertions depend on it; its two D26 assertions do not |
| B2 | `Items/Artifacts/Equipment/Armor/Sets/ArmourSetBonusVerification.cs:37` `AloronSetGrantsItsSetBonus` | hand-set layer in `Wear` (`:31`), then `AddItem` |
| B3 | `…/ArmourSetBonusVerification.cs:129` `StockArmourIsUnaffected` | same |
| B4 | `…/ArmourSetBonusVerification.cs:145` `TigerPeltAloneIsNotASetItem` | same |
| B5 | `…/AbsorptionAttributesVerification.cs:78` `AbsorptionAggregatesAcrossEquippedItems` | same (`Wear` at `:32`) |
| B6 | `…/AbsorptionAttributesVerification.cs:97` `StockArmourEatsNothing` | same |
| B7 | `…/AbsorptionAttributesVerification.cs:113` `ACompletedAloronSetEatsColdDamage` | same |
| B8 | `…/AbsorptionAttributesVerification.cs:159` `ColdDamageThroughAosDamageReachesTheEater` | same |
| B9 | `…/ArmourSetCompletionVerification.cs:95` `AllEightVirtuePiecesCompleteTheSet` | same (`Wear` at `:31`) |
| B10 | `…/ArmourSetCompletionVerification.cs:170` `TheVirtueTooltipSaysEightPiecesAndThenFullSet` | same |
| B11 | `…/ArmourSetCompletionVerification.cs:268` `EachGargoyleHalfCompletesWithItsKilt` | same. **Wears `BestialArms` on `Arms`; the live item is on `InnerTorso`** (section 4) |
| B12 | `…/ClothingSetCarrierVerification.cs:82` `ACompletedClothingSetReachesTheMobile` | same (`Wear` at `:76`); redundant, the pieces are clothing and already on those layers |
| B13 | `…/ClothingSetCarrierVerification.cs:144` `StockClothingIsUnaffected` | same, redundant |
| B14 | `…/JewelSetCarrierVerification.cs:76` `ACompletedJewelSetReachesTheMobile` | same (`Wear` at `:70`), redundant |
| B15 | `…/MarksmanSetVerification.cs:40` `ABowImplementingISetItemCompletesTheSetWithTheQuiver` | same (`Wear` at `:34`), redundant: `Bow` and the quiver set their own |
| B16 | `…/QuiverSetCarrierVerification.cs:72` `ACompletedQuiverSetReachesTheMobile` | same (`Wear` at `:66`); the quiver's is redundant, the test armour's is not |
| B17 | `…/ShieldSetCarrierVerification.cs:84` `ACompletedShieldSetReachesTheMobile` | same (`Wear` at `:78`) |
| B18 | `…/ShieldSetCarrierVerification.cs:162` `StockShieldIsUnaffected` | same |
| B19 | `…/WeaponSetCarrierVerification.cs:61` `ACompletedWeaponSetReachesTheMobile` | same (`Wear` at `:55`). **The second sword is worn on `TwoHanded`; a viking sword is `OneHanded`** in the shard's tiledata, so the "set" is two one-handers in both hands, which a player cannot wear. Harmless for a carrier test with test-local pieces, and worth knowing |

**The menu of workarounds, then, is one item long.** Seeding rows plus raising `MaxItemValue` is
the only thing that makes the host behave like the shard. Setting `item.Layer` by hand before
`AddItem` makes a fact *look* like it wears something on a real layer, and section 3.2 shows none
of B2-B19 depends on it.

### Bucket C: in scope and sound. **24 facts**

| # | Fact | Why it is sound |
|---|---|---|
| C1 | `…/ArmourSetCompletionVerification.cs:217` `TheTwoKiltsAreGargoyleKiltsOnTheClothingCarrier` | `Layer.Gloves` is the kilts' constructor argument (`BestialKilt.cs:19`); `Weight 5.0` is their `DefaultWeight` override (`:38`) |
| C2 | `…/MarksmanSetVerification.cs:107` `SwiftflightSetStateSurvivesASerializationRoundTrip` | `Layer.TwoHanded` is `Bow`'s own. (A separate weakness, not D27: see section 6) |
| C3 | `Mobiles/Normal/CC6Batch1CreatureVerification.cs:324` `TheRestOfTheBatchKeepsItsServUOShape` | the gremlin's `TwoHanded` item is `new Bow()` (`Gremlin.cs:37`), on its own layer |
| C4 | `Mobiles/Normal/CC6Batch2CreatureVerification.cs:259` `TheRestOfTheBatchKeepsItsServUOShape` | outfit presence in `Mobile.Items` (Sai, Wakizashi, JinBaori, Kasa, Bandana, a weapon, a skirt): `AddItem` is layer-blind |
| C5 | `…/CC6Batch2CreatureVerification.cs:185` `TheFurClusterShearsOnceThroughTheBladedItemRoute` | fur reaches the pack through `TryDropItem`, a weight check (`HighPlainsBoura.cs:75`); an empty pack takes it live too, and the fact does not claim the full-pack branch |
| C6 | `Mobiles/Normal/CC6Batch3CreatureVerification.cs:206` `TheOrcScoutBandagesItselfSparesAKinMaskAndBurnsItOffAnAggressor` | the bow sets its own layer; `OrcishKinMask` is a `BaseHat` (pinned `Hats.cs:368`), so `Helm` is real |
| C7 | `…/CC6Batch3CreatureVerification.cs:438` `TheSixItemsCarryTheirServUOValues` | weights 1.0 and 0.1: the host can only give 0, so they come from code |
| C8 | `Mobiles/Normal/CC6Batch4CreatureVerification.cs:185` `PeerlessKeyIsTheThreeKeysFinalParentAndCountsDown` | weights 1.0, 1.0, 2.0, from code; the orb's trip into the pack is weight-gated and unremarkable |
| C9 | `…/CC6Batch4CreatureVerification.cs:263` `TheHighExecutionerIsAGeneratedSubclassOfOurOwnAssassin` | outfit presence (the Sai and the `StuddedMempo` are on `Invalid` here); `AddItem` is layer-blind |
| C10 | `…/CC6Batch4CreatureVerification.cs:454` `TheChickenLizardLaysForItsBondedOwnerAndPersistsTheCooldown` | the egg's route is a `TryDropItem` test; an empty pack accepts it live too |
| C11 | `Mobiles/Normal/CC6Batch5CreatureVerification.cs:245` `TheArtifactGoesToThePlayerWhoDidTheMostDamage` | `AxeOfAbandon` into the pack; the refusing pack is full by **count** (`MaxItems` candles), which D27 does not touch. No weight limit is claimed |
| C12 | `…/CC6Batch5CreatureVerification.cs:565` `TheFiveNewArtifactsSitOnTheirFinalParents` | the mantle's and kilt's layer and weight are set in code; the three weapons are only constructed |
| C13 | `Mobiles/Normal/CC6Batch7Verification.cs:301` `TheGrandMageIsAGeneratedSubclassOfOurMageAndDropsTheKeyOnEveryDeath` | `Kasa` presence, clothing |
| C14 | `…/CC6Batch7Verification.cs:349` `TheRatmenKeepTheirServUOShape` | bow presence; `DoesNotContain(BaseWeapon)` would see a weapon added by `AddItem` on any layer |
| C15 | `Mobiles/Bosses/CC6Batch8Verification.cs:173` `BasePeerlessReachesEveryMLSpecialDropAndPacksTheSixResources` | the corpse holds ML armour pieces; a corpse takes them by `DropItem`, layer-blind and weight-blind |
| C16 | `…/CC6Batch8Verification.cs:277` `NavreysLeavesCarryTheirServUOValues` | the eye's weight 1.0 is in code |
| C17 | `…/CC6Batch8Verification.cs:313` `NavreyDropsHerLootThroughRealKillsAndNeverTheEye` | `Tangle1` (clothing) into the pack |
| C18 | `…/CC6Batch8Verification.cs:525` `BaseSABossAwardsAnArtifactToADamagerAndTheDragonDropsItsHead` | `LifeSyphon` into the pack, weight-gated, near-empty pack |
| C19 | `…/CC6Batch8Verification.cs:744` `MedusaConstructsWithServUOValuesAndHerLeavesCarryTheirs` | bow presence. Note that `CompositeBow` sets **no** layer of its own, so hers is on `Invalid` here and on `TwoHanded` live; presence holds either way |
| C20 | `…/CC6Batch8Verification.cs:841` `MedusaIsHarvestedAliveOnAOneMinuteCooldownAndCarvedDeadForDarkScales` | scales into the pack by a weight-gated route; the pack is far from any limit |
| C21 | `Services/Revamped Dungeons/Shame Revamped/ShameRevampedVerification.cs:587` `ThePortedCreaturesCarryWhatServUOGivesThem` | the burning mage's `OuterTorso` item is a robe, clothing |

Three more drive a reward into a pack through `AddToBackpack` and assert it arrived, which is a
weight check that cannot fail here and would not fail live on an empty pack: **C22**
`Engines/MLQuests/AthenaeumIsleQuestVerification.cs:205` (a book), **C23**
`Engines/MLQuests/NewHavenQuestBoardVerification.cs:557` (`RecarosRiposte`, a weapon), **C24**
`Services/Revamped Dungeons/Shame Revamped/ShameRevampedVerification.cs:527` (the whetstone, via
`CorrosiveAsh.cs:46`).

Across bucket C, the weight half of D27 has one consequence worth saying once: **no fact has ever
exercised a container refusing an item for weight**, because nothing here weighs anything. Every
"it arrived in the pack" above is also true live on a near-empty pack, and none of them claims the
full-by-weight branch. The one fact that does test a refusal (C11) fills the pack by item count.

### Bucket D: out of scope. **104 facts**

147 − 0 (A) − 19 (B) − 24 (C) = **104**, each read and found to assert nothing that depends on a
layer, an equip, or an `ItemData` value. Two groups inside it are close enough to the line to name:

- **Seven spawner facts** touch tile data through map placement: Batch 6 `:72`, Batch 7 `:102`,
  Batch 8 `:355`, `:711`, `:1042`, Despise `:52`, Shame `:104`. That is the **land** half of the same
  early return (`LandTable`, `MaxLandValue`), not D27, and each file's header already says so and
  routes around it (`SpawnBounds = default`, or asserting containment rather than placement).
- **Twelve facts in the set files construct armour or weapons and never put them on anyone.** The
  set files hold 32 facts: 18 are B2-B19, 2 are C1-C2, and these 12 are the rest. Seven serialization
  round trips (Absorption `:204`, SetBonus `:161`, Clothing `:161`, Jewel `:153`, Quiver `:152`,
  Shield `:179`, Weapon `:143`); `AloronPiecesCarryTheirColdEater` (Absorption `:62`);
  `TheStockVirtuePiecesCarryServUOsValuesAndTheSetId` (Completion `:45`); and three type tests,
  `StockJewelIsUnaffected` (`:140`), `StockQuiverIsUnaffected` (`:140`), `StockWeaponIsUnaffected`
  (`:130`). Constructing an item on `Invalid` is harmless when nothing reads where it is.

**Totals: A 0, B 19 (20 cases), C 24, D 104. 147 facts, 148 cases.** With the guard, 148 and 149.

---

## 3. Proofs

Two build runs. **The probe run** (`build.sh --tests-only`) carried three temporary changes at once,
each described below and each reverted afterwards. **The final run** is a full `build.sh` with none
of them: only the guard file differs from HEAD.

### 3.1 The guard

`server/tests/Route/TestHostTileData.cs`, fact `TheHostHasNoItemTileDataSoArmourAndWeaponsAreOnNoLayer`,
beside `ShardTestClock.cs` because it is the same kind of thing: a written-down truth about the host.
Its header carries the D27 explanation, what it means for a fact author, and what to do when it goes
red. It asserts, in this order:

1. `TileData.MaxItemValue` is **0**;
2. a `new LeatherChest()` (a `BaseArmor`) is on **`Layer.Invalid`**;
3. a `new Dagger()` (a `BaseWeapon` with no layer of its own) is on **`Layer.Invalid`**. This is the
   half the brief left out;
4. `PlayerMobile.EquipItem(chest)` returns **false** and the chest has **no parent**: the silent refusal
   that makes a worn-item assertion vacuous;
5. a plain `new Item(0x13CC)` weighs **0**.

It prints all five values before asserting any, so a red run shows the whole new state, not just
the first difference.

**Red, for the right reason.** In the probe run the guard began by doing what a fixture that loaded
the shard's tiledata would do: `MaxItemValue` set to `0xFFFF` and the two rows it uses seeded with
their real values (leather tunic `0x13CC`: weight 6, quality 13; dagger `0xF52`: weight 1, quality 1),
all restored in `finally`:

```
  Failed ShatteredLegacy.Tests.TestHostTileDataVerification.TheHostHasNoItemTileDataSoArmourAndWeaponsAreOnNoLayer [2 ms]
  Error Message:
   Assert.Equal() Failure: Values differ
Expected: 0
Actual:   65535
  Stack Trace:
     at ShatteredLegacy.Tests.TestHostTileDataVerification.TheHostHasNoItemTileDataSoArmourAndWeaponsAreOnNoLayer() in /build/modernuo/Projects/UOContent.Tests/Tests/Route/TestHostTileData.cs:line 91
  Standard Output Messages:
 MaxItemValue=65535; LeatherChest layer=InnerTorso, EquipItem=True, parent=the mobile; Dagger layer=FirstValid; plain item weight=6
```

All five readings moved, so every assertion discriminates, not only the first. (`FirstValid` is how
.NET names `Layer` value 1: the enum declares `FirstValid = 0x01` before `OneHanded = 0x01`.)

**Green**, with the simulation removed, is the final run:

```
== 1/3 building builder stage (patches gate) ==============================
== 2/3 running ShatteredLegacy.Tests tests (test gate) ==========================
  Passed ShatteredLegacy.Tests.TestHostTileDataVerification.TheHostHasNoItemTileDataSoArmourAndWeaponsAreOnNoLayer [1 ms]
Total tests: 149
     Passed: 149
[tests] 149 test(s) passed.
== 3/3 building runtime image sl-modernuo:latest =================================
Built sl-modernuo:latest with patches applied and 149 shard test(s) passing.
```

The only difference between the red run and this one, for the guard, is the simulation block.

### 3.2 The hand-set layers protect nothing

In the probe run, `item.Layer = layer;` was deleted from **all nine** `Wear` helpers (the brief's
"armour-set facts" are eight files, and `AbsorptionAttributesVerification.cs:32` is the ninth), and
the builder image was checked afterwards to prove the edit reached the build tree:

```
$ docker run --rm sl-uo-builder:latest sh -c 'cd .../Tests/Items/Artifacts/Equipment/Armor/Sets && grep -c "D27 PROBE" *.cs; ...'
AbsorptionAttributesVerification.cs:1
ArmourSetBonusVerification.cs:1
... (all nine)
no hand-set layer left in any Wear helper
```

Result: **all 32 facts in the nine set files passed**, including all 18 that call `Wear`. The run's
only two failures were the two deliberate reds (3.1 and section 4):

```
Total tests: 150
     Passed: 148
     Failed: 2
```

148 passed = the 148 existing cases, every one of them. So nothing any set fact asserts depends on
the layer it sets. The helpers were restored with `git checkout` afterwards; their diff had been
exactly one line each.

This is the honest version of the brief's §1 sentence. The set facts did not dodge D27; D27 never
reached them, because `AddItem` does not check layers and `SetHelper` does not read them. The
hand-set layer is a comment that happens to compile.

---

## 4. `BestialArms` is on the chest layer

**Ours to fix, not fixed here.** A port error, CC9 batch 4, and the audit's one real find.

**The defect.** ServUO's `BestialArms` derives from `GargishLeatherArms`, whose constructor calls
`base(0x302)` (ServUO `Items/Equipment/Armor/GargishLeatherArms.cs:17`). `BaseArmor`'s constructor
takes the layer from the tile row **at that moment** (ServUO `BaseArmor.cs:2373`), so the layer comes
from `0x302`: **Arms**. Only then does `BestialArms` set `ItemID = 0x4052` (ServUO
`Bestial/BestialArms.cs:27`), and changing an item ID does not recompute the layer. Our port, moved
onto `BaseSetArmor`, passes `0x4052` straight to the base call
(`server/customizations/Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialArms.cs:14`, and its own
comment says so), so the layer comes from `0x4052`, whose row is `Gargoyle Armor Plate`,
quality 13: **InnerTorso**.

This is AGENTS.md's final-parent rule in a new shape: "changing a parent means porting the old
parent's members too", and here the member is not in any file. It is a value `BaseArmor` computes
from the parent's item ID.

**Proof, from the file.** The shard's own `client-data/classic-client/tiledata.mul`, D26's parser:

```
0x302  gargoyle_leather_arm   quality 19  Arms
0x4052 Gargoyle Armor Plate   quality 13  InnerTorso
```

**Proof, headless.** A temporary fact in the probe run seeded `0x302`, `0x304` (a gargish leather
chest) and `0x4052` with those values, raised `MaxItemValue`, restored all of it in `finally`, and
asserted what ServUO does:

```
  Failed ShatteredLegacy.Tests.D27BestialArmsProbe.BestialArmsIsOnTheArmsLayerAsServUOsIs [4 ms]
  Error Message:
   Assert.Equal() Failure: Values differ
Expected: Arms
Actual:   InnerTorso
  Standard Output Messages:
 GargishLeatherChestType1 0x304 layer=InnerTorso equipped=True; BestialArms 0x4052 layer=InnerTorso equipped=False; GargishLeatherArmsType2 0x302 layer=Arms equipped=True
```

**What a player sees**: a gargoyle already wearing a chest piece cannot put Bestial Arms on at all
(`equipped=False` above), and one wearing Bestial Arms cannot wear a chest piece. The set itself
still completes, because its four pieces (InnerTorso, Earrings, Neck, Gloves) do not collide.
Not checked in a client.

**Why no test saw it.** `EachGargoyleHalfCompletesWithItsKilt` (B11) wears it with
`Wear(m, new BestialArms(), Layer.Arms)`. The hand-set layer is precisely what hid it.

**How I looked for more.** Two sweeps across every type in `server/customizations` (918 class
names), both regex-based, so "none found" means none of these two shapes, not none at all:

1. ServUO constructors of ported types that reassign `ItemID` after the base call: six hits. Four
   are weapons (`SkullLongsword`, `GargishSkullLongsword`, `SkullGnarledStaff`,
   `GargishSkullGnarledStaff`), which our port constructs exactly as ServUO does, and whose new IDs
   are on the same layer as the old anyway (`0xA341`/`0xA345` OneHanded like `0xF61`;
   `0xA343`/`0xA347` TwoHanded like `0x13F8`). `MysticsGarb` is a robe, whose layer is a constructor
   argument. **`BestialArms` is the only one that changes layer.**
2. Ported types where ServUO sets `Layer = Layer.X` explicitly and ours does not (as an assignment or
   a base argument): **none**.

And the hand-set layer of every piece the set facts wear, against the real tiledata (script in
section 7): **18 of 20 match.** The two that do not are `BestialArms` (Arms by hand, InnerTorso
really) and the second test sword in B19 (TwoHanded by hand, OneHanded really, a deliberate device in
a carrier test).

**The fix is small, and it is Chase's**, because it changes live content: one line,
`Layer = Layer.Arms;` in the constructor, reproducing ServUO's effective value. Saves: `Item`
serializes a layer that is not `Invalid`, so any existing `BestialArms` keeps `InnerTorso` after a
code fix. The live save cannot hold one (D25: no CC9 type in it). The LAN test shard runs
`sl-modernuo:latest` and **may** hold one; unverified. The fact that should go with the fix is
B11 with the three rows seeded and `Layer.Arms` asserted, which is the probe above. Opened as
**Q-065**.

---

## 5. The shared mechanism: not built

The brief's condition was "more than a couple" of bucket A entries. There are none, so there is
nothing for a mechanism to serve today, and one user of the reflection (D26's fact) is not a
pattern yet. **The trigger is the second fact that drives an `EquipItem` path with armour or a
weapon**, most likely the fix for Q-065 or any of D26's S14-S18 profession differences if one is
ever fixed. At that point the reflection in `GargoyleStartingClothesVerification` should move out,
not be copied.

**What it should be, when it is built**, so the decision is not re-derived:

- One `IDisposable` scope in `server/tests/Route/`, e.g. `using var _ = TestTileRows.Seed(TileRows.GargishLeatherArms, TileRows.BestialArms);`,
  which saves `MaxItemValue` and each named row, raises `MaxItemValue` to `0xFFFF`, writes the rows,
  and restores all of it on `Dispose`. That is D26's `finally`, once.
- The rows as named constants in one file, each with the comment D26 already uses: the item ID, the
  values, and "read from `client-data/classic-client/tiledata.mul` (3,188,736 bytes) by the parser in
  `notes/d26-gargoyle-kilt.md` §3.2". Only rows a fact needs. **No `tiledata.mul` at test time.**
- **Parallel safety: not safe, and acceptable here, for a reason that can be checked.** `TileData`
  is static. All 27 test classes under `server/tests/` carry `[Collection("Sequential UOContent Tests")]`
  (counted; `PropertyListReader.cs` is a helper with no facts), and `build.sh` runs only the
  `ShatteredLegacy.Tests` namespace, so no fact that can see the table runs concurrently with one that
  changes it. The scope should say that in its header, and the day a shard test class leaves that
  collection is the day it stops being true. It is the same condition D26's reflection already
  depends on without saying so.

**On setting `MaxItemValue` globally in the fixture: I would not, and not even as a first step.**
Raising the mask alone makes every item read its own row, and in this host every row except a
seeded one is empty, so:

- **layers do not improve at all.** An empty row has quality 0, so every armour piece and one-hander is
  still on `Invalid`; the only thing that changes is which empty row it reads;
- **weights get worse, not better.** `DefaultWeight` turns an empty row's 0 into **1**
  (`Item.cs:448-466`), so every item without its own weight goes from 0 to a uniform, fictional 1
  stone, which is no closer to the shard than 0 and is harder to notice.

So the global mask buys nothing on its own. The change that would make the host honest is **loading
the real `tiledata.mul`**, which is D26's "fixture patch plus a Dockerfile copy step", with the
catch that `client-data/` is outside the build context and is the game client's data, not ours.
That is worth doing only when enough facts need real layers or weights that seeding rows becomes
the bigger cost. We are at one fact. The guard exists so that when it happens, it happens as a
decision.

---

## 6. Seen in passing

None of these is D27, none was fixed, and each is a one-line item for Chase to disposition.

1. **A tautology.** `ShameRevampedVerification.cs:547`:
   `Assert.Equal("Whetstone of Enervation", "Whetstone of Enervation");` compares a literal to itself
   and cannot fail. The item's name is its `LabelNumber`, 1151811 (`WhetstoneOfEnervation.cs:28`), so
   the assertion it was presumably meant to be is `Assert.Equal(1151811, whetstone.LabelNumber)`.
   Small and obvious, but it is not a D27 fact, so it is listed rather than changed.
2. **A round trip that cannot see a lost layer.** `MarksmanSetVerification.cs:141` asserts
   `copy.Layer == TwoHanded` after deserializing, but the copy is built with `new Swiftflight()`,
   whose constructor already sets `TwoHanded` (through `Bow`). If the save dropped the layer, the copy
   would still read `TwoHanded`. The other fields in that fact are zeroed on the copy before the read,
   which is the guard this one lacks.
3. **Weapon-bearing creatures fight with their fists in the host.** `Mobile.Weapon` looks on
   `OneHanded` then `TwoHanded`. A creature carrying a one-hander, or a bow without its own layer (like
   Medusa's `IronwoodCompositeBow`, a `CompositeBow`), has that weapon on `Invalid` here, so any future
   fact about such a creature's melee damage, swing speed or weapon ability through its weapon would
   measure `Fists`. No current fact does. It belongs in the guard's family if one ever does.
4. **B19's two-sword "set"** is two one-handers in both hands (section 2), a configuration no player
   can reach. Fine for a carrier test; misleading if it is ever copied as an example of a weapon set.

---

## 7. Method and scripts

- **Layer check** (`layers.py`, in the session scratchpad, not committed): D26's parser, unchanged,
  over the shard's `tiledata.mul`; it asserts the parse ends at exactly 3,188,736 bytes and that the
  four sanity rows from the D26 note still read correctly, then prints the real layer of every piece a
  set fact wears. 20 pieces, 18 match.
- **ItemID sweep** (`itemid_sweep2.py`): for every class name declared in `server/customizations`,
  find ServUO's class of that name and any `ItemID =` inside its constructors. 17 hits, 11 of them not
  equipment (a grape vine, a door, eggs, creatures' hair). Section 4 has the six that are.
- **Layer-assignment sweep** (`layer_sweep.py`): every ported type where ServUO has
  `Layer = Layer.X` and ours has neither that nor `Layer.X` in its base call. No output.
- **Counts**: facts by `grep -rn -E '^\s*\[(Fact|Theory)'` (147, one theory with two cases);
  collection attributes by `grep -c 'Collection("Sequential UOContent Tests")'` (27 of 27 classes).

No container was started, stopped or restarted. Nothing was deployed. `D:\UO\ServUO-pub57` and
`D:\UO\ModernUO-pinned` were only read. The final `build.sh` built `sl-modernuo:latest`; per D25 the
live shard does not run that image, and per D26 a running container does not pick up a rebuilt image.
