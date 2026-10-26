# Codex review: P629

CC task P629: build League reward tokens (warrants), stage 1. Reviewed by Codex (`codex exec review`, read-only) after P629 DONE and before the Golem's commit, 2026-10-26 00:08.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.9). The catalog, guarded item skeleton, tests and remaining-stage drafts largely match stage 1. However, the seeder lacks the requested test-world restriction. The notes report a green build; I did not independently rerun it.

- **medium** [P2] Restrict investigation marker placement to the test shard (`server\customizations\LeagueInvestigations\LeagueInvestigationSeeder.cs:24`)
  On a live shard, an administrator can run this command and place investigation markers even while investigations are disabled: `Seed` never checks `ClusterFStaffHub.IsTestShard`, and `Settings.Enabled` is not consulted. The `TestFirst` annotation is descriptive metadata and explicitly permits eventual live use, contrary to this prompt's test-world-only requirement. Add a server-side test-shard refusal before placement and declare the command `TestOnly`.

(1.1 minutes, 330,947 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.88). The only change in this repository is the new P629 notes file. It documents stage 1, red/green and build results, verification limits, and the remaining-stage prompt drafts. No actionable defects were found in this documentation; the server implementation and reported test results were not independently verified in this review.

No findings.

(0.3 minutes, 114,458 tokens)
