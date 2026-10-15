# cc-P114: The Human, Admin, Gargoyle and Elf test shortcuts start our TazUO build

2026-10-15. Prompt: `D:\UO\cc-prompts\cc-P114-test-shortcuts-our-build.md`. Player-package launcher and its tests, plus
four desktop shortcuts. Not committed (the Golem commits after DONE). Both repos were clean at the start, apart from the
play-test importer's and the overnight bot's machine output in `testing\`.

## Headlines

- **New launcher option: `Play.ps1 -Test -ClientDir <folder>`.** It starts the `TazUO.exe` in that folder instead of
  `app\tazuo`'s. Everything else is the same launch:
  - the same `settings.test.<account>.json`, so the saved logins are untouched;
  - the same autologin (`-skiploginscreen`) and the same `-uofilesoverride`;
  - the same settings rewrite.
- **Refused without `-Test`**, as `-Account` is, with one red line and nothing written, so live never runs a
  development build. A folder with no `TazUO.exe` is refused the same way. Players never see it.
- **Each account keeps its per-character data.** The launcher passes TazUO's own `-profilespath` argument, pointing at
  the package's `app\tazuo\Data\Profiles`. So our build reads and writes the same files as the package client:
  gump layout (`gumps.xml`), macros, hotkeys, spell bars, autoloot, grid containers, journal filters.
- **Copied once, if missing.** TazUO reads three more things only from beside its own exe. The launcher copies them
  from the package into our build's folder when they are missing there, and never overwrites:
  - the last character per account (so autologin enters the world as the same character);
  - the Fiddle-Me-This HUD gumps;
  - your three `SL_*.py` Legion scripts.
- **What does not carry over** is listed under Deviations, item 2. The main one: the Legion scripts' remembered state
  (mining veins, satchel, forge).
- **`ExternalImages`: nothing to do.** Our build's folder already has P111's SFW set, 1,856 files. All six bodies
  hash-match `vendor\paperdoll-sos\bodies-sfw`.
- **The P111 option works through this path.** The launcher's stand-down now reads `sl-build.txt` from the client
  actually started, and it tells that client where the add-on is. The four settings files now name it.
- **The four shortcuts are repointed.** Each now runs
  `Play-Test.bat -Account <name> -ClientDir "D:\UO\tazuo-sl-build\client"` with our build's icon.
  - Each was backed up first as `<name>.lnk.bak-20261014`.
  - `LIVE`, `TEST` and `TEST (our build)` were not touched.
- **The installed package got the updated launcher.** The shortcuts run the installed `app\`, a copy of the repo from
  2026.10.05. I copied the repo's `Play.ps1`, `Launch-Settings.ps1` and `Paperdoll-Bodies.ps1` into it. The old two
  are kept as `.bak-20261015`. What an update does to this is in Deviations, item 6.
- **Tests:**
  - 8 new facts, each seen failing first.
  - All four launcher suites are now fully green: 27/27, 9/9, 12/12, 10/10. Three of them were partly red since cc-P81
    for a sandbox bug, now fixed.
- **All four shortcuts started live** for about 30 s each:
  - each ran `D:\UO\tazuo-sl-build\client\TazUO.exe`;
  - each logged straight in as that account's last character: Ringo, Eve, Garg, Elf Female;
  - each closed cleanly;
  - no errors.

## What changed, with file:line

### Shard repo (`D:\ShatteredLegacy`)

| File:line | Change |
|---|---|
| `player-package/payload/app/Launch-Settings.ps1:19-28` | `Get-LaunchTarget -ClientDir`: refused without `-Test` ("-ClientDir works only with -Test, so the live shard never runs a development build.") and refused when the folder holds no `TazUO.exe` |
| `player-package/payload/app/Launch-Settings.ps1:42-43` | the target carries `ClientDir` (full path, or empty) |
| `player-package/payload/app/Launch-Settings.ps1:52-66` | `Get-TazUOLaunch`: the exe, its folder and the arguments. The argument building moved here from `Play.ps1` unchanged (`-settings`, `-skiploginscreen` for a profile, `-uofilesoverride`), so it can be tested. With `-ClientDir` it uses that folder's exe and adds `-profilespath "<app>\tazuo\Data\Profiles"` |
| `player-package/payload/app/Launch-Settings.ps1:76-117` | `Sync-ClientDirData`: merges `Data\Profiles\lastcharacter.json`, adding only the account+server entries the client lacks (exact match, as TazUO's `LastCharacterManager` does); copies missing `Data\XmlGumps\*.xml` and `LegionScripts\*.py` (not `API.py` or `__builtins__.py`, which each client writes itself). Never overwrites; returns what it copied |
| `player-package/payload/app/Launch-Settings.ps1:233-258` | `Start-TazUO -SettingsDir`: the graphics fallback rewrites the settings files where they are (the package), while the working folder and `Logs` are the client's. Defaults to `-TazDir`, so other callers are unchanged |
| `player-package/payload/app/Play.ps1:17-22` | header: the option, TEST only |
| `player-package/payload/app/Play.ps1:42`, `:58` | the parameter, passed to `Get-LaunchTarget` |
| `player-package/payload/app/Play.ps1:293` | prints `client   <folder>` under the server and UO files |
| `player-package/payload/app/Play.ps1:310-319` | `Get-TazUOLaunch`, then `Sync-ClientDirData` for `-ClientDir` (a failure there is one yellow line; the game still starts) |
| `player-package/payload/app/Play.ps1:323`, `:332` | the paperdoll check and `Start-TazUO` use the client actually started |
| `player-package/payload/app/Paperdoll-Bodies.ps1:68-73` | `Test-ClientPaperdollOption -TazDir`: reads `sl-build.txt` from a given client folder |
| `player-package/payload/app/Paperdoll-Bodies.ps1:84-108` | `Sync-PaperdollBodies -TazDir`. The stand-down checks that client. For a client outside `app\tazuo` it also carries the install's default add-on folder, when it exists, into the settings file: that client looks for the add-on beside its own folder, so it would otherwise never find it. The carry now runs before the "no SFW source" early return, so an install from before cc-P81 (no `app\paperdoll-sfw`) still gets it |
| `player-package/tests/Launch-Settings.Tests.ps1:160-257`, `:549-587` | 7 new facts (below); `New-Sandbox` also copies `Paperdoll-Bodies.ps1` (`:421`); `Invoke-Raw -GameDir` |
| `player-package/tests/Paperdoll-Bodies.Tests.ps1:155-184` | 1 new fact |
| `player-package/tests/Build-UoOverrides.Tests.ps1:447`, `Cliloc-Overrides.Tests.ps1:296` | their `Play.ps1` sandboxes copy `Paperdoll-Bodies.ps1` too |
| `CHANGELOG.md`, `VERSION` | 2026.10.15, one `### Staff` line |

Why `-ClientDir`:
- It is the prompt's own example.
- It says what the value is: a folder holding the client. It reads like the launcher's existing `-UoPath`.
- It is not tied to our build. It starts any TazUO folder, so a second build (another branch, a newer upstream) can use
  it too.
- `-Client` alone would suggest a version or a name rather than a path.

### Outside both repos (Chase's PC)

- **Installed package** `D:\UO\ShatteredLegacy\ShatteredLegacy-2026.10.02.0840\`:
  - `app\Play.ps1`, `app\Launch-Settings.ps1`: replaced by the repo's, the old ones kept as `*.ps1.bak-20261015`;
  - `app\Paperdoll-Bodies.ps1`: new (the repo's `Play.ps1` dot-sources it);
  - `paperdoll-bodies.txt` (new, beside `app\`): `mode=sfw` and `folder=D:\ShatteredLegacy\client-addons\paperdoll-nsfw`,
    written with the launcher's own `Set-PaperdollSetting` (Deviations, item 4).
  - Nothing deleted.
- **The four settings files** gained `sl_paperdoll_folder` on their first launch. Username and password are unchanged
  (checked before and after each start).
- **The shortcuts**, Desktop:

  | Shortcut | Arguments now | Backup |
  |---|---|---|
  | `SL TEST - Human.lnk` | `-Account human -ClientDir "D:\UO\tazuo-sl-build\client"` | `.bak-20261014` |
  | `SL TEST - Admin.lnk` | `-Account admin -ClientDir "..."` | `.bak-20261014` |
  | `SL TEST - Gargoyle.lnk` | `-Account gargoyle -ClientDir "..."` | `.bak-20261014` |
  | `SL TEST - Elf.lnk` | `-Account elf -ClientDir "..."` | `.bak-20261014` |

  - Target (`app\Play-Test.bat`) and working folder (`app`) are unchanged.
  - Icon `D:\UO\tazuo-sl-build\client\TazUO.exe,0`.
- **Our build's folder** `D:\UO\tazuo-sl-build\client\`. On the first launch it received:
  - four `lastcharacter.json` entries (human, admin, Gargoyle, Elf; the client's own `elf` entry kept);
  - six `Data\XmlGumps\*.xml`;
  - `LegionScripts\SL_Lumberjack.py`, `SL_Mining.py`, `SL_Retaliate.py`.

## Tests

### New facts, each seen failing first

Run against the launcher before the change, with the new tests in place:
- 7 of 7 new Launch-Settings facts failed (27 facts, 20 passed);
- the new Paperdoll fact failed ("Cannot bind argument to parameter 'Path'": no `-TazDir`).

Then with the change: all passed.

`Launch-Settings.Tests.ps1`:
1. `ClientDirWithoutTestIsRefused`: `-ClientDir`, `-Lan -ClientDir` and `-ClientDir -Account human` without `-Test`
   are refused with the one line.
2. `AClientDirWithNoTazUOIsRefused`: an empty folder, a missing folder and an empty string.
3. `ClientDirKeepsTheProfileFileAndItsSettings`:
   - server, port, settings file name, label, server name and profile are identical with and without `-ClientDir`;
   - the settings file written is byte for byte the same.
4. `ClientDirStartsThatExeWithTheSameSettingsAutologinAndOverrides`:
   - without `-ClientDir`, the command line is exactly today's;
   - with it, that folder's exe and folder, and today's command line plus `-profilespath "<package>\Data\Profiles"`;
   - no profile means no `-skiploginscreen`.
5. `ClientDirCopiesWhatTazUOKeepsBesideItsExeWithoutOverwriting`:
   - a missing last-character entry is added and the client's own is kept;
   - a missing HUD gump and script are copied; the client's own gump is kept; `API.py` is not copied;
   - every package file hashes the same afterwards; no BOM;
   - a second run copies nothing; a client with no `lastcharacter.json` gets both entries.
6. `EndToEnd_AShortcutWithClientDirStartsThatClientAsTheSameProfile`: runs `Play-Test.bat` exactly as the shortcut does,
   in the sandbox.
   - The stub in the client folder is started, and the package's is not.
   - The command line is `-settings "<package>\settings.test.gargoyle.json" -skiploginscreen -profilespath "..."`.
   - It prints `client <folder>`.
   - The saved login is kept, and no settings file is written anywhere else.
7. `EndToEnd_ClientDirWithoutTestIsRefusedWithOneLineAndWritesNothing`: the real `Play.ps1` with `-ClientDir` and with
   `-Lan -ClientDir`. Exit 1, one line, no game started, no settings file, refused before Setup ran.

`Paperdoll-Bodies.Tests.ps1`:
8. A client started from another folder:
   - its stamp is the one read, and the package's stock client does not count;
   - the install's default add-on folder is named in the settings file even with no `app\paperdoll-sfw`, other keys kept;
   - its bodies stay SFW;
   - with no add-on in the install, nothing is named.

### Whole suites, final

| Suite | Before (HEAD) | After |
|---|---|---|
| `Launch-Settings.Tests.ps1` | 15/20 | **27/27** |
| `Paperdoll-Bodies.Tests.ps1` | 8/8 | **9/9** |
| `Build-UoOverrides.Tests.ps1` | 10/12 | **12/12** |
| `Cliloc-Overrides.Tests.ps1` | 9/10 | **10/10** |

**Why the old suites were red.** P111 reported those failures and left them for the overseer.
- All eight came from one cause: the test sandboxes copied `Play.ps1` without `Paperdoll-Bodies.ps1`, which it
  dot-sources since cc-P81.
- So every sandboxed `Play.ps1` stopped with "The term ... is not recognized".
- One added file name per sandbox fixed all eight. With that fix alone, before my launcher change, the old
  Launch-Settings end-to-end facts already passed (20 of the 20 old facts).
- So that change is a test fix, not a behaviour change.
- The overrides suites now show again that `Play.ps1` still passes `-uofilesoverride`.

The end-to-end launch facts need the test shard up (they check its port first, as `Play.ps1` does); it was up.

### The four shortcuts, live

What was done:
- Each `.lnk` was started itself (`Start-Process` on the shortcut), left for 28 s, then inspected.
- Each was closed with `CloseMainWindow` (TazUO saves its profile on close) and checked again.

Results:

| Shortcut | Process | Window title | Connected | Profile files TazUO saved on close |
|---|---|---|---|---|
| Human | `D:\UO\tazuo-sl-build\client\TazUO.exe` | `Ringo - [TazUO - 5.31.2.0]` | `192.168.1.58:2594` | 18, in the package's `human\Shattered Legacy TEST\Ringo\` |
| Admin | same | `Eve - [TazUO - 5.31.2.0]` | same | 18, in `admin\...\Eve\` |
| Gargoyle | same | `Garg - [TazUO - 5.31.2.0]` | same | 18, in `Gargoyle\...\Garg\` |
| Elf | same | `Elf Female - [TazUO - 5.31.2.0]` | same | 18, in `Elf\...\Elf Female\` |

- **Command line** of each:
  `-settings "<package>\app\tazuo\settings.test.<name>.json" -skiploginscreen -uofilesoverride "<package>\app\uo-overrides\files-override.txt" -profilespath "<package>\app\tazuo\Data\Profiles"`.
- **Logged straight in.** The title is the character name only once the client is in the world.
- **The right characters.** The four names are exactly the package's `lastcharacter.json` entries.
- **The overrides are passed.** P111's shortcut lacked them (its deviation 5).
- **Profiles really are shared.** The saved files went to the package's profile folders. The only file written under
  the client's own `Data\Profiles` was `lastcharacter.json`.
- **No new errors:**
  - no `Play-Test.bat` window stayed open (it pauses only on a non-zero exit);
  - no `Logs` folder or crash file in the client folder;
  - no Application-log errors in those minutes;
  - no TazUO left running;
  - username, password and autologin were unchanged in all four settings files.
- **Not seen:** I did not look at the screen. Whether each character's windows sat where you left them is inferred from
  the shared profile folder, not observed (For Chase, step 2).

## Deviations and decisions for Chase

1. **The name is `-ClientDir`** (reasons above, under What changed).

2. **What carries over and what does not.** TazUO keeps some data in the profiles folder and some only beside its exe.
   - **Carried, and kept in step from now on** (the package's `Data\Profiles`, via `-profilespath`):
     - everything per character: gump layout, macros, hotkeys, spell bars, autoloot, grid containers, journal
       filters, name overhead, skill groups, cooldown bars;
     - the package client and our build read and write the same files.
   - **Copied once, then separate** (TazUO reads these only beside its exe, `CUOEnviroment.ExecutablePath`, with no
     setting to move them):
     - the last character per account;
     - the six HUD gump files: `Update.ps1` notes these also hold the HUD gumps' positions, so HUD positions start
       from the package's and then move on their own;
     - the three `SL_*.py` scripts. A script you change later in one client is not copied again, because existing
       files are never overwritten.
   - **Not carried, so these start fresh on our build:**
     - `Data\legionvars.db`: the Legion scripts' remembered state. Today 18 values: SL_Mining's forge, satchel,
       crumbs, depleted, veins, links and known spots for human/Test and human/Ringo; SL_Lumberjack's groves, satchel,
       known, depleted and crumbs for admin/Chase. The scripts will rediscover or ask again.
     - `friendlies.db`: two entries, Adam and Test.
     - `Data\Client`: journal logs, user map markers. `Data\Shattered Legacy TEST`: per-shard map markers.
     - `items.db`: an item cache TazUO rebuilds.
     - `settings.db` holds only a migration number and `gump_positions.db` is empty, so nothing is lost there.
   - **Why these are not copied:**
     - they are SQLite databases and folders that both clients keep writing;
     - copying one over the other would discard whatever the other has learned, and two copies diverge anyway;
     - the only way to share them is to run both clients from one folder, which is the package client.
   - **Nothing in the package folder was deleted** and none of its data files was changed, apart from what the clients
     themselves saved on close.

3. **Two clients now share one profile folder.**
   - The same as two package clients today: if the stock TEST client and our build run the same character at the
     same time, the one closed last wins.
   - Both are TazUO upstream `3212623f` (our build is that pin plus patches 0001 and 0002), so the profile format is
     the same.
   - **If our build ever moves to a newer upstream than the package's TazUO**, it could migrate a profile forward
     that the older stock client then reads badly. Rebase both together, or drop `-profilespath` from the shortcuts
     for that period.

4. **The add-on folder for the four accounts.**
   - The install had no `paperdoll-bodies.txt` and no `client-addons\` of its own. So our build, started from its own
     folder, would have offered SFW only.
   - I named your add-on (`D:\ShatteredLegacy\client-addons\paperdoll-nsfw`, the folder P111's shortcut uses) in the
     install's `paperdoll-bodies.txt`, mode `sfw`, with the launcher's own `Set-PaperdollSetting`.
   - The launcher then carried it into the four settings files. Options > Paperdoll should list Topless and Nude.
   - It changes nothing for the stock-client shortcuts: their launcher path never swaps for `sfw`, and this install
     has no `app\paperdoll-sfw` anyway.
   - To undo: delete that `paperdoll-bodies.txt`, and remove `sl_paperdoll_folder` from the four settings files.

5. **Should `SL - TazUO TEST (our build)` move onto this path? I recommend not, for now.**
   - **It is the bare control.** It runs our build with no overrides, its own settings and its own profiles. When
     something looks wrong in one of the four, that shortcut tells you whether the launcher (overrides, shared
     profiles) or the build itself is the cause.
   - **Moving it changes how it logs in.** On this path it would be `Play-Test.bat -ClientDir ...`:
     - with no `-Account` it uses the plain `settings.test.json`, which never saves a login, so you would type it
       every time;
     - with a fifth profile (say `-Account ourbuild`) it logs in once and then straight in, like the others.
   - **Either way it would gain the overrides** (our custom texts and art) and the shared profiles. Your call.

6. **The installed copy and future updates.**
   - **What was done:**
     - the shortcuts call the installed `app\Play-Test.bat`, so the updated scripts had to be in the installed `app\`;
     - running the repo's `Play.ps1` directly would not work: it finds the settings, the UO path and `tazuo\` relative
       to its own folder;
     - so the repo's three scripts were copied in.
   - **What an update does:**
     - `Update.ps1` replaces those scripts with the new package's;
     - it never touches `settings*.json`, `Data\`, the `.bak` files, or `paperdoll-bodies.txt`.
   - **The published package is 2026.10.05.1606**, the same as installed, so the shortcuts show no update prompt today.
   - **Safe:** any package built from this commit onward carries `-ClientDir`.
   - **The risk:**
     - `dist\` already holds 2026.10.06 and 2026.10.13, built before P114;
     - if either is published and an update is accepted (Enter means yes), the four shortcuts stop with "A parameter
       cannot be found that matches parameter name 'ClientDir'" in a paused window;
     - rebuild the package before publishing to avoid it.
   - **Fixes, if it happens:**
     - copy the three scripts again (command in For Chase);
     - or put the shortcuts back from their `.bak-20261014`.
   - **After an in-place update,** the game that `Update.ps1` restarts is the package client, once (`Update.ps1` does
     not know `-ClientDir`). The next shortcut start is our build again.

7. **Test fixes outside the brief.** Three suites' sandboxes gained `Paperdoll-Bodies.ps1`, one line each (Tests,
   above). This is the cause behind the old failures P111 left for the overseer.

8. **The live test re-saved your real test profiles.** Closing each client made it save its profile (18 files per
   character) into the package's profile folders. This is the same as you closing the game. TazUO also keeps its own
   `backups\` beside each profile.

## For Chase

1. Double-click each, and you should see:
   - **SL TEST - Human:** a short console window, then our build (window title ends `[TazUO - 5.31.2.0]`), in the
     world as **Ringo** on the test shard, windows where you left them.
   - **SL TEST - Admin:** the same, as **Eve**.
   - **SL TEST - Gargoyle:** the same, as **Garg**.
   - **SL TEST - Elf:** the same, as **Elf Female**.
2. Things to check that I could not see:
   - your gumps and macros are where you left them;
   - Options > Paperdoll > Shattered Legacy lists SFW, Topless and Nude;
   - SL_Mining or SL_Lumberjack starts (it will not remember earlier veins, Deviations item 2).
3. **To put a shortcut back:** on the Desktop, delete `SL TEST - Human.lnk` and rename
   `SL TEST - Human.lnk.bak-20261014` to `SL TEST - Human.lnk`. The same for Admin, Gargoyle and Elf.
   - The old shortcut runs the package client exactly as before.
   - The updated launcher in the install still runs it the old way when `-ClientDir` is not given.
4. **To put the installed launcher back:** in `D:\UO\ShatteredLegacy\ShatteredLegacy-2026.10.02.0840\app`, rename the
   two `*.ps1.bak-20261015` over `Play.ps1` and `Launch-Settings.ps1`. Do this only together with step 3, since the
   old launcher does not know `-ClientDir`.
5. **If an update ever replaces the launcher** with a package older than this change (Deviations item 6), run this
   (one line, PowerShell):
   `foreach ($f in 'Play.ps1','Launch-Settings.ps1','Paperdoll-Bodies.ps1') { Copy-Item "D:\ShatteredLegacy\player-package\payload\app\$f" "D:\UO\ShatteredLegacy\ShatteredLegacy-2026.10.02.0840\app\$f" -Force }`
6. **Before publishing a player package,** build a new one from this commit or later, not the 10.06 or 10.13 zips
   already in `dist\`.

## Repo size

- No pending file over 5 MB in either repo. The largest changed file is `Launch-Settings.Tests.ps1`, about 30 KB.
- No scratch went into either repo: the live-test script and the debug folder are in my session scratchpad. The build,
  the shortcuts and the installed package are outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code:** `CHANGELOG.md`, `VERSION`, the launcher's `Launch-Settings.ps1`, `Paperdoll-Bodies.ps1` and `Play.ps1`,
  and four test files.
- **docs:** this note, plus the play-test importer's `testing/SUMMARY.md` and `testing/play-tests.json` and the
  overnight bot's `testing/bot-runs/2026-10-15-0130/` (machine output).

P114 DONE
