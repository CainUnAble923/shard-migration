# P587: review of the Hammer of Hephaestus T3 and Craft This Order

Reviewed 2026-10-25 by the Golem's Codex lane. Documentation only. No code changed.

## Scope and evidence

Read these task records:

- `notes/cc-P168-hammer-t3-craft-order.md`
- `notes/cc-P372-cont-fixup-hammer-t3-craft-order.md`
- `notes/cc-P372-cont-fixup-hammer-t3-craft-order-codex-review.md`

Reviewed the merged tree at `6b74371`, using `608d0b4` as the pre-P372 comparison. The diff has these 19 paths, including packaging, release notes, and tests, rather than 19 C# implementation files:

```text
CHANGELOG.md
docker/uo/apply-patches.sh
player-package/tests/Cliloc-Overrides.Tests.ps1
player-package/vendor/shattered-legacy-cliloc/entries.json
player-package/vendor/shattered-legacy-cliloc/registry.csv
server/customizations/ClusterFCraftOrder.cs
server/customizations/ClusterFCraftRun.cs
server/customizations/ClusterFSmithBODPayout.cs
server/customizations/HammerOfHephaestus.cs
server/customizations/Services/BulkOrders/BulkOrderDeedGumpLines.cs
server/customizations/Services/BulkOrders/BulkOrderGuildPay.cs
server/customizations/Services/BulkOrders/BulkOrderVendors.cs
server/customizations/ShardClilocs.cs
server/customizations/SmithGuildmasterGump.cs
server/patches/BOD-properties-guild-pay.patch
server/patches/CraftItem-shard-hooks.patch
server/patches/PlayerMobile-craft-order-hurt.patch
server/tests/Engines/Craft/HammerCraftOrderVerification.cs
server/tests/Services/BulkOrders/BulkOrderGuildPayVerification.cs
```

Traced the relevant dependencies in canonical customizations and patches, including `LargeBODItemFill.cs`, `BODCombineContained.cs`, `ClusterFSmithBODSystem.cs`, and `server/patches/LargeSmithBOD.cs`. Checked the older held-bonus tests in `server/tests/Engines/Craft/HammerHeldBonusVerification.cs`.

The read-only `D:/UO/ModernUO-pinned` tree is clean at `d4531cd94b739613155225c234900de9f47d2c88`, matching the Dockerfile. Upstream references below are relative to that tree. Shard references are relative to the code work copy.

These are source-level findings. The described runtime outcomes need regression probes before implementing fixes. I did not run the server, build an image, rerun the shard tests, or verify a client. P372's reported green build is historical evidence, not a test result from this review. No Haven connection or deployment was made.

## Findings

### 1. Medium [P2]: consuming the last charge leaves the held skill bonus active

**Location:** `server/customizations/HammerOfHephaestus.cs:1065`, with the exhaustion trigger at `:1187`.

`ApplyHeldBonus` checks `_exhausted`, deletion, and the holder, but not the remaining uses. Successful and failed crafts decrement the inherited `UsesRemaining` property. Neither path calls `TriggerExhaustion`. That method is reached only by a later double-click. After the last charge, the order loop stops, but the held hammer still has its +15 Blacksmithy modifier and `_exhausted` remains false. A save and load also schedules the same bonus application without checking the empty charge count.

The existing test at `server/tests/Engines/Craft/HammerCraftOrderVerification.cs:210` checks that the run stops and uses reach zero. It never checks `Exhausted` or the modifier after depletion.

**Suggested fix:** make depletion update the exhaustion state and remove the modifier as soon as uses reach zero, for both successful and failed attempts. Require positive uses in `ApplyHeldBonus` as well. Add regression cases for last-use depletion and an equipped empty hammer after loading, without double-clicking first. Keep the last attempt's skill calculation intact.

**Correction to the earlier P372 review:** its proposed exploit of keeping an empty T3 equipped while smithing with an ordinary backpack tool is blocked by upstream `Projects/UOContent/Items/Skill Items/Tools/BaseTool.cs:128` (`CheckTool`) and `Projects/UOContent/Engines/Craft/DefBlacksmithy.cs:100`. The stale modifier is real in the source; that particular route to using another tool is not supported by the source. Also, upstream `DefBlacksmithy.cs:95` accepts zero uses and refuses negative uses, so exhaustion needs enforcement in actual craft validation, not only in double-click handling.

### 2. Medium [P2]: regeneration banks time while the hammer is already full

**Location:** `server/customizations/HammerOfHephaestus.cs:1019`.

The full-hammer early return leaves `_lastRegenAtTicks` unchanged. After a full hammer sits unused for an hour, spending a charge and refreshing its properties can immediately restore that charge from the hour spent at full capacity. The timestamp represents the constructor or previous regeneration, rather than the start of the current missing charges. The 800-use cap limits the visible total but does not prevent credit from time when no charge was missing.

This does not prove unlimited charges. The normal Craft This Order stop at `server/customizations/ClusterFCraftRun.cs:256` still checks for fewer than one use. The defect is stored regeneration credit beyond the intended full capacity. T3 copies this pattern from the earlier tiers.

**Suggested fix:** discard regeneration credit accrued while full, and start or maintain the next-charge time when the hammer first becomes less than full. Preserve the intended partial interval while it remains below full. Add a test that leaves a full T3 idle for several intervals, spends one use, and confirms that the missing use needs a new ten-minute interval. The present craft tests construct fresh hammers and do not exercise this boundary.

### 3. Medium [P2]: automatic large-order combining can waste a completed small deed

**Location:** `server/customizations/ClusterFCraftOrder.cs:177`.

`CombineSmallDeeds` offers every completed small smith deed to the large deed before crafting. Upstream `Projects/UOContent/Engines/Bulk Orders/LargeBOD.cs:147` adds the small deed's whole `AmountCur` and deletes it. It only checks whether the line is already full, not whether the whole small deed fits.

For example, a large order with a gorget line at 8/10 and a matching completed 10/10 small gorget deed consumes that whole small deed and sets the line to 18. The large deed counts as complete, but eight items of the small deed's value were unnecessary. This situation is reachable because the shard permits filling large deeds one crafted item at a time. The underlying combine behavior predates P168; automatically selecting that destructive combine is new here.

**Suggested fix:** before an automatic combine, check the matching line's remaining space. Preserve the small deed when its whole amount would exceed that space, then craft only the missing pieces. Keep the existing manual combine behavior as a separate decision. Add the partial-line case to `server/tests/Engines/Craft/HammerCraftOrderVerification.cs:336`; the current test combines a small helm deed into an empty helm line, so it misses this loss.

### 4. Medium [P2]: cached payout tooltips can describe a previous holder or guild state

**Location:** `server/customizations/Services/BulkOrders/BulkOrderGuildPay.cs:147`, with refresh limited to `:178`.

The text depends on `RootParent`, that player's guild membership, and that player's completed-order setting. Upstream `Projects/Server/Items/Item.cs:850` caches the property list. Its parent setter at `:676` does not invalidate it. The new code refreshes backpack deeds when the payout setting changes, but adds no refresh for a change of holder or guild membership.

Generate a completed deed's tooltip for a Society member using Always bank, then transfer it to a Society member using Always cash out. The cached tooltip can still promise Seals while the payout follows the recipient's gold setting. A completed deed transferred from a non-member can instead retain no guild-pay line. Moving a container that holds the deed has the same dependency problem. Joining or leaving the relevant guild can also leave stale text. Opening the deed gump recomputes its lines, so the gump and tooltip can disagree.

**Suggested fix:** invalidate affected deed properties after changes to the root holder or guild membership, including container transfers. Continue refreshing on payout-mode changes. Test a real cached `deed.PropertyList` before and after each change. `server/tests/Services/BulkOrders/BulkOrderGuildPayVerification.cs:143` constructs a fresh `ObjectPropertyList` and calls `GetProperties` directly, so that helper cannot catch a stale cached list. This confirms the earlier P372 tooltip concern at the source level.

### 5. Medium [P2]: reading hammer properties performs a mutation forbidden by the pinned property-list builder

**Location:** `server/customizations/HammerOfHephaestus.cs:1233`, through the uses assignment at `:1028`.

`GetProperties` calls `ApplyPassiveRegen`. When a charge is due, that changes the inherited `UsesRemaining` property, whose field has `[InvalidateProperties]` in upstream `Projects/UOContent/Items/Skill Items/Tools/BaseTool.cs:24`. Recovering from exhaustion also changes the hue and explicitly invalidates properties.

Upstream `Projects/Server/Items/Item.cs:2618` rejects invalidation while the cached property list is being built. It throws in DEBUG and logs an error and refuses the nested invalidation in RELEASE. Thus reading a below-full T3's real cached property list when regeneration is due reaches a forbidden side effect. A DEBUG build can fail the read before the timestamp update finishes. The inherited T1/T2 approach has the same problem; copying it into T3 carries it forward.

**Suggested fix:** apply regeneration outside property-list construction, through a suitable timer or action hook, and make `GetProperties` read the resulting state. Add a due-regeneration test using the actual `PropertyList` cache, with an assertion that building it neither throws nor mutates charges. Direct calls to `GetProperties` on a separate list do not exercise the builder's guard.

### 6. Low [P3]: T3-specific tests omit important tool, resource, and order transitions

**Locations:** `server/tests/Engines/Craft/HammerHeldBonusVerification.cs:70`; `server/tests/Engines/Craft/HammerCraftOrderVerification.cs:79`, `:336`, and `:388`.

The older held-bonus factory takes a Boolean and constructs only T1 or T2. T3 is absent from its repeated equip/remove, held-load, restore, and regeneration checks. The new save/load test checks charge and familiarity data, not the equipped modifier lifecycle.

The new craft tests also leave these behaviors unverified:

- A genuinely failed skill roll during an order, including material loss, one use spent, no ingot refund, no deed progress, and continuation to a later success. The normal-quality exceptional-deed test is a successful craft rejected by the deed, not a failed craft.
- A large order that must craft more than one unfinished item type. The present large-order case only crafts two gorgets after combining a helm deed, so it cannot detect a broken transition between craft recipes.
- A colored deed crafted to completion, including a post-Valorite metal, with the matching familiar-metal refund. The refund test crafts iron at the cap and dull copper at zero familiarity; it does not verify a positive colored-metal refund or the order's material selection.
- Deed removal and hammer removal during an active order. The initial refusal tests check the bank and an unequipped hammer before starting, which does not test those mid-run stops.

**Suggested fix:** extend the held-bonus fixture to select all tiers and add focused order tests for these transitions. Include a check that equipping an Ancient Smithy Hammer while using a backpack T3 gives only the Ancient hammer's held modifier, and that moving the T3 back into hand removes the other tool's contribution. Each new regression must be observed failing before the relevant fix, then passing, as the working agreements require.

## Checks that did not produce a finding

- No ordinary route to stacking T3's held bonus with T1, T2, or an Ancient Smithy Hammer was found. These tools use the one-handed equipment layer, T3 removes its own modifier on removal, and `BaseTool.CheckTool` limits the active tool. T3's resource refund follows the tool actually used; it does not apply merely because a T3 is somewhere in the backpack.
- The successful-craft hook refunds the selected metal, uses familiarity from before that craft's gain roll, and excludes the Dev Testing Crystal bypass. The failed-craft path does not call that hook. For ordinary single-item smith recipes, `MetalUsed` follows the same subresource substitution used by upstream `CraftItem.ConsumeRes`. No negative material cost or refund over the recipe's ingot cost was found.
- Craft This Order explicitly selects iron for a deed with no material, rather than reusing the player's last selected colored metal. A large order selects the next unfinished recipe after each attempt. The direct fill uses the deed's combine rules for type, exceptional quality, and material. Taking eligible small deeds first is the recorded design choice; finding 3 concerns partial lines, not that choice of sequence.
- The Society payout and stock vendor payout now read the same deed quote as their corresponding display helpers. The normal terms changed by bribery are included in quote invalidation. The tooltip-cache problem in finding 4 is separate from the payout calculation.
- The merged patch runner retains the new tooltip and damage hooks after the existing patches. The cliloc number 1900011 and its text agree across the changed server constant, package entries, registry, and test expectation. Actual patch application and client rendering were not rerun.

## Verification and handoff

No new tests were written, so no red/green result is claimed. Lane tests are none for this review. P372's reported tests do not cover the missing cases above.

Ran the required progress reporter with work-copy path overrides and `--dry-run`; it exited successfully. Despite its option description, `build()` writes `tools/progress.json` before the dry-run return. Restored that generated file byte-for-byte from HEAD because it was clean before the command and this task requests only the review note. No progress files are part of the deliverable. No coverage totals from that unrelated report are used here.

Only this notes file is intended for the Golem to commit. No branch changes, commits, merges, or pushes were made. Runtime reproduction, regression tests, and all suggested code fixes remain for a follow-up implementation task.

P587 DONE
