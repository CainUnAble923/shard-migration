# cc-P825: build review of P823 (fix-up of P817: the Wakening Isle bank roof and the door-side shot)

## In plain words

- The grey squares on the isle bank's west roof slope are gone. The same squares on the League lodge's roof are gone
  too. Both buildings now show a plain shingle roof on that side, from the road and in the renders.
- The outside photos of the bank are clean now: no paperdoll or version window covers them. The bank lesson signpost
  stands on the grass north of the road.
- So the review says PASS, and P823 can merge (it carries P817's isle changes with it).
- Nothing for you to do.

Reviewer: Iron Golem, fresh session, 2026-11-08. I read `notes/guides/building-and-decorating.md` in full and P823's
notes, `placed.md` and Codex review. I read both diffs (`main...origin/golem/Iron/P823`: the map patch
`trammel.mapops`, the driver `notes/cc-P662-tools/build_isle.py` and its CSV). I also read P821's FAIL list and looked
at all ten images in `notes/cc-P823-review/`. Nothing in P823's own files was edited.

## P821's two items

| Item | Check | Result |
|---|---|---|
| 1. 0x049C ceiling at Z 20 on the bank's west eave column, 6758,3973..3980 | `trammel.mapops`: the eight `S+ 6758 y 20 1180 0` lines are gone. The west slope 0x05C4 (1476) at Z 19 on 6758,3973..3981 is untouched. `bank-after-isorender.png` shows the west slope plain, like the east slope; `bank-before-isorender.png` shows the eight squares | pass |
| (same defect) the lodge, 6778,3996..4003 | the same eight lines are gone; `lodge-before-isorender.png` has the squares, `lodge-after-isorender.png` and `lodge-outside-after.jpg` do not | pass |
| The driver | `build_isle.py` skips the west eave column (x == x1) only while `eaveDz` (19) is below the ceiling Z (20), so a rebuild lays the same map. The east side needs no change. I checked the shipped patch: the ceiling at x2+1 (bank 6767, lodge 6787) sits at 20 under the east slope at 22, and the eave column (6768 / 6788) at 19 has no ceiling. The after renders show the east slopes plain | pass |
| 2. Door-side shot covered by the paperdoll and Version History | `bank-outside-after.jpg` and `bank-outside-west-after.jpg` are clear of windows, from the default camera. Both show the door, the hanger sign, the potted plant on the apron, the signpost 0xA854 at 6757,3982 on the grass north of the road, and the plain west slope. `bank-outside-before.jpg` is the old covered shot | pass |

## The checklist, rechecked on the after images

- **Walls and corners:** the stone shop set is whole in `bank-after-cutaway.png` and `bank-inside-after.jpg`: post at
  the north-west, L corner at the south-east, no stubs. No wall piece changed. Pass.
- **Door:** 0x06A9 WestCCW at 6762,3980, hung in the south wall line, leaf closed in the wall (inside and outside
  shots). Pass.
- **Roof:** it sits on the walls, the gable is on the south row, and nothing is on top now that the ceiling squares are
  gone. Pass. Removing the ceiling under the eave opens no hole: the slope at Z 19 covers that column from outside, and
  the client hides everything above a player who is inside.
- **Wall-mounted items:** torches 0x0A0C (north wall) and 0x0A07 (west wall) at floor + 13. The sign hanger is 0x0B98
  with board 0x0C0B outside the south wall. Unchanged. Pass.
- **Signs:** the lesson stop is the signpost 0xA854, not a rune, north of the road. Pass.
- **Stairs, bridges, docks:** none in this build, and nothing walkable changed (the removed tiles are at Z 20 under
  the roof), so there is no walk to prove.
- **Shores and foliage:** unchanged. The ferns and palms stay off the road and the apron. Pass.
- **What to use where (Bank):** every piece is in the stock bank set. No better piece on disk is needed for this fix.
- **Inside:** Merrin stands behind the counter, facing the customer side. The strongbox, bank box and vault chests
  stand on the back wall, and the counter has its gap at the east end, as P821 passed. Pass.

## Outside this review's scope

Codex flagged one medium point on P823's docs side: the release diff's profession filter does not stamp the no-op case,
so `-CheckOnly` marks it stale on every launch. That is launcher code carried over from P817, not a build or decoration
item, so it does not change this verdict. It is already on the overseer's Codex list (`D:\UO\overseer\codex-flags.md`).

BUILD REVIEW P823: PASS

P825 DONE
