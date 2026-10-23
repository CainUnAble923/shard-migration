# P468: League hall decor rewards review

Reviewed 2026-10-23 against code commit `4c2af57` and notes commit `b807bcb`. Notes only; no code changes.

Read `cc-P243-league-hall-decor-rewards.md`; no separate P243 review was found beside it. Also read P437 and its Codex review, so its negative Hall price finding and shared shop test gaps are not repeated here; P243's already documented successful wall-placement test gap is not repeated either.

## Findings

1. **bug**: `server/customizations/LeagueShop/LeagueHall.cs:314`, `:334`, and `:468`: chopping with a full backpack deletes the addon and drops its replacement deed on the ground through inherited `BaseAddon.OnChop` and `Mobile.AddToBackpack`, bypassing the deed's drop refusal; the regular, movable deed can then decay even inside the house (`pinned Projects/UOContent/Items/Addons/BaseAddon.cs:108`, `:121`, `Projects/Server/Mobiles/Mobile.cs:7594`, `:7605`, and `Projects/UOContent/Regions/HouseRegion.cs:205`). Refuse chopping until the replacement deed can be stored safely, keep the addon on failure, and add a full-backpack chop test that checks no ground deed and no reward loss.

2. **risk**: `server/customizations/LeagueShop/LeagueShopGumps.cs:179`, `:222`, and `:350`: a Hall confirmation retains a snapshot of its price and AP requirement, so raising `case.glass` from 150 Renown and 250 AP to 1,000 Renown and 1,750 AP while that confirmation is open still lets a 250-AP buyer purchase at 150. Resolve the Hall key again when Buy is pressed and refresh confirmation if its terms changed, with a test that changes both settings after opening confirmation.

3. **risk**: `server/customizations/LeagueShop/LeagueHall.cs:277` and `:314`: account binding protects the deed but does not stop a decorated house from being transferred to a different account, which keeps the placed rewards without meeting their AP gates; chopping then gives that owner a deed still bound to the original buyer (`pinned Projects/UOContent/Multis/Houses/BaseHouse.cs:3836` and `Projects/UOContent/Items/Addons/BaseAddon.cs:88`, `:112`). To enforce P243's stated rule that another account cannot acquire gated decor, recover these addons safely to their bound account before cross-account house transfer, and test transfer followed by chopping.

4. **risk**: `server/tests/Misc/LeagueHallVerification.cs:332` and `:361`: the lifecycle test places and chops in memory, leaving deed binding, component links, separate shelf and insert hues, and trophy wall offsets untested across save/load. Add serialization round-trip coverage for an unused deed, a dyed display case, and a trophy, then verify placement or chopping still yields exactly one correctly bound reward after loading.

## Checks with no finding

- No free duplicate purchase or double claim was found in the normal positive-price path: `LeagueShop.cs:163` rechecks eligibility and balance, and `:198` charges every repeat purchase; Hall decor is repeatable merchandise, not a once-per-account claim.
- No repeat-placement duplication was found: `LeagueHall.cs:401` refuses a deleted deed, `:406` rechecks its account, `:412` rechecks its backpack location, and `:429` deletes it on successful placement. Failed placement deletes the temporary addon at `:445` and retains the deed.
- No placement outside an owned house was found: `LeagueHall.cs:422` uses pinned `BaseAddon.CouldFit`, whose component checks require an owned house (`Projects/UOContent/Items/Addons/BaseAddon.cs:156`, `:198`). Trophies also use its adjacent-wall check at `:165`; successful wall mounting remains a client verification item already recorded by P243.
- No ordinary placed-addon decay or clear restart-loss defect was found by source inspection. Pinned addons and their components are immovable, `Projects/Server/Items/Item.cs:336` ties ordinary decay to movability, and the Hall's custom state plus the base addon/component references and house addon list have serialization fields or read/write paths; this does not verify an actual restart.

## Scope and verification

Read `server/customizations/LeagueShop/LeagueHall.cs`, `LeagueShop.cs`, `LeagueShopGumps.cs`, the binding helper in `server/customizations/LootBoxes/LootBoxItems.cs`, the art initialization in `server/customizations/ShatteredRunestone.cs`, and `server/tests/Misc/LeagueHallVerification.cs`. Read the Hall fact in `player-package/tests/Build-UoOverrides.Tests.ps1:512` and the Hall entries in the art registry, records, and source credits.

Followed placement, chopping, house transfer, moving-crate recovery, decoration movement, and decay through the clean read-only `D:/UO/ModernUO-pinned` checkout at `d4531cd94b739613155225c234900de9f47d2c88`. In the findings, `pinned` paths are relative to that checkout.

These are source-review findings; runtime and client reproduction remain unverified. No tests were added or run, no build was made, and no live server or Haven connection was made; existing P243 test results were not rerun, as this task specifies no lane tests.

Ran `tools/progress.py --dry-run` with the two work-copy paths; it completed successfully. It writes `tools/progress.json` despite that flag, so its original contents were retained in memory and restored byte for byte, leaving the review note as the only changed file.

P468 DONE
