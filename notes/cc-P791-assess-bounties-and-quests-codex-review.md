# Codex review: P791

CC task P791: assess bounties, goals and quest chains. Reviewed by Codex (`codex exec review`, read-only) after P791 DONE and before the Golem's commit, 2026-11-03 11:14.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The note covers the requested packages, rules check, and ranked recommendations, but its primary recommendation misstates existing gold sinks and its terms assessment overlooks explicit source conditions. No files were changed during review.

- **medium** [P2] Include the goal stone's explicit source-header terms (`notes\cc-P791-assess-bounties-and-quests.md:29`)
  Both `GoalStone.cs` and `GoalGump.cs` explicitly permit use but require retaining their first two credit lines, including credit to Visam and PyrO. Reporting all five packages as having no stated terms misses that condition and substitutes a generic credit-the-author summary. Since terms assessment is an explicit deliverable, record the source-header permission and retention requirement separately from the intake policy; clarify that an independent idea-only rebuild does not copy those files.
- **medium** [P2] Distinguish a new community fund from existing gold sinks (`notes\cc-P791-assess-bounties-and-quests.md:38`)
  The rank-one recommendation rests partly on the claim that the shard has no gold sink, but existing customizations already consume gold: `GuildResources.TryPay` calls `CompactGoldHelper.ConsumeGold`, and `MinersCompactLiaisonGump` defines repeatable restoration costs of 100???60,000 gold. A shared community fundraising mechanism may be new, but gold removal is not. Correct the overlap assessment and recommendation rationale so Chase is not prioritizing work against a nonexistent economy gap. This also follows the source-verification requirement in [AGENTS.md:58???60](../AGENTS.md#L58-L60).

(1 minutes, 297,812 tokens)
