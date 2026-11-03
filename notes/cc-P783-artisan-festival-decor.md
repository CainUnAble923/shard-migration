# cc-P783: Artisan Festival decor for the spring stock

## In plain words

- **Spring gets 64 new house decorations:** OSI's Artisan Festival pieces for the virtues and the dungeons. There are
  16 paper lanterns, 16 wooden sculptures, 16 throw pillows and 16 tapestries. The lanterns and sculptures light up
  when double-clicked where they stand. Lanterns, pillows and tapestries turn to face the other way when double-clicked
  in the backpack.
- **Where players get them:** while spring is on, the Festival Peddler sells 12 of them for 10 to 25 Festival Tokens
  (four lanterns, four pillows, two tapestries, two sculptures). Every loot box earned in spring may hold one of the
  other 52. Spring's stall goes from 5 things to buy to 17.
- **The pictures are already in our client:** I checked all 160 images the pieces use before building. Nothing in the
  player package changes.
- **For you:** nothing to do. The pieces, the twelve on sale, their prices and how often the rest come in boxes are in
  `Configuration/artisan-festival.json`.

Iron Golem, 2026-11-03. Code in `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P783`), image
`sl-modernuo:cc-p783`. Built as our own code and data. The pieces and their item IDs are from **Sareus's "Artisan
Festival - Reward Items (2016/2017/2018/2019)"** (servuo.dev, `D:\UO\third-party\code\artisan-festival-rewards`,
assessed in cc-P779). No class was copied (Sareus wrote 64), and nothing was built or run from it. Sareus is credited in
the CHANGELOG line and here, and the `CODE-INTAKE.md` row now reads "assess (P779), built (P783)".

## 1. The art check (done first)

The prompt: check art 0x9DE7-0x9E80 in our client and stop if it is missing. **It is present.**

- **Which client:** the player package's client data, `D:\UO\tool-trials\client-data-copy` (7.0.117.0), plus our own
  registered art. Our art registry (`player-package/vendor/shattered-legacy-art/registry.csv`) has no row from 40,421
  to 42,153, so nothing of ours sits on these IDs.
- **The real ID range is wider than the prompt's.** The prompt's range (40,423 to 40,576) covers only the 2016 set.
  Sareus's 64 classes use 160 item IDs from **40,421 to 42,153** (0x9DE5 to 0xA4A9): 4 for each lantern (unlit and lit,
  two facings), 2 for each sculpture (unlit and lit), 2 for each pillow and tapestry (two facings). I checked all 160.
- **The check, by script** (`cc-P783-tools/artcheck.py`, results in `cc-P783-tools/art-check.txt`):
  - every ID has an entry in `artLegacyMUL.uop` with a real image: lanterns 44 x 65, sculptures 66 x 71 to 66 x 78;
  - every ID's tiledata name matches the piece, for example `lamp_virtue_tear`, `Heart_OFF_East` and `Heart_ON_1_South`,
    `sculpture_wood_coin_`, `Ank_OFF_South`. The OFF/ON and East/South names also confirm each lantern's unlit/lit and
    facing pairs.
- **Why P779 thought it might be ship parts:** an item's tiledata and art entry is item ID plus 0x4000. Read without the
  offset, 0x9DE7 lands on a land/ship entry ("BritanianShip MainHu"). With the offset it is `lamp_blood`.
- **Not done:** I meant to look at one rendered image (`D:\UO\tools\vseUOAware\exports\Art\art_0x9DE7.png`, made by the
  art tool) with the Read tool. The unattended run denied it, so I did not retry it another way. The data check above
  stands without it.

## 2. What was built

| Piece | File |
|---|---|
| The table, its file and validation (`artisan-festival.json`): 64 pieces, the stock, the box weight, the light | `server/customizations/ArtisanFestival/ArtisanFestivalTable.cs` |
| Two item types (`ArtisanFestivalLight` on pinned's `BaseLight`, `ArtisanFestivalDecor`), the factory, `[ArtisanFestivalStaff` | `server/customizations/ArtisanFestival/ArtisanFestivalItems.cs` |
| The spring stall's 12 rows, from the table | `server/customizations/RewardStores/FestivalStore.cs` (`Spring()`, `ArtisanLabel`) |
| The spring loot box slot: the other 52 pieces as `@ArtisanDecor` entries | `server/customizations/LootBoxes/LootBoxRoller.cs` (`SeasonItems`, the `@ArtisanDecor` special) |
| `LootBoxRoller.MakeRow` (needed by the tests) | the same file: **P782's identical hunk** (see below) |
| Six facts; the spring-slot fact of `LootBoxDiversityVerification` widened | `server/tests/Misc/ArtisanFestivalVerification.cs`, `server/tests/Misc/LootBoxDiversityVerification.cs` |
| CHANGELOG `2026.11.03.4`, `VERSION` | repo root |

### How it works, and why

- **Data-driven:** one row per piece (key, name, kind, virtue, facings), not one class per piece. A facing is an item ID
  and, for a light, its lit ID. Lanterns have two lit facings, sculptures one, pillows and tapestries two unlit.
- **Two saved types:** each item saves its piece key and its facing; everything else is read from the table.
  `[SerializationGenerator(0)]` on both (D40: new types, nothing older to read, no migration file).
- **Lights:** pinned's `BaseLight` with the lit and unlit IDs from the facing and `Duration` zero, so they never burn
  out (as Sareus set). Double-clicked where it stands, a light lights or goes out (stock behaviour). The light is
  `Circle300` (Sareus's), in the file.
- **Turning:** pinned's interior decorator only turns items whose two IDs are fixed in a `[Flippable]` attribute, and
  these come from data. So, as our `LootDecor` already does, a piece **turns when double-clicked in the pack**. A lit
  lantern turns lit. A sculpture faces one way and says so.
- **Names:** Sareus's, in our style ("a paper tear drop lantern", "an Honesty throw pillow", "a wooden Valor
  sculpture"); the virtue or dungeon shows as a property line ("Artisan Festival: Sacrifice").
- **The stall (8-12 at 10-25 tokens):** 12 pieces, one per virtue where it can be: the Honor, Compassion, Valor and
  Spirituality lanterns (15); the Honesty, Justice, Sacrifice and Humility pillows (10); the Covetous and Hythloth
  tapestries (15); the Deceit and Pride sculptures (25). Row keys `festival.spring.artisan.<key>`, so
  `reward-stores.json` can still override a price the way it can for every row.
- **The box pool ("the rest"):** the 52 pieces not on sale, each `@ArtisanDecor` at `boxWeight` 2. The spring slot's own
  entries (garland, seeds, plants, chocolates, heart box) weigh 100 in all, so about half of spring boxes' seasonal
  items are an Artisan piece.
  - They are added to the slot in code (`LootBoxRoller.SeasonItems`), not to `loot-boxes.json`'s spring list. A world's
    `loot-boxes.json` replaces a season's whole list, and every running world already wrote one, so a list change would
    never reach them.
  - `@ArtisanDecor` is also a special the file can name itself.

## Rules check

| Rule | How it holds |
|---|---|
| No skill or stat points, power scrolls, bless deeds, property artifacts | Plain house decor: no properties, not blessed (fact 6). |
| Rewards usable now and mostly helpful | House decor and light sources, for Festival Tokens players already earn in spring. |
| All numbers in a config file | `Configuration/artisan-festival.json`: the pieces (IDs, names), the stock and its prices, the box weight, the light. A bad file is refused whole (a duplicate key, a wrong lit ID, a stocked piece that does not exist; fact 1). |
| Appears on an existing world by itself, idempotent | The file is written on first start. The stall's rows and the box slot's entries come from it in code, so a world with old `reward-stores.json` and `loot-boxes.json` files gets them too (a row the price file does not list keeps its default). Nothing is placed in the world. |

## Tests

`ArtisanFestivalVerification`, six facts (names in the file header):
1. the table: 64 pieces, 16 of each kind, 160 IDs once each; 12 stocked at 10 to 25; refused files;
2. every row makes its piece; every light lights to its lit ID and goes out to its unlit one;
3. every flip pair turns and turns back in the pack; a lit lantern turns lit; a sculpture does not turn; out of the
   pack nothing turns;
4. the stall sells the stocked pieces at the table's prices, and only in spring;
5. the spring slot holds the other 52 at their weight, each made by the loot boxes' factory; other seasons unchanged;
6. every piece is plain decor.

`LootBoxDiversityVerification.SeasonalPoolsRollOnlyInTheirWindow` checks the spring slot's item came from the slot's
pool. It now also accepts an Artisan piece in spring.

**Seen failing first** (probe: builder image `sl-uo-builder:cc-p781`, this branch's base, with the change mounted;
`cc-P783-tools/probe.sh`):
- Against the code before the change, the test files do not compile: `Server.Engines.ArtisanFestival` and its table
  are unknown (`red-probe.txt`).
- First green runs:
  - a compile error of mine (the factory did not see the item types' namespace; `green-probe1.txt`);
  - then `MakeRow` was missing (`green-probe2.txt`), see below;
  - then **29 of 29**: the six facts, `LootBoxDiversityVerification` and `RewardStoreVerification`
    (`green-probe3.txt`).
- A mutant with one break per fact: **all 6 failed**, each on its own break (`red-mutants.txt`). The breaks:
  1. no duplicate-key check;
  2. a light's lit ID is its unlit one;
  3. turning does not change the art;
  4. the stall charges 10 whatever the table says;
  5. every piece goes in the box slot;
  6. a piece made blessed.

**Gated build** (`cc-P783-tools/gated-build.ps1`, the `docker-build` lock taken and released): **EXIT=0**, 3,006 tests:
3,000 passed, 6 skipped, 0 failed; all 186 patches applied; the six `ArtisanFestivalVerification` facts and all nine
`LootBoxDiversityVerification` facts among the passes. Image `sl-modernuo:cc-p783` (`latest` not touched). Summary in
`cc-P783-tools/green-gated-build.txt` (the raw log is git-ignored). Free memory was 5.5 GB and 9.0 GB before the probe
and the build.

## Deviations and notes for Chase

- **`MakeRow` duplicates P782's hunk on purpose.** The tests make each box entry through `LootBoxRoller.MakeRow`, which
  P782 (grave digging) added and which is not on this branch's base. I applied P782's own diff of that file
  (`git diff 1cba9fc golem/Iron/P782`), so the hunk is byte for byte the same at the same place, and git should merge
  the two branches cleanly. If the integrator sees a conflict there, take either side: they are identical.
- **The art range:** the pieces use 40,421 to 42,153, not just the prompt's 0x9DE7-0x9E80, and all of it is present.
  P779's doubt came from reading the IDs without the 0x4000 art offset.
- **Turning is in the pack, not with the house decorator tool.** The pieces turn by double-click in the pack, as our loot
  box decor does, not with the interior decorator's turn command.
- **No visual look at the art:** the Read tool was denied once on a rendered PNG (unattended run). I did not try another
  way; the art check is by data.
- **Reloads:** the stall's rows are built once per season. After `[ArtisanFestivalStaff reload`, they change at the next
  restart; the box slot follows the reload at once.
- Version `2026.11.03.4`: main has `2026.11.03.3`.
- No in-game proof run: not in "Done means".

## Files

- ShatteredLegacy:
  - new: `server/customizations/ArtisanFestival/` (2 files), `server/tests/Misc/ArtisanFestivalVerification.cs`;
  - changed: `server/customizations/LootBoxes/LootBoxRoller.cs`, `server/customizations/RewardStores/FestivalStore.cs`,
    `server/tests/Misc/LootBoxDiversityVerification.cs`, `CHANGELOG.md`, `VERSION`.
- shard-migration: this file; `notes/cc-P783-tools/` (the art check, its scripts and the parsed pieces, the probe and gate
  scripts, red and green logs).
- `D:\UO\third-party\CODE-INTAKE.md`: the artisan-festival-rewards row's status (CRLF kept; backup in the session
  scratchpad).

P783 DONE
