# P435: Review of smith orders batch 2 (P46)

Reviewed 2026-10-22. Notes only. Code HEAD: `7508639ae5e728bcd35cd6fee923e06036bea307`.

Read both work copies' AGENTS.md, the direction decision, task list, and `notes/cc-P46-smith-orders-2.md`. No separate P46 Codex review was found beside that note. Reviewed P46's code changes in commit `1f2b899` against the current canonical files and their tests, including the post-Valorite combine patches, teaching setting and serialization, commission rewards, catalog, Self Repair floor, familiarity hook, test host, and Despise changes.

Also checked the later P61, P170 and P263 work and the related P379, P402 and P423 reviews. Their findings, P46's disclosed economy concerns, and subsequently fixed behavior are excluded below. Paths and line numbers refer to the current code work copy unless marked pinned; pinned source is `D:/UO/ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88`.

## Findings

1. **bug | `server/customizations/ClusterFSmithCommissions.cs:202`, `:728`.** With teaching off, the small commission picker can request dragon armor in the rolled metal, but the normal craft produces scale armor and `IsMatch` requires its resource to equal that metal, so the player cannot fulfill the order. Give scale items a supported resource requirement before picking and pricing the order, or exclude them from small commissions, and test generation followed by matching an actually crafted piece.

2. **risk | `server/customizations/ClusterFSmithCommissions.cs:585`, `:630`.** Large dragon commissions price rewards from the rolled ore even though `IgnoreMaterial` accepts the same scale pieces for every ore: an exceptional five-piece set calculates 3,000 standing under Iron and 27,000 under Celestial without requiring different materials. Price scale sets from their actual requirements, including their existing exotic-set bonus, or explicitly approve and document ore-based rewards for scale-only work, then test it with teaching off where these sets remain selectable at high skill.

3. **risk | `server/tests/Misc/SmithCommissionRewardsVerification.cs:111`.** The large commission test checks only that Seals are divisible by three and at least fifteen, so a large-only multiplier of six or a constant reward of fifteen would satisfy its Seal assertions despite violating P46's promised payout. Control the random roll and assert independent expected Seal amounts for ordinary and exotic sets, including the floor and post-Valorite tiers, with each new assertion seen failing first.

4. **risk | `server/tests/Misc/SmithCommissionRewardsVerification.cs:136`.** The payout test calls `Complete` directly with an arbitrary new Longsword, bypassing type, resource and quality matching, and the test tree contains no calls to `TurnInLargePiece` or `CompleteLarge`, leaving final-piece payment and stale-response handling uncovered. Add small and large commission tests through the book or guildmaster with matching crafted items, verify no payment before the final piece and exactly one payment afterward, and reject a stale second submission.

## Evidence and scope

- Findings 1 and 2 concern existing commission material rules that P46 retains and exposes through its off setting and reward changes; they are not claimed to have originated in P46. The dragon entries are shared by the small and large pools at `ClusterFSmithCommissions.cs:149` through `:153`, but only the large set has `IgnoreMaterial` at `:342`. `TeachingKey` checks makeability and teaching, without resource compatibility. Pinned `Projects/UOContent/Engines/Craft/DefBlacksmithy.cs:655` through `:668` registers the dragon pieces with RedScales and `UseSubRes2`; `:697` through `:704` offers scale resources only. Pinned `Items/Armor/BaseArmor.cs:545` assigns the crafted resource from that choice. The shard's additive blacksmith registrations do not replace these recipes.
- Finding 2's standing figures are arithmetic from the source, not observed payouts: exceptional piece standing is `80 + tier * 40`, multiplied by five pieces, the 1.5 set bonus, the 2.5 dragon bonus and P46's standing multiplier of two. Iron tier zero gives 3,000; Celestial tier sixteen gives 27,000. Seals likewise use the unused ore's gold-equivalent and multiplier. Whether this reward policy was intended is unverified; P46's note lists a Valorite dragon payout but does not resolve the unused-metal pricing rule.
- Finding 3 concerns assertion strength, not a demonstrated wrong multiplier in the current implementation. Finding 4 follows reading `SmithCommissionRewardsVerification.cs`, `SmithOrdersTeachVerification.cs`, `SmithTeachingToggleVerification.cs`, and searching the full `server/tests/` tree for the large completion methods. The tests generate orders and inspect selections or reward fields without completing a large commission through its player-facing path.

## Checks with no additional finding

- **Store-bought items:** nothing new found in the reviewed smith paths. P263's `SmallBOD-crafted-only.patch`, `LargeBODItemFill.cs:65`, and the small and large commission matchers reject uncrafted equipment when the default crafted-only setting is enabled. Hammer auto-fill is called after crafting. The separate CraftBOD bypass and crafted-only coverage gaps are already reported in P379 and P402 and are not repeated here.
- **Deed duplication:** no new player-accessible duplication or repeat-payment path found. Small deeds and items are deleted when combined; the current Society payout checks deletion and ownership in `ClusterFSmithBODPayout.cs:126` and `:130`, then deletes the paid deed. Commission gump handlers look up the active commission again, and large-piece matching rejects an already fulfilled key. Direct completion helpers trust their callers, so repeated direct helper calls are not proof of a client exploit; the missing commission transaction tests are finding 4.
- **OSI reward tables:** no additional unexplained table change found in P46 itself. Its commission multipliers and Seal catalog prices are explicitly requested custom Society rules; regular deed reward methods still delegate to the pinned calculator. Current OSI numeric tables were not independently verified, and P423's separate 2016 reward-table findings are excluded.
- **Other P46 changes:** no additional defect found in the post-Valorite material guards, teaching-setting persistence, Self Repair floor, null-resource familiarity fix, fixture configuration, or Despise attack-order and kill-award fixes. Later P61, P82 and P170 behavior was distinguished from the original P46 implementation.

## Validation and limits

This is a source review. Runtime reproduction, client appearance, packet replay, and live OSI behavior remain unverified. No builds or tests were run or added; the prompt specifies no lane tests. The shell is Windows PowerShell 5.1. No Haven connection, deployment, code edit, commit, merge, push or branch switch was made.

Ran `tools/progress.py --dry-run` with both work-copy path overrides; it exited 0. Its dry-run still rewrites `tools/progress.json`, so that generated file was restored byte for byte. Final status showed only the requested note pending; whitespace checks passed, and the note is ASCII and below 5 MB.

P435 DONE
