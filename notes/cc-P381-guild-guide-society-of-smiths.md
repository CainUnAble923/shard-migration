# cc-P381: Society of Smiths player guide

October 21, 2026. Codex lane, Verite tower. Docs-only task. Work copies:

- Code: `D:\UO\golems\Verite-tower\ShatteredLegacy`.
- Notes: `D:\UO\golems\Verite-tower\shard-migration`.

## Outcome

Wrote `notes/wiki-drafts/society-of-smiths.md`, a player-facing draft covering free joining, the chapter and planned headquarters, ranks and recipe access, Blacksmithy and Arms Lore, the guild book, deeds, contracts, commissions, Seals, salvage, catalog rewards, both built hammer tiers, extended metals, and exceptional material bonuses. The page ends with Sources and Contradictions. File:line evidence is kept here, not on the page.

The draft describes source behavior and decided plans. Running-shard availability, world placement, deployment version, actual configuration overrides, and client appearance remain **unverified**. No Haven connection or runtime inspection was made. No code, tests, `docs/`, or generated status files changed. Nothing committed, merged, pushed, or switched branches.

## Run timing and pauses

- First segment: approximately 16:45:47 to 16:50:57 CDT, 5 minutes 10 seconds. The Golem requested a budget pause during research; a continuation checkpoint was saved.
- Second segment: approximately 17:37:38 to 17:46:00 CDT, 8 minutes 22 seconds. Completed the guide and validation, then paused again when the Golem stop flag returned during final checks. Restored the progress reporter's unexpected generated-file change before stopping.
- Final review resumed at 20:33:48 CDT with explicit authorization and the stop flag absent. Final elapsed time is recorded below.

Both work copies were initially clean. Only the two requested notes files are intended deliverables. No tests were added or run; no code, docs directory, deployment, account, or live server was changed.

## Read and discovery

Read both work-copy `AGENTS.md` files, `docs/direction-decision.md`, and the opening working agreements and task sections of `docs/tasks.md`. The first combined output was truncated; the migration agreements were re-read separately with UTF-8. The task-list tail still needs a read if relevant. Newer Golem rules override its old commit/push instructions.

Read `notes/wiki-drafts/league.md`, the P374 format model. Use its draft date, availability caveat, plain paragraphs, useful tables, and sources/contradictions ending. This task explicitly asks for a Markdown file; no Pages write workflow is needed.

`rg` is unavailable in this environment. Python 3.12 is available. Use `python -X utf8` for output, because the default Windows encoding failed on source arrows. Windows PowerShell commands used the environment shell; no PowerShell script or test was executed. Any subsequent PowerShell script/test must use `powershell.exe` 5.1.

Searched `notes/**/cc-P*.md` for the literal phrase `Society of Smiths`, case-insensitively, excluding this task's own note. The required-file inventory is below. Reviewed Smith-related passages and surrounding sections in every listed note, including historical descriptions and later changes. Some initial combined outputs were truncated; the continuation used smaller excerpts to inspect the relevant missing passages. Unrelated build logs and operational sections were not used as evidence of player behavior. Repeated the inventory at continuation and found the same files.

- `cc-P118-port-bulk-orders.md`
- `cc-P122-port-bulk-orders-core.md`
- `cc-P14-newhaven-guild-mapping.md`
- `cc-P150-requisitions-and-leads.md`
- `cc-P151-guild-halls-survey.md`
- `cc-P169-requirement-colors.md`
- `cc-P170-smith-teaching-orders-fix.md`
- `cc-P177-guild-menus-template-mockups.md`
- `cc-P179-league-design-pass.md`
- `cc-P217-crystal-wiki-catch-up.md`
- `cc-P218-crystal-mage-crafter-scripts.md`
- `cc-P224-playtest-bot-checks-second.md`
- `cc-P261-levelable-gear-build.md`
- `cc-P265-guild-hall-decor-packs.md`
- `cc-P280-league-register-build.md`
- `cc-P286-test-plans.md`
- `cc-P32-spawner-importer-bods-self-repair.md`
- `cc-P378-playtest-plans-10-21.md`
- `cc-P42-defect-batch-3.md`
- `cc-P52-bug-batch-4.md`
- `cc-P55-bug-batch-5.md`
- `cc-P56-smith-economy-and-labels.md`
- `cc-P58-changelog-catch-up.md`
- `cc-P78-recipe-gating.md`

Additional relevant notes reviewed for the material, hammer, economy, and recipe changes:

- `cc-P46-smith-orders-2.md`
- `cc-P53-two-hundred-cap.md`
- `cc-P57-batch-6.md`
- `cc-P61-batch-7.md`
- `cc-P228-exceptional-material-gap.md`

Read relevant feature-queue passages in F-9 (starter path), F-18 (teaching BODs), F-20 (craft BODs), F-34 (bank crafting proposal), F-43 (recipes), and F-49 (halls). On continuation read F-25, F-29, and F-37 completely, and checked F-47's Smith requisitions against their implementation. F-9 retains the old Smiths' Fellowship name.

No nested `AGENTS.md` was found under `server/customizations`, `server/tests`, or the migration notes directory by the targeted search. Never inspect the stale `server/uo` tree.

## Test review

The initial segment discovered declarations. On continuation read relevant assertion bodies for Smith BOD paths/choice, commissions, high-skill teaching, Seal pricing/bank value, hammer held bonuses/familiarity pace, recipe gating, exceptional materials, and salvage returns in the files below. **No tests were added or run.** This is docs-only with no lane tests; existing assertions were inspected as corroborating source, not reported as newly passing.

Test files reviewed (paths relative to code):

- `server/tests/Misc/SmithBODPathsVerification.cs`
- `server/tests/Misc/SmithBulkOrderChoiceVerification.cs`
- `server/tests/Misc/SmithCommissionRewardsVerification.cs`
- `server/tests/Misc/SmithOrdersTeachHighSkillVerification.cs`
- `server/tests/Misc/SmithSealPriceVerification.cs`
- `server/tests/Misc/SmithBankValueVerification.cs`
- `server/tests/Engines/Craft/HammerHeldBonusVerification.cs`
- `server/tests/Engines/Craft/HammerFamiliarityPaceVerification.cs`
- `server/tests/Engines/Craft/RecipeGatingVerification.cs`
- `server/tests/Items/ExceptionalMaterialVerification.cs`
- `server/tests/Items/SalvageBagIngotReturnVerification.cs`

## Continuation: additional verified evidence

Resumed October 21, 2026 at 17:37:38 CDT, with the stop file absent and explicit Golem authorization to continue. Source pin read directly with `git -C D:\UO\ModernUO-pinned rev-parse HEAD`: `d4531cd94b739613155225c234900de9f47d2c88`. Only the canonical customizations, patches, tests, and this pristine reference were consulted, never `server/uo`.

The page uses current implementation for available features, records differences without changing decisions, and labels future features (planned). The historical P78 recipe inventory is explicitly contrasted with the current Exodus registration.

| Page claim or decision | Current source evidence |
|---|---|
| Character membership, standing, and currency | `server/customizations/ClusterFAccountData.cs:136`, `:783`, `:802`, `:972`, `:984`, `:1103`; access is through the character Serial. |
| First hammer claim shares the quest record | `server/customizations/ClusterFGuildStarterPath.cs:335`, `:377`, `:405`, `:420`, `:435`; only membership and a valid starter quest are required, already-claimed rewards are refused, and the matching quest is marked done. |
| Rank requirements and grants | `server/customizations/ClusterFGuildPromotion.cs:68` reads base skill; `:85` computes skill cap; `:141` updates and grants rank; `:173` grants books or starter scrolls. Defaults are `server/customizations/Engines/Craft/ClusterFRecipeTable.cs:75`, `:78`, `:81`. The grandfathered-record behavior is retained in source but is not needed as a new-player instruction. |
| Promotion versus display discrepancy | `server/customizations/SmithGuildmasterGump.cs:89` uses its standing-only GetRank; the guild book also calls the standing overload. `server/customizations/ClusterFGuildSystem.cs:662` and `:690` use promotion-aware rank. |
| Book bands and costs | `server/customizations/Engines/Craft/ClusterFRecipeTable.cs:36`, `:39`, `:56`, `:59`, `:64`; `GuildRecipeShopGump.cs:26` uses one-band-ahead access and the rank-4/5 rotation. `ClusterFRecipeGate.cs:135` preserves own-recipe gates; `:204` merges sparse bands but stops at the last book band; `:219` lists only nonempty books. |
| **Band IV now exists, contrary to P78's inventory** | `server/customizations/Engines/Craft/ExodusCraftRegistrations.cs:65` registers `ExodusSacrificalDagger` at minimum Blacksmithy 95.0, with no own recipe. `ClusterFRecipeGate.cs:126` classifies it as a Band IV book design under defaults. The last book band never folds forward (`:204`). Added Band IV price 800, Master purchase, and Grandmaster grant to the draft. No current per-band item counts are asserted. |
| Large BOD recipe chance | `server/customizations/ClusterFSmithBODPayout.cs:187`; `server/customizations/Engines/Craft/ClusterFRecipeRewards.cs:70`; default chance `ClusterFRecipeTable.cs:87`. Commission rewards differ: `ClusterFRecipeRewards.cs:87` checks the empty default `CommissionScrolls` at `ClusterFRecipeTable.cs:89`. |
| Smith-related crafts and mule schematics | `server/customizations/LeagueRegister/LeagueRepair.cs:135`, `:139`, `:143` add repair crafts with Arms Lore. `server/customizations/Mobiles/Mule/MuleModule.cs:207` assigns Field Smelter Rig to Blacksmithy with Arms Lore, and `:269` registers crafts with their own schematic recipes (`:281`). `MuleModuleGumps.cs:477` requires rank indexes 1/2/4 for tiers I/II/III; `:508` also checks Mining Vouchers and later code checks guild currency. The page states separate costs without inventing or conflating them with recipe-book prices. |
| Current fixed BOD limits, not promised rank allowances | `server/customizations/ClusterFSmithBODSystem.cs:56`, `:60`, `:93`, `:141`, `:174`, `:276`; `server/tests/Misc/SmithBulkOrderChoiceVerification.cs:194`, `:211`; `SmithBODPathsVerification.cs:169`. F-25's approved rank caps remain in `docs/feature-queue.md:2060`, `:2099`; listed as planned, not implemented. |
| Current teaching toggle and selection | `server/customizations/ClusterFSmithTeaching.cs:53`, `:68`, `:82`; current high-skill armor selection is documented at `:43` and verified by `server/tests/Misc/SmithOrdersTeachHighSkillVerification.cs:136`, `:236`. The page describes fallback without promising gains. |
| Cash-out pays no Seals | `server/customizations/ClusterFSmithBODPayout.cs:159` to `:185`, then `:213`; F-25's conflicting gold/Seals/item description is `docs/feature-queue.md:2067`. Current checks per deed come from `ClusterFSmithBODSystem.cs:461`. |
| Seal prices are baseline times three | `server/customizations/SmithSealCatalogGump.cs:58`, `:62`, `:70`, `:83`, `:94`; guards against buying placeholders at `:254`, payment at `:266`. `server/tests/Misc/SmithSealPriceVerification.cs:92`, `:102`, `:130`, `:220` corroborate catalog and post-Valorite valuation. No old payout table is copied into the page. |
| Contracts pay the character's Seals, standing, and gold | `server/customizations/ClusterFWorkOrderSystem.cs:1107` to `:1379` enumerate Smith contracts, with the example at `:1111`; `server/customizations/GuildContractLedgerGump.cs:448` checks membership/eligibility, `:541` consumes pack/bank materials, `:547` pays standing and currency, and `:562` names Smithing Seals. Ledger previews use generic Vouchers wording in places; page uses the actual payout currency. |
| Current commissions versus future League commissions | `server/customizations/ClusterFSmithCommissions.cs:454`, `:522`, `:570`, `:619`, `:679`, `:712`; the instances do not impose a completion deadline. `SmithCommissionGump.cs:231` checks the small-request wait after abandonment; the default is `ClusterFSmithCommissions.cs:462`. The page confines that statement to the guildmaster's menu and discloses no UI bypass. F-37's League Renown/deadline/Infamy decisions are `docs/feature-queue.md:3080` to `:3115` and are marked planned. |
| Hammer usable-held bonuses, caps, recharge, upgrade | `server/customizations/HammerOfHephaestus.cs:145`, `:235`, `:278`, `:305`, `:525`, `:612`, `:660`, `:704`, `:1098`, `:1162`, `:1302`. Upgrade handler uses skill Value at `:1312`, explaining why page says shown skill with bonuses, unlike promotion. `:1316` refuses an exhausted T1. `:1328` pays through GuildResources; `:1337` transfers familiarity. T3/T4 remain stubs at `:23` and `:1074`. Existing assertions: `HammerHeldBonusVerification.cs:126`, `:233`; `HammerFamiliarityPaceVerification.cs:110`, `:183`, `:216`. |
| Familiarity and BOD autofill actually connect to crafting | `server/patches/CraftItem-shard-hooks.patch:214`, `:216`, `:228`; `server/customizations/HammerOfHephaestus.cs:1376` scans matching small orders before large orders and consumes matching crafted pieces. |
| Mining is now tiered, correcting P56's historical 100 | `server/customizations/ClusterFMiningExtension.cs:96`, `:105`, `:155`, `:188`; requirements come from `ClusterFMetalTiers.cs:20`. `server/patches/Ore-smelt-at-forge.patch` adds the same post-Valorite tier to ore difficulty. `SmithGuildSalvageBag.cs:62` uses that table for resmelting. Gain ceilings are `ClusterFMetalTiers.cs:70`; Dawnstone is separate at `:34`. |
| Exceptional material scaling is built | `server/customizations/ClusterFExceptionalMaterial.cs:40` to `:92`; positive values are x1.5 rounded half up, penalties and runic ranges unchanged. Wiring: `server/patches/BaseArmor-exceptional-material.patch:10`, `:31`; `BaseWeapon-exceptional-material.patch:10`, `:19`, `:28`, `:37`. `server/tests/Items/ExceptionalMaterialVerification.cs:105`, `:144`, `:393`, `:461` corroborate live attributes, unchanged runics, and wearer resistance caps. |
| Salvage pays Seals only for successful items and membership | `server/customizations/SmithGuildSalvageBag.cs:84`, `:144`, `:192`, `:260`, `:282`; failed material checks leave the item intact. Ingot returns are checked in `server/tests/Items/SalvageBagIngotReturnVerification.cs:84`, `:99`, `:150`. No exploit instructions or yield optimization are given. |
| Register binding is distinct from native Smith book access | `server/customizations/LeagueRegister/LeagueRegister.cs:46`, `:155`, `:178`, `:184`, `:204`, `:219`. A nonempty book is refused; unbinding returns a fresh one. P177/P179 proposals do not establish current Smith book restrictions. |
| Requisitions pay different rewards | `server/customizations/Requisitions/RequisitionTable.cs:285` lists the Smith themes; `RequisitionSystem.cs:218`, `:248` to `:255` consume the matching item and pay Renown, Society reputation, and gold, no Seals. The page links the League guide instead of duplicating its Lead rules. |
| Headquarters is planned, not a claimed live location | `server/customizations/ClusterFGuildStarterPath.cs:217` remains the New Haven directory location; F-49 at `docs/feature-queue.md:3394` decides Serpent's Hold, with facet still an open decision; `notes/cc-P151-guild-halls-survey.md:165` proposes Trammel and a site, but places nothing. `notes/cc-P265-guild-hall-decor-packs.md:5` likewise says nothing placed. Page does not advertise proposed footprint coordinates or a settled headquarters facet. |

## Contradictions retained in the page

The final page has a separate Contradictions list for names/membership, standing-only rank displays, the old missing Band IV inventory, large-deed requirements and rank allowances, turn-in check counts, cash-out Seals, changed Seal economy and mining, high-skill teaching changes, the commission relocation, and proposed book restrictions versus current access. These are recorded as source differences; no code or design was changed to reconcile them.

Also reviewed the peripheral required notes: P217's wiki survey, P218's stopped script work, P224's bot result, P261's unchosen Smith's Seal acquisition, P286's proposed crafter checks, and P378's pending plans. They establish neither current deployment nor a new available Society reward. The page does not advertise the Smith's Seal deed, hidden achievements, staff-only content, or a play-test plan as a passed gameplay check.

## Validation

Ran the progress reporter with explicit work-copy `SL_SHARD` and `SL_MIGRATE` overrides and `--dry-run`. **It unexpectedly rewrote `tools/progress.json` despite that option.** Source explains the side effect: `tools/progress.py:732` calls `build()`, which writes the JSON at `:722`, before main checks the dry-run option at `:737`. This is a reporter defect in this repo, not a player feature; recorded here without broadening P381 into a code fix. Restored only that generated file from its exact HEAD bytes, since initial and pre-reporter status proved it clean. Verified byte equality to HEAD and clean tracked diff afterward. No numbers from its broad inventory are claimed in this guide.

Draft review completed at 17:45:14 CDT: links resolve; no em dash or file:line citation on the page; both output files below 5 MB; no trailing whitespace or missing terminal newline. The draft was 2,864 whitespace-separated words and 18,911 bytes at that check. No tests were added or run. `git diff --check` was clean. New-file whitespace was separately checked because Git does not include untracked files in that command.

## Final review

Resumed the same task at 20:33:48 CDT on October 21, 2026. Reviewed the full draft for consistency with the evidence table, clarified the notes to remove superseded research reminders, and retained both historical pause records. No implementation, build, deployment, or new tests were needed. Final scope and formatting checks passed before completion was signaled.

Final checks passed: all 24 relative Markdown links resolve; required sections are present; no em dashes or file:line citations occur on the guide; both files have terminal newlines, no trailing whitespace, and sizes below 5 MB. The guide is 18,911 bytes. Both repositories pass git diff --check, the code repository is clean, and migration status contains exactly the two requested new notes files. No new tests or lane tests were required. The stop flag was absent at final validation and completion.

Completed 2026-10-21 20:35:22 -0500. Final review segment: approximately 1 minutes 34 seconds. Total active run time across all three segments: approximately 15 minutes 6 seconds, excluding the two Golem pauses. Both requested deliverables are finished; no required work remains.

P381 DONE
