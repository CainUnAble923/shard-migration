# Codex review: P832

CC task P832: fix-up for P363 (CC task P363: quest markers over NPCs, key items, and colored moongat. Reviewed by Codex (`codex exec review`, read-only) after P832 DONE and before the Golem's commit, 2026-11-08 03:42.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The conflict resolutions preserve both sides, and the notes report a passing gated build. However, the restored marker logic misses current tutorial behavior, and keyed gates do not enforce possession at teleport time. Tests were not rerun during this read-only review.

- **medium** [P2] Check tutorial ownership before advertising a pending reward (`server\customizations\QuestMarkers.cs:216`)
  When one character has a pending graduation companion, another character on that account also receives Ready here because Tutorial is account-scoped and the character check occurs later. ClusterFTutorial.OfferCompanion explicitly rejects characters other than the recorded participant, so the marker advertises a reward that this viewer cannot claim. Apply the recorded-character check before the pending-companion branch.
- **medium** [P2] Recheck the gate key immediately before teleporting (`server\customizations\ShardMoongates.cs:114`)
  For a non-hub keyed gate, MayPass is checked only when CheckGate starts the stock one-second timer. A player can then transfer or drop the key before DelayCallback runs, and base.DelayCallback eventually calls the inherited UseGate without checking possession again. A pending confirmation provides an even longer window. Enforce MayPass at the final teleport boundary so a key cannot be passed among players with travel already queued.
- **medium** [P2] Register markers for the current tutorial guide (`server\customizations\QuestMarkers.cs:176`)
  On current main, TutorialGuide (Tamsin) teaches the core lessons on the Wakening Isle; Rook remains in New Haven. This dispatch recognizes only TutorialRecruiter, so Tamsin falls through to Guildmaster and always returns None. New trainees therefore never see the offered-lesson marker over their actual guide. Update the sources for the tutorial's current NPC roles and test Tamsin as well as Rook.
- **medium** [P2] Map farm markers to the current lesson stages (`server\customizations\QuestMarkers.cs:234`)
  TutorialFarm.StepOf now returns 2 after the pests are cleared, while the player must return to Wren to choose their pet; stage 3 means the pet is already claimed and command practice remains. This mapping suppresses the marker when Wren has the reward and displays Ready during practice instead. Match the current StepOf/Talk flow rather than P363's older stage meanings.

(2.2 minutes, 1,292,049 tokens)

## shard-migration

Not reviewed: Codex is not signed in (WARNING: failed to clean up stale arg0 temp dirs: Access is denied. (os error 5)).
