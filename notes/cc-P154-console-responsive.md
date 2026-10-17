# cc-P154: Keep the Shard Console responsive (background refresh)

2026-10-17. Opus. Chase, 13:10: "right now console is a little unresponsive". The quick fix only: no redesign, no new
features, the same layout and behaviour. Everything is in `D:\ShatteredLegacy\scripts\Shard-Console.ps1` and its facts.

## Headlines

- **The window opens in about 1.8 s instead of 43 s.** 26 of the build's 29 s went into one loop: the World setup tab's
  table laid itself out again on every `Controls.Add` (about 200 controls). It is laid out once now, and under the
  console's own start the tab is built the first time it is opened, from registrations read in the background.
- **A 30 s refresh freezes the window for at most 92 ms (before: 3.0 s).** Docker, git, the processes, the Golem's files,
  play-tests.json, the VPN facts and the download site are read in a runspace of their own; the window only draws what
  comes back (40-60 ms). Never two at once: a tick that finds one running is skipped and counted.
- **Only the open tab's details are read**: the tiles always; the Commit tab's git only on the Commit tab (it was read
  every 5 s on the window's thread, 0.55 s each time); the package light's git and site GET on the Player package tab,
  or when two minutes old (the lights file must stay current); the Golem panel drawn only while its tab shows.
- **A button's read-only checks** (docker, git, dist\, the Golem's folder, this PC's adapters, the CLI sign-in check)
  run in a second runspace; the click carries on with them, dialogs and all, when they are back.
- **The per-second timers only count** from cached values: the VPN facts and the Commit facts are no longer read on them.
- **Three causes found by measuring, not guessed**: the World table's layout (26 s), line-by-line RichTextBox filling
  (4 ms a line; the Golem panel 0.8 s: now one RTF assignment, identical look, proved per character), and see-through
  themed controls repainting synchronously during a layout (a tile row 10 px taller held the window about 2 s, 0.19 s
  with the window's drawing turned off around it).
- **Still slow, once each**: the first opening of the World setup tab (about 1.0-1.3 s), of the Golem tab (0.3-0.5 s) and
  the first fill of the status (about 0.5 s). Each is WinForms making the controls of a page the first time, not a read.
- **Facts**: six new, each seen failing (nine breaks, all restored by hash). Full suite **362 facts, 357 passed, 5
  failed**: the same five that failed before this prompt (P133's baseline), all from this PC being in Haven mode since
  the ops cutover. Not green; see Deviations.
- There is no task-list tool in this session, so Chase could not follow a task list; progress was in the chat only.

## Timings (this PC, the real docker, git and files; the Enhanced look Chase uses)

Method: `scratchpad\measure.ps1` timed each source directly; `ui-probe.ps1` built the real form, showed it, and ran a
15 ms timer on the window's thread: the longest gap between two ticks is the longest the window could not answer.
"Before" is the console at the code repo's HEAD (`67c47fd`), run from a temporary copy in `scripts\`, deleted after.

### Where the window's thread was blocked (before)

| Source (read on the window's thread) | ms, three runs | When |
|---|---|---|
| `Get-ConsoleState` (docker) | 1297 / 999 / 1058 | every 30 s refresh, every button that reads the shard |
| `Get-PackageLightFacts` (git, the download site GET at most every 10 min) | 1014 / 828 / 922 | every refresh |
| `Get-RebuildFacts` (git, a process listing) | 854 / 670 / 817 | every refresh |
| `Get-PlayTestGlanceNow` (play-tests.json) | 462 / 419 / 372 | every refresh |
| `Get-AutopilotViewNow` (the Golem's files, every queued prompt's head, ten finished notes) | 249 / 99 / 78 | every refresh, and on opening the Golem tab |
| `Get-VpnFacts` (route, CIM, services) | 1201 / 253 / 283 | the 1 s timer, every 30 s |
| `Get-CommitFacts` (git) | 700 / 655 / 708 | the 1 s countdown, every 5 s while the Commit tab shows |
| Format-StatusReport, Invoke-QuestionMail (mail stubbed) | 60 / 4 / 2, 7 / 1 / 1 | every refresh |
| The 150 ms pane timer (`Update-PaneJob`) | under 1 | only drains a queue: left as it was |
| The 1 s network and websites ticks | 1 | their probes already ran in runspaces (cc-P52, cc-P101) |
| `New-ConsoleForm` (with the first refresh) | 42,913 | start; of which the World setup loop **26,139** (`profile-lines.ps1`) |

### Before and after

| What the window does | Before (HEAD) | After |
|---|---|---|
| Build the window | 43,203 ms (the first status inside it) | **1,575-1,823 ms**, first status drawn about 4-5 s later in the background |
| A 30 s refresh | longest freeze **3,049 ms** | longest freeze **46-92 ms**, 0 over 100 ms; read 1.9-2.2 s in the background, drawn in 40-59 ms |
| Commit tab open, 6 s of countdown | longest **546 ms**, 2 over 100 ms (git every 5 s) | **50-62 ms**, 0 over 100 ms |
| Golem tab open | longest **1,947 ms** | **331-522 ms** (the page's first show; its panel formatted in the background) |
| Player package tab open | (not measured before) | 164-202 ms (the page's first show) |
| World setup tab, first open | (built at the start: 26 s of the 43) | **1,022-1,298 ms**, once |
| 1 s timers with the VPN facts due | 44 ms | 42-51 ms (the VPN facts read in the background) |
| First status after the window shows | (inside the 43 s) | longest freeze 343-536 ms, once (its first tile fit) |

Per source after (one refresh, background): docker 942, rebuild light 582, vpn 244, golem 83 (with its panel's lines),
play tests 63; total 1,917 ms, none of it on the window's thread.

Target "no UI freeze over ~100 ms during a refresh": **met** (46-92 ms over five runs). The first opening of a page is
not a refresh and still freezes once; listed under For Chase.

## What changed (`D:\ShatteredLegacy\scripts\Shard-Console.ps1`)

| Where | What |
|---|---|
| `New-WorldSetupTable` :9443, `$worldTable.SuspendLayout()` :9465 | The World setup table in its own function, laid out once after every row is in (the 26 s) |
| `Show-WorldSetupPage` :9526, `Start-WorldCommandsRead` :9550 | Under `-BackgroundRefresh` the page says loading, its registrations (274 .cs files, parsed) are read in a runspace at the start, and the page is built and themed (suspended, drawing held) on first open |
| `$script:ConsoleScriptFile` :8340 ... `Update-ConsoleStatus` :8598 | The background refresh: `Get-ConsoleRefreshData` :8351 (every read, no window, timed per source, `Parts` tiles/golem/package/commit/vpn, never throws), `Show-ConsoleRefresh` :8397 (draws only), `Get-RefreshParts` :8444 (the open tab's), `Start-ConsoleJob` :8457 / `Receive-ConsoleJobs` :8481 / `Stop-ConsoleJobs` :8509 (one persistent runspace per slot, the console loaded there once with `-LoadOnly`, one job per slot, a 250 ms collector, 120 s abandon), `Start-ConsoleRefresh` :8518 (skip a tick while one runs; `-Queue` asks for one more after), `Update-ConsoleStatus` :8598 (starts one under `-BackgroundRefresh`; reads and draws inline for the facts' forms, as before) |
| `Get-ActionFacts` :8546, `Start-ActionPrecheck` :8576, `Invoke-ConsoleButton` :9239 (`-Prefetched`, :9261) | A click's reads in the background, then the click carries on with them; the same reads for the same keys as before |
| `Show-AutopilotView` :8235 | The Golem view's drawing split from its reading; the panel drawn only while the Golem tab shows; its lines formatted in the background |
| `Update-Lights` | `-Gathered`: draws from facts read elsewhere; with no package facts in a refresh the last package light stays |
| `Update-VpnButtons` :8693, `Update-CommitCountdown` :9133 | The 1 s ticks never read; they ask the refresh runspace and count from the last read ("Reading the repos..." until the first) |
| `Get-FileHeadCached` :5914, `Find-FileCached` :5928, in `Get-GolemExtra` and the finished list | Prompt and notes heads read again only when the file's write time or length changed; a folder listed again only when its write time changed |
| `ConvertTo-RichLinesRtf` :7758, `Set-RichLines` :7800 | The status box, the Golem panel and the Websites panel filled with one `.Rtf` assignment, then the exact fonts (RTF sizes are halves; the mono is 9.75) |
| `Suspend-WindowDraw` :8031, `Resume-WindowDraw` :8042 | `WM_SETREDRAW` through WinForms' own (non-public) `Control.SendMessage` by reflection, nothing compiled; held around a tile-row or column change in `Update-TileFit` :8136, the World page build, and a tab switch (`Add_Selecting` :10479, only the tabs repainted after) |
| `Get-TileFitFont` :8054, `Update-TileFit` | The fitted size remembered per text, font and box (500 kept); one fit per refresh drawn, not one per tile changed |
| `New-ConsoleForm` :9561 | `-BackgroundRefresh`; the 250 ms collector :10483; the tab handler shows the last view at once and asks for its reads; jobs stopped with the window. The entry passes it :10641 |

`CHANGELOG.md`: `## 2026.10.17.2`, one `### Staff` line (2026.10.17 was committed with P133); `VERSION` 2026.10.17.2.

Files created: none in the repos besides these edits. Scratch (outside both repos, in the session scratchpad):
`measure.ps1`, `profile-form.ps1`, `profile-lines.ps1`, `ui-probe.ps1`, `draw-profile.ps1`, `draw-first.ps1`,
`draw-tf.ps1`, `grid-test.ps1`, `world-steps.ps1`, `rtf-test.ps1`, `mutate154.py`, the patch specs, and the HEAD copy
of the console. The temporary `scripts\zz-p154-head-console.ps1` was deleted right after the before-run (`git status`
clean of it).

## Tests

`scripts\tests\Shard-Console.Tests.ps1`, six new facts (:6438-6591) and four helpers (`New-P154Form`, `Close-P154Form`,
`Wait-P154`, `Get-P154Controls`):

| Fact | Proves | Seen failing by |
|---|---|---|
| `P154_TheRefreshNeverRunsOnTheWindowsThread` | a stub source that sleeps 2 s: the build does not wait, the window's 15 ms timer keeps ticking (40+ ticks, longest gap under 500 ms), the stub ran on another thread, its result is drawn | waiting for the job on the window's thread: "ticked 1 times while the source slept 2 s" |
| `P154_NeverTwoRefreshesAtOnce` | a tick while one runs is skipped and counted, asks nothing more; a click queues one, which starts after the first ended | both busy checks removed: "A pipeline is already running" |
| `P154_OnlyTheVisibleTabsSourcesRun` | the parts per tab (Test shard, Commit, Player package, Golem, package facts two minutes old); `Parts tiles` reads docker, golem, rebuild light, play tests and nothing else; the Golem panel drawn only while its tab shows | every tab reading the Commit git ("expected [tiles,vpn] but got [tiles,vpn,commit]"); and the panel drawn on every tab ("expected [untouched]") |
| `P154_TheFileCachesReadAgainOnlyWhenAFileChanges` | a head served from the cache while write time and length match, read again on a new write time or length; a folder listing again on a file added or removed | the head cache never invalidated; the folder cache never invalidated |
| `P154_APanelFilledInOneGoLooksAsLineByLine` | in Plain, UO and Enhanced, every character's color, bold, font and size, and the text, the same as Add-RichLine's | the last paragraph mark dropped; the exact fonts not set |
| `P154_TheWorldSetupTabIsBuiltWhenFirstOpenedAndOnlyThen` | loading at the start, registrations read in the background, built on opening, the same rows as the eager build | built with the window again |

Each break was applied to `Shard-Console.ps1`, the fact run alone, and the bytes restored and checked by SHA-256 (all
nine identical).

Full suite (Windows PowerShell 5.1), after the last edit to the console: **362 facts, 357 passed, 5 failed**:
P83_TheLinksOpenTheTwoPagesAndNothingElse, P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo,
P101_TheTileAndTheTabAreBuiltAndDrawn, P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing,
P107_LinksAndSitesPointAtHavenAfterTheCutoverAndAtThisPcBefore. P133's full run, before any P154 change, was 356 facts
with the same five failing (`expected [http://localhost:8093/] but got [http://192.168.1.61:8093/]`, `expected [pc] but
got [haven]`): this PC's real `D:\UO\haven-ops\state.json` says `haven`, and those facts expect this PC's sites. No
existing fact changed result. Python (`shard-migration\tools\tests`): 99 tests, the same 2 failures as before P154
(`test_play_who.RealFiles` on the play-test data in `testing\`); P154 touches nothing there.

## Deviations and decisions for Chase

1. **"Full suites green" is not met**, by five facts outside this prompt (above). The fix is test isolation: re-parse
   the sites in the facts' `New-P107Config` so this PC's real Haven mode does not leak in (the one line is in P133's
   notes, Deviations 1). That Read of the tests file was denied in the unattended P133 run with "do not retry another
   way", so I left it; P83 and P101 want the same kind of fix.
2. **The facts' forms keep the old, inline order** (`New-ConsoleForm` without `-BackgroundRefresh`): every existing
   fact reads the form right after building it. Only the console's own start passes `-BackgroundRefresh`. Both paths draw
   through the same `Show-ConsoleRefresh`.
3. **The package light's facts** are read on the Player package tab and otherwise at most every two minutes
   (`PackageFactsMaxAge` 120), not every 30 s, so the lights file the status page reads can be up to two minutes old.
4. **A second click while a button is still reading** is told to wait ("Still reading for X; click Y again"), not queued.
   A click shows "X: reading what its plan needs..." before its plan.
5. **The question email** is now sent from the refresh runspace (same function, same file of what was sent).
6. **Not done, still slow once each**: the first opening of the World setup tab (1.0-1.3 s), the Golem tab (0.3-0.5 s)
   and the first status fill (0.3-0.5 s): WinForms creating that page's controls and laying them out the first time, with
   the themed see-through controls. Building those pages differently would change the layout, which this prompt rules out.
7. Under the Enhanced look a layout change repaints the see-through controls synchronously, which is the root cost of
   the remaining first-open freezes. Worth knowing for the web console rebuild.
8. `WM_SETREDRAW` goes through WinForms' non-public `Control.SendMessage(int, int, int)` by reflection, so nothing is
   compiled at the start. If a .NET Framework update ever removed it, the holds quietly do nothing and the window is only
   slower again.

## For Chase

- **Before → after**: open 43 s → about 2 s; a status refresh froze it 3.0 s → under 0.1 s; the Commit tab stalled half a
  second every 5 s → never; the Golem tab 1.9 s → 0.3-0.5 s. Full tables above.
- **Still slow**: the first time you open World setup (about a second; it says "loading the world commands..." until its
  registrations are read), and the first time you open the Golem tab (about half a second). After that, tab switches are
  quick. The background read itself still takes about 2 s (docker 0.9, git for the rebuild light 0.6), but the window
  no longer waits for it.
- Restart the console to get it (the running one has the old code). Nothing to set.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

No file over 5 MB added; all scratch is in the session scratchpad, outside both repos.

P154 DONE
