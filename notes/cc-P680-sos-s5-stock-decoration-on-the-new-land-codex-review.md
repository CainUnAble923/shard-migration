# Codex review: P680

CC task P680: Stock decoration on the new land (SoS swap S5). Reviewed by Codex (`codex exec review`, read-only) after P680 DONE and before the Golem's commit, 2026-10-28 21:19.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The decoration integration and audit artifacts are present, and the three Python facts pass. However, independent map checks identify retained decorations in newly created void and inside newly added impassable statics, contradicting the task's placement requirements.

- **medium** [P2] Reject obstructed placements even when the building matches (`server\data\Decoration\Britannia\britain.cfg:3527`)
  These barrels remain at `(1406,1824,0)` and `(1406,1824,5)` inside SoS's impassable hedge `0x0C8F` spanning Z 0???6; the pair at `(1408,1806)` similarly intersects hedge `0x0DB9` spanning Z 0???9. These obstructions do not exist on the stock map. The CSV retains them because nearby structural pieces match, overriding the failed space check. Apply the obstruction check to building-match placements too, then regenerate the cfgs so matching surroundings cannot preserve items inside newly added impassable statics.
- **medium** [P2] Drop the mutually supporting blood tiles in Destard's void (`server\data\Decoration\Britannia\_destard.cfg:285`)
  The blood entries `0x122B` and `0x122C` at `(5271,968,-40)` remain on both facets even though SoS replaces the stock ground there with void (`0x0244`, Z -50) and has no statics there. The CSV keeps each because it supposedly stands on the other blood tile. The water/void fact likewise accepts these unsupported decorations as support, so it passes despite violating the requested invariant. Require support ultimately rooted in solid land or a supported surface, and drop these entries.

(2.8 minutes, 828,209 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The grading fallback retains decoration inside newly added impassable geometry, and the water/void test cannot detect stranded cfg statics. These undermine both the requested placement behavior and its required proof.

- **medium** [P2] Exclude the tested static from its own supporting geometry (`tools\tests\test_s5_decoration.py:93`)
  `facet_layout()` includes every cfg static, including the entry currently being checked. Consequently, an isolated `Static` placed anywhere over water or void always finds itself at `sz == z` and passes this test. This leaves the required water/void proof ineffective for static decoration. Remove the current entry from the support candidates and verify actual supporting geometry rather than accepting any static arbitrarily far below it.
- **medium** [P2] Check collision clearance after matching a building (`notes\cc-P680-tools\deco.py:255`)
  When `fit()` rejects an item because SoS added an impassable static, this fallback can still keep it solely because surrounding structure matches. For example, the Britain barrels at (1406,1824,0/5) and (1408,1806,0/5) are retained inside new impassable hedges; those blockers are absent from the stock map. Validate clearance at the proposed destination before accepting a structural match, otherwise the generated cfg violates the requirement to drop items under impassable statics.

(1.7 minutes, 427,822 tokens)
