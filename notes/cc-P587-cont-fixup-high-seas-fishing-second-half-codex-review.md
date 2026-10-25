# Codex review: P587

CC task P587: fix-up for P269 (CC task P269: High Seas fishing, the second half (baits, hooks, the O. Reviewed by Codex (`codex exec review`, read-only) after P587 DONE and before the Golem's commit, 2026-10-25 03:12.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The conflict resolution preserves both patch blocks, and the task notes report a successful gated build. However, the imported implementation introduces exploitable shipping-order and hook-consumption paths. I did not independently rerun the build or client tests.

- **high** [P1] Revalidate the hook before applying it through a pending target (`server\customizations\Services\Expansions\High Seas\Items\Fish\Hooks.cs:89`)
  The target callback never checks whether `_hook` still exists or belongs to the player. A player can open its target cursor, transfer the hook to another player who applies it, then use the original cursor to apply that already-deleted hook to another pole. Its saved type and uses are still readable, so one hook supplies multiple poles; swapping those hooks subsequently creates additional hook items. Check deletion and backpack ownership again before changing the pole.
- **high** [P1] Prevent carving fish already credited to a shipping order (`server\customizations\Services\Expansions\High Seas\Quests\ProfessionFishQuest\ShippingCrate.cs:287`)
  Fish inside the new crate can still be targeted with a blade: `BaseHighseasFish.Carve` unconditionally calls `ScissorHelper`, consuming the fish and replacing them with steaks. `CheckLift` does not intercept carving, and `_orderHave` remains unchanged. Consequently, players can recover the fish as steaks and still collect the order's reward, since `DeleteQuestItems` ignores whether `ConsumeTotal` succeeds. Restore the shipping-crate carving restriction or verify actual contents before paying.

(2.1 minutes, 1,520,891 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.87). No actionable defects found in this docs-repository diff. The fix-up notes describe the conflict resolution and test results, and both changed JSON files parse successfully. The companion server implementation and reported build results were not independently verified.

No findings.

(0.6 minutes, 174,703 tokens)
