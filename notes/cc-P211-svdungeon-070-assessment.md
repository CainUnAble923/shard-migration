# cc-P211: SVDungeon 0.7.0 as the shard's staff dungeon builder: assessment, no port

Written 2026-10-20 by the Bronze Golem (Fable) on CHASES-TOWER, branch golem/Bronze/P211 of shard-migration (docs
only; nothing in ShatteredLegacy changed, nothing in `D:\UO\third-party` built, run or copied). Prompt:
`cc-prompts/claimed/Bronze/cc-P211-svdungeon-070-assessment.md`. House shape: `D:\UO\third-party\code\PORT-ASSESSMENT.md`
(P93). Engine citations are from `D:\UO\ModernUO-pinned` at d4531cd94 (paths under `Projects\`, "PIN\"); SVDungeon
citations are from `D:\UO\third-party\code\svdungeon-0.7.0\SVDungeon-0.7.0\Scripts\Custom\ScriptVisitor\SVDungeon\`
("SV\"); shard citations from `D:\UO\golems\Bronze\ShatteredLegacy\server\customizations\`. Every count below was made
with `wc` or `grep` over the files; statements marked **(guess)** or **(unverified)** were not.

## Headlines

1. **What it is, measured:** 77 `.cs` files, 12,363 lines (70 files and 11,771 lines without the 7 examples), split
   into an engine with no game types (2,619 lines), three layout strategies (1,665), themes and decorators (897), the
   population stage (2,683, of which 1,638 are the game half) and the ServUO server half (3,841: commands, area check,
   builder, two gumps, state). It builds a dungeon as **dynamic items at runtime**: one stock `Static` wall block per
   wall tile at the land's Z, torches, props, pillars, moongates and stock spawners, all tagged so `[SVDungeonClean`
   removes exactly them. It writes **nothing into map files**, makes **no region**, has **no doors** and keeps **one
   dungeon per shard** (section 1).
2. **The "0 hand-written Serialize" claim is true** (section 2.6): no item or mobile class of its own; the only
   persistence is one side file (`SV\Server\SVDungeonState.cs:130-196`) that becomes a 60-line `GenericPersistence`
   subclass on pinned, the pattern two of our customizations already use.
3. **Port effort: the engine is a copy, the server half is a rewrite of known shape.** Every ServUO API it touches
   has a pinned equivalent (section 2, checked file by file): the legacy `Gump` class survives with mechanical
   signature changes, spawners take a `Rectangle3D` and `SpawnerEntry` rows instead of `SpawnObject` lists,
   `WeakEntityCollection` does not exist and needs a small replacement, the creature scanner leans on three ServUO-only
   members. Sizes: engine S, builder and commands S, gumps S-M, population M, in all **about 2 to 3 weeks of prompts
   (guess)**, and the single-dungeon state would need to become per-instance for League dives.
4. **Fit with Rootdeep (section 3): it neither replaces nor fights the map pipeline; it can feed it.** Rootdeep is
   map statics with OSI wall sets placed by the run-topology rule, dressed corners, framed doorways and a 12-point
   checklist; SVDungeon is full-block walls, lattice pillars and shuffled litter at 3 to 5 pieces per 100 floor tiles.
   As built it fails four playbook rules (wall pieces, frames, variety, torch height) and would never pass the junction
   sheet. What is worth having is its **plan**: the three layout generators, the two validators, `BlockerProof`, the
   per-stage seeded random streams, the room-kind-by-distance rule and the population stage's depth tiers and
   spawn-box fit. A layout export in our `layout.json` shape would hand a generated plan to `build_burrows.py`.
5. **Uses ranked (section 4):** 1. a staff tool for **quick League dives** (temporary, seeded, torn down, entered by
   gate: exactly what dynamic items are for, once the trial maps exist); 2. a **spawn reference** now (the pool file
   format and depth tiers for the dive spawn table); 3. the **Minecraft dungeon** (block walls and square cells are
   what it draws, but the dungeon has no brief anywhere in the repo, and a permanent one belongs in map statics);
   4. the **starter dungeon**: no, the Rootdeep Burrows exist (P36 region, P167 map, P141 spawners).
6. **Recommendation (section 6): borrow now, port later, in two pieces**, and a draft prompt for the first piece
   (engine, builder, commands, population with a hand-written pool; no scanner, no admin gump) to queue once F-24
   dives and the trial maps are on the board. Section 7's playbook additions are written into
   `notes\map-building-playbook.md` (new section 5).

## 1. What 0.7.0 does, stage by stage, measured from the code

### 1.1 The run, from the command to the items

`[SVDungeonGen` or the gump's Generate calls `SVDungeonCommands.Generate` (`SV\Server\SVDungeonCommands.cs:178-304`):

1. Refuses without an anchor (set by `[SVDungeonAnchor`, a corner and a map, `SVDungeonState.cs:53-65`).
2. Checks the theme's ids against tile data: every wall id must be impassable and at least 15 high, floor paving flat
   and walkable, "walkable" decoration kinds passable (`SVDungeonTileset.cs:15-156`).
3. Removes the previous dungeon (`WeakEntityCollection.Delete("svdungeon")`, `SVDungeonBuilder.cs:99-102`): one
   dungeon per shard, always.
4. Scans the footprint plus a 2-tile margin (`SVDungeonCheck.cs:96-222`): land ids, land Z spread (more than 6 refuses),
   static tiles (any refuses), items (any refuses), mobiles other than the admin (any refuses), regions per the
   `RegionCheck` setting (Error refuses, Warning reports, Ignore skips). It never levels ground and never reads Z
   inside the plan: every item lands at its own tile's land Z (`SVDungeonBuilder.cs:67, 88`).
5. Runs the pipeline (`SV\Engine\Pipeline\DungeonPipeline.cs:179-206`): the layout strategy, the theme name, the
   validators in list order (any issue = nothing is built), then the decorators in list order on a passing layout; a
   later decorator loses a tile an earlier one took, torches excepted (`YieldToEarlier`, `:152-177`).
6. Builds (`SVDungeonBuilder.cs:40-96`): for every tile the theme's `Place` returns 0 or more `(id, zOffset)`;
   each becomes `new Static(id)` tagged in `WeakEntityCollection` and moved to `(x, y, landZ + zOffset)`. With
   `WallShellOnly` a wall tile with no walkable neighbour that is not on the border is skipped. Then every planned
   decoration goes through the factory chain of its kind (`SVDungeonItems.cs:49-72`): `static` makes a `Static`,
   `torch` a burning `WallTorch` flipped for north walls at +12 (`TorchFactory.cs:17-34`), `gate` a non-dispellable
   `Moongate` (`GateFactory.cs:22-28`), `spawner` a `Spawner` or `ProximitySpawner` (`SpawnerFactory.cs:97-140`).
7. Records seed, size, fingerprint, entrance, exit, boss, mini-boss and shrine centres in `SVDungeonState` and
   re-points the gates (`SVDungeonCommands.cs:223-260`).

**What it writes into the world, and only this:** dynamic `Static`, `WallTorch`, `Moongate`, `Spawner` and
`ProximitySpawner` items, all tagged (`SVDungeonBuilder.cs:72, 90`); one untagged `Moongate` outside, placed by hand
with `[SVDungeonGate here` (`SVDungeonGate.cs:48-78`). Nothing in `map*.mul`/`statics*.mul`, no region, no doors
(`EdgeKind` has Arch, Door, Locked and Secret but "only Open is produced so far", `SV\Engine\Model\EdgeKind.cs:5`), no
loot or quest logic (README "Roadmap"). Files: `Data\SVDungeon.cfg` (settings), `Data\SVDungeonPool.cfg`,
`Data\SVDungeonCreatures.cfg`, `Data\SVDungeonCreatureBlock.cfg`, `Saves\SVDungeon\SVDungeon.bin`.

### 1.2 Layout strategies (`SV\Packages\Layouts\`, 1,665 lines)

All three put the entrance on the short side (south for square or tall layouts, west for wide ones,
`SV\Engine\Util\Sides.cs:23-26`), the exit opposite when `ThroughMode` says so, and give rooms their purpose by walking
distance from the entrance (`RoomKindAssigner.cs:16-36`: farthest combat room = boss, next = treasure, the one nearest
0.65 of the maximum = mini-boss, nearest 0.30 = shrine; needs 4 combat rooms besides start and exit).

| Strategy | How it draws | Size rule | Rooms |
|---|---|---|---|
| `maze` (`CellGraphGenerator.cs` + `GridRasterizer.cs`) | a cell grid; 2x2 to 4x4-cell rooms dropped at random with a 1-cell margin (`:97-108`), a recursive-backtracker maze through the remaining cells, regions joined by a random spanning tree plus 3 percent extra links (`:132-220`); every cell becomes a `w x w` floor square, linked cells share a `w`-tile opening, unlinked ones keep one wall tile between them (`GridRasterizer.cs:84-126`) | cells = (size - 1) / (w + 1), at least 8x8, size rounded down to whole cells (`MazeLayoutGenerator.cs:56-75`) | 6 to 16 at 36x36 cells, more on bigger grids; a 3x2 start hall on the entrance side |
| `rooms` (`RoomsLayoutGenerator.cs`) | recursive split of the area into territories of at least `minRoom + 2` (minRoom = max(13, 4w), `:54-61`), one rectangle per leaf (`:251-272`), sibling territories joined by an L-shaped corridor of width `w` between their two closest rooms (`:274-349`), 20 percent chance of an extra corridor per room (`:119-135`); a straight opening from the room nearest the short side to the border (`:402-432`) | exactly the requested size; at least 3 territories a side | one per leaf, 6 at least |
| `cave` (`CaveLayoutGenerator.cs`) | random noise box-blurred twice (radius max(4, w + 1)), cut so `CaveFill` percent is open (`:170-201`), then every open tile not inside a `w x w` open square is closed (summed-area table, `:234-279`) and only the largest connected area is kept (`:281-329`); chambers are the spots of greatest clearance, each a square of `2c - 1` with a 1-tile margin, at most max(6, area / 2000) (`:497-540`) | exactly the requested size, at least max(40, 10w + 20) | start and exit are `w x w` squares cut at the edge; wishes "no pillars" (`:98`) |

### 1.3 Validators (`SV\Engine\Validators\`, 91 lines; both required, cannot be switched off)

- `reachability`: a 4-neighbour flood from `EntranceInside` must reach every floor tile and the exit
  (`ReachabilityValidator.cs:15-31`).
- `width`: every floor tile not on the border must lie inside some `w x w` square of floor
  (`WidthValidator.cs:19-56`). This is the "pets and mounts fit" promise.
- `BlockerProof.Keeps` (`SV\Engine\Util\BlockerProof.cs:17-52`) re-runs both on a copy with every planned blocking item
  closed; `pillars`, `props` and `seal` call it before they keep a blocking item.

### 1.4 Themes and decorators (`SV\Packages\Themes\`, `SV\Packages\Decorators\`, 897 lines)

A theme is a list of **full-block wall ids** picked at random per wall tile (or one fixed style), optional floor
paving ids, looks per decoration kind and wishes (`SV\Engine\Theme\DungeonTheme.cs:66-77`). The shipped ones: `stone`
0x0080/0x0081/0x008C/0x008E with paving 0x04FC-0x04FF and pillar 0x0077; `sandstone` 0x0175-0x0178, paving
0x0525-0x052C, marble pillars 0x011B/0x011D/0x011F; `cave` fourteen rock blocks 0x025C-0x026A (minus 0x0264) and
`cave-smooth` three of them, both wishing `character = natural` and `light = 0.5` (`CaveTheme.cs:15-28`). **No theme uses
a wall set with run pieces, corners or posts; no corner or end logic exists** (the base `Place` looks at nothing but
the tile's own kind). `Place` is virtual, so a theme with neighbour logic is possible (`examples\BossStoneTheme.cs`).

| Decorator | What it plans | Where it writes |
|---|---|---|
| `lighting` (138 lines, order 0, on) | wall torches on floor tiles with a wall to the west or north, about `TorchSpacing` (8) apart, 0.6 of that in boss, treasure, shrine and mini-boss rooms, divided by the `light` wish; spots shuffled with the stage's own stream (`LightingDecorator.cs:64-105`) | `WallTorch` at land Z + 12, burning, flipped for north (`TorchFactory.cs`) |
| `pillars` (118 lines, order 10, on) | a lattice from `w` tiles inside the room's north-west edge every `w + 1` tiles, 70 percent of rooms, 100 percent of lattice points, never in start, exit or boss rooms, only where the theme gives `pillar` a look; the whole set proven with `BlockerProof`, else room by room (`PillarsDecorator.cs:54-116`) | blocking `Static` of the theme's pillar id |
| `props` (324 lines, order 20, on) | per room kind: litter (bones 0x1B09-0x1B0E, 0x0ECA-0x0ECD, a skull one time in four) at one per 60 floor tiles in combat rooms, 120 treasure, 45 mini-boss, 25 boss; webs 0x0EE3-0x0EE6 in inner corners at 50/30/50/70 percent; crates 0x0E3C/0x0E77/0x0E7E in corners at 25/80/30 percent (blocking); graves 0x0ED7 at 60 percent in the shrine, 50 in the boss room (blocking); four candles 0x0A0F at +-2 around the shrine's centre; bones in corridors at one per 150 tiles; nothing within 4 tiles of the entrance or exit; all scaled by the Decoration amount (None 0, Sparse 0.5, Normal 1, Dense 2); man-made kinds held back where the place is `natural` (`PropsDecorator.cs:92-311`) | walkable `Static` items; blocking ones only if `BlockerProof` passes, else all of them dropped |
| `population` (248 + 1,045 lines, order 30, off) | section 1.5 | `Spawner`, `ProximitySpawner` |
| `seal` (100 lines, order 40, off) | a wall block on every floor tile of the border row or column on the entrance side (and the exit side of a through dungeon), the theme's walls unless it gives `seal` a look (`SealDecorator.cs:44-98`) | blocking `Static`; stops walking only, not recall or gates (its own tooltip, `:34`) |
| `gates` (112 lines, order -10, off, recommends `seal`) | one gate on the floor tile nearest the centre of the start room, one in the exit room (`GatesDecorator.cs:47-110`) | `Moongate`, `Dispellable = false`, target = the gate outside; the gate outside targets the inside gate nearest the entrance, or the entrance tile without gates (`SVDungeonGate.cs:126-177`) |

**How many items.** Every wall tile is one `Static`, every floor tile with paving one more. For the default (maze,
145x145, width 3, no paving) the rasterizer makes 36x36 = 1,296 cells of 9 floor tiles plus a 3-tile opening per link,
so roughly a quarter of the 21,025 tiles are wall: **about 5,000 wall statics plus some hundreds of torches and props
(estimate from the rasterizer's rule, not a run)**; `WallShellOnly` drops the buried ones. The README says "thousands of
static items" and "back up your world first". Those items are world-saved and sent to every client that enters the
sectors, which matters for a permanent place and not for a dive (section 4).

### 1.5 The population stage (`SV\Packages\Decorators\Population\`, 2,683 lines)

- **Plan** (`PopulationDecorator.cs:78-187`): per room, tier = round(TierMin + depth x (TierMax - TierMin)) where depth is
  the room's walking distance as a share of the deepest room; treasure and mini-boss one tier harder; boss = 5.
  Start and exit rooms stay empty unless `PopulationEnds` says otherwise. Spawner count = min(3, floor tiles / 80),
  one in boss, mini-boss and shrine rooms. The spawner's radius is the largest, up to min(12, longer side / 2), at
  which the whole square around it is floor of its own room (`FitRadius`, `:196-214`), tried at six spots, best wins:
  **no creature can spawn through a wall**. Each spawner is a `DecoItem` of kind `spawner.boss` or
  `spawner.proximity`, mounted (takes no floor tile), with its plan as text in `DecoItem.Data`
  (`home=;trigger=;min=;max=;mobs=Type:count,...`, `PopulationPool.cs:365-430`).
- **Pool** (`PopulationPool.cs`): `Data\SVDungeonPool.cfg`, one group per line, `tier | name | Type, Type:count |
  rooms=combat,treasure picks=N auto`; a room draws the group that serves its kind with the nearest tier (lower first
  at equal distance, `:308-328`), and `picks` different types of it. The shipped starter pool is 13 groups of stock
  ServUO creatures (`:75-90`).
- **Build** (`SpawnerFactory.cs:97-140`): a boss plan becomes a ServUO `Spawner(total, min, max, 0, home, objects)`
  with `HomeRange = home` and a `Respawn()` two seconds later; a proximity plan a `ProximitySpawner` with
  `MaxCount = the largest single count`, `TriggerRange`, `HomeRange`. Respawn 10 to 20 minutes by default. At start
  the pool is loaded and every type the shard does not have, cannot construct or has blocked is dropped with a console
  line (`:34-95`).
- **Scan** (`CreatureScanner.cs`): `[SVDungeonScan` or the window's "Scan now" constructs every `BaseCreature` type with
  a `[Constructable]` parameterless constructor (`FindTypes`, `:315-338`) five times each, reads fame, karma, hit
  points, damage, AI, fight mode, tamable, can fly, control slots, virtual armour and highest skill (`Sample`,
  `:341-409`), deletes each sample and its mount at once, sets `NoLootOnDeath` first, then sweeps unowned leftover items
  after 3 and 30 seconds (`:243-296`). It blocks the server (the window runs it in 40 ms slices from a `Timer`,
  `PopulationGump.Setup.cs:93-168`). Output: `Data\SVDungeonCreatures.cfg`, a tab table. "Build groups" turns it into
  one auto group per tier of the hunters that give fame or karma, and a boss group from the strongest half of tier 5
  (`PoolAutoGroups.cs:32-79`); tiers are quintiles of fame, hit points or hits x damage (`CreatureCatalog.cs:147-187`).

### 1.6 The server half (`SV\Server\`, 3,841 lines)

Commands (602 lines, all Administrator, each wrapped so an exception reports instead of taking the shard down,
`SVDungeonCommands.cs:31-49`): Anchor, Gen, Layout, Set, Clean (preview / dungeon / all), Info, Go, Tiles, plus Check,
Gate and Scan in their own files. `Clean all` deletes every item on the ground inside the rectangle, **player corpses
and their contents included** (`SVDungeonBuilder.cs:188-212`, `SVDungeonCommands.cs:397-403`), and every creature
there that no spawner owns; the gump asks first (`SVDungeonGump.cs:464-474`). State: a static class saved to
`Saves\SVDungeon\SVDungeon.bin` through ServUO's `Persistence.Serialize` on WorldSave (`SVDungeonState.cs:128-196`,
version 5, including the gate outside as an item reference). Settings: a `SettingsStore` every stage defines its own
keys into (`SV\Engine\Settings\SettingsStore.cs`), read once from `Data\SVDungeon.cfg`, written back by Apply
(`SVDungeonConfig.cs`). The admin gump (799 + 189 + 174 + 241 lines) is a legacy `Gump` with a tab column, rows generated
from the settings definitions, Validators and Decorators tabs that toggle and reorder the stage lists, and a log strip;
the preview (486 lines) draws the layout as merged rectangles of `AddImageTiled` + `AddAlphaRegion` with a letter per
special room and teleport buttons when the picture matches the built dungeon's fingerprint (`PreviewRaster.cs`,
`SVDungeonPreview.cs:241-422`). The tooltip hack (`GumpTooltipText.cs`) exists only because stock ServUO's
`AddTooltip` takes no text; pinned's does (section 2).

## 2. ModernUO port effort and blockers

Checked against pinned for every API the server half uses. Sizes: S = days, M = one to two weeks, L = longer (guesses).

### 2.1 The engine and the engine halves of the packages (6,226 lines): S

`Engine\` (2,619), `Layouts\` (1,665), `Themes\` and `BuiltinWishes` (105), the five decorators (792) and the population
engine half (1,045) reference nothing but `System` and `System.Collections.Generic`, in script-compiler C# (`delegate`
lambdas, `out` parameters, no LINQ). They compile under .NET 10 in a customizations subfolder as they are
**(unverified: not built here, the prompt forbids it)**. One thing to confirm when it is built: the seeds. Every stream is
`new Random(seed)` or `new Random(hash ^ seed)` (`SV\Engine\Pipeline\DungeonContext.cs:103-121`,
`CellGraphGenerator.cs:43`), and the seeded `System.Random` keeps the legacy algorithm on modern .NET, so the author's
seeds should reproduce **(unverified by running)**. The developer manual's console harness (section 7 there) is the
test: hash the ASCII of seeds 1 to 300 on both runtimes.

### 2.2 Gumps (2,974 lines across `SVDungeonGump`, `SVDungeonPreview`, `PopulationGump.*`, `SVTabbedGump`,
`SVGumpKit`, `SettingsEditor`): S-M, mechanical

Pinned keeps a legacy `Gump` class (`PIN\UOContent\Gumps\Base\Legacy\Gump.cs:25`) with `AddPage`, `AddBackground`,
`AddButton`, `AddHtml`, `AddImageTiled`, `AddAlphaRegion`, `AddLabel`, `AddLabelCropped`, `AddTextEntry` and
`AddTooltip(int number, string args = null)` (`:59-190`). Changes: `OnResponse(NetState sender, in RelayInfo info)`
(`BaseGump.cs:74`) and `info.GetTextEntry(id)` returns the string (`RelayInfo.cs:48`), not a `TextRelay`;
`Dragable` is `Draggable` (`Gump.cs:51`); `GetTypeID()` overrides become the `TypeID` property set in the constructor
(`BaseGump.cs:30, 54`); `CloseGump(typeof(X))` and `FindGump(typeof(X))` become the generic extensions
`CloseGump<X>()` and `FindGump<X>()` (`GumpSystem.cs:87-105`). `SVTooltipEntry` and `GumpTooltipText.cs` are deleted:
pinned's `AddTooltip(1042971, text)` is the same packet. The generic `SVTabbedGump<T> : Gump` base and the `partial`
window classes need no change of shape. P93 rated the same changes S for Visual Builder and the duplicator, and
`ClusterFVisualBuilder.cs` (1,045 lines) is the shard's proof that a legacy gump of this size ports.

### 2.3 Timer: none

`Timer.DelayCall(TimeSpan, Action)` exists (`PIN\Server\Timer\Timer.DelayCall.cs:34`); the scan's `ScanTimer : Timer`
subclass and the spawner's two-second `Respawn` call port as they are.

### 2.4 Spawners (`SpawnerFactory.cs`, 142 lines): S, a rewrite of one file

Pinned `Spawner(int amount, TimeSpan minDelay, TimeSpan maxDelay, int team = 0, Rectangle3D spawnBounds = default,
params ReadOnlySpan<string> spawnedNames)` (`PIN\UOContent\Engines\Spawners\Spawner.cs:54-62`) and
`ProximitySpawner(amount, minDelay, maxDelay, team, spawnBounds, int triggerRange, TextDefinition spawnMessage, bool
instantFlag, params names)` (`ProximitySpawner.cs:48-62`); there is no `SpawnObject`, entries are `SpawnerEntry` rows
with `maxCount` and `probability` (`SpawnerEntry.cs:81-105`); `HomeRange` is settable after `MoveToWorld` and the
shard's own seeder does exactly this (`ClusterFRootdeepSeeder.cs:189-196`). Per-type counts become one entry per type
with its `maxCount`, which is cleaner than the ServUO workaround (`MaxCount = the largest single count`,
`SpawnerFactory.cs:118-120`).

### 2.5 Map, region, tile data, commands: none to S

`map.Tiles.GetLandTile(x, y)` (`PIN\Server\TileMatrix\TileMatrix.cs:341`), `GetStaticTiles(x, y)` (`:271`, an
enumerable, so `.Length` becomes a count), `map.GetItemsInBounds(rect)` and `map.GetMobilesInBounds(rect)`
(`Map.ItemEnumerator.cs:80`, `Map.MobileEnumerator.cs:80`; no `GetObjectsInBounds`, so the area check loops twice, and
no `.Free()`), `Region.Find(Point3D, Map)` (`Region.cs:291`), `map.DefaultRegion` (`Region.cs:228`), `TileData.ItemTable`,
`MaxItemValue`, `ItemData.Impassable`, `Height`, `Surface` (`PIN\Server\TileData.cs:100-165, 289-291`),
`CommandSystem.Register(string, AccessLevel, CommandEventHandler)` (`PIN\Server\Commands.cs:221`), `[Usage]` and
`[Description]` (`PIN\Server\Attributes.cs:118-126`), `Moongate(Point3D target, Map targetMap = null, bool
dispellable = true)` with settable `Target` and `TargetMap` (`PIN\UOContent\Items\Skill Items\Magical\Misc\Moongate.cs:34-40`),
`WallTorch()` with `Flip()` and `Burning` (`PIN\UOContent\Items\Lights\WallTorch.cs:11-25`), `Static(int)`
(`PIN\UOContent\Items\Misc\Static.cs:11`). All present.

### 2.6 Persistence and the "0 Serialize" claim: S

Verified: `grep` over the 77 files finds no class deriving from `Item`, `Mobile` or `BaseCreature` and no
`Serialize(IGenericWriter)`; the two hits are `Persistence.Serialize` / `Deserialize` in `SVDungeonState.cs:130, 164`,
a side file written on `EventSink.WorldSave`. Pinned's shape for that is a `GenericPersistence` subclass
(`PIN\Server\Serialization\GenericPersistence.cs:23-60`), which `ClusterFVisualBuilderStore` and
`ClusterFWinterDecorState` already use. Fields: a map, a point, an enum, ints, points, a string and one item
reference (the gate outside). About 60 lines.

### 2.7 The tag collection: S, but it is new code

`WeakEntityCollection` (ServUO) has no pinned counterpart (0 hits in `PIN\`). It is used for tagging every built item
(`SVDungeonBuilder.cs:72, 90`), counting them, cleaning, and finding the inside gates (`SVDungeonGate.cs:109-124`).
Replacement: a `HashSet<Serial>` inside the state's `GenericPersistence` (saved serials, dead ones dropped on load) or,
simpler, an `Item` subclass is out (it would add a serialized class); the serial set is about 40 lines.

### 2.8 Reflection and the scanner: S-M, and the one piece to redesign

`ScriptCompiler.FindTypeByName(name, true)` is `AssemblyHandler.FindTypeByName(name, fullName: false, ignoreCase: true)`
(`PIN\Server\AssemblyHandler.cs:189`); `ScriptCompiler.Assemblies` is `AssemblyHandler.Assemblies` (`:31`);
`Core.Assembly` exists (`PIN\Server\Main.cs:264`). `[Constructable]` is `[Constructible]` (`PIN\Server\Attributes.cs:105`)
and `Add.IsConstructable(ctor, level)` is `TypeAttributes.IsConstructible(ctor, level)`
(`PIN\UOContent\Utilities\TypeAttributes.cs:9`); pinned's `AccessLevel` has no `Spawner` level (`PIN\Server\Mobiles\Mobile.cs:141-150`:
Player, Counselor, GameMaster, Seer, Administrator, Developer, Owner), so the check uses GameMaster. Three members
the scanner relies on do not exist: `BaseCreature.NoLootOnDeath` (0 hits; pinned generates loot inside the constructor,
`PIN\UOContent\Mobiles\BaseCreature.cs:864`, and the pack is deleted with the creature, so the flag is unneeded),
`Serial.LastItem` (snapshot `World.Items` keys instead, `PIN\Server\World\World.cs:88`) and `Cleanup.IsBuggable` exists
(`PIN\UOContent\Misc\Cleanup.cs:155`). The real question is whether to port the scan at all: it constructs every
creature type of the shard, five times, on the main thread, and depends on constructor side effects being harmless.
On our shard the tiers it guesses from fame quintiles will be superseded by F-14's creature levels, so the port should
**replace the scan with a hand-written pool** (section 6) and keep the pool format.

### 2.9 Size per stage

| Part | Lines | Port | Size |
|---|---|---|---|
| Engine, layouts, themes, decorators, population plan | 6,226 | copy, build, seed check | S |
| Builder, items, area check, config, state, tag set | 214 + 74 + 240 + 102 + 199 + new | rewrite the ServUO calls (sections 2.5 to 2.7) | S |
| Commands and gate | 602 + 179 | mechanical | S |
| Spawner factory | 142 | rewrite | S |
| Admin gump, preview, kit, editor | 1,889 | mechanical (section 2.2) | S-M |
| Population window and scanner | 1,085 + 411 | window mechanical; scanner replaced by a pool file | M |
| Per-instance state (for several dives at once) | new | the static `SVDungeonState` and the one-dungeon rule become an instance per trial map | M |
| Tests (facts for the layout rules, the builder, the clean) | new | the author's console harness becomes xunit facts | S |

Whole port as it stands, one dungeon per shard: **2 to 3 weeks of prompts (guess)**; the dive-ready version with
per-instance state and no scanner about the same, because the scanner and the gump pages it needs fall away.

## 3. Fit with how we already build dungeons

### 3.1 The two pipelines side by side

| | Rootdeep (P36, P139-P141, P167, P180-P185; the playbook) | SVDungeon 0.7.0 |
|---|---|---|
| Medium | land and statics written into the map files of a scratch client copy, verified by re-reading, shipped in the player package (`notes\cc-P167-rootdeep-map-batch.md` section 1) | dynamic `Static` items at runtime, world-saved, removable (`SVDungeonBuilder.cs`) |
| Plan | `layout.json` (floors, solid blocks, openings) approved as a mockup, then `build_burrows.py` | a seed plus settings; the plan lives only in memory (`DungeonLayout`), plus a saved fingerprint |
| Walls | OSI sets by the run-topology rule: ew, ns, post, corner, Ts; cave rock rings with a Z profile (playbook 2.1, 2.7) | one full-block id per wall tile, picked at random (`DungeonTheme.cs:76`); no pieces, no corners, no rock rings |
| Doorways | framed per set (playbook 2.3) | none: an opening is floor; `EdgeKind` doors unimplemented |
| Corners | every inner corner dressed by a zone rule (2.2) | webs, crates and graves in inner corners by chance (`PropsDecorator.cs:195-203`): the same idea, thinner |
| Density | 5 to 12 pieces per 100 floor tiles, OSI-measured (2.4) | about 3 to 5 at Normal (litter 1 per 60 plus corner items), 6 to 10 at Dense; torches separate |
| Variety | weighted stock variants, never two identical pieces touching, seeded clusters (2.6) | random picks with repeats allowed; torches on a shuffled list with a spacing radius |
| Torches | floor tile before a north or west wall at Z +13 to +15 (OSI 150 of 150) | the same tiles, Z +12 (`TorchFactory.cs:17`) |
| Pillars | a walled block with a floor at wall height (playbook section 1, last row) | one blocking `Static` on a lattice (`PillarsDecorator.cs`) |
| Walkability gate | the plan's floor, openings and walls equal the record (checklist 8) | reachability and `w x w` width validators, `BlockerProof` after every blocking decorator |
| Spawns | hand rows in `ClusterFRootdeepSeeder.cs` (count, home range inside the room, group respawn, Young limit) | depth tiers from a pool, spawn box fitted inside the room, proximity spawners |
| Region | `OldHavenBurrowsRegion : DungeonRegion`, travel rules, Young limit | none; `seal` walls the door up instead |
| Z | floors at 0, rings at 0 / +12 / +20 | flat area required (land Z spread at most 6), every item at its tile's land Z |

### 3.2 Replace, feed or fight

- **Replace: no.** As built it fails playbook section 1 rows 1 (wall pieces), 5 (variety), 6 (frames) and 11
  (torch height), and its lattice pillars are the "grid-placed decor" of row 4. It cannot produce a permanent dungeon
  that passes the junction sheet, and a permanent place made of 5,000 dynamic items is the wrong medium (every world
  save, every sector packet).
- **Fight: no.** It touches no map file and no region, so nothing it does conflicts with a map build or with
  `OldHavenBurrowsRegion`; a region can be registered over a generated rectangle the same way, and `[SVDungeonClean
  dungeon` leaves the map as it was.
- **Feed: yes, three ways.** (a) The layouts: `DungeonLayout.Tiles`, `RoomAt` and `Rooms` are the floor, solid and
  room record `layout.json` carries (the mockup's shape, `notes\art\rootdeep-mockup\layout.json`); an exporter of about
  80 lines would let `build_burrows.py` dress a generated plan with OSI sets, frames and corners by the playbook's
  rules, which is the right way to make a permanent generated dungeon. (b) The validators and `BlockerProof` are the
  formal form of checklist 8, cheap to add to `mapbuild.checklist`. (c) The population plan (depth tiers, one spawner
  per 80 floor tiles, spawn box fitted to the room) is a rule set our seeder rows follow by hand today.

### 3.3 Which stages are worth having

| Stage | Worth having | Why |
|---|---|---|
| maze, rooms, cave layouts | yes, as a plan source | three generators with a size rule and a width guarantee; cave is the one we lack (Rootdeep's warrens were hand-drawn) |
| reachability, width, BlockerProof | yes | the walkable gate as code; `w x w` squares are a better pet test than our floor-set equality |
| room kinds by distance | yes | boss farthest, treasure next, mini-boss 0.65, shrine 0.30: a rule for every dive |
| population plan and pool format | yes, as design and as the dive spawn table | depth tiers, box fit, `tier | name | types | rooms=` lines; the shard's F-14 levels replace the fame quintiles |
| creature scan and auto groups | no | constructs every type; our tiers come from F-14 and the Bestiary; a hand pool per dive theme is smaller and safer |
| lighting | as is for dives; the playbook's Z for anything permanent | same wall rule as OSI; Z 12 against our measured 13 to 15 |
| props | for dives only | thinner and less varied than the playbook; fine for a 20-minute place |
| pillars | no | lattice look; a walled block is the house pillar |
| themes as shipped | for dives only | block walls; a dive theme of our own could use OSI block sets (the Minecraft look is exactly block walls, section 4.3) |
| seal | no | a region's travel rules and a gate do this without 3 wall blocks in a doorway |
| gates and the gate outside | yes | the moongate pair is the trial-map entrance the storyline instancing note describes (`docs\league-storyline.md:39-47`) |
| admin gump and preview | later | a dive is started by a job, not by a gump; the preview's ASCII (`DungeonLayout.ToAscii`) and our renderer cover staff checks |

## 4. Uses, ranked

1. **Staff tool for quick League dives: the best fit.** F-24's dives are temporary, solo-or-party, with a mini boss on
   investigation (`docs\feature-queue.md:1918-1960`), and the storyline note settles that each party gets a private
   trial map (`docs\league-storyline.md:39-47, 142`). A dive is built when the job starts, played for twenty minutes
   and torn down: dynamic items are the right medium, the seed makes every dive of a job reproducible, `gates` is the
   way in and out, `population` with a per-theme pool fills it, `[SVDungeonClean` is the teardown. Missing for that
   use: per-instance state (section 2.9), a region per dive (ours, for the travel rules and the Young limit), objectives
   and loot from the F-24 contract framework, and a size cap (an 80x80 rooms layout at width 3 is a few hundred wall
   items; the 145x145 default is thousands).
2. **Spawn reference, now.** The pool file format and the depth-tier rule are the design for the dive spawn table and
   for any new seeder's rows; `FitRadius` is the rule the Rootdeep rows follow by hand ("home ranges stay inside their
   room", `ClusterFRootdeepSeeder.cs:18-20`). Nothing to port for this; section 7 records it.
3. **The Minecraft-themed dungeon.** Full-tile block walls on a square cell grid are what the maze rasterizer draws, so
   a "block" theme (stone, sand, wood and cobble block ids chosen from tile data, torches, no props) would read as
   intended with no engine change. Two cautions: the dungeon has no brief anywhere in the repo (the only mentions are
   the intake row and this prompt; `grep -ri minecraft docs notes` finds nothing else), so what it is for, where and how
   big is Chase's to say; and a permanent one should be a generated plan dressed and baked into map statics through the
   layout export (section 3.2a), not thousands of live items.
4. **The starter dungeon: no.** The Rootdeep Burrows are built (region P36, map P167 at the renders stop, creatures
   P139-P141, spawner rows P141) by the playbook's rules, which this tool cannot meet.

## 5. License and crediting

The terms are one sentence in the README ("Free to use and modify, credit is appreciated but not required", line 12)
and in `SOURCE.txt`; there is no LICENSE file in the zip (listed: `find` shows none). Crediting for us, following the
house pattern of `ClusterFVisualBuilder.cs:14-20` and `ClusterFLayoutCapture.cs:14-18` (both name their servuo.dev
author and the kept download in the file header):

- every ported or rewritten file carries a header naming ScriptVisitor, "SVDungeon 0.7.0 (servuo.dev, 2026-10-20)",
  the download kept at `D:\UO\third-party\code\svdungeon-0.7.0`, and what we changed;
- the port prompt's notes and the CODE-INTAKE row say the same;
- if any of it ever ships to players (a dive is content, the generator is not), a line in the player-facing credits
  where the shard lists third-party work.

Nothing in it is GPL and nothing is ripped art: the themes use stock tile ids only.

## 6. Recommendation: borrow now, port later, in two pieces

**Now (no code):** take the population design and the pool format into the League dive spawn table (section 7 records
the rules), and keep the layout generators in mind as the plan source for any generated permanent dungeon.

**Port later, piece 1, when F-24 dives and the trial maps are being built:** engine, layouts, themes, the five
decorators minus `seal`, the builder, commands, state as `GenericPersistence`, the serial tag set, population from a
hand-written pool, `gates`; no scanner, no admin gump, no preview gump (ASCII preview to the console and
`[SVDungeonGen seed` are enough for staff). Piece 2, only if dives are run by hand rather than by jobs: the admin gump
and preview.

**Not: themes as shipped for anything permanent, the scanner, `seal`, `Clean all`** (it deletes player corpses; a dive
region's own teardown should move players and corpses out first).

### Draft prompt (into the notes only; the overseer queues it)

```
# CC task P-nnn: SVDungeon on ModernUO, piece 1: the dive generator (engine, builder, commands, population)

**Model:** Fable

**Touches:** server/customizations (new folder SVDungeon/), tests (UOContent.Tests facts), docs (notes, feature-queue
F-24 cross-reference, map-building-playbook section 5). No pinned patch. No map file, no region file, no player package.

**Summary:** Port ScriptVisitor's SVDungeon 0.7.0 generator (D:\UO\third-party\code\svdungeon-0.7.0, assessed in
notes\cc-P211-svdungeon-070-assessment.md) as the staff tool that builds a temporary League dive from a seed: the
engine, the three layouts, the themes, lighting, pillars, props and gates, the builder, the commands, the state, and
the population stage fed by a hand-written pool. Leave out the creature scanner, the admin gump, the preview gump and
seal. Credit ScriptVisitor in every file header (free to use and modify, credit appreciated).

Read first: the assessment (sections 1, 2 and 6), DEVELOPER-MANUAL.md, notes\map-building-playbook.md section 5, the
Rootdeep seeder (ClusterFRootdeepSeeder.cs) for the shard's spawner shape, ClusterFVisualBuilder.cs for the house
pattern of a ported staff tool.

1. Engine and packages: copy SV\Engine, SV\Packages\Layouts, Themes, BuiltinWishes, the Lighting, Pillars, Props and
   Gates decorators and the population engine half (PopulationDecorator, PopulationPool, PoolAutoGroups may be left
   out, CreatureCatalog left out) into server/customizations/SVDungeon/, namespaces kept. Build. Facts: the ASCII of
   seeds 1 to 50 for each layout at widths 2, 3 and 5 is stable run to run (a golden file), every one passes both
   validators, and the width rule holds after pillars and props.
2. Server half, rewritten for pinned as the assessment's section 2 says: SVDungeonItems, SVDungeonBuilder (a
   GenericPersistence-backed serial set replaces WeakEntityCollection), SVDungeonCheck (GetItemsInBounds +
   GetMobilesInBounds), SVDungeonConfig, SVDungeonState as GenericPersistence, SVDungeonGate, SVDungeonTileset,
   SVDungeonCommands (Anchor, Gen, Layout, Set, Clean preview|dungeon only, Info, Go, Tiles, Gate; no Clean all),
   TorchFactory, GateFactory, SpawnerFactory with SpawnerEntry rows (one per type with its maxCount). Facts on the test
   host: a 60x60 rooms layout builds at a flat spot of the test map and Clean removes exactly the tagged items; a
   second Gen removes the first; the area check refuses statics, items, a Z spread over 6 and a region in Error mode.
3. Population from a pool file: Data/SVDungeonPool.cfg in the shipped format, written by hand for one dive theme
   (undead) from creatures the shard has; the factory makes ProximitySpawners with the plan's home range and trigger;
   fact: every spawn box lies on its room's floor, boss room tier 5, start room empty.
4. Docs: notes with counts, the seeds golden file, what was left out and why; F-24 entry gains a line pointing at the
   tool; playbook section 5 updated with anything learned.

Tests red first, as always. Do not run it against the live shard or the player package; the test shard only, with
the lock. Last line P-nnn DONE.
```

## 7. Added to the playbook

Written into `notes\map-building-playbook.md` as section 5 ("Generated dungeons: what SVDungeon 0.7.0 taught, P211"):
the width rule as a `w x w` square test, the blocker proof after every blocking placement, per-stage seeded streams,
room kinds by walking distance, spawn boxes fitted to their room, the one-spawner-per-80-floor-tiles and
depth-tier rules, the area check's numbers, and the medium rule (items for temporary places, map statics for
permanent ones, with the item-count reason).

## Preflight

Docs only: this file and the playbook section. No file over 5 MB. shard-migration Bronze copy: two files changed, nothing
else; ShatteredLegacy Bronze copy untouched. The commit script's dry run was not run (it reads the main checkouts, which
are other desks under the hand-off rules).

P211 DONE
