# Feature queue audit, October 22, 2026

This is a source review of `docs/feature-queue.md`, not a queue edit. Each F-number
appears once below, including dropped F-2. Repeated batch rows are part of the same
entry. Queue status describes what the queue says, including its older handoff.

Built means implementation exists in this checkout. It does not mean placed in a
world, published in a player package, deployed, or verified in a client today.
Partly built names the remaining work. Not started refers to the requested
implementation; research and decisions can already exist. Future work is marked
`(planned)`.

File references use these roots:

- `C/`: `ShatteredLegacy/server/customizations/`.
- `P/`: `ShatteredLegacy/server/patches/`.
- `T/`: `ShatteredLegacy/server/tests/`.
- `K/`: `ShatteredLegacy/`, for client and package files.
- `U/`: `D:/UO/ModernUO-pinned/Projects/UOContent/`.
- `N/`: this repository's `notes/`.
- `Q:line`: the source entry in `docs/feature-queue.md`.

Code HEAD was `b240bb4d6e47d72ab6be6aafc202b6b28833a7c1`; notes HEAD was
`e3d2a0a060e36215a2c20a19d891ae30c023f806`. The read-only upstream checkout is
`d4531cd94b739613155225c234900de9f47d2c88`.

## Queue entries

| Entry | Queue status | Status shown by the code | File:line evidence | Building prompt, if known |
|---|---|---|---|---|
| F-1: Craft X through failures | Open; batched P18 (`Q:156`) | Built. Item and attempt modes, exceptional-only runs, limits, reject routing, and stop summaries exist. | `C/ClusterFCraftRun.cs:84`, `C/ClusterFCraftRun.cs:138`, `C/ClusterFCraftRejects.cs:27`, `T/Engines/Craft/MakeXRepeatVerification.cs:163` | P18, following P17's repeat work; P33 connected the trash bag. |
| F-2: Diminishing Custodian token returns | Dropped in favor of F-3 (`Q:3586`) | Not started, as decided. Cleanup now uses Clean Up points; Civic Tokens are retired. No diminishing-return feature is needed by this dropped entry. | `C/ClusterFCustodianSystem.cs:156`, `C/ClusterFCustodianSystem.cs:176`, `C/ClusterFCustodianSystem.cs:214` | Dropped; P33 built the replacement. |
| F-3: Custodians folded into Clean Up Britannia | Open; batched P33; decisions settled (`Q:214`) | Built. Character points, lifetime standing, cleanup valuation, owned trash bags, and one store exist. Both NPCs use that store. | `C/ClusterFCustodianSystem.cs:176`, `C/TrashBag.cs:76`, `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:84`, `T/Services/CleanUpBritanniaStoreVerification.cs:210` | P33; P175 finished reward reachability. |
| F-4: One character per account | Decided; not scheduled; staff and test exemptions (`Q:343`) | Not started. Creation still checks the account's upstream limit. The single-character rule and exemptions are (planned). | `C/CharacterCreation.cs:161`, `U/Accounting/Account.cs:461` | None found. |
| F-5: Young status by time played | Open; batched P18 (`Q:363`) | Built. Duration is account play time, the skill cutoff is removed, and voluntary renunciation remains. The later Young-clock reset is also present. | `C/ClusterFYoungPlayer.cs:35`, `C/ClusterFYoungPlayer.cs:41`, `P/PlayerMobile-young-time-only.patch:1`, `T/Misc/YoungPlayerVerification.cs:109` | P18; P192 added the restartable clock; P371 preserves Young at graduation. |
| F-6: World-map fog | Server half present; client half needs scoping; Cartography additions approved (`Q:400`) | Partly built. Server exploration packets and the TazUO fog overlay exist. Trading explored maps, treasure-map reveals, walked-only percentage achievements, and exploration Cartography gains remain (planned). | `C/ClusterFExplorationManager.cs:51`, `C/ClusterFExplorationManager.cs:96`, `K/client/patches/0004-world-map-fog-of-war.patch:121`, `C/Engines/Craft/ClusterFRecipeRewards.cs:136` | P240, P352, P357 built the client half. Original server tracking predates those prompts. |
| F-7: Player account reset | Open; batched P18; per-character guild data decided (`Q:461`) | Built. The stone opens the shared self-reset path; guild data and exploration can be cleared. Character guild records are separate. | `C/ClusterFResetStone.cs:113`, `C/ClusterFDevTools.cs:79`, `C/ClusterFDevTools.cs:153`, `T/Misc/ResetStoneVerification.cs:183` | P18. |
| F-8: Animated runestone and updater art route | Handoff says shipped P26; entry still says ready to batch (`Q:512`) | Built. Runestone variants, animation records, and local client-file overrides exist. Becoming the progression loop stone is (planned). | `C/ShatteredRunestone.cs:37`, `C/ShatteredRunestone.cs:83`, `K/player-package/payload/app/Build-UoOverrides.ps1:1` | P26. |
| F-9: Guild starter path | Open and batched P15; follow-ups P22 and P48 (`Q:578`) | Built for the starter path: tools, reward claims, directory directions, welcome page, and League signposting exist. Reissuing rewards on later progression loops remains tied to F-12 (planned). | `C/ClusterFGuildStarterPath.cs:290`, `C/ClusterFGuildStarterPath.cs:405`, `C/ClusterFGuildStarterPath.cs:588`, `C/ClusterFGuildStarterPath.cs:790`, `T/Misc/GuildStarterPathVerification.cs:294` | P15; P18 separated guild data; P22 and P48 added follow-ups; P77 added the Alembic. |
| F-10: Gargoyle starting-town choice | Decided; not scheduled (`Q:852`) | Not started. Royal City is declared as a location, but the available starting-city list returns New Haven only. The creation choice and second starter route are (planned). | `C/CharacterCreation.cs:119`, `C/CharacterCreation.cs:129`, `C/ClusterFGuildHallSeeder.cs:75` | None found for the choice. Existing Royal City services do not supply it. |
| F-11: Bank resources for guild services | Open; batched P22 (`Q:885`) | Built. A shared helper counts and consumes across pack and bank, including nested satchels, before charging. Guild services use it. | `C/GuildResources.cs:96`, `C/GuildResources.cs:184`, `C/GuildResources.cs:294`, `T/Misc/GuildResourcesVerification.cs:222` | P22. |
| F-12: Player levels, XP, loops, and progression | Research P20/P54; revised ladder; handoff says research on hold (`Q:926`) | Partly built. Flat skill caps, extended skill-gain paths, the loop ladder helper, and first-loop graduation exist. Actual player XP, leveling, level-based caps, skill resets, echo, Keeper/Breaker progression, and Legacy rewards are (planned). The reset integration body is empty. | `C/ClusterFSkillCaps.cs:11`, `C/ClusterFSkillGain.cs:20`, `C/Tutorial/ClusterFLoops.cs:25`, `C/Tutorial/ClusterFLoops.cs:31`, `C/Tutorial/ClusterFLoops.cs:40`, `T/Tutorial/GraduationLoopVerification.cs:71` | P53 flat cap; P66/P67/P71 skill work; P191 gain rates; P80 loop signals; P371 first-loop graduation. P282 is numbers research. |
| F-13: AP-gated League shop and titles | Ready to batch; starter list approved (`Q:1288`) | Partly built. The AP/Renown shop, selectable titles, and both entry points exist. Player-level gates and veteran XP bonuses await F-12 (planned). The decided larger veteran stat-cap reward is also (planned); no matching override was found. | `C/LeagueShop/LeagueShop.cs:37`, `T/Misc/LeagueShopVerification.cs:92`, `T/Misc/LeagueShopVerification.cs:166`, `C/ClusterFStatCaps.cs:105`, `U/Engines/Veteran Rewards/RewardSystem.cs:589` | P229; P243 added hall-decor rewards. |
| F-14: Creature levels and Appraisal | Ready to batch; creature details can precede player XP (`Q:1386`) | Partly built. Creature/NPC levels, relative con information, skill detail tiers, a stat card, and the package skill rename exist. Player comparisons use a provisional skill-based level. Real player-level comparisons, item requirements, and the creature-half unlock quest remain (planned). | `C/ClusterFCreatureLevels.cs:50`, `C/ClusterFCreatureLevels.cs:165`, `C/ClusterFCreatureLevels.cs:251`, `C/ClusterFCreatureLevels.cs:354`, `K/player-package/payload/app/Build-UoOverrides.ps1:64` | P239. |
| F-15: Version and login patch notes | Open; batched P22 (`Q:1466`) | Built. Version/changelog parsing, login notices, browser links, patch-history UI, and status-feed version exist. Wiki publication is an external step, unverified here. | `C/ShardVersion.cs:38`, `C/ShardVersion.cs:5`, `C/PatchHistoryGump.cs:1`, `K/scripts/Publish-PatchNotes.ps1:1` | P22; P26 started versioned notes; P64 added history. |
| F-16: Lower-tier pickaxe restoration prices | Ready to batch; batched P22 (`Q:1517`) | Built. The approved lower-tier prices are constants used by restoration. | `C/MinersCompactLiaisonGump.cs:43`, `C/MinersCompactLiaisonGump.cs:49`, `T/Misc/GuildResourcesVerification.cs:153` | P22. |
| F-17: Combine contained items into BODs | Ready to batch; batched P22 (`Q:1553`) | Built. Small and large deed gumps expose the container-combine route. Later craft BODs use the shared paths. | `P/BOD-combine-contained.patch:1`, `T/Misc/BODCombineContainedVerification.cs:1`, `T/Services/BulkOrders/BulkOrderCraftsVerification.cs:256` | P22; P123 added craft deeds. |
| F-18: BODs as skill training | Partly delivered by P42; tailoring, per-item checks, and beginner track left (`Q:1593`) | Partly built. Smith teaching selection and turn-in checks exist. Checks still follow small/large/material rules, not items divided by five. Tailoring retains the OSI points route. The shared guild-seal training system and beginner track remain (planned). | `P/SmallSmithBOD-teaching-orders.patch:1`, `C/ClusterFSmithBODSystem.cs:461`, `C/Services/BulkOrders/BulkOrderVendors.cs:158`, `T/Misc/SmithOrdersTeachVerification.cs:123` | P42 and follow-up smith fixes including P170. P118/P122/P123 ported OSI BOD behavior, not the remaining training design. |
| F-19: Larger banks | Ready to batch; P22 base; rank bonus described as stub (`Q:1641`) | Built. Base capacity and the later milestone-rank bonus are active in source. Client opening performance was not measured in this audit. | `C/ClusterFBankLimit.cs:26`, `C/ClusterFBankLimit.cs:40`, `C/ClusterFBankLimit.cs:46` | P22; P48 connected League milestone bonuses. |
| F-20: Other craft and gathering BODs | Ready after F-18; widened skill list decided (`Q:1680`) | Partly built. The added OSI craft deeds, issuers, and points framework exist. Cartography/Fishing training deeds and the proposed guild-currency/training rules for the broader skill list are (planned). Existing gathering and taming contracts remain separate. | `C/Services/BulkOrders/BulkOrderGivers.cs:34`, `C/Services/BulkOrders/BulkOrderVendors.cs:39`, `C/Services/BulkOrders/BulkOrderSystem.cs:81`, `C/ClusterFWorkOrderSystem.cs:49` | P118, P122, P123 built OSI BOD support. |
| F-21: New Haven community art | Ready after F-8; older download/check list (`Q:1739`) | Built for the selected community-art placements and records: carts, lighting, railings, beams, paintings, and camp art. The candidate list is not a promise that every downloaded pack ships. World placement and package publication are unverified here. | `C/ClusterFCommunityArtSeeder.cs:39`, `C/ClusterFCommunityArtSeeder.cs:93`, `C/ClusterFCommunityArtLayout.cs:1`, `T/Misc/CommunityArtVerification.cs:1` | P237; P236 shipped the separate satchel icons discussed in the handoff. |
| F-22: Winter decorations | Batched P34 (`Q:1804`) | Built. Seasonal dates, stock/community decor, and the later bank/calendar additions exist. Whether a world is configured to enable them is unverified here. | `C/ClusterFWinterDecorSeeder.cs:108`, `C/ClusterFWinterDecorSeeder.cs:227`, `C/WinterAdventCalendar.cs:1`, `T/Misc/WinterDecorVerification.cs:1` | P34; P266 expanded winter decor. |
| F-23: Paperdoll replacements | Approved for everyone; checks still pending (`Q:1877`) | Built in package sources. The normal body art and equipment overrides ship through the paperdoll route. A later client option controls body appearance. Current published package contents were not inspected. | `K/player-package/payload/app/Paperdoll-Bodies.ps1:5`, `K/player-package/payload/app/Paperdoll-Bodies.ps1:87`, `K/client/patches/0002-paperdoll-bodies-option.patch:1` | P81; P111 added the client option; P124 updated package delivery. |
| F-24: League jobs, hunts, dives, and citizen commissions | P47 research; P48 batch 1; remaining batches described (`Q:1918`) | Partly built. Signposts, metal ranks, promotion checks, milestone bonuses, hunt/cull creature tables, and first-encounter bestiary records exist. Promotion jobs and story trials remain waived. The shared contract board, job objectives, party jobs, non-member pay banking, and escrowed citizen commissions are (planned). Requisitions are a separate built board. | `C/ClusterFLeagueRanks.cs:163`, `C/ClusterFLeagueRanks.cs:182`, `C/ClusterFLeagueRanks.cs:275`, `C/ClusterFLeagueBestiary.cs:56`, `C/Requisitions/RequisitionSystem.cs:48` | P48 batch 1; P364 bestiary foundation. P150/P203 built requisitions, not the planned contract engine. |
| F-25: Bank BOD rewards and direct-fill large deeds | P42 partly delivered; follow-up includes payout choice, caps, and add-ons (`Q:2019`) | Partly built. Smith bank/cash/ask modes, direct large fills, and later OSI per-craft points banking exist. Smith caps remain fixed; rank growth, a distinct reduced direct-fill bonus, and the requested guild add-on stores remain (planned). | `C/ClusterFSmithBODPayout.cs:64`, `C/LargeBODItemFill.cs:28`, `C/ClusterFSmithBODSystem.cs:56`, `C/ClusterFSmithBODSystem.cs:477`, `C/Services/BulkOrders/BulkOrderSystem.cs:81`, `C/SmithSealCatalogGump.cs:44` | P42, P55, P57; P118/P122/P123 added OSI banking for the other crafts. |
| F-26: Arms Lore to 200 and new uses | Approved; base work ready; expose weakness/attunement later (`Q:2102`) | Partly built. Crafting bonuses, reduced wear, field maintenance, better smith repairs, and the gain path exist. Expose weakness and player-level gear attunement are (planned). | `C/ClusterFArmsLore.cs:52`, `C/ClusterFArmsLore.cs:65`, `C/ClusterFArmsLore.cs:103`, `C/ClusterFArmsLore.cs:147`, `T/Skills/ArmsLoreMattersVerification.cs:143` | P226 built the base work. |
| F-27: Very rare Self Repair | Batched P32 Part C (`Q:2174`) | Built. A separate high-end-source roll exists; ordinary random/runic production is patched. Fixed artifact properties remain separate. | `C/ClusterFRareSelfRepair.cs:40`, `C/ClusterFRareSelfRepair.cs:43`, `C/ClusterFRareSelfRepair.cs:76`, `P/BaseRunicTool-no-random-self-repair.patch:1`, `T/Items/RareSelfRepairVerification.cs:1` | P32. |
| F-28: Extended wood bonuses | Ready with/after P36 and F-29 (`Q:2208`) | Partly built. Weapon/shield tables, exceptional additions, and craft gates exist. Lower player-level requirements are stored in the table but have no effect until F-12 (planned). | `C/ClusterFWoodBonuses.cs:34`, `C/ClusterFWoodBonuses.cs:76`, `C/ClusterFWoodBonuses.cs:204`, `C/ClusterFWoodTiers.cs:19`, `T/Items/ExtendedWoodBonusesVerification.cs:209` | P227; P53/P57 supplied earlier tier work. |
| F-29: Exceptional material gap everywhere | Ready; normal unchanged, exceptional material bonuses multiplied (`Q:2286`) | Partly built against the blanket wording. Material accessors and OSI bow bonuses scale exceptional items. Extended-wood F-28 tables are deliberately excluded from that multiplier and keep their own exceptional additions. See Contradictions. | `C/ClusterFExceptionalMaterial.cs:23`, `C/ClusterFExceptionalMaterial.cs:41`, `C/ClusterFExceptionalMaterial.cs:68`, `C/ClusterFExceptionalMaterial.cs:113`, `T/Items/ExceptionalMaterialVerification.cs:278` | P228. |
| F-30: Staff Hub, including Events | First build P51; Events second batch ready (`Q:2329`) | Built. Tool/player/travel panels and saved spots exist. Events now has monster surges, wave timing, cleanup, gates, and participation prizes. No command instructions are reproduced here. | `C/StaffHub/StaffHubGump.cs:56`, `C/StaffHub/ClusterFSurge.cs:39`, `C/StaffHub/ClusterFSurge.cs:234`, `T/Misc/StaffHubEventsVerification.cs:176`, `T/Misc/StaffHubEventsVerification.cs:224` | P51; P230 built Events. |
| F-31: Raptor pack friends | Batched P51 after engine upgrade (`Q:2387`) | Built as an upstream patch, with friend lifecycle tests. | `P/Raptor-pack-friends.patch:1`, `T/Mobiles/Normal/RaptorPackFriendsVerification.cs:100`, `T/Mobiles/Normal/RaptorPackFriendsVerification.cs:192` | P51. |
| F-32: Dungeon chests and mimic pet source | P49 research done; P50 mimic; chest-system build ready (`Q:2408`) | Partly built. The stationary chest mimic, art, spring helper, and pet conversion exist. The ordinary dungeon-chest depth/loot/refill system and random mimic trigger remain (planned). No production caller of the spring helper was found. | `C/Mobiles/Normal/ChestMimic.cs:671`, `T/Mobiles/Normal/ChestMimicVerification.cs:59`, `T/Mobiles/Normal/ChestMimicVerification.cs:131`, `N/cc-P50-chest-mimic-monster.md:118` | P50 built the mimic. P49 is chest research. |
| F-33: Multi-guild work and mule upgrades | P47 research; mule core/modules described as unnumbered prompts (`Q:2513`) | Partly built. Mule acquisition, tiers, breeding, upgrades, and module loadouts exist. Shared multi-guild jobs and broader equipment reputation gates are (planned). Module data still marks unfinished gem, auto-sort/scavenger, bandaging, dismount, and property-socket effects. | `C/Mobiles/Mule/MuleErrand.cs:107`, `C/Mobiles/Mule/MuleModuleData.cs:57`, `C/Mobiles/Mule/MuleModuleData.cs:118`, `C/Mobiles/Mule/MuleModuleData.cs:123`, `C/Mobiles/Mule/MuleErrand.cs:37` | P69 core; P70 modules; P78 learned schematics; P82 portable imbuing integration. |
| F-34: Crafting bank-access item | Decided; placed with future League batches (`Q:2693`) | Partly built. The League Register has a bank summary page and F-11 supplies bank resource helpers. Per-guild crafting unlocks, range tiers, and ordinary-crafting integration are (planned). | `C/LeagueRegister/LeagueRegisterGump.cs:21`, `C/LeagueRegister/LeagueRegisterGump.cs:243`, `C/GuildResources.cs:159`, `N/cc-P280-league-register-build.md:145` | P280 built the Register base, not crafting access. |
| F-35: Tutorial story and evolution pets | Story/farm decisions; P59 art research; P65/P80 work named in handoff (`Q:2753`) | Partly built. Tutorial state, vision, station framework, farm pet/pest/heal lesson, evo framework, and graduation loop exist. Unimplemented stations still show previews. Full story lessons, progression integration, Bond Trial, role abilities, and pending fox/bird/kitsune stages are (planned). | `C/Tutorial/ClusterFTutorial.cs:122`, `C/Tutorial/TutorialStations.cs:176`, `C/Tutorial/TutorialFarm.cs:45`, `C/Mobiles/Evo/EvoPetData.cs:114`, `C/Mobiles/Evo/EvoPetData.cs:202`, `C/Tutorial/ClusterFLoops.cs:34` | P65, P80, P276, P371; P62/P138/P166 developed wearable art. |
| F-36: Climbing boots and mined-block ledger | Decided; costs/counts placeholders; purchase not batched in queue (`Q:3005`) | Built. Upgrade tiers, mining/block/rank gates, hops, stamina/cooldown, ledge memory, restoration, and logbook block tracking exist. Live mountain rendering is unverified here. | `C/ClusterFClimbing.cs:123`, `C/ClimbingBoots.cs:61`, `C/ClimbingBoots.cs:87`, `C/ClusterFMinedBlocks.cs:1`, `T/Misc/ClimbingBootsVerification.cs:1` | P238; P278 integration fix-up. |
| F-37: Move client commissions to the League | Ready after the League engine; tailoring next (`Q:3073`) | Not started for the move. Existing smith commissions still pay smith standing/currency directly. League deadlines, recurring-client progression, commission Renown, Infamy, and tailoring commissions are (planned). | `C/ClusterFSmithCommissions.cs:452`, `C/ClusterFSmithCommissions.cs:675`, `C/ClusterFSmithCommissions.cs:757`, `C/SmithCommissionGump.cs:1` | P46 improved existing smith commissions. No League move found. |
| F-38: Rolled gathering contracts and balancing | Needs numbers pass before batching (`Q:3119`) | Not started for rolled contracts. Definitions are still registered fixed work orders. Mule's first-Haul callback remains unassigned. P235 supplied a numbers proposal (planned), not an implementation. | `C/ClusterFWorkOrderSystem.cs:347`, `C/ClusterFWorkOrderSystem.cs:382`, `C/ClusterFWorkOrderSystem.cs:1991`, `C/Mobiles/Mule/MuleErrand.cs:37` | P235 research only. |
| F-39: More dismount sources | All ideas planned; source details open (`Q:3154`) | Not started. The mule dismount-resistance module is explicitly stubbed. The proposed monster, area, trap, and wildlife sources are (planned). | `C/Mobiles/Mule/MuleModuleData.cs:116`, `N/cc-P234-dismount-sources-design.md:9` | P234 design only; P70 supplied the module placeholder. |
| F-40: Achievement loot boxes | Phase-1 prompt still unnumbered; designed (`Q:3172`) | Partly built. Award/open/roll flow, achievement/boss/rank sources, and loop awards exist. Dungeon-clear tracking, actual player-level snapshots, and usable loop-scroll progression remain (planned). | `C/LootBoxes/ClusterFLootBoxes.cs:58`, `C/LootBoxes/ClusterFLootBoxes.cs:86`, `C/LootBoxes/ClusterFLootBoxes.cs:132`, `C/LootBoxes/ClusterFLootBoxes.cs:218`, `C/LootBoxes/ClusterFLootBoxes.cs:225` | P79; P371 connected the first real loop award. |
| F-41: Fanfare | Server phase 1, client voice/effects phase 2 (planned) (`Q:3198`) | Partly built overall; server phase 1 is built. Minor/major/capstone delivery, merging, and mute state exist. The custom voice hook has no implementation; future level/trial sources also await their systems (planned). | `C/LootBoxes/ClusterFFanfare.cs:32`, `C/LootBoxes/ClusterFFanfare.cs:49`, `C/LootBoxes/ClusterFFanfare.cs:76`, `C/LootBoxes/ClusterFFanfare.cs:91` | P79; later flying-loot presentation is separate. |
| F-42: Epic crafting | Explicitly planned; not designed (`Q:3210`) | Not started for crafting. Components can roll in boxes and recipe-source restrictions exist, but consuming epic recipes and the crafting progression are (planned). | `C/LootBoxes/LootBoxItems.cs:412`, `C/LootBoxes/LootBoxRoller.cs:458`, `C/Engines/Craft/ClusterFRecipeRewards.cs:103` | P79 components; P78 recipe-source framework. |
| F-43: Recipe-gated crafting and Alembic | Designed; unnumbered prompts; Imbuing excluded (`Q:3216`) | Partly built. Account learning, books/scrolls, menu filtering/hints, guild ownership/promotion rewards, and learned module schematics exist. Region-map learning has no exploration caller; custom/epic recipe content and unbuilt commission sources remain (planned). Imbuing received its separate implementation. | `C/Engines/Craft/ClusterFRecipeGate.cs:126`, `C/Engines/Craft/ClusterFRecipeStore.cs:68`, `C/Engines/Craft/ClusterFRecipeStore.cs:93`, `C/Engines/Craft/ClusterFRecipeRewards.cs:87`, `C/Engines/Craft/ClusterFRecipeRewards.cs:136` | P77 Alembic; P78 recipes; P82 separate Imbuing work. |
| F-44: Instanced inn room | Decided outline; room/rent rules open (`Q:3256`) | Not started. Housing is a tutorial station description, not an inn-room instance/rent/storage system. All room mechanics are (planned). | `C/Tutorial/TutorialStations.cs:145`, `C/Tutorial/ClusterFTutorial.cs:122` | None found. |
| F-45: Rootdeep bestiary and tutorial Vault | Ready for prompt numbering; depends on F-46 (`Q:3282`) | Built in source. Named creature families, registered bodies, tutorial loot, Vault access/exit behavior, and the later Rootdeep placement data exist. Live layout/client behavior is unverified here. | `C/Mobiles/Burrows/VaultCreatures.cs:1`, `C/Mobiles/Burrows/GloomCreatures.cs:1`, `C/Regions/RootdeepVault.cs:37`, `C/ClusterFRootdeepSeeder.cs:42`, `T/Mobiles/Burrows/BurrowsCreaturesVerification.cs:190`, `T/Regions/RootdeepVaultVerification.cs:207` | P140 creatures, P141 Vault; P167/P188 completed later map/placement work. |
| F-46: Third-party creature-body delivery | No body has shipped; route needed; same unnumbered prompt as F-45 (`Q:3320`) | Built. Creature animation encoding, body conversion/type records, package assembly, and local overrides exist. This does not turn on the still-pending evo rows automatically. | `K/scripts/build-equip-anims.py:256`, `K/player-package/payload/app/Build-UoOverrides.ps1:40`, `T/Mobiles/Burrows/BurrowScampBodyRouteVerification.cs:1` | P139 route; P140 expanded body content. |
| F-47: Requisitions and Appraiser | Decided; unnumbered prompt waiting behind ports (`Q:3332`) | Partly built against the full entry. The board/Appraiser cycle, personal requests, tier gates, turn-ins, Renown/standing, and Appraiser-price gold exist. Custodians are excluded. Hunt-specific slayer selection and future real-hall integration remain (planned). See Contradictions. | `C/Requisitions/RequisitionSystem.cs:109`, `C/Requisitions/RequisitionSystem.cs:123`, `C/Requisitions/RequisitionSystem.cs:216`, `C/Requisitions/Appraiser.cs:111`, `T/Misc/RequisitionsVerification.cs:198` | P150; P203 integration fix-up. |
| F-48: Leads | Designed with F-47; unnumbered prompt (`Q:3370`) | Built with differences from the design wording. Personal area/group Leads, expiry, additional drops, and pity tracking exist. Qualifying kills use a Fame/area/family proxy; the additional roll approximates the requested doubled chance. See Contradictions. | `C/Requisitions/RequisitionLeads.cs:50`, `C/Requisitions/RequisitionLeads.cs:161`, `C/Requisitions/RequisitionLeads.cs:211`, `C/Requisitions/RequisitionLeads.cs:240` | P150; P203 integration fix-up. |
| F-49: Guild headquarters outside New Haven | Towns decided; per-hall survey (planned); placement unspecified (`Q:3394`) | Not started for the world headquarters. P151 surveyed sites without placing halls. Current seeder anchors remain the chapter locations. Decor packs exist, but do not implement the world headquarters, full shops, travel stops, or trials (planned). | `C/ClusterFGuildHallSeeder.cs:36`, `C/ClusterFGuildStarterPath.cs:210`, `N/cc-P151-guild-halls-survey.md:3` | P151 survey; P265 chapter decor only. |
| F-50: Unravel-result satchel routing | Batched P137 section 6 (`Q:3439`) | Built. Disenchant output routes to a backpack satchel; stock unravel materials also route on loot pickup. A full satchel falls back to the backpack. The queue's Essence Shard wording differs from the custom output's name. | `C/ArtificersSatchel.cs:68`, `C/ArtificersSatchel.cs:73`, `C/ArtificersSatchel.cs:96`, `C/ArtificersImbueGump.cs:1991`, `C/ClusterFBackpack.cs:50`, `T/Misc/UnravelSatchelVerification.cs:182` | P137; P176 added later container unraveling. |
| F-51: Herbalism and reagent growing | Design settled; P260 research and phased plan (`Q:3450`) | Not started for Herbalism. Stock-style raised beds exist as a prior port. The new skill, wild gathering, reagent strains, garden kit/familiar, yard placement, and public plots are (planned). | `C/Services/Plants/Raised Garden Beds/RaisedGarden.cs:23`, `N/cc-P260-herbalism-research.md:13` | P260 research only; P128 built raised beds. |

## Built features without their own queue entry

These are additional systems or substantial parts found in the reviewed source.
Ports are grouped by their player feature, rather than listing every item class.
A mention as a dependency or an idea under another F-number is identified below.

| Built feature or part | Relationship to queue | Evidence | Prompt, if known |
|---|---|---|---|
| Levelable crafted equipment, equipment XP, and attribute spending | F-12 discusses player levels and requirements; it does not track the separate equipment-level system. Its acquisition source is not established by this audit. | `C/LevelGear/ClusterFLevelGear.cs:1`, `C/LevelGear/SmithsSealDeed.cs:1`, `T/Misc/LevelGearVerification.cs:1` | P261; P285 follow-up. |
| Additional accessory slots and toe rings | No separate entry. Loop-dependent slots remain disabled pending integration (planned). | `C/Accessories/ClusterFAccessories.cs:41`, `C/Accessories/AccessoryContainer.cs:1`, `C/Accessories/ToeRings.cs:1` | P262; P355 follow-up. |
| Companion base, lineage record, and party support | Companions appear as dependencies under F-12/F-33, not a tracked companion build. This is a foundation, not the full companion game (planned). | `C/Companions/BaseCompanion.cs:35`, `C/Companions/CompanionLineage.cs:1`, `C/Companions/CompanionParty.cs:1` | P264; P369 follow-up. |
| Artificer property knowledge, formula books, imbuing budgets, and forge sites | F-43 explicitly leaves this to a separate chat; no separate feature entry records the built rework. | `C/Imbuing/ClusterFImbueKnowledge.cs:26`, `C/Imbuing/ImbueFormulaBooks.cs:1`, `C/Imbuing/ImbueSites.cs:1`, `T/Misc/ImbuingReworkVerification.cs:1` | P82; later property/recipe fixes. |
| League Register book binding, consolidated ledger/logbook/satchel, backpack upgrades, and repair support | F-34 covers bank access, not the Register's wider implemented services. | `C/LeagueRegister/LeagueRegister.cs:167`, `C/LeagueRegister/LeagueConsolidation.cs:24`, `C/LeagueRegister/LeagueBackpack.cs:18`, `C/LeagueRegister/LeagueRepair.cs:31` | P280. |
| Expanded achievement presentation and event hooks | F-40 discusses reward boxes; no separate entry tracks the newer presentation and general trigger work. Hidden entries, names, conditions, and rewards are intentionally omitted. | `C/ClusterFNotedBySystem.cs:1`, `T/Misc/NotedBySystemVerification.cs:1` | P263; P361 follow-up. |
| Deployable trap kits and trap lesson | No separate entry. This is distinct from F-39's proposed dismounting traps. | `C/Items/Traps/Deployable/DeployableTraps.cs:49`, `C/Items/Traps/Deployable/TrapLesson.cs:1`, `T/Items/Traps/DeployableTrapsVerification.cs:1` | P275. |
| Young-clock restoration at a Fountain of Youth | F-5 tracks Young duration, not this later restoration service. | `C/FountainOfYouth/FountainOfYouth.cs:57`, `C/ClusterFYoungPlayer.cs:41`, `T/Misc/FountainOfYouthVerification.cs:1` | P192. |
| Player self-resurrection service | No separate entry. It is distinct from Young-clock restoration and the tutorial's death lesson. | `C/ClusterFSelfResurrect.cs:5`, `C/ClusterFSelfResurrect.cs:34` | Original prompt unknown. |
| Taming anger and pet skill-gain scaling | No separate entry for these later training changes. Loop integration remains a separate dependency (planned). | `C/ClusterFTamingAnger.cs:37`, `C/ClusterFPetGainSpeed.cs:22`, `T/Skills/TamingAngerVerification.cs:1`, `T/Skills/PetGainSpeedVerification.cs:1` | P171, P172. |
| Pet training and ability profiles | No separate feature entry. Training support and saved profiles exist; this statement does not certify every proposed ability. | `C/Services/Pet Training/BaseCreature.PetTraining.cs:1`, `C/Services/Pet Training/PetTrainingStore.cs:1`, `T/Services/PetTraining/PetTrainingVerification.cs:1` | P120, P121, P130; P233 profile inspection. |
| Treasure-map revamp | F-6's proposed map reveals and F-33's mule reference treasure maps, but neither records the port. | `P/TreasureMap.cs:1`, `P/TreasureMapChest.cs:1`, `C/Services/TreasureMaps/TreasureMapInfo.cs:1`, `T/Services/TreasureMaps/TreasureMapRevampVerification.cs:1` | P127. |
| Monster stealing and shard gathering rules | Mentioned under F-48 as a tie, without its own queue entry. | `C/Services/Monster Stealing/Core/StealingHandler.cs:1`, `C/Services/Monster Stealing/Core/ThievesDenStealRules.cs:1`, `T/Services/Monster Stealing/MonsterStealingShardRulesVerification.cs:1` | P127; P142 shard rules. |
| High Seas fish, lobster traps, trophies, and sea champions | F-20 proposes Fishing deeds; it does not record this port. Profession fish quests remain (planned). Ships and naval combat are not certified by this row. | `C/Services/Expansions/High Seas/Items/Fish/FishInfo.cs:1`, `P/Fishing-high-seas-fish.patch:1`, `T/Services/HighSeasFishingVerification.cs:215`, `T/Services/HighSeasFishingVerification.cs:589` | P193; P209 follow-up. |
| Revamped dungeon encounters | F-32 references existing dungeon chests, not the encounter ports. Despise, Shame, Wrong, Covetous Void, Exodus, and Blackthorn have source/test coverage. This is not a fresh fidelity audit of each dungeon. | `T/Services/Revamped Dungeons/DespiseRevamped/DespiseRevampedVerification.cs:1`, `T/Services/Revamped Dungeons/Shame Revamped/ShameRevampedVerification.cs:1`, `T/Services/Revamped Dungeons/WrongDungeon/WrongRevampedVerification.cs:1`, `T/Services/Revamped Dungeons/Covetous Void Spawn/CovetousVoidSpawnVerification.cs:1`, `C/Services/Revamped Dungeons/TheExodusEncounter/ExodusEncounter.cs:1`, `T/Services/Revamped Dungeons/BlackthornDungeon/BlackthornDungeonVerification.cs:1` | Earlier dungeon batches; P194, P195, P196 and follow-ups. |
| Underworld mini-champion encounters | No separate entry. | `C/Services/MiniChampionSystem/MiniChampionSpawn.cs:1`, `C/Services/MiniChampionSystem/MiniChampType.cs:1` | P197. |
| Additional Eodon content | No separate entry. This row records ported content, not the completeness of every Eodon encounter. | `T/Services/TimeOfLegends/EodonRemainderVerification.cs:1` | P198; P354 follow-up. |
| Region, monster, and boss music selection | No separate entry. | `C/Music/ClusterFShardMusic.cs:45`, `C/Music/ShardMusicTable.cs:1`, `T/Misc/ShardMusicVerification.cs:1` | P368. |
| Halloween decorations and seasonal switching | F-21 originally held Halloween back; there is now a separate seasonal implementation. | `C/ClusterFHalloweenDecorSeeder.cs:1`, `C/ClusterFSeasonalSwitch.cs:1`, `T/Misc/HalloweenDecorVerification.cs:1` | P267. |
| Flying-loot presentation | F-41 specifies fanfare, but does not track this later visual addition. | `C/LootBoxes/ClusterFFlyingLoot.cs:1`, `T/Misc/LootBoxFlyingLootVerification.cs:1` | P242, identified by the source header; P366 follow-up. |
| Container unraveling | F-50 tracks output placement, not selecting a container of input items. | `C/ArtificersImbueGump.cs:1`, `T/Misc/UnravelContainerVerification.cs:1` | P176. |
| Grove discovery records and resource satchel art | Discussed as dependencies or handoff items, without separate F-entries. | `C/WoodDiscoveryEntry.cs:1`, `C/ForestersLogbook.cs:1`, `C/SatchelArt.cs:1` | P13 grove tracking; P236/P284 satchel art. |

## Verification limits

No code, configuration, world state, or `docs/` file changed. No tests were added
or run, as this task has no lane tests. Existing test bodies and historical prompt
results were evidence, not a new passing test run. No build or package was made.
No live service, account, or Haven connection was used.

Absence findings used the canonical customization and patch trees, the existing
tests, and the corresponding current implementation. For example, the account
limit still comes from upstream, the level-reset body is empty, the League gates
are waived, and commission payout still goes directly to smith currency. Searches
also checked for alternate names and call sites. No production call to the chest
spring helper, exploration map-learning helper, or first-Haul callback was found.
The generated `server/uo/` tree was not read.

External art licenses, installed client rendering, published package contents,
current live settings, world placements, and actual play pacing are unverified by
this review. The additional-features table is a system-level review, not a claim
that every leaf content class has been independently audited.

## Sources

- `docs/feature-queue.md`, read-only, including its handoff, Open, Batched, and
  Dropped sections. Its F-1 through F-51 entries are the row list above.
- Both work copies' `AGENTS.md`; read-only `docs/direction-decision.md`,
  `docs/tasks.md`, and `docs/README.md` supplied the working rules and scope.
- The current source and test files cited in the tables are the primary evidence.
  Client patches and player-package scripts were read for features that need them.
  Upstream `Accounting/Account.cs:461` was checked in the pinned read-only tree.
- Early queue research and builds: `N/cc-P14-newhaven-guild-mapping.md`,
  `N/cc-P15-guild-starter-path.md`, `N/cc-P18-reset-stone-young-craftx.md`,
  `N/cc-P20-skill-scaling-research.md`, `N/cc-P22-small-features-1.md`,
  `N/cc-P24-new-haven-dungeon-research.md`, `N/cc-P26-animated-runestone.md`,
  `N/cc-P30-modernuo-upgrade-research.md`,
  `N/cc-P32-spawner-importer-bods-self-repair.md`, `N/cc-P33-clean-up-britannia.md`,
  `N/cc-P34-winter-decor.md`, `N/cc-P36-dungeon-build-1.md`.
- League, BOD, mimic, progression, and pet history:
  `N/cc-P41-companions-research.md`, `N/cc-P42-defect-batch-3.md`,
  `N/cc-P45-companion-probes.md`, `N/cc-P46-smith-orders-2.md`,
  `N/cc-P47-league-research.md`, `N/cc-P48-league-batch-1.md`,
  `N/cc-P49-dungeon-chests-research.md`, `N/cc-P50-chest-mimic-monster.md`,
  `N/cc-P51-staff-hub-and-raptor-pack.md`, `N/cc-P53-two-hundred-cap.md`,
  `N/cc-P54-f12-xp-and-gain-paths.md`, `N/cc-P55-bug-batch-5.md`,
  `N/cc-P57-batch-6.md`, `N/cc-P59-evo-pet-body-sheet.md`,
  `N/cc-P62-kitsune-walk-test.md`, `N/cc-P65-evo-pets-framework.md`,
  `N/cc-P69-mule-core.md`, `N/cc-P70-mule-modules.md`.
- Recipe, tutorial, and client builds: `N/cc-P77-alembic-guild.md`,
  `N/cc-P78-recipe-gating.md`, `N/cc-P79-loot-boxes-fanfare.md`,
  `N/cc-P80-new-player-tutorial.md`, `N/cc-P81-paperdoll-sos.md`,
  `N/cc-P137-usable-ankhs-and-playtest-fixes.md`,
  `N/cc-P139-rootdeep-burrows.md`, `N/cc-P140-rootdeep-burrows.md`,
  `N/cc-P141-rootdeep-burrows.md`, `N/cc-P150-requisitions-and-leads.md`,
  `N/cc-P151-guild-halls-survey.md`,
  `N/cc-P203-cont-fixup-requisitions-and-leads.md`.
- Later queue work: `N/cc-P226-arms-lore-matters.md`,
  `N/cc-P227-extended-wood-bonuses.md`, `N/cc-P228-exceptional-material-gap.md`,
  `N/cc-P229-league-reward-shop.md`, `N/cc-P230-staff-hub-events-tab.md`,
  `N/cc-P234-dismount-sources-design.md`, `N/cc-P235-work-order-numbers-pass.md`,
  `N/cc-P237-new-haven-community-art.md`, `N/cc-P238-climbing-boots.md`,
  `N/cc-P239-creature-levels-appraisal.md`, `N/cc-P240-fog-of-war-client-half.md`,
  `N/cc-P260-herbalism-research.md`, `N/cc-P266-new-haven-winter-decor.md`,
  `N/cc-P276-tutorial-farm-build.md`, `N/cc-P278-cont-fixup-climbing-boots.md`,
  `N/cc-P280-league-register-build.md`, `N/cc-P282-f12-numbers-and-level-gates.md`,
  `N/cc-P352-cont-fog-of-war-client-half.md`,
  `N/cc-P357-cont-fog-of-war-client-half.md`,
  `N/cc-P364-league-bestiary-batch-2.md`,
  `N/cc-P371-graduation-is-the-first-loop.md`.

## Contradictions

These are reported for review. This audit does not choose between them or change
the queue, decisions, or implementation.

- Status conflicts: F-8 says shipped in the handoff and ready to batch in its own
  entry. F-13, F-21, F-22, F-23, F-26's base work, F-28, F-30 Events, F-36, F-45,
  F-46, F-47, F-48, and F-50 retain pending or old batch wording despite the
  implementations cited above. F-6's client half is also present now. F-40/F-41
  and F-43 still name unnumbered prompts despite their built portions.
- F-4 fixes a single character per account, while F-44 says the character limit
  remains open. Current creation uses `a.Limit` (`C/CharacterCreation.cs:161`),
  supplied by the upstream expansion-based limit (`U/Accounting/Account.cs:461`).
- F-9 promises starter rewards once per loop. Current starter claims use saved
  records (`C/ClusterFGuildStarterPath.cs:405`); recording a loop does not reset
  those records (`C/Tutorial/ClusterFLoops.cs:47`). The complete progression reset
  remains empty at line 40 of that file.
- F-12 retains superseded ladders and an old on-hold research handoff. Current
  source has a ladder helper and first-loop graduation, while player skill caps
  remain flat (`C/Tutorial/ClusterFLoops.cs:31`, `C/ClusterFSkillCaps.cs:11`). P282's
  newer numbers are proposals, not built progression.
- F-14 asks for con color on every creature's name. The implemented con is a
  separate single-click information line, preserving the normal name color
  (`C/ClusterFCreatureLevels.cs:251`). Its player level is provisional at line 50.
  Box reward scaling uses a different skill-based substitute
  (`C/LootBoxes/ClusterFLootBoxes.cs:58`); neither is F-12 player XP.
- F-13's later decision calls for a larger veteran stat-cap reward. Upstream still
  adds five (`U/Engines/Veteran Rewards/RewardSystem.cs:589`), and the shard cap
  assignment sets the configured total without consulting veteran status
  (`C/ClusterFStatCaps.cs:105`). No corresponding reward override was found in the
  customization or patch trees. Current live cap settings are unverified.
- F-18's per-five-item checks and tailoring guild training are still described as
  remaining work, but newer OSI BOD ports can look like that work is finished.
  Smith checks remain one per small deed and a material-based large-deed count
  (`C/ClusterFSmithBODSystem.cs:461`). Tailoring uses OSI points
  (`C/Services/BulkOrders/BulkOrderVendors.cs:158`), not the requested seal system.
- F-19's entry says a bonus per League rank, while F-24's later decision changes
  bonuses to milestones. Code implements milestones
  (`C/ClusterFBankLimit.cs:46`). The old F-19 stub description also remains.
- F-24 names milestone chapters, then calls them five trials in the same block.
  Source defines chapter slots at `C/ClusterFLeagueRanks.cs:123`; the queue's
  listed milestone names and this code remain the evidence, without adopting the
  prose count. Promotion jobs and trials are still waived at lines 182 and 188.
- F-25's final answer restores rank-based deed caps, while current smith issuance
  uses fixed caps (`C/ClusterFSmithBODSystem.cs:56`). It also asks for a smaller
  direct-fill bonus, while payout computes from the deed without recording that
  fill distinction (`C/ClusterFSmithBODSystem.cs:477`, `C/LargeBODItemFill.cs:28`).
  Its cash-out description includes seals; current cash-out pays gold and an item
  chance (`C/ClusterFSmithBODPayout.cs:213`).
- F-29 says every exceptional material gets the multiplier, including F-28's
  woods. P228 deliberately excludes the extended-wood table
  (`C/ClusterFExceptionalMaterial.cs:23`). That table keeps normal plus its
  exceptional additions instead. This audit does not decide which rule should win.
- F-33 and F-39 refer to dismount resistance as if the mule module already hooks
  it. The module explicitly says Stubbed
  (`C/Mobiles/Mule/MuleModuleData.cs:116`); P234 reports the same gap.
- F-35's early story promises the guided lesson sequence; current station dispatch
  still includes a preview fallback (`C/Tutorial/ClusterFTutorial.cs:122`). The
  later farm and graduation implementation does not complete those other trials.
  Fox/bird/kitsune rows also remain art-pending despite F-46's completed body route
  (`C/Mobiles/Evo/EvoPetData.cs:114`).
- F-38 describes fixed-contract counts and says a numbers pass is needed. P235
  disputes the old mining count and provides its definition list. The audit does
  not adopt either count; the current registered definitions are at
  `C/ClusterFWorkOrderSystem.cs:382` and `C/ClusterFWorkOrderSystem.cs:1991`.
- F-43 says minimum-skill items at or below its free threshold are free, while
  classification checks an existing OSI recipe before the free band
  (`C/Engines/Craft/ClusterFRecipeGate.cs:135`). It also says existing OSI recipe
  gates remain, leaving overlapping rules for that case.
- F-48 promises doubled drop chance. The code makes an additional Fame-band roll
  with pity, rather than multiplying the creature's actual loot probability
  (`C/Requisitions/RequisitionLeads.cs:211`). Its proposed qualifying-loot-table
  test is replaced by Fame, area, and family checks at line 161. The source comments
  explicitly identify that substitution at lines 5 and 11.
- F-47 says each guild posts requests and all open postings roll over daily. The
  Custodians post none (`T/Misc/RequisitionsVerification.cs:198`), and requests with
  live Leads are retained (`C/Requisitions/RequisitionSystem.cs:123`). F-48 also
  says Leads outlast a daily refresh, so the queue contains overlapping expiry
  rules without stating the exception in F-47.
- F-50 calls the custom output Essence Shards; the satchel routes `PropertyEssence`
  plus stock unravel materials (`C/ArtificersSatchel.cs:68`). That custom item
  displays as "Essence of" its property (`C/PropertyEssence.cs:42`). This is a
  terminology difference, not evidence of an additional missing output type.
