# P552: player guide for Clean Up Britannia changes

October 24, 2026. Documentation only. Read AGENTS.md in both supplied work copies, the direction decision, tasks, and the migration repo's remaining working agreements. No code, docs/ content, services, or client package files changed.

## Deliverables

- [Player guide draft](wiki-drafts/clean-up-britannia-changes.md): old-bundle redemption, point-based Civic Contracts, both corpse menu actions, ownership, ranges, loot protections, confirmation, cooldown, rewards, and player package requirements.
- This file is the lane notes destination requested in the outer prompt.
- [Companion notes](cc-P552-guide-clean-up.md) preserves the shorter notes destination requested in the embedded task. Both notes refer to the same completed work.

The guide uses plain American English and no em dashes. It is a local draft, not a wiki publication. No Pages skill was needed because the task explicitly requests Markdown files in an established repository destination.

## Source evidence

Code paths below are relative to the ShatteredLegacy work copy. These are inspected implementations, not live gameplay observations.

| Player-facing statement | Evidence |
|---|---|
| Bundles are retired but their saved item type remains | `server/customizations/CleanedDebris.cs:7`, `:18`; no production call remains in current cleanup or bag dump paths. |
| Redeem stacks at the Warden, no membership gate, 10 points per bundle, deleted once | `server/customizations/SanitationWarden.cs:73`; `server/customizations/ClusterFCustodianSystem.cs:619`, `:625`. The guard rejects deleted stacks; there is no per-character redemption cap. |
| Newly accepted contracts count later lifetime earnings; spending cannot reduce progress | `server/customizations/ClusterFWorkOrderSystem.cs:507`, `:523`. |
| Contracts from before P414 start at the first progress lookup | `server/customizations/ClusterFWorkOrderSystem.cs:523`; `server/customizations/GuildContractLedgerGump.cs:313`. The guide tells returning players to open the ledger before cleaning. |
| Contract tiers require 50 / 150 / 400 / 800 / 2,000 points; first pays 100 gold | `server/customizations/ClusterFWorkOrderSystem.cs:2670`, `:2687`, `:2704`, `:2721`, `:2738`. |
| Turn-in keeps spendable points and removes overlap with other contracts | `server/customizations/ClusterFWorkOrderSystem.cs:535`; `server/customizations/GuildContractLedgerGump.cs:592`. |
| Corpse menus belong to the owner with the bag in their backpack; no membership check on their use | `server/customizations/TrashBag.cs:105`, `:153`, `:155`, `:177`, `:198`. Single target range is 12 tiles. |
| Nearby action reaches 10 tiles, filters only corpses, shares a 60-second cooldown with cleanupall | `server/customizations/ClusterFCustodianSystem.cs:47`, `:348`, `:406`, `:432`, `:475`. Empty searches and canceled warnings return before setting the cooldown. |
| Players' corpses are refused; others' loot rights and instanced loot are protected | `server/customizations/ClusterFCustodianSystem.cs:121`, `:161`, `:172`. Pinned ModernUO `Projects/UOContent/Items/Misc/Corpses/Corpse.cs:92`, `:94`, `:321`, `:465`, `:750` supplies the underlying rules. The guide avoids promising a single expiry time. |
| Remaining contents cause confirmation and are permanently deleted with the corpse | `server/customizations/ClusterFCustodianSystem.cs:193`, `:365`, `:432`, `:471`, `:513`. Loose-item exclusions are not descendant protection inside a corpse. |
| Payout uses remaining contents and the earned creature bonus, not a guaranteed flat award | `server/customizations/ClusterFCustodianSystem.cs:210`, `:218`; `server/customizations/Services/CleanUpBritannia/ClusterFCorpseValue.cs:74`, `:83`. |
| Joining issues a bag; replacements remain member-only and delete old bags | `server/customizations/SanitationWarden.cs:103`; `server/customizations/SanitationWardenGump.cs:246`; `server/customizations/TrashBag.cs:85`. Menu use without membership is not a new nonmember acquisition route. |
| New menu text requires the matching player package | `server/customizations/ShardClilocs.cs:65`, `:68`; `player-package/vendor/shattered-legacy-cliloc/entries.json:15`, `:16`. P415 records blank, unusable rows with the old package. |

Read the P414 and P415 implementation notes and the existing `CivicContractPointsVerification.cs` and `TrashBagCorpseClaimVerification.cs` fixture descriptions alongside the current implementations. Historical P432 and P530 notes describe snapshots before these changes; current source includes both P414 and P415 and governs this draft. No older guide or report was edited.

## Verification and limits

No lane tests are required. No tests or gates were added, and no build or runtime tests were run for this prose-only task. Shell work used Windows PowerShell 5.1. Ripgrep was unavailable, so searches used tracked-file lists and PowerShell Select-String.

Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE set to the supplied work copies. It completed successfully. As in P530, its unconditional progress.json write was suppressed in memory; the file stayed byte-identical. No global counts or coverage percentages were used as evidence of player behavior.

Live deployment, installed player packages, menu rendering, saved bundles and contracts, NPC placement, and in-game interactions remain unverified. No Haven connection, deploy, account action, commit, merge, push, or branch switch occurred.

Final checks passed: the guide and both notes are ASCII with no em dashes or trailing whitespace; relative links and cited source paths/line bounds resolve; every deliverable is below 5 MB. Git whitespace checks passed in both repositories. The code work copy is clean, and the migration work copy contains only the three requested Markdown deliverables. Windows PowerShell version 5.1 was confirmed. No stop request was present at completion. No P552 work remains.

P552 DONE
