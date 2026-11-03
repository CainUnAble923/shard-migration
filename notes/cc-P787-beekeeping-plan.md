# cc-P787: beekeeping plan (for Chase, before building)

## In plain words

- **The headline:** a beehive you place in your house. You start it with a bee swarm, keep flowers and water near it,
  and treat it with potions when it gets sick. Every day it makes honey and raw wax. You render the wax in a wax pot and
  make candles from it with Alchemy (the Order of the Alembic, herbalism's guild).
- **It sits beside gardening, not against it.** A hive does not use a garden bed or a yard slot. The plants near it
  count as its flowers, and the bees never change how plants grow or breed. Outside houses, hives wait for herbalism's
  yard tool and then share its item budget.
- **Wild hives (my recommendation: yes, a few):** about a dozen in Trammel's woods. Anyone can pull a honeycomb or two
  (and get stung a little), and a beekeeper can catch a swarm there to start a hive for free. Each regrows after a few
  hours.
- **For you:** pick one of the choices in the question: build as planned, build with no wild hives, or something else.

Iron Golem, 2026-11-03. Read before writing this:
- P778's assessment (`notes/cc-P778-assess-gathering-activities.md`) and its rules check;
- Shafev's Cooking Expansion Set apiculture (`D:\UO\third-party\code\cooking-expansion\...\Apiculture`, 36 files,
  2,650 lines with the gumps; reference only);
- the herbalism design (`D:\UO\cc-prompts\design\f-herbalism-reagents.md`, F-51's master) and P519's
  against-the-build table;
- what pinned and ServUO already have.

The prompt's `claude/f-herbalism-reagents.md` is not in this copy. P778 found the same for the `claude/` folder, so I
read the master design file in the prompts repo, which the feature queue names as the master.

## What already exists (read from the trees)

- **Neither ServUO nor pinned has apiculture.** The only bee pieces are:
  - stock **Beeswax** (pinned `Items/Misc/Beeswax.cs`, 0x1422), sold for 1-2 gold by beekeepers, innkeepers and
    provisioners and **used by no craft**;
  - stock **jars of honey** (0x9EC), sold for 3 gold by beekeepers, bakers and cooks, and used by Cooking (sweet
    dough, cookie mix, parrot wafers, a fish pie);
  - our **Clean Up Britannia beehive** reward (`CleanUpRewardAddons.cs:453`), a decor hive that makes honeypots every
    4 hours. It stays as it is: a reward, not a farm.
- **A Beekeeper vendor** (pinned `SBBeekeeper`) stands at one stock Trammel spawner, near Vesper (2954,705).
- **No craft makes candles** in pinned or our tree. Pinned has the candle items (lights).
- **Art:** every piece below uses stock art that is in our client (`cc-P787-tools/art-check.txt`):
  - beehive 0x91A and the bees overlay 0x91B;
  - jar of honey 0x9EC and beeswax 0x1422;
  - "pot of wax" 0x142A (full) and 0x142B (overflowing), kettle 0x9ED, pot 0x9E4, fork 0x9F5 (the hive tool);
  - the candles 0xA28, 0xA26, 0x142F, 0x1430 and 0x1433, and the skull candles 0x1853 and 0x1854.

## 1. The hive

- **A beehive deed** turns into a **beehive** (0x91A, with the bees overlay 0x91B while it is lived in) placed in your
  house. It counts as one lockdown, and the owner and co-owners tend it. At most `maxHivesPerHouse` (2) per house.
  - It is one saved item, like the Clean Up hive, not a multi-tile addon, so it fits anywhere.
  - Serialization by the generator (D40), versioned from 0.
- **Getting bees:** a new hive is empty. You start it with a **bee swarm**:
  - bought from a Beekeeper vendor (the stock vendor's list gains the deed, the swarm, the hive tool and the wax pot);
  - or caught at a wild hive with a hive tool (if wild hives are on).
- **Outside houses:** not in this task. F-51's yard tool (not built yet) is where garden items go outside a house. When
  it lands, a hive becomes one more yard item counted in the yard's budget. Nothing in this task places anything
  outside a house.

## 2. Care, like the plant system

The model is the package's, rebuilt our way, and close to the OSI plant system players already know:

- **A daily check** (`checkHours`, 23, the plants' pace) moves the colony along. A hive's next check is saved, and one
  shared sweep runs every few minutes (F-51's Q12 rule), so a restart neither skips nor doubles a day.
- **Stages:** empty, then colonizing, brooding, and producing (honey and wax from about the third day).
- **Population** grows by one a day (to 10) while the colony is healthy and fed, and falls when it is not.
- **Needs**, read at each check within `range` (5) tiles of the hive:
  - **Flowers:** living plants count: plant bowls, raised-bed mounds, and flowers and garden decor on the ground. More
    bees need more flowers.
  - **Water:** water containers (troughs, tubs, barrels, pitchers of water) and water tiles.
  - Each shows on the hive's gump as too low, fine or too much, as the plant gump does.
- **Ailments:** now and then **parasites** (cured by a Poison potion poured on the hive) or **disease** (a Cure potion).
  - A Greater Heal potion mends health.
  - A Strength potion makes the colony hardier for a day; an Agility potion makes the bees range a little further for a
    day.
  - This is the package's potion list, and the same potions the plant system uses.
- **Neglect never kills at once.** Low flowers, water, or an untreated ailment lowers health, then population. At zero
  population the bees leave and the hive is empty again, kept for a new swarm.
- **A gump** like the plant gump shows the stage, health, population, flowers, water, ailments, and honey and wax
  ready.

## 3. Products

- **Honey and raw beeswax** build up in a producing hive each day (more with more bees and better health, up to
  `maxHoney` and `maxWax`). You harvest them with a **hive tool** (a fork, 0x9F5, with uses):
  - honey comes out as stock **jars of honey**, so every Cooking recipe that uses honey takes it as it is;
  - wax comes out as **raw beeswax** (0x1422, hued darker).
- **The wax pot** (0x142A, sold by the Beekeeper and made by Tinkering) renders raw beeswax into stock **Beeswax** at a
  heat source, a few at a time, with a little slumgum waste.
- **Candle-making on Alchemy**, the Order of the Alembic's craft and herbalism's guild. New recipes in an
  Alchemy "Candles" group make stock candles from Beeswax and a wick (cut from cloth or thread):
  - candle, long candle, short candle, the candelabra pieces stock art allows, and a skull candle (with a skull);
  - they are stock light items: usable now, decor and light.
- **No food buffs** (no stat food, no XmlSpawner), and no skill or stat points, scrolls, deeds beyond the hive's own,
  or property items.

## 4. How it fits herbalism (F-51), so the two do not fight over garden space

- **No shared slot.** A hive is not a bed, a mound or a yard item. In houses it is one lockdown.
- **Gardens help hives.** Plants within range count as the hive's flowers, so a gardener's house makes the best
  beekeeping. Nothing is taken from the garden.
- **Hives do not touch plants.** The bees never pollinate, water, speed or slow a plant. The OSI plant loop and
  herbalism's breeding stay exactly as designed (fidelity, and F-51's "breeding and mutation stay with the player").
- **Later, with the yard tool:** hives become yard items and count in the same per-house budget as beds and kit, so
  the budget, not the bees, decides how a yard is split. F-51's garden kit could one day list a hive as a Soil or
  Shelter helper. That is F-51's call, not this task's.
- **Guild tie:** candles on Alchemy give the Alembic a small side craft, and beeswax becomes useful for the first time.

## 5. Wild hives: yes or no

**Recommendation: yes, a few.**

- About 12 wild hives (0x91A, not movable) are seeded at woodland spots in Trammel: near Yew, Vesper's beekeeper,
  Britain's woods and Skara. The seeding is idempotent on every world load: a missing hive is re-placed, and two are
  never placed at one spot.
- Anyone may double-click one for a **honeycomb** (honey and raw wax together, opened at a kettle or by hand), 1 to 3
  per hive, with a small sting (a few hits, never lethal).
- Once emptied, it falls and regrows after `wildRegrowHours` (4).
- A beekeeper with a hive tool may instead **catch a swarm** there, a free start for a home hive (one per wild hive per
  regrowth).
- **Why yes:** it gives non-beekeepers a reason to stop in the woods, a free way in, and a first step toward F-51's
  wild foraging.
- **Why no:** less to build and test. Then swarms come only from the Beekeeper vendor.

## 6. Numbers (all in `Configuration/beekeeping.json`)

The numbers in the file:
- check hours;
- range;
- the flower and water need per population;
- the ailment chances;
- the potion effects;
- the population step;
- honey and wax per day per population, and the caps;
- the hive tool's uses;
- the wax pot's batch size and waste;
- the vendor prices;
- the candle recipes' skills and amounts;
- max hives per house;
- the wild spots, the combs per wild hive, the sting damage, the regrow hours and the swarm chance.

The file is written with defaults on first start and refused whole if bad. Staff use `[Beekeeping status|reload|seed`.

**Starting values** (to tune in playtest):
- a producing hive of 10 healthy bees makes about 3 jars of honey and 2 raw wax a day;
- a hive tool has 50 uses;
- a swarm costs 250 gold, the deed 500, and the wax pot 150.

## 7. Size and tests

- **Size:** about 1,500 lines of ours: the hive with its gump and care, the swarm, the tool, the wax pot, the
  honeycomb, the wild hives and their seeding, the candle recipes, the vendor rows and the table. Plus the facts.
  Probably one large Golem task. If it runs long I would split off the wild hives as a second one.
- **Facts:**
  - the table and its rules;
  - placement: house only, the per-house cap, owner access;
  - a colony's stages and population over saved check times, with no double day after a reload;
  - flowers from plants and water in range;
  - ailments and each potion;
  - neglect, ending with the bees leaving and the hive kept;
  - harvest amounts and the tool's uses;
  - the wax pot;
  - each candle recipe;
  - the vendor rows;
  - wild hive seeding is idempotent, with combs, regrowth and swarms;
  - the hive's save round-trip.
