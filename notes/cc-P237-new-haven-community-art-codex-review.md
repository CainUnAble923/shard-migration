# Codex review: P237

CC task P237: New Haven community art (F-21). Reviewed by Codex (`codex exec review`, read-only) after P237 DONE and before the Golem's commit, 2026-10-21 06:10.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The art registration, source conversions and seeder largely fulfill the task, but the seeded light sources transmit the wrong light shape. Build and runtime tests were not independently rerun during this read-only review.

- **medium** [P2] Initialize the light shape on seeded light-source items (`server\customizations\ClusterFCommunityArtSeeder.cs:207`)
  The lanterns and campfire never set `Item.Light`, so their world-item packets carry the default light ID 0 (ArchedWindowEast), rather than the intended shapes 2 and 29. TazUO's `GameScene.AddLight` uses the packet's `item.LightID` for world items, not tiledata's quality byte. Consequently these decorations cast window-shaped light despite the correct tiledata records. Set `Light` from the corresponding record when constructing light-source pieces, and assert it in the placement test.

(1.8 minutes, 960,040 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.95). The placement and art tooling introduce beam collision that protrudes through the boardwalk, an issue the placement validator misses. This review covers this repository's new notes and tools; the separate code repository's implementation and reported build results were not independently verified.

- **medium** [P2] Keep support-beam collision below the boardwalk surface (`notes\cc-P237-tools\records.py:21`)
  All eight beam rows place these impassable, height-16 pieces at z=1, giving a collision top of 17. Reading the map shows the boardwalk's walking surface is z=16 at every beam coordinate. Pinned `Projects/UOContent/Engines/Pathing/Movement.cs:223-228` rejects movement when an impassable item's top exceeds the walking z, so these supposedly underground decorations also block walking on the boardwalk above. Reduce the collision height or lower the placement, keep the server/package records synchronized, and check clearance above the beams during validation.

(1.2 minutes, 558,334 tokens)
