# cc-P750: continue P708 (the guild headquarters on the Siege of Sosaria land): the Rangers' post, two signs, the reply wording

Iron Golem, 2026-10-31. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P750` (main with P708 merged). Not committed by me; nothing deployed; the shared Test Shard and Haven
not touched. **Paused at Chase's request** at a clean point: the code builds green and every fact is green. The live
shots are left (Continuation, and `cc-P753-cont-guild-hqs-live-shots.md`).

## In plain words

- **The Rangers' guildmaster at Fort Viridian moves to where you can see him.** In P708's spot, the fort's south court,
  the tall rampart in front of it hid both him and any player from the game's camera. He now stands in the fort's open
  inner court (1002,985), with nothing in front of him. The road stop and the sign stay where they were.
- **Two guild signs hang where they show:** the League's at Valunstead keep moves from beside the gate steps (the steps
  hid it) to the grass in front of the east gate tower. The Tinkers' at Hammerhill moves one tile along the workshop's
  east wall, clear of the house beside it.
- **The staff command's reply is clearer:** `[ClusterFGuildHalls place` lists what it took away from a hall's old site
  on its own line ("rangers (Fort Viridian): took away from its old site the old OutridersGuildmaster at ...").
- **For you:** nothing to decide. The in-game pictures are not taken yet. The PC had 4.7 GB free and the run stopped
  itself before starting. P753 takes them when memory allows.

## What changed

### 1. Fort Viridian: why nothing showed, and the move

- **Why:** the map was right; 1003,1004 is open sky at Z 0. The camera was the problem. That court is a slot about 6
  tiles deep (x 991-1009, y 1001-1006) between rampart blocks whose walkways stand at Z 45. In the client's view, the
  south block draws over every tile behind it. That is the "green walls and yellow walkways" in P708's shot.
- **The measure:** a cover model on the SoS land P708's checks read. It takes the share of a standing figure's 20 by
  60 pixel screen box covered by art drawn after his tile (larger x + y), from the art's own pixels. As the client
  does, it leaves out a static at or above the first one over his head.
  - It reads P708's post 100% covered. The six moved guildmasters read 0% once moved, the indoor ones under their
    roofs.
  - It agrees with P708's shots on the signs too: the four signs P708 saw read 0-4%, the two it could not see 100%
    and 48%.
- **The move** (`design/guild-halls/halls.json`, `check.py` and `gen.py` from P708's `p281sos` copy): the guildmaster
  goes to **1002,985,0**, in the open inner court. Four candidates in that court passed every hall check; 1002,985 stands
  mid-court in a render (`notes\cc-P750-tools\renders\vir-court.png`). The travel stop (1015,1003, the author's go
  point) and the sign (1014,1008) are unchanged. The walk from the stop reaches him.
- **An old post on a placed world:** a world placed with P708's table has the Rangers' guildmaster at 1003,1004. A new
  `ClusterFGuildHallMoves.Shifted` list (posts moved within their new place, apart from the six town moves in `All`)
  names it, and `place` and `clear` take him away there as at a town move's old post.

### 2. The two signs (`halls.json`; the building guide's 2.5 and its wall-mounted rule)

| Sign | P708 | Now | Cover then / now |
|---|---|---|---|
| League, Valunstead keep | 566,321,18, brass, West | **567,321,18**, brass, North (0x0BD1): the grass just outside the east gate tower's south wall (base Z 20), beside the steps | 100% (the steps' side block) / 0% |
| Tinkers, Hammerhill | 1494,1026,8, North | **1494,1025,8**, West (0x0C02): outside the workshop's east wall (base Z 10), the tile south of the double door | 48% (the house south-east) / 0% |

- The keep's gate faces south (door 564,320, steps x 563-565), so its sign hangs on a south face, the even art.
- The workshop's double door is in its east wall, so its sign hangs on the east face, the odd art.
- The guide's two tiles from the door (1021 or 1026) are both about half covered by the neighbouring house. At 1025 the
  sign draws after both door tiles, so a door leaf cannot hide it.
- `place` rehangs both on a world that has P708's signs: a hall's sign anywhere but its design spot is an old-site
  piece.

### 3. `place`'s reply (`ClusterFGuildHallPlacement.Place`)

- A moved hall's removals now have their own line, before the placed line:
  `"<hall> (<town>): took away from its old site the old ... at ...; ..."`. A dry run says "would take away from its
  old site".
- The placed line lists only what was placed. The summary adds "; took away N from old sites" when there were any.
- Fact 3's dry-run check for "would take away" is kept.
- I also run `TakeAway` once, into a list, since it deletes as it is read.

## Tests

| Fact | Red | Green |
|---|---|---|
| docs `tools/tests/test_guild_hqs_sos.py` **fact 4 (new)**: each moved hall's guildmaster at most 25% covered in the camera | P708's design file: fails with exactly "rangers ... (1003, 1004, 0) is 100% covered" (`red\red-test-guild-hqs-sos-p708-design.txt`) | 5 of 5 (`green\test-guild-hqs-sos.txt`) |
| docs fact 5 (new): each moved hall's sign (the server's own art, 0x0B95 + 2 x type + facing) at most 25% covered | the same run: exactly "league ... (566, 321, 18) is 100%" and "tinkers ... (1494, 1026, 8) is 48%" | same |
| docs `test_s8_spots.py` (P281's hall checks on SoS, every hall) | | 4 of 4 (`green\test-s8-spots.txt`; `SL_SOS_MAP` = P708's SoS client folder) |
| code `GuildHallSosMovesVerification` fact 3 (extended): the real place has a "tinkers (" line "took away from its old site ... GuildHallSign", no line runs "placed ... took away" together, the summary "took away 2 from old sites" | mutant A, P708's placement code: facts 3 and 5 fail (`red\red-a-p708-placement.txt`) | 20 of 20 guild hall facts on `sl-uo-builder:cc-P708` with this branch's files (`green\probe-guildhall.txt`) |
| code fact 5 (new): a P708-post Outrider at 1003,1004 is named in the dry run ("would take away from its old site"), taken away by place, the guildmaster stands at 1002,985, a second place adds nothing | mutant B, OldSite without `Shifted`: fact 5 fails only (`red\red-b-no-shifted.txt`) | same |

- `make_sosclient.py` and `make_p281sos.py` were run first, as the prompt says. `gen.py --verify` matches.
- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P750` via `gated-build.ps1`, the `docker-build` lock taken and
  released each time):
  - first build: EXIT=0;
  - the second, with the signs, hit the known apply-patches flake: "PublicMoongate-sos-gates.patch never applied"
    though its "Applied:" line is in the log (`gated-build-2-flake.log`);
  - the rerun: **EXIT=0, 2,836 tests: 2,830 passed, 6 skipped, 0 failed** (`green\gated-build-2-summary.txt`).
- `check.py` rewrites `notes\cc-P677-tools\p281sos\check.out.txt` and P708's copy on each run (P708's mistake too).
  I restored both from git after each run.
- CHANGELOG: a new `2026.10.31.3`, Staff (P751's branch already uses 2026.10.31.2). VERSION 2026.10.31.3.

## Live: not done (paused)

`run-shots750.ps1` (overlay, private shard 2596, `shots750.json` with P708's runner off-screen, shard down, lock
released) checked memory first: 4.7 GB free, under its 6 GB floor. It stopped before taking the lock or starting
anything. No container is left. Then Chase asked for the pause.

## Mistakes, and what to trust

- **One read of the main desk.** My first scratch cover scripts imported `scripts/mapbuild/isorender` alone. Its `Art()`
  then read tiledata from its default client folder, `D:\ShatteredLegacy\client-data`. That is read-only, nothing was
  written, and the numbers are the same from this task's folder. Every later run, and the facts, point at
  `D:\UO\golems\Iron\p708-work\sosclient`.
- **The cover model is a model.** It matches all six of P708's sign shots, and the hidden Rangers post. It reads two
  travel stops covered: the Custodians' (1560,974) 100%, in a narrow lane south of the hall's door, and the Tinkers'
  (1495,1023) 42%. No fact holds the stops to it; P753's shots check them in game.

## Deviations and decisions for Chase

- **The Rangers' post moved** (the prompt allowed it if the court reads poorly). It is still Fort Viridian, still the
  inner court, now the open one.
- **The Tinkers' sign is one tile from the door, not two.** Both two-tile spots are half hidden by the house beside it.
- Unchanged from P708 and still yours: Valunstead's access, the Smiths' Stormhammer option, the Smiths' forge decor
  refusal at Serpent's Hold.

## Continuation

Done:
- part 1: the cause found, the post moved, the old post cleared on placed worlds;
- part 2: both signs measured and rehung by the guide;
- part 3: the reply wording;
- part 4: the facts (seen failing, green), make_sosclient/make_p281sos, check/gen, two green gated builds (one flake
  rerun), CHANGELOG/VERSION.

Left, in `D:\UO\cc-prompts\queue\cc-P753-cont-guild-hqs-live-shots.md`:
- the live shots (`run-shots750.ps1` when 6 GB are free) and a look at them: the Rangers' guildmaster, both signs, the
  two stops the model flags, and `place`'s reply in the log;
- the review folder.

Nothing is mid-flight: no lock held, no container running.

## Files

- **Code copy:**
  - `design/guild-halls/halls.json`; `server/customizations/ClusterFGuildHallPlacementData.cs` and
    `server/tests/Misc/GuildHallPlacementDesignCopy.cs` (generated by `gen.py`);
  - `server/customizations/ClusterFGuildHallMoves.cs` (`Shifted`), `ClusterFGuildHallPlacement.cs` (OldSite, Place's
    reply);
  - `server/tests/Misc/GuildHallSosMovesVerification.cs` (fact 3 extended, fact 5 new);
  - CHANGELOG.md, VERSION.
- **Docs copy:**
  - `tools/tests/test_guild_hqs_sos.py` (facts 4 and 5);
  - `notes/cc-P750-tools/`: `probe-guild.sh`, `gated-build.ps1` (logs git-ignored), `overlay.ps1`, `proof-shard.ps1`,
    `shots750.ps1`, `make_shots750.py`, `shots750.json`, `run-shots750.ps1`, `renders/`, `red/`, `green/`;
  - this file.
- **Outside the repos:** `D:\UO\golems\Iron\p750-mutants\` (the two mutant copies and P708's design file), deletable.

P750 PAUSED
