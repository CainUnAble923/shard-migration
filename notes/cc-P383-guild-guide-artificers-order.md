# P383: Artificers' Order player guide draft

Task: documentation only, Codex lane. Date: October 21, 2026, America/Chicago.

Deliverable: [wiki-drafts/artificers-order.md](wiki-drafts/artificers-order.md). It follows the P374 League guide's draft notice, short paragraphs, tables, Sources, and recorded contradictions. It is a local Markdown draft, not a published wiki page.

## Scope and method

- Read both work-copy AGENTS.md files first, plus the migration repository's direction decision, document index, and task list. The prompt's work-copy paths replace the older absolute paths in those agreements.
- Read `notes/wiki-drafts/league.md` as the style model; `docs/artificers-imbuing-design.md`; `design/guilds/artificers_order.md`; and the Artificer-related feature-queue decisions. Queue passages reviewed include F-9, the F-24 non-member payout decision, F-33, F-34, F-37, F-43, F-47/F-48, F-49, F-50, and the satchel hue decision near the queue's beginning.
- Searched every `notes/cc-P*.md` for `Artificer`, case-insensitively. Read the guild and Imbuing passages with surrounding context in every matching note, expanding the central implementation notes where necessary. Cross-cutting operations notes were used for context, not as proof of game behavior. The complete matching input inventory is below; keyword matches were not treated as evidence of implementation.
- Compared the notes against canonical `server/customizations/`, relevant patches, and existing verification sources. Did not read `server/uo/`. Did not use external web research: this task's evidence is the local design and implementation.
- Numbers on the page come from source defaults, not a live settings file. Learned formulae versus essence mastery, character guild data versus account knowledge, and currency versus physical ingredients are kept distinct.
- No code, tests, configuration, services, or files under `docs/` changed. No builds, deployments, live connections, account operations, commits, branch changes, merges, or pushes.

## Implementation evidence

All paths in this table are relative to the Shattered Legacy work copy. File and line citations are intentionally here rather than on the player page.

| Claim checked | Source evidence |
|---|---|
| Identity, Imbuing, intended name Thornwick Vesper | `design/guilds/artificers_order.md:7`; `server/customizations/ArtificersGuildmasterGump.cs:47` and `:116`; `server/customizations/ClusterFGuildStarterPath.cs:63`. Thornwick is the design/menu name; actual placed NPC names were not inspected. |
| Free character membership | `server/customizations/ClusterFGuildSystem.cs:309` and `:313` (`CanJoin`), `:427` (`Join`); shared join page `:1085`, response `:1204`; member-services navigation `:1174` and `:1224`. The Talk context entry is added by `server/customizations/ClusterFGuildmasterExtension.cs:37` (`GuildMembershipEntry`). |
| Apprentice task, rewards and tribute consumption | `server/customizations/ClusterFGuildSystem.cs:236` registers the task, Imbuing 20.0 or 3 Diamonds, 25 reputation and 10 currency; `:333` checks base skill or eligible resources; `:382` completes it; `:400` consumes tribute only when the skill half is unmet. The task mark, reputation and currency are added at `:412`. |
| Starter satchel/toolkit, once per character | `server/customizations/ClusterFGuildStarterPath.cs:290` (`GiveTools`), `:324` (`GiveJoinBonus` and record); `server/customizations/ClusterFGuildSystem.cs:499` issues the two items. `server/customizations/ArtificersToolkit.cs:21`, `:30` and `:50` establish blessing, backpack and membership checks, and portable table access. |
| Standing ladder | `server/customizations/ArtificersGuildmasterGump.cs:262` (`GetRankName`); `server/customizations/ClusterFGuildSystem.cs:620` (`ArtificerThresholds`) and `:642` (`GuildRankIndex`). Standing thresholds: 0, 1,000, 5,000, 15,000, 40,000. |
| Apprentice task raises the effective rank | `server/customizations/ClusterFGuildSystem.cs:670` (`StandingRankIndex`) raises completed Apprentice tasks to rank index 1; `:690` (`GetRankName` overload) raises the displayed standing to the second-rank threshold. `server/customizations/Imbuing/ImbueFormulaBooks.cs:89` uses the effective index for shop rows. This reaches the first book with the task completed, even at 25 standing. This is a source-traced behavior, not a newly executed gameplay check. |
| Imbuing is excluded from generic craft-skill promotion | `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:385` (`RecipeOwners`), especially `:389` through `:400`: no Imbuing entry. `server/customizations/ClusterFGuildPromotion.cs:101` returns without tracking non-craft owners. Do not import the general 30/50/70/90/100 craft promotion skill requirements into this guide. |
| Account-wide formulae and mastery; character standing/currency/orders | `server/customizations/Imbuing/ClusterFImbueKnowledge.cs:122` (`KnownTier`), `:147` (`Grant`), `:235` (`ReadBook`); `server/customizations/ClusterFAccountData.cs:50`, `:75`, `:635`, `:776` and `:815`. Formula keys use the account's learned-recipes store; mastery uses its discovery dictionary. |
| Free properties, book contents, book prices | `server/customizations/Imbuing/ImbuingTable.cs:161` (free set), `:167` through `:182` (ladder groups), `:191` (`BooksFromLadder`), `:193` (book names), `:279` (250/500/1,000/2,000/4,000 prices). Each book grants its own Basic group, the preceding group's Refined, and the earlier group's Full where present. |
| Book purchase/read rules and trial | `server/customizations/Imbuing/ImbueFormulaBooks.cs:78` (membership, rank, unread shop rows), `:112` (Shards only), `:135` (read, trial, duplicate handling and consumption), `:216` (purchase near guildmaster). `server/customizations/ClusterFGuildPromotion.cs:33` defaults the trial waiver to true; `:79` implements trial or waiver. |
| Tier fractions, property slots and site defaults | `server/customizations/Imbuing/ImbuingTable.cs:99` (0.333/0.667), `:109` (5 slots, slot mode, +1 Master slot), `:121` (Anywhere Full, MuleII Refined, MuleIII Full, Forge Overcharged), `:132` (forge range 2). `server/customizations/Imbuing/ClusterFImbueKnowledge.cs:214` (`MaxSlots`), `:400` (`MaxFor`, rounds with at least 1; bools stay 1). |
| Eligible equipment and known-tier apply gate | `server/customizations/ArtificersImbueGump.cs:745` (`ForItem`), `:755` (weapon/armor/jewel/clothing), `:1004` (known rows), `:1750` (`HandleApplyImbue`), `:1767` (known-tier and site checks), `:1797` (slot/budget checks). Spellbooks, instruments and talismans are not included equipment kinds. |
| Essence mastery, material costs, success/failure, standing | `server/customizations/ArtificersImbueGump.cs:725` (per-property mastery thresholds); `:1815` (custom ingredients), `:1824` (essence until mastered), `:1837` (Shards and gold), `:1853` (skill check), `:1859` (failure can reduce current weapon/armor durability), `:1865` (consume after success), `:1883` (mastery), `:1898` (standing). No resource cost on skill failure. |
| Self Repair is Basic without a rank gate; expensive floor remains | `server/customizations/ArtificersImbueGump.cs:89`, `:103`, `:158`; `server/customizations/Imbuing/ImbuingTable.cs:165`. Old standing gates no longer occur in `HandleApplyImbue`. |
| Skill bonuses and custom-property limit | `server/customizations/ArtificersImbueGump.cs:488`, `:519` (jewelry groups), `:531` (craft/gather groups), `:538` (configured crafter gear), `:560` (skill row and group refusal), `:602` (one custom property). Default aprons: `server/customizations/Imbuing/ImbuingTable.cs:136`. Basic/Refined/Full +5/+10/+15 is also asserted by `server/tests/Misc/ImbuingReworkVerification.cs:338`. |
| Craft-property effects | `server/customizations/Imbuing/ClusterFImbueEffects.cs:230` (Bountiful), `:243` (Prospector), `:257` (gather application), `:279` and `:297` (carving/kill parts), `:350` (Mastercraft). Integration calls are in `CompactOreSatchelRoutingHook.cs`, `ClusterFLumberjackingExtension.cs`, `ClusterFHuntersSatchelHooks.cs`, and `server/patches/Imbue-custom-property-hooks.patch`. The page limits gathering claims to mining/lumber. |
| Forge/mule rules | `server/customizations/Imbuing/ImbueSites.cs:68` chooses the best cap then bonus, `:81` considers owner mule tiers II/III, `:92` considers nearby forges. The page does not claim an Artificers' hall forge has been placed. |
| Full Disenchant and container yield | `server/customizations/ArtificersImbueGump.cs:1397` (confirmation), `:1957` (`CanUnravel`), `:1970` (`UnravelOne`: Shards, 25% essence roll per active property, gain check, deletion), `:2004` (direct children), `:2027` (bag inside backpack and unlocked), `:2040` (shared per-item path and summary). No formula-knowledge or membership gate in these operations. |
| Extract and durability; craft essences | `server/customizations/ArtificersImbueGump.cs:2076` extracts, `:2101` reduces weapon/armor maximum by integer division by 5 and clamps current HP, `:2114` gives essence and Shards. `:2134` crafts only mastered non-custom essences for Shards/gold, placing them in the backpack. The page does not claim crafting essences gives skill gain. |
| Satchel and physical material distinction | `server/customizations/ArtificersSatchel.cs:37` (capacity), `:40` (blessed), `:49` (`CheckHold`), `:68` (PropertyEssence, MagicalResidue, EnchantedEssence, RelicFragment), `:70` (nested backpack lookup), `:73` and `:96` (satchel then backpack fallback), `:109` (loot pickup), `:127` (mastery dashboard), `:224` (contents/mastery display). `server/customizations/ClusterFBackpack.cs:48` and `:59` route drag pickups. Shards are added through character currency at `ArtificersImbueGump.cs:1982` and `:2119`, never created as an item. |
| Enchanting work orders | `server/customizations/ArtificerWorkOrderSystem.cs:167` (mastery, Smith membership), `:202` (regular definitions), `:475` (combined weapon definitions), `:813` (supplied serial versus combo type/resource), `:836` (GuildResources candidate lookup), `:903` (one active order and handout), `:950` (turn-in), `:1000` (consume and rewards), `:1024` (abandon). Availability has no rank or formula-knowledge check. |
| Requisitions versus enchanting orders | `server/customizations/ClusterFGuildSystem.cs:1184` and `:1243` (hall requisition entry); `server/customizations/Requisitions/RequisitionTable.cs:337` (Artificer themes); `server/customizations/Requisitions/RequisitionSystem.cs:233` (backpack item), `:245` through `:255` (Renown, standing, appraiser gold, consume; no Shards). |
| Exchange upgrades, not a base mule purchase | `server/customizations/CrossGuildExchangeGump.cs:13`, `:62`, `:128`; `server/customizations/Mobiles/Mule/MuleUpgrades.cs:31` includes Artificers' currency in a later upgrade, and `:43` names it Essence Shards. The page directs a first mule to the League errand, following the current exchange text. |
| Actual source locations versus proposed hall | `server/customizations/ClusterFGuildStarterPath.cs:228` and `:229`: New Haven 3483,2501,52 Trammel and Royal City 797,3431,-10 Ter Mur. `server/customizations/ClusterFInstitutionSeeder.cs:98` places the Ter Mur post. The directory resolves an existing NPC and prefers the same facet at `ClusterFGuildStarterPath.cs:609`. `notes/cc-P151-guild-halls-survey.md:311` distinguishes the outdoor post from a hall; `docs/feature-queue.md:3394` fixes the future HQ town; P265 places no hall. |

## Contradictions retained, not resolved

The page records these source differences and does not change any decision or implementation:

1. **Joining versus Apprentice task.** Original `design/guilds/artificers_order.md:11` requires skill or tribute for entry; its later sections and the custom guildmaster text advertise rewards on joining. F-9 Decision 3 and P15 put them on the later task. Current `ClusterFGuildSystem.cs:313`, `:382` and `:427` implement the latter; `ArtificersGuildmasterGump.cs:197` still says rewards are received upon joining.
2. **Rank names after the Apprentice task.** `ArtificersGuildmasterGump.cs:262` uses standing alone. `ClusterFGuildSystem.cs:670` and `:690` lift the task-completer to the second rank and `ImbueFormulaBooks.cs:89` uses that effective rank. This is why the guide labels the table a standing ladder and separately explains first-book access through the task.
3. **Power by standing versus learned tiers.** Original design, P20, P42 and P58 describe the old caps/slots and Self Repair rank gate; P82 explicitly removes them. Current code checks knowledge, site and slots at `ArtificersImbueGump.cs:1767`. `ArtificersGuildmasterGump.cs:157` and `ClusterFGuildSystem.cs:508` retain old claims. No attempt was made to correct that UI in a docs-only task.
4. **Rank index 4 has no standing rung.** Design/`ImbuingTable.cs:178` assigns the Arcane book to 4 and Master to 5. `ClusterFGuildSystem.cs:642` maps the five standing rungs to 0/1/2/3/5. P82 section 6 raises this explicitly. Both books open at Arcane Artisan, subject to the Master's trial condition.
5. **Trial requirement versus waiver.** The design and `ImbueFormulaBooks.cs:97` and `:145` require a trial. `ClusterFGuildPromotion.cs:33` and `:79` waive it by default while unbuilt. Live waiver configuration and any character trial state are unverified.
6. **Reinforce, Casting Focus, and advanced sources.** Design promises free Reinforce and advanced learning through the 140+ path. P82 section 6 reports the missing operations/effects. Current table has no Reinforce stage, and `ClusterFImbueKnowledge.cs:49` keeps Casting Focus grant-only without a row. A search across canonical customizations and patches for `ClusterFImbueKnowledge.Grant(`, `imbue:` and `ReadBook(` found book/knowledge operations and the administrative grant interface, not player quest/boss/box reward calls. The API alone is not a built acquisition path. Those future sources are marked planned on the page.
7. **F-50 satchel specification versus currencies.** `docs/feature-queue.md:3444` names Essence Shards alongside physical ingredients. P137 section 6 and `ArtificersSatchel.cs:68` distinguish the actual accepted items; `ArtificersImbueGump.cs:1982` credits Shards as currency. Its Unravel does not produce the standard residue/essence/relic progression.
8. **Order tier claims, examples and availability.** Original design's work-order tiers/examples and `ArtificerWorkOrderSystem.cs:113` imply standing-based availability. Current `:167` only tests mastery and Smith membership. Combined definitions at `:475` through `:505` are weapons, unlike the design's armor/shield examples. No normal-player instructions to bypass gates or exploit missing checks were added. The page recommends checking learned tiers before accepting an order.
9. **Mule II/III and portable toolkit.** F-33 at `feature-queue.md:2671` assigns Unravel to II and Imbue to III; the later rework design gives II Refined and III Full. P70 predates site checks, P82 adds them and records the overlap with default Anywhere Full. Current `ImbueSites.cs:68` chooses the best permitted site, so the default toolkit cap outranks mule II.
10. **Hall and NPC coordinates.** Original design gives Royal City 793,3468,-20 and old New Haven 3490,2627,0. Current `GuildLocations` and institution seeder use the coordinates cited above. F-49 says Royal City is already posted; P151 documents an outdoor NPC, not a finished headquarters. P265 only supplies unplaced decoration templates. The draft distinguishes the existing post from the planned hall and leaves the survey's building choice open.

Additional historical differences that did not require a player-guide claim: P22 leaves essences pack-only, P27 widens to pack and bank; P18 changes guild data from account-wide to character-specific; P236 changes the satchel's appearance. These are recorded implementation changes, not grounds to silently edit their original notes. P82's statements that levelable items and LeagueJob Renown do not exist predate P261 and P150. Current source has both systems, but a caller search for `EchoOfTheLoopPercent(` and `RenownedAmount(` found only their definitions in `Imbuing/ClusterFImbueEffects.cs:446` and `:452`; this guide does not advertise either as a working reward.

## Existing tests read

No new tests or gates were written. Lane tests: none. Existing C# verification sources were read to cross-check behavior; no suite was run or claimed green in this task.

- `server/tests/Misc/ImbuingReworkVerification.cs:98`: account knowledge; `:123`: tier clamping; `:145`: default book table; `:197`: shop currency and reading; `:226`: trial/slot behavior; `:311`: non-member extraction; `:338`: skill groups; `:376`: base-skill gains; `:402`: custom effects; `:509`: forge; `:536`: mule sites.
- `server/tests/Misc/ImbueSelfRepairGateVerification.cs:180`, `:202`, `:223`, `:248`, `:267`: no rank gate, learned Full, price floor, charged price, other-property scaling.
- `server/tests/Misc/ImbueEssenceSourcesVerification.cs:211`, `:225`, `:241`, `:263`, `:284`: backpack, bank, split counts, wrong property refusal, satchel ordering.
- `server/tests/Misc/ImbueExtractDurabilityVerification.cs:138` and `:161`: weapon and armor maximum/current durability after extraction.
- `server/tests/Misc/UnravelSatchelVerification.cs:104`, `:134`, `:182`, `:203`, `:238`, `:293`: plain-item refusals, extracted/full-disenchant delivery, pickup routing, bank/pack/craft exclusions, full-satchel fallback.
- `server/tests/Misc/UnravelContainerVerification.cs:109`, `:143`, `:182`, `:213`: mixed bags, protected/nested skips, single blessed refusal, container location refusal.
- `server/tests/Misc/ImbueAllSlayersVerification.cs:120`, `:169`, `:219`, `:238`, `:265`: extract/imbue, catalogue coverage, existing essence keys, button ranges, super slayers.
- `server/tests/Misc/GuildRankIndexVerification.cs:128`: Apprentice task lifts index; its Artificer ladder fact checks the skipped index. `GuildStarterPathVerification.cs:154`, `:247`, `:548`, `:666` check free joining, each character's kit, directions and the separate task. `ArtificerRankCommandVerification.cs` was also inspected for the fresh-account and known-tier readout cases; the optional player command is not necessary to follow this guide.

## Unverified and deliberately not promised

- Running build, live configuration, NPC existence/name/position, access to Ter Mur, placement of a soul forge, and client appearance were not checked. No live connection was made.
- Default tier fractions, book prices, slot mode, site caps, and the trial waiver can be configured. The draft labels numbers as source defaults.
- No general Imbuing-to-200 training route is promised. P283 still reports the ordinary Imbuing gain ceiling and proposes separate mastery work, not a built extension.
- No rare advanced formula drops, usable Reinforce action, top-rank trial entrance, tool belts, full Royal City hall, hall decor placement, or automatic replacement of join-only tools are advertised as available.
- Hidden achievements and their triggers, staff commands, and exploit recipes are absent from the player page, including its Contradictions list.

## Review inventory of matching CC notes

The list below is the complete case-insensitive `Artificer` match set used for this task, excluding this new P383 note. Several matches are only incidental console-command inventories; their existence does not establish any game feature.

- [cc-P11-account-data-serializer.md](cc-P11-account-data-serializer.md): matching lines 106.
- [cc-P137-usable-ankhs-and-playtest-fixes.md](cc-P137-usable-ankhs-and-playtest-fixes.md): matching lines 32, 62, 260, 262, 272, 276, 286, 290, 302, 317, 463, 494.
- [cc-P14-newhaven-guild-mapping.md](cc-P14-newhaven-guild-mapping.md): matching lines 142, 162, 239, 240, 242, 265, 268, 281.
- [cc-P145-combat-script.md](cc-P145-combat-script.md): matching lines 27, 29, 31, 34, 62, 63, 64, 90, 92, 100, 143, 160, 171, 172, 195, 199, 219, 248, 250.
- [cc-P146-playtest-decisions-inbox.md](cc-P146-playtest-decisions-inbox.md): matching lines 274, 275.
- [cc-P149-away-mode-and-email-controls.md](cc-P149-away-mode-and-email-controls.md): matching lines 120.
- [cc-P15-guild-starter-path.md](cc-P15-guild-starter-path.md): matching lines 24, 26, 81, 164, 177, 242, 275, 281, 312, 358, 448, 466, 516, 517.
- [cc-P150-requisitions-and-leads.md](cc-P150-requisitions-and-leads.md): matching lines 37, 64, 87, 93, 252, 255, 417.
- [cc-P151-guild-halls-survey.md](cc-P151-guild-halls-survey.md): matching lines 24, 59, 63, 311, 314, 327, 373.
- [cc-P152-art-requests-openai.md](cc-P152-art-requests-openai.md): matching lines 384.
- [cc-P153-queue-notes-and-package-whats-new.md](cc-P153-queue-notes-and-package-whats-new.md): matching lines 136.
- [cc-P17-playtest-bugs-1.md](cc-P17-playtest-bugs-1.md): matching lines 287, 632.
- [cc-P173-imbue-all-slayers.md](cc-P173-imbue-all-slayers.md): matching lines 8, 26, 37, 59, 137, 164.
- [cc-P174-session-closer-fix.md](cc-P174-session-closer-fix.md): matching lines 109, 110.
- [cc-P175-cont-clean-up-britannia-finish.md](cc-P175-cont-clean-up-britannia-finish.md): matching lines 51.
- [cc-P176-cont-artificers-unravel-container.md](cc-P176-cont-artificers-unravel-container.md): matching lines 1, 7, 47, 110, 162, 174, 187, 203.
- [cc-P177-guild-menus-template-mockups.md](cc-P177-guild-menus-template-mockups.md): matching lines 39, 47, 80, 81, 82, 83, 168.
- [cc-P179-league-design-pass.md](cc-P179-league-design-pass.md): matching lines 159, 165.
- [cc-P18-reset-stone-young-craftx.md](cc-P18-reset-stone-young-craftx.md): matching lines 20, 52, 53, 54, 55, 98, 101, 128, 148, 160, 161, 216, 441, 489.
- [cc-P182-cont-web-console-phase2.md](cc-P182-cont-web-console-phase2.md): matching lines 139.
- [cc-P186-cont-golem-join-kit.md](cc-P186-cont-golem-join-kit.md): matching lines 218.
- [cc-P190-cont-test-crystal.md](cc-P190-cont-test-crystal.md): matching lines 127.
- [cc-P191-cont-earned-skill-gain.md](cc-P191-cont-earned-skill-gain.md): matching lines 82.
- [cc-P192-cont-fountain-of-youth.md](cc-P192-cont-fountain-of-youth.md): matching lines 171.
- [cc-P20-skill-scaling-research.md](cc-P20-skill-scaling-research.md): matching lines 854, 858, 859, 861.
- [cc-P208-cont-shadow-iron-merger.md](cc-P208-cont-shadow-iron-merger.md): matching lines 140.
- [cc-P21-console-world-commands.md](cc-P21-console-world-commands.md): matching lines 307, 317, 318.
- [cc-P217-crystal-wiki-catch-up.md](cc-P217-crystal-wiki-catch-up.md): matching lines 52, 197.
- [cc-P22-small-features-1.md](cc-P22-small-features-1.md): matching lines 31, 218, 226, 242, 488.
- [cc-P224-playtest-bot-checks-second.md](cc-P224-playtest-bot-checks-second.md): matching lines 191, 396.
- [cc-P23-live-defect-sweep.md](cc-P23-live-defect-sweep.md): matching lines 193, 199, 209, 237, 344.
- [cc-P236-satchel-icons-ship.md](cc-P236-satchel-icons-ship.md): matching lines 11, 19, 35, 42, 79, 97, 100, 113, 122, 165, 169, 193, 250, 254.
- [cc-P239-creature-levels-appraisal.md](cc-P239-creature-levels-appraisal.md): matching lines 144, 148.
- [cc-P24-new-haven-dungeon-research.md](cc-P24-new-haven-dungeon-research.md): matching lines 791.
- [cc-P25-stats-above-125-research.md](cc-P25-stats-above-125-research.md): matching lines 49, 53, 198, 334.
- [cc-P26-animated-runestone.md](cc-P26-animated-runestone.md): matching lines 319.
- [cc-P260-herbalism-research.md](cc-P260-herbalism-research.md): matching lines 202.
- [cc-P261-levelable-gear-build.md](cc-P261-levelable-gear-build.md): matching lines 211.
- [cc-P265-guild-hall-decor-packs.md](cc-P265-guild-hall-decor-packs.md): matching lines 7, 10, 161, 162, 163, 164, 165, 166, 303, 311, 381, 424.
- [cc-P27-defect-batch-1.md](cc-P27-defect-batch-1.md): matching lines 23, 135, 147, 154, 336, 366, 367, 413, 418.
- [cc-P283-skill-gain-paths-research.md](cc-P283-skill-gain-paths-research.md): matching lines 54, 137.
- [cc-P29-defect-batch-2.md](cc-P29-defect-batch-2.md): matching lines 200, 329, 336, 348, 349, 351, 374, 458, 461, 503, 512, 513, 517.
- [cc-P32-spawner-importer-bods-self-repair.md](cc-P32-spawner-importer-bods-self-repair.md): matching lines 34, 35.
- [cc-P33-clean-up-britannia.md](cc-P33-clean-up-britannia.md): matching lines 72.
- [cc-P378-playtest-plans-10-21.md](cc-P378-playtest-plans-10-21.md): matching lines 235, 236, 286, 287.
- [cc-P42-defect-batch-3.md](cc-P42-defect-batch-3.md): matching lines 46, 53, 54, 55, 58, 59, 62, 65, 66, 94, 101, 504, 526.
- [cc-P46-smith-orders-2.md](cc-P46-smith-orders-2.md): matching lines 161, 178, 187, 354.
- [cc-P47-league-research.md](cc-P47-league-research.md): matching lines 12, 60, 67, 95, 220, 259, 272, 349, 362, 387, 388, 772.
- [cc-P48-league-batch-1.md](cc-P48-league-batch-1.md): matching lines 159, 168, 233.
- [cc-P49-dungeon-chests-research.md](cc-P49-dungeon-chests-research.md): matching lines 412, 437.
- [cc-P52-bug-batch-4.md](cc-P52-bug-batch-4.md): matching lines 52, 54, 226, 282, 284, 291, 292.
- [cc-P54-f12-xp-and-gain-paths.md](cc-P54-f12-xp-and-gain-paths.md): matching lines 123, 124, 451, 572, 619.
- [cc-P55-bug-batch-5.md](cc-P55-bug-batch-5.md): matching lines 166.
- [cc-P58-changelog-catch-up.md](cc-P58-changelog-catch-up.md): matching lines 127.
- [cc-P70-mule-modules.md](cc-P70-mule-modules.md): matching lines 36, 106, 146, 265, 266, 268, 335, 341.
- [cc-P72-level-items-research.md](cc-P72-level-items-research.md): matching lines 207, 224, 310.
- [cc-P73-test-account-wipe.md](cc-P73-test-account-wipe.md): matching lines 425.
- [cc-P75-league-rewards-rethink.md](cc-P75-league-rewards-rethink.md): matching lines 164.
- [cc-P82-artificers-imbuing.md](cc-P82-artificers-imbuing.md): matching lines 1, 3, 9, 11, 12, 33, 37, 59, 69, 82, 152, 168, 179, 231.
- [cc-P91-overnight-playtest-bot.md](cc-P91-overnight-playtest-bot.md): matching lines 41, 203.
- [cc-P95-imbue-boot-fix.md](cc-P95-imbue-boot-fix.md): matching lines 24, 91, 228, 253.

## Validation and elapsed time

- Read back the draft and cross-checked all gameplay sections against the evidence table. Book prices, tier fractions, rank thresholds, join-task rewards, slots, forge range, skill bonuses, and Unravel probability come from the cited defaults. No property-catalogue total or other keyword-derived content count is presented as a measurement.
- Both new Markdown files are ASCII, use LF newlines, and are below 5 MB. The player page contains no em dash, staff command, hidden-achievement name/trigger, or exploit instructions. All relative Markdown links resolve. Sources and Contradictions are the final two sections of the page.
- Existing test sources were inspected only. No new tests, lane tests, C# builds, or PowerShell test scripts were needed for this documentation change. Shell commands ran under Windows PowerShell 5.1 (verified version 5.1.26100.9444).
- Ran the standing progress command with work-copy overrides and `--dry-run`; it completed with exit 0 and printed its report, including existing global overseer-review items. **Existing tooling defect observed:** `tools/progress.py:722` writes `tools/progress.json` inside `build()` before `main()` handles `--dry-run` at `:737`, despite its print-only documentation. This is ours to fix in a separate tooling task, not a gameplay issue. Restored only that generated snapshot byte-for-byte from the initially clean HEAD. No tool fix or generated progress changes are part of P383.
- Final change scope: only this note and `notes/wiki-drafts/artificers-order.md` in the migration work copy. Code work copy clean. No `docs/` edits. Checked the stop-request path between steps; it was absent at each check.

Timing: started 2026-10-22 02:09:41 UTC (October 21, 21:09:41 CDT). Finished 2026-10-22 02:21:28 UTC. Total elapsed: 11 minutes 47 seconds (reading, drafting, and review; no build time).

P383 DONE
