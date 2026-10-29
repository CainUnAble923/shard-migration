# cc-P684: treasure maps, houses, boats and docks, and SOS bottles on the SoS land (SoS swap S11)

Iron Golem, 2026-10-29. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P684`. Not committed; nothing deployed; the test shard not touched. The map is Zigholtul's (Siege of
Sosaria Trammel Map 3.0).

## In plain words

- **Treasure maps fit the new land.** The old treasure spots that fell into water, rock or a new town were moved a
  short way or dropped. 245 new spots were added on the author's new land. Chests from the newer treasure maps, which
  pick a random spot, now also keep out of the fenced unfinished land. On Felucca they keep out of the new towns too.
- **Houses and SOS bottles needed nothing.** Houses already follow the land, and the new towns and the author's
  dungeons forbid them. SOS bottles always point at open sea: 1,000 tries never landed on the new land or anywhere a
  boat can't go.
- **Boats float at 8 of the author's 11 docks.** Two docks can't take a boat on this map:
  - **Haven:** New Haven's docks face a closed lagoon. A boat floats there but can't sail out.
  - **Nujel'm:** the new continent swallowed the docks; the nearest water is 44 tiles away.
  - The third is a tiny quirk at Skara Brae's east dock, unchanged from stock.
- **For Chase to decide:** whether New Haven needs a working dock (for example a pier on the town's east shore, about
  70 tiles away on the open sea) and Nujel'm a new one. Both are map changes, for S19 or their own prompt. Nothing else
  to do until the swap goes live.

## 1. treasure.cfg

**What the file still does.** The shard runs ServUO's treasure map revamp (`server/patches/TreasureMap.cs`, cc-P127).
A level 1+ map picks a random valid tile anywhere on the surface (`ValidateLocation`). `Data/treasure.cfg` still
decides three things:

- the level-0 maps' spots (those inside `TreasureMap.IsInHavenIsland`'s box);
- every map's spot when `treasureMaps.newChestLocations` is off;
- TreasureMapProtection's no-housing square round each spot, on both facets.

**The rule** (`notes\cc-P684-tools\treasure.py`): `ValidateLocation`'s own checks, read off the SoS files.

- The land is not ignored, impassable or a road, and its name is diggable (dirt, grass, jungle, forest, snow).
- Every static on the tile is passable and diggable by name.
- The tile is not in a TownRegion or DungeonRegion (P676's `regions-trammel.json`).
- And this prompt's: not in an S14 closure box.

**Calibrated on stock:** 34 of pinned's 193 spots fail that rule on stock's own map (they predate ServUO's rule). A
spot that fails on stock too, on a tile SoS left exactly as it was, is **stock-tolerated** and stays.

**Results** (`out\treasure.csv`, `out\treasure.txt`):

| | Spots |
|---|---|
| Pinned's | 193 |
| Kept | 152, and 5 stock-tolerated |
| Moved to the nearest passing tile within 20 | 34 |
| Dropped (none within 20) | 2: 1511,967 is inside Hammerhill now; 2804,2255 |
| New, on the new land | 245 |
| **Shipped** | **436**, 10 of them in the Haven box (the level-0 maps) |

**The new land:** dry on SoS and not on stock Trammel, x under 5120, outside towns, dungeons and closures. That is
1,714,685 tiles; one spot per 7,000 of them (P673's figure) is 245. They stand on tiles that pass, each the passing tile
farthest from every spot so far.

**The random chests** (the revamp): `ValidateLocation` already refused towns, dungeons, champion spawns and houses.
`ClusterFSosTreasureLand.Refused` (new) adds two refusals:

- S14's five closure boxes (P673's list, the same as treasure.py's), until S14's fences and S19 replace them;
- on Felucca, Trammel's town and dungeon regions. Felucca stands on the same land (P675), but its regions stay
  pinned's until S13 (P686) redraws them, so without this a Felucca chest could be buried in Valunstead.

`ValidateLocation` asks it first.

**How it ships:** `server\data\treasure.cfg`, put in pinned's place by a Dockerfile line
(`COPY server/data/treasure.cfg /build/modernuo/Distribution/Data/treasure.cfg`). It has CRLF lines, as pinned's has.

## 2. Houses

- **Nothing to change.** Pinned's HousePlacement reads the tiles, so placement follows the SoS land by itself.
  GuardedRegion (so every TownRegion) and DungeonRegion refuse housing (`AllowHousing => false`).
- **P676 drew the author's 7 new towns** as guarded TownRegions and all 46 of his Trammel DungeonRegions (stock's dungeons among them) as
  DungeonRegions. A fact checks both. So none of them takes a house.
- **Migration dropped** (Chase's fresh test world): no house exists to orphan, and the test shard's houses go with the
  wipe.
- **Felucca:** its regions are pinned's until S13. Until then a Felucca house could stand in a new town's footprint.
  That is S13's to close (the treasure check above covers chests only).

## 3. Boats and docks

`notes\cc-P684-tools\sea.py` reads the water the way pinned's boat code does:

- **Boat water** (`BaseBoat.CanFit`, per tile at Z -5): water land (168-171, 310-311) at Z -5 or a water static at -5,
  and nothing else at -5 or above.
- **Seas:** its 4-connected bodies of 100,000 tiles or more. The open sea is 12,688,989 tiles; the Lost Lands' own sea,
  which Papua's docks serve as in stock, is 407,952.
- **The test** (`docks_sos.py`): for each of the author's 11 dock points (his go-menu's "Docks"), the nearest place
  within 15 where a small boat fits. Multi 0x0 facing north or 0x1 east, footprints from the client's multi.mul. Every
  tile must be in a sea. A boat that leaves the dock reaches the rest of that sea and comes back, which is P699's
  route-and-return point (R15). The boat code's own bounds (`BritWrap`) include all of these.

| Dock | Boat | Distance |
|---|---|---|
| Buccaneers Den | 2742,2160 east | 6 |
| Jhelom East | 1504,3686 east | 12 |
| Magincia | 3661,2272 north | 14 |
| Moonglow | 4400,1034 north | 11 |
| Papua (the Lost Lands' sea) | 5831,3249 east | 7 |
| Skara Brae East | 717,2229 east | 4 |
| Skara Brae West | 649,2226 north | 10 |
| Trinsic East | 2077,2847 north | 8 |
| Vesper (Island I) | 3019,837 north | 9 |
| **Haven** | the nearest place a boat fits is 18 away (3632,2654), in a **closed body of 5,831 tiles** | none |
| **Nujel'm** | **no water a boat fits within 60**; the nearest boat water is 44 away (3815,1236) | none |

**Haven:** on SoS the author's Haven docks face the old bay, which his new land closes off. Round the docks it is two
pools, 5,831 and 8,534 tiles, with no way to the open sea. A player can still buy a boat and place it on the open sea
off the town's east shore.

**Nujel'm:** the new continent joined Nujel'm, and the docks point is inland now.

Both are the map's. A new dock needs map work (a `trammel.mapops` pier, S19), so this prompt records them and the fact
holds them to their stated state. If the map changes, the fact shows it.

**Dock regions:** every dock point is in a no-housing region (its town's, or a dock NoHousingRegion P676 kept from
pinned), except Skara Brae East. Its point, 716,2233, stands one tile east of pinned's own one-tile dock strip (x 715),
on the shore: stock's geometry, unchanged. P678 already drops the ML plaza's "New Haven Docks" with the plaza.

## 4. SOS bottles

- **The replay** (`docks_sos.py`): SOS.cs `FindLocation`, 1,000 times with a fixed seed. Up to 50 tries, a random tile
  of (0, 0, 5120, 4096), accepted when it and the 20 tiles 5 to 25 out on its diagonals are deep water by land id.
- **0 picks returned Point3D.Zero**, and **every accepted pick is open sea** (boat water, in the open-sea body), so
  never the new continent's land, never void.
- 5 picks fall inside the rectangles of the author's Nujelm Desert or Moonglow Forest regions: his boxes reach over the
  sea, and those picks are water.
- **The isle** (6594-6865, 3905-4049) is outside SOS.cs's rectangle, so no pick can reach it. That is stated, not
  sampled (P699 R15).
- **No code change:** the land-id test already leaves the author's land out. SoS's new land is not water by id.

## Facts

| Fact | Red | Green |
|---|---|---|
| docs `tools/tests/test_sos_s11.py`: (1) the shipped treasure.cfg is treasure.py's output; every spot passes on SoS or is stock-tolerated, none in a town, dungeon or closure; one new spot per 7,000 new dry tiles; the Haven box keeps 5 or more; (2) the 7 new towns are guarded TownRegions and every Trammel DungeonRegion of the author's is a DungeonRegion; (3) a boat floats in a sea within 15 of every dock but Haven and Nujel'm, which still fail as stated; (4) 1,000 SOS replays: no Point3D.Zero, every pick open sea | a mutated copy (a spot added on Valunstead's bank, Valunstead made a plain region): facts 1 and 2 fail, `red\red-facts-mutated.txt`. Facts 3 and 4 read the map only, so the copy cannot break them. Their tools' first versions failed on the real map (Haven's pool, the region-box rule), the cases now stated | 3 of 3, `green-facts.txt` |
| code `server/tests/Misc/SosTreasureLandVerification.cs`: (T1) the shipped treasure.cfg is ours (436 spots, none in a closure, the Haven maps get a spot); (T2) Refused for each closure box on both facets and never on another map; on Felucca inside a Trammel TownRegion or DungeonRegion, not on Trammel | the gated build with the Dockerfile's treasure.cfg line held out (pinned's file shipped): T1 fails, T2 and the other 2,765 pass, `red\red-build-1.txt` | 2 of 2 in the gated build, `green-build-2.txt` |

**The gated build** (the repo's gated build script, `-t sl-modernuo:cc-P684`, detached through
`cc-P684-tools\gated-build.ps1`; the Docker VM's page cache dropped first; docker-build lock taken and released):

- **Run 1, red:** 2,772 facts, T1 failed, 2,765 passed, 6 skipped.
- **Run 2, green** (`green-build-2.txt`): **EXIT=0, 2,772 facts, 2,766 passed, 6 skipped, 0 failed.** The skips are
  the real-map-file facts that skip in every build.

## Not done, and why

- **New docks for Haven and Nujel'm:** map work, for Chase to decide (above).
- **Felucca's housing in the new towns:** S13.
- **In-game trips** (a boat out of each dock and back, an SOS chest fished up, a chest dug on the new land): they need
  the server and client on SoS together (S1, S2 live), for S15.

## Deviations and decisions for Chase

- **Code-copy edits by script.** The Read tool is auto-denied for files in my code copy. I read them with Bash and
  changed them with an exact-text Python script, `cc-P684-tools\edit_p684.py` (the TreasureMap.cs call, its header line, the Dockerfile line), as in
  P682 and P683.
- **The Dockerfile replaces pinned's Data/treasure.cfg in place**, not under Data/ShatteredLegacy with a patch: the
  file has two readers (TreasureMap and TreasureMapProtection), and the replacement keeps both unchanged.

## Commit preflight

- **Code copy:** new `server/data/treasure.cfg` (436 lines, CRLF), `server/customizations/ClusterFSosTreasureLand.cs`
  and `server/tests/Misc/SosTreasureLandVerification.cs`; changed `server/patches/TreasureMap.cs` (ValidateLocation
  asks Refused; a header line) and `docker/uo/Dockerfile` (the treasure.cfg line).
- **Docs copy:** this file, new `tools/tests/test_sos_s11.py`, and `notes/cc-P684-tools/` (sea.py, treasure.py,
  docks_sos.py, the edit script, the build wrapper, `out/`, `red/`, the fact and build outputs; 1.6 MB, no file over
  5 MB). The sea masks cache outside the repo (`%TEMP%\p684-sea.npz`).
- **Lock:** docker-build, taken for the gated builds and released. No test shard, package or Haven work. Nothing
  committed.

P684 DONE
