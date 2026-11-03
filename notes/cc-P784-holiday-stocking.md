# cc-P784: holiday stocking at the winter Festival stall

## In plain words

- **A holiday stocking now hangs on the Festival Peddler's table in New Haven** while the winter festival is on. A
  player double-clicks it and holds still for 6 seconds, then pulls out gingerbread cookies, candy canes, jelly beans,
  a cake, or a small winter decoration (a holiday bell, a poinsettia or a snowflake).
- **Once a day per account.** The day's grab also gives 1 Festival Token. Moving during the wait cancels the grab and
  costs nothing. A second character on the same account gets nothing until the next day.
- **It looks after itself.** It goes up with the winter stall and comes down with it, on this world too, with nothing
  for staff to do. It gives no deeds, scrolls or gear.
- **For you:** nothing to do. If you want to change it, every number and the prize list are in
  `Configuration/holiday-stocking.json`. Edit the file, then run `[HolidayStocking reload`.

Iron Golem, 2026-11-03. Code in `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P784`), image
`sl-modernuo:cc-p784` (`latest` not touched). Built as our own code from P779's sketch. The idea is from **Candy
Apple's "Stocking full of goodies"** (`D:\UO\third-party\code\stocking-snowman`, reference only, never built or run).
Nothing was copied: not the prizes, not the 30% roll, not the `CantWalk` freeze. Candy Apple is credited in the
CHANGELOG line and here.

## What it does

- **The item:** `HolidayStocking` is a red stocking (0x2BDC). It cannot be moved, and its tooltip says "Hold still
  beside it for a treat, once a day". It is `[SerializationGenerator(0, false)]` with no saved fields (D40).
- **The grab:** the player double-clicks within `range` (2) tiles. The stocking says "Hold still for 6 seconds". When
  the time is up, the player must still be on the same tile, alive and in range, with the season on and a grab left
  today. Then they get one prize, drawn by weight, in the backpack, with a System line: "You pull … from the holiday
  stocking!". The day's first grab also pays `tokensOnFirstGrab` (1) through `FestivalTokens.Grant`, which prints its
  own "+1 Festival Token" line.
  - Moving cancels the grab ("the stocking slips from your grasp") and does not count.
  - The player is not frozen: holding still is checked, not forced.
  - A double-click during a running wait is refused.
- **The day:** the shard's local day (`FestivalSeasons.Clock`, `FestivalTokens.DayIndex`, as the daily login token
  uses). It is kept per account in two achievement counters, `festival.stocking.day` and `festival.stocking.grabs`.
  These are saved with the existing counters, so there is no new saved type.
- **"One token on the first grab of the day":** with the default of one grab a day, every grab is the first grab. If
  `grabsPerDay` is raised, the later grabs that day give a prize but no token (fact 3 checks both cases).
- **The season gate:** the stocking works only while `FestivalSeasons.Current()` is the table's `season` (winter).
  When the season is wrong or `enabled` is false, it says it is empty.
- **Where it hangs:** on the east half of the peddler's table (anchor +1, +1, +6). The table tile 0x0B7D is 6 high in
  `tool-trials/client-data-copy/tiledata.mul`. It hangs in reach of a player standing in front of the stall.
- **Seeding** (`HolidayStockings.Sync`) runs on every world load, every hour, and whenever the stall goes up or down.
  `FestivalMarket.Up` and `Down` now call it; that two-line hook is the only change to `FestivalStore.cs`.
  - While the winter stall is up, Sync hangs one stocking, tracked by serial in `ClusterFSeasonalState`
    (`festival-stocking`).
  - Otherwise, Sync takes the stocking away.
  - Running Sync twice places once. An existing world that already has the winter stall up gets the stocking on its
    first load.
- **Staff:** `[HolidayStocking status|reload|place|clear]` (GameMaster), with `[ShardCommand]`.

## The table and the rules

`Configuration/holiday-stocking.json` is written with the defaults on first start and refused whole if anything in it
is bad. It uses the GoldPanningTable pattern. The numbers in it: `enabled`, `season`, `holdSeconds` 6, `range` 2,
`grabsPerDay` 1, `tokensOnFirstGrab` 1, `offsetX/Y/Z` 1/1/6, `itemID` 0x2BDC, and the prize rows.

| Prize (pinned type) | Amount | Weight | |
|---|---|---|---|
| GingerBreadCookie | 3 | 20 | treat (food) |
| CandyCane | 3 | 20 | treat (food; blessed) |
| JellyBeans | 10 | 15 | treat |
| Cake | 1 | 15 | food |
| HolidayBell | 1 | 8 | decor |
| RedPoinsettia | 1 | 6 | decor |
| WhitePoinsettia | 1 | 6 | decor |
| BlueSnowflake | 1 | 5 | decor |
| WhiteSnowflake | 1 | 5 | decor |

Treats are 70% of the weight, so most grabs are something a player can eat now. Unstacked treats (cookies, candy
canes) come in a little bag.

**Rules check:** the table refuses (the file fails to load, and the table in force is kept):
- any type with "Deed" in its name;
- any `SpecialScroll`: power, stat cap, alacrity and transcendence scrolls, so no skill or stat points;
- weapons, armour, jewellery, clothing and talismans: anything that could carry item properties or artifacts;
- containers, which could carry any of those.

Bless deeds fall under the deed rule. Nothing in the defaults grants points or properties. P779's source had a holiday
tree deed; it is not here.

## Tests

`server/tests/Misc/HolidayStockingVerification.cs`, four facts:

1. **The prize table:** the defaults validate and round-trip as JSON. Every prize is made, in its amount, and is none
   of the refused kinds. Each of these is refused whole and the table in force is kept: a power scroll, a stat cap
   scroll, a holiday tree deed, a longsword, a gold ring, a bag, and an unknown setting. Each row is drawn by its own
   share of the weight.
2. **The season gate:** nothing and no token in each of these: out of season (forced), in Halloween, in spring, in
   July by the dates, and with the table off. In winter by the dates, a prize and the token.
3. **The daily limit:**
   - moving during the wait, or standing out of range, gives nothing and is not counted;
   - the day's grab gives one prize and one token;
   - later the same day, nothing, from either character on the account;
   - another account still gets its own grab;
   - the next day the stocking is full again, with the token;
   - with `grabsPerDay` 2, the second grab gives a prize and no token, and a third gives nothing.
4. **The seeding:**
   - no stocking without the stall;
   - the winter stall going up hangs it at its spot, unmovable;
   - repeated syncs and a place hang one;
   - one deleted by staff is hung again at the next sync;
   - in Halloween it is taken away;
   - the stall coming down takes it with it.

**Seen failing first** (probe `cc-P784-tools/probe.sh`: builder image `sl-uo-builder:cc-p782`, this branch's base,
with the change mounted):

- Against the code before the change, the test file does not compile: `HolidayStocking`, `HolidayStockings`,
  `HolidayStockingTable` and `StockingPrizeRow` are unknown (`red-probe.txt`).
- The first green run passed 4 of 4 (`green-probe1.txt`).
- I then ran one mutant per fact (`red-mutants.txt`). Each fact failed on its own break:
  1. the refused-kinds check switched off: fact 1 fails;
  2. the season gate opened to any festival season: fact 2 fails, and fact 4 too, since the stocking then stays up at
     Halloween;
  3. the grab no longer counted: fact 3 fails;
  4. Place no longer checks for a stocking already hanging: fact 4 fails.

**Gated build** (`cc-P784-tools/gated-build.ps1` runs `docker/uo/build.sh -t sl-modernuo:cc-p784`, under the
`docker-build` lock, which I took and released):
- **EXIT=0**: 3,011 tests, 3,005 passed, 6 skipped, 0 failed.
- The four `HolidayStockingVerification` facts and the existing `TheFestivalStallIsPlacedInSeasonAndRemovedWhenItEnds`
  are among the passes.
- Summary in `cc-P784-tools/green-gated-build.txt`. The raw log is git-ignored (`*.log`).
- I checked free memory first: 3.7 GB, and 6.6 GB after dropping the Docker VM's page cache.

## Deviations and notes for Chase

- **No in-game proof run** on the private shard: it is not in "Done means", and the facts run the real grab and
  placing code.
- **The stocking's look on the table is not checked by eye.** 0x2BDC is a wall-hanging stocking art. On a table it
  may look like it is lying flat or floating. If it looks wrong, move it with `offsetX/Y/Z` or `itemID` in the file;
  0x2BDB is the other facing.
- **The hold-still wait is not saved.** A grab running at a restart is simply lost, and nothing is counted.
- **Version `2026.11.03.5`.** P783's branch is at `.4`, as main is, so the integrator may need to renumber if P783
  bumps too.
- **The Talking Snowman** from the same package stays an idea only, as P779 recommended.

## Files

- ShatteredLegacy:
  - new: `server/customizations/HolidayStocking/HolidayStocking.cs` and `HolidayStockingTable.cs`;
  - changed: `server/customizations/RewardStores/FestivalStore.cs` (the Up and Down hook);
  - new: `server/tests/Misc/HolidayStockingVerification.cs`;
  - `CHANGELOG.md`, `VERSION`.
- shard-migration: this file; `notes/cc-P784-tools/` (probe and gate scripts, red and green logs).
- `D:\UO\third-party\CODE-INTAKE.md`: the stocking-snowman row's call and status now read "built (P784)". A backup
  of the file from before the edit is in this session's scratchpad.

P784 DONE
