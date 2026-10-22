# P392: open design questions for Chase

2026-10-22. Source snapshot: ShatteredLegacy `b240bb4`, shard-migration `ba2abfb`.
Recommendations below are proposals, not new decisions. Questions come first, grouped by system and ordered by their effect on usable progression and pending builds. `U` identifiers belong to this report, not the project's Q-number series.

## Decisions that block progression or a coherent build

### Levels, loops, scrolls and followers (F-12, F-33, F-35)

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U01 | Must a character reach level 50 before tutorial graduation, or does finishing the tutorial itself earn loop 1? | [P282](cc-P282-f12-numbers-and-level-gates.md), Result / reserve transaction; [P371](cc-P371-graduation-is-the-first-loop.md), decision and Implemented behavior. | P282 models every reset at cap; P371 explicitly makes graduation the first loop, but its reset integration is empty. No level-50 prerequisite exists in that graduation path. | Make graduation the explicit first-loop exception; require the current cap for subsequent loops. State how XP earned during the tutorial carries. |
| U02 | Is the five-level reserve valued at the outgoing cap, with scroll consumption and reset performed together? | [F-12 note](f12-levels-loops-caps.md), Still open 1 / Reserve size and scroll/reset interaction; [P282](cc-P282-f12-numbers-and-level-gates.md), Result. | Five levels, raw credit from level 1 and the 21-reset ladder are settled. The exact valuation and atomic transaction are still proposals; the queue's 25-percent rule is obsolete. | Accept the outgoing-cap five-transition sum, zero at 200, and one confirmed transaction that consumes the next scroll and credits the reserve once. |
| U03 | Which custom combat jobs, dives and Setting floors need a current-level gate after each reset? | [F-12 note](f12-levels-loops-caps.md), Still open 2 / What current level unlocks. | P282 proposes level bands and Setting floor N at current level `95 + 5*N`, alongside the decided loop gate. No later approval found. | Accept that table for custom combat content; keep stock content and permanent capacities outside it. |
| U04 | Which permanent titles, cosmetics and Renown awards should levels grant? | [F-12 note](f12-levels-loops-caps.md), What current level unlocks / For Chase. | P282 proposes milestone titles/badges and +2 Renown per previously unrewarded account level, with no AP or free stats/skills. Unanswered. | Adopt the small once-per-account Renown budget and permanent cosmetic/title milestones; do not pay again on re-climbs. |
| U05 | What names, sources, drop rates, merge recipe, Renown cost and League gates fit the current loop and scroll ladder? | [Feature queue](../docs/feature-queue.md), F-12 Open questions / scroll merging; [F-12 note](f12-levels-loops-caps.md), Scroll sources. | The old five named scroll tiers and realm stages belong to the discarded 1000-cap ladder. P282 confirms twenty +5 keys but explicitly leaves acquisition and merging costs outside its model. | Name scrolls by target cap, retain realm names as cosmetic loop titles, and merge adjacent keys through a data table. Put each required source before its own locked content and cost rates against S2. |
| U06 | How do Keeper skill retention floors, companion ranks, the evo mount and Legacy follower-slot purchases fit the current loop ladder? | [P41](cc-P41-companions-research.md), 11.2; [P47](cc-P47-league-research.md), 6 Still unknown; queue F-12/F-33. | [P389](cc-P389-guide-companions-and-evo-pets.md), Progression reachability and decisions, preserves conflicting old rank/slot tables. Player plus five companions is the later party decision; mount cost and final remapping remain unspecified. | Use five companions plus player; publish one per-loop rank/slot table satisfying the loop-11-with-Tack and loop-21-without-Tack targets, with Legacy slots inside the total. Specify the Breaker retention floor and Legacy node caps in the same pass. |
| U07 | Does the player's loop-based individual skill cap also apply to pets? | [P212](cc-P212-code-intake-batch-1.md), Open questions 4. | [P25 decisions](p25-decisions-2026-10-02.md) 5 settles pet **stats**, not pet skill caps. Pet Training and evo progression do not answer this question. | Keep stock pet-training skill caps separate; apply the level-cap rule to player skills only. This keeps pet power scrolls meaningful. |
| U08 | What playable Bond Trial unlocks an evo pet's final stage? | Queue F-35, Still open; [P65](cc-P65-evo-pets-framework.md), Decisions 5. | [Decision inbox](../testing/decisions.json) `P65-D5` says keep built, which preserves a staff flag; [P389](cc-P389-guide-companions-and-evo-pets.md) and `Mobiles/Evo/EvoPet.cs:50` still say no player trial is designed. | A short repeatable Farmhand trial at the decided loop/XP gate; keep the existing stage and bond on failure. The accepted staff flag is a deferral, not trial content. |

### Earned skill gain to 200 (F-12, F-18, F-20, F-37)

All rows below are still content-design work, not permission to replace every check with unrestricted gains. [October 5 decisions](f12-decisions-2026-10-05.md) chose content for these skills; [P283](cc-P283-skill-gain-paths-research.md) rechecked the actual remaining paths.

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U09 | Do the five casting schools train through a Ward or repeatable special quests, and where is that training unlocked? | [P54](cc-P54-f12-xp-and-gain-paths.md), Decisions 8/13; [P283](cc-P283-skill-gain-paths-research.md), For Chase A. | October 5 explicitly rejected hook G for casting schools, leaving Ward versus quest open. | One League lesson per school unlocks a placed shared Ward; paid repeatable practice must require a qualifying cast, resources and cooldowns. |
| U10 | Which outputs and sinks train Inscription, Alchemy, Cooking and Tailoring above their existing ceilings? | P54 Decisions 11; [P283](cc-P283-skill-gain-paths-research.md), For Chase B; queue F-18/F-20. | Recipe gating and the later BOD ports do not provide the required high-skill content automatically. No later selection found. | Start with paid high-tier orders using obtainable existing outputs; add recipes only with their ingredient and reward sources. Keep potion combat strength independent of training difficulty. |
| U11 | Which high-skill animals teach Taming, Animal Lore and Herding without creating overpowered pets? | [P66](cc-P66-clamps-and-hook-g.md), Decisions 5; October 5 follow-ups; [P283](cc-P283-skill-gain-paths-research.md), For Chase C. | High animals were approved in principle; actual species, source, tame retention and control policy remain open. | New wild variants on existing bodies, with a bridge and tame requirements around 150.1 and 170.1; specify post-tame power and slots before adding spawns. |
| U12 | What repeatable maps or chests train Lockpicking and Cartography through 200? | [P67](cc-P67-craft-ceilings.md), Decisions 4; [P283](cc-P283-skill-gain-paths-research.md), For Chase D. | F-32's planned L5/L6 chests and P127's map port do not settle a complete repeatable path to 200. | Shard survey maps/chests with explicit acquisition, lock difficulty and a bounded reward sink; preserve stock chest rules. |
| U13 | Which shard encounters can train all three bard skills beyond stock difficulty? | [P283](cc-P283-skill-gain-paths-research.md), For Chase D. | The creature-level field is built, but stock bard difficulty is a different input. No eligible target list or revised gain difficulty approved. | Opt in selected nonimmune custom encounters; use level near skill for gain eligibility, leaving stock effects intact and retaining headroom at 199.9. |
| U14 | Is Imbuing's remaining high-skill path improvement commissions or a separate masterwork action? | October 5 decision 12; [P283](cc-P283-skill-gain-paths-research.md), For Chase E; queue F-37/F-43. | P82's rework exists, but the remaining difficulty ceiling is not solved merely by learning advanced properties. | Real improvement commissions with measurable item improvement and ordinary materials; no larger property budget just to manufacture gains. |

### Levelable crafted gear (F-12; P72/P261)

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U15 | Should each qualifying contributor receive full item XP, or should the kill pool be split by damage? | [P72](cc-P72-level-items-research.md), Decisions 4; [P261](cc-P261-levelable-gear-build.md), Headlines 5 / Deviations. | Inbox `P72-D4` accepts full credit on October 18. P261 implements share-splitting and attributes it to its brief. The referenced master design `D:/UO/cc-prompts/design/f-levelable-gear.md`, Design notes, labels splitting an overseer suggestion, **not decided**. No later Chase reconciliation found. | Full credit above the accepted contribution threshold, unless Chase explicitly replaces the October 18 answer. Do not copy P261's attribution as a new decision. |
| U16 | Should item XP use P72's accepted curve or P261's stock XmlLevelItems curve and points? | P72 Decisions 9; [P261](cc-P261-levelable-gear-build.md), Headlines 5 / For Chase 4. | Inbox `P72-D9` accepts `13 x n^1.4`; current `LevelGear/ClusterFLevelGear.cs` uses the quadratic stock curve. The implementation note calls the different brief controlling, without a later recorded Chase answer. | Reconcile explicitly before player release; prefer the accepted P72 curve and recalculate point costs against its pace. |
| U17 | Does Echo of the Loop increase item XP? | [P261](cc-P261-levelable-gear-build.md), Deviations / For Chase 5; [P82](cc-P82-artificers-imbuing.md), custom properties. | P72 says item XP has no echo; the imbue property's design promises extra XP for levelable items. P261 leaves the hook unused. | Keep automatic re-climb echo out of item XP; either make this named property an explicit capped item-XP bonus or rename it to its player-XP purpose. Prefer the explicit bonus its tooltip promises. |
| U18 | Which property costs, ceilings and missing anti-farm limits should the player-facing gear release use? | P72 C.2/C.3 and Decisions 7/8; [P261](cc-P261-levelable-gear-build.md), For Chase 2 / Not built. | Property kinds were accepted, but P261 omits the accepted creature-level floor and per-minute cap and uses a different point budget. Current code's per-kill cap is not the same rule. | Retain accepted property exclusions, shared imbuing slots and caps; add the accepted eligibility/rate limits before player acquisition, then tune costs against U16. |

### Tutorial, account limit and the first home (F-4, F-35, F-44)

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U19 | Does skipping the tutorial count as graduating and opening the island gate? | [P371](cc-P371-graduation-is-the-first-loop.md), For Chase. | Built provisionally as yes, behind `skipCountsAsGraduation`; remedial training is the other explicit option. No later answer found. | Keep yes; veterans may skip without being trapped, while remedial lessons remain available. |
| U20 | Is the player limit still one character per account? | Queue F-4, Answered October 3; F-44, second pass / Open. | F-4 says one, staff/test exempt; the newer F-44 says the number is open. The later text reopens a previously decided rule. | Retain one for players and the stated exemptions; change only with an explicit new number. |
| U21 | Is the inn room truly instanced or a rentable region inside a shared inn? | Queue F-44, second pass; [P212](cc-P212-code-intake-batch-1.md), Open questions 6. | F-44 decides instanced; P212 proposes reopening the shape after source research. No later answer or room build found. | Keep instanced, accessible through any inn; reuse the trial-map approach rather than replacing the player-facing promise with public room stock. |
| U22 | What rent, grace period and non-payment outcome does the inn room use? | Queue F-44, second pass / Open. | Weekly rent is decided; amounts and recovery rules are not. | Low weekly gold rent, a warning and one-week grace; close access on expiry and preserve possessions for bank/claims retrieval. |
| U23 | What room size, lockdown/secure limits and decoration rules teach housing without replacing a real house? | Queue F-44, Open. | No later sizing decision found. | One fixed small room, a small explicit storage budget, and ordinary decorative items; no growth, vendors or production fixtures. Publish exact limits with the room prototype. |
| U24 | May other players visit an inn room, and does it survive a loop? | Queue F-44, Open. | No later answer found. P371 does not implement housing resets. | Owner-invited visitors only; preserve room and belongings through loops, consistent with permanent housing/collection progress. |

### Reachability of existing encounters (F-35; Old Haven)

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U25 | Where should the displaced Old Haven Mages and Vorlak live so their achievements remain earnable? | [P189](cc-P189-cont-old-haven-new-player-safe.md), For Chase / section 5. | They were removed from the tutorial route; the note proposes Deceit but does not place them. No later relocation decision found. | Move both to surveyed Deceit locations, away from the tutorial, retaining their existing achievement keys. |

## Decisions needed before the next subsystem builds

### League jobs, client commissions and utility rewards (F-24, F-33, F-34, F-37)

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U26 | Which real metal ranks replace Steel and Silver for Citizen Commission permissions? | [P47](cc-P47-league-research.md), 7.2; [P376](cc-P376-league-decisions.md), Q4. | No commission implementation or later accepted mapping found. P47 incorrectly numbers Blaze as 11; the generated ladder makes it 12. | Accept at Iron, small posts at Bronze, larger at Verite, public/high-value at Blaze, resolving by metal key. |
| U27 | What posting fees, expiry, listing limits and reward caps should Citizen Commissions use? | P47, 7.2 Numbers (defaults to confirm). | Values are proposed, not accepted by the later bank/rank answers. | Start with P47's 5%/100-gold minimum fee, seven-day default expiry, rank-based posting caps and escrowed tier limits; keep commission Renown outside LifetimeRenown. |
| U28 | What does Infamy do, how does it decay and how do recurring clients unlock better commissions? | Queue F-37, Decided / Infamy / Open questions. | Three-day expiry and 10% Renown penalty are accepted placeholders. The standing axis, titles/effects and recurrence thresholds are still undesigned. | Use a separate decaying commission-reliability axis, affecting offered tiers and shady clients; tune a small recurring-client ladder before implementation. Keep requisitions exempt. |
| U29 | What replaces the dropped Scavenger in Load Harness III, and should II still sort bags or Field Medic II gain ranged bandaging? | [P70](cc-P70-mule-modules.md), Decisions 8/9; [P75](cc-P75-league-rewards-rethink.md), B.3/B.4. | Inbox `P75-D1` drops the auto-looter; current `Mobiles/Mule/MuleModuleData.cs:70-83` still promises its redirect and marks ranged bandaging partial. October 18 did not explicitly answer all B.4 module changes. | Retarget III to the proposed loot-only Overflow to the mule; retain ordinary sorting and self-cure initially; defer the range patch until it supplies a distinct benefit. |
| U30 | Should the League sell extra bank capacity beyond the milestone bonus? | [P179](cc-P179-league-design-pass.md), decision 7; [P280](cc-P280-league-register-build.md), Answer 7; P376 Q9. | P280 explicitly records the bank answer as unanswered and builds nothing. Dropping the Scavenger does not answer this separate Warehouse question. | Do not sell bank capacity now; use the existing milestone ladder and revisit only after a full-bank client check shows a need. |
| U31 | Should League Featherweight satchels survive beside guild satchels and the Field Satchel? | P75 B.2; [P179](cc-P179-league-design-pass.md), utility disposition; P376 Q9. | P179 recommends dropping them; P280's no-weight-sale answer covers backpack upgrades, not explicitly all satchels. No final disposition found. | Drop the duplicate League weight line; let guild satchels supply weight reduction and the League consolidate them. |
| U32 | Which guild-specific resource types, costs and range checks complete the Register's Bank page? | Queue F-34, Answered / costs at build time; [P179](cc-P179-league-design-pass.md), decision 3; [P280](cc-P280-league-register-build.md), Answer 3. | Folding the ledger into the Register is settled. Crafting from the bank remains unbuilt; the old Healers reagent row predates the Alembic ownership change. | Preserve the decided three range tiers and crafting-only scope; move Alchemy resources to the Alembic and specify each guild's resource allowlist and prices in the F-34 build. |
| U33 | Which cross-guild reputation pairs gate mining, lumber and ranger upgrades after the mule? | Queue F-33, First upgrades / Suggested item pairs. | Mule work landed, but the later pickaxe, hatchet and ranger pairings remain suggestions. | Miners plus Smiths for pickaxes, Foresters plus Smiths for hatchets, Rangers plus Tailors for the satchel; size the next item independently. |

### Rolled gathering contracts (F-38, F-20)

Each row comes from [P235](cc-P235-work-order-numbers-pass.md), **Decisions for Chase** (item number shown). No later acceptance or rolled-contract build was found; current `ClusterFWorkOrderSystem.cs` still issues static work orders.

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U34 | Is the proposed gathering pay curve the right initial scale? | P235 decision 1. | F-38 approves one formula but leaves the numbers pass open. | Start at P235's proposed curve and adjust with one global dial after measured play, rather than hand-tuning each material. |
| U35 | Should standing equal gold, with guild tokens at standing divided by 25? | P235 decision 2. | No later answer found. | Yes, one base value and explicit rounded payouts. |
| U36 | Should Rare finds use mined ML gems instead of stock jeweler gems? | P235 decision 3. | F-38 keeps gems with Miners; it does not select the gem list. | Use the mined rare gems, keeping bought jeweler gems out of gathering rewards. |
| U37 | Which harvest window carries the extended wood ladder to 200? | P235 decision 4; [P283](cc-P283-skill-gain-paths-research.md), Lumberjacking row; [P385](cc-P385-guide-gathering-guilds.md), unresolved differences. | P235 proposes tier +/-40; P283 later proposes upper tier +45 with worn-bonus handling. Current harvest teaching still ends early. | Use the shared craft-tier requirements with P283's bonus-safe upper headroom; verify 199.9-to-200. Do not change the crafting gates independently. |
| U38 | Does an expired Rush order downgrade to ordinary pay or disappear? | P235 decision 5. | No answer found. | Downgrade, keeping the player's materials and progress useful. |
| U39 | Which towns get the first Haul depots? | P235 decision 6. | The mule requirement is decided; depot towns are not. | Minoc/Britain for Miners and Yew/Skara Brae for Foresters, as proposed. |
| U40 | Must a Survey gather after acceptance in the named region, or just report a new vein or grove? | P235 decision 7. | No answer found. | Region-tagged gathering after acceptance on the shared engine; keep discovery reporting as its own reward. |
| U41 | Should rolled gathering work wait for the League engine or extend the existing guild ledger first? | P235 decision 8; queue F-38 Check first. | No shared job engine is delivered by P48's rank build or P150's requisitions. | Use the shared League engine; avoid another persistent order format just to bridge the gap. |
| U42 | Do Dawnstone and Rootwood stay out of ordinary rolled contracts? | P235 decision 9. | No answer found. | Yes; keep these dungeon materials on named/dungeon work. |
| U43 | Should offers be four per guild, last six hours, resist decline-rerolling and keep three active jobs? | P235 decision 10. | Separate guild and League caps are decided; this offer schedule is not. | Accept the proposed offer schedule and preserve separate caps. |
| U44 | How many gain checks should a gathering turn-in grant? | P235 decision 11; queue F-20. | Gain checks are approved in principle, not their final count/window. | Three checks, one per third delivered, in the proposed material window; test against ordinary gathering so hand-ins do not dominate. |
| U45 | Must a colored material be reported in the ledger before its contract can roll? | P235 decision 12. | Existing static orders use discovery gating; no later rolled-rule answer found. | Retain the reported-discovery gate. |
| U46 | Should granite roll at twice ingot value, one quarter of offers, behind the stone-mining book? | P235 decision 13. | No answer found. | Accept provisionally; keep the book prerequisite and measure granite collection time. |

### Herbalism and reagent farming (F-51)

The queue's **None at design level** predates the code-forced questions. Each item below is from [P260](cc-P260-herbalism-research.md), **For Chase (decisions the code forces)**. [P382](cc-P382-guild-guide-order-of-the-alembic.md), contradiction 7, confirms those choices were not resolved by the guide.

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U47 | May reagent plants cross with decorative stock plants? | P260 item 1. | No later answer found. | Separate pollen lanes; average only along the reagent ladder. |
| U48 | Is strain tier a separate field instead of a PlantHue value? | P260 item 2. | Stock dye/basket behavior makes the original hue proposal incompatible. | Yes; keep plant color independent and derive the display metal hue from strain tier. |
| U49 | Do tended reagent plants yield indefinitely instead of exhausting stock lifetime resources? | P260 item 3. | Bulk output targets are decided, but stock finite yield does not reach them. | Perennial reagent harvests with type/tier/Herbalism yield; stock decorative plants keep finite yields. |
| U50 | Do reagent beds need slow water and pest upkeep, or remain carefree? | P260 item 4. | Existing mounds have neither; F-51 expects neglect/grace mechanics. | Slow upkeep for reagent beds, two-to-seven-day grace and reduced malady rate; leave stock raised gardens faithful. |
| U51 | Should Herbalism be selectable at creation, using player-built skill-file overrides and the saved-group client patch? | P260 item 5. | No implementation/selection answer found. | Use the proposed override route and allow it as a starter skill once its starter kit works. |
| U52 | Does the Alembic use the higher of Alchemy and Herbalism for guild promotion? | P260 item 6. | The guild's present Alchemy-only rule does not decide its new two-skill policy. | Yes, with recipes still respecting their own skill requirements. |
| U53 | Are stock reagent pickup spawners kept, removed or converted into herb patches? | P260 item 7. | F-51's vendor-only premise was corrected by the survey; no replacement ruling found. | Keep stock pickups for fidelity and add the new foraging lane. If conversion is preferred, record it as an explicit deviation. |
| U54 | Is graveyard digging part of the reagent build? | P260 item 8. | No engine exists for it in the surveyed shovel path; no later decision found. | Defer to phase 3; vendors and existing creature/hunt sources cover necro reagents meanwhile. |
| U55 | What happens to the garden familiar when its house collapses? | P260 item 9. | No later answer found. | Preserve it as a deed in a durable moving crate/claims store. |
| U56 | Do yard items use house lockdowns or a separate house-sized budget? | P260 item 10. | Radius/count by house size is decided; accounting is not. | A separate small explicit yard budget, while stored containers keep ordinary storage rules. |
| U57 | What survives expiry of a public plot? | P260 item 11. | Warning and weekly guild rent are decided; loss rules are not. | Crops become twigs; preserve owned items in bank/claims storage after warning. |
| U58 | Should growth use a dedicated one-minute sweep instead of autosaves? | P260 item 12. | No later answer found. | Yes, persist timestamps and use one shared timer. |
| U59 | Does phase 1 reuse a fern for Blood Moss or wait for new plant art? | P260 item 13. | No later art choice found. | Reuse a stock fern for the first build; art remains a later Chase-owned request. |
| U60 | Are reagent bed deeds crafted through Foresters or sold by the Alembic? | P260 item 14. | No later answer found. | Carpentry recipe through Foresters; Alembic supplies seeds and farm consumables. |

### Additional dismount sources (F-39, F-33)

These are the unaccepted gameplay rows in [P234](cc-P234-dismount-sources-design.md), **Decisions for Chase**. The build order and deviation entry are implementation obligations, not separate questions. `Mobiles/Mule/MuleModuleData.cs:116-118` still marks the Wraps stubbed.

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U61 | What hit qualifies for a big-monster dismount roll? | P234 item 2. | No later answer found. | At least 15% of rider maximum hits after resists, as proposed. |
| U62 | Which monster families dismount, with what chances and cooldowns? | P234 items 3/4. | F-39 approves the idea, not the source list or rates. | Start with P234's family list, 10% top families/5% others, ten-second creature cooldown and +5 for paragons; exclude champions/Peerless initially. |
| U63 | Are pets and summons excluded from the new passive dismount rolls? | P234 item 5. | No later answer found. | Yes; trained Dismount remains its own ability. |
| U64 | Which caves are no-ride areas, and is all Rootdeep or only its crawlway included? | P234 item 6. | No later answer found. | Proposed caves/mines plus Orc/Painted Caves; Rootdeep crawlway only. |
| U65 | Does a low ceiling ground gargoyles, and can Steady Hoof Wraps resist it? | P234 items 7/8. | No later answer found. | Block mounting, dismount/ground on entry without daze; Wraps cannot defeat a ceiling. |
| U66 | Which traps dismount and how long is the daze? | P234 item 9. | No later answer found. | Use its fire/blast 25%, jolt 15%, dart/magic 10%, hold 50%, poison/gas 0 table and five-second daze. Route every attempt through the shared check. |
| U67 | Which wildlife charges riders and where may it happen? | P234 items 10/11. | No later answer found. | Start with its species/rate table, running riders within six tiles, creature/rider cooldowns; wild areas only, outside guarded towns, houses and dungeons. |

### Guild headquarters and menu template (F-49, F-9)

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U68 | Is P177's shared guild-menu look approved for P178 and future guild books? | [P177](cc-P177-guild-menus-template-mockups.md), Deviations / For Chase; [P280](cc-P280-league-register-build.md), template limitation. | [P378](cc-P378-playtest-plans-10-21.md), For Chase item 4, still calls it an unapproved visual proposal; P178 remains held. | Review the seven mockups once and adopt one template, recording specific layout changes before conversion. |
| U69 | Does the League use Castle British's keep or a new courtyard hall? | [P151](cc-P151-guild-halls-survey.md), Decisions 1. | F-49 fixes Britain grounds; later decor packs do not select a building. | Reuse the empty keep, as surveyed. |
| U70 | Is the Thieves' Den headquarters on Felucca or Trammel? | P151 Decisions 2; queue F-49 Open. | [P384](cc-P384-guild-guide-thieves-den.md) still marks facet/building undecided. | Felucca, reusing Buccaneer's Bath, with a safe travel stop. |
| U71 | Is the Maritime hall on Felucca Ocllo or moved to a Trammel port? | P151 Decisions 3. | Trammel Ocllo is Old Haven; no later answer found. | Felucca Ocllo, honoring the chosen town; explicitly provide safe arrival. |
| U72 | Do Rangers use Skara Brae's free Counselor's Guild or share the stock Rangers' Guild? | P151 Decisions 4. | No later choice found. | Reuse the free Counselor's Guild. |
| U73 | Does the Dojo get a new hall by Makoto-Jima gate or share the occupied stock dojo? | P151 Decisions 5. | No later choice found. | New hall on the surveyed north field, after the footprint/world check. |
| U74 | Do Artificers get a new plaza hall or reuse the larger building north of Royal City's bank? | P151 Decisions 6. | Existing outdoor post is not a headquarters; [P383](cc-P383-guild-guide-artificers-order.md) preserves that distinction. | Reuse the larger free building unless the plaza identity is essential. |
| U75 | Does the Alembic get a new swamp-edge hall or share Papua's alchemy shop? | P151 Decisions 7. | No later choice found. | New swamp-edge hall, with its exact plot checked for player/world conflicts. |
| U76 | Are the remaining surveyed hall sites/facets and their decor sets accepted, and how are travel stops unlocked? | Queue F-49 Open; P151 Summary; [P265](cc-P265-guild-hall-decor-packs.md), What an F-49 placement prompt needs. | P265 supplies templates, not final hall selections or a travel network. Native Tokuno/Malas/Ter Mur halls cannot all be placed on Trammel. | Accept P151's remaining native-facet/reuse proposals, choose decor per hall, then design one rank-aware travel service that also keeps New Haven chapters. |

## Smaller policy choices, reward design and tuning

### Requisitions and Leads (F-47, F-48)

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U77 | Do live Leads preserve their requests across the daily refresh? | Queue F-47/F-48; [P150](cc-P150-requisitions-and-leads.md), Decisions 3; [P376](cc-P376-league-decisions.md), Q7. | Built as yes to reconcile a daily board with a three-day Lead; explicit acceptance of the exception is still asked in P376. | Accept the built exception and keep its request slot occupied until completion/expiry. |
| U78 | Are the Fame/group/area extra-roll and pity rules the accepted replacement for literal doubled loot-table odds? | Queue F-48 Open; P150 Decisions 4/5; P376 Q7. | Code uses its own extra roll and Fame floor, not a measured multiplier of natural item odds. No later acceptance found. | Accept the implementable personal extra roll/pity rule, and describe it accurately instead of promising literal 2x natural odds. |
| U79 | Should requisitions pay non-member standing immediately or bank it until the Apprentice task? | Queue F-24 banking; P150 Decisions 2; P376 Q8. | Built immediate payout; the October 3 exception predates requisitions and explicitly names existing payouts. This new system is not expressly covered. | Keep immediate lowest-tier requisition payout; reserve delayed banking for League jobs and document the distinction. |

### Commissions, crafting, loot boxes and seasonal rewards (F-20, F-37, F-40 to F-43, F-22)

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U80 | Is Client Commissions the final name for NPC work, distinct from player-posted Citizen Commissions? | Queue F-37, name proposed / not confirmed. | Current Smith commissions do not decide the future shared-engine name. | Yes; use both distinct names consistently. |
| U81 | What are the first epic recipes, components, sources and power limits? | Queue F-42, Not designed yet; F-43, custom Band V+ list. | F-40 can supply hinting components; no later epic-crafting design found. | One complete boss/box-only recipe with obtainable components and a bounded improvement budget before expanding the list. |
| U83 | Should the Dented Box replace the normal achievement box or be additional? | [P263](cc-P263-noted-by-the-system-achievements.md), The reward table / One decision. | Built as replacement; no later answer found. | Replacement, as built, with one guaranteed joke item; avoid doubling achievement rewards. |
| U84 | Where do Plate Socks and the two toe rings come from, and what unlocks the extra bracelet? | [P262](cc-P262-accessory-slots.md), For Chase 2/3. | The accessory jokes are not in P263's listed Dented rewards. League bracelet rank 9 / companion rank 5 are provisional; no later choice found. | Put the joke accessories in the Dented pool; retain Valorite for the player bracelet and map the companion gate to the final rank ladder. |
| U85 | Should full cooking/furniture BOD quality and material rewards be supported? | [P123](cc-P123-port-bulk-orders-crafts.md), Deviations 1. | The port deliberately excludes impossible exceptional/material requests; food/furniture quality support remains a separate follow-up. | Build real craft-produced quality/material support before offering those requests; keep current filtered deeds until then. |
| U86 | Can Eodon kills award the stock recipe scrolls under account recipe gating? | [P198](cc-P198-port-eodon-remainder.md), 7 Still open; Q-064 in [codex questions](codex-questions.md). | Inbox `T-008-D1` asked for the missing gate/spawns first; P198 provides the generator/content, but explicitly leaves recipe gating unanswered. | Yes, as wild recipe sources feeding the existing account store; add only recipes whose outputs and resources are obtainable, then grow toward the full faithful table. |
| U87 | Which remaining Clean Up rewards should be completed, and how should the fishing set bonus work? | [P175](cc-P175-cont-clean-up-britannia-finish.md), Decisions 5 / remaining reward table. | Many old missing rewards were ported; the fishing bonus and system-backed reward tail remain separate decisions. | Port independent exact rewards; use the smallest faithful fishing-bonus hook and defer system-backed items rather than invent substitutes. |
| U88 | What real daily gifts replace the winter advent calendar's candy-cane placeholders? | [P266](cc-P266-new-haven-winter-decor.md), Decisions 6. | No later gift table found. | A small dated cosmetic/consumable table, avoiding power/scroll rewards; keep an explicit per-character claim policy. |
| U89 | Should the community Halloween layer and Hestia fireplace be added after source/terms clearance? | [P267](cc-P267-halloween-bank-decor.md), community-art follow-up; [P266](cc-P266-new-haven-winter-decor.md), Decisions 1. | Stock Halloween is built; the missing community layer and uncleared fireplace are not. | Keep the shipped stock/MrRiots layers; queue only specifically cleared pieces and follow the existing Chase art-request workflow. |

### Other long-term reward and content choices

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U90 | What cooldown and reward-reset policy makes the Fountain of Youth safe for normal play? | [P192](cc-P192-cont-fountain-of-youth.md), Decisions 1/2. | Built restrictions default off; resetting tutorial/trainer rewards can reissue items. No later production policy found. | Thirty-day account cooldown; preserve already-claimed tutorial/trainer rewards, or explicitly disable their reset on normal play. |
| U91 | Should secret achievements show a question-mark row before discovery? | P192 Decisions 3. | Not built; hidden achievements currently stay hidden. | Keep fully hidden; do not expose a secret checklist merely to fill page rows. |
| U92 | Are flying mounts wanted, and should they cross water through pinned flight mechanics? | [P212](cc-P212-code-intake-batch-1.md), Open questions 3. | Approval to ship the red-dragon body (`P139-D6`) is not a flight-mechanics decision. | Defer until a specific rideable mount is available; then use pinned flight plus the smallest movement hook, without altitude simulation. |
| U93 | Should handed-in taming animals disappear or populate a visible Rangers' pen? | P212 Open questions 7. | Existing hand-ins consume the creature; later bot checks do not select new pen fiction. | Release/delete for turn-in, with bounded decorative pen animals unrelated to actual deliveries. |
| U94 | Are Treasures of Events items wanted now, and does the prior GPL permission extend to Feng's wider collection? | P212 Open questions 2/5; [October 14 decisions](decisions-2026-10-14.md), servuo.dev assessment. | GPL permission is explicit for the Animal Lore dashboard only; P212 reopens broader collection use. No blanket ruling found. | Keep that narrow permission; select reward classes when their source framework needs them, verifying original item stats and credits individually. |
| U95 | What numeric cap should the accepted bestiary-plus-slayer bonus use? | [P93](cc-P93-servuo-code-port-assessment.md), For Chase; inbox `P93-D13`. | Chase answered cap the combined bonus, but supplied no number. P364's hunt bestiary is a different system and supplies no combat bonus cap. | Set a named combined cap when that reward is built; start at the existing slayer ceiling rather than introducing a larger stack. |
| U96 | Which music tracks should play in which regions, monster fights and boss fights? | [P368](cc-P368-added-music-areas-monsters-bosses.md), Open questions 1/2. | Playback infrastructure exists; unselected/flagged music still needs Chase's per-track use and source decision. | Select a small cleared region/boss set in Music Room, with exact target keys; leave all other tracks unshipped. |

### Staff tooling and household policies (no F-number)

These do not block shard content. Routine deployments, visual checks, deleting scratch and submitting upstream reports are actions, not design questions, and are not promoted into this decision list.

| ID | Question | Asked in | Later answer or remaining conflict | Recommendation |
|---|---|---|---|---|
| U97 | Should the map-check heuristic honor a solid surface over wet land, and should no-tiledata be reported? | [P135](cc-P135-vseuoaware-staff-commands.md), Open questions 6. | The note deliberately leaves the heuristic as surveyed; no later semantics ruling found. | Follow server standability for a valid surface at the standing height; retain missing-tiledata as a diagnostic warning. |
| U98 | Should footprint checks become a report in StampLayout, and should map reports be capped or pruned? | P135 Open questions 1/2. | No later product decision found; current commands are independent diagnostics. | Attach a nonblocking report when the importer has real footprints; retain recent reports with a configurable age/count cap. |
| U99 | Should read-only map diagnostics also have a Shard Console group? | P135 Open questions 5. | Staff Hub and Map/Art syntax panel are present; no explicit choice for an additional group found. | Keep the existing panel and Hub; add a group only when the console action can be reused by its web twin. |
| U100 | Should a new building stamp's undo survive restart, and should Visual Builder gain categories/Clone? | [P98](cc-P98-building-duplicator.md), Deviations; [P100](cc-P100-visual-builder.md), Deviations. | Stamp undo is in memory; Visual Builder has its own persistent undo. Categories/Clone were left out, not answered by the other tool. | Persist stamp ownership/history before expanding destructive editing; defer categories/Clone unless search proves insufficient. |
| U101 | Which household Golems may run Docker, during which hours, and how is Autologon enrolled? | [P186](cc-P186-cont-golem-join-kit.md), For Chase 1/2/4. | Inbox `P126-D7` settles **Stone** as no Docker, not the daughters' machines or their schedules. | No Docker on laptops by default, school-night hours chosen per owner, and interactive Autologon enrollment instead of a password argument. |
| U102 | Should the join kit distribute the shared art library and intake-ideas index to other PCs? | [P201](cc-P201-deployable-traps-design.md), Deviations/decisions 2. | No later explicit distribution decision found; remote research can still lack those sources. | Mirror the small text inventories with the kit; keep large sources outside git with stamps and explicit local acquisition. |
| U103 | Should the print queue be available away from home? | [P109](cc-P109-haven-print-queue.md), Deviations 5. | Built LAN-only; the later shard intranet's Tailscale policy is not a print-queue authorization. | Tailscale-only if remote access is wanted; keep customer data off public unauthenticated routes. |

## Settled, docs not updated

These are not questions to send back to Chase. Some answers defer work or leave an implementation gap; that does not erase the answer. Built source is evidence of code behavior, not proof of deployment.

| System / old question | Settlement and evidence | Documentation follow-up |
|---|---|---|
| F-12: 1000 cap, +25 steps, separate twenty post-cap loops, scrolls versus loop caps | Queue's dated October 3 ladder, [P282](cc-P282-f12-numbers-and-level-gates.md), and `Tutorial/ClusterFLoops.cs:31`: 50, 100, +5 to 200 at loop 21. Twenty scroll steps. | Remove the obsolete ladders and five-tier scroll examples; retain U02/U05's genuinely unspecified detail. |
| F-12: which XP curve, pacing, overflow and raw reserve-credit policy | [October 5 decisions](f12-decisions-2026-10-05.md), Levels and XP, accepts S2, the opening pace, raw credit from level 1, terminal zero reserve and lost overflow. P282 explicitly preserves these. | Do not ask for S1/S2/S3 again; label playtime tables estimates and separate the new exact reserve proposal. |
| F-12: stat resets, stat ceilings, free points and veteran +50 | [P25 decisions](p25-decisions-2026-10-02.md) and F-12 note Stats supersede the earlier level-linked ceilings/veteran award. Stats persist; no free skill/stat points. Pet **skill** policy is still U07. | Rewrite F-13's obsolete veteran-cap paragraph; do not infer a new stat award from it. |
| F-12: live gain rate x1 versus the later rate | [P191](cc-P191-cont-earned-skill-gain.md), Deviations 7, explicitly supersedes October 5's x1 with the October 19 recommendation; `ClusterFSkillGain.cs` now defaults to two attempts and 1x amount. | Preserve the old decision as history, not current configuration. Running settings were not checked. |
| F-5/F-35: tutorial order, recruiter, voice, vision, graduation and Young | [October 14 decisions](decisions-2026-10-14.md), Tutorial, answers P80; [P371](cc-P371-graduation-is-the-first-loop.md) makes graduation a real first loop and keeps Young's ordinary timer. | Mark P80's old open list answered and promote the graduation/Young decision. U01/U19 are the remaining edge policies. |
| F-35: evo bodies, hues, stats, picks, release, names and animation policy | Queue F-35 / [evo handoff](f35-evo-pets-handoff-2026-10-05.md), then inbox `P65-D1` through `D10`: keep built. | Stop presenting the accepted placeholders as unanswered approvals. Bond Trial remains deferred (U08); real owner-loop integration is implementation work, explicitly left by P371. |
| F-33: drop the Clockwork Scavenger as auto-looter | Inbox `P75-D1`, October 18, explicitly accepts dropping it. | Correct queue F-33 and P376 Q9's claim no answer exists. The mule tooltip still needs changing; do not resurrect the old reward. |
| League utility: Field Salvager, Corpse Claim, Courier, Expedition Ledger and pricing | Inbox `P75-D2` through `D7`: forge rule; 12-tile/10-second Claim; Courier **any loot**, overflow to mule; Ledger yes after jobs; F-13 price range; no DisableFeatures action. | Record these answers separately from U29-U31. Exact party-kill eligibility for Claim was not separately answered by the range-only answer; keep pinned lawful looting rights as the default. |
| Extra facets | Inbox `P76-D1` through `D8`: author-permitted maps with credit, Proving Ward first, provisional names, main package, tools at wiring, Siege loop-gated, before wipe, revisit CALYPSO. | These are approved directions; a download or build still being absent is not another scope question. |
| Alembic and recipe-gating defaults | Inbox `P77-D1` through `D8` and `P78-D1` through `D10`: keep built names/currency/NPC/task, no extra mule module, existing gates/merged books/prices/hints, no reading skill floor. | F-43's old rank-name and price questions have answers. Do not add an Alembic module on the strength of old one-per-guild prose. |
| Achievement boxes and Artificer rework defaults | Inbox `P79-D1` through `D8` and `P82-D1` through `D5`: keep built account scope, tier rules/leather repeats/gear rolls/placeholders/fanfare, rank-4 handling/toolkit access/forge bonus/skill-property rank/flavor. | These are accepted defaults; future playtest tuning is not an unanswered design question. P371 supersedes the box loop placeholder. |
| F-9/F-11/F-15/F-19: resource order, bank essences, Wren, bank overrides and patch-note page | [P22 decisions](p22-decisions-2026-10-01.md), items 1-5; P27 widens essences to bank. | Keep pack-before-bank, Wren at z56, automatic bank limits and `uo:patch_notes`. Wiki sidebar publication is an action. |
| F-12/F-26: guard reveal, thief clamp, craft gain and high-skill effects | October 5 decisions and October 6 follow-ups settle P54/P66; P67/P71 implement the craft/effect choices. | Do not revive P57's uncatchable-with-gear question, the optional guard fix or the old high-effect clamp alternatives. |
| F-13/F-19/F-24: ranks, story milestones, chapter count and Renown spenders | Queue F-24's October 3 answers; `ClusterFLeagueRanks.cs:123,483-505` has six named chapters including Blaze/Mythril; `ClusterFBankLimit.cs:26-47` adds 100 per milestone. P229/P243/P280 spend Renown. | P376 Q1/Q2/Q3/Q5 are settled. Fix five/every-third/per-rank/no-spender wording. Citizen permissions remain U26. |
| F-13: AP and title totals | [P376](cc-P376-league-decisions.md), Q6 Evidence, explains dated counts; [P387](cc-P387-guide-achievements-and-loot-boxes.md) avoids stale totals. `LeagueShop/LeagueShop.cs` is the title catalogue. | Prefer names/unlock conditions over a volatile published ceiling. P376's own visible-AP subtotal does not support its claim that the 1000 tier needs hidden achievements. No new AP recount is claimed here. |
| F-25/F-18/F-20: banking, direct large fills, rank caps and ordinary BOD ports | Queue F-25's last answer says 3/1 was P42 only; P55 implements bank/cash-out. P118/P122/P123 later port ordinary craft BODs with OSI points, while Society keeps its custom seals. | Mark delivered pieces and distinguish approved future rank caps/skill checks from the still-fixed implementation. Missing implementation does not reopen those decisions. |
| F-26/F-28/F-29 | P226, P227 and P228 implement Arms Lore, extended wood tables and exceptional material scaling. `ClusterFWoodBonuses.cs` supplies the separate custom-wood table. | Mark these built; retain code's explicit separation of stock x1.5 material scaling and extended woods' own exceptional rows. |
| F-30/F-31/F-32 | P51 restores Raptor behavior; P230 builds Events; queue F-32's October 5 block answers all seventeen P49 decisions. | Do not ask P49's timer/tiers/odds/window/party/icon questions again. Surges' one-at-a-time, ordinary loot and insurance-fee behavior are built defaults, not blockers. Dungeon-chest rollout still needs implementation/verification where absent. |
| F-21/F-22/F-23/F-36/F-46/F-50 | P237 community art, P34/P266 winter, P81/P111 paperdolls, P238/P278 boots, P139/P140 creature-body route, P137/P176 satchel routing are built. | Replace early ready-to-batch and route-unknown statements with these notes. Essence Shards are currency, not missing physical satchel items. Art appearance and placement checks remain tests. |
| F-47: Appraiser prices/posts, ordinary items and Clean Up double credit | P150 supplies `Requisitions/Appraiser.cs`, `RequisitionsBoard.cs` and table settings; `RequisitionSystem.cs:248-253` pays and deletes the item, awarding no Clean Up points. | F-47's original formula/town-list/no-tag/double-dip proposals are settled in code. Distinguish them from U77-U79's design conflicts. |
| Levelable gear: acquisition, kinds, companion gear, reset dormancy and trade | Inbox `P72-D1/D2/D3/D5/D6/D8/D10`: design-only rebuild, League unlock then crafted consumable, death payout, dormant bonuses with item kept wearable, helper gear, allowed properties and tradeability. `LevelGear/SmithsSealDeed.cs:1-4` still has no player source. | The acquisition answer is missing implementation, not wholly unanswered; P261's re-ask should cite it. U15-U18 isolate actual conflicting rules and budgets. |
| F-40: surprise-only boxes versus shop boxes | F-13 approves shop boxes; `LeagueShop/LeagueShop.cs` sells them; inbox `P79-D1` through `D8` keeps the existing box rules. | Keep the shipped shop products. F-40's later surprise-only suggestion was not adopted in code and must not silently replace the approved shop. |
| Music account scope, staff diagnostics and ordinary deed materials | `Music/ClusterFShardMusic.cs:375-380` stores the off switch per account. P135 follows test-only overlay scope; P170 keeps OSI's any-material plain deeds. | These are explicit built policies. Optional changes raised alongside them are not missing implementations; retain them until a replacement is requested. |
| Older drop and customization defaults | `Miasma-pinned-waiting-drop.patch` preserves pinned's sixteen-case drop body (P7); P127 later ports the treasure-map/SOS/monster-steal content P8 had priced; P129 renames our Drelgor to Vorlak and ports ServUO's Drelgor. | Old stop/choose-the-port questions are superseded by these source changes. Do not count their historical delivery checklists as current blockers. |
| Traps: skills/guild/PvP/practice lesson | [P275](cc-P275-deployable-traps-build.md), What each decision became / Deviations, builds P201's design with monster-only default, Remove Trap setting and Tinkering kits. | Stop asking the original whole design table. Iron kits stopping gains at 130 follows the decided craft ceiling; adding higher-tier kits is content work. |
| Ankh, kitsune, Rootdeep, stealing, script publishing and combat defaults | Inbox `P137`, `P138`, `P139-D6`, `P140`, `P141`, `P142`, `P144` and `P145` answers settle the older alternatives. P188 completes the later Rootdeep geometry. | Keep working/decoration ankh distinction, both-sex kitsune wear, approved bodies/layout/drops, durable stealing state and accepted script policies. P141's nightly rerun is overtaken by time, not a design question. |
| Haven/intranet/live retirement | October 14 decisions plus P108 retirement and P133 Tailscale-only dashboard supersede old live/container/public-host questions. | No connection/deploy was made in P392. Don't turn retired live's load prompt, old hostnames or scratch deletion into Chase design work. |
| Golem, console and play-test defaults | Inbox `P126-D7`, `P155-D9`, `P160-D2`, `P161-D2`; P131 phrase loosening; P132 layout/DPI; P182/P187 web controls; P153 explicit model overrides. | Stone has no Docker, phase 2 was requested/built, and later console behavior answers old suggestions. Preserve U101's genuinely machine-specific questions. |
| P18: discoveries and bestiary per account or per character | Current `ClusterFAccountData.cs` retains ore/wood/imbuing discoveries and encountered creatures on the account; guild and League records use their character tables. P13, P69/P70 and P389 build on that separation. | P18's original alternatives are settled in the maintained persistence model; don't migrate these collections merely because guild standing moved. |
| Small built balance/UX choices | P67 supersedes P61's gain-band proposal; P170 supersedes the stale teaching-order/set-selection concern; P57 supplies the custom clilocs; P226/P227/P239 specify maintenance/wood/con-band defaults. | Keep the implemented numbers/labels until playtests justify tuning. Optional invitations to alter working values are not new blockers. |
| Built staff-tool choices | P132 supersedes the old Plain/DPI/readability proposals; P108/P133 supersede old live/dashboard controls; P187 establishes console/web parity. P86 leaves WiFiman state alone; P135 keeps the overlay test-only. | Report missing functionality separately from questions already answered by later implemented behavior. |

### Accepted directions that still need delivery

- **F-9/F-43 top-guild trials, F-24 jobs/story trials and F-37 commission move:** approval and major shape exist; absence of code is a backlog item. U26-U28 and U68 identify the outstanding choices, rather than asking whether those systems are wanted again.
- **F-40/F-41 contents tuning and custom-client fanfare:** the server phase is built and its default rules are accepted. Actual voice/effect assets, audio testing and later content tables belong to the phase-2/art work; no unrecorded voice-tool preference is treated as an answered decision.
- **Levelable item acquisition and loop integration:** U15-U18 must be reconciled, but P72's accepted acquisition/dormancy/ownership choices should be implemented without re-asking the entire design. The current staff-only Seal and empty F-12 reset hook do not establish player availability.
- **P65-D5 and P77-D6:** keep-built means a deferred Bond Trial and no Alembic mule module, respectively. It does not approve an invented trial or a new module. The Scavenger's cosmetic name remains optional future content; only its auto-looter role was explicitly dropped.

## Boundaries, evidence and review coverage

- Read both work-copy AGENTS files first, then governing-doc index, direction and tasks. Read `docs/feature-queue.md` end to end. Audited every top-level `notes/cc-P*.md` for For Chase, Still open, Decisions and Open questions sections, including inline versions and differently named decision lists. Followed candidates into the dated decision records, `testing/decisions.json`, the overlay, later notes and relevant canonical code. The scan manifest below includes notes with no matching section and review-only notes; it is the file list beside the source count, not a count of open questions.
- The local inbox records 144 answered entries (the key inventory was enumerated during review). An answered keep-built placeholder can defer a feature; it cannot invent its missing player quest. Conversely, pure implementation defaults, optional tuning invitations and visual checks are not reopened when later code/answers already establish behavior.
- Source code paths in this report are relative to ShatteredLegacy `server/customizations/`, unless otherwise stated. No `server/uo/` tree was read. Source-default behavior is distinguished from running settings, world placement and player reachability.
- Unverified: Haven/live state, unmirrored answers made after this checkout, active game configuration, actual XP pacing, visual/art approval and unresolved runtime defects reported in P379. No external service, client, container or account was used. No web research was necessary for this repository-only audit. P392 neither approves a new rule nor changes implementation.
- Routine client checks, bug fixes, scheduling/deployment actions, art production/approval and duplicate older formulations are omitted from the open-design list. Examples: P30 scratch cleanup/upstream filing, P134 tool authorization, P135 flaky tests, P139 body look, P152 art review and P198 running GenEodon. Their absence here is not a claim that those actions happened.
- Only this notes deliverable is intended to change. No new tests or repository gates are required for a docs-only audit; final checks are editorial/source checks, not added test cases.

<details>
<summary>Reviewed source-note manifest: 305 files</summary>

```text
cc-P4-fiddle-me-this.md
cc-P5-player-updater.md
cc-P6-status-publisher.md
cc-P7-pinned-waiting-drops.md
cc-P8-loot-tables-and-d35.md
cc-P9-test-center.md
cc-P10-updater-polish-and-d36.md
cc-P11-account-data-serializer.md
cc-P12-audit-correction.md
cc-P13-grove-tracking.md
cc-P14-newhaven-guild-mapping.md
cc-P15-guild-starter-path.md
cc-P16-mine-camp-tents.md
cc-P17-playtest-bugs-1.md
cc-P18-reset-stone-young-craftx.md
cc-P19-registrar-office-decor.md
cc-P20-skill-scaling-research.md
cc-P21-console-world-commands.md
cc-P22-small-features-1.md
cc-P23-live-defect-sweep.md
cc-P24-new-haven-dungeon-research.md
cc-P25-stats-above-125-research.md
cc-P26-animated-runestone.md
cc-P27-defect-batch-1.md
cc-P28-launcher-account-profiles.md
cc-P29-defect-batch-2.md
cc-P30-modernuo-upgrade-research.md
cc-P31-registrar-office-cleanup.md
cc-P32-spawner-importer-bods-self-repair.md
cc-P33-clean-up-britannia.md
cc-P34-winter-decor.md
cc-P35-clean-machine-test.md
cc-P36-dungeon-build-1.md
cc-P37-upgrade-prep.md
cc-P38-engine-upgrade.md
cc-P39-test-shard-cutover.md
cc-P40-custom-client-research.md
cc-P41-companions-research.md
cc-P42-defect-batch-3.md
cc-P43-stop-timeout-and-cutover.md
cc-P44-wait-for-ea-patch.md
cc-P45-companion-probes.md
cc-P46-smith-orders-2.md
cc-P47-league-research.md
cc-P48-league-batch-1.md
cc-P49-dungeon-chests-research.md
cc-P50-chest-mimic-monster.md
cc-P51-staff-hub-and-raptor-pack.md
cc-P52-bug-batch-4.md
cc-P53-two-hundred-cap.md
cc-P54-f12-xp-and-gain-paths.md
cc-P55-bug-batch-5.md
cc-P56-smith-economy-and-labels.md
cc-P57-batch-6.md
cc-P58-changelog-catch-up.md
cc-P59-evo-pet-body-sheet.md
cc-P60-console-commit-button.md
cc-P61-batch-7.md
cc-P62-kitsune-walk-test.md
cc-P63-console-package-and-deploy.md
cc-P64-patch-history-gump.md
cc-P65-evo-pets-framework.md
cc-P66-clamps-and-hook-g.md
cc-P67-craft-ceilings.md
cc-P68-console-package-check.md
cc-P69-mule-core.md
cc-P70-mule-modules.md
cc-P71-high-skill-effect-scaling.md
cc-P72-level-items-research.md
cc-P73-test-account-wipe.md
cc-P74-autopilot-console.md
cc-P75-league-rewards-rethink.md
cc-P76-extra-facets.md
cc-P77-alembic-guild.md
cc-P78-recipe-gating.md
cc-P79-loot-boxes-fanfare.md
cc-P80-new-player-tutorial.md
cc-P81-paperdoll-sos.md
cc-P82-artificers-imbuing.md
cc-P83-play-test-queue.md
cc-P84-console-uo-skin.md
cc-P85-status-dashboard.md
cc-P86-console-vpn-disconnect.md
cc-P87-console-readability.md
cc-P88-shared-menu.md
cc-P89-haven-pages-plan.md
cc-P90-feature-ideas.md
cc-P91-overnight-playtest-bot.md
cc-P92-port-list-target.md
cc-P93-servuo-code-port-assessment.md
cc-P94-autopilot-progress-console.md
cc-P95-imbue-boot-fix.md
cc-P96-fix-test-shard.md
cc-P97-bug-reports.md
cc-P98-building-duplicator.md
cc-P99-golem.md
cc-P100-visual-builder.md
cc-P101-console-websites.md
cc-P102-bot-nightly-archive.md
cc-P103-tazuo-client-command.md
cc-P104-uorespawn-read.md
cc-P105-haven-h1-host-agnostic.md
cc-P106-shard-questions.md
cc-P107-haven-ops-move.md
cc-P108-retire-live.md
cc-P109-haven-print-queue.md
cc-P110-haven-mega-dashboard.md
cc-P111-tazuo-paperdoll-option.md
cc-P112-playtest-bot-icon.md
cc-P113-console-window-icon.md
cc-P114-test-shortcuts-our-build.md
cc-P115-playtest-who-and-how.md
cc-P116-console-tab-scroll.md
cc-P117-fresh-login-bulletin-regression.md
cc-P118-port-bulk-orders.md
cc-P119-port-creatures-part1.md
cc-P120-port-pet-training.md
cc-P121-pet-ability-core.md
cc-P122-port-bulk-orders-core.md
cc-P123-port-bulk-orders-crafts.md
cc-P124-package-ships-our-tazuo.md
cc-P125-golem-long-run-toggle.md
cc-P126-second-machine-design.md
cc-P127-port-treasure-maps-monster-stealing.md
cc-P128-port-consumables-crafting-gaps.md
cc-P129-port-creatures-part2.md
cc-P130-pet-training.md
cc-P131-wake-golem-from-console.md
cc-P132-console-layout-and-art-slots.md
cc-P133-haven-intranet-dashboard.md
cc-P134-vseuoaware-art-checks-mcp.md
cc-P135-vseuoaware-staff-commands.md
cc-P136-status-page-self-judging.md
cc-P137-usable-ankhs-and-playtest-fixes.md
cc-P138-kitsune-paperdoll-refit.md
cc-P139-rootdeep-burrows.md
cc-P140-rootdeep-burrows.md
cc-P141-rootdeep-burrows.md
cc-P142-monster-stealing-shard-rules.md
cc-P144-legion-scripts-updater.md
cc-P145-combat-script.md
cc-P146-playtest-decisions-inbox.md
cc-P147-achievements-button.md
cc-P149-away-mode-and-email-controls.md
cc-P150-requisitions-and-leads.md
cc-P151-guild-halls-survey.md
cc-P152-art-requests-openai.md
cc-P153-queue-notes-and-package-whats-new.md
cc-P154-console-responsive.md
cc-P155-web-console-phase1-status.md
cc-P156-night-shift-batches.md
cc-P157-plain-english-emails.md
cc-P158-codex-second-agent-codex-review.md
cc-P158-codex-second-agent.md
cc-P159-codex-lane-second-pc-codex-review.md
cc-P159-codex-lane-second-pc.md
cc-P160-plan-usage-pacing.md
cc-P161-close-finished-sessions.md
cc-P162-end-of-week-spend.md
cc-P163-dashboard-fixes-portainer.md
cc-P164-playtest-sessions.md
cc-P165-achievements-button-fix.md
cc-P166-kitsune-fit-west-bald.md
cc-P167-rootdeep-map-batch.md
cc-P169-requirement-colors.md
cc-P170-smith-teaching-orders-fix.md
cc-P171-taming-anger-scales.md
cc-P172-pet-gain-speed.md
cc-P173-imbue-all-slayers.md
cc-P174-session-closer-fix.md
cc-P175-cont-clean-up-britannia-finish.md
cc-P176-cont-artificers-unravel-container.md
cc-P177-guild-menus-template-mockups.md
cc-P179-league-design-pass.md
cc-P180-cont-rootdeep-renders-round2.md
cc-P181-cont-rootdeep-round3.md
cc-P182-cont-web-console-phase2.md
cc-P183-cont-golem-run-cap-and-stale-usage.md
cc-P184-cont-multi-golem.md
cc-P185-cont-rootdeep-round4.md
cc-P186-cont-golem-join-kit.md
cc-P187-cont-web-console-parity.md
cc-P188-cont-rootdeep-goes-in.md
cc-P189-cont-old-haven-new-player-safe.md
cc-P190-cont-test-crystal.md
cc-P191-cont-earned-skill-gain.md
cc-P192-cont-fountain-of-youth.md
cc-P193-port-high-seas-fishing.md
cc-P194-port-wrong-and-covetous-void.md
cc-P195-port-exodus-encounter.md
cc-P196-port-blackthorn-dungeon-codex-review.md
cc-P196-port-blackthorn-dungeon.md
cc-P197-port-underworld-mini-champions.md
cc-P198-port-eodon-remainder.md
cc-P199-port-base-items-remainder.md
cc-P200-cont-marathon-mode.md
cc-P201-deployable-traps-design.md
cc-P202-cont-fixup-cont-earned-skill-gain.md
cc-P203-cont-fixup-requisitions-and-leads.md
cc-P204-cont-fixup-cont-fixup-cont-earned-skill-gain.md
cc-P207-golem-card-glow.md
cc-P208-cont-shadow-iron-merger.md
cc-P209-cont-fixup-port-high-seas-fishing.md
cc-P211-svdungeon-070-assessment.md
cc-P212-code-intake-batch-1.md
cc-P213-cont-changelog-version-merges.md
cc-P214-tool-trials.md
cc-P215-golem-test-accounts-codex-review.md
cc-P215-golem-test-accounts.md
cc-P216-golem-questions-in-console.md
cc-P217-crystal-wiki-catch-up.md
cc-P218-crystal-mage-crafter-scripts.md
cc-P219-tazuo-script-test-harness.md
cc-P220-crystal-status-page-judgments.md
cc-P221-cont-fixup-port-wrong-and-covetous-void.md
cc-P222-tinker-golem-watchdog.md
cc-P224-playtest-bot-checks-second.md
cc-P225-cont-fixup-cont-test-crystal.md
cc-P226-arms-lore-matters.md
cc-P227-extended-wood-bonuses.md
cc-P228-exceptional-material-gap.md
cc-P229-league-reward-shop.md
cc-P230-staff-hub-events-tab.md
cc-P231-osi-joke-achievements.md
cc-P232-pkcs-pin-drop-audit-flag.md
cc-P233-props-ability-profile.md
cc-P234-dismount-sources-design.md
cc-P235-work-order-numbers-pass.md
cc-P236-satchel-icons-ship-codex-review.md
cc-P236-satchel-icons-ship.md
cc-P237-new-haven-community-art-codex-review.md
cc-P237-new-haven-community-art.md
cc-P238-climbing-boots.md
cc-P239-creature-levels-appraisal.md
cc-P240-fog-of-war-client-half.md
cc-P241-achievement-category-icons.md
cc-P243-league-hall-decor-rewards.md
cc-P244-cont-fixup-tinker-golem-watchdog.md
cc-P245-cont-fixup-port-base-items-remainder.md
cc-P260-herbalism-research.md
cc-P261-levelable-gear-build.md
cc-P262-accessory-slots.md
cc-P263-noted-by-the-system-achievements.md
cc-P265-guild-hall-decor-packs.md
cc-P266-new-haven-winter-decor-codex-review.md
cc-P266-new-haven-winter-decor.md
cc-P267-halloween-bank-decor.md
cc-P268-high-seas-ships-assessment.md
cc-P271-cont-fixup-port-exodus-encounter.md
cc-P272-cont-fixup-codex-second-agent-codex-review.md
cc-P272-cont-fixup-codex-second-agent.md
cc-P275-deployable-traps-build.md
cc-P276-tutorial-farm-build.md
cc-P278-cont-fixup-climbing-boots.md
cc-P280-league-register-build.md
cc-P282-f12-numbers-and-level-gates-codex-review.md
cc-P282-f12-numbers-and-level-gates.md
cc-P283-skill-gain-paths-research-codex-review.md
cc-P283-skill-gain-paths-research.md
cc-P284-cont-fixup-satchel-icons-ship.md
cc-P285-cont-fixup-levelable-gear-build.md
cc-P286-crystal-mage-crafter-docs-and-tests.md
cc-P286-test-plans.md
cc-P352-cont-fog-of-war-client-half.md
cc-P353-cont-golem-questions-install-and-round.md
cc-P354-cont-fixup-port-eodon-remainder.md
cc-P355-cont-fixup-accessory-slots.md
cc-P356-cont-fixup-golem-questions-in-console.md
cc-P357-cont-fog-of-war-client-half.md
cc-P358-cont-fixup-playtest-bot-checks-second.md
cc-P361-cont-fixup-noted-by-the-system-achievements.md
cc-P364-league-bestiary-batch-2.md
cc-P366-cont-fixup-cont-loot-box-flying-loot.md
cc-P367-music-room-console-page.md
cc-P368-added-music-areas-monsters-bosses-codex-review.md
cc-P368-added-music-areas-monsters-bosses.md
cc-P369-cont-fixup-companions-b1-base-and-record.md
cc-P371-graduation-is-the-first-loop-codex-review.md
cc-P371-graduation-is-the-first-loop.md
cc-P374-league-player-guide-draft.md
cc-P376-league-decisions.md
cc-P377-crystal-wiki-catch-up-2.md
cc-P378-playtest-plans-10-21-codex-review.md
cc-P378-playtest-plans-10-21.md
cc-P379-crystal-review-10-21-merges.md
cc-P381-guild-guide-society-of-smiths-codex-review.md
cc-P381-guild-guide-society-of-smiths.md
cc-P382-guild-guide-order-of-the-alembic-codex-review.md
cc-P382-guild-guide-order-of-the-alembic.md
cc-P383-guild-guide-artificers-order-codex-review.md
cc-P383-guild-guide-artificers-order.md
cc-P384-guild-guide-thieves-den-codex-review.md
cc-P384-guild-guide-thieves-den.md
cc-P385-guide-gathering-guilds-codex-review.md
cc-P385-guide-gathering-guilds.md
cc-P386-guide-rangers-custodians-healers-codex-review.md
cc-P386-guide-rangers-custodians-healers.md
cc-P387-guide-achievements-and-loot-boxes-codex-review.md
cc-P387-guide-achievements-and-loot-boxes.md
cc-P388-guide-levels-loops-and-scrolls-codex-review.md
cc-P388-guide-levels-loops-and-scrolls.md
cc-P389-guide-companions-and-evo-pets-codex-review.md
cc-P389-guide-companions-and-evo-pets.md
cc-P390-guide-crafting-changes-codex-review.md
cc-P390-guide-crafting-changes.md
```

</details>

## Validation

- Windows PowerShell 5.1.26100.9444; Python 3.12.10. `rg` is unavailable, so file discovery/search used PowerShell and Python. No PowerShell 7 script or test was used.
- Local editorial checks: every Markdown file link resolves, decision identifiers are unique, the manifest exactly matches the input-note set, there is a final newline and there are no trailing spaces. Referenced canonical code files were checked for existence and the substantive source/default claims above were inspected. No new tests were added or run.
- Both work copies pass `git diff --check`. ShatteredLegacy is unchanged; shard-migration contains only this new tracked candidate. It is well below 5 MB. Scratch review helper and progress output are under `notes/__pycache__/`; both paths were proven ignored with `git check-ignore`.
- Ran the required original progress reporter in memory with `--dry-run` and work-copy path overrides. The reporter's dry-run still attempts to write `tools/progress.json`; intercepted only that write with `Path.write_text` so the docs-only task changes no generated output. It completed successfully. Its broad source counts were reviewed but are not repeated here as behavior/completion measurements. Ignored local record: `notes/__pycache__/p392-progress.txt`.
- No `docs/` edit, code change, commit, branch switch, merge, push, deployment, Haven connection, generated art or account-affecting action. The stopping-point request was absent at the review checkpoints and is checked again before the final status line.

P392 DONE
