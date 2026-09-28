# D26: the gargoyle starting kilt, and a sweep of the race branches

2026-09-27. Bug-list **D26** (ours, fixed here) and **E4** (upstream ModernUO, to report).
Work is in `D:\ShatteredLegacy`, uncommitted, not deployed.

- The fix: `server/customizations/CharacterCreation.cs`, `AddPants`, the two gargoyle arms.
- The test: `server/tests/Engines/CharacterCreation/GargoyleStartingClothesVerification.cs`, one
  theory, both sexes.

---

## 1. The brief's §1, checked

Every claim in §1 checked out except for the details listed below.

| Claim | Checked against | Result |
|---|---|---|
| Pinned `AddPants` equips `GargishClothLegsType1/2` | pinned `CharacterCreation.cs:796-797` | **true** (the method spans `:787-809`) |
| ServUO `AddPants` equips `GargishClothKiltArmor` | ServUO `Scripts/Misc/CharacterCreation.cs:138-141` | **true** |
| Our file differs from pinned only in `ConstructAvailableStartingCities` | `diff` of the two files | **true**. One hunk, pinned `:131-157` against ours `:131-135`, so our line numbers run 22 below pinned's from there on. Our `AddPants` arms are at `:774-775` |
| Five profession branches in pinned equip a kilt | pinned `:539, :576, :612, :649, :689` | **true** |
| `GargishClothKiltType1` carries `[TypeAlias("Server.Items.GargishClothKiltArmor")]` | pinned `Items/Armor/Cloth/GargishClothKiltType1.cs:6` | **true** (it also aliases `GargishClothKilt`) |
| Kilt and legs carry identical stats | the two files | not re-derived, as instructed. Aside: the **tiledata** weights differ (kilt 2, legs 4), but both classes override `DefaultWeight` to 2.0, so the item weight a player sees is the same |

What §1 left out, and one small correction:

- **Which layers.** Measured from the shard's own `client-data/classic-client/tiledata.mul`
  (3,188,736 bytes), with the parser in section 3.2. The chest `0x405/0x406` is quality 13,
  **InnerTorso**. The kilt `0x407/0x408` is quality 7, **Gloves**. The legs `0x409/0x40A` are
  quality 4, **Pants**. So the kilt sits on the *gloves* layer, not on a legs layer. That is why a
  kilt and legs can be worn together (Q-061) and why the fix cannot collide with anything the
  legs used to occupy.
- **`GargishClothKiltType2` has no `[TypeAlias]`.** ServUO has a `FemaleGargishClothKiltArmor`
  (`Items/Equipment/Armor/GargishClothArmor.cs:539`), and pinned's legs and chest `Type2` files
  alias their ServUO female names, but the kilt `Type2` does not. This is harmless for us, because
  nothing imports a ServUO save. I am recording it because the brief uses `[TypeAlias]` as the
  mapping authority, and for this one type there is no alias to go by.
- **ServUO does not split by sex at character creation.** Its `AddShirt` and `AddPants` equip the
  male-named `GargishClothChestArmor` and `GargishClothKiltArmor` on both sexes, with no female
  branch (ServUO `:97-100`, `:138-141`). Pinned picks `Type2` for female characters. So the fix
  follows pinned's sex split, not ServUO's code, in exactly the way `AddShirt` already does. See
  sweep row S1.

The **warrior** profession path deserves a line because the fix changes something there too. In
pinned, `swordsman / fencer / warrior / mace fighter` `break`s instead of `return`ing
(pinned `:702`), so it goes on to `AddShirt` and `AddPants` after equipping leather chest, arms,
kilt and legs. Before the fix, the cloth legs found Pants taken by the leather legs and went to the
backpack. After it, the cloth kilt finds Gloves taken by the leather kilt and goes to the backpack.
So a warrior gargoyle's backpack now holds a cloth kilt where it used to hold cloth legs. What the
warrior wears does not change. ServUO's warrior carries a spare cloth chest in the same way,
because its `AddShirt` runs for professions up to 3 (ServUO `:259-264`).

---

## 2. The change

`server/customizations/CharacterCreation.cs:774-775`:

```csharp
Race.AllowGargoylesOnly when female => new GargishClothKiltType2 { Hue = hue },
Race.AllowGargoylesOnly             => new GargishClothKiltType1 { Hue = hue },
```

The file had LF line endings and was ASCII before the change, and it still is. It is still
byte-identical to pinned outside the two hunks (the cities hunk and this one).

---

## 3. The test

### 3.1 What it drives

The test calls `CharacterCreation.CharacterCreatedEvent(args)`, the generated event that the login
packet handler raises, and nothing else. It supplies a real `Account` (constructed, then removed
afterwards), a test `NetState` from `PacketTestUtilities.CreateTestNetState()`, profession 0,
`Race.Gargoyle`, and the New Haven `CityInfo`. So the path runs through `OnCharacterCreated`,
`GiveProfessionItems(null)`, `AddShirt`, `AddPants`, `AddShoes` and the real private `EquipItem`.
It does not call `AddPants` through any seam.

It asserts the following:

- the chest on `InnerTorso` is the sex-matched `GargishClothChestType1/2`;
- no `GargishClothLegsType*` is anywhere on the character, worn or packed;
- a sex-matched `GargishClothKiltType1/2` exists, is **worn** (its parent is the mobile), and is
  the item on its own layer;
- the kilt's layer is valid and differs from the chest's.

### 3.2 The one thing the headless path cannot do on its own, and what the test does about it

**The test host has no tile data.** `TileData`'s static constructor returns early when
`Core.IsRunningFromXUnit` (pinned `Server/TileData.cs:293-301`), so `MaxItemValue` stays 0, because
only `Load` sets it (`:381`). `Item.ItemData` is `ItemTable[m_ItemID & TileData.MaxItemValue]`
(`Server/Items/Item.cs:732`), so **every item in a test reads row 0**. `BaseArmor` takes its layer
from `ItemData.Quality` (`UOContent/Items/Armor/BaseArmor.cs:166`), so every armour piece built in a
test is on `Layer.Invalid`. `Item.CanEquip` rejects that (`Server/Items/Item.cs:2150`), and the
creation path's own `EquipItem` then drops the piece into the backpack. That is why the existing
armour-set tests set `item.Layer` by hand.

Without intervention, then, the real path runs but nothing ends up worn, and "occupies different
layers" cannot be asserted. The first probe showed exactly that: chest and legs in the pack on
`Layer.Invalid`. **Seeding the rows alone did not help**, and I found the `& MaxItemValue` mask only
after a probe where the seeded rows made no difference. So for the duration of the fact only, the
test does two things and restores both in `finally`:

1. writes the **six** gargish cloth rows into `TileData.ItemTable`;
2. sets `TileData.MaxItemValue` to `0xFFFF`, the value a real `Load` of this 64-bit-flag file
   gives. The setter is private, so this goes through reflection.

Step 2 has side effects while the fact runs. Every other item now reads its own, still empty, row
instead of row 0. The layer is the same `Invalid` either way. `DefaultWeight` (`Item.cs:448-466`)
goes from 0 to 1 for items that do not override it, which touches only the starting gold, book and
candle. Nothing in the fact reads weight. All 148 shard tests pass with it in place.

The row values were read from the shard's tiledata by this parser, which follows pinned
`TileData.Load` (`:303-380`) field for field:

```python
# 64-bit flags: land header at i==1 and every 32nd after; items 41 bytes, header every 32
off=0
for i in range(0x4000):
    if i==1 or (i>0 and (i&0x1f)==0): off+=4
    off+=8+2+20
for i in range(0x10000):
    if (i&0x1f)==0: off+=4
    # flags u64, weight u8, quality u8, anim u16, u8, qty u8, i32, u8, value u8, height u8, name[20]
    off+=41
```

The parser ends at offset 3,188,736, exactly the file length. Its readings for known items match
their known layers: doublet `0x1F7B` → 17 MiddleTorso, leather tunic `0x13CC` → 13 InnerTorso,
shirt `0x1517` → 5 Shirt, short pants `0x152E` → 4 Pants. The six rows it gives for the gargish
cloth, all with flags `0x404002` and height 1:

| ID | name | weight | quality → layer | anim |
|---|---|---|---|---|
| 0x405 | gargoyle_clothing_ch | 6 | 13 InnerTorso | 592 |
| 0x406 | gargoyle_clothing_ch | 6 | 13 InnerTorso | 593 |
| 0x407 | gargoyle_clothing_ki | 2 | 7 Gloves | 594 |
| 0x408 | gargoyle_clothing_ki | 2 | 7 Gloves | 595 |
| 0x409 | gargoyle_clothing_le | 4 | 4 Pants | 596 |
| 0x40A | gargoyle_clothing_le | 4 | 4 Pants | 597 |

This is test setup; no production code is substituted. The seeded values are the ones the
live server loads from the same file. The layer-inequality assertion is therefore partly
circular: it can only be as right as the seeded rows. The **type** assertions are not circular,
and they are the ones that catch D26.

The assertions are ordered so that **the two D26 assertions come first**: no
`GargishClothLegsType*` anywhere, and a sex-matched kilt present. Those hold or fail whatever layer
the pieces land on, so they would catch D26 with the seeding removed. The worn-and-layer
assertions come after them and do depend on the seeding.

**What it would take to remove the seeding:** give the test host a real `tiledata.mul`.
`client-data/` is uncommitted and not in the builder image, and `TileData.Load` is `internal` to
`Server`, so the change would be a fixture patch plus a copy step in the Dockerfile. That is not
worth doing for this one fact. It is worth doing the first time a second fact needs real layers or
weights, and at that point the reflection here should go.

Other setup, none of which changes the path. These are three startup hooks the fixture never runs,
and each would have stopped the path before it completed:

- `Accounts.Configure()`: otherwise `new Account(...)` throws on `Accounts.NewAccount`.
- `AccountSecurity.CurrentAlgorithm`: otherwise it is `None` and `SetPassword` throws "Do not use
  PasswordProtectionAlgorithm.None". The test sets PBKDF2 directly, because it never checks a
  password.
- `WelcomeTimer.Initialize()`: the last line of `OnCharacterCreated` constructs a `WelcomeTimer`,
  which reads the message table that `Initialize` fills. The timer it starts is never cancelled.
  It targets a mobile the fact deletes, so if a later fact turns the wheel, it sends to a deleted
  mobile with no NetState.
- Stats are given as a valid spread (90 or 80 total, depending on `NewCharacterCreation`). An
  invalid spread falls back to 10/10/10, and Str 10 is below the cloth pieces' `AosStrReq` 20, so
  the equip would fail for a reason unrelated to D26.

### 3.3 Red, then green

**Red** is the unfixed `CharacterCreation.cs` with the finished test,
`docker/uo/build.sh --tests-only`, builder stage passing, test gate failing:

```
  Failed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: False) [30 ms]
  Error Message:
   expected no GargishClothLegsType*, found GargishClothLegsType1
  Stack Trace:
     at ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(Boolean female) in /build/modernuo/Projects/UOContent.Tests/Tests/Engines/CharacterCreation/GargoyleStartingClothesVerification.cs:line 161
  Standard Output Messages:
 worn  Backpack                   layer Backpack  0x0E75
 worn  BankBox                    layer Bank  0x0E7C
 worn  GargishClothChestType1     layer InnerTorso  0x0406
 worn  GargishClothLegsType1      layer Pants  0x040A
 pack  RedBook                    layer Invalid  0x0FF1
 pack  Gold                       layer Invalid  0x0EED
 pack  Dagger                     layer Invalid  0x0F52
 pack  Candle                     layer TwoHanded  0x0A28

  Failed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: True) [1 ms]
  Error Message:
   expected no GargishClothLegsType*, found GargishClothLegsType2
  Standard Output Messages:
 worn  Backpack                   layer Backpack  0x0E75
 worn  BankBox                    layer Bank  0x0E7C
 worn  GargishClothChestType2     layer InnerTorso  0x0405
 worn  GargishClothLegsType2      layer Pants  0x0409
 pack  RedBook                    layer Invalid  0x0FF1
 pack  Gold                       layer Invalid  0x0EED
 pack  Dagger                     layer Invalid  0x0F52
 pack  Candle                     layer TwoHanded  0x0A28

Test Run Failed.
Total tests: 148
     Passed: 146
     Failed: 2

BUILD FAILED: ShatteredLegacy.Tests tests did not pass. No image was built.
```

That is Chase's client observation reproduced headlessly: chest worn, legs worn, no kilt.

**Three earlier red runs do not count, and I record them so nobody mistakes one for the proof.**

1. A compile error in the test: a missing `using Server.Engines.CharacterCreation`.
2. A test-setup exception, `PasswordProtectionAlgorithm.None`. The `WelcomeTimer` gap was then found
   by reading the source before it could throw.
3. A run where the path completed but my seeded rows were ignored because of the `MaxItemValue`
   mask. It failed on `Assert.NotNull(chest)`. Its dump did show legs and no kilt, in the pack, but
   it failed on the wrong assertion.

Only the run above failed on the D26 assertion, for the D26 reason.

**Green** is the fix applied, full `docker/uo/build.sh`, all three steps:

```
== 1/3 building builder stage (patches gate) ==============================
== 2/3 running ShatteredLegacy.Tests tests (test gate) ==========================
  Passed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: False) [34 ms]
  Passed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: True) [1 ms]
Total tests: 148
     Passed: 148
[tests] 148 test(s) passed.
== 3/3 building runtime image sl-modernuo:latest =================================
Built sl-modernuo:latest with patches applied and 148 shard test(s) passing.
```

The only change between red and green is the two lines in section 2. **Not deployed.** Per D25 the
live container runs the `uo-modernuo` image, so a fresh gargoyle on the live shard still gets
legs until Chase deploys. No container was started, stopped or restarted.

**Not verified in a client.** "Fix verified in a client" is a separate claim that has not been made.

---

## 4. The §3 sweep

Scope, as briefed, was the race-conditioned branches of pinned `CharacterCreation.cs` against
ServUO pub57 `Scripts/Misc/CharacterCreation.cs`. That covers `AddShirt`, `AddPants`, `AddShoes`,
hair, and every race branch in `AddSkillItems` (the shield and arms branches the brief names are
two of them). I added `AddBackpack` because ServUO branches on race there. ServUO's ninja branch
at `:707-714` was resolved separately, as asked. Line numbers below are **pinned** and **ServUO**.
Our file is pinned + 0 above `:131` and pinned − 22 below it.

Mapping authority: `[TypeAlias]` in pinned. Resolved: `GargishClothChestArmor` →
`GargishClothChestType1`, `GargishClothKiltArmor` → `GargishClothKiltType1`,
`GargishClothLegsArmor` → `GargishClothLegsType1`, `GargishClothArmsArmor` →
`GargishClothArmsType1`, `GargishLeatherArms/Chest/Kilt` → `GargishLeather*Type1`,
`SerpentStoneStaff` → `SerpentstoneStaff`. **`GargishPlateChest/Arms/Legs/Kilt` and `GargishDagger`
have no class and no alias in pinned.**

### 4.1 Matches

| Branch | Pinned | ServUO | Result |
|---|---|---|---|
| `AddShirt`, gargoyle | `:773-774` | `:97-100` | match (see S1 for the sex split) |
| `AddShirt` / `AddPants`, elf and human | `:772, :776-781, :795, :799-805` | `:78-96, :107-137` | match |
| `AddShoes` | `:811-821` | `:144-150` | match: elf `ElvenBoots`, human `Shoes`, gargoyle nothing |
| Hair and facial hair | `:255-265` | `:234-244` | match: both defer to `race.ValidateHair/ValidateFacialHair`, and neither branches on race itself |
| Parry shield (brief's `:1246`) | `:1242-1252` | `:1295` case | match: `GargishWoodenShield` / `WoodenShield` |
| Wrestling arms (brief's `:1329`) | `:1324-1335` | `:1409` case | match: gargoyle `GargishLeatherArms` ↔ `Type1`, sex split as in S1 |
| Fencing, Macing, ItemID, Lumberjacking, Throwing, Hiding, DetectHidden, Bushido/Ninjitsu costume, Fishing hat, Magery hat and robe, Carpentry apron | pinned `AddSkillItems` | ServUO `AddSkillItems` | match per race |
| Which characters get `AddShirt/AddPants/AddShoes` | `:706-708` (all but necro, paladin, samurai, ninja) | `:259-264` (profession ≤ 3) | match: the same set |

### 4.2 Differences (for Chase to disposition; none fixed here)

| # | Branch | Pinned | ServUO | Difference |
|---|---|---|---|---|
| **S1** | Gargoyle cloth chest and kilt by sex | `:773-774`, `:796-797` | `:99`, `:140` | pinned gives a female `Type2`; ServUO gives the male-named type to both sexes. This fix follows pinned. Very probably correct as OSI and unverified as such |
| **S2** | `AddBackpack` dagger | `:177` `new Dagger()` for everyone | `:68-71` `GargishDagger` for gargoyles | a gargoyle's starting dagger is a human dagger. Pinned has **no `GargishDagger` type at all**, so matching ServUO needs a port, not a one-liner. Pinned also sets the race after `AddBackpack` (`:231`, then `:235-236`), so a race branch there would see Human |
| **S3** | Swords / Tactics weapon, gargoyle | `:905` `DreadSword` | `:1339`, `:1350` `GlassSword` | different sword |
| **S4** | ArmsLore sword, gargoyle | `:1000` → `DreadSword` | `:970` case, `GlassSword` | same as S3 |
| **S5** | Begging staff, gargoyle | `:1011` `GlassStaff` | `:1020` case, `SerpentStoneStaff` | different staff |
| **S6** | Blacksmith apron | `:1024` `HalfApron` for everyone | `:1031` case, `HalfApron` only for human or elf | a gargoyle smith is given an apron it probably cannot wear, which would go to the backpack. "Cannot wear" is unverified |
| **S7** | SpiritSpeak cloak | `:1277` `Cloak` for everyone | `:1325` case, human or elf only | as S6, with a cloak |
| **S8** | Tracking knife, gargoyle | `:1315` `EquipItem(SkinningKnife)` | `:1377` case, `PackItem(SkinningKnife)` for gargoyles | probably the same in effect: if a gargoyle cannot equip a non-gargish knife, `EquipItem` packs it. Unverified |
| **S9** | Herding, elf | `:1133` `ShepherdsCrook` | `:1155` case, `WildStaff` for elves | elf-only |
| **S10** | Bushido / Ninjitsu, human or elf | `:1032`, `:1233` delete the `OuterLegs` item first | ServUO does not | pinned removes the starting skirt or kilt before the hakama. Not gargoyle-related |
| **S11** | AnimalLore robe hue | `:973` `RandomGreenHue` | `:939` case, `RandomBlueHue` | cosmetic, inside a race branch |
| **S12** | Archery weapon, gargoyle | `:932` `SerpentstoneStaff` | `:959` case, nothing | **unreachable**: `ValidateSkills` zeroes Archery for gargoyles (`:451`), so neither code runs |
| **S13** | Face | none | `:246-257` sets `FaceItemID/FaceHue`, random by race | pinned sets no face at all. That matters only to Enhanced Client faces. It is not a race branch in the strict sense, and I noticed it while reading |

### 4.3 ServUO `:707-714`: the ninja branch

It is **profession 7, Ninja**, in ServUO's `SetSkills` profession switch (`case 7`, `:688`), not an
all-skills path. The gargoyle arm equips a `GargishDagger`, then one random ninja hue applied to
cloth chest, arms, legs and kilt.

Pinned's equivalent is the `"ninja"` case of `GiveProfessionItems`, gargoyle arm `:644-651`:
`DualPointedSpear`, then **leather** chest, arms, kilt and legs, unhued.

**Pinned is not short an item.** Both give four armour pieces including a kilt and legs, so there
is no "second E4 row for a missing item". They differ in three ways: the weapon
(`GargishDagger`, which pinned lacks, against `DualPointedSpear`), the material (cloth against
leather), and the hue (a random ninja hue against none). It is **S14** below if Chase wants it as
a row.

### 4.4 Seen in passing: gargoyle profession outfits (outside the briefed branches)

I read these while resolving 4.3 and did not hunt further. Each is a fidelity call.

| # | Profession | Pinned | ServUO |
|---|---|---|---|
| **S14** | Ninja | `:644-651` `DualPointedSpear` + leather ×4 | `:705-715` `GargishDagger` + cloth ×4, hued |
| **S15** | Warrior | `:685-691` leather chest, arms, kilt, legs | `:548-551` leather chest only |
| **S16** | Paladin | `:571-578` `GlassSword` + **Stone** ×4 | `:638-645` `DreadSword` + **Plate** ×4 (`GargishPlate*` absent from pinned) |
| **S17** | Samurai | `:607-614` `GargishTalwar` + leather ×4 | `:670-677` `GlassSword` + **Plate** ×4 |
| **S18** | Necromancer `BoneHelm` | `:522` for every race | `:569-570` human or elf only |

The necromancer's weapon and leather ×4 otherwise match (pinned `:534-541`, ServUO `:594-601`).

**None of these differences makes a gargoyle unclothed.** D26 was the only case where the result
was visibly wrong. Everything else is a different item, an extra item left in the backpack, or
an unreachable branch.
