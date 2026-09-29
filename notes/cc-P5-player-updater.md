# cc-P5: installed player packages update themselves

2026-09-29. Brief: `D:\UO\cc-prompts\cc-P5-player-updater.md`. Nothing committed, deployed or
ssh'd. `dist\` was left alone: every build went to the session scratchpad. The overseer's
uncommitted `payload\` changes (`-Test` on :2594, `Play TEST Shard.bat`, README sections) are
all still there.

## Read this first: the 09-26 players need one more manual download

The only build ever published is the 09-26 zip, and its `Play.ps1` has no update check at all
(probe 1b: no `version.json` or `UpdateBase` in it, no `Update.ps1`). Nothing on the server can
reach those installs. **The first P5 build you publish is the first one that updates itself.**
Every current player has to download it by hand once, so announce it. From then on it is
automatic. (P4's build was never published, so nobody is on it.)

## What changed

`D:\ShatteredLegacy\player-package\`:

- `Build-PlayerPackage.ps1`
  - Stamp is now `yyyy.MM.dd.HHmm` (was `yyyy-MM-dd`). It names the zip, the top folder inside
    it, `VERSION.txt`, and the new `app\package-version.txt` (one line). Two builds on one day
    no longer overwrite each other.
  - Writes `dist\ShatteredLegacy-<stamp>.version.json` beside the zip:
    `version`, `sha256` (lowercase), `bytes`, `url` (the fixed get. URL), plus an optional
    `notes` from the new `-Notes "<one line>"` parameter (ASCII only, checked). The launcher
    prints `notes` as "What is new". That was the only way I found to satisfy "print what is new"
    without a changelog file. It is an addition to the brief's fields.
  - Gate 4 (`Test-PackageZip`, so also `-CheckZip`) additionally requires
    `app/package-version.txt` with a valid stamp, `app/Update.ps1`, and a valid `retired-files.txt`.
  - New gate 5 (`Test-VersionJson`): the version.json's version equals the zip's
    `package-version.txt`, its sha256 and bytes equal the zip's, url is the get. URL, ASCII only.
    If it fails at build time, both files are deleted. `-CheckZip` runs gate 5 whenever the
    `.version.json` is beside the zip.
- `payload\app\Update.ps1` (new): the updater. See the design section.
- `payload\app\retired-files.txt` (new): header comments only, so no paths.
- `payload\app\Play.ps1`: the update check, `-NoUpdate`, `-Update`, `-UpdateBase`, and recovery
  from an interrupted update.
- `payload\README.txt`: an "Updates" paragraph after "That is all".

`D:\UO\haven-migration\` (**not a git repo**, so `Commit-ShardWork.ps1` may not pick it up):

- `Publish-PlayerPackage.ps1`: finds `<zip>.version.json`. It stops if the file is missing,
  unparseable, or its sha256 or bytes are not the zip's. It shows the version and notes, copies
  the json to staging, and passes its sha256 to Haven.
- `publish-player-package.sh`: now takes `<zip sha> <bytes> <json sha>`. It checks the staged
  json, and that the json names the zip's sha. It swaps and verifies both zips exactly as before.
  **Only after both zip URLs verify** does it back up get.'s `version.json` to
  `~/backups/player-zips/get-<ts>.version.json`, swap in the new one (atomic `mv`), then fetch it
  back through NPM and compare. If that fails, it puts back the old json (or removes the new one
  if there was none before) **and** the old zips, so the pair stays consistent. It was checked
  with `bash -n` only; it has never run (no ssh, per the brief).

Every touched file has 0 bytes above 127 (python byte count), and the four .ps1 parse cleanly
with `Parser.ParseFile`.

## Design as built, and where it departs from the brief

1. **The check** runs after the Mark-of-the-Web block and before Setup, as the brief says. It asks
   `<UpdateBase>/version.json?t=<ticks>` (the cache-buster is in case anything caches get.).
   **Windows fact:** `Invoke-WebRequest -TimeoutSec` does not cover name resolution
   (HttpWebRequest documents that DNS can take 15 s regardless of Timeout). The request therefore
   runs on a second runspace, and the launcher waits for it for 4 s and then abandons it.
   `Invoke-WebRequest -UseBasicParsing` with TLS 1.2 forced, as the brief asked, runs inside
   that runspace. The body is read from `RawContentStream`, because in 5.1 `.Content` is a byte
   array when the server does not call the type text. The json is refused unless the version is
   a stamp, sha256 is 64 hex, bytes is a number, and the url's host equals the UpdateBase host.
2. **The download** goes to `%TEMP%\sl-update\package.zip`, with the progress bar off (it slows
   5.1 roughly tenfold). Size and SHA-256 are checked, `Expand-Archive` unpacks to
   `%TEMP%\sl-update\x\`, and the launcher checks for exactly one top folder with
   `app\tazuo\TazUO.exe`, `app\package-version.txt` equal to the json's version, and
   `app\Update.ps1`. **Windows fact:** a file fetched by `Invoke-WebRequest` gets no
   Zone.Identifier, so nothing is marked. The updater unblocks what it copies anyway, as the
   brief asked.
3. **The updater that runs is the new package's** `Update.ps1`, copied to `%TEMP%\sl-update\`.
   Updater fixes therefore ship with the release that needs them. The cost: **its parameters are
   now a contract with every installed `Play.ps1`**, which the header says. Add to them, never
   rename or remove one.
4. **Windows fact: cmd.exe reads a .bat by byte offset while it runs**, so replacing
   `Play Shattered Legacy.bat` under a live cmd can execute garbage. The updater therefore
   starts in a **new window** (`Start-Process`), and the launcher exits 0 so the bat ends. The
   updater waits for the launcher's powershell PID **and** its parent cmd.exe PID, and only
   counts the parent when it really is cmd, so "Run with PowerShell" does not wait on
   explorer. Then it waits for any `TazUO.exe` whose path is this install (or whose path is
   unreadable), and says why.
5. **Backup folder is `update-backup\`, not `app.previous\`.** Departure from the brief. The reason
   is that an update also replaces files **outside** `app\`: the two root .bat files and
   README.txt. Retired paths may also be outside `app\`. A copy of `app\` alone would not restore
   a broken root .bat. `update-backup\` holds a full copy of `app\` (as the brief asked), plus
   every outside file the update will replace or retire, plus `.created.txt`, which lists each
   new file **before** it is created. Restore copies the backup back and deletes the listed new
   files. On success the backup is renamed to `update-backup.done` and then deleted, so a
   half-deleted backup can never be restored over a finished update.
6. **Crash safety beyond the brief:** `app\package-version.txt` is removed after the backup and
   written back **last**. An install that stops anywhere in between therefore reports no version
   and gets the offer again. If the machine dies mid-update, `update-backup\` survives, and the
   next `Play.ps1` start runs `Update.ps1 -Restore` before anything else (probe 6). Play.ps1 also
   removes a leftover `update-backup.done`.
7. **Never overwritten:** `app\uo-path.txt`, `app\tazuo\settings*.json`, and everything under
   `app\tazuo\Data\` except a `Data\XmlGumps\*.xml` that the install does not have yet. Files
   the player added are not in the package, so they are never touched. Unchanged files (same
   size and hash) are skipped, so an A-to-B update writes 3 files, not 930.
8. **Relaunch** runs `app\Play.ps1 -NoUpdate` (plus `-Test` or `-Lan` if the player started
   that way), through `powershell -File` with the bat's pause-on-failure behaviour, rather than
   through the .bat itself. Passing a quoted .bat path with spaces through `cmd /c` from 5.1 is
   fragile. The effect is the same launch.
9. **On failure** the updater restores, says so in red and yellow, and pauses for 60 s or a
   keypress. That is not a bare `Read-Host`, so a probe window cannot hang. Then it starts the
   old version. If the restore itself fails, the updater says where the backup is and tells the
   player to re-download and send `update-log.txt`.
10. **`update-log.txt`** is written at the install root (a transcript of the updater window).
    It is outside `app\` so a restore cannot overwrite it.
11. **Retired files:** paths relative to the package root, files or folders, with `#` comments
    allowed. The rule is shared by the build gate and the updater (the same function in both;
    the comment says to change them together). It refuses `..`, anything absolute or containing
    `:`, wildcards, anything under `app\tazuo\Data\`, the protected names (`app`, `app\tazuo`,
    `app\uo-path.txt`, `settings*.json`, `update-backup`), and, at build time only, any path the
    package itself ships. The updater skips an invalid line with a warning rather than failing.
12. **Test hooks shipped in Update.ps1**: the env vars `SL_UPDATE_FAIL_AFTER` and
    `SL_UPDATE_PAUSE_SEC`, documented in its header. Harmless unless set.

## Build gates: red, then green

Brief gate 1 (the version in the zip equals the version.json's):
- Red: a doctored json with version `2026.09.29.9999`, run with `-CheckZip`, failed GATE 5 with
  "version '2026.09.29.9999', zip ... '2026.09.29.1236'".
- Red at build time: a scratch copy of the script that writes `2000.01.01.0000` into
  `package-version.txt` failed GATE 5 with "both deleted", leaving an empty `out\`.
- Red: the 09-26 zip failed with "no app/package-version.txt" and "no app/Update.ps1", along with
  the P4 reds.
- Green: the real build.

Brief gate 2 (sha256 and bytes):
- Red: json sha256 all zeros failed with "sha256 000..., zip a37187a6...".
- Red: json bytes +1 failed with "bytes 79688948, zip 79688947".
- Red (extra): a url of `https://evil.example/x.zip` failed.
- Green: the real build.

Brief gate 3 (retired-files.txt):
- Red at build time: a scratch copy with 12 extra lines. All 11 bad ones were named: `..\outside.txt`,
  `app\..\x.dll` (contains ..), `C:\Windows\notepad.exe`, `\app\tazuo\x.dll` (absolute),
  `...\Data\XmlGumps\HP Orb.xml`, `app/tazuo/data/profiles` (under Data), `app\tazuo\*.dll`
  (wildcard), `app\tazuo\TazUO.exe` (shipped in this package), `app`, `app\tazuo\settings.json`,
  `app\uo-path.txt` (protected). The 12th, `app\tazuo\OldThing.dll`, was correctly not flagged.
  The zip was deleted.
- Green: a control copy with `app\tazuo\OldThing.dll` and `app/tazuo/old-folder/` built fine.
  This became build B for the probes. The real, comment-only file is also green.

Brief gate 4 (the P4 gates still pass): `-CheckZip` on the new zip passes GATE 4 and GATE 5. The
09-26 zip is still red on the P4 items (0 PNGs, 0 XmlGumps, no licence, `.unblocked`).

The build-script variants needed a throwaway `git init` above the scratch copy, because the
script's `git rev-parse ... 2>$null` throws under `$ErrorActionPreference = 'Stop'` outside a
git repo. That behaviour predates P5 and has no effect on Chase's machine.

## Probes

All probes ran on scratch extracts. Build A (`2026.09.29.1236`, the real script) was the old
install and build B (`2026.09.29.1239`, the retired-files control) was served by
`python -m http.server` on 127.0.0.1:8765 with `-UpdateBase http://127.0.0.1:8765`, and the
json's url was rewritten to match. Every old install was seeded with a `settings.json` username of
`probe-user`, `HP Orb.xml` moved to 300,200, `MP Orb.xml` deleted (so the update has an XmlGump
to add), the player's own `LegionScripts\mine.py` and root `my-notes.txt`, the retirees
`OldThing.dll` and `old-folder\`, and the real `uo-path.txt`. Launches went through the real
`Play Shattered Legacy.bat` with "y" on stdin. The live shard was reachable, so "game starts"
means a real TazUO.exe from the scratch folder was running (then killed).

1. **Update A to B: pass.** The offer showed both versions and the notes. The log reported
   "1 files to add, 2 to replace, 2 to remove". Afterwards: version 1239, username `probe-user`,
   `uo-path.txt` kept, `HP Orb` still at x=300 y=200, `MP Orb.xml` added, both retirees gone,
   the player's files kept, no `update-backup`, no `%TEMP%\sl-update`. The game relaunched
   ~23 s after start (76 MB from localhost).
   - 1b: in a 09-26 extract, `Play.ps1` has no update code (see the top section).
   - 1c: the same 09-26 tree with only the new `Play.ps1` and `Update.ps1` dropped in, and no
     version file. The offer said "you have an older one". The update added 179 files (170 PNGs,
     6 XmlGumps, the FMT licence, retired-files.txt, `Play TEST Shard.bat`), replaced 3 and
     retired 2. The username and uo-path survived, and the game was up in 19.1 s.
2. **Unreachable: pass.** Time from start to the TazUO process appearing, against a
   `-NoUpdate` baseline of 1.1-1.2 s: the current version (no offer) 1.1, a refused port 3.2, a
   server that accepts and never answers 5.0, blackhole IP 10.255.255.1 5.1, a DNS failure
   (`.invalid`) 1.1, bad JSON 1.1, 404 1.1, and the real get. (which has no version.json yet)
   1.1. **The most added is 4.0 s.** No run printed anything beyond the normal launcher lines,
   on stdout or stderr.
3. **Corrupt download (wrong sha in the json): pass.** It printed "the download is not the file
   the server described (79688946 bytes, expected 79688946; SHA-256 differs)" and "Nothing in
   your game folder was changed". The tree hash was identical before and after (934 files), and
   the game was up in 1.9 s.
4. **Failure injected mid-copy: pass.**
   - 4a (A install, fail after 2 of 3 copies): restored, tree identical, game up at 26.9 s (this
     includes the 2 s pause).
   - 4b (09-26 tree, fail after 100 copies, most of them new files): restored, tree identical
     (755 files), and the 100 created files removed. Directories created along the way stay
     behind empty (`Data\XmlGumps`, `ExternalImages\gumps`). That is harmless and not worth
     tracking.
5. **TazUO running during the update: pass.** With the game started from the install first, the
   updater printed the three "still open ... close the game window ... close this window to
   skip" lines and changed nothing for 27 s. After the game was closed it logged "The game is
   closed. Carrying on.", updated, and the new game was up 8 s later.
6. (Extra) **Killed mid-update:** a hand-made half state (full backup, a created file listed and
   present, a replaced `VERSION.txt`, no version file). `-NoUpdate` start: "The last update did
   not finish. The version you had before it is back." The tree was identical and the game started.

Probe caveat: PS 5.1 `Start-Process -Wait` waits for the whole process tree, including the
game. My first probe-1 harness therefore sat until the game was killed. That was a harness
problem, not a product one, and the later runs polled for the game process instead.

## Not verified

- The publish scripts have not run end to end. `bash -n` passes and the PowerShell parses.
  The first real publish is the test.
- HTTPS against get. with a real version.json: only the 404 path was exercised (1.1 s, silent).
- An install somewhere the player cannot write, such as `Program Files`. By the code, creating
  the backup fails first, and the updater says "Nothing had been changed yet" and starts the old
  game. Not run.
- Corporate proxies, and antivirus locking a freshly copied DLL mid-update. By the code, the
  latter is an error followed by a restore.

## Zip size

| zip | bytes |
|---|---|
| 09-26 dist (last published) | 76,717,212 |
| P4, new script (from cc-P4 notes) | 79,670,572 |
| P5 build A | 79,688,947 |

P5 adds **18,375 bytes** over P4 (Update.ps1, retired-files.txt, package-version.txt, and the
larger Play.ps1 and README). Against 09-26 it is +2,971,735.

## Checklist for Chase

- [ ] 1. Build: `.\player-package\Build-PlayerPackage.ps1 -Notes "Fiddle-Me-This gumps, test shard launcher, self-update"`
      (the notes are optional). Two files land in `dist\`: the zip and its `.version.json`.
- [ ] 2. Publish once: `D:\UO\haven-migration\Publish-PlayerPackage.ps1`. Confirm the output
      ends with "OK: published <sha> with version.json <sha>", and that the get. listing shows
      `version.json`.
- [ ] 3. Tell every current player to download the package again by hand, one last time (see
      the top section).
- [ ] 4. From tek-director, outside the house (phone hotspot, not house wifi). The 09-26 zip
      cannot be the "old install" here, because it has no updater. Use an extract of the build
      from step 1 instead: unzip it, log in once, then build and publish a second, newer
      package (any `-Notes`). Run the older extract. The offer should appear; press Enter, let
      the update window run, and the game should start on the new version. Check that
      `app\package-version.txt` shows the newer stamp and that your saved login is still filled in.
- [ ] 5. On the same machine, with the network off, start the game: no update text, and at most
      ~4 s slower.
- [ ] 6. If anything goes wrong, `update-log.txt` in the package folder has the whole updater
      window.
