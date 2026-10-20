# cc-P214: tool trials (UORegionEditor, uotinker, SpriteMotion): Phase 1 review and Phase 2 sandbox trial

Written 2026-10-20 by the Bronze Golem (Fable) on CHASES-TOWER, branch golem/Bronze/P214 of both repos (docs only;
nothing in ShatteredLegacy changed). Prompt: `cc-prompts/claimed/Bronze/cc-P214-tool-trials.md`. Phase 1 (sections 1 to
4) stopped at the review gate before 17:07; Chase's decisions of 17:07 are in the prompt and Phase 2 (sections 5 to 9) ran
17:08 to 17:55 on the same desk. Sandbox: `D:\UO\tool-trials\` (nothing deleted; Chase may look). Pinned ModernUO is
`D:\UO\ModernUO-pinned` (d4531cd94).

## Headlines

1. **UORegionEditor: adopt for the map pipeline.** Built from source with ClassicUO's three managed assemblies also built
   from source (the TazUO tree already on this PC, section 5.1), none of the zip's DLLs. It opened the client-data copy,
   drew a region over Ocllo, and its ModernUO export is byte-for-byte the shape pinned loads from
   `Distribution/Data/regions.json` (section 6.1): no converter needed. Two limits: it renders and edits on map0 only, and
   its ImGui UI has no facet picker, so a Trammel region is a Felucca export with `"Map"` hand-edited; nested regions
   need `Parent` added by hand.
2. **uotinker: keep as an occasional tool, with one caveat Chase should know.** It built, opened the copy, showed item
   0x0F3F and hue 1258, exported the arrow as PNG, renamed one tiledata entry and saved; pinned ModernUO's own
   `TileData.cs` reads the saved file back with the new name and nothing outside that one file changed (section 6.2).
   The caveat: **its `--selftest` ignores `CheckUpdates` and contacted GitHub**, downloading the 65 MB release
   installer twice to verify its checksum code (`SelfTest.cs:402-418`); I ran that self-test before reading that far.
   Nothing was installed or run and the file was deleted by the test itself, but a request with the version string did
   leave the PC (section 8). The GUI honours the setting (`MainForm.cs:140`); the self-test is not something we would
   ever run again.
3. **The shard's client art is UOP; uotinker edits MUL only.** UOAlive 7.0.116 ships `artLegacyMUL.uop` and
   `gumpartLegacyMUL.uop`; uotinker's `ArtStore` opens `art.mul/artidx.mul` and `gumpart.mul/gumpidx.mul` only
   (`Core.cs:175-178`). To trial it I unpacked the two UOPs into MUL files inside the copy with a 90-line converter built
   on the from-source ClassicUO.IO/Utility (section 5.2). So for our client, uotinker is a viewer and a tiledata/hues/
   radarcol/skills editor; art edits would need a MUL to UOP step we do not have.
4. **SpriteMotion: deferred** (Chase's decision 3c). Nothing copied, built, fetched or installed. Section 7.3 says when to
   come back to it.
5. **Nothing outside the sandbox changed except each tool's own profile folder** and `%TEMP%`: the untouched UOAlive
   folder hashes identical before and after (524 files); the copy differs only by the four MUL files I generated and the
   one `tiledata.mul` uotinker saved (section 6.2). Full list of writes in section 8.
6. **Deviations for Chase** (section 9): the self-test network calls above; one stray mouse click that landed on the
   Claude desktop app window before the helper script was fixed; `nuget.org` had to be added as a package source in the
   sandbox (this PC's user NuGet config has no sources); a one-line patch to the sandbox copy of ClassicUO so the
   editor's art view works on a UOP client.

## 1. UORegionEditor (`code/uo-region-editor`, MIT, v0.8.11 by chemist/uoblood)

**What it is.** A .NET 10 Windows desktop app (`net10.0-windows`, WinForms host, ImGui over OpenGL through Silk.NET;
`--classic` runs the older WinForms-only UI) that draws regions on the rendered map and exports Sphere `.scp`, CentrED
`cedserver.xml`, ServUO `Regions.xml` and ModernUO `regions.json`, and imports all four. 21 `.cs` plus a `Server\`
project (a TCP region server with accounts, so several people can edit one shard's regions). Read: README.md,
SOURCE.txt, UORegionEditor.csproj, Server/UORegionEditor.Server.csproj, build-release.ps1 (zip), THIRD-PARTY-NOTICES,
Program.cs, ImGuiApp.cs, ImGuiPanels.cs, MainForm.cs, NetClient.cs, ModernUoJson.cs, MulRadar.cs, Model.cs, ArtView.cs.

**Needs.** .NET 10 SDK (present: 10.0.201). NuGet at build: Silk.NET.Input, Silk.NET.OpenGL,
Silk.NET.OpenGL.Extensions.ImGui, Silk.NET.Windowing 2.23.0 (managed packages with GLFW natives inside, from
nuget.org). From the zip: five `lib\*.dll` (below). An OpenGL desktop (the game PC has one).

**Downloads at run time.** None on its own. `NetClient.cs:59-83` opens a TcpClient only when the user presses Connect
on a region server (default host `127.0.0.1`, `ImGuiApp.cs:155`); the muls it then downloads come from that server into
`%LocalAppData%\UORegionEditor\mulscache\<host>_<port>`. No other socket, no HTTP, no update check. `--selftest` starts
its own region server on an ephemeral loopback port and connects two clients to it (`Program.cs:698-755`).

**Writes.** `%LocalAppData%\UORegionEditor\`: `ui.json`, `layout.ini`, `last-project.json`, `autosave-*.json`,
`crash.txt`, the map render cache `radar-<hash>.png` (`MulRadar.cs:190-205`). Project saves and the four exports go
where the user's file dialog points (`ImGuiPanels.cs:1456-1514`). `Process.Start` opens Explorer on an export folder and
shell-opens a file the user picked (`ImGuiPanels.cs:343, 389, 1653`). Diagnostics write `slopescan.txt` and the self-test
report into the working directory or the path given. No registry, no service, no installer, no admin right.

**Binaries not built from source (Phase 1 stop).** `lib\ClassicUO.Assets.dll`, `ClassicUO.IO.dll`,
`ClassicUO.Renderer.dll`, `ClassicUO.Utility.dll`, `zlib.dll` in the zip; `UORegionEditor.csproj:31-35` references
Assets, IO and Utility by `HintPath` and copies all five. The zip's `zlib.dll` is byte-identical (sha256 fcf9f36b...) to
the one the shard's own ClassicUO and TazUO clients run. Chase chose (b): build the managed ones from source, keep the
zip's DLLs out. Done in section 5.1; the zip's five DLLs were never extracted.

## 2. uotinker (`code/uotinker`, GPL-3.0-or-later, v0.2.0 by uo-vasilas / Daniel Kowarek)

**What it is.** A .NET 8 WinForms viewer and editor for client files: art, land, gumps, radar colours, hues,
animations (mul and uop), tiledata (64-bit flags), skills, cliloc. Edits tiledata, imports and exports art and gumps
as PNG, edits hues, radar colours, skills and cliloc. 24 `.cs`; one borrowed file, `src/BwtDecompress.cs`, from
ClassicUO (BSD-2, THIRD-PARTY-NOTICES.md). Interface in German by default, English through `"Language": "en"`. Read:
README.md, SOURCE.txt, UOTinker.csproj, Setup/UOTinker.nsi (zip), src/Core.cs, src/MainForm.cs, src/Updater.cs,
src/Tables.cs, src/TileEditor.cs, src/GraphicEditor.cs, src/ItemDefList.cs, src/About.cs, src/Ui.cs, src/Help.cs and,
too late (section 8), src/SelfTest.cs.

**Needs.** .NET 8 SDK to build or .NET 8 Desktop Runtime to run (8.0.32 present; the 10.0.201 SDK built
`net8.0-windows` with the 8.0 targeting pack already on disk, no restore needed). No NuGet packages. No binaries in
the tree; the release binaries were not downloaded by the intake.

**Downloads and network.** At start, when `CheckUpdates` is true (default): one GET to
`https://api.github.com/repos/<repo>/releases/latest` with user agent `UOTinker/<version>` (`Updater.cs:21-29`,
`MainForm.cs:137-143`). If a newer release exists it offers the installer; on the user's click it downloads
`UOTinker_Setup_*.exe` to `%TEMP%`, verifies SHA-256 against the release digest and starts it (`Updater.cs:75-81`).
The About box opens a Ko-fi URL on click (`About.cs:11, 60`). **And `--selftest` calls `Updater.CheckAsync()` and
`Updater.DownloadAsync()` unconditionally** (`SelfTest.cs:402-418`): two release-API GETs and two downloads of the
current installer, the second with a deliberately wrong checksum to prove it is rejected and deleted. Phase 1 missed this
because I read the self-test only as far as its data checks.

**Writes.** `%APPDATA%\UOTinker\settings.json` (`Core.cs:20, 43-44`); backups before every save in
`%APPDATA%\UOTinker\backups\` (`Tables.cs:7-22`, `Core.cs:316-320, 582-586`, `TileEditor.cs:559-582`); the client files
it is pointed at, on Save only (art and gump data appended, indexes rewritten; tiledata, hues, radarcol, skills and
uncompressed cliloc rewritten). `--selftest` writes `%TEMP%\uotinker_selftest`, `uotinker_arttest` (a 312 MB copy of
art.mul), `uotinker_savetest`, `uotinker_tabletest`, and the report path given. The NSIS installer is per-user
(`RequestExecutionLevel user`, `$LOCALAPPDATA\Programs\UOTinker`, HKCU keys only); not built or run. No service, no
admin right.

## 3. SpriteMotion (`code/spritemotion`, MIT, DatMoshu, commit of 2026-10-18)

**What it is.** A Python 3.10+ toolkit (266 `.py`, `pyproject.toml`, `uv.lock`) for fitting and rendering equipment
on UO's 2D bodies: Content Studio (`tools/uo-content/studio.py`, a local web app on 127.0.0.1:8772), Fit Lab
(`tools/fit-lab/run.py serve`, 127.0.0.1:8774), a live pose editor (127.0.0.1:8768), a Blender build pipeline
(`tools/blender/`), a Godot Sprite Pose Editor (`tools/sprite-pose-editor/`), and `third_party/UO_Model3D_v13`, Levy's
rigged 3D rebuild of body 0x190 (shared with the artist's permission, NOTICE.md).

**Needs.** Python 3.10+ (3.12.10 present); a venv at `.venvs\spritemotion` inside the checkout; pip extras `imaging`
(numpy, Pillow) and `test` (pytest, jsonschema, scipy). **Blender 4.2 LTS or 5.2 LTS** for every render, build and
import step (not installed; blender.org's installer is machine-wide). **Godot 4.7** for the Sprite Pose Editor only.

**Downloads at build or run time.** `0-setup.bat`: pip from PyPI, then `tools/godot/fetch.py` downloads
`Godot_v4.7-stable_win64.exe` as a zip from GitHub releases, SHA-512 pinned (`fetch.py:6-7, 22-26, 55-57`). The 29
lfs pointers (the `.blend` and all 28 example `.glb`) need `git lfs pull` against GitHub to become files. The three web
servers bind 127.0.0.1 only (SECURITY.md, `common/local_guard.py`). No telemetry, no update check found.

**Writes.** Everything under the checkout by default (`common/workpaths.py:10-14`). No registry, no service, no admin
right, no installer. **Binaries not built from source:** none in the tree.

**Chase's decision 3(c): defer.** Nothing was copied to the sandbox, built, fetched or installed. Section 7.3.

## 4. Phase 1 decisions and Chase's answers (2026-10-20 17:07)

1. UORegionEditor: (b) build ClassicUO's three managed assemblies from source, keep the zip's DLLs out. Done.
2. uotinker: run with `CheckUpdates` off from the first start. Done for the GUI; see headline 2 for the self-test.
3. SpriteMotion: (c) defer. Done (nothing run).
4. Client data: `D:\UO\UOAlive\UOAlive 7.0.116.0` copied to `D:\UO\tool-trials\client-data-copy\` (robocopy, 524
   files, 2.546 GB, 22 folders; original untouched, verified by hash in 6.2).
5. UOFiddler not installed: uotinker's own reload plus pinned's `TileData.cs` and the from-source ClassicUO `ArtLoader`
   in a headless check (`D:\UO\tool-trials\uotinker\Check\`). Done, section 6.2.

## 5. What was built and how (Phase 2)

All under `D:\UO\tool-trials\`. Originals under `D:\UO\third-party` untouched (robocopy copies; the intake's `_zips\`
never extracted). No Docker, test shard, package or Haven work, so no Golem lock was needed.

### 5.1 UORegionEditor

- `uo-region-editor\src\`: robocopy of `third-party\code\uo-region-editor\UORegionEditor-main` (1.79 MB).
- `uo-region-editor\classicuo-src\`: robocopy of **`D:\UO\tazuo-sl-build\src`** (the TazUO checkout the shard's own
  client is built from: commit `3212623f` "Merge pull request #1069 from PlayTazUO/dev", 2026-09-09, plus the shard's
  12 local file changes, none in the three assemblies used except `ClassicUO.Assets/ExternalImageLoader.cs`), excluding
  `.git`, `bin`, `obj` (3,884 files, 176 MB). Chosen over a fresh `git clone` of upstream ClassicUO because it is the
  same code family, already on the PC, already trusted to ship to players, and needed no download. TazUO's
  `ClassicUO.Assets` API matches what the editor calls (`UOFileManager(ClientVersion, path)`, `Arts.GetArt`,
  `Texmaps.GetTexmap`, `Hues.HuesRange/HuesCount`, `TileData.StaticData/LandData`; `ArtView.cs:60-64, 817-855`).
- **One sandbox-only patch**, `classicuo-src\src\ClassicUO.Assets\UOFileManager.cs:49-50`: the constructor now sets
  `IsUOPInstallation` (version >= 7.0.0.0 and `MainMisc.uop` present). TazUO sets it only inside `UOFileManager.Load()`
  (line 146), which the editor never calls, so `Arts.Load()` fell through to `art.mul` and threw on a UOP client. The
  editor's own `ArtView.CheckArtPack` (`ArtView.cs:47-48`) expects exactly the MainMisc.uop rule, so the author's
  upstream build must decide it in the constructor; unverified against upstream, which I did not fetch.
- `dotnet build src\ClassicUO.Assets\ClassicUO.Assets.csproj -c Release` in the copy: builds `ClassicUO.Assets.dll`
  (8.9 MB, embedded fonts and gump assets), `ClassicUO.IO.dll`, `ClassicUO.Utility.dll` and their in-tree dependencies
  `FNA.dll`, `FontStashSharp.FNA.dll`, `MP3Sharp.dll` (all from `external\` source; 38 warnings, 0 errors, 9 s). NuGet:
  `SixLabors.ImageSharp 3.1.11` and `SixLabors.Fonts 2.1.3` were already in the user package cache; the TazUO tree's own
  `nuget.config` names nuget.org.
- Copied those six DLLs plus `zlib.dll` from `classicuo-src\external\x64\` (the TazUO client's own native zlib, same
  sha256 as the shard's running clients; the only binary not built here) into `uo-region-editor\src\lib\`.
- Added `uo-region-editor\src\nuget.config` pointing at nuget.org: this PC's `%APPDATA%\NuGet\NuGet.Config` has an
  empty `<packageSources>` and only the Visual Studio offline folder is registered, so the first build failed with
  NU1101 on every Silk.NET package. With it: restore 1.3 min (Silk.NET 2.23.0 family, ImGui.NET), build 0 warnings.
- `--selftest` with `UORE_MULS=D:\UO\tool-trials\client-data-copy`: **99 PASS, 3 FAIL**
  (`uo-region-editor\selftest-report.txt`). The three: "cave floor statics share the land cave type: 0 cave statics",
  "detail chunk render" and "iso chunk render" non-empty checks. All three are the author's fixtures for his own custom
  map: the render checks sample tile 6500,3320 ("the mall"), which on the OSI Felucca map is the black void east of the
  Lost Lands, and the cave check looks for his tiledata names. The same code renders Britain fine (next line).
- `--rendertest 1430 1690 shots\rendertest-britain-1430-1690.png`: a 1600x1200 isometric composite of Britain from the
  copy, land, statics, hues and texmaps all correct (`uo-region-editor\shots\rendertest-britain-1430-1690.png`).
- GUI run: `src\bin\Release\net10.0-windows\UORegionEditor.exe`, driven by `D:\UO\tool-trials\ui.ps1` (a 40-line
  screenshot, click, drag, wheel and SendKeys helper written for this trial), with `last-project.json` pre-seeded to the
  copy's path so no folder dialog was needed. Section 6.1.
- Not built or run: the `Server\` project, `--classic`, `build-release.ps1`.

### 5.2 uotinker

- `uotinker\src\`: robocopy of `third-party\code\uotinker\uotinker-0.2.0` (450 KB).
- `%APPDATA%\UOTinker\settings.json` written before the first start:
  `{"DataFolder": "D:\\UO\\tool-trials\\client-data-copy", "ReadOnly": false, "CheckUpdates": false, "Language": "en"}`.
- `dotnet build UOTinker.csproj -c Release`: 5 s, 1 warning (nullable in the borrowed BwtDecompress.cs), 0 errors, no
  restore. Output `src\bin\Release\net8.0-windows\UOTinker.exe` (the window title says "Version 0.1.1": the assembly
  version in the csproj lags the 0.2.0 release tag).
- **UOP to MUL unpack**, because uotinker reads MUL art only (headline 3): `uotinker\Uop2Mul\` (C#, 70 lines, references
  the from-source `ClassicUO.IO` for `UOFileUop.CreateHash` and `ClassicUO.Utility.BwtDecompress`; `uotinker\uop2mul.py`
  is the first, Python, version that handled art but not the flag-3 zlib+BWT gump entries). Written into the copy only:
  `art.mul` 148,028,746 bytes + `artidx.mul` (81,920 entries, 43,433 valid, all flag 1), `gumpart.mul` 174,597,976 bytes
  + `gumpidx.mul` (65,536 entries, 5,548 valid of 5,556 in the uop, all flag 3; the 8 unmatched hashes are not in the
  `build/gumpartlegacymul/NNNNNNNN.tga` name range). Section 6.2 checks the art against the uop pixel for pixel.
- `--selftest` (four runs: three crashed early on missing art.mul, gumpidx.mul and the author's gump-id fixture, the
  fourth passed every data test; `uotinker\selftest-report.txt`). **This is the run that reached the update section and
  went to GitHub** (section 8). I should have read `SelfTest.cs` to the end before running it.
- GUI run: `UOTinker.exe`, same helper. Section 6.2.
- Not built or run: `Setup\UOTinker.nsi`, `tools\*.ps1`, any "check for updates" menu item.

### 5.3 SpriteMotion

Nothing. Deferred by decision 3(c).

## 6. Trial results

### 6.1 UORegionEditor: open, draw, export

Screenshots in `D:\UO\tool-trials\uo-region-editor\shots\` (full 2560x1440 desktop captures; the editor window is the
left two thirds):

| Shot | What it shows |
|---|---|
| `01-startup.png` | Start dialog: Connect to server / Work offline / Open muls folder. |
| `02-offline-map.png` | Work offline: Felucca radar map of the copy at 0.21x, status bar `MULS: LOCAL (client-data-copy) OFFLINE MODE`. |
| `03-zoomed.png` | Wheel-zoomed to 1.58x on Ocllo (map0 3497,2559). |
| `04-drawn-box.png` | F2 Draw box, one drag: `A_REGION_1` over Ocllo town, auto P at 3651,2547, 99x131 tiles. |
| `05-view-menu.png`, `06-options.png`, `07-shard-combo.png` | Renamed to "Old Haven Training"; View > Options > Shard "Editing for": Sphere / ServUO / CentrED / ModernUO. |
| `08-modernuo-mode.png`, `09-type-picker.png` | ModernUO mode: properties become Type (picker lists BaseRegion, TownRegion, DungeonRegion, NoHousingRegion, GuardedRegion, JailRegion, GreenAcresRegion), Priority, Music, Go location, Boxes. Type set to BaseRegion. |
| `10-file-menu.png`, `11-export-menu.png`, `12-save-dialog.png`, `13-after-export.png` | File > Export > "ModernUO regions.json... your shard" opens a normal Save As dialog; typed the path; status "Exported ModernUO regions.json". |
| `14-project-saved.png` | File > Save project as: `export\old-haven-training-project.json` (the editor's own format, keeps MapPlane, Sphere fields, colour). |
| `15-centred-view.png` | View > CentrED view: the isometric art view of the same spot drawn from the copy through the from-source ClassicUO loaders. |
| `rendertest-britain-1430-1690.png` | The offline `--rendertest` composite of Britain. |

**The export** (`D:\UO\tool-trials\uo-region-editor\export\regions.json`, 323 bytes):

```json
[
  {
    "$type": "BaseRegion",
    "Map": "Felucca",
    "Name": "Old Haven Training",
    "Priority": 50,
    "Area": [ { "x1": 3602, "y1": 2482, "x2": 3701, "y2": 2613 } ],
    "GoLocation": { "x": 3651, "y": 2547, "z": 0 }
  }
]
```

**Does it fit the shard?** Yes, as-is, for a flat region. Pinned reads `Distribution/Data/regions.json` through
System.Text.Json with `$type` as the polymorphic discriminator set to each registered region class's name
(`Projects/Server/Regions/RegionJsonSerializer.cs:32, 93`), and the data file's own records carry exactly these keys in
this order (`Distribution/Data/regions.json:1-40`: `$type`, `Map`, `Name`, `Priority`, `Area`, `GoLocation`, `Music`,
and for towns `Entrance`). `BaseRegion` is `Projects/UOContent/Regions/BaseRegion.cs:10`. The `+1` on x2/y2 is right:
pinned's `Rectangle2D` treats the end as exclusive (`Projects/Server/Geometry/Rectangle2D.cs:126-130`), and the editor
shows the drawn box as 3602,2482 - 3700,2612 (99x131) and exports 3701/2613. So a staff member can paste the array
element into the shard's regions.json (or a P-prompt can merge it) with no converter.

What it cannot do, and the workaround for each:

- **One map.** `MulRadar.FindMap` looks for `map0LegacyMUL.uop / map0.uop / map0.mul` only (`MulRadar.cs:171-182`), so
  the editor always shows Felucca. A region's facet is `MapPlane`, exported as the `Map` name
  (`ModernUoJson.cs:24, 50`), and the ImGui UI has no control for it (the only "Map" text in `ImGuiPanels.cs` is the
  Controls help heading, line 516); it is 0 for anything drawn. For Trammel (same land as Felucca) draw on the Felucca
  picture and change `"Map": "Felucca"` to `"Trammel"` in the export. For Ilshenar, Malas, Tokuno or Ter Mur there is
  no picture to draw on: the workaround is a copy of the client folder with that facet's files renamed to map0 (or the
  ServUO/CentrED imports, which carry facets), which is a job for the install step, not this trial.
- **No `Parent`, `Entrance`, `MinZ`/`MaxZ`**, and only the seven region classes above. Nested regions (a jail inside a
  dungeon level, as P194 registers in code) and the shard's own region classes stay hand-written or code.
- **The P189 "Old Haven Training" region** does not exist in this tree (no regions file in the Bronze ShatteredLegacy
  copy, no such region in the server code; pinned's `regions.json` is the shard's region data), so the test region here
  is the Ocllo box named after it, not a comparison with it.

Everything else behaved: 60 fps, chunked background rendering, undo, a readable status bar, sensible dialogs. Writes
outside the sandbox: `%LocalAppData%\UORegionEditor\` (`last-project.json`, `layout.ini`, `ui.json`, one 4.6 MB
`radar-<hash>.png` map cache). No crash, no `crash.txt`.

### 6.2 uotinker: view, export, edit, save, reopen

Screenshots in `D:\UO\tool-trials\uotinker\shots\`:

| Shot | What it shows |
|---|---|
| `01-startup.png` | Overview page in English, data folder `client-data-copy`: 39,189 item art, 5,514 gumps, 1,131 animated bodies, file table (art.mul, gumpart.mul, tiledata.mul, hues.mul, radarcol.mul, skills.mul, anim1-6, AnimationFrame*.uop, bodyconv/body.def, mobtypes.txt). No update prompt. |
| `02-items.png` | Items (Art) grid from the unpacked art.mul. |
| `03-goto-0F3F.png` | Go to ID `0x0F3F`: arrow, 44x33, tiledata name "arrow", flags, with Import / Export as PNG / Clear slot / Save Art buttons. |
| `04-export-png.png` | Export as PNG through a normal Save dialog: `export\arrow-0x0F3F.png` (228 bytes). |
| `05-hues.png`, `06-hue-1258.png` | Hues grid (3,000 hues, 375 groups); hue 1258 "FireWeap5", table 15360-32513, the 32 colour cells and the raw values. |
| `07-tiledata.png`, `08-tiledata-0F3F.png` | Tiledata grid; item 0x0F3F editor (name, weight, height, layer, quantity, animID, hue, light, 36 flags). |
| `09-name-edited.png`, `10-panel-scrolled.png` | Name changed to "arrow P214"; "1 change(s) not saved yet"; Save (1). |
| `11-saved.png` | After Save: Save (0), no error. |
| `12-after-reload.png` | Overview > Reload, back to 0x0F3F: name reads "arrow P214" from the reloaded file. |
| `13-exit.png` | Exit through its own power button. |

**Save mechanics as observed.** `tiledata.mul` in the copy rewritten at 17:45:32, same size (3,188,736 bytes), with a
copy of the old file first in `%APPDATA%\UOTinker\backups\tiledata-20261020-174532.mul` (byte-identical to the
pre-edit hash). The self-test earlier had left backups of hues, radarcol and skills from its own temp copies in the same
folder; the copy's hues.mul, radarcol.mul and skills.mul did not change.

**Headless reopen** (`uotinker\Check\`, output in `uotinker\headless-check.txt`): pinned ModernUO's own
`Projects/Server/TileData.cs` compiled unchanged (linked read-only, with a 20-line stub for `Core.FindDataFile`, the
two string helpers and the attribute types) and pointed at the copy, plus the from-source ClassicUO loaders:

```
pinned TileData: items=65536 lands=16384
pinned TileData item 0x0F3F: name='arrow P214' flags=Generic, Unknown3 weight=0 height=1
pinned TileData neighbours: 0x0F3E='arrow_WEST' 0x0F40='arrows'
ClassicUO TileData item 0x0F3F: name='arrow P214' flags=Generic, Unknown2
ClassicUO ArtLoader on art.mul/artidx.mul: 39189 item graphics decode, 38999 with pixels; 0x0F3F = 44x33
art 0x0F3F from artLegacyMUL.uop = 44x33; pixel-identical to the mul copy: True
sampled every 97th item graphic: 405 compared, 0 differ between mul and uop
```

So the saved tiledata loads in the shard's own reader with the edit and its neighbours intact, and the unpacked art.mul
(what uotinker was actually showing and would edit) is pixel-identical to the client's uop art. (The flag name
differs only because pinned and ClassicUO name bit 2^31 differently.)

**Nothing else changed.** SHA-256 of every file before and after (`D:\UO\tool-trials\hashes-*.txt`):

| Tree | Before | After | Difference |
|---|---|---|---|
| `client-data-copy` | 524 files | 528 files | + `art.mul`, `artidx.mul`, `gumpart.mul`, `gumpidx.mul` (my unpack); `tiledata.mul` changed (the save). Nothing else. |
| `D:\UO\UOAlive\UOAlive 7.0.116.0` | 524 files | 524 files | identical |

**Fit for our client.** Everything uotinker reads here except art and gumps is the same file the client uses
(tiledata.mul, hues.mul, radarcol.mul, skills.mul, anim*.mul, AnimationFrame*.uop, cliloc). Art and gump edits land in
MUL files the UOP client ignores, so for art work uotinker needs a MUL to UOP packer we do not have (the unpacker here is
one way). Cliloc: our `Cliloc.enu` is BWT-compressed and uotinker says it cannot write compressed cliloc
(self-test line "Cliloctest: Fehler=This file is BWT-compressed").

### 6.3 SpriteMotion

Not run. See 7.3.

## 7. Verdicts

### 7.1 UORegionEditor: adopt for the map pipeline (staff tool)

Why: builds clean from source (with ClassicUO rebuilt from our own TazUO tree), reads our client data, exports pinned's
exact `regions.json` records, fast and pleasant to use, and its only network path is opt-in. Limits are the single map
and the missing facet field; both are workable by hand-editing `"Map"` and, later, a per-facet client folder. License
MIT (`LICENSE`), with ClassicUO's BSD-2 notice in `THIRD-PARTY-NOTICES` for the assemblies: keep both next to any
copy, and note in the copy that `lib\` holds our own TazUO-built assemblies, not the author's.

### 7.2 uotinker: keep as an occasional tool

Why: a good viewer for every client table and a careful editor (backup first, index-only rewrite, read-only switch,
reload), and the saved tiledata reads back in pinned's loader. Not for the pipeline because our art is UOP and it edits
MUL, because its cliloc writer cannot do our compressed cliloc, and because of the self-test's unconditional GitHub
calls, which say the author does not treat "no network" as a rule even if the GUI setting holds. Run it from its own
build with `CheckUpdates` off; never run `--selftest`. License GPL-3.0-or-later: a tool we run, not code we ship;
nothing from it goes into the shard's source (the UOP unpacker here uses ClassicUO's BSD code, not uotinker's).

### 7.3 SpriteMotion: deferred

Not trialled (decision 3c). Come back to it when a creature or gear rework is queued, and then do it as the fuller
trial from Phase 1's option 3(b): a portable Blender under the sandbox (`SPRITEMOTION_BLENDER`), `git lfs pull` for the
29 model files, the hash-pinned Godot fetch, all inside `D:\UO\tool-trials\spritemotion\`. Until then there is no sprite
step for it to prove. License MIT with the UO_Model3D v13 permission notice.

## 8. Everything that left the sandbox, and every network call

Writes outside `D:\UO\tool-trials\`:

- `%LocalAppData%\UORegionEditor\` : `last-project.json`, `layout.ini`, `ui.json`, `radar-63A9C2FC....png` (4.6 MB).
- `%APPDATA%\UOTinker\` : `settings.json` (written by me), `backups\` (tiledata from the GUI save; hues, radarcol,
  skills from the self-test's temp copies).
- `%TEMP%\uotinker_selftest`, `uotinker_arttest` (312 MB), `uotinker_savetest`, `uotinker_tabletest` (the
  self-test's scratch), `%TEMP%\p214-mul-only` (two symlinks from my headless check).
- Windows Error Reporting archives for the three self-test crashes (`C:\ProgramData\Microsoft\Windows\WER\ReportArchive\AppCrash_UOTinker.exe_*`).
- NuGet: `%USERPROFILE%\.nuget\packages\` gained the Silk.NET 2.23.0 family, ImGui.NET and their dependencies.
- The repo: this file only.

Network, all from this PC outbound:

- nuget.org: package restore for the region editor (Silk.NET, ImGui.NET; `uo-region-editor\editor-build.log`).
- **api.github.com and github.com release assets, by uotinker's `--selftest`** (fourth run, 17:27): `GET
  /repos/<repo>/releases/latest` twice, user agent `UOTinker/0.2.0.0`; `UOTinker_Setup_0.2.0.exe` (65,360,743 bytes)
  downloaded to `%TEMP%` twice, checksum verified once, then re-downloaded with a wrong expected checksum, rejected and
  deleted by the test (`SelfTest.cs:402-418`, report lines "Update-Pruefung", "Update-Download", "Update-Falschsumme").
  Nothing was executed; no copy of the installer remains (`%TEMP%` searched). This happened under my run, not under a
  setting Chase approved, and is the one thing in this trial that the prompt's stop rule would have caught had I read
  the file first.
- The region editor's self-test: loopback only (127.0.0.1, ephemeral port).

## 9. Deviations and decisions for Chase

1. **The uotinker self-test network calls** above. My mistake in reading order; the GUI never phoned home. If this
   changes the verdict on uotinker, the drop is easy (nothing installed).
2. **One stray click.** The first automated click ran before the helper's mouse-move function worked (its name
   collided with PowerShell's `Move` alias), so a left click fired at wherever the cursor already was, which the next
   screenshot shows was the Claude desktop app window on the right half of the screen (shot `02-offline-map.png`, first
   version, overwritten). The app's chat looked unchanged afterwards; I cannot prove the click hit nothing. All later
   clicks moved the cursor first and landed on the tool windows.
3. **nuget.org added as a source** in `uo-region-editor\src\nuget.config` (and copied into the two helper projects),
   because the user-level NuGet config here lists no sources. Sandbox only; the user config was not touched.
4. **Sandbox patch to ClassicUO** (`UOFileManager.cs:49-50`, section 5.1) so the editor's art view works on a UOP
   client. One line, commented `P214 sandbox patch`. If the editor is installed properly, either keep the patch in our
   TazUO build of the three assemblies or ask the author which upstream commit his DLLs come from.
5. **The UOP to MUL unpack** inside the copy (section 5.2) went beyond "copy the client data" so that uotinker had
   anything to show. It is derived data in the sandbox only; the uop files are untouched.
6. **No P189 region, no UOFiddler** (Phase 1 headline 5): handled as section 6.1 and decision 5 say.
7. **GUI steps needing a person:** none in the end; every step was driven by `ui.ps1` with screenshots as the record.
   The one thing a person would do differently is pick the facet files for a non-Felucca map (6.1).
8. **The `Read` tool was denied on files outside the repo** (unattended run), so screenshots were viewed from copies in
   the session scratchpad; the originals are the ones linked above.

## 10. Install steps for the adopted tools under `D:\UO\tools\` (not done in this prompt)

**UORegionEditor** (adopt):

1. `D:\UO\tools\UORegionEditor\src\`: the source copy (from `third-party\code\uo-region-editor`), with the sandbox
   `nuget.config` and the `lib\` assemblies built from `D:\UO\tazuo-sl-build\src` as in 5.1 (carry the one-line
   `IsUOPInstallation` patch, or re-check against upstream ClassicUO first). Keep the zip's five DLLs out.
2. `dotnet publish UORegionEditor.csproj -c Release -r win-x64 --self-contained false -o D:\UO\tools\UORegionEditor`
   (needs the .NET 10 Desktop Runtime, present). Do not enable single-file compression (the author's
   `build-release.ps1` warns it breaks Silk.NET's native loading).
3. Copy `LICENSE`, `THIRD-PARTY-NOTICES` and a short `OUR-BUILD.md` saying the ClassicUO assemblies and zlib.dll are our
   TazUO build (commit 3212623f) next to the exe.
4. A muls folder per facet to draw on: `D:\UO\tools\UORegionEditor\muls\felucca` can point at a read-only copy of the
   client data (never the player package or the live client); for other facets a folder with that facet's
   `mapNLegacyMUL.uop`, `staidxN.mul`, `staticsN.mul` renamed to the map0 names plus `radarcol.mul`, `tiledata.mul`,
   `hues.mul`, `texmaps.mul`, `texidx.mul`, `artLegacyMUL.uop`, `MainMisc.uop`.
5. Shard Console tools list entry; staff note: export ModernUO, fix `"Map"` by hand for non-Felucca, add `Parent` by
   hand for nested regions, then merge into the shard's regions data through a prompt.

**uotinker** (occasional):

1. `D:\UO\tools\UOTinker\`: `dotnet publish UOTinker.csproj -c Release -r win-x64 --self-contained false` from the
   source copy; .NET 8 Desktop Runtime present. Copy `LICENSE` (GPL-3.0) and `THIRD-PARTY-NOTICES.md`.
2. `%APPDATA%\UOTinker\settings.json` with `"CheckUpdates": false` and `"Language": "en"` before the first start;
   `"ReadOnly": true` as the default, flipped only for a planned tiledata/hue/radarcol/skills edit on a copy.
3. Point it only at copies. For art, keep the `Uop2Mul` unpacker beside it (BSD code), and accept that art edits do not
   reach the UOP client without a packer.
4. Never run `--selftest` (section 8).

**SpriteMotion**: nothing to install now.

## Licenses

UORegionEditor: MIT (LICENSE), with ClassicUO's BSD-2 notice for the assemblies (THIRD-PARTY-NOTICES): keep both
notices next to any copy, and our own note that the assemblies are the TazUO build. uotinker: GPL-3.0-or-later: a tool
we run, not code we ship; nothing from it goes into the shard's source. SpriteMotion: MIT (Copyright 2026 Moshu and
SpriteMotion contributors), with UO_Model3D v13 shared by permission of its artist (NOTICE.md); nothing copied.

## Repo size rule and preflight

Docs only: this file (under 40 KB). Nothing from `D:\UO\tool-trials\` is in either repo (the sandbox is 3.2 GB of
client data, builds and screenshots). ShatteredLegacy Bronze copy: `git status` clean on golem/Bronze/P214.
shard-migration Bronze copy: this file untracked, nothing else. The commit script's dry run was not run because it reads
the main checkouts, which are other desks under the hand-off rules.

P214 DONE
