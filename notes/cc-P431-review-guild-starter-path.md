# P431: review of the guild starter path

Reviewed 2026-10-22 by Codex. Code HEAD: `7508639ae5e728bcd35cd6fee923e06036bea307`. Pinned ModernUO: `d4531cd94b739613155225c234900de9f47d2c88`.

Read both work copies' `AGENTS.md`, the direction decision, task list, and `notes/cc-P15-guild-starter-path.md`. No separate P15 Codex review was found beside that note. Existing P15 findings are not repeated below.

## Findings

1. **bug** | `server/customizations/ClusterFGuildSystem.cs:400`: The Merchants' Apprentice task checks that the character owns 500 gold, but never consumes it because its dummy ItemID threshold is zero (`:221`), so the skill comparison prevents payment while reputation, scrip, and Apprentice status are awarded. Consume the tribute unconditionally for `ItemOnly`, retain the skill exemption only for `SkillOrItem`, and add regressions that assert the gold is removed from the backpack or bank.

2. **bug** | `server/customizations/SmithGuildmasterGump.cs:311`; `server/customizations/SanitationWardenGump.cs:269`: A nonmember can open the speech-triggered join window beside the guildmaster (`ClusterFGuildmasterExtension.cs:89`), walk beyond the guildmaster's eight-tile range or change facets, then join and receive tools because these handlers check only `CanJoin`, which checks account and membership. Route these joins through the hall's guarded response or recheck a matching nearby guildmaster when Join is pressed, and add response tests for moving away before pressing it.

3. **risk** | `server/customizations/ClusterFGuildStarterPath.cs:456`: No test under `server/tests/` calls `ReplaceStarterItem` or `OwnsCopy`, leaving the paid replacement path's ownership checks, scrip charge, and failed-delivery handling without behavior coverage. Add tests for a successful replacement charging exactly the owning guild's scrip, refusal while a copy is worn or nested in the backpack or bank, refusal for the pickaxe and hammer, and a full backpack preserving scrip and claim eligibility.

## Checks with no new finding

- **Duplicate free starter claims:** No new duplicate-claim defect found in the reviewed guild, trainer, and board paths. `GetState` checks both the character's starter record and the quest completion record (`ClusterFGuildStarterPath.cs:335`), and taking an item cancels a held quest before recording completion (`:427`). Pinned `MLQuest.OnAccept` rechecks `CanOffer` (`Projects/UOContent/Engines/ML Quests/MLQuest.cs:189`), while `MLQuestInstance.ClaimRewards` rejects a removed instance (`MLQuestEntry.cs:353`), protecting stale offer and reward windows too.
- **Gargoyle equivalents:** No additional finding beyond P15 sections 1.8 and 6. Reviewed the current creation-kit race branches, starter reward construction, race predicate in `GuildStarterPathVerification.cs:147`, and pinned equipment guards; the already recorded equivalent-item question remains outside this review's new findings.
- **Older saves:** No new starter-record load defect found by source inspection. Account versions before 14 skip the starter block (`ClusterFAccountData.cs:385`), later versions read it independently of the membership block, and the record's field order matches its writer (`:1021`, `:1039`). Existing serializer tests cover version 13, version 14 with retained character starter records, and the current round trip; dropping old account-wide membership is the explicit P18 behavior, not a new P15 defect.
- **Free joins:** The old skill and tribute requirements intentionally moved to the Apprentice task. Joining without them is the intended P15 behavior; finding 1 concerns payment for that later task, and finding 2 concerns the required guildmaster visit.

## Files reviewed

P15 implementation and relevant tests, using canonical source only:

- `server/customizations/ClusterFGuildStarterPath.cs`
- `server/customizations/ClusterFStarterGuildmasters.cs`
- `server/customizations/ClusterFGuildHallSeeder.cs`
- `server/customizations/Engines/ML Quests/Definitions/NewHavenTrainerGuildLines.cs`
- `server/customizations/ClusterFAccountData.cs`
- `server/customizations/CharacterCreation.cs`
- `server/customizations/ClusterFGuildSystem.cs`
- `server/customizations/SmithGuildmasterGump.cs`
- `server/customizations/ClusterFDevTools.cs`
- `server/customizations/ClusterFInstitutionSeeder.cs`
- `server/customizations/OutridersGuildmaster.cs`
- `server/customizations/ForestersGuildmaster.cs`
- `server/customizations/MinersCompactLiaison.cs`
- `server/customizations/Engines/ML Quests/Items/NewHavenQuestBoard.cs`
- `server/customizations/LeagueRegistrarGump.cs`
- `server/tests/Misc/GuildStarterPathVerification.cs`
- `server/tests/Misc/AccountDataSerializerVerification.cs`
- `server/tests/Engines/MLQuests/NewHavenQuestBoardVerification.cs`

Followed the join routing through `ClusterFGuildmasterExtension.cs`, `SanitationWardenGump.cs`, and `SanitationWarden.cs`, and checked pinned quest response, cancellation, and equipment code. Searched the shard's C# tests for replacement calls, Apprentice completion, and guild hall and starter-item response coverage.

Source review only. No code or tests changed, no tests or builds run, and no client or saved world opened. Runtime reproduction of the findings and actual old-save loading remain unverified. Haven was not contacted.

P431 DONE
