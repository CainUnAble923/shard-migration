# P600: Hammer of Hephaestus player guide

October 25, 2026. Documentation only. The requested draft is [wiki-drafts/hammer-of-hephaestus.md](wiki-drafts/hammer-of-hephaestus.md). The Golem's designated run note is [cc-P600-guide-hammer-of-hephaestus.md](cc-P600-guide-hammer-of-hephaestus.md).

## Scope

The guide covers the free Society starter claim and alternative training quest, all available tiers through T3, familiarity, upgrade requirements and costs, recharging, ordinary automatic deed filing, and Craft This Order. T4 is explicitly unavailable. Plain American English, with no em dashes. No code, docs directory, service, configuration, package, or deployment changes.

Read AGENTS.md in both work copies, the direction decision, and the single task list before writing. Followed the prompt's work-copy mapping and no-commit rule over older instructions. Both work copies were clean at the start. No agents were delegated.

## Source evidence

Shard paths below are relative to the code work copy. Line numbers refer to the source inspected for this task.

| Topic | Evidence |
|---|---|
| First free hammer, shared quest claim, no task requirement | `server/customizations/ClusterFGuildStarterPath.cs:101`, `:335`, `:377`, `:405`. `TakeStarterItem` checks membership and the shared claim, gives the quest's rewards, then records the quest complete. |
| Location and free joining | `ClusterFGuildStarterPath.cs:217`; `server/customizations/ClusterFGuildSystem.cs:73`. |
| Quest alternative | Read-only pinned `Projects/UOContent/Engines/ML Quests/Definitions/NewHavenSkillTraining.cs:621`: ItsHammerTime has a 500 fixed-point Blacksmith objective and HammerOfHephaestus reward. `Objectives/GainSkillObjective.cs:54` refuses an offer at or above the threshold. |
| Tier values and separate benefits | `server/customizations/HammerOfHephaestus.cs:141`, `:305`, `:521`, `:660`, `:704`, `:934`, `:1087`. T3 is a separate SmithHammer subclass and does not inherit T1's refund or T2's familiarity skill modifier. |
| Metal list, gain chance, exceptional gains | `HammerOfHephaestus.cs:47`, `:113`. Iron through Celestial; gain chance is max(5%, 1 - current/cap), gain +1 normal or +3 exceptional, clamped to cap. |
| Ingot refunds | `HammerOfHephaestus.cs:1087`, `:1105`, `:1115`, `:1119`, `:1126`; `server/patches/CraftItem-shard-hooks.patch`, successful-craft hook. Uses familiarity before this craft's gain. Full resource availability is checked before the refund. |
| Restore and upgrade prices, skill, transfer | `HammerOfHephaestus.cs:1549`, `:1628`, `:1642`, `:1730`, `:1764`, `:1803`, `:1851`. Checks current skill Value, standing thresholds, and exhaustion. Source lookup is main-pack items plus the equipped hammer. Constructor supplies full charges; familiarity snapshot is copied before deleting the old hammer. |
| Pack and bank costs versus pack-only crafting | `server/customizations/GuildResources.cs:3`, `:97`; pinned `Projects/UOContent/Engines/Craft/Core/CraftItem.cs`, ConsumeRes. Guild costs use pack and bank; ordinary crafting uses backpack resources. |
| Menu controls and future tier | `HammerOfHephaestus.cs:1336`, `:1368`, `:1519`, `:1720`; `server/customizations/ShardClilocs.cs`, CraftThisOrder; `player-package/vendor/shattered-legacy-cliloc/entries.json`, entry 1900011. |
| Ordinary filing, small before large | `HammerOfHephaestus.cs:1923`, `:1949`, `:1994`, `:2117`; `CraftItem-shard-hooks.patch`, post-AddToBackpack hook. Society membership is required for ordinary filing; no named metal accepts any metal. |
| Order start, selecting resources, direct fill | `server/customizations/ClusterFCraftOrder.cs:41`, `:115`, `:204`, `:250`, `:282`; `server/patches/LargeSmithBOD.cs`, EndCombine dispatches item filling. Craft This Order itself checks the held T3, smith deed, backpack, life, uses, and nearby anvil and forge; it has no separate membership gate. |
| Completed small deeds consumed first | `ClusterFCraftOrder.cs:177`; pinned `Projects/UOContent/Engines/Bulk Orders/LargeBOD.cs:131`, `:147`. A matching completed small deed must have the large deed's quantity but its entire amount is added to a partly filled line. Guide advises banking completed deeds to preserve them. |
| Stops and continuation | `ClusterFCraftOrder.cs:309`; `server/customizations/ClusterFCraftRun.cs:97`, `:224`, `:324`, `:405`; `server/patches/PlayerMobile-craft-order-hurt.patch`. Normal timed attempts, 500-attempt cap, stops, and stop-after-current-attempt behavior. |
| Payout display and stale tooltip workaround | `server/customizations/Services/BulkOrders/BulkOrderGuildPay.cs:117`, `:147`, `:178`; P587's cache finding. Guide tells players to reopen the deed after a trade or guild change and does not promise a permanently fixed quote. |

Pinned upstream HEAD read as `d4531cd94b739613155225c234900de9f47d2c88`. No generated server/uo tree was read. P168 and P372 records supplied implementation history; claims above were checked against source rather than accepted from those records. Existing hammer tests were located as supporting evidence, not executed.

## Limitations and known issues

This is a source-checked draft, not a live playtest or confirmation of deployed availability. No server, Docker build, account operation, Haven connection, or client session was used. Current client text rendering, live NPC placement, and live timing remain unverified.

P587 reports unresolved last-charge held modifiers, regeneration credit while full, property-list regeneration side effects, excessive consumption of completed small deeds into partial large lines, and cached payout tooltips. The relevant patterns remain in the inspected source. This task fixes none of them. The guide labels recovery rates as configured, gives practical advice for preserving small deeds and refreshing payout information, and avoids claiming exhaustion and recharge are defect-free.

No lost-hammer reissue promise is made. A restoration-registry unlock or a status-page suggestion alone does not verify an accessible replacement route. The ordinary starter replacement method explicitly excludes the hammer (`ClusterFGuildStarterPath.cs:456`).

## Validation

Lane tests: none. No tests or gates added, so the failing-first rule did not require a new test. No build was needed for prose-only changes. Shell confirmed Windows PowerShell 5.1. Final document and worktree checks are recorded in the designated run note.

Read back the player draft and checked its numbers against the source evidence above. All relative Markdown links resolve. All three deliverables have no em dashes or trailing whitespace and are below 5 MB. Both repositories pass `git diff --check`; the code worktree remains clean and the migration worktree contains only the three requested Markdown deliverables.

Ran the required progress reporter successfully with `--dry-run`, `SL_SHARD` and `SL_MIGRATE` pointing to these work copies. Its build function still writes progress.json even in dry-run mode, so preserved and restored that file byte-for-byte. No README or progress artifact is included. No unrelated coverage totals are quoted.

Checked the P600 STOP-REQUESTED path between steps, including after the final document checks. It was absent.

P600 DONE
