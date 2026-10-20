# cc-P203: fix-up for P150 (Requisitions board, the Appraiser, and Leads): merge main into the P150 work

Written 2026-10-20 by the Bronze Golem (Fable), on branch golem/Bronze/P203 of both repos. P150 finished on
golem/Bronze/P150 and the integrator could not merge it into main: CHANGELOG.md and VERSION conflicted with P186 (the
Golem join kit), which had landed on main in between. Pinned paths are relative to `D:\UO\ModernUO-pinned\Projects`.

## Headlines

1. **Both repos now hold the merge of golem/Bronze/P150 and main, staged and uncommitted on golem/Bronze/P203.** As in
   cc-P202, the branch the Golem gave me was created at main (7083632 in ShatteredLegacy, c39b295 in shard-migration),
   so merging P150 into P203 is the same merge as "check out P150 and merge main into it": same two heads, same base
   (453735e / 1ed5782). I did it that way because the hand-off forbids switching branches. `MERGE_HEAD` is left in place
   in both repos (d8c08c3 and 23daf7f), so the Golem's `git add -A; git commit` makes a merge commit with both parents.
2. **Two conflicts, both in ShatteredLegacy, resolved so both sides survive.** CHANGELOG.md: main had added a
   `## 2026.10.19.5` section (P186) and P150 a `## 2026.10.19.6` section; the merged file keeps both, P150's .6 above
   main's .5, each with its own lines, in version order. VERSION: 2026.10.19.5 on main, 2026.10.19.6 on P150; it takes
   the higher, 2026.10.19.6. shard-migration merged clean (P150 only added its notes file there).
3. **The gate went red once on the merged tree and the red was a test defect in P150, not a server defect.** Fact 9 of
   `RequisitionsVerification` (a Lead's 40th kill drops the item into the corpse) failed with "That has no Hit Chance
   Increase.": it took the **first** sword in the corpse as the drop, and a stock Orc packs a Scimitar or a Katana in 2
   constructions of 20 (pinned `UOContent/Mobiles/Monsters/Humanoid/Melee/Orc.cs:42-52`; `LootPack.Meager` can add a
   magic weapon on top, `UOContent/Misc/LootPack.cs:188-205, :268-275`). The orc's own plain blade reaches the corpse
   before the Lead's drop, so the fact failed about one run in ten and P150's green run was the other nine. The fact now
   takes the sword that fills the request and names every sword it saw when none does. One line of the test changed in
   substance; no server file changed in this task.
4. **Green on cycle 2: `sl-modernuo:cc-P203`, 1,561 tests, 1,557 passed, 4 skipped, 0 failed**, the same figures as
   P150's final cycle; all 12 `RequisitionsVerification` facts passed. Nothing else needed fixing.
5. **For the integrator: this branch will conflict again with P202 in CHANGELOG.md.** P202 (merged after P150 was
   written) adds P191's lines inside the `## 2026.10.19.5` section; this branch inserts a `## 2026.10.19.6` section
   directly above that heading. The two hunks touch adjacent lines, so whichever of P202 and P203 merges second will
   most likely stop on CHANGELOG.md. The resolution is mechanical: keep the .6 section (P150's five Added lines and one
   Staff line) above the .5 section, and keep P191's Changed line and Staff line inside .5 as P202 placed them. Nothing
   else overlaps: P191 touched `ClusterFSkillGain.cs`, `NewHavenQuestBoard.cs` and a new test; P150 touched none of them.

## What changed

Through the merge, exactly P150's work (see `notes\cc-P150-requisitions-and-leads.md`): 15 files in ShatteredLegacy,
3,495 insertions, 9 deletions against main (seven new files under `server\customizations\Requisitions\`, the account
data record at v20, the guild system, dev tools and Registrar gump hooks, `AccountDataSerializerVerification` on v20,
and the new `RequisitionsVerification`), plus P150's notes in shard-migration.

By this task:

- `CHANGELOG.md`: the merged head, `## 2026.10.19.6` (P150) then `## 2026.10.19.5` (P186), then the sections both
  sides already shared from `## 2026.10.19.4` down.
- `VERSION`: 2026.10.19.6.
- `server\tests\Misc\RequisitionsVerification.cs`, fact 9 (`ALeadGivesTheExtraRollAndThePityMakesTheFortiethKillCertain`),
  the lines after `orc.Kill()`: `swords` is every corpse item the "sword" category matches (`Assert.NotEmpty`), `drop`
  is the first of them that `RequisitionMatch.Check` accepts, and the assertion that one exists prints each sword's type
  and refusal reason when it fails. The rest of the fact is unchanged (the match, `LeadKills` back to 0, HCI at least
  30%, the extra roll to the backpack, the four kills that must not count). 11 lines added, 2 removed.

## The conflicts, exactly

`git merge-tree --write-tree golem/Bronze/P203 golem/Bronze/P150` named CHANGELOG.md and VERSION; nothing else.

- CHANGELOG.md, lines 32-53 after the merge: HEAD held `## 2026.10.19.5` and its five Staff lines (P186); P150 held
  `## 2026.10.19.6`, five Added lines and one Staff line. Resolution: P150's block, a blank line, then HEAD's block, by a
  small Python script in the session scratchpad; no line of either side was dropped or edited.
- VERSION: `2026.10.19.5` against `2026.10.19.6`; resolved to 2026.10.19.6.

The prompt's rule says "both sets of lines under the newer version heading". The two sides here used different
headings, and main's 2026.10.19.5 was already a committed section, so I kept both sections rather than moving P186's
lines under 2026.10.19.6: every line survives, each under the version it shipped with, and VERSION is the higher. If the
integrator prefers one section, moving the five P186 lines under .6 is a cut and paste.

Checked afterwards: zero conflict markers in either repo (`git grep` for the three marker forms), zero unmerged paths.

## Build record

- Free memory before the first launch: 7.1 GB of 31.7 GB (the 2026-10-19 kill happened at 3.3 GB). Docker Desktop
  29.5.2 up; no `sl-modernuo-bot` container, no manual bot run.
- docker-build lock taken for 75 minutes at 10:25 and released after cycle 2.
- Both cycles ran detached from the agent shell (a runner script started with `Start-Process bash.exe`; logs
  `build-P203-cycle1.log` and `build-P203-cycle2.log` in the session scratchpad), so a memory reap could not kill them.
- Cycle 1, 10:26:01 to 10:26:22: every builder-stage layer CACHED (the merged `server\` tree is byte-identical to P150's,
  since P186 touched no server file), test gate in a fresh container: **1,561 tests, 1,556 passed, 4 skipped, 1 failed**
  (fact 9, headline 3). No image built, as the gate requires.
- Cycle 2, 10:29:08 to 10:31:17, with the fact 9 change: builder stage recompiled (the test file is copied into the
  builder), test gate **1,561 tests, 1,557 passed, 4 skipped, 0 failed**, runtime image `sl-modernuo:cc-P203` built with
  labels sl.commit=70836321 (main's head, since the merge is uncommitted) and sl.dirty=1; the image carries the merged
  CHANGELOG.md (2026.10.19.6 above 2026.10.19.5) and VERSION 2026.10.19.6 at `/modernuo/Data/ShatteredLegacy/`.
- Red first: the gate failed on the real tree before any change (cycle 1), and the changed assertion fails the same way
  for the same reason as the old one when no sword in the corpse fills the request (`drop` null, with the list of swords
  in the message). I did not spend a third cycle breaking the factory to watch it fail again; P150's note records fact
  9's own red against a broken death event.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -Branch golem/Bronze/P203 -CodeRepo D:\UO\golems\Bronze\ShatteredLegacy
-DocsRepo D:\UO\golems\Bronze\shard-migration`, 2026-10-20 10:30. Neither repo BLOCKED. No file over 5 MB in either repo
(find -size +5M: none).

```
=== code  (D:\UO\golems\Bronze\ShatteredLegacy) ===
  15 file(s) pending:
    CHANGELOG.md
    VERSION
    server/customizations/ClusterFAccountData.cs
    server/customizations/ClusterFDevTools.cs
    server/customizations/ClusterFGuildSystem.cs
    server/customizations/LeagueRegistrarGump.cs
    server/customizations/Requisitions/Appraiser.cs
    server/customizations/Requisitions/RequisitionData.cs
    server/customizations/Requisitions/RequisitionItems.cs
    server/customizations/Requisitions/RequisitionLeads.cs
    server/customizations/Requisitions/RequisitionSystem.cs
    server/customizations/Requisitions/RequisitionTable.cs
    server/customizations/Requisitions/RequisitionsBoard.cs
    server/tests/Misc/AccountDataSerializerVerification.cs
    server/tests/Misc/RequisitionsVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\golems\Bronze\shard-migration) ===
  1 file(s) pending:
    notes/cc-P150-requisitions-and-leads.md
  dry run: would add, commit and push
```

This note is the second pending file in docs once saved. No test-shard, package or haven lock was needed (P150's Touches
line says haven, but its diff holds no Haven file, and nothing here deployed anything); nothing was placed in any world
and no config was changed.

P203 DONE
