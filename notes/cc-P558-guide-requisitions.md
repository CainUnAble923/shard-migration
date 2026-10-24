# P558: player guide for Requisitions and Leads

Written October 24, 2026. Docs-only source review and player guide draft. Code HEAD at the start: `1c9c5d8bbf9ab4d9a8dd288aace3afff549479dd`. Migration work-copy HEAD: `a352115432407582ddd7d692cc06db38be7600a7`.

## Deliverables and scope

- `notes/wiki-drafts/requisitions.md`: player instructions for opening the board, matching and turning in equipment, tiers and rewards, refresh, Leads, and the Appraiser.
- This file is the work note requested by the inner P558 brief.
- `notes/cc-P558-guide-requisitions-and-leads.md` is the lane note at the path explicitly requested by the unattended wrapper. It links this evidence note and records the final checks.

Read AGENTS.md in both work copies, the migration document index, direction decision, and task list. Reviewed P150, P203, the P422 findings and its review, P515's League comparison, and the October 23 answers in the feature queue. No code, settings, tests, or files under `docs/` were changed. No connection to Haven, deployment, commit, merge, push, or branch change was made. The generated `server/uo/` tree was not read.

## Accepted October 23 behavior

`docs/feature-queue.md:2018` records the League decision sheet. Answers 7 and 8 accept P150's behavior: requests with live Leads survive daily refresh; area, group, and at least 1,000 Fame determine qualifying kills; extra rolls culminate in the 40th qualifying kill guarantee; non-member requisition standing pays immediately. `notes/cc-P515-league-design-vs-build.md`, the October 23 baseline table, independently records how those answers apply.

The guide therefore describes the actual extra roll and guarantee. It does not repeat the older literal 2x natural-loot claim or propose reverting to daily deletion of live Leads. It does not apply League-job standing banking to requisitions. P203 corrected an integration test's selection of the Lead drop and did not change these server rules.

## Source evidence

Paths beginning `C/` are in `ShatteredLegacy/server/customizations/`. References describe this work copy, not the deployed shard.

| Guide claim | Source read |
| --- | --- |
| Per-character requests, saved Lead expiry and kill count | `C/Requisitions/RequisitionData.cs`, `RequisitionEntry` and `CharacterRequisitionData`; `C/Requisitions/RequisitionSystem.cs`, `DataOf` |
| Board entry points, paging, labels, counter range and response-time proximity check | `C/Requisitions/RequisitionsBoard.cs`, `OnDoubleClick`, `OpenFor`, `CanTurnInHere`, `RequisitionsBoardGump`, `RequisitionTurnInTarget`; `C/LeagueRegistrarGump.cs:145`, `:424`; `C/ClusterFGuildSystem.cs:91`, `:1187`, `:1243` |
| Tier is the lesser of membership rank and League gate; non-member tier zero | `C/Requisitions/RequisitionSystem.cs`, `TierFor`; `C/ClusterFGuildSystem.cs`, `GuildRankIndex` |
| Default tiers, League gates, theme examples, no Custodian themes | `C/Requisitions/RequisitionTable.cs`, `BuildDefaults` |
| Three slots per guild, 05:00 UTC, lazy refresh, completed slots wait, live Leads retained | `C/Requisitions/RequisitionSystem.cs`, `DayIndex`, `EnsureCurrent`, `Refresh`; defaults in `RequisitionTable.BuildDefaults` |
| Backpack ownership, one request and item removed, Renown source, immediate standing, Appraiser gold | `C/Requisitions/RequisitionSystem.cs`, `TurnIn`, `GiveGold` |
| Named properties, total count, super slayers, blessed-item refusal | `C/Requisitions/RequisitionItems.cs`, `RequisitionProperties`, `RequisitionMatch.Check`; `C/ArtificersImbueGump.cs:134`, `:799` for intensity and count |
| Ordinary spellbooks are blessed on construction | Read-only `D:/UO/ModernUO-pinned/Projects/UOContent/Items/Skill Items/Magical/Spellbook.cs:122` |
| Three-day expiry, Lead chances by League gate, Fame floor, first-kill chances, area unlocks | `C/Requisitions/RequisitionTable.cs`, `RequisitionLeadRules`, `LeadChancePercent`, `ExtraRollPercent`, `BuildDefaults`; `C/Requisitions/RequisitionLeads.cs`, `TryRoll`, `Attach` |
| Area and group qualification, pet-master credit, integer pity, delivery, repeat drops and independent Leads | `C/Requisitions/RequisitionLeads.cs`, `Qualifies`, `KillerOf`, `DropChancePercent`, `HandleKill`, `Deliver`; item creation in `C/Requisitions/RequisitionItems.cs`, `RequisitionItemFactory.Create` |
| Appraiser menu, quotes, confirmation, blessed refusal and gold-only sale | `C/Requisitions/Appraiser.cs`, `Appraiser.Sell`, `AppraiserGump`, `AppraiserTarget` |
| Named posts and facets; actual placement can skip unloaded maps or unsuitable tiles | `C/Requisitions/Appraiser.cs`, `ClusterFRequisitionSeeder.AppraiserPosts`, `OfficeBoard`, `Seed` |
| Shared price, property count and intensity, default 500 gold cap | `C/Requisitions/RequisitionItems.cs`, `AppraiserPricing`; `C/Requisitions/RequisitionTable.cs`, `RequisitionAppraiserRules` |
| Journal command lists rather than remote turn-in | `C/Requisitions/RequisitionSystem.cs`, `Lines`, `OnPlayerCommand` |

The reward table was transcribed from the actual `BuildDefaults` rows. Its property-count and intensity exceptions for Slayer and AnyMagic requests were checked against `Make` and `RequisitionMatch.Check`. The guide distinguishes request tier labels from individual guild rank names. It explains catalogue-relative intensity without assuming any particular running Imbuing configuration.

## P452: changing soon, not already fixed

Read the actual queued brief at `D:/UO/cc-prompts/claimed/Iron/cc-P452-fix-requisitions-fix-up-appraiser-magic-test.md`, along with `notes/cc-P422-review-requisitions-and-leads.md`. All four underlying source paths still have the reviewed behavior in this work copy. The guide marks each area as changing soon:

1. Ordinary exceptional crafting bonuses currently count as magic. P452 calls for excluding them from eligibility, counts, and pricing for the Appraiser and board, with the final board decision recorded in P452's notes. The player draft describes the change without giving an arbitrage recipe or treating the future board decision as settled.
2. Ordinary spellbooks and necromancy books, including Lead-created books, are currently blocked by the blanket blessed check. P452 queues ordinary-book turn-ins. Its brief explicitly leaves blessed-book Appraiser sales uncertain and defaults to refusing them. The guide promises neither current turn-in success nor future Appraiser acceptance.
3. Refresh currently compares the stored day for equality, allowing a backward day to issue another set. P452 queues monotonic automatic issuance, with staff forcing separate. The draft identifies the timing fix while retaining the intended daily allowance.
4. Null required configuration collections can currently be published before the reload fails. P452 queues refusal before publication and preservation of the old table. The guide gives only the player-facing reliability consequence, with no configuration procedure.

These are existing P422 findings queued for P452, not new defects discovered or fixed by this writing task. No P452 build or live status was assumed from the brief being claimed.

## Verification and limits

Lane tests: none, as requested. No tests or new gates were added, so no red/green cycle was needed. No shard build, container, client, runtime kill/drop, sale, turn-in, or live settings check was run. Runtime availability, actual NPC placement, active tuning, and P452 deployment remain unverified. The guide says this up front and labels its numbers as built-in defaults.

Final formatting, link, size, scope, and progress-reporter results are recorded in the lane note. The draft is plain American English and contains no em dashes.

P558 DONE
