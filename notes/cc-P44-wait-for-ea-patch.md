# cc-P44: one-step install, wait for EA's patch instead of stopping

2026-10-03. Agent: Claude Code. Brief: `D:\UO\cc-prompts\cc-P44-wait-for-ea-patch.md`. Builds on
`notes\cc-P40-custom-client-research.md` section A.

**Nothing committed, published or deployed.** Git in `D:\ShatteredLegacy` was read with `--no-optional-locks` only.
EA's installer and EA's patcher were **not** run. `D:\UO\UltimaOnlineVanilla` was only read. Scratch:
`D:\UO\cc-p44-work\` (fake patcher, harness, every probe's folder and output).

> **Headlines**
>
> 1. **Chase's 2026-10-02 stop is reproduced** (red, today's `Setup.ps1` after a fake EA installer: the exact
>    "installed but not ready: ... missing client.exe, tiledata.mul, ..." message, 4 s in), and **gone** with the new
>    `Setup.ps1`: same fake installer, Setup waits for the patch, closes EA's window gently and carries on (exit 0).
> 2. **EA's patcher asks for administrator** (`requireAdministrator` in `UO.exe`'s manifest) **and restarts itself
>    as `UO.bin`**. Both shape the code: Setup looks for both process names, reads their paths with the one access
>    right a normal window has over an elevated process, and says that Windows will ask for permission.
> 3. **Likely in real life, not provable here:** because EA's window runs elevated and ours does not, Windows will
>    probably drop our "close" request to it (UIPI). Setup then waits 15 s, tells the player to close it themselves
>    and not press Play, and carries on. That path is probed (a fake window that ignores close). P35 will show which
>    one really happens.
> 4. **All 7 brief probes green; 4 of them were watched red first** (today's Setup, or a mutant for probe 3), plus
>    four extra probes and two reds for the new gate. Package gates 1 to 5 and `-CheckZip` green on a fresh build;
>    both package test files green.
> 5. **One file outside the brief's list changed:** `Build-PlayerPackage.ps1` (+9 lines), because the brief's own
>    "a gate checks it is not set in the zip" can only live there.

---

## 1. Facts (each cited)

**F1. Process names: `UO.exe`, then `UO.bin`.** `D:\UO\UltimaOnlineVanilla\logs\patcher.090626.Log` (the only log
there):

    [2026/09/06 08:41:31] Currently running as [D:\UO\UltimaOnlineVanilla\UO.exe]
    [2026/09/06 08:41:32] Notification of restart with alternate filename
    [2026/09/06 08:41:33] Currently running as [D:\UO\UltimaOnlineVanilla\UO.bin]

and it does it twice (08:41:32 and 08:41:41: once to self-patch "EAMythic Patcher", once for the game). `UO.bin` in
the folder is byte-identical to `UO.exe` (583,256 bytes, `cmp`). Strings of `UO.exe` carry the same story:
"Restart: Restarting image [%ls]", "Patcher patched. A restart is needed to continue.". `UOPatch.exe` (73,728 bytes)
is also in the folder; its strings name only a Pub75 PDB path and nothing patch-related, and the log never runs it.
**Measured (fake patcher, this PC):** a process started from `UO.bin` has `ProcessName` **`UO.bin`** (Windows
PowerShell 5.1 strips only `.exe`), so `Get-Process -Name UO` alone would miss it.

**F2. `UO.exe` asks for administrator.** `D:\UO\UltimaOnlineVanilla\UO.exe.manifest` and the manifest embedded in
`UO.exe` (its strings) both say `requestedExecutionLevel level="requireAdministrator"`. So: starting it from our
(non-elevated) window brings up UAC, and the on-screen text says so. Consequences checked on this PC (this shell is
Medium integrity, `whoami /groups`):
- `Process.Path` is empty for higher-integrity processes of the same user (ctfmon, TabTip, OverwolfHelper here),
  but `QueryFullProcessImageName` with `PROCESS_QUERY_LIMITED_INFORMATION` read all three. Setup uses the latter.
  431 of 624 processes were readable that way; the unreadable ones are services and system processes, none ours.
- Gentle close of an elevated window from a normal one: **not tested** (it needs a UAC click). Windows' UIPI is
  documented to drop such messages; Setup handles "did not close in 15 s" either way (probe x2).

**F3. Log line formats** (`patcher.<MMddyy>.Log`, format string `%ls/%ls.%02d%02d%02d.Log` in `UO.exe`; every line
`[yyyy/MM/dd HH:mm:ss] text`, local time). Quoted from the real log:

| Meaning | Line |
|---|---|
| size (several per run: patcher product first, then the game; the **last** one is the game) | `Patch size is 1901658` ... `Patch size is 1765233726` ... `Patch size is 1765126031` |
| done | `Patch Operation Complete.` |
| restart, not done (a "Failed" before it was harmless) | `Failed to patch stage [notes].` / `Patch Operation Restarting...` |
| already up to date (one product) | `Nothing to patch for [EAMythic Patcher]` |
| benign, every run | `Failed to load string table from [...]`, `Failed UI copy from [...]`, `Failed to load module [http]`, `No usable UI present! Initializing 'headless' patch.` |

From `UO.exe`'s strings only (format strings, **never seen in a log**): failures `Failed to patch main product.`,
`Failed to connect to remote host for location [%ls].`, `Failed to retrieve remote file [%hs].`,
`Retrieval for file [%ls] failed.  Status code [%u]`, `Failed local write for file [%ls].`; up to date
`Product [%ls] is up to date. Using quick patch mode.`; UI string IDs `STR_ERR_DISK_FULL`, `STR_ERR_NETWORK_FAILURE`,
`STR_PLAY`, `STR_STAT_PATCH_COMPLETE`. There is **no** "disk full" log format string, only the UI string ID; a full
disk would show as a write failure line, if at all. There is no progress line other than `Patch size`.

**F4. No log from a run with a window.** `D:\UO\ea-patch-2026-10-02\` does not exist. So whether EA's patcher shows a
window, and what it shows when done, is still unknown; Setup handles windowed (close gently), headless (probe x3:
the patcher exits, that counts as done once the folder passes) and a window that will not close (probe x2).

**F5. PS 5.1 `Start-Process -Wait` waits for the whole process tree it can see.** Measured with the fake: it did not
return while the `UO.bin` child ran (146 s, until I stopped it). Chase's run returned early, so EA's patcher was not
in our tree, consistent with it being started elevated by EA's installer. Kept `-Wait` as is (it is what found the
folder on 2026-10-02); the fake installer in the probes starts the patcher from outside Setup's tree to match.

**F6. App Paths on this PC:** both `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\UO.exe` and its
`WOW6432Node` twin exist, default value `D:\UO\UltimaOnlineVanilla\UO.exe` (`reg query`).

**Brief figures re-checked:** "1.8 GB" = `Patch size is 1765126031`; "2.7 GB" = 2,743,994,359 on disk (P40). The
old wording "about 2.5 GB" (`Setup.ps1:131`, `:175`, README) matched neither; now "about 1.8 GB" (the download).

## 2. The change

`player-package\payload\app\Setup.ps1` (all of the logic), `payload\README.txt` (wording),
`Build-PlayerPackage.ps1` (gate). `Play.ps1`: nothing there mentions the two-step flow, unchanged.

- **Detect:** App Paths `UO.exe` and its WOW6432Node twin added to the candidates (folder of the default value).
- **New state "installed, not patched":** a candidate holding `UO.exe` that fails `Test-UoFolder` (files missing, or
  `client.exe` below `$minVersion`). Reached from all three places that used to stop: after EA's installer, any
  later start, and `-UoPath`. `Wait-EaPatch`:
  - After the installer it gives EA's installer 30 s to start the patcher itself (EA: 8 s); otherwise, and on a
    later start, it starts `<folder>\UO.exe` with that working directory **only if no `UO.exe`/`UO.bin` runs from
    that folder** (path-checked; one whose path cannot be read counts as running: better wait than start a second).
  - One `Write-Progress` bar, redrawn every 2 s: bytes on disk under the folder against
    `max(2,744,000,000, last Patch size x 1.55)`, capped at 99%, plus elapsed time. **Deviation from the brief's
    "against Patch size":** Patch size is the download (1.77 GB) and the folder ends at 2.74 GB, so the bar would
    reach 100% at 64% done; 1.55 is the measured ratio from the same run. A folder already over 1 GB (the update case)
    gets "updating" with elapsed time and no percentage.
  - **Done = `Test-UoFolder` passes AND (`Patch Operation Complete.` logged at or after the wait began, or the
    patcher has been gone 15 s).** 15 s because of the `UO.exe` -> `UO.bin` handoff. `client.exe` alone never counts.
  - Then a gentle close (`CloseMainWindow`), 15 s, else the line "Close it yourself; do not press its Play button".
    Never killed.
  - Patcher gone (or Complete logged) and the folder still fails, seen on two polls: one line, the last log line
    naming an error (benign every-run lines excluded), `Start EA's launcher again? [Y/n]` once, then `Stop-WithHelp`
    with a patch-specific text (internet, ~3 GB free, double-click again; where EA's log is).
  - No byte added and no log change for `-StallMinutes` (default 10): says so, `Keep waiting? [Y/n]`. No other limit.
  - UAC refused (Start-Process fails): its own final line, "answer Yes when Windows asks".
  - Writes nothing while waiting; `uo-path.txt` only after success. EA's folder is never written (P26 rule kept).
- **Version floor:** below `$minVersion` with `UO.exe` present waits like the rest; the old "Open the launcher from
  the Start menu" text is gone (`:56` now says only the versions). A folder below the floor with no `UO.exe` still
  stops with the manual help.
- **`Stop-WithHelp`:** manual-install steps 3 and 4 ("let it finish updating, then close it" / "double-click again")
  became one step 3 that says the launcher waits. New `-PatchDir` variant for the patch failures.
- **Test-only options (none of them shipped in use):** `-ProbeFolder <dir>` (search only there), `-ProbeInstaller
  <file>` (with `-ProbeFolder` only: run this instead of EA's checked download), `-StallMinutes`. Parameters, not
  environment variables, so an inherited environment cannot switch them on. **Gate 4** now fails a zip in which any
  shipped `.ps1/.bat/.cmd` other than `app/Setup.ps1` mentions `ProbeFolder`/`ProbeInstaller`, or `Setup.ps1`
  assigns either a value (a default).
- **README:** step 2 is one step (no "close it, then double-click again"); one new "If something goes wrong" bullet.
  ASCII only; no em dashes.

**Clash check with P35/P36.** `$minVersion`, its name and its comment block stay at `Setup.ps1:26-30` (line numbers
unchanged), so P36's edit lands. **One P36 note is now stale:** P36 step 5 says "check the message an older client
gets (`:56`) still reads right". `:56` is still that message, but an older client **with** EA's launcher now waits
for EA's patch instead of getting it; P36 should read `:56` and probe 6 here instead. P35 step B4.2 already describes
this behaviour ("since P44 our launcher waits"). No other clash.

## 3. Probes

The fake: `D:\UO\cc-p44-work\fake-src\FakePatcher.cs`, built to `FakeUO.exe`, copied in as `UO.exe` and `UO.bin`. It
starts as `UO.exe`, logs EA's restart lines, starts `UO.bin`, writes `logs\patcher.<MMddyy>.Log` in EA's formats
(F3), writes `client.exe` first (a real file version, 7.0.117.0 or 7.0.24.0) and the other six required files and
filler over 20 to 40 s, logs `Patch Operation Complete.`, and has a window titled "Ultima Online" that closes on
`CloseMainWindow` unless told not to. `Run-Probe.ps1` runs Setup in a child PowerShell with answers on stdin;
`Run-AllProbes.ps1` runs the set. Red = `Setup.red.ps1`: today's HEAD `Setup.ps1` with only its candidate list and its
download replaced by the probe folder and the fake installer (diff in scratch), so its stops are today's code.

Final run of every probe against the final `Setup.ps1` (`D:\UO\cc-p44-work\probes-summary.txt`, full output in
`probe-<name>.txt`). "Starts" = `UO.exe` starts in `fake-starts.txt`; "left" = fake patchers still running when Setup
ended (the harness then stops them).

| Probe | Run | Result | Starts | Left |
|---|---|---|---|---|
| 1 after EA's installer (Chase's case) | **red**, today's Setup | exit 1 at 4 s: "Ultima Online is installed but not ready: ... missing client.exe, tiledata.mul, hues.mul, cliloc.enu, artLegacyMUL.uop, gumpartLegacyMUL.uop, map0LegacyMUL.uop." | 1 | 1 (abandoned mid-patch) |
| 1+2 after EA's installer, which starts the patcher 8 s later from outside Setup's tree | new | exit 0, 54 s: waited, "Ultima Online is ready", window closed gently 2 s after `Complete` | **1** (not a second) | 0 |
| 1 later start, folder unpatched, patcher not running | **red**, today's Setup | exit 1 at 1 s, "Found Ultima Online, but it cannot be used yet: ... missing ..." | 0 | 0 |
| 1 same | new | exit 0, 45 s: started it, waited, closed it, ready | 1 | 0 |
| 2 patcher already running at a later start | new | exit 0, 39 s, never printed "Starting EA's launcher" | **1** | 0 |
| 3 `client.exe` at second 0, the other six after the 30 s fill, 4 s apart | new | exit 0, 59 s: ready only after the last file and `Complete` | 1 | 0 |
| 3 all seven required files at second 3, `Complete` at second 33 | new | exit 0, 35 s: waited for `Complete` | 1 | 0 |
| 3 same | **red**, mutant: done = folder passes only (`Setup.mut-no-log-gate.ps1`, one line) | exit 0 at **6 s**, and closed EA's window mid-patch | 1 | 0 |
| 4 patcher fails (`Failed to connect ...`, `Failed to patch main product.`, exits), answer **y** | new | 32 s: "EA's launcher closed before Ultima Online was ready: the download is not complete." / "Its log says: Failed to patch main product." / offer / restarted once / failed again at 62 s / no second offer / patch help, exit 1 | 2 | 0 |
| 4 same, answer **n** | new | 32 s: same two lines, offer, patch help, exit 1 | 1 | 0 |
| 5 patcher stalls after 3 s, `-StallMinutes 0.5`, answers y then n | new | warning at 38 s and 69 s ("Nothing has changed for 0.5 minutes: ..."), then "Stopped waiting ..." help, exit 1; patcher **not** killed | 1 | 1 |
| 6 complete folder, `client.exe` 7.0.24.0 | **red**, today's Setup | exit 1 at 1 s: "client is version 7.0.24.0, ... Open the Ultima Online launcher from the Start menu once ..." | 0 | 0 |
| 6 same | new | exit 0, 25 s: "Ultima Online needs an update from EA first: client is version 7.0.24.0, the server needs 7.0.114.40 or newer.", waited for `Complete`, ready at 7.0.117.0 | 1 | 0 |
| x1 Setup killed 15 s into the wait (as closing the window) | new | no `uo-path.txt`; nothing written into EA's folder; patcher kept running | 1 | 1 |
| x2 EA's window ignores close (as UIPI would make it) | new | after `Complete`, 15 s, "EA's launcher is still open. Close it yourself; do not press its Play button, ...", then ready, exit 0 | 1 | 1 |
| x3 headless patcher (no window, exits when done) | new | exit 0, 34 s | 1 | 0 |
| x4 `UO.exe` will not start (stand-in for a refused UAC) | new | "EA's launcher did not start: ..." twice (offer, y), then patch help, exit 1 | 0 | 0 |

`p4 ... answer y` was rerun alone: in the batch its second fake froze at launch (see test-double trouble). x4 ran
before its final line got its own wording ("EA's launcher did not start. It needs Windows' permission ...: answer Yes
when Windows asks."); that line was checked by reading and a parse, not rerun.

**Probe 7 (already patched, current)** - 8 runs each, median wall-clock of a whole `powershell -File Setup.ps1`:

| | old | new |
|---|---|---|
| probe folder | 965 ms | 974 ms |
| real lookup on this PC (remembered path, registry; finds `D:\UO\UltimaOnlineVanilla`) | 1,029 ms | 1,050 ms |

No output from either, exit 0. +9 and +21 ms, inside the run-to-run spread (941 to 1,099 ms); `Add-Type` is only
compiled when a wait starts.

**Progress bar text** (Write-Progress shadowed by a logging function, since redirected output hides it):
22 calls in a 43 s wait, every 2 s, e.g.
`[EA's launcher is downloading Ultima Online] 12% 320 MB of about 2,617 MB (12%), 0 min 18 s`, then `COMPLETED`
before the "ready" line. (The fake wrote 600 MB, so it ended at 23%; the real 2.74 GB would reach 99%.)

**Gates.** Fresh build `ShatteredLegacy-2026.10.03.1159` into scratch (`D:\UO\cc-p44-work\dist\`, not `dist\`):
gates 1 to 5 passed; `-CheckZip` passed gates 4 and 5; `-GateSelfTest` stopped at gate 1 as designed. New gate red on
two doctored copies of that zip: `app/Play.ps1` passing `-ProbeFolder 'C:\x'` -> "app/Play.ps1 passes Setup.ps1's
test-only -ProbeFolder/-ProbeInstaller"; `Setup.ps1` with `$ProbeFolder = 'C:\x'` -> "app/Setup.ps1 gives a
test-only -Probe option a value". Gate 2 covers both changed payload files (`.ps1` and `.txt` outside `app\tazuo`);
in the zip `app/Setup.ps1` is 0 non-ASCII bytes (LF, as every shipped `.ps1`), `README.txt` 0 non-ASCII, 89 of 89
line ends CRLF. `tests\Build-UoOverrides.Tests.ps1` 8/8, `tests\Launch-Settings.Tests.ps1` 13/13.

**Test-double trouble, for whoever reruns this:**
- SentinelOne deleted the first fake (an unsigned exe that copied itself to `UO.bin` and started the copy) and
  refused to start it ("Access is denied"). The fake now never copies itself; the harness places `UO.bin`.
- Four times a freshly started fake froze before its first line (about 0.03 s of CPU, no log, no window): twice while
  two probes ran at once, and twice in a row in one folder (`runs\vis-progress`), which a fresh folder cured. Setup
  did the right thing each time (kept waiting; the stall prompt would have followed); those runs were void and were
  rerun alone. Cause not proven; the endpoint scanner holding new unsigned launches is the likely one.
- The Terminal panel's shell would not start (its integration script is missing), so the progress bar was captured
  by shadowing `Write-Progress`, not by eye.

## 4. Not verified

- Anything with EA's real patcher: elevation and UAC from our window, whether `CloseMainWindow` reaches an elevated
  window (expected: not, UIPI), what EA's window shows when done, whether EA's installer always starts the patcher
  itself, real progress against the 1.55 ratio, real failure lines. **P35 is the proof.**
- The 30 s grace after EA's installer is based on one measured 8 s.
- A patcher that is already running, logged `Complete` before we started, and stays open with the folder still
  failing (e.g. EA serving a version below our floor) is only caught by the 10-minute stall prompt.

## 5. Checklist for Chase

1. Run `Commit-ShardWork.ps1`. Build the package (`player-package\Build-PlayerPackage.ps1`); **do not publish yet**.
   The changed files: `player-package\payload\app\Setup.ps1`, `player-package\payload\README.txt`,
   `player-package\Build-PlayerPackage.ps1`.
2. Hand **P35** to CC next. Its sandbox run is the real proof: one double-click, EA's license, wait, game opens. Ask
   it to note: did Windows ask twice or once, did EA's window close by itself or did Setup print "Close it
   yourself", and how long the wait was.
3. Publish only after P35 passes.

Scratch, safe to delete: `D:\UO\cc-p44-work\` (about 1.5 GB of probe folders).
