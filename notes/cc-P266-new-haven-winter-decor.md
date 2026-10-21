# cc-P266: F-22, New Haven winter holiday decorations, ready to switch on December 1

## In plain words

- New Haven gets its winter dress on December 1 and loses it after January 6, by itself: on top of what P34 drafted
  (the square's tree and Father Christmas, the gates' candy canes, the inn's feast) the bank now has a big lit
  Christmas tree, garlands, candles and presents inside, small lit trees at its doors and wreaths on its wall, and
  small lit trees stand on the square and along the main roads with snow between them. 109 pieces in all, 48 new.
- An advent calendar hangs in the bank: double-click it in December and open that day's door for a small gift
  (a gift box with a candy cane for now, a placeholder for you to change), one door a day, once per character.
- Staff see the same `[ClusterFWinterDecor` command with new verbs (`preview`, `place`, `clear`, an area such as
  `bank` after them) and the dates as settings: `clusterf.seasonal.winter.start` and `.end`, 12-01 and 01-06 unless
  changed. The art ships in the player package (47 new pictures and the calendar gump, nothing replaced).
- For you to do: walk the previews (`notes\art\winter-decor\`), say what to move; build and publish the player
  package before December 1; approve the placeholder gifts or name real ones. The pieces whose terms I could not read
  (Hestia's Christmas fireplace) are left out until you clear them.

Builder: Claude (Fable), the Bronze Golem, 2026-10-21. A fresh session on `golem/Bronze/P266` (ShatteredLegacy at
`47b3eae`, shard-migration at `88f4692`), both clean. Pinned is `D:\UO\ModernUO-pinned` (`d4531cd94`); every pinned
citation is at that commit. Image `sl-modernuo:cc-P266`; `latest` untouched. Nothing has run against any world (the
test shard is held by another Golem today; section 7 says what was and was not proven).

## Status: finished on 2026-10-21

## Headlines

- **The winter decor is on the shared seasonal switch** (`ClusterFSeasonalSwitch`, cc-P267's), as P267 intended:
  `clusterf.seasonal.winter.start` and `.end` (`MM-DD`, defaults `12-01` and `01-06`, both inclusive, the window wraps
  the year), `clusterf.seasonal.winter.automatic` (default true). On the start date the hourly check places the
  decor; after the end date it removes **exactly what it placed, by serial** (`ClusterFSeasonalState.Placed("winter")`,
  saved with the world). P34's own copy of the switch and its `clusterf.winterDecor.enabled` setting are gone.
- **Staff commands:** `[ClusterFWinterDecor status | preview [area] | place [area] | clear [area] [dryrun]`
  (Administrator; `up` and `down` still work), and the same verbs on the server console as `winter ...`. `place`
  works before the dates, for the test shard, and says so. An area is a row's area: `bank`, `square`, `main road`,
  `inn`, `entrance`, `healer hall`, `field office`, `docks`.
- **47 new art IDs, 0x3388-0x33B6 (13192-13238), and the gump 22469,** from MrRiots' "Christmas Art for UO" and
  "Christmas Calendar" packs (both say "use as you wish, edit as you wish"), registered first, converted and recorded
  through P26's pipeline. Six pieces animate: the two trees (11 frames each), the candle stand, the candle, the antler
  candelabra and the advent candles. Seven tiledata records, every value from a named OSI tile.
- **The placement is 109 rows: P34's 61 untouched, 48 new,** every one checked against the server's map files
  (`validate.py`: 109 ok) and against a wider protected set than P34 had (P237's community art rows, P267's Halloween
  rows, pinned's spawner rings and decoration, P188's walk). Previews: `notes\art\winter-decor\` (the top-down plan
  `topdown.png` and nine client-view renders).
- **The advent calendar** (`WinterAdventCalendar`, part 5): hangs in the bank, opens MrRiots' 25-door gump; door N
  opens from December N, once per character per year; the gift is a placeholder (`ClusterFWinterAdventGifts.ForDay`).
- **Not an in-game screenshot:** the "preview screenshot" is the client-view render of each area with the real
  pixels drawn in (section 7). No client ran here.

## Part 1: the packs, what is used and what is skipped

Read: `D:\UO\third-party\ART-LIBRARY.md` (section 6 and the legend), each folder's `SOURCE.txt`, the F-22 entry, P34's
and P237's notes. The legend's **REG** means *registered in registry.csv, in the player package*: it is a status, not a
licence. The REG part of `winter-holiday` is P34's 47 IDs (0x3C40-0x3C6E), already shipped; they are used as they are
and **nothing more is registered from that folder** (its licence is "none stated").

| Pack (folder) | Author's terms (SOURCE.txt) | Used | Skipped, and why |
|---|---|---|---|
| `mrriots-christmas` (102 BMP) | "Per usual, use these freely and edit them/label as you wish." EA flag: ships as our PNG overrides only | the two animated Christmas trees (11 frames each; "Thanks Vorspire" is his credit for the animation), the two ribbon garlands, the tall candle stand (4 lit frames), the short candle (4 lit frames), the antler candelabra (4 frames), the advent candles (4 frames, one facing), the poinsettia, the potted tree, the gnome, the toy soldier, the dragon plushie: 47 IDs | the second facings (gnome, soldier, plushies, figurines, reindeer, horseshoes, elk trophy, advent candles) and the unlit frames: no spot uses them; the table cloths, eggnog cauldron and glasses, hot cocoa, coffee press: the inn's tables are P34's feast already; the horseshoes and elk trophy: not winter; the crystal figurines, angel box, nightmare and phoenix plushies: no table top for them in the bank (it has none); his mistletoe: P34 hangs OSI's; the second tall candle (TallCnalde): one candle stand is enough |
| `mrriots-christmas-calendar` (3 BMP) | "Use as you wish, edit as you wish, enjoy!" EA flag | the calendar item, both facings (0x33B5 west wall, 0x33B6 north wall), and the 400 x 400 gump (22469) | nothing |
| `winter-holiday` (342): MrRiots "For ServUO 2" (= `mrriots-winter`, the same 87 files) and Vrark's "Christmas sprites" | none stated on either page (P34 read both); Vrark's two animated trees come from other games | P34's 47 registered IDs, as they are (the rows reuse the presents and snow patches) | every unregistered piece: no terms to read, so nothing new from here; Vrark's animated trees as P34 decided |
| `hestia-christmas-fireplace` (16 BMP, two fireplaces of 8 frames) | **none stated** | nothing | the prompt's rule: a licence I can read that allows use and changes. Hestia's page says nothing. P243 used Hestia's trophies on Chase's say-so (2026-10-21); the same word would clear this one, and it is an hour's work on this pipeline |
| `hestia-christmas-pole` (31 BMP) | none stated | nothing | as above, and the library lists it queued, not for this task |
| the Hestia Christmas window (`hestia-walls-windows-fences`), the queued Christmas village and gift box rows | queued (Q#) or none stated | nothing | not on disk, or no terms |

Also used: OSI's own holiday art by ID (wreaths 0x232D, snow piles 0x08E2/0x08E0/0x08E6/0x08E5/0x08E3 at hue 0x481,
snowy trees 0x2377), as P34 did, in `WinterDecor` items of ours (no bells to ring, no stockings to open).

## Part 2: registration

- `registry.csv`: 47 art rows (13192-13238) and 1 gump row (22469), written by `notes\cc-P266-tools\registry_rows.py`
  before any PNG. Each row's license column quotes the author ("Per usual, use these freely..." / "Use as you wish...")
  and the credit rule: credit MrRiots (the trees' animation with thanks to Vorspire, his words), ship only as our PNG
  overrides inside the player package, never as an EA file, do not repost. 609 rows now (568 art, 16 gump, 24 body, 1 anim).
- Slots: `find-free-art.py --placeholder --run 56` against the tool-trials client copy: the 0x3C00 block P34, P50, P237,
  P243 and P265 used has no run of 40 free IDs left; the longest run is 0x3386-0x3420 (155). This set takes
  0x3388-0x33B6, 8-aligned, straight after the satchel icons (0x3380-0x3385). Gump 22469: FREE (`--explain-gump`).
- PNGs: `art\13192.png` to `13238.png` (456 KB together) by `convert_art.py` through `anchor-art-frames.py --keep-geometry
  --black-transparent`: the 24-bit BMP became a PNG and pure black became transparent, nothing else; the tool re-reads
  each against its source. `gumps\22469.png`: the calendar re-encoded opaque (it has no pure black pixel), 363 KB.
- `records.json`: 7 tiledata and 6 animdata records by `records.py --write`, each value from a named OSI tile:

  | IDs | Name | Flags | Light | Height | From |
  |---|---|---|---|---|---|
  | 13192 | christmas tree (large) | 0x01004041 | | 20 | OSI's tree 0xCCA, Animation added |
  | 13203 | christmas tree (small) | 0x01004041 | | 10 | the same; height as OSI's small banana tree 0xCAB |
  | 13216 | candle stand | 0x05804040 | 29 | 15 | OSI's tall candelabra 0xB26 (Unknown3 is OSI's bit) |
  | 13220 | candle | 0x01804000 | 2 | 1 | OSI's lit candle 0xB1A: walk-over |
  | 13224 | antler candelabra | 0x01808040 | 1 | 5 | OSI's candelabra 0xB1D; ArticleAn |
  | 13228 | advent candles | 0x01804000 | 2 | 3 | OSI's holiday candle 0x236E without PartialHue |
  | 13233 | potted tree | 0x00004040 | | 5 | OSI's potted tree 0x11C8 |

  Animdata: every animated piece runs its frames 0..n-1 at interval 3, as OSI's lit candle, candelabra and holiday
  candle do (read from the client's animdata.mul); the pack gives no timing of its own. Walk-through pieces (ribbons,
  poinsettia, gnome, soldier, plushie, the calendar) need no record (P26 section 13).
- The server's copy is `ClusterFWinterDecorArt.Records` (P34's seven first, then these seven, as records.json holds
  them, with the light shape); `ShatteredLegacyArt.Apply` writes them into `TileData.ItemTable` as before. The package
  fact compares the two by value (section 6).
- `SOURCE.txt`: a section for the set (authors, URLs, their words, the frames in order, what was done to the pixels,
  every record's source, what was left out and why).
- Credits for the website: see the end.

## Part 3: the placement

**Tools** (`notes\cc-P266-tools\`, README there): P237's loader (`nhbase.py`: pinned's GetAverageZ, GetTopSurfaceZ and
CanFit's blocked test over the client copy's map files, the doors, spawners, decoration, the renderer), this task's
`protected.py`, `draft.py`, `validate.py`, `gen_layout.py`, `rend.py`, `topdown.py`.

**Protected tiles** (1,359 in x3400-3660, y2460-2660): doors from `ClusterFNewHavenServicesSeeder` and pinned
DoorGenerator's scan, each with its swing tile (where the seeder places a door, its facing wins over the scan's guess:
P34's mistletoe sits where the scan's guessed swing would have been, knowing the real door swings the other way); every
coordinate literal in any `server\customizations` .cs file but the winter layout itself (so P237's 44 community-art
rows and P267's 17 New Haven Halloween rows are never shared); every pinned spawner with its 8 neighbours; pinned
Decoration cfg items; teleporter ends; every tile of P188's walk. A piece on a table top ignores a spawner's ring and
the scan's guessed swings (it blocks nothing); that is what P34's inn rows needed to pass the wider set.

**Rules by mode** (`validate.py`): P34's (floor: surface within 2 of z, nothing impassable, not a walkway; square and
pier: a walkway allowed; indoor; table: a table top at z; wall: a wall at the floor z behind the art's face; post: a
lamp post; wallout: a wall piece outside) plus **wallfoot**: a street tile at the foot of a building's outer wall
(P267's "outside" rule), for the four trees at the bank's doors, since the ground round the bank is all cobbles.

**The new rows** (`validate.out.txt`; P34's 61 are unchanged and listed in its notes):

| key | area | x,y,z | item | mode | why |
|---|---|---|---|---|---|
| bank-tree | bank | 3489,2565,20 | 0x3388 a decorated Christmas tree | indoor | the alcove north of the hall, against its north wall; the tellers and the doors are clear |
| bank-gift1, bank-gift2 | bank | 3488,2566 / 3490,2566, z20 | 0x3C54, 0x3C56 presents | indoor | at the tree |
| bank-gnome, bank-soldier, bank-plush | bank | 3489,2567 / 3490,2567 / 3490,2568, z20 | 0x33B2 gnome, 0x33B3 toy soldier, 0x33B4 dragon plushie | indoor | in front of the tree |
| bank-calendar | bank | 3487,2566,20 | 0x33B5 an advent calendar | wall | the alcove's west wall (x3486), beside the tree |
| bank-ribbon-w | bank | 3487,2567,20 | 0x339F a ribbon garland | wall | the alcove's west wall, under the calendar |
| bank-ribbon-n | bank | 3486,2569,20 | 0x339E a ribbon garland | wall | the hall's north wall (y2568), its west end |
| bank-candle-tall | bank | 3487,2569,20 | 0x33A0 a tall candle stand | indoor | the hall's north wall, east of the garland |
| bank-antler | bank | 3488,2570,20 | 0x33A8 an antler candelabra | indoor | the hall's north side, off the carpet and the tellers' line |
| bank-potted | bank | 3490,2569,20 | 0x33B1 a potted holiday tree | indoor | the hall's north-east, at the alcove mouth |
| bank-poinsettia-1, -2 | bank | 3486,2570 / 3486,2577, z20 | 0x33B0 a poinsettia | indoor | the hall's north-west and south-west corners |
| bank-candle-short-1, -2 | bank | 3484,2572 / 3484,2574, z20 | 0x33A4 a candle | indoor | the tellers' line, against the west wall between the two tellers (walk-over) |
| bank-out-tree-n, -s | bank | 3493,2567,15 / 3493,2576,14 | 0x3393 a decorated Christmas tree | wallfoot | outside, north and south of the porch, by the east face and the hitching posts |
| bank-out-tree-sw, -se | bank | 3479,2580,15 / 3484,2580,15 | 0x3393 a decorated Christmas tree | wallfoot | outside, at the foot of the south face, either side of the Minter's door (3481,2579) |
| bank-wreath-n, -s | bank | 3492,2566,20 / 3492,2578,20 | 0x232D a holiday wreath | wallout | outside, on the east face (x3491) north and south of the porch (pinned Wreath.cs:258: the west-wall facing, its east face shows) |
| bank-snow-1..6 | bank | 3493,2565 / 3494,2566 / 3495,2568 / 3496,2578 / 3495,2580 / 3490,2581 | snow piles 0x08E2, 0x08E6, 0x08E0; snow patches 0x3C6B, 0x3C6C; a snowy tree 0x2377 | floor | the grass strips north-east, east, south-east and south of the bank |
| bank-snow-7, -8 | bank | 3474,2571,7 / 3475,2583,7 | 0x2377 a snowy tree, 0x08E5 a pile of snow | floor | the slope west and south-west of the bank, by the fence |
| sq-gnome, sq-soldier, sq-poinsettia | square | 3512,2578 / 3513,2577 / 3511,2577, z14 | 0x33B2, 0x33B3, 0x33B0 | square | at the foot of P34's tree (3512,2577), south, east and west |
| sq-tree-ne-1, -2 | square | 3509,2570 / 3513,2570, z14 | 0x3393 a decorated Christmas tree | floor | the grass north-east of the square, by the road in from the north |
| sq-snow-ne | square | 3507,2569,14 | 0x08E3 a pile of snow | floor | between the two trees |
| road-inn-w, road-inn-e | main road | 3498,2536,21 / 3507,2535,20 | 0x3393 | floor | the road south from the inn, west and east sides, below the lamp post at 3500,2529 |
| road-inn-snow | main road | 3496,2536,22 | 0x3C6D a snow patch | floor | the grass west of the road below the inn |
| road-healer | main road | 3484,2544,15 | 0x3393 | floor | the road west to the Healer's Hall |
| road-main-w, road-main-e | main road | 3494,2560,15 / 3512,2561,14 | 0x3393 | floor | the main road into the square, west (north-east of the bank) and east |
| road-main-snow-w, -e | main road | 3493,2559,15 / 3511,2563,14 | 0x08E2 a pile of snow, 0x3C6B a snow patch | floor | the grass beside the main road |
| road-east-n, road-east-s | main road | 3521,2567,7 / 3519,2572,6 | 0x3393 | floor | the east road to the gate, north and south sides (the road runs low here, z6-7) |
| road-east-snow | main road | 3524,2567,6 | 0x08E6 a pile of snow | floor | the grass north of the east road |
| inn-advent | inn | 3503,2513,33 | 0x33AC advent candles | table | on the table by the inn's north wall that P34 left bare (z27, top z33) |

**How the bank was read:** the hall is x3485-3490, y2569-2578 at z20; the tellers stand at 3484,2570 and 3484,2576
(pinned Vendors.json) with the west wall x3483 behind them; the doors are in the east wall x3491 at y2571 and y2573
(swings 3492,2570 and 3492,2574) onto a porch with steps east; the alcove x3487-3490, y2565-2568 opens off the hall's
north-east. The walk from the doors to the tellers crosses the hall's middle, so nothing that blocks goes there: the big
tree, the candle stand, the candelabra and the potted tree stand in the alcove and along the north wall; the floor
candles are walk-over and stand between the tellers against their wall. The bank has no table, so the figurines stayed
in the pack.

**Facings** measured as P34 did (the art's top edge: falling to the right is a north wall, to the left a west wall):
ChristmasRibbon.bmp north, ChristmasRibbon1.bmp west; calendar 2.bmp north, 1.bmp west. The hall's and alcove's north
and west walls are the faces the client shows.

**Not decorated:** the bank's vault and the Minter's room (crates and shelves, the Minter's spawner ring); the upper
floor; the docks beyond P34's sleigh and P237's lanterns.

**Previews** (`notes\art\winter-decor\`, committed; the full-size PNGs are git-ignored in the tools folder):
`topdown.png` (the top-down plan of the town with every row as a coloured square, new rows ringed in magenta),
`preview-bank-inside.jpg` (the roof off), `preview-bank-outside.jpg`, `preview-square.jpg`, `preview-road-inn.jpg`,
`preview-road-main.jpg`, `preview-road-east.jpg`, `preview-road-healer.jpg`, `preview-inn.jpg`, `preview-town.jpg`
(the whole town at half size). Magenta rings mark the new rows, blue P34's.

## Part 4: the switch and the seeder (`server\customizations\ClusterFWinterDecorSeeder.cs`)

- `ClusterFWinterDecor.Season = new ClusterFSeasonalSwitch("winter", "WinterDecor", "12-01", "01-06", Up, Down)`:
  the shared class reads the two settings (writing the defaults on a first start; a value that is not `MM-DD` falls
  back and says so on the console), hooks world load, and runs `Sync` then and every hour: up when the window opens,
  down after it closes, acting only when the season differs from the state it last brought the world to. A staff
  `place` before December 1 or a `clear` inside the window stands until the season next changes.
- **By serial:** `Up` adds each placed item's serial to `ClusterFSeasonalState.Placed("winter")`; `Placed()` resolves
  them (a serial whose item is gone is dropped); `Down` deletes those and, so the world is never left with one, any
  stray `WinterDecor` or `WinterAdventCalendar` the list does not know (both types are made only here), and says so.
  Nothing else on a decor tile is touched: not a player's item, not a same-art lookalike.
- **Rows** come from `ClusterFWinterDecorLayout` (generated): a row whose layer is `calendar` becomes a
  `WinterAdventCalendar`, every other row a `WinterDecor`. The layout also carries `RegisteredIds` (the 94 winter IDs
  registry.csv holds) so the test refuses a row with an ID nobody registered.
- **Commands:** `[ClusterFWinterDecor status | preview [area] | place [area] | clear [area] [dryrun]` (Administrator,
  `[ShardCommand]` WorldSetup / Skips / TestFirst / preview), `up` and `down` kept as aliases; the console command
  `winter ...` posts the same `Run` to the game loop. `status` says the local date, the season, the rows up by area and
  the automatic check's state. Both are in `docker\uo\COMMANDS.md`.
- **Gone:** `ClusterFWinterDecorState` (P34's own persistence, "WinterDecor") and `clusterf.winterDecor.enabled`. A save
  written by P34's build keeps an orphan `WinterDecor` folder that pinned's `Persistence.Load` never reads (it loads
  the registered persistences only, `Server/Serialization/Persistence.cs:54-66`); a `modernuo.json` that holds the old
  key keeps an unused line. Neither has been on live: P34 was never placed on a world (its notes).

## Part 5: the advent calendar (`server\customizations\WinterAdventCalendar.cs`)

- `WinterAdventCalendar : Item, IWinterDecorItem`: the row's key, the year its openings belong to, and per character
  a bit per door opened (`Dictionary<Mobile, int>`, through the serialization generator as pinned's `ChampionSpawn`
  does). Not constructible by `[add`, not movable, does not decay. Double-click within 3 tiles opens the gump.
- `WinterAdventCalendarGump`: MrRiots' picture (gump 22469) with a small button on each of the 25 doors (5 x 5 cells of
  80 px) and a check mark on a door already opened; the line under it says which doors are open today.
- The rule (`TryOpen(from, day, local)`): door N opens from December N on, in December only, once per character; a new
  year clears the openings. The gift goes to the backpack, or the bank box when the backpack refuses.
- **Placeholder gifts:** `ClusterFWinterAdventGifts.ForDay(day)` returns a `GiftBox` named "an advent calendar gift
  (December N)" holding a `CandyCane`. Chase names the real gifts; that table is the only thing to change.

## 6. Tests (each watched red, then green)

See the run table below (section 6.1). Facts in `server\tests\Misc\WinterDecorVerification.cs` (10 facts, one a theory
of 8 dates):

1. `ThePlacementTableLoadsAndEveryItemIsRegisteredOrStock`: 109 rows, unique keys and tiles, every ID registered
   (both blocks) or an OSI holiday ID, every record's ID registered; the bank has the large tree, garlands, lights
   and snow and four small trees outside, the square two and the main roads six; exactly one calendar, in the bank.
2. `NoRowSitsOnADoorItsSwingAnNpcASpawnerAFixedTileOrACommunityArtTile`: P34's fact plus P237's 44 rows.
3. `TheSettingKeysAndDefaultsAreThePromptsAndTheSwitchIsTheSharedOne`; the 8-date theory (Nov 30 out, Dec 1 in, Jan 6
   in, Jan 7 out ...); `ABadDateSettingFallsBackToTheDefaultAndSaysSo` (and a moved window moves the season).
4. `TheAutomaticCheckPlacesInRangeRemovesAfterAndActsOnlyWhenTheSeasonChanges`: November nothing; a staff place
   stands; December 1 up without doubling; a staff clear in December stands; January 7 down, zero winter items
   left; a world first seen in season comes up; the window from the settings (12-20 to 12-26) decides.
5. `PlaceTwicePlacesOnceAndClearRemovesExactlyTheDecorBySerialAndNothingElse`: preview changes nothing and tracks
   nothing; up twice gives 109 items, each at its row, tracked by serial, the calendar its own type; down removes
   them and leaves a gold pile and a same-art lookalike on the first row's tile, the world's item count back by
   exactly 109; up after down restores the same keys. `AnAreaFilterPlacesAndClearsOnlyThatArea` (`bank`, `main road`).
6. `TheDecorAndTheStateSurviveARestart`: the item round-trips; the state is written, wiped and read back with the same
   serials; the in-season check and a second place add nothing; a vanished item is dropped; a stray is swept and
   reported by the season's end.
7. `TheServerHasTheWinterArtRecords`: 14 records in `TileData.ItemTable` with name, flags, height and light shape;
   the lit tree blocks and animates, the candle stand lights (29), the floor candle is walk-over.
8. `TheAdventCalendarOpensOneDoorADayOncePerCharacterAndStartsFreshEachYear`: not before December, not a day not
   come, not a non-door; December 3 opens doors 3 and 1 once each (two gift boxes in the backpack, named for the day);
   another character has its own doors; door 25 on the 25th; January refuses; next December opens door 3 again; the
   openings round-trip with the item; the seeder places it as its own type and clears it.

**Art** (`player-package\tests\Build-UoOverrides.Tests.ps1`): the winter fact now compares both blocks with the C#
table (14 records, the light shape too, the regex taking the optional sixth value and `Unknown3`), lists the ten
animated IDs, checks the 47 second-block rows' PNGs and licences (the author's words and the credit) and the calendar
gump's row and 400 x 400 PNG; the registry counts are 609 rows, 16 gumps, 568 art; the kitsune filter skips the new
block; the by-place byte check names the new records too.

### 6.1 Runs

**Art** (`powershell -File player-package\tests\Build-UoOverrides.Tests.ps1`, 20 facts; the two Play facts pass on this PC
because the test shard answers):

| Run | Result |
|---|---|
| first run after the edits | 18 passed, 2 failed: my own test code (the kitsune fact's animdata filter took in the new block; the gump size read `[byte] -shl 8` as a byte, 400 came back as 144). Both fixed in the test file |
| green | **20 passed** |
| **red:** the candle stand's light set to 0 in records.json, `gumps\22469.png` moved away | 19 passed, **1 failed**: "light shape of 13216 ... expected [29] but got [0]" (the fact stops at its first assertion, so the missing PNG was not reached) |
| green, after a byte-for-byte restore (records.json SHA-256 equal, the PNG moved back) | **20 passed** |

`find-free-art.py --check-registry` (the tool-trials client copy): **0 of 609 registered IDs are no longer free.**

**Server** (`docker\uo\build.sh -t sl-modernuo:cc-P266`, each cycle detached with its log in the session scratchpad;
Windows had 11.5 GB available before the first):

| Run | Result |
|---|---|
| 1 (`--tests-only`) | the builder stage refused: a missing comma after the sleigh record once P34's seven were moved ahead of P266's (my edit). Fixed |
| 1b (`--tests-only`) | refused again: the test project treats xUnit analyzer rule xUnit2013 as an error (`Assert.Equal(0, list.Count)`); two assertions reworded to `Assert.Empty` / `Assert.Single` |
| 1c (`--tests-only`) | **2,084 passed, 1 failed**: `TheSettingKeysAndDefaults...` read `ClusterFSeasonalSwitch.All["halloween"]` before anything had touched the Halloween class, so its static switch was not registered in the host (a test-host trap, not the shard); the fact now asserts on `ClusterFHalloweenDecor.Season` itself |
| **2, red** (`breaks.py apply`, `--tests-only`) | **2,075 passed, 10 failed: every winter fact and nothing else** (the theory's other seven dates passed). Break by break below |
| **3, green** (`breaks.py restore`: byte copies, SHA-256 equal, no `P266-BREAK` left; the full build) | **2,085 passed, 4 skipped**, image **`sl-modernuo:cc-P266` = `77504be47da0`**; `latest` (`f53bfa00612d`) untouched |

The red run, one break per fact:

| Break | Failed |
|---|---|
| 1. the square's gnome given 0x33B7, an ID nobody registered | `ThePlacementTableLoads...`: "sq-gnome: 0x33B7 is neither a registered winter ID nor an OSI holiday ID" |
| 2. the bank's plushie moved onto P237's fruit cart tile 3512,2574 | `NoRowSitsOn...`: "bank-plush at 3512,2574 is on a protected tile: community art market-fruit" |
| 3. the default end set to 01-05 | `TheSettingKeysAndDefaults...` (expected "01-06"), the theory's January 6 case (expected in season, got out), and `TheDecorAndTheStateSurviveARestart` (the window string) |
| 4. place forgets to remember what it placed, by serial | `TheAutomaticCheck...` (expected 109 placed, got 0 tracked), `PlaceTwice...`, `AnAreaFilter...` |
| 5. clear also deletes a same-art item on a row's tile that is not ours | `PlaceTwice...` (the lookalike, reached once break 4 was the first assertion to trip in that fact) |
| 6. the candle stand's light shape set to 0 | `TheServerHasTheWinterArtRecords`: expected 29, got 0 |
| 7. a door opens before its day | `TheAdventCalendar...`: expected NotYet, got Opened |

## 7. What was proven where, and what was not

**On a private throwaway container, not the shared test shard** (`sl-p266-proof` from `sl-modernuo:cc-P266`, a fresh
world in the session scratchpad, the test shard's two configuration files copied out of the running `sl-modernuo-test`
with `docker cp` and the winter window set to `10-01` to `11-30` so 2026-10-21 is in season; the tool-trials client
copy as the data directory; a tty as the test compose file gives; the Golem accounts manifest so the owner-account
prompt never asks; `notes\cc-P266-tools\..\..\` has no copy of the script, it lives in the session scratchpad as
`proof\proof.sh`). The evidence is the shard's own log (`docker logs`):

| Step | What was done | What the shard logged |
|---|---|---|
| 1 | first start on the image, window 10-01 to 11-30 | `[WinterDecor] 2026-10-21: the season has begun (10-01 to 11-30).` `placed 109 of 109 row(s); 0 already up.` then the start-up status `up: 109 of 109 rows placed (by serial).` (the Halloween decor, 10-24 to 11-02, stayed down: `out of season`, `0 of 316`) |
| 2 | the world saved (an automatic save at 17:15:00 Chicago, kept as `Backups\Automatic\2026-10-21-22-15-00`) | `SeasonalDecor\SeasonalDecor.bin`, decoded: version 0, two seasons; `halloween` down with 0 serials; **`winter` up with 109 serials** (0x40000298 to 0x40000304). **The serial list is saved with the world.** |
| 3 | `end` set to `10-20`; the shard that wrote the last save started at 17:13:36 (`status\status.json`: version 2026.10.21.21) and saved at 17:16:26 | that save's `SeasonalDecor.bin`: `halloween` down, 0; **`winter` down with 0 serials.** The switch brought the world down once the window closed. |

**What was lost:** the second start's console lines (`the season is over ... removed 109 tracked item(s) by serial`),
the lines P267 quoted for Halloween. The harness stopped the proof script for low memory (2.7 GB free afterwards) while
a first, mis-mounted attempt's shell was still alive (`TaskStop` ends the shell, not a `sleep` already running, and
that shell went on to stop and remove the container it shared a name with), so the container's log went with it and
the two attempts' saves cannot be told apart line by line. Per the harness's note it was not started again. What the
saves say stands on their own: a save with the switch up and 109 serials, then a save with it down and none, from a
shard on this build. The restart path itself is pinned by `TheDecorAndTheStateSurviveARestart` and was walked on the
real test shard by P267 for the same shared class.

Not proven here, for want of a client: the `[ClusterFWinterDecor` command typed in game and the console verbs typed
on a tty (both call the same `Run` the facts cover: place, preview, clear, the area filter), what the pieces look like
in game (the previews stand in: the same pixels the client draws, placed from the map files), whether any piece is in
a walker's way (the tile rules stand in), and the calendar gump's look (the fact covers its rule, not its picture).
Section "For Chase" says what to walk.

## Files changed

`ShatteredLegacy` (the Bronze worktree):
- `server\customizations\ClusterFWinterDecorSeeder.cs` (rewritten on the shared switch; the records table carries both blocks)
- `server\customizations\WinterAdventCalendar.cs` (new: the item, the gump, the placeholder gifts)
- `server\customizations\ClusterFWinterDecorLayout.cs` (regenerated: 109 rows, `RegisteredIds`)
- `server\customizations\ClusterFVisualBuilder.cs` (a comment named the removed persistence)
- `server\tests\Misc\WinterDecorVerification.cs` (rewritten)
- `player-package\vendor\shattered-legacy-art\`: `registry.csv` (+47 art, +1 gump), `records.json` (+7 tiledata, +6
  animdata), `SOURCE.txt` (the set's section), `art\13192.png` to `13238.png` (47 new), `gumps\22469.png` (new)
- `player-package\tests\Build-UoOverrides.Tests.ps1` (the winter fact, the counts, the filters)
- `docker\uo\COMMANDS.md` (the `[ClusterFWinterDecor` row), `CHANGELOG.md` (2026.10.21.21), `VERSION`

`shard-migration` (the Bronze worktree):
- `notes\cc-P266-new-haven-winter-decor.md`
- `notes\cc-P266-tools\` (tools, `placement.json`, `validate.out.txt`, `breaks.py`; the PNG previews git-ignored)
- `notes\art\winter-decor\` (the picture set for Chase)

## Website credits

> Winter decorations: art by **MrRiots** ("Winter/Christmas Related stuff", "Christmas Art for UO" with its animated
> trees by Vorspire, and the "Christmas Calendar", all on servuo.dev) and **Vrark** ("Christmas sprites", servuo.dev),
> with OSI's own holiday art. Thank you all.

## Deviation text for the register

> **F-22 winter event (ours).** From `clusterf.seasonal.winter.start` to `.end` (12-01 to 01-06 unless changed, server
> time, America/Chicago), New Haven carries a winter decoration placed and removed by `ClusterFWinterDecor` on the
> shared seasonal switch, tracked by serial. It uses OSI holiday art by art ID and community art by MrRiots and Vrark,
> shipped in the player package as IDs 0x3C40-0x3C6E and 0x3388-0x33B6 with the advent calendar gump 22469. OSI ran
> seasonal decorations and gifts on its own dates; this one is ours and is not an OSI publish. The advent calendar is
> ours (daily placeholder gifts, one door a day in December). Pinned's 2004 gift giver stays as shipped (inactive).

## Deviations and decisions for Chase

1. **The Hestia fireplace is out** (no terms stated). Say "cleared" and it is an hour on this pipeline.
2. **Hestia-free, MrRiots-heavy:** every new piece is MrRiots'. His terms are the only ones that say "use and edit".
3. **Snow outside the bank is on the grass strips, the trees on the cobbles at the wall's foot** (the whole plaza round
   the bank is paved). The four small trees stand against the building, clear of the porch, the steps and the Minter's
   door. If one is in a walker's way in game, the row moves: `placement.json`, `validate.py`, `gen_layout.py`, rebuild.
4. **The tellers' candles are walk-over** (OSI's floor candle flags), so a player who stands between the tellers is not
   blocked. The candle stand and candelabra block, like OSI's; both stand along the north wall, off the walk.
5. **The calendar's doors are small arrow buttons** in each cell's lower-left (gump 4005), not the picture's own doors:
   an invisible button over the art is possible but a visible one is what every client shows the same way. Opened
   doors carry a ticked box. Say if you want the picture's cells themselves to be the buttons.
6. **Gifts are placeholders**: a gift box with a candy cane, named for its day. Name real ones and they go in
   `ClusterFWinterAdventGifts.ForDay`.
7. **P34's rows are untouched**, including the four that fail the wider protected set only on table and door-scan
   technicalities (section 3 says how the rules let them stand). Chase has not walked P34's table either: walk both.
8. **The advent calendar is one item in the bank**, per character, not per account. An account's other characters can
   each open a door. Say if that should be per account.
9. **No client ran:** the preview screenshot is the client-view render (the same pixels the client draws, from the map
   files), not a capture of the client. Section 7 lists what only a walk can tell.
10. **The proof ran on a private container, not the shared test shard.** The test-shard lock was the Iron Golem's for
    most of the sitting; once it was mine, a start from this worktree would still have rebuilt the shared shard's world
    and configuration from a tree that has neither (both are git-ignored and live in the main copy this Golem may not
    open). A throwaway container from the same image, with the test shard's own configuration copied out of the running
    container, proves the same switch without touching anyone's world (section 7). The shared test shard was not
    restarted and still runs `latest`.
11. **Typed console verbs were not run:** Docker from this harness has no terminal to attach, and a redirected stdin
    puts pinned ModernUO in headless mode (`Main.cs:582`), where the console pump is off. P267 typed its verbs through
    `winpty docker attach` from a real console; Chase can do the same on the test shard (`winter status`, `winter
    place bank`, `winter clear`).

## For Chase

1. **Commit.** The Golem does it after this DONE.
2. **Build and publish the player package** (Console > Player package > Build package, then Publish selected) before
   December 1: without it the new pieces show as "UNUSED" tiles. (Not built here: the package build takes the package
   lock and a scratch build was not needed to prove the art; the package facts pass.)
3. **Rebuild the test shard** from the commit, or deploy `sl-modernuo:cc-P266`. On its first start the shard writes
   `clusterf.seasonal.winter.start = 12-01`, `.end = 01-06`, `.automatic = True` into the test `modernuo.json`.
4. **On the test shard, as an Administrator:** `[ClusterFWinterDecor status` (out of season, 0 of 109);
   `[ClusterFWinterDecor preview` (109 "would place" lines); `[ClusterFWinterDecor place` ("Outside the dates ...
   putting it up anyway", "placed 109 of 109 row(s); 0 already up."); `place` again ("placed 0 of 109; 109 already
   up"); `[ClusterFWinterDecor place bank` and `clear bank` to try one area.
5. **Walk the previews in game** and say what to move: the bank's alcove (the tree, the calendar on the west wall, the
   garlands flat on their walls, the candles lit and animating), the tellers' candles, the four trees at the bank's
   doors and the wreaths on its east face, the square's north-east trees, the roadside trees (seven), the inn's advent
   candles on their table. Then P34's table, which nobody has walked either.
6. **Open the calendar** (double-click it; on the test shard set `clusterf.seasonal.winter.start` earlier or wait for
   December): a door's button gives the placeholder gift once.
7. **Take it down:** `[ClusterFWinterDecor clear dryrun` lists 109; `clear` removes 109 and nothing else.
8. **Live:** deploy the image and publish the package before December 1; the date does the rest. `status` at any time.

**Promote to `docs\`:** the deviation text above (fidelity register), F-22's status in `feature-queue.md`, the website
credits, and the `uo:world:seasonal` wiki page P377 keeps (the winter row: dates, settings, the calendar).

P266 DONE
