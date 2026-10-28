# cc-P727: land P721 (via its fix-up P723) on main

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P727` (from main `f6ee4fd`, plus the overseer's `bd3e89d`).

## In plain words

- P721's isle fixes are now on main, ready for the integrator to merge. They had failed to merge twice. Once merged,
  the test shard's isle will have them: the beach wake-up, the help after dying, Wren's pitchfork and war-mode lesson,
  Pip the hurt farm boy for the bandage lesson, the quicker bandage there, and the longer vision at the stones.
- The isle plays through on main with them: a fresh character went from the beach to Rook in New Haven through all ten
  lessons, with no failed checks.
- The patch notes list them as their own version, 2026.10.28.6.
- Nothing for you to do.

## What I did

- **The changes:** P723 (`cb4dd56`) is P721's commit merged onto P718 with its conflicts already resolved. I brought in
  that merge's own changes, `git cherry-pick -m 1 --no-commit cb4dd56`, the same way P722 did on the release branch.
  They are left uncommitted for the Golem.
- **One conflict, the one the integrator hit:** `server/customizations/Tutorial/TutorialCoreTrials.cs`, the vision
  lesson's instruction line.
  - P720 changed "the bright blue rune stone" to "the lesson's signpost there".
  - P721 changed "under a minute" to "about a minute", because it lengthened the scene.
  - I kept both: "...double-click the lesson's signpost there. Watch the vision; it lasts about a minute...". This is
    P722's own script (`notes\cc-P722-tools\resolve_coretrials.py`), and the file is now byte for byte the release
    branch's.
- **Everything else merged by itself.** Every tutorial file and test P721 touches is identical to the release branch's
  (`release/isle-20261028`, where the full tests and the bot route passed).
  - Three files differ from the release branch, only by main's own swap work: `FoldRegions.cs`, `apply-patches.sh` and
    `CHANGELOG.md`.
  - P721's hunks are in both code files: the wake light hook (`TutorialWake.AlterLight`) in `FoldRegions.cs`, and
    `Bandage-tutorial-wait-lines.patch` registered after `Bandage-tutorial-real-heal.patch`.
- **CHANGELOG:** P723's merge had put P721's five lines into P718's section (`2026.10.28.3` on main). They land on main
  now, so they get their own newest section, **2026.10.28.6** (3 Added, 2 Changed), and `VERSION` is `2026.10.28.6`
  (`notes\cc-P727-tools\changelog_section.py`).
  - On the release branch the same lines sit in P718's section there (`.2`). Whoever releases main after it will see
    them listed again under `.6`. That is harmless, but worth knowing.

## Tests

- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P727`, `docker-build` lock, released): **EXIT=0**. 2,735
  tests: 2,729 passed, 6 skipped (the usual client-data facts), 0 failed. Both bandage patches report "Applied"
  (`cc-P727-tools\green-gated-build.txt`).
- **Bot route** (private shard 127.0.0.1:2596 running `sl-modernuo:cc-P727` on a copy of the bot world, with this
  branch's map, the SoS base plus today's `trammel.mapops`; `test-shard` lock, released; the shard is down):
  **0 failed checks** on the first run (`cc-P727-tools\runs\run1\playlog.txt`).
  - A fresh character woke on cold sand on the beach.
  - It took all ten lessons, including P721's steps: Wren's pitchfork held, war mode on, Pip bandaged and really healed.
  - The moongate put it beside Rook at 3632,2584.
  - The New Haven pick started on the plaza at 3634,2586.
  - The route is P722's `isle.py` (P721's route, taught P720's isle) with Rook's and the New Haven start's spots back
    on main's New Haven, after P678's move (`make_isle_bot.py`).
- No new tests: P721's own facts (`TutorialIsleBandageWaitVerification` and the changed tutorial facts) come in with it
  and pass in the build above.

## Files

- Code copy (uncommitted):
  - P723's changes: `TutorialDeathHelp.cs`, `TutorialWake.cs`, `Bandage-tutorial-wait-lines.patch` and
    `TutorialIsleBandageWaitVerification.cs` new, plus changes to `TutorialCoreTrials.cs`, `TutorialFarm.cs`,
    `TutorialStart.cs`, `TutorialVisionScene.cs`, `FoldRegions.cs`, `apply-patches.sh` and four tutorial tests.
  - My own: `CHANGELOG.md` and `VERSION`.
- Docs copy: `notes\cc-P727-tools\` (the gated build script and summary, the changelog script, the bot route and its
  run, the proof-shard copy).
- Outside the repos: `D:\UO\golems\Iron\p727-work\` (the map overlay, the shard copy); it can be deleted.

P727 DONE
