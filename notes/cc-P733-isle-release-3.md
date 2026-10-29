# cc-P733: isle-only release 3 (isle addons, the wake pose fix, shore and tropical plants)

Iron Golem, 2026-10-29.

## In plain words

- The isle-only release branch now also has three things. The new dressing: the shipwreck on the beach where you
  wake, the lighthouse by the dock, the stone frame round the moongate and the fountain by the bank. The real beaches
  with surf, and the tropical palms and jungle. And the wake fix: you lie on the sand until your first move. Still
  none of the map swap. `release/isle-20261028`, commit `9e616f3` (pushed). The overseer releases from it.
- I played it in the real game client with a brand-new character that TazUO made itself:
  - It lay flat on the sand in the dark for 25 seconds and got up on its first move, a turn, on the same tile.
  - It went through the cloak chest, Wren's pests and the pup reward, Pet Info, and Pip healed in the farmhouse.
  - It walked past the fountain to the bank door, then along the dock into the moongate frame and back.
  Nothing failed. The bot also went from the beach to Rook with nothing failing.
- In the shots, the wreck, lighthouse, frame and fountain stand upright and face the right way. None of them is on
  the road or a lesson's path. The new palms and jungle leave the road and every stop clear.
- One thing you may notice: the north and south shores still have a small stepped edge, with surf along it. The west
  side is smooth. P725 built it that way, and it is the same on main.
- The sparring dummy and the market tents are not in it: P724 did not place them (no lesson uses the tents, and
  ModernUO has nothing for the dummy; the yard already has stock training dummies). Nothing for you to do.

## What to release

- **Branch:** `release/isle-20261028`, pushed to origin (`c925c0f..9e616f3`).
- **Commit:** `9e616f37e6cd5b9b728c25d77e84d34e7e34e1cf`.
- **Worktree:** `D:\UO\golems\Iron\release-isle-20261028` (P722's).
- **Image tag:** `sl-modernuo:cc-P733` (image `30cfe4fa09ca`).
- **`VERSION`:** `2026.10.29`, main's numbers for these sections (`.10` P724, `.12` P732, `2026.10.29` P725).
- Not built as a player package, not published, not merged into main. The shared Test Shard was not touched.

## Picks (in main's merge order, each merge taken against its first parent, as P722 and P731 did)

| Task | Picked from main | On the branch | Result |
|---|---|---|---|
| P724 isle addons | `e09dbc4 -m 1` | `07477e6` | clean |
| P732 wake pose, first move | `b5373e2 -m 1` | `e803220` | clean |
| P725 shore and plants | `92f6392 -m 1` | `9e616f3` | `SOURCE.txt` conflict; map merged by itself (checked below) |

- **Merge order:** on main, P724 merged first (`e09dbc4`), then P732 (`b5373e2`), then P725 (`92f6392`), with SoS swap
  merges in between (P680, P682 to P685). The swap merges were not picked.
- **No fix-ups.** No later commit on main names P724, P725 or P732.
- Each commit keeps its task's own subject line, plus a line naming the merge it was picked from.
- CHANGELOG and VERSION merged by themselves each time. P731 had already set the branch's numbers to main's.

**Left out, as asked:** every SoS swap commit (P674 to P691, P708) and everything else on main since `c925c0f`.

## What I adapted for the stock land

**P725's map patch (`trammel.mapops`).** P725 rebuilt the isle on main's SoS-based file, so I checked the merge
block by block (`notes\cc-P733-tools\mapops_verify_merge.py`, output `mapops-verify.txt`):
- P725 changed **164 blocks** (x 6624-6839, y 3928-4023). All are on the isle.
- All 164 sit on void in both maps:
  - their B fingerprints are the same on the branch (stock) and on main (SoS);
  - their lines on the branch equal P725's parent's.
- So git's merge is exactly right:
  - the 164 blocks carry P725's lines;
  - every other block, all 879 fingerprints and the header are the branch's.
  - Old Haven's way in, the Burrows' mouth and P276's farm removals stay, as on the stock land.
- The merged file is also **byte for byte** P725's own stock-base build (`notes\cc-P725-tools\trammel-stock-base.mapops`).
  P725 had built it from this branch for this release.

**`SOURCE.txt`.** One conflict, between the branch's P720 lines (stock-land words, P722) and main's P720 and P725
lines (SoS words). I kept the branch's P720 lines and added P725's line in stock-land words. P725's line says the
isle lines sit on void on both maps and that this file is P725's stock-base build. Script:
`notes\cc-P733-tools\resolve_source.py`.

**Nothing built on swap code.** After the picks, every code and test file the three picks touched is byte for byte
main's `92f6392`:
- `TutorialIsleAddons.cs`, `IsleAddons-SOURCE.txt` and `TutorialCorePlacement.cs`;
- `TutorialWake.cs`;
- the three test files.
Only `CHANGELOG.md` (the swap's sections), `SOURCE.txt` and `trammel.mapops` differ from main. P724's addons use the
isle's own spots, and the moongate frame takes its height from the ground under `TutorialWorld.Moongate`.

## Tests

- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P733`, `docker-build` lock, released): **EXIT=0**.
  - 2,749 shard tests: 2,744 passed, 5 skipped (the usual client-data facts), 0 failed.
  - P728's `PlayerMobile-tutorial-wake-move.patch` and the bandage patches report "Applied".
  - Output: `cc-P733-tools\green-gated-build.txt`.
  - The log's 110 "Item.Amount <= 0" lines are in P724's, P731's and P732's logs too.
  - Free memory was low at the start: 1.1 GB on Windows, 13.6 GB inside the Docker VM. So I ran the build detached;
    it finished in about 4 minutes.
- No map fact run of my own: the merged file is P725's stock-base build byte for byte. P725 ran the map facts on it
  (11 of 11, `cc-P725-tools\both-bases.txt`, `green-test-mapops.txt`).

## On the private shard (127.0.0.1:2596, never the shared Test Shard)

Setup:
- The shard ran `sl-modernuo:cc-P733` on a fresh copy of the bot world each time (`proof-shard.ps1`, its own
  container `sl-p733-proof`).
- The map was the branch's patch on **stock** client data, put on by the test shard's own `Build-MapOverlay.ps1`
  (`overlay.ps1`).
- The `test-shard` lock was taken and is now released, and the shard is down.

**Bot route: run 1, 0 failed checks, 85 passed** (`cc-P733-tools\runs\run1\playlog.txt`, 191 s).
- The route is P732's `isle.py` (the newest, also P725's), with Rook and the New Haven start back on stock New Haven
  (P731's `make_isle_bot.py`).
- A fresh character woke on cold sand at 6638,3993, saw "Move to get up.", and its first step got it up.
- It took every lesson:
  - the cloak chest (appears, opens, goes);
  - Wren's pitchfork, war mode and the pests, then the pet as the reward, with Pet Info;
  - Pip healed in the farmhouse;
  - the yard, the bank, the lodge and the vision.
  It walked the bot's own paths over P725's new map.
- It walked into P724's moongate frame, and the gate put it beside Rook at 3501,2572.
- The New Haven pick started on the plaza at 3503,2574.

**Real character in TazUO.**
- The client was the built TazUO (`D:\UO\tazuo-sl-build\client`). It started with no profiles except the branch
  launcher's `default.json`, and its map was built from the branch's patch on stock data, as the package does.
- TazUO made **Iron Tide** itself from the character list, with P731's test-only creation plugin. So the character's
  first login was TazUO's own.
- `IsleWalk733.py` played it with the client's own steps, clicks, drags and speech, and no teleport. It is made by
  `make_walk733.py` from P731's walk: P732's wake check in place of P731's, plus the fountain walk and the shots.
- **59 checks, 0 failed** (`runs\tazuo1\walk.log`, shots `shots\tazuo-*.jpg`):

| Step | Result |
|---|---|
| Lying | At 2, 6, 12 and 25 s: **drawn lying flat on the sand**, in the dark, beside Tamsin; no server window; "Move to get up." (`tazuo-lying-*.jpg`). |
| First move | A turn only (`API.Turn`). **Up at once**: the get-up drawn from the ground (`tazuo-getting-up.jpg`), on the same tile 6638,3993. Then the light, and the held windows. |
| Cloak chest | By the clothes rack; opened; the cloak taken and worn; the chest went. |
| Farm and pet | Pitchfork first, no pet before the pests; war mode opened the gate; rats and snakes killed; "the cabbage rows are clear"; then the pet window, a pup, "yours to keep". |
| Pet Info | From the pup's menu, its window opened; "all follow me" and "all guard me" counted. |
| Pip | In through the farmhouse door; Pip on his bench; a bandage really healed him; back out. |
| Fountain | Walked beside it, then past it and the lesson's signpost to the bank door (6762,3981), and back to the road. **It blocks no way in.** |
| Dock and frame | East from the road at 6812,3991 up the frame's steps onto its floor at 6830,3991 (z 4), and back west to 6812,3991,0. No stuck step either way. |

**Facing** (my own look at the shots). The Tester shots (`shots\tester-*.jpg`) were taken with P724's runner on the
stock land: the Admin moved Iron the Tester beside each spot, and `Clear733.py` closed the login windows.
- **Wreck** (`tester-wreck`, `tester-wake`): on the west tip's sand at the waterline, the bow up and out toward the
  sea, the hull on its side. It is west of the road's end and Tamsin, clear of the wake spot.
- **Lighthouse** (`tester-lighthouse`): upright on the sand of the point north of the road, its door toward the
  camera, the lamp lit. The road runs past it untouched.
- **Moongate frame** (`tester-frame`, `tazuo-dock-landing-frame`): stone steps all round, the wooden floor, four
  corner pillars with lanterns, the gate standing on the dais. The dock's planks and rope rails run straight onto it.
- **Fountain** (`tazuo-fountain`): the brass fountain upright on the bank's paved square, east of the walk to the
  bank's door.

**P725's shore and plants** (`tester-*-coast`, `tester-jungle`, `tester-dock-shore`, `tazuo-path-*`):
- Surf breaks along the west and south-west sand.
- The north and south coasts keep a small stepped edge, with surf. P725 notes that this edge stays on those sides.
  The isle's lines are identical to main's, so it looks the same there.
- The palms, banana trees, ferns and OSI's whole jungle trees are thick inland and thin toward the beaches.
- The road, the blue and gold tiles, Tamsin, the camp, the signposts, the farm and the farmhouse stay clear.

Nothing faced the wrong way. The Tester's shots were retaken once because the paperdoll and TazUO's own page had
covered the wreck (`Clear724.py` closes only the server's windows). They are not the release's windows.

## Deviations and decisions

- **Sparring dummy and market tents** (named in the prompt's summary): P724 did not place them. Its notes say the
  dummy needs ServUO's `DamageableItem`, and the isle has no market lesson for the tents. The "dock" is P724's moongate
  frame on P720's dock. So I checked what P724 did place: the wreck, lighthouse, frame and fountain.
- **Commits and a push.** The Golem's standing rule is no commits or pushes. This prompt asks for a pushed release
  branch, so, as P722 and P731 did, I committed the three picks on `release/isle-20261028` in its own worktree and
  pushed that branch only. My Golem branches have no commits from me; the only new files are these notes.
- **No player package, no shared Test Shard, no merge into main.**

## Files

- Code copy: nothing. The picks are commits on `release/isle-20261028` in its own worktree, pushed.
- Docs copy: this note, and `notes\cc-P733-tools\`:
  - `resolve_source.py`, `mapops_verify_merge.py` and `mapops-verify.txt`;
  - `gated-build.ps1`, `gated-build.log`, `green-gated-build.txt`;
  - `overlay.ps1`, `proof-shard.ps1`;
  - `isle.py` and `make_isle_bot.py`, `runs\run1\` (bot) and `runs-run1-console.txt`;
  - the TazUO tools: `tazuo-walk.ps1`, `ui.ps1`, `make_create_bin.py`, `make_walk733.py`, `IsleWalk733.py`, and
    `runs\tazuo1\` (walk log, runner log, plugin log, shard log);
  - the shot tools: `isle-shots.ps1`, `shots.json`, `Clear724.py`, `Clear733.py`, `shots-console.txt`;
  - `shots\` (`tazuo-*.jpg` from the walk, `tester-*.jpg` from the spots, `proof-log.txt`).
- Outside the repos: `D:\UO\golems\Iron\p733-proof\` holds the shard copy, the overlay, the clients, the plugin build
  and the raw shots; it can be deleted. `release-isle-20261028\` stays until the release is out.

P733 DONE
