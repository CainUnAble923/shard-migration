# P554: League Register fixes review

Reviewed October 24, 2026. Notes only. P451 commit `21b4561` is in local code `main`, whose tip and this work copy's HEAD are `1c9c5d8`. The reviewed League files and tests have no differences from that main. Pinned ModernUO was verified at `d4531cd94b739613155225c234900de9f47d2c88`.

Read both work copies' AGENTS.md, the direction decision and task list, P451's implementation note and adjacent Codex review, and P418's earlier review. The populated Field Satchel return-to-backpack capacity finding already appears in P451's adjacent review and is excluded here.

## Finding

1. **bug: the nested Hunter's Satchel admits ordinary items through its open container.** `server/customizations/LeagueRegister/LeagueConsolidation.cs:163`, `:176`; `server/customizations/HuntersSatchel.cs:134`, `:155`. P451 passes non-satchel items through the parent capacity check, assuming the inner guild satchel already filtered them. Hunter's Satchel filters only `TryDropItem` and `OnDragDrop`; it inherits an unfiltered `OnDragDropInto`. Dropping gold, a weapon, or an ordinary bag into its open container therefore reaches the Field Satchel, passes capacity checks, and receives the backpack item-count discount. After inserting a bag, its ordinary contents can receive the discount too. The Hunter's Satchel omission predates P451, but P451 opens this path while it is consolidated. Suggested fix: enforce the Hunter's Satchel resource filter in `CheckHold`, including the parent walk from any existing child container. Add a regression through its `OnDragDropInto` while nested in a Field Satchel that rejects gold and bags, permits its intended resources, and leaves refused items and backpack totals unchanged; observe it fail before fixing it and pass afterward.

Source trace: pinned `Projects/Server/Items/Item.cs:3735` sends an open-container drop to `OnDroppedInto`, which calls the destination's `OnDragDropInto` at `:3662`. Pinned `Projects/Server/Items/Container.cs:302` calls `CheckHold` and then adds the item at `:308`, without calling either Hunter's Satchel filter. Its parent walk at `:274` reaches the new League check. `LeagueConsolidation.cs:178` cancels the incoming item count there when the Field Satchel is directly in the player's backpack. This is a source-level finding; client reproduction is unverified.

Missing coverage for this finding: `server/tests/Misc/LeagueRegisterVerification.cs:557` exercises nested ore and lumber insertion and refuses gold dropped directly on the Field Satchel at `:586`. Its Hunter's Satchel at `:603` is only inserted as an empty family member. The other Hunter's Satchel references under `server/tests/` are in `Items/SatchelIconsVerification.cs` and `Items/StarterResourcesVerification.cs`, covering icons and hide conversion, respectively. None tests this nested open-container refusal.

## Requested checks with no new finding

- **Repair deeds and kits:** no remaining reuse of a consumed field deed or exhausted kit was found. `LeagueRepair.cs:116` rechecks deletion, possession in the user's backpack, and remaining charges before repair and consumption. The pending-target regression is at `LeagueRegisterVerification.cs:390`. A Remote Repair Deed intentionally repairs multiple items once, as its tooltip and wiki specify; that is separate from a one-item field deed.
- **Blaze repair:** no repair of carried, bagged, banked, or another player's gear was found. `LeagueRegister.cs:346` calls `RepairWorn`; `LeagueRepair.cs:52` visits only the member's direct non-container items. `LeagueRegisterVerification.cs:271` checks the rank gate and those excluded locations.
- **Refused-drop fees:** no remaining charge on a refused Field Satchel insertion was found. `LeagueConsolidation.cs:243` requires insertion to succeed before spending at `:250`. The test at `LeagueRegisterVerification.cs:594` covers refusal for a duplicate/fifth family and for backpack weight, plus free repositioning inside the same Field Satchel.
- **Items at the feet:** no remaining ground fallback was found in the reviewed satchel/logbook purchases, unbinding, or Register issue paths. They use checked `PlaceInBackpack` before payment, old-item deletion, or unbinding, and delete the proposed replacement on refusal (`LeagueConsolidation.cs:52`, `LeagueRegister.cs:93`, `:218`). Pinned `Projects/Server/Mobiles/Mobile.cs:7584` confirms that this method has no ground fallback. `LeagueRegisterVerification.cs:681` covers item and weight refusal and checks the ground, currency, originals, binding, and current Register.

No additional findings in those requested repair, fee, or delivery paths. The missing Hunter's Satchel regression is included with the bug above rather than counted again as a separate risk.

## Scope and verification

Read the P451 changes in `LeagueRepair.cs`, `LeagueConsolidation.cs`, `LeagueRegister.cs`, and `server/tests/Misc/LeagueRegisterVerification.cs`, plus its changelog, version, and wiki changes. Also traced `LeagueRegisterGump.cs`, `LeagueBackpack.cs`, `ClusterFBackpack.cs`, the ore, lumber, hunter's and artificers' satchels, and the cited pinned container, item, mobile, and target paths.

No code or tests changed. No lane tests were requested or run. No build, client session, saved-world load, or live service was run; P451's recorded red and green runs were not independently repeated. No Haven connection, deployment, commit, merge, push, branch switch, or edit under `docs/` was made.

Ran `tools/progress.py --dry-run` successfully with `SL_SHARD` and `SL_MIGRATE` pointing at these work copies. Restored the reporter's generated `tools/progress.json` to its original bytes, leaving only this review note changed.

P554 DONE
