# cc-P202: fix-up for P191 (skill gain that feels earned): merge main into the P191 work

Written 2026-10-20 by the Bronze Golem (Fable), on branch golem/Bronze/P202 of both repos. P191 finished on
golem/Bronze/P191 and the integrator could not merge it into main: CHANGELOG.md conflicted with P186 (the Golem join
kit), which had landed on main in between.

## Headlines

1. **Both repos now hold the merge of golem/Bronze/P191 and main, staged and uncommitted on golem/Bronze/P202.** The
   branch the Golem gave me, golem/Bronze/P202, was created at main (7083632 in ShatteredLegacy, c39b295 in
   shard-migration), so "check out P191 and merge main into it" and "merge P191 into P202" are the same two heads with the
   same merge base; I did the second, because the hand-off forbids switching branches, and the integrator merges P202
   into main afterwards, which then carries P191 and its resolution. `MERGE_HEAD` is left in place in both repos
   (08c0162 and 4a918f1), so the Golem's `git add -A; git commit` produces a proper merge commit with both parents, and
   the P191 commits stay in history.
2. **One conflict, in ShatteredLegacy CHANGELOG.md, resolved as the prompt says.** Both sides had started the same
   version section `## 2026.10.19.5` (P186 a Staff list of five lines, P191 a Changed line and a Staff line). The merged
   section keeps the one heading, P191's `### Changed` line first, then one `### Staff` list with P186's five lines
   followed by P191's line. VERSION was 2026.10.19.5 on both sides, so it needed nothing. shard-migration merged clean
   (P191 only added its notes file there).
3. **Build and tests green on the merged tree: `sl-modernuo:cc-P202`, 1,558 tests, 1,554 passed, 4 skipped, 0 failed**,
   the same figures as P191's cycle 3. All nine results of P191's `SkillGainRateVerification` (R1 five pairs, R2, R3, R4,
   S1) passed. One cycle; nothing was red, so nothing needed fixing.
4. **A note for the integrator on the version number.** The prompt's rule (both sets of lines under the newer heading,
   VERSION takes the higher) gives one 2026.10.19.5 section carrying both P186's and P191's lines. If main's
   2026.10.19.5 has already been deployed or its patch notes published, the P191 lines would be invisible to the login
   bulletin, which shows notes once per account per version; in that case the fix is to move the P191 Changed and Staff
   lines under a new `## 2026.10.20` heading and bump VERSION. I followed the rule as written and did not do that.

## What changed

Nothing new was written in either repo beyond this note and the conflict resolution. The merged content is exactly
P191's (see `notes\cc-P191-cont-earned-skill-gain.md`):

- `server\customizations\ClusterFSkillGain.cs`: defaults 2 chance attempts and 1x amount (were 3 and 5), header comment.
- `server\customizations\Engines\ML Quests\Items\NewHavenQuestBoard.cs`: comment only.
- `server\tests\Skills\SkillGainRateVerification.cs`: new, 461 lines.
- `CHANGELOG.md`: the merged 2026.10.19.5 section (headline 2). `VERSION` unchanged at 2026.10.19.5.
- shard-migration: `notes\cc-P191-cont-earned-skill-gain.md` (P191's notes) arrives through the merge.

## The conflict, exactly

`git merge-tree --write-tree golem/Bronze/P202 golem/Bronze/P191` named CHANGELOG.md only. The block between the
markers (lines 34-47 after the merge):

- HEAD (main, P186): `### Staff` + five lines (join kit, web console per Golem, portraits, pause rules, Shard Console
  crash fix).
- golem/Bronze/P191: `### Changed` + one line (the earned rate), blank, `### Staff` + one line (the seeded simulation).

Resolution written by a small Python script in the session scratchpad that spliced the two lists (5 + 1 Staff lines),
then `git add CHANGELOG.md`. Checked afterwards: zero conflict markers in either repo (`git grep` for the three marker
forms), zero unmerged paths, and the image built from the tree carries the merged file at
`/modernuo/Data/ShatteredLegacy/CHANGELOG.md` with VERSION 2026.10.19.5 beside it (read back from the container).

## Build record

- Free memory before launch: 7.5 GB of 31.7 GB (the 2026-10-19 kill happened at 3.3 GB). Docker Desktop 29.5.2 up, no
  `sl-modernuo-bot` container, no manual bot run, so the nightly was not in the way.
- docker-build lock taken for 75 minutes at 10:18 and released at about 10:21.
- The build ran detached from the agent shell (a runner script started with `Start-Process bash.exe`, log in the
  session scratchpad `build-P202-cycle1.log`, 3,511 lines), so a memory reap of the shell could not kill it.
- Cycle 1, 10:19:14 to 10:19:39: every builder-stage layer was CACHED, because the merged `server\` tree is byte-identical
  to P191's (P186 touched no server file); the test step still ran in a fresh container (13.4 s, 1,558 tests); in the
  runtime stage only the `COPY CHANGELOG.md VERSION` layer and after it rebuilt. Image id fc89cbd6fe0b, labels
  sl.commit=70836321 (main's head, since the merge is uncommitted) and sl.dirty=1.
- Red-first: this task added no gate, so there was nothing to watch fail; P191's note records its own red run.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -Branch golem/Bronze/P202 -CodeRepo D:\UO\golems\Bronze\ShatteredLegacy
-DocsRepo D:\UO\golems\Bronze\shard-migration`, 2026-10-20 10:22. Neither repo BLOCKED. No file over 5 MB in either repo
(find -size +5M: none).

```
=== code  (D:\UO\golems\Bronze\ShatteredLegacy) ===
  4 file(s) pending:
    CHANGELOG.md
    server/customizations/ClusterFSkillGain.cs
    server/customizations/Engines/ML Quests/Items/NewHavenQuestBoard.cs
    server/tests/Skills/SkillGainRateVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\golems\Bronze\shard-migration) ===
  1 file(s) pending:
    notes/cc-P191-cont-earned-skill-gain.md
  dry run: would add, commit and push
```

This note is the second pending file in docs once saved. No test-shard, package or haven lock was needed; nothing was
placed in any world and no config was changed.

P202 DONE
