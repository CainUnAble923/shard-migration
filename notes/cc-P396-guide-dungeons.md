# P396: dungeon player guide draft

October 22, 2026. Docs-only work in the Valorite-tower work copies. No code changes.

## Deliverables

- `notes/wiki-drafts/dungeons.md`: a new-player guide covering Rootdeep, classic dungeon coverage, the revamped ports, built bosses, chests and keys, and the connection to difficulty labels, graduation, loops, and League work.
- This evidence and handoff note. Source citations belong here rather than in the player prose.

The page is a draft, not a live availability announcement. It gives no rare spawn locations, hidden-content coordinates, staff commands, exploits, or hidden-achievement conditions. Future features carry `(planned)`.

## Scope and sources

Read the AGENTS files in both work copies before research. Read the direction decision and governing-document index, and consulted the single task list. The task's local work-copy paths replace the older absolute paths in the project notes. No `docs/` file was edited.

Starting code HEAD: `1ecd9f3cc786db045d5619d89ee4e15f1f279784`.
Starting notes HEAD: `2b7def6a5507cc084dc741b92378f388722835f7`.
Pinned ModernUO was checked read-only at `D:/UO/ModernUO-pinned`: HEAD `d4531cd94b739613155225c234900de9f47d2c88`.

Required reference reading: `notes/wiki-drafts/league.md`, `notes/wiki-drafts/high-seas-fishing.md`, `notes/dungeon-decisions-2026-10-01.md`, P24, P36, P49, P196, P211, and the relevant F-12/F-14/F-24/F-32/F-35/F-45/F-47/F-48 portions of `docs/feature-queue.md`. The companion drafts establish the plain-language style and explicit distinction between implemented content and unverified live access.

Followed the source forward where early research predates the implementation: P140/P141/P188 for Rootdeep, CC4 Despise and Shame, P194/P221 for Wrong and Covetous, P195/P271 for Exodus, P197 for unfinished Underworld work, P199 for keys and Remove Trap, P239 for creature difficulty, P371 for tutorial graduation, and P150/P203 for requisitions. These notes informed the research; the implementation and existing tests determine the page's current-behavior claims.

`rg` is unavailable in this shell. Used `git grep`, bounded PowerShell reads, and file enumeration outside `server/uo/` instead. No generated build-tree copy was read.

## Evidence: Rootdeep and the tutorial

Code paths in the tables are relative to the code work copy. Notes paths are relative to the notes work copy. Line citations are to the checked working tree, not an earlier note's historical pin.

| Page claim | Evidence |
|---|---|
| Player name, Trammel region, ruined bank entrance, and limit of three hostile creatures on a Young player | `server/customizations/Regions/OldHavenBurrowsRegion.cs:35`, `:38`, `:46`, `:49`, `:128`. The actual rule counts living wild hostile attackers whose combatant is that player, rather than every nearby monster. Existing `server/tests/Regions/OldHavenBurrowsRegionVerification.cs:224` covers the fourth attacker and exceptions. |
| Physical hole and return ladder; landing ankh | `server/customizations/ClusterFRootdeepSeeder.cs:52`, `:55`, `:68`, `:75`. Existing `server/tests/Regions/RootdeepWayInVerification.cs:109` checks placement and both travel directions. `notes/cc-P188-cont-rootdeep-goes-in.md:19` describes the bank's collapsed south wall. |
| No Recall/Sacred Journey/gate entry, no Mark inside, no gate out, physical exit and Recall out | `server/customizations/Regions/OldHavenBurrowsRegion.cs:87` through the travel switch and return. Existing `server/tests/Regions/OldHavenBurrowsRegionVerification.cs:117` and `:153` cover refused and allowed cases. The page includes the newer island restriction as a qualification. |
| Vault participants and pets only, graduate/credited-player refusal, Overdraft damage credit, temporary one-way crawlway | `server/customizations/Regions/RootdeepVault.cs:122` (MayEnter), `:170` (OnOverdraftDeath), `:204` (TryCrawl), `:237` (TurnOut). Existing `server/tests/Regions/RootdeepVaultVerification.cs:161`, `:207`, and `:280` cover admission, player/pet credit, use, and sealing. The page omits exact room coordinates and the solution to optional content. |
| Broader Burrows creatures and bosses are built; poison, webs, and floor traps exist | `server/customizations/ClusterFRootdeepSeeder.cs:87` and `:99` enumerate the actual placements. `server/customizations/Mobiles/Burrows/WarrenCreatures.cs:155` defines the Burrow Mother and her brood; `server/customizations/Mobiles/Burrows/GloomCreatures.cs` defines the Gloom Queen and her web attack. Existing `server/tests/Mobiles/Burrows/BurrowsCreaturesVerification.cs:362`, `:437`, `:490` cover drops, brood, and webs; `server/tests/Items/Traps/DeployableTrapsVerification.cs` includes the floor-trap placement checks. No spawn coordinates or rare drop odds are copied into the guide. |
| Starter gathering gates are 45; Rootwood and Gloomsilk are cosmetic rather than special combat bonuses | `server/customizations/Engines/Harvest/BurrowsRegionHarvest.cs:23` and `:49` define the actual harvest requirements. `server/customizations/ClusterFMetalTiers.cs` and `server/customizations/ClusterFWoodTiers.cs` define the starter material craft thresholds; `server/customizations/Engines/Craft/BurrowhideTailoringRegistration.cs:36` registers its RequiredSkill. `server/customizations/ResourceInfo.cs:525` gives Rootwood an empty attribute record. `server/customizations/ClusterFStarterResources.cs` supplies Gloomsilk as Cloth. P36 Part D describes the registrations; the guide does not publish the research's suggested gear-upgrade bonuses. |
| Graduation is required before leaving the island by default; Rootdeep is included | `server/customizations/Tutorial/TutorialIslandGate.cs:13`, `:23`, `:27`, `:30`, and `:54`. Existing `server/tests/Tutorial/GraduationLoopVerification.cs:116` and `:163` exercise movement and spell travel. The page describes the default, not an inspected live setting. |
| Graduation records loop 1 but does not reset skills or implement XP levels | `server/customizations/Tutorial/ClusterFLoops.cs:25`, `:34`, `:40`, `:47`. The reset integration method is empty. Existing `server/tests/Tutorial/GraduationLoopVerification.cs:71` checks loop recording and retained skills. No later-loop acquisition route is invented. |

## Evidence: classic coverage and dungeon ports

Stock data presence is evidence of a supported setup, not evidence that its world objects have been imported on the running shard. No list below claims a full shard dungeon census.

For the classic list in the guide, read the stock spawn definitions in pinned ModernUO under `Distribution/Data/Spawns/shared/trammel/` and `shared/felucca/`: `Deceit.json`, `Destard.json`, `Hythloth.json`, `Fire.json`, `Ice.json`, `OrcCaves.json`, and `TerathanKeep.json`. The same names are in `server/customizations/Requisitions/RequisitionTable.cs:354` through `:366` as hunting-area definitions. These file names accompany the list so it is reproducible; no spawn or completion count is inferred from a keyword search.

| Page claim | Evidence |
|---|---|
| Despise revamp is Trammel; Felucca classic creatures remain; stock chests are retained | `server/customizations/Services/Revamped Dungeons/DespiseRevamped/Region.cs:55` selects Trammel. `server/customizations/ClusterFDespiseStockSpawns.cs` filters the stock import. Existing `server/tests/Services/Revamped Dungeons/DespiseRevamped/DespiseStockSpawnsVerification.cs:86` checks chest retention and facet-specific filtering. |
| Karma-matched ankh gives a wisp orb; creature possession; Adrian/Andros boss restriction | `server/customizations/Items/Functional/DespiseAnkh.cs:43` checks karma and creates the orb. `server/customizations/Items/Quest/WispOrb.cs:71` implements the possession link. `server/customizations/Mobiles/Bosses/DespiseBosses.cs:62` gates boss damage; `:180` and `:248` define the bosses. Existing `server/tests/Services/Revamped Dungeons/DespiseRevamped/DespiseRevampedVerification.cs:182` and `:258` exercise the orb and immunity to ordinary damage. |
| Shame on both facets; altars, troll walls, guardian types; summoning currency disabled | `server/customizations/Services/Revamped Dungeons/Shame Revamped/Generate.cs:1` and its Generate body; `ShameAltar.cs:125`; `Mobiles/Bosses.cs:28` onward. `server/customizations/Services/PointsSystems/ShameCrystals.cs:27` is false, `:29` returns zero, AwardPoints is empty. `server/customizations/Services/Revamped Dungeons/Shame Revamped/ShameCrystal.cs` keeps crystals when disabled. Existing `server/tests/Services/Revamped Dungeons/Shame Revamped/ShameRevampedVerification.cs:296` first verifies that a positive-cost summon fails, then explicitly changes the cost to exercise a guardian. That test is not proof that ordinary player summoning is enabled. `Mobiles/Bosses.cs:5` and `ShameSpawns.cs` record Flame/Wind as ordinary spawns too. |
| Wrong revamp, prisoners and jail behavior on both facets | `server/customizations/Services/Revamped Dungeons/WrongDungeon/Generate.cs:1` and `WrongSpawns.cs`; `Region.cs:43` registers both facets, `:107` implements capture on death. Existing `server/tests/Services/Revamped Dungeons/WrongDungeon/WrongRevampedVerification.cs` covers generation, prison creatures, maze doors, escorts, and jail rules. No maze solution or hidden-tunnel location is disclosed. |
| Covetous revamp, Cora, Void Pool defense and its separate rewards | `server/customizations/Services/Revamped Dungeons/Covetous Void Spawn/Generate.cs:91` builds both facet controllers. `VoidPoolController.cs` implements the battle; `VoidPoolStats.cs` computes scores. `Creatures/Cora.cs:35` is the boss; `Creatures/Vela.cs:62` opens the reward interaction. Existing `server/tests/Services/Revamped Dungeons/Covetous Void Spawn/CovetousVoidSpawnVerification.cs:323` covers waves and battle outcome; `:607` covers rewards. No Cora coordinates or rare reward spawn locations are on the page. |
| Exodus combat, theft, chest, and recipe supply routes | `server/customizations/Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusChest.cs:26`, `:76`, `:105`, `:230`; `Mobiles/ExodusMinionLord.cs:73`, `Mobiles/DupresChampion.cs:93`; `server/customizations/Services/Monster Stealing/Core/StealingHandler.cs:124`; `server/customizations/Engines/Craft/ExodusCraftRegistrations.cs:1` and registration body. The recipe header explicitly flags the robe's missing Abyssal Cloth source. The page qualifies crafting instead of promising a complete available materials chain. No hidden supply-chest locations or reveal procedure are given. |
| Exodus party ritual, supported shrines, close party members, robe requirement and consumption, transport | `server/customizations/Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusSummoningAltar.cs:44` and its Build method; `Items/ExodusTomeAltar.cs:147`, `:167`, `:188`, and the owner context entry. Existing `server/tests/Services/Revamped Dungeons/TheExodusEncounter/ExodusEncounterVerification.cs:408` exercises a real ritual; `:539` covers encounter death/exit. The guide supplies neither shrine coordinates nor hidden-content directions. |
| Blackthorn access and restrictions, Minax artifacts and Agent rewards; invasion absent | `server/customizations/Services/Revamped Dungeons/BlackthornDungeon/Generate.cs` and pinned `Distribution/Data/teleporters.json` provide castle travel; `Region.cs` implements the reveal/idle-poison behavior and spell/pet/mount restrictions. `server/customizations/Services/PointsSystems/BlackthornData.cs:60` rolls artifacts and `:124` processes looting-rights damagers. `server/customizations/Services/Revamped Dungeons/BlackthornDungeon/Creatures/AgentoftheCrown.cs` supplies turn-in and claim behavior. Existing `server/tests/Services/Revamped Dungeons/BlackthornDungeon/BlackthornDungeonVerification.cs:283`, `:638`, `:774` cover region behavior, Agent trade, and awards. P196's Headlines and section 6 defer the controller/beacon. The canonical tracked code still has neither class. No claim of identical modern official reward properties is made. |
| Underworld and mini champions are unfinished, not verified-open destinations | `server/customizations/Services/Underworld/Generate.cs:1` and `server/customizations/Services/MiniChampionSystem/MiniChampionSpawn.cs:1` document their placement paths, but `notes/cc-P197-port-underworld-mini-champions.md:15`, `:39`, `:51`, `:59`, `:96` explicitly leave review/tests pending and end PAUSED. No dedicated Underworld/MiniChamp behavioral test was found in the tracked shard tests. The page labels the work unfinished (planned), rather than treating compilable code as proven encounters. |

## Evidence: chests and keys

Pinned source paths below are relative to `D:/UO/ModernUO-pinned/Projects/`.

| Page claim | Evidence |
|---|---|
| Classic lock requirements 57/72/84/92 and dart/explosion/poison/explosion traps | `UOContent/Items/TreasureChests/TreasureChestLevel1.cs:15`, `:19`; the corresponding Level2, Level3, Level4 files use the same constructor line positions. Actual integers read from each file, not taken solely from P49. |
| Requirement allows a roll, not guaranteed unlock | `UOContent/Items/Skill Items/Thief/LockPick.cs:121` and `:128`. The shard's failed-pick patch specializes treasure-map chests, not the classic table. |
| Disarm depends on trap power; even Remove Trap 100 may fail a stock L4 trap | `UOContent/Skills/RemoveTrap.cs:61` checks TrapPower through TrapPower + 30. `UOContent/Items/TreasureChests/TreasureChestLevel4.cs:16` can exceed 100. The page publishes no derived probability or fabricated recommended skill level. |
| No Lockpicking/Detect Hidden prerequisites under EJ | `server/patches/RemoveTrap-trap-training-kits.patch:21` through `:30`; registered by `docker/uo/apply-patches.sh:755`. Existing `server/tests/Items/Functional/TrapTrainingKitVerification.cs:135` exercises Remove Trap with both prerequisites at zero and asserts Core.EJ; `:427` checks the patched source lines. This supersedes neither source file by editing it; both historical descriptions stay recorded below. |
| Classic chest loot and decay are independent of looting | Loot bodies and Decays/DecayTime members of `UOContent/Items/TreasureChests/TreasureChestLevel1.cs:71`, Level2 `:68`, Level3 `:113`, Level4 `:116`. `UOContent/Engines/Spawners/BaseSpawner.cs` and the chest rows in the stock dungeon spawn JSON provide replacement behavior. No personal refill exists in these classes. |
| Shame chests differ and delete after opening | `server/customizations/Items/Containers/TreasureChestMod.cs:19` and constructors of TreasureLevel2/3/4; `server/customizations/Items/Containers/BaseTreasureChestMod.cs:64` starts deletion on opening, `:93` guards against restarting and schedules deletion. Unlike the classic classes they use MagicTrap and their own loot tables. The guide does not advertise them as reforged equipment. |
| Ten-use keys, 10/100 gate reductions, master success and unpickable exceptions | `server/customizations/Items/Tools/SkeletonKey.cs:39`, `:49`, `:67`, `:134`, `:142`, `:152`; `server/customizations/Items/Tools/MasterSkeletonKey.cs:24`. Existing `server/tests/Items/P199ResourcesToolsVerification.cs:447`, `:468`, `:492` verify those rules. `server/customizations/Services/TreasureMaps/TreasureMapInfo.cs:539` includes both keys in its reward table. No broad claim that keys remove encounter entrance requirements is made. |
| Unified chest overhaul, L5/L6 and 30-60 minute first-access refill are decided future work | `docs/feature-queue.md:2494` through `:2511`, particularly `:2503` and `:2505`; P49's proposal/decision sections. A tracked canonical code/test search for DungeonChest found no implementation. Its planned numbers are separated from current stock and Shame behavior. |
| Built mimic monster, no player chest/tame route | `server/customizations/Mobiles/Normal/ChestMimic.cs:20` lists the handoff/placement work as later; `:273` keeps Tamable false. Existing `server/tests/Mobiles/Normal/ChestMimicVerification.cs:283` explicitly covers target forwarding and absence of a PetMimic handoff. No DungeonChest trigger was found. P50 builds the monster, not the complete F-32 chest system. |

## Evidence: progression and the League

- `server/customizations/ClusterFCreatureLevels.cs:50` implements the provisional best-combat-skill source, `:94` defaults the settings on, `:232` onward provides the difficulty words and label, and its ClusterFAppraisal class implements the skill-dependent detail. Existing `server/tests/Mobiles/CreatureLevelsVerification.cs:325` verifies the provisional comparison and replacement seam; `:374` and `:426` cover Appraisal details and skill targeting. The page does not turn the provisional display into an earned character level or dungeon entry gate.
- `server/customizations/Tutorial/ClusterFLoops.cs:30` contains a ladder helper but explicitly does not enforce caps. The empty reset method at `:40` is why the guide separates real graduation loop recording from planned F-12 resets and XP.
- `server/customizations/Requisitions/RequisitionTable.cs:351` through `:368` includes dungeon area names. `server/tests/Misc/RequisitionsVerification.cs:325` checks consumed items and Renown/standing payouts; `:539` covers Leads. The page links the companion League guide rather than reproducing its full reward tables or promising a suitable item from every dungeon kill.
- `docs/feature-queue.md:1946` through `:1948` decides gather/cull/investigate dives and party sharing; `:1968` through `:1970` records order/dependencies. `server/customizations/ClusterFLeagueRanks.cs:180` through `:200` keeps the unbuilt promotion/trial waivers. P211 is an assessment and proposed generator port, not a released player dive system; no SVDungeon implementation is in canonical customizations/tests.
- `docs/feature-queue.md:1227` through `:1234` supplies the decided Setting plan: twenty floors, floor N opens on loop N+1, final epilogue on the last floor. The guide's 20 and 2-21 come directly from that decision, not from the earlier placeholder ladder. No Setting entrance or playability claim is made.

## Contradictions and limits left on record

The guide ends with Sources and Contradictions. Nothing in the underlying notes, decisions, or code is changed to reconcile them.

1. Shame's old headers say its points framework does not exist, while `server/customizations/Services/PointsSystems/PointsSystem.cs` and Blackthorn's real integration do exist. The Shame seam itself remains disabled. The guide describes the observed disabled state and preserves the source disagreement.
2. F-32 says there should be one chest system, but the current classic and Shame classes have different lock/trap/loot/deletion behavior. Planned first-access refill is not current universal behavior.
3. P49's Remove Trap prerequisites describe the unpatched pinned source. P199's applied EJ patch removes them. Both descriptions remain recorded.
4. `notes/cc-P24-new-haven-dungeon-research.md:112` proposes the Burrow Mother as a mini champion final boss. The Rootdeep seeder directly places her, and WarrenCreatures implements her own brood. The separate MiniChamp table does not name her.
5. Older F-12 passages retain post-cap-loop Setting timing, while the later decision at `docs/feature-queue.md:1225` gives the 2-21 schedule. P371 also records an actual first loop without building the planned resets. No source is edited to reconcile these layers.
6. P211's description of Rootdeep as built differs in scope from P188's explicit outstanding client/world/package steps (`notes/cc-P188-cont-rootdeep-goes-in.md:35`, `:39`, `:148`, `:157`, `:307`, `:380`). No current-world inspection was authorized, so open/live status stays unverified.

Further limit discovered while reading forward: P197's unfinished Underworld/mini champion port has no dedicated encounter-test evidence in this tree. It is described as unfinished rather than included in the implemented-dungeon table. Its note's continuation number is not used as proof of a completed follow-up.

## Validation and handoff

Lane tests: none, as the prompt specifies. No tests or gates were added or changed, so no new red/green cycle applies. Existing tests were read as implementation evidence; no build, test suite, Docker container, or client session was run for this writing task. Historical green builds in source notes are not reported as a P396 result.

Progress reporting: ran `tools/progress.py --dry-run` in memory against these work copies. Its build function unconditionally attempts to write `tools/progress.json` even with `--dry-run`; a temporary in-process `Path.write_text` override suppressed that snapshot write. The report completed with empty stderr and no repository changes. No progress proxy counts were promoted into the guide.

No Haven connection, deployment, live configuration inspection, branch change, commit, merge, or push. No account or save changes. No art was needed.

Final editorial review:

- Read the complete guide back after writing. Split the longer Exodus directions into short paragraphs and removed staff implementation details from the player-facing availability paragraph.
- Checked every Markdown link in the guide against the local notes checkout: no missing targets. Sources and Contradictions are its final sections.
- Checked the guide for em dashes and non-ASCII characters: none. Reviewed the numeric literals against the evidence above, including the explicitly planned refill timer and Setting schedule.
- Checked full code file:line citations for existing files and valid line bounds. Corrected the WispOrb path to `Items/Quest/`. The separate `server/uo/` mention is a prohibited-tree boundary, not a source citation.
- Parsed each named classic dungeon spawn JSON on both facets and inspected creature entries. File presence alone was not promoted into proof of a live population.
- Inspected chest implementations and the relevant patch list for the proposed refill/depth behavior, in addition to searching names. The mimic's own header explicitly leaves chest triggering and taming for F-32. No unified implementation was identified.
- Both new files are below 5 MB. Checked their whitespace and conflict markers as text. `git diff --check` is clean in both repos; because these files are new and untracked, the direct text review supplies their editorial check.
- Windows PowerShell reports version `5.1.26100.9444`. No PowerShell 7 scripts or tests were used.
- Final scope is only this note and `notes/wiki-drafts/dungeons.md` in the notes work copy. The code work copy is clean. There are no changes under `docs/`, no new tests, and no generated progress artifacts.
- Checked `D:/UO/golem/codex-runs/P396-Valorite.STOP-REQUESTED` between research, writing, and final verification steps; it was absent on each check.

Unverified: current live dungeon setup, actual player access, package publication, client appearance/walkability, and pending Underworld/mini champion behavior. This writing task does not certify those. There is no remaining P396 implementation work.

P396 DONE
