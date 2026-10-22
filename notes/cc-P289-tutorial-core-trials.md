# cc-P289: the tutorial's core trials, placed on a test world and played end to end

## In plain words

- The nine core tutorial lessons now work for real. On a private copy of the test world, a brand-new character walked
  the marks, put on the practice cloak, opened the practice bag, spoke the phrase, died to the echo and was raised,
  banked the token, took the tutorial gate, met Elara and watched the loop vision. Then it graduated at Rook. Skip,
  remedial training and "Reset this lesson" worked too.
- The play-through found three server bugs, and the fixes are written:
  - a ghost double-clicking the tutorial healer got her paperdoll instead of the resurrection offer;
  - an arrow left over from a logout later wiped the arrow to the next lesson;
  - staff accounts were greeted into the tutorial at login.
- **Not finished:** the last build-and-test round was stopped because the PC ran low on memory, so the fixes are not
  in the code tree yet. They wait in a patch beside these notes, with the new tests that catch the bugs.
- For you: say "Continue" on the Golem card, and a new session runs the last round (about 40 minutes): tests, fixes,
  then a final clean play-through. Nothing is placed on live; the tutorial stays off there.

2026-10-21, the Iron Golem (Opus 5.5), branch `golem/Iron/P289` of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Iron\cc-P289-tutorial-core-trials-playable.md`. Not committed. Nothing deployed, and
nothing was run against live or the shared test shard (2594).

## Where it stands

| Step | State |
|---|---|
| Valorite's draft (code 0abfa6a, docs 7278976) | Brought in as uncommitted changes. The Golem rules forbid a real merge here, so: `git diff HEAD origin/golem/Valorite/P289 \| git apply --index` (code); its notes file is folded into this one and removed |
| Build gate on the draft | **Green, first try:** `Built sl-modernuo:cc-P289 with patches applied and 2096 shard test(s) passing.` 2,100 tests, 4 skipped, 0 failed (16:19-16:23, image 7319cb9d90ef). Valorite's 27 failures came from its own scratch route, not the code |
| Part 1, the nine trials | Built (Valorite), and **played for real**: all nine pass (play logs below) |
| Part 2, the seeder | **Played for real:** dry run, seed, seed again (0 placed), dry run (0 to place) |
| Part 3, the wings | Coming-soon page in code and in fakes. The real-play check is in the driver but not run yet (it was added after the last run) |
| Part 4, the play-through's fixes | 3 bugs found; tests written (in the tree); fixes written (`notes\cc-P289-tools\fixes.patch`, **not applied**). Loop placeholder: listed, not settled (For Chase 7) |
| Red run of the new tests | **Not run.** The background lock wait was killed for low memory before it got the lock (1.6 GB free at 17:04); nothing was built |
| Final gate and clean play-through | **Not run** (Continuation) |

## The play-through

**The shard.** A private, loopback-only scratch shard, not the shared test shard: container `sl-modernuo-p289`,
image `sl-modernuo:cc-P289`, `127.0.0.1:2596`. World and Configuration are scratch copies of the bot shard's (210,802
items, 35,133 mobiles: New Haven as it stands). The Configuration was changed to listen on 2596 and to put the map
overlay first. The client data is `D:\UO\UltimaOnlineVanilla` (7.0.117.0), read only. The overlay is P276's patch
applied by `docker\uo\Build-MapOverlay.ps1 -UoData D:\UO\UltimaOnlineVanilla` into scratch ("1597 pieces added, 7
removed"), so the farm's two trees are gone and `TutorialFarm.MapPatched` passes. `golem-accounts.json` is in the world
folder: 18 Golem accounts were made at load. The test-shard lock was held while it ran. The compose file:

```
name: sl-uo-p289
services:
  modernuo-p289:
    image: sl-modernuo:cc-P289
    container_name: sl-modernuo-p289
    restart: "no"
    stop_grace_period: 60s
    ports: ["127.0.0.1:2596:2596"]
    volumes:
      - D:/UO/golems/Iron/ShatteredLegacy/server/customizations:/modernuo-projects:ro
      - ./Configuration:/modernuo/Configuration
      - ./world:/var/lib/uo/modernuo
      - D:/UO/UltimaOnlineVanilla:/var/lib/uo/client-data/classic-client:ro
      - ./overlay:/var/lib/uo/client-data/sl-map-overlay:ro
    environment: {TZ: America/Chicago, SL_SHARD_ROLE: test}
    stdin_open: true
    tty: true
    security_opt: [seccomp:unconfined]
```

**The player.** `notes\cc-P289-tools\playthrough.py` drives the play-test bot's own client (`tools\playtest-bot\uobot`:
the packets a 7.0.117 client sends). Iron's Admin seeds; Iron's Player account makes a fresh character, "Iron Trainee",
with normal character creation (0xF8). Every step is a player action the server checks; no staff command completes
anything. The one staff step is `[Tutorial reset` before the skip run, so the same account can start again. Walking
uses a breadth-first path over the patched map files (P188's walk model), replanned around refused steps and server
items; doors are opened by double-clicking. Passwords come from `Get-GolemTestAccount.ps1` and never reach a file.
No screenshots: this PC has no capture route for the bot, so the evidence is the System lines and state changes.

**Results** (logs in `notes\cc-P289-tools\`):

- `playlog-seed.txt` (run 1): the dry run would place 9 station markers, 4 NPCs and the echo, 1 gate, 1 gold mark and
  the farm (1 addon, 1 door, 1 Farmhand, 2 spawners). The seed placed exactly that. The second seed placed 0 of each
  ("already there 5"); the last dry run would place 0.
- `playlog-core.txt` (run 10): League, the loop vision (five lines over about 8 s, then "Core finished"), back to Rook,
  Graduate ("Graduated. New Haven survived you."), "Open that box here in town", the dog and the pup-color pick. The
  first seven trials passed in runs 3 to 9 on the same character (logs in the session scratch, not kept): the movement
  marks, cloak, bag, phrase (a wrong line first did nothing), death, bank (said "bank", token into the box) and travel.
- `playlog-skip-remedial.txt` (run 11), after `[Tutorial reset`: the relog enters the core again. Skip asks twice;
  "No, teach me" at the second leaves it InCore; yes at both skips ("Skipped. Bold."). Rook offers Remedial ("I saved
  your seat"). Remedial walks the trials again: movement, paperdoll, backpack; chat after pressing "Reset this lesson",
  which reopens it undone; death; bank; travel; League. The run stopped at the vision on a driver fault, fixed since:
  the walker could open a door only once per run, so it was shut in the Registrar's house. Its two other FAILs: the
  ghost double-click (bug 1, below), and the skip achievement check, which read only chat lines while the title is in
  the unlock gump (the driver now reads both).

**What the play-through found and fixed** (the patch; tests in the tree):

1. **A ghost cannot ask the healer** (`TutorialHealer`). Pinned's `Mobile.Use` sends a dead player's double-click to
   `OnDoubleClickDead`, which opens the paperdoll. Valorite's override is `OnDoubleClick`, which never runs for a
   ghost. Its fact called `healer.OnDoubleClick` directly, so it passed. The stock offer, `BaseHealer.OnMovement`, needs
   a step into range; `OnMovement` is only called from `Mobile.Move` (pinned `Mobile.cs:4438`), and the lesson teleports
   the ghost beside Sera. So the hint's "double-click the healer" did nothing; only walking off and back worked (the
   driver does that as a fallback, logged as a FAIL). Fix: override `OnDoubleClickDead`. Test: the hooks fact now goes
   through `p.Pm.Use(healer)` and asserts the offer was observed.
2. **An arrow left behind by a logout** (`GuildDirectionArrow`, shared with the guild and League arrows). Pinned's
   logout calls `ClearQuestArrow`, which drops the reference without stopping the arrow
   (`PlayerMobile.cs:1585`). The orphan ticks for up to 10 minutes. On arrival it said "You have found ..." and its
   stop sent 0xBA off, wiping the client's arrow to the next lesson: three of them did, after the earlier runs'
   relogs. Fix: an arrow that is no longer the player's ends its timer silently. Test:
   `AnArrowLeftBehindByALogoutNeverFindsItsSpotLater`.
3. **Staff were entered** (`ClusterFTutorial.TryEnter`). Iron's Admin got the recruiter's greeting and an arrow at its
   first login. Fix: GameMaster and above, by character or account, are never entered. Test:
   `StaffAreNeverEnteredIntoTheTutorial`.
4. **Text:** the death lesson said "Your corpse stays by the echo". A Young character's things come back to its
   backpack on resurrection (pinned's Young death notice says so), so the hint and the echo's page now say that.

**Seen, not changed** (other systems; For Chase 8 and 9):

- A new character's first login brings three Common Boxes, three achievement pages, the Welcome page and the patch
  notes, all at once with the tutorial's two lines. The greeting is easy to miss.
- Shard-wide, System lines are sent as `SendMessage` with the text "System: ..." from the name "System", so the bot's
  log reads "System: System: ...". Whether TazUO's journal shows the prefix twice is unverified (no client here).
- Twice, New Haven townsfolk called the guards on something near the plaza and the guards killed it (corpses of body
  0x58F and 0xFC at 3504,2573). The player was not involved. The driver now logs the mobiles around when that happens.

## Tests

- **Gate 1 (Valorite's draft):** green, above.
- **New and changed facts** (`server\tests\Misc\TutorialVerification.cs`, in the tree now): the hooks fact goes through
  `Use` for the ghost; `StaffAreNeverEnteredIntoTheTutorial`; `AnArrowLeftBehindByALogoutNeverFindsItsSpotLater`.
  **Not yet seen red or green.** Without the patch all three should fail: the offer is never observed; the Admin's
  state becomes InCore; the orphan stops itself on arrival.
- Valorite's 26 focused facts were seen red then green on its native route (its notes, folded below). On the gate they
  were green; they were not broken again here.

## For Chase

The prompt's defaults, kept:

1. Recruiter: Rook Hallowell at 3500,2572,14.
2. Voice: the "System:" lines.
3. Order: the core first, then the wings.
4. Graduation box: Explorer's tier 1.
5. Live: `tutorial.enabled` stays off on live. The code now refuses it unless `testCenter.enable` is set, and every
   seeder refuses anywhere but a test world.
6. Client: server-driven hints only, no TazUO patch.

Open:

7. **The loop placeholder (P80 decision 7) is not settled.** P282 (F-12 numbers) is Valorite's open prompt, numbers
   only with no code. F-12's decisions count a new character as loop 0 ("loop 0 about 3 h",
   `notes/f12-decisions-2026-10-05.md:27`; "50 at creation, 100 at loop 1", `docs/feature-queue.md:1227`). That matches
   `EvoPet.OwnerLoopsSource` (0) and makes `ClusterFLootBoxes.LoopProvider`'s default of 1 the odd one out. The vision
   changes neither. Left as it is for F-12.
8. **The first-login flood:** should the tutorial's greeting come after the boxes and pages, or should those wait for
   the tutorial? (Other systems; not changed.)
9. **"System: System:" in the journal**, if TazUO shows the name: worth a look in a client.
10. **Young death:** the lesson now says a Young character's things come back to the backpack. A remedial player past
    Young keeps a real corpse by the echo; the line covers only the Young case.

Deviations:

- The draft was brought in with `git apply --index`, not merged (the Golem's standing rules forbid merging).
- A private shard on 2596 instead of the shared test shard. `Start-TestShard.ps1` mounts the main checkout's folders,
  which this Golem may not touch. The test-shard lock was still taken while it ran.
- Unattended permission denials, not retried another way: the Read tool on
  `D:\UO\golems\Iron\ShatteredLegacy\docker\uo\Start-TestShard.ps1` (read with `cat` after taking the test-shard lock,
  as the guard hook asked); one of two identical Reads of `server\tests\Misc\TutorialVerification.cs` (offset 360); the
  other went through. A Bash read of `docker\uo\build.sh` was refused by the guard hook while another Golem held the
  docker-build lock, so no builder-image probe was tried.
- **The red run was killed** by Claude Code for low memory while it waited for the docker-build lock (Bronze held it
  from 16:47 for up to 90 min). It had not started. As the harness asked, I did not restart it.

## How to play it

On a test world (never live) with P276's map patch, `testCenter.enable` and `tutorial.enabled` set:

1. As an Administrator: `[ClusterFSeedTutorial dryrun`, then `[ClusterFSeedTutorial`. A second run places nothing.
2. Make a new character (any account that has never done the tutorial). It arrives at 3503,2574,14 and is told to find
   the recruiter; the arrow points to Rook at 3500,2572.
3. Double-click Rook and press "Core: Walking, running and the camera". Each lesson's page has "Next lesson" when it
   is done; "Hint and arrow" repeats the hint, and "Reset this lesson" starts it again.
   1. Walk onto the blue mark (3499,2571), then the gold mark (3501,2571).
   2. Drag the practice cloak from your backpack onto your paperdoll.
   3. Open your backpack and double-click the blue practice bag.
   4. Say `I am ready to learn`.
   5. Walk to the farm gate. Double-click the pale echo (3402,2617), press Ready, and die. As a ghost, double-click
      Sera (3402,2613; after the fix) and press Resurrect.
   6. Walk to the banker (3492,2577), say `bank`, and drag the practice token into the bank box.
   7. Walk back to the farm gate and double-click the blue moongate (3402,2615); it puts you on the plaza.
   8. Walk to Elara Voss (3459,2601, inside the Registrar's house; the door is on the north side) and double-click her.
   9. Walk to the vision marker (3402,2619), double-click it and stay within 4 tiles until "Core finished".
4. Back at Rook: Graduate. A box comes (open it in town) and the pet pick.
5. Skip: on a fresh record, Rook's "Skip the tutorial", yes twice ("No, teach me" at either step changes nothing).
   Rook then offers Remedial training, the same nine lessons and a second achievement.

The bot does the same with:

```
python -P notes\cc-P289-tools\playthrough.py --port 2596 --out <folder> --map <overlay folder> --tiledata D:\UO\UltimaOnlineVanilla --parts seed,core,skip
```

## Continuation

Exact steps for the next session, on this branch, in order:

1. **Red:** take the docker-build lock (`Use-GolemLock.ps1 -Take docker-build -Minutes 30 -Wait`), drop the Docker VM's
   page cache (memory: docker-vm-page-cache-low-memory), check at least 4 GB is free, and run
   `bash docker/uo/build.sh -t sl-modernuo:cc-P289 --tests-only` detached. Expect exactly 3 failures, the three facts
   above.
2. **Fix:** `git apply D:\UO\golems\Iron\shard-migration\notes\cc-P289-tools\fixes.patch` in the code copy (it applies
   cleanly: checked 17:04).
3. **Green:** `bash docker/uo/build.sh -t sl-modernuo:cc-P289` (the full gate, the image too). Release the lock.
4. **The clean run:** take the test-shard lock. Rebuild the scratch world from `D:\UO\bot-shard\world\Saves` and
   `D:\UO\bot-shard\Configuration`, edited as above, with `clusterf.testShard.allowAccountWipe` "True" so the Golem
   accounts are made (the Saves `AccountWipe` folder removed, so nothing is wiped). Rebuild the overlay, start the
   compose file above, and run the driver with `--parts seed,core,skip` and a new `--name`. Keep its play log here
   (`playlog-final.txt`). Expect 0 FAIL except "first login" checks on a reused character. Then compose down and
   release the lock.
5. Finish the notes: the red and green tables, the final run, a CHANGELOG line (the code repo's CHANGELOG has
   Valorite's 2026.10.21.21 Staff line; add a Fixed line for the three bugs, renumbering if main has moved), and run
   `python tools/progress.py`.

Mid-flight: nothing running. No lock held by Iron; the private shard is down (`sl-uo-p289` removed). The scratch copies
are in the session scratchpad and are not needed (step 4 rebuilds them).

## Valorite's draft notes, folded in

The Codex Golem Valorite's handoff (docs 7278976, `notes\cc-P289-tutorial-core-trials-playable.md`, removed here so only
one P289 notes file carries the last line), in short:

- It built the action-evidence model (`TutorialTrialProgress`), the nine handlers (`TutorialCoreTrials`), and the
  placement (`TutorialCorePlacement`: markers, Rook, the echo, Sera, the banker, Elara and the gate if missing; the
  P276 farm; a `CanFit` preflight; refusal on live and on an unpatched map). It also made the wings' coming-soon page,
  the character check on account actions, the live gate on `testCenter.enable`, and practice supplies that delete
  themselves.
- Its facts, seen red then green on a native route: the 12 cases in `server\tests\Tutorial\TutorialTrialProgressVerification.cs`,
  the reset, the hooks and the seeder facts in `TutorialVerification.cs`, and 5 of P276's farm facts: 26 in all.
- It could not run Docker or Bash, so the gate and the play-through were left; this session ran both.

P289 STOPPED: asked Chase (Iron-P289-20261021-170559-0c06). The final red-green gate and clean play-through were interrupted: the background build wait was killed for low memory and is not restarted unasked. Fixes are in notes\cc-P289-tools\fixes.patch.
