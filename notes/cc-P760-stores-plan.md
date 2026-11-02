# Reward stores plan (cc-P760) — for Chase to approve

Iron Golem, 2026-11-01. Nothing is built yet.

**Headline:** four kinds of store, all built on the League shop's pattern:
- **Guild stores:** each of the 18 guilds gets a store at its guildmaster, paid in that guild's own points.
- **Festival store:** a Festival Peddler stands in New Haven only while Halloween, winter or spring is on, and sells
  for Festival Tokens.
- **Achievement store:** spends AP without lowering your AP total.
- **The League shop:** grows from 14 rows to 28.

Every price is a placeholder in one table (section 6), kept in a json file so it can be retuned without a code change.

## 0. One pattern for all four

The League shop (`LeagueShop/`, P229) is the model:
- **One price table:** each row has what it is, what opens it, and its price.
- **One gump:** CleanUpBritanniaRewardGump's frame, five rows a page, with the art greyed until the row can be bought.
- **A confirm step,** then a server-side buy that checks everything again. The buy hands over the items (all or none),
  then takes exactly the price.
- **Spending never touches lifetime totals.**
  - Renown: `SpendRenown` takes from the balance, never from `LifetimeRenown`, so League rank never drops.
  - The other three currencies get a separate spent counter, so they work the same way.

I'll lift the shop into one shared `RewardStore` class (rows, check, buy, gump). The League shop keeps its own
behaviour exactly, and its tests stay as they are.

**Guardrails (F-12, F-13), for every store:**
- nothing grants skill or stat points;
- no power scrolls, bless deeds, or artifacts with item properties;
- art only from `registry.csv`;
- everything sold works on the shard today, and most of it helps.

## 1. Guild and society stores

**The currency already exists.** Every guild has a per-character points balance, `CharacterGuildData.GuildCurrency`.
The guild menu already shows it:

| Guild | Its points (name today) | Earned today |
|---|---|---|
| Miners' Compact | Mining Vouchers | work orders, survey reports, satchel routing |
| Society of Smiths | Smithing Seals | smith BODs, commissions, work orders |
| Rangers' League | Trail Marks | work orders |
| Foresters' Union | Timber Tokens | logbook, work orders |
| Artificers' Order | Essence Shards | imbuing, artificer work orders |
| The Custodians | Custodians scrip | work orders |
| Thieves' Den | Thieves' Den scrip | stealing |
| the other 11 | "<guild> scrip" | **only the scrip given on joining** |

**What I add so every guild earns points:**
- **BODs.** The deed-giving guilds other than the Smiths pay gold and stock BOD points today, and no guild points:
  Tailors, Foresters, Tinkers, Maritime, Alembic and Arcane. Their members now also get guild points, 1 per 50 BOD
  points the deed is worth. The deed's tooltip and gump show it, as the Smiths' already do.
- **Requisitions.** These already pay standing to every guild. A member now also gets guild points, 1 per 10 standing.
- **Names.** The 11 guilds with a generic "scrip" name get real ones: Arcane Sigils, Tailors' Thimbles, Tinkers' Cogs,
  Healers' Tokens, Bards' Notes, Warriors' Marks, Maritime Charts, Merchants' Bills, Dojo Seals, Keepers' Candles and
  Alembic Drops.
- Rank-ups and the Smiths' seal catalog, the craft guilds' recipe shop and the mule upgrades are left as they are. The
  new store is one more tab.

**Where:**
- a "Guild Store" section in each guild's menu (`GuildMenuGump`), opened at its guildmaster as the menu is today;
- no new NPCs, so nothing to place and nothing for the render review.

**What each guild's store sells.** Not yet checked against the code: the guild-store items named below that are
not already in the shard's loot boxes or shops. These include the healer's bag, music stand, training dummy, dress
form, disguise kit, commodity deed bundle and vendor's sign. The build checks each class; one that doesn't exist or
does nothing here is swapped for the closest working item, and the swap goes in the notes.

Some rows open only at a guild rank, set per row in the table.

**The stock:**
- every guild:
  - its guild title (a new account title, top rank): "Master of the Forge", "Keeper of the Last Door" and so on;
  - a guild-hued cloak (cosmetic);
- the craft guilds:
  - their craft's tool, in a 50-use bundle;
  - a stack of the next-tier material;
  - the craft's runic tool at the lowest material, at Master rank, where stock has one (hammer, sewing kit, dovetail
    saw, fletcher's tool);
- Miners: a prospector's tool, a shovel bundle, a gem pouch.
- Smiths: their seal catalog stays; the store adds the title, the cloak and a smithing banner.
- Rangers: arrows and bolts in bulk, a fletcher's kit, a hunting horn.
- Foresters: a hatchet bundle, boards of the next tier, a potted tree.
- Artificers: gems for imbuing, and a floating crystal (registered art).
- Healers: bandage bundles, heal and cure potions, a healer's bag.
- Bards: an instrument of their choice (lute, harp, drum), a music stand.
- Warriors: a training dummy (decor), whetstones as weapon repair kits.
- Maritime: bait, a fishing pole, a sextant, a spyglass, rope.
- Merchants: a commodity deed bundle, a vendor's sign, a scale.
- Thieves: lockpicks, a skeleton key, a disguise kit.
- Dojo: a tatami mat, a bonsai.
- Keepers: grave dust, a candle bundle.
- Alembic: empty bottles, a mortar and pestle, partial-hue flasks (registered art).
- Arcane: blank scrolls, reagent bundles, a crystal ball (registered art).
- Tinkers: tinker tools, gears, springs, a clock.
- Tailors: cloth, spined leather, a dress form.
- Custodians: a broom, a trash barrel (decor), cleaning cloths.

## 2. Festival store (event tokens)

**Currency: Festival Tokens.**
- An account balance, not an item, so it can't be lost on death or traded for gold. It is saved with the achievement
  counters, which is already done for the loot boxes' counters.
- The spent count is kept apart from the earned count.

**Earned only while a season is on** (Halloween, winter, or the new spring window), on the shared seasonal switch:
- a creature with 1,000 fame or more drops 1 token to the player with the most damage, at 10% plus 1% per 1,000 fame
  (at most 25%);
- each Treasures of Sorcerer's Dungeon artifact handed in: 2;
- each daily login during a season: 1.

**Where:** a Festival Peddler, a traveling vendor, with a small striped market stall:
- New Haven, just off the bank square, on the walk side of the road and clear of doors, signs and paths;
- a counter, a crate and a signpost north of the path, from the guide's Market list;
- placed when a season starts and taken away when it ends, through the seasonal switch, as the Halloween decor is
  (tracked by serial);
- the exact spot is chosen at build, with an isorender, shots and `placed.md` for the reviewer, per the building guide.

**Stock: only the season that is on.**

| Season | Stock |
|---|---|
| Halloween | stock treats; the five painted masks; HalloweenPumpkin; PumpkinScarecrow; SkullsOnPike; ColoredSmallWebs; ChairInAGhostCostume; HalloweenGuillotine; our PumpkinCarvingKit |
| Winter | SnowGlobes; Snowman; HolidayTreeDeed; WreathDeed; RockingHorse; FirefliesDeed; CandyCane; the registered winter art as house decor (the Father Christmas statue, presents, the gingerbread house, the paintings and so on) |
| Spring | FlowerGarland; seeds; potted plants; ValentineChocolate; HeartShapedBox |

- **Every season:** a "Festival" title per season (three titles), and a seasonal loot box.
- **Halloween art:** the MrRiots Halloween and spring packs are not taken in, so they are not in the stock. If you
  want them, the intake is a separate task.

## 3. Achievement store

**Currency: AP to spend.**
- Achievements already award AP: 1,955 in all today (P229's count).
- The store spends AP earned minus AP already spent. The spent count is a new account counter.
- Your AP total never drops. That total opens League shop rows and AP titles, and it stays.
- Rows open by AP total, as the League shop's do.

**Where:**
- a new button in the achievements window's footer, beside "League Shop";
- the same store from the League Registrar's menu;
- no new NPC.

**Stock:**
- **Titles** (new account titles): "the Completionist" (1,500 AP total), "the Curious" (the Discovery achievements
  done), "the Collector", "the Explorer".
- **Cosmetics:** an achievement sash in five hues; the robe of the Noted (cosmetic, no properties).
- **Decor:** the 12 Odin paintings (registered art), one row each; an "Achievement plaque" with the account's AP total
  engraved.

## 4. The League shop, 14 rows to 28

**Kept as they are:**
- the 14 F-13 rows;
- the Hall decor page (P243);
- the mount rows (P365).

**Fourteen new rows**, all paid in Renown and opened by AP, under the same guardrails:

| Row | Kind | Opens at AP |
|---|---|---|
| Runebook (blessed, League hue) | Convenience | 100 |
| Bag of sending (stock, 30 charges) | Convenience | 250 |
| Hair dye (one use, a special hue) | Cosmetic | 100 |
| Beard dye (one use) | Cosmetic | 100 |
| Metallic dye tub (ported) | Cosmetic | 500 |
| Furniture dye tub (stock) | Cosmetic | 250 |
| Pet bonding potion (ported) | Convenience | 500 |
| Name change deed (stock) | Convenience | 1000 |
| Crystal ball (RedRooster, registered) | Decor | 250 |
| Floating crystal, green (MrRiots, registered) | Decor | 500 |
| Floating crystal, purple (MrRiots, registered) | Decor | 500 |
| Oil lantern (Ems, registered) | Decor | 100 |
| Title: League Champion | Title | 1750 |
| System's Loot Box, Platinum (two draws past Gold) | LootBox | 1750 |

## 5. Tests the build adds

For each currency (Renown, guild points, Festival Tokens, spendable AP):
- earning adds to it;
- buying takes exactly the price and hands over the items;
- a buy it can't afford is refused and takes nothing;
- the balance can't go negative;
- the lifetime total (LifetimeRenown, AP total, tokens earned) never moves.

And:
- every row of every store can be made;
- nothing sold has item properties or grants skill or stat points;
- tokens drop only in season;
- the Festival Peddler is placed and removed with the season.

Plus TazUO shots of each store's window, and the peddler's stall shots and render for the building review.

## 6. The price table (placeholders, `Configuration/reward-stores.json`)

| Store | Row | Price | Opens at |
|---|---|---|---|
| Guild (all) | guild title | 2,000 points | top rank |
| Guild (all) | guild-hued cloak | 300 points | rank 2 |
| Guild (craft) | tool bundle (50 uses) | 50 points | rank 0 |
| Guild (craft) | next-tier material, 50 | 150 points | rank 1 |
| Guild (craft) | runic tool, lowest material | 1,500 points | rank 3 |
| Guild (other) | each consumable bundle | 50 to 150 points | rank 0 to 2 |
| Guild (other) | each decor item | 400 to 800 points | rank 2 to 4 |
| Festival | treats, candy | 2 tokens | |
| Festival | masks, small decor | 10 tokens | |
| Festival | large decor (tree, scarecrow, guillotine) | 25 tokens | |
| Festival | season title | 40 tokens | |
| Festival | seasonal loot box | 15 tokens | |
| Achievement | each painting | 50 AP | 100 AP total |
| Achievement | achievement sash (each hue) | 40 AP | 0 |
| Achievement | robe of the Noted | 150 AP | 500 AP total |
| Achievement | plaque | 75 AP | 250 AP total |
| Achievement | titles | 100 to 300 AP | as named |
| League | runebook, oil lantern, dyes | 75 to 150 Renown | 100 AP |
| League | bag of sending, furniture tub, crystal ball | 200 to 300 Renown | 250 AP |
| League | metallic tub, bonding potion, crystals | 300 to 400 Renown | 500 AP |
| League | name change deed | 600 Renown | 1000 AP |
| League | League Champion title, Platinum box | 800 Renown each | 1750 AP |
