# cc-P662: the Wakening Isle, map work (P481 F2)

Iron Golem, 2026-10-27. Docs copy `D:\UO\golems\Iron\shard-migration`, code copy `D:\UO\golems\Iron\ShatteredLegacy`,
both on `golem/Iron/P662`. Site A (P673 1.4: x 6594-6865, y 3905-4049), painted on today's stock Trammel ("Tutorial
first", overseer 10-27 06:45). Not committed; nothing deployed or published; no package built; Haven not touched.

## In plain words

- **The Wakening Isle now exists on the map.** It used to be empty black void. The map patch now holds the whole
  island: beach, road, the fenced meadow for the farm, the training yard, the trades square, a stone bank and a stone
  lodge with roofs, the standing stones on their knoll, the north woods, and a dock with a stone landing for the
  moongate.
- **Where you will see it:** nowhere yet. Players get it in the player package, and the test shard gets it in its
  map, once this patch ships. Then P663's tutorial can be set up on the isle with `[ClusterFSeedTutorial`. Until now
  that command refused, because the land was void.
- **A walk check passed:** a script walked from the beach to the moongate under the server's own movement rules, with
  the farm and P663's props in place. Every leg matches the plan, and every spot where P663 puts a person, door or
  prop has room.
- **For you: look at the pictures and say yes or what to change** (`notes\art\wakening-isle\index.html`: top-down,
  every stop, the shore, inside the bank and the lodge). The patch should not go out in a package before your yes.

## What was built

The driver is `notes\cc-P662-tools\build_isle.py`. It takes `--fresh`, `--plan-only`, `--base <pristine folder>`
(stock now, the SoS file after P675) and `--ship`, and gives each stage its own seeded random stream
(`Random(seed ^ crc32(stage))`). It imports P481's plan from `newisle.py` (the stops, the road, the zones, the
island's shape) and adds one constant shift, (+424, +1992). The look lives in `isle-sets.json`. Every id in it was
measured on stock Trammel by the survey scripts beside it, or picked from a candidates sheet (`candidates.py`).

| Part | What, and where its rule came from |
|---|---|
| Sea | Over the whole drawn area, Z -5 (OSI's sea). 39,440 land cells, every one void before. |
| Shore | `survey_shore.py` / `survey_corners.py` over stock Trammel's mainland: **OSI puts plain sand straight against the sea**, with no land transition tile. The smooth waterline comes from the static water 0x1797 laid on the first ring of *sand*, which dips to -7 under it (1,736 such pieces on OSI's coasts; `osi-beach.png` in the session). Here: first ring -7 under 0x1797 at -5, then -3, -1, 0. Sand to grass: the 12 stock tiles 0x0033-0x003E, one per corner pattern (each measured at 46-78 percent of its uses). |
| Road | Dirt 0x0071-0x0074, 3 wide along P481's line, with the stock dirt-to-grass tiles 0x0079-0x008C by corner pattern (`survey_pairs.py`). 0x0079 is too rare for the survey (under 5 uses), so I confirmed it by render: each of 0x0079-0x007C has its grass at the corner measured for its siblings. On the beach the path stays sand (dirt is kept 2+ tiles from the sand, so no tile has three terrains). |
| Square, landing | Stone paving 0x0442-0x0445 with a hard edge against grass, as OSI's paving does (survey: almost no transition tiles there). |
| Meadow, yard | Flat Z 0. The meadow is fenced with the farm's own fence set (0x0835 post, 0x0836 east-west, 0x0837 north-south), open where the road runs beside it and at the farm's gate. Runs the road cut to under 3 tiles are dropped. The yard is packed dirt, fenced, with a 3-tile gate on the road side. It has two training dummies of each facing, an archery butte, and an east-west ankh (0x0004 + 0x0005, laid as OSI's four are). |
| Bank, lodge | Stone walls by the run rule. **Measured on OSI with `walls.wall_role`: 0x001A is the corner (69 of 74), 0x001B north-south (761 of 782), 0x001C east-west (779 of 813), 0x001D the post (55 of 60).** P481's sketch had east-west and corner swapped. Floors: the bank in cobblestones 0x0515-0x0518, the lodge in boards 0x04A9-0x04AF. Doors are passages, OSI's rule for stone town buildings (`survey_doors.py`): the floor static on the door tile, the run piece either side. The door itself is P663's server item, at its spot. Roof: grey slate 0x049C at +20 over the visible room, the most common piece OSI puts on this wall set (3,608 tiles). I also built and drew a pitched shingle roof (0x05D0/0x05CE/0x05CF); its gable ends showed open, so I left it out. Corners: all 8 inner corners dressed (playbook 2.2): a wall torch on the north wall (NW) and the west wall (SW) at +13, a stool, and crates, barrels and kegs on the visible strip. |
| Knoll, stones | The knoll rises to Z 8 (P481's profile), tapered to 0 two tiles from the sand. Nine tall boulders (0x1350, 0x135D, 0x134F) stand in P481's ring with a gap to the south. From the candidates sheet: P481's rock 0x1772 reads as pebbles. |
| Dock | Planks 0x07C9/0x07CD at Z -3 (OSI: 1,325 planks over the sea at -3). Rope rails 0x03A6 along x and 0x03A9 along y at +5, and stacked pier posts at the shore end, all laid as OSI's dock at 496,768. The planks also cover the wet first ring of sand, as OSI's docks do. |
| Woods | The two north lobes: 7.0 pieces per 100 tiles (oak, walnut, cedar pairs, ferns), inside the 5 to 12 asked. The rest is light: beach 2.7 (seaweed, small rocks), open grass 1.6, meadow 0.8 (flowers). None of the decor blocks a spot or the road. |
| Kept clear | Every spot P663 places something on, read from its code (TutorialWorld, TutorialCorePlacement, TutorialFarm, TutorialIsleFarmLayout), stays free of our statics; decor also stays off their neighbours. The driver reads those files from the code copy, falling back to `golem/Iron/P663` until that merges. |

**Statics:** 1,647, in 161 blocks (`statics-placed.csv`). Walls 70, floors 128, roofs 160, fences 167, shore water
791, dock and landing 81, stones 9, yard and square 13, decor and corner dressing 228. No land tile is impassable
except the sea.

## The walkable gate (pinned movement, on the written files)

`build_isle.Walker` copies pinned `Movement.cs` (CheckMovement, Check, GetStartZ, IsOk), `Map.GetAverageZ` and
`Map.CanFit`, reduced to the map files plus P663's server items: the farm's 330 pieces and the six props. It walks
as a player: 8 directions, a diagonal only when both orthogonal steps are open, doors open. It runs on the files
after they are written and re-read.

| Leg | To | Walked | P481 11.2 sketch |
|---|---|---|---|
| 0 to 1 | walking tiles | 8 | 8 |
| 1 to 2 | camp: backpack | 10 | 10 |
| 2 to 3 | rack: paperdoll | 9 | 9 |
| 3 to 4 | signpost: chat | 27 | 27 |
| 4 to 5 | farm gate: Wren, Tobin | 28 | 28 |
| 5 to 6 | yard: echo, Sera | 23 | 23 |
| 6 to 7 | bank: Merrin | 27 | 27 |
| 7 to 8 | lodge: Elara | 20 | 20 |
| 8 to 9 | stones: the vision | 12 | 12 |
| 9 to 10 | moongate to New Haven | 37 | 37 |
| **beach to moongate** | | **201** | **201** |
| bank: stop 7 to Merrin (through the door) | | 5 | |
| lodge: stop 8 to Elara (through the door) | | 5 | |
| yard: stop 6 to the echo, the echo to Sera | | 3, 4 | |
| farm: stop 5 to Wren, Wren to the pests | | 1, 12 | |
| dock end to the moongate | | 1 | |

Every leg equals the sketch because the ground between stops is open, so each leg is its straight 8-way distance.
That fact matters: the built map adds no detour. **All 25 spots P663's seeder fit-checks pass `CanFit` at their
ground** (Map.CanFit(p, 16) at the land's average Z, as `TutorialWorld.Ground`). 8,132 walkable tiles are recorded in
`plan-cells.json`; a later build of this layout must match them.

## The playbook's checklist (`checklist_isle.py`)

| Check | Result | Detail |
|---|---|---|
| 1 walls against a test room | PASS | 5 x 5 room in the stone set: corners post / ew / ns / corner, runs single pieces |
|   fence set (no corner piece) | PASS | its south-east corners carry both runs, by walls.wall_pieces; the farm addon lays them the same way |
| 2 no diagonal runs | PASS | 236 wall tiles, none joined only diagonally |
| 3 rows straight | PASS | no furniture rows (furniture is server items) |
| 4 inner corners dressed | PASS | 8 inner corners, every one dressed |
| 4 doorways framed or passages | PASS | 2 doors: passages, OSI's stone town rule; the yard gate a 3-tile gap |
| 5 variety | PASS | 43 distinct decor ids, 14 categories, 0 identical pieces side by side |
| 6 transitions | PASS | slope audit: no tile over the limit |
|   vseUOAware diagnose | PASS | west shore 6624-6633 x 3994-3999 on the written files: sea -5, wet sand -7, sand -3, stock 0x0033/0x0036/0x0037/0x003C/0x003E, grass 0; no step over 4. Second reader: `inspect_map_coordinate` 6832,3991 = 0x0444 at Z -2, no statics, as mine |
| 7 one wall piece per tile | PASS | every stone wall tile one piece |
| 8 walkable gate, files re-read | PASS | 17 legs and detours, 25 of 25 spots fit; re-read: 0 land mismatches, statics equal (1,647) |
| 9 junctions by the run rule | PASS | 236 wall tiles carry the run-topology piece |
| 10 torches mounted | PASS | 4 wall torches before a north or west wall, +13 |
| 11 frames touch | PASS | no framed openings |
| 12 junction sheet | PASS | 27 crops (`junctions-1.png`): 15 L, 8 ends, 4 mounts |

**The junction sheet, checked crop by crop.** In round 1 the yard's south-east fence corner stood in the sea. The
yard (and the square) had been stamped onto the plan's rectangles where the sketch's shape had water. Fixed: the shape
keeps dry land under the yard, square, bank and lodge, with a 4-tile margin. In round 2 all 27 crops looked right.

**Render rounds** (each fault was fixed by a rule in the driver, not by patching a tile):
1. The sketch's land ran under its own dock to x 6409, so there were no planks. The route's points east of x 6384 no
   longer shape the land.
2. The road came out as a broken line of dirt blotches, and the deck's end posts doubled the landing's. The waterline
   was a flat stair-step: I moved the static water onto the first sand ring (OSI's way).
3. A wider road brush made the road 5 wide; unbounded road growth wandered into the meadow; the meadow fence left
   stubs; the knoll's rise met the beach dip and left a black wedge. Fixed with the 3 x 3 brush, growth limited to 1
   tile, runs under 3 dropped, the knoll tapered.
4. The real cause of the blotches was the one dirt pattern missing from the survey. I added 0x0079 after checking it
   by render.

## The patch

`mapops.py diff`, pristine stock Trammel (hashes as `ORIGINAL-SHA256.txt`, the same as P167's) against the scratch
build (pristine + the shipped patch less anything in the isle's area + the isle) gives
`player-package\vendor\shattered-legacy-map\trammel.mapops` in the code copy.

- **Size: 253,167 to 1,037,429 bytes (+784,262).** That is 41,753 lines added: 39,440 L, 1,647 S+ and 665 B lines,
  plus the F line's new count (214 to 879 blocks). The file is under the 5 MB rule. P481 11.3 estimated 0.8 to 0.9 MB.
- `mapops.check`: drifted 0, missing 0, land identical, 0 blocks differing.
- **The player's applier**, run on the real vanilla files (`Build-MapOverride`): 50,760 cells, 3,292 pieces added, 7
  removed. Its map and index are byte-identical to the scratch build, and `statics1.mul` matches block by block
  (`mapops.compare`: land identical, 0 blocks differing; the applier appends blocks at the end, so the file's bytes
  differ by design).
- The package's map gate (`Test-MapOps`, run on the vendored file without building a package): 0 failures.
- `player-package\tests\Map-Overrides.Tests.ps1`, under the `package` lock (taken and released): 7 facts, 0 failed.
- `tools\tests\test_mapops.py` (with `SL_SHARD_REPO` set to my code copy and `MAPBUILD_CLIENT` set to the vanilla
  folder):
  - Facts 1, 2, 3, 4, 6, 7 pass.
  - **Fact 4** now allows the isle's drawn area. It failed first on the new patch: "(6594, 3905)" outside the Burrows.
  - **Fact 7 is new:** every cell of the drawn area is an L line; its tiles and heights are `land-summary.csv`; its
    S+ lines are exactly `statics-placed.csv`; it removes nothing of EA's; and the moongate stands on land with
    nothing on it. It failed first on HEAD's patch: "39440 != 0 : every cell of the drawn area".
  - **Fact 5** leaves the isle out (`without_isle`; P167's scratch never had it). It still fails on this PC on exactly
    the two blocks it already failed on before this prompt (231751, 332429; P413's notes: the scratch build here
    predates P188's way in). Nothing new fails.

## Decisions and deviations

- **A stone landing at the dock's end** (x 6829-6833, y 3989-3993, paving at Z -2, rails and corner posts). P663's
  seeder places and fit-checks the moongate and the dock-end marker at `TutorialWorld.Ground`, which is the *land's*
  average Z. Over open sea that is -5, under the planks, and pinned `CanFit` would refuse forever (no surface at that
  Z, and a plank overhead). On the landing both spots stand on land at the deck's height. P663's code needs no change.
- **The east shore was pulled in** (the route's points east of x 6384 no longer shape the land), so the dock runs over
  real sea; the sketch's land reached x 6409 under its dock. The yard, square, bank and lodge keep dry land under them
  with a 4-tile margin. The walked legs are unchanged.
- **Flat slate roofs, not pitched.** OSI's own commonest top for this wall set. A pitched roof needs gable pieces for
  this set that I could not lay as OSI does in the time. Pitched roofs can come later if Chase wants them.
- **The sketch's art fixes:** the wall roles (above); 0x04A9 and 0x04A1 are floor statics, not land tiles (the
  sketch used them as land); the standing stones; the dock pieces (OSI's measured planks, rails and pier posts in
  place of 0x04A1 and 0x01CD).
- **The base is selectable:** `--base` takes the SoS folder after P675 (S2). Site A is void in both maps, so only the
  B fingerprints of these lines should change.
- **No CHANGELOG line**, as the prompt says (F3 makes the isle reachable).
- **Not done: `SOURCE.txt`.** I wanted to add a paragraph about the isle to
  `player-package\vendor\shattered-legacy-map\SOURCE.txt` in the code copy. The Read tool on it was denied by the
  unattended run, and I was told not to route around that. Text to add after the P413 paragraph: "cc-P662,
  2026-10-27: the Wakening Isle (site A, x 6594-6865, y 3905-4049; P481 F2, P673 1.4): 39,440 L lines (the whole
  drawn area, void before) and 1,647 S+ lines, built by shard-migration notes/cc-P662-tools/build_isle.py; nothing of
  EA's removed."

## Not verified

- **Nothing on a running shard or in a client.** The test shard's map overlay is built from this file only at the
  next server image build, and the TazUO play-through is P664's (Chase, 10-27). The renders use `isorender` (the
  client's layout). The walk uses pinned's rules on the files, not the server.
- **The farm on flat ground:** the farm pieces are P663's server items, drawn into the meadow render. Its floor
  heights are P663's (kept from New Haven's slope), not checked in a client.
- **Roof hiding:** the client should hide the slate when a player is inside (a tile over their head). This is not
  seen in a client.
- **The SoS base:** only the stock base was built.

## Commit preflight

- Code copy: one file changed, `player-package/vendor/shattered-legacy-map/trammel.mapops`.
- Docs copy: `tools/tests/test_mapops.py`; new `notes/cc-P662-tools/` (the driver, the look file, the survey,
  candidate, checklist and render scripts, and the build's records: `statics-placed.csv`, `land-summary.csv`,
  `plan-cells.json`, `walk-report.json`, `build-report.json`, two survey JSONs; 404 KB); new
  `notes/art/wakening-isle/` (13 PNGs and `index.html`, 5.6 MB in all, none over 5 MB); this file.
- The scratch maps (`D:\UO\golems\Iron\p662-work`, 112 MB) are outside both repos.
- Locks: `package` taken for the package tests and released. No Docker build, no test shard. Nothing committed (the
  Golem commits). No question asked of Chase.

P662 DONE
