# cc-P4: Fiddle-Me-This in the player package, and the unblock marker

2026-09-29. Brief: `D:\UO\cc-prompts\cc-P4-fiddle-me-this.md`. Nothing committed or deployed.
The dist\ zip was left alone: every build for this task went to the session scratchpad.

## What changed (all in `D:\ShatteredLegacy\player-package\`)

- `vendor\fiddle-me-this\`, new. Upstream `e1d2a09f` (2024-02-03; origin/HEAD is the same
  commit today), cloned with `core.autocrlf=false` so every file is the upstream blob. Upstream
  stores LF; a default Windows clone would have rewritten the XML and LICENSE to CRLF.
  Counted after the copy: `[Original]\ExternalImages\gumps` **107** PNG, `[Custom]\ExternalImages\gumps`
  **63** PNG, `[Custom]\Data\XmlGumps` **6** XML, `LICENSE-FiddleMeThis.txt`, `SOURCE.txt`. No
  filename appears in both gumps folders (case-insensitive comparison). PNGs are byte-identical
  to upstream (`diff -r`). The XMLs differ only on the `<gump x= y=>` line (`diff -r` shows five
  one-line hunks). Left out: `Images\`, `Art ID List.xlsx`, `README.md`.
- `Build-PlayerPackage.ps1`
  - `ExternalImages` added to the client exclusions (see finding 1).
  - Copies `[Original]` then `[Custom]` into `app\tazuo\ExternalImages\gumps\` and
    `app\tazuo\Data\XmlGumps\`, plus `LICENSE-FiddleMeThis.txt` next to `LICENSE-TazUO.txt`.
    `-LiteralPath` everywhere, because `[Original]` and `[Custom]` are wildcard patterns to `-Path`.
  - Stops if a name is in both `[Original]` and `[Custom]`, or if the staged gumps folder already
    has one of the names before the copy.
  - Gate 1: the old rule "any `app\tazuo\Data` is a leak" becomes an allowlist. `Data\` may hold
    only `XmlGumps\<vendored name>.xml`. Anything else is reported by path.
  - Gate 3 also byte-compares every staged Fiddle-Me-This file against `vendor\`.
  - New gate 4 reopens the finished zip and checks brief gates 1-5 against what actually shipped.
    A failing zip is deleted. `-CheckZip <path>` runs gate 4 alone against any zip, for example
    the one on `get.` before or after an upload.
  - `-GateSelfTest` also plants a fake `Data\Profiles\canary\`, `settings.db` and
    `gump_positions.db`.
- `payload\README.txt`: two lines under "What is in here" (credit with URL and CC0; the custom
  health/mana gumps are off until turned on from the TazUO top bar XmlGumps menu).
- `payload\app\Play.ps1`: marker file removed. The missing-client check now runs first and prints
  the brief's Extract All sentence. Unblocking happens whenever `TazUO.exe` still has a
  `Zone.Identifier` stream.

All four touched text files contain no byte above 127 (checked with perl).

## Findings, including where the brief was wrong

1. **The unchanged build would already have shipped 107 of these PNGs, unrecorded.** Chase's
   `D:\UO\TazUO\client\ExternalImages\gumps\` holds the 107 `[Original]` files, byte-identical,
   installed 2026-09-27 18:04. The build did not exclude `ExternalImages`, so a baseline build
   today with the old script produced 856 entries (749 in the 09-26 zip + 107). Brief B.2's
   "already staged" check would have failed every build on this machine. The fix: exclude
   the client's `ExternalImages` entirely, so overrides come only from `vendor\` and a local
   experiment cannot ship. TazUO creates the empty folders itself (`ExternalImageLoader.Load`).
2. **The old build excluded all of `Data\`, and gate 1 treated any staged `Data` as a leak.**
   B.3's assertion therefore did not exist in the needed form. It is now the allowlist above.
3. **The D-90 quest board does not draw with gumps 3500-3508.** `NewHavenQuestBoard.cs:397` uses
   background **9270**, and its buttons are 0xFA5/0xFA7/0xFAE/0xFB0. Fiddle-Me-This overrides none
   of these. No gump in `server/customizations` uses 3500 (the grep hits are gold and standing
   amounts). In pinned ModernUO, **8** files call `AddBackground(..., 3500)`: the six ConPVP gumps
   under `Engines/ConPVP/Gumps/`, `Engines/Help/PagePromptGump.cs` and `Gumps/VirtualCheckGump.cs`.
   The board is still worth a look (below) but is not the gump at risk. The help-page prompt is
   the most likely to be seen.
4. **No XML gump declares a size**, so by the brief's rule all six open at 0,0. Opened together
   they stack at the top-left corner. Whether 0,0 sits under TazUO's top bar is **unverified**;
   client check 4 covers it. A position computed from each background PNG's size would spread
   them out; I did not do that because the brief said 0,0.
5. **TazUO writes the position back into the XML** when a player moves or locks one of these
   gumps (`XmlGumpHandler.SaveFile`, `root.SetAttribute("x"...)`). So a player's placement sticks,
   and re-extracting over an old folder resets it to 0,0.
6. **Residual gap in Part C, by design of the brief.** Only `TazUO.exe` is probed. A re-extract
   over an already-unblocked folder that stops *before* reaching `TazUO.exe` leaves the old,
   unmarked exe in place, and the fresh files stay marked (probe case 2). A full re-extract,
   or a partial one that gets past `TazUO.exe`, is handled. Players are told to delete the
   folder and unzip again, which also avoids this case. Closing it fully would mean probing more
   files on every start.
7. Old folders keep a stale `app\.unblocked`. It is harmless, since nothing reads it now.

## TazUO source check

Both paths were read at **v26.0909.63** (`3212623f`, the shipped version; `v.txt` in the client
says 26.0909.63). `git diff v26.0909.63 7deed693` is empty for both files:

- `src/ClassicUO.Assets/ExternalImageLoader.cs:280`: `Path.Combine(AppContext.BaseDirectory,
  "ExternalImages", "gumps")`. It reads `*.png` and `*.bmp` recursively, and the file name is the
  gump ID (decimal, or hex with `0x`).
- `src/ClassicUO.Client/Game/UI/XmlGumpHandler.cs:21`: `Path.Combine(CUOEnviroment.ExecutablePath,
  "Data", "XmlGumps")`, `*.xml`. The root `x`, `y`, `locked` and `saveposition` are read at :45-66.

This does not contradict the brief. The one addition is finding 5.

## Position table (also in SOURCE.txt)

| File | before | after |
|---|---|---|
| Default Style HP Bar - Large.xml | 2053,746 | 0,0 |
| HP Bars Stacked - Large.xml | 514,1007 | 0,0 |
| HP Bars Stacked - Small.xml | 0,0 | 0,0 (unchanged upstream) |
| HP Orb.xml | 514,1007 | 0,0 |
| MP Orb.xml | 1872,1007 | 0,0 |
| Status Gump - Icons.xml | 2304,367 | 0,0 |

## Gates: red, then green

Gate 4 against real older zips (`-CheckZip`):

- 09-26 dist zip: red on 0 PNGs, 0 XmlGumps, no licence, and "Play.ps1 still references
  .unblocked" (brief gates 1, 2, 5).
- Today's baseline (old script): red on "107 PNGs, expected 170", 0 XmlGumps, no licence.

A doctored copy of the good zip had `HP Orb.xml` back at 514,1007 and `3500.png` removed. It also
had `app/.unblocked`, `Data/Profiles/canary/profile.json`, `Data/settings.db`,
`Data/settings.db.1`, `Data/gump_positions.db`, `Data/backups/x.db` and
`Data/Shattered Legacy/canary/journal.txt` added. It went red on all of them: 169 PNGs, the
position, all six Data paths listed, and `.unblocked` (brief gates 1, 3, 4, 5).

Build-time guards, each run through a scratchpad copy of the script and vendor tree (nothing in
the repo was altered to break it):

- A: `3500.png` in both `[Original]` and `[Custom]`. Red, and no zip was written.
- B: `ExternalImages` exclusion removed. Red: "already held 107 of its files before the copy".
- C: a staged vendored PNG was altered after the copy. Red at gate 3.
- D: `-GateSelfTest` on the real script. Red at gate 1: `Data\Profiles`, `Data\Profiles\canary`,
  `profile.json`, `gump_positions.db`, `settings.db` and `leak-canary.json` were all listed.
  (The first D attempt accidentally ran variant B, because PowerShell variable names are
  case-insensitive and `$B` overwrote `$b`. I reran it alone.)
- E: `HP Orb.xml` back at 514,1007 in the vendor copy. The zip was built, then red at gate 4,
  and the zip was deleted.
- Control: the unmodified variant was green.

Green: the real script built to the scratchpad and passed gate 4. I checked separately with
`unzip`: 926 entries (856 - 107 + 170 + 6 + 1), 170 PNGs, exactly the six XmlGumps under `Data/`,
both licences, all six at `x="0" y="0"`, and `\.unblocked` 0 times in the shipped `Play.ps1`. The
comment still uses the word "unblocked" in prose. Apart from the gumps folder, the only entries
not in the baseline are the 6 XMLs and the licence.

Part C probe: I extracted the new zip, planted `Zone.Identifier` streams, and ran `Play.ps1`
truncated before Setup. Results by case:

1. Fresh extract (41 marked): all cleared, no marker written.
2. Only non-exe files marked: stayed marked (finding 6).
3. `TazUO.exe` missing: the new message, exit 1, nothing unblocked.
4. Full re-extract over a used folder (927 marked): all cleared.

## Zip size

| zip | bytes |
|---|---|
| 09-26 dist (last shipped build) | 76,717,212 |
| today, old script (includes the 107 leaked from the client) | 78,476,404 |
| today, new script | 79,670,572 |

Against the 09-26 zip: **+2,953,360 (+2.8 MB)**. Fiddle-Me-This entries compress to 2,916,042 of
that. Against today's old-script build it is only +1.19 MB, because of finding 1.

## Client checks for Chase

- [ ] 1. Build (`.\player-package\Build-PlayerPackage.ps1`), unzip the new package fresh with
      Windows Extract All, launch, and log in.
- [ ] 2. The paperdoll, backpack, status bar and spellbook show the restyled art.
- [ ] 3. Open the New Haven quest board (D-90) and its 26-quest picker, and confirm they are
      readable. Per finding 3 it draws with 9270, which Fiddle-Me-This does not replace, so expect
      no change. The gumps that do use 3500 are the help-page prompt (`[help` then a page) and
      the ConPVP duel gumps. If convenient, look at the help prompt: press the paperdoll Help button,
      pick a page type, and check the text box. `PagePromptGump.cs:29` draws it on 3500.
- [ ] 4. From the top bar XmlGumps menu, open each of the six. Each appears on screen at 1920x1080
      at the top-left. Note whether any sits under the top bar (finding 4). Move one, relog, and
      confirm it reopens where you left it (finding 5).
- [ ] 5. On a machine with an old extract (it will still have `app\.unblocked`), re-unzip over it
      and confirm there is no SmartScreen prompt on start.
