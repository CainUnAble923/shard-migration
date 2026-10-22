# cc-P390: player guide to crafting changes

October 21-22, 2026. Codex lane, Verite-tower. Docs-only draft. Resumed October 22 with explicit Golem authorization and the stop-request file absent. Work copies:

- Code: `D:\UO\golems\Verite-tower\ShatteredLegacy`.
- Notes: `D:\UO\golems\Verite-tower\shard-migration`.

## Historical checkpoint, October 21

The Golem's stop-request file became present at the checkpoint immediately after the guide draft was written. Paused under the prompt's explicit instructions. At that point the task was not complete and the draft had not passed its final editorial and source audit. The completed continuation is recorded below.

Written: `notes/wiki-drafts/crafting-changes.md`. It covers recipe learning, exceptional materials, extended metal and wood ladders, BODs, contracts, commissions, requisitions, levelable gear, and recycling, with Sources and Contradictions at the end. It includes a short Make X section because that directly affects salvage.

No code was changed. No connection to Haven, deployment, Docker operation, commit, merge, push, or branch switch was made. Both work copies were clean at the initial status check. No test or gate was added or run; the task specifies no lane tests. Existing tests were read as corroborating source, not reported as passing in this run.

## Initial read and source scope

Read `AGENTS.md` in both work copies before the substantive work. Read the direction decision and the task list, though the large task-list output was truncated. The current explicit no-commit, no-docs-edit rules take precedence over old commit/push passages.

Read the two required model pages, `notes/wiki-drafts/league.md` and `notes/wiki-drafts/society-of-smiths.md`. Read relevant full feature-queue sections F-18, F-20, F-25, F-28, F-29, F-37, F-42, F-43, F-47, and F-48. Full feature-queue review was not completed. No nested AGENTS file was returned under the canonical source/tests/patches and notes search; an unrelated notes `__pycache__` subtree returned access-denied errors. Do not inspect that scratch subtree on continuation.

The following notes were read in relevant sections or substantial excerpts, not all cover to cover:

- P18 Make X; P23 salvage findings; P53 material tiers; P55 payout choices; P56 economy/smelting; P57 mining tiers; P61 training; P67 crafting ceilings; P70 module schematics; P72 gear research; P78 recipe gating.
- P118 BOD research; P122 BOD core; P123 other crafts; P128 crafting additions; P150 requisitions; P170 teaching-order fix; P203 integration; P226 Arms Lore; P227 wood bonuses; P228 exceptional materials; P235 contract numbers; P261 levelable gear; P285 integration.
- P376 League decision questions, P377 wiki catch-up, P381 Smith guide evidence, and P385 gathering guide evidence.

Some of those were initially identified by keyword/heading searches. Those hits are discovery, not proof of a behavior. At the pause, the remaining topical review included P32, P42, P46, P52 and pertinent portions of P263. The continuation below records those reads and the additional evidence. Reading was focused on relevant sections of cross-cutting notes, not on unrelated deployments, console changes, or achievement triggers.

Canonical code and patches read for behavior include:

- `Engines/Craft/ClusterFRecipeGate.cs`, `ClusterFRecipeTable.cs`, `ClusterFRecipeStore.cs`, `RecipeItems.cs`, `GuildRecipeShopGump.cs`, `ClusterFRecipeRewards.cs`, and `BasketWeavingCraftRegistrations.cs`.
- `ClusterFGuildPromotion.cs`, `ClusterFMetalTiers.cs`, `ClusterFWoodTiers.cs`, `ClusterFCraftGain.cs`, `ClusterFWoodBonuses.cs`, `ClusterFExceptionalMaterial.cs`, and the relevant body of `ClusterFArmsLore.cs`.
- `Services/BulkOrders/BulkOrderSystem.cs`, `BulkOrderVendors.cs`, `BulkOrderGivers.cs`, and `CraftBOD.cs`; `server/patches/LargeSmithBOD.cs` and `SmallBOD-crafted-only.patch`.
- `ClusterFSmithCommissions.cs` generation, validation and payout bodies; `Requisitions/RequisitionSystem.cs` refresh and turn-in bodies.
- `LevelGear/SmithsSealDeed.cs` and the eligibility, XP, spending and read-time bonus sections of `LevelGear/ClusterFLevelGear.cs`.
- `SmithGuildSalvageBag.cs`, `ClusterFCraftRun.cs`, `CraftCountGump.cs`, `ClusterFCraftRejects.cs`, and both recycling-access patches.

All source paths in this list are under `server/customizations/` unless explicitly stated otherwise. The stale `server/uo/` tree was not read.

Verified the pristine reference directly: `git -C D:\UO\ModernUO-pinned rev-parse HEAD` returned `d4531cd94b739613155225c234900de9f47d2c88`. Read its `Projects/UOContent/Engines/Craft/Core/Resmelt.cs` and the recycling body of `Projects/UOContent/Items/Containers/SalvageBag.cs`. No reference file was edited.

## Evidence already established

File:line citations below are code-repo relative. They support the draft and identify issues to finish checking. There are no file:line citations on the player page.

| Claim | Evidence |
|---|---|
| Existing own-recipe gates are checked before free/book bands | `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:126`, particularly `:135`/`:137`; `IsKnown` at `:246`. Read the actual classification and enforcement bodies. |
| Free threshold, band boundaries, merge threshold and prices | `server/customizations/Engines/Craft/ClusterFRecipeTable.cs:36`, `:39`, `:53`, `:56`, `:59`, `:60`. Defaults were read directly. |
| Scroll materials, promotion skill thresholds, starter grants and rotations | `server/customizations/Engines/Craft/ClusterFRecipeTable.cs:62`, `:75`, `:78`, `:81`; actual shop uses the table in `GuildRecipeShopGump.cs:35` and `:55`. |
| Account learning, existing recipe/book synchronization | `server/customizations/Engines/Craft/ClusterFRecipeStore.cs:65`, `:93`, `:147`; `RecipeItems.cs:26` checks backpack, preserves known copies and consumes newly learned ones. |
| Owning guild map | `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:389` through the `BySkill` table. |
| Sparse-band merge and rank-display discrepancy | `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:204`, `:210`, `:351`, `:356`, `:475`; `GuildRecipeShopGump.cs:43` chooses original bands up to rank+1 and `:45` merges them; `ClusterFGuildPromotion.cs:184` merges the granted rank's band. P78's folded-book description and hint text do not describe that shop/grant ordering. |
| Promotion uses base crafting skill and grants books/scrolls | `server/customizations/ClusterFGuildPromotion.cs:68`, `:85`, `:141`, `:173`, `:184`, `:204`. Directly read the skill, cap, update and grant bodies. |
| Smith-only large-BOD recipe hook | `server/customizations/ClusterFSmithBODPayout.cs:190` was the only live call returned by the canonical customization search for `TryLargeBodScroll(`. Hook implementation is `Engines/Craft/ClusterFRecipeRewards.cs:70`; commission selection is empty at `ClusterFRecipeTable.cs:89`. |
| Loot-box and monster-steal recipe callers now exist | `server/customizations/LootBoxes/LootBoxRoller.cs:392` implements the reward choice, with the call at `:394`; `Services/Monster Stealing/Core/StealLootTables.cs:190` implements the choice, with calls at `:199`, `:208`. Continuation read the surrounding fallback and return paths, not just the search hits. |
| Current metal and wood ladders and training ceilings | `server/customizations/ClusterFMetalTiers.cs:20` through `:27` are the metal constants; `:43` requirements, `:70` gain ceilings, `:34` Dawnstone. `ClusterFWoodTiers.cs:19` through `:26` are the wood constants; `:36` requirements, `:54` ceilings, `:33` Rootwood. `ClusterFCraftGain.cs:45` computes the window, `:64` checks consumption, `:76` limits the rule to four crafts, `:87` tests the actual recipe resources, `:101` calls the real gain check. |
| Material multiplier and wood exception | `server/customizations/ClusterFExceptionalMaterial.cs:41` rounds positive values half up; `:45`/`:62`/`:65` select by quality; `:68` scales individual fields but preserves runic ranges; `:113` scales the stock bow switch's changes. `ClusterFWoodBonuses.cs:76`/`:114` contain weapon/shield rows; `:159`/`:182` apply normal plus exceptional additions. The three exceptional-material patches and both wood-bonus patches connect these to actual crafting and property readers. |
| Society salvage is separate from menu recycling | Read all of `server/customizations/SmithGuildSalvageBag.cs`, including its two-ingot minimum, bounded crafted-item formula, material threshold, forge/tool requirements, Seal payout and scissors path. Pristine menu `Resmelt.cs` was read directly and returns half recipe cost for crafted gear, 1 for other eligible gear. The two current Resmelt patches only expose the target/method and add a recycling notification. |
| Levelable gear cannot yet be obtained through a normal player source | Read `server/customizations/LevelGear/SmithsSealDeed.cs`, including its header and target action. A canonical customization/patch search for `SmithsSealDeed` returned only its own definition, constructor and target members. P261 and P377 agree that acquisition is not built. No staff acquisition instructions are included on the page. |
| Levelable item rules and points | `server/customizations/LevelGear/ClusterFLevelGear.cs:44` sets the level-200 default, `:58`/`:59`/`:60` set the 4/8/every-10th defaults; `:341` checks eligible kinds, artifacts and crafted flag; `:398` chooses points; `:469` splits creature XP, `:548` pays worn items, `:586` shares the imbuing slot limit, `:589` checks point purchases. Read these bodies and the existing assertions; no behavior was exercised here. |

The current draft deliberately avoids old recipe inventory counts, a total number of catalog rewards, numeric crafting rates, levelable-gear pacing estimates, and any description of a farming exploit or secret achievement.

## Existing tests inspected so far

Read actual relevant assertions, not just test names, in:

- `server/tests/Engines/Craft/RecipeGatingVerification.cs`: actual menu visibility and account-sharing assertion body.
- `server/tests/Items/ExceptionalMaterialVerification.cs`: armor/weapon material rows and crafting helper.
- `server/tests/Items/ExtendedWoodBonusesVerification.cs`: W1/W2 table assertions, W3 stock and Rootwood comparisons, W4 random-extra parity, start of W5.
- `server/tests/Services/BulkOrders/BulkOrderSystemVerification.cs`: three-offer/six-hour, skill, fill/combine and gold/points turn-in bodies.
- `server/tests/Services/BulkOrders/BulkOrderCraftsVerification.cs`: six-craft offers, large-offer skill gate, small/large fill and stack-count assertions.
- `server/tests/Misc/LevelGearVerification.cs`: curve, points, per-kill cap, owner/pet share and backpack exclusion, property ceilings and slots.
- `server/tests/Items/SalvageBagIngotReturnVerification.cs`: actual crafted PlateChest return of 17 at Mining 100, bounded return assertions, flat 2 for noncrafted items.

These were not executed. Additional gain-ceiling, Arms Lore, Make X and requisition assertions were read during the continuation, listed below. No tests were added for this prose-only task.

## Continuation, October 22

Completed the remaining topic checks and the editorial review. Read additional relevant sections of P29 (salvage labels), P32 (both Smith BOD paths), P36 (starter resources and Rootwood), P42 (choice, teaching and direct large fills), P46 (teaching toggle, commissions and payouts), P52 (Society naming), P72 (point budget, reset and pacing proposals), P78 (promotion and shop), P79 (recipe rewards), P142 (recipe rewards), P199/P245 (later reward additions), P218/P286 (crafter-helper status and training limits), P263 (crafting fixes only), and P379 (reviewed crafting/levelable-gear findings). Also completed relevant feature-queue sections F-1, F-26, F-27 and F-38. P376 is a decision-question sheet, not evidence that its recommendations were accepted.

The draft now dates its source check through October 22. It qualifies book access after sparse-band merges, limits material training extensions to their four supported crafts, distinguishes the Smith's Seal item from Smithing Seals currency, and labels unbuilt player access and other approved future work. Sources and Contradictions remain the final sections. No decision or contradiction was resolved and no wiki seed or published page was changed.

### Additional implementation evidence

| Page claim | File:line evidence, code-repo relative unless marked PIN |
|---|---|
| Free character joining and player directory | `server/customizations/ClusterFGuildSystem.cs:96` registers the player command; `:427` joins using character guild data, with the free-join message in the method; `:890` retrieves that character's record; `:953` draws Show me the way. |
| Pattern book trial waiver and basket book | `server/customizations/ClusterFGuildPromotion.cs:34` and `:38` default the unbuilt trial waiver on. `Services/BasketWeaving/BasketWeavingBook.cs:19` defines account knowledge; `:36` handles reading, with pack, Tinkering and already-known checks. `Engines/Craft/BasketWeavingCraftRegistrations.cs:61` registers the additional key requirement. Ordinary band gating remains a separate check. |
| Imbuing has its own knowledge system | `server/customizations/Imbuing/ClusterFImbueKnowledge.cs:122` reads known property tiers; `:141` uses account data; `:155` checks prior knowledge. The draft links the Artificers guide instead of duplicating its mechanics. |
| Extended mining versus crafting/wood harvesting | `server/customizations/ClusterFMiningExtension.cs:93` builds the extended ore resources from the shared metal constants. `server/patches/Ore-smelt-at-forge.patch:27` reads the same constants for ore-smelt difficulty. `ClusterFLumberjackingExtension.cs:233` still starts the flat-100 harvest rows, while its craft subresources below use the wood-tier table. The guide labels wood requirements as crafting only. |
| Exceptional Arms Lore contribution and upkeep | `server/customizations/ClusterFArmsLore.cs:52`/`:56` compute weapon and armor contributions; `:62` reduces wear; `:103` performs own-gear field maintenance; `:147` modifies tool-repair weakening. Read the implementation, plus actual crafting and maintenance test assertions. |
| BOD craft/giver coverage and normal offer/point rules | `server/customizations/Services/BulkOrders/BulkOrderSystem.cs:52`/`:53` set cache and delay; `:108` consumes an offer; `:191` generates the craft-specific deed with the 70.1 base-skill large rule; `:278` converts point value to the small/large banking fractions. `BulkOrderVendors.cs:301` checks valid/complete/pending status, handles the three point modes, deposits gold and deletes the deed. `BulkOrderGivers.cs:29` checks member and base skill; `:34` maps Foresters and Alembic; `:99` asks which craft where necessary. |
| Reward placeholders remain while later rewards are real | `server/customizations/Services/BulkOrders/BODRewardCollections.cs:89` constructs placeholders; examples remain at `:98` and `:174`. AutomatonActuator at `:186` and RunicMalletAndChisel entries starting `:207` are real constructors. `BODRewardsGump.cs:76` hides a placeholder's buy button, `:90` writes the unavailable text, and `:140`/`:164` refuse buying it. No old catalog count/list was copied into the page. |
| Smith limits, teaching and payout choices | `server/customizations/ClusterFSmithBODSystem.cs:56`/`:57` are the 3/1 limits, `:60` is the 70.1 requirement, `:65` checks it; `:579` counts deeds. `ClusterFSmithBODPayout.cs:159` pays standing and either cash or Seals, rolls turn-in checks, and calls the large recipe hook; `:429` routes member turn-ins at a regular smith. `server/patches/LargeSmithBOD.cs:157` overrides combining for small deeds or direct item fills. |
| Current Smith commission cap, cooldown and payment | `server/customizations/ClusterFSmithCommissions.cs:454`/`:456` set 3/1; `:462` sets five minutes, `:474` reads the cooldown, `:528` enforces it for small generation. `:675` completes sets, pays Seals and standing, and checks Blacksmithy; `:749` completes a small commission. The records store issuance time but impose no completion deadline. `SmithGuildBook.cs:212` draws the commission tab, with requests/turn-ins in the same file. |
| Guild Contracts differ from deeds and commissions | `server/customizations/GuildContractLedgerGump.cs:521` checks and consumes the listed requirements, `:547`/`:548` pay standing/currency and `:551` pays listed gold. This path has no turn-in skill check. The player page does not promise F-20's planned checks here. |
| Personal requisition refresh and turn-in | `server/customizations/Requisitions/RequisitionTable.cs:120` defaults three; `RequisitionSystem.cs:109` caps the guild tier by League gate, `:123` refreshes but preserves live Leads, `:218` consumes the matching backpack item and pays Renown/standing/Appraiser gold. Read the actual turn-in and refresh bodies and test assertions. |
| Guild salvage formula, requirements and benefits | `server/customizations/SmithGuildSalvageBag.cs:62` checks material thresholds, `:84` defines Seal pay, `:126` bounds the crafted return, `:144` consumes eligible items, `:192` checks backpack tool and forge, `:299` cuts with scissors, `:338` does both, `:374` issues the join bag. Failure for insufficient Mining leaves the item. |
| Menu recycling uses a different formula | PIN `Projects/UOContent/Engines/Craft/Core/Resmelt.cs:77` contains the stock material difficulty switch; `:102` returns half recipe cost for a crafted piece, `:106` returns one otherwise. PIN `Items/Containers/SalvageBag.cs:75` has its own stock difficulty switch; `:94`/`:95` clamp Mining before the bag's formula. The shard's Resmelt access/notification patches do not replace these formulas. |
| Make X caps, stops and rejects | `server/customizations/ClusterFCraftRun.cs:84`/`:85` cap the respective modes; `:217` onward checks stopping; `:254` ends a run. `ClusterFCraftRejects.cs:38` specifically finds ordinary SalvageBag, `:47` onward tries menu resmelt, `:64` cuts Tailoring rejects, `:73` uses an owned trash bag, `:81` uses the selected bag, `:91` runs ordinary Salvage All once. The Society bag derives from Bag at `SmithGuildSalvageBag.cs:30`. |
| New Smith Band IV design | `server/customizations/Engines/Craft/ExodusCraftRegistrations.cs:65` adds the dagger at minimum 95.0 without an own-recipe registration, making P78's old no-Band-IV inventory stale. No current item-per-band count is asserted. |

Method line citations identify code read, not a runtime test result. Earlier implementation notes may cite different source revisions; all current-code citations above refer to this work copy.

### Additional test source read

Inspected assertion bodies in these existing files. No test was run, added, or modified:

- `server/tests/Engines/Craft/CraftCeilingsVerification.cs:197` verifies all four material chains against actual menu requirements; `:241` checks that a recipe really consumes the material.
- `server/tests/Skills/ArmsLoreMattersVerification.cs:143` checks exceptional damage at 0/100/200, `:165` caps extra armor points, `:295`/`:319` verify own-gear maintenance and waiting.
- `server/tests/Engines/Craft/CraftXVerification.cs:334` checks direct reject resmelting, `:367` verifies the ordinary salvage bag also consumes a pre-existing item, `:397` distinguishes cutting and bagging Tailoring rejects.
- `server/tests/Misc/RequisitionsVerification.cs:325` checks consumption and the three rewards, `:635` checks quiet expiry and a live Lead surviving refresh.
- `server/tests/Misc/SmithBulkOrderChoiceVerification.cs:194` checks 70.1 with no standing; `:211` checks the fixed 3/1 limits.

### Contradictions and findings left unresolved

The player page keeps the conflicts between guild BOD plans and ordinary points, fixed and rank-based allowances, stale recipe inventories/reward callers, merged-book hints/access, exceptional-wood wording, craft and harvest ladders, League commission plans/current Society commissions, the P72/P261 gear designs, daily refresh/live Leads, and the two salvage-bag types. These are observations, not a choice of replacement policy.

Two implementation concerns belong in a separate code task, not this guide:

- Ordinary menu and ordinary-bag recycling do not have the Society bag's post-Valorite difficulty branches (PIN citations above). The page restricts its tier statement to the Society bag and supplies no bypass instructions. This is ours to investigate, not an upstream defect proved by this documentation run.
- P379 reports incomplete crafted-only enforcement in the ported craft combiner and a real-death-path issue with levelable XP. The relevant current combiner and XP paths were read; these reports were not independently reproduced here. The page confines its crafted-only statement to Smith deeds and makes no claim that killing pets cannot award XP. It contains no exploit procedure or secret achievement details. No fix was made in this docs-only task.

### Verification and limits

Read-only editorial checks ran through `powershell.exe` version **5.1.26100.9444**: every relative Markdown link resolved, no em dash, no code file:line citations on the page, Sources and Contradictions are the final sections, and the only bracket command on the page is the player Guild Directory command. Both deliverables are below 5 MB. `git diff --check` was clean in both work copies; an explicit whitespace check covers the new untracked deliverables too.

The required progress reporter was inspected before execution. Its `--dry-run` still calls `build()`, which writes `tools/progress.json` at `tools/progress.py:722` before the dry-run return at `:737`. To keep this task docs-only, ran the original reporter through a one-use in-memory wrapper with work-copy path overrides and intercepted that specific `Path.write_text` call; no reporter source or generated artifact was changed. Initial output rendering hit the console's cp1252 encoding after the report had been calculated; reran with ASCII-safe output. Result: the reporter completed successfully and the intercepted target was only `tools/progress.json`. Its source-count and backlog output was reviewed; filename-stem coverage is not a behavior measurement and is not quoted on the player page. This is a reporter/console limitation, not a crafting finding.

Unverified: live deployment, live configuration values, client appearance and menus, actual player progression or time-to-level, and the P379 runtime reports. No live or test shard, account, client, container, or network service was touched. Existing test assertions and earlier build notes are evidence about intended/source behavior, not a claim of a new green test run.

Final checks completed: both new Markdown files have final newlines and no trailing whitespace; all page links resolve; both repository whitespace checks are clean. The code work copy is unchanged. The notes work copy contains only the two requested new files. The stop-request file was absent at the final checkpoint. No required work remains for this draft task; publication and runtime checks are outside its scope.

P390 DONE
