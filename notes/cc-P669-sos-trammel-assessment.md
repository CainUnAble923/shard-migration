# cc-P669: replacing stock Trammel with the Siege of Sosaria map, the impact measured

Iron Golem, 2026-10-26. Assessment only: no code, no map files, nothing deployed. Map by **Zigholtul** (Siege of
Sosaria Trammel Map 3.0); credit him if any of it ships. The map files were read only through P481's data copies in
`notes\cc-P481-tools\scratch\sos\`; nothing was built or run from `D:\UO\third-party`.

## In plain words

- Siege of Sosaria rebuilds almost half of Trammel. 42 percent of the map differs from stock, with 65 new islands and a
  new desert that joins Nujel'm to Moonglow. It also wipes out things we built on: New Haven's plaza (our tutorial
  start) becomes forest, Old Haven becomes a living town, and the empty corner the Wakening Isle was going into is now
  one of the author's caves. The pictures are in `notes\art\sos-survey\` (open `index.html`); `change-map.png` is the
  one-glance view.
- The author says it is unfinished and that he has made his last update. It shows: a bare rooster-shaped island, towns
  pasted in as hard-edged rectangles, and twice as many uncovered cliff seams as stock.
- A full swap means about 20 to 25 prompts of rework before 1.0. Across stock and our own code, about 3,400 placed
  things (spawners, decorations, gates, teleporters, our seeders) need reworking, and about 6,000 more need checking.
  It also breaks two promises we made: shipping only our own changes to the map, and standard geography that matches
  the wikis.
- **What you need to decide:** my recommendation is to lift the pieces you like (Valunstead, Fort Whitestone, the keeps)
  into stock Trammel one at a time, at about one prompt each, and to keep a whole "Sosaria" facet as a quest-gated
  extra world for after 1.0. If you agree, P662 to P666 (the Wakening Isle) can go ahead unchanged. The questions are
  at the end.

## 1. What it changes, measured

Tools: `notes\cc-P669-tools\` (`sosdiff.py`, `places.py`, `unfinished.py`, `newislands.py`, `render.py`, `pieces.py`,
`voids.py`, `geo.py`, `felucca.py`). Their CSV outputs are in `cc-P669-tools\out\`; the large block arrays stay in
`scratch\`, which is git-ignored. Stock Trammel means the vanilla 7.0.117.0 client: `map1LegacyMUL.uop`, `staidx1.mul`
and `statics1.mul`. Both maps are 7168 x 4096. A block is 8 x 8 tiles. Land differs on a tile when its id or Z differs.
Statics differ when the block's set of (x, y, z, id) differs (hue is ignored).

| Measure | Stock | SoS 3.0 | Change |
|---|---|---|---|
| Blocks differing (of 458,752) | | | **194,548 (42 percent)**: land 174,947, statics 128,319, both 108,718 |
| Surface blocks differing (x < 5120, of 327,680) | | | 146,031 (45 percent) |
| Dungeon and staff strip differing (x >= 5120, of 131,072) | | | 48,517 (37 percent) |
| Land tiles differing (of 29,360,128) | | | 9,513,224 (32 percent; includes re-tiled water round the new islands) |
| Statics | 2,903,696 | 3,842,765 | 1,271,032 only in stock, 2,210,101 only in SoS |
| Dry tiles | 9,470,899 | 12,681,729 | +34 percent: 3,471,207 new (from water or void), 260,377 lost |
| Islands of 400+ tiles (P481's survey, kind "island") | 33 | 97 | **65 new**, 465,664 dry tiles (`out\new-islands.csv`) |
| The author's 410 go-menu spots | | | 216 new or rebuilt, 101 touched, 93 as stock (`out\spots.csv`) |

**The change map** is `art\sos-survey\change-map.png`, with stock and SoS overviews beside it. Almost the whole
mainland is red (land and statics both rebuilt). The sea east of Nujel'm is a new desert continent that reaches Moonglow
(`top-nujelm-desert-the-new-landmass.png`; 1.11 million land tiles changed in its box). New islands lie all round. The
dungeon and staff strip east of x 5120 holds most of the author's 20+ custom dungeons.

**Towns** (author spots by town; new or rebuilt / touched / stock): Britain 6/26/9, Bucs' Den 10/2/0,
Cove 2/2/1, Delucia 11/1/0, Haven 8/2/0, Jhelom 0/1/6, Magincia 3/1/0, Minoc 3/3/0, Moonglow 4/2/0, Nujel'm 3/0/5,
Papua 0/8/6, Serpent's Hold 0/3/1, Skara Brae 4/2/2, Trinsic 3/0/5, Vesper 4/31/1, Wind 1/0/5, Yew 3/0/3.
New towns: Valunstead, Hammerhill, Kameron Kove. The author's regions also name Elmhaven, Kettleburg, Fort Yondall,
Elandrim Nur Shaz and Glimmerwood.

**Keeps, dungeon entrances and islands**, with renders in `notes\art\sos-survey\` (stock left, SoS right, the client's
layout; `index.html` shows them all):

| # | Place | Where | What SoS has |
|---|---|---|---|
| 1 | New Haven plaza (our tutorial start) | 3500,2585 | forest and shore: 3,587 of 3,711 stock statics gone, 2,200 of 2,601 land tiles changed |
| 2 | Old Haven, our Rootdeep way in | 3625,2620 | a living town over the ruins |
| 3 | SoS's Haven (Uzeraan's Mansion, docks, smithy, bank) | 3614-3722, 2516-2657 | the author's town on Old Haven's site |
| 4-5 | Britain and Moonglow moongates | 1336,1997; 4467,1283 | the stone circle is replaced (Britain: a rock ring round a tree) |
| 6 | Valunstead, walled town and moated keep | 479,388 | open sea in stock |
| 7 | Fort Whitestone | 890,1055 | new keep in Yew forest |
| 8-9 | Castle Dunbain, Fort Stormhammer | 1333,1377; 1490,1323 | new keeps north of Britain |
| 10 | Hammerhill (bank 1530,994, moongate 1541,1081) | region 1481-1622, 959-1068 | new town |
| 11 | Kameron Kove (moongate 1353,2451) | region 1200-1341, 2391-2558 | new town |
| 12 | Tigerclaw Fortress | 2595,1085 | new fort |
| 13 | Khalahandra Keep | entrance 2505,1707 (island 2456-2543, 1648-1707) | new island keep |
| 14 | Pyramid, Compassion Desert | 2104,611 | new |
| 15 | Nujel'm desert | e.g. 3813,1277 | new continent |
| 16 | Skypoint Islands | 4357,2349 | new isles with a ship |
| 17 | Glimmerwood | 2123,3330 to 2834,3488 | new region |
| 18 | Dragonstorm Island moongate | 3186,3884 | new island |
| 19 | Isle of the Avatar | 4764,3819 | new |
| 20 | New Magincia | 3700,2160 | rebuilt: 17,042 statics added |
| 21 | Fold void C | 6230,2000 | a cave dungeon (Passage of Lost Souls level 2, 6202,2116) |
| 22 | EA's Blackthorn dungeon area | 6151-6563, 2301-2839 | the author's dungeons (Hammerhill Sewers level 1 at 6394,2771); all 31,016 of EA's statics there are gone |

The other new dungeon entrances are listed with coordinates in `out\spots.csv` (rows "Dungeons", verdict "new or
rebuilt"), and the new islands in `out\new-islands.csv`.

**Unfinished areas** (`out\unfinished.csv`, pictures `top-unfinished-*.png`):
- The author's own words: the folder is "Siege of Sosaria Trammel Map (UNFINISHED)", and update 2 says "This will be
  the final update" (his servuo.dev page, read 2026-10-26).
- Bare new land, with no statics at all on whole 128 x 128 cells: a **rooster-shaped island** at 2840-3039, 1324-1523
  (15,584 dry tiles); the snow isles north-east of Moonglow (4224-4479, 256-767), where a town block is pasted in as a
  hard-edged rectangle; land east of Haven (3072-3199, 2304-2559); cells round Echoback and Darkfathom
  (4096-4223, 2560-2815).
- Uncovered cliff seams: dry tiles with no static where land Z jumps 20 or more, the black cuts in the renders. There are
  **107,741 on SoS's surface against 55,297 in stock**. The worst cells are Glimmerwood (2688-2943, 2688-3071) and the
  north-east isles.

**Custom art: none needed.** Every one of SoS's 8,683 item ids has art in the stock 7.0.117.0 art file
(`D:\UO\cc-p167-work\scratch-client\artidx.mul`). The 7 land ids without art are EA's own, used the same way in stock.
One caution: the author also publishes "UO Art Static Replacements for TazUO", so screenshots of his map may show
replaced art that our players would not see.

## 2. What breaks or moves on our side

Each point is graded on its own 3 x 3 tiles (`geo.py`):
- **Unchanged:** land and statics are the same.
- **Moves:** something changed there, but the spot is still dry, open and within 5 Z of stock. It must be looked at in
  game.
- **Rework:** the spot is now water or void, under an impassable static, or more than 5 Z off.

Points are counted from the files (`out\geo-points.csv`, per file `out\geo-files.csv`).

| What | Count | Unchanged | Moves | Rework |
|---|---|---|---|---|
| Stock spawners (pinned `Spawns/{post-uoml,shared}/trammel/*.json`) | 2,182 | 1,341 | 496 | 345 |
| Stock decoration items (`Decoration/Britannia` and `Trammel` cfg) | 25,568 | 18,423 | 4,774 | 2,371 |
| Stock teleporter ends on Trammel (`teleporters.json`) | 834 | 594 | 180 | 60 |
| Treasure map spots (`treasure.cfg`) | 193 | 57 | 66 | 70 |
| Public moongates (`PublicMoongate.cs` PMList.Trammel) | 9 | 2 (Jhelom, Skara Brae) | 3 (Trinsic, Magincia, New Haven) | 4 (Moonglow, Britain, Yew, Minoc) |
| Stock region rectangles (centres; `regions.json`, 145 regions) | 337 | 206 | 85 | 46 |
| Coordinates in our code and the bot (813 literals in 50 files) | 813 | 358 | 293 | 162 |

**Regions by share of their area changed** (`out\stock-regions.csv`): 17 untouched, 27 under 25 percent, 47 from 25 to
75 percent, and 54 at 75 percent or more. That includes New Haven (94 percent), Bucs' Den (91), Magincia (90),
Delucia (82), Moonglow (81), Minoc (71), Haven (66) and Britain (55), plus every New Haven shop region. 19 of our files
look regions up by town name. They keep working only if the redrawn regions keep the same names.

**Our files** (50 hold coordinates: 20 unchanged, 18 moves, 12 need rework):

| Area | Grade | Detail |
|---|---|---|
| New Haven and the tutorial plaza | **rework** | `Tutorial/TutorialCorePlacement.cs`: 8 of its 11 points need rework (the marks 3499,2571 and 3501,2571; the death, healer and gate spots). `ClusterFNewHavenSeeder.cs`: 1 rework. The plaza itself is gone (picture 1) |
| Old Haven and the Rootdeep way in | **rework** | SoS builds its living Haven over the ruins. Our achievement "found the ruins of Old Haven" (`ClusterFAchievements.cs:172`) would name a town. Of the 4 trammel.mapops blocks outside the Burrows, the 2 at the way in (3608-3623, 2616-2623) collide with SoS changes |
| Rootdeep Burrows | unchanged | 210 of trammel.mapops' 214 blocks sit in void that SoS leaves untouched, so the patch's fingerprints still match there |
| The Fold's void C | **rework** | Not empty: 63,346 dry tiles and 8,325 statics (a cave; 26,285 dry tiles inside the isle's drawn area 6170-6441, 1913-2057). The Fold maps read Trammel's file (P661), so all 17 would show it. The largest void left that is empty is 1008 x 352 at 6160-7167, 3744-4095. It takes the isle's 272 x 145 drawn area but not void C's whole 480 x 448 (`out\voids.csv`). P661's mirror region and P662's drawing would move there |
| `trammel.mapops` | moves | Re-based onto SoS: the 2 colliding blocks need redoing; the Burrows come through as they are |
| Moongates | 4 rework, 3 moves | above; SoS's go-menu also lists its own moongate spots (Hammerhill, Kameron Kove, Dragonstorm) |
| Guard zones and regions | rework | `regions.json`'s Trammel part redrawn, plus new regions for every new town and dungeon (the author's `Regions.xml` is ServUO format, reference only) |
| Spawners and decoration | 345 / 2,371 rework, 496 / 4,774 moves | above, plus new spawns for 216 new or rebuilt places |
| Vendors and NPCs | rework where they stood | the stock spawners above include the vendor sets; our seeders: `ClusterFNewHavenServicesSeeder.cs`, `ClusterFInstitutionSeeder.cs` (4 rework), `ClusterFMineCampLayout.cs` (6), `ClusterFSouthMineDecor.cs` (4) |
| Guild halls | rework | `ClusterFGuildHallPlacementData.cs`: 12 of its 118 points rework, 28 moves |
| Houses | nothing to move | live is retired and 1.0 is a fresh world, so no houses exist to orphan. House placement follows the new land by itself |
| Boats and docks | rework | New Haven's docks are gone; dock regions are part of the region rewrite. SOS bottles pick random water at runtime (`SOS.cs:168-180`), so they follow any map |
| Treasure maps | 70 rework, 66 moves | `treasure.cfg`'s 193 spots; the 3.47 million new dry tiles have none |
| Champion spawns | none on Trammel | stock champions are Felucca only (`GenChamps.cs:33-53`); see 3 |
| EA's later dungeons we run | rework | Blackthorn (`BlackthornDungeon/Generate.cs`: 61 rework; its dungeon is gone in SoS). Despise revamped (`DespiseRevamped/Setup.cs`: 6 rework; 2,203 of stock Despise's 4,667 statics differ). Stealable artifacts (`StealableArtifacts-servuo-entries.patch`: 44 rework). Shame is identical; Wrong has 139 statics changed |
| Play-test bot routes | moves | 3 bot files hold 4 points: `checks_p224_guilds.py` and `checks_p224_vbuild.py` move, `checks_p224_mule.py` unchanged |
| Achievements naming places | rework 1 | "found the ruins of Old Haven" (above). "visited all five facets" (`ClusterFAchievements.cs:174`) only matters for option (b). Exploration tracks 8 x 8 chunks per facet and does not care which map |

Not measured: whether SoS's walls block the walk between places (no flood fill was run); live NPC positions in the test
world save; the 6,000 "moves" points one by one.

## 3. Felucca

- **No Felucca version exists.** The author's servuo.dev page covers Trammel only, and update 2 is "the final update".
  The download holds only `Map1`, `Staidx1` and `Statics1` (`D:\UO\third-party\sos-trammel-map`, listed).
- **Stock Felucca is already its own geography.** It differs from stock Trammel in 33,678 blocks (17,187 on the surface):
  EA's Felucca-only areas (`felucca.py`).
- **Felucca's content on SoS land** (if Felucca used the same terrain) fares as Trammel's does:

| Felucca content | Count | Unchanged | Moves | Rework |
|---|---|---|---|---|
| Stock spawners | 2,122 | 1,311 | 505 | 306 |
| Decoration items | 26,107 | 18,879 | 5,065 | 2,163 |
| Teleporter ends | 864 | 558 | 234 | 72 |
| Moongates (PMList.Felucca: Bucs' Den in place of New Haven) | 9 | 2 | 3 | 4 |
| Region rectangles | 272 | 185 | 54 | 33 |
| Champion spawns (`GenChamps.cs`, Felucca only) | 17 | 11 | 3 | 3 |
| Our Felucca-only code | 6 points in 1 test patch | 0 | 0 | 6 |

Felucca's rules (PvP, no insurance and so on) are rules, not geography, so they do not move with the map.

**Swapping both, compared with Trammel only:**
- **Trammel only.** The two facets stop sharing geography. Moongates, runes and our 467 coordinates that serve "both"
  would each need two answers where the maps differ. A player crossing a moongate lands somewhere that no longer
  mirrors where they left. This is the worst of both.
- **Both, on one terrain (my pick if you choose the swap).** The server already lets a facet read another's file: pinned
  `map-definitions.json` has a `fileIndex` per facet, and the Fold maps use Trammel's this way (P661). Felucca would
  keep its index 0 and rules but read file 1. The client needs both `map0` and `map1` pointed at the same SoS file
  through `files-override.txt`; that is unverified, so a TazUO check comes first. Cost: one file, and Felucca's own
  content (above) reworked alongside Trammel's.
- **Both, Felucca from its own copy** gives the same terrain at twice the download, with no gain.

## 4. Delivery

**Client.**
- **Ship the whole map.** `Map1.mul` 89,915,392 + `Statics1.mul` 46,271,141 + `Staidx1.mul` 5,505,024 =
  **141.7 MB** on disk. The author's zip is 36,845,885 bytes, so the download is about 37 MB. TazUO is pointed at it
  through the existing `files-override.txt` lines (`map1legacymul.uop=`). The override names a UOP, so the MUL would be
  packed into one; `mapops.py`'s `synthetic_facet` already writes a UOP, so this is a small extension. Whether TazUO
  takes a `.mul` override directly is unverified. The launcher's stamp already skips the rebuild after the first start.
  Copying 142 MB takes seconds; the art build is unaffected, since the map is not art. The files cannot live in git
  (the 5 MB rule), so they would be a package vendor asset kept outside the repo.
- **A mapops patch is not workable.** Measured from the counts: 9,513,224 land lines, 2,210,101 adds, 1,271,032
  removes and 194,548 block lines, about 13.2 million lines. At the current patch's 19.2 bytes a line (253,167 bytes,
  13,186 lines) that is **about 250 MB of text** (an estimate from the counts, not a written file). That is 50 times the
  repo limit, and a PowerShell applier reading it line by line would be slow at first start (unmeasured).
- **Policy.** Chase's client policy (2026-10-02, `map-building-playbook.md` section 6) is "the map never ships; a patch
  of our changes does". A full swap or an added facet ships a whole third-party map built on EA's terrain. That is your
  call (question 5).

**Server.**
- The same 3 files go first in the data folders. The overlay mechanism already does this (`Build-MapOverlay.ps1`,
  `dataDirectories`). The file reader's order (UOP before MUL) needs one check.
- ModernUO needs its own data rewritten:
  - Trammel's part of `regions.json`: 145 regions, plus new ones.
  - Decoration: 2,371 stock items to rework and 4,774 to check, plus a port of the author's
    `SOS Trammel Dungeons.cfg` (775 lines of ServUO decoration: doors, teleporters and props for his dungeons).
  - Spawns: 345 to rework, 496 to check, plus new ones.
  - `teleporters.json`: 60 ends.
  - `treasure.cfg`: 70 spots.
  - `PMList`: 4 moongates.
  - The go-menu locations.
- The author's `Regions.xml` and `Locations\trammel.xml` are reference only (ServUO format). The overseer's
  `notes\sos-map-author-spots.md` already lists them.

**Art.** None needed (part 1).

## 5. Options with cost

Prompt counts are my estimates from the counts above, not measured.

| | (a) Full replacement | (b) Added facet | (c) Lift chosen pieces into stock Trammel |
|---|---|---|---|
| What it is | SoS becomes Trammel (and, best, Felucca on the same file) | SoS as a new world: its own map slot and rules, the way the Fold was registered (P661) | Copy a keep, a town or an island into stock Trammel through our existing mapops patch |
| Work in prompts | **about 20 to 25**: delivery and policy 2; regions 3; decoration and the author's cfg 2; spawns 4; moongates, teleporters and treasure 1; our code (12 files rework, 18 check) 4; the Fold moved and P662 to P666 re-planned 2; finishing the unfinished areas 3+; Felucca 1-2; bot and play tests 2 | **about 10 to 12**: delivery (new client map index, 142 MB) 2; registration and rules 1; regions 2; spawns and decoration 3; access and gating 1; trimming the duplicate stock towns 1-2 | **about 1 per piece** (land, statics, a blended edge, region, spawns, a play test); 5 to 8 pieces is about 6 to 10 prompts, done one at a time |
| Patch size | the whole map (above) | the whole map, as a new file | 0.2 to 2.5 MB a piece (`out\pieces.csv`): Valunstead 0.65 MB, Fort Whitestone 0.29, Khalahandra Keep 0.19, Tigerclaw 0.20, Hammerhill 0.75, Kettleburg 2.48; the whole Nujel'm desert would be 29 MB |
| What breaks | New Haven and the tutorial, Old Haven and Rootdeep's way in, the Fold's void C, Blackthorn, Despise, 4 moongates, 54 regions over 75 percent changed | nothing of stock | only what each piece's box covers (Valunstead, Khalahandra Keep and Fort Yondall's removals: 0, 0 and 1,553 stock statics; Kameron Kove's 6,790) |
| Risks | an unfinished map with no more updates from its author (we finish it); the fidelity principle (wikis would describe a different Trammel); every stock Trammel guide would be wrong | a second Britain, Moonglow and so on (SoS keeps the stock towns, rebuilt), confusing until trimmed; another file for players | a seam where SoS's land meets stock's at each box edge (one blending pass each) |
| What players see | a different Trammel from day one, unfinished patches included | stock Trammel, plus a new land they unlock | stock Trammel with new keeps, towns and islands appearing over time |
| 1.0 timeline | pushes 1.0 back by the whole block; P662 to P666 re-planned | after 1.0, nothing held | P662 to P666 go now; pieces fit between prompts before or after 1.0 |

**My recommendation: (c) now, and (b) as a later option.**
- Option (c) gives you the places you picked (Valunstead and Fort Whitestone, which stand on open sea or wild forest in
  stock) without breaking the tutorial start, Rootdeep or the Fold. It ships through the patch we already have and keeps
  stock geography where the wikis describe it.
- If after 1.0 you want the whole of Sosaria, (b) adds it as a quest-gated world, and (c)'s pieces stay where they are.
- Option (a) costs the most, breaks the most of what we have built, inherits an unfinished map, and is the only option
  that moves 1.0.

## 5b. Facet access (design only)

Gating facets behind quests or F-12 loops does not depend on the map. The public moongate's destination list, and
recall and gate between facets, can check a per-player unlock. The Fold already refuses travel by region rules
(`FoldRegion.CheckTravel`, P661), which is the model.

How each option fits:
- **(a) Full replacement.** Neutral for gating Ilshenar, Malas, Tokuno and Ter Mur. Trammel is still the hub. Its 9
  public moongates need re-placing (4 rework), and SoS adds its own moongate spots (Hammerhill, Kameron Kove,
  Dragonstorm), so the hub's gate list is redesigned anyway. A good moment to make the gate gump show only unlocked
  destinations.
- **(b) Added facet.** Fits best. A new world is a natural reward: no stock content expects to reach it, so a quest gate
  object or an F-12 loop unlock can be its only way in from the start, like the Fold's no-recall rule. It changes the
  "visited all five facets" achievement to six, or keeps it as five and gives Sosaria its own.
- **(c) Lift pieces.** Neutral for the other facets. Small gated spots inside Trammel (an island keep reached only by a
  quest boat or teleporter, Khalahandra Keep for example) would let us try the gating design cheaply before any facet
  is closed.

## For Chase

1. **Which path for Siege of Sosaria?**
   - **(c) Lift the pieces you like into stock Trammel, one prompt each (recommended).** I start with Valunstead and Fort
     Whitestone, which stand on open sea and wild forest in stock, so nothing of ours moves.
   - (b) Add it whole as a quest-gated facet after 1.0. I write that design next, with nothing held now.
   - (a) Replace Trammel with it (and Felucca on the same file) before 1.0. About 20 to 25 prompts, and P662 to P666
     re-planned.
   - Leave it as reference only.
2. **Release P662 to P666 (the Wakening Isle) now?**
   - **Yes (recommended).** Under (b) and (c), void C stays empty in stock Trammel, and the isle goes where P481 drew it.
   - No: hold them until the Siege of Sosaria path is settled.
3. **If (c), which pieces first?**
   - **Valunstead, Fort Whitestone, Khalahandra Keep, Fort Yondall (recommended).** Small patches (0.19 to 0.65 MB) with
     few or no stock statics removed.
   - Pick your own from `notes\art\sos-survey\` or `notes\sos-map-author-spots.md`.
4. **If (a), Felucca?**
   - **Same SoS land as Trammel, one file (recommended).**
   - Keep stock Felucca. The two facets stop mirroring each other.
5. **Shipping a whole map file (needed for (a) and (b), not for (c)): allowed?**
   - **Yes, as a package asset outside git (about 37 MB download, 142 MB on disk; recommended only if you choose (a) or
     (b)).**
   - No: patches only. Then only (c) is open.

## Asked, and commit preflight

- Nothing asked through Ask-Chase: the prompt asks for decisions as questions in these notes. Haven was not touched.
  Nothing was built or deployed, and no lock was needed.
- No code and no map files changed. New in this repo: these notes; `notes\cc-P669-tools\` (9 scripts, a `.gitignore`
  for `scratch\`, and `out\` CSVs and JSON, the largest `geo-points.csv` at 2.5 MB); `notes\art\sos-survey\` (33
  pictures and `index.html`, 6.4 MB in all, the largest 714 KB). No file over 5 MB. `docs\` untouched.
- Branch `golem/Iron/P669` in both work copies; not committed (the Golem commits).

P669 DONE
