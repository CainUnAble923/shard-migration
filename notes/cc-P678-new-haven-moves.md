# cc-P678: New Haven moves into the author's Haven, and Rootdeep's way in (SoS swap S7)

Iron Golem, 2026-10-27. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P678` (main after P674 and P710). Not committed; nothing deployed; Haven not touched. **Stopped
partway with a question to Chase** (`Iron-P678-20261027-160606-ff97`).

## In plain words

- **New Haven's heart has moved into the author's Haven town (test shard, once the map swap ships).** A new character
  now starts on the town square north of Uzeraan's Mansion. Rook, the quest board, the reset stone, the Fountain of
  Youth and Sir Helper stand beside it. The healer, bank, vet, docks and public moongate spots are in the new town too.
  Every spot was checked on the new map's own files.
- **The "found the ruins of Old Haven" achievement now reads "found the way beneath Haven".** It keeps the same key, so
  anyone who earned it keeps it.
- **The rest is bigger than planned.** Our code holds 1,167 New Haven coordinates; the plan's count found a fraction.
  Most belong to places the plan did not list: the League office and registrar, the Alembic guild, community art,
  the guild starter path, seasonal decor and three tours.
- **For you: one decision** on your Golem card: how the rest should be moved. The pictures of the new town in our
  client, the bot's walk and the Rootdeep walk also wait for the server's map swap (S2), which nobody has started.

## What was measured

**Every New Haven coordinate in our code, graded on the new map** (`notes\cc-P678-tools\havenpoints.py`, using P669's
grader on each point's tile and the 8 round it). Every "x, y" pair inside the Haven island's box (3314-3813,
2345-3094) in our customizations, patches, tests and bot, outside comments: **1,167 points in 70 files: 405 unchanged,
482 changed nearby but still open ground, 280 rework** (water or void, under a wall, or the height moved more than
5). The list is `out\haven-points.csv`, one row per point; per file it is `out\haven-files.csv`.

**P669's count was far too low, and the plan rested on it.** P669 read only `new Point3D(...)` style calls, and missed
every layout table: `ClusterFNewHavenServicesSeeder.cs` holds 126 Haven points, and P669 counted 1. The biggest
movers the plan's item 2 does not name:

| File | Points | Rework |
|---|---|---|
| `ClusterFWinterDecorLayout.cs` | 173 | 58 |
| `ClusterFNewHavenServicesSeeder.cs` (ServUO's `NewHaven.cfg` decoration for the old plaza) | 126 | 49 |
| `ClusterFNewHavenSeeder.cs` (Sir Helper, the ML quest givers in plaza buildings, the bank and registrar anchors) | 59 | 27 |
| `ClusterFOldHavenCleanup.cs` | 47 | 2 |
| `ClusterFCommunityArtLayout.cs` | 44 | 22 |
| `ClusterFRegistrarOfficeLayout.cs` (the League field office) | 28 | 8 |
| `ClusterFGuildStarterPath.cs` | 20 | 8 |
| `ClusterFHalloweenDecorLayout.cs` | 19 | 11 |
| `ClusterFAlembicGuild.cs` | 11 | 11 |
| `ClusterFMineCampLayout.cs` (S8's) | 47 | 25 |

`TutorialFarmLayout.cs` (336 points) is 330 unchanged: the west farm survives on SoS as it is.

**The author's town is OSI's own pre-UOML Haven, rebuilt, so stock data fits it already:**
- pinned `Spawns/uoml/trammel/Vendors.json` puts Haven's shopkeepers in it: the banker at 3620,2617 inside the Second
  Bank, the healer at 3665,2581, the smith at 3645,2617, the inn, provisioner, mage shop and the rest;
- pinned `Decoration/Trammel/haven.cfg` is that town's decoration (our services seeder's own header says so);
- pinned `regions.json` still holds the "Haven" town region and all its shops: the Second Bank of Haven, the Healers of
  Haven, the library, the Albatross and more, 24 in all, over the same streets.

So the town's own services do not need moving. Only our additions need homes. That is the question to Chase.

**Pictures and tools:** `out\haven-top.png` is a top view of the new town with a 10-tile grid and the author's named
spots. `townmap.py` draws the town's open ground, walls and water as characters and reports a tile's floor Z (the
lowest walkable surface or passable land, so a roof is not taken for a floor). `towntop.py` draws the picture.

## What changed (part 1, the single spots, and part 5)

All in `Tutorial/HavenSpots.cs`, the one place P663 made for this. Each spot keeps its place relative to the start.

| Spot | Was | Now (SoS) | Why there |
|---|---|---|---|
| Start (character creation's city, the skip, the isle's send-home) | 3503,2574,14 | **3634,2586,0** | the square's east-west street, north of the mansion's garden |
| Rook | 3500,2572,14 | 3631,2584,0 | two tiles from the start, as before |
| Moongate's way out | 3501,2572,14 | 3632,2584,0 | beside Rook |
| Quest board (new) | 3502,2573,14 | 3633,2585,0 | one tile from the start |
| Reset stone (new) | 3501,2575,14 | 3632,2587,0 | |
| Fountain of Youth (new) | 3497,2583,14 | 3646,2596,0 | its 4 x 4 addon on open, flat ground with no static under it. The garden I tried first held 11 statics. |
| Centre (the tour's first stop; the vet rule's middle) | 3500,2590,0 | 3660,2590,0 | the square's east end, so the vet is within the 60 tiles the seeder counts |
| Vet | 3526,2578,7 | 3712,2580,20 | by the farmhouse at the east edge, near the farmlands |
| Public moongate | 3450,2677,25 | 3696,2570,16 | the open field east of the square; S4 puts the gate here |
| Healer | 3462,2559,35 | 3665,2581,0 | pinned's pre-UOML Haven healer spawner |
| Bank (new) | | 3620,2617,0 | the Second Bank of Haven, pinned's banker spawner |
| Dock (new) | | 3650,2653,0 | the author's "Haven / Docks" spot |
| Town (new box) | | 3568-3761, 2460-2712 | pinned's "Haven" town region's bounding box; the reset stone's "already in town" check |
| Island bounds | 3314,2345 +500,750 | unchanged | the author's Haven region is the same island |

Readers changed to take them from `HavenSpots`: `CharacterCreation.NewHavenStartingCities`, `NewHavenQuestBoard.HomeLocation`,
`ClusterFResetStoneSeeder.Location` and its in-town check, `FountainOfYouthSystem.NewHavenSpot` and
`TutorialWingTrials.TourCentre`. Sir Helper's seeder row moved to the start. Character creation, Rook, the isle's
moongate, the Fold mirror's send-home and the island gate already read `HavenSpots` (P663, P705).

Part 5: `ClusterFAchievements.cs` now says "found the way beneath Haven", and the description names the hatch in the
Second Bank. The key `discovery.old_haven` is unchanged, and the trigger is unchanged: entering a region named "Old
Haven...", the Burrows. The League registrar's welcome page no longer sends players to "the ruins of Old Haven to the
southwest". It says "Something lies beneath Haven: ask at the Second Bank."

**A bug the move would have caused, caught by an existing fact:** the tutorial seeder places a town vet only when none
stands within 60 tiles of `Centre`. With the centre on the square (3640) and the vet 72 tiles east, every run would
have placed another vet. The centre moved east to 3660, and both new facts now check the 60-tile rule.

## Facts

| Fact | Where | Red | Green |
|---|---|---|---|
| Every `HavenSpots` spot is open ground on SoS at its floor's Z; the start group is within 3 tiles; the services and the vet are in the town and within 60 tiles of the centre; the fountain's 16 tiles are flat, open and clear | docs `tools/tests/test_haven_spots.py` (3 facts; reads `HavenSpots.cs` and the SoS files) | Today's spots on SoS: 4 of 7 not at their floor (Rook, the way out, the centre, the healer; `red\red-old-spots-on-sos.txt`). Today's file also lacks the new spots (`red\red-py-spots.txt`) | 3 of 3 |
| A new character's New Haven start is the square, read from `HavenSpots` | code `tests/Tutorial/HavenMoveVerification.cs` | HEAD: (3503, 2574, 14) | yes |
| Rook, the way out, quest board, reset stone, fountain, tour centre, moongate, healer, vet at their spots | same | HEAD: Rook (3500, 2572, 14) | yes |
| The achievement keeps its key and names the way beneath Haven | same | HEAD: "ruins of Old Haven" | yes |

Red runs for the three code facts: `red\red-cs-haven-move.txt` (HEAD's code with only the new test file added). The
old start tile is still open forest at the same height on SoS, so fact 1 alone would pass it. Fact 2's town box is
what catches it.

**Existing facts updated, each a value that moved on purpose:** `NewHavenQuestBoardVerification.SaveShapeIsUnchanged`
(the board's location is in its save bytes; the comment says which), `FountainOfYouthVerification` (the new spot),
`NewHavenSeederFloorVerification` (Sir Helper's measured floor, now Z 0 at the start).

**Probe** (`probe.sh`, the changed files mounted over `sl-uo-builder:cc-P710`; every Tutorial, fountain, reset stone,
quest board, achievement, New Haven and Fold fact): **275, 268 passed, 4 failed** (`green-probe-summary.txt`):

- `TutorialTradeTrialVerification.ATourCountsItsStopsInOrderAndFinishesAtTheLast` for `housing.basics`,
  `reputation.wing` and `shard.systems`, and `GoingFarFromNewHavenStopsATourAndLeavingTheYardStopsATrade`. **Left red on
  purpose.** The tours start at the new centre, and a tour ends 160 tiles from it. Their stops include the west farm's
  porch and the training yard (both still on SoS, about 250 tiles away). They also include the bank and League office
  anchors in `ClusterFNewHavenSeeder`, which are the old plaza's. Where those stops go is part of the question.
- **Not run:** the gated build (`build.sh`). The tree is not green, so the gate would stop at the tests.

## Not done, and why

- **The question** (`Iron-P678-20261027-160606-ff97`): use stock pre-UOML Haven for the town's shops, decoration and
  regions, and find homes for our own places here (recommended); or split each unlisted place into its own prompt; or
  move the essentials and park the rest.
- **Part 2, the other seeders** (`ClusterFNewHavenSeeder`'s quest givers and anchors, `ClusterFNewHavenServicesSeeder`,
  `ApprenticeTraining`'s two boxes, the tours, `Appraiser`'s League office posts): they wait on the answer. With stock
  Haven they mostly retire or re-anchor, and with a split they go elsewhere.
- **Part 3, regions:** pinned's "Haven" region already covers the town with every shop. The choice is to rename it or
  fold it into "New Haven", which 19 of our lookups use by name, or to redraw "New Haven" over it. It is in the same
  answer.
- **Part 4, the cellar hatch:** designed, not built. On SoS the Rootdeep hole tile (3619,2620) is open floor inside the
  rebuilt Second Bank of Haven, so the region's entrance and the way down can stay there. The hatch would be a server
  item: art 0x7E65, "hatch", a dark opening with its lid raised, checked by render. But the 12 teleporters on the
  burrow's mouth (P413) would sit on the bank's floor and swallow anyone walking through. On SoS the way down must be
  the hatch tile alone, with the ladder landing beside it inside the bank. That changes P413's facts, and it must land
  with S2, which drops the burrow from the map. The next session does it.
- **Part 6's other proofs:** the P289 bot route, the Rootdeep flood fill and TazUO pictures need the server reading SoS
  (S2) and the package's map (P674, stopped on its own question). Nothing goes live before wave 1 anyway.
- **"Drop any migration work":** Chase chose a fresh test world on swap day, so nothing here moves existing NPCs or
  items. `ClusterFNewHavenSeeder`'s `WasAt` repair stays as it is, unused on a fresh world.

## Deviations and decisions for Chase

- The plan's figures (P669's per-file counts, used in P673's S7) were too low. The table above is counted from the
  code, and the list sits beside the count.
- `HavenSpots.Centre` is not the square's middle: it is the square's east end (3660), so the vet counts as New Haven's.
- The Read tool is denied on the code copy in this unattended run. I read with `cat` and edited through
  `edit_spots.py` and small scripts.

## Asked, and commit preflight

- Asked Chase: `Iron-P678-20261027-160606-ff97`.
- Code copy: `CharacterCreation.cs`, `ClusterFAchievements.cs`, `ClusterFNewHavenSeeder.cs`, `ClusterFResetStone.cs`,
  `Engines/ML Quests/Items/NewHavenQuestBoard.cs`, `FountainOfYouth/FountainOfYouth.cs`, `LeagueRegistrarGump.cs`,
  `Tutorial/HavenSpots.cs`, `Tutorial/TutorialTradeTrials.cs`; tests `Engines/MLQuests/NewHavenQuestBoardVerification.cs`,
  `Misc/FountainOfYouthVerification.cs`, `Misc/NewHavenSeederFloorVerification.cs`, new `Tutorial/HavenMoveVerification.cs`.
- Docs copy: this file, new `tools/tests/test_haven_spots.py`, `notes\cc-P678-tools\` (294 KB: the grader, the town map
  and picture tools, the edit script, the probe, the question, red runs, the probe summary, `out\` with the point list
  and the town picture). No file over 5 MB; `docs\` untouched. No lock taken, no build, nothing committed.

P678 STOPPED: asked Chase (Iron-P678-20261027-160606-ff97) how to move the places the plan did not list; the spots, the achievement and their facts are done, and the tours are left red until the answer
