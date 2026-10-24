# P562: glossary update

Updated October 24, 2026 by the Golem's Codex lane.

## Changes

Updated only `notes/wiki-drafts/glossary.md`, plus this required task note. Added or refreshed the tutorial lessons and optional wings, Hint and arrow, graduation companion pick, reward mounts and statuettes, quest markers, mining quotas, Mining For Quality Stone, Stone Contracts, retired civic waste bundles, Trash Bag corpse clearing, planned Town Houses, and the planned new facet and tutorial island. Entries remain alphabetical, with links to the recent player guides.

Applied the October 23 League answers to Citizen Commissions, named milestones, six story chapters, Leads, and immediate non-member requisition standing. Updated the historical contradiction entries so they no longer present those answered questions as unresolved. Corrected the Remote repair deed comparison while checking the current League Register guide: the deed reaches carried and banked gear, while the free Blaze action reaches equipped gear only.

The task's older "pull first" instruction conflicts with the unattended handoff's explicit prohibition on merging or switching branches. Used the prepared `golem/Verite/P562` branches and their clean starting work copies. No pull, fetch, merge, commit, push, or branch switch occurred.

## Evidence

Paths in this list are relative to the code work copy unless they start with `notes/` or `docs/`, which refer to the migration work copy.

- Tutorial core: `server/customizations/Tutorial/TutorialStations.cs`, the `Core` entries in `All`. Read and enumerated the nine entries: movement, backpack, paperdoll, chat, death, banking, travel, League, and loop. `TutorialCoreTrials.cs`, especially `Hint`, `MakeSupply`, and `Resupply`, supplies the lesson actions and replacement behavior. `TutorialGumps.cs` supplies the graduation pet picker. Cross-checked `notes/wiki-drafts/new-player-tutorial.md`, `first-companion.md`, and P480/P525 notes for the wing flow, saved progress, and Farmhand exclusion.
- Reward mounts: `server/customizations/Mobiles/Mounts/RewardMountStatuette.cs`, `OnDoubleClick`, verifies backpack use and deletion only after successful mount delivery. Cross-checked `notes/wiki-drafts/mounts.md` and the P521 review for horse-level placeholder stats, follower capacity, and acquisition limits.
- Mining: `server/customizations/ClusterFWorkOrderSystem.cs`, `WorkOrderMiningRequirement`, `NeedsStoneMining`, `QuotaMet`, `Consume`, and `OnOreMined`; `server/customizations/MinersCompactLiaisonGump.cs`, `StoneBookStanding`, `StoneBookVouchers`, and `TryBuyStoneMiningBook`. Cross-checked `notes/wiki-drafts/mining-changes.md` for the reading and seller rules.
- Cleanup: `server/customizations/TrashBag.cs`, corpse menu ownership and backpack conditions; `server/customizations/ClusterFCustodianSystem.cs`, `ClearCorpse`, `ClearCorpsesNearby`, and `RedeemBundles`; `server/customizations/SanitationWarden.cs`, bundle redemption entry point. Cross-checked `notes/wiki-drafts/clean-up-britannia-changes.md` for range, cooldown, protected loot, and retired bundles.
- League answers: read `docs/feature-queue.md`, the October 23 decision sheet's nine answers, and `notes/cc-P515-league-design-vs-build.md`. Read the current `notes/wiki-drafts/league-register.md` and `server/customizations/LeagueRegistrarGump.cs` for the related player terminology. No design decisions were made or changed.
- Quest markers: canonical `server/customizations/QuestMarkers.cs` is absent, and a search of canonical customizations and patches found no marker implementation. `notes/cc-P522-review-quest-markers.md` records the same integration gap. Read `D:/UO/cc-prompts/merging/cc-P363-quest-markers-keys-gates.md` for the intended personal ! offer and ? turn-in symbols. The glossary marks the feature planned and integration pending; it does not claim it is available.
- Planned housing and start area: `notes/wiki-drafts/town-houses.md` and `D:/UO/cc-prompts/queue/cc-P481-new-player-start-area-design.md`. The latter explicitly proposes the new custom facet, tutorial island, private visibility, private vision scene, and later trial/event space as design work. No map index, rental price, or finished implementation is invented.

## Validation and limits

No lane tests were requested. No code, tests, or new gates were added, so no red/green cycle applies. No build or client playthrough was run for this prose-only task. Running-shard placement, deployment, settings, package publication, and actual feature availability remain unverified. No Haven connection or service operation occurred.

Editorial inspection found no alphabetical inversions, missing relative link targets, undefined reference links, or em dashes in the glossary. `git diff --check` passed. Both changed Markdown files are below 5 MB. The code work copy remains clean; the migration work copy contains only the glossary edit and this new note.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` set to these work copies: exit 0. It reports shard version 2026.10.24.10. As previously documented by P525, the tool writes `tools/progress.json` even in dry-run mode. Preserved and restored its exact starting bytes, then confirmed the snapshot matches, keeping the final diff within the authorized files. This task does not certify the tool's unrelated project-wide counts.

Checked the P562 STOP-REQUESTED path between steps; no request was present during the work.

P562 DONE
