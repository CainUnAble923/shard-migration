# Codex review: P451

CC task P451: League Register fix-up: repair targets, Field Satchel holding and fees, safe delivery. Reviewed by Codex (`codex exec review`, read-only) after P451 DONE and before the Golem's commit, 2026-10-24 11:22.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The requested fixes are largely implemented, but the location-dependent item discount introduces a capacity regression when putting a populated Field Satchel into a backpack. Build and test results were documented in the task notes but were not independently rerun during this review.

- **medium** [P2] Preserve the one-slot allowance when inserting a populated Field Satchel (`server\customizations\LeagueRegister\LeagueConsolidation.cs:132`)
  When a populated Field Satchel is lifted, its parent becomes null, so this now reports its full contents before the destination backpack checks capacity. Pinned `Container.CheckHold` counts `item.TotalItems + 1`, meaning a Field Satchel containing 125 or more items cannot enter even an otherwise empty standard backpack, despite occupying only one slot once inserted. Smaller loads also fail unnecessarily in partially filled packs. Make the destination capacity check account for the backpack-only discount, and test returning a populated Field Satchel through `OnDragDrop` or `OnDragDropInto`; the current bank round-trip test uses unchecked `DropItem`, hiding this regression.

(1.5 minutes, 425,957 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.85). The only change in this repository is the new P451 notes file; no actionable defects were found. The server changes and reported test results are outside this diff, so their correctness could not be independently verified.

No findings.

(0.4 minutes, 98,361 tokens)
