# cc-P676: Trammel's regions and guard zones redrawn on the SoS land (SoS swap S3)

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P676`.

## In plain words

- The server now has its own map of Trammel's towns, dungeons and wild areas for the Siege of Sosaria land, in place of
  the stock one: 241 regions instead of 145. You will notice it once the swap goes live: the guards stand over the
  author's towns where they are now, and his 7 new towns (Valunstead, Hammerhill, Kameron Kove, Elmhaven, Kettleburg,
  Fort Yondall, Elandrim Nur Shaz) have guards too.
- Guards cover the towns themselves, not the forest and fields round them: each new or redrawn town's guard zone is
  cut back to its buildings and streets, plus a step past the edge. The author's 36 dungeons are dungeon regions (no
  houses), his docks and keeps are no-house areas, and S14's four unfinished areas are fenced off from housing.
- Every place our own code looks up by name is still there, and Felucca and the other lands are exactly as before.
- For you: nothing to try yet; it goes live with the rest of the swap. When it does, look at two things: Yew's guard
  zone comes out as patches round its scattered houses, and four Fountain of Youth spots (Avatar Isle Cave, Ice Isle
  Cave 2, Mt Kendall, North Territory Mine 2) keep their stock names over land whose caves the new map no longer has.

## What changed

**Code copy**
- `server/data/regions-trammel.json` (new, 111 KB): Trammel's 241 regions, 1,619 rects, written by
  `notes\cc-P676-tools\gen_regions.py`. Only pinned's own region types and keys appear in it.
- `server/patches/RegionJsonSerializer-shard-maps.patch` (new): pinned's `LoadRegions` reads its whole
  `Data/regions.json` and registers each region as it is read, so one map's regions cannot be swapped by a data file
  alone. With the patch, each `Data/ShatteredLegacy/regions-<map>.json` takes the place of pinned's regions of the maps
  it names, put where that map's first region stood. Every other map keeps pinned's, to the byte (`MergeShardRegions`).
  A merged copy of the whole pinned file was the alternative; it would hide upstream's region changes. Built with
  `diff -u`; it applies at fuzz 0.
- `docker/uo/apply-patches.sh` registers the patch beside the other region patch. `docker/uo/Dockerfile` copies the
  file into `Distribution/Data/ShatteredLegacy/` (where the tests read it; the runtime copies that folder whole).
- `server/tests/Regions/SosTrammelRegionsVerification.cs` (new), 6 facts. See Tests.

**Docs copy**
- `tools/tests/test_regions_sos.py` (new): the map facts.
- `notes/cc-P676-tools/`: the generator and its helpers, the decision log `out-decisions.csv` (one row per region,
  with the reason), `out-measure.csv`, the probe, the pictures in `pics/`, and the red and green outputs.

## How each region was decided

Inputs, all read only: pinned `regions.json` (145 Trammel regions), P669's change share per region
(`cc-P669-tools/out/stock-regions.csv`), the author's `Regions.xml` (150 Trammel entries), P669's new islands, his dock
spots (`sos-map-author-spots.md`), S14's list (P673 section 2). The land is the server's own: the SoS base with
today's `trammel.mapops`, built by `docker/uo/Build-MapOverlay.ps1`.

The brief's figures, counted again: 145 stock regions, **54** changed 75 percent or more, **47** changed 25 to 75
percent (101 in all), **65** new islands. All four match P669's files.

| Decision | Regions | Rule |
|---|---|---|
| kept | 44 | changed under 25 percent: exactly as pinned has it |
| kept for S7 | 42 | New Haven, Haven Island and old Haven with all their shops: S7 (P678, merged) re-registers New Haven from them at every start, so they stay as pinned has them |
| redrawn from the author | 15 | changed 25 percent or more and he draws the same name: his rects, pinned's type, priority, music, rune and children |
| clipped | 12 | changed, not drawn by him: only its rects that changed under 25 percent (the moongates' zones, some fields, Covetous Mine) |
| kept by name | 4 | changed, not drawn by him, but our code looks it up by name: stock rects kept (see below) |
| dropped | 28 | changed, not drawn by him, no unchanged rect, not looked up: fields and caves the land no longer has, and three dungeon entrances |
| added | 124 | his 7 new towns and Lord British Castle (guarded), 8 keeps and hamlets (no housing), 36 dungeons, 33 named wild areas, 2 no-housing areas, 9 docks, 24 isles, 4 unfinished areas |

**Redrawn from the author (15):** Bravehorn's drinking pool, Huntsman's Forest, Cove, Britain, Britain Graveyard,
Minoc, Vesper, Yew, Moonglow, Magincia, Buccaneer's Den, Destard, Delucia, Papua, Orc Cave. The name is kept (stock
spelling), since our code and players look regions up by it.

**Guard zones follow the town (item 1).** His town rects take in a lot of countryside: for example 42 percent of
Kameron Kove's area is open meadow, and Yew's covers the whole forest. So for each guarded region drawn here (10
redrawn towns, 7 new ones, Lord British Castle), `peel_to_town` works on 8 x 8 blocks inside his rects:
1. Start from the blocks with something built on them: walls, roofs, doors, bridges, floors and counters. Trees,
   foliage, flowers (they carry the Surface flag), rocks, grass and cave walls do not count.
2. Join built blocks up to 2 blocks apart (16 tiles), so scattered houses make one town, not dots.
3. Fill in any block the outside cannot reach without crossing the town: a yard, or a harbour inside the walls.
4. Add one block of margin where there is land or something built, never out to sea.

Result: Yew went from 4,341 blocks to 1,126, Buccaneer's Den from 1,926 to 661, Kettleburg from 1,465 to 784 and
Kameron Kove from 341 to 257. Walled Valunstead (an island city) keeps 1,681 of 2,552 blocks, much of it its harbour.
Yew is houses scattered through forest, so its zone is a set of patches round them, as the pictures show.

**The 7 new towns (item 2)** are guarded `TownRegion`s; so is Lord British Castle, which he draws on its own. Keeps
and hamlets (Plunderers Peak, Red Baron Stronghold, Red Dagger Keep, Sea Market, Seraphim Peak, Skaddria Naddheim,
Viligant Valley, Blackthorn Castle) get no housing and no guards; S10 decides their people. Blackthorn Castle is his
region over his castle; P691 moves our Blackthorn into the Fold, and this region does not stand in its way.

**Wild regions (item 2):** 33 of his named areas as `BaseRegion` under the towns, Glimmerwood and the Nujel'm desert
("Nujelm Desert", his spelling) among them. For the 65 new islands, 24 got an isle region over their dry 8 x 8 blocks.
The other 41 already lie in one of his areas (Khalahandra Keep holds 20, then Echoback Estuary, Everstar Estuary,
Skypoint Islands and others).

**Docks (item 2):** a no-housing region over each of his town docks' planks: Buccaneer's Den, Jhelom east, Magincia,
Moonglow, Papua, Skara Brae east and west, Trinsic east, Vesper. Nujel'm's spot (3803,1279) has no plank within 24
tiles, so it has none.

**Dungeons (item 3):** his 36 dungeons are `DungeonRegion`s, for example Azurite Caverns, Stone Burrow Mines, Wylarn
Caverns, Hammerhill Sewers, Khaldun, Britain Sewers and Haven Catacombs. A DungeonRegion already forbids housing and
uses dungeon light. Pinned's Trammel dungeons add no recall rule, so neither do these: recall in works as in stock.
Music is his where ours has the track, else Dungeon9. S14 seals them and S18 opens each; nothing here does either.

**Unfinished land (item 4):** a no-housing region over each of S14's four areas: the rooster island, the north-east
snow isles, the bare land east of Haven, and the cells round Echoback and Darkfathom.

**Not added:** 4 of his region types have no ModernUO class (`PoisonedTree`, `AcidRiver`, `CrystalField`, `IcyRiver`:
small event spots of a ServUO system), so they are left out. His `Jail` and `GreenAcres` regions are left out too,
because pinned's own stay.

## Names our code looks up

The brief says 19 files. Counted again (`namelookups.py`, `namelookups.txt`): **28 stock Trammel names in 22 files**,
11 in `server/customizations` and 11 in tests. The shipped code's lookups are **21 names**: Avatar Isle Cave, Blighted
Grove, Covetous, Despise, Destard, Fire, Haven, Haven Island, Hythloth, Ice, Ice Isle Cave 2, Jail, Mt Kendall, New
Haven, New Haven Moongate, North Territory Mine 2, Orc Cave, Sanctuary, Shame, Terathan Keep and Wrong. All 21 are in
the file (fact R3). The tests' extra names (Britain, Cove, Green Acres, Wrong Entrance, the Haven shops) belong to
facts whose host registers its own regions.

**Kept by name (4), all `FountainPool.cs`'s Fountain of Youth spots:** Avatar Isle Cave (68.8 percent changed), Ice
Isle Cave 2 (36.4), Mt Kendall (60.5) and North Territory Mine 2 (87.5). The author drew none of them, so the rule
would drop them. A missing name only leaves that pool entry with no spots, it does not crash
(`FountainPool.AreaOf`). But the brief says to keep the names, so their stock rects stay. Every rect is still 93 to
100 percent dry land on the SoS map (`dropped_lookups.py`). The caves themselves are gone or moved, so those 4 pool
spots should be looked at when the author's caves are known (S18).

**Dropped entrances:** Wrong Entrance, Covetous Entrance, Despise Entrance and Despise Passage. Only a test names one
(Wrong Entrance), and that test registers its own regions. The dungeons themselves (Covetous, Despise, Wrong) stay.

## Tests

**Server, `SosTrammelRegionsVerification`** (6 facts, read from the shipped files; nothing is registered):
- R1: the merge replaces only the maps the shard file names, at the first one's place.
- R2: the file is Trammel only, uses pinned's types, has unique names, parents before children, and every rect inside
  the facet.
- R3: the 21 looked-up names are there.
- R4: guards cover only pinned's guarded regions, the 7 new towns and Lord British Castle; the 7 are top-level
  `TownRegion`s; no isle or unfinished area is guarded; Glimmerwood and the Nujel'm desert are `BaseRegion`s.
- R5: his dungeons are `DungeonRegion`s, and S14's areas are no-housing regions over their exact rects.
- R6: pinned merged with the file has the file's Trammel regions and pinned's other maps, entry for entry.

Red then green (`probe.sh`, bind-mounted over `sl-uo-builder:cc-P720`):
- **Red:** the loader stub `red-stub/` (the merge returns pinned unchanged) and no data file: **6 of 6 failed**
  (`red-probe.txt`). R1 fails on "Collections differ", R6 on the null file, the rest on `NotNull`.
- **Green:** **6 of 6** pass (`green-probe.txt`).

**Map, `tools/tests/test_regions_sos.py`** (3 facts; `SL_SHARD_REPO`, `SL_SOS_MAP`):
1. Every rect lies on dry SoS land or its own water. A rect must hold dry land or something built (a dock), or touch
   a dry rect of the same region (a harbour). A non-dungeon rect is not mostly void; a dungeon's is not mostly water
   and has some floor.
2. No guard zone drawn here covers open wild. Every open-wild block of a redrawn or new guarded region is enclosed by
   the town, or within 3 blocks (24 tiles) of a built block of that zone.
3. The 7 new towns, Glimmerwood and the Nujel'm desert are each over half dry land.

Red, then green:
- **Red on pinned's own 145 Trammel regions** laid on the SoS land (`SL_REGIONS`, `red-test-regions-sos.txt`): facts 2
  and 3 fail. Cove's stock zone covers open wild on the new land, and the new towns are missing.
- **Red for fact 1:** it passed on pinned (pinned's rects mostly still sit on land), so I proved it twice. My own
  earlier generation failed it on a Valunstead margin strip in open sea (rect 608,456 to 640,464), which led to the
  "never out to sea" margin. A mutant with one Britain rect moved to open sea at 2000,3900 also fails it
  (`red-test-regions-sos-mutant.txt`).
- **Green: 3 of 3** (`green-test-regions-sos.txt`).

**Pinned's own guard zones**, kept where their land changed under 25 percent, are counted, not changed. By the same
strict count they cover open wild: the Heartwood 916 of 1,089 blocks, Trinsic 474 of 1,161, Nujel'm 697 of 2,530,
Serpent's Hold 223 of 675, Wind 100 of 489, Skara Brae 89 of 475, and the Moongates' small zones 17 of 18. That is how
OSI draws them on land that hardly changed (fidelity principle), so I left them. Say if you want them cut to their
towns too; it is one rule in the generator.

**Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P676`, `docker-build` lock, released): **EXIT=0**, 2,734 tests,
2,728 passed, 6 skipped (the usual client-data facts), 0 failed. The patch reads "Applied" (`green-gated-build.txt`).
- **The first build failed 2,711 of 2,734** (`red-gated-build-1-poisoned.txt`). My test's file lookup read
  `Core.BaseDirectory`, which caches its first answer. Read before any fixture, it cached "" for every later test,
  whose fixture then tried to load "Server.dll" as a relative path. The probe hid it because it ran my facts alone.
  The test now uses only `AppContext.BaseDirectory`. A probe of my facts together with `TypeIdentityVerification`
  passed 15 of 15 before the rebuild.

**Boot** (the image on a private shard, port 2596, a copy of the bot world, the SoS overlay; `test-shard` lock,
released; the shard is down). The log (`boot-regions.txt`) reads "Regions: regions-trammel.json replace pinned's
regions of their maps", then "Loading regions done (467 regions)". The New Haven seed and the Fold registered with no
error.

**Pictures** (`notes\cc-P676-tools\pics\`; `radar_regions.py`, each tile coloured from the client's `radarcol.mul`):
- `regions-sos.png` is the whole facet at a quarter size. Guarded towns are red, dungeons purple, no-housing orange,
  wild areas and isles green.
- `crop-britain.png`, `crop-yew.png`, `crop-kettleburg.png`, `crop-valunstead.png` and `crop-kameronkove.png` are at
  double size. I looked at each: Britain's and Kettleburg's guards follow their streets and buildings, Valunstead's
  covers the walled island city and its harbour, and Yew's sits round its houses.

## Decisions and deviations

- **P692 had not merged** (`origin/golem/Valorite/P692`, the Codex prep's `trammel-regions.json`), so I did not
  start from it; the prompt says to use it only if merged. This builds on the earlier P676 session's generator (its WIP
  commit on this branch), finished and changed as above.
- **No migration work.** Chase chose a fresh test world on swap day; this prompt planned no character or house
  migration, so there was none to drop.
- **The Read tool** was not needed for any file outside the work copies.
- **Live is not touched.** The regions go wherever the image goes, so they ship with the swap release. The overseer
  holds releases until S1, S2, S3, S7 and S8 have merged. Felucca's regions are S13's.
- Outside the repos: `D:\UO\golems\Iron\p676-work\` (the SoS overlay, the patch's a/b copies, the shard copy, the
  pinned extract and mutant). It can be deleted.

P676 DONE
