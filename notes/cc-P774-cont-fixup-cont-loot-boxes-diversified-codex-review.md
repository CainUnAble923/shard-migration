# Codex review: P774

CC task P774: fix-up for P763 (CC task P763: continue P759 (loot boxes, more varied and more useful). Reviewed by Codex (`codex exec review`, read-only) after P774 DONE and before the Golem's commit, 2026-11-02 07:32.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The P774 notes and empty placed list reasonably address the decoration-review false positive, and record a passing gated build. However, the merged loot-box implementation still contains two functional reward/capacity bugs. I did not independently rerun the build.

- **medium** [P2] Select the recipient's relevant craft for multi-craft guild boxes (`server\customizations\LootBoxes\ClusterFLootBoxes.cs:402`)
  For a Foresters' Union member who advances through Fletching rather than Carpentry, `RecipeOwners.SkillsOf("foresters")` lists Carpentry first, so every Society box is rolled for Carpentry. This gives the fletcher a dovetail saw instead of FletcherTools, scales resources using their potentially zero Carpentry skill, and guarantees the wrong runic tool at Epic/Legendary rarity. Select the member's qualifying or strongest guild craft instead of always taking the first registered skill.
- **medium** [P2] Apply reagent weight reduction during capacity checks (`server\customizations\LootBoxes\LootBoxRewards.cs:108`)
  When the backpack is near its weight limit, adding reagents can be refused even though their reduced weight would fit. This delegates to pinned `Container.CheckHold`, which checks and propagates the incoming item's full weight; only `UpdateTotal` applies the reduction afterward. Account for the reduced weight during admission checks too, including the rounding difference against the bag's current contents.

(2.7 minutes, 1,173,248 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The fix-up supplies the missing placed list and records a successful gated build; omitting world renders is justified because nothing is placed. However, the added probe still masks build and test failures. Server implementation changes are outside this repository's review scope.

- **medium** [P2] Propagate build and test failures from the probe (`notes\cc-P763-tools\probe.sh:29`)
  When either build fails, the semicolon-separated commands still run tests with `--no-build`, potentially testing stale assemblies. When tests fail, the final `grep -v warning` normally succeeds, so Docker and the probe return zero. Stop after failed builds and preserve the test runner's exit status through output filtering. This also undermines the failure-verification requirement in [AGENTS.md](../../AGENTS.md#L339-L343).

(1.7 minutes, 300,409 tokens)
