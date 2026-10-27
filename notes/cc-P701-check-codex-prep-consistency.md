# P701 lane notes: SoS preparation cross-check

October 27, 2026. Requested report: [cc-P701-prep-cross-check.md](cc-P701-prep-cross-check.md).

Read AGENTS.md in both assigned work copies first, followed by the direction
record and task list. Work remained notes-only and preserved the ModernUO and
both-facet SoS decisions.

The work-copy checkout contained P673 but none of the P692 through P699 output
paths. All eight prep result commits were available locally. Read their exact
snapshots using git show, with full commit hashes and input paths recorded in
the report. No merge, restore of prep files, branch switch or network fetch was
needed. Extracted review copies are scratch only, beneath
notes/__pycache__/p701-prep, proven ignored by git check-ignore before writing.
Every extracted file was checked against the 5 MB limit.

Reviewed prep notes and data together, including native region rectangles,
rosters, teleporter endpoints, champion proposals, wiki drafts and stock-spawn
plans. Checked runtime semantics in pinned ModernUO and relevant canonical
sources. The report gives disagreements, fixes and owning prompts, identifies
checks that found no conflict, and lists what each currently Iron-assigned
swap prompt should consume. It also hands integration checks to the other
owners and the final playthrough. The queued briefs' October 27 at 06:30
decisions supersede older prep wording: fresh test world, Haven move, Blackthorn
move through P691 before 1.0, and closures. The report applies those decisions
without performing any of them. It also identifies the source-backed mismatch
between Blackthorn's 413 by 539 region and the proposed 261 by 176 Fold box.

No source prep was revised. No code or docs/ change, build, new test, live-world
operation, Haven connection, deployment, commit, merge, push or branch switch.
The report explicitly separates geometric evidence from unverified terrain,
runtime behavior and current online terms. Lane tests are none.

Ran tools/progress.py --dry-run with SL_SHARD and SL_MIGRATE set to the assigned
work copies. It reported 1,676 customization files, 176 patch files, and 1,801
tests in 264 files. These are its existing tree counts, not SoS readiness.
The reporter writes tools/progress.json even in dry-run mode. Preserved its
original bytes before running and restored them in a finally block; subsequent
git status confirms no generated snapshot change remains. Its output is in
the ignored scratch folder. No progress-tool fix is included.

Final preflight passed: 14 findings with fixes and owners; all 13 currently Iron-assigned swap prompts have a handoff row. Exact uncovered teleporter IDs were rechecked against both parsed region arrays. Both notes are below 5 MB with no em dashes or trailing whitespace. Both repos passed git diff --check. The code work copy is clean; the docs work copy contains only these two new notes. Stop-request checks between steps and at finalization found none. All requested work is finished.

P701 DONE
