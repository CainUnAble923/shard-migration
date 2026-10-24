# P524: review of P370 Golem build and reclaim fixes

Reviewed 2026-10-24. Docs only. No code changed.

## Scope

P370 is in local code `main`: implementation task commit `91d122b`, merge `f2853e8`. Its notes are in local docs `main` at `621e0cc`. The code commit contains only `CHANGELOG.md` and `VERSION`; the implementation was installed outside Git in `D:\UO\golem`, as the P370 notes explain. This review reads that installed implementation and compares its changed scripts with their `.bak-20261024-P370` backups. An exact versioned implementation snapshot in `main` could not be verified.

Read `cc-P370-golem-fixes-flaky-builds-reclaims.md` and its adjacent Codex review first. That review reported no findings and explicitly left the installed kit unverified. Neither finding below repeats an earlier finding or the follow-ups already recorded in P370.

Files reviewed: `D:\UO\golem\Golems.ps1`, `golem.ps1`, `Answer-Question.ps1`, `Remote-Agent.ps1`, `Clear-Golem.ps1`, the P370 README changes, and `tests\Golem.Tests.ps1`'s P370 facts and relevant fixture helpers; the repository's P370 `CHANGELOG.md` and `VERSION` changes; `docker\uo\build.sh`; and the relevant merge commit flow in `D:\UO\Commit-ShardWork.ps1`. Locations below refer to the installed files read during this review.

## Findings

1. **bug: the original can be reclaimed before its fix-up merges.** `D:\UO\golem\Golems.ps1:638` and `:652`. A failed original remains in `claimed\`, but the new stale-claim guard only protects work already in main. If its fix-up is still queued, running, or waiting to merge when the original ages out, the original goes back to `queue\` and another eligible Golem can start it again; there is no pending-ticket or fix-up check before that move. Suggested fix: retain originals with an unresolved merge ticket or fix-up, or move them into an explicit waiting-for-merge state that stale-claim release does not recycle. Add a case where the original ages out while its fix-up is still queued, before testing successful fix-up completion.

   Evidence: an isolated call to the installed `Release-StaleClaims` with a five-hour-old original and a queued fix-up produced `originalRequeued=True; fixupStillQueued=True; completed=False`. The existing fact at `tests\Golem.Tests.ps1:4249` tests cleanup after the fix-up merges, but does not test this waiting interval. The candidate selection at `Golems.ps1:438` does not exclude an original because its fix-up exists.

2. **bug: a partial merge across the two repos is treated as completed.** `D:\UO\golem\Golems.ps1:591`, consumed at `:638`. `Find-PromptWorkInMain` returns on the first matching commit in either repo, so a code merge alone makes stale-claim release archive the original even if its docs changes never merged. This is a reachable failure state: `D:\UO\Commit-ShardWork.ps1:169` commits and pushes repos separately, continues after a failure, and does not undo the first repo's commit; `Golems.ps1:1391` resets to `HEAD`, which retains an already committed merge. Suggested fix: require a successful integration receipt, or verify the expected branch head in every repo changed by the ticket before completing the original. Add a partial-merge case where only one changed repo contains the task and the other remains outstanding.

   Evidence: the installed helpers, with mocked Git responses representing a matching merge in code and no merge in docs, produced `originalCompleted=True; docsGitQueries=0; completed=True`. The existing stale-claim case at `tests\Golem.Tests.ps1:4263` supplies a successful match in one repo and expects completion; it does not cover unfinished changes in the other repo.

## Verification and limits

Behavior probes ran under `powershell.exe` 5.1.26100.9711 using functions extracted from the installed library, temporary fixture folders, and mocked Git responses. No actual Git mutations or network calls ran in those probes. The scratch driver is `%TEMP%\P524-review-probes.ps1`; its fixture folder is `%TEMP%\P524-review-c6a0dc1a`. A separate failed-fetch repair probe confirmed that checkout and reset are still attempted after fetch fails; that observation alone is not listed as a defect because it did not establish an additional failure beyond P370's documented reset policy.

No additional actionable retry defect or reproduced leaked-lock case was found. The reviewed retry path makes at most two build calls, preserves both attempts, and keeps a second failure red. This is source inspection, not a real Docker build or a concurrency test. The full Golem suite and the shard build were not run; no regression tests were added. No Haven connection, deployment, commit, push, or branch switch was made.

The required progress check ran with workspace path overrides and `--dry-run`. It still rewrote `tools\progress.json`; that generated file was restored byte for byte from its initially clean Git version. Final scope is the new review note only.

Final checks: code work copy clean; docs work copy contains only this new note; `git diff --check` passed; the note is ASCII, has no trailing whitespace, and is below 5 MB. No stop request was present at the final check.

P524 DONE
