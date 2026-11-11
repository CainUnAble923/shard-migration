# cc-P863: Color Wars, an opt-in staff team event

## In plain words

- **Staff can now run Color Wars, a team battle between players.** On the Staff Hub's Events tab, press "Color Wars"
  (or type `[ColorWars`). Mark the arena's two corners, open it for 2 or 4 teams, put the gate where players gather,
  start the battle when the teams are in, and end it.
- **Players choose to join.** Stepping into the gate asks first. Joining puts you on the smallest team, dressed and
  armed in your team's colour with a lent kit. Everything you had waits in a bag in your bank and comes back when you
  leave (by your team's stone) or when the battle ends, even if you are logged out. A death costs nothing: you rise
  at your base a few seconds later.
- **The winning team gets 15 Festival Tokens each.** The team with the most kills wins when staff end it; a tie pays
  nobody. Nothing is learned in the arena (no skill or stat gain), and nobody can recall or gate in or out.
- **For you:** nothing is required. Try `[SL`, Events, "Color Wars" next time you're on the test shard; it needs two
  players to be a fight.

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy, both on `golem/Iron/P863`.
Read first: `notes\cc-P854-tools-minigames-assessment.md` (item 5) and `notes\cc-P810-staff-events-egg-hunt-mine-maze.md`.
Main only. The source, `D:\UO\third-party\code\color-wars` (Omni, servuo.dev 2014), was read as reference only:
nothing in it was built, run or copied. Credit to Omni is in the code's header, the staff gump's title and the
CHANGELOG line.

## What was built

| File (ShatteredLegacy) | What it is |
|---|---|
| `server/customizations/StaffHub/StaffColorWars.cs` | The event: the arena region (`ColorWarsRegion`), the run and its players, joining, the lent kit, the bank stash, deaths, scores, leaving, the end and the payout, the notoriety colours, the gate (`ColorWarsGate`), the exit stones (`ColorWarsExitStone`), the join question (`ColorWarsJoinGump`) and the save (`StaffColorWarsStore`) |
| `server/customizations/StaffHub/StaffColorWarsGump.cs` | The staff gump and `[ColorWars` |
| `server/customizations/StaffHub/StaffEventsSettings.cs` | Eleven `Cw*` numbers in `Configuration/staff-events.json`, range-checked like the rest |
| `server/customizations/StaffHub/StaffHubGump.cs` | A "Color Wars" button on the Events tab, under "Egg hunt, maze", in both views |
| `server/tests/Misc/ColorWarsVerification.cs` | 14 facts |
| `CHANGELOG.md`, `VERSION` | `2026.11.10.8`: one Added line and one Staff line (.7 is taken by P861 and P862) |

No engine change, no `.patch`, no PlayerMobile edit.

### How it plays

- **Staff:** mark two corners (8 tiles a side at least, 4,096 tiles at most, never on the Wakening Isle, one arena at
  a time), then open it for 2 teams (red and blue, at the two ends of the long side) or 4 (red, blue, white and black,
  in the corners). Each team gets an exit stone at its base. "Gate here" puts the join gate (a moongate) where the GM
  stands, never inside the arena, and tells the shard. "Start the battle" lets the teams fight. "End: most kills win"
  pays the leading team and sends everyone home; "Call it off" sends everyone home with no prize.
- **Joining is opt-in.** Stepping into the gate (or double-clicking it) asks first, and says what happens to your
  things. Refused: the dead, the Young, the mounted, staff, and an ungraduated trainee on Haven Island (see
  Deviations). A late joiner may join while the battle runs. Teams stay even: a new player goes to the smallest team.
- **No item loss.** Everything worn and carried (not hair or the backpack itself) goes into one bag in the player's
  bank. The lent kit is all in the team's colour and none of it blessed: a robe, studded armour and a leather cap, a
  viking sword, a bow and 100 arrows, a full spellbook with 30 of each reagent, and 50 bandages (each part can be
  turned off in the settings). The body takes the team's colour too.
- **The fight.** While the teams gather nobody can harm anybody (the original's walls). Once it starts, players may
  harm the other teams only, and help their own team only. Teammates show green and the other teams orange; nobody
  turns criminal or gets a murder count for an event kill. A death keeps every kit piece (the corpse's contents go
  back to the pack and the corpse is removed), scores a kill for the killer's team, and the player rises at the base
  `CwReviveSeconds` (5) later with the kit put back on.
- **The arena:** nobody walks in from outside, a player who walks off the field is brought back to the base, no
  recall, gate or mark in or out, no house, and no skill or stat gain (`Region.AllowGain`).
- **Leaving:** a team's stone (within 2 tiles) or the end. The kit is taken back wherever it is (on the floor too),
  with any stack split off it; the player's own things come back, worn ones worn again (a piece they may not wear
  goes to the pack), the bag is removed, and they stand where they joined. A logged-out player gets everything back
  and wakes where they joined.
- **Winning:** the leading team's players get `CwWinTokens` (15) Festival Tokens each; a tie, or no kills, pays
  nobody. With `CwKillsToWin` above 0 the first team to that many kills wins at once (0, off, by default).
- **It survives a restart:** the arena, phase, scores, gate, stones and every player (team, bank bag, worn list, kit,
  where to return) are saved, versioned (an unknown version throws), and the region is registered again at world
  load. A saved gate or stone with no run behind it removes itself after load. Nothing else needs seeding: the event
  is off until staff open one, and the button, command and settings arrive with the build.

### Rules check

- Nothing grants skill or stat points (no gain in the arena at all), power scrolls, bless deeds or property items.
  The only prize is Festival Tokens through `FestivalTokens.Grant`. The kit is lent and taken back.
- Credit: Omni, in the code header, the staff gump's title and the CHANGELOG line.

## Tests

- **Red, then green.** The facts were written with the code, so each was watched red by breaking the code on purpose
  (`notes\cc-P863-tools\mutate863.py`, 50 breaks, run in one throwaway container from `sl-uo-builder:cc-P872`).
  - Round 1 (`mutants.txt`): 47 of 50 turned a fact red. The three unseen: `blessedkit` broke a line that changed
    nothing (no worn kit piece is blessed by default; the break moved to the carried pieces, where the spellbook is),
    `kitstays` (no kit piece had left the pack; the leave fact now drops the bow on the arena floor) and `playergm`
    (a player's press failed for want of corners anyway; the fact now checks a player's corner press does nothing).
  - Round 2 (`mutants-2.txt`): all three red, and the real code green. Every one of the 14 facts went red at least
    once.
- **Gated build** `sl-modernuo:cc-p863` (`gated-build.ps1`, docker-build lock, page cache dropped first, `latest` not
  moved): **EXIT=0, 3,387 tests passed** (`gated-build.log`). It ran three times, each green: before the first proof
  run (`gated-build-1.log`), after the join question was made taller (`gated-build-2.log`), and on the final code
  with the notoriety refresh below (`gated-build.log`).
- Free memory was 1.1 GB before the first container; dropping the Docker VM's page cache brought it to 7.7 GB, so I
  did not wait.

## Proof shots (TazUO, private proof shard 127.0.0.1:2596, test-shard lock)

In `notes\cc-P863-shots\` (the final run's full folder is `final\`, with `walk.txt` and the frames).

- "Iron Wars" (on the Golem's admin account, as P810 did) set things up as staff, then dropped to Player.
- The other team was "Iron the Tester" on the Golem's Player account, driven by the uobot client (`kit\foe863.py`),
  which stepped into the gate and answered Join itself.
- The arena was the meadow by Britain's south road (1987-2002, 2237-2246, Trammel), the gate at 1983, 2242.
- On this proof copy only, `CwKillsToWin` was 1 and the other player was left at 1 hit point, so one fight shows the
  kill, the payout and the trip home.
- All checks in `final\walk.txt` passed. Its last line, "did not answer end", is the bot logging out before it
  acknowledges, as written.

1. `1-staff-hub-events-tab.jpg`: the Events tab with the new "Color Wars" button.
2. `2-color-wars-gump-closed.jpg`: the staff gump before an arena is open.
3. `3-color-wars-gump-open.jpg`: the arena open, the gate placed, the other player on the Blue team.
4. `4-before-the-gate-own-things.jpg`: the character's own pack (1,000 gold and its things) before joining.
5. `5-the-gate-asks.jpg`: stepping into the gate asks first.
6. `6-in-the-arena-with-the-kit.jpg`: in the arena in red, the pack holding only the lent kit.
7. `7-the-kill.jpg`: "Iron Wars (Red) defeats Iron the Tester (Blue)", "+15 Festival Tokens", "The Red team has won
   Color Wars! (Red 1, Blue 0)", "Color Wars is over. Your own things are back with you."
8. `8-won-and-home-with-own-things.jpg`: back where it joined with its own pack; attacks on the other player are now
   refused ("You cannot perform negative acts on your target"), Trammel's rules again.

Two earlier runs are kept:

- `run1\`: the other player's bot used a direction name its client does not know, so it never joined.
- `run2\`: the other player joined, but TazUO asked "This may flag you criminal!" at every attack, so no blow was
  struck: the client still showed the other player as innocent. This found a real bug. Joining changes how players
  see each other, but nothing told the clients already showing them. `StaffColorWars.RefreshNames` now resends each
  player of the event to the clients in range after every join and leave, and run 3 fought with no prompt.

**Not my code:** the journal in the shots shows the test center's welcome gifts for a new character ("A bag of
PowerScrolls has been placed in your bank box", treasure maps, gold, raw materials, tools: pinned's
`Misc/WelcomeTimer.cs`, test-center shards only) and the staff character's skill gains before it joined. "You may not
wear this." at the end is the character's own GM robe going back to the pack because it is now a Player.

## Deviations and decisions for Chase

- **One harness denial.** An unattended run denied a combined command that was going to: apply the fact and code
  edits, regenerate the three unseen breaks, `rm -rf` the round-1 `mutants` folder and swap in a new one, then run
  them. I made the edits on their own, wrote the round-2 breaks into a new folder (`mutants-2`) with no deletion, and
  ran them. Afterwards both mutant folders (copies of the source) were moved to my scratchpad, not committed.
- **An ungraduated trainee on Haven Island cannot join.** The isle gate refuses their move off the island, and the
  first fact run showed a join would otherwise have put their things in the bank and left them standing by the gate.
  They are now refused before anything is touched. A gate placed in New Haven therefore suits graduates only.
- **Who may join:** I refused the Young, the mounted and staff. Young characters are protected from players, a mount
  cannot be put in a bank, and staff run the event. Say if you want any of these changed.
- **The prize** is 15 Festival Tokens per winner (the original paid 10 tokens of its own), granted in any season, as
  P810's events are. It is one setting (`CwWinTokens`).
- **A small kit leak is possible:** a stack split from the kit (bandages, arrows, reagents) and handed across the
  arena's edge to someone outside is not taken back.

## Tools

In `notes\cc-P863-tools\`: `run-facts.sh` (quick fact runs), `mutate863.py`, `run-mutants.sh` and
`run-mutants-inner.sh` with `mutants.txt` and `mutants-2.txt`, `gated-build.ps1`, `build-then-run.ps1`, `run863.ps1`,
and `kit\` (P872's TazUO rig repointed, with `Walk863.py`, `foe863.py`, and `proof-shard.ps1` setting the proof copy's
`CwKillsToWin`). Both locks were released by the scripts.

P863 DONE
