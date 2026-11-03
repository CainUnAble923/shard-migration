# Codex review: P787

CC task P787: beekeeping (apiculture). Reviewed by Codex (`codex exec review`, read-only) after P787 DONE and before the Golem's commit, 2026-11-03 09:21.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The implementation substantially covers the requested beekeeping loop, but lockdown bookkeeping, cap enforcement, and configuration handling contain actionable defects. Build results were documented in the task notes; I did not independently rerun the build or verify behavior in a client.

- **medium** [P2] Reject or normalize null configuration collections (`server\customizations\Beekeeping\BeekeepingTable.cs:361`)
  A configuration containing `"candles": null` passes validation because this loop substitutes an empty collection without updating `t.Candles`. `Reload()` then installs the table and throws on `table.Candles.Count`; startup recipe registration also dereferences the null collection. `beekeeper` has the same problem. Reject these values or normalize the properties before accepting the table so a malformed configuration preserves the previous working configuration instead of breaking startup or reload.
- **medium** [P2] Enforce the hive cap when released hives are locked down again (`server\customizations\Beekeeping\HouseBeehive.cs:661`)
  The cap only applies when using a deed. An owner can release existing hives, place more deeds while `HivesIn` excludes the released hives, and then use the ordinary house lockdown command on all of them. `BaseHouse.LockDown()` has no beekeeping-cap check, and `CheckDue()` accepts every resulting hive, allowing unlimited productive colonies up to the general storage limit. Enforce the limit on reactivation as well as deed placement.
- **medium** [P2] Release the lockdown before packing up the hive (`server\customizations\Beekeeping\HouseBeehive.cs:632`)
  Packing up a locked-down hive deletes it without removing it from the house's `LockDowns` list. Pinned ModernUO's `BaseHouse.GetLockdowns()` counts these entries even when their items are deleted, so each placement/packing cycle consumes another lockdown until cleanup or reload. Release the hive through the house before deleting it, and test that packing restores the original lockdown allowance.

(2.3 minutes, 991,588 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.8). No actionable defects found in this repository's new plan, completion notes, and verification artifacts. The supplied results support the reported green build and mutation checks; the server implementation and CHANGELOG/version changes are outside this diff and were not independently verified.

No findings.

(0.6 minutes, 167,009 tokens)
