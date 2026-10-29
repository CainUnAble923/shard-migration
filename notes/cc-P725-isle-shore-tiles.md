# cc-P725: shore tiles and tropical plants for Tutorial Island

Iron Golem, 2026-10-29. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P725` (main at the P685 merge). Not committed, nothing deployed, no package built, Haven not touched.

## In plain words

- **The Wakening Isle has real beaches now.** Before, the coast was a jagged edge of square sand tiles against the sea.
  Now the sand runs down to the water and the surf breaks along the shore all round, the way stock UO coasts are drawn.
  You can walk the sand right to the water's edge, and not into the sea. Pictures, before and after, from the game
  client: `notes\cc-P725-tools\shots\pair-*.jpg`.
- **The isle is a tropical island.** Palms, banana trees, o'hii trees and big jungle trees, ferns, fan plants and
  grasses, all stock UO art: thick in the middle and the two north hills, thinning toward the beaches, in clumps with
  clearings. The road, every lesson stop, sign, door and person, the wreck, the lighthouse and the beach where you wake
  stay clear. Whole island: `notes\cc-P725-tools\shots\render-whole-before.jpg` and `render-whole-after.jpg`.
- **New art from the downloads:** I picked what is worth adding (beach trees, bamboo, fruit crates, a fire pit,
  fireflies) and drafted the client-package task for it below. Three packs need your call first, because their
  pages say the art was taken from other games.
- **For you:** walk the isle on the next test build and say if the beaches and the planting look right. The map
  reaches the test shard with its next overlay build and players with the next isle release (this goes out in the
  next one, not P722's). Decide on the flagged packs (seagulls, the plant sets) if you want them.

## 1. The shore

**What stock UO does.** P662 measured that OSI puts plain sand against the sea and laid OSI's plain water piece
0x1797 on the first ring of sand. That is only part of the rule, and it drew the sawtooth Chase saw: a whole water
diamond on each first sand tile, stepping along every coast that is not straight in x or y. I counted every water
piece on stock Trammel's mainland (`survey_surf.py`, `surf-survey.json`) and then, cell by cell, what OSI lays beside
its sandy coasts (`survey_beach.py`, `survey_rule.py`, `shore-rule.json`):

| Where the land is, from the sea cell | OSI's piece (count on the mainland) |
|---|---|
| north | surf-edged 0x179F / 0x17A0 (4,626 and 4,439 with that pattern) |
| west | surf-edged 0x17A3 / 0x17A4 (5,581 and 5,830) |
| north and west | the corner 0x17A6 / 0x17AF (1,811 and 1,836) |
| only one diagonal | the corner diamonds 0x17A9 (NE), 0x17AB (SW), 0x17AC (NW) |
| east only (the side the camera faces) | half-tile surf 0x179D / 0x179E over land (857 of 1,032 and 885 of 1,056) |
| south only | half-tile surf 0x17A1 / 0x17A2 over land (814 of 960 and 810 of 942) |
| east and south | 0x17A7 (1,455 of 1,581) |
| the last sand tile, land south or east of the water | small surf pieces 0x17A5, 0x17A8, 0x17AD, 0x17AE, 0x17B0, 0x17B2 |

**The rule in the driver** (`build_isle.py`, stage 8, and `isle-sets.json` `shoreFront`, `shoreFallback`):

1. Sea cells with land only east and/or south (the front coasts): OSI's half-tile surf piece over impassable sand
   0x001A at the sea's -5. The sand fills the notch and the surf runs along it. This is what removes most of the
   teeth on the north and north-west sides of the isle.
2. Every other cell beside the line takes OSI's piece for its 8-neighbour pattern from `shore-rule.json` (learned on
   stock sandy coasts whose land lies within 6 of the sea, so not OSI's sand cliffs). A cell takes any composition
   OSI uses at least a quarter as often as its commonest one, so 0x179F and 0x17A0 alternate as on OSI's coasts.
   A filled notch counts as land for its neighbours.
3. A sea cell whose pattern OSI's beaches show fewer than 20 times falls back to the surf edge for the side its land
   is on (north, west, or the north-west corner).
4. The first ring of sand now stands at -4 (was -7 under P662's water diamond), then -3, -1, 0. The dock rows keep
   P720's -3 (the dock step gate still passes: 0, -1, -3, -3, planks -2).

Counts on this build: 249 front notches filled (70 east, 126 south, 53 both), 706 sea cells with OSI's table piece,
107 by the fallback, 112 last-sand tiles with a small surf piece; 1,174 shore pieces in all (P662 had 791 plain
diamonds). The wake-up beach is as wide as before (the sand rim is unchanged) and one tile wider to walk.

## 2. The tropical planting

Every id is stock art OSI plants on Buccaneer's Den's island, counted there (`survey_tropics.py`,
`tropics-bucs.txt`): ferns 0x0C9F-0x0CA4 (2,704), small palms 0x0C99-0x0C9D (929), the jungle trees (0x0D41-0x0D93),
fan plant 0x0C98 (136), o'hii 0x0C9E (125), elephant ear 0x0C97 (109), blade plant 0x0C93 (107), pampas 0x0CC4 (88);
plus coconut and date palms 0x0C95/0x0C96, banana trees 0x0CA8/0x0CAA/0x0CAB, ponytail palm 0x0CA6, snake plant
0x0CA9 and grasses.

OSI's jungle trees are several tiles each: a trunk run up the north-east diagonal with leaf layers.
`survey_jungle_trees.py` lifted the two commonest whole compositions of each of the four families from Buccaneer's
Den (`jungle-trees.json`; for example 47 of the 140 0x0D41 trees are exactly D45, D46, D41+D47, D42+D48, D43+D49,
D44+D4A, D4B along the diagonal), and the isle lays them whole, as OSI does.

Placement (`isle-sets.json` `tropics`, `build_isle.py` stage 8):
- **Tiers by distance from the sand:** beach (sand at least 3 from the sea: sparse coconut, date and small palms),
  edge (to 3 tiles in: palms, pampas, ferns), middle (to 7: banana, o'hii, palms, ferns, fan and elephant-ear plants),
  deep (OSI's jungle trees, banana, o'hii, dense ferns).
- **Clusters, not a grid:** a tile's chance is its tier's share times a seeded field of round clumps (one per 28 land
  tiles, radius 2.5-5.5), so there are thickets and clearings.
- **Kept clear:** trees stay 3 tiles from the road, every stop, server item (NPCs, signs, doors, props, the farm) and
  P724's wreck and lighthouse, and 4 tiles round the buildings, yard, square and meadow. Undergrowth keeps P662's
  margins (2 from the road, 1 round every spot, off the server items). Nothing grows within 4 of the wake-up spot
  and no tree within 8. The farm meadow keeps its flowers only.
- **Counts:** 8 jungle trees, 210 single trees (21 beach, 106 edge, 68 middle, 15 deep), 650 undergrowth pieces.
  Density in the north woods 33.5 pieces per 100 tiles (was 7.0), the open grass 13.1 (was 1.6), the beach 4.6
  (was 2.7).
  P662's oaks, walnuts and cedars are gone from the isle.

**P724's addons.** P724 (merged before this) placed a shipwreck on the wake-up beach's west tip, a lighthouse north of
the dock and a fountain on the bank's square, as server items. The driver now reads their tiles from
`TutorialIsleAddons.cs` (the pieces tables) and keeps every plant off them and trees 3 away. The wreck lies in the
surf, so OSI's water pieces may lie under it (the plan check allows exactly that).

## Facing

Nothing placed here has a facing to choose: the water pieces are chosen by the coast's side (the table above), the
palms and plants are single pieces drawn the same from every side, and OSI's jungle trees only come in their one
north-east diagonal. **No piece was turned.** Checked from the default camera in every after shot. The buildings,
doors, signs, wreck, lighthouse and moongate frame are untouched (P720's and P724's).

## Tests

**Map facts** (`tools\tests\test_mapops.py`, `SL_SHARD_REPO` = the code copy, `MAPBUILD_CLIENT` = the vanilla
folder): **11 of 11 pass** (`cc-P725-tools\green-test-mapops.txt`). Fact 7 checks the shipped isle equals this build's
`statics-placed.csv` and `land-summary.csv`.

**New: fact 11** `test_11_the_isle_has_osis_surf_and_tropical_plants`: no plain water diamond on walkable sand; over
500 surf pieces; every sea tile with the island to its north (and sea east and south) carries a surf-edged piece; over
100 palms, banana and o'hii trees; over 40 jungle-tree pieces. **Seen failing first** on main's patch
(`red-fact-11.txt`: "a plain water diamond on walkable sand", 791 tiles), then on my first build of this branch (11
north-coast sea tiles without surf, the notch patterns OSI rarely shows; that is what the fallback in rule 3 fixed),
then passing.

**The walk** (P662's gate, pinned ModernUO movement on the written files, the server items, the farm and P724's
wreck and lighthouse in place): every leg as before, beach to moongate 201 steps; every detour as before; 25 of 25
seeder spots fit; the dock steps at most 2. `walk_check.py` (`walk-check.txt`) against P720's walkable tiles: 583 new
(the first sand ring, which P662's water diamond had made impassable), 260 lost (the new trees and pampas, and the wreck
and lighthouse the gate now knows about), **no sea tile walkable** except the 21 dock planks. `plan-cells.json` was
regenerated (8,494 walkable tiles).

**P662's playbook checklist** (`checklist.txt`): every check PASS. I replaced its fixed "vseUOAware diagnose" line, a
one-off reading from P662 that still said "wet sand -7" after the shore changed, with a reading of the written files:
west shore heights -5, -4, -3, -1, 0, largest step between neighbours 3.

**Both bases.** Built on the SoS copy (main's base, `p720-work\sos-base`, shipped) and on stock Trammel with the
release branch's patch (`SL_CODE` = `D:\UO\golems\Iron\release-isle-20261028`, `--base` the vanilla folder): the isle's
42,462 lines are **identical** (`both-bases.txt`); only the B fingerprints differ, as P662 expected (site A is void in
both). The stock-base patch is kept at `cc-P725-tools\trammel-stock-base.mapops` for the next isle release. Outside the
isle, the shipped patch's lines are byte-identical to main's (`patch-outside-isle.txt`).

**Package map facts** (`player-package\tests\Map-Overrides.Tests.ps1`, `package` lock taken and released): 16 facts,
0 failed (`green-ps-map-overrides.txt`).

**No Docker gated build.** No server code changed: the map patch is data the package and the test shard's overlay
read, not part of the image. The private shard ran main's image (`sl-modernuo:cc-P685`, tagged `sl-modernuo:cc-P725`,
the same image id 7c8065ae9e98).

## Live, in TazUO (private shard 127.0.0.1:2596, `test-shard` lock)

`proof-shard.ps1` (P722's, its own container `sl-p725-proof`) on a copy of the bot world, the map overlay built by the
test shard's own `Build-MapOverlay.ps1` on the SoS base (`overlay.ps1`), once from main's patch (before) and once
from this branch's (after). The client is our TazUO with the map built from the same patch the way the package does
(`isle-shots.ps1`, P720's). Nine stretches, each shot before and after from the same spot (`shots.json`, standing
spots picked on flat walkable grass by `shot-spots.json`): the wake-up beach, the north, north-west, west, south,
south-west and east coasts, the dock and landing, and the jungle. Pairs in `cc-P725-tools\shots\`. The first shot of
each run still has the login windows open, so the wake-up beach was shot again at the end (`pair-wake-again.jpg`).

What the shots show: surf along the west and north-west coasts where there was a hard diamond edge; on the north
coasts the teeth are filled and much smaller (a fine edge stays, as on OSI's own coasts of this side); the wreck sits
in the surf; palms and jungle inland, the road and Tamsin's spot clear.

**Bot route: 0 failed checks, 85 passed** (`runs\run2\playlog.txt`, 192 s; the isle in 166 s). It is main's route,
P732's `isle.py` unchanged, on a fresh copy of the bot world with this branch's overlay: a fresh character woke on
cold sand at 6638,3993, got up on its first move, took every lesson (the farm with its pet and pests, healing Pip,
the yard's death, the bank, the lodge, the vision) walking the bot's own paths over the new map, and the moongate put
it beside Rook at 3632,2584; the New Haven pick started on the plaza. Run 1 (`runs\run1`) used P722's older route by
mistake (`isle-p722-stale.py`): it failed 4 checks, all at steps main has changed since (P732's wake lines, P724's
cloak chest) and none about the map; it is kept for the record. The shard is down and the `test-shard` lock released.

## 3. Art on disk to consider (not added: new art needs new item ids in the client)

Read from each pack's `SOURCE.txt` in `D:\UO\third-party` (read only) and looked at on contact sheets
(`packsheet.py`).

| Pack | Worth it? | What | Credit and terms (SOURCE.txt) |
|---|---|---|---|
| `beach-trees` (ParanoiaPhD, 4 BMP) | **Yes** | `beechtree1.bmp`/`beechtree2.bmp` (a wide shade tree, mirrored pair) and `beachtree3.bmp`/`beechtree4.bmp` (smaller, mirrored): broad shade trees for the beach tier among the palms. Not palms. The author says they may need cleanup. | No terms stated; credit ParanoiaPhD; ship only in the package, do not repost. |
| `bamboo` (Thagoras, 31 BMP) | **Yes** | Clumps `Bamboo 01`-`10` (thickets for the jungle's edge), small `11`-`16`, and the tall stem and foliage pairs `20a/b`-`25a/b` (stem plus leaves, as OSI's trees). | No terms stated; credit Thagoras; package only; "register in the art registry before use". |
| `laoth-wooden-crates` (Laoth, 20 BMP) | **Yes, for the farm** | Fruit and vegetable crates (bananas `crate (19)`/`(20)`, oranges `(1)`/`(2)`, grapes `(3)`/`(4)`, melons `(5)`/`(6)`, tomatoes `(7)`/`(8)`, greens `(9)`/`(10)`, fish `(11)`/`(12)`) and empty crates `(13)`-`(18)`: by Wren's farmhouse and the trades square. | No terms stated; credit Laoth; package only. |
| `mrriots-firepit` (MrRiots, 8 BMP) | **Yes** | The new fire pit (`NewFirepit.bmp`, frames `1`-`7`) for the camp stop (stop 2). | "Use and edit as you wish." Credit MrRiots; package only, do not repost the raw files. |
| `fireflies` (Ems, 5 BMP) | **Yes, small** | Animated fireflies (`Item 0x357F`-`0x3583`, the author's slots: renumber) over the meadow and woods at night. | No terms stated; original art; credit Ems; renumber to our free ids. |
| `african-trees` (Thagoras, 51 BMP) | Maybe, a few | Savanna trees, not tropical. Only the aloe (`Aloe a/b`) and lovegrass (`Lovegrass a1-a3, b1-b2`) suit the beach edge. | "Feel free to modify for your own purposes." Credit Thagoras; package only. |
| `kevsurcu-big-trees` (Kevsurcu, 27 tiles) | No | Three big temperate trees cut into tiles: a landmark tree would fight the jungle look. | No terms stated; credit Kevsurcu. |
| `new-tree-art` (manofwar, 48 BMP) | No | Very large temperate trees (264 x 497 at full size), partly from uo-pixel.de; see-through untested; not tropical. | No terms stated; credit manofwar and uo-pixel.de. |
| `tall-trees` (Zigholtul, 97 BMP) | No | Replacements for stock tree ids; the isle no longer uses the stock temperate trees, and Chase's rule is not to overwrite stock art blindly. | No terms stated; credit Zigholtul. |
| `osi-plants` (82) and `plants-set-2` (100), Thagoras | **Chase's call** | Flowers and blooming plants (bluebell, daisy, buttercup, fireweed...). | **Flagged:** the author says they come from another, abandoned game; SOURCE.txt says to treat as EA-owned art and not use without Chase's call. |
| `seagulls` (Vrark, 5 .vd, 4 .wav, 1 .cs) | **Chase's call** | The best fit for the beaches: flying gulls with sounds and a spawner script. | **Flagged:** "IE" in the file names points to Infinity Engine sprites; the sound source is not stated. |
| `butterflies` (Vrark) | No | | **Flagged:** "Legend of Zhao Yun" sprites, ripped from another game. |
| `sea-creatures` (Vert-I-Go, 5 .vd) | Not for the isle | Seahorse, whale shark and sharks: nobody swims on the isle; keep for a sea area. | No terms stated; credit Vert-I-Go. |
| `farm-carts` (6 images) | **Not until sourced** | Farm carts for the farm. | **No `SOURCE.txt`** in the folder (only `existing-slots.png`, `sheet.png`, four TIFFs): the author and terms are unknown, so it cannot be credited yet. |

Queued downloads that would fit later (not on disk yet, so not checked): Shipwrecks Q#889 is already on the isle as
P724's wreck (Celestial's, from `D:\UO\third-party\code`); New Lighthouse Q#929 likewise (Milva's, P724); DockAddon
Q#930, Sparring Dummy Q#911 and the training hall Q#858 are for a later task.

### Draft follow-up prompt (client package)

> **CC task P7xx: tropical art for Tutorial Island (client package).** Chase 10-28 asked for a tropical isle; P725
> planted it with stock art and picked these downloads to add. Add them as **new item ids** (never over stock art):
> PNGs in `player-package\vendor\shattered-legacy-art\art\<id>.png`, one row each in `registry.csv` and its record in
> `records.json` (flags and height after the stock piece named here), credits in the package README's art credits.
> 1. ParanoiaPhD's beach trees (`D:\UO\third-party\beach-trees`, 4 BMP: two mirrored pairs): tiledata after OSI's
>    tree 0x0CCA (Impassable, Foliage on the leaves). Check the black background keys out cleanly; the author says
>    they may need cleanup.
> 2. Thagoras' bamboo (`bamboo\Bamboo Update`, 31 BMP): clumps 01-10 and 11-16 as single pieces after OSI's fern
>    0x0CA1 (passable) or o'hii 0x0C9E (impassable) by size; the tall pairs 20a/b-25a/b as stem plus foliage, after
>    OSI's tree and leaves pairs.
> 3. Laoth's crates (`laoth-wooden-crates`, 20 BMP) after OSI's crate 0x0E3D (Impassable, Container off: decor).
> 4. MrRiots' fire pit (`mrriots-firepit`, 8 BMP) as an animated item after OSI's campfire 0x0DE3 (animdata frames).
> 5. Ems' fireflies (`fireflies`, 5 BMP, the author's slots 0x357F-0x3583: renumber) as one animated piece.
> Then, in shard-migration `notes\cc-P662-tools\isle-sets.json` `tropics`, add the beach trees to the beach and edge
> tiers and the bamboo clumps to the middle and deep tiers, the crates beside Wren's farmhouse and the square, the fire
> pit at the camp (TutorialWorld.Camp, off its spot), and rebuild with `build_isle.py --fresh --base <SoS copy>
> --ship`; P725's fact 11 and fact 7 must stay green, and the walk legs unchanged. Package tests under the `package`
> lock; shots of each new piece in TazUO on a private shard. Do not use `osi-plants`, `plants-set-2`, `seagulls` or
> `butterflies` unless Chase has said yes (their SOURCE.txt flags them as art from other games), nor `farm-carts`
> until it has a SOURCE.txt.

## Decisions and deviations

- **The shore rule is learned, not hand-picked.** Where the brief says "the same transition rules stock coasts use",
  the driver reads them from `shore-rule.json` (made by `survey_rule.py` from stock Trammel), plus two small explicit
  tables in `isle-sets.json` with their stock counts: the front-coast half-tiles and the fallback. P662's survey looked
  only at sand touching sea land tiles; OSI's sandy coasts are mostly drawn with water pieces over impassable sand
  and sea-floor land at -15, which that survey never saw.
- **The sea floor stays sea land at -5**, not OSI's sand at -15 under the water: at -15 every coast becomes a cliff
  (as on stock Trammel's beaches round Moonglow), which is the opposite of a gentle beach. The edge pieces are drawn
  on the sea at -5 as OSI draws them.
- **Front coasts keep a fine edge.** On the north and north-west coasts (the sea behind the land from the camera)
  OSI's own coasts show small steps too; the half-tile surf fills each notch, so the steps are a quarter of their old
  size, but not gone. Hiding them fully would need new art.
- **P662's driver was changed in place** (`notes\cc-P662-tools\build_isle.py`, `isle-sets.json`, `checklist_isle.py`),
  as P720 did, because it is the isle's one source and fact 7 reads its outputs. Its records were regenerated
  (`statics-placed.csv`, `land-summary.csv`, `plan-cells.json`, `walk-report.json`, `build-report.json`), and
  `shore-rule.json` was added beside it.
- **The temperate woods are gone.** `isle-sets.json` keeps P662's `woods` block marked superseded, for the record.
- **CHANGELOG** `2026.10.29` (main is at `2026.10.28.12`), two Changed lines; `VERSION` bumped. If another branch
  merges a `2026.10.29` first, this section takes the next number.

## Not done

- **Nothing deployed** and no package built. The test shard gets the isle's new map with its next overlay build;
  players with the next isle release.
- **No new art added** (by the brief): the client-package prompt above is a draft for the overseer.

## Files

- Code copy: `player-package/vendor/shattered-legacy-map/trammel.mapops` and `SOURCE.txt`; `CHANGELOG.md`, `VERSION`.
- This repo: this file; `tools/tests/test_mapops.py` (fact 11); `notes/cc-P662-tools/` (the driver, the look, the
  checklist, `shore-rule.json` and the regenerated records); `notes/cc-P725-tools/` (the surveys and their outputs,
  the walk check, the render, shot and shard scripts, the bot routes (`isle.py`, P732's, and the stale
  `isle-p722-stale.py`) and their runs, the red and green outputs, the stock-base patch, the shots).
- Outside both repos: `D:\UO\golems\Iron\p725-work` (the SoS scratch build), `p725-work-stock` (the stock one) and
  `p725-proof` (overlays, the shard copies, every raw shot and the shard logs).

## Commit preflight

- Code copy (`git status`): 4 files changed: `player-package/vendor/shattered-legacy-map/trammel.mapops` (1,066,673
  bytes), its `SOURCE.txt`, `CHANGELOG.md`, `VERSION`. Nothing else.
- Docs copy: `tools/tests/test_mapops.py`; `notes/cc-P662-tools/` (8 changed, `shore-rule.json` new); new
  `notes/cc-P725-tools/` (5.9 MB in all, the largest file the stock-base patch at 1.1 MB; none over 5 MB); this file.
- Locks: `package` (twice) and `test-shard` taken and released; no `docker-build` (no image built: `cc-P725` is a tag
  of main's `cc-P685` image). The private shard `sl-p725-proof` is removed and no TazUO is left running.
- Nothing committed, merged or pushed; no question asked of Chase.

P725 DONE
