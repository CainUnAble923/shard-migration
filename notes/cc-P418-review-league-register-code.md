# P418: League Register code review

Reviewed October 22, 2026. Review only; no code or tests changed. Code snapshot: `da1a0cb`; notes snapshot before this review: `241feef`. P280's build note and `notes/wiki-drafts/league.md` were read first, after both working agreements.

This is a source review, not a runtime reproduction. No build, test suite, client session, save load, or live service was run. The P280 note's green build and deliberate test failures are its author's record, not verification repeated here. Runtime behavior and exploit reproduction remain unverified.

## Files reviewed

Paths in findings are relative to the code repository unless marked pinned.

- `server/customizations/LeagueRegister/LeagueRegisterSettings.cs`
- `server/customizations/LeagueRegister/LeagueRegister.cs`
- `server/customizations/LeagueRegister/LeagueRegisterGump.cs`
- `server/customizations/LeagueRegister/LeagueBackpack.cs`
- `server/customizations/LeagueRegister/LeagueConsolidation.cs`
- `server/customizations/LeagueRegister/LeagueRepair.cs`
- `server/customizations/ClusterFAccountData.cs`, especially `CharacterLeagueData` and account persistence
- `server/customizations/GuildContractLedgerGump.cs`, especially the extracted `TurnIn`
- `server/customizations/LeagueRegistrarGump.cs`, the Register button and response
- `server/tests/Misc/LeagueRegisterVerification.cs`
- `server/tests/Mobiles/Mule/MuleVerification.cs`, the League data compatibility test

Related code checked: `SmithGuildBook.cs`, `CompactDispatchLedger.cs`, `ProspectorsLogbook.cs`, `ForestersLogbook.cs`, `CompactOreSatchel.cs`, `ForestersLumberSatchel.cs`, `HuntersSatchel.cs`, `ArtificersSatchel.cs`, `ClusterFBackpack.cs`, `ClusterFWeightPatch.cs`, `CompactGoldHelper.cs`, `ClusterFSmithBODPayout.cs`, and the League data setup and assertions in `server/tests/Misc/AccountDataSerializerVerification.cs`. These customization filenames are under `server/customizations/`.

Pinned means the read-only `D:/UO/ModernUO-pinned` tree, verified at `d4531cd94b739613155225c234900de9f47d2c88`. Relevant pinned files were `Projects/Server/Items/Container.cs`, `Projects/Server/Items/Item.cs`, `Projects/Server/Mobiles/Mobile.cs`, `Projects/Server/Targeting/Target.cs`, `Projects/UOContent/Items/Containers/Container.cs`, and `Projects/UOContent/Multis/Houses/BaseHouse.cs`.

## Findings

1. **bug: repair targets do not recheck the deed or kit.** `server/customizations/LeagueRegister/LeagueRepair.cs:92`, `:175`, `:211`: players can pass one deed, or a kit with one charge left, between characters and open a repair target on each before anyone finishes; after the first repair deletes the source, the other callbacks still repair their targets because only the damaged equipment is checked. Pass the source item into the target callback and require it to exist, remain in that user's backpack, and have a charge before repairing and consuming it in the same callback.

2. **bug: consolidated guild satchels reject their resources.** `server/customizations/LeagueRegister/LeagueConsolidation.cs:110`: pinned `Projects/Server/Items/Container.cs:274` calls the parent container's `CheckHold` with the resource being inserted, so ore, logs, leather, and essences are rejected by the Field Satchel even when their own guild satchel accepts them, breaking normal drops and routing paths that use `TryDropItem`. Keep the satchel-only rule on direct insertion into the Field Satchel and make parent capacity checks allow resources entering its existing guild satchels.

3. **bug: populated satchels hit a four-item limit meant for satchel families.** `server/customizations/LeagueRegister/LeagueConsolidation.cs:95`, `:133`: an incoming guild satchel with four resource stacks is rejected because pinned `Projects/Server/Items/Container.cs:247` counts its contents plus the satchel itself against four, even though the Field Satchel reports its own item total as zero. Count direct satchel families separately from their resource stacks while preserving each guild satchel's limits and the intended backpack discount.

4. **bug: failed merges still spend guild currency.** `server/customizations/LeagueRegister/LeagueConsolidation.cs:136`, `:138`, `:150`: both drop handlers spend the default 50 currency before the base handler checks duplicate families, item limits, or weight, so a refused drop can take payment and leave the satchel outside. Validate first and take payment only for a successful insertion, with a refund if insertion fails after payment.

5. **bug: purchases and unbinding can leave the replacement on the ground.** `server/customizations/LeagueRegister/LeagueConsolidation.cs:55`, `:75`, `:77`, and `server/customizations/LeagueRegister/LeagueRegister.cs:196`, `:206`: payment, old-logbook deletion, or removal of a binding happens before an unchecked `AddToBackpack`, which drops the replacement at the player's feet when the pack cannot accept it, exposing unbound goods and guild books to loss or another player taking them (pinned `Projects/Server/Mobiles/Mobile.cs:7587`). Reserve delivery space or use a checked placement with rollback before committing payment and deleting originals; cover both item and weight limits, including a full pack with the old logbooks stored elsewhere.

6. **risk: the backpack item discount also bypasses other storage counts.** `server/customizations/LeagueRegister/LeagueConsolidation.cs:98`, `:100`: the Field Satchel hides its contents from every parent, including bank containers and secure house storage, whose checks read `TotalItems` (pinned `Projects/Server/Items/Container.cs:247` and `Projects/UOContent/Multis/Houses/BaseHouse.cs:719`, `:1377`), so players can store populated Field Satchels while paying for only their outer slots. Limit the discount to the character's backpack checks, or explicitly enforce real recursive counts for banking and housing if the benefit is meant only for backpacks.

7. **bug: the combined turn-in skips ready smith deeds in bags.** `server/customizations/LeagueRegister/LeagueRegister.cs:298`: only direct backpack children are scanned, so a complete deed in an ordinary bag or another Smith Guild Book is skipped even though `ClusterFSmithBODPayout.CanPay` accepts descendants of the backpack at `server/customizations/ClusterFSmithBODPayout.cs:130`. Search recursively, copy the results before deleting deeds, and test a nested complete deed beside an incomplete one.

8. **risk: Blaze repair has no per-use cost or cooldown.** `server/customizations/LeagueRegister/LeagueRegister.cs:319`, `:325` and `server/customizations/LeagueRegister/LeagueRepair.cs:40`: once the rank gate is met, every worn, carried, and banked durable item can be restored repeatedly without materials, currency, charges, skill checks, or loss of maximum durability, letting a Blaze character repair other players' tradeable gear for free too. P280 describes this as the League benefit, so confirm and document that economic policy before treating it as a defect; if free service was not intended, give the action an explicit configurable cost or cooldown and test it.

9. **risk: the satchel and repair tests miss the failing player paths.** `server/tests/Misc/LeagueRegisterVerification.cs:474`, `:475`, `:337`: the satchel test calls `Merge` followed by unchecked `DropItem`, and the repair test immediately resolves each target, leaving actual merge refusals, nested resource routing, shared pending targets, and full-pack delivery uncovered. Add regression cases through both drop handlers and through target creation followed by source transfer or deletion, plus delivery failures, and observe each new test failing before applying its fix.

10. **risk: item persistence and exact record boundaries lack coverage.** `server/tests/Misc/LeagueRegisterVerification.cs:420` tests the account subrecord but does not serialize the actual Register owner, partly used repair kit, populated Field Satchel, or upgraded backpack, and its padded buffers do not assert where the reader stops; the broader account test's `AssertSameLeague` at `server/tests/Misc/AccountDataSerializerVerification.cs:276` omits the new fields. Add item save/load cases that preserve ownership, remaining charges, contents, weight and item totals, and backpack capacity, and assert complete record consumption with nonempty older-version records followed by a sentinel.

## Checks with no finding

- **Older saves:** no incompatible version change found in `CharacterLeagueData`; `server/customizations/ClusterFAccountData.cs:737` reads the v1 mule fields only for v1 and newer, and `:743` reads the new v2 fields only for v2, with matching write order at `:754`. The existing Mule test at `server/tests/Mobiles/Mule/MuleVerification.cs:578` supplies v0 bytes, and the Register test at `server/tests/Misc/LeagueRegisterVerification.cs:436` supplies v1 bytes. The new item types start at generated version 0, so they have no earlier P280 item format to migrate. An actual saved world was not loaded.
- **Backpack upgrades:** no player-controlled weight increase or free tier purchase found under the default settings. `server/customizations/LeagueRegister/LeagueBackpack.cs:115` rechecks rank and price, saves the tier per character, and changes only `MaxItems`; the existing strength-based weight behavior remains in `server/customizations/ClusterFBackpack.cs:33`. The Field Satchel storage-count risk above is separate from the purchased backpack tiers.
- **Consolidation data:** no item duplication or discovery-record deletion found in the ordinary bind/unbind or Combined Logbook paths. Binding rejects a Smith Guild Book with contents at `server/customizations/LeagueRegister/LeagueRegister.cs:178`, and the old logbooks read account data instead of storing discoveries themselves. Replacement delivery remains vulnerable as listed above.
- **Immediate repair consumption:** the remote deed deletes itself when it repairs anything at `server/customizations/LeagueRegister/LeagueRepair.cs:255`, and ordinary deed/kit consumption is present; the defect is the missing source validation when a pending target completes.

## Verification and scope

No lane tests were requested or run, and no new tests were added. All behavior findings above come from tracing the cited source paths; runtime confirmation is still needed before claiming a demonstrated exploit or a verified fix. No Haven connection, deployment, branch change, commit, or edit under `docs/` was made.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointed at these work copies, as the working agreements request. The reporter writes `tools/progress.json` even in dry-run mode; that generated change was restored to its original bytes so this task leaves only the review note.

P418 DONE
