# cc-P679: moongates, teleporters and the staff go-menu on the new land (SoS swap S4)

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P679`. Not committed, nothing deployed, Haven not touched. The map was read through the server's
overlay (P728's build of `Build-MapOverlay.ps1`, copied to `D:\UO\golems\Iron\p679-work\overlay`; its stamp's patch hash
equals this branch's `trammel.mapops`). Map by **Zigholtul** (Siege of Sosaria Trammel Map 3.0); the go-menu is his.

## In plain words

- **The public moongates stand in the author's stone circles.** On the new map each town's circle is where it was,
  just higher or lower, so the gates stay put and move up or down to its floor (Britain's is the rock ring round a
  tree; Bucs' Den's stays on its jungle path). New Haven's gate is in the author's Haven town, east of the square.
  There are pictures of every gate in our game client in `notes\art\sos-s4-gates\shots\`.
- **The dungeon entrances work on the new map.** Of the 863 stock teleporters on Trammel and Felucca, 817 are kept, 48
  ends moved onto a floor (Deceit's cave mouth moved one step out, for example) and 46 are left out, each with a reason:
  Blackthorn's way in (Blackthorn is off until it moves), Bucs' Den's ladders whose upper rooms are gone, a cave near
  Haven the author filled with rock, and links to Felucca-only land that no longer exists. A test character walked into
  all 16 dungeon entrances the author rebuilt, and arrived inside each one.
- **Staff get the author's own go-menu**: his 410 places (towns, dungeons, his new keeps and islands) on both Trammel
  and Felucca.
- **For you: nothing to do now.** It goes live with the rest of the swap. Worth knowing (end of this note): the
  author's three extra gate spots have no gate art, so there is nothing to keep as decoration; Felucca gets the same
  go-menu as Trammel; and Felucca's own way to Ter Mur is gone with its old land (Trammel's remains).

## What changed, by the prompt's parts

### 1. The public moongates (`server/patches/PublicMoongate-sos-gates.patch`)

Every gate was looked at in a render (`notes\cc-P679-tools\art\before-*.png`) and a tile grid (`grid.py`). The author
kept a stone circle at each town gate, centred on the stock tile at a new height. So each gate keeps its x, y and takes
the circle's floor Z (pinned's `GetAverageZ` there, which is where a walker stands):

| Gate | Stock | Now | Note |
|---|---|---|---|
| Moonglow | 4467,1283,5 | 4467,1283,**23** | standing stones at 4 to 5 tiles round it, on a mound |
| Britain | 1336,1997,5 | 1336,1997,**15** | the rock ring round a tree (the brief's "author's ring") |
| Jhelom | 1499,3771,5 | unchanged | |
| Yew | 771,752,5 | 771,752,**15** | standing stones |
| Minoc | 2701,692,5 | 2701,692,**20** | standing stones |
| Trinsic | 1828,2948,-20 | 1828,2948,**-16** | standing stones |
| Skara Brae | 643,2067,5 | unchanged | |
| Magincia | 3563,2139, map's Z | unchanged | pinned already reads its Z off the map (34 on SoS) |
| New Haven (Trammel) | 3450,2677,25 | **HavenSpots.PublicMoongate** (3696,2570,14) | S7's town (P678 chose the spot); PMList now reads it from there |
| Buccaneer's Den (Felucca) | 2711,2234,0 | unchanged | the jungle path the author drew; no circle there |

Felucca's list carries the same eight shared gates. `HavenSpots.cs`'s comment now says PMList reads it.

### 2. The author's own gate spots

His go-menu names gates at Hammerhill 1541,1081, Kameron Kove 1353,2451 and Dragonstorm 3186,3884 (and also Delucia,
Valunstead, Skara Brae's 889,2189 and Vesper's island). **There is no moongate art at any of them**: the whole SoS map
holds one static whose tiledata name says moongate (6518,365, the staff strip). Hammerhill and Kameron Kove are open
grass; Dragonstorm is a ring of stalagmites. So there is nothing to leave as decor, and none of them is in the gate list
(fact G3). If P669 5b gates them later, each needs a gate item placed and a PMList entry.

### 3. The teleporters (`server/data/teleporters-sos.json`, `GenTeleporter-sos-teleporters.patch`, `SosTeleporters.cs`)

**How it is wired.** Pinned's `[TelGen` reads one file. Our file holds every pinned entry with an end on Trammel or
Felucca (both stand on the SoS land, `SosMaps.cs`), as decided. `SosTeleporters.Merge` puts it in place of those entries
and keeps pinned's other facets (P676's pattern for regions; a copy of pinned's whole file would hide upstream's
changes). No pinned entry outside those facets shares a teleporter tile with ours, so the order changes nothing.

**Counted.** Pinned has 1,368 entries; **863** have an end on Trammel or Felucca, with **834 Trammel ends and 864 Felucca
ends**. On SoS, before any fix, **81 Trammel and 84 Felucca ends fail** the final rule (`out-tele.csv`, by `tele.py`):
58 and 60 do not stand, 10 and 10 are cave-mouth land with no floor, and 13 and 14 are sources that never fire. Some of
those are stock's own quirks (below). The brief said 60 and 72, from P669's coarser 3 x 3 grade; my first pass, with
P677's rule as it was, counted 68 and 70. Every end is decided in `notes\cc-P679-tools\out-tele-decisions.csv` (made by
`tele_fix.py`):

| | Trammel ends | Felucca ends |
|---|---|---|
| ok on SoS | 749 | 769 |
| as stock (fails the same way on EA's own Trammel, untouched by SoS) | 26 | 26 |
| re-placed onto a floor | 23 | 25 |
| dropped (with their entry) | 36 | 44 |

**The rule** (`tele.py`, shared by the fact):
- An end must stand: P677's rule (a floor, nothing solid in the 16 Z above, its Z within 5).
- **A source must fire.** Pinned hands `OnMoveOver` to an item 1 high only when it is at the walker's floor or up to 14
  above it (`Mobile.cs:4224-4228`). A source even 1 Z below the floor never fires.
- "As stock" applies only where SoS left the 3 x 3 alone and EA's Trammel fails the same way. For Felucca it needs the
  very same end on Trammel, since Felucca's own map is gone.

**Two checker fixes found on the way, both in P677's `spots.py`.** P677's fact was re-run after each and is still green,
with the same 397 literals:
- `avgz` halved toward zero; pinned's `FloorAverage` (`Map.cs:287-297`) rounds down. It was one Z high on odd negative
  sums (half of Destard's "never fires" came from this).
- **Cave-mouth land is not ground.** Pinned ignores land ids 2, 0x1DB and 0x1AE-0x1B5 (`LandTile.Ignored`;
  `Movement.cs:437` `considerLand`); only a static floor counts there. The walk below found it at Deceit.

**Re-placed (48 ends).**
- 15 needed only a Z.
- 15 moved one tile: Deceit's mouth (6), Britain Forest North's cave (6), a log wall in Bucs' Den (2), and an
  impassable edge in Felucca's Destard (1).
- 18 were set by hand:
  - **The Lost Lands pass at 5126,3143.** The author kept its shape but lowered it from Z ~98 to -5. It leads through
    the cave at 5850,432 to Britain, 1987,2062.
  - **Deceit's way out** lands on 4110-4112,432, one row past its new entrance row (431), so leaving the dungeon does
    not drop you on the way back in. Deceit's mouth is ignored land, and SoS removed stock's cave floor there (0x53C at
    Z 5, `art\deceit-stock.png` beside `deceit-sos.png`), so nobody could stand in it.

**Dropped (46 entries)**, by reason:
- **Blackthorn's entrance** (10: 1477,1471-1475 to 6432/6440,2677-2681). It is off on this land (P677); its land end is
  water, and its dungeon end is the author's Bleak Wind Tunnels, sealed until S18. **For P691:** Blackthorn's new way in
  must be added; the stock Trammel pair is gone from our file.
- **Bucs' Den** (6: 2685,2063 and 2756-2759,2092-2097). The author kept the Z -20 tunnel but rebuilt the town over it; no
  floor stands at Z 38-39 above it, so its ladders have no top.
- **The cave south of the old New Haven plaza** (1: 3508,2777 to 5912,355). Solid rock on SoS; nothing else leads into
  that cave.
- **Water at both ends even on EA's Trammel** (8: 424,3283 to 5267,2757 and 2985,2890 to 5974,2697). Felucca-only stock
  links that never worked on Trammel.
- **Felucca's own EA land** (21). Felucca reads the SoS Trammel files since P675, so its map0-only places are void, rock
  or somewhere else:
  - the x 6900+ strip, including the Ter Mur link at 6992,1367 and 7149,756;
  - Deceit's 7109,1097 link;
  - Felucca's Lost Lands pair at 5503,3971 and 5996,2367;
  - pinned's own slip, entry 1362, from Ter Mur 7149,756, which is outside Ter Mur.

  Ter Mur is still reached from Trammel (4194,3260). Felucca's way to Ter Mur is gone with its land; see the decisions
  below.

**Walked in a client.** On a private shard (2596, `sl-modernuo:cc-P679`), the playtest bot's client walked the Golem's
Tester onto every surface entrance whose ground SoS changed: **16 of 16 arrive inside** (`walks.json`, `walk_entrances.py`,
`notes\art\sos-s4-gates\walk-results.json`). The bot world was generated on stock and an Administrator cannot run
`[TelGen` (Developer; `Properties.cs:372` refuses raising one's own level). So the re-placed teleporters were moved in
that world with `[global set` first (`walk-prep*.json`).
- Deceit's first walk showed the cave-mouth gap: stepping onto the old mouth is refused.
- After the move, all three of its tiles teleport.
- Britain Forest North's moved cave (1297,1081) walks in too (`britain-forest-north\`).
- 1714,2996 is reached from the east; its north side is a static.

### 4. The staff go-menu (`server/data/Locations/`, `GoLocations-sos-go-menu.patch`)

`golocations.py` converts his `Data\Locations\trammel.xml` (copied as `cc-P679-tools\sos-trammel-locations.xml`):
- every `<parent>` becomes a category and every `<child>` a location, in his order, with his names and numbers;
- **410 spots in 112 categories**, counted from the file;
- the layout is pinned's (`name`, `categories`, `locations` with `[x, y, z]`).

`trammel.json` and `felucca.json` are the same tree under their facet's name. `GoLocations` reads
`Data/ShatteredLegacy/Locations/<facet>.json` when it exists, else pinned's. The Dockerfile copies the folder.

### 5. Proof

**The map fact, `tools/tests/test_s4_gates.py`** (`SL_SHARD_REPO`, `SL_SOS_MAP`, optional `SL_STOCK_TRAMMEL`):
1. every PMList gate on Trammel and Felucca (pinned's file with our patch, applied by `patch` at fuzz 0) stands exactly on
   one of its tile's floors;
2. every Trammel and Felucca end of the teleporters `[TelGen` makes stands, and every source fires, except stock's own
   quirks as defined above.

Results:
- **Red on main** (`red-test-s4-gates.txt`): 10 gates off their floor (Moonglow, Britain, Yew, Minoc and Trinsic on both
  facets) and 105 ends failing (60 more pass as stock quirks).
- **Green** (`green-test-s4-gates.txt`): 2 of 2, 1,618 ends, 52 stock quirks, 0 failing.
- P677's fact after both checker fixes: `green-test-s8-spots-after-p679.txt`.

**The code facts, `server/tests/Maps/SosGatesVerification.cs`:**
- G1, G2: the gates.
- G3: his spots are not gates.
- T1: the merge.
- T2: the shipped file (817 entries, none of the dropped ones, the Lost Lands pass).
- L1: the go-menu (410 spots, both facets).

Red runs (the gate patch, the shipped files and their Dockerfile and apply lines held back; pristine copies kept and
restored):
- **Run 1** (`red-gated-build-1-summary.txt`): my class was not in the "Sequential UOContent Tests" collection, so it ran
  before the host had maps. Pinned's PMList initializer threw (`Map.Trammel` null) and took pinned's Eodon PMList fact
  down with it. Fixed by joining the collection.
- **Run 2** (`red-gated-build-summary.txt`): G1, G2, T2 and L1 fail as they should (Moonglow at Z 5, not 23; no shipped
  files). T1 and G3 pass on red, as expected: T1 tests the new merge, and stock has no extra gates.
- An earlier attempt failed in `apply-patches.sh`: my three patches were not listed by name. Adding them is part of the
  change. The same run hit the known "never applied" race on `ItemIdentification-item-knowledge.patch`.

**Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P679`, `docker-build` lock, released), on the finished tree:
**EXIT=0, 2,753 tests, 2,747 passed, 6 skipped, 0 failed**, the three patches applied (`gated-build-summary.txt`). An
earlier green run before the Deceit fix gave the same counts.

**Moongate pictures** (`notes\art\sos-s4-gates\shots\`, P716's `shots.ps1`, off-screen TazUO with the SoS client,
`scenes.json` from `make_scenes.py`). One scene per gate: the Tester on Trammel and the Admin on Felucca, three tiles
north-west of it. The bot world's gates were moved to PMList's new spots with `[global set` (the log lists them before
and after).

What the final set shows (every picture was looked at):
- **In each of the 9 Felucca admin pictures, the gate stands where PMList puts it.** Moonglow, Yew, Minoc, Trinsic and
  Skara Brae sit in their standing stones. Britain's is inside the rock ring by the tree. Jhelom's, Magincia's and Bucs'
  Den's stand on open ground.
- **The Trammel Tester pictures show the same gates on Trammel**, and New Haven's in the author's Haven, east of the
  square. Scenes 6 to 9 are a retake (`proof-log-retake-6-to-9.txt`): in the main run the Tester was killed at Trinsic,
  so he was resurrected and made Blessed for the retake.
- **Britain from the Tester's side**: the ring's tree canopy hides the gate from every spot that keeps it clear of the
  login windows (`retake-britain\`). The admin's Felucca picture of the same tile shows it.

The earlier tries are kept, trimmed, beside the final set:
- `first-try\`: the Tester was a ghost from the dungeon walks, and the login windows covered the gate.
- `second-try\`: the first try's New Haven scene left the Tester on Haven Island, and the tutorial island gate then
  kept him there (he is a loop-0 trainee; `TutorialIslandGate.CanMove`). Every scene showed Haven's farm. The private
  shard's own Configuration copy then had `clusterf.tutorial.islandGate` off for the final set.

## Decisions and deviations

- **No migration work** (Chase 10-27: a fresh test world). None was planned here; the existing world's gates and
  teleporters are made by `[MoonGen` and `[TelGen` on swap day.
- **Felucca gets the author's go-menu too.** Its land is the same map. Pinned's Felucca menu would send staff into the
  author's walls.
- **Felucca's link to Ter Mur is gone** with Felucca's own land (x 6900+). Trammel's (4194,3260) remains. If Felucca
  needs one, it is a new teleporter on SoS land, a design call (not stock data).
- **His extra gate spots** have no gate art; nothing is placed for them.
- **`HavenSpots.cs`'s note says 3450,2677 is sea on SoS.** On the overlay it is dry land at Z 25. It no longer matters
  (the gate moved), and the comment was left as P678 wrote it, apart from the PMList sentence.
- **Follow-up, not done here:** P678's `notes\cc-P678-tools\soswalk.py` (behind `tools/tests/test_haven_spots.py`) has
  both slips: it halves the average Z toward zero (line 55) and stands people on cave-mouth land. New Haven's square is
  flat at Z 0, so its facts are unlikely to change, but a later swap prompt that reuses it should take `spots.py`'s two
  fixes.
- No CHANGELOG line: the swap is held from release. The swap release's notes should cover it.
- Outside the repos: `D:\UO\golems\Iron\p679-work\` (the overlay copy, main's tree for the red fact). It can be deleted.

## Files

- Code copy:
  - `server/patches/PublicMoongate-sos-gates.patch`, `GenTeleporter-sos-teleporters.patch`, `GoLocations-sos-go-menu.patch`
    (all built with `diff -u`, checked at fuzz 0), listed in `docker/uo/apply-patches.sh`;
  - `server/customizations/Maps/SosTeleporters.cs`; `server/customizations/Tutorial/HavenSpots.cs` (a comment);
  - `server/data/teleporters-sos.json`, `server/data/Locations/trammel.json` and `felucca.json`, copied by
    `docker/uo/Dockerfile`;
  - `server/tests/Maps/SosGatesVerification.cs`.
- Docs copy:
  - `tools/tests/test_s4_gates.py`;
  - `notes\cc-P677-tools\spots.py` (the two checker fixes);
  - `notes\cc-P679-tools\`: `sosland.py`, `grid.py`, `changed.py`, `tele.py`, `tele_fix.py`, `golocations.py`,
    `edit_pmlist.py`, `walkplan.py`, `walk_entrances.py`, `make_scenes.py`, the gated-build script, the outputs
    (`out-tele*.csv`, `walks*.json`, `scenes.json`, the red and green texts and summaries), `sos-trammel-locations.xml`,
    `art\`;
  - `notes\art\sos-s4-gates\`.

P679 DONE
