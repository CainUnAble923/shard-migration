# P420: review of the new player tutorial framework

Reviewed 2026-10-22. Code HEAD: `da1a0cb`; notes HEAD before this file: `0636306`.
This is a source review only. No code or tests were changed, and no build, test server, client session, or Haven connection was used. Runtime reproduction and actual save/restart behavior are unverified.

Read both work copies' `AGENTS.md`, the direction decision and task list, `notes/cc-P80-new-player-tutorial.md`, the farm implementation note, and the P371 implementation's Codex review. No separate P80 Codex review was found beside its note. The findings below concern the current canonical source, including the farm and graduation integration added after P80.

Code paths below are relative to the ShatteredLegacy work copy. Severity uses the requested labels: **bug** for a concrete faulty path in the source, **risk** for an abuse opportunity or missing regression coverage. These are our customizations to fix.

## Findings

1. **bug: another character can operate the active tutorial.** `server/customizations/Tutorial/ClusterFTutorial.cs:124`, `:144`, `:164`, `:218`; `server/customizations/Tutorial/TutorialGumps.cs:44`.

   A second character on the same account gets the recruiter's active controls and can run or complete stations, skip, or collect graduation rewards despite failing `IsParticipant`, because those operations never compare `CharacterSerial` with the caller. Enforce the recorded character in each mutation, provide an explicit recovery path if that character was deleted, and extend `server/tests/Misc/TutorialVerification.cs:171` to exercise the second character's recruiter responses and reward attempts.

2. **bug: graduation can permanently lose the pet choice.** `server/customizations/Tutorial/ClusterFTutorial.cs:229`, `:255`; `server/customizations/Tutorial/TutorialGumps.cs:63`, `:244`.

   A graduate who closes the pet picker, disconnects, or restarts before choosing has no saved pending claim and no recruiter option to reopen it; the full-follower message also promises a recruiter retry that does not exist, while pinned `Projects/UOContent/Gumps/Base/GumpSystem.cs:37` clears gumps on disconnect. Persist a pending/claimed pet entitlement, let the recruiter resume an unclaimed choice, and test closing, disconnecting, loading a save, failed follower allocation, and exactly one successful claim.

3. **bug: remedial training grants another farm pet.** `server/customizations/Tutorial/ClusterFTutorial.cs:202`; `server/customizations/Tutorial/TutorialFarm.cs:123`, `:173`, `:186`.

   Take the farm pet, skip at the recruiter, then start remedial training: `StationsDone.Clear()` removes `farm.pet`, so the Farmhand grants another bonded pet while the first survives, bypassing the account's one-pet rule. Preserve reward claims separately from lesson progress and test this sequence, including after saving and loading the skipped record.

4. **risk: the healing step supplies unlimited transferable bandages.** `server/customizations/Tutorial/TutorialFarm.cs:158`, `:225`.

   While on farm step 3, a player can put each bandage stack in the bank or on the ground and talk to the Farmhand again, since issuance checks only the current backpack and records no grant. Save an issuance limit or use lesson supplies that cannot be stockpiled, and test repeated conversations after moving the first stack out of the backpack.

5. **risk: tutorial serialization boundaries lack focused tests.** `server/tests/Misc/TutorialVerification.cs:126`; `server/customizations/ClusterFAccountData.cs:445`, `:1256`, `:1276`.

   The tutorial round-trip checks only the active state, character serial, and one station, leaving skipped/remedial/graduated records, `WasSkipped`, timestamps, pre-v19 input, and invalid nested versions or state bytes without tutorial-specific assertions. Add frozen v18 and v19 input fixtures, full-field round-trips with a trailing sentinel, and rejection tests for unsupported `TutorialRecord` versions and states.

6. **risk: Young transitions during an active tutorial are untested.** `server/tests/Misc/TutorialVerification.cs:193`; `server/tests/Tutorial/GraduationLoopVerification.cs:71`; `server/tests/Misc/YoungPlayerVerification.cs:146`.

   The tutorial tests preserve an already-Young player during the vision and graduation, while the separate expiry, renunciation, and murder tests never start a tutorial, so they do not prove that losing account-wide Young status mid-lesson preserves participation, progress, and graduation. Add active-core and remedial cases for expiry and voluntary renunciation, verify every character's Young flag, then complete and graduate without restoring Young or duplicating rewards.

## Checks with no additional finding

- **Serialization:** no layout mismatch found between the current account writer and reader: account version 22 still embeds `TutorialRecord` version 0 at the v19 position (`ClusterFAccountData.cs:445`, `:503`, `:603`), and the nested reader rejects unknown versions and state bytes (`:1276`). The record writes state, character serial, stations, skip history, and both timestamps in matching order (`:1281`, `:1296`); ordinary progress has no apparent logout reset.
- **Young:** no additional behavioral defect found in the reviewed tutorial paths. Participation is independent of Young (`ClusterFTutorial.cs:53`), tutorial creatures explicitly ignore Young protection (`TutorialCreature.cs:31`), and loop recording does not remove or restore Young (`ClusterFLoops.cs:47`). P371's preservation of Young at graduation is intentional.
- **Skip and rewards:** no additional bypass of the two skip confirmations or repeat graduation/achievement grant was found. Pinned `Projects/UOContent/Gumps/Base/GumpSystem.IncomingPackets.cs:39` requires a live matching gump and validates the response button (`:57`), so directly invoking a second-confirmation object in a unit test does not establish a client exploit; graduation changes the account state before awarding (`ClusterFTutorial.cs:229`), and repeated loops are refused (`ClusterFLoops.cs:54`).
- **Known limitations excluded from new findings:** P80's unfinished station stubs and existing-account entry issue; P276's in-memory pest counter resetting on restart; P371's previously reported disabled-tutorial trap and pet transport ordering. They are already recorded and are not repeated as new defects here.

## Review scope and limits

Read the tutorial state machine, station registry, recruiter, gumps, loop/vision code, creature base, farm lesson and seeder, and island gate under `server/customizations/Tutorial/`. Traced the tutorial account serializer and persistence item in `server/customizations/ClusterFAccountData.cs`, starter pet creation in `server/customizations/Mobiles/Evo/EvoPet.cs`, tutorial achievement definitions in `server/customizations/ClusterFAchievements.cs`, and reward deduplication in `server/customizations/LootBoxes/ClusterFLootBoxes.cs`.

Test review covered `server/tests/Misc/TutorialVerification.cs`, `server/tests/Tutorial/TutorialFarmVerification.cs`, `server/tests/Tutorial/GraduationLoopVerification.cs`, `server/tests/Misc/YoungPlayerVerification.cs`, and relevant serializer and achievement assertions in `server/tests/Misc/AccountDataSerializerVerification.cs` and `server/tests/Misc/AchievementEarnedLineVerification.cs`. Checked `ClusterFYoungPlayer.cs`, both Young patches, and pinned Account, PlayerMobile, and gump lifecycle source for the relevant dependencies.

No tests were added or run, as this task is review notes only with no lane tests. A running player reproduction, a real restart, and generated NPC serialization round-trips remain unverified. The progress generator was not run because its `build()` writes `tools/progress.json` even with `--dry-run`, outside this task's requested notes-only output. No files under `docs/` were edited.

P420 DONE
