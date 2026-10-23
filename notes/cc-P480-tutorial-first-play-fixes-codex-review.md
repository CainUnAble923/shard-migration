# Codex review: P480

CC task P480: tutorial fixes from Chase's first play: core-only recruiter menu, bright colored tiles. Reviewed by Codex (`codex exec review`, read-only) after P480 DONE and before the Golem's commit, 2026-10-23 15:12.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.93). The changes largely implement the requested tutorial improvements, but the new veterinarian permits remote resurrection through a retained offer. Build and client verification were documented in the task notes but were not independently rerun during this read-only review.

- **medium** [P2] Revalidate proximity to the vet before resurrecting a pet (`server\customizations\Tutorial\TutorialPetCare.cs:136`)
  A player can open the resurrection offer, leave with their ghost pet, and accept it anywhere later. The offer neither freezes the player nor expires, and `Resurrect` checks only proximity to the pet???not proximity to the veterinarian. This turns the town service into portable resurrection, bypassing the need to return to a vet or consume an elixir. Before charging or resurrecting, recheck that the player is alive and that the player, pet and vet are nearby on the same map.

(2 minutes, 821,237 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.9). The documentation and evidence largely address the requested work, but the new play-through can silently pass with missing graduation features. Server implementation correctness cannot be established from this docs-repository diff.

- **medium** [P2] Fail the play-through when graduation rewards are absent (`notes\cc-P480-tools\playthrough.py:607`)
  If graduation never opens the companion picker, this driver merely logs its absence without failing. Likewise, if no graduation box matches the expected description, the loop skips the elixir assertion and returns success. These missing P480 features can therefore produce a green play-through. Assert that the picker and graduation box exist before checking their contents, consistent with [AGENTS.md:339???347](../../AGENTS.md#L339-L347), which requires gates to demonstrably catch failures.

(0.8 minutes, 369,814 tokens)
