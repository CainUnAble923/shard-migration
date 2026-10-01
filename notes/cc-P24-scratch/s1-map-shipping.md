# P24 s1: shipping edited Trammel map files in the player package

Read-only research, 2026-10-01. Nothing outside this folder was changed.

Sources and the exact revisions read:

- **TazUO** source: tag `v26.0909.63`, commit `3212623f63436be1c0f4e3b308b202b29597c026`
  (github.com/PlayTazUO/TazUO, found with `git ls-remote --tags`, shallow-cloned into the session
  scratchpad, not into the repo). That tag matches `D:\UO\TazUO\client\v.txt` = `26.0909.63` exactly.
  Below, `TazUO:` means `src/` of that commit.
  Binary cross-check: the shipped `D:\UO\TazUO\client\TazUO.dll` contains the UTF-16 string
  `uofilesoverride` once, and `ClassicUO.IO.dll` / `ClassicUO.Assets.dll` contain `UOFilesOverrideMap`.
  I counted the byte occurrences. I did not decompile the DLLs, so I have not proven they were built
  from this exact commit. The version string and tag do match.
- `D:\UO\ClassicUO\ClassicUO` is **not source**. It is an old binary ClassicUO install (Mono/FNA,
  `ClassicUO.exe` dated 2023-02-16, its `settings.json` says `clientversion 7.0.98.1`, set up for another
  shard plus Razor). The only `.cs` files in it are RazorEnhanced example scripts. I did not use it.
- **ModernUO** pinned `D:\UO\ModernUO-pinned` at `7c9215d97` (checked with `git log -1`).
- **CentrED#**: github.com/kaczy93/centredsharp at HEAD `50d23f7a` (2026-06-30), shallow-cloned to the scratchpad.

## 1. Where TazUO reads Trammel (map index 1)

All paths go through `UOFileManager.GetUOFilePath(file)` (`TazUO: ClassicUO.Assets/UOFileManager.cs:103-109`).
It checks the override map first and otherwise uses `Path.Combine(BasePath, file)`. `BasePath` is
`ultimaonlinedirectory` (`UOFileManager.cs:22-25`, `ClassicUO.Client/Client.cs:194`).

UOP or MUL: `IsUOPInstallation = Version >= CV_7000 && File.Exists(GetUOFilePath("MainMisc.uop"))`
(`UOFileManager.cs:146`). An EA 7.x install has `MainMisc.uop` (present in `D:\UO\UltimaOnlineVanilla`),
so this is true for every player.

`MapLoader.Load`, loop over map index `i` (`TazUO: ClassicUO.Assets/MapLoader.cs:139-213`):

| Order | File for i=1 | When | Line |
|---|---|---|---|
| 1 | `map1LegacyMUL.uop` | if `IsUOPInstallation` and the file exists | 141-143 |
| 1x | `map1xLegacyMUL.uop` | opened alongside 1 if present | 150-156 |
| 2 | `map1.mul` (+ `map1x.mul`) | **only** if the UOP branch is not taken | 161-174 |
| 2d | `mapdifl1/mapdif1/stadifl1/stadifi1/stadif1.mul` | only in the MUL branch | 176-187 |
| 3 | `statics1.mul`, `staidx1.mul` | always | 190-200 |
| 3x | `statics1x.mul`, `staidx1x.mul` | always opened if present | 202-213 |

- On an EA install, the files TazUO actually reads for Trammel are **`map1LegacyMUL.uop`, `statics1.mul` and
  `staidx1.mul`**. TazUO never applies the dif files to a UOP install. A loose `map1.mul` is ignored while
  `map1LegacyMUL.uop` exists.
- The `x` files are used only when `LoadMap(i, useXFiles: true)` (`MapLoader.cs:363-404`). The client asks for
  that when the server sets `CLF_UNLOCK_FELUCCA_AREAS` (0x8000) (`ClassicUO.Client/Game/World.cs:226,234,275`).
  On our server that flag is off: ModernUO's `NewFeluccaAreas = 0x8000` (`Projects/Server/ExpansionInfo.cs:117`)
  is `false` in the shard's `Configuration/expansion.json:53` (Endless Journey) and in all 12 entries of the
  pinned `Distribution/Data/expansions.json`, which I counted. **So `map1x`/`statics1x`/`staidx1x` are opened
  but not used.**
- Silent failure mode: if `map1` ends up null, `MapLoader.cs:229-235` copies map0's files into slot 1, so
  **Trammel would render as Felucca without any error**. A missing `statics1` gives a Trammel with no statics.
- `facet01.mul` (the pre-rendered paper map used by `MultiMapLoader`) is found with
  `Directory.GetFiles(FileManager.BasePath, "*.mul")` (`ClassicUO.Assets/MultiMapLoader.cs:35-40`). That
  **bypasses the override map** and always comes from the player's folder.
- `radarcol.mul` is a per-tile-ID colour table, loaded once (`ClassicUO.Assets/HuesLoader.cs:46-52`). It is not
  per-map, so a map edit does not need it.
- The world map PNG cache is keyed by the MD5 of the map and statics contents
  (`ClassicUO.Client/Game/Map/Map.cs:532-552`, saved as `Data\Client\MapsCache\map1_<hash>.png`). An edit
  regenerates it by itself.

## 2. Pointing TazUO at package files while everything else stays in the player's folder

**TazUO already has a per-file override, so no code change is needed.**

- `UOFilesOverrideMap` (`TazUO: ClassicUO.IO/UOFilesOverrideMap.cs:16-55`) reads a text file of
  `filename=fullpath` lines. Lines starting with `;` or `#` are skipped (line 36). The key is lowercased
  (line 40). The line is split on `=` and must yield exactly 2 parts (lines 37-38), and the value is **not
  trimmed**.
- `GetUOFilePath` consults it first (`UOFileManager.cs:105`). It is loaded before any loader runs
  (`UOFileManager.cs:144`).
- It is set **only on the command line**: `-uofilesoverride <file>` or `-filesoverride <file>`
  (`ClassicUO.Client/Main.cs:310-313`). There is no `settings.json` key: `Settings.cs` has no "override"
  match, and keys such as `ultimaonlinedirectory` (`Settings.cs:58`) and `maps_layouts` (`Settings.cs:98`)
  are unrelated. `maps_layouts` only changes map dimensions (`MapLoader.cs:102-133`).
- **Other mechanisms I looked for and did not find:**
  - a second data path;
  - a "custom map" folder;
  - a `Data\Client` override for maps. `Data\Client` holds `cave.txt`, `lights.txt` and similar, plus MapsCache.
  - `ExternalImages`, which is for gump and art PNGs.
- UltimaLive exists in TazUO (`ClassicUO.Client/Game/UltimaLive.cs`), but pinned ModernUO has no UltimaLive
  code (`grep -rli ultimalive Projects` returns nothing). It would be a server port. Not considered further.

What the launcher would do (sketch, not written): `Play.ps1` generates `app\uo-overrides.txt` at each launch with
absolute paths, for example `map1legacymul.uop=<install>\maps\map1LegacyMUL.uop`, and the same for
`statics1.mul` and `staidx1.mul`. Optionally it also points `map1xlegacymul.uop`, `statics1x.mul` and
`staidx1x.mul` at the same three files, so that turning `NewFeluccaAreas` on later cannot quietly swap EA's
Trammel back in. Then it adds `-uofilesoverride "<path>"` to the existing `Start-Process`
(`player-package/payload/app/Play.ps1:303`). It must also:

- check that the three files exist, with the expected sizes, before launch, because of the silent fallback
  above;
- refuse an install path containing `=` (the split rule).

Cost is about 30 lines of PowerShell.

**Merged-folder alternative (not recommended):** the EA install here is 2,743,994,359 bytes in 517 files (339 at
top level), measured with `du -sb` and `find` on `D:\UO\UltimaOnlineVanilla`.

- **Copies:** about 2.7 GB per player.
- **NTFS hardlinks:** no admin needed, but they must be on the same volume as the EA install, which is often
  `C:\Program Files (x86)` while the package sits in Downloads or elsewhere. Whether a standard user can
  hardlink to read-only files under Program Files is **unverified**. An EA patch that replaces a file breaks
  the link and leaves a stale copy.
- **File symlinks:** need admin or Developer Mode.
- **Junctions:** directory-only, so they cannot mix files.

The override file avoids all of this.

## 3. What ships, sizes, and the effect on downloads

The 7.0.117.0 files in `D:\UO\UltimaOnlineVanilla` (`client.exe` FileVersion `7, 0, 117, 0`). Raw bytes are
measured. "Deflated" is zlib level 6 as a stand-in for .NET `CompressionLevel.Optimal`, computed with Python,
**not** with the build script:

| File | Raw bytes | Deflated |
|---|---:|---:|
| map1LegacyMUL.uop | 89,965,543 | 17,130,517 |
| statics1.mul | 20,393,786 | 6,500,312 |
| staidx1.mul | 5,505,024 | 540,877 |
| **Trammel set** | **115,864,353** | **~24.2 MB** |
| (optional) tiledata.mul | 3,188,736 | 109,591 |
| (not needed) map1xLegacyMUL.uop + statics1x + staidx1x | 115,960,617 | ~24.2 MB |

Package size: the brief says 73 MB. Counted in `player-package/dist`:

- `ShatteredLegacy-2026-09-26.zip` is 76,717,212 bytes (73.2 MiB);
- the current `ShatteredLegacy-2026.09.29.1331.zip` is 79,688,947 bytes (76.0 MiB).

Adding the Trammel set brings the zip to about **104 MB**, and the unpacked install grows by 116 MB.

**Every update re-downloads the whole zip.** `Play.ps1:154-156` downloads `$j.url`, the full package, and there
is no delta. `Update.ps1:195-202` then copies only the files whose length or SHA-256 differ, so on disk an
unchanged map is not rewritten. A one-line script fix still costs every player about 104 MB of download, and
any map change is a full package release.

Further per-update costs if the maps sit under `app\`:

- `Update.ps1:236` backs up **all of `app\`** on every update that changes anything. That is 116 MB more
  copied each time, plus 116 MB unpacked under `%TEMP%\sl-update`.
- Files **outside** `app\` are backed up only when they are replaced (`Update.ps1:237-243`).

**So put the maps at the install root (`maps\`), not under `app\`.**

## 4. Updater rules and build gates that change

Updater (`Update.ps1`):

- **Never-overwrite list:** `Test-Kept` (`Update.ps1:100-111`) protects only these:
  - `app\uo-path.txt`;
  - `app\package-version.txt`;
  - `app\tazuo\settings*.json`;
  - `app\tazuo\Data\...`.

  Map files are not protected, so **a changed map is already replaced on update** by the hash compare at
  `Update.ps1:200-201`. No rule change is needed for that.
- **Retired files:** `retired-files.txt` (10 comment lines, no entries). If a map file is ever dropped, list it.
  `Test-RetiredLine` (`Update.ps1:114-122`, and the copy at `Build-PlayerPackage.ps1:70-78`) already allows
  `maps\...`.
- The updater waits until TazUO is closed (`Update.ps1:172-183`), so open map files are not a problem.
- After an update, the new `Play.ps1` is what starts the game (`Update.ps1:316`). The first launch after an
  update therefore writes the override file. A player who declines an update keeps the old maps and the old
  launcher together, which is consistent.

Build (`Build-PlayerPackage.ps1`):

- The header premise "Nothing of EA's goes in" (`Build-PlayerPackage.ps1:20`) and `notes/player-package.md:252`
  ("would mean shipping EA's files, which the brief rules out") become false. These are edited EA-derived data
  files. This is **a policy change for `docs/`, and Chase's call** (licensing and redistribution).
  `README.txt` wording should follow.
- Gate 3 (TazUO byte-identical, `Build-PlayerPackage.ps1:328-333`) is unaffected if the maps sit outside
  `app\tazuo`. It needs a sibling check that each staged map equals its source.
- Gate 1 scans `.json/.txt/.ini/.xml/.cfg` (`Build-PlayerPackage.ps1:302-305`). The override file is generated
  at launch and is not shipped, so gate 1 is unaffected. It must never ship, because it holds absolute paths
  from Chase's machine.
- Gate 4 (`Test-PackageZip`, `Build-PlayerPackage.ps1:83-147`) should add checks that `maps\` holds exactly the
  expected file names with the expected SHA-256 values (from a manifest), and that `app\Play.ps1` passes
  `-uofilesoverride`.
- New **gate 6, server parity**: see section 5.
- `Setup.ps1:30` (`$minVersion 7.0.114.40`) and `Setup.ps1:33-34` (required files) are unaffected by shipping
  maps. Q-063's floor discussion still applies.

## 5. Server side

How pinned ModernUO finds files:

- `Core.FindDataFile` walks `ServerConfiguration.DataDirectories` and returns the **first directory that has the
  file** (`Projects/Server/Main.cs:180-212`).
- `DataDirectories` is a `HashSet<string>` (`Configuration/ServerSettings.cs:28-29`). With no removals, .NET
  enumerates a HashSet in insertion order, which here is the JSON array order. That is **runtime behaviour,
  not a documented contract**.
- A CUO `settings.json` found in a data dir would also add its `ultimaonlinedirectory`
  (`Configuration/ServerConfiguration.cs:260-266`).

Map selection in `TileMatrix` (`Projects/Server/TileMatrix/TileMatrix.cs:94-141`):

- `map{n}.mul` **first**; `map{n}LegacyMUL.uop` only if no `.mul` (lines 94-113). This is the **opposite**
  precedence to TazUO.
- Then `staidx{n}.mul` (line 121) and `statics{n}.mul` (line 133).
- `x` files are never read by the server.
- Dif patches: land difs are on only below 6.0 and statics difs only below 7.0.9, unless the `maps.*`
  settings say otherwise (`TileMatrix/TileMatrixPatch.cs:57-72`). Off for us, so the server and TazUO agree
  that the difs are ignored.
- Streams are opened at startup with `FileShare.Read` (`TileMatrix.cs:96,105,125,137`). **New map bytes take
  effect only at a server restart.**

How the server gets its data today:

- `docker/uo/.env` has `CLIENT_DATA_PATH=D:/ShatteredLegacy/client-data/classic-client`.
- Live mounts it read-only at `/var/lib/uo/client-data/classic-client` (`docker/uo/docker-compose.yml:27`).
  The test stack mounts **the same folder** (`docker/uo/docker-compose.test.yml:41`).
- Both `modernuo.json` files list only that directory in `dataDirectories` (live and test
  `Configuration*/modernuo.json:5-7`). Neither has `clientData.*` or `maps.*` keys.
- Config is mounted from `${SERVER_PATH}/uo/modernuo/Configuration` (`docker-compose.yml:18`), with
  `SERVER_PATH=D:/ShatteredLegacy/server`. That folder is inside `server\uo`, which the brief called stale, so
  **I read only the `dataDirectories`/`clientData`/`maps` keys of the two `modernuo.json` files and
  `expansion.json:53`**, nothing else there.

The server's data is still 7.0.114.40. Measured hashes (first 16 hex) differ from 7.0.117.0 for:

- `map1LegacyMUL.uop` (76a5bcfb vs 872269bb);
- `statics1.mul` (ebfbba6d vs 2109d96b);
- `staidx1.mul`;
- `facet01.mul`;
- `tiledata.mul` (f5360f51 vs f4486078);
- `hues.mul`;
- `tileart.uop`;
- `map0LegacyMUL.uop`.

The `stadif*1` files are identical. **A 117-based Trammel cannot run on the 114.40 server data without
mixing tiledata versions.** Q-063 (`notes/codex-questions.md:3425`, answered "yes, update") has to land first
or together.

Keeping the server and client identical:

- **Recommended:** one folder is both the server's data and the package's source. Make a full 7.0.117.0 data
  folder for the server (copying 2.7 GB is cheap on the host) and write the edited Trammel files into it in
  place. `Build-PlayerPackage.ps1` takes the three map files *from that folder*.
  - It has no dependency on HashSet ordering.
  - It also settles Q-063's 114 to 117 move.
  - Q-063's test-first plan needs `docker-compose.test.yml` to get its own `CLIENT_DATA_PATH` variable
    (`notes/deploy-readiness.md:355`).
- **Alternative:** an overlay folder (only our 3 files) mounted at its own path and listed **first** in
  `dataDirectories`. It is smaller and keeps EA's base pristine, but it relies on the ordering above and adds
  a mount to both compose files.

**Proposed gate 6, in `Build-PlayerPackage.ps1`**, run before zipping:

- (a) For each shipped map file, its SHA-256 equals the file of the same name in the server's data folder.
  Read the path from `docker\uo\.env`, or from a new `-ServerData` parameter.
- (b) No `map1.mul` exists in any server data folder, because the server would prefer it
  (`TileMatrix.cs:94`) while TazUO reads the UOP.
- (c) The running container started after the map files' last write time (`docker inspect -f
  '{{.State.StartedAt}}' sl-modernuo`), which proves the server has loaded those bytes. If the container is
  down, (c) is a warning, not a failure.

A stronger variant of (c) is a small new customization that logs the SHA-256 of `Core.FindDataFile("map1LegacyMUL.uop")`,
`statics1.mul` and `staidx1.mul` at startup into the bind-mounted `status` folder (`docker-compose.yml:25`).
Gate 6 would compare against that, and the shard console could show it. Cost is about 40 lines of C#, plus a
test.

## 6. Q-063 interaction: a player whose EA install is newer than 117

The base is 7.0.117.0. When EA later patches the player's own folder:

- **Trammel:** pinned by our files. The world draws exactly what the server collides with, apart from the
  tiledata point below.
- **tiledata.mul (collision and height flags) is the real risk.** If EA ever changes flags or height for an
  existing ID, the client predicts movement and draws with the new flags while the server keeps 117. The
  result is rubber-banding or walking "through" a wall, in Trammel too.
  - New static IDs that only newer tiledata has cannot appear in our map, since it is built on 117.
  - A player **older** than 117 (Setup still allows 7.0.114.40, `Setup.ps1:30`) could lack an ID that our
    dungeon uses, if the dungeon uses a 117-only ID. That is unlikely but checkable at build time.

  Shipping `tiledata.mul` and overriding it costs about 0.11 MB in the zip (table above), pins collision
  flags to the server's for every facet, and is the **one extra file I would consider shipping**. The
  override map supports it (`TazUO: ClassicUO.Assets/TileDataLoader.cs:25` reads it through `GetUOFilePath`).
- **Felucca, Ilshenar, Malas, Tokuno, Ter Mur:** still the player's files. Each EA patch reopens the Q-063
  drift for them against the server's 117.

  Shipping them later costs, deflated: Felucca about 24.4 MB, Ilshenar 4.0, Malas 4.3, Tokuno 2.2,
  Ter Mur 3.9, so about 38.7 MB for all five (measured).

  A cheaper first step: `Setup.ps1` or `Play.ps1` warns, and records in the log, when the player's
  `client.exe` is newer than the server's.
- **art, hues, gumps, multis (`MultiCollection.uop`), texmaps:** cosmetic for the client. Multi collision is
  the server's own. A newer `hues.mul` or art only changes looks, and new art IDs beyond our tiledata would
  never be sent by a 117 server. These never need to ship for map reasons.
- **facet01.mul:** the paper or cartography map comes from the player's folder and cannot be overridden
  (`MultiMapLoader.cs:35-40`). It shows EA's Trammel, so the new dungeon will not appear on treasure or paper
  maps. This is cosmetic. Fixing it needs a TazUO code change, about 5 lines to route it through
  `GetUOFilePath`.

## 7. Editors

- **CentrED# (kaczy93), commit `50d23f7a`, edits UOP maps directly, with no conversion.**
  - `Server/Map/ServerLandscape.cs:33` opens the map `ReadWrite, FileShare.None`.
  - `:36-41` sets `IsUop` from the `.uop` extension and reads the UOP table.
  - `:191-196` translates block offsets into the UOP (`CalculateOffsetFromUop`, `:532`).
  - `Server/Packets.cs:128-129` advertises the UOP flag to CentrED+ clients.
  - Statics are always MUL (`ServerLandscape.cs:44-60`).

  So it edits `map1LegacyMUL.uop` in place plus `statics1.mul`/`staidx1.mul`. `statics1.mul` grows as blocks
  are rewritten. Because of `FileShare.None`, **never point it at the folder the live server mounts**: edit a
  working copy and promote it at a restart. I read the code but **did not run it**.
- **UOFiddler** (polserver): PR #179, merged 2026-09-13 per GitHub, adds "a per-profile option for whether
  ... maps are written as mul or uop" and makes map copy and diff work on UOP-only clients. UOFiddler is a
  copy, diff and replace tool, not a statics editor for building a dungeon. The UopPacker plugin and
  LegacyMULConverter convert in both directions if ever needed. These are web sources, not tested here:
  [PR #179](https://github.com/polserver/UOFiddler/pull/179),
  [LegacyMULConverter](https://www.servuo.dev/archive/legacymulconverter-v4-uop-packer-unpacker.147/).
- **If someone converts to MUL anyway:**
  - ModernUO reads `map1.mul` in preference to the UOP (`TileMatrix.cs:94`).
  - TazUO on an EA install reads the UOP and ignores `map1.mul` (`MapLoader.cs:141-143`).

  A converted `map1.mul` left in the server folder would make the server and client disagree silently. Gate
  6(b) exists for this. **Stay on UOP end to end.**

## 8. Recommendation and cost

1. **The client uses TazUO's `-uofilesoverride`. No TazUO change.** Ship `maps\map1LegacyMUL.uop`,
   `maps\statics1.mul` and `maps\staidx1.mul` at the install root, plus optionally `maps\tiledata.mul`.
   `Play.ps1` writes the override file each launch, checks that the files exist with the right sizes, and
   passes the argument. About 30 lines.
2. **One data folder for the server and the package:** a full 7.0.117.0 copy with our Trammel edits in it,
   mounted by both stacks through separate `.env` variables. This is the Q-063 swap and the map ship as one
   scheduled change, after Q-063's test-shard walk and the seeded-coordinate check. Editing happens in
   CentrED# on a working copy, promoted at a restart.
3. **Build changes:** read the maps from that folder; add checks to gate 4; add gate 6 (hash parity, no
   `map1.mul`, the server restarted after the maps changed); rewrite the "nothing of EA's" header and docs.
   About 60-80 lines.
4. **Accepted costs:**
   - the zip grows from 76 to about 104 MB;
   - every update is a full roughly 104 MB download;
   - every map change needs a server restart and a package release together.

   Splitting the maps into a separately versioned download (its own `version.json` entry) would make script-only
   updates small again. That is roughly 100-150 lines across `Play.ps1`, `Update.ps1` and the build. Defer it
   until updates become frequent.

**Unverified:**

- the TazUO DLLs are byte-built from `3212623f`;
- hardlink permissions under Program Files;
- CentrED# behaviour at runtime;
- .NET Optimal compressed sizes, which were estimated with zlib 6;
- whether the 2026-09-06 timestamps on `D:\UO\UltimaOnlineVanilla\map*LegacyMUL.uop` are EA's patch or a local
  edit. The hashes differ from the server's either way.
