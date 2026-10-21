# CC task P285: fix-up for P261 (levelable crafted gear, phase 1): its branch did not merge into main

Copper, 2026-10-21. Paused at Chase's request after the build step, with both repos building and green.

## Headlines

- P261 now merges with main. The three conflicts in ShatteredLegacy are resolved: `CHANGELOG.md`, `VERSION` and
  `docker/uo/apply-patches.sh`. Both sides are kept where they do not contradict.
- shard-migration merged on its own, with no conflicts (P261's notes file).
- Green: `docker/uo/build.sh -t sl-modernuo:cc-P285` built the image with every patch applied. 1,924 tests: 1,920
  passed, 0 failed, 4 skipped. All 7 `LevelGearVerification` facts pass, and so do P238's climbing boots facts.
- Not committed. The merge is staged in both work copies (`MERGE_HEAD` set) for the Golem to commit.

## How it was merged

The hand-off put both work copies on `golem/Copper/P285` and said not to switch branches. `golem/Copper/P285` was exactly
main: `2ab20d7` in ShatteredLegacy, `125bcac` in shard-migration. So, as P272 and P278 did, I ran
`git merge --no-commit --no-ff golem/Copper/P261` on P285. The tree comes out the same as merging main into P261, with
P261 and main as its parents.

## Conflicts resolved (ShatteredLegacy)

| File | Main's side | P261's side | Resolution |
|---|---|---|---|
| `VERSION` | `2026.10.21.7` | `2026.10.21.6` | The higher one: `2026.10.21.7` (so VERSION has no change against main) |
| `CHANGELOG.md` | new sections `2026.10.21.7` (Staff: the Codex lanes on the second PC, P159) and `2026.10.21.6` (P237's community art) | its own `2026.10.21.6` (one Staff line: levelable gear) | P261's Staff line moves under `## 2026.10.21.7` / `### Staff`, after P159's. Its own heading is dropped, so main's `2026.10.21.6` stays P237's alone |
| `docker/uo/apply-patches.sh` | P238's block (`PlayerMobile-climbed-tile-rules.patch`, `HousePlacement-climbed-tile.patch`) | P261's block (`AOS-level-gear-attribute-aggregation.patch`) | Both blocks, P238's first, each with its own comment |

The two blocks of patches touch different files: P238 patches `PlayerMobile.cs` and `HousePlacement.cs`, P261 patches
`Misc/AOS.cs`. All three are `Applied` in the build log. `server/customizations/Mobiles/PlayerMobileSetResistances.cs`
(P261's resist term) merged without a conflict.

## Tests

| What | Result |
|---|---|
| `docker/uo/build.sh -t sl-modernuo:cc-P285` (took and released the `docker-build` lock) | "Built sl-modernuo:cc-P285 with patches applied and 1920 shard test(s) passing." Total 1,924, passed 1,920, skipped 4, failed 0 |

## Merge note for the integrator

P262 (accessory slots, `golem/Copper/P262`) also patches `AosAttributes.GetValue` and also appends a block to
`apply-patches.sh`. Its hunk is after the loop, and P261's is at the loop's start, so the two patches' contexts do not
overlap. When both are in main, keep both `apply-patches.sh` blocks.

## Continuation

- **Done:** everything this prompt asks for. The merge is resolved and staged, the build is green, and these notes are
  written.
- **Left:** nothing in the code. The Golem commits the staged merge, and the integrator merges P285 into main again.
- **Mid-flight:** nothing. No file is half-edited, and no lock is held.
- **Continuation prompt:** `D:\UO\cc-prompts\queue\cc-P287-cont-fixup-levelable-gear-merge-check.md`. It only checks that
  P285 reached main, and redoes the merge if main moved and it did not.

P285 PAUSED
