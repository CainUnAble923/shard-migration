# Codex review: P872

CC task P872: fix-up for P858 (CC task P858: port real-light lamps and the Festival Peddler's wagon). Reviewed by Codex (`codex exec review`, read-only) after P872 DONE and before the Golem's commit, 2026-11-10 14:08.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.92). The three requested roof corrections are implemented, and the supplied renders, character-walk evidence and successful gated-build log support them. However, the newly introduced wagon setting does not update or disable an already persisted wagon.

- **medium** [P2] Reconcile the existing wagon with its configuration (`server\customizations\RewardStores\FestivalStore.cs:685`)
  If the wagon has already been saved, changing `clusterf.festival.wagonAt` to `off` and restarting leaves it standing; changing the coordinates likewise leaves it at the old location. This guard returns without reconciling the persisted wagon, and `Sync()` does nothing when the festival state is unchanged. Remove the tracked wagon when disabled and relocate it when its configured position changes, without requiring staff to clear and replace the entire stall.

(1 minutes, 435,130 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The generator changes and supplied screenshots address all three visual findings, and the build log records a passing gated build. However, the required observed failure of the new regression checks was explicitly skipped. Server implementation changes are outside this repository's diff and were not independently verified.

- **medium** [P2] Observe the roof regression checks failing before claiming red (`notes\cc-P872-cont-fixup-lamps-and-peddler-wagon.md:56`)
  The notes explicitly substitute source inspection for running the new roof and cat assertions against P858. This leaves their ability to catch the original defects unverified and misses the required red-before-green confirmation ([AGENTS.md:49](../../AGENTS.md#L49)). Run the updated test against the original P858 design, confirm an assertion failure rather than a compilation failure, then restore the fixed design and record the passing result.

(0.8 minutes, 317,730 tokens)
