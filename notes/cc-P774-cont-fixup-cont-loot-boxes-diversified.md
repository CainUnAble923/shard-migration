# cc-P774: fix-up for P763 (loot boxes, more varied and more useful): its build review said FAIL

Iron Golem, 2026-11-02. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P774`, not committed. Tools and logs are in `notes\cc-P774-tools\`. The review folder is
`notes\cc-P774-review\`.

## In plain words

- **P763's loot box update is ready for its second review.** Its first review failed for one reason only: it left no
  "what was placed in the world" list.
- **I added that list.** It says P763 places nothing in the world. The review was triggered because a patch file has
  "Decorative" in its name, but that patch is about setting a plant to "decorative", not about decorating the map.
- **P763's work is now joined with today's main**, and the full server build and its tests ran on the result:
  2,950 tests passed, 0 failed.
- **Nothing for you to do.** The integrator queues the second review and merges after a PASS.

## 1. The branch

The prompt says to check out `golem/Iron/P763` and merge main into it. The hand-off says not to switch branches. So,
as P746 did, I merged `golem/Iron/P763` into this branch (`golem/Iron/P774`, which is main at `33c5257` in the code copy
and `3ff02f0` in the docs copy). I used `git merge --no-commit --no-ff`. The tree is the same either way. MERGE_HEAD is
P763's tip in both copies: `144faea` in the code copy and `008bf6f` in the docs copy. The Golem's commit makes the merge
commit.

- **Docs copy:** merged by git with no conflict.
- **Code copy:** two conflicts, both in the version files.
  - `CHANGELOG.md` conflicted because both sides added sections at the top. Main's sections (2026.11.01.5 to
    2026.11.02.2) stay as they are. P763's section, written as 2026.11.01.4 (a version main has used since), is now the
    newest one: **2026.11.02.4**. I skipped .3 because P715's branch, committed but not yet merged, uses 2026.11.02.3.
    The text of every section is unchanged. Script: `notes\cc-P774-tools\resolve_changelog.py`.
  - `VERSION` is `2026.11.02.4`.
- **Files both sides changed** since P763 branched (merge base `55472a5`): only `CHANGELOG.md`, `VERSION` and
  `docker/uo/apply-patches.sh`.
  - `apply-patches.sh` merged by git. P763's two `apply_patch` lines sit after main's newest one
    (`MLQuestEntry-quest-milestones.patch`).
  - The gated build below applies every patch and checks that every patch file is named.
  - No loot box, guild or season file that P763 touches was changed on main.

## 2. The reviewer's items (P768, Gold Golem)

1. **"No renders or placed list left for review: `notes/cc-P763-review/` and its `placed.md` are missing."**
   - **Done:** `notes\cc-P774-review\placed.md`, as the reviewer asked:
     - P763 places no pieces in the world;
     - an empty placed table (item ID, location, facing);
     - why the classifier picked it up: `SetToDecorativeGump-loot-box-herbalist.patch` is a plant-status hook that
       awards a Herbalist loot box, not map decoration.
   - **Checked on the merged tree**, not taken from the review (`notes\cc-P774-tools\placement-search.txt`):
     - the 22 files that differ from main are all loot box code, its tests, one migration, two patches, three
       guild/season files that award boxes, `apply-patches.sh`, `CHANGELOG.md` and `VERSION`;
     - the added lines' only `MoveToWorld` or `Point3D` is a test fixture moving a test mobile (`Pm.MoveToWorld(new
       Point3D(1400, 1400, 0), Map.Trammel)`).
   - **No renders, shots or isorender** (prompt part 3). Nothing is built or placed, so there is nothing to walk past or
     render. The reviewer said the same ("No renders are needed because nothing is built"). P763's in-game shots of
     opened boxes are still in `notes\cc-P763-shots\` for anyone who wants to see the boxes.

The reviewer also notes that the integrator's classifier treats "Decorative" in a patch name as decoration work. That
is a false positive. I did not change the classifier (it is in the Golem kit, outside this prompt's server area). I list
it for the overseer under Deviations.

## 3. Tests and the gated build

P763 ran its new facts and the full suite through the gated build. The merge changes what is under `server\` and
`docker\uo\` relative to both main and P763, so I ran the gated build again on the merged tree:
- **How:** `docker\uo\build.sh -t sl-modernuo:cc-P774`, via `notes\cc-P774-tools\gated-build.ps1` (P763's script with
  the new tag), detached.
- **Before it:** the `docker-build` lock was taken and the Docker VM's page cache was dropped (13.6 GB free in the VM
  after the drop).

**Result: EXIT=0** (`notes\cc-P774-tools\green-gated-build.txt`).
- **Tests:** 2,956 in all; 2,950 passed, 6 skipped, 0 failed.
  - P763's own run had 2,896 tests. The extra 60 are main's tests added since P763 branched.
  - P763's nine `LootBoxDiversityVerification` facts ran in this build.
- **Patches:** all 186 applied, P763's two among them. Every patch file is accounted for.
- **Image:** `sl-modernuo:cc-P774`. The `docker-build` lock was released after.
- **A low-memory reap along the way:** Claude Code stopped my background wait on the log during the run. The build
  itself was detached and finished on its own; I read the result from the log on disk.

## Deviations and decisions for Chase

- **Merged P763 into this branch, not main into P763** (the hand-off forbids switching branches). The tree is the same.
- **P763's CHANGELOG section moved from 2026.11.01.4 to 2026.11.02.4**, the newest. Main had already shipped versions
  past .01.4, so the old number would have sat in the middle of the history.
- **No walk, shots or isorender** for part 3: nothing is placed. The placed list says so.
- **For the overseer:** the integrator's build-review classifier matched "Decorative" in a patch name (a plant gump
  patch). That sent a loot box prompt to a build review and cost one review and this fix-up. Worth a narrower match in
  the kit.

P774 DONE
