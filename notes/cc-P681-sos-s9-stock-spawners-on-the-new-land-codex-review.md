# Codex review: P681

CC task P681: Stock spawners on the new land (SoS swap S9). Reviewed by Codex (`codex exec review`, read-only) after P681 DONE and before the Golem's commit, 2026-10-28 02:00.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The relocation hook moves spawner items without updating their actual spawn bounds, undermining the primary terrain fix. The required complete town-service coverage is also explicitly deferred. Build results were inspected in the notes but not independently rerun.

- **high** [P1] Update the DTO location before constructing moved spawners (`server\patches\ImportSpawners-sos-placements.patch:10`)
  For moved entries, this changes only the local `location`, but `dto.ToSpawner()` still constructs `SpawnBounds` around `dto.Location` in `BaseSpawner.ApplyDto`. Moving the resulting item does not recenter those bounds: `OnLocationChange` checks whether they were centered on the item's previous location, initially (0,0,0). Consequently, moved spawners retain their old spawn area, including the old Z for range-zero vendors, and can continue spawning on the broken terrain instead of their new homes. Update the DTO before construction and verify spawn bounds and spawned positions, not just the spawner item's location.
- **medium** [P2] Prove and supply all four required town services (`server\tests\Misc\SosSpawnPlacementsVerification.cs:6`)
  The delegated service check only verifies that towns retain roles present in the stock baseline, rather than the prompt's requirement that every town has a bank, healer, smith and provisioner. The P681 notes explicitly leave Cove without a bank, Yew and Wind without smiths, Nujel'm without a healer or provisioner, and Magincia without a smith or provisioner. These are existing towns, not the new towns assigned to S10. Supply the missing services and make the fact require all four roles instead of accepting baseline omissions.

(2.1 minutes, 719,755 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The submitted tools and evidence weaken two explicit acceptance criteria and retain wild spawners contrary to the requested terrain-or-drop rule. A green build does not resolve these task-completion gaps.

- **medium** [P2] Drop wild spawners when no matching terrain exists (`notes\cc-P681-tools\regrade.py:343`)
  This fallback contradicts the explicit instruction to move wild spawners onto matching terrain within 20 tiles or drop them. It retains, for example, the wildlife spawners at (2085,658) on sand after identifying their original habitat as green and finding no match. Keeping them to preserve existing import-count assertions does not satisfy the requested placement behavior; emit drops for these records and update the affected count expectations instead.
- **medium** [P2] Check required town services independently of the baseline (`notes\cc-P681-tools\services.py:76`)
  The prompt requires every town to have a bank, healer, smith and provisioner, but this check only fails when an existing service disappears. Consequently `MISSING 0` passes despite the submitted report showing Cove without a bank, Yew and Wind without smiths, and other missing services. These gaps are explicitly deferred in the notes without a corresponding task exemption. Check all required roles for the applicable towns and fill the gaps, or report this acceptance criterion as unfinished.
- **medium** [P2] Verify walkable homes rather than nearby land (`notes\cc-P681-tools\regrade.py:180`)
  This predicate does not establish the requested home-and-range invariant: a ranged land spawner can pass with an unwalkable home and mostly unwalkable range. The submitted map cache and ledger demonstrate this at (5192,695), where both facets retain Ghoul/PoisonElemental spawners on open water as `passes on SoS`. The new fact simply repeats this weaker predicate. Validate the actual required home and range conditions, or obtain explicit approval for these exceptions instead of reporting the requested proof complete.

(1.9 minutes, 527,183 tokens)
