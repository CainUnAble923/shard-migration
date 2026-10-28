# Codex review: P728

CC task P728: fixes from Chase's walk of Tutorial Island (round 4). Reviewed by Codex (`codex exec review`, read-only) after P728 DONE and before the Golem's commit, 2026-10-28 17:39.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.91). The changes substantially address the walkthrough requests, but the reordered farm progression introduces a no-pet softlock. Build and bot results were inspected in the task notes, not independently rerun.

- **medium** [P2] Skip pet commands when the pet disappears after war mode (`server\customizations\Tutorial\TutorialFarm.cs:662`)
  If the trainee releases or loses their pet after completing the war-mode step but before finishing follow/guard, the lesson becomes stuck. The no-pet fallback now runs only while recording `WarKey`; subsequent checks require a pet forever, and double-clicking Wren merely repeats the command instructions. Previously, returning to Wren without a pet skipped those commands. Handle the no-pet case during the command stages as well so the trainee can reach the pests.

(1.3 minutes, 640,162 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The added verification scripts contain failure-masking bugs. This repository's changes otherwise consist of notes and evidence; the separate server implementation is not part of this diff, so its full correctness cannot be established here.

- **medium** [P2] Check the current arrow rather than its entire history (`notes\cc-P728-tools\isle.py:244`)
  `Client.arrows` is an append-only packet history, and the farm lesson already points at Wren before combat (the recorded run shows this at 57 seconds). Therefore this assertion passes even if clearing the pests never redirects the arrow, or leaves it disabled. Check the latest arrow state and require a post-clear update so this verifies item 6 rather than an earlier lesson instruction.
- **medium** [P2] Preserve the test process exit status inside the container (`notes\cc-P728-tools\probe.sh:26`)
  When `dotnet test` fails, this pipeline normally still returns success because `grep -v warning` determines its exit status. Consequently Docker and `probe.sh` report success for failing tests, including the deliberate red runs. Enable `pipefail` in the container's Bash invocation or explicitly propagate the test exit status. This recreates the failure-masking behavior specifically warned about in [AGENTS.md](../../AGENTS.md#L345-L347).

(1.2 minutes, 370,500 tokens)
