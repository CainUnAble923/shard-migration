# cc-P661: the Fold, map 32, its rules and the copy pool's indexes (P481 F1)

## In plain words

- The new player isle now has a world of its own on the server: "the Fold", plus 16 private copies of it for trainees.
  Each one shows Trammel's map to the client, so players need no new files. Nobody can get there yet; nothing changes
  for players today.
- On the Fold you cannot place a house, recall, mark a rune or cast a gate in or out, and it is always daylight. If
  anyone ever ends up on the matching empty patch of Trammel, they are sent to New Haven.
- Staff on the test shard can visit with `[Fold goto 0` (the Fold) to `[Fold goto 16` (copy 16), optionally with x y.
  It is refused on the live shard.
- Nothing for you to do. The isle itself is drawn in P662.

## What was built (code work copy, branch golem/Iron/P661)

| File | What |
|---|---|
| `server/customizations/Fold/FoldMaps.cs` | Registers map 32 "TheFold" and 33 to 48 "TheFold 1" to "TheFold 16" in `Map.Maps` and `Map.AllMaps`: client id 1, file index 1, Trammel's width and height, season 0, `TrammelRules`. `Configure` runs at `[CallPriority(3)]`: after pinned's `MapLoader.Configure` (2) and before `TileMatrixLoader`, regions and `World.Load` (`Main.cs:667-671`). Running it twice changes nothing. If a JSON entry has already taken a reserved index, it logs an error and leaves that map in place. The header says indexes 32 to 48 are reserved for good. |
| `server/customizations/Fold/FoldRegions.cs` | `FoldRegion` (a `NoHousingRegion`): `CheckTravel` refuses every type for players (the Green Acres model), `AlterLightLevel` sets day. `FoldMirrorRegion` on Trammel over void C (x 6160-6639, y 1832-2279): a non-staff player who enters is sent, with pets, to the New Haven start (`CharacterCreation`'s start city, 3503, 2574, 14); travel into it is refused for players. |
| `server/customizations/Fold/FoldCommands.cs` | `[Fold goto <n> [x y]`, GameMaster, test shard only (`TestCenter.Enabled`, refused otherwise). n 0 is the Fold, 1 to 16 a copy; default spot the arrival beach (6214, 2001); Z is the land average. |
| `server/customizations/Fold/FoldSavedMapCheck.cs` | At `Initialize` (after `World.Load`): names in the log every player, creature or item a save left without a map (an unregistered index), and gives a lost player a way back to the New Haven start. Nothing is deleted. Silent when there is nothing to find. |
| `server/customizations/ClusterFAnkhs.cs` | The ankh survey skips the Fold's maps, which would list Trammel's ankh statics 17 more times. |
| `server/tests/Regions/FoldVerification.cs` | 7 facts, below. |
| `CHANGELOG.md`, `VERSION` | 2026.10.26.11, one Staff line. |

Design (shard-migration): section 3.1 of `cc-P481-new-player-start-area-design.md` now records that 32 to 48 are
reserved for good, and the zone-region rule below.

### One decision that differs from the design: the rules are each map's default region

The design (3.1) said "one `FoldRegion` per zone". The first build registered one region over each whole map. That made
the 7 facts take **4 minutes 2 seconds** in the test host, against 2 seconds for the same facts on stubs. A registered
region is added to every sector it covers, and 7168 x 4096 is 114,688 sectors a map, 1.95 million on 17 maps.

So the rules are each Fold map's **default region**, which `Region.Find` returns wherever no registered region lies
(`Region.cs:291-311`; pinned has `Region.IsDefault` for it). No sectors are made. The facts then took 3 seconds.
**For F2 to F4:** every zone region added on the Fold must take `FoldRegion.On(map)` as its `Parent`.
`BaseRegion.CheckTravel` defers to the parent (`BaseRegion.cs:171-175`) and `HousePlacement`'s `IsPartOf` walks
parents, so the zone keeps the rules. A zone region with no parent would lose them.

## Facts (`FoldVerification`), red first

Red: the same test file against stubs with the same public names and no behaviour (`FoldMaps.Configure` does nothing,
`IsFold` is false, the regions register nothing, `Run` returns nothing, `Goto` returns ""). They ran in a throwaway
`sl-uo-builder:cc-P659` container (the branch's base, `28a2093`) with the vanilla client mounted. **7 of 7 failed.**
Green: the real files, same container: **7 of 7 passed** with client data, and 6 passed plus 1 skipped without it.

| Fact | What it pins | Red on the stubs |
|---|---|---|
| `MapsThirtyTwoToFortyEightAreRegisteredOnTrammelsFiles` | 32 to 48: names, index, client id 1, file index 1 (read by reflection), Trammel's size, season 0, `TrammelRules`, once each in `AllMaps`; 49 free; a second `Configure` adds nothing | `Assert.NotNull() Failure` |
| `APlayerOn32And40StandsOnTrammelsTileAndZ` (real data only) | At 3503,2574, 3503,2573 and 6214,2001, a player on 32 and on 40 stands at Trammel's Z on Trammel's land tile, with Trammel's statics. Seen: land 0x03E9 Z 14; 0x03FC Z 14 with statics 0x0B24 and 0x0D33 at 14; void 0x0244 Z 0 | `NullReferenceException` |
| `HousingRecallMarkAndGateAreRefusedOnTheFold` | On 32 and 40: the region at both corners is `FoldRegion` and is the default region; `HousePlacement.Check` is `BadRegion` for a player and `Valid` for staff; recall, gate and teleport in, recall and gate out, and mark are refused for a player (stock messages 1019004, 501035, 502361, 501802) and allowed for staff; light is `DayLevel` | `IsType() Failure ... Actual: typeof(Server.Region)` |
| `APlayerFoundOnTrammelsMirrorIsSentToNewHaven` | The mirror's exact corners; not on the Fold; recall into it refused; a player inside is at the New Haven start one timer tick later, staff stay | `IsType() Failure` |
| `ASaveAndReloadKeepsACharacterOnMapForty` | Serialize a player on 40 and load it as a new mobile: its way back (`LogoutMap`, `LogoutLocation`) is 40 at the same spot, and logging in there puts it on 40 inside `FoldRegion` | `NullReferenceException` |
| `AnUnregisteredIndexInASaveIsReportedNotCrashedOn` | With 40 taken out of `Map.Maps`, a saved player and item load **without an exception** (pinned's own behaviour: `Map.Maps[index]` is null). The check names both, the player's way back becomes New Haven, the item is kept | `Assert.Contains() Failure` (no report) |
| `FoldGotoIsForStaffOnTheTestShardOnly` | Refused when not a test shard; usage for 17, -1 and a bad verb; 1 goes to 33 at the beach, 0 to 32, `8 6300 1990` to 40 there; out-of-map x y refused | `Strings differ` |

The real-data fact runs only with client files, so the gate skips it, as it skips the 4 `MapCheckRealDataVerification`
facts. It was run by hand with `D:\UO\UltimaOnlineVanilla` mounted read-only and `MODERNUO_TEST_DATA_DIR` set
(cc-P135's method).

## Memory and file handles (part 4)

Measured in the builder's test host with the vanilla client mounted (a scratch fact, kept as
`notes\cc-P661-tools\FoldMeasure.cs.txt`, never committed). Each line is the change from the line before. Managed
memory is `GC.GetTotalMemory(true)`; private bytes and RSS are the process; handles are `/proc/self/fd`.

| Step | Managed | Private bytes | RSS | File handles |
|---|---|---|---|---|
| Baseline: Trammel open, Fold not registered | 45.7 MB | 310 MB | 201 MB | 311 (3 on Trammel's files) |
| 17 maps registered, none touched (`Configure`: under 1 ms) | +75 KB | +0 | +88 KB | +0 |
| The Fold (32) opened | +45 KB | (noise) | (noise) | +3 |
| 16 empty copies opened | +718 KB | +25.4 MB | +21.3 MB | +48 (3 each) |
| The isle's drawn area (272 x 145) read on all 17 | +2.3 MB | +1.7 MB | +2.0 MB | +0 |
| One copy with the farm seeded (P276's addon moved whole, door, Farmhand, both spawners filled) | +480 KB | +156 KB | +1.4 MB | +0 |

- **Registering costs nothing.** A map opens its three Trammel files only when its tiles are first read (`Map.Tiles` is
  lazy). Every open copy holds 3 handles: 51 for all 17.
- **Opening is slow, once.** Opening the Fold took 416 ms and the 16 copies 5,813 ms, about 360 ms each. Most of it is
  `TileMatrix` hashing its three files (`TileMatrix.cs:154-159`) and reading the UOP index. It happens on the main
  thread the first time anything reads a copy's tiles. No startup step reads them (the private shard loaded its world
  in 2.8 s). **For F4:** either open the pool at startup (about 6 s added to boot) or accept a one-time 0.4 s stall
  when a copy is first used.
- **Unmanaged memory is about 1.5 MB per open copy** (UOP entries and file buffers). Cached blocks are shared between
  matrices on one file (`TileMatrix.cs:79-86`): reading the isle area on 17 maps added 2.3 MB managed.
- **A seeded farm is small:** +341 items (the addon's components among them) and +8 mobiles (the Farmhand and the
  spawned pests and pen animals), +0.5 MB managed.

## The private-world shots (part 5), `notes\cc-P661-tools\`

A private shard (`proof-shard.ps1`, container `sl-p661-proof`, image `sl-modernuo:cc-P661`, 127.0.0.1:2596, a copy
of the bot-shard world), under the `test-shard` lock. The shared Test Shard on 2594 was not touched. `proof2.ps1`
(P265's `proof.ps1`, changed to log in **both** of Iron's characters at once in two TazUO windows) ran the scenes in
`scenes.json`. Its log is `proof-log.txt`.

| Shot | Shows |
|---|---|
| `1-voidC-32-33-after-save-restart-player.jpg` / `-admin.jpg` | Iron the Tester put on 32 and Iron (Admin) on 33 by `[Fold goto 1`, both at 6214,2001. Then `[save`, a container restart (the server logged "The Fold: registered 17 maps" again, then loaded the world in 2.35 s with no saved-map warning), and both logged in: each window is black, Trammel's void C. The login gumps cover the middle. |
| `2b-newhaven-32-33-player.jpg` / `-admin.jpg` | Both at 3503,2574: the Tester on 32, the Admin on 33. Each sees Trammel's New Haven plaza (its statics), with **no NPCs or items**, since those are Trammel's and the Fold is another world. Neither sees the other. The Tester is a ghost (grey view; it was killed in scene 3's first run, below). The Admin, a GM who would see a ghost on the same map, does not see it. |
| `3-control-trammel-felucca-player.jpg` / `-admin.jpg` | The control. The Tester on **Felucca** at the same spot sees wild Felucca land (land 0x0006, not New Haven): a map the client took as Felucca would look like this. The Admin on real Trammel sees the same plaza as 2b, now with Trammel's NPCs and items. |

Scene 2's first try caught the Tester's client still on "Logging into Shard" after 30 s. That shot was dropped, and the
scene was rerun as 2b with 50 s. Felucca's spot is wild land, and the Tester was killed there on the scratch world (the
"died for the first time" achievement in shot 3). `[global call Resurrect` is not a command, so 2b shows a ghost. The
scratch world was deleted afterwards.

## Build

The gated build with `-t sl-modernuo:cc-P661`: **green, `EXIT=0`.** 2655 tests: 2650 passed, 0 failed, 5 skipped (the
4 usual `MapCheckRealDataVerification` facts and `APlayerOn32And40StandsOnTrammelsTileAndZ`, which needs client data
and passed by hand above). The 6 other Fold facts are among the passed. `sl-uo-builder:cc-P661` and
`sl-modernuo:cc-P661` were built under the `docker-build` lock, which is released.

## For the next prompts (F2 to F4)

- Zone regions on the Fold take `FoldRegion.On(map)` as `Parent` (above).
- `TutorialIslandGate.IsOnIsland` knows only Trammel's Haven and the Burrows. A trainee moved onto the Fold is not "on
  the island", and a move from Haven to the Fold would be refused for a loop-0 player (P605 risk 4). F3 adds the Fold
  to it.
- The copies' names have a space ("TheFold 1"). `[set ... Map` takes the index (`Map 33`), since `Map.Parse` accepts
  one (`Map.cs:1768-1800`).
- First use of each copy costs about 0.4 s on the main thread (above).
- `[Fold goto` is test shard only. Whether staff get it on the live shard is a later call.

## Not verified

- A real player-package client: the shots used TazUO from `D:\UO\tazuo-sl-build\client` with the vanilla client
  files. The isle is still void until F2, so there is no painted-tile proof yet.
- Player-driven travel on a running shard (a recall rune, a gate scroll) on the Fold: the facts call
  `SpellHelper.CheckTravel` and `HousePlacement.Check` directly.
- The memory figures are from the test host (Linux container, .NET 10), not the live server under load.

## Asked, and commit preflight

- Nothing asked of Chase. Haven was not touched. Nothing deployed.
- Both work copies are on `golem/Iron/P661`. Not committed (the Golem commits).
- Code: `CHANGELOG.md`, `VERSION`, `server/customizations/ClusterFAnkhs.cs` changed; `server/customizations/Fold/`
  (4 files) and `server/tests/Regions/FoldVerification.cs` new.
- Notes: this file, `cc-P481-new-player-start-area-design.md` (3.1), and `notes\cc-P661-tools\`: 6 JPEGs (1.2 MB in
  all), the scripts and the scene list, the scratch measurement fact as `.txt`, and the proof log (no passwords). No
  file over 5 MB. `docs\` untouched.

P661 DONE
