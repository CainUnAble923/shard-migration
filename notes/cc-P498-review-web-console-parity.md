# P498: review of web console parity (P187 and P182)

Reviewed on 2026-10-23 in the Valorite work copies. Review only; no code or test files changed.

P187 (`256c4a751191a9d3b2054f8fd416c78a4a609264`) and P182 (`9ad22c5043f1fdd4354a62f6ed51697cb74fdd23`) are ancestors of local code `main`, reviewed at `579ad58f8f478280b03b8cf80f1ee9a5b3001a27`. The reviewed files match main. Read both AGENTS.md files, direction-decision.md, tasks.md, cc-P187-cont-web-console-parity.md, and cc-P182-cont-web-console-phase2.md first; no separate P187 or P182 review was found beside those notes. Findings below do not repeat the implementation notes' recorded limitations or test failures.

## Findings

1. **bug** - `web-console/server.py:559`: Token lookup, consumption, and job admission happen in separate critical sections, so two requests can both validate one token and both run if the first job finishes before the second checks for a busy job. Consume the token and reserve the job atomically, and add a concurrent replay test that requires exactly one launch.

2. **bug** - `scripts/Shard-Console.ps1:5963`, `web-console/server.py:542`: Roll back resolves the newest good image independently during preview and execution, while the token stores only the empty caller inputs and the unchanged phrase, so the accepted run can target an image the user never reviewed. Bind the preview to the resolved image ID and refuse a changed target until another preview, with a regression test that adds a newer good image between preview and run.

3. **bug** - `web-console/server.py:1812`, `scripts/Invoke-WebConsoleAction.ps1:164`: The picker disables other Golems when `multiGolem` is false, but the action handler and runner do not enforce that setting, so an already open page or direct authenticated POST can still dispatch their actions. Apply the same eligibility check at dispatch and again in the runner, and test rejection for both local and remote Golems after switching multi-Golem mode off.

4. **risk** - `web-console/server.py:382`: The timeout kills only the runner process, leaving child commands able to continue after the job is marked idle, and on Windows the observed exit code of 1 also leaves the displayed result without a timeout warning. Supervise the process tree with a Windows Job Object or equivalent cancellation mechanism, explicitly record the timeout, and test a runner that starts a child before hanging.

5. **risk** - `web-console/server.py:402`, `web-console/server.py:430`: The action audit is written only after execution and every audit write error is silently discarded, so a console action can complete successfully without its user, inputs, and result reaching actions.log or the Timeline. Persist a start record before launching a changing action, surface audit failures, and add tests for an unwritable log and an interrupted run.

## Evidence and checks

- The single-use token probe used the real `start_page_action` and `_start_job`, with a harmless job stand-in and a forced thread interleaving after both token lookups: both requests returned 202 and two jobs launched from one token.
- A Windows PowerShell 5.1 probe called the real `Get-WebPagePlan` and `Get-LastGoodImage`, with only `Get-ActionPlan` replaced by a recorder: preview selected `sl-modernuo:good-aaaaaaa`; after adding a newer image, execution selected `sl-modernuo:good-bbbbbbb` and returned `Ok=True` for the same inputs and phrase. No plan was executed.
- The real loopback HTTP handler with the existing fake runner reported Bronze's picker row as `usable=False` with `multiGolem=false`, then accepted `rest bronze` with HTTP 202 and invoked the fake runner once. The PowerShell dispatch path scopes the Golem's files without calling the desktop's `Get-GolemActionConfig` eligibility check.
- A harmless Python runner started a child that wrote a synthetic marker after the parent's 0.3-second timeout: the job became idle with code 1 and result `parent running`, and the surviving child wrote its marker afterward. No shard, Docker, Golem, or deployment command was run.
- Pointing a synthetic action's audit target at an existing directory reproduced an unwritable log: HTTP 202, exit code 0, successful result, and no audit record or surfaced logging error.
- Existing Python tests passed: 32 tests from `web-console/tests/test_actions.py` (`Proof`, `LiveActions`, `ProofForwarder`) and `web-console/tests/test_pages.py` (`Pages`, `Parity`). These cover authentication, checked inputs, confirmation words, sequential token reuse, busy actions, output, logging, lists, and registry parity; they do not cover the failing scenarios above.
- Initial fixture setup failed with PermissionError because Python's temporary directories lacked usable inherited permissions, including inside the work copy. The successful run used an in-memory `tempfile.mkdtemp` adapter that created fixture directories with inherited permissions under `scripts/shard-console-cache/P498`; no production or test source was modified.
- Read the relevant P182 and P187 PowerShell facts and their fixtures, the runner and list script, console planning and safety functions, both action registries, server and authorization code, installer, proof proxy and sidecar configuration, and browser action and confirmation handlers. No new authentication bypass or action that selects the wrong shard was found in those paths; the rollback finding concerns an image target on the test shard.
- `tools/progress.py --dry-run` completed against these work copies. Its unconditional generated progress.json write was intercepted in memory so this review changes only this note.

## Limits

No Haven connection, real service action, deployment, build, account change, or Golem control was attempted. Installed service behavior, real Tailscale forwarding and login-header replacement, browser interaction, the full PowerShell fact suite, and actual shard operations remain unverified in this review. Python HTTP checks used throwaway loopback listeners and synthetic proof and login values; all new probes demonstrated current behavior, with no fixes made or claimed.

Scratch fixtures remain under the git-ignored `scripts/shard-console-cache/P498` directory, verified with `git check-ignore -v`; they contain synthetic data only and no file exceeds 5 MB. Python bytecode is also ignored. No commits, merges, pushes, or branch switches were made.

P498 DONE
