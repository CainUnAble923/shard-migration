# P699 lane notes: review of P673

2026-10-27, Golem Codex lane, Verite work copies.

Requested deliverable: `notes/cc-P699-review-p673.md`. This companion uses the Notes path named by the lane wrapper. Both contain review notes only.

Read AGENTS.md in both work copies before substantive work, then the governing index, direction record and task list. Reviewed P673 and P669 against their tools/data, author reference data and canonical customizations plus pinned ModernUO source. The review preserves Chase's choice of engine and both-facet map replacement.

The report assigns severity and fixes to release-set gaps, world conversion, package Gate 4/admission, map precedence/parity, omitted coordinates and training behavior, shared terrain protections, wave conflicts, dungeon sealing, placement validation, site A qualifications, task sizing and SOS validation. It gives a corrected release sequence without changing the implementation plan or choosing Chase's outstanding options.

Only this companion and the requested review are intended changes. No code, maps, docs/, live services, accounts or saves changed. No commits, branch changes, builds or deployments. No Haven connection. Lane tests: none; no new tests added.

Review scope and verification details, including what could not be verified, are in the report's Evidence and limits section.

Final preflight: Windows PowerShell 5.1.26100.9711; both repos passed git diff --check; only these two new notes remain in git status. The report has fifteen numbered findings, each with severity and a fix. Both files are under 5 MB, have no trailing whitespace and contain no em dashes. The code work copy is clean. The stop-request file was absent at each step and the final check.

Ran tools/progress.py --dry-run with SL_SHARD and SL_MIGRATE pointing at these work copies; exit 0. Discovered that build() writes tools/progress.json before main() checks --dry-run (tools/progress.py:722,732-737). Restored that generated file to its original HEAD bytes and verified it no longer differs. Git restore could not acquire the external worktree index lock under this lane's permissions, so the restoration used read-only git show and a direct write to the permitted work-copy file. No index or branch was changed. This existing dry-run side effect is an incidental tool defect for follow-up, not fixed in this notes-only task.

P699 DONE
