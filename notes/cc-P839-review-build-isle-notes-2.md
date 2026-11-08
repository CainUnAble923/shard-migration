# cc-P839: build review of P837 (the League lodge door, merged onto main)

## In plain words

- **The lodge door work passed its build review.** The door now sits in the lodge's east wall, facing the road, with a
  brick walk and a fire on each side. The bank work from the last few days is still there.
- **What you will notice:** once a player package with this map ships, you walk from the road down a brick path to the
  lodge's side door, and Elara faces you as you come in.
- **Nothing for you to do.** P837 can merge.

Iron Golem, 2026-11-08, on `golem/Iron/P839`, review only, no files of the build changed.

BUILD REVIEW P837: PASS

## What I looked at

- The guide `notes/guides/building-and-decorating.md`, in full.
- `origin/golem/Iron/P837` in both copies (fetched, branch not changed): `notes/cc-P837-review/` (placed.md, 2 new
  merged isorenders, P818's renders and 12 TazUO before/after shots, door-test.png), the notes
  `notes/cc-P837-cont-fixup-isle-notes-2.md`, Codex's review, and the code diff.
- The map patch diff (`trammel.mapops`, main...P837), line by line against placed.md:
  - 0x04A9 floor (1193) gone from 6782,3995 and 0x0058 (88) run piece put there: the old north door tile is plain wall
    with no floor under the north row (2.2).
  - 0x0057 (87) gone from 6787,4000: the new door's opening.
  - 0x0B26 candelabra (2854) 6786,3998 -> 6786,3999, off the east window's floor tile (11.4, 11.13).
  - 0x0E31 brazier (3633) gone from 6786,4000 (the door's inside tile); two added outside at 6788,3999 and 6788,4001.
  - 0x1589 banner (5513) 6788,4000,8 -> 6788,4002,8, off the door tile.
  - 0x0525-0x0528 (1317-1320) bricks at 6788,4000 and 6789,3990-4000, all at Z 0.
  - Exactly placed.md's list; nothing else of the lodge moved.

## Checks, one by one

| Check | Result |
|---|---|
| Walls and corners | Lodge (OSI stone shop set): post NW, L corner SE, unchanged; the merged cutaway shows every corner whole. The filled north wall tile reads as a plain run with no gap or stub (`lodge-old-door-after.jpg`). Bank unchanged from main. |
| Door | 0x06B3 DarkWoodDoor NorthCW at 6787,4000 stands in the east wall's line (cutaway, `lodge-inside-after.jpg`, `lodge-door-step-after.jpg`); `door-test.png` shows the facings side by side; NorthCW folds north along the wall, not out over the walk. Opens onto the lodge's own room. Approach (6788,4000, 6789,4000) holds only the walk. |
| Stairs | None placed. |
| Wall-mounted items | Banners 0x1589 at 6788,3997,8 and 6788,4002,8 hang flat on the east wall from outside, as guide 3 has them, one either side of the door. Notice board and torches inside unchanged. |
| Roof | Shingle roof sits on the walls, nothing on it; no grey ceiling squares on either west eave (P823's fix kept). |
| Signs | Two 0xA854 signposts (lodge, lesson 8) at 6788-6789,3984, north of the road at the walk's mouth, reading from the south (`lodge-walk-mouth-after.jpg`); the bank's at 6757,3982 by its path. Signposts, not rune markers. |
| Heights | Walk all Z 0 on flat grass; P818's `walk-lodge.log` walked it both ways (P826 checked it). No bridge or dock touched. |
| Shores, foliage | Not changed; nothing grows on the walk or within the door's approach. |
| Better piece on disk | Sandstone bricks for a path and braziers at a hall door are the guide's own picks (9.1 floors, Guild hall braziers). Nothing better listed. |
| Merge | P818's 22 map lines exact on main; main's P817 bank moves and P823 ceiling removals kept; gated build EXIT=0, 3311 tests (from P837's notes). |

## Small observations (not fixes)

- The brazier at 6788,4001 stands just outside the east window 6787,4001. Guide 11.4 is about furniture inside in
  front of a window; from the default camera the window still shows in the shots, so I do not count it.
- P837 took no new TazUO shots; they are P818's (passed by P826). The map lines and server spots are byte-for-byte
  P818's, so the shots still show what ships. The two new merged isorenders agree with them.

P839 DONE
