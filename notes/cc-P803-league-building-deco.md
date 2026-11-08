# cc-P803: New Haven League building: replace the bulletin board and a full decoration review

## In plain words

- **The League board in New Haven's League office hangs on a wall now.** On the testers' version it stood in the front
  doorway, half hidden by the door and facing the wrong way. It now hangs on the wall just inside, to the left as you
  come in, and faces the room. It is the same board: double-click it to read the League's requisitions. If a world
  somehow has two League boards in the office, only one is kept.
- **The office is tidied.** The bookcases face the room, and nothing stands in front of a window any more: a
  flowerpot is gone, and a chest, a bookcase and a candelabra moved. Outside, a proper standing signpost names the
  League by the corner on the street side, and a League banner hangs on the wall by the ankh.
- **On main (the new town) the same board fix is made.** It hangs on the hall's north wall. Main's bookcases now face
  the room, and its sign sticks out from the wall.
- **For you:** the overseer applies `notes\cc-P803-tools\p803-release-isle-20261028.diff` to the release branch. A
  world that already has the old office changes by itself when the shard starts. Nothing else to decide.

## State

Iron Golem, 2026-11-07, on `golem/Iron/P803` in both copies, not committed. P799, P806 and P814 are on main and on the
release branch (`56f98af`), which is what Chase's answer of 11-06 was waiting for. The release copy is
`D:\UO\golems\Iron\p803-isle`, a detached worktree at `56f98af` with the change uncommitted. Its diff is
`notes\cc-P803-tools\p803-release-isle-20261028.diff` (10 files; it reverses cleanly). `latest` was not moved, nothing
was published and nothing went to the release branch. All play ran on the private proof shard, 127.0.0.1:2596.

**The second session (11-07 evening, after Chase's "rerun the gated builds and take the after shots").** The first
builds had finished green after all. The first after run then found a real bug: **two League boards in the release
office** (`shots-release-after-run1\`). The overnight bot world is a main world, and release images have run on it too,
so it holds a League board on each town's old spot. The release had listed main's old spot (3662,2547) as one of its
own. It moved that board across town, stopped at the first board it found, and left its own board in the doorway. Main
had the same weakness the other way round. Fixed in both copies (section 2), facts added and seen red first, both
gated builds run again (green), and the after run repeated: one board in each office, and it opens (section 5).

## 1. The review: what read wrong

Before renders and TazUO shots: `notes\cc-P803-review\render-*-before-*.jpg` and `shots-release-before\`,
`shots-main-before\`. I read every piece's facing from renders against a wall (`board-facings.png`,
`piece-facings*.png`), not from names. Building guide sections in brackets.

**Isle release (the ML New Haven house, walls x3453-3462, y2596-2603, floor Z 18, door in the north wall at 3459,2596):**

1. **The bulletin board.** This is the League requisitions board (`RequisitionsBoard`, cc-P150), seeded at
   3459,2596,18. That is the front door's own tile, in the north wall's line: the door and its frame draw over it. Its
   art, 0x1E5E, is the face that hangs on a west wall, so on a north wall it stood edge-on. It worked (double-click
   opened it in the before run) but read as a stray board in the doorway. (2.4, 3)
2. **Bookcase 0x0A99 at 3461,2597** faces east, so in the north-east corner it showed its back to the room. (3)
3. **Four pieces on window floor tiles:** flowerpot 3460,2597 and chest 3456,2597 (north windows), candelabra
   3461,2602 (east window), bookcase 3454,2602 (west window). (11.4, 11.13)
4. **The sign:** the arm 0x0B97 and its board 0x0BCF stood at 3463,2597. No wall stands north of that tile for an arm
   to hang from, and the roof's eave covers it. (2.5, 6, 11.12)
5. **Nothing outside says League.** The isle lodge got League banners (P720); this office had none.
6. Kept as they are: the desk with its books, inkwell, scroll and hourglass; the map's bed, dresser, rug and stretched
   hide; the potted tree by the door; the ankh dais (P799).

**Main (SoS Haven's hall, walls x3658-3674, y2547-2562, floor Z 0, open arch at 3667-3668,2562):**

1. **The board** stood on 3662,2547, the north wall's own tile, with the same west-wall art.
2. **Three east-facing bookcases on the north wall:** 0x0A99 at 3660,2548, and 0x0A9A at 3661,2548 and 3670,2548.
3. **The sign arm was 0x0B97,** which lies along a wall, under the window at 3670,2562.
4. **Not changed, for a later prompt:** the hall is still the map's barber or tailor shop: dressers with mirrors, wig
   stands, display cases, a long counter. A League office in it would need its own design pass. I only fixed what
   broke the guide's rules.

## 2. The board

- Same function, same item: the League requisitions board, the one players use. It is not a stock bulletin board, so
  there is nothing to post. Its use is to open it, read the requests guild by guild and turn items in. **"Post and read
  a message" in the prompt does not fit this board.** The proof is that a Player character opens it and reads it in
  TazUO (2.4 below).
- Release: 3458,2598,18, art 0x1E5E (hangs on a west wall), against the dividing wall x3457. That is the first wall you
  face as you come in, north of the doorway's approach (3458,2599) and clear of every door's swing.
- Main: 3662,2548,0, art 0x1E5F (hangs on a north wall), between main's bookcases and the flowerpot.
- An existing world: `ClusterFRequisitionSeeder` (every load) moves a League board found on an old spot to the new one
  and sets the art. It is the same item, so nothing changes for players. A new world gets it there directly.
  (`Appraiser.cs`: `OfficeBoard`, `OfficeBoardItemID`, `OldOfficeBoardSpots`, `MoveOldOfficeBoard`.)
- Each copy lists only its own town's old spots. The release lists the ML house door (3459,2596,18) only: SoS Haven's
  hall is another building there, and a board in it is left alone. Main lists both, because main's New Haven was the
  ML town before P678.
- Every League board on an old spot is handled. The first moves to the wall when the wall has none, and any other is
  a duplicate and is deleted, so the office never shows two. A League board holds no state (its guild key is empty),
  so nothing is lost. Script: `notes\cc-P803-tools\edit_board_dupes.py`; the copies from before it are
  `Appraiser-*.pre-dupes.cs`.

## 3. The decoration

Every piece is in `notes\cc-P803-review\placed.md` with its tile, facing and wall. The design files are
`design/registrar-office/layout.json` in each copy, edited by `notes\cc-P803-tools\edit_layouts.py` and turned into
code by `notes\cc-P803-tools\gen_office_layout.py`. Registered stock art only.

- Release: bookcase 0x0A98 (south face) at 3461,2597; candelabra to 3461,2601; flowerpot gone; chest 0x0E42 at the
  bed's foot, 3455,2598; quarters bookcase to 3454,2599 on the plain west wall; standing signpost 0xA854 "League of
  Extraordinary Citizens" at 3463,2596 (grass, road just north, clear of the eave: guide 11.12 for a north-door house);
  League banner 0x1589 at 3463,2599,26 on the east wall, between its two windows.
- Main: bookcases 0x0A98, 0x0A97 and 0x0A98 (south faces) on the north wall; sign arm 0x0B98 with board 0x0BCF at
  3670,2563.
- **The world changes by itself.** A seeded office addon never changes, because `BaseAddon` builds its parts once. So
  `ClusterFRegistrarOfficeSeeder` now runs `UpgradeStale` after every world load (setting
  `clusterf.registrarOffice.upgradeOnWorldLoad`, default true). If the office decor on the world is not the current
  layout, it swaps it with the existing `replace`. It changes nothing when there is no office decor (seeding a fresh
  world is still `seedOnWorldLoad`, default off, or `[ClusterFSeedRegistrarOffice`). It also leaves decor alone when any
  of it stands outside this layout's building, so a world whose office is in the other town's house is never touched.

## 4. Tests and builds

Probes on the builder images with the changed files dropped in (`notes\cc-P803-tools\probe.sh`): main on
`sl-uo-builder:cc-p817`, release on `sl-uo-builder:isle12-20261107`. Filter: `RegistrarOfficeVerification`,
`LeagueOfficeDecorVerification`, `RequisitionsVerification`. **27 of 27 passed on each** after the duplicate fix
(`probe-main.txt`, `probe-release.txt`; 26 before it). `probe.sh` wrote a relative output path into the code copy
(it changes into the repo first). It now resolves the path first and builds UOContent before the tests.

- Duplicate fix facts: `ASecondBoardOnAnOldSpotIsRemovedSoTheOfficeShowsOne` (a board on every old spot, with and
  without one already on the wall, leaves exactly one, on the wall) and, on the release only,
  `ABoardInSoSHavensHallIsAnotherBuildingHereAndIsLeftAlone`. Red first: with the old `MoveOldOfficeBoard` put back,
  both fail and the other five pass (`red-dupes.txt`).

- New facts, `server/tests/Misc/LeagueOfficeDecorVerification.cs` (one per copy, written by `make_facts.py` from the
  template with each town's walls and windows): the board hangs in front of its wall with that wall's art; a board on
  either old spot moves and stays the same item; no floor prop stands on a window's floor tile; every bookcase stands
  on the wall its art backs onto; a stale office is swapped on load, while a current one, or one in another building,
  is left alone.
- Red first (`red.sh`, `red.txt`, release): with each fix put back, the matching fact fails, and clean is 6 of 6.
  (The last mutation, "no upgrade on load", emptied the office search in both `Replace` and `UpgradeStale`, not
  `UpgradeStale` alone as I meant. The fact still went red.)
- Changed facts: on the release, `RegistrarOfficeVerification` counts 13 pieces (was 14), lists cc-P19's 11 leftover
  pieces (was 5) and reads the signpost 0xA854 at 3463,2596. On main, 0x0B98 left the banned-graphics list, since it
  is now the real sign arm; cc-P19's own tiles are still checked.
- Gated builds through `docker\uo\build.sh` (`builds.ps1`, under the `docker-build` lock), after the duplicate fix:
  release `sl-modernuo:cc-p803-isle` **EXIT=0, 2978 shard tests passing** (`gated-build-isle.log`), built from
  `release/isle-20261028` at `56f98af` (still the tip) with the diff; main `sl-modernuo:cc-p803` **EXIT=0, 3273
  passing** (`gated-build.log`). The first builds, before the fix, were green too (2977 and 3272,
  `gated-build*.run1.log`). `latest` was not moved.
- The release diff, `notes\cc-P803-tools\p803-release-isle-20261028.diff`, was made again after the fix (10 files);
  `git apply -R --check` passes on the release copy. The diff from before the fix is kept as `.pre-dupes`.

## 5. In TazUO

Before (`shots-release-before\`, `shots-main-before\`, walk logs `walk.txt`): on both towns a fresh Player character
found exactly one League board, on its old spot (release 3459,2596,18; main 3662,2547,0), and double-clicking it opened
the requisitions window (PASS). Two things to fix in the rig for the after run, both done in `Walk803.py`: the new
character lay in the wake pose in every shot (it now takes two steps first), and the login patch-notes window stayed
open behind the board (every window is now closed before each shot).

After, on the new images, each on a fresh copy of the bot world that still holds the old office and the old boards
(`shots-release-after\`, `shots-main-after\`):

- **Release: PASS.** One League board in the office, 0x1E5E at 3458,2598,18, and double-clicking it opens the League
  requisitions board window (`after-board-open.jpg`). `shard.log`: "League board: moved from (3459, 2596, 18) to (3458,
  2598, 18)", and "registrar office upgrade: the decor was an older layout; replacing it" (3 addons swapped). The shots
  show the board on the west wall, the bookcases facing the room, the banner on the east wall and the signpost at the
  corner.
- **Main: PASS.** One League board, 0x1E5F at 3662,2548,0, and it opens. `shard.log`: the board moved from (3662, 2547,
  0), and the stray release board at (3459, 2596, 18) was removed as a duplicate. The office decor on this world stands
  in the other house, so the upgrade left it alone, as it should.
- The first after run, before the duplicate fix, is kept as `shots-release-after-run1\` (FAIL: two boards) and
  `shots-main-after-run1\` (PASS).
- **"Post and read a message"** does not fit this board (section 2): it is the League requisitions board, not a
  message board. The proof is that a fresh Player character opens it and reads the requests.

## Files

- Code copy and release copy (`D:\UO\golems\Iron\p803-isle`, a detached worktree at `56f98af`, the release tip): `design/registrar-office/layout.json`,
  `server/customizations/ClusterFRegistrarOfficeLayout.cs` (generated), `ClusterFRegistrarOfficeSeeder.cs`,
  `Requisitions/Appraiser.cs`, `server/tests/Misc/LeagueOfficeDecorVerification.cs` (new),
  `RegistrarOfficeVerification.cs`, `RegistrarOfficeLayoutDesignCopy.cs` and `RegistrarOfficeLayoutP19Copy.cs`
  (generated), `CHANGELOG.md`, `VERSION`.
- Docs copy: this file, `notes\cc-P803-review\` (renders, shots, `placed.md`), `notes\cc-P803-tools\` (scripts, red
  runs, build logs, the release diff), and a new section 7 in `notes\map-building-playbook.md`.

P803 DONE
