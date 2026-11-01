# cc-P749: isle-only release 4 (wake easier to see, bandages, coast, shipwreck, signs, farm, bank, League house)

Iron Golem, 2026-10-31 (fourth start, after Chase's go-ahead).

## In plain words

- **The isle-only release branch has this round's isle work.** The wake is lighter: you can see yourself lying on
  the sand, and you get up slowly. Bandages lie on the farmhouse table, and Wren tells you where to get more. The isle
  also gets the new coast, the whole shipwreck, the signs on the north side of the paths and the turned-round farm
  with the farmhouse beside its gate. The bank and the League lodge are re-dressed. None of the map swap is in it.
  Branch `release/isle-20261028`, commit `9c31000` (pushed). The overseer releases from it.
- **I played it in the game with a brand-new character.** The character lay flat in the lighter dusk with "Move to
  get up." over its head, got up slowly on its first move, and saw no window until it stood. It took the bandages
  from the table, heard Wren's hint, healed Pip, and walked chat sign, farm, farmhouse, then on east, never
  doubling back. Then it walked into the bank and the League lodge and out along the dock. 77 checks, none failed.
  The bot also went from the beach to Rook with nothing failing (85 checks).
- **In the shots:** both wreck halves run aground the right way (`tester-wreck-from-north.jpg`). Every sign stands
  north of its path. The bank and the lodge look as on main.
- **One thing you may notice:** the north, north-east and east beaches still step a little at the sand's edge.
  P741 left them that way, and main is the same. The west beach and the beach by the training yard are smooth.
  Nothing for you to do; the overseer builds and publishes the player package from the branch.

## What to release

- **Branch:** `release/isle-20261028`, pushed to origin (`9e616f3..9c31000`).
- **Commit:** `9c3100006a496998791d8a89a433cac329f249d9`.
- **Worktree:** `D:\UO\golems\Iron\release-isle-20261028` (P722's).
- **Image tag:** `sl-modernuo:cc-P749` (image `13e1d307afe7`).
- **`VERSION`:** `2026.10.31.4`. As P731 and P733 did, the release takes main's numbers for its sections: `2026.10.30.3`
  (P740) and `2026.10.31.4` (the isle round).
- Not built as a player package, not published, not merged into main. The shared Test Shard was not touched.

## Chase's answer, and what was on main

- Chase's answer `Iron-P749-20261031-175622-383d` (18:21): "P751 (which carries P741 and P746) passed review P752 and
  merged to main at 18:04. Go ahead with the release."
- Code main (`origin/main`) is `1ce8f7a`: "Merge golem/Iron/P751".
- **P741 and P746 are on main only inside P751.** P751 applied P746's whole change (P741 plus P746) onto main, without
  merging (see P751's notes, "Getting P746's work onto this branch"). So main has one commit, `34ed792`, holding P741,
  its fix-up P746 and P751's seven review fixes. `golem/Iron/P741` and `golem/Iron/P746` are not ancestors of main.
- No other commit on main after P740 touches the Tutorial folders or names P740, P741, P746 or P751.

## Picks (in main's merge order, each merge taken against its first parent, as P722, P731 and P733 did)

| Task | Picked from main | On the branch | Result |
|---|---|---|---|
| P740 wake, bandages | `b2efbd2 -m 1` | `847dd8e` | CHANGELOG and VERSION conflicts only |
| P741 + P746 + P751 isle round | `1ce8f7a -m 1` (holds `34ed792`) | `9c31000` | CHANGELOG, VERSION and `trammel.mapops` conflicts |

- **Merge order:** on main, P740 merged first (`b2efbd2`), then the SoS swap's P691 and P708, P750, then P751
  (`1ce8f7a`). The swap merges were not picked.
- Each commit keeps its task's subject line, plus a line naming the merge it was picked from.
- **Every code and test file both picks touched is byte for byte main's** (`git diff` against `b2efbd2` and `1ce8f7a`,
  each file). That covers TutorialWake, TutorialFarm, TutorialCoreTrials, TutorialVisionScene, TutorialCorePlacement,
  TutorialIsleAddons, TutorialIsleFarmLayout, TutorialWorld and IsleAddons-SOURCE.txt, and the nine test files. Among
  them is P746's CreatureLevels test fix (it reads The Butcher's level more times).
  - Nothing in them is built on swap code. The isle's spots are the same on both lands, and the build compiles and
    passes on the stock branch (below).

**Left out, as asked:** every SoS swap commit (P674 to P691, P708), P690, P750 (guild headquarters on the SoS land),
P743 (New Haven), and everything else on main since `9e616f3`.

## How each conflict was resolved

**`CHANGELOG.md` and `VERSION`** (`notes\cc-P749-tools\resolve_p740.py`, `resolve_p751.py`):
- P740: kept main's `2026.10.30.3` section (its two isle lines). Dropped main's `2026.10.30` Staff section (the SoS
  swap's credits). VERSION `2026.10.30.3`.
- The isle round: kept main's `2026.10.31.4` section (its ten isle lines). Dropped `2026.10.31.3` (P750, the Rangers'
  guildmaster at Fort Viridian) and `2026.10.31` (P708, guild headquarters on the SoS land). VERSION `2026.10.31.4`.

**`trammel.mapops`** (the map patch). The round's map changes were made on main's SoS-based patch. I adapted them
block by block, as P722 and P733 did (`mapops_plan.py` checks, `mapops_merge.py` writes the file):
- The round changed **471 blocks** (x 6624-6871, y 3904-4055). All of them are on the isle (`mapops-plan.txt`).
- **All 471 sit on void in both maps:**
  - their fingerprints are the same on the release (stock) and on main (SoS);
  - the release's lines in them equal main's lines before the round (`34ed792^`).
  - The round changed no fingerprint and not the header.
- So the release's file is its own stock-land file with exactly those blocks' lines taken from `34ed792`. Each op
  kind's run is kept in mapops.py's x,y order.
- **Check:** the release's change to the file is exactly main's round, line for line. That is 16,546 lines in and
  16,550 out, and the sorted `+`/`-` lines are identical. Everything outside the isle stays the release's own,
  including Old Haven's way in, the Burrows' mouth and P276's farm removals.
- P741's `trammel-stock-base.mapops` was not used: P746 and P751 changed the isle after it.
- git's own merge conflicted only because sorted neighbour lines outside the isle differ between the two bases.

## Tests

- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P749`, `docker-build` lock taken and released): **EXIT=0**.
  - 2,761 shard tests: 2,756 passed, 5 skipped (the usual client-data facts), 0 failed (`green-gated-build.txt`).
  - Among them: TutorialIsleWakeVisible 2, TutorialIsleCoast 5, TutorialIsleReviewFixes 4, TutorialIsleWalkFixes2 6
    and TutorialFarm 15, all passed.
  - Every patch reports "Applied", among them `PlayerMobile-tutorial-wake-move.patch` and the bandage patches.
  - Free memory at the start: 10.9 GB on Windows and 13 GB in the Docker VM. The build ran detached.
- **Map facts:** main's `tools/tests/test_mapops.py` on the release's patch (`test-mapops-release.txt`): 9 passed, 1
  skipped, 4 failed. All four failures come from the stock base, not from the isle:
  - 12 (Blackthorn's dungeon copy) and 4 (a line at 3615,2616): the SoS swap's lines, which the release does not
    have;
  - 6 (Old Haven's way in is gone): the release keeps it, as P722 and P733 did;
  - 7 (the isle is the build): this docs branch predates P751, so the fact read old builder CSVs. Rerun against
    main's CSVs (`fact7_main_csv.py`, `fact7-main-csv.txt`): **all 7 parts pass**, so the release's isle is main's
    build exactly.
  - The isle's own facts pass: 11 (surf and plants), P741's coast fact and P751's 13 (the yard's beach runs straight).

## On the private shard (127.0.0.1:2596, never the shared Test Shard)

Setup:
- The shard ran `sl-modernuo:cc-P749` on a fresh copy of the bot world (`proof-shard.ps1`, its own container
  `sl-p749-proof`).
- The map was the branch's patch on **stock** client data, built by the branch's own `Build-MapOverlay.ps1`
  (`overlay.ps1`).
- The `test-shard` lock was taken twice and released both times, and the shard is down.
- **Seed on load** (`seed-on-load.txt`): "1 props" (the lodge sign), "placed 1 farm addon, 3 door, 2 spawners" (the
  farm laid fresh), "Isle addons: placed 1, replaced 1 old wreck".

**Bot route: 0 failed checks, 85 passed** (`runs-run1-console.txt`, `runs\run1\`, 186 s).
- The route is `isle.py`, made by `make_isle749.py` from P733's (the release's stock New Haven). It adds P740's two
  wake-timing lines, and then main's `cc-P741-tools\make_isle741.py` adds the turned-round farm. It differs from
  main's P741 route only in New Haven's spots.
- A fresh character woke on the sand at 6638,3993, saw "Move to get up.", and its first step got it up.
- Then:
  - the cloak chest;
  - Wren at the new gate (6696,3978) with the pitchfork, war mode and the pests;
  - the pet;
  - Pip healed in the farmhouse at its new place (door 6702,3978);
  - the yard, the bank, the lodge and the vision.
- The moongate put it beside Rook at 3501,2572. The New Haven pick started on the plaza at 3503,2574.

**Real character in TazUO: 77 checks, 0 failed** (`runs\tazuo1\walk.log`, shots `shots\tazuo-*.jpg`).
- The client was the built TazUO with no profiles except the release launcher's `default.json`. Its map was built from
  the branch's patch on stock data (no `-MapBase`), as the package does.
- TazUO made **Iron Rook** itself from the character list, with P731's test-only creation plugin.
- `IsleWalk749.py` (made by `make_walk749.py` from P740's walk, itself from P733's stock-land walk) played it with the
  client's own steps, clicks, drags and speech, and no teleport.

| Step | Result |
|---|---|
| Lying | At 2, 5 and 10 s: drawn lying flat in the lighter dusk beside Tamsin, "You lie on the wet sand... Move to get up." over the head, no server window (`tazuo-lying-02`, `-10`). |
| Getting up | A turn only. A slow get-up across the burst frames (`tazuo-getting-up-02` to `-12`), on the same tile. The first lines came 5.2 s after the turn, the first window 2.0 s after them, nothing before. |
| Bandages | The lesson's bandages set down. Wren's hint over her head (`tazuo-wren-hint`). Wren double-clicked: "Here are more bandages". Set down again. In the farmhouse, bandages lie on the table at 6702,3975,13; dragged: "You take some bandages from the table", and the stack stayed (`tazuo-table-bandages`). Pip healed with them; lesson finished (`tazuo-healed`). |
| Farm order | Chat sign (x 6690), Wren at the gate (6697), in the farmhouse (6702), the road east (6719): each stop east of the last, no doubling back. |
| Bank | Past the fountain to the bank door (6762,3981). The fountain blocks no way in. |
| League lodge | In through its door to 6782,3997 and back out to the road. |
| Dock | East onto the moongate frame (6830,3991, z 4) and back west, no stuck step. |

**Shots of the round's places** (`shots\tester-*.jpg`). Iron the Tester was moved beside each of P741's and P751's
spots by the Admin (`isle-shots749.ps1`, `shots749.json`, `shots749b.json`). My own look at them:
- **Wreck** (`tester-wreck-from-north`, `tester-wreck-both-halves`): two halves, both upright, run aground across the
  waterline. The stern half stands in the shallows, the bow half up the beach, their broken ends toward each other,
  with driftwood round them. The first wreck shot (`tester-coast-wreck`) had the paperdoll over it, so I retook it
  from two spots.
- **Coast:**
  - the west beach (`tester-coast-west`, `-southwest`), the yard's west and south beaches and their corner: smooth,
    with surf along the sand;
  - the north, north-east and east beaches (`tester-coast-north`, `-northeast`, `-east`): still a small step at the
    sand's edge. P741 notes this ("The far coasts still step"), and the isle's lines are main's.
- **Signs** (`tester-sign-1-movement`, `-4-chat`, `-6-death`, `-11-travel`, `tazuo-path-*`): each stands on the north
  side of its path, facing it. The travel sign stands where the road meets the dock.
- **Farm** (`tester-farm`, `-farm-gate`, `-farmhouse-front`, `-inside`, `-roof`, `-fence-nw`, `-fence-se`):
  - the field is west, with ploughed soil and fewer, low crops, and its gate is on the east fence;
  - the farmhouse stands right beside the gate;
  - the hearth is on the back wall, with no chimney through the thatch;
  - nothing stands before the windows;
  - the fence corners are clean.
- **Bank** (`tester-bank-front`, `-inside`): it sits in the grass with a small paved step at its door and a paved
  square round the fountain. Inside: the counter with scales and coin, and a strongbox in the vault.
- **League lodge** (`tester-lodge-front`, `-inside`, `-sign`; `tazuo-lodge-inside`): an even wooden floor,
  bookcases, a long table with chairs, candles, and banners outside between the windows. Its name sign stands beside
  the League lesson sign north of the road.

## Deviations and decisions

- **One pick for three tasks.** The prompt names P741 and its fix-up P746. On main they exist only inside P751's
  commit, together with P751's review fixes (a fix-up of those tasks, which the prompt allows). So the second pick is
  that one merge.
- **Commits and a push.** The Golem's standing rule is no commits or pushes. This prompt asks for a pushed release
  branch, so, as P722, P731 and P733 did, I committed the two picks on `release/isle-20261028` in its own worktree and
  pushed that branch only. My Golem branches have no commits from me; the only new files are these notes and tools.
- **Map fact 7** was rerun against main's CSVs because this docs branch is older than P751 (above).
- **No player package, no shared Test Shard, no merge into main.**

## Earlier sessions (same day)

- Three earlier starts stopped because P741 and P746 were not on main. Chase answered "Wait" (15:22, 15:27). P751
  merged at 18:04 and Chase said to go ahead (18:21). Those stops changed nothing on any branch.

## Files

- Code copy: nothing. The picks are commits on `release/isle-20261028` in its own worktree, pushed.
- Docs copy: this note, and `notes\cc-P749-tools\`:
  - the resolvers and map tools: `resolve_p740.py`, `resolve_p751.py`, `mapops_plan.py`, `mapops-plan.txt`,
    `mapops_merge.py`, `mapops-merge.txt`, `fact7_main_csv.py`, `fact7-main-csv.txt`, `test-mapops-release.txt`;
  - the build: `gated-build.ps1`, `gated-build.log` (UTF-16), `green-gated-build.txt`;
  - the shard: `overlay.ps1`, `proof-shard.ps1`, `seed-on-load.txt`;
  - the bot route: `make_isle749.py`, `isle.py`, `runs-run1-console.txt`, `runs\run1\`;
  - the TazUO walk: `run-tazuo.ps1`, `tazuo-walk.ps1`, `ui.ps1`, `make_create_bin.py`, `make_walk749.py`,
    `IsleWalk749.py`, `runs\tazuo1\`;
  - the shot tools: `isle-shots749.ps1`, `shots749.json`, `shots749b.json`, `Clear741.py`, `copy_shots.py`,
    `sheet749.py`;
  - `shots\`: 22 `tazuo-*.jpg` from the walk, 28 `tester-*.jpg` from the spots (shrunk to 960 wide), and the proof
    logs.
- Outside the repos: `D:\UO\golems\Iron\p749-proof\` holds the shard copy, the overlay, the clients, the bot copy and
  the full-size shots. It can be deleted. `release-isle-20261028\` stays until the release is out.

P749 DONE
