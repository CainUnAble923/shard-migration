# P657: review of P647 weekend review fixes

Reviewed October 26, 2026. Notes only. P647 is commit `3c2f8eb1744f8eb439d67b93baa33ac66b6fa779`, merged at code HEAD `e4c2dd9`. Notes HEAD at review start was `ab307974906efc483be98d863873282fecdc86d2`. Pinned ModernUO is clean at `d4531cd94b739613155225c234900de9f47d2c88`.

Two Medium findings remain in P647's fixes. Both include a specific case missed by the new regressions. No High finding was identified. These findings concern our code.

## Findings

### 1. Medium: an obsolete courier letter becomes payable again after a restart

**Location:** `server/customizations/ClusterFExchangeLetter.cs:96-104`, with removal at `:106-112` and payment eligibility at `server/customizations/ClusterFPersuasion.cs:557-581`.

P647 deliberately handles saves containing several letters for one courier by choosing the letter with the latest expiry. The other letters remain saved items. Their replacement status exists only in `_outstanding`; nothing on those items records that they lost the selection.

Consider two unexpired letters A and B left by the old banking loophole, with B expiring later. On load B wins, and A cannot pay. Deliver B, which deletes it and removes the dictionary entry. Leave A untouched in the bank, save, and restart before A expires. A is now the only saved letter, so its `AfterDeserialization` calls `Claim` and makes it outstanding. `Deliver` will accept it and award its practice. Several old letters can be revived one per restart. The same revival follows deleting the newest letter instead of delivering it.

This is a persistence failure in the new replacement rule, not a repeat of the original ability to request another job by banking a letter. P647 closes that issuance route, but does not durably retire the stockpile it explicitly tries to invalidate. Actual legacy stockpiles in the current world were not inspected.

**Evidence:** an offline .NET probe linked the unchanged canonical `ClusterFExchangeLetter.cs` with minimal engine shims. With both letters present it printed `older=False, newer=True`; after deleting the newer one it printed `older=False`; after invoking the older one's actual deserialization hook it printed `older=True`. This isolates the real registry and hook logic. It is not a full engine serialization or world-restart test. The payment consequence follows the production `IsOutstanding` check and subsequent practice call cited above.

**Fix:** make replacement durable. For example, reconcile all loaded letters per courier after loading and delete or permanently mark every loser, regardless of load order. Alternatively persist the active assignment or a replacement generation on courier data and validate every letter against it. Consuming or deleting the winner must not allow a surviving loser to become valid on the next load.

**Missing regression:** load two legacy letters in both orders, consume the winner, save and reload while the loser is still unexpired, and attempt delivery of the loser. It must stay invalid and grant no practice. Include deletion of the winner and a valid single-letter control. `server/tests/Skills/PersuasionVerification.cs:603` tests banking and expiry in one process only; it never rebuilds the new registry after the winner disappears. Observe the new regression fail before repairing it.

### 2. Medium: the new action matcher still absorbs a separate victimless crime

**Location:** `server/customizations/ClusterFGuardWitness.cs:403-406`, consumed at `:293-294`; the merge keeps the old action at `:316-330` and gathers witnesses again at `:341-362`.

`SameAction` requires the same frame and culprit position, but treats an incoming `CriminalAction` as a wildcard for kind and its null victim as a wildcard for victim. After a player attacks someone, a separate victimless crime at the same position in the same server frame therefore matches the completed aggression incident. No pet or forwarded-owner callback is required.

The existing incident keeps its aggression kind, victim, and action location. The separate crime gets no incident of its own. Witness collection runs again against the old action location. A player who arrives between the two acts can consequently be attached to the earlier attack they never saw, provided they can currently see the actor and that location. Conversely, someone who sees the new crime but cannot see the earlier victim is excluded from reporting the new act. Two separate attacks against the same victim in that frame also match.

This is the remaining same-position, same-frame hole in P647's replacement matcher. It does not reissue the old one-second merge across arbitrary places and victims, which P647 fixed. It is also separate from the pet-owner suppression defect already reported in `cc-P647-fix-weekend-review-findings-codex-review.md`; that finding is not counted again here.

**Evidence:** the offline probe compiled the exact `SameAction` method extracted unchanged from the canonical file. It returned `True` for an independent victimless criminal callback against an existing aggression incident, and `True` for a second attack against the same victim. Pinned `Projects/Server/Main.cs:711-732` sets `Core.Now` once before slicing timers and networking, so independent actions can share it. The actual criminal-action and aggression callback sequence is in pinned `Projects/Server/Mobiles/Mobile.cs:4528-4537` and `:8386-8404`, reached by `server/patches/GuardedRegion-witness-observe.patch`. Full gameplay and packet reproduction were not run.

**Fix:** correlate callbacks using the originating action's identity or a narrowly scoped action context. Only that action's criminal flag and aggression/assist callbacks should join. A completed incident must not remain a candidate for a later victimless callback just because the clock and actor position match. Preserve the stock legal callbacks and freeze the witnesses for the completed act.

**Missing regression:** without advancing the clock or moving the culprit, finish an attack, move another witness into view, then perform a separate victimless crime. Require a second incident with its own location and witnesses, and prove that the newcomer is absent from the first incident. Retain the one-action/two-callback control and add two distinct attacks against the same victim. The new `OneActionIsOneIncidentAndADistinctOffenseIsAnother` at `server/tests/Regions/GuardWitnessVerification.cs:257` changes both victim and culprit position, so its passing case cannot catch this wildcard match. Observe the new regression fail before repairing it.

## Review scope and earlier findings

Read both work-copy `AGENTS.md` files, the direction decision and task list, both `cc-P647-*.md` notes, and every primary review and adjacent Codex review from P637 through P646. Also reread the earlier P626 and P628 inline findings where necessary to distinguish the incomplete fixes above. P647 explains the missing P636 note; no new P636 source was assumed.

Reviewed the P647 diff and surrounding implementations and regressions in these files. Paths below are relative to the code work copy:

- `CHANGELOG.md`, `VERSION`, and `player-package/tests/Build-UoOverrides.Tests.ps1`.
- `server/customizations/ClusterFExchangeLetter.cs`, `ClusterFPersuasion.cs`, `ClusterFTrackingPing.cs`, `ClusterFItemKnowledge.cs`, `ClusterFGuardWitness.cs`, and `ClusterFNotedBySystem.cs`.
- `server/customizations/LeagueEchoes/LeagueEchoSystem.cs` and `server/customizations/Mobiles/LeagueEchoes/LeagueDragonEcho.cs`.
- `server/customizations/LeagueInvestigations/LeagueInvestigationCatalog.cs`, `LeagueInvestigationSeeder.cs`, and `LeagueInvestigationWarrant.cs`.
- `server/customizations/Leaseholds/ClusterFLeaseSite.cs` and `ClusterFLeasehold.cs`.
- `server/customizations/LevelGear/ClusterFLevelGear.cs`, `LevelGearMilestoneGump.cs`, and `LevelGearProcs.cs`.
- `server/customizations/Townsfolk/ClusterFTalkRules.cs`, `ClusterFTownsfolk.cs`, and `ClusterFTownsfolkService.cs`.
- `server/tests/Items/ItemKnowledgeVerification.cs` and `ScoringArcheryButteArtVerification.cs`.
- `server/tests/Misc/LeagueEchoesVerification.cs`, `LeagueInvestigationVerification.cs`, and `LevelGearProcVerification.cs`.
- `server/tests/Mobiles/LeagueDragonEchoVerification.cs`, `server/tests/Multis/LeaseholdVerification.cs`, and `server/tests/Regions/GuardWitnessVerification.cs`.
- `server/tests/Skills/PersuasionVerification.cs`, `TrackingPingVerification.cs`, `server/tests/Townsfolk/TownsfolkTalkVerification.cs`, and `server/tests/Route/ShardTestClock.cs`.

Traced relevant pinned ModernUO mobile crime callbacks, guard eligibility, event-loop time, item and container drops, generic persistence, tile-matrix loading, map fit and multi-sector enumeration, and addon-container chopping. Read the unchanged guard observation patch and the supporting imbuing/requisition property readers. The generated `server/uo/` tree was not used.

The other inspected fixes had no additional finding. In particular, the warrant's direct-root restriction closes ordinary movable-bag placement; the map gate checks land and both static streams; the investigation region scan checks overlapping regions independent of the winning region; the house multi scan uses occupied components; and proc confirmations retain the displayed price and unlock level. These are source observations, not runtime acceptance passes.

P647's explicitly skipped charity history/storage decisions, townsfolk packet/menu coverage, and town-house client acceptance remain with their existing reviews. Its disclosed pet-outside-jurisdiction limitation, later-stage house changes, Echo configuration boundary, and provisional house storage size are not presented as new findings. No new policy decision or deployment is proposed by this review.

## Verification and limits

Lane tests are none. No shard tests were added or changed, and no Docker build, container, shard startup, client session, save/account operation, or Haven connection was performed. P647's reported gated build and failing-then-passing regression results were read, not independently rerun. The new regression suggestions above still require failing-first execution in their fixing task.

The diagnostic project is under ignored `downloads/p657-review/`, confirmed with `git check-ignore downloads/p657-review/probe.csproj`. It links the real letter implementation and extracts the real matcher; its engine shims do not establish map, packet, or full-world behavior. Every scratch artifact is below 5 MB. No canonical code was edited.

The required progress reporter completed with `--dry-run` and both work-copy path overrides. Its incidental `tools/progress.json` write was suppressed in memory, so generated files were unchanged. Both repositories passed `git diff --check`. The note passed plain ASCII, no-em-dash, trailing-whitespace, and size checks; all ignored diagnostic files passed the size limit. Windows PowerShell was 5.1.26100.9711. The code work copy is clean and the only notes-repo change is this file. No `docs/` file changed. No commit, merge, push, or branch switch was performed. The stop-request file was absent at the final checkpoint.

P657 DONE
