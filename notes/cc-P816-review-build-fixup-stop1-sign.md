# cc-P816: build review of P814 (fix-up for P806: the housing stop 1 sign)

## In plain words

- **P814 passes.** The New Haven signpost for the first housing stop no longer stands through a park bench. It now stands clear between the two benches by the statue, and the stop moved with it.
- **The stables sign on main moved one tile east,** out from under the barn's eave. It still reads from the door path.
- **One small leftover:** an older code comment on main still names the stables sign's old tile. It is not a fault in the game, and the line itself carries the right note.
- **Nothing for you to do.** Your open questions from P799 and P806 (the stables sign and the mine sign) still stand; this review adds none.

## Verdict

BUILD REVIEW P814: PASS

## What was checked

P814 placed two things, both 0xA854 signposts, and moved one lesson stop. It placed no walls, doors, stairs, roofs, shores, docks, bridges or foliage, so those checks have nothing to look at.

| Check | Result |
|---|---|
| P807 fix 1, stop 1 sign | Now at **3471,2588,10** in the release code (`p814-release-isle-20261028.diff`, `HavenPieces`), as P807 asked. I read the stock 7.0.117 map: forest floor at Z 10, **no statics** on the tile; dirt 1 and 2 south and cobblestones 3 south; forest 1-3 north (Z 25 at 3 north is the bank's grass, not road); forest on both sides. It meets section 6 (north of the path, road south, none north or beside). The old tile 3469,2589 does hold the stock bench 0x0B2C, so the move was needed. |
| Stop 1 | `HousingStop(0)` is **3470,2590**: dirt, Z 10, no statics, 2 tiles from the sign (within 2, not on it). The walk log shows "stop 1 fired on arrival" and "walked stop 1 both ways". |
| Default camera | `stop1-sign-clear-of-both-benches.jpg`, shots 2, 3 and 4 and `render-stop1-sign.jpg`: the post stands on its own between the two benches, clear of both, the statue's plinth and the lamp posts. The figure beside it is a spawned NPC, as Iron says. |
| The north bench | The second stock bench 0x0B2D is at 3471,2587, right north of the sign. It is still reachable from 3470,2588 and 3472,2588 (no statics), so the post does not take it out of use. The shots show it whole. |
| Sign read | `sign-read-3471-2588.jpg`: "Housing lesson, stop 1: a small house". Sign, not a rune marker. |
| P807 fix 2, the record | The `HavenPieces` comment names the old tile, the bench and the bank dirt at 3469,2586; `placed.md` replaces P806's line and records the new tile's nearest bank dirt (3470,2585, outside the sign's column). `RookFacing`'s doubled word is gone. |
| Main stables sign | Moved 3608,2614 to **3609,2614** (`NewHavenLessons.cs:355`), off the barn's eave (hay roof 0x26EC). `render-main-stables-sign.jpg` and both main shots show it standing in the open, north of the door path, not under the roof and not in the door's line. Sign read: "The stables: the sick-bay stall is inside, on the left". |
| Upgrade in place | `SeedHaven`'s stray rule takes the old sign away; fact `AStop1SignLeftAtItsOldSpotIsTakenAwayOnASeededWorld`. Code read, not seen in a client (Iron says the same). |
| Better piece | Nothing in What to use where beats a standing signpost for a lesson stop. |
| `placed.md` against the code | Both signs and the stop match the release diff and the main code. |

## Small note, not a fix

`NewHavenLessons.cs:347-349` on main keeps cc-P755's remark "just north of the door path (3608,2614)". It is history of P755's move, and the entry on line 355 says why it is now 3609,2614. Worth one word in the next prompt that touches that file.

## Not verified

- This PC has no game client; the shots are Iron's.
- I read the stock (release) map for stop 1. I did not read main's SoS map for 3609,2614; the render, the two shots and Iron's new statics fact are the evidence there.
- Main's walk log is one leg to the sign and away, not a both-ways walk; a signpost beside a path is not a walkable join, so section 4 does not ask for more.

## How this was checked

Read the guide in full, P807's review, P814's notes and `placed.md`, the walk logs, the main code and the release diff. Looked at every image: 2 renders, the zoom, 7 isle images and 3 main images (both `frame-001.jpg` are the session's start on the Wakening Isle beach, not part of this build, and the isle `frame-002.jpg` repeats shot 2). Land and statics read with `scripts/mapbuild` (scratch script, not kept).

P816 DONE
