# P371: graduation is the first loop

Chase's decision, 2026-10-21: New Haven island is loop 0, maximum level 50. Graduation is the first real loop,
records loop 1, raises the future maximum level to 100, and permits leaving the island. Young lasts to its hours
limit and is not ended by graduation. The loop demonstration remains a vision.

## Documentation promotion (docs are read-only in this lane)

For F-12, F-5, F-35 and the tutorial entries in `docs/feature-queue.md`, promote this dated line:

> Chase 2026-10-21: New Haven island = loop 0, max level 50; tutorial graduation = loop 1, max level 100.
> Young lasts to its hours limit and is not ended by the graduation loop. Leaving the island requires graduation.
> The 2026-10-03 ladder continues +5 per loop from loop 2 (105) to loop 21 (200).

P80's row 4 is corrected, along with its superseded test expectation and loot-box loop placeholder note.
No files under docs are edited, per the explicit lane instruction.

## Patch alternatives, recorded before writing the patches

- Region OnMoveInto handles walking but does not veto MoveToWorld. Region exit notifications are too late.
- Per-route patches alone leave new teleporters and help transports free to bypass the gate.
- PlayerMobile already overrides MoveToWorld and SetLocation. Small guards there cover the shared movement paths
  without a core-project patch or copied upstream movement logic. Allow Map.Internal for logout/deletion.
- SpellHelper.CheckTravel adds an early refusal for recall, gate and teleport destinations (before resources and
  pets move), and Mark. PlayerMobile.CheckSpellCast also refuses Mark immediately. Island-local travel stays usable
  for P289's travel trial; its loop station still only runs the vision.
- BaseBoat needs a preflight in both Move and Teleport. Vetoing only a passenger's SetLocation would let the boat
  sail out from under them. Preflight every passenger before packets or any entity moves, including passengers on
  someone else's boat and the legacy Teleport movement route.

Source checked: pinned `Projects/UOContent/Mobiles/PlayerMobile.cs` MoveToWorld/SetLocation (1829/1836),
`Spells/Base/SpellHelper.cs` CheckTravel (612), `Multis/Boats/BaseBoat.cs` Move/Teleport (1667/1852),
`Engines/Help/StuckMenu.cs` TeleportTimer, and `Items/Misc/Teleporter.cs` DoTeleport (220).
The three patches apply after the climbed-tile CheckSpellCast patch; recheck all these on a pin bump.

## Implemented behavior

- Per-character loop count is stored in the existing account `FlagValues`, key `character:<uint serial>:loops`.
  No account schema change. Missing record means loop 0. The ordinary account serializer persists it.
- `ClusterFLoops.Graduate` records loop 1 through `CompleteLoop`. Completed loop numbers are monotonic and
  idempotent: repeat graduation or later remedial graduation cannot rewind or award the first-loop box twice.
  Loot boxes now read this loop count instead of the old global loop-1 placeholder.
- Graduation retains the existing Explorer tier-1 reward and starter-pet offer, in addition to the real Loop box.
  The loop fanfare uses the existing capstone path. The vision changes no progression or Young state.
- Removed loop-triggered `RemoveYoungStatus` entirely, including later loops: F-5 says time only; F-12 contains
  no later-loop Young-removal requirement. Existing hours expiry, voluntary renunciation and murder rules are unchanged.
- The tutorial is still once per account. At login, a character on an already graduated account receives its own
  first loop (including accounts graduated before P371); a skipped account gets that waiver only with option (a)
  enabled. Normal tutorial rewards are not replayed. Later loops are preserved.
- `clusterf.tutorial.islandGate` defaults true. Players at loop 0 may move within Haven island, but an exit says
  `System: Graduate with the League recruiter in New Haven before leaving the island.` Staff are exempt.
  Internalization remains possible for logout/deletion. No settings are changed on a running shard.
- **Island includes its underground tutorial space.** F-35's step 8 and the existing Rootdeep teleporter require
  access before graduation. `OldHavenBurrowsRegion.Area` is off-map (5136..5247,1128..1263) but under Old Haven, with
  its entrance at 3619,2620. It is treated as island space in both directions; a loop-0 player inside it still
  cannot recall/teleport to the mainland. Surface bounds are pinned Haven Island (3314,2345,500,750), Trammel only.
  The Vault is inside the Burrows rectangle, so its tutorial route stays available too.
- P289's prompt was read (`D:\UO\cc-prompts\queue\cc-P289-tutorial-core-trials-playable.md`). No branch merges or
  trial build are attempted here. Island-local travel, the dungeon and the vision remain usable by its trials.

## What F-12 must build

`MaxLevelFor(loop)` is a ladder hook only: 0 -> 50, 1 -> 100, 2 -> 105, ... 21+ -> 200. It does not touch skills.
`ResetLevelAndSkillsForF12` is the clearly named, currently empty integration point called before a new loop is stored.

F-12 still needs actual per-character level/XP and peak/reserve storage; XP earning and the revised ladder's curve;
level reset to 1 at every real loop; Keeper/Breaker skill resets and peak memory/echo rules; application of individual
skill caps from max level (and the agreed unlimited total cap); eligibility, scroll gates and confirmation for later
loops; level-gated gear/content; Legacy rewards, titles and loop achievements. Wire evo pets' `OwnerLoopsSource` to
the real counter when that integration is built (it remains its existing placeholder here). Do not treat the loot
system's skill-total-derived `LevelOf` as the new player level. Current flat skill caps are untouched.

## For Chase (nonblocking)

Should skipping count as graduating (a), or must skippers finish remedial training (b)? Implement (a) provisionally
behind `clusterf.tutorial.skipCountsAsGraduation` (default true). False leaves a skipper at loop 0 until remedial
graduation. The skipped achievement/state remain available for the remedial path.

## Validation and remaining work

Pinned source verified at `d4531cd94b739613155225c234900de9f47d2c88`. No Haven connection, deployment, account operation
on a running shard, commit, merge, push or branch switch. VERSION is `2026.10.21.21`, with a CHANGELOG entry.

### Local test route and its limits

Docker and the Git Bash runtime are unavailable to this sandbox (Bash fails CreateFileMapping, Win32 error 5).
Instead, archived pristine pinned source into ignored `ShatteredLegacy/server/lib/p371-build/tree`, installed the
canonical customizations/tests/migrations/replacements, and matched each patch's full context in build-script order.
Applied the build script's Lumberjacking partial-class structural fix too. Scratch was proven ignored with
`git check-ignore server/lib/p371-build/probe.txt` before producing large output. Pinned and `server/uo` were never
used as writable build trees.

Compiled with local SDK 10.0.201 and ran actual xUnit tests on Windows. Every PowerShell helper was invoked with
`powershell.exe -NoProfile -ExecutionPolicy Bypass -File ...` (5.1). Local compilation needs `-m:1 -nr:false
-p:UseSharedCompilation=false` in this sandbox.

**Local-only dependency exception:** offline NuGet has Pkcs 10.0.0, not the canonical security pin 10.0.13. Only the
ignored scratch `Directory.Build.targets` used the cached version, with audit disabled for offline restore. The
repository security pin is unchanged. This local run is useful behavior/compile evidence, not the official build.
No client MUL files were supplied to this run.

### Red then green

Tests live in `server/tests/Tutorial/GraduationLoopVerification.cs` (25 expanded cases), plus the revised
`server/tests/Misc/TutorialVerification.cs`. The new cases cover loop persistence/idempotence, Young, actual
Moongate.UseGate and Teleporter.DoTeleport, the shared movement paths used by recall/help/facet travel, actual
SpellHelper destination checks and Mark casting, actual BaseBoat passenger enumeration/Teleport with a fake
footprint, settings, remedial graduation, staff, internalization, island-local travel, the Rootdeep annex and ladder.
The help UI/timers and a live sailing boat were not exercised; their shared movement paths and source call sites were.

- Before implementing the new APIs, the pinned-source test build went red on their absence. It also exposed an
  invalid Assert.Single call on ModernUO's ref-struct item enumerator, corrected to a foreach count.
- With scratch-only baseline mutations (no graduation/skip loop calls, no gate, broken cap hook), the 30-case focused
  run failed **22**, passed 8. This catches the required loop, skipper, exit, spell, boat and ladder assertions.
- A second scratch-only mutation removed staff/setting/local-move exemptions and restored loop-triggered Young
  removal; its five selected cases all failed. The added dungeon test was also observed refusing the landing before
  extending the island domain. Thus every new expanded case was observed red.
- Restored canonical code, including Rootdeep in the island domain: **47 passed** across these files:
  `Tutorial/GraduationLoopVerification.cs`, `Misc/TutorialVerification.cs`, `Tutorial/TutorialFarmVerification.cs`,
  `Regions/RootdeepWayInVerification.cs`, `Misc/YoungPlayerVerification.cs`.
- The broader run caught a new side effect: LoopOf used GetOrCreate during movement. Changed it to the existing
  read-only Get accessor. `StaffHubVerification.ThePanelShowsTheFixtureCharactersValuesAndCreatesNothing` was
  observed failing, then passing after this fix.
- Existing region/trap fixtures assumed trainees could teleport to the mainland. Updated
  `Regions/OldHavenNewPlayerSafeVerification.cs` to leave the training region for the island plaza,
  `Items/Traps/DeployableTrapsVerification.cs` to test practice-net crumbling on the island surface, and
  `Regions/OldHavenBurrowsRegionVerification.cs` to use real loop-1 player fixtures for its independent region
  travel/refusal rules. All affected cases were observed red first. No island-gate disabling was added to fixtures.
- Final compatibility filter: **74 passed**, zero failures, zero compiler warnings/errors. Files:
  `Tutorial/GraduationLoopVerification.cs`, `Misc/TutorialVerification.cs`, `Regions/OldHavenBurrowsRegionVerification.cs`,
  `Regions/OldHavenNewPlayerSafeVerification.cs`, `Misc/StaffHubVerification.cs`,
  `Items/Traps/DeployableTrapsVerification.cs`.

The tested scratch copies of the loop, tutorial and gate implementations and new tests were compared to their
canonical files after restoring mutations. All matched. The three new patches passed `git apply --check --reverse
--ignore-whitespace` against the assembled tree. Both repositories passed `git diff --check`; all changed/new tracked
candidates are below 5 MB.

### Broad run: local limits, not a green full gate

Final actual shard-test run: **2,093 passed, 4 skipped, 13 failed, 2,110 total**. TRX evidence (ignored scratch):
`server/lib/p371-build/results/p371-local-final.trx`; stdout `final-tests.log`. Remaining failing files/cases:

- `TypeIdentity/TypeIdentityVerification.cs`: EverySpawnableTypeResolvesToItselfByShortName,
  EveryTypeResolvesToItselfByFullName, TheOursClassifierKnowsOursFromPinned, and the two D35_OursAreGoneAndPinnedsRemain
  data cases. All explicitly require Docker's `/customizations` staging path, absent here.
- `Misc/CommandDeclarationVerification.cs`: EveryCommandWeRegisterDeclaresACategory,
  AWorldCommandDeclaresRerunShardAndDryRun, ADeclaredDryRunIsAWordOfItsUsageAndAStringItsClassReads,
  TheCompiledRegistrationsAreTheOnesInTheSource, PlayerAccessAndThePlayerCategoryAreTheSameCommands. Same absent path.
- `Misc/SmithGuildNameVerification.cs`: NoCustomizationSourceNamesTheOldGuild. Same absent path.
- `Misc/ShardStatusPublisherVerification.cs`: TheFileIsReplacedWholeNeverRewrittenInPlaceAndLeavesNoTemp. Windows
  sandbox UnauthorizedAccessException from File.Move, outside this change.
- `Misc/LootBoxFanfareVerification.cs`: TheDataFilesRoundTripAndABadOneIsRefusedWhole. Its LF-specific JSON string
  replacement leaves JSON the unchanged parser accepts. Windows JSON line endings are the inferred cause; this
  unrelated parser test was not changed here.

The local broad suite is not claimed green. The **required official Lane-Build.ps1 / docker/uo/build.sh gate was not
run here**, as expressly delegated by this task: the Golem runs patches, compile and every shard test after DONE,
before accepting a commit. Linux behavior and an in-client play-through remain unverified here.

Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE set to these work copies; raw report is ignored scratch
`server/lib/p371-build/progress.txt`. That tool writes `tools/progress.json` even in dry-run; kept its generated update
per the working agreements. No README or docs files changed.

P371 DONE
