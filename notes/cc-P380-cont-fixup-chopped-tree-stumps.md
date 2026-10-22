# cc-P380: fix-up for P359 (chopped tree stumps): merge main and settle the conflicts

**Golem:** Iron. **Date:** 2026-10-22. **Branch:** `golem/Iron/P380` in both work copies. **Image:**
`sl-modernuo:cc-P380`.

## In plain words

- The chopped-tree stumps from P359 can now be merged. When you chop the last wood from a grove, a stump appears
  at the tree you chopped and disappears when the wood grows back. It was blocked only because two files had also
  changed on main.
- Both sides were kept. The shard builds, and all 2155 shard tests pass, including P359's 14 stump tests. They had
  never run before, because the Codex lane cannot build.
- One known flaw remains, flagged by Codex and confirmed here: on a normal map tree the stump will likely sit about
  one tree-height above the ground, not at its foot. It is not fixed in this fix-up (see below).
- For you: decide whether to queue a small task for the stump height before the stumps go live. P359's notes also
  ask you to choose a client option (a, b or c); their recommendation is (a), the server stump as built.

## What conflicted and how I settled it

ShatteredLegacy: `origin/golem/Valorite/P359` (`43c4cc3`) merged into `origin/main` (`b240bb4`). My branch was
already at `b240bb4`, so the `git merge origin/main` step was a no-op. Three files conflicted:

| File | Resolution |
|---|---|
| `docker/uo/apply-patches.sh` | Main's P371 block (PlayerMobile, SpellHelper and BaseBoat `-tutorial-island-gate.patch`) first, then P359's block (`HarvestBank-lumber-stumps.patch`), each with its own comment. No `apply_patch` line is listed twice (checked with `sort \| uniq -d`). The build's patch gate applied all four, and its check that every patch is accounted for passed. |
| `CHANGELOG.md` | P359 had its own `## 2026.10.21.21` heading, but main already has a different .21. I dropped P359's heading and moved its two lines under main's newest heading, **2026.10.21.24**: the stump line at the end of `### Added`, the settings line at the end of `### Staff`. Main's sections are otherwise unchanged. |
| `VERSION` | The higher one: 2026.10.21.24 (main), over P359's .21. That is main's value, so VERSION shows no change against main. |

shard-migration: `origin/golem/Valorite/P359` (`5a0f128`) merged cleanly. It adds
`notes/cc-P359-chopped-tree-stumps.md` and `notes/cc-P359-chopped-tree-stumps-codex-review.md`.

Both merges are staged and not committed (`--no-commit` in shard-migration; ShatteredLegacy is stopped at the
resolved conflict). The Golem's commit records each as a merge.

## Build

`docker/uo/build.sh -t sl-modernuo:cc-P380`, run under the docker-build lock (the lock is now released). Before the
build, 6.3 GB was free on Windows and the Docker VM had 12.7 GB free. Result:
`Built sl-modernuo:cc-P380 with patches applied and 2155 shard test(s) passing.` Exit 0, with no failed test.
Nothing was red, so nothing needed fixing.

P359's notes say its xUnit tests "could not be compiled or observed red/green in the real shard host". This build is
their first real run. All 14 cases of `ChoppedTreeStumpsVerification` pass.

`git diff --cached --check` reports trailing whitespace only in `server/patches/HarvestBank-lumber-stumps.patch`.
These are the patch's own blank context lines (`+ `), which a unified diff needs. They are not a defect.

## Open: the stump height on map trees (Codex's P2, confirmed, not fixed here)

Codex's review of P359 says that a stump on a tree from the map (not a placed `Static`) will sit too high. I
checked the pinned source and the finding holds. `D:\UO\ModernUO-pinned\Projects\Server\Targeting\StaticTarget.cs`
adds `TileData.ItemTable[ItemID].CalcHeight` to the target's Z in both constructors.
`ClusterFLumberStumps.cs:23` passes the `loc` from `GetHarvestDetails` straight to `Mark`, so the stump lands at
the tree's base Z plus the tree's height. I have not seen it in game.

The tests cannot catch it as written. They chop a dynamic `Static`, and in the test host `StaticTarget` masks every
item ID to row 0 (`TestHostTileData.cs`), whose height is 0.

I left it unfixed because this fix-up's brief is to merge and get the build green. It is already on the overseer's
Codex-flag list. A fix-up task would:

1. When `harvested` is a `StaticTarget`, subtract `TileData.ItemTable[st.ItemID].CalcHeight` from `loc.Z` before
   calling `Mark`.
2. Add a fact that opens a `TestTileRows.Seed` scope for the tree's real row, read from tiledata.mul as
   `TestTileRows.cs` asks. It would chop through a `StaticTarget` and assert the stump's Z is the tree's base Z.

P380 DONE
