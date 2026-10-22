# P432: Clean Up Britannia and Custodians review

2026-10-22. Review of merged P33 and P175. Notes only; no code changed, tests added, builds run, or live services contacted.

Read both work-copy AGENTS.md files, direction-decision.md, tasks.md, and the P33 and P175 implementation notes. No separate P33 Codex review was found beside its note; the P386 guide review has no findings. Previously recorded wood and cloth premiums, bundle farming, property-weight deviations, missing rewards, and corpse-base persistence are not repeated as new findings.

Paths below are relative to the ShatteredLegacy work copy unless labeled otherwise. These findings follow the current source and pinned ModernUO at `d4531cd94b739613155225c234900de9f47d2c88`; gameplay reproductions remain unverified.

## Findings

1. **bug** | `server/customizations/Services/CleanUpBritannia/CleanUpTrash.cs:78`, `:111`, `:127`: A house barrel remembers an item's original value by serial, so depositing 1,000 iron ingots, lifting one from that stack, retrieving the remaining 999, and returning the original one can pay 100 points when only one ingot is destroyed. Invalidate records on withdrawal and track the quantity actually destroyed, with a regression covering this sequence; this bookkeeping flaw is also present in ServUO's BaseTrash and needs a deliberate fix rather than another faithful copy.

2. **bug** | `server/patches/TrashBarrel-clean-up-britannia.patch:29`, `server/customizations/Services/CleanUpBritannia/CleanUpTrash.cs:74`: The barrel records a drop after the base container has stacked it, so a second matching stack is already deleted and scores zero while the surviving stack retains only its first deposit's cached value, losing points and potentially another dropper's credit. Record accepted quantities before stacking consumes their identity and cover matching stacks from both the same player and different players, including a drop directly onto a stack.

3. **bug** | `server/customizations/Services/PointsSystems/CleanUpBritanniaData.cs:121`, `:461`; `server/tests/Services/CleanUpBritanniaPointsVerification.cs:500`: Crafted sandals take the fixed 2-point table entry before the crafted-equipment rule, although their four regular leather cost only 0.4 points, and the anti-farm measurement explicitly skips types in that table. Give player-crafted sandals a material-based value while preserving the intended value of noncrafted sandals, and include table-listed craft outputs in the measurement; this is a separate inherited ServUO loophole from the already documented wood and cloth premiums.

4. **bug** | `server/customizations/TrashBag.cs:85`: Asking for a replacement deletes every old owned bag and recursively deletes its contents without points or a warning, even if the bag is in the bank or another character's backpack. Recover the contents safely before replacing the bag, or refuse replacement until that can be done, and test full bags in each location rather than only the empty bags covered today.

5. **bug** | `server/customizations/ClusterFCustodianSystem.cs:367`, `:387`: The area sweep checks eligibility but never checks each item's visibility, line of sight, accessibility, or height, so an accessible target point can clear items behind walls or on another floor, including corpse loot hidden from that Custodian by instancing. Validate each deletion against the acting character and preserve protected loot rights, with command-level tests for walls, floors, and another player's instanced corpse rather than only value-helper tests.

6. **risk** | `server/customizations/ClusterFCustodianSystem.cs:130`, `:167`: A monster corpse is accepted before its contents are examined, and recursive valuation plus corpse deletion bypasses the blessed and quest-item exclusions for descendants, including protected items inside nested containers. Refuse a corpse containing protected belongings or preserve those belongings explicitly, and test nested protected items while retaining the deliberate rule that ordinary corpse gold contributes points.

7. **bug** | `server/customizations/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:438`: Purchase confirmation checks only the trader's coordinates, so a player can open confirmation, change facets to the same coordinates, and still buy from the old trader. Require the trader to exist on the player's current map before checking range, and test confirmation after a facet change or trader deletion rather than only opening the store from far away.

## Evidence and test coverage

- The stack sequence in finding 1 follows pinned `Projects/Server/Mobiles/Mobile.cs:5235`: `LiftItemDupe` reduces the original item's amount to the lifted amount and creates a new serial for the remainder. Neither withdrawal nor return refreshes the original cleanup entry, and confirmation checks the serial rather than its remaining amount.
- Finding 2 follows pinned `Projects/Server/Items/Container.cs:426` and `Projects/Server/Items/Item.cs:2480`: the container merges stacks before returning, and `StackWith` deletes the incoming item. Our `GetPoints` returns zero for a deleted item (`CleanUpBritanniaData.cs:114`).
- Sandals' actual recipe is pinned `Projects/UOContent/Engines/Craft/DefTailoring.cs:367`, and their default material is regular leather in `Projects/UOContent/Items/Clothing/Shoes.cs:169`. The fixed sandal value also exists in the ServUO reference; the proposed crafted-item exception therefore needs its deviation recorded by the overseer.
- Recursive deletion in finding 4 follows pinned `Projects/Server/Items/Item.cs:1549` and `:3542`. The existing replacement test, `CustodianLayerVerification.cs:96`, replaces empty bags, so it does not exercise lost contents.
- Corpse instancing is enforced by pinned `Projects/UOContent/Items/Misc/Corpses/Corpse.cs:465`; the sweep calls neither that visibility check nor a per-item access check. The corpse tests exercise values, pet exclusions, kill rights, and lifetime awards, but do not execute the cleanup targets against protected or inaccessible corpses.
- Pinned `Projects/Server/Mobiles/Mobile.cs:3076` confirms that `InRange(Point3D, int)` compares only X and Y. The existing store-distance test does not send purchase confirmation after changing maps.

Read the relevant implementation paths listed in P33, including the barrel patches and their routing, bag migration, craft reject routing, guild synchronization and resets, work orders, store, placement, and NPC entry points, plus P175's valuation and corpse record. Reviewed these test files:

- `server/tests/Services/CleanUpBritanniaPointsVerification.cs`
- `server/tests/Services/CleanUpBritanniaBarrelVerification.cs`
- `server/tests/Services/CleanUpBritanniaStoreVerification.cs`
- `server/tests/Services/CustodianLayerVerification.cs`
- `server/tests/Services/CleanUpPropertyWeightVerification.cs`
- `server/tests/Services/ClusterFCorpseValueVerification.cs`

No tests were executed or added for this notes-only review. Suggested regressions above must be observed failing before fixes and passing afterward; the earlier implementation notes' green builds are historical evidence, not a test run for this review.

## Store prices

No price mismatch found between the implemented OSI reward rows in `server/customizations/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs` and the matching rows in `D:/UO/ServUO-pub57/Scripts/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs`. A read-only comparison matched types, accounting for the `ScrollofAlacrity` spelling, and compared every implemented price.

The tiers shown on the [official UO Clean Up Britannia reward page](https://uo.com/wiki/ultima-online-wiki/gameplay/npc-commercial-transactions/clean-up-britannia/) agree with the corresponding store tiers, including mushrooms at 5,000, pigments at 250,000, and talismans at 300,000. No OSI price defect found in those checks; the custom consumable supplies have no OSI counterpart, and no live OSI vendor was inspected.

## P414 and P415 safeguards

P414 and P415 are queued, as stated in this prompt. Their implementations are not present for review here.

- **P414, bundle retirement:** Remove bundle production from both the area sweep and bag dump, the civic-contract requirements and gold payouts, and the Warden's bundle instructions together; account for existing `CleanedDebris` and accepted work orders. Preserve per-character Clean Up balances, lifetime-based standing, store purchases, and the existing Civic Token retirement behavior; bundle removal alone does not close the point farms in findings 1 and 3.
- **P415, trash bag corpse clearing:** Both the preview (`TrashBag.cs:170`) and payout (`:269`) currently call `ComputePoints(item)` without the player, so admitting corpses without changing those calls would omit the earned Fame base. Pass the acting character to both, preserve bag ownership and location checks, player-corpse rejection, pet and summoned exclusions, kill-credit rules, and the protection checks in findings 5 and 6; delete and award a corpse once, without separately paying its recursively included loot again.

## Completion checks

Only this notes file changes. Source inspection and the read-only price comparison completed; runtime behavior, current live shard state, and the future P414/P415 implementations remain unverified.

Ran `tools/progress.py --dry-run` with `SL_SHARD` set to this work copy; it exited successfully but still regenerated `tools/progress.json` before its dry-run return. Restored that incidental output to its initially clean contents and confirmed the code work copy is clean and the migration work copy contains only this new note; whitespace, file size, finding format, and absence of em dashes were checked.

P432 DONE
