# cc-P261: levelable crafted gear, phase 1 (the item level engine)

Copper, 2026-10-21. Brief: `D:\UO\cc-prompts\claimed\Copper\cc-P261-levelable-gear-build.md`. Research: `notes\cc-P72-level-items-research.md`
(P72). Design and Chase's five rules: `D:\UO\cc-prompts\design\f-levelable-gear.md`. Code repo branch `golem/Copper/P261`,
based on main `90c0402`. Not committed (the Golem commits).

**Pinned source.** `D:\UO\ModernUO-pinned` is not on this PC. I read pinned from the patched build tree in
`sl-uo-builder:cc-P231`, which is this branch's base with every patch applied, copied to the session scratchpad.
File:line citations below are into that tree (`Projects\` relative), so they include the shard's own patch hunks.

## Headlines

1. **Built: the item level engine, staff-only.** Crafted weapons, armour, shields and jewellery can be made levelable
   with a **Smith's Seal** (`SmithsSealDeed`, `[add` only; its source is Chase's). They earn XP from creature deaths, shared
   by damage, with pets, summons, provoked creatures and spells counting as the player's. They level to 200 on
   XmlLevelItems' curve, earn 4 points a level and 8 on every 10th, and spend them in a gump (`[ItemLevel`) on 18
   AosAttribute properties and the 5 resists, each priced per +1 and capped at the property's imbuing ceiling.
2. **No stock item type changed (P72 B.1).** The state is our own `GenericPersistence` save (`Saves/LevelGear`), keyed by
   item serial, and rows for deleted items are pruned at save. The item's own `Attributes` are never written. Bonuses are
   added where the stock values are read:
   - **one new patch** of one hunk (`AOS-level-gear-attribute-aggregation.patch`, in `AosAttributes.GetValue`);
   - the existing `GetItemResistance` virtual for resists (PlayerMobile and BaseCreature overrides);
   - the existing `Item.ExtraProperties` hook for the tooltip.
3. **Companions:** no companion type exists yet. A creature's equipped levelable items earn XP: a pet or companion that
   dealt damage passes its master's share to its own gear. Their bonuses act through the same two readers, and a fact
   shows a horse wearing levelable gear gets its bought resist and DCI.
4. **Tests:** 7 new facts in `server\tests\Misc\LevelGearVerification.cs`, each seen failing first. In the red run, 7
   marked breaks gave exactly these 7 failures, each at its own assertion. Full `docker\uo\build.sh -t
   sl-modernuo:cc-P261`: **1,909 tests, 1,905 passed, 0 failed, 4 skipped; image built.**
5. **Where I followed the brief over P72** (both are Chase-facing; see "For Chase"):
   - XP is **split by damage share** (Chase's decision in the brief), not P72's full award per contributor.
   - The curve and points are **XmlLevelItems' own** (`((n+1)x10)^2-100`, 4/8 points), not P72's proposed `13 x n^1.4`
     and 1 point a level.
   - P72's material budget, item-level/4 creature floor and per-minute award cap are **not built**. The brief did not ask
     for them.

## What was built (ShatteredLegacy)

| File | What |
|---|---|
| `server/customizations/LevelGear/ClusterFLevelGear.cs` (new) | `LevelGearSettings` (every number), `LevelGearAttribute` (the table), `LevelGearState` and `LevelGearStore` (the registry and its save), `ClusterFLevelGear` (eligibility, curve, XP from deaths, spending, read-time bonuses, tooltip, `[ItemLevel` and `[LevelGearSet`) |
| `server/customizations/LevelGear/LevelGearGump.cs` (new) | The spending gump. Every reply re-checks that the player still holds the item, that the button is in range, and the buy rules (P72 A.6 bug 3) |
| `server/customizations/LevelGear/SmithsSealDeed.cs` (new) | The deed: blessed, used up only when it works |
| `server/customizations/LevelGear/LevelGearCreatureResistances.cs` (new) | `BaseCreature.GetItemResistance` override (partial): a creature's levelable gear adds its bought resist |
| `server/customizations/Mobiles/PlayerMobileSetResistances.cs` | The PlayerMobile override adds the bought resist, on a set piece or not |
| `server/patches/AOS-level-gear-attribute-aggregation.patch` (new) | One 4-line hunk in `AosAttributes.GetValue` (`Misc/AOS.cs:655` in the patched tree): `value += ClusterFLevelGear.AttributeBonus(m, obj, attribute);` beside the set-bonus hunk |
| `docker/uo/apply-patches.sh` | Applies it last (made against the tree every patch above leaves), with the usual comment |
| `server/tests/Misc/LevelGearVerification.cs` (new) | 7 facts |
| `CHANGELOG.md`, `VERSION` | New section `2026.10.21.6`, Staff only, because players cannot get a seal yet. VERSION was `2026.10.21.5` |

### 1. The registry

`LevelGearStore : GenericPersistence("LevelGear", 10)` follows the shape of `ImbueCustomStore` (cc-P82): an encoded
version int (0), then rows. Each row holds:
- serial, level, XP (long), unspent points, max level;
- when the item was made levelable and by whom (an audit serial);
- the bought bonuses, as key and value pairs.

The save writes only rows whose `World.FindItem` is live, so a deleted item drops out at the next save. Pinned has no
item-deleted event (P72 B.1). A row is only ever read through a live item, so a stale row does no harm until then. A
version above 0 on load throws, as `ImbueCustomStore` does.

### 2. Making an item levelable

`ClusterFLevelGear.WhyNot` makes these checks:
- **Kind:** `BaseWeapon`, `BaseArmor` (shields are `BaseShield : BaseArmor`) or `BaseJewel`. Clothing is refused, as the
  brief asks ("weapons, armor, shields and jewelry").
- **Not an artifact:** `ArtifactRarity` must be 0 (`BaseWeapon.cs:231`, `BaseArmor.cs:476`, `BaseJewel.cs:128`).
- **Crafted:** `Item.PlayerConstructed` must be true. That is "the shard's crafted flag" P72 B.2 names
  (`Server/Items/Item.cs:798`, set by the craft engine). `BaseWeapon.Crafter` exists only on some bases, so the flag is the
  one test that covers all three kinds. Staff-made, found, bought and reward items never have it.
- **Not already levelable.**

The **Smith's Seal** targets an item the player carries or wears, and is used up only when the item is accepted.
Nothing drops, sells or rewards it, so `[add SmithsSealDeed` is its only source.

### 3. XP

- **The pool** is `BaseInstrument.GetBaseDifficulty(creature) x xpMultiplier`
  (`Items/Skill Items/Musical Instruments/BaseInstrument.cs:249`). P72 A.2 shows XmlLevelItems' `CalcExp` is this
  formula copied: hits, stamina, mana and skills, the 700 knee, +100 per ability, +20 per poison level, then /10. F-14
  recommends the same function for creature levels. Pinned's version reads `HitsMax x 1.6`, adds a paragon bonus, and
  caps at 160 under SE.
- **The split** is paid at `CreatureDeathEvent` (`[OnEvent]`; raised at `BaseCreature.cs:3694` after `base.OnDeath`; the
  damage list is not cleared before it, which fact 4's real kill proves). It walks `DamageEntries` the way pinned's
  `GetLootingRights` (`BaseCreature.cs:3370`) does:
  - each entry's `Responsible` sub-entries credit their player master. Those are filled by `GetDamageMaster` for pets,
    summons (including Blade Spirits and Energy Vortexes, whose `SummonMaster` is the caster) and provoked creatures;
  - any rest of the entry credits the damager if it is a player. Spell damage is registered with the caster as damager;
  - **every damager's damage counts in the total**, so damage dealt by a non-player (another monster, a guard) takes its
    share out of the pool and nobody gets it.
  - Each credited player's share is `round(pool x their damage / total)`.
- **Who gets it:** every levelable item the credited player wears (rule 4), and every levelable item worn by any creature
  of theirs that dealt damage (rules 3 and 5). A backpack item gets nothing.
- **The cap after the split** is per item: `XpForLevel(level + 1) / 20` (XmlLevelItems' `CalcExpCap`, P72 A.2). It bites
  at low levels (15 at level 0) and barely at high ones, as stock.
- **No XP** from a controlled or summoned creature, one whose master is a player, or one flagged `NoKillAwards`.
- **The curve** is the total XP to reach level n, `((n + 1) x 10)^2 - 100`: 0 at level 0, 300 at 1, 4,040,000 at 200
  (P72 A.3: "about 4.0 million XP at level 200"). XP never passes the max level's total.
- **A multi-level award pays every level's points.** XmlLevelItems paid one level's (P72 A.6, bug 4). That is a bug that
  makes something broken, so it is fixed, not copied.

### 4. Points and the gump

- 4 points a level, 8 on every 10th (settings). At level 200 an item has earned **880 points**.
- `[ItemLevel` (Player access) targets an item the player holds and opens `LevelGearGump`. The gump shows level, XP,
  points, properties used of the slot limit, and one row per property this item kind may take: bought, most, cost, and
  a + button that shows only when +1 is buyable.
- `Buy` checks, in this order:
  1. the item is levelable;
  2. the property goes on this item kind (the imbuing row's kinds);
  3. enough points;
  4. **bought + 1 ≤ MaxBuy**, where MaxBuy is the setting's max, if set, capped by what the **ceiling** leaves above the
     item's own value;
  5. **the slot limit:** a property the item does not have yet needs one of the imbuing table's `BaseSlots` (5),
     counting the item's own properties and those a level added.
- The ceiling is the imbuing catalogue's Full value. On an exceptional weapon or armour piece it is x1.5, but never past
  the row's Overcharged maximum (P72 C.3, F-29). Jewellery has no quality.
- Every shard property cap still applies. The bonus is clamped again at read time (`EffectiveBonus`), so an item imbued
  higher after a level bought never passes the ceiling. Wearer totals go through the same `GetValue` the stock caps read
  (HCI 45, DCI 45, LMC and the rest are applied by their readers to the summed value).
- `[LevelGearSet <level> [points]` (GameMaster, DevTool) sets an item's level for testing.

### 5. Applying the bonuses: where they count

P72 B.2 chose read-time aggregation:
- **AosAttribute values:** `AosAttributes.GetValue(Mobile, AosAttribute)` sums every worn item for any mobile. Every
  attribute on the menu is read there. Counted in the patched tree, these are `GetValue` call sites per attribute:

| Attribute | GetValue readers | Direct item reads (not wearer totals) |
|---|---|---|
| WeaponDamage | 18 | 2: `ClusterFExceptionalMaterial.cs:106` (the item's own properties), `WhetstoneOfEnervation.cs:62` (the item's own) |
| AttackChance | 15 | 1: `ClusterFExceptionalMaterial.cs:106` |
| WeaponSpeed | 12 | 1: same |
| BonusMana | 11 | 0 |
| DefendChance, SpellDamage | 8 each | 0 |
| Luck | 6 | 1: same |
| RegenHits | 5 | 1: `ClusterFExceptionalMaterial.cs:107` |
| LowerManaCost | 5 | 0 |
| CastRecovery | 4 | 0 |
| CastSpeed, LowerRegCost | 3 each | 0 |
| RegenStam, RegenMana | 2 each | 0 |
| BonusHits, BonusStam, ReflectPhysical, EnhancePotions | 1 each | 0 |

  The command was `grep -rn "AosAttribute.<X>" | grep GetValue` and `grep -rn "\.Attributes\.<X>\b"` over `UOContent` and
  `Server`, excluding loot, imbuing, reforging, runic and artifact setters. A keyword hit is a candidate. I opened the
  five direct reads above: they read an item's own properties, not a wearer's total, so a level bonus correctly does not
  count there.
- **Resists:** `Mobile.ComputeResistances` adds every item through `GetItemResistance` (our hook,
  `Mobile-set-item-resistance-hook.patch`). The PlayerMobile override (set pieces) and a new BaseCreature override add
  the bought resist. `Buy` calls `UpdateResistances` and `Delta(Hits | Stam | Mana)` on the wearer.
- **Left off the menu, because a bonus would not count where the stock one does:**
  - Str, Dex and Int: stat mods added at equip by `AosAttributes.AddStatBonuses` (`AOS.cs:781`), not read through
    `GetValue`.
  - Spell Channeling and Night Sight: on/off properties read from the item's own `Attributes`.
- **Never on the menu, by P72 C.3 and decision 8:** skill bonuses (they would pass 200 by D-113), Self Repair (F-27), and
  weapon hit effects and leeches (read from `WeaponAttributes` all over `BaseWeapon`).

**The patch, argued (AGENTS.md: alternatives first):**
- **Write the bonus into the item's own `Attributes`.** Rejected. It changes the item's saved values, so the item stops
  being "exactly the crafted item it was" if it leaves the registry. Imbuing and unravelling would then see level
  bonuses as imbued properties. Dormant bonuses after a loop reset (C.4) would also need a rewrite of every item at every
  reset.
- **Customizations alone.** Not possible. `GetValue` is a static method with no event or virtual, and it is called from
  over 100 sites in pinned (counted in the table above).
- **Extend `AOS-set-attribute-aggregation.patch`**, which is what P72 drafted. Rejected in favour of a separate file, so
  each patch keeps one purpose, its own comment in `apply-patches.sh`, and its own reverse step. The hunk sits beside
  the set-bonus hunk all the same.
- **Chosen:** a new one-hunk patch, applied last.

  **Reverses when:** delete `server/customizations/LevelGear/`, the patch, its `apply-patches.sh` line and the
  `+ ClusterFLevelGear.ResistBonus` term in `PlayerMobileSetResistances.cs`. The `Saves/LevelGear` file then orphans
  harmlessly.

### 6. Companions

No companion type exists yet: P41 and P45 are research and probes, and `grep "class \w*Companion"` over
`server/customizations` finds none. So, as the brief allows, this build only makes sure a creature's equipped items are
handled:
- XP goes to a pet's own levelable gear when it dealt damage, with its master's share.
- The bonuses act for any mobile: `GetValue` walks any mobile's items, and the BaseCreature resist override covers
  resists.

Fact 6 shows a horse wearing a levelable shield and ring: its physical resist rises by exactly the bought 3 and its DCI
reads 3. How much a companion's levelable *weapon* matters depends on P41's parity work (creature melee uses
`SetDamage`, not the weapon; P72 decision 6).

### 7. Settings (`Configuration/modernuo.json`, all `clusterf.levelGear.*`)

There are 57 in all: 11 global and 2 for each of the 23 attributes. Each is read when used, through
`ServerConfiguration.GetOrUpdateSetting`, so a missing key is written with its default at start
(`LevelGearSettings.Configure`).

| Setting | Default | What |
|---|---|---|
| `enabled` | true | XP from deaths on or off |
| `maxLevel` | 200 | The max level (Chase's rule 1). An item keeps its own max, which is set from this when it is made levelable; the lower of the two counts |
| `curveBase`, `curveOffset` | 10, 100 | Total XP to level n = `((n+1) x curveBase)^2 - curveOffset` |
| `xpMultiplier` | 1.0 | Pool = Bard difficulty x this |
| `capEnabled`, `capDivisor` | true, 20 | Per item per kill: next level's total XP / capDivisor |
| `pointsPerLevel`, `pointsPerMilestone`, `milestoneEvery` | 4, 8, 10 | Points a level |
| `exceptionalCeilingFactor` | 1.5 | Exceptional ceiling = Full x this, never above Overcharged |
| `attr.<key>.cost` | the table below | Points per +1 |
| `attr.<key>.max` | 0 (= the ceiling) | The most a level may buy of it, below the ceiling |

The slot limit is **not** a level gear setting. It is the imbuing table's own `baseSlots` (`Configuration/imbuing.json`),
so one number governs both systems.

## The attribute table (defaults)

Full and Overcharged come from the imbuing catalogue (`ArtificersImbueGump.cs`, built-in `MaxVanilla` and `MaxGuild`;
`imbuing.json` `overchargedMax` wins). Costs are on XmlLevelItems' scale (P72 A.3: Damage Increase 5, Hit Chance 10, Luck
2, resists 2). I set the rest so a property bought from 0 to its regular ceiling costs about 150 to 450 points, against
880 earned by level 200.

| Key | Property | Goes on | Ceiling (Full) | Exceptional | Cost per +1 | Points to the regular ceiling |
|---|---|---|---|---|---|---|
| damageIncrease | Damage Increase | weapon | 50 | 70 | 5 | 250 |
| swingSpeed | Swing Speed Increase | weapon | 60 | 85 | 5 | 300 |
| hitChance | Hit Chance Increase | weapon | 45 | 65 | 10 | 450 |
| defenseChance | Defense Chance Increase | all | 45 | 65 | 10 | 450 |
| spellDamage | Spell Damage Increase | all | 12 | 18 | 15 | 180 |
| castRecovery | Faster Cast Recovery | all | 3 | 4 | 60 | 180 |
| castSpeed | Faster Casting | all | 1 | 1 | 120 | 120 |
| lowerManaCost | Lower Mana Cost | all | 40 | 55 | 6 | 240 |
| lowerRegCost | Lower Reagent Cost | all | 100 | 100 | 2 | 200 |
| luck | Luck | all | 100 | 150 | 2 | 200 |
| enhancePotions | Enhance Potions | armour, jewel | 25 | 37 | 5 | 125 |
| reflectPhysical | Reflect Physical Damage | armour | 15 | 22 | 10 | 150 |
| hitPointRegen, staminaRegen, manaRegen | HP, Stamina, Mana Regen | armour, jewel | 5 | 7 | 30 | 150 |
| hitPointIncrease | Hit Point Increase | all | 5 | 7 | 30 | 150 |
| staminaIncrease, manaIncrease | Stamina, Mana Increase | all | 8 | 12 | 20 | 160 |
| physicalResist ... energyResist | the five resists | armour, shields | 20 | 30 | 2 | 40 |

"All" means weapon, armour and jewel; clothing cannot be made levelable. The exceptional column is
`min(Full x 1.5, Overcharged)` (jewellery has no quality, so it always uses Full). Fact 5 checked the Damage Increase row
in the test host (Full 50, Overcharged 70). The rest are computed from the catalogue's built-in numbers, not each
asserted.

## Tests

`server/tests/Misc/LevelGearVerification.cs`, 7 facts:
1. `OnlyCraftedWeaponsArmourShieldsAndJewelsCanBeMadeLevelable`:
   - refused: a found Longsword, a crafted `TheDragonSlayer` (an artifact, rarity 11) and a crafted Cloak;
   - accepted once: a crafted Longsword, PlateChest, HeaterShield and GoldRing, each with max level 200;
   - the seal is blessed.
2. `TheCurveIsXmlLevelItemsAndEveryLevelPaysItsPoints`:
   - the curve at 0, 1, 2, 10 and 200 (0, 300, 800, 12,000, 4,040,000);
   - a jump from 8 to 11 pays 4 + 8 + 4;
   - XP stops at level 200's total, with 848 points by then.
3. `OneKillGivesAnItemAtMostTheNextLevelsXpOverTwenty`: 15 at level 0, and 13,515 at level 50.
4. `ThePoolIsSplitByDamageWithAPetsDamageCountingAsItsMasters`:
   - player A 10 damage, A's horse 20, player B 20, pool 1000. A's share 600, B's 400. A's sword and ring and the
     horse's ring get 600, B's sword 400, A's backpack bracelet 0;
   - then a real `Kill()`: the pool is the orc's Bard difficulty, and all of it goes to the sole damager's sword;
   - a pet's death pays nothing.
5. `PointsBuyUpToEachPropertysCeilingAndNoFurther`:
   - Damage Increase: 50 bought at 5 each, the 51st refused;
   - an own value of 30 leaves 20 to buy, and raising the own value to 45 later clamps the bonus to 5;
   - the exceptional ceiling is 70 (Overcharged);
   - refused: a weapon property on a ring, too few points, a resist on a ring, and a new property on a ring that
     already has 5 (raising one it has is allowed);
   - the luck max setting at 3 caps luck at 3.
6. `TheBonusCountsWhereTheStockValueIsReadOnlyWhileWorn`:
   - a sword with own DI 10 and 7 bought: `GetValue` reads 0 while it is in the backpack and 17 once it is worn, and its
     own `Attributes` stays 10;
   - a shield's 4 bought physical raises the wearer's resist by 4;
   - a horse wearing a levelable shield and ring gets +3 resist and DCI 3.
7. `RowsSurviveSaveAndLoadAndADeletedItemsRowIsDropped`: every field round-trips through the store's own
   `Serialize`/`Deserialize`, and a deleted ring's row is gone.

**Seen failing first (AGENTS rule 6).** I put 7 marked breaks (`P261-BREAK 1` to `7`) into `ClusterFLevelGear.cs` and ran
`docker/uo/build.sh -t sl-modernuo:cc-P261 --tests-only`. The result: 1,909 tests, 1,898 passed, **7 failed, exactly the 7
new facts**, each at its own assertion. I then copied the green file back (`cmp` identical, no marker left).

| Fact | Break | Line | Failure |
|---|---|---|---|
| 1 | `WhyNot` skips the PlayerConstructed check | 95 | `Contains("crafted")`: a found sword was accepted |
| 2 | Milestone points ignored | 131 | Expected 8, actual 4 |
| 3 | The per-kill cap off | 165 | Expected 15, actual 9223372036854775807 |
| 4 | `Responsible` ignored (a pet's damage credits nobody) | 213 | Expected 600, actual 200 |
| 5 | The ceiling check skipped | 258 | `Contains("at its most")` |
| 6 | `AttributeBonus` returns 0 (the patch's only call) | 334 | Expected 17, actual 10 |
| 7 | The save writes no bought bonuses | 402 | `KeyNotFoundException: 'damageIncrease'` |

Break 6 stands for the patch line: the patch's one line is `AttributeBonus`'s only caller, so making it return 0 is the
same as removing the hunk.

**Runs:**

| Run | Result |
|---|---|
| 1 | Compile errors (`ItemQuality` is `WeaponQuality`/`ArmorQuality` in pinned; `Server.Collections` and `Server.Gumps` usings missing). Fixed |
| 2 (tests only) | 1,909 tests, 1,903 passed, 2 failed, **all 7 of mine green**. The 2 are known flakes, not mine (below) |
| 3 (red) | As above, 7 failed, exactly mine; the flakes did not fire |
| 4 (full) | **1,909 tests, 1,905 passed, 0 failed, 4 skipped. "Built sl-modernuo:cc-P261 with patches applied and 1905 shard test(s) passing."** The patch step was a cached layer from run 2, the same green tree (run 2's log: `[patches] Applied: AOS-level-gear-attribute-aggregation.patch`) |

**The two flakes in run 2** (bugs, ours to fix, not this prompt's):
- `WispOrbPossessionVerification.APossessedCreatureFightingNeverBecomesItsMastersCombatant(ForestNymph, Naba)`. This is
  the known wisp-orb flake (P135, P142, P177 and P193 notes saw it).
- `CC6Batch1CreatureVerification.TheRestOfTheBatchKeepsItsServUOShape`, line 338, Skree `ControlSlots` expected 3, actual
  2. This is the same bug P225 fixed for the High Plains Boura in CC6Batch2. **Skree is also on `SlotLowerableNames`**
  (`Services/Pet Training/BaseCreature.PetTraining.cs:166`), so its construction roll can lower 3 to 2. The fix is P225's:
  read `SlotsLowered` and expect 2 or 3. I did not change it here.

Neither touches levelable gear. With no row in the store, both new hooks return 0 before doing anything, and every
`LevelGearVerification` fact clears the store.

## Deviations and decisions

- **Ours entirely; OSI has no item levels.** A register line drafted for the overseer (`docs\fidelity-principle.md`, next
  free D-number): "Levelable crafted gear (ours; OSI has none; from ServUO XmlLevelItems' design). Crafted weapons,
  armour, shields and jewellery made levelable by a Smith's Seal earn XP from creature deaths by damage share, and buy
  AosAttribute properties and resists within the imbuing table's ceilings. Reverses when: delete
  `server/customizations/LevelGear/`, `AOS-level-gear-attribute-aggregation.patch` and its `apply-patches.sh` line, and
  the ResistBonus term in `PlayerMobileSetResistances.cs`. Registry rows orphan harmlessly."
- `docs\patch-backlog.md` line drafted: `AOS-level-gear-attribute-aggregation.patch`, 1 hunk, `Misc/AOS.cs` `GetValue`,
  alternatives argued above.
- **The split by damage share** is the brief's (Chase's) decision. P72 decision 4 recommended full credit to every
  contributor over 10 %, and estimated a party of four at about 4x slower with a split (P72 C.5).
- **Fixed, not copied:** the multi-level jump's lost points (A.6 bug 4), the gump's unchecked button and item (bug 3),
  and the deed used up on a refused item (bug 1). The seal is used up only on success.
- **Not built (not asked for in this phase):**
  - P72's anti-farm rules 4 and 6 (the creature floor at item level / 4, and the per-minute award cap);
  - the material budget (C.3);
  - respec;
  - the dormant bonuses of C.4 (no player levels exist; f12);
  - the cap at the owner's max level;
  - spellbooks, talismans and instruments (design note).

  The `m` parameter of `AttributeBonus` is there for C.4's "acting level", unused today.
- **Echo of the Loop** (cc-P82's custom imbue property, `ClusterFImbueEffects.EchoOfTheLoopPercent`, "TODO(F-12,
  XmlLevelItems)") is still not wired into item XP. Its design says "% more XP for a levelable item", but P72 C.4 says
  item XP has no echo. That is Chase's call, so it is left as the hook it was.
- **The name "Smith's Seal"** (the brief's placeholder) sits close to the smiths' **Seals** currency (Smith Seals, P56
  and P57). The type is `SmithsSealDeed` so the two never share a type name, but players may confuse them.

## For Chase

1. **The Smith's Seal's source.** Today it is `[add SmithsSealDeed` only. The options:
   - a Society of Smiths quest. The stock 100-Blacksmithy validation fits it (design note);
   - a Smiths guildmaster or vendor sale, perhaps for Seals, as a sink for P56's raised Seal income (P72 C.1 B);
   - P72's recommendation: a League quest once per character, then a crafter-made consumable per item (P72 C.1 A then C).

   Also, should tailored, tinkered, inscribed and carpentry gear get their own guild's path later? And keep the name
   "Smith's Seal" beside the Seals currency, or rename it?
2. **The attribute table** (above):
   - Are the 23 properties right? Str, Dex and Int and the two on/off properties are left out because they would not
     count everywhere; skill bonuses, Self Repair and hit effects are out by P72 decision 8.
   - Are the costs per +1 right? 880 points at level 200 buys about two to five properties to their ceiling, depending
     on price.
   - Keep the imbuing slot limit shared (5), and the x1.5 exceptional ceiling up to Overcharged?
   - Every cost and max is a setting, so this is tuning, not code.
3. **The reset rule (P72 C.4)**, for when player levels and loops exist. Recommended:
   - **item level is kept through every reset**;
   - **bonuses above the wearer's current level plus Arms Lore attunement go dormant, but the item stays wearable**;
   - **an item cannot level past its owner's max level**;
   - a companion's gear acts at its owner's level plus the owner's attunement.

   The alternative is F-12 read literally: the item's level is the equip requirement, which makes high item levels
   capstone-only. Nothing in this build depends on a player level. The read-time design means dormancy will be one test
   in `EffectiveBonus`, with no item rewrite.
4. **Pacing**, to be set by playtest. With the stock curve (4.04 M XP at 200) and the pool being Bard difficulty (at most
   160 under SE, paragons included), one player soloing the hardest creatures needs at least about 25,000 kills to reach
   200. That is about 210 hours at P72's 120 kills an hour, and far more at ordinary difficulty. A share split makes a
   party slower per person. `xpMultiplier`, `curveBase` and `curveOffset` are the knobs. This is arithmetic from the
   formulas, not measured play.
5. **Echo of the Loop:** should it add to item XP, or stay a player-level-only property (P72 C.4: "item XP has no
   echo")?

## Unverified

- **Not tried in a client.** The gump layout, the tooltip lines (cliloc 1060847 with a tab between the two halves) and the
  `[ItemLevel` targeting are untested in TazUO. The gump's logic (rows, re-checks) is reached only through `Buy`, which
  the facts cover.
- Fact 4's real kill proves the damage list survives to `CreatureDeathEvent` in the test host. A bonded pet's death path
  (`BaseCreature.cs:3565`) also raises the event; it pays nothing because the creature is controlled. I read that and did
  not test it.
- Summons (Blade Spirits, Energy Vortexes) and provoked creatures are credited through the same `Responsible` path as the
  horse in fact 4, by reading `GetDamageMaster` (`BaseCreature.cs:4020`). They are not tested one by one, and neither is
  spell damage (registered with the caster as the damager).
- That `GetValue`'s callers then apply their own caps (HCI 45 and so on) is read from pinned, not tested for each
  attribute.
- `tools/progress.py` was not run. Recent prompts do not run it either, because its README block would conflict between
  Golems working at once.

P261 DONE
