# cc-P87: Shard Console readability pass (UO look)

Prompt: `D:\UO\cc-prompts\cc-P87-console-readability.md` (handed off by the autopilot from `queue\` while this was in
progress; same file, 5,062 bytes). Builder (console script and tests); no shard build. Code
in `D:\ShatteredLegacy`. Not committed (autopilot commits after DONE).

**Start state.** The code repo was clean. The docs repo had two uncommitted files that are not mine:
`testing\SUMMARY.md` and `testing\play-tests.json` (the play-test list grew from 130 to 171 entries at 13:27Z, after
Chase's 08:17 commit). The prompt says to stop in that case. Chase said "go" in chat with them dirty, and this task
neither reads nor writes them, so I went ahead and left them untouched. The next commit will sweep them in with
this work.

**Why the queue was paused.** The autopilot log shows P86 DONE at 07:34, then `commit exit 1, queue paused`.
`cc-autopilot.ps1` line 210 passes the commit subject to `Commit-ShardWork.ps1` through `powershell.exe -File`, and
P86's subject contained double quotes ("Disconnect VPN"). The quotes split the argument, so the rest of the subject
landed on `-MaxFileMB` ("Cannot convert value "VPN button" to type System.Int32"). Chase then committed by hand.
Nothing here fixes it: it is the autopilot's script, not this task's. See "For Chase".

## Headlines

- **All seven spots are fixed in the UO look. Plain is unchanged**, value for value, and a new fact pins that.
- **Text on the stone now sits on a dark, semi-opaque backing** (24,22,20 at alpha 200). This covers the header, the
  Status group with its options row, and the output group with the pane bar.
  - Measured honestly: these pairs already passed WCAG before. Gold on the stone's lightest pixel was 5.29:1. What
    made them hard to read was the texture: it runs from 16 to 74 grey right behind thin serif strokes.
  - Under the backing, that range is 22 to 35. Gold now reads 9.56:1 and light text 12.45:1 at the worst point.
- **Disabled buttons are drawn by hand.** Before, they were WinForms' own dark-on-dark at **2.00:1**, which fails
  even the 3:1 floor for disabled text. They are now a flat grey-brown face with no gold and 190,178,156 text, at
  **4.74:1**: plainly off, still legible.
- **Tabs are bold, padded wider, and the selected tab is parchment with a gold bar.**
- **Tile buttons are 9 pt bold** (were 8.25 regular).
- **Status lines:** green, amber and gray are darkened to at least **7:1** (were 6.30, 5.93 and 6.60). The UO
  Consolas is 9.75 pt, up from 9.
- **Nothing in a tile clips, from the smallest window (900 x 700) to 2400 wide.**
  - The tiles go six across while every tile's buttons fit a sixth of the width. Otherwise they go three across in
    two rows.
  - Each row is as tall as its tallest tile needs, from 96 to 130 px.
  - Titles shrink toward 9 pt, and wrap only if they still do not fit. Details shrink toward 8.25 pt.
  - Two more clips turned up and are fixed. The window's single grid column grew to its widest caption (1,100 px),
    so below that width the right edge ran off the window. The options row also hid its last box on a narrow window.
- **Contrast is measured, not eyeballed.** A new CORE function, `Get-ThemeContrastPairs`, lists all **35** text and
  background pairs the UO look draws. Each pair carries its floor: 4.5 for normal text, 3 for large text, 3 for
  disabled text.
  - Text on the art is checked against the art's lightest and darkest pixel, under the backing.
  - Two pairs Windows draws itself are included, measured from screenshots: the tooltip at 6.86, and the DRY RUN
    box locked on at 4.67.
  - All 35 pass. The table below is generated from that function.
- **Tests:**
  - **210 / 210** green. That is 205 old facts plus 5 new ones.
  - The new facts went red under 6 deliberate breaks, every break caught by the fact aimed at it.
- **No behavior changed.** No action, plan, caption text, tooltip or key was touched.

## The seven spots

| # | Spot | What changed | Measured (worst case) |
|---|---|---|---|
| 1 | Section headers and the window title on stone | The Status and output GroupBoxes and the header panel carry the backing. Gold text unchanged. | Gold on backing over the stone's lightest pixel: 5.29 to **9.56**. Over the darkest: 11.35 to 10.89. With no art: 8.30 to 10.24. |
| 2 | Options row ("refresh every 30 s", DRY RUN, "Look:", "actions in their own windows") | Sits inside the Status group, so it is on the backing too. In UO the row wraps and grows instead of hiding its last box on a narrow window. | Light text on backing over the lightest stone: 6.88 to **12.45**. |
| 3 | Small buttons in tiles (Disconnect VPN, Play tests, Dashboard, Status) | 9 pt bold (were 8.25 regular). Disabled ones are drawn by hand (see 7). | Button text on button 6.92. Hover 4.87, the lowest normal pair, unchanged. |
| 4 | Tiles cut off ("AUTOPILOT: NEEDS", "this house. N", PLAY TESTS off the edge) | `Update-TileFit`, plus a 100% column style on the window grid (UO only). Details below. | The fact checks every title, detail and button at six window sizes. |
| 5 | Tab labels thin; selected tab hard to tell apart | Drawn bold, padding 20,6 (was 14,5). The selected tab is parchment with a 4 px gold bar on top, the others are dark wood. | Unselected 6.92, selected 9.26, LIVE selected 7.75. |
| 6 | Colored lines in the status box | Green 24,100,30 to 18,86,24; amber 138,74,0 to 120,62,0; gray 92,82,70 to 84,74,62. Red (7.50) and head (11.59) were already above 7. Consolas 9 to 9.75. | Green 6.30 to **7.66**, amber 5.93 to **7.30**, gray 6.60 to **7.49**. |
| 7 | Disabled buttons (the pane's Stop, Disconnect VPN when greyed) | A Paint handler in `Set-ControlTheme` redraws a disabled button: DisabledBack 72,66,58, DisabledBorder 120,108,90 (no gold), DisabledText 190,178,156. | **2.00 to 4.74** (floor 3). |

Before the change, I checked from pixels what the status box draws: its lines are exactly the theme's colors, so
spot 6 really was the theme's values. Sampled from a screenshot, LIVE COMPOSE FILE is drawn 138,74,0 on 246,238,218.

## Contrast table, every pair

Generated by `Get-ThemeContrastPairs` (after) and by the same function run on the cc-P84 values (before). In "before":
- there was no backing, so stone text is measured on the raw stone;
- the lines are the old colors;
- the disabled text is WinForms' own 30,23,15 on 92,70,44, measured from a screenshot of the old pane Stop and
  Disconnect VPN buttons.

**The colors in the first column are the after colors.** Floors are 4.5 for normal text, 3 for large text (18 px and
up, or 14 px and up bold) and 3 for disabled text.

| Text and background | Floor | Before | After | |
|---|---|---|---|---|
| Window title (gold, 17 pt bold) on backing over stone art, lightest (232,196,104 on 35,33,32) | 3 | 5.29 | 9.56 | pass |
| Group titles (gold, bold) on backing over stone art, lightest (232,196,104 on 35,33,32) | 4.5 | 5.29 | 9.56 | pass |
| Options row and pane label text on backing over stone art, lightest (238,226,196 on 35,33,32) | 4.5 | 6.88 | 12.45 | pass |
| Window title (gold, 17 pt bold) on backing over stone art, darkest (232,196,104 on 22,21,19) | 3 | 11.35 | 10.89 | pass |
| Group titles (gold, bold) on backing over stone art, darkest (232,196,104 on 22,21,19) | 4.5 | 11.35 | 10.89 | pass |
| Options row and pane label text on backing over stone art, darkest (238,226,196 on 22,21,19) | 4.5 | 14.78 | 14.17 | pass |
| Window title (gold, 17 pt bold) on backing over stone, drawn (no art) (232,196,104 on 29,27,25) | 3 | 8.30 | 10.24 | pass |
| Group titles (gold, bold) on backing over stone, drawn (no art) (232,196,104 on 29,27,25) | 4.5 | 8.30 | 10.24 | pass |
| Options row and pane label text on backing over stone, drawn (no art) (238,226,196 on 29,27,25) | 4.5 | 10.80 | 13.34 | pass |
| Page text on parchment art, lightest (60,38,20 on 246,222,172) | 4.5 | 10.79 | 10.79 | pass |
| Page dim text on parchment art, lightest (72,54,34 on 246,222,172) | 4.5 | 8.74 | 8.74 | pass |
| Page warning text on parchment art, lightest (112,16,12 on 246,222,172) | 4.5 | 9.03 | 9.03 | pass |
| Page text on parchment art, darkest (60,38,20 on 222,164,131) | 4.5 | 6.59 | 6.59 | pass |
| Page dim text on parchment art, darkest (72,54,34 on 222,164,131) | 4.5 | 5.34 | 5.34 | pass |
| Page warning text on parchment art, darkest (112,16,12 on 222,164,131) | 4.5 | 5.51 | 5.51 | pass |
| Page text on parchment, drawn (no art) (60,38,20 on 230,206,160) | 4.5 | 9.26 | 9.26 | pass |
| Button text on button (246,226,170 on 92,70,44) | 4.5 | 6.92 | 6.92 | pass |
| Button text on button, hover (246,226,170 on 118,92,58) | 4.5 | 4.87 | 4.87 | pass |
| Button text, disabled (190,178,156 on 72,66,58) | 3 | **2.00 FAIL** | 4.74 | pass |
| Tab, not selected (246,226,170 on 92,70,44) | 4.5 | 6.92 | 6.92 | pass |
| Tab, selected (60,38,20 on 230,206,160) | 4.5 | 9.26 | 9.26 | pass |
| Tab, LIVE shard selected (112,16,12 on 230,206,160) | 4.5 | 7.75 | 7.75 | pass |
| Field and list text (40,28,16 on 250,244,228) | 4.5 | 15.13 | 15.13 | pass |
| Status and output line, normal (40,28,16 on 246,238,218) | 4.5 | 14.37 | 14.37 | pass |
| Status and output line, head (24,40,110 on 246,238,218) | 4.5 | 11.59 | 11.59 | pass |
| Status and output line, green (18,86,24 on 246,238,218) | 4.5 | 6.30 | 7.66 | pass |
| Status and output line, amber (120,62,0 on 246,238,218) | 4.5 | 5.93 | 7.30 | pass |
| Status and output line, red (150,22,18 on 246,238,218) | 4.5 | 7.50 | 7.50 | pass |
| Status and output line, gray (84,74,62 on 246,238,218) | 4.5 | 6.60 | 7.49 | pass |
| Tile, green (24,84,30 on 214,232,200) | 4.5 | 6.98 | 6.98 | pass |
| Tile, amber (122,62,0 on 246,226,180) | 4.5 | 6.54 | 6.54 | pass |
| Tile, red (128,20,16 on 240,206,196) | 4.5 | 7.08 | 7.08 | pass |
| Tile, grey (70,62,52 on 220,212,196) | 4.5 | 7.13 | 7.13 | pass |
| Tooltip text (drawn by Windows) (87,87,87 on 249,249,249) | 4.5 | 6.86 | 6.86 | pass |
| DRY RUN box, locked on (drawn disabled by Windows) (128,94,15 on 246,226,180) | 3 | 4.67 | 4.67 | pass |

How the art was measured: from the cached gumps (`3604.png`, 128 x 128; `9304.png`, 240 x 240). I took the lightest
and darkest single pixel and the lightest and darkest 3 x 3 and 6 x 6 averages. The single pixels are the extremes,
so those are what the theme records (`StoneLight`, `StoneDark`, `ParchmentLight`, `ParchmentDark`):
- stone: lightest 74,74,74, darkest 16,16,16 (3 x 3: 61 and 30; 6 x 6: 54 and 36);
- parchment: lightest 246,222,172, darkest 222,164,131.

## Fit at each window size and scaling

**What scaling does here.** PowerShell 5.1's WinForms runs **DPI-unaware**. I measured this in this session:
`GetProcessDpiAwareness` returned 0, and a new form's `AutoScaleMode` is `Inherit`. So at 125% and 150% Windows
stretches the whole window as a bitmap, and the layout is the 100% layout at the window's logical size:
- 1280 px at 125% lays out as 1024;
- 1280 px at 150% would be 853, below the 900 px minimum, so the smallest window at 150% is 900 logical
  (1350 physical).

This PC runs 100% (AppliedDPI 96, 2560 x 1440). I did not change Windows' scaling, because that is a system setting.
So "at 125% and 150%" is proven by laying out at those logical sizes, and the 150% screenshots are the 100% captures
stretched 1.5 times, which is what Windows does to this window. **Unverified on a real 150% display.**

From the fact `P87_UOTilesNeverClipFromTheNarrowestWindowToAWideOne`, with the tiles' words from Chase's screenshot
time (the longest seen: STATUS PUBLISHER: NOT PUBLISHING, AUTOPILOT: NEEDS YOU, the full PUBLIC DNS line):

| Window (logical) | Means | Tiles | Tile row | Smallest title | Smallest detail | Clipped |
|---|---|---|---|---|---|---|
| 900 x 700 | the minimum; the minimum at 150% | 3 across, 2 rows | 232 px | 9.75 pt | 9.75 pt | nothing |
| 1024 x 768 | 1280 x 960 at 125% | 3 across, 2 rows | 232 px | 11.25 pt | 9.75 pt | nothing |
| 1280 x 1000 | 1280 at 100% | 3 across, 2 rows | 200 px | 11.5 pt | 9.75 pt | nothing |
| 1300 x 1000 | Chase's screenshot | 3 across, 2 rows | 200 px | 11.5 pt | 9.75 pt | nothing |
| 1600 x 1000 | | 6 across | 120 px | 9 pt | 9.75 pt | nothing |
| 2400 x 1000 | wide | 6 across | 104 px | 11.5 pt | 9.75 pt | nothing |

For every tile at every size the fact checks three things:
- the title fits its label;
- the detail fits the space left;
- every button lies wholly inside its tile and its bar.

It also checks that the tile row ends inside the window. At 900 x 700 the status and output boxes are short, but
they scroll; nothing is cut.

## What was built

All in `D:\ShatteredLegacy`:

- **`scripts\Shard-Console.ps1`**
  - **CORE:**
    - `Get-ConsoleTheme` (UO only):
      - fonts gain `TileButtonSize`, `TileFloor` and `DetailFloor`, and Consolas goes to 9.75;
      - three line colors change;
      - the chrome gains `Backing`, `BackingAlpha`, `DisabledBack`, `DisabledText` and `DisabledBorder`;
      - the gumps gain `StoneLight`, `StoneDark`, `ParchmentLight` and `ParchmentDark`.
    - New `Get-BlendedColor` (alpha blending), `$script:MeasuredPairs` (the two pairs Windows draws) and
      `Get-ThemeContrastPairs`.
  - **SHELL:**
    - `Set-ControlTheme`: tile buttons bold at `TileButtonSize`; a disabled-button Paint handler (a closure over
      three colors, so it calls no script function); GroupBoxes on the stone get the backing.
    - `Set-TabTheme`: bold labels, wider padding, a gold bar on the selected tab.
    - New `Get-TileFitFont`, `Update-TileFit` and `Update-CaptionFit`.
      - `Update-TileFit` runs on the tiles' resize, on the window's Shown, and after every tile update.
      - `Update-CaptionFit` wraps the 1,100 px captions to the window when it is narrower.
    - `New-ConsoleForm`, UO only:
      - a 100% column style on the grid;
      - `$script:ui.Glance` and `$script:ui.Grid` exposed;
      - the options row auto-sizes;
      - the header carries the backing.
- **`scripts\tests\Shard-Console.Tests.ps1`**: 5 facts and 2 helpers (`New-P87Form`, `Test-P87TileFits`).
- **`CHANGELOG.md`**: a 2026.10.13.9 `### Staff` line. 2026.10.13.8 was already committed, so this starts the next
  version.
- **`VERSION`**: 2026.10.13.9.

## Tests

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1`

| Run | Result |
|---|---|
| Before this task (untouched script) | **205 / 205** |
| With the change and the 5 new facts | **210 / 210** |
| Red A: amber back to 138,74,0; the disabled Paint handler made a no-op; the group backing removed; `Update-TileFit` allowed to run on Plain | **4 failed**, one per break: `P87_EveryUOTextPair...` (line amber at 7:1), `P87_TextOnTheStone...` (Status on the backing), `P87_ADisabledUOButton...` (face is DisabledBack), `P87_PlainKeeps...` (expected 6 got 3) |
| Red B: `Update-TileFit` made a no-op; the options row's auto-size removed | **2 failed**: `P87_UOTilesNeverClip...` (900 wide, title "LIVE: STARTING?" needs 48 px, has 30) and `P87_TextOnTheStone...` ("actions in their own windows" at Y=42 outside its 34 px bar) |
| Restored from a copy, `cmp`-identical; final run | **210 / 210** |

The 5 new facts:
- `P87_EveryUOTextPairMeetsItsFloorOnTheArtsLightestAndDarkest`
- `P87_TextOnTheStoneSitsOnTheBacking`
- `P87_ADisabledUOButtonIsDrawnInItsOwnLegibleColors`
- `P87_UOTilesNeverClipFromTheNarrowestWindowToAWideOne`
- `P87_PlainKeepsItsOneRowOfSixAndItsOwnLook`

## Screenshots

All are in `D:\ShatteredLegacy\scripts\shard-console-cache\screenshots\p87\`. That is P84's git-ignored cache
(`.gitignore:90:scripts/shard-console-cache/`, checked with `git check-ignore`), because they contain EA's gump art.
Each is the real console reading docker (read-only), built in-process with the UO look and the pane.

| File | What |
|---|---|
| `before-uo-1300.png` | Before, at 1300 px: "AUTOPILOT: NEEDS", the DNS detail under its button, PLAY TESTS' buttons crowded, Disconnect VPN unreadable |
| `after-uo-1280-tab0.png` | After, 1280 px, 100% |
| `after-uo-1280-tab3.png` | After, Diagnostics tab: the disabled Disconnect VPN and the pane's disabled Stop |
| `after-uo-1024-tab0.png` | After, 1024 px (1280 at 125%) |
| `after-uo-900-tab0.png` | After, the 900 x 700 minimum |
| `after-uo-900-tab0-at150pct-simulated.png`, `after-uo-1280-tab0-at150pct-simulated.png` | The two above stretched 1.5 times, as Windows shows a DPI-unaware window at 150% |
| `after-uo-2400-tab0.png` | After, wide: six across |
| `after-plain-1280-tab0.png` | Plain, after this task: as before |

## Deviations and decisions for Chase

1. **Plain still clips its tiles, as it always has.** The prompt says both "nothing clips" and "Plain must not
   change", and I kept Plain unchanged. `after-plain-1280-tab0.png` shows "STATUS PUBLISHER: N" and
   "AUTOPILOT: NEEDS Y". Turning `Update-TileFit` and the grid's column style on for Plain is a two-line change.
   Want it?
2. **The tiles take two rows on a narrower window.** They were two rows at 1300 and one row at 1600; the exact
   switch point (where PLAY TESTS' three buttons stop fitting a sixth of the width) was not measured. I chose two
   full-size rows over six cramped ones. The cost is that the status box is 96 px shorter at 1280 (a 200 px tile
   row instead of 104).
3. **DPI.** The console is DPI-unaware, so at 125% and 150% Windows stretches it and the text goes soft. Declaring it
   DPI-aware (`SetProcessDPIAware` before the form) would make it crisp. But every hard-coded pixel size in the
   form (button widths, row heights, margins) would then need scaling, which is a layout change of its own and was
   not asked for. Proposed, not done.
4. **Spot 2 is fixed by the backing, not by the text color.** On this PC the options row was already drawn in light
   text (238,226,196). "Dark text on a dark texture" may have come from the stone's speckle, or from a state I could
   not reproduce. Please look again at the new row.
5. **The selected-tab gold bar shows thinner on screen than the 4 px it is drawn.** I did not find out why. The
   parchment fill is what really marks the selected tab. A thicker bar is easy if you want it.
6. **The tooltip and the locked DRY RUN box are drawn by Windows.** They pass (6.86 and 4.67), but they are
   measured from screenshots on this PC's Windows 11 build. Restyling them would mean owner-drawing the tooltip.
   Not done.
7. **The hover button (4.87:1) is now the lowest normal pair.** It passes. Left as P84 set it.

## For Chase

- **Look at:** `scripts\shard-console-cache\screenshots\p87\after-uo-1280-tab0.png` against `before-uo-1300.png`,
  then open the console itself and narrow the window: the tiles drop to two rows and nothing cuts off.
- **The autopilot's commit failed on P86 because of the quotes in its subject** (see the top of these notes). The
  same will happen to any task title with a double quote in it. The fix belongs in `cc-autopilot.ps1` line 210:
  pass the message as base64, or through a temp file, rather than as a quoted `-File` argument. Not touched here.
- The two dirty `testing\` files in the docs repo will go into the next commit with this task.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run after this notes
file was written:

```
=== code  (D:\ShatteredLegacy) ===
  4 file(s) pending: CHANGELOG.md, VERSION, scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1
  dry run: would add, commit and push
=== docs  (D:\UO\shard-migration) ===
  6 file(s) pending: README.md, dashboard.html, testing/SUMMARY.md, testing/play-tests.json, tools/progress.json,
  notes/cc-P87-console-readability.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

P87 DONE
