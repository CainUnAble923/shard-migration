# Codex review: P481

CC task P481: design a secluded new player start area (likely a tutorial island) holding the arrival. Reviewed by Codex (`codex exec review`, read-only) after P481 DONE and before the Golem's commit, 2026-10-26 13:41.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The new island renders and six draft build prompts substantially satisfy the latest request without changing maps or shard code. However, the copy lifecycle can permanently exhaust capacity, and party-shared copies do not provide the required private vision scene.

- **medium** [P2] Keep the vision private within party-shared copies (`notes\cc-P481-new-player-start-area-design.md:773`)
  F4 explicitly puts party members on the same copy, so playing the vision at that copy's standing stones is not a fully private moment. Other party members can enter the scene, and the plain mobiles specified below are visible on their shared map; sending effects and subtitles privately does not isolate those figures. Retain a per-player chamber or explicitly design per-player visibility and interaction isolation, and add a simultaneous-party-vision check.
- **medium** [P2] Expire copy reservations for offline trainees (`notes\cc-P481-new-player-start-area-design.md:747`)
  Holding a copy while an occupant is offline means an abandoned tutorial never releases its slot: that occupant never leaves, so the 30-minute empty-copy timer never starts. After 16 such abandoned starts, every subsequent trainee waits indefinitely on map 32. Specify a bounded logout reservation and recovery into a fresh copy, including treatment of pets and belongings.

(2 minutes, 705,486 tokens)
