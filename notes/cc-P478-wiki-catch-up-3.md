# cc-P478: wiki catch-up, round 3 (the Codex guide drafts, and what merged since P377)

2026-10-23. Prompt: `shattered-legacy-prompts/queue/cc-P478-wiki-catch-up-3.md`. Golem: Crystal (Claude Code cloud
session, GitHub only, no game PC). Set up as P217 says: branch `golem/Crystal/P478` from `origin/main` in the code repo
(at `0f1871f`, VERSION `2026.10.23.2`) and in this repo (at `6160786`).

## In plain words

The wiki seed in the code repo now has the Codex guide drafts as DokuWiki pages: a page for nine guilds, a new players'
corner (hub, FAQ, glossary), guides to crafting and High Seas fishing, a dungeons page, and Treasures of Sorcerer's
Dungeon. The League, achievement, loot box, trap, bulk order, materials, recipes, mining, imbuing, blacksmithy, stealing,
Clean Up, pet training, Young and New Haven pages are corrected against the 10-22 cross-check and Chase's 10-22 and
10-23 calls. Tutorial, levels and loops, companions, guild halls, Rootdeep, levelable gear and the red dragon are drafts.

P377's pages, which waited in `notes/wiki-drafts/pages/`, are copied into the seed first (commit `c963d19`; the seed had
not changed since P377, so the copy was one for one). That folder in this repo is now a stale copy and can be deleted.

Nothing is published. Deploying is Chase's step (`sync-dokuwiki-content.sh`). Many existing pages changed, so the
deploy needs `SYNC_MODE=overwrite` (or a hand copy of the changed files); `seed` mode keeps the old versions.

## Rules applied

- **Live or draft:** P217's rule (headline 3), as P377 kept it. Live retired, so "live" = in `main`, finished for
  players, placed by the code's own seeders: it ships with the 1.0 world as it stands. Live pages go in their namespace
  with a sidebar link; anything test-only, staff-placed or planned goes in `uo:drafts:` with a bold reason line at the
  top and no sidebar link. Planned features on live pages are either left out or one line marked **(planned)**.
- **Cross-check 2026-10-22:** every row that names a page was applied (C01-C54 and the unverified-claims table). Where
  it leaves something unresolved (C01 boss boxes, C08 gear strength, C20 job XP, C40 reserve), the page does not state
  the contested claim.
- **Chase 2026-10-23 (F-24, nine League answers):** chapters 4 and 5 at Blaze and Mythril; six chapters; bonuses only at
  the six milestones; Renown shop delivered; no AP total and no title count anywhere (visible titles listed by name);
  Leads as built; non-member requisition standing pays at once; no Warehouse, no Featherweight satchels; the Clockwork
  Scavenger stays (planned).
- **Chase 2026-10-22:** Blaze free repair on worn gear only; recycling counts own crafts or loot only; guild hall towers
  walkable once built; stone mining gated until learned (P416, queued: planned on the pages); mining quotas by metal
  (P416/P417: planned).
- Hidden achievements: categories only. League story: chapter 1 only.
- Checks run over the whole seed: no em dashes, no British spellings, no staff commands or `clusterf.*` names, every
  internal link resolves to a seed page (one false hit in an older macro page's code block).

## The table

Pages are under `docker/wiki/content/pages/` in the code repo. "Live" uses the rule above.

| Draft or system | Page | New or merged | Live or draft | Open questions |
|---|---|---|---|---|
| P377's 21 files (`notes/wiki-drafts/pages/`) | league_shop, league_register, accessories, creature_levels, traps, climbing_boots, seasonal, guides:league, levelable_gear and hubs | copied in, then merged below | as P377 | none |
| achievements-and-loot-boxes.md | `uo:systems:achievements` | merged | live | none |
| achievements-and-loot-boxes.md | `uo:systems:loot_boxes` | merged | live | C01: first boss boxes look broken by source; page says not to count on one. Needs a kill on the test shard |
| league.md | `uo:guides:league` | merged | live | none |
| league.md | `uo:systems:league` | merged | live | Second bracelet opens at Valorite (rank 9), not a milestone: keep, or move under "bonuses only at milestones"? |
| league.md, Chase 10-22 | `uo:systems:league_register` | merged | live | Blaze repair: page says worn gear only; code (`LeagueRegister.cs:317-328`) also repairs carried and banked gear. Needs a fix-up prompt |
| league.md | `uo:systems:league_shop` | merged | live | none |
| cross-check C01, C17, C18 | `uo:professions:traps` | merged | live | none |
| (checked) | `uo:systems:accessories`, `uo:systems:creature_levels` | unchanged / spelling only | live | none |
| guilds.md | `uo:systems:guilds` | merged | live | C22: fix the standing-only rank displays so the caveat can go? |
| guilds.md | `uo:guilds:start` | new | live (hub) | none |
| artificers-order.md | `uo:guilds:artificers_order` | new | live | C21, C35: rewrite the Artificers' old "joining requirement" and standing-cap help text in game? C37: socket II gives nothing for imbuing |
| artificers-order.md | `uo:professions:imbuing` | merged (corrected) | live | book ranks were wrong; rare properties no longer described as obtainable |
| society-of-smiths.md | `uo:guilds:society_of_smiths` | new | live | Large commissions sharing the small cooldown (Chase 10-22) waits on P454 |
| society-of-smiths.md | `uo:professions:blacksmithy` | merged | live | none |
| order-of-the-alembic.md | `uo:guilds:order_of_the_alembic` | new | live | none |
| thieves-den.md | `uo:guilds:thieves_den` | new | live | none |
| thieves-den.md | `uo:professions:stealing` | merged | live | Burrows rows taken off until it opens |
| rangers-custodians-healers.md, gathering-guilds.md | `uo:guilds:rangers_league` | new | live | none |
| rangers-custodians-healers.md | `uo:guilds:custodians`, `uo:systems:clean_up_britannia` | new, merged | live | Civic waste bundles described as built; P414 (retire them) is queued |
| rangers-custodians-healers.md | `uo:guilds:healers_covenant` | new | live | `[SelfRes` is a player command on by default: tell players or not? |
| gathering-guilds.md | `uo:guilds:foresters_union` | new | live | none (lumber stumps, P380, added here) |
| gathering-guilds.md | `uo:guilds:miners_compact` | new | live | Stone gate and quotas shown as planned until P416 merges |
| gathering-guilds.md, CHANGELOG | `uo:professions:mining` | merged (stub rewritten) | live | Blackrock, stone mining as OSI plus the planned gate |
| crafting-changes.md | `uo:guides:crafting` | new | live | none |
| crafting-changes.md | `uo:professions:bulk_orders`, `materials`, `recipes` | merged | live | none |
| high-seas-fishing.md | `uo:guides:high_seas_fishing` | new | live (ported) | Do lobster traps have any player source? |
| dungeons.md | `uo:world:dungeons` | new | live | Despise and Shame generated on the test world? (P217 assumed yes) |
| P408 | `uo:world:sorcerers_dungeon` | new | live (starts by itself on the dates; code places it) | Artifact drop chance not stated (formula in `Data.cs:44-45`) |
| P266 winter, C44 | `uo:world:seasonal` | merged | live | none |
| new-haven-start.md, P289 + P475, P371, P276 | `uo:drafts:tutorial` | merged | draft (entry off outside the test shard) | see "Possible live problem" below |
| new-haven-start.md, P189 | `uo:world:new_haven` | merged | live | Rook moved to "coming later" (only a test-world command places him) |
| new-player-faq.md | `uo:newplayer:faq` | new | live | none |
| (hub) | `uo:newplayer:start` | new | live | none |
| glossary.md | `uo:newplayer:glossary` | new | live | Velara Thorne's spot comes from hint text, unchecked in game |
| levels-loops-and-scrolls.md | `uo:drafts:levels_and_loops` | new | draft (mostly planned) | C40 reserve size still undecided |
| companions-and-evo-pets.md | `uo:drafts:companions` | new | draft | none |
| companions-and-evo-pets.md, P172 | `uo:systems:pet_training` | merged | live | none |
| P371 | `uo:systems:young_players` | merged | live | old line "a real loop ends Young" was wrong; now "never" |
| (checked) | `uo:new_player_guide` | merged (C01, C11 fix) | live | none |
| P281 | `uo:drafts:guild_halls` | new | draft (test shard only; refuses on live) | Towers walkable now on the test shard? |
| P277 | `uo:drafts:red_dragon` | new | draft (staff only) | none |
| cross-check Burrows row | `uo:drafts:rootdeep_burrows` | merged | draft | none |
| cross-check unverified row | `uo:drafts:levelable_gear` | merged | draft | none |
| P364 League hunt bestiary | none | none | test (staff seeder places the spawners) | page once placed |
| P354 Eodon | `uo:world:dungeons` (not open yet) | line only | test (`[GenEodon` staff, test first) | none |
| P368 shard music | none | none | live code, but no tracks ship yet | page when the first tracks ship |
| P274, P287, P288, P410 | none | none | not player-facing | none |
| Hubs | `sidebar`, `uo:start`, `uo:systems:start`, `uo:professions:start`, `uo:world:start`, `uo:guides:start`, `uo:drafts:start` | merged | live hubs (drafts hub has no sidebar link) | none |

Counts, from `git diff --name-status origin/main` on the code branch: 55 page files, 30 new and 25 changed. The 30 new
are P377's 9 (from the copy commit) and this round's 21: 9 guild pages and their hub, 3 new player pages, 2 guides,
2 world pages and 4 drafts. Plus CHANGELOG 2026.10.23.3 and VERSION.

## Code citations

Each worker cited file:line for every number. Summary, paths under `server/customizations/` unless marked:

- **Loot boxes:** ladders `LootBoxes/ClusterFLootTable.cs:82-99` (Hunter's Barbed twice, C06); Artisan ladders
  `LootBoxRoller.cs:40-55` (C04); base gold and Renown `:156-157`; League theme `50 * tier` Renown `:284-287` (C07);
  promotion box tiers `ClusterFLootTable.cs:130`; promotion hook `ClusterFLeagueRanks.cs:425`, `ClusterFLootBoxes.cs:208`
  (C11); boss box Major fanfare `ClusterFLootBoxes.cs:200` (C02); Loop box Capstone tier 6 `:218-221`; abandoned-box
  cleanup `:243-250` (C03).
- **League:** six chapters `ClusterFLeagueRanks.cs:123`; milestone-only bonuses `:25-27`, `:417`; ladder `:485-503`;
  second bracelet `Accessories/ClusterFAccessories.cs:49-51`; Blaze repair code `LeagueRegister/LeagueRegister.cs:317-328`.
- **Guilds:** definitions and Apprentice tasks `ClusterFGuildSystem.cs:100-300`; task then join `:382-427` (C21);
  thresholds and ladders `:618-656`, `:717-756` (five-rank ladder skips index 4, C23); Custodians
  `ClusterFCustodianSystem.cs:47-54` (C41); promotion skill 30/50/70/90/100 `Engines/Craft/ClusterFRecipeTable.cs:75`,
  base skill and trial waiver `ClusterFGuildPromotion.cs:34`, `:55-97` (C22); Miners' rank names
  `MinersCompactLiaisonGump.cs:712-721`.
- **Artificers and imbuing:** book gate `Imbuing/ImbueFormulaBooks.cs:79-105`; property ladder `Imbuing/ImbuingTable.cs:144-180`;
  sites and slots `:109-133` (C37); Casting Focus grant-only `Imbuing/ClusterFImbueKnowledge.cs:46-49`; Self Repair price
  `ArtificersImbueGump.cs:158-173`.
- **Smiths:** caps `ClusterFSmithBODSystem.cs:56-62` (C25); checks `:470-481`, `:621-633` (C26); cash-out
  `ClusterFSmithBODPayout.cs:180`, `:215` (C27); teaching fallback `ClusterFSmithTeaching.cs:197-203` (C16); large Smith
  direct fill `patches/LargeSmithBOD.cs:155-165` (C15); hammers `HammerOfHephaestus.cs:145-147`, `:525-527`, `:1100-1105`.
- **Materials:** exceptional x1.5 `ClusterFExceptionalMaterial.cs:1-28`, `:41-43` (C34); wood bonuses
  `ClusterFWoodBonuses.cs:75-149`; Arms Lore `ClusterFArmsLore.cs:8-9`; extended woods harvest at 100
  `ClusterFLumberjackingExtension.cs:224-238` (C33); extended metals `ClusterFMiningExtension.cs:173`.
- **Gathering and service guilds:** satchels `ForestersLumberSatchel.cs:49`, `HuntersSatchel.cs:79`,
  `CompactOreSatchel.cs:55-92`, `:176` (C52); Alembic `ClusterFAlembicGuild.cs:13-149`; Den rules
  `Services/Monster Stealing/Core/StealingHandler.cs:53`, `:68`, `ThievesDenStealRules.cs:53-55`, `:151-173`; Shadow Cloak
  schematics `Mobiles/Mule/MuleModuleGumps.cs:475-480` (C50); Den recipes 9400+ (C51); trash bag to members only
  `SanitationWarden.cs:72-73`; corpse credit `Services/CleanUpBritannia/ClusterFCorpseValue.cs:8`, `:38`; healer policy
  `ClusterFHealerPolicy.cs:10-17`.
- **Traps:** double-click the kit `Items/Traps/Deployable/DeployableTrapKit.cs:261` (C17); alarm exempt
  `DeployableTraps.cs:302` (C18).
- **High Seas:** thresholds `Services/Expansions/High Seas/Items/Fish/FishInfo.cs:236`, `:353-361`.
- **Sorcerer's Dungeon:** automatic on the dates and placed by the code `.../TreasuresOfSorceresDungeon/Generate.cs:1-20`,
  `:59-67`; rooms and bosses `Spawner.cs:1-6`, `:374-382`; rewards `SorcerersDungeonRewards.cs:5-40`; one point per
  artifact `SorcerersDungeonResearcher.cs:1-5`.
- **Tutorial and loops:** core trials `Tutorial/TutorialCoreTrials.cs:45-247`, titles `TutorialStations.cs:58-110`;
  test-only `ClusterFTutorial.cs:33-47`; staff exempt `:91-93`; placement `TutorialCorePlacement.cs:70-106`; island gate
  `TutorialIslandGate.cs:13-85`; graduation `ClusterFTutorial.cs:224-264`; later characters at loop 1 `:78-85` (C13);
  skip and remedial `:169-216`; loops `Tutorial/ClusterFLoops.cs:31`, `:40-64` (C38, C40, C47).
- **Pets and Young:** evo XP `Mobiles/Evo/EvoPetData.cs:215`; loops read 0 `EvoPet.cs:28`, `:92` (C39); pet gain
  `ClusterFPetGainSpeed.cs:22-98`; Young 336 hours `ClusterFYoungPlayer.cs:35`.
- **Guild halls:** `ClusterFGuildHallPlacement.cs:1-25` (refuses on live), `ClusterFGuildHallPlacementData.cs:43-155`.
- **Not re-traced, taken from the drafts:** Smith catalog and book prices, salvage Seals, disenchant and extract odds,
  the commission wait, hammer refill, the crook's bonuses, Tracking range, healing thresholds, fishing tables, the chest
  table, Despise and Shame details, Make X caps and salvage returns. The pages carry code defaults; tuned settings live on
  the game PC.

## Possible live problem (not a wiki question)

`TutorialIslandGate` is on by default and checks only "loop 0 and on the island", not whether the tutorial is enabled.
On a world with the tutorial off, a new character is loop 0 and can never graduate, so may not be able to leave Haven
island. Needs a check on the game PC, or Chase's call on whether the gate should follow the tutorial's switch.

## Needs the game PC

- Whether the tutorial farm, Rook and the core trial props are placed on the test world.
- Whether Treasures of Sorcerer's Dungeon comes up by itself on the test world on 10-24.
- Whether the guild halls' towers are walkable on the test shard; whether the Artificers' Royal City post stands.
- Whether Despise and Shame are generated on the test world.
- A first boss kill, to confirm or clear C01.
- The tuned settings behind every price and threshold (the pages carry code defaults).
- The `TODO image:` shots listed on each page.

## For Chase

1. Deploy the seed with `SYNC_MODE=overwrite` (many existing pages changed).
2. Answer the open questions in the table: the Valorite bracelet, Blaze repair's code, `[SelfRes` on the wiki, the C22
   rank displays, the Artificers' help text and socket II.
3. Fix-ups worth a prompt: Blaze repair to worn gear only; the island gate's switch; the C14 vision text in
   `ClusterFLoops.cs:79-80` ("your skills go with it").
4. `notes/wiki-drafts/pages/` in this repo is now a stale copy of what is in the seed; delete it when convenient.

## Working as a cloud Golem (round 3)

- The code repo being writable this time removed P377's copy step.
- The drafts were large (about 350 KB), so the work was split across six parallel workers with fixed file ownership,
  then one pass over hubs, links, spelling and dashes. A cross-check written per page (as this one was) made that split
  easy.
- A "what is placed where" list would still settle most of the "Needs the game PC" items.

P478 DONE
