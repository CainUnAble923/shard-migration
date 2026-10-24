# P533: review findings checked against main, round 3

October 24, 2026. Notes only. These are proposed prompts, not queued tasks or authority to change a running service.

Checked local code main `70df7c5add59d18310be69b1950d06558f6ed6cd` and notes main `42d9618445c7a0505af6ef51101ac435cb74eeb6`. Both work-copy HEADs matched those refs and started clean. Read both working agreements, direction decision, task list, P429, P476, P480, the available P482-P529 notes and adjacent reviews, prompt queue/completed work, and Chase's October 23 decisions at `docs/feature-queue.md:2018`.

During final checking, code main advanced to `0de0d9e8926583765b1404459af6eb8f3c5a3683` with P411. Read its full prompt from `cc-prompts/merging/cc-P411-launcher-always-starts.md`, its merge diff, and the new launcher source with `git show main:<path>`, without changing this work copy. P411 explicitly requires launch after timeout/failure with previous overrides or none. Accordingly P504 #1 is now a policy risk, not authority to block launch; U7 is restricted to server-overlay safety and warning tests, with client policy in C16. Other reviewed implementation branches were unchanged by that merge. Snapshot references below are to the initial source unless a row explicitly cites P411/main.

Notes main also advanced to `ec0c5e38c3c666182e18935b908624fa825d3250` for P534 and generated/test-report artifacts. Checked the changed-file list and P534 work record directly from main. No P482-P529 source note, governing decision or implementation tool changed in that delta. P534 is another design comparison, not a queued implementation of the findings here. The work-copy branches remained untouched. These are the final audited main cutoffs for this report.

## In plain words

- Checked every numbered bug/risk finding in the available review set against current source. The table has 141 entries, including P482's optional cleanup nit, from the 32 source files listed at the end.
- Wrote 32 grouped prompt drafts, urgent player-loss/value/save failures first, and additions to existing work instead of duplicate prompts.
- Kept policy choices, unfinished features and missing tests distinct from demonstrated source failures. Chase's existing League decisions remain in force.
- Changed only these notes. No code, queue prompts, running services or accounts changed, and no implementation tests were run.

`C/` = code server/customizations; `T/` = code server/tests; `P/` = code server/patches; `U/` = read-only D:/UO/ModernUO-pinned/Projects; `G/` = installed D:/UO/golem; `M/` = migration tools; `N/` = migration notes. Other paths start in the code repo. Current line numbers sometimes differ from the original reviews.

Confirmed means source-confirmed, not newly reproduced in a running shard. Risk means mechanism verified but impact/runtime still unverified. Test gap does not establish a bug. Covered means existing prompt/draft ownership, not fixed in main. Policy requires Chase's choice. Backlog means unfinished or deferred functionality. Installed means checked against current external Golem files; their exact correspondence to versioned main is unverified.

## Verdict table

The source for each numbered row is `notes/cc-P<number>-review-*.md`, with the topic identified below. Repeated findings retain both review IDs and share one owner.

| Finding | Verdict and effect | Current evidence | Owner |
|---|---|---|---|
| P482 #1 | Confirmed: imbuing ignores level-bought property slots. | C/ArtificersImbueGump.cs:1799; LevelGear/ClusterFLevelGear.cs:568,612 | W2 |
| P482 #2 | Confirmed: extra jewelry loses bought bonuses and XP. | C/Accessories/ClusterFAccessories.cs:302,320; LevelGear/ClusterFLevelGear.cs:556 | W3, same as P486 F05 |
| P482 #3 | Policy: material Luck sits outside the stated item ceiling; no wearer-wide cap bypass established. | C/LevelGear/ClusterFLevelGear.cs:175; ResourceInfo.cs:189; ClusterFExceptionalMaterial.cs:43 | C1 |
| P482 #4 | Policy/risk: gear XP awarded after owner leaves fight. | C/LevelGear/ClusterFLevelGear.cs:490,524,533 | C2 |
| P482 #5 | Test gap: repair/trade/death/cold-load preservation. No reset found in source. | T/Misc/LevelGearVerification.cs:372 | W2 |
| P482 #6, nit | Confirmed: save filters deleted rows without pruning memory. | C/LevelGear/ClusterFLevelGear.cs:251 | W2 optional |
| P483 #1 | Policy/risk: public flight reveals position without visibility/LOS filtering. Rendering unverified. | C/LootBoxes/ClusterFFlyingLoot.cs:148; U/Server/Effects.cs:465 | C3 |
| P483 #2 | Test gap: Sent/Major notification does not prove actual effect recipients. | T/Misc/LootBoxFlyingLootVerification.cs:144,280 | Attach to C3 if approved |
| P483 #3 | Test gap: full pack/bank delivery. No loss found: fallback bank DropItem bypasses capacity refusal. | C/ClusterFGuildPromotion.cs:236; U/Server/Items/Container.cs:464 | Attach to C3; no separate fix |
| P484 #1 | Confirmed: current-tile probe collides with climber, disabling climbed-state restrictions. | C/ClusterFClimbing.cs:110,187; U/Server/Maps/Map.cs:1000 | W1 |
| P484 #2 | Confirmed: destination validation omits caster and region travel veto. | C/ClusterFClimbing.cs:289; U/UOContent/Spells/Base/SpellHelper.cs:609,634 | W1 |
| P484 #3 | Confirmed: hop resolution permits Frozen/Paralyzed. | C/ClusterFClimbing.cs:329 | W1; P458 concerns vines |
| P484 #4 | Test gap: pending boots target lifecycle. Deletion/equipment/life checks already exist. | T/Misc/ClimbingBootsVerification.cs:186,381; C/ClimbingBoots.cs target callback | W1 |
| P486 F01 | Confirmed: locked slot hides stored jewel and Remove. | C/Accessories/AccessoriesGump.cs:81 | W3 |
| P486 F02 | Confirmed: eligibility loss leaves applied bonuses and cached resists. | C/ClusterFLeagueRanks.cs:251; Accessories/ClusterFAccessories.cs:338 | W3 |
| P486 F03 | Confirmed: extra-slot insertion skips equip validation/hooks. Special-ring examples partly dormant. | C/Accessories/ClusterFAccessories.cs:430 | W3 |
| P486 F04 | Confirmed: carrier-based rings/bracelets rejected by KindOf. | C/Accessories/ClusterFAccessories.cs:115; Items/Artifacts/Equipment/Jewelry/BraceletOfPrimalConsumption.cs | W3 |
| P486 F05 | Confirmed, same failure as P482 #2. | C/Accessories/ClusterFAccessories.cs:302,320; LevelGear/ClusterFLevelGear.cs:556 | W3 only |
| P486 F06 | Confirmed: custom imbues and Fortune equip time skip active extras. | C/Imbuing/ClusterFImbueEffects.cs:153,172,186 | W3 |
| P486 F07 | Confirmed: changing an active jewel's skill bonus leaves old applied mod. | C/ArtificersImbueGump.cs:1895; Accessories/ClusterFAccessories.cs:345 | W3 |
| P486 F08 | Confirmed: taking shoes off activates toe rings without achievement check. | C/Accessories/ClusterFAccessories.cs:508,520 | W3 |
| P486 F09 | Test gap: filled-slot transitions, repeated refresh, stats/skills and actual capped consumers. No normal item duplication found. | T/Misc/AccessorySlotsVerification.cs:153,313 | W3 |
| P487 #1 | Confirmed save-order defect: elemental split recomputed before equipment payloads load. | C/Companions/BaseCompanion.cs:280,313; U/Server/World/World.cs:661,684 | U1 |
| P487 #2 | Confirmed player loss: inherited transfer clears bond. | U/UOContent/Mobiles/AI/BaseAI/TransferItem.cs:149,163; C/Companions/CompanionParty.cs:108 | U1 |
| P487 #3 | Confirmed: stock transfer checks slots, not companion party count. | Same TransferItem.cs:77; C/Companions/CompanionParty.cs:61 | U1 |
| P487 #4 | Confirmed player loss: hourly loyalty sweep can release companions. | U/UOContent/Mobiles/BaseCreature.cs:6008,6014,6046; no companion exception in patches | U1 |
| P487 #5 | Confirmed recovery failure: disabled login skips saved away companion. | C/Companions/CompanionParty.cs:141,150; BaseCompanion.cs:308 | U1 |
| P487 #6 | Risk/save problem: restart of online-owner save lacks logout/away reconciliation. | Same party file:28,150; U/Server/Mobiles/Mobile.cs:6510; CanAutoStable=false | U1 |
| P487 #7 | Test gap: same-serial copies and helper calls mask cold load/death/release. | T/Mobiles/Companions/CompanionBaseVerification.cs:54,61,156 | U1 |
| P488 #1 | Confirmed save problem: Exodus exit/restart timer disappears. Inherited broken behavior. | C/Services/Revamped Dungeons/TheExodusEncounter/Region.cs:140,147; VerLorRegController.cs:129 | U5 |
| P488 #2 | Confirmed: Asclepius tooltip has no bandage consumer. | Same encounter Loot/Asclepius.cs:27 and GargishAsclepius.cs:27; bandage patches | U5 |
| P488 #3 | Confirmed save problem: revealed locked chest loses expiry. | Same encounter Items/ExodusChest.cs:244 | U5 |
| P488 #4 | Confirmed: available Exodus rewards retain MISSING cleanup value rows. | C/Services/PointsSystems/CleanUpBritanniaData.cs:851-856 | U5 |
| P488 #5 | Test gap: separate rewarded-character store not restarted; no repeat-stat exploit established. | T/Services/Revamped Dungeons/TheExodusEncounter/ExodusEncounterVerification.cs:778,818 | U5 |
| P489 #1 | Confirmed port loss: Wrong keeps first XML entry only. | C/Services/Revamped Dungeons/WrongDungeon/WrongSpawns.cs:64-91; ServUO RevampedSpawns/WrongRevamped.xml | W4 |
| P489 #2 | Confirmed: capture resurrects before normal death sets ghost body. | Same Wrong folder Region.cs:115; U/Server/Mobiles/Mobile.cs:4872,4911 | W4 |
| P489 #3 | Covered, still present: pending confirmations deliver without payment. | C/Gumps/BaseRewardGump.cs:254; Covetous Void Spawn/Gumps.cs:293 | P476 U1 explicitly includes Void Pool |
| P489 #4 | Confirmed player/save loss: cauldron charges unsaved. | C/Services/Revamped Dungeons/Covetous Void Spawn/Items/CauldronOfTransmutation.cs:29 | U6 |
| P489 #5 | Risk: destination 5868,554,15 lacks return bedroll in search range. Actual escape unverified. | WrongDungeon/Items/BedrollSpawner.cs:41,249; room doors in WrongDecoration.cs | W4, probe first |
| P489 #6 | Confirmed: best-single update returns after first improved player. | Covetous Void Spawn/VoidPoolStats.cs:74 | U6 |
| P489 #7 | Confirmed record loss: BestWave aliases CurrentScore, cleared next battle. | Same VoidPoolStats.cs:294; VoidPoolController.cs:282 | U6 |
| P489 #8 | Risk/restart race: delayed cleanup deletes a new wave. | Same VoidPoolController.cs:775,781 | U6 |
| P489 #9 | Test gap: Cora real death, rights and delivery not exercised together. | T/Services/Revamped Dungeons/Covetous Void Spawn/CovetousVoidSpawnVerification.cs:565,607 | U6 |
| P490 #1 | Confirmed: category heading can be orphaned and continuation has no heading. | C/ClusterFAchievements.cs:2364; T/Misc/AchievementCategoryIconsVerification.cs:131 | W5 |
| P491 #1 | Confirmed exception: second wrong guess repeats Dictionary.Add. | U/UOContent/Engines/Khaldun/PuzzleChest.cs:344; P/PuzzleChest-trap-training-kit.patch does not repair it | A1 to P476 W5, urgent |
| P491 #2 | Confirmed: disabled mini champion restarts in cooldown or after load. | C/Services/MiniChampionSystem/MiniChampionSpawn.cs:236,444 | A1 |
| P491 #3 | Confirmed: shallow cleanup versus recursive key searches preserves session items until their own expiry. | C/Services/Underworld/PuzzleRoom/MagicKey.cs:102; PuzzleBox.cs:46,74 | A1 |
| P491 #4 | Risk: deleting gem before startup callback leaves repeating timer. | C/Services/Underworld/ExperimentalRoom/ExperimentalGem.cs:168,177,380,408 | A1 |
| P492 #1 | Installed/confirmed: nonterminating file errors bypass kit rollback. | G/Kit.ps1:135-167; Install-Kit.ps1:15 | W12 |
| P492 #2 | Installed/confirmed: WIP fix reports success after failed Git. | G/TinkerLib.ps1:249-253 | W12 |
| P492 #3 | Installed/confirmed: unknown reasoned fixes bypass daily fix cap. | G/TinkerLib.ps1:577,603-607 | W12 |
| P492 #4 | Installed/confirmed wrong evidence: remote warning judged from local lock folder. Actual remote state unverified. | G/TinkerLib.ps1:221 | W12 |
| P492 #5 | Installed/confirmed: equal hashes/local resync success does not recover dead watch; Force ineffective. | G/TinkerLib.ps1:369,373 | W12 |
| P492 #6 | Installed/confirmed: card asks for answers but has no answer action. | G/TinkerLib.ps1:427; web-console/static/app.js Tinker card | W12 |
| P492 #7 | Installed/confirmed: equal hashes skip missing settings keys in both kit paths. | G/Remote-Agent.ps1:248-250; TinkerLib.ps1:373 | W12 |
| P492 #8 | Installed/risk: allowed fixes ignore confidence/response shape. | G/TinkerLib.ps1:601-606; tinker-rulebook.md | W12 |
| P492 #9 | Installed/risk: dynamic mail text lacks common credential redaction. No real leak verified. | G/TinkerLib.ps1:427; TinkerMail.ps1:80,82 | W15 |
| P493 #1 | Confirmed: correctly leveled account retains elevated character. | C/Misc/GolemTestAccounts.cs:234-245 | W11 |
| P493 #2 | Installed/risk: git grep puts real password in process arguments. | G/tests/GolemTestAccounts.Tests.ps1:173 | W11 |
| P493 #3 | Installed/risk: failed ACL ignored, plaintext written first, old explicit grants retained. | G/GolemTestAccounts.ps1:127,215-216 | W11 |
| P494 #1 | Confirmed player loss: approval destroys newly added/swapped items not previewed. | C/ArtificersImbueGump.cs:1438,2042 | U2 |
| P494 #2 | Confirmed: BlessedFor gear passes shared protection guard. | Same file:1961; U/Server/Items/Item.cs:4428 | U2 |
| P494 #3 | Confirmed economic risk: Basic imbue returns more shards than purchase costs, with gold/gear still spent. | C/ArtificersImbueGump.cs:100,114,308,1979; Imbuing/ImbuingTable.cs:99 | U2; C4 for formula |
| P494 #4 | Confirmed: selected bag's lock checked, ancestors ignored. | C/ArtificersImbueGump.cs:2031; GuildResources.cs:92 | U2 |
| P494 #5 | Test gap: self-referential yields and immediate approval miss changing contents/protection/delivery. | T/Misc/UnravelContainerVerification.cs:114,133-137 | U2; update expected yield if formula changes |
| P495 #1 | Confirmed inconsistent state: partial reload reported old and acknowledged successful. | docker/test-queue/server.py:624,629,633; M/codereload.py:99,143 | W16 |
| P495 #2 | Confirmed: survey mistakes rejuvenation/Despise ankhs for resurrection sources. | C/ClusterFAnkhs.cs:43; U/UOContent/Items/Addons/RejuvinationAnkhs.cs; C/Items/Functional/DespiseAnkh.cs | W17 |
| P495 #3 | Confirmed: standalone working ankhs omitted from Sightings. | C/ClusterFAnkhs.cs:230-235 | W17 |
| P495 #4 | Policy/risk, inherited: shrine offer can travel. Region resurrection veto still applies. | U/UOContent/Items/Construction/Ankhs.cs:43; Gumps/ResurrectGump.cs:193 | C5 |
| P495 #5 | Test gap: no accepted resurrection/fame loss/cancel/region/living-action proof. | T/Misc/AnkhVerification.cs:169,201 | W17 |
| P495 #6 | Confirmed upstream defect: ghost context resurrection entry disabled. | U/UOContent/Items/Construction/Ankhs.cs:22; Context Menus/ContextMenuSystem.cs:95 | W17 |
| P496 #1 | Test gap only: props arrow tested with null TrainingProfile. | T/Services/PetTraining/PropsAbilityProfileVerification.cs:255 | Next pet-training change; no standalone fix |
| P497 #1 | Confirmed build risk: cached publish and no-restore tests skip fresh advisory audit. No current vulnerable package established. | docker/uo/Dockerfile:65; build.sh:71,88 | W10 |
| P497 #2 | Test gap: missing-source/collision installer guards not exercised red first. | docker/uo/apply-patches.sh:260,264 | W10 |
| P498 #1 | Confirmed: token read, consumption and job reservation are separate. | web-console/server.py:559,579,590 | W8 |
| P498 #2 | Confirmed: rollback resolves latest image again after preview. | scripts/Shard-Console.ps1:5975; web-console/server.py:542 | W8 |
| P498 #3 | Confirmed: multiGolem=false is picker-only, not dispatch/runner restriction. | web-console/server.py:1812; scripts/Invoke-WebConsoleAction.ps1:161 | W8 |
| P498 #4 | Risk: timeout kills parent, leaves children, and code 1 lacks timeout label. | web-console/server.py:382,399 | W8 |
| P498 #5 | Risk: actions run without durable start audit; write failures swallowed. | web-console/server.py:402,430 | W8 |
| P499 #1 | Installed/confirmed: idle pending marathon wake without restReason never retried. | G/golem.ps1:4404-4412,4426 | W13 |
| P499 #2 | Installed/confirmed: no fresh target does not stop remembered automatic wake. | G/golem.ps1:1868-1883 | W13 |
| P499 #3 | Installed/confirmed: cached usage timestamp replaced by watch time, manufacturing slowdown. | G/golem.ps1:927,936 | W13 |
| P499 #4 | Installed/risk: auto marathon survives weekly reset with unknown projection. | G/golem.ps1:1091-1116 | W13 |
| P500 #1 | Installed/confirmed: comments after first version can expose draft text and select future version. | G/Golems.ps1:1186-1197,1216-1220 | W14 |
| P500 #2 | Installed/confirmed announcement loss: duplicate identity ignores audience. | Same file:1211,1218 | W14 |
| P500 #3 | Installed/confirmed: duplicate table ignores star bullets. | Same file:1211; C/ShardVersion.cs consumer | W14 |
| P500 #4 | Test gap: existing-heading additions and unreadable-input rollback. | G/tests/Golem.Tests.ps1 P213 facts | W14 |
| P501 #1 | Confirmed: only first socket gets disconnect reset handler. | client/patches/0003-shard-buttons-achievements.patch:291-307 | W6 |
| P501 #2 | Confirmed: enhanced enabled-ID set survives connections. | Same patch:232; TazUO EnhancedOutgoingPackets.cs/EnhancedPacketHandler.cs | W6 |
| P501 #3 | Test gap: actual UI clicks, missing-art fallback and successive logins. | Same patch embedded ShardButtonsTests | W6 |
| P502 #1 | Confirmed: retained Rangers' elixir menu buys remotely or while dead. | C/OutridersGuildmasterGump.cs:366-385 | U4 |
| P502 #2 | Confirmed paid-item loss: full pack drops bank-funded elixir on ground. | Same file:377,383; U/Server/Mobiles/Mobile.cs:7594 | U4 |
| P502 #3 | Covered: alt can consume pending graduate claim. P480 reopening fixed a different failure. | C/Tutorial/ClusterFTutorial.cs:264; P453 recorded-character scope | A2 to P453 |
| P502 #4 | Test gap: independent prices, paid non-Young vet, refusal paths. | T/Tutorial/TutorialFirstPlayVerification.cs:397,453,465 | U4 |
| P503 #1 | Confirmed escaped value: split remainder untracked until startup sweep. | C/Tutorial/TutorialWingTrials.cs:362,427,486 | U3; P523 #1 same root |
| P503 #2 | Confirmed escaped value: missed-shot recovery creates ordinary arrows. | Same file:349; U/UOContent/Items/Weapons/Ranged/BaseRanged.cs:145; AmmoRecovery.cs:116 | U3 |
| P503 #3 | Confirmed save problem: outstanding tithing loan unsaved while points save. | Same wing file:92,109,432; U/Server/Mobiles/Mobile.cs:2378 | U3 |
| P503 #4 | Confirmed false completion: delayed spell damage counts as weapon/readied-move hit. | C/Tutorial/TutorialWingTrials.cs:553-580 | W7 |
| P503 #5 | Confirmed false completion: school roll and unrelated later effect accepted. | Same file:533,579,586 | W7 |
| P503 #6 | Confirmed false completion: spell heal satisfies bandage lesson. | Same file OnPatientHealed; pinned Bandage removes context before healing | W7 |
| P503 #7 | Confirmed blocker: rejected supply deleted but trial remains armed. | Same file:240,362-370 | U3 |
| P503 #8 | Test gap: injected callbacks accept missing/wrong actual action. | T/Tutorial/TutorialWingTrialVerification.cs:130,173,208,248 | W7 |
| P504 #1 | Policy/risk persists: P411 now deliberately launches with previous overrides or none. Do not reverse that approved behavior. Player stranding unverified. | New main player-package/payload/app/Overrides-Launch.ps1:149,163; Build-UoOverrides.ps1:897; Setup.ps1:34 | C16; U7 covers server half only |
| P504 #2 | Test gap: Young warning/protection exists but not exercised on entry. | T/Regions/RootdeepWayInVerification.cs:174; U/UOContent/Regions/BaseRegion.cs:76 | U7 |
| P505 #1 | Confirmed validation gap: missing required animation group omitted from checks. Current assets present. | scripts/build-equip-anims.py:364; player-package/Build-PlayerPackage.ps1:197 | W9 |
| P505 #2 | Confirmed validation gap: shifted hips pass crown/back-box checks. No current bad tail proved. | scripts/check-paperdoll-fit.py:147,252 | W9 |
| P506 #1 | Installed/confirmed message loss: routine batch deleted before successful send. | G/golem.ps1:374-375; G/GolemMail.ps1:521 | W15 |
| P506 #2 | Installed/confirmed message loss: last 30 returned after whole queue deleted. | G/GolemMail.ps1:520-522 | W15 |
| P506 #3 | Installed/risk: note/question formatting lacks credential redaction. | G/GolemMail.ps1:111,137,335 | W15 |
| P506 #4 | Risk: bot crash reason/logs unfiltered in subject/body. | tools/playtest-bot/uobot/notify.py:51,57 | W15 |
| P506 #5 | Confirmed false success: soak-only errors leave passing opening/Nothing to do. | tools/playtest-bot/uobot/report.py:101,113 | W15 |
| P507 #1 | Installed/confirmed: repeated trigger and refused wake clear existing batch guard. | G/golem.ps1:2242,2253-2258 | W13 |
| P507 #2 | Installed/confirmed: slow opening permits second launch after duplicate spacing expires. | G/golem.ps1:2190,4087 | W13 |
| P507 #3 | Installed/confirmed: delayed night trigger opens noon window. | G/golem.ps1:4073-4094 | W13 |
| P507 #4 | Installed/confirmed: pending check ignores disabling night shift. | G/golem.ps1:2205,4337 | W13 |
| P508 #1 | Risk: pending staff callbacks retain authority after demotion. | C/StaffHub/ClusterFMapCheckCommands.cs:307,338 | W18 |
| P508 #2 | Confirmed: contained item supplies container-local coordinates. | Same file:340,346 | W18 |
| P508 #3 | Confirmed data loss: one list per staff member, not export name/map; clear ignores name. | Same file:283,296 | W18 |
| P508 #4 | Confirmed data loss: report paths collide within second. | C/StaffHub/ClusterFMapCheck.cs:988 | W18 |
| P508 #5 | Confirmed: malformed coordinate aborts whole validation. | Same file:543,562 | W18 |
| P508 #6 | Risk: accepted-spot cap does not bound input bytes/parsing/bad-row memory. | Same file:436,448; command File.ReadAllText:138 | W18 |
| P508 #7 | Test gap: immediate DeleteAll hides missing timer/load cleanup. | T/Misc/MapCheckVerification.cs:333-367 | W18 |
| P509 #1 | Confirmed decision-corruption mechanism: positional IDs attach answers to changed questions. | M/decisions.py:244 | U8 |
| P509 #2 | Confirmed answer loss from view when source question disappears. | Same file:254-270 | U8 |
| P509 #3 | Confirmed stale-transition risk: take/undo lack expected answer/taken revision. | Same file:425-446 | U8 |
| P509 #4 | Confirmed draft loss by renderer path; browser reproduction unverified. | docker/test-queue/html/index.html:361,430 | U8 |
| P509 #5 | Test gap: source-string tests do not execute hostile data in DOM. No current escaping defect found. | M/tests/test_decisions.py:410; page esc/md helpers | U8 |
| P510 #1 | Confirmed: claimed running prompt summary/model read uses prompt root only. | scripts/Shard-Console.ps1:7631 | W19 |
| P510 #2 | Confirmed: no-Summary prose parser consumes metadata. | Same file:5104 | W19 |
| P511 #1 | Confirmed gate failure: CheckZip skips client stamp validation. | player-package/Build-PlayerPackage.ps1:661-675 | W20 |
| P511 #2 | Confirmed gate gap: stamp not tied to required binaries. Wrong published client unverified. | player-package/PackageClient.ps1:82-108; builder:985 | W20 |
| P511 #3 | Confirmed gate gap: SkipTests writes shippable stamp. | client/Build-Client.ps1:70,86 | W20 |
| P521 #1 | Confirmed missing reward route; retroactive grants need policy. | C/ClusterFAchievements.cs:1340,1347 | C6, no automatic compensation draft |
| P521 #2 | Confirmed: initial Horse/Lizard body pick never offered. | C/Mobiles/Evo/EvoPet.cs:453,492; EvoPetData.cs initial choices | W21 |
| P521 #3 | Test gap: owner/mount/item/stable reload and unused statuette redemption. | T/Mobiles/Mounts/RewardMountVerification.cs:147 | W21 |
| P523 #1 | Confirmed escaped value: split/conversion outputs survive loan cleanup; conversions evade startup sweep. | C/Tutorial/TutorialTradeTrials.cs:346,371; TutorialWingTrials.cs:427 | U3, merged with P503 #1 |
| P523 #2 | Confirmed false completion: receiving existing product increases pack count. | C/Tutorial/TutorialTradeTrials.cs:538; T/Tutorial/TutorialTradeTrialVerification.cs:203 | W7 |
| P523 #3 | Confirmed false completion: passive combat Lumberjacking/craft Arms Lore accepted. | C/Tutorial/TutorialTradeTrials.cs:575; U/UOContent/Items/Weapons/BaseWeapon.cs:684,2532 | W7 |
| P523 #4 | Risk/blocker: outsider can tame lesson goat; TrialOwner unenforced. | C/Tutorial/TutorialTradeTrials.cs:404,629; pinned AnimalTaming.cs | W7 |
| P524 #1 | Installed/confirmed: original reclaimed before outstanding fix-up integrates. | G/Golems.ps1:638,652 | W14 |
| P524 #2 | Installed/confirmed: first matching repo treated as complete integration. | G/Golems.ps1:586-594,638; D:/UO/Commit-ShardWork.ps1 separate repo flow | W14 |

## Supplemental audits and guides

| Source/finding | Current verdict and evidence | Disposition |
|---|---|---|
| P512 plans; P513 patch notes | Plans/summary, no new defect findings. Earlier failures are explicitly still pending. | Existing finding owners, not proof of fixes. |
| P514/P512: unavailable tutorial with active island graduation gate | Confirmed dormant release blocker: C/Tutorial/ClusterFTutorial.cs:46; TutorialIslandGate.cs:27. P480 did not coordinate guards. | U4, inherited P475 review finding. |
| P514/P512: missing core client-window buttons | Confirmed actual trial route uses TutorialTrialGump without legacy Options/Journal/Map controls. | W7. |
| P514: portable vet offer; P480 driver silently skips absent rewards | Confirmed current TutorialPetCare.cs:136 and N/cc-P480-tools/playthrough.py:607. | U4; these are new defects, not P480's completed first-play work. |
| P514: P291 placement contention, saved Hiding loan, premature Fishing completion, false rerun failure | Confirmed TutorialTradeTrials.cs:292,455,575; N/cc-P291-tools/tradetrials.py:482. | Hiding U3; remaining cases W7. |
| P514/P516: open-door duplication, replacement stock signs, generator checks wrong checkout | Confirmed C/ClusterFGuildHallPlacement.cs:152,187; N/cc-P281-tools/gen.py:129. | A3, extend existing hall repair ownership. |
| P516: NPC adoption/deletion, dryrun door links, copied-design test | Covered by P463/P476; decor half and walkable towers already P459. | No second seeder prompt. |
| P516: Maritime, lab space, officer identity, Royal City post, tower assignments/player routes | Content/layout/rollout choices; private placement proof is not current-world availability. | C12. |
| P515 Register overflow/truncation and rank label | Confirmed C/LeagueRegister/LeagueRegisterGump.cs:152,200,207,309. P451 does not include paging/rank display. | W22. |
| P515 reset/rejoin keeps Register binding | Confirmed C/ClusterFGuildSystem.cs:1302 omits binding cleanup; DropLeft runs at book open. | W22. |
| P515 combined turn-in omits other order systems | Missing integration beyond P451's nested Smith-deed repair. | C10; future P178/shared action catalog. |
| P515 mule payment ignores gold helper result | Risk, not established free upgrade: MuleUpgrades.cs:141-154 preflights immediately on game thread; CompactGoldHelper.cs:35 rechecks but ignores lower consume results. | C11; prove a reachable mismatch before a currency-engine draft. |
| P515 partial mule effects, first-Haul and hunt hooks | Existing F-33/F-38/League backlog: MuleModuleData.cs, MuleModules.cs, MuleErrand.FirstHaulContract, RequisitionSystem.HuntFamily. | C11; do not rebuild delivered mule framework. |
| P514/P515/P528 owner-loop integration | Confirmed missing providers: EvoPet.cs:28, Companions/CompanionSettings.cs:121, Accessories/ClusterFAccessories.cs:164; no production assignment. Bond Trial unbuilt. | C7; do not enable loop slots or invent F-12/Bond Trial. |
| P517 F-12 flat caps and absent XP/reset/scroll/reserve/echo | Deferred player progression; ladder and tutorial loop exist. | Existing F-12 build, not regression fix. |
| P518 Focus gear causes early certainty/no gain | Conditional source risk, runtime unverified: C/RegenRates.cs Focus formula; ClusterFSkillGain.cs:247-268; U/UOContent/Skills/SkillCheck.cs:90-106. | C8; remaining practice paths P283 backlog. |
| P519 mound emptying creates bowl | Confirmed incomplete port interaction: U/UOContent/Engines/Plants/EmptyTheBowlGump.cs:95; raised-garden patches lack specialization. | W23. |
| P519 Herbalism, strains/seed-box key, familiar access, schedules/plots | Unbuilt content and future constraints. Current seeds have no strain field to lose. | F-51/P260/P392 backlog; C13. |
| P525 and many reviews: dry-run writes progress JSON | Confirmed M/progress.py:722 executes before dry-run return:737. | W24, one draft only. |
| P526 old achievement earners, initial choices, Boss/Tamer reachability | Old earners duplicate P521 #1; body choices duplicate #2; boss death already P455; absent Tamer mapping a source-design choice. | C6/C9, W21; no second death-hook prompt. |
| P526 routes/stats/deployment/veteran interval/red dragon | Publication/balance questions, not new verified failures. | C9. |
| P528 history/ground/mining/range/followers, quick large commissions, recycling, dictionary tests | Already P427/P454/P457/P476 W15. P457 includes Chase's own-craft-or-loot ruling. | Existing owners only. |
| P528 Sacred Journey/scissors achievement omissions | Source omissions beyond P457's specified fixes. | A4 if broader routes retained. |
| P528 companion-boss achievement, later-loop replays, missing tiers/conditions | Uncalled hooks, often waiting on owning gameplay; account-wide grants were disclosed. | C7/C14; F-12/League backlog. |
| P528 placeholder rewards, novelty sources, Hunter scaling, strength guarantee, replacement joke box, mute/audience | Existing defaults plus unfinished content/balance policy. Universal gear-strength guarantee unproved. | C3/C9/C14; no generated art or duplicate reward framework. |
| P529 map failure/entry, entrance upgrades, Vault recovery/rewards, reinforcements, resource/tests | Map client C16 after P411; server overlay loss from P425 #1 U7. Entrance P413. Vault/reinforcements P476 U4. Resmelt P476 W11; goza P476 W14; tests with owners. | No second Rootdeep/crafting build. |
| P529 Rootwood, Brood Pit, puzzles, recipes/replacement quest, Young death destination | Existing P24/P36/F-45 backlog and explicit death-route policy. | C15. |

P485, P520 and P527 have no review note in this snapshot. P522 skipped absent quest-marker code as instructed. All adjacent P482-P529 Codex review files report no additional findings. P525/P526's player guides are draft documentation, not code fixes.

## Overlap rules for issuing the drafts

P427 keeps pet-death gear XP and its other findings. P451-P460 keep all P429 work. P476 U1 already explicitly includes the Void Pool confirmation exploit. P476 W5 owns mini champion/Underworld state; extend it with A1. P459 and P476's hall follow-up own seeder work; extend with A3. P453 owns recorded-character tutorial claims; extend with A2. P457 owns its achievement sweep; A4 is an optional extension.

P480 is completed in main: do not draft its core-only menu, reorder, colored supplies, reopened picker, vet creation or elixir stock again. P502 and the retained-offer/driver failures concern behavior its work did not fix. P412/P413 keep stump/entrance work; P481 is start-area design only. Queue/completed prompts were read and searched, with claimed work checked as well. No queued/completed fix implements the new U/W scopes below in this snapshot.

Final overlap update: P411 merged while P533 was running. Its timeout, staging, progress, update-time preparation and launch-without-overrides behavior are already owned and built. No draft below repeats or reverses them. Any stricter client map requirement needs the explicit policy resolution in C16.

## Urgent drafts

Replace P?? consistently before issuing. Every prompt below inherits both working agreements: canonical layering, no Haven/deploy/account operations, no docs/ edits, no Git mutations by the lane, files below 5 MB, Windows PowerShell 5.1, and every new regression seen failing before the fix and passing afterward. A test-only gap can use a controlled broken-behavior run before restoring it. These rules apply even where a block is short. Any upstream patch needs an alternatives note first. Drafting does not authorize implementation in this task.

### U1. Companions survive transfers, loyalty sweeps, disabling and restart

```text
# CC task P??: companion lifecycle fix-up: keep bonds and recover owners and equipment after restart
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P487 #1-#7 found permanent companion loss and cold-load failures. Fix the existing base without building hiring, rooms, combat AI, or a new progression system.

1. Reproduce an isolated cold load of an owner, companion and elemental weapon. Recompute the weapon split only after equipment payloads and parents are loaded, or calculate it at the actual damage reader. Do not treat the existing same-serial copy test as cold-load proof.
2. Block ordinary companion pet transfers until a supported transfer path exists. Check both the initial command and acceptance of an already open trade. Preserve normal pet transfers. This closes bond loss and the bypass of CompanionParty.CanTake without inventing companion trading policy.
3. Exempt controlled companions from involuntary hourly loyalty release through a narrow hook. Ordinary pets retain stock loyalty behavior; player-requested release remains possible and frees slots once.
4. Recover already-away companions even when the feature has since been disabled. Reconcile unroomed companions whose owner was online at save but offline after load, including ghosts. Avoid recovering a released, deleted or genuinely roomed companion.
5. Tests, red first: elemental weapon cold load; transfer opened before refusal; full party with spare follower slots; repeated loyalty hours; enabled logout/disabled login; restart from online-owner save; ghost logout/login; release and deletion without resurrection or double slot changes.
6. Use versioned fields/migrations only if required, preserving existing saves. Run docker/uo/build.sh -t sl-modernuo:cc-P?? with the companion regressions. Record exact cold-load setup, patch alternatives and limits in notes/cc-P??-companion-lifecycle.md. End with P?? DONE.
```

### U2. Unravel exactly what was approved, preserve protected gear, close shard gain

```text
# CC task P??: Artificers unravel fix-up: stable confirmation, personal blessings, locked ancestors and bounded recovery
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P494 #1-#5 found destructive confirmation changes and a shard recovery imbalance. The recovery policy in P533 C4 needs approval before that part is numbered; the protection fixes can proceed separately.

1. Retain the exact eligible item identities at preview. At approval, recheck each saved item's deletion, direct parent, ownership and protection. Newly added items and same-count replacements must survive. Moving an approved item out must not destroy it elsewhere. Do not fix this by comparing counts alone.
2. CanUnravel must reject BlessedFor as well as Blessed/Newbied for single and bulk paths. Preserve the existing intentional single-item insurance exception; bulk still skips insured items.
3. Walk locked ancestors up to the backpack using the existing ILockable protection contract. Recheck at approval, including an outer chest locked after preview.
4. Approved recovery proposal: use actual positive property intensity and cap returned shards below the corresponding minimum paid imbue cost. Permit zero recovery for tiny properties if necessary; never round a recovery floor back into shard profit. Test Basic Hit Life Leech 17 purchase and recovery together, including mastery discounts. Keep gold prices and ordinary reward probabilities unchanged unless the approved formula requires a documented adjustment.
5. Tests, red first: added item, swapped item, moved item, personal blessing, protection added after preview, locked ancestor, repeated response, exact independent shard totals, both controlled essence-roll outcomes and full destinations. The old fixture totals 8 under the old formula; derive the new expected result independently if recovery changes. Preserve documented delivery behavior without making unsupported no-loss claims.
6. Run docker/uo/build.sh -t sl-modernuo:cc-P??. Notes: notes/cc-P??-unravel-protection-recovery.md, with the approved formula, examples and regression evidence. No repair or compensation of real player inventories. End P?? DONE.
```

### U3. Tutorial loans return after splitting, conversion and restart

```text
# CC task P??: tutorial loan fix-up: no escaped materials, recovered arrows or saved skill and tithing loans
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P503 #1-#3/#7 and P523 #1 share loan ownership failures. P514 also carries P291's saved Hiding-base loan defect. Fix these together in TutorialWingTrials/TutorialTradeTrials.

1. Preserve loan identity across partial stack lifts and conversions, or refuse those operations on borrowed supplies. Cover cloth-to-bandage and log-to-board conversions. Keep the explicitly permitted finished lesson products; do not ban ordinary crafting or alter nonloan items.
2. Exclude borrowed ammunition from ordinary missed-shot recovery, or carry its loan identity through recovery. A miss followed by Stop and leaving war mode must not create sellable ordinary arrows.
3. Persist enough original Hiding and outstanding tithing-loan state to reconcile a world saved mid-trial. On cold load restore only borrowed state, once. Preserve original tithing and legitimate earned skill changes according to the existing loan contract. A relog in the same process is not a restart test.
4. Make Lend report failure. If any required supply cannot be delivered, unwind partial items, skill/stat/tithing loans and trial creatures, leave no armed impossible trial, and explain making room and retrying. Never delete a player's existing gear.
5. Tests, red first: both split halves after completion/Stop/Reset/logout/yard exit; transferred remainder; cloth/log conversions after normal cleanup and startup; recovered miss; nonloan arrows unaffected; cold-load Hiding and tithing with repeated reconciliation; full pack and failure halfway through lending; successful retry.
6. Run docker/uo/build.sh -t sl-modernuo:cc-P??. Notes: notes/cc-P??-tutorial-loan-lifecycle.md, including save versions/migrations and real-event evidence. Coordinate shared action hooks with the separate tutorial evidence fix; do not redo P480's first-play features. End P?? DONE.
```

### U4. Safe tutorial purchases and pet services; an unavailable tutorial cannot trap players

```text
# CC task P??: tutorial service fix-up: safe elixir delivery, local vet offers and coordinated exit gating
**Model:** Opus
**Touches:** server, notes tooling
**Agent:** Codex OK
**Summary:** P502 #1/#2/#4 and P514's retained P475/P480 findings remain after P480. Fix failed delivery, portable services, the unavailable-tutorial gate and the false-green play-through. P453 owns wrong-character pet claims.

1. Retain the Rangers' guildmaster identity in its elixir purchase flow. Recheck membership, buyer alive, NPC exists, same map and ordinary interaction range before charge and delivery, including a retained/reopened menu.
2. Preflight backpack capacity and use checked delivery that never drops the paid elixir on the ground. On failed delivery take no payment, or refund an already taken payment exactly once. Preserve trainer base price 500 and member price 375; do not derive expected test prices from production constants.
3. TutorialVeterinarian.Resurrect must recheck owner alive and vet/pet/owner existence, ownership, maps and service distances at confirmation. Refused/canceled/remote offers take no fee and apply no pet skill loss. Test a paying non-Young owner as well as Young, exact debit and one resurrection.
4. Coordinate TutorialIslandGate with tutorial availability. When entry is disabled, a fresh loop-zero player must have a way off the island without enrolling, skipping or granting a loop. Keep tutorial test-only; do not solve this by enabling it on live.
5. Repair N/cc-P480-tools/playthrough.py so missing companion picker or graduation box fails explicitly before checking contents. This is a verification repair, not another tutorial UI build. A farm-pet fixture must follow its own legitimate no-picker outcome rather than bypass all assertions.
6. Tests, red first: full pack with bank gold; retained purchase across distance/map/death; remote vet offer; insufficient funds/nonmember; exact prices/fees; unavailable-tutorial exit; deliberately absent required rewards make the driver fail. Run build.sh and the corrected play-through only against an isolated loopback scratch shard with scratch accounts, never the shared world. Record genuine client limitations.
7. Notes: notes/cc-P??-tutorial-services-and-exit.md. End P?? DONE. Fold P502 #3 into P453 using P533 A2, not this prompt.
```

### U5. Exodus restart state and reward integration

```text
# CC task P??: Exodus fix-up: resume the exit after restart, expire chests, honor healing and cleanup values
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P488 #1-#5 found save-state failures and missed integrations. Explain repair of inherited broken behavior in notes before changing it.

1. Persist the encounter's exit phase/deadline in saved controller state. Recreate warning, evacuation and one restart after world load. Saving in either exit phase must neither strand the encounter nor create duplicate bosses/timers. Preserve the existing elapsed-time contract.
2. Save/resume revealed locked chest expiry, or remove such loaded chests safely without granting another ritual item. Verify spawner capacity recovers. Preserve hidden chest behavior.
3. Add the held Asclepius/GargishAsclepius bandage adjustment from ServUO: +15 effective healing in the corresponding calculation. Compose it with existing shard skill scaling; do not replace that scaling or apply the bonus to unrelated healing routes.
4. Register Asclepius, BracersofAlchemicalDevastation, GargishAsclepius, GargishBracersofAlchemicalDevastation, HygieiasAmulet and ScrollofValiantCommendation at ServUO's 5,000 cleanup points each. Validate each real type, not MISSING comments.
5. Tests, red first: both cold-loaded exit phases, overdue exit, revealed locked chest reload, both held staffs versus neither, each cleanup valuation, and the separate rewarded-character persistence store refusing a fresh stat scroll after restart. That last test is preventive; P488 did not demonstrate a repeat-stat exploit.
6. Use compatible migrations, run docker/uo/build.sh -t sl-modernuo:cc-P??, and write notes/cc-P??-exodus-save-and-rewards.md. No world resets or real-player stat changes. End P?? DONE.
```

### U6. Void Pool cauldron, score records and startup cleanup

```text
# CC task P??: Void Pool fix-up: preserve cauldron charges and battle records, clean old waves before restart
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P489 #4/#6-#9 found save loss and startup races. P476 U1 already owns the unpaid reward-confirmation exploit; do not implement or draft that twice.

1. Serialize remaining CauldronOfTransmutation charges with version handling. A partly used addon reloads with that count, not zero or a refill. Explain the conservative legacy-save behavior because old payloads cannot reveal the lost count.
2. CheckBestSingle must process all players and report whether any changed. BestWave must own a score snapshot that later CurrentScore.Clear cannot erase.
3. Complete old-spawn cleanup after load before permitting a new battle. Do not use a timed blanket cleanup that can delete its first wave. Controller tracking must match surviving entities.
4. Tests, red first: partially spent cauldron save/load; two improving participants; record scores preserved after next start and after save/load; connected player during first ten seconds after load. Add real Cora death with controlled rolls, eligible/ineligible damage contributors and backpack/bank delivery.
5. Record inherited broken behavior and patch alternatives if needed. Run docker/uo/build.sh -t sl-modernuo:cc-P??. Notes: notes/cc-P??-void-pool-state.md. End P?? DONE.
```

### U7. Saved Rootdeep entry refuses a missing server overlay

```text
# CC task P??: Rootdeep server map safety: refuse unsafe saved entry when its overlay is unavailable
**Model:** Opus
**Touches:** server, docker/uo
**Agent:** Codex OK
**Summary:** P529 retains P425 #1's server-overlay risk and P504 #2's missing Young-entry proof. P411 now explicitly preserves client launch without fresh overrides, so this prompt does not block client launch or redo launcher work. P413 owns entrance geometry.

1. Protect already-saved entry when the server overlay is missing. Choose a narrow startup refusal or owned entry/use guard after inspecting the real saved route. Do not rely only on the seeder's MapBuilt check. A startup refusal can protect characters already saved inside without moving real accounts; justify the choice.
2. Preserve safe ordinary entry when the overlay exists and do not rewrite every stock teleporter. Coordinate with P413's upgrade route rather than implementing entrance geometry again.
3. Tests, red first: seed/save with the map ready, then cold load/start with overlay removed; unsafe use/start refuses clearly, and restoring the correct overlay restores normal behavior. Use real saved-state/movement evidence rather than only forcing MapBuilt in a test.
4. Add Young warning/protection transition through real entry with a test connection. Verify the normal warning exists and Young protection differs across the approach and landing without changing the chosen Young death destination.
5. Run docker/uo/build.sh -t sl-modernuo:cc-P?? in an isolated world only. No real saved-character edits, shared-shard startup, client launch changes or P411 reimplementation. P533 C16 owns the separate missing-client-map policy. Notes: notes/cc-P??-rootdeep-server-map-safety.md. End P?? DONE.
```

### U8. Decisions keep their identity, answer revision and unsaved text

```text
# CC task P??: decisions inbox fix-up: stable identity, safe take/undo, archived answers and durable drafts
**Model:** Opus
**Touches:** migration tools, docker/test-queue
**Agent:** Codex OK
**Summary:** P509 #1-#5 found answer misattachment and draft loss. No evidence says Chase's current answers are already corrupt. Preserve stored decisions and use synthetic stores for tests.

1. Give questions persistent identity separate from positional display numbers. Store and compare question revision/text when joining saved answers. On an ambiguous legacy mismatch, retain the saved answer visibly for review; never silently attach it to a different question or rewrite a docs/ source.
2. Emit unmatched stored answers as archived questions using saved question text, including temporary source loss. They remain visible to answer counts and copy/export without being mistaken for new open questions.
3. Take/undo requests carry expected answer revision and expected taken record. Check under the existing lock and reject stale requests. An old undo cannot reopen an answer subsequently taken into another prompt.
4. Preserve textarea drafts by stable decision ID through filter-chip changes, another card's save, and data refresh. Clear a draft only after its own successful save or explicit discard.
5. Tests, red first: insert/reorder/renumber questions; remove/recover source; stale answer take; delayed/repeated undo; DOM typing/filter/other-save/reload; quotes, tags, writer fields and a closing-textarea payload render literally without injected elements or events. Keep escaping helpers intact.
6. Run focused Python decision tests and an actual local DOM/browser test. If browser startup fails, report that as unverified, not passed. Use a throwaway loopback service only; do not touch Haven or current stored answers. Notes: notes/cc-P??-decisions-identity.md. End P?? DONE.
```

### W3 (urgent). Extra jewelry stays removable and obeys equipment systems

```text
# CC task P??: accessory fix-up: recover locked jewelry and integrate validation, level gear and custom imbues
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P486 F01-F09 and P482 #2 share active-extra-jewelry paths. Locked-slot removal is player loss of access, so do this before broad content work.

1. A locked row must still show its stored jewel and permit removal. Recheck ownership on responses. Eligibility changes, including League rank loss and relevant setting reloads, immediately remove effects while retaining the item.
2. Extra insertion must honor equipment restrictions and applicable CanEquip/CheckEquip/OnEquip behavior while deliberately allowing the occupied paperdoll layer. Do not bypass all checks to avoid a layer collision. Recognize supported BaseJewel ring/bracelet layers after the toe-ring exception, including set/absorption carriers.
3. Provide one active-extra enumeration for consumers. Include bought level attributes/resists/XP and custom imbue readers exactly once. Inactive or shoe-covered toe rings contribute nothing. Notify Fortune's Favor activation using the same contract as worn gear.
4. Property edits on active extra jewelry rebuild the affected skill/stat effects immediately. Shoe removal that makes the last jewelry contribution active must check achievements.
5. Tests, red first: rank-lock removal from fresh gump, rank/settings eligibility changes, blocked jewelry and special-ring restrictions, carrier jewel behavior, bracelet paperdoll-to-extra-to-inactive transitions, active/covered toe ring, XP, custom properties, Fortune timing and edited skill bonus. Exercise repeat refresh/equip/remove and combined caps at actual HCI/DCI/mana/casting/skill/stat consumers, not capped raw totals.
6. Preserve loop-slot defaults; this task does not enable dormant loop slots or implement companion equipment menus. Coordinate the shared slot counter with the level-gear fix. Run docker/uo/build.sh -t sl-modernuo:cc-P??. Notes: notes/cc-P??-accessory-integration.md. End P?? DONE.
```

### A1 (urgent addition to an existing draft). Extend P476 W5

Do not number another overlapping mini champion/Underworld prompt. Add this scope to P476 W5 before issue, or to its implementation follow-up if already started:

- P491 #1: fix repeated wrong guesses in pinned PuzzleChest through a narrow patch. ServUO uses replacement assignment. Test two wrong submissions by the same player through the real board and trap training path; prove feedback instead of ArgumentException. This is an exception, not proof of a process crash.
- P491 #2: distinguish explicitly disabled controllers from completion cooldown. Cancel pending restart even if already inactive; persist an actual pending restart and its timing rather than scheduling every inactive loaded controller. Cover disabling during cooldown and loading a disabled controller alongside P476's boss-death save test.
- P491 #3: remove matching puzzle-session keys/boards recursively on expiry and success. Preserve unrelated items and any valid other-session state; do not delete every key in the world.
- P491 #4: retain/cancel the startup callback, and guard callback/ticks against Deleted/inactive gems. Delete an activated gem before five seconds and prove no later repeating timer remains.
- Red first, compatible saves, inherited-bug explanation and `build.sh` as in the parent draft. Update its notes and tests rather than duplicating that subsystem's prompt.

## Other grouped drafts

W3 appears above because it includes player loss of access. The remaining labels keep the verdict table easy to trace.

### W1. Climbing boots recognize footing and honor travel and immobilization

```text
# CC task P??: climbing boots fix-up: real mountain footing, regional travel vetoes and paralysis
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P484 #1-#4 found three movement defects masked by fake terrain tests. P458's Eodon vine work is separate.

1. Separate current terrain classification from destination occupancy. Exclude the querying climber when recognizing current mountain footing; retain other-mobile/static collision checks at landings. Do not globally turn off destination collision.
2. Pass the player through MayLandAt to caster-aware TeleportTo travel validation for both normal hop and ledge return. Retain town/dungeon/house checks.
3. Recheck Frozen and Paralyzed when the target resolves. Refusal spends no stamina, starts no cooldown and changes no ledge memory. Do not use zero durability as a broken-boots test; these boots intentionally have no durability.
4. Tests, red first: player actually standing on mountain terrain; restrictions and pet Stay/Follow; BaseRegion allowing TeleportFrom but refusing TeleportTo; immobilization before/after targeting; pending target after removal/deletion/upgrade/death. Use the real OnDoubleClick/target path for lifecycle cases.
5. Run docker/uo/build.sh -t sl-modernuo:cc-P??. Notes: notes/cc-P??-climbing-boots-guards.md with map-backed proof and limits. End P?? DONE.
```

### W2. Level gear and imbuing share property slots

```text
# CC task P??: level gear fix-up: one property-slot count across leveling and imbuing
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P482 #1/#5/#6. Buying properties first leaves imbuing free to add another distinct property. Extra-slot aggregation is the separate accessory prompt, not duplicated here.

1. Use a shared distinct-property count for stored and level-bought properties. A property present in both counts once; raising an existing property is allowed within existing ceilings and budgets. Preserve the configured imbuing mastery slot contract and level-gear limits instead of hard-coding every caller to five.
2. Test both operation orders, overlap, raising an existing property, at-limit rejection and no charge/change on refusal through the real purchase/imbue routes. Bought bonuses remain effective only under existing wearer rules.
3. Add repair, trade, player death/recovery and isolated world-load tests asserting serial, level, XP, points, bought properties and new wearer's effective values. Same-process buffer round trips alone are insufficient.
4. Optional small cleanup: prune deleted item states on the game thread, testing the in-memory registry rather than only deserialized output.
5. Do not choose material Luck or presence policy here; P533 C1/C2 need answers. Run docker/uo/build.sh -t sl-modernuo:cc-P??. Notes: notes/cc-P??-level-gear-property-slots.md. End P?? DONE.
```

### W4. Wrong restores full spawn entries and actual capture resurrection

```text
# CC task P??: Wrong fix-up: complete XML spawns, post-death capture and safe tunnel return links
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P489 #1/#2/#5. Wrong's port truncates multi-entry XML rows, and capture resurrection executes before the ghost transition. Tunnel stranding is a source risk requiring an escape-path check.

1. Parse every :OBJ= entry from pristine ServUO RevampedSpawns/WrongRevamped.xml. Compare independent type/count/total-cap fixtures with all port definitions. Recompute capacity from source entries and MaxCount; do not copy the old 68 expectation or another note's count. Publish differing rows beside totals.
2. Defer first-capture resurrection until normal death has completed, with lifetime/map/region safety checks. Test a living player's actual Kill and timer path, plus repeated capture behavior; starting a ghost and directly calling the region is insufficient.
3. Examine destination 5868,554,15 and every tunnel destination for a usable return link and alternate exits. If return cannot be established, add the appropriate source-consistent bedroll or restrict destinations to valid paired routes. Do not claim client stranding without a walk/probe. Test full destination coverage and locked-room behavior.
4. Explain inherited broken behavior versus the XML port error. Run docker/uo/build.sh -t sl-modernuo:cc-P?? with red/green regressions. Notes: notes/cc-P??-wrong-spawns-capture.md. End P?? DONE.
```

### W5. Achievement category headings stay with their rows

```text
# CC task P??: achievement list pagination keeps category headings and repeats them on continuation pages
**Model:** Sonnet
**Touches:** server
**Agent:** Codex OK
**Summary:** P490 #1 demonstrated an orphan category heading with valid row heights. Existing tests inspect the union of headings and miss boundaries.

1. Keep a category heading with its first achievement, and render the category on continuation pages. Account for repeated heading height before packing rows, including earned/not-yet section dividers. Never expose an unearned hidden title or create an empty loop for an oversized row.
2. Red-first boundary cases: 326-pixel room with heights 26,50,54,54,54,50,54; long category spanning pages; section/category transition; hidden-only category. Assert each visible achievement occurs once, every page stays within layout rules and no heading ends alone.
3. Run docker/uo/build.sh -t sl-modernuo:cc-P??. Notes: notes/cc-P??-achievement-pagination.md. End P?? DONE.
```

### W6. Client achievement availability follows each connection

```text
# CC task P??: achievement client buttons reset enhanced capabilities on every connection
**Model:** Opus
**Touches:** client patches
**Agent:** Codex OK
**Summary:** P501 #1-#3. Only the first socket has a reset subscription, and enabled enhanced-packet IDs persist across servers.

1. Track the subscribed socket and detach/attach as sockets change. Clear button availability and enhanced enabled-ID state at connection boundaries. Derive offered capabilities only from the current server's handshake; preserve P165's login acknowledgement fix.
2. Red-first sequences: two shard logins then a server with no handshake; id 4 offered then a handshake without it; delayed negotiation; disconnect/reconnect socket replacement. Assert no stale request/visible button on unsupported servers.
3. Exercise classic paperdoll, modern menu and top-bar click routes, another character's paperdoll and missing gumps 22456-22458. Missing custom art keeps Help usable; menu/top bar can still request achievements where negotiated.
4. Build from the pinned TazUO source through client/Build-Client.ps1 with tests enabled, using isolated output. Verify patch application and packaged-client gate compatibility without publishing or launching a real shard session. Record any UI execution that remains unverified.
5. Notes: notes/cc-P??-achievement-client-connections.md. End P?? DONE.
```

### W7. Tutorial completion observes the required action

```text
# CC task P??: tutorial evidence fix-up: real hits, spells, bandages, crafts and private practice targets
**Model:** Opus
**Touches:** server, notes tooling
**Agent:** Codex OK
**Summary:** P503 #4-#6/#8 and P523 #2-#4 accept unrelated actions. P514 carries P291's catch/placement/runner findings and P475's dropped core controls. Loan ownership has its own prompt.

1. Record actual weapon/special-move hits with weapon, move and intended target. A delayed spell while a weapon or move is ready cannot substitute. Observe the requested spell's actual effect on the trial target, not a school roll and an unrelated later damage/heal.
2. Observe successful bandage completion with healer/patient identity, including self and villager in either order. Absence of a BandageContext during Heal is not evidence of a bandage; pinned removes the context first.
3. Require a successful craft by this trainee after arming, for the required product. Picking up, receiving or retrieving an old product must fail. Gathering waits for the actual requested harvest/catch; combat Lumberjacking and passive craft Arms Lore must not satisfy hands-on actions.
4. Enforce TrialOwner for the lesson goat and recover clearly if unavailable. Two trainees' prop-free lessons must not contend with a smith's anvil/forge. Allocate only needed safe prop footprints and test overlapping lessons without deleting another trial's objects.
5. Restore Options/Journal/World Map controls on the actual core trial pages for capable clients, with useful noncapable fallback. Correct N/cc-P291-tools/tradetrials.py selected reruns so completed core is not tested as a fresh character. Do not redo P480's lesson order/menu/style.
6. Red-first negative cases for every unrelated action above, followed by real valid execution. Include false Fishing skill success without catch, outsider taming, two players' simultaneous lessons and real timer-based bandaging. Keep small helper tests, but do not present them as integration proof.
7. Coordinate shared hooks with loan and P453 farm-heal work. Run docker/uo/build.sh -t sl-modernuo:cc-P??, corrected bot checks on a throwaway loopback world only, and record client-control limits. Notes: notes/cc-P??-tutorial-action-evidence.md. End P?? DONE.
```

### W8. Web console runs exactly the reviewed action once

```text
# CC task P??: web action fix-up: atomic tokens, pinned rollback target, eligibility, cancellation and audit
**Model:** Opus
**Touches:** web-console, console runner
**Agent:** Codex OK
**Summary:** P498 #1-#5. Keep using the console's Get-ActionFacts/Get-ActionPlan/Invoke-Plan; do not reimplement actions for the web.

1. Validate/consume a preview token and reserve its job atomically. Concurrent replay gets exactly one launch, even if the first synthetic job completes before the second request reaches admission. Define busy/refusal token handling explicitly.
2. Bind rollback preview to resolved image identity and relevant plan inputs. Changed target requires another preview; do not silently resolve a newer image at execution or rely only on the unchanged typed phrase.
3. Enforce multi-Golem eligibility at HTTP dispatch and the PowerShell runner, including stale pages, local/remote targets and the approved home/integrator rules.
4. Supervise the complete Windows process tree. Timeout records a timeout explicitly, terminates owned descendants and does not announce idle while an action continues. Test with harmless child marker processes, never Docker/service commands.
5. Persist a redacted start audit before changing execution and a finish/failure record afterward. Surface audit errors; do not claim a successful unlogged action. Handle interrupted jobs without inventing completion.
6. Red-first concurrent token, changed rollback, disabled multi mode, child timeout, unwritable audit and interrupted-run tests. Run focused Python web tests and Windows PowerShell 5.1 console/runner facts with stubs. No Haven, service restart, real rollback, deployment or Golem control.
7. Notes: notes/cc-P??-web-action-admission.md. End P?? DONE.
```

### W9. Kitsune art gates catch missing groups and moved hips

```text
# CC task P??: kitsune validation fix-up: required animation coverage and measured body silhouette
**Model:** Sonnet
**Touches:** art validation scripts and package gates
**Agent:** Codex OK
**Summary:** P505 #1/#2 found validation gaps, not currently missing assets. Change no artwork and generate no art.

1. Require animation 4783 actions 0,2,4 in directions 0-4 with expected frame counts 10,10,1 respectively in source validation and the package gate. Unsupported actions stay optional. A group missing entirely must fail before encoding success and when checking an archive.
2. Pin the measured SFW body alpha silhouettes or validate the actual lower-back geometry used by the fit spec. A crown-only match cannot authorize an old tail-root box after hips move.
3. Red-first scratch cases remove a complete required group and shift hips while retaining crown. Restore fixtures and prove current assets pass; never edit the committed artwork to manufacture a regression.
4. Run Python encoder/fit tests and the focused Windows PowerShell 5.1 package animation facts without shard probes. Notes: notes/cc-P??-kitsune-validation-gaps.md. End P?? DONE.
```

### W10. Fresh dependency audit and overwrite-guard proof

```text
# CC task P??: build gate fix-up: audit cached dependencies freshly and prove installer guards fail
**Model:** Opus
**Touches:** docker/uo build tooling
**Agent:** Codex OK
**Summary:** P497 #1/#2. P232's pin and audit settings are correct; a cached build can skip fresh advisory retrieval. No presently vulnerable binary is claimed.

1. Add a required audit outside cached Docker publish for the resolved dependency set. Refresh advisories and fail on audit errors/unavailable required data, honoring the existing severity policy. Keep the ordinary tests network-free and maintain build.sh as the only supported image build gate.
2. Use synthetic advisory/restore results for red-first behavior tests: cached builder plus a newly flagged resolved package fails; clean data passes; audit failure does not become success. Do not prove this by relying on an advisory appearing during a test.
3. Add isolated apply-patches.sh installer checks for missing source and existing destination. Require final nonzero exit and unchanged colliding destination. Prove these assertions fail when the relevant guards are disabled, then restore them.
4. Preserve all flat/mirrored/replacement routing and failure aggregation. Use throwaway builder/tests only under the appropriate local build lock; no live image build/deploy. Run build.sh and the focused shell checks, recording environmental failures honestly.
5. Notes: notes/cc-P??-fresh-audit-and-install-guards.md. End P?? DONE.
```

### W11. Test accounts cannot retain staff characters or expose passwords through checks

```text
# CC task P??: Golem test-account fix-up: character levels and credential-file handling
**Model:** Opus
**Touches:** server, installed Golem tooling
**Golem:** home
**Agent:** Codex OK
**Summary:** P493 #1-#3. The installed helper is outside versioned main; recheck it before editing. This task tests synthetic accounts and credentials only.

1. Validate every seeded character independently of account access level. Correct/count drift even when the account already has the desired level. Dryrun reports the same intended changes without mutating accounts.
2. Send synthetic search patterns to git grep through standard input, not command-line arguments. Test a stand-in git rejecting secret-bearing argv. Do not run the current real-key scanning fact or read actual key files to prove this.
3. Create an exact owner-and-SYSTEM ACL before plaintext credential bytes are written; reject ACL errors and remove unrelated explicit grants on reused files. Cover both failure and old-file cases with synthetic data. Preserve the intended DPAPI/local delivery contract without performing a real delivery.
4. Red-first Player-account/GM-character fixture, unchanged account with corrected character, dryrun, argv inspection, ACL failure and extra grant. Run build.sh for C# and focused Windows PowerShell 5.1 helper facts with no network/account operations.
5. If the implementing lane cannot write the installed root, finish a reviewable patch in its authorized location and state the limitation; never silently claim the kit is updated. No real account seeding, key rotation, SSH or service action. Notes: notes/cc-P??-golem-account-guards.md. End P?? DONE only for the actually assigned deliverable.
```

### W12. Tinker trusts successful repairs and has answerable questions

```text
# CC task P??: Tinker fix-up: transactional kit errors, checked repairs, remote facts and real question choices
**Model:** Opus
**Touches:** installed Golem tooling, web-console
**Golem:** home
**Agent:** Codex OK
**Summary:** P492 #1-#8. Re-read installed Kit/Tinker/Remote-Agent scripts before implementation; current source is not a versioned main artifact. Mail redaction belongs to the mail fix-up.

1. Make backup/staging/replacement/settings/rollback file errors terminating and checked through Install-Kit's actual entry point. A failed rollback must be reported as such, never all-or-nothing success. Test actual file-operation failure, not only an injected throw under a test's Stop preference.
2. WIP fix checks git add/commit exits and resulting cleanliness before clearing a flag or waking. Failure preserves the blocking state. Tests stub all Git and wake effects; do not commit real work as a test.
3. Apply fix budgets to automatic and reasoned actions. Validate response schema, allowed arguments and numeric confidence; below 0.6, missing or invalid confidence asks instead of running.
4. Judge a remote lock using target-PC facts, not absent local locks. Missing/unavailable evidence is unknown. A dead watch is recovered only with a targeted owned-watch restart and fresh heartbeat proof; equal hashes or local resync are not recovery.
5. Include missing settings keys in both kit delivery decisions even when files match. Merge additively without overwriting receiving-PC values.
6. Register Tinker questions through Questions.ps1 and the existing answer lifecycle; choices invoke the proposed action once. Add desktop/web counterparts for any new controls per P187, calling the same console functions.
7. Red-first entry-point file failures, failed WIP Git, repeated unknown stalls, low/invalid confidence, remote-held/local-free lock, dead equal-hash watch, settings-only manifest and answered-action-once tests. Use Windows PowerShell 5.1 and synthetic roots/mail/remote executors only. No real fixes, task restarts, SSH or Haven.
8. Notes: notes/cc-P??-tinker-verified-repairs.md with installed revision hashes and any unverified deployment. End P?? DONE for the assigned implementation deliverable.
```

### W13. Night shift and marathon share fresh eligibility and launch state

```text
# CC task P??: Golem scheduling fix-up: idempotent night batches, eligible wakes and fresh weekly usage
**Model:** Opus
**Touches:** installed Golem scheduling
**Golem:** home
**Agent:** Codex OK
**Summary:** P499 #1-#4 and P507 #1-#4 share wake/state paths. Recheck current installed scripts and coordinate with the Tinker fixes without running a real watch.

1. Reserve an opening/active batch under the existing lock. Repeated night triggers within and beyond two minutes must neither clear its budget/end guard nor launch another session. A refused wake cannot erase a previous batch's longRun.
2. NightShift catch-up starts only inside the configured night window. Recheck enabled state at every pending check/batch start; disabling cancels pending starts. Preserve manual rest, bot window, usage and owner-back-off restrictions.
3. Retry transient idle marathon pending wakes even without a preexisting restReason. Before every automatic launch require a fresh eligible target; when marathon turns off or hours/back-off change, no remembered target may override the new refusal.
4. Preserve source observation timestamps for usage. Duplicate/stale reports cannot manufacture a zero burn rate. Tie auto marathon state to its weekly reset and clear prior-week state before an unknown new projection is evaluated. Manual on/off remains explicit policy.
5. Fixed-clock red-first fixtures: repeat at 22:31 and 22:33 before current appears; original guard still stops on budget and 06:30 end; noon catch-up; disable before pending check; full session then reset from idle; pending wake after marathon off outside hours; repeated cached report; weekly reset with auto on/unknown projection.
6. Run targeted Windows PowerShell 5.1 P156/P200 facts with synthetic roots, usage and CLI stubs. No actual CLI sessions, scheduled-task edits, model spending, mail or remote operations. Notes: notes/cc-P??-golem-schedule-state.md with installed hashes and exact limits. End P?? DONE.
```

### W14. Golem merges preserve visible changelog text and complete both repos

```text
# CC task P??: Golem integration fix-up: comment-aware changelogs and complete two-repo receipts
**Model:** Opus
**Touches:** installed Golem integration tooling
**Golem:** home
**Agent:** Codex OK
**Summary:** P500 #1-#4 and P524 #1/#2. Re-read current Golems.ps1 and Commit-ShardWork flow. Never use a subject match in one repo as proof of a completed task.

1. Parse HTML comments throughout CHANGELOG, including version sections. Hidden headings/bullets cannot become visible additions or influence Get-NextShardVersion. Preserve main's existing text and the consumer's supported structure.
2. Include audience/section in duplicate identity. Normalize supported dash/star bullets for comparison while retaining player versus Staff announcements. Test additions under an existing heading, not only whole new sections.
3. Keep failed originals out of stale reclaim while their merge ticket/fix-up is queued, running or awaiting integration. Apply the same rule in candidate selection. Do not depend on a recent heartbeat alone.
4. Require a successful integration receipt or verified expected task branch heads in every repo the ticket changed before completing originals. One-repo tasks remain valid; a code-only partial merge of a two-repo task does not archive the original. Never reset already committed main work to hide a partial result.
5. Red-first fixtures: commented future version inside section; Staff bullet repeated visibly; identical star bullets; existing-section addition; unreadable input with both fixture repos restored and no merge left open; aged original before fix-up; code merged/docs outstanding; one-repo and complete-two-repo success.
6. Use Windows PowerShell 5.1, mocked Git or disposable synthetic fixture repos and no real integration, pushes or branch changes. Record unverified end-to-end paths if fixture setup cannot run. Notes: notes/cc-P??-golem-integration-receipts.md. End P?? DONE.
```

### W15. Email queues survive delivery failures and diagnostics are truthful

```text
# CC task P??: Golem and bot mail fix-up: durable batches, redacted diagnostics and soak failures
**Model:** Opus
**Touches:** installed Golem mail tooling, playtest-bot
**Golem:** home
**Agent:** Codex OK
**Summary:** P506 #1-#5 plus P492 #9. Do not duplicate P476 W18's Away-mail work or P410's existing routing findings.

1. Claim routine mail batches durably and acknowledge them only after successful delivery. Keep/restore failed batches and preserve updates beyond 30 for subsequent delivery or an explicit complete summary. Handle concurrent additions and process interruption without dropping old messages.
2. Return meaningful sender success/failure instead of deleting a batch before a void sender call. Preserve both direct fallback and Tinker/outbox routes. Do not infer real SMTP delivery from a formatter test.
3. Apply common credential redaction to subject, body, question/model text, forwarded event bodies and logs. Keep useful path diagnostics under Details; plain sections should use short human descriptions. Test Windows paths containing spaces and extensionless paths. Formatting cleanup alone is not secret filtering.
4. Bot crash mail uses an approved short opening and redacted diagnostics. Soak-only failures must affect the opening and What to do, even when individual checks pass; no Nothing to do success for a failed soak.
5. Red-first failed-send/retry, 31-plus events across batches, concurrent append, interrupted claim, old-note fallback, Tinker question/log forwarding, credential-bearing synthetic exception and passing-checks/failed-soak cases. No real credential files, mailboxes or SMTP.
6. Run focused Windows PowerShell 5.1 formatter/queue facts and Python bot email/report tests with sender stubs. Notes: notes/cc-P??-mail-durability-and-diagnostics.md. End P?? DONE.
```

### W16. Failed code reload restarts cleanly instead of serving mixed modules

```text
# CC task P??: test-queue reload fix-up: never reopen requests on partly updated tools
**Model:** Opus
**Touches:** docker/test-queue, migration tools
**Agent:** Codex OK
**Summary:** P495 #1. importlib.reload mutates modules in place, so reporting old code and returning True after failure is incorrect.

1. After a reload exception, keep requests drained and enter the controlled process-restart path instead of reopening mixed modules. Report restart required accurately. Do not advance the watcher's loaded fingerprint as successful. Preserve bounded drain/refusal behavior when work is still running.
2. Red-first tests use two modules: first changes, later fails; and one module changes globals before raising. Assert no subsequent request serves mixed state, the service restarts/reinitializes coherently, and unchanged/new successful code works. Also cover failure during dependent verifier initialization.
3. Run focused codereload/gate/service tests through a disposable loopback server with mocked restart where needed. This edits service source only; do not connect to Haven, restart a deployed service or alter service inventory for an unchanged service topology.
4. Notes: notes/cc-P??-safe-tool-reload.md with actual service-test results and environment limits. End P?? DONE.
```

### W17. Ankh survey and ghost context actions match real resurrection

```text
# CC task P??: ankh fix-up: honest resurrection survey and usable ghost context action
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P495 #2/#3/#5/#6. Rejuvenation and Despise ankhs are useful interactive objects but not resurrection sources. Shrine-offer portability is a separate policy question.

1. Classify true resurrection heads/halves separately from rejuvenation and WispOrb ankhs. Seeding must not skip a required resurrection source merely because one of those other objects is nearby.
2. Include standalone working heads in actual Sightings enumeration. Deduplicate static/item sightings at the same map/location while retaining their useful classification; do not test by supplying already constructed sightings alone.
3. Patch pinned Ankhs context entry to enable resurrection for ghosts, with the normal living tithing behavior retained. Test enabled states and the real context response handler, not direct OnClick that bypasses Enabled.
4. Red-first classification, standalone/deduplicated survey and ghost-menu tests. Add accepted resurrection on a standable surface, cancel, region veto, living refusal and positive fame's 10 percent loss only on successful resurrection. Keep AOS murderer policy unchanged.
5. No generic ResurrectGump rewrite unless P533 C5 is approved. Explain upstream defect/patch alternatives, run docker/uo/build.sh -t sl-modernuo:cc-P?? and write notes/cc-P??-ankh-survey-context.md. End P?? DONE.
```

### W18. Staff map tools preserve exports and bound their input work

```text
# CC task P??: map-check tools fix-up: safe targets, independent exports, unique reports and bounded parsing
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P508 #1-#7. Keep intended staff/live read reach and test-only overlays; no real staff command execution or deployment is needed.

1. Recheck GM access in point and bounding-box callbacks before reading/writing/changing anything. Normalize item/mobile targets to world coordinates, or reject unsupported targets consistently with the prompt. Never export backpack-local coordinates as map coordinates.
2. Key point lists by staff and export name, with explicit facet handling. Returning alpha/beta/alpha preserves alpha; clear beta cannot clear alpha. Allocate report files with exclusive unique creation even within the same clock tick or across staff members.
3. Validate JSON kinds and TryGetInt32 per coordinate. Report malformed rows and continue valid ones instead of converting all results into a read error.
4. Bound input bytes before full read, total parse work and stored malformed diagnostics as well as accepted spots. Explain truncation/refusal. A 500-accepted-spot limit is not a memory bound.
5. Red-first demotion after targeting, contained-item target, export-name/facet switching, same-clock report writes, malformed rows between valid rows and oversized input refused before full processing. Add elapsed timer and loaded-marker deletion tests without calling DeleteAll; prove cleanup assertions fail with each hook disabled.
6. Run docker/uo/build.sh -t sl-modernuo:cc-P??. Notes: notes/cc-P??-map-tools-input-and-exports.md. End P?? DONE.
```

### W19. Console queue notes use the claimed file and skip metadata

```text
# CC task P??: queue display fix-up: read claimed prompt summaries and ignore all metadata before prose
**Model:** Sonnet
**Touches:** scripts/Shard-Console.ps1
**Agent:** Codex OK
**Summary:** P510 #1/#2. Use the existing Find-HandedPromptPath route already used by Open prompt.

1. Get-GolemExtra reads the actual running claimed file, preserving its Summary and actual model. Use the existing lookup/cache contract rather than a second folder search.
2. No-Summary fallback skips Touches, Agent, Lane tests, Golem and other prompt metadata before collecting the opening prose. Preserve explicit summaries and documented unreadable fallback.
3. Red-first claimed Fable prompt checks desktop/exported note, model and gray state; no-Summary prompt with current metadata checks the real prose. Run focused Windows PowerShell 5.1 P125/P153 queue/status facts. No live Golem actions or new buttons.
4. Notes: notes/cc-P??-queue-notes-lookup.md. End P?? DONE.
```

### W20. Package validation ties tested client provenance to its actual files

```text
# CC task P??: package client fix-up: validate archived provenance, binary hashes and required test results
**Model:** Opus
**Touches:** client build, player-package
**Agent:** Codex OK
**Summary:** P511 #1-#3. A current sl-build.txt is not enough to identify the assembly beside it, and CheckZip skips even that validation.

1. Record required published client files and hashes after a successful build, alongside pin, ordered patch hashes and required client-test outcome. SkipTests may produce a development build but must be unmistakably unshippable. Older stamps may still be readable for display; they cannot silently satisfy stronger shipping proof.
2. Validate required assemblies and hashes before staging, after copying and inside CheckZip against the current pin/patch contract. Missing/stale/extra/reordered patch records and missing/replaced assemblies must fail even when archive sidecar hash/size are internally consistent.
3. Red-first synthetic client/archive fixtures for every refusal, tested versus skipped builds, and a good complete manifest. Keep current native-import/ASCII/vendor gates. Hashes establish consistency with builder output, not an externally signed security attestation.
4. Run Windows PowerShell 5.1 Package-Client facts and isolated builder-stub tests, then a local tested client/package validation if resources allow. Keep outputs below repo limits in proven ignored scratch and do not publish, contact a shard, or inspect remote packages.
5. Notes: notes/cc-P??-package-client-provenance.md with exactly what was built versus stubbed. End P?? DONE.
```

### W21. Initial evo body choices reach the owner

```text
# CC task P??: evo appearance fix-up: offer the initial Horse and Lizard body picks
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P521 #2/#3. Initial stage variants exist but only later-stage choices are offered. Existing achievement mount backfill remains Chase's separate decision.

1. Offer an unmade current-stage choice when the pet is given and on owner double-click after closing it. Coordinate hue/body selection so one gump does not discard the other. Apply the chosen current body immediately and persist the choice. Nonowners cannot choose; dead pets follow existing restrictions.
2. Red-first owner-flow tests for every initial Horse/Lizard option, closing/reopening, repeated replies, nonowner refusal and save/load. Do not substitute StaffSetStage for player choice or change stage XP/loop/Bond Trial gates.
3. Add isolated owner/mount/mount-item/stable load and unused RewardMountStatuette reload followed by exactly one redemption. This closes P521's coverage gap without alleging a demonstrated mount duplication bug.
4. Run docker/uo/build.sh -t sl-modernuo:cc-P??. No real reward backfill or account changes. Notes: notes/cc-P??-initial-evo-picks.md. End P?? DONE.
```

### W22. Register pages expose every guild and clear reset bindings

```text
# CC task P??: League Register fix-up: full-guild paging, accurate ranks and reset-time binding cleanup
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P515 found current UI truncation and reset integration outside P451's repair/satchel fixes. Keep the shared book/action-catalog build out of this correction.

1. Page bound guilds, available bindings and ledger rows so every joined guild remains reachable at supported Register capacities. Keep controls within the frame and revalidate response indices/ownership as membership changes between pages.
2. Render rank from the actual guild-rank helper, not reputation alone. Show the current next-promotion requirements from existing rules without inventing top-rank trials.
3. Clear the reset guild's bound key during ResetGuild/DoReset, not only on next Register open. Reset followed by rejoin before opening must not retain the old binding. Preserve other guild bindings and record order.
4. Red-first all-guild/high-capacity page enumeration with no omissions/duplicates; late-page actions after membership change; promoted-rank mismatch; reset/rejoin. Run docker/uo/build.sh -t sl-modernuo:cc-P?? and coordinate shared files after P451 if it has started.
5. No Warehouse, Featherweight, replacement BOD-book product or broad turn-in engine. Notes: notes/cc-P??-register-paging-reset.md. End P?? DONE.
```

### W23. Emptying a raised mound does not create a bowl

```text
# CC task P??: raised garden fix-up: mound-aware emptying and plant-gump presentation
**Model:** Sonnet
**Touches:** server
**Agent:** Codex OK
**Summary:** P519 carries P260's incomplete raised-bed port interaction. P128 added mound virtuals, but pinned EmptyTheBowlGump still always creates a PlantBowl. No Herbalism subsystem is required.

1. Compare actual ServUO mound handling in EmptyTheBowlGump/MainPlantGump with pinned and the current plant hooks. Add the smallest behavior/presentation hook preserving stock bowls and owner/co-owner checks. Do not copy unrelated newer plant systems.
2. Red-first real emptying-gump response on a mound, including seed-return stage and capacity refusal; assert no invented bowl, correct mound/plot link cleanup and ordinary seed behavior. Test stock bowl emptying remains correct, plus cancel/distance/access refusal.
3. Do not add reagent plants, new upkeep, strain fields, familiar access or art. Explain patch alternatives, run docker/uo/build.sh -t sl-modernuo:cc-P?? and write notes/cc-P??-raised-mound-emptying.md. End P?? DONE.
```

### W24. Progress dry run really is read only

```text
# CC task P??: progress reporter dry-run fix-up: suppress all generated writes without monkey-patching
**Model:** Sonnet
**Touches:** migration tools
**Agent:** Codex OK
**Summary:** P525/P526 and the reviews repeatedly found progress.py build() writing tools/progress.json before main checks --dry-run. Keep ordinary regeneration intact.

1. Separate report computation from artifact writes or pass an explicit write mode through the builder. --dry-run prints the report and changes no progress JSON, README or dashboard output. Ordinary mode still updates the intended files with existing behavior.
2. Red-first temporary-work-copy invocation records bytes, existence and timestamps of generated outputs before/after dry run, including initially absent outputs. Test ordinary mode separately and a computation failure that leaves old artifacts intact. Exercise the real CLI path rather than replacing Path.write_text.
3. Run focused Python reporter tests and both invocation modes only in synthetic copies. Do not rewrite docs/ or real project status as a test side effect. Notes: notes/cc-P??-progress-read-only.md. End P?? DONE.
```

## Additions to existing work, not new numbered drafts

### A2. P453 owns the graduate character's pending companion

Add P502 #3's concrete regression to P453: graduate A leaves its saved choice pending; character B on the same account sees no offer/reminder and cannot claim through a retained reply; A can still claim once after reload. Apply CharacterSerial to reminder, visibility, offer and claim. P480 already made the picker reopenable, so do not build that feature again.

### A3. Existing hall repair owns repeat-placement omissions

P476's Not drafted section points P463 work to P477 O2. Extend that owner, rather than P459's distinct decor template/tower work, with P514/P516's retained P281 findings:

- Find existing BaseDoor by closed position, accounting for Open/Offset; reseeding with every front door open creates none and preserves links. Dryrun never relinks.
- Reconcile a new visible stock Sign even if the guild sign already exists. Cover SignGen replacement, rerun and clear without deleting unrelated signs/NPCs.
- N/cc-P281-tools/gen.py passes its selected checkout/input paths to check.py. A valid Iron checkout cannot authorize invalid selected data. Test the real halls.json instead of a C# copy.
- P459 already includes walkable towers from Chase's October 23 answer. Do not ask whether they should have real doors again, or assign them to halls without a layout choice.

### A4. Optional addition to P457's achievement routes

P528 notes that Sacred Journey and scissors recycling lack the corresponding notification paths. Add them only if the broader displayed contract is retained, using real successful actions and Chase's accepted recycler-own-craft-or-loot provenance rule. Existing P457 combat/history/ground/mining/range/follower fixes and P454 large quick-commission work are not new drafts. Keep hidden trigger details out of player-facing summaries.

## For Chase

These are recommended answers, not approvals recorded by this task. They are nonblocking for the other drafts. Decisions already made in the October 23 League block stand: six named milestones, delivered shop, no published AP ceiling/title count, built Lead semantics, immediate requisition standing, no Warehouse/Featherweight, and the Clockwork Scavenger retained.

| ID | Decision | Recommended answer |
|---|---|---|
| C1 | Should bought Luck include material Luck under the per-item ceiling? P482 #3. | Yes: count material Luck in the item baseline before buying and test normal/exceptional gold. Do not claim a wearer-total cap defect. If enchantment-only was intended, clarify wording instead. |
| C2 | Must gear-XP contributors remain present? P482 #4. | Require owner alive, connected, same map and within the existing ordinary loot-rights range of the victim at award. Apply it to direct and pet credit; verify the pinned range rather than inventing one. Do not change the separately deferred XP floor/rate design. |
| C3 | Should major flying loot be visible through concealment/walls? P483/P528. | Filter public recipients by CanSee and InLOS while always preserving the opener's own valid effect. Then require actual packet-recipient tests and full-pack/full-bank reward preservation. This changes an audience policy; do not infer a stolen-item exploit. |
| C4 | Approve bounded intensity-based unravel recovery? P494 #3. | Yes: recovered shards must remain below the minimum corresponding imbue cost, including Basic/mastery cases; allow zero for tiny properties. Keep gold prices unchanged. U2's destructive-protection fixes can be issued while the exact formula waits. |
| C5 | Should ankh offers require returning to their source? P495 #4. | Yes, after a real retained-offer reproduction: retain the shrine and recheck ghost state, source existence, map and range at acceptance. Scope the change to shrine offers, preserving other resurrection types and region vetoes. This is inherited behavior, not P137's introduction. |
| C6 | Should pre-P365 achievement earners get mount rewards? P521 #1/P526. | Prefer an explicit durable one-time claim for eligible earners, without regranting AP/Renown or replaying achievements. Approve that policy before a separate claim draft; no automatic real-account compensation pass here. Preserve the no-world-reset rule. |
| C7 | Connect existing tutorial loop 1 to evo, companion and accessory providers now? | Yes, as a small separately approved integration using the one canonical per-character loop record. Keep loop-slot enable defaults unchanged. Do not pretend later loops, reset/XP, Bond Trial, companion personality mapping or later rank calibration are already built. Companion-boss achievement wiring belongs with genuine kill attribution/owner participation. |
| C8 | Should wearing Focus gear stop base gains at early certainty? P518. | No. First reproduce +15 Focus near base 185/199.9 in a controlled resource state, then make only the gain-chance input bonus-safe. Preserve effective regeneration strength and avoid another global gain-rate increase. |
| C9 | Mount/loot availability, Tamer box source, red dragon stats/routes and veteran interval? | Keep all unverified routes labeled draft. Choose an actual gameplay Tamer source before promising its tier 5/6 mount pool. P455 fixes boss death; do not queue that again. Keep staff-only red dragons until acquisition/balance is chosen, and require client riding proof before publication. Do not silently approve P365 proposal prices/stats or change veteran timing. |
| C10 | Finish every Register turn-in route and missing book action now? P515. | Keep P451's specified repair first; schedule remaining subsystem routing with P178's shared action catalog. Use each subsystem's real turn-in method. Do not build a second BOD book where mixed-craft storage already exists. Paging/reset corrections W22 can proceed independently. |
| C11 | Mule payment risk and advertised unfinished module effects? P515. | Probe the payment helper with real count/consume rules before asserting free upgrades. Prioritize a reachable failure if found. Track missing gem proc, bandage range, dismount resistance, socket filling, sorting and Scavenger redirect as F-33 follow-ups, not another mule framework. First Haul waits for jobs. |
| C12 | Hall deployment/layout choices? P516. | Finish existing repeat-placement repair and P459 first. Then choose tower attachments, League officer identity and Royal City replacement, Alembic lab space and Maritime's surveyed dock footprint. P268's assessment does not prove a naval engine is required for a dockside hall. Place only through a separately authorized test-world action. |
| C13 | Herbalism and its inherited questions? P519. | Keep P260/P392's question IDs as the single design decision list. Follow P519's narrower recommendations: reuse skill writer, separate reagent strains/pollen, preserve stock bowls/beds, keep stock pickups, and use owner-authorized worker/claims paths. Fix mound emptying W23 independently; no duplicate Herbalism build or fresh art request is needed for this correction. |
| C14 | Achievement/loot scope, replay, placeholders, novelty sources and balance guarantees? P528. | Preserve account-wide AP/Renown grants. Design offline/pending reward delivery and per-loop observations explicitly without regranting currency/boxes. Keep known replacement-joke-box and mute defaults until changed deliberately. Replace labeled placeholder rewards with real owning-system items only under approved scope; do not promise weaker-than-crafted gear without an independently defined comparison. Hunter resource scaling needs a chosen relevant skill. |
| C15 | Rootdeep remaining content and Young death destination? P529. | Keep existing P24/P36/F-45 backlog. Fix U7 and P476 Vault recovery first. Retain stock Young death routing until a separate decision approves Landing resurrection; an ankh's presence alone does not provide that route. P413 owns the entrance upgrade, not these encounters. |
| C16 | How should a client without the required custom map be protected while honoring P411's always-start requirement? P504 #1, updated for the new merge. | Keep P411's launch-with-last-good-or-none behavior. First prove missing/outdated map impact in an isolated client/world. Then prefer a narrowly scoped custom-area access/capability safeguard or explicit recovery flow if needed; do not queue a launcher hard stop or claim P411 fixed map compatibility. Map input diagnostics can improve without blocking launch, but a new capability protocol requires its own approved scope. |

## Evidence, inventory and verification limits

Numbered code-review source files read:

```text
cc-P482-review-levelable-gear-build.md
cc-P483-review-flying-loot.md
cc-P484-review-climbing-boots.md
cc-P486-review-accessory-slots.md
cc-P487-review-companions-b1-base.md
cc-P488-review-exodus-encounter.md
cc-P489-review-wrong-and-covetous-void.md
cc-P490-review-achievement-category-icons.md
cc-P491-review-underworld-mini-champions-2.md
cc-P492-review-tinker-golem-watchdog.md
cc-P493-review-golem-test-accounts.md
cc-P494-review-artificers-unravel-container.md
cc-P495-review-usable-ankhs.md
cc-P496-review-props-ability-profile.md
cc-P497-review-pkcs-pin-drop-audit-flag.md
cc-P498-review-web-console-parity.md
cc-P499-review-marathon-mode.md
cc-P500-review-changelog-version-merges.md
cc-P501-review-achievements-button.md
cc-P502-review-tutorial-first-play-fixes.md
cc-P503-review-tutorial-wing-combat-magic.md
cc-P504-review-rootdeep-goes-in.md
cc-P505-review-kitsune-paperdoll-refit.md
cc-P506-review-plain-english-emails.md
cc-P507-review-night-shift-batches.md
cc-P508-review-vseuoaware-staff-commands.md
cc-P509-review-playtest-decisions-inbox.md
cc-P510-review-queue-notes-and-package-whats-new.md
cc-P511-review-package-builds-from-tazuo.md
cc-P521-review-reward-mounts-evo-stages.md
cc-P523-review-tutorial-trades-wing.md
cc-P524-review-golem-fixes-flaky-builds.md
```

Also read P522's skipped-review note; P512/P513 planning/patch notes; P514's full feature audit; P515 League report; P516 hall report; P517 F-12 report; P518 skill-path report; P519 Herbalism report; P525/P526 guide work records; and P528/P529 design/build reports. Their exact filenames are those named by their adjacent work-record links. No additional findings were extracted from their review-of-notes wrappers.

The source checks read current failure branches and relevant test fixtures, followed inheritance into pinned ModernUO, and searched canonical customizations/patches for alternate providers/consumers. A missing name alone was not treated as missing behavior. Examples independently checked include transfer bond clearing and loyalty release, mobile-before-item load order, PuzzleChest insertion, map-only travel validation, paid-elixir fallback, loan split/conversion/recovery paths, ankh context Enabled, plant emptying, module payment preflight and the actual decision joins.

Installed source fingerprints at inspection:

| File | SHA-256 |
|---|---|
| G/golem.ps1 | 36310DFF636F35E07EC98D1CFAEDC44F272E37199373F9F1BC66A781BBB304F4 |
| G/Golems.ps1 | 4047692F91514FAF4CD72233182ADBE1E8641BCAA89D0D4A152F79937145A100 |
| G/TinkerLib.ps1 | 34F1D8A928EDE62CF8EA24E6BE55E81A0D087A4C5A6538E09C838AA4EB05B8B7 |
| G/Kit.ps1 | F20E7B6A2A0BEAD8C3EBCEB73B769F019DFD7BABC8A191A808C512D0C23B5638 |
| G/GolemMail.ps1 | 521496F4F1547DC7349A92325CF0C58D06F3FC4DE7DE7B2479ADBEA30D953F73 |
| G/TinkerMail.ps1 | 0211675A539254C47A1BCC6CEB957C5C0A26AB25C3D2FD506239249A9F14D192 |
| G/GolemTestAccounts.ps1 | E6B09BEF2268D1C35422DBB5962C0BB803C87E5EE1C4C3CF623446AF309C5E80 |

External files were read only, without executing their hooks, fixes, senders or remote operations. Current source differs from some original review hashes; the relevant failure branches were re-read instead of assuming identical files. This does not establish deployed behavior on any other PC.

No build, gameplay test, client session, save/restart experiment, SMTP delivery, real-account check, network connection or Haven action was performed. Earlier reviews' probes and test results were read, not rerun or claimed as P533 passes. Runtime impact, map escape routes, actual public effect rendering, active settings and existing player damage remain unverified. Test-gap rows are deliberately not promoted into demonstrated exploits. No code, docs/ files or queue prompts were changed.

Final editorial checks passed: complete finding IDs and source inventory, draft ownership, table columns, local citation paths, links, ASCII punctuation, code fences, whitespace and file sizes. The read-only progress run completed with its known JSON write suppressed in memory. The code work copy is clean; only this report and the companion work record are new in the notes work copy. No further P533 work remains.

P533 DONE
