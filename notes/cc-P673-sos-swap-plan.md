# cc-P673: the Siege of Sosaria swap (Trammel and Felucca), planned, and the Wakening Isle re-sited

Iron Golem, 2026-10-26. Plan only: no code, no map files, nothing built or deployed. Chase chose (a) on 10-26 19:25:
the whole Siege of Sosaria map (Zigholtul, Trammel Map 3.0) replaces both Trammel and Felucca before 1.0, and the
Wakening Isle goes ahead, re-sited first. The map was read only through P481's copies in
`notes\cc-P481-tools\scratch\sos\`; nothing was run from `D:\UO\third-party`. Counts come from P669
(`notes\cc-P669-sos-trammel-assessment.md`, `notes\cc-P669-tools\out\`) unless a line says otherwise.

## In plain words

- **The Wakening Isle has a new home.** Its old spot is one of the author's caves now, so it moves to the big empty
  black area at the south-east corner of the map (x 6594-6865, y 3905-4049). Nothing of his is within 161 tiles of it,
  and there is room beside it for the League's later private spaces. Every coordinate in the isle plan just shifts by
  the same amount; the island itself does not change. Pictures: `notes\art\sos-isle-site\`.
- **The swap is 19 build prompts** (S1 to S19 below), plus small changes to the five held isle prompts. Five of them
  (the map delivery, the server's map data, New Haven, regions and the old-dungeon fixes) have to go live together on
  the test shard, or players would walk through walls the client does not draw. After that, players can play while
  the rest lands: the author's 20-odd dungeons stay sealed until they have monsters in them.
- **New Haven moves into the author's Haven town** (his rebuilt town on the old Old Haven site, with a bank, docks
  and a smithy). The old plaza is forest on his map. Rootdeep's way in becomes a cellar hatch in that town.
- **For you:** four decisions at the end: New Haven's new home, what happens to the test shard's characters and houses
  on the swap day, EA's Blackthorn dungeon (his map has no room for it), and what stays closed at 1.0.

## 1. The isle re-sited

### 1.1 How I looked (`notes\cc-P673-tools\sitefind.py`, `sitecheck.py`)

- **The need** (P481 11.2): the drawn area of 272 x 145 tiles, west to east, with its 24-tile sea margin inside.
- **A site:** a spot where that box, plus a buffer all round, holds only empty void (void land 0x0244 or 0x0002 with no
  static) on the SoS file. The buffer matters twice after the swap. First, the author's players on Trammel and
  Felucca (both read this file) must not see our sea. Second, players on the Fold must not see his caves.
- **Scanned** on a 4-tile grid over the whole map, for void and, for comparison, for open sea with no statics.
- **Checked** each finalist against all of the roughly 30,000 points P669 graded (stock spawners, decoration, teleporters, treasure
  spots, moongates, regions, our code and the bot, Trammel and Felucca). I also checked that the box is void in stock
  Trammel too, so nothing breaks if the swap ever slips.
- **Shifts are multiples of 8,** so every tile keeps its place inside its 8 x 8 block. P481's plan then moves by plain
  addition, and P662's patch has the same block layout as the sketch.

### 1.2 The candidates (`notes\art\sos-isle-site\overview-dungeon-strip.png`, `site-A.png` to `site-D.png`)

| Site | Box (x, y) | Clear all round | Room it can slide in | Nearest content | Verdict |
|---|---|---|---|---|---|
| **A: south-east void** | 6594-6865, 3905-4049 | **161 tiles** (46 to the map's south edge) | 6160-7167, 3744-4095 (1008 x 352) | the author's dungeon block at 6427, 3743; nearest go-spot Bharlim Passage, 175 tiles | **recommended** |
| C: east of void C | 6874-7145, 1913-2057 | 79 | 6812-7167, 1852-2120 | 6794, 1892; Guardian's Power Plant 176 tiles | good; the same rows as the old site (every y stays) |
| B: north-east corner | 6888-7159, 4-148 | 107 | 6808-7167, 0-228 | 6781, 124 | fits, but it sits against the map's top edge with little room |
| D: south of void C | 6372-6643, 2132-2276 | 43 | 6168-6847, 2112-2292 | the Mongbat Hideout, 90 tiles; Passage of Lost Souls level 2 just north | too close to his caves |
| Open sea | many, up to 192 clear | | | | **not used.** A boat on Trammel or Felucca would see an island it cannot land on |

The other voids P669 listed are too thin for the box: 64 x 2,928 at the east edge, and 464 x 144, one row short.

### 1.3 Recommendation: site A (`pick-A.png`)

- **It has the most room.** Nothing of the author's comes within 161 tiles of the box. The room round it
  (434 tiles west, 161 north, 302 east) holds the Fold's later zones (P481 3.2), which void C held before.
- **Nothing to clear.** No stock, ServUO or our own point lies within 64 tiles. It is void in stock Trammel too.
- **Site C** is the fallback: every y coordinate stays as P481 drew it. But it has half the clearance and almost no
  room east (22 tiles to the map's edge), so the League's spaces would not fit beside it.

**The shift is (+424, +1992).** Add it to every coordinate in P481 section 11.2:

| What | Old (void C) | New (site A) |
|---|---|---|
| Drawn area with its sea | 6170-6441, 1913-2057 | **6594-6865, 3905-4049** |
| Walkable land and dock | 6202-6409, 1938-2026 | 6626-6833, 3930-4018 |
| Stop 0, the beach (Tamsin; `[Fold goto` default) | 6214, 2001 | **6638, 3993** |
| Stop 1, the bright tiles | 6222, 2000 | 6646, 3992 |
| Stop 2, the camp | 6232, 1998 | 6656, 3990 |
| Stop 3, the clothes rack | 6241, 2000 | 6665, 3992 |
| Stop 4, the signpost | 6268, 1998 | 6692, 3990 |
| Stop 5, the farm gate | 6290, 1987 | 6714, 3979 |
| Stop 6, the training yard | 6312, 2003 | 6736, 3995 |
| Stop 7, the trades square | 6338, 1989 | 6762, 3981 |
| Stop 8, the League lodge door | 6358, 2002 | 6782, 3994 |
| Stop 9, the standing stones | 6370, 1990 | 6794, 3982 |
| Stop 10, the dock's end, moongate | 6407, 1999 | **6831, 3991** |
| The meadow | 6252-6292, 1966-1995 | 6676-6716, 3958-3987 |
| The farm (334 pieces) | 6262-6291, 1975-1991; shift from New Haven (+2890, -628) | 6686-6715, 3967-3983; shift from New Haven **(+3314, +1364)** |
| The training yard | 6302-6324, 2002-2018 | 6726-6748, 3994-4010 |
| The trades square | 6330-6350, 1979-1996 | 6754-6774, 3971-3988 |

**The Fold's later zones at site A** (proposed; each at least 24 tiles from the isle's box):

| Zone | Old (void C) | New |
|---|---|---|
| 2 Vision chamber (free since P481 12) | 6440-6463, 1850-1873 | 6720-6743, 3800-3823 |
| 3 League private spaces | 6480-6630, 1850-2040 | 6180-6560, 3770-4080 |
| 4 Events | 6170-6400, 2125-2270 | 6890-7150, 3770-3880 |
| 5 Custom dungeons | 6420-6630, 2060-2270 | 6890-7150, 3905-4080 |
| The Fold's mirror region on Trammel **and Felucca** | 6160-6639, 1832-2279 | **6160-7167, 3744-4095** (the whole empty room) |

### 1.4 Addendum for the held prompts P662 to P666

**A must-fix first, before the swap goes live (it goes in S2):** P661's `FoldMirrorRegion` sits on Trammel over void C
(6160-6639, 1832-2279). On SoS that is the author's cave dungeon (Passage of Lost Souls level 2, 6202, 2116). Left
alone, it would throw every player who enters that dungeon back to New Haven. S2 moves it to 6160-7167, 3744-4095
and adds a twin on Felucca. Felucca reads the same file after the swap, so the isle shows there too.

Nothing changes in `FoldMaps.cs`. The Fold maps already read file index 1, and the client draws its map 1. Once S1 and
S2 land, both are the SoS file, so **the Fold reads the new Trammel file by itself**.

| Prompt | Changes |
|---|---|
| **P662** (map) | Coordinates: the drawn area becomes **x 6594-6865, y 3905-4049**. `newisle.py` keeps its old numbers; the driver adds one constant shift (+424, +1992), so the plan and the build cannot drift apart. **The base is the SoS file:** `mapops.py diff` runs against a pristine SoS copy (S2 puts its hashes in `ORIGINAL-SHA256.txt`), not the vanilla UOP. **Order:** after S2 has re-based `trammel.mapops` onto SoS, so the isle's lines join a file whose fingerprints match. The renders read SoS too. Nothing else changes: the site is void in both maps. **Ships with** S1 (the client needs the SoS base under the patch). |
| **P663** (server) | Stop coordinates from the table above; the farm's shift from New Haven becomes (+3314, +1364); the start-choice "Tutorial Island" display spot is re-picked in the SoS sea south of the new New Haven. **New Haven's spots move in S7.** P663 reads them (Rook, the dock moongate's way out, the skip start, the island gate's Haven bounds) from one class, `HavenSpots`, so S7 changes one file. The trade and wing trials stay "in New Haven" and move with S7. `TutorialIslandGate.IsOnIsland` gets the Fold (P661's note) and, after S7, the new Haven bounds. |
| **P664** (server) | No coordinates of its own. The beach of map 32, where trainees wait for a copy, is 6638, 3993. |
| **P665** (server) | The stones are at 6794, 3982. If the vision ever uses a chamber, zone 2 is at 6720-6743, 3800-3823. |
| **P666** (server, patch) | Tobin stands by the farm gate (6714, 3979). "New Haven's stable vet" becomes whichever vet S7 seeds in the new town. |
| **P661's code** (now in S2) | `FoldRegions.cs`: the mirror moves to 6160-7167, 3744-4095, with a Felucca twin. `FoldCommands.cs`: the default spot becomes 6638, 3993. `FoldVerification.cs`: 6214,2001 becomes 6638,3993, and the mirror's corners change. The mirror's send-to spot (the New Haven start, 3503, 2574, 14) moves with S7. |

Order with the swap: S1 and S2, then P662; P663 can be written against `HavenSpots` at any time. The isle still ships
as P662 plus P663's cliloc lines, and goes live with P664, as the held prompts say.

## 2. The swap as build prompts (drafts for the overseer to number)

**Size:** S is about one session, M one long session, L may need a continuation. **Golem:** Iron has done the map and
package work (P481, P661, P669, P670); Verite the place and quest content (P672); Valorite the reviews and server
checks (P671). The overseer may reassign.

**Waves.** Prompts in one wave can run in parallel: they touch different files, and each takes the shared locks
(`docker-build`, `test-shard`, `package`) only for its build and proof. Each wave starts when the one before has
merged.

| Wave | Prompts | Lands |
|---|---|---|
| 1 | S1 delivery, S2 server map data, S3 regions (towns), S8 old dungeons and our seeders | built in parallel, **live together** with S7 |
| 2 | S7 New Haven and Rootdeep, S4 moongates and teleporters, S5 stock decoration | S7 must join wave 1's go-live; S4 and S5 straight after |
| 3 | S9 stock spawns, S10 new towns' people, S6 the author's 775 lines, S11 treasure, houses and boats, S12 champions | parallel; any order |
| 4 | S13 Felucca's regions, S14 fences for the unfinished areas, S15 walk survey and bot routes | parallel |
| 5 | S16 credits and docs, S17 the whole-world playthrough (the 1.0 gate) | last |
| After 1.0 | S18 the author's dungeons spawned and opened, S19 finishing the unfinished land | one area per prompt |

**Must land together (the swap go-live on the test shard):** S1, S2, S3, S7 and S8. The client and server must show the
same land (S1 + S2). Without S3, guard zones and town rules cover the wrong ground. Without S7, new characters start in
a forest. Without S8, Blackthorn's generator scatters its items into the author's dungeons. A package version floor
(S1) keeps an old client off the swapped server.

---

### S1. The Siege of Sosaria map in the player package, for Trammel and Felucca

**Model:** Opus · **Touches:** package, client · **Golem:** Iron · **Size:** L

**Summary:** Ship the SoS map as a package vendor asset kept outside git, packed for TazUO's map 1 and map 0, so
Trammel and Felucca both draw it. Our `trammel.mapops` applies on top of it as today.

1. **The asset.** The author's `Map1.mul`, `Staidx1.mul` and `Statics1.mul` (141.7 MB) go in a vendor folder outside
   the repo. The repo keeps a manifest: SHA-256 of each file, the source URL, `SOURCE.txt` with the author's terms and
   credit (S16's wording). The package build fetches or copies them and refuses on a hash mismatch.
2. **Packing for TazUO.** The override names a UOP (`map1legacymul.uop=` in `files-override.txt`). Extend `mapops.py`'s
   `synthetic_facet` to pack the MUL into `map1LegacyMUL.uop`. **Felucca:** a UOP's entries are hashed by name
   (`build/map1legacymul/...`). So map 0 needs its own pack, with `map0` names over the same tile data; pointing
   `map0legacymul.uop=` at the map 1 file would miss every hash. Statics are MULs, so both overrides can name one
   `statics1.mul` and `staidx1.mul` pair. Check that on TazUO before relying on it, or copy them.
3. **Download size.** Ship the map 1 pack (about 37 MB zipped) and build the map 0 pack on the player's PC at first
   start. That is a name rewrite in `Apply-MapOps.ps1`, after our mapops lines are applied to map 1, so both match.
   Measure the first-start time and the disk use (about 90 MB more), and compare with shipping both packs.
4. **The launcher's stamp** covers the new files, so later starts skip the rebuild. Art is unaffected (a map is not
   art), and P670's redrawn statics still apply.
5. **A package version floor:** the server refuses, with a plain message, a client whose package predates the swap.
   A stale client would draw stock land under SoS walls.
6. **Gate 4** (no EA files) still holds: the SoS files are the author's, built on EA's terrain. The README line from
   P670 ("No EA game file is included") still reads true.
7. **Proves:** on a private world with S2's server, TazUO from the built package shows SoS at Valunstead (479, 388),
   at the author's Haven and at site A's void, on both Trammel and Felucca. The download and disk sizes, the
   first-start time, and the package gates green. Take the `package` lock.

### S2. The server reads the SoS map, Felucca on the same file, and the Fold's mirror moves

**Model:** Opus · **Touches:** server, docker, map · **Golem:** Iron · **Size:** M

**Summary:** The server's map overlay puts the SoS files first for file index 1. Felucca reads file index 1. Our
`trammel.mapops` is re-based onto SoS. P661's mirror region moves off the author's cave.

1. `Build-MapOverlay.ps1` and `dataDirectories`: the SoS files (or S1's map 1 pack) first. Check the reader's order
   (UOP before MUL) so pinned's own `map1LegacyMUL.uop` never wins.
2. **Felucca:** file index 1 in code, the way `FoldMaps.cs` registers maps (a customization `Configure` after
   `MapLoader.Configure`), not a JSON patch. Its rules and map id 0 stay.
3. **Re-base `trammel.mapops`:** a pristine SoS copy with its hashes in `ORIGINAL-SHA256.txt`. The Burrows' 210 blocks
   apply as they are (void SoS left alone); `check` reads drifted 0, missing 0 for them. The 2 way-in blocks at
   3608-3623, 2616-2623 collide with the author's Haven and are dropped here; S7 makes the new way in.
4. **The Fold** (section 1.4): `FoldMirrorRegion` moves to 6160-7167, 3744-4095 with a Felucca twin. The `[Fold goto`
   default becomes 6638, 3993. `FoldVerification` follows.
5. **Proves:** facts, each seen failing first. A player on Trammel, on Felucca and on map 32 at Valunstead stands on SoS's
   tile and Z. A player inside Passage of Lost Souls level 2 (6202, 2116) is not moved. One at 6638, 3993 on Trammel or
   Felucca is sent to New Haven. Then `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green, and TazUO shots with S1's
   client.

### S3. Trammel's regions and guard zones redrawn on the SoS land

**Model:** Opus · **Touches:** server data (`regions.json` patch) · **Golem:** Valorite · **Size:** L

**Summary:** Redraw Trammel's 145 regions where the land moved, and add regions for the author's new towns and
dungeons. His `Regions.xml` is the reference (ServUO format, read only; `notes\sos-map-author-spots.md`).

1. 54 regions are 75 percent or more changed, 47 from 25 to 75 percent (`out\stock-regions.csv`). Redraw each to the
   SoS town, keeping the stock name, since 19 of our files look regions up by name. Guard zones follow the new town
   walls.
2. New town regions, guarded: Valunstead, Hammerhill, Kameron Kove, Elmhaven, Kettleburg, Fort Yondall, Elandrim Nur
   Shaz. Wild regions for Glimmerwood, the Nujel'm desert and the 65 new islands. Dock regions where his docks are.
3. His dungeons: a `DungeonRegion` each (no housing, dungeon light, no recall in where stock does the same). Sealed by
   S14 until S18 opens each one.
4. A no-housing region over every unfinished area in S14's list.
5. **Proves:** every region's rectangles lie on dry SoS land or its own water. No guard zone covers open wild. A
   region-name fact for the 19 lookups. Build green. A top-down picture of the regions over the SoS radar map.

### S4. Moongates, teleporters and the staff go-menu

**Model:** Opus · **Touches:** server, patch · **Golem:** Valorite · **Size:** M

**Summary:** Re-place the public moongates on both facets, fix the stock teleporters, and give staff the author's
go-menu.

1. `PMList` Trammel and Felucca: Moonglow, Britain, Yew and Minoc need rework; Trinsic, Magincia and New Haven (on
   Felucca, Bucs' Den) moved. Each gate goes on the author's ring where he built one (Britain: the rock ring round a
   tree). The New Haven gate goes in S7's town.
2. His extra gate spots (Hammerhill 1541, 1081; Kameron Kove 1353, 2451; Dragonstorm 3186, 3884) get their moongate
   statics left as decor. They join the gate list only when the facet-access design gates them (P669 5b). Default: not
   in the list at 1.0.
3. `teleporters.json`: 60 Trammel ends and 72 Felucca ends need rework, and 180 and 234 moved. Each is re-placed onto
   a walkable tile or dropped with a reason. Dungeons whose entrance SoS rebuilt are walked in client.
4. The staff go-menu: the author's `Locations\trammel.xml` (410 spots) converted to our go-menu format.
5. **Proves:** a fact that every gate destination and teleporter end stands on walkable SoS land. A TazUO shot at each
   moongate. Build green.

### S5. Stock decoration on the new land

**Model:** Opus · **Touches:** server data (decoration cfg patch), tools · **Golem:** Iron · **Size:** L

**Summary:** Keep stock decoration where the land is unchanged. Re-place what still has a building to belong to. Drop
the rest.

1. A tool grades each of the 25,568 Trammel and 26,107 Felucca decoration items (P669's `geo.py` rules). It keeps
   unchanged items; re-places doors, signs, forges, anvils, banks' fittings and books onto the matching SoS building
   by its statics; and drops items in water, in void, under impassable statics, or inside a block SoS rebuilt with no
   match. Counts to start from: 2,371 + 2,163 rework, 4,774 + 5,065 to check.
2. Every dropped and moved item is listed in a CSV with its reason.
3. **Proves:** no item in water or void, and no door hanging outside a doorway (a fact over the cfg). Renders of
   Britain, Moonglow and Minoc with the decoration placed. Build green.

### S6. The author's 775 decoration lines for his dungeons

**Model:** Opus · **Touches:** server data · **Golem:** Verite · **Size:** M

**Summary:** Port `SOS Trammel Dungeons.cfg` (ServUO decoration: doors, teleporters and props) to ModernUO's
decoration format, as data for Trammel and Felucca.

1. Convert each line; map ServUO types to pinned's (list any with no match). Credit line in the file header.
2. **His teleporters into a dungeon S18 has not opened stay out** (a list kept in the file), so the dungeons are sealed
   by the absence of their way in. Doors, props and the teleporters inside a dungeon go in.
3. **Proves:** each converted type exists in pinned; every teleporter's two ends are walkable; build green.

### S7. New Haven moves into the author's Haven, and Rootdeep's way in

**Model:** Opus · **Touches:** server, map, package (cliloc) · **Golem:** Iron · **Size:** L

**Summary:** The start city and everything we built round it move to the author's Haven (3614-3722, 2516-2657: Uzeraan's
Mansion, docks, smithy, bank). The old plaza is forest and shore on SoS. Rootdeep's way in becomes a cellar hatch in
the town.

1. **One place for the spots:** `HavenSpots` holds the start (`CharacterCreation`'s city, today 3503, 2574, 14), Rook, the
   New Haven moongate, the bank, the healer, the stable vet, the dock, and the island gate's Haven bounds. The Fold
   mirror's send-to and the isle dock moongate read it.
2. **Seeders moved:** `ClusterFNewHavenSeeder.cs` (1 rework, 2 moves), `ClusterFNewHavenServicesSeeder.cs`,
   `NewHavenQuestBoard.cs`, `ClusterFResetStone.cs`, `FountainOfYouth.cs`, `ApprenticeTraining.cs`,
   `TutorialRecruiter.cs`, and the trade and wing trials (15 `Map.Trammel` uses that stay in New Haven, P481 12.3).
   `TutorialCorePlacement.cs` (8 rework) retires when P663 moves the core to the isle. Until then its stations sit in
   the new town.
3. **Regions:** "New Haven" and its shop regions are redrawn over the town, with the same names. The stock region
   "Haven" is folded into it or kept for the mansion.
4. **Rootdeep:** a cellar hatch in a town building leads down to the Burrows' Landing (the rope ladder and teleporter
   rule from playbook 6). The hatch is a `trammel.mapops` block or a server item, whichever leaves the town's statics
   untouched. `OldHavenBurrowsRegion.cs` and `ClusterFOldHavenStockSpawns.cs` follow.
5. **The achievement** "found the ruins of Old Haven" (`ClusterFAchievements.cs:172`) is reworded to the hatch (draft:
   "found the way beneath Haven"). Its key stays, so players who earned it keep it.
6. **Proves:** facts for a new character's start, Rook and the moongate at their spots. The P289 bot route from the
   start to the bank and back. The Rootdeep walk from the hatch to the Landing, with the playbook's flood fill. TazUO
   shots of the town. Build green.

### S8. Our code and EA's later dungeons on the new land

**Model:** Opus · **Touches:** server, patch · **Golem:** Valorite · **Size:** L

**Summary:** Fix the 12 of our files that need rework, and check the 18 that moved (P669 `out\geo-files.csv`), except
those S7 owns.

1. **Blackthorn:** its dungeon area (6151-6563, 2301-2839) now holds the author's dungeons. `BlackthornDungeon/Generate.cs`
   (61 rework) and `Region.cs` (8) are switched off before the 1.0 world is generated (Chase's question 3). The test
   world's Blackthorn items are deleted at go-live.
2. Despise revamped `Setup.cs` (6 rework, 14 moves), `WrongDungeon/Generate.cs` (2 rework),
   `StealableArtifacts-servuo-entries.patch` (44 rework, 38 moves): each spot is re-placed on SoS's version of the
   room or dropped.
3. Seeders and layouts: `ClusterFInstitutionSeeder.cs` (4), `ClusterFMineCampLayout.cs` (6), `ClusterFSouthMineDecor.cs`
   (4), `ClusterFGuildHallPlacementData.cs` (12 rework, 28 moves),
   `ImportCleanupTests-guid-key.patch` (6, Felucca).
4. The 293 "moves" literals (P669) are walked by a fact: each spot must be dry, open and within 5 Z. Those that fail
   are fixed here.
5. **Proves:** a fact over every coordinate literal left in these files. Build green.

### S9. Stock spawners on the new land

**Model:** Opus · **Touches:** server data (spawn JSON patch) · **Golem:** Verite · **Size:** L

**Summary:** Fix the pinned Trammel and Felucca spawners (2,182 and 2,122): rework 345 and 306, check 496 and 505.

1. Vendor and town-NPC spawners first: re-placed into the SoS building that holds that trade, or a new spot in the
   town.
2. Wild spawners: moved onto the nearest matching terrain within 20 tiles, or dropped.
3. **Proves:** a fact that every spawner's home and range lie on walkable land. Every town has its bank, healer,
   smith and provisioner. Build green.

### S10. People for the author's new towns and keeps

**Model:** Opus · **Touches:** server (spawn data, seeders) · **Golem:** Verite · **Size:** L (may split per town)

**Summary:** The author ships no spawns. Give his new towns vendors, guards and townsfolk: Valunstead, Hammerhill,
Kameron Kove, Elmhaven, Kettleburg, Fort Yondall. His keeps (Fort Whitestone, Castle Dunbain, Fort Stormhammer,
Tigerclaw, Khalahandra Keep) get a small garrison. Verite's quest seeds (P672) name who lives there.

1. One spawn file per town, built from the town's buildings (shop by its statics: forge, loom, counters).
2. Wild creatures on the new land: the Nujel'm desert continent, Glimmerwood and the 65 new islands, matched to the
   terrain (desert, forest, snow, swamp) from stock's terrain-to-spawn tables.
3. **Proves:** every town has a bank and a healer. A spawn density figure per 100 dry tiles, against stock's.
   Build green.

### S11. Treasure maps, houses, boats, docks and SOS bottles

**Model:** Opus · **Touches:** server data, server · **Golem:** Valorite · **Size:** M

1. `treasure.cfg`: 70 spots rework, 66 checked; new spots on the new land (about one per 7,000 new dry tiles, as
   stock's density), none in a town or an unfinished area.
2. Houses: placement follows the land. The new towns and the author's dungeons are no-housing (S3). Nothing exists to
   orphan in a fresh world. The test shard's houses follow Chase's question 2.
3. Boats and docks: boat placement and dock regions at the author's docks. A test that a boat placed at each dock
   floats.
4. SOS bottles pick random water at runtime (`SOS.cs:168-180`). A fact that 1,000 picks never land in the new desert,
   in void, or inside the isle's box.
5. **Proves:** facts above; build green.

### S12. Felucca's champion spawns

**Model:** Opus · **Touches:** server · **Golem:** Valorite · **Size:** S

1. `GenChamps.cs`: 17 champions; 11 unchanged, 3 moved, 3 rework. Each altar and its spawn area go onto walkable SoS
   land, with the area clear of town guard zones.
2. **Proves:** a fact per altar; build green.

### S13. Felucca's regions

**Model:** Opus · **Touches:** server data · **Golem:** Valorite · **Size:** M

1. Felucca's 272 region rectangles (33 rework, 54 moved) are redrawn from S3's Trammel work. The towns match. Felucca's
   own rules stay (guards where stock Felucca has them, Bucs' Den unguarded).
2. **Proves:** S3's region facts for Felucca; build green.

### S14. Fences for the unfinished areas and the sealed dungeons

**Model:** Opus · **Touches:** server, map · **Golem:** Iron · **Size:** M

**Summary:** For 1.0, the author's unfinished land is fenced rather than finished.

1. **The list** (`out\unfinished.csv`): the rooster island (2840-3039, 1324-1523); the north-east snow isles with
   their hard-edged town paste (4224-4479, 256-767); bare land east of Haven (3072-3199, 2304-2559); the cells round
   Echoback and Darkfathom (4096-4223, 2560-2815).
2. **A fence region each:** players who enter are turned back to the last shore with a line ("Thick fog rolls in;
   the way is lost"). No housing. Boats can sail by.
3. **Cliff seams** (107,741 uncovered against stock's 55,297): a seam-dressing pass covers seams within 40 tiles of a
   town, road or moongate with stock cliff and rock statics, as `trammel.mapops` lines. The worst cells (Glimmerwood
   2688-2943, 2688-3071; the north-east isles) are fenced instead. Report the patch size against the 5 MB rule.
4. **Sealed dungeons:** for each of the author's dungeons with a walk-in entrance (not a teleporter, which S6 leaves
   out), a fence region at the entrance. S18 removes it when the dungeon is spawned.
5. **Proves:** renders before and after of three dressed seams; a fact per fence region; `check` drifted 0. Build
   green.

### S15. The walk between places, and the bot's routes

**Model:** Opus · **Touches:** tools, bot · **Golem:** Iron · **Size:** M

1. **A flood fill over SoS** with pinned's movement rules reduced to the files (playbook 6). It runs from every town
   bank, moongate and dock, and lists which places cannot reach each other on foot. P669 did not measure this. Fixes
   (a cleared gap, a teleporter) go to the prompt that owns the area.
2. The bot's points: `checks_p224_guilds.py` and `checks_p224_vbuild.py` (moved), the P289 tutorial route, and the
   nightly bot's routes.
3. **Proves:** the reachability table in the notes; one nightly bot run on a private world green.

### S16. Credits, the fidelity register and the wiki

**Model:** Sonnet · **Touches:** docs, package · **Golem:** Verite · **Size:** S

Section 4's list: the package README, `SOURCE.txt`, the CHANGELOG player line, the in-game patch notes, the fidelity
register's row (`docs\fidelity-principle.md`), and the shard wiki's world-map page.

### S17. The whole swapped world, played through (the 1.0 gate)

**Model:** Opus · **Touches:** tests, private world · **Golem:** Iron · **Size:** L

1. A fresh private world with everything above, from the built package. Two clients: character creation (both start
   choices), the isle (P662 to P664), the dock moongate to New Haven, every public moongate on both facets, one walk
   to each new town, Rootdeep by the hatch, a boat from a dock, a treasure map dug, a Felucca champion seen.
2. A list of what failed, each assigned to the owning prompt for a fix.
3. **Proves:** the playthrough log and shots; the go-live checklist for 1.0.

### S18 (after 1.0). The author's dungeons, spawned and opened, one or a few per prompt

**Model:** Opus · **Touches:** server data · **Golem:** Verite · **Size:** M each

His 20+ custom dungeons (`out\spots.csv`, "Dungeons", "new or rebuilt"): spawns from stock's dungeon tables by
level, S6's held teleporters placed, S14's fence removed. Order by where the quest seeds (P672) point first.

### S19 (after 1.0). Finishing the unfinished land, one area per prompt

**Model:** Opus · **Touches:** map · **Golem:** Iron · **Size:** M each

By the playbook: the rooster island, the north-east snow isles (blend the paste), east of Haven, Echoback and
Darkfathom, Glimmerwood's seams. Each lifts its S14 fence.

## 3. Order against 1.0

| When | What | Why it cannot wait, or can |
|---|---|---|
| **Go-live on the test shard** | S1, S2, S3, S7, S8 together (waves 1 and 2) | Client and server must agree. New characters need a start city, guard zones must sit on the towns, and old generators must not run into the author's dungeons |
| Straight after | S4, S5 | Gates and teleporters that drop players in walls, and decoration floating in water, are the first bugs players hit |
| Before 1.0 | S9, S10, S11, S12, S13, S14, S15, and the isle (P662 to P666) | A playable world: people in every town, monsters in the wild, treasure, boats, Felucca's rules on its land, unfinished areas fenced, routes walked |
| The 1.0 gate | S16, S17 | Credit before any player sees the map; the full playthrough |
| **Can wait past 1.0** | S18 (his dungeons, sealed until spawned), S19 (finishing the land), the extra moongates as unlocks | Players have the stock dungeons (Despise, Shame, Covetous, Wrong, Destard and the rest, fixed in S8) and the whole surface. Sealed dungeons are a promise, not a hole |

**Prompt count:** 17 before 1.0 (S1 to S17), plus the isle's 5, plus S18 and S19 after. That is within P669's 20 to
25, because the plan fences rather than finishes for 1.0.

## 4. Credit and terms

**Terms** (overseer's `notes\sos-map-author-spots.md`): the author invites reuse ("take advantage to your hearts
content"), with no license file. His update 2 says it is the final update, so we maintain our own copy from here on.

**Where his credit appears:**
- **The package README** (`player-package\payload\README.txt`, "What is in here"): a line for the map beside P670's
  line for his redrawn art, naming "Siege of Sosaria Trammel Map 3.0 by Zigholtul" and saying Trammel and Felucca are
  built on it.
- **`SOURCE.txt`** in the vendor asset folder: source URL, version, his terms quoted with the date read, and our
  changes listed (the mapops lines, the fences).
- **The CHANGELOG player line** on the swap day, and the in-game patch notes.
- **The shard wiki's world-map page,** and the fidelity register's row. Trammel's geography is no longer OSI's, so the
  wiki, not the outside guides, documents it.
- **Data files:** the converted decoration (S6) and the regions taken from his `Regions.xml` (S3), with a header line.
- **Place names we use** (P672's rule): credited to him; the stories are ours.

**Custom art: none needed.** All 8,683 item ids SoS uses have art in the stock 7.0.117.0 art file, and its 7 land ids
without art are EA's own, used as in stock (P669). He ships only the map, index and statics, with no tiledata, hues or
multis, so nothing else changes. The isle uses only stock art (P481 11.2). P670's redrawn statics stay an opt-in look,
separate from the map. Screenshots of his map elsewhere may show that replaced art, which a player without the tick box
will not see.

## For Chase

1. **Where does New Haven go?**
   - **Into the author's Haven town (recommended).** It stands on the old Old Haven site, already has a bank, docks, a
     smithy and Uzeraan's Mansion, and keeps the name, so every "New Haven" lookup still works. Rootdeep's way in
     becomes a cellar hatch there.
   - Build a new New Haven plaza on the forest where ours stood (3500, 2585): one more map prompt, and it sits beside
     his town.
2. **The test shard on swap day: what happens to its characters and houses?**
   - **Keep characters and their banks (recommended).** Every character is moved to the new New Haven. Houses standing
     on land SoS changed become deeds in their owner's bank. World items (decoration, spawners, Blackthorn) are
     regenerated.
   - A fresh test world, as 1.0 will be.
3. **EA's Blackthorn dungeon:** SoS put the author's dungeons on its site.
   - **Drop it for 1.0 (recommended).** It is a later EA dungeon with no place on his map. It could come back on the
     Fold's zone 5 after 1.0.
   - Move it now into the Fold's zone 5 (one more map and server prompt before 1.0).
4. **What stays closed at 1.0?**
   - **Fence the unfinished land and seal his dungeons until each has monsters (recommended).** S14 at 1.0; S18 and S19
     open them one by one after.
   - Finish everything before 1.0: about 6 to 10 more prompts, and 1.0 moves.

## Deviations, checks and commit preflight

- **Not run (permission denied in this unattended run):** I wanted to grep the code work copy
  (`D:\UO\golems\Iron\ShatteredLegacy\server`, `*.cs`) for the void C coordinates (6214, 6160-6639, 1832-2279, 6170-6441,
  1913-2057). I wanted the exact lines the isle re-site touches in our code. Instead, section 1.4 names the files from
  P661's notes (`FoldRegions.cs`, `FoldCommands.cs`, `FoldVerification.cs`). The prompt that edits them should grep
  first.
- **Measured here:** the site scan and checks (`out\sites.csv`, `out\sitecheck.json`). Every other count is P669's.
- **Not measured:** the walk between places (S15 does it). TazUO's override with two maps on one UOP (S1 checks; I
  expect the hashed names to need a second pack). The first-start time with a 142 MB base.
- Nothing asked through Ask-Chase: the prompt wants decisions in this list. Nothing built, deployed or locked; Haven
  not touched.
- **Files (shard-migration):** this note; `notes\cc-P673-tools\` (`sitefind.py`, `sitecheck.py`, `out\sites.csv`,
  `out\sites.json`, `out\sitecheck.json`); `notes\art\sos-isle-site\` (7 PNGs). No code and no map files changed. Code
  work copy untouched. Branch `golem/Iron/P673`; not committed (the Golem commits).

P673 DONE
