# P449: review of graduation as the first loop

Reviewed 2026-10-22 against ShatteredLegacy `7508639`, including the merged P371 change `fa2810f`. Read both work copies' AGENTS.md, the direction decision, the task list, P371's implementation notes, and its adjacent Codex review first.

The findings below concern the graduation flow and its existing tutorial dependencies. Findings 1 through 3 were already present before P371; they are not claimed as regressions introduced by the new loop counter. The earlier review's findings are excluded.

## Findings

1. **bug** - `server/customizations/Tutorial/ClusterFTutorial.cs:255`, `server/customizations/Tutorial/TutorialGumps.cs:63`, `server/customizations/Tutorial/TutorialGumps.cs:252`: A graduate who logs out or closes the pet picker before choosing loses access to the starter pet, and a graduate with full follower slots also loses access after closing the retry picker, despite its instruction to ask the recruiter again; the recruiter has no pet-claim action for Graduated accounts and OnLogin only repairs the loop count. Persist a pending/claimed starter-pet entitlement, offer pending claims through the recruiter or login, and test reconnecting and freeing a follower slot without replaying boxes.

2. **bug** - `server/customizations/Tutorial/ClusterFTutorial.cs:202`, `server/customizations/Tutorial/TutorialFarm.cs:123`, `server/customizations/Tutorial/TutorialFarm.cs:186`: A trainee can take the farm's bonded starter pet, skip, and start remedial training, which clears `farm.pet` and lets the Farmhand give another pet while the first still exists. Keep the pet entitlement outside the resettable station set, or preserve the claimed marker when starting remedial training, and test this sequence with the original pet still owned.

3. **bug** - `server/customizations/Tutorial/ClusterFTutorial.cs:164`, `server/customizations/Tutorial/ClusterFTutorial.cs:218`, `server/customizations/Tutorial/TutorialGumps.cs:44`: An alternate character can open the recruiter while another character on the account owns the active tutorial, skip that character's training, or graduate using its completed core and receive the graduation rewards, because the mutators check only the shared account state while `IsParticipant` correctly checks `CharacterSerial`. Require the active character's serial for station changes, skipping, and graduation, provide an explicit handoff if needed, and test that an alternate cannot mutate another character's active record.

4. **risk** - `server/tests/Tutorial/GraduationLoopVerification.cs:202`, `server/tests/Misc/TutorialVerification.cs:121`: The logout coverage internalizes and manually moves the player back, or calls OnLogin twice on the same connection, so it does not exercise a fresh connection's LogoutMap/LogoutLocation restoration or graduation with an outstanding reward choice. Add a real disconnect/reconnect regression around InWings, Remedial, and the pending pet claim, asserting the restored location, saved station progress, loop count, and unchanged box awards.

## Review evidence and limits

Read the canonical loop, tutorial, station, recruiter, gump, farm, account-record, and loot-box implementations, all three island-gate patches, and their apply-patches.sh registrations. Reviewed these test files named in P371's notes:

- `server/tests/Tutorial/GraduationLoopVerification.cs`
- `server/tests/Misc/TutorialVerification.cs`
- `server/tests/Tutorial/TutorialFarmVerification.cs`
- `server/tests/Regions/RootdeepWayInVerification.cs`
- `server/tests/Misc/YoungPlayerVerification.cs`
- `server/tests/Regions/OldHavenBurrowsRegionVerification.cs`
- `server/tests/Regions/OldHavenNewPlayerSafeVerification.cs`
- `server/tests/Misc/StaffHubVerification.cs` (the cited panel regression)
- `server/tests/Items/Traps/DeployableTrapsVerification.cs` (the affected practice-net case)

Pinned ModernUO was verified at `d4531cd94b739613155225c234900de9f47d2c88`. Its `Projects/UOContent/Gumps/Base/GumpSystem.cs:28` keys open gumps by NetState, and `:67` creates an empty list for a new connection; the graduation pet choice has no persistent pending claim. `Projects/Server/Mobiles/Mobile.cs:1320` restores LogoutMap and LogoutLocation on connection, a different route from the internalization test.

No additional defect was found in the monotonic loop counter, ordinary repeat graduation's box suppression, or keeping Young through graduation. The Explorer box and Loop box are separate intended awards, not duplicate delivery of one source. The default skip waiver and later-character login waiver are explicit P371 choices and are not findings. No additional island-exit bypass or location softlock was established in the reviewed paths.

This was a source review, not a runtime reproduction. No tests were added or run, as requested for this docs-only lane. Client behavior, live placement and settings, and the official Docker build remain unverified. Ran the progress reporter with work-copy paths and `--dry-run` successfully, then restored its incidental progress.json write byte for byte to keep the deliverable limited to this note. No code, docs directory, services, accounts, branches, or commits were changed, and no Haven connection was made.

P449 DONE
