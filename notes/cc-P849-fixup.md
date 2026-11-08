# cc-P849: fix-up of P827 (the New Haven League office) after its build review (P836) said FAIL

## In plain words

- **The League requisitions board now hangs flat on its wall in both towns.** In New Haven's League field office the
  board stood edge-on, sticking out of the wall like a partition. The two pictures of the board had been swapped. On
  the testers' New Haven it now lies flat on the office's dividing wall, south of the desk. On main's New Haven it lies
  flat on the hall's north wall, beside the bookcases.
- **Worlds that already have the board turn it by themselves** the next time the shard starts. It is the same board,
  just the other picture.
- **The building guide now says which board picture goes on which wall**, from a render of both, so the swap does
  not come back.
- **For you:** the overseer applies `notes\cc-P849-tools\p849-release-isle-20261028.diff` to the release branch, in
  place of P827's diff. Nothing to decide.

Iron Golem, 2026-11-08, on `golem/Iron/P849` in both copies, not committed.

The release copy is `D:\UO\golems\Iron\p849-isle`, a detached worktree at `8f6eb2e` (the tip of
`release/isle-20261028`, update 13) with the whole change staged. It is mine to remove after the merge. Nothing went
to the release branch and nothing was deployed. All play ran on the private proof shard, 127.0.0.1:2596, under the
test-shard lock.

## Bringing P827 in

The prompt says to check out `golem/Iron/P827` and merge `main`. The hand-off says to stay on `golem/Iron/P849` and
not to commit, merge or switch branches. P849 stood at main (`6638331` code, `3776dddd` docs), so I ran
`git merge --no-commit --no-ff golem/Iron/P827` in each copy, as in P848. The end state is P827 with main merged in.
The unfinished merge (MERGE_HEAD) is left for the Golem's commit.
- Docs copy: merged cleanly.
- Code copy: two conflicts.
  - `VERSION`: **2026.11.08.3**.
  - `CHANGELOG.md`: a new **2026.11.08.3** section with P827's lines. Its Fixed line now says what is true after this
    fix: the board hangs flat on the north wall, and older worlds turn it.
- **Merging `main` again at the end:** `origin/main` is still `6638331` / `3776dddd` (fetched last), so there is
  nothing to merge.
- **Separate isle and main commits:** I do not commit (hand-off rule). The isle part is only the release diff in the
  docs copy. The main part is the code copy.

## The reviewer's items (P836)

**3 first: which art hangs on which wall.**
- **`board-sprites.png`** draws the two board arts beside the two grey-brick wall pieces.
  - 0x1E5E's frame runs the same way as 0x0034, the piece of a **north** wall (east-west).
  - 0x1E5F's frame runs the same way as 0x0035, the piece of a **west** wall (north-south).
- **`board-arts-on-walls.jpg`** (from `notes/cc-P849-tools/board_walls.py`) puts each art on the floor tile in front
  of a north wall and of a west wall, in four small rooms. 0x1E5E draws flat on the north wall and edge-on at the west
  wall. 0x1E5F does the opposite. The reviewer's reading is right.
- **Where the swap came from.** P803's `boards.json`/`board-facings.png` and the guide's Bank row ("0x1E5E bulletin
  board, east face") had them the wrong way round.
- **The guide.** Both rows in section 10 (Bank and Guild hall) of `notes/guides/building-and-decorating.md` now say:
  0x1E5E for a north wall (frame east-west, faces south), 0x1E5F for a west wall (north-south, faces east). Each row
  points at the render.

**1. Release board 0x1E5E edge-on from the west wall: fixed.**
- `OfficeBoardItemID` is now **0x1E5F** in the release copy, at the same spot, 3458,2602,18.
- `release-board-zoom.jpg` (from `release-board-before-after.jpg`) shows the result. The frame lies flat on x3457 and
  draws on the tile's west edge. Nothing reaches over the desk's south end.

**2. Main board 0x1E5F edge-on from the north wall: fixed.**
- `OfficeBoardItemID` is now **0x1E5E** in the main copy, at the same spot, 3663,2548,0.
- `main-board-zoom.jpg` shows the result: flat along the north wall, in line with the bookcases.

**Both copies, the code:**
- **`Appraiser.cs`.** The summary now records the right mapping and the swap. The load-time retag
  (`board.ItemID != OfficeBoardItemID`, unchanged) now logs "League board: art turned from 0x.... to 0x.... at ..."
  so a world's upgrade shows in `shard.log`.
- **`LeagueOfficeDecorVerification.cs`.**
  - `BoardArt` is set per copy.
  - The two places that mapped art to wall (`BoardArt == 0x1E5E ? post.X == room.WestX + 1 : ...` and the
    neighbour-tile choice) had the same swap. They now go through named constants: `NorthWallBoard = 0x1E5E`,
    `WestWallBoard = 0x1E5F`.
  - New fact `TheBoardsArtIsTheOneThatHangsFlatOnItsWall`: the board stands in front of exactly one wall, and its art
    is the one that hangs flat there.
  - New fact `ABoardWithTheEdgeOnArtIsTurnedOnLoadOnceAndStaysTheSameItem`: a League board on the spot with the other
    art is turned by one seed, keeps its serial, and a second seed turns nothing.
- **The script.** Both copies were changed by `notes/cc-P849-tools/fix_board_art.py <copy> north|west`.

## Tests and builds

- **Red first.** The new facts ran on P827's own `Appraiser.cs` (`red/main-p827-art`, `red/release-p827-art`):
  - main (`sl-uo-builder:cc-P837`): **5 failed, 14 passed** (`red-main.txt`);
  - release (`sl-uo-builder:isle13-20261108`): **4 failed, 15 passed** (`red-isle.txt`).
  - The first main run hit the xUnit2000 analyzer rule on an `Assert.Equal` with a constant. I rewrote that check as
    an `Assert.True` with a message, then ran again.
- **Green.** Main **19 of 19**, release **19 of 19** (`green-main.txt`, `green-isle.txt`).
- **Gated builds** (the docker\uo build script, through `both-builds.ps1`, under the docker-build lock):
  - **Main** `sl-modernuo:cc-p849`: **EXIT=0, 3326 passed, 6 skipped** (`gated-build.log`).
  - **Release** `sl-modernuo:cc-p849-isle` (update 13 plus the diff): **EXIT=0, 3025 passed, 5 skipped**
    (`gated-build-isle.log`).
- **The release diff.** `notes/cc-P849-tools/p849-release-isle-20261028.diff` (10 files, made against `8f6eb2e`) passes
  `git apply --cached --check` on `origin/release/isle-20261028` (`8f6eb2e`). It **replaces P827's diff**, which
  conflicted on update 13 in `CHANGELOG.md` and `VERSION` only.
  - Release changelog: a new section **2026.11.08.2** with P827's lines and the turned board.
  - Release `VERSION`: 2026.11.08.2.

## Proof in TazUO (`after849.ps1`, P827's kit with an art check)

Each image ran on a fresh copy of the bot world, and a fresh Player-account trainee walked the office.
- **Release** `sl-modernuo:cc-p849-isle`:
  - "board 0x1E5F at 3458,2602,18";
  - **PASS** one League board;
  - **PASS** "the board's art is 0x1E5F, the one for its west wall".
  - Run 1 (`shots-release-after-run1\`): **PASS** double-clicking opens it. In that run's board shot the trainee
    stood in front of the board.
  - Run 2 (`shots-release-after\`) shot the board from 3461,2598, where nothing stands in front of it. From there the
    board is 4 tiles away, out of use range, so that run's double-click check reads FAIL. Run 1 proves the board
    opens.
- **Main** `sl-modernuo:cc-p849`: "board 0x1E5E at 3663,2548,0", **PASS** one board, **PASS** the art for its north
  wall, **PASS** double-click opens it.
- **Older worlds, as seen in `shard.log`.** The bot world was made before P827, so each run's `shard.log` shows P827's
  move from the old spot, taking the new art. The release reads "moved from (3459, 2596, 18) to (3458, 2602, 18)". Main
  reads "moved from (3662, 2547, 0) to (3663, 2548, 0)". The turn of a board that already stands on its spot with the
  old art is proven by the fact above.
- **"walked out and back" reads FAIL in both runs, as it did in P827's own run.** It is the kit, not the building:
  - The first `API.Walk` in a new direction only turns the character. Each change of direction loses one step, so
    the walk ends one tile short.
  - Every real step through the doorway passed, both ways (`walk.txt`).
  - This fix changes no walkway.
- **Before and after:**
  - `board-before-after-release-tazuo.jpg`: P827's shot (left), this one (right).
  - `board-before-after-main-tazuo.jpg`: the same for main.

## What is in `notes\cc-P849-review\`

- **`placed.md`:** the board's new art in each town, what an existing world does, and P827's office list again (its
  two board rows corrected).
- **Item 3's renders:** `board-sprites.png` and `board-arts-on-walls.jpg`.
- **The isorenders** (`render_office.py`: each copy's layout, with the board drawn in with P827's art and with this
  fix's): `release-board-before-after.jpg`, `main-board-before-after.jpg`, and their zooms `release-board-zoom.jpg`
  and `main-board-zoom.jpg`.
- **The TazUO shots:** `shots-release-after\`, `shots-release-after-run1\`, `shots-main-after\`, and the two
  before/after sheets.

## Files

- **Code copy:** P827's merge, `server/customizations/Requisitions/Appraiser.cs`,
  `server/tests/Misc/LeagueOfficeDecorVerification.cs`, `CHANGELOG.md` and `VERSION`.
- **Release copy `D:\UO\golems\Iron\p849-isle`:** P827's release change and the same two files (west wall), plus
  `CHANGELOG.md` and `VERSION`.
- **Docs copy:**
  - P827's merge;
  - `notes/guides/building-and-decorating.md` (section 10, two rows);
  - `notes/cc-P849-tools/` (the renders, the fix script, probes, the red mutants, build scripts and logs, the walk kit,
    the release diff);
  - `notes/cc-P849-review/`;
  - this file.

P849 DONE
