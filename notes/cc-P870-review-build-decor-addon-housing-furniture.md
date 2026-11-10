# cc-P870: build review of P867 (fix-up of P855's decor addons and housing furniture)

## In plain words

- **Most of the furniture looks right.** All ten grey fireplaces, both country kitchens, both harpsichords, the blue
  couches and the holiday fireplace face into their rooms with their backs on the right wall.
- **The two small corner kitchens are not right yet.** Their marble counter stands two tiles out from the corner
  walls and closes off a 2 by 2 patch of floor behind it. Nobody can walk in there, and the sink faces that patch.
  In the test shot a potted tree from the town building is trapped inside it.
- **Some proof shots are spoiled by a town banner.** In one New Haven room, an orange banner already hung on the
  wall. It shows through the middle of the holiday fireplace, the south couch, the south kitchen and three south
  fireplaces in their shots.
- **Nothing for you to do.** The verdict is FAIL, and the three fixes below go back to the Iron Golem. Your open
  question from P867 is still open: should the medium and grand fireplaces be trimmed by one so they fit under an
  upper floor?

Iron Golem (a fresh session), 2026-11-10. I read the guide in full and fetched `golem/Iron/P867` in both copies
without switching branches. I looked at every one of the 19 `town-*.jpg` renders. I opened the TazUO shots for the
holiday fireplace, the small east fireplace, the north-west kitchen and the south couch, and enlarged the kitchen
crops. I checked `placed.md` against the diff's 30 `.cfg` files, and read the SoS map's statics behind each shot spot
with P678's `sosbase` (my probe is `probe870.py` in my scratchpad; nothing was written to either copy except this
file). I did not rebuild anything.

## What passed

- **Facing, every wall-backed design.** The east facings stand on a west wall and the south facings on a north wall,
  as `placed.md` part 1 says (guide 3):
  - the grey fireplaces (small, low, medium, large, grand): mantel along the back wall, hearth and fire open into
    the room;
  - both country kitchens: hutches on the back wall, the counter in front of them;
  - both harpsichords: keyboard and bench toward the room;
  - the blue couches (east and south): back to the wall;
  - the holiday fireplace: on the north wall, the bear rug in front.
- **The country kitchen's stove.** The south kitchen uses 0xA2A9, which tiledata names "Wood_Stove_1_East". Drawn
  alone (with 0xA2A3-0xA2AA beside it), 0xA2A9 shows its fire door on the south face, as 0xA2A8 "Off_South" does. So
  it is the south stove with a wrong name, and the facing is right. The east kitchen's 0xA2A5 opens east. Right too.
- **The "windows" behind the east spots are not windows.** The blue arches above the west wall at 3623,2570-2575
  are energy-field statics (0x3956) outside the building at x 3622. The wall itself is solid weathered stone (0x01D1
  at Z 0 and 20), so no piece stands in front of a window (guide 11.4).
- **The holiday fireplace fix (P864 item 3).** The fieldstone wall box is gone. The surround (0x29B0, mantel 0x0025)
  stands on the house's own north wall with no second wall and no stubs.
- **Nothing stray on top.** No piece of any design stands above its own top course.
- **Out of scope for this review:** walls, doors, stairs, roofs, signs, shores, bridges and foliage. Nothing is
  placed in the world: these are house addons placed from a deed.

## Verdict

BUILD REVIEW P867: FAIL

1. **small-kitchen-northwest (0x99C8 at 3668,2592-2594, 0x99CB 3667,2594, 0x9A15 3666,2594) and
   small-kitchen-southeast (0x99C9 at 3609-3611,2577, 0x9A17 3609,2578, 0x9A19 3609,2579): the counter shuts off
   its own corner.**
   - **What is wrong.** Both designs put the L on the far side of their 3 by 3 tiles: offsets +1 column and +1 row
     for the north-west one. The download's `KitchenNWAddon.cs` lays it out the same way. So when the design stands
     in its corner, the counter is two tiles from both walls. It closes a 2 by 2 pocket behind it:
     - north-west: 3666-3667,2592-2593;
     - south-east: 3610-3611,2578-2579.
   - **Why it matters.** Every counter piece is impassable, so the pocket cannot be reached. The sink is on the
     pocket side. In the shot (`town-small-kitchen-northwest.jpg`, `shots/p867-small-kitchen-northwest.jpg`), the
     town's potted tree 0x11C9 at 3666,2592 is trapped inside. `placed.md` calls the design "against the north and
     west walls", which it is not.
   - **What the guide wants.** Guide 3: a counter faces its room with the keeper behind it. Guide 2.5's bank counter
     has "a gap at one end" so the keeper can get behind it.
   - **The fix.** Either:
     - make the keeper side reachable: leave a gap at one end of the L (drop or move the end piece, through the
       converter's `DROP` rule as for the holiday fireplace); or
     - re-cut each design so its L backs onto the two walls.

     Then correct `placed.md`'s description, and re-shoot at a spot with nothing inside the 3 by 3.
2. **The north-wall spot at 3581-3585,2583: a town banner on the back-row tiles.**
   - **What is wrong.** The SoS map has wall banners at 3583,2583,0 (0x15A8) and 3584,2583,0 (0x15A9), hung on the
     north wall. They sit on the same tiles as the back row of six designs. In the renders and shots, the orange
     banner draws across the middle of each piece:
     - holiday-fireplace (over the 0x29B0 surround at 3584,2583);
     - blue-couch-south (over the pillows 0x163B/0x13A5 at 3584-3585,2583);
     - country-kitchen-south (over the lantern 0xA26D at 3583,2583);
     - grey-fireplace-low-south, -large-south and -grand-south.
   - **Why it slipped through.** `town867.py` counts only items with height, or impassable ones, as clutter. Wall
     art is height 0, so it passed.
   - **What the guide wants.** Guide 3 says to "check every piece from the default camera in the shots", and 2.6
     says nothing stray. A banner across the piece hides what is being checked.
   - **The fix.** Make `town867.py` treat any item on a back-row tile as clutter, height-0 wall art included. Then
     re-shoot those six designs at a clear north wall, or clear the two banners on the private shard's copy before
     the shots.
3. **grey-fireplace-medium-south (0x0519 grey paver at offset 2,-1,0; 3621,2610,0 in the shot): a doubled piece.**
   - **What is wrong.** The `.cfg` lists that offset twice, and so does `placed.md` (lines 229-230). That is why
     the file has 41 pieces against the east file's 40.
   - **The fix.** Drop the second row (guide 2.6: no doubled pieces). Then set fact 1's piece count to 641.

Not a fail item, noted for the fix-up: the medium and grand fireplaces are 21 high (0x071E at Z 11, height 10).
Guide 11.3 is about exactly this (a tall piece comes through the floor above). P867 asked Chase about it rather than
change the design, and the house rules refuse it under a floor. In the grand-south town shot, staff placement put its
top 1 Z into the flagstones at Z 20. That cannot be seen in the shot. Leave it to Chase's answer.

P870 DONE
