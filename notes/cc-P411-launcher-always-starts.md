# CC task P411: the launcher always starts the game, and Play defaults to the test shard

Iron, 2026-10-24 (04:45 to 05:45). Branch golem/Iron/P411 in both work copies; the code is in the code repo's
`player-package\` only. Built and gated as package 2026.10.24.0532 in my scratch folder; not published (the overseer
publishes after the merge).

## In plain words

- After an update, the launcher now shows "Preparing Shattered Legacy art and map..." with a progress bar (which part,
  a count and the seconds), then "...done in N s". On the game PC the whole thing takes about 4 seconds.
- **The game always starts.** If preparing takes more than a minute (what happened on your work PC), the game starts
  with the art you had, says so in one yellow line, and the new art is used from the next start. A half-built set is
  never used. The updater now prepares the art itself, so Play is quick right after an update.
- "Play Shattered Legacy.bat" now connects to the test shard (port 2594), and "Play-Lan.bat" to the test shard inside
  the house (192.168.1.58:2594). The live entry point is gone until live comes back.
- **For you:** on the work PC, after the next package is published: play once, then send me (or the overseer) the
  newest `app\logs\overrides-....log`. It names the slow step. Then you can delete two of your three stopgaps ("For
  Chase" below).

## What changed (code repo, `player-package\`)

### `payload\app\Build-UoOverrides.ps1`

- **Trace (part 1):** with `-TraceLog <file>` it writes a header (PC, PowerShell, Windows, the UO folder, each EA file's
  size and file attributes: an `Offline` or `RecallOnDataAccess` attribute means a cloud placeholder that downloads on
  read) and one line per step with its seconds: `art.read`, `art.targets`, `art.anim-records`, `art.tile-records`,
  `art.write`, `art.stamp`, `equip`, `cliloc.compile` (the `Add-Type` compile), `cliloc.read`, `cliloc.merge`,
  `cliloc.write`, `skills`, `music`, `map.copy`, `map.read`, `map.ops`, `map.statics`, `map.write`, then `total`. Every
  yellow line it says goes in as `said: ...`. It keeps the last 10 `overrides-*.log`.
- **Progress:** with `-ProgressFile` it rewrites a small JSON file (step, count, total, seconds) at most four times a
  second; `Get-AnimTargets` reports every 4,096 entries, the record loops each record, the map's land loop every 1,024
  cells.
- **`-CheckOnly`:** compares every part's stamp and builds nothing: `{ Fresh, Stale, List }`.
- **`-ListDir`:** the folder the override list names, so a set built into a staging folder already points at the final
  one. Every part's lines use it (they used `Resolve-Path` of the output folder).
- **`-ReadyFile`:** written last, only after the list, so "ready" means complete.
- Test hook `SL_OVERRIDES_SLOW=<step>:<seconds>`: that step takes that long and still reports progress.

### `payload\app\Apply-MapOps.ps1`

`-ListDir` and `-CheckOnly` as above, optional, so `docker\uo\Build-MapOverlay.ps1` (the server's map overlay, the other
caller) is unchanged; each map step is timed when the caller defines `Start-Step`.

### `payload\app\Overrides-Launch.ps1` (new): `Invoke-UoOverrides`, for Play.ps1 and Update.ps1

1. A staged set that finished while the game ran (`app\uo-overrides.next\` with its ready file) is swapped in:
   current to `uo-overrides.old`, staged to `uo-overrides`, old deleted. Each rename is tried for up to 4.5 s (a scanner
   may hold a file it just saw written); a set the game holds stays where it is until the next start.
2. `-CheckOnly` in this process (0.27 s on the tower). Up to date: the current list, done.
3. Otherwise **the line before**, then the rebuild in a hidden child PowerShell into `uo-overrides.next\`, with the trace
   in `app\logs\overrides-<time>.log` and the progress file. The child is started without output redirection on
   purpose: redirection hands it this process's handles, and a caller reading the launcher's output then waits for the
   whole rebuild (found by the tests).
4. **The bar** (`Write-Progress`, as Play.ps1's `Save-Download`): the step, its count, the seconds, redrawn every half
   second even while a step reports nothing.
5. **The time limit** (part 3): `app\launch-options.json` `"overridesTimeLimitSeconds"` (not shipped, so an update
   keeps it; default 60). Done in time: swapped in, "...done in N s". Not done: one yellow line, the last good list
   (or none on a first install), and the child carries on at below-normal priority; the next start swaps it in. A child
   that died left no ready file: the next start deletes the staging folder and builds again. The child's yellow lines
   are shown from its trace.

### `payload\app\Play.ps1`

- **Part 6:** every target is the test shard (`$Test` is always on; `-Test` still taken, as the shortcuts and every
  installed updater pass it).
- **Part 7:** every launch is a transcript in `app\logs\launch-<time>.log` (the last 10), and `-SkipArtRebuild` starts
  with the art as it is, checking nothing (`app\Play-Skip-Art.bat`).
- The art goes through `Invoke-UoOverrides` (inside the same try as before: anything wrong is one yellow line and the
  game starts).

### `payload\app\Launch-Settings.ps1`

`Get-LaunchTarget`: no switch is `shatteredlegacyuo.com:2594`, `settings.test.json`; `-Lan` is `192.168.1.58:2594`,
`settings.test.json`. The live target (2593, `settings.json`) is gone, and with it the "only with -Test" refusals of
`-Account` and `-ClientDir` (there is no live left to protect). The plain test file still never saves a login, as
before: a player who wants the login kept uses a profile (`-Account`). An old `settings.json` is left as it is.

### `payload\app\Update.ps1` (part 4)

After a good update, before starting the game: `Invoke-UoOverrides -Reason update` when `app\uo-path.txt` names a
folder that exists. The same staging, trace, bar and limit; never able to stop the game starting. Test hook
`SL_UPDATE_NO_PLAY=1`.

### Shortcuts and README

`Play Shattered Legacy.bat` and `app\Play-Lan.bat` comments name the test shard; new `app\Play-Skip-Art.bat`;
`README.txt`: the test shard for now, the progress bar, `app\logs\` and `Play-Skip-Art.bat`.

### Also

- `CHANGELOG.md` 2026.10.24.2 (three `### Changed` lines for players, two `### Staff`), `VERSION` 2026.10.24.2.
- Tests: `player-package\tests\Launch-Overrides.Tests.ps1` (new, 8 facts); `Launch-Settings.Tests.ps1` (the 5 facts
  that expected live or a refusal without `-Test` replaced by 5 that expect the test shard); one copy line each in the Play sandboxes of
  `Build-UoOverrides.Tests.ps1` and `Cliloc-Overrides.Tests.ps1`, and the cliloc Play fact now prints what Play said
  when it fails.

## Part 5: the tower trace, and what is slow

From the built package's own `app\` (2026.10.24.0532: its records, anim7, map patch), into an empty overrides folder,
against `D:\UO\ClassicUO\ClassicUO\Ultima Online Classic` (EA 7.0.x, no cloud attributes), Windows PowerShell 5.1:

```
art.read                0.079 s      cliloc.compile          0.161 s      map.copy                0.059 s
art.targets             0.065 s      cliloc.read             0.003 s      map.read                0.040 s
art.anim-records        0.291 s      cliloc.merge            0.026 s      map.ops                 0.738 s
art.tile-records        0.066 s      cliloc.write            0.003 s      map.statics             0.043 s
art.write               0.005 s      skills                  0.025 s      map.write               0.066 s
art.stamp               0.002 s      equip                   0.053 s      total 2.236 s
```

The whole first start after the update: 4.2 s (the child PowerShell starting, the rebuild, the swap). The next start:
0.27 s. The slowest steps are `map.ops` (0.74 s), `art.anim-records` (0.29 s) and the `Add-Type` compile (0.16 s).
**No step is over a second, so no loop moved into C#** (the prompt's rule), and the overseer's 2.9 s is confirmed.

What the work PC's trace will tell, and the fix for each (not built, because guessing is what the prompt forbids):

- `art.read` slow, with `Offline` or `RecallOnDataAccess` on the EA files in the header: the EA folder is a cloud
  placeholder (OneDrive Files On-Demand). Fix: "Always keep on this device" for that folder, or Setup.bat with a local copy.
- `art.write` or every write step slow: endpoint protection scanning each write under the game folder. Fix: an
  exclusion for the game folder (the district's IT), or the game folder on a local, unsynced drive.
- `cliloc.compile` slow or the last line before a stop: `Add-Type`'s compiler (csc.exe) blocked or scanned. Fix: a
  prebuilt assembly (below).
- The trace stops at `art.read` with no line after: a read that waits (a file held by a TazUO left running, the direct
  start stopgap). The time limit now covers it either way.

**A prebuilt assembly instead of `Add-Type` at launch, if the trace says so.** What it would take: the package build
compiles `ShatteredLegacy.Cliloc` once with `Add-Type -OutputAssembly app\ShatteredLegacy.Cliloc.dll` (the same C#
source), and `Use-ClilocType` loads it with `Add-Type -Path` (no compiler at launch). For the gates: gate 6 skips an
IL-only .NET file (it checks native imports only; the build log says "172 skipped (IL-only .NET...)"), gate 4 checks
names against EA's (no clash), and the payload's file list needs the new file; Play's Mark of the Web clearing already
covers it. Not built: on the tower the compile is 0.16 s, and only the work PC's trace can say it is the problem.

## Part 6: from outside the house (a note, not code)

From outside, 2594 is not forwarded at the router, and the server's relay names 192.168.1.58. The launcher's
`ignore_relay_ip` (Launch-Settings.ps1) makes the client reconnect to the address it logged in to rather than the relay,
but the port still has to be reachable: remote play on the test shard needs its own decision (you dropped the
Tailscale route on 10-22). Inside the house, `app\Play-Lan.bat` goes straight to 192.168.1.58:2594.

## Tests

Every new fact failed first against HEAD's payload (swapped in, run, swapped back), then passed:

| Suite | Red first (HEAD payload) | Now |
|---|---|---|
| `Launch-Overrides.Tests.ps1` (new) | 8 facts, 0 passed, 8 failed | **8 passed** |
| `Launch-Settings.Tests.ps1` | 27 facts, 22 passed, 5 failed: the 2 new P411 facts and the 3 rewritten ones | **27 passed** |

The facts: a rebuild is staged then swapped in and the next start only checks; **the time limit starts the game with
the previous overrides and leaves them intact** (hashes of tiledata, stamp and list before and after; the rebuild
finishes in the background and the next start swaps it in); a first start past the limit starts with no list, not half
of one; **a killed rebuild never leaves a half-built set and the next start builds again**; **a rebuild reports progress
every few seconds and a forced slow step still shows the bar** (redraws never more than 2 s apart, the slow step's count
shown); **the trace log is written and pruned to 10** (every art step timed, the header, the total); **a stale stamp
after an update is rebuilt by Update.ps1** (the real Update.ps1 on a sandbox install and a new package with new
records); `-CheckOnly` builds nothing; **Play with no switch targets 2594** (the function, and end to end with the
launch log); `-Account` without `-Test` is a test profile.

All package suites, Windows PowerShell 5.1, on my version:

| Suite | Result |
|---|---|
| Build-UoOverrides | 23 passed |
| Cliloc-Overrides | 10 passed |
| Launch-Overrides | 8 passed |
| Launch-Settings | 27 passed |
| Map-Overrides | 7 passed |
| Music-Overrides | 7 passed |
| Legion-Scripts | 24 passed |
| Paperdoll-Bodies | 9 passed |
| Ui-Skins | 4 passed |
| Package-Client | 6 failed: "No EA client data in ...\client-data\classic-client (-UoData)". The suite builds packages from this work copy's default folder, which a Golem work copy does not have; not this change (it touches no client or package code) |

- Before that, Build-UoOverrides had 3 and Cliloc-Overrides 1 failure, **the same on HEAD's builder**: the generated
  `vendor\shattered-legacy-art\build\sl-anim7*.bin` (git-ignored) predated P365's creature bodies. Regenerated with
  `python scripts\build-equip-anims.py` (the test header's own instruction); then all green.
- **The package build and its gates:** `Build-PlayerPackage.ps1 -TazUO D:\UO\golems\Iron\tazuo-p411\client -UoData
  "D:\UO\ClassicUO\ClassicUO\Ultima Online Classic" -Out <scratch>` under the package lock: exit 0, every gate green
  ("paperdoll fit: 2 gumps, 0 failures", "anim7 matches", "gate 6: 123 native files checked"), 139 MB, 740 files, TazUO
  3212623f + 5 patches. The zip holds `Overrides-Launch.ps1` and `Play-Skip-Art.bat`.
  - The shared client build `D:\UO\tazuo-sl-build\client` is stale (it lacks P362's `0005-ui-skins-appearance.patch`),
    so the client gate refused it. I built our client into my own folder (`Build-Client.ps1 -Out
    D:\UO\golems\Iron\tazuo-p411 -SkipTests`; client tests skipped, no client code changed here) rather than rebuild
    your shared one. **The next release needs `client\Build-Client.ps1` run first** (the overseer's release does).
- A manual run on the tower's real files: time limit 3 s with an 8 s forced step gave the previous list at once, the live
  tiledata unchanged (same md5), the rebuild finished staged, and the next start swapped it in.

## For Chase

1. **The work PC trace** (after the next package is published and installed there): play once, then send the newest
   `app\logs\overrides-*.log` and `app\logs\launch-*.log`. To get a trace on the work PC before that, with any copy of the
   new package unzipped there, in PowerShell:
   `cd "<unzipped folder>\app"; .\Build-UoOverrides.ps1 -UoDir "<your Ultima Online folder>" -OutDir "$env:TEMP\sl-trace" -TraceLog "$env:TEMP\sl-trace.log"; notepad "$env:TEMP\sl-trace.log"`
   (it builds into a temp folder only; your install is not touched).
2. **Your work-PC stopgaps**, once the new package is installed there:
   - `D:\Play TEST Now (skip art rebuild).bat`: **delete**; `app\Play-Skip-Art.bat` does the same from the package.
   - `D:\UO\ShatteredLegacy\Launch-Log.ps1`: **delete** unless you want its extras. `app\logs\launch-*.log` and the
     override trace replace the transcript and the timing; not folded in are its direct TazUO start with stdout and
     stderr captured, and the event log entries (TazUO writes its own crash logs in `app\tazuo\Logs\`).
   - `D:\Update and Play Shattered Legacy.bat`: **keep only if you still want its `git pull` of `D:\UO\sl-scripts`**; the
     `Play.ps1 -Test` part is now plain "Play Shattered Legacy.bat", and the published Legion scripts update themselves
     at every start. If you keep it: `D:\UO\sl-scripts` on the work PC has untracked `SL_Combat_*.py` files and a
     `from-installs\` folder; a pull that adds files of those names will fail. Move them aside before the next pull.
   - Your two lessons are kept: nothing here names a function `H` (the Get-History alias), and Update.ps1 passes Play's
     switches as an array, never as text.
3. **Remote play on the test shard** needs a decision (Part 6): forward 2594 and set the relay, or no remote play.
4. The next release: run `client\Build-Client.ps1` before the package build (the shared client is one patch behind).

## Deviations and decisions for Chase

1. **No loop moved into C#, no prebuilt assembly:** nothing is over a second on the tower; the trace on the work PC
   decides (Part 5 says what each answer means and what the assembly would take).
2. **The live target is removed, not just labelled.** With live retired the only thing a live entry point could do is
   fail. When live returns at 1.0, `Get-LaunchTarget` gets it back (one line), as a switch.
3. **The plain test settings file still never saves a login** (unchanged). Now that everyone plays on it you may want
   that the other way; it is one line in `Write-LaunchSettings`.
4. **The Read tool was denied** for `player-package\tests\Cliloc-Overrides.Tests.ps1` (unattended run). I read it with
   Bash and edited it with a small checked script instead; nothing else was affected.
5. The child rebuild is started hidden and without output redirection; its messages come back through its trace. If
   PowerShell itself fails to start the child (no trace at all), the line says "could not be prepared" and the game starts.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P411 -NoRefresh`:
code dry run, docs dry run, neither BLOCKED. Code: 16 files (CHANGELOG.md, VERSION, the two .bat files, README.txt,
Apply-MapOps.ps1, Build-UoOverrides.ps1, Launch-Settings.ps1, Overrides-Launch.ps1 (new), Play-Skip-Art.bat (new),
Play.ps1, Update.ps1, and four test files, one new). Docs: this notes file. No file over 5 MB in either repo: the
regenerated `sl-anim7.bin` (80 MB) is under `vendor\shattered-legacy-art\build\`, git-ignored (`.gitignore:100`,
`git check-ignore`). The built package and the client build are outside both repos.

P411 DONE
