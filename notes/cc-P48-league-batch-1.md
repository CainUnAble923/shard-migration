# cc-P48: League batch 1, signposts and the 17-rank ladder

2026-10-04. Brief: `D:\UO\cc-prompts\cc-P48-league-batch-1.md` (cc-P47's Batch 1). Engine: `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88` (`rev-parse HEAD` today); every pinned citation is against it. "C\" =
`D:\ShatteredLegacy\server\customizations\`, "T\" = `D:\ShatteredLegacy\server\tests\Misc\`. Scratch: `D:\UO\cc-p48-work\`.

## Headlines

1. **All five parts done, all green.** Final verified build (build 3) through `docker\uo\build.sh -t sl-modernuo:cc-p48`:
   **41/41 patches** (no patch added or changed), **606/606 shard facts** (579 before + 27 new), image
   `sl-modernuo:cc-p48` = **`beb5677d7a5d`**. `sl-modernuo:latest` not moved (`8d7505c739f6` before and after). Nothing
   deployed, no shard touched, no world state changed, nothing committed.
   **Build 4 did not finish: Docker stopped answering.** After build 3 I changed only two comments in
   `T\LeagueSignpostsVerification.cs` (diffed against the tree build 3 used: comments only; no customization changed).
   Build 4 of that tree passed the builder stage, then sat at "2/3 running ShatteredLegacy.Tests" from 08:12; from about
   08:24 `docker version` and `docker ps` gave no answer in 20-30 s. Both shards still accepted TCP connections on 2593
   and 2594 (08:35). I did not restart Docker or WSL (it would stop both shards); I stopped my own build client at about
   08:40, so `sl-modernuo:cc-p48` is still build 3's image. **Chase: once Docker answers, re-run
   `docker\uo\build.sh -t sl-modernuo:cc-p48` before committing** (expect 41/41, 606/606; the image id will change).
   If Docker Desktop has to be restarted, the recipe is `notes\cc9-artifacts.md` section 10.
2. **Red proof, every new fact.** A copy of the final tree with every P48 behaviour undone or stubbed
   (`D:\UO\cc-p48-work\make-trees.py red`, built with its own `build.sh --tests-only`): **28 of 607 fail**: 25 of the 27
   new facts, the round-trip fact I extended, one existing fact my Mining fix now feeds
   (`GuildStandingCommandVerification`, below), and a scratch probe that fails on purpose. The other two new facts
   (`SmithingSixRanks`, `AGenericGuildSixRanks`) stay green there, because that red folds only the 7- and 5-rank ladders
   wrong; a second variant with `GuildRankIndex` absent (`make-trees.py red-c`) fails **9**, those two included. Then
   green in builds 3 and 4.
3. **The brief's milestone numbers are wrong; I built by name.** Counted from the enum (`ResourceInfo.cs:6-27`): Iron 1,
   Dull Copper 2, Shadow Iron 3, Copper 4, Bronze 5, Gold 6, Agapite 7, Verite 8, Valorite 9, Platinum 10, **Toxic 11**,
   **Blaze 12**, Frost 13, **Obsidian 14**, **Mythril 15**, Adamantium 16, Celestial 17. The brief (Parts D and E), P47
   2.1 and `docs\league-storyline.md:56-58` say "Blaze (11)" and "Mythril (14)". Chase's own decision names the metals
   (feature-queue F-24: "Dull Copper, Bronze, Verite, Blaze, Mythril, Celestial"), the storyline's chapter headings are
   metal names, and "every third rank" would give Toxic and Obsidian instead. The milestones are a column in the
   editable table, so Chase can move chapters 4 and 5 to Toxic and Obsidian with no build. **Chase to say which.**
4. **The Registrar never spoke, proved and fixed.** Her ambient lines started only in `OnAfterSpawn`, which pinned calls
   from a spawner alone (`BaseSpawner.cs:1131, :1146`; the only callers). `ClusterFNewHavenSeeder.ApplyEntry` places her
   with `MoveToWorld` (`:194`), and a world load calls neither. Now started on arriving on a map, after deserializing,
   and from a spawner, with one timer token so it never doubles. The fact was red without the fix ("no ambient timer
   after MoveToWorld"), green with it. Ours and small, so fixed (P47 section 1 said "probably never fires, unverified").
5. **Storage: `ClusterFAccountData` v15 to v16.** P46 bumped `CharacterGuildData` (0 to 1), not the account record,
   which was still at 15 (`ClusterFAccountData.cs:348` at `92f8f5f`). v16 appends lifetime Renown and a
   `CharacterLeagueData` per character serial; every older version still loads (facts: v13, v14, v15 bytes from frozen
   writers). A pre-v16 account starts lifetime Renown at its Renown and reads as Iron on every character if registered.
6. **Renown curve proposed:** today's 74 achievements pay **6,505** Renown (counted, by parsing every `Reg(` call;
   matches P47). Bronze (5) at **2,500** is reachable by achievements alone; Gold (6) at **7,000** is not, so everything
   past Bronze waits for batch 2's jobs. Full table below.
7. **Build 2's one failure was my fact, and its cause was probed, not guessed.** The Guild Board path found no
   directory. Two candidates: the board's `CanUse` refusing, or the account-less test connection's 4 KiB send ring
   (cc-P30). A scratch probe with build 2's exact setup: `[guild` sent 2,039 bytes and the connection stayed up;
   **the board's `CanUse` was false**. The fact had not called `NewHavenQuestBoard.Register()`, as
   `NewHavenQuestBoardVerification` does. Fixed in the fact (plus an account on the connection, harmless and as the
   board's facts do).
8. **Clash, not mine:** an untracked `D:\ShatteredLegacy\design\tutorial-farm\` (python, png, json; 07:35 to 07:54
   today) appeared during this task; `git status` was clean at my preflight. No overlap with any file of mine. Not
   touched. As P46 found, "one builder at a time" was not held by that session.
9. **For Chase to weigh (changed, small):** the dev reset's "League, flags" option now also clears every character's
   League rank (it already cleared registration), and its "Renown" option clears lifetime Renown too. Rank survives
   every other option, the "loop" parts included. Without this, "League, flags" would leave an unregistered character
   holding a stored rank.

## Clashes checked

- **P36** (`D:\UO\cc-prompts\cc-P36-dungeon-build-1.md`, not run yet): appends `Dawnstone` after Celestial and widens
  the metal range (`ResourceInfo.cs:1092`). No file in common with this batch. The ladder walks
  `Enum.GetValues<CraftResource>()` filtered by `CraftResources.GetType(r) == Metal`, so once P36 widens the range
  Dawnstone is walked and dropped by name (`LadderExcluded`, enum name `Dawnstone`, the name P36 uses, its line 127).
  Works before and after P36: fact B2 adds a Dawnstone metal and gets 17. **P36's consumer walk (its line 133) should
  list the League ladder as "stays out, already excluded by name".**
- **P34** (winter decor) reads `ClusterFRegistrarOfficeSeeder.cs`. I did not edit it (the sign needed no change), so no
  overlap. They can still run one after the other as the brief asks.
- **P46** left `CharacterGuildData` at v1 and `ClusterFAccountData` at v15; v16 is mine. Smith code untouched.

## What changed

New:
- `C\ClusterFLeagueRanks.cs` (842 lines). `LadderExcluded` `:87`; `MetalsFromEnum` `:96`; `Generate` `:112`;
  waiver settings `:148-188`; `Configure` `:168` (reads the settings, loads or writes the table, registers
  `[LeagueLadder`); `GetRank` `:194`; `SetRank` (staff) `:208`; `LeagueMilestonesReached` `:222`; `Evaluate` (the four
  checks) `:241`; `TryPromote` `:344`; `[LeagueLadder` `:392`; `LeagueLadderTable` `:433` (defaults `:443`, `Parse`
  `:547`, `LoadOrWriteDefaults` `:702`); `PlayerMobile` partial with the `[props` fields `:764`.
- `T\LeagueSignpostsVerification.cs` (4 facts), `T\LeagueLadderVerification.cs` (12), `T\GuildRankIndexVerification.cs`
  (10).

Changed:
- `C\ClusterFAccountData.cs`: `LifetimeRenown` `:40`; per-character League store `:152`; v16 read `:349` (pre-v16:
  lifetime = Renown); `CurrentVersion = 16` `:396`; v16 write `:474`; `GrantRenown(amount, RenownSource)` `:516` (the
  one earning seam); `enum RenownSource` `:538` (Achievement, LeagueJob, Commission, Staff; Commission never counts);
  `CharacterLeagueData` `:551` (own version 0, fails loudly on another).
- `C\ClusterFAchievements.cs:838`: `TryGrant` pays through `GrantRenown(.., Achievement)`.
- `C\ClusterFGuildSystem.cs`: the Mining case in `GetRankName` `:584`; `RankThresholds` `:609`; `GuildRankIndex` by
  standing `:623` and by character `:643` (Apprentice bump); `RankIndexName` `:650`. Guild Directory: `LeagueRowY`,
  `LeagueRowName`, `BtnLeagueWay = 60` `:784-795`; the League row `:871`; its button `:955`. Header 92 to 140 px.
- `C\ClusterFLeagueSystem.cs`: `RegistrarPost` `:152` (read from the seeder entry, so the two cannot disagree);
  `ShowTheWayToRegistrar` `:175` (same arrow and wording rules as a guild row).
- `C\ClusterFGuildStarterPath.cs`: `GuildWelcomeGump` H 230 to 260, `LeagueLine` `:784`, in the page `:803`.
- `C\LeagueRegistrar.cs`: ambient speech `:106-150` (token `:113`, `OnMapChange` `:123`, `[AfterDeserialization]`
  `:129`, cancel on delete `:145`); two em dashes in spoken lines made ASCII.
- `C\LeagueRegistrarGump.cs`: `BtnRank = 18`, `BtnPromote = 19` `:28-29`; rank in the status line `:102`; the rank on
  Citizen Status `:151`; `DrawRank` `:157`; Promote `:335` (only from the Rank page, only from the rank it was drawn at).
- `C\ClusterFBankLimit.cs`: `ItemsPerLeagueRank` renamed `ItemsPerLeagueMilestone` `:32` (no other reference);
  `LeagueRankBonus` = 100 x milestones `:46`.
- `C\ClusterFDevTools.cs`: Renown option also zeroes lifetime Renown `:190`; "League, flags" clears League records
  `:209` and re-applies bank limits; gump texts updated.
- `C\ClusterFGuildStandingCommand.cs:96`: `RankName` is now just `GetRankName` (its Mining workaround is the fix above).
- `T\AccountDataSerializerVerification.cs`: round trip carries the new fields; frozen v15 writer; new v15 fact; the two
  "written again it is 15" asserts now say 16; unknown `CharacterLeagueData` version fails loudly.

## Part A: signposts

**Guild Directory.** All three lists are one gump: `[guild` (`ClusterFGuildSystem.OnGuildCommand`), the Guild Board
(`NewHavenQuestBoard.OnDoubleClick`, `Engines\ML Quests\Items\NewHavenQuestBoard.cs:121-128`) and the Registrar (buttons
14 and 20) all build `GuildProgressGump`, so one row covers all three (F-9 Decision 2.3 holds). The League row is drawn
on page 0, so it sits above the guild rows on every page, fenced by a rule above and below. It shows the League's name,
"Field Office, New Haven", the character's League rank (or "Not registered"), one line ("Ties every guild together. Its
Registrar keeps your League rank.") and **Show me the way** (button 60). The button finds the Registrar within 15 tiles
of her seeder tile and sets the same `GuildDirectionArrow` the guild rows use; a missing Registrar is reported ("Please
tell a Game Master"), no arrow.

**Welcome page.** One line after the Guild Board line: "The League of Extraordinary Citizens ties every guild together.
Find its Registrar in New Haven." (the brief's text). The page grew 30 px so it fits.

**Office sign.** No code change: it is already built (`ClusterFRegistrarOfficeSeeder.cs:43-46`, item 0x0BCF named
"League of Extraordinary Citizens", in the outside addon). Placed only by the command or the world-load setting
(default false, `:52, :60`). **Twice is safe:** the plain command skips any of the three addon types already on Trammel
and moves or deletes nothing (`RegistrarOfficeVerification.SeedingTwicePlacesTheDecorOnce`: second run "placed 0 of 3").
Whether the test world has it is **unverified** (I did not touch either shard); the commands below check first.

**Registrar speech.** Headline 4.

## Part B: the ladder and storage

- **Generated, 17 ranks** (fact B1 lists them): one per metal in enum order, named "<Metal> Citizen", hued with the
  metal's hue (`CraftResources.GetHue`; Iron's is 0, so its label is drawn in plain white, hue 1153).
- **Exclusion by enum name**, `LadderExcluded = { "Dawnstone" }`. A new metal adds a rank only when not excluded (B2
  shows both). A rank added later with no table row asks what the rank below asks and has no trial.
- **Per character**: `CharacterLeagueData { Rank, PromotionDone, TrialsDone }` keyed by serial in the account record,
  apart from the guild data, so no guild reset touches it. **Registration stays the account flag**: `GetRank` is 0 on an
  unregistered account, else at least 1, so registering on one character makes every character Iron, and a pre-v16
  save needs no write to read its characters as Iron (B4).
- **Lifetime Renown, per account, only rises.** `GrantRenown` is the one way in; `SpendRenown` touches only the balance.
  **Seams for later batches:** batch 2's jobs call `GrantRenown(n, RenownSource.LeagueJob)` (counts); batch 4's
  Commissions must call `GrantRenown(n, RenownSource.Commission)` (never counts,
  `ClusterFAccountData.CountsTowardLeagueRank`). There is no other way to raise `Renown` in code today (grep: the only
  writer was `TryGrant`; the dev reset zeroes).
- **Statuses:** Unregistered = 0, Registered = Iron via `JoinLeague` (unchanged code; Iron is what a registered
  account reads as), Recognized stays the computed tag.

## Part C: `GuildRankIndex`

Rungs 0 to 3 are Initiate, Apprentice, Journeyman, Master on every ladder; the top rung is 5; a 7-rank ladder's two
rungs between are both 4; a 5-rank ladder has no 4. Thresholds are written beside `GetRankName` and a fact holds them
to the names (`GuildRankIndexVerification` fact 1), so the two cannot drift:

| Ladder | Guilds | Thresholds | Index per rung |
|---|---|---|---|
| Generic | arcane, tailoring, tinkers, healers, bards, thieves, warriors, maritime, merchants, dojo, keepers | 0, 1k, 5k, 15k, 50k, 100k | 0 1 2 3 4 5 |
| Smithing | smithing | same | 0 1 2 3 4 5 |
| Seven-rank | rangers (Outriders), foresters, mining | 0, 1k, 5k, 15k, 40k, 80k, 150k | 0 1 2 3 4 4 5 |
| Artificers | artificers | 0, 1k, 5k, 15k, 40k | 0 1 2 3 5 |
| Custodians | custodians | 0, 25, 125, 500, 1,250 (Clean Up points) | 0 1 2 3 5 |

The Apprentice task lifts index 0 to 1 (as `GetRankName`'s bump at `ClusterFGuildSystem.cs:594`) and never lowers a
higher one. **Mining's rank names are fixed**: `GetRankName("mining")` is now the Miners' Compact ladder, so the
Directory shows "Surveyor" where it showed "Master". `GuildStandingCommandVerification` reads the Mining name through
`[GuildStanding`'s `RankName`, which now delegates to `GetRankName`: red in the red tree, green in the final one.

A guild counts toward League promotion only when the character has **joined** it (fact D1: a rank held as a non-member,
for example Artificers standing from imbuing, does not count).

## Part D: promotion

`ClusterFLeagueRanks.Evaluate(pm)` gives the four checks for the next rank; the Registrar's Rank page draws them, and
**Promote** calls `TryPromote(pm, <the rank the page was drawn at>)`, which evaluates again and refuses if the rank has changed or
any check fails. One press, one rank. Announced to the player only ("The League names you Dull Copper Citizen, a
milestone rank. Your bank box now holds 1,100 items."); no broadcast.

| Check | Passes when | Waived |
|---|---|---|
| Lifetime Renown | `LifetimeRenown >= row.renown` | never |
| Guild ranks | joined guilds with `GuildRankIndex >= row.guildRank` number at least `row.guilds` | never |
| Promotion job | `PromotionDone` holds the next rank | while `league.promotionJobsWaivedUntilBuilt` is true (default) |
| Story trial | the row has no chapter, or `TrialsDone` holds it | while `league.trialsWaivedUntilBuilt.chapterN` is true (default, each of 1 to 6 its own) |

Settings are `modernuo.json` keys written on first start like every `clusterf.*` key. **Never required after the
fact:** the trial is checked only when rising **to** its rank (fact D3: a Bronze citizen keeps Bronze and reaches Gold
after chapter 2's waiver is cleared).

**The table** is `Configuration/league-ladder.json` (that folder is bind-mounted: `server\uo\modernuo\Configuration`
on live, `Configuration-test` on test). **How it loads:** at start; missing, it is written with the defaults (the
log says so); `[LeagueLadder reload` re-reads it in game. **How a bad row fails:** the file is refused whole, never row
by row; every error is printed with its row and metal (console at start, the staff member's screen on reload), and the
table in force is kept (the defaults at start). Checked: JSON syntax; a `ranks` array; metal is a ladder metal and
appears once; renown a whole number of 0 or more that never falls from one rank to the next; guildRank one of
Initiate, Apprentice, Journeyman, Master, Grandmaster, Top; guilds 0 to 17; chapter 0 to 6, each used once; a row for
every rank from Dull Copper. Iron's row is optional and unused. Fact D5 puts six kinds of bad row into one file and
gets every one named.

## Part E: milestone bonuses

`ClusterFLeagueRanks.LeagueMilestonesReached(m)`: milestone ranks at or below the character's rank, 0 to 6 (a milestone
is a row with a chapter). `ClusterFBankLimit.LeagueRankBonus` = 100 per milestone, so 1,000 / 1,100 / ... / 1,600.
`TryPromote` and `SetRank` call `ClusterFBankLimit.Apply`; it writes the bank only when the number changes. The BOD and
active-job bonuses are not here (F-25 follow-up, batch 2); they should read the same helper.

## Facts, red then green

Red = `make-trees.py red` (build `build-red2.log`) unless marked (c) = `red-c` (`build-red-c.log`). Green = builds 3 and
4. All red builds were of a scratch copy, never `D:\ShatteredLegacy`.

| Fact | What it pins | Red with |
|---|---|---|
| Signposts 1 `TheLeagueRowIsFirstInAllThreeLists` | League row first in `[guild`, the Guild Board, the Registrar's two openers | "[guild: no League row" |
| Signposts 2 `TheLeagueRowPointsAQuestArrowAtTheRegistrar` | arrow to the Registrar; a missing one reported | no arrow |
| Signposts 3 `TheWelcomePageCarriesTheLeagueLine` | the League line, once, beside the Guild Board line | line not found |
| Signposts 4 `TheRegistrarSpeaksAfterTheSeederPlacesHer` | speech after `MoveToWorld`; one timer after moves | "no ambient timer after MoveToWorld" |
| B1 `TheGeneratedLadderHas17RanksIronFirstCelestialLast` | 17, order, names, hues, six milestones | names differ |
| B2 `ADawnstoneMetalAddsNoRankAndAMetalNotExcludedWould` | Dawnstone excluded; a new metal adds one | 18 ranks |
| B3 `TwoCharactersOnOneAccountHoldDifferentRanks` | ranks per character, registration per account | rank 0 |
| B4 `AnAccountSavedBeforeTheBumpLoadsWithItsCharactersAtIron` | v15 joined account reads Iron; unjoined 0 | rank 0 |
| B5 `SpendingRenownLeavesLifetimeRenownUnchanged` | spend, achievement, job, Commission | lifetime 0 |
| Serializer `AVersion15SaveFromTheBuildBeforeLeagueRanksLoads` | v15 bytes load; lifetime = Renown; written as 16 | lifetime 0 |
| Serializer round trip (extended) | every new field kept, two ranks | League records lost |
| D1 `EachCheckBlocksAloneAndAllFourPromoteByExactlyOne` | each of four blocks alone; one rank per promote | red (first assert: rank 0) |
| D2 `PromoteChecksAgainSoAStalePageCannotPromote` | double press, stale page | red (no Promote button) |
| D3 `AClearedWaiverBlocksUntilTheChapterIsDoneAndOnlyItsOwnRank` | waived passes; cleared blocks until done; per chapter; not after the fact | red |
| D4 `RankNeverDropsOnARenownSpendOrTheResetsLoopParts` | spend; reset's loop parts; "League, flags" clears | red |
| D5 `TheTableReadsBackRefusesABadFileWholeAndTakesAGoodOne` | defaults round trip; bad file refused whole; good taken | bad file put in force |
| D6 `TheRegistrarShowsTheRankAndTheFourChecks` | rank in status line, Rank page, hue | no rank label |
| E1 `TheBankStepsOnlyAtMilestones` | 0, 1, 6 milestones; non-milestone unchanged; 16 promotions, 6 steps | red |
| C fact 1 `EachLaddersThresholdsAreWhereItsRankNameChanges` | thresholds match names | "rangers: the name does not change at 50000" |
| C `SmithingSixRanks`, `AGenericGuildSixRanks` | 6-rank ladders | (c) |
| C `OutridersSevenRanks`, `ForestersSevenRanks`, `MiningSevenRanks` | 7-rank ladders | collections differ at 4 |
| C `ArtificersFiveRanks`, `CustodiansFiveRanks` | 5-rank ladders | top is not 5 |
| C `TheMiningRankNameIsTheMinersCompactsLadder` | Mining names | differ |
| C `TheApprenticeTaskLiftsTheIndexToApprentice` | the bump | 0 |

Not watched red: the extension of `AnAccountRecordOrStarterRecordOfAnUnknownVersionFailsLoudly` to
`CharacterLeagueData` (no undo touched the version check). **A caution on the red tree:** with every behaviour undone at
once, several facts fail at an early assertion (often "rank 0", since stored rank was undone), so a red fact proves the
fact can fail, not that each of its assertions was watched failing separately. D1's four "blocks alone" steps were
watched individually only in the green direction (each must block and then pass when mended, inside one fact).

## Test-shard commands for Chase

Deploy is yours (passdown: `docker tag sl-modernuo:cc-p48 sl-modernuo:latest`, then
`D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild`, stopping first with `-Down`). On first start the server
writes `Configuration-test\league-ladder.json` and the seven `league.*` keys into `modernuo.json`.

Office sign (GM, in game):
```
[ClusterFSeedRegistrarOffice status
[ClusterFSeedRegistrarOffice
```
The first changes nothing and lists what it would place; the second places only what is missing. Safe to run twice. If
`status` says a cc-P19 office is there, `[ClusterFSeedRegistrarOffice replace dryrun` then `replace` swaps it (deletes
only its own three addons).

Quick promotion walk (staff character on yourself or a test character; `[props` then the League fields):
1. `[guild`: the League row is at the top; "Show me the way" points at Elara Voss. Stand near her for a minute: she
   should speak (needs a restart onto this image first, which restarts her timer).
2. At the Registrar: League Rank. Not registered: "Register with the League first". Join, then League Rank: Iron Citizen,
   next Dull Copper, Renown and guild checks unticked, job and trial "not yet required".
3. `[props` on the character: `LeagueLifetimeRenown` = 100. `[GuildStanding warriors 1000` targeting the character
   (and join the Warriors' guild at its guildmaster, or be already joined: standing counts only as a member). Reopen
   League Rank: all ticked, Promote. Bank box now 1,100.
4. `[props`: `LeagueLifetimeRenown` = 110000, and set `LeagueRank` directly (1 to 17) to look at any rank; the bank
   follows (`LeagueMilestones` shows 0 to 6). `LeagueTrialsDone` / `LeaguePromotionJobsDone` take "1,2" style lists.
5. `[LeagueLadder` lists the table in force and the waivers; `[LeagueLadder reload` re-reads the file.
6. To try a built chapter: set `league.trialsWaivedUntilBuilt.chapter1` to false in `Configuration-test\modernuo.json`,
   restart; rising to Dull Copper then needs `LeagueTrialsDone` to hold 1.

## The placeholder tables, as written

Requirements for rising TO each rank (`LeagueLadderTable` defaults, `ClusterFLeagueRanks.cs:443`):

| # | Rank | Lifetime Renown | Guild rank | in guilds | Trial chapter |
|---|---|---|---|---|---|
| 1 | Iron Citizen | (registration) | | | |
| 2 | Dull Copper Citizen | 100 | Apprentice | 1 | 1 |
| 3 | Shadow Iron Citizen | 400 | Apprentice | 1 | |
| 4 | Copper Citizen | 1,000 | Apprentice | 1 | |
| 5 | Bronze Citizen | 2,500 | Apprentice | 2 | 2 |
| 6 | Gold Citizen | 7,000 | Apprentice | 2 | |
| 7 | Agapite Citizen | 10,000 | Apprentice | 2 | |
| 8 | Verite Citizen | 14,000 | Journeyman | 3 | 3 |
| 9 | Valorite Citizen | 19,000 | Journeyman | 3 | |
| 10 | Platinum Citizen | 25,000 | Journeyman | 3 | |
| 11 | Toxic Citizen | 32,000 | Journeyman | 4 | |
| 12 | Blaze Citizen | 40,000 | Journeyman | 4 | 4 |
| 13 | Frost Citizen | 50,000 | Journeyman | 4 | |
| 14 | Obsidian Citizen | 62,000 | Master | 4 | |
| 15 | Mythril Citizen | 76,000 | Master | 4 | 5 |
| 16 | Adamantium Citizen | 92,000 | Master | 4 | |
| 17 | Celestial Citizen | 110,000 | Master | 5 | 6 |

Guild ranks are the brief's defaults by **rank number** (2-4, 5-7, 8-10, 11-13, 14-16, 17). Note that the guild bands
follow the numbers, the chapters follow the names, so Blaze (12) and Mythril (15) sit one rank into their bands. If
Chase moves chapters to 11 and 14 the two line up.

Renown: achievements alone (6,505 in all) pass Bronze (2,500) with room, never Gold (7,000). After Gold the curve
roughly adds a third each rank to Celestial at 110,000. The gaps are sized for nothing yet: batch 2's job pay (and F-12)
should set them.

Bank: 1,000 + 100 per milestone (1,100 at Dull Copper ... 1,600 at Celestial).

## Left for batch 2 (and later)

- Promotion jobs: set `PromotionDone.Add(rank)` on turn-in of a job tagged for that rank, and pay Renown with
  `GrantRenown(n, RenownSource.LeagueJob)`. Then set `league.promotionJobsWaivedUntilBuilt` false.
- Active-job cap 3 + `LeagueMilestonesReached` (3 to 9), the F-25 BOD bonus: read the helper, nothing else to add.
- Batch 4: Commission Renown through `GrantRenown(n, RenownSource.Commission)` only.
- Trials: each chapter's end adds its number to `TrialsDone`; clear that chapter's waiver when it ships.
- A Jobs button on the Registrar (P47 2.3); the main menu has room for one more row.
- Not verified in a client: the gump layouts (directory header, Rank page), label hues per metal (the client may show a
  hue one off what the number means), the speech, the welcome page wrap. Add to the client-check list.
- `LeagueMemberPass` still handed out by nothing; `FlagIntroCompleted` still never set (both P47, unchanged).

## Builds

| Build | Tree | Result |
|---|---|---|
| 1 | final, first try | builder failed: one test compile error (mine, a static helper) |
| 2 | final | 605/606: the board fact (headline 7) |
| 3 | final | 41/41 patches, 606/606 |
| red2 | `make-trees.py red` + probe | 28/607 failed (red table above; the probe failing on purpose) |
| red-c | `make-trees.py red-c` | 9/606 failed: the 8 ladder facts and E1 |
| 4 | final (two comments changed since 3) | not finished: builder stage passed (41/41 patches), then Docker stopped answering at the test gate; client stopped by me |

(`build-red.log`, the first red attempt, stopped at the probe's own missing `using`; nothing ran.)
