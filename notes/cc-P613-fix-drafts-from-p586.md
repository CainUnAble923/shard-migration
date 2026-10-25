# cc-P613: the urgent fix-up draft from P586, built

## In plain words

- **Tutorial farm bandages:** when your backpack is too full (by item count or by weight), or you have no pack, the Farmhand now asks you to make room, and the gift does not count against your account's three. Before, the bandages fell on the ground and used up one of the three.
- **A tutorial whose character is gone:** if the character doing an account's tutorial is deleted or moved to another account, the account's next character now carries on with it when it logs in or double-clicks Rook. Lessons, the pet already taken and the bandage count are kept. Before, the next character was stuck with a read-only page.
- The shard build with these fixes, `sl-modernuo:cc-P613`, is green: 2,472 tests pass, the usual 4 are skipped, none fail.
- For you: nothing to do. The tutorial runs only on the test shard, so this reaches players with the next test-shard deploy.

## Drafts

P586's urgent section has one draft, U1. W1-W5 are under "Other drafts", A1/A2 are additions to queued P452/P478, and C1/C2 are For Chase. None of those was built here.

| Draft | Done or skipped | Why / what |
|---|---|---|
| U1 part 1: failed bandage delivery spends nothing | Done | `TutorialFarm.GiveBandages` places the stack with `PlaceInBackpack`, with no fallback that drops it on the ground. If that fails, it deletes the stack and returns a new result, `BandageGift.NoRoom`. Wren then says "Your backpack is too full for these bandages. Make room in it, then double-click me again." `BandagesIssued` goes up only after the stack is in the pack. The cap (3), the stack size (10) and the existing-bandage check are unchanged. |
| U1 part 2: an orphaned active record is taken up | Done | New `ClusterFTutorial.AdoptOrphanedRecord`, called at login (`OnLogin`) and when the player double-clicks Rook (`TutorialRecruiter.OnDoubleClick`), never from an eligibility check. It applies when the record is InCore, InWings or Remedial and its character is gone: no serial recorded, deleted, or moved to another account (`IsRecordedCharacter`, the rule cc-P453 already uses for Rook's page). It stores the new character's serial, cancels any open trial and says one System line. It does not touch the state, lessons, start and finish times, the skip flag, `PetClaimed`, `PetClaimPending` or `BandagesIssued`. A living recorded character keeps the record, and staff never take it. After that, every participant check (lessons, farm, graduation) passes through the same `IsParticipant`. |
| W1-W5, A1, A2 | Not in scope | They are not in the urgent section. A1 and A2 add to queued P452 and P478. |
| C1, C2 | Skipped | For Chase. |

U1 was not done by a merged prompt or queued. I checked `queue\`, `waiting\`, `completed\`, `merging\` and `held\` for `BandagesIssued`, `GiveBandages` and the orphan case; the only hits were old unrelated prompts using the word "orphan". It is not wrong against today's code: `TutorialFarm.cs` and `ClusterFTutorial.cs` were as P586 described at base `6857dd2`. It does not overlap P533 U4 (vet and paid services, built by P610).

## Tests (seen failing first, then passing)

New file `server/tests/Tutorial/TutorialDeliveryRecoveryVerification.cs`, 21 cases, probed on builder image `sl-uo-builder:cc-P612` with the files bind-mounted.

- **Red on the old code: 19 of 21 failed.**
  - `ABandageThatCannotBeDeliveredSpendsNothing` (pack full by items, full by weight, no pack; each asked 5 times through `TutorialFarm.Talk`, then room made and asked again): the first case already spent the whole allowance, expected 0 and got 3.
  - All 18 cases of `AnActiveRecordWhoseCharacterIsGoneCarriesOnWithTheNextCharacter` (InCore, InWings, Remedial x no serial, deleted, other account x login, Rook): the next character never became a participant.
  - The 2 that passed are controls, which the old code already got right. `DeliveredBandagesStillStopAtTheSavedCap`: banked stacks, the cap and a save and load. `ALivingRecordedCharacterKeepsItsTutorial`: another of the account's characters gets no record and sees Rook's page read-only.
- **The recovery cases also check:**
  - After adoption, the farm talks at the right step and a core lesson finishes for the new character.
  - The adopted record survives a save and load, with a trailing sentinel read back.
  - A third character on the account then cannot take the record over, and sees Rook's page read-only.
- **Green after the fix:** 139 of 139 tutorial facts (`FullyQualifiedName~Tutorial`) in the probe.
- **Gated build:** I took the `docker-build` lock and released it afterwards. `docker\uo\build.sh -t sl-modernuo:cc-P613` finished with EXIT=0: "Built sl-modernuo:cc-P613 with patches applied and 2472 shard test(s) passing". That is 2,472 passed, 4 skipped (the real-map-data facts) and 0 failed, and all 21 new cases are among the passes. The images are `sl-modernuo:cc-P613` = `9b16466a6e4f` and `sl-uo-builder:cc-P613` = `05dc3cd70053`. The log is `build-P613.log` in the session scratchpad.

## Deviations and limits

- **The tests reach the Farmhand through `TutorialFarm.Talk`.** That is the conversation her double-click runs, and the existing farm tests use it too. They reach login through `ClusterFTutorial.OnLogin`, the login event's handler. No client was used.
- **No retry is needed for a pack full by weight.** The player makes room and asks again, as the line says. Nothing is held for them.
- **CHANGELOG:** version `2026.10.25.6`, because this base already uses `.5` from P610. P611's unmerged branch also used `.5`, which is a separate matter for the integrator when that branch merges. `VERSION` is bumped to match.
- **The corrected guide wording for P478 was not written.** The draft says to hand it over "after behavior is verified", meaning on the test shard. A guide could now say: if your backpack is full, Wren keeps your bandages for you; and a new character on the account carries on with a tutorial whose character was deleted.

## Files

ShatteredLegacy (branch golem/Iron/P613, base `6857dd2`):
- `server/customizations/Tutorial/TutorialFarm.cs`
- `server/customizations/Tutorial/ClusterFTutorial.cs`
- `server/customizations/Tutorial/TutorialRecruiter.cs`
- `server/tests/Tutorial/TutorialDeliveryRecoveryVerification.cs` (new)
- `CHANGELOG.md`, `VERSION`

No Haven connection, deployment, real account action, `docs\` edit, commit, merge, push or branch switch.

P613 DONE
