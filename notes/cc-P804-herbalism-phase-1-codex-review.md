# Codex review: P804

CC task P804: Herbalism, phase 1 (skill, foraging, reagent beds and bowls, processing). Reviewed by Codex (`codex exec review`, read-only) after P804 DONE and before the Golem's commit, 2026-11-05 17:45.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The change implements much of phase 1, but progression, ranked-seed access, mixed-bed harvesting, and seed storage have substantive defects. This was a read-only source review; builds and runtime tests were not rerun.

- **high** [P1] Preserve reagent strain identity through seed-box operations (`server\customizations\Herbalism\HerbalItems.cs:39`)
  The existing `SeedBox` accepts these new `Seed` subclasses, but `GetExisting` compares only plant type and `PlantHue`, which is Plain for every reagent strain. Depositing different strains therefore merges them into whichever strain was deposited first, allowing cheap seeds to become top-strain seeds or destroying valuable strains. Partial withdrawal also constructs an ordinary `Seed`, losing the strain entirely. Update seed-box matching and withdrawal to preserve `ReagentSeed` identity, or explicitly reject reagent seeds until supported.
- **high** [P1] Include Herbalism in the Alembic promotion calculation (`server\customizations\ClusterFGuildStarterPath.cs:50`)
  For a character training Herbalism rather than Alchemy, adding this ownership row and changing the Apprentice task does not unlock ranked seeds. `ClusterFGuildPromotion.CraftSkill` reads `RecipeOwners.SkillsOf`, whose table still contains only Alchemy for the Alembic. Newly joined herbalists therefore retain an Alchemy-based rank cap, and `HerbalLane.MayPlant` rejects their ranked seeds regardless of Herbalism. Wire Herbalism into the actual promotion calculation and cover promotion plus planting together.
- **high** [P1] Provide a reachable gain path through 200 Herbalism (`server\customizations\Herbalism\HerbalLane.cs:306`)
  With the default configuration, cultivable herbs are only tiers 1???2, so even strain 16 has a gain-window maximum of 180. Tier-3 herbs only occur as wild patches, whose checks always use strain 0 and stop at 150. `ClusterFSkillGain.TryRow` has no Herbalism ceiling override. Consequently normal Herbalism actions cannot train to 200; the test claiming otherwise supplies a tier-3, strain-16 combination that players cannot obtain. Add a reachable high-skill gain path and test actual progression rather than hypothetical window inputs.
- **medium** [P2] Avoid shrinking stored harvests when daily yield falls (`server\customizations\Herbalism\HerbalLane.cs:431`)
  If maladies accumulate or the strain drops, today's `DailyYield` decreases and this assignment retroactively reduces previously stored resources to today's smaller storage cap. With enough maladies to make daily yield zero, it deletes the entire accumulated harvest. This makes a yield penalty destroy earlier production, undermining the intended ability to save several days of herbs. Limit new accumulation without reducing already stored resources merely because today's yield decreased.
- **medium** [P2] Preserve each herb type when harvesting a mixed bed (`server\customizations\Herbalism\HerbalLane.cs:458`)
  When a bed contains different reagent plants, `BedOf` includes all of them and this method sums every mound's resources, but creates only the herb type of the clicked mound before clearing every mound. For example, harvesting a garlic mound converts neighboring mandrake and ginseng harvests into garlic. Create separate outputs and ledger entries per herb type, or restrict collection to matching plants without discarding the others.

(2.2 minutes, 1,191,628 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The supplied release diff implements most requested features, but its reachable progression cannot reach 200 and its harvesting logic can convert or delete earned resources. These defects require correction despite the reported green builds.

- **high** [P1] Provide a reachable gain path through 200 Herbalism (`notes\cc-P804-tools\p804-release-isle-20261028.diff:1222`)
  With the default settings, growable herbs only reach tier 2, so even strain 16 produces a maximum gain window of 130???180. Tier-3 herbs cannot be grown and use strain 0 when foraged or processed, topping out at 150. Pinned `SkillCheck.CheckLocation` returns without rolling gains once the skill reaches the window maximum, making 200 unreachable. The `TopStrainsKeepTheSkillRisingTo200` test masks this by using GraveMoss at strain 16, which players cannot obtain. Add coverage using actually reachable plants and actions.
- **medium** [P2] Avoid deleting stored harvest when daily yield decreases (`notes\cc-P804-tools\p804-release-isle-20261028.diff:1347`)
  The storage ceiling is recalculated from today's malady-adjusted yield, so a lower-yield day destroys previously accumulated herbs. For example, a bowl holding 42 herbs drops to at most 35 when its daily yield falls from 6 to 5; a zero-yield day erases the entire stored harvest. Maladies are described as reducing production, not consuming existing stock. Use a stable capacity or otherwise ensure this production update cannot reduce already available resources.
- **medium** [P2] Preserve each herb type when harvesting a mixed bed (`notes\cc-P804-tools\p804-release-isle-20261028.diff:1374`)
  When a bed contains different reagent plants, `BedOf` includes every reagent mound, but harvesting sums their resources and creates a single stack using only the clicked plant's herb type. Clicking garlic therefore converts the bed's mandrake, nightshade, and other harvests into garlic before clearing every mound. Group the harvest by herb type, or enforce homogeneous beds when planting; the existing bed test only exercises identical plants.

(1.7 minutes, 978,512 tokens)
