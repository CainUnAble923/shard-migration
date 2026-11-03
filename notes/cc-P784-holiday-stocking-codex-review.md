# Codex review: P784

CC task P784: holiday stocking at the winter Festival stall. Reviewed by Codex (`codex exec review`, read-only) after P784 DONE and before the Golem's commit, 2026-11-03 06:53.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The implementation covers most requested functionality, but does not enforce continuous holding still and can throw on malformed configuration instead of rejecting it. Build and test results were inspected in the task notes, not independently rerun.

- **medium** [P2] Reject null prize rows without throwing (`server\customizations\HolidayStocking\HolidayStockingTable.cs:225`)
  If the configuration contains a null prize entry, such as `"prizes": [null]`, JSON deserialization succeeds but validation throws when accessing `row.ItemType`. Because neither `Parse` nor its callers catch this exception, a malformed configuration can interrupt startup or throw from the reload command instead of being refused while retaining the current table. Validate null entries before dereferencing them.
- **medium** [P2] Track movement throughout the hold-still interval (`server\customizations\HolidayStocking\HolidayStocking.cs:176`)
  A player can start grabbing, walk away, and return to the original tile before six seconds expire and still receive the reward. Comparing only the final position does not enforce the requested six seconds of holding still. Track movement during the interval and cancel the attempt on the first move; include an out-and-back case in the tests.

(1.2 minutes, 257,266 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The submitted probe bypasses the explicitly required build/test route and can report success after build or test failures. This review covers the documentation repository changes, not the implementation in the separate code repository.

- **medium** [P2] Run red/green probes through the required build gate (`notes\cc-P784-tools\probe.sh:19`)
  The prompt requires building and testing only through `docker/uo/build.sh`, but this helper invokes `dotnet build` and `dotnet test` directly against an older builder image. It also continues after compilation failures and masks failed tests behind `grep` exit statuses; `red-probe.txt` demonstrates it running a stale assembly with no matching tests after compilation failed. Route these probes through the required gate and preserve failure exit codes so the recorded red/green evidence verifies the changed code. This also follows [AGENTS.md:341???347](../../AGENTS.md#L341-L347), which explicitly requires gates to demonstrate failures rather than convert them to success.

(0.7 minutes, 210,887 tokens)
