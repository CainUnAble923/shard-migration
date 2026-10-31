# cc-P751 review folder (for the build reviewer)

The task: fix the seven items of P748's build review of P746 (the P741 isle round). Notes:
`notes\cc-P751-isle-round-review-fixes.md`. Every piece placed: `placed.md` (one line a piece; its first section lists
what P751 changed, its farm section names the wall each farmhouse piece stands against). P741's own folder
(`notes\cc-P741-review\`) is unchanged and still shows the rest of the round (the wreck, the signs, the bank).

## Renders (isorender, client-correct statics; the server's farm, signs and addons drawn in)

| Subject | Before (P746) | After (P751) |
|---|---|---|
| Whole isle | `before-whole-isle.jpg` | `after-whole-isle.jpg` |
| Farm (field, gate, farmhouse) | `before-farm.jpg` | `after-farm.jpg` |
| Fence corners, north-west (left) and south-east (right) | (in `before-farm.jpg`) | `after-fence-corners.jpg` |
| Farmhouse, roof on (nothing on the thatch) | | `after-farmhouse.jpg` |
| Farmhouse, roof off | `before-farmhouse-inside.jpg` | `after-farmhouse-inside.jpg` |
| Lodge, roof on, and roof off | `before-lodge-inside.jpg` | `after-lodge.jpg`, `after-lodge-inside.jpg` |
| The yard's south-west beach | `before-coast-south.jpg` | `after-coast-south.jpg` |

The renders do not draw doors or NPCs (server items); the TazUO shots show everything.

## TazUO shots (`shots\`, the default camera, private shard 127.0.0.1:2596, image `sl-modernuo:cc-P751`, this branch's map)

See the list in the notes (section "Live, on a private shard"). The door-side shots of the farmhouse and the lodge,
the farmhouse inside with its hearth, the fence corners, the yard's beaches, and frames of the walk at each door.

## Walk log

`isle-walk.log`: Iron the Tester walked the isle in TazUO with the client's own steps (no teleport), 292 steps in 19
legs: the west beach past the wreck, every lesson leg from the wake spot (stop 0) to the dock end (stop 10), in and out
of the farmhouse (its step and door), the bank door and the lodge door, and the dock back to the land. Each line is one
step: the position with its Z, the change in Z from the step before, and the Z the builder's walker expected. The route
is `notes\cc-P751-tools\walk-paths.json` (`walk_paths.py`).

**Result: 19 of 19 legs, 292 of 292 steps, no step over 4 in Z.** 289 steps stood at the walker's Z. The 3 others
are on the moongate platform at the dock end, (6829,3990) and (6830,3991), where the game stands the Tester on the
stone floor at Z 0 and 4 and the walker modelled -2. Shots: `shots\walk-*.jpg` (mid and end of each door leg, the
beach and the dock) and `shots\isle-walk-f*.jpg` (every fifth frame).

## What to check (the P748 list)

1. This folder: `placed.md`, renders, shots, the walk log.
2. Fence: post 0x0838 at 6677,3967; one L 0x0835 at 6695,3983 (and at 6695,3973 where the pen meets the east fence).
3. Farmhouse hearth: StoneFireplaceSouth (0x0967 + 0x0961) at 6702-6703,3973 on the north wall under the ridge; the
   roof-on render and shot show nothing on the thatch. No furniture before a window (the bed, barrel and box moved).
4. Farmhouse door: WestCCW (0x06A9), opens along the south wall; rehung in place on an existing world.
5. Lodge sign: a standing signpost "The League lodge" at 6781,3989, north of the road where the walk to the lodge's
   north door leaves it, beside the League lesson sign. Laid first at 6784,3994 (two east of the door, outside the north
   wall, as P748 asked), it stood behind the lodge's north eave from the camera: `shots\tazuo-lodge-sign-at-6784-3994-hidden-*.jpg`.
6. Walk: `isle-walk.log`, 19 of 19 legs, 292 steps, no blocked step.
7. The yard's south-west beach: two straight runs (x 6718, y 4014) where the spit's one-tile stairs were.
