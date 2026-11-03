# Codex review: P792

CC task P792: assess druid spells and spellcrafting. Reviewed by Codex (`codex exec review`, read-only) after P792 DONE and before the Golem's commit, 2026-11-03 11:19.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.92). The assessment provides the requested recommendations, ranking, rules checks and prompt sketch, and the external intake rows are present. However, the explicitly requested saved-type assessment is missing and its substitute includes an incorrect count.

- **medium** [P2] Inventory saved types instead of counting Serialize methods (`notes\cc-P792-assess-magic-systems.md:28`)
  The task explicitly asks for saved types, but this substitutes method counts without identifying the persistent classes. These are not equivalent: the druid archive contains two alternative `SleepingBody.cs` implementations, while inherited serialization can cover types without their own override. Even the stated method count is incorrect for lich-staff: all four classes implement `Serialize`, not three. Add a per-pack saved-type inventory, distinguishing existing core types and alternative implementations, so the assessment actually establishes persistence scope. This also satisfies [AGENTS.md:61???69](../AGENTS.md#L61-L69), which requires counting artifacts and publishing the supporting file list.

(0.9 minutes, 301,223 tokens)
