# P462: review of the rideable red dragon (P277)

Reviewed October 23, 2026. Notes only. No code or tests changed.

Read `notes/cc-P277-rideable-red-dragon.md` and
`notes/cc-P277-rideable-red-dragon-codex-review.md` first. The earlier proof and
package finding, the low rider position, and the pending acquisition decision are
not repeated here.

## Findings

No confirmed runtime bug found in the current staff-only implementation. These
are test coverage risks, not reproduced combat, restriction, or pet-loss bugs.
Paths below are relative to the ShatteredLegacy work copy.

1. **risk** - `server/tests/Mobiles/Mounts/RideableDragonVerification.cs:102`:
   The ride test mounts an idle red dragon and dismounts immediately, so it cannot
   catch a dragon continuing to damage an opponent while ridden or its combat
   stats affecting the rider. Add cases for both dragons that establish combat,
   mount, advance the test clock through attack intervals, and verify no further
   dragon damage and no change to the rider's combat stats.

2. **risk** - `server/tests/Mobiles/Mounts/RideableDragonVerification.cs:81`:
   The serializer test copies only an unmounted dragon while its original mount
   item remains in the test world, then checks body, name, and item ID, so it does
   not establish that a saved ridden dragon and its mount item reconnect after a
   world reload. Add an isolated save/load case for each ridden dragon that
   restores the rider, dragon, and mount item together, checks both directions of
   their references, and dismounts without deletion or duplication.

3. **risk** - `server/tests/Mobiles/Mounts/RideableDragonVerification.cs:95`:
   The lifecycle test never exercises trainer stable/claim or logout auto-stable
   and login claim, leaving ownership, follower accounting, and recovery of these
   new types unverified. Add cases for both dragons with ownership assigned in
   the fixture, including a full follower limit that leaves the dragon safely
   stabled, successful later claim and remount, and a stable save/load cycle.

## What the source establishes

Pinned ModernUO was verified at
`d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`.
The following paths are relative to `D:/UO/ModernUO-pinned`.

- **Combat:** `server/customizations/Mobiles/Mounts/RideableDragons.cs:54` and
  `:69` in ShatteredLegacy derive directly from `BaseMount`, with horse stats
  and no dragon breath or ridden attack override. Keeping the creature's own
  stats while ridden is normal mount behavior, not itself a defect:
  `Projects/UOContent/Mobiles/Animals/Mounts/BaseMount.cs:120` internalizes it,
  `Projects/UOContent/Mobiles/AI/BaseAI/AITimer.cs:204` stops its AI on the internal
  map, and `Projects/Server/Mobiles/Mobile.cs:787` rejects combat across maps.
  `BaseMount.cs:311` supplies no mount attack ability.
- **Mount bans:** neither dragon overrides `OnDoubleClick` or assigns a rider
  through a separate entry point. `BaseMount.cs:211` calls the shared guard;
  `:283` checks the active region, mount block, and gargoyle restriction before
  the staff ownership exception at `:241`. Existing upstream coverage is
  `Projects/UOContent.Tests/Tests/Mobiles/MountRegionTests.cs:28`, using a horse
  through this same path. ShatteredLegacy's
  `server/customizations/Services/Revamped Dungeons/BlackthornDungeon/Region.cs:296`
  also handles any mount on entry, and its verification at
  `server/tests/Services/Revamped Dungeons/BlackthornDungeon/BlackthornDungeonVerification.cs:349`
  covers dismounting and stabling a controlled horse. No dragon-specific bypass
  found; a duplicate region-guard finding is not warranted.
- **Stable and claim:** `Projects/UOContent/Mobiles/Vendors/NPC/AnimalTrainer.cs:204`
  accepts an owned controlled creature without a dragon type exclusion; `:355`
  restores its control master and world location. The same generic handling is
  in `Projects/UOContent/Mobiles/PlayerMobile.cs:3509` and `:3570`, including
  skipping ridden mounts and retaining pets in the stable when followers are
  full. ShatteredLegacy's
  `server/patches/BaseCreature-PlayerMobile-can-auto-stable.patch` adds a guard
  whose inherited default permits these dragons. The current unowned staff
  spawns cannot be trainer-stabled until ownership is assigned, which matches
  their placeholder scope; this is not evidence of a lost pet.

## Scope and verification limits

Also inspected P277's body registrations, package records, registry and source
credit entries, mount item PNG presence, outside-git encoder changes and Python
tests, launcher dragon fact, ignore rule, and changelog entry. No additional
actionable finding there. The scope is the merged implementation, not a player
acquisition system or new dragon combat design.

This was a static source review. No lane tests were requested, and no tests,
build, client session, or save/load probe ran. Actual combat and persistence
behavior remain unverified at runtime in this review. No connection to Haven,
deployment, or branch or commit operation was made.

`tools/progress.py --dry-run` completed successfully with `SL_SHARD` and
`SL_MIGRATE` pointing at these work copies. Despite the flag, its `build()`
function refreshed `tools/progress.json`; that generated file was restored to
its clean starting content to preserve this task's notes-only scope.

P462 DONE
