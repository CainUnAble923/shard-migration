# cc-P135: vseUOAware part 2: in-game staff commands and the console home (Parts A and D)

2026-10-17. Parts A and D of the vseUtilities adaptation, after cc-P134 (Parts B and C, DONE). Part A adapts
vseUOAware's placement, statics, water and snippet tools as six ModernUO staff commands over the server's own map;
Part D puts the art checks and the commands' syntax on a Shard Console tab. ASCII only.

## Headlines

1. **Six GameMaster commands in `server\customizations\StaffHub\ClusterFMapCheckCommands.cs`**, over the check library
   `ClusterFMapCheck.cs` beside it (both GPL-3.0, credit line in each header): `[CheckFootprint`, `[ValidateSpots`,
   `[FindStaticProblems`, `[Walkable`, `[ShoreCheck`, `[ExportPoints`. They read ModernUO's loaded map, statics and
   tiledata (file:line in section 2) and report; nothing changes a world. The one thing that places anything,
   `[Walkable overlay`, drops red runes that delete themselves (default 60 s, max 600), never survive a restart, and
   is refused on the live shard.
2. **13 facts over a hand-built region** in `server\tests\Misc\MapCheckVerification.cs` (the gate's host loads no client
   files), every one watched red by a deliberate break of the behaviour it guards, then green (section 4). Four
   more facts run against the **real maps** when tile data is present (`MapCheckRealDataVerification.cs`, skipped in
   the gate): the adapter agrees with cc-P134's independent UOP read of New Haven, and `[ValidateSpots` was pointed at
   the twelve world-setup spawn files and every decoration file (section 5).
3. **Part D: a "Map and Art" tab in the Shard Console** (`scripts\Shard-Console.ps1`), argued in section 6: four
   buttons run `validate-art.py`'s read-only checks (registry, body table, check a .vd or propose a body, hues diff)
   with the output in the Action output pane, and six print the in-game commands' syntax. 8 new console facts, each
   watched red (section 7). `Test-PlanSafety` lets python run only as `validate-art.py` with a read-only subcommand,
   never `render`.
4. **Built and tested through `build.sh` as `sl-modernuo:cc-p135`**: 1,398 passed, 4 skipped (the real-data facts), 0 failed, and the runtime image `sl-modernuo:cc-p135` was built (section 8). The red rounds and the real-data run are sections 4 and 5.
5. **The Argonious buildings and the stampers are not wired to the check** (section 3.1): a hook is one call,
   `ClusterFMapCheck.CheckFootprint(new ClusterFMapTileSource(map), x, y, w, h)`, but `[StampLayout` stamps indoor
   furniture where walls always "block", and no .uoa importer exists yet. Say if you want it on the stamp anyway.

## 1. Where things are

| File | What |
|---|---|
| `D:\ShatteredLegacy\server\customizations\StaffHub\ClusterFMapCheck.cs` (new) | `IClusterFTileSource` (land, statics, flags for one map), `ClusterFMapTileSource` (the real one over `Map.Tiles` and `TileData`), the checks (`Blocked`, `CheckFootprint`, `ParseSpotLines`/`ParseSpawnerJson`/`ParseDecorationCfg` + `Validate`, `FindStaticProblems`, `CheckWalkable`, `CheckShore`), the JSON writers (`PointsJson`, `RectangleJson`), file rules (`ResolveReadable`, `WriteReport`), and `ClusterFWalkMarker`, the self-deleting rune |
| `...\StaffHub\ClusterFMapCheckCommands.cs` (new) | the six commands, targets and bounding boxes, the report files |
| `D:\ShatteredLegacy\server\tests\Misc\MapCheckVerification.cs` (new) | 13 facts over the hand-built region |
| `D:\ShatteredLegacy\server\tests\Misc\MapCheckRealDataVerification.cs` (new) | 4 skippable facts over the real maps |
| `D:\ShatteredLegacy\scripts\Shard-Console.ps1` (changed) | the Map and Art tab: actions, plans, safety rule, child line, headless entry, tooltips, the page |
| `D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1` (changed) | 8 `P135_` facts; the tab list fact and the click harness extended |
| `D:\ShatteredLegacy\CHANGELOG.md`, `VERSION` (changed) | 2026.10.17.5, one Staff line |
| `D:\UO\shard-migration\notes\cc-P135-tools\` (new) | the red-first runs and the real-data reports quoted here |

Why StaffHub: the brief named it the natural home, and it is where staff tooling that is not a seeder lives
(`ClusterFStaffHub.cs` lists every `[ShardCommand]` outside Player, so the six appear in the hub's Diagnostics
category with no upkeep). The checks are a library file apart from the commands so the facts can run them over a
fake map, and so a stamper can call them without going through a command.

## 2. Pinned ModernUO behaviour used (d4531cd94; the brief says 7c9215d97, AGENTS.md says cc-P38 moved it)

| What | Where |
|---|---|
| the map's tile matrix | `Projects/Server/Maps/Map.cs:105` (`Tiles`), `:111-113` (`Width`, `Height`) |
| land tile at x,y: `GetLandTile` | `Projects/Server/TileMatrix/TileMatrix.cs:341`; `LandTile.ID`, `.Z` `:527-551` |
| map statics at x,y, no multis: `GetStaticTiles` | `TileMatrix.cs:271` (`includeMultis: false`); `StaticTile.ID`, `.Z`, `.Hue` `:554-600`; the enumerator `Maps/Map.StaticTileEnumerator.cs:60-72` reads the static block the same way |
| land flags: `TileData.LandTable[id & MaxLandValue].Flags` | `Projects/Server/TileData.cs:288`, read as `Map.CanFit` reads them `Maps/Map.cs:944` |
| item flags, name, height: `TileData.ItemTable[id & MaxItemValue]` | `TileData.cs:289`, `:59-105`; read as `Map.CanFit` reads them `Map.cs:960`; indexed by the item id itself `:369` (vseUOAware's `0x4000 + id` is the file's layout) |
| `TileFlag.Impassable 0x40`, `Wet 0x80`, `Surface 0x200` | `TileData.cs:225-228` |
| a table slot for every 16-bit item id (`MaxItemValue = 0xFFFF`) | `TileData.cs:289`, `:381-382`; so "no tiledata entry" here means an empty entry (no name, flags, height), never "past the table" |
| `Map.TryParse` for a map name or number | `Maps/Map.cs:1765` |
| `BoundingBoxPicker.Begin(from, (map, start, end) => ...)` | `Projects/UOContent/Commands/BoundingBoxPicker.cs:9` (namespace `Server`) |
| ground targets: `Target(-1, true, TargetFlags.None)`, `IPoint3D` | `Projects/Server/Targeting/Target.cs:12`, `:216`; as `ClusterFLayoutCapture.StampTarget` uses them |
| a self-deleting item: `Timer.StartTimer(delay, Delete)` in the constructor and again `[AfterDeserialization]` | `Projects/UOContent/Items/Misc/Blood.cs:18-25`, `Projects/Server/Timer/Timer.DelayCall.cs:60` |
| the spawn files' JSON: `"location": [x, y, z]`, `"map": "Trammel"` | `UOContent/Engines/Spawners/Json/Point3DArrayConverter.cs:18-27`, `Server/Json/Converters/MapConverter.cs:32-33`, `SpawnerDto.cs:42-51` |
| `"spawnBounds": {x1, y1, x2, y2}` with exclusive x2,y2 (Rectangle3D's End), Z -128..127 when absent | `Server/Json/Converters/Rectangle3DConverter.cs:176-194` (write), `:58-165` (read: `x1..y2` keys build `Rectangle3D(start, end)`, `hasZ` false gives -128..127) |
| `JsonConfig.DefaultOptions` carries those converters, so the facts read the export back with ModernUO's own reader | `Server/Json/JsonConfig.cs:28-52` |
| decoration .cfg grammar: header `Type 0xID(params)`, then `x y z [extra]` lines to a blank one, `#` comments; which maps each folder decorates | `UOContent/Commands/Object Creation/Decorate.cs:1308-1380`, `:1419-1427` (`DecorationEntry`), `:37-46` (Britannia = Trammel and Felucca) |
| spawn files are found under `Core.BaseDirectory` | `UOContent/Engines/Spawners/Commands/ImportSpawnersCommand.cs:38-42` |
| the test host loads tile data only from `MODERNUO_TEST_DATA_DIR` or `C:\Ultima Online Classic`, else `TileDataLoaded` is false and tile facts skip | `UOContent.Tests/Fixtures/TestServerInitializer.cs:34-39`, `:56-59`, `:84`; `Fixtures/TileDataRequirement.cs:13-17` |
| `GetLandBlock` returns the invalid block while `MapStream` is null, whatever `SetLandBlock` stored | `TileMatrix.cs:293-297`: why the facts cannot hand a fake block to a real `Map` and use a fake source instead |
| `TestCenter.Enabled`, the test-shard switch | `UOContent/Special Systems/Engines/TestCenter.cs:15-19`, as `ClusterFStaffHub.IsTestShard` reads it |

vseUOAware source adapted (`D:\UO\third-party\code\vseutilities\vseProjects\vseUOAware\vseUOAware_09272026_Latest\vseUOAware\Tools\`):
`MapPlacementTools.cs` (`ValidateCoordinateList`, `CheckHousePlacement`, `Blocked`), `MapStaticsTools.cs`
(`FindStaticProblems`, `CheckWalkability`), `WaterTools.cs` (`FindDeepWaterNearShore`), `SnippetTools.cs`
(`GenerateCodeSnippet`). Read, never built or run; the MCP server cc-P134 built from a copy was used only to cross-check
numbers (section 5).

**What was kept of his rules, and what changed:**
- Blocked tile: his rule exactly (Wet land; Impassable land; a static with Z in [landZ, landZ + 16] whose tiledata is
  Impassable and not Surface). `[ValidateSpots` uses the spot's own Z as the base when a line or spawner gives one
  (his validator ignored z); a spot with no z uses the land Z as he did.
- Footprint: his (every tile on the map, none blocked, Z spread within the limit, max 64x64).
- Statics: his three problems and his thresholds (duplicate = same id and Z on one tile, hue ignored; buried = 10 or
  more below the land; unknown id). A box past the map edge checks the tiles that exist instead of erroring.
- Shore: his definition of water (Wet land, or a non-Wet land tile under a Wet static, whose surface is its highest
  Wet static), his 8-neighbour shore test, his seven height buckets, his one fault (|Z| > 120). The CSV he could
  write to any folder is a report file in the map-checks folder.
- Snippets: not ServUO C# arrays but the spawn files' JSON (Why section of the brief). A list is
  `[{ "location": [x, y, z], "map": "Trammel" }, ...]`; a rectangle is one object with `spawnBounds` and its centre
  as `location`. `[ValidateSpots` reads the list back, so a captured list can be checked.
- Caps: his 500 coordinates, 64x64 footprint, 512x512 area. Overlay markers are capped at 2,000 a run.

## 3. The commands

All GameMaster, declared `[ShardCommand(CommandCategory.Diagnostic, Shard = CommandShard.Any)]` (read only; the hub
lists them under Diagnostics; the console's World setup tab shows world-changing commands only, so they are not
there, and the Map and Art tab prints their syntax instead). Full reports longer than the in-game cap go to
`<world folder>\map-checks\<command>-<time>.txt` beside `layout-captures\`, and the message names the file.

| Command | Then | What it says |
|---|---|---|
| `[CheckFootprint <width> <height> [maxZSpread=5]` | target the top-left corner | `Footprint (x,y) WxH: CAN be placed` or `CANNOT be placed. N blocked tiles, land Z a..b (spread s, allowed m).`, then each blocked tile and why (20 listed) |
| `[ValidateSpots <file under Data> [map]` | no target | `N spots checked: a ok, b with problems[, c lines not understood][, d past the first 500 not read].`, then each bad spot: `line 7: (x,y,z) on Trammel: water` (50 listed). The file is x,y[,z][,map] lines (the map argument is the default), a spawner .json (location and map from each spawner, the spawner's name as the source), or a decoration .cfg (`x y z` lines under their headers; give the map, or `Britannia` for Trammel and Felucca both). Only a path under `Data\` or the map-checks folder, no rooted path, no `..` |
| `[FindStaticProblems` | two corners (max 512x512) | `Checked T tiles, S statics in (x,y) WxH: d duplicates, b buried, u unknown IDs.` then each (50 listed) |
| `[Walkable [list|overlay [seconds]|clear]` | two corners | `T tiles in (x,y) WxH: w walkable, water, impassable land, blocked by statics.` then each blocked tile (30 listed). `overlay` also drops a `ClusterFWalkMarker` (recall rune graphic 0x1F14, hue 0x21, `Name = "blocked: <why>"`, not movable) at the land Z of each blocked tile, up to 2,000, which deletes itself after the seconds given (1 to 600, default 60); refused on live. `clear` deletes every live marker now |
| `[ShoreCheck [stepThreshold]` | two corners | the region line, the coast height buckets, deep water ids, shallow bed ids, shore ids, then each shore-touching water tile (20 listed; the threshold lists only shores at least that many Z above the water) |
| `[ExportPoints <name> [rect|point|clear]` | `rect`: two corners; `point`: one spot, added to that name's list and the file rewritten; `clear`: forgets the list | writes `<world folder>\map-checks\<name>.json`; a name is 1 to 40 letters, digits, - or _ |

The in-game lines are hued: green when nothing is wrong, red when something is, grey for information.

### 3.1 The hook for the stampers and the Argonious buildings

The check is one static call with no command around it:

    var r = ClusterFMapCheck.CheckFootprint(new ClusterFMapTileSource(map), x, y, width, height, maxZSpread);
    if (!r.CanPlace) { foreach (var line in r.Lines()) from.SendMessage(0x22, line); return; }

**Not wired now, and I advise against wiring it into `[StampLayout` and `[VBuild` as they are:** both place furniture
and decoration *inside* buildings, on floors between walls, and the footprint rule treats every impassable
non-surface static within 16 Z (every wall, every door frame) as a blocker, so a legitimate indoor stamp of a captured
room would be refused. The rule is for a building's ground footprint, which is what the Argonious `.uoa` designs
(`D:\UO\third-party\argonious-buildings\`, UO Architect) need: when their importer is written, call `CheckFootprint`
over the design's bounds before placing, and refuse or warn on CANNOT. `[StampLayout check <name>` already exists as the
dry run; a `check` that also ran `CheckFootprint` and only *reported* (not refused) would be a two-line change in
`ClusterFLayoutCapture.OnStamp`. Your call (open question 1).

## 4. Facts, red then green (Part A)

The gate's host has no client files (`TestServerInitializer.cs:34-39`; the builder image copies none), and a real
`Map` returns its invalid block while its stream is null whatever is stored in it (`TileMatrix.cs:293-297`), so the
facts run every check over `FakeTiles`, an `IClusterFTileSource` built in the test with its own land, statics and
flag tables. The region (32x32, grass Z 0 unless said) is drawn in the file header: a water land tile, an impassable
land tile, an impassable static at Z 0, one at Z 20 (above the stand height), a table (Impassable and Surface), a
static below the land, one at exactly Z 16, a slope (Z 0, 3, 6, 7), two identical rugs plus one at another Z, a static
10 below the land and one 9 below, an id with no tiledata, a 4x4 water block at Z -5, a shallow bed (grass at Z -3
under a Wet static), and a water tile at Z -125.

Each fact was made red by breaking `ClusterFMapCheck.cs` in exactly the way the fact exists to catch, through the real
gate (`docker/uo/build.sh --tests-only -t sl-modernuo:cc-p135`), in two rounds of several breaks at once (each break
aimed at a different fact, so each red names its break), with the file restored and proved byte-identical
(SHA-256 `98e8546b...` before and after both rounds). Logs: `notes\cc-P135-tools\build5-red1-tests.txt` and
`build6-red2-tests.txt` (the test sections of the two gate runs, with each failure's message).
Baseline before the rounds: 1,397 passed, 1 red (a wrong indent in my own
expectation of the Walkable lines, fixed), 4 skipped (the real-data facts).

| Break (how it was made red) | Fact that went red, and what it said |
|---|---|
| B1 a Surface static (a table) blocks too | `AStaticAboveStandHeightBelowTheLandOrASurfaceDoesNotBlockAndOneAtTheEdgeDoes` (the table at (6,2) listed); and `WalkableCountsEachCause...` (5 walkable, not 6) |
| B2 a spread equal to the limit is refused (`<` for `<=`) | `TheZSpreadIsMeasuredAndRefusedPastTheLimit`: "a spread of 7 is allowed when the limit is 7" |
| B3 a tile is read before the footprint is refused | `AFootprintOverSixtyFourOrOffTheMapIsRefusedBeforeReading`: Reads 5, not 0 |
| B4 the 500-spot cap is not applied | `SpotLinesParseWithOptionalZAndMap...FirstFiveHundredAreRead`: 503 spots, not 500 |
| B5 a spawner with no map does not get the default | `ASpawnerJsonAndADecorationCfgGiveSpots`: map null, not Malas |
| B6 a spot off the map is not caught | `ValidationNamesAnUnknownMapASpotOffTheMap...`: IndexOutOfRange from the fake (the real adapter would read the invalid block) |
| B7 a duplicate is the same id at any Z | `StaticProblemsAreDuplicatesBuriedAndUnknownIds...`: 2 duplicates, not 1 |
| B9 markers are not hued | `MarkersAreRedNamedForTheCause...`: hue 0, not 33 |
| B10 a shallow bed is not water | `ShoreFindsWaterTouchingLandShallowBeds...`: 16 water tiles, not 17 |
| B11 the rectangle is written with inclusive x2,y2 | `ExportedPointsAndRectanglesReadBack...`: (100,200,109,203), not (100,200,110,204) |
| B12 `..` is allowed in a file path | `ADataFileIsReadOnlyUnderTheGivenRoots...`: "no .." not said (the file was simply not found) |
| B8 buried only when strictly more than 10 below | `StaticProblemsAreDuplicatesBuriedAndUnknownIds...`: 0 buried, not 1 (the static at exactly -10) |
| B13 the overlay is allowed on live | `WalkableCountsEachCause...TheOverlayIsTestShardOnly`: the refusal is null, "test shard only" not said |
| B15 the water surface limit is the hard limit 127 | `ShoreFindsWaterTouchingLand...OnlyASurfaceOutsideTheLimitIsAFault`: 0 problems, not 1 (Z -125 passed) |
| B16 a third token that is not a number is a bad line, never a map | `SpotLinesParseWithOptionalZAndMap...`: 3 spots, not 4 ("13,23,Malas" dropped) |
| B19 a decoration entry gives a spot for the first map only | `ASpawnerJsonAndADecorationCfgGiveSpots`: 3 spots, not 6 (Felucca missing) |

`AFlatGrassFootprintCanBePlacedAndEachBlockerSaysWhy` had no break of its own: B1 and B6 cover its two halves (the
blocked rule, the footprint over it), and it went red in my first run of all for a reason of my own, which is the
same evidence (the expectation had the wrong text; the fact found it).

**Found in passing, not mine:** in the round 1 run `LootBoxFanfareVerification.ContentsAreRolledAtEarnAndOpeningHandsOverExactlyThoseThenTheBoxIsGone`
went red too: the roll was `12000 gold, 200 Renown, 60 x Iron Ore, 5 x Sapphire, 7 x Lesser Heal Potion, 5 x Sapphire,
War Hammer`, two stacks of the same gem, and `Assert.False(item.Deleted)` at `:212` fails when the second stack merges
into the first on hand-over. It passed in every other run. A random roll that can give two stacks of one stackable
is a flaky fact, not a loot bug; worth a `Stackable` guard in the fact or a distinct-type roll (open question 4).

## 5. The real maps: the adapter, the twelve spawn files, every decoration file, New Haven

**How it was run.** The gate's test host has no client files, so the same facts were run once more, by hand, in the
builder image `build.sh` had just built (`sl-uo-builder:cc-p135`, the one whose tests the gate ran), with the client
folder mounted read-only and the two switches the fixture and the facts read:

    docker run --rm --network=none --security-opt seccomp=unconfined \
      -v D:/ShatteredLegacy/client-data/classic-client-7.0.117.0:/clientdata:ro -v <scratch>:/report \
      -e MODERNUO_TEST_DATA_DIR=/clientdata -e SL_MAPCHECK_REPORT_DIR=/report -w /build/modernuo \
      sl-uo-builder:cc-p135 dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore \
      --filter "FullyQualifiedName~ShatteredLegacy.Tests.MapCheck" --logger "console;verbosity=detailed"

Nothing was built; `TileDataLoaded` came up true; **17 of 17 passed** (the 13 region facts and the 4 real-data ones).
The reports it wrote are `notes\cc-P135-tools\realdata-spawns.txt`, `realdata-decoration.txt` (every file, 40 problems
listed per file), `realdata-new-haven.txt`, and the run itself `realdata-run.txt`.

### 5.1 The adapter against cc-P134's independent read

`TheRealAdapterReadsNewHavenAsTheIndependentUopReadDid`: Trammel 3503,2574 is land 0x03E9 at Z 14 with no statics,
and 3503,2573 holds statics 0x0B24 and 0x0D33 at Z 14, exactly what cc-P134 read from `map1LegacyMUL.uop` by name
hash and from `statics1.mul` (its section 4), and what the fixed vseUOAware answers. The flags come from the real
tiledata: 0x00A8 is Wet, 0x0003 is open, 0x0080 is Impassable with an entry. So `Map.Tiles` and `TileData`, read the
way `Map.CanFit` reads them, agree with two independent readers on these tiles.

### 5.2 The same New Haven box through vseUOAware's own tools (the cc-P134 MCP server, same tiledata, facet 1)

| Check, Trammel (3400,2400) 300x300 | this port, in the test host | vseUOAware (`check_walkability`, `find_static_problems`, `find_deep_water_near_shore`, `check_house_placement`) |
|---|---|---|
| walkable / water / impassable land / blocked by statics | 62,806 / 14,747 / 7,308 / 5,139 of 90,000 | 62,806 / 14,747 / 7,308 / 5,139 |
| statics / duplicates / buried / unknown ids | 44,497 / 0 / 153 / **3** | 44,497 / 0 / 153 / **0** |
| water tiles / shore-touching / surface faults | 20,719 / 802 / 0 | 20,719 / 802 / 0 |
| coast buckets (below, level, 1-4, 5, 6-9, 10-24, 25+) | 16 / 34 / 196 / 244 / 221 / 91 / 0 | the same |
| deep water ids | 0x00A8 x3947, 0x00A9 x3558, 0x00AA x3628, 0x00AB x3614 | 168 x3947, 169 x3558, 170 x3628, 171 x3614 |
| footprint (3503,2574) 8x8 | CANNOT, 8 blocked (0x11CB/0x11CC/0x2FF6 at Z 20, 0x0B24 at Z 14, 0x11CA at Z 16), land Z 14..14 | the same eight tiles |

Every number agrees except **unknown ids**, which is a definition, not a bug: vseUOAware counts an id as known when
the tiledata file has an entry for it, and a 7.0.9.0+ file has one for every 16-bit id, so it can never say unknown;
this port calls an entry with no name, no flags and no height "no tiledata entry", and three New Haven statics have
one: 0x2821 at (3512,2414), 0x365E and 0x365F at (3551,2455) and (3551,2456). Those are drawn by the client and are
nothing to the server's rules. Keep the stricter reading, or match his (open question 6)?

### 5.3 `[ValidateSpots` over the twelve world-setup spawn files

`ValidateSpotsOverThePinnedSpawnFiles`, `notes\cc-P135-tools\realdata-spawns.txt`: **387 spawner locations, 18 with
problems**, by file:

| File | Spots | Problems |
|---|---|---|
| post-uoml/termur/Abyss.json | 22 | 0 |
| post-uoml/termur/TerMur.json | 65 | 9: two blocked by static 0x21A3 (1109,3744,-34 and 668,3831,-31), three on water (1099,3010,50; 1053,2971,50; 1062,3026,50), four on impassable land 0x022C..0x022F (762,3073,105; 839,3086,83; 817,2960,76; 354,3283,57) |
| post-uoml/termur/Underworld.json | 44 | 4: impassable land 0x00E3 at 1058,1135,-37; water at 1064,1106,-65, 1187,1186,-40, 1208,984,-1 |
| shared/malas/Citadel.json, Labyrinth.json | 15, 17 | 0, 0 |
| shared/trammel and felucca/Sanctuary.json | 8, 8 | 0, 0 |
| shared/trammel and felucca/PrismOfLight.json | 21, 21 | 1 each: spawner 8 / 21 at (6576,91,0), water (the same spot on both facets) |
| post-uoml/trammel/Vendors.json | 95 | 3: (3504,2612,0), (3520,2598,0), (3555,2698,5), all "water" |
| post-uoml/felucca/Vendors.json | 34 | 0 |
| post-uoml/trammel/Outdoors.json | 37 | 0 |

**Read the three New Haven vendors before acting on any of these.** They are the dock vendors, and the docks are
planks (Surface statics) laid over Wet land. The rule, his and now ours, says "water" for Wet land before it looks at
statics, so a plank over water, a bridge, a floor laid over rock, each reads as blocked. `Map.CanFit` would let a
mobile stand on the plank. The same caveat applies to a spawner in TerMur or the Underworld on a walkway over water
or rock. So the 18 are places to look at, not 18 defects; nothing was changed (the brief: do not fix data). Open
question 6 asks whether the rule should let a non-Impassable Surface static within the stand height make a tile
standable, which would be a deliberate step past vseUOAware's heuristic.

### 5.4 `[ValidateSpots` over every decoration file pinned's `[Decorate` reads

`ValidateSpotsOverThePinnedDecorationFiles`, `notes\cc-P135-tools\realdata-decoration.txt`: the 71 .cfg files under
`Data\Decoration\{Britannia, Trammel, Felucca, Ilshenar, Malas, Tokuno}`, a Britannia entry counted once per facet as
`[Decorate` places it: **55,538 spots, 6,222 "problems": blocked by a static 1,029, impassable land 4,916, water 277.**
For decoration that total is a map of which spots are not floor, not a list of defects: a decoration stands where it
stands, on a cave's rock (`_orccave.cfg`: 2,280 of 5,284, almost all impassable land), against a wall, on a pier over
water. The files with the most: `_orccave` 2,280, `magincia` 358, `jhelom` 352, `skara` 268, `vesper` 200,
`patches` 158 of 236, `nujelm` 146, `moonglow` 144, `_covetous` 141, `_shame` 86; New Haven's own `haven.cfg` 16 of
181 and `_haven additions.cfg` 56 of 433. The per-file lines are in the report. What the run does prove is the
command's reach: every file parsed (0 lines not understood), every map resolved, 55 thousand spots in 4 seconds.

### 5.5 New Haven's statics, walkability, shore and one footprint

`NewHavenStaticsWalkabilityAndShore`, `notes\cc-P135-tools\realdata-new-haven.txt`, the numbers in 5.2. Of the 153
buried statics, 22 are 0x0045 at Z -88 under sea bed at Z -5 (a sunken line of tiles along the coast at
3446..3450 and 3602..3609), 17 are a row of 0x07A3 at Z 56 under land at Z 66 along x 3464..3479 at y 2498 (something
under the hill), and the rest are single tiles 10 to 21 Z under the land. 0 duplicates. The shore: 802 water tiles
touch land, most 1 to 9 Z above the water, no cliff over 25, no surface fault. The footprint at the bank's spot
(3503,2574) CANNOT be placed for the eight wall and door tiles listed; the land is flat (Z 14 throughout).

## 6. Part D: where it lives, and why the console won

**The argument.** The console tab wins over a standalone tool because (a) the four art checks are seconds-long,
read-only command lines whose output is a table to read, which is exactly what the console's Action output pane
(cc-P84) and plan model already do for `Check-Docker.ps1` and the package gates: a `-DryRun` prints the one `RUN python
...` line that runs, `Test-PlanSafety` can refuse anything else, and the run file lands in
`scripts\shard-console-output\`; (b) the in-game commands cannot be run by any PC tool (the console says so of the World
setup tab too), so their "home" on a PC is a place that prints the syntax where staff already look; and (c) a second
GUI would duplicate the console's dry run, safety check, tooltips, facts and theme for four buttons. cc-P134's input
(validate-art stays a CLI; the MCP server belongs in no GUI) stands: the tab runs the CLI as it is and the MCP server
is untouched. What a standalone tool would have bought, a long-lived window with the body table in a grid, is not
worth a second code base; the pane and the run file hold the table.

**Where the output goes.** The brief says "output in the tab". Since cc-P84 every run's output goes to the one Action
output pane under the tabs (or a window of its own when the pane is busy or the setting says windows), and I kept
that rather than build a second pane inside the tab: one place to read, Copy, Clear and Stop, and the P84 facts
hold. Deviation noted.

**What the tab is** (`Map and Art`, right after World setup):
- a caption, then a `.vd` box with Browse and a body box, then a `hues.mul` box with Browse;
- **Check the art registry** (`validate-art.py check-registry`), **Body table** (`bodies`), **Check a .vd** (`check-vd
  <file> <body>`, or `propose <file>` when the body box is empty), **Compare a hues.mul with ours** (`hues-diff <ours>
  <theirs>`, ours being `client-data\classic-client-7.0.117.0\hues.mul`). All `RunIn = 'window'`, `Mutates = $false`,
  so they stream into the pane and run with no `-Mode` (Resolve-RunMode: a read-only action needs none);
- six **map command** buttons, `RunIn = 'here'`: each prints the usage, what the command says, and that the console
  cannot run it.
- **Exit 1 is "found problems", not "failed".** `validate-art.py` exits 1 when a check finds something. A plan step may
  now carry `-Named @{ ReportExit = 1 }`: `Invoke-Plan` says `exited with 1: it found something; read the lines above.
  Not a failure.` in amber and the run is done; any other non-zero exit fails as before, and a step without the name
  fails on 1 as before.
- **Safety.** `Test-PlanSafety` has a new rule: a step whose exe is python (any `python`, `python3`, `pythonX.Y`,
  `.exe` or not, any folder) or that names `validate-art.py` anywhere must be an `exec` step of `python
  <scripts\validate-art.py> <bodies|check-registry|check-vd|propose|hues-diff> ...` with no `--out`. So `render` (the
  one subcommand that writes PNGs), `actions`, another script, `python -c`, `python -m`, `cmd /c python ...` and a
  `window` step are all refused.
- **Headless:** `-Action art.registry|art.bodies`, `-Action art.checkvd -VdFile <path> [-Body <n>]`, `-Action art.hues
  -HuesFile <path>`, `-Action map.<footprint|spots|statics|walkable|shore|export>`; `-DryRun` prints the plan. The child
  line a click builds carries `-VdFile "<path>"`, `-Body <digits only>` and `-HuesFile "<path>"`, quotes in a path
  dropped. The banner says `MAP AND ART  <action> (map and art)`.
- Config: `ValidateArt`, `Python`, `OurHues`, `ArtSubcommands` in `Get-ConsoleConfig`. Tooltips for every button, box
  and the tab (`Get-ConsoleTooltips`; the P84 tooltip facts still pass: 265 controls).

Section 4 of `notes\shard-console.md` is the `-DryRun` transcript of every button. The new buttons' transcripts, from
`Shard-Console.ps1 -DryRun -Action <key> ...` on this PC:

```
== DRY RUN: art.registry (mapart) ====================================================
  1. SAY      Check the art registry: rows registered twice, art ids with EA art in the slot, anim rows mobtypes names or records.json does not route, body rows with no mobtypes entry.
  2. RUN      python D:\ShatteredLegacy\scripts\validate-art.py check-registry
         # validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.
   (dry run: nothing was run)

== DRY RUN: art.bodies (mapart) ======================================================
  1. SAY      The body table: every body the client data names or draws (about 1,300 lines): type, flags, classic or UOP, file, slot, layout, the actions it has frames for, and which line defines it. Copy from the pane, or read the run file in scripts\shard-console-output.
  2. RUN      python D:\ShatteredLegacy\scripts\validate-art.py bodies
         # validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.
   (dry run: nothing was run)

== DRY RUN: art.checkvd (mapart) =====================================================
  1. SAY      Check Kirin.vd against body 2052: its layout and actions, whether the body is free, where it lands, whether the layout fits, and what mobtypes must say.
  2. RUN      python D:\ShatteredLegacy\scripts\validate-art.py check-vd D:\UO\third-party\kirin\Kirin.vd 2052
         # validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.
   (dry run: nothing was run)

== DRY RUN: art.checkvd (mapart) =====================================================
  1. SAY      No body given, so propose one: a free server body (from 0x800) and a free anim7 slot of the right layout for Kirin.vd, then the check on it. Registers nothing.
  2. RUN      python D:\ShatteredLegacy\scripts\validate-art.py propose D:\UO\third-party\kirin\Kirin.vd
         # validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.
   (dry run: nothing was run)

== DRY RUN: art.hues (mapart) ========================================================
  1. SAY      Compare D:\UO\third-party\argonious-buildings\hues.mul with ours (D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\hues.mul): the hues whose colours differ, and those that differ only in name or table range. Report only; neither file is changed.
  2. RUN      python D:\ShatteredLegacy\scripts\validate-art.py hues-diff D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\hues.mul D:\UO\third-party\argonious-buildings\hues.mul
         # validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.
   (dry run: nothing was run)

== DRY RUN: map.footprint (mapart) ===================================================
  1. SAY      [CheckFootprint <width> <height> [maxZSpread=5]   (GameMaster; then target the top-left corner)
  2. SAY      CAN or CANNOT a w x h building stand there: the blocked tiles (water, impassable land, an impassable non-surface static within 16 Z) and the land Z spread. Max 64x64.
  3. SAY      Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.
   (dry run: nothing was run)

== DRY RUN: map.spots (mapart) =======================================================
  1. SAY      [ValidateSpots <file under Data> [map]   (GameMaster; no target)
  2. SAY      Names each bad spot in a spawn .json, a decoration .cfg (give the map, or Britannia for both) or x,y[,z][,map] lines; at most 500 a file. The full report goes to the map-checks folder beside the saves.
  3. SAY      Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.
   (dry run: nothing was run)

== DRY RUN: map.statics (mapart) =====================================================
  1. SAY      [FindStaticProblems   (GameMaster; then target two corners (max 512x512))
  2. SAY      Duplicate statics (the same id and Z on a tile), statics buried 10 or more Z under the land, and ids with no tiledata entry.
  3. SAY      Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.
   (dry run: nothing was run)

== DRY RUN: map.walkable (mapart) ====================================================
  1. SAY      [Walkable [list|overlay [seconds]|clear]   (GameMaster; then target two corners (max 512x512))
  2. SAY      The tiles a mobile cannot stand on, by cause. overlay marks each with a red rune that deletes itself (default 60 s, max 600; test shard only); clear removes every marker now.
  3. SAY      Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.
   (dry run: nothing was run)

== DRY RUN: map.shore (mapart) =======================================================
  1. SAY      [ShoreCheck [stepThreshold]   (GameMaster; then target two corners (max 512x512))
  2. SAY      Water touching non-water land: coast heights in buckets, the water and shore tile ids, and any water surface outside -120..120.
  3. SAY      Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.
   (dry run: nothing was run)

== DRY RUN: map.export (mapart) ======================================================
  1. SAY      [ExportPoints <name> [rect|point|clear]   (GameMaster; rect: two corners; point: one spot at a time)
  2. SAY      Writes the rectangle (spawnBounds and its centre) or the points as spawn-file JSON to <world folder>\map-checks\<name>.json. [ValidateSpots <name>.json reads it back.
  3. SAY      Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.
   (dry run: nothing was run)
```

And three of them run for real on this PC, through the same headless path a click uses (`-Mode Execute`; a read-only action also runs with no mode at all, as `map.shore` shows at the end), from `notes\cc-P135-tools\console-transcripts.txt`:

```
=== REAL RUN: -Mode Execute -Action art.registry
==============================================================================
  MAP AND ART  art.registry (map and art)
  Runs scripts\validate-art.py, which reads the client data and writes nothing, or prints a command's syntax. No shard is touched.
==============================================================================
== PLAN: art.registry (mapart) ====================================================
  1. SAY      Check the art registry: rows registered twice, art ids with EA art in the slot, anim rows mobtypes names or records.json does not route, body rows with no mobtypes entry.
  2. RUN      python D:\ShatteredLegacy\scripts\validate-art.py check-registry
         # validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.

[1/2] Check the art registry: rows registered twice, art ids with EA art in the slot, anim rows mobtypes names or records.json does not route, body rows with no mobtypes entry.
[2/2] validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.
      > python D:\ShatteredLegacy\scripts\validate-art.py check-registry
   ... 112 registry rows, each ": ok" ...
0 of 112 rows have problems
art.registry: done.
exit 0

=== REAL RUN: -Mode Execute -Action art.checkvd -VdFile D:\UO\third-party\kirin\Kirin.vd -Body 2052
==============================================================================
  MAP AND ART  art.checkvd (map and art)
  Runs scripts\validate-art.py, which reads the client data and writes nothing, or prints a command's syntax. No shard is touched.
==============================================================================
== PLAN: art.checkvd (mapart) =====================================================
  1. SAY      Check Kirin.vd against body 2052: its layout and actions, whether the body is free, where it lands, whether the layout fits, and what mobtypes must say.
  2. RUN      python D:\ShatteredLegacy\scripts\validate-art.py check-vd D:\UO\third-party\kirin\Kirin.vd 2052
         # validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.

[1/2] Check Kirin.vd against body 2052: its layout and actions, whether the body is free, where it lands, whether the layout fits, and what mobtypes must say.
[2/2] validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.
      > python D:\ShatteredLegacy\scripts\validate-art.py check-vd D:\UO\third-party\kirin\Kirin.vd 2052
D:\UO\third-party\kirin\Kirin.vd: high layout, 110 records, 65 with frames, actions 0-12
lands: anim slot 2052, read as HUMAN (people layout, 35 actions) at records 324100-324274
mobtypes: needs "2052 MONSTER 0"
note: only actions 0-12: a monster, or an animal (a mount) cut into a high block, as the kirin. An animal needs ANIMAL 0, and the client then reads a low block (13 actions) at the slot low-layout offset, so the frames must be written there, not at slot x 110. Render it to tell.
note: has action 8; if that is a hover idle the body needs flag 0x4 (IdleAt8Frame)
PROBLEM layout: the .vd is a high block but the client reads a people block here
verdict: 1 problem(s)
      exited with 1: it found something; read the lines above. Not a failure.
art.checkvd: done.
exit 0

=== REAL RUN: -Mode Execute -Action art.hues -HuesFile D:\UO\third-party\argonious-buildings\hues.mul
==============================================================================
  MAP AND ART  art.hues (map and art)
  Runs scripts\validate-art.py, which reads the client data and writes nothing, or prints a command's syntax. No shard is touched.
==============================================================================
== PLAN: art.hues (mapart) ========================================================
  1. SAY      Compare D:\UO\third-party\argonious-buildings\hues.mul with ours (D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\hues.mul): the hues whose colours differ, and those that differ only in name or table range. Report only; neither file is changed.
  2. RUN      python D:\ShatteredLegacy\scripts\validate-art.py hues-diff D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\hues.mul D:\UO\third-party\argonious-buildings\hues.mul
         # validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.

[1/2] Compare D:\UO\third-party\argonious-buildings\hues.mul with ours (D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\hues.mul): the hues whose colours differ, and those that differ only in name or table range. Report only; neither file is changed.
[2/2] validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.
      > python D:\ShatteredLegacy\scripts\validate-art.py hues-diff D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\hues.mul D:\UO\third-party\argonious-buildings\hues.mul
D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\hues.mul: 265500 bytes, 3000 hues
D:\UO\third-party\argonious-buildings\hues.mul: 265500 bytes, 3000 hues
   ... 40 lines not quoted ...
  hue 1259 (0x4EB): 32 of 32 colours; table 15360-32513 -> 54016-54272; name "FireWeap5" -> ""
  hue 1260 (0x4EC): 32 of 32 colours; table 19648-33737 -> 65280-33792; name "FireWeap6" -> "???'-(-I1I5j9?=?=?I?"
  hue 1261 (0x4ED): 32 of 32 colours; table 231-1071 -> 45418-45674; name "ColdWeap1" -> "n?{6?y???????'9?A?E?"
  ... 1322 more (raise --limit)
art.hues: done.
exit 0

=== -Action map.shore with no -Mode (a read-only action runs)
==============================================================================
  MAP AND ART  map.shore (map and art)
  Runs scripts\validate-art.py, which reads the client data and writes nothing, or prints a command's syntax. No shard is touched.
==============================================================================
== PLAN: map.shore (mapart) =======================================================
  1. SAY      [ShoreCheck [stepThreshold]   (GameMaster; then target two corners (max 512x512))
  2. SAY      Water touching non-water land: coast heights in buckets, the water and shore tile ids, and any water surface outside -120..120.
  3. SAY      Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.

[1/3] [ShoreCheck [stepThreshold]   (GameMaster; then target two corners (max 512x512))
[2/3] Water touching non-water land: coast heights in buckets, the water and shore tile ids, and any water surface outside -120..120.
[3/3] Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.
map.shore: done.
exit 0
```


## 7. Console facts, red then green

The 8 `P135_` facts (`scripts	ests\Shard-Console.Tests.ps1`), plus the tab-list fact `TheFormBuildsFromACaptureWithoutBeingShown`
which now names `Map and Art` after `World setup`, and the click harness (`Invoke-ClickCapture`), which hands a .vd and a
hues.mul to the two buttons that need one, as it hands notes and a zip to the package buttons. What they cover:

| Fact | What it pins |
|---|---|
| `P135_TheFourArtChecksRunOnlyValidateArtReadOnlyAndReportExitOne` | each art plan is one `exec` of `python validate-art.py <subcommand>`, no confirm, no log, no window; a body gives `check-vd <file> <body>`, none gives `propose <file>`; hues-diff takes ours first; every plan passes the safety check |
| `P135_CheckVdAndHuesRefuseAMissingWrongOrOwnFileAndANonNumericBody` | no file, a missing file, the wrong kind of file, a hex or word body, and ours-against-ours are refused, and a refused plan runs nothing |
| `P135_TheSafetyCheckRefusesPythonOutsideValidateArtAndRenderOrAnyOtherSubcommand` | `render`, another script, `python -c`, `python3.exe -m`, a `window` step, `cmd /c python`, an unlisted subcommand and `--out` are refused; the five listed subcommands pass; `render` is not among them |
| `P135_EveryMapButtonPrintsItsCommandsSyntaxAndRunsNothing` | six buttons, three `say` steps each; the usage printed is the `[Usage]` the command declares in `ClusterFMapCheckCommands.cs`, and each command is registered GameMaster there; a click prints here and opens no window |
| `P135_TheChildLineCarriesTheVdFileBodyAndHuesFileAndOnlyDigitsForTheBody` | `-VdFile "<path>"`, `-Body <digits>` (a quote in a path dropped, a non-digit body not crossing), `-HuesFile "<path>"`; a dry click opens one window carrying them; no file, no window, the refusal said |
| `P135_AReportedExitCodeIsSaidInAmberAndTheRunIsDoneAnyOtherFails` | a step with `ReportExit = 1` exiting 1 is done and said in amber with its output shown; exit 2 fails; exit 1 with nothing declared fails as before (a throwaway script, never validate-art) |
| `P135_TheTabIsBuiltWithItsBoxesButtonsAndTooltips` | the page, right after World setup; the ten buttons' keys and labels; the three boxes by name and trimmed; two Browse buttons; a tooltip for every key, box and the tab |
| `P135_EveryMapAndArtButtonRunHeadlessWithDryRunRunsNothing` | the real child, `powershell -File Shard-Console.ps1 -DryRun -Action <key> ...`, for eight cases: exit 0, `== DRY RUN: <key> (mapart)`, nothing run, no REFUSE, the RUN line names python; and `-Action map.shore` with no mode runs and prints `[ShoreCheck [stepThreshold]` |

**Each watched failing**, one break at a time in the real `Shard-Console.ps1`, the facts run with
`SL_FACT_FILTER=P135_|TheFormBuildsFromACapture`, the file restored and checked byte-identical by SHA-256
(`notes\cc-P135-tools\redfirst_console.py`; the run, `redfirst-console.txt`):

| Broken | Red |
|---|---|
| C1 the safety check lets any validate-art subcommand through (render included) | the safety fact ("a subcommand not listed") |
| C2 a reported exit code is not reported: exit 1 fails the run | the exit-code fact ("the reported exit is done") |
| C3 the child line drops `-Body` | the child-line fact (the line shows `-VdFile` and no `-Body`) |
| C4 Check a .vd with no body runs check-vd anyway | the plans fact ("no body: propose one") and the headless fact (`art.checkvd` without a body is REFUSED) |
| C5 a map button no longer says the console cannot run the command | the map fact (`say,say`, not `say,say,say`) |
| C6 the tab is added after Diagnostics | the tab-list fact and the tab fact ("right after World setup": 6, not 5) |
| C7 the headless entry does not name the family (`$sk` stays test) | the headless fact (the banner reads `(test)`, not `(mapart)`) |

Baseline 9 of 9 green, every break 1 or 2 red as above, 9 of 9 green after the last restore, hash identical. The whole
console suite: 376 facts, 370 passed, 6 failed, and the six are not this task's. Each fails the same way against the pre-patch
`Shard-Console.ps1` and `Shard-Console.Tests.ps1` (swapped in from copies taken before the patch, the six run, both
restored and proved byte-identical): `P83_TheLinksOpenTheTwoPagesAndNothingElse` and
`P107_LinksAndSitesPointAtHavenAfterTheCutoverAndAtThisPcBefore` (`scripts\haven-ops.json` says the ops pages are on
Haven now, and the facts expect this PC), `P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo` and
`P101_TheTileAndTheTabAreBuiltAndDrawn` (the real `testing\play-tests.json` reads `1 FAIL NOT LOGGED` and Play tests is
a Haven site now), `P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing` (`web.redeploy` on the Play tests site
refuses, because that site is on Haven now), and `P84_TheUOLookAddsUnderASecondToTheStart` (the UO look added 1.25 to
1.41 s on this PC tonight, against a 1 s budget). The first five are the cc-P107 cutover's state; the facts that pin
"before the cutover" need the mode file pinned the way `Get-ConsoleConfig` pins live. Not changed here: they are
cc-P107's facts and cc-P107's state, and a note for Chase (open question 7)..


## 8. Build record and the Golem's view

Every build was `docker/uo/build.sh` from Git Bash, tag `sl-modernuo:cc-p135` (builder `sl-uo-builder:cc-p135`);
`--tests-only` for the iterations, the full three steps at the end. Logs in the scratchpad; the test sections of the
red rounds are in `notes\cc-P135-tools\`.

| Run | Result |
|---|---|
| 1, 2 | the builder stage failed: two compile errors in my test file (an `Assert.Equal` overload picked up a collection expression; a message argument on an `Assert.Equal`). The two StaffHub files compiled. |
| 3 | 1,402 tests: 1,397 passed, 1 failed (my Walkable expectation lacked the two-space indent the report lines carry; the code was right, the fact fixed), 4 skipped (the real-data facts, no tile data in the gate) |
| 4 | round 1 of the breaks: the builder stage failed, because break B10 left a local function unused and pinned treats warnings as errors (`Directory.Build.props`, `TreatWarningsAsErrors`); the break was reworded, nothing else changed |
| 5 | round 1 red: 1,385 passed, 13 failed: the 12 MapCheck facts the breaks aimed at, and the loot box fact (section 4, not mine) |
| 6 | round 2 red: 1,393 passed, 5 failed: the five MapCheck facts the breaks aimed at |
| 7 | the full build: 1,396 passed, 2 failed, both unrelated and green in every other run of this session: `WispOrbPossessionVerification.APossessedCreatureFightingNeverBecomesItsMastersCombatant(petName: "Sagittarri", foeName: "Phantom")` and `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies`. No image was built, by the gate's rule |
| 8 | the full build again, unchanged code: **1,398 passed, 0 failed, 4 skipped. `[tests] 1398 test(s) passed.` Image `sl-modernuo:cc-p135` (a1a03628f924, 1.29 GB) built, labelled `sl.commit=88b6f1b9 sl.dirty=1`** (dirty because this work is uncommitted; Chase commits) |

The real-data run (section 5) was a `docker run` of run 8's builder image, not a build.

**Found in passing, not mine, for the bug list:** three facts that pass or fail on a roll, each seen red once in eight
runs here and green in the other seven: the loot box one (two stacks of the same gem merge on hand-over, section 4), the
wisp orb one (which pet and foe names it drew are in the failure line), and the raised garden one. None reads the map or
touches anything this task added; a flaky gate fails a build by chance about once in four full runs tonight.

**Not done:** the commands were not typed in a client. The facts and the real-data run exercise the checks and the
adapter over the real maps; the targets and bounding boxes are the pinned ones every other command here uses
(`BoundingBoxPicker`, `Target(-1, true, TargetFlags.None)`), unexercised by a test host that has no client. A pass on the
test shard is Chase's: deploy `sl-modernuo:cc-p135` to test (Shard Console > Test shard > Deploy built image) and run
the checklist in section 11.

## 9. Deviations and decisions for Chase

- **ValidateSpots reads three shapes, not one.** The brief says `x,y[,z][,map]` lines; I added the spawner .json and
  the decoration .cfg as inputs, because "point it at our real spawner and decoration data" otherwise needs a converter
  nobody has, and because `[ExportPoints` writes the spawner shape, which closes the loop. The 500 cap holds for all
  three in the command; the real-data facts lift it (a parameter) to read whole files.
- **Two readable roots, not one.** "A file under the server data folder" is `Core.BaseDirectory\Data` (where the
  spawn and decoration files are, read-only in the image) **and** the map-checks folder beside the saves (where
  `[ExportPoints` writes, so its files can be validated). Rooted paths and `..` are refused in both.
- **Walkable's overlay is a Diagnostic command that places items.** Declared Diagnostic because the markers are
  temporary by construction (timer, no persistence, test shard only); a WorldSetup declaration would put it on the
  World setup tab among seeders, which is the wrong place. If you would rather the overlay were its own TestOnly
  command, it is a split of one handler.
- **The output goes to the Action output pane, not a pane inside the tab** (section 6).
- **The real-data run was done by hand in the builder image** (section 5): the gate's test host has no client files
  by design, so `[ValidateSpots` over the real data ran as the same facts, in the same image `build.sh` built, with the
  client folder mounted read-only and `MODERNUO_TEST_DATA_DIR` set. Nothing was built outside `build.sh`; this was a
  second `docker run` of its test step. If that is too far from "test only through build.sh", say so and I will drop
  the section to "unverified" rather than keep it.
- **Red-first in rounds, not one break per build.** Each gate run is five minutes; two rounds of several breaks, each
  aimed at a different fact, gave every fact its red. The console facts were broken one at a time (seconds each).
- **The pinned commit is d4531cd94**, as AGENTS.md says since cc-P38, not the brief's 7c9215d97.
- The brief's "Part B table for the 10-15 downloads" and "Part C build record and .mcp.json entry" are cc-P134's
  (sections 5 and 7 there); this note does not repeat them.

## 10. Open questions for Chase

1. Wire `CheckFootprint` into `[StampLayout check` as a *report* (not a refusal), or wait for the Argonious importer
   and gate that instead (section 3.1)? My advice: wait; the stamp check would say CANNOT for every indoor room.
2. The map-checks folder (`<world folder>\map-checks\`) is beside the saves, like `layout-captures\`, so it is
   bind-mounted and survives a container recreate. Reports accumulate one file per run; nothing prunes them. Fine, or a
   cap?
3. `[Walkable overlay` on live is refused outright. Would you want it allowed for an Administrator with a short
   timeout, or is "test shard only" right? (The brief said test shard only; I followed it.)
4. The flaky loot box fact (section 4): fix in the fact (skip stackables that merged) or in the roll (no two stacks of
   one type)?
5. The six commands show in the Staff Hub under Diagnostics but not on the console's World setup tab (world-changing
   only, by design). Is the Map and Art tab's syntax panel enough, or should the World setup tab grow a read-only
   "Diagnostics" group too?
6. **Two rule choices the real data put a face on** (section 5): (a) keep "no tiledata entry" as an empty entry (three
   New Haven statics, 0x2821, 0x365E, 0x365F), or match vseUOAware and never report it? (b) should a non-Impassable
   Surface static within the stand height (a dock plank, a bridge, a laid floor) make a Wet or Impassable land tile
   standable? Today the three New Haven dock vendors read "water", as his tool reads them. Making that change is a
   deliberate step past the heuristic the brief asked for, so I left it; it is a few lines and a fact if you want it.
7. Six console facts from cc-P83, cc-P84, cc-P101 and cc-P107 fail on this PC tonight with or without this task's
   change (section 7): five because the ops pages have cut over to Haven and the facts pin "this PC", one because the
   UO look takes over a second to build here. Pin the ops mode in those facts as live is pinned, or retire them?

## 11. For Chase

- **New:** `server\customizations\StaffHub\ClusterFMapCheck.cs`, `ClusterFMapCheckCommands.cs`,
  `server\tests\Misc\MapCheckVerification.cs`, `MapCheckRealDataVerification.cs` (shard repo);
  `notes\cc-P135-tools\` (this repo: the break scripts, the console patch script, the red-first outputs, the console
  transcripts, the real-data reports). **Changed:** `scripts\Shard-Console.ps1`, `scripts\tests\Shard-Console.Tests.ps1`,
  `CHANGELOG.md` (a 2026.10.17.5 section, one Staff line), `VERSION` (2026.10.17.5). `tools\progress.py` was run.
- **Nothing in `D:\UO\third-party\`, `D:\UO\ModernUO-pinned` or `docs\` was touched.** No file over 5 MB (the largest
  new one is the 139 KB decoration report). The image is `sl-modernuo:cc-p135`; `latest` was not moved.
- **To try on the test shard** (deploy `sl-modernuo:cc-p135` first; everything below reads, only the overlay places):
  1. Stand in New Haven as a GameMaster. `[CheckFootprint 8 8` and target the bank's doorstep (around 3503,2574): CANNOT,
     eight wall and door tiles, land Z 14..14. Then target the open field north of town: CAN.
  2. `[ValidateSpots Spawns/post-uoml/trammel/Vendors.json`: 95 spots, 3 problems, the three dock vendors (section 5.3).
     `[ValidateSpots Decoration/Trammel/haven.cfg Trammel`: 181 spots, 16 problems. Both say where the full report is.
  3. `[FindStaticProblems`, two corners round the docks: a few buried 0x17A5/0x17B2 planks at Z -5 under land at 5 to 8
     (3555..3567, 2588..2611).
  4. `[Walkable overlay 90` and two corners round the bank: red runes on the walls and the water, gone after 90 s;
     `[Walkable clear` sooner. The runes are named `blocked: <why>` on hover.
  5. `[ShoreCheck` and two corners along the coast: the coast height buckets and the water ids.
  6. `[ExportPoints haven-test` and two corners, then `[ValidateSpots haven-test.json`: the rectangle's centre is checked,
     and the file is in `Saves\..\map-checks\` beside `layout-captures\`.
  7. `[SL`: the six are under Diagnostics.
  8. Shard Console > Map and Art: Check the art registry (0 of 112 rows have problems), Check a .vd with
     `D:\UO\third-party\kirin\Kirin.vd` and body 2052 (the layout problem cc-P134 found, said in amber as "found
     something"), Compare a hues.mul with `D:\UO\third-party\argonious-buildings\hues.mul`, and each map button.

## 12. Attribution

- `server\customizations\StaffHub\ClusterFMapCheck.cs` and `ClusterFMapCheckCommands.cs`: "Adapted from vseUOAware by
  ghostbyte420, GPL-3.0 (vseUtilities commit e4b1d243 ...)" in each header, with the source files named. Both files
  are GPL-3.0, ModernUO's own license family; the tests and the console change are ours.
- vseUOAware: ghostbyte420 (consultant otimpyre), GPL-3.0, https://github.com/ghostbyte420/vseUtilities, servuo.dev
  resource 2687. Read only; nothing under `D:\UO\third-party\` was changed, built or run, and the zip's binaries were
  not touched. The cc-P134 build at `D:\UO\tools\vseUOAware\` was used through its MCP tools for the cross-check in
  section 5 only.

## 13. Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run twice (the second after
`realdata-run.log` was renamed `.txt`, because `*.log` is git-ignored and the note names it), commits nothing. Neither
repo read BLOCKED. The second run, with this note written up to its last line:

```
=== code  (D:\ShatteredLegacy) ===
  8 file(s) pending:
    CHANGELOG.md
    VERSION
    scripts/Shard-Console.ps1
    scripts/tests/Shard-Console.Tests.ps1
    server/customizations/StaffHub/ClusterFMapCheck.cs
    server/customizations/StaffHub/ClusterFMapCheckCommands.cs
    server/tests/Misc/MapCheckRealDataVerification.cs
    server/tests/Misc/MapCheckVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\shard-migration) ===
  18 file(s) pending: README.md, dashboard.html, testing/SUMMARY.md, testing/play-tests.json (the play-test mirror,
  machine output), tools/progress.json, notes/cc-P135-tools/ (12 files), notes/cc-P135-vseuoaware-staff-commands.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

Largest new file: `notes\cc-P135-tools\realdata-run.txt` at 161 KB; nothing near 5 MB. Images built: `sl-modernuo:cc-p135`
and `sl-uo-builder:cc-p135`, outside both repos.

P135 DONE
