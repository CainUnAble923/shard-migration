# Loot box plan (cc-P759, written in cc-P763) — for Chase to approve

Iron Golem, 2026-11-01. Research: `notes\cc-P759-loot-boxes-diversified.md`. Nothing is built yet. Every number below
goes into `Configuration/loot-boxes.json`, so you can retune any of it after it ships without a code change.

**Headline:** every box gets a rarity roll (Common, Rare, Epic, Legendary) on top of today's 6 tiers; 6 new themes
(Fisher, Sailor, Herbalist, Society, Delver, League Dive); Halloween, Winter and Spring add a seasonal slot while their
window is on; the 11 kinds of "does nothing" items go; pools are refilled with working ported items, our registered art,
TheArt's Bags of Holding and Bittiez's Reagent Bag.

## 1. Rarity, kept apart from the tier

Today's 6 tiers stay as they are: the **source** sets the tier (achievement points, boss type, League rank, dungeon,
loop), and the tier sets the slots (2 to 6), the gold and the Renown. What changes is the name. Today the tier ladder
is already called Common, Uncommon, Rare, Epic, Legendary, Celestial (`LootTable.Rarity`), which would clash with the
new rarity words. So:

- **Tier is renamed "grade":** Plain, Sturdy, Fine, Grand, Exalted, Celestial. The resource themes keep their material
  ladder as the grade (Dull Copper to Celestial, Oak to Celestial, Leather to Celestial).
- **Rarity is a separate roll at the moment the box is earned**, and only rarity uses the words Common, Rare, Epic,
  Legendary. The rarity sets the box's colour (grey, blue, purple, orange) and its fanfare.
- **The box's name puts the two together:** "Epic Fine Explorer's Box", "Rare Valorite Miner's Box",
  "Legendary Celestial Loop Box".

**Rarity odds by grade** (percent Common / Rare / Epic / Legendary; `RarityOdds` in the json):

| Grade | 1 Plain | 2 Sturdy | 3 Fine | 4 Grand | 5 Exalted | 6 Celestial |
|---|---|---|---|---|---|---|
| Odds | 85 / 13 / 2 / 0 | 75 / 20 / 4.5 / 0.5 | 65 / 25 / 8 / 2 | 50 / 32 / 14 / 4 | 40 / 35 / 18 / 7 | 25 / 40 / 25 / 10 |

**What each step adds** (`RarityBonus` in the json):

| Rarity | Extra slots | Stack sizes | Pool shift | Guaranteed | Fanfare (P79's levels) |
|---|---|---|---|---|---|
| Common | 0 | x1 | none | nothing extra | Minor (as today) |
| Rare | +1 | x1.5 | +5 to Rare and Cosmetics | nothing extra | Minor, with the "rare" line and a blue flash |
| Epic | +1 | x2 | +10 | one item from the theme's Epic list | Major |
| Legendary | +2 | x3 | +15 | one item from the theme's Legendary list | Capstone (today used only for loops, trials and 200) |

Gold and Renown also scale by the stack multiplier.

## 2. Taking out what does nothing

These are no longer rolled. The classes stay, so old saves still load.

| Today | Where | Replaced with (usable now) |
|---|---|---|
| "[Placeholder] Ore Satchel Upgrade" | Miner slot | a mining tool: Pickaxe or Shovel (Plain to Fine), ProspectorsTool (Grand and up), and our Jacob's Pickaxe as an Epic or Legendary pick |
| "[Placeholder] Grove Ledger Page" | Woodsman slot | a hatchet or axe, and a stack of the tier's boards |
| "[Placeholder] Companion Treat" | Tamer slot | the ported pet treats: TastyTreat, DeliciouslyTastyTreat (Rare+), IrresistiblyTastyTreat (Epic+) |
| "[Placeholder] Trophy of ..." | Boss slot | a real house trophy, from the registered Hestia and Archaaz trophy and head art, named "Trophy of <boss>" |
| "[Placeholder] League Shop Discount Token" | League slot | +50% Renown and a League-hued cloak or sash (cosmetic, account-bound) |
| "[Placeholder] Unique Title" | Rare pool | a League title from the existing title list (LeagueTitles) the account does not have yet |
| "[Placeholder] Unique Hue" | Rare pool | a real dye: MetallicDyeTub (ported), or a stock special or furniture dye tub |
| "[Placeholder] Companion Item" | Rare pool | PetBondingPotion or ElixirOfRebirth (both ported) |
| LoopScrollFragment | Loop slot, Rare pool | the loop's bound sash (kept) and an extra Rare pool pick |
| EpicComponent | Rare pool | dropped; its weight moves to the box-in-a-box and mule schematics, which already work |
| Recipes pool | all | stays, but only recipes for a craft where the opener has 50+ skill (otherwise a plain resource) |

## 3. The pools (general, by grade)

Pool weights by grade stay as today (`PoolWeights`); rarity shifts them (section 1). There is one new pool, **Tools**.
Each sample below is usable on the shard now (a ported class or a stock item, checked in the code).

**Consumables (5 to 10 samples):**
- heal, cure and refresh potions (as today, by the opener's level);
- bandages;
- EnchantedApple (ported);
- the ported foods: Pizza, Stew, FruitBowl, Cheese;
- Sake and Wine (ported drinks);
- ExplodingTarPotion (ported) at Fine and up;
- GoldFoil and SkinTingeingTincture (ported).

**Resources:**
- the tier's ingots, boards, leather and gems (as today);
- cloth and bones;
- fertile dirt and seeds (the plants system works).

**MagicGear:** as today (1 to 4 properties, capped at 60%).

**Tools (new):**
- SkeletonKey (ported);
- a sewing kit, tinker tools, smith hammer, fletcher tools, mortar and pestle, sextant;
- a RunicMalletAndChisel (ported) at Epic;
- trap training kits (ported, the trap system works).

**Recipes:** as today, filtered to the opener (section 2).

**Cosmetics:**
- the ported costumes, belts and FlowerGarland;
- registered art decor as house items: the Odin paintings (10), RedRooster's crystal ball (9), MrRiots's floating
  crystals (19), Ems's flasks and lantern;
- one Noted joke item at 3% of this pool, well under the helpful ones.

**Rare:**
- the box-in-a-box and mule schematics (both work today);
- a League title;
- a real dye;
- a pet item;
- the Bags of Holding and the Reagent Bag (section 6).

## 4. Themes: today's ten, refilled, and six new ones

Each theme keeps its theme slot (what fits the player), then fills the rest from the pools.

| Theme | Theme slot (by grade) | Epic list | Legendary list | How it is earned |
|---|---|---|---|---|
| Miner | ore by Mining skill, gems, a mining tool | ProspectorsTool, 2x ore | Jacob's Pickaxe | Mining achievements (as today) |
| Woodsman | boards by Lumberjacking, a hatchet | a top-tier axe | a runic dovetail saw (Oak) | (as today) |
| Artisan | the craft's resources and its pattern book (as today) | the craft's runic tool, lowest material | the craft's runic tool, one step up | Crafting and Legacy achievements |
| Hunter | hides, a slayer weapon (as today) | a slayer weapon with 2 extra properties | a Bag of Holding | Combat achievements |
| Explorer | a treasure map and a blank map (as today) | a level 4 map | a level 5 map, and a Bag of Holding | Exploration and Discovery; tutorial graduation |
| Tamer | the pet treats, a mount (as today, P365) | PetBondingPotion | ElixirOfRebirth and a mount chance | (as today) |
| Scholar | reagents and scrolls (as today), the **Reagent Bag** | a Reagent Bag (75%) and 2x reagents | a Reagent Bag (90%) | Skills and Collection |
| Boss | a trophy of that boss (registered art), a mount (P365) | a second trophy | a Legendary Bag of Holding | boss kills (as today) |
| Loop | the loop sash (as today) | 2 Rare picks | a Grand Bag of Holding | loops (as today) |
| League | +50% Renown, a League cloak | a League title | a Grand Bag of Holding | League rank (as today) |
| **Fisher** (new) | high seas bait (our patch), a fishing pole, fish steaks | BegFishingPole (ported), a special fishing net | a fishing pole of the tier, and a Bag of Holding | see 4a |
| **Sailor** (new) | a sextant and a spyglass, rope, rations | a message in a bottle (an SOS, which works) | a small boat deed (boats and docks work, P684) | see 4a |
| **Herbalist** (new) | seeds, fertile dirt, the plant potions, a mortar and pestle | SeedBox (ported) | ChickenCoop (ported) and rare seeds | see 4a |
| **Society** (new, one per crafting guild) | that guild's craft resources and tool | the craft's runic tool | the craft's runic tool, one step up, and a Bag of Holding | promotion in the guild (`ClusterFGuildPromotion`): one box per new rank, grade = rank. For the Society of Smiths, Arcane Society, Tailors' Circle, Tinkers' Union, Foresters' Union and Artificers' Order. Maritime and Healers' guild promotions give Fisher/Sailor and Herbalist boxes |
| **Delver** (new, the dungeon dive) | a treasure map and dungeon consumables (heal potions, bandages, a SkeletonKey) | a slayer weapon for that dungeon's creatures | a Bag of Holding | the first kill of each dungeon's boss inside a dungeon region (grade by boss); later, the existing `OnDungeonCleared` hook when clears are tracked |
| **League Dive** (new) | +Renown, consumables | a League title | a Grand Bag of Holding | every 10th League commission (work order) finished, grade by League rank |

### 4a. Fisher, Sailor and Herbalist sources (no achievement category covers them)

- **A per-key theme map**, `AchievementTheme` in the json: an achievement key goes to a theme, ahead of its category.
  The fishing achievements (shoes, bait, high seas fish) go to Fisher, the boat and dock ones to Sailor, and the plant
  and raised-garden ones to Herbalist.
- **First-time events, once per character** (the Award source key records them):
  - Fisher: each kind of high seas fish caught for the first time.
  - Sailor: each SOS chest level recovered for the first time.
  - Herbalist: each plant type first grown to its decorative stage.
- **Guild promotion:** Maritime Brotherhood ranks give Fisher (odd ranks) and Sailor (even ranks); Healers' Covenant
  ranks give Herbalist.

## 5. Seasons

- **The seasons:** Halloween (10-24 to 11-02), Winter (12-01 to 01-06), and a new **Spring** (03-20 to 04-20).
  `ClusterFSeasonalSwitch` holds all three: the same settings and staff commands, and Spring has no decor.
- **While a season is on,** every box earned gets **one extra slot** from that season's pool, and its name gains the
  season ("Halloween Epic Fine Explorer's Box"). Out of season the pool is never rolled.
- **Halloween:**
  - stock treats (Lollipops, WrappedCandy, JellyBeans, Taffy, NougatSwirl);
  - foods (CreepyCake, PumpkinPizza, HarvestWine);
  - painted masks (PaintedDaemonMask, PaintedEvilClownMask, PaintedEvilJesterMask, PaintedPlagueMask, PaintedPorcelainMask), HalloweenPumpkin and PumpkinScarecrow;
  - decor (SkullsOnPike, ColoredSmallWebs, ChairInAGhostCostume, HalloweenGuillotine);
  - our PumpkinCarvingKit;
  - later, the MrRiots Halloween 2024 and 2023 art, once taken in.
- **Winter:**
  - stock SnowGlobes, Snowman, HolidayTree, HolidayBell, Wreath, GiftBox, RockingHorse, Fireflies and HolidayFoods;
  - our WinterAdventCalendar;
  - the registered MrRiots Christmas and winter art (79) and Vrark's Christmas sprites (13), as house decor.
- **Spring:** there is no stock spring art.
  - Until the intake, the spring pool is FlowerGarland, seeds, decorative plants, ValentineChocolate and HeartShapedBox.
  - After the intake, MrRiots spring-easter (45) and spring-plants (40) are added.

## 6. The two community scripts (ported to ModernUO; reference only in `D:\UO\third-party\code\`)

- **Bags of Holding, by TheArt.** Five bags with no weight limit and an item cap. Their names are changed so they do
  not clash with the rarity words:

  | Bag | Cap | Rarity | Odds |
  |---|---|---|---|
  | Lesser Bag of Holding | 12 items | Rare | 4% of the Rare pool |
  | Bag of Holding | 24 | Epic | 6% of the Rare pool, and in the Epic lists above |
  | Greater Bag of Holding | 36 | Epic | 3% of the Rare pool |
  | Legendary Bag of Holding | 48 | Legendary | 4% of the Rare pool |
  | TheArt's "Rare" bag, renamed **Grand Bag of Holding** | 125 | Legendary | Legendary lists only |

  - Contents still weigh what they weigh on the carrier; only the bag's own cap is lifted.
  - Credit TheArt in the CHANGELOG and the notes.
- **Reagent Bag, by Bittiez.** It holds only reagents and cuts their weight.
  - In the Scholar slot and the Rare pool, the weight cut grows with rarity: Common 25%, Rare 50%, Epic 75%,
    Legendary 90%.
  - Odds: 10% of the Scholar theme slot at Common, 25% at Rare, always at Epic and Legendary.
  - Credit Bittiez.

## 7. Guardrails (unchanged)

- Nothing grants skill or stat points (F-12): no skill balls, power scrolls or stat scrolls.
- No bless deeds outside what the design already gives.
- Ethereal mounts stay as P365 set them.
- Helpful items are 95% or more of every pool; the joke items are 3% of Cosmetics only.

## 8. Tests the build will add

- Every theme at every grade and every rarity rolls without an empty slot.
- No rolled item is a placeholder, loop fragment or epic component.
- Seasonal pools roll only in their window.
- The rarity odds and bonuses come from the json.
- Recipes only for the opener's crafts.
- The bags' caps and the Reagent Bag's reagent-only rule and weight cut.
- The Fisher, Sailor, Herbalist, Society, Delver and League Dive sources each award once.
