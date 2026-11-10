# cc-P855: a data-driven decor addon, then the housing furniture batch

## In plain words

- **New house furniture you buy with rewards:** grey stone fireplaces in five sizes, a blue couch, small and country
  kitchens, a barbecue (all in the Achievement store, `[apstore`), a harpsichord (the Bards' guild store) and a holiday
  fireplace (the Festival's winter stock, from December 1).
- **The League shop has a hunt row:** the Hunt Master's buffet table, the Hunt Master's formal dining table and a
  festival feasting table, bought with Renown from the League hunts.
- **Each deed asks which way the piece should face**, then places it in your own house like any house addon. Every
  piece says who designed it (Diesel, Lagatha, manwitch, Olórin, and Gwenivere for the holiday fireplace).
- **New furniture from now on is a data file, not new code:** staff can list, place and clear these pieces with
  `[DecorAddon`. Prices are placeholders in `reward-stores.json` and the League shop table, as before.
  Nothing for you to do, unless you want different prices or a different store for a piece.

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P855`. Main only (no isle branch change). The downloads in `D:\UO\third-party\code\` were read
for their component numbers only: nothing built, run or copied from there.

## What was built

**`server/customizations/Items/Addons/ShardDecor/ShardDecorAddon.cs`** (new):

- `ShardDecorDesigns` reads `Data/ShatteredLegacy/Decoration/Addons/*.cfg` (shipped from `server/data/Decoration/Addons`
  by the Dockerfile's existing `COPY server/data/Decoration/` line; `[Decorate` reads only the facet folders, so these
  files are never decorated into the world). Each file is pinned's own `[Decorate` text (`Static 0x.... (Hue=..;
  Light=..; Name=..)` then `x y z` lines), plus `#!` header lines pinned's reader skips as comments: `name`, `credit`,
  `group`, `facing`. A file with anything else (another type, a bad coordinate, an unknown parameter, no name or
  author, no pieces) is refused and listed; the rest still load.
- `ShardDecorAddon` (a `BaseAddon`): built from one design; each piece is a `ShardDecorComponent` (an
  `AddonComponent` that adds "Design by <author>" to its properties). Pieces keep their own hues (`ShareHue` false).
  Serialized: design, group, author. Redeeding (chopping, pinned `BaseAddon.OnChop`) gives back the group's deed.
- `ShardDecorDeed` (a `BaseAddonDeed`): names a group. With more than one facing it opens a small window, one button
  per facing, then pinned's own placement target (house owner, fit and door checks unchanged). Properties: the author,
  the facings, "House decor". A deed whose design file is gone says so and does nothing.
- Staff: `[DecorAddon` (GameMaster): no argument lists the groups, facings, piece counts and any refused file;
  `reload` rereads the files; `<group>` puts that deed in your pack; `place <design> [x y z]` stands one design with
  no house rules (town dressing); `clear [x y z]` removes the data addons within 6 tiles. `[ShardCommand]` declared.

**Stores** (rows are code, so they appear on an existing world by themselves; an existing `reward-stores.json` that
never heard of them sells them at their defaults, as `RewardStorePrices` already did for a missing row):

| Deed (group) | Where | Price, opens at | Author |
|---|---|---|---|
| `buffet-table` | League shop, hunt row (`hunt.buffet`) | 400 Renown, 500 AP | manwitch |
| `formal-dining-table` | League shop, hunt row (`hunt.formaldining`) | 400 Renown, 500 AP | manwitch |
| `feasting-table` (3 styles) | League shop, hunt row (`hunt.feasting`) | 300 Renown, 250 AP | Olórin |
| `grey-fireplace-small` / `-low` | Achievement store | 100 AP, opens 250 | Diesel |
| `grey-fireplace-medium` | Achievement store | 150 AP, opens 500 | Diesel |
| `grey-fireplace-large` | Achievement store | 200 AP, opens 750 | Diesel |
| `grey-fireplace-grand` | Achievement store | 250 AP, opens 1000 | Diesel |
| `blue-couch` (4 facings) | Achievement store | 100 AP, opens 250 | Diesel |
| `small-kitchen` | Achievement store | 100 AP, opens 250 | Lagatha |
| `barbecue` | Achievement store | 75 AP, opens 100 | Lagatha |
| `country-kitchen` | Achievement store | 150 AP, opens 500 | Lagatha |
| `harpsichord` | Bards' guild store | 800 points, Master rank | Lagatha |
| `holiday-fireplace` | Festival winter stock | 40 tokens | Lagatha, after Gwenivere |

The League rows are `boxable: false` (no loot box draws them). The holiday fireplace, as a winter row, can be drawn by
the winter loot box like every other winter row.

## The data

`notes/cc-P855-tools/convert.py` turns each download's YAAAG component list (the `{id, x, y, z}` table and the
`AddComplexComponent` calls: id, offsets, hue, light, name) into one file per facing. Counted from the output
(`convert-report.txt`, and fact 1 recounts): **30 files, 14 deeds, 649 pieces.**

| Download (author) | Files |
|---|---|
| `grey-fireplaces` (Diesel) | `grey-fireplace-{small,low,medium,large,grand}-{east,south}` (10) |
| `lagatha-holiday-fireplace` (Lagatha; originally Gwenivere, Knights of the Round Table shard) | `holiday-fireplace` |
| `olorin-feasting-tables` (Olórin) | `feasting-table-{1,2,3}` |
| `manwitch-buffet-table` (manwitch) | `buffet-table-{east-west,north-south}` |
| `manwitch-formal-dining` (manwitch) | `formal-dining-table-{east-west,north-south}` |
| `lagatha-pianos` (Lagatha) | `harpsichord-{east,south}` |
| `lagatha-kitchens-bbq` (Lagatha) | `small-kitchen-{northwest,southeast}`, `barbecue-{east,south}` |
| `lagatha-new-kitchen` (Lagatha) | `country-kitchen-{east,south}` |
| `blue-couches` (Diesel) | `blue-couch-{east,north,south,west}` |

- **Stock art only.** `artcheck.py` looks up all 139 distinct IDs in `D:\UO\tool-trials\client-data-copy\artidx.mul`
  with their tiledata names: 139 present, 0 missing (`artcheck.txt`). None lies in our art package's ID ranges.
- **Facings** are the authors' file names where they give one (East, South, E2W, N2S, NW, SE). The two piano files do
  not, so the art names decide: `pianomodern` is all "Harpsichord SOUTH", `pianomodern2` "Harpsichord EAST".
- **Kept as the authors made them:** the lights (YAAAG light 29 = `Circle300` on the fireplace fires, 1 = `Circle225`
  on the feasting tables' braziers, and light 0 = `ArchedWindowEast` on the country kitchen's stove fire, an odd shape
  for a fire but what the file says); the country kitchen's candied apples and Halloween spice pieces (P852 suggested
  swapping them out of season; not done, see below); the barbecue's animated "explosion" flame (0x36BD).

## Tests

`server/tests/Misc/ShardDecorAddonVerification.cs`, six facts, and `LeagueShopVerification`'s starter table gains
the three hunt rows:

1. Every shipped file reads, none refused: 30 designs, the 14 groups and their facings, each author, 649 pieces, no ID
   in our art ranges.
2. The reader takes `[Decorate` text and refuses what an addon cannot be made of (8 bad files).
3. An addon puts each piece at its offset with its hue, light and name, keeps its own hues, shows the author, gives
   its group's deed back, and survives a save.
4. A deed with several facings asks (no target until a choice), places the one chosen, refuses outside a house and
   keeps the deed; a one-facing deed goes straight to the target; a deed with no design says so.
5. Every deed is sold, the three tables in the League hunt row; an older price file sells the new rows at defaults.
6. `[DecorAddon place` stands a design anywhere; `clear` removes only the data addons near the point.

**Red first** (`red-stub.txt`): the facts run against a stub with the same API and no behaviour, no store rows (the
image's own store files): all 6 new facts and the League starter table failed (7 failed, 25 passed). **Green**
(`green.txt`): 31 of 32 in the filtered probe; the one left, `TheStockIsF13sStarterTableAndHandsOverNoMagicItem`,
fails in any filtered run at `BasePigmentsOfTokuno.IsValidItem` (a null `TreasuresOfTokuno.RewardEra`: the Tokuno
config only loads in the full suite; my first probe, which ran the image's own unchanged tests after a compile error of
mine, failed it the same way) and passes in the gated build.

**Gated builds** (the docker\uo build script through `gated-build.ps1`, image `sl-modernuo:cc-p855`, under the
docker-build lock, page cache dropped first; `latest` not moved):

- `gated-build-1.log`: EXIT=0, 3362 shard tests passing, 6 skipped (before fact 6 and `[DecorAddon place/clear`).
- `gated-build.log` (the final code): **EXIT=0, 3363 passing, 0 failed, 6 skipped** (the same 6 skips as main), all
  six ShardDecor facts and `TheStockIsF13sStarterTableAndHandsOverNoMagicItem` passing.

Free memory before the second build read 2.6 GB, 3.0 GB after dropping the Docker page cache; I wrote the walk and
these notes meanwhile and started the build when it read 10.1 GB.

## In game (TazUO, `notes\cc-P855-shots\`)

Private proof shard only (127.0.0.1:2596, a fresh copy of the bot world, image `sl-modernuo:cc-p855`, main's SoS New
Haven), under the test-shard lock. A Player-account trainee, "Iron Decor", in TazUO; staff hands through
`kit\stage855.py`. The shard's start log: `[DecorAddon] 30 designs in 14 deeds from
/modernuo/Data/ShatteredLegacy/Decoration/Addons`, no file refused.

- **Run 1, the pieces** (`p855-<design>.jpg`, 30 shots): staff stood each design on the grass east of the League hall
  (`[DecorAddon place <design> 3677 2570 0`, then `clear` before the next). Every piece draws where its file says:
  e.g. `p855-grey-fireplace-large-south.jpg` (lit fires), `p855-holiday-fireplace.jpg` (stockings, poinsettias, the
  bear rug), `p855-buffet-table-east-west.jpg`, `p855-harpsichord-south.jpg`, `p855-blue-couch-south.jpg` (the
  cushions' and table's own hues). Logs in `run1-logs\`. Its player half stopped on a script bug of mine (TazUO
  title-cases property text, so my lowercase "buffet" match missed a deed that was there; the log shows the deed's
  text), so:
- **Run 2, the player** (`player\`, `walk.txt`: every check PASS): with 1,000 AP and 2,000 Renown granted,
  `[leagueshop`, the hunt row's buffet table confirm (`p855-league-hunt-row-confirm.jpg`), Buy: one deed in the pack
  reading "A Deed For A Hunt Master's Buffet Table | Design By Manwitch | Facings: East-west, North-south | House
  Decor"; double-click: the facing window (`p855-facing-window.jpg`); east-west: the placement cursor; aimed at open
  ground: "You can only place this in a house that you own!" and the deed kept (`p855-refused-outside-house.jpg`).
  `p855-achievement-store.jpg` is the store's first page only; the furniture rows are on later pages and were not
  paged to in the shot (fact 5 covers them).
- Not shown in game: a player placing a deed inside their own house (no house was staged; P809's perch proof did the
  same). That path is pinned's `BaseAddonDeed` target, unchanged.

## Deviations and decisions for Chase

- **"The League hunt row"**: there was no such row, so the three tables are a new run of League shop rows labelled
  "Hunt reward: ...", paid in Renown (what the hunts pay). If you meant a reward inside the hunts themselves (the great
  hunt's payout), that is a small follow-up.
- **Where the rest are sold** was my choice: the house furniture in the Achievement store, the harpsichord at the
  bards, the holiday fireplace in the Festival winter stock. Prices are placeholders like every store's.
- **One deed per piece, facing chosen on use** (a small window), instead of one deed per facing: 14 deeds, not 30.
- **The country kitchen's Halloween spice and candied apples stay** in both facings, as Lagatha made it.
- The house placement itself is pinned's `BaseAddonDeed` target, covered by fact 4's refusal; the in-game run shows
  the refusal on open ground and the pieces placed by staff, as P809's perch proof did. No player house was staged.
- Unattended run: the Read tool was denied once on my own new test file
  (`server\tests\Misc\ShardDecorAddonVerification.cs`, to look at two lines a script edit had split); I read and fixed
  them with `sed` and a one-off Python script instead.
- `D:\UO\third-party\CODE-INTAKE.md` was not touched (P852 already filed these rows).

## Files

- `ShatteredLegacy`: `server/customizations/Items/Addons/ShardDecor/ShardDecorAddon.cs` (new),
  `server/data/Decoration/Addons/*.cfg` (30 new), `LeagueShop/LeagueShop.cs`, `RewardStores/AchievementStore.cs`,
  `RewardStores/GuildStores.cs`, `RewardStores/FestivalStore.cs`, `server/tests/Misc/ShardDecorAddonVerification.cs`
  (new), `server/tests/Misc/LeagueShopVerification.cs`, `CHANGELOG.md` (2026.11.10), `VERSION` (2026.11.10).
- `shard-migration`: this file, `notes/cc-P855-tools/` (convert.py, artcheck.py and their output, the probe and the
  red stub, the build logs, the proof kit), `notes/cc-P855-shots/`.

P855 DONE
