# cc-P844: fix-up of P721 (the bandage wait on the isle) after P834's build review

## In plain words

- **Pip, the hurt farm boy on Tutorial Island, now sits on one whole bench.** Before, his bench was made of the wrong
  piece, so it showed as two short crosswise bench ends inside the farmhouse. It is one bench along the east wall now.
  An existing world gets the new bench by itself on the next server start.
- **The pictures the build review asked for are now in `notes\cc-P844-review\`.** They are drawings of the farm gate,
  the clothes stop and the chat stop, game shots of every sign with its words showing, and Pip on his bench. A list of
  every piece is in `placed.md`. They show the pieces as the game has them now.
- **One thing found and left for you:** at the chat stop and at the farm gate, two signposts stand on diagonal tiles.
  On screen each pair looks like one tall post with two boards, and a click reads only one of them. I did not move
  them, because that changes P741's sign spots.
- **For you:** nothing to try or deploy. If you want those two sign pairs split, say so and it can be a small job.

Iron Golem, 2026-11-08. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P844`. Nothing committed. The shared Test Shard and Haven were not touched, and nothing was
published.

## Step 1: bringing P721 in

This step was not done as written, on purpose:

- The prompt says to check out `golem/Iron/P721` and merge `main` into it.
- The hand-off says to stay on `golem/Iron/P844` and not merge or switch branches.
- P834's item 2 says not to merge the old branch's spots back over main's.

P721's code already reached main through P727 ("land P721 via its fix-up P723"). Main has since moved its pieces (P741,
P748, P751). `golem/Iron/P844` is at main (`4ec6962` code, `c452a5b` docs). So "P721 plus main, main's side kept"
is main itself. I took nothing from the old branch. `git cherry` lists P721's commit as not on main only because it
landed as a different commit (P727). Its files (`TutorialWake.cs`, `Bandage-tutorial-wait-lines.patch`, the healing
lesson) are on main.

## The reviewer's items

**1. No renders or placed list: done.** `notes\cc-P844-review\` now holds the pieces as main has them. Its
`README.md` is the index:

- **`placed.md`:** one line per piece, grouped by stop:
  - the clothes table 0x0B8F (6664,3990);
  - the chat signpost 0xA854 at Signpost -2,-4 (6690,3986);
  - the farm gate signpost 0xA854 (6697,3977, in the farm addon);
  - the field gate (0x0843, LightWoodGate NorthCCW, read live) at 6695,3979, and the fence 0x0837 at 6695,3978;
  - Pip's bench and the three blood decals at 6703-6704,3974-3976,7;
  - the vision braziers 0x0E31, which have been in P742's chamber since P742 (its folder has their render and shots).
- **Isorenders**, with the server's pieces drawn in by `notes\cc-P844-tools\render844.py` (P741's `render741.py` plus
  the pieces `build_isle.server_items()` does not read):
  - the farm gate and stop area;
  - the farmhouse with the roof off;
  - the clothes and chat stops together and one by one.
- **TazUO shots from the default camera** on a private shard (127.0.0.1:2596, `test-shard` lock):
  - each signpost and the clothes table, clicked so its name shows over it;
  - the field gate and fence;
  - Pip on the bench, before and after the fix below.
- **Walk:** `tour-walk.log` (see Walk below).

While checking the bench, as the reviewer asked, I found it was the wrong piece:

- **Pip's bench was 0x0B2D, which runs east-west.** Its two tiles stand in a north-south line, so it drew as two
  crosswise stubs (`bench-0B2D-left-0B2C-right.png`, `before-tazuo-pip-on-bench.jpg`). This is the same mistake P805
  found on Rook's bench, the other way round.
- **The fix, in `TutorialFarm.cs`:**
  - `BenchId` is now 0x0B2C, the north-south piece.
  - `TakeAwayOldPipBench` removes 0x0B2D pieces from Pip's two tiles before the seed lays the bench, so an existing
    world swaps them in place instead of keeping both (guide section 7).
  - `OldPipProps`, the pre-P741 spots the seed clears, still names 0x0B2D, because that is what was laid there.
- **Fact 6** in `TutorialIsleCoastVerification`: `PipsBenchIsTheNorthSouthPieceAndTheCrosswiseOneIsSwapped`.
- **Proven live as an upgrade.** I saved the proof world with the old bench, stopped it, and restarted it on the fixed
  image. The tour then found exactly one 0x0B2C piece on each tile. The after shots show Pip seated on one bench.

**2. Do not merge the old branch's spots back over main's: done.** Nothing of `golem/Iron/P721` was merged or taken
(step 1). Every piece in `placed.md` and every picture is main's current spot:

- Pip on the bench at 6704,3975, not standing at 6715,3981;
- the chat signpost at Signpost -2,-4, not +0,-2;
- the field gate at 6695,3979, not 6713,3979.

The seed still clears P721's old spots (`MoveFromOldLayout`, `MoveChatSignpost`). The coast facts 3 and 4 cover that.

## Found, not fixed: signposts on diagonal tiles

Two standing signposts on tiles (x, y) and (x+1, y+1) draw one right under the other, as one tall pole with two
boards (`signpost-one-left-two-diagonal-right.png`). A player sees one post and clicks one name. Two isle stops have
such a pair:

- **The chat stop:** the farm signpost 6690,3986 and the core.chat lesson sign 6691,3987
  (`after-tazuo-chat-signpost-read.jpg` shows one post).
- **The farm gate:** the gate signpost 6697,3977 and the core.farm lesson sign 6698,3978.

I did not move them:

- They are not on P834's list.
- Their spots come from P741's sign chooser under the north-of-path rule.
- Moving them means re-checking both stops against the road and Wren's spot.

I added the rule to guide section 6 with this open finding, so the next isle sign job can split them.

## Walk

`notes\cc-P844-review\tour-walk.log` comes from Iron the Tester, a Player account, in TazUO. The walk used Pathfind,
which makes the client's own steps (no teleport), driven by `notes\cc-P844-tools\Tour844.py`:

- **The route:** the clothes stop, the road east to the chat stop, the farm gate, up the farmhouse steps (Z 0, 4, 7)
  and through the door to Pip, then back out to the road.
- **The result:** 13 PASS and no FAIL. Every piece is at its spot, every sign reads its name, and each bench tile
  holds one 0x0B2C piece.
- **One leg:** the walk toward 6694,3982 ended at 6696,3979, by Wren and inside reading range of the gate. The next
  leg went on from there normally. Nothing blocked a step.

P834 listed no stairs, doors, bridges or docks as changed, and the bench fix changes nothing walkable.

## Tests and build

- **Gated build** `docker/uo/build.sh -t sl-modernuo:cc-P844`, with the fix: **green**, 3,309 shard tests, EXIT=0
  (`notes\cc-P844-tools\green-gated-build.txt`). The first build, of main before the fix, was also green, with 3,308.
  That is the suite P721 ran, and it includes P721's facts.
- **Red first:** `notes\cc-P844-tools\mutate844.sh` ran the coast facts on the builder image:
  - mutant 1, `BenchId` back to 0x0B2D: fact 6 fails (`red-m1.txt`);
  - mutant 2, the seed skips `TakeAwayOldPipBench`: fact 6 fails, two pieces on a tile (`red-m2.txt`);
  - the fix: 6 of 6 pass (`green-probe.txt`).
- **CHANGELOG:** a new section 2026.11.08.2 with one Fixed line. `VERSION` is 2026.11.08.2.
- **Locks:** `docker-build` was taken and released twice. `test-shard` was taken and released, and the proof shard is
  down. Free memory was 10.3 GB and 9.9 GB before the builds.

## Deviations and decisions for Chase

- **Step 1** was not done as written (see above): nothing was merged, by the hand-off's and the reviewer's rules.
- **The bench fix** is a server change that P834 did not list. The reviewer asked for the bench to be checked in a
  shot, and the shot showed it was wrong.
- **The diagonal signpost pairs** are left as an open finding (see above).
- **The shot client** is P823's built player package (`D:\UO\golems\Iron\p823-pkg`). Its `trammel.mapops` is
  byte-equal to main's. No package was built.
- **One cleanup command was refused:** `docker rm -f` on a leftover probe container, after I stopped a probe run that
  had started on a test file that did not compile. The container ran with `--rm` and exited by itself. No containers
  of mine are left running.
- **Guide:** section 6 now gives the bench's two runs (0x0B2C north-south, 0x0B2D east-west) and the diagonal-signpost
  rule. The piece tables note the bench's run.

P844 DONE
