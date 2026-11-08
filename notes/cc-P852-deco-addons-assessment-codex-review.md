# Codex review: P852

CC task P852: assess decoration addons from the 11-07/11-08 scout (holiday, furniture, lamps, struct. Reviewed by Codex (`codex exec review`, read-only) after P852 DONE and before the Golem's commit, 2026-11-08 13:59.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The assessment covers all 65 folders and provides the requested shortlists, but its central art-verification claim is incomplete and overlooks demonstrated appearance mismatches. Those errors affect the reliability of the port recommendations.

- **medium** [P2] Include indirect and helper-based art IDs in the survey (`notes\cc-P852-tools\survey.py:33`)
  The extractor misses art used by the assessed downloads: Diesel's numeric `AddComponent(...)` helper calls, the carpet's `new GroundItemPart(...)` tables, and lamps' `LitItemID`/`UnlitItemID` return values are not matched. Consequently, for example, the reported nine carpet IDs cover the separate gold carpet rather than the variable carpet's styles, and the claim that every used ID was checked is unsupported. Extend the extraction to these actual source forms and regenerate the inventory and conclusions, or explicitly mark those portions unverified, as required by [AGENTS.md](../../AGENTS.md#L61-L66).
- **medium** [P2] Resolve the art-name mismatches before recommending unchanged ports (`notes\cc-P852-deco-addons-assessment.md:30`)
  The supplied evidence contradicts ???Every name matches???: `high-art-names.txt` identifies the witches' 0x63B8???0x63BB as sick/dead gargoyle art, not flying witches. Separately, Drafted's `DragonBrazier` and `OrnateTableLamp` constructors use 0x4C1, which the checked client identifies as wooden logs. These downloads cannot deliver the advertised appearance merely by rebuilding their existing component lists or converting serialization. Record the mismatches and required replacements, and qualify the affected port recommendations rather than declaring the whole batch verified stock-art content. This follows the source-verification requirement in [AGENTS.md](../../AGENTS.md#L58-L61).

(1.7 minutes, 689,430 tokens)
