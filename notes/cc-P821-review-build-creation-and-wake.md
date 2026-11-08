# cc-P821: build review of P817 (the Wakening Isle bank tidy-up)

## In plain words

- The bank changes themselves are good: the lesson sign is off the road, the bank box and strongbox stand on the back
  wall with the vault chests, the plant that blocked a window is gone and Merrin faces his counter.
- One thing on the bank's roof is wrong, and has been since the bank was first built (P720): a row of eight grey
  squares shows on the west slope. They are the bank's ceiling tiles poking up through the bottom row of the roof.
  You see them when you look at the bank from the road on its west side.
- So the review says FAIL, and the Iron Golem gets a short fix-up: take those eight ceiling tiles out from under the
  roof's edge, then take a clean outside photo.
- Nothing for you to do.

Reviewer: Iron Golem, fresh session, 2026-11-07. I read `notes/guides/building-and-decorating.md` in full, the P817 notes
and `placed.md`, and both diffs (`main...origin/golem/Iron/P817`, code and docs copies). I also looked at all nine images in
`notes/cc-P817-review/`, cropped and enlarged where needed. Nothing in P817's own files was edited.

## What P817 placed or moved (all checked)

| Piece | Check | Result |
|---|---|---|
| 0x09A8 strongbox, 6762,3973,0 (map; old 6766,3974 line removed) | on the back wall's floor tile under the north torch 0x0A0C (6762,3973,13); the wall tile behind it, 6762,3972, is a plain 0x0058 run, not a window | pass |
| 0x11CA potted plant removed, 6766,3978 (map) | it stood on the floor tile of the east window 6767,3978 (guide 11.4 / 11.13); removing it fixes that | pass |
| 0x0E7C practice bank box, 6761,3973,0 (server) | back wall with the chests, clear of the north window's tile 6760,3973; the old one is deleted on load (`MoveOldProps`, matched by ID, name and spot) | pass |
| 0xA854 "Lesson 7: The bank" signpost, 6757,3982,0 (server) | signpost, not a rune marker; on grass north of the road (road y 3983-3986), off the apron (x 6759-6765) and two tiles or more from the door line x 6762 (guide 2.4, 6); the after cutaway shows it on grass with the road south of it. The before shot shows the old one standing in the road at the apron's east end | pass |
| Merrin, 6762,3976, Direction South (server) | behind the counter (y 3977), facing the customer side, the carpet and the door (guide 3: counter serving side toward the door, keeper behind it); in the inside-after shot he stands behind the counter | pass |

Window floor tiles, all seven (guide 11.13): 6759,3979 and 6765,3979 carpet only; 6766,3975 empty; 6766,3978 empty now;
6758,3976 empty (the west torches are on 3975 and 3978, not the window tile); 6760,3973 and 6764,3973 empty. Pass.

## Unchanged P720 pieces, rechecked

- Walls and corners: the stone shop set, post at the north-west, L-corner at the south-east, whole in the cutaway. Pass.
- Door 0x06A9 WestCCW at 6762,3980: hung in the south wall line, closed leaf in the wall in both inside shots. Pass.
- Shop sign 0x0B98 + 0x0C0B at 6764,3981,10: the arm (not 0x0B97), two tiles east of the door. Pass.
- Torches 0x0A0C (north wall) and 0x0A07 (west wall) at floor + 13. Counter row with a gap at the east end, carpet
  from corner and edge pieces, bench, candelabra. Pass.
- Stairs, bridges, docks, shores: none in this build.
- Foliage: the ferns and small palm round the bank are unchanged, and none is on the road or apron. Pass.
- Roof: it sits on the walls, with the gable 0x0069 on the south row. **There are stray pieces on top**, see item 1.
- Brass fountain on its own pad at 6767-6769,3983-3985: unchanged and left for Chase's call, as P817's notes say. Not a review item.
- What to use where (Bank): every piece is the stock bank set the section lists. No better piece is needed.

BUILD REVIEW P817: FAIL

1. 0x049C (the bank's ceiling at Z 20), 6758,3973 to 6758,3980, the roof's west eave column: the eight tiles stand one Z
   above the west slope pieces 0x05C4 at Z 19 on the same tiles. They draw as a row of eight grey squares on the west
   slope (`bank-after-isorender.png` and `bank-before-isorender.png`, the same in both, so this dates from P720 and
   P817 did not cause it). Guide 1 item 1 and 2.3 say the roof covers the box and has nothing on it. Fix: remove 0x049C
   from the x 6758 column, or lower it under the eave there. Do it in `trammel.mapops` and in the driver's layout, so a
   rebuild lays the same. Then re-render and confirm the west slope is plain shingle, as the east one is.
2. `bank-outside-after.jpg`: the paperdoll and TazUO's Version History window cover the lower-left half of the door-side
   shot, including the road side of the new signpost. Guide 8 item 3 asks for an outside shot from the door side with
   each sign readable. After item 1, retake it with those windows closed, so the signpost at 6757,3982 and the roof's
   west slope both show.

P821 DONE
