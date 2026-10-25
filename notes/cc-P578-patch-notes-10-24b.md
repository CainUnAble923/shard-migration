# P578: patch notes for the rest of October 24

## In plain words

Wrote [the continued October 24 player draft](cc-P578-patch-notes-2026-10-24b.md). It covers the merged Rootdeep, cleanup, mining, League Register, tutorial, smith commission, reward, and hidden achievement changes missing from P541. Known corpse-clearing, satchel, and tutorial limits remain visible. Hidden achievement conditions are not disclosed in the player draft.

The two filenames follow the outer lane's work-record destination and the embedded task's player-draft destination, matching P541's separate draft and evidence-note format. Only these notes are deliverables. No skill is needed for explicitly requested Markdown files.

## Scope and release boundary

Read AGENTS.md in both work copies first, then direction-decision.md, tasks.md, P541's player draft, evidence note, and review. Both work copies began clean. Paths in this note refer to these work copies, not the original folders named by older task notes.

Code snapshot: `bca69995142fa5f24305880a602e6888274364f2` (short name `bca6999`), version `2026.10.24.15`. Notes snapshot: `0460d4b5efec934c10d5a5a46c3135c5fcf6a622`. Coverage stops at these local snapshots, using October 24 merge times in America/Chicago. No remote fetch or service request was used.

P541 merged in the notes repo as `8f4cada`, but its code cutoff was `372bf89`, version `2026.10.24.3`. P413's Rootdeep entrance merged shortly before P541's notes merge and was absent from its player draft. Included P413 to close that gap. The code inventory below is the first-parent range `372bf89..bca6999`; the notes inventory is `8f4cada..0460d4b`. This is a supplement to P541, not a package-to-package comparison. Launcher and chopped-tree changes already covered there are not announced again.

The player draft is pending the next package and server update. Running server version, shared test-world fixtures, effective live settings, package availability, published wiki pages, client appearance, and gameplay outcomes are unverified. Source defaults are used for prices and limits. Implementation notes and review reports are prior evidence, not runtime checks performed for P578.

## Code merge inventory

Every merge in the code range is listed below. Read the change lists against each merge's first parent, the changelog, and relevant implementation paths.

| Merge | Task | Treatment |
| --- | --- | --- |
| `96473d4` | P413 | Rootdeep entrance and ladder landing; matching map required. |
| `86654d1` | P414 | Civic point contracts and old bundle redemption; retain the old-contract ordering caveat. |
| `b23e87f` | P415 | Trash bag corpse actions, confirmation, points, and loot rights; retain known deletion limits. |
| `491bb49` | P416 | Stone learning gate and book, ore quotas, old turn-ins, and missing-voucher gold restoration. |
| `82ba93f` | P427 | Pet XP exclusion, crafted-item bulk order checks, and generic hidden achievement fixes. Internal cleanup and art registry correction omitted. |
| `1c9c5d8` | P451 | League repair, satchel fees and capacity behavior, checked delivery, and nested smith deed turn-in. |
| `1020e36` | P453 | Tutorial pet claims, pending picks, character ownership, bandage cap, actual healing, and outsider protection. Reseeding repair omitted as staff maintenance. |
| `6127603` | P454 | Shared smith commission abandon cooldown. Hidden achievement integration folded into the generic achievement line. |
| `d83b902` | P455 | Boss boxes, rare Self Repair roll, bestiary credit, and pet kill-effect exclusion. |
| `bca6999` | P457 | Hidden achievement corrections described generically; no claim that every requested case is fixed. |

## Notes merge inventory

Every merge after P541 in the notes snapshot is listed here. Reviews, proposals, unpublished guide drafts, and pending play-test plans do not implement gameplay or establish publication. Paired implementation notes support the code inventory above.

| Merge | Task | Treatment |
| --- | --- | --- |
| `5d68019` | P414 | Implementation evidence. |
| `70a3e28` | P415 | Implementation evidence. |
| `0e6ee6e` | P416 | Implementation evidence. |
| `7bad9b4` | P427 | Implementation evidence. |
| `898d461` | P544 | Tree review; no new tree fix. |
| `629809b` | P537 | Port status inventory; no new port. |
| `f469e51` | P545 | Rootdeep review; no additional entrance fix. |
| `d5126c5` | P546 | Civic review; old-contract baseline caveat retained. |
| `310565d` | P547 | Corpse review; confirmation and pet-corpse caveats retained. |
| `6af575f` | P548 | Mining review; no additional quota or restoration fix. |
| `9d8d404` | P451 | Implementation evidence and populated-satchel review caveat. |
| `9a3faab` | P549 | Launcher review; no new launcher fix. |
| `ef0e2a4` | P550 | Town Houses design review; no rentals announced. |
| `63af610` | P551 | Unpublished mining guide draft. |
| `94c7008` | P552 | Unpublished cleanup guide draft. |
| `96b8e4c` | P553 | Unpublished launcher guide draft. |
| `82e76d2` | P554 | League review; no new satchel filtering fix. |
| `7529d1c` | P555 | P427 review; prior evidence and coverage limits. |
| `a352115` | P557 | Unpublished League Register guide draft. |
| `c27c7a4` | P556 | Proposed fix-up prompts; not implemented repairs. |
| `bf672b1` | P558 | Unpublished Requisitions and Leads guide draft. |
| `21d5e1c` | P559 | Unpublished companion guide draft. |
| `ed8f7d2` | P560 | Planned Town Houses guide; no housing system announced. |
| `98bfd6c` | P561 | Wiki draft cross-check; no publication. |
| `b9c724c` | P562 | Draft glossary updates; no new gameplay. |
| `e208e5b` | P563 | Tracking Ping design; not built. |
| `7941129` | P564 | Pumpkin King design; no event announced. |
| `16b9e68` | P565 | League reward token design; no shop change announced. |
| `8356b8b` | P453 | Implementation evidence. |
| `378c0ea` | P566 | Townsfolk feature designs; not built. |
| `fb5878e` | P567 | League summon reward design; not built. |
| `9e4d3cc` | P568 | Attunement design; not built. |
| `3e07963` | P569 | Levelable weapon proc design; not built. |
| `787040a` | P570 | Gate tiles and mount levels design; not built. |
| `91a8aae` | P571 | Butte and deed design; not built. |
| `4b9420b` | P572 | Proposed fix-up prompts; not implemented repairs. |
| `f24bb1d` | P454 | Implementation evidence. |
| `aff0876` | P573 | Tutorial review; failed bandage delivery and deleted-trainee limits retained. |
| `1dc6521` | P574 | Open questions; no new feature or decision treated as code. |
| `c239ca8` | P455 | Implementation evidence. |
| `1d58f2f` | P575 | Weekend summary; not a new release. |
| `7e1c1a0` | P576 | Pending play-test plans; no tests executed or passed by that task. |
| `0460d4b` | P457 | Implementation evidence and remaining requirement caveat. |

## Source checks and editorial choices

Code paths below are relative to the ShatteredLegacy work copy. Linked notes are in this repo. Read the implementation notes for P413, P414, P415, P416, P427, P451, P453, P454, P455, and P457 alongside the changed source.

- **Rootdeep:** `server/customizations/ClusterFRootdeepSeeder.cs` defines the mouth rows, outside ladder landing, and in-place retargeting on reseed. `player-package/vendor/shattered-legacy-map/trammel.mapops` supplies the mound. [P413](cc-P413-rootdeep-anthill-entrance.md) and [P545](cc-P545-review-rootdeep-anthill-entrance.md) supply earlier placement and travel evidence. The draft requires matching maps and does not announce a new dungeon opening, new spawns, or a completed shared-world reseed.
- **Civic Contracts:** `ClusterFWorkOrderSystem.cs` has `WorkOrderCleanUpRequirement`, `Accept`, `CleanUpProgress`, and `ClaimCleanUpPoints`. Earnings remain spendable, but overlapping contract baselines advance after a claim. `ClusterFCustodianSystem.RedeemBundles` deletes old bundles and awards `PointsPerBundle`, default 10. [P546](cc-P546-review-retire-civic-waste-bundles.md) identifies deferred initialization on old entries. Source still initializes their baseline at first inspection, so the draft tells holders to open Active before redemption. No claim of exploit-proof point pricing is made.
- **Corpse clearing:** `TrashBag.cs` adds the two owner/backpack menu entries. `ClusterFCustodianSystem.cs` implements `CanClear`, `LootRightsLapsedFor`, `ClearCorpse`, and `ClearCorpsesNearby`. Player corpses are excluded; criminal and instanced loot checks protect other players' rights. Confirmation deletes remaining contents, and the nearby callback rescans around the player's current location. Bonded pet corpses are not excluded. [P547](cc-P547-review-trash-bag-corpse-clearing.md) records these remaining issues and a missing bag recheck after confirmation. The draft explains the main destructive limits without promising a fixed selection. New labels are in `player-package/vendor/shattered-legacy-cliloc/entries.json` and `registry.csv`; no package was rebuilt here.
- **Mining:** `ClusterFWorkOrderSystem.cs` gates stone work with `NeedsStoneMining`, defines the iron and Dull Copper requirements, and retains legacy turn-ins through `FromBeforeQuotas`. `CompactOreSatchelRoutingHook.cs` counts actual harvest delivery before satchel merging. `MinersCompactLiaisonGump.cs` checks membership, rank, and voucher payment for the book, and recalculates the missing-voucher restoration price at confirmation. The book's 100 base Mining reading rule is also documented by the source references in [P551](cc-P551-guide-mining.md). [P548](cc-P548-review-stone-mining-gate.md) found no player bypass of those gates but records shared-method and coverage risks. Iron Beetle quota credit remains unverified and is not promised. New quota rewards do not consume the mined ore; old material turn-ins do.
- **League Register:** `LeagueRepair.cs` distinguishes `RepairWorn` from `RepairAll` and rechecks the source item in `BeginTarget`. `LeagueConsolidation.cs` applies the item discount only in the direct owner's backpack, charges after successful insertion, and uses checked delivery. `LeagueRegister.cs` scans nested smith deeds in `TurnInAll` and checks delivery before unbinding. [P451's review](cc-P451-fix-league-register-fix-up-repair-targets-codex-review.md) identifies capacity refusal while a populated Field Satchel is lifted; retained in the player limits. [P554](cc-P554-review-league-register-fixes.md) identifies the nested Hunter's Satchel filter gap; do not interpret the resource-routing fix as a comprehensive content-filter repair.
- **Tutorial:** `Tutorial/ClusterFTutorial.cs`, `TutorialFarm.cs`, `TutorialGumps.cs`, and the versioned `TutorialRecord` in `ClusterFAccountData.cs` preserve account pet claims, pending choices, bandage issues, and character ownership. `Bandage-tutorial-real-heal.patch` calls the lesson hook after healing; `Notoriety-tutorial-creature-outsiders.patch` refuses harmful actions by outsiders. `GiveBandages` still spends an issue before unchecked `AddToBackpack`. The ownership fallback also leaves active records stuck when their trainee is deleted, as [P573](cc-P573-review-tutorial-fixes-p453.md) explains. Both limits are retained. The test-shard label follows [P453](cc-P453-tutorial-fixups.md); no live tutorial availability is asserted.
- **Crafting and commissions:** `Services/BulkOrders/CraftBOD.cs` adds `ClusterFStoreBought.Refuses`; the player text refers to the affected shop weapons and clothing rather than claiming new provenance tracking for every item type. `SmithGuildBook.cs` records both abandon paths and displays the wait; `ClusterFSmithCommissions.cs` enforces it for large requests and integrates their completion with an existing hidden achievement. Default `AbandonCooldown` is five minutes. The latter integration is not explained as an achievement recipe.
- **Death rewards:** `LevelGear/ClusterFLevelGear.cs`, `LootBoxes/ClusterFLootBoxes.cs`, `ClusterFRareSelfRepair.cs`, and `Imbuing/ClusterFImbueEffects.cs` now use the earlier creature deletion event with death guards, preserving master and corpse state. The boss path retains looting-rights qualification and its existing first-award rules. The Self Repair roll retains its eligible magic weapon/armor filter and does not make every boss item eligible. `ClusterFLeagueBestiary.KillerOf` resolves pet, summon, and provocation ownership. These source changes support the reward lines; no new loot table or rate increase is claimed.
- **Hidden achievements:** checked the P427 and P457 changes in `ClusterFNotedBySystem.cs` and their registered damage/movement/mining patches. Use only the changelog's generic public wording. [P457's review](cc-P457-fix-noted-by-the-system-fix-up-codex-review.md) says the requested loot recycling exception remains absent. The player draft does not claim complete achievement correctness or reveal triggers, distances, timing windows, or rewards.
- **Wiki and documentation:** actual wiki seed edits in the code range are `docker/wiki/content/pages/uo/guides/crafting.txt`, `guilds/society_of_smiths.txt`, and `systems/league_register.txt`. They clarify the shared commission wait and backpack-only satchel discount. They require a later wiki publish and are not a newly verified wiki release. The other guide and glossary changes remain in `notes/wiki-drafts/`. Design and review merges in the inventory supply context, not features to announce. No Town Houses, Tracking Ping, Pumpkin King, attunement, new League tokens, summons, or progression milestones are presented as built by this interval.

The committed CHANGELOG.md and VERSION are authoritative for the snapshot version. P455's implementation note names .13 and P457's names .14; the merged changelog places their changes at .14 and .15 respectively. The draft uses the date without inventing missing release entries or treating older branch-local version text as current.

## Validation and limits

Docs-only task; lane tests are none. No tests or gates were added, so no red-first cycle applies. No build or gameplay test was run, and no historical test totals are claimed as P578 results.

- All shell commands ran under Windows PowerShell `5.1.26100.9711`.
- Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE set to these work copies. It completed and identified `2026.10.24.15`. Its dry-run still writes `tools/progress.json`; preserved and restored that file byte for byte and confirmed clean Git status afterward. No generated reporting changes are delivered.
- No code, CHANGELOG.md, VERSION, docs/ file, service, account, save, installed tool, or package changed. No Haven connection, build, deployment, commit, merge, push, or branch switch occurred.
- Compared the inventory tables with local first-parent Git history: all 10 code merges and all 43 notes merges match exactly, in order. The tables publish each merge and its treatment beside those counts.
- Reviewed the player draft against the source and known findings: plain American English, no em dashes, no staff commands, no hidden achievement spoilers, and explicit update and known-defect limits.
- Local Markdown links resolve, neither new file has trailing whitespace or an em dash, and both are below 5 MB. `git diff --check` passed in both work copies; the new files were also checked directly because they are untracked.
- Final scope is the two requested notes files. The code work copy remains clean; generated reporting files are unchanged.
- Checked the stop-request path between research, drafting, and validation steps; it was absent. No work remains for P578.

P578 DONE
