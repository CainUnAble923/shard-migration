# cc-P204: fix-up for P202 (the P191 skill-gain merge): main merged again, nothing to resolve

Written 2026-10-20 by the Bronze Golem (Fable), on branch golem/Bronze/P204 of both repos. The integrator could not
merge golem/Bronze/P202 into main at 10:26, not for a conflict but because the shared docker-build lock was held: by me,
for cc-P203's build (taken 10:25:43 for 75 minutes, released 10:31). It undid the merge, marked P202 handled in its
queue (`D:\UO\golem\merge-queue\handled-P202-*`) and wrote this prompt, so this branch is P202's route to main.

## Headlines

1. **No conflict and no change: golem/Bronze/P204 is now a fast-forward to golem/Bronze/P202 in both repos.** Main has
   not moved since P202 was made (7083632 in ShatteredLegacy, c39b295 in shard-migration), and P202's merge commit
   already has main as a parent, so "merge main into P202" is a no-op and "merge P202 into P204" is a fast-forward:
   `git merge --ff-only golem/Bronze/P202` moved P204 to fe1e4b0 (ShatteredLegacy) and e4f7396 (shard-migration). No
   merge commit was made and there was nothing to resolve; the commit preflight reports both repos clean, so the Golem's
   commit after this DONE adds only this note.
2. **The gate is green on this tree again: `sl-modernuo:cc-P204`, 1,558 tests, 1,554 passed, 4 skipped, 0 failed**, the
   same figures as P202 and P191; all nine `SkillGainRateVerification` results passed. Run because `server\` differs from
   main (P191's two files and its test), as the prompt asks, even though the tree is byte-identical to the one P202
   built an hour earlier.
3. **For the integrator: the lock and the merge round can trip each other.** A Golem's build holds docker-build for its
   stated minutes; a merge round that finds it held writes a fix-up prompt instead of waiting, and that fix-up then
   builds, which holds the lock again while the next merge (P203 is queued, tries 0) may come round. I kept this build's
   hold to 20 minutes asked and about two minutes used (10:33:40 to 10:35:26). A merge round that waits on the lock, or
   retries P<nn> itself before writing a fix-up, would close the loop; that is a change to the Golem scripts, not to this
   branch.
4. **Also for the integrator, repeated from cc-P203's note:** P203 and this branch both touch CHANGELOG.md next to the
   `## 2026.10.19.5` heading (P203 inserts `## 2026.10.19.6` above it; this branch adds P191's two lines inside it), so
   whichever merges second will most likely stop on CHANGELOG.md. Keep the .6 section above .5 and P191's Changed and
   Staff lines inside .5. Nothing else overlaps.

## What changed

Nothing, beyond this note. The tree is P202's: against main, ShatteredLegacy differs in `CHANGELOG.md` (P191's two lines
in the 2026.10.19.5 section), `server\customizations\ClusterFSkillGain.cs`, `server\customizations\Engines\ML Quests\
Items\NewHavenQuestBoard.cs` and the new `server\tests\Skills\SkillGainRateVerification.cs` (474 insertions, 5
deletions); shard-migration differs in the P191 and P202 notes. See `notes\cc-P202-cont-fixup-cont-earned-skill-gain.md`
for the CHANGELOG resolution P202 made and `notes\cc-P191-cont-earned-skill-gain.md` for the content.

## The conflicts

None. `git merge-base --is-ancestor main golem/Bronze/P202` is true in both repos, so there was no second side.

## Build record

- Free memory before launch: 4.0 GB of 31.7 GB (lower than the 7 GB of the two earlier builds today; the 2026-10-19 kill
  happened at 3.3 GB). The build ran detached from the agent shell (runner script started with `Start-Process
  bash.exe`, log `build-P204-cycle1.log` in the session scratchpad, 3,506 lines), so a memory reap could not reach it,
  and the builder stage was fully cached, so only the 13-second test container used memory.
- docker-build lock taken 10:33:40 for 20 minutes, released 10:35:26.
- One cycle, 10:34:06 to 10:34:30: every builder layer CACHED (the tree is P202's), test gate in a fresh container
  **1,558 tests, 1,554 passed, 4 skipped, 0 failed**, runtime image `sl-modernuo:cc-P204` (id c593cf89e758, label
  sl.commit=fe1e4b0, the P202 merge commit, and sl.dirty as the script reports it).
- Red first: no gate was added or changed.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -Branch golem/Bronze/P204 -CodeRepo D:\UO\golems\Bronze\ShatteredLegacy
-DocsRepo D:\UO\golems\Bronze\shard-migration`, 2026-10-20 10:35: code "nothing to commit", docs "nothing to commit",
both "clean"; this note is the one file the Golem's commit will add. No file over 5 MB in either repo (find -size +5M:
none). No test-shard, package or haven lock was needed; nothing was placed in any world and no config was changed.

P204 DONE
