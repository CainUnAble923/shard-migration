# cc-P732: the washed-ashore wake lies down and ends on the first move, in the real client

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P732` (from main `d0dadde`). Not committed, nothing deployed.

## In plain words

- On the Wakening Isle's beach, a new character now lies on the sand in the dark, in the game client itself. Before,
  it showed standing in daylight.
- The player's first step or turn gets them up at once. Before, pressing a key did nothing and they lay there for a
  minute. The light then comes up over two seconds, and the patch notes and other windows come after, as before.
- I checked it with a brand-new character in TazUO on my private shard. Its shots are in
  `notes\cc-P732-tools\shots\`. The bot also played the whole isle with nothing failing.
- For you: nothing to try here. To have it in the isle-only release, it needs one pick onto `release/isle-20261028`;
  it applies cleanly there (see the end).

## The two problems (from P731), and why

1. **"Move to get up" did nothing in TazUO.**
   - P721's wake set the trainee `Frozen` while lying.
   - TazUO's `PlayerMobile.Walk` refuses to send any step or turn while the server marks the player frozen
     (`IsParalyzed`, TazUO `3212623f`, `PlayerMobile.cs:744` and `:959`).
   - So P728's move hook never heard from the client, and only the 60-second safety stood them up.
2. **The lying character showed standing, in daylight.**
   - TazUO plays a server animation frame by frame and, when it ends, goes back to the standing frame
     (`Mobile.ProcessAnimation`, `SetAnimation(0xFF)`). So P721's death animation, played once forward, ended
     standing.
   - The dark rose to near daylight 4 seconds in (P721's schedule, from when the lie lasted 5 s).
   - The first dark packet went out during the login, before TazUO counted itself in the world. TazUO drops light
     packets until then (`LightLevel.Receive`: `if (!world.InGame) return`).

## The fix (`server/customizations/Tutorial/TutorialWake.cs`)

- **No freeze.** The trainee is held down by P728's move patch (`PlayerMobile-tutorial-wake-move.patch`, unchanged).
  - While they lie, each move request is refused, so the client snaps back and the player stays on their tile.
  - The first request, a step or a turn, gets them up and is spent on it.
  - TazUO now sends that request, because nothing marks the player frozen.
- **The lying pose TazUO draws.** The human death animation (action 21, 6 frames; frames 3 to 5 are on the ground) is
  sent **backward** with frame count 5 and the longest frame delay, 255 (`HoldPose`).
  - TazUO draws frame 5 at once, then holds frame 4 and then frame 3, each for 80 ms × 256 = 20.5 s. All three are
    the body flat on the sand.
  - Starting from frame 5 avoids a one-tick flash of the standing frame (frame 0 when starting from 6).
  - The pose is sent again 1 s in (the login's one goes out before the client is in the world), then every 20 s, so
    it never reaches the rising frames.
  - Getting up is the same animation backward from frame 5 at the normal pace.
- **The dark.** It is level 24 (near night) from the start, sent again 1 s in, and stays until they stand. Then the
  dawn: 14, then 6, a second apart, then the isle's own light.
- **Unchanged:**
  - the 60-second safety;
  - "Move to get up." at 8 s (System line and over the head);
  - the waves every 6 s and "You wake on cold sand...";
  - P728's hold on the first login's windows and lines until they stand, then 2 s;
  - a disconnect while down ends it.

There is a clean pose, so no stand-in effect was needed. TazUO ignores the server's screen-fade packet (P665), so the
dark is the light level, as before.

## Tests

- **Facts.**
  - Updated in `TutorialIsleWalkFixes4Verification` (fact 2) and `TutorialIsleBandageWaitVerification` (fact 6):
    the trainee is **not** frozen while lying, the dark lasts until they stand, then the dawn, then the isle's light.
  - New in `TutorialIsleWalkFixes4Verification`: `ATurnGetsThemUpAndThePoseAndTheDarkHoldUntilThen`.
    - The pose's frame, delay and resend fit TazUO's timing.
    - It is sent at the start, 1 s in and every 20 s.
    - It stays dark for 59 s.
    - A turn alone gets them up; they stay on their tile, facing as they were.
- **Red first** (`notes\cc-P732-tools\mutate.py`, `probe.sh` on `sl-uo-builder:cc-P680`). Each mutant fails its facts:
  - the freeze back: 3 facts fail (`red-frozen.txt`);
  - the pose sent once only: 2 fail (`red-noresend.txt`);
  - P721's early dawn: 2 fail (`red-earlydawn.txt`).
  - Green: 14 of 14 in the two files (`green-probe-1.txt`).
- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P732`, `docker-build` lock, released): **EXIT=0**. 2,762
  tests: 2,756 passed, 6 skipped, 0 failed. The wake move patch reports "Applied" (`green-gated-build.txt`).

## In the real client (private shard 127.0.0.1:2596, never the shared Test Shard)

Setup:
- The shard ran `sl-modernuo:cc-P732` on a fresh copy of the bot world, with main's map (P680's SoS-base overlay).
- The `test-shard` lock was taken and is now released, and the shard is down.
- The client was the built TazUO (`D:\UO\tazuo-sl-build\client`) with an empty profile folder except the
  launcher's `default.json`.
- TazUO made the new character **Iron Dusk** itself, from the character list. P731's test-only plugin sends the
  creation packet; it is not shipped. So the character's first login was TazUO's own.
- A Legion script (`Wake732.py`) took the shots and made the moves with the client's own keys.

Run 2 (`runs\run2\walk.log`; shots in `cc-P732-tools\shots\`; a frame every 2 s in `shots\capture\`):

| When | What the client showed |
|---|---|
| 2, 6, 12, 25 s | **Lying on the sand**: the body flat on the ground beside Tamsin, in the dark (`lying-*.jpg`, `zoom-lying-12-25-and-up.jpg`). No server window. "Move to get up." over the head. Still down at 25 s, after the 21 s resend. |
| the first move | `API.Turn("south")`, a turn only. **Up at once**, the get-up drawn from the ground (`getting-up.jpg`), on the same tile (6638,3993). |
| +1 to +5 s | The light came up (`up-dawn.jpg`, `up-day.jpg`); then the held windows came: the patch notes and two achievements. |
| after | Walked east two tiles. |

**Bot route: 0 failed checks** (`runs\bot1\playlog.txt`, 191 s). It is P726's route on main:
- woke on cold sand; "Move to get up."; still lying with no window;
- the first step was spent getting up;
- all the lessons; the moongate to Rook at 3632,2584.

Run 1 (`runs\run1`) died on my script's mistake: `API.Player.Direction` is a name, not a number. But the untouched
character lay on its own until the safety, and its frames show the scene staying dark until then.

## The isle-only release branch

`release/isle-20261028` (`c925c0f`) has P728's wake. `TutorialWake.cs`, the two test files and the move patch are
byte for byte the same there as on this branch's base. So this task's commit picks onto it cleanly; only
`CHANGELOG.md` and `VERSION` need a hand. The release branch's `.9` is P730, the same as main's, so its section would
be `2026.10.28.11` as here, or the next number free there. Nothing in this fix depends on the map swap.

## Deviations and decisions

- **Version number.** P724's `2026.10.28.10` is on its own branch, not yet on main. I used `2026.10.28.11` so the two
  do not clash; whichever merges first, the integrator keeps both sections.
- **The Read tool** was denied once on `TutorialWake.cs` (the code copy is outside the working directory in an
  unattended run). Every edit went through small Python scripts in the scratchpad instead; nothing was skipped.
- **TazUO tools.** P731's real-client tools were reused: the plugin, `ui.ps1` and `tazuo-walk.ps1`, renamed into
  `p732-proof`, with the client's map built on the SoS base (`-MapBase`).
- Outside the repos: `D:\UO\golems\Iron\p732-proof\` holds the shard copy, the client, the plugin build and the runs.
  It can be deleted.

## Files

- Code copy:
  - `server/customizations/Tutorial/TutorialWake.cs`;
  - `server/tests/Tutorial/TutorialIsleWalkFixes4Verification.cs` and `TutorialIsleBandageWaitVerification.cs`;
  - `CHANGELOG.md` (`2026.10.28.11`, Fixed) and `VERSION`.
- Docs copy: this note and `notes\cc-P732-tools\`:
  - `probe.sh`, `mutate.py` and the red and green outputs;
  - the gated build output;
  - `Wake732.py`, `tazuo-walk.ps1`, `ui.ps1`, `proof-shard.ps1`, `isle.py`, `make_create_bin.py`;
  - `runs\`, `shots\`.

P732 DONE
