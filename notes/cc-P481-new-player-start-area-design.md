# cc-P481: a secluded new player start area (design only)

## In plain words

**Update 10-26 (sections 11 to 13): the new island, and the six build prompts.** You asked for a new island built for
the tutorial.
- **The new Wakening Isle** is drawn in `notes\cc-P481-tools\new-isle\plan.png`. It is a long island, about 200 by
  90 tiles, in the empty corner of the map. One road runs west to east: the beach where players wake, the first
  lessons, a flat meadow with the farm, a training yard, a trades square with the practice bank, the League lodge,
  standing stones on a low hill for the vision, and a dock with the moongate to New Haven. The walk is 201 tiles,
  measured on the sketch, plus 20 inside the farm. Players need only the usual package update, no new map files.
- **One change from your lean:** I now recommend giving each new player (or party) a **private copy of the whole
  island**, instead of one shared island where other players are hidden. With one shared island, two hidden players
  still fight over the same farm pests, share one lodge door and can bump into each other's invisible pets. Copies
  avoid all of that, and on this server they cost little memory. Section 12 has the comparison.
- **Six build prompts** (F1 to F6) are written at the end of the notes, in order, for the overseer to number: the
  new world, the island map, moving the tutorial with the start choice, the private copies, the vision scene, and
  pet protection with the vet.
- **For you:** look at the island pictures. Then say whether you agree to private copies instead of the hidden-players
  mix, before F4 is queued. F1 to F3 do not depend on that answer.

**From the 10-25 design (history; the Fold still holds, and sections 11 to 13 replace the island, the walk and the
privacy choice):**

- New characters would wake on a small island of their own, the **Wakening Isle**, instead of the busy New Haven plaza.
  One road runs across it with every core lesson in a line, the farm included. The last lesson is a moongate on the
  pier that drops them beside Rook in New Haven. No lesson sends them back the way they came. The walk from the beach
  to the moongate is about 165 tiles.
- The island sits on a new world of our own, **the Fold**. To the server it is a separate world, with nobody else's
  players, items or monsters in it. On players' screens it is drawn from an empty, unused corner of the Trammel map
  file. So **players need no new client files and no client change**: the island reaches them through the same map
  patch the player package already ships. A world with its own client map number would need new map files on every
  PC and a TazUO setting change, and anyone with an old package would see Felucca. That is a real problem, so I
  recommend against it.
- On the island, each new player sees only themselves, staff, the island's own NPCs, and the lesson items made for
  them. The vision lesson becomes a 45-second private scene: the screen goes dark, the Stranger strikes the Gem, the
  sword breaks, the player meets their own echo, and a hint of the League. Character creation offers "Tutorial Island
  (recommended)" or "New Haven (skip the tutorial)". The farm keeps its vet, free while Young, so a dead pet can be
  brought back there.
- **For you:** pick one in the Ask-Chase question: the recommended Fold island, or option A, B or C. A second
  question asks how private the island should be (my pick: the mix you leaned toward). The build is then about six
  Golem prompts. Pictures are in `notes\cc-P481-tools\` (list below).

2026-10-25, the Iron Golem (Opus 5.5), branch `golem/Iron/P481` of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Iron\cc-P481-new-player-start-area-design.md`. Design only: no code, map or package was
changed, nothing was built, deployed or run on a shard. Not committed (the Golem commits).

## The pictures (`notes\cc-P481-tools\`)

| File | What it shows |
|---|---|
| `fold-zones.png` | The Fold's usable space: void rectangle C of the Trammel map file (x 6160-6639, y 1832-2279), with zones 1 to 5 |
| `fold-isle.png` | **The recommended layout:** the Wakening Isle top-down, stops 0 to 10, the road, the farm; the walk counted on foot over the sketch, 165 tiles |
| `fold-isle-iso.png` | A mock in-client view of the arrival camp (stops 0 to 4), drawn by `scripts/mapbuild/isorender.py` with stock art (no shore transitions yet, hues not applied; the build's renders follow the playbook) |
| `option-A.png` | A: a new island in the sea south of Haven Island (Trammel), about 90 x 60; walk 70 tiles counted straight (no tiles exist yet), plus the boat or gate |
| `option-B.png` | B: a palisade glade on Haven Island's south-west arm; walk 97 tiles, **walked on the real map** |
| `option-C.png` | C: a new hall west of New Haven beside the P276 farm; walk 71 tiles (the hall legs straight, since the hall is not built; the farm legs walked) |
| `topdown.py`, `facet_plan.py`, `plan-*.json` | The scripts and plans that drew them (read-only on the client files; `MAPBUILD_CLIENT=D:/UO/UltimaOnlineVanilla`, `MAPBUILD_ART=D:/UO/cc-p167-work/scratch-client`) |

Route lengths: `topdown.py` walks the real map files with an 8-direction search under pinned Movement.cs's rules,
reduced to the files as P188's `Walk` does (land Impassable or Wet blocks; an Impassable non-Surface static within
PersonHeight 16 blocks; a step up over 2 blocks; no diagonal past a blocked corner). Server items such as doors and
the farm addon are not in the files, so legs through them are counted straight and marked so.

## 1. What must live in the start area

| Thing | Today (P289, P475, P480) | In the start area | Could stay in New Haven? |
|---|---|---|---|
| Arrival point | 3503,2574,14, the plaza (`CharacterCreation.cs:129-136`) | Yes: the start | No: that is the point of moving it |
| Rook Hallowell (recruiter, lesson menu, graduation, wings, remedial, companion) | 3500,2572,14 | **A greeter runs the core menu on the isle**; Rook stays in New Haven, where the last lesson's moongate lands (`TutorialCorePlacement.GateExit` 3501,2572 is already beside him) | **Yes, Rook stays.** He graduates, opens the wings, runs remedial training |
| Walking tiles (blue and gold, P480) | 3499,2571 and 3501,2571 | Yes | No |
| Practice bag (backpack lesson) | the plaza | Yes | No |
| Practice cloak (paperdoll lesson) | the plaza | Yes | No |
| Chat ("I am ready to learn") | the plaza | Yes | No |
| Death and resurrection: the pale echo and Sera | 3402,2617 and 3402,2613, the farm gate | Yes | No |
| Practice bank (Merrin, the token) | the New Haven bank, 3492,2577 | Yes: a small practice bank and its own banker | It could, but then the line breaks: the player would leave and come back |
| Getting around (the moongate) | 3402,2615, to the plaza | **Yes, and last:** the pier moongate is the way out | No |
| The League (Elara Voss) | inside the Registrar's house, 3459,2601 | Yes: a League lodge with a second Elara (the same `LeagueRegistrar` type, placed by the seeder as P289 does) | It could, but it is lesson 8 of 10 and would need a return trip |
| The vision marker | 3402,2619 | Yes: standing stones, and the private scene (section 6) | No |
| The farm (Wren, pests, pen, the pet pick, P276) | 3388-3411 x 2600-2626 | Yes: in line after chat | No (Chase 11:18) |
| The vet (Tobin, P480) | 3400,2612 | Yes, at the farm | New Haven keeps its own vet by the stables (3526,2578, P480) |
| The 28 wing lessons (trades, combat, magic) | Rook's menu, New Haven | **No: they stay in New Haven** with Rook, the skill trainers and the quest board | Yes |

## 2. The options

The same line runs in every option (Chase 11:24): arrival, walking, backpack, paperdoll, chat, farm (pet pick, pests,
bandages, the vet), death (echo and Sera), bank, League, vision, then the moongate or boat to New Haven as the last
step. The order keeps P480's rule that each lesson only needs what came before it: the bank needs speech and dragging
(chat and paperdoll come first), and the League lodge keeps P480's "double-click its door to open it" line.

| | **The Fold (recommended)** | A. New island off Haven (Trammel) | B. Walled glade, Haven SW arm | C. Private hall in New Haven |
|---|---|---|---|---|
| Where | Server map 32 on Trammel's map file, void C (6200-6400 x 1890-2110) | Sea south of Haven Island, about 3540-3630 x 2930-2990 (water now; inside the "Haven Island" region, which ends at y 3094) | 3376-3444 x 2702-2786 (forest and grass, no buildings) | A new hall at 3368-3394 x 2566-2590, next to the P276 farm |
| Why it is quiet | No other player is on the map at all (and section 5 hides even other trainees) | Water all round; only the ferry or gate reaches it | South of everything; but the New Haven **public moongate** (3446-3456 x 2674-2684) is 20 tiles from its north gate, and pinned spawns Brigand, Harpy, Ettin, wolf and wildlife spawners at 3379,2693, 3446,2741, 3449,2737 and 3450,2734 (`Spawns/post-uoml/trammel/Outdoors.json`, `WildLife.json`), which would need moving | Not quiet: town traffic walks past; only the walls keep it apart |
| Walk | 165 tiles (sketch) | 70 tiles (straight, sketch) | 97 tiles (walked) | 71 tiles (hall straight, farm walked) |
| Leaving | Pier moongate to 3501,2572 beside Rook | A ferry (a stock boat cannot be relied on, so a ferryman's "Board" button, a timed teleport with a boat sound) or a gate | A gate at the north palisade, or simply the road north | The farm-gate moongate as today |
| Reused | Every lesson's code, the farm addon (moved), the vet, the elixir, Rook, all New Haven | The same | The same | The same, and the farm stays where it is |
| New map work | An island of about 200 x 90 inside a 220 x 220 sea, in a void nobody else uses | A 90 x 60 island, plus shoreline transitions against stock sea | A palisade ring, a second farm site (the farm addon moves; its tree removals become new ones) | One hall (a building: walls, roof, doors, by the playbook) |
| Prompts to build | 6 (section 7) | 4 | 4 | 3 |
| New server work | A map definition, a region, the private visibility hook | A ferry and the region | The region, spawner moves | A region over the hall |
| Private? | Fully (a world of its own, plus section 5) | Only by distance | No: Haven's spawns and travellers | No |
| Room to grow | The rest of void C (480 x 448) and voids D and E (P24 2.1) | None | None | None |

**What breaks for characters partway through (every option).** The tutorial runs only on test worlds today
(`ClusterFTutorial.Enabled` needs `testCenter.enable`, P289), so no live character is partway. The record keeps
done keys, not places (`TutorialRecord.StationsDone`, P480 part 4), so a test character InCore keeps every lesson it
finished. At its next login it is moved to the isle stop of its first undone lesson. One case needs a rule: a
character that finished the travel lesson under the old order is past the moongate. The move treats travel as done
only once the other eight are done, and otherwise offers it again at the pier.

**How staff and returning players skip it.** Staff are never entered (P289 fix 3, `ClusterFTutorial.TryEnter`) and
start where staff start today (Green Acres). They reach the isle with `[Tutorial goto` (new, staff only) or `[go`.
Characters made before the go-live are never entered or moved: P80's open item 1 (every NotStarted account entered at
its next login) is settled as "only characters made after go-live". They can still ask Rook for the tutorial. A
returning player's new character gets the start choice below and can skip.

## 3. The recommended direction: the Fold

### 3.1 The map

- **Server map index 32, client id 1, file index 1** (Trammel's files), width 7168, height 4096, `TrammelRules`,
  season 0 (spring, as Trammel), name "TheFold". Why:
  - Pinned allows any index outside 0-31, 127 and 255, and the client id and file index must be 0-5 for a map the
    stock client can show (`Projects/Server/Maps/MapLoader.cs:33-41`, table of 0x100 at `Map.cs:91`; registration
    `MapLoader.cs:103-118`). 32 is the first free index.
  - Two maps with the same file index share one tile matrix (`TileMatrix.cs:79-86`), so the Fold costs almost no
    memory. It is how Felucca and Trammel were once two worlds on one file.
  - The client is told map id 1 (`OutgoingMapPackets.cs:62`, `(byte)map.MapID`) and draws Trammel's tiles. Nothing
    in the client knows the Fold exists.
- **Where the tiles are:** the island is painted into **void rectangle C of Trammel's file, x 6160-6639,
  y 1832-2279 (480 x 448)**. P24 (section 2.1) found it empty, and this prompt recounted it on the 7.0.117.0 files:
  every one of its 215,040 cells is void land 0x0244 at Z 0, with 0 statics. It lies in no pinned region and no
  ServUO Trammel region, and away from the GM Jail and Rootdeep (candidate A, 5136-5247 x 1128-1263). Growth room:
  voids D (6496-6815 x 1552-1815) and E3 (6672-7151 x 776-1143), same source.
- **Trammel side:** the same painted tiles also exist on Trammel, where no road, gate or teleporter reaches them.
  A small `FoldMirrorRegion` on Trammel over void C sends any non-staff player found there to New Haven, in case a
  bug or a future teleporter ever puts someone there. Exploration: `ClusterFExplorationManager.cs:31-38, 73` stops at
  x 6144, so the island never marks as explored. That is harmless (P24).
- **How the client gets it:** through the existing route, with no new files. The island's land and statics become
  lines in `player-package/vendor/shattered-legacy-map/trammel.mapops` (now 12,972 change lines, facet 1, `F 1 214`).
  `Apply-MapOps.ps1` writes them into the player's own copy of the Trammel files, and the server's overlay gets the
  same file through `docker/uo/Build-MapOverlay.ps1` (playbook section 6). TazUO and ClassicUO need nothing.
- **File sizes:** the shipped files do not grow, since the Trammel files stay 89,965,543 + 5,505,024 + 20,393,786
  bytes. The patch text grows. The sea has to be written over the void too, so a 220 x 220 box is up to 48,400 `L`
  lines at about 20 bytes each: about 1 MB. Add the isle's statics (estimate 4,000 to 6,000 `S+` lines). That fits
  the 5 MB rule, and the package zips it. A one-line `R` (fill a rectangle) operation in `mapops.py` and both appliers
  would cut it to a few hundred KB, which is worth it if a later zone is bigger.
- **Rules (one `FoldRegion` per zone, registered in code as `OldHavenBurrowsRegion` is, on map 32):**
  - No housing: the region forbids it (pinned `HousePlacement.cs:76` honours `NoHousingRegion`). A map-wide rule
    needs a region over the whole map, since map-wide bans are hard-coded per stock map (`HousePlacement.cs:66`).
  - No recall, mark or gate in or out: `CheckTravel` refuses every type (the `GreenAcresRegion` model,
    `GreenAcresRegion.cs:23-41`; `SpellHelper.cs:633-642` asks both ends). Only our moongates and staff move people.
  - Young and Trammel protection: `TrammelRules`.
  - Light: always day on the isle (`AlterLightLevel`, as `DungeonRegion.cs:27`), except in a vision.
  - Season 0 from the map definition (`Mobile.cs:7065`, sent at login). Winter decor (P266) never applies here.
- **Map definition, how:** pinned loads `Data/map-definitions.json` (`MapLoader.cs:53`), which the image copies from
  pinned's Distribution (`docker/uo/Dockerfile:102`). Either a customization registers map 32 in code before world
  load, or a one-entry patch to the json. **Unverified:** whether a customization's `Configure` runs early enough. It
  is the first thing the facet prompt checks. Saves store a mobile's map by index, so index 32 must never be reused.
- **Built (P661, 10-26): indexes 32 to 48 are reserved for good.** `server/customizations/Fold/FoldMaps.cs` registers
  map 32 "TheFold" and the tutorial copies 33 to 48 "TheFold 1" to "TheFold 16" in a `Configure` at priority 3, after
  `MapLoader.Configure` (2) and before world load, so no JSON patch. A save names a map by its index byte, so none of
  32 to 48 may ever be reused, renumbered or unregistered; a larger pool grows upward from 49. The Fold's rules (no
  housing, no recall, mark or gate in or out, always day) are each map's **default region** (`FoldRegion`), not a
  registered whole-map region: registering one over 7168 x 4096 builds all 114,688 sectors of each map (P661 notes).
  So every zone region F2 to F4 adds on the Fold takes `FoldRegion.On(map)` as its `Parent`, or it loses those rules.

**Not recommended: a facet with its own client map number (id 6, file index 6).** This is a real problem for the
client and the package, and it is the plain answer to the prompt's question:

- TazUO loads `MAPS_COUNT = 6` maps with a hard-coded size table (`ClassicUO.Assets/MapLoader.cs:23, 38`). A seventh
  map needs a seven-entry `maps_layouts` in every player's settings (`:102-123`; ours is null).
- TazUO turns any map id at or above `MAPS_COUNT` into 0 (`World.cs:205-211`). A player with an old package would
  stand on the isle and see **Felucca**.
- The package may not ship EA files (gate 4, `Build-PlayerPackage.ps1:50-53, 441-444`), and `Apply-MapOps.ps1` only
  knows facets 0-5 (`:45, 134`). So map6, staidx6 and statics6 would have to be built on each PC from a source we
  write. A 1280 x 1280 map file alone is 5,017,600 bytes.
- The server overlay script expects exactly three files back (`Build-MapOverlay.ps1:35`).

The void route gives the same separate world with none of this. Keep id 6 for a day when the voids run out.

### 3.2 The Fold's layout (`fold-zones.png`)

| Zone | Where (void C) | What |
|---|---|---|
| 1 Wakening Isle | 6190-6410 x 1890-2110 (220 x 220 with its sea; the island about 200 x 90 on the diagonal) | The tutorial |
| 2 Vision chamber | 6440-6463 x 1850-1873 | A 24 x 24 dark stone room. It exists on every Fold map (same tiles), so each vision copy (section 5) uses it for free |
| 3 League private spaces | 6480-6630 x 1850-2040 | Chapter 6's custom "Setting" and any later solo trial rooms |
| 4 Events | 6170-6400 x 2125-2270 | Seasonal and staff events |
| 5 Custom dungeons | 6420-6630 x 2060-2270 | Custom content that should not share Trammel |

The League's other chapters (2 to 5) are private copies of vanilla dungeons on other file indexes (storyline,
decided 5 and 6). They follow the same trick: maps 33+ with Trammel's, Malas's or Ilshenar's file index, sharing
tiles. So the Fold's slot manager (section 5) is the League's trial-map pool, built once.

### 3.3 The Wakening Isle (`fold-isle.png`, `fold-isle-iso.png`)

The road runs south-west to north-east, one way, each stop 8 to 24 tiles after the last:

| Stop | Place | Leg (tiles) | Lesson |
|---|---|---|---|
| 0 | The shore: the player wakes on the sand; the greeter (proposal: "Tamsin, the League guide") | - | arrival |
| 1 | Two bright floor tiles by the road | 8 | `core.movement` |
| 2 | A camp: campfire, bedrolls | 10 | `core.backpack` (the blue bag) |
| 3 | A sign and a clothes rack | 12 | `core.paperdoll` (the cloak) |
| 4 | A signpost; the greeter's second spot | 10 | `core.chat` |
| 5 | The farm gate (P276's farm, moved whole; Wren, the pen, the field, Tobin the vet) | 16 | the pet pick, the pests, the bandages, the pet death line |
| 6 | A small shrine with an ankh: the pale echo and Sera | 24 | `core.death` |
| 7 | A stone practice bank, Merrin | 22 | `core.banking` |
| 8 | The League lodge (a door to open), Elara | 20 | `core.league` |
| 9 | Standing stones | 19 | `core.loop`, the private vision |
| 10 | The pier and its moongate | 24 | `core.travel`: out to 3501,2572, beside Rook |

## 4. The walk, start to finish (recommended option)

The arrow is the existing quest arrow (`GuildDirectionArrow`, P289 fix 2), pointed by each lesson in turn.

1. Character creation, "Tutorial Island (recommended)". The character wakes on the isle shore (stop 0). Lines: "You
   wake on a quiet shore." Arrow -> the greeter (stop 0).
2. Double-click the greeter (two quick left clicks, P480's wording): the core menu, the nine lessons. Arrow -> the
   blue tile (stop 1).
3. Walk onto the blue tile, then the gold. Arrow -> the camp (stop 2).
4. Open the paperdoll, then the backpack on it, and double-click the blue bag. Arrow -> the rack (stop 3).
5. Drag the cloak onto the paperdoll. Arrow -> the signpost (stop 4).
6. Say "I am ready to learn". Arrow -> Wren at the farm gate (stop 5).
7. At the farm: pick a dog or a cat (the account's one pet; graduation then offers none). Clear three pests, use
   Wren's bandages. Hear the pet line: "If your pet dies, bring its ghost to a vet. Tobin here does it free while you
   are Young. In New Haven the vet is by the stables." Arrow -> the shrine (stop 6).
8. Double-click the pale echo, Ready, die. As a ghost double-click Sera, Resurrect. Arrow -> the bank (stop 7).
9. Say "bank", drag the token into the box. Arrow -> the lodge door (stop 8).
10. Open the lodge door, double-click Elara. Arrow -> the standing stones (stop 9).
11. Double-click the stones: the vision plays (section 6), then "Core finished but one: take the moongate."
    Arrow -> the pier moongate (stop 10).
12. Step into the moongate: travel is done, and the player stands beside Rook on the plaza. Arrow -> Rook.
13. Rook: Graduate (loop 1, the box, opened in town), then the wings, as today.

## 5. Instanced, so nobody interrupts

What the engine gives (pinned): a viewer's `CanSee` decides what is sent and heard. Speech goes only to mobiles
that `CanSee` the speaker (`Mobile.cs:5611-5613`), and `PlayerMobile.CanSee(Mobile)` is virtual, with a visibility
list already (`PlayerMobile.cs:3239-3279`, `:3282`). Entity effects check `CanSee` (`Effects.cs:101-103`), but
**location effects and sounds go to every client in range** (`Effects.cs:66-77`, `:168`). In Trammel rules players
walk through each other (`Mobile.cs:4477`, `FreeMovement`), so an invisible player never blocks a road.

| | (i) Private visibility | (ii) Copies of the area | (iii) The mix (recommended) |
|---|---|---|---|
| How | One isle. A patch hook in `PlayerMobile.CanSee(Mobile)` and `CanSee(Item)` (`ClusterFPrivacy.CanSee`): inside the isle region a player sees only themselves, staff, the shared NPCs (seeded with no owner), their own pet and corpse, their party, and items made for them (`IPrivateTutorialItem.Owner`) | N Fold maps (33 to 32+N), all on Trammel's file, each a full seeded copy of the isle; a slot manager gives a free copy and resets it on leave | (i) for the whole isle, plus a private copy of only the **vision chamber** for the 45-second scene |
| Cost | 1 patch (two hooks, about 20 lines), 1 region; about 1 prompt | Map work is **not** N times: all copies share the tiles. But N times the NPCs, farm addon (330 pieces), spawners and seeding; a slot manager; resets; a full-house queue | (i) plus a slot manager for small, empty chamber copies (the scene spawns its own figures); about 2 prompts. The same manager is the League's trial pool |
| Speech | Others' speech never reaches you (`CanSee` gate), so "I am ready to learn" is yours alone | Separate maps: nothing crosses | As (i) |
| Party | **A party sees each other**, so friends can start together | Only if the manager puts a party in one copy | As (i); a party's members each get their own vision |
| Pets | Your pet follows your visibility; others' pets are hidden | Separate | As (i) |
| Corpses | Yours only (the corpse's owner) | Separate | As (i) |
| Effects and sounds | Must be sent to the one NetState in code (location effects otherwise reach everyone in range) | Separate | The scene sends to one NetState, and is in its own copy anyway |
| Staff | See everyone and everything (AccessLevel above Player) | Must pick a copy (`[Tutorial goto <n>`) | As (i); the vision copies are visible with `[Tutorial goto vision <n>` |
| Logout and reconnect | You log back in where you were; lesson items are yours and persist | The copy must be held for you (say 30 minutes) or you lose your place | As (i); a vision in progress is ended and you return to the stones, scene replayable |
| League trial maps | No help | The same pool idea | Builds the pool the storyline needs (decided 5: private trial maps) |

Recommendation: **(iii)**, as Chase leaned (11:29). (i) alone leaves the vision's sounds and lights shared with
anyone near the stones. (ii) costs the most server objects and turns a crowd into a queue.

## 6. The vision as a staged scene (about 45 seconds)

Run by a server timer (`TutorialVisionScene`), for one player, in a private copy of the vision chamber (zone 2).
The player is held still with `Frozen` and released at the end. Light changes per player: the chamber region's
`AlterLightLevel` reads the scene's current level, and `CheckLightLevels(true)` pushes each change
(`LightCycle.cs:61-62`, the 5-second timer `:96-106`). Subtitles appear in a borderless centred gump (HTML, P480's
`TutorialStyle` colours). Optional full-screen still panels are gump art Chase draws later. They ship as gump
overrides in the package (`vendor/shattered-legacy-art/gumps\<id>.png`, cc-P62), on IDs reserved in `registry.csv`.
Every effect and sound goes to the player's NetState only. The figures are temporary mobiles in the copy, deleted at
the end. The lines are P80's four (`ClusterFLoops.cs`, `TutorialVision.Lines`), split over the beats; chapter 1 of
the storyline adds the hint.

| s | Beat | Effects (item art / particle) | Sound (pinned use) | Line (subtitle unless said) |
|---|---|---|---|---|
| 0-3 | Touch the stones. Frozen; fade to black (light 30 per player); move to the chamber copy | sparkles 0x376A at the player (`Resurrection.cs`) | 0x1FE (Teleport.cs) | "A vision." |
| 3-8 | Dim light up (18). The Gem on a plinth, a worldgem bit 0x1EA7 tinted Celestial; the Stranger (body 0x190, dark robe) beside it with a longsword 0x0F61 | sparkles 0x376A on the gem, repeating | 0x20F (DivineFury.cs) as a low chime | "Long ago, the Stranger came for the Gem of Immortality." |
| 8-12 | The strike | bolt (`BoltEffect`, `Lightning.cs:52`); explosion particles 0x36BD at the gem (`Explosion.cs`) | 0x29 (ChainLightning.cs), then 0x307 (Explosion.cs) | "The sword strikes the Gem. The shards fly." |
| 12-17 | The shards and the broken sword: moving particles from the gem to five points; crystal shards 0x5738 left on the floor; the sword item replaced by its pieces | moving particles 0x3779 (`WordOfDeath.cs`) | 0x211 (WordOfDeath.cs) | "The blade breaks with it." |
| 17-21 | White flash (light 0), then black: the world folds | optional **panel 1** (the broken sword) | 0x220 (Earthquake.cs) | "You fall, and the world folds shut behind you." |
| 21-30 | Dim light. The player's own echo appears (a clone of the player's body and clothes, pinned's `Clone` in `MirrorImage.cs:119`), and speaks above its head | sparkles 0x376A as it forms; 0x374A as it fades (`WraithForm.cs`) | 0x44D (WraithForm.cs) as it forms; 0x3C4 (Invisibility.cs) as it fades | echo, said: "You wake where you started, remembering. That is a loop. Your level goes back to 1; your skills go with it." |
| 30-38 | A hooded figure at the edge of the light; a stone ring with a broken sword (the League crest) | optional **panel 2** (the crest) | 0x212 (HolyLight.cs) | figure, said: "Some of us remember. We keep the League, and we are looking for the pieces." Then subtitle: "What you keep: the League, your recipes, your achievements, your guild ranks." |
| 38-45 | Fade to black; back to the stones; light restored; released | sparkles 0x376A | 0x1FE | "This was only a vision. Nothing about you has changed. Yet." Then: "Take the moongate on the pier." |

The scene changes no skill, level, loop or Young status, as the vision is built today (`ClusterFLoops.cs`, P289's
check). A logout ends it. The chamber copy is freed, the player is put back at the stones, and the next login can
replay it. If no chamber copy is free, the scene plays in place under (i) and only the player sees the figures. The
art IDs above are candidates from tiledata names; the scene prompt picks them from a render, as the playbook asks.

## 7. Start choice at character creation

- **The city list can carry it, with no client change.** `CharacterCreation.ConstructAvailableStartingCities` (now
  only New Haven, `CharacterCreation.cs:129-136`) gets two entries:
  - index 0, "Tutorial Island", with a new cliloc description, "Start with the tutorial (recommended)...";
  - index 1, "New Haven", with the description "Skip the tutorial: start in New Haven".
  - The custom text goes in the package's cliloc entries (`vendor/shattered-legacy-cliloc/entries.json`).
  - The server already moves the character to the chosen entry (`:268-269`, `GetStartLocation` returns `args.City`
    under SA, `:298-300`). The Tutorial Island entry is caught there and sent to the isle on map 32.
- **Send both entries as Trammel.** TazUO draws city 0's map picture, and it would crash on a city 0 on map 6 or
  above (`CreateCharCityGump.cs:104-106`, the name table of six, `:21-28`). It places buttons by percentage of the
  facet size (`:165-173`). So the Tutorial Island entry carries display coordinates in the sea south of Haven
  Island (about 3600,2960), where its button reads as "an island near New Haven". Index 0 is the default selection
  (`:59-61`), so a player who just clicks through gets the tutorial. The client never skips the city screen (no
  check on the count, `CharCreationGump.cs:40, 101`).
- **Skipping follows P371.** At creation the character has no NetState yet (pinned `IncomingAccountPackets.cs:198-207`),
  so `OnCharacterCreated` only records the choice (an account flag value). The first login then calls `TryEnter` and
  `Skip`. That gives the same state as Rook's skip button: Skipped, loop 1 (`ClusterFLoops.Graduate`), "Didn't Read the
  Manual". It has no graduation box, as P371 built it, and Rook later offers Remedial training.
- **Choosing the tutorial later:** Rook's Remedial training button sends the skipper to the isle's shore. They walk
  the same road with remedial rules, and the pier moongate brings them back to Rook, who gives the box and the
  second achievement as today. A loop-1 character on the isle is fine: the isle's region keeps out recall and gates
  either way.
- **Fallback if the list ever cannot carry it** (an old client below 7.0.13 has no map or description in the list,
  `LoginHandshake.cs:526-535`): one city, and a two-button gump at the first login ("Tutorial Island
  (recommended)" / "Skip: New Haven"), which calls the same code.

## 8. Pets on the island (Chase 11:34)

- **The vet at the farm:** Tobin (`TutorialVeterinarian`, P480), free while Young, moves to the isle farm with the
  farm. New Haven keeps the vet P480 places by the stables (3526,2578) when no vet stands within 60 tiles of the town
  centre. Pinned's spawn data has none there (P480 findings).
- **One lesson line** at the farm (walk step 7). Wren's existing ghost-pet line (P480 `TutorialFarm.NoticeGhostPet`)
  points to Tobin.
- **Young pet protection on the isle (recommended):** a Young player's pet that dies anywhere on the isle is
  resurrected free the moment its ghost comes within 3 tiles of Tobin, with no fee or skill loss. Its corpse's things
  return to the pet. It still dies, so the lesson means something. Sera points pet ghosts to Tobin. The graduation
  box keeps its blessed elixir of rebirth (P480).
- **Shard-wide vets:** pinned's `Veterinarian` cannot resurrect at all (P480). P480's prompt draft (every vet brings
  pets back) is still the fix for the rest of the world, and the pup that died on 10-23 would have needed it.

## 9. Build plan (Golem prompts)

*Superseded by section 13 (10-26): the full prompt drafts, with private copies in F4.*

| # | Prompt | Touches | Notes |
|---|---|---|---|
| F1 | The Fold: map 32 on Trammel's file, the `FoldRegion` rules, the Trammel mirror guard, `[Tutorial goto` | server | First check: register map 32 before world load (customization or a json patch). A fact moves a player to 32 and back; a TazUO shot shows Trammel's tiles |
| F2 | The Wakening Isle, map work: land, shore, road, decor, buildings (shrine, bank, lodge, pier) and the vision chamber, by the playbook's pipeline, with the render rounds | map, package | The `trammel.mapops` lines; the player package and the server overlay rebuilt. Can ship before F3: nobody can see void C |
| F3 | The tutorial moves to the isle: the greeter and menu, the new order (travel last, farm in line, pet pick at the farm), the seeder on map 32, the farm addon and the vet moved, the start choice and skip at creation, Rook's remedial to the isle, the moved-in-progress rule | server, cliloc (package) | Needs F1 and F2 |
| F4 | Private visibility: the `CanSee` hooks, party sight, owned lesson items and corpses | server (one patch) | Ships with F3: the isle without it is the crowded plaza again |
| F5 | The vision scene and the chamber slot pool (maps 33+, the League's pool) | server | After F3; panels added later when Chase draws them (package) |
| F6 | Young pet protection on the isle, and P480's "every vet brings pets back" | server, one patch | Independent |

**Must ship together in one player package:** F2's map patch and F3's cliloc lines. F3 and F4 must go live
together. Nothing goes live until F1 to F4 have played through on a private world (P289's bot route, plus TazUO
shots).

## For Chase

1. **The pick** (asked): the Fold (recommended), A, B, C or another.
2. **How private** (asked): (iii) the mix (recommended), (i) or (ii).
3. Names: "the Fold", "the Wakening Isle", the greeter "Tamsin". Rename freely.
4. The loop line: P371 made Haven Island loop 0 until graduation. The isle sits before Haven Island, and the island
   gate stays as built, so nothing changes there. A trainee who walks out of the moongate is still loop 0 until Rook
   graduates them.
5. A skip from the creation screen earns "Didn't Read the Manual", as P371's skip does. Keep, or give the
   creation-screen skip no achievement?

## Checks and limits

- Counted here: void C's 215,040 cells (all 0x0244 at Z 0, 0 statics), Trammel file 7.0.117.0 in
  `D:\UO\UltimaOnlineVanilla`. Walks: B and C's real legs over the same files. Spawners near B: pinned
  `Distribution/Data/Spawns/post-uoml` read with a script (listed above).
- **Unverified:**
  - that a customization can register map 32 before regions and the world load (F1's first check);
  - how TazUO places the Tutorial Island button for display coordinates south of Haven, until it is seen in a
    client;
  - that the borderless subtitle gump sits centred in a resized TazUO window;
  - the sounds by ear (each was chosen by its pinned spell, not listened to);
  - the isle's 165 tiles and option A's 70, which are counted on sketches, not built maps.
- Research for sections 3 and 7 was done by two read-only helper agents. Their citations were spot-checked
  (`MapLoader.cs:33-41`, `TileMatrix.cs:79-86`, the map definitions, `CharacterCreation.cs`), not every one re-read.
- Nothing was run against live, the shared test shard or any shard; no lock was needed.

## Asked, and commit preflight

- Asked Chase through `Ask-Chase.ps1`, question `Iron-P481-20261025-060051-0bb2`. The choices are the Fold with the
  mix (recommended), A, B and C. The privacy alternative goes in his reply text if he wants it. The build prompts come
  after his answer.
- Docs (`D:\UO\golems\Iron\shard-migration`): this file and `notes\cc-P481-tools\` (two scripts, three plan files, six
  PNGs, the largest 513 KB). Code (`D:\UO\golems\Iron\ShatteredLegacy`): no change. No lock held, nothing running.

Chase answered on 10-25 at 20:05: **the Fold**. At 20:12 he asked to be shown the island's land before the build
prompts are written, and at 20:23-20:24 to look at every map we have (section 10).

## 10. Which land becomes the Wakening Isle (Chase 10-25 20:12-20:24)

### 10.1 How I looked

- **The maps.** Ten in all:
  - Six stock maps from the vanilla 7.0.117.0 client in `D:\UO\UltimaOnlineVanilla`: Felucca, Trammel, Ilshenar,
    Malas, Tokuno, Ter Mur.
  - The four downloaded maps in the art library's "Added facets and whole maps" section and the third-party
    README. I copied their data files only (map, staidx, statics: 12 files, about 410 MB) into
    `notes\cc-P481-tools\scratch\`. That folder is git-ignored (`notes\cc-P481-tools\.gitignore`, and `*.mul`
    repo-wide, proven with `git check-ignore`). Nothing was run from `D:\UO\third-party`, and nothing is added to
    the package.
  - Each file's size matches its stated size exactly (196 bytes per 8x8 block). For example, Siege of Sosaria's
    Map1.mul is 89,915,392 bytes = 7168 x 4096.
- **The tools** (in `notes\cc-P481-tools\`):
  - `islands.py`. Reads stock UOP or downloaded MUL land and the statics, colours each tile the way the radar map
    does, and finds every dry patch on a 4x4-tile grid, so sizes are good to about 4 tiles. A tile is water when its
    land or topmost static is Wet in tiledata, and void when it is 0x0244 or NoDraw with nothing on it.
  - A patch counts as an island when at least 80% of its border is water. A void border means a dungeon or staff
    area.
  - Each island is tagged with the pinned regions it touches (`Distribution/Data/regions.json`) and the teleporters
    that land on it (`teleporters.json`).
  - `iso.py` draws a patch as the classic client lays it out, through `scripts\mapbuild\isorender.py`.
  - `compose.py` builds the comparison sheet.
- **The pictures** (`notes\cc-P481-tools\island-candidates\`; the scratch renders stay out of git):
  - `candidates.png` (743 KB): the three finalists side by side, from above and in-client style.
  - `where-trammel.png` and `where-sos.png`: whole-map locators with every island numbered. Red means no region and
    no teleporter.

### 10.2 What each map offers

| Map | Islands found | Usable for the isle? |
|---|---|---|
| Trammel (and Felucca, the same layout) | 33 | Seven unclaimed islands of 7,000-17,000 dry tiles. The best are **#16** (2008-2211 x 2056-2207, 204 x 152, forest and grass with a sandy cove) and #23 (2392-2543 x 3872-4047). #174 (6396-6471 x 1208-1291) is a sand island with a cave, alone in a sea square among the dungeon blocks: a real unused corner, but 76 x 84, too small for the road |
| Ilshenar | 3 | No: Spectre's entrance, the Ancient Citadel, and one 28 x 28 rock |
| Malas | 0 | No |
| Tokuno | 10 | No: the largest is 152 x 56 (3,920 dry tiles) |
| Ter Mur | 14 | No: the unclaimed patches in its middle are river-cut jungle in the Valley of Eodon, which is live Time of Legends content, not islands |
| Siege of Sosaria (Zigholtul) | 97 | Several new islands. The best is **#51, the "Isle of Colossus"** in the author's own Regions.xml: 1832-2079 x 1656-1851, 248 x 196, 27,280 dry tiles, 15,376 statics. #99 is shaped like a rooster (a joke island), #179 is unfinished bare dirt, and #155 (360 x 252) hugs the mainland |
| Dungeon map 4 (TheArt) | 1 | No: an undecorated cave map |
| Ter Mur replacement (TheArt) | 6 | No: mostly blank blobs (five of the six islands carry 851-2,342 statics on 6,000-50,000 dry tiles; the sixth, its one built town, 11,000) |
| ParanoiaPhD custom map | 12 | No: rough painted landmasses (recognisably Britain and Ireland) with blanket ground cover |

Every count above is from the scripts' CSVs (`scratch\<map>-islands.csv`). The "island" test is mine: it is a
candidate list, not a census of every islet.

### 10.3 The three finalists, best first

| | 1. Isle of Colossus (Siege of Sosaria #51), **recommended** | 2. Forest isle south-east of Britain (Trammel #16) | 3. A new island painted in void C |
|---|---|---|---|
| Look | Finished and hand-decorated: mixed woods, a rock-ringed pond with a footbridge, rocky hills, paths, a cave mouth | Natural but plain: grass rim, dense forest heart, a sandy cove on the south side, nothing built | Whatever we paint (this morning's sketch: about 200 x 90 on the diagonal) |
| Size | 248 x 196 (27,280 dry tiles) | 204 x 152 (15,504) | about 200 x 90 |
| Today | On no stock map. In Siege of Sosaria it is a named region with no town | On every Trammel and Felucca map. No pinned region and no teleporter; players can sail to it on Trammel | Nothing: void C is 215,040 empty cells |
| Art | 188 distinct statics and 146 land tiles, **all in the stock client** (checked against `artidx.mul`; land IDs up to 0x305) | 96 statics and 90 land tiles, all stock | Stock, by the playbook |
| How players get it | The Fold's plan as written: the island's land and statics are copied into **void C** of Trammel's file, as lines in `trammel.mapops`, the patch the package already ships | **Nothing new:** the Fold (map 32 on Trammel's file) already shows it. Every building is a server item on map 32, so nothing changes on Trammel | As 1, but the island is painted rather than copied |
| Patch size | About 1.5 MB more patch text. A 280 x 230 box with its sea is 64,400 land lines at the file's measured 18.7 bytes, plus 15,376 static lines at 21.6 bytes. Today's `trammel.mapops` is 253 KB. Under the 5 MB rule. The `R` (fill) op from section 3.1 would cut the sea's share | 0 | About 1 MB plus the decor (section 3.1) |
| Map work | One prompt: copy, place in void C (the zone plan shifts a little: zone 1 grows to about 280 x 230 and the vision chamber moves east), then the road and the lesson buildings | None for land; the road and the buildings as server items | The most: land, shore, decor and buildings, with render rounds |
| Licence | The author: "feel free to take advantage to your hearts content". No licence file. Credit Zigholtul; ship only inside the package | EA's own map, already on every PC | Ours |
| Catch | A copy of someone else's island (credited); its cave mouth and colossus theme hint at content we don't have (dress it, or block the cave) | A sailor on Trammel can find its twin, an empty island shaped like the tutorial isle | Time, and art judgement round by round |

**Why 1:** it is the only candidate that already looks like a place someone made, it is big enough for the
165-tile road with room for the farm, it needs no new client files, and its copy cost is one prompt and about 1.5
MB of patch text. If you would rather not use someone else's island, 2 is the zero-cost fallback.

**Unverified:**
- How #51's shore and cliffs look in a real client (the renders are `isorender`'s classic layout, without hues).
- That nothing in Siege of Sosaria's statics depends on its own hue or verdata files. All IDs exist in stock
  `artidx.mul`, but a stock tile could still be drawn with an author's hue.
- Whether its cave mouth leads anywhere in the author's map. It is outside the copy box either way.

## Asked, and commit preflight

- The first question, `Iron-P481-20261025-060051-0bb2` (the Fold), was answered on 10-25.
- The island question went to Chase through `Ask-Chase.ps1`, question `Iron-P481-20261025-212706-1405`: use the Isle of Colossus (recommended), look for
  another, or make a new one. F1 to F6 come after his answer, folding in Codex's review
  (`notes\cc-P605-start-area-design-review.md`, owned interactions against full copies) as the overseer asked.
- Docs (`D:\UO\golems\Iron\shard-migration`): this file and `notes\cc-P481-tools\` (new: `islands.py`, `iso.py`,
  `compose.py`, `.gitignore`, `island-candidates\` with three PNGs under 1 MB). Scratch: `notes\cc-P481-tools\scratch\`
  (git-ignored). Code (`D:\UO\golems\Iron\ShatteredLegacy`): no change. No lock held, nothing running.

Chase answered on 10-26 at 12:37: **make a new one**. The Isle of Colossus has too few flat places for the farm.
Paint a new island in the Fold's empty corner, built for the tutorial: a flat farm meadow, the training and trades
yards, a dock, with the one-way route laid out first. Then write F1 to F6 (sections 11 to 13).

## 11. The new Wakening Isle (Chase 10-26)

### 11.1 The pictures (`notes\cc-P481-tools\new-isle\`, drawn by `notes\cc-P481-tools\newisle.py`)

| File | What it shows |
|---|---|
| `plan.png` | **The island, top-down:** stops 0 to 10, the walked road (white), the walk inside the farm (yellow), the zones |
| `where.png` | Where it sits in void C, with the Fold's other zones |
| `iso-farm.png` | In-client style mock (`isorender`): the road and the flat meadow with P276's farm moved onto it whole |
| `iso-east.png` | In-client style mock: the trades square and bank, the League lodge, the stones on their knoll, the dock and moongate |
| `legs.txt` | Every leg's walked length, and the counts below |

The script reads only the vanilla client files (`MAPBUILD_CLIENT=D:/UO/UltimaOnlineVanilla`, `MAPBUILD_ART` as for
`isorender`) and the farm layout from the code work copy (`TutorialFarmLayout.cs`). It writes no map file. The
mocks have no shore transitions, no hues and no roofs on the bank and lodge, so the lessons inside show. F2 builds
the real tiles through the playbook.

### 11.2 The plan

The route was laid first, as Chase asked: a road of 18 waypoints, three tiles wide, west to east. The island was then
shaped round it: every tile within about 11 tiles of the road, plus eight round lobes for the meadow, the yards, the
knoll and two wooded hills to the north. The shore is a 4-tile sand rim. All of it is flat Z 0 except the knoll,
which rises to Z 8 under the stones.

| | Where (Trammel file, void C) | Size |
|---|---|---|
| Walkable land and dock | x 6202-6409, y 1938-2026 | 208 x 89 (9,184 dry tiles) |
| Drawn area with its sea | x 6170-6441, y 1913-2057 | 272 x 145 (39,440 cells) |
| Sea margin | at least 24 tiles past every walkable tile, more than the client's view range, so no one on the isle sees the void's black edge or another zone | |

The Fold's zones (section 3.2) still fit round it: zone 1 is now the box above. The vision chamber (zone 2, 6440-6463 x
1850-1873) is 40 tiles north of the isle's sea and 31 tiles east of the dock's tip. Under section 12's
recommendation the vision no longer needs it, so zone 2 is free for later.

| Stop | Place (x, y) | Leg walked | Lesson |
|---|---|---|---|
| 0 | West beach (6214, 2001): the player wakes; Tamsin the guide | - | arrival, the core menu |
| 1 | Two bright tiles in the road (6222, 2000) | 8 | `core.movement` |
| 2 | A camp beside the road (6232, 1998): campfire, bedrolls, the blue bag | 10 | `core.backpack` |
| 3 | A clothes rack (6241, 2000) | 9 | `core.paperdoll` |
| 4 | A signpost at the meadow's edge (6268, 1998) | 27 | `core.chat` |
| 5 | The farm gate (6290, 1987): Wren, Tobin the vet just outside; inside, the pet pick, the pests, the bandages | 28 | the farm (section 12.3 says how it joins the core) |
| 6 | The training yard (6312, 2003): a low fence, four training dummies, an archery butte; the pale echo, Sera and an ankh | 23 | `core.death` |
| 7 | The trades square (6338, 1989): cobbles, a forge, an anvil, a loom; the practice bank's door (Merrin inside) | 27 | `core.banking` |
| 8 | The League lodge door (6358, 2002): Elara inside | 20 | `core.league` (open the door) |
| 9 | The standing stones on the knoll (6370, 1990) | 12 | `core.loop`, the vision |
| 10 | The dock's end (6407, 1999): the moongate | 37 | `core.travel`: out to New Haven beside Rook |

- **Walked:** 201 tiles from the beach to the moongate, plus 20 inside the farm (gate, crop rows, the pen fence, back
  to the gate). Legs were walked on the sketch: 8 directions, no diagonal past a blocked corner, fences, walls, trees,
  dummies and stones blocking, gates and doors open. Among equal walks the road is preferred.
- **This corrects two of P605's points about the first sketch.** Its legs summed to 185, not the 165 I wrote. Its walk
  allowed diagonals past blocked corners, and its square was 221 wide. The 201 here is measured with those fixed.
  It is still a sketch: F2's built map is walked again, with doors and lesson detours.
- **One direction:** every stop is ahead of the last. The only steps back are in and out of a gate or door, at the
  farm, the yard, the bank and the lodge.
- **The farm, moved whole:** all 334 pieces of P276's approved layout (`TutorialFarmLayout.cs`, x 3372-3401, y 2603-2619),
  shifted by (+2890, -628) to x 6262-6291, y 1975-1991, inside a flat meadow of 41 x 30 (x 6252-6292, y 1966-1995).
  Its gate stays on the east side, toward the road. Each piece keeps its height above the old ground. That ground ran
  from Z 3 to 45 in New Haven; none of the 334 pieces sat below it, so none is clipped. The farmhouse door goes on as
  a real door, as P276 placed it.
- **The yards:** the training yard (x 6302-6324, y 2002-2018) holds the death lesson, with room for later combat
  tasters. The trades square (x 6330-6350, y 1979-1996) holds the bank, with room for later trade tasters. These are
  the "training and trades yards" Chase named. Only the core lessons use them in F3.
- **Art in the mocks** (all stock, from tiledata names): the farm's own pieces; stone walls 0x001A along x, 0x001B along
  y, 0x001C corner, 0x001D post. That order was picked from a 5 x 5 test room; the swapped order rendered as loose
  slabs. Also wooden boards 0x04A9, cobbles 0x0442-0x0445, fence 0x0836/0x0837 (the farm's), training dummies 0x1070
  and 0x1074, archery butte 0x100A, forge 0x0FB1, anvil 0x0FAF, loom 0x1049/0x104A, rocks 0x1772 for the stones,
  ankh 0x0003, planks 0x04A1, dock poles 0x01CD, moongate 0x0F6C (a server item in the build). Trees: oak, walnut and
  cedar pairs.

### 11.3 What it costs in the package

- **Patch text:** every cell in the drawn area changes from void to sea or land: 39,440 `L` lines at the measured
  18.7 bytes, about 0.74 MB. The sketch has 1,127 statics. The built isle with decor is estimated at 3,000 to 5,000
  `S+` lines at 21.6 bytes, 0.07 to 0.11 MB. So `trammel.mapops` grows by about 0.8 to 0.9 MB, under the 5 MB rule.
- **Correction (P605):** the player's `statics1.mul` does grow. `Apply-MapOps.ps1` appends the changed static blocks
  and repoints the index. With about 5,000 statics at 7 bytes, plus about 650 touched blocks, that is under 50 KB. The
  map file's size does not change. "No new client files" means no new facet files and no client change. Players
  still need the package update that carries the patch and the cliloc lines; a stale package shows the old void.

## 12. Privacy, priced: the mix against full copies (P605)

P605 split the promise in two: other trainees are hidden, and other trainees cannot interrupt your lesson. The mix
(section 5, (iii)) gives the first easily. The second needs every shared interactive thing on the isle to be owned
by one trainee. Here is that list against today's code, and the same list for full copies.

### 12.1 What sharing breaks, and what it costs to fix

| Shared thing on one isle | What goes wrong | Fix under the mix | Under copies |
|---|---|---|---|
| Farm pests | `TutorialCreature.cs:35` admits any active trainee; `TutorialFarm.cs:242` credits everyone who hit a dying pest; `:402` seeds shared spawners. Hidden trainees fight over one pest and see it vanish | Per-trainee spawns on demand, owned, hidden from others, cleaned up on leave; credit only the owner | Nothing: the copy's pests are yours |
| The pale echo | One echo for everyone; it can be fighting another trainee | Spawn one owned echo per trainee | Nothing |
| The lodge door | A door's open or closed state is shared; a closed door hidden or not still blocks movement | Accept a door that moves by itself, or replace the door lesson | Nothing |
| NPC replies | One public `Say` today (`TutorialRecruiter.cs`); a shared greeter's reply reaches everyone who can see the greeter | `SayTo` / private messages for every lesson NPC | Nothing (P605's rule is still good practice) |
| Effects and sounds | Location effects and sounds reach every client in range (`Effects.cs:66-77, :168`); the walking-tile sparkles use them | Send each lesson effect to the one NetState | Nothing |
| Others' pets and summons | Hidden mobiles still occupy tiles; whether one blocks you depends on movement rules, not sight | Make tutorial pets pass-through, or accept bumps | Nothing |
| The vision | Its sounds, lights and figures | A private chamber copy (a slot pool), or private-everything at the stones | Plays in place at the stones, on your copy |
| Hiding itself | The `CanSee` hooks (`PlayerMobile.cs:3239, 3282`) with party, staff, corpse and ghost rules, ordered against the existing visibility list (P605 risk 1) | Needed | Not needed |

### 12.2 What copies cost

| Cost | Size |
|---|---|
| Memory per copy | Small. Pinned allocates a map's sector array and its tile-block arrays as columns are first used (`Map.cs:88, 1447`; `TileMatrix.cs`). Matrices on one file index link to each other's caches (`TileMatrix.cs:79-86`). Each copy still opens its own three file streams (map, index, statics). **Unverified:** a measured number; F1 measures it |
| Objects per copy | The farm addon (334 pieces), about eight lesson NPCs, the farm's animals and pests, the lesson props: about 400 items and 15 mobiles, saved with the world while a copy is seeded |
| Map indexes | One per copy, reserved forever once a save can name it (P605). A pool of 16 at map 33 to 48, raised later if ever full |
| A slot manager | Give a free copy to a trainee, or to a party's leader with the members; hold it while anyone is inside, online or not; free it and reseed it when empty |
| A logout rule | Every copy has the same coordinates. A trainee who logs back in after their copy was freed goes to a fresh copy at the stop of their first undone lesson. No queue for "your" copy |
| Staff | `[Tutorial goto <n>`, and a list of copies in use |

**Settled: full copies, one per trainee or party** (the old (ii), on the Fold's shared tiles). The mix needs the
ownership work above plus the visibility hooks plus a vision pool. Copies need a pool too, and nothing else. Once each
copy shares the Trammel tiles, the remaining cost is seeding and resetting about 400 items, which the seeder already
does once. Copies also remove the bug classes outright (shared pests, the door, stray sounds, invisible blockers)
instead of patching each one. They match the League's private trial maps (storyline decided 5), so the pool is
built once. This changes Chase's lean of 10-23 (the mix), so it is his to confirm before F4 (see "For Chase"). If
he keeps the mix, F4's alternative text below is the larger build.

### 12.3 Other P605 corrections folded into the prompts

- **Map startup:** a customization `Configure` with an explicit priority runs after pinned's `MapLoader.Configure`
  (priority 2) and before regions and `World.Load` (`Main.cs:667`, `Attributes.cs:40`). So the Fold registers in code
  with no JSON patch (F1).
- **Hard-coded Trammel:** 18 `Map.Trammel` uses in the core lesson files (`TutorialCorePlacement.cs` 8,
  `TutorialCoreTrials.cs` 4, `TutorialFarm.cs` 4, `TutorialRecruiter.cs` 1, `TutorialIslandGate.cs` 1; counted today
  on code HEAD 3b4d321). The trade and wing trials (15 more) stay in New Haven. F3 routes the core 18 through the
  trainee's own lesson map.
- **The farm is optional today** (`TutorialFarm.cs:52`; `CoreDone` and `Graduate` need only core stations). Putting it
  in line needs a rule. Proposal: a new core station `core.farm` (pick the pet, clear the pests, use the bandages),
  so the arrow does not skip it. The pet pick then moves from graduation to the farm (dog or cat). An account that
  already has its pet skips the pick. That is Chase's 11:18 intent, stated so he can see the trade.
- **The travel item answers a double-click** (`TutorialCorePlacement.cs:174`), not a step. The moongate takes both.
- **Supplies are not persistent:** login cancels the active trial, and the bag, cloak and token delete themselves on
  load. Keep that: a reconnect regenerates the current lesson's supply.
- **Pets cross maps only when moved.** `MoveToWorld` takes carried items, not followers; stock moongates call
  `BaseCreature.TeleportPets`, which has range and order limits. Every Fold crossing (arrival into a copy, the dock
  moongate out, Rook's remedial trip in) moves all the trainee's controlled pets on the Fold with them, whatever the
  range.
- **The island gate:** `TutorialIslandGate.cs` and `PlayerMobile-tutorial-island-gate.patch` treat any destination
  outside Haven and Rootdeep as leaving the island. Rook's remedial trip to the Fold needs an explicit allowed route.
- **Account eligibility** needs a full rule (F3's table).
- **Skip wording:** a creation-screen skip gives no *tutorial graduation* box. The loop box still comes from
  `ClusterFLoops` -> `ClusterFLootBoxes.OnLoopCompleted`.
- **Light is not a guaranteed blackout:** client light settings can override server light (TazUO `LightLevel.cs`,
  `PersonalLightLevel.cs`). The scene tries `NetState.SendScreenEffect` for fades. Its subtitles must make sense
  with lighting overridden.
- **No stock `Clone`:** the echo figure copies appearance only. Pinned's Mirror Image clone copies skills, follows,
  times out and registers itself.
- **A restart mid-scene:** the scene saves enough to return the player to the stones, unfrozen, with the light
  restored, at startup or the next login.
- **Tobin today** charges Young owners 0, but refuses an existing corpse and takes 0.2 from every skill
  (`TutorialPetCare.cs`). Free, lossless revival on the isle is new behaviour (F6).

## 13. Build prompts F1 to F6 (drafts for the overseer to number)

Order: F1, then F2 and F3 (F3 needs F1; F2 can ship first, since nobody can see void C), then F4, then F5 and F6.
**Must ship together:** F2's map patch and F3's cliloc lines in one player package. F3 and F4 go live together
(the isle without copies is a crowded shared isle). Nothing goes live until F1 to F4 have played through on a
private world with two clients.

---

### F1. The Fold: map 32, its rules and the copy pool's indexes

**Model:** Opus

**Touches:** server

**Summary:** Register the Fold (server map 32, client id 1, file index 1, Trammel's tiles) and the tutorial copy maps
(33 to 48, same files) in code, with their region rules, and prove a player can stand there, save, reload and come
back. Design: `notes\cc-P481-new-player-start-area-design.md` sections 3.1, 11 and 12 (shard-migration).

**Read first:** that design, P605 (`notes\cc-P605-start-area-design-review.md`) risk 8 and "What holds up", pinned
`Projects/Server/Maps/MapLoader.cs`, `Map.cs`, `TileMatrix/TileMatrix.cs`, `Main.cs:667`, `Attributes.cs:40`.

1. A customization registers maps 32 to 48 in `Map.Maps` and `Map.AllMaps`, in a `Configure` with an explicit
   priority after `MapLoader.Configure` (2) and before world load: `TrammelRules`, season 0, names "TheFold" and
   "TheFold 1" to "TheFold 16". Indexes 32 to 48 are reserved for good; say so in a comment and in the design.
2. Regions on every Fold map: no housing, no recall, mark or gate in or out (`CheckTravel`, the Green Acres model), and
   always-day light. A `FoldMirrorRegion` on Trammel over void C sends any non-staff player found there to New Haven.
3. `[Fold goto <n> [x y]` for staff, test shard only to start.
4. Facts, each seen failing first: a player moved to 32 and to 40 stands on Trammel's tile and Z at that spot;
   housing, recall and gate are refused there; a save and reload keeps a character on map 40; an unregistered index
   in a save is reported, not crashed on. Measure the memory and file handles of 16 empty copies and one copy with a
   seeded farm, and write the numbers in the notes.
5. A TazUO shot on the private world, two characters on 32 and 33: each sees Trammel's void C (black until F2), not
   Felucca.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. Staff CHANGELOG line. Notes, last line `P<nn> DONE`.

---

### F2. The Wakening Isle, map work

**Model:** Opus

**Touches:** map, package

**Summary:** Paint the new island into void C of the Trammel files by `notes\map-building-playbook.md`: land, shore,
road, meadow, yards, square, bank, lodge, knoll, dock, and decor, following the approved plan
(`notes\cc-P481-tools\new-isle\plan.png`, coordinates in design section 11.2). Ship it as `trammel.mapops` lines for
the package and the server overlay.

**Read first:** the playbook (all of it), design section 11, `notes\cc-P481-tools\newisle.py` (the plan's
coordinates, to import or copy), `notes\cc-P167-tools\build_burrows.py` (the driver's shape).

1. A driver `notes\cc-P<nn>-tools\build_isle.py` with `--fresh` and `--plan-only`, one seeded random stream per stage.
   Sea over the whole drawn area (x 6170-6441, y 1913-2057), shore with stock sand-to-water and grass-to-sand
   transitions (audit them with vseUOAware `diagnose_land_transitions`), the road and meadow flat at Z 0, the knoll to
   Z 8 with the slope audit clean.
2. The bank and lodge as stone buildings with roofs, doors framed, every corner dressed (playbook section 4); the
   training yard and the meadow fenced; the dock of planks with poles; woods on the north hills at 5 to 12 pieces per
   100 tiles. The farm addon and every NPC, door and moongate stay server items (F3), not statics.
3. The walkable gate: walk the built map from the beach to the dock with pinned's movement rules reduced to the files.
   Record each leg in a table beside design 11.2's sketch numbers.
4. The playbook's checklist table and junction sheet in the notes; the picture set in `notes\art\wakening-isle\`:
   top-down, every zone, the shore, the bank and lodge in-client style. Chase approves the renders before the patch
   ships.
5. `mapops.py diff` to `player-package\vendor\shattered-legacy-map\trammel.mapops`; `check` reads drifted 0, missing 0.
   Report the patch's size. `tools\tests\test_mapops.py`, the package's map gate and `Map-Overrides.Tests.ps1` green.
   Take the `package` lock for any package build.
6. Notes, last line `P<nn> DONE`. No CHANGELOG line until F3 makes it reachable.

---

### F3. The tutorial moves to the isle, with the start choice

**Model:** Opus

**Touches:** server, package (cliloc)

**Summary:** Move the core tutorial from the New Haven plaza to the Wakening Isle, in one line west to east (design
11.2), with the farm as a core station, the dock moongate as the last lesson, and a start choice at character
creation. Single-copy for now (map 32); F4 adds the copies, so every lookup goes through the trainee's lesson map.

**Read first:** design sections 4, 7, 11 and 12.3; P605 risks 3, 4 and 5; P289, P371, P475, P480, P276 notes;
`server\customizations\Tutorial\*.cs`; `CharacterCreation.cs`.

1. **One lesson map.** A `TutorialWorld.MapOf(PlayerMobile)` (32 now; F4 returns the trainee's copy) replaces the 18
   core `Map.Trammel` uses (design 12.3 lists them). The wing and trade trials stay on Trammel.
2. **The seeder on the isle:** Tamsin (the core menu, Rook's core role, directed replies with `SayTo`), the lesson
   props at design 11.2's stops, Wren, Tobin, Sera, the pale echo, Merrin and a practice bank box, Elara in the lodge,
   the stones, the dock moongate (walk in or double-click). The farm addon moves with its pieces' heights above the
   old ground kept (design 11.2); its door and pen as P276 placed them.
3. **The order:** movement, backpack, paperdoll, chat, `core.farm` (new: pet pick, pests, bandages; an account that
   has its pet skips the pick), death, banking, league, loop (the vision as built today until F5), travel last. A
   character partway through keeps its done keys and resumes at its first undone stop; old-order travel counts only
   once the rest are done.
4. **Pets cross with the trainee** on every Fold crossing: all controlled pets on the Fold, whatever the range.
5. **The start choice:** two city entries, "Tutorial Island" (index 0, default; display coordinates in the sea south
   of Haven Island) and "New Haven" (skip), both sent as Trammel; cliloc descriptions in the package. The choice is
   stored on the new character and consumed once at its first login.
6. **Eligibility,** decided per account and character:

   | Account state | "Tutorial Island" chosen | "New Haven" chosen |
   |---|---|---|
   | Fresh (NotStarted) | isle, entered on this character | skip (P371: Skipped, loop 1, "Didn't Read the Manual", no tutorial graduation box) |
   | InCore on another character | New Haven, told the tutorial is with that character | New Haven |
   | Graduated or Skipped | New Haven; Rook offers Remedial training | New Haven |
   | Tutorial character deleted mid-core | isle, re-bound to this character, done keys kept | skip |
   | Created before go-live | never entered or moved (P80 item 1) | - |

7. **Remedial:** Rook's button sends a skipper to the isle's beach, through an allowed route past the island gate
   patch; the dock moongate brings them back to Rook, who gives the box and the second achievement as today.
8. Facts, each seen failing first: the order; a pet crossing the dock; each row of the eligibility table; a choice
   surviving a disconnect before first login; a second character not consuming another's choice; the moongate by step
   and by double-click; a reconnect regenerating the current supply. Then the P289 bot route on a private world with
   the isle loaded, and TazUO shots of the city screen and five stops.
9. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. CHANGELOG player lines (test shard only until F4 ships). Notes,
   last line `P<nn> DONE`.

---

### F4. Private copies of the isle

**Model:** Opus

**Touches:** server

**Summary:** Each trainee, or a party, gets a private copy of the Wakening Isle (maps 33 to 48 from F1), seeded on
first use and reset when empty, so nobody else's pests, doors, pets or sounds reach a lesson. Settled in design section
12 against the hidden-players mix; Chase confirms first.

**Read first:** design section 12, P605 risks 1, 2 and 6, F1's memory numbers.

1. A slot manager: assign a free copy at entry (a party's leader and members share one); hold it while anyone is
   inside, online or offline; free and reseed it after the last occupant has been gone 30 minutes; staff
   `[Tutorial copies` lists them. A trainee whose copy was freed goes to a fresh copy at their first undone stop.
2. `TutorialWorld.MapOf` returns the copy; the seeder seeds a copy on assignment, and removes exactly what it placed on
   reset (no stray items left on a reused copy).
3. When all 16 are in use, the next trainee waits on the beach of map 32 with a line saying so, and is moved when a
   copy frees. Report how often that would happen at today's sign-up rate.
4. Facts, each seen failing first: two trainees in two copies kill pests without crediting each other; a party shares
   one copy; logout and login inside a held copy; login after the copy was freed; a reset copy holds only fresh seeds;
   a save and restart with copies in use.
5. Two-client TazUO playthrough on the private world, solo and as a party.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. CHANGELOG player line. Notes, last line `P<nn> DONE`.

*If Chase keeps the mix instead:* one isle (map 32); `CanSee` hooks hiding other trainees, ordered against pinned's
visibility list and its staff, ghost and container checks; per-trainee owned pests and echo; `SayTo` replies; lesson
effects to one NetState; a decision on the lodge door; pass-through tutorial pets; and F5's chamber pool. Same facts,
plus two hidden trainees on one pest and one door. Expect it to be the larger prompt.

---

### F5. The vision as a staged scene

**Model:** Opus

**Touches:** server, package (panels later)

**Summary:** Replace the vision placeholder with the 45-second scene of design section 6, for one player, at the
standing stones of their own copy, with restart-safe recovery.

**Read first:** design section 6 (the storyboard) and 12.3; P605 risks 6 and 7; `docs\league-storyline.md` chapter 1;
`ClusterFLoops.cs`, `TutorialCoreTrials.cs`.

1. `TutorialVisionScene`: frozen, private light per player, fades with `SendScreenEffect` where the client honours
   it, centred subtitle gump that reads correctly with lighting overridden, the beats and effect and sound IDs of
   section 6, all sent to the one player.
2. The figures are plain mobiles that copy the player's appearance only (no Mirror Image `Clone`), deleted at the end.
3. Recovery: logout, death, disconnect or restart mid-scene returns the player to the stones, unfrozen, light
   restored, figures gone, scene replayable; the saved state survives a restart.
4. The scene changes no skill, level, loop or Young status (a fact, against the current check).
5. Two full-screen panel IDs reserved in the art registry for Chase's later drawings; the scene runs without them.
6. Facts, each seen failing first; a TazUO recording (frame burst) of the scene; sounds checked by ear on the private
   world.
7. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. CHANGELOG player line. Notes, last line `P<nn> DONE`.

---

### F6. Pets on the isle, and every vet brings pets back

**Model:** Opus

**Touches:** server, patch

**Summary:** On the isle a Young player's dead pet comes back free and whole at Tobin; Sera points pet ghosts to him;
a lesson line at the farm says what to do when a pet dies. Shard-wide, stock vets resurrect pets as P480 drafted.

**Read first:** design section 8 and 12.3; P480's notes and its "every vet" draft; `TutorialPetCare.cs`.

1. On any Fold map: a Young owner's pet ghost within 3 tiles of Tobin is resurrected free, with no skill loss, and
   its corpse's things go back to it. It still dies, so the lesson has meaning.
2. Off the isle: Tobin's rule today (free while Young, 0.2 skill loss) stays, unless Chase says otherwise.
3. Stock `Veterinarian` everywhere offers resurrection on ServUO's fee (P480's draft), so New Haven's stable vet and
   every town vet can bring a pet back.
4. Wren's and Sera's lines; the farm's pet lesson line.
5. Facts, each seen failing first: free and lossless on the isle; the fee and loss off it; a stock vet resurrects; a
   non-Young owner pays.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. CHANGELOG player lines. Notes, last line `P<nn> DONE`.

## For Chase (10-26)

1. **The island:** `notes\cc-P481-tools\new-isle\plan.png`, `iso-farm.png` and `iso-east.png`. Say if anything should
   move. F2 makes the real tiles and shows you its renders before anything ships.
2. **Private copies instead of the mix** (section 12): agree, or keep the mix. This is needed before F4 is queued,
   not before F1 to F3.
3. **The farm becomes a required lesson,** and the pet pick moves there from graduation (section 12.3). Agree, or keep
   the farm optional off to one side of the road.
4. Still open from 10-25: the names (the Fold, the Wakening Isle, Tamsin), and whether a creation-screen skip earns
   "Didn't Read the Manual".

## Checks, files and commit preflight (10-26)

- **Counted here:** the legs, sizes and tile counts in section 11 (`legs.txt`); the farm's 334 pieces and their
  ground (none below it); 18 core `Map.Trammel` uses on code HEAD 3b4d321; the one public `Say` in the tutorial NPCs.
  Read in pinned: `Map.cs:88, 1447` and `TileMatrix.cs:71-110` for the per-map allocations.
- **Unverified:** memory per copy (F1 measures it); every leg on a built map (F2 walks it); how the shore and the
  knoll look with real transitions; P605's citations not listed above, which this design folds in as written.
- **A repair, not part of the design:** the Golem's WIP commit `1777f59` (when P659 was claimed) recorded the deletion
  of 11 files that exist on main: `tools\decisions.py`, `tools\playwhere.py`, `tools\tests\test_decisions.py`,
  `tools\tests\test_play_who.py`, `notes\cc-P265-tools\proof.ps1`, `notes\cc-P480-tools\playthrough.py` and five P481
  scripts. Every one is a `.py` or `.ps1` script, which points to something outside git removing scripts from the
  work copy. I restored all 11 from `89fbbe2` (staged, not committed), so merging this branch does not delete them
  from main. Worth a look by the overseer.
- **Files (shard-migration):** this note; `notes\cc-P481-tools\newisle.py`; `notes\cc-P481-tools\new-isle\` (four PNGs,
  the largest 0.94 MB, and `legs.txt`); the 11 restored files. Code work copy: no change. Nothing was built, run on a
  shard, or sent to Haven, and no lock was needed.

P481 DONE
