# cc-P26: F-8, the animated runestone (first custom art through the player updater)

2026-10-01. Agent: Claude Code. Brief: `D:\UO\cc-prompts\cc-P26-animated-runestone.md`. Spec: `docs\feature-queue.md` F-8.
Pinned ModernUO `7c9215d97` (paths below under `D:\UO\ModernUO-pinned\Projects\`). TazUO paths are in the source of the
TazUO we ship (section 1). "Ours" paths are under `D:\ShatteredLegacy\`. Tools and red-run scripts:
`notes\cc-P26-tools\`. Nothing was placed in any world; no shard was deployed, restarted or recreated; the package
was built to scratch only and not published; `sl-modernuo:latest` was not moved (`f030e07f59bc` before and after).

> **Headlines**
>
> 1. **Built end to end, all green.** Art IDs **15376-15419 (0x3C10-0x3C3B)**, four designs of 11 frames. The package
>    ships 44 PNGs and a 15-line `art-records.json`; Play.ps1 builds patched copies of the player's own
>    `tiledata.mul` and `animdata.mul` in `app\uo-overrides\` and starts TazUO with `-uofilesoverride`. Skip path
>    **13 ms**, rebuild **278 ms**. **383 shard tests pass** (379 before, 4 new); **8 launcher facts** pass. Every new
>    fact and every new gate was seen failing first (section 7).
> 2. **Proved in the real client, short of logging in:** the packaged TazUO, started with our override list, held
>    **our** `animdata.mul` open and let go of it on exit (section 4.6). Animation in game is Chase's T-row.
> 3. **The server would have let players walk through the stone.** It reads the unpatched EA tiledata, where our
>    slots have no flags (pinned `Movement.cs:112`). Fixed **without a blocker item and without touching
>    `CLIENT_DATA_PATH`**: at startup the server writes our four records into its in-memory table
>    (`TileData.ItemTable`), the same values the players' files get (section 5.2).
> 4. **License: worse than "none stated".** The download is named "MMH7 runestone", which reads as *Might & Magic
>    Heroes VII*, and Vrark's page calls the four designs **"four directions"** of one stone. Same question F-22 raised
>    for Vrark's animated trees. **Chase's call before this goes to players** (section 3.4).
> 5. **Patch notes:** first version **2026.10.01**, the overseer's lines unchanged (all checked against the code) plus
>    one runestone line. Server start prints `Shattered Legacy 2026.10.01`; the wiki page renders; dry run only.
> 6. **Two commits already exist, made by Chase's commit script while I worked: `c386e3c` (15:12) caught
>    `ShatteredRunestone.cs` mid red run, with two deliberate breaks in it; `0f4c989` (15:13) restored it.** HEAD is
>    the tested state. Do not build or cherry-pick `c386e3c` alone (section 10).

---

## 0. Before starting

- `git --no-optional-locks status` in `D:\ShatteredLegacy`: clean at `fd88276` (P22 and P23 committed).
- Read P5, P10, P18 and P22 notes, `notes\p22-decisions-2026-10-01.md`, F-8, F-15, F-21 to F-23.
- **Numbering:** no clash. `cc-prompts` holds only P26; P22, P23, P24 have notes; nothing named P25 exists yet.
- **Not mine, in the same tree:** `docker/website/html/index.html`, `apple-touch-icon.png`, `media/` were modified by
  someone else during this task. Untouched; they went into `c386e3c` with my files.

## 1. The TazUO we ship, checked in its own source

`D:\UO\TazUO\client\TazUO.exe` and `ClassicUO.*.dll`: **26.0909.63, ProductVersion `+3212623f63436be1c0f4e3b308b202b29597c026`**
(`v.txt` says the same). That commit is "Merge pull request #1069" of 2026-09-09. I cloned PlayTazUO/TazUO and checked
it out at that commit (scratch only), so every TazUO citation below is **the shipped code**, not upstream 7deed69.

| Brief's fact | At 3212623f | Note |
|---|---|---|
| PNG art override, key id + 0x4000, before EA's art | `src/ClassicUO.Assets/ExternalImageLoader.cs:299-313`; `src/ClassicUO.Renderer/Arts/Art.cs:183-194` (`LoadSourceArtInfo`) | same lines as the brief |
| file name parse | `ExternalImageLoader.cs:428-433` `TryParseId`: **decimal**, or hex only with a `0x` prefix | we name files in decimal |
| folder | `ExternalImages\art` under `AppContext.BaseDirectory` (`:14`, `:277`, `:299`) = `app\tazuo\` | |
| only inside the art file's range | `Art.cs:196-199`; `Entries` is `max(count, 65535) + 0x4000` (`ClassicUO.IO/UOFileUop.cs:137`) | every static ID up to 0xFFFF is in range |
| a static animates with the Animation flag and animdata frames | `ClassicUO.Client/Game/Managers/AnimatedStaticsManager.cs:19-49`, `:51-120` | same |
| ground items too, not only map statics | `GameObjects/Views/ItemView.cs:463-484`, `View.cs:294-309` (`DrawStaticAnimated`) | the stone is a server item, so this mattered |
| animdata layout | `AnimDataLoader.cs:32-63`: 68 bytes at `id x 68 + 4 x (id / 8 + 1)`, 64 **signed** offsets, count, interval, start | |
| frame time | `AnimatedStaticsManager.cs:67`, `:91-98`: `FrameInterval x ITEM_EFFECT_ANIMATION_DELAY x 2 + 1` ms; constant 50 (`Game/Constants.cs:20`) | interval 1 = about 100 ms; GIFs are 80-90 ms (counted: 80,90,80,80,90,80,80,90,80,80,80 in all four) |
| `-uofilesoverride` / `-filesoverride` | **`ClassicUO.Client/Main.cs:310-312`** (the brief's 267-270 is upstream); `ClassicUO.IO/UOFilesOverrideMap.cs:16-55` | each line is split on `=` and must give exactly 2 parts; `#` and `;` lines are comments |
| tiledata and animdata opened by name through it | `TileDataLoader.cs:25`, `AnimDataLoader.cs:24`, via `UOFileManager.GetUOFilePath` (`UOFileManager.cs:103-108`), map loaded first (`:144`) | |
| how hue reaches PNG art | the PNG goes into the same atlas as EA art (`Art.cs:217-224`) and is hued by the shader; `Art.cs:58-151` (`GetHuedArtPixels`/`ApplyHue`) mirrors that shader on the CPU: RGB comes from the hue ramp indexed by the texel's red channel | so hue 0 |
| where a static is drawn | `View.cs:25-26` (`TILE_CENTER_OFFSET` 22, `TILE_HEIGHT_OFFSET` 44) and `:311-319`: image column `Width >> 1` on the tile centre, bottom row on the tile's bottom tip | the anchor rule in 3.2 |

Found while checking, worth knowing for F-21 to F-23:
- `art.def` can fill an **empty** art slot from another (`UOFileManager.cs:380-445`); a slot holding the placeholder is not
  empty, so it does not apply. The scanner treats any art.def mention as taken anyway.
- `verdata.mul`, if a player had a patched one, can replace whole tiledata groups (`UOFileManager.cs:262-336`). The
  Classic Client has none (our `client-data` has no `verdata.mul`). Not handled; noted.
- TazUO also reads `tuoassets.zip` beside the exe or in the UO folder (`ExternalImageLoader.cs:445-457`); we ship none,
  and the client folder has none.

## 2. Part 1: the 44 art IDs

### 2.1 The tool: `scripts\find-free-art.py`

`python scripts\find-free-art.py` (runs of 11), `--run 44`, `--placeholder`, `--explain 0x3C10`, `--check-registry`.
About 7 s. An ID is free only when **all** hold (the docstring lists them):

| Test | How |
|---|---|
| art | slot empty, or decodes to OSI's placeholder: **SHA-1 of the decoded pixels `1fed9f31d008...`, shared by 2,494 slots**, among them F-21's farm-cart slots 6784/6785/6807/6808. Raw bytes are no good: the same picture is stored in several encodings (the four cart slots have two different byte hashes). Other UNUSED-looking variants (7182 "Valid_Art", 9224 "Missing_Name", 12073) are refused on purpose |
| art.def | not named there |
| tiledata | flags 0, name empty or "UNUSED" |
| animdata | its entry inside the file (the shard's `animdata.mul` is 4,486,748 bytes, which ends partway through block 8187, so IDs above about 65,500 cannot animate at all), no frames, and **no other entry draws it as a frame** |
| maps | no static in `statics*.mul`/`stadif*.mul` (11,808 IDs used), no multi in `MultiCollection.uop` or `multi.mul` (13,368) |
| code | number absent from pinned `Projects\` and `Distribution\` and our `server\customizations\`, `server\patches\`, as hex (any case, any zeros) **or as a decimal word**. Decimal hits are mostly coordinates and clilocs; they still block, which is conservative but cheap |
| overrides | no `ExternalImages\art` file under any `player-package\vendor\` folder names it (Fiddle-Me-This ships gumps only: 0) |
| registry | not in `registry.csv` |

`--check-registry` re-tests the registered IDs; a hit in **our own** `server\` code counts as the ID's expected use, a
pinned hit does not. Today: **0 of 44 no longer free**.

### 2.2 The choice: 0x3C10-0x3C3B (15376-15419)

`--placeholder --run 11` found 34 runs; the longest is **0x3C01-0x3D11, 273 placeholder slots**. I took 44 consecutive
from 0x3C10 (8-aligned, clear of the decimal hits at 15360/15361). One block means each stone's frames are offsets 0 to
10 from its base and the four bases are 11 apart. Placeholder slots, not empty ones, so a client without the update
shows the word UNUSED, which is what T-2 needs to prove the updater rather than luck (`notes\cc-P26-tools\preview-on-tile.png`,
rightmost tile). Empty slots were plentiful too (the scan without `--placeholder` finds runs of 1,795 at 0xD0FD), but
a client without the update would draw the land placeholder there (`Art.cs:207-214`), which proves less.

The tiledata fields beyond flags and name are zero on all 44; nothing in the four maps' fields-range (`StaticFilters.IsField`,
0x3914-0x399F) is near.

### 2.3 The registry

`player-package\vendor\shattered-legacy-art\registry.csv`: id, id_hex, what, source, license; one row per ID, 44 rows.
The build gates on it (section 4.3), the scanner reads it, and the launcher fact checks every animdata frame is in it.

## 3. Part 2: the frames and our records

### 3.1 Frames

All 44 PNGs were checked **byte-identical** to the PNGs in Vrark's four zips (design 2's zip has a `TOP\` folder; the
others do not).

### 3.2 Anchor (`scripts\anchor-art-frames.py`)

The frames are cropped inconsistently: transparent margins of 10, 13, 24 and 7 rows at the bottom, and design 2's art
sits 14 px right of centre (x 36-86 in a 94-wide frame). They are **floating** stones with orbiting fragments, no base.
Per design, the same for all 11 frames so they stay registered: cut to the union of the frames' non-transparent pixels,
which centres it (TazUO centres on `Width >> 1`, `View.cs:311`); then **22 transparent rows below**, so the lowest
fragment sits on the tile centre and the cluster hovers over its tile. Never scaled; the tool re-reads every file and
checks the pixels inside are the source's, or fails. Result: 51x121, 51x120, 51x115, 56x119.
`notes\cc-P26-tools\preview-on-tile.png` shows the four on a grass tile drawn the way TazUO places them, beside OSI's
runestone 0xADBA and the UNUSED placeholder.

### 3.3 Records (`records.json`, shipped as `app\art-records.json`)

- **Comparable static: OSI's own animated runestone, 0xADBA "Runestone01 Glow01"** (with 0xADB5-0xADC8: five runestones,
  each with three Glow frames). Read from the client's tiledata on 2026-10-01: flags **0x01040040** (Animation, PartialHue,
  Impassable), weight 1, height 3. OSI puts its animdata only on the first Glow ID (count 4, interval 4, frames 0,1,2,1).
  The gift stone 0xED4 the Reset Stone used is a "gravestone", 0x4040, height 5: a worse match.
- **Tiledata** for the 4 base IDs only: name "shattered runestone", flags 0x01040040, weight 1, height 3, the rest 0.
  The 40 frame IDs keep their UNUSED tiledata: they are only ever drawn as frames.
- **Animdata** for the 4 base IDs: frames 0..10, count 11, interval 1, start 0.
- Readable JSON; every value is written by hand. A reviewer can see nothing of EA's is in it.

### 3.4 SOURCE.txt and the license

`SOURCE.txt`: Vrark, the URL, posted 2025-12-27, downloaded 2026-09-30, **no license stated**, the page's description in
full ("An animated runestone in four directions."), what was changed (the cut and the padding only), frame timing, and
where the record values come from.

**For Chase:** the download is "MMH7 runestone.zip" with "MMH runestone"/"MM7H runestone" files. That reads as *Might
& Magic Heroes VII* (Ubisoft); the page does not say. This is the question F-22 recorded for Vrark's animated trees
("from other games"), where the answer was to leave them out unless cleared. The pipeline does not care which art it
ships; swapping the 44 PNGs is a re-run of `anchor-art-frames.py` and a rebuild.

The **four designs are four directions** of one stone, per Vrark. `Design` is still the right control (staff pick
the facing); the feature queue's "four designs" wording is the only thing off.

## 4. Part 3: the package and the launcher

### 4.1 Launcher: `payload\app\Build-UoOverrides.ps1` (new), called from `Play.ps1`

Play.ps1, after the settings are written and before `Start-Process`: runs `Build-UoOverrides.ps1 -UoDir $uoDir` inside
a `try`, and adds `-uofilesoverride "<path>"` only when it returns a path. The builder itself never throws: any
failure is one yellow line, "Shattered Legacy art could not be prepared (<why>). Starting without it.", and `$null`.
Play.ps1's own `catch` is a second net (red run m5 showed it working).

The builder: stamp (`stamp.txt`: format line, both files' size and `LastWriteTimeUtc` ticks, the records' SHA-256);
if it matches and both copies exist at the source's size, return. Otherwise read both files, check the tiledata size
is the 7.0.9.0+ layout, find every frame drawn by another animation (one pass over animdata), and per stone check all
its frame IDs (tiledata free, animdata empty and inside the file, not another animation's frame); skip a stone that
fails with a yellow line naming the ID and why; write the records; write the copies, then `files-override.txt` (UTF-8
without BOM, since the install path may not be ASCII), then the stamp last. A path containing `=` is refused (TazUO's
split, 1). The art slot itself is **not** re-checked on the player's machine: a PNG override wins over whatever EA puts
there, and EA cannot use a slot without giving it tiledata, which is checked. That is the one place it differs from the
part 1 test.

Timing on the shard's real client data (scratch output): **rebuild 278 ms, skip 13 ms and 12 ms.** Written bytes checked
with the independent Python reader: **96 bytes changed in tiledata and 48 in animdata, all inside our 8 records**, the
files' sizes unchanged.

### 4.2 Updater (`Update.ps1`)

- `Test-Kept`: anything under `app\uo-overrides\` is never written by an update.
- `Test-RetiredLine` (and the build's copy of it, kept identical): `app\uo-overrides` is protected, so no
  `retired-files.txt` line can delete it.
- Nothing ships there, so nothing is copied over it; a new `art-records.json` changes the stamp and the next start
  rebuilds. The full `app\` backup now also copies the two overrides (about 7.7 MB); a restore puts them back with their
  own stamp, which stays consistent.

### 4.3 Build (`Build-PlayerPackage.ps1`)

- Copies `vendor\shattered-legacy-art\art\*.png` to `app\tazuo\ExternalImages\art\` and `records.json` to
  `app\art-records.json`, as Fiddle-Me-This is handled: exact count (= registry rows), no file not in the registry, no
  overwrite of a file already staged, byte-for-byte in gate 3.
- **Refuses** a payload that holds `app\uo-overrides\` (Play.ps1 run from `payload\` would leave patched EA files and a
  local path there). That is the personal-data answer too: `files-override.txt` holds the player's install path, so
  the folder is refused outright rather than scanned.
- **Gate 4, nothing of EA's:** fails on any `.mul`, `.uop`, `.idx` or `.def`, any file named like a file in the EA folder
  (`-UoData`, default `client-data\classic-client`; the build stops if it is missing), and anything under
  `app/uo-overrides/`. Our own `app/VERSION.txt` is exempt by exact path: **the gate's first real run failed on it**
  (EA has a `Version.txt`), which is how I found the clash.
- Gate 4 also checks the 44 art files against the registry and that every record ID is registered.

The real build: `ShatteredLegacy-2026.10.01.1453.zip`, **76 MB, 740 files**, gates 1 to 5 green, in scratch only.

### 4.4 CHANGELOG

Part 6 (section 8).

### 4.5 `.gitignore` (not changed)

`payload\app\uo-overrides\` would be a gitignore candidate, but `.gitignore` is outside the brief's files. The build
refusal covers the risk.

### 4.6 In the real client (no login)

The built zip extracted to scratch, the overrides built from the shard's client data, and the packaged `TazUO.exe` started
with `-settings` (empty login, 127.0.0.1) and `-uofilesoverride`. It reached its login screen and stayed up. While it ran,
renaming **our** `animdata.mul` failed with "being used by another process" and after exit it succeeded: TazUO opened the
copy the override list named (AnimDataLoader keeps it open; tiledata is read once at load and closed, through the same
lookup). It writes no log at its default level. The animation itself needs a logged-in client: T-1.

## 5. Part 4: the server

### 5.1 `ShatteredRunestone` (`server\customizations\ShatteredRunestone.cs`)

`[SerializationGenerator(0, false)]` (version 0), `: Item`, `[Constructible]` with an optional design, not movable,
`Decays` false, name "a shattered runestone", hue 0. `Design` (`[SerializableProperty(0)]`, `[CommandProperty(GameMaster)]`)
sets `ItemID` to `DesignItemIds[design - 1]` and throws for anything but 1 to 4, which `[props` reports as "An exception
was caught, the property may not be set." (pinned `UOContent/Commands/Properties.cs:398-401`) and leaves the stone as it
was. At load, `ItemID` is put back to the design's, so a GM who set ItemID by hand gets the design back. Players cannot
reach `Design`.

**Placement:** none. No seeder; nothing placed in any world. For T-1, Chase adds stones with `[add ShatteredRunestone <n>`
on the test shard. Nothing more is asked for until F-12 gives the stone a job.

### 5.2 The walk-through check: yes, it would have been

- The server loads tiledata from `CLIENT_DATA_PATH` (`Server/TileData.cs:303-305`, `Core.FindDataFile`), unpatched,
  shared by live and test (`docker-compose.yml:27`, `docker-compose.test.yml:41`).
- Movement collects only items whose `ItemData` has Impassable or Surface (`UOContent/Engines/Pathing/Movement.cs:112`)
  and blocks by `CalcHeight` (`:208-224`). For 0x3C10 the EA entry has flags 0 and height 0: **walk-through, zero
  height**, while a patched client thinks it is impassable.
- **Chosen fix: give the server our records in memory.** `ShatteredLegacyArt.Configure` (same file) writes four
  `ItemData` entries into `TileData.ItemTable`, a static array whose elements are settable (`TileData.cs:288-292`), after it
  has loaded. No file is touched, so live's shared data is unaffected. Why not a pinned `Blocker` on the tile: two items
  to place, move and delete together; a stone moved by a GM leaves an invisible wall behind; and the blocker would not
  give the stone its height or line of sight. This way the server and a patched client agree on every check that reads
  tiledata. The cost: every item with one of those four IDs blocks, which is what a registered ID is for.
- Unverified in game: an **un-updated** client sees a walkable placeholder and gets its step refused by the server (a
  rubber band). Expected, harmless.
- Line of sight and `CanFit` read the same table, so they follow too (not separately tested).
- The values are duplicated (C# constants vs `records.json`) because the server image does not contain the package.
  The launcher fact `TheServersCopyOfTheRecordsIsRecordsJsonAndEveryIdIsRegistered` compares them (watched red).

### 5.3 The Reset Stone (`ClusterFResetStone.cs`)

`StoneGraphic` is now design 1's base ID (from `ShatteredRunestone.DesignItemIds[0]`, so it is no longer a `const`), hue
0. **A stone already placed was saved with 0xED4 and hue 0x2B**, so a constant alone would not have changed it: an
`[AfterDeserialization]` sets both at load. Nothing is added to the save, no version change. Behaviour unchanged (fact 5 of
P18 still passes).

## 6. Part 5: tests

### 6.1 Server (`server\tests\Items\ShatteredRunestoneVerification.cs`, 4 facts)

1. `EachDesignRoundTripsWithItsDesignAndItemId`: designs 1-4 through the generated serializer; not movable, no decay,
   hue 0; a hand-set ItemID comes back as the design's.
2. `DesignsOneToFourAreTheRegisteredIdsAndAnythingElseIsRefused`: through `Properties.SetValue` as `[props` does: 1-4
   set and map to 0x3C10/0x3C1B/0x3C26/0x3C31; 0, 5, -1, 15376 refused and the stone unchanged; constructor and
   `ItemIdOf` throw; a Player cannot set it.
3. `TheServersTiledataForTheFourBaseIdsIsOurs`: the four table entries (name, 0x01040040, Impassable, not Surface,
   weight 1, height 3). The test host loads no tiledata (`TileData.cs:294-300` returns under xUnit), so this checks the
   table movement reads, not a step.
4. `TheResetStoneWearsDesignOneAndAnOldOneTakesItAtLoad`: new stone 0x3C10 hue 0; one with 0xED4/0x2B round-trips to
   0x3C10/0.

### 6.2 Launcher (`player-package\tests\Build-UoOverrides.Tests.ps1`, 8 facts)

`powershell -NoProfile -ExecutionPolicy Bypass -File player-package\tests\Build-UoOverrides.Tests.ps1`. Same shape as
`scripts\tests\Shard-Console.Tests.ps1`. **No EA file is read**: tiledata and animdata are built in the test, the
expected offsets are written as numbers.

1. Records land at 1125908/1126359/1126814/1127265 (tiledata) and 1053260/1054012/1054764/1055520 (animdata) as the
   expected 41 and 68 bytes; exactly 96 and 48 bytes change; the source is untouched; the list names both copies.
2. A frame slot EA has named: that stone skipped and said, the others written.
3. A frame another animation draws: that stone skipped.
4. Skip when unchanged (not rewritten, under 500 ms); rebuild after the source's time changes, after the records
   change, and after the folder is deleted.
5. Missing tiledata, a wrong size, an unwritable output: `$null` and one yellow line.
6. The C# copy of the records equals `records.json`; every frame is registered; 44 rows.
7. **Play.ps1 end to end** in a sandbox (stub `TazUO.exe` that writes its command line, stub `Setup.ps1`, `-Test
   -NoUpdate`): the game starts with `-settings ... -uofilesoverride "<list>"`; delete `uo-overrides\`, start again, it is
   rebuilt.
8. Same with tiledata missing: the game **still starts**, with `-settings` only, and the yellow line is printed.

Facts 7 and 8 check the test shard's port before launching, as Play.ps1 does, so they need the test shard up.

## 7. Red, then green

| Run | Breaks | Result |
|---|---|---|
| server build 1 | none | **383 / 383**, image built |
| server red 1 (`mutate_server.py apply`, `--tests-only`) | r1 design 2's ID off by one; r2 setter takes anything; r3 server tiledata not applied; r4 old Reset Stone keeps 0xED4; r5 hand-set ItemID kept | **4 failed / 379 passed**: exactly the four new facts. r1 masked r2 and r5 |
| server red 2 (`apply 2 5`) | r2, r5 | **2 failed**: fact 2 ("Expected: Not 'Property has been set.'"), fact 1 (expected 15398) |
| server final (`build.sh -t sl-modernuo:cc-p26`) | none | **383 / 383**, image **`61bcbbfbd028`** |
| launcher (`mutate_player.py`) | m1 record one byte late; m2 named slot counts free; m3 other animations' frames unseen; m4 stamp never matches; m5 builder throws; m6 Play.ps1 always passes an override | each fails its fact (m1 also fact 2); m5 leaves facts 7 and 8 green because Play.ps1's own catch holds |
| launcher, cross-check | C# height 3 to 4 | fact 6 red ("expected [4] but got [3]") |
| package gate 4 on doctored copies of the real zip | `app/tiledata.mul`; `app/Login.cfg`; a `.uop`; `app/uo-overrides/...`; an unregistered PNG; a missing PNG; no records; a record for an unregistered ID | **all 8 red** with their own message; the real zip green (gates 4 and 5) |
| package staging | `payload\app\uo-overrides\` present; an unregistered file in `vendor\...\art\` | both refused before staging |

Every mutated file was restored and checked by SHA-256 (`ShatteredRunestone.cs e3681a0f3941`, `ClusterFResetStone.cs
6a56f16ac83e`, `Build-UoOverrides.ps1 3c5ad2b92dce`, `Play.ps1 5af27c1704ca`). Final: 8/8 launcher facts green, 383/383
shard tests, scanner `--check-registry` 0 of 44 lost.

## 8. Part 6: the first patch notes

- `CHANGELOG.md`: section **`## 2026.10.01`** (format per its header), the overseer's lines **unchanged**, plus under
  Added: "The Reset Stone in New Haven is now a floating, shattered runestone. Accept the game update when it is offered
  to see it." It is visible to players in this build only through the Reset Stone, which is on the test shard.
- `VERSION`: `2026.10.01`.
- **Every line checked against the code**, none untrue: Wren (`ThievesDenLookout.cs:33-38`; "sits" is generous, he
  stands on a stool at z56, as Chase settled); BOD combine (`BODCombineContained.cs`, P22 5.2); bank 1,000
  (`ClusterFBankLimit.cs`); patch notes and `[version` (`ShardVersion.cs`, `ClusterFBulletin.cs`); bank materials
  (`GuildResources.cs`); T1/T2 restoration (`MinersCompactLiaisonGump.cs`); no power scrolls (`SmithSealCatalogGump.cs:36`,
  P23 D43); Artificers listed twice (P23 D41); "Show me the way" nearest and names the town
  (`ClusterFGuildStarterPath.cs:599`, P23); salvage ingots (`SmithGuildSalvageBag.cs:121-130`, P23 D42).
- **Proved on a throwaway container** of `cc-p26` (no network, a scratch copy of `Configuration-test`, client data
  read-only, empty world, removed afterwards): `[ShardVersion] Shattered Legacy 2026.10.01 (1 version(s) in the
  changelog)` at start; `VERSION` in the image is `2026.10.01`.
- `scripts\Publish-PatchNotes.ps1 -Container sl-p26-probe`, **dry run**: version 2026.10.01, a 1,251-byte page with
  Added (5), Changed (3), Fixed (3), "The wiki has no patch notes page yet." Not published.
- **Not done by me:** `[version` and the login bulletin in a client (T-5). The test shard runs `latest`, which I may
  not move, and its compose names `latest`.

## 9. T-rows for Chase (proposed; `docs\client-test-queue.md` not edited)

Before them: put `sl-modernuo:cc-p26` on the test shard your usual way, and build the package
(`.\player-package\Build-PlayerPackage.ps1`). For T-1 the updated client is that build; T-2 needs an install of the
**currently published** package (one that has never taken this update).

| Row | Steps | Pass |
|---|---|---|
| T-1 updated client animates | Update an install to the new package (or unzip it), start `Play TEST Shard.bat`, log in as GM. On open ground: `[add ShatteredRunestone 1`, then `2`, `3`, `4` on four tiles. Watch them; then walk into one | each floats over its tile and turns through 11 frames at about 10 a second (a little slower than the GIFs); you cannot walk into it; the four are the four directions. The Reset Stone (3501,2575,14) shows design 1 |
| T-2 not updated sees UNUSED | Same spot from the old install (it will offer the update: answer n) | the stones and the Reset Stone draw OSI's grey "UNUSED" tile and do not move. Walking into one, you are put back (the server blocks it) |
| T-3 rebuild | Close the game. Delete `app\uo-overrides\` in the updated install. Start again | the folder is back with 4 files (`tiledata.mul`, `animdata.mul`, `files-override.txt`, `stamp.txt`); the stones animate again; no yellow line |
| T-3b fallback | Leave EA's files alone. Rename `app\art-records.json` to anything, start | the game starts normally; stones are still and drawn from our PNGs (still art, no animation); rename it back |
| T-4 Reset Stone | Double-click the Reset Stone from 2 tiles, then 3; `[props` it | the reset gump opens from 2; "That is too far away." from 3; ItemID 0x3C10, Hue 0 |
| T-5 version and notes | `[version`. Log out and in on a fresh account, then again | "Shattered Legacy 2026.10.01" and the notes; the bulletin shows the notes on the first login only |
| T-6 staff only | As a Player, `[props` a stone | Design cannot be set |
| cleanup | `[delete` each stone added in T-1 | |

T-3b note: renaming the records file makes the builder return no override (a package with no art of ours), so it is
the mildest way to see the game start without overrides. The automated fact 8 covers a missing EA file.

## 10. Commits already made, and what to commit

`Commit-ShardWork.ps1` ran twice during this task (not by me):
- **`c386e3c` (15:12)** holds this task's files **with `ShatteredRunestone.cs` mid red run 2** (r2: the setter takes any
  value; r5: a hand-set ItemID is not put back). It compiles; two of my facts fail on it. It also holds the website files
  that are not mine.
- **`0f4c989` (15:13)** restores `ShatteredRunestone.cs`. HEAD = the tree built as `cc-p26` and tested above (the working
  tree was clean against HEAD when I checked at the end, apart from what came after: this note).

Still to commit: this note and `notes\cc-P26-tools\` (in shard-migration). Nothing else of mine is uncommitted.

## 11. For the register (deviation text)

- **F-8 (ours, a custom static):** a "shattered runestone" item with four staff-chosen designs, art by Vrark (servuo.dev
  "Animated Runestone", no license stated, possibly from *Might & Magic Heroes VII*), shipped as TazUO PNG overrides in
  art slots 0x3C10-0x3C3B, animated through tiledata and animdata records the launcher writes into copies of the player's
  own files. OSI has no such item. Why: Chase, 2026-09-30/10-01, to prove the package can ship new art end to end. The
  server's in-memory tiledata for its four item IDs is ours, not the EA file's, so it blocks like OSI's runestone.
- **F-7b, amended:** the Reset Stone now wears the runestone's look (design 1, hue 0) instead of the gift stone hued 0x2B.

## 12. Go-live

- **The Reset Stone leaves** at the live rebirth, as P18 lists (its file, seeder, `[ResetMyAccount`, its facts 5 and 6). Also
  delete fact 4 of `ShatteredRunestoneVerification` (the Reset Stone one) with it.
- **Stay:** `ShatteredRunestone`, `ShatteredLegacyArt`, the art and records, the registry, the launcher builder, the gates,
  both scripts. Live needs the package published **before or with** the server build, or live players see UNUSED.
- The license question (3.4) should be settled before the art reaches live players.

## 13. For F-21 to F-23

- Pick IDs with `python scripts\find-free-art.py --placeholder --run <n>`; add rows to `registry.csv` first; prepare
  frames with `anchor-art-frames.py` (`--bottom-pad 0` for art that stands on the ground). The build counts PNGs from the
  registry, so new art is a registry row plus a PNG, nothing in the build script.
- **Still art needs no records at all**: a PNG override is enough. Only animated art, or art that must block or have
  height, needs tiledata/animdata records, and then **the server needs them too** (`ShatteredLegacyArt`, generalise its
  list) and the cross-check fact should cover the new IDs.
- F-21's farm-cart TIFFs target 6784/6785/6807/6808: all four are placeholder slots, but `--explain` them first (the
  decimal-number test may object; then read the hit).
- F-22's animated stove, firepit and Father Christmas are 4 to 5 frames: same pipeline, interval to taste
  (`FrameInterval x 100 ms`).
- F-23 is gumps (`ExternalImages\gumps`), not art: the registry and scanner do not cover gump IDs yet.
- The records' `name` is limited to 19 ASCII characters (20 bytes, zero-terminated).

## 14. Not verified

- Anything in a logged-in client: the animation, its speed, the anchor on real terrain, walk blocking from either side,
  `[version`, the bulletin. T-rows above.
- A player's install with a `verdata.mul` that patches tiledata (1).
- HTTPS publish and update (unchanged code; the package was not published).
- `tools\progress.py` was not run (no ported content changed).

## 15. Files (`D:\ShatteredLegacy`)

```
CHANGELOG.md                                           section 2026.10.01
VERSION                                                2026.10.01
scripts/find-free-art.py                               NEW  free art ID scanner (part 1)
scripts/anchor-art-frames.py                           NEW  frames to <id>.png, cut and padded, never scaled
player-package/Build-PlayerPackage.ps1                 our art and records; uo-overrides refusal; nothing-of-EA's gate; -UoData
player-package/payload/app/Build-UoOverrides.ps1       NEW  patched copies of the player's own tiledata/animdata
player-package/payload/app/Play.ps1                    -uofilesoverride when the copies are built
player-package/payload/app/Update.ps1                  app\uo-overrides\ kept and protected
player-package/tests/Build-UoOverrides.Tests.ps1       NEW  8 facts
player-package/vendor/shattered-legacy-art/            NEW  art\ (44 PNG), registry.csv, records.json, SOURCE.txt
server/customizations/ShatteredRunestone.cs            NEW  the item; ShatteredLegacyArt (server tiledata)
server/customizations/ClusterFResetStone.cs            design 1's look, hue 0, old stones updated at load
server/tests/Items/ShatteredRunestoneVerification.cs   NEW  4 facts
```

Every file is ASCII and LF (checked by script; PNGs excepted).

## Checklist for Chase

1. Decide the art's license question (3.4).
2. Commit this note and `notes\cc-P26-tools\`: `D:\UO\Commit-ShardWork.ps1`. (The shard repo is already committed; see 10.)
3. Put `sl-modernuo:cc-p26` (`61bcbbfbd028`, 383 tests green) on the test shard your usual way.
4. Build the package: `.\player-package\Build-PlayerPackage.ps1`. Keep an install of the currently published package for T-2.
5. Run T-1 to T-6 (section 9).
6. Publish the package, then the patch notes:

   ```
   cd D:\ShatteredLegacy
   .\scripts\Publish-PatchNotes.ps1
   .\scripts\Publish-PatchNotes.ps1 -Publish
   ```
