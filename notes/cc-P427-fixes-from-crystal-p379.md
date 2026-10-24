# cc-P427: fixes from Crystal's review of the 10-21 merges (P379)

## In plain words

- **Levelable gear no longer earns experience from killing someone's pet.** Before, two players could farm item levels
  by having one kill the other's tame animals.
- **Fletching, carpentry and tinkering bulk orders now refuse shop-bought items,** as the other bulk orders already did.
  A bow, quarter staff or cleaver from a shopkeeper no longer fills them. A crafted one still does.
- **A hidden achievement was sometimes given when it should not have been; that is fixed.** The server also stops
  keeping a slowly growing list of released pets.
- **Nothing for you to do.** One fix is a new one-line server patch, `PlayerMobile-noted-damage-memory.patch`; it
  builds and applies cleanly. The art list's one wrong hex number is corrected too.

## Verified against main first

All five findings were still present on this branch (ShatteredLegacy at `b23e87f`). None had been fixed
by a later merge.

| # | Where (before) | Still there? |
|---|---|---|
| 1 | `ClusterFLevelGear.cs:455-462`: the award ran on `CreatureDeathEvent` | yes |
| 2 | `CraftBOD.EndCombineSmall`: no `ClusterFStoreBought.Refuses` | yes; it was used only in the SmallBOD patch, `LargeBODItemFill.cs:68` and the commissions |
| 3 | `ClusterFNotedBySystem.cs:609`: `pm.FindDamageEntryFor(bc) == null` alone | yes |
| 4 | `ClusterFNotedBySystem.cs:647-661`: `_released` pruned only by `Tamed` | yes |
| 5 | `registry.csv:55`: `54783,0xD5EF` | yes, and the only mismatched row of all 561 (counted by script) |

## The fixes (ShatteredLegacy, branch `golem/Iron/P427`)

### 1. Level gear: no XP from a pet's death

- **The bug, confirmed in pinned.**
  1. `BaseCreature.OnDeath` raises `CreatureDeathEvent` only after `Mobile.OnDeath` has deleted a non-player
     (`BaseCreature.cs:3662-3669`).
  2. `OnDelete` raises `CreatureDeletedEvent` first (`:3674`), and only then clears the master (`:3687-3688`).
  3. So a killed pet looked wild by the time the award ran.
- **The fix.** `ClusterFLevelGear.OnCreatureDeleted` (`LevelGear/ClusterFLevelGear.cs:461`) awards on
  `CreatureDeletedEvent`, with P263's guard `bc.Hits <= 0 && !bc.IsDeadPet`. At that point the master and the damage
  list are still there.
  - A bonded pet's death deletes nothing and the pet is still controlled, so it pays nothing.
  - A summoned creature keeps `Summoned`, so it pays nothing.
  - A wild creature pays as before: the orc case is unchanged and green.
- **The test.** `LevelGearVerification`, the "pool is split" fact, now kills the horse with `tame.Kill()` and asserts
  the wearer's sword XP did not move. It also adds a summoned orc killed the same way.

### 2. Crafted only, for the ported craft deeds

- `CraftBOD.EndCombineSmall` (`Services/BulkOrders/CraftBOD.cs:218`), after the type check, refuses
  `ClusterFStoreBought.Refuses(item)` with `ClusterFStoreBought.Refusal`, as `LargeBODItemFill.cs:68-72` does.
- `EndCombineLarge` takes only small deeds, never items, so it needs nothing. The container combine
  (`BODCombineContained.cs:84`) calls the same `EndCombine`, so it is covered too.
- Jewels (the tinker rings) are not armor, weapons or clothing. `ClusterFStoreBought.IsStoreBought` is false for them,
  as before.
- The existing `BulkOrderCraftsVerification` facts built uncrafted weapons. Their `Make` helper and the explicit
  `QuarterStaff` and `Bow` now set `PlayerConstructed`, as a craft does (P263 did the same on the smith side).

### 3. Noted by the System: the hidden kill rule survives a heal

- **The bug.** The check used the player's own damage list, which pinned empties at full hits (`Mobile.cs:2043`) and
  expires after 2 minutes. A creature that had hit the player before they healed counted as one that never had.
- **The fix.** A record of which players each creature has damaged: `_damagedPlayers`, `PlayerDamaged`
  (`ClusterFNotedBySystem.cs:604`) and `HasReached` (`:615`). The kill check now refuses when either the record or the
  damage list shows a hit (`:643`).
- **How the record is filled.** The new patch `server/patches/PlayerMobile-noted-damage-memory.patch` adds one call in
  `PlayerMobile.OnDamage`, which pinned's `Mobile.Damage` calls on every hit (`Mobile.cs:6009`, after `RegisterDamage`
  at `:5983`). That is the same place and the same damage the list records. The patch is registered in
  `docker/uo/apply-patches.sh` with a comment, and both builds logged "Applied: PlayerMobile-noted-damage-memory.patch".
- **Why a patch.** No damage event or existing hook reaches the player's side. The pet-training hook in `AOS.Damage`
  sees only damage that goes through AOS, and it is pet code.
- **Clean-up.** A creature's record is removed in `OnCreatureDeleted` (`:589`) whenever it is deleted, dead or not, so
  the record holds only living creatures.

### 4. Released pets forgotten

- `OnCreatureDeleted` removes a deleted pet from `_released`.
- `Released` (`:684`) drops every remembered release that is deleted or past `RetameWindow` (5 minutes, the only time
  it can count) before adding the new one.

### 5. Art registry

- `player-package/vendor/shattered-legacy-art/registry.csv:55` now reads `54783,0xD5FF` (54783 is 0xD5FF; 0xD5EF is
  54767).
- A new package fact, `EveryRegistryRowsHexIsItsId` (`player-package/tests/Build-UoOverrides.Tests.ps1`), checks that
  every row's hex is its id.

## Tests

| Fact | Red (mutant or old row) | Green |
|---|---|---|
| `LevelGearVerification.ThePoolIsSplitByDamageWithAPetsDamageCountingAsItsMasters` (pet through `Kill()`) | the pet's death paid 23 XP (260645 expected, 260668) | pass |
| `BulkOrderCraftsVerification.TheFletchingCarpentryAndTinkeringDeedsTakeOnlyCraftedItems` (shop bow, staff, cleaver refused; crafted taken; setting off takes the shop's) | the shop's bow filled the deed (1, expected 0) | pass |
| `NotedBySystemVerification.ACreatureThatHitYouStillReachedYouAfterAHealToFull` (hit, heal to full, kill: no count; record forgotten on death and on a plain delete) | the bug reproduced: the count was 1 after the heal | pass |
| `NotedBySystemVerification.AReleasedPetThatIsGoneOrPastTheWindowIsForgotten` (deleted pet forgotten; a release past the window dropped by the next) | the deleted pet was still remembered | pass |
| Package: `EveryRegistryRowsHexIsItsId` | `expected [] but got [54783=0xD5EF]` | pass; 24 of 24 package facts |

**How the red runs were done.** I applied each fix, then switched each off in a mutant: the award back on
`CreatureDeathEvent` with no guard, no store-bought check, `HasReached` always false, and nothing removed or pruned. The
new and changed facts failed: 4 failed, 2,284 passed.

The first red run stopped the Noted fact at a check on the record itself, before the kill. I reordered the fact so
the count is checked first, and a second red run then showed the bug itself (count 1). The package fact ran red
against the old row before I fixed it. Its first run failed on a path-escaping slip in the test text, not on the row,
so I fixed the text and ran it red again.

**Green.** `docker/uo/build.sh -t sl-modernuo:cc-P427`, under the `docker-build` lock (taken, then released):
**2,292 tests, 2,288 passed, 0 failed, 4 skipped**, and the image `sl-modernuo:cc-P427` was built. 13.3 GB was free,
and I dropped the VM page cache before the green build.

`CHANGELOG.md` (2026.10.24.8, three Fixed lines) and `VERSION` were edited after the build. The changelog's line for
finding 3 does not say what the hidden achievement's rule is.

## Deviations and decisions for Chase

- **Finding 3 needed a new server patch** (one line in `PlayerMobile.OnDamage`); there was no other way to see hits
  on the player's side. The record is in memory only and is forgotten when the creature goes.
- **The kill check keeps both tests** (the record and the damage list), so it can only become stricter than before.
- The P379 drafts asked for separate notes files per finding. The prompt merged them into this one.

P427 DONE
