# cc-P847: build review of P846 (the isle release diff for P818 + P837, the League lodge door)

## In plain words

- **The lodge-door change for the isle release passes review.** On the release map the League lodge's door sits in the east wall, between two fires, at the end of a brick walk from the road, with the two lodge signposts north of the road.
- **It is the same lodge that already passed review on main.** The release map change is line for line the change P818 made (and that its review passed), and the server code is byte for byte main's.
- **Nothing for you to do.** The integrator merges P846; the overseer then applies its diff to the isle release as P846's notes say.

Iron Golem, 2026-11-08. Fresh session; I did not build P846. Branch looked at: `origin/golem/Iron/P846` (docs copy). The
code copy has no P846 branch: P846 changed only the release worktree and left its work as a diff file in the docs copy.

## What I checked

Guide: `notes/guides/building-and-decorating.md`, read in full (checklist, 2.2-2.6, 3, 4, 5, 6, 8, 10, 11).

**The review folder** `notes/cc-P846-review/` has `placed.md` and three TazUO shots (`lodge-road-west.jpg`,
`lodge-walk-mouth.jpg`, `lodge-door-step.jpg`). P846 placed nothing new; its placed list is P818's.

**The map patch is P818's, line for line.** I took the `trammel.mapops` +/- lines from P846's release diff
(`notes/cc-P846-tools/p846-release-isle-20261028.diff`) and from P818's own release diff
(`notes/cc-P818-tools/p818-release-isle-20261028.diff`), sorted both and compared: 22 lines each, identical. Read
against `placed.md`:

| Line | Item | Check |
|---|---|---|
| -6787,4000,0 0x0057 | east wall run piece removed | the door's opening; the floor under the east column stays (2.2) |
| -6782,3995,0 0x04A9 / +6782,3995,0 0x0058 | old north door: floor out, east-west run in | a plain run piece in a north wall (stone shop set 0x0058 = E-W), no floor under the north row (2.2) |
| +6788,3999 / +6788,4001 0x0E31 | braziers outside the east wall | beside the door's approach, not on it (2.4 two-tile approach clear) |
| -6786,4000 0x0E31 | inside brazier removed | it stood on the door's inside tile |
| 6786,3998 -> 6786,3999 0x0B26 | candelabra | off the east window's floor tile 6786,3998 (11.4, 11.13) |
| 6788,4000,8 -> 6788,4002,8 0x1589 | League banner | off the door's tile, flat on the east wall from outside at Z 8 (3) |
| +6788,4000 and 6789,3990-4000 0x0525-0x0528 | sandstone brick walk at Z 0 | flat, variants mixed (9.1), joins the road at y 3989 |

**The server code is main's.** The post-image blob hashes in P846's diff equal `main:` in the code copy for
`TutorialCorePlacement.cs` (63febed) and `TutorialWorld.cs` (3a16f22), so the door (0x06B3 `NorthCW` in the east wall
line, folding north along the wall), the moved signposts and Elara's facing are exactly what P818's review passed.

**The shots, one by one:**

- `lodge-walk-mouth.jpg` (on the road at the walk's mouth): the walk runs straight south from the road and turns west one
  tile to the door; both braziers flank the door in the east wall; the two banners hang flat on the east wall, one north
  of the door near the window, one south of the south brazier. The two 0xA854 signposts stand **north** of the road
  beside the walk's mouth and read from the south (6). Roof sits on the walls, nothing on it (2.3).
- `lodge-door-step.jpg` (at the walk's foot): the door leaf sits in the east wall's line between the fires (2.4);
  windows show on the west and east walls; whole corners at the south-east (L corner) and the roof's eaves on the walls.
  The approach tile 6788,4000 holds only the walk. No stray item on the roof.
- `lodge-road-west.jpg` (arriving from the bank): the road bends east to the lodge, the end of the brick walk and the
  signposts show at the right edge; the bank square's fountain at the top. No grey squares on the visible roof (P823 kept).

**Walls, corners, stairs, roof, inside:** unchanged from P720/P751 and already passed in P818's review
(`notes/cc-P818-review/`: isorender, cut-away, inside shot, `door-test.png`, `walk-lodge.log` both ways). The release
map's lodge lines are identical to those, so they carry over. There are no stairs, bridges or docks in this change.
**Signs** are signposts, not rune markers. **Foliage:** none added; the walk keeps clear of plants.

## Observations (not this build's work, no fix asked)

- `lodge-door-step.jpg` shows the coast south-west of the lodge as a row of one-tile teeth (sea south of the sand, a
  diagonal near coast). That is the existing isle shore (guide 5 and 11.14), not touched by P818 or P846. Worth a look
  in a later shore pass.
- P846's review folder has only the three outside shots, no isorender, inside shot or walk log of its own (guide 8). I
  accept P818's for this port because the map lines and server files are identical; a port that changes any line
  should leave its own.

BUILD REVIEW P846: PASS

P847 DONE
