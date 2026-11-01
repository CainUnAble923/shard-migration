# Codex review: P749

CC task P749: isle-only release 4 (wake easier to see, bandages, coast, shipwreck, signs, farm, bank. Reviewed by Codex (`codex exec review`, read-only) after P749 DONE and before the Golem's commit, 2026-10-31 19:05.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.9). The release notes and recorded build and play-through results support the requested release work. However, the new screenshot helper defaults to mutating the explicitly excluded shared Test Shard.

- **medium** [P2] Default the screenshot helper to the private shard (`notes\cc-P749-tools\isle-shots749.ps1:27`)
  Running this helper without `-Port` targets port 2594, the shared Test Shard, despite this task explicitly forbidding changes there. The guard permits that port, and the helper subsequently executes the specification's admin commands, moving the tester character and changing its logout location. Default to 2596 and reject the shared shard, as `proof-shard.ps1` already does.

(0.7 minutes, 333,935 tokens)
