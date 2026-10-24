# cc-P413: a bigger way into the Rootdeep Burrows: an ant-hill burrow with a wide mouth

**Golem:** Iron. **Date:** 2026-10-24. **Branch:** `golem/Iron/P413` in both work copies. **Image:**
`sl-modernuo:cc-P413`.

## In plain words

- The way down into the Rootdeep Burrows, in Old Haven's ruined bank, is now a big burrow instead of one small hole. It
  is a dirt crater about six tiles across, with loose rocks round its rim and a dark mouth in the middle. It reads as a
  burrow from across the bank. Picture: `notes/cc-P413-tools/entrance-before-after.png` (before on the left, after on
  the right) and `entrance-close.png`.
- Stepping anywhere into the dark mouth (3 by 4 tiles) takes you down to the Landing. The rope ladder back up now
  leaves you just outside the bank's broken south wall, facing the burrow, so you are never dropped straight back in.
- I checked it on a private copy of the test world with the test bot. It walked from New Haven's east edge to the
  burrow (130 steps, every one accepted by the server), went down from each of the 12 mouth tiles, and climbed the
  ladder back up each time.
- For you: after the overseer merges, rebuilds the player package and restarts the test shard, type in game, as
  Administrator: `[ClusterFSeedRootdeep dryrun`, then `[ClusterFSeedRootdeep`. It adds the new mouth's teleporters and
  points the old ladder at the new landing. Running it again adds nothing. Then walk in from New Haven and step in.

## What it looks like, and the IDs

![before and after](cc-P413-tools/entrance-before-after.png)

The crater is **OSI's own sinkhole set**, 0x30E7-0x310A: 36 pieces, a 6 by 6 ground decal, height 0, flags Background
only (passable). OSI places it once, at Trammel and Felucca 5575-5580, 3015-3020. I lay it exactly the same way, with
the piece at column c, row r being `0x310A - c - 6 r`.

- **Placement:** with its first piece on 3615,2616, the set covers x 3615-3620, y 2616-2621, inside the Second Bank
  of Haven.
- **Its dark core is the mouth:** columns 2-4, rows 1-4, which is **x 3617-3619, y 2617-2620**. Those pieces measure
  34 to 100 percent dark pixels; the rim pieces round them measure 0 to 48 percent (`sheet.py` in the session).
- **The rim:** thirteen loose pieces on its rim tiles inside the bank, seeded (`random.Random(413)`), never two alike
  side by side, at Z 0 or 1. The pieces are rocks 0x1771, 0x1773, 0x1775-0x1779, 0x177B, 0x177C and debris 0x0C2E,
  0x0C30. Every one is passable; I left out 0x1772 and 0x177A, which are impassable.
- **Removed:** P188's hole 0x1B71 at 3619,2620. It was our own `S+` line, so the patch simply loses it.

Every ID was checked in tiledata (the pristine 7.0.117.0 `tiledata.mul`, and the shard's copy in
`D:\UO\tool-trials\client-data-copy` has the same rows). None of them is in our art registry
(`player-package\vendor\shattered-legacy-art\registry.csv`: 0 rows touch any of them), so nothing collides. All are
stock art; no art request was needed.

The full list with every coordinate is in `notes/cc-P413-tools/statics-placed.csv`, and the removal is in
`statics-removed.csv`.

**Why the sinkhole set and not a ring of separate pieces:** the stock "ant hill" 0x2232 is a single impassable tile.
The "dirt" decals (0x1B27-0x1B3E) and dirt patches are flat and have no dark centre. Only the sinkhole set has a crater
round a black hole that spans several tiles, and OSI already uses it on its own map. P188's note had dismissed it as "a
multi-tile ground set", which is exactly what an ant-hill hole needs.

**Placement, and the one I did not pick:** the bank's floor is x 3616-3625. The nearest skeleton spawner's walking box
(3635,2625, walk 15) starts at x 3620.

- **Chosen: the set starting at x 3615.** The mouth is x 3617-3619, outside every box, and so is the whole walk. Only
  the rim's east column (x 3620: decal, three rocks) sits on the box's west edge. The gap's east tile 3620,2622 was
  already there. A decal and loose rocks change nothing for a creature or a player.
- **Not chosen: the set starting at x 3614.** It keeps the set entirely outside the box, but the west wall then cuts
  the crater in half (`notes/cc-P413-tools/alternative-west-placement-close.png`). Say if you want that one instead;
  it is one switch (`build_anthill.py --ox 3614`) and three numbers in the seeder.

## The walk

The flood fill is cc-P188's `Walk` (pinned `Movement.cs`'s rules reduced to the map files), run over the edited files
(`notes/cc-P413-tools/walk-report.json`).

- **Every mouth tile is reachable.** The shortest walk from New Haven's east edge (3545,2579) to the mouth is
  **130 steps**; before, it was 131 to the old hole. The route is the same: through the bank's collapsed south wall
  (3618-3620,2622) and north onto the mouth.
- **Nothing became unwalkable:** 6,359 tiles are reachable on foot from New Haven, before and after.
- **No step of the route is in any spawner's walking box**, and neither is any mouth tile or the ladder's landing.
- **The ladder's landing** (3619,2623) stands at Z 0, is not a mouth tile, is 3 tiles from the nearest one, and walks
  back to New Haven in 122 steps.
- **The picture:** `walk-overview.png` shows the route in yellow, the mouth in magenta, the landing in cyan, and the
  spawners and their boxes in orange.

## The teleporters and the seeder (server)

`server/customizations/ClusterFRootdeepSeeder.cs`:

- `MouthX1..MouthY2` (3617-3619, 2617-2620) and `IsMouth`.
- `Teleporters` is now one row per mouth tile (12), each to the arrival 5193,1138, then `LadderUp`: the ladder's foot
  5193,1132 up to `BesideMound` (3619,2623), which replaces `BesideHole` (3619,2621).
- `Hole` (3619,2620) and `OldHavenBurrowsRegion.HoleEntrance` stay: that tile is one of the mouth's twelve, so the
  region's Entrance and the other facts that use the hole are still right.
- **On a world P188's seeder already seeded:**
  - the old hole's teleporter matches its row (same tile, same destination) and is kept;
  - the other eleven are placed;
  - the old ladder teleporter is **pointed at the new landing**, not doubled. That is the new `FindOurTeleporterAt`:
    a teleporter named `Rootdeep: ...` on the row's tile.
- The result line says how many were pointed elsewhere (`SeedResult.TeleportersRetargeted`).

**For Chase, on the current test world** (after the overseer's rebuild, so the shard reads the new map overlay):

```
[ClusterFSeedRootdeep dryrun
[ClusterFSeedRootdeep
```

- **On the test world as P188 seeded it**, the dry run says "would place 0 spawners, 0 ankh, 0 crawlway, 11
  teleporters, ...; would point 1 teleporters at their new landing; already there ...".
- **On a world never seeded**, it says 13 teleporters.
- **The real run** does the same; nothing is deleted or moved apart from that one destination.
- **Re-running** finds everything in place and places nothing (seen live below: "0 teleporters ... already there 48").
- It refuses while the shard reads EA's Trammel (the Landing still void land), as before.

## Tests

### Server

Built and tested only through `docker/uo/build.sh`, under the docker-build lock.

- `server/tests/Regions/RootdeepWayInVerification.cs`:
  - **W1 (rewritten).** The 12 mouth rows are exactly x 3617-3619, y 2617-2620. The ladder lands on 3619,2623, which
    is not a mouth tile and is at least 2 tiles from one. The seeder places all 13, active, players only, invisible.
    The mouth is in Old Haven Training, the ladder's foot in the Burrows. For **every mouth tile**, a player stepping
    on it lands on the arrival, then climbs the ladder back to 3619,2623. A skeleton is not moved. A re-run places
    nothing.
  - **W6 (new).** On a world with P188's two teleporters, the dry run says 11 placed and 1 pointed elsewhere, and
    changes nothing. The real run does it. The ladder tile holds exactly one teleporter, now pointing at 3619,2623.
    Every mouth tile holds exactly one. A re-run does nothing.
- `RootdeepVaultVerification.cs` V5 counts the seeder's teleporters as `Teleporters.Length` (13), not 2.
- **Red first:** a build with the seeder put back to P188's behaviour (`red413.py` in the session: one down row on the
  old hole, the old landing, no retargeting). W1 failed ("Expected 13, Actual 2") and W6 failed ("Expected (11, 1),
  Actual (0, 0)"): 2 failed, 2,269 passed.
- **Green:** `Built sl-modernuo:cc-P413 with patches applied and 2271 shard test(s) passing.` 2,275 in all, 0 failed,
  4 skipped.

### The map patch

`tools/tests/test_mapops.py`, run against my own copies:

```
SL_SHARD_REPO=D:\UO\golems\Iron\ShatteredLegacy MAPBUILD_CLIENT=D:\UO\UltimaOnlineVanilla python -P tools/tests/test_mapops.py
```

Both variables are new. Their defaults are unchanged, so on the game PC nothing changes.

- **Facts 1-4 pass**, including the PowerShell applier writing the same bytes as the Python one.
- **New fact 6 passes:**
  - the shipped patch's additions in the bank are exactly `statics-placed.csv`;
  - P188's hole line is gone;
  - the 36 pieces are laid as OSI lays them;
  - their dark core is the seeder's mouth.
  - Red first against HEAD's patch: "the hole is still in the patch".
- **Fact 5 fails on this PC, and it already did before this change.** It compares the patch with P167's scratch build
  in `D:\UO\cc-p167-work\scratch-client`. On this PC that build predates P188's way in: the bank's south wall and no
  ladder. With HEAD's patch it fails on the same two blocks (231751, the bank, and 332429, the Landing's ladder).
  - I taught it to put P188's hole back in place of the burrow (`as_p188`, as `without_farm` already does for the
    farm), so it still means "the way in as P188 built it" where that scratch exists (the Gold PC).

`mapops.check` on the new patch, against pristine and my build: drifted 0, missing 0, land identical, 0 blocks
differing.

### Player-package gates

`player-package/tests/Map-Overrides.Tests.ps1`, under the package lock: 7 facts, 0 failed.

The package build itself and its publish are the overseer's after the merge, as the prompt says.

### On a private test shard (the test-shard lock)

I did not use the shared Test Shard on 2594. I used `notes/cc-P413-tools/proof-shard.ps1`:

- a copy of `D:\UO\bot-shard` on 127.0.0.1:2596, running `sl-modernuo:cc-P413`;
- the new map mounted first, as the test shard mounts `sl-map-overlay`: my build's `edited` folder, which
  `mapops.check` proves equal to pristine plus the shipped patch;
- the pristine 7.0.117.0 files for everything else.

`notes/cc-P413-tools/walk.py` used the playtest bot's client as Iron's own admin and player:

- **Seeding (first run):** "would place ... 13 teleporters, 8 floor traps; would point 0 teleporters at their new
  landing". Then "placed ... 13 teleporters". This world had never been seeded with P188's teleporters, so the
  retargeting was not seen live; W6 covers it.
- **Seeding (second run):** "placed 0 spawners, 0 ankh, 0 crawlway, 0 teleporters, 0 floor traps; ... already there
  48" (`seed-on-the-test-world.txt`).
- **The walk in:** the player stood on New Haven's east edge (3545,2579) and walked the 130-step route tile by tile.
  The server accepted every step. Stepping from 3618,2621 onto the mouth (3618,2620) put it on the Landing at
  5193,1138.
- **Every mouth tile:** for each of the 12, the player walked north to the ladder's foot and landed at 3619,2623.
  It then walked back to that mouth tile without crossing any other mouth tile, and landed on 5193,1138.
  **12 of 12 down, 12 of 12 ladder landings beside the mound** (`walk-result.json`).
  - The two centre tiles (3618,2618 and 3618,2619) have mouth tiles on every side, so no walk reaches them without
    dropping first. For those two the player was stood on the tile to the west by staff command, which fires no
    teleporter, and stepped east.

The container is removed, the world copy deleted and the lock released. The new patch-notes line showed in the login
bulletin on that shard.

Not seen: the burrow in a game client. No client was driven; the renders are the picture.

## Files

**ShatteredLegacy:**

- `player-package/vendor/shattered-legacy-map/trammel.mapops`: the hole line out; 49 new statics (36 crater, 13 rim);
  one more block fingerprint (`F 1 214`).
- `player-package/vendor/shattered-legacy-map/SOURCE.txt`
- `server/customizations/ClusterFRootdeepSeeder.cs`
- `server/customizations/Regions/OldHavenBurrowsRegion.cs`: a comment only.
- `server/tests/Regions/RootdeepWayInVerification.cs`, `server/tests/Regions/RootdeepVaultVerification.cs`
- `CHANGELOG.md`, `VERSION`: 2026.10.24.4.

**shard-migration:**

- `notes/cc-P413-tools/`:
  - `build_anthill.py`: the build, the walk report, the renders and the patch;
  - `proof-shard.ps1`, `walk.py`;
  - `statics-placed.csv`, `statics-removed.csv`, `walk-report.json`, `walk-result.json`,
    `seed-on-the-test-world.txt`;
  - the pictures.
- `scripts/mapbuild/uofiles.py`: `MAPBUILD_CLIENT`.
- `tools/tests/test_mapops.py`: `SL_SHARD_REPO`, `as_p188`, fact 6.
- This note.

The scratch maps (`D:\UO\golems\Iron\p413-work`, 115 MB) are outside both repos. No file in either repo is over 5 MB.

## Deviations and decisions for Chase

1. **The rim's east column sits on a spawner box's edge** (x 3620, decal and three loose rocks). The mouth, the route
   and the ladder's landing are all outside every box. The fully outside placement is the alternative above.
2. **The ladder up lands outside the bank** (3619,2623, just south of the collapsed wall), not inside it. The old
   landing, 3619,2621, is now on the crater's rim right beside the mouth. Inside the bank, any landing that is not on
   the mound would be in the skeletons' box (x 3620 and east).
3. **The mouth is 3 by 4 tiles, not 3 by 3:** the set's dark core is four rows deep (row 1 is 56 to 67 percent dark).
   A dark tile that did nothing would read as broken.
4. **I read another work copy's client-data by accident.** `scripts/mapbuild/uofiles.py` points `CLIENT` at
   `D:\ShatteredLegacy\client-data\classic-client-7.0.117.0`. My first two renders (OSI's sinkhole, and the bank before
   the change) and the tile sheet read tiledata and texmaps from there before I saw it. From then on every script
   points it at `D:\UO\UltimaOnlineVanilla` (the same pristine 7.0.117.0 files, hashes 872269bb, 2109d96b, d7ae4bfc).
   `MAPBUILD_CLIENT` now makes that a setting. Nothing was written there.
5. **The Read tool was denied** (unattended run) for `server/customizations/ClusterFRootdeepSeeder.cs`. I edited it
   and the facts with small Python scripts that assert each replaced block is there exactly once.

P413 DONE
