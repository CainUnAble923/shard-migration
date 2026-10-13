# cc-P84: Shard Console polish (UO look, tooltips, cleanup, Action output pane)

Prompt: `D:\UO\cc-prompts\cc-P84-console-uo-skin.md`. Code repo `D:\ShatteredLegacy`; no shard build (a builder of
the console script and its tests only). Not committed (autopilot commits after DONE).

## Headlines

- **A UO look, switchable.** The UO look has stone and parchment backgrounds, gold-trimmed gump-style buttons, owner-drawn tabs, Palatino Linotype and the Shattered Legacy crest in a header. Plain is the console as it was.
  - Pick the look in the status bar ("Look: UO / Plain"). The choice is remembered on this PC.
  - The default is UO.
  - Every color and font is in one table, `Get-ConsoleTheme`.
- **Client gump art, never in git.** Gumps **3604** (stone) and **9304** (paper) are read once from `client-data\classic-client\gumpartLegacyMUL.uop` into the git-ignored `scripts\shard-console-cache\`.
  - When the client data is missing, the look falls back to its own drawn colors.
  - With the cache warm, startup is no slower than Plain. With an empty cache the first start adds about 0.13 s.
- **Tile states keep their meaning and contrast.** Green, amber, red and grey mean the same in both looks, and every tile's text measures at least 5.3:1. All UO text reaches at least 4.5:1, and that is checked on the art itself too.
- **A tooltip on every control.** 184 buttons, tiles, tabs, boxes and fields are checked by a fact. The texts live in one table, `Get-ConsoleTooltips`, keyed by action key or control name.
- **An Action output pane.** Non-interactive window actions and the two log tails now stream into the window instead of their own PowerShell window.
  - The pane has Copy, Clear, Stop (ends the whole process tree) and Show/Hide.
  - Output streams live with its colors and ends with the exit code. The window never freezes.
  - Two interactive actions always keep their own window: Wipe test accounts (it asks a password) and Publish (it asks "Type yes").
  - A setting sends everything back to separate windows.
- **Nothing a button does changed.** The same plans, refusals, phrases, dry runs and child command line are used; the pane form swaps `-NoExit` for `-NonInteractive` and nothing else.
- **Tests:** Pester stays green, **195 / 195**. That is the 181 old facts plus 14 new ones, which went red when the code was broken on purpose.

## What was built

All in `scripts\Shard-Console.ps1`, plus its test file:

- **CORE:**
  - `Get-ConsoleTheme` (UO and Plain).
  - `Get-RelativeLuminance` and `Get-ContrastRatio` (WCAG).
  - `Get-ConsoleTooltips`.
  - `ConvertFrom-ConsoleSettings` and `ConvertTo-ConsoleSettings`.
  - `$script:InteractiveActions` and `Get-OutputRoute`.
  - `Format-PaneLine`, `ConvertFrom-PaneLine` and `Format-PaneExit`.
- **SHELL:**
  - `Read-ConsoleSettings` and `Save-ConsoleSettings`.
  - A small C# helper (`ShardConsoleNative`). It is compiled only on first use: the first pane job, or a gump missing from the cache.
  - `Get-GumpImage`, `Set-ControlTheme`, `Set-TabTheme` and `Set-ConsoleTooltips`.
  - The pane: `New-OutputPane`, `Start-PaneJob`, `Update-PaneJob`, `Stop-PaneJob` and `Show-OutputPane`.
  - `Format-ArgumentList`.
- **Changed:**
  - `Get-ConsoleConfig` gained SettingsFile, CacheFolder, GumpFile and CrestFile.
  - `Get-ChildArgumentLine` gained `-ForPane`.
  - `Write-ConsoleLine` marks each line with its color in a pane child.
  - `Add-RichLine` and `Get-TileColors` read the theme.
  - `New-StatusTile` takes the theme's fonts and gets names for its tooltips.
  - `Set-ConsoleDryRun` uses the theme's colors.
  - `Invoke-ConsoleButton` routes to the pane.
  - The three dialogs take the theme.
  - `New-ConsoleForm` gained `-Theme`, `-Pane` and `-Settings`, plus the header, the settings controls, control names, shorter captions, the pane and the tooltips.
  - The entry point reads the settings.
- **Other files:**
  - `.gitignore`: `scripts/shard-console-settings.json` and `scripts/shard-console-cache/`.
  - `CHANGELOG.md`: a 2026.10.13.6 `### Staff` line.
  - `VERSION`: 2026.10.13.6.
  - `design\console-uo-skin\`: the screenshot script and screenshots.
- **The facts' own forms are Plain with no pane.** They are built without `-Theme` or `-Pane`, so every existing form fact sees the console as it was. Only the entry point (a normal start) passes the setting.

## The theme table (`Get-ConsoleTheme`)

| Field | Plain (the old look, value for value) | UO |
|---|---|---|
| Fonts | Segoe UI 9; tiles Segoe UI 13 bold; Consolas 9 | Palatino Linotype 9.75; tiles 11.5 bold; title 17 bold; Consolas 9 |
| Tile green (back / text) | 222,244,226 / 20,100,40 | 214,232,200 / 24,84,30 |
| Tile amber | 255,238,204 / 150,80,0 | 246,226,180 / 122,62,0 |
| Tile red | 250,218,218 / 150,20,20 | 240,206,196 / 128,20,16 |
| Tile grey (any other state) | 234,234,234 / 80,80,80 | 220,212,196 / 70,62,52 |
| Line box back | white | 246,238,218 |
| Lines normal, head, green, amber, red, gray | Black, Navy, ForestGreen, DarkOrange, Firebrick, DimGray | 40,28,16; 24,40,110; 24,100,30; 138,74,0; 150,22,18; 92,82,70 |
| Chrome | none (WinForms defaults) | stone 46,44,42 with text 238,226,196 and gold 232,196,104; page 230,206,160 with ink 60,38,20, dim 72,54,34, warning 112,16,12; button 92,70,44 with text 246,226,170, hover 118,92,58, border gold; field 250,244,228 with text 40,28,16 |
| Gumps | none | Stone 3604, Parchment 9304 |
| Header | no | crest + "Shattered Legacy - Shard Console" in gold, gold trim |

## Gump IDs, extraction and cache

- **3604:** the middle tile of the dark stone background, 3600-3608 (128 x 128). It is tiled behind the window and header.
- **9304:** the middle tile of the paper background, 9300-9308 (240 x 240). It is tiled behind the tab pages.
- **Tried and not used:** 9270-9278 (our gumps' bluish stone), 3500-3508 (grey scroll), 9200, 9350, 2604 and others. I rendered a contact strip and picked the warmest stone and paper.
- **Extraction (C#, ported from TazUO at 3212623f, BSD 2-Clause):**
  - `UOFileUop.CreateHash` locates the file entry in the UOP.
  - zlib inflate, then `BwtDecompress` (flag 3).
  - The gump run-length format, decoded to a 32-bit bitmap.
  - Each gump takes about 20 ms. The compile takes about 290 ms and happens only when the cache is empty.
- **Cache:** `scripts\shard-console-cache\gumps\<id>.png`, git-ignored, as is the screenshots folder beside it:
  ```
  .gitignore:89:scripts/shard-console-settings.json   scripts/shard-console-settings.json
  .gitignore:90:scripts/shard-console-cache/          scripts/shard-console-cache/gumps/3604.png
  ```
- **Fallback:** with no client file and no cache, `Get-GumpImage` returns null and the theme's solid colors (the art's average colors) are drawn instead. The fact `P84_AUOFormIsThemedAndFallsBackWithoutTheClientArt` builds a UO window that way.
- **Delete-and-restart, the real console with `-DryRun`:**

  | Look, cache | Window up after | Cache afterwards |
  |---|---|---|
  | Plain, empty | 14,653 ms | (none) |
  | UO, empty | 14,786 ms | 3604.png, 9304.png, rebuilt |
  | UO, warm | 14,575 ms | |

  Both looks start in about 14.6 s. That time is the status read from the capture, as before; UO adds at most 0.13 s. The fact `P84_TheUOLookAddsUnderASecondToTheStart` builds the window in both looks and asserts the difference is under 1 s.

## Fonts

Palatino Linotype ships with Windows (Vista and later). It is a book serif close in spirit to the UO client's gump text, and it stays legible at 9 to 10 points. Book Antiqua is the same family but narrower, and Georgia is wider and more modern. Consolas stays for the output, status and pane boxes, which are columns of text.

Tile words use 11.5 point type: at 13 points the serif clipped "PLAY TESTS: 111 OPEN". The long words ("STATUS PUBLISHER: UNKNOWN") already clip at the 1,200 pixel default width in Plain, so that predates this task.

## Contrast results (WCAG, from `P84_*` facts; 4.5:1 is the floor)

- **Tiles:**
  - Plain: green 6.29, amber 5.33, red 6.69, grey 6.70.
  - UO: green 6.98, amber 6.54, red 7.08, grey 7.13.
- **UO lines on their box:** normal 14.37, head 11.59, green 6.30, amber 5.93, red 7.50, gray 6.60.
- **UO chrome:**
  - stone text on stone 10.80, gold on stone 8.30
  - page ink 9.26, dim 7.50, warning 7.75
  - button text 6.92, button text on hover 4.87
  - field text 15.13
- **On the art itself.** Each pair is measured against the gump pixel nearest in color to the text drawn on it: stone text 6.88, gold 5.29, page ink 6.59, dim 5.34, warning 5.51.
  - Two first tries failed and were fixed: gold 201,162,74 gave 3.69 on stone, and the dim and warning inks gave 4.12 and 4.32 on parchment.
- **Plain's own line colors are unchanged, and two are below 4.5:** DarkOrange amber is 2.33:1 and ForestGreen is 4.39:1 on white. Plain must look exactly as before, so they stay; see Decisions.

## Where each action runs now

With the default setting (pane):

| Action | Where |
|---|---|
| test.start, test.fresh, test.stop, test.rebuild, test.deploy | pane |
| live.start, live.stop, live.restart | pane (the typed phrase is still asked by the console's dialog first) |
| snapshot.create, snapshot.restore, snapshot.delete | pane |
| diag.docker, diag.shard | pane |
| commit.preview, commit.run | pane (commit.run's phrase is asked first, as before) |
| package.build, package.check | pane |
| test.tail, live.tail | pane (`docker logs -f`, ended by Stop) |
| **test.wipe** | **own window, always**: `Read-WipePassword` reads the new admin password with `Read-Host -AsSecureString`, twice |
| **package.publish** | **own window, always**: `Publish-PlayerPackage.ps1` line 70, `Read-Host '... Type yes'` |
| test.client, live.client, diag.folder, autopilot.queue, autopilot.log, links.* | in the console, as before (they only open something) |
| snapshot.list | in the console output, as before |
| autopilot.on, .off, .email, .test | as before: each opens the autopilot's own script in a window of its own (Setup-Email asks a password there) |

How the routing was decided, and how it is guarded:
- **Decided from the code.** Start-TestShard.ps1, Check-Docker.ps1, Check-Shard.ps1, Commit-ShardWork.ps1 and Build-PlayerPackage.ps1 contain no Read-Host, PromptForChoice, Get-Credential, ReadKey or `-it` docker call. Every typed phrase and yes/no is asked by the console's own dialog before the run and passed as `-ConfirmLive` / `-Yes`.
- **Pinned by a fact.** `P84_InteractiveActionsNeverGoToThePaneAndTheRestOnlyWhenAsked` covers the routing for every action and both settings, and greps those scripts for prompts.
- **A second guard.** A pane child runs with `-NonInteractive` and with stdin closed, so a prompt fails instead of hanging.
- **A busy pane** (one job at a time) sends the next action to a window of its own, and the console says so.
- **Stop** runs `taskkill /PID <n> /T /F`: the PowerShell child and everything it started, including docker CLI processes. The fact `P84_StopEndsTheWholeProcessTree` proves the child's own child (ping) dies too.
- **Closing the console** ends a running pane job.

## Screenshots

| What | Where |
|---|---|
| Plain, and UO drawn without client art (our colors and crest only) | `D:\ShatteredLegacy\design\console-uo-skin\` (committed, no EA art) |
| UO with the gump art | `D:\ShatteredLegacy\scripts\shard-console-cache\screenshots\` (git-ignored) |
| Script that takes them | `design\console-uo-skin\Take-ConsoleScreenshots.ps1` |

Each look has 13 shots:
- the main window on each of the 8 tabs (`*-tab-N-*.png`)
- every tile state (`*-tile-states.png`)
- a tooltip (`*-tooltip.png`, from the screen)
- the pane running Rebuild through the gates under DRY RUN (`*-pane-rebuild-dry.png`)
- the pane mid-stream (`*-pane-streaming.png`)
- the pane after Stop (`*-pane-stopped.png`)

How they were taken:
- The windows are built from the capture fixture, as `-DryRun`.
- Shots come from the screen: `DrawToBitmap` leaves a RichTextBox blank.
- The 27 committed files total 2.0 MB; the largest is 92 KB.

Deviation: the prompt asks for the pane "streaming a build". This task's own rule is no shard build, so the pane shot shows Rebuild through the gates as a dry child, which prints its plan. A separate shot shows a 40-line, 120 ms-apart stream caught mid-run.

## Cleanup

Safe changes, done here. None changes an action or what it does.
- **Captions cut to what a person needs at a glance:**
  - Test shard: kept "START FRESH and WIPE TEST ACCOUNTS are different", which a fact pins.
  - LIVE shard: removed the D29 and D36 codes.
  - Diagnostics, Commit (kept the autopilot sentence a fact pins), Player package, Autopilot, World setup.
- **Jargon moved into tooltips:** cc-P numbers, D-codes and script paths.
- **Button wording:** "Run Check-Docker.ps1" is now "Check Docker", and "Run Check-Shard.ps1" is now "Check the test shard". `-Action list` labels are unchanged.
- **Every tooltip is one to three plain sentences.** It says what the control does, whether it changes anything, and what it refuses. A fact checks there are no internal codes.

## Deviations and decisions for Chase

Proposed, not done. Each would remove, merge or change something:
1. **The LIVE shard tab and LIVE tile.** The prompt calls the live shard retired. Its five buttons (Start, Stop, Restart, Tail, Open a client), the LIVE tile and the LIVE snapshot radio are still there and still work. Remove them, hide them behind a setting, or keep them?
2. **Play tests and Dashboard appear twice** (in the PLAY TESTS tile and on the Autopilot tab, P83's choice). Keep only the tile's pair?
3. **Snapshots > List.** It prints what the list above it already shows. Remove it?
4. **Plain's amber and green output lines** are 2.33:1 and 4.39:1 on white. Plain must look exactly as before, so they were not changed. Darken them to UO's 138,74,0 and 24,100,30?
5. **The tab strip's empty area** beside the tabs is drawn by Windows in its own grey in UO. Coloring it needs a custom tab control. Worth it?
6. **The UO look is the default** (as the prompt says). The facts build Plain.
7. **The pane is one job at a time.** A second action while one runs goes to its own window. Queue them in the pane instead?
8. **Stopping a build.** Stop ends the docker CLI the build runs in; BuildKit cancels a build when its client goes away. That was not tested with a real build here (no shard build in this task).

Fixed along the way:
- `PlayerCommandsNeverAppearInTheWorldTab` was already red before this task (checked by running the suite against the untouched script: 180 / 181). Its list of player commands lacked `FanfareMute`, which P79 added. The name is now in the list.

## For Chase

- **Switch looks:** the status bar's "Look:" box (UO or Plain). It takes effect the next time the console opens. It is saved in `scripts\shard-console-settings.json`; deleting that file goes back to UO with the pane.
- **Use separate windows:** tick "actions in their own windows" in the status bar. It applies at once.
- **The pane:** sits beside the console's output, at the bottom. It opens by itself when an action starts. Copy, Clear, Stop and Hide/Show are on its bar.
- **The gump art:** read from your client data on the first start; delete `scripts\shard-console-cache\` to read it again. Without the client data the console draws its own colors.
- **Hover anything** for a tooltip.

## Tests

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1`

| Run | Result |
|---|---|
| Before this task (the untouched script) | 180 / 181 (`PlayerCommandsNeverAppearInTheWorldTab`, stale since P79) |
| First run with the new code | 2 failures. A shortened caption dropped a phrase a fact pins; restored. The stale fact above |
| With the 14 new facts | 1 failure at a time, each a color below 4.5:1 on the art (gold, then dim, then warning). All three fixed |
| **Red** | 7 deliberate breaks: a tooltip removed, UO amber line too pale, test.wipe taken off the interactive list, taskkill without /T, Plain's grey text changed, `-ForPane` keeping `-NoExit`, the pane never used by a click. **9 facts failed**, every one aimed at a break. Restored from a backup, `cmp`-identical |
| **Green** | **195 / 195** |

The 14 new facts:
- `P84_EveryActionHasATooltipOfOneOrTwoPlainSentences`
- `P84_EveryTileStateKeepsItsMeaningAndAt45ToOneInBothLooks`
- `P84_UOTextKeepsAt45ToOneOnEveryBackgroundAndOnTheArt`
- `P84_PlainIsTheOldLookValueForValue`
- `P84_APlainFormIsBuiltAsBefore`
- `P84_AUOFormIsThemedAndFallsBackWithoutTheClientArt`
- `P84_EveryControlInTheWindowHasATooltip`
- `P84_InteractiveActionsNeverGoToThePaneAndTheRestOnlyWhenAsked`
- `P84_APaneChildEndsByItselfAndMarksEachLineWithItsColor`
- `P84_StopEndsTheWholeProcessTree`
- `P84_ThePaneStreamsWhileTheWindowRunsAndAClickGoesThere`
- `P84_TheGumpCacheFillsFromTheClientOnceAndFallsBackWithoutIt`
- `P84_TheSettingsDefaultToUOAndThePaneAndABadFileFallsBack`
- `P84_TheUOLookAddsUnderASecondToTheStart`

The `-DryRun` starts, one in each look, are the delete-and-restart table above: both windows came up with their titles, and the cache was rebuilt.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run again after this notes file was written:

```
Repo Result
---- ------
code dry run
docs dry run
```

P84 DONE
