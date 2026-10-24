# cc-P453: tutorial fix-up (one pet per account, bounded bandages, pests refuse outsiders, the recorded character)

## In plain words

- Each account now gets one tutorial pet: the Farmhand's dog or cat, or the graduation pick, never both. Skipping and
  then doing remedial training no longer hands out a second one. A graduation pet that has not been picked yet stays
  waiting through a closed window, a logout or a restart, and Rook offers it again.
- Only the character who started the tutorial can do it. The account's other characters see Rook's page with no
  buttons on it.
- On the farm, the Farmhand gives at most 3 stacks of 10 bandages per account, and the patch-up lesson finishes only
  when a bandage really heals someone. Players who are not in the tutorial can no longer attack the tutorial's
  creatures, so they cannot practise weapon skills on them for free.
- Nothing for you to do. The farm is still test shard only. The tutorial is not on live, so no live account has
  two tutorial pets (see "Live accounts" below).

## What changed

All server code is in `server/customizations/Tutorial/` plus the tutorial record in `server/customizations/ClusterFAccountData.cs`
(ShatteredLegacy, branch golem/Iron/P453). There are two new one-line patches. Pinned is ModernUO d4531cd.

Some of this had already moved since Crystal's check on da1a0cb. cc-P480 had added a pending companion, kept as done
keys (`graduation.petPending`, `graduation.pet`), and Rook's re-offer button. `IsParticipant` already checked
`CharacterSerial`, and `RunStation`, `CompleteStation`, `Skip` and `Graduate` all call it. What was still open is
listed below.

| # | Finding | Fix |
|---|---|---|
| 1 | P420 #3 = P421 #2: the pet marker lived in `StationsDone`, which `StartRemedial` clears | `TutorialRecord` v1 (`ClusterFAccountData.cs:1258`) adds `PetClaimed`, `PetClaimPending` and `BandagesIssued`. A v0 record takes `PetClaimed` from `farm.pet` or `graduation.pet` and `PetClaimPending` from `graduation.petPending`, then drops the two graduation keys (`:1309`). `ChoosePet` (`TutorialFarm.cs:237`) and `ChooseCompanion` (`ClusterFTutorial.cs:280`) set the claim. `StepOf` (`TutorialFarm.cs:177`) and the graduation offer (`ClusterFTutorial.cs:340`) read it. Remedial training and the Fountain of Youth reset clear `StationsDone`, but never the claim. |
| 2 | P420 #2: the pending pick was lost | It is now the record field `PetClaimPending`, which is saved. It is set when graduation earns the pick and cleared only when `GivePet` succeeds. `CompanionPending` is `PetClaimPending && !PetClaimed` (`:245`). Rook's button (cc-P480) and the login reminder both reopen the pick. |
| 3 | P420 #1: any character on the account | `IsRecordedCharacter` (`ClusterFTutorial.cs:71`) is true for the recorded serial. It is also true when the record names no character, or when the recorded one is deleted or not on this account. `StartRemedial`, `OfferCompanion`, `ChooseCompanion` and the login reminder require it, so remedial no longer moves the record to whichever character asked. Rook's page is `ReadOnly` (`TutorialGumps.cs:40`) for any other character on the account: it shows who owns the tutorial, has no buttons, and ignores a reply. |
| 4 | P420 #4 = P421 #1: endless bandages | `GiveBandages` (`TutorialFarm.cs:282`) still gives a stack only when the pack has none. Each stack it gives now counts toward `BandagesIssued`. After `clusterf.tutorialFarm.bandageIssues` stacks (default 3, so 30 bandages, at most 30 gp at a healer), the Farmhand says "That's all the bandages I can spare. The healer in town sells them." I chose a count over blessed tutorial bandages: it needs no new item type, and normal bandages behave like the ones the player will buy later. |
| 5 | P421 #4: the step completed on a skill roll | `Bandage-tutorial-real-heal.patch`: one line after `Patient.Heal` in `BandageContext.OnTick` (pinned `Bandage.cs:418`; it applies at +17 after the other bandage patches). It calls `TutorialFarm.BandageHealed`. `OnBandageHealed` (`TutorialFarm.cs:301`) completes step 3 for the healer. The `SkillEvents.SkillUsed` hook is gone. The prompt's `EndHeal` is called `OnTick` at d4531cd. |
| 6 | P421 #6: outsiders swing at pests | `Notoriety-tutorial-creature-outsiders.patch`: `NotorietyHandlers.Mobile_AllowHarmful` returns false when the target is a `TutorialCreature` and the attacker (or the pet's master) is not a participant. This runs after the staff check. Pinned `Mobile.CanBeHarmful` asks it through `Region.AllowHarmful` (`Mobile.cs:8367`, `Region.cs:802`). The `Combatant` setter then refuses the target (`Mobile.cs:737`), so there is no combat timer, swing or skill roll. Spells and pets get the same check. I patched the handler rather than wrapping `Mobile.AllowHarmfulHandler` in an `Initialize`, because `NotorietyHandlers.Initialize` sets it and the two would race. The only regions that override `AllowHarmful` are Jail, WrongDungeon (always false) and OldHavenBurrowsRegion (calls base). Every `TutorialCreature` is tutorial-only by design (the 11 Burrows creatures, the echoes and the farm pests), so this affects nothing else. |
| 7 | P421 #3: reseed with the door open | `FindDoor` (`TutorialFarm.cs:451`) looks 2 tiles around and matches a door by where it stands closed: location minus `Offset` when open. Pinned `BaseDoor.OnOpenChanged` moves it by the offset, which is +1,+1 for SouthCW. |

Both patches are listed in `docker/uo/apply-patches.sh`, after P427's, with the reason.

## Tests

`server/tests/Tutorial/TutorialFarmVerification.cs` facts 6 to 12, and three new facts in
`server/tests/Misc/TutorialVerification.cs`:

- `AFarmPetThenSkipAndRemedialGivesNoSecondPetAcrossASaveAndLoad`: after a farm dog, skip and then remedial, the save
  still has the claim, `StepOf` is 2 and `ChoosePet` gives nothing. Graduation offers no pick and `ChooseCompanion`
  gives nothing; there is one follower.
- `AClosedCompanionPickWaitsOnTheRecordAndIsClaimedOnce`: the pick is closed unchosen, then a save and load still has
  `PetClaimPending`. Rook offers it again. The fox is given, the bird is refused, and a second graduation box does not
  reopen the pick.
- `AnotherCharacterOnTheAccountChangesNothing`: the alt's page is read-only with zero buttons. A reply naming every core
  station, skip and graduate changes nothing, nor does the skip gump's "Yes. Really." or `CompleteStation`. The alt
  cannot graduate the finished core, start remedial, move the record, or open or claim a waiting companion. Once the
  trainee is deleted, the alt can start remedial and the record moves to it.
- `BandagesMovedOutOfThePackAreReissuedOnlyUpToTheCap`: the stack is banked and asked for again, five times. 3 stacks
  are given, a full pack gets none, and the count is saved.
- `AFailedTreatmentLeavesTheHealStepAndARealHealCompletesIt`: pinned's `OnTick` is run with Healing 120 and 100 slips.
  No hits are restored, the Healing roll passes, and step 3 holds. With 0 slips the bandage heals and the step completes.
  Fact 3 now heals the pet with a real bandage too (Veterinary).
- `AnOutsidersSwingAtAPestRunsNoSkillCheck`: `CanBeHarmful` is false for the outsider and true for the trainee. After
  `Combatant = pest` and 6 seconds of clock, the combatant is null, there are no skill events, and the pest is unhurt.
  The test host leaves `Mobile.AllowHarmfulHandler` null (every region allows), so this fact installs the real handler
  and restores null after it. My first green run installed it in the class fixture instead, and 16 combat facts in other
  classes failed. Scoping it to the fact fixed that.
- `ReseedingWithTheDoorOpenPlacesNoSecondDoor`: the door is opened, so it stands aside. The reseed places 0 doors and
  finds 5 pieces present, there is one door within 3 tiles, and it is the same door.
- `ThePenAndThePestsAreReplacedAfterADeathAndATaming` (P421 #8): the pest spawner starts with 3 and the pen with 4. One
  pest is killed and one pen animal tamed. After 4 minutes both are full again with new creatures. The prompt also lists
  a save/load and reseed of the farm objects; I covered the reseed (facts 1 and 11) but not a world save/load of the
  spawners.
- `TheTutorialRecordRoundTripsWithATrailingSentinel` (Skipped, Remedial, Graduated; P420 #5): every field round trips,
  and the reader ends exactly at the sentinel the writer wrote after it.
- `AVersionZeroRecordLoadsItsPetFromTheOldKeys` (4 cases): a hand-written v0 record, followed by a sentinel.

**Red first.** I ran `docker/uo/build.sh -t sl-modernuo:cc-P453` under the `docker-build` lock (taken, then released).
Free memory was 9.8 GB before the first run. Before the last run it was 1.8 GB, and 5.6 GB after I dropped the Docker
VM's page cache. The new facts need the new record fields to compile, so "red" means the fixed code with mutants that
put each old behaviour back. I saved pristine copies first and restored them after each red run.

- Green run 1: every tutorial fact passed, and 16 facts in other classes failed (the handler above). Fixed.
- Red run 1 (`--tests-only`, eight mutants: v0 save with no migration, any character is the recorded one, the pet as a
  done key, no bandage cap, the heal step on a skill roll, the outsider check off, the door matched by its tile, slow
  spawners). **Exactly 14 failed, 2,302 passed, 4 skipped**, all new facts. Each one's failure:
  - pending pick: `PetClaimPending` not saved
  - alt: page not read-only
  - outsider: `CanBeHarmful` true
  - door: 1 door placed, 4 present
  - pen: 2 pests, expected 3
  - round trip: `(False, False, 0)`, expected `(True, False, 2)`
  - v0 farm.pet, graduation.pet and petPending cases: wrong flags (the core.movement case expects no pet either way, so
    it passed)
  - first save after the farm pet: claim lost

  The bandage and heal facts stopped at step 1 instead, because the pet mutant moved them back.
- Red run 2 (`--tests-only`, three mutants: remedial forgets the claim, no bandage cap, the heal step on a skill roll).
  **Exactly 3 failed, 2,313 passed.**
  - bandages: 5 banked, expected 3
  - heal: step 4 after the failed treatment, expected 3
  - remedial: the claim was gone from the save
- Green run 2: **2,320 tests, 2,316 passed, 0 failed, 4 skipped**, and the image `sl-modernuo:cc-P453` was built. No
  `MUTANT` text is left in either tree.

`CHANGELOG.md` (2026.10.24.11, six Fixed lines) and `VERSION` were edited after the last red run. They are not code.

## Live accounts with two pets

The prompt asks how many live accounts already took two pets, if the tutorial is live. It is not. `ClusterFTutorial.Configure` enables the
tutorial only when `testCenter.enable` is true. That setting defaults to false (`GetSetting("testCenter.enable", false)`).
Live's `modernuo.json` leaves it off: `TestCenterLiveGuard`'s header says only a hand edit of that file could turn it
on, and the guard logs an error if it is ever on at the live port 2593. The compose files do not set it. The farm seeder also refuses off the
test shard unless `clusterf.tutorialFarm.allowLive` is set. So no live character can have reached `ChoosePet` or the
graduation pick, and the count is 0 by construction. I did not read the live save or Haven to check (standing rule 1),
so that count is unverified against the data. On the test shard, an old two-pet account keeps its pets. Its v0 record
loads with `PetClaimed` set, so it gets no third.

## Not done here

- The pen stays stock animals, open to visitors (Chase 10-22). Whether the pen must hold one of each species
  (P421 #7) is still Chase's decision. Nothing changed.
- The Fountain of Youth's tutorial reset (`FountainOfYouth.cs:480`) clears stations, state and character, but not the
  pet claim or the bandage count. I think that is right for "one pet per account". If Chase wants a Fountain reset to
  allow a new tutorial pet, that is one line there.

P453 DONE
