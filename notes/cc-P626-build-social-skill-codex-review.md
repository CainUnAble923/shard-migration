# Codex review: P626

CC task P626: build the social skill (Begging reworked), stage 1. Reviewed by Codex (`codex exec review`, read-only) after P626 DONE and before the Golem's commit, 2026-10-25 23:02.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The change implements the stage-one identity, charity, and training ladder, and the companion notes contain the remaining-stage drafts and reported build results. However, assignment stockpiling undermines earned training, and stale menu responses bypass conversation eligibility. Build results were not independently rerun during this read-only review.

- **medium** [P2] Revalidate conversation eligibility when the menu is answered (`server\customizations\ClusterFPersuasion.cs:175`)
  After opening the menu, a player can move behind a wall, die, or change facets before answering. This handler checks only coordinate distance and the NPC's life state; ModernUO's `InRange` does not check maps, and neither action method supplies the missing validation. Consequently, the stale menu can grant charity or issue jobs without a living player actually able to converse with that NPC. Recheck the player's life state, matching maps, line of sight, and target eligibility before executing either choice.
- **medium** [P2] Track outstanding courier jobs independently of the backpack (`server\customizations\ClusterFPersuasion.cs:422`)
  A player can bank a letter, request another, and repeat because `CarriedLetter` searches only the backpack. The banked letters remain valid and each independently awards practice, allowing a player to stockpile many letters for the same destination and obtain many gains from one trip. Persist an outstanding assignment per courier, or invalidate the previous assignment when issuing another, so moving the item cannot bypass the one-job limit.

(1.6 minutes, 460,632 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.86). The only change in this repository is the P626 notes file. It records stage 1, reported red-then-green tests and the gated build, provides the five remaining prompt drafts, and ends with the required completion marker. No actionable defects were found in this documentation change; build results were not independently reproduced.

No findings.

(0.6 minutes, 210,409 tokens)
