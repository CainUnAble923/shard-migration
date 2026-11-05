# cc-P805: build review of P799 (League ankh, New Haven lessons)

## In plain words

- **P799 does not pass yet.** The ankh itself is fine and works on both versions, but several small things around the New Haven lessons are placed wrong, so it goes back to the Iron Golem with a list.
- **What a tester would notice:** only one of the two blue figures in the theater music lesson can be seen from the floor, because the stage's overhang hides the other. Rook's bench is two short stubs instead of one bench, and Rook sits with his back to the square.
- **Three of the four new signposts stand on the wrong side of the road,** against the "all signs north of the path" rule. Two of those have no good spot nearby that meets the rule, so you may get a question about them.
- **Nothing for you to do.** The Iron Golem gets the numbered list below, and P799 stays unmerged until the fix-up passes.

## Verdict

BUILD REVIEW P799: FAIL

## Fixes

Coordinates are stock New Haven, Trammel (the release branch) unless marked main.

1. **Rook's bench, 0x0B2C at 3502,2530,22 and 3503,2530,22: wrong piece for an east-west bench.** `0x0B2C` runs north-south, so two of them side by side along x draw as two separate crosswise stubs (`5-rook-bench.jpg`; `cc-P805-evidence\bench-0B2C-left-0B2D-right.jpg`, left). The east-west piece is **0x0B2D**, which joins into one bench (right). The guide's 11.2 says to read each facing from the art. `HavenSpots.cs` and `placed.md` both call 0x0B2C "east-west". Main has the same two pieces from P743 at 3669,2636,0 and 3670,2636,0: change them too. For section 7, upgrade in place: `HasPiece` and `StrayPieces` match on ID, so a world already seeded would keep the old 0x0B2C pieces under the new ones unless the seed takes them away. Update the facts that pin 0x0B2C.
2. **Rook, 3502,2530,22: faces away from the square.** `Direction.North`, in `MoveRook` and on the `rookMissing` line of `TutorialCorePlacement.cs`, points him at the Inn's low wall one tile north, with his back to the yard, to the moongate exit at 3502,2532 and to the square, which is south. The code's own comment says "facing the square". Section 3 wants seats to face their room. On the release it should be **`Direction.South`** on both lines, with `AnOlderWorldsRookMovesToHisBenchByTheTavern` changed to match. A world where Rook already sits on the bench must be turned too, as `FindOldRook` skips him there. Main's facing was not checked here: look at it while changing fix 1.
3. **Bard echoes, 3410,2603,60 and 3411,2604,60: not visible from the lesson's spot.** A flat canopy (0x07BD at Z 80, trimmed by 0x0110) covers x 3410-3411 of the stage. From 3414,2602,55 and the default camera it draws over echo A completely, and echo B stands half behind the curtain at 3411,2605 (0x011B, 0x043B). `2-theater-echoes-on-stage.jpg` shows one blue figure while the lesson says "the two blue human figures". `cc-P805-evidence\stage-echo-spots-with-canopy.jpg` has a crate on A's tile (hidden) and a box on B's. P799's `stock-theater.jpg` leaves the canopy out, so it could not show this. Move both to the open planks at x 3412-3413. My suggestion is 3412,2604,60 and 3413,2603,60, clear of the Actor's 3412,2602 and of the stairs at 3413,2605; neither was tried in a client. Then shoot it with the lesson gump closed and both figures in view (section 3, check every piece from the default camera). P799 did not play this lesson in a client, so this is also its first real test.
4. **Signpost 0xA854, 3521,2573 (stables): stands at the road's edge, behind the stock shop sign.** Land read from the map: the sign's own tile is dirt, 3521,2572 directly north and 3520,2573 directly west are cobblestones, and dirt road runs on north to about y 2569. Section 6 wants "road within 3 tiles south of the sign, none north of it or beside it". `stock-sites.md` calls it a shoulder "off the cobbles", which the land does not bear out. Its post also draws through the stock stables sign (`5-stables-sign.jpg`), so the two read as one tangle. Move it clear of the stock sign. The only tiles my check found that meet the rule are the bank at 3517-3519,2564-2565, Z 20, about 15 above the road, which may read badly. If no tile works, record it in `placed.md` as a deviation and put it to Chase.
5. **Signpost 0xA854, 3477,2617 (mine): on the south side of its road.** Land read from the map: road directly north (3477,2616) and west (3476,2617), grass south. 0xA854 reads from the south, so its board faces away from the road and from a walker leaving the gate. P799 flags that the road runs north-south, which is fair, but this spot leaves the board facing no part of the road. Two ways: a tile that does meet the rule, the nearest clear one my check found being **3469,2624, Z 12**, about 9 tiles south of the gate (hilly here: render and walk it); or the west shoulder with **0xA855**, the face that reads from the east, so the board faces the road. The first keeps to Chase's rule as written.
6. **Signpost 0xA854, 3464,2596 (housing stop 1): south of its road.** Land read from the map: road at y 2595 directly north, grass south, so it has its back to the street a walker arrives on. "Beside the stop, within 2" and "north of the path" cannot both be met at stop 3465,2596: the only legal tile near is 3465,2589, Z 30, on the bank. Either move stop 1 and its sign together so both hold, or record the deviation in `placed.md` and ask Chase. The `HavenPieces` comment "Each sign stands north of its path, beside it" is false for fixes 4, 5 and 6, and only the mine sign is flagged to Chase.
7. **Proof left for review is short (section 8, checklist item 8).**
   - No picture shows a placed piece from above: every render is a before picture with markers. Add an after render of the bench, the four signs and the stage.
   - The bucket 0x0FFA at 3535,2575,7 appears in no shot: thatch and the lesson gump cover the stall in all of them. The ID and tile are right. Take a shot from inside with the gump closed.
   - No shot reads a sign's name. Single-click each of the four.
   - The notes cite `shots-isle\walk.log` and `shots-main\walk.log`, and neither is on the branch: `.gitignore` drops `*.log`. Save them as `.txt`.

## Passed

| Check | Result |
|---|---|
| League ankh, release | AnkhWest at 3464,2600-2601,27 sits exactly over the map's statics 0x0003 and 0x0002 (read from `statics1.mul`). Same art and facing. Resurrection shown in `1-ankh-*`. |
| League ankh, main | AnkhWest at 3676,2562-2563,0, on grass by the hall's south-east corner. Resurrection shown. |
| Seeding | `SeedLeagueAnkh` runs after the load through `Timer.DelayCall`, and only where no working ankh stands (section 7). |
| Bucket | 0x0FFA is "bucket of water" in tiledata, and 3535,2575 holds no other low static. |
| Signpost 3474,2601 (housing stop 2) | Meets the rule: road directly south at 3474,2602, none north within 3. Road also starts one tile east, the only blemish. |
| Sign art | All four are 0xA854 signposts, no rune markers. |
| Walls, corners, doors, stairs, roofs, shores, foliage, bridges, docks | P799 placed none: all are the stock town. The shots show nothing stray and nothing new on a roof. |
| Old pieces | The code clears P276's farm (`ClearHaven`) and moved signs (`StrayPieces`). The old trades-yard vein was a lesson prop. Not seen in a shot. |
| Better piece | Nothing in What to use where beats a signpost, bench or bucket here. |
| Lesson text | No "0 more"; each step in the mine and stables shots says the next one. |

## How this was checked

- Read the guide in full, `placed.md`, P799's notes, `stock-sites.md`, the diff against `origin/main`, and the release diff `p799-release-isle-20261028.diff`. Local `main` here is stale: `main...` gave 2851 files and `origin/main...` gave 8 in the shard repo.
- Looked at all 38 images: 12 renders, 18 isle shots, 8 main shots.
- Facing and land were checked on the stock 7.0.117 files with `scripts/mapbuild` (`cc-P805-evidence\sign_and_bench_check.py`). The art sheet is `cc-P805-evidence\art-sheet-benches-signs-bucket.jpg`.

**Not verified.**

- This PC has no game client, so nothing here was seen in TazUO. Fix 3 rests on P799's shot plus my render and the statics, not on a live view.
- The sign and echo spots suggested in fixes 3, 4 and 5 passed a land and impassable-static check only, not a walker.
- "Road" in that check means land named dirt or cobblestones plus unnamed edge tiles, so a natural dirt patch can count as road.
- Main's bench was read from code, as no main shot shows it.

P805 DONE
