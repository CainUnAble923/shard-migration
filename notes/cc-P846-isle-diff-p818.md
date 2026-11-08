# cc-P846: the isle release diff for P818 + P837 (the League lodge door) on top of update 13

## In plain words

- **The lodge-door fix is ready for the isle release.** The isle's League lodge door now sits in the wall you can see from the road, with a brick walk and two fires leading to it. It now fits on top of isle update 13, and the bank changes from update 13 are kept.
- **What players will see:** coming along the road from the bank, the walk, both fires and the door are in view, and the two lodge signposts stand where the walk meets the road (shots in `notes\cc-P846-shots\`).
- **For you:** the overseer applies `notes\cc-P846-tools\p846-release-isle-20261028.diff` to `release/isle-20261028`, then writes CHANGELOG and VERSION. Players need the next player package to see the new door and walk, because they are map changes.

Iron Golem, 2026-11-08. Release copy `D:\UO\golems\Iron\p846-isle` is a detached worktree at `8f6eb2e`, the `release/isle-20261028` tip after `git fetch`, version 2026.11.08.1. The change is staged there. Nothing was committed or pushed, `latest` did not move, and nothing was published.

## 1. Scratch copy

`git worktree add --detach D:\UO\golems\Iron\p846-isle 8f6eb2e` from the code copy, as P762 and P818 did.

## 2. P818 + P837 onto the tip

I applied P818's own release diff with `git apply --3way --index`. It already carried all of P818's isle work: the map patch, `TutorialWorld`, `TutorialCorePlacement`, `TutorialCoreTrials` and the facts. P837 added no isle code of its own. It merged P818 onto main and resolved the clashes with P817 and P823, and I made the same choices here. Every file except these applied cleanly:

- **`CHANGELOG.md`, `VERSION`:** left at the tip, as the prompt says (`git checkout HEAD --`).
- **`player-package/vendor/shattered-legacy-map/SOURCE.txt`:** I kept both entries in order: cc-P817 and cc-P823 (the release), then cc-P818.
- **`server/customizations/Tutorial/TutorialCorePlacement.cs`:** three hunks, resolved as P837 resolved them on main:
  - `SignPoint`: `core.banking` takes P817's 6757,3982 with its comment, and `core.league` takes P818's 6789,3984.
  - `SeedOn`'s upgrade passes: P817's `FaceCounter` and `MoveOldProps`, then P818's `RemoveOldLodgeDoor` and `MoveLodgeSign`.
  - The mobile table: Merrin facing his counter (P817) and Elara with `ElaraFacing` (P818).
  - Result: the file is **byte for byte main's** (same md5 as `main:` in the code copy). `TutorialWorld.cs` and `TutorialLodgeDoorVerification.cs` also equal main's.
  - `TutorialCoreTrials.cs` differs from main only in the release's three New Haven lines ("Bountiful Harvest Inn" against main's "Albatross tavern"). The lodge lines are P818's.
- **`trammel.mapops`:** git merged it by content. The change from the tip is exactly P818's 22 lines (5 dropped, 17 added). The sorted +/- lines are identical to P818's release diff, with no L or B line. P823's west-eave ceiling lines stay gone: there is no 0x049C at Z 20 on x 6758 or 6778.

The resolver is a short script in my scratchpad. Its rules are the bullets above.

## 3. Tests, build and shot

- **Free memory** before the build: 4.3 GB, then 6.5 GB after dropping the Docker VM's page cache.
- **Gated build:** `docker/uo/build.sh -t sl-modernuo:cc-p846-isle` under the docker-build lock, started detached by `notes/cc-P846-tools/gated-build-isle.ps1`. It came back **green: EXIT=0, 3,025 tests, 3,020 passed, 5 skipped, 0 failed.** That covers every isle fact, including P818's six `TutorialLodgeDoorVerification` facts and the changed `TutorialIsleWalkFixes2` and `TutorialIsleReviewFixes` facts, alongside P813/P817/P823's. The summary is in `notes/cc-P846-tools/green-gated-build-isle.txt` and the full log (UTF-16) in `gated-build-isle.log`. Lock released.
- **TazUO shots:** taken under the test-shard lock (released afterwards) on the **private proof shard only** (port 2596, container `sl-p846-proof`, image `cc-p846-isle`). The shard ran a copy of the overnight bot world with the release copy's map as overlay. The client was P823's package copy (`D:\UO\golems\Iron\p846-pkg`) with the release copy's `trammel.mapops` dropped in (same md5). No package was built or published.
  - The world was seeded before the change. On load it reported "1 doors" (`notes/cc-P846-tools/proof-shard-seed.txt`): the east door was hung and the old north door taken away.
  - `notes/cc-P846-shots/lodge-walk-mouth.jpg`, from where the player arrives on the road (6789,3988): the brick walk, a brazier on each side of the door in the east wall, and both signposts north of the road.
  - Also `lodge-road-west.jpg`, arriving from the bank, and `lodge-door-step.jpg`, at the door. No grey squares show on the lodge's west slope.
  - Tools: `notes/cc-P846-tools/` holds `overlay.ps1`, `proof-shard.ps1`, `shots823.ps1` with `stage817.py` and `Clear823.py`, `shots846.json` and `run-shots.ps1`.
- **Not run:** `tools/tests/test_mapops.py`. Its statics-placed check compares the driver's main-base records, and P837 ran it on main. The release map change is P818's 22 lines exactly, checked above.

## 4. The diff

- **The diff:** `notes/cc-P846-tools/p846-release-isle-20261028.diff` is `git diff --cached --binary 8f6eb2e` of the release copy. It changes 8 files: +524 / -35 lines.
- **`git apply --check`** on a fresh detached worktree at `8f6eb2e`: **EXIT 0**.
- Applied there with `--index`, its `git write-tree` (`df9006dc`) equals the staged release copy's tree, so the diff is exactly what was built and shot.

## For the build reviewer

`notes/cc-P846-review/`: `placed.md` (P818's piece list, unchanged, with what this task checked) and the three TazUO shots.

## Deviations

- **Overlay builder:** the release copy's `Build-MapOverlay.ps1` has no `-Stock` switch, so the proof overlay was built by the code copy's builder from the release copy's `trammel.mapops`. This only affects the proof shard. Nothing in the diff changed because of it.

P846 DONE
