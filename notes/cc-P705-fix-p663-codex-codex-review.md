# Codex review: P705

CC task P705: fix the Codex findings on P663 (dock surface, start fallbacks). Reviewed by Codex (`codex exec review`, read-only) after P705 DONE and before the Golem's commit, 2026-10-27 09:53.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.85). The changes address all three prior findings and add the missing-island fallback, with four regression tests and a player-visible changelog entry. The task notes record red/green checks and a successful gated build; I did not independently rerun the build or verify behavior against live map data.

No findings.

(1.2 minutes, 473,363 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The new test probe masks failing test exit codes. The remaining docs-repository changes contain no other confirmed defects; the server implementation and full build claims cannot be independently verified from this diff.

- **medium** [P2] Preserve the test failure status in the probe (`notes\cc-P705-tools\probe.sh:19`)
  When `dotnet test` fails, the container shell returns the status of `grep`, which normally succeeds because test failures produce non-warning output. Consequently, this probe reports success for failing tests or compilation errors. Enable `pipefail` inside the container shell or explicitly propagate the test command's status. This also follows [AGENTS.md:339???346](../../AGENTS.md#L339-L346), which specifically warns against checks that convert failures into exit status zero.

(0.6 minutes, 135,498 tokens)
