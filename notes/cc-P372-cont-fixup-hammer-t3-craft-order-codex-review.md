# Codex review: P372

CC task P372: fix-up for P168 (CC task P168: Hammer of Hephaestus T3: crafts a whole bulk order for . Reviewed by Codex (`codex exec review`, read-only) after P372 DONE and before the Golem's commit, 2026-10-24 23:57.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The conflict resolutions preserve both sides, and the task notes report a successful gated build. However, the imported implementation retains a skill bonus after depletion and can display stale holder-dependent payouts. Tests were not rerun during this read-only review.

- **medium** [P2] Invalidate guild-pay tooltips when the deed changes holders (`server\customizations\Services\BulkOrders\BulkOrderGuildPay.cs:145`)
  The new tooltip depends on the holder's guild membership and payout setting, but ModernUO caches item property lists and changing an item's parent does not invalidate them. After a deed's tooltip is generated and the deed is traded, the recipient can therefore retain the previous holder's payout text, or no guild-pay text at all, until another operation invalidates the deed. Add invalidation for ownership changes, including transfers of containers holding deeds, so the displayed payout reflects the current holder.
- **medium** [P2] Remove the T3 skill bonus when its last use is consumed (`server\customizations\HammerOfHephaestus.cs:1064`)
  After crafting consumes the last use, `_exhausted` remains false and the equipped hammer's +15 Blacksmithy modifier remains active. `TriggerExhaustion` is only called by a subsequent double-click, so the player can leave the empty T3 equipped and continue receiving its bonus while crafting with an ordinary tool from their backpack. Handle depletion when uses reach zero and remove the modifier at that point.

(1.9 minutes, 1,286,562 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.89). The docs-repo changes restore P168's notes and add the requested P372 conflict-resolution and verification record. No actionable defects were found in these files; the server merge and reported test results cannot be independently verified from this diff.

No findings.

(0.3 minutes, 105,169 tokens)
