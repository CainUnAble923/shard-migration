# Codex review: P378

CC task P378: play-test plans for everything merged on 10-21. Reviewed by Codex (`codex exec review`, read-only) after P378 DONE and before the Golem's commit, 2026-10-21 15:37.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.87). The change covers the merged prompts and preserves pending status, but some achievement entries remain source-review outlines rather than the executable play-test instructions requested.

- **medium** [P2] Replace source-reference placeholders with executable test steps (`testing\playtest-steps.json:3661`)
  The Noted achievement plans delegate essential instructions to source code instead of supplying the requested steps and expected results. For example, this item never tells testers to walk 100/1,000 overweight steps, use three pack animals at least 90% full, or cover 25 fire tiles/500 snow tiles, nor names the corresponding expected earns. P378-58 similarly substitutes a definitions-file checklist for concrete cases. Expand these plans with the actual prerequisites, actions, thresholds and expected achievements so testers can execute them and recognize success without first writing the test plans themselves.

(1.9 minutes, 1,065,884 tokens)
