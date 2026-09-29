# cc-P10: player updater polish, D36 (a stop saves), D38 (console exec output)

Brief: `D:\UO\cc-prompts\cc-P10-updater-polish-and-d36.md`. Done in the brief's order: C, then A, then B.
Nothing is committed or deployed. Every change is in `D:\ShatteredLegacy`'s working tree, **mixed in with cc-P9's
uncommitted Test Center work** (`server/customizations/TestCenter/`, the AccountHandler patch,
`CharacterCreation.cs`, `apply-patches.sh`). Only the files listed under each part are P10's.

## 0. Read first: the live shard has not been running its world since 14:16

Found while reading the live log for fact B3. **Not caused by P10 and not touched by it.** Read-only facts:

- `sl-modernuo` started at 19:16:01Z (14:16 local). World load stopped at
  `***** Bad deserialize of Server.ClusterFAccountPersistence (0x40128E03) *****`,
  `ArgumentOutOfRangeException: Ticks must be between DateTime.MinValue.Ticks and DateTime.MaxValue.Ticks`,
  thrown in `IGenericReader.ReadDateTime` from `WoodDiscoveryEntry..ctor` from `ClusterFAccountData..ctor`, and it
  is waiting at `Delete the object and continue? (y/n/a):`. At 16:15 local the log had no line after the archive
  prune at 14:16:17 and **zero** `Client:` lines for the whole run.
- Port 2593 still accepts TCP (Docker's forwarder), so `Test-NetConnection` and `Play.ps1`'s reachability check both
  pass. A player gets a client that connects to nothing.
- Every file in the live `Saves/` is timestamped 13:50:00 (20 files), the autosave 52 s before the T-018 stop at
  13:50:52. There is no file named for `ClusterFAccountPersistence` among them; where that type is read from, and
  whether its data was written by a different version of `WoodDiscoveryEntry`'s serializer, is **unverified**.
- Answering that prompt deletes something from the live world. That is Chase's decision. I sent a phone notification
  at about 16:12.

## Part C: D38, the console swallows exec output

**Changed:** `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`.

- `Invoke-ExecStep` (`:1407`) runs the command with `2>&1`, sends each line to `Write-ConsoleLine` (the screen, or the
  form's output box) and to a file, and returns **only** the exit code. `ErrorActionPreference` is set to Continue
  inside it, because under Stop 5.1 throws on the first stderr line of a native command, and docker writes its
  progress to stderr. Failure is still `$LASTEXITCODE` only.
- **The tee: yes.** One file per run that has exec steps, `scripts/shard-console-output/<yyyyMMdd-HHmmss>_<action>_<shard>.log`
  (`New-ExecOutputFile`, `:1397`), headed and footed per step (`== <time> [n/m] <command>`, `== exited with N`). It is
  written with AutoFlush, so a window killed mid-build still leaves what it had. A failure prints `Everything the
  commands printed is kept in <path>` (`:1532`). `*.log` is already gitignored. The folder is never pruned; a rebuild
  writes about 72 KB.
- **The red run showed a worse bug than D38 described.** `$ok` came back as `System.Object[]`: the child's lines plus
  `False`. `if ($ok)` (`:2142`) treats that array as true, so on the old code **a failed exec step that printed
  anything would have ended the headless run with `done.` and exit 0**. Chase's 15:28 rebuild printed `exited with 1`
  from the catch block. What its last line said is not recorded.

**Facts, red then green:**

| Fact | Old code | New code |
|---|---|---|
| `AnExecStepThatSucceedsLeavesTheExecutorReturningOneTrue` (`Tests.ps1:468`) | FAIL: "Invoke-Plan returned 3 objects: d38 out one \| d38 out two \| True" | PASS |
| `AFailedExecStepShowsItsOutputInAHeadlessRunAndTheResultIsOneFalse` (`:478`): a real `powershell.exe` with no form runs a step that prints two lines and one stderr line and exits 1 | FAIL: `RESULT count=3 type=System.Object[] value=d38 out one d38 out two False`, and the two stdout lines were not on screen | PASS: all three lines on screen, `FAILED at step 1 ... exited with 1`, one `False`, one output file holding all three lines and `exited with 1`, and the failure names the file |

My first attempt at the second fact was red for the wrong reason: `powershell.exe -EncodedCommand` called from
PowerShell returns CLIXML. It now writes a script and uses `Start-Process` with redirects, the way the existing D37
facts do.

**A defect I introduced, then fixed:** the existing `TheExecutorRunsNothingWithoutTheTypedPhraseOrTheYes` used the
real config, so after the change it wrote `*_fact_live.log` files into the real `scripts/shard-console-output/`. That
fact now uses a throwaway log path, and I deleted the four stray files it had written.

**Suite:** 68 facts before; 71 after, all green (two D38 facts, one D36 wording fact). ASCII-only checked.

**Real run:** `Shard-Console.ps1 -Action test.rebuild -Mode Execute` at 16:33 ran for 218 s. All three build.sh gates
were on screen as they ran (844 lines), then `Built sl-modernuo:latest ... 258 shard test(s) passing`,
`test.rebuild: done.`, and `20260929-163354_test.rebuild_test.log` (72,448 bytes). `test.stop` and `test.start` also
ran for real, with compose's own output on screen.

## Part A: player updater polish

**Changed:** `player-package/payload/app/Play.ps1`, `player-package/payload/app/Update.ps1`. README: no change,
because its update section does not mention `-Update` (the brief said to change it only if it did).

1. **Download progress.** A new `Save-Download` uses `HttpWebRequest` and copies the stream in 64 KB chunks. It calls
   `Write-Progress` at most once per 250 ms ("12.3 of 76.0 MB (16%)") and prints `Downloaded 76.0 MB in N s` at the end.
   **I chose this over BITS** because BITS needs the BITS service and a server that behaves the way it expects, it
   has proxy quirks, and it would be one more moving part on players' PCs. The request goes through the same
   `ServicePointManager`, so TLS 1.2 is unchanged. `Timeout = 600000`, which is what I believe 5.1's
   `Invoke-WebRequest -TimeoutSec 600` set; **I have not verified that against 5.1's source.** A stalled body fails on
   the default `ReadWriteTimeout` (5 min). The size and SHA-256 check is untouched. `$ProgressPreference =
   'SilentlyContinue'` is gone from `Install-Package`. It never affected `Expand-Archive`'s bar anyway, because a
   module function reads its preferences from the module's scope, not the caller's.
2. **Wording.** When the versions are equal: `-Update: reinstalling the current Shattered Legacy package, <v>. You
   already have it.` When the server's version is older: `...which is OLDER than yours (<v>). Installing it anyway.`
3. **Waiting.** `Update.ps1` now waits **only for a `cmd.exe`** PID, and prints `Waiting for the launcher window to
   close...` then `It closed after N s` or `It is still open after 60 s. Carrying on.` PowerShell PIDs are skipped:
   PowerShell has read Play.ps1 in full before it runs, and Play.ps1 holds no file open. From an open PowerShell
   prompt the PID was the prompt itself, which never exits. The choice is made in `Update.ps1` because it is the new
   package's copy that runs, and every installed Play.ps1 still passes both PIDs. The .bat case is unchanged: the cmd
   running the .bat is still waited for.
4. **Nothing to do.** With 0 to add, replace and remove, it makes no backup and runs no copy. It writes
   `package-version.txt` only if that file is missing or different (the file is outside `$copy`), says `Already up to
   date: <v>. Nothing was changed.`, and relaunches. The header comment says so.
5. `-Update` on the current version is kept. It now proves offer, download, checksum and unpack, then does nothing.

**Gates.** Build A (`2026.09.29.1602`) and build B (`2026.09.29.1603`) were built from the final code into scratch.
Both builds passed gates 1 to 5 (exit 0), and `-CheckZip` on both printed `GATE 4 passed` and `GATE 5 passed`.
Nothing went into `dist\`.

**Probes.** All ran on scratch extracts, served by `python -m http.server` on 127.0.0.1:8765 with `-UpdateBase`, and
launched through the real `Play Shattered Legacy.bat` with "y" on stdin unless the row says otherwise. Each install
was seeded with username `probe-user`, the real `uo-path.txt` and a player file `my-notes.txt`. "Game at" is seconds
from launch until a `TazUO.exe` from that install was running; the harness then killed it. The tree diff always
includes the 3 files TazUO creates on first run and the `settings.json` Play.ps1 rewrites.

| # | Run | Old code (red) | New code (green) |
|---|---|---|---|
| 6 | same version, `-Update`, via the .bat | 1331 to 1331: "A newer ... is out: 1331 (you have 1331)"; "0 files to add, 0 to replace, 0 to remove"; **backup made**; game at **31.5 s** | 1549 to 1549: reinstall wording; "Already up to date"; **no backup folder seen at any poll**; game at **17.7 s** |
| 8 | same, from an open PowerShell prompt | game at **86.4 s** (a silent 60 s wait) | game at **17.2 s**; no waiting line, because there is no cmd.exe to wait for |
| 8b | from an open cmd prompt (the cmd outlives the .bat) | not run | `Waiting for the launcher window to close...` / `It is still open after 60 s. Carrying on.`; game at 78.4 s. The honest line, still the old wait: that cmd is reading the .bat |
| 1 | A to B, with one file to replace and one XmlGump to add | (P5) | "1 files to add, 2 to replace, 0 to remove" (the 2nd is `VERSION.txt`); version 1603; `MP Orb.xml` added; `README.txt` replaced; username, uo-path and `my-notes.txt` kept; no `update-backup`, no `%TEMP%\sl-update`; game at 26.2 s. No waiting line: the .bat's cmd had already exited |
| 2 | unreachable update server | (P5) | `-NoUpdate` 1.4 s; current version, no offer 2.3 s; refused port 3.3 s; blackhole 10.255.255.1 5.2 s; DNS `.invalid` 1.4 s. **Adds at most 3.8 s**, silent |
| 3 | wrong sha in version.json | (P5) | "the download is not the file the server described (79690264 bytes, expected 79690264; SHA-256 differs)"; "Nothing in your game folder was changed"; no unpack; tree unchanged; game at 2.0 s |
| 4 | `SL_UPDATE_FAIL_AFTER=1` | (P5) | "The update stopped: test failure injected after 1 files"; "Everything was put back"; version still 1602; tree unchanged; game at 28.5 s |
| 5 | game open from the install | (P5) | the three "still open ... close the game ... close this window" lines; carried on once the game was closed; updated to 1603; game at 36.0 s |
| T-021 | **1331 install to B**: old Play.ps1 with the new Update.ps1, which is what the outside computer will do | - | "A newer ... 1603 (you have 1331)"; 0 add, 3 replace (`Play.ps1`, `Update.ps1`, `VERSION.txt`); version 1603; game at 26.7 s |

**Probe 7, the cost of the progress bar.** Each download ran in its own real console window (where a bar costs
something), 3 rounds, times in seconds. Progress records were counted in a runspace.

| file | old: IWR, bar off (HEAD) | old: IWR, bar on | new: Save-Download, bar on |
|---|---|---|---|
| 8 MB, localhost | 0.13 / 0.11 / 0.16 (0 records) | 3.61 / 3.88 / 3.65 (842) | 0.21 / 0.16 / 0.17 (2) |
| 76 MB package, localhost | 0.50 / 0.54 / 0.45 (0) | 35.69 / 37.11 / 35.10 (7,980) | 0.47 / 0.55 / 0.62 (3) |
| 20 MB at 4 MB/s (a throttled local server) | 5.09 / 5.09 (0) | not run | 5.05 / 5.17 (**21 records, about 4 a second**, "0.1 of 20.0 MB (0%)" to "19.3 of 20.0 MB (97%)") |

So the new bar costs nothing measurable. On localhost it has almost no time to show, but on a real link it updates
about four times a second. The old bar-on IWR is about 70x slower, which is why it was turned off.

**Not verified:** HTTPS against get. (every probe was plain HTTP to localhost), a proxy, and a TLS failure halfway
through a download.

## Part B: D36, a `docker stop` saves

**Changed:** `server/customizations/Misc/SaveOnShutdown.cs` (new), and the console wording in `scripts/Shard-Console.ps1`
plus its facts. Two temporary probe files were built, run and deleted; copies are in this session's scratch only.

### B.1 Fact 1: what runs on SIGTERM. Answer: nothing, unless something registers for it

`entrypoint.sh` ends with `exec dotnet ModernUO.dll`, so dotnet is PID 1 (`docker top`). The pinned logger writes
through `WriteTo.Async` (`Server/Logger/LogFactory.cs:25`), so a missing log line after a stop proves nothing. Every
probe line below used `Console.WriteLine` plus `Flush`.

| Build (tag, all via build.sh, 258 shard tests green) | Probe hooks | `docker stop -t 60` result |
|---|---|---|
| stock image (before any probe) | none | 0.93 s, exit 143, no `Shutting down` line |
| `p10-red2`: probe **without** a signal registration, the stock default | Unloading, ProcessExit, EventSink.Shutdown, CancelKeyPress | 0.81 s, exit 143, **none of the four lines** |
| `p10-red`: probe **with** a non-cancelling `PosixSignalRegistration(SIGTERM)` | the same, plus the registration | 1.14 s, exit 143; **only** `SIGTERM seen by a PosixSignalRegistration` |
| `p10-green`: the probe plus `SaveOnShutdown.cs` | the same | 1.6 s, **exit 0**; SIGTERM, then `Saving the world before shutdown...`, `...saved in 498 ms`, `Shutting down`, `EventSink.Shutdown raised`, `Unloading raised`, `ProcessExit raised` |

**So in this container a SIGTERM runs no managed shutdown at all.** `HandleClosed` (`Server/Main.cs:333-348`) never
runs on a stop, and neither do `EventSink.Shutdown` or `ProcessExit`. The green row shows the probe's lines do print
when shutdown really runs, so their absence in red2 is real. **Why .NET 10 terminates this way here is unverified.**
The measurement is what counts, and it overturns part of D36 as written: `-t 60` never let "a write in flight
finish", because nothing waits.

The one thing that does run is a `PosixSignalRegistration`, as the red row shows. The fix uses that path, so it is not
an invented one.

### B.2 Fact 2: how a save is triggered and awaited

- `World.Save()` (`Server/World/World.cs:241-252`) only queues work: `WaitForWriteCompletion`, `Reset`, state
  `PendingSave`, then `Preserialize` on the thread pool, which posts `RequestSnapshot` to the event loop. The
  snapshot runs **on the loop** (`Main.cs:483-488`), and `WriteFiles` runs on the thread pool and calls
  `_diskWriteHandle.Set()` (`World.cs:380`) only after `MoveDirectoryContents` into `Saves/`. So a save needs a
  running loop.
- `Core.Kill()` straight after `Save()` on the loop would deadlock: the loop's kill branch calls
  `WaitForWriteCompletion` (`Main.cs:490-494`) before the snapshot it waits for has run. Pinned's own shutdown with
  save (`AdminGump.cs:4015-4034`) calls Save, then does the wait and Kill from the thread pool. The fix copies that
  order.
- `EventLoopContext.Post` enqueues on a `ConcurrentQueue` (`Server/EventLoopTasks.cs:45-46`), so posting from the
  signal thread is safe. `World.Save` is only ever called on the loop.

### B.3 Fact 3: how long a live save takes. The bug list was wrong

The captured live log (`scripts/tests/fixtures/console-capture-2026-09-29.txt`, section `logs sl-modernuo`) has three
saves. The snapshot phase took at most 0.07 s. **The write, which includes the backup move, took 32.16, 17.72 and
3.54 s.** The 32 s write came right after the hourly archive. D36 used to say 1.00 s. The test world's write takes
0.27 to 0.50 s.

**Both containers have `StopTimeout: 1`** (`docker inspect`), and neither compose file sets `stop_grace_period`. So a
bare `docker stop` without `-t` gives the shard **1 s**, not the 10 s the brief assumed. Where the 1 comes from is
unverified.

### B.4 The change

`SaveOnShutdown.Configure` registers `PosixSignalRegistration.Create(PosixSignal.SIGTERM, ...)` (kept in a field,
because a collected registration unregisters itself) and prints
`[SaveOnShutdown] listening for SIGTERM: a stop saves the world first (D36)`.

On SIGTERM:
- If the server has crashed (tracked through `EventSink.ServerCrashed`), is already closing, or `!World.Running`, it
  returns and the default handling is not cancelled. That is "nothing different on a crash".
- Otherwise it sets `Cancel`, and only the first SIGTERM does anything after that. It posts `SaveThenStop` to the
  loop. `SaveThenStop` prints the "before" line, calls `World.Save()` (a no-op if a save is already under way; the wait
  then covers that save), waits on the thread pool with `WaitForWriteCompletion`, prints `...saved in N ms`, and calls
  `Core.Kill()`.
- A watchdog: if the loop has not started `SaveThenStop` within 5 s (a hung loop), it prints that and calls
  `Environment.Exit(143)`, the exit code the default gives.

It logs with `Console.WriteLine`, not the logger, for the reason in B.1.

**Not exercised: the crash guard, the hung-loop watchdog, a second SIGTERM, and a SIGTERM that arrives mid-autosave.**
I read them; I did not run them.

### B.5 The risk this adds, which is Chase's to decide before a live deploy

A save moves the old save into `Backups/` and the new one into `Saves/` **file by file**
(`AutoArchive.Backup` into `PathUtility.MoveDirectoryContents`, `Server/Utilities/PathUtility.cs:94-124`). A SIGKILL
during either move leaves `Saves/` empty or half-filled.

- Today that happens only when a stop lands inside an autosave write.
- With the fix, **every** stop writes. The console always passes `-t 60`, which is enough for a 32 s write. But a bare
  `docker stop` (1 s) or a compose recreate during a deploy (compose's own timeout, unmeasured for a live-sized world)
  can land in that window.
- **Recommendation, not made because it is outside P10's files:** add `stop_grace_period: 90s` to the service in both
  `docker/uo/docker-compose.yml` and `docker-compose.test.yml`, recreate, and confirm `StopTimeout` is 90 with `docker
  inspect`. The same edit also makes today's stops safer against the autosave window. Until that is done, T-028 should
  not be run by anything but the console.

### B.6 Proof (test shard only)

1. **Red** (`p10-red`, no fix): a marker was placed at 21:22:03Z, 3 minutes before the next autosave. `docker stop -t 60`
   followed, then a start. `markers in the loaded world: 0`.
2. **Green** (`p10-green`): a marker was placed at 21:26:53Z, after the 16:25:00 autosave. `docker stop -t 60`: saved in
   498 ms, exit 0. On start: `markers in the loaded world: 1 [P10 marker 212653]`. The same run also found `212258`,
   which was placed at the red build's second start and taken by the 16:25:00 autosave. That fits the timeline.
3. The markers were then deleted and that deletion saved on a green stop (273 ms), so the test world holds no probe
   items.
4. On the final image (the tree without the probe), the **console's** `test.stop` ran `compose down` and the shard
   saved (299 ms, `Shutting down` after). `test.start` brought it back up.
5. Gates: every build.sh run passed its patch gate and **258 shard tests**. `p10-red`, `p10-green` and the final
   `latest` all printed the same 108 `Item.Amount <= 0` lines from the test run, so those are not P10's.

### B.7 Wording

The console now says `The shard saves on stop (D36 fix, seen in its log since this start). If the stop times out,
play since the last autosave is lost.` for a container whose log since its start has the registration line
(`Test-SavesOnStop`, `:368`; state `:950`; plan `:623`). Otherwise it keeps the old warning and its `BEFORE YOU TYPE`
preface. I chose the log over the image because the running process saying it listens is proof, while an image name
proves nothing (D29, D37). The line and `SaveOnShutdown.RegisteredLine` must change together; both say so. The live
tab's blurb no longer claims a stop does not save. Fact `AShardWhoseLogSaysAStopSavesGetsThatWordingAndNoWarningFirst`
(`Tests.ps1:879`) was red before the change ("live says it saves") and green after.

The console's live stop text still says `docker stop, waiting up to 60 seconds for a save in progress to finish`.
**B.1 shows that is false on any image without the fix.** I left it, because it is outside D36's wording list; it
should become "and up to 60 s for the save on stop".

## Docs touched

- `docs/bug-list.md`: D38 marked fixed (D37's style), with the `Object[]` finding. D36 marked fixed on test, not on
  live, and its wrong 1.00 s and "`-t 60` lets a write finish" statements corrected.
- `docs/client-test-queue.md`: **T-028** added (highest was T-027): a live stop saves. Nothing was marked passed.

## State left behind

- The test shard was **stopped at 16:11 by me**, not knowing that P9's session had just recreated it for Chase's
  client checks. It was started again at 16:12 on the same container. It then ran `p10-red`, `p10-red2`, `p10-green`
  and finally `sl-modernuo:latest`, rebuilt at 16:37 from the working tree, which is **P9's uncommitted work plus
  P10**. Its save (`Saves-test`) was kept throughout, so P9's test characters are there.
- `sl-modernuo:latest` moved at 16:37. Live runs `uo-modernuo` and was not touched. The three `p10-*` tags are removed.
- Nothing in `dist\`. The scratch builds, servers and extracts are gone.

## Checklist for Chase

- [ ] **Live first:** decide the `Delete the object and continue? (y/n/a)` prompt on `sl-modernuo` (section 0).
- [ ] 0. Re-run test **Rebuild through the gates and start** from the console and read the output (D38). I ran it
      headless at 16:33 and it passed; your run is the one in the form.
- [ ] 1. Build and publish the player package: `.\player-package\Build-PlayerPackage.ps1`, then
      `D:\UO\haven-migration\Publish-PlayerPackage.ps1`. The new version stamp means the outside computer's 1331
      install sees a **real** update, which settles T-021. Expect the new download line, a bar, and "0 to add, 3 to
      replace" (the T-021 probe above).
- [ ] 2. The D36 fix reaches live only with the next shard deploy. **Before that deploy,** decide section B.5 (a
      `stop_grace_period` in both compose files). After it, run T-028.
- [ ] Commit, with `Commit-ShardWork.ps1`: P10's files are `player-package/payload/app/Play.ps1`, `Update.ps1`,
      `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`, `server/customizations/Misc/SaveOnShutdown.cs`,
      and here `docs/bug-list.md`, `docs/client-test-queue.md` and this note. The P9 files in the same tree are P9's.
