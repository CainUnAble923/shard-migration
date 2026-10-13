# cc-P76: Extra facets research (downloaded custom maps as added facets)

Run 2026-10-12 by Claude Code (autopilot hand-off after P75). Notes only: no code, no build, no patch notes, no deploy.
The brief's Part B target `docs\design\extra-facets.md` is this file, since agents never edit `docs\`.

Sources:
- Pinned engine `D:\UO\ModernUO-pinned` at **`d4531cd94b739613155225c234900de9f47d2c88`**.
- Our TazUO: **v26.0909.63, commit `3212623f`**. Source at `D:\UO\cc-p40-work\tazuo-3212623f`; the installed client is
  `D:\UO\TazUO`.

**Provenance.** Three research subagents read the server, the client and package, and the four candidate maps (byte
by byte, with scripts in the session scratchpad). Each cited file:line, and the citations below are theirs, except
where this note says it re-read something:
- I re-read the server's map-ID comment (A.1).
- I checked that the UltimaLive sender one agent cited exists only in the stale `server\uo\` tree, not in
  `server\customizations` (A.2). The shard has no UltimaLive code.

Short names:
- **P** = `D:\UO\ModernUO-pinned\Projects`.
- **T** = `D:\UO\cc-p40-work\tazuo-3212623f\src`.
- **TP** = `D:\UO\third-party`.
- **PKG** = `D:\ShatteredLegacy\player-package`.

---

## Part A: facts

### A.1 ModernUO: how a facet is defined, read and used

**Definitions:** `Distribution\Data\map-definitions.json`, read by `P\Server\Maps\MapLoader.cs:47-101`
(`[CallPriority(2)] Configure`, which reads `Data/map-definitions.json` at :53).
- Fields per map: index, id, fileIndex, name, width, height, season, rules.
- Stock: Felucca 0 to TerMur 5, plus Internal 127.
- `RegisterMap` is private (:103-118); there is no public API, so **a new facet is one entry in that JSON**. The shard
  overrides no Distribution data today. The Dockerfile copies pinned's Data folder (`docker\uo\Dockerfile:97`), so the
  entry ships as a data patch or a copy step.

**Three numbers per map** (re-read: `P\Server\Maps\MapLoader.cs:31-44`):
- **index:** the slot in `Map.Maps[0x100]`. 0-31, 127 and 255 are reserved for core, so **custom maps use 32 to 126**.
- **id:** what the client is sent, one byte. The comment says "for any visible maps, this value must be from 0-5".
  That is written for the stock EA client; nothing found in pinned enforces it (A.2: TazUO takes more).
- **fileIndex:** which data files the server reads (`map{N}.mul`, `staidx{N}.mul`, `statics{N}.mul`).
- **MapRules:** flags (`P\Server\Maps\Map.cs:29-39`). Trammel rules restrict harm and movement; Felucca rules restrict
  nothing.

**Files** (`P\Server\TileMatrix\TileMatrix.cs:101-160`, by fileIndex):
- the map: `map{N}.mul` first (:105), then `map{N}LegacyMUL.uop` (:113);
- statics: `.mul` only (:132, :144);
- diff files are off for client 7.0.117 (`TileMatrixPatch.cs:57-69`);
- data path: `Core.FindDataFile` over modernuo.json `dataDirectories` (`P\Server\Main.cs:346-350`);
- **missing files only log a warning, and the map is empty** (:128, :141, :152). No crash.

**What a new facet needs server side:**
- **Works on any registered map:**
  - regions (`Data\regions.json`, by map name; 398 regions, 145 on Trammel);
  - teleporters (`Data\teleporters.json`);
  - decoration (`Data\Decoration\<Map>\*.cfg`; `Decorate.Generate(folder, maps)` is public static, `Decorate.cs:52`);
  - spawners (`Data\Spawns\...\<map>\*.json`);
  - housing, by `Region.AllowHousing` (`Region.cs:793`);
  - travel, by region (`SpellHelper.cs:637-645`);
  - shard code that already loops all maps (`ClusterFStaffHub.cs:576`, `:609`).
- **Assumes the six maps:**
  - `MapSelectionFlags` has six bits and expansions.json six booleans (`MapSelection.cs:8-16`, `:55`), which our
    `CharacterCreation.cs:286-356` uses: only for starting maps, so an added facet need not be startable.
  - Public moongates are a hard-coded list per map (`Items\Misc\PublicMoongate.cs:177ff`): a new facet has no gate
    unless it is added there.
  - `[go` picks a locations file per map and falls back to Felucca (`GoLocations.cs:20-47`): it needs a small patch for
    a seventh map.
  - Decoration folders are hard-coded per map (`Decorate.cs:37-46`): a shard command can call `Generate` with ours.
  - Per-map travel zones (`SpellHelper.cs:666-797`): a new facet simply has none of them.
- **How the shard builds content today:**
  - Regions are code (`server\customizations\Regions\OldHavenBurrowsRegion.cs`, a `DungeonRegion` registered in
    `Initialize`, cc-P36).
  - Placements are C# seeders on `EventSink.WorldLoad` (11 `ClusterF*Seeder.cs` files).
  - A new facet can be added the same way, plus its JSON entry.

### A.2 TazUO: map count, sizes, files

- **Count and sizes:** a static table of six maps (`T\ClassicUO.Assets\MapLoader.cs:23`, `:38-59`).
- **It can be extended two ways, neither needing code:**
  - **(a) The `maps_layouts` setting** (`T\ClassicUO.Client\Configuration\Settings.cs:98`; also `-maps_layouts` on the
    command line, `Main.cs:439-441`). It replaces the count and the whole size table, `w,h;w,h;...`, all maps listed
    (`MapLoader.cs:102-133`). Ours are `null` today (`D:\UO\TazUO\client\settings.json:33`).
  - **(b) A server packet:** 0x3F subcommand 0x10, "dynamic map definitions" (`T\ClassicUO.Client\Game\UltimaLive.cs:286-333`).
    It is registered unconditionally and needs no UltimaLive session; it resizes and reloads the maps. ModernUO has no
    sender for it.
- **Files per index** (`MapLoader.cs:139-214`):
  - `map{i}LegacyMUL.uop` on a UOP install if present, else `map{i}.mul`;
  - `staidx{i}.mul` and `statics{i}.mul` in either case;
  - diff files only in the .mul branch.
- **Unknown index, no crash:** `World.MapIndex` puts an out-of-range index on Felucca (`World.cs:208-211`), and a
  missing map file falls back to index 0 (`MapLoader.cs:365-368`).
- **The world map** draws itself from the map files (`Map.GenerateMapPng`, `Map.cs:488-514`) and lists `MAPS_COUNT`
  facets (`WorldMapGump.cs:393`, `:716`), so an extra facet appears.
  - **Ship a statics and staidx file even if empty:** `GenerateMapPng` opens the statics path without a null check
    (`Map.cs:509-514`).
- **Smallest client change: none in code.** Our launcher passes `-maps_layouts` with eight sizes (or the settings key).
  Since `Update.ps1` never overwrites `app\tazuo\settings*.json`, the command-line switch from `Play.ps1` reaches
  existing installs.

### A.3 The player package

- **Our own files ship now through TazUO's override list.** `-uofilesoverride` maps any lowercase file name to a path
  (`T\ClassicUO.IO\UOFilesOverrideMap.cs:30-46`; `UOFileManager.cs:103-108`).
  - The precedent is `sl-anim7.bin` given to TazUO as `anim7.mul` (`PKG\payload\app\Build-UoOverrides.ps1:38-43`, `:281`).
  - Map files ship the same way: `sl-map7.bin` as `map7.mul`, `sl-staidx7.bin` as `staidx7.mul`, `sl-statics7.bin`
    as `statics7.mul`.
  - The package build refuses `.mul`, `.uop`, `.idx` and EA-named files (`PKG\Build-PlayerPackage.ps1:35-36`,
    `:247-251`), so the neutral names are needed.
  - Add the anim7-style refusal if a player's folder already holds that map index.
- **The client policy:**
  - "Custom client" covers "our own client data (art, map, tiledata, gumps)" (`SM\notes\client-policy-2026-10-02.md:14`).
  - The rule is "ship patches from us, not EA's files" (:15-17).
  - A whole new map file made entirely by a community author, with no EA bytes, reads as allowed. The policy does not
    name whole new map files, so **Chase should confirm** (section B.6).
- **Size:**
  - The package zip is **80,158,779 bytes** today (`dist\ShatteredLegacy-2026.10.06.0638.zip`).
  - Updates download the whole zip (`Play.ps1:84-172`), and `Update.ps1` backs up `app\` in full each time.
  - So a big map rides along with every update unless it is split into its own download (not designed yet). The
    per-candidate sizes are in A.4.

### A.4 The candidates (measured from the files; numbers counted, not estimated)

All are `.mul`, none `.uop`. Every dimension checks out from the file sizes (map bytes / 196 = blocks; staidx bytes
/ 12 = the same blocks).

| Candidate | Size | Map + used statics | Statics placed | Art not in stock | Terms (SOURCE.txt) |
|---|---|---|---|---|---|
| **sos-trammel-map** (Siege of Sosaria Trammel 3.0, Zigholtul) | **7168x4096** | 89.9 MB map + 27.1 MB used statics (the file is 46.3 MB; 19.1 MB unreferenced) | 3,875,783 (8,683 distinct IDs) | **16 static IDs (26 statics) and 7 land IDs (40 cells)**, all OSI "UNUSED" placeholders | "feel free to take advantage to your hearts content"; no license file; credit him |
| **paranoia-custom-map** (ParanoiaPhD) | **6144x4096** | 77.1 MB + 95.5 MB statics | 13,648,333 (879 IDs) | **1 land ID (2 cells)** | none stated; credit; ship only inside the package, never repost |
| **dungeon-map-4** (TheArt) | **1448x1448** | 6.4 MB + 0.9 MB used statics (the file is 44.7 MB; 43.8 MB unreferenced) | 130,064 (458 IDs) | **ID 0xC000, 40,467 times**, a filler at z 0 with no art slot (strip or remap) | "as is"; no license; credit TheArt |
| **termur-replacement** (TheArt) | **1280x4096** | 16.1 MB + 0.4 MB used statics | 53,788 (606 IDs) | **none** | "as is"; no license; credit TheArt |
| **calypso** | - | - | - | - | **Not downloaded**: `TP\download-queue.md` row #75 "todo" (the daily limit, 2026-10-12). Skipped |

**Notes on the table:**
- **Rewriting the statics drops the unreferenced bytes:** SoS loses 19 MB, dungeon-map-4 44 MB. Any copy tool does
  this.
- **The Siege of Sosaria art kit does not cover the SoS map's missing IDs.**
  `TP\paperdoll-siege-of-sosaria` holds 29 item BMPs (hair, 0x3B6F to 0x3B8A, and angel wings 0x3C89) and gumps, no
  map art. The 23 missing tiles are 66 placements in a 7168x4096 map: replace or delete them.
- **SoS ships ServUO data for its own map:**
  - **Regions.xml:** 150 Trammel regions (23 nested) over 1,128 rectangles, every type present in ModernUO.
  - **Locations\trammel.xml:** 410 places in 112 groups.
  - **SOS Trammel Dungeons.cfg:** 201 teleporters. One entry may be malformed: 200 coordinate lines were counted.
  - **Conversion:** decoration is ModernUO's own format (change `MapDest`), about 1 hour. Locations need an XML-to-JSON
    script, about 1 hour. Regions need a converter (rect x,y,w,h to x1..x2; z ranges; go; entrance; rune; logout
    delay; nested parents), 0.5 to 1 day plus review. Spawners and moongates are not in the data.
  - Its Regions.xml also covers a "Sosaria" facet with 132 regions whose map files are not in the download.
- **Tools on disk: none.** CentrED/CentrED+, UOFiddler, RadCopy, MapCopy, UOLandscaper and Mulpatcher are all missing
  (searched `D:\UO` and `D:\ShatteredLegacy` at full depth). What Chase would need (not downloaded):
  - **UOFiddler** to inspect art and IDs, and to repack a map to .uop if ever wanted;
  - **CentrED+** (client and cedserver) to edit, trim and fix the 23 missing tiles, or the 0xC000 filler;
  - **RadCopy** (SoS's author invites it) to copy regions between maps.
  A small Python script can do the renumbering (file names) and the statics rewrite. That is ours to write when wiring
  starts.

---

## Part B: proposal

### B.1 In plain language

- **The server:** ModernUO can add a facet with one entry in its map list and the map's three files. Missing files do
  not crash it.
- **The client:** our TazUO can show more than six maps with a single setting our launcher can pass, and extra files
  ship through the package as our own files, the way the worn-item animations already do. Nothing in either needs a
  code change to try it.
- **The candidates:**
  - **termur-replacement** is small (16 MB) and needs no new art;
  - **dungeon-map-4** is small but carries 40,467 tiles of a filler with no art, to be stripped;
  - **Paranoia** is big (173 MB) and nearly clean;
  - **Siege of Sosaria** is big (117 MB after trimming), the richest, needs 23 tiles fixed, and comes with region and
    dungeon data worth about two days to convert.
- **The cost that matters is size:** the package is 80 MB and is downloaded whole on every update.

### B.2 Slot plan (all names are placeholders)

New maps take server **index 32 and up**, and client map **ids 6 and up** (the client's own index; TazUO is told the
sizes). The server's fileIndex equals the client id, so `map6.mul` serves both.

| Server index | Client id / fileIndex | Candidate | Size | Working name (placeholder) | Why the name |
|---|---|---|---|---|---|
| 32 | 6 | termur-replacement | 1280x4096 | **The Proving Ward** | the League's training ground; the "Training Ward" |
| 33 | 7 | dungeon-map-4 | 1448x1448 | **The Hiltdeeps** | dungeons under the broken sword's hilt |
| 34 | 8 | sos-trammel-map | 7168x4096 | **Sosaria Before** | a looped, older Sosaria: the world as it was a turn of the loop ago |
| 35 | 9 | paranoia-custom-map | 6144x4096 | **The Unwritten Reach** | the League's frontier: land the loop has not drawn yet |

**Order:** smallest and cleanest first. Index numbers are kept even if a candidate is dropped, so a facet's index
never changes once a world holds items on it.

### B.3 Uses and what each would take

- **The Proving Ward (termur-replacement):**
  - **Use:** the Training Ward (a private, rule-light ground for the tutorial's trial room, F-35 step 0, or skill
    practice); seasonal events; a League muster town.
  - **Takes:**
    - the client setting and three files in the package (16.4 MB, under 1 MB of statics after the rewrite);
    - the map entry; a code region (the Burrows pattern) with travel rules;
    - one teleporter in and out;
    - no art.
- **The Hiltdeeps (dungeon-map-4):**
  - **Use:** a dungeon facet: F-32's chest depth tiers, the mule's haul contracts, loop-gated floors above a
    character's cap.
  - **Takes:**
    - strip or remap the 40,467 0xC000 statics (a script);
    - decorate the bare dungeons (they are undecorated);
    - regions per dungeon (DungeonRegion), spawners, teleporters;
    - about 7 MB in the package after the rewrite.
- **Sosaria Before (sos-trammel-map):**
  - **Use:** loop-gated content ("the world a loop ago"); 20+ ready dungeons for League expeditions; a second town
    network.
  - **Takes:**
    - fix or remove 23 tile IDs (66 placements);
    - convert regions, locations and decoration (about 2 days);
    - spawners and moongates by hand;
    - 117 MB in the package, which argues for a separate optional download (B.5);
    - a design pass, since it duplicates Trammel's geography and names.
- **The Unwritten Reach (paranoia-custom-map):**
  - **Use:** guild or League expedition frontier, player towns, housing.
  - **Takes:**
    - 2 land cells fixed;
    - everything else built (one starter city exists);
    - 173 MB, the largest, which also argues for a separate download;
    - the least defined terms (none stated).

### B.4 Recommended first facet and the smallest end-to-end test (steps only, not done here)

**First: The Proving Ward (termur-replacement):** small, no missing art, terms permissive.
1. **Make the files:** copy `TP\termur-replacement` `map5.mul`, `staidx5.mul` and `statics5.mul` into a scratch
   folder as `map6.mul`, `staidx6.mul`, `statics6.mul`, rewriting the statics to drop the 2.3 MB unreferenced (a short
   script). Never into EA's folder.
2. **Server:** a copy of the test client-data folder (`CLIENT_DATA_PATH_TEST`, the 7.0.117.0 copy) with the three
   files added. In the test shard's data, one map entry: index 32, id 6, fileIndex 6, name "ProvingWard", 1280x4096,
   season 0, rules TrammelRules.
3. **Test shard:** build with `docker/uo/build.sh -t sl-modernuo:cc-pNN` and run the test shard only. In the log, the
   map loads with no "was not found" warnings.
4. **Client:** in a test TazUO only, either:
   - add `map6.mul`, `staidx6.mul` and `statics6.mul` to its files-override list and pass `-maps_layouts` with seven
     sizes (`7168,4096;7168,4096;2304,1600;2560,2048;1448,1448;1280,4096;1280,4096`); or
   - put the files in a copy of its UO folder.
5. **One teleporter in and out:** staff `[add Teleporter` in New Haven with `MapDest` the new map and a point on it;
   another back.
6. **Walk it:**
   - the land and statics draw;
   - the world map lists a seventh facet and draws it;
   - logging out and in on the facet works;
   - `[where` reads the map name;
   - an unpatched client sent to it lands on Felucca's coordinates (A.2) and does not crash.
7. **Then decide** the package route (B.5) before any player sees it.

### B.5 Risks

- **Client on an unknown index:** TazUO falls back to Felucca rather than crashing (A.2). A player without the new
  files sees the wrong map at that spot, which is confusing, not fatal. **The EA client is not supported for extra
  ids** (the server comment's 0-5), so these facets are TazUO-only, which is the shard's client anyway.
- **File size:** 80 MB today, downloaded whole on every update. The two big maps would roughly double or triple it
  (117 MB and 173 MB after trimming, before compression; compression unverified).
  - **Proposal:** small facets go in the package; big ones ship as a separate, versioned, optional "facet pack" the
    launcher fetches once (not designed yet).
- **Art IDs:** SoS (23 tiles), Paranoia (1 land tile) and dungeon-map-4 (the 0xC000 filler) need fixing before use;
  termur needs none. Missing art draws as OSI's "UNUSED" placeholder, not a crash.
- **Wipe timing:**
  - Adding a facet before the fresh world is cheapest: no item on a renumbered index, nothing to migrate.
  - After the wipe, adding is still safe if the index and file numbers never change.
  - **Removing** a facet later deletes whatever is on it.
- **Licenses:**
  - none of the four has a license file;
  - SoS's author invites reuse;
  - TheArt's two are "as is";
  - Paranoia states nothing;
  - all ask for credit;
  - the client policy reading in A.3 needs Chase's confirmation.
  Credit lines belong in the package's SOURCE files, as for the art.
- **Engine assumptions:** moongates, `[go` and per-map travel zones know only the six maps (A.1). Small engine patches
  or shard code are needed per facet that wants them.
- **Unverified end to end:** that a server id of 6 or more plus TazUO's `maps_layouts` work together in play. Step B.4
  proves it.

### B.6 Decisions for Chase

1. **Confirm the policy reading:** may we ship whole community-made map files (no EA bytes) as our own data?
2. **First facet:** The Proving Ward (termur-replacement), recommended. Or another.
3. **Names:** the four above are placeholders.
4. **Big maps:** a separate optional facet pack, or in the main package?
5. **Tools:** fetch UOFiddler and CentrED+ (and RadCopy for SoS) when wiring starts.
6. **Siege of Sosaria's role:** loop-gated content, an expedition world, or skip it (it is a second Trammel).
7. **Timing:** add before the world wipe (cheapest), or after the stock-map buildings that come first (2026-09-30)?
8. **CALYPSO:** still to download (5 a day on servuo.dev); revisit when it lands.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, run 2026-10-12 before DONE:

```
Repo Result
---- ------
code clean
docs dry run
```

Docs pending: `notes/cc-P76-extra-facets.md` only. The code repo is clean: this task wrote no code.

P76 DONE
