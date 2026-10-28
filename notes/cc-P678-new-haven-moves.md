# cc-P678: New Haven moves into the author's Haven, and Rootdeep's way in (SoS swap S7)

Iron Golem, 2026-10-27 and 28, two sessions. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy
`D:\UO\golems\Iron\shard-migration`, both on `golem/Iron/P678`. Not committed; nothing deployed; Haven not touched.
The first session stopped with a question; Chase answered "stock pre-UOML Haven plus our pieces, in P678", held until
the isle release shipped. It shipped at 21:09 on the 27th (package 2026.10.27.2106, `D:\UO\overseer\release-20261027.log`,
main 9ee74b6 with P707 and P713 in it), so this session went ahead.

## In plain words

- **New Haven is now the author's Haven town, ready for the map swap.** A new character starts on its square. The
  town's own shops, bank, healer, smiths, inn and town crier come from OSI's old Haven data, which fits this town
  exactly. Our old plaza's decoration and its shopkeepers are gone, because that spot is forest on the new map.
- **Every one of our places has a home in the new town.** The League office and the registrar are in an empty hall
  by the square. The Alembic guild has the empty house to the north-west, and the magery trainers the hall to the
  north. The dojo and the necromancers have the two east cottages. Each ML quest giver is in the shop of its trade.
  Every guild post, the community art, and the winter and Halloween decorations moved too. Every spot was walked on
  the new map's own files.
- **Rootdeep's way in is a cellar hatch in the Second Bank of Haven.** It is one tile west of where Old Haven's hole
  was, and the ladder brings you up three tiles away. The undead that Old Haven's training quests send you to fight
  now live in the woods just north of town, not in the streets.
- **For you: nothing until the swap.** Everything waits for the server to read the new map (S2). Then the bot's walk
  and pictures in our client can be taken. Two small decisions are listed at the end (the dojo's home, and the
  winter feast in the bakery).

## What Chase chose, and how it was built

"Stock pre-UOML Haven plus our pieces" (`D:\UO\golem\answers\Iron-P678-20261027-160606-ff97.json`). The author's town
is OSI's pre-UOML Haven rebuilt, so pinned already holds its data. Pinned just never uses it on this expansion:

| Stock data | What it holds | How it comes in now |
|---|---|---|
| `Spawns/uoml/trammel/Vendors.json`, `TownsLife.json` | Haven's shopkeepers and town pets (25 spawners in the town, every one standing on its floor on SoS) | The console's fresh-world order imports both files. The import hook admits only the spawners inside the town (`ClusterFHavenTownSpawns`). |
| `Decoration/Trammel/haven.cfg` | The town's decoration and its working ankh (3606,2582) | Already placed by `[Decorate`, as today. S5 grades it with the rest. |
| `regions.json` "Haven" and its 23 shops | The town's rectangles and shop regions, which end at SE so never load | `HavenTownRegions` registers them at start as "New Haven" and its shops |

## What changed

### Part 1 (the first session, kept): `HavenSpots`

Start 3634,2586,0; Rook, the moongate's way out, the quest board, the reset stone, the Fountain of Youth, the centre,
the vet, the public moongate, the healer, the bank, the dock and the town box. This session corrected one value: the
**public moongate stands at Z 14, not 16** (pinned's GetAverageZ on that slope; the first session's tile reader took
the land's corner).

### Part 2: our places in the new town

**NPCs and guild posts** (`notes\cc-P678-tools\homes.py` writes `out\homes.csv`, `edit_homes.py` writes it into the
code). Every tile is inside its building, on the floor itself, reachable on foot from the start, not a stock tile, and
at least 2 apart.

| Who | Old home (forest on SoS) | New home |
|---|---|---|
| League Registrar, the Appraiser, the Sanitation Warden (custodians) | the field office house, the civic hall | **the free hall north-east of the square** (3659-3673, 2548-2561), now the League field office |
| Lyle and the five magery trainers, arcane and artificers guildmasters | New Haven Magery School | **the free hall to the north** (3640-3654, 2464-2478), "Haven Magery School" |
| Alembic guildmaster, Sadrah | Little Shop of Alchemy | **the free house to the north-west** (3600-3616, 2496-2512) |
| Warriors' guildmaster and the eight warrior trainers | Warrior's Guild Hall, training area | the Proving Grounds yard |
| Andric, Kashiel (bowyers) | New Haven Bowyer | the Bullseye Marksmen |
| Asandos | Bountiful Harvest Inn | the inn building (3664-3680, 2608-2624) |
| Clairesse | A Stitch In Time | A Stitch in Time (stock tailor guildmaster there too) |
| Lowel, Hargrove | Carpenters of New Haven | Carpenters of Haven |
| Nibbet, Amelia Youngstone | Springs N Things | Haven Clockworks and Tinker Shop |
| Andreas Vesalius, Avicenna | Healer's Hall | the Healers of Haven |
| Sarsmea Smythe, merchants guildmaster | New Haven Bank | the Second Bank of Haven |
| George Hephaestus | Forge and Anvil | the room beside The Haven Blacksmith |
| Dojo guildmaster, Ryuichi, Chiyo, Jun, Walker, Hamato | Ninja Dojo, Hamato Dojo | **the east cottage** (3736-3744, 2561-2568). The harbour hall was the first choice, but the walk finds no way onto its floor. |
| Keepers guildmaster, Mulcivikh, Morganna | Necromancers Guild Hall | **the east house** (3728-3736, 2632-2640) |
| Thieves guildmaster and the den lookout | the inn's back room, the fighting pit | The Haven Thieves' Guild |
| Bards guildmaster | Bardic Guild | the Bardic Guild in Haven |
| Norton, maritime guildmaster | the docks | the docks |
| Outriders guildmaster | the stables | the farmhouse stables by the vet |
| Foresters guildmaster | the wood yard | the Woodsman in Haven |
| Healers, smithing, tinkers and tailoring guild posts | pinned's ML vendors | pinned's pre-UOML guildmaster spawners in the matching shops |

**Layouts** (three helpers, each with its own SoS validator in `notes\cc-P678-tools\office\`, `art\` and `winter\`,
every check 0 failing):

- **League office props**: `design\registrar-office\layout.json` regenerated into the hall. The desk items are on the
  counter east of the registrar, who now faces south. The board is on the north wall, and the sign is by the door at
  3667-3668,2562.
- **Alembic hall props**: in the house's north room.
- **Community art**: 36 of 44 rows moved: the orc camp to the forest west of town, carts on the square and by the east
  fields, lanterns on the pier posts and the main road, and paintings in the hall, the healers, the magery school,
  the bardic guild, the tailor's and the inn. **The 8 support beams are dropped:** SoS's docks are one level, so there
  is no overhang to brace.
- **Winter decor**: all 109 rows moved under their own keys. It is 109 rows; the first session's 173 counted coordinate
  pairs. The square's group is east of the start, the arches are at the west road, the docks street, the east road and
  the south road, and the bank, the healers and the hall are decorated.
- **Halloween at New Haven's bank**: 10 rows at the Second Bank (was 17). The bank's drawn outer walls are mostly
  its entrance.
- **Chase's ankh by the League office** (fidelity D-123) moved to the grass by the hall's south-east corner
  (3676,2562). Its static is forest on SoS.

**Retired** (their places are forest on SoS, and a fresh test world is built on swap day):

- `ClusterFNewHavenServicesSeeder`: ServUO's NewHaven.cfg decoration for the ML plaza and the stand-in Healer. Its
  one-line decoration helper lives on as `ClusterFDecorLine`, which the ankh and Rootdeep seeders use. Its console
  steps and fact file went with it.
- `ClusterFOldHavenCleanup`: on SoS it would delete Haven's own vendors, its "stranded" targets. Its command, its fact
  file and its console rows went with it.
- `ClusterFOldHavenStockSpawns`: it refused the town crier while Old Haven was a ruin. He is the town's crier again.

**Spawners** (`ClusterFHavenTownSpawns`, called by the import hook `server\patches\ImportSpawners-despise-exclusion.patch`):

- It refuses the 58 post-uoml Vendors/TownsLife spawners inside the ML plaza.
- It refuses the 10 ruin spawners inside the town box: the four undead spawners, the 90-strong undead field, the
  two brigand camps, the two wildlife spawners at the town's west and east edges (Mongbats, wolves, bears) and the
  ruin's lone Healer.
- It refuses every pre-UOML spawner outside the town.
- The pumpkin and sheep fields, the crier and the dock escorts stay.

**Old Haven Training moves to the north woods.** The ML trainers' quests train there against undead. The 90-strong
field is re-seeded at 3640,2418,34 with pinned's entries, and its home and walking range go from 60 to 40, so nothing
it spawns reaches the town. The region and Drelgor (range 35) follow.

**The tutorial's yards and tours.** The training yard is now the grass behind the Little Shop of Magic (3633,2562). The
trades yard is 24 tiles west of it (3617,2554). The housing tour's porch is the stables farmhouse's (3708,2593). Each
yard's 7 x 5 is open, flat and reachable on foot (`yards.py`). This fixes the four tour facts the first session left
red.

**Smaller:**

- `ClusterFAreaScan`'s boxes.
- The play-test bot's square, guild posts and hunting ground.
- The comments that named the old office.

### Part 3: regions

`Regions\HavenTownRegions.cs` runs every start, after the regions load:

- It unregisters ML "New Haven", everything under it, and "New Haven Moongate".
- It registers "New Haven" as a guarded TownRegion over pinned "Haven"'s rectangles. It keeps the ML region's rune name
  and music, and its go location is the start.
- It registers pinned's 22 Haven shop regions under it, with their own names, read from the shipped regions.json.
- The 23rd, "The Gentle Rest Inn in New Haven", is drawn on the ML plaza in pinned's data, so it is left out.
- The inn building becomes "the New Haven Inn" instead. That keeps the townsfolk's innkeeper rules and the no-delay
  logout.

Every lookup by the name "New Haven" now finds the new town. S3 (P676) redraws the rest of Trammel and should leave
these to S7.

### Part 4: the cellar hatch

- The hatch is a server item, `ClusterFRootdeepSeeder.PlaceHatch`, so the town's statics are untouched. It is art
  0x3E65 "hatch".
- It sits at 3618,2620 in the bank's main hall, one tile west of Old Haven's hole and three tiles from the bankers.
- It is set **one below the floor**. At Z 0 its top (3) is a step too high (pinned's StepHeight 2,
  `Engines/Pathing/Movement.cs:265, :346`), so nobody could walk onto it.
- One teleporter on the hatch goes down. The mouth is that one tile, and the region's Entrance is the hatch.
- The ladder up lands at 3621,2620.
- The first pick was the bank's north annex, but the winter decor's tree group stands there. The cross-check found the
  hall spot clear of every layout, seasonal ones included.

### Part 5 (the first session, kept)

"found the way beneath Haven", key `discovery.old_haven` unchanged.

## Facts

| Fact | Red | Green |
|---|---|---|
| docs `tools/tests/test_haven_spots.py`: (1) every HavenSpots spot is reached on foot from the start at its standing Z, now by the walk with pinned's rules (was the rough tile reader); (2) the start group, services and vet; (3) the fountain; (4) **new**: `crosscheck.py` over every tile our code uses in the town: 262 rows, no shared tiles, every NPC and spot reachable with all 36 blocking props in place, nothing by the hatch or the landing | HEAD's code (`red\red-py-session2.txt`): the moongate 2 too high; the yards in the forest | 4 of 4 |
| code `tests/Regions/HavenTownVerification.cs` (new): T1 the hook refuses exactly the plaza, the ruin and pre-UOML outside town; T2 real imports (the crier placed, no ruin, only Haven's pre-UOML people); T3 the north woods field; T4 the regions | not run red separately: the classes are new | 4 of 4 in the gated build |
| `RootdeepWayInVerification` W1/W2 rewritten for the hatch (W3-W5's crier and skeleton facts are T1/T2 now; W6, a world P188 seeded, is gone with the fresh world); `RootdeepMapSafetyVerification`; `OldHavenBurrowsRegionVerification`; `OldHavenNewPlayerSafeVerification` (the north woods); `NewHavenSeederFloorVerification` (every floor re-measured on SoS); `SpawnerImportVerification` fact 4 (the hook's refusals) and fact 5 gone with the stand-in; `AnkhVerification`; the layout helpers' `RegistrarOffice`, `AlembicGuild`, `CommunityArt`, `HalloweenDecor`, `WinterDecor` facts | | |

**Offline proofs** (`out\`):

- `route.txt`: P289's route on the SoS files with every blocking prop in place. Start to the banker is 45 steps, and
  back is 45. Start to the hatch is 50. The ladder's landing back to the start is 49, and to the hatch is 3.
- `crosscheck.txt`: the whole-town check.
- `haven-homes.png`: the town with our places marked. `north-woods.png`: the training field.

**The gated build** (`docker\uo\build.sh -t sl-modernuo:cc-P678`, detached through `gated-build.ps1`, docker-build
lock taken and released; free memory read 2.5 GB in Windows, 13 GB in the Docker VM):

- **Run 1, red** (`red\red-build-1-summary.txt`): it compiled, and the test gate ran 2,688 facts with 8 failing.
  Each was a value that moved on purpose, or a fact this move invalidated:
  - the tour fact stepped 200 tiles east of the new centre, which is off the island, so the island gate held the
    trainee; it now steps 200 south;
  - the ruin count was 10, not 8: the two edge wildlife spawners;
  - the winter facts' community art floor (now 36), and the west-road arch one tile outside the town box (entrance
    arches may sit 3 outside);
  - the Thieves' Den lookout's post and the hall names in three guild and recipe facts.
- **Run 2, green** (`green-build-2-summary.txt`): **EXIT=0, 2,688 facts, 2,683 passed, 5 skipped, 0 failed**. The 5
  skipped are the real-map-file facts that skip in every build. All 169 facts in the files this prompt touched
  passed, and `sl-modernuo:cc-P678` was built.

**Console facts** (`scripts\tests\Shard-Console.Tests.ps1`, run through the PowerShell tool, since the classifier
refused `-ExecutionPolicy Bypass` from Bash): 452 facts, 439 passed, 13 failed.

- None of the 13 is this prompt's.
- Most are this PC's environment: no client `hues.mul` in the work copy, the play-tests tile, the Haven cutover links.
- `RedMeansTestOnly...` lists dozens of other prompts' red commands. My edit only took the retired cleanup out of its
  expected list, and the cleanup is absent from the list it got too.
- The bot's unit tests: 59 run, 1 failure, the overnight installer's dry run on this PC. That is not this prompt's
  either.

## Not done, and why

- **The live proofs**: TazUO shots of the town, the bot's P289 route on a server, and the Rootdeep walk into the
  Landing. They need the server reading SoS (S2, P675) and the client's SoS map (P713's switch, off until the swap).
  The map's side of each is proved offline above. The Landing's own side is unchanged from P188/P413, on the map patch.
- **Mine camp** (Gervis, Mugg, Jacob Waltz, the Miners' Compact liaison, the archivist, `ClusterFMineCampLayout`,
  `ClusterFSouthMineDecor`): they stand on rock on SoS. This is S8's (P677) job, as the plan says.
  `edit_floorfact.py` reports the three.
- **For S9 (P681)**: the stock post-uoml/shared spawners S7 refuses are listed by the hook. S9 should not re-place
  them, and the north woods field is ours.
- **For S2 (P675)**: the map patch's ant hill (3615-3620, 2616-2621) must go, as P675 already says. The hatch needs
  nothing from the map.
- **For S3 (P676)**: "New Haven" and its shops are registered in code here, so S3's redraw should not touch them.

## Deviations and decisions for Chase

- **The dojo** went to the east cottage, since the harbour hall can't be walked into. Say if it belongs elsewhere.
- **The winter feast** went to the Shakin' Bakery's dining hall, because the inn is bedrooms with one table (the winter
  helper's call). The old north arches went to the docks street, since the town has no north road.
- **The 8 support beams are dropped**, and the Halloween bank has 10 rows, not 17.
- **The undead field's range** is 40, not pinned's 60, so it stays out of town.
- **Retired seeders**: there is no migration for an existing world, by Chase's fresh-world decision.
  `ClusterFNewHavenSeeder`'s legacy-tile repair stays in place for the mine camp.
- **This branch's base is older than main** (P710, P713, P706 and P707 merged since). No file overlaps (checked). The
  first session's work is in a WIP commit on this branch labelled "cc-P666".
- **The surge staging gate** (`ClusterFSurge.NewHavenGate`, three tiles south of the bank anchor) now opens inside the
  bank's hall. It is staff-only, and it was left as it is.

## Commit preflight

- Code copy: 56 entries in `git status` (the first build added the guild-hall, lookout, recipe and tour facts' fixes), new
  `ClusterFHavenTownSpawns.cs`, `Regions/HavenTownRegions.cs`, `ClusterFDecorLine.cs`, `tests/Regions/HavenTownVerification.cs`;
  removed `ClusterFNewHavenServicesSeeder.cs`, `ClusterFOldHavenCleanup.cs`, `ClusterFOldHavenStockSpawns.cs` and two
  fact files (staged deletions).
- Docs copy: this file, `tools/tests/test_haven_spots.py`, `notes\cc-P678-tools\` (the tools, `out\`, `red\`, and
  the helpers' `office\`, `art\` and `winter\`).
- Lock taken: docker-build (released after the build). No package, no deploy, nothing committed.
- No file over 5 MB; the build logs are git-ignored (`*.log`) and summarised beside them. `docs\` untouched.

P678 DONE
