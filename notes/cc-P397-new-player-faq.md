# P397: New player FAQ linking the wiki drafts

Completed October 22, 2026 after resuming the same session. The earlier pause
honored the Golem's 95-percent budget stop; the user authorized continuation once
the stop file was removed. No scope or source decisions changed on resumption.

## Deliverables

- `notes/wiki-drafts/new-player-faq.md`: a draft FAQ with 25 numbered questions,
  two or three sentences per answer, guide links in every answer, a short guild
  comparison table, and final Sources and Contradictions lists.
- This task note: reading inventory, review results, and verification limits.

The FAQ covers arrival and orientation, Young, island travel, skipping, loops,
levels, scrolls, guild choice and contacts, the League and currencies, starter
animals and humanoid companions, pet growth, healing, crafting, recipes, bulk
orders, contracts, commissions, requisitions, discoveries, Imbuing, fishing,
achievements, and opening boxes. The numbered headings are the question list;
the guild table is part of question 9.

## Reading inventory

Read both work copies' `AGENTS.md` before work. Also read the migration copy's
`docs/README.md`, `docs/direction-decision.md`, and `docs/tasks.md` for governing
context. Read `docs/feature-queue.md` through its final Dropped table, including
historical alternatives and later decisions. The resume used smaller batches to
cover the middle omitted by an earlier truncated output.

Read every input file in `notes/wiki-drafts/`, listed below. The new FAQ is the
output and is excluded from this input inventory.

- `achievements-and-loot-boxes.md`
- `artificers-order.md`
- `companions-and-evo-pets.md`
- `crafting-changes.md`
- `cross-check-2026-10-22.md`
- `gathering-guilds.md`
- `glossary.md`
- `high-seas-fishing.md`
- `league.md`
- `levels-loops-and-scrolls.md`
- `new-haven-start.md`
- `order-of-the-alembic.md`
- `rangers-custodians-healers.md`
- `society-of-smiths.md`
- `thieves-den.md`
- `pages/sidebar.txt`
- `pages/uo/start.txt`
- `pages/uo/drafts/levelable_gear.txt`
- `pages/uo/drafts/start.txt`
- `pages/uo/drafts/tutorial.txt`
- `pages/uo/guides/league.txt`
- `pages/uo/guides/start.txt`
- `pages/uo/professions/bulk_orders.txt`
- `pages/uo/professions/climbing_boots.txt`
- `pages/uo/professions/start.txt`
- `pages/uo/professions/traps.txt`
- `pages/uo/systems/accessories.txt`
- `pages/uo/systems/achievements.txt`
- `pages/uo/systems/creature_levels.txt`
- `pages/uo/systems/league.txt`
- `pages/uo/systems/league_register.txt`
- `pages/uo/systems/league_shop.txt`
- `pages/uo/systems/loot_boxes.txt`
- `pages/uo/systems/start.txt`
- `pages/uo/world/seasonal.txt`
- `pages/uo/world/start.txt`

## Source handling

The FAQ links the existing guides for detail and retains disputed descriptions as
`(being confirmed)`, including differences already carried by the glossary and
individual guides. It does not choose between competing reset rules, reserve
amounts, party budgets, membership descriptions, payout rules, recipe-book ranks,
box promises, deployment claims, or ship decisions. Future work is marked
`(planned)`. Contradictions remain unresolved in their original files.

Focused canonical-source reads supplemented the draft synthesis:

- `ShatteredLegacy/server/customizations/Tutorial/ClusterFLoops.cs`: the real
  graduation counter, vision, and empty level/skill integration hook.
- `ShatteredLegacy/server/customizations/Tutorial/ClusterFTutorial.cs`: core
  completion, optional wings, provisional skipping, graduation, and pet offer.
- `ShatteredLegacy/server/customizations/ClusterFYoungPlayer.cs`: the implemented
  `Duration = TimeSpan.FromHours(336.0)`, account play clock, and renunciation.
- `ShatteredLegacy/server/customizations/Mobiles/Evo/EvoPet.cs`: damage-share XP
  award, evolution gates, and separate owner-loop source.
- `ShatteredLegacy/server/customizations/ClusterFGuildStarterPath.cs`: the skill
  table and directory direction mechanism.
- `ShatteredLegacy/server/customizations/LeagueRegister/LeagueRegisterSettings.cs`:
  League service and purchase settings, without publishing its prices in the FAQ.

These reads do not resolve the cross-check's source disputes or establish live
availability. Other subjects are concise synthesis of the linked source-audited
guides, not a new claim of full source-tree or runtime verification.

## Review and validation

- Reviewed the complete FAQ against the requested topics and cross-check. The
  question inventory is its numbered headings 1 through 25 in the deliverable.
- Listed answer sentence counts with a one-off PowerShell metadata read, then
  reviewed the prose and table manually. Every answer has two or three sentences
  and at least one relevant guide link, including the links in question 9's table.
- Checked every distinct relative Markdown target against the local filesystem;
  all exist. This establishes local targets only, not live wiki publication.
- Checked for em dashes and trailing whitespace; neither was present in the FAQ.
- Reviewed the only gameplay amount stated, Young's play-time duration, against
  `ClusterFYoungPlayer.Duration`. Numeric question labels and cross-check IDs are
  navigation, not invented game values.
- Reviewed for staff commands, exploit instructions, and hidden-achievement
  spoilers; none are included. The only command strings are player-facing
  `[guild` and `[achievements`.
- Inspected file sizes: both deliverables are comfortably below 5 MB.
- Ran `python tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` set to
  these work copies; it exited 0. Its existing project-wide warnings do not change
  this task's scope. An existing tooling defect surfaced: `build()` writes
  `tools/progress.json` before `main()` checks `--dry-run`, despite the documented
  print-only behavior. The initial status was clean for that file; restored only
  this run's generated change byte-for-byte from HEAD and confirmed it is clean.
  This is our tooling to fix separately; no tooling code was changed by P397.
- Ran `git diff --check` and reviewed repository status. Only the two deliverables
  are new in the migration work copy; the code work copy is unchanged.
- No tests or gates were added. Lane tests are none; no build or runtime test was
  needed for this docs-only change. Editorial checks ran in Windows PowerShell
  5.1, not PowerShell 7. `rg` was unavailable, so reads used `Get-Content` and
  inventory used `Get-ChildItem`.

## Limits and operational scope

Running settings, NPC and dungeon placement, client appearance, reward behavior,
and live wiki availability remain unverified. No Haven connection, network lookup,
build, deployment, restart, world/account change, commit, merge, push, or branch
switch occurred. No existing draft or file under `docs/` was edited, and
`server/uo/` was not read.

Final review complete. The final stop-request check was absent; no P397 work remains.

P397 DONE
