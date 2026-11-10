# Codex review: P859

CC task P859: port the Horn of Plenty, Mister Gobbles and the roasting pig. Reviewed by Codex (`codex exec review`, read-only) after P859 DONE and before the Golem's commit, 2026-11-10 11:33.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The port largely implements the requested content, with store availability, donation integration, tests and client-proof artifacts. However, recharge loses elapsed daily charges and overlapping nap timers end freezes prematurely. Build results were not independently reproduced during this read-only review.

- **medium** [P2] Prevent nap timers from clearing another freeze (`server\customizations\Items\Thanksgiving\HornOfPlenty.cs:182`)
  Players can use the horn again while frozen, so two nap outcomes create independent timers: the first timer clears Frozen before the second ten-second nap finishes. The unconditional assignment can also clear a freeze owned by another system. Coordinate the nap lifetime and freeze ownership, and test overlapping naps and expiry rather than only asserting that Frozen initially becomes true.
- **medium** [P2] Restore all charges earned during elapsed November days (`server\customizations\Items\Thanksgiving\HornOfPlenty.cs:86`)
  If an emptied horn is left unused from November 1 until November 10, it recovers only one charge instead of the accumulated daily charges. No timer calls this method, and resetting NextRecharge to tomorrow discards every other elapsed day. Calculate the eligible November recharge intervals and advance the saved deadline accordingly, capped at ten charges. This also preserves the refill behavior required by the [fidelity principle](AGENTS.md#L169-L173).

(1.5 minutes, 425,249 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The submitted proof runner masks failures and bypasses the required build route for red/green verification. The notes record a successful final gated build and client evidence, but the server implementation itself is outside this repository's review scope.

- **medium** [P2] Preserve failures in the red/green proof runner (`notes\cc-P859-tools\probe-inner.sh:18`)
  When compilation or a test fails, this runner can still exit successfully: the build pipeline returns `head`'s status, and the test status is overwritten by the subsequent output filters. A failed build also proceeds to `dotnet test --no-build`, potentially testing stale assemblies. Thus the recorded red run does not demonstrate a failing gate. Run the red/green proof through the task-required `docker/uo/build.sh` route and verify its nonzero/zero exit statuses, consistent with [AGENTS.md:339???343](../../AGENTS.md#L339-L343).

(1.1 minutes, 291,134 tokens)
