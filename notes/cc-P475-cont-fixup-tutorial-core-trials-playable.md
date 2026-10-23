# cc-P475: fix-up for P289 (the tutorial's core trials), merged with main

## In plain words

- The tutorial work from P289 (nine core lessons playable end to end, plus its three bug fixes) now sits on top of
  today's main, so the integrator can merge it. Nothing about the lessons changed in this fix-up.
- Where the two sides overlapped, both were kept: the tutorial stays switched off outside the test world (P289), and
  the "skipping counts as graduating" setting and the first-loop count from P371 stay too. An optional wing's
  "Coming soon" page still offers to open the matching game window in TazUO, as main had it.
- The patch notes get a new version, 2026.10.23.2, above main's 2026.10.23.
- Nothing for you to do: the full build check passed (2,194 tests, none failed) and the integrator merges it next.

2026-10-23, the Iron Golem (Opus 5.5), branch `golem/Iron/P475` of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Iron\cc-P475-cont-fixup-tutorial-core-trials-playable.md`; original P289 notes:
`notes\cc-P289-tutorial-core-trials.md`. Not committed (the Golem commits). Nothing deployed.

## What was done

The hand-off forbids switching branches, and both work copies were already on `golem/Iron/P475` at main's tip
(ShatteredLegacy 4c2af57, shard-migration b9bf572). So instead of checking out P289 and merging main into it, P289
was merged into P475 (`git merge --no-commit --no-ff golem/Iron/P289`): the same tree, and the commit the Golem makes
concludes the merge, with both P289 commits (the WIP and the finished one) as its second parent.

- **shard-migration:** merged cleanly (README.md, dashboard.html, tools/progress.json auto-merged; both JSON files
  parse).
- **ShatteredLegacy:** the four conflicts the integrator saw, resolved as below.

## Conflicts resolved

| File | Main (ours) | P289 (theirs) | Kept |
|---|---|---|---|
| `VERSION` | 2026.10.23 | 2026.10.23.2 | 2026.10.23.2 (the higher) |
| `CHANGELOG.md` | new `## 2026.10.23` (guild halls, Staff) | new `## 2026.10.23.2` (Fixed: ghost healer, old arrow; Staff: core trials, staff not entered) | Both sections; P289's 2026.10.23.2 on top as the newer version. Different versions, so they were not folded under one heading |
| `server/customizations/Tutorial/ClusterFTutorial.cs` `Configure` | added `SkipCountsAsGraduation` setting (P371) | `Enabled` needs `testCenter.enable` | Both lines |
| `server/tests/Misc/TutorialVerification.cs` fixture | `LoopProvider = ClusterFLoops.LoopOf` (P371) | added `TutorialCoreTrials.EnsureHooks()` | Both: EnsureHooks, then main's LoopOf |

One silent overlap git did not flag: main (P103, the TazUO ClientCommand buttons) gave `TutorialStationGump` a `canOpenWindows`
argument and `RunStation` passed `TazUOClientCommand.CanRunCommands(pm.NetState)`; P289 rewrote `RunStation` to show
the wing's coming-soon page with `new TutorialStationGump(station)`, which compiles (the argument defaults to false)
but would have stopped offering the TazUO window buttons. `RunStation` now passes the argument again.

## Tests

| Run | When | Result |
|---|---|---|
| Full gate, the merged tree (`docker\uo\build.sh -t sl-modernuo:cc-P475`, docker-build lock held) | 10-23 08:30-08:33 | `Built sl-modernuo:cc-P475 with patches applied and 2194 shard test(s) passing.` 2,198 total, 2,194 passed, 4 skipped, 0 failed |

Free memory before the build: 7.0 GB on Windows, 13.6 GB free in the Docker VM (no cache drop needed). The gate
includes P289's own facts (`TutorialVerification`, `TutorialTrialProgressVerification`, the three red-then-green
facts from its play-through) and main's `TazUOClientCommandVerification`, all passing. 2,198 against P289's 2,102 is
main's newer tests.

Not rerun: P289's 93-check bot play-through on a private world copy (`notes\cc-P289-tools\playthrough.py`). The
merge changed no lesson logic (two lines kept from each side plus the restored gump argument), and every fact
covering those lines is green, so a second world play-through was judged not worth the test-shard time.

P475 DONE
