# ShrunkPet: restore stops following, follower count drifts, pet escapes on logout

2026-10-03. Follow-up to `notes/cc-P41-companions-research.md` section 5 item 3, where two defects were
found **by reading only**. This task proved both with probe tests, fixed them, and reran the tests green.
It also found a third defect, larger than either: **a shrunk pet left its figurine on the owner's next
logout and login, and at every restart.** That one was probed and fixed too.

Files (shard repo, `D:\ShatteredLegacy`):

- `server/customizations/ShrunkPet.cs`: the fix
- `server/tests/Items/ShrunkPetVerification.cs`: 5 tests, new

`OutridersCrook.cs` is unchanged. See section 4.

## 1. What the tests showed on the old code

Every run was `docker/uo/build.sh --tests-only` in a clean detached worktree of shard `HEAD` (`d22a649`)
plus only these two files. The main checkout held another session's uncommitted cc-P46 work, and a build
there would have tested that work too.

Final red run (unchanged `ShrunkPet.cs`, final tests): **496 total, 491 passed, 5 failed**. Four of the
failures are ours, and the fifth is a known flake (below). Test output:

| Test | Old code printed |
|---|---|
| `ARestoredPetKeepsFollowingAfterAnAiTick` | `after restore: order=Follow target=null`, then `after one DoOrderFollow: order=None` |
| `AShrunkPetStaysInItsFigurineAcrossALogoutAndLogin` | `after logout: map=Internal stabled=True master=null`, then `after login: map=Trammel` |
| `FollowerCountSurvivesARestartWhileShrunk` | after the pet's load `followers=1` (should be 0), then `after startup and login: map=Trammel` |
| `AFigurineRestoredByAnotherPlayer...` | shrinker `0`, holder `2` (slots=1) |
| `FollowerCountIsUnchangedByAShrinkAndRestoreInOneSession` | passed (control) |

The fifth failure in that run was `SmithBODPathsVerification.ALargeDeedNeedsSeventyPointOneBlacksmithyAtTheGuild`,
which threw a `NullReferenceException` at pinned `SkillCheck.cs:72` (`AntiMacroSystem.Settings` null). It passed
in the other four runs. At `HEAD` the settings exist only if a craft test happens to run first, so it depends
on test order. The cc-P46 session's uncommitted `server/tests/Route/ShardTestHost.cs` is fixing exactly this
(cc-P46 Part F). It is unrelated to this change.

The two earlier red runs, before the logout test existed, showed the restart drift on its own:
followers `0` when shrunk, `1` after the pet's load, `2` after restore.

So, in the old code:

1. **Restore did not follow.** `SetControlMaster` clears `ControlTarget` (pinned `BaseCreature.cs:3782`).
   The raw `ControlOrder = Follow` after it left no target, and one `DoOrderFollow` tick
   (`PetOrders.cs:638-644`) dropped the order to `None`. The pet appeared at your feet and stood still.
2. **Restart drift.** `Followers` is not saved (pinned `Mobile.cs:6331-6334`). The pet's own `Deserialize`
   adds its slots back to `Master` (`BaseCreature.cs:2514`), and restore then added them a second time.
3. **Transfer double count (new, not in cc-P41).** The figurine is movable. When another player restored it,
   `SetControlMaster` moved the slots to them through the `Master` setter (`BaseCreature.cs:1163-1170`), and
   the old `pm.Followers += ControlSlots` added them again.
4. **The pet escaped the figurine (new, and the worst).** `TryShrink` left the pet in the owner's
   `AllFollowers`, and the load path puts it back there regardless. With SE on (this shard runs EJ),
   pinned auto-stables every controlled follower in `AllFollowers` on logout (`PlayerMobile.cs:1522`) and
   at every startup (`CheckPets`, `:950`, `:1064-1083`). It brings them back on login
   (`ClaimAutoStabledPets`, `:1276`, `:3570`). The shrunk pet came out at the owner's feet. The figurine
   was left pointing at a pet no longer on `Map.Internal`, so double-clicking it only said "This creature
   does not appear to be stored", and it was never deleted. **So the figurine has never held a pet across
   a logout.** Item 2 could only show up when the owner stayed online, and the code cannot have that
   across a restart, because every owner is offline at startup.

## 2. The fix

- Restore calls `pet.IssueOrder(OrderType.Follow, null, pm)`. It sets `ControlTarget` before the order
  (`BaseCreature.cs:1213`), and `IssueFollow` records it as the persistent target (`PetOrders.cs:157-173`).
- `TryShrink` takes the pet out of `AllFollowers` (`pm.RemoveFollower`) as well as out of `Followers`.
- New `public static void Initialize()` on `ShrunkPet` undoes the load path. After `World.Load`
  (`Main.cs:672-674`) it walks `World.Items` and takes each stored pet off its master's `Followers` and
  `AllFollowers`. This happens before `CheckPets`, which is a timer that `PlayerMobile.Initialize` starts.
  `Followers` is clamped at 0, the same way `RemoveFollowers` clamps. **This also corrects figurines shrunk
  before the deploy**, because their pets still have `Master` set.
- Restore first puts the pet back in its current master's `Followers` and `AllFollowers`, then calls
  `SetControlMaster(pm)` only when the master is someone else. The `Master` setter moves both in that case.
  There is no separate `+= ControlSlots` any more.

**Rejected: clear the master on shrink, the way pinned stabling does** (`PlayerMobile.cs:3551-3557`,
`AnimalTrainer.cs:253-259`). That would have kept the load path and auto-stable away from the pet, but
`IsStabled` is not saved: it is restored at owner login only for pets in `pm.Stabled`
(`PlayerMobile.cs:3099-3105`). An uncontrolled, not-stabled pet with a `LastOwner` gets a 3-day
`DeleteTimer` at load (`BaseCreature.cs:2504-2507`), and `DeleteTimer.OnTick` just deletes (`:5940-5943`).
Shrunk pets would have been deleted 3 days after any restart.

## 3. Green

Same worktree with the final fix: **496 total, 496 passed** (`[tests] 496 test(s) passed.`). All five
`ShrunkPetVerification` tests pass, and so do the 491 that already existed, including the SmithBOD flake this
time. An intermediate fix without the `AllFollowers` part had passed the first four tests (495/495) before
the logout test existed. That fix was incomplete, which is why the logout test was added.

Each gate was proved: every test that fails above was watched failing on the old code, then passing.

## 4. `OutridersCrook.cs` and other raw `ControlOrder = Follow`

- `OutridersCrook.cs:239-272` (`BeginShrink` / `ShrinkTarget`) only calls `ShrunkPet.TryShrink` and drops the
  figurine into the pack. It assigns no order. `:168` only reads `ControlOrder`. **Nothing to fix there.**
- Every other raw `ControlOrder = OrderType.Follow` in `server/customizations` at `HEAD` sets `ControlTarget`
  first, as pinned `AnimalTrainer.DoClaim` does (`AnimalTrainer.cs:357-360`), so none has this defect:
  `WispOrb.cs:382-383, 401-402, 579-581`, `DespiseBosses.cs:360-361, 424-425`, `DespiseController.cs:533-534`.
- **Unverified, not touched:** `DespiseRevamped/AI.cs` (`HEAD` lines 40, 111, 220, 291) sets raw `Follow`
  without setting the target. After an `IssueOrder(Attack, null, target)` the `ControlTarget` is the
  attack target, so a raw Follow there may follow the enemy, or drop to None if the enemy is deleted.
  That file is in the cc-P46 session's uncommitted work (bug-list D58), so I left it alone.

## 5. Found while reading, not fixed

All three come from reading only. None is tested.

- **The figurine transfers a bonded pet and keeps the bond.** Any holder can restore it, and restore sets
  `IsBonded = true`. Pinned's own transfer clears the bond (`TransferItem.cs:163`). This was here before
  the fix and is unchanged. Whether a figurine should be owner-only is Chase's call.
- **Deleting the owner no longer releases a shrunk pet.** Pinned releases a deleted player's pets by walking
  `AllFollowers` (`PlayerMobile.cs:3839-3850`), and a shrunk pet is now out of that set. The figurine is in
  the deleted player's pack and goes with it, so the pet stays on `Map.Internal`, controlled by a deleted
  mobile. Before this fix the pet was released instead. Same for any figurine deleted by hand: the pet was
  orphaned there before the fix as well. A `ShrunkPet.OnAfterDelete` that deletes or releases the pet would
  close both cases.
- **Saves already holding an escaped pet.** Any figurine whose pet already came out through auto-stable is
  now an empty figurine that says "does not appear to be stored" for ever. The fix does not touch those.
  They are harmless but permanent.

## 6. What not to trust

- `FollowerCountSurvivesARestartWhileShrunk` serializes the **pet** and deserializes it back into the same
  object, which runs `BaseCreature.cs:2514`. The owner's reload is represented by setting `Followers = 0`
  and removing the pet from `AllFollowers`, since neither is saved. `Initialize` is invoked by reflection,
  the way `AssemblyHandler.Invoke` calls it. The startup timer is represented by calling `AutoStablePets`
  under `CheckPets`'s own condition. No real world save and load was run.
- Logout and login are represented by calling `AutoStablePets` and `ClaimAutoStabledPets` directly, the two
  calls those events make. No client check either: nobody has watched a figurine survive a relog in game.
- The test calls `DoOrderFollow` directly instead of waiting for an `AITimer` tick.
