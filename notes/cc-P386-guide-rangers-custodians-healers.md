# P386: player guide to the Rangers, Custodians, and Healers

October 21, 2026. Docs-only draft, prepared in the Golem's Verite work copies. No code, test, configuration, save, service, or world changes. No Haven connection, deployment, build, commit, merge, push, or branch switch.

## Deliverable and scope

- `notes/wiki-drafts/rangers-custodians-healers.md`: one new-player guide, with Sources and Contradictions at the end.
- This work note: source evidence, omissions, contradictions, and verification limits. Code citations stay here, not on the page.

The page covers joining and chapter locations, Ranger Archery and Tracking, field contracts and starter tools, the proposed Rangers' Guild hall, Clean Up points and the Sanitation Warden, Healing, and resurrection. It distinguishes source defaults from verified running settings. Only built behavior and recorded decisions are advertised; the headquarters, travel stops, trials, and pet-gain loop contribution are marked `(planned)`.

The source snapshots were ShatteredLegacy `2d9fea4`, shard-migration `2e6be5b`, and read-only ModernUO `d4531cd94b739613155225c234900de9f47d2c88`. Both work copies were clean initially. Work-copy paths replace the brief's shared checkout paths throughout this task.

## Agreements and reading

Read both work-copy `AGENTS.md` files before work, plus `docs/direction-decision.md`, `docs/README.md`, and the task-list context. Read the model pages `notes/wiki-drafts/league.md` and `society-of-smiths.md`. Used `docs/feature-queue.md` for decisions, particularly F-3, F-9, F-20, F-33, F-47/F-48, and F-49. No `docs/` file was edited.

Searched every top-level `notes/cc-P*.md` for Ranger, Custodian, Healer, Sanitation Warden, Clean Up Britannia, Healing, Tracking, Archery, and resurrection references. Read the relevant subject sections, following historical claims forward into current code:

| Notes | Subject used |
|---|---|
| P14, P15, P18, P23, P29, P48, P52, P77 | Guild mapping, free joining, character storage, starter records, rank display, and the Alembic split |
| P33, P56, P57, P175 | Clean Up's original port, bag menu label, replacement of Civic Tokens, updated property and corpse valuation, and store expansion |
| P17, P32, P42, P137, P141, P189 | Healer spawn history, movement-based resurrection, ankhs, and New Haven/Old Haven distinctions |
| P20, P25, P54, P66, P71, P171, P172, P191, P283 | Historical skill ceilings versus current hooks, Tracking radius, scaled bandage healing, taming context, and pet gains |
| P47, P70, P78, P150, P151, P177, P179, P212, P217, P235, P236, P265 | Contracts versus proposals, requisitions, future halls, mockups versus live menus, mule context, and later surveys |

Incidental hits about a creature's Archery stats, infrastructure tracking, third-party packages, companion-class research, and other wiki-guide tasks were not treated as evidence for a guild feature. P212's proposed taming BODs were not advertised as built or as a settled design. P177's mockup rewards and layout were not treated as the real shop. P235's mining/wood rebalance proposal did not replace the Ranger contract values in source. P265 explicitly describes unplaced decor, not finished headquarters.

`rg` was unavailable in the shell. Used `git grep`, `Select-String`, and explicit file reads instead. The recursive instruction-file discovery encountered denied access in unrelated ignored `notes/__pycache__/p378-test-temp/` directories; neither deliverable is inside those directories. The tracked instruction files in both repositories are the root `AGENTS.md` files.

## Current code evidence

Paths in this section are relative to ShatteredLegacy unless prefixed `ModernUO/`. ModernUO means the read-only pinned tree's `Projects/UOContent/`. Citations are source inspection, not runtime verification.

### Joining, starter items, skills, and locations

| Page claim | Source |
|---|---|
| Membership belongs to the character; joining has no skill or tribute check | `server/customizations/ClusterFGuildSystem.cs:309`, `:314`, `:427` |
| Apprentice task uses base skill, consumes tribute only if the skill half fails, pays once | `ClusterFGuildSystem.cs:333`, `:382`, `:400`, `:412` under `server/customizations/` |
| Healers' task: Healing 50 or 25 Bandages; pays 25 standing / 10 scrip | `server/customizations/ClusterFGuildSystem.cs:145` |
| Rangers' task: Archery 30 or 25 Arrows; pays 25 standing / 10 Trail Marks | `server/customizations/ClusterFGuildSystem.cs:195` |
| Custodians' task definition has no skill requirement and pays zero standing/scrip | `server/customizations/ClusterFGuildSystem.cs:245` |
| Guild skills: Healers are Healing/Anatomy, Rangers have their seven wilderness skills, Custodians no skill | `server/customizations/ClusterFGuildStarterPath.cs:48`, `:51`, `:64` |
| Healers' and Rangers' signature quest rewards | `server/customizations/ClusterFGuildStarterPath.cs:98`, `:99`; P14 maps the quest classes to Tunic of Guarding, Healer's Touch, Heartseeker, and Walker's Leggings |
| Current chapter posts | `server/customizations/ClusterFGuildStarterPath.cs:214`, `:215`, `:225`: Healer's Hall, New Haven stables, upstairs civic hall |
| Tools are issued once, deduplicated by type across skills, with the guild join bonus | `server/customizations/ClusterFGuildStarterPath.cs:290`, `:303`, `:324` |
| Healers' current kit is 50 bandages, scissors, race-appropriate robe; Anatomy's 3 extra bandages are deduplicated | `server/customizations/CharacterCreation.cs:967`, `:1140`; skill order above; `server/tests/Misc/AlembicGuildVerification.cs:151`, `:158` |
| Rangers receive crook and satchel | `server/customizations/ClusterFGuildSystem.cs:475` |
| Signature claim shares quest completion state; first claim has no skill task | `server/customizations/ClusterFGuildStarterPath.cs:335`, `:405`, `:436`; F-9 explicitly excludes quest acceleration from the guild route |
| General rank recognizes Apprentice completion | `server/customizations/ClusterFGuildSystem.cs:672`, `:690`; Ranger ladder `:728`, generic Healers ladder `:749` |
| Directory contracts and guild requisitions are accessible | `server/customizations/ClusterFGuildSystem.cs:959`, `:1013`, `:1187`, `:1243` |

The `ClusterFGuildSystem` free-join documentation says Initiate universally, but the actual Ranger initial rank is Wanderer and the Warden uses Volunteer or the preexisting lifetime rank. The page uses each guild's actual ladder. No craft-guild skill promotion thresholds were imported into these non-craft guilds: `server/customizations/ClusterFGuildPromotion.cs:101` returns for non-craft owners.

### Rangers, Tracking, and Archery

| Page claim | Source |
|---|---|
| Member dashboard, Field Contracts link, Trail Marks, standing ladder | `server/customizations/OutridersGuildmasterGump.cs:204`, `:226`, `:276` |
| Early deliveries are leather/game; further field and taming orders have standing/skill gates | `server/customizations/ClusterFWorkOrderSystem.cs:1394`, `:1399`, `:1414`, `:1431`, `:1763` |
| Contract acceptance checks membership, eligibility, and per-guild limit | `server/customizations/GuildContractLedgerGump.cs:448`, `:489` |
| Resource turn-in consumes requirements and pays standing, currency, and gold | `server/customizations/GuildContractLedgerGump.cs:521`, `:542`, `:547`, `:550` |
| Three active orders per guild | `server/customizations/ClusterFWorkOrderSystem.cs:342`; enforced in the ledger acceptance path above |
| Crook is blessed, needs backpack for actions; starter bonuses 5 Taming / 5 Peacemaking | `server/customizations/OutridersCrook.cs:45`, `:79`, `:124`, `:133` |
| Pet delivery requires own following pet and active matching contract; permanently removes pet | `server/customizations/OutridersCrook.cs:146`, `:168`, `:205`, `:218` |
| Shrinking and bonding have actual target paths; bond requires own, unbonded, tamable pet, starter cooldown 48 hours | `server/customizations/OutridersCrook.cs:239`, `:277`, `:311`, `:317`, `:48`; `server/customizations/ShrunkPet.cs:39` |
| Satchel acceptance, supported hide conversion, 30-percent weight reduction, blessing | `server/customizations/HuntersSatchel.cs:34`, `:67`, `:79`, `:109` |
| Automatic routing reaches carved resources and backpack insertion | `server/customizations/ClusterFHuntersSatchelHooks.cs:35`, `:74` |
| Archery uses bows/crossbows and matching ammo; ordinary movement pause | `ModernUO/Items/Weapons/Ranged/BaseRanged.cs:27`, `:34`, `:40`, `:168`; `ModernUO/Items/Weapons/Ranged/Bow.cs`, `Crossbow.cs` |
| Tracking category selection, target list, arrow | `ModernUO/Skills/Tracking/Tracking.cs:36`, `:110`, `:125`, `:148`, `:374` |
| Tracking radius uses at most skill 100, hence 110 tiles | `server/patches/Tracking-radius-osi.patch:7`; `server/customizations/ClusterFSkillClamps.cs:82` |
| Tracking and Healing keep gaining above stock ceilings on the recognized uses | `server/customizations/ClusterFSkillGain.cs:350`, `:382`; qualifying-use and cap checks in `PastStockCeilingChance` |
| Rangers' member rank and Taming/Lore improve controlled pet gain chance; loops are a stub | `server/customizations/ClusterFPetGainSpeed.cs:45`, `:57`, `:68`, `:75`; `server/patches/SkillCheck-pet-gain-speed.patch`; P172 |
| Requisition interests and separate payout | `server/customizations/Requisitions/RequisitionTable.cs:264`, `:274`; `RequisitionSystem.cs:218`, `:249`, `:253` in that directory |

Did not promise a general Trail Mark store: the Outriders' reward text describes one, while the actual dashboard exposes contracts, replacement tools, and the mule exchange. Did not advertise T2/T3 tool acquisition, universal item-capacity numbers, or Peaceful Approach/Peaceful Taming. P49 already records the missing taming consumer, and `ClusterFRangersSystem.HasPeacefulTaming`'s descriptive comments alone cannot establish that behavior. No exploit mechanism or hidden-achievement information is on the page.

### Custodians and Clean Up

| Page claim | Source |
|---|---|
| Ranks 0 / 25 / 125 / 500 / 1,250; commands require membership; 10-tile radius and 60-second cooldown | `server/customizations/ClusterFCustodianSystem.cs:41`, `:47`, `:98`, `:348` |
| Eligibility protections distinguish loose items, player corpses, monster corpses, and containers | `server/customizations/ClusterFCustodianSystem.cs:115` |
| Points and corpse contents | `server/customizations/ClusterFCustodianSystem.cs:155`, `:163` |
| Standing synchronized to floor(lifetime), not spendable balance | `server/customizations/ClusterFCustodianSystem.cs:192`, `:206`; `server/customizations/Services/PointsSystems/CleanUpBritanniaData.cs:94` |
| Earned corpse base Fame x 0.001, parties, no pet/summon base, no record means no base | `server/customizations/Services/CleanUpBritannia/ClusterFCorpseValue.cs:39`, `:75`, `:83`; P175 dragon example; existing corpse verification examples |
| Equipment property weight excludes player-crafted gear | `server/customizations/Services/PointsSystems/CleanUpBritanniaData.cs:294`, `:316` |
| Ordinary barrels credit on destruction; appraisal does not destroy the item | `server/customizations/Services/CleanUpBritannia/CleanUpTrash.cs:42`, `:86`, `:116`, `:138`; `server/patches/TrashBarrel-clean-up-britannia.patch` |
| Special barrel requires value and empties immediately | `server/customizations/Services/CleanUpBritannia/CleanupTrashBarrel.cs:54`, `:76`, `:81` |
| Bag is blessed, character-owned, one at a time; replacement deletes old bag wherever it is | `server/customizations/TrashBag.cs:46`, `:68`, `:75` |
| Actual context label is Clean Up Britannia; dump and return controls; owner-only dump | `server/customizations/TrashBag.cs:121`, `:212`, `:251`, `:299` |
| Bundles only for valued items in one sweep or dump, one per five | `server/customizations/ClusterFCustodianSystem.cs:405`; `server/customizations/TrashBag.cs:283` |
| Civic Contracts pay gold only | `server/customizations/ClusterFWorkOrderSystem.cs:2403`, `:2413` through final Civic Contract definition |
| Warden store opens for nonmembers too, within five tiles of Warden or Officer | `server/customizations/SanitationWardenGump.cs:37`, `:180`, `:223`; reward confirmation at `Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:438` under customizations |
| Supply prices: 100 Bandages 15, 5 Refresh Potions 3, 3 Greater Heal Potions 5 | `server/customizations/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:226` |
| No Custodian requisitions | `server/tests/Misc/RequisitionsVerification.cs:198`; current requisition theme table has none |

The page does not repeat historical store totals. The current reward array still contains MISSING rows, so F-3's full-catalog promise must not become a claim that every OSI reward is purchasable. No farm recipes, valuation loopholes, or suggested farming technique appear on the page.

### Healing and resurrection

| Page claim | Source |
|---|---|
| People use Healing/Anatomy; animal/monster patients use Veterinary/Animal Lore | `ModernUO/Items/Skill Items/Misc/Bandage.cs:175`, `:185` |
| Resurrection requires 80/80, cure requires 60/60, checks are probabilistic; poison branch precedes hit-point healing | `ModernUO/Items/Skill Items/Misc/Bandage.cs:239`, `:321`, `:372` |
| Must remain nearby; damage can cause slips | `ModernUO/Items/Skill Items/Misc/Bandage.cs:157`, `:215` |
| Scaled high-skill heal amount | `server/patches/Bandage-heal-scaled-200.patch`; `server/customizations/ClusterFSkillClamps.cs:323` |
| Ordinary healer resurrects when ghost crosses into four-tile range, with freeze, LOS, and CanFit checks | `ModernUO/Mobiles/Healers/BaseHealer.cs:127` |
| Healer Guildmaster adds that resurrection path, without a membership gate | `server/patches/HealerGuildmaster-resurrection.patch:13` |
| Criminals and murderers allowed by defaults; ordinary healer honors those flags | `server/customizations/ClusterFHealerPolicy.cs:15`; `server/patches/Healer-resurrection-policy.patch:7` |
| War mode not checked in these offer paths | Complete movement path in BaseHealer and guildmaster patch above; ordinary healer `CheckResurrect` at `ModernUO/Mobiles/Healers/Healer.cs:43` plus policy patch |
| Working ankh by Registrar is registered in seeder, not every ankh graphic made functional | `server/customizations/ClusterFAnkhs.cs:54`; P137 |
| SelfRes is a Player command, default enabled, requires dead mobile and CanFit | `server/customizations/ClusterFSelfResurrect.cs:11`, `:17`, `:20` |

Did not treat `clusterf.healerPolicy.enabled` as an effective kill switch: the class stores it, but the two patches consult AllowCriminals and AllowMurderers directly. Did not describe all healer variants as identical, promise free resurrection everywhere, or claim that guild membership changes bandage success. No staff commands are included on the page.

### Headquarters and contradictions

F-49 decides towns, not final buildings or installed travel stops. `notes/cc-P151-guild-halls-survey.md:121`, `:136`, and `:347` record the Healers' Abbey church proposal, the Rangers' Counselor's Guild proposal versus stock Rangers' Guild, and the Custodians' empty Britain hall proposal. All remain `(planned)` on the page. P265 is explicitly unplaced decor and does not establish these halls as built.

The page's Contradictions section preserves differing source claims about free versus old joining, account versus character storage, Ranger rank readers, the Healers' name/kit, Civic Tokens and rank thresholds, corpse and magic-property valuation, store coverage, historical healer/ankh reports, and the unresolved Skara building. No decisions were made to reconcile them.

Additional discrepancy kept in this work note: completing the generic Custodian Apprentice task can trigger the shared guild rank bump (`ClusterFGuildSystem.cs:690`), while the Warden calculates rank straight from lifetime points (`SanitationWardenGump.cs:84`). The page gives the Warden's actual ladder and does not advertise an Apprentice shortcut. The code was not changed.

## Verification and limits

Lane tests: none, as requested. No tests or new gates were added, and none are claimed as run. Existing test sources were inspected, including:

- `server/tests/Misc/GuildStarterPathVerification.cs:158`, `:210` and `AlembicGuildVerification.cs:128`, `:171`: character joining, current Healing kit, skill ownership, and preservation of worn items.
- `server/tests/Misc/GuildRankIndexVerification.cs:88`, `:104`, `:109`: Ranger, Custodian, and Healer ladders.
- `server/tests/Services/CustodianLayerVerification.cs:97`, `:180`, `:210`, `:267`, `:297`: ownership and replacement, dump eligibility, lifetime rank, corpse protection, and token retirement.
- `server/tests/Services/CleanUpPropertyWeightVerification.cs`, `ClusterFCorpseValueVerification.cs`, and `CleanUpBritanniaStoreVerification.cs`: property provenance, earned kill/party rules, store rows and purchases. Read as verification specifications; historical green results are P175's report, not a P386 run.
- `server/tests/Skills/SkillClampsVerification.cs:408`, `SkillGainPastStockCeilingVerification.cs:138`, `SkillGainRowKeysVerification.cs:60`, `SkillScalingVerification.cs:346`, and `PetGainSpeedVerification.cs:198`: Tracking clamp, gain hooks, bandages, and member rank inputs for pets.
- `server/tests/Misc/NewHavenServicesVerification.cs:235` and `AnkhVerification.cs:169`: NPC/ankh offer checks. These permit the CanFit refusal when the mapless host cannot prove a standable location; they do not establish client success on the running world.

Unverified: running configuration, deployment state, actual NPC/ankh positions, walkability and appearance in a client, rendered menus, and runtime gain pacing. No stale `server/uo/` content was read. No new numbers about file/type coverage were inferred. The only deliverables are the guide and this note, both under 5 MB.

Ran the required progress reporter with work-copy path overrides and `--dry-run`. It completed successfully. Its output ended with `Counted from the trees: 1567 customization files, 153 patch files, 1388 tests in 221 files.` Those are the tool's reported metrics, not a P386 coverage audit. Despite its documented print-only flag, it rewrote `tools/progress.json` before returning. The file had been clean initially; restored it byte-for-byte from HEAD so it is not part of this docs-only deliverable. No README or dashboard was regenerated.

Final review completed:

- Both requested Markdown files exist. The page ends with Sources and Contradictions, with no code file:line citations on it.
- All local page links resolve. The page has zero em dashes and no trailing whitespace. Numeric claims were checked against the code or explicitly attributed historical source claims.
- The page's only command instructions are the Player commands `[guild`, `[cleanup`, `[cleanupall`, and `[SelfRes`. No staff commands, exploits, or hidden-achievement spoilers are included.
- Windows PowerShell version explicitly verified as 5.1.26100.9444. No PowerShell 7 scripts or tests ran.
- `git diff --check` is clean in both work copies. Separate inspection covered the new, untracked Markdown files, which `git diff --check` does not include.
- Code work copy remains clean. Docs work copy has only this note and `notes/wiki-drafts/rangers-custodians-healers.md` as new files. Each is under 20 KB, below the 5 MB limit. No `docs/` changes remain.
- STOP-REQUESTED was absent at the initial, intermediate, and final review checkpoints. No work remains for P386; running-world and client verification are explicitly outside this draft's evidence.

P386 DONE
