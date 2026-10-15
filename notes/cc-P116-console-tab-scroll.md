# cc-P116: Console tabs scroll when their content does not fit, and the GOLEM tile counts the real queue

2026-10-15. Prompt: `D:\UO\cc-prompts\cc-P116-console-tab-scroll.md`. `scripts\Shard-Console.ps1` and its tests only,
plus the changelog. Not committed (the Golem commits after DONE). Both repos were clean at the start.

## Headlines

- **Every tab page now scrolls when its content does not fit.**
  - Five pages had parts that could fall off with no scroll bar: Golem, Websites, Shard question, Snapshots and Player
    package. Each now scrolls once it is smaller than what it needs.
  - The other six were already a single scrolling panel. They are unchanged, apart from captions now wrapping in the
    Plain look too.
  - **Proven by rendering:** every button, text box and drop-down on every tab is reachable at the console's minimum
    (900x700) and default (1200x1000) sizes, in the UO look with the action pane (a normal start) and in Plain.
- **The Golem tab's buttons show without scrolling at the default size.**
  - What I measured before the change: at 1200x1000 in the UO look with the pane, the tab page was **157 px** tall, and
    the Golem caption plus two rows of buttons needed about 190. Its second row of buttons was cut off, with no scroll
    bar: Chase's report.
  - The tab row now takes **38%** of the window's middle (was 30), taken from the Status box (36%, was 44). At the
    default size a page is **210 px** tall.
  - A page now **opens at its top** when you pick its tab. Before, a scrolling page jumped down to its first button
    and cut off the caption above it.
- **Captions wrap to the page width** in both looks; before, only UO did (cc-P87). They also widen again when the
  window grows: before, a fitted caption stayed narrow.
- **Rows that used to cut off now grow to fit** when they wrap: Player package's top row (its Build package button was
  cut off at 96 px in the UO look) and the button rows on Shard question, Snapshots and Player package.
- **The mouse wheel over a page scrolls that page**: a button passes the wheel up to its page. Proven by sending a
  real wheel message to a Golem button.
- **The GOLEM tile counts the queue folder.**
  - It now reads the folder listing the console already takes on every refresh, through `Get-AutopilotQueue`, its one
    copy of the runner's `cc-P<nn>-*.md` rule. Before, it read `status.json`'s `queued`, which goes stale while the
    Golem rests.
  - "N unnumbered file(s) ignored" is kept.
  - `status.json`'s list is used only when the folder cannot be listed.
  - It is right whether the Golem is running, idle, off or resting, before or after the cutover: the listing does not
    depend on who wrote `status.json`.
- **Tests:**
  - 5 new facts, each seen failing first. Two of them were also broken on purpose and restored.
  - **Three old failures fixed in the test file** (details under Tests): two that cascaded since the real Golem
    cutover, and one that assumed a scheduled task was never installed.
  - **Full suite under Windows PowerShell 5.1.26100: see the end of Tests.**

## The tab list

At the minimum size (900x700, UO look with the pane) and the default size (1200x1000):

| Tab | What it is | Now |
|---|---|---|
| Test shard | one scrolling panel (caption and buttons) | fitted (it already scrolled) |
| Fix test shard | one scrolling panel | fitted (it already scrolled) |
| Shard question | shard pick, question text, six answer buttons | **now scrolls**; the buttons wrap and their row grows |
| Snapshots | shard pick, list, note, name box and buttons | **now scrolls**; the button row grows when it wraps |
| World setup | one scrolling table | fitted (it already scrolled) |
| Diagnostics | one scrolling panel | fitted (it already scrolled) |
| Commit | one scrolling panel (message box, buttons, Force, countdown) | fitted (it already scrolled) |
| Player package | caption, notes and Build, zip list, Refresh/Check/Publish | **now scrolls**; the top and bottom rows grow to fit |
| Golem | caption, 12 buttons, the panel | **now scrolls**; the buttons show without scrolling at the default size |
| Websites | caption, site pick, 9 buttons, the panel | **now scrolls** |
| LIVE shard | one scrolling panel (greyed while live is retired) | fitted (it already scrolled) |

"Already scrolled" means the page's one child is a `FlowLayoutPanel` or `TableLayoutPanel` with `AutoScroll`: the two
containers the prompt counted (about lines 7203 and 7586). They cover seven of the eleven tabs.

**Measured before the change** (my probe; every control's bounds against each ancestor's client area):
- **UO look with the pane, 900x700:** unreachable on Shard question (the second row of answers), Snapshots (List,
  Restore, Delete), Player package (the notes box and Build package), Golem (all 12 buttons) and Websites (every
  button).
- **UO look with the pane, 1200x1000:** Golem's second row of buttons and Websites' Check now and its last row.
- **After:** all eleven tabs reachable at every size and look tried, including Chase's 1187x1200.

## What changed, with file:line (`D:\ShatteredLegacy`)

| File:line | Change |
|---|---|
| `scripts/Shard-Console.ps1:3628-3631` | `Get-AutopilotStatusGlance`: the count comes from `$View.Queue.Runs` (the folder, via `Get-AutopilotQueue`) when the folder was listed, else `status.json`'s `queued` |
| `scripts/Shard-Console.ps1:6309-6330` | `Update-CaptionFit`: both looks, to the tab page's width less 40 px (at most 1100, at least 300); a fitted caption is marked (`Tag = 'caption'`) so it can widen again; then calls `Update-PageScroll` |
| `scripts/Shard-Console.ps1:6332-6371` | `PageFillMin` (80 px) and `Update-PageScroll`. A page that is one scrolling panel is left to it. Any other page gets `AutoScroll` and an `AutoScrollMinSize`: the docked top and bottom parts at their own height (a wrapping part at the height it wraps to at this width), plus 80 px for the list or text that fills the rest; as wide as its widest single control |
| `scripts/Shard-Console.ps1:7522-7523`, `:7576`, `:7787-7788`, `:7819` | `AutoSize` with `GrowAndShrink` on four fixed-height rows: Shard question's answers, Snapshots' bottom row, and Player package's top and bottom rows |
| `scripts/Shard-Console.ps1:7936-7942` | on a tab change: `Update-PageScroll`, then (posted, after WinForms focuses the first button) the page goes back to its top |
| `scripts/Shard-Console.ps1:7969-7971` | pane mode rows: Status 36, tabs 38, output 26 (were 44, 30, 26) |
| `scripts/tests/Shard-Console.Tests.ps1:5248-5428` | the 5 new facts and their helpers (below) |
| `scripts/tests/Shard-Console.Tests.ps1:38-41`, `:84` | the fact runner re-pins `$config.Autopilot` before each fact (old failure 1, below) |
| `scripts/tests/Shard-Console.Tests.ps1:2910-2913` | `P74_TheTileAndTheTabAreBuiltAndDrawn`: a Golem root of its own, with no ACTIVE file (old failure 2) |
| `scripts/tests/Shard-Console.Tests.ps1:2963-2966` | `Get-ApsView -Queue`, default `$null` (a folder that could not be listed), so the cc-P94 facts keep testing `status.json`'s own list |
| `scripts/tests/Shard-Console.Tests.ps1:4886-4892` | `P107_TheSnapshotSendsNothing...`: "registered nothing" compares the task before and after the dry run (old failure 3) |
| `CHANGELOG.md`, `VERSION` | 2026.10.15.3, one `### Staff` line (today's 2026.10.15.2 was committed with P115) |

**The runner's rule, one copy.**
- **The Golem:** `D:\UO\golem\golem.ps1:200` and `:277-280` take `cc-P*.md` files matching `^cc-P(\d+)-`, lowest
  number first, and report any other `.md` as ignored.
- **The console:** its single copy is `Get-AutopilotQueue` (`Shard-Console.ps1:3362`), with the same pattern. It has
  listed the folder on every refresh since cc-P74 (`Get-AutopilotFacts`, `:4949`). The tile now uses that listing
  instead of a second source; no new rule was written.
- `golem.ps1` is outside both repos and runs as a hook, so the console cannot dot-source it.

## Tests

**New facts in `scripts\tests\Shard-Console.Tests.ps1`:** the form is shown off screen, because WinForms only lays out
a shown form.
1. **`P116_EveryTabScrollsOrFitsAtTheMinimumAndDefaultSize`:**
   - every button, text box and drop-down on every tab is reachable at 900x700 and 1200x1000, in UO with the pane and
     in Plain;
   - reachable means every ancestor either shows it inside its client area, or scrolls with a viewport at least one
     button tall;
   - in UO, the tab control also fits the window's width.
2. **`P116_TheGolemButtonsShowAtTheDefaultSizeAndScrollIntoViewAtTheMinimum`:**
   - at the default size the page opens at its top and all 9 Golem buttons are inside it with no scrolling;
   - at the minimum it scrolls, and its bottom button scrolls fully into view.
3. **`P116_TheMouseWheelOverAPageScrollsThatPage`:** a real `WM_MOUSEWHEEL` (one notch down) sent to a Golem button
   scrolls its page.
4. **`P116_LongCaptionsWrapToThePageWidth`:** at 900 wide, in both looks, no caption runs past its page.
5. **`P116_TheGolemTileCountsTheQueueFolderWhileStatusJsonIsStale`:**
   - in a temp Golem folder, `status.json` says IDLE (then OFF) with `queued: []`;
   - adding `cc-P114-...`, `cc-P115-...` and `notes for later.md` to the queue folder makes the tile say "2 queued" and
     "1 unnumbered file(s) ignored";
   - with no folder to list, `status.json`'s list is used.

**Seen failing first:**
- Against the code before the change: **4 of 5 failed.**
  1. Shard question's answers were outside their 52 px row (and the rest, as in the tab list above).
  2. "[Golem settings] at Y=155 in a page 157 tall."
  3. The wheel left the page at 0.
  5. "queue empty; 1 unnumbered file(s) ignored", with two numbered files there.
- **Fact 4 passed** before the change: UO already fitted its captions (cc-P87), and Plain's pages were wider than the
  window. So I broke it on purpose:
  - with `Update-CaptionFit` stubbed to return, it failed: "UO Snapshots: a caption 1063 wide runs to 1063 in a page
    853 wide";
  - restored, and `cmp` showed the file identical.
- **The "opens at its top" assertion** was added after a render showed the Golem page opening scrolled down. With the
  posted reset removed it failed ("expected [0] but got [67]"). Restored, `cmp` identical.
- After the change: **5 of 5.**

**Three old failures, found by the full suite and fixed in the test file only:**
1. **`P99_MoveToTheGolemAsksAPhraseAndRunsTheCutoverInAWindow`** (and the same cause made
   `P94_ThePanelSaysTheRunTheStepsTheActivityAndTheSettings` read `D:\UO\golem`).
   - The cause: every form built on the shared `$config` runs `Update-AutopilotView`. That re-picks the active folder
     (cc-P99, `:6456`), and since the real cutover (`D:\UO\golem\ACTIVE`) it picks the real Golem. So every later fact
     saw the real Golem.
   - **Proven at HEAD:** `TheFormBuildsFromACaptureWithoutBeingShown` and then this fact → FAIL; this fact alone →
     PASS.
   - **Fix:** the `Fact` runner re-pins `$config.Autopilot` to the pinned cc-autopilot folder before each fact.
2. **`P74_TheTileAndTheTabAreBuiltAndDrawn`** failed at HEAD too, even alone ("expected GOLEM: NEEDS YOU but got GOLEM:
   RUNNING"), for the same re-pick reason: its own form read the real Golem. It now uses a Golem root with no ACTIVE.
3. **`P107_TheSnapshotSendsNothingBeforeTheCutoverAndDryRunPrintsItsJson`** asserted that the scheduled task "SL game
   PC snapshot" does not exist. Chase has since installed it, so the fact always failed (P112 recorded the same).
   - Its point is "the dry run registered nothing". It now compares the task's exported registration before and after
     the dry run.

**Full suite, Windows PowerShell 5.1.26100.9444:**
- First run (before fixing the three old failures): **314 facts, 311 passed, 3 failed**: exactly those three.
- Second run (with fixes 1 and 2): **314 facts, 313 passed, 1 failed**, only P107. That run had loaded the test file
  before fix 3; alone, after it, P107 passes.
- **Final run, everything in place: 314 facts, 313 passed, 1 failed:
  `P84_TheUOLookAddsUnderASecondToTheStart`** ("UO adds 1047 ms").
  - That fact times building the window in each look and allows UO 1,000 ms more than Plain. It ran while another
    full suite and the commit dry run were also running.
  - **Alone, three times with my change:** 967, 1,115 and 221 ms (pass, fail, pass).
  - **At HEAD (stashed), twice:** 955 and 755 ms (both pass). Builds take 26 to 27 s either way.
  - So it sits close to its limit at HEAD too, and this change adds nothing measurable to a build. That is expected:
    the new resize handling runs only on a shown, resized form, and this fact never shows one.
  - **I did not loosen it.** It is listed under Deviations.
- **So the suite is green apart from one timing fact that is flaky at HEAD.** Not the "all green" the prompt asks for,
  stated plainly.

## Deviations and decisions for Chase

1. **The Status box is a little shorter.**
   - So that a tab's buttons show without scrolling at the default size, the tab row now takes 38% of the middle of
     the window (was 30) and the Status box 36% (was 44). This is in the normal start, with the action pane.
   - The Status box is mostly empty at that size and scrolls. The tiles above it, and the output pane, are unchanged.
   - Say if you would rather keep the old split; the tabs would then still scroll, just sooner.
2. **At the minimum size (900x700) a tab page is only about 67 px tall,** about one row of buttons. Everything is
   reachable by scrolling, but it is cramped: the tiles take two rows at that width and leave little room. The minimum
   size itself is unchanged.
3. **Plain look at 900 px wide:**
   - every page scrolls and its captions wrap;
   - but in Plain the whole console is still about 1,180 px wide, so it is cut off at the right below that. cc-P87
     fitted only the UO look to the window and left Plain as it was on purpose; I kept that decision. UO is the
     default look.
   - Fitting Plain to the window too would squeeze its single row of seven tiles. Say if you want it.
4. **While the Golem is running, the tile shows the run's position** ("P116 3 of 8"), as before, not a queue count.
   The queue count shows when it is idle or off, where the stale `status.json` misled it.
5. **I fixed three old test failures** that were not caused by this task. Each was proven to fail at HEAD; the causes
   are above.
6. **`P84_TheUOLookAddsUnderASecondToTheStart` is flaky at its limit, at HEAD as well.**
   - Building the window takes 26 to 27 s on this PC now (its comment says 15 s), and UO's extra time sits around 0.8
     to 0.95 s against a 1 s limit.
   - It failed once in the final full run and once in three runs alone, with or without this change.
   - **Options:** raise the limit or compare medians (a test change, the overseer's call), or look at why a window
     build now takes 26 s (a separate task). I changed neither.

## For Chase

Close and reopen the Shard Console: every tab scrolls when it does not fit (the Golem tab's buttons now show at the
normal size), and the GOLEM tile counts what is in the queue folder.

## Repo size

- No pending file over 5 MB. The largest changed file is `Shard-Console.ps1` (about 8,200 lines, under 600 KB).
- The probe script and its screenshots stayed in my session scratchpad, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the code was final:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code:** `CHANGELOG.md`, `VERSION`, `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`.
- **docs:** this note, plus the importer's `testing/SUMMARY.md` and `testing/play-tests.json` if they changed (machine
  output).

P116 DONE
