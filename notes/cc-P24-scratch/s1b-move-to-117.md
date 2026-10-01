# P24 s1b: moving the server's client data from 7.0.114.40 to 7.0.117.0

Read-only research, 2026-10-01. Nothing outside `notes\cc-P24-scratch\` was changed. Scripts, CSVs and
renders are in `notes\cc-P24-scratch\s1b\` (all Python 3.12, numpy, Pillow; re-runnable).

**Inputs read**

| What | Where | Identity |
|---|---|---|
| Server data today ("114") | `D:\ShatteredLegacy\client-data\classic-client` | `client.exe` FileVersion 7.0.114.40 |
| EA current ("117") | `D:\UO\UltimaOnlineVanilla` | `client.exe` FileVersion 7.0.117.0 |
| Engine | `D:\UO\ModernUO-pinned` | HEAD `7c9215d97` |
| Our scripts | `D:\ShatteredLegacy\server\customizations` | repo HEAD `f49e693`, `git status --short` empty when read |
| Test save | `D:\ShatteredLegacy\server\lib\uo\modernuo\Saves-test` | written 07:00 and 07:05 today while I read it (see 2) |
| Live save | `D:\ShatteredLegacy\server\lib\uo\modernuo\Saves` | files dated 2026-09-29 13:50 |

**P22 (pit thief) is not in the tree.** The working tree is clean and nothing in `customizations` mentions a
pit thief; `notes\passdown-overseer-2026-10-01.md:27` has P22 "queued on disk", to run after P23. I used the
spot its brief specifies, `D:\UO\cc-prompts\cc-P22-small-features-1.md:105`: Trammel **3440,2558** (z55 stool),
and guildmaster 3495,2515.

---

## 1. Statics recount, and every literal coordinate we place at

### 1.1 Statics blocks (staidx/statics, 8x8 blocks, compared as sorted record lists)

`diff_statics.py`. Facet sizes from pinned `Distribution/Data/map-definitions.json`; the server reads
`staidx{n}.mul`/`statics{n}.mul` with n = fileIndex (`Projects/Server/TileMatrix/TileMatrix.cs:121-142`).

| Facet | Blocks | Statics blocks differing | Re-order only | Bounding box of the changed tiles |
|---|---|---|---|---|
| 0 Felucca | 458,752 | **338** | 0 | x 736-6847, y 2120-3327 |
| 1 Trammel | 458,752 | **1,149** | 0 | x 736-6951, y 2120-3623 |
| 2 Ilshenar | 57,600 | 0 | 0 | - |
| 3 Malas | 81,920 | 0 | 0 | - |
| 4 Tokuno | 32,761 | 0 | 0 | - |
| 5 TerMur | 81,920 | 0 | 0 | - |

**338 and 1,149 confirmed.** The location description in `notes\player-package.md` Part C is not quite right:
the changes sit in exactly **two places per facet** (`clusters.py`, `land_clusters.py`), and the "Skara Brae"
box it gives (x 736-1023, y 2120-2559) is much bigger than the data, which only reaches x 791, y 2167:

| Area | Felucca statics blocks | Trammel statics blocks | What changed (117 vs 114) |
|---|---|---|---|
| **A. North of Skara Brae**, x 736-791, y 2120-2167 | 26 | 18 | The **Archers' Guild** (sign 0xBF0 is added here) gets a new wing east of the existing building: +769/-189 statics on Fel, +743/-152 on Tram. Added: wooden shingles 0x5C2-0x5D0 (~500), wooden walls 0x6-0xD/0x18 (~180, all Impassable), windows 0xE, roof pieces 0xAEE-0xAFA, banners, signpost 0xB98. Removed: trees, grasses, rocks, logs, and 5 walls 0x8 (the old east wall, opened into the wing). No door statics added (doors are items) |
| **B. East edge**, x 6448-6959, y 3040-3623 | 312 (12 groups of 26) | 1,131 | Felucca 114 was an empty void there; 117 adds a stone plateau with 12 octagonal stone-walled rings (0xC7-0xCC, 408 statics each). Trammel 114 had a 12-island compound with buildings plus a walled path complex (**22,979 statics removed**); 117 replaces it with the same 12 rings as Felucca (+1,630 in the big cluster). Nothing in pinned regions, teleporters, spawns or decoration touches this box (scan in 1.3) |

Renders (left 114, right 117; colours from each version's `radarcol.mul`; magenta = statics-changed block,
yellow = land-only block; `render.py`): `s1b\skara_fel.png`, `s1b\skara_tram.png`, `s1b\skara_fel_zoom.png`,
`s1b\east_fel.png`, `s1b\east_tram.png`.

### 1.2 Literal coordinates in our seeders and decorators

`scan_coords.py` reads every `.cs` under `server\customizations` and takes **every pair of adjacent decimal
literals** `a, b` with 16 <= a < 7168 and 16 <= b < 4096 (plus `x: a, y: b`, `X = a, Y = b`, and every
`Rectangle2D`, tested over its whole area). That deliberately over-collects (gump sizes, stat tables): **2,855
candidate pairs in 167 files**, all in `s1b\coords_all.csv` with file, line, kind, x, y and the line text. Each
is tested against the changed set for **both** Felucca and Trammel = statics blocks union land blocks (1.1 and 3).

**Result: 0 of 2,855 candidates fall in a changed block on either facet.** Ter Mur, Ilshenar, Malas and
Tokuno did not change at all, so their coordinates cannot be hit.

The placement files the brief names, one row per file (all rows per line in `s1b\coords_placements.csv`, 782
rows; `placements.py`). "Nearest" = Chebyshev distance in tiles to the nearest changed block on Fel or Tram.

| Source file (lines with coordinates) | Map | Pairs | x range | y range | In changed block? Nearest |
|---|---|---|---|---|---|
| `ClusterFNewHavenSeeder.cs:23-71` | Trammel | 59 | 3418-3555 | 2414-2749 | no, 2627 |
| `ClusterFNewHavenServicesSeeder.cs:60-189` (P17's DecorEntry list) | Trammel | 126 | 3434-3559 | 2452-2607 | no, 2643 |
| `ClusterFInstitutionSeeder.cs:48-102` | Trammel, 1 Ter Mur (`:104`) | 8 | 797-3524 | 2560-3431 | no (Trammel part 2700+) |
| `ClusterFMineCampLayout.cs:18-76` (P16; seeder `ClusterFMineCampSeeder.cs:156` places at it, Trammel) | Trammel (`Layout:14`) | 47 | 3492-3516 | 2742-2756 | no, 2701 |
| `ClusterFRegistrarOfficeLayout.cs:20-67` (P19; seeder has no literals) | Trammel (`Layout:15`) | 36 | 3454-3463 | 2595-2602 | no, 2663 |
| `ClusterFRoyalCitySeeder.cs:41-98` | Ter Mur | 46 | 702-851 | 3387-3525 | no (Ter Mur unchanged) |
| `ClusterFGuildStarterPath.cs:206-223` `GuildLocations` (used by `ClusterFGuildHallSeeder.cs:66,142`) | Trammel, 1 Ter Mur (`:223`) | 22 | 3410-3559 (+797) | 2463-2744 (+3431) | no, 2600+ |
| `ClusterFOldHavenSeeder.cs:31-78` | Trammel | 6 | 3556-3645 | 2457-2540 | no, 2765 |
| `ClusterFOldHavenCleanup.cs:27-79` | Trammel | 47 | 3585-3752 | 2476-2709 | no, 2696 |
| `ClusterFSouthMineDecor.cs:49-50` | Trammel | 2 | 3508-3510 | 2746 | no, 2717 |
| `ClusterFResetStone.cs:30` | Trammel | 1 | 3501 | 2575 | no, 2710 |
| `ClusterFAreaScan.cs:23-25` (scan box, not a placement) | Trammel | 6 | 3400-3760 | 2400-2760 | no, 2609 |
| `CharacterCreation.cs:83-360` (start locations) | Trammel | 8 | 368-5445 | 20-2625 | no, 1297 |
| `Engines\ML Quests\Items\NewHavenQuestBoard.cs:69` | Trammel | 1 | 3502 | 2573 | no, 2711 |
| Despise: `DespiseRevamped\Setup.cs:74-143`, `DespiseSpawns.cs:97-143`, `DespiseController.cs:181-696`, `Region.cs:37` | Trammel | 126 | 516-5605 | 24-1965 | no, 2066+ |
| Shame: `Shame Revamped\Generate.cs:38-134`, `ShameSpawns.cs:65-258`, `ShameWall.cs:156-168` | Fel and Tram | 241 | 5387-5820 | 17-235 | no, 2805+ |
| P22 pit thief (brief only, not in tree) | Trammel | 2 | 3440, 3495 | 2558, 2515 | no, ~2600 |
| Fountain of Fortune (`notes\s2-fountain.md:60,194`: ServUO's spot, nothing here places it) | Ter Mur | 1 | 1121 | 957 | no (Ter Mur unchanged) |

Everything we place on Trammel is in and around New Haven (x 3400-3760, y 2400-2760), about 2,600 tiles from
the nearest change. **No coordinate hit, so there is no per-hit before/after picture to make**; the renders
above show the two changed areas instead.

### 1.3 Stock content in the changed areas (not ours, but it is in both worlds)

Pinned `Distribution/Data` scanned for coordinates inside or within 8 tiles of areas A and B:

- **Decoration:** `Decoration/Britannia/skara.cfg` (applied to both Fel and Tram) has **40 placements** in
  changed blocks around the old Archers' Guild (doors, chairs, bookcases, butte). For 38 of them the tile itself
  is identical in 114 and 117. Two `Static 0x1036` at (754,2159) and (755,2159) (`skara.cfg:1849,1892`) see
  only a land change, dirt z1 -> grass z0, no new static. Nothing stock ends up inside a new wall.
- **Locations:** `Locations/felucca.json:344`, `trammel.json:315` "Skara Brae North" (746,2165,0): tile unchanged.
- **Regions:** the guarded Skara Brae TownRegion is x 538-688 (`regions.json:555`, `:2204`), so **area A is
  outside town and housing could be placed there**. Nothing in regions.json overlaps area B.
- **Spawns and teleporters:** no spawn `location` and no teleporter endpoint inside either area.

---

## 2. Houses and spawners in the changed blocks (test and live saves, read only)

The test stack mounts its save at `${SERVER_PATH}/lib/uo/modernuo/Saves-test` (`docker\uo\docker-compose.test.yml:40`).
**Parsing the binary save was cheap enough to do.** `saves_scan.py` reads `Items.idx` (v3 entries: flag byte,
type hash u64, serial u32, created i64, position i64, length i32; pinned
`Serialization/GenericEntityPersistence.cs:100-122`, `:273-320`), maps hashes through `SerializedTypes.db`
(`Serialization/Persistence.cs:54-80`) and decodes only the base `Item` header (version, SaveFlag, last-moved,
optional direction/loot type, location, item ID, hue, amount, layer, name, items, weight, map;
`Items/Item.cs:816-1060`, flags `:4280-4310`). Sanity check: every decoded top-level item has map 0-5.

**The test shard was running while I read** (`docker ps`: `sl-modernuo-test Up 14 hours`; I did not start or touch
it). It saved at 07:00 and 07:05; the two reads saw 204,147 and 204,118 items. Both parsed cleanly.

| | Test (`Saves-test`) | Live (`Saves`, 2026-09-29 13:50) |
|---|---|---|
| Items / top-level on a map | 204,147 / 97,489 | 192,177 / 92,831 |
| Types in `Server.Multis` (all `BaseHouse` subclasses live there; checked by grep of pinned UOContent and our tree) | 11 camps + 2 addon/artifact name matches, **0 player houses** | 10 camps + `LockableBarrel`, **0 player houses** |
| Spawners (`Spawner`, `RegionSpawner`, `DespiseSpawner`, `GauntletSpawner`) | 5,386 | 5,336 |
| Top-level items within 32 tiles of area A / area B | 281 / **0** | 251 / **0** |
| ...of which inside a changed block on their own map | 49 Fel + 49 Tram | 50 Fel + 43 Tram |
| ...whose own tile changes (statics or land) | 4 Fel + 6 Tram | 5 Fel + 1 Tram |
| Spawners inside a changed block | **0** | **0** |

The only spawners near area A are a `Spawner` at (813,2164) and a `RegionSpawner` at (813,2163) on each facet,
22 tiles east of the nearest changed block. The items whose tile changes are **reagents** (Sulfurous Ash, Black
Pearl, Mandrake Root, Bloodmoss, Ginseng, Spiders' Silk) lying where the new wing now has floor, wall or roof,
plus the two stock `Static 0x1036` from 1.3. Serials and before/after tiles: `saves_tiles.py Saves-test` and
`saves_tiles.py Saves`. They are spawned resources that get picked or respawned; nothing to fix.

**Not covered:** mobiles were not parsed (a logged-out character standing in area A would not show), and the
32-tile pad around each area is a heuristic for multi footprints (moot with zero houses). If the build task wants
a second opinion in game: `[where` at (770,2145) on both facets and a staff `[area`/`[props` sweep of x 720-800,
y 2110-2175, or ModernUO's `[ClusterFAreaScan`-style scan if extended to those bounds.

---

## 3. Land, cell by cell, every facet's map UOP

`diff_land.py`. UOP read as in pinned `Projects/Server/Client/UOPFiles.cs:24-100` (`MYP\0`, version, signature,
table blocks of offset/headerLength/compressedLength/decompressedLength/hash/adler/flag) with entries named
`build/map{n}legacymul/{i:08}.dat` and hashed with `HashLittle2` (ported, `UOPFiles.cs:121-`). Server use:
`TileMatrix.cs:102-113`. Each block is 196 bytes: 4-byte header plus 64 cells of (ushort id, sbyte z). All map
entries are uncompressed (flag 0) in both versions.

| Facet | UOP ver | Entries | Chunks whose payload differs | Land cells differing (id / z / either) | Blocks | Where |
|---|---|---|---|---|---|---|
| 0 Felucca | 5 / 5 | 113 / 113 | 10 | 133,170 / 139,561 / **140,114** | **2,300** | 19 blocks in area A (727 cells: forest -> wooden floor, z 0 to -21), 2,281 in area B (139,387 cells: void -> stone plateau, z -20 to +42) |
| 1 Trammel | 5 / 5 | 113 / 113 | 11 | 189,288 / 141,407 / **192,841** | **3,285** | 13 blocks in area A (541 cells), 3,272 in area B (192,300 cells, z -71 to +20) |
| 2 Ilshenar | 5 / 5 | 15 / 15 | 0 | 0 | 0 | packaging only |
| 3 Malas | 5 / 5 | 21 / 21 | 0 | 0 | 0 | packaging only |
| 4 Tokuno | 5 / 5 | 8 / 8 | 0 | 0 | 0 | packaging only |
| 5 TerMur | 5 / 5 | 21 / 21 | 0 | 0 | 0 | packaging only |

Block headers are equal everywhere. For facets 2-5 every chunk payload is byte-identical; the files differ only in
container bytes (file header or table). **Land changes are confined to the same two areas as the statics**, never
elsewhere. Union of changed blocks (statics or land): **Felucca 2,310** (29 in A, 2,281 in B), **Trammel 3,295**
(19 in A, 3,276 in B). Q-063's "1,487 changed blocks" counted statics only.

Not read by the server and not compared: the `x` variants (`map0x`, `map1x`, `staidx1x` ...). The `mapdif`/`stadif`
patches are disabled for clients >= 7.0.9.0 (`TileMatrixPatch.cs:57-72`) and are byte-identical anyway.

---

## 4. tiledata.mul, hues.mul, radarcol.mul, multis

`diff_tables.py` (full output `s1b\tables.txt`), `multi_cmp.py`. Tiledata layout per pinned
`Projects/Server/TileData.cs:303-375`: 3,188,736 bytes means 64-bit flags and 0x10000 items (`:313-318`); land
groups of 32 x (flags u64, texture u16, name 20), item groups of 32 x (flags u64, weight, quality, animation u16,
byte, quantity, int, byte, value, height, name 20), 4-byte header per group. Flags enum `:215-283`. Both files are
3,188,736 bytes.

- **Land tiles: no change** (0 of 16,384).
- **New item tiles: 345**, all empty in 114: 0x6400-0x64FE (Halloween/pumpkin and holiday items) and 0xB4D2-0xB52B
  (fireworks, gems, singed scrolls, trophies, statues). New art only; nothing on the maps or in either save uses them.
- **Changed existing item tiles: 21.** 3 change only the int the server skips (`TileData.cs:361`): 0x9985,
  0x9986 (epaulets), 0xAEAC (close helmet). **18 change flags:**

| Tiles | Name | Flag change |
|---|---|---|
| 0xA90E-0xA90F | Farm_Stand | -Foliage |
| 0xB272-0xB277 | Moon Flower Closed 1-6 | **-Impassable** |
| 0xB3D2-0xB3D5 | Unity Tapestry S/E | **-Impassable** |
| 0xB406-0xB409 | Whimsy Tapestry S/E | **-Impassable** |
| 0xB41B-0xB41C | Firework Crate S | +Container |

  Usage of those 18 IDs: **0** statics in any facet's statics file (both versions), **0** items in either save
  (`saves_itemids.py`, ItemID decoded for all but one item per save), **0** references in pinned `Projects` or our
  customizations. So no collision changes anywhere today.
- **hues.mul:** 3,000 hues both. 17 differ, all previously unnamed slots that gain names: hues 2753, 2758, 2759
  (name only, colours equal) and 2786-2799 (new colours and names, e.g. "Shattered Midnight", "Void Abyss").
  Group headers equal. The server does not read hues.mul (no `FindDataFile` for it in pinned).
- **radarcol.mul:** 81,884 entries, 36 differ, all items in the new 0x640F-0x64FE range. Server does not read it.
- **multi.mul / multi.idx:** identical (and unused while `MultiCollection.uop` exists, `MultiData.cs:31-38`).
- **MultiCollection.uop** (`MultiData.cs:55-130`): 871 -> 872 multis. **One new multi, 0x212B** (1,654
  components, x -34..16, y -26..24). For all 871 existing multis the **component lists are identical**; 304 differ
  only in the per-component cliloc arrays the server skips (`MultiData.cs:117-119`). `housing.bin` entry: same
  size, different checksum (not compared further).
- **artLegacyMUL.uop** also differs (hash only, not parsed). The server only uses art via `ItemBounds.bin`, which
  ships prebuilt in pinned `Distribution/Data/Items/` and is not regenerated from our client data while it
  exists (`Items/ItemBounds.cs:42-60`).

**For the server, the swap changes:** collision in areas A and B on Felucca and Trammel, the tile flags above
(no current users), one new multi definition, and the detected client version.

---

## 5. What moves together, checked against the current tree

| # | Thing | Today | What the build task changes |
|---|---|---|---|
| 1 | Data folder, live | `docker\uo\docker-compose.yml:27` mounts `${CLIENT_DATA_PATH}` from `docker\uo\.env` = `D:/ShatteredLegacy/client-data/classic-client` (`.env` is gitignored, `.gitignore:5`) | at the live step only: point `CLIENT_DATA_PATH` at the new folder |
| 2 | Data folder, test | `docker-compose.test.yml:41` mounts the **same** `${CLIENT_DATA_PATH}` | change `:41` to `${CLIENT_DATA_PATH_TEST:-${CLIENT_DATA_PATH}}`, add `CLIENT_DATA_PATH_TEST` to `.env` and `.env.example:5`. Test can then move first; the default keeps today's behaviour |
| 3 | The new folder | does not exist | **a copy**, e.g. `D:\ShatteredLegacy\client-data\classic-client-7.0.117.0`. Do not mount `D:\UO\UltimaOnlineVanilla`: EA's launcher patches it in place (its map UOPs are dated 2026-09-06, newer than the rest), so a mounted install would change under a running server or be locked against the patcher. `client-data/` is gitignored (`.gitignore:34`) |
| 4 | Server's detected version | `UOClient.Load` (pinned `Server/Client/UOClient.cs:36-44`): no `clientData.clientVersion`, no `settings.json` in either folder, so it reads `client.exe` (`:92-`) | moves to 7.0.117.0 by itself |
| 5 | Kick floor | `ClientVerification.Initialize` sets MinRequired = detected version when neither min nor max is set (`UOContent/Misc/ClientVerification.cs:52-55`); `minRequired` is read with `GetSetting`, never written (`:34`); value parsed with `new ClientVersion(string)` (`Server/Configuration/ServerConfiguration.cs:43-44`). Staff are exempt (`:120`) | **decision for Chase:** add `"clientVerification.minRequired": "7.0.114.40"` to the `settings` of both `server\uo\modernuo\Configuration\modernuo.json` and `Configuration-test\modernuo.json` (both have the clientVerification keys at lines 37-41, identical) to keep today's floor; or leave it out and the floor becomes 7.0.117.0 |
| 6 | Package floor | `player-package\payload\app\Setup.ps1:30` `$minVersion = [version]'7.0.114.40'`, also inside the zip family already holds | nothing if (5) pins 7.0.114.40. If the floor goes to 7.0.117.0, change `:30`, rebuild and redistribute, or 7.0.114.40-7.0.116.x players pass setup and get kicked 20 s after login |

The configs the containers use are `server\uo\modernuo\Configuration` and `Configuration-test` (compose `docker-compose.yml:18` and `docker-compose.test.yml:39`),
not anything under `customizations`.

---

## 6. Plan for the build task

Small change, because nothing of ours is in the changed blocks and neither world has a player house there.

**Prepare (no restart)**
1. Copy `D:\UO\UltimaOnlineVanilla` to `D:\ShatteredLegacy\client-data\classic-client-7.0.117.0` (robocopy, about
   2.5 GB). Verify the copy: `client.exe` FileVersion 7.0.117.0, and SHA-256 equal to the source for `tiledata.mul`,
   `MultiCollection.uop`, `artLegacyMUL.uop`, `map0-5LegacyMUL.uop`, `staidx0-5.mul`, `statics0-5.mul`. Leave the old
   folder untouched; it is the rollback.
2. Re-run `s1b\diff_statics.py` and `diff_land.py` with `NEW` pointed at the copy: expect 338 / 1,149 statics and
   2,300 / 3,285 land blocks, 0 elsewhere. If EA has patched in between, the numbers change and 1.2 must be re-run.
3. Edit `docker-compose.test.yml:41` and `.env.example:5` as in 5.2, add `CLIENT_DATA_PATH_TEST` to `.env`.
4. Chase decides 5.5. Recommended: pin `minRequired` 7.0.114.40 in both configs for a grace window, so the
   package already handed out keeps working; raise floor and `Setup.ps1:30` together later.

**Test shard first** (it is running now; the mount change needs the container recreated, so this is a test restart)
5. Bring the test shard down and up with the usual scripts (`docker\uo\Start-TestShard.ps1`). No image rebuild is
   needed for a mount and config change.
6. Log checks: `Automatically detected client version 7.0.117.0`; `Restricting client version to 7.0.114.40 or
   newer` (or 7.0.117.0 if not pinned); no `... was not found` warnings from `TileMatrix`; no `MultiData` errors.
7. In game with a **player** account (staff are exempt from the version check), on both Felucca and Trammel:
   - walk around the Archers' Guild wing north of Skara Brae, (760-790, 2128-2160): walls block, the opened east
     wall of the old building passes, roof does not block the floor, nothing floats;
   - check the stock doors and furniture of the old guild building still sit where they did;
   - optionally `[go 6700 3300` on both facets to see area B is the 12 stone rings, unreachable for players.
8. Run one seeder dry run (for example `[ClusterFSeedRegistrarOffice dryrun`) to confirm it reports nothing to
   move: expected, since no placement is in a changed block.
9. Log in with a 7.0.117.0 client (TazUO via the package) and, if pinned, with a 7.0.114.40 data set: both stay
   past 20 s.

**Live, at a restart Chase already plans**
10. Set `CLIENT_DATA_PATH` in `.env` to the new folder, apply the same `minRequired` decision to the live
    `Configuration\modernuo.json`, restart live, repeat the log checks of step 6.
11. Rollback is one line: put `CLIENT_DATA_PATH` back and restart. No save migration either way: houses and
    items carry coordinates, not tile data.
12. Afterwards, if the floor moves to 7.0.117.0: edit `Setup.ps1:30`, rebuild and redistribute the package.

---

## Could not verify / caveats

- In-game behaviour of the new wing (doorways, roof z) is from tile data only; not walked.
- What area B is for (an EA event or staging area?) is a guess; it is unreachable as far as pinned data shows.
- Mobiles in the saves were not parsed; house detection relies on all `BaseHouse` types being in `Server.Multis`
  (true for pinned UOContent; our tree has none).
- The test save changed while being read (shard running). Live's on-disk save is dated 2026-09-29 13:50
  although `sl-modernuo` shows `Up 41 hours`; I did not look into why.
- `artLegacyMUL.uop` and the `housing.bin` payload were hash-compared only.
- The coordinate scan cannot see coordinates computed at runtime or read from data files outside
  `customizations` (none exist there: no .json/.csv/.xml in the tree). Despise/Shame placement code may also
  compute offsets from these literals; all of its literals are 2,000+ tiles from any change.
