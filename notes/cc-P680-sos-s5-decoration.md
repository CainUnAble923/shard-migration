# cc-P680: stock decoration on the new land (SoS swap S5)

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P680`. Not committed, nothing deployed, Haven not touched. The map was read through the server's
overlay (`D:\UO\golems\Iron\p680-work\overlay`; its stamp's patch hash equals this branch's `trammel.mapops`). EA's own
maps for comparison are `D:\UO\UltimaOnlineVanilla` (P669's stock; Felucca is graded against Felucca's own file).

## In plain words

- **The towns keep their furniture on the new map.** Lord British's library, Britain's inn rooms and Moonglow's garden
  (statues, flowerbeds, the lamp post) all stand where they belong in the author's buildings. Pictures before and after
  are in `notes\art\sos-s5-decoration\` (open a `-decided` and a `-pinned` picture side by side).
- **Nothing floats, nothing sinks, no door hangs in mid-air or inside a wall.** About 530 pieces whose building the
  author removed or rebuilt differently are left out. Every one is listed with its reason in
  `notes\cc-P680-tools\out-decisions.csv`.
- **About 2,570 pieces were already on the map as part of the author's own art**, so they are not placed twice.
- **One thing to know:** Old Haven's shrine ankh (inside what is now a hall on the new map) is left out. New Haven's
  working ankh is still Chase's, by the League office. Nothing for you to do: it goes live with the rest of the swap.

## What was done

**Counted from the files:** pinned's `Data/Decoration` has **25,568 Trammel entries** (23,376 in Britannia's cfgs, which go
on both facets, and 2,192 Trammel-only) and **26,107 Felucca** (Britannia's and 2,731 Felucca-only). These match the brief.
The brief's 2,371 + 2,163 "rework" and 4,774 + 5,065 "to check" are P669's 3 x 3 grades. This tool decides each entry
instead, so its classes differ (below).

**The tool** is `notes\cc-P680-tools\deco.py`, with `maps.py` (the three maps, per-tile statics) and `doors.py` (the
doorway rule). It reads every cfg line, decides it, writes the decided cfgs (comments and order kept) and a CSV row for
every entry that is not left as it was. It decides in this order:

1. **Unchanged.** The tile and the 8 round it are the same on SoS as on the EA map the entry was made for: the same land
   height and kind and the same statics. A re-textured floor at the same height counts as the same (the author re-tiled
   Destard's caves). Left as it is.
2. **A door** is kept where SoS still has a doorway on its tile, else dropped. This is checked again at the end against
   the decoration as finally placed. The doorway rule (`doors.py`), facing left out:
   - walls on both sides along one axis (the map's or the cfg's own; a neighbouring door counts);
   - nothing impassable in the doorway;
   - no wall piece at the door's own height on its tile, other than an arch or door art.
3. **Already on the map.** The same art on the same tile within 5 Z: the author froze a decorated world into his
   statics. A `Static` entry is a duplicate and is dropped (**2,566**). A working item (an oven, a bed, a chest) is kept
   over the art.
4. **Fits as placed.** On SoS's land or a floor within 3 Z of its height (a cfg piece under it counts, such as flowers
   on a flowerbed), with nothing impassable in its body and no floor slab 4 to 11 above it. It is snapped onto that
   floor.
   - Guard: an entry that stood in one of EA's rooms (map walls or a roof round it) fits only where the author built
     something round it too.
   - **This is the big one (3,962 kept).** Pinned's cfgs were often made for an older map than EA's 7.0, and the author
     built from a ServUO world with the same decoration. So Lord British's library fits his castle floor for floor
     (EA's 7.0 castle has no such floors), and Britain's inn furniture fits his inn rooms.
5. **Its building is still here.** The structure round it on EA's map (walls, floors, counters, posts, the cfg's own
   included) is found again on SoS at the same offsets, 60 percent or more, with one height shift of at most 10. This
   covers things hung on walls.
6. **Its building moved whole** within 8 tiles: 80 percent, 6 or more pieces, 3 neighbours agreeing.
   - The first versions found such moves, but renders showed them matching shared wall art in different buildings
     (Ocllo's hall into another house).
   - With these limits, and fit checked first, **none remain**. Where the author kept a building, he kept it in place.
     "Re-placing" in practice is keeping on the same tile at his height: 1,114 entries are written at a new Z.
7. **Open ground on EA's map**, where the ground moved: it follows the ground if it fits there (42).
8. **Dropped** otherwise, with the reason:
   - its building is gone (454);
   - nothing to stand on within 3 Z (55);
   - SoS built on its tile (16);
   - void (5);
   - no doorway (1).

| | Trammel | Felucca |
|---|---|---|
| unchanged | 18,628 | 19,268 |
| kept (fits, doorway, building, working item) | 3,967 | 3,751 |
| on moved ground | 41 | 33 |
| dropped | 2,932 | 3,055 |

Most drops outside the duplicates are where a town was really rebuilt:
- Felucca's Ocllo (128), which is gone with Felucca's own map;
- New Magincia (88);
- an underground room of cfg walls under Moonglow (53);
- Destard's and Despise's edits (46, 31).

**How it ships:**
- the decided cfgs: `server/data/Decoration/{Britannia,Trammel,Felucca}`, all 59 files of those folders, LF line ends;
- the Dockerfile copies them to `Distribution/Data/ShatteredLegacy/Decoration`;
- `server/patches/Decorate-sos-decoration.patch` (built with `diff -u`, fuzz 0; listed in `apply-patches.sh`) makes
  `Decorate.Generate` read a folder from there when it exists, else pinned's. The other folders (Ilshenar, Malas,
  Tokuno, BountyBoards, the ruined Magincia sets) stay pinned's.

**Old Haven's shrine ankh** (`haven.cfg`'s AnkhNorth at 3606,2582) was dropped. Its shrine was built from cfg statics on
Old Haven's ruins; on SoS that tile lies under a hall's upper floor at Z 20. SoS's Haven has no ankh statics at all.
`ClusterFAnkhs.cs`'s comment that called it "the town's own working ankh" now says Chase's ankh by the League office
is the town's.

## Proofs

**The map fact, `tools/tests/test_s5_decoration.py`** (`SL_SHARD_REPO`, `SL_SOS_MAP`):
1. no item stands in water or void with nothing under it;
2. no door hangs outside a doorway (the rule above);
3. the shipped cfgs are pinned's, less exactly the CSV's drops, with its moves applied, every row with a reason.

Facts 1 and 2 leave out stock's own placements: an entry exactly as pinned has it, on land SoS left alone, failing the
same way on EA's map (4 and 8).

Results:
- **Red on main** (`red-test-s5-decoration.txt`): all 3 fail. Fact 1 finds 4 stranded entries (a Destard chest in void,
  a serpent pillar in water); fact 2 finds 2 door placements (the hedge maze door, inside a wall on SoS); fact 3 finds
  no decided cfgs shipped.
- **Mutant** (`red-test-s5-doors-mutant.txt`): one Britain door pushed 3 tiles along its wall is caught as "inside a
  wall". Most pinned doors already sit in doorways on SoS, so this shows the door fact can fail.
- **Green** (`green-test-s5-decoration.txt`): 3 of 3, 25,202 entries placed, 1,325 door placements.

**The server facts, `server/tests/Maps/SosDecorationVerification.cs`:**
- D1: the 59 files ship, and pinned's `DecorationList.ReadAll` reads each.
- D2: the entry counts, 20,486 / 2,150 / 2,566.
- D3: the old Haven ankh is out and Moonglow's garden lamp is in.

Red run (the decided cfgs and their Dockerfile line held back, pristine copies restored after;
`red-gated-build-summary.txt`): D1 to D3 fail, nothing else.

**Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P680`, `docker-build` lock, released): **EXIT=0, 2,756 tests,
2,750 passed, 6 skipped, 0 failed** (`gated-build-summary.txt`).

**Renders** (`notes\art\sos-s5-decoration\`, `render_deco.py`: the SoS land with a decoration set drawn in the client's
layout, roofs cut at a height as the client does indoors). Each place has a `-decided` (ours) and a `-pinned` (pinned's
cfgs on SoS) picture:

| Place | Decided | Pinned |
|---|---|---|
| Britain, Lord British's castle library | 185 entries | 209 |
| Britain, the inn rooms by the market | 64 | 64 |
| Moonglow, the garden | 77 | 130 (the 53 left out: 34 walls of a cfg-built room under the ground, 19 flowers with nothing under them on SoS) |
| Minoc, the market | 50 | 50 |
| The old New Haven plaza, forest on SoS | 0 | 0 (no cfg entries there) |

Every picture was looked at. The renders drove most of the rules above:
- an early version put courtyard items on the castle roof;
- an early version dropped the library and the inn furniture;
- an early version dropped the garden.

## Decisions and deviations

- **No migration work** (a fresh test world, Chase 10-27). `[Decorate` places the decided set on swap day.
- **The "re-place onto the matching building" of the brief** turned out to be keep-in-place at the author's height:
  every match off its own tile that the tool found was false (shared wall art). The move machinery stays in the tool,
  with strict limits, and finds nothing now.
- **Felucca is graded against EA's own Felucca map** (map0 differs from Trammel on about 1.07 million tiles), and placed
  on the SoS land it now shares with Trammel.
- **Not in scope, left pinned's:** the ruined Magincia sets (`[DecorateMag`) and the other facets' folders.
  - Follow-up: `ClusterFAnkhs` also places two Felucca ankhs at x 6937 and 6947 (Felucca's own map0 land, void on
    SoS; P679 dropped that land's teleporters). That is our code, for a later swap prompt.
- **Denied in this unattended run:** one command was refused for approval. It would have deleted the first set of
  renders before re-rendering (`rm -f notes/art/sos-s5-decoration/*.png`, chained with a Python edit and the renders).
  I made the edit with the Edit tool and wrote the new renders over the same file names instead. Nothing depended on
  the deletion.

## Files

- Code copy:
  - `server/data/Decoration/` (59 cfgs) and `server/patches/Decorate-sos-decoration.patch`;
  - `docker/uo/Dockerfile`, `docker/uo/apply-patches.sh`;
  - `server/customizations/ClusterFAnkhs.cs` (a comment);
  - `server/tests/Maps/SosDecorationVerification.cs`.
- Docs copy:
  - this note and `tools/tests/test_s5_decoration.py`;
  - `notes\cc-P680-tools\`: `deco.py`, `maps.py`, `doors.py`, `render_deco.py`, `edit_decorate.py`, the gated-build
    script, `out-decisions.csv` (one row per entry not left as it was), `out-summary.txt`, the red, mutant and green
    outputs, the build summaries, and `art\` (working renders);
  - `notes\art\sos-s5-decoration\`.

P680 DONE
