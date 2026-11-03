# Codex review: P778

CC task P778: assess gathering and crafting side activities. Reviewed by Codex (`codex exec review`, read-only) after P778 DONE and before the Golem's commit, 2026-11-02 19:49.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The note covers all seven activities and supplies rules checks and ranked recommendations, but its saved-type estimates materially misstate the requested porting scope. It also includes an unsupported camping defect. External intake-file changes are outside this diff.

- **medium** [P2] Recount serialized classes rather than files containing Serialize (`notes\cc-P778-assess-gathering-activities.md:40`)
  The saved-type estimates understate the conversion work requested by the task. Gold panning has six serialized classes, not three: four nugget/brick types in GoldNuggets.cs, the trader, and the pan. Similarly, crafting totems contains 29 Serialize overrides rather than eight, including the summon classes in TalismanSummons.cs. Recount the classes across the packages and publish the supporting file/type inventory, distinguishing existing replacements from new types. This also follows [AGENTS.md:61???65](../AGENTS.md#L61-L65), which requires artifact counts and their supporting lists.
- **low** [P3] Remove the unsupported camping button collision claim (`notes\cc-P778-assess-gathering-activities.md:93`)
  For the documented nine entries, CampingMapGump assigns rename/travel IDs 2???19 and removal IDs 20???28, so these ranges do not overlap. The assessment currently reports a defect that its own arithmetic disproves, potentially sending a future implementer toward an unnecessary repair. Remove this claim or document a demonstrated reachable case with more entries.

(1.4 minutes, 408,425 tokens)
