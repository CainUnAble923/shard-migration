# Codex review: P631

CC task P631: build the townsfolk features and inn rest, stage 1. Reviewed by Codex (`codex exec review`, read-only) after P631 DONE and before the Golem's commit, 2026-10-26 01:08.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The change implements the intended stage-1 dialogue surface, but lacks an effective live-shard activation guard and has failure paths in accepted dialogue data and file loading. Build execution, red-then-green evidence, and external notes/prompt drafts were not verified.

- **medium** [P2] Convert dialogue file read failures into load diagnostics (`server\customizations\Townsfolk\ClusterFTalkRules.cs:192`)
  If the dialogue file exists but is unreadable, or disappears between the existence check and read, `ReadAllText` throws outside the loader's error handling. Because `Configure()` calls `Reload()` during startup, an optional dialogue-file problem escapes startup instead of disabling talk cleanly; administrative reload also fails without the promised validation diagnostic. Catch expected filesystem exceptions and return a failed load while retaining the previous table.
- **medium** [P2] Handle repeated identical responses without an empty selection (`server\customizations\Townsfolk\ClusterFTownsfolkService.cs:200`)
  The parser accepts multiple responses with identical text. After that text has been spoken once, a subsequent request excludes every response when the matching phase contains two identical entries, leaving `choices` empty and throwing here. Reject duplicate responses or retain a fallback when no distinct alternative exists; an accepted dialogue reload should not make ordinary topic requests throw.
- **medium** [P2] Enforce the test-shard gate before enabling townsfolk (`server\customizations\Townsfolk\ClusterFTownsfolkService.cs:253`)
  On a live shard, an Administrator can type `[ClusterFTownsfolk on` and enable conversations. `ShardCommand(TestOnly)` is descriptive metadata; only the staff hub checks it, while direct command dispatch invokes this handler without that check. Add an actual test-shard guard so stage 1 cannot be activated live contrary to the task's scope.

(2 minutes, 381,695 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.87). The only change in this repository is the new P631 note. It follows the design's stage-1 scope, records test and build results, includes the remaining-stage prompt drafts, and ends with the required DONE line. No actionable defects found in this change; server implementation and reported build results were not independently verified in this docs-only review.

No findings.

(0.4 minutes, 113,958 tokens)
