# Codex review: P687

CC task P687: Fences for the unfinished areas and the sealed dungeons (SoS swap S14). Reviewed by Codex (`codex exec review`, read-only) after P687 DONE and before the Golem's commit, 2026-10-29 10:47.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.92). The change substantially implements the requested fences and seam dressing, but its claimed login protection misses ModernUO's unchanged-location login path. Build and test results were inspected in the task notes, not independently rerun.

- **medium** [P2] Enforce the fence when a player logs in without moving (`server\customizations\Regions\SosFenceRegions.cs:168`)
  If a player logs out aboard a boat inside a fence and the boat subsequently leaves, logging back in does not trigger this handler. Pinned ModernUO restores `Map = LogoutMap` and `Location = LogoutLocation`, but internalization preserves the coordinates, so `SetLocation` returns early because the location is unchanged. With no `OnEnter` or login enforcement, the player remains inside off-boat until they move, contrary to the promised fallback protection. Add entry/login enforcement and test the actual login path rather than only calling `Placement`.

(2.8 minutes, 1,118,078 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.78). No actionable defects found in the changed tests, supporting tools, or task evidence in this repository. The runtime fences and map patch reside in the separate code repository and are not covered by this verdict; the reported build results were not independently rerun.

No findings.

(1.2 minutes, 244,105 tokens)
