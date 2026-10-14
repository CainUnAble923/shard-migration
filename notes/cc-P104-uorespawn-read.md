# cc-P104: UORespawn, a closer read of its ModernUO scripts (read and report)

2026-10-14. Read and report. Prompt: `D:\UO\cc-prompts\cc-P104-uorespawn-read.md`. No shard code changed, nothing built
or run. Not committed (autopilot commits after DONE). Both repos were clean at the start, apart from the play-test
importer's machine output.

## Headlines

- **Recommendation: idea only.** Do not port this code. A wilderness gap filler of our own, if wanted, is **M**.
- **It sits beside stock spawners, not in place of them, but it is not harmless to them:**
  - It spawns in a ring 30 to 80 tiles around every logged-in player, everywhere.
  - Nothing checks for stock spawners, houses, guarded towns or anywhere else.
  - At start it executes a file of commands against stock `Spawner` items. Its DELETE deletes **any item** by serial.
- **The code has real bugs on current ModernUO:**
  - its day/night test reads hours as clilocs, so night is never detected;
  - every effect hue lands in the `speed` argument;
  - the frequency roll makes Rare unreachable;
  - an ambush leader's death likely deletes its whole gang;
  - invisible "effect" birds damage players within 3 tiles;
  - rift gates drop players on the other facet at the same coordinates, unchecked.
- **There is no global cap.** It deletes mobs only per type (more than 20 of a type, out of sight). Every 250 ms it
  does O(players x its own spawn) work and allocates lists.
- **License: MIT, by the GitHub repository's LICENSE file** (`github.com/Kita72/UORespawnProject`; the README credits
  "Wilson (Creator)"). The ModernUO scripts themselves carry no header.
  - Their "server source" is a nested zip inside the editor download. The GitHub repo's own server folder is labelled
    for ServUO.
  - SOURCE.txt's "0 .cs" is wrong, as P93 said.
- **Nothing in it is OSI-faithful.** Player-anchored spawning is the opposite of OSI's fixed spawns.

## What changed

Nothing in either repo. One folder outside both repos:

- `D:\UO\third-party\code\uorespawn\_extracted-muo\`: the MUO zip
  (`_app-resources-binaries-removed\Data\SERVER\MUO\UORespawnServer.zip`, 123,189 bytes) extracted. That is 96
  entries, 77 `.cs` (12,473 lines) and `DOCS\SERVER_README.md`; 436,525 bytes.
- The extraction checked every entry for absolute or `..` paths before writing.
- `D:\UO\third-party` is not a git repository (`git rev-parse` fails), so nothing there can reach a commit. There is
  nothing to `git check-ignore`.
- `SOURCE.txt` and the other third-party records were not edited.

## How it was read

- All 77 files and the README were read whole, in three parallel read-only passes:
  - core, managers, timers and services;
  - spawners, entities, helpers, enums, commands, targets and gumps;
  - mobiles and items.
- API questions were checked against pinned ModernUO (`D:\UO\ModernUO-pinned`, d4531cd94).
- I re-read these claims in the source myself before writing them here:
  - the clock call (`UOR_Utility.cs:144-149` against `Clocks.cs:53,86`);
  - XMLManager's delete (`XMLManager.cs:133-143`);
  - the connect hook (`UOR_Core.cs:364-374`);
  - "ALWAYS create new" (`UOR_Core.cs:450-453`);
  - the effect damage (`EffectUtility.cs:160-185`);
  - the effect call (`EffectUtility.cs:375-377` against `Effects.cs:130-131`);
  - the rift gate (`RiftGate.cs:14-30`);
  - the ambush deletion (`AmbushNPC.cs:187-206`).

Paths below are under `_extracted-muo\`.

## What it does, by area

### Hooks and start-up

- No `Configure`. `UOR_Core.Initialize` (`UOR_Core.cs:109-135`):
  - writes the editor's OUTPUT files (`GameManager.InitializeData`);
  - reads its INPUT spawn packs and settings (`SpawnManager.LoadSpawns`);
  - subscribes `ServerStarted`.
- `OnServerStarted` (:141-191), in order:
  1. re-links its own spawn (:197);
  2. **deletes every UOR mob from the last session** (:219-227);
  3. spawns vendors if enabled (:233-284);
  4. runs `XMLManager.ProcessCommands` (:165);
  5. builds or loads a spawn-location cache (:170);
  6. creates seven services (:290-303);
  7. subscribes `WorldSave`, `WorldSavePostSnapshot`, `Connected`, `Logout`, `Shutdown`, `ServerCrashed` (:308-329);
  8. starts its timers (:408-415).
- **`Connected` gives every PlayerMobile, staff or not, a per-player search timer** (:364-374).
- Logging out of the last session pauses the whole system (:376-392).
- Commands (`Commands\UOR_Commands.cs:8-15`):
  - `[UORespawn`/`[UOR` (Administrator): the control gump;
  - `[UORAdd`/`[UORDrop` (Counselor);
  - `[ShowRespawn` (Administrator): every UOR creature within 40 tiles says "I AM RESPAWNED!", in public.
- The gumps' `OnResponse` handlers do not re-check AccessLevel; they rely on only staff being sent the gump.

### Its own spawner, beside the stock ones

- `UOR_Spawner : Item, ISpawner` (`Spawners\UOR_Spawner.cs:16-17`) is not a `BaseSpawner`.
  - Two singletons, invisible at `Point3D.Zero` on `Map.Internal` (:52-62): `UOR_MobSpawner` (home range 50) and
    `UOR_VendorSpawner` (home range 15).
  - They own creatures through `Mobile.Spawner` plus a serialized serial list (:21-25), re-linked after load (:143-168).
  - `Running => false`, `Respawn()` is a no-op, and `OnDelete` is overridden to do nothing (:40-46, :77-81).
- `Spawners\RegionSpawner.cs` is `internal static class RegionSpawner` in `Server.Custom.UORespawnServer` (:6-7). It does
  not collide with pinned's `Server.Engines.Spawners.RegionSpawner` (P93's guess was wrong). It, `BoxSpawner` and
  `TileSpawner` only pick a creature name.

### The spawn decision

- **Where:** each player's `SearchTimer` runs every 125 ms (`RespawnerEntity.cs:29`, `UOR_Settings.cs:15`). It queues up
  to 5 spots (`SearchTimer.cs:38-48`). `Locate` makes up to 3 tries (`UOR_Utility.cs:228-323`), picking a point in a ring
  30 to 80 tiles from the player:
  - from the cache, or a random angle checked with `Map.CanSpawnMobile` (:345-434);
  - rejected if more than 3 non-vendor mobiles stand within 30 tiles, or if it is within 30 tiles of a spot already
    queued (:436-473; `RespawnerEntity.cs:43-67`);
  - lava is refused; "water" tiles are allowed.
- **When:** one global `ProcessTimer` runs every 250 ms. For each player with fewer than 25 mobiles within 80 tiles, it
  spawns one queued spot (`ProcessTimer.cs:35-57`).
  - Every mobile is counted except vendors, including players and stock spawns (`UOR_Utility.cs:460-473`). That is its
    only awareness of stock spawning.
- **What:** one dice roll picks a frequency (`SpawnEntity.cs:120-154`): Timed < 0.01, Weather < 0.01, Rare < 0.01,
  Uncommon < 0.1, else Common.
  - The name then comes from the spawn packs. In a town or dungeon region only the region's lists are used; elsewhere
    box, then region, then tile (`SpawnEntity.cs:156-210`).
  - Nothing found, or an unknown type name, spawns a **WanderingHealer** (:196-207; `UOR_Utility.cs:610-619`).
- **"Recycling":** before creating a mob, it moves an existing UOR mob of the same type that no player is within 80
  tiles of. It picks the one furthest from players and resets its hits (`UOR_Core.cs:439-454`; `SpawnQueryService.cs:38-81`;
  `ProcessService.cs:88-100`). Its `Home` is not updated.
- **Despawn:** every 5 s, `ValidateAndTrim` deletes the excess of any type with more than 20 live mobs, furthest first,
  out of sight only (`SpawnQueryService.cs:89-154`).
  - Nothing else despawns: not by distance, not by age. Every restart deletes them all.
- **Extras:** on about 1% of spawns (`ProcessService.cs:79-175`): a water mob, an undead by a grave at night, a weather
  effect and rift mob, or a TownNPC 3 to 10 tiles away.
- **Vendors** are off by default (`ENABLE_VENDOR_SPAWN=false`, `UOR_Settings.cs:55`).
  - When on, it places named vendors at shop-sign and beehive spots from `INPUT\UOR_VendorSpawn.bin` (`SpawnManager.cs:528-658`;
    `Spawners\VendorSpawner.cs:20-107`).
  - It never checks for stock vendors already there, so it would duplicate them.

### Persistence

- Everything is under `<server>\Data\UORespawn\` (`UOR_DIR.cs:7-55`):
  - INPUT: four binary spawn packs written by the desktop editor, a settings CSV, and `UOR_XmlCommands.txt`;
  - OUTPUT: map, bestiary, region, tile, spawner, sign and hive lists, rewritten every start for the editor;
  - COMMANDS: in-game edits for the editor;
  - SYS: a debug log and a binary location cache;
  - STATS: daily files, those older than 7 days deleted.
- The two singleton items save through ModernUO's serialization generator. The mobs are ordinary creatures in the save.
- No network, process, socket or file-watcher code anywhere (all 77 files searched). `ProcessService` is the spawn-queue
  service, not a process launcher. The editor link is files on disk, read once at start; there is no hot reload.
- Its command files do not round-trip. Edits made in game write data that the start-up replay cannot parse, and the
  command file is deleted before it is applied (`CommandManager.cs:210-222`; `EditCommand.cs:105-135`).

### XMLManager (not XmlSpawner)

There is no XmlSpawner code. `XMLManager` runs `INPUT\UOR_XmlCommands.txt` once at start, then deletes the file
(`XMLManager.cs:24-113`):

- `DELETE|serial`: `World.FindItem(...)`, then `item.Delete()`, with **no type check**: any item (:119-152);
- `ADD`: a stock `new Spawner()` with entries (:160-219);
- `EDIT`: sets a `BaseSpawner`'s HomeRange and delays (:228-267).

### Creatures and items (`Mobiles\`, `Items\`)

- Eleven invisible, blessed "effect" Birds emit ambient effects as they move. On each step there is a 50% chance that
  every player within 3 tiles takes, or heals, a random tenth of their hits, with no attacker and no region or Young
  check (`EffectUtility.cs:108-188`, :160-185).
  - The generic `EffectNPC` never fires, and can throw a NullReferenceException (`EffectUtility.cs:90-92`).
- `AmbushNPC`: a hidden paragon skeletal knight that springs a facet-themed gang of 1 to 5 when anything steps on it
  (`AmbushNPC.cs:23-183`).
  - Members are placed on the same Z with no fit check.
  - When its combatant clears it deletes the gang and itself (:187-206). That likely includes its own death, since
    `Kill` clears the combatant before the corpse is made (inference, not run).
- `RiftMob`: a "rift wisp", the Blizzard weather spawn. After more than 4 spell hits it opens a `RiftGate` on death
  (`RiftMob.cs:98-127`).
  - The gate goes Trammel to Felucca (or back) at the **same X, Y, Z**, unchecked (`RiftGate.cs:14-30`). It lasts 30 s
    and anyone can use it.
- `SpecialSnowMob`: a single-instance paragon frost warden on snow tiles.
- `TownNPC`/`WorldNPC`: flavour walkers with invented speech.
- `PlaceHolder` (debug): anyone who double-clicks it is teleported to its spawn point.
- `DebugFlag` (debug): one item per failed search; it shows a player's name to anyone.
- Paragons are rolled on every facet, at 1% per ambush creature (`AmbushUtility.cs`). ModernUO limits paragons to Ilshenar.
- `NPCUtility.CheckNightDress` runs on vendors every minute when vendors are on.
  - By day it deletes whatever the vendor holds in both hands, a stock vendor's weapon included.
  - By night it makes a new lantern or torch each time, which likely leaks when the hand is full (`NPCUtility.cs:19-38`).

## The answers

### 1. Replace, beside, or only empty space?

**Beside**, with no notion of "empty space".

- It never replaces, wraps or disables stock spawners or their timers (`UOR_Spawner.cs:16-17` is its own `ISpawner`).
- It spawns around every player regardless of what stock spawns are there:
  - the only check is a crowd count of any mobiles (`UOR_Utility.cs:436-473`, `ProcessTimer.cs:41-43`);
  - there are no house, guard-zone or spawner-coverage checks (none in all 77 files);
  - town regions are spawn sources, not exclusions (`SpawnEntity.cs:160-166`).
- It also reads stock spawners for the editor (`GameManager.cs:348-388`), and executes edit, add and delete commands
  against them at start (`XMLManager.cs:119-267`).
- So with stock spawns intact it would add a second population on top, and move it toward wherever players are.

### 2. Limited to places stock spawns do not cover?

**Possible, but it means rewriting the selection, not configuring it.** What it would take:

- **A coverage map:** at start, rasterise every stock spawner's home range (and region spawners' regions) into a
  per-facet bitmap. Refuse any spot inside it, inside a house or guarded region, or inside our tutorial and event regions.
- **An allowlist of regions or boxes** where it may spawn at all, empty by default.
- **Remove or stub XMLManager**, the vendor spawner, the effect NPCs' damage, the rift gate, the ambush deletion and the
  debug teleport.
- **Fix the clock call** (`Clock.GetTime(map, x, y, out int cliloc, out string _)`) and the frequency thresholds.
- **A global cap** and a despawn by distance and age.
- **Our own spawn lists** in reviewable text, not the editor's binary packs.

That is most of the system. A small filler of our own would cost less than changing this one.

### 3. Main-thread cost, unbounded things

All of it runs on the game loop (`Server.Timer` throughout; no async or threads), except one handler.

- **Every 250 ms:** for each player, a `GetMobilesInRange(80)` count. Each spawn calls `FindRelocatable`, which builds a
  list of all UOR spawn plus LINQ, and makes client scans at 80 and 320 tiles per same-type candidate
  (`SpawnQueryService.cs:38-81`). That is O(players x UOR spawn) per tick, with allocations.
- **Every 125 ms per player:** up to 3 location tries with a 30-tile mobile scan each, until its queue of 5 is full.
- **Every 5 s:** trimming, with more client scans per over-limit mob.
- **Every 30 s and 60 s:** full `World.Mobiles` scans for its counts (`UOR_Spawner.cs:174-229`).
- **At start:**
  - two `World.Items` scans;
  - a location cache that samples every 20th tile of every map, if its file is missing;
  - if the hive file is missing, **an index of every named static on every tile of every map, kept in memory for good**
    (`UOR_Utility.cs:185-226`).
- **Unbounded:**
  - the total UOR population: there is no global cap (`UOR_Core.cs:450-453`, README:931), only 20 per type out of sight;
  - the session log, which grows until shutdown (`LogManager.cs:14,51,126`);
  - debug flags, one per failed search;
  - the static index;
  - the inferred night-lantern leak.
- **Thread safety:** `WorldSavePostSnapshot` is raised on a thread-pool thread in pinned (`World.cs:372,443`). Its handler
  writes the stats list that the main thread's `ProcessTimer` is adding to: a data race.

### 4. License and the real "server source"

- **MIT:** the GitHub repository `Kita72/UORespawnProject` has a `LICENSE` file, and its README says MIT and credits
  "Wilson (Creator)". Read today with a web fetch; P93's "verify" is now settled.
- The 77 ModernUO files carry no header. "Wilson" appears only in the console logo (`UOR_Core.cs:40`). The version is
  2.0.1.4 (`UOR_Settings.cs:9`).
- **The server source** is a zip nested in the editor download (`Data\SERVER\MUO\UORespawnServer.zip`, 77 `.cs`, dated
  2026-03-10), beside a ServUO set. The GitHub repo shows only `UORespawnApp/UORespawnServer/`, described as for ServUO.
  So the ModernUO set's authoritative copy is the editor zip.
- SOURCE.txt is wrong twice: "0 .cs" and "TERMS: none stated".

### 5. Fit with the faithful-port direction

**No fit.**

- Nothing in it reproduces OSI. OSI spawned from fixed spawners and region spawns; this anchors spawns to players and
  moves them toward them.
- Its tiers, boxes, recycling, rifts, ambushes, effect birds, paragons on every facet and vendor night-hiding are all its
  own. The README's own word is "player-centric".
- The few stock systems it touches (game clock, weather zones, moongate rules) are ModernUO's, not additions.
- It would add custom behaviour with no OSI basis, in the one area the shard protects most, stock spawns
  (`patches\ImportSpawners-guid-key.patch`, `tests\Misc\SpawnerImportVerification.cs`).

## Recommendation: idea only

- **Do not port.** Porting means auditing and rewriting most of it: the bugs above, the start-up item deletion, the
  player damage, the unchecked facet gate, no global cap, and the per-tick allocations. The result would still fight
  "faithful port first".
- **Ideas worth keeping**, if the shard ever wants spawns in places OSI left empty, such as new custom areas:
  - an `ISpawner` singleton that owns dynamic spawn, so `Mobile.Spawner` cleanup works (`UOR_Spawner.cs`);
  - a sampled valid-location cache per facet, and a ring search around a point (`SpawnLocationCache.cs`, `UOR_Utility.Locate`);
  - per-type trimming that only removes what no player can see (`SpawnQueryService.ValidateAndTrim`);
  - weather and time bands as spawn conditions, with the clock call done right.
- **If wanted, our own "wilderness filler" is M:**
  - region- or box-allowlisted only;
  - refuses any stock spawner's coverage, houses, and guarded or event regions;
  - global and per-area caps, despawn by distance and age;
  - spawn lists in reviewable JSON;
  - tests in the shard's suite.

## Deviations and decisions for Chase

1. The reading was split across three parallel read-only agents. I verified their key claims in the source myself (the
   list under "How it was read"); the rest is as they reported, with file:line.
2. Two findings are inferences, not observed: an ambush leader's death deleting its gang and corpse, and the
   night-lantern leak. Nothing was run, as the brief says.
3. I fetched the public GitHub page once, read only, to settle the license, since the local files state none.
4. **Decision for you:** keep this as an idea only (recommended), or ask for an M-sized wilderness filler of our own
   for custom areas. Nothing on the current plan needs one.

## For Chase

- `D:\UO\third-party\code\uorespawn\_extracted-muo\` (436 KB) can be deleted whenever you like. Nothing refers to it.
- The UORespawn `SOURCE.txt` still says "0 .cs" and "TERMS: none stated". Correct it to: MUO scripts in the nested zip
  (77 `.cs`), MIT per the GitHub LICENSE. That correction is for whoever keeps the third-party records; this task does
  not edit them.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code clean
docs dry run
```

P104 DONE
