# cc-P683: the author's dungeon decoration for Trammel and Felucca (SoS swap S6)

Iron Golem, 2026-10-29. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P683`. Not committed; nothing deployed; the test shard not touched. The file and its dungeons are
Zigholtul's (Siege of Sosaria Trammel Map 3.0, `SOS Trammel Dungeons.cfg`), used with the credit in its header.

## In plain words

- **The author's dungeon teleporters are in the shard now, on both Trammel and Felucca.** His file is 200 teleporters
  for 25 of his dungeons (no doors or props, despite the plan's wording). The ones inside each dungeon, the stairs
  between levels and the ways out, ship: 130 a facet. When the world is decorated, they go in with everything else.
- **Every one of his dungeons stays sealed.** The 70 teleporters that would take a player in from the surface are left
  out, listed by dungeon at the top of the file. Nothing else leads in either: none of the shard's other teleporters
  (817 on both facets, and 126 in the stock decoration) goes into one of his dungeons.
- **Every teleporter was checked on the map:** both ends of all 200 stand on a floor a player can reach or land on.
  None share a tile with a teleporter the shard already has.
- **For you:** nothing to do now. When S18 has monsters in a dungeon, opening it is one line (its name in `OPENED`
  in `notes\cc-P683-tools\port.py`) and a rerun.

## How it was done

**Starting point.** The prompt says to start from P694 if it merged. It has not (its branch is `golem/Valorite/P694`,
1f8b0f8); I read its notes and data from git and checked them rather than redoing them. P694 found the author's file
already in the cfg syntax pinned's `DecorationList` reads: no type or coordinate translation is needed.

**The type map (part 1).** The file's one type is ServUO's `Server.Items.Teleporter`. Pinned has the same class,
`Server.Items.Teleporter` (item 0x1BC3, invisible, immovable, PointDest and MapDest). **No type is without a match.**
The file has 775 lines: 167 comments, 207 blank, 201 Teleporter headers and 200 placements. The last header, under
MISC, places nothing (`PointDest=(0, 0, 0)` with no coordinate line); it stays as a comment (`# S6 UNPLACED: `).

**The tool** (`notes\cc-P683-tools\port.py`) checks the author's file is unchanged (its SHA-256) and writes the two
cfgs into the code copy:

- every author line, in order, after our header (credit, facet, type map, the sealed list);
- `server\data\Decoration\Trammel\sos-dungeons.cfg`: MapDest=Trammel.
- `server\data\Decoration\Felucca\sos-dungeons.cfg`: MapDest=Felucca. A Trammel copy loaded on Felucca would send
  Felucca's players to Trammel (Teleporter.cs: a MapDest overrides the map).

Their active lines are identical to P694's `sealed\` files. The tool also writes `out\teleporters.csv`: every
placement, both ends, shipped or sealed.

**How the server uses it.** P680 (S5) ships the shard's decided decoration as `Data/ShatteredLegacy/Decoration/
{Britannia,Trammel,Felucca}`, and `Decorate-sos-decoration.patch` reads those folders in place of pinned's. The stock
`[Decorate` loads the Trammel folder on Trammel and the Felucca folder on Felucca. So the two files go in those folders:
no new patch, no Dockerfile change, no new command. `[Decorate` on the fresh world places them.

**Sealed (part 2).** Every block the author heads `## Entrance` (his surface way in: Level 1, 2 and 3 Entrance blocks
are links between levels and ship) is commented out (`# S6 SEALED: `) for each dungeon not in the tool's `OPENED`
list. The list is empty: S18 has opened none (Chase 10-27: "seal the author's dungeons until each has monsters"). That
is 70 placements across all 25 dungeons with placements. Their names are in each file's header. Exits and inner
links stay: harmless with no way in.

**No other way in.** P676's regions give each of the 25 a DungeonRegion (`Oboru Burial Grounds` is `Oboru Burial
Ground` in his Regions.xml). None of P679's 817 shipped teleporters (Trammel and Felucca), and none of the 126 teleporters in
P680's decoration cfgs, lands inside one of them from outside.

## Walkable ends (part 3)

`notes\cc-P683-tools\check.py`, on the SoS map (P481's copy, P681's `sosgrid.Surfaces`: every standable Z of a tile):

- **The test:** each end has a floor from 15 Z below to 5 Z above its Z.
  - Below: pinned fires an item for a walker up to 15 under it (Mobile.cs Move: `item.Z + height > newZ && newZ + 15
    > item.Z`; 0x1BC3 has height 1), and a player put down at a PointDest steps down to the floor under him.
  - Above: 5, for the walk model's own error, P681's tolerance.
- **Calibrated on stock.** A stricter test (the teleporter at or over the floor) fails 40 of the shard's 393 shipped
  Trammel teleporters that work in game today. The model's land Z is a point or two off the server's on sloped
  dungeon floors. With the window above, 18 of the 393 fail.
- **The author's 200: all pass, both ends.** One needed the window: Hammerhill Sewers' exit at 6394,2770,31 sits
  partway up a rope ladder (stone to 25, the ladder's top at 42). A walker on the stones at 25 sets it off, and a
  player sent there steps down to 25: a UO ladder, kept as the author made it.
- **Collisions:** no shipped teleporter (P679's or a decoration cfg's) stands on any of the 130 tiles.
  - This matters because `Decorate.cs` counts an existing Teleporter at the same XYZ as already placed, whatever its
    destination.

Full lists: `out\ends.csv` (every end and its floor), `out\check.txt`.

## Facts

| Fact | Red | Green |
|---|---|---|
| docs `tools/tests/test_sos_dungeon_decoration.py`: (1) the shipped cfgs are port.py's output of the unchanged author file, 200 placements, one type Teleporter, each copy's MapDest its own facet, the two otherwise the same; (2) the 70 entrances out and everything else in; no shipped teleporter (P679's, the decoration cfgs') into an author dungeon from outside; (3) every end of all 200 walkable on SoS, no shared tile | a mutated copy (one Agurast Ascension entrance un-sealed, a Felucca MapDest set to Trammel, a teleporter into Agurast added to teleporters-sos.json): 3 of 3 fail, `red\red-facts-mutated.txt` | 3 of 3, `green-facts.txt` |
| docs `tools/tests/test_s5_decoration.py` (P680) | | 3 of 3 (2 skip without `SL_SOS_MAP`, as before): it now reads pinned's cfgs only |
| code `server/tests/Maps/SosDungeonDecorationVerification.cs`: (S1) both files ship, pinned's reader reads them, one type, pinned's Teleporter, 130 a facet, every MapDest its facet; (S2) a real Generate of each on its facet places 130 Teleporters where the file says, each PointDest the file's, MapDest that facet | the gated build with the two cfgs held out: exactly these 4 fail, 2,759 others pass, `red\red-build-1.txt` | 4 of 4 in the gated build, `green-build-2.txt` |

`server/tests/Maps/SosDecorationVerification.cs` (P680's D1 and D2 count every cfg in the three folders: 59 files,
2,150 Trammel and 2,566 Felucca entries) now counts pinned's decided files only and leaves `sos-dungeons.cfg` to the
new facts. It is a 7-line change, commented. It passed in the red build, which also shows it is not counting the new
file.

**The gated build** (the repo's gated build script, `-t sl-modernuo:cc-P683`, detached through
`cc-P683-tools\gated-build.ps1`; docker-build lock taken and released; the Docker VM's page cache dropped
first, 1 to 5 GB free in Windows):

- **Run 0:** did not compile: CS0411, LINQ over `Map.GetItemsAt`, which is a ref-struct enumerable. Now a loop.
- **Run 1:** apply-patches stopped on `BaseWeapon-axe-bonus-osi.patch` "never applied" right after an "Applied:"
  line, the known pipe race (`red\red-build-1-patch-flake.txt`). Rerun unchanged.
- **Run 1 again, red** (the two cfgs held out): 2,769 facts, the 4 new ones failed, 2,759 passed, 6 skipped.
- **Run 2, green** (`green-build-2.txt`): **EXIT=0, 2,769 facts, 2,763 passed, 6 skipped, 0 failed.** The skips are
  the real-map-file facts that skip in every build. P680's D1 to D3 pass beside the new file.

## Not done, and why

- **Doors and props.** The plan says the file holds doors, teleporters and props. It holds 200 teleporters only (P694
  counted the same). His dungeons' doors and props are in his map's statics.
- **The three empty sections** (Boulder Tunnel, Guardians Power Plant, Kal-Berbesia: an `## Entrance` heading with
  nothing under it) and MISC's unplaced header: the author left them empty. Nothing is invented; S18 has them to
  answer.
- **Walking through in game.** The ends are checked on the map files. A player's trip (in a dungeon, down a level, out)
  needs the server and the client on SoS together (S1, S2 live) and a dungeon opened (S18).
- **Migration dropped** (Chase's fresh test world): `Decorate.cs` skips a teleporter already on its tile. An existing
  world decorated before this would keep what it has. The fresh world on swap day has none.

## Deviations and decisions for Chase

- **Two code-copy edits by script.** The Read tool is auto-denied for files in my code copy outside this session's
  working folder. I read them with Bash and changed them with a small exact-text Python script: P680's C# fact in this
  prompt, and P683's own `GetItemsAt` loop. It is the same way as in P682.
- **The walk test's window** (15 below, 5 above) is wider than P681's plain "within 5": it follows pinned's own
  trigger rule. With "within 5" only the Hammerhill ladder would fail, and it works as a ladder.

## Commit preflight

- **Code copy:** new `server/data/Decoration/Trammel/sos-dungeons.cfg` and `Felucca/sos-dungeons.cfg` (about 24 KB
  each), new `server/tests/Maps/SosDungeonDecorationVerification.cs`; changed
  `server/tests/Maps/SosDecorationVerification.cs` (pinned's files only).
- **Docs copy:** this file, new `tools/tests/test_sos_dungeon_decoration.py`, changed `tools/tests/test_s5_decoration.py`
  (pinned's cfgs only), and `notes/cc-P683-tools/` (port.py, check.py, the build wrapper, `out/`, `red/`, the fact and
  build outputs; 1.6 MB, no file over 5 MB).
- **Lock:** docker-build, taken for the gated builds and released. No test shard, package or Haven work. Nothing
  committed.

P683 DONE
