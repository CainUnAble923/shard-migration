# Codex review: P676

CC task P676: Trammel's regions and guard zones redrawn on the SoS land (SoS swap S3). Reviewed by Codex (`codex exec review`, read-only) after P676 DONE and before the Golem's commit, 2026-10-28 15:36.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The loader integration and much of the requested region data are present, but overlapping dock regions do not preserve town semantics, and substantial new-island land remains outside all regions. The full Docker build was not rerun during this read-only review.

- **medium** [P2] Cover the remaining dry land of the new islands (`server\data\regions-trammel.json:221`)
  The generated island regions leave substantial interior land uncovered. For example, P669 island 1 (180???391,3144???3407) has 12,846 dry tiles outside every shipped region, including (289,3296). The generator discards an entire candidate rectangle whenever any existing region intersects it, rather than subtracting the covered portion. Subtract existing coverage and retain the remainder so the requested island regions cover the islands rather than disconnected portions.
- **medium** [P2] Parent overlapping dock regions to their guarded towns (`server\data\regions-trammel.json:209`)
  The Moonglow docks overlap Moonglow at (4406,1045), but both are independent priority-50 regions. `Region.CompareTo` cannot distinguish them, and `Region.Find` returns only the first match: either the dock region is masked, or it masks the town without inheriting its guards. Magincia and Papua have the same problem. Parent these dock regions to their towns so dock identification preserves town protection.

(2.9 minutes, 1,749,537 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The work substantially implements the requested regions and records build evidence, but the guard-zone proof excludes independently registered child regions. Concrete guarded wilderness remains outside the redrawn town boundaries, violating the requested invariant.

- **medium** [P2] Include child guard zones when checking redrawn towns (`tools\tests\test_regions_sos.py:97`)
  Skipping every region with a parent hides guard zones that survive outside the newly peeled town boundaries. For example, `A Wheatfield in Britain 4` still independently registers as a `TownRegion` over (1104,1608)???(1136,1640), entirely outside the redrawn Britain region; its block at (1104,1608) is dry, has no built statics, and has none within three blocks. Thus the shipped regions still guard open wild while this proof passes. Check guarded children too, and reconcile their rectangles with the redrawn towns rather than assuming the parent's boundary constrains them.

(2.1 minutes, 871,849 tokens)
