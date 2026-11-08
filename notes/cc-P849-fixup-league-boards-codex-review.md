# Codex review: P849

CC task P849: overseer fix-up for P827 (League building decoration): its build review said FAIL. Reviewed by Codex (`codex exec review`, read-only) after P849 DONE and before the Golem's commit, 2026-11-08 12:10.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The facing swaps and proof artifacts address the principal review findings, but the migration misses worlds seeded with P803's intermediate board positions. Those worlds retain the misplaced, wrong-facing boards. Build results were inspected in the supplied notes, not independently rerun.

- **medium** [P2] Migrate boards from P803's intermediate positions (`server\customizations\Requisitions\Appraiser.cs:338`)
  On a world previously seeded by P803, the main board remains at `(3662,2548,0)`, which is missing from this list. `MoveOldOfficeBoard` therefore ignores it, while the range-5 lookup finds it and prevents placement at the new spot; the exact-coordinate retag condition also leaves its wrong-facing art unchanged. The release diff has the same omission for P803's `(3458,2598,18)` position. Include each copy's intermediate position and test those upgrades so already-seeded worlds receive the fix, as required by [the building guide](D:/UO/golems/Iron/shard-migration/notes/guides/building-and-decorating.md#L358-L362).

(0.9 minutes, 335,570 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The renders demonstrate corrected board facings, and the supplied build logs report green gates. However, intermediate seeded layouts are not upgraded correctly, and the playbook still teaches the reversed mapping.

- **medium** [P2] Correct the reversed board mapping in the playbook too (`notes\map-building-playbook.md:205`)
  This newly added instruction still tells future decorators to use 0x1E5E on west walls and 0x1E5F on north walls???the exact mistake P849 fixes. It contradicts both the new wall renders and the corrected Bank/Guild rows, leaving a required read-first document directing agents to reproduce the defect. Swap these two mappings and reference the P849 render instead.
- **medium** [P2] Include P803's board locations in the load-time upgrade (`notes\cc-P849-tools\p849-release-isle-20261028.diff:379`)
  On a world previously seeded by P803, the release board remains at (3458,2598,18): this list only recognizes the original doorway location. The nearby-item lookup still finds that board, preventing placement at the new location, while the exact-coordinate retag condition prevents correcting its art. Main has the analogous omission for (3662,2548,0). Include both towns' respective intermediate locations and test upgrading those layouts, as required by the [existing-world upgrade rule](notes/guides/building-and-decorating.md#L358-L362).

(1.2 minutes, 612,070 tokens)
