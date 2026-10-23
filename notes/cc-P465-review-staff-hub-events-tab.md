# P465: Staff Hub Events tab review

Reviewed 2026-10-23. Code HEAD: `4c2af57`. Notes HEAD before this review: `ac7e8ec`.
Docs only. All findings concern our Staff Hub code.

## Scope and limits

Read `cc-P230-staff-hub-events-tab.md` first. No separate P230 review was found beside it;
`cc-P379-crystal-review-10-21-merges.md` explicitly excludes P230 from its reviewed range.
The findings below do not repeat P230's recorded insurance charge, healed-damage sampling
window, template display limit, or deliberate normal creature loot.

Reviewed these code-repo files and the paths they call:

- `server/customizations/StaffHub/ClusterFSurge.cs`
- `server/customizations/StaffHub/ClusterFSurgeTemplates.cs`
- `server/customizations/StaffHub/StaffHubGump.cs`
- `server/customizations/StaffHub/ClusterFStaffHub.cs`
- `server/tests/Misc/StaffHubEventsVerification.cs`
- `server/tests/Misc/StaffHubVerification.cs` (including button IDs and stale responses)
- `server/tests/Misc/StaffHubReadabilityVerification.cs`
- `CHANGELOG.md` (P230's player and staff promises)
- `VERSION`

Upstream references below are relative to `D:\UO\ModernUO-pinned`, verified at
`d4531cd94b739613155225c234900de9f47d2c88`. These are source-review findings, not runtime
reproductions. No build, client session, server connection, or test execution was performed;
the prompt specifies no lane tests. Suggested tests remain work for the fixing task, which
must observe them failing first.

## Findings

1. **bug: replacement monsters escape cleanup.** `server/customizations/StaffHub/ClusterFSurge.cs:542`,
   `:596`, `:700`, `:824`: a permitted `KhaldunZealot` creates a BoneKnight and deletes itself
   instead of completing an ordinary death, so the next tick forgets the original and can end
   the surge while the untracked BoneKnight remains hostile and survives End and restart cleanup
   (pinned `Projects/UOContent/Mobiles/Monsters/Humanoid/Melee/KhaldunZealot.cs:93`).
   Restrict templates to supported creature types until replacement and child spawns can inherit
   surge ownership, and add a real Zealot death test that checks the replacement, End, and the saved cleanup list.

2. **bug: an old window or cursor acts on a different surge.**
   `server/customizations/StaffHub/StaffHubGump.cs:793`, `:807` and
   `server/customizations/StaffHub/ClusterFSurge.cs:785`: if GM A leaves surge A's running window
   or extra-prize cursor open while GM B ends A and starts B, A's End button ends B and the old
   cursor gives B's configured prize because both actions resolve the current global run.
   Capture the displayed run in the gump and cursor, reject a changed run before acting, and
   test two staff members retaining A's controls while B starts.

3. **bug: a dead pet's unsampled damage loses its owner.**
   `server/customizations/StaffHub/ClusterFSurge.cs:211`: if a non-bonded controlled pet damages
   a surge creature and dies before the next sample, `GetMaster()` is already null and its damage
   is skipped, even though pinned saved the responsible owner with the hit
   (`Projects/Server/Mobiles/Mobile.cs:5910`, `Projects/UOContent/Mobiles/BaseCreature.cs:3688`).
   Track deltas from each damage entry's `Responsible` records instead of relying on current
   ownership, and add a pet-hit, pet-`Kill()`, then-sample test asserting the owner's total and prize.

4. **bug: the extra-prize cursor survives loss of staff access.**
   `server/customizations/StaffHub/StaffHubGump.cs:807` and
   `server/customizations/StaffHub/ClusterFSurge.cs:783`: a GM can open Give extra, be demoted
   below GameMaster, then answer the cursor and still mint the prize, since the callback and
   `GiveExtra` omit the access check made by the initial gump response at `StaffHubGump.cs:865`.
   Recheck the giver's access at the mutation boundary and add a test that opens the real cursor,
   demotes its owner, invokes it, and verifies no item or award was created.

5. **risk: a failed prize delivery can stop the timer before cleanup and duplicate earlier prizes.**
   `server/customizations/StaffHub/ClusterFSurge.cs:675`, `:687`, `:777`: if an item constructor
   or delivery throws during Award, Finish has already stopped the timer but never reaches
   RemoveEverything or clears Active, and pressing End again starts the award list over with
   no record that prevents paying earlier recipients twice or reverses their delivered items.
   Make cleanup unconditional, isolate and record each recipient's delivery so retry cannot
   repay it, and add an injected delivery-failure test checking cleanup and exactly one payment
   to recipients who succeeded before the failure.

6. **risk: staff event changes and grants have no audit log.**
   `server/customizations/StaffHub/StaffHubGump.cs:789`, `:823`, `:1260` and
   `server/customizations/StaffHub/ClusterFSurge.cs:804`: Start, End, template save/replace/delete,
   and extra grants call helpers directly without `CommandLogging`, while broadcasts and the
   in-memory Awards summary do not provide a durable account/target/settings record; pinned's
   command logger records opening `[SL`, not these later clicks
   (`Projects/UOContent/Commands/Logging.cs:16`, `:124`).
   Log successful mutations and each automatic or extra prize with staff identity where applicable,
   run identity, recipient, and item/amount, and add assertions that each successful action emits
   its audit record while a rejected action emits no success record.

7. **risk: accepted invulnerable NPC templates cannot finish automatically.**
   `server/customizations/StaffHub/ClusterFSurgeTemplates.cs:95` and
   `server/customizations/StaffHub/ClusterFSurge.cs:610`: `Banker` passes the public BaseCreature
   constructor check, but under pinned's default vendor invulnerability it cannot be killed,
   so a surge containing it keeps its gates and no-loot zone until staff manually press End
   (`Projects/UOContent/Mobiles/Townfolk/Banker.cs:13`, `:18`,
   `Projects/UOContent/Mobiles/Vendors/BaseVendor.cs:50`, `:102`).
   Reject noncombat or invulnerable templates during validation, or explicitly offer a bounded
   duration for such events, and test the refusal with vendor invulnerability enabled.

## Test coverage and checks

`StaffHubEventsVerification.cs:224` checks cleanup of directly created Orcs and gates;
`:272` round-trips the surge serial list without performing a full world restart.
Neither covers replacement monsters or prize-delivery failure. Its damage test at `:331`
uses direct player hits, and its access test at `:610` presses Start as a Counselor rather
than completing a previously authorized target cursor. The button test at `:535` uses one
GM and one run at a time. There are no audit-record assertions in these reviewed tests.

No ordinary double-start defect was found: `ClusterFSurge.cs:419` refuses Start while
Active is set. That refusal itself has no explicit second-Start regression assertion in
`StaffHubEventsVerification.cs`; add one when extending lifecycle coverage.

The failure-injection scenario in finding 5 and the live configuration and client behavior
in finding 7 remain unverified. Findings 1 through 4 were traced through the pinned code,
but their suggested runtime reproductions have not been run. No code or tests were changed.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work
copies; it completed successfully but rewrote `tools/progress.json` despite the flag.
Restored that generated file to its original HEAD bytes to keep this task notes-only.
Both work copies were clean before review. The only added file is this note, below 5 MB,
with no em dashes.

P465 DONE
