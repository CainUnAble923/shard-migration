# cc-P132: Console facelift part 1: resizing, an Enhanced Client look, and art slots with a spec for Chase

2026-10-16. Prompt: `D:\UO\cc-prompts\cc-P132-console-layout-and-art-slots.md` (handed by the Golem after P131, into the
same desktop session). Both repos were clean at the start. **Model:** the prompt asks for Opus; this session ran Fable
(the Golem's model routing has no model figure for a desktop session and handed it anyway).

## Headlines

- **Resizing.** The three rows under the tiles are two draggable splitters (Status over the tabs, the tabs over the
  output; the Action output pane kept its own). The tiles already wrapped (cc-P87) and the tab content stretches; the
  window remembers its size, place, maximized state and the three splitter positions in a per-user file outside the
  repo (`%LOCALAPPDATA%\ShatteredLegacy\shard-console-window.json`), wrapped so a bad or missing file is the defaults
  and never a stop, and placed back on a screen only when at least part of it would show. The process is made
  per-monitor DPI aware before the first window and the form scales from 96 DPI, so text and art stay crisp at 125%
  and 150% (this PC runs at 100%, so that is by the documented path, not seen). The minimum stays 900x700.
- **The Enhanced look is the default.** Dark slate drawn in code (a seeded speckle whose lightest and darkest pixel are
  known, so the contrast facts can check text against them), bronze trim, slate tab pages with light type, Segoe UI
  and a Palatino title, a rune before every tab header, a sigil at the header's end, and **green, amber and red
  crystals on every tile** (a dull grey one for off, retired and unknown). **The Golem figure** sits on the GOLEM tile
  and the Golem tab: glowing with a halo and lit eyes while it runs a prompt, a soft glow when awake with nothing
  running, dark when resting, stopped or off. UO and Plain still work and are unchanged apart from the shared fixes.
- **Art slots.** `scripts\console-art\` with twenty fixed file names (`Get-ArtSlots`): the four crystals, the Golem's
  three states, the tab rune, the corner sigil, the spinner, the header band, the stone and page textures, and one icon
  per tile. Each has a displayed size and a KB budget (they sum to about 1.9 MB). A missing or bad file is the drawn
  fallback and one line in the startup log (one line names every missing slot; one line per bad file, with why).
  Animated slots take a horizontal sprite strip PNG with its frames and fps in `console-art\art.json`, or an animated
  GIF; the console prefers the strip (8-bit transparency, no halo on the stone, exact timing, the console draws the
  frames). Only the first frame is drawn until P133.
- **The spec** for Chase's image tool is `notes\console-art-spec.md`: one shared style paragraph, then every slot's file
  name, sizes, format, frames and loop, and a plain image prompt; and how to drop the files in. No images were made.
- **Readable text everywhere.** Every look now carries six named text colors (normal, muted, warning, danger, success,
  link) chosen to pass AA on the page they are drawn on, plus warning and danger colors for words drawn on the stone,
  and a **plate**: the confirm phrase ("Type exactly: publish player package") is 14 pt bold gold on a plain near-black
  plate. Before, in the UO look, it was the page's dark red on the stone: **1.34:1** measured on the art's lightest
  pixel (AA is 4.5:1); after, **12.7:1** (UO) and **13.7:1** (Enhanced). The commit countdown's ForestGreen (2.04:1 on the
  darkest parchment) and DarkOrange (1.08:1) are the named success (5.4:1) and warning (5.07:1) now. The theme walker
  maps every WinForms color a control was given to the named one for where it sits. The contrast fact covers 68 pairs
  per themed look, each against the lightest and darkest pixel under it.
- **The test shard's rebuild light** (TEST tile second line, and beside Rebuild on the Test shard tab): green when the
  running image was built from HEAD or nothing since touches the server; amber "3 commits: P127, P128, P129 touch the
  server since the running build: Rebuild can go now"; red with the reason (a build already running, the Golem running
  P<nn>, N uncommitted files: commit first); grey when the running image has no `sl.commit` label or nothing runs.
  The running image's commit is its label, which `docker/uo/build.sh` has stamped since cc-P96 (no build change was
  needed). Hover lists the commits and the server files. `scripts\shard-console-cache\lights.json` carries both lights
  in status.json style.
- **The player package light** (beside Build package on the Player package tab, and in `lights.json`): green when the
  published package (the live `version.json`) was built from the newest player-facing commit; amber "changes since the
  published package: Build package (...)" or "built, not published: Publish package (...)"; red with the reason (the
  Golem running, uncommitted changes, a stale client by P124's gate, a build running, the download site unreachable).
  What each zip was built from is its `app\VERSION.txt` "built from ShatteredLegacy <commit>" (cc-P124), read without
  extracting; one that says "uncommitted" is called out. The site is asked once every ten minutes at most.
- **Tests:** console **346 facts, 341 passed, 5 failed**, the five being the pre-existing Haven-cutover facts (P131's
  note names them; red before and after this change); the 10 new P132 facts all red against the stashed pre-change script (10 facts, 0 passed, 10 failed). The
  real console, opened through the shortcut's launcher: 1200x1000, resized to 900x700 and 1800x1000 by Win32 MoveWindow,
  closed normally with "errors logged this session: 0" in the startup log, "DPI: per-monitor DPI aware" in the action
  log, and the window file written with the last size, place and splitters.

## What changed, with file:line (`D:\ShatteredLegacy`)

### `scripts/Shard-Console.ps1` (CORE)

| Where | What |
|---|---|
| `Get-ConsoleTheme` | `-Name` takes `Enhanced`; every look gains `Text` (the six named colors), `Plate` (themed looks) and `Crystals`; UO gains `Chrome.StoneWarn` and `StoneDanger`, and its `Text.Warning` and `Text.Success` were darkened from the line colors so they pass on the darkest parchment pixel (3.92 and 4.11 were under AA) |
| `Get-EnhancedTheme` | the Enhanced look: fonts, tiles, lines (all at 7:1 or better), text, plate, `Glow` per state, chrome, `Texture` (the drawn stone's and page's base, spread and measured bounds) |
| `Get-ThemeContrastPairs` | the stone's and page's extremes come from the gumps (UO) or the drawn texture (Enhanced); adds warning and danger words on the stone, the six named colors on each page extreme, and the plate |
| `ConvertFrom-ConsoleSettings` | default `Enhanced`; accepts the three looks |
| cc-P132 CORE block (before `Get-ConsoleTooltips`) | `Get-ArtSlots`, `ConvertFrom-ArtManifest`, `Test-ArtFile`, `ConvertFrom-WindowState`, `ConvertTo-WindowState`, `Resolve-WindowBounds`, `$script:ServerPaths` / `$script:ShipPaths`, `ConvertFrom-GitLogWithFiles`, `Select-CommitsTouching`, `Format-CommitPrompts`, `Get-RebuildLight`, `Get-PackageLight`, `ConvertTo-LightsJson` |
| `Get-ConsoleTooltips` | `rebuild.light`, `package.light`, `golemFigure`, `headerRune` |
| `Get-ConsoleConfig` | `ArtFolder`, `WindowStateFile`, `LightsFile`, `PublishedVersionUrl` |

### `scripts/Shard-Console.ps1` (SHELL)

| Where | What |
|---|---|
| cc-P132 SHELL block (before `Get-ThemeFont`) | `New-SpeckleTexture`, `Get-ThemeImages`, `Get-ConsoleArt`, `Get-ArtImage`, `Get-ArtOrFallback`, `Get-GlowColor`, `New-FallbackImage` and the five `Draw-*Fallback` functions, `Set-ConsoleDpiAwareness`, `Read-WindowState`, `Save-WindowState`, `Restore-WindowBounds`, `Restore-WindowSplitters`, `Set-SplitterSafely`, `Get-RebuildFacts`, `Get-GolemRunningPrompt`, `Test-ProcessRunning`, `Read-ZipBuiltFrom`, `Get-PublishedPackageVersion`, `Get-PackageLightFacts` |
| `Get-StateTextColor`, `Get-ThemedTextColor` | the named colors as the walker and the countdown use them |
| `Set-ControlTheme` | a `plate`-tagged panel keeps its colors; a PictureBox goes transparent; labels, check boxes and radios take the named color for their meaning and place |
| `Set-TabTheme` | the rune before each header, wider padding |
| `New-StatusTile` (`-Figure`), `Set-TileCrystal`, `Set-GolemFigure` | the crystal as a child of the word label, the figure of the detail label |
| `New-LightLabel`, `Set-LightLabel`, `Update-Lights` | the two lights, the TEST tile's second line, `lights.json` |
| `New-TypedConfirmForm`, `Show-TypedConfirm` | the dialog built apart from being shown; the plate |
| `New-ConsoleForm` | `-RestoreWindow`; the art folder read first; DPI autoscale; the GOLEM tile with the figure; the two splitters in place of the three grid rows (same first shares as cc-P116); the header band or rune; the Look picker widened and `Enhanced` added; the rebuild light after Rebuild; the package light beside Build package; the Golem tab's figure |
| `Update-ConsoleStatus`, `Update-AutopilotView` | `Update-Lights` after the tiles; the figure follows the Golem |
| `Update-CommitCountdown`, `Set-ConsoleDryRun` | named colors in place of ForestGreen, DarkOrange, Firebrick and Black |
| `Write-ConsoleLog` | never throws (a config with no log file drops the line) |
| the entry | DPI awareness logged, `-RestoreWindow` |

### Other files

- `scripts/console-art/README.md` (the slot table and the formats), `scripts/console-art/art.json` (empty manifest).
- `design/console-enhanced/`: `Take-ConfirmScreenshots.ps1`, `confirm-before-uo.png`, `confirm-after-uo.png`,
  `confirm-after-enhanced.png`, `confirm-after-plain.png`, `window-enhanced.png`, `window-uo.png`, `window-plain.png`
  (the window shots are `DrawToBitmap` of the headless form: the two RichTextBoxes draw blank that way).
- `scripts/tests/Shard-Console.Tests.ps1`: 10 P132 facts; `P84_TheSettingsDefaultToUOAndThePaneAndABadFileFallsBack`
  updated to the Enhanced default.
- `CHANGELOG.md` 2026.10.16.6 `### Staff`; `VERSION` 2026.10.16.6.
- Docs repo: `notes/console-art-spec.md` (new), this note.

## The slot list

| Slot | Shown at | Kind | Budget | Fallback drawn |
|---|---|---|---|---|
| `crystal-green/amber/red.png` | 32 (28 on tiles, 22 beside a light) | animated | 120 KB each | a six-faceted gem with a glow halo |
| `crystal-grey.png` | 32 | static | 60 KB | the same gem, dull, no halo |
| `golem-running.png` | 64 (56 on the tile) | animated | 300 KB | the silhouette, bronze, halo, lit eyes |
| `golem-idle.png`, `golem-dark.png` | 64 | static | 120 KB each | softer glow and dim eyes; slate, no eyes |
| `rune-tab.png`, `rune-corner.png` | 16 (the corner 40 in the header) | static | 30 KB each | a bronze ring with three strokes |
| `spinner.png` | 24 | animated | 100 KB | eight fading spokes |
| `header-band.png` | 64 tall, tiled | static | 250 KB | backing, bronze rule, a rune |
| `stone.png`, `page.png` | 256, tiled | tile | 200 KB each | the speckle textures |
| `icon-live/test/publisher/dns/golem/playtests/websites.png` | 32 | static | 40 KB each | the ring with the tile's letter |

## The readable-text audit

Measured with the console's own `Get-ContrastRatio` against the lightest and darkest pixel under each spot (the UO
gumps as cc-P87 measured them; the Enhanced texture's bounds). Before and after, in the UO look unless said:

| Spot | Before | After |
|---|---|---|
| Confirm phrase line (Chase's example) on the stone | 1.34:1 (page red on the backing) | 12.73:1 on the plate; Enhanced 13.73:1 |
| Commit tab countdown "Ready to commit" (ForestGreen on parchment, darkest) | 2.04:1 | 5.40:1 (Text.Success); Enhanced 9.37:1 |
| Commit tab countdown waiting (DarkOrange on parchment, darkest) | 1.08:1 | 5.07:1 (Text.Warning); Enhanced 8.67:1 |
| Commit tab countdown error (Firebrick on parchment) | 5.51:1 (the walker's PageWarn) | 5.51:1 (Text.Danger); Enhanced 6.46:1 |
| Any Firebrick caption that sits on the stone (the walker made them PageWarn) | 1.35:1 | 8.14:1 (StoneDanger); Enhanced 9.27:1 |
| The DRY RUN box off, drawn Black in Plain's value on the stone | 1.31:1 (UO already used StoneText, 12.45:1) | 13.63:1 Enhanced |
| DimGray captions on parchment, darkest | 2.55:1 raw (the walker: PageDim 5.34:1) | 5.34:1 (Text.Muted); Enhanced 6.73:1 |
| UO Text.Warning / Text.Success on the darkest parchment (the P87 line colors reused) | 3.92:1 / 4.11:1 | 4.9:1 / 5.2:1 (darkened) |
| Enhanced tiles | new | green 10.3, amber 8.8, red 8.1, grey 7.9 |
| Enhanced buttons, fields, tabs, title | new | 8.8, disabled 5.1, fields 13.0, selected tab 10.0, gold title on the backing 9.2 |

Lowest pair in Enhanced: the DRY RUN box locked on, drawn disabled by Windows, 4.67:1 (cc-P87's measured pair).
Screenshots: `design\console-enhanced\confirm-before-uo.png` (the old dialog rebuilt from cc-P84's code, since the
old script has no builder that returns the form unshown) and `confirm-after-*.png`; `window-*.png` for each look.

## Tests (each new one seen failing first)

- `P132_EveryLookPassesAAOnItsTextColorsTilesAndPlate` (every pair of every look; and the old confirm color fails AA)
- `P132_TheConfirmPhraseIsLargeAndBrightOnAPlateInEveryLook` (measured on the built controls)
- `P132_NamedTextColorsReplaceTheHardCodedOnes`
- `P132_EachLookRendersWithItsOwnChromeAndTheTabsStretch` (three forms; the stone's pixels inside the measured bounds)
- `P132_TilesWrapAtNarrowWidths` (two rows at 900 wide, one at 1700)
- `P132_SplittersAndTheWindowStatePersistAndSurviveACorruptFile` (the file, a corrupt file, off-screen bounds, a drag saved and read back, a splitter restored)
- `P132_EverySlotLoadsASamplePngAndFallsBackWhenMissingAndABadFileLogsOneLine` (twenty sample PNGs, two strips with art.json; an empty folder; two bad files, one line each)
- `P132_TheGolemFigureFollowsTheGolemsState`
- `P132_TheRebuildLightSaysEachColourFromFixtures` (a server change, docs only, the Golem running, uncommitted, a build running, no label, nothing running, a dirty image, the JSON)
- `P132_ThePackageLightSaysEachColourFromFixtures` (each colour; the git log parser; a missing zip)
- Against the stashed pre-change script (`git stash` of the console script only): **10 facts, 0 passed, 10 failed**.
- Full suite under Windows PowerShell 5.1: the last full run read **346 facts, 336 passed, 10 failed**; five were
  mine (two tooltips over the two-sentence rule, cc-P87's pair-count pin at 35 where the UO look now draws 68, cc-P87's
  backing fact looking for the two groups in the old grid instead of the splitters' panels, an array compared by
  reference in a new fact, and a `-LiteralPath` wildcard that removed nothing) and were fixed; those facts, every
  P116, P87 and P132 fact and the two P84 tooltip facts were rerun together: **22 facts, 22 passed, 0 failed**. So
  341 of 346, with the five below the only red ones.
- The five that fail before and after this change (the Haven ops cutover, not this prompt): `P83_TheLinksOpenTheTwoPagesAndNothingElse`,
  `P83_TheTileHasItsTwoLinksAndTheAutopilotTabHasThemToo`, `P101_TheTileAndTheTabAreBuiltAndDrawn`,
  `P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing`, `P107_LinksAndSitesPointAtHavenAfterTheCutoverAndAtThisPcBefore`.
- Golem suite: unchanged by this prompt (292 of 292 at the end of P131).

## Play-test items

None: staff tooling only.

## Deviations and decisions for Chase

- **No eighth tile.** The prompt puts the package light "on the Player package tab and its tile"; the package has no tile
  of its own (STATUS PUBLISHER is the status page's publisher), and seven tiles already wrap at the default width. It
  is on the Player package tab beside Build package, and in `lights.json`. Say the word and it gets a tile or a line
  on the publisher tile.
- **The lights cost about 1.3 s per refresh** (git, the Golem's status and a process listing, every 30 s with the status)
  and a GET of the download site at most every ten minutes. The form itself took about 17 s to build before this
  prompt (measured on the stashed script) and takes the same now.
- **Server paths** that count for a rebuild: `server/`, `docker/uo/`, `CHANGELOG.md`, `VERSION` (the last two are baked
  into the image by the Dockerfile). **Shipping paths** for the package: `player-package/`, `client/patches/`,
  `TAZUO_COMMIT`, `client/Build-Client.ps1`. The built client in `D:\UO\tazuo-sl-build\client` is outside git, so it
  is judged by P124's stale gate (red), not by commits. Both lists are one line each at the top of the CORE block.
- **"A build is already running"** is read from the processes on this PC (`Start-TestShard.ps1`, `build.sh`, `docker
  build`, or this console's own rebuild child; `Build-PlayerPackage.ps1` for the package).
- **DPI:** per-monitor awareness is set by `SetProcessDpiAwareness` before the first window, and the form autoscales
  from 96 DPI. On this 100% PC nothing changes; at 125% or 150% WinForms scales the layout and draws text at the
  monitor's DPI. Not seen on such a monitor here.
- **The Enhanced look has no client gump art**: it draws its own stone, by design (the prompt's slate and stone), and
  the stone and page slots take real textures when you have them.
- **Only the first frame** of an animated slot is drawn; the spinning and glowing animations are P133's.
- **The P116 facts' default sizes:** the two splitters' bars take 12 px that the old grid did not, so a tab page is
  about 12 px shorter at the same window size. The P116 reachability facts still pass (below).
- The confirm "before" screenshot is the old dialog rebuilt from cc-P84's code under the UO look (its walker turned the
  Firebrick label to the page's dark red on a transparent panel over the stone), because the old script only has a
  `Show-TypedConfirm` that blocks on `ShowDialog`.

## For Chase

Close and reopen the console: it starts in **Enhanced** with the drawn stand-ins (crystals, the Golem, runes), remembers
its size and place from then on, and the Status / tabs / output rows have splitter bars you can drag. The Look picker
on the Status bar still offers UO and Plain.

The art: make each piece with your image tool from `D:\UO\shard-migration\notes\console-art-spec.md` (the shared style
paragraph plus one prompt per piece), save it under the exact file name in `D:\ShatteredLegacy\scripts\console-art\`,
add a line to `art.json` for a sprite strip, and reopen the console. The startup log says `console-art: N of 20 slots
have art` and names any file it refused.

The lights: the TEST tile's second line and the Test shard tab say whether a rebuild is due and why it cannot go; the
Player package tab's line says Build, Publish, latest, or why it is blocked; hover either for the commits.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
=== code  (D:\ShatteredLegacy) ===
  pending: CHANGELOG.md, VERSION, scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1,
           design/console-enhanced/ (the script and seven PNGs), scripts/console-art/README.md, scripts/console-art/art.json
  dry run: would add, commit and push

=== docs  (D:\UO\shard-migration) ===
  pending: testing/SUMMARY.md, testing/play-tests.json (the play-test mirror), notes/cc-P132-console-layout-and-art-slots.md, notes/console-art-spec.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

`scripts/shard-console-cache/lights.json` is ignored (`git check-ignore -v`: `.gitignore:90 scripts/shard-console-cache/`).
No file over 5 MB: the largest new file is `design/console-enhanced/window-enhanced.png` at 282 KB.

P132 DONE
