# cc-P34: F-22, winter holiday decorations for New Haven (dated event decor, two layers)

Builder: Claude. The autopilot handed this prompt over at 2026-10-12 16:30:08 (after P83). Before starting, both repos
were clean, and P31, P32, P33 and P37 to P39 were all committed. Pinned is `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88`, the commit after the bump (`git rev-parse HEAD`). **Every pinned
citation below is at that commit.** The prompt and F-22 cite paths only, no line numbers; every path they name exists
there unchanged (`Items/Special/Holiday/`, `Items/Special/Holiday/Christmas/HolidayTree.cs`,
`Items/Deeds/HolidayTreeDeed.cs`, `Holiday Stuff/Christmas/2004/`, `2010/`). No clash found.

## Status: finished on 2026-10-12

Built and tested. **Not deployed, and nothing has run against any world.** The image is `sl-modernuo:cc-p34`;
`sl-modernuo:latest` is untouched. The player package was built to scratch only (all gates passed) and **not
published**. Chase's steps are at the end.

## Headlines

- **One event seeder places 61 items around New Haven:** 22 OSI holiday art, 39 community art.
  - It puts them up on **December 1** and takes them down after **January 6**, by itself, on the shard's Chicago
    clock.
  - Staff commands: `[ClusterFWinterDecor status`, `up` and `down`, each with `dryrun`. `up` works before December 1,
    for the test shard, and says so.
- **Take-down removes exactly what it placed.** Every piece is a `WinterDecor`, a type only this seeder creates, and
  each knows its row key. Down deletes those and nothing else: not a player's item, not another seeder's, not pinned's
  own holiday items. Up skips a row already placed. Proven by tests.
- **47 new art IDs, 0x3C40-0x3C6E (15424-15470),** from MrRiots' and Vrark's packs, registered, converted and
  shipped through P26's pipeline.
  - Four pieces animate: Father Christmas, the raised firepit, and two stoves.
  - The statue, firepit, stoves, tree, fireplace and sleigh block and have height, on the client and the server alike.
  - The only change to the pixels: BMP became PNG, and pure black became transparent.
- **The placement is a table of 61 rows,** each checked against the server's own map files. The table, with a
  reason per row, is below.
  - Each row has a surface at its height and nothing impassable in the way.
  - Outdoors, no row sits on a road.
  - No row sits on a door, a door swing, an NPC post, a spawner tile, the board, the arrival tile, the Reset Stone, or
    the field office's components.
  - Wall art is only on the faces the client shows.
- **Two things to know.**
  - The **Warriors' "Guild Hall" is an open training yard**, so it got nothing; the Healer's Hall stands in for "guild
    halls".
  - **Vrark's holiday paintings sit centred on their tile** rather than against the wall the way OSI's do. Walk them
    and say if they float (Deviations).

## Part A: facts (read only)

### A1. Pinned's holiday items: decoration or reward

Placeable world decorations are things that look right standing in a town, belong to no player, and have no
behaviour that matters. Pinned's classes, judged that way:

| Class (pinned file) | Art | Verdict |
|---|---|---|
| `Snowman` (`Items/Special/Holiday/Snowman.cs:5`, `:88`) | 0x2328 / 0x2329 | **decoration**. Blessed and dyeable, with a title. Used by art ID |
| `WreathAddon` (`Wreath.cs:18`, facing `:254`/`:258`) | 0x232C north wall, 0x232D west wall | **decoration**. Its deed is a reward (`:164`) |
| `MistletoeAddon` (`Holiday Stuff/Christmas/2004/Mistletoe.cs:18`, facing `:266`/`:270`) | 0x2374 north wall, 0x2375 west wall | **decoration**. Its deed is a reward |
| `HolidayBell` (`HolidayBell.cs:29`, double-click `:44-52`) | 0x1C12 | **decoration** by art. The class rings on double-click and is a blessed reward |
| `GreenStocking` / `RedStocking` (`Stockings.cs:6`, `:20`) | 0x2BD9/0x2BDA, 0x2BDB/0x2BDC | **decoration** by art. The classes are containers |
| `SnowPileDeco` (`SnowPiles.cs:8`, hue `:16`) | 0x8E2, 0x8E0, 0x8E6, 0x8E5, 0x8E3, hue 0x481 | **decoration** |
| `SnowyTree` (`2004/SnowyTree.cs:9`) | 0x2377 | **decoration**. A blessed reward in the 2004 gift |
| Icicles (`Icecicles.cs:9-55`) | 0x4572-0x4577 | decoration. Not used: no icicle spot passed the wall checks |
| `IcyPatch` (`IcyPatch.cs:22-46`) | 0x122A / 0x122F | **not decoration**: `OnMoveOver` makes a player slip. Not used |
| `SnowPile`, `PileOfGlacialSnow` (`2004/SnowPile.cs:19`) | 0x913 | **reward**: double-click throws snow. Not used |
| `HolidayTree` (`Christmas/HolidayTree.cs:23-110`) | 0xCD7 / 0x1B7E plus 23-28 ornaments | an addon a player's deed places in a house (`Placer = from`). Not used; Vrark's static tree takes the square |
| `HolidayTreeDeed` (`Items/Deeds/HolidayTreeDeed.cs:36`) | | **reward, and dated**: refuses outside December (`Core.Now.Month != 12`) |
| `Poinsettias`, `Snowflakes`, `SnowGlobes`, `GiftBox`, `HolidayGiftBoxes`, `HolidayTimepiece`, `WristWatch`, `GingerBreadHouseDeed`, `HolidayPottedPlant`/`PottedPlantDeed`, `SnowStatue*` and `SnowStatueDeed`, `WinterGiftPackage2003`, `PKHolidayStuff` (coal, bad card, spam) | | **rewards** (blessed, or deeds a player places in a house, or gags) |
| `DecorativeTopiary`, `FestiveCactus`, `LightOfTheWinterSolstice` (`2004/*.cs`) | 0x2378, 0x2376, 0x236E | rewards in the 2004 gift. Not used |
| 2010: `FirefliesDeed`, `AngelDecoration` (0x46FA), `RockingHorse` (0x4214) | | rewards. Not used |

**Only `HolidayTreeDeed` sets itself to a date** (`:36`). Nothing else checks the season.

**Why the seeder places OSI art by art ID in its own `WinterDecor`, not pinned's classes:** those classes carry
behaviour a town decoration must not have. Bells ring, stockings are containers, a snow pile throws snowballs, an icy
patch trips people. They would also make take-down depend on telling our snowman from a player's. The art is
identical.

### A2. `WinterGiftGiver` and the 2004 and 2010 sets

- There is no class called `WinterGiftGiver`. There is **`WinterGiftGiver2004`**
  (`Holiday Stuff/Christmas/2004/Winter2004.cs:6`).
  - Its `Initialize` registers it with `GiftGiving` (`:11-14`), so **it is registered in our build**.
  - Its window is **fixed at 2004-12-24 to 2005-01-01** (`:8-9`), and `GiftGiving.OnLogin` gives only inside the
    window (`Special Systems/Engines/GiftGiving.cs:38-41`). So **it never fires: inactive today and every year.**
- What it would do if its dates were moved:
  - At login, to an account at least 30 days old (`:43-46`, `MinimumAge` `:62`) that has not logged in since the start
    (`:48-51`), it gives a gift box.
  - The box holds a mistletoe deed, a pile of glacial snow, a Light of the Winter Solstice, and one of: a topiary
    (60%), a festive cactus (24%) or a snowy tree (16%) (`Winter2004.cs:18-37`).
  - It goes in the backpack, or the bank if the backpack is full or overloaded (`GiftGiving.cs:73-82`).
- Not enabled. A gift event is its own feature if Chase wants it.
- In passing: `GiftGiving.OnLogin` sets `acct.LastLogin` on every login, givers or not (`:56`). That is harmless.
- **The 2010 set** (`2010/Addons/FireFliesDeed.cs`, `Items/AngelDecoration.cs`, `Items/RockingHorse.cs`) has **no
  giver and no dates**. These are reward items.

### A3. The community art

**TazUO (the shipped build, commit `3212623f`, read at that commit):**
- It reads `.bmp` art overrides (`ExternalImageLoader.cs:102-104`, `:271`), but only 24- or 32-bit (`:213-216`).
- **It keys no colour.** A 24-bit pixel gets alpha 255 (`:250`), and `FixPNGAlpha` only premultiplies (`:369-378`). So
  a BMP's black would draw as solid black.
- So every BMP becomes a PNG with pure black (0,0,0) made transparent. All 328 BMPs in the two packs are 24-bit.
- `scripts\anchor-art-frames.py` gained `--files`, `--black-transparent` and `--keep-geometry`. Nothing else in the
  tool changed.

**Keep geometry:** both authors drew their art already laid out on the canvas the way UO's art file holds it.
- The content sits off-centre, with bottom margins chosen for the tile: the firepit has 22 rows below, the snow
  paintings 59, Vrark's paintings and garlands about 20.
- So nothing is cut or padded. Converting format and making black transparent is all that was done.
- The tool re-reads each PNG and checks it pixel for pixel against its source.

The art chosen (file, ID, frames, facing):

| IDs | What | Source file(s) | Size | Frames | Facing |
|---|---|---|---|---|---|
| 15424-15428 | Father Christmas statue | MrRiots `Statues\Father Christmas\1..5.bmp` | 44x155 | 5 | one of two (the `n.bmp` set; `n-n.bmp` is the other) |
| 15429-15433 | raised firepit | MrRiots `Raised Firepit\1..5.bmp` | 72x114 | 5 | one |
| 15434-15437 | iron stove | MrRiots `Stoves\1\1..4.bmp` | 50x80 | 4 | one of two |
| 15438-15441 | stone stove | MrRiots `Stoves\2\1..4.bmp` | 54x84 | 4 | one of two |
| 15442 | Christmas tree | Vrark `Christmas tree_1.bmp` | 89x163 | 1 | one of four |
| 15443 | Santa's bag | Vrark `SS Santa's Bag_1.bmp` | 43x92 | 1 | |
| 15444-15446 | presents | Vrark `Gift Box 01_1`, `Gift Box 02_1`, `Present.003_Kharzug_1` | about 30x55 | 1 | |
| 15447, 15448 | candy cane arch | MrRiots `Candy Cane stuff\SmallCaner.bmp`, `SmallCaner2.bmp` | 54x133 | 1 | two facings |
| 15449-15455 | eggnog trays (2), cookie pan, candy cane tray, platter, turkey, gingerbread house | MrRiots `Food Items\EggNogTray`, `Eggnogtray1`, `ChristmasCookiesPan1`, `CandyCaneOnTray`, `ChristmasPlatter`, `turkey`, `1` | 44x44 | 1 | |
| 15456 | Christmas fireplace | Vrark `M3DCF Christmas Fireplace_1.bmp` | 93x141 | 1 | front turned west: back to an east wall |
| 15457, 15458 | garland | Vrark `Garland.003_1`, `_4` | 87x129, 99x124 | 1 | 15457 north wall, 15458 west wall |
| 15459-15462 | holiday paintings | Vrark `Painting 12_1`, `12_4`, `15_1`, `15_4` | about 45x120 | 1 | `_1` north wall, `_4` west wall |
| 15463-15466 | snow-covered painting (2), shield (2) | MrRiots `Snow Covered Shields and Paintings\1`, `2`, `S1`, `s2` | 44x133 | 1 | 1 and S1 west wall; 2 and s2 north wall |
| 15467-15469 | snow patches | MrRiots `Snow Patches\Snowpatches\1\2`, `3`, `4` | 44x44 | 1 | |
| 15470 | Christmas sleigh | Vrark `Christmas Sleigh_1.bmp` | 130x139 | 1 | |

**How each wall piece's facing was decided:**
- OSI's own wall art was measured in New Haven's statics. The painting 0x0EC9 at 3484,2573 has content in the left
  half and its wall to the west; 0x0EA0 at 3474,2500 has content in the right half and its wall to the north. The
  item stands on the floor tile in front of the wall.
- For Vrark's full-width pieces, the slope of the art's top edge decides: down to the right means a north wall, down
  to the left a west wall.
- **That caught my own first labels of the two garlands, which had them the other way round.** The registry has the
  corrected text.

**Not used:**
- Vrark's two animated trees: his page says they come from other games.
- The rest of both packs (toys, gnomes, other trees, more presents, the second facings): kept to what the placement
  uses.

### A4. Slots

`python scripts\find-free-art.py --placeholder --run 47`: 7 runs, the longest 0x3C3D-0x3D11 (213 IDs). I took
**0x3C40-0x3C6E**, 8-aligned, straight after the fox ears (0x3C3C).
- The animations' frames sit right after their base IDs.
- These are placeholder slots, so a client without the update shows "UNUSED", as P26 wanted for proving the updater.
- `--check-registry` afterwards: **0 of 94 registered IDs are no longer free.**

## Part B: the art

- **`registry.csv`:** 47 rows (id, hex, what, source with file, license **"none stated; see SOURCE.txt"**, kind art),
  written by `notes\cc-P34-tools\registry_rows.py` before the PNGs were used.
- **PNGs:** `vendor\shattered-legacy-art\art\15424.png` to `15470.png`, written by `convert_art.py`.
- **`records.json`: 7 tiledata records and 4 animdata records,** written by hand. Names are 19 characters or fewer.

  | Record | Flags | Height | Taken from |
  |---|---|---|---|
  | father christmas | 0x01004040 | 20 | OSI's statue 0x1224 is 0x4000 with height 0; Animation and Impassable added so it blocks |
  | raised firepit | 0x01806240 | 0 | OSI's animated fire pit 0x29FD |
  | iron stove, stone stove | 0x0180A050 | 20 | OSI's animated oven 0x462 (35 there) |
  | christmas tree | 0x00004041 | 20 | OSI's tree 0xCCA |
  | christmas fireplace | 0x00006050 | 20 | OSI's fireplace 0x45D |
  | christmas sleigh | 0x00004040 | 10 | ours |

  - Weight is 255 on all seven.
  - **Animdata:** frames 0..n-1, interval 2, as OSI's fire 0x19AB and campfire 0xDE3 (about 200 ms a frame). The
    packs give no timing of their own.
  - **Comparables read from the client's tiledata, 2026-10-12.** My first animdata read was one byte off: the 68-byte
    entry is 64 frame offsets, an unknown byte, then count, interval and start. Corrected before use.
- **Walk-through pieces** (presents, bag, food, paintings, garlands, arches, snow patches) need no records (P26
  section 13).
- **Server:** `ShatteredLegacyArt.Apply` now also calls `ClusterFWinterDecorArt.Apply()`, which writes the 7 records
  into `TileData.ItemTable`, as the runestone's are. The values are a C# table (`ClusterFWinterDecorArt.Records`) that
  the package fact compares with records.json.
- **`SOURCE.txt`:** a winter section with both authors, URLs, "LICENSE NONE STATED", the frames in order, what was
  done to the pixels, and where each record value comes from.

## Part C: the event seeder (`server\customizations\ClusterFWinterDecorSeeder.cs`)

- **Clock:** `Core.Now` (UTC, `Server/Main.cs:657`) in the server's time zone, America/Chicago. Both compose files
  set it (`docker/uo/docker-compose.yml:29`, `docker-compose.test.yml:48`). It is Chicago because December 1 means
  Chase's and the players' December 1; UTC's would start six hours early.
  - **Season:** `IsInSeason`: the whole of December, plus January 1-6.
- **Automatic:** on world load, and every hour after, `Sync` compares the season with the state it last brought the
  world to. That state is saved in `ClusterFWinterDecorState`, a versioned `GenericPersistence`. Sync acts **only
  when the season has changed**: up when December 1 comes, down once January 7 begins.
  - So a staff `up` in November (for the test shard), or a `down` in December, stands until the season next changes.
  - A world first seen in season is brought up. A world first seen out of season is left alone.
  - It checks hourly rather than daily, so the change lands within an hour of midnight. Nothing is done unless the
    season changed.
- **Switch:** `clusterf.winterDecor.enabled` (default true, written to modernuo.json on first start). False keeps the
  automatic check off; the commands still work.
- **Marker:** `WinterDecor : Item` (SerializationGenerator version 0, one saved field `Key`).
  - It is not constructible, so `[add` cannot make one. It is not movable and does not decay.
  - Name and hue come from the row (snow piles hue 0x481, as pinned's `SnowPileDeco` sets).
- **Commands:** `[ClusterFWinterDecor status|up|down [dryrun]`, Administrator, `[ShardCommand]` WorldSetup /
  Skips / TestFirst / dryrun.
  - `up` outside the dates says "Outside the dates ... putting it up anyway, for testing".
  - Idempotent: up places only missing keys, down removes only `WinterDecor`.
- **Placement as data:** `ClusterFWinterDecorLayout.cs`, **generated** by `notes\cc-P34-tools\gen_layout.py` from
  `placement.json`. The generator refuses to write while `validate.py` fails.
  - Each row: key, area, x, y, z, item ID, name, hue, facing, layer. All rows are on Trammel.
  - The file also carries the 64 spawner tiles the test checks against.

## Part D: the placement

**Tools** (`notes\cc-P34-tools\`, README there):
- `tiles.py`, `floormap.py`, `pick.py`: ports of pinned's `Map.GetAverageZ` and `GetTopSurfaceZ`, plus a CanFit-style
  blocked check over the server's map files.
- `protected.py`: 262 protected tiles.
  - doors: 74 door tiles, plus 74 swing tiles from pinned `BaseDoor.GetOffset`
    (`Items/Construction/Doors/BaseDoor.cs:13-28`, `:240`)
  - 44 NPC posts
  - 72 spawner entries, on 64 distinct tiles (the 64 the generated file carries)
  - the board, the arrival tile and the Reset Stone
  - 28 field office components
- `validate.py`: the row checks.

**What "walkway" means here:** the ground is dirt, cobblestone or flagstone, or a static named
road/path/planks/boards/floor sits at the row's z.
- **The square is all road, and so is the pier**, so rows there are allowed on a walkway. They stay clear of the board
  corner, the plaza's lamp posts, the statue's steps and the ruined wall.
- **Indoor rows** sit on floor boards and are checked for blocking only.
- **Outdoor snow and arches are never on a road:** they are picked by the tool as the nearest free off-road tile.

**Wall art** stands on the floor tile in front of a north wall (art facing south) or a west wall (art facing east),
because those are the faces the client shows. **Outside**, the visible faces are a building's south and east walls,
so the two outside pieces (the inn's mistletoe and the office's wreath) hang on east walls. They sit at the wall's own
height, 27 and 18, above lower ground.

Previews, drawn from the map files with our PNGs: `notes\cc-P34-tools\preview-square.png` (the square with the decor),
`square.png`, `docks.png`, `town.png`.

**The table** (`validate.py`, all 61 rows ok):

| key | area | x,y,z | item | layer | mode | why |
|---|---|---|---|---|---|---|
| sq-tree | square | 3512,2577,14 | 0x3C52 a christmas tree | community | square | east edge of the plaza, clear of the lamp posts and the ruined wall at 3511-3512,2580 |
| sq-bag | square | 3511,2578,14 | 0x3C53 Santa's bag | community | square | at the tree |
| sq-gift1 | square | 3513,2578,14 | 0x3C54 a present | community | square | at the tree |
| sq-gift2 | square | 3511,2576,14 | 0x3C55 a present | community | square | at the tree |
| sq-gift3 | square | 3513,2576,14 | 0x3C56 a present | community | square | at the tree |
| sq-father | square | 3500,2581,14 | 0x3C40 a statue of Father Christmas | community | square | west edge of the plaza |
| sq-firepit | square | 3499,2577,14 | 0x3C45 a raised firepit | community | square | west of the plaza, two tiles from the Reset Stone |
| sq-snowman | square | 3501,2583,14 | 0x2328 a snowman | osi | square | south-west corner of the plaza (pinned Snowman.cs:5, 0x2328) |
| gate-1 | entrance | 3417,2527,14 | 0x3C57 a candy cane arch | community | floor | west road (x3420, y2527-2531), north side, on grass: 3420,2525 holds a lantern on a stone base |
| gate-2 | entrance | 3420,2533,15 | 0x3C57 a candy cane arch | community | floor | west road, south side |
| gate-3 | entrance | 3494,2487,33 | 0x3C58 a candy cane arch | community | floor | north road (y2486, x3496-3503), west side |
| gate-4 | entrance | 3505,2487,22 | 0x3C58 a candy cane arch | community | floor | north road, east side |
| gate-5 | entrance | 3541,2562,0 | 0x3C57 a candy cane arch | community | floor | east road (x3540, y2567-2572), north side, on grass: the tiles nearer have a stone base and boards |
| gate-6 | entrance | 3540,2574,0 | 0x3C57 a candy cane arch | community | floor | east road, south side |
| gate-7 | entrance | 3468,2635,5 | 0x3C58 a candy cane arch | community | floor | south road (y2636, x3469-3474), west side |
| gate-8 | entrance | 3476,2635,8 | 0x3C58 a candy cane arch | community | floor | south road, east side |
| post-1 | main road | 3498,2563,15 | 0x232C a holiday wreath | osi | post | lamp post 0x0B24 at 3498,2563 z15 on the main road |
| post-2 | main road | 3492,2564,15 | 0x1C12 a holiday bell | osi | post | lamp post 0x0B24 at 3492,2564 z15 on the main road |
| post-3 | main road | 3483,2562,15 | 0x232C a holiday wreath | osi | post | lamp post 0x0B24 at 3483,2562 z15 on the main road |
| post-4 | main road | 3510,2585,14 | 0x1C12 a holiday bell | osi | post | lamp post 0x0B24 at 3510,2585 z14 on the main road |
| post-5 | main road | 3517,2566,16 | 0x232C a holiday wreath | osi | post | lamp post 0x0B24 at 3517,2566 z16 on the main road |
| post-6 | main road | 3519,2578,7 | 0x1C12 a holiday bell | osi | post | lamp post 0x0B24 at 3519,2578 z7 on the main road |
| post-7 | main road | 3500,2529,22 | 0x232C a holiday wreath | osi | post | lamp post 0x0B24 at 3500,2529 z22 on the main road |
| post-8 | main road | 3489,2523,40 | 0x1C12 a holiday bell | osi | post | lamp post 0x0B24 at 3489,2523 z40 on the main road |
| inn-eggnog1 | inn | 3498,2514,33 | 0x3C59 a tray of eggnog | community | table | on the table at z27 (height 6): top z33 |
| inn-cookies | inn | 3498,2516,33 | 0x3C5B a pan of cookies | community | table | on the table at z27 (height 6): top z33 |
| inn-turkey | inn | 3501,2514,33 | 0x3C5E a roast turkey | community | table | on the table at z27 (height 6): top z33 |
| inn-platter | inn | 3506,2515,33 | 0x3C5D a holiday platter | community | table | on the table at z27 (height 6): top z33 |
| inn-canes | inn | 3506,2517,33 | 0x3C5C a tray of candy canes | community | table | on the table at z27 (height 6): top z33 |
| inn-gingerbread | inn | 3506,2519,33 | 0x3C5F a gingerbread house | community | table | on the table at z27 (height 6): top z33 |
| inn-eggnog2 | inn | 3507,2522,33 | 0x3C5A a tray of eggnog | community | table | on the table at z27 (height 6): top z33 |
| inn-fireplace | inn | 3508,2515,27 | 0x3C60 a christmas fireplace | community | indoor | its back to the hall's east wall (x3509), facing into the hall |
| inn-stocking1 | inn | 3508,2513,27 | 0x2BD9 a stocking | osi | wall | north wall of the hall (pinned Stockings.cs:6: 0x2BD9 is the north-wall facing) |
| inn-stocking2 | inn | 3505,2513,27 | 0x2BDB a stocking | osi | wall | north wall of the hall (Stockings.cs:20: 0x2BDB) |
| inn-stove1 | inn | 3494,2516,27 | 0x3C4A an iron stove | community | indoor | the west room with the barrels: the kitchen |
| inn-stove2 | inn | 3508,2524,27 | 0x3C4E a stone stove | community | indoor | the south-east room, by its east wall (x3509) |
| inn-mistletoe | inn | 3510,2519,27 | 0x2375 mistletoe | osi | wallout | outside, on the east wall (x3509) just south of the front door 3509,2518, by the porch rail; the east face shows; pinned Mistletoe.cs:270, 0x2375 the west-wall facing |
| inn-painting | inn | 3502,2514,27 | 0x3C63 a holiday painting | community | wall | north wall |
| inn-snowshield | inn | 3497,2515,27 | 0x3C69 a snow-covered shield | community | wall | west wall of the hall |
| heal-wreath | healer hall | 3461,2547,35 | 0x232C a holiday wreath | osi | wall | north wall, by the east door 3462,2551 |
| heal-garland | healer hall | 3457,2547,35 | 0x3C61 a garland | community | wall | north wall, the middle |
| heal-painting | healer hall | 3454,2549,35 | 0x3C64 a holiday painting | community | wall | west wall |
| heal-snowpainting | healer hall | 3454,2552,35 | 0x3C67 a snow-covered painting | community | wall | west wall |
| heal-shield | healer hall | 3459,2547,35 | 0x3C6A a snow-covered shield | community | wall | north wall |
| off-wreath | field office | 3463,2600,18 | 0x232D a holiday wreath | osi | wallout | outside, on the east wall (x3462), whose east face shows; P31's sign is at 3463,2597 |
| off-painting | field office | 3454,2600,18 | 0x3C66 a holiday painting | community | wall | quarters, west wall (clear of the P31 bookcase 3454,2602 and scroll 3454,2598) |
| off-shield | field office | 3458,2598,18 | 0x3C69 a snow-covered shield | community | wall | office, on the inner wall x3457 (its east face) |
| off-garland | field office | 3457,2597,18 | 0x3C61 a garland | community | wall | office doorway side, north wall |
| dock-sleigh | docks | 3517,2598,1 | 0x3C6E a christmas sleigh | community | pier | the pier's cargo corner by the crates at 3512,2596: a delivery |
| snow-1 | square | 3494,2583,14 | 0x08E2 a pile of snow | osi | floor | outdoors, off the road (the nearest free tile to 3496,2584) |
| snow-2 | square | 3514,2570,14 | 0x3C6B a snow patch | community | floor | outdoors, off the road (the nearest free tile to 3514,2571) |
| snow-3 | inn | 3512,2521,39 | 0x08E0 a pile of snow | osi | floor | outdoors, off the road (the nearest free tile to 3512,2520) |
| snow-4 | inn | 3510,2514,32 | 0x2377 a snowy tree | osi | floor | outdoors, off the road (the nearest free tile to 3512,2514) |
| snow-5 | healer hall | 3449,2548,36 | 0x3C6C a snow patch | community | floor | outdoors, off the road (the nearest free tile to 3448,2545) |
| snow-6 | healer hall | 3445,2564,36 | 0x08E6 a pile of snow | osi | floor | outdoors, off the road (the nearest free tile to 3445,2560) |
| snow-7 | field office | 3465,2598,12 | 0x08E5 a pile of snow | osi | floor | outdoors, off the road (the nearest free tile to 3465,2598) |
| snow-8 | field office | 3461,2591,18 | 0x3C6D a snow patch | community | floor | outdoors, off the road (the nearest free tile to 3460,2593) |
| snow-9 | docks | 3488,2598,4 | 0x08E3 a pile of snow | osi | floor | outdoors, off the road (the nearest free tile to 3488,2598) |
| snow-10 | entrance | 3423,2525,15 | 0x2377 a snowy tree | osi | floor | outdoors, off the road (the nearest free tile to 3423,2524) |
| snow-11 | entrance | 3507,2490,26 | 0x3C6B a snow patch | community | floor | outdoors, off the road (the nearest free tile to 3507,2490) |
| snow-12 | entrance | 3474,2632,10 | 0x08E2 a pile of snow | osi | floor | outdoors, off the road (the nearest free tile to 3473,2632) |

Not decorated, and why:
- **The Warriors' "Guild Hall"** (Aelorn and Dimethro at 3524-3527,2536, z20) is an open training yard, not a
  building.
- **The other guild halls** have no New Haven building of their own. The guild directory is the board.
- **Upper floors.**

## Tests (each watched red, then green)

**Server** (`server\tests\Misc\WinterDecorVerification.cs`, 6 facts, the season fact with 8 dates). Through
`docker\uo\build.sh`:

| Run | Result |
|---|---|
| first green, `--tests-only` | **1025 passed** (the winter facts among them) |
| **red**, `notes\cc-P34-tools\breaks.py apply` | **6 failed, 1019 passed**; break by break below |
| green, after `breaks.py restore` (byte copies, SHA-256 checked, no `P34-BREAK` left), full build | **1025 passed**, image **`sl-modernuo:cc-p34` = `60c57bce705c`**. `latest` untouched |

The red run, one break per fact:

| Break | Failed |
|---|---|
| 1. row `sq-gift2` moved to 3503,2574 | `NoRowSits...`: "sq-gift2 at 3503,2574 is on a protected tile: NPC Sir Helper" |
| 2. January 6 left out (`Day < 6`) | `TheSeasonIs...(2027-01-06 23:59, True)`, and `TheAutomaticCheck...` (its January 6 step became a season change) |
| 3. down also deletes a same-art item on the tile | `UpTwicePlacesOnce...`: the lookalike was deleted |
| 4. `ClusterFWinterDecorArt.Apply()` commented out | `TheServerHasTheWinterArtRecords`: expected "father christmas" |
| 5. the saved state loses "down" | `WinterDecorAndTheStateRoundTrip` |

Fact by fact:
1. `ThePlacementTableLoadsAndEveryItemExists`: unique keys and tiles; every ID is ours (0x3C40-0x3C6E) or a pinned
   OSI holiday ID; every layer is there.
2. `NoRowSits...`: doors and their swings from `ClusterFNewHavenServicesSeeder.Decoration` with
   `BaseDoor.GetOffset`, `ClusterFNewHavenSeeder.Entries`, the spawner tiles, the board, the arrival tile (checked to
   be Sir Helper's seeded tile), the Reset Stone, and the office components.
3. The season on an injected date (Nov 30 23:59 out, Dec 1 00:00 in, Jan 6 23:59 in, Jan 7 00:00 out, and more), and
   `TheAutomaticCheckActsOnlyWhenTheSeasonChanges`:
   - November: nothing;
   - a staff up in November stands;
   - December 1 up, without doubling;
   - a staff down in December stands;
   - January 7 down;
   - a world first seen in season comes up.
4. `UpTwicePlacesOnceAndDownRemovesExactlyTheDecor`:
   - up dryrun and down dryrun change the item count by 0;
   - up twice gives 61, each at its row with its art, hue, not movable, no decay;
   - down twice gives 0, and a gold pile and a same-art lookalike on the first row's tile stay;
   - up after down gives the same 61 keys.
5. `WinterDecorAndTheStateRoundTrip`: the key, art, hue and name come back; the state comes back as null, up and down.
6. `TheServerHasTheWinterArtRecords`: after `ShatteredLegacyArt.Apply`, all 7 records are in `TileData.ItemTable`.
   Names are 19 characters or fewer; the tree is Impassable and the statue has Animation.

**Art** (`player-package\tests\Build-UoOverrides.Tests.ps1`, **11 facts, 11 passed**):
- The new fact `TheWinterDecorRecordsAreTheServersTableAndEveryFrameAndPngIsThere` compares records.json with the C#
  table, checks every animation frame is registered, and checks every winter ID has a PNG with license "none stated".
  It also checks **PNG count = registry art rows (92)** and that no PNG is unregistered.
- **Red, then green:** the sleigh's height set to 12 in records.json gave "height of 15470: expected 10, got 12".
  15455.png moved away gave "PNG for 15455". Both were restored from copies (records.json SHA-256 identical), then 11
  of 11 passed.
- The existing fact that compared the exact tiledata bytes counted only the stone and fox records (120 bytes). It now
  checks by place: no byte changed outside records.json's own records, and each winter record was written with its
  name. It went red first on the old count (120 against 254), as it should.

**P26's gates** (no EA file shipped; PNG count equals registry rows): `Build-PlayerPackage.ps1 -Out <scratch>` built
`ShatteredLegacy-2026.10.12.1657.zip`, 77 MB, with every gate passing. Its `ExternalImages\art` holds 92 PNGs, 47 of
them winter. **Not published.**

**Tools:** `validate.py`: 61 rows, 0 failing. `find-free-art.py --check-registry`: 0 of 94 no longer free.

## Files changed

`D:\ShatteredLegacy`:
- `server\customizations\ClusterFWinterDecorSeeder.cs` (new)
- `server\customizations\ClusterFWinterDecorLayout.cs` (new, generated)
- `server\customizations\ShatteredRunestone.cs` (`ShatteredLegacyArt.Apply` calls the winter records)
- `server\tests\Misc\WinterDecorVerification.cs` (new)
- `player-package\vendor\shattered-legacy-art\`: `registry.csv` (+47 rows), `records.json` (+7 tiledata, +4
  animdata), `SOURCE.txt` (winter section), `art\15424.png` to `art\15470.png` (47 new)
- `player-package\tests\Build-UoOverrides.Tests.ps1`:
  - the server-copy fact limited to its own IDs, its registry counts now 94/92;
  - the byte-exact fact changed from counts to place, with each winter record's name checked;
  - a new winter fact.
- `scripts\anchor-art-frames.py` (`--files`, `--black-transparent`, `--keep-geometry`)
- `CHANGELOG.md`, `VERSION`

`D:\UO\shard-migration`:
- `notes\cc-P34-winter-decor.md`
- `notes\cc-P34-tools\` (tools, `placement.json`, outputs, previews)

## Deviation text for the register

> **F-22 winter event (ours).** From December 1 to January 6 (server time, America/Chicago), New Haven carries a
> winter decoration placed and removed by `ClusterFWinterDecor`. It uses OSI holiday art by art ID (snowman, wreaths,
> mistletoe, stockings, holiday bells, snow piles, snowy trees) and community art by MrRiots ("Winter/Christmas
> Related stuff") and Vrark ("Christmas sprites"), shipped in the player package as IDs 0x3C40-0x3C6E. OSI ran
> seasonal decorations and gifts on its own dates; this one is ours and is not an OSI publish. Pinned's 2004 gift
> giver stays as shipped (its fixed 2004 dates make it inactive).

## Website credits

> Winter decorations: art by **MrRiots** ("Winter/Christmas Related stuff", servuo.dev) and **Vrark** ("Christmas
> sprites", servuo.dev), with OSI's own holiday art. Thank you both.

## Deviations and decisions for Chase

1. **"Guild halls" became the Healer's Hall.** The Warriors' "hall" is an open yard, and New Haven has no other guild
   hall building. The field office was decorated as asked.
2. **Vrark's holiday paintings and garlands sit centred on their tile.** OSI's own wall art sits in the half of the
   tile against the wall. Vrark's are 3D renders with their own layout, and only their format was changed (the rule).
   If they float off the wall in game, the fix is to pad their canvas sideways with transparent columns, which leaves
   the pixels alone, but the brief's rule says to ask first.
3. **"Mistletoe in the doorway" is mistletoe beside the inn's front door,** on the outside east wall at 3510,2519. A
   row may not sit on a door or its swing tile (3509,2518 swings onto 3509,2517), and OSI's mistletoe only hangs on a
   north or west wall (`Mistletoe.cs:262-271`).
4. **Wreaths and bells "on posts" are on the lamp posts' own tiles** (8 lamp posts on the main road), at the post's
   z. How they read against a post is a game check.
5. **The sleigh is on the pier's cargo corner** (3517,2598, by the crates), clear of Norton and of the walkway out.
6. **OSI art by ID, not pinned's classes** (A1): no bells to ring, no stockings to open, no snow to throw, no icy
   patches.
7. **Hourly check instead of daily** (Part C).
8. **Stoves and fireplace are walls to the server** (Wall plus Impassable, as OSI's oven and fireplace are), so
   nothing can be placed through them.

## Checklist for Chase

1. **Commit.** The autopilot does it after this DONE.
2. **Rebuild the test shard** from the commit: Console > Test shard > Rebuild through the gates and start. Or deploy
   the built image: Console > Test shard > Deploy built image... and pick `sl-modernuo:cc-p34`.
3. **Build and publish the player package** (the new art ships with it): Console > Player package > Build package,
   then Publish selected. The scratch build of this tree passed every gate: 77 MB, 92 art PNGs (47 winter). Then
   start `Play TEST Shard.bat` and accept the update. Without it, the decor shows as "UNUSED".
4. **On the test shard, as an Administrator:**
   - `[ClusterFWinterDecor status`: the date, out of season, 0 of 61 placed, automatic check on.
   - `[ClusterFWinterDecor up dryrun`: 61 "would place" lines, nothing placed.
   - `[ClusterFWinterDecor up`: "Outside the dates ... putting it up anyway, for testing", then "placed 61 of 61".
   - `up` again: "placed 0 of 61; 61 already up".
5. **Walk the placement table above, with screenshots for the overseer.** In particular:
   - the square;
   - the Father Christmas torch, firepit and stoves animating;
   - you cannot walk through the tree, statue, fireplace or sleigh;
   - the inn's food on the tables;
   - the wall pieces against their walls (decision 2);
   - the arches at the five gates;
   - the sleigh on the pier.
6. **Take it down:**
   - `[ClusterFWinterDecor down dryrun` lists 61 items.
   - `[ClusterFWinterDecor down` removes 61.
   - New Haven is back to normal; any item of yours on a decor tile is still there.
7. **The live plan:**
   - Publish the package before December 1.
   - Deploy the image that has this to live.
   - The date does the rest. On world load it is out of season, so nothing happens. On December 1 the hourly check
     puts it up; after January 6 it takes it down.
   - Nobody needs to run a command. `status` shows the state at any time.

**Promote to `docs\`:** the deviation text above (fidelity register) and F-22's status in `feature-queue.md`.

P34 DONE
