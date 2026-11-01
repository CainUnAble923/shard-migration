# cc-P754: build review of P743 (New Haven tutorial fixes)

## In plain words

- I checked the New Haven pieces P743 placed against the building guide. I used its pictures, its list of placed pieces
  and its code. These pieces are Rook's bench, the stable stall's bucket and straw, and three signposts.
- Rook's bench, the stall and both housing signposts are fine. The old farm west of town is gone and nothing of it is
  left.
- One thing is wrong: the signpost for the mountain path to the mining cave stands in the middle of the dirt road.
  Players have to walk round it. The guide says it belongs on the grass on the north side of the road.
- Nothing for you to do. The Iron Golem gets a one-item fix-up list. After that P743 merges.

## What was reviewed

- The guide: `notes/guides/building-and-decorating.md`, read in full.
- P743's own files, from `origin/golem/Iron/P743`, not edited:
  - `notes/cc-P743-review/`: `placed.md`, `proof-log.txt`, 5 renders and 9 TazUO shots;
  - `notes/cc-P743-new-haven-tutorial-fixes.md`;
  - the code diff (`git diff main...origin/golem/Iron/P743`): `NewHavenLessons.cs` `HavenPieces` and `SeedHaven`,
    `HavenSpots.cs`, `TutorialCorePlacement.cs`.
- No walls, doors, stairs, roofs, shores, bridges, docks, foliage or wall-mounted items were placed, so those checks do
  not apply. These are the 9 pieces placed:

| Piece | Place | Check |
|---|---|---|
| 0x0B2C bench x2 | 3669-3670,2636,0 | Pass. It runs east-west, as two pieces in one line (render and shot). It is on grass, 2 tiles south of the gate exit and clear of the Albatross's door (3666,2639). Rook stands on it facing north. P743 already flags that he is not drawn seated; that is a choice for Chase, not a guide rule. |
| 0xA854 signpost, mining | 3702,2745 | **Fail**, item 1 below. |
| 0xA854 signpost, stables | 3610,2613 | Pass. It is on the ground north of the walk to the east barn door (3607,2615-2616) and off the door's 2-tile approach. It reads from the south. |
| 0x0FFA bucket, 0x1036 / 0x0F34 straw | 3605-3606,2619-2620,0 | Pass. They sit inside the south-east stall beside the map's own trough and hay. The straw shows in the render and the shot. The bucket is hidden behind the south wall from the default camera; that is acceptable for a floor prop in a stall. |
| 0xA854 signpost, housing stop 1 | 3713,2591 | Pass. It is on the grass east of the cottage with the dirt path south of it, beside the stop (3709,2594) and not on it, away from the cottage's south door. |
| 0xA854 signpost, housing stop 2 | 3704,2604 | Pass. It is on open grass one tile north of its stop (3704,2605), clear of the trees. |
| Old farm removal | 3372-3401 x 2603-2619 | Pass. The shot shows plain grass and trees with nothing left. The dry run finds 0 left. |

The pieces are signs, not rune markers. Every piece is stock art, and nothing from What to use where fits better.
Seeding is idempotent at world load and upgrades in place, which the guide's section 7 asks for.

Caveat: I could not cross-check 3702,2745 on the map data. vseUOAware's saved folder holds the stock Trammel map, not
the shard's Siege of Sosaria land (it reads Z -5 there, while the Tester stood at Z 30). The finding below rests on
P743's own render and live shot, which agree.

BUILD REVIEW P743: FAIL

1. 0xA854 signpost "The mountain path: the mining lesson's cave is west, round the hill", 3702,2745 (land Z), at the
   mountain path's start south of town:
   - **What is wrong:** in both `render-mountain-sign.jpg` and `mountain-path-sign-player.jpg` the post's foot is in the
     middle of the dirt road. The road is several tiles wide there and runs on both sides of the post, and a signpost
     is impassable.
   - **What the guide wants** (section 6, "Signs, not rune markers" and "Every sign stands north of its path, facing
     it"): the sign stands off the walked route and the road, beside it on its **north** side. The road may be within 3
     tiles south of the sign, with none north of it or beside it.
   - **The fix:** move the post onto the first grass tile north of the dirt band, near where the path leaves the shore
     road (for example about 3703,2742; pick the tile with `notes/cc-P741-tools/sign_spots741.py`). Keep it clear of the
     trees just north of the road. Update `HavenPieces` and `placed.md`, then take a new render and a new shot. The
     seeder's move-in-place step already takes the old post away.

P754 DONE
