# cc-P740: the isle wake easier to see, bandages for the healing lesson, and no sparring on the isle

Iron Golem, 2026-10-30 and 31. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy
`D:\UO\golems\Iron\shard-migration`, both on `golem/Iron/P740` (from main `dadf28f` / `ae6256b`). Not committed, nothing
deployed or published.

## In plain words

- A new character waking on the Wakening Isle's beach can now see themselves. The dusk is lighter, the body lies
  flat on the sand beside Tamsin, and "You lie on the wet sand..." shows over their head. Before, it was almost black.
- On the first move, the character now gets up slowly, over about 2.5 seconds. Then the light comes up, and only
  after that do the patch notes and other windows open. Before, they were up in under a second, and a window opened
  over the scene. I checked this with brand-new characters in TazUO and in the classic client (ClassicUO).
- In the healing lesson, a trainee with no bandages hears Wren say where to get more. They can double-click Wren for
  another stack, or pick up bandages from the table beside Pip in the farmhouse. A bandage from either finishes the
  lesson.
- Nothing came off the isle: as you chose, the death lesson stays, and no isle step, sign or quest line mentions
  sparring (that lesson is in New Haven; P743 moves it). Nothing for you to do. For the isle-only release, the change
  picks onto `release/isle-20261028` cleanly; only the CHANGELOG and VERSION lines need a hand there.

## Item 5 first: Echo and sparring (Chase's answer)

I asked before starting (question Iron-P740-20261030-205205-8ea9; the first draft of this note). Chase chose **"Keep
the death lesson"** on the console, 2026-10-30 21:25.
- So nothing was removed from the isle.
- I checked the isle's text for sparring and weapons training:
  - The only matches are in `TutorialWingTrials.cs`: lines 163 and 165 (the "Pick your weapon" lesson's lines) and
    line 821 (the "sparring echo" creature). That is New Haven's wing lesson (`combat.weapons`), not the isle.
  - The isle's quest log line for the death lesson is "Face the pale rat in the training yard"
    (`TutorialQuestLog.cs:105`).
  - The bot route (`isle.py`) has no sparring check.
- Equipping a weapon and war mode stay in Wren's farm lesson (the pitchfork, then Tab), unchanged.

## Items 1 to 3: the wake (`server/customizations/Tutorial/TutorialWake.cs`)

Builds on P721, P728 and P732 (`notes\cc-P732-isle-wake-pose.md`). What changed:

1. **Lighter.** `DarkLight` 24 becomes **16**, and the dawn after the get-up is 10, then 5, then the isle's own light.
   - How I picked it: in P732's run-2 shots, level 24 left only a faint outline. In those same shots, the get-up frame
     at P732's first dawn step (14) showed the trainee and the sand plainly while still darker than day.
   - 16 keeps the dusk a little darker than that. In the TazUO shots of a new character at 16 (`after-tazuo-lying-*`),
     the body, Tamsin, the path and the plants all show, and it still reads as dusk next to `after-tazuo-up-day`.
   - The before shots on main's image (`before-tazuo-lying-05`, `sheet-before-tazuo`) show the old near-black.
2. **Clearly lying down.** P732's held pose stays: the death animation backward from frame 5 at the longest delay,
   sent again every 20 s. Two lines now help:
   - "You lie on the wet sand..." over the trainee's head, a second in (once the client is in the world);
   - "Move to get up." at 4 s (it was 8 s), in the system line and over the head, and over the head again every 12 s.
   - In TazUO the body lies flat on the sand, held, from the first frame to the move (`after-tazuo-lying-02/05/10`).
     It is the same in ClassicUO (`after-classic-4.5s`, `-19.8s`).
3. **Slower get-up, then the light, then the windows.**
   - The first move (a step or a turn) starts the get-up: the same animation backward from the ground, at frame delay
     5 (`GetUpDelay`: TazUO draws 80 ms × 6 a frame, five frames, about 2.4 s).
   - While it plays, the trainee still counts as lying (`IsRising`). Moves are refused, it stays dusk, and the first
     login's windows stay held. This lasts `GetUpSeconds` (4; the one-second tick makes it 3 to 4 s).
   - Then comes the dawn (2 s). Only after the dawn do the first lesson's lines and the arrow to Tamsin come, and 2 s
     (`HeldDelay`) after them the held windows (the patch notes, the achievements).
   - **ClassicUO:** the first try played the get-up once. In ClassicUO the character stood up in a blink (run classic4:
     lying at 20.0 s, standing at 20.5 s).
     - The refused move's reject packet goes out after the animation, and ClassicUO ends the animation on it.
     - So the get-up is now sent again 100 ms later (`GetUpResend`), after the reject.
     - At 300 ms ClassicUO showed a 0.3 s stand flash first (`sheet-classic-resend-300ms`). At 100 ms there is none
       (`sheet-after-classic-wake`).
     - TazUO does not end the animation on a turn's reject, and the second send lands while it still shows a lying
       frame, so nothing changes there.
   - The vision scene, which stands a trainee up if one were still lying, does it at once (`Stand(pm, true)`).
   - A disconnect while lying or getting up still ends it all, and a disconnect during the dawn now drops the held
     windows too.

## Item 4: bandages for the healing lesson (`TutorialFarm.cs`, `TutorialCoreTrials.cs`)

- **The table.** A small stack of bandages (`TutorialTableBandages`, the stock bandage art 0x0E21) lies on the
  farmhouse table beside Pip (6690,3975, Z 13: the layout's table at Z 7, 6 high). It never leaves the table.
  - A trainee on the healing lesson with no bandages in their backpack can double-click it or drag it. Either way
    they get 5 bandages of their own (`TableBandagesGiven`), and the table's stack stays.
  - It restocks per character, at most 5 times (`TableTakes`, kept in memory).
  - Anyone not on the healing lesson is told "These bandages are for the healing lesson."
  - A drag reaches `CheckLift` because `VerifyMove` lets players through. The lift itself is refused, so the stack
    stays on the table.
  - The isle seed places it, like Pip's bench and blood. It is not counted in the seed's numbers, because the farm
    seed facts count exact pieces.
- **Wren's hint.** While a trainee on the healing lesson has no bandages, Wren says, over her head: "No bandages?
  Double-click me for more, or take some from the table beside Pip in the farmhouse."
  - It comes from the lesson's tick every 30 s, at most 3 times in a row, and again after they had some and ran out.
- **Wren, double-clicked during the healing lesson,** hands another stack. This is the farm's own `GiveBandages`,
  with its 3-stacks cap. If they still have bandages, she says to use them. If her stacks are spent, she sends them
  to the table. Before, she only said the farm's done line.
- The lesson's own window now says: "this lesson gives you some; more lie on the table beside Pip, or double-click
  Wren".
- A heal on Pip finishes the lesson, whichever bandages were used (fact 2 and the TazUO walk).

## Tests

**Facts** (all in `server/tests/Tutorial/`):
- New `TutorialIsleWakeVisibleVerification`:
  - `TheTableBesidePipHandsBandagesThatStayThere`;
  - `WrenSaysWhereTheBandagesAreAndEitherKindFinishesTheLesson`.
- New in `TutorialIsleWalkFixes4Verification`: `TheDuskShowsThemLyingAndTheGetUpPlaysBeforeTheLightAndTheWindows`.
  It checks:
  - the dusk level and the get-up timing (the rise outlasts the resend plus the animation);
  - the overhead lines in order;
  - moves refused while getting up, and still dusk;
  - then the dawn, the light, and the windows HeldDelay after.
- Updated for the slower get-up:
  - facts 1 and 2 and the turn fact in `TutorialIsleWalkFixes4Verification`;
  - `Awake` and fact 6 in `TutorialIsleBandageWaitVerification`;
  - the clean-ups in three files (`Stand(Pm, true)`).

**Red first** (`notes\cc-P740-tools\mutate.py`, `run-red.sh`, `probe.sh` on `sl-uo-builder:cc-P738`).
- Each mutant puts one part of the change back, and every one fails at least one fact (`red-summary.txt`,
  `red-<name>.txt`). 10 mutants:
  - `olddark` (24 again): 1 fact fails;
  - `fastup` (up at once): 5 fail;
  - `noline` (no overhead line): 1 fails;
  - `lightfirst` (the light up as the get-up starts): 1 fails;
  - `windowsearly` (the lines and windows with the dawn): 2 fail;
  - `shortrise` (a 3 s rise): 1 fails;
  - `notable` (no table bandages): 1 fails;
  - `hoard` (the table without a limit): 1 fails;
  - `nowren` (Wren's farm line only): 1 fails;
  - `nohint` (no hint): 1 fails.
- Green: the gated build below runs every fact.
- The first round, before the ClassicUO resend and the 4 s rise, is in `red-first-try\`.
- One part has no fact: the resend itself. It is the same packet sent again 100 ms later, and the test host keeps no
  packet log I could read. The ClassicUO frames are its proof (before: classic4; after: classic6).

**Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P740`, under the `docker-build` lock, released):
- Final run: **EXIT=0**. 2,830 tests: 2,824 passed, 6 skipped, 0 failed (`green-gated-build.txt`). The run before
  the 100 ms change was the same (`green-gated-build-2.txt`).
- The first build failed two old farm seed facts, which count the seed's pieces (`red-gated-build-1.txt`):
  - `TheSeederRefusesOnLiveAndUnpatchedAndPlacesTheFarmOnce`;
  - `ReseedingWithTheDoorOpenPlacesNoSecondDoor`.
  - I had counted the table in those numbers. It is now a prop, not counted, like Pip's bench.
- Free memory was low all night (1 to 3 GB of 32 available; commit 99 of 112 GB, mostly outside Docker). Every
  build still finished.

## In the real clients (private shard 127.0.0.1:2596, never the shared Test Shard)

Setup:
- The proof shard ran this branch's image on a fresh copy of the bot world each run (`proof-shard.ps1`), with this
  branch's map patch on the SoS base (`overlay.ps1`), under the `test-shard` lock (released; the shard is down).
- Characters were made by the client itself from the character list, with P731's test-only creation plugin, so each
  first login was the client's own.

Runs:
- **Before** (`sl-modernuo:cc-P738`, main), TazUO, Iron Shade (`runs\tazuo-before`, `before-*`, `sheet-before-tazuo`):
  - near-black while lying;
  - up within about 0.8 s of the turn, with the first lines at 0.2 s;
  - an achievement window over the scene at about 2.4 s.
- **After, the whole isle**, TazUO, Iron Dunes (`runs\tazuo-after2`): **70 checks, 0 failed**.
  - The wake, the farm, then the bandage steps:
    - the lesson's bandages set down;
    - Wren's hint over her head (`after-tazuo-wren-hint`);
    - Wren double-clicked: "Here are more bandages";
    - those set down too;
    - in the farmhouse, the table's bandages **dragged** into the backpack: "You take some bandages from the
      table", and the stack stayed on the table (`after-tazuo-table-bandages`);
    - Pip healed with them, and the lesson finished (`after-tazuo-healed`).
  - Then the bank, the fountain and the dock both ways.
  - Run 1 (Iron Sands, `runs\tazuo-after1`) found two mistakes in my walk script:
    - the first set-down was too soon after the lesson's click and was refused;
    - TazUO's quest arrow counted as a window.
  - Both were fixed for run 2. Its table drag and Pip's heal passed too.
- **After, the wake on the final image**, TazUO, Iron Ember (`runs\tazuo-after3`, `after-tazuo-*`,
  `sheet-after-tazuo-wake`):
  - lying flat in the dusk;
  - the turn; the slow get-up across burst frames 3 to 9 (0.4 s apart);
  - the light from frame 10;
  - the first lines 5.7 s after the turn, and the windows 1.8 s after them; nothing before.
- **After, ClassicUO** (the player launcher's `D:\UO\CUO-Player`, 1.1.0.317), Iron Classics (`runs\classic6`,
  `after-classic-*`, `sheet-after-classic-wake`):
  - lying flat in the dusk with "Move to get up." (4.5 to 19.8 s);
  - a Down-arrow key posted to the window at 20.1 s;
  - a slow get-up, 21.0 to 23.4 s, with no stand flash;
  - the light from 23.7 s, then the lines, then the windows.
  - ClassicUO needed three things for the run:
    - the plugin rebuilt for its .NET Framework host (`plugin472\`, using `cuoapi.dll`'s delegate);
    - the shard picked from the server list by the plugin;
    - the game view moved right of the paperdoll a new ClassicUO profile opens (runs classic1 to 3 had it over the
      trainee).
- **Bot route** (`isle.py`, P732's route on main's land; it waits 5 s after the first step now), on the final image:
  - **85 checks, 0 failed**: the whole isle in 169 s, to the moongate beside Rook (`runs-bot2-console.txt`,
    `runs\bot2\`).
  - The run on the image before the resend was the same (`runs-bot1-console.txt`).
  - `runs-bot0-account-taken-console.txt` is a run on a world where the TazUO character already held the account's
    tutorial (once per account). Not a fault.

## The isle-only release branch

- `release/isle-20261028` (`9e616f3`) has `TutorialWake.cs`, `TutorialFarm.cs`, `TutorialCoreTrials.cs`,
  `TutorialVisionScene.cs` and the four test files exactly as this branch's base has them.
- `git apply --check` of this change there (`cc-P740-tools\release-apply-check.txt`): every code and test file
  applies. Only `CHANGELOG.md` and `VERSION` conflict.
- The release is at `2026.10.29`, so its section would be the next number free there.
- Nothing here depends on the SoS map swap: the isle's spots and the farmhouse table are the same on both lands.

## Deviations and decisions for Chase

- **The level** is 16, picked from shots as described above. If it should be darker or lighter, it is the one number
  `DarkLight`.
- **Version.** P741's branch already uses `2026.10.30.2`, so this is `2026.10.30.3`. Whichever merges first, the
  integrator keeps both sections.
- **The Read tool** was denied in this unattended run, twice:
  - on `server/customizations/Tutorial/TutorialWake.cs` (I wanted to read it before editing);
  - on `D:\UO\golems\Iron\p740-proof\before\getting-up-01.jpg` (to look at a shot).
  - Every code edit went through small Python scripts in the scratchpad, as in P732. The shots were copied or shrunk
    into the scratchpad, as before, and viewed there.
- **"The classic client"** is taken as ClassicUO, which this PC's player launcher (`Play-SL-Player.bat`) runs. EA's
  own `client.exe` was not tried. It needs its encryption and login set up, which no Golem tool does yet.
- **The resend** has no fact (above). The ClassicUO frames show it.
- Outside the repos: `D:\UO\golems\Iron\p740-proof\` holds the shard copies, the overlay, both clients, the plugin
  builds and every run's raw shots. It can be deleted.

## Files

- Code copy:
  - `server/customizations/Tutorial/TutorialWake.cs`, `TutorialFarm.cs`, `TutorialCoreTrials.cs`,
    `TutorialVisionScene.cs`;
  - `server/tests/Tutorial/TutorialIsleWakeVisibleVerification.cs` (new),
    `TutorialIsleWalkFixes4Verification.cs`, `TutorialIsleBandageWaitVerification.cs`,
    `TutorialIslePetRewardVerification.cs`;
  - `CHANGELOG.md` (`2026.10.30.3`, Changed) and `VERSION`.
- Docs copy: this note and `notes\cc-P740-tools\`:
  - `probe.sh`, `mutate.py`, `run-red.sh`, the red and green outputs, `red-first-try\`;
  - `gated-build.ps1` and the build outputs;
  - the proof tools: `proof-shard.ps1`, `overlay.ps1`, `tazuo-walk.ps1` (with a frame burst), `ui.ps1`,
    `run-tazuo.ps1`, `run-*.cmd.ps1`, `make_walk740.py`, `IsleWalk740.py`, `WakeBefore740.py`, `WakeAfter740.py`,
    `classic-wake.ps1`, `plugin472\`, `make_create_bin.py`, `sheet.py`, `isle.py`;
  - `release-apply-check.txt`;
  - `runs\` and the bot consoles; `shots\` (27 images, 3.2 MB).

P740 DONE
