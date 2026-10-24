# P514: feature queue audit, round 2, work record

October 23, 2026. Docs-only work in the two Valorite prompt work copies.

The audit requested by the task is
[cc-P514-feature-queue-audit-2.md](cc-P514-feature-queue-audit-2.md). This work
record uses the filename specified by the lane wrapper; the audit uses the filename
specified inside P514. Both are notes, with no edits under `docs/`.

Read both `AGENTS.md` files first, then P398's notes, its audit and review, the
direction decision, task list and document index. Compared every queue entry with
main's canonical source, relevant notes and decisions, and the changes since P398.
Both work copies started exactly at their local main refs. The audit records the
full snapshot hashes and the evidence for each entry.

Main findings:

- Old batch/ready labels still outlast built systems. Several other entries need
  an explicit split between a built foundation and pending scope.
- The tutorial core and all listed optional lessons are now implemented. F-35
  remains partial for actual progression and evo scope, with review defects noted.
- Guild-hall placement is now implemented for test use, with Maritime waiting.
  Proof used a private world copy; current shared-world placement is unverified.
- The October 23 League decisions resolve older chapter/milestone, shop, Lead,
  non-member payout, and utility-reward conflicts. The older individual entries
  still need those decisions reflected in their status lines.
- P398's missing veteran +50 reward finding is corrected: Chase withdrew that
  reward on October 2. It is stale queue wording, not work to implement.

The audit includes the requested entry/status/main/suggested-status table, source
references, changes to P398, unresolved differences and verification limits. No
code, docs, configuration or world state changed. No tests were added or run; the
task has no lane tests. No build, Haven connection, deploy, commit or branch change.

Final validation passed:

- Matched the complete F-1 through F-51 table, including dropped F-2, with no
  missing or duplicate entries; checked four columns per row.
- Checked cited source files and line bounds, reviewed queue references, and
  checked ASCII punctuation, trailing whitespace and the 5 MB file limit.
- Both repos pass `git diff --check`. Tracked files match the audited main refs.
  Code remains clean; only these two P514 notes are new.
- Ran progress.py --dry-run with SL_SHARD and SL_MIGRATE set to the work copies,
  exit 0. A process-local write guard suppressed its known progress.json write;
  the tracked JSON stayed byte-identical. No generated or reporter file changed.
- Stop-request checks remained clear through finalization. No implementation or
  lane tests remain to do for this notes-only task.

P514 DONE
