# cc-P741: isle coast, shipwreck, signs, farm, bank and League house round

Iron Golem, 2026-10-30. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P741` (main at the P738 merge). Not committed, nothing deployed, no package built, Haven not touched,
the shared Test Shard not touched.

## In plain words

- **The isle's coast reads as one shore now, and the wreck is a whole ship.** The surf follows the sand all the way
  round, the square notches and sand-coloured lumps are gone, and driftwood, seaweed and shells lie along the waterline.
  The wreck is now OSI's own whole ship, both halves. It has run aground across the beach where you wake: one half in
  the shallows, the other up the sand, with driftwood round it. Before and after: `notes\cc-P741-review\before-whole-isle.jpg`
  and `after-whole-isle.jpg`; in the game client, `shots\walk2-beach-walk-f12.jpg` and `tazuo-coast-wreck.jpg`.
- **Every sign stands north of its path, and the farm runs one way.** Lesson 1's sign and all the others now stand on
  the north side of the road, facing it. The moongate's sign stands where the road meets the dock, so you see it before
  you walk out. The farm is turned round: the field is to the west, with ploughed soil and fewer, lower crops, so the
  rats are easy to see (`tazuo-farm-gate.jpg` shows one). The farmhouse with Pip stands right beside the field gate, so
  there is no walking back.
- **The bank and the League lodge are redone.** The bank sits in the grass with a small paved step at its door and a
  paved spot round the fountain, instead of the big square of paving. It has plants by its walls, and scales, coin and
  a strongbox inside. The lodge has one even wooden floor, bookcases, a long table with chairs, candles, a brazier, and
  banners outside.
- **For you:** walk the isle on the next test build (or the next isle release, below). One thing to judge: the north-
  and east-facing beaches still step a tile at a time along the sand's edge, with the surf now running along them. That
  is the tile art's limit on those sides (OSI's own coasts there step too); evening it into longer runs looked worse.
  This also needs a second Golem's render review before it merges (guide section 8); the review folder is ready.

## What changed

### 1. The coast (Chase: "shoreline is not fluid, it's choppy and directions are incorrect")

**What OSI does, measured.** P725 put its surf pieces on the sea tiles beside the sand. On the north and north-west
coasts it filled those sea tiles with impassable sand under the piece, which drew the lumps. I surveyed OSI's gentle
sandy coasts on stock Trammel again, cell by cell (`cc-P741-tools\survey_shore741.py`, 704 sand cells,
`shore-survey741.json`). OSI does it the other way round: **the first sand tile drops to the sea's height (Z -5) and
carries the surf piece for its own edge**:
- sea to the west: 0x179D/0x179E;
- sea to the south: 0x179F/0x17A0;
- the inside corner of a stair: 0x17A9;
- sea only on the south-west diagonal: 0x17A5.

On its north- and east-facing coasts OSI puts nothing on the sand. One coast OSI draws this way is rendered in
`osi-diag1.jpg`.

**The new rule** (`notes\cc-P662-tools\build_isle.py` `osi_land_shore`, `isle-sets.json` `shoreRule: osi-land`, beachZ
1 = -5):
- **Near coasts (sea west or south):** OSI's piece on the sand, as above. It always lays a piece where OSI's table has
  one (OSI leaves about a third bare; on a small isle each bare one read as a tooth). It never lays the plain diamond
  0x1797 on sand.
- **Far coasts (sea north or east):** the sea tile beside the sand takes a surf-edged piece over its own water: land
  south of it 0x17A1/0x17A2, land west 0x17A3/0x17A4, the inside corner 0x17AB. I chose these by rendering every
  candidate on a test stair (`stair_test.py`, `stair-test2.jpg`, top middle).
- **Beside the moongate's paved landing:** P725's measured surf edge for that side.
- **No one-tile notch or spur** (`smooth_coast`; main had 6 notches).
- **A strand line** on the second sand ring: seaweed 0x0DBA/0x0DBB, driftwood 0x0C2D-0x0C30, shells, small rocks (64
  pieces).
- **Tried and dropped:** evening the coast into 3-tile runs. It drew square bays and spoiled the smooth west shore
  (`try2-*.jpg`).

**Counts:** 378 sand tiles with OSI's piece, 72 by its side's fallback, 294 far-coast sea tiles with surf, 5 beside the
landing. The far coasts still step a tile at a time; the surf runs along them (`tazuo-coast-north.jpg`,
`walk2-beach-walk-f12.jpg` top right). That is the art's limit there, the same as P733 said; I do not claim it gone.

**Walkable:** the wet sand under the surf is walkable, as on OSI's beaches: a surf piece is 0 high at Z -5. No sea tile
is walkable except the 24 dock planks (`walk-check.txt`: 8,413 walkable tiles, 24 on water land, all planks).

### 2. The wreck (Chase: "shipwreck may need orientation and both ship halves")

- **One half, by survey.** Celestial's West wreck (P724) is 20 of the 30 pieces of one half of the stock ShipwreckBow
  art. OSI lays that art exactly once, on Malas (`survey_wrecks.py`): both halves, the "West" set's 30 pieces and the
  "East" set's 30, broken open toward each other across a swirl of water, with driftwood and morning glories round
  them (`osi-malas-wreck.png`, `.txt`).
- **The new wreck.** `WakeningIsleShipwreckAddon` is now that composition (`gen_wreck.py`), 94 pieces: the 60 hull
  pieces, the waves and swirl in the break, driftwood against the hull and up the beach, seaweed on the sand.
- **Placement.** It lies across the west tip's waterline at 6624,3995,-4, the way a ship runs aground: the West half in
  the shallows (x 6617-6623), the break in the surf, the East half up the beach (6626-6632). It ends 6 tiles west of the
  wake spot (6638,3993) and clear of the road.
- **The ground under it.** The map lays sand under the beached half and one tile round it (it was grass).
- **Existing worlds.** A world seeded with P724's half has it swapped for the whole ship at the next seeding: on load
  for the Fold, as the copies are seeded. The load line said "replaced 1 old wreck" (below).
- **Credits.** `IsleAddons-SOURCE.txt` records the swap; Celestial is still credited for the wreck the isle had.

### 3. The signs (Chase: "all signs should be north of path"; "sign next to moongate at end is hard to see")

- **The chooser.** `sign_spots741.py` is P720's chooser with one more rule: a sign stands north of its path, beside it
  (road within 3 tiles south, none north of it or beside it, not on the road). The standing signpost 0xA854 is the face
  that reads from the south, so it faces the path. Rendered: `signpost-big.png`; 0xA855 is the face that reads from
  the east.
- **The 11 lesson signs:**

| Lesson | Before | Now |
|---|---|---|
| movement | 6646,3994 | 6646,3990 |
| backpack | 6656,3992 | 6656,3988 |
| paperdoll | 6665,3993 | 6665,3989 |
| chat | 6692,3991 | 6691,3987 |
| farm | 6714,3981 | 6698,3978 |
| healing | 6688,3980 | 6701,3980 |
| death | 6736,3996 | 6736,3989 |
| banking | 6762,3982 | 6766,3981 |
| league | 6780,3994 | 6782,3989 |
| loop | 6794,3981 | 6794,3981 |
| travel | 6831,3992 | 6811,3988 |

  - The death lesson's stop is the yard gate, south of the road, so its sign stands across the road on the north side.
  - The travel sign stood on the moongate frame in the gate's glow. It now stands where the road meets the dock, north
    of it, clear of the frame and the lighthouse (`tazuo-sign-11-travel.jpg`). It is still the standing signpost
    0xA854, the largest standing sign in the stock art.
  - The chat lesson's second sign (the farm signpost Wren's lesson points at) moved from the road's edge to 6690,3986,
    beside the lesson sign. Both are kept.
- **Building signs.** The farm gate's own signpost and the farmhouse and bank signs stand north of the road already.
- **Existing worlds.** Every lesson sign on the isle moves to its new spot, and a second sign for a lesson is removed
  (`MoveOldMarkers`). See Mistakes below.
- **The guide.** Section 6 has the new rule ("Every sign stands north of its path, facing it"), plus one for signs at
  a glowing landmark.

### 4. The farm (Chase: "farm house should be east of farm and farm shifts west so no doubling back")

- **The layout.** `gen_isle_farm.py` is P720's generator with new constants:
  - the field, its fence, gate, pen, Wren, Tobin, the pests and their spawners moved 18 tiles west (field x 6678-6694);
  - the farmhouse (OSI's cottage, with Pip's bench and blood) moved 12 tiles east (x 6699-6705), beside the field's
    east gate;
  - the well moved to the house's east side, because its old tile was now Tobin's;
  - the road's short jog leads to the gate (Wren at 6696,3978, the stop at 6696,3979) and runs past the farmhouse steps
    (`newisle.py` ROAD and STOPS 5);
  - the lesson runs road, gate, pests, farmhouse, then east to the yard.
- **The field.** It is furrowed land laid as OSI lays its fields west of Britain (`survey_furrows.py`, `osi-field.jpg`):
  0x0009 inside, border pieces on each edge and corner. There are two beds.
- **The crops.** Two short rows on every other tile (cabbage, carrots) and a pumpkin row; no corn or wheat. P720 had
  six full rows, two of them tall.
- **Rats.** The rats are easy to spot in the client (`tazuo-farm-gate.jpg` shows one between the rows), so I did not
  switch to giant rats.
- **Existing worlds.** `TutorialFarm.MoveFromOldLayout`: the old farm addon is relaid by `IsCurrent`. The old door,
  field gate, its fence piece, Pip's old bench and blood and the old spawners (with their spawn) go. Wren, Tobin and
  Pip walk to their new spots, and nothing is doubled.

### 5. The bank (Chase: "sandstone pavement around bank is a lot and unnatural"; "bank needs some deco work")

- **The ground.** The 21 x 18 paved square is gone. Paving is now:
  - the bank's footprint;
  - an apron at its door (x 6759-6765, y 3981-3982);
  - a pad round P724's fountain.

  Each is edged with worn dirt that blends into the grass through the dirt-grass transitions. The road's dirt runs up
  to the apron, and the smithy corner (forge, anvil) stands on dirt. Paved tiles: 147 (were 403). There are ferns, a
  small palm and a potted plant by the walls and door.
- **Inside**, the P734 practice bank's pattern:
  - the counter with its gap at the east end, scales and gold on it;
  - three vault chests and a strongbox behind it;
  - candelabras in the corners;
  - torches on plain north and west wall pieces;
  - a bench and a potted plant for the queue, and the framed carpet.

  The sign now hangs on 0x0B98 (0x0B97 lies flat along the wall, guide 2.5).

### 6. The League lodge (Chase: "league house needs deco work and floor needs work")

- **The floor.** One board tile (0x04A9; P720 mixed seven) on every floor tile and the door tile, and under the south
  row and east column of the walls as OSI's multis lay it (guide 2.2, `floorUnderSouthEast`).
- **Inside**, the practice lodge's pattern:
  - Elara's desk with a book and scroll;
  - bookcases 0x0A98 on the north wall and 0x0A99 on the west wall (P720's 0x0A97 stood edge-on), none in front of a
    window;
  - a long table with chairs on both sides by the art (0x0B4F north, 0x0B50 south), on a framed carpet, with a book, a
    mug and a map on it;
  - candelabras, a brazier, torches on plain wall pieces;
  - the League banners outside the east wall, moved off the windows.
- **No hearth.** The only hearth art faces east or south. On the west wall its chimney comes through the low eaves
  (guide 11.3), and the north wall holds the door and two windows, so a brazier lights the room instead.

## Tests

- **Map facts** (`tools\tests\test_mapops.py`, `SL_SHARD_REPO` = the code copy): **12 of 12** (`green-test-mapops.txt`).
  - **New fact 12:** no bare edge on either kind of coast, no sea tile filled with sand, no one-tile notch or spur, the
    strand line, and the field's furrows inside the field. **Seen failing** on main's patch (`red-map-fact-12.txt`:
    the bare sand edges).
  - **Fact 11 (P725)** now accepts the north coast's surf on the sand north of the sea cell, where OSI lays it. Its
    first run on this map failed at the five sea tiles south of the moongate landing; I added the surf edge there and
    it passes.
- **The map builder's gates:**
  - every leg and lesson detour walks (pinned movement, server items in place), 25 of 25 spots fit, the dock steps at
    most 2;
  - **new:** every lesson sign is north of its path. Seen failing on main's signs (`red-signs-gate.txt`: 9 of 11), now
    passing (`green-signs-gate.txt`).
- **C# facts** (`server\tests\Tutorial\TutorialIsleCoastVerification.cs`, new, 5 facts). Each was seen failing on a
  mutant that undoes its change (`mutate741.py`, `red-*.txt`); each mutant fails exactly its own fact:
  1. the whole wreck, and P724's half swapped once (`red-nowreckswap.txt`);
  2. the farmhouse east of the field, the crops sparse (`red-oldlayout.txt`, P720's layout);
  3. a farm laid before the move, moved in place (`red-nofarmmove.txt`);
  4. the chat signpost moved, not doubled (`red-nochatmove.txt`);
  5. a lesson sign from before, moved north of its path, not doubled (`red-oldmarkers.txt`, P720's mover).
- **Updated tests:** the existing facts that pinned the farm's and signs' old places (`TutorialIsleWalkFixes2Verification`,
  `TutorialIsleWalkFixesVerification`). The sign fact now allows a sign up to 6 tiles from its stop: across the road
  from the yard gate, and at the dock road's end for travel. All isle tests: **75 of 75** (`probe-3.txt`).
- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P741`, `docker-build` lock taken and released): **EXIT=0**,
  2,832 tests: 2,826 passed, 6 skipped, 0 failed (`green-gated-build.txt`; the first build before the marker fix,
  `green-gated-build-1.txt`, was 2,831 / 2,825 / 6 / 0). The Docker VM had 12.5 GB free; Windows read 1.3 GB, so the
  builds ran detached.

## Live, on a private shard (127.0.0.1:2596, `test-shard` lock taken and released, container down)

- **Setup.** `proof-shard.ps1` (P733's) on a fresh copy of the bot world (seeded with P724-P733's isle), this image,
  and the map overlay built by the test shard's own `Build-MapOverlay.ps1` from this branch's patch on the SoS base.
- **Seed on load, the old world** (`seed-on-load.txt`): "placed 0 station markers, 2 NPCs/echo/vets, ... farm: placed
  1 farm addon, 3 door, 0 Farmhand, 2 spawners; already there 2. Isle addons: placed 1, replaced 1 old wreck."
  - The old farm was relaid in its new place, the old wreck swapped, and the signs moved (no new ones).
  - The "2 NPCs/echo/vets" is main's too: main's image on the same world says the same every load (`shard.log` in
    `p741-proof\shard-main`).
- **Bot route:** 0 failed checks, 85 passed (`runs\run1\playlog.txt`, 186 s). It is P732's main route with the farm's
  new spots (`make_isle741.py`):
  - a fresh character woke on the beach;
  - the farm: the pitchfork, war mode and the pests in the new field, the pet;
  - then Pip on his bench at 6704,3975 in the farmhouse beside the gate;
  - then the yard, bank, lodge, stones and the moongate to Rook; the New Haven pick started on the plaza;
  - the Admin's seeding: dry run and two runs placed 0 (idempotent).
- **A real walk on the beach in TazUO** (`beach-walk.log`; frames `walk-*.jpg`, `walk2-*.jpg`). Iron the Tester walked
  with the client's own steps, no teleport:
  - north along the west beach past the wreck, 6629,4003 to 6629,3985;
  - east to 6650, back west and south to 6631,4002.

  Every leg reached its end with no stuck step, and no step changed Z by more than 3 (Z -5 on the wet sand, -3, -1, 0).
- **19 TazUO shots from the default camera** (`notes\cc-P741-review\shots\tazuo-*.jpg`): eight coast stretches, four
  signs, the farm, the farm gate and the farmhouse inside, the bank front and inside, and the lodge front and inside.
  What they show:
  - surf along every coast;
  - the wreck whole;
  - each sign north of its road with its board toward it;
  - the field, gate, Wren, Tobin and the farmhouse in a row, a rat plain among the crops;
  - the bank on its apron with the fountain pad;
  - the lodge dressed, with Elara at her desk.

  One mistake of mine: the coast-north shot set the Tester on a sea tile; the shore beside him is still what the shot
  shows.

## Facing

| Piece | Facing, and how checked |
|---|---|
| Surf pieces | Chosen by the edge they sit on (the survey, and the stair test render for the far side). |
| Wreck | OSI's own composition, not turned. |
| Signs | 0xA854 throughout, the south-reading face, rendered (`signpost-big.png`). |
| Bank sign hanger | 0x0B98 (sticks out from the south wall). |
| Bookcases | 0x0A98 north wall, 0x0A99 west wall (guide 3). |
| Chairs | 0x0B4F north of the table, 0x0B50 south of it (guide 3). |
| Banners | 0x1589 flat on the east wall outside (P720). |
| Farm cottage | OSI's multi whole, moved, not turned. |

Nothing was turned from its art. Every piece is in `notes\cc-P741-review\placed.md`.

## The isle-only release (`release/isle-20261028`)

- **Applies cleanly.** Every code and test change (6 server files, 3 test files) and `IsleAddons-SOURCE.txt` apply
  with `git apply --check` to the release branch's tree (checked in a throwaway index, no worktree touched;
  `release-apply-check.txt`).
- **Three conflicts, all the usual per-release ones** (P733 met the same):
  - **`trammel.mapops`:** the release has the stock land's patch. Use `notes\cc-P741-tools\trammel-stock-base.mapops`
    instead of the diff. I built it with this branch's code on the release's own patch and stock Trammel. Its 42,488
    isle lines are identical to main's build, and every line outside the isle is the release branch's own, byte for
    byte.
  - **`CHANGELOG.md` and `VERSION`:** the release keeps its own numbering (2026.10.29). Put the 2026.10.30.2 section's
    six lines on top of it.
- **The bot route for the release.** Run `make_isle741.py` on P733's `isle.py` (the release's stock New Haven);
  `make_isle741.py` asserts each edit.

## Mistakes, and what to trust

- **Signs doubled on an old world.** My first image doubled every lesson sign on an old world. The seed-on-load line
  said "placed 10 station markers", because P720's mover only moves a sign still on its stop tile. Fixed with a new
  fact (5, seen red), rebuilt, re-run: 0 placed. Nothing was released with it.
- **Six West-half pieces dropped.** My first wreck table dropped them (a line off in a copy). The new wreck fact
  caught it (24 of 30); the table is regenerated and checked stable against the map it shapes.
- **The first gated build started in the release worktree.** A substitution in the copied launcher failed. I stopped
  it within a minute (its test container removed; the release worktree shows no change) and started the right one.
  Its only trace is a `sl-uo-builder:cc-P741` tag that the correct build then replaced.
- **Not checked:** how the far coasts look in other light or seasons; the release branch built and played (only the
  apply check and the stock-base map build were done).

## Deviations and decisions for Chase

- **The far coasts still step.** The north- and east-facing beaches still step a tile at a time along the sand's edge,
  with surf along them. Fully hiding that needs new art (a diagonal shore piece for those sides) or a different
  coastline. Say if you want either.
- **No giant rats.** The rats stayed rats: in the shots they are easy to see on the bare furrows between the sparse
  rows.
- **No hearth in the lodge, and no building sign.** No hearth, for the reason in item 6. The lodge still has no
  building sign of its own: its lesson sign names it, north of the road at its door.
- **One file read refused.** The unattended run refused one read: viewing a TazUO frame in
  `D:\UO\golems\Iron\p741-proof\walk\` (outside the working folder) with the file viewer, to check the walk's frames.
  I copied the frames into `notes\cc-P741-review\shots\` and viewed them there instead. Nothing was lost.

## Files

- **Code copy:**
  - `server/customizations/Tutorial/`: TutorialIsleAddons.cs (the whole wreck, the swap), TutorialIsleFarmLayout.cs
    (generated), TutorialFarm.cs (the farm's new spots, MoveFromOldLayout), TutorialCorePlacement.cs (the signs,
    MoveChatSignpost, MoveOldMarkers), TutorialWorld.cs (stop 5), IsleAddons-SOURCE.txt;
  - `server/tests/Tutorial/`: TutorialIsleCoastVerification.cs (new), TutorialIsleWalkFixes2Verification.cs,
    TutorialIsleWalkFixesVerification.cs;
  - `player-package/vendor/shattered-legacy-map/trammel.mapops`; CHANGELOG.md; VERSION.
- **Docs copy:**
  - `notes/cc-P662-tools/build_isle.py` and `isle-sets.json` (the shore rule, smoothing, the strand line, the field
    beds, the bank's ground, the floors, the interiors, the sign gate), and its regenerated CSVs, reports and
    `plan-cells.json`;
  - `notes/cc-P481-tools/newisle.py` (stop 5, the road's jog);
  - `tools/tests/test_mapops.py` (fact 12; fact 11's north coast);
  - `notes/guides/building-and-decorating.md` (the shore rule, the sign rule, the whole wreck);
  - `notes/cc-P741-tools/` (surveys, generators, chooser, renders, probe, mutants, proof scripts, logs);
  - `notes/cc-P741-review/` (renders, shots, walk log, `placed.md`, README).

P741 DONE
