# cc-P862: Battle Chess in the Haven inn

## In plain words

- **New Haven has a living chess board.** It stands in the inn's front yard, just south of the inn's front doors (the
  inn's casino is inside, behind them). The board is a raised marble dais with steps all round. Two players move
  living pieces (soldiers, knights, monsters or animals) that walk to their square and fight when one takes another.
- **To play,** double-click the board, choose a set of pieces (Classic, Fantasy, Giants, Animals or Undead), then
  invite a player standing nearby. It plays real chess: castling, en passant, promotion, check, checkmate and draws.
  It is free: nothing is staked, and the only thing you win is your record of wins, losses and draws.
- **It placed itself** when the test world loaded, and it will do the same on the live world. In the test client
  a player played a whole game against the staff bot, won by checkmate, and then resigned a second game (shots in
  `notes\cc-P862-shots\`).
- **For you to decide:** the board couldn't go inside the inn. The inn's rooms are 5 by 3 tiles, and the board needs
  10 by 10, so it stands just outside the front door (render `00-render-board-in-the-inn-yard.jpg`, shot 03). If you
  want it somewhere else, the spot is three numbers in `Configuration/battle-chess.json`.

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P862`. Nothing committed. Main only, not the isle branch. The source is
`D:\UO\third-party\code\battle-chess` (and the identical `battle-chess-125`, which adds a changelog). I used it as
reference only: nothing was built, run or copied from it.

## What was built

All of it is in `server/customizations/BattleChess/` (code copy), with its facts in
`server/tests/Misc/BattleChessVerification.cs`. There is no engine change and no `.patch` file.

| File | What it is |
|---|---|
| `ChessRules.cs` | The rules of chess, written fresh as a plain position value with no world, mobiles or timers. It handles legal moves, check, checkmate, stalemate, castling, en passant, promotion, the fifty-move rule and bare kings. A refused move says why ("A knight moves in an L...", "That move would leave your king in check."). |
| `BattleChessBoard.cs` | The board, a 10 x 10 addon (saved). The 64 marble squares sit on a dais 5 high, ringed by sandstone stairs that climb toward the board on every side, with rounded corners. Double-click any part of it. White sits on the south side, the camera's side. |
| `BattleChessPiece.cs` | A living piece (saved; it deletes itself at the next start). It is a plain blessed mobile with no AI, skills or loot. It walks square by square (a knight along its L) and fights the piece it takes: the attack, a stagger, then a lightning bolt. The file also holds the five sets' bodies and sounds. |
| `BattleChessGame.cs` | One game: invitation, colours drawn at random, turns, promotion, the end, and the clock (an invitation lapses after 2 minutes, a player who doesn't move in 10 loses on time, and a player logged out for 5 forfeits). Not saved: a restart ends the game. |
| `BattleChessGumps.cs` | The board's window (choose a set, invite, or watch a game in progress), the invitation, each player's game bar (Move, Resign, How to play, and pieces taken), the promotion choice, the resign confirmation and the rules text. |
| `BattleChessRecords.cs` | Each player's wins, losses and draws (GenericPersistence `BattleChess`, versioned; an unknown version fails loudly). |
| `BattleChessSettings.cs` | `Configuration/battle-chess.json`: the spot, the hues, the walking speed and the time limits. It is written with defaults at first start, and a bad file is refused whole. |
| `BattleChessSeeder.cs` | Places the board at every world load when it is missing (idempotent), and the `[BattleChess status|seed|end|reload` command (GameMaster, with `[ShardCommand]`). |

There are three saved types: `BattleChessBoard`, `BattleChessPiece` and `BattleChessRecords`. That matches the
original's three (control stone, piece mobile and winner paper).

**No gold, no rewards.** The original handed the winner a "winner paper". This port gives no item at all, only the
record. Nothing touches gold, skills or stats. The facts check that a player's gold doesn't change over a game.

**Credit:** "After Battle Chess by Arya, kept up by dragon slayer2" is in the CHANGELOG line, the rules window and the
file headers. The poster names no other authors.

### What changed from the original, and why

- **The rules engine is ours.** The original misses chess rules: it castles by sending the king onto the rook (we
  accept that, and also the usual two-square king move), and it offers "do not promote", which chess does not allow.
  It never draws by the fifty-move rule or bare kings, and its pawn move list adds the wrong square for an en passant capture on one side. The
  facts prove the new engine against the published perft counts of four standard positions (below).
- **The board places itself.** It is seeded from settings, where the original needed a GameMaster to target a corner
  at run time.
- **No region.** The original fenced spectators off the board during a game and blocked Invisibility near it. Here
  anyone may watch from the steps. Pieces move by stepping server-side, so a bystander on a square does not block them.
- **Pieces are plain mobiles,** not creatures walking AI waypoints. Each moves one tile per step on a timer, and the
  clients draw that as a walk.
- **The Classic set's clothes are plain worn art.** The original dressed its pieces in real armour and weapons. A
  piece's clothes are deleted with it, so nothing on the board can be looted. The knight is not mounted.

## Where it stands

The prompt asks for "the Haven inn next to the casino". Main's inn on the SoS map is 3663-3679, 2607-2623, and it is
split into bedrooms 5 by 3 tiles. A living 8 x 8 board with its steps is 10 x 10, so it can't go inside. I searched
for spots within 34 tiles of the casino that are flat, clear and not protected (P678's list of doors, spawners and
seeded rows); `notes\cc-P862-tools\` has the probes, and the search is described in this section. The results:

- the cobblestone square west of the inn is the town's main plaza (the town crier, the Fountain of Youth);
- the street north of the inn is only 7 rows deep;
- the yard east of the inn climbs from Z 0 to Z 20 through woods;
- the inn's front yard to the south is flat at Z 0.

So the board stands in the front yard: rim north-west corner **3673, 2628, 0** (Trammel), with the squares from
3674, 2629 to 3681, 2636 at Z 5.

- **The inn's doors (3667-3668, 2623)** are 5 tiles west of the board and 4 rows north, so their approach stays clear.
- **The town's lamp post at 3672, 2633** stands just west of the rim, which keeps its west column at x 3673 to clear
  it (one tile further west put the lamp on the steps).
- **Two cedars (3684, 2634 and 3676, 2640)** stand 2 and 3 tiles off the rim. From the default camera they stand at
  its corners and cover no square (shot 03). They are map statics, so moving them would take a map change.
- **Two flat rune decorations (3676, 2631-2632)** lie under the dais, which covers them.

## Tests: red, then green

`notes\cc-P862-tools\probe.sh` builds the facts in the main builder image (`sl-uo-builder:cc-p861`, this branch's
base) and runs only `BattleChessVerification`. `red-all.sh` ran the red runs, then green; the summary is `red-all.txt`
and each run has its own `probe-*.txt`.

| Run | What it is | Result |
|---|---|---|
| RED 0 | The facts with no Battle Chess code (before the change) | does not compile (CS0234/CS0246) |
| RED m-rules | No en passant, castling through check allowed, "Illegal move." as the refusal, fifty-move rule at 500 | 5 facts fail |
| RED m-seed | The seeder places a board at every load | 1 fails (the board places itself once) |
| RED m-game | The taken piece stays, results aren't booked, the promotion choice is ignored, no range check on invitations, a deleted piece leaves the game running | 6 fail |
| RED m-board | The NW corner swapped, square colours inverted | 1 fails |
| RED m-records | Version unchecked, draws not saved | 1 fails |
| RED m-settings | A 0-minute move limit let through | 1 fails |
| GREEN | The real code | **15 of 15 pass** |

Every fact fails under at least one mutant. The first green run also found a real bug: pinned's `Map.Parse` throws on
an unknown facet name instead of returning null, so the settings check now uses `Map.TryParse`. (P811's
`CasinoSettings` has the same pattern; I did not change it.)

The 15 facts cover:

- **Rules:**
  - perft of the start position (20 / 400 / 8,902), "Kiwipete" (48 / 2,039), position 3 (14 / 191 / 2,812) and
    position 4 (6 / 264);
  - refusals that say why;
  - checkmate, stalemate, the fifty-move rule and bare kings;
  - castling (the king onto its rook or two squares, never through check, lost once the king has moved), en passant,
    and promotion to the player's choice.
- **World:**
  - the board's 100 pieces, its stairs and corners, and the square-to-tile mapping both ways;
  - the board placing itself once, and nothing when off;
  - a game: 32 pieces on their squares facing their way, a move out of turn refused, a busy board refused;
  - Fool's mate ending the game, booking the result, clearing the pieces, freeing the board and leaving gold untouched;
  - a capture removing the taken piece;
  - promotion to a knight;
  - resigning, losing on time and forfeiting after staying away;
  - invitations refused plainly (yourself, a far player), and a lapsed invitation;
  - a piece deleted by staff stopping the game with no result;
  - records and board saving and loading, an unknown version refused;
  - a bad settings file refused.

## Gated builds

`notes\cc-P862-tools\gated-build.ps1` runs the gated build under the docker-build lock, dropping the page cache
first. The image is `sl-modernuo:cc-P862`; `latest` was not moved. There were three builds, each **EXIT=0, 3,388
passed, 0 failed, 6 skipped** (`gated-builds-summary.txt`; the last log is `gated-build.log`):

1. the first full code;
2. the board moved one tile north (to 3673, 2628), clear of the lamp post and both cedars;
3. the board's window widened so the five set names show in full (run 2 showed them cut off).

The proof ran on build 3's image, which is the committed code.

## In game (TazUO, private proof shard 2596)

`notes\cc-P862-tools\run862.ps1` ran under the test-shard lock on a fresh copy of the bot world. The kit is P867's,
repointed (`kit\`).

- **The trainee:** "Iron Chess", on the Golem's Player account (a new character), driven by `kit\Chess862.py`.
- **The opponent:** the Golem's admin character "Iron", logged in through uobot by `kit\chessbot862.py`. It moves the
  trainee to the board, stands beside it, accepts invitations and plays its colour's moves.

The final run is run 4; all 15 checks passed (`cc-P862-shots\walk.txt`, the bot's `chessbot-out.txt`):

- the board placed itself at world load (`[BattleChess status`: "The board stands at (3673, 2628, 0) on Trammel");
- the trainee double-clicked a square, chose Classic, invited the bot, and the bot accepted;
- the colours were drawn: the trainee got White;
- the trainee played e4, Bc4, Qh5 and Qxf7, and the bot played e5, Nc6 and Nf6;
- "Iron Chess wins by checkmate with Qh5xf7.", with "*checkmate*" over the black king;
- the record was told and kept: "1 won, 0 lost, 0 drawn";
- the pieces left the board 20 seconds after the end;
- a second game with the Undead set started (the trainee drew Black) and was resigned;
- the board's window then showed the record "1 won, 1 lost, 0 drawn".

Shots (`notes\cc-P862-shots\`, default camera):

| Shot | What it shows |
|---|---|
| `00-render-board-in-the-inn-yard.jpg` | an isorender of the spot, from the map files |
| 01 | the board in the yard before a game |
| 02 | the invitation going out |
| 03 | the Classic pieces set up |
| 04 | the first move |
| 06, 07 | the queen beside f7, striking |
| 08 | checkmate and the result in the game bar |
| 09 | the board free again |
| 10 | the Undead pieces |
| 11 | resigned |
| 12 | the board's window with the five sets and the record |

The lightning flash of the capture fell between frames 07 and 08. Those two frames show the queen striking and then
standing on f7 with the pawn gone.

Earlier runs, kept in `notes\cc-P862-tools\run1`-`run3`:

- **Run 1:** no game started. `chessbot862.py` looked for "invites you" in uobot's `gump_text`, which is a list, so
  the test never matched. The server did send the invitation, and the transcript shows it.
- **Run 2:** passed, but the camera cut off the board's north half.
- **Run 3:** passed, but the board was half hidden under the game bar and the chat lines.

So the trainee now stands by the board's south-west corner, and the script's own messages go to the log only.

## Deviations and decisions for Chase

- **The spot** (above): outside the inn's front door, not inside. Moving it means editing `battle-chess.json`
  (X, Y, Z = the rim's north-west corner at ground height), running `[BattleChess seed`, and deleting the old board
  by hand.
- **The east cedar** stands two tiles off the board's south-east corner and draws beside it. It doesn't cover a
  square in the shots. Removing it would need a map change.
- **Two tool calls were denied in this unattended run.** The Read tool on
  `D:\UO\third-party\code\battle-chess-125\Battle Chess\ChessGame.cs` was denied. I read the reference source with
  `cat` instead, as the Golem's standing note and the hand-off say to do for files outside the work copies. A Grep of
  my own `server\customizations\BattleChess` for the animation calls (a last read-through) was also denied. The
  in-game run covers that path.
- **Memory:** at the end of gated build 2 free memory was 2.1 GB, under the prompt's 3 GB line. I waited until it was
  back over 3 GB (4.6 GB, about a minute) before starting the shard.

## Files

- **Code copy:**
  - `server/customizations/BattleChess/` (8 files);
  - `server/tests/Misc/BattleChessVerification.cs`;
  - `CHANGELOG.md` (2026.11.10.7: one Added line and one Staff line);
  - `VERSION` (2026.11.10.7).
- **Docs copy:**
  - this file;
  - `notes/cc-P862-shots/`;
  - `notes/cc-P862-tools/`: the probes and red runs, the mutants, the gated build wrapper and summary, the proof kit
    and runner, the spot renders, and runs 1-3.

P862 DONE
