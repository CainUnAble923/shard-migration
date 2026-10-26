# Codex review: P630

CC task P630: build the Mythril Echo summon reward, stage 1. Reviewed by Codex (`codex exec review`, read-only) after P630 DONE and before the Golem's commit, 2026-10-26 00:45.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The stage-1 implementation and accompanying notes largely match the requested scope, but the test-only command is usable on live and harmful actions do not consistently enforce owner eligibility. Build results are documented in the notes; I did not independently rerun the Docker gate.

- **medium** [P2] Recheck owner eligibility before permitting harmful actions (`server\customizations\Mobiles\LeagueEchoes\LeagueDragonEcho.cs:134`)
  Between watchdog ticks, an Echo can continue attacking after its caller enters a forbidden region, exceeds the leash, loses rank, enters a duel, or the feature is disabled. This override checks only the Echo's location and the owner's ordinary harmful-action permission, which does not enforce those Echo-specific restrictions; a missing or deleted owner even skips that permission check. Apply the lifetime eligibility checks here and refuse harm/dissolve immediately when they fail, as the design requires before harmful actions rather than only once per second.
- **medium** [P2] Enforce the test-shard restriction inside the command handler (`server\customizations\LeagueEchoes\LeagueEchoSystem.cs:332`)
  On a live shard, a GameMaster can type `[LeagueEcho on` followed by `[LeagueEcho call` and enable this unfinished feature. `ShardCommand(TestOnly)` is metadata: `ClusterFStaffHub.CanRun` enforces it for hub actions, but typing the command invokes the handler directly through `CommandSystem.Handle`. Add an actual test-shard check before allowing these mutations so stage 1 remains test-only as requested.

(1.6 minutes, 622,188 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.86). The only change here is the P630 note, which documents stage 1, verification claims, limitations, and the remaining prompt drafts, ending with the required DONE line. No actionable defect was found in this repository's change; the server implementation and reported build results are outside this diff and were not independently verified.

No findings.

(0.7 minutes, 165,511 tokens)
