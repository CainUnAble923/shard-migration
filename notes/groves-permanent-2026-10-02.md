# Groves must be permanent (Chase, 2026-10-02, 12:55)

Raised by the skills design chat; confirmed by the overseer in code. For the next defect batch.

- **Fact:** pinned sets `lumber.RandomizeVeins = Core.ML` (`UOContent/Engines/Harvest/Lumberjacking.cs:118`), so on this
  post-ML shard each tree bank picks a random wood vein when first touched (`HarvestDefinition.cs:136-139`), and banks
  live only in memory, so after a restart (or the bank cache going) the same spot can roll a different wood. Our
  `ClusterFLumberjackingExtension.cs` appends the 8 extended woods (`:200-258`) but never sets `RandomizeVeins`.
  Mining is already permanent: `ClusterFMiningExtension.cs:131` sets `def.RandomizeVeins = false`, which makes the vein
  a stable function of x, y and map (`HarvestDefinition.cs:141-143`, `StableRandom` over `VeinWeights`).
- **Decision (Chase):** groves are permanent, so the logging book (P13's grove ledger, and its planned teleport to a
  recorded grove) can trust that a recorded spot keeps its wood type.
- **Fix:** set `def.RandomizeVeins = false` in `ClusterFLumberjackingExtension` after the veins are combined, as mining
  does; check `VeinWeights` is recomputed for the combined vein list (`HarvestDefinition.cs:77`, set by the `Veins`
  setter); a fact that the same x, y, map returns the same vein across fresh definitions; and check what P13's ledger
  records against the now-stable vein. A deviation to register (OSI randomizes per tree bank since ML).
