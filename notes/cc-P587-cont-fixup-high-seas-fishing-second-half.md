# CC task P587: fix-up for P269 (High Seas fishing, the second half, did not merge)

## In plain words

- The second half of High Seas fishing (P269: bait, magic hooks, lava fishing, the Oracle of the Sea, fish pies, the
  fish mongers' delivery orders) is now on a branch that merges cleanly into main.
- The merge failed only because P269 and the Hammer of Hephaestus work (P168) each added lines at the same spot in
  the build's patch list. Both sets are kept; nothing in the game changes beyond what P269 already did.
- The server image builds and all 2,380 tests run: 2,376 passed, 4 skipped (the usual four), none failed.
- For you: the same as P269. Once it is merged and the test shard is rebuilt, run `[GenFishMongers` once, or
  nobody sees the fish mongers.

## Headlines

- Both work copies are on `golem/Iron/P587`, which starts at current main (code `6b74371`, docs `cf1e97b`). P269's
  one commit in each repo (code `19fd417`, docs `49e4beb`) is applied on top with `git cherry-pick --no-commit`, and
  the result is staged, not committed. The Golem commits.
- One conflict, `docker/uo/apply-patches.sh`, resolved by keeping both sides. Everything else merged by itself.
- `docker/uo/build.sh -t sl-modernuo:cc-P587`: **2,380 tests, 2,376 passed, 4 skipped, 0 failed; no compiler
  warnings; image built** (`sha256:0f6775eafba0`). All nine P269 facts (`HighSeasFishingSecondHalfVerification`)
  passed, and all five patches in question applied. 11.4 GB free before the build; the docker-build lock was taken
  at 03:08 and released after.

## The conflicts

- **`docker/uo/apply-patches.sh`:** main (P168, via its fix-up P372) added `BOD-properties-guild-pay.patch` and
  `PlayerMobile-craft-order-hurt.patch` at the end of the patch list; P269 added `FishingPole-high-seas-bait-hooks.patch`,
  `Fishing-high-seas-bait-hooks-lava.patch` and `AOS-fish-pies.patch` at the same place. Each says "made against the
  tree every patch above leaves, so it goes last". The two sets touch different files (SmallBOD.cs, LargeBOD.cs,
  PlayerMobile.cs against FishingPole.cs, Fishing.cs, AOS.cs), so order between them does not matter. I kept P168's
  block first and P269's after, with both comments. The build applied all five.
- **`CHANGELOG.md`:** merged by itself. P269's `## 2026.10.25` section sits above main's `## 2026.10.24.18`.
- **`VERSION`:** merged by itself to P269's `2026.10.25`, the higher of the two (main has `2026.10.24.18`).
- **Docs repo:** README.md, dashboard.html and tools/progress.json merged by themselves. The three JSON files P269
  touched (tools/progress.json, tools/expansion-coverage.json, testing/playtest-steps.json) still parse. README.md,
  dashboard.html and tools/progress.json end up equal to main's: they are generated counters (file and test counts,
  the generation time), and main's copies are newer. I did not regenerate them, so their counts leave out P269's files until the next run of
  the progress generator.

## How

The hand-off says not to merge or switch branches, so I did not check out `golem/Iron/P269` and merge main into it.
Cherry-picking P269's single commit onto the P587 branch (which starts at main) without committing gives the same
tree as that merge would. Same approach as P542.

P587 DONE
