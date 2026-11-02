# Codex review: P767

CC task P767: Codex usage tracking per account (Steph's lane reads Chase's numbers). Reviewed by Codex (`codex exec review`, read-only) after P767 DONE and before the Golem's commit, 2026-11-01 22:59.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The changes largely address account separation and idle visibility, but the new status writer risks losing usage accounting, and idle totals include active time.

- **medium** [P2] End idle intervals when the lane starts working (`notes\cc-P767-tools\p767-kit.diff:107`)
  When a run starts between idle samples, this calculation continues counting idle time until the next idle sample or the ten-minute cap because it ignores run-start events. The new test demonstrates the error: Valorite starts at 11:40, but the 11:35 idle sample counts through 11:45, producing 25 idle minutes instead of 20. Use activity transitions to terminate idle intervals so Status and Sweep do not report working time as starvation.
- **medium** [P2] Serialize usage updates before adding a status writer (`notes\cc-P767-tools\p767-kit.diff:164`)
  When a lane-specific status call overlaps run completion, both processes can execute `Update-CodexUsage` for the same file. That function performs an unlocked read-modify-write and uses a shared `.tmp` filename, so status can overwrite the completed run with an older run list or interfere with its write. This loses tokens, before/after limits and budget-share accounting. Keep status read-only or serialize the entire update with the run writer.

(1.8 minutes, 515,198 tokens)
