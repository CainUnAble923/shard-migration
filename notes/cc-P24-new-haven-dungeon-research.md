# cc-P24: New Haven dungeon, read-only research

2026-10-01. Brief: `D:\UO\cc-prompts\cc-P24-new-haven-dungeon-research.md`.
**Read only.** Nothing changed except this file and `notes\cc-P24-scratch\`: seven section drafts, scripts and
renders. No build was run, no world was touched, and nothing was committed. Every behavioural claim below comes
from reading source unless it says "measured" or "parsed".

**Numbering:** P24 has no collision. `cc-prompts` and `cc-prompts\completed` hold P20 to P23 and this brief only,
and nothing in `notes\` or `docs\` uses P24.

**Versions read:**

- Pinned ModernUO `7c9215d97`.
- ServUO pub57.
- Shard `D:\ShatteredLegacy` at `f49e693`. Two drafts saw different working trees, because P23 work appeared
  while this ran:
  - s1b saw the tree clean.
  - s2 saw `server/customizations/SmithGuildSalvageBag.cs` modified and
    `server/tests/Items/SalvageBagIngotReturnVerification.cs` new. That is P23's D42 work, uncommitted.
  - s3a cites `SmithGuildSalvageBag.cs` line numbers from that working-tree copy.
  - Nothing else cited was touched.
- P22, the pit thief, is not in the tree. Its spot was taken from its brief (`cc-P22-small-features-1.md:105`,
  Trammel 3440,2558).
- TazUO source: tag `v26.0909.63`, commit `3212623f`. This matches the shipped client's `v.txt`. It was cloned to
  the session scratchpad, not to the repo.
- CentrED#: commit `50d23f7a`.
- Client data: 7.0.114.40 at `D:\ShatteredLegacy\client-data\classic-client` and 7.0.117.0 at
  `D:\UO\UltimaOnlineVanilla`.

**Detail lives in the drafts.** Each section below is the short form. The draft holds the full tables, file lists
and render paths:

| Section | Draft |
|---|---|
| 1 | `cc-P24-scratch\s1-map-shipping.md` |
| 1b | `cc-P24-scratch\s1b-move-to-117.md`, plus `s1b\` (scripts, CSVs, PNGs) |
| 2 | `cc-P24-scratch\s2-location.md`, plus `s2\` (16 PNGs, scripts) |
| 3.1-3.3 | `cc-P24-scratch\s3a-harvest-dawnstone.md` |
| 3.4-3.7 | `cc-P24-scratch\s3b-leather-wood-cloth.md` |
| 4 | `cc-P24-scratch\s4-ports.md` |
| 5 | `cc-P24-scratch\s5-gear-quest.md` |

---

## 0. One page

**Pointing TazUO at the shipped map: use TazUO's existing per-file override. It needs no client code change.**

- TazUO resolves every data file through `UOFileManager.GetUOFilePath`, and that consults a `filename=fullpath`
  override list first (TazUO `ClassicUO.Assets/UOFileManager.cs:103-109`, `ClassicUO.IO/UOFilesOverrideMap.cs:16-55`).
- The list is passed only on the command line, as `-uofilesoverride <file>` (`ClassicUO.Client/Main.cs:310-313`).
- On an EA install, Trammel is exactly three files: `map1LegacyMUL.uop`, `statics1.mul` and `staidx1.mul`
  (`MapLoader.cs:139-213`).
- `Play.ps1` writes the list at each launch and passes the argument. It must first check the three files exist,
  because a missing `map1` makes TazUO draw Felucca as Trammel without any error (`MapLoader.cs:229-235`). That is
  about 30 lines.
- Ship the files in `maps\` at the install root, not under `app\`. `Update.ps1:236` backs up all of `app\` on every
  update.
- **Cost:** the zip grows from about 76 MB to about 104 MB. The Trammel set is 115.9 MB raw, about 24 MB deflated
  (estimated with zlib, not the build). Every update is a full download (`Play.ps1:154-156`). The build changes are
  about 60-80 lines: map hash checks in gate 4, plus a new gate 6 for server parity.
- **Server side:** keep one data folder that is both the server's data and the package's source.
  - Pinned prefers `map1.mul` over the UOP (`Server/TileMatrix/TileMatrix.cs:94-113`), the reverse of TazUO. So
    gate 6 must also fail if any `map1.mul` exists in the server's data folder.

**Recommended location:**

- **Interior: candidate A**, Trammel x 5136-5247, y 1128-1263 (112 x 136).
  - It is in the classic dungeon strip, 24 tiles west of the GM Jail.
  - It is void land with zero statics in both 114 and 117, and lies in no pinned region and no ServUO Trammel
    region.
  - It is inside the shard's fog-of-war grid. That grid stops at x 6144 (`ClusterFExplorationManager.cs:31-38, 73`),
    which counts against the bigger east candidates.
- **Entrance: B1**, the ruined "Second Bank of Haven" in **Old Haven**, with the hole at 3619,2620.
  - New Haven's own town region (3416-3545 x 2480-2648, `regions.json:1516-1526`) has **no abandoned buildings**.
    Every ruin on the island is in Old Haven.
  - B1 is clear of P16, P17, P19, P22 and every quest NPC.
  - It sits inside the range of the pinned post-UOML skeleton and zombie spawners, which suits the story but is
    worth knowing.

**What the move to 7.0.117.0 touches: very little of ours.**

- Statics recount: 338 Felucca blocks and 1,149 Trammel blocks, as the brief said. 0 on the other four facets.
- Land, compared cell by cell for the first time: 2,300 Felucca blocks and 3,285 Trammel blocks. Again 0 elsewhere.
- All changes sit in two places per facet: a new Archers' Guild wing north of Skara Brae (x 736-791, y 2120-2167),
  and a remodelled east-edge void at x 6448-6959, y 3040-3623.
- **0 of 2,855 literal coordinate pairs in our customizations fall in a changed block.**
- The test world and the retired live world both have **0 player houses** and 0 spawners in changed blocks.
- tiledata: 18 existing tiles change flags, but none of them is used by any map, save or code.
- What moves together: the test compose needs its own data variable; the kick floor needs
  `clientVerification.minRequired`, which is Chase's call; and `Setup.ps1:30`.

**Size of the four resources, all additive, with no new upstream patch unless noted:**

| Resource | Files | Lines | Notes |
|---|---|---|---|
| Dawnstone | 4-5 | ~125-165 | Includes the shared region-harvest file |
| Burrowhide | 6-8 | ~150-250 | |
| Rootwood | 7-9 | ~150-250 | A bow bonus needs 1 pinned patch; without it Rootwood is cosmetic |
| Gloomsilk | 1 | ~60-100 | Only as a cosmetic `Cloth` subclass. A real cloth tier is a subsystem (400-700 lines, 3-5 patches) |

- Region-only harvest is one additive override of pinned's unused virtual `MutateResource`
  (`HarvestSystem.cs:140, 332`). It is about 80-120 lines and is shared by ore and wood.

**Parts and upgrade system: about 600-900 lines.** This is my estimate, not measured.

- The set pieces are new types on our `BaseSet*` carriers with pinned's real no-trade flag,
  `Item.Nontransferable` (`Item.cs:522`), plus `BlessedFor`.
- The upgrade level is a `[SerializableField]` on new types, so no migration is needed.
- Upgrades go through either pinned's `CustomCraft` path or a consent gump modelled on our Imbue gump.
- The replacement quest is a custom `BaseReward` on ML Quests.
- MiniChampionSystem is a small, near port of about 610 lines, and the Burrow Mother can be its final boss.
- The PuzzleRoom and Tomb of Kings chambers have zero-port pinned equivalents.

**What blocks building:**

1. **Q-063's data swap has to land first, or together with the map.** A 117-based Trammel cannot run on the
   server's 114 tiledata.
2. **Chase's decisions**, collected in section 6.2:
   - the kick floor;
   - Young players in the dungeon (stock `DungeonRegion` lets monsters attack them);
   - crafter option (a), (b) or (c);
   - widening the wood range (finding F3);
   - Gloomsilk cosmetic or tiered;
   - the starter numbers;
   - travel rules;
   - how strict no-trade storage is.
3. **One latent crash** (F1) should be probed before any new ore copies the extended ores' pattern.

**Findings outside the brief:**

| # | What | Status |
|---|---|---|
| F1 | A GM miner with stone mining toggled on can hit `Types[1]` on our one-type extended ores (`ClusterFMiningExtension.cs:86-93` against pinned `Mining.cs:284-288`). That throws `IndexOutOfRange` inside the harvest timer | Latent crash candidate, not reproduced |
| F2 | Pinned `Mining.cs:28` has an inverted pair, `252, 236`, which matches nothing | Pinned bug, harmless |
| F3 | Our `ResourceInfo.cs:1095` wood range stops at Frostwood, so the 8 extended woods classify as `None` | Probably unhued and unnamed logs and boards; not seen in a client |
| F4 | `HuntersSatchel.cs:64-70` turns any unknown hide into plain Leather | Ours |
| F5 | A 0/0-durability weapon is `Delete()`d on the 1-in-25 wear roll (`BaseWeapon.cs:2080-2108`) | Pinned behaviour, matters for the set |

I re-read the cited lines for F1, F3 (the enum and range) and F5 myself.

**Brief figures that were wrong:**

- Our extended woods are **8**, not 6. Emberbark and Frostbark are missing from the brief's list
  (`ResourceInfo.cs:49-57`).
- The package is 76.0 MiB today (`ShatteredLegacy-2026.09.29.1331.zip`). 73 MB was the 09-26 zip.
- The changed areas are smaller and differently placed than `player-package.md` Part C says. See 1b.3.
- Q-063's "1,487 changed blocks" counted statics only.
- "New Haven abandoned buildings" are in Old Haven.

---

## 1. Shipping the edited map in the package

### 1.1 What TazUO reads for Trammel

TazUO tag `v26.0909.63`:

- `IsUOPInstallation` = version >= 7.0 and `MainMisc.uop` exists (`UOFileManager.cs:146`). This is true for every
  EA 7.x install.
- `map1LegacyMUL.uop` is used if present (`MapLoader.cs:141-143`). `map1.mul` and the dif files are read only in
  the non-UOP branch (`:161-187`).
- `statics1.mul` and `staidx1.mul` are always read (`:190-200`).
- The `x` files are opened but used only when the server sets `NewFeluccaAreas` (0x8000,
  `World.cs:226,234,275`). That flag is false in our `Configuration/expansion.json:53`.
- `facet01.mul` (the paper map) is found by directory listing and bypasses the override
  (`MultiMapLoader.cs:35-40`). So treasure and paper maps keep showing EA's Trammel. That is cosmetic; making it
  follow the override is about a 5-line TazUO change.
- `radarcol.mul` is per tile ID, not per map. The world-map cache is keyed by the hash of the map content
  (`Map.cs:532-552`), so it regenerates by itself.
- `D:\UO\ClassicUO\ClassicUO` is an old ClassicUO binary install, not source. It was not used.

### 1.2 How to point TazUO at package files

- **Recommended: `-uofilesoverride`**, cited in section 0.
  - Values are not trimmed, and a path containing `=` breaks the split rule (`UOFilesOverrideMap.cs:36-40`).
    `Play.ps1` should refuse such an install path.
  - Optionally also map `map1xlegacymul.uop`, `statics1x.mul` and `staidx1x.mul` to the same three files. Then
    turning on `NewFeluccaAreas` later cannot silently bring EA's Trammel back.
- **No other mechanism exists.** There is no settings.json key, no second data path and no custom map folder.
  `maps_layouts` changes dimensions only (`Settings.cs:98`, `MapLoader.cs:102-133`).
- **A merged folder is rejected.** The EA install is 2,743,994,359 bytes in 517 files (measured).
  - Copying it costs about 2.7 GB per player.
  - Hardlinks need the same volume and break when EA patches; whether they work under Program Files is unverified.
  - File symlinks need admin or Developer Mode.

### 1.3 What ships, and its effect on updates

| File | Raw bytes (measured) | Deflated (zlib 6 estimate) |
|---|---:|---:|
| map1LegacyMUL.uop | 89,965,543 | 17.1 MB |
| statics1.mul | 20,393,786 | 6.5 MB |
| staidx1.mul | 5,505,024 | 0.5 MB |
| **Trammel set** | **115,864,353** | **~24.2 MB** |
| tiledata.mul (optional, see 1.6) | 3,188,736 | 0.11 MB |

The zip grows from 79,688,947 bytes (76.0 MiB) to about 104 MB.

**Every update is a full zip download** (`Play.ps1:154-156`). On disk, `Update.ps1:195-202` replaces only files
whose length or SHA-256 differ, so an unchanged map is not rewritten. Any map change is a package release.

A separately versioned map download (its own `version.json` entry) would cost about 100-150 lines. Defer it until
script-only updates become frequent.

### 1.4 Updater and build gates

- **Never-overwrite list:** `Test-Kept` (`Update.ps1:100-111`) protects only `app\uo-path.txt`,
  `app\package-version.txt`, `app\tazuo\settings*.json` and `app\tazuo\Data\...`. Map files are not on it, so a
  changed map is already replaced. **No updater rule change is needed.**
- **Retired files:** `retired-files.txt` has 10 comment lines and no entries. `Test-RetiredLine` already accepts
  `maps\...` (`Update.ps1:114-122`, `Build-PlayerPackage.ps1:70-78`). List a map there only if one is ever dropped.
- **Build changes:**
  - `Build-PlayerPackage.ps1:20` states "Nothing of EA's goes in". That premise becomes false, as does
    `player-package.md:252`. Chase made the decision on 2026-10-01; it still needs writing into `docs/` and
    `README.txt`, licensing included.
  - Gate 3 (TazUO byte-identical) is unaffected while `maps\` sits outside `app\tazuo`.
  - Gate 4 (`Test-PackageZip`, `:83-147`) adds: `maps\` holds exactly the expected names and SHA-256 values, and
    `Play.ps1` passes `-uofilesoverride`.
  - The override list is generated at launch. It must never ship, because it holds absolute paths.

### 1.5 Server side, and a parity gate

- Pinned finds data with `Core.FindDataFile`: the first directory in `dataDirectories` that has the file wins
  (`Server/Main.cs:180-212`). `dataDirectories` is a HashSet, so its order is runtime behaviour, not a contract.
- `TileMatrix` reads `map{n}.mul` **before** the UOP (`TileMatrix.cs:94-113`; I re-read the lines). Statics difs
  are off for clients >= 7.0.9 (`TileMatrixPatch.cs:57-72`).
- **New map bytes take effect only at a server restart.** The streams are opened at startup (`TileMatrix.cs:96-137`).
- Today both stacks mount `${CLIENT_DATA_PATH}` (= `D:/ShatteredLegacy/client-data/classic-client`) read-only:
  live at `docker/uo/docker-compose.yml:27`, test at `docker-compose.test.yml:41`. Both `modernuo.json` files list
  only that folder.
- **Recommended:** one full 7.0.117.0 folder with our Trammel edits written into it. The server mounts it, and the
  package build copies the three map files from it.
  - The alternative is an overlay folder listed first. It depends on the HashSet ordering above, so it is rejected.
- **Gate 6, in `Build-PlayerPackage.ps1`, run before zipping:**
  - (a) Each shipped map file's SHA-256 equals the file of the same name in the server's data folder. The path
    comes from `docker\uo\.env` or a `-ServerData` parameter.
  - (b) No `map1.mul` exists in the server's data folder.
  - (c) `sl-modernuo` started after the maps' last write time. Only a warning if the container is down.
  - A stronger variant of (c): a ~40-line customization logs the map file hashes at startup into the bind-mounted
    `status` folder, and gate 6 and the console compare against that.
- **Editing:** edit a working copy, never the mounted folder (CentrED# opens files `FileShare.None`). Promote the
  copy at a restart.

### 1.6 Players whose EA install is newer than 117

- **Trammel is pinned by our files.**
- **tiledata.mul is the real residual risk.** If EA later changes an existing tile's flags or height, the client
  predicts movement differently from a server that is still on 117.
  - Shipping and overriding `tiledata.mul` costs about 0.11 MB. TazUO reads it through `GetUOFilePath`
    (`TileDataLoader.cs:25`).
  - **It is the one extra file worth shipping.** It is still EA's data, so it needs Chase's call under the same
    exception.
- **The other five facets** keep following the player's own install and drift as EA patches. Shipping all five
  later would cost about 38.7 MB deflated (measured per facet).
  - The cheap first step: `Play.ps1` logs a warning when the player's `client.exe` is newer than the server's.
- **art, hues, gumps, texmaps and `MultiCollection.uop`** are cosmetic on the client and never need shipping for
  map reasons.
- **Players older than 117** (`Setup.ps1` still allows 7.0.114.40) could lack a tile ID that only exists in 117.
  This is checkable at build time: reject any static ID in our edited blocks that 114's tiledata lacks.

### 1.7 Editor

- **CentrED# edits `map1LegacyMUL.uop` in place**, with no conversion:
  - it opens the UOP and maps block offsets (`Server/Map/ServerLandscape.cs:33-41, 191-196, 532`);
  - statics stay MUL (`:44-60`);
  - it advertises UOP to CentrED+ clients (`Server/Packets.cs:128-129`).
  - Read, not run.
- **UOFiddler** PR #179 (merged 2026-09-13, per GitHub) writes maps as MUL or UOP. It is a copy, diff and replace
  tool, not a dungeon editor.
- **Stay on UOP end to end.** A converted `map1.mul` left in the server folder would silently desync the server
  from the client, which is gate 6(b).

### 1.8 Recommendation and cost

| Part | What | Cost |
|---|---|---|
| Client | `-uofilesoverride` with three files, plus `tiledata.mul` if Chase agrees | ~30 lines of PowerShell |
| Server | One 117-plus-our-Trammel folder for the server and the package | Ships with the Q-063 swap |
| Build | Read the maps from that folder; checks in gate 4; gate 6; docs | ~60-80 lines |
| Optional | The startup hash log | ~40 lines of C#, plus a test |

Accepted costs: a 104 MB zip, full re-download on every update, and a map change always means a server restart and
a package release together.

---

## 1b. Moving the server to 7.0.117.0 (facts for the build task)

### 1b.1 Our coordinates in the changed blocks: none

- **Method:** `s1b\scan_coords.py` takes every adjacent pair of number literals in all of `server\customizations`,
  plus `Rectangle2D`s tested over their whole area.
  - That found 2,855 candidate pairs in 167 files (`s1b\coords_all.csv`). The 782 seeder rows are in
    `s1b\coords_placements.csv`.
  - Each pair was tested against the changed set: statics blocks plus land blocks, on Felucca and on Trammel.
- **Result: 0 hits.** The table below is one row per placement file. "Nearest" is the distance in tiles to the
  nearest changed block.

| Source | Map | Nearest |
|---|---|---|
| `ClusterFNewHavenSeeder.cs:23-71` | Trammel | 2,627 |
| `ClusterFNewHavenServicesSeeder.cs:60-189` (P17) | Trammel | 2,643 |
| `ClusterFInstitutionSeeder.cs:48-102` | Trammel and Ter Mur | 2,700+ |
| `ClusterFMineCampLayout.cs:18-76` (P16) | Trammel | 2,701 |
| `ClusterFRegistrarOfficeLayout.cs:20-67` (P19) | Trammel | 2,663 |
| `ClusterFRoyalCitySeeder.cs:41-98` | Ter Mur (unchanged) | n/a |
| `ClusterFGuildStarterPath.cs:206-223` / `ClusterFGuildHallSeeder.cs` | Trammel and Ter Mur | 2,600+ |
| `ClusterFOldHavenSeeder.cs`, `ClusterFOldHavenCleanup.cs`, `ClusterFSouthMineDecor.cs`, `ClusterFResetStone.cs`, `NewHavenQuestBoard.cs:69` | Trammel | 2,696+ |
| `CharacterCreation.cs:83-360` | Trammel | 1,297 |
| Despise (`DespiseRevamped\*`) | Trammel | 2,066+ |
| Shame (`Shame Revamped\*`) | Felucca and Trammel | 2,805+ |
| P22 pit thief, from its brief | Trammel | ~2,600 |
| Fountain of Fortune spot (`s2-fountain.md`) | Ter Mur (unchanged) | n/a |

**Stock content:**

- Pinned `Decoration/Britannia/skara.cfg` has 40 placements in changed blocks. None ends up inside a new wall.
  Two `Static 0x1036` see only dirt turn to grass.
- Area A is outside Skara Brae's town region (`regions.json:555`), so a house could be placed there in principle.

With no hits there was nothing to picture per coordinate. These renders show both areas, 114 beside 117:
`s1b\skara_fel.png`, `skara_tram.png`, `skara_fel_zoom.png`, `east_fel.png`, `east_tram.png`.

### 1b.2 Houses and spawners

`s1b\saves_scan.py` reads `Items.idx` and the base `Item` header directly, following pinned
`GenericEntityPersistence.cs:100-122, 273-320` and `Item.cs:816-1060`.

- **Test world:** 204,147 items, **0 player houses** (11 camps), 5,386 spawners, **0 spawners in a changed block**.
- **Retired live world:** **0 houses** and **0 spawners in a changed block**. Per D40 (`docs/bug-list.md:59`) the
  test world becomes the next live, so the test result is the one that counts.
- Items whose own tile changes:
  - test: 4 on Felucca and 6 on Trammel, all spawned reagents;
  - retired live: 5 on Felucca and 1 on Trammel, reagents plus the two stock statics.
- The test shard was running while it was read (it saved at 07:00 and 07:05). It was not started or touched.
- Mobiles were not parsed.

### 1b.3 Land, cell by cell

Pinned `UOPFiles.cs:24-100` format; `s1b\diff_land.py`.

| Facet | Land cells differing | Blocks | Where |
|---|---:|---:|---|
| Felucca | 140,114 | 2,300 | 19 blocks in A (forest to wooden floor), 2,281 in B (void to stone plateau) |
| Trammel | 192,841 | 3,285 | 13 in A, 3,272 in B |
| Ilshenar, Malas, Tokuno, Ter Mur | 0 | 0 | Container bytes only |

- Area A: x 736-791, y 2120-2167. Area B: x 6448-6959, y 3040-3623.
- The union of statics and land changes is **Felucca 2,310 and Trammel 3,295 blocks.** Q-063's 1,487 counted
  statics only.
- **Area A** is the Archers' Guild wing north of Skara Brae: +743/-152 statics on Trammel.
- **Area B** on Trammel removes a 22,979-static compound and replaces it with 12 stone-walled rings.
  - Nothing in pinned regions, teleporters, spawns or decoration touches B.
  - What B is for is unknown.
- `player-package.md` Part C's "Skara Brae box" (x 736-1023, y 2120-2559) is much larger than the data.

### 1b.4 tiledata and hues

`s1b\diff_tables.py`, layout per pinned `TileData.cs:303-375`.

- **Land tiles:** 0 of 16,384 changed.
- **Item tiles:** 345 new (0x6400-0x64FE and 0xB4D2-0xB52B) and 21 changed.
  - 3 change only an int the server skips.
  - **18 change flags:**

    | Tiles | Change |
    |---|---|
    | Moon Flower 0xB272-0xB277 | lose Impassable |
    | Unity tapestry 0xB3D2-0xB3D5 | lose Impassable |
    | Whimsy tapestry 0xB406-0xB409 | lose Impassable |
    | Farm_Stand 0xA90E-0xA90F | loses Foliage |
    | Firework Crate 0xB41B-0xB41C | gains Container |

  - **Each of the 18 is used 0 times** in any facet's statics, in either save, or in pinned or our code. Server
    collision does not change today.
- **hues.mul:** 17 hues differ; previously unnamed slots gain names and some colours. The server does not read it.
- **radarcol.mul:** 36 entries differ. The server does not read it.
- **Multis:** one new multi, 0x212B. The other 871 have identical component lists.

### 1b.5 What moves together, checked against the current tree

| Thing | Today | The build task changes |
|---|---|---|
| Live data | `docker-compose.yml:27` mounts `${CLIENT_DATA_PATH}` | At the live step, point `.env` at the new folder |
| Test data | `docker-compose.test.yml:41` mounts the **same** variable | `${CLIENT_DATA_PATH_TEST:-${CLIENT_DATA_PATH}}`, plus the variable in `.env` and `.env.example:5` |
| New folder | does not exist | A **copy** at `client-data\classic-client-7.0.117.0`. Never mount `UltimaOnlineVanilla`: EA's launcher patches it in place |
| Detected version | `UOClient.Load` reads `client.exe` (`Server/Client/UOClient.cs:36-44`) | Moves to 7.0.117.0 by itself |
| Kick floor | `ClientVerification.cs:52-55` sets the floor to the detected version when min and max are unset. `minRequired` is read with `GetSetting`, never written (`:34`). Staff are exempt (`:120`) | **Chase decides.** Recommended: add `"clientVerification.minRequired": "7.0.114.40"` to both `server\uo\modernuo\Configuration\modernuo.json` and `Configuration-test\modernuo.json`, the configs the compose files mount (`docker-compose.yml:18`, `docker-compose.test.yml:39`) |
| Package floor | `Setup.ps1:30`, `$minVersion 7.0.114.40`, also inside the zips already handed out | Nothing if the floor is pinned. Otherwise raise it and redistribute |

### 1b.6 Plan for the build task

**Prepare:**

1. Copy `UltimaOnlineVanilla` to `client-data\classic-client-7.0.117.0`.
2. Verify the copy: `client.exe` is 7.0.117.0, and the hashes of the map, statics, tiledata and multi files match
   the source.
3. Re-run `s1b\diff_statics.py` and `s1b\diff_land.py` against the copy. Expect 338 / 1,149 statics blocks and
   2,300 / 3,285 land blocks. Different numbers mean EA patched in between, and 1b.1 must be re-run.
4. Make the compose and `.env` change above.
5. Chase decides the floor.

**Test shard:**

6. Recreate the test containers. No image rebuild is needed.
7. Check the logs: `Automatically detected client version 7.0.117.0`, the `Restricting ...` line, no `TileMatrix`
   "not found" warnings, and no `MultiData` errors.
8. Walk the Archers' Guild wing (760-790, 2128-2160) on Felucca and Trammel with a **player** account.
9. Run one seeder dry run. It should report nothing to move.
10. Log in with a 117 client and stay past 20 seconds.

**Live, at a restart Chase already plans:**

11. Point `.env` at the new folder, apply the same `minRequired` setting, restart, and repeat the log checks.
12. Rollback is one `.env` line and a restart. No save migration is needed either way.

**Then the dungeon map edits** go into that same folder, after their own test pass. That is batch 1 in section 6.

---

## 2. Where it goes

### 2.1 Interior

**"Empty"** means void land `0x0244` with zero statics, in **both** 114 and 117. 0x0244 is the most common land ID
at x >= 5120; 0x0002 is not the filler.

Masked out:

- every Trammel rectangle in pinned `regions.json` (337), whatever its expansion range;
- 28,584 teleporter, spawn and decoration points;
- ServUO's Trammel `Regions.xml` rectangles, as a risk for future ports;
- the 114/117 changed zone plus 32 tiles.

Then whole blocks only, with a 16-tile buffer.

| Rank | id | x | y | Size | Notes |
|---|---|---|---|---|---|
| 1 | **A** | 5136-5247 | 1128-1263 | 112x136 | Classic strip. 24 tiles W of the Jail (5271-5312 x 1159-1192). Inside the fog-of-war grid. Keep building >= 20 tiles from x 5120 |
| 2 | C | 6160-6639 | 1832-2279 | 480x448 | Room to grow; use the middle (e.g. 6320-6479 x 1980-2139). Edges near ServUO-only Underwater World (N) and TOL Blackthorn (S) |
| 3 | D, E3 | 6496-6815 x 1552-1815; 6672-7151 x 776-1143 | | | Same properties as C, smaller margins |
| 4 | A2 | 5264-5359 | 1048-1135 | 96x88 | Squeezed between the Jail and Destard |

- One spot was rejected: 5520-5623 x 1416-1527 lies inside ServUO's Trammel Khaldun rectangle.
- Our shard's only extra regions are Despise's four, registered in code (`DespiseRevamped/Region.cs:33`,
  `DespiseController.cs:178-181`). None touches a candidate.
- **The x >= 6144 caveat:** `ClusterFExplorationManager.cs:31-38` and `ClusterFExplorationSync.cs:33-36` size
  Trammel as 6144 wide, and `:73` skips chunks with cx >= 768. A dungeon at C, D or E would never mark as explored.
  Nothing breaks.
- Renders: `s2\overview_strip_x5120.png`, `s2\overview_candidates.png`, `s2\cand_A_strict.png`,
  `s2\cand_C_D_strict.png`.

### 2.2 Entrance building

- New Haven proper has no abandoned building. The ruins are 622 "ruin*" statics in 28 clusters, all in **Old Haven**
  (3572-3760).
- Old Haven's own town region, "Haven", is `MaxExpansion: SE` (`regions.json:1670-1684`). Pinned registers a JSON
  region only within its expansion range (`RegionJsonSerializer.cs:60`), so on our Endless Journey shard it does
  not exist.
- That leaves only "Haven Island" (`NoHousingRegion`, 3314-3814 x 2345-3095, `regions.json:1499-1506`) over B1: no
  housing, Young protected.

| id | Building | Verdict |
|---|---|---|
| **B1** | Ruined "Second Bank of Haven", room 3616-3625 x 2610-2621, wooden floor at z0, open to the NE (3624-3626 x 2610-2613) | **Top pick.** Hole centred on **3619,2620** (a free 3x3) |
| B2 | Ruined provisioner's, 3665-3680 x 2587-2600 | Second: heavily decorated |
| B3 | Ruined blacksmith compound | Rejected: Skeleton x10 spawner at its centre |
| B4 | South-east shore inn block | Rejected: roofed and crowded |
| B5 | Uzeraan's mansion | Rejected: intact, with a teleporter and quest decoration |

**B1 has neighbours to know about:**

- Pinned spawners inside or near the room:
  - inside: a Healer (3618,2614, post-UOML) and a Banker/Minter (3620,2617, UOML);
  - near: a Skeleton spawner at 3635,2625 whose range of 15 reaches the hole.
- `ClusterFOldHavenCleanup.cs` targets the room's NPCs. Whether it, or `[Decorate`, has run on the test world is not
  verified.
- A pinned decoration `BarredMetalDoor` sits at 3626,2621.
- 114 and 117 are identical across the room.

**Overlap checks, all clear:**

| Neighbour | Distance from B1 (tiles) |
|---|---:|
| P16 mine camp | >130 |
| P19 registrar | >150 |
| P17 (New Haven only; its nearest Old Haven point is the ankh at 3606,2582) | 30 |
| P22 pit thief | ~180 |
| Quest board and quest NPCs | >60 |

`CharacterCreation.cs:83` has an old Haven start location at 3677,2625, 58 tiles east of B1.

Renders: `s2\bldg_B1_second_bank.png` (and B2 to B5), `s2\newhaven_overview.png`, `s2\cat_oldhaven_south.png`.

### 2.3 `DungeonRegion` and defining a region

**What `DungeonRegion` gives** (`UOContent/Regions/DungeonRegion.cs`, 33 lines):

- **`YoungProtected => false` (:21).** Monsters attack Young players: `PlayerMobile.cs:4341-4350`,
  `Notoriety.cs:214-218`. Young players also get `YoungDungeonWarningGump` on entry (`BaseRegion.cs:76-81`).
- `Entrance` (:23) is used by `YoungDeathTeleport` (`PlayerMobile.cs:4398-4403`).
- No housing (:25).
- Dungeon light level 26 (:27-30, `LightCycle.cs:15`).
- Stuck menu allowed off Felucca (:32).
- **Travel is not restricted on Trammel.** `SpellHelper.CheckTravel` blocks only Felucca dungeons and a fixed list
  of ML dungeon names (`SpellHelper.cs:648-687, 733-737, 836`). To forbid recall, gate and mark, use
  `NoTravelSpellsAllowedRegion : DungeonRegion` (`NoTravelSpellsAllowedRegion.cs:6, 23-27`).

**How regions are defined:**

- Pinned loads one file, `Data/regions.json` (`RegionJsonSerializer.cs:98`), whose types are registered in code
  (`RegionJsonRegistration.cs:9`). Orc Cave (`regions.json:2746-2759`) is a template.
- Our shard has never edited `regions.json`. Its precedent is a **code-registered region**: Despise at priority 51,
  with the reason recorded (`DespiseRevamped/Region.cs:44-55`).
- Recommended: a code-registered `DungeonRegion` subclass over the built rectangle, with Entrance = B1 and its own
  GoLocation and Music.
- **Young players are Chase's decision.** Stock behaviour means Young players are attacked inside. A Young-safe
  dungeon is a subclass with `YoungProtected => true`, which is a deviation for `docs/fidelity-principle.md`.
- This matters more here than on OSI. The shard made Young last two weeks of play and removed the 450-skill exit
  (`Account-young-duration.patch`, `PlayerMobile-young-time-only.patch`), so many visitors to a starter dungeon will
  be Young.

---

## 3. The four new resources

### 3.1 Harvest by region

**How our extensions hook in.** They are runtime mutations of pinned's singleton harvest definitions, not patches:

- **Mining** (`ClusterFMiningExtension.cs:37-41, 66-134`):
  - appends 8 `HarvestResource`s, all `reqSkill` 100 with one type each, and 8 veins (weights 8 down to 1, Iron as
    the fallback) to `Mining.System.OreAndStone`;
  - sets `RandomizeVeins = false` (`:131`);
  - that switches on pinned's coordinate-seeded 8x8 bank veins (`HarvestDefinition.cs:104-144`).
- **Lumberjacking** (`ClusterFLumberjackingExtension.cs:200-259`) does the same but keeps random veins.
- **`Give` overrides:** both systems are made `partial` so we can override `Give`. Mining uses a replacement file
  (`patches\Mining.cs`, with only line 8 changed); Lumberjacking uses a `sed` in `apply-patches.sh:359-365`.

**Pinned has no per-region harvest table.** There is no `RegionalVeins`, and `Definitions` is init-only
(`HarvestSystem.cs:9`).

**The seam is `MutateResource`** (`HarvestSystem.cs:140`, body `:332-352`; I confirmed it is virtual and that
neither pinned nor our code overrides it):

- it receives the target map and location;
- its return value is what the skill gate at `:147` checks, so a region resource can carry its own low skill band.

**Design:** one new additive file. It overrides `MutateResource` in our existing `partial Mining` and
`partial Lumberjacking`: inside the dungeon region it returns Dawnstone or Rootwood (else Iron or regular log),
and everywhere else it calls `base`.

- Nothing changes outside the region.
- Bank depletion still uses the global banks, so the world-map haze (`ClusterFExplorationSync.cs:275`) keeps working.
- The prospector's tool and the gargoyle pickaxe become no-ops in the region.
- **Size: ~80-120 lines, no patch.**

### 3.2 Mineable and choppable tiles

- **Mining land list:** `Mining.cs:24-50`, ranged. It is 22 pairs; 436 IDs were counted against tiledata.
  - The cave terrain is land 0x0245-0x026D ("cave", 41 IDs), plus the "rock" sets (0x01D3-0x01DA and the rock
    members of 0x021F-0x0243 and 0x06EB-0x075C).
  - **A wall built as raised terrain from these IDs mines natively, with zero code.**
- **Mining static list:** `Mining.cs:52-55` is only 0x053B-0x054F, and all 21 are "cave floor".
- **Static "cave wall" items are not mineable in pinned.** None of the 35 IDs (0x025C-0x0276, 0x027D-0x0280,
  0x2166-0x2169) is in either list. There are three ways to build walls players can mine:
  1. terrain walls (recommended);
  2. cave-floor statics at the wall foot (OSI's model);
  3. an extra region-only harvest definition through `GetDefinition`/`CheckResources` overrides (~+40 lines, s3a
     section 2.4).
- **Choppable:** `Lumberjacking.cs:11-34`, an exact list of 149 IDs. **Tiledata has no root, trunk or
  petrified-wood static at all.** Choppable "giant roots" must use listed tree statics, such as "tree"
  0x0CCA-0x0CCD and 0x0D41-0x0D44, or "Yew tree" 0x12B5-0x12C7. Anything else needs the region-only override.
  How they look as roots in a cave is untested.

### 3.3 Dawnstone (metal)

**How the 8 extended ores were added:**

- The enum and tables are the full-file replacement `customizations\ResourceInfo.cs` (859 lines become 1,170).
- The ore and ingot classes are `ClusterFExtendedOres.cs:23-151`.
- Blacksmithy registers them with `AddSubRes` at server start (`ClusterFMiningExtension.cs:174-181`).
- BODs go through `patches\BulkMaterialType.cs`, `SmallSmithBOD-PostValorite.patch` and `patches\LargeSmithBOD.cs`.

**Placement rules:**

- **Append `Dawnstone = 18` after Celestial.** Values are saved as ints: on ore, on crafted gear, and as raw `int`
  keys in `HammerOfHephaestus.cs:117, 148-176`.
- Widen the metal range at `ResourceInfo.cs:1092`.
- The `m_MetalInfo` entry must come directly after Celestial's, because `GetIndex` is `resource - Iron`
  (`:1116-1126`).

**Consumers:** the extended ore names appear in **21 files, 403 lines**. The per-file table is in s3a section 3.3.

**Minimum viable Dawnstone:**

| Piece | Lines |
|---|---|
| `ResourceInfo.cs` | ~25 |
| Ore and ingot classes | ~15 |
| One Blacksmithy `AddSubRes` line | 1 |
| The 3.1 harvest file (shared with Rootwood) | 80-120 |
| `CompactOreSatchel` accepted types | +2 |
| **Total** | **4-5 files, ~125-165** |

- **Tinkering has never had the extended ores.** Dawnstone would be the first, at one line. Pinned smelts unknown
  ores at difficulty 50 (`Ore.cs:176-187`), a sensible starter value.
- **Recommended: no BOD or commission tier.** That would touch 6+ files, two of them on the patch route.
- **Give Dawnstone two types**, ore and granite, because of F1.

### 3.4 Burrowhide (leather)

**How pinned does tiers:**

- Enum values 101-104 (`ResourceInfo.cs:19-22`).
- Two info arrays, `m_LeatherInfo` and `m_AOSLeatherInfo`.
- `BaseHides`/`BaseLeather` with four subclasses each (`Hides.cs`, `Leathers.cs`). Hides scissor to leather. The
  resource is saved as an int (`Hides.cs:52`).
- `HideType` enum in `BaseCreature.cs:113-119`; the carve chain is at `:1649-1768`.
- Tailoring registers leather with `SetSubRes(typeof(Leather))` plus `AddSubRes` at 0/65/80/99
  (`DefTailoring.cs:658-665`).
- `SubRes2` is unused by tailoring.

**Creatures per hide type:**

| Tree | Spined | Horned | Barbed |
|---|---:|---:|---:|
| Pinned | 19 | 5 | 9 |
| Ours | 14 | 7 | 2 |

The name lists are in s3b section 1.1.

**What a fourth tier needs:**

- Append `BurrowhideLeather = 105` and widen the leather range at `:1093`.
- Add entries to both info arrays.
- New hide and leather classes, plus a `CraftItem.cs:80-83` equivalence pair.
- A tailoring `AddSubRes` at server start.
- **Carving through `OnCarve` overrides on the dungeon creatures (`BaseCreature.cs:1649`), not a new `HideType`.**
  That enum is pinned, so extending it would need a patch.
- A `HuntersSatchel` case (F4).
- No BODs: they would mean range edits in 11 pinned BOD files.

**Size: 6-8 files, ~150-250 lines, 0 patches.**

### 3.5 Rootwood (wood)

**How pinned does tiers:**

- Enum 301-307.
- **All six wood `CraftAttributeInfo` entries are empty.** The only wood bonuses are on bows, in a private closed
  switch (`BaseRanged.cs:239-281`).
- Carpentry and Bowcraft register wood with `AddSubRes` at 65/80/95/100.

**Ours:** 8 woods at 308-315, integrated through **11 real files out of 16 hits** (s3b section 2.2). `ResourceInfo.cs:1095`
was never widened (F3).

**What one more wood needs:**

- Append `Rootwood = 316`.
- Widen the range. **This also changes the 8 existing woods' look, so it is a decision, not a side effect.**
- An info entry; log and board classes; an equivalence pair.
- Two `AddSubRes` lines (Carpentry and Fletching).
- One P13 discovery-dictionary line (`ClusterFLumberjackingExtension.cs:33-57`). No serializer change, because
  `WoodDiscoveryEntry` v1 is type-agnostic.
- A satchel map line.
- The region harvest (3.1).
- A bow bonus needs **one pinned patch** to `BaseRanged`. Without it Rootwood is cosmetic, like the 8 extended woods.

**Size: 7-9 files, ~150-250 lines.**

### 3.6 Gloomsilk (cloth)

- **Pinned has no cloth resource:**
  - `CraftResourceType` has no Cloth value (`ResourceInfo.cs:40-47`).
  - `Cloth`, `UncutCloth` and `BoltOfCloth` carry no resource field.
  - Clothing reads no resource attributes at all.
- **Option A, recommended: small and near.** A `GloomsilkCloth : Cloth` subclass with a fixed hue (plus a bolt if
  wanted).
  - It is consumed by every cloth recipe, because consumption matches subclasses (`Container.cs:825, 863, 891`).
  - Its hue carries into clothing (`CraftItem.cs:357-379`).
  - **1 file, ~60-100 lines.** It gives no bonus, and players cannot select it in the craft gump.
- **Option B: a real tier.** A new resource type, a resource field on three pinned cloth items, `SubRes2` on 49
  tailoring recipes, and a `BaseClothing` `OnCraft` path. **That is a subsystem: ~400-700 lines and 3-5 pinned
  patches.**
- **Drop:** a new `CaveSpider` uses `PackItem`, as spiders already do with spiders' silk (`GiantSpider.cs:43`), or
  an `OnCarve` override.

### 3.7 "Low skill, modest bonuses" in numbers (first proposal)

**Existing lowest tiers** (pinned; our copy is identical for these rows):

| Tier | Harvest req / min / max | Craft gate | Bonuses |
|---|---|---|---|
| Dull Copper | 65 / 25 / 105 (`Mining.cs:116-123`) | Blacksmithy and Tinkering 65 | Armour phys resist 6, durability 50, lower requirements 20; weapon durability 100, lower requirements 50 (`ResourceInfo.cs:61-78`) |
| Spined | carved | Tailoring 65 | Phys resist 5, luck 40 (`:234-248`) |
| Oak | 65 / 25 / 105 (`Lumberjacking.cs:72`) | Carpentry and Bowcraft 65 | None, except bows: luck +40, damage +5 (`BaseRanged.cs:245-249`) |

**Proposal.** Harvest and craft halfway down, bonuses about half, no runic tools:

| Resource | Harvest | Craft | Bonuses |
|---|---|---|---|
| Dawnstone | 45 / 5 / 85 | 45 | Phys 3, durability 25, lower requirements 10; weapon durability 50, lower requirements 25 |
| Burrowhide | carve | 45 | Phys 2, luck 20 |
| Rootwood | 45 / 5 / 85 | 45 | Bows: luck +20, damage +2 (needs the patch) |
| Gloomsilk | spider loot | n/a | Hue only |

- If the starter tier should not undercut the 65 gate, use 65 for crafting.
- All four append at the top of their enum ranges, so keep them out of every range-based table (BODs, random
  resource picks).
- Every number here is a deviation to record in `docs/fidelity-principle.md` once adopted.

---

## 4. The three ports (pub57)

None of the three is in pinned or ours today, searched by name and by behaviour. Every recommended route makes 0
upstream changes.

| System | pub57 | Dependencies | Pinned covers | Verdict |
|---|---|---|---|---|
| **MiniChampionSystem** | 3 files, 1,015 lines | None of XmlSpawner, PointsSystem, Core checks, regions or quests (grep). Needs ServUO core `Map.GetSpawnPosition` (17 lines, inline it). Stock table: 80 types; 33 pinned, 39 ours, 7 clan types ported under other names (Q-056), 1 leaf missing (`EssencePersistence`, 62 lines) | Nothing. `ChampionSpawn` always builds an altar and platform, and a new type throws in `ChampionTitleContext.cs:40-45`. `GauntletSpawner` is one type per room, scaled by player count | **Small, near: ~610 lines for the engine plus our one entry** |
| **Underworld PuzzleRoom** | 8 files, 788 lines | `BaseDecayingItem` (142, missing in both trees; carrier for 42 ServUO classes). `CircuitTrapGump` sits on ServUO's `BaseGump`, which **collides by name** with pinned's, so rewrite it on `DynamicGump`. Its `ExperimentalGem` reward is a subsystem, so replace it | `TicketTeleporter` (`ML Quests/Items/Teleporters.cs:91-141`) **is** `PuzzleRoomTeleporter`. `PowerGenerator`/`ControlPanel` is the circuit puzzle. `StrongBoxPuzzle`/`MetalGoldenPuzzleChest` is the mastermind | **Medium, near: 9 files, ~1,150-1,180.** A zero-port alternative loses only the timed key chain |
| (Maze of Death) | 7 files, 1,717 lines | A 372-line region with a literal Ter Mur path table | Nothing | **Subsystem, skip** |
| **Tomb of Kings chambers** | 5 files, 547 lines | All resolve: `Blocker`, `LOSBlocker` and `SilverSerpent` in pinned; `UndeadGuardian`, `PutridUndeadGuardian` and `WeakEntityCollection` in ours | `RaiseSwitch` plus `RaisableItem` (`Engines/Khaldun/`) = a lever that opens a passage and closes it after N minutes. `Spawner` with `Group = true` (`BaseSpawner.cs:85, 966-977`) = respawn only when all are dead | **The size is small; the design is wrong for us.** Its literal Ter Mur tables rebuild on every boot and re-randomise the levers. Redesign as one `ChamberController` (~300-350 lines), or use the zero-port set |

**`LeverPuzzleController`** is welded to Doom: Malas coordinates and regions (`LeverPuzzleController.cs:61-70`,
`LeverPuzzleRegions.cs:12, 89`). It cannot be reused.

**Traps and teleporters:**

- Pinned has 8 `BaseTrap` types: FireColumn, FlameSpurt, Gas, GiantSpike, Mushroom, Saw, Spike and StoneFace.
- It has 7+ teleporter variants.
- None of the three systems uses floor traps, so nothing needs porting for traps.

**The Burrow Mother ends the mini champ with no engine change.**

- A boss is just the last level with one `MiniChampTypeInfo(1, typeof(X))`, as Meraktus is
  (`MiniChampType.cs:383-386`).
- She needs to be a `BaseCreature`, plus one enum member and one table entry **appended at the same index**.
  `m_Table` is positional and the type is saved as an int (`MiniChampionSpawn.cs:400`).
- **Four surprises to design around:**
  - There is no completion hook or reward beyond her own loot.
  - `BossSpawnPoint` applies to **every** creature at every level (`MiniChampSpawnInfo.cs:72-75`).
  - Earlier levels' creatures linger until the cycle stops.
  - An inactive controller restarts itself after a reboot (`MiniChampionSpawn.cs:448-451`).
- **Placement:** drop `[GenMiniChamp]`, which hard-codes 14 Ter Mur and Malas controllers, and place ours from our
  own generator using our `WeakEntityCollection`.
- **Serialization:** switch to generated serialization. No migration is needed, assuming no ServUO save is ever
  imported.
- **Test:** ship it with one, per `docs/subsystem-policy.md`.

---

## 5. Gear, parts, upgrades and quest

### 5.1 No-trade

**Pinned has a real no-trade flag: `virtual bool Nontransferable => QuestItem` (`Server/Items/Item.cs:522`,
re-read).** It refuses:

- dropping on a player, which is how secure trade starts (`:3400-3415`, `Mobile.cs:7560-7568`);
- dropping into any container except the owner's top-level backpack (`:3424, :3461`). That excludes the bank box,
  sub-bags and the trade container;
- dropping on the ground (`:3513`);
- splitting a stack (`Mobile.cs:5033`).

It also keeps the item on death (`:2200, :2230`).

- It is used by 25 overrides in 24 files. The non-quest precedent is `ArcaneFocus.cs:32`.
- **`LootType.Blessed`, `BlessedFor` and `Insured` do not block trade.** They only keep items on death, block
  stealing and insuring, and are skipped by `DestroyEquipment`.
- The only bind-to-one-character pattern is the talisman's `CanEquip` owner check (`BaseTalisman.cs:340-361`).
- **Ours today:** P15/F-9 binds the *grant*, not the items. A per-character record replaces a lost kit item for 10
  scrip only when `OwnsCopy` finds none (`ClusterFGuildStarterPath.cs:423-490`). That check is reusable.
  - Our existing set pieces are blessed only.
  - Our tree uses neither `Nontransferable`, `AllowSecureTrade` nor `BlessedFor`.
- **Recommended piece:** new classes on our `BaseSet*` carriers with:
  - `Blessed`;
  - `BlessedFor = owner`;
  - `Nontransferable => true`;
  - an owner check in `CanEquip`;
  - `AllowSecureTrade => false`.
- **Chase decides the storage strictness.** Stock no-trade bars the bank box and bags.

### 5.2 Crafter upgrades on no-trade gear

| Option | What pinned and ours allow | Cost |
|---|---|---|
| (a) Owner only | Works as stock: the target is in the owner's own pack or worn | Lowest, only the 5.3 craft entry. Removes the crafter economy |
| (b) Together, with consent, the item never moves | **(b2), recommended:** the owner targets a crafter within 2 tiles of a forge or loom. The crafter gets a gump; on accept, the code checks the crafter's skill against the threshold, consumes the parts and raises the level. It calls `CheckSkill` directly, as our Imbue gump does (`ArtificersImbueGump.cs:1406`). (b1), crafter-initiated, needs `AllowNonlocal` (`Target.cs:115-120`) and only sees **worn** pieces | ~150-250 lines (estimate) |
| (c) Through a trade window | Override `OnDroppedToMobile`, `OnDroppedInto`/`Onto` and `AllowSecureTrade` to allow a qualifying counterparty | Moderate, plus a **hostage risk**: once traded, the owner's only recourse is the replacement quest. Not recommended |

Stock repair and enhance require the item in the crafter's own pack (`Repair.cs:269, 343, 414`; `Enhance.cs:34`),
so OSI's model is "hand it over", which no-trade forbids.

### 5.3 Applying an upgrade, and storing it

**Pinned's `CustomCraft` already does "target an item, consume resources, modify it"**
(`Engines/Craft/Core/CustomCraft.cs:6-34`):

- Its only user is `TrapCraft` (`DefTinkering.cs:590-695`).
- Our `CraftItem.cs` checks resources and skill, consumes, then calls `customCraft.CompleteCraft`
  (`customizations\CraftItem.cs:1066-1178`).
- Parts go in with `AddRes`. The 30/50/70 threshold is `minSkill` on three entries.
- Blacksmithy already demands an anvil and forge (`DefBlacksmithy.cs:110-117`). A loom check would be ours to add,
  using `ILoom`.
- Registration is additive at server start, following `TinkeringCraftRegistrations.cs:29-55`.

**Storage:**

- New types only: `[SerializationGenerator(0, false)]` with `[SerializableField(0)] _upgradeLevel`. **No migration
  is needed**, unlike PetMimic's nine schema files.
- Recompute the item's stats from base on every change, so a replacement piece starts at base level for free.

### 5.4 Durability

- **Armour, clothing and shields with initial hits 0/0 never wear.** See `BaseArmor.cs:771`,
  `BaseClothing.cs:368` and `BaseShield.cs:80`. Ilhenir and `DestroyEquipment` skip them too.
- Our Initiation pieces do wear (150 hits).
- **Weapons at 0/0 are deleted on the 1-in-25 wear roll.** `BaseWeapon.cs:2080-2108`; I re-read it.
  - Set weapons need high durability plus self repair, or an override.
  - Note `patches\BaseWeapon-talisman-durability.patch` exists; it was not read.
- **Death:** pinned has no durability loss on death. Blessed items cannot be insured (`PlayerMobile.cs:3817`).

### 5.5 Jewelry

- **Tinkering makes jewelry.** It has 9 `AddJewelrySet` calls (`DefTinkering.cs:145-160, 380-388`), and ours adds 4
  gargish entries.
- **Template for a multi-part recipe:** the ML magic jewelry (`DefTinkering.cs:511-567`). For example
  `ResilientBracer` = ingots + `CapturedEssence` + gems. Parts slot in with `AddRes`.
- **`BaseJewel.OnCraft` is not virtual** (`BaseJewel.cs:128`), unlike the armour, weapon and clothing versions.
  Apply properties in the constructor or through a `CustomCraft`.
- Jewelry is tradeable, so no binding.

### 5.6 Repeatable quest

**ML Quests is the New Haven board's engine** (`NewHavenQuestBoard.cs:50, 98-99`).

- `OneTimeOnly` (`MLQuest.cs:61`), `HasRestartDelay` (`:63`) and a virtual `GetRestartDelay` (`:240`). Pinned uses
  `HasRestartDelay` 50 times in 3 files.
- `CanOffer` (`:117-183`) can refuse a player who still owns every piece, reusing `OwnsCopy`.
- A custom `MissingSetPieceReward : BaseReward` overrides `AddRewardItems` (`Rewards/BaseReward.cs:20`). It hands
  out only the missing pieces, at base level and bound. An empty list is handled (`MLQuestEntry.cs:354-416`).
- **That is the whole replacement path.**
- The old `QuestSystem` (`RestartDelay`, `QuestSystem.cs:61`) is heavier and not recommended.

---

## 6. Build plan

### 6.1 Batches, ranked

The sizes are estimates. Those marked "guess" have no measured basis.

| # | Batch | Content | Size | Depends on |
|---|---|---|---|---|
| 0 | **F1 probe and fix** | A test: a GM stone-mining miner harvests an extended ore. Fix by giving the 8 extended ores a second type (granite), or by guarding `GetResourceType` | ~20-40 lines plus a test | none |
| 1 | **Q-063 swap, test first** | The 1b.6 plan, the compose and `.env` variable, the `minRequired` decision | Config only, plus operations | Chase: the floor |
| 2 | **Map pipeline** | `Play.ps1` override (~30), build gates 4 and 6 (~60-80), optional startup hash log (~40 C#), a docs policy entry | ~130-150 | 1 |
| 3 | **Region and harvest** | A code-registered `DungeonRegion` subclass over candidate A (~30); the `MutateResource` overrides (~80-120) | ~110-150 | Chase: Young and travel |
| 4 | **Resources** | Dawnstone (~45 beyond batch 3); Burrowhide (~150-250); Rootwood (~150-250; first decide F3, the wood range); Gloomsilk option A (~60-100) | ~400-650 | 3; Chase: numbers, F3, cloth option |
| 5 | **The map itself** | In CentrED# on a copy of the batch 1 folder: terrain cave walls from mineable land IDs, roots from listed tree statics, the B1 hole, teleporters both ways. Build-time check: every static ID exists in 114 tiledata | Editing work, not code | 1, 2, 3 |
| 6 | **Creatures and mini champ** | The MiniChamp port (~610 plus a test), Burrow Mother, Gloom Queen, the monster families with part drops and `OnCarve`/`PackItem` resources | ~610 plus ~500-800 (guess) | 4 |
| 7 | **Rooms** | Zero-port first: `RaiseSwitch`/`RaisableItem`/`Spawner(Group)` chambers, `PowerGenerator`, `StrongBoxPuzzle`, `TicketTeleporter`, pinned traps. Later, if wanted: a ~300-350-line chamber controller, or the PuzzleRoom key chain (~1,150) | ~0 now | 5, 6 |
| 8 | **Set, parts, upgrades** | `BaseDungeonSet*` (Nontransferable, `BlessedFor`, `CanEquip`, `_upgradeLevel`, `ApplyLevel`); the parts items; the upgrade path ((b2) gump ~150-250, or `CustomCraft` entries); weapon durability; jewelry recipes | ~600-900 (guess) | 4, 6; Chase: crafter option, storage |
| 9 | **Quest** | Repeatable ML quests on the board, `MissingSetPieceReward`, `CanOffer` gate | ~200-300 (guess) | 8 |

**Order:**

- Batches 0, 1, 3 and 4 can run in parallel once the decisions are in.
- Batch 5 waits for 1 to 3.
- Batches 6 to 9 follow the map.

### 6.2 Decisions for Chase, collected

1. **Kick floor:** pin `clientVerification.minRequired` at 7.0.114.40 (recommended), or let it follow to 7.0.117.0
   and redistribute the package.
2. **Ship `tiledata.mul` too?** About 0.11 MB, and it pins collision flags. Recommended, under the same EA-files
   exception.
3. **Young players in the dungeon:** stock `DungeonRegion` (Young attacked, warned on entry), or a Young-safe
   subclass (a deviation).
4. **Travel:** recall and gate allowed (stock Trammel), or `NoTravelSpellsAllowedRegion`.
5. **Interior A or C.** A is recommended. Pick C if the dungeon will grow past ~110 x 130.
6. **Entrance B1**, among Old Haven's undead spawners. Fine for the story? Or B2.
7. **Widen the wood range (F3).** It changes how the 8 existing woods look, probably for the better (hue and name).
   Verify in a client first.
8. **Gloomsilk:** cosmetic subclass (A) or a real tier (B, a subsystem).
9. **Starter numbers** (section 3.7). Craft gate 45, or 65 so the tier does not undercut existing ones.
10. **Crafter option:** (a), (b2) recommended, or (c).
11. **No-trade storage:** top-level backpack only (stock), or also bags and the owner's bank.
12. **Rootwood bow bonus:** one pinned patch, or leave it cosmetic.

### 6.3 Promotions this note proposes

These are not done here; `docs/` is the overseer's.

- `docs/bug-list.md`: F1 (latent crash, ours), F3 (wood range, ours), F4 (hide downgrade, ours), F2 (pinned, harmless).
- `docs/fidelity-principle.md`: the four custom resources and their numbers; any Young-safe dungeon region.
- Package policy: the EA-files exception for the edited maps (and tiledata, if agreed). This replaces
  `Build-PlayerPackage.ps1:20`'s premise.
- `notes/player-package.md` Part C: correct the changed-area boxes and add the land counts (1b.3).

---

## Not verified

- Nothing was built or run. Every pinned, TazUO and CentrED# behaviour here comes from reading source.
- That the shipped TazUO DLLs were built from `3212623f`. The version string and tag match, and the DLLs contain
  the override strings.
- Whether the `UltimaOnlineVanilla` map UOPs, dated 2026-09-06, are EA's patch or a local edit. Their hashes differ
  from the server's either way.
- Hardlink behaviour under Program Files; .NET `Optimal` zip sizes, which were estimated with zlib 6.
- Live or test world state at B1: whether `[Decorate`, `ClusterFOldHavenCleanup` and `ClusterFOldHavenSeeder` have
  run. Walkability of B1's north-east gap.
- Client behaviour at x >= 6144, and whether anyone at sea near x 5119 can see candidate A.
- F1 and F3 in game.
- The weapon 0/0 path's overridability; jewelry `ICraftable` re-implementation; the `PropertiesGump` signature in
  the MiniChamp port.
- Mobiles in the saves were not parsed. Art and housing.bin were compared by hash only.
- The line sizes for batches 6, 8 and 9 are guesses.
