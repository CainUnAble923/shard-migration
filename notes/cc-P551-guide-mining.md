# P551: mining changes player guide sources and open questions

Written October 24, 2026. Docs-only task. Deliverable: [mining-changes.md](wiki-drafts/mining-changes.md). Run record: [cc-P551-guide-mining-changes.md](cc-P551-guide-mining-changes.md).

## Scope

Drafted a standalone player guide for the P416 stone mining gate, Compact book purchase, per-metal mining quotas, old contract compatibility, and gold covering missing vouchers during pickaxe restoration. Plain American English, no em dashes. No code, published wiki content, or files under docs/ changed.

The outer lane instruction names cc-P551-guide-mining-changes.md, while the embedded prompt requests this sources file. Both are supplied. No deployment or live availability is claimed by the draft.

## Primary source evidence

Paths beginning server/ refer to the ShatteredLegacy work copy. Pinned paths refer to the read-only D:/UO/ModernUO-pinned/Projects/UOContent tree. Line references describe the source read for this draft.

| Player-facing claim | Source |
|---|---|
| Reading from the backpack requires 100.0 base Mining, teaches the character, and consumes the book | Pinned Items/Skill Items/Specialized/StoneMiningBook.cs:18-39 |
| Stone Crafter offers the same book at a listed base price of 10,625 gold | Pinned Mobiles/Vendors/SBInfo/SBStoneCrafter.cs:31. This is a vendor-table price, not a verified live quote. |
| Garrett Ashveil is the Compact Liaison at the New Haven mine camp | server/customizations/MinersCompactLiaison.cs:10-26; constructor name and placement annotation |
| Compact book defaults: Journeyman at 5,000 standing, 50 vouchers; buying before GM is permitted | server/customizations/MinersCompactLiaisonGump.cs:114-118, :688-769, :894-901. Purchase checks membership, learned state, standing, and voucher balance. Reading skill is an informational line on the purchase page. |
| Learned status replaces the dashboard book offer | server/customizations/MinersCompactLiaisonGump.cs:328-336 |
| Unlearned characters cannot take new Stone Contracts or see discovery-locked stone cards | server/customizations/ClusterFWorkOrderSystem.cs:138, :185-203, :610-616; server/customizations/GuildContractLedgerGump.cs:141, :240 |
| Dispatch Ledger in the backpack opens the same contract list for members | server/customizations/CompactDispatchLedger.cs:40-60 |
| Granite requires learned stone mining, 100 base Mining, and the toggle; enabled mining can yield ore or stone | server/patches/Mining.cs:273-291; pinned Items/Skill Items/Harvest Tools/BaseHarvestTool.cs:134-159, :181-220 |
| Iron quota: 100 ore, no extra skill or standing gate, 75 standing / 4 vouchers / 60 gold | server/customizations/ClusterFWorkOrderSystem.cs:648-661 |
| Dull Copper quota: 50 ore, 5,000 standing, 65 Mining, reported DullCopper discovery, 350 standing / 16 vouchers / 400 gold | server/customizations/ClusterFWorkOrderSystem.cs:759-774; eligibility at :185-197 |
| Only exact matching ore mined for that character after acceptance counts | server/customizations/ClusterFWorkOrderSystem.cs:573-603; server/customizations/CompactOreSatchelRoutingHook.cs:145-150. Credit uses the actual ore handed over, after substitutions and yield bonuses, before satchel routing. Inventory transfers and smelting do not call this quota hook. |
| Active shows progress; completed quotas consume no ore and need a Turn In action for payment | server/customizations/GuildContractLedgerGump.cs:306-310, :536-548, :562-605; server/customizations/ClusterFWorkOrderSystem.cs:281-327 |
| Old ore entries retain either-way completion: 100 iron for Raw Ore Sample, 150 iron for Ore Refinement Run, or the respective new mining quota | server/customizations/ClusterFWorkOrderSystem.cs:295-297, :320-325, :368-369, :399-410, :648-661, :759-774. Legacy turn-in applies only to pre-quota entries and takes ore only when the quota is unmet. |
| Existing held Stone Contracts remain finishable without relearning eligibility | server/customizations/GuildContractLedgerGump.cs:562-591 checks requirements at turn-in, not eligibility; stone remains an item requirement |
| Missing vouchers cost 100 gold each by default; held vouchers, ingots, and base gold remain part of payment | server/customizations/MinersCompactLiaisonGump.cs:108-109, :674-680, :775-823, :1030-1083 |
| Reinforced restoration example: 4 vouchers, 100 iron ingots, 15 dull copper ingots, 1,000 base gold; with 1 voucher pay 1,300 gold | server/customizations/MinersCompactLiaisonGump.cs:51-54, :611-618, :819-823 |
| Restoration needs membership, an unlocked tier, and no active copy; normal page offers the highest unlocked tier | server/customizations/MinersCompactLiaisonGump.cs:627-672, :1030-1054 |
| Pack and bank pay costs; insufficient funds are checked before consumption | server/customizations/GuildResources.cs:282-341; server/customizations/CompactGoldHelper.cs:23-61; server/customizations/MinersCompactLiaisonGump.cs:1068-1083 |

Supporting context read: [P416 implementation notes](cc-P416-stone-mining-gate.md), [P548 source review](cc-P548-review-stone-mining-gate.md), and [existing gathering guilds draft](wiki-drafts/gathering-guilds.md). P417's broader gathering redesign is not treated as implemented behavior in this guide.

## Open questions and verification limits

- **Unverified: deployment and configured prices.** No connection to Haven or the live shard was made. Book standing, voucher price, and the gold-per-missing-voucher rate are configurable; the draft explicitly uses source defaults and directs players to the displayed prices. The Stone Crafter price is the stock vendor-table base price. Actual stock and vendor availability were not checked.
- **Unverified: Iron Beetle quota credit.** P416 left this open. The draft gives no promise about pet-mined ore. Player mining through the quota hook was source-verified.
- **Unverified: client presentation and runtime behavior.** No game client session or build was run. UI wording and paths were read in source. P548 records test gaps for legacy Ore Refinement Run completion and voucher changes during confirmation, plus a shared turn-in method replay risk; this docs task makes no claim that those have been fixed or reproduced.
- No blocking question prevents delivery of the requested draft. A publication review should confirm rollout and the displayed prices first.

## Validation

No lane tests were requested. No tests or gates were added, so no red/green cycle applies. Source cross-checks and prose review cover the draft's claims, table values, and restoration arithmetic. Final checks cover relative Markdown links, absence of em dashes, whitespace, file sizes, and notes-only changes.

Ran tools/progress.py --dry-run with SL_SHARD and SL_MIGRATE pointing to the work copies: exit 0, report completed. The reporter writes tools/progress.json even with --dry-run; its exact previous bytes were preserved and restored so this task leaves only the requested Markdown deliverables.

Final inspection passed: all relative links resolve; no em dashes, trailing whitespace, or oversized files; final newlines present; git diff --check clean. The code work copy is clean and the notes work copy contains only the requested guide and both P551 notes files. No stop request was present at the final checkpoint.

P551 DONE
