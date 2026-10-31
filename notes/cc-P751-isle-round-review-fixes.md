# cc-P751: fix the seven items from P748's build review (isle coast, farm, farmhouse, lodge)

Iron Golem, 2026-10-31. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P751`. Nothing deployed, no package built, the shared Test Shard and Haven not touched. Not
committed (the Golem commits).

## In plain words

- **The isle round is fixed.** On the Wakening Isle the farmhouse fireplace now stands against the back wall under the
  middle of the roof, so the grey chimney no longer pokes through the thatch. Its door opens inward along the wall, and
  nothing stands in front of its windows. The farm fence closes neatly at both corners. Pictures:
  `notes\cc-P751-review\shots\tazuo-farmhouse-inside.jpg` and `tazuo-farmhouse-front.jpg`.
- **The League lodge has a name sign,** "The League lodge", beside the League lesson sign where the path turns to its
  door (`tazuo-lodge-front.jpg`). Beside the door itself, as the review asked, the roof hid it from the game's camera.
- **The beach below the training yard runs straight** along the yard's south and west sides, with no stepped edge
  (`tazuo-coast-yard-south.jpg`). The rest of the isle's land and planting is unchanged, tile for tile.
- **A real character walked the whole isle in the game,** the beach past the wreck, every lesson path, in and out of
  the farmhouse, bank and lodge doors, and out to the moongate and back: 292 steps, none blocked
  (`notes\cc-P751-review\isle-walk.log`, shots `walk-*.jpg`). Nothing for you to do; the branch goes to its build
  review.

## Getting P746's work onto this branch

The prompt says to check out `golem/Iron/P746` and merge main into it. The hand-off says not to switch branches, merge
or commit. So in both copies I applied P746's whole change (P741 plus P746, `git diff <fork point> golem/Iron/P746`)
onto `golem/Iron/P751` (which is main) with `git apply --3way`, uncommitted. The tree is the same as "P746 with main
merged in". The history differs: the Golem's commit carries P741's and P746's work as one commit, not as merged
commits.

- **No conflicts.** Since P746's fork point, main has changed none of the isle's files and not `trammel.mapops`. P708
  touched other files (the guild headquarters).
- **CHANGELOG and VERSION:** main's newest version is now 2026.10.31 (P708), so P741's six isle lines move out of the
  old 2026.10.30.3 into a new **2026.10.31.2** section. P751's four lines go there too, and VERSION is 2026.10.31.2.

## The seven items

1. **Review folder** `notes\cc-P751-review\`: `README.md`, `placed.md` (516 lines, by `make_placed.py`; it opens
   with what P751 changed and names the wall each farmhouse piece stands against), renders before and after, and
   TazUO shots and the walk log (item 6).
2. **Farm fence** (`notes\cc-P751-tools\gen_isle_farm.py`, P741's generator; it writes `TutorialIsleFarmLayout.cs`):
   the fence set is now the guide's: post **0x0838** at the north-west, **0x0835** the L corner at the south-east.
   - Pieces: 0x0838 at 6677,3967, one 0x0835 at 6695,3983, and one 0x0835 at 6695,3973. That last tile, where the
     pen's south row meets the east fence, had the same two-pieces-on-a-tile fault.
   - No tile has two fence pieces (render `after-fence-corners.jpg`, shots `tazuo-farm-fence-nw.jpg` and `-se.jpg`).
3. **Farmhouse fireplace:** pinned's StoneFireplaceSouth (0x0967 at 6702,3973 and 0x0961 at 6703,3973, Z 7), on the
   north wall under the ridge (x 6703), facing south into the room.
   - The roof over those columns is at Z 33 and 36. The fireplace's top is at Z 31. On the west wall it had been under
     Z 27 and 30.
   - Roof on, nothing shows above the thatch: `after-farmhouse.jpg`, and the TazUO shots `tazuo-farmhouse-front.jpg`
     and `tazuo-farmhouse-roof.jpg`.
   - **The windows, all of them.** My new fact checks every window's inside floor tile. It found three more pieces in
     front of a window, which P741's and P748's reviews had not caught:
     - the bed's foot (6704,3974);
     - the barrel (6700,3977);
     - the wooden box (6704,3977).
   - Moved:
     - the bed is now SmallBedEast (0x0A5D + 0x0A62) in the north-west corner;
     - the barrel goes along the west wall to 6700,3976;
     - the box goes to the north-east corner (6704,3973).
     - The north-wall torch moves to the west wall's plain piece (0x0A07 at 6700,3976, Z 20).
     - The chairs face the table by the art: 0x0B4F north, 0x0B50 south (guide 3).
4. **Farmhouse door:** `TutorialFarm.MakeIsleDoor` hangs `DarkWoodDoor(DoorFacing.WestCCW)` (closed art 0x06A9, open
   offset -1,0, along the south wall), as the bank and lodge do.
   - **On a world that already has the farm**, the seeder finds a door at the farmhouse door spot that is not 0x06A9,
     takes it away and hangs the new one, once (`TutorialFarm.IsleDoorClosedId`).
5. **League lodge sign:** a standing signpost 0xA854 named "The League lodge" at **6781,3989**
   (`TutorialCorePlacement.LodgeSign`, in `Props`, so an existing world gets it on the next load).
   - **Not where P748 asked.** I placed it first at 6784,3994: two east of the door, outside the north wall. In TazUO it
     stood behind the lodge's north eave from the game's camera, which looks from the south-east. It could not be seen
     from anywhere (`shots\tazuo-lodge-sign-at-6784-3994-hidden-1.jpg` and `-2.jpg`).
   - No wall hanger fits there either: every hanger (0x0B97-0x0B9A) hangs from a wall to its north (rendered against
     a wall on both sides).
   - So it stands north of the road where the walk to the door leaves it, beside the League lesson sign (6782,3989),
     as the chat lesson's two signs stand. That also matches the prompt's "north of the path".
   - The builder's sign gate now checks it with the lesson signs, and it passes. Shots: `tazuo-lodge-front.jpg`,
     `tazuo-lodge-door.jpg`.
6. **Walk proof: done, 19 of 19 legs, 292 of 292 steps** (`notes\cc-P751-review\isle-walk.log`). `walk_paths.py`
   turned the builder's walker (pinned movement rules, the server items in place) into the route `walk-paths.json`:
   - the west beach past the wreck;
   - every lesson leg from the wake spot (stop 0) to the dock end (stop 10);
   - in and out of the farmhouse (its step and door), the bank door and the lodge door;
   - the dock back to the land.

   `IsleWalk751.py` stepped Iron the Tester through TazUO along it tile by tile with the client's own steps (no
   teleport and no pathfinding: there was no RECOVER line). It logged each step's Z and the change from the step
   before, and asked for a shot at each door.
   - **Result:** no step changed Z by more than 4. 289 of 292 steps stood at the Z the builder's walker expected.
   - **The other three steps are on the moongate platform** at the dock end, (6829,3990) and (6830,3991). The game
     stands the Tester on its stone floor at Z 0 and 4; the builder's walker modelled the dock's -2 there. That is a
     gap in the walker's model, not a blocked step (shot `walk-dock-end-end.jpg`).
   - **Shots** (`notes\cc-P751-review\shots\`): `walk-<place>-mid.jpg` and `-end.jpg` for the beach, the farmhouse
     in and out (the client's "Opening door..." in the farmhouse shot), the bank in and out, the lodge in and out, the
     dock end and the dock back. There is also every fifth frame of the run (`isle-walk-f5.jpg` to `-f35.jpg`).
   - **The first run walked 2 of 19 legs** (`notes\cc-P751-tools\isle-walk-run1-sign-bug.log`). It was the script,
     not the map. Its `sign()` did bool math, `(v > 0) - (v < 0)`; in TazUO's IronPython that made direction keys that
     missed the table, so a step was logged STUCK without being tried. SL_Lumberjack hit the same trap on 2026-10-05.
     Plain ints fixed it, and the second run walked everything.

7. **The yard's south-west beach:** the coast there was the shape's gentle diagonal and a small spit (x 6728-6741,
   down to y 4018). Their one-tile stairs drew the saw-tooth however the surf pieces were chosen. My renders of
   alternatives showed that, and a test coast (`edge_test.py`) showed a straight south-facing run of 0x179F/0x17A0
   drawing a smooth surf line.
   - It is now two straight runs (`isle-sets.json` "straightCoast", `build_isle.shape`):
     - the west beach: first sand at x 6718 from y 4000 to 4014;
     - the south beach: first sand at y 4014 from x 6718 out to x 6752, joining the straight run that was already
       there;
     - the spit is sea.
   - **Only that window changed.** Changing the land's tile count re-rolls every seeded palm and tree on the isle. So
     `build_isle.plan_spliced` plans the isle without and with the straight coast and takes only the window (x
     6700-6760, y 4000-4025) from the second plan.
   - The patch differs from P746's only inside the window: 413 lines out, 387 in, 0 outside. Renders
     `before-coast-south.jpg` and `after-coast-south.jpg`; shots `tazuo-coast-yard-south.jpg`, `-west.jpg` and
     `-corner.jpg`.
   - **Not claimed:** the beach south of the farm road, further west, still steps tile by tile (bottom left of
     `tazuo-farmhouse-front.jpg`). P748's item was the yard's beach; that stretch is as P741 left it.

## Tests

- **New C# facts** (`server\tests\Tutorial\TutorialIsleReviewFixesVerification.cs`, 4). Each was seen failing on a
  mutant that undoes its own fix and nothing else (`mutate751.py`, `mutants.txt`):
  1. the fence's corners, one piece per tile;
  2. the hearth on the north wall under a roof higher than its top, and nothing before any window;
  3. the door hung WestCCW, and an old WestCW door rehung once;
  4. the lodge sign beside the League sign, placed once on an existing world.
- **Updated facts:** `TutorialIsleWalkFixes2Verification` (the hearth and bed art, the door art, the fence set),
  `TutorialIsleCoastVerification` (the fence set), and `TutorialFarmVerification` (the door art).
- **All Tutorial facts** on `sl-uo-builder:cc-P746` (main has not changed the Tutorial folders since P746): **247 of
  247** (`probe-tutorial.txt`).
- **Map facts** (`tools\tests\test_mapops.py`, `SL_SHARD_REPO` = the code copy): **14 of 14** (`test-mapops.txt`).
  - New fact 13: the yard's beach runs straight with its surf pieces, and no land south of it.
  - Seen failing on P746's patch: 12 rows of the west beach out of line (`red-map-fact-13.txt`).
- **The builder's gates** (`build-isle-ship.txt`):
  - every leg and lesson detour walks;
  - 25 of 25 spots fit;
  - the dock steps at most 2;
  - every lesson sign and the lodge sign stand north of their path;
  - the shipped patch round-trips (land identical, no block differing).
- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P751`, `docker-build` lock taken and released): **EXIT=0**,
  2,844 tests: 2,838 passed, 6 skipped, 0 failed (`green-gated-build.txt`). That was the second build, after the sign
  moved; the first was the same count.

## Live, on a private shard (127.0.0.1:2596, `test-shard` lock taken and released, container down)

- **Setup:** `proof-shard.ps1` on a fresh copy of the bot world, the image `sl-modernuo:cc-P751`, and the map overlay
  built by the test shard's own `Build-MapOverlay.ps1` from this branch's patch.
- **Seed on load** (`seed-on-load.txt`): "1 props" (the lodge sign); the farm relaid with its door ("placed 1 farm addon,
  3 door"); the old wreck swapped. The bot world predates P741, so the farm was laid fresh. The rehang of a WestCW door
  in place is proven by fact 3, not live.
- **TazUO shots** (default camera; `notes\cc-P751-review\shots\`):
  - the farmhouse: from the door side, inside, and the roof;
  - both fence corners;
  - the lodge: from the door side, with its sign;
  - the requested sign spot, hidden;
  - the yard's west and south beaches and their corner;
  - the bank front.

## Deviations and decisions for Chase

- **The walk ran in a second session** (2026-10-31, 16:45-17:00, Chase chose "Run it now"), with 11.6 GB free.
  The `test-shard` lock was taken and released, and the container is down. The walk script was fixed between its two
  runs (item 6).

- **Applied P746 onto P751 instead of checking out P746 and merging main** (the hand-off forbids switching branches
  and merging). Same tree, one commit.
- **The lodge sign is not two tiles east of the door** (item 5 above): there the roof hid it from the camera.
- **Three furniture moves the review did not list** (item 3): the bed, barrel and box stood before windows.
- **The CHANGELOG lines moved** to a new 2026.10.31.2. I did this after the second gated build, so that build did not
  see this CHANGELOG. The code and tests are unchanged since.
- **One search refused.** The unattended run denied a content search of the code copy for "CHANGELOG" in *.cs, *.py,
  *.sh and *.ps1 files. I wanted to confirm that no test or build step reads CHANGELOG.md's sections, before moving
  the isle lines. A shell grep that named `docker/uo/build.sh` was also stopped by the lock hook. The new section
  follows the file's own format.
- **The guide:** section 2.5's farmhouse furnishing is updated to the north-wall hearth. Section 11 has four new
  lessons (12-15):
  - wall signs hang only from a wall to the north;
  - check every window tile;
  - near coasts: straight runs, kept local;
  - the walker never entered a house.

## Files

- **Code copy:**
  - P741's and P746's files (see their notes);
  - `server/customizations/Tutorial/`: TutorialIsleFarmLayout.cs (regenerated), TutorialFarm.cs (the door and its
    rehang), TutorialCorePlacement.cs (the lodge sign);
  - `server/tests/Tutorial/`: TutorialIsleReviewFixesVerification.cs (new), TutorialIsleWalkFixes2Verification.cs,
    TutorialIsleCoastVerification.cs, TutorialFarmVerification.cs;
  - `player-package/vendor/shattered-legacy-map/trammel.mapops` (the yard's beach);
  - CHANGELOG.md, VERSION.
- **Docs copy:**
  - P741's and P746's files;
  - `notes/cc-P662-tools/build_isle.py` (straightCoast, plan_spliced, the lodge sign in the props and the sign gate),
    `isle-sets.json`, and the regenerated CSVs, reports and `plan-cells.json`;
  - `tools/tests/test_mapops.py` (fact 13);
  - `notes/guides/building-and-decorating.md`;
  - `notes/cc-P751-tools/` (generators, probe, mutants, walk route and script, proof scripts, logs);
  - `notes/cc-P751-review/`;
  - this file.


P751 DONE
