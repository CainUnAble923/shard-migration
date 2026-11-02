# Codex review: P763

CC task P763: continue P759 (loot boxes, more varied and more useful). Reviewed by Codex (`codex exec review`, read-only) after P763 DONE and before the Golem's commit, 2026-11-01 12:36.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The implementation substantially covers the approved plan, but recipe filtering, Society reward targeting, and reagent-bag capacity handling have functional gaps. I inspected the changes and recorded verification notes; I did not rerun the build or client tests.

- **medium** [P2] Choose the player's qualifying guild craft for Society rewards (`server\customizations\LootBoxes\ClusterFLootBoxes.cs:402`)
  For a Foresters' Union member promoted through Fletching, `SkillsOf("foresters")` lists Carpentry first, so this always rolls the Society box using Carpentry???even if that skill is zero. The player receives Carpentry tools/runic saws and resources scaled to their zero Carpentry instead of their qualifying Fletching. Select the strongest relevant guild craft, consistent with `ClusterFGuildPromotion.CraftSkill`, rather than the first table entry.
- **medium** [P2] Apply reagent weight reduction during capacity checks (`server\customizations\LootBoxes\LootBoxRewards.cs:108`)
  When a backpack is near its weight limit, this forwards the incoming reagents' full weight to stock `Container.CheckHold`, which also checks every parent container. For example, a backpack with 20 stones free rejects 100 stones of reagents even when the 90%-reduction bag would add only 10. Adjust the capacity calculation to use the actual reduced weight delta; reducing only the totals after insertion leaves legitimate drops rejected.
- **medium** [P2] Filter the Band V reward branch by the opener's craft (`server\customizations\LootBoxes\LootBoxRoller.cs:670`)
  When the opener has any qualifying craft, half of recipe rolls bypass the filtered recipe IDs and call `CreateFromTable("bandV", ...)`. That table defaults to `bandV:any`, and its implementation selects across all gated crafts without checking the player. A blacksmith with no Tailoring can therefore receive a Tailoring recipe, contrary to the approved recipe-filtering requirement. The new test checks only `RecipeScroll`, so it misses these `AccountRecipeScroll` rewards.

(2.1 minutes, 1,265,800 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.93). The notes document the approved plan, implementation and successful gated builds, but the new probe can silently report success after build or test failures. The server implementation itself is outside this repository's diff and could not be validated from these changes.

- **medium** [P2] Propagate build and test failures from the probe (`notes\cc-P763-tools\probe.sh:30`)
  When a build fails, the semicolon-separated commands still run `dotnet test --no-build`, potentially testing stale assemblies. When tests fail, the final `grep -v warning` normally succeeds, so Docker and this script return zero anyway. Check each build's status before continuing and preserve the test runner's exit status through filtering. This also undermines the failure-verification requirement in [AGENTS.md](../../AGENTS.md#L339-L343).

(1.1 minutes, 418,225 tokens)
