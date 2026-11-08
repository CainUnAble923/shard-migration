# cc-P827: fix-up of P803 (the New Haven League office) after P824's build review

## In plain words

- **The League board no longer covers anything.** On the testers' version it hung over a stretched animal hide on the
  office wall. It now hangs at the south end of the writing desk. The hide hangs alone again, and the inkwell and scroll
  moved up the desk. On main it moved one step east, off the bookcase it was covering.
- **The League signpost on the testers' version faces the street.** It stood south of the road with its back to
  passers-by. It now stands on the verge north of the road, opposite the front door, and reads as you walk up.
- **On main, the hanging League sign is off the stained-glass window.** It hangs one wall piece east now, on plain
  wall. This time the photos show it, and the north wall with the board.
- **For you:** the overseer ships `notes\cc-P827-tools\p827-release-isle-20261028.diff` to the release branch instead
  of P803's diff. Nothing else to decide.

Iron Golem, 2026-11-08, on `golem/Iron/P827` in both copies, not committed. The release copy is still
`D:\UO\golems\Iron\p803-isle` (detached at `56f98af`, which is still the tip of `release/isle-20261028`), now holding
P803 plus this fix-up, uncommitted. `latest` was not moved and nothing was published. All play ran on the private proof
shard 127.0.0.1:2596, under the test-shard lock.

## Step 1: bringing P803 in

This step was not done as written. The prompt says to check out `golem/Iron/P803` and merge `main`. The hand-off says to
stay on `golem/Iron/P827` and not merge or switch branches. P827 was already at `main`, so I took P803's commits with
`git cherry-pick --no-commit`. In the docs copy that was two, WIP `1ab59fc` and `ef2488c`; neither deletes a file. In
the code copy it was one, `c5810b9`. The end state is the same.

The one conflict was `CHANGELOG.md`: P817/P823 had taken 2026.11.07.9. P803's lines went into a new section,
**2026.11.08**, and `VERSION` is 2026.11.08. The release keeps its own number from P803's diff (2026.11.07.2).

## The reviewer's items

Every spot was checked with `notes/cc-P803-tools/office_statics.py` against the map and rendered before I chose it.
The building guide's sections are in brackets.

**1. The release board 0x1E5E at 3458,2598 hung over the map's stretched hide on 3458,2597: fixed.**
- **No other free tile on the wall.** The office's west wall (the dividing wall x3457) has only one other tile with a
  wall behind it. 3457,2599 is the doorway to the quarters, and 3458,2600-2601 is the map's desk.
- **Its north wall is full too.** That wall holds the hide, the front door, a window and the bookcase.
- **The new spot.** The board hangs at **3458,2602,18**, south of the desk. That tile held the bookcase 0x0A9A, which
  was removed; the office keeps its north-wall case.
- **The desk.** Rendered there, the board's art reached over the desk's south end and covered the inkwell and scroll.
  Those two moved to the desk's north end, 3458,2600,24, beside the books and hourglass.
- **The render** (`release-board-desk-before-after.png`) shows the corner without and with the board. The board hangs
  over the bare end of the desk, and the hide stands alone.
- **Code.** The board's spot is `OfficeBoard` in `Appraiser.cs`. An existing world moves its board there on load. The
  proof run's log says: "moved from (3459, 2596, 18) to (3458, 2602, 18)".

**2. The release signpost 0xA854 at 3463,2596 stood south of the road, its back to the street: fixed.**
- **The new spot.** It now stands at **3460,2591,20**, on the verge just north of the road (road y 2592-2595).
- **Flat ground.** The tile is flat: land corners 20, 20, 20, 19. The cliff starts one row further north.
- **Off the door's line.** It stands one tile east of the door's line x3459 and four tiles north of the door.
- **Proof.** `shots-release-after/after-outside-door-side.jpg` and `after-outside-sign-from-the-street.jpg` show the
  board's face toward the road (guide 6).
- **The walk.** A real walk from the door's step north to the road, east past the sign and back (`walk.txt`) climbs
  15→17→19→20, at most 2 per step.

**3. The main sign arm 0x0B98 and board 0x0BCF at 3670,2563 hung on the stained-glass window: fixed.**
- **The new spot.** Both now hang at **3671,2563,0**, from a plain wall piece, 0x0034 at 3671,2562.
- **3671 against 3672.** I rendered both (`main-sign-3671-vs-3672.png`). At 3672 the arm touches the window at 3673;
  at 3671 it clears both windows.
- **The arch.** 3671 is three tiles east of the arch (2.5, 11.4, 11.12).

**4. The main board 0x1E5F at 3662,2548 covered the bookcase at 3661: fixed.**
- **The new spot.** The board hangs at **3663,2548,0**, so 3662 and 3664 are both empty.
- **The flowerpot.** It stood on 3663 and moved to the north-east corner, 3673,2548, beside the chest. I kept it
  rather than drop it, so main's piece counts stay as they were.
- **Proof.** `render-main-after-cutaway.jpg` shows the bookcases, the board and the map's pieces each whole.

**5. Main's changed decor had no TazUO shot: done.**
- **Seeding the office.** The main run now sends `[ClusterFSeedRegistrarOffice replace` before any shot
  (`stage827.py`, command `office`). On that world copy it deleted the office decor that stood in the other town's
  house and placed the current layout in the hall (`shots-main-after/stage-out.txt`).
- **`after-outside-door-side.jpg`.** It shows the League sign arm off plain wall between two windows, and the potted
  tree by the arch.
- **`after-inside-hall-north-wall.jpg` and `after-inside-hall.jpg`.** They show the bookcases, the board with a gap on
  each side, and the flowerpot in the north-east corner. The registrar and her neighbours stand in front of the north
  wall in some frames.
- **The board opens.** One League board in the hall, and double-clicking it opens it. On the release, the same.

**The reviewer's two "not fix" notes.**
- **The journal.** The rig closes every gump before each shot, so the door-side shots are clear.
- **Main's bookcase at 3670 beside the map's fish trophy.** Left as it was: it was there before P803.

## Walks

Both walks are real client steps, logged by `Walk827Rel.py` and `Walk827Main.py`
(`shots-*-after/walk.txt`):
- the release walk from the door's step north to the road, east past the signpost and back;
- the main walk in through the arch past the sign and out, then east along the front.

Every step moved, with no step over 2 Z. The script logged "FAIL walked out and back" for one reason only. The first
press after each change of direction only turns the character, and the script counted that turn as a step, so each
return ended one tile short. Each such press shows as "STUCK" in the log, and the next press in that direction moved.
No tile blocked the way.

## Tests and builds

- **New facts** in `server/tests/Misc/LeagueOfficeDecorVerification.cs`, one per copy, section 6, written by
  `notes/cc-P827-tools/add_facts.py`:
  - `TheBoardHasItsStretchOfWallToItself`: no office piece, and none of the map's own wall pieces, on the tile each
    side of the board along its wall.
  - On main, `TheSignArmHangsFromAPlainWallClearOfTheWindowsAndTheArch`.
  - On the release, `TheSignpostStandsNorthOfTheRoadOffTheDoorsLine`.
- **Red first.** With P803's spots put back, both new facts failed in each copy and the other 7 passed
  (`red-main.txt`, `red-release.txt`). Then the files were restored.
- **Changed facts.**
  - Main: `RegistrarOfficeVerification` reads the sign at 3671,2563.
  - Release: the layout has 12 pieces (was 13; the office group 6, was 7). The signpost is at 3460,2591,20. cc-P19's
    leftovers now include the desk's old inkwell and scroll and the west-wall bookcase.
- **Probes** on the builder images (`sl-uo-builder:cc-p803`, `cc-p803-isle`), filtered to the office, decor and
  requisitions facts: **29 of 29 passed in each copy** (`probe-main.txt`, `probe-release.txt`).
- **Gated builds** through `docker\uo\build.sh` under the docker-build lock (`builds.ps1`):
  - release `sl-modernuo:cc-P827-isle`: **EXIT=0, 2980 passing** (`gated-build-isle.log`);
  - main `sl-modernuo:cc-P827`: **EXIT=0, 3302 passing** (`gated-build.log`).
- **Release diff.** `notes/cc-P827-tools/p827-release-isle-20261028.diff` is P803's diff plus this fix-up (10 files).
  `git apply -R --check` passes on the release copy. It replaces `notes/cc-P803-tools/p803-release-isle-20261028.diff`.

## Files

- **Code copy and release copy:**
  - `design/registrar-office/layout.json`;
  - the generated `ClusterFRegistrarOfficeLayout.cs`, `RegistrarOfficeLayoutDesignCopy.cs` and
    `RegistrarOfficeLayoutP19Copy.cs`, by `notes/cc-P827-tools/edit_layouts.py` and then `gen_office_layout.py`;
  - `Requisitions/Appraiser.cs` (`OfficeBoard`);
  - `LeagueOfficeDecorVerification.cs` and `RegistrarOfficeVerification.cs`;
  - main only: `CHANGELOG.md` and `VERSION` (the merge, above).
- **The facts' generator.** `make_facts.py` in P803's tools is superseded by `add_facts.py` for these facts.
- **Docs copy:**
  - this file;
  - `notes/cc-P827-review/`: `placed.md`, the after isorenders, the two comparison renders, and the TazUO shots and walk
    logs in `shots-release-after/` and `shots-main-after/`;
  - `notes/cc-P827-tools/`: the scripts, the proof rig (a copy of P803's, pointing here), probe and red runs, build
    logs and the release diff;
  - P803's own files, from the cherry-pick.

P827 DONE
