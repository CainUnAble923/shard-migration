# Codex review: P827

CC task P827: fix-up for P803 (CC task P803: New Haven League building: replace the bulletin board a. Reviewed by Codex (`codex exec review`, read-only) after P827 DONE and before the Golem's commit, 2026-11-08 01:32.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The corrected layouts and recorded visual evidence address the review items, but existing P803 boards are not upgraded to the corrected position. Build success was verified from the recorded log; tests were not rerun during this review.

- **medium** [P2] Migrate boards from P803's position to the corrected tile (`server\customizations\Requisitions\Appraiser.cs:338`)
  For a save containing P803's board at `(3662,2548,0)`, this fix never moves it: `OldOfficeBoardSpots` omits that position, and `Seed` accepts the existing board within five tiles as already placed. Consequently, reviewer item 4 remains broken after restarting or reseeding that world. Add P803's position to the migration and test upgrading an existing board there, as required by the [existing-world upgrade rule](D:/UO/golems/Iron/shard-migration/notes/guides/building-and-decorating.md#L40).

(0.9 minutes, 343,023 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.86). The reviewed artifacts address all five reviewer items, including corrected placements and new main-town client shots. Red/green test evidence and successful gated builds are recorded. I inspected the renders and shots but did not rerun builds or client tests.

No findings.

(0.8 minutes, 424,894 tokens)
