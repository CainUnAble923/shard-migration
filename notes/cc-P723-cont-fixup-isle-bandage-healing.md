# cc-P723: fix-up for P721 (the isle bandage wait): merged with main

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`, both
on `golem/Iron/P723`, which starts at main (the P718 merge, `bb203a8`). Not committed (the Golem commits), nothing
deployed, Haven not touched.

## In plain words

- **P721's isle changes now sit on top of main without conflicts:** the wake-up on the beach, Pip the farm boy as the
  bandage patient with the visible bandage wait, the pitchfork and war-mode lesson, the dying help, and the slower, lit
  vision. P718's changes already on main all stay.
- **The patch notes keep both sets of lines** under one heading, 2026.10.28.3.
- **The full test build is green**: 2,723 tests passed, none failed.
- **For you:** nothing to do. The integrator merges this branch next.

## What was done

The prompt says to check out `golem/Iron/P721` and merge main into it. The hand-off says not to switch branches, and my
copies are on `golem/Iron/P723`, which is main. So I merged the other way, `git merge --no-commit --no-ff golem/Iron/P721`,
in both copies. It gives the same tree, and the Golem commits it. The docs copy merged cleanly (P721's notes and tools,
26 files).

## The conflicts (code copy), and how each was resolved

| File | Resolution | Why |
|---|---|---|
| `CHANGELOG.md` | Both sections under one `## 2026.10.28.3`: P721's three Added and two Changed lines, followed by P718's four Added, three Changed, one Fixed and one Staff line | Both branches had numbered their section `.3`; P721's branch also had P718's lines under `.2`. Both sets are kept under the newer heading, as the prompt says. `VERSION` is `2026.10.28.3` on both sides, so it is unchanged. |
| `server/customizations/Tutorial/TutorialFarm.cs` | P721's side | Main's copy of each of these four files is byte for byte P718's commit (`08d9692`; checked with `git rev-parse` of each blob). P721's branch already carried P718's work, and its diff from P718's commit holds only P721's own changes: the pitchfork step instead of the pet-command gate lines, Pip as the patient, and the seeder's new counts. So P721's side keeps both. |
| `server/tests/Tutorial/TutorialCopiesVerification.cs` | P721's side | as above |
| `server/tests/Tutorial/TutorialFarmVerification.cs` | P721's side | as above (the seeder counts with Pip) |
| `server/tests/Tutorial/TutorialIsleWalkFixesVerification.cs` (add/add) | P721's side | as above |

After resolving, the staged tree differs from `golem/Iron/P721` in `CHANGELOG.md` only (`git diff --cached --stat
golem/Iron/P721`). The other files git merged by itself (`apply-patches.sh`, `FoldRegions.cs`, `TutorialCoreTrials.cs`,
`TutorialStart.cs`, `TutorialVisionScene.cs` and P721's new files) are already as P721 had them.

## Tests

`docker/uo/build.sh -t sl-modernuo:cc-P723`, detached (`notes\cc-P723-tools\gated-build.ps1`), under the `docker-build`
lock (released), Windows 3.2 GB free: **green, EXIT=0**, "Built sl-modernuo:cc-P723 with patches applied and 2723 shard
test(s) passing". 2,729 tests: 2,723 passed, 6 skipped (the usual client-data facts), 0 failed. This covers every
fact P721 ran, including its new `TutorialIsleBandageWaitVerification` (`notes\cc-P723-tools\gated-build.log`).

## Heads-up for the integrator

P720 (`golem/Iron/P720`, also from the P718 merge) edits `TutorialFarm.cs`, `TutorialFarmVerification.cs`, `CHANGELOG.md`
and `VERSION` (2026.10.28.4), so it will conflict with this merge in the same places. Its changes are the isle
farm layout, a `MakeIsleDoor`, `IsCurrent` with the relaying in `Seed`, and the house sign's name. They are separate
from P721's Pip and pitchfork work, so both can be kept.

P723 DONE
