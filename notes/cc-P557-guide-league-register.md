# P557: League Register player guide draft

October 24, 2026. Docs-only work in the Verite-tower work copies. Code HEAD inspected: `1c9c5d8`. Read both AGENTS.md files, the direction decision, and the task list. No code changes.

## Deliverable

Created [the League Register guide](wiki-drafts/league-register.md) in plain American English, with no em dashes. It covers getting and replacing the Register, binding and unbinding, capacity, its tabs, remote contracts, combined turn-ins, Blaze repair, repair items and smithing recipes, the Field Satchel, backpack upgrades, and the Combined Logbook.

The guide describes the current implementation, including P451. Numbers are explicitly built-in defaults, not verified running-shard settings. It distinguishes Blaze's free equipped-gear repair from the Remote Repair Deed's worn, backpack, and bank pass. It also spells out the combined smith turn-in's treatment of Ask each time, sequential backpack purchases, direct-backpack placement for the satchel discount, and safe delivery on a full pack.

## Primary sources

Paths below are relative to the ShatteredLegacy work copy unless stated otherwise. Line numbers refer to the inspected tree. These are implementation sources, not keyword counts.

| Source | What was verified |
|---|---|
| `server/customizations/LeagueRegister/LeagueRegisterSettings.cs:26` | Issue rank, guild capacity table, action gates, goods prices, merge fee, backpack steps, Arms Lore/material defaults, kit charges, full-repair default. |
| `server/customizations/LeagueRegister/LeagueRegister.cs:45` | Actual book requirements: Smith Guild Book and Compact Dispatch Ledger. |
| `server/customizations/LeagueRegister/LeagueRegister.cs:70` | League membership/rank requirement, free issue, checked delivery, replacement invalidation. |
| `server/customizations/LeagueRegister/LeagueRegister.cs:120` | Dropped guild display, membership checks, top-level book search, empty-book refusal, free unbinding and safe book return. |
| `server/customizations/LeagueRegister/LeagueRegister.cs:261` | Bronze contract access; Verite active-work-order loop and recursive completed smith-deed search; cash-out-only boolean means Ask banks. |
| `server/customizations/LeagueRegister/LeagueRegister.cs:338` | Blaze rank gate calls `RepairWorn`, with no price or cooldown. |
| `server/customizations/LeagueRegister/LeagueRegister.cs:361` | Blessed, character-bound Register and backpack requirement. |
| `server/customizations/LeagueRegister/LeagueRegisterGump.cs:23` | Bank summary categories and bank-check gold; tabs and actual button labels at `:119`, Guilds/Contracts at `:156`, League actions at `:225`, Goods at `:261`. Ledger rows stop at the window boundary, so the draft avoids promising every guild fits on screen. |
| `server/customizations/LeagueRegister/LeagueRepair.cs:28` | Durability-only repair, full versus configured partial restoration, no maximum-durability change, carried targets, equipped-only pass, recursive backpack/bank remote pass, and target source revalidation at `:111`. |
| `server/customizations/LeagueRegister/LeagueRepair.cs:152` | Blacksmithy minimums, Arms Lore second skill, recipe ingredients. Field deed use at `:194`, kit charges/use at `:208`, remote deed use and conditional consumption at `:269`. No user-skill or League-rank checks on the three finished items. |
| `server/customizations/LeagueRegister/LeagueConsolidation.cs:30` | Four accepted satchel families and corresponding currency keys. Checked delivery at `:52`; logbook purchase/removal at `:83`. |
| `server/customizations/LeagueRegister/LeagueConsolidation.cs:117` | One satchel per family, direct-player-backpack discount, normal totals elsewhere, weight parent checks, insertion fee after success, free repositioning and removal. |
| `server/customizations/LeagueRegister/LeagueConsolidation.cs:270` | Combined Logbook backpack requirement and member-only choices. |
| `server/customizations/LeagueRegister/LeagueBackpack.cs:55` | Character-specific tier, login application, next-tier-only purchase, item-limit change; `LeaguePrice` at `:141` checks and pays Renown plus gold. |
| `server/customizations/LeagueRegistrar.cs:36` | Registrar name Elara Voss and double-click interaction at `:72`. |
| `server/customizations/LeagueRegistrarGump.cs:135` | League Register button beside Citizen Status; issue handler at `:417`. |
| `server/customizations/ClusterFGuildSystem.cs:193` | Guild display names for the four satchel currency families, including Rangers' League and Foresters' Union. |
| `server/customizations/GuildContractLedgerGump.cs:562` | Work-order requirements, consumption from pack/bank, normal payouts, and completion history. |
| `server/customizations/ClusterFSmithBODPayout.cs:16` | Payout modes; deed possession and payout at `:125` and `:159`. |
| `server/customizations/CompactGoldHelper.cs:23` | Gold availability and backpack-first, bank-second payment. |
| `server/customizations/ClusterFAccountData.cs:666` | Spending Renown changes only the balance, not Lifetime Renown. |
| `D:/UO/ModernUO-pinned/Projects/Server/Items/Container.cs:177` | Default 125-item capacity; `:247` includes incoming contents when checking item capacity. Pinned checkout independently verified at `d4531cd94b739613155225c234900de9f47d2c88`. |

Read the existing `server/tests/Misc/LeagueRegisterVerification.cs` as supporting evidence for issue/reissue, binding, action gates, combined turn-ins, repair source checks, fees, full-pack delivery, bank totals, and persistence. No tests were run or added for this prose-only task. P280/P451's recorded build results are historical evidence, not new verification by P557.

## Earlier notes and discrepancies

- Read `notes/cc-P280-league-register-build.md`, `notes/cc-P451-league-register-fixups.md`, P451's adjacent Codex review, and `notes/cc-P554-review-league-register-fixes.md` in this docs work copy.
- P280's original description says Blaze repairs worn, carried, and banked gear. P451 supersedes that with worn gear only. The Remote Repair Deed retains the wider pass and is usable at any rank. The guide avoids the old claim that the remote deed simply duplicates Blaze for lower ranks.
- The earlier `notes/wiki-drafts/pages/uo/systems/league_register.txt` still describes the original Blaze pass. The code repo's `docker/wiki/content/pages/uo/systems/league_register.txt:32` has the equipped-only correction, but its final repair paragraph still equates the remote deed to Blaze. Neither existing file was edited: P557 requests a new Markdown draft and its notes only.

## Open questions and publication checks

1. **Running settings and availability are unverified.** No live shard, Haven, client, or saved world was accessed. Confirm the displayed prices, skill requirements, capacities, and availability before publication. Several original numbers were proposals; P557 reports the implemented defaults without claiming a separate balance approval.
2. **Loaded Field Satchel return remains a known limitation.** P451's adjacent review identifies the incoming-capacity check counting full contents while the lifted satchel has no parent. Current `LeagueConsolidation.cs:125` and pinned `Container.cs:247` retain that shape. The guide includes a short player-facing limitation and does not promise arbitrary loaded-satchel transfers. This is source corroboration; client reproduction and a fix are unverified here.
3. **Hunter's Satchel filtering review finding remains open.** P554 records an open-container resource-filter bypass when nested in the Field Satchel. The draft explains intended use without claiming all insertion paths enforce the filters. Keep exploit reproduction details in the review notes, not the player guide. No repair was attempted in this docs-only task.
4. **Screenshots and UI fit are unverified.** Capture the Guilds, League, and Goods tabs in a client before publication, especially with many bound guilds. No new art is needed to complete this text draft, and no art was generated or requested.

## Validation

Reviewed the draft against the cited source branches and checked the tables, menu labels, relative League-guide link, and repair scopes. Checked both new Markdown files for em dashes: none. Both files are below 5 MB. `git diff --check` is clean in both work copies, and worktree status shows only the two requested new Markdown files in shard-migration; the code work copy remains clean. No lane tests requested. No new tests or gates added.

Ran `python tools/progress.py --dry-run` successfully with `SL_SHARD` and `SL_MIGRATE` set to these work copies. Restored its generated `tools/progress.json` to its original bytes, keeping the task docs-only and limited to the requested files. Commands ran in Windows PowerShell 5.1. Checked the P557 stop-request marker between steps; none was present.

No Haven connection, deployment, build, service change, commit, merge, push, branch switch, or edit under `docs/` was made. The guide remains a draft; the open publication checks above are explicitly unverified, nonblocking follow-up items.

P557 DONE
