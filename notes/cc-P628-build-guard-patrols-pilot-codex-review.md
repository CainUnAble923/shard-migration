# Codex review: P628

CC task P628: build guards that patrol and see, pilot town. Reviewed by Codex (`codex exec review`, read-only) after P628 DONE and before the Golem's commit, 2026-10-25 23:48.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The change supplies the ordered stage-one recorder, tests, changelog and remaining-stage drafts, but its witness evidence can misrepresent what was observed and its test-only restriction is not enforced. The notes report a successful build; that build was not independently rerun during this read-only review.

- **medium** [P2] Enforce the test-shard restriction before enabling observation (`server\customizations\ClusterFGuardWitness.cs:387`)
  An administrator can execute `[GuardWitness on` on the live shard as well: registration is unconditional and this branch performs no runtime shard check. `ShardCommandAttribute` supplies descriptive metadata for tooling and tests, not execution enforcement. Consequently, the advertised test-only restriction does not satisfy the prompt's explicit never-live boundary. Reject activation outside the test shard and add a test for that rejection.
- **medium** [P2] Deduplicate callbacks without merging distinct offenses (`server\customizations\ClusterFGuardWitness.cs:240`)
  If one culprit commits two distinct offenses within one second, this merges them regardless of victim, kind or location. Witnesses of the second offense are then attached to the first offense's location, time and potentially unrelated victim; subsequent reports therefore attribute evidence they never observed. The design requires genuinely new offenses to create new incidents. Deduplicate callbacks belonging to the same action rather than every action by the same culprit within a time window.
- **medium** [P2] Check visibility of the action location when recording witnesses (`server\customizations\ClusterFGuardWitness.cs:280`)
  For aggression or criminal assistance, a witness can see the culprit without seeing the victim or the action's location, for example across a building corner. `Record` always passes `culprit.Location` to `Sees`, so its separate action-location check never runs through the gameplay hooks. This records witnesses who did not see the action, contrary to the requested witness contract. Pass the relevant action location through the hooks and test this through a real crime callback.

(1.2 minutes, 310,676 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.83). The only change in this repository is the new P628 note. It documents the design???s first-stage witness contract, reported red/green tests and gated build, and includes all eight remaining prompt drafts. No actionable defect was found in this diff; the server implementation and reported test results cannot be independently verified from this notes-only change.

No findings.

(0.4 minutes, 135,913 tokens)
