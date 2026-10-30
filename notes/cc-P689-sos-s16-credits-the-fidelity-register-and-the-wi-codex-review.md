# Codex review: P689

CC task P689: Credits, the fidelity register and the wiki (SoS swap S16). Reviewed by Codex (`codex exec review`, read-only) after P689 DONE and before the Golem's commit, 2026-10-30 03:37.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The credits and wiki content are prepared for go-live, but the new test incorrectly requires every subsequent release to repeat the map credit. Cross-repository deliverables and test execution were not verified.

- **medium** [P2] Check the swap release's credit rather than the newest release (`player-package\tests\Map-Overrides.Tests.ps1:429`)
  Once the map switch is on, the first subsequent release without a Zigholtul credit will fail this test, even though the swap release correctly credited him. The switch remains on after go-live, whereas `Get-NewestPlayerLines` always selects the latest release. Check the recorded swap release or retain a historical credit check so ordinary later changelog updates do not break the suite.

(0.9 minutes, 258,833 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.86). No actionable defects found in this repository's uncommitted changes. The notes provide the proposed fidelity row, explain the deferred publication steps, and record test evidence. The code-repository changes described in those notes are outside this diff and were not verified by this review.

No findings.

(0.5 minutes, 146,229 tokens)
