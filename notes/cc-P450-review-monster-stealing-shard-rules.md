# P450: Review of P142 monster stealing rules

Reviewed 2026-10-22. Notes only; no code changes.

Read `cc-P142-monster-stealing-shard-rules.md` and the relevant P127 port notes. No earlier P142 Codex review was found beside them. The known unwired damage sites and the outstanding restart check are not repeated here.

## Findings

1. **bug**, `server/patches/Stealing-monster-stealing.patch:9`: The unconditional hook still rolls monster loot and skill gain after `TryStealItem` rejects the attempt, such as when a thief equips a weapon after opening the cursor or has Young status (`D:/UO/ModernUO-pinned/Projects/UOContent/Skills/Stealing.cs:99`, `:107`); `StealingHandler.HandleSteal` repeats neither check. Apply shared attempt eligibility before both stealing paths and add a regression through `Target.Invoke`, while keeping the special reward independent of whether an ordinary pack item was successfully stolen.

2. **bug**, `server/customizations/Services/Monster Stealing/Core/ThievesDenStealRules.cs:207`: A Master targeting a boss on open land gets `NotHere`, contrary to P142's headline 2 and ladder promising bosses anywhere, because the place gate returns before checking the boss and `RequiredRank(None, true)` also remains `int.MaxValue` at line 162. Treat a boss outside the listed regions as a covered target requiring Master, preserve the never list, and test both an Initiate's refusal and a Master's legal attempt there; the existing boss tests only place bosses inside covered dungeons.

3. **risk**, `server/tests/Services/Monster Stealing/MonsterStealingVerification.cs:387` and `server/tests/Services/Monster Stealing/MonsterStealingShardRulesVerification.cs:694`: The gem test substitutes a ghost body and calls `Offer` directly, and the one-success test never kills either participant, leaving actual item retention, the death event, and duplicate rewards on death untested. Add death-path coverage for a stolen gem staying in the thief's backpack and producing its offer, protected pack items resisting ordinary theft, and a stolen-from monster's corpse receiving no second copy of the awarded special item.

## Protection and duplication checks

No missing blessed or newbied flag was found in the reviewed items. `Items/GemOfSalvation.cs:29` explicitly sets Blessed, matching ServUO, and pinned `Skills/Stealing.cs:222` rejects Newbied and blessed pack items before moving them. Recipe scrolls are explicitly ordinary tradeable items in `server/customizations/Engines/Craft/RecipeItems.cs:1`; P142 supplies no requirement to bless its new components or crafted equipment.

No unintended duplication on death was found by source inspection. Special and minor rewards are newly constructed and delivered to the thief rather than also inserted into the monster's pack. `StealLootTables.TryFamilyPart` intentionally creates an extra family part while leaving the original available as ordinary loot, as P142's loot table specifies. The Burrow Mother and Gloom Queen create their separate boss parts on death, rather than recreating an awarded monster-stealing special.

## Evidence and limits

Reviewed these canonical files listed by P142:

- `server/customizations/Services/Monster Stealing/Core/StealingHandler.cs`
- `server/customizations/Services/Monster Stealing/Core/ThievesDenStealRules.cs`
- `server/customizations/Services/Monster Stealing/Core/StealLootTables.cs`
- `server/customizations/Services/Monster Stealing/Core/MonsterStealingStore.cs`
- `server/customizations/Services/Monster Stealing/Items/StolenComponents.cs`
- `server/customizations/Services/Monster Stealing/Items/ThievesDenRecipeItems.cs`
- `server/customizations/Services/Monster Stealing/Items/GemOfSalvation.cs`
- `server/customizations/Engines/Craft/ThievesDenCraftRegistrations.cs`
- `server/customizations/Engines/Craft/ClusterFRecipeTable.cs`
- `server/customizations/Engines/Craft/ClusterFRecipeRewards.cs`
- `server/customizations/Services/Pet Training/SpecialAbility.cs` (Life Drain)
- `server/tests/Services/Monster Stealing/MonsterStealingShardRulesVerification.cs`
- `server/tests/Services/Monster Stealing/MonsterStealingVerification.cs`

Also traced the stealing hook and companion stealing patches; guild membership and rank helpers; skill-gain wrappers; loot-box boss classification; recipe and fragment constructors; Burrows family and boss loot; and pinned Stealing, Target, and Item death handling. The read-only ModernUO reference was verified at `d4531cd94b739613155225c234900de9f47d2c88`. Later Exodus additions were accounted for: their explicit open-land exception does not extend to other bosses.

Finding 1 is inherited from the P127 hook and ServUO's independent bonus roll, rather than introduced by P142. Finding 2 is in our rank and place rules. Finding 3 is a gap in our tests.

This was a source review. No build, test, client session, save reload, or death scenario was run, so runtime reproduction remains unverified. No tests were added. Haven was not contacted. The progress reporter completed in dry-run mode with file writes suppressed to keep this task limited to its review note.

P450 DONE
