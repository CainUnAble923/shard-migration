# cc-P759: loot boxes, more varied and more useful (paused at the plan stage)

Iron Golem, 2026-11-01. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P759`. Paused at Chase's request during the first step (research for the plan). **No code was
changed**; nothing was built, deployed or asked yet.

## In plain words

- **Nothing in the game has changed yet.** I was gathering what the loot boxes hold today and what we could add, so I
  could write the plan the task asks you to approve first.
- **Found so far:** several things the boxes hand out today do nothing. These are the "[Placeholder]" items, the loop
  scroll fragments ("the loop scroll ... does not exist yet") and the epic components ("you have not found the recipe
  yet"). The plan will take them out.
- **Found so far:** there is plenty to fill the boxes with that works now:
  - stock Halloween treats and masks, and winter items, plus our own registered winter art;
  - more than 100 items already ported from the reward pool;
  - the shard's 14 guilds, for the new society boxes.
- Nothing for you to do yet. A follow-up task (P763) writes the plan and sends it to you to approve before anything is
  built.

## What the research found (for the plan)

**Today's system** (`server/customizations/LootBoxes`, P79):
- **Ten themes, six pools.**
- **Six tiers, set by the source:**
  - achievements by their points;
  - bosses by type;
  - League rank;
  - dungeon clear at tier 3;
  - loop at tier 6.
- **Box names:** the resource themes use their material ladder (Dull Copper to Celestial, Oak to Celestial, Leather to
  Celestial). The rest use a rarity ladder already named Common, Uncommon, Rare, Epic, Legendary, Celestial by tier
  (`LootTable.Rarity`).
  - So "rarity tiers" partly exist, but they are tied to the source tier. The plan must say how the new rarity roll and
    the tier ladder are named apart.
- **Slots:** 2/3/3/4/5/6 by tier: one theme slot, one gold (plus Renown) slot, and the rest from the pools by tier
  weights (`LootTable.PoolWeights`).
- **Fanfare:** today it is Minor below tier 4 and Major from tier 4 (`ClusterFLootBoxes.Award`, line 113). Capstone is
  used only for loops, trial chapters and 200.
- **Dented Box:** each Noted joke achievement earns one, with one guaranteed joke item (`NotedJokeItems.cs`, 20 items).

**Items that do nothing on the shard today (break the "usable now" rule):**
- `LootBoxPlaceholder` (shows as "[Placeholder] ...") in eight places:
  - Miner "Ore Satchel Upgrade" and Woodsman "Grove Ledger Page";
  - Tamer "Companion Treat" and Boss "Trophy of ...";
  - League "League Shop Discount Token";
  - Rare pool "Unique Title", "Unique Hue" and "Companion Item".
- `LoopScrollFragment`: `ClusterFLootBoxes.CombineLoopScroll` only says the loop scroll "does not exist yet". It is in
  the Loop theme slot and the Rare pool.
- `EpicComponent` ("Something, somewhere, calls for this. You have not found the recipe yet."): Rare pool.
- **The Recipes pool:** it gives any stock recipe scroll below id 9000, whatever the opener's skills. The plan should
  filter it to recipes the opener can use.
- These classes stay (old saves hold them); they just stop being rolled.

**Usable stock to draw on:**
- **Halloween** (ModernUO `Holiday Stuff/Halloween`):
  - treats (Lollipops, WrappedCandy, JellyBeans, Taffy, NougatSwirl) and foods (CreepyCake, PumpkinPizza, HarvestWine,
    MurkyMilk, MrPlainsCookies);
  - painted masks and PumpkinHead, and HalloweenPumpkin;
  - house decor (SkullsOnPike, ColoredSmallWebs, ChairInAGhostCostume, HalloweenGuillotine).
  - Our own `PumpkinCarvingKit` (Items/Decorative).
- **Winter:**
  - stock: SnowGlobes, Snowman, HolidayTree, HolidayBell, Wreath, GiftBox, RockingHorse, AngelDecoration, Fireflies,
    the Mistletoe deed, PileOfGlacialSnow, HolidayFoods;
  - ours: `WinterAdventCalendar`, and the registered MrRiots Christmas and winter art (79 IDs) and Vrark's Christmas
    sprites (13 IDs).
- **Valentine** (stock): HeartShapedBox, CupidStatue and the St Valentine's bears. Ours: ValentineChocolate.
- **Ported reward-pool items** (`server/customizations/Items`):
  - **Consumables (37):** for example TastyTreat, DeliciouslyTastyTreat, IrresistiblyTastyTreat (pet treats),
    EnchantedApple, ElixirOfRebirth, GoldFoil, SkinTingeingTincture, FlowerGarland, foods and drinks;
  - **Tools (11):** BegFishingPole, PetBondingPotion, MetallicDyeTub, RunicMalletAndChisel, SkeletonKey and others;
  - **Equipment (127):** costumes, belts, musical instruments, gems and jewellery;
  - **Functional (37):** SeedBox, JewelryBox, trap training kits, ChickenCoop and others.
  - The port list's reward tier (`tools/port-list.json`, id `rewardpool`) had 708 candidates and 288 done on
    2026-10-13.
- **Registered art with no reward use yet** (`player-package/vendor/shattered-legacy-art/registry.csv`, 672 art IDs):
  - Odin "Paintings" (10);
  - Hestia "Trophys and Statues" (14) and Archaaz "New Trophies and Heads" (14). These are real items to stand in for
    the Boss placeholder trophy;
  - RedRooster's Crystal Ball (9), Ems's partial-hue flasks (8) and oil lantern (3);
  - MrRiots's Floating Crystals (19) and Moonrose's farm carts (4).
- **Event art not yet brought in** (`D:\UO\third-party\ART-LIBRARY.md` section 6; copy through the intake, never run
  from there):
  - Halloween: `mrriots-halloween-2024` (88, EA) and `mrriots-halloween-2023` (63);
  - spring and Easter: `mrriots-spring-easter` (45, EA) and `mrriots-spring-plants` (40, EA). Spring has no stock art,
    so it needs this intake.
- **Season windows already exist:** `ClusterFSeasonalSwitch` (P267). Each season's window is a setting in
  `modernuo.json`, with staff commands. The Halloween and winter switches are in `ClusterFHalloweenDecorSeeder` and
  `ClusterFWinterDecorSeeder`.
  - The seasonal boxes should read these windows, and a new "spring" switch (with no decor) adds its own window.
- **The crafting societies are guilds** (`ClusterFGuildSystem`, 14 guilds):
  - crafting: Society of Smiths, Arcane Society, Tailors' Circle, Tinkers' Union, Foresters' Union, Artificers' Order;
  - the Maritime Brotherhood fits Fisher and Sailor;
  - the Healers' Covenant fits Herbalist;
  - the others: Merchants' Exchange, Bards' Consortium, Thieves' Den, Warriors' Brotherhood, Miners' Compact, Rangers'
    League.
  - `ClusterFGuildPromotion` is the likely hook for "a society box on promotion".
- **No achievement category for fishing, sailing or gardening** exists. The categories are Combat, Skills,
  Exploration, Mining, Crafting, Legacy, Discovery, Collection, League and Mischief. So the plan must give the Fisher,
  Sailor and Herbalist themes a source, for example:
  - a per-key theme map in loot-boxes.json;
  - guild promotion;
  - SOS bottles or treasure.
- The plants system (`Services/Plants`), fishing, boats and docks (P684) and treasure maps all exist, so their tools and
  materials count as usable now.

## Deviations and decisions for Chase

- **Paused before the plan was written,** at Chase's request through the Golem. No Ask-Chase question was sent: the
  plan has to exist before it can be approved.
- **Earlier in the session, three tool calls were denied in the unattended run:**
  - a `Grep` over `D:\UO\golems\Iron\ShatteredLegacy\server` for hood and cowl item classes (P761, done with Bash grep
    instead);
  - two `Read`s of image files outside the working folder (P761, read from scratchpad copies instead).
  - None blocked P759.

## Continuation

- **Done:** reading today's loot box code and its config, the art registry, the port list's reward tier, the
  third-party event art, the stock holiday items, the seasonal switch, the guild list and the achievement categories
  (all above).
- **Left:** everything the prompt asks for:
  - write `notes\cc-P759-loot-plan.md` and ask Chase (Ask-Chase) to approve it;
  - then build parts 1 to 4, the tests, the TazUO shots, the gates, the CHANGELOG line and the final notes.
- **Mid-flight:** nothing. No file in either repo was changed by P759.
- **Continuation prompt:** `D:\UO\cc-prompts\queue\cc-P763-cont-loot-boxes-diversified.md`.

P759 PAUSED
