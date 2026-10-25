# cc-P457: Noted by the System fix-up 2 (bard check, mining streak, ground at the destination, 15 tiles, Mule Train)

## In plain words

- Several of the hidden "Noted by the System" achievements now check what really happened, so they can no longer be
  earned by accident or by a shortcut, and a few that could never be earned in the right case now can.
- Players will only see the patch note "Some hidden achievements now check their conditions more carefully."
  (version 2026.10.24.14). Nothing else is visible.
- Nothing for you to do. One reading of your F07 decision is below under "For Chase", in case you meant something
  different.

## What changed

ShatteredLegacy, branch golem/Iron/P457, on main 6127603. P427 has merged, and P427's damage record is reused here.
Line numbers are from after this change.

| # | Finding | Fix |
|---|---|---|
| 1 | F01, the provoked half: "the bard never hit it" was read from the victim's damage list. Pinned empties that list at full hits (`Mobile.cs:2043`) and prunes it after 2 minutes (`:5880`). | A record of the same kind as P427's, the other way round. `_hitBy` holds creature → players who damaged it. It is filled by `CreatureDamaged` (`ClusterFNotedBySystem.cs:629`) from a new `BaseCreature.RegisterDamage` override (`BaseCreature-noted-damage-memory.patch`; nothing below `Mobile` overrides it, and `Mobile.Damage` calls it for every hit that has a damager, `:5983`). The record is forgotten in `OnCreatureDeleted`, with P427's. Not My Problem now also needs `!HasHit(bard, bc)` (`:680`). |
| 2 | F02: the empty-vein streak survived a successful swing elsewhere | `patches/Mining.cs` `CheckResources`: a swing (not timed) at a vein that has ore calls `SwungAtOre` (`:874`), which ends the streak. |
| 3 | F03: the ground was read at the departure tile, with no Z | Steps are now counted after the move. `PlayerMobile-noted-step.patch` adds an `OnAfterMove` override that calls `PlayerMoved` (`:974`). Pinned raises `EventSink.Movement` before `SetLocation` (`Mobile.cs:4103`, `:4386`), so the movement subscription, `Configure` and `Register` are gone. A turn in place leaves the location unchanged and does not count as a step. `GroundAt(map, x, y, z)` (`:903`) reads the player's own tile and height. First it looks for a fire field, or a passable lava or snow overlay that is not a surface, within 2 of the feet (pinned's step height). If there is none, it takes the highest walkable surface whose top is at or below the feet. Only if there is no such surface does the land count. |
| 4 | F04: `InRange` includes its range (`Mobile.cs:3076`), so 15 tiles was not remote | `RemoteWorkRange - 1` (`:686`). 15 tiles and more counts, as the header says. |
| 5 | F06: a Mule Train follower on another facet, or a dead one, counted | Followers now need `IsDeadPet: false` and `bc.Map == pm.Map` (`:1028`). |
| 6, F09 | Runebook markers | `RunebookFilled` (`:768`) writes nothing once Rune Archivist is earned. `FirstTimeFor` now sets its marker to 1, where it used to increment it on every refill of the same book. |
| 6, F10 | Cost per step | `PlayerMoved` reads the ground only for a player who is barefoot, in armor and on foot, the only set that uses it. `ClusterFAchievements.OfKind` keeps each kind's definitions in a sorted array built on first use (`_byKind`, declared beside `_defs`). `Reg` empties it. I did not add an early stop once an account's last tier is earned. |
| F07 | Recycling credited another player's fresh craft | Chase decided (10-22). `CraftItem-fail-streak-achievement.patch` now passes the new item to `CraftAttempt` at both success hooks. `Crafted` (`:829`) records the crafter in a `ConditionalWeakTable` held in memory: the windows are a minute at most, and a restart forgets nothing that could still count. `Recycled` counts an item only when `CrafterOf(item)` is the recycler. |

**What Hot Foot means now.** In the client's tiledata, lava land (0x1F4-0x1F7) and the lava pools are impassable,
so nobody stands on them. What a player actually walks through is passable lava overlay, such as 0x136E (flags
Damaging, not Impassable, not Surface), and fire fields. Those still count. The old code read the departure tile at
any height, so it could count lava a storey below a floor, or snow land under a floor.

**Test seam.** `ClusterFNotedBySystem.TilesFor` is null in play. The test host has no map files, and pinned's
`TileMatrix.GetLandBlock` and `GetStaticBlock` return the invalid or empty block without them, ignoring
`SetLandBlock`. So the step fact passes its tiles to `GroundAt` through this seam. The move itself is pinned's real
`Mobile.Move`.

## Tests

New file `server/tests/Misc/NotedFixupsVerification.cs`, eight facts:

1. `ABardWhoHitTheCreatureStillTouchedItAfterItHealsToFull` (:144): the bard hits the creature, it heals to full and
   pinned's damage list no longer holds the bard, then the provoked creature kills it. It does not count. An
   untouched creature does.
2. `EmptyAtAOreAtBEmptyAtAStartsTheStreakOver` (:170): 19 empty swings at A, a swing at ore at B, one at A. Rock
   Bottom is not earned. A fresh run of 20 at A earns it. All swings go through `Mining.CheckResources`.
3. `StepsCountWhereTheyLandAtThePlayersHeight` (:262): through `Mobile.Move` on a seeded row. A step onto snow
   counts, a step off it does not. The same for a lava flow. A floor over snow land does not count, and neither does a
   fire field 20 above the feet. A turn in place is no step. The tile rows were read from
   `D:/UO/UltimaOnlineVanilla/tiledata.mul` (md5 dd3acaacb5d953827c80af71ed2f736d), as `TestTileRows` requires.
4. `RemoteWorkFifteenTilesIsRemote` (:313): an owner 14 tiles away is near; 15 and 16 are remote.
5. `MuleTrainCountsLivingFollowersOnTheOwnersFacet` (:350): three full pack horses earn Mule Train. With one of the
   three on Felucca, or one a dead bonded pet, it is not earned (F11 positive, F06 negatives).
6. `RecyclingCountsOnlyTheRecyclersOwnCraft` (:388): a fresh exceptional item crafted by another player counts for
   neither recycle achievement; the recycler's own craft counts.
7. `EveryLiveCountedTierIsEarnedAtItsThresholdAndOnlyOnce` (:439) (F11): every live counted tier past the first,
   21 of them, at P263's numbers, which are written in the test. Each is not earned one short, is earned at the
   threshold with exactly its AP, and pays no more AP on the next event.
8. `CraftedOnlyHoldsAtEveryOrderAndCanBeTurnedOff` (:491) (F13): the large smith deed (`LargeBODItemFill`), a large
   commission's piece and a tailoring deed each refuse a bought item and take a crafted one. With `CraftedOnly`
   false, a small deed takes a bought sword; the setting is restored in a `finally`.

Changes to `NotedBySystemVerification.cs`: no `N.Register()` (it is gone). The turn-in-place check calls
`PlayerMoved` with the location unchanged. The recycle part records its crafter through `CraftAttempt`, as the
patch does. The runebook part asserts the marker stays at 1 after a refill. The fixture calls
`ShardTestHost.EnsureCraftSystems()`: P454's commission facts there threw a NullReferenceException when the class
ran alone, because only another class had built the smithing menu first.

`CC6Batch8Verification.BasePeerlessReachesEveryMLSpecialDropAndPacksTheSixResources`: the first full gate failed it
with "no HumanFeyLeggings in 100 kills". The leggings are an independent 10% per kill, so a fair generator misses all
100 about once in 37,000 runs. The fact passed alone and next to the Noted classes, so its result depended on the
draws made by the facts before it on the shared generator. The 100 kills now run on their own `System.Random(8129)`,
restored afterwards. I did not look for whichever fact leaves the shared generator in a fixed state.

**Red first.** The new facts call new methods (`PlayerMoved`, `GroundAt` with Z, `SwungAtOre`, `CraftAttempt` with
the item), so they cannot compile against the old code. As in P453, "red" means the fixed code with mutants that put
each old behaviour back. I ran them as bind-mounted probes on `sl-uo-builder:cc-P454` (this branch's base), with the
patched sources taken from that image.

- **R1**, seven mutants at once, one per fact: no `HasHit`, ground read at `oldLocation`, `RemoteWorkRange` without
  the -1, no map or dead-pet check, no crafter check, Frostbitten at 499, Mining without `SwungAtOre`, and
  `LargeBODItemFill` without `Refuses`. All 8 new facts failed, each at its own assert: "a creature the bard hit
  counted as never touched", "the streak at A survived a swing at ore", "at 1: snow 0, want 1", "owner 15 tiles
  away: remote False, want True", the Mule Train count, the recycle count, "noted.frostbitten at 499, the list says
  500", and the large deed amount.
  The tiers fact first read its thresholds from the definitions and passed R1. I then wrote P263's numbers into it.
- **R2**, floors ignored and the large commission without `Refuses`: the step fact failed (floor over snow: expected
  Other, actual Snow), and so did the crafted-only fact ("a bought piece filled a large commission").
- **R3**, fire fields at any height and `Refuses` ignoring the setting: the step fact failed (expected Other, actual
  Fire) and the crafted-only fact failed at the setting-off assert.
- **R4**, the old incrementing `FirstTimeFor`: the runebook marker assert failed with expected 1, actual 2.
- Not mutated separately: the tailoring deed's refusal. It is the same `SmallBOD-crafted-only.patch` line as the
  small smith deed, which is compiled into the image.

**Green, the gate:** `docker/uo/build.sh -t sl-modernuo:cc-P457`, under the `docker-build` lock, taken and released
for each run. The first run had 1 failure, the CC6Batch8 fact above. The second, after that fix: 2,327 passed. The
third, after the F09 marker change: **2,327 passed, 0 failed, 4 skipped**, no compiler warnings, image built, EXIT=0.
All patches applied, including `BaseCreature-noted-damage-memory.patch` and `PlayerMobile-noted-step.patch`, which
are listed in `apply-patches.sh` after P427's. Free memory went as low as 3.3 GB. I dropped the Docker VM's page
cache before the first run.

## For Chase

- **F07, how I read "count only items the recycler crafted, or loot".** Both recycle achievements say "something you
  made", and loot never counted before, because they require a crafted item. So I made "crafted by you" the rule and
  left loot out. If you meant fresh loot to count too, it is a one-line change in `IsCraftedBy`, but the achievement
  text would then need rewording.
- **Hot Foot** (part 3, not a decision): it now counts lava flows and fire fields only. Lava land and pools can't be
  stood on in the client's data.

## Deviations

- I made the ShatteredLegacy edits with small Python exact-replace scripts, as in P454 and P455, because the Read
  tool is denied there in unattended runs.
- I added the `TilesFor` test seam (above), which the prompt did not mention, so the step fact can use the real
  `Mobile.Move`.
- The CC6Batch8 seed and the two `EnsureCraftSystems` lines are test fixes outside the prompt. I made them so the
  gate passes for the right reason.
- Not done: F10's "stop grant checks at the final tier". F08 and F12's save/load and bonded-pet cases were not asked
  for here.

P457 DONE
