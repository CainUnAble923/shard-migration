# cc-P807: build review of P806 (fix-up for P799, League ankh and New Haven lessons)

## In plain words

- **P806 does not pass yet, but it is close.** Everything from the last review is fixed: Rook's bench is one bench, Rook faces the yard, both blue figures show on the stage, and the music lesson was played through in the real game.
- **One thing a tester would see:** the housing stop 1 signpost in New Haven stands straight through a park bench by the statue. It goes back to the Iron Golem to move it a couple of tiles.
- **One small correction:** that same sign also has a strip of dirt on the bank behind it, the same blemish as the stables sign, and the notes say it has none.
- **Nothing for you to do for this review.** Iron's two questions to you (the stables sign and the mine sign) still stand. I checked both claims against the map, and they hold.

## Verdict

BUILD REVIEW P806: FAIL

## Fixes

Coordinates are stock New Haven, Trammel (the release branch).

1. **Signpost 0xA854, 3469,2589,10 (housing stop 1): stands on a stock bench.** The map has a bench 0x0B2C at 3469,2589,10 (read from `statics1.mul`), and the post goes straight through it from the default camera: `6-stop1-from-the-street.jpg`, enlarged in `cc-P807-evidence\stop1-sign-through-bench-client-shot.jpg`. A signpost is impassable, so it also takes the bench out of use. The guide wants a clean spot beside the stop: section 3 "check every piece from the default camera", 2.6 "nothing stray", and 6. `placed.md` says only "in the bed by the statue". The tile that meets the rule is **3471,2588,10**: forest floor, no statics, road directly south, no road within 3 north, none beside. It renders clear of both benches (`cc-P807-evidence\stop1-sign-as-built-left-suggested-right.jpg`, right). That tile is 3 from the stop at 3468,2591, so move **stop 1 to 3470,2590** (dirt, Z 10, no statics, 2 from the sign) in `HousingStop(0)`. "Across the street, south-west of here" still holds. Other tiles near it fail: 3470,2588 has the bank's dirt 3 tiles north at 3470,2585, and 3469,2590 and 3468,2589 are planted and too close to the lamp post at 3468,2590. Take a new client shot and a new sign read, walk to the stop, and add a fact that no fixed sign shares a tile with a stock static.
2. **The record of that sign is wrong, and goes wrong again if it stays.** The notes say 3469,2589 meets the rule with "none north or beside", and the `HavenPieces` comment says the stables sign has "one blemish". The land has dirt at 3469,2586, Z 27, three tiles north on the bank: the same blemish as the stables sign, not disclosed. Fix 1 removes it. If stop 1's sign stays on any tile with bank dirt within 3 north, put it in `placed.md` and the comment. Also, while in `HavenSpots.cs` on main: the `RookFacing` summary has a doubled word, "the the moongate exit".

## Passed

| Check | Result |
|---|---|
| P805 fix 1, bench | 0x0B2D on both branches. One joined bench in `after-rook-bench.jpg`, `after-main-rook-bench.jpg` and both client shots. No 0x0B2C left on main (`shots-main\walk.txt`). The swap on a seeded world shows in the log P806 quotes, 6 taken away; I read the code, not that log. |
| P805 fix 2, Rook | South on the release: he sits with his legs toward the yard (`1-rook-bench.jpg`). North on main: the moongate exit is north of him, as `1-main-rook-from-the-moongate-exit.jpg` shows. Sound reasoning, and it matches the code. |
| P805 fix 3, echoes | 3412,2604,60 and 3413,2603,60 stand on planks 0x04D4 (map). Both are in view with the gump closed (`3-theater-both-echoes-gump-closed.jpg`), clear of the canopy, the Actor and the stairs. Their spacing in the shot matches those tiles. Brawl shots 1-6 show them fighting and stopping. |
| P805 fix 4, stables sign | 3520,2568: grass, no statics, road directly south, none beside. **The deviation is real.** Dirt at 3520,2566 is Z 20 against 8 at 3520,2567, a cliff. My scan of every terrain within 12 tiles found only the bank top and the stable's own planks. Flagged to Chase. |
| P805 fix 5, mine sign | 3469,2624: grass, no statics, dirt road 3 south, none north or beside. It is on its land, and not visible from the gate (`5-mine-sign-from-the-gate.jpg`), as Iron says and has flagged to Chase. It is the nearest tile that meets the rule. |
| Housing stop 2 | Unchanged, passed by P805, read in `6-stop2-sign-read.jpg`. |
| P805 fix 7, proof | After renders, all four signs read, walk logs saved as `.txt`. |
| Bucket | 0x0FFA at 3534,2574,8 on hay 0x0F34, inside the stall (walls 0x00B8 west, 0x00BC north). Seen beside the character in `7-bucket-from-the-stall.jpg` and in `after-stall-bucket-no-roof.jpg`. Iron moved it against the P805 review with good reason: it hid behind the east wall before. |
| False FAIL in `walk.txt` | "FAIL Peacemaking on an echo" is what the notes say: the same log has "Finished: Peacemaking ... (1 of 3)". The lesson ends "done=True". |
| `placed.md` against the code | Every sign, bench, bucket, stop and echo matches `p806-release-isle-20261028.diff` and P806's commit on main. |
| Sign art | All 0xA854, no rune markers. |
| Walls, corners, doors, stairs, roofs, shores, bridges, docks, foliage | P806 placed none: all stock town. No new walkable join, and nothing new on a roof. |
| Better piece | Nothing in What to use where beats a signpost, bench or bucket here. |

## How this was checked

- Read the guide in full, `placed.md`, the README, P806's notes, both walk logs, P805's review, P806's commit in the code repo and the release diff. `main...` in the code repo is stale here (2862 files), so I read commit 69045de directly.
- Looked at all 27 images: 7 renders, 18 isle shots, 2 main shots. Enlarged the stop 1, bucket and Rook shots.
- Land and statics were read from the stock 7.0.117 files with `scripts/mapbuild`; the stop 1 scan is `cc-P807-evidence\stop1_land_check.py`.

**Not verified.**

- This PC has no game client, so nothing here was seen in TazUO by me. The shots are Iron's.
- The suggested tiles in fix 1 passed a land and statics check and one render, not a walker or a client.
- "Road" in my scan means land named dirt or cobblestones plus unnamed edge tiles, as P805's did, so a natural dirt patch counts.
- Rook's facing on the release is read from the seated pose in one small shot, plus the code.
- Iron's open item stands: main's `[global get Direction` read `North (2)`, so that world may hold a second Rook. Not traced, and not a placement matter. Only one Rook shows in the main shots.

P807 DONE
