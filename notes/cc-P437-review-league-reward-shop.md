# P437: League reward shop review

Reviewed 2026-10-22 against code commit `7508639` and notes commit `8dd79a9`. Notes only; no code changes.

Read `cc-P229-league-reward-shop.md`. No separate P229 Codex review was found beside it; `cc-P379-crystal-review-10-21-merges.md` explicitly excludes P229 from its review range.

## Findings

1. **risk**: `server/customizations/LeagueShop/LeagueShop.cs:148` and `:198`, `server/customizations/ClusterFAccountData.cs:668`, and `server/customizations/LeagueShop/LeagueHall.cs:62`: the shared purchase path accepts a negative Hall Renown setting, so a price of -1 increases a balance of 10 to 11, while `int.MinValue` can overflow the balance after the reward is delivered. Reject negative prices before fulfillment and in `SpendRenown`, and add tests for negative settings and integer boundaries; this requires a bad server setting, not client control of the price.

2. **bug**: `server/customizations/LeagueShop/LeagueShopItems.cs:175` and `:196`: after starting the dye target, a player can move or transfer the pigment out of the backpack and still use the pending target on their own item, consuming the pigment from its new location. Recheck `_pigment.IsChildOf(from.Backpack)` in `OnTarget` before changing the item or deleting the pigment, and test moving it away between double-click and target response.

3. **risk**: `server/tests/Misc/LeagueShopVerification.cs:92` and `:182`: purchases are tested with room available, but no test reaches `NoRoom`, so the promise of no charge and no partial reward on a full pack is unprotected. Add cases for a missing pack, item and weight limits, and regalia with room for only two pieces, checking unchanged Renown, no delivered pieces, and deletion of all generated rewards, including rejected boxes' contents.

4. **risk**: `server/tests/Misc/LeagueShopVerification.cs:488` and `:199`: the window test only inspects entries, and the duplicate-title test repeats a direct purchase on the same character, leaving stale confirmation responses and account-wide duplicate refusals untested. Exercise `LeagueShopConfirmGump.OnResponse` after AP or Renown changes and after another character on the account buys the title, and verify that refusals deliver nothing and spend nothing.

## Checks with no finding

- No negative-price or overflow path was found in P229's starter table (`LeagueShop.cs:92`): its literal prices are positive, and purchases subtract one price without quantity multiplication; the settings risk above comes from the later Hall caller of the shared method.
- No full-pack token-loss bug was found by reading the purchase path: `LeagueShop.cs:179` creates the rewards, `:181` checks capacity for the whole purchase, and `:198` charges only after delivery. `CanHoldAll` at `:219` includes all three regalia pieces' item count and weight, matching pinned `Projects/Server/Items/Container.cs:230`; rejected boxes delete their stored contents through `LootBoxItems.cs:285`.
- No client-only eligibility check was found: `LeagueShopConfirmGump.OnResponse` calls `Purchase` at `LeagueShopGumps.cs:222`, which reruns `Check` at `LeagueShop.cs:163`. P229 requires AP and Renown, not League rank or registration, as its implementation notes specify.
- No account-wide duplicate-title purchase bug was found: ownership is checked at `LeagueShop.cs:143` and recorded at `:172` in the shared account record (`ClusterFAccountData.cs:1073`, `:1321`). Repeatable cosmetics are intentional; bought titles are the once-per-account rewards.

## Scope and verification

Read the shop, gumps, items, and `server/tests/Misc/LeagueShopVerification.cs`; checked P229's account serialization, achievement, Registrar, `AccountDataSerializerVerification.cs`, and `RequisitionsVerification.cs` changes. Followed fulfillment into `LootBoxes/LootBoxItems.cs`, `ClusterFBackpack.cs`, and pinned container code, and checked the Hall price caller and `LeagueHallVerification.cs` for the shared-method finding.

The pigment finding follows the source path: pinned `Projects/UOContent/Network/Packets/IncomingItemPackets.cs:35` calls `Mobile.Lift` without canceling the target; `Projects/Server/Mobiles/Mobile.cs:5039` also leaves it active, and `Projects/Server/Targeting/Target.cs:146` checks the selected item rather than the source pigment. Runtime and client reproduction remain unverified.

No tests were added or run, and no build or server connection was made, as this is a notes-only review with no lane tests. Existing test results in P229's note were not rerun. Ran `tools/progress.py --dry-run` with both work-copy paths; it completed successfully but rewrote `tools/progress.json` despite the flag, so that generated file was restored to its initial contents to keep this task notes-only.

P437 DONE
