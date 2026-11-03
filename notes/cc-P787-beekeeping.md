# cc-P787: beekeeping

## In plain words

- **Players can keep bees.** A beekeeper (one stands near Vesper) now sells a beehive deed, bee swarms, a hive tool and
  a wax pot. The hive goes in your house (one lockdown, two per house). Keep flowers and water near it, treat it with
  potions as you would a plant, and from its third day it makes honey and raw beeswax every day.
- **Candles from your wax.** A wax pot by a fire or oven turns raw beeswax into beeswax, and Alchemy has a new Candles
  group (candle, short, long and large candle) made from beeswax and thread.
- **Twelve wild hives in Trammel's woods** (near Yew, Britain, Vesper, Minoc, Trinsic and Skara Brae): anyone can pull a
  honeycomb (and get stung a little), and a hive tool can catch a free swarm. They appear by themselves on the next
  start of any world.
- **For you:** nothing to decide. Try it in game when you like: buy the deed and a swarm at the Vesper beekeeper. The
  numbers are in `Configuration/beekeeping.json`.

Iron Golem, 2026-11-03. Code in `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P787`). Plan:
`notes/cc-P787-beekeeping-plan.md`; Chase chose "Build as planned, with wild hives" (answer
`Iron-P787-20261103-074427-ae52`, 08:50). Built as our own code after the apiculture of **Shafev's Cooking Expansion
Set** (`D:\UO\third-party\code\cooking-expansion`, reference only: never built or run, nothing copied). Shafev is
credited in the CHANGELOG line and here.

## What was built

All under `server/customizations/Beekeeping/`:

- `BeekeepingTable.cs`: every number, in `Configuration/beekeeping.json` (written with the defaults on first start,
  refused whole if bad, `[Beekeeping reload` reads it live). The rules check is in its `Validate`: a candle row must make
  a stock light (a `BaseLight`, not a weapon, armour, jewel, cloth or talisman), and a beekeeper row may sell only the
  four beekeeping items or stock honey and beeswax, so no scroll, deed (besides the hive's own), point or property item
  can be put in.
- `HouseBeehive.cs`: the hive (stock art 0x91A, the bees 0x91B over it while a colony lives there). Serialized by the
  generator, version 0 (D40). Placement, the daily check, needs, ailments, potions, harvest and packing up.
- `BeehiveGump.cs`: the plant-gump-like status gump with pour, harvest, add swarm and pack up.
- `BeekeepingItems.cs`: `BeehiveDeed`, `BeeSwarm`, `HiveTool` (50 uses), `RawBeeswax`, `Honeycomb`, `WaxPot`.
- `WildBeehive.cs`: the wild hive and its seeder.
- `BeekeepingSystem.cs`: start-up, the shared sweep, the candle (Alchemy) and wax pot (Tinkering) recipes, the
  `[Beekeeping status|reload|seed [dryrun]` command, and `SBApiarist` (the beekeeper's extra rows).
- `server/patches/Beekeeper-beekeeping.patch` (made with `diff -u` against pinned, checked with `--fuzz=0`) adds
  `SBApiarist` to pinned's `Beekeeper`; one `apply_patch` line in `docker/uo/apply-patches.sh`.

### How it works (the plan, as built)

- **Placement:** a beehive deed, used in your house, targets a spot inside the same house; the hive is locked down
  there (pinned `BaseHouse.LockDown`, so it counts against the house's lockdowns). Only owners and co-owners place and
  tend; friends may look. At most `maxHivesPerHouse` (2). An empty, harvested hive packs back into its deed.
- **Daily check:** each hive saves its next check time; one sweep every `sweepMinutes` (5) runs the hives that are due.
  A day late or three days late is still one day (as plants), and the same sweep twice is no second day. A hive that is
  not locked down in a house keeps its state and lives no days.
- **Needs** within `range` (5) tiles: flowers are plant bowls from the Plant stage to decorative, and stock flower art
  (campion, foxglove, orfluer, poppies, snowdrops, white flowers, the flower pots, and mandrake, nightshade and ginseng
  plants: every id's name read from the client's tiledata, `cc-P787-tools/flower-ids.txt`). Water is troughs, the water
  tub, the water barrel, a filled pitcher of water, and any wet tile (a pond, river or sea) counted as 3. A colony needs
  half a flower and 0.3 water per bee (rounded up); more than six times the water it needs is "too much".
- **Health and bees:** no problem: +10 health and, at 50 or more, one more bee (to 10). Each problem (low flowers, low or
  too much water, parasites, disease) costs 15 health; under 30 health the colony loses a bee; at none the bees leave
  and the hive is empty again, honey and wax kept. A swarm starts at 3 bees and 80 health.
- **Stages:** Colonizing, then Brooding after a day, then Producing after another; a producing colony makes
  `bees x 0.3 x health%` honey and `bees x 0.2 x health%` raw wax a day (rounded), up to 20 and 15. Ten healthy bees: 3
  jars and 2 wax a day, as the plan said.
- **Potions** (poured from the backpack, the bottle given back, as plants): any Poison potion clears parasites, any Cure
  potion clears disease, Heal +15 and Greater Heal +35 health, Strength halves the day's losses and ailment chances for
  24 hours, Agility adds 2 tiles of range for 24 hours. A potion the hive does not need is kept. Parasites (10%) and
  disease (8%) are rolled each day.
- **Products:** the hive tool harvests everything ready (one use), honey as stock jars of honey (so every Cooking recipe
  takes it), wax as raw beeswax. The wax pot, next to a heat source (pinned's craft heat list), renders up to 5 raw
  beeswax a use into stock beeswax, 20% lost as slumgum (5 make 4).
- **Candles on Alchemy** (a new "Candles" group): candle 10-60, short candle 25-75 (1 beeswax, 1 thread each), long
  candle 35-85 (2 beeswax), large candle 45-95 (3 beeswax). They make pinned's own `Candle`, `CandleShort`,
  `CandleLong` and `CandleLarge`. The wax pot is in Tinkering's Miscellaneous (30-80, 6 iron ingots).
- **Beekeeper:** pinned's `Beekeeper` keeps its honey and beeswax and adds the deed (500), swarm (250), hive tool (60)
  and wax pot (150). Pinned reloads a vendor's lists on world load, so standing beekeepers stock them with no respawn.
- **Wild hives:** 12 spots in Trammel (the table lists them by name), each checked on the client map: passable land,
  no static on the tile, not water (`cc-P787-tools/wild-spots.txt`). Three honeycombs a hive, a sting of 2-6 hits that
  never takes the last hit point, regrowth 4 hours after it is emptied, and one swarm per regrowth with a hive tool (50%
  a try, each try a tool use and a sting). A honeycomb opens by hand into a jar of honey and a raw beeswax.
- **On an existing world:** the table file is written on first start; the recipes join at start; the wild hives are
  seeded one tick after every world load (a spot with a wild hive within one tile is left alone, so it is idempotent);
  the vendor rows come with the patch. `[Beekeeping seed dryrun` shows what seeding would do.
- **Herbalism (F-51):** as the plan says, a hive is not a bed, mound or yard item and takes no garden slot. Blooming
  plants count as its flowers, and the bees never touch a plant. Nothing is placed outside houses (that waits for
  F-51's yard tool).

## Tests

`server/tests/Misc/BeekeepingVerification.cs`, 11 facts (listed in its header): the table and its refusals; placement,
the cap and access; a colony's stages and days over saved check times (no double day, a released hive waits);
flowers and water in range (Agility widens it); ailments and each potion; neglect and the bees leaving; harvest, the
tool's uses and the wax pot; the candles in Alchemy and each made from beeswax and thread, the wax pot in Tinkering;
the beekeeper's rows; wild hive seeding (idempotent), combs, the sting, regrowth and one swarm; a hive and a wild
hive surviving a save and load.

The test host has no multi data, so the facts' house is pinned's `SmallOldHouse` with a 7 x 7 floor given to it (as
`LeaseholdVerification` does), on classic lockdown rules: pinned finds a house's AOS lockdown allowance by its exact
type, which a test subclass is not.

**Seen failing first** (probe `cc-P787-tools/probe.sh`: builder image `sl-uo-builder:cc-p786`, this branch's base, with
the change mounted; `Beekeeper.patched.cs` is pinned's file with the patch applied):

- Against the code before the change, the test file does not compile: `Server.Engines.Beekeeping` and
  `BeekeepingTable` are unknown (`red-probe.txt`).
- First green runs (`green-probe1.txt`, overwritten by each attempt): compile fixes (a helper named `Range` clashed with
  a property, `MessageType` is in `Server`, a gump local function cannot use the builder), then a real catch: **the
  Clean Up Britannia reward is already `Server.Items.Beehive`**, so ours became `HouseBeehive`. Then 5 of 11: every
  placement failed at the lockdown, because pinned looks a house's AOS allowance up by its exact type and the facts'
  house is a subclass. Giving that test house classic lockdown rules, 11 of 11 (`green-probe2.txt`).
- One mutant per fact (`mutants.py`, `run-mutants.sh`, results `red-mutants.txt`). Each failed its own fact and no
  other:
  1. the forbidden-kinds and sellable checks off: fact 1;
  2. the per-house cap off: fact 2;
  3. the next check not moved on (a second sweep is a second day): fact 3;
  4. every plant bowl a flower, wilting or not: fact 4;
  5. a Poison potion that does not clear parasites: fact 5;
  6. a colony at no bees not leaving: fact 6;
  7. a harvest that uses no tool use: fact 7;
  8. no candle recipe added: fact 8;
  9. pinned's `Beekeeper.cs` without the patch: fact 9;
  10. the seeder not looking for a hive already there: fact 10;
  11. the honey lost on load: fact 11.
- The patch alone: `PATCHCHECK=1 bash probe.sh x` (`patch-check.txt`): not applied in the image, applies with
  `--fuzz=0`.

**Gated build** (`cc-P787-tools/gated-build.ps1` runs the shard build script with tag `sl-modernuo:cc-p787`, under
the `docker-build` lock, which I took and released):
- **EXIT=0**: 3,038 tests, 3,032 passed, 6 skipped, 0 failed (`green-gated-build.txt`; the raw log is git-ignored).
- All 189 patches applied, including `Beekeeper-beekeeping.patch`.
- The 11 facts pass, and so do `RecipeGatingVerification` and `CraftCategoryPagingVerification`, which walk the craft
  menus the candles and the wax pot join.
- The gate built the final code, which has one change after the mutant runs: a hive picked up into a pack drops its
  bees overlay (`OnAdded`).
- Free memory was 12.3 GB before the probes and 10.1 GB before the gate.

## Deviations and notes for Chase

- **Our hive class is `HouseBeehive`**, not `Beehive`: the Clean Up Britannia reward is already `Server.Items.Beehive`,
  and two types of one name would make `[add Beehive` and type lookups ambiguous. The reward hive is unchanged.
- **No skull candle.** The plan named one, but neither pinned nor our tree has a skull item to make it from. The four
  candles are pinned's stock candles. A skull candle could come with any skull resource later.
- **The wick is a spool of thread** (the plan said cloth or thread): one resource keeps the recipes simple.
- **The heat sources are a copy of pinned's list** (`CraftItem` keeps its own private). They are art ids, not tuning
  numbers, so they are in code, not the table.
- **Fidelity:** beekeeping is not OSI content; it is a shard addition after a community package, as the prompt asks.
  The candles are stock items and honey and beeswax stock resources, so nothing new enters Cooking. Turning
  `enabled` off stops the hives' days and wild seeding (placed items stay).
- **No in-game proof run** on the private shard: it is not in "Done means", and the facts run the real house lockdown,
  vendor and craft code.
- **Version `2026.11.03.9`** (main is at `.8`). If another branch takes `.9` first, the integrator renumbers.

## Files

- ShatteredLegacy:
  - new: `server/customizations/Beekeeping/` (`BeekeepingTable.cs`, `HouseBeehive.cs`, `BeehiveGump.cs`,
    `BeekeepingItems.cs`, `WildBeehive.cs`, `BeekeepingSystem.cs`);
  - new: `server/patches/Beekeeper-beekeeping.patch`; changed: `docker/uo/apply-patches.sh` (one `apply_patch` line);
  - new: `server/tests/Misc/BeekeepingVerification.cs`;
  - `CHANGELOG.md`, `VERSION`.
- shard-migration: this file, the plan `notes/cc-P787-beekeeping-plan.md`, and `notes/cc-P787-tools/` (the art check,
  the flower ids and wild spots checks, the probe, mutant and gate scripts, the patched and pinned `Beekeeper.cs` the
  probe mounts, red and green logs).
- `D:\UO\third-party\CODE-INTAKE.md`: the Cooking Expansion Set row's status now reads "apiculture built (P787)". A
  backup of the file from before the edit is in this session's scratchpad.

P787 DONE
