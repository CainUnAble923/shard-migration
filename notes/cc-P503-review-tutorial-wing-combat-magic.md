# P503: review of the tutorial combat and magic wing trials

Reviewed 2026-10-23. P290 is merged in local code `main` at
`579ad58f8f478280b03b8cf80f1ee9a5b3001a27`; this work copy's HEAD is the same commit.
The trial and test files match `main`.

Read `cc-P290-tutorial-wing-trials-combat-magic.md` and its coverage limits before
reviewing the code. No separate P290 review was found beside it. The findings below
do not repeat its fixed notoriety problems, self-bandage regeneration caveat, or
unplayed weapon choices.

Code paths below are relative to the code repo. `P/` means
`D:/UO/ModernUO-pinned/Projects/`, verified at
`d4531cd94b739613155225c234900de9f47d2c88` with a clean working tree.

## Findings

1. **bug** | `server/customizations/Tutorial/TutorialWingTrials.cs:349`, `:410`, `:468`: Splitting a loaned reagent, bandage, or arrow stack creates a new remainder that is absent from `trial.Loaners`, so that remainder can be kept, banked, or traded after Stop, Reset, logout, or leaving the yard, until the next server startup sweep. Track split descendants with their loan or prevent splitting loan stacks, and test reclaiming both halves after cancellation and transfer.

2. **bug** | `server/customizations/Tutorial/TutorialWingTrials.cs:332`, `:407`: Under SE or later rules, missed shots with the loaned arrows enter normal ammunition recovery, which creates ordinary arrows outside the loan list, so repeating Archery and then leaving war mode produces arrows the player can keep or sell to a provisioner. Preserve loan identity through ammunition consumption and recovery, or exclude loan ammunition from recovery, and test a miss followed by Stop and recovery.

3. **bug** | `server/customizations/Tutorial/TutorialWingTrials.cs:248`, `:415`, `:445`: If a world save occurs during Chivalry and the server restarts before the trial returns its loan, the extra tithing points survive in the mobile save while the in-memory loan record disappears, so the player keeps the unspent points and can borrow another 100. Persist and reconcile the outstanding tithing loan on load, and test saving and reloading an unfinished trial without changing the player's original balance.

4. **bug** | `server/customizations/Tutorial/TutorialWingTrials.cs:543`, `:555`, `:730`: The weapons trial counts any damage while the selected weapon skill is equipped, and the Bushido and Ninjitsu trials count any damage while a move is readied, so delayed spell damage can finish these lessons without the required weapon hit or move landing. Record a validated weapon or move hit with its actual weapon and target instead of inferring it from `OnDamage`, and add negative cases for spell damage while the weapon or move is ready.

5. **bug** | `server/customizations/Tutorial/TutorialWingTrials.cs:514`, `:559`, `:573`: A successful school skill roll only sets a timestamp, so Magery can pass after casting Heal on yourself and punching the echo, and Chivalry can pass after Close Wounds on yourself followed by a Magery heal on the villager within ten seconds. Tie completion to the required spell's actual effect on that trial's target, and test a successful cast on a different target followed by unrelated damage or healing.

6. **bug** | `server/customizations/Tutorial/TutorialWingTrials.cs:577`, `:743`: The villager half of the bandage lesson accepts any heal from its trainee when no bandage context exists, so a Magery Heal can satisfy it without bandaging the villager. Record successful bandage completion for that healer and patient, and test that a spell heal leaves `PatientHealed` false.

7. **bug** | `server/customizations/Tutorial/TutorialWingTrials.cs:223`, `:345`: When the backpack cannot accept a book, weapon, or reagents, `Lend` silently deletes the rejected supply while the trial remains armed and tells the player to use it, leaving a new player unable to continue until they make room and reset. Make lending report failure, return all partial loans, and explain how to retry; test both a full backpack and failure partway through a multi-item loan.

8. **risk** | `server/tests/Tutorial/TutorialWingTrialVerification.cs:130`, `:173`, `:176`, `:208`, `:248`: The completion tests inject damage and skill callbacks, invoke `SelfHealed` directly, and accept a plain `villager.Heal`, so they can pass while the actual required action is missing or its observation is broken. Keep these small tests, but add tests through real weapon, spell, and bandage execution that reject the wrong action and exercise both bandage orders through the timer.

## Source checks behind the findings

- Split stacks: `P/Server/Mobiles/Mobile.cs:5133` calls `LiftItemDupe` on a partial lift;
  `:5240`, `:5265`, and `:5269` create a separate remainder and copy its loan name.
  The trial tracks only the original object; `TutorialWingTrials.cs:119` sweeps
  names only at startup. This is retention until restart, not permanent retention
  of named loaners across restart. `P/Server/Items/Item.cs:2474` also prevents
  normal unnamed supplies from stacking with a named loaner, so ordinary stacking
  into the player's own reagents is not the reported issue.
- Recovered arrows: `P/UOContent/Items/Weapons/Ranged/BaseRanged.cs:175` consumes
  ammunition by type, and `:145` banks missed ammunition by type, without its name
  or loan identity. `AmmoRecovery.cs:116`, `:128`, and `:145` create and deliver a
  fresh ordinary stack after the player leaves war mode. This path requires
  `Core.SE`; live expansion settings were not inspected.
  `TutorialWingTrials.cs:407` neither tracks these new items nor cancels recovery.
  `P/UOContent/Mobiles/Vendors/SBInfo/SBProvisioner.cs:114` buys arrows.
- Tithing: `P/Server/Mobiles/Mobile.cs:2378` writes tithing points and `:6240`
  reads them. `TutorialWingTrials.cs:99` stores active trials only in a static
  dictionary; startup sweeps items, and login can cancel only a trial still in
  that dictionary. The tithing test at `TutorialWingTrialVerification.cs:215`
  covers normal completion only.
- Damage evidence: `P/UOContent/Spells/First/MagicArrow.cs:24` makes Magic Arrow
  delayed, and `:65` sends its damage through `SpellHelper`, which eventually
  reaches the same mobile damage callback as a weapon. The callback passed to
  the trials contains neither a spell nor a weapon identity. Readying a move
  does not establish that the later damage came from that move.
- Healing evidence: `P/UOContent/Spells/First/Heal.cs:67` uses `SpellHelper.Heal`,
  and `P/UOContent/Spells/Base/SpellHelper.cs:1047` calls `target.Heal`.
  `P/Server/Mobiles/Mobile.cs:6135` calls `OnHeal` without any bandage identity.
  `P/UOContent/Items/Skill Items/Misc/Bandage.cs:197` removes the bandage context
  before the eventual heal at `:418`, so absence of a context cannot distinguish
  a completed bandage from a spell heal. The yard's beneficial exception at
  `TutorialWingTrials.cs:680` allows the owner's beneficial acts generally.
- Missing supplies: `P/Server/Mobiles/Mobile.cs:7587` reports a failed backpack
  placement; the wing's `Lend` deletes that item and does not report the failure
  to `Arm`. The core trial already handles this situation with cancellation and
  a make-room message at `TutorialCoreTrials.cs:125`.

## Rewards, scope, and verification limits

No repeatable graduation reward was found through wing completion or Reset:
`ClusterFTutorial.cs:161` records station completion once, `:281` requires an
active participant to graduate, and `:293` changes that state before rewards.
Loan replenishment is intentional; the escaped arrows and saved tithing above
are the repeatable value paths found in this review. Original blessed loaners
cannot be sold directly to ordinary NPC vendors because
`P/UOContent/Mobiles/Vendors/BaseVendor.cs:464` requires standard loot and
`P/Server/Items/Item.cs:4433` excludes blessed items.

Reviewed the full `TutorialWingTrials.cs` and
`TutorialWingTrialVerification.cs`, plus the relevant tutorial framework,
creature, core trial, and pinned server paths cited above. Checked the shard
patches and loan references for another reclaim hook. No code, test, or files
under `docs/` changed. No build, test shard, client, Docker daemon, or Haven
connection was used. These are source review findings; reproduction in a
running shard and the proposed fixes are unverified. No new tests were added
or run, as this prompt has no lane tests.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` set to these
work copies; it exited 0 but rewrote `tools/progress.json` despite that option.
Restored that generated file to its initially clean state, leaving only this
requested note changed.

P503 DONE
