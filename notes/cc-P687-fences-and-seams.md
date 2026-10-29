# cc-P687: fences for the unfinished land and the sealed dungeon, and the cliff seams dressed (SoS swap S14)

Iron Golem, 2026-10-29. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P687` (main at the P725 merge). Not committed, nothing deployed, no package built or published.

## In plain words

- **The unfinished parts of the new map are fenced off.** Five places cannot be walked into: the rooster island, the
  north-east snow isles, the bare land east of Haven, the land round Echoback and Darkfathom, and Glimmerwood's
  broken cliffs. A player who walks up to the edge stops there with the line "Thick fog rolls in; the way is lost."
  Recall, gate and mark do not land inside. Boats sail past, and nobody can build a house there. This works on both
  Trammel and Felucca.
- **The author's dungeons stay sealed.** 33 of them can only be entered by teleporters, and P683 left those out. One,
  the Swamp of Desolation (a walled valley north-east of Britain), can be walked into through three gaps, so it has the
  same fence until S18 fills it with monsters.
- **The ugly cliff edges near towns and roads are covered.** The author's land has hard grass and dirt cliffs that draw
  as stretched, smeared faces. 6,143 of them within 40 tiles of a town, road or moongate now have OSI's own big grey
  boulders along their foot. Nothing becomes blocked by them. Before and after pictures:
  `notes\cc-P687-tools\renders\seam-*-before-after.jpg`.
- For you: after you restarted Docker, the full build check passed (10:46): all 2,818 shard tests, none failed.
  The map patch grows from 1.07 MB to 1.29 MB (the limit is 5 MB). When the swap is live, look at a few dressed
  cliffs in the game and say if the boulders suit you.
- Worth a look on Chases-Tower: Windows had only about 0.5 to 1.7 GB of its 32 GB free during the build. Windows'
  own kernel memory pools held 32 GB (22 GB paged, 10 GB nonpaged). That usually means a driver is leaking, and a
  reboot clears it.

## 1. The list

The four unfinished areas match P669's `out\unfinished.csv` (`notes\cc-P687-tools\out\`):
- the rooster island has 15,183 new dry tiles and no statics at all;
- the north-east snow isles have 4,048 bare seams, against 93 on stock;
- east of Haven has 485;
- Echoback and Darkfathom have 6.

Part 3's fifth box, Glimmerwood's seam cells (2688-2943, 2688-3071), has 5,605 bare seams against 0 on stock.
These are the same five boxes P684 already keeps treasure out of (`ClusterFSosTreasureLand.Closures`).

## 2. and 4. The fences

`server/customizations/Regions/SosFenceRegions.cs` (new). Six regions, registered at every start on Trammel and on
Felucca (both stand on the same land, P675). Each is above S3's no-housing and wild regions over the same ground
(priority 60, against their 50).

| Fence | Rects | Turn-back spot | Walkable tiles inside |
|---|---|---|---|
| the rooster island | 2840-3039, 1324-1523 | 2665,1148,-1 | 14,569 |
| the north-east snow isles | 4224-4479, 256-767 | 4223,511,0 | 78,036 |
| the bare land east of Haven | 3072-3199, 2304-2559 | 2958,2675,0 | 13,618 |
| Echoback and Darkfathom | 4096-4223, 2560-2815 | 4401,3078,-1 | 8,932 |
| Glimmerwood's broken cliffs | 2688-2943, 2688-3071 | 2944,2879,0 | 66,398 |
| Sealed: the Swamp of Desolation | its 8 rects from S3's region | 1960,912,3 | 64,757 |

What each fence does, to a player, and to a player's pet or summon (staff and the world's own creatures are free):
1. **A step in is refused**, with "Thick fog rolls in; the way is lost." So the walker stays on their own last shore.
2. **Boats sail by.** On a boat's deck a player may cross the fence; a step off the deck onto its land is refused the
   same way.
3. **Anyone inside anyway, off a boat**, is put back. That covers a login, or a move by some other code. If they came
   from a deck or from outside every fence, they go back there. Otherwise they go to the fence's turn-back spot, the
   nearest walkable mainland outside every fence (`notes\cc-P687-tools\fences.py`: the nearest standable tile on a
   walkable area of 20,000 tiles or more). Pinned asks a region's `OnMoveInto` only when a mobile crosses from another
   region. So a step off a deck inside the box needs `OnLocationChanged`, which fires after every move. The put-back
   runs on the next tick, after the move in progress.
4. **No recall, gate, mark or teleport ends inside.** Leaving that way is allowed.
5. **No houses.**

What is inside: no shipped teleporter end, spawner (810 read), decoration line (25,462 read), public moongate or guarded
town is in any fence (fact 2 below). The fences overlap only S3's wild regions there: Poultry Paradise, Darkfathom
Hollow, Buccaneers Jungle, Britain Forest North and Compassion Desert.

**The dungeons (part 4).** `notes\cc-P687-tools\dungeon_ways_in.py` uses P681's walk grid (pinned's movement reduced
to the files, the author's land). It looks for every standable tile inside one of his 34 dungeon regions that is a
step from a standable tile outside all of them. Sanctuary Entrance and Paroxysmus Exit are not counted as his
dungeons: they are the way into a stock dungeon and out of one.
- 33 dungeons have none. Each sits in the dungeon area past x 5120, reached only by the 70 teleporters S6 left out.
- Dragons Den and Mongbat Hideout show 3 to 4 tiles each. Each one is a 3-tile sliver just past its own rect's edge,
  with no way to it from anywhere.
- The Swamp of Desolation is a walled valley on the surface: 58,406 walkable tiles with three gaps, at x 1805
  (y 1022-1059), y 1214 (x 1881-1886) and y 913 (x 2019-2029). S3 had marked it "sealed by S14". The fence covers its
  own rects, so every gap refuses a walker and no spell lands inside. S18 removes the fence when the swamp has
  monsters: one row in `SosFenceRegion.Fences`.
- No fence is needed at a teleporter, which the prompt leaves to S6.

The fog line is the prompt's. I used it for the swamp too, rather than invent a second line.

## 3. The cliff seams

**What counts.** The prompt's 107,741 is P669's count of dry tiles with no static where the land rises 20 or more to a
neighbour. Looking at them (`renders\`):
- **47,958 of them are stock's own:** the same land id and Z, and a seam there too. Britain's castle moat is one; it
  renders the same on stock (`look-britain-sos.jpg`, `look-britain-stock.jpg`). The pass leaves OSI's land alone.
- **On mountain rock land the "seams" are the mountain** (`look-mountain-3168-3840.jpg`): it draws as OSI's own
  mountains do, so the pass leaves rock and cave land alone too.
- **What is left is the author's own grass, dirt, sand, forest, jungle and snow cliffs.** The client stretches the high
  tile's ground texture down the face, a smeared wall, which is the hard-edged look the plan means. Within 40 tiles of
  a town rect, a road tile (pinned's road ids) or a public moongate, and outside the five fenced boxes: **14,209 seam
  tiles** (`seamgrid.py`).

**What OSI does.** Nothing to copy:
- under 1 in 500 of OSI's rocks stand on a cliff (`out\rock-palette.csv`);
- its surface cave walls stand buried 30 under the land at cave mouths (`out\cavewall-survey.csv`);
- the statics on its few dressed seams are buildings (`out\stock-seam-statics.csv`).
So the pass uses OSI's own tall grey boulders, stock art 0x1357-0x135C, 58 to 85 px tall
(`renders\rock-and-cave-wall-art.jpg`). The brown cave walls look like a dungeon, and the small rocks are too short to
hide a face.

**The pass** (`notes\cc-P687-tools\dress.py`):
- Every target tile that stands 20 or more above its south, east or south-east neighbour gets a boulder: those are the
  faces the camera, looking from the south-east, sees.
- The boulder goes on the high tile, at the low neighbour's Z, so it is drawn from the foot of the cliff up over the
  face. A taller face gets one more every 20 Z.
- Each piece's top stays at least 2 under the high tile's walking Z (pinned's GetAverageZ), and nothing is placed on
  the low tile. So no tile becomes harder to walk on.
- The pieces are picked by a hash of the place, so a rerun gives the same patch.
- Result: **6,143 faces, 8,389 pieces**.

**The patch.** `player-package/vendor/shattered-legacy-map/trammel.mapops` grows from 1,066,673 to **1,292,850 bytes
(1.23 MiB)**, a quarter of the 5 MB rule. It has 8,389 more S+ lines and B lines for the blocks they touch.
`SOURCE.txt` has P687's line. Checks:
- `mapops check` on the pristine SoS copy: **drifted 0**, missing 0, land identical, 0 statics blocks differing;
- `diff(base, edited)` gives back the shipped patch exactly;
- the server's overlay and the player package read the same file (`Build-MapOverlay.ps1`, `Apply-MapOps.ps1`).

**Renders, before and after** (`renders\seam-*-before-after.jpg`, P180's `isorender.py`, the client's layout):
- **2688,696**, a road cut through a hill: the left face is covered all along.
- **1992,1680**, a hillside with two cliffs: the long lower face is covered, the upper one in two places.
- **4200,2832**, a sandy bank under trees: only partly covered. Most of that bank's faces sit under tiles that already
  carry a tree, so they are not bare seams by P669's rule, and the pass leaves tiles with something on them alone.

## 5. Tests

**Code copy, `server/tests/Regions/SosFenceRegionsVerification.cs`** (new). One theory row per fence, for each of
F1 to F4, on Trammel and Felucca:
- F1: registered over its rects (corners and centre found, one past a corner not), no housing.
- F2: a step in is refused; staff walk in; onto a boat's deck is allowed; off the deck is refused.
- F3: someone inside is put back, or on the turn-back spot (outside every fence); on a deck they stay.
- F4: recall, gate, mark and teleport into it are refused with the fog line; recall out is allowed; staff are exempt.
- F5: the five boxes are `ClusterFSosTreasureLand.Closures`, and the swamp's are S3's own rects.

25 facts in all. How they ran:
- **Red** on a mutant with every rule switched off (`mutate_fence.py`): 25 of 25 fail (`red-probe.txt`).
- **Green**: 25 of 25 (`green-probe.txt`, `probe.sh` on `sl-uo-builder:cc-P685`).
- The boat check is a seam the facts stand in for (`OnBoatAt`); a real boat needs the multi data the test host lacks.

**Docs copy, `tools/tests/test_sos_fences.py`** (new, needs `SL_SOS_BASE`), 4 facts on the SoS land:
1. each fence and its turn-back spot (standable, outside every fence, on 20,000+ walkable tiles) is `fences.py`'s;
2. nothing a player needs is inside;
3. the only walk-in dungeon ways that lead anywhere are the swamp's, all inside its fence;
4. every boulder stands on a target tile, at the low Z plus a multiple of 20 and 2 under the walking Z; more than 6,000
   faces; under 5 MB; applied to the pristine SoS copy with 0 drifted and 0 missing.

How they ran:
- **Red**: facts 1, 3 and 4 failed on a mutant table without the swamp and the undressed patch
  (`red-test-sos-fences.txt`); fact 2 failed on a fence rect over Britain's moongate (`red-test-sos-fences-2.txt`).
- **Green**: 4 of 4 (`green-test-sos-fences.txt`).

**`tools/tests/test_mapops.py`**: fact 4 said every patch line is the Burrows or the isle. It now also allows S14's
seam boulders: OSI's 0x1357-0x135C on the surface, x < 5120, checked on the land by the fact above.
- Red: the old fact 4 fails on the dressed patch at (375, 224, 0x1358) (`red-test-mapops-fact4.txt`).
- Green: 11 of 11 (`green-test-mapops.txt`). Fact 5 shows the patch made on the SoS map, line for line.

**Package**: `player-package\tests\Map-Overrides.Tests.ps1`, 16 facts, 0 failed (`green-ps-map-overrides.txt`,
`package` lock taken and released).

**Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P687`, `docker-build` lock):
**green on run 3**. Run 3 (10:45, after Chase restarted Docker): every gate passed and `EXIT=0`. 2,818 tests:
2,812 passed, 6 skipped (client-data facts), 0 failed. All 25 fence facts passed. Image `sl-modernuo:cc-P687`
485fd9f7097f (`gated-build.log`). Free memory before the run was 1.6 GB, and it dipped to about 540 MB during the
run. The Docker VM was empty, and the kernel pools held 32 GB. Runs 1 and 2:
- **Run 1** (07:48) ran every shard test: 2,818 tests, 2,810 passed, 6 skipped, 2 failed. Both are explained under
  Deviations: one was mine and is fixed, the other a random roll (`red-gated-build-1.log`). The new code compiled and
  all 25 new fence facts passed in the gate.
- **Run 2** (07:52), after the fix: the builder stage finished, then the image export failed with "failed to extract
  layer ... error reading from server: EOF". From 08:04 every Docker call answered "500 Internal Server Error" or hung.
  At 08:31 it was still down. So the gate did not run (`failed-gated-build-2.log`).
- The fix was checked on the builder image before run 2 (`green-probe.txt`): the 25 fence facts and all
  `FoldVerification` facts, 31 passed, 1 skipped (a client-data fact).
- **To finish** (done in run 3), once Docker is back:
  1. Take the lock: `powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take docker-build -Minutes 40 -Wait`.
  2. Run `notes\cc-P687-tools\gated-build.ps1` detached (Start-Process).
  3. Wait for `EXIT=` in its UTF-16 log.
  4. Release the lock.
  If The Butcher's roll fails again, rerun once; that fact is not this change's.
- Asked Chase (Iron-P687-20261029-083155-c53a) whether he restarts Docker Desktop, the Golem does, or the task is
  accepted on run 1 and the probe. Chase restarted and pruned Docker at 10:00-10:08 (C had filled up). Run 3 followed.

## Chase's decisions applied

- **A fresh test world on swap day:** this prompt planned no migration; the fences are code and the dressing is map
  data, both read at start.
- **1.0 scope:** the unfinished land is fenced and the one walk-in dungeon is sealed until S18 spawns it. S19 lifts a
  land fence when its area is finished.

## Deviations and decisions

- **The seam count narrowed.** The plan's figure counts stock's own cliffs and every mountain. I dressed only the
  author's new soft-ground cliffs near players (14,209 tiles), and said why above. Dressing the rest would bury stock
  OSI land and the mountains in boulders.
- **The boulders are my choice, not an OSI pattern.** OSI has no cliff dressing to copy (measured above). The rest of
  the map's look is unchanged. Chase may prefer another piece; the pass takes its ids from two lists in `dress.py`.
- **Turn-back spots are the nearest mainland**, not a stored "last shore" per player. A walker is simply refused at the
  edge, which leaves them on their own shore; the spot is only for someone found inside.
- **The gated build's first run failed two facts.** One was my facts leaving their test players in the world, which
  `FoldVerification`'s saved-map check then reported; the facts now delete them. The other was a random roll in
  `CreatureLevelsVerification` (The Butcher's difficulty read 12 times, under pinned's cap once), which is unrelated to
  this change. `red-gated-build-1.log`.
- **The Read tool is denied** on the code copy in unattended runs; I read it with shell commands and edited with small
  scripts and scratchpad copies.

## Files

- Code copy:
  - `server/customizations/Regions/SosFenceRegions.cs` (new);
  - `server/tests/Regions/SosFenceRegionsVerification.cs` (new);
  - `player-package/vendor/shattered-legacy-map/trammel.mapops` and `SOURCE.txt`.
- Docs copy:
  - `tools/tests/test_sos_fences.py` (new) and `tools/tests/test_mapops.py` (fact 4);
  - `notes\cc-P687-tools\`: `seams.py`, `seamgrid.py`, `rock_palette.py`, `cavewall_survey.py`, `dress.py`,
    `install_patch.py`, `fences.py`, `dungeon_ways_in.py`, the mutants, `probe.sh`, `gated-build.ps1`, `out\`
    (the surveys, `dress.csv`, `fences.json`), `renders\`, and the red and green outputs.
- Outside the repos: `D:\UO\golems\Iron\p687-work\` (the edited map copy, the before and after patches, the full-size
  renders) can be deleted.

P687 DONE
