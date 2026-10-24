# P546: review of retiring civic waste bundles (P414)

2026-10-24. Notes only. No code changed, tests added or executed, builds run, or live services contacted.

P414 code commit `3821e70d7f6c540bbb2ea5a8c09e3ec61e0a567d` is an ancestor of local `main`, merged by `86654d1`. The reviewed customization and test trees match local `main`. Upstream references below use the read-only ModernUO source at `D:/UO/ModernUO-pinned`, commit `d4531cd94b739613155225c234900de9f47d2c88`.

Read both work-copy AGENTS.md files, direction-decision.md, tasks.md, `notes/cc-P414-retire-civic-waste-bundles.md`, and the related P432 review and its Codex review. No separate P414 review note was found. Existing barrel, crafted-sandal, wood, cloth, and ordinary store-conversion findings are not repeated below.

## Findings

1. **bug** | `server/tests/Services/CivicContractPointsVerification.cs:315`; `server/customizations/ClusterFWorkOrderSystem.cs:2676`, `:2682`: The vendor-farm guard uses fresh buy-list prices without applying town discounts. A Felucca faction town with a -20%, -25%, or -30% tax sells the 5 gp sandals for 4 gp after integer rounding; after accepting Refuse Collection, buying and dumping 25 pairs costs 100 gp, earns 50 Clean Up points, and returns all 100 gp through the repeatable contract while keeping the points spendable. Stock and restocks limit the rate, but the loop replenishes its gold and can farm store points without further gold cost. Suggested fix: test the actual minimum final vendor prices, including rounding and tax, and adjust contract requirements or eligible point sources so even the cheapest reachable purchase leaves a positive net cost for retained points.

   Source trace: pinned `Projects/UOContent/Engines/Factions/Gumps/FinanceGump.cs:13` permits these negative taxes; `Engines/Factions/Core/Town.cs:145` resolves faction towns on the faction facet. `Mobiles/Vendors/BaseVendor.cs:162`, `:1353`, and `:1361` apply the tax to buy information, and `Mobiles/Vendors/GenericBuy.cs:79` computes `(5 * 80 + 50) / 100` as integer 4. `Mobiles/Vendors/SBInfo/SBCobbler.cs:19` sells sandals at base price 5, while our `Services/PointsSystems/CleanUpBritanniaData.cs:461` values each at 2. P414 keeps the points at turn-in and does not limit repeat completions. This is a source-derived scenario, not a live reproduction; current town ownership, taxes, vendor placement, and live availability are unverified. Unlike P414's documented purchase of store points for gold at ordinary prices, this loop recovers the entire purchase cost.

2. **risk** | `server/customizations/ClusterFWorkOrderSystem.cs:526`; `server/customizations/ClusterFCustodianSystem.cs:632`: An old contract has no baseline until its requirements are inspected, but redeeming bundles does not initialize that baseline before deleting the stack and awarding points. A player with an old Refuse Collection contract who follows the Warden's bundle instructions first can redeem five bundles for 50 points, then open the Active tab and see zero progress; those bundles cannot be presented again, so the player must earn another 50 points for the 100 gp contract. P414 explicitly chose initialization at the first look, but neither the Warden's instructions nor the redemption path explains this ordering requirement. Suggested fix: initialize old civic baselines after point data loads and before any new award, or at least initialize them before bundle redemption; add a regression that redeems bundles before opening the old contract.

   The current migration test, `server/tests/Services/CivicContractPointsVerification.cs:246`, inspects requirements before awarding new points, so it misses this player sequence. Opening the Warden's status gump reads lifetime and spendable points but never inspects the old contracts. This is a source-derived compatibility risk; no live save or client session was tested.

3. **risk** | `server/tests/Services/CivicContractPointsVerification.cs:142`: The claimed-points test accepts both contracts at the same lifetime total, completes only the smaller contract, and checks the larger one's remaining progress without completing it. That leaves the partial-overlap branch in `ClusterFWorkOrderSystem.cs:563`, reverse completion order, a third open civic contract, and persistence of adjusted baselines without regression coverage. Suggested fix: add staggered-acceptance and reverse-order completion cases, including a save/reload after a claim, and assert cumulative gold and remaining progress through actual turn-ins. No accounting defect in those branches was established by this review.

## Checks and limits

No repeat redemption of a deleted bundle stack was found: `RedeemBundles` checks deletion and deletes the stack before awarding points. No new bundle producer was found in the customization tree. No double gold payout or missing normal gold reward was found through the ledger and League Register turn-in callers; both select their entries from the active list. The current civic definitions retain the 100, 300, 750, 1,500, and 4,000 gp rewards.

Reviewed P414's implementation files and its test file:

- `server/customizations/CleanedDebris.cs`
- `server/customizations/ClusterFCustodianSystem.cs`
- `server/customizations/ClusterFWorkOrderSystem.cs`
- `server/customizations/GuildContractLedgerGump.cs`
- `server/customizations/SanitationWarden.cs`
- `server/customizations/SanitationWardenGump.cs`
- `server/customizations/TrashBag.cs`
- `server/tests/Services/CivicContractPointsVerification.cs`

Also traced the point award and lifetime record, League Register turn-ins, and pinned vendor pricing paths cited above. P414's recorded green build is historical evidence, not a test run for this review. Any regressions added during follow-up must be seen failing before the fix and passing afterward.

Ran `tools/progress.py --dry-run` against this code work copy successfully. It rewrote `tools/progress.json` despite dry-run; that incidental output was restored byte for byte. Only this review note is intended to change.

P546 DONE
