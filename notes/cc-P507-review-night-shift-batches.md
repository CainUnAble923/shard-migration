# P507: review of night shift batches (P156)

## In plain words

- A repeated night shift trigger can remove the budget stop or open another session for the same task.
- A delayed trigger can start work at noon, and turning night shift off does not cancel its pending checks.
- This review changes no code. A later task can fix the findings and add the missing tests.

## Scope

Reviewed on 2026-10-23. P156's code commit `6f3370b8f5a9b98ec2d9a2d08977263f57a938ad` is an ancestor of code main (`579ad58f8f478280b03b8cf80f1ee9a5b3001a27`), merged by `9ccce19`. The console implementation and test have no differences from main in this work copy.

Read `notes/cc-P156-night-shift-batches.md`; no separate P156 review was found beside it. The findings below do not repeat its reported test failures or acknowledged timing and usage limits.

Files reviewed: `D:\UO\golem\golem.ps1`, its P156 settings defaults and related settings reads, `D:\UO\golem\tests\Golem.Tests.ps1`, `D:\UO\golem\README.md`, `D:\UO\golem\Set-NightShift.ps1`, and code main's `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`, `CHANGELOG.md`, and `VERSION`. Golem kit paths below refer to the current files outside the repos, which include later changes; their historical P156 contents are not independently versioned by the code commit.

## Findings

1. **bug**, `D:\UO\golem\golem.ps1:2254`: Repeating NightShift within two minutes while the first session is opening creates a second batch, then the duplicate-wake refusal resets `nightShift.batch` to zero and removes `longRun`, leaving the first session without its budget or night-end guard. Preserve the existing batch when a wake is refused, and add a regression that starts its prompt after the refusal and verifies both the budget stop and the end-of-night handoff.

2. **bug**, `D:\UO\golem\golem.ps1:3969`: Repeating NightShift after two minutes while the first session has not set `current` starts another batch and launches a second session for the same prompt, because `Get-NightGate` checks neither the active batch nor a session still opening and the wake duplicate guard has expired. Make repeated triggers harmless while a batch or launch is active, check and reserve that state under the lock, and add a delayed-session regression across the two-minute boundary.

3. **bug**, `D:\UO\golem\golem.ps1:3961`: A NightShift event delivered at noon rolls the expired end forward to tomorrow and opens a batch immediately, so the scheduled task's `StartWhenAvailable` catch-up can run outside the configured 22:30 to 06:30 hours. Require the event time to fall inside a configured night window before opening it, and test catch-up both during the window and after its end.

4. **bug**, `D:\UO\golem\golem.ps1:4219`: Watch still invokes a pending check after `nightShiftEnabled` becomes false, and `Invoke-NightCheck` never checks that setting, so turning night shift off between batches can still launch another session. Recheck the enabled setting before every batch start and cancel pending checks when it is turned off, with a regression that disables an already-open window before its next check.

## Verification and missing coverage

Used Windows PowerShell **5.1.26100.9711**. Existing tests passed:

- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\Golem.Tests.ps1 -Only P156_`: all six named P156 facts, 43 checks passed, zero failed.
- `scripts/tests/Shard-Console.Tests.ps1` with `SL_FACT_FILTER=^P156_`: `P156_TheNightShiftLineShowsTheBatchItsBudgetAndTheNextCheck` passed.

Read the P131 night facts and the P156 facts at `D:\UO\golem\tests\Golem.Tests.ps1:3087`, `:3112`, `:3149`, `:3162`, `:3173`, and `:3194`. They do not exercise the four sequences above; in particular, the disabled case starts with night shift already off, and the end-of-night cutoff case stays inside an otherwise valid night window.

Additional fixed-clock probes reused the suite's fixture helpers, stub CLI, stub commit script, temporary roots, and `-NoMail`; helper definitions were loaded into memory, with no test file added or changed. Observed results:

| Sequence | Result |
|---|---|
| Start at 22:30, repeat at 22:31 before a session reports | One CLI launch, one unfinished batch record, but active batch zero and no long run. |
| Register P101 after that refusal, report week 48% and session 51%, Watch at 22:40 | P101 remains current with no winding request and no STOP-REQUESTED, despite the original 47.1% week and 50% session limits. |
| Repeat the refusal sequence, then finish P101 at 06:40 with fresh usage under the limits | P102 is handed on after the configured 06:30 end because the long run was removed. Only the fixture's stub commit script ran. |
| Start at 22:30, repeat at 22:33 before a session reports | Two CLI calls for P101, two session-book launch records, and two batch records with neither earlier batch closed. The asynchronously written CLI log was read again after both calls completed. |
| Deliver NightShift at 2026-10-18 12:00 with usage under the limits | One CLI launch; window starts at noon and ends 2026-10-19 06:30. |
| Fail the 22:30 check on usage, set nightShiftEnabled false, lower usage, Watch at 23:00 | One CLI launch and batch 1, even though status reports night shift disabled. |

Actual overlapping model sessions and a live overnight run remain unverified. No real CLI session, mail delivery, Haven connection, deployment, or commit was performed; no full-suite result is claimed. No additional finding was found in the console display change.

P507 DONE
