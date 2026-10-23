# P484: review of climbing boots (P278 / P238)

Reviewed October 23, 2026. Notes only. These are source review findings, not reproduced player reports.

Read both working agreements, the direction decision and task list, `notes/cc-P278-cont-fixup-climbing-boots.md`, and its implementation note, `notes/cc-P238-climbing-boots.md`. No separate P278 review was found beside them; P379's merge review explicitly excludes P278. The findings below do not repeat the implementation note's open client checks or recorded design choices.

Code paths below are relative to the ShatteredLegacy work copy. Pinned paths are relative to `D:/UO/ModernUO-pinned`, verified at `d4531cd94b739613155225c234900de9f47d2c88`.

## Findings

1. **bug** | `server/customizations/ClusterFClimbing.cs:187` and `:110`: On a real mountain, the current-tile probe includes mobile collisions, so the climber's own body makes the tile Blocked instead of Mountain, disabling the combat, taming, Mark and house-placement restrictions and preventing the normal Follow order when hopping down. Separate terrain classification from landing occupancy checks, excluding the querying mobile when recognizing its current footing while retaining destination collision checks, and add a real-terrain regression with a player standing on mountain land.

2. **bug** | `server/customizations/ClusterFClimbing.cs:289`: The destination call to `SpellHelper.CheckTravel` omits the player, which skips region-specific travel checks and can permit landings in staff areas such as GreenAcresRegion when range, footing and the other checks pass. Pass the player through `MayLandAt` to the player-aware overload, and test both ordinary hops and ledge returns against a BaseRegion that allows TeleportFrom but refuses TeleportTo.

3. **bug** | `server/customizations/ClusterFClimbing.cs:329`: Neither the common checks nor the target callback rejects Frozen or Paralyzed players, so a wearer can hop out of reach while immobilized, including by answering a target opened before paralysis. Reject both states when the hop resolves, and test ordinary hops and ledge returns without allowing movement, stamina loss or a new cooldown.

4. **risk** | `server/tests/Misc/ClimbingBootsVerification.cs:186` and `:381`: Movement tests call `TryHop` or `TryLedgeReturn` directly, leaving the boots' pending-target lifecycle untested when the boots are removed, deleted or upgraded, or the wearer dies before answering. Add tests through `ClimbingBoots.OnDoubleClick` and the resulting target callback that verify these changes cancel the hop without spending stamina or changing ledge memory.

## Evidence and existing coverage

- Finding 1: `MapClimbTerrain.Probe` calls `Map.CanFit` with `checkMobiles: true` at `ClusterFClimbing.cs:81` and `:110`; `IsOnClimbedTile` calls that same probe at `:189`. Pinned `Projects/Server/Maps/Map.cs:1000` checks every mobile occupying the body volume, including the querying player, and returns false at `:1007`. The restrictions all depend on `IsOnClimbedTile`, as does the hop-down pet branch at `ClusterFClimbing.cs:403`. The fake terrain at `ClimbingBootsVerification.cs:109` ignores occupancy; the real-terrain test at `:256` never asserts climbed status on occupied mountain land.
- Finding 2: Pinned `Projects/UOContent/Spells/Base/SpellHelper.cs:609` supplies a null caster for the map-only overload; `:634` only calls destination/current `BaseRegion.CheckTravel` when the caster is present. Pinned `Projects/UOContent/Regions/GreenAcresRegion.cs:26` refuses player travel, and GreenAcres is absent from SpellHelper's fixed validator list at `:83`. The existing refusal test at `ClimbingBootsVerification.cs:233` covers towns, dungeons and a house, which the separate type/house checks already reject.
- Finding 3: Pinned `Projects/Server/Mobiles/Mobile.cs:4140` refuses normal movement while paralyzed or frozen. Its item-use path at `:4934` and `Projects/Server/Targeting/Target.cs:146` do not supply that movement check; the boots instead reach `MoveToWorld` at `ClusterFClimbing.cs:391` through the common checks at `:329`.
- Finding 4: The callback already checks deletion at `ClimbingBoots.cs:103`, and `CheckCommon` rechecks deletion, the boots' parent and the wearer's life at `ClusterFClimbing.cs:331`. This is missing regression coverage, not a claim that deleted boots currently work.

## Requested checks with no additional finding

No broken-boots defect found: the boots intentionally have no durability (`ClusterFClimbing.cs:12`), inherit zero initial hit points from pinned `Projects/UOContent/Items/Clothing/BaseClothing.cs:322`, and do not override those defaults. Deleted boots are refused at target resolution and in the shared hop checks; adding a blanket zero-hit-point refusal would disable normal boots.

No additional direct house-entry or DungeonRegion-entry bypass found. Both hop paths share `Land`, which calls `MayLandAt`; that method rejects TownRegion, DungeonRegion, HouseRegion and a matching house at `ClusterFClimbing.cs:279` and `:284`. Finding 1 defeats the special house-placement refusal from a mountain, but does not itself remove these destination checks.

Also inspected the boots' binding, purchase, upgrade and recovery paths, mined-block recording and account serialization, Liaison and Logbook changes, patch registration, and the related tests named in P238's note. No additional finding from those paths.

## Verification and limits

No code or tests changed. No build, game server, client or test suite was run for this review; lane tests are none. Actual staff-area approach routes, gaps between live dungeon regions, mountain rendering and mining line of sight remain unverified. No Haven connection or deployment was made.

Ran `tools/progress.py --dry-run` with both work-copy path overrides. It unexpectedly rewrote `tools/progress.json`; restored that file byte-for-byte from HEAD and verified its diff was empty, keeping this task notes-only.

P484 DONE
