# P523: review of the tutorial trades wing (P291)

Reviewed 2026-10-24. Docs only. No code or tests changed.

P291 is in main: code commit `aa6fce4`, merge `bd95351`. This work copy and main both point to `f2853e86ca96c89d8f97a6c3a17c9fd2661ad41d`; the tutorial code and tests have no diff against main.

Read P291's implementation note and `cc-P291-tutorial-wing-trials-trades-and-more-codex-review.md` first. The findings below are additional to that review and the implementation note's already disclosed behavior.

## Findings

### 1. Bug: split and converted materials escape the loan return

Locations: `server/customizations/Tutorial/TutorialTradeTrials.cs:346`, `:371`; `server/customizations/Tutorial/TutorialWingTrials.cs:362`, `:427`, `:486`.

Loans are ordinary stock items, tracked only by their original object references. Splitting a loaned stack creates an untracked remainder that survives finishing, stopping, resetting, and leaving the yard. For example, lifting one of the eight loaned cloth leaves seven cloth in a new stack that Return never visits. That stack still carries the loaner name and is swept on a server restart, but nothing takes it back during normal play.

Conversion also escapes cleanup and removes that eventual protection. Cut the loaned cloth with the player's own scissors to obtain eight ordinary bandages, or axe the five loaned fletching logs into ordinary boards, then stop or reset. The original materials are consumed, while the replacement items have neither tracked references nor the loaner name, so they survive leaving and the startup sweep. This can be repeated without making the lesson's intended product. It is separate from the already disclosed ability to keep a finished lesson's product.

Engine evidence at pinned commit `d4531cd94b739613155225c234900de9f47d2c88`:

- `Projects/Server/Mobiles/Mobile.cs:5133` calls `LiftItemDupe`; `:5235` creates a new remainder, copying the name and loot type but registering no tutorial ownership.
- `Projects/UOContent/Items/Resources/Tailor/Cloth.cs:40` converts cloth to bandages.
- `Projects/UOContent/Items/Skill Items/Lumberjack/Log.cs:41` and `:92` convert logs to boards through `ScissorHelper`.
- `Projects/Server/Items/Item.cs:4371` consumes the source and places the new item without copying its name. The tutorial's `SweepLoaners` at `TutorialWingTrials.cs:135` recognizes names, not the origin of these replacements.

Suggested fix: carry loan ownership through splits and conversions, or prevent these operations on borrowed supplies while allowing the intended craft result. Add regression coverage for a split remainder and a converted material after Stop, Reset, leaving, and restart cleanup; the existing return assertions only retain references to the originally lent items.

### 2. Bug: picking up an existing product completes a crafting lesson

Location: `server/customizations/Tutorial/TutorialTradeTrials.cs:538`.

The only evidence for the `made` step is a higher backpack count than at arming. A player can drop an existing skullcap before starting Tailoring, pick it back up once the lesson arms, and receive completion without using Tailoring, the sewing kit, or the cloth. The same bypass applies to the other listed products; Blacksmithy, Tinkering, and Alchemy still require their additional skill roll, but never require their crafting skill to be used.

The current test explicitly supplies this false evidence: `server/tests/Tutorial/TutorialTradeTrialVerification.cs:203` constructs an item and adds it to the backpack, then expects completion. `ProductsAlreadyInTheBackpackDoNotCount` at `:219` covers the initial count but not an old item brought back after arming.

Suggested fix: record a successful craft of the required product by this player after the trial arms, then award the step from that evidence. Test that picking up, receiving, or retrieving an existing product grants no credit, and that the real craft path does.

### 3. Bug: passive skill checks count as the instructed hands-on action

Location: `server/customizations/Tutorial/TutorialTradeTrials.cs:575`.

`TradeSkillUsed` accepts every successful check of a named skill, with no action or target information. During Lumberjacking, a successful passive Lumberjacking roll from an axe hit counts as chopping the practice tree and ends the lesson even though no wood was harvested. The player can remain within the lesson's 14-tile reach while attacking a target near the adjacent training yard. This is a different failure from the earlier review's Fishing catch issue.

Blacksmithy's separate instruction to use Arms Lore on the dagger has the same problem: an exceptional weapon craft can passively roll Arms Lore and satisfy that step before the player studies anything. Pinned `Projects/UOContent/Items/Weapons/BaseWeapon.cs:2532` supplies the combat Lumberjacking check, and `:684` supplies the exceptional-craft Arms Lore check. `Projects/UOContent/Skills/SkillCheck.cs:52` publishes location checks through the same `SkillUsed` event. The local `BaseWeapon-arms-lore.patch` preserves the passive crafting check.

Suggested fix: require evidence from the requested action and, where appropriate, the trial's actual object, rather than a generic skill roll. Add negative tests for combat Lumberjacking and passive craft Arms Lore; the current gathering test at `server/tests/Tutorial/TutorialTradeTrialVerification.cs:164` injects a generic successful event, and cannot distinguish these actions.

### 4. Risk: another player can take the lesson's goat and block its trainee

Location: `server/customizations/Tutorial/TutorialTradeTrials.cs:629`, with creation at `:404`.

`TutorialFarmGoat` is a normal tameable Goat with a `TrialOwner` property that no access check reads. A nearby player can tame it before its trainee does, leaving the trainee unable to perform the taming step on that goat. The trial remains armed and does not replace a goat controlled by somebody else; the trainee must reset and repeat the lesson. This is separate from the earlier placement conflict finding.

Pinned `Projects/UOContent/Skills/AnimalTaming.cs:136` refuses already controlled animals and `:443` assigns the successful tamer as master. Neither that path nor the shard's AnimalTaming patches enforce `TrialOwner`. The current animal test at `server/tests/Tutorial/TutorialTradeTrialVerification.cs:245` injects success and assigns ownership directly at `:248`, so it never exercises competing tamers.

Suggested fix: enforce the trial owner's exclusive right to tame the practice goat and recover clearly if it becomes unavailable. Add a two-player test in which an outsider attempts to tame the goat and the intended trainee can still complete the lesson.

## Rewards and coverage

I found no additional repeated graduation-box or starter-pet reward path introduced by P291. `ClusterFTutorial.CompleteStation` at `:160` records each station once, and `Graduate` at `:281` requires an active tutorial before changing its state and giving graduation rewards. The previously documented replay products and alternate Farmhand completion of Animals are not repeated as new findings here. The material escape in finding 1 is an additional repeatable source of items.

Reviewed the P291 file list:

- `server/customizations/Tutorial/TutorialTradeTrials.cs`
- `server/customizations/Tutorial/TutorialWingTrials.cs`
- `server/customizations/Tutorial/TutorialFarm.cs`
- `server/customizations/Tutorial/ClusterFTutorial.cs`
- `server/customizations/Tutorial/TutorialCoreTrials.cs`
- `server/customizations/Tutorial/TutorialGumps.cs`
- `server/tests/Tutorial/TutorialTradeTrialVerification.cs`
- P291's changes and relevant facts in `server/tests/Tutorial/TutorialFarmVerification.cs` and `server/tests/Tutorial/TutorialFirstPlayVerification.cs`
- P291's `CHANGELOG.md` and `VERSION` changes

Also checked the shared loan tests in `TutorialWingTrialVerification.cs`, `TutorialCreature.cs`, the relevant pinned engine implementations, and the local patches affecting those paths.

Validation limits: this was source review only. No new tests, builds, Docker operations, client sessions, account changes, or Haven connections. The reported action sequences and multiplayer behavior were not reproduced in a running shard; those runtime checks remain unverified. The suggested regressions do not exist in this change.

The standing progress command was run with `--dry-run` and work-copy path overrides, and exited 0. Its implementation still writes `tools/progress.json` before checking the dry-run flag; that incidental write was restored byte-for-byte from HEAD, since the task only authorizes this review note. No progress output is treated as tutorial behavior evidence.

P523 DONE
