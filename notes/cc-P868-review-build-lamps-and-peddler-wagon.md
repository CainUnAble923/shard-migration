# cc-P868: build review of P858 (real-light lamps and the Festival Peddler's wagon)

## In plain words

- I checked the fortune teller's wagon that P858 puts beside the Festival Peddler's stall in New Haven, and the eleven
  new lamps, against the building guide.
- The lamps and the new steps up to the wagon's porch are good: the steps climb the right way and a real character
  walked up and back down without sticking.
- The wagon's roof is not: four glowing green rune symbols, a grey "vent" and a black cat sit on top of it, and the
  guide says nothing goes on a roof (the same kind of "small gray structure" you turned down on the isle farmhouse).
- Nothing for you to do: the Iron Golem gets the three fixes below, and the wagon merges after they are done.

Iron Golem, 2026-11-10. Reviewed `origin/golem/Iron/P858` in both copies (fetched, not checked out), against
`notes/guides/building-and-decorating.md` read in full. Looked at: `notes/cc-P858-review/placed.md`, `walk-log.txt`,
the three renders (`main-stall-wagon-3647-2632.jpg`, `main-wagon-cutaway.jpg`, `wagon-design.jpg`), the three lamp art
sheets, `release-vanilla-stall-yard.jpg`, all ten TazUO shots, the notes `notes/cc-P858-lamps-and-peddler-wagon.md`,
and the code diff (`FestivalWagon/FortuneTellerWagon.cs`, `FortuneTellerWagonDesign.cs`, `ShardLamps.cs`, the stores).

BUILD REVIEW P858: FAIL

1. **Four rune glyphs on the roof (0x4862 at 3649,2630,52; 0x4856 at 3649,2635,50; 0x4856 at 3647,2631,56; 0x4844
   at 3647,2635,56; placed.md parts 92, 93, 156, 190; `FortuneTellerWagonDesign.cs` rows at lines 108, 109, 172,
   206).** They are the author's hidden light emitters (`LightType.ArchedWindowEast`), but our client draws them: every
   shot from the default camera (`p858-stall-and-wagon.jpg`, `p858-porch.jpg`, `p858-stair-going-down.jpg`) shows four
   bright green symbols lying on the shingles. The guide wants a roof with nothing on it (checklist 1, 2.3 "no props",
   2.6). Take them out. If the window glow is wanted, give the light to a part that is already inside and drawn as a
   light (the lantern 0x0A22 at 3649,2636,30 and the lamp stand 0x4C53 at 3646,2631,20 already carry Circle300; the
   stained glass window 0xA5F8 at 3650,2630,20 carries Circle150), or to a part whose art the client does not draw,
   proven by a render and a shot that show no mark on the roof.
2. **The vent sculpture 0x2419 at 3648,2633,53 (part 89, named "A Vent", line 105) stands on the roof's ridge.** In the
   shots it is a pale grey lump on the ridge, exactly what Chase rejected as a "small gray structure" on the isle
   farmhouse roof (guide 2.1, 2.3: no chimney standing apart, nothing on the roof). Take it out.
3. **The black cat 0x4689 at 3650,2629,47 (part 75, "You notice a black cat looking down at you", line 91) sits on the
   roof's north-east corner.** A prop on a roof (checklist 1, 2.3). Keep the cat and its line, but move it off the
   roof: onto the porch deck (z 21) on a tile clear of the walk line from the stair to the door (the walk uses
   3647,2636-2637, so for example 3646,2637 if the stool and keg leave it free), or to the bench at the wagon's north
   end (0x0B2D at 3647-3648,2627,21).

After the fixes: redo `wagon-design.jpg`, the main render and the outside shots so the roof can be seen bare, update
`placed.md` (the part count) and fact 6's count (212), and keep every other part as it is.

## What passed

- **The stair (14 parts).** Light wood north steps 0x0722 at 3647 and 3648, y 2641..2638, z 0, 5, 10, 15, climbing
  north toward the porch it serves; blocks 0x0721 under the two upper steps; one step per tile, 5 a step; the top
  step's top 20 against the porch deck's 21 (guide 4.2). Walked for real both ways in TazUO (`walk-log.txt`: 0, 0, 2,
  7, 12, 17, 21, 21, 19 and back), shots from the foot, the porch, inside and going down. The stair's side shows only
  its blocks and steps from the default camera; nothing on its tiles.
- **Placed whole, one variant, nothing turned** (guide 3): the design has only one facing, its long side north-south,
  the stair coming down onto the street.
- **Wall-mounted pieces inside face the room:** the daemon mask (east facing, 0x4A93 at 3646,2633) on the west wall
  (x 3645); the throne 0xA586 faces south onto the crystal ball; the painting, stained glass and wheels on the outside
  of the east wall (x 3649) hang on the tile east of it, facing the street.
- **Doorway and walk:** the doorway 0x9B29 at 3647,2635 opens from the porch onto the carpet at z 19; walked in and out.
- **Placement:** on the paved square's west edge, its stair foot reachable, nothing blocking the square's walk
  (P858's `find858.py`), nothing tall south or east of it for the camera.
- **Lamps:** store items, not placed in the world; eleven laid on the proof shard, all lit by double-click at night,
  the dragon lantern turned and stayed lit (shots `p858-lamps-*.jpg`, `p858-lantern-turned.jpg`). Art read from
  tiledata and rendered (`lamp-art-1..3.jpg`).
- **Appears on an existing world by itself** (guide 7): `TopUpWagon` at load and hourly.

## Seen, not part of the verdict

- The release's New Haven has no spot for the stall or the wagon (P858's notes, "Both New Havens"); a release prompt
  is needed before this goes to the testers. Not a build fault of P858.
- An oak and a dead tree of the SoS map stand right against the wagon's west side and porch; they are behind it from
  the default camera and hide nothing, so I let them stand.
- The wagon is named by its painting on the east wall ("Fortune's For Tell, Lucky Charms", 0x403E), not by a sign on
  the north side of a path; it is a stall's wagon, not a building, and the stall beside it has its own sign.
- Skeletons from pinned post-UOML spawners walk the square (already in P858's notes).

## Deviations and decisions for Chase

- I wanted to run `Grep "class LightSource"` in `D:\UO\ModernUO-pinned\Projects\UOContent` to name a stock invisible
  light part for fix 1; the unattended run denied it. Fix 1 is written so it does not depend on that class.

P868 DONE
