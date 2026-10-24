# P514: feature queue audit, round 2

October 23, 2026. Read-only comparison of `docs/feature-queue.md` with local main.
No queue or code edits are proposed by this file itself. Suggested lines are for
the overseer to apply after review.

Both prompt work copies matched main at the start:

- Code: `6f540be8b84f63f76b8852fe638039b363b66a6b`.
- Notes: `d80e795115eafda1946071aadd9d46516b8680ba`.
- Read-only pinned upstream: `d4531cd94b739613155225c234900de9f47d2c88`.
- P398 baseline: code `b240bb4d6e47d72ab6be6aafc202b6b28833a7c1`, notes
  `e3d2a0a060e36215a2c20a19d891ae30c023f806`.

Read P398's task note, its audit `feature-queue-audit-2026-10-22.md`, and its review
before comparing the queue. Rechecked source at the older audit's citations and
the changes since that snapshot. The important new implementation is F-35's
tutorial lessons and evo additions, and F-49's test-only hall placement. The
October 23 decision block under F-24 also settles several older contradictions.

Built here means code and its integration exist in main. It does not establish
deployment, shared test-world placement, package publication, or a fresh client
check. A partly built entry names the remaining implementation. Research alone
does not make a feature built. "Keep" identifies an existing disposition that
still describes the feature, although its wording can be made clearer.

References use these roots:

- `Q:line`: `docs/feature-queue.md` in this notes repo.
- `C/`: `ShatteredLegacy/server/customizations/`.
- `P/`: `ShatteredLegacy/server/patches/`.
- `K/`: `ShatteredLegacy/` for client and package files.
- `N/`: this repo's `notes/`.
- `U/`: read-only `D:/UO/ModernUO-pinned/Projects/UOContent/`.

## Every queue entry

The table enumerates F-1 through F-51 once each, including dropped F-2. The old
Open heading, handoff, and repeated Batched rows also need to follow these statuses.
Status descriptions below summarize the entry plus any newer decision that governs it.

| Entry | Status says | Main shows | Suggested status line |
|---|---|---|---|
| F-1: Craft X through failures | Open; batched P18 (`Q:158`). | Item and attempt modes, exceptional runs, caps, and reject handling exist: `C/ClusterFCraftRun.cs:84`, `C/ClusterFCraftRun.cs:138`, `C/ClusterFCraftRejects.cs:27`. | Built: P18, with the Clean Up trash route connected by P33. |
| F-2: Diminishing Custodian returns | Dropped for F-3 (`Q:3604`). | Cleanup uses Clean Up valuation and points; Civic Tokens are retired: `C/ClusterFCustodianSystem.cs:156`, `C/ClusterFCustodianSystem.cs:214`. | Keep Dropped: replaced by F-3; no diminishing-return system required. |
| F-3: Custodians and Clean Up Britannia | Open; batched P33 in the batch table (`Q:214`, `Q:3591`). | Character points, owned trash bags, standing, and the shared reward store exist: `C/ClusterFCustodianSystem.cs:176`, `C/TrashBag.cs:76`, `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:84`. | Built: P33; reward reachability completed by P175. |
| F-4: One character per account | Decided, unscheduled, with staff/test exemptions (`Q:360`). | Creation still uses the upstream account limit: `C/CharacterCreation.cs:161`, `U/Accounting/Account.cs:461`. | Keep Planned: single-character enforcement and exemptions are not built; starts with the fresh world. |
| F-5: Young by time played | Open; batched P18 (`Q:365`). | The 336-hour clock and removal of the skill cutoff exist: `C/ClusterFYoungPlayer.cs:35`, `P/PlayerMobile-young-time-only.patch:3`. Graduation leaves Young running: `C/Tutorial/ClusterFLoops.cs:45`. | Built: P18; restartable clock P192; graduation preserves Young P371. |
| F-6: World-map fog | Server half exists; client half needs scoping before batching (`Q:431`, `Q:459`). | Server tracking and the TazUO packet/overlay patch exist: `C/ClusterFExplorationManager.cs:51`, `K/client/patches/0004-world-map-fog-of-war.patch:121`. Map learning still has no exploration caller: `C/Engines/Craft/ClusterFRecipeRewards.cs:10`. | Partly built: server and client fog built, including P240/P352/P357; traded-map reveals, treasure-map reveals, walked-percent achievements, and exploration Cartography gains remain planned. |
| F-7: Player account reset | Open; batched P18 (`Q:463`). | Stone and self-reset share the reset path, including separate character guild records and exploration cleanup: `C/ClusterFResetStone.cs:113`, `C/ClusterFDevTools.cs:79`, `C/ClusterFDevTools.cs:153`. | Built: P18; test-world reset tool. |
| F-8: Animated runestone and art pipeline | Handoff says shipped; entry says ready to batch (`Q:123`, `Q:574`, `Q:576`). | Standalone runestone variants and the local client override route exist: `C/ShatteredRunestone.cs:83`, `K/player-package/payload/app/Build-UoOverrides.ps1:1`. | Built: P26. Future use as the progression loop stone belongs to F-12. |
| F-9: Guild starter path | Open; batched P15, with P22/P48 follow-ups (`Q:580`, `Q:848`). | Tool claims, starter rewards, directions, and welcome pages exist: `C/ClusterFGuildStarterPath.cs:290`, `C/ClusterFGuildStarterPath.cs:405`, `C/ClusterFGuildStarterPath.cs:588`. Loop completion does not reset starter claims: `C/Tutorial/ClusterFLoops.cs:47`. | Starter path built: P15/P18/P22/P48/P77. Reissuing starter rewards on later loops still awaits F-12 integration. |
| F-10: Gargoyle starting-town choice | Decided; not scheduled (`Q:880`). | Royal City is declared, but the offered creation locations still return New Haven only: `C/CharacterCreation.cs:119`, `C/CharacterCreation.cs:129`. A Royal City guild hall does not implement a start choice. | Keep Planned: Ter Mur default, New Haven choice, and the second starter route are not built. |
| F-11: Bank resources for guild services | Open; batched P22 (`Q:885`, `Q:3587`). | Shared helpers count and consume across pack, bank, and nested resource containers: `C/GuildResources.cs:96`, `C/GuildResources.cs:184`, `C/GuildResources.cs:294`. | Built: P22 for guild services and work-order resource use. Ordinary crafting bank access is F-34. |
| F-12: XP, player levels, loops | Research P20/P54; handoff still says on hold; entry defers to the revised design note (`Q:80`, `Q:928`). | Flat skill caps and gain paths exist, as do the ladder helper and first graduation loop. The actual level/skill-reset integration remains empty: `C/ClusterFSkillCaps.cs:11`, `C/Tutorial/ClusterFLoops.cs:31`, `C/Tutorial/ClusterFLoops.cs:40`. P282 is research: `N/cc-P282-f12-numbers-and-level-gates.md:3`. | Partly built: skill paths and graduation loop only. XP, leveling, enforced level-based skill caps, real resets, echo, Keeper/Breaker, and Legacy progression remain planned; current design and numbers are in the revised F-12 note/P282. |
| F-13: AP/Renown shop and titles | Entry says ready to batch; newer F-24 decision says the shop is delivered (`Q:1383`, `Q:2025`). It still describes the veteran +50 stat cap (`Q:1370`). | Shop, titles, Hall page, and now reward-mount rows exist: `C/LeagueShop/LeagueShop.cs:37`, `C/LeagueShop/LeagueShop.cs:121`. The veteran +50 was withdrawn, not left to build: `N/p25-decisions-2026-10-02.md:27`, `N/f12-levels-loops-caps.md:78`. | Shop and titles built: P229/P243; mount rewards added P365. Player-level gates await F-12. Mark the veteran +50 and earlier stat/XP reward proposal as superseded; follow the October 23 shop decision. |
| F-14: Creature levels and Appraisal | Ready to batch; creature details can precede F-12 (`Q:1463`). | Difficulty levels, Appraisal detail tiers, stat card, and skill rename exist. Player comparison is provisional and con appears on a separate click line: `C/ClusterFCreatureLevels.cs:50`, `C/ClusterFCreatureLevels.cs:165`, `C/ClusterFCreatureLevels.cs:251`. | Partly built: P239 creature levels/Appraisal. Real player-level comparisons, item requirements, and the creature-half unlock quest remain planned. |
| F-15: Version and patch notes | Open; batched P22 (`Q:1466`, `Q:3589`). | Image-supplied version/changelog parsing, login notices, links, and history UI exist: `C/ShardVersion.cs:5`, `C/PatchHistoryGump.cs:3`. P288 also fills the package's What is new line through `K/scripts/Shard-Console.ps1:9037`. | Built: P22/P26/P64, with package integration P153/P288. Current wiki publication remains an external check. |
| F-16: Cheaper pickaxe restoration | Ready to batch; P22 batch row (`Q:1551`, `Q:3584`). | T1 and T2 prices are the approved constants used by the liaison: `C/MinersCompactLiaisonGump.cs:43`, `C/MinersCompactLiaisonGump.cs:49`. | Built: P22. |
| F-17: Container-to-BOD combine | Ready to batch; P22 batch row (`Q:1591`, `Q:3588`). | Small/large BOD container-combine UI and handlers exist: `P/BOD-combine-contained.patch:3`. Later craft BODs use those paths. | Built: P22; later craft deeds P123. |
| F-18: BOD skill training | Explicitly partly delivered by P42; tailoring, per-five checks, beginner track left (`Q:1636`). | Smith teaching selection exists. Turn-in checks still use small/large/material rules; tailoring still uses OSI points: `C/ClusterFSmithBODSystem.cs:461`, `C/Services/BulkOrders/BulkOrderVendors.cs:158`. | Keep Partly built: P42 smith teaching selection; tailoring guild training, one check per five items, and the under-50 track remain planned. Later OSI BOD ports do not finish this design. |
| F-19: Larger banks | Ready to batch; base P22, rank bonus described as a stub (`Q:1674`). | Base capacity plus active milestone bonus exist: `C/ClusterFBankLimit.cs:26`, `C/ClusterFBankLimit.cs:46`. The newer decision explicitly replaces per-rank wording: `Q:2022`. | Built: P22 base plus P48 milestone bonuses. Replace the old stub and per-rank description with the October 23 milestone rule. |
| F-20: Other craft and gathering BODs | Ready after F-18; wider skill list decided (`Q:1712`, `Q:1725`). | Added craft BOD types, issuers, and OSI points banking exist: `C/Services/BulkOrders/BulkOrderGivers.cs:34`, `C/Services/BulkOrders/BulkOrderVendors.cs:39`, `C/Services/BulkOrders/BulkOrderSystem.cs:81`. The wider training design is not thereby complete. | Partly built: OSI craft BODs P118/P122/P123. Cartography/Fishing training deeds and the broader guild-currency/turn-in training rules remain planned. |
| F-21: New Haven community art | Ready after F-8; placement walk still requested (`Q:1801`). | Selected packs have art records, placement data, and a seeder: `C/ClusterFCommunityArtSeeder.cs:39`, `C/ClusterFCommunityArtSeeder.cs:93`, `C/ClusterFCommunityArtLayout.cs:1`. | Built: P237 selected community-art layout. Shared-world placement, client walk, and publication are not established by this audit. |
| F-22: Winter decorations | Batched P34 (`Q:1875`). | Seasonal dates, stock/community layers, and advent calendar exist: `C/ClusterFWinterDecorSeeder.cs:108`, `C/ClusterFWinterDecorSeeder.cs:227`, `C/WinterAdventCalendar.cs:1`. | Built: P34/P266, including seasonal switching. Current world enablement remains unverified. |
| F-23: Paperdoll replacements | Approved for everyone; checks still required before batching (`Q:1914`). | Package scripts ship the default body art; local body selection and client option exist: `K/player-package/payload/app/Paperdoll-Bodies.ps1:5`, `K/client/patches/0002-paperdoll-bodies-option.patch:1`. | Built in client/package sources: P81/P111/P124. Published package and current rendering remain unverified here. |
| F-24: League jobs and commissions | Research P47; batch 1 P48; later engine batches; October 23 decisions recorded (`Q:1998`, `Q:2018`). | Metal ranks, promotion framework, milestone bonuses, and bestiary foundation exist. Promotion jobs and story trials remain waived: `C/ClusterFLeagueRanks.cs:182`, `C/ClusterFLeagueRanks.cs:188`, `C/ClusterFLeagueBestiary.cs:56`. Requisitions are a separate built system. | Partly built: P48 ranks/signposting and P364 bestiary. Shared jobs, objectives/party work, job pay banking, citizen commissions, and story trials remain planned. Use the October 23 decisions for chapters, milestones, and posting permissions. |
| F-25: BOD banking and direct large fills | P42 partly delivered; bank/cash/ask, other crafts, add-ons and caps described as follow-up (`Q:2111`). Later decision makes bonuses milestone-based (`Q:2022`). | Smith payout modes, direct large fills, and other crafts' OSI banking exist. Smith deed caps are still fixed, and rewards do not distinguish direct fill: `C/ClusterFSmithBODPayout.cs:64`, `C/LargeBODItemFill.cs:28`, `C/ClusterFSmithBODSystem.cs:56`, `C/ClusterFSmithBODSystem.cs:461`. | Partly built: P42/P55/P57 and P118/P122/P123 cover payout choice, direct fill, and OSI banking. Milestone-based deed caps, reduced direct-fill bonus, and the requested guild add-on stores remain planned. |
| F-26: Arms Lore to 200 and new uses | Base work can go first; expose weakness and attunement approved (`Q:2180`). | Craft bonuses, reduced wear, field maintenance, repair support and gain path exist: `C/ClusterFArmsLore.cs:52`, `C/ClusterFArmsLore.cs:65`, `C/ClusterFArmsLore.cs:103`. | Partly built: base Arms Lore P226. Expose weakness and player-level gear attunement remain planned. |
| F-27: Very rare Self Repair | Batched P32 Part C (`Q:2224`). | High-end death-source roll and runic exclusion exist: `C/ClusterFRareSelfRepair.cs:40`, `C/ClusterFRareSelfRepair.cs:43`, `P/BaseRunicTool-no-random-self-repair.patch:1`. | Built: P32. Fixed artifact properties retain their own values. |
| F-28: Extended wood bonuses | Ready with/after F-29 and the ranged fix (`Q:2301`). | Weapon/shield tables, exceptional additions and craft gates exist; lower-level requirement values are stored only: `C/ClusterFWoodBonuses.cs:34`, `C/ClusterFWoodBonuses.cs:76`, `C/ClusterFWoodBonuses.cs:204`. | Partly built: P227 wood effects and gates. Lower player-level requirements await F-12. |
| F-29: Exceptional material multiplier | Ready; every material gets x1.5 (`Q:2344`). | Multiplier code exists, but explicitly excludes F-28's extended-wood table, which has separate exceptional rows: `C/ClusterFExceptionalMaterial.cs:23`, `C/ClusterFExceptionalMaterial.cs:41`. | Implemented by P228 with an unresolved scope difference: extended woods use F-28 additions instead of the blanket x1.5 rule. Review that exception before marking the full entry complete. |
| F-30: Staff Hub and Events | First build P51; Events still described as the next batch (`Q:130`, `Q:2347`, `Q:3597`). | Commands, player/travel tools, saved spots, and Events surges/prizes exist: `C/StaffHub/StaffHubGump.cs:56`, `C/StaffHub/ClusterFSurge.cs:39`, `C/StaffHub/ClusterFSurge.cs:234`. | Built: P51 hub and P230 Events. Future F-12 panels wait for their subsystem. |
| F-31: Raptor pack friends | Batched P51; after the upgrade (`Q:2424`, `Q:3597`). | Behavior is restored through the pinned Raptor patch: `P/Raptor-pack-friends.patch:1`. | Built: P51. |
| F-32: Dungeon chests and mimics | P49 decisions complete; ready for chest-system build; P50 named for mimic (`Q:2529`). | Stationary mimic, spring helper, combat and pet conversion exist. No production caller springs it from ordinary dungeon chests: `C/Mobiles/Normal/ChestMimic.cs:671`. | Partly built: P50 mimic. P49 chest-depth, loot/refill, traps and random mimic-trigger integration remain planned. |
| F-33: Multi-guild work and mule upgrades | P47 research; mule core/modules still described as ready unnumbered prompts (`Q:2635`). | Acquisition, tiers, breeding and module framework exist. Several effects are partial/stubbed, including dismount resistance and property sockets: `C/Mobiles/Mule/MuleErrand.cs:107`, `C/Mobiles/Mule/MuleModuleData.cs:62`, `C/Mobiles/Mule/MuleModuleData.cs:118`. | Partly built: mule P69/P70, learned schematics P78, portable imbuing P82. Multi-guild jobs, unfinished module effects, and Clockwork Scavenger remain planned; Scavenger is retained by the October 23 decision. |
| F-34: Crafting bank-access item | Decided; with future League batches (`Q:2768`). | Register bank summary and F-11 helpers exist, not ordinary-crafting unlocks or range tiers: `C/LeagueRegister/LeagueRegisterGump.cs:20`, `C/GuildResources.cs:159`, `N/cc-P280-league-register-build.md:145`. | Partly built foundation: P280 Register summary only. Per-guild crafting access and its range tiers remain planned. |
| F-35: Tutorial story and evo pets | P59 stage research; framework with art-pending rows; story/farm plan and later trials (`Q:2771`, `Q:3013`). | Core handlers and all listed optional lessons now exist: `C/Tutorial/TutorialStations.cs:176`, `C/Tutorial/TutorialWingTrials.cs:120`, `C/Tutorial/TutorialTradeTrials.cs:76`. P365 adds Horse/Lizard and the dog's wolf choice; fox/bird/kitsune rows remain pending: `C/Mobiles/Evo/EvoPetData.cs:119`, `C/Mobiles/Evo/EvoPetData.cs:149`. | Partly built overall: tutorial core and all listed wings built P289/P475/P480/P290/P291, farm P276, graduation P371; evo framework P65 with additions P365. Real progression, Bond Trial, role abilities, and remaining fox/bird/kitsune stages are still planned. See review defects below. |
| F-36: Climbing boots and mined-block ledger | Design and placeholder prices; no delivered status (`Q:3023`). | Tiers, purchase/restoration, mining/block gates, hops, stamina/cooldown and ledge memory exist: `C/ClusterFClimbing.cs:123`, `C/ClimbingBoots.cs:61`, `C/ClimbingBoots.cs:87`. | Built: P238/P278. Live mountain/client checks and tuning remain separate. |
| F-37: Commissions move to the League | Ready after the contract engine, mistakenly called P48's engine (`Q:3133`). | Smith commissions still pay smith standing/seals directly: `C/ClusterFSmithCommissions.cs:675`, `C/ClusterFSmithCommissions.cs:757`. League deadlines/Infamy and other-guild expansion are absent. | Keep Planned implementation: P46 improved smith commissions, but the League move awaits the unbuilt shared contract engine. P48 built ranks, not that engine. |
| F-38: Rolled gathering contracts | Needs a numbers pass before batching (`Q:3167`). | P235 delivered the numbers proposal; source still registers fixed orders: `N/cc-P235-work-order-numbers-pass.md:3`, `C/ClusterFWorkOrderSystem.cs:347`, `C/ClusterFWorkOrderSystem.cs:382`, `C/ClusterFWorkOrderSystem.cs:1991`. | Research/numbers proposal delivered: P235. Rolled contract types, balancing changes and first-Haul integration are not built. |
| F-39: More dismount sources | Planned; exact sources open; assumes mule resistance already hooks a check (`Q:3184`). | P234 is design only; Steady Hoof Wraps is still stubbed, with no shared resistance check: `N/cc-P234-dismount-sources-design.md:10`, `C/Mobiles/Mule/MuleModuleData.cs:116`. | Design pass delivered: P234; new sources and the shared mule-resistance hook remain planned. |
| F-40: Achievement loot boxes | Designed; phase-1 prompt unnumbered (`Q:3193`). | Award/open/roll flow and achievement/boss/rank/loop hooks exist; level snapshots still use skills: `C/LootBoxes/ClusterFLootBoxes.cs:58`, `C/LootBoxes/ClusterFLootBoxes.cs:86`, `C/LootBoxes/ClusterFLootBoxes.cs:132`. P365 adds mount pool rewards. | Partly built: P79 boxes, P371 first-loop award, P365 mount rewards. Dungeon-clear tracking and actual player-level/loop-scroll progression remain planned. |
| F-41: Fanfare | Two phases; shares F-40's unnumbered prompt (`Q:3218`, `Q:3225`). | Server tiers, merging and mute state exist. Custom voice hook remains unset: `C/LootBoxes/ClusterFFanfare.cs:32`, `C/LootBoxes/ClusterFFanfare.cs:49`, `C/LootBoxes/ClusterFFanfare.cs:76`. | Server phase 1 built: P79. Client voice/new-effects phase 2 and sources depending on unbuilt levels/trials remain planned. |
| F-42: Epic crafting | Explicitly planned; not designed (`Q:3228`). | Epic components can roll in boxes; recipe-source restrictions exist, not the epic crafting system: `C/LootBoxes/LootBoxItems.cs:412`, `C/LootBoxes/LootBoxRoller.cs:460`, `C/Engines/Craft/ClusterFRecipeRewards.cs:103`. | Keep Planned: epic crafting is not built; component drops and source restrictions are foundations only. |
| F-43: Recipe gating and Alembic | Designed; prompts still unnumbered; Imbuing separate (`Q:3239`). | Account learning, books/scrolls, craft-menu gates and guild promotions exist. Region-map helper still has no exploration caller: `C/Engines/Craft/ClusterFRecipeStore.cs:93`, `C/Engines/Craft/ClusterFRecipeGate.cs:126`, `C/Engines/Craft/ClusterFRecipeRewards.cs:136`. | Core recipe gating built: P77/P78; separate Imbuing P82. Region-map learning, custom/epic recipes and sources tied to unbuilt commissions remain planned. |
| F-44: Inn room | Outline decided; room/rent/storage details open (`Q:3295`). | Housing now has a walking tour, not an instanced room: `C/Tutorial/TutorialTradeTrials.cs:168`. No room/rent/transfer implementation was found. | Keep Planned: housing lesson built by P291, but the inn room itself is not built. |
| F-45: Rootdeep creatures and tutorial Vault | Ready for prompt numbering; depends on F-46 (`Q:3336`). | Creature families, tutorial loot, Vault access/exit, map/placement support exist: `C/Mobiles/Burrows/VaultCreatures.cs:1`, `C/Mobiles/Burrows/GloomCreatures.cs:1`, `C/Regions/RootdeepVault.cs:37`, `C/ClusterFRootdeepSeeder.cs:42`. | Built in source: P140/P141, with later map/placement work P167/P188. Current shared-world/client state remains unverified here. |
| F-46: Creature-body delivery route | No third-party creature body has shipped; route blocks every such mob (`Q:3340`). | Anim7/body conversion/type records and package override assembly exist: `K/player-package/payload/app/Build-UoOverrides.ps1:38`, `K/scripts/build-equip-anims.py:256`. P277/P365 add further mount/evo bodies through that route. | Route built: P139/P140; extended P277/P365. Each additional body still needs its own registration and client check; pending evo rows are not automatically enabled. |
| F-47: Requisitions and Appraiser | Own entry waits on an unnumbered prompt; later F-24 decision says built as changed (`Q:3385`, `Q:2029`). | Board, daily rolls with live-Lead retention, rank gates, Appraiser and payouts exist: `C/Requisitions/RequisitionSystem.cs:109`, `C/Requisitions/RequisitionSystem.cs:123`, `C/Requisitions/RequisitionSystem.cs:218`. Custodians post no requests; no new hunt engine was added. | Built: P150/P203, as accepted October 23. Update the entry's old refresh/non-member wording; retain the Custodian exception and future hunt linkage explicitly. |
| F-48: Leads | Own entry still gives the old doubled-chance/loot-table design; F-24 accepts the implemented alternative (`Q:3396`, `Q:2029`). | Personal area/group/Fame-qualified Leads, expiry, extra roll and pity guarantee exist: `C/Requisitions/RequisitionLeads.cs:50`, `C/Requisitions/RequisitionLeads.cs:161`, `C/Requisitions/RequisitionLeads.cs:211`. | Built: P150/P203, as changed and accepted October 23. Replace old 2x/loot-table wording with extra roll, pity, and area/group/Fame qualification. |
| F-49: Real guild halls | Unnumbered survey, places nothing; facets/sites open (`Q:3449`, `Q:3455`). | P281 adds test-only hall placement, NPCs, signs, decor, buildings and travel-stop data: `C/ClusterFGuildHallPlacement.cs:57`, `C/ClusterFGuildHallPlacementData.cs:41`. Maritime explicitly waits on P268: `C/ClusterFGuildHallPlacementData.cs:153`. | Partly built: P151 survey and P281 test-only halls. Maritime, the player travel network, top-rank trials, directory/live release integration remain pending. Review placement defects before declaring complete. |
| F-50: Unravel-result satchel routing | Batched P137 section 6 (`Q:3467`). | Satchel recognizes custom PropertyEssence and stock unravel materials, stores or falls back to backpack, and pickup routing exists: `C/ArtificersSatchel.cs:68`, `C/ArtificersSatchel.cs:96`, `C/ClusterFBackpack.cs:50`. | Built: P137; container unraveling later P176. Use PropertyEssence for the custom output's name rather than treating Essence Shards as another missing item. |
| F-51: Herbalism and reagent growing | Design settled; P260 research/phased plan (`Q:3573`). | P260 is research. Raised beds are an earlier plant port, and the newest tutorial still says Herbalism is unbuilt: `N/cc-P260-herbalism-research.md:5`, `C/Services/Plants/Raised Garden Beds/RaisedGarden.cs:23`, `C/Tutorial/TutorialTradeTrials.cs:69`. | Keep Research delivered, implementation planned: P260. Raised beds P128 do not supply Herbalism, reagent strains, kit/familiar, yard tool, or public plots. |

## Changes to P398's conclusions

### Tutorial and pet scope

P398's lesson-preview finding is obsolete for the current station list. The core
table in `C/Tutorial/TutorialStations.cs:54` and its handlers at line 176, plus
`C/Tutorial/TutorialWingTrials.cs:59`, `:120` and
`C/Tutorial/TutorialTradeTrials.cs:76`, cover these keys:

- Core: `core.movement`, `core.backpack`, `core.paperdoll`, `core.chat`,
  `core.death`, `core.banking`, `core.travel`, `core.league`, `core.loop`.
- Combat/magic: `combat.weapons`, `combat.healing`, `magic.magery`,
  `magic.necromancy`, `magic.chivalry`, `magic.bushido`, `magic.ninjitsu`,
  `magic.mysticism`.
- Gathering/crafting/animals: `gathering.mining`, `gathering.lumberjacking`,
  `gathering.fishing`, `gathering.camping`, `crafting.blacksmithy`,
  `crafting.tailoring`, `crafting.carpentry`, `crafting.tinkering`,
  `crafting.alchemy`, `crafting.fletching`, `crafting.cooking`,
  `crafting.inscription`, `crafting.cartography`, `animals.taming`.
- Other: `bard.trial`, `thieving.trial`, `housing.basics`, `travel.wing`,
  `reputation.wing`, `shard.systems`.

The fallback page still exists, but its existence no longer proves a listed
station is unfinished. Historical notes report scratch-world play-throughs:
`N/cc-P289-tutorial-core-trials.md:5`,
`N/cc-P290-tutorial-wing-trials-combat-magic.md:5`, and
`N/cc-P291-tutorial-wing-trials-trades.md:5`. Those are historical results, not
tests rerun by this audit.

P365 expands the evo data to Horse and Lizard and changes the dog's final choice
to great wolf or windrunner. It does not fill the fox/bird/kitsune pending rows,
build the Bond Trial, or connect owner loops to real progression.
`C/Mobiles/Evo/EvoPet.cs:28` still defaults `OwnerLoopsSource` to zero.
`N/cc-P365-reward-mounts-and-evo-stages.md:25` explicitly says no world ran and
the player package was not built or published in that task.

### Guild halls

P398's "not started" placement conclusion is obsolete. The source table at
`C/ClusterFGuildHallPlacementData.cs:41` lists these halls: `league`, `warriors`,
`arcane`, `healers`, `rangers`, `mining`, `smithing`, `tinkers`, `thieves`, `dojo`,
`keepers`, `foresters`, `tailoring`, `merchants`, `bards`, `artificers`, `alembic`,
`custodians`. `maritime` is in the waiting table, not the placement table.

P281's opening summary says the halls are on the test shard. Its precise account
says the proof used a private copy and the shared Test Shard still needs placement
after merge: `N/cc-P281-guild-halls-placement.md:241`. Use "test-only placement
built and exercised on a private copy" rather than claiming current shared-world
placement. The table records travel stops, not a built player travel network
(`N/cc-P281-guild-halls-placement.md:106`). Existing NPC services come with the
placed guildmaster types; P281 does not build the missing top-rank trials.

### Resolved decisions and an older audit correction

The only feature-queue change since P398 is the October 23 decision block under
F-24, `Q:2018-2034`. It accepts named chapter milestones and six chapters,
milestone-only bonuses, the delivered Renown shop, requisitions/Leads as built,
immediate requisition standing for non-members, and the retained Clockwork
Scavenger. It drops League Warehouse and Featherweight. These are settled
decisions, not questions to reopen. Old lines elsewhere in the queue still need
to be labeled history or updated. In particular, F-47/F-48 should not remain
"waiting" or keep the superseded 2x loot-probability design.

P398 also described veteran +50 as missing implementation. That was incorrect:
Chase withdrew it on October 2 (`N/p25-decisions-2026-10-02.md:27`), and the
governing F-12 note records the withdrawal at `N/f12-levels-loops-caps.md:78` and
`:94`. The queue's F-13 cap paragraph is stale; it is not a reason to schedule a
new reward override. The earlier September 30 veteran XP paragraph is retained
as superseded reasoning, so it should not be silently revived as pending work.

## Defects and unresolved differences that limit a completion label

This is a status audit, not a new defect-fixing task. The following review findings
remain visible in the reviewed source and matter when describing the newly built
features:

- F-49: open doors are found by their current position instead of closed position,
  and an existing guild sign bypasses stock-sign reconciliation:
  `C/ClusterFGuildHallPlacement.cs:152`, `:187`;
  `N/cc-P281-guild-halls-placement-codex-review.md:10`.
- F-35: tutorial entry is disabled outside test mode while the island gate can
  still require graduation. Trial pages also bypass the earlier core client-window
  buttons: `C/Tutorial/ClusterFTutorial.cs:46`,
  `C/Tutorial/TutorialIslandGate.cs:27`,
  `N/cc-P475-cont-fixup-tutorial-core-trials-playable-codex-review.md:10`.
- F-35: the veterinarian's retained offer lacks a fresh vet-proximity check:
  `C/Tutorial/TutorialPetCare.cs:136`,
  `N/cc-P480-tutorial-first-play-fixes-codex-review.md:10`.
- F-35: trade trials share placement tiles, the borrowed Hiding base lacks restart
  recovery, and Fishing completion can precede an actual catch:
  `C/Tutorial/TutorialTradeTrials.cs:292`, `:455`, `:575`;
  `N/cc-P291-tutorial-wing-trials-trades-and-more-codex-review.md:10`.

The P475, P480 and P291 reviews also limit confidence in their play-through
evidence: the merged P289 play-through was not rerun in P475, the P480 runner can
pass with missing graduation rewards, and P291's selected-trial rerun falsely
applies fresh-character assertions. Those are recorded in each task's review
note. No new client or runtime verification was attempted here.

Other unresolved differences from P398 still apply where the table names them:
F-29's extended-wood exception, F-25's direct-fill/cap/store work, the missing
F-32 spring caller, F-33's partial effects, and F-43's missing map-learning caller.
F-43 also checks an existing OSI recipe before its free-skill band
(`C/Engines/Craft/ClusterFRecipeGate.cs:135`), so the queue should not imply every
item below the free threshold bypasses existing OSI recipe requirements.

## Verification and limits

Primary evidence is the source cited in the table, checked against main and the
P398-to-main diff. Notes establish prompt history, decisions, and the limits of
earlier verification. Source-presence findings are not a new full fidelity audit
of each system. Absence findings also use the current implementation and the
unchanged relevant trees since P398, not a keyword search alone.

No tests added or run; lane tests are none. No build, package publication, live
inspection, Haven connection, deployment, account operation, commit, merge, push,
or branch switch. No `docs/` or code changes. The generated `server/uo/` tree was
not used as evidence. Current configuration, shared-world state, installed client
rendering, publishing state, and play pacing remain unverified.

Final validation passed: the table has exactly the F-1 through F-51 row set, no
duplicates, and four columns per row. Checked cited source-file existence and
line bounds, and reviewed queue citations against their text. Both notes use
ASCII punctuation, have no trailing whitespace, and are below 5 MB. Both repos
pass `git diff --check`; tracked files match main, the code work copy is clean,
and only the two requested P514 notes are new. Snapshot refs still match those
above. Stop-request checks remained clear through finalization.

Ran `tools/progress.py --dry-run` against these work copies, exit 0. P398's
reported dry-run defect still exists: the renderer writes progress.json before
the dry-run return. For this audit, a process-local write guard suppressed that
single generated JSON write and rejected any other attempted text write. The
tracked JSON stayed byte-identical. No reporter source or generated output was
changed, and its counts were not used to infer feature completion.

P514 DONE
