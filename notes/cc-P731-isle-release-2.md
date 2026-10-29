# cc-P731: isle-only release 2 (round 4 fixes, the pet reward and the TazUO page fix)

Iron Golem, 2026-10-28.

## In plain words

- The isle-only release branch now also has your round 4 fixes, the pet as Wren's reward with Pet Info, Pip's
  healing lesson in the farmhouse, and the fix for TazUO's own page at start. Still none of the map swap.
  `release/isle-20261028`, commit `c925c0f` (pushed). The overseer releases from it.
- I played it in the real game client with a brand-new character that TazUO made itself. It went through:
  - the cloak chest;
  - Wren's pitchfork, war mode, the rats and snakes, then the pup as the reward;
  - Pet Info from the pup's menu;
  - Pip healed on his bench;
  - the dock both ways.
  No TazUO page opened at start. The bot also went from the beach to Rook with nothing failing.
- **One thing does not work in the real client: "Move to get up."** TazUO sends no step or turn while the server
  holds the character still, so moving does nothing. The trainee lies there until the 60-second timer stands them up.
  Windows and lines still wait until then, as you asked. It is the same on main. The bot could not see it, because
  it sends its steps straight to the server.
- For you to decide: release with the 60-second wait, or have a fix first. A fix would be its own task, for example
  "hold the trainee down without freezing them". In TazUO the lying character also shows standing, in daylight.

## What to release

- **Branch:** `release/isle-20261028`, pushed to origin (`61ebab0..c925c0f`).
- **Commit:** `c925c0fd38480059c83a3e4b354f9101166714b2`.
- **Worktree:** `D:\UO\golems\Iron\release-isle-20261028` (P722's).
- **Image tag:** `sl-modernuo:cc-P731`.
- **`VERSION`:** `2026.10.28.9`, the same numbers main uses for these sections.
- Not built as a player package, not published, not merged into main. The shared Test Shard was not touched.

## Picks (in main's merge order, each merge taken against its first parent, as P722 did)

| Task | Picked from main | On the branch | Result |
|---|---|---|---|
| P727 land P721 | `722ad95 -m 1` | not picked | Nothing to add (below) |
| P728 round 4 | `666759d -m 1` | `5cc8af5` | CHANGELOG/VERSION conflict only |
| P729 no TazUO page | `466a91e -m 1` | `45d4e0e` | clean |
| P726 via P730 | `d558cb3 -m 1` | `c925c0f` | clean |

**Merge order.** On main, P729 merged (`466a91e`) before P730 (`d558cb3`). So P729 went first here too, though the
prompt lists P726/P730 first. The two touch different files.

**P727 left out.** P727 brought P723 onto main, and the branch has P723 already (`67cd6fd`). Picked here, its
merge changed only two files:
- `CHANGELOG.md`: a new section `2026.10.28.6` repeating P721's five lines. They are already in the branch's
  `.2` section, where P723 put them.
- `VERSION`.
Every code file was byte for byte the branch's already. So I picked nothing, and the branch goes `.5` to `.7`.

**The one conflict: P728's CHANGELOG and VERSION.** I kept P728's own section under main's number `2026.10.28.7`,
dropped P727's `.6` that came with it, and set `VERSION` to `.7`. The script is
`notes\cc-P731-tools\resolve_changelog.py`. P729 (`.8`) and P730 (`.9`) then merged by themselves.

**Nothing built on swap code.** After the picks, I diffed the branch's tutorial, Evo, creation and player-package
files against main's `d558cb3`. The only differences are P678's swap edits:
- New Haven's start through `HavenSpots`;
- the yard directions in `TutorialStations`;
- `TutorialTradeTrials` and `TutorialWingTrials`;
- `HavenMoveVerification`.
P728's seed-on-load, P726's farmhouse bench and Pip, and P730's quest log use only isle coordinates. Pip's
farmhouse is P720's, already on the branch. So nothing needed adapting, and the map patch is unchanged since
`61ebab0`.

Left out, as asked: every SoS swap commit (P674 to P691) and everything else on main since `61ebab0`.

## Tests

- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P731`, `docker-build` lock, released): **EXIT=0**.
  - 2,745 shard tests: 2,740 passed, 5 skipped (the usual client-data facts), 0 failed.
  - P728's `PlayerMobile-tutorial-wake-move.patch` and both bandage patches report "Applied".
  - Output: `cc-P731-tools\green-gated-build.txt`.

## On the private shard (127.0.0.1:2596, never the shared Test Shard)

The shard ran `sl-modernuo:cc-P731` on a fresh copy of the bot world each time. The map was the branch's patch on
stock client data, P722's overlay (the map did not change). It used the `test-shard` lock, now released, and the
shard is down.

**Bot route: run 1, 0 failed checks, 85 passed** (`cc-P731-tools\runs\run1\playlog.txt`, 206 s). The route is
P726's (`isle.py`), with Rook and the New Haven start put back on stock New Haven (`make_isle_bot.py`). The checks:
- woke on cold sand; "Move to get up."; no window while lying;
- the first step spent getting up;
- the cloak chest appears, opens and goes;
- Wren's pitchfork first, then war mode, then the pests;
- "the cabbage rows are clear" in the lesson window, with the arrow on Wren;
- the pet window only after that;
- Pet Info named in the System line;
- Pip on his bench, bandaged and really healed;
- the moongate to Rook at 3501,2572;
- the New Haven pick on the plaza at 3503,2574.

**Real character in TazUO.** The client was the built one (`D:\UO\tazuo-sl-build\client`, patches 0001 to 0009). Its
`Data\Profiles` was empty except `default.json`. That file was written by the branch's own launcher function
(`Initialize-NewProfileDefaults`, P729), as `Play.ps1` does: `always_run` false, paperdoll closed, and
`last_version_history_shown` `5.31.2.0`.

How the character was made:
- TazUO made the new character itself. A test-only plugin (`cc-P731-tools\Engine.cs`, never shipped) sent the
  creation packet from the character list. Window clicks could not do it: TazUO reads the real cursor, and you were
  using this PC, so I did not take the mouse. The packet's bytes are the bot's own.
- So the character's first login was TazUO's.
- A Legion script played it (`IsleWalk731.py`), with the client's own steps, clicks, drags and speech, and no teleport.

Run 8 (`runs\tazuo8\walk.log`, shots in `cc-P731-tools\shots\`):

| Step | Result |
|---|---|
| First login | Woke at 6638,3993 with **no server window**; "Move to get up." came; the lesson's lines waited. **No TazUO Version History page**; the new profile stores `5.31.2.0`. |
| Getting up | **Failed in the client.** Three steps and a turn did nothing; up after about 60 s by the safety timer (below). Then the patch notes and achievements came, and the first lesson. |
| Cloak chest | A blue chest by the clothes rack; opened ("Chest With Your Cloak"), cloak dragged out and worn; the chest went. |
| Farm | Wren gave the pitchfork first; no pet before the pests; holding it counted; war mode counted and she opened the gate; the character killed the rats and snakes itself; the lesson window said "the cabbage rows are clear". |
| Pet reward | Back at Wren: "Choose your farm pet", then "This pet is yours to keep" and the Pet Info line; a pup. |
| Pet Info | From the pup's context menu: "Pet Info: a pup", Dog (protector), pup stage 1 of 5, 0 of 500 growth, loyalty 100% (`run7-petinfo.jpg`). Then "all follow me" and "all guard me" counted. |
| Healing | "Healing: bandage Pip"; in through the farmhouse door; Pip on his bench at 6692,3975; a bandage healed him; the lesson finished; back out the door. |
| Dock | East from 6812,3991 onto the landing at 6830,3991,-2, and back west to 6812,3991,0. No stuck step either way. |

**Facing of what is new** (my own look at the run 8 shots):
- The cloak chest stands upright on the clothes table beside the rack, blue as the isle's supply things.
- The farmhouse is whole: walls, chimney, door and steps. Inside are the hearth, the table and chair, the red rug,
  and Pip.
- The pup and the pitchfork are stock art. Their shots are partly covered by the backpack (it opens at
  login), so I did not judge them.
- Nothing I could see faced the wrong way.

**Why "Move to get up" fails in TazUO.** TazUO's `PlayerMobile.Walk` (`PlayerMobile.cs:744` and `:959`, TazUO
`3212623f`) returns before sending anything while `IsParalyzed`, which is the server's Frozen flag. P721's wake sets
`pm.Frozen = true` while lying. So the client never sends the move request that P728's
`PlayerMobile-tutorial-wake-move.patch` waits for, whether it is a step or a turn. The lie then ends only at
`TutorialWake.SafetySeconds` (60). The bot sends raw move packets, so it gets up at once.

Main has the same code. A fix belongs in its own task. One idea: hold the trainee by refusing their moves on the
server instead of freezing them. TazUO would then send the step, and the patch would spend it on getting up. Also,
P721 said a client may show the trainee standing: in TazUO the character shows standing, and the lit scene shows no
dark.

**Getting there** (runs 1 to 7, kept in `runs\`):
- Run 1: a bot-made character's later login is not a first login: the account's isle was used.
- Run 2: a disconnect while lying ends the wake.
- Run 3: auto-login took the existing Tester.
- Run 4: the first creation through the plugin.
- Run 5: found the getting-up failure; TazUO's Pathfind gives up past about 10 tiles.
- Run 6: the item-move throttle hit the pitchfork.
- Run 7: the whole route, but the facing shots were covered by windows.
These were limits of my script and setup, apart from the getting-up failure.

## Files

- Code copy: nothing. The picks are commits on `release/isle-20261028` in its own worktree, pushed.
- Docs copy: this note, and `notes\cc-P731-tools\`:
  - the resolver, the gated-build script and output;
  - `isle.py` and `make_isle_bot.py`, `proof-shard.ps1`, `pet_menu_probe.py`;
  - the TazUO runner `tazuo-walk.ps1`, `ui.ps1`, `IsleWalk731.py`;
  - the plugin source `Engine.cs` and `P731Create.csproj`, and `make_create_bin.py`;
  - `runs\` and `shots\`.
- Outside the repos: `D:\UO\golems\Iron\p731-proof\` holds the shard copy, the client, the plugin build and every
  run's shots. It can be deleted. `release-isle-20261028\` stays until the release is out.

P731 DONE
