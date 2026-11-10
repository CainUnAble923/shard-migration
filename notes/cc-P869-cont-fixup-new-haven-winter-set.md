# cc-P869: fix-up of P856 (New Haven's winter set) after its build review P865 said FAIL

## In plain words

- **Main's New Haven:** the four winter pieces now stand round the little garden with the pond and waterfall just
  south-east of the square, instead of in the wooded park west of the big hall. The Christmas train is on the open
  paving east of the garden, the snow globe at its west corner, the snowman bench along its south side and the Santa
  bench on the paving north-west of it. No tree and no other winter decoration stands within 3 tiles of any of them,
  so nothing covers them any more.
- **The testers' (release) New Haven:** the train moved from beside a walnut tree on the east side to open grass among
  the houses on the town's west hill. The Santa bench moved 2 tiles east, away from a tree, and the snow globe 1 tile,
  away from the dock's sleigh. The snowman bench stays where it was.
- The tool that picks the spots now checks for trees and other winter decorations by itself, so a later move can't
  put a piece back under a tree.
- **For you:** nothing new. As before, the release half is a file for the overseer to apply to the release branch
  (`notes\cc-P869-tools\p869-release-isle-20261028.diff`, which replaces P856's).

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy, both on `golem/Iron/P869`;
the release copy is my P856 worktree `D:\UO\golems\Iron\p856-isle` (release/isle-20261028 at `6459dd3` plus the
release half, staged, not committed). Read first: `notes\guides\building-and-decorating.md`. Stock art only, no
client or player package. All play on the private proof shard (2596) under the test-shard lock.

## Step 1: P856 onto this branch

The prompt says to check out `golem/Iron/P856` and merge main into it; the Golem's hand-off says not to switch
branches or merge. Same result without either: this branch is main, and `git cherry-pick --no-commit
origin/golem/Iron/P856` put P856's change into the working tree of both copies (left uncommitted for the Golem).
- shard-migration: clean.
- ShatteredLegacy: one conflict in `CHANGELOG.md`. P859 (merged since) took **2026.11.10.2** for the Horn of Plenty,
  the version P856 had used. P856's two lines now head a new **2026.11.10.3** section, and `VERSION` is 2026.11.10.3.
  `git cherry-pick --quit` cleared the pick state and kept the change.

## The reviewer's list (P865) and what I did

1. **Main snowman bench** (was 3618,2545,0, two park trees against its west side): moved to **3641,2600,0**, along
   the south side of the garden by the square. The nearest tree is more than 3 tiles away; the garden's juniper
   bushes and flower beds sit beside it, which the guide allows.
2. **Main Santa bench** (was 3613,2554,0, a cedar on each side): moved to **3622,2596,0**, on the paving at the
   garden's north-west side.
3. **Main large snow globe** (was 3639,2557,0, P678's decorated tree and snow pile in front and a walnut behind):
   moved to **3631,2603,0**, at the garden's west corner. None of P678's rows were moved.
4. **Release Christmas train** (was 3548,2523,14, a sapling inside its outline and a walnut beside the engine): moved
   to **3436,2614,43**, open grass among the houses on the release town's west hill. The reviewer suggested the grass
   north of the old spot, but it doesn't work: the ground there rises 3-6 z across the train's 21 tiles, and every
   flat origin within reach is still within 3 tiles of the walnut or the sapling (`notes/cc-P869-tools/nearrel.py`).
   The new spot is the nearest one that passes every rule. The train's area is now `west` (was `east`); the release
   test checks it.
5. **Shots and the finder:**
   - New rule, `notes/cc-P856-tools/keepclear.py`, used by both `find856.py` (main) and `rel/findrel.py` (release):
     no tree and none of P678's winter rows within 3 tiles of any tile a piece covers.
   - A tree is matched by its tiledata name: tree, leaves, sapling, palm, pine, fir, cypress, yew, spruce, birch,
     bamboo; a palm-frond roof, a stump and a potted tree don't count. The first version matched only
     tree/leaves/sapling/palm and missed the "tuscany pine" by the garden's pond (0x1B7E at 3638,2592). It would have
     let the Santa bench stand 1 tile from it, so I widened the names and searched again.
   - **Red first:** on P856's spots the rule flags all four main pieces, P865's items exactly, plus main's train
     (below), and the release train (`validate856.py` and `findrel.py --validate`, before the move).
   - **Green after:** all eight rows pass in both towns, and with all four pieces standing, the walk still reaches
     every tile it reached before (`placed.md`).
   - Shots retaken. The trainee now stands beside the middle of each piece's west or north side, so the camera frames
     the whole piece; both trains are whole in frame (`spots.py` chose the tiles).
   - `main-park.jpg`'s replacement is `main-garden.jpg` (the four pieces with P678's winter rows drawn), plus
     `main-old-park-empty.jpg`; `rel-train.jpg` and `rel-harbour.jpg` were redone. `placed.md` was regenerated.

### Where I went beyond the list, and why

- **Main's train moved too** (was 3612,2539,0; P865 passed it). The new rule caught a sapling inside its outline
  (0x0CE9 at 3610,2533), an o'hii tree one tile off its south end (the camera side) and a cedar 2 tiles west, the
  same faults as the release train. The whole park is wooded: no train spot there passes (`near.py`).
  - Candidates by the full rule: a farm field's edge at 3706,2615,20, a dirt road at 3681,2566, along a building's
    back wall at 3616,2592, and the open paving east of the square's garden at **3652,2595,0**. I rendered all four
    (`notes/cc-P869-tools/t-train-*.jpg`).
  - I took the garden spot: open paving, read from the default camera, the town's walk intact. P856's own prompt also
    asked for the set "on the square".
  - With the train there, the other three were placed round the same garden, which keeps the set together. The area
    is now `garden` for all four (was `park`, and `square` for the globe), so staff can still place or clear the set
    on its own (`[ClusterFWinterDecor place garden`).
- **Release Santa bench and globe nudged** (P865 passed both):
  - the Santa bench had an o'hii tree 2 tiles off its west end; it moved 2 east and 1 south to **3505,2589,16**;
  - the globe had P678's dock sleigh 3 tiles south, on its camera side; it moved 1 west and 1 north to
    **3518,2591,1**.
  - The release snowman bench stays at 3503,2596,1.
- **The set's own pieces are not held to the 3-tile rule against each other.** They keep P856's one-tile gap. The
  set is meant to stand as a group, and P865 passed the release harbour's Santa and snowman benches, which stand 3
  apart. "No other winter row" in item 5 is read as P678's rows. That was the rule P865's item 3 broke.

## Tests and builds

`WinterSetVerification` fact 5:
- **main** now checks that all four rows are in area `garden`. It fails on P856's rows (`park`, `square`), which is
  its red; I did not run a separate red build;
- **release** checks for area `west` (P856's rows have `east`).

The seeder's command help names the set's area (`garden` on main, `west` on release). No other code changed.

Gated builds (`notes/cc-P869-tools/both-builds.ps1`, docker-build lock, page cache dropped first; logs UTF-16;
`latest` not moved):
- main `sl-modernuo:cc-p869`: **EXIT=0, 3371 passed, 0 failed, 6 skipped** (`gated-build.log`); the six
  WinterSet facts and the WinterDecor facts among them.
- release `sl-modernuo:cc-p869-isle` (the p856-isle copy): **EXIT=0, 3070 passed, 5 skipped** (`gated-build-isle.log`).

The release half for the overseer: `notes/cc-P869-tools/p869-release-isle-20261028.diff`, 9 files, made with
`git diff --cached 6459dd3` in p856-isle. It passes `git apply --cached --check` against
`origin/release/isle-20261028`, which is still `6459dd3`. It replaces P856's diff, which I also rewrote in place
(`notes/cc-P856-tools/p856-release-isle-20261028.diff`) so the old file can't be applied by mistake.

## In game (TazUO, `notes\cc-P869-shots\`)

Private proof shard (2596) only, under the test-shard lock, a fresh copy of the bot world per run, release then main,
on the new images (`notes/cc-P869-tools/run869.ps1`, kits `kit/` and `kit-isle/` with `Walk869.py`).
- A Player-account trainee, "Iron Winter".
- Staff hands (`stage856.py`) put the decor up as December 1 would (`[ClusterFWinterDecor place`), set the trainee
  beside each piece, and cleared it all at the end.
- At each piece, the trainee's own client walked 4 tiles along its side and back (API.Walk, no teleport), logging
  each step's position and z.

**All 16 checks PASS** (`walk-main.txt`, `walk-release.txt` in the review folder): each piece's part is found at its
new spot, and each walk leg moves one tile a step with z within 2, in both towns. Free memory was low when the run
started (1.9 GB; the page cache drop did not help much), but both runs finished.

Shots (`notes\cc-P869-review\shots\`): `p869-main-*` and `p869-release-*`, one per piece, each piece whole and no
tree over it. The square on main is busy with pinned post-UOML undead spawns (P858 saw them too); not ours.

## Deviations and decisions for Chase

- Main's whole set moved from the park to the garden by the square, including the train, which the reviewer had
  passed (see "Where I went beyond the list").
- The release train is now on the west hill (z 43), about 110 tiles west of its old spot. No closer spot passes.
- Version 2026.11.10.3 for P856's lines (P859 took .2).
- `notes/cc-P869-tools/t-train-*.jpg` and `t-rel-train-w.jpg` are the candidate renders I chose from; kept for the
  reviewer.

## Files

- `ShatteredLegacy` (main): P856's change (`server/customizations/WinterSet/` 3 new, `ClusterFWinterDecorSeeder.cs`,
  `RewardStores/FestivalStore.cs`, `server/tests/Misc/WinterSetVerification.cs` new, `WinterDecorVerification.cs`,
  `CHANGELOG.md`, `VERSION`). On top of it: the new rows in `WinterSet/ClusterFWinterSetLayout.cs`, the area name in
  the seeder's help and in fact 5, and the version 2026.11.10.3.
- `p856-isle` (release, staged): the same for the release rows; the diff above.
- `shard-migration`:
  - P856's notes and tools, with `cc-P856-tools/keepclear.py` (new), `find856.py` and `rel/findrel.py` (the rule and
    the release rows), and the release diff rewritten;
  - this file;
  - `notes/cc-P869-tools/` (render869.py, near.py, nearrel.py, spots.py, the kits, run869.ps1, the build scripts and
    logs, the find results, the diff, the candidate renders);
  - `notes/cc-P869-review/` (placed.md, renders, shots, walk logs);
  - `notes/cc-P869-shots/` (the full runs).

P869 DONE
