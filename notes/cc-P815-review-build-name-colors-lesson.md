# cc-P815: build review of P801 (the New Haven jail)

## In plain words

- The new jail for the Name Colors lesson looks right in most places: the walls, roof, door, windows, sign, cells and furniture follow the building guide, and a real character walked in and out on both versions.
- It does not pass yet, for four small things: a stray bit of wall sticks out at the jail's south-west corner, a wall torch hangs on a window, two orange torch-light patches show on the roof from the street, and the marked crate the lesson sends you to is hidden behind the south wall.
- These go back to the Iron Golem as a fix-up. Once they are fixed the jail can merge.
- Nothing for you to do.

## State

Gold Golem, 2026-11-07. Reviewed `golem/Iron/P801` (shard-migration `a63fb6df`, ShatteredLegacy `c1df67f`) without changing my branch. I read the building guide, `notes/cc-P801-review/placed.md`, the P801 notes and the generator `notes/cc-P801-tools/gen_jail.py`, which makes `TutorialJailLayout.cs`. I looked at all four renders (with and without the roof, main and stock), both contact sheets and the door, hall, crate and after shots on both builds. I zoomed in on the corners and the west wall. I did not change any of the build's files.

## What passes

- **Corners NW, NE, SE:** post 0x0036 at the NW, 0x0034 along the north row up to and including the NE tile, 0x0035 down the east column, L-corner 0x0033 at the SE (guide 2.2).
- **Floor:** pavers 0x0519 inside the box and under the south row and east column, not under the north row or west column.
- **Windows:** 0x003B in the south wall, 0x003C in the west and east walls. Each matches its wall.
- **Door:** MetalDoor WestCCW in the south wall line at x+5. The open shot shows it folded along the wall (2.4).
- **Sign:** hanger 0x0B98 and brass board 0x0BD2 two tiles east of the door, just outside the south wall, at floor - 2. Named "The New Haven Jail". It stands north of the road and does not cover the door (2.5, 6, 11.5, 11.12).
- **Roof:** shingles 0x05C4/0x05C2/0x05C3 cover x0+1..x1+1 and y0+1..y1+1, pitched along y. The eaves are at floor + 19, rising 3 per course, with the ridge at the middle column. Grey brick gable 0x0055 fills the south row at every course. No props on the roof (2.3). See item 3 for the light.
- **Cells:** 0x0035 dividers, iron fence 0x0821 running east-west, and a static closed gate 0x0828 in each cell front. Hay 0x0F34 and shackles 0x1262 hang on the north walls.
- **Hall:** writing table 0x0B4A with the ledger and a scroll on top. Benches 0x0B2C along the bars, facing the right way.
- **Walks:** the trainee walked in through the real door and back out on both builds, Z 20 to 21 on main and 10 to 11 on the release (4.1).
- **Not part of this build:** no stairs, shore, docks or new foliage.

## Verdict

BUILD REVIEW P801: FAIL

1. **0x0034 grey brick "south" piece at the south-west corner tile: main 3702,2634 + (0,8) = 3702,2642,21; release 3469,2605,11.** The south-west tile holds both 0x0034 and 0x0035. Zoomed in, the render and `shots-main/2-hall-window-open.jpg` show the south wall sticking out past the west wall's line there, a stub. Guide 2.2 and 11.1 say the south-west tile takes the "east" piece only. The south row runs between the corners. The P734 survey (`notes/cc-P734-tools/stair-survey.txt`) finds 0x0034 only at the NE corner and 0x0035 only at the SW corner in OSI's multis. Fix: in `gen_jail.py`, start the south-row loop at x = 1 (`range(1, W)`, still skipping the door), regenerate `TutorialJailLayout.cs`, and remove the old piece from existing worlds when they load.
2. **Wall torch 0x0A07 on a window: main 3703,2640,34; release 3470,2603,24.** It hangs on the floor tile of the west window 0x003C (main 3702,2640). In `2-hall-window-open.jpg` on both builds, the torch overlaps the window's arch. Guide 11.4 says never hang a torch on a window tile. Fix: move it to a plain west-wall tile. Layout (1,7) works: main 3703,2641,34, release 3470,2604,24. The wall there is a plain 0x0035, and no window has (1,7) as its floor tile. Or drop the torch.
3. **Two orange light patches on the roof's west slope**, over the hall torches: `1-outside-door-and-sign.jpg`, `1b-at-the-door.jpg` and `8-outside-after.jpg` on main, and `1b-at-the-door.jpg` on the release. From the street they read as something on the roof. Guide 2.3 and 2.6 say nothing stray on the roof, and 11.3 says tall or lit pieces against a side wall come through the low eaves. P801 lists this as unconfirmed. Fix: take the door-side shot again with the west-wall torches removed. If the patches go away, light the hall from a source away from the eave, such as a candelabra 0x0B26 standing by the warden's table, or put the torches back only if the new shot is clean. Leave the before and after shots.
4. **The marked crate 0x0E3D (TutorialJailCrate, hue 0x22) is hidden: main 3711,2641,21; release 3478,2604,11.** It stands in the south-east corner, right inside the south wall, which hides it from the default camera. In `4-crate-gray-name.jpg` only a red sliver shows behind the wall. The lesson sends the player to it by name. Guide 3, 9.2 item 7 and 5's "keep clear: reachable and visible" say lesson items and tall pieces go toward the north and west, with open floor toward the south-east. Fix: move the crate's spot (`TutorialJail.cs` CRATE) to a hall tile in view. For example, layout (7,4) beside the bench (main 3709,2638, release 3476,2601), kept off every window's floor tile and the door line. Move the existing crate when the world loads, and show it in the hall shot.

P815 DONE
