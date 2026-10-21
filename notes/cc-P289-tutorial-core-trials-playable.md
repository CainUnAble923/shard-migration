# P289: tutorial core trials, implemented but awaiting the official gate and real play-through

2026-10-21, Valorite Codex lane. Both work copies were clean at entry. No commits, branch changes,
Haven access, live configuration changes or deployment. This is the notes path specified by the
Golem wrapper; it supersedes the shorter filename inside the embedded task.

## Evidence and scope

Read both AGENTS.md files, direction-decision.md, tasks.md, P80 in full, F-35, F-12, P276,
and every rule in map-building-playbook.md. P276's farm code and map patch are present in this branch;
its note says placement/playtesting was deferred to P372 after a boot failure. No P282 implementation
or note was found in this work copy. The actual source still has loot-box LoopProvider defaulting to
1 (LootBoxes/ClusterFLootBoxes.cs) and EvoPet.OwnerLoopsSource defaulting to 0 (Mobiles/Evo/EvoPet.cs).
This task does not invent a loop persistence/reset implementation.

## Implemented

- The action-evidence model and nine handlers: core.movement, core.paperdoll, core.backpack, core.chat,
  core.death, core.banking, core.travel, core.league, core.loop.
- Per-character trial sessions, one timer each; hints and quest arrows; reset; exact-instance practice
  supplies; cleanup on completion/skip/graduation/relog/disconnect. Completed keys stay in TutorialRecord.
- Test-only placement extends ClusterFSeedTutorial, includes the P276 farm, and preflights the actual
  map with CanFit. It refuses on live and on an unpatched farm map. Placement has NOT run on a world.
- Optional unbuilt wings say coming soon and no longer award completion for opening their plan page.
- Character ownership checked before account tutorial actions; live cannot enable login entry through Configure.
  The gate reads testCenter.enable directly, avoiding Configure-order dependence on TestCenter.Enabled.
- Graduation's player UI sends the player back to Rook in town, where the graduation box can be opened.
- Practice bags reject items, so lesson cleanup cannot consume a player's belongings. Practice supplies disappear
  after their lesson and abandoned supplies delete after loading a save; ordinary player items are never selected.
- Young death recovery: pinned PlayerMobile.OnDeath calls YoungDeathTeleport before PlayerDeathEvent.
  That sends a New Haven Young ghost to Old Haven (3665,2587,0). The tutorial death event returns only
  its echo's victim to the farm healer; it does not toggle Young. Tested with fake players, unverified in a running shard.

## Verification

- Native .NET 10, source-linked isolated xUnit project under tools/playtest-bot/cache/p289 (git-ignored,
  proven with git check-ignore): nine positive cases observed failing against Observe=false, three
  ordering cases observed failing against an intentionally permissive Observe; correct implementation
  passes all 12 cases. Canonical test file: server/tests/Tutorial/TutorialTrialProgressVerification.cs.
- This isolated suite exercises the real TutorialTrialProgress source. It does NOT prove engine hooks,
  NPC placement, or a real client play-through.
- Docker daemon probe failed: permission denied at npipe:////./pipe/dockerDesktopLinuxEngine.
- The required docker/uo/build.sh invocation was attempted via the installed Git Bash; Bash itself
  failed with CreateFileMapping Win32 error 5. No Docker image was built and no shard was started.
- Supplementary native compilation succeeded in an ignored copy of the pinned source. It is
  NOT the required gate: MSYS is unavailable, so the scratch overlay uses native git apply plus exact
  full-context replacements for historical patches git rejects; it also uses the cached Pkcs 10.0.0
  with audit disabled ONLY IN SCRATCH because the official 10.0.13 dependency is not cached and this
  environment has only offline NuGet feeds. Canonical security/package settings are untouched.

The source-linked isolated test project uses the locally cached xUnit packages. The full native source build uses
Windows .NET SDK 10.0.201; the official Dockerfile uses 10.0.203. All PowerShell scripts ran in powershell.exe 5.1.
Native tests needed Distribution/Data copied into their output folder and the existing Windows libdeflate.dll;
these changes are only inside the ignored scratch folder. No test-host or dependency changes ship in either repo.

### Red then green

| Source / case | Observed red | Observed green |
|---|---|---|
| TutorialTrialProgressVerification.cs: nine core completion cases | Observe always false: 9 failures at Assert.True(trial.Done) | 9 pass |
| Same file: movement/death/vision ordering cases | Observe accepts every action: 3 failures at Assert.False | 3 pass |
| TutorialVerification.cs: ResetClearsEvidenceAndReplacesSuppliesAndAnotherCharacterCannotUseTheRecord | Omitted Cancel in Reset: old and new session are the same instance | pass |
| TutorialVerification.cs: BagSpeechBankLeagueAndTimedVisionObserveTheRealHooksWithFakePlayers | Omitted OpenedBag evidence: core.backpack missing | pass |
| TutorialVerification.cs: SeederRefusesLiveAndUnpatchedMapsAndIsIdempotentWithAFakeMap | Disabled the live refusal: expected Test world only, got map preflight refusal | pass |

The latter three breaks were made ONLY in the ignored source copy, then restored from canonical files. All Tutorial
source copies were checked by SHA-256 after restoration. One initial red-mutation attempt failed to compile because
its comment consumed a closing brace; corrected before the three assertion failures above. It is not counted as a red proof.

**Focused native result: 26 passed.** The files are:

- server/tests/Tutorial/TutorialTrialProgressVerification.cs (12 theory cases).
- server/tests/Misc/TutorialVerification.cs (9 facts, including the original entry/save, skip/remedial, account
  ownership, vision/no-progression-change, creature engagement, and graduation tests).
- server/tests/Tutorial/TutorialFarmVerification.cs (5 existing P276 facts).

The expanded action-hook fact drives ALL nine adapters with fake PlayerMobile/NetState objects: moves across both
marks and advances ShardTestClock; equips the supplied cloak (the fake host's missing tiledata layer is supplied
explicitly); opens the supplied bag (a stranger cannot finish it); sends wrong and correct speech; accepts the actual
death-echo gump and dies, invokes the real death event handler (the curated test fixture does not register generated
player events), and accepts the actual healer's resurrection gump; deposits the actual practice token into BankBox;
uses the actual gate with a fake destination-fit check (blocked first, then clear); talks to the actual League
Registrar from afar and then nearby; watches the actual timed vision. The normal core and skip/remedial/graduation
paths also run through the shared action-evidence boundary with fakes. These are NOT a real player play-through.

Seeder tests prove live refusal, missing-map-patch refusal, blocked-placement refusal, dry-run nonmutation and
idempotence with a FAKE map-fit predicate. They do not verify the physical tiles in the test world's map.

**Broader supplementary native result: 2,069 passed, 27 failed, 4 skipped (2,100 cases). This is NOT a green gate.**
All tutorial cases passed. Confirmed limitations of this route include tests requiring the builder's absolute
/customizations path and historical quoted-path patch hunks that the supplementary overlay did not install.
The latter leaves some BOD UI hooks absent in scratch. The other failures were not fully triaged; no claim is made
that canonical main has these failures. Do not replace docker/uo/build.sh with this supplementary route.

The failed case list (from native-full.log, ignored scratch) is:

```
TypeIdentityVerification.EverySpawnableTypeResolvesToItselfByShortName
TypeIdentityVerification.EveryTypeResolvesToItselfByFullName
TypeIdentityVerification.D35_OursAreGoneAndPinnedsRemain [GauntletsOfAnger; ShroudOfDeceit]
TypeIdentityVerification.TheOursClassifierKnowsOursFromPinned
BulkOrderSystemVerification.AutomaticBanksAtOnceAndTheDeedGumpCyclesTheMode
BulkOrderCraftsVerification.TheBookStoresTheCraftFiltersByItAndRebuildsTheDeed [Carpentry; Alchemy; Cooking; Inscription; Fletching; Tinkering]
BulkOrderCraftsVerification.TheChefsApronAddsItsBonusToTheExceptionalChance
BulkOrderCraftsVerification.TheSmithMetalFiltersNoLongerShowTinkeringDeedsAndTheBookKeepsAJewelsGem
SmithGuildNameVerification.NoCustomizationSourceNamesTheOldGuild
ShardStatusPublisherVerification.TheFileIsReplacedWholeNeverRewrittenInPlaceAndLeavesNoTemp
PostValoriteDeedMaterialLineVerification.EveryPostValoriteDeedNamesItsMetalInGumpsAndTooltips
LootBoxFanfareVerification.TheDataFilesRoundTripAndABadOneIsRefusedWhole
LargeBODItemFillVerification.ContainedItemsFillAMixedBag
CommandDeclarationVerification.ADeclaredDryRunIsAWordOfItsUsageAndAStringItsClassReads
CommandDeclarationVerification.EveryCommandWeRegisterDeclaresACategory
CommandDeclarationVerification.AWorldCommandDeclaresRerunShardAndDryRun
CommandDeclarationVerification.TheCompiledRegistrationsAreTheOnesInTheSource
CommandDeclarationVerification.PlayerAccessAndThePlayerCategoryAreTheSameCommands
BODCombineContainedVerification.BothGumpsCarryTheButtonAboveExit
BODCombineContainedVerification.ALargeDeedTakesItsSmallDeedsFromABag
BODCombineContainedVerification.ASmallDeedFillsFromABagAndLeavesTheWrongMaterialBehind
```

## For Chase

Defaults from the task, retained pending Chase's choices:

1. Rook Hallowell remains the recruiter at Trammel 3500,2572,14.
2. System: voice, short server chat/gump text.
3. Required core first, optional wings afterwards.
4. Explorer's tier 1 graduation box.
5. Live tutorial entry stays off. Placement is test-world only.
6. Server-driven hints only; no client patch added by P289.
7. Loop placeholder discrepancy remains unresolved: loot boxes use 1; evo pets use 0. F-12/P282 has
   not supplied a unified source in this branch. The vision never changes skills, levels, loops or Young.

## How to play it (proposed; not yet play-tested)

On a test world with the P276 map patch, use an Administrator from GolemTestAccounts:
`[ClusterFSeedTutorial dryrun`, then `[ClusterFSeedTutorial`. Repeat to check zero new placements.
Enable tutorial.enabled on that test world before the fresh player's first login. No live edits.
Use normal character creation for a fresh New Haven character under the Golem's player account; the kit's
pre-created Green Acres starter is not a substitute for the first-login test. If this pool account already
started the tutorial in an earlier test, reset only its tutorial record on the test world before this run.
Start at New Haven 3503,2574,14 and double-click Rook (3500,2572,14). Choose the first core lesson.
Each done page offers the next lesson; Rook can reopen any unfinished one.

1. Walk onto 3499,2571,14, then 3501,2571,14.
2. Open your paperdoll, drag the practice cloak onto it (remove an existing cloak first).
3. Open the backpack, then double-click its blue practice bag.
4. Say `I am ready to learn` in ordinary local speech.
5. Follow the arrow to the farm gate. Double-click the death echo at 3402,2617 and explicitly accept.
   As a ghost double-click Sera at 3402,2613 and accept resurrection.
6. At the New Haven banker (the seeder's canonical BankAnchor, 3492,2577,15), say `bank` and
   drag the practice bank token into the actual bank box.
7. Double-click the blue tutorial gate at 3402,2615; it returns you to 3501,2572,14.
8. Double-click Elara Voss at 3459,2601,18. Joining is optional; reading the League page is the task.
9. At the farm's vision marker (3402,2619), double-click and remain nearby until the final System line.
Then return to Rook on the plaza, double-click him and Graduate. The final done page points back to him.
Wings are optional.
For the skip path, use Rook's Skip and both confirmations. Speak to Rook again for Remedial training;
complete the full core and graduate. A real run must use player actions, not staff completion or fakes.

## Map playbook checklist

| Check | Result |
|---|---|
| Terrain, walls, corners, doorframes, transitions, furniture rows, junction sheet | Not applicable: P289 changes no map files or architecture. P276's farm remains its existing addon/layout/patch. |
| Loaded map and passability | Runtime CanFit preflight implemented. Actual server-map placement is UNVERIFIED. |
| New obstacles or permanent decor | No new architecture. Stock marker and moongate graphics; marker tiledata refusal implemented. Actual route clearance is still UNVERIFIED. |
| Farm hook and spawn ranges | Existing P276 farm seeder reused, not rewritten; existing farm tests pass locally. |
| Repeat seeding | Green with fakes; actual test-world repeat is UNVERIFIED. |
| Client pictures / real System log | Unavailable: no current-build test world was started. Fake test logs do not substitute for this. |

## Files and handoff

New implementation files: server/customizations/Tutorial/TutorialCoreTrials.cs,
TutorialCorePlacement.cs, TutorialTrialProgress.cs. New test file:
server/tests/Tutorial/TutorialTrialProgressVerification.cs. Existing framework and Registrar changes are in the git
diff, with the expanded server/tests/Misc/TutorialVerification.cs. CHANGELOG.md and VERSION are 2026.10.21.21;
the staff line explicitly says test-world validation is still needed.

Ran progress.py with SL_SHARD and SL_MIGRATE set to these work copies. It refreshed README.md, dashboard.html and
tools/progress.json in the migration work copy. No docs/ edits. Scratch is tools/playtest-bot/cache/p289, proven
ignored with git check-ignore (including the compiled UOContent.dll, which exceeds 5 MB). No large tracked output.
Final verification: all Tutorial implementation files, LeagueRegistrar.cs and TutorialVerification.cs match the
compiled scratch sources by SHA-256. Both git diff --check runs passed (only a normal CRLF normalization warning
for TutorialRecruiter.cs). Every changed/untracked non-ignored file in both work copies was checked below 5 MB.
The final focused run on the final compiled code passed all 26 cases again. No source changes followed it.

## Remaining / blocker

Implementation and focused fake tests are complete. The official build gate and REAL play-through are NOT done.
Resume in an environment permitted to run Git Bash and access the local Docker daemon:

1. Run docker/uo/build.sh -t sl-modernuo:cc-p289 with its actual patch/test gates; resolve any real failures.
2. Under the test-shard lock, start an isolated loopback-only test world with scratch saves using that image,
   the P276 map overlay, and GolemTestAccounts. Do not touch Haven or live.
3. Seed dry-run, actual, then repeat; verify the physical marker/NPC tiles and walking routes against the playbook.
   If preflight refuses a tile, inspect it and fix the placement rather than bypassing CanFit.
4. Use a FRESH test-account character to play all core lessons, skip, return for remedial and graduate. Save
   screenshots if supported, otherwise the real System lines and state changes. Verify guarded-town box opening.
5. Record that evidence here and only then mark P289 DONE.

No Golem test-account credentials were read or changed. Ask-Chase.ps1 was not invoked: it persists a question in
D:/UO/golem, outside the wrapper's two writable work copies. The blocker requires an execution environment change,
not a tutorial design decision. The draft remains uncommitted for the Golem to handle.

P289 STOPPED: Docker/Bash permissions block the official build gate and required real test-world play-through.
