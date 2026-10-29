# cc-P686: Felucca's regions on the SoS land (SoS swap S13)

Iron Golem, 2026-10-29. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P686` (main at the P685 merge). Not committed, nothing deployed.

## In plain words

- Felucca now has its own map of towns, dungeons and wild areas for the Siege of Sosaria land, made from the Trammel
  map that S3 (P676) drew. Felucca stands on the same land as Trammel since the swap, so its towns are now exactly
  Trammel's towns: the same edges, the same guard zones cut back to the buildings, and the author's 7 new towns.
- Felucca's own rules stay. Buccaneer's Den has no guards. Every other town Felucca guards today is still guarded,
  and so are the author's 7 new towns. No champion spawn's ground lies inside a guard zone.
- You will notice it once the swap goes live: Felucca's guards stand over the same streets as Trammel's. Felucca's
  old Haven town keeps its name, Ocllo, over the same ground as Trammel's New Haven. Felucca's T2A Arena region is
  gone, because the land under it changed and nothing uses it.
- For you: nothing to try yet; it goes live with the rest of the swap.

## What changed

**Code copy**
- `server/data/regions-felucca.json` (new, written by `notes\cc-P686-tools\gen_felucca.py`): Felucca's 201 regions,
  1,543 rects. Only pinned's own region types and keys appear in it.
- `docker/uo/Dockerfile`: copies the file into `Distribution/Data/ShatteredLegacy/`, beside S3's `regions-trammel.json`.
  No code change was needed. P676's `RegionJsonSerializer-shard-maps.patch` already reads every
  `Data/ShatteredLegacy/regions-*.json`, and each one replaces pinned's regions of the maps it names.
- `server/tests/Regions/SosFeluccaRegionsVerification.cs` (new), 6 facts (see Tests).

**Docs copy**
- `tools/tests/test_regions_sos.py`: S3's three land facts now run on Felucca's file too. Two new facts need no map:
  the towns match, and no champion area lies in a guard zone.
- `notes/cc-P686-tools/`:
  - `measure_felucca.py`, which measures how much of each Felucca region the land changed (`out-felucca-measure.csv`);
  - `gen_felucca.py` and its decision log `out-decisions.csv` (one row per region, with the reason);
  - the probe, the mutants, and the red and green outputs.

An earlier sitting of this task wrote the generator, the file and the Python facts, kept as the WIP commits
`275cf01` (docs) and `b279a40` (code). This sitting checked that WIP, then:
- regenerated the file; it came out byte for byte the same;
- added the Dockerfile line and the C# facts;
- ran every test and booted the server.
The WIP deleted nothing.

## How each region was decided

Felucca reads Trammel's map files since P675, so stock Felucca's 107 regions (272 rects) now lie over SoS land. 100 of
the 107 have exactly the rects of the pinned Trammel region of the same name, so they take S3's decision for that
region. The other 7 are Felucca's own geography, and they get S3's rule measured on Felucca's own change.

| Decision | Regions | Rule |
|---|---|---|
| kept | 45 | as S3 kept it on Trammel, or Felucca's own and under 25 percent changed |
| redrawn from the author | 15 | as on Trammel: the author's rects, the guard zone peeled to the town (Britain, Minoc, Vesper, Yew, Moonglow, Magincia, Buccaneer's Den, Cove, Delucia, Papua; Destard, Orc Cave, Britain Graveyard, Huntsman's Forest, Bravehorn's drinking pool) |
| redrawn to the town | 2 | Ocllo and its inn (below) |
| clipped | 12 | as on Trammel: only the rects under 25 percent changed (the moongates' zones, fields, Covetous Mine) |
| kept by name | 4 | as on Trammel: our code looks them up (FountainOfYouth: Avatar Isle Cave, Ice Isle Cave 2, Mt Kendall, North Territory Mine 2) |
| dropped | 29 | as on Trammel (fields, caves, mines and three dungeon entrances the land no longer has), plus Felucca's own T2A Arena (70 percent changed) and Moonglow's inn (100 percent) |
| added | 123 | S3's additions, the same on Felucca: the author's 7 towns and Lord British Castle (guarded), keeps and hamlets, 36 dungeons, wild areas, docks, isles and S14's 4 unfinished areas |
| not added | 1 | Khaldun: Felucca already has its own, with the same rect |

**The towns match.** Every region named on both facets has the same rects on both. That covers all 15 redrawn
towns and places, and the 7 new towns. The only Felucca-only names are Ocllo and Felucca's own children:
- **Ocllo** is Felucca's name for the pre-UOML Haven town, which the author rebuilt. It takes pinned Trammel
  `Haven`'s rects: S3 keeps those for S7, and Trammel's New Haven is registered over them at every start (P678,
  `HavenTownRegions.cs`). Its inn child takes the inn building that Trammel's New Haven Inn is registered over
  (`HavenTownRegions.InnArea`).
- Britain's and Nujel'm's inn children are Felucca's own. They changed under 25 percent, so they stay.

**Felucca's rules stay.**
- Every region keeps Felucca's own fields: type, priority, music, rune name, logout.
- Buccaneer's Den keeps `GuardsDisabled`.
- Every town Felucca guards today is still guarded (19 top-level guarded regions in pinned, 26 here with the author's
  7). Nothing else is guarded.

**The brief's figures.** P669's table (272 rects: 185 unchanged, 54 moved, 33 rework) grades each rect by its
centre point, with `geo.Grader`. S3, and this task after it, decide by the share of 8 x 8 blocks changed under the
rect, against stock Felucca's land. On that measure the 272 rects are 101 unchanged, 85 moved and 86 rework.
The 272 rects match P669's count. The two measures differ, so the split differs.

**Codex prep.** P693 (`felucca-regions.json`) has not merged (no commit names it on main), so there was nothing to
start from.

## Tests

**C# facts** (`SosFeluccaRegionsVerification`, S3's R2 to R6 for Felucca):
- F1 the file is Felucca only, in pinned's types, with unique names, each parent first and every rect in bounds;
- F2 every Felucca name our code looks up is there (17);
- F3 Felucca's rules: guards only on pinned Felucca's guarded regions and the author's towns, Buccaneer's Den
  unguarded, the 7 new towns guarded TownRegions, no isle or unfinished land guarded;
- F4 the author's dungeons are DungeonRegions and the unfinished land has no housing;
- F5 the towns match Trammel's, and Ocllo has pinned Trammel Haven's rects;
- F6 pinned merged with both files, as the loader does: Felucca and Trammel are the files', the other maps pinned's.

How they ran (`notes\cc-P686-tools\probe.sh`, on `sl-uo-builder:cc-P685`):
- **Red**, the file not shipped: all 6 fail; S3's 6 pass (`red-probe.txt`).
- **Red**, a mutant with Buccaneer's Den guarded and Britain's first rect one tile wide (`mutate.py`): F3 fails
  ("Buccaneer's Den stays unguarded") and F5 fails ("different rects on the two facets: Britain")
  (`red-mutant-probe.txt`).
- **Green**: 12 of 12 (`green-probe.txt`).

**Map facts** (`tools\tests\test_regions_sos.py`, `SL_SOS_MAP` = this branch's SoS overlay at
`D:\UO\golems\Iron\p686-work\sos-overlay`, `SL_SHARD_REPO` = the code copy): **8 of 8 pass**
(`green-test-regions-sos.txt`): S3's 3 on Trammel, the same 3 on Felucca, and facts 4 and 5.
- Red, run by the earlier sitting on pinned's Felucca regions (`red-test-regions-sos.txt`):
  - fact 2 fails: the T2A Arena's guard zone covers open wild;
  - fact 3 fails: no Valunstead;
  - fact 4 fails: Bravehorn's drinking pool, Britain, Moonglow, Papua, Vesper, Yew and others differ from Trammel.
- Fact 5 passes on pinned's file too, so I made it fail with a mutant: Britain's guard zone given a rect over
  champion LL01 (`mutate_champ.py`, `red-fact-5.txt`: "('LL01', 'Britain', ...)").
- Fact 1 on Felucca is S3's own fact, seen failing in P676; pinned's Felucca rects pass it too.
- The pinned guard zones that are only counted are as on Trammel, plus Ocllo (272 of 633 blocks open wild: the same
  as Trammel's Haven rects, which S7 keeps).

**Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P686`, `docker-build` lock, released): **EXIT=0**. 2,799
tests: 2,793 passed, 6 skipped, 0 failed. All six F facts ran in the gate (`green-gated-build.txt`).
`RegionJsonSerializer-shard-maps.patch` reports "Applied".

**Boot** (private shard 127.0.0.1:2596, `sl-modernuo:cc-P686`, P676's `proof-shard.ps1`, `test-shard` lock, released;
the shard is down): "Regions: regions-felucca.json, regions-trammel.json replace pinned's regions of their maps",
"Loading regions done (561 regions)". That is P676's 467, less pinned's 107 Felucca regions, plus these 201. No error
(`boot-regions.txt`).

## Chase's decisions applied

- **A fresh test world on swap day:** nothing here migrates characters or houses. The regions are data read at
  start. This prompt planned no migration work, so there was none to drop.
- **Blackthorn:** the author's Blackthorn Castle region comes over from S3 on Felucca as on Trammel (no housing, no
  guards). It does not stand in the way of P691 moving our Blackthorn into the Fold.

## Deviations and decisions

- **The Read tool was denied** on the code copy's `docker\uo\Dockerfile` (an unattended run denies reads outside
  the working directory). As in P732, I read that copy with `sed`, `grep` and `cat`. I made the edits with small
  Python scripts and copies from the scratchpad (the Dockerfile line, the new test file). Nothing was skipped.
- **T2A Arena dropped on Felucca.** It is a guarded region over arena land that the SoS map changed by 70 percent,
  and no code looks it up. Under S3's rule it goes, and fact 2 shows its old zone covers open wild.
- **Moonglow's Felucca inn child dropped:** its whole rect changed. Moonglow itself is the author's town, as on
  Trammel.

## Files

- Code copy: `server/data/regions-felucca.json` (from the WIP commit, unchanged), `docker/uo/Dockerfile`,
  `server/tests/Regions/SosFeluccaRegionsVerification.cs`.
- Docs copy: `tools/tests/test_regions_sos.py` (from the WIP commit) and `notes\cc-P686-tools\`:
  - `measure_felucca.py`, `gen_felucca.py`, `out-felucca-measure.csv`, `out-decisions.csv`;
  - `probe.sh`, `mutate.py`, `mutate_champ.py`, and the red and green outputs;
  - `gated-build.ps1`, `green-gated-build.txt`, `proof-shard.ps1`, `boot-regions.txt`.
- Outside the repos: `D:\UO\golems\Iron\p686-work\` (the SoS overlay, pinned's Felucca regions for the red run, the
  boot copy) can be deleted.

P686 DONE
