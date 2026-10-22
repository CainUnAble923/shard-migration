# P382: player guide to the Order of the Alembic

Run date: October 21, 2026, America/Chicago. Codex lane, unattended.

## Scope and output

Created `notes/wiki-drafts/order-of-the-alembic.md`, following P374's League guide: short player-facing paragraphs and tables, built behavior separated from decided plans, Sources and Contradictions at the end. No code changes, new tests, deployment, publishing, Haven connection, commits, branch changes, or edits under `docs/`.

The user explicitly requested Markdown files, so no Page/Space writing workflow applies. Work-copy paths supplied in the prompt replace the historical paths in the agreements. The prompt's current no-commit and no-docs-edit rules override older commit/push instructions.

## Reading and discovery

Read the work copies' root `AGENTS.md`, migration `docs/README.md`, `docs/direction-decision.md`, and `docs/tasks.md`. Read `notes/wiki-drafts/league.md` as the model. Consulted the relevant F-9, F-20, F-43, F-49, and F-51 feature-queue sections directly, not just keyword hits. No nested tracked AGENTS files were listed for the note destination.

Searched the top-level `notes/cc-P*.md` files for both the full guild name and the broader `alembic` term. The latter also catches indirect references. Read the guild-related portions and surrounding context of every matching note listed below, with deeper reads of P77/P78, P123, P151, P260, and P265. The other systems in large mixed-topic notes were outside scope.

| Note read | Relevant material |
|---|---|
| `cc-P77-alembic-guild.md` | Guild foundation, hall, data, rank proposals, outstanding decisions, tests. |
| `cc-P78-recipe-gating.md` | Research, recipe ownership, band counts/merging, promotion, gifts, shop, tests, defaults. |
| `cc-P118-port-bulk-orders.md` | Proposed giver mapping and decision boundary; no implementation in that run. |
| `cc-P123-port-bulk-orders-crafts.md` | Built Alchemy orders, member-only guildmaster, payouts, reward placeholders, tests. |
| `cc-P146-playtest-decisions-inbox.md` | P77/P78 outstanding naming and progression choices. |
| `cc-P150-requisitions-and-leads.md` | Order theme row and requisition behavior. |
| `cc-P151-guild-halls-survey.md` | Summary and section 18 Papua candidates, uncertainties, questions. |
| `cc-P177-guild-menus-template-mockups.md` | Alembic crest stand-in, generic hall page, mockups do not change service behavior. |
| `cc-P217-crystal-wiki-catch-up.md` | Guild and recipe inventory, evidence references, historical use of "live". |
| `cc-P218-crystal-mage-crafter-scripts.md` | Herbalism absent, ordinary reagent handling, recipe gate. |
| `cc-P260-herbalism-research.md` | Headlines; plant and bed status; reagent sources; currency, plots and rank; phased plan and code-forced questions. |
| `cc-P265-guild-hall-decor-packs.md` | Status, registered art and templates, no world placement, screenshot continuation. |
| `cc-P286-crystal-mage-crafter-docs-and-tests.md` | Herbalism still unbuilt; craft ceiling limits. |
| `cc-P377-crystal-wiki-catch-up-2.md` | Decor status and exclusion of staff-only material from player pages. |
| `cc-P378-playtest-plans-10-21.md` | Hall placement/appearance plans are proposed checks, not passed client evidence. |

`rg` was unavailable, so discovery used PowerShell `Select-String` and Python reads. An initial recursive notes listing encountered denied scratch-cache directories under `notes/__pycache__/p378-test-temp`; the required CC notes were subsequently enumerated directly at the notes root, without entering caches. This did not prevent reading any required matching CC note. No generated `server/uo/` tree was read.

## Evidence ledger

Unless prefixed PIN or migration, paths below are relative to ShatteredLegacy. PIN means `D:/UO/ModernUO-pinned/Projects/UOContent`, read-only. Line numbers were checked in the work copy during this run.

| Page claim | Source evidence |
|---|---|
| Guild identity, currency, placeholder names | `server/customizations/ClusterFAlembicGuild.cs:35`, `:41`, `:43`, `:46`; NPC name `:149`, guild key `:163`. |
| Alchemy/Taste ID ownership | `server/customizations/ClusterFGuildStarterPath.cs:48`, `:50`; recipe owner is Alchemy only at `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:389`, `:396`, `:405`. |
| Free, per-character join | `server/customizations/ClusterFGuildSystem.cs:309`, `:314`, `:427`; new craft members start tracking at `:448`. |
| Starter kit and once per character | `server/tests/Misc/AlembicGuildVerification.cs:128`, `:142`, `:143` through `:146`; `server/customizations/ClusterFGuildStarterPath.cs:282` through `:325` starter-tool receipt path. |
| Apprentice task, tribute only if skill unmet | `server/customizations/ClusterFGuildSystem.cs:279` through `:287`, `:355`, `:382`, `:400` through `:418`. Counts/pay are data, not inferred from prose. |
| Standing ladder, task bump, effective rank | `server/customizations/ClusterFGuildSystem.cs:618`, `:628`, `:662`, `:669`; `server/customizations/ClusterFGuildPromotion.cs:56`, `:68`, `:85`, `:150`. Task completion is not a bypass of the craft skill cap. |
| Skill thresholds, waived top trial, durable promotions | `server/customizations/Engines/Craft/ClusterFRecipeTable.cs:75`; `server/customizations/ClusterFGuildPromotion.cs:33`, `:79`, `:97`, `:150`, `:162`. |
| Actual book grants and shop availability | `server/customizations/ClusterFGuildPromotion.cs:173`, `:182` through `:197`; `server/customizations/Engines/Craft/GuildRecipeShopGump.cs:25`, `:42` through `:49`. Both apply MergedBand inside the rank loop. |
| Band pricing and merge threshold | `server/customizations/Engines/Craft/ClusterFRecipeTable.cs:36`, `:41`, `:54`, `:57`, `:108`; `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:171`, `:205`, `:222`. Static catalog audit below. |
| Grandmaster rotation and Legendary gift need eligible designs | `server/customizations/Engines/Craft/GuildRecipeShopGump.cs:52`, `:77`; `server/customizations/ClusterFGuildPromotion.cs:199` through `:218`; `server/customizations/Engines/Craft/ClusterFRecipeRewards.cs:37`, `:40` through `:58`. Own-recipe items do not join the Band V pool. |
| Pattern visibility and separate recipe gates | `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:126`, `:135`, `:145`, `:153`; `server/patches/CraftGump-recipe-gating.patch`; separate keys for softened reeds in `AlchemyCraftRegistrations.cs:17`. |
| Tradeable unread account books/scrolls, consumed once | `server/customizations/Engines/Craft/RecipeItems.cs:1`, `:26`, `:40`, `:49`, `:81`; account sync in `server/customizations/Engines/Craft/ClusterFRecipeStore.cs:147`, `:168`, `:182`. |
| Additional Alchemy crafts | `server/customizations/Engines/Craft/AlchemyCraftRegistrations.cs:57`, `:101` through `:115`; `server/customizations/Engines/Craft/ExodusCraftRegistrations.cs:88`, `:94`. Individual scroll-backed recipes exist too; the page does not promise that every ingredient is obtainable. |
| Taste ID targets and effects | PIN `Skills/TasteID.cs:35` through `:69`; shard's gain extension identifies the food roll at `server/customizations/ClusterFSkillGain.cs:385`. No claim of a new guild ability or poison immunity. |
| Glassblowing book, tool, skill, forge, sand | PIN `Items/Skill Items/Specialized/GlassblowingBook.cs:18` through `:37`; `Engines/Craft/DefGlassblowing.cs:18`, `:38`, `:48`, `:103`; `Mobiles/Vendors/SBInfo/SBGlassblower.cs:40` through `:42`. |
| Glassblowing shared unlock, separate craft system | `server/customizations/Engines/Craft/ClusterFRecipeStore.cs:147` through `:182`; band exemption `ClusterFRecipeGate.cs:68` through `:77`; PIN `DefGlassblowing.cs:7`. Character skill 100 is still checked each time. Guild shop rows contain only band-gated skills, not a Glassblowing book. |
| Orla offers Alchemy BODs to members with skill above 0 | `server/customizations/Services/BulkOrders/BulkOrderGivers.cs:29`, `:38`, `:90`, `:135`, `:240`; `server/customizations/Services/BulkOrders/BulkOrderVendors.cs` Alchemist partial. |
| BOD payouts are gold, Fame, craft points | `server/customizations/Services/BulkOrders/BulkOrderVendors.cs:301` through `:367`, especially `:336` through `:359`; claim paths `:158` through `:182`. No AddCurrency/AddReputation in this payout. |
| Available Alchemy BOD rewards, placeholders | `server/customizations/Services/BulkOrders/BODRewardCollections.cs:289` through `:308`: 250-use mortar at `:291`, dyes `:295`, `:305`, `:307`, talismans `:298`, `:301`, `:304`. Placeholder rows have no purchase button: `server/customizations/Services/BulkOrders/BODRewardsGump.cs:76`, `:88`. |
| Requisition interests and payments | `server/customizations/Requisitions/RequisitionTable.cs:269` through `:273`; `server/customizations/Requisitions/RequisitionSystem.cs:3` through `:14`, `:225` through `:264`, `:301`. No Drams payout. |
| No additional Alembic work-order currency route verified | `server/customizations/ClusterFWorkOrderSystem.cs:349` through `:355` registers the existing guilds; its guild-key definitions contain no alembic order. Repository search of AddCurrency call sites found the generic Apprentice payment, specific other-guild paths, and generic ledger completion, but no Alembic work-order definition. Page advertises only the confirmed Apprentice Drams award. |
| Herbalism remains planned | migration `docs/feature-queue.md:3450` through `:3555`; `server/customizations/Tutorial/TutorialStations.cs:108` explicitly says not built; source-wide Herbalism search produced no skill or harvest implementation. P218 and P286 agree. |
| Existing reagent pickups are distinct from planned herb gathering | migration `notes/cc-P260-herbalism-research.md:256` through `:300`; independently checked `D:/UO/ModernUO-pinned/Distribution/Data/Spawns/shared/trammel/Reagents.json:14` through `:22`, PIN `Mobiles/Monsters/Arachnid/Melee/GiantSpider.cs:43`, and the shard's shared-spawn import folders at `server/customizations/ClusterFStockSpawnData.cs:13`, `:17`. Actual running spawns remain unverified. |
| New Haven post and planned Papua headquarters | `server/customizations/ClusterFGuildStarterPath.cs:233`; `server/customizations/ClusterFAlembicGuild.cs:15`, `:63`; migration `docs/feature-queue.md:3394` through `:3435`; `notes/cc-P151-guild-halls-survey.md:330` through `:347`. |
| Decor preparation is not a placed hall | `server/customizations/GuildHallDecor/GuildHallDecorSeeder.cs:1` through `:17`, `:34` through `:47`; P265 status paragraphs. No location or live appearance inferred from art registration. |

## Catalog audit: why the page says Bands II and III

This is a static source audit under the built-in recipe table and the shard's stated SE/SA/TOL expansion coverage, not an executed server catalog query. Enumerated the actual AddCraft entries, then applied `BandOf`, the exclusion of entries with their own recipes, and `MergedBand`'s raw-band counts. Alchemy referrer search covered customizations, patches, and tests to find additive registrations; it was not limited to filenames containing "Alchemy".

Files supplying the non-own-recipe entries counted here:

- PIN `Engines/Craft/DefAlchemy.cs`.
- `server/customizations/Engines/Craft/AlchemyCraftRegistrations.cs`.
- `server/customizations/Engines/Craft/ExodusCraftRegistrations.cs`.

The complete item list beside each count follows. DefAlchemy line numbers are PIN; the other two filenames are the customization paths immediately above.

| Raw band | Count | Actual entries, with source line |
|---|---|---|
| Free | 12 | DefAlchemy: RefreshPotion 93, TotalRefreshPotion 95, AgilityPotion 109, NightSightPotion 125, LesserHealPotion 139, HealPotion 141, StrengthPotion 147, LesserPoisonPotion 173, PoisonPotion 185, LesserCurePotion 213, CurePotion 215, LesserExplosionPotion 221. |
| I | 4 | DefAlchemy: GreaterAgilityPotion 111, GreaterStrengthPotion 159, ExplosionPotion 233; AlchemyCraftRegistrations: PlantPigment 105. |
| II | 9 | DefAlchemy: GreaterHealPotion 143, GreaterPoisonPotion 187, GreaterCurePotion 217, GreaterExplosionPotion 245, ConflagrationPotion 265, GreaterConflagrationPotion 278, ConfusionBlastPotion 292, GreaterConfusionBlastPotion 305; AlchemyCraftRegistrations: ElixirOfRebirth 57. |
| III | 8 | DefAlchemy: DeadlyPoisonPotion 199, SmokeBomb 260; AlchemyCraftRegistrations: NaturalDye 101, ColorFixative 108, CrystalGranules 112, SoftenedReeds 114; ExodusCraftRegistrations: NexusCore 88, GoldDust 94. |
| IV | 0 | None among the enumerated entries. |
| V | 0 | None among the enumerated entries. |

Own-recipe paths checked separately, excluded from book counts and Band V rotation: Eodon potion entries in `AlchemyCraftRegistrations.cs:63` through `:95` call AddRecipe; Thief's Smoke Bomb in `ThievesDenCraftRegistrations.cs:68` through `:75` has its own recipe; Field Medic Pack in `Mobiles/Mule/MuleModule.cs:195` uses AddQuestRecipe at `:281`. Its main skill and secondary Healing requirement do not make Taste ID a promotion skill, nor do they create an Alembic-owned mule schematic.

With merge-below 5, raw Band I folds into II. II and III remain separate, IV has no entries. Shop loop rank 0 already processes raw band 1 and offers the merged II book; rank 2 reaches raw band 3 and offers III. Promotion rank 1 offers II and rank 3 offers III. Rank 2 can hand over II again if the account has not actually learned it; the page does not advertise duplicate unread grants. Rank 4 has no eligible book and rank 5 has no eligible Band V design. Prices are the resulting book band's price: II 200, III 400, not the raw band's price.

No new test was created for this reading task. This static audit is not a claim that an Alchemy-specific integration test passed.

## Contradictions left on record

These also appear in player language at the end of the draft. No decision or code was changed to settle them.

1. **Previous owning guild:** feature-queue F-20 `:1728` says Alchemy moved from Arcane Society; F-9 `:758` and P77 say it moved with Taste ID from Healers' Covenant.
2. **Apprentice task versus promotion:** P77's task-lifts-rank description and its untracked-data rank test (`AlembicGuildVerification.cs:210` through `:222`) differ from a newly joined, tracked character under P78. `CompleteApprenticeTask` sets the flag at any skill if tribute is paid, while `CapFor` and `Effective` retain rank 0 below Alchemy 30. Page distinguishes task completion from actual promotion.
3. **Book catalog and merged-rank behavior:** P78's historical Alchemy row reports I=3, II=8, III=2, books II/IV, and its prose says merged IV sells at rank 3 and grants at 4. Later Alchemy registrations change the actual raw counts; separately, the loops apply MergedBand before checking availability, allowing shared books at the earlier raw-band rank. Page records the source-derived default behavior, leaving the old note intact.
4. **Bulk-order availability:** P77/P78 say no Alchemy issuer exists; P123 and current giver/vendor code implement one. This is a historical status disagreement. Guild-currency reward intentions do not describe the current Alchemy turn-in path, which pays craft points, gold, and Fame.
5. **Glassblowing menu:** P77 says book unlock "inside the Alchemy menu"; PIN uses DefGlassblowing and Blowpipe separately, with Alchemy as MainSkill. The guild pattern shop does not stock the stock unlock book.
6. **Reagents only from vendors:** F-51 `:3457` states the premise; P260 section 4 records wild spawners and creature sources. Existing ground pickups do not establish the planned Herbalism system.
7. **Herbalism design closure:** F-51 `:3553` says no open design questions; P260 `:514` through `:546` retains code-forced decisions. No yield, upkeep, plot limit, rent, or familiar upgrade numbers were promoted into the guide.

## Verification and limitations

Read, rather than ran, the existing guild tests in `server/tests/Misc/AlembicGuildVerification.cs`, recipe promotion/shop/account tests in `server/tests/Engines/Craft/RecipeGatingVerification.cs`, and Alchemy giver/payout tests in `server/tests/Services/BulkOrders/BulkOrderCraftsVerification.cs:584` through `:615`. Their relevant assertions support kit, owner, membership, rank plumbing, account learning, recipe purchase, and BOD payouts. The early Alembic rank test creates CharacterGuildData directly and does not itself prove the skill cap for a new member. No new tests were needed or added; lane tests are none, as requested.

Unverified: running-world placement of Orla or decor; deployed configuration overrides and prices; player-package publication; appearance in a client; actual in-game delivery of the newly audited merged Alchemy books; sources for every specialized potion ingredient; and any post-October-21 implementation outside these work copies. Historical notes calling features "live" were not treated as a live-server check. No staff instructions, exploits, or hidden-achievement spoilers were copied into the page.

Validation completed:

- Read back the draft and checked every topic against the evidence ledger and the static catalog audit. Pinned source HEAD is `d4531cd94b739613155225c234900de9f47d2c88`, matching the agreed pin.
- All draft Markdown links resolve to existing local files. Sources and Contradictions are the final sections. The page contains no em dashes or other non-ASCII punctuation, staff commands, exploits, or hidden-achievement details.
- Both new files are well below 5 MB. Reviewed whitespace and repository status; only the requested guide and work note are new, and the code work copy remains clean.
- No tests were added or run for this docs-only task. Existing test results in earlier notes were not presented as runs performed here. Tool shell reports Windows PowerShell 5.1.26100.9444; no PowerShell 7 script or syntax was used.
- Ran the progress reporter's main routine with `--dry-run` and `SL_SHARD`/`SL_MIGRATE` pointing at these work copies. It completed. Inspection found that `build()` still attempts to write `tools/progress.json` even with `--dry-run` (`tools/progress.py:722`, before the main return at `:737`), so the invocation intercepted that one Path.write_text call in memory. No reporter file was written or changed. The reported shard status itself says the deployed build and published package are not visible from repositories; no live availability was inferred. This reporter behavior was observed and left unchanged because P382 is docs-only.
- Checked the P382 stop-request path between research, writing, and review steps; it was absent through final review.

## Run timing

First recorded clock: 2026-10-22 01:43:20 UTC. Completion stamp: 2026-10-22 01:53:44 UTC. Measured elapsed time: 10 minutes 24 seconds. Both stamps fall on October 21 in America/Chicago.

P382 DONE
