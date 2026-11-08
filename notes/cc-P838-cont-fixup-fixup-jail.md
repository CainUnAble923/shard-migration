# cc-P838: fix-up of P820 (the New Haven jail) after its build review (P828) said FAIL

## In plain words

- **The jail cells now look shut.** In the New Haven jail, the bars across the three cells used to show as short
  stubs pointing into the hall. There were also open gaps where the cell walls met the bars. The bars now run in one
  straight line with the cell gates, and each cell wall meets them with no gap. Both versions are fixed: main's SoS New
  Haven and the testers' New Haven.
- **The hall's candelabra moved off the west cell's gate.** It now stands beside the warden, so Finn's gate is in
  view.
- **A world that already has the jail fixes itself on the next start.** The old bars, the old wall ends and the
  candelabra are swapped on load.
- **For you:** the overseer applies `notes\cc-P838-tools\p838-release-isle-20261028.diff` to the release branch,
  instead of P820's diff. Nothing to decide.

Iron Golem, 2026-11-08, on `golem/Iron/P838` in both copies, not committed. The release copy is
`D:\UO\golems\Iron\p838-isle`, a detached worktree at `56f98af` (still the tip of `release/isle-20261028`) with the whole
change staged; mine to remove after the merge. Nothing went to the release branch and nothing was deployed. All play
ran on the private proof shard, 127.0.0.1:2596, under the test-shard lock.

## Bringing P820 in

The prompt says to check out `golem/Iron/P820` and merge `main`. The hand-off says to stay on `golem/Iron/P838` and
not merge or switch branches. P838 stood at main, so I took P820's one commit in each copy with
`git cherry-pick --no-commit`, as P827 and P837 did. The end state is main plus P820. P820's commit carries P801's
whole jail, so merging P838 lands P801, P820 and these fixes. P820's commits delete no files.

- Docs copy: applied cleanly.
- Code copy: two conflicts.
  - `VERSION`: the higher, `2026.11.08.1`.
  - `CHANGELOG.md`: both sets of lines go under the newer heading **2026.11.08.1**. Main's Added, Changed and Staff
    lines come first, then P820's jail lines under Changed and Fixed. This fix-up adds one more Fixed line.

## The reviewer's items (P828)

**1. Cell bars 0x0821 in an east-west row face north-south: fixed.**
- **The render first (guide 11.2).** `notes/cc-P838-tools/bar-test.jpg` (made by `bar_test838.py`) draws 0x0821,
  0x0822 and 0x0823 each in an east-west row with the cell gate 0x0828 in the middle, on the stock land by the jail.
  - 0x0821 draws a short north-south stub on each tile, which is the reviewer's reading.
  - 0x0822 draws an L on each tile.
  - 0x0823 draws one closed east-west line that runs on through the gate.
- **The generator.** `notes/cc-P801-tools/gen_jail.py` `BAR_EW` is now **0x0823**, and `TutorialJailLayout.cs` is
  regenerated. The four bar tiles are layout (1,3), (4,3), (6,3) and (8,3):
  - main: 3703, 3706, 3708 and 3710 at y 2637, Z 21;
  - release: 3470, 3473, 3475 and 3477 at y 2600, Z 11.
- **Older worlds.** `TutorialJail.Retired` now lists 0x0821 on those four tiles, so a world seeded by P801 or P820
  swaps them on load. The layout's new 0x0823 is then placed as missing.
- **Fact:** `TheCellFrontIsOneClosedEastWestLine`. No 0x0821 anywhere in the layout. Along the bar row x 1..9, each
  tile holds exactly the gate (x 2, 5, 9), the L corner (x 3, 7) or 0x0823.

**2. A one-tile gap where each cell wall meets the bar row: fixed.**
- **The generator.** The dividers at layout x 3 and x 7 now end at y 3 in the grey brick L corner **0x0033**, in place
  of the plain "east" piece 0x0035. The L closes the tile's south edge too, the same pattern as the building's outer
  south-east corner (guide 2.2). The rest of each divider (y 1, 2) keeps 0x0035.
  - main: 3705,2637,21 and 3709,2637,21;
  - release: 3472,2600,11 and 3476,2600,11.
- **Seen in the renders.** The roof-off renders (`render-sos-after-roofless.jpg`, `render-stock-after-roofless.jpg`)
  show the front as bars, then the L's brick end, then bars, with no floor showing through. The reviewer's fallback (a
  0x0823 bar stacked on the divider tile) was not needed.
- **Older worlds.** `Retired` lists 0x0035 on exactly those two tiles. Only that ID on those tiles goes, so each
  divider's other 0x0035 pieces stay.
- **Fact:** `EachDividerEndsInTheLCornerAtTheBars`. The L is there, no 0x0035 is in the bar row, and the run's
  0x0035 at y 1 stays.

**The reviewer's advice (the candelabra at (2,4) in front of the west cell's gate): taken.**
- **The move.** The candelabra 0x0B26 is at layout **(1,4)** now, beside the warden at (1,5):
  - main: 3703,2638,21;
  - release: 3470,2601,11.
- **Why it fits there.** It is off the west window's floor tile (1,6). At 15 high it stays under the west eave
  (floor + 19 on that column), so P820's roof fix still holds: the roof-on renders show no patch.
- **Older worlds.** `Retired` lists the candelabra on (2,4).
- **Facts.** `NoLightStandsInFrontOfACellGate` is new. P820's `NoTorchHangsOnAWindowAndNoneComesThroughTheEave` now
  expects the candelabra at (1,4), and its exclusion list names 0x0823 instead of 0x0821.

**An older jail on load:** `AP820JailGetsTheNewFrontOnLoad`.
- It places P801/P820's seven old pieces on a seeded jail and loads.
- All seven go ("removed 7 old ones"), and every piece of the current bar row is there.
- A second load removes nothing.
- P820's `AnOlderJailIsPutRightOnLoad` now counts `Retired.Length` (10) instead of 3.

## Tests and builds

- **Red first.** P820's own `TutorialJail.cs` and `TutorialJailLayout.cs` were put back (`red/p820-front/`) under
  the new facts, on `sl-uo-builder:cc-P832` (main's tip). **5 failed, 25 passed**: the four new facts and the changed
  candelabra fact (`red-p820-front.txt`).
- **Green.** The jail, tutorial and trade-trial facts: **72 of 72** (`probe-clean.txt`).
- **Gated builds** (the docker\uo build script, via `both-builds.ps1` and `isle-build.ps1`, under the docker-build
  lock):
  - **Main** `sl-modernuo:cc-P838`: **EXIT=0, 3337 shard tests passing** (`gated-build.log`).
  - **Release** `sl-modernuo:cc-P838-isle`: the first run failed one fact outside this change (`gated-build-isle.run1.log`).
    The fact was `DeathHooksVerification.AKilledNonBondedPetPaysNoImbueKillEffect`, which failed with
    `MissingMethodException: Cannot dynamically create an instance of type 'Server.Items.DaemonClaw'`. The rerun
    passed: **EXIT=0, 3000 passing** (`gated-build-isle.log`). See the flag below.

## Proof in TazUO

Both builds were walked by a fresh Player-account character, each on a fresh copy of the bot world on the private
proof shard (`run838.ps1`, P820's kit copied and repointed).
- **The route.** The character walked in through the real door, met the five people, took from the crate and put
  the pouch back, read the ledger, called the guards and walked out.
- **Result.** `walk-main.log` and `walk-isle.log`: **23 PASS, 0 FAIL each**.
- **The seed.** Both worlds were fresh: `shard.log` reads "placed 272 pieces, removed 0 old ones". The upgrade of an
  older jail is proven by the facts above, not by these runs.

## What is in `notes\cc-P838-review\`

- **`placed.md`:** every piece on both plots, from `make_placed.py`. It also lists what a P801 or P820 world loses
  on load.
- **The isorenders,** roof on and roof off, for both lands: `render-sos-after*.jpg` and `render-stock-after*.jpg`.
  The crate and ledger are drawn in at their server spots.
- **The TazUO shots:** `shots-main\` and `shots-isle\`, all of the walk's shots. The closed fronts are clearest in
  `2-hall-window-open.jpg` and `2b-hall-window-closed.jpg`.
- **Before and after:** `cell-fronts-before-after-main.jpg` and `-isle.jpg` put P820's hall shot (left) beside the new
  one (right).
- **The fence art test:** `notes\cc-P838-tools\bar-test.jpg`.

## Flag for the overseer (not fixed here)

There is a random failure in Butcher's Eye, `ClusterFImbueEffects.ButcherOn`, on main and on the release alike.
- **What fails.** The rare-part roll calls `Activator.CreateInstance` on a random name from `ButchersEyeRareParts`.
  One of those names, `DaemonClaw`, has no parameterless constructor, so whenever the roll lands on it the kill throws.
- **Why it is not fixed here.** It has nothing to do with the jail, and no file of it changed here.
- **The fix it needs.** Drop that name from the table, or guard the create. Until then a gated build can fail at
  random on `AKilledNonBondedPetPaysNoImbueKillEffect`, as this release build's first run did.

## Files

- **Code copy:**
  - P820's 13 files (P801's jail with P820's fixes, merged with main as above);
  - from this task: `TutorialJail.cs` (Retired), `TutorialJailLayout.cs` (regenerated) and
    `TutorialJailVerification.cs` (section 10);
  - `CHANGELOG.md` and `VERSION`.
- **Release copy `D:\UO\golems\Iron\p838-isle`:** P820's release change plus the same three files and the changelog
  line. `notes/cc-P838-tools/p838-release-isle-20261028.diff` (13 files, made against `56f98af`) **replaces
  `notes/cc-P820-tools/p820-release-isle-20261028.diff`**.
- **Docs copy:**
  - P820's notes, review folder and tools, plus P801's, from the cherry-pick;
  - `notes/cc-P801-tools/gen_jail.py` (the fixes);
  - `notes/cc-P838-tools/` (the fence test, probes, the red mutant, build scripts and logs, the walk kit and logs,
    `make_placed.py`, the release diff);
  - `notes/cc-P838-review/`;
  - this file.

P838 DONE
