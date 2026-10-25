# cc-P481: a secluded new player start area (design only)

## In plain words

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

P481 STOPPED: asked Chase (Iron-P481-20261025-060051-0bb2), waiting for Chase's pick
