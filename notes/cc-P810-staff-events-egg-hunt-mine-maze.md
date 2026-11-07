# cc-P810: staff events: egg hunt and mine maze

## In plain words

- **Staff can now run an egg hunt.** On the Staff Hub's Events tab, press "Egg hunt, maze", then "Hide egg here". Every player on that facet gets an arrow to the egg. The first to reach it and double-click it wins 25 Festival Tokens, and the shard hears who did. It ends by itself after 30 minutes if nobody finds it.
- **Staff can now lay a mine maze.** Mark two corners and press "Lay the maze". Players walk in over the start row and learn the hidden mines by dying on them. They keep everything they carry and rise at the start 5 seconds later. The first three across win 20 Festival Tokens each. "Reset" moves the mines and opens the prizes again for everyone.
- **Both are off until a GM starts one.** All the numbers are in `Configuration/staff-events.json`, including whether the maze pays tokens or a small loot box.
- **For you:** nothing is required. Try `[SL`, then Events, then "Egg hunt, maze", next time you're on the test shard.

## What was built

All of this is in `D:\UO\golems\Iron\ShatteredLegacy`.

| File | What it is |
|---|---|
| `server/customizations/StaffHub/StaffEventsSettings.cs` | `Configuration/staff-events.json`: written with the defaults on first start, and refused whole when wrong |
| `server/customizations/StaffHub/StaffEggHunt.cs` | The hunt, its arrow (`EggHuntArrow`) and the saved type `EventEgg` |
| `server/customizations/StaffHub/StaffMineMaze.cs` | The maze's layout (`MineMazeRun`), its region (`MineMazeRegion`), the rules and prizes, and its save (`StaffMineMazeStore`) |
| `server/customizations/StaffHub/StaffEventsGump.cs` | The events gump and the `[StaffEvents` command |
| `server/customizations/StaffHub/StaffHubGump.cs` | One "Egg hunt, maze" button on the Events tab, in both the setup view and the running-surge view, and its response |
| `server/tests/Misc/StaffEventsVerification.cs` | 14 facts |
| `CHANGELOG.md`, `VERSION` | `2026.11.07.3`: two Added lines and one Staff line |

There is no engine change and no `.patch` file.

### Egg hunt

Credit: the idea came from Bittiez's World Egg Hunt (third-party, reference only). No code was taken.

- **Hiding the egg:** a GM hides it where they stand or at a target. It can't go on the Wakening Isle, and only one hunt runs at a time.
- **The egg:** art 0x47E6, the dragon Easter egg (one large egg), in a random bright hue. It can't be moved.
- **Arrows:** every player on the egg's facet gets one, and so does anyone who arrives later, within 20 seconds. Staff get none.
- **Winning:**
  - The first living player within 2 tiles who double-clicks it wins `EggTokens` (25) through `FestivalTokens.Grant`.
  - The shard is told who won, every arrow is stopped, and the egg is removed.
  - Staff and ghosts can't win, and nobody can claim it from far away. The original had no working range check.
- **Ending:** after `EggMinutes` (30), by the GM's End button, or by a restart. A saved egg deletes itself after load, so no hunt outlives the server.
- **No power scrolls.** The original's power scroll prize is gone.

### Mine maze

Credit: the idea came from ExX's Landmine maze (third-party, reference only). No code was taken. The original laid mines one at a time by hand and used a token; here the whole field is laid from a seed.

- **Laying it:** a GM marks two corners. Each side must be at least 5 tiles, the area at most 1,600 tiles (40 x 40), and it can't be on the isle. Only one maze runs at a time.
  - The maze runs along the longer side. The start row is the end nearest the first corner, and the finish row is the far end.
- **The mines:** a seed lays one safe path that only moves forward or sideways, so it always connects start to finish. Mines then cover 35% of the other tiles. The start and finish rows are safe.
  - Everyone in a run gets the same layout, so players learn it by dying.
  - Mines are not items. They are a set of tiles checked as players step (`MineMazeRegion.OnLocationChanged`), so a 40 x 40 field puts nothing in the world.
- **The region:**
  - Players may only walk in over the start row.
  - Young characters are kept out.
  - No recall, gate, mark or teleport works in or out.
  - No house can be placed there.
  - Staff are exempt from all of these.
- **A mine:** an explosion effect and sound, then death. A death anywhere in the maze keeps every item: the corpse's contents go back to the backpack, as in a surge's no-loot zone. After `MazeReviveSeconds` (5) the player is resurrected at the middle of the start row.
- **Winners:** the first `MazeWinners` (3) living players to reach the finish row win, once each. The prize is `MazeTokens` (20) Festival Tokens, or with `MazePrize: LootBox` a loot box (`MazeBoxTheme` Explorer, `MazeBoxTier` 1) through `ClusterFLootBoxes.MakeBox`. The shard is told each place. Later finishers are told every prize has been won.
- **Reset (the fair reset):** a new seed moves the mines, the winners are cleared, and everyone inside goes back to the start row. "Remove maze" takes it all away.
- **It survives a restart.** The corners, seed, mine percent and winners are saved. The region is registered again at world load, and doing that twice does nothing.
- **Typed commands:** `[StaffEvents` with `status`, `reload`, `egg here`, `egg end`, `maze corner1`, `maze corner2`, `maze lay`, `maze reset`, `maze end` or `maze path`. `maze path` lists the safe path for staff only, so a GM can check a layout or show a winner the way.

### Rules check

- **Nothing grants** skill or stat points, power scrolls, bless deeds or property artifacts. The prizes are Festival Tokens or a loot box. No power scroll, stat scroll or bless deed type appears anywhere in the loot box code.
- **All numbers are in** `staff-events.json`.
- **It reaches an existing world by itself.** The command, the Events tab button and the settings file arrive with the build. A saved maze is registered again on load, idempotently. Nothing has to be seeded in the world, since both events are off until a GM starts one.
- **No engine change.**
- **Serialization (D40):**
  - `EventEgg` uses the generator at version 0.
  - `StaffMineMazeStore` writes its own version, and an unknown version throws `InvalidDataException`.
- **The web console** is listed under the prompt's Touches, but nothing there needed changing. The console has no surge or Staff Hub view, and both events live in the game's Staff Hub, as P797's sketch said.

## Tests

- **Red:** I wrote the facts beside the code, so to see each one fail I broke the code on purpose, in a throwaway container from `sl-uo-builder:cc-P808` (`mutate810.py`, results in `mutants.txt`). I made 38 breaks, and every one of the 14 facts went red at least once.
  - One break went unseen at first (`twiceprize`: a winner crossing twice). The cap of three hid it, so I tightened `TheFirstThreeThroughWinOnceEach` so the first runner crosses twice before anyone else. That break then failed it (`twiceprize.log`).
  - All 14 facts pass on the real code, along with the 30 existing Staff Hub facts.
- **Gated build:** `sl-modernuo:cc-p810` (`c34679ecfd34`), 197 patches applied, **3,219 shard tests passing, `EXIT=0`**.
  - This ran twice. The first run (`gated-build-1.log`) was also green. I then widened the events gump, because the first shots showed cropped labels, and built again on the final code.
  - `latest` was not moved.

## Proof shots (TazUO, private proof shard 127.0.0.1:2596)

These are in `notes\cc-P810-shots\`. A new character on the meadow by Britain's south road set things up as staff, then set itself to Player. Every check in `walk.log` passed.

1. `1-staff-hub-events-tab.jpg`: the Events tab with the new "Egg hunt, maze" button.
2. `2-staff-events-gump.jpg`: the events gump.
3. `3-egg-hunt-arrow.jpg`: the hunt's arrow as a player.
4. `4-the-egg.jpg`: the egg on the ground, with the arrow over the player.
5. `5-egg-found.jpg`: the win, with tokens and the shard line.
6. `6-maze-start.jpg`: standing at the maze's start row.
7. `7-mine-death.jpg`: "You stepped on a mine!" and "Your belongings are safe…".
8. `8-risen-at-start.jpg`: risen at 1990, 2243, the middle of the start row.
9. `9-maze-crossed.jpg`: the safe path walked, with "+20 Festival Tokens (the mine maze, place 1)" and "Iron Events has crossed the mine maze, place 1 of 3!".

**Not my code:** the journal in these shots also shows "A bag of PowerScrolls has been placed in your bank box" and "One of each level of treasure map…". That is pinned's test-center welcome text for a new character (`Misc/WelcomeTimer.cs`, test center only). The death achievement's loot box is also there; it comes from the shard's existing "died for the first time" achievement.

## Deviations and decisions for Chase

- **Two harness denials.** An unattended run cannot approve these.
  - When I meant to re-check the one break that went unseen, a combined command was denied. It was going to: edit the fact, copy the `twiceprize` break into a folder of its own, run it with a copy of the break runner, then `rm -rf` the copies. I made the same fact edit and re-ran that one break with `run-facts.sh` (its mutant-folder argument) instead. The fact went red, as expected.
  - In P809 the Grep tool was denied on `apply-patches.sh`. This prompt needed no patch.
- **Memory:** free memory was 3.1 GB before the first build, just above the 3 GB stop line. Most of it was the Docker VM's page cache, so I dropped that cache and memory rose to about 6 GB. I did not stop to ask.
- **Festival Tokens are granted even out of season.** `FestivalTokens.Grant` doesn't check the season, and players spend them at the festival store when it opens. If you'd rather the events pay gold, or a loot box, out of season, say so. A loot box is already one setting away (`MazePrize`).

## Tools

These are in `notes\cc-P810-tools\`:

- `run-facts.sh`: quick fact runs, optionally with a break.
- `mutate810.py` and `run-mutants*.sh`: the deliberate breaks, with results in `mutants.txt`.
- `gated-build.ps1`: the gated build.
- `shots.ps1`, `Shots810.py` and the TazUO rig copied from P804's.

Both locks have been released.

P810 DONE
