# P622: work record

The requested report is [cc-P622-codex-findings-to-fixes-7.md](cc-P622-codex-findings-to-fixes-7.md). This separate work record uses the filename required by the unattended wrapper.

## Delivered

Drafts U1-U7 and W1-W8 cover the uncovered findings in the in-range implementation reviews. A1-A2 add suppressed-mail durability, normalized mail modes and complete question content to the existing P533 W15/W12 owners. C1-C2 preserve unresolved High Seas acquisition scope; C3 rejects the unsupported confirmed-bug interpretation of the filename fallback while retaining an optional portability proposal.

The verdict table accounts for every labeled primary-review finding and the actionable adjacent implementation-review findings. P587's Hammer review and separate High Seas merge fix-up are identified separately. P610-P613's already implemented work, the older unissued scopes, queued P478/P623, and existing policy IDs retain their ownership. Guide and design content was excluded as requested.

## Verification

Read both work-copy AGENTS.md files and required direction/task/index guidance. Source snapshots, input inventory, prompt-catalog fingerprint and limits are in the report. Ripgrep is unavailable; searches used PowerShell and Python over named source/catalog directories. The shell is Windows PowerShell 5.1.26100.9711.

Lane tests: none. No tests or gates were added. Drafted test cases and mutations are future implementation instructions, not results. Source inspections and the retained Alembic still were checked locally. No code or historical findings were edited; no external service was contacted.

The report contains 15 complete prompt blocks, with the explicit list U1-U7 and W1-W8 beside that count. Each has metadata, concrete acceptance criteria, notes destination and a placeholder completion marker. The input inventory names every included primary/adjacent review; the excluded adjacent-review finding scan found no overlooked actionable finding. All named input files and relative links resolve. ASCII, no em dashes, trailing whitespace, table structure, balanced fences, final newlines and size checks passed. Both files are below 5 MB. Git whitespace checks included the untracked files explicitly; no whitespace diagnostics were emitted. The no-index check's normal new-file difference status was distinguished from a whitespace error.

The prompt catalog changed only when P273 was reassigned to Iron and claimed. The report records both fingerprints and the read-only reconstruction that isolates that change. The final catalog was checked for new overlapping fixes. No prompt files were written.

The required progress reporter exited 0 with --dry-run and SL_SHARD/SL_MIGRATE pointing to these work copies. A process-local Path.write_text guard suppressed only its known unconditional tools/progress.json write; unexpected Path.write_text destinations would have failed. No reporter tool was edited. The original progress.json remained byte-identical, SHA-256 `6e5b59e3eb78dce0c6c7fe5229b76a7c710c4ef22c6ae3f1ea8807472a13507e`. It recognized version 2026.10.25.7. Its general status prose and content totals are not verification results for this drafting task. P533 W24 retains the reporter fix.

Installed-kit source hashes recorded after source inspection, SHA-256:

| Read-only source under D:/UO/golem/ | SHA-256 |
|---|---|
| DockerPrune.ps1 | 88c39f8cae933b5ddb6f4f0cfcefd6f10d06074f12b1b2109b9ee66c497c551c |
| Use-GolemLock.ps1 | 757366c3d7baffbcc145b02914c30b4486a962d900d6c17856414dfc6a0d2ce8 |
| Golems.ps1 | 4047692f91514faf4cd72233182adbe1e8641bcaa89d0d4a152f79937145a100 |
| TinkerLib.ps1 | f3d0b1e72c133395a2acfab3a94fea9c009f9fb10b138ef9208735de7c1cc7fa |
| TinkerMail.ps1 | aacef49112a6fbaedd6c8bf8812d45c615e58e4b47928642182b2b8e9da9c60a |
| golem.ps1 | 59eea6e7eee45642d3601a268275b31efaa44e60a821b13177c94f58e9ac5e52 |

Both work-copy HEADs stayed unchanged, the code work copy is clean, and the only notes changes are the requested report and this work record. No docs/, guide, code, service, configuration, real lock, account or save was changed. No Haven connection, deployment, mail send, Docker operation, commit, merge, push or branch switch occurred. Stop requests were absent at the checked step boundaries.

All requested review reconciliation, drafting and validation are complete. Proposed implementation, policy decisions and client/runtime proof remain future work as labeled in the report, not unfinished P622 work.

The final input-inventory, table/fence/link, draft-completeness, whitespace, size, catalog-fingerprint, HEAD and changed-file checks passed. The final stop-request check was absent.

P622 DONE
