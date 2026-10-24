# P515: the League design against what is built

Reviewed 2026-10-24 against the local `main` snapshots supplied for the 2026-10-23 prompt.
Code: `6f540be8b84f63f76b8852fe638039b363b66a6b`. Migration notes and design decisions:
`d80e795115eafda1946071aadd9d46516b8680ba`. In both work copies, task HEAD equaled local
`main` before this work. No fetch, branch change, server connection, build, or code change was made.
Remote GitHub main and the running shard were not checked.

The League has its registration, rank ladder, signposts, reward shop, Register, consolidation goods,
backpack purchases, requisitions, and much of the mule system. Its main unfinished work is the shared
job framework, player commissions, promotion jobs, and the story chapters. A requisitions board is
built, but it does not implement the designed League job board.

This is a source comparison. **Built** means an implementation and its entry point are present in
the inspected source, not that the feature was deployed or verified in a client. **Partial** identifies
both the working portion and the missing portion. **Not built** means no implementation was found in
the inspected canonical source and callers. **Dropped** means Chase removed it from the design.

Sizes estimate the remaining work, not elapsed time: **none** means no identified implementation gap;
**S** is a local change; **M** is a feature touching several paths; **L** is a subsystem or substantial
integration; **XL** is a sequence of subsystem and content tasks. Estimates overlap and must not be
added together. They are planning judgments, not measured schedules.

Source notation: `C/` means `ShatteredLegacy/server/customizations/`; `P/` means
`ShatteredLegacy/server/patches/`. File and line references are for the code commit above. The read-only
`D:/UO/ModernUO-pinned` exists and is at `d4531cd94b739613155225c234900de9f47d2c88`.
`server/uo/` was not read.

## Design baseline and the October 23 answers

Primary comparisons are `notes/cc-P179-league-design-pass.md`,
`notes/cc-P47-league-research.md`, and `docs/feature-queue.md`, especially F-24, F-33, F-34,
and F-37. The original institution design is
`ShatteredLegacy/design/systems/league_of_extraordinary_citizens.md`. P280's implementation
note records Chase's October 21 answers to P179. Later answers override older proposals.

All nine October 23 answers are in `docs/feature-queue.md:2018` through `:2035`:

| Answer | Baseline used in this report | Effect on the gap list |
| --- | --- | --- |
| 1 | Chapters 4 and 5 are at Blaze (12) and Mythril (15). Other three-rank bands stay as built. | Do not propose moving requisition tiers, loot-box bands, or guild requirements to those chapter ranks. |
| 2 | Six chapters, from Dull Copper through Celestial. | The chapter gates exist; the playable chapters do not. Old references to five trials are history. |
| 3 | Bonuses step at the six named milestones. | Bank growth is built. Job and BOD bonuses remain work. No bonus at every metal rank is owed. |
| 4 | Citizen Commissions: accept at Iron; small posts at Bronze; larger at Verite; public/high-value at Blaze. | Use these names when building commissions. Steel and Silver are not additional ranks. |
| 5 | Shop, Hall page, and backpack purchases are delivered. | P47, P75, and P179 statements that nothing spends Renown are obsolete. |
| 6 | Give players no AP ceiling or title count; name visible titles and keep hidden ones secret. | Do not carry historical AP totals or hidden-title lists into player guidance. |
| 7 | Accept P150's Lead behavior: live requests survive refresh; extra roll and guarantee by qualifying kill 40; area, creature group, and 1,000+ Fame decide qualification. | These are accepted behavior, not fidelity gaps to reverse. |
| 8 | Requisitions pay non-member standing immediately. Banking applies only to League jobs. | Do not retrofit banking into requisitions or existing non-member payouts. |
| 9 | No Warehouse or Featherweight satchels. Clockwork Scavenger remains the League auto-loot reward. | Remove the first two from the backlog. Keep the Scavenger as missing work. This also answers P179's bank question. |

The named milestones are Dull Copper, Bronze, Verite, Blaze, Mythril, and Celestial.
`C/ClusterFLeagueRanks.cs:485` defines their chapter rows. Its generator and
`C/ResourceInfo.cs:9` produce this ladder: Iron, Dull Copper, Shadow Iron, Copper, Bronze, Gold,
Agapite, Verite, Valorite, Platinum, Toxic, Blaze, Frost, Obsidian, Mythril, Adamantium, Celestial.
Dawnstone is excluded by the generator's `LadderExcluded` set.

## Institution, rank, and bonuses

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| Registration open from day one; account registration and character rank | Built | `C/ClusterFLeagueSystem.cs:94` (`JoinLeague`); `C/ClusterFLeagueRanks.cs:228` (`GetRank`); `C/ClusterFAccountData.cs:155` and `:688` | Registration is an account flag. Each character defaults to Iron and keeps its own rank record. No identified implementation gap. | none |
| Generated metal ladder, excluding Dawnstone | Built | `C/ClusterFLeagueRanks.cs:121` (`LadderExcluded`), `:146` (`Generate`), `:485` (`DefaultRows`) | Uses metal names and hues. Renown and guild requirements remain configurable defaults, not a verified balance curve. | none; play tuning unverified |
| Promotion eligibility: lifetime Renown plus standing in enough guilds | Built | `C/ClusterFLeagueRanks.cs:275` (`Evaluate`), `:359` (`CountGuildsAtOrAbove`), `:383` (`TryPromote`); `C/ClusterFGuildSystem.cs:608` (`GuildRankIndex`) | Server checks again before promoting one rank. Spending Renown does not lower eligibility. | none |
| Promotion job at each rank after Iron | Not built; waiver built | `C/ClusterFLeagueRanks.cs:180`, `:318`; `C/ClusterFAccountData.cs:698` (`PromotionDone`) | No gameplay caller records completion of a League promotion job. Stored completion sets and staff properties are hooks. Build jobs and their completion path, then disable the promotion-job waiver. | L, shares job engine |
| Story gate at each named milestone; waive chapters until built | Partial | `C/ClusterFLeagueRanks.cs:184`, `:198`, `:330`, `:485`; `C/ClusterFAccountData.cs:701` (`TrialsDone`) | Per-chapter waivers and checks exist, all waived by default. No playable chapter writes completion. Future chapter builds must allow already-promoted citizens to play for rewards without taking rank away. | M gate integration per chapter; content below |
| Rank page and four eligibility checks | Built | `C/LeagueRegistrarGump.cs:234` (`DrawRank`), `:432` (`BtnPromote` response) | Shows current/next rank and server-side promotion checks. Waived content is shown as not yet required. | none |
| Lifetime Renown distinct from the spendable balance | Built | `C/ClusterFAccountData.cs:653` (`GrantRenown`), `:663` (`CountsTowardLeagueRank`), `:666` (`SpendRenown`) | Citizen Commission Renown is already excluded from lifetime totals by source type. That exclusion does not mean commissions themselves exist. | none for accounting hook |
| Bank grows 100 items per milestone, from 1,000 to 1,600 | Built | `C/ClusterFBankLimit.cs:26`, `:32`, `:40`; `C/ClusterFLeagueRanks.cs:256`, `:252`, `:418` | Uses milestones reached, applies on promotion and login. Full-bank rendering and live limits were not checked. | none; client check remains |
| BOD allowance grows by milestones | Not built | `C/ClusterFSmithBODSystem.cs:56`, `:127`, `:151`, `:190`; `C/Services/BulkOrders/BulkOrderSystem.cs:201` | Smith requests still use fixed small/large caps. No BOD cap caller reads League milestones. Implement the F-24 sizing: one more small allowance at each milestone and one more large at Verite and Mythril, alongside the intended guild-rank allowances. Existing allowance systems need a shared rule. | M |
| League job cap: base 3, rising to 9 at milestones; separate guild caps | Partial | `C/ClusterFWorkOrderSystem.cs:342`, `:377`; `C/GuildContractLedgerGump.cs:490` | Existing work orders preserve three active per guild. No separate League job ledger/cap exists. A multi-guild League job must consume one League slot. | S rule within L job engine |
| Directory League row, welcome line, office sign, ambient greeting | Built in source | `C/ClusterFGuildSystem.cs:909`; `C/ClusterFGuildStarterPath.cs:797`; `C/ClusterFLeagueSystem.cs:147` (`RegistrarPost`); `C/ClusterFRegistrarOfficeSeeder.cs:43`, `:59`; `C/LeagueRegistrar.cs:119` | Directory has a Registrar arrow and welcome names the League. Greeting starts on map arrival and deserialization, fixing P47's concern. Sign seeding defaults off, so placement on the running shard is unverified. | none; world placement check |
| Introductory League teaching and profession referral | Partial, with a newer tutorial implementation | `C/LeagueRegistrarGump.cs` (`DrawWhereToStart`, `DrawGuildReferrals`); `C/ClusterFLeagueSystem.cs:131`; `C/Tutorial/TutorialCoreTrials.cs:53`; `C/LeagueRegistrar.cs:82` | The tutorial observes talking to Elara, and joining is optional. P47's claim of no introduction is too broad now. The original visit-a-guild, return-to-League reward flow is not implemented as a dedicated quest; `FlagIntroCompleted` is still only declared (`ClusterFLeagueSystem.cs:32`). Decide whether the newer tutorial supersedes that old example before commissioning another intro. | S reconciliation; M if the old quest is retained |
| League Dispatch/MOTD | Built for bulletin access | `C/ClusterFLeagueSystem.cs:111` (`OnDispatchRead`); `C/LeagueRegistrarGump.cs` (response 16); `C/ClusterFBulletin.cs` | First-read tracking and bulletins exist. Automated commission highlights, expeditions, and faction/season outcomes wait on those systems. | none for access; M later feeds |
| League Member Pass | Item exists, no issuance found | `C/LeagueMemberPass.cs:20`; Register issuance is `C/LeagueRegister/LeagueRegister.cs:81` | The old pass opens the guild directory, and no normal caller creates it. The Register is the implemented book. Treat the pass as legacy inventory/design cleanup, not evidence of an unbuilt League. | S, optional cleanup |

## Jobs, commissions, and adventuring work

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| Shared framework for League contracts, guild work orders, and Citizen Commissions | Not built as a shared engine | `C/ClusterFWorkOrderSystem.cs` (`WorkOrderDef`, `WorkOrderEntry`); `C/GuildContractLedgerGump.cs:521`; `C/ArtificerWorkOrderSystem.cs:950`; `C/ClusterFSmithCommissions.cs:454` | Existing systems retain separate acceptance, progress, turn-in, and storage. No League world-instance ledger, shared contract state machine, escrow, or common payout path was found. Build P47's engine beside current ledgers first; fold the older systems into it later. | L engine, L later fold-in |
| League board tabs and realm-wide board placement | Not built | `C/LeagueRegistrarGump.cs:130` through `:146`; `C/Requisitions/RequisitionsBoard.cs:53`; `C/GuildContractLedgerGump.cs` | Registrar opens requisitions and guild ledgers, not League/multi-guild job tabs. Requisition board placement does not fulfill League job-board placement. Need the item, menus, offer generation, and checked town/tavern/dungeon locations. | M after engine |
| Gather-after-accept, craft-after-accept, and delivery objectives | Partial reusable building blocks | `C/GuildResources.cs:109`, `:294`; `C/ClusterFCraftRun.cs`; `P/CraftItem-shard-hooks.patch`; `C/ClusterFWorkOrderSystem.cs` | Deliveries can consume pack and bank resources, and taming work has progress. Existing delivery orders do not prove a fresh gather/craft after acceptance. Need persisted objective progress and harvest/craft event routing for League entries. | M after engine |
| Expiry, abandon, rotation, and rank locks for League jobs | Not built for League jobs | `C/ClusterFWorkOrderSystem.cs` (`WorkOrderEntry.AcceptedAt`); `C/ArtificerWorkOrderSystem.cs:1024` (its own abandon); `C/ClusterFSmithCommissions.cs` (`IssuedAt`) | Individual systems have some gates and abandon paths. They do not provide common deadlines, expiry/refund transitions, daily League offers, or League-rank job locks. | M within engine |
| Full standing and currency to each guild on a multi-guild job | Partial precedent, no League implementation | `C/ArtificerWorkOrderSystem.cs:1003` through `:1010`; `C/GuildContractLedgerGump.cs:547` | Artificer work can pay Artificers and Smiths. Ordinary work orders pay their one guild. No reusable list of receiving guilds or League multi-guild job entries exists. Custodian standing is derived from lifetime Clean Up points (`C/ClusterFCustodianSystem.cs:192`), so that guild needs points payout rather than a standing increment that SyncStanding would overwrite. | M with common payout |
| Bank League-job standing and scrip until the guild's Apprentice task | Not built | `C/ClusterFAccountData.cs` (`CharacterGuildData`, `AddReputation`, `AddCurrency`); `C/ClusterFGuildSystem.cs` (`CompleteApprenticeTask`); `C/Requisitions/RequisitionSystem.cs:248` | No pending standing/currency records or Apprentice-task flush path were found. Add versioned records, payouts, display, and reset handling for League jobs only. Requisitions and older direct payouts remain immediate by Chase's answer 8. | M |
| League job Renown, XP, gold, and guild currency | Partial | `C/ClusterFAccountData.cs:653`; `C/GuildContractLedgerGump.cs:547`; `C/Requisitions/RequisitionSystem.cs:248`; `C/Tutorial/ClusterFLoops.cs:37` | Renown/gold/standing paths exist separately. No combined League payout or player XP progression exists. The tutorial's loop counter and level-cap formula are not an XP system; its level/skill reset method is empty. | M payout; L F-12 dependency |
| Solo jobs shareable with nearby party members, full reward to each accepted entry | Not built | `C/ClusterFLeagueBestiary.cs:174` (`OnCreatureDeath`, LastKiller); `C/GuildContractLedgerGump.cs:521`; `C/Companions/CompanionParty.cs` | No accepted shared League entry, range-based objective fan-out, or party job payout exists. Companion follower management is a different feature. Need player-party credit rules and tests; do not pay multiple delivery rewards for one consumed stack. | L |
| Hunts and culls scaled with F-14 creature levels | Partial content and sizing | `C/ClusterFCreatureLevels.cs:41`; `C/ClusterFLeagueBestiary.cs:128`, `:131`; `C/Mobiles/Bestiary/HavenHuntCreatures.cs`, `CullingPackCreatures.cs`, `BestiaryMiniBosses.cs`, `BestiaryParts.cs` | Creature levels, targets, parts, first-kill records, and spawner definitions exist. Hunt/cull tables have no job consumer. Need accepted hunts, species/area kill counting, level-sized offers, turn-in sinks for parts, and party credit. F-14 is no longer wholly absent; the player level source is still provisional. | L job integration/content |
| Slayer requisitions follow an active hunt's family | Hook only | `C/Requisitions/RequisitionSystem.cs:44` (`HuntFamily`), `:194` (`ResolveFamily`) | The delegate is read but no assignment was found. Wire it to active hunts once hunts exist. | S after hunts |
| Dungeon dives: gather, cull, investigate, temporary party mini-boss | Not built as jobs | `C/ClusterFLeagueBestiary.cs:133` and its `Spawners`; `C/Requisitions/RequisitionLeads.cs` | Bestiary mini-bosses have ordinary world spawners. Leads create matching loot opportunities. Neither implements an investigation-owned encounter with party access, engagement timer, cleanup, and dive objectives. | L after engine and encounter work |
| Citizen Commissions: accept/post permissions and escrowed player rewards | Not built | `C/ClusterFAccountData.cs:663`, `:679` are the accounting hook; `C/ClusterFSmithCommissions.cs` is NPC work | Need player postings, requirements, gold/Renown/scrip escrow, fee, expiry, account limits, cancellation, and atomic delivery. Apply Iron/Bronze/Verite/Blaze permissions from October 23. Smith commissions are not Citizen Commissions. | XL including engine |
| Commission safeguards, claims ledger, deletion handling | Not built | `C/ClusterFAccountData.cs` (no commission/claim record); existing `SpendRenown` and guild currency methods | P47's protections still need implementing: same-account refusal, pay/refund once, full-bank claims, deletion cleanup, item validation, fee retention, and currency-only guild rewards. The lifetime-Renown exclusion is already built. P47's fee/limit numbers remain proposed defaults unless separately approved. | L within commissions |
| Client Commissions move from Smiths to League, then other guilds (F-37) | Not built | `C/ClusterFSmithCommissions.cs:454`, `:520`, `:740`; `C/SmithGuildBook.cs:371`, `:420`; `C/SmithCommissionGump.cs` | Still Smith-specific work with Seals/standing, separate caps, and no deadline enforced from `IssuedAt`. Need League routing, low-tier League membership gates and high-tier Society gates, play-earned Renown, the approved three-day deadline/penalty, and Infamy. Infamy's behavior needs its own design/build. | L after engine; Infamy adds L |

## P179: Register, consolidation, and upgrades

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| Free Register at Dull Copper, blessed and character-bound; replacement invalidates old copy | Built | `C/LeagueRegister/LeagueRegister.cs:69`, `:81`, `:332`; `C/LeagueRegistrarGump.cs:417` | Registrar issues it; serial and owner checks identify the current copy. | none |
| Bind books by consuming them; unbind free; capacity 2/4/6/9/12/18 | Built with a deliberate interim path | `C/LeagueRegister/LeagueRegister.cs:44`, `:127`, `:167`, `:193`; `C/LeagueRegister/LeagueRegisterSettings.cs:29` | Smith and Mining books are consumed; guilds without a book bind by membership. A bookless guild cannot yet return a book on unbind. This is P280's recorded accommodation pending P178, not the final all-guild-book design. | M when P178 lands |
| Each bound guild displays the same remote action list as its own book | Not built | `C/LeagueRegister/LeagueRegisterGump.cs:152` (`DrawGuilds`); `C/LeagueRegister/LeagueRegister.cs:242` (`OpenContracts`); `C/GuildMenuGump.cs:1` | Register offers status/contracts/unbind, not a shared per-guild action catalog with action, rank, and price. The template exists; conversion and per-guild books/actions remain. Reuse the eventual catalog rather than copying action implementations. | L across guilds |
| C1 Guild Ledger: all guild rank, standing, currency, next promotion | Partial | `C/LeagueRegister/LeagueRegisterGump.cs:207` (`DrawLedger`), `:309` (`Standing`) | Lists joined guilds and next standing threshold. It breaks when rows reach the bottom, has no paging, and omits skill/trial requirements from the next promotion step. Also derives the displayed rank from reputation alone instead of the full character guild-rank helper. | M |
| Register remains usable as its capacity grows | Partial; source layout limitation | `C/LeagueRegister/LeagueRegisterGump.cs:78` (width/height), `:152` (`DrawGuilds`), `:207` (`DrawLedger`) | Bound rows have no page or height guard. Bind choices and Ledger stop at a height limit without a next page. Bound-row controls extend beyond the declared frame. High-capacity use therefore needs paging/layout work. This is source evidence, not a reproduced client screenshot. | M |
| League remote actions: Bronze contracts; Verite combined turn-in | Partial | `C/LeagueRegister/LeagueRegisterSettings.cs:35`; `C/LeagueRegister/LeagueRegister.cs:242`, `:270` (`TurnInAll`) | Rank gates work. Combined turn-in handles ordinary active work orders plus complete Smith BODs in the top-level backpack. It does not handle Smith client commissions, Artificer special orders, other crafts' BODs, or future League contracts. Extend it through each subsystem's own turn-in method. | M now; later engine integration |
| Blaze repair pass and C10 special-guild-item maintenance | Partial against P179's broader maintenance proposal | `C/LeagueRegister/LeagueRegister.cs:317`; `C/LeagueRegister/LeagueRepair.cs:31`, `:49` | P280 built one pass over worn, carried, and banked `IDurability` gear, plus crafted repair deeds/kits. It does not replenish use-count guild tools such as the Hammer or invoke each bound guild's priced maintenance action. That part still depends on P178's action catalog. | M for guild maintenance |
| C2 League Field Satchel | Built | `C/LeagueRegister/LeagueConsolidation.cs:26`, `:46`, `:84`, `:98`, `:141`; settings `:40` | Holds the existing ore/lumber/hunter/essence satchel families and stops their item totals at the wrapper. Bronze, 5,000 Renown plus 500 gold; each merge costs 50 of its guild's currency. Guild reduction/cap behavior remains in the contained satchels. This is consolidation, not the dropped Featherweight reward. | none; full gathering/client flow unverified |
| C3 Combined Logbook | Built for the existing mining and forestry logs | `C/LeagueRegister/LeagueConsolidation.cs:60`, `:162`, `:186`; settings `:47` | Dull Copper, 500 Renown plus 50 gold. Deletes carried old logbooks and opens their existing record views. Future hide/cloth logs will need additional routes when those logs exist. | none now; S per future log |
| F-34 bank ledger folded into Register; per-guild craft-from-bank links | Base built; upgrades not built | `C/LeagueRegister/LeagueRegisterGump.cs:23` (`LeagueBank`), `:243` (`DrawBank`); `C/GuildResources.cs:4`; `P/CraftItem-shard-hooks.patch` | Bank page summarizes materials and checks. No per-guild links, purchased resource permissions, or bank/town/anywhere crafting range tiers were found. Work-order bank consumption is not crafting-from-bank. Keep this separate from the mule's portable bank, which already exists. | L crafting count/consume integration |
| Backpack purchases: 150/175/200/250 at Bronze/Verite/Blaze/Mythril | Built | `C/LeagueRegister/LeagueRegisterSettings.cs:55`; `C/LeagueRegister/LeagueBackpack.cs:18`, `:60`, `:115`; `C/ClusterFAccountData.cs:715` | Sequential purchases cost 2,000/6,000/15,000/30,000 Renown plus configured gold. Saved character tier is reapplied at login/world load. Item count only, no weight purchase. | none; 250-item client rendering unverified |
| Currency: Renown first, small gold cost; guild money for guild components | Built for P280 goods | `C/LeagueRegister/LeagueBackpack.cs:143` (`LeaguePrice`); `C/LeagueRegister/LeagueConsolidation.cs:141` (`Merge`) | Renown/gold pricing and guild merge fees exist. It is not P47's general multi-currency/material transaction helper. | none for goods; general helper below |
| Follow guild membership live; clear state on staff reset | Partial | `C/LeagueRegister/LeagueRegister.cs:112` (`DropLeft`); `C/ClusterFGuildSystem.cs:1302` (`DoReset`); `C/ClusterFDevTools.cs:207` | Left guild is shown once and removed at Register open. Dev League reset clears League records. `ResetGuild` does not immediately clear bound keys; an intervening rejoin before opening retains the binding. P179 specified reset-time key cleanup as well. No player League-leave/reissue-to-bank flow exists; that was conditional future behavior. | S reset cleanup; M if player exit is commissioned |
| C5 League BOD book | Core capability already built outside League | `C/Services/BulkOrders/BulkOrderBooks.cs:18`; `P/BOB-all-crafts.patch:15`, `:84`; pinned `Projects/UOContent/Engines/Bulk Orders/Books/BulkOrderBook.cs:112` | Stock book already holds mixed crafts; shard patch adds the other crafts and filters. No special Bronze/2,500-Renown League product was found. P179 listed it as later work. Decide whether a separate product adds anything before building one. | S shop wrapper if retained |
| C6 Guild Toolroll | Not built; later proposal | `C/LeagueRegister/LeagueConsolidation.cs`; existing guild tools remain separate items | No carried toolroll or remote access to tools inside one was found. Needs contained-tool interaction rules and capacity behavior, not just a container graphic. | M if retained |
| C7 Retire Compact Dispatch Ledger | Not done; candidate cleanup | `C/ClusterFGuildSystem.cs:461`; `C/MinersCompactLiaisonGump.cs:807`; `C/LeagueRegister/LeagueRegister.cs:47` | It is still issued/replaced and used as Mining's bindable book. Retire only with P178/its replacement so existing access is preserved. | S with book conversion |
| C8 Starter stock-tool deduplication across guilds | Not built | `C/ClusterFGuildStarterPath.cs:290`, `:297` (`kitTypes`) | Deduplication set is local to one guild's kit. It does not inspect tools from a previously joined guild. | S |
| C9 Combined salvage/trash carried bag | Not built as a League item; later proposal | `C/SmithGuildSalvageBag.cs`; `C/TrashBag.cs`; `C/Mobiles/Mule/MuleModules.cs:752` | Existing carried bags remain separate. Mule Salvage Bin already provides a related combined function on the mule; do not count that as a new carried League bag. | M if retained |
| C11 Commodity deeds sold by Registrar | Not built as a League service; stock capability exists | `C/LeagueRegistrar.cs:23` (BaseCreature); `C/LeagueShop/LeagueShop.cs:92`; pinned `Projects/UOContent/Items/Deeds/CommodityDeed.cs` | No Registrar commodity-deed sale or Copper gate found. Reuse stock deeds if this later proposal is kept. | S |
| Sell bank capacity, weight reductions, house storage, stat/skill caps | Dropped, reserved, or explicitly outside this purchase plan | `C/ClusterFBankLimit.cs:40`; `C/LeagueRegister/LeagueRegisterSettings.cs:55`; `C/LeagueShop/LeagueShop.cs:92` | No Warehouse or Featherweight work is owed. Bank growth belongs to milestones; weight to existing satchels/Strength; mule capacity to mule tiers. House storage was later consideration. Stat/skill caps are not League purchases. | none |

## Reward shop, requisitions, and the mule

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| F-13 Renown shop, AP gates, titles, Hall rewards | Built; accepted delivered October 23 | `C/LeagueShop/LeagueShop.cs:92`, `:134`, `:153`; `C/LeagueShop/LeagueHall.cs:120`; `C/LeagueShop/LeagueShopGumps.cs`; `C/LeagueRegistrarGump.cs:409` | Purchases spend the balance, not lifetime Renown. Hall entries use the same purchase path. The achievements/shop AP figure is the player's earned score, not a promised content ceiling. Future F-12 level gates are a progression integration, not a reason to mark this delivered shop missing. | none for delivered scope |
| Visible title guidance without AP ceiling or title count | Built in title picker; documentation rule adopted | `C/LeagueShop/LeagueShop.cs:335`; `C/LeagueShop/LeagueShopGumps.cs:377`, `:407` | Visible names are the Registered Adventurer, the Veteran of the League, the System's Favorite, the Noted, the Accomplished, the Distinguished, the Renowned, and the Illustrious. Hidden titles are omitted until held. Do not publish a fixed AP ceiling. | none |
| F-47 requisitions and Appraiser | Built | `C/Requisitions/RequisitionSystem.cs:99`, `:114`, `:214`; `C/Requisitions/Appraiser.cs:131`; `C/Requisitions/RequisitionsBoard.cs`; `C/LeagueRegistrarGump.cs:424` | Daily guild-themed requests, tier gates, magic-item validation, Renown/standing/gold pay, and appraisal exist. They do not need League-job escrow, a three-to-nine active cap, or delayed non-member standing. | none under October 23 ruling |
| F-48 Leads, kept requests, extra roll, pity guarantee | Built; accepted behavior | `C/Requisitions/RequisitionSystem.cs:134`; `C/Requisitions/RequisitionLeads.cs:161`, `:210`, `:250`; `C/Requisitions/RequisitionTable.cs:71` | Area/group/Fame qualification and default guarantee at qualifying kill 40 match the answer. Live Lead survives refresh. No literal doubling-of-stock-loot or loot-table qualification patch is owed. Actual settings and live drop behavior are unverified. | none |
| F-33 base mule earned at League; tiers, saved breeding and bloodlines | Built in source | `C/Mobiles/Mule/MuleErrand.cs:30`, `:96`, `:108`; `C/Mobiles/Mule/MuleData.cs:56`; `C/PackMule.cs:367`; `C/PackMuleBreedingSystem.cs:66`; `C/BredPackMuleDeed.cs:59`; `C/Mobiles/Mule/MuleGenes.cs` | Errand gives a bonded tier-one mule; exchange upgrades it. Tier rows, genes, saved pregnancy handling, and follower recount replace P47's old mule description. No new core build is owed by that historical report. Breeding was not exercised here. | none for core presence |
| Mule errand leads into first Haul contract | Hook only | `C/Mobiles/Mule/MuleErrand.cs:37`, `:129` (`FirstHaulContract`) | No assignment found. Collecting the mule falls back to the message saying hauling work will come later. Build F-38 hauling and assign the first-contract hook. | M after job engine |
| Multi-reputation upgrades requiring ranks in multiple guilds | Partial, narrower than P47 | `C/Mobiles/Mule/MuleUpgrades.cs:17`, `:26`, `:58`; `C/Mobiles/Mule/MuleModuleGumps.cs:483`; `C/GuildResources.cs:294` | Mule steps consume multiple guild currencies but gate rank only in Mining. Schematics gate their issuing guild and charge Mining Vouchers too. No generic multi-guild rank/material requirement record exists. Several currencies are not proof of ranks in several guilds. | M reusable rule and first converted steps |
| Atomic common multi-currency payment; mining/lumber/ranger upgrade follow-through | Partial | `C/Mobiles/Mule/MuleUpgrades.cs:126`; `C/GuildResources.cs:294`; `C/JacobsProspectorPickaxe.cs:315`, `JacobsDeepdelverPickaxe.cs:317`, `JacobsWorldbreakerPickaxe.cs:320` | Exchange now calls MuleUpgrades, but that code subtracts scrip before calling gold consumption and ignores the result. General GuildResources payment still takes one guild currency. Existing pickaxe paths remain single-guild payment. Generalize checks/payment and wire the subsequent F-33 items; do not assume this is done because the exchange has a table. | M helper; M per item family |
| Mule module items, attach/detach, learned schematics and crafting | Built | `C/Mobiles/Mule/MuleModule.cs:117`, `:245`, `:281`; `C/Mobiles/Mule/MuleModules.cs:122`, `:153`, `:175`; `C/Mobiles/Mule/MuleModuleGumps.cs:483`, `:539` | Rank-gated schematics teach an account recipe once. This follows Chase's later October 5 decision; P47's consumed-schematic proposal is obsolete. Module effects have the separate gaps below. | none for module framework |
| P47's difficult vendor-selling module | Built by a custom sell flow | `C/Mobiles/Mule/MuleModuleGumps.cs:305` (`MuleSell`), `:343`; `C/Mobiles/Mule/MuleModuleData.cs:118` | Trader's Ledger sells cargo and has a portable-bank tier. P47's old vendor patch/own-flow question is no longer an unbuilt feature. | none for presence |
| Remaining mule module effects | Partial | `C/Mobiles/Mule/MuleModuleData.cs:60`, `:80`, `:123`, `:127`; `C/Mobiles/Mule/MuleModules.cs:244`; `C/Mobiles/Mule/MuleModule.cs:117` | Ore Hopper III's mining gem proc is unwired; Field Medic II's extended bandage range is pending; Steady Hoof dismount resistance is stubbed; Imbued Barding has socket storage/effects but no gameplay socket-filling route. Load Harness II also promises bag sorting, but its only effect consumer adds pack weight and no sorting path was found. These are separate follow-ups, not an absent module framework. No effects were runtime-tested here. | S gem proc; M bandage/dismount/socket/sorting paths |
| Clockwork Scavenger granted by League; backpack loot redirected by Load Harness III | Not built; redirect claim not verified | `C/Mobiles/Mule/MuleModuleData.cs:69`; `C/Mobiles/Mule/MuleModules.cs:256`; `C/Mobiles/Mule/MuleModuleGumps.cs:52` | No League reward/creature acquisition or auto-loot implementation found. The table claims a redirect hook exists, but the Load Harness consumer only adds pack weight; no redirect implementation or caller was found. Build and verify both the reward and its mule destination, per October 23 answer 9. | M to L, needs reward and looting rules |
| Follower curve permits full party at intended loop milestones | Curve built; integration and calibration missing | `C/Companions/CompanionSettings.cs:88`, `:121`; `C/Companions/CompanionParty.cs:81`, `:146`; `C/Mobiles/Mule/MuleModules.cs:260`; `C/Mobiles/Evo/EvoPet.cs:78`; `C/Tutorial/ClusterFLoops.cs:25` | No assignment to OwnerLoopProvider was found, so this curve reads loop zero even though tutorial loop storage now exists. It also retains P47's evo cost placeholder of three while EvoPet actually costs one slot. Reconcile companion ranks, actual evo costs, and Legacy slots before claiming the loop-11/21 targets work. | M integration/calibration; F-12 dependency |

## Story and private trial maps

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| Private trial-map pool and lifecycle | Not built | `C/ClusterFLeagueRanks.cs:184` only supplies waivers; source search found map lookups but no League map registration/run manager | Need stable map indexes, private run ownership, region travel restrictions, party entry/exit, death/logout/restart recovery, pet/corpse cleanup, and reset. P47's implementation proposal is research, not code. Existing tutorial trials run a different lesson system. | L foundation |
| Six blade/ring story chapters | Not built | `C/ClusterFLeagueRanks.cs:485` has chapter numbers; `C/Tutorial/TutorialCoreTrials.cs:53` has introductory League/vision lessons | Pommel, Grip, Crossguard, Blade, Point, and Ring have no League quest objectives, chapter rewards, or completion writers. Existing dungeons and a loop vision are useful foundations, not completed chapters. Follow the named chapter gates, not the obsolete every-third-rank wording. | XL; one chapter at a time after foundation |
| Keeper/Breaker permanent choice, echo/retained skills, title/cosmetic, seasonal tally | Not built as a progression system | `C/Tutorial/ClusterFLoops.cs:37` (`ResetLevelAndSkillsForF12` is empty); chapter completion storage in `C/ClusterFAccountData.cs:701` | No League choice record, echo progression, retained-skill reset implementation, or seasonal tally consumer found. Use the later F-12 decisions for Keeper/Breaker curves and the loop-21 capstone; the older storyline still contains superseded proposals. Do not confuse Keeper profession-guild code with this choice. | L progression plus chapter 5 |
| Setting dungeon, loop-opened floors, Unbroken ending and Hall of Legacies | Not built | `C/Tutorial/ClusterFLoops.cs:31` supplies a cap formula; no League Setting/Hall progression implementation found | Need chapter 6's private dungeon and routes, loop-based floor access, final crest/title rewards, and permanent records. The reward shop's Hall page sells house decor and does not implement the Hall of Legacies. | XL, downstream of F-12 and story |

## Findings that change the next prompt

The useful starting point is P47 batch 2, updated for the code that now exists. Preserve the guild ledgers;
build the common contract/payout records and the separate League cap; then add the board, non-member
banking, and promotion jobs. Reuse existing craft/harvest hooks and inspect the available death-credit
paths before deciding on any pinned patch. P47's 2026-10-03 patch estimates are not a current patch plan.

Citizen Commissions should follow that engine and retain their own escrow/claims work. NPC Client
Commissions remain a separate design and integration task. Neither is implemented by requisitions.

P179's remaining book work centers on P178 integration, full-guild paging, missing turn-in routes,
and F-34 crafting from the bank. C5's mixed-craft BOD capability already exists. C6/C9/C11 remain later
proposals, not newly approved mandatory builds. No Warehouse or Featherweight task should be created.

For the follower target, do not simply wire the old curve and declare victory. At a top companion cost
of three, five companions use 15 slots. With the current one-slot evo and one-slot mule, the total is
17; the current curve reaches 17 at loop 10. This is a conditional source calculation, not an observed
play result, and shows why P47's old three-slot evo assumption must be rechecked. The unassigned loop
provider currently prevents even the intended curve from tracking tutorial loop state.

The missing League gameplay and the Register/mule follow-ups are shard-owned work. They are not
ServUO defects to copy or confirmed ModernUO defects to report. Source-derived limitations are
identified as such; this audit does not claim a reproduced runtime cause.

## Verification and limits

Read both work copies' AGENTS.md, the migration document index, direction decision, and task list.
Read P47, P179, P280, P376, the League institution design, the storyline draft, and the relevant
feature-queue decisions. Traced implementations and normal entry points in canonical customizations
and patches. Used `git grep`/tracked-file lists after `rg` proved unavailable. Searched gameplay writers,
callers, state records, and related behavior, not just proposed type names. In particular, searched for
promotion/trial completion writers, job/commission state, pending payouts, map registration, hunt-family
and first-Haul delegate assignments, loop-provider assignments, and Renown spenders.

Existing test files inspected as supporting evidence, not newly run proof:
`server/tests/Misc/LeagueLadderVerification.cs`, `LeagueSignpostsVerification.cs`,
`LeagueRegisterVerification.cs`, `LeagueShopVerification.cs`, `LeagueHallVerification.cs`,
`RequisitionsVerification.cs`; `server/tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs`;
`server/tests/Mobiles/Mule/MuleVerification.cs`, `MuleModuleVerification.cs`; and
`server/tests/Mobiles/Companions/CompanionBaseVerification.cs`.
No tests were added or changed. No lane tests were requested. No build or game test was run for this
documentation-only comparison. Existing tests do not by themselves establish full client flows or
prove completion of the missing systems.

Unverified: the latest remote main, deployed image, live configuration overrides, world seeding,
client rendering, full-bank/backpack behavior, ordinary-player breeding/module flows, trial-map
resource costs, and economy balance. Sizes are estimates. This report does not assert that missing
features need the exact patches or line counts proposed in historical research. No Haven connection
was made and nothing was deployed.

P515 DONE
