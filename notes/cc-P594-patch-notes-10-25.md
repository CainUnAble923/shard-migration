# P594: patch notes for October 25

## Deliverables

Wrote [the October 25 player draft](cc-P594-patch-notes-2026-10-25.md). This file is the outer lane's work record; the dated player draft is the embedded task's deliverable, following P578's two-file format. Both are explicitly requested Markdown files, so no writing skill is needed.

## Scope

Read both work copies' AGENTS.md first, then the direction decision, task guidance, and P578's draft, evidence note, and review. Both work copies started clean. Paths below refer to these work copies.

Code cutoff: `8b0ccb80c00aedd9898be6f453d419b0a2119f2c`, version `2026.10.25`. Notes cutoff: `9328d4f045df0dadab0aabd6fb841070cb416595`. Used local first-parent merge dates on October 25 in America/Chicago. No fetch or remote request was needed. The inventories below cover every merge on that date through those snapshots.

P372 merged just after midnight on October 25, although its changes sit under changelog version `2026.10.24.18`. Included it by merge date. The other October 24 changes after P578, including P458, P459, and P460, are outside this date's scope. Their October 25 reviews do not create new fixes.

This is an unpublished draft for a later package and server update. Running server version, fish-monger placement, effective settings, installed package, published wiki, client appearance, and gameplay outcomes are unverified. Historical build and play-test reports are evidence from their authors, not tests run for P594.

## Code merge inventory

| Merge | Task | Treatment |
| --- | --- | --- |
| `6b74371` | P372, importing P168 | Masterwork Hammer, Craft This Order, guild payout display, and package label. Kept relevant review limits. |
| `db4c85b` | Iron P587, importing P269 | Bait, hooks, lava fishing, SOS finds, delivery orders, Oracle, and pies. Retained ingredient, reward, and access limits. Corgul is not announced as reachable. |
| `8b0ccb8` | P479 | Staff maintenance task. In this code copy the actual changes are mail-mode parsing/display and its console test. Omitted from player notes; no Docker cleanup or disk-space improvement is verified by these files. |

## Notes merge inventory

| Merge | Task | Treatment |
| --- | --- | --- |
| `c146f95` | P372 | Hammer implementation evidence and imported P168 notes. |
| `c5c0389` | P585 | Artificers text review; no new text fix. |
| `5025421` | P586 | Proposed fix-up prompts; no implemented repairs. |
| `cf1e97b` | Valorite P587 | Hammer review; preserve small-deed, exhaustion, regeneration, and tooltip caveats. |
| `586b1c6` | Iron P587 | Fishing import and build evidence. The shared P587 number identifies a different task from the Valorite review above. |
| `d9663bb` | P588 | Proposed tutorial wording; no changed tutorial messages. |
| `a34a3a6` | P589 | Unpublished Rootdeep guide draft; no new dungeon work. |
| `1cb24c8` | P590 | Unpublished Sorcerer's Dungeon guide draft; no new event activation. |
| `6e2aae4` | P591 | Unpublished Eodon guide draft; no new travel, spawns, or taming fix. |
| `63a86ba` | P592 | Unpublished achievements and loot boxes guide refresh; no new reward fix or hidden-achievement disclosure. |
| `9328d4f` | P584 | Guild hall seeder review; no additional placement fix. |

Generated reporting and bot-run artifacts also appear in this notes history. They are not new player features or P594 verification results. These notes merges do not establish publication of any guide.

## Source evidence and editorial choices

Paths are relative to the code work copy unless linked to a note in this repo.

- **Hammer and upgrade:** `server/customizations/HammerOfHephaestus.cs` defines T3's 800 uses, +15 held bonus, 5,000 familiarity cap, refund formula, upgrade requirements, payment, and familiarity transfer. `ClusterFCraftOrder.cs` validates the holder, deed, anvil, and forge; combines top-level small deeds; selects the next recipe; and fills through the deed's own rules. `ClusterFCraftRun.cs` and `server/patches/PlayerMobile-craft-order-hurt.patch` supply stop behavior. `ShardClilocs.cs` and `player-package/vendor/shattered-legacy-cliloc/entries.json` agree on the menu label. No package rebuild is claimed.
- **Hammer limits:** [the Valorite P587 review](cc-P587-review-hammer-t3.md) identifies the last-use modifier, time banked while full, property-list regeneration mutation, partial large-deed overfill, and cached tooltip issues. Current `ApplyHeldBonus`, `ApplyPassiveRegen`, `GetProperties`, `CombineSmallDeeds`, and `BulkOrderGuildPay.Refresh` retain those paths. The draft warns about loss of small deeds and stale tooltips and does not promise corrected exhaustion or regeneration. These are source findings; no runtime reproduction was performed here.
- **Guild payouts:** `server/customizations/Services/BulkOrders/BulkOrderGuildPay.cs`, `BulkOrderDeedGumpLines.cs`, `BulkOrderVendors.cs`, `ClusterFSmithBODPayout.cs`, and `server/patches/BOD-properties-guild-pay.patch` share deed quotes between display and payout. Opening the window recomputes membership-dependent lines; cached tooltips need not follow holder or guild changes. Avoided the changelog's unconditional promise that every displayed number always matches payment.
- **Fishing and placement:** under `server/customizations/Services/Expansions/High Seas/`, read `Generate.cs`, `Items/Fish/Bait.cs`, `Hooks.cs`, `FishInfo.cs`, `Items/LavaFishItems.cs`, `HighSeasFishing.cs`, and `Items/OracleOfTheSea.cs`. `Quests/ProfessionFishQuest/ProfessionalFisherQuest.cs` requires an owned nearby boat and puts accepted orders in its hold; `ShippingCrate.cs` owns progress, turn-in consumption, and deletion. `FishQuestHelper.cs` supplies rewards. The draft makes dock availability conditional on placement. Staff must later use the existing fish-monger setup command; no placement was attempted here.
- **Fishing defects:** [the Iron P587 review](cc-P587-cont-fixup-high-seas-fishing-second-half-codex-review.md) flags hook duplication through a pending target and carving fish after crate credit. Current hook targets lack a renewed ownership/deletion check, and `DeleteQuestItems` does not check consumption success. The player draft acknowledges item-handling defects without publishing duplication steps. Neither defect is treated as repaired by a merge-conflict fix-up.
- **Reward reachability and Charybdis:** `FishQuestHelper.GetTier` tests points at least 100 before its higher thresholds, leaving tiers 3 and 4 unreachable, as [P269's implementation note](cc-P269-high-seas-fishing-second-half.md) already records. Its reachable bait branches select indices below 34; the special Charydbis row is index 35 in `FishInfo.BuildTable`, selected by the unreachable tier-4 branch. `HighSeasFishing.TrySummonCharybdis` requires that bait. This source-derived consequence is not runtime-tested here. The draft describes the Oracle's mechanism but explicitly keeps normal summoning blocked. It does not promise every guide volume or every bait as obtainable. The reachable reward table still includes the Oracle and all three hook types.
- **Pies and Corgul:** `Mobiles/Charybdis.cs` rolls two to five pies. `Items/Fish/FishPies.cs` implements the timed effects; `server/patches/AOS-fish-pies.patch` connects damage reduction and attributes. The Fairy Salmon and Lava effects have no active consumer here. `server/customizations/Engines/Craft/CookingCraftRegistrations.cs` supplies oven recipes. Searched canonical customizations, patches, and pinned ModernUO UOContent for MentoSeasoning, SamuelsSecretSauce, and DarkTruffle: only ingredient definitions and recipe references occur in the shard, with no stock supplier. Their absence and Corgul's unfinished altar/boat access are also recorded in P269's note. Baking and player access remain limited in the draft.
- **Staff maintenance:** compared P479 to its first parent. `scripts/Shard-Console.ps1` adds `mailMode` defaults, accepted settings, and a panel line; `scripts/tests/Shard-Console.Tests.ps1` adds its fact. Other machines or repositories are outside this snapshot. The task title alone is not evidence of storage maintenance taking effect.

## Validation

Documentation only; lane tests are none. No tests or gates were added, so no red-first cycle applies. No build or gameplay test was run.

- Shell: Windows PowerShell `5.1.26100.9711`.
- Ran `tools/progress.py --dry-run` with both work-copy overrides. It completed and identified version `2026.10.25`. Preserved and restored `tools/progress.json` byte for byte around its unconditional write; no generated report is delivered.
- No code, `docs/`, changelog, version, service, package, account, or save changed. No Haven connection, deployment, commit, merge, push, or branch switch occurred.
- Compared the tables with local first-parent history: all 3 code merges and all 11 notes merges match exactly, in order. Each merge and its treatment is listed above.
- Checked both new files directly for relative Markdown links, trailing whitespace, em dashes, and the 5 MB limit. All checks passed. `git diff --check` passed in both work copies.
- Reviewed the player draft for plain American English, release boundaries, known limits, and absence of staff commands or hidden achievement spoilers.
- Only the two requested notes files are delivered. The code copy remains clean, and generated reporting files are unchanged.
- Checked the stop-request path between research, drafting, and validation; it was absent. No work remains for P594.

P594 DONE
