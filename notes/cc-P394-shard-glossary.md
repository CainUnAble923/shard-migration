# P394: Shattered Legacy glossary draft

October 22, 2026. Unattended Codex lane, Verite tower. Documentation only.

## Scope

Work copies are `D:/UO/golems/Verite-tower/ShatteredLegacy` and `D:/UO/golems/Verite-tower/shard-migration`. Read both root AGENTS.md files first. Read the direction decision and task-list context, then inventoried the wiki-drafts tree recursively, including its DokuWiki `pages/` subtree, and the feature queue. Consulted the cited CC notes and the canonical customization files for terminology. Historical operational instructions in source notes are evidence, not authorization to execute them.

Deliverable: `notes/wiki-drafts/glossary.md`. It defines shard terms alphabetically, references the relevant wiki draft or topic page, distinguishes plans from built behavior, and retains contradictions without deciding them. Ordinary UO terms are included only where shard behavior or naming needs explanation.

## Boundaries and verification limits

No code, tests, configuration, saves, services, or world state are changed. No Haven connection, deployment, Docker build, commit, merge, push, or branch switch. No `docs/` writes or `server/uo/` reads. PowerShell commands run under Windows PowerShell 5.1 (observed version 5.1.26100.9444). `rg` is unavailable, so searches use Python and PowerShell. No new tests are required for this docs-only prompt; validation uses editorial and repository checks.

Source inspection establishes meanings and built paths, not running-shard availability or settings. The draft will not claim a source-defined feature is deployed. Hidden-achievement triggers, names, keepsakes, and exploit details are excluded from the player page.

## Outcome

Created an alphabetical glossary with 338 entries, counted from its table rows; the full term list is the glossary itself. Every definition is one or two sentences and every row supplies a topic page reference. Letter tables keep the alphabetical index readable. The page ends with Sources and Contradictions.

Confirmed guild identities and skill ownership, the graduation loop and empty reset hook, Young duration, recipe bands, box rarity names, evo gates, companion groundwork, mule tiers/modules, and Register/accessory terminology against canonical source. Added the main dungeon areas and starter materials, without turning the glossary into a creature catalog or publishing hidden discovery details.

Preserved the recorded disagreements about loops, retention, reserve, Young, pets versus companions, League milestones, guild identity/membership, work systems, Renown, recipes, materials, essences, box behavior, and placement. No decision or code was changed to reconcile them.

## Canonical source evidence

References below are file:line anchors in this prompt's canonical ShatteredLegacy work copy. Related functions and tables were inspected for the summarized meanings. Historical notes are not treated as proof of deployment.

| Glossary scope | Current source evidence | Meaning and limit |
|---|---|---|
| Guild names and joining | `server/customizations/ClusterFGuildSystem.cs:314` | Character membership, free joining, and the separate Apprentice task. |
| Skill ownership | `server/customizations/ClusterFGuildStarterPath.cs:46` | The guild skill table includes all current owners and the Alembic reassignment. |
| Citizen ladder | `server/customizations/ClusterFLeagueRanks.cs:43` | Metal-named ranks; generation excludes Dawnstone; milestone story trials remain waived while unbuilt. |
| Metal bonuses | `server/customizations/ResourceInfo.cs:277` | Extended material names and effects, including Frost's negative fire modifier. |
| Renown balances | `server/customizations/ClusterFAccountData.cs:653` | Qualifying Renown feeds lifetime totals; spending does not reduce them. |
| League Register | `server/customizations/LeagueRegister/LeagueRegister.cs:167` | Character ownership, rank-gated services, binding and free unbinding. |
| Combined Logbook and Field Satchel | `server/customizations/LeagueRegister/LeagueConsolidation.cs:24` | Consolidation retains the underlying discovery records and satchel rules. |
| Repair deeds and kits | `server/customizations/LeagueRegister/LeagueRepair.cs:31` | Repairs durability; guild tool use restoration remains separate. |
| Accessory slots | `server/customizations/Accessories/ClusterFAccessories.cs:32` | Additional jewelry slots; loop slots disabled by default. Hidden triggers are excluded. |
| Creature levels and Appraisal | `server/customizations/ClusterFCreatureLevels.cs:13` | Creature difficulty and temporary player strength are separate from future XP levels. |
| Young | `server/customizations/ClusterFYoungPlayer.cs:35` | 336 hours of account play; skills and graduation do not remove it. |
| Real loops and unfinished reset | `server/customizations/Tutorial/ClusterFLoops.cs:40` | The empty reset hook leaves skills, level, stats and XP unchanged. |
| Graduation and remedial | `server/customizations/Tutorial/ClusterFTutorial.cs:216` | Core completion, normal rewards, and the separate provisional skip behavior. |
| Recruiter Rook | `server/customizations/Tutorial/TutorialRecruiter.cs:30` | Recruiter and tutorial contact, separate from Elara Voss. |
| Farmhand Wren Tallow | `server/customizations/Tutorial/TutorialFarm.cs:469` | Farm pet choice and pest/heal lesson, with placement unverified. |
| Den lookout Wren | `server/customizations/ThievesDenLookout.cs:33` | A distinct NPC from Wren Tallow. |
| Craft bands | `server/customizations/Engines/Craft/ClusterFRecipeTable.cs:41` | The actual nine-band default table, rather than an invented tier list. |
| Merged books and exemptions | `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:204` | Small bands merge forward; spell scrolls, Cartography and whole-craft books use distinct rules. |
| Metal tiers | `server/customizations/ClusterFMetalTiers.cs:20` | Post-Valorite metals and starter Dawnstone are different sets. |
| Wood tiers | `server/customizations/ClusterFWoodTiers.cs:19` | Crafting ladder and gain ceilings are separate from harvesting requirements. |
| Wood bonuses | `server/customizations/ClusterFWoodBonuses.cs:76` | Normal and exceptional addition tables; wooden shields use defensive rows. |
| Exceptional materials | `server/customizations/ClusterFExceptionalMaterial.cs:15` | Positive material bonuses scale; penalties and extended wood exceptions remain distinct. |
| Arms Lore | `server/customizations/ClusterFArmsLore.cs:62` | Reduced wear, exceptional work, repair support and field maintenance. |
| Rare Self Repair | `server/customizations/ClusterFRareSelfRepair.cs:40` | Rare high-end loot roll; ordinary random/runic rolls removed; fixed named values retained. |
| Formularies and intensities | `server/customizations/Imbuing/ImbuingTable.cs:193` | Named book ladder and Basic/Refined/Full/Overcharged knowledge. |
| Formula knowledge | `server/customizations/Imbuing/ClusterFImbueKnowledge.cs:122` | Account knowledge is separate from essence mastery and guild standing. |
| Essence mastery and recovery | `server/customizations/ArtificersImbueGump.cs:1078` | Mastery check is separate from learned tier; extraction and full disenchant differ. |
| Imbuing sites | `server/customizations/Imbuing/ImbueSites.cs:68` | Toolkit, mule and real-forge caps; advertised mule property sockets remain unfinished. |
| Custom craft properties | `server/customizations/Imbuing/ImbuingTable.cs:247` | Bountiful, Mastercraft, Prospector and Butcher's Eye have distinct effects. |
| Box rarities | `server/customizations/LootBoxes/ClusterFLootTable.cs:74` | Common through Celestial; resource themes use separate material labels. |
| Box themes and contents | `server/customizations/LootBoxes/LootBoxRoller.cs:21` | Named themes, Artisan craft-dependent naming, and the Tamer placeholder. |
| Fragments | `server/customizations/LootBoxes/LootBoxItems.cs:378` | Item and tooltip exist; no scroll combination is implied. |
| Fragment combination limit | `server/customizations/LootBoxes/ClusterFLootBoxes.cs:18` | Current hook keeps fragments and creates no scroll. |
| Fanfare | `server/customizations/LootBoxes/ClusterFFanfare.cs:32` | Minor/Major/Capstone audiences and mute limits. |
| Evo lines and choices | `server/customizations/Mobiles/Evo/EvoPetData.cs:93` | Four lines, body and hue choices, pending forms, XP and Bond Trial gates. |
| Owner-loop disconnect | `server/customizations/Mobiles/Evo/EvoPet.cs:28` | The pet's owner-loop source still defaults to zero despite graduation's real count. |
| Humanoid groundwork | `server/customizations/Companions/BaseCompanion.cs:35` | Separate rank and loop fields; player hiring and promotion remain planned. |
| Companion paths | `server/customizations/Companions/CompanionSettings.cs:23` | Blade, Bow, Arcane, Support and Rogue; acquisition and class development remain planned. |
| Mule upgrades and bloodlines | `server/customizations/Mobiles/Mule/MuleData.cs:56` | Compact through Celestial upgrades; bloodline traits are separate. |
| Mule modules | `server/customizations/Mobiles/Mule/MuleModuleData.cs:57` | Working and partial effects are explicitly distinguished in the catalog. |
| Chest mimic | `server/customizations/Mobiles/Normal/ChestMimic.cs:273` | Monster built; dungeon-chest springing, taming, PetMimic handoff and placement remain planned. |
| Wearable PetMimic | `server/customizations/PetMimic.cs:456` | An Item, initially on the Talisman layer, separate from a tameable animal or humanoid companion. |
| Starter materials | `server/customizations/ClusterFStarterResources.cs:52` | Burrowhide, Dawnstone, Rootwood and cosmetic Gloomsilk. |
| Dungeon harvesting | `server/customizations/Engines/Harvest/BurrowsRegionHarvest.cs:23` | Region-only starter resources are separate from extended ladders. |
| Vault and crawlway | `server/customizations/Regions/RootdeepVault.cs:91` | Trainee access, Overdraft credit and one-way exit; activities separate from required core. |
| Dungeon layout names | `server/customizations/ClusterFRootdeepSeeder.cs:121` | Warren, Tangle, Dawnseam, Gloom, Stacks, landing and boss names; not proof of placement. |
| Spiders and Gloomsilk | `server/customizations/Mobiles/Burrows/GloomCreatures.cs:38` | Gloom spider loot; the Gloom Queen is defined in the same file. |
| Custodian points | `server/customizations/ClusterFCustodianSystem.cs:185` | Lifetime Clean Up points determine standing; Civic Tokens are retired. |
| Ore satchel upgrade | `server/customizations/ReinforcedOreSatchel.cs:36` | Further labels also checked at SurveyorsSatchel.cs:39, DeepdelversSatchel.cs:39 and MasterExpeditionSatchel.cs:41. |
| Levelable gear | `server/customizations/LevelGear/ClusterFLevelGear.cs:39` | Item leveling is built, but normal acquisition of a Smith's Seal remains planned. |

## Reading inventory

Read the wiki-draft Markdown pages and the DokuWiki subtree, including hubs and the sidebar. Loaded the cited implementation notes and consulted relevant definitions, decisions, source ledgers, and verification limits; larger historical build notes were read by pertinent sections rather than re-audited as build work. The context-note list also includes adjacent numbered prerequisites and the named P381/P391 work notes and reviews.

Read-only governing context: both root AGENTS.md files, docs/direction-decision.md, docs/tasks.md, and docs/feature-queue.md. Also consulted notes/f12-decisions-2026-10-05.md and the relevant model/retention sections of notes/f12-levels-loops-caps.md.

### Preexisting wiki artifacts (33)

- [wiki-drafts/achievements-and-loot-boxes.md](wiki-drafts/achievements-and-loot-boxes.md)
- [wiki-drafts/artificers-order.md](wiki-drafts/artificers-order.md)
- [wiki-drafts/companions-and-evo-pets.md](wiki-drafts/companions-and-evo-pets.md)
- [wiki-drafts/crafting-changes.md](wiki-drafts/crafting-changes.md)
- [wiki-drafts/gathering-guilds.md](wiki-drafts/gathering-guilds.md)
- [wiki-drafts/league.md](wiki-drafts/league.md)
- [wiki-drafts/levels-loops-and-scrolls.md](wiki-drafts/levels-loops-and-scrolls.md)
- [wiki-drafts/new-haven-start.md](wiki-drafts/new-haven-start.md)
- [wiki-drafts/order-of-the-alembic.md](wiki-drafts/order-of-the-alembic.md)
- [wiki-drafts/pages/sidebar.txt](wiki-drafts/pages/sidebar.txt)
- [wiki-drafts/pages/uo/drafts/levelable_gear.txt](wiki-drafts/pages/uo/drafts/levelable_gear.txt)
- [wiki-drafts/pages/uo/drafts/start.txt](wiki-drafts/pages/uo/drafts/start.txt)
- [wiki-drafts/pages/uo/drafts/tutorial.txt](wiki-drafts/pages/uo/drafts/tutorial.txt)
- [wiki-drafts/pages/uo/guides/league.txt](wiki-drafts/pages/uo/guides/league.txt)
- [wiki-drafts/pages/uo/guides/start.txt](wiki-drafts/pages/uo/guides/start.txt)
- [wiki-drafts/pages/uo/professions/bulk_orders.txt](wiki-drafts/pages/uo/professions/bulk_orders.txt)
- [wiki-drafts/pages/uo/professions/climbing_boots.txt](wiki-drafts/pages/uo/professions/climbing_boots.txt)
- [wiki-drafts/pages/uo/professions/start.txt](wiki-drafts/pages/uo/professions/start.txt)
- [wiki-drafts/pages/uo/professions/traps.txt](wiki-drafts/pages/uo/professions/traps.txt)
- [wiki-drafts/pages/uo/start.txt](wiki-drafts/pages/uo/start.txt)
- [wiki-drafts/pages/uo/systems/accessories.txt](wiki-drafts/pages/uo/systems/accessories.txt)
- [wiki-drafts/pages/uo/systems/achievements.txt](wiki-drafts/pages/uo/systems/achievements.txt)
- [wiki-drafts/pages/uo/systems/creature_levels.txt](wiki-drafts/pages/uo/systems/creature_levels.txt)
- [wiki-drafts/pages/uo/systems/league.txt](wiki-drafts/pages/uo/systems/league.txt)
- [wiki-drafts/pages/uo/systems/league_register.txt](wiki-drafts/pages/uo/systems/league_register.txt)
- [wiki-drafts/pages/uo/systems/league_shop.txt](wiki-drafts/pages/uo/systems/league_shop.txt)
- [wiki-drafts/pages/uo/systems/loot_boxes.txt](wiki-drafts/pages/uo/systems/loot_boxes.txt)
- [wiki-drafts/pages/uo/systems/start.txt](wiki-drafts/pages/uo/systems/start.txt)
- [wiki-drafts/pages/uo/world/seasonal.txt](wiki-drafts/pages/uo/world/seasonal.txt)
- [wiki-drafts/pages/uo/world/start.txt](wiki-drafts/pages/uo/world/start.txt)
- [wiki-drafts/rangers-custodians-healers.md](wiki-drafts/rangers-custodians-healers.md)
- [wiki-drafts/society-of-smiths.md](wiki-drafts/society-of-smiths.md)
- [wiki-drafts/thieves-den.md](wiki-drafts/thieves-den.md)

### Implementation and guide context notes (130)

- [cc-P13-grove-tracking.md](cc-P13-grove-tracking.md)
- [cc-P14-newhaven-guild-mapping.md](cc-P14-newhaven-guild-mapping.md)
- [cc-P15-guild-starter-path.md](cc-P15-guild-starter-path.md)
- [cc-P16-mine-camp-tents.md](cc-P16-mine-camp-tents.md)
- [cc-P17-playtest-bugs-1.md](cc-P17-playtest-bugs-1.md)
- [cc-P18-reset-stone-young-craftx.md](cc-P18-reset-stone-young-craftx.md)
- [cc-P20-skill-scaling-research.md](cc-P20-skill-scaling-research.md)
- [cc-P22-small-features-1.md](cc-P22-small-features-1.md)
- [cc-P23-live-defect-sweep.md](cc-P23-live-defect-sweep.md)
- [cc-P24-new-haven-dungeon-research.md](cc-P24-new-haven-dungeon-research.md)
- [cc-P26-animated-runestone.md](cc-P26-animated-runestone.md)
- [cc-P27-defect-batch-1.md](cc-P27-defect-batch-1.md)
- [cc-P30-modernuo-upgrade-research.md](cc-P30-modernuo-upgrade-research.md)
- [cc-P32-spawner-importer-bods-self-repair.md](cc-P32-spawner-importer-bods-self-repair.md)
- [cc-P33-clean-up-britannia.md](cc-P33-clean-up-britannia.md)
- [cc-P34-winter-decor.md](cc-P34-winter-decor.md)
- [cc-P35-clean-machine-test.md](cc-P35-clean-machine-test.md)
- [cc-P36-dungeon-build-1.md](cc-P36-dungeon-build-1.md)
- [cc-P37-upgrade-prep.md](cc-P37-upgrade-prep.md)
- [cc-P38-engine-upgrade.md](cc-P38-engine-upgrade.md)
- [cc-P39-test-shard-cutover.md](cc-P39-test-shard-cutover.md)
- [cc-P41-companions-research.md](cc-P41-companions-research.md)
- [cc-P42-defect-batch-3.md](cc-P42-defect-batch-3.md)
- [cc-P43-stop-timeout-and-cutover.md](cc-P43-stop-timeout-and-cutover.md)
- [cc-P44-wait-for-ea-patch.md](cc-P44-wait-for-ea-patch.md)
- [cc-P45-companion-probes.md](cc-P45-companion-probes.md)
- [cc-P46-smith-orders-2.md](cc-P46-smith-orders-2.md)
- [cc-P47-league-research.md](cc-P47-league-research.md)
- [cc-P48-league-batch-1.md](cc-P48-league-batch-1.md)
- [cc-P49-dungeon-chests-research.md](cc-P49-dungeon-chests-research.md)
- [cc-P50-chest-mimic-monster.md](cc-P50-chest-mimic-monster.md)
- [cc-P51-staff-hub-and-raptor-pack.md](cc-P51-staff-hub-and-raptor-pack.md)
- [cc-P52-bug-batch-4.md](cc-P52-bug-batch-4.md)
- [cc-P53-two-hundred-cap.md](cc-P53-two-hundred-cap.md)
- [cc-P54-f12-xp-and-gain-paths.md](cc-P54-f12-xp-and-gain-paths.md)
- [cc-P55-bug-batch-5.md](cc-P55-bug-batch-5.md)
- [cc-P56-smith-economy-and-labels.md](cc-P56-smith-economy-and-labels.md)
- [cc-P57-batch-6.md](cc-P57-batch-6.md)
- [cc-P59-evo-pet-body-sheet.md](cc-P59-evo-pet-body-sheet.md)
- [cc-P61-batch-7.md](cc-P61-batch-7.md)
- [cc-P62-kitsune-walk-test.md](cc-P62-kitsune-walk-test.md)
- [cc-P65-evo-pets-framework.md](cc-P65-evo-pets-framework.md)
- [cc-P66-clamps-and-hook-g.md](cc-P66-clamps-and-hook-g.md)
- [cc-P67-craft-ceilings.md](cc-P67-craft-ceilings.md)
- [cc-P69-mule-core.md](cc-P69-mule-core.md)
- [cc-P70-mule-modules.md](cc-P70-mule-modules.md)
- [cc-P71-high-skill-effect-scaling.md](cc-P71-high-skill-effect-scaling.md)
- [cc-P72-level-items-research.md](cc-P72-level-items-research.md)
- [cc-P75-league-rewards-rethink.md](cc-P75-league-rewards-rethink.md)
- [cc-P77-alembic-guild.md](cc-P77-alembic-guild.md)
- [cc-P78-recipe-gating.md](cc-P78-recipe-gating.md)
- [cc-P79-loot-boxes-fanfare.md](cc-P79-loot-boxes-fanfare.md)
- [cc-P80-new-player-tutorial.md](cc-P80-new-player-tutorial.md)
- [cc-P82-artificers-imbuing.md](cc-P82-artificers-imbuing.md)
- [cc-P103-tazuo-client-command.md](cc-P103-tazuo-client-command.md)
- [cc-P118-port-bulk-orders.md](cc-P118-port-bulk-orders.md)
- [cc-P120-port-pet-training.md](cc-P120-port-pet-training.md)
- [cc-P121-pet-ability-core.md](cc-P121-pet-ability-core.md)
- [cc-P122-port-bulk-orders-core.md](cc-P122-port-bulk-orders-core.md)
- [cc-P123-port-bulk-orders-crafts.md](cc-P123-port-bulk-orders-crafts.md)
- [cc-P128-port-consumables-crafting-gaps.md](cc-P128-port-consumables-crafting-gaps.md)
- [cc-P129-port-creatures-part2.md](cc-P129-port-creatures-part2.md)
- [cc-P130-pet-training.md](cc-P130-pet-training.md)
- [cc-P137-usable-ankhs-and-playtest-fixes.md](cc-P137-usable-ankhs-and-playtest-fixes.md)
- [cc-P141-rootdeep-burrows.md](cc-P141-rootdeep-burrows.md)
- [cc-P142-monster-stealing-shard-rules.md](cc-P142-monster-stealing-shard-rules.md)
- [cc-P146-playtest-decisions-inbox.md](cc-P146-playtest-decisions-inbox.md)
- [cc-P147-achievements-button.md](cc-P147-achievements-button.md)
- [cc-P150-requisitions-and-leads.md](cc-P150-requisitions-and-leads.md)
- [cc-P151-guild-halls-survey.md](cc-P151-guild-halls-survey.md)
- [cc-P165-achievements-button-fix.md](cc-P165-achievements-button-fix.md)
- [cc-P170-smith-teaching-orders-fix.md](cc-P170-smith-teaching-orders-fix.md)
- [cc-P172-pet-gain-speed.md](cc-P172-pet-gain-speed.md)
- [cc-P173-imbue-all-slayers.md](cc-P173-imbue-all-slayers.md)
- [cc-P175-cont-clean-up-britannia-finish.md](cc-P175-cont-clean-up-britannia-finish.md)
- [cc-P176-cont-artificers-unravel-container.md](cc-P176-cont-artificers-unravel-container.md)
- [cc-P177-guild-menus-template-mockups.md](cc-P177-guild-menus-template-mockups.md)
- [cc-P179-league-design-pass.md](cc-P179-league-design-pass.md)
- [cc-P188-cont-rootdeep-goes-in.md](cc-P188-cont-rootdeep-goes-in.md)
- [cc-P195-port-exodus-encounter.md](cc-P195-port-exodus-encounter.md)
- [cc-P199-port-base-items-remainder.md](cc-P199-port-base-items-remainder.md)
- [cc-P201-deployable-traps-design.md](cc-P201-deployable-traps-design.md)
- [cc-P203-cont-fixup-requisitions-and-leads.md](cc-P203-cont-fixup-requisitions-and-leads.md)
- [cc-P217-crystal-wiki-catch-up.md](cc-P217-crystal-wiki-catch-up.md)
- [cc-P218-crystal-mage-crafter-scripts.md](cc-P218-crystal-mage-crafter-scripts.md)
- [cc-P226-arms-lore-matters.md](cc-P226-arms-lore-matters.md)
- [cc-P227-extended-wood-bonuses.md](cc-P227-extended-wood-bonuses.md)
- [cc-P228-exceptional-material-gap.md](cc-P228-exceptional-material-gap.md)
- [cc-P229-league-reward-shop.md](cc-P229-league-reward-shop.md)
- [cc-P231-osi-joke-achievements.md](cc-P231-osi-joke-achievements.md)
- [cc-P234-dismount-sources-design.md](cc-P234-dismount-sources-design.md)
- [cc-P235-work-order-numbers-pass.md](cc-P235-work-order-numbers-pass.md)
- [cc-P236-satchel-icons-ship.md](cc-P236-satchel-icons-ship.md)
- [cc-P238-climbing-boots.md](cc-P238-climbing-boots.md)
- [cc-P239-creature-levels-appraisal.md](cc-P239-creature-levels-appraisal.md)
- [cc-P241-achievement-category-icons.md](cc-P241-achievement-category-icons.md)
- [cc-P243-league-hall-decor-rewards.md](cc-P243-league-hall-decor-rewards.md)
- [cc-P245-cont-fixup-port-base-items-remainder.md](cc-P245-cont-fixup-port-base-items-remainder.md)
- [cc-P260-herbalism-research.md](cc-P260-herbalism-research.md)
- [cc-P261-levelable-gear-build.md](cc-P261-levelable-gear-build.md)
- [cc-P262-accessory-slots.md](cc-P262-accessory-slots.md)
- [cc-P263-noted-by-the-system-achievements.md](cc-P263-noted-by-the-system-achievements.md)
- [cc-P265-guild-hall-decor-packs.md](cc-P265-guild-hall-decor-packs.md)
- [cc-P275-deployable-traps-build.md](cc-P275-deployable-traps-build.md)
- [cc-P276-tutorial-farm-build.md](cc-P276-tutorial-farm-build.md)
- [cc-P280-league-register-build.md](cc-P280-league-register-build.md)
- [cc-P282-f12-numbers-and-level-gates.md](cc-P282-f12-numbers-and-level-gates.md)
- [cc-P283-skill-gain-paths-research.md](cc-P283-skill-gain-paths-research.md)
- [cc-P285-cont-fixup-levelable-gear-build.md](cc-P285-cont-fixup-levelable-gear-build.md)
- [cc-P286-crystal-mage-crafter-docs-and-tests.md](cc-P286-crystal-mage-crafter-docs-and-tests.md)
- [cc-P361-cont-fixup-noted-by-the-system-achievements.md](cc-P361-cont-fixup-noted-by-the-system-achievements.md)
- [cc-P366-cont-fixup-cont-loot-box-flying-loot.md](cc-P366-cont-fixup-cont-loot-box-flying-loot.md)
- [cc-P369-cont-fixup-companions-b1-base-and-record.md](cc-P369-cont-fixup-companions-b1-base-and-record.md)
- [cc-P371-graduation-is-the-first-loop.md](cc-P371-graduation-is-the-first-loop.md)
- [cc-P376-league-decisions.md](cc-P376-league-decisions.md)
- [cc-P377-crystal-wiki-catch-up-2.md](cc-P377-crystal-wiki-catch-up-2.md)
- [cc-P378-playtest-plans-10-21.md](cc-P378-playtest-plans-10-21.md)
- [cc-P381-guild-guide-society-of-smiths-codex-review.md](cc-P381-guild-guide-society-of-smiths-codex-review.md)
- [cc-P381-guild-guide-society-of-smiths.md](cc-P381-guild-guide-society-of-smiths.md)
- [cc-P382-guild-guide-order-of-the-alembic.md](cc-P382-guild-guide-order-of-the-alembic.md)
- [cc-P383-guild-guide-artificers-order.md](cc-P383-guild-guide-artificers-order.md)
- [cc-P384-guild-guide-thieves-den.md](cc-P384-guild-guide-thieves-den.md)
- [cc-P385-guide-gathering-guilds.md](cc-P385-guide-gathering-guilds.md)
- [cc-P386-guide-rangers-custodians-healers.md](cc-P386-guide-rangers-custodians-healers.md)
- [cc-P387-guide-achievements-and-loot-boxes.md](cc-P387-guide-achievements-and-loot-boxes.md)
- [cc-P388-guide-levels-loops-and-scrolls.md](cc-P388-guide-levels-loops-and-scrolls.md)
- [cc-P389-guide-companions-and-evo-pets.md](cc-P389-guide-companions-and-evo-pets.md)
- [cc-P390-guide-crafting-changes.md](cc-P390-guide-crafting-changes.md)
- [cc-P391-guide-new-haven-start-codex-review.md](cc-P391-guide-new-haven-start-codex-review.md)
- [cc-P391-guide-new-haven-start.md](cc-P391-guide-new-haven-start.md)

## Verification and remaining limits

- Editorial checks counted 338 unique term rows and confirmed case-insensitive alphabetical order, valid three-column rows, one or two sentences per definition, defined reference links, and existing local link targets. No em dashes or code file:line citations occur on the player page. Its final sections are Sources and Contradictions.
- Numeric gameplay definitions are limited to source-backed crafting bands, ordinary box tier numbers, the first loop, the planned above-100 scroll gate, and the 336-hour Young duration. The glossary adds no drop chances, guessed prices, XP pacing, or rank threshold tables.
- All eighteen current guild names have entries (Custodians is indexed without the leading article). Spell scrolls, recipe scrolls, pattern books, formularies, mule schematics, current Power Scrolls, planned loop scrolls, and fragments have distinct definitions. So do AP/Renown/Lifetime Renown, guild standing/currency, player/creature/item progress, evo stages and companion ranks.
- Manual content review excluded staff commands, hidden-achievement names and triggers, named secret keepsakes, and exploit details. The general Mischief, Dented Box, and accessory descriptions disclose no unlock method.
- A useful source limit: ChestMimic is still not tameable and does not implement its planned PetMimic handoff. Both entries preserve planned status rather than treating F-32 as built.
- The Rootdeep page ID comes from the existing DokuWiki drafts hub. Its body is absent from this wiki-draft subtree. The glossary explicitly identifies the destination, but its current remote text and exact coverage remain unverified. No connection to the hosted wiki was made.
- Running-shard settings, NPC placement, encounters, and player access were not verified. Boss-box awards remain reported defective, and the box-versus-exceptional-gear comparison remains unverified. The farm-placement disagreement is retained.
- Lane tests: none, as specified. No tests or gates were added, so no new red/green test obligation was introduced. No build was needed for these prose files.
- Ran the progress reporter in dry-run mode with SL_SHARD and SL_MIGRATE set to these work copies. Its build() function still attempts to write tools/progress.json before the dry-run early return; a process-local interception suppressed that exact write, keeping this task to its two requested Markdown files. The read-only report completed successfully. No progress numbers are promoted as glossary evidence.
- Repository checks show a clean code tree and only the two requested untracked Markdown deliverables in the notes tree. Final untracked-file whitespace and size checks are recorded below before the completion marker.

Final checks: git diff --no-index --check passed for each new file; both have zero trailing-whitespace lines and are below 5 MB. All local links in both deliverables resolve. Code repository is clean; notes repository contains only these two requested new files. The stop-request file was absent at completion. No required task work remains.

P394 DONE
