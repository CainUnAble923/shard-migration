# cc-P710: fix-up for P664 (private copies of the isle): its branch now merges into main

Iron Golem, 2026-10-27. Both work copies on `golem/Iron/P710` (at main: P666 and P665 merged). Not committed: the
merge is staged with `--no-commit`, for the Golem's commit. Nothing deployed; Haven not touched.

## In plain words

- **P664's private isle copies can now join the rest of the work.** Its branch had clashed with P705, P665 and P666
  in three small places. I kept both sides each time, and the whole shard's tests pass with everything together.
- **The patch notes now list the private copies under 2026.10.27.4,** beside the vision scene. Before, they had
  claimed 2026.10.27.3, which the vet change (P666) already uses.
- **Nothing for you to do.** P707's two-client play-through still gates going live, as you decided.

## What I did

1. **Merged P664 into this branch** in both copies: `git merge --no-commit --no-ff golem/Iron/P664`. The prompt says
   to check out P664's branch and merge main into it. The hand-off rules say not to switch branches, and this branch is
   main, so I merged the other way. The resulting tree is the same.
   - Docs copy: merged with no conflicts (P664's notes, its tools and its Codex review).
   - Code copy: three conflicts, below. The other 8 files merged by themselves.
2. **Resolved:**
   - `server/tests/Tutorial/TutorialTestStart.cs`: both lines kept. `Begin` sets P705's `TutorialWorld.IsleReady =
     () => true` (the test world has no isle map), then P664's `ReleaseIdleCopies()`.
   - `VERSION`: the higher, `2026.10.27.4`.
   - `CHANGELOG.md`: P664 had used `2026.10.27.3`, which on main is P666's (the vets). As the prompt says, P664's
     lines went under the newer heading, `2026.10.27.4` (P665's vision scene). Its "Added" line is there now, and its
     "[Tutorial copies" line joins P665's under "Staff". P666's `.3` section is unchanged.
3. **Checked a merge git did by itself:** P664's notes warned that `TutorialStart.cs` must keep P705's readiness check
   and P664's `Claim` together. It does. `OnCreated` (line 131) and `ConsumeAtLogin` (line 150) ask
   `TutorialWorld.IsleReady()`, and every way onto the isle goes through `SendToIsle`, which asks
   `TutorialCopies.Claim` (line 210).
4. **A leftover moved out of the work copy:** P674's git-ignored map files (`player-package/vendor/sos-trammel-map/files/`,
   141 MB) were still on disk. This branch's `.gitignore` does not cover them, so a commit could have picked them up.
   They are now in `D:\UO\golems\Iron\p674-sos-files\`; P674's `Add-SosMap.ps1` makes them again in 2 s. P674's own
   commit holds everything it tracks. This changed nothing in git.

## Build

`docker\uo\build.sh -t sl-modernuo:cc-P710`, run detached under the `docker-build` lock (taken and released), after
dropping the WSL page cache (5.4 GB free before): **green**. "All 170 patches applied successfully." "Built
sl-modernuo:cc-P710 with patches applied and 2694 shard test(s) passing." 2,699 tests: 2,694 passed, 0 failed, 5
skipped (the usual client-data facts). Image ae846e8a25f9. The three isle prompts' facts all ran and passed together:
`TutorialCopiesVerification` 7 (P664), `TutorialPetCareVerification` 5 (P666), `TutorialVisionSceneVerification` 7
(P665). No fix was needed beyond the conflicts.

## Not verified

- Nothing on a running shard or in a client (P707 does the play-through).
- P665's scene asks `TutorialWorld.MapOf`, which reads P664's copies. The facts pass with both. A trainee watching the
  scene on a private copy has not been seen in game.

## Commit preflight

- Code copy, staged as P664's merge: `CHANGELOG.md`, `VERSION`, `server/customizations/Tutorial/` (`ClusterFTutorial.cs`,
  new `TutorialCopies.cs`, `TutorialCorePlacement.cs`, `TutorialFarm.cs`, `TutorialStart.cs`, `TutorialWorld.cs`),
  `server/tests/Tutorial/` (new `TutorialCopiesVerification.cs`, `TutorialIsleVerification.cs`, `TutorialTestStart.cs`).
- Docs copy, staged as P664's merge: `notes/cc-P664-*` and `notes/cc-P664-tools/`; new, this file.
- No file over 5 MB; `docs\` untouched. Nothing committed, no locks held, nothing asked.

P710 DONE
