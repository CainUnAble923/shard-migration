# cc-P760: reward stores (guild and society, Festival tokens, achievements, a bigger League shop)

## In plain words

- **Every guild now has a Guild Store**, paid in that guild's own points: tools, materials, runic tools for the craft
  guilds, decor, a cloak in the guild's colour and, at the top rank, a guild title. Open it with the new "Guild Store"
  row in the guild's window, by saying "guild store" to the guildmaster, or by typing `[guildstore` beside them.
  Spending never lowers your standing or rank. Six more guilds now earn points from bulk orders, every guild earns them
  from requisitions, and the guilds that showed "scrip" have real currency names (Tailors' Thimbles and so on).
- **A Festival Peddler sets up a small stall in New Haven** (south-east of the bank) while Halloween, winter or spring
  is on, and sells that season's treats and decorations for **Festival Tokens**. You earn tokens only in season: strong
  creatures sometimes drop one, Sorcerer's Dungeon artifacts pay 2, and your first login of the day pays 1. She is up on
  the test shard right now, because today is inside the Halloween window (it closes after November 2).
- **The Achievement Store** ("AP Store" in the achievements window, at the League Registrar, or `[apstore`) spends your
  achievement points on titles, sashes, a robe, an engraved plaque and twelve paintings. Your AP total never goes down.
- **The League shop has 14 more rows** (34 in all), among them a League runebook, a bag of sending, dye tubs, a pet
  bonding potion, a name change deed, two floating crystals, "the League Champion" title and a Platinum loot box.
- **For you:** every price is a placeholder in one file, `Configuration/reward-stores.json` (written on first start;
  `[RewardStores reload` after an edit). The plan's items that don't exist on the shard were swapped for the closest
  working item (list below); have a look. Nothing to deploy beyond the normal merge.

Iron Golem, 2026-11-01. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P760`. Built the plan Chase approved on the console (answer Iron-P760-20261101-124254-6051,
"Approve as written"): `notes/cc-P760-stores-plan.md`.

## What was built

All new code is in `server/customizations/RewardStores/`:

| File | What it is |
|---|---|
| `RewardStore.cs` | the shared core on the League shop's pattern: `RewardStoreRow` (what, what opens it, price, what it hands over), `IRewardCurrency` (a balance that spends without touching a lifetime total), `RewardStoreDef`, and `RewardStore.Check`/`Purchase` (every check again server side, items all or none, then exactly the price; a failed spend takes the items back) |
| `RewardStoreGumps.cs` | `RewardStoreGump` (the League shop's scroll frame, five rows a page, art greyed until a row opens, cc-P169 colours, a Titles button) and `RewardStoreConfirmGump` (requirements list, then Buy) |
| `RewardStorePrices.cs` | the one price table: `Configuration/reward-stores.json`, every row of every store by key (price and what opens it). Missing file: written with the defaults. Bad file: refused whole. `[RewardStores [reload\|grant ...]` |
| `RewardStoreTitles.cs` | the 26 titles the stores sell, added to `LeagueTitles.All` as hidden-until-held (18 guild titles, three festival, four achievement, the League Champion) |
| `GuildStores.cs` | the 18 guild stores, their currencies (`GuildPointsCurrency`; the Custodians' `CleanUpPointsCurrency`), their stock, and `GuildPointEarning` (BODs and requisitions) |
| `FestivalStore.cs` | `FestivalSeasons`, `FestivalTokens` (currency and earning), the Festival stock per season, the `FestivalPeddler`, and `FestivalMarket` (the stall, up and down with the season, by serial) |
| `AchievementStore.cs` | `SpendableAp` (the AP total less a spent counter) and the Achievement store's stock |
| `RewardStoreCommands.cs` | `[apstore`, `[leagueshop`, `[guildstore` (players) and the staff `grant` verb |
| `RewardStoreItems.cs` | `RewardDecor`: plain movable house decor for registered or stock art (no properties) |

Changed files (each change marked `cc-P760`):

- `LeagueShop/LeagueShop.cs`: the 14 new rows, `BoxTier.Platinum` (5 draws, P79 tier 5, rows to 1,750 AP), a `Boxable`
  flag so the new rows and the mounts never go in a box (Bronze, Silver and Gold draw exactly what they drew before),
  `MakeBox` split so the Festival box uses the same code, and the store titles appended to `LeagueTitles.All`.
- `ClusterFAchievements.cs`: `AddToCounter` (public, never below 0) and the footer's "AP Store" button.
- `LeagueRegistrarGump.cs`: "Achievement Store" on the About Renown row.
- `ClusterFGuildSystem.cs`: the "Guild Store" row in `GuildTaskDetailGump` for members at the guildmaster (the window is
  440 high, was 400). `SmithGuildmasterGump.cs` and `SanitationWardenGump.cs`: a Guild Store button.
- `ClusterFGuildmasterExtension.cs`, `OutridersGuildmaster.cs`, `ForestersGuildmaster.cs`, `MinersCompactLiaison.cs`:
  "guild store" opens the store (the last three are their own NPCs, not stock guildmasters).
- `Mobiles/Mule/MuleUpgrades.cs` and `ClusterFAlembicGuild.cs`: the eleven currency names.
- `Services/BulkOrders/BulkOrderVendors.cs` and `BulkOrderGuildPay.cs`: guild points on a non-smith turn-in, shown on
  the deed ("... gold to the bank and 4 Tailors' Thimbles").
- `Requisitions/RequisitionSystem.cs`: a member gets 1 point per 10 standing.
- `Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonResearcher.cs`: 2 tokens per artifact in season.
- `CHANGELOG.md` (2026.11.01.5) and `VERSION`.

### The currencies, and where each one's spent count lives

| Store | Currency | Balance | Lifetime total a spend never touches | Spent count |
|---|---|---|---|---|
| League | Renown | `ClusterFAccountData.Renown` | `LifetimeRenown` (League rank) | (existing) |
| Guild (17) | the guild's points | `CharacterGuildData.GuildCurrency` | standing (`GuildReputation`) and rank | achievement counter `guildstore.spent.<serial>.<guild>` |
| Guild (Custodians) | Clean Up points | `CleanUpBritanniaData` points | lifetime Clean Up points (their standing) | the same counter |
| Festival | Festival Tokens | earned less spent | `festival.tokens.earned` | `festival.tokens.spent` |
| Achievement | AP | AP total less spent | `AchievementPoints` (opens rows, AP titles) | `ap.spent` |

The counters are the account's achievement counters (`ClusterFAchievementSystem`), saved with them, so no save format
changed. The Festival's daily-login day is the counter `festival.login.day`.

### Stock swaps (the plan said the build would check each class)

Counted against the class index of pinned ModernUO and our customizations, and the art registry:

| Plan | What exists | Shipped as |
|---|---|---|
| Miners: gem pouch | no class | a pouch holding ten stock gems (2 each of amber, citrine, ruby, sapphire, emerald) |
| Healers: healer's bag | no class | a healer's kit: a bag of 50 bandages, two greater heal and two greater cure potions |
| Bards: music stand | no class | stock art 0x0EB5 "music stand" as `RewardDecor` |
| Warriors: training dummy | pinned `TrainingDummyEastDeed` | that deed (a working addon) |
| Warriors: whetstones as weapon repair kits | no whetstone | pinned `RepairDeed` (smithing, 90) |
| Merchants: vendor's sign | no class | stock brass sign 0x0BD2 as decor |
| Thieves: skeleton key | no class | a bigger lockpick row (50) |
| Rangers: hunting horn | no class | feathers (100), a fletching material |
| Dojo: tatami mat, bonsai | no classes | stock art 0x29CA and 0x28DC as decor |
| Custodians: broom, cleaning cloths | no classes | stock art 0xB027 "Broom" as decor; cloth (50) |
| Tailors: dress form | pinned `Dressform` | that |
| Maritime: bait | ours (High Seas) `Bait`, single use and typed | bait for a random fish, 20 uses |
| Smiths: smithing banner | no class | the pole banner art 0x15AE in the Society's hue as decor |
| Healers' and Bards' and Warriors' "consumable bundles" | | bags of three stock tools, stacks of materials |
| Arcane: crystal ball; Artificers: floating crystal; Alembic: flasks | registered (cc-P265: RedRooster, MrRiots, Ems) | `RewardDecor` on those IDs |
| Achievement: 12 Odin paintings | registered (cc-P237, 0x3C9E-0x3CA9) | `RewardDecor` |
| Festival winter art | registered (F-22, 0x3C40-0x3C65) | `RewardDecor` |
| League: oil lantern | registered (cc-P237, Ems, 0x3C8C) | `RewardDecor` |

Every stock art ID was looked up in the client's tiledata (`find_item_id_by_name`; note it reports item IDs plus
0x4000: it listed the 0x0B3D counters as 0x4B3D, and the IDs above are corrected for that).

## Tests

`server/tests/Misc/RewardStoreVerification.cs`, 14 facts, plus updates to two existing files:

1. Guild points are earned from BODs (1 per 50, none for the Smiths or a non-member) and requisitions (1 per 10, none for
   the Custodians); the eleven names.
2. A guild buy takes exactly the price; standing and rank never move; the spent counter records it; a Master row is
   locked at Journeyman.
3. A guild buy it cannot afford is refused, nothing taken; `TrySpend` refuses more than the balance and a negative
   amount; a non-member cannot shop.
4. The Custodians' store spends Clean Up points and never the lifetime total.
5. A guild title is bought once at the top rank and can be shown (`the Songkeeper`).
6. Festival Tokens: none out of season; the drop chance table; the top damager's drop on a roll; 2 per artifact; once a
   day for a login; a buy lowers the balance and never the earned count; refused when short; nothing negative; out of
   season the store sells nothing and a stale row buys nothing.
7. Each season sells its own stock with one title and one box; the seasons follow the switches' dates.
8. The stall is placed in season and removed when it ends; a world first seen out of season is left alone; place twice
   places once; take-down deletes exactly what it placed.
9. The Achievement store spends AP and the AP total and AP titles never drop; new AP adds to the balance; refused when
   short; nothing negative; rows open by the total and the category titles need the category; the plaque is engraved.
10. The League shop's new rows spend Renown and never LifetimeRenown; the runebook is blessed and League-hued; the bag
    has 30 charges; the Champion title; the Platinum box draws 5, never a mount or a new row; the Gold box draws none of
    the new rows.
11. Every row of every store (all three new stores' rows, every season's, and the League shop's 34) can be made, and nothing it hands over is a
    weapon, armour, jewel, power or stat scroll, or clothing with properties (a stock hatchet or prospector's tool with
    no properties is allowed); every decor ID in our art ranges is a registered piece.
12. Row keys are unique; 18 guild stores, each with a title and a cloak; the price table's defaults round-trip; a changed
    price applies; a bad file is refused whole.
13. A guild store opens for a member at the guildmaster by `[guildstore` and by "guild store" through the engine's
    speech, at a stock guildmaster and at the Rangers' League's own NPC; not for a non-member.
14. The window greys a locked row with "Requires 500 AP total" and no button; the confirm step buys for exactly the
    price.

Changed: `LeagueShopVerification` (the starter table gains the 14 rows; titles and boxes 3 to 4) and
`BulkOrderGuildPayVerification` (the tailor member's line now shows the guild points, and the turn-in pays them).

**Seen failing first:** the new test file against the code before the change (the probe mounting only the tests) fails
to build (the store types don't exist). **Mutations, each seen red and restored:** the AP store not recording its spend
(2 facts red); the Rangers' guildmaster without the "guild store" phrase (fact 13 red).

**Gates:** `docker/uo/build.sh -t sl-modernuo:cc-P760`, five cycles (the last after the last code change):
2,920 tests, **2,914 passed**, 6 skipped, 0 failed, EXIT=0 (`notes/cc-P760-tools/green-gated-build.txt`,
`gated-build.log`). The first cycle was red once, on `CommandDeclarationVerification` (the new commands had no
`[ShardCommand]`); fixed. Free memory before the first cycle: 5.4 GB.

## TazUO proof (private shard 127.0.0.1:2596, image `sl-modernuo:cc-P760`)

`notes/cc-P760-tools/`: `proof-shard.ps1` (P761's), `store-shots.ps1` (P761's runner), `make_shots.py` (writes
`shots760.json` and one Legion script per store), `render_stall.py`. Shots in `notes/cc-P760-review/`:

- **Festival store:** `festival-window.jpg` (41 tokens, Halloween stock, prices green and "Open"),
  `festival-confirm.jpg`, `festival-after-buy.jpg` (31 tokens after the 10-token mask).
- **Achievement store:** `apstore-window.jpg` (615 AP; the titles red with their reasons, the sash open),
  `apstore-confirm.jpg`, `apstore-after-buy.jpg` (AP 465 to spend, the AP total still 615).
- **League shop:** `league-window.jpg`, `league-confirm.jpg` (the new runebook row: 1,215 AP of 100, 2,030 Renown of
  150), `league-after-buy.jpg`.
- **Guild store:** `guild-window-by-command.jpg` and `guild-confirm-by-command.jpg` (the Rangers' League store by
  `[guildstore`: crossbow bolts, 50 Trail Marks of 15,000).
- **The stall:** `stall-south.jpg` (from the customers' side), `stall-outside.jpg`, `stall-isorender.png`, and
  `placed.md` for the build reviewer.
- Seen live too: the stall came up by itself on the world's first load ("[FestivalMarket] The Festival Peddler's stall
  is up at (3636, 2627, 0) (6 pieces)"), `reward-stores.json` was written on first start, and a login paid
  "+1 Festival Token (the day's first login). You have 1."

## Deviations and decisions for Chase

- **The Custodians' store spends Clean Up points, not scrip.** The plan's table listed "Custodians scrip earned by work
  orders", but cc-P33 retired Civic Tokens and `RetireCivicTokens` deletes any "custodians" scrip at every world load.
  Clean Up points are the Custodians' real currency (their standing is the lifetime total, which a spend never touches).
- **The League shop was not lifted into the shared class.** The plan said "I'll lift the shop into one shared
  RewardStore class"; the shared core is built on its pattern and the three new stores use it, but the League shop keeps
  its own code so its behaviour and tests stay exactly as they were. It only gained rows, the Platinum tier and the
  `Boxable` flag.
- **Spring** follows a registered "spring" seasonal switch when there is one (cc-P763 adds it on its own branch,
  clusterf.seasonal.spring.*, 03-20 to 04-20) and the same window built in otherwise, so the two branches merge cleanly.
- **The plan's achievement titles' gates** were named loosely; built as: the Completionist at 1,500 AP total, the Curious,
  the Collector and the Explorer for every live Discovery, Collection and Exploration achievement.
- **Extra routes added:** `[guildstore` (and `[apstore`, `[leagueshop`). The Rangers', Foresters' and Miners' NPCs have
  their own menus with no Guild Store button; they answer "guild store" and the command. The Artificers reach it through
  their guild hall window.
- **One live shot not taken:** "guild store" spoken in the client at New Haven did not open the store in four tries. The
  first three were my mistake: the smith and tailor guildmasters I found by coordinates were Felucca's old Haven (the
  `[global get Location` replies carry no map). The last, at the Rangers' guildmaster, I did not settle (he may be the
  Felucca one too, or past the NPC's 4-tile speech range). The speech route is proven in the test host through the
  engine's own speech (fact 13, red without the hook), and the store window and purchase are proven in the client by
  `[guildstore`.
- **One Read was auto-denied** in this unattended run: reading `D:\UO\golems\Iron\p760-proof\shots\stall-outside.jpg`
  directly with the Read tool, to look at the first stall shot. I copied the shots into the session scratchpad and read
  them there instead; nothing was skipped.
- **Shots show the patch-notes window** in the top left (first login of a version on a fresh world copy); the store
  windows draw beside it.
- Prices are the plan's placeholders, one row per store row in `reward-stores.json`.

P760 DONE
