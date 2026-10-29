# cc-P724: Tutorial Island dressed with the new addon downloads

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P724` (from main `d0dadde`). Not committed, nothing deployed.

## In plain words

- The Wakening Isle has four new pieces, all from the downloads and all made of art the game already has, so no
  client update is needed:
  - a shipwreck on the beach where you wake, with its bow out to sea;
  - a lighthouse on the point by the dock;
  - a stone frame with steps round the moongate at the end of the dock;
  - a brass fountain on the practice bank's square.
- You walk up the dock into the frame and through the gate as before. A real character in the game client did it,
  and the bot played the whole isle with nothing failing.
- The other downloads did not fit the isle, or the isle already has them. The reasons are below.
- Nothing for you to do. One note for P725 (the shore tiles), which has not run yet: it should keep its trees and
  shore changes clear of the wreck and the lighthouse (spots below).

## What was kept, and why

| Download (author) | Kept as | Where | Why |
|---|---|---|---|
| `celestial-shipwrecks` (Celestial) | `WakeningIsleShipwreckAddon`, the **West** variant, 20 pieces | centre 6627,3995,-3, on the west tip's waterline | Chase picked these for the wake beach. The wake beach is the west tip, so the sea is west, and the West variant's bow points west. |
| `new-lighthouse` (Milva) | `WakeningIsleLighthouseAddon`, 3 pieces | 6815,3984,0, on the grass-and-sand point north of the dock | A landmark by the departure. It stands 5 tiles north of the road to the dock. |
| `moongate-structure` (Carl Hamilton) | `WakeningIsleMoongateFrameAddon`, 88 pieces and 3 lanterns | centred on the gate, 6832,3991, its base at the landing's z -2 | It frames the dock's moongate, as asked. The gate stands on the frame's dais (+10), where the original leaves a blue tile for a moongate. |
| `lagatha-brass-fountains` (Lagatha) | `WakeningIsleBrassFountain` (art 0xA62B) | 6768,3984,0, on the bank's square | A fountain for the square. It stands east of the walk from the road to the bank door (x 6762). |

Code: `server/customizations/Tutorial/TutorialIsleAddons.cs`.
- **Seeding.** `TutorialCorePlacement.SeedOn` places them on the Fold and on each copy, and a copy's reset removes
  them. P728's top-up at world load added them to the copies seeded before: the private shard logged "Isle addons:
  placed 4, the gate stood on its frame" for the Fold and every copy.
- **The gate tile.** The seeding's own fit check now looks at the gate's tile only while the gate is missing. Once the
  gate is there, the frame's dais stands on that tile, and the check would refuse every later top-up.
- **Credits.** `server/customizations/Tutorial/IsleAddons-SOURCE.txt` gives the author, link, folder and terms for
  each one. No terms were stated for any, so they are treated as community work: credited, private repo and shard
  only, not reposted. The CHANGELOG line thanks all four authors.

## What was dropped, and why

- **`dock-addon` (+Qwerty).** The isle already has its dock (P707/P720/P722): 3 planks wide, with a stone landing,
  posts, rails and a sign. Those are map statics, and walking on them was fixed in P722. The addon's docks are
  15x16 platforms; any of them would cover or fight that dock.
- **`da-training-hall` (Dameon).** It is 96 x 45 tiles, more than a third of the isle's width, with no room for it.
- **`sparring-dummy` (ImaNewb).** It needs ServUO's `DamageableItem`, which ModernUO does not have. The isle's
  training yard already has a row of stock training dummies and an archery butte from the map.
- **`training-weapons` (Age of Britannia).** The isle's one weapon path is Wren's pitchfork (P721/P726). Loaner
  weapons would give a second path, and the prompt asks to keep one.
- **`lockpicking-chest-trainer` (FreeReign).** The isle has no thieving lesson or tip station to put it in.
- **`olorin-market-tents` (Olorin).** There is no market or vendor lesson on the isle. Each tent is 8 x 15. Worth
  keeping for New Haven's market later.
- **`region-banner` (Wilson).** It opens a window when you enter the isle. P728 cut first-login windows down at your
  request, and the isle's lesson window already names each place.
- **`welcome-gump`, `tutai`.** Ideas only, as the prompt says. The isle's own lesson window covers both.
- **`milva-pond-bridge`.** Not on disk (`D:\UO\third-party\code` has no such folder). The isle has a pond north of
  the training yard if it comes.
- **`celestial-cave-entrances` (Celestial).** No lesson needs a cave.

No new client art is needed, so there is nothing for a client-package follow-up.

## Facing (Chase 10-28 12:13)

I checked each piece from the default camera in the TazUO shots (`cc-P724-tools\shots\after-*.jpg`). No piece had to
be turned:
- **Shipwreck.** The West variant was chosen for the coast, not turned. Its bow and mast point out to sea from the
  west tip; the broken ribs lie toward the land. From the wake spot it shows on the beach to the upper left
  (`after-wake-view.jpg`).
- **Lighthouse.** The art has one facing only. The door faces south-east, onto the sand strip by the water, where a
  player walking the beach reaches it.
- **Moongate frame.** Steps on all four sides, so any side fits. The dock meets its west steps, the gate stands on the
  dais, and the lanterns hang on the corner pillars. The dock's own corner posts and rope rails stay (map statics) and
  show at the frame's west edge.
- **Fountain.** Round; either of its two art IDs looks the same.

## Tests

- **New facts** (`server/tests/Tutorial/TutorialIsleAddonsVerification.cs`):
  1. Seeding a copy places each addon once at its spot and stands the gate on the dais. Seeding again places nothing.
  2. No addon covers a lesson stop, sign, NPC, door, prop, the bank's floor or doorstep, or the road out along the
     dock. Only the frame covers the gate's own tiles, by design.
  3. A copy's reset removes them.
- **Red first** (`cc-P724-tools\mutate.py`, `probe.sh` on `sl-uo-builder:cc-P680`):
  - with the seeding call removed, facts 1 and 3 fail (`red-noseed.txt`);
  - with the lighthouse moved onto the road, fact 2 fails (`red-onroad.txt`).
  - Green: 3 of 3 (`green-probe-1.txt`).
- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P724`, `docker-build` lock, released): **EXIT=0**. 2,764
  tests: 2,758 passed, 6 skipped (the usual client-data facts), 0 failed (`green-gated-build.txt`).

## On the private shard (127.0.0.1:2596; never the shared Test Shard)

Setup:
- A fresh copy of the bot world, with P680's SoS-base map overlay (this branch's map; P724 changes no map).
- The `test-shard` lock was taken and is now released, and the shard is down.
- Before: `sl-modernuo:cc-P680`. After: `sl-modernuo:cc-P724`.

**Bot route: 0 failed checks** (`runs\run1\playlog.txt`, 191 s). It is P726's route (`isle.py`, main's New Haven
spots). A fresh character went from the beach through all the lessons. It walked the dock into the frame to
6831,3990, and the gate on the dais took it beside Rook at 3632,2584.

**Real character in TazUO** (`WalkFrame.py`, the client's own steps, `runs\walk-frame.log`):
- East along the road and dock from 6812,3991. It climbed the frame's steps (6829, z 0) onto the floor (6830, z 4).
- Back west to the road at 6812,3991. No stuck step either way.
- East again, onto 6831 (z 5) and into the gate. The gate sent him to 3632,2584 beside Rook.

**Shots.** Before and after, four spots, in `cc-P724-tools\shots\`:
- `before-*.jpg` / `after-*.jpg`, the Tester standing beside each piece;
- `after-wake-view.jpg`, from the wake spot;
- `walk-frame-f20.jpg` and `f22.jpg`, the character in the frame and leaving it.

The runner is P722's `isle-shots.ps1`, with these changes:
- the client's map is built on the SoS base (`-MapBase`), as the package builds it on main;
- the Tester's paperdoll-at-login and the TazUO page are turned off, and `Clear724.py` closes the login windows.
  One paperdoll from the Tester's saved layout still shows at the top left.

## Deviations and notes

- **P725 has not run.** It is still in the queue. The prompt says P724 runs after it, but the Golem handed P724 out
  now, and nothing here depends on P725's map. When P725 runs, it should keep its shore tiles and trees clear of:
  - the wreck: x 6625-6630, y 3993-3998;
  - the lighthouse: x 6814-6816, y 3984;
  - the frame: x 6829-6836, y 3988-3995.
  If P725 widens the wake beach, the wreck might move one or two tiles to sit on the new sand. That is one constant
  (`TutorialIsleAddons.WreckSpot`).
- **Planning renders** (offline, from the map files): `isle_topdown.py` (a top-down isle map), `plan_render.py` and
  `render_addons.py` (isometric, with the addons placed), `charmap.py` (tile kinds and heights).
- Outside the repos: `D:\UO\golems\Iron\p724-work\` holds the overlay, the shard copy, the client and all the shots.
  It can be deleted.

## Files

- Code copy:
  - `server/customizations/Tutorial/TutorialIsleAddons.cs` (new);
  - `server/customizations/Tutorial/IsleAddons-SOURCE.txt` (new, credits);
  - `server/customizations/Tutorial/TutorialCorePlacement.cs` (the seeding call and the gate-tile check);
  - `server/tests/Tutorial/TutorialIsleAddonsVerification.cs` (new);
  - `CHANGELOG.md` (`2026.10.28.10`, Added) and `VERSION`.
- Docs copy: this note and `notes\cc-P724-tools\`.

P724 DONE
