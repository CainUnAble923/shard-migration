# P434: review of recipe gating (P78)

Reviewed October 22, 2026. Notes only. No code or tests changed.

Read both work copies' AGENTS.md, the direction decision, task list, and `notes/cc-P78-recipe-gating.md`. No P78 Codex review was present beside that note. Also checked the P390 crafting review and notes and the P392 accepted-defaults summary. The already documented sparse-band access versus hint-rank discrepancy is not repeated below, and the accepted forward merge policy is not reopened.

Paths beginning with `server/` or `docker/` are relative to the code work copy. `PIN/` means `D:/UO/ModernUO-pinned/Projects/UOContent/`, verified at `d4531cd94b739613155225c234900de9f47d2c88`. PIN line numbers refer to pristine source; the cited menu methods and stock learning methods are not replaced by the current patches.

## Findings

1. **bug | `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:130`**: The exemption return runs before the own-recipe check at line 135, so Survey Saddle Roll schematics registered in Cartography (`server/customizations/Mobiles/Mule/MuleModule.cs:210`, `:281`) are always known, appear in the menu, and pass both patched craft-entry recipe checks without learning them, bypassing schematic purchase requirements while retaining ordinary skill, resource, and previous-tier requirements. Check an item's explicit recipe before exempting its system from bands, and test unknown and learned Survey Saddle Roll recipes with gating both on and off.

2. **bug | `server/customizations/Engines/Craft/ClusterFRecipeStore.cs:65`, `:147`; `PIN/Items/Skill Items/Misc/RecipeScroll.cs:79`**: A character can read a stock scroll and switch characters before opening a craft category or logging back into the learner, leaving the recipe absent from the account because login sync imports only the character logging in; stock Masonry and Glassblowing books have the same character-only learning path (`PIN/Items/Skill Items/Specialized/MasonryBook.cs:34`, `GlassblowingBook.cs:34`). Record stock learning immediately in the account store or sync the departing learner, and test actual stock item use followed directly by a character switch rather than calling `Learn` in the test.

3. **bug | `PIN/Engines/Craft/Core/CraftGump.cs:525`; `PIN/Engines/Craft/Core/CraftGumpItem.cs:72`**: A crafted category-details response (`3 + 7 * itemIndex`) opens a hidden item's name, ingredients, and skills because the handler never calls `IsKnown`, and band-locked items even show active MAKE NOW and MAKE X buttons because detail-page disabling still checks only stock recipes; Last Ten also draws newly locked history entries without filtering (`CraftGump.cs:310`). Apply `IsKnown` to details responses, detail-page controls, and history rows while preserving original button indices, and add menu-response tests for a hidden item and history made before a table change or revocation.

4. **risk | `server/customizations/ClusterFGuildPromotion.cs:123`**: Loading a pre-v3 guild record sets `PromotedRank` to the standing rank even though none of the new recipe grants was delivered, so `Update` at line 154 skips those grants permanently, including every grant for an existing top-rank member whose account has no new books. Keep the grandfathered rank separate from the grant-delivery record, provide a one-time catch-up for unknown grants, and extend `server/tests/Engines/Craft/RecipeGatingVerification.cs:608` to check inventory after promotion update rather than only the seeded rank values.

5. **risk | `server/customizations/ClusterFGuildPromotion.cs:184`, `:197`**: Without reading anything between promotions, a single update through ranks 1 to 4 grants the same tradeable Fletching Band IV book at every rank because each raw rank merges to IV and the duplicate check at line 191 checks learned knowledge rather than earlier deliveries. Preserve forward merging but record distinct merged keys already granted to that character, and test a multi-rank jump plus later updates with the first book left unread or moved to another container.

6. **bug | `server/customizations/Engines/Craft/ClusterFRecipeStore.cs:105`, `:155`**: Account-wide `revoke` or `forgetall` removes a stock recipe or system-book flag only from the targeted character, so a second character previously populated by `Sync` restores the supposedly revoked knowledge to the account on its next login. Clear the mirrored knowledge on all characters of that account or persist revocations that sync respects, and test learn, sync to an alt, revoke on the first character, then sync the alt.

7. **risk | `server/tests/Engines/Craft/RecipeGatingVerification.cs:467`; `server/customizations/Engines/Craft/RecipeItems.cs:110`**: The scroll shop test stops after finding the purchased `AccountRecipeScroll`, while the consumption/refusal test at line 284 exercises only `PatternBook`, leaving the scroll's own key, consumption, duplicate refusal, cross-character use, and serialization path without a lifecycle test. Add tests that use and round-trip an actual account scroll, verify one unknown copy is consumed and a known copy is retained, and verify another character can use the learned recipe without consuming another scroll.

## Evidence and limits

The findings above are source traces, not runtime reproductions. No server, Docker build, client session, or test suite was run, and no claim of a passing runtime test is made. No new test was added, so no red/green test cycle applies. The P78 note already identifies its missing direct `CraftItem.Craft` enforcement test; that known coverage gap is not raised again as a new finding.

For finding 1, `Classify` returns `Exempt` for Cartography and `IsKnown` returns true through its default branch at line 277. `server/patches/CraftGump-recipe-gating.patch:74` and `:84` replace both original recipe checks with that result. The Survey Saddle Roll registrations explicitly call `AddQuestRecipe`; `PIN/Engines/Craft/DefCartography.cs:27` checks tool access, not schematic knowledge. `server/tests/Mobiles/Mule/MuleModuleVerification.cs:136` verifies recipe registration but does not check unknown-recipe refusal, and the P78 repeated-schematic test at `RecipeGatingVerification.cs:514` selects only the first tier-one entry rather than checking each craft system.

For finding 3, `CraftGump` and `CraftGumpItem` derive from `DynamicGump`. The incoming response handler in `PIN/Gumps/Base/GumpSystem.IncomingPackets.cs:55` checks that buttons exist only for the separate `Gump` class, so its button validation does not prevent the hidden-details request. The current craft patches do not add an `IsKnown` check to those handlers. For band-gated systems, the later craft check still refuses crafting; the details leak alone does not establish a craft bypass.

For finding 5, the current Fletching raw book entries in `PIN/Engines/Craft/DefBowFletching.cs` are FukiyaDarts in band I, Crossbow and CompositeBow in II, and HeavyCrossbow, RepeatingCrossbow, and Yumi in III. Each raw band is below `MergeBelow = 5`, so `MergedBand` at `ClusterFRecipeGate.cs:204` leads to IV throughout. The current lumber extension changes subresources, and mule registrations add own-recipe entries excluded from the book counts. `Update` does iterate every intermediate rank at `ClusterFGuildPromotion.cs:160`; no skipped-rank loop defect was found for newly tracked members.

No direct item-duplication path was found in custom scroll use: `RecipeItemHues.Use` checks backpack ownership, calls `Learn`, and synchronously deletes a newly learned item at `RecipeItems.cs:47`, with no intervening timer or target. Known copies are intentionally retained, and paid repeat purchases of unread tradeable scrolls are not duplication. Finding 5 concerns repeated free book awards, not a proven scroll duplication exploit.

Implementation and integration reviewed:

- `server/customizations/Engines/Craft/ClusterFRecipeGate.cs`
- `server/customizations/Engines/Craft/ClusterFRecipeStore.cs`
- `server/customizations/Engines/Craft/ClusterFRecipeTable.cs`
- `server/customizations/Engines/Craft/RecipeItems.cs`
- `server/customizations/Engines/Craft/GuildRecipeShopGump.cs`
- `server/customizations/Engines/Craft/ClusterFRecipeRewards.cs`
- Recipe and promotion serialization in `server/customizations/ClusterFAccountData.cs`
- `server/customizations/ClusterFGuildPromotion.cs` and the relevant join, task, rank, hall, and shop paths in `ClusterFGuildSystem.cs`
- `server/customizations/Mobiles/Mule/MuleModule.cs` and the schematic paths in `MuleModuleGumps.cs`
- Reward call sites in `server/customizations/ClusterFSmithBODPayout.cs` and `ClusterFSmithCommissions.cs`
- The craft patch registration in `docker/uo/apply-patches.sh`, `CraftGump-recipe-gating.patch`, and the existing craft menu, detail, context, and item patches
- Pristine craft menu, item, context, Cartography, Fletching, stock scroll, system-book, and incoming gump response source cited above

Tests read for relevant assertions and gaps:

- `server/tests/Engines/Craft/RecipeGatingVerification.cs`
- `server/tests/Mobiles/Mule/MuleModuleVerification.cs`
- Relevant serializer assertions in `server/tests/Misc/AccountDataSerializerVerification.cs` and `RegularSmithBODVerification.cs`
- P78's gating-off setup in `server/tests/Engines/Craft/MakeXRepeatVerification.cs`, `CraftXVerification.cs`, and `HammerFamiliarityVerification.cs`

`python tools/progress.py --dry-run` completed with exit code 0 using both work-copy path overrides. Despite the option's documented behavior, it rewrote `tools/progress.json` inside `build()` before checking dry-run mode; that incidental generated change was restored byte-for-byte from HEAD, which was clean at the initial status check. Final scope is only this requested notes file. STOP-REQUESTED was checked between review steps and was absent. No Haven connection, deployment, account change, commit, merge, push, or branch switch was made.

P434 DONE
