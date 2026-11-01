# Codex review: P714

CC task P714: build the Chivalry and Necromancy initiation gates and the shorter start-skill list. Reviewed by Codex (`codex exec review`, read-only) after P714 DONE and before the Golem's commit, 2026-10-31 22:10.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The implementation covers much of the requested functionality, but training can bypass initiation through the existing test-bank refill, pet combat does not earn quest credit, and persisted mode overrides configuration. Runtime tests and the external P714 notes were not verified.

- **high** [P1] Preserve school restrictions when refilling the test bank (`server\customizations\ClusterFSchoolGate.cs:333`)
  On the test shard, an uninitiated player can run `[TCFill` to bypass the training restriction. `TestCenterKit.RefillBank` calls stock `TestCenter.FillBankbox`, which sets both schools' caps to 120, and preserves those raised caps. NPC teaching, Transcendence scrolls and soulstones then accept points without permission. Reapply the school restrictions after refills or enforce permission at those assignment paths; login/load cap enforcement alone is insufficient.
- **medium** [P2] Apply the configured gate override after loading persisted mode (`server\customizations\ClusterFSchoolGate.cs:130`)
  After the first save, changing `clusterf.schoolGates.enabled` can have no effect on restart. `Configure` applies the setting before `World.Load`, but deserialization subsequently overwrites it with the previously saved mode here. For example, a saved `auto` mode overrides an explicit `off` configuration on the test shard. Resolve the configuration override after persistence loads, or keep configured and persisted command modes separate.
- **medium** [P2] Count damage dealt by the initiate's pets (`server\customizations\ClusterFInitiation.cs:610`)
  When an initiate fights using only a pet, neither condition credits the kill: `LastKiller` is the pet, and `FindDamageEntryFor(pm)` searches direct damage entries only. ModernUO records the master's contribution inside the pet entry's `Responsible` collection. Consequently both quests reject pet-only combat despite explicitly telling players that a pet will do. Include controlled/summoned damage-master participation in this check.

(1.5 minutes, 1,002,603 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The added probe masks failing test exit codes. This work copy contains notes and supporting artifacts only, so the server implementation and its fulfillment of the gameplay requirements could not be verified from this diff.

- **medium** [P2] Propagate test failures from the probe container (`notes\cc-P714-tools\probe714.sh:27`)
  When `dotnet test` fails, the container still exits successfully because the inner Bash pipeline returns `grep`'s status, and failure output contains non-warning lines. This makes failed probes appear successful to callers. Enable `pipefail` inside the container or explicitly propagate the test process's status; setting it only in the outer script is insufficient. This also conflicts with the failure-sensitive verification requirement in [AGENTS.md:339???347](../AGENTS.md#L339-L347).

(0.6 minutes, 190,685 tokens)
