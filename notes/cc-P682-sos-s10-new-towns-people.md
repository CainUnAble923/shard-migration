# cc-P682: people for the author's new towns and keeps, and wild creatures on his new land (SoS swap S10)

Iron Golem, 2026-10-29. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P682`. Not committed; nothing deployed; the test shard not touched. Place names and land are
Zigholtul's (Siege of Sosaria Trammel Map 3.0). The rosters are P695's draft (Verite, from P672's cast).

## In plain words

- **The author's six new towns have people now.** Valunstead, Hammerhill, Kameron Kove, Elmhaven, Kettleburg and Fort
  Yondall each get a banker, a healer, a smith, a provisioner and the other shops P695 planned, standing inside the
  buildings that fit their trade (the smith at the forge, the tailor at the loom, the baker at the oven). Each town also
  gets guard posts, a town crier, wandering townsfolk and town animals, about as many per tile as a stock town.
- **The five keeps get a small garrison:** Fort Whitestone, Castle Dunbain, Fort Stormhammer, Tigerclaw Fortress and
  Khalahandra Keep, 2 to 6 armoured guards each, at the gate and inside.
- **The author's new land gets wild creatures:** the new Nujel'm desert continent, Glimmerwood and the new islands.
  Each kind of ground gets the creatures stock puts on that ground (scorpions and giant spiders on sand, the forest
  mixes in the woods), at stock's density, and none in towns, the fenced unfinished land or near the sealed dungeons.
- **For you:** nothing goes live until the swap does. On swap day the fresh world needs one more command after the
  stock spawn files, `[GenerateSpawners Data/Spawns/sos/**/*.json` (the console's fresh-world list now has it). Two
  things to know: Fort Yondall's keep is sealed by its portcullis on this map, so its shops can only be reached by
  recall or gate until S15 (P688) finds or opens a way in; and the named people of P695 (Mabel Quinn the banker and so
  on) are not given their names yet (see below).

## How it was done

`notes\cc-P682-tools\build_spawns.py` reads the SoS map (P481's copy, through P681's `sosgrid` walk rules), the
shard's Trammel regions (P676's `regions-trammel.json`), P695's rosters (`cc-P682-tools\rosters.json`, copied from
`golem/Verite/P695` f8c5099, not merged to main), P669's author points and new-island list, and P681's ledger of the
stock spawners S9 keeps or moves. It writes the spawn files into the code copy and its working figures into
`cc-P682-tools\out\`. Every spawner is a stock ModernUO spawner record in pinned's spawn JSON with a fixed guid
(uuid5 of its facet, place and role), so a rebuild gives the same file and a re-import replaces, never duplicates.

**Starting point.** The prompt says to start from P695 if it has merged. It has not (its branch is
`golem/Verite/P695`); I used its rosters as the source of which trades and how many, and checked each on the map
rather than redoing them.

### The towns (part 1): one spawn file per town

- **Buildings** are the roofed tiles of the town's region (a non-foliage static 10 or more above the standing Z), joined
  4-way into components of 9 or more tiles, that a player walks into.
- **Walking in.** A tile counts as reachable if it joins (steps of at most 8 Z, as stairs climb) the walkable land
  round the town, or the author's Bank point / the region's go point (where recall and the go-menu land). Both are
  needed: Valunstead's survey box is ringed by water, and Fort Yondall's go point is inside a keep that its portcullis
  statics seal from the courtyard. `out\build-log.txt` lists the four places where the two are not joined on foot
  (Elmhaven, Kettleburg, Fort Yondall, Khalahandra Keep's high entrance): for S15's route walk.
- **Shop by its statics.** Each building is scored by the trade fittings among its statics and one tile round it
  (tiledata names: forge, anvil, bellows for a smith; loom, spinning wheel, bolts of cloth for a tailor; oven and flour
  for a baker; woodworker's bench and saws for a carpenter; a bar, kegs and beds for an inn; gold coins and counters
  for a bank; bandages and wash basins for a healer; and so on, `FITTINGS` in the tool).
- **Assignment.** The banker goes in the building holding the author's Bank point when he has one (Valunstead,
  Hammerhill, Kameron Kove). Every other trade takes the free building whose fittings score best for it; a trade with
  no fitting in town takes the largest free building; with no free building left it shares one. Of the 56 Trammel shop
  placements, 39 are by fittings or the Bank point, 12 by size and 5 share (all five in Fort Yondall, whose only
  building is the keep, with no fittings at all).
- **Where they stand:** the building's deepest reachable interior tile (rings in from its walls), 3 or more tiles from
  another shopkeeper, home range 0 and a walking range of 0 to 2 by how deep the tile is: they stay indoors.
- **Guards** are stock `OrderGuard` posts, one per post, range 0, walking 1: the type and record of stock's Serpent's
  Hold posts (`shared/trammel/TownsPeople.json`). Stock spawns no WarriorGuard or ArcherGuard anywhere (P628's
  inventory), and P695 says never to use them as decoration: a guarded town's real guards still come from its region
  (S3), as in every stock town. P695's guard counts (8 for Valunstead, 6 for four towns, 4 for Fort Yondall). The first
  post stands by the bank; the rest are spread over the town's reachable streets.
- **Townsfolk** are stock's town mixes: a TownCrier by the bank (stock's 1-count, range-1 record), the
  EscortableMage/Noble/SeekerOfAdventure walkers (3 at a time, range 10, one spawner per 15,000 dry tiles), and
  Bird/Cat/Dog/Rat, sized so the town meets stock's town median density.
- **P695's other residents** (relief clerks, drain tenders, dock hands) and the **named people** are held. P695 says
  its non-vendor residents and quest actors "require later actor implementation", and a vendor's random gender would
  not match a name like Mabel Quinn. They come with the quest build (P672) that gives them their lines.

| Town (Trammel; Felucca the same) | Shops placed | Banker | Healer | Guard posts | Townsfolk |
|---|---|---|---|---|---|
| Valunstead | 11 (11 by fittings or the Bank point) | 482,430,25, the author's Bank point | 332,386,7, beds and bloody bandages | 8 | 154 |
| Hammerhill | 9 (7) | 1538,985,5, the Bank point | 1594,994,0, beds | 6 | 9 |
| Kameron Kove | 10 (7) | 1297,2461,10, the Bank point | 1299,2489,10, wash basin and bandages | 6 | 9 |
| Elmhaven | 10 (5) | 1965,3159,1, gold coins and a counter | 1995,3248,1, bedroll | 6 | 26 |
| Kettleburg | 10 (9) | 632,2395,0, gold coins and a counter | 706,2515,0, beds | 6 | 86 |
| Fort Yondall | 6 (0, all in the keep) | 3393,337,0 | 3393,334,0 | 4 | 4 |

Every placement, with its building, fitting score and reason: `out\towns-placed.csv`; every surveyed building and its
top fittings: `out\town-buildings.csv`.

### The keeps

A small OrderGuard garrison at each, P695's count (Fort Whitestone 4, Fort Stormhammer 4, Tigerclaw Fortress 2,
Khalahandra Keep 6) and 2 at Castle Dunbain, which P695 gives no public guards because its rooms are the Open Ledger's
(P672-06) encounter: Dunbain's 2 stand at the gate only. Elsewhere half stand on the outdoor tiles nearest the author's
point (the gate) and half inside the keep's largest building. No shops or healers: the prompt asks for a garrison, and
P695's keep services are proposals for later.

### The wild (part 2)

- **Stock's terrain-to-spawn table, measured from stock.** Every stock wild-encounter and wildlife spawner on the
  surface (P681's ledger kinds, x under 5120, outside the stock towns), grouped by the terrain class of its home on the
  stock map (P681's classes from the tiledata land names). The rate is stock's creatures per 100 dry outdoor tiles of
  that class outside towns. Felucca's table is Felucca's own.
- **The new land:** the author's Nujelm Desert and Moonglow Forest regions (the new continent) and Glimmerwood, each
  taking only land that was sea or void in stock or whose terrain class changed; and the 59 surface components of
  P669's 65 new islands (the six dungeon strips are S18's), their newly dry tiles.
- **Left out:** towns (all guarded regions, plus 10 tiles), S14's five closure boxes, dungeon regions, 12 tiles round
  every author dungeon entrance, roofed tiles, water, and land already in range of a stock wild spawner S9 kept or moved.
- **Placing.** For each area and terrain class, stock spawners of that class are copied (entries, count, ranges,
  delays) onto random tiles of it, spaced by their range, until the area holds stock's rate; the last one's count is
  trimmed to the target. A copied range shrinks (to 3 at least) until a quarter of it is land, else the tile is skipped.
  Stock's wide wildlife fields (40 deer over 100 tiles) are scaled to a 30-tile range at the same density.
- **Held:** no copy of a stock spawner holding P698's B3 tier (dragons, drakes, daemons, liches, efreets and the like:
  "isolated from towns and travel, after review"), treasure chests or camps, or Old Haven's undead training field.

| Facet | Area | Spawners | Creatures | Free dry tiles | Per 100 | Stock's rate for that ground |
|---|---|---|---|---|---|---|
| Trammel | Nujel'm continent | see `out\wild-ledger-trammel.csv` | 633 | 671,241 | 0.094 | 0.094 |
| Trammel | Glimmerwood | | 104 | 69,530 | 0.150 | 0.151 |
| Trammel | new islands | | 377 | 264,804 | 0.142 | 0.148 |
| Felucca | Nujel'm continent | see `out\wild-ledger-felucca.csv` | 757 | 671,241 | 0.113 | 0.113 |
| Felucca | Glimmerwood | | 104 | 69,530 | 0.150 | 0.150 |
| Felucca | new islands | | 361 | 257,369 | 0.140 | 0.145 |

What the mixes are, by ground: sand (the desert) is stock's GiantSpider/Scorpion and EarthElemental/Ratman spawners;
forest and grass mix stock's wildlife fields (deer, bears, wolves, birds) with its Ettin/Troll/Orc encounters; jungle
takes stock's Alligator/Lizardman/Snake and wildlife; dirt adds stock's savage and orc camps' fighters and brigands.

## The density figure (part 3)

Full text: `cc-P682-tools\out\density.txt` (`density.py`). Per 100 dry tiles:

- **Towns:** stock's 19 Trammel towns hold their people and town animals at a median of **0.256** (range 0.072 for Yew
  to 1.80 for the Heartwood). The new towns: Valunstead 0.259, Hammerhill 0.261, Kameron Kove 0.266, Elmhaven 0.259,
  Kettleburg 0.257, Fort Yondall 0.531 (small, with a full set of services). Felucca: stock median 0.268, new towns 0.283
  to 0.287, Fort Yondall 0.531.
- **Wild:** stock's surface wild is **0.166** per 100 dry outdoor tiles on Trammel (forest 0.225, grass 0.092, jungle
  0.140, sand 0.048, snow 0.070, rock 0.163, dirt 0.318). The new land: **0.111** on 1,005,575 free dry tiles, against
  0.112 that stock's rates give for the same ground (it is mostly sand, which stock spawns thinly). Felucca 0.122
  against 0.124.

## How the server uses it

- `server\data\Spawns\sos\towns\<Town>.json` (6), `keeps\<Keep>.json` (5) and `wild\{NujelmContinent,Glimmerwood,
  Islands}.json`: 14 files, 810 spawners (Trammel 374, Felucca 436), 3,176 creatures, 652 KB. Each file holds both
  facets. Generated by `build_spawns.py`: do not edit by hand.
- `docker\uo\Dockerfile`: `COPY server/data/Spawns/ /build/modernuo/Distribution/Data/Spawns/`, so the set sits at
  `Data/Spawns/sos/` beside pinned's own, for the server and the tests.
- `scripts\Shard-Console.ps1`: the fresh-world order gains `[GenerateSpawners Data/Spawns/sos/**/*.json` after the 14
  stock files (`Shard-Console.Tests.ps1`'s fact now counts 15 and checks it is last).
- No C# code: the stock importer builds the records. None of the import's hooks touch them (Despise's and Haven's
  refusals and S9's placements match by stock guid; these guids are none of stock's, a fact).
- **Migration dropped** (Chase's fresh test world): nothing adds these to an existing world but the command.

## Facts

| Fact | Red | Green |
|---|---|---|
| docs `tools/tests/test_sos_new_spawns.py`: (1) every home passes P681's walk test on SoS; (2) every new town has a banker, healer, smith and provisioner on each facet, in its region, indoors and reachable; (3) no wild spawner in a town (+10), closure, dungeon region, near an author dungeon entrance or past x 5120, none held, every entry a stock name; (4) each keep's garrison on each facet, OrderGuard only, within 40 of the author's point; (5) towns at 95 percent or more of stock's town median, each wild area within 10 percent of stock's rate; (6) guids unique and none of stock's, Trammel and Felucca only | a mutated set (`mutate.py`: Hammerhill's Trammel banker removed, a wild spawner moved onto Valunstead's bank, a Dragon added, a Whitestone post dropped): 4 of 6 fail, `red\red-facts-mutated-set.txt`. Fact 1 also caught a real fault there, a Felucca island spawner whose range had shrunk to the minimum without reaching land; the tool now skips such tiles | 6 of 6, `green-facts.txt` |
| code `server/tests/Misc/SosNewSpawnsVerification.cs`: (1) every record a Spawner on Trammel or Felucca, guids unique and none of stock's, every entry a mobile type; (2) on each facet every new town's four core services inside its region (regions-trammel.json); (3) a real `[GenerateSpawners Data/Spawns/sos/**/*.json` builds every record where the file puts it, with its count and ranges | the gated build without the Dockerfile line (the set not shipped): exactly these 5 fail, 2,758 others pass, `red\red-build-1.txt` | 5 of 5 in the gated build |
| code `scripts/tests/Shard-Console.Tests.ps1` `TheFreshWorldGroupIsTheFifteenSpawnStepsThenShameThenDespiseThenSave` | | passes (run in my copy: 452 facts, 434 passed, 18 failed; see below) |

**The gated build** (the repo's gated build script, `-t sl-modernuo:cc-P682`, detached through `cc-P682-tools\gated-build.ps1`;
docker-build lock taken and released; 1 to 5 GB free in Windows, 13 GB in the Docker VM):

- **Run 0:** did not compile, xUnit2029 (`Assert.Empty` over a `Where`); now `Assert.DoesNotContain`.
- **Run 1, red** (the set not shipped): 2,769 facts, the 5 new ones failed, the rest passed.
- **Run 2** (`red\red-build-2-two-fails.txt`): 2 failed. My fact's floor of "more than 1,000 records" was wrong (the
  set has 810; now "more than 500"). And `CC6Batch1CreatureVerification.EveryStockSpawnEntryNamingOneOfTheTwentyNowResolves`
  counts entries across every file in `Data/Spawns` and pins 46: three of my wild copies name its goblins, so it saw
  49. It is a fact about stock's files, so it now skips `Data/Spawns/sos` (a commented two-line change).
- **Run 3, green** (`green-build-3.txt`): **EXIT=0, 2,769 facts, 2,763 passed, 6 skipped, 0 failed.** The skips are
  the real-map-file facts that skip in every build.

**The console's facts** (`Shard-Console.Tests.ps1`, PowerShell): the changed fact passes. 18 others fail in my copy,
all about window actions, website and map buttons, dashboards and Portainer (P83, P84, P101, P107, P133, P135, P163 and
four window-mode facts), none touching the fresh-world list. I tried the same run on an export of the branch's HEAD to
show they fail there too: the first try hit Windows' 260-character path limit in the scratchpad, and Claude Code
stopped the second for low memory while the build ran. So whether those 18 already fail before this change is **not
verified**. To check: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1` on main.

## Not done, and why

- **Named people and non-vendor residents** (P695's 18 named townsfolk across these towns, the clerks and crews):
  held for the quest-actor build, as P695 asks.
- **Elandrim Nur Shaz, Seraphim Peak, Skaddria Naddheim, Viligant Valley, Sea Market, Plunderers Peak** and P695's
  other places: not on the prompt's list. P701 (finding 2) flags that their law and purpose need deciding first.
- **Felucca's regions.** Felucca has no SoS regions until S13 (P686), so its copies of the towns have no guard zone
  yet; their OrderGuard posts stand there anyway.
- **In-game walk and pictures.** These need the server and client on SoS together (S1, S2 live); the walk-in routes
  of the four split places go to S15 (P688).
- **The stock towns P681 found short** (Cove's bank, Yew's and Wind's smiths, Nujel'm's healer and provisioner,
  Magincia's smith and provisioner): S10's list is the author's new towns, and adding to stock towns changes their
  stock layout, so they stay a question for Chase.

## Deviations and decisions for Chase

- **The Read tool was denied** (unattended run) on `scripts\Shard-Console.ps1` and `docker\uo\Dockerfile` in my code
  copy, which sits outside this session's working folder. As my standing notes say for that case, I read them with
  Bash and changed them with a small Python script that replaces exact text (`cc-P682-tools\edit_code.py`;
  the three edits are the Dockerfile line, the console step and its fact, shown in the diff).
- **Guards are stock OrderGuards**, not a new guard type: the only stock spawned guard record. If Chase wants the posts
  to look like town watch rather than Serpent's Hold's order guards, that is a later dress change.
- **Castle Dunbain** gets 2 gate guards although P695 proposes none, because the prompt asks for a garrison at every
  keep; they stay out of its rooms.

## Commit preflight

- **Code copy:**
  - new `server/data/Spawns/sos/` (14 JSON files, 652 KB, none over 300 KB) and
    `server/tests/Misc/SosNewSpawnsVerification.cs`;
  - changed `docker/uo/Dockerfile` (the COPY line), `scripts/Shard-Console.ps1` (the fresh-world step),
    `scripts/tests/Shard-Console.Tests.ps1` (its fact: 15 steps, the SoS set last) and
    `server/tests/Mobiles/Normal/CC6Batch1CreatureVerification.cs` (stock's files only).
- **Docs copy:** this file, `tools/tests/test_sos_new_spawns.py` and `notes/cc-P682-tools/` (the tools, P695's
  `rosters.json` copy, `out/`, `red/`, the fact and build outputs; about 2.8 MB). The map grid caches stay outside the
  repo (P681's `%TEMP%\p681-sosgrid*.npz`).
- **Lock:** docker-build, taken for the gated builds and released. No test shard, package or Haven work. Nothing
  committed.

P682 DONE
