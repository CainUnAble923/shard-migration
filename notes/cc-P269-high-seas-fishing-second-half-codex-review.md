# Codex review: P269

CC task P269: High Seas fishing, the second half (baits, hooks, the Oracle of the Sea, lava fishing,. Reviewed by Codex (`codex exec review`, read-only) after P269 DONE and before the Golem's commit, 2026-10-25 01:17.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). Most requested systems and tests are present, but hook duplication, the missing crate-carving protection, and an incorrectly omitted Corgul artifact need correction. Build and runtime tests were not independently rerun during this read-only review.

- **high** [P1] Revalidate the hook before completing its target (`server\customizations\Services\Expansions\High Seas\Items\Fish\Hooks.cs:116`)
  A player can open the hook's target cursor, transfer the hook to another player who attaches it, and then finish the original cursor. This callback copies the deleted hook's unchanged uses onto another pole, duplicating its charges. Check that `_hook` is not deleted and is still in the acting player's backpack before modifying the pole.
- **medium** [P2] Port the Mysticism handbook using MysticSpellbook (`server\customizations\Services\Expansions\High Seas\Mobiles\Corgul\CorgulTheSoulbinder.cs:122`)
  The stated reason for omitting Corgul's third unique artifact is incorrect: pinned ModernUO provides `Projects/UOContent/Items/Skill Items/Magical/MysticSpellbook.cs`, including the Mystic book type, offset and spell count. ServUO's `CorgulsHandbookOnMysticism` can derive from that equivalent just as the undead handbook derives from `NecromancerSpellbook`. Omitting it removes requested loot and changes the other artifacts' odds. The applicable name-equivalence rule is [migration AGENTS.md:231???233](D:/UO/shard-migration/AGENTS.md#L231-L233).
- **medium** [P2] Prevent carving fish already counted toward an order (`server\customizations\Services\Expansions\High Seas\Quests\ProfessionFishQuest\ShippingCrate.cs:287`)
  The existing `BaseHighseasFish.Carve` still lacks ServUO's shipping-crate guard. Players can fill an order, carve its fish inside the crate, and collect the reward anyway: `Completed` trusts `_orderHave`, while this unchecked `ConsumeTotal` fails to consume the now-missing fish. Port the carving restriction and validate the actual contents before awarding payment. This also follows the fidelity requirement in [AGENTS.md:171???173](AGENTS.md#L171-L173).

(3.5 minutes, 2,374,278 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.9). The notes and play-test additions document substantial implementation and verification, but explicitly leave fish-pie crafting unavailable to players. This review covers the docs-repository changes, not an independent review of the companion server patch.

- **medium** [P2] Make the fish-pie ingredients obtainable before declaring completion (`notes\cc-P269-high-seas-fishing-second-half.md:253`)
  For ordinary players, the new recipes remain unusable because their required seasonings have no acquisition path. This leaves the requested fish-pie crafting portion unfinished despite the completion claim; the play test bypasses the problem with staff `[add` commands. Port the corresponding ServUO vendor stock and placement, or obtain an explicit scope deferral before marking this portion complete. This also conflicts with the repository's requirement to check that ported behavior is reachable ([AGENTS.md:322???324](../AGENTS.md#L322-L324)).

(0.8 minutes, 315,126 tokens)
