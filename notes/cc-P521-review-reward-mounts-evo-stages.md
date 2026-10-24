# P521: review of reward mounts and evo stages (P365)

Reviewed October 24, 2026. Notes only. No code or tests changed.

P365 commit `51d04230744a23fd4fa9d66078e5cf9ebca9794d` is an ancestor of local
`main`, merged by `6f540be`. The reviewed mount, evo, and test files match main.
Read `cc-P365-reward-mounts-and-evo-stages.md` and its `cc-P365-tools/p365_art.py`
first. No separate P365 review was present. The implementation note's known
limitations, including client rendering, existing windrunner choices, placeholder
stats, and acquisition decisions, are not new findings here. P514's already
reported owner-loop and Bond Trial gaps are also not repeated.

## Findings

Paths below are relative to the ShatteredLegacy work copy. These are source
findings; no running-world reproduction was performed.

1. **bug**: `server/customizations/ClusterFAchievements.cs:617` (also `:479`,
   `:706`, and `:1129`). Adding mount items to already existing achievements
   leaves prior earners without their mounts. For example, an account that
   earned `combat.undead_hunter` before P365 cannot receive its bonewalker by
   killing more undead or logging in: `TryGrant` returns at `:1340` for an
   already earned key, before reward delivery at `:1347`, and there is no
   separate reward claim or backfill path. Add a persisted, per-account claim
   record for these rewards and deliver unclaimed mounts to existing earners
   without granting AP or Renown again; test an old earned record and repeated
   login/claim attempts.

2. **bug**: `server/customizations/Mobiles/Evo/EvoPetData.cs:154` and `:168`.
   Horse and Lizard introduce multiple body choices at stage 1, but a player
   given either pet cannot choose its initial body. Construction uses the first
   body, `EvoPet.GivePet` opens only the hue picker (`EvoPet.cs:492`), and both
   evolution and double-click offer body choices only for a later stage
   (`:298`, `:453`); the other foals and hatchlings remain available only through
   staff tools. Offer the current stage's unmade body choice when the pet is
   given or double-clicked, and apply that choice to its current body; exercise
   the owner gump flow for each initial choice instead of `StaffSetStage`, which
   is what `RewardMountVerification.cs:179` currently tests.

3. **risk**: `server/tests/Mobiles/Mounts/RewardMountVerification.cs:147`.
   The persistence check serializes only the stabled mount while its original
   mount item remains registered, then checks body and item ID. Entity reads
   resolve serials against the existing world, so this does not prove that the
   mount item and ownership reconnect after a reload; unused statuettes and
   their serialized `MountKey` are never round-tripped either. Add an isolated
   save/load case restoring the rider, mount, mount item, and stable membership
   together, plus an unused-statuette reload followed by exactly one successful
   redemption. This is missing coverage, not evidence of a reproduced save-loss
   or duplication bug.

## Checks with no additional finding

- **Mount bans:** no bypass found. `RewardMounts.cs:200` derives from `BaseMount`
  and supplies no alternate riding entry point. Pinned
  `Projects/UOContent/Mobiles/Animals/Mounts/BaseMount.cs:211` calls the shared
  guard; `:283` checks the active region, mount block, and gargoyle restriction.
  The statuette calls a following creature, not a rider assignment. Pinned
  `Projects/UOContent.Tests/Tests/Mobiles/MountRegionTests.cs:28` already covers
  this inherited path using a horse.
- **Stage skips or repeats:** none found in the new enabled stage sequence or
  `NextEnabled`/`TryEvolve` loop. The initial-choice bug above is separate from
  stage advancement. The new horse and lizard test uses staff stage changes,
  so it does not establish normal XP, loop, Bond Trial, and owner-pick behavior
  for those lines; the existing dog test exercises that shared mechanism.
- **Double claims:** no player-accessible duplicate path found in source.
  Achievement keys are inserted before delivery (`ClusterFAchievements.cs:1340`),
  successful statuette use deletes the item (`RewardMountStatuette.cs:58`), shop
  purchases charge Renown, and loot-box opening clears its stored contents.
  Buying another statuette with another payment is allowed. Runtime replay and
  restart behavior remain unverified.
- **Missing package IDs:** none found in the committed P365 sources. A read-only
  Python check matched every listed body file's SHA-256 to its registry row,
  found each bodyAnims entry and mount-layer tiledata record, and found every
  listed PNG. VD index inspection found the full low-layout action range on
  the new horse/lizard bodies; the movement-only saddle files are used only as
  ridden looks. `Build-PlayerPackage.ps1:815` rebuilds and checks the animation
  binaries before staging. No distributable package was built or inspected.

Pinned ModernUO was verified at `d4531cd94b739613155225c234900de9f47d2c88`.
Its `Projects/Server/Serialization/SerializationExtensions.cs:32` resolves
entity references by serial, which is why finding 3 distinguishes an object
round-trip from a world reload.

## Reviewed file inventory

The P365 commit lists 71 files: these 19 text files and the 52 binary source
files enumerated below. Related shared code was also traced in EvoPetGumps,
EvoPetCommands, LeagueShopGumps, LootBoxItems, the package builder/encoder,
and pinned BaseMount and serialization code.

```text
CHANGELOG.md
VERSION
player-package/tests/Build-UoOverrides.Tests.ps1
player-package/tests/Cliloc-Overrides.Tests.ps1
player-package/vendor/shattered-legacy-art/SOURCE.txt
player-package/vendor/shattered-legacy-art/records.json
player-package/vendor/shattered-legacy-art/registry.csv
server/customizations/ClusterFAchievements.cs
server/customizations/LeagueShop/LeagueShop.cs
server/customizations/LootBoxes/LootBoxRoller.cs
server/customizations/Mobiles/Evo/EvoPet.cs
server/customizations/Mobiles/Evo/EvoPetData.cs
server/customizations/Mobiles/Evo/ShardBodyTypes.cs
server/customizations/Mobiles/Mounts/RewardMountStatuette.cs
server/customizations/Mobiles/Mounts/RewardMounts.cs
server/tests/Misc/LeagueShopVerification.cs
server/tests/Mobiles/Evo/EvoPetVerification.cs
server/tests/Mobiles/Mounts/RewardMountVerification.cs
server/tests/Tutorial/TutorialFarmVerification.cs
```

Under `player-package/vendor/shattered-legacy-art/anim-src/bodies/`, the 34
checked `.vd` filenames are:

```text
2088.vd 2089.vd 2090.vd 2091.vd 2092.vd 2093.vd 2094.vd 2095.vd
2096.vd 2097.vd 2098.vd 2099.vd 2100.vd 2102.vd 2104.vd 2105.vd
2106.vd 2108.vd 2109.vd 2110.vd 2111.vd 2112.vd 2113.vd 2114.vd
2115.vd 2118.vd 2119.vd 2125.vd 2126.vd 2129.vd 2130.vd 2131.vd
2132.vd 2133.vd
```

Under `player-package/vendor/shattered-legacy-art/art/`, the 18 checked PNG
filenames are:

```text
46672.png 46673.png 46674.png 46675.png 46676.png 46677.png
46678.png 46679.png 46680.png 46681.png 46682.png 46683.png
46684.png 46685.png 46686.png 46687.png 46688.png 46689.png
```

## Verification limits

Lane tests: none requested. No tests were added or run, and no build, client
session, or save/load probe ran. The existing test assertions were reviewed;
P365's reported green gate was not rerun. Asset checks above inspected committed
sources, not the installed client or a published package. No Haven connection,
deployment, account change, commit, merge, push, or branch switch occurred.

`tools/progress.py --dry-run` completed with `SL_SHARD` and `SL_MIGRATE` set to
these work copies. Its generated `tools/progress.json` was restored to its
starting bytes to keep this review notes-only.

P521 DONE
