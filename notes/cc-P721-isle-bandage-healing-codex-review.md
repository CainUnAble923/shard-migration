# Codex review: P721

CC task P721: make the bandage wait clear to a new player on the isle. Reviewed by Codex (`codex exec review`, read-only) after P721 DONE and before the Golem's commit, 2026-10-28 10:56.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The change implements most requested features, but can strand the weapon lesson and omits belongings guidance during the scripted death lesson. The vision approach also teleports instead of walking. Build gates and private-client capture were not verified in this read-only review.

- **medium** [P2] Move the Stranger with walking steps instead of teleports (`server\customizations\Tutorial\TutorialVisionScene.cs:303`)
  During the approach beat, MoveToWorld uses pinned Mobile.SetLocation(newLocation, true), i.e. teleport movement. Setting Direction.Running does not turn those updates into walking steps, so the Stranger jumps between three positions rather than visibly walking up to the Gem as requested. Use ordinary mobile movement for these steps and verify the approach in the client; the current test checks coordinates only.
- **medium** [P2] Include the death lesson in belongings-recovery guidance (`server\customizations\Tutorial\TutorialDeathHelp.cs:51`)
  Excluding core.death means the normal scripted first death never explains where belongings remain or starts the post-resurrection corpse arrow. TutorialCoreTrials.OnDeath only supplies the ghost/resurrection instruction; it does not cover belongings or corpse recovery. Consequently, a non-Young trainee completing this lesson gets none of the requested recovery teaching, and even Young trainees miss the explanation that their belongings stayed in their backpack. Preserve the lesson's existing resurrection progression while supplying the missing guidance and revival tracking.
- **medium** [P2] Retry issuing the pitchfork after a full-backpack failure (`server\customizations\Tutorial\TutorialFarm.cs:581`)
  If the backpack is full when Guard is observed, GivePitchfork deletes the undelivered weapon, but GuardKey is still recorded. Subsequent checks skip this branch, and double-clicking Wren again calls BeginCommands without retrying the gift for a player who still has a pet. The player therefore cannot satisfy HoldsPitchfork or finish the farm lesson, even after following the instruction to make room and speak to Wren again.

(2.2 minutes, 895,530 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.8). No actionable defects found in this repository's added notes, helper scripts, and evidence. The actual server changes are outside this diff, so this verdict does not independently establish that the complete P721 implementation meets every requirement.

No findings.

(1.2 minutes, 320,987 tokens)
