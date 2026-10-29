# Codex review: P684

CC task P684: Treasure maps, houses, boats, docks and SOS bottles (SoS swap S11). Reviewed by Codex (`codex exec review`, read-only) after P684 DONE and before the Golem's commit, 2026-10-29 01:23.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.91). The treasure-map changes appear consistent with the requested land restrictions, but the required per-dock boat-placement deliverable is knowingly incomplete. Build success is recorded in the task notes; I did not independently rerun the build.

- **medium** [P2] Complete the required boat-placement checks at every dock (`server\tests\Misc\SosTreasureLandVerification.cs:10`)
  P684's dock requirement remains incomplete. The companion `cc-P684-tools/out/docks.csv` reports no usable placement at Haven (3650,2653) or Nujel'm (3803,1279), and `test_sos_s11.py` explicitly accepts those failures. The notes defer repairs to future map work, but the prompt requires boat placement and a passing float test at each dock. Supply working dock placements and enforce that requirement, or obtain an explicit scope change before treating S11 as complete.

(1.9 minutes, 378,528 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The verification can silently reuse stale map results, and the passing dock gate excludes two locations required by the task. The notes acknowledge those unresolved docks, but declaring P684 complete is not supported by the requested acceptance criteria.

- **medium** [P2] Resolve the failed dock requirements before declaring completion (`tools\tests\test_sos_s11.py:100`)
  For Haven and Nujel'm, this gate explicitly passes when no usable boat placement is found. Task item 3 requires boat placement and a floating-boat test at each author's dock; recording these failures is useful evidence but does not complete that requirement. Resolve the dock locations or obtain an explicit scope deferral and report the task as incomplete rather than treating the failures as passing acceptance criteria.
- **medium** [P2] Invalidate sea masks when their map inputs change (`notes\cc-P684-tools\sea.py:83`)
  After the first run, every subsequent run loads the cached water and connectivity masks without checking the map files or mask-generation rules. Changing land or adding blocking statics can therefore leave the dock and SOS facts passing against the previous map, despite loading current land and statics alongside those stale masks. Fingerprint the inputs and algorithm version, or rebuild the masks for verification runs.

(1.8 minutes, 400,004 tokens)
