# CC task P278: fix-up for P238 (Climbing boots for the unreachable mountain ore, F-36): its branch did not merge into main

Copper, 2026-10-21.

## Headlines

- P238 now merges with main. The two conflicts in ShatteredLegacy are resolved: `CHANGELOG.md` and
  `docker/uo/apply-patches.sh`. Both sides are kept in both files. Both conflicts came from P231 (hidden joke
  achievements), which merged first and wrote into the same places.
- shard-migration merged on its own, with no conflicts (P238's notes and `notes/cc-P238-tools/unreachable_banks.py`).
- Green: `docker/uo/build.sh -t sl-modernuo:cc-P278` built the image with every patch applied. 1,912 tests: 1,908
  passed, 0 failed, 4 skipped. P238's 10 `ClimbingBootsVerification` facts and P231's `JokeAchievementsVerification`
  are both in that run.
- Not committed. The merge is staged in both work copies (`MERGE_HEAD` set) for the Golem to commit.

## How it was merged

The hand-off put both work copies on `golem/Copper/P278` and said not to switch branches. `golem/Copper/P278` was
exactly `main` (`90c0402` in ShatteredLegacy, `6463915` in shard-migration). So instead of checking out P238 and
merging main into it, I ran `git merge --no-commit --no-ff golem/Copper/P238` on P278, as P272 did. The tree comes out
the same, and P238 and main are both its parents.

Only `CHANGELOG.md`, `VERSION` and `docker/uo/apply-patches.sh` changed on both sides since the merge base (`b518c81`).
No C# file did, so P238's account data v22 bump has nothing to clash with.

## Conflicts resolved (ShatteredLegacy)

| File | Main's side (P231) | P238's side | Resolution |
|---|---|---|---|
| `VERSION` | `2026.10.21.5` | `2026.10.21.5` | No conflict: both are the same |
| `CHANGELOG.md` | under `## 2026.10.21.5`: one Added line (secret achievements), one Staff line | under the same heading: four Added lines (climbing boots), one Staff line | One `## 2026.10.21.5` section. Under Added, P231's line comes first, then P238's four. Under Staff, P231's line, then P238's |
| `docker/uo/apply-patches.sh` | the cc-P231 block: nine `*-achievement.patch` lines | the cc-P238 block: `PlayerMobile-climbed-tile-rules.patch`, `HousePlacement-climbed-tile.patch` | Both blocks, P231 first, then P238, each with its own comment |

The two blocks of patches touch different files. P231 patches Scissors, Begging, Food, Bandage, CraftItem,
HarvestSystem, Beverage, Fishing and BaseExplosionPotion. P238 patches PlayerMobile and HousePlacement. So the order
between them doesn't matter, and the build log shows all eleven as `Applied`.

## Tests

| What | Result |
|---|---|
| `docker/uo/build.sh -t sl-modernuo:cc-P278` (took and released the `docker-build` lock) | Image built: "Built sl-modernuo:cc-P278 with patches applied and 1908 shard test(s) passing". Total 1,912, passed 1,908, skipped 4, failed 0 |

That is P238's 1,901 tests plus P231's 11 new ones, all passing.

## Commit preflight

- No unmerged paths in either work copy. Both are on `golem/Copper/P278` with `MERGE_HEAD` = P238.
- `git diff --cached --check` flags only trailing whitespace in P238's two `.patch` files. Those are blank context
  lines that a unified diff needs, and both patches apply, so I left them alone.

P278 DONE
