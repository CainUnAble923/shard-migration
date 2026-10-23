# Codex review: P475

CC task P475: fix-up for P289 (CC task P289: the tutorial's core trials, placed on the test world an. Reviewed by Codex (`codex exec review`, read-only) after P475 DONE and before the Golem's commit, 2026-10-23 08:33.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The merge retains most tutorial and main-branch behavior, but introduces a live-player progression deadlock and drops existing core tutorial client-window controls. The build and play-through were not independently rerun during this read-only review.

- **high** [P1] Disable the island graduation gate when tutorial entry is disabled (`server\customizations\Tutorial\ClusterFTutorial.cs:46`)
  On a non-test shard, this now unconditionally disables tutorial entry, but `TutorialIslandGate` remains enabled by default and blocks island exits for players with zero loops. A fresh account stays `NotStarted`, so Rook offers neither lessons nor skipping, and the player cannot earn the graduation required to leave. Coordinate the gate with tutorial availability so keeping the tutorial test-only does not strand new live players.
- **medium** [P2] Preserve the client-window buttons in the core trial pages (`server\customizations\Tutorial\TutorialCoreTrials.cs:108`)
  For a handshake-capable TazUO client, the movement, chat and travel stations previously offered Options, Journal and World Map buttons through `TutorialStationGump`. Core stations now return through their trial handlers and display only `TutorialTrialGump`, which has none of those buttons. Restoring the capability argument on the optional-wing page does not preserve these core features; carry the existing window actions into the trial pages too. The existing TazUO tests instantiate the old page directly, so they do not catch this regression.

(1.7 minutes, 507,809 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.9). The notes explicitly omit a test run required by the task. No additional actionable defects were found in this docs-repository diff; the server conflict resolutions are outside this review's scope.

- **medium** [P2] Rerun P289's play-through against the merged build (`notes\cc-P475-cont-fixup-tutorial-core-trials-playable.md:53`)
  Step 2 explicitly requires running the tests P289 ran, which included the 93-check end-to-end bot play-through. The retained log exercises the pre-merge build, while the reported build gate only reruns assembly tests. Run the play-through against `sl-modernuo:cc-P475` and record its results before declaring this fix-up complete; otherwise the requested post-merge integration verification remains missing.

(0.8 minutes, 220,220 tokens)
