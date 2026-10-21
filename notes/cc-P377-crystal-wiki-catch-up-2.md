# cc-P377: wiki catch-up, round 2 (what merged on 10-20 and 10-21)

2026-10-21. Prompt: `shattered-legacy-prompts/queue/cc-P377-crystal-wiki-catch-up-2.md`, method from
`completed/cc-P217-crystal-wiki-catch-up.md` sections 1 to 5. Golem: Crystal (Claude Code cloud session, GitHub only).
Docs repo branch `golem/Crystal/P377` from `origin/main` (`341e651`). Code repo read only, at `origin/main` `47b3eae`
(VERSION `2026.10.21.20`).

## In plain words

The player wiki now has pages for what merged on 10-20 and 10-21: the League Shop and its Hall decor, the League
Register and its repair items, deployable traps, climbing boots, accessory slots and toe rings, creature levels and
Appraisal, the Halloween decor, and a player's guide to the League made from P374's draft. The achievements, loot box,
League and bulk order pages are brought up to date, the tutorial draft gains the farm, and levelable gear gets a draft.
Nothing is published, and the pages are not in the code repo yet: they wait in this repo for someone to copy them over.

## Where the pages are, and why not in the code repo

P217 wrote straight into the code repo's seed (`docker/wiki/content/pages/`). This run was told the code repo is read
only, so the pages are in this repo at **`notes/wiki-drafts/pages/`**, laid out exactly as the seed folder: the files
copy over one for one.

    cp -r notes/wiki-drafts/pages/* <ShatteredLegacy>/docker/wiki/content/pages/

The updated pages (the five content pages and seven hubs below) started as byte copies of the seed at `47b3eae`, the
last change to the seed being `b35e4cd`; if the seed changes before the copy, merge rather than overwrite.

## 1. Inventory

Everything player-facing merged into the code repo's `main` after P217 (merge `f2e38f8`, CHANGELOG 2026.10.20.6), read
from the CHANGELOG 2026.10.20.7 to 2026.10.21.20, the first-parent merge log, and the C# each merge touched. Status uses
P217's rule (headline 3 of its notes): **live** = in `main`, finished for players, and reachable without a staff
placing it; **test** = the code or CHANGELOG says test shard only, or nothing puts it in players' hands; **unclear** =
in `main` but depends on something not checkable from GitHub.

| # | System | Prompt(s) | Where in the code | Status | Page now | New or updated |
|---|---|---|---|---|---|---|
| 1 | League Shop, League titles | P229 | `LeagueShop/LeagueShop.cs`, `LeagueShopGumps.cs`, `LeagueShopItems.cs` | live (through the Registrar, already seeded) | `uo:systems:league_shop` | new |
| 2 | League Hall decor | P243 | `LeagueShop/LeagueHall.cs` | live; art needs the player package | `uo:systems:league_shop` (Hall section) | new |
| 3 | League Register, League actions, League goods, repair items | P280 | `LeagueRegister/*.cs` | live | `uo:systems:league_register` | new |
| 4 | P374's League guide | P374 | `notes/wiki-drafts/league.md` (this repo) | live (the League is live under P217's rule) | `uo:guides:league` | new |
| 5 | The League page itself | P229, P280, P262 | as above | live | `uo:systems:league` | updated (Renown is now a balance plus Lifetime Renown; the old "it only rises" was wrong after P229) |
| 6 | Deployable traps | P275 | `Items/Traps/Deployable/*.cs`, `Engines/Craft/TinkeringCraftRegistrations.cs` | live (crafted, no placement); 4 traps on stand-in art | `uo:professions:traps` | new |
| 7 | Tutorial farm and the evo pet pick | P276 | `Tutorial/TutorialFarm.cs`, `TutorialFarmLayout.cs`, `ClusterFTutorial.cs` | **test**: the seeder refuses off the test shard unless `clusterf.tutorialFarm.allowLive` (`TutorialFarm.cs:24-26`); the tutorial itself is a draft (P217 row 21) | `uo:drafts:tutorial` | updated (draft) |
| 8 | Halloween bank decor | P267 | `ClusterFHalloweenDecorLayout.cs`, `ClusterFHalloweenDecorSeeder.cs`, `ClusterFSeasonalSwitch.cs` | live: goes up by itself 10-24 to 11-02 (`automatic` defaults true) | `uo:world:seasonal` | new |
| 9 | Guild hall decor packs | P265 | `GuildHallDecor/*.cs` | **test**: nothing placed; the four commands refuse on live (CHANGELOG 2026.10.21.19) | none: nothing a player can see | none |
| 10 | Levelable crafted gear | P261, P285 | `LevelGear/*.cs`, `AOS-level-gear-attribute-aggregation.patch` | **test**: the Smith's Seal has no player source (`SmithsSealDeed.cs:1-4`); CHANGELOG lists it under Staff only | `uo:drafts:levelable_gear` | new (draft) |
| 11 | "Noted by the System" secret achievements, Dented Box | P263, P361 | `ClusterFNotedBySystem.cs`, `LootBoxes/NotedJokeItems.cs`, 8 event patches | live | `uo:systems:achievements` (category only) | updated |
| 12 | Joke secret achievements | P231 | `ClusterFJokeAchievements.cs`, 9 event patches | live | `uo:systems:achievements` (category only) | updated |
| 13 | Achievement category icons | P241 | client package gumps 22459-22468 | live (needs the player package) | `uo:systems:achievements` | updated |
| 14 | Flying loot | P242, P360, P366 | `LootBoxes/ClusterFFlyingLoot.cs`, `LootBoxItems.cs` | live (on by default; needs the player package) | `uo:systems:loot_boxes` | updated |
| 15 | Climbing boots, mined block count | P238, P278 | `ClusterFClimbing.cs`, `ClimbingBoots.cs`, `ClusterFMinedBlocks.cs`, `MinersCompactLiaisonGump.cs`, 2 patches | live (sold by the already-seeded Liaison) | `uo:professions:climbing_boots` | new |
| 16 | Hammer of Hephaestus T3 | P168 | not in `main`: `origin/golem/Copper/P168` exists, the prompt sits in the prompts repo's `merging/`; `HammerOfHephaestus.cs` still has T3 as a stub (`:23-31`, `:1070-1074`) | not merged | none | none |
| 17 | Accessory slots, toe rings | P262, P355 | `Accessories/*.cs` | live (`[accessories` is a player command, `ClusterFAccessories.cs:97`) | `uo:systems:accessories` | new |
| 18 | Creature levels, con colors, Appraisal | P239 | `ClusterFCreatureLevels.cs`, `BaseCreature-con-color-line.patch` | live (Appraisal's new name needs the player package) | `uo:systems:creature_levels` | new |
| 19 | Bulk orders take crafted items only; commission abandon wait | P263 | `ClusterFStoreBought.cs`, `SmallBOD-crafted-only.patch`, `ClusterFSmithCommissions.cs` | live | `uo:professions:bulk_orders` | updated |
| 20 | New BOD rewards (automaton parts, runic mallets and chisels), Kotl automatons, chicken coop, base items | P199, P245 | per CHANGELOG 2026.10.20.16 | live | `uo:professions:bulk_orders` (rewards line) | updated |
| 21 | Exceptional items get material bonuses x1.5 | P228 | CHANGELOG 2026.10.21 | live | none | gap (`uo:professions:materials`) |
| 22 | Extended woods' weapon and shield bonuses | P227 | CHANGELOG 2026.10.20.22 | live | none | gap (`uo:professions:materials`) |
| 23 | Arms Lore to 200, field maintenance | P226 | `ClusterFArmsLore`, CHANGELOG 2026.10.20.19 | live | none | gap |
| 24 | Pet learning speed for seasoned owners | P172 | CHANGELOG 2026.10.20.5 (merged after P217) | live | none | gap (`uo:systems:pet_training`) |
| 25 | Old Haven apprentice training ground; mages and Vorlak gone | P189 | CHANGELOG 2026.10.20.8 | live | none | gap (`uo:world:new_haven`) |
| 26 | High Seas fishing, first half (ported) | P193, P209 | CHANGELOG 2026.10.20.9 | live, ported (UOGuide covers it) | none | gap (one short page) |
| 27 | Blackrock from mining | P195/P271 | CHANGELOG 2026.10.21.11 | live | none | gap (`uo:professions:mining`) |
| 28 | Upgrade menus' met/not-met colours | P169 | CHANGELOG 2026.10.20.20 | live | none needed | none |
| 29 | Satchel and bag icons | P236, P284 | CHANGELOG 2026.10.21.7 | live (needs the package) | none needed | none |
| 30 | Monster surges | P230 | Staff Hub Events tab | live, but only when staff run one | none | gap (short events page) |
| 31 | Fog of war on the world map | P352, P357 | TazUO client patch 0004 | **unclear**: seen only once a player package built with that client is published (CHANGELOG 2026.10.21.11 Staff) | none | gap |
| 32 | Rootdeep's way in from Old Haven | P188 | `ClusterFRootdeepSeeder.cs`, map overlay | **unclear**: placed by a staff seeder; live gets the map overlay "at a restart you plan" (CHANGELOG 2026.10.20.16 Staff) | `uo:drafts:rootdeep_burrows` unchanged | none |
| 33 | Trap training kits, the Collector of Oddities | P199 | `[ClusterFPlaceCollectorOfOddities` | **unclear**: the vendor is placed by a staff command, "test shard first" | one line on `uo:professions:traps`, hedged | partial |
| 34 | New Haven community art, the orc camp | P237 | `[ClusterFCommunityArt` | **test**: "Nothing runs by itself: run 'place' on the test shard first" | none | gap until placed |
| 35 | The Exodus Encounter | P195, P271 | `[GenExodusEncounter` | **test** until Chase runs it live | none | gap |
| 36 | Blackthorn Dungeon (revamped) | P196 | `[GenBlackthorn` | **test** ("Nothing is placed at boot") | none | gap |
| 37 | Wrong (revamped), Covetous Void Spawn | P194, P221 | `[GenWrongRevamp`, `[SetupNewCovetous` | **test** until run live | none | gap |
| 38 | Underworld (Stygian Abyss), mini champions | P197 | `Services/Underworld/*`, `Services/MiniChampionSystem/*` (30 files) | **unclear**: merged (`e8f4b92`) with no CHANGELOG entry at all | none | none: ask how it is placed |
| 39 | Companions, first part | P264, P369 | staff commands only | **test** | none | none |
| 40 | Fountain of Youth | P192 | CHANGELOG 2026.10.20.11 Staff: "never put it on the wiki or in player notes" | secret by instruction | none, deliberately | none |

Counts: 40 rows, counted from the table. 26 live (rows 1-6, 8, 11-15, 17-30), 8 test shard only (7, 9, 10, 34-37,
39), 4 unclear (31-33, 38), 1 not merged (16), 1 kept off the wiki on instruction (40). Pages: 8 new live pages, 1 new draft, 5 content pages
updated (`league`, `achievements`, `loot_boxes`, `bulk_orders`, the tutorial draft), 7 hubs (`sidebar`, `uo:start`,
and the `start` pages of systems, professions, world, guides and drafts): **21 files**, counted with `find
notes/wiki-drafts/pages -type f`.

Expected topics from the prompt, each checked: League shop (row 1), Register and repair deeds (3), League hall decor
(2), traps (6), tutorial farm and evo pet picks (7), Halloween (8), guild hall decor packs (9), levelable gear (10),
Noted by the System (11), flying loot (14), climbing boots (15), Hammer T3 (16: not merged, so no page).

Staff-only things found and left off every page: every `[ClusterF*` seeder, `[DecorAlembicHall` and the other three hall
commands, `[LevelGearSet`, `[add SmithsSealDeed`, `[ClusterFAchievement list`, `[CompanionMake`/`[CompanionSet`,
`[CreatureLevels`, `[Gen*`/`[Delete*`, `[SeedGolemAccounts`, the Staff Hub Events tab, every `clusterf.*` setting name,
the Fountain of Youth. The three secret titles are not named anywhere (CHANGELOG names them under Staff only); the
pages say "three come with a title".

## 2. The pages

All in `notes/wiki-drafts/pages/`, DokuWiki syntax as P217's pages (`======` titles, `^` tables, `[[...]]` links, a
"Needed images" list of `TODO image:` lines).

Live, with a sidebar link:

| Page | What it says |
|---|---|
| `uo/systems/league_shop.txt` | AP opens, Renown pays, Lifetime Renown untouched; the 14-row starter table; the System's boxes; bought and free titles; the Hall page's 19 pieces by AP band with price ranges, deeds, placement, chop, dye |
| `uo/systems/league_register.txt` | issue at Dull Copper and re-issue; binding and guild books; capacity table; the pages and League actions by rank; League goods table (logbook, field satchel, four backpack steps); the three repair items with skills and materials |
| `uo/systems/accessories.txt` | `[accessories`; slots table (rings with loops, not open; bracelet at Valorite; toe rings from secret achievements, unnamed); toe rings: Tinkering 40, 2 ingots, recipe-gated, bare feet or Plate Socks |
| `uo/systems/creature_levels.txt` | the seven con colours and words with their level gaps; level from Bard difficulty, 200/190/1; your level is your best combat skill; Appraisal at any/30/60/90 |
| `uo/professions/traps.txt` | the eight kits with Tinkering, Remove Trap, effect and charges; setting, loading, re-setting; how many out; the rules (monsters only, 12 tiles, credit, flyers, incorporeal, bosses, decay); the Den; practice |
| `uo/professions/climbing_boots.txt` | the three boots with every requirement; half stamina; ledge memory; blessed and bound; hopping and its refusals; what you can do on a mountain tile; pets |
| `uo/world/seasonal.txt` | Halloween 10-24 to 11-02 at 21 banks over 6 facets; winter in New Haven 12-01 to 01-06 |
| `uo/guides/league.txt` | P374's draft as DokuWiki, every "(planned)" kept (bold), its sources section dropped (repo links do not belong on a player page; the draft and P374's notes keep them); links added to the new shop and Register pages |

Updated: `uo/systems/league.txt` (Renown balance and Lifetime Renown, the Register and the bracelet slot under "What a
rank gives", links), `uo/systems/achievements.txt` (icons, the Mischief category described by kind only, Dented Box,
titles, AP opens shop rows; the "76 achievements, 20 secret" sentence dropped, see section 4),
`uo/systems/loot_boxes.txt` (System's boxes, Dented Box, a Flying loot section, FanfareMute hides it),
`uo/professions/bulk_orders.txt` (crafted items only; the rewards now on the shard taken off the "not yet" list).

Draft, no sidebar link: `uo/drafts/levelable_gear.txt` (new; the reason line at the top), `uo/drafts/tutorial.txt`
(the farm, Wren Tallow's three steps, no second pet at graduation).

## 3. Code citations behind the numbers

Paths under `shattered-legacy-infrastructure/server/customizations/` at `47b3eae` unless marked; "CL" is the code repo's
CHANGELOG by version.

- **League Shop.** Stock, AP and Renown: `LeagueShop/LeagueShop.cs:92-121`. Renown spent from the balance only:
  `:7-8`, `ClusterFAccountData.cs:648-666`. Box draws 1/2/3 and AP ceilings 0/250/1000: `LeagueShop.cs:254-259`; pool
  (sash plus opened non-box rows): `:265-283`. Free titles 100-1,750: `:330-339`; three hidden titles `:342-344`. Rune:
  `:228-240`. No registration needed, tabard not dyeable: P374's sources (`notes/cc-P229-league-reward-shop.md`).
- **Hall.** 19 pieces, AP and Renown: `LeagueShop/LeagueHall.cs:96-114`; deed, owner-only placement, wall rule, chop,
  binding, dye: `:5-21`, `:69-90`. Art needs the package: CL 2026.10.21.14.
- **Register.** Issue rank, capacity table, action ranks, goods prices, backpack table, repair thresholds:
  `LeagueRegister/LeagueRegisterSettings.cs:25-68`. Re-issue, binding, live membership: `LeagueRegister.cs:4-15`.
  Repair craft entries (Blacksmithy 60/80/90, Arms Lore 90/110/120, ingots 5/30/20, star sapphire):
  `LeagueRepair.cs:135-146`; repair to full, no max loss: `:10-11`, `:28-41`. Carry weight unchanged: CL 2026.10.21.20.
- **Traps.** Rules: `Items/Traps/Deployable/DeployableTraps.cs:9-20`; settings `:57-64`; per-trap numbers `:81-134`;
  incorporeal list `:194-198`; traps out `:206-207`; arming, concealment `:209`, `:231`; exceptional +1 charge
  `:247-248`; owner present `:253-264`; bosses `:268`, `:317`; Master at half `:8`. Kit gates and materials:
  `Engines/Craft/TinkeringCraftRegistrations.cs:126-161`. Burrows nets and floor traps: CL 2026.10.21.17. Stand-in art:
  `DeployableTraps.cs:154-176`.
- **Climbing boots.** Tiers (range, standing, Mining, blocks, vouchers, gold, ingots), stamina, cooldown, ledge range:
  `ClusterFClimbing.cs:121-144`; rules `:3-21`. Rank names by standing: `MinersCompactLiaisonGump.cs:715-717`. Blessed,
  bound, replaced: `ClimbingBoots.cs:11-12`, `:45-49`. Half stamina, logbook count: CL 2026.10.21.5.
- **Accessories.** Slots and rules: `Accessories/ClusterFAccessories.cs:4-16`; bracelet at rank 9: `:51`; command
  `:97`. Toe ring craft: `Accessories/AccessoryCraftRegistrations.cs:38`; recipe gate and ring art: `ToeRings.cs:1-6`.
  Plate Socks staff-only: CL 2026.10.21.10 Staff.
- **Creature levels.** Level, overrides, bands, the word line: `ClusterFCreatureLevels.cs:5-24`, `:91`, `:213-218`.
  Appraisal thresholds: CL 2026.10.21.9 (not traced to code).
- **Halloween.** Dates `ClusterFHalloweenDecorSeeder.cs:34-35`; automatic default true `ClusterFSeasonalSwitch.cs:127`;
  local time zone `:12-13`; the banks `ClusterFHalloweenDecorLayout.cs:21-43`; not movable
  `ClusterFHalloweenDecorSeeder.cs:291`. Winter dates: CL 2026.10.12.4 era entry (CHANGELOG line 1120).
- **Achievements.** Mischief category: `ClusterFAchievements.cs:283`. Noted by the System, its events and the five not
  yet earnable: `ClusterFNotedBySystem.cs:1-40`, CL 2026.10.21.14. Dented Box: `LootBoxes/NotedJokeItems.cs:1-31`.
  Icons: CL 2026.10.21.13.
- **Flying loot.** `LootBoxes/ClusterFFlyingLoot.cs:1-14`, setting `:49`.
- **Bulk orders.** Crafted only: `ClusterFStoreBought.cs:9`, `:23`; rewards: CL 2026.10.20.16.
- **Tutorial farm.** Layout, Wren Tallow, the three steps, no second pet, test-only seeder: `Tutorial/TutorialFarm.cs:1-26`;
  3 pests `:69`; graduation change `Tutorial/ClusterFTutorial.cs` (diff in `484cf7e`).
- **Levelable gear.** Every number: `LevelGear/ClusterFLevelGear.cs:1-21`, `:41-66`; `[ItemLevel` is a player command
  `:242`, `:726-730`; Seal rules `LevelGear/SmithsSealDeed.cs:1-4`.

## 4. What I could not check from GitHub alone

- **Whether the pages render.** No DokuWiki here; the syntax follows P217's pages by eye.
- **The tuned settings.** Every price and threshold is a `clusterf.*` setting; the pages carry the code defaults and
  say "starting prices". `Configuration/modernuo.json` is on the game PC.
- **Whether the player package with the new art is published** (Hall decor, flying loot, achievement icons, satchel
  icons, the Appraisal name, fog of war). The pages say "update your game through the launcher", as the CHANGELOG does.
- **Whether staff have run the placement commands** (Collector of Oddities, community art, Exodus, Blackthorn, Wrong,
  Covetous, Rootdeep's way in, the tutorial farm) on the test shard, or anywhere.
- **How Underworld and the mini champions reach players** (row 38): no CHANGELOG line, and I did not trace a generator.
- **The achievement totals.** P217's "76, 20 secret, 6 retired" is now out of date. `Reg(` occurrences per file at
  `47b3eae`: `ClusterFAchievements.cs` 80 (one is the method's own definition at `:1235`, so 79 calls),
  `ClusterFJokeAchievements.cs` 16, `ClusterFNotedBySystem.cs` 45, `Accessories/AccessoryAchievements.cs` 5. That is
  145 registrations if each call is one achievement, but some may be conditional and the hidden and retired flags are
  set differently in the new files, so I did not put a total on the page. `[ClusterFAchievement list` on the test shard
  gives the real count.
- **Appraisal's thresholds** (30/60/90) came from the CHANGELOG, not traced to code.
- **Client looks**: wall trophy facings, the trap art, the farm without its two trees.

## 5. CHANGELOG

P217 section 5 says to add one line to the code repo's `CHANGELOG.md` (and bump `VERSION` per its convention). This run
may not commit there, so the line is here for whoever copies the pages over:

    ### Added
    - The player wiki catches up again: new pages for the League Shop and its Hall decor, the League Register and its repair items, deployable traps, climbing boots, accessory slots and toe rings, creature levels and Appraisal, the seasonal decorations, and a player's guide to the League; the League, achievements, loot box and bulk order pages are brought up to date; and draft pages for levelable gear and the tutorial's farm wait in the drafts section. The pages reach the wiki with its next deploy.

Under a new version section after the newest one at the time (it was 2026.10.21.20 here), with `VERSION` to match.

## 6. For Chase

1. Copy `notes/wiki-drafts/pages/*` into `docker/wiki/content/pages/` in the code repo, add the CHANGELOG line above.
2. Deploy with `sync-dokuwiki-content.sh`. The 12 updated files (5 content pages, 7 hubs) need `SYNC_MODE=overwrite` or a
   hand copy; seed mode keeps their old versions.
3. 16 new `TODO image:` shots across the pages.
4. Decide rows 31-38's status as their placement happens, and say whether the Hall decor and flying loot count as
   live before the package is published.

## 7. Working as a cloud Golem (round 2)

- The setup was done for me; the code repo was read-only by instruction, so the pages live in this repo and need a copy
  step. A standing place in the code repo that a Crystal branch may write (the wiki seed) would remove that step.
- P217's notes were the best orientation available: the format, the live rule and the citation style carried over.
- A "what is placed where" list (which `[Gen`/`[ClusterFSeed` commands have run on test and live) would have settled
  rows 31-38.

P377 DONE
