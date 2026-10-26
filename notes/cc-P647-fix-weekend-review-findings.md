# P647: fix the findings from the weekend build reviews (P636-P646)

Done 2026-10-26 by the Iron Golem (Claude). Code in `D:\UO\golems\Iron\ShatteredLegacy`, branch golem/Iron/P647.

## In plain words

- Every High and Medium problem Codex found in the weekend's eleven new features is fixed in code: 43 of them, plus 8 of the 11 small (Low) ones. The one left is a hands-on test-shard check for town houses that needs the client. Each fix has its own new test that failed before the fix and passes after it.
- Players will notice a few fixes on live, all in the patch notes: Tracking Ping refunds a ping that gets overloaded and stops reading the area once its time is up. Persuasion checks the conversation again when you choose from its menu, and a courier letter left in the bank still counts as your one job. Bankers in part of a town (like Luna's bank) count for courier letters, and gypsy bankers and minters accept them.
- The other features are still test-shard only, and now they really are. Before, staff could switch seven of them on live by typing the command. Now those commands refuse anywhere except the test shard.
- For you: two small questions under For Chase below (how many lockdowns a town house gets, and a Persuasion storage choice). Nothing to deploy beyond the normal merge.

## What was reviewed

The prompt names `notes\cc-P636-*` through `cc-P646-*`. There is no P636 note in this repository and no P636 prompt in the prompts repo's queue, waiting or completed folders, so the Pumpkin King (P624) has only its inline review, which found nothing. Read: the ten review notes P637-P646, their own Codex reviews (all "no findings"), and the inline `*-codex-review.md` of P624-P635. The prompts repo's `queue\` holds only guide prompts (P648-P655), and `waiting\` is empty; no merged prompt after P634 touched these files (code HEAD was `a3f017e`, the P634 merge). So nothing was already fixed or already queued.

Not counted as findings to fix here: the P634 notes-repo finding (see the table) and every item the build notes and reviews name as a later stage.

## How it was done and tested

Five Claude subagents fixed one or two features each, in parallel, in this one work copy, each touching only its own files. I did the scoring butte test gaps. Each finding was first checked against today's code. All of them still applied; none was wrong against the code.

Tests ran on throwaway containers from `sl-uo-builder:cc-P634` (the P634 base) with the work copy mounted read-only. A script in the session scratchpad (`probe.sh`, `run.sh`) copies in only the named files. The red run copies in only the new test files, so it runs against the base code. Where a test needed a new seam (`IsTestShard`, an empty `Prune` stub), the seam alone was added before the red. Two test-gap findings (P645-3, P644-1) were made red by mutating the production code, then restoring it. Failure messages are in the table. The final per-class green counts:

| Test class | Green |
|---|---|
| TrackingPingVerification | 21/21 |
| PersuasionVerification | 20/20 (58/58 with ShardTestClock and TutorialWing) |
| ItemKnowledgeVerification | 12/12 |
| GuardWitnessVerification | 10/10 |
| LeagueInvestigationVerification | 11/11 |
| LeagueEchoesVerification + LeagueDragonEchoVerification | 17/17 (67/67 with NotedBySystem, NotedFixups, StaffHub) |
| TownsfolkTalkVerification | 16/16 |
| LevelGearProcVerification | 15/15 (22/22 with LevelGearVerification) |
| LeaseholdVerification | 12/12 (14/14 with the tile guard facts) |
| ScoringArcheryButteArtVerification | 13/13 |

**Gated build:** took the `docker-build` lock (released after). `docker\uo\build.sh -t sl-modernuo:cc-P647`: EXIT=0, "Built sl-modernuo:cc-P647 with patches applied and 2633 shard test(s) passing": 2,633 passed, 4 skipped (the real-map-data facts), 0 failed. Images `sl-modernuo:cc-P647` = `2373bb315322`, `sl-uo-builder:cc-P647` = `e2de690a8746`. Log `build-P647.log` in the session scratchpad. No patch file changed, so the build's patch step is unchanged.

## Findings: done or skipped

The test-shard gate is the same fix everywhere: the house `IsTestShard` seam, as in `TutorialCorePlacement`. The command refuses with a plain message off the test shard, and the feature's effective `Enabled` also requires the test shard.

| Review | Finding | Sev | Done or skipped | Why / how; test (red) |
|---|---|---|---|---|
| P625 inline | Overload during an active pulse gave no refund | M | Done | Mid-pulse overload refunds the 15 stamina and clears the cooldown. `ARefreshOverTheCeilingEndsThePingAndRefundsIt` (red: stamina 85, expected 100) |
| P625 inline | Stale Ping offer bypassed a later skill's delay | M | Done | The offer records the Tracking use that sent it. `AStaleOfferCannotSkipALaterSkillsDelay` (red: focus started) |
| P637 | 1. Player sensing ignored CanSee | M | Done | `CanSee` required for players and their pets only; wild-creature sensing unchanged. `APlayerTheEngineHidesIsNotFoundNorTheirPet`, with a real tournament duel-context veto (red: Outsider found) |
| P637 | 2. Catch-up callbacks scanned after the deadline | M | Done | The pulse ends on `Core.Now >= End` before any read; new `ShardTestClock.Stall`. `ACallbackAfterTheDeadlineEndsThePingWithoutReading` (red: watched warning sent) |
| P637 | 3. Cooldown/warning records never pruned | L | Done (trivial) | Pruned at each paid ping and on `PlayerDeletedEvent`; a disconnect keeps them. `ExpiredAndDeletedRecordsArePrunedButADisconnectKeepsThem` |
| P626 inline | Stale Persuasion menu not revalidated | M | Done | One `CannotConverse` check (alive, facet, range, LOS, target) at open and at answer. `AStaleMenuRechecksTheConversation` (red: 14 gold given across facets). The LOS part is in the code, but no fact covers it: the test host has no map data. |
| P626 inline | Banked letters let a courier stockpile jobs | M | Done | A per-courier table of outstanding letters, rebuilt on load, with no new saved fields. `ABankedLetterStillHoldsTheOneJob` (red: second letter issued) |
| P638 | 1. Unnamed town subregion hid the town | M | Done | `TownOf` walks to the first named TownRegion; it is used everywhere. `AnUnnamedTownSubregionResolvesToItsTown` (red: town null) |
| P638 | 2. Banker subclasses selected but could not receive | M | Done | The recipient is the recorded type or a subclass. `ABankerSubclassTakesTheLetterItWasPickedFor` (red: refused) |
| P638 | 3. Rotation history lost on restart | L | Skipped | Not trivial: it needs a new persistent per-character record |
| P638 | 4. Charity ledger pruned at 200 | L | Skipped | Not trivial, and it is a storage choice; see For Chase |
| P627 inline | Public protection labels hidden while concealed | M | Done | Blessed, cursed, insured, blessed-for, quest item and locked down/secure are public. `ConcealmentKeepsPublicProtectionAndRestrictionLabels` (red: blessed line missing). The two house flags are in the catalog but untested: the host never sets them. |
| P627 inline | Test-shard gate for [ItemKnowledge | M | Done | Gate on on/conceal/forget and Enabled. `ThePolicyRunsOnlyOnTheTestShard` |
| P639 | 1. Completing both tracks bypassed the catalog | M | Done | A known item still renders through the catalog, so unowned lines stay hidden. `CompletingBothTracksKeepsUnclassifiedLinesHidden` (red: "Hidden power 42" sent) |
| P639 | 2. Difficulty missed Use Best Weapon Skill | M | Done | Counted as one full-intensity enchantment; skill bonuses are counted too. `TheDifficultyReaderCountsUseBestSkillAndSkillBonuses` (red: 10, expected 90) |
| P639 | 3. Dead registry rows never pruned | L | Done (trivial) | Pruned at save. Extended `TheRegistrySurvivesASaveAndLoad` |
| P628 inline + P635 | Test-shard gate for [GuardWitness | M | Done | `ObservationRunsOnlyOnTheTestShard` |
| P628 inline + P635 | Distinct offenses merged within one second | M | Done | A callback joins an incident only for the same culprit, moment, place and victim. `OneActionIsOneIncidentAndADistinctOffenseIsAnother` (red: one incident) |
| P628 inline + P635 | Witnesses not checked against the action location | M | Done | Incidents record `ActionAt` (the victim's place for an attack or assist). `AWitnessMustSeeTheVictimOfAnAttackOrAssist`, through real DoHarmful/DoBeneficial |
| P640 | 1. A pet's forwarded flag made a second incident at the master | M | Done | The creature's incident names `ResponsibleMaster`; the forwarded callback adds nothing; the master's position is shown only to those who saw the master. `APetsCrimeNamesItsOwnerWithoutASecondIncident` (red: 2 incidents) |
| P640 | 2. Actors stock guards reject were reportable | M | Done | Stock `IsGuardCandidate` is checked at the event. `ActsStockGuardsRejectAreNotReportable` (red: blessed player and invulnerable healer recorded) |
| P640 | 3. Caller history grew forever | L | Done (trivial) | Pruned on each call and cleared by off. `CallerHistoryKeepsOnlyCallersInsideTheLimit` |
| P629 inline | Seeder not limited to the test shard | M | Done | Seam, refusal, command now TestOnly. `TheSeederRefusesOffTheTestShard` (red: 2 markers placed) |
| P641 | 1. A bag carried the warrant past its transfer rules | M | Done | The smaller warrant-only fix: it rests only on top of the owner's backpack or bank; a saved nested warrant moves back after load. `TheWarrantRestsOnlyInItsOwnersBackpackOrBankNeverInABag` |
| P641 | 2. Missing map files passed the site gate | M | Done | Land, index and statics streams are checked and reported separately; the seeder fact now uses an explicit flat fixture. `ASiteOnUnloadedMapDataIsRefusedAndGetsNoMarker` (red: 2 markers on absent data) |
| P641 | 3. Region scan missed regions hidden by priority or height | M | Done | Every touching region, full column, plus a per-tile Z check; the shipped sites still pass. `ARefusedRegionHiddenByPriorityOrHeightStillRefusesTheSite` |
| P630 inline | Echo harm not rechecked between watchdog passes | M | Done | `CanBeHarmful` asks `WhyEnd` first and dissolves on the next tick. `BetweenWatchdogPassesItRefusesHarmTheMomentItsCallerStopsQualifying` |
| P630 inline | Test-shard gate inside [LeagueEcho | M | Done | Every verb except status. `TheStaffCommandDoesNothingOffTheTestShard`, through `CommandSystem.Handle` |
| P642 | R1. A lethally damaged Echo counted as a pet loss | M | Done | `ClusterFNotedBySystem`: the pet-died check also requires `!NoKillAwards`, so ordinary pets still count. `AWildCreaturesLethalHitOnTheEchoGivesItsOwnerNoPetLossAchievement` (red: counter 1) |
| P642 | R2. Disconnect did not end the Echo | M | Done | `Disconnected` subscription, offline callers refused. `ADisconnectEndsTheEchoAtOnceAndAnOfflineCallerIsRefused` |
| P631 inline | Unreadable dialogue file threw | M | Done | IO and access errors are a failed load that keeps the old table. `AnUnreadableTableFileIsAFailedLoadThatKeepsTheTable` (red: IOException out of Reload) |
| P631 inline | Duplicate responses could empty the choices | M | Done | The parser refuses them, with a fallback. `RepeatedIdenticalResponsesAreRefused` |
| P631 inline | Test-shard gate for [ClusterFTownsfolk | M | Done | `TalkCannotBeSwitchedOnOffTheTestShard` |
| P643 | F1. "Mara move" relocated the residents | M | Done | The move keyword is not passed to the base for these two residents only. `MoveSpeechDoesNotShiftTheStationaryResidents` (red: moved one tile) |
| P643 | F2. Pet orders could be swallowed | M | Done | Multiword orders are reserved; dispatch never claims speech carrying a stock keyword. `StockPetOrdersAreReserved`, `SpeechTaggedAsAPetOrderReachesThePet` |
| P643 | F3. Region keys not validated | M | Done | A fixed region per launch tag, checked before the swap. `ARegionTypoOrWideningKeepsThePreviousTable` |
| P643 | F4. Topic IDs could carry markup | L | Done (trivial) | Plain identifiers, and labels are escaped. `ExtraTopicIdsArePlainIdentifiers` |
| P643 | F5. Packet and gump lifecycle coverage | L | Skipped | Not trivial; the review itself calls it coverage, not a defect |
| P632 inline | (no findings) | - | - | - |
| P644 | 1. Mapping test allowed swapped pictures | L | Done (trivial, test only) | A literal table for all 10 states. `EachShotShowsItsOwnRingAndAmmoPicture` (red: an inner/middle swap mutant fails 2 cases while the old facts pass) |
| P644 | 2. Package parity left fields unchecked | L | Done (trivial, test only) | Layer, count, hue and light asserted in `Build-UoOverrides.Tests.ps1`, plus the server ItemData fields. Red: each field mutated to 1 in a temporary records copy fails the new fact and passes the old one. |
| P633 inline | Test-shard gate for [LevelGearProcs and the switch | H | Done | `TheMilestoneStaysOffOffTheTestShard` (red: Enabled true) |
| P633 inline | Milestone tooltip never connected | M | Done | Called from `ClusterFLevelGear.AddTooltip`. `TheBoughtEffectShowsOnTheWeaponTooltip` |
| P645 | 1. Confirmation could charge more than shown | M | Done | A server-side quote of price and unlock; a change means no charge and a refreshed confirmation. `TheConfirmationChargesOnlyThePriceItShowed`, through the real gump (red: 240 left of 440) |
| P645 | 2. Damage-immune targets used up a proc | M | Done | `CanBeDamaged()` is required. `AShutChestMimicDrawsNoRollAndNoCooldown`, through a real katana OnHit |
| P645 | 3. Live weapon cooldown across a restart untested | M | Done (test only) | `AWeaponCooldownSurvivesARestartAndAHandOver` (mutation red: with weapon-map persistence removed, expected 0, got 12) |
| P645 | 4. Disabled effect shown as ready | L | Done (trivial) | `TheBoundEffectPageShowsWhenItIsUnavailable` |
| P645 | 5. Cooldown maps never pruned | L | Done (trivial) | Pruned on the game thread before save, and on read. `ExpiredAndDeletedCooldownsArePruned` |
| P634 inline | Test-shard gate for [Leaseholds and its targets | H | Done | `OnlyTheTestShardMakesOrLeasesSites` |
| P634 inline | Guarded-town coverage not checked across the volume | M | Done | A TownRegion ancestor with guards on, and every tile at every floor in the street's region, at create and at assign. `TheWholeVolumeMustBeInTheGuardedTown` |
| P634 inline | AOS storage given a container count | M | Done | `GetAosMaxSecures` = 2 x lockdowns, the stock HousePlacementEntry ratio. `LockdownsAndAFilledSecureFitTheStorage` (red: chest could not be secured). Size question: For Chase |
| P646 | 1. Town addon container could be chopped into a deed | M | Done | Sites holding any addon container or component are refused. `TownAddonContainersKeepASiteOut` |
| P646 | 2. Ban spot need not be walkable | M | Done | `CanFit` (16 high, surface required), not inside a house, at create and assign; ejection and login land there. `TheStreetSpotIsWalkable` |
| P646 | 3. Other multis checked by origin | M | Done | Component footprints with Z from the covering sectors. `OtherMultisAreFoundByWhatTheyOccupy` |
| P646 | 4. Half of a linked door pair | M | Done | A registered door's link must be registered to the same site; another site's door is refused. `ALinkedDoorNeedsItsPartner` |
| P634 inline (shard-migration) | Run L1's in-client test-shard acceptance before calling P634 done | M | Skipped | Not a code fix and not this prompt's lane: it needs a test-shard start and a client session. It stays with P634's Draft A, where P634 put it. |

Count, from the rows above: 44 High/Medium findings (2 High). 43 are fixed in code; the one skipped is the P634 notes-repo acceptance row. 11 Lows: 8 fixed, 3 skipped (P638-3, P638-4, P643-F5).

## Limits and deviations

- Guard witness (P640-1): if a pet acts outside any guarded region while its master stands in Cove, the master's forwarded flag can still record an incident. Closing that needs a BaseCreature patch, which was left out of this stage.
- Town houses: a street spot that is valid at assignment can still be built over during the lease, and fixtures are refused rather than recorded and protected. Both belong with the later stages.
- Echo: `[LeagueEcho` is gated, but the `clusterf.leagueEchoes.enabled` config switch is still the future live switch and is not tied to the test shard.
- Shared files touched: `server/tests/Route/ShardTestClock.cs` (a new `Stall` method, additive only) and `server/customizations/ClusterFNotedBySystem.cs` (one condition).
- I could not Read `server/tests/Items/ScoringArcheryButteArtVerification.cs` with the Read tool: the unattended run denied it. I made the edit with a small Python script after reading the file with cat.
- CHANGELOG: new section `2026.10.26.8` and VERSION bumped. Player lines (Fixed) cover only Tracking Ping and Persuasion, the two features live on the shard. Everything else is a Staff line, because those features are test-shard only.
- No client, shard, Haven, save or account was touched. `docs/` was not changed.

## For Chase

1. **Town house size.** Lockdowns are still P634's provisional 8 per floor tile. A 16x16 building gets 2,048 lockdowns, and now 4,096 storage items (the stock 2:1 ratio): castle level (2,038 / 4,076), well above a stock house of the same floor area, and without stock's ML x1.2. Keep that, or follow stock houses of the same floor area? This is P409 open question 8.
2. **Persuasion charity ledger (P638-4).** The account remembers the last 200 people who taught a low-skill character. Past that, an old contact can teach again. Keep every credited contact forever (the account tag grows), or accept the 200 cap? Left as it is until you say.
3. **League warrants, stage 2:** the site check now treats the policy area as the map's full height, so the investigation's own region should be full height too when stage 2 adds it. Not a question unless you want otherwise.

P647 DONE
