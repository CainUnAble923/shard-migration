# cc-P40: custom client research (our TazUO build, our patches over EA's files, one-step install)

2026-10-02. Agent: Claude Code. Brief: `D:\UO\cc-prompts\cc-P40-custom-client-research.md`. Policy:
`notes\client-policy-2026-10-02.md`. **Research only.** Nothing in `D:\ShatteredLegacy` was written, built or committed
(read with `git --no-optional-locks` only); nothing was published or deployed. Scratch: `D:\UO\cc-p40-work\` (TazUO
clones and builds, the patch lab, extracted EA installer pieces). Tools kept beside this note: `notes\cc-P40-tools\`.
EA's files were read in place from `D:\UO\UltimaOnlineVanilla` and copied only into scratch; nothing of EA's was
downloaded except two header-only HTTP requests (section A.1).

**Numbering:** no clash. `cc-prompts\` holds P34, P35, P36, P39, P40, P41, P42; no other P40 note exists.

> **Headlines**
>
> 1. **Everything Chase asked for is possible with stock tools and no hand-patching of EA's files.** The route:
>    EA's own installer (player clicks through it, about 19 MB) whose own patcher then fetches the game (1.77 GB
>    measured on this machine, 10 min); our package then builds **patched copies** of the few EA files we change into
>    `app\uo-overrides\` and starts TazUO with `-uofilesoverride`, exactly as P26 does for tiledata/animdata.
> 2. **EA's "installer" carries no game data at all.** It is a WinRAR SFX around an NSIS 2.38 setup and EA's patcher
>    `UO.exe` (byte-identical to the installed one); every game file comes from `patch.uo.broadsword.com`. Its
>    "7.0.24.0" name is not the version you get: this machine's install is **7.0.117.0** (the floor P36 sets).
> 3. **Measured patch for maps: our own "map ops" text format.** For a synthetic dungeon filling candidate A
>    (4,914 land cells, 1,952 statics) plus an edit at the B1 entrance: **135,854 bytes (22,839 gzipped)**, applied
>    by PowerShell 5.1 in **0.6 to 0.8 s** cold, **3 to 6 ms** when nothing changed. Output map byte-identical to the
>    editor's; statics identical per block. bsdiff is the same size (24,924 bytes) but opaque, and when EA updated
>    the base under it, it **applied silently and corrupted an EA block we never touched**; the ops format reported
>    the drift and the one removal it could no longer make.
> 4. **Our own TazUO build works from source today.** Upstream (BSD 2-Clause) builds with the .NET 10 SDK on this
>    machine in seconds once NuGet is configured; both our shipped commit `3212623f` and upstream `7deed69` build and
>    reach the login screen on EA's 7.0.117.0 data. **Recommendation: build our own exe in a gated pipeline with zero
>    source patches first**, and add patches only for a named need. Nothing found needs a fork yet.
> 5. **Two things for Chase that nobody had seen:** (a) the TazUO we ship sends crash reports to **TazUO's own
>    Discord webhook** (baked in by upstream's CI); a build of ours sends none unless we add our own. (b) Upstream
>    `dev` (not yet in a release marked Latest) adds **loose-file overrides for clilocs, gumps and sounds** and fixes
>    a bug that made **land map patches never apply against ModernUO**.
> 6. **Size of the work:** about **13 units** in five prompts (section D), none of which has to land before the
>    fresh-world wipe except the map-ops pipeline if the dungeon map batch is meant to open with the new world.

---

## A. Getting EA's client with no hand work

### A.1 Where EA's client comes from, and what the player clicks

**The official source:** `https://uo.com/client-download/` links two installers (WebFetch, 2026-10-02):
`https://downloads.eamythic.com/uo/installers/UOClassicSetup_7_0_24_0.exe` (Classic) and `UOEnhancedSetup_4_0_10_1.exe`.
A HEAD request today: **200, Content-Length 18,827,017, Last-Modified 2021-03-26** - the same file and size
`Setup.ps1:36-42` pins (SHA-256 `c19f93f9...`; the copy at `D:\UO\UOClassicSetup_7_0_24_0 (1).exe` hashes to exactly
that). EA's launcher and patch servers are the only other official source (below).

**What the installer is** (read in scratch, `D:\UO\cc-p40-work\ea-installer\`):

| Layer | Evidence |
|---|---|
| WinRAR SFX, RAR archive from offset 99,840 | 7-Zip `l -slt`; PE overlay starts `Rar!`; `WinRAR SFX` string |
| inside: `setup.exe` (NSIS), `data1\UO.exe`, `data1\UO-patch.cfg`, `data1\Uo.cfg`, DirectX redist, `GDF\`, help | 228 files, 22,254,428 bytes unpacked |
| `setup.exe` is **"Mythic UO Installer 1.0.3 (NSIS v2.38)"** | string in its decompressed NSIS header |
| `data1\UO.exe` = the installed `UO.exe`, byte for byte (583,256 bytes) | `cmp` |
| the NSIS script copies `\data1\*.uop`, `\data1\UO.exe`, `\data1\*.cfg`, writes `Software\Electronic Arts\EA Games\` `InstallDir`, `App Paths\UO.exe`, an uninstaller, and shows **a license page with a checkbox** | strings of the decompressed header |
| **no game data:** the archive holds no `.uop` or `.mul` at all | 7-Zip listing |

So the installer only places EA's patcher; **the patcher downloads the game.** Its config in the installer points at
`http://patch.uo.eamythic.com/uopatch-sa/legacyrelease/...`; the installed `UO-patch.cfg` points at
`http://patch.uo.broadsword.com/uopatch-sa/legacyrelease/uo/manifest/` (the patcher updated its own config: it patches
product "EAMythic Patcher" before "UO Classic Client"). The manifest folder answers **403** to a plain GET (expected;
the patcher asks for named files). Plain HTTP, no TLS.

**Measured on this machine** (`D:\UO\UltimaOnlineVanilla\logs\patcher.090626.Log`): installer finished 08:41:22
(`uninstUOClassic.exe` timestamp), the patcher started 08:41:30 by itself, "Patch size is 1765126031", "Patch Operation
Complete" at **08:51:52**. Result: **517 files, 2,743,994,359 bytes**, `client.exe` FileVersion **7, 0, 117, 0**. The
log also says "No usable UI present! Initializing 'headless' patch": the patcher ran without its window here and still
finished.

**What the player has to click:** UAC (the installer writes HKLM), EA's license checkbox, Install, then wait. NSIS
installers accept `/S` (silent) and `/D=<dir>` unless the script blocks them; **not tested** (it would be a second full
EA download), and see decision 1: a silent install would accept EA's license on the player's behalf.

**Version delivered:** whatever EA's patch server serves, 7.0.117.0 today. The installer's own name is irrelevant.

### A.2 How established shards do it

| Shard / launcher | Gets EA's data how | Evidence |
|---|---|---|
| ClassicUO launcher | **does not**: "ClassicUO does not provide any game asset"; the player enters the path to their UO files | [ClassicUO wiki, Installation](https://github.com/ClassicUO/ClassicUO/wiki/Installation); the local `ClassicUOLauncher.exe` has strings for its own update manifest and `github.com/ClassicUO/presets/.../presets.xml`, none for any EA host |
| TazUO launcher (`D:\UO\TazUO\TazUOLauncher.exe`) | does not: downloads TazUO builds and PR builds only | string scan: `DownloadLauncherZip`, `DownloadPRBuild`, no EA host (a string scan, not a source read) |
| Outlands | **ships everything itself**: own launcher, own patch server, about 2.5 GB, ClassicUO and Razor bundled | [uooutlands.com/connecting](https://uooutlands.com/connecting/) |
| UO Forever | own launcher; "Click Install ... wait while the client downloads" | [UO Forever wiki](https://uoforever.com/wiki/index.php/Download_&_Installation) |
| UOAlive (copy at `D:\UO\UOAlive`) | **ships EA's folder**: `UOAlive 7.0.116.0\`, 2.6 GB, plus a ClassicUO launcher | local folder |
| Excelsior (copy at `D:\UO\Excelsior`) | ships a 1.8 GB client folder | local folder |

**None of the six fetches from EA.** The big shards redistribute EA's files (Outlands, UOAlive,
Excelsior, UO Forever), which is exactly what Chase's decision 2 rules out; the launchers leave it to the player.
Our package already does more than any of them by offering EA's installer (`Setup.ps1:127-178`).

### A.3 What our package should do

`Setup.ps1` already does most of it. Changes, in order of value:

1. **Detect** (exists: remembered path, three registry keys, four default folders, `Setup.ps1:61-85`). Add
   `HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\UO.exe` (the installer writes it; string above).
2. **Offer to fetch** (exists, `:127-178`): keep running EA's installer **with its UI**, so the player sees and accepts
   EA's license (decision 1). Then, instead of "let it finish, then double-click again", **wait for the patch**: poll
   `client.exe` FileVersion until it reaches the floor or `UO.exe`/`UO.bin` exits, with a progress line from the
   folder size against about 2.7 GB. That removes the second double-click.
3. **Verify the version** (exists, `:30`, `:54-57`); P36 moves the floor to 7.0.117.0.
4. **Keep EA's launcher able to patch:** we already never write into EA's folder (P26: copies in
   `app\uo-overrides\`), so EA's patcher sees untouched files and its own `mft.myp`/`patch.myp` stay valid. Keep it
   that way; the map ops (B.2) follow the same rule. When EA patches, the stamps (P26's and B.2's) see the new size or
   time and rebuild on the next start.
5. **Do not** reimplement EA's patch protocol against `patch.uo.broadsword.com`: undocumented, plain HTTP, and EA's
   own `UO.exe` already does it.

---

## B. Our patches over EA's files

### B.1 Per file type: format, change size, and how TazUO can take it

All TazUO facts are at our shipped commit `3212623f` (clone `D:\UO\cc-p40-work\tazuo-3212623f`), paths under `src\`.
Every EA file below is opened through `UOFileManager.GetUOFilePath` (`ClassicUO.Assets/UOFileManager.cs:103-108`), so
**`-uofilesoverride` can point any of them at a copy of ours**; the **87 call sites** (counted:
`grep -rn "GetUOFilePath(" src --include=*.cs`, minus the definition) cover the loaders for anim, animdata, art, cliloc, fonts, gumps, hues, light, maps, statics, multi,
sounds, skills, speech, texmaps, defs).

| File (EA, this install) | Format (measured) | Typical change of ours | Load ours without touching EA's file? | Route |
|---|---|---|---|---|
| `artLegacyMUL.uop` 156 MB, 43,760 entries, uncompressed | UOP | new or replaced **item** art | **yes**: PNG in `ExternalImages\art\<id>.png` (`ExternalImageLoader.cs:299-313`), or in `tuoassets.zip` (`:447-457`) | P26, done |
| same file, **land** art (IDs below 0x4000) | | a new floor/ground tile | **no**: ExternalImages keys art as `id + 0x4000` only (`:311`) | rebuild a copy of the UOP, or a fork patch (C.3) |
| `texmaps.mul` 47 MB | MUL+idx | stretched land texture | no loose override found | records into a copy (as tiledata) |
| `gumpartLegacyMUL.uop` 81 MB, 5,579 entries, flag 3 (zlib+BWT) | UOP | new gump art | **yes**: `ExternalImages\gumps\<id>.png` (`:280-292`) | PNG, like art |
| `tiledata.mul` 3,188,736 | fixed records | flags, height, name | records into a copy | P26, done |
| `animdata.mul` 4,486,748 | fixed records | frames | records into a copy | P26, done |
| `map1LegacyMUL.uop` 89,965,543, 113 entries, **uncompressed** (flag 0) | 196-byte blocks, 4,096 per entry | the dungeon: 4,914 cells in my test | copy + in-place writes | **map ops, B.2 (measured)** |
| `statics1.mul` 20,393,786 + `staidx1.mul` 5,505,024 | 7-byte records, 12-byte index | 1,952 added, 3 removed in my test | copy, append our blocks, repoint index | **map ops, B.2 (measured)** |
| `mapdif*/stadif*` overlays | MUL | | **no, on a UOP install**: TazUO opens the dif files only in the `.mul` branch (`MapLoader.cs:159-187`), never when `map{i}LegacyMUL.uop` exists (`:141-157`) | not usable without a fork patch; also ModernUO turns them off for 7.x clients (`TileMatrixPatch.cs:61-69`) |
| `hues.mul` 265,500 = 375 groups x 708 bytes | fixed records | a new hue | copy + records | records, like tiledata |
| `radarcol.mul` 163,768 | fixed u16 per ID | minimap colour for new land/art | copy + records | records |
| `MultiCollection.uop` 568,698, 873 entries, flag 1 (zlib) | UOP | a new house or ship shape | no loose override; TazUO uses the UOP first (`MultiLoader.cs:25-33`) | rebuild a copy with our entries added (zlib), whole-file |
| `Cliloc.enu` 5,078,062, BWT-compressed (byte 3 = 0x8E), **124,000 entries, highest 3,011,032** (P29 reader) | | a few dozen strings | copy: TazUO reads an **uncompressed** cliloc too (`ClilocLoader.cs:123`). Rebuild measured: 5,062,977 bytes uncompressed, 0.04 s to write (Python decode 1.9 s). Upstream dev reads `Clilocs.txt` (A.5 below) | records into a copy now; `Clilocs.txt` once dev lands |
| `soundLegacyMUL.uop` 168 MB | UOP | a new sound | **yes**: `SoundOverrides\<id>.mp3` beside the exe (`SoundOverrideLoader.cs`, at `3212623f`) | loose file |
| `AnimationFrame*.uop`, `anim*.mul`, `Body.def`, `mobtypes.txt` | | a new creature body | no loose override found | not needed for any queued feature; leave until one asks |

**The server needs some of these too.** ModernUO reads tiledata, maps, statics and multis from `CLIENT_DATA_PATH`
(`Server/TileMatrix/TileMatrix.cs:105-152`: `map{n}.mul` first, else `map{n}LegacyMUL.uop`; `statics{n}.mul`,
`staidx{n}.mul`). P26 solved tiledata in memory. **Map edits cannot be done in memory cheaply**: the server must load
patched copies too, built by the same ops file at deploy time into a data folder of its own. Today live and test
share one `CLIENT_DATA_PATH` (P26 5.2; P36 adds `CLIENT_DATA_PATH_TEST`), so the ops must reach the test shard's data
first. Gumps, cliloc, art PNGs, sounds and hues are client-only.

### B.2 Patch format: measured on a real change

**Lab:** `D:\UO\cc-p40-work\patch-lab\` (tools copied to `notes\cc-P40-tools\`). `make_edit.py` simulates an editor's
output on scratch copies of EA's Trammel files: rooms and corridors in **candidate A (5136-5247 x 1128-1263)**, which
today is **238 blocks of land 580 (0x244) at z 0 with zero statics** (read from EA's file), plus the B1 entrance block
(3619,2620): 3 EA statics removed, 4 added. The statics file is rewritten compacted, as editors save.

**Three formats compared:**

| | Whole-file rebuild (P26 style, records) | **Map ops (ours, text)** | bsdiff (bsdiff4 1.2.6) |
|---|---|---|---|
| what ships | our records | one line per changed cell / static: `L x y tile z`, `S+ x y z id hue`, `S- x y z id hue`, plus `B <block> <fingerprint>` | opaque binary diff |
| size, this change | n/a for maps (blocks would carry EA's neighbouring cells) | **135,854 bytes, 22,839 gzipped**; 4,914 L, 1,952 S+, 3 S-; 185 blocks | **24,924 bytes** (map 4,301; statics 3,972; staidx 16,651) |
| make time | | 2.3 s (`diff_ops.py`) | **23.9 s** (19.5 on the map) |
| apply time | | **PowerShell 5.1, new process: 580-820 ms rebuild, 1.4 s whole process; skip 3-6 ms** (281 ms when the C# is compiled before the stamp check: put the check first) | 0.33 s (Python) |
| result | | map **byte-identical** to the editor's; statics: 458,574 blocks identical, **178 the same statics in another order, 0 different** | identical |
| auditable: "no EA bytes"? | yes | **yes**: every line is a change we made; fingerprints are hashes | no; cannot be read |
| EA updated the base (simulated: a Britain cell, a static added in Britain shifting the file, a cell and a static removed in our entrance block) | | applied; **reported "EA changed block 231751" and "static to remove is not in EA's block ... skipped"**; all of EA's changes kept | **applied without complaint and corrupted block 231750, an EA block we never touched** (gained one of the entrance block's statics, lost one of its own) and the entrance block |

**Recommendation: map ops for maps and statics; records (P26) for fixed-record files (tiledata, animdata, hues,
radarcol, cliloc); loose files where TazUO has them (art, gumps, sounds).** No bsdiff anywhere.

Notes from the run:
- The applier copies `map1LegacyMUL.uop` (90 MB), `statics1.mul` and `staidx1.mul` into `uo-overrides` (about 116 MB
  more on disk) and finds the map's blocks by hashing the UOP entry names (Jenkins `hashlittle2`, implemented in the
  inline C# of `Apply-MapOps.ps1`). EA's map entries are uncompressed, so no decompression is needed.
- Statics: EA's file kept as is, our blocks appended, their index entries repointed (output 20,407,548 bytes).
- Order of statics within a block: ours come after EA's; the editor's order differs in 178 blocks. Ties on the same
  cell and z may draw in another order. Not seen in a client.
- A static the patch removes is matched exactly (id, x, y, z, hue). If EA moved it, ours stays, which is the safe
  side; the applier says so in one yellow line.

### B.3 Authoring tooling and the "no EA bytes" gate

1. **Edit** in CentrED+ (map) or UOFiddler (art, hues, multis) against a **scratch copy** of EA's files at a pinned EA
   version (record the 3 files' SHA-256 beside the ops). For new art, P26's pipeline already exists.
2. **Diff** the edited copy against the pinned base with `diff_ops.py` (generalise to all facets) into
   `player-package\vendor\shattered-legacy-map\<facet>.mapops`. Commit the ops, never the edited files.
3. **Round-trip gate** (in the build): apply the ops to the pinned base and compare with the edited copy (map
   byte-identical, statics equal per block as multisets), as measured above. Fails the build on any difference.
4. **Content gate** (extend P26's gate 4): ops files must parse line by line as the schema; every `L` line must
   differ from the base cell; every `S-` must exist in the base; no `S+` duplicates a base static on the same cell.
   That makes "every line is a change of ours" a checked fact, not a promise.
5. **Server side:** the same applier (or a C# twin in `server\`) builds the server's copies at deploy, and a
   cross-check fact compares the server's map with the client's for the touched blocks (as P26's records fact does).

---

## C. Our own TazUO build

### C.1 License

`LICENSE.md` upstream = `player-package\LICENSE-TazUO.txt`: **BSD 2-Clause, "Copyright (c) 2025, andreakarasho"**,
unchanged since `2e1dc77e7` (2025-02-03) and identical at `3212623f` (diffed). A distributed fork must **reproduce the
notice, conditions and disclaimer in its documentation**; we already ship that file. Nothing else: no source offer,
no naming rule, changes may stay private.

**Bundled third-party code** (submodules and `external\`), which travels in the same zip:
FNA (Ms-PL, `external/FNA/licenses/LICENSE`), FontStashSharp (zlib), Myra and XNAssets and FileEmbed (MIT), **MP3Sharp
(LGPL-3.0, `external/MP3Sharp/license.txt`)**, plus prebuilt native DLLs in `external\x64\` (FAudio, FNA3D, SDL3, zlib,
libtheorafile; byte-identical to the ones we ship today). **Our package ships none of their license texts today.**
This is true already, fork or not. MP3Sharp is a separate `MP3Sharp.dll`, which is the LGPL-friendly form; it still
wants its license text and a pointer to its source in the package.

### C.2 Keeping a build current with upstream

**Measured** (scratch, `D:\UO\cc-p40-work\`):
- Clone with submodules; `dotnet publish src/ClassicUO.Client/ClassicUO.Client.csproj -c Release -r win-x64` with .NET
  SDK 10.0.201. **It failed until a `nuget.config` naming nuget.org was added** (this machine has no NuGet source;
  NU1101). Then it builds in seconds (12-14 s here with warm caches).
- The build **modifies two tracked files** (`LegionScripting/docs/API.py`, `LegionAPI.md`, by its `GenerateDocs`
  target, `ClassicUO.Client.csproj:105-108`). A gated pipeline must expect that or the tree looks dirty.
- Our build of `3212623f` vs the shipped client: 760 files against 768; **555 of 759 shared files the same size**; the
  rest differ because the shipped one was published with a newer .NET 10 runtime (`mscordaccore ... 10.0.1226` vs
  mine `10.0.526`) and upstream CI stamps versions. **Pin the SDK with `global.json`** in our pipeline.
- Upstream CI stamps the version (`.github/workflows/tuo-deploy.yml`: `yy.MMdd.run`), writes `v.txt`, and **injects
  `CRASH_WEBHOOK` into `CrashReporter.cs`**. Ours shows `TazUO - 5.31.2.0` in the title and has no webhook.
- **Smoke test:** both builds (`3212623f` and `7deed69`) started with a settings file pointing at
  `D:\UO\UltimaOnlineVanilla` and 127.0.0.1:1, **still running at 20 s, window "TazUO - 5.31.2.0", 740-827 MB**
  (the data loaded). Not logged in.

**Pipeline, mirroring `build.sh` and `server\patches\`:**
`client\` in `D:\ShatteredLegacy` holding: `TAZUO_COMMIT` (pinned SHA), `patches\*.patch` (applied with `git apply`
at zero fuzz, like `apply-patches.sh` after F2), `nuget.config`, `global.json`, `build-client.sh` (clone at the pin,
submodules, apply patches, publish, stamp `v.txt` as `<upstream version>-sl.<n>`, gate: the patch set applies cleanly,
the exe starts and reaches the login screen as in my smoke test, the package's gates pass). The exe goes into the
player package as `app\tazuo\` does today; `Build-PlayerPackage.ps1 -TazUO` already takes the folder.

### C.3 What a fork would add, and what we already have without one

**Already possible without a fork:** item art and gumps as PNG (ExternalImages), sounds (`SoundOverrides\`), any EA
file replaced by our copy (`-uofilesoverride`), Legion scripts, server gumps for any UI the server drives, and a
launcher in PowerShell. (Plugins: the modern .NET builds "do not support plugins", per upstream's own release text in
`tuo-deploy.yml`, and our launcher already empties `plugins`, `Launch-Settings.ps1:70-71`.)

**Only a source patch can give us:**
| Need | Size of patch | Needed now? |
|---|---|---|
| map dif overlays on a UOP install (`MapLoader.cs:159-187`) | about 10 lines | **no**: map ops do the job with stock TazUO |
| land art as PNG (`ExternalImageLoader.cs:311`) | small | not until someone draws a new ground tile |
| crash reports to us instead of nowhere | CI secret, no code | decision 3 |
| our name/icon/version in the title, a default server list | small | cosmetic |
| client-side UI of our own (new panels beyond server gumps) | open-ended | nothing queued asks for it |

**Recommendation: our own build at a pinned upstream release, with zero patches**, so "our build of TazUO" is true
from the first package and every later patch has a pipeline to land in. Do not fork the repository; keep patches.

### C.4 What changed upstream since our build (26.0909.63, `3212623f`)

- `main` = release **v26.0923.64** (marked Latest, `7deed693c`): **19 commits** since ours, all client features and
  crash fixes (list: `git log 3212623f..7deed69`; e.g. #1074 "Only support managed zlib", #1078 guard JSON saves,
  #1090 crash fixes).
- `dev` = **v26.1002.2034** (pre-release "TazUO-BleedingEdge", `6766d21fa`, today): **39 commits** since ours, 127
  files. For us the one that matters is **#1107 "Upstream prs from CUO" (`2c59d5087`, 2026-09-28)**:
  - `Clilocs.txt` read after `Cliloc.enu`, last write wins, through `GetUOFilePath` (so overridable): **our strings
    with no cliloc rebuild at all**;
  - loose gumps `Gumps\<id>.gump` in the **UO folder** (`FileManager.BasePath`, not the exe folder: we would not use it,
    we never write there; ExternalImages already covers gumps);
  - loose sounds `Sounds\<id>.wav`;
  - **the map-patch packet fix:** clients read land and statics counts in the wrong order, so "land patching against
    every server that sends this packet" never applied (its own comment, `MapLoader.cs`). Irrelevant while we use
    map ops; it would matter if we ever used dif overlays.
- `LICENSE.md` unchanged.

---

## D. Plan

Units as in cc-P30 section 7 (one unit about one focused builder session).

| Prompt | Kind | Content | Units | Gate / proof |
|---|---|---|---|---|
| **P-a client pipeline** | builder | `client\` in the shard repo: pin `7deed693c` (v26.0923.64) or keep `3212623f` (decision 4); `nuget.config`, `global.json`, `build-client.sh`; version `-sl.N`; package uses our exe; third-party license texts into the package; crash webhook per decision 3 | 3 | builds from a clean clone; smoke start; package gates green; a patch that does not apply fails the build (red first) |
| **P-b one-step install** | builder | `Setup.ps1`: App Paths key; run EA's installer with its UI, then wait for the patcher and show progress instead of asking for a second start; keep the hash pin | 2 | P35's clean-machine test (it exists for this) |
| **P-c map ops** | builder | `Apply-MapOps.ps1` hardened (stamp before C#, all facets, ASCII, yellow-line failures like `Build-UoOverrides.ps1`), called from `Play.ps1`; `diff_ops.py` into `scripts\`; round-trip and content gates in `Build-PlayerPackage.ps1`; server-side copies for the test shard's own data folder; cross-check fact | 4 | red-run like P26: mutate an op, a fingerprint, the stamp; simulated EA update (B.2) in the tests |
| **P-d records for hues, radarcol, cliloc** | builder | generalise `Build-UoOverrides.ps1` records to these files (cliloc: write uncompressed, keep raw bytes, no `replace` decoding) | 2 | as P26's 8 facts |
| docs | Claude | `docs\` package policy line (client policy, this note), deviation text if any | 1 | |
| P36 / map batch | unchanged | P36 (region, rules, client floor) needs none of this. **The dungeon's map batch needs P-c first**; F-21 to F-23 need nothing new (PNGs and records exist; F-23 gumps need registry rows only) | | |

About **12 to 13 units**. Order: **P-a and P-c can run in parallel** (different folders); P-b any time before P35;
P-d when the first hue or string is wanted. Against P36: P36 first (it is written and touches `Setup.ps1:30`), then
P-b on top of it. Against F-21 to F-23: independent.

**Before the fresh-world wipe:** nothing here is required by the wipe itself. Map ops change only map and statics,
which no save holds, so they can land before or after. If the dungeon is meant to open with the new world, P-c and
the map batch must land before it. The client pipeline (P-a) can land any time; it changes no game data.

---

## Not verified

- **EA's installer silently** (`/S`, `/D=`): NSIS 2.38 normally honours both; not run (a second 1.77 GB download, and
  decision 1). Whether the patcher can be started headless on purpose (here it went headless because
  `patchui.dll` could not be copied, per its log) is not known.
- **Anything in a logged-in client:** the patched map drawn, walking, statics draw order on tied cells, our TazUO build
  playing a session. Both builds only reached the login screen.
- The applier against facets other than 1, against a map whose UOP entries are compressed (EA's are not today), and
  on a path with non-ASCII characters.
- How EA's patcher reacts to a file it did not write in its folder: we never put one there, so not tested.
- Whether upstream dev's `Clilocs.txt` works in our launcher setup (read, not run).
- MultiCollection.uop rebuild and texmaps: described from the format, not measured.
- Outlands, UO Forever: from their pages (WebFetch summaries), not from their launchers.

## Decisions for Chase

1. **EA's license.** EA's installer shows a license with a checkbox; among its terms: "You will not create, use or
   provide any server emulator" and not "play Ultima Online on any service that is not controlled or authorized by
   Electronic Arts" (installer text). **Recommended: the player runs EA's installer with its UI and ticks it
   themselves; our package never installs silently.** Your call if you want it otherwise.
2. **Patch format:** map ops for maps/statics, records for fixed-record files, loose files where TazUO has them; no
   bsdiff. (Recommended.)
3. **Crash reports:** today's shipped TazUO sends crash text (exception, OS, version) to **TazUO's Discord webhook**.
   Our build: none, or our own webhook, or keep upstream's (needs their secret, so not really possible).
4. **Which upstream to pin:** `main` v26.0923.64 (stable, 19 commits on ours, recommended), or `dev` v26.1002.2034
   (adds `Clilocs.txt` and the map-patch fix, but marked bleeding edge).
5. **Fork size:** zero patches now (recommended), patches only for a named need (land art, dif overlays).
6. **Disk:** map ops add about 116 MB of copies in `app\uo-overrides\` per edited facet. Acceptable?
7. **Server data per shard:** map edits need the test shard's own patched data folder (P36 starts
   `CLIENT_DATA_PATH_TEST`). Confirm the test shard gets map edits first and live only at go-live.
8. **Third-party license texts** (FNA Ms-PL, MP3Sharp LGPL-3.0, MIT, zlib) are missing from the package today. Add them
   in P-a? (Recommended; it costs nothing.)

## Files

```
notes\cc-P40-tools\uolib.py           UOP reader (hashlittle2), map block offsets, statics reader
notes\cc-P40-tools\make_edit.py       simulated editor output (scratch copies only)
notes\cc-P40-tools\diff_ops.py        base vs edited -> trammel.mapops
notes\cc-P40-tools\Apply-MapOps.ps1   the player-side applier prototype (PowerShell 5.1 + inline C#)
notes\cc-P40-tools\cmp.py             compares a TazUO build folder with the shipped client
```

Scratch (not committed, safe to delete): `D:\UO\cc-p40-work\` (tazuo clone + `3212623f` worktree, two builds, the EA
installer pieces, the patch lab with its 116 MB outputs and bsdiff files).
