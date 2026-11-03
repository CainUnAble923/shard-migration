# Codex review: P785

CC task P785: chocolatiering recipes in Cooking. Reviewed by Codex (`codex exec review`, read-only) after P785 DONE and before the Golem's commit, 2026-11-03 07:16.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The recipe additions and provisioner integration largely satisfy the task, but configuration coverage is incomplete and malformed configuration can abort startup. Recorded build results were inspected; tests were not independently rerun.

- **medium** [P2] Reject null configuration collections before accepting the table (`server\customizations\Chocolatiering\ChocolatieringTable.cs:385`)
  A valid JSON file containing `{"recipes":null}` passes validation because its loop substitutes an empty collection, but this count then throws NullReferenceException during startup instead of falling back to defaults. `provisioner:null` has the same problem, and null recipe/resource/vendor elements throw inside validation. Reject these null values with validation errors so an invalid configuration cannot abort server startup.
- **medium** [P2] Make the existing five recipes configurable too (`server\customizations\Chocolatiering\ChocolatieringTable.cs:280`)
  The prompt requires all chocolatiering numbers in a config file, but cocoa butter, cocoa liquor and the three chocolate bars retain their hard-coded upstream skill ranges and ingredient amounts. This validation also rejects those item types, so staff cannot configure them through chocolatiering.json. Include settings for those five existing entries and apply them without registering duplicate recipes.

(1.8 minutes, 477,907 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The notes document the requested implementation and a successful gated build, but the added probe silently masks verification failures. This review covers the documentation repository changes, not an independent review of the separate server implementation.

- **medium** [P2] Propagate build and test failures from the probe (`notes\cc-P785-tools\probe.sh:32`)
  When compilation or a test fails, the pipelines return the status of `head` or `grep` rather than `dotnet`, and the semicolon-separated commands continue into `dotnet test --no-build` against potentially stale assemblies. The supplied red probe demonstrates this by attempting tests after compilation errors and reporting no matching tests. Make the container shell fail on unsuccessful builds/tests and reject zero matching tests, consistent with [AGENTS.md:339???346](../AGENTS.md#L339-L346). The separate successful gated build does not make this reusable verification script reliable.

(0.8 minutes, 181,918 tokens)
