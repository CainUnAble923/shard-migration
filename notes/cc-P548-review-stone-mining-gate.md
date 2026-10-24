# P548: review of the P416 stone mining gate and mining quotas

Reviewed 2026-10-24. Notes only. No code changed.

## Scope and evidence

P416 commit `7266d07b067a98276a09f76156ba8440278ddf3e` is an ancestor of local `main`. The reviewed implementation and its test file match `main` in this work copy.

Read `cc-P416-stone-mining-gate.md` first. No separate P416 review was found beside it. The existing Iron Beetle uncertainty is not repeated as a new finding. Read these P416 files:

- `server/customizations/ClusterFWorkOrderSystem.cs`
- `server/customizations/CompactOreSatchelRoutingHook.cs`
- `server/customizations/GuildContractLedgerGump.cs`
- `server/customizations/MinersCompactLiaisonGump.cs`
- `server/tests/Services/StoneMiningGateVerification.cs`
- `CHANGELOG.md` and `VERSION`

Also checked `GuildResources.cs`, `LeagueRegister/LeagueRegister.cs`, `Mobiles/Normal/IronBeetle.cs`, `ClusterFMiningExtension.cs`, `server/patches/Mining.cs`, and `server/tests/Engines/Harvest/ExtendedOreStoneMiningVerification.cs`. Checked the book and gump response code against pristine ModernUO at `d4531cd94b739613155225c234900de9f47d2c88`.

## Findings

1. **risk: the shared turn-in method can pay a completed quota again.** `server/customizations/GuildContractLedgerGump.cs:562`, `:593`, `:600`. By source trace, calling `TurnIn` twice with the same completed mining entry pays standing, vouchers, and gold twice: it never checks `CompletedAt` or membership in `ActiveWorkOrders`, and quota progress remains sufficient after the first payment. Removing an entry that is already absent does not prevent the second payment. The ledger currently selects entries from the active list at `:544`, and the League Register does the same at `LeagueRegister/LeagueRegister.cs:283`, so this is a shared-method risk, not a demonstrated player exploit. The unchecked method predates P416; P416 makes quota completion require no consumable materials. Suggested fix: reject a completed entry, an entry absent from this character's active list, or a mismatched guild before checking requirements or paying. Add a regression that completes a quota, retries the same entry, and verifies that all rewards and history remain unchanged.

2. **risk: the new gold-confirmation path lacks a test for vouchers gained after its price was shown.** `server/tests/Services/StoneMiningGateVerification.cs:405`, `:437`. The sufficient-voucher case presses the old restoration button 61 and checks the price helper, while the new button 82 is exercised only with a voucher shortfall. A regression that charges gold for vouchers gained between opening the confirmation and pressing it could pass these tests; the current handler correctly reads the balance again at `MinersCompactLiaisonGump.cs:1068`. Suggested fix: open the gold confirmation with one voucher, raise the balance to at least four, then confirm through button 82 and assert that exactly four vouchers and the 1,000 base gold are taken, with no surcharge or duplicate pickaxe.

3. **nit: the legacy Ore Refinement Run and its Dull Copper payout are not covered.** `server/tests/Services/StoneMiningGateVerification.cs:315`, `:325`. The Dull Copper test stops when its mining requirement is met; the version-2 compatibility test uses only the unchanged 100-iron contract. Neither would catch a regression that asks an old Ore Refinement Run holder for Dull Copper instead of permitting the promised 150-iron turn-in, or pays the wrong rewards for the new metal. Suggested fix: exercise a version-2 `mining.ore_refinement_s` entry with 150 iron and no reported Dull Copper discovery, then separately finish a fresh Dull Copper quota. Assert consumption only on the legacy path and the defined 350 standing, 16 vouchers, and 400 gold on each completion.

## Checks with no defect found

- **Stone without the book:** no bypass found. `server/patches/Mining.cs:284` requires learned stone mining, 100 base Mining, and the stone toggle before choosing granite. New Stone Contracts are gated in `ClusterFWorkOrderSystem.cs:191` and excluded from locked discovery cards at `GuildContractLedgerGump.cs:240`. Existing held stone contracts remaining finishable is intentional.
- **Book below Journeyman:** no defect found with default settings. `MinersCompactLiaisonGump.cs:752` checks standing at purchase, not just while drawing the page; membership and the voucher payment are also checked. The configurable default is 5,000 standing and 50 vouchers. Reading uses the pinned book's 100 base Mining requirement.
- **Per-metal quota credit and pay:** no wrong-metal credit or payout found. `ClusterFWorkOrderSystem.cs:597` compares exact ore types. The iron and Dull Copper definitions at `:648` and `:759` require 100 and 50 ore, respectively, and retain their stated rewards. Only one definition per ore exists, and the ledger blocks duplicate active keys at `GuildContractLedgerGump.cs:520`.
- **Gold for vouchers already held:** no charging defect found in the current code. `MinersCompactLiaisonGump.cs:822` subtracts the current held balance from the voucher price, clamps the missing amount to zero, and charges gold only for that missing amount. `:1068` recalculates before payment; `GuildResources.TryPay` checks affordability before consuming resources.

## Verification limits

This is a source review. Existing tests were read, not rerun; no new tests, build, live connection, or client checks were performed. Runtime reproduction of the shared-method replay is unverified. The prompt specifies no lane tests. `tools/progress.py --dry-run` completed against the work copies but unexpectedly rewrote `tools/progress.json`; that generated change was restored to its original contents to keep this task notes-only. No confirmed player-facing bug was found.

P548 DONE
