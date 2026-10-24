# Codex review: P413

CC task P413: a bigger way into the Rootdeep Burrows: an ant-hill mound with a wide hole. Reviewed by Codex (`codex exec review`, read-only) after P413 DONE and before the Golem's commit, 2026-10-24 07:01.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.92). The teleporter expansion, existing-world retargeting, map patch and recorded walking proof otherwise match the task. However, the mound footprint violates the explicit spawner-box clearance requirement. I did not independently rerun build.sh.

- **medium** [P2] Keep the entire mound outside the spawners' walking boxes (`player-package\vendor\shattered-legacy-map\trammel.mapops:11584`)
  The mound's east column at x=3620 overlaps the skeleton spawner's walking box (3635,2625 with walking range 15), including all six rim tiles at y=2616???2621. Task requirement 2 explicitly keeps the mound outside every walking box, not just its teleporters and the selected route. The notes acknowledge this deviation, but passable rim pieces do not prevent skeletons from walking onto that part of the entrance. Adjust the footprint or obtain approval for relaxing this constraint.

(1.7 minutes, 405,016 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The new entrance builder depends on an uncommitted pre-change scratch baseline and cannot rebuild from the shipped patch. Server and map changes in the separate code repository were outside this review's diff.

- **medium** [P2] Make the entrance builder work with the shipped patch (`notes\cc-P413-tools\build_anthill.py:95`)
  On a fresh work folder after this change lands, `current` is built from the updated shipped patch, which already contains the burrow and no longer contains `OLD_HOLE`. The unconditional removal therefore returns zero and this assertion aborts before producing renders or a map patch. The documented alternative-placement command fails for the same reason unless the original session's pre-change scratch survives. Normalize the entrance back to a known baseline before rebuilding, consistent with the reproducible fresh-build requirement in [the playbook](notes/map-building-playbook.md#L194).

(1 minutes, 218,534 tokens)
