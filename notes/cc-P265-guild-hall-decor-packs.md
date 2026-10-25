# cc-P265: guild hall decor packs, ready for the halls (registered and seedable, not placed)

## In plain words

- The art library's guild hall decor is now in the player package as 279 new pictures, none replacing a stock one: a
  bubbling alchemy vat, creature tanks, flasks and a crystal ball for the Order of the Alembic; a working blacksmith and
  a fire pit for the Society of Smiths; floating crystals and arc orbs for the Artificers; five round towers, marble
  railings and a ladder for any hall. Players see nothing new yet: nothing is placed in the world.
- Staff get four test-shard-only commands that lay out a guild's whole set from a template around a spot they pick
  ([DecorAlembicHall, [DecorSmithsHall, [DecorArtificersHall, [DecorHallStructure). On the live shard they refuse.
- On the way, this work found that adding one more start-up step could crash the server at start (a latent ModernUO
  ordering quirk); a small fix makes that start-up order fixed, and the server now starts every time.
- For you: the in-game screenshots are not taken yet (you asked for a stopping point; continuation prompt P374 does
  them). After merging: build and publish the player package, and say where the halls go (F-49) when you are ready.

## Status: PAUSED on 2026-10-21 (Chase asked for a stopping point)

Parts 1 to 3 are done, tested and green; part 4 (screenshots on a test shard) is left to `cc-P374-cont-guild-hall-
decor-proof.md` (see Continuation). The Iron Golem (Opus), branch `golem/Iron/P265` of both repos. Not committed (the
Golem commits). Image `sl-modernuo:cc-P265` = `92153e00c938`; `latest` untouched. The package was not built or published.
Nothing ran against the live shard or the shared test shard's world.

## Headlines

- **279 new art IDs, 0x6D70-0x6E86 (28016-28294), 179 pieces**, in the player package: registry rows, PNGs, 179 tiledata
  and 33 animdata records, the package `SOURCE.txt` section. The server's copy is `GuildHallDecorArt` (generated).
  - First art IDs above 0x4000 in our registry: the placeholder slots below are used up. The run 0x6D61-0x71F3 is free
    and empty (`find-free-art.py`), TazUO draws a PNG override before looking at the client's slot, and the client and
    server tile tables hold 65,536 statics. The package test fixtures were grown to reach these IDs (Tests).
- **Four seeders, one per guild plus the shared structure**, placing a template around a target point (or "here"),
  a group alone if named, skipping rows already standing at that point, `clear` removing only their own items.
  **Test shard only:** on a shard without `testCenter.enable`, place and clear refuse and change nothing.
- **The templates are data:** `design/guild-hall-decor/templates.json` (one row per item: piece or stock item, dx, dy,
  dz, hue), compiled into `GuildHallDecorTemplates.cs` by `decor.py layout`, with a test that the two match.
- **A boot crash found and fixed:** with this branch's one extra `Configure` method, the server stopped at start
  (`NullReferenceException: GumpActivator` in `VirtualCheck.Configure`). `VirtualCheckActivatorFirst.cs` fixes the
  order for good (section 5).
- **The multi-piece art was solved from the authors' previews** (section 2): the vat (9 parts), all five towers, the
  tank stands, the crystal ball and the railing corner, each checked in a client-geometry render.

## 1. The packs (part 1)

Read: `D:\UO\third-party\ART-LIBRARY.md` section 5 and its legend; each pack's `SOURCE.txt`; the two RedRooster `.txt`
notes; P34, P237, P243 notes (the registration path); P151's survey. Nothing was built or run from `third-party`.

| Pack | Library tags | Terms read | Decision |
|---|---|---|---|
| bubble-vat (Hestia) | disk | none stated (page has images only): community work, credit Hestia | used, all 33 files |
| creature-tanks (RedRooster) | CREDIT | "add me to Shard Credits List" | used, all 42 files |
| partialhue-flasks (Ems) | EA | none stated; files named by stock item IDs | used, 8 files, EA-derived |
| rooster-crystal-ball (RedRooster) | CREDIT | "add me to Shard Credits List" | used, all 9 files |
| blacksmith-shop (Apocalypse) | EA | none stated; frames cut from EA body 400 | used, 3 frames, EA-derived |
| mrriots-firepit (MrRiots) | disk | "Use and edit as you wish" | used, all 8 files |
| floating-crystals (MrRiots) | disk | "Use them as you please" | used, all 19 files |
| arc-orb-fx (otimpyre) | disk | none stated; shares his sources for remixing | used, the 27 game frames |
| marble-railings (OUTLANDSOwyn) | (SOURCE.txt: "check the page's terms") | page read 2026-10-21: "Feel free to use them in your own projects ... Please credit Outlands" | used, 70 new (2 were cc-P237's); EA-derived |
| hestia-large/medium/small/white-brick/white-column-tower (Hestia) | disk | none stated: community work, credit Hestia | used, 60 files |

**Skipped, and why:**
- `mad-scientist`: out by the prompt (its readme credits an unknown original author).
- arc-orb-fx `My Source Files\` (150 px sources) and the three GIF previews: not game art.
- Every preview JPG; the large tower's `Corel Auto-Preserve\DW a2ma.bmp` (an editor's autosave copy of DW a2ma).
- Marble railings 70321 and 70324: already shipped by cc-P237 as 15503 and 15504; the templates use those IDs.
- Nothing in these packs is tagged IP, and no readme forbids changes or redistribution. No pack is REG without a
  readable license: the railings' terms were missing from their SOURCE.txt, so I read the page (servuo.dev 2663).

**EA-derived pieces** (Ems' flasks, Apocalypse's blacksmith, and the marble railings, which their author says are
"based on the existing wooden assets") ship as P243's EA-derived trophies do: only as our PNG override inside the
player package, never as an EA file. Each registry row says so. P237 shipped two of the railings without that mark;
see Deviations.

## 2. How the multi-piece art fits

Tools: `notes\cc-P265-tools\` (`decor.py`, `first_templates.py`; scratch solvers in the session). The client draws a
static with its image centred on the tile and its bottom on the tile's bottom tip, 4 px up per z, in x+y then z order
(isorender's rules). Screen slots were measured in 22 px steps against each author's preview and turned into tiles
(x = (row + col) / 2, y = (row - col) / 2); every result was rendered and compared by eye.

- **Bubble vat (9 parts):** the back three, the three bubbling middles and the front three sit on a tile diamond
  around the centre: parts 1, 4, 6 at (-2,0), (-1,-1), (0,-2); 3, 5, 7 at (-1,0), (0,0), (0,-1); 2, 1i, 8 at (0,2),
  (1,1), (2,0). Matches Hestia's preview exactly. Parts 1-8 animate (a-d frames); 1i, the hueable front band, is still.
- **Creature tanks:** a stand is two tiles (S2 west, S1 east; E2 north, E1 south). The tank sits on the stand's S1 or
  E1 tile at z+5, as RedRooster's "height 5" says.
- **Crystal ball:** the cloth at z0, the ball (lit or unlit, animated) on it at z+1.
- **Towers:** each ring is a back row and a front row of wall pieces (large: 14 slots plus two door variants for the
  front centre; medium: 3 + 3, window and door variants; white towers: 5 + 5, window/door variants; small: back, two
  narrow sides, front). Caps: large top floor and turret at z20, medium turret at z28 one tile forward, small top at
  z22, white brick dome at z24, white column storeys every z22 with the dome on top. The white towers' back rows were
  matched in their previews; their sides were settled by a convexity search over every arrangement, then rendered.
- **Railings:** 70298 runs north-south, 70292 east-west, 70303 closes the west corner. Most other pieces are stair
  banisters (sloped); they are registered for a later stair.
- **Draw note:** a few tower caps sit on the front tile at a raised z so they draw after the walls. TazUO's own sorting
  should agree; the screenshots (P374) confirm it.

## 3. Registration (part 2)

Written by `notes\cc-P265-tools\decor.py` (registry first, then PNGs, then records):
- `registry.csv`: 279 rows (`what` names the guild and piece and frame; `source` the author, pack, page and file;
  `license` the author's terms and, where it applies, the EA-derived rule).
- `art\28016.png`-`28294.png` (1.9 MB): `scripts\anchor-art-frames.py --keep-geometry`, with `--black-transparent` for
  the black-background BMPs. Six sources were drawn on pure white (the large tower's top and turret, both white domes,
  the arc orb gate, the blacksmith): their border-connected white was made transparent first. The railings are
  UOFiddler PNG exports with their own alpha, re-encoded only. Nothing else changed.
- `records.json`: 179 tiledata records (one per piece, on its base ID; the light shape in the layer byte) and 33
  animdata records; its "about" text says where each value comes from: OSI's vat 0x1550, flask 0x182A, crystal balls
  0xE2D/0xE2E, fire pit 0x29FD, brazier 0x19AA, moongate 0xF6C, wooden banister 0x08AE, tall ladder 0x2FDE, stone wall
  0x001B, or RedRooster's own notes (tanks and crystal ball, with his frame timings). Every animated base carries
  Animation. Names are 19 ASCII characters at most.
- `SOURCE.txt` (the package's credits file): the set's section, by pack, with ranges, terms, what was not shipped.
- Server: `GuildHallDecorArt.cs` (generated), applied in `ShatteredLegacyArt.Apply`.

### The pieces

`Used` names the template groups that place the piece; a piece no template uses yet is registered for F-49.

| Pack | Piece | New ID(s) | Credit | Used | Record copies |
|---|---|---|---|---|---|
| bubble-vat | bubbling vat, part 1 of 9 (4 frames) | 0x6D70-0x6D73 (4 frames) | Hestia | alembic/vat | OSI's vat 0x1550 |
| bubble-vat | bubbling vat, part 2 of 9 (4 frames) | 0x6D74-0x6D77 (4 frames) | Hestia | alembic/vat | OSI's vat 0x1550 |
| bubble-vat | bubbling vat, part 3 of 9 (4 frames) | 0x6D78-0x6D7B (4 frames) | Hestia | alembic/vat | OSI's vat 0x1550 |
| bubble-vat | bubbling vat, part 4 of 9 (4 frames) | 0x6D7C-0x6D7F (4 frames) | Hestia | alembic/vat | OSI's vat 0x1550 |
| bubble-vat | bubbling vat, part 5 of 9 (4 frames) | 0x6D80-0x6D83 (4 frames) | Hestia | alembic/vat | OSI's vat 0x1550 |
| bubble-vat | bubbling vat, part 6 of 9 (4 frames) | 0x6D84-0x6D87 (4 frames) | Hestia | alembic/vat | OSI's vat 0x1550 |
| bubble-vat | bubbling vat, part 7 of 9 (4 frames) | 0x6D88-0x6D8B (4 frames) | Hestia | alembic/vat | OSI's vat 0x1550 |
| bubble-vat | bubbling vat, part 8 of 9 (4 frames) | 0x6D8C-0x6D8F (4 frames) | Hestia | alembic/vat | OSI's vat 0x1550 |
| bubble-vat | bubbling vat, the hueable front band (part 9 of 9) | 0x6D90 | Hestia | alembic/vat | OSI's vat 0x1550 |
| creature-tanks | tank stand, south facing, east half | 0x6D91 | RedRooster | alembic/tanks-north | RedRooster's own recommendation |
| creature-tanks | tank stand, south facing, west half | 0x6D92 | RedRooster | alembic/tanks-north | RedRooster's own recommendation |
| creature-tanks | tank stand, east facing, south half | 0x6D93 | RedRooster | alembic/tanks-west | RedRooster's own recommendation |
| creature-tanks | tank stand, east facing, north half | 0x6D94 | RedRooster | alembic/tanks-west | RedRooster's own recommendation |
| creature-tanks | creature tank: fish, south facing (4 frames) | 0x6D95-0x6D98 (4 frames) | RedRooster | alembic/tanks-north | RedRooster's own recommendation |
| creature-tanks | creature tank: fish, east facing (4 frames) | 0x6D99-0x6D9C (4 frames) | RedRooster | registered, not in a template yet | RedRooster's own recommendation |
| creature-tanks | creature tank: frog, south facing (3 frames) | 0x6D9D-0x6D9F (3 frames) | RedRooster | alembic/tanks-north | RedRooster's own recommendation |
| creature-tanks | creature tank: frog, east facing (3 frames) | 0x6DA0-0x6DA2 (3 frames) | RedRooster | registered, not in a template yet | RedRooster's own recommendation |
| creature-tanks | creature tank: hamster, south facing (2 frames) | 0x6DA3-0x6DA4 (2 frames) | RedRooster | alembic/tanks-north | RedRooster's own recommendation |
| creature-tanks | creature tank: hamster, east facing (2 frames) | 0x6DA5-0x6DA6 (2 frames) | RedRooster | registered, not in a template yet | RedRooster's own recommendation |
| creature-tanks | creature tank: lobster, south facing (2 frames) | 0x6DA7-0x6DA8 (2 frames) | RedRooster | alembic/tanks-north | RedRooster's own recommendation |
| creature-tanks | creature tank: lobster, east facing (2 frames) | 0x6DA9-0x6DAA (2 frames) | RedRooster | registered, not in a template yet | RedRooster's own recommendation |
| creature-tanks | creature tank: scorpion, south facing (2 frames) | 0x6DAB-0x6DAC (2 frames) | RedRooster | registered, not in a template yet | RedRooster's own recommendation |
| creature-tanks | creature tank: scorpion, east facing (2 frames) | 0x6DAD-0x6DAE (2 frames) | RedRooster | alembic/tanks-west | RedRooster's own recommendation |
| creature-tanks | creature tank: snake, south facing (2 frames) | 0x6DAF-0x6DB0 (2 frames) | RedRooster | registered, not in a template yet | RedRooster's own recommendation |
| creature-tanks | creature tank: snake, east facing (2 frames) | 0x6DB1-0x6DB2 (2 frames) | RedRooster | alembic/tanks-west | RedRooster's own recommendation |
| creature-tanks | creature tank: tarantula, south facing (2 frames) | 0x6DB3-0x6DB4 (2 frames) | RedRooster | registered, not in a template yet | RedRooster's own recommendation |
| creature-tanks | creature tank: tarantula, east facing (2 frames) | 0x6DB5-0x6DB6 (2 frames) | RedRooster | alembic/tanks-west | RedRooster's own recommendation |
| creature-tanks | creature tank: turtle, south facing (2 frames) | 0x6DB7-0x6DB8 (2 frames) | RedRooster | registered, not in a template yet | RedRooster's own recommendation |
| creature-tanks | creature tank: turtle, east facing (2 frames) | 0x6DB9-0x6DBA (2 frames) | RedRooster | alembic/tanks-west | RedRooster's own recommendation |
| partialhue-flasks | partial-hue flask 1 of 8 | 0x6DBB | Ems (EA-derived) | alembic/bench | OSI's flask 0x182A |
| partialhue-flasks | partial-hue flask 2 of 8 | 0x6DBC | Ems (EA-derived) | alembic/bench | OSI's flask 0x182A |
| partialhue-flasks | partial-hue flask 3 of 8 | 0x6DBD | Ems (EA-derived) | alembic/bench | OSI's flask 0x182A |
| partialhue-flasks | partial-hue flask 4 of 8 | 0x6DBE | Ems (EA-derived) | alembic/bench | OSI's flask 0x182A |
| partialhue-flasks | partial-hue flask 5 of 8 | 0x6DBF | Ems (EA-derived) | alembic/bench | OSI's flask 0x182A |
| partialhue-flasks | partial-hue flask 6 of 8 | 0x6DC0 | Ems (EA-derived) | alembic/bench | OSI's flask 0x182A |
| partialhue-flasks | partial-hue flask 7 of 8 | 0x6DC1 | Ems (EA-derived) | alembic/bench | OSI's flask 0x182A |
| partialhue-flasks | partial-hue flask 8 of 8 | 0x6DC2 | Ems (EA-derived) | alembic/bench | OSI's flask 0x182A |
| rooster-crystal-ball | crystal ball: the base cloth | 0x6DC3 | RedRooster | alembic/scrying | RedRooster's own recommendation |
| rooster-crystal-ball | crystal ball: unlit (4 frames) | 0x6DC4-0x6DC7 (4 frames) | RedRooster | registered, not in a template yet | RedRooster's recommendation |
| rooster-crystal-ball | crystal ball: lit (4 frames) | 0x6DC8-0x6DCB (4 frames) | RedRooster | alembic/scrying | as the unlit ball, plus LightSource and light 2 as OSI's lit crystal ball 0xE2E |
| blacksmith-shop | a blacksmith at work (3 frames) | 0x6DCC-0x6DCE (3 frames) | Apocalypse (EA-derived) | smiths/forge | Apocalypse's description |
| mrriots-firepit | fire pit, burning (7 frames) | 0x6DCF-0x6DD5 (7 frames) | MrRiots | smiths/forge | OSI's fire pit 0x29FD |
| mrriots-firepit | fire pit, cold | 0x6DD6 | MrRiots | smiths/forge | OSI's fire pit 0x29FD without Animation and LightSource |
| floating-crystals | crystal pillar, without its crystal | 0x6DD7 | MrRiots | artificers/gate | OSI's brazier 0x19AA |
| floating-crystals | floating crystal: green (9 frames) | 0x6DD8-0x6DE0 (9 frames) | MrRiots | artificers/gate | OSI's brazier 0x19AA |
| floating-crystals | floating crystal: purple (9 frames) | 0x6DE1-0x6DE9 (9 frames) | MrRiots | artificers/gate | OSI's brazier 0x19AA |
| arc-orb-fx | arc orb, gate version (9 frames) | 0x6DEA-0x6DF2 (9 frames) | otimpyre | artificers/gate | OSI's blue moongate 0xF6C |
| arc-orb-fx | arc orb, floor version (9 frames) | 0x6DF3-0x6DFB (9 frames) | otimpyre | artificers/gate | as the arc orb gate |
| arc-orb-fx | arc orb, item version (9 frames) | 0x6DFC-0x6E04 (9 frames) | otimpyre | artificers/gate | OSI's lit crystal ball 0xE2E |
| marble-railings | marble rail (his Item-70290) | 0x6E05 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70291) | 0x6E06 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70292) | 0x6E07 | OUTLANDSOwyn (Outlands) (EA-derived) | structure/balustrade | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70293) | 0x6E08 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70294) | 0x6E09 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70295) | 0x6E0A | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70296) | 0x6E0B | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70297) | 0x6E0C | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70298) | 0x6E0D | OUTLANDSOwyn (Outlands) (EA-derived) | structure/balustrade | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70299) | 0x6E0E | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70300) | 0x6E0F | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70301) | 0x6E10 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70302) | 0x6E11 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70303) | 0x6E12 | OUTLANDSOwyn (Outlands) (EA-derived) | structure/balustrade | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70304) | 0x6E13 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70305) | 0x6E14 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70306) | 0x6E15 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70307) | 0x6E16 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70308) | 0x6E17 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70309) | 0x6E18 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble rail (his Item-70310) | 0x6E19 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70311) | 0x6E1A | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70312) | 0x6E1B | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70313) | 0x6E1C | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70314) | 0x6E1D | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70315) | 0x6E1E | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70316) | 0x6E1F | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70317) | 0x6E20 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70318) | 0x6E21 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70319) | 0x6E22 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70320) | 0x6E23 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70322) | 0x6E24 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70323) | 0x6E25 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70325) | 0x6E26 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70326) | 0x6E27 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70327) | 0x6E28 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70328) | 0x6E29 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70329) | 0x6E2A | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70330) | 0x6E2B | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70331) | 0x6E2C | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70332) | 0x6E2D | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70333) | 0x6E2E | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70334) | 0x6E2F | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70335) | 0x6E30 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70336) | 0x6E31 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70337) | 0x6E32 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70338) | 0x6E33 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70339) | 0x6E34 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70340) | 0x6E35 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70341) | 0x6E36 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70342) | 0x6E37 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70343) | 0x6E38 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70344) | 0x6E39 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70345) | 0x6E3A | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70346) | 0x6E3B | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble banister (his Item-70347) | 0x6E3C | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70348) | 0x6E3D | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70349) | 0x6E3E | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70350) | 0x6E3F | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70351) | 0x6E40 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70352) | 0x6E41 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70353) | 0x6E42 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70354) | 0x6E43 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70355) | 0x6E44 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70356) | 0x6E45 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70357) | 0x6E46 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70358) | 0x6E47 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble post (his Item-70359) | 0x6E48 | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's wooden banister 0x08AE and wooden rail 0x087E |
| marble-railings | marble ladder (his Item-70388) | 0x6E49 | OUTLANDSOwyn (Outlands) (EA-derived) | structure/balustrade | OSI's tall ladder 0x2FDE |
| marble-railings | marble ladder (his Item-70389) | 0x6E4A | OUTLANDSOwyn (Outlands) (EA-derived) | registered, not in a template yet | OSI's tall ladder 0x2FDE |
| hestia-large-brick-tower | large brick tower wall (his DW 2a) | 0x6E4B | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW 2b) | 0x6E4C | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW 2c) | 0x6E4D | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW 2d) | 0x6E4E | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW 2e) | 0x6E4F | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW 2h) | 0x6E50 | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW 2J) | 0x6E51 | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW 2k) | 0x6E52 | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW a2f) | 0x6E53 | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW a2g) | 0x6E54 | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW a2i) | 0x6E55 | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW a2La) | 0x6E56 | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW a2ma) | 0x6E57 | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall (his DW a2Na) | 0x6E58 | Hestia | registered, not in a template yet | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall with a door (his DW 2Q) | 0x6E59 | Hestia | structure/tower-large | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower wall with a window (his DW a2p) | 0x6E5A | Hestia | registered, not in a template yet | OSI's stone wall 0x001B |
| hestia-large-brick-tower | large brick tower: the top floor (his temp 23a) | 0x6E5B | Hestia | registered, not in a template yet | ours: Roof \| ArticleA, height 0 |
| hestia-large-brick-tower | large brick tower: the hueable turret (his temp 28) | 0x6E5C | Hestia | structure/tower-large | ours: Roof \| ArticleA, height 0, plus PartialHue |
| hestia-medium-brick-tower | medium brick tower wall (his 1a) | 0x6E5D | Hestia | structure/tower-medium | OSI's stone wall 0x001B |
| hestia-medium-brick-tower | medium brick tower wall (his 1b) | 0x6E5E | Hestia | structure/tower-medium | OSI's stone wall 0x001B |
| hestia-medium-brick-tower | medium brick tower wall (his 1c) | 0x6E5F | Hestia | structure/tower-medium | OSI's stone wall 0x001B |
| hestia-medium-brick-tower | medium brick tower wall (his 1d) | 0x6E60 | Hestia | structure/tower-medium | OSI's stone wall 0x001B |
| hestia-medium-brick-tower | medium brick tower wall (his 1e) | 0x6E61 | Hestia | structure/tower-medium | OSI's stone wall 0x001B |
| hestia-medium-brick-tower | medium brick tower wall (his 1f) | 0x6E62 | Hestia | registered, not in a template yet | OSI's stone wall 0x001B |
| hestia-medium-brick-tower | medium brick tower wall with a window (his 1g) | 0x6E63 | Hestia | registered, not in a template yet | OSI's stone wall 0x001B |
| hestia-medium-brick-tower | medium brick tower wall with a door (his 1h) | 0x6E64 | Hestia | structure/tower-medium | OSI's stone wall 0x001B |
| hestia-medium-brick-tower | medium brick tower: the turret (his i) | 0x6E65 | Hestia | structure/tower-medium | ours: Roof \| ArticleA, height 0, plus PartialHue |
| hestia-small-brick-tower | small brick tower: front (his DW51 a1b) | 0x6E66 | Hestia | registered, not in a template yet | OSI's stone wall 0x001B |
| hestia-small-brick-tower | small brick tower: back (his DW51 a2a) | 0x6E67 | Hestia | structure/tower-small | OSI's stone wall 0x001B |
| hestia-small-brick-tower | small brick tower: west edge (his DW51 a3) | 0x6E68 | Hestia | structure/tower-small | OSI's stone wall 0x001B |
| hestia-small-brick-tower | small brick tower: east edge (his DW51 a4) | 0x6E69 | Hestia | structure/tower-small | OSI's stone wall 0x001B |
| hestia-small-brick-tower | small brick tower: front with a window (his DW51 a6b) | 0x6E6A | Hestia | registered, not in a template yet | OSI's stone wall 0x001B |
| hestia-small-brick-tower | small brick tower: front with a door (his DW51 a8) | 0x6E6B | Hestia | structure/tower-small | OSI's stone wall 0x001B |
| hestia-small-brick-tower | small brick tower: the crenellated top (his DW51 a7) | 0x6E6C | Hestia | structure/tower-small | ours: Roof \| ArticleA, height 0 |
| hestia-white-brick-tower | white brick tower wall (his 1) | 0x6E6D | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall (his 2) | 0x6E6E | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall (his 3) | 0x6E6F | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall (his 4) | 0x6E70 | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall (his 5) | 0x6E71 | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall (his 6) | 0x6E72 | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall (his 7) | 0x6E73 | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall (his 8) | 0x6E74 | Hestia | registered, not in a template yet | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall (his 9) | 0x6E75 | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall (his 10) | 0x6E76 | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall with a window (his 11) | 0x6E77 | Hestia | registered, not in a template yet | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower wall with a door (his 12) | 0x6E78 | Hestia | structure/tower-white-brick | OSI's stone wall 0x001B |
| hestia-white-brick-tower | white brick tower: the hueable dome (his template 31) | 0x6E79 | Hestia | structure/tower-white-brick | ours: Roof \| ArticleA, height 0, plus PartialHue |
| hestia-white-column-tower | white column tower wall (his 1) | 0x6E7A | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall (his 2) | 0x6E7B | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall (his 3) | 0x6E7C | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall (his 4) | 0x6E7D | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall (his 5) | 0x6E7E | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall (his 6) | 0x6E7F | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall (his 7) | 0x6E80 | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall (his 8) | 0x6E81 | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall (his 9) | 0x6E82 | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall (his 10) | 0x6E83 | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower wall with a door (his 11) | 0x6E84 | Hestia | structure/tower-white-column | OSI's stone wall 0x001B |
| hestia-white-column-tower | white column tower: the top floor (his template 13) | 0x6E85 | Hestia | registered, not in a template yet | ours: Roof \| ArticleA, height 0 |
| hestia-white-column-tower | white column tower: the hueable round turret (his template 22) | 0x6E86 | Hestia | structure/tower-white-column | ours: Roof \| ArticleA, height 0, plus PartialHue |

## 4. Seeder commands (part 3)

All four are Administrator commands, declared `WorldSetup`, `Rerun = Skips`, `Shard = TestOnly`, dry run `dryrun`:

```
[DecorAlembicHall | [DecorSmithsHall | [DecorArtificersHall | [DecorHallStructure
    status                          the set's groups and how many placements stand in the world
    place [group] [dryrun]          target the point to dress from
    place [group] here [dryrun]     dress from where you stand
    clear [dryrun]                  remove this set's placements anchored within 24 tiles of you
    clear all [dryrun]              remove every placement of this set
```

- Groups: alembic `vat`, `tanks-north`, `tanks-west`, `bench`, `scrying` (51 items); smiths `forge` (5); artificers
  `gate` (8); structure `tower-large`, `tower-medium`, `tower-small`, `tower-white-brick`, `tower-white-column`,
  `balustrade` (69).
- Each item is a `GuildHallDecor` (set, group, row, anchor): not movable, does not decay, named and hued by its row,
  never a player's item. Place twice at one point places once; clear removes only these.
- **On live:** `testCenter.enable` false (as the Staff Hub reads test or live): place and clear answer "Refused: the
  guild hall decor seeders run on the test shard only (testCenter.enable is false here). Nothing was placed or
  removed." Status still works.
- Stock props in the templates: counters 0x0B3F under the flasks, the forge 0x0FB1 and anvil 0x0FAF beside the smith.
- Code: `server\customizations\GuildHallDecor\` (`GuildHallDecorSeeder.cs` by hand; `GuildHallDecorArt.cs` and
  `GuildHallDecorTemplates.cs` generated).

## 5. The start-up crash (found while preparing the proof)

The branch's image stopped at start: `NullReferenceException: GumpActivator` at `VirtualCheck.Configure`
(`Server/Items/VirtualCheck.cs:34`). Pinned runs every `Configure` in the order of a `List.Sort` by `CallPriority`;
nearly all share the default 50 and the comparer returns 0 for them, so the order is whatever the unstable sort leaves.
`VirtualCheck.Configure` throws when the edit gump is on (default `Core.TOL`, on for our expansion) and
`VirtualCheckGump.Configure`, which sets the activator, has not run yet. The same world copy booted with `latest`,
`cc-P369` and `cc-P275` (both containing this branch's base) and crashed only with this branch's one extra `Configure`.
The tests could not see it: they never start the server through `AssemblyHandler`.

Fix: `server\customizations\VirtualCheckActivatorFirst.cs` calls `VirtualCheckGump.Configure()` at `CallPriority(0)`,
before every default-priority method. The image then booted the same world copy (210,842 items, listening). **Any
branch adding or removing a `Configure` could have tripped this**; with the fix merged it cannot.

## Tests

**Server** (`docker\uo\build.sh -t sl-modernuo:cc-P265`, run detached, docker-build lock, page cache dropped first):

| Run | Result |
|---|---|
| 1, green | 2,035 tests: 2,031 passed, 4 skipped |
| 2, red, six breaks, `--tests-only` | all six new facts failed; plus `CC6Batch1CreatureVerification.TheRestOfTheBatchKeepsItsServUOShape` (Skree's control slots, a random roll; P237 saw the same flake) |
| 3, red, break 4 alone | 1 failed: place-twice ("placed 0 item(s)" not found: 51 placed again) |
| 4, green | 2,035: 2,031 passed, 4 skipped |
| 5, red, the activator fact | 1 failed: "VirtualCheckActivatorFirst.Configure must sort strictly first" |
| 6, green, final | **2,036 tests: 2,032 passed, 4 skipped, 0 failed**; image `92153e00c938` |

`GuildHallDecorVerification` (6 facts) and the breaks (`notes\cc-P265-tools\breaks.py`, restored by SHA-256):

| Fact | Break | Red message |
|---|---|---|
| `TheTemplatesAreTheDesignFile` | 1: the large turret's dz 20 to 21 in C# | "structure/tower-large/14: dz" |
| `EveryRowIsARegisteredPieceOrStockAndNoTwoRowsShareATileAndZ` | 2: vat part 1 claims 3 frames | "Expected 279, Actual 278" |
| `OnTheLiveShardPlaceAndClearRefuseAndChangeNothing` | 3: `Refusal` never refuses | "placed 51 item(s)..." where "Refused:" was expected |
| `PlaceTwiceAddsNothingAGroupPlacesAloneAndClearRemovesOnlyItsOwn` | 4 (alone): place forgets what stands | "placed 0 item(s)" not found |
| `GuildHallDecorRoundTrips` | 5: the group key altered | expected "gate", got "gate-" |
| `TheServerHasTheGuildHallDecorRecords` | 6: the records never written | expected "bubbling vat", got null |

`VirtualCheckActivatorVerification`: our `Configure` sorts strictly before `VirtualCheck.Configure` under pinned's own
comparer; red with the attribute removed.

**Package** (`player-package\tests\Build-UoOverrides.Tests.ps1`): **20 of 20** (the two Play facts pass today).
- New fact `TheGuildHallDecorRecordsAreTheServersTableAndEveryIdIsRegisteredWithItsPngAndItsAuthorsCredit`: C# and
  records.json equal by value (flags by number), pieces contiguous, Animation exactly on animated pieces, animdata frames
  inside each piece, every ID registered once with its PNG, each license naming its author's rule and the EA mark.
- Red a (records.json height of the vat's front band 8 to 9): "expected [8] but got [9]. height of vat-front".
  Red b (one railing row without its EA mark): "not true: 28165: Outlands' credit, EA-derived". Both restored by SHA-256
  (`pkg_breaks.py`). A first attempt ran while the server breaks were still applied and failed on the C# parse instead;
  it was redone on a clean tree.
- Ledger: 561 registry rows, 521 art (`:299-301`); the records carve-out gains 28016-28294 (`:257`).
- **Fixtures grown:** the synthetic tiledata/animdata in the test file stopped near ID 16,000, so records at 28016+
  would land past their end. They now hold 28,800 statics (the real 7.0.117 files hold 65,536).

**Not run:** P26's package gates (`Build-PlayerPackage.ps1`) and the in-game screenshots (P374).

## What an F-49 placement prompt needs from Chase

1. **Which halls get which set**, and the site picks P151 left open (row 18 Papua for the Alembic, row 7 Serpent's Hold
   for the Smiths, row 17 Royal City for the Artificers, and which halls take a tower or the balustrade).
2. **Live or test only:** the seeders are test-only by declaration and code. Dressing live halls needs either a live
   switch on these commands or a placement seeder like P237's (fixed coordinates, run once); say which.
3. **Tunings per hall:** each template is anchored on one point; per hall, F-49 copies a set into the design file with
   the hall's own offsets (and hues: the vat's liquid, the turrets and domes, the flasks take a hue).
4. **The EA-derived ruling** (Deviations 1) for the flasks, the blacksmith and the railings.
5. **Which spare pieces matter:** 85 registered pieces are in no template yet: 66 marble pieces (stair banisters,
   rails, posts, the second ladder), 10 tower variants (window and plain fronts, the two top floors), the eight tank
   facings the template does not use, and the unlit crystal ball.

## Website credits

> Guild hall decor: the bubbling vat and five towers by **Hestia**; the creature tanks and crystal ball by
> **RedRooster** (Steven Armstrong); the partial-hue flasks by **Ems**; the working blacksmith by **Apocalypse**; the fire
> pit and floating crystals by **MrRiots**; the arc orbs by **otimpyre**; the marble railings, banisters and ladder by
> **Outlands** (OUTLANDSOwyn). All shared on servuo.dev. Thank you all.

RedRooster asks to be on the shard credits list for both packs; Outlands asks to be credited.

## Deviations and decisions for Chase

1. **EA-derived art ships as our PNG override** (flasks, blacksmith, marble railings), as P243's trophies do. If you want
   them only as true patch records, they come out of registry.csv, records.json and the catalogue.
2. **P237's two marble railings (15503, 15504) are not marked EA-derived** in their registry rows; the author's page says
   the set is based on the wooden assets. I did not change P237's rows; a one-line follow-up if you agree.
3. **No in-game screenshots yet** (part 4): paused at your request; P374 does them. The renders in
   `notes\cc-P265-tools\preview-*.png` (git-ignored) show each template in the client's geometry.
4. **The shared test shard could not be started from this work copy:** its compose file takes every path from
   `docker\uo\.env`, which only the main checkout has, and every mount is under `D:\ShatteredLegacy`. I prepared a
   private copy instead (the bot shard's Configuration and save, on 127.0.0.1:2596) and used it only to boot-check images.
5. **An unattended permission denial:** the Read tool was refused on
   `D:\UO\golems\Iron\ShatteredLegacy\docker\uo\build.sh`; I did not read it another way and ran it as P243's notes
   describe (`-t <tag>`, `--tests-only`).
6. **The start-up fix (section 5) is outside the prompt's scope** but was needed to ship this branch at all.
7. **Templates are drafts:** laid out for a flat open floor, not a real hall; F-49 tunes them.
8. **Art IDs above 0x4000** are new for our registry (Headlines).

## Continuation

- **Done:** parts 1-3; all tests and red runs above; the start-up fix; the CHANGELOG (2026.10.21.17, Staff) and VERSION.
- **Left:** part 4, the screenshots and the live refusal shown in game: `D:\UO\cc-prompts\queue\cc-P374-cont-guild-hall-
  decor-proof.md`. Its tools are ready: `proof.ps1` (client with our art and overrides, Admin setup through P219's
  `uobot.legionsetup`, one capture per set), `find_spot.py` (empty spots: Alembic 1135,1791; Smiths 1199,1823;
  Artificers 1231,1889, Trammel z0).
- **Mid-flight:** nothing. The proof container is removed, its scratch copy deleted, both locks released.
- **Part 4 done in cc-P374** (2026-10-25): `notes\cc-P374-cont-guild-hall-decor-proof.md`, shots in
  `notes\art\cc-P374\`. It found that our client drew every animated piece on its first frame; client patch 0007 fixes it.

## Files changed

`ShatteredLegacy`:
- `server\customizations\GuildHallDecor\GuildHallDecorSeeder.cs` (new), `GuildHallDecorArt.cs`,
  `GuildHallDecorTemplates.cs` (new, generated)
- `server\customizations\VirtualCheckActivatorFirst.cs` (new)
- `server\customizations\ShatteredRunestone.cs` (`ShatteredLegacyArt.Apply` calls `GuildHallDecorArt.Apply`)
- `server\tests\Misc\GuildHallDecorVerification.cs`, `GuildHallDecorDesignCopy.cs` (generated),
  `VirtualCheckActivatorVerification.cs` (new)
- `design\guild-hall-decor\templates.json` (new)
- `player-package\vendor\shattered-legacy-art\`: `registry.csv` (+279), `records.json` (+179 tiledata, +33 animdata,
  about), `SOURCE.txt` (+section), `art\28016.png`-`28294.png` (279 new)
- `player-package\tests\Build-UoOverrides.Tests.ps1` (new fact, fixtures, ledger, carve-out)
- `CHANGELOG.md`, `VERSION` (2026.10.21.17)

`shard-migration`: this note; `notes\cc-P265-tools\` (`decor.py`, `first_templates.py`, `find_spot.py`, `proof.ps1`,
`breaks.py`, `pkg_breaks.py`; previews git-ignored).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P265` (this Golem's
work copies; the script's defaults name the main checkouts). Code: 294 files pending (7 changed, 279 PNGs, the three
seeder files, the design file, three test files, the start-up fix). Docs: 7 (this note and the tools). Neither is
BLOCKED. Largest new file: the large tower's top floor PNG (28251), 55 KB; the 279 PNGs are 1.9 MB together.

```
Repo Result
---- ------
code dry run
docs dry run
```

P265 PAUSED
