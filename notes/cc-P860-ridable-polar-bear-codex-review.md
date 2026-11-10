# Codex review: P860

CC task P860: port a live ridable polar bear (the ice bloodline source). Reviewed by Codex (`codex exec review`, read-only) after P860 DONE and before the Golem's commit, 2026-11-10 14:38.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.92). No actionable code defects or missing deliverables found. The implementation, tests, build logs and TazUO screenshots support the requested behavior. Tests were not rerun during review; the notes disclose that the required low-memory wait was skipped.

No findings.

(0.9 minutes, 347,527 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.9). The screenshots and recorded run support the riding demonstration, but the red/green verification bypasses the explicitly required build route. The production implementation, tests, changelog and version changes are outside this repository's diff and were not verified here.

- **medium** [P2] Run the red/green verification through the required build gate (`notes\cc-P860-tools\red-all.sh:16`)
  The task explicitly requires building and testing only through `docker/uo/build.sh`, but this harness invokes `dotnet build` and `dotnet test` directly against `sl-uo-builder:bot`. Only the bear files and test are overlaid, so the recorded red/green results can use dependencies and patches different from the task's working tree. Route these verification runs through the required gate rather than treating the separate builder run as equivalent. The repository also establishes the gated build route in [AGENTS.md:85???89](../../AGENTS.md#L85-L89).

(0.8 minutes, 267,506 tokens)
