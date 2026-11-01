# cc-P755: fix-up of P743 (New Haven tutorial fixes) after its build review (P754) said FAIL

## In plain words

- The signpost for the mountain path to the mining cave, south of New Haven, used to stand in the middle of the dirt
  road. It now stands on the grass just north of the road, at the edge of the trees. Players walk past it instead of
  round it.
- The stables signpost used to stand in the middle of the dirt lane outside the barn. It now stands on the barn's porch
  beside the hitching post, just north of the barn door.
- The first stop of the housing lesson moved 3 steps east, next to its signpost (they were 4 tiles apart). The arrow
  now leads to the spot beside the sign.
- Nothing for you to do. A second Golem reviews the new pictures, then P743 and this fix merge together.

## How the branch was made

Neither repo's main was touched. In both work copies, `golem/Iron/P755` (main at the P747 merge) has `golem/Iron/P743`
merged in, **not committed** (`git merge --no-commit --no-ff`; MERGE_HEAD is P743's tip: 350b5b3 in the code copy,
5ee616e in the docs copy). The hand-off says not to switch branches. So I merged P743 into this branch and did not
check out P743 and merge main into it. The tree is the same either way (P746 did the same). The Golem's commit makes
the merge commit.

- **Conflicts:** only `VERSION` and `CHANGELOG.md` in the code copy. Main had 2026.10.31.10 (P747) and 2026.10.31.9
  (P714). P743 had also used 2026.10.31.9. P743's section is now **2026.10.31.11**, above main's two sections, word for
  word. `VERSION` is 2026.10.31.11 (the shots' patch-notes window reads it).
- Everything else merged without a conflict. The full gated build below ran on the merged tree.

## The reviewer's list (P754), item by item

**1. 0xA854 signpost "The mountain path: the mining lesson's cave is west, round the hill", at 3702,2745 in the dirt
road: fixed.**

- I mapped the SoS land round it (`notes\cc-P755-tools\ascii755.py`). The road here is a dirt band 5 to 8 tiles wide.
  It runs from north-east to south-west, from the shore road (about 3712,2732) to 3690,2756. 3702,2745 is in the
  middle of it.
- The new spot is **3702,2742** (land Z 24), on grass. It passes the guide's section 6 rule:
  - road 2 tiles south of it (3702,2744);
  - no road north of it within 3 tiles, and none beside it (3701,2742 and 3703,2742 are grass);
  - no static on the tile, and the nearest trees (3696-3697,2742 and 3698,2744) are 4 or more tiles away;
  - the board (0xA854 reads from the south) faces the road.
- The reviewer suggested about 3703,2742. But 3704,2742 is dirt, so that tile has road beside it. 3702,2742 is the
  first tile in that row that passes.
- **Not on the walked route.** The shortest walk from the shore road to the cave (`notes\cc-P743-tools\route.py`
  3712,2725 to the cave) cuts through the forest further north-west, through 3702,2736 and 3699,2739. A player who
  follows the road walks the dirt band. Neither touches 3702,2742.
- The reviewer pointed at `notes/cc-P741-tools/sign_spots741.py`. That chooser only knows the Wakening Isle's build
  files, so I applied its rule by hand on the ASCII map and the render.
- The seeder's move-in-place step (`StrayPieces`) takes away a post a world already has at 3702,2745.
- Shown in `render-mountain-sign.jpg` (old spot ringed red, new green) and `mountain-path-sign-player.jpg` (the
  Tester on the road, the post on the grass edge north of him, nothing in the road).

## The Codex review's two flags on P754 (not on the reviewer's list): both fixed

The Codex review of P754 (`notes\cc-P754-review-build-new-haven-tutorial-fixes-codex-review.md`) said the list missed
two placements. I checked both against the guide and the map. Both flags hold, so I fixed them here rather than let
them cost another review round.

**A. The stables signpost at 3610,2613 stood in the dirt lane outside the barn: moved to 3608,2614.**

- The barn's east wall is x 3607 and its door is 3607,2615-2616. East of it is a dirt lane, 3608-3614 wide, between the
  barn and the stone house. 3610,2613 was in the middle of that lane.
- Column 3608 is the barn's porch strip under the eave. The map has hitching posts at 3608,2611 and 3608,2613, its
  own wooden signpost (0x0B97) at 3608,2611, and saddles at 3608,2618 and 3608,2620. People walk the lane, not this
  strip.
- **3608,2614** is between the hitching post at 3608,2613 and the door path (3608-3609, 2615-2616). It is therefore
  north of the walk into the door, beside it, with the board facing it.
- It is off the door's 2-tile approach line and out of the lane.
- On a north-south lane, no tile can meet the guide's literal test (road within 3 south, none north or beside) and also
  stay off the road. The porch strip is the closest fit.
- Shown in `render-stable-sign.jpg` (roofs off, old spot red), `render-stable-sign-roofs.jpg` and
  `stables-sign-player.jpg`. In the live shot the post stands under the eave by the hitching post, the lane clear.

**B. Housing stop 1 (3709,2594) was 4 tiles from its signpost (3713,2591); the guide says within 2: the stop moved to
3712,2593.**

- The sign itself already met the north-of-path rule (the dirt yard south of it, forest and grass north and east). The
  P754 reviewer passed it for that reason.
- So I moved the stop, not the sign. Every tile within 2 of the old stop is either the dirt yard or the cottage's
  south wall, so no sign could stand there by the rules.
- **3712,2593** is dirt in front of the cottage's south-east corner, Z 20. It is 1 tile west and 2 south of the sign.
- The cottage door (3707,2591, from `generated_doors`) is 5 tiles west, so the stop is off the door's line.
- The map's lamp post (`haven.cfg` LampPost1, 3711,2592) is diagonal to the stop, not on it.
- The stop's text ("this cottage is a small house") still fits. `HousingStop(0)` in `NewHavenLessons.cs` changed.
- Shown in `render-housing-stop1.jpg` (old stop red, new green, door cyan) and `housing-stop1-player.jpg` (the Tester
  on the new stop, the signpost beside him at the cottage's corner).

## What changed

- `server/customizations/Tutorial/NewHavenLessons.cs` (code copy):
  - `HavenPieces`: the mountain-path sign is now 3702,2742 and the stables sign 3608,2614, with a remark saying why;
  - `HousingStop(0)` is now 3712,2593.
- `server/tests/Tutorial/NewHavenFixesVerification.cs`:
  - `TheHousingLessonHasThreeClearStopsWithSigns` now asks for the guide's "within 2, never on it" (it allowed 4,
    which let the 4-tile gap through);
  - new fact `TheMountainAndStableSignsStandOffTheRoad` pins the two reviewed spots and keeps every signpost off the
    barn door's approach line.
- `CHANGELOG.md` and `VERSION`: the merge resolution above. The player-facing lines of P743 still describe the change
  ("A signpost marks where the path starts"), so no new line.

## Tests

- **Gated build:** `docker/uo/build.sh -t sl-modernuo:cc-P755` on the merged tree, run through
  `notes\cc-P755-tools\gated-build.ps1` with the `docker-build` lock taken and released.
  - Result: **EXIT=0, 2,884 tests: 2,878 passed, 6 skipped, 0 failed**. Image `sl-modernuo:cc-P755` built.
  - Files: `green\gated-build-summary.txt`, and the 18 `NewHavenFixesVerification` lines (P743's 17 facts plus the new
    one) in `green\gated-build-newhaven-facts.txt`. The full log is `gated-build-utf8.txt`.
- These are the tests P743 ran (its gated build). P743's red mutants were not re-run, because none of the code they
  aim at changed.

## Live walk and shots

- **Private shard:** 127.0.0.1:2596, a fresh copy of the bot world, image `sl-modernuo:cc-P755`. The `test-shard` lock
  was taken and released. Runner: `notes\cc-P755-tools\run-shots755.ps1` with the spec `shots755.json`
  (`make_shots755.py`). This is P743's runner (P753's TazUO shot runner, windows off-screen). The log is
  `run-shots755.log`, and the runner's own log is `notes\cc-P755-review\proof-log.txt`.
- The first try refused to start at 2.7 GB free. That was the Docker VM's page cache after the build. I dropped the
  cache (privileged alpine `drop_caches`) to 6.4 GB and the second try ran.
- The admin's `[ClusterFSeedTutorial` reply on that shard: "New Haven (cc-P743): placed 0 pieces (took away 0 from old
  spots)". The world load had already seeded the pieces at the new spots; the shots show them there.
- The three shots, each with the Tester moved by the Admin's commands (not a fresh character, as in P743):

| Shot | What it shows |
|---|---|
| `mountain-path-sign-player.jpg` | The Tester on the dirt road at 3703,2746. The post is on the grass at the forest edge north of him, and the road is clear. |
| `stables-sign-player.jpg` | The Tester in the lane at 3611,2616. The post stands under the barn's eave by the hitching post, north of the door, and the lane is clear. |
| `housing-stop1-player.jpg` | The Tester at 3712,2594, one tile south of the new stop 1 (3712,2593). The signpost is at the cottage's south-east corner beside him. |

- **Renders:** `render-mountain-sign.jpg`, `render-stable-sign.jpg`, `render-stable-sign-roofs.jpg` and
  `render-housing-stop1.jpg`, all made by `notes\cc-P755-tools\render755.py` (P708's hallbase client-view renderer on
  the SoS land, the same kind P743 used). Old spots are ringed red and new ones green.
- **`notes\cc-P755-review\placed.md`:** every placed piece, with item ID, location and facing. It is P743's list with
  the three changed lines, and it points at P743's renders for the pieces that did not move.

## Not done

- Unchanged pieces (Rook's bench, the stall props, housing stop 2's sign, the old farm's removal) were not re-shot.
  P754 passed them, and P743's shots in `notes\cc-P743-review\` still show them.
- No lesson was run live, for the same reason as in P743: the shot runner's Admin cannot answer a target, so it
  cannot start a lesson for the Tester.

## Files

- Code copy: `server/customizations/Tutorial/NewHavenLessons.cs`, `server/tests/Tutorial/NewHavenFixesVerification.cs`,
  `CHANGELOG.md`, `VERSION`, plus all of P743 through the merge.
- Docs copy:
  - this file;
  - `notes/cc-P755-review/`: `placed.md`, `proof-log.txt`, 4 renders and 3 shots;
  - `notes/cc-P755-tools/`: `ascii755.py`, `render755.py`, `make_shots755.py`, `shots755.json`, `run-shots755.ps1`,
    `run-shots755.log`, `gated-build.ps1`, `gated-build-utf8.txt`, `green/`;
  - plus all of P743's docs through the merge.

P755 DONE
