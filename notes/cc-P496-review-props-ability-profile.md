# P496: review of the props ability profile (P233)

Reviewed 2026-10-23. Notes only; no code changes.

P233 is in main: implementation commit `b5ac1f6c83452a6b35ce2827b5d3947599a34de5` is an ancestor of main, merged by `0e9e61f`. Reviewed the work copy at `579ad58`; its P233 customization and test match main.

Read `cc-P233-props-ability-profile.md` and the earlier P233 review summaries in `cc-P158-codex-second-agent.md`. Their findings are not repeated here.

## Finding

- **risk**, `server/tests/Services/PetTraining/PropsAbilityProfileVerification.cs:255`: The TrainingProfile test presses the arrow only when the profile is null, so it cannot catch a failure to open an existing training profile or show that pet's training values, behavior promised in P233's notes. Add a case with a stored TrainingProfile and distinct training values, press the real props arrow, and assert that the opened object is that same profile and its displayed rows contain those values without changing the record.

## Review result and evidence

No incorrect stat reads or value differences from P233's notes were found in the reviewed props path. The finding above is missing coverage, not a reproduced runtime defect.

- `server/customizations/Services/Pet Training/BaseCreature.PetTraining.cs:34` and `:65` enable navigation with `canModify: true`; the getters still return the creature's ability profile and existing training profile, respectively.
- Pinned ModernUO `Projects/UOContent/Gumps/Props/PropsGump.cs:141`, `:210`, and `:316` confirm the arrow, permission check, and nested property-object routing described in P233. Its `:320` null branch returns to the creature page, explaining why the current TrainingProfile test does not exercise opening a profile.
- `server/customizations/Services/Pet Training/AbilityProfile.cs:51`, `:63`, and `:83` expose the combined magical abilities, ability names, and stored regeneration bonuses. `TrainingProfile.cs:51` and `:54` through `:63` derive progress and slot values from that profile's creature and training state.
- `AbilityProfileStore.cs:81` excludes empty profiles from saves; `PetTrainingStore.cs:92` leaves the training profile absent when called with `create: false`.
- Read all of `PropsAbilityProfileVerification.cs`, plus the relevant natural-ability, regeneration, and persistence tests in `PetAbilityCoreVerification.cs` and the training and persistence tests in `PetTrainingVerification.cs`. Those existing subsystem tests do not drive the props arrow into a non-null TrainingProfile.
- Read P233's changelog entry and VERSION. The later version numbers are expected; P233 explicitly allowed merge renumbering.

## Verification and limits

Source review against the read-only pinned ModernUO tree at `d4531cd94b739613155225c234900de9f47d2c88`. No new tests were written, and no tests or builds were run for this notes-only task; client rendering and runtime behavior remain unverified in this review. No Haven connection or deployment was made.

Ran `python tools/progress.py --dry-run` successfully with both work-copy path overrides. Its build function still writes `tools/progress.json` before checking the dry-run flag; restored that generated change to its initially clean state so this review delivers only this note.

P496 DONE
