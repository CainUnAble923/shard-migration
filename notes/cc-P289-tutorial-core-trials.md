# cc-P289: the tutorial's core trials, placed on a test world and played end to end

## In plain words

- The new player tutorial now plays from first login to graduation. On a private copy of the test world, a brand-new
  character did all nine lessons: walking, paperdoll, backpack, chat, death, bank, travel, the League and the loop
  vision. Then it graduated at Rook, got its box and picked its dog. Skip, remedial training and "Reset this lesson"
  worked too. The final run passed all 93 checks with no failures.
- The play-through found three bugs, now fixed and tested. A ghost double-clicking the tutorial healer now gets the
  resurrection offer, not her paperdoll. An old arrow from a previous login no longer wipes the arrow to the next
  lesson. Staff are no longer pulled into the tutorial when they log in.
- Nothing is placed on live, and the tutorial stays switched off there. On a test world, `[ClusterFSeedTutorial`
  places everything, and running it twice places nothing new.
- For you: the open decisions under "For Chase" (the loop placeholder, the crowded first login, the doubled "System:"
  name). Also, one shared build check can fail at random (For Chase 11). Otherwise nothing for you to do.

2026-10-21 to 10-23, the Iron Golem (Opus 5.5), branch `golem/Iron/P289` of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Iron\cc-P289-tutorial-core-trials-playable.md`. Not committed (the Golem commits). Nothing
deployed, and nothing was run against live or the shared test shard (2594).

## Where it stands

| Step | State |
|---|---|
| Valorite's draft (code 0abfa6a, docs 7278976) | Brought in as uncommitted changes (`git diff HEAD origin/golem/Valorite/P289 \| git apply --index`; the Golem rules forbid a real merge); its notes are folded in below |
| Iron's WIP (code c3cf628, docs dc21ef4) | The branch head in both repos; this sitting continued from it |
| Build gate on the draft | Green: 2,100 tests, 4 skipped, 0 failed (10-21 16:19-16:23) |
| Part 1, the nine trials | Built and played for real twice in the final run (core, then remedial): all pass |
| Part 2, the seeder | Played for real: dry run, seed, seed again (0 placed), dry run (0 to place) |
| Part 3, the wings | Played for real: Alchemy says "Coming soon. This wing is optional", is not marked done, and graduation does not wait for it |
| Part 4, the play-through's fixes | 3 bugs fixed, each with a test seen red then green. Loop placeholder: listed, not settled (For Chase 7) |
| Red run | 10-23 06:4x: 2,102 tests, **3 failed** (exactly the three new facts), 2,095 passed, 4 skipped |
| Green gate | 10-23 06:58: `Built sl-modernuo:cc-P289 with patches applied and 2098 shard test(s) passing.` 2,102 tests, 0 failed, 4 skipped (image db37b1fe6642) |
| Final play-through | 10-23 07:37-07:41, fresh world: **93 PASS, 0 FAIL** (`notes\cc-P289-tools\playlog-final.txt`) |

## The play-through

**The shard.** A private, loopback-only scratch shard, not the shared test shard: image `sl-modernuo:cc-P289`,
`127.0.0.1:2596`, with the test-shard lock held throughout. The world and Configuration were scratch copies of the bot
shard's (`D:\UO\bot-shard`, saved 10-23 05:49: New Haven as it stands, 211,511 items and 35,241 mobiles). The listener
was changed to 2596, and the `AccountWipe` folder was removed, so the Golem accounts were made and nothing was wiped.
The client data is `D:\UO\UltimaOnlineVanilla` (7.0.117.0), read only. The overlay is P276's patch, rebuilt into
scratch by `docker\uo\Build-MapOverlay.ps1 -UoData D:\UO\UltimaOnlineVanilla -Out <scratch>`. The compose file:

```
name: sl-uo-p289
services:
  modernuo-p289:
    image: sl-modernuo:cc-P289
    container_name: sl-modernuo-p289f
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

**A newer save.** Main had moved on since this branch was cut, so the bot shard's save holds things this build does
not know: P359's `ChoppedTreeStump` items, and P408's `SorcerersDungeon` points system in `PointsSystem.bin`. The
server stops at load and asks on its console "Delete all of those types? (y/n)", then "Skip this file and continue?
(y/n)". It refuses a piped stdin ("headless"), and `docker attach` refuses a non-terminal stdin on a TTY container.
So a scratch script wrote "y" to the container's stdin through the Docker Engine API (`\\.\pipe\docker_engine`,
`POST /containers/<name>/attach?stream=1&stdin=1`). On this scratch world that dropped the tree stumps and the points
table; the tutorial uses neither. A run on a world saved by this branch's own build needs none of this.

**The player.** `notes\cc-P289-tools\playthrough.py` drives the play-test bot's own client (`tools\playtest-bot\uobot`:
the packets a 7.0.117 client sends). Iron's Admin seeds. Iron's Player account makes a fresh character, "Iron
Graduate", with normal character creation (0xF8). Every step is a player action the server checks; no staff command
completes anything. The one staff step is `[Tutorial reset` before the skip run, so the same account can start again.
Passwords come from `Get-GolemTestAccount.ps1` and never reach a file. There are no screenshots: this PC has no capture
route for the bot, so the evidence is the System lines and state changes.

**The final run** (`playlog-final.txt`; 93 PASS, 0 FAIL):

- Seed: the dry run would place 9 station markers, 4 NPCs and the echo, 1 gate, 1 gold mark and the farm (1 addon, 1
  door, 1 Farmhand, 2 spawners); the seed placed exactly that; the second seed placed 0 ("already there 5"); the last
  dry run would place 0. The Admin's login brought no recruiter greeting (bug 3's fix, live).
- Core: the first login greets and arrows to Rook. Then: the two marks; the cloak onto the paperdoll; the blue bag; the
  phrase (a wrong line first finishes nothing); death at the echo and, as a ghost, a **double-click on Sera that offers
  the resurrection** (bug 1's fix, live); the bank; the gate to the plaza; Elara; the vision (no skill changed). Then
  back to Rook: the Alchemy wing says coming soon and stays not done; Graduate; "Open that box here in town"; the box
  opens in town; the dog.
- Skip and remedial, after `[Tutorial reset`: the login enters the core again; "No" at the second confirmation leaves
  it InCore; yes at both skips and earns "Didn't Read the Manual". Rook offers Remedial training, and the nine lessons
  are played again, chat after "Reset this lesson" reopens it undone. A second graduation earns "Read the Manual
  Eventually".
- No arrow went missing between lessons in either pass (bug 2's fix).

**The driver's own faults, fixed in this sitting** (the server was right each time):

- After the new wing check, the double-click on Rook came too soon and was refused ("You must wait to perform another
  action"). `recruiter_station` now waits and tries once more when that happens.
- The dog from the graduation pick followed the player into the Registrar's house and stood in the one-tile doorway.
  The walker counted every mobile as a wall, so it found no way out. New Haven is in Trammel, where a player walks
  through mobiles (pinned `Mobile.CheckShove`, `MapRules.FreeMovement`), so the walker now plans through mobiles when
  there is no other way. It also never marks a door's tile as blocked, and may open the same door up to three times.
- Meditation (skill 46) rose while the vision played: mana regeneration's passive gain (pinned `RegenRates.cs:140`),
  sped up by `testCenter.skillGainMultiplier`. The "vision changed no skill" check now leaves Meditation out, as it
  already did Focus.

**Earlier runs** (10-21, logs kept): `playlog-seed.txt`, `playlog-core.txt` and `playlog-skip-remedial.txt` are the
first sitting's runs. They found the three bugs below.

**What the play-through found and fixed:**

1. **A ghost cannot ask the healer** (`TutorialHealer`). Pinned's `Mobile.Use` sends a dead player's double-click to
   `OnDoubleClickDead`, which opens the paperdoll; the draft overrode `OnDoubleClick`, which never runs for a ghost.
   The stock offer, `BaseHealer.OnMovement`, needs a step into range, and the lesson teleports the ghost beside Sera.
   Fix: override `OnDoubleClickDead`. Test: the hooks fact goes through `p.Pm.Use(healer)` and asserts the offer.
2. **An arrow left behind by a logout** (`GuildDirectionArrow`, shared with the guild and League arrows). Pinned's
   logout calls `ClearQuestArrow`, which drops the reference without stopping the arrow (`PlayerMobile.cs:1585`). The
   orphan kept ticking, and when it arrived, its stop sent 0xBA off and wiped the arrow to the next lesson. Fix: an
   arrow that is no longer the player's ends its timer silently. Test:
   `AnArrowLeftBehindByALogoutNeverFindsItsSpotLater`.
3. **Staff were entered** (`ClusterFTutorial.TryEnter`). Fix: GameMaster and above, by character or account, are
   never entered. Test: `StaffAreNeverEnteredIntoTheTutorial`.
4. **Text:** the death lesson said "Your corpse stays by the echo". A Young character's things come back to its
   backpack on resurrection, so the hint and the echo's page now say that.

**Seen, not changed** (other systems; For Chase 8 and 9): a new character's first login brings three Common Boxes,
achievement pages, the Welcome page and the patch notes all at once with the tutorial's greeting; System lines read
"System: System: ..." in the bot's log.

## Tests

| Run | When | Result |
|---|---|---|
| Gate on Valorite's draft | 10-21 16:19 | 2,100 total, 0 failed, 4 skipped |
| Red: new facts, no fixes (`--tests-only`) | 10-23 06:4x | 2,102 total, **3 failed**, 2,095 passed, 4 skipped |
| Green: full gate with fixes (image too) | 10-23 06:58 | 2,102 total, 0 failed, 2,098 passed, 4 skipped |

The red failures, each the bug's own symptom:

- `BagSpeechBankLeagueAndTimedVisionObserveTheRealHooksWithFakePlayers`: offers observed, expected 2, actual 1 (the
  ghost's double-click went to the paperdoll). `TutorialVerification.cs:366`.
- `StaffAreNeverEnteredIntoTheTutorial`: expected NotStarted, actual InCore. `TutorialVerification.cs:508`.
- `AnArrowLeftBehindByALogoutNeverFindsItsSpotLater`: the orphan stopped itself on arrival. `TutorialVerification.cs:529`.

The first red attempt never reached the tests. The patch step's "every patch file is accounted for" check reported
`CraftItem-chefs-apron.patch` as "never applied" although the same log shows "Applied: CraftItem-chefs-apron.patch".
That is a race in `apply-patches.sh`, not this branch (For Chase 11). The rerun passed that step, with nothing changed.

Valorite's 26 focused facts (`server\tests\Tutorial\TutorialTrialProgressVerification.cs` and the tutorial facts) were
seen red then green on its native route and are green on both gates here.

## For Chase

The prompt's defaults, kept:

1. Recruiter: Rook Hallowell at 3500,2572,14.
2. Voice: the "System:" lines.
3. Order: the core first, then the wings.
4. Graduation box: Explorer's tier 1.
5. Live: `tutorial.enabled` stays off on live. The code refuses it unless `testCenter.enable` is set, and every seeder
   refuses anywhere but a test world.
6. Client: server-driven hints only, no TazUO patch.

Open:

7. **The loop placeholder (P80 decision 7) is not settled.** P282 (F-12 numbers) is open and numbers only. F-12's
   decisions count a new character as loop 0 (`notes/f12-decisions-2026-10-05.md:27`; `docs/feature-queue.md:1227`).
   That matches `EvoPet.OwnerLoopsSource` (0), and makes `ClusterFLootBoxes.LoopProvider`'s default of 1 the odd one
   out. The vision changes neither. Left as it is, for F-12.
8. **The first-login flood:** should the tutorial's greeting come after the boxes and pages, or should those wait for
   the tutorial? (Other systems; not changed.)
9. **"System: System:" in the journal**, if TazUO shows the sender's name: worth a look in a client.
10. **Young death:** the lesson says a Young character's things come back to the backpack. A remedial player past
    Young keeps a real corpse by the echo; the line covers only the Young case.
11. **A random build failure in the shared patch step.** `docker/uo/apply-patches.sh` runs under `set -o pipefail` and
    checks each patch with `printf '%s' "$HANDLED_PATCHES" | grep -Fxq "$name"`. When `grep -q` finds the name early
    and exits, `printf` can die of SIGPIPE, the pipeline fails, and a patch that was applied is reported "never
    applied". Main has the same line. A one-line fix is `grep -Fxq "$name" <<< "$HANDLED_PATCHES"`. It is not made
    here, because it is shared build code outside this task. Worth its own small prompt.

Deviations:

- Valorite's draft was brought in with `git apply --index`, not merged (the Golem's standing rules forbid merging).
- A private shard on 2596 instead of the shared test shard: `Start-TestShard.ps1` mounts the main checkout's folders,
  which this Golem may not touch. The test-shard lock was held while it ran.
- The scratch world's load prompts were answered "y" through the Docker Engine API (above). Only the scratch copy was
  touched.
- The play-test driver was changed three times in this sitting (above), and the final run used the changed driver. The
  server code did not change after the green gate, except `CHANGELOG.md` and `VERSION`.
- `notes\cc-P289-tools\fixes.patch` is removed: its changes are now in the code tree.
- Unattended permission denials, not retried another way:
  - 10-21: the Read tool on `docker\uo\Start-TestShard.ps1` (read with `cat` after taking the lock, as the guard hook
    asked). One of two identical Reads of `server\tests\Misc\TutorialVerification.cs`.
  - 10-23: the Read tool on `D:\UO\golems\Iron\ShatteredLegacy\CHANGELOG.md` (lines 30-35), wanted before an Edit
    that added the Fixed lines. The section had already been read with `cat`, so the edit was made by a small Python
    script, an exact one-match replace (the project memory's approved route for these files).
- 10-21: the first red run was killed by Claude Code for low memory while it waited for the docker-build lock. It was
  not restarted unasked; Chase answered "Continue" (Iron-P289-20261021-170559-0c06), and this sitting ran it.

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
      Sera (3402,2613) and press Resurrect.
   6. Walk to the banker (3492,2577), say `bank`, and drag the practice token into the bank box.
   7. Walk back to the farm gate and double-click the blue moongate (3402,2615); it puts you on the plaza.
   8. Walk to Elara Voss (3459,2601, inside the Registrar's house; the door is on the north side) and double-click her.
   9. Walk to the vision marker (3402,2619), double-click it and stay within 4 tiles until "Core finished".
4. Back at Rook: Graduate. A box comes (open it in town), then the pet pick. A wing (for example Alchemy) says "Coming
   soon" and is optional.
5. Skip: on a fresh record, Rook's "Skip the tutorial", yes twice ("No, teach me" at either step changes nothing).
   Rook then offers Remedial training, the same nine lessons and a second achievement.

The bot does the same with:

```
python -P notes\cc-P289-tools\playthrough.py --port 2596 --out <folder> --map <overlay folder> --tiledata D:\UO\UltimaOnlineVanilla --parts seed,core,skip
```

## Valorite's draft notes, folded in

The Codex Golem Valorite's handoff (docs 7278976, `notes\cc-P289-tutorial-core-trials-playable.md`, removed so only
one P289 notes file carries the last line), in short:

- It built the action-evidence model (`TutorialTrialProgress`), the nine handlers (`TutorialCoreTrials`) and the
  placement (`TutorialCorePlacement`: markers, Rook, the echo, Sera, the banker, Elara and the gate if missing; the
  P276 farm; a `CanFit` preflight; refusal on live and on an unpatched map). It also made the wings' coming-soon page,
  the character check on account actions, the live gate on `testCenter.enable`, and practice supplies that delete
  themselves.
- Its 26 facts were seen red then green on a native route. It could not run Docker or Bash, so the gate and the
  play-through were left; the Iron Golem ran both.

## Commit preflight

- Code (`D:\UO\golems\Iron\ShatteredLegacy`): the three fixes (`ClusterFGuildStarterPath.cs`,
  `Tutorial\ClusterFTutorial.cs`, `Tutorial\TutorialCorePlacement.cs`, `Tutorial\TutorialCoreTrials.cs`), and
  `CHANGELOG.md` with `VERSION`. The section is renumbered `2026.10.23.2`, since main is at 2026.10.23, with a Fixed
  list and a Staff line. The new tests are already in the WIP commit c3cf628.
- Docs (`D:\UO\golems\Iron\shard-migration`): this file, `cc-P289-tools\playthrough.py`, the new
  `cc-P289-tools\playlog-final.txt`, `cc-P289-tools\fixes.patch` removed, and `tools/progress.py`'s regenerated
  `README.md`, `dashboard.html`, `tools/progress.json` and `tools/expansion-coverage.json`.
- Nothing running: the private shard is down, and no lock is held by Iron.

P289 DONE
