# cc-P188: Rootdeep goes in (the way in from Old Haven, spawners, the real map write)

Gold Golem, 2026-10-20. Prompt: `D:\UO\cc-prompts\claimed\Gold\cc-P188-cont-rootdeep-goes-in.md`. Branch
golem/Gold/P188 in both repos. Image `sl-modernuo:cc-P188`. Continues P167 (sections 2 and 3), P180, P181, P185;
Chase approved the round 4 renders 2026-10-19 14:46.

## Headlines

- **The Burrows and the way in are in the map, as a patch of our own changes.** The package never ships a byte of
  EA's (Chase's client policy, 2026-10-02; `Build-PlayerPackage.ps1` gate 4), so the "map override" is the map-ops
  patch cc-P40 designed and measured: `player-package\vendor\shattered-legacy-map\trammel.mapops` (252 KB, 11,320
  land cells, 1,597 statics added, 3 removed, 211 blocks fingerprinted), made by `scripts\mapbuild\mapops.py` from the
  pristine 7.0.117.0 files and the scratch build, shipped as `app\trammel.mapops`, and applied on each player's PC by
  `app\Apply-MapOps.ps1` (PowerShell 5.1, no inline C#) into `app\uo-overrides\` at launch, the same way as our
  tiledata and cliloc. The server reads the same map from `client-data\sl-map-overlay\`, built by
  `docker\uo\Build-MapOverlay.ps1` with the very same applier and mounted first in the test shard's data folders.
  Three independent checks agree byte for byte: the Python applier rebuilds the scratch build exactly, the PowerShell
  applier writes the same three files as the Python one (synthetic facet and the real Trammel), and the shipped
  patch's every line is inside the Burrows or the way in.
- **The way in is one collapsed stretch of wall.** Before any change the hole sat in a sealed pocket of the ruins:
  2,614 tiles reachable on foot from the hole, none of them New Haven, walled on every side by ruined walls (50
  one-tile cuts in the walk's rectangle; the whole list is in section 1). Three single ruined-wall pieces (0x0281,
  height 20) came out of the Second Bank's south wall at 3618-3620,2622; the tiles either side keep OSI's own rubble
  piles, so it reads as a collapsed stretch. The hole 0x1B71 is on 3619,2620 (Z 0, the bank's wooden floor), the
  rope ladder 0x08A6 leans on the Landing's north wall at 5193,1131, and the seeder places the two teleporters: the
  hole down to the arrival 5193,1138, the ladder's foot 5193,1132 up to 3619,2621 beside the hole. The walk from New
  Haven's east edge is 131 steps; no step of it is inside any undead spawner's walking box, and the hole is one tile
  outside the nearest (3635,2625, walk 15).
- **The skeletons stay; the crier goes at its source.** Spawner (113) is untouched and a fact imports the real
  `post-uoml/trammel/Outdoors.json` to prove it is placed and spawns ten skeletons. The town crier is pinned's own:
  `shared/trammel/TownsPeople.json` "Spawner (123)" at 3652,2619 (the P167 prompt said it was not in pinned's files;
  cc-P42 had already found it there). The import hook that already drops stock Despise creatures now refuses that
  one spawner by its guid (`ClusterFOldHavenStockSpawns`), so a fresh world never places it, and
  `[ClusterFOldHavenRetire` deletes it and its crier from a world that has it.
- **No client on this PC, so the test-shard walk is Chase's**, with the whole route rendered step by step and the
  shard's side proven in the test host (section 6). What the test shard does prove here without a client: it starts
  on the new image with the map overlay mounted first, and `status.json` now carries `world.rootdeepMap`, the
  seeder's own test of the Landing's land, which reads `true` only when the shard reads our Trammel (section 7).
- **Not done here, and why (section 9):** the player package build (this PC has no TazUO build to package; the
  gates and the applier are tested, the build is the game PC's), `[ClusterFSeedRootdeep` and `[ClusterFOldHavenRetire`
  on the test world (in-game commands; the seeder's and the retire's effects are the facts W1 and W5), and the client
  walk. Publishing is Chase's step as the prompt says.

## 1. The way in (prompt 1; P167 section 2)

### The survey

The scratch map was rebuilt first: `D:\UO\cc-p167-work\` did not exist on this PC (P167 to P185 ran on the game PC),
so `scratch-client\` was made from the shard's pristine copies (their SHA-256 are P167's `ORIGINAL-SHA256.txt`:
872269bb, 2109d96b, d7ae4bfc), the art unpacked with the new `scripts\mapbuild\uop2art.py` (43,760 entries), and
`build_burrows.py --fresh` run: `statics-placed.csv`, `land-summary.csv` and `build-report.json` came out identical to
round 4's committed files (only CRLF differed; the files were restored from git). 1,595 statics, 11,320 land tiles,
verify 0 mismatches, the walkable gate green.

The walk (`notes\cc-P188-tools\build_way_in.py`, class `Walk`): a flood fill on foot over x 3536-3664, y 2556-2652
with pinned `Movement.cs`'s rules reduced to what the map files decide (land Impassable or Wet blocks; a static that is
Impassable and not a Surface and overlaps the walker's 16 Z blocks; a Surface raises the standing Z; a step up over
StepHeight 2 blocks; land Z from the four corners' average). From New Haven's east edge (3545,2580, where pinned's New
Haven region ends; cc-P189 measured from the same spot; the tile itself is a wall, the nearest open tile is 3545,2579)
the hole was not reachable. From the hole, 2,614 tiles were, none west of x 3608: a pocket closed by

| Side | What closes it (tiles that touch both the pocket and the New Haven side) |
|---|---|
| north, y 2564-2565 | jungle walls 0x3EF2-0x3F04 at x 3622-3642 and a stone wall with a portcullis 0x06F5 at 3630-3635,2565 |
| east, x 3642-3680 | the intact buildings' walls (0x3EF9 jungle, 0x001B/0x001C stone, 0x0226/0x0008 wooden), y 2566-2655 |
| the bank's west wall, x 3615 | ruined walls 0x0279-0x0282 and stone 0x0057/0x0064, y 2611-2621 |
| the bank's south wall, y 2622 | 0x0058 at 3616, rubble piles 0x0277/0x0278 at 3617 and 3621-3623, **0x0281 at 3618, 3619, 3620** |
| south-west, x 3623 | ruined walls 0x0282/0x027A/0x027C/0x0279, y 2632-2637 |

(50 cuts in all; `notes\cc-P188-tools\walk-report.json` lists every one with its static.) That is what Chase saw on
10-18: "the area around the hole is blocked off by broken buildings".

### What changed in the map

The cheapest natural opening is the bank's own south wall: the ground south of it (dirt at Z 0, x 3586-3622, y
2623-2631) is already on the New Haven side, and the three pieces are single, identical, full-height ruined walls
between two of OSI's rubble piles.

Statics removed (`notes\cc-P188-tools\statics-removed.csv`):

| x | y | z | id | what |
|---|---|---|---|---|
| 3618 | 2622 | 0 | 0x0281 | ruined wall, the bank's south wall |
| 3619 | 2622 | 0 | 0x0281 | ruined wall, the bank's south wall |
| 3620 | 2622 | 0 | 0x0281 | ruined wall, the bank's south wall |

Statics placed (`statics-placed.csv`):

| x | y | z | id | what |
|---|---|---|---|---|
| 3619 | 2620 | 0 | 0x1B71 | the hole (tiledata "hole", passable, height 0; the teleporter down stands on it) |
| 5193 | 1131 | 0 | 0x08A6 | rope ladder, leaning on the Landing's north wall (Bridge + Surface, height 22, so it is on the wall tile, not the floor; the teleporter up stands on the floor tile at its foot, 5193,1132) |

The ladder is on the wall tile on purpose: a Bridge piece of height 22 stands the walker at Z 11 (pinned
`Movement.cs`, CalcHeight halves a bridge), which is over StepHeight, so a ladder on a floor tile could not be
stepped onto and the teleporter under it would never fire. The pieces were chosen from a render of fourteen
candidates (hole, sinkholes, rope, rope ladders, tall ladder, wooden ladders, dirt, rocks); 0x08A5 leans west, 0x08A6
north.

After the change the hole is reachable: 131 steps from 3545,2579, along the mansion's north wall (y 2580), down x
3571, east along y 2603 and 2608, through the ruins' west gap at 3605-3614 x 2611, south along x 3614 to 2623, east
to 3619,2623 and north through the gap. Pinned's undead by the walk, from `Outdoors.json` (cc-P189's table):

| Spawner | Path tiles inside its walking box | The hole |
|---|---|---|
| Skeleton x7 at 3635,2625 (home 8, walk 15) | 0 | 1 tile outside its box (x 3620 is the box's west edge; the gap's east tile 3620,2622 is inside it) |
| Spawner (113), Skeleton x10 at 3651,2627 (home 8, walk 15), kept | 0 | outside |
| Zombie x10 at 3625,2594 (walk 15) | 0 | outside |
| Zombie x10 at 3649,2591 (walk 15) | 0 | outside |

So a new player meets, on the way in, whatever has wandered to the edge of those boxes: the 3635 skeletons can walk
into the bank through its open north-east corner (3624-3628 x 2609) or the new gap's east tile, and stand on the hole
room's floor; a Young player is attacked by none of them (Haven Island is Young-protected, cc-P189). The hole and the
ladder's foot are both inside cc-P189's Old Haven Training rectangle (x 3546-3703, y 2543-2650; fact W1 and W2).

### Renders

`notes\art\rootdeep-build\way-in.html`, linked from the top of `index.html`: `way-in.png` (the bank before, EA's
file, and after, side by side), `way-in-close.png` (the gap and the hole), `walk-overview.png` (the walk in radar
colours, the shortest path on foot in yellow, the undead spawners in orange), `landing-return.png` (the Landing before
and after, the ladder on the north wall). 1.0 MB in all; nothing over 5 MB in either repo (`find -size +5M`: nothing).

### The checklist and the junction sheet

Nothing walled was built: three pieces of an OSI ruin came out and two passable or wall-mounted pieces went in, so
the playbook's wall checks have nothing to check (no diagonal runs, one piece per tile, junctions by the run rule all
concern wall tiles we place; the gap's two ends are OSI's rubble piles, which are not run pieces). The Burrows' own
checklist is unchanged from round 4 (the rebuild is identical, above). The ladder sits on a wall tile that already
carries its north-edge piece 0x0242; a ladder is not wall-flagged, so the one-wall-piece rule holds.

## 2. The spawners (prompt 2)

- **Spawner (113), 10 Skeletons at 3651,2627: kept.** Nothing excludes it; fact W4 imports the real file and watches
  it spawn. Its walking box (x 3636-3666, y 2612-2642) does not reach the hole (3619) or the gap (3618-3620).
- **The town crier, "Spawner (123)" at 3652,2619.** Source: pinned's `Distribution/Data/Spawns/shared/trammel/
  TownsPeople.json` (guid `8b75bcf8-7b83-4d94-8573-92aff88cd41f`, one TownCrier, 5 to 10 minutes, home 1, walk 5);
  the same file has every other town's crier. Stopped where it enters a world: the import hook
  (`server/patches/ImportSpawners-despise-exclusion.patch`, the one line that asks `ClusterFDespiseStockSpawns.Admit`
  now also asks `ClusterFOldHavenStockSpawns.Admit`, which refuses that guid on Trammel). The patch applies after the
  guid-key patch (checked with `git apply --check` on a copy of pinned's file, then by the build).
  **Alternatives to editing the patch:** (a) a second patch on the same hunk cannot apply after the first; (b)
  chaining through `ClusterFDespiseStockSpawns.Admit` would hide an Old Haven rule inside a Despise class; (c) editing
  pinned's json is never allowed. One `||` on the existing line, with a comment, was the smallest change.
- **Removing it from a world that has it:** `[ClusterFOldHavenRetire [dryrun]` (cc-P189's command) now also finds the
  crier spawner by its guid, or by its spot and single TownCrier entry for one placed before guids were kept, anywhere
  on Trammel (it stands at y 2619, south of the seeder's X 3520-3680, Y 2420-2600 box), and deletes it with its crier
  (fact W5). The command is already on the console's red list; its summary names the crier now.
- **Not run on the test world here** (an in-game command; no client on this PC): For Chase, dry run first.

## 3. The seeder (prompt 3)

`[ClusterFSeedRootdeep [dryrun | force]` gains the two teleporters (`ClusterFRootdeepSeeder.Teleporters`): stock
`Teleporter` items (pinned `Items/Misc/Teleporter.cs`: invisible, Active, players only, no delay, no effect), placed
where missing and counted in the result (`SeedResult.Teleporters`), skipped on a re-run like the rest; nothing new is
saved. The down teleporter is on the hole tile and `OnMoveOver` cancels the step onto it; the up one is at the ladder's
foot. `MapBuilt()` (the arrival tile's land is not void) still gates the command, so on a shard without the map
overlay it still refuses. **Not run on the test world here** (no client); fact W1 and V5 are the seeder's proof, and
`status.json` `world.rootdeepMap` shows the gate's answer on a running shard.

## 4. The real map (prompt 4; P167 section 3)

### Why a patch and not the files

Chase's client policy (`notes\client-policy-2026-10-02.md`): the package carries our changes and applies them to EA's
files on the player's machine; our download server never hosts EA's files. `Build-PlayerPackage.ps1` gate 4 refuses
any `.mul` or `.uop` in the zip. cc-P40 B.2 measured three formats for exactly this map and recommended map ops
(byte-identical result, auditable, and it reported EA changing a block under it where bsdiff silently corrupted one).
So "the package's map overrides" is that pipeline, built here for the first time:

| Piece | Where | What |
|---|---|---|
| `scripts\mapbuild\mapops.py` | docs repo | `diff(base, edited, facet)` makes the patch (one line per changed land cell `L x y tile z`, per static added `S+ x y z id hue`, per EA static removed `S- x y z id hue`, and a `B block fingerprint` per touched block); `apply` is the reference applier; `check` applies to a scratch copy and compares with the edited files; `synthetic_facet` for tests |
| `player-package\vendor\shattered-legacy-map\trammel.mapops` + `SOURCE.txt` | shard repo | the patch: F 1 211; 11,320 L, 1,597 S+, 3 S-; 251,905 bytes, 13,134 lines, ASCII, LF |
| `player-package\payload\app\Apply-MapOps.ps1` | ships in `app\` | `Build-MapOverride -UoDir -Ops -OutDir`: Jenkins lookup3 for the UOP entry names, the chunk table, land cells written in place in a copy of the player's `map1LegacyMUL.uop`, statics blocks rewritten at the end of a copy of `statics1.mul` with the index repointed, the fingerprint check (one yellow line per drifted block, patched anyway), a removal EA moved reported and left, a stamp (`map-stamp.txt`: the three EA files' size and time and the patch's hash) that makes every later start a skip. PowerShell 5.1 only: no Add-Type, no inline C#. Two traps found and written down in it: `0xFFFFFFFF` and `0xDEADBEEF` parse as negative Int32 literals, so the masks are decimals |
| `Build-UoOverrides.ps1` | `app\` | a fourth part, `Build-Map`, after art, worn-item art and text; its three override lines (`map1legacymul.uop=`, `statics1.mul=`, `staidx1.mul=`, lowercase as TazUO keys them) join `files-override.txt`; any failure is one yellow line and the game starts without the map, as the other parts |
| `Build-PlayerPackage.ps1` | the build | stages the patch as `app\trammel.mapops` (checked byte for byte in gate 3); a map gate (`Test-MapOps`) on the vendored file before staging and again in gate 4 on what shipped: ASCII, no BOM, LF, one F line naming facet 1 with the right B count, every other line L, S+ or S- with every number in range, and `app\Apply-MapOps.ps1` present |
| `docker\uo\Build-MapOverlay.ps1` | the server | applies the same patch with the same applier to copies of the shard's pristine files into `client-data\sl-map-overlay\` (git-ignored by `.gitignore:34 client-data/`, proven with `git check-ignore`); `docker-compose.test.yml` mounts it at `/var/lib/uo/client-data/sl-map-overlay` and `Start-TestShard.ps1` rebuilds it on every start and puts it first in Configuration-test's `dataDirectories` (pinned `Core.FindDataFile`, `Main.cs:346-372`, takes the first folder that holds a file) |

Measured here: the PowerShell applier patches the real Trammel in 1.2 s cold and its three files hash exactly as the
Python applier's (`134de278`, `2a6bb0c7`, `de0be747`); the test-shard overlay is 116 MB.

### The package build

Not run on this PC: `Build-PlayerPackage.ps1` packages our own TazUO build (`D:\UO\tazuo-sl-build\client` with its
`sl-build.txt`, cc-P124), which is made from a TazUO clone that is only on the game PC; the client gate refuses
anything else. Everything the build does with the map is covered without it: the map gate is proven on the vendored
file and on four bad files (BOM, non-ASCII, a wrong facet, a wrong B count, a bad line), both scripts parse, and the
applier the zip would carry is the one tested in section 6. For Chase: Shard Console > Player package > Build, then
Publish, on the game PC.

### The test shard

See section 7.

## 5. What changed, file:line

`D:\ShatteredLegacy`:

| File | Change |
|---|---|
| `server/customizations/ClusterFOldHavenStockSpawns.cs` (new) | the crier spawner's guid, `Admit`, `CrierStock`, `FindCrierSpawner` |
| `server/patches/ImportSpawners-despise-exclusion.patch` | the hook line asks both `Admit`s; the hunk is `-253,6 +253,17` now |
| `server/customizations/ClusterFRootdeepSeeder.cs` | header; `TeleporterRow`, `Hole`, `LadderFoot`, `BesideHole`, `Teleporters`; `SeedResult.Teleporters`; the loop in `Seed`; `PlaceTeleporter`, `FindTeleporter`; the command's text |
| `server/customizations/ClusterFOldHavenSeeder.cs` | `Retire` takes the crier spawner too; the command's text |
| `server/customizations/Regions/OldHavenBurrowsRegion.cs` | `ProvisionalEntrance` is `HoleEntrance`, confirmed (one reference in `ApprenticeTraining.cs`'s comment and one in the Vault facts followed) |
| `server/customizations/ShardStatusPublisher.cs` | `Render(..., bool rootdeepMap = true)` writes `world.rootdeepMap`; `Publish` passes `ClusterFRootdeepSeeder.MapBuilt()` |
| `docker/uo-status/README.md` | the field |
| `server/tests/Regions/RootdeepWayInVerification.cs` (new) | W1 to W5 (section 6) |
| `server/tests/Regions/RootdeepVaultVerification.cs` | V5 counts the teleporters; `HoleEntrance` |
| `server/tests/Misc/ShardStatusPublisherVerification.cs` | the `world` keys and the flag both ways |
| `player-package/payload/app/Apply-MapOps.ps1` (new), `Build-UoOverrides.ps1`, `Build-PlayerPackage.ps1`, `vendor/shattered-legacy-map/` (new), `tests/Map-Overrides.Tests.ps1` (new) | section 4 |
| `docker/uo/Build-MapOverlay.ps1` (new), `docker-compose.test.yml`, `Start-TestShard.ps1` | section 4; `Start-TestShard.ps1` also gains `-NoMapOverlay` (an empty overlay, the shard reads EA's Trammel: the control in section 7, and a way to see what the patch adds) |
| `CHANGELOG.md`, `VERSION` | 2026.10.20.12 (2026.10.20.11 was committed) |

`D:\UO\shard-migration`:

| File | Change |
|---|---|
| `scripts/mapbuild/uofiles.py` | `remove_statics` |
| `scripts/mapbuild/mapops.py` (new), `scripts/mapbuild/uop2art.py` (new) | section 4; the art unpacker |
| `notes/cc-P188-tools/build_way_in.py` (new), `statics-removed.csv`, `statics-placed.csv`, `walk-report.json` | section 1 |
| `notes/art/rootdeep-build/way-in.html`, `way-in.png`, `way-in-close.png`, `walk-overview.png`, `landing-return.png`; `index.html` | the pictures; the link at the top of the page (`render_burrows.py` `page`) |
| `tools/tests/test_mapops.py` (new) | section 6 |
| `notes/map-building-playbook.md` | section 6 of the playbook: the way in, holes and the map patch (added below in this task) |

No saved type changed: `Teleporter` is pinned's, the spawner data is pinned's, the regions have no saved data. No
version bump, no migration.

## 6. Tests and gates

Every new fact was seen red first. Server facts: built and tested only through `docker/uo/build.sh` (docker-build
lock taken and released each time).

**Red run** (`build.sh --tests-only -t sl-modernuo:cc-P188-red`, with four production files mutated by
`red.py` in the session scratchpad and restored after: the hook's guid set to Spawner (113)'s so the crier is admitted
and the skeletons refused; `PlaceTeleporter` never called; `Retire` blind to the crier; the Vault's region one column
short; and `ShardStatusPublisher` with the new parameter but not the field):

| Fact | Red (the mutated tree) |
|---|---|
| W1 teleporter, both ends | `Assert.NotNull` failed: no teleporter on the hole |
| W2 region rectangles | the Vault's region read 5142-5177, not the floor's 5142-5178 |
| W3 the crier's source gone | the crier spawner was placed by the import |
| W4 Spawner (113) still spawns | `Assert.Single` failed: the skeleton spawner was not placed (refused by the mutated hook) |
| W5 retire takes the crier | the crier's stock row was not found (the mutated guid), a null reference |
| V5 the seeder (P141) | the teleporter count and the Vault's crawlway litter from W1's red run (W1 now cleans up before it asserts) |
| V1, V2 the Vault's rectangle and doorway (P141) | red with the mutated Vault region, as they should be |
| status `rootdeepMap` | the `world` keys were `lastSaveAt` only |

1,629 tests: 1,616 passed, 9 failed (the nine above), 4 skipped; "ShatteredLegacy.Tests tests did not pass. No image
was built."


**Green**: `build.sh -t sl-modernuo:cc-P188`: 1,629 tests, 1,625 passed, 0 failed, 4 skipped; "Built sl-modernuo:cc-P188 with patches applied and 1625 shard test(s) passing" (image ad642abb5bac). The first green run failed two of my own facts on their expectations, not the code: W3 assumed over 100 spawners in the Trammel townspeople file (it holds 48) and W2 assumed the Burrows region began at the built land (it begins four tiles west, x 5136, P36's rectangle); both expectations were corrected to the measured values and the build rerun.

| Fact | What it proves |
|---|---|
| W1 teleporter, both ends | the seeder places both, on the hole and at the ladder's foot, pointing at the arrival and beside the hole; a player who steps on each is moved to the other end and the step is cancelled; a skeleton is not moved; both ends sit in the regions they should (Old Haven Training, the Burrows); a re-run places neither again; V5 counts them |
| W2 region rectangles match the built floors | the Vault's region is exactly the Vault floor extent of the approved layout; the Burrows' region holds every zone's floor with its wall ring, the built land's extent (x 5140-5245, y 1131-1261) and the ladder's wall tile; the hole is outside both and inside Old Haven Training; the region's Entrance is the hole |
| W3 the crier's source is gone | the shipped `TownsPeople.json` still holds the crier spawner (3652,2619, one TownCrier); a real import of the file places every other spawner of it and not that one; `Admit` admits every one placed |
| W4 Spawner (113) still spawns | a real import of `Outdoors.json` places it at 3651,2627 with its 10 Skeleton entry, both hooks admit it, and `Respawn` gives 10 skeletons inside its home range |
| W5 retire takes the crier | with the crier spawner and the skeleton spawner in a world, the dry run deletes nothing and names the crier; the real run deletes the crier spawner and its crier, keeps the skeletons and their ten |
| status: `world.rootdeepMap` | the key is there and true when the map is built, false when not |

**Map patch facts** (docs repo `tools/tests/test_mapops.py`, 5 of 5; PowerShell `player-package/tests/
Map-Overrides.Tests.ps1`, 7 of 7): the diff is exactly the change and the Python applier rebuilds the edited files
(land byte for byte, statics block by block, EA's file a prefix of the output, an emptied block unlinked); a drifted
block is reported and patched, a moved removal reported and left; the PowerShell applier writes the same bytes as
the Python one and skips on its stamp; the shipped patch is the Burrows and the way in only and rebuilds the scratch
build exactly; and on the PowerShell side with numbers written out: the entry-name hash against three values from the
Python port, a land line's three bytes and nothing else, statics rows after EA's with the index repointed, the stamp
skip and a new patch rebuilding, drift and a missing removal reported, no patch no lines, a missing chunk an error.
Seen red: the PowerShell hash first came out wrong three times (the Int32 hex-literal trap, a swallowed
initialisation, a swallowed header line in the test's own UOP writer), each caught by the Python cross-check or a
fact before the applier touched a real file; the block arithmetic in two facts was wrong first (the fact caught the
fact).

**The map gate** (`Test-MapOps`): pass on the vendored file; red on a bad B line, an unknown line, a wrong B count, a
BOM, non-ASCII bytes and a Felucca F line (run from the session scratchpad with the function extracted from the
build script).

**Other suites**: `Build-UoOverrides.Tests.ps1` cannot run on this PC (its setup stops at "the encoded animation files
are missing: run python scripts\build-equip-anims.py first", before any fact; unrelated to this change).
`tools\progress.py --dry-run`: 1131 customization files, 110 patches, 1068 tests in 180 files before this task's
new test file.

## 7. The test shard

Test shard on this PC, under the test-shard lock, `Start-TestShard.ps1 -Image sl-modernuo:cc-P188` (it rebuilt the
overlay, stamp unchanged, and put `/var/lib/uo/client-data/sl-map-overlay` first in Configuration-test's
`dataDirectories`, then `/var/lib/uo/client-data/classic-client`):

- healthy on port 2594; `docker exec ... ls` shows the three overlay files (89,965,543; 20,405,063; 5,505,024
  bytes) and the stamp inside the container;
- the first `status.json` (30 s up): `"version": "2026.10.20.12"`, `"world": { "lastSaveAt": null, "rootdeepMap": true }`;
- the log: "Automatically detected client version 7.0.114.40" (this PC's `.env` points the test shard at the 7.0.114
  copy, deviation 10), "Restricting client version to 7.0.117.0 or newer", "Loading maps done", listening on 2594;
  no exception.

**The control, seen red:** the same image started with the new `-NoMapOverlay` switch (an empty overlay folder is
mounted in the same place): healthy, and `status.json` reads `"rootdeepMap": false`. So the flag follows the map the
shard reads, and the overlay is what makes the Landing's land not void.

Both shards were stopped afterwards (`-Down`); nothing else on this PC ran. `Start-TestShard.ps1` tagged the image
`sl-modernuo:good-7653de2-dirty` on the first healthy start, as it always does.

Not done here: walking it. This PC has no TazUO, no EA client and no play-test bot, so the walk from New Haven to the
hole, the drop, the Vault doorway for a tutorial and a non-tutorial character, the crawlway, the zones and the way
back up are the play-test chunks in section 8; every step has its render (section 1, `way-in.html`, the round 4 zone
pictures in `index.html`) and its fact (W1 walks a player through both teleporters, W2 the regions, V2 the doorway's
refusals, V3 the crawlway).

## 8. Play tests for Chase (P115 format)

Test shard, `sl-modernuo:cc-P188`, after the package is built and published and the test shard started by
`Start-TestShard.ps1` (which builds the overlay). First, as Administrator, in game:

```
[ClusterFSeedRootdeep dryrun
[ClusterFSeedRootdeep
[ClusterFOldHavenRetire dryrun
[ClusterFOldHavenRetire
```

The seed dry run says "would place 33 spawners, 1 ankh, 1 crawlway, 2 teleporters" on a world that has none; it
refuses with "The landing is still void land" if the shard did not read the overlay (then check `status.json`'s
`world.rootdeepMap`).

**Chunk 1, the walk in (10 minutes).** Who: you, a fresh (Young) character. Where: New Haven, walk east. Do: from New
Haven's east edge go east along the mansion's north wall, then south through the ruins' west side to the Second Bank
(the roofless wooden-floored room at 3616-3625 x 2610-2621); enter through the collapsed stretch of its south wall
(3618-3620,2622); step on the dark hole at 3619,2620. Pass: you land on the Landing (5193,1138) with the Echo's dungeon
warning; the ankh is on the east wall; the rope ladder on the north wall; nothing attacked you on the way (skeletons
may be standing in the bank room: they ignore a Young character).

**Chunk 2, the Vault doorway (5 minutes).** Who: you, twice: a tutorial character (in the core) and one who is not.
Where: the Landing. Do: walk west to the doorway at x 5179, y 1137-1138. Pass: the tutorial character walks in; the
other is refused with "The Vault is for the League's trainees..." (P141-3 and P141-4 become playable here: the
Counting Room's bats, the Stacks' rats, the Deposit Hall's three decoy chests).

**Chunk 3, the Overdraft and the crawlway (15 minutes).** Who: you, the tutorial character. Where: the Strongroom.
Do: kill the Overdraft; go to the rocks in the south wall at 5160,1159 and double-click or step on. Pass: the
crawlway opens for 2 minutes, you come out in the Crawl Den at 5160,1163, the Vault seals behind you (P141-7 becomes
playable).

**Chunk 4, every zone (20 minutes).** Who: you, any character (staff is fine). Where: from the Landing's tunnel south.
Do: Warren (Crawl Den, Tunnel Foot, Great Burrow), the Brood Pit through its mouth at x 5209-5211, the descents to the
Tangle and the Dawnseam, the Thicket and Seam Heart gaps, the Gloom ring, the lair mouth at x 5183. Pass: every zone
reachable on foot, every spawner's creatures inside their room, no wall piece out of line (the round 4 renders are
the reference).

**Chunk 5, the way back up (3 minutes).** Who: you. Where: the Landing. Do: step on the floor tile at the foot of the
rope ladder (5193,1132, against the north wall). Pass: you stand beside the hole in the bank (3619,2621); walk out
through the gap south and back to New Haven.

**Chunk 6, Old Haven's spawners (3 minutes).** Who: you, staff. Where: Old Haven, 3652,2619 and 3651,2627. Do: after
the retire command, look for a town crier near the bank's east side; count skeletons by 3651,2627. Pass: no crier,
no crier spawner (`[props` on the tile finds nothing); skeletons still spawn from Spawner (113).

## 9. Deviations and decisions for Chase

1. **The ladder sits on the wall tile, not the floor** (section 1): a Bridge piece of height 22 cannot be stepped
   onto from the floor, so it is a wall decoration and the teleporter is on the floor tile at its foot.
2. **The way in is the south wall, not the west wall or the north-east corner.** The west wall's pieces are stacked
   (three per tile at 3615,2617) and the north-east corner opens onto the pocket, not New Haven. Three identical
   single pieces out of the south wall was the smallest change; say if you want the gap wider or elsewhere.
3. **No third-party art** (P167 D6, otimpyre's X-6 cave hole was the natural piece): the stock hole 0x1B71 reads as a
   hole in a wooden floor and needs no registration; X-6 is still an option if you want a bigger, rougher one.
4. **The map ships as a patch, the server reads an overlay.** The prompt's "write the scratch map and statics into the
   package's map overrides" had no existing path (nothing shipped a map before); this is cc-P40's design, built. On
   the game PC: `Start-TestShard.ps1` makes the overlay itself. For a live shard (there is none now: retired
   2026-10-14 until the fresh 1.0 world) the same two lines go in `docker-compose.yml` and the live
   `modernuo.json`'s `dataDirectories` at a restart you plan, and `Build-MapOverlay.ps1` runs first.
5. **`status.json` has one new field**, `world.rootdeepMap` (schema 1, additive; README updated). It is how a shard
   without the overlay is seen without logging in. Nothing about players is in it.
6. **`GoLocation` stays at 5191,1195** (P141-D6: moves to the arrival "if Chase wants it"). One line.
7. **The crier is excluded by guid**, read from the shipped file, so an upstream change that renumbers the file is
   seen by fact W3 (it loads the real file).
8. **`ProvisionalEntrance` is renamed `HoleEntrance`** now that it is confirmed; two references followed.
9. **The package build and the three in-game steps are not done here** (no TazUO build and no client on this PC).
   The facts and the renders stand in for them; the chunks above are the live proof.
10. **The 114 and 117 question**: this PC's `.env` points the test shard at `client-data\classic-client` (7.0.114);
    the overlay is built from the 7.0.117.0 copy, so the test shard here reads 117's Trammel and 114's everything
    else. P24 measured 114 and 117 identical across the Burrows rectangle and the bank room, so the walk is the same;
    the game PC's test shard reads 117 throughout (P36).

## For Chase

1. **Approve the way in** (`notes\art\rootdeep-build\way-in.html`): the gap, the hole, the ladder. Say if the gap
   should be wider, elsewhere, or the hole bigger.
2. **Build and publish the package** (Shard Console > Player package: Build, then Publish): it now carries
   `app\trammel.mapops` and `app\Apply-MapOps.ps1`; a player's first launch after the update patches copies of their
   own map files (about 116 MB more under `app\uo-overrides\`, one yellow line if EA changed a block under us).
3. **Rebuild the test shard** (`Start-TestShard.ps1 -Image sl-modernuo:cc-P188`, or the console's Rebuild): it builds
   the map overlay from your client data and mounts it. Check `status.json` reads `"rootdeepMap": true`.
4. In game, as Administrator: the four commands at the top of section 8, dry runs first.
5. The play-test chunks in order.

## Repo size

No file over 5 MB in either repo (`find -size +5M` over both, outside `.git`, `client-data`, `server/uo` and
`server/lib`: nothing). The scratch map (115 MB), the unpacked art (149 MB) and the server overlay (116 MB) are outside
the repos or git-ignored (`client-data/`, `.gitignore:34`, proven with `git check-ignore`). The session scratch
(the red tree's saved files, the synthetic facets, the probes) is in the session scratchpad.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

(code: 21 files pending, among them the new vendor folder, the applier, the overlay script and the facts; docs: 18,
the pictures, the tools, this note and the playbook. Neither repo BLOCKED; nothing over 5 MB; the dry run's own
`tools/progress.json` refresh is in the docs list. Its "prompts with a finished note" lines name P180, P181 and
P185, whose notes end in PAUSED by design.)

P188 DONE
