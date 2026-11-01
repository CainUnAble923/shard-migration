# cc-P758: isle-only release 5 (the vision shrine)

Iron Golem, 2026-11-01.

## In plain words

- **The isle-only release branch now has the new vision.** When a trainee double-clicks the signpost at the standing
  stones, the screen goes dark and they are taken into a small dungeon shrine. They watch, unseen, as the Stranger
  walks to the Gem on its pedestal and strikes it, and the Gem shatters. Then they are back on the very tile they
  stood on. Nothing else was added: none of the map swap, no New Haven work.
  Branch `release/isle-20261028`, commit `7a220f1` (pushed).
- **I watched it in the game.** A new character in TazUO went dark, saw the shrine, watched the Stranger strike, and
  saw the Gem break into shards. Then it was back on its tile with "Lesson finished" (sheet:
  `notes\cc-P758-tools\shots\sheet-vision.jpg`).
- **Pulling the plug mid-vision is safe.** I killed the game in the middle of the vision. On logging back in, the
  character stood on the same tile it started from, seen, and could walk. The bot also played the whole isle from the
  beach to Rook with nothing failing (85 checks).
- Nothing for you to do; the overseer builds and publishes the player package from the branch.

## What to release

- **Branch:** `release/isle-20261028`, pushed to origin (`9c31000..7a220f1`).
- **Commit:** `7a220f10cf32c6a2fa656af6bf1b369b26af1ba5`.
- **Worktree:** `D:\UO\golems\Iron\release-isle-20261028` (P722's).
- **Image tag:** `sl-modernuo:cc-P758` (image `0046a4d73344`).
- **`VERSION`:** `2026.10.31.7` (main's number for P742's section, as earlier rounds took main's numbers).
- Not built as a player package, not published, not merged into main. The shared Test Shard was not touched.

## The pick

| Task | Picked from main | On the branch | Result |
|---|---|---|---|
| P742 vision shrine | `c738631 -m 1` (holds `49298f3`) | `7a220f1` | CHANGELOG and VERSION conflicts only |

- **Merge order:** on main, P742 merged as `c738631`, after P751 (already on the release) and P735. P735, P753, P714,
  P743, P747, P755 and P757 were not picked.
- **No fix-ups of P742 on main.** No commit after `c738631` on `origin/main` (`14f3b14`) names P742, the vision or the
  shrine. None touches any of P742's five files.
- **Every code and test file is byte for byte main's** (`git diff c738631` per file, all equal):
  - `TutorialVisionChamber.cs`, `TutorialVisionChamberLayout.cs` and `TutorialVisionScene.cs`;
  - `TutorialVisionChamberVerification.cs` and `TutorialIsleBandageWaitVerification.cs`.
- The commit keeps P742's subject line, plus lines naming the merge it was picked from.

**How the conflicts were resolved** (`notes\cc-P758-tools\resolve_p742.py`):
- `CHANGELOG.md`: kept main's `2026.10.31.7` section (P742's one line). Dropped `2026.10.31.5`, a Staff section from a
  task that is not in the release, which sat in main's side of the conflict.
- `VERSION`: `2026.10.31.7`.

**No map change was needed.** The shrine is not on the map. It is 114 scene props placed when the vision starts and
removed when it ends. Its strip (x 6170-6570, y 3752-3760 on the player's lesson map) is void on stock Trammel as
well as on the SoS map: P742 read both files, and the live run shows it on the stock land. The release's
`trammel.mapops` is unchanged (`git diff 9c31000 7a220f1 -- player-package/vendor/shattered-legacy-map` is empty).

**Left out, as asked:** every SoS swap commit (P674 to P691, P708, P750, P753), P690, P743 and P755 (New Haven), and
everything else on main since `9c31000`.

## Tests

- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P758`, `docker-build` lock taken and released): **EXIT=0**.
  2,770 shard tests: 2,765 passed, 5 skipped (the usual client-data facts), 0 failed
  (`notes\cc-P758-tools\green-gated-build.txt`).
  - P742's 9 chamber facts passed, and so did P721's and P665's vision facts and the bandage-wait facts.
  - Every patch applied.
  - Free memory at the start: 7.3 GB on Windows, 13.4 GB in the Docker VM after dropping its page cache. The build
    ran detached.

## On the private shard (127.0.0.1:2596, never the shared Test Shard)

Setup:
- `sl-modernuo:cc-P758` on a fresh copy of the bot world for each session (`proof-shard.ps1`, container
  `sl-p758-proof`).
- The map overlay is P749's (`D:\UO\golems\Iron\p749-proof\overlay`): the release's patch on **stock** client data.
  The patch has not changed since then.
- The `test-shard` lock was taken once and released, and the container is down.
- The shard logs of all three sessions have no exceptions (`runs\tazuo\shard-session*.log`).

**Bot route, beach to Rook: 85 checks, 0 failed** (`runs-run1-console.txt`, `runs\run1\`, 186 s).
- The fresh character woke on the sand and played every lesson.
- "core.loop done" after 62 s, through the shrine.
- The moongate put it beside Rook at 3501,2572. The New Haven pick started on the plaza.
- **One fix to the bot, not the server.** The first full run (`runs-run1a-console.txt`) reached Rook with one failed
  check, "a quest arrow points to Tamsin". The server sent the arrow exactly as in P749's green run: same packet,
  30.47 s against 30.48 s, straight after the "quiet shore" line. The bot read its arrow list the moment that line
  arrived, before the next packet was parsed. P742 does not touch the wake.
  - My copy of `isle.py` (P749's) now waits up to 2 s for that arrow.
  - The rerun on a fresh world: 0 failed.

**A real character in TazUO** (`isle-shots758.ps1`, `vision758.json`). This is P742's runner, changed in two ways:
- it uses the release's stock land (no `-MapBase`, as the release's own launcher does);
- it handles a `KILL` signal, which kills the client for a hard disconnect.

The bot's client made **Iron Visionary** and played every lesson before the vision, stopping at the standing stones
(`runs-stop1-console.txt`). The two failures there are the Tamsin arrow race above and the route's Rook check, which
a stopped run never reaches. TazUO then logged that character in, and Legion scripts started by the client played
the vision with its own double-clicks.

1. **Disconnect mid-vision** (`VisionDrop758.py`, `VisionBack758.py`, `runs\tazuo\drop.log`): 0 failed.
   - The character started the vision from 6792,3984 and was in the chamber at 6176,3758 at 10 s, after the strike.
     Then the client was killed.
   - The Admin's check while it was logged out: not hidden, not frozen. Its `Location` read 6176,3758 on map Internal.
     That is the spot it was in when the link dropped, which a logged-out mobile keeps; the spot it comes back to is
     its logout spot, and the login below shows that is the start tile.
   - Logged back in: on 6792,3984, the very tile, not in the strip, seen, and it walked a step.
2. **The whole vision** (`VisionShots758.py`, `runs\tazuo\vision.log`, shots `shots\tazuo-vision-00` to `-16`):
   - The character was in the chamber and hidden from 1 s to 58 s. It was back on 6792,3984 at 64 s, seen, with the
     lesson finished.
   - The script's last check, a single step, "failed": the first step only turned the character, as in P742's run.
     The disconnect run shows free movement (the third step moved it), and so does the bot, which walked on to the
     moongate.
   - **Run 1** of this script (`runs\tazuo\vision-run1.log`) did not start the vision. My disconnect check's step had
     left the character at 6792,3985. That is 4 tiles from the signpost, and the sign answers within 3. The script
     now walks back north first; this was my test's fault, not the release's.
   - My look at the shots (`sheet-vision.jpg`):
     - dark at first, then the stone room lit by braziers and wall torches, with broken pillars;
     - the Stranger walks from the north-west corner to the white pedestal and strikes it;
     - the blue burst of the second blow, then the Gem gone, with shards on the pedestal and the floor;
     - the trainee's echo, and the hooded figure speaking its line;
     - back at the stones with "Lesson finished", next "Getting around".

## Deviations and decisions

- **A commit and a push.** The Golem's standing rule is no commits or pushes, but this prompt asks for a pushed
  release branch. As P722, P731, P733 and P749 did, I committed the pick on `release/isle-20261028` in its own
  worktree and pushed that branch only. `golem/Iron/P758` has no commits from me.
- **Bot fix:** the Tamsin arrow check waits up to 2 s (above). This is in my tools copy only, not in the repo's bot.
- **Two TazUO characters became one.** The second bot character (Iron Dreamer) started in New Haven, because only an
  account's first character takes the isle. So the disconnect test and the whole vision were both played on Iron
  Visionary, the disconnect test first.

## Files

- Code copy: nothing. The pick is commit `7a220f1` on `release/isle-20261028`, pushed.
- Docs copy: this note, and `notes\cc-P758-tools\`:
  - `resolve_p742.py`;
  - the build: `gated-build.ps1`, `gated-build.log` (UTF-16), `green-gated-build.txt`;
  - the shard and the bot: `proof-shard.ps1`, `isle.py`, `runs-run1-console.txt` (green), `runs-run1a-console.txt`
    (the arrow race), `runs-stop1-console.txt`, `runs-stop2-console.txt` (the New Haven character), `runs\run1\`;
  - TazUO: `isle-shots758.ps1`, `vision758.json`, `vision758-replay.json`, `VisionDrop758.py`, `VisionBack758.py`,
    `VisionShots758.py`, `runs\tazuo\` (logs), `shots\` (23 shots shrunk to 960 wide, and `sheet-vision.jpg`).
- Outside the repos: `D:\UO\golems\Iron\p758-proof\` holds the shard copy, the client, the bot copy and the
  full-size shots. It can be deleted.

P758 DONE
