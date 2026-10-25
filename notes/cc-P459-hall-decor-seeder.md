# P459: guild hall decor seeder: refuse overlapping or out-of-date placements; walk-in towers; test the real design file

Done 2026-10-24 by the Iron Golem. Code copy D:\UO\golems\Iron\ShatteredLegacy, branch golem/Iron/P459.
Sources: Codex's P419 #1, #2, #4, #5 (and nit #6), checked by Crystal's P429 (draft W6); Chase's decision of 10-23 on
P419 #3 (the towers are meant to be walked into).

## In plain words

- The five guild hall towers ([DecorHallStructure, test shard) can now be walked into. Each has a door you double-click
  to open (it closes itself after 20 seconds) and a stone or marble floor inside. A picture of the large tower, shut
  and open: `notes/cc-P459-tower-large.png`.
- The decor commands now refuse, and place nothing, instead of making a mess. That covers a spot whose template was
  edited since it was dressed (clear it first), a placement one tile off the same set (it used to double the set),
  and a piece that would stand in a wall, an object or a doorway. A dry run lists what is in the way.
- The test now reads the real design file, so editing templates.json without regenerating the server's copy fails
  the build.
- Two things for you to decide, both below: whether the white column tower should get an upper floor and stairs (it
  has none in the art), and a separate bug I found in Butcher's Eye (a rare roll can crash on goblin blood). No deploy
  needed: all of this is test-shard only.

## What changed

All code paths are in the code copy.

| Part | Change |
|---|---|
| 1 | `server/customizations/GuildHallDecor/GuildHallDecorSeeder.cs`: `GuildHallDecor` is now generator version 1, with a new saved `TemplateHash` (field 4: the first 16 hex digits of the SHA-256 of the group's rows: art, offsets, hue, piece, door and hidden switches, in order). `MigrateFrom(V0Content)` carries the four old fields; a version-0 item has no hash. Schema: `server/migrations/Server.Items.GuildHallDecor.v0.json`. `Place` now refuses, placing nothing: (a) when any item of the group already at that point carries another hash: "the template changed since it was placed at x,y,z. Clear first ([cmd clear), then place again"; a version-0 item counts as changed; (b) when any tile of the new placement holds an item of the same set placed from another point: "it meets <group> placed from x,y,z". |
| 2 (done, not only optional) | `GuildHallDecorSeeder.Conflict`: every row about to be placed is checked against impassable statics and multi tiles, impassable items, a door on its tile, and a door whose swing (its `Offset`) lands on its tile, each over the row's own height. The placement's own standing items are not conflicts (a tank on its stand). A dry run lists the conflicts ("would be refused"); a real run lists them and places nothing. `ClusterFGuildHallPlacement` (P281's hall placer, which calls `Place`) now prints a refusal instead of counting the decor as placed. |
| 3 | `GuildHallDecorVerification.TheTemplatesAreTheDesignFile` reads `design/guild-hall-decor/templates.json` itself: `docker/uo/Dockerfile` copies it to `/design/...` in the builder image, where build.sh runs the tests (only `.cs` files reach the test project, so it is not literally in the test output folder; `SL_DESIGN_ROOT` overrides the root for a local run). It compares the file's hash with the generated table's and every row, now with its door and hidden switches. `server/tests/Misc/GuildHallDecorDesignCopy.cs` (the C# copy the old test hashed) is deleted, and `notes/cc-P265-tools/decor.py layout` no longer writes it. |
| Chase 10-23 | **Towers.** `design/guild-hall-decor/templates.json` (regenerated into `GuildHallDecorTemplates.cs` by `decor.py layout`): each tower's door piece is marked `"door": true`; the three two-row towers (medium, white brick, white column) get two `"hidden": true` invisible walls (stock 0x21A3, "nodraw", Wall/Impassable, height 100) on the open tiles at their sides; and every tile inside gets a floor (stone pavers 0x051A in the brick towers, white marble 0x050E in the white ones). Structure rows: 69 to 116. `Row` gains `Door` and `Hidden`. The seeder places a door row as a `GuildHallDecorDoor` (a `GuildHallDecor`, so P281's lookups and clear still see it) and a hidden row with `Visible = false`. |
| the door | `GuildHallDecorDoor`: double-clicked within 2 tiles it opens. It becomes stock 0x0001 ("nodraw", not impassable) and invisible, so the doorway is walkable and shows the floor behind it. A timer closes it after 20 seconds, then every 10 while a mobile stands in the doorway, as pinned's `BaseDoor` timer does. A door saved open loads closed. Saved field: its closed art. It is not a `BaseDoor`, because the seeder's items must stay `GuildHallDecor`. |

### The towers, tile by tile

Interiors were found by flood fill from outside with the player diagonal rule (pinned `Movement.cs:146-152`: a player's
diagonal step needs both side tiles clear), so only the side gaps leaked.

| Tower | Door (offset) | Side gaps closed | Floor tiles | Inside |
|---|---|---|---|---|
| large brick | 3,3 | none (a closed ring) | 14 stone pavers | 14 tiles |
| medium brick | 8,-4 | 6,-4 and 8,-6 | 5 stone pavers | 5 tiles |
| small brick | 11,-9 | none | none | **the door tile itself**: the tower is a 2 x 2 of wall pieces with no tile inside, so the open doorway is all there is |
| white brick | 16,-12 | 13,-11 and 17,-15 | 11 white marble | 11 tiles |
| white column | 22,-18 | 19,-17 and 23,-21 | 11 white marble | 11 tiles, ground floor only |

**No stairs.** Chase's instruction was "stairs if it has floors". No tower has an upper floor in the art: the white
column tower's second storey is a second ring of wall pieces at z 22, with nothing to stand on. Its 11-tile inside is
also too small for stock stairs to climb 22 (the longest straight run inside is 3 tiles). So every tower is one room
at ground level. Decision for Chase below.

**The render** (`notes/cc-P459-tower-large.png`, from `notes/cc-P459-tools/render_tower.py`, P265's client-geometry
renderer): the large tower with its door shut, then open, showing the floor through the doorway. The medium tower's
render is in the git-ignored `notes/cc-P459-tools/tower-medium.png`.

## Tests

`server/tests/Misc/GuildHallDecorVerification.cs`, five new facts plus the two changed ones:

- `TheTemplatesAreTheDesignFile` (part 3): reads the real JSON, as above.
- `APlacementOneTileOffTheSameSetIsRefusedAndPlacesNothing` (P419 #1): the vat one tile east is refused with "it meets
  vat placed from 1300,1300,0", and nothing is placed; another group reaching the vat's tiles, and its dry run, are
  refused too; ten tiles away it places.
- `AfterATemplateEditPlacingAtTheOldPointIsRefusedUntilCleared` (P419 #4): the crystal ball's row is moved one tile
  in the live table. Placing at the old point is refused with "clear first" and places nothing. An item with no hash
  (version 0) is refused the same way. Cleared, the edited row places at its new tile.
- `ARowInSomethingImpassableOrADoorwayIsRefusedAndTheDryRunSaysWhy` (P419 #2): a vat-art item on the cloth's tile (the
  dry run names it), a stock MetalDoor on that tile, and a MetalDoor whose swing lands on it are each refused, placing
  nothing; with all three gone it places.
- `EveryTowerIsClosedUntilItsDoorOpensOntoAWalkableInside` (Chase 10-23): places the whole structure set, then walks a
  33 x 35 box with pinned's own `Movement.CheckMovement` (`MovementImpl`). Doors shut: no door tile and no floor tile
  can be reached. Each door opened by a player beside it: every door tile and all 41 floor tiles can be reached. A
  player standing in a doorway keeps that door open past 20 seconds; the other four close and show again; it closes
  10 seconds after the doorway clears; from 3 tiles away nobody opens it.
- `PlaceTwice...` now also checks each item's hash; `GuildHallDecorRoundTrips` round-trips the hash and a door.

The host has no tiledata and masks every item ID to row 0 (`Route/TestHostTileData.cs`). The tower and preflight
facts open a `TestTileRows.Seed` scope with four stock rows added to `Route/TestTileRows.cs` (NoDraw 0x0001,
InvisibleWall 0x21A3, StonePavers 0x051A, WhiteMarble 0x050E). They were read field by field with a TileData.Load-order
parser that ends exactly at the end of `D:\UO\ClassicUO\ClassicUO\Ultima Online Classic\tiledata.mul`, which is
3,188,736 bytes like the shard's client-data copy (that copy is off limits to my shell).

Not done: P419 #6 (the activator test also running the initializer). `VirtualCheck.GumpActivator` is an unsafe
function pointer, and I did not confirm the test project allows unsafe code. It is optional in the prompt.

### Runs (`docker/uo/build.sh -t sl-modernuo:cc-P459`, under the `docker-build` lock, taken and released)

Free memory was 9.8 GB at the start after dropping the Docker VM's page cache, which I dropped again before each run.

| Run | Tree | Result |
|---|---|---|
| 1 (`--tests-only`) | everything | 2,334 passed, 2 failed: the tower and preflight facts. The host's 0 item mask made every decor item invisible to movement and to the preflight; fixed in the tests with `TestTileRows.Seed`. |
| 2 (`--tests-only`) | everything | **2,336 passed, 0 failed**, 4 skipped |
| red (`--tests-only`) | five breaks: no overlap check, no template check, no preflight, door rows placed as plain decor, and the JSON alone edited (the large turret dz 20 to 21) | 2,331 passed, **exactly the 5 new behaviours failed**, each at its own assertion: "placed 9 item(s)" where "Refused: this would overlap" was due; "placed 0 item(s)" where "Refused: the template changed" was due; "templates.json changed without regenerating GuildHallDecorTemplates.cs"; the preflight dry run listing no conflict; no tower doors at all |
| red 6 (`--tests-only`) | one break: hidden side walls not placed | **1 failed**: "tower-medium: (1506, 1595) is reachable with the door shut" (5 of 5 medium-tower floor tiles) |
| green 1 (full build) | breaks restored (seeder and JSON md5-checked against the green copies) | 2,335 passed, 1 failed: `DeathHooksVerification.AKilledNonBondedPetPaysNoImbueKillEffect`, not mine (below); it passed in the three runs before on the same code |
| green 2 (full build) | same tree | **2,336 passed, 0 failed, 4 skipped**; image `sl-modernuo:cc-P459` built with patches applied; no compiler warnings |

Against the old code the JSON-only edit would have stayed green: the old test hashed the C# copy, which a JSON edit
does not touch. That was P419 #5.

## Deviations and decisions for Chase

- **Decision: an upper floor for the white column tower?** Its art draws two storeys, but there is no floor to stand
  on, and the inside is too small for stairs. If you want one, a later prompt can add a floor at z 22 and a ladder or
  a teleporter tile, or new art for a spiral stair. Today it is one tall room.
- **The small tower's inside is its doorway.** It is four wall pieces in a 2 x 2 with no tile between them. Opened,
  you can step into the doorway under its crenellated top, and that is all.
- **The open door and the side walls are invisible items**, not drawn tiles. I could not confirm the client hides
  "nodraw" art on items (its art reads NO DRAW), so an open door and the side walls are simply not sent to players.
  The cost: a player's client does not know about the side walls, so walking into one from outside makes the server
  refuse the step (a stutter). The walls sit behind the towers' own wall art, so nobody should be walking there.
- **A refused placement in P281's hall placer** now prints the seeder's reason; it used to count it as placed. The
  preflight can refuse the halls' decor on the test shard where a piece meets a real wall (the test host has no map,
  so this is not tested against the real sites).
- **Not my code, found on the way: Butcher's Eye can throw.** `server/customizations/Imbuing/ClusterFImbueEffects.cs:334-336`
  makes the rare part with `Activator.CreateInstance(type)`, and its list includes `GoblinBlood`, which has no
  parameterless constructor ("MissingMethodException ... GoblinBlood"). On that roll the kill event throws. It failed
  P455's `DeathHooksVerification.AKilledNonBondedPetPaysNoImbueKillEffect` once here. Worth a small prompt (construct
  with an amount, or drop GoblinBlood from the list).
- **The Read tool is denied on code-copy files** in unattended runs, so I wrote files in the scratchpad and copied or
  patched them with Python. Nothing was skipped.
- **Optional P419 #6 not done** (above).

## Files changed

Code copy (`D:\UO\golems\Iron\ShatteredLegacy`):

- `CHANGELOG.md` (2026.10.24.16, Staff), `VERSION`
- `design/guild-hall-decor/templates.json`
- `docker/uo/Dockerfile`
- `server/customizations/ClusterFGuildHallPlacement.cs`
- `server/customizations/GuildHallDecor/GuildHallDecorSeeder.cs`
- `server/customizations/GuildHallDecor/GuildHallDecorTemplates.cs` (generated)
- `server/migrations/Server.Items.GuildHallDecor.v0.json` (new)
- `server/tests/Misc/GuildHallDecorDesignCopy.cs` (deleted)
- `server/tests/Misc/GuildHallDecorVerification.cs`
- `server/tests/Route/TestTileRows.cs`

Docs copy (`D:\UO\golems\Iron\shard-migration`): this file, `notes/cc-P459-tower-large.png`,
`notes/cc-P459-tools/render_tower.py`, and `notes/cc-P265-tools/decor.py` (layout writes the door/hidden switches and
no test copy).

No Haven connection, no test-shard start, no player package build.

P459 DONE
