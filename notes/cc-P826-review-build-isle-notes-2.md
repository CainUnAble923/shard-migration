# cc-P826: build review of P818 (the Wakening Isle League lodge's door moved to the east wall)

## In plain words

- **The League lodge change passes review.** The door is now in the lodge's east wall, the side you see from the
  road, and it sits properly in the wall and swings along it, not out over the path.
- **The way in reads clearly** in the game shots: a tan brick walk from the road to the door, a brazier burning on
  each side, and the two signposts standing north of the road where the walk starts. Inside, Elara faces the door.
- **A real character walked it** from the road through the door and back, every step level.
- Nothing for you to do. P818 can merge; the lodge change reaches players with the next player package.

Reviewer: Iron Golem, fresh session, 2026-11-08. Branch reviewed: `origin/golem/Iron/P818` at `d6b2c94b` (docs copy)
and the matching code branch. Nothing of P818's was edited.

## What I looked at

- The guide `notes/guides/building-and-decorating.md`, in full.
- `notes/cc-P818-review/placed.md`, the notes `notes/cc-P818-isle-notes-2.md`, the code diff (`TutorialCorePlacement.cs`,
  `TutorialCoreTrials.cs`, `TutorialWorld.cs`, the facts) and the 22-line `trammel.mapops` diff.
- Every render and shot in `notes/cc-P818-review/`: `door-test.png`, `lodge-before/after-isorender.png`,
  `lodge-before/after-cutaway.png`, `lodge-area-before-isorender.png`, `lodge-mockup.png`, and the TazUO shots
  `lodge-road-west`, `lodge-walk-mouth`, `lodge-old-door`, `lodge-door-step` (before and after) and `lodge-inside-after`.
- The walk log `D:\UO\golems\Iron\p818-proof\walk-lodge.log` (not in the branch; see the notes below).

## Checks, one by one

| Check (guide) | Result |
|---|---|
| Walls and corners (2.2) | Pass. Corners unchanged (stone shop set, post NW, L corner SE). The old north door tile 6782,3995 now holds 0x0058, the stone shop set's east-west piece, and its floor static under the north row is gone (the map diff swaps 1193 for 88), as 2.2 wants. The east opening at 6787,4000 drops 0x0057 and keeps the floor under the east column. The north wall reads as one unbroken run in the inside shot. |
| Door (2.4, 3) | Pass. DarkWoodDoor NorthCW, closed 0x06B3 (0x06A5 + 2 x 7, right), in the east wall's line. Open it folds north onto 6787,3999 along the wall, not out over the walk or onto the carpet: `door-test.png` and fact 1. It opens onto the lodge's room. The two-tile approach (6788,4000, 6789,4000) holds only the walk. The old north door is taken away on load. |
| Stairs (4.2) | None placed. |
| Wall-mounted items (3) | Pass. The banner 0x1589 moved off the door to 6788,4002,8, flat on a plain east-wall tile from outside, as P720's banners hang; the other stays at 6788,3997. The inside brazier left the new door's tile; the candelabra 0x0B26 left the window's floor tile 6786,3998 for 6786,3999. Both east windows' floor tiles are empty (11.13). |
| Roof (2.3) | Pass. Unchanged, sits on the walls, gable on the south row, nothing on it. The two braziers stand on the grass under the east eave and draw clear of it in every shot. The grey squares on the west slope are the known ceiling flaw that P823 fixes, not this branch's. |
| Signs (6) | Pass. Both are standing signposts 0xA854, named, no rune markers: "The League lodge" at 6788,3984 and the Lesson 8 sign at 6789,3984, north of the road (y 3985-3989) at the walk's mouth, readable from the south (`lodge-walk-mouth-after.jpg`). The old ones are moved on load. |
| Walkable joins (4.1) | Pass. The walk is flat floor statics 0x0525-0x0528 at Z 0 on grass. The log shows a real TazUO character from 6789,3988 down the walk, through the door to 6784,4000 and back to 6789,3988, every step at Z 0, "ALL LEGS WALKED". |
| Shores, bridges, docks | Not touched. |
| Foliage (5, 2.6) | Not touched. No plants on the walk or in the door's approach. |
| Better piece on disk (10) | Pass. Sandstone bricks match the bank square's apron; brazier 0x0E31 is the guild-hall pick for light. Nothing in What to use where fits better. |

## Notes (not blocking)

1. **The walk log is not in the branch.** placed.md and the notes cite `walk-lodge.log`, but it is only in
   `D:\UO\golems\Iron\p818-proof\`. Guide section 8 item 4 asks for walk logs in the review folder. I read it there and
   it proves the walk. A later Iron prompt could copy it into `notes/cc-P818-review/`.
2. **`lodge-mockup.png` is the same file as `lodge-after-isorender.png`** (same md5, 373bda51...). The notes say it is
   the isorender with the server's door and signs drawn in, but the door only shows because the isorender reads the
   map. The TazUO shots show the server's door and signs, so nothing is missing from the proof.
3. The south brazier (6788,4001) stands outside the east window 6787,4001. Rule 11.4 is about furniture inside, and
   from the camera the brazier draws below the sill, so I left it.
4. No shot of the lesson window or Elara's call (the notes say why). Facts 5 and 6 cover them. They are text, not
   building work.

BUILD REVIEW P818: PASS

P826 DONE
