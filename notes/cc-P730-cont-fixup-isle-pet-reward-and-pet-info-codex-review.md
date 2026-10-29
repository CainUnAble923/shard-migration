# Codex review: P730

CC task P730: fix-up for P726 (CC task P726: the isle pet is a reward, and players can see their evo. Reviewed by Codex (`codex exec review`, read-only) after P730 DONE and before the Golem's commit, 2026-10-28 20:33.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The conflict resolution preserves the intended features, but legacy healing credit breaks graduation and failed bandage delivery lacks the normal retry path. Tests were inspected but not independently rerun.

- **high** [P1] Honor legacy healing credit when checking travel completion (`server\customizations\Tutorial\ClusterFTutorial.cs:192`)
  For an existing trainee with `farm.heal` but no `core.healing`, this alias marks healing complete, but the travel prerequisite loop below still checks `StationsDone.Contains(s.Key)` directly. Consequently, even after every lesson and travel are finished, `CoreDone` remains false and graduation is unavailable. Starting travel again only displays its already-finished window. Apply the legacy healing credit consistently when checking travel prerequisites, or materialize the new station key.
- **medium** [P2] Retry bandage delivery when reopening the healing lesson (`server\customizations\Tutorial\TutorialCoreTrials.cs:233`)
  If the backpack is full when healing starts, `BeginHealing` returns `NoRoom`, but the trial remains active. After making space, reopening the lesson or clicking Hint only calls `Show`; this delivery block is skipped, and `Resupply` cannot help because healing has no `trial.Supply`. Wren also no longer issues bandages. The player must discover that restarting the lesson is required, despite the delivery message telling them to return to Wren. Retry the capped bandage delivery when the active healing lesson is shown.

(1.9 minutes, 716,663 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.92). The notes document conflict resolutions and a successful gated build, but explicitly omit the required rerun of P726's end-to-end test. Server conflict resolutions themselves are outside this repository's diff and were not independently verified here.

- **medium** [P2] Rerun P726's bot route against the resolved build (`notes\cc-P730-cont-fixup-isle-pet-reward-and-pet-info.md:58`)
  Step 2 explicitly requires rerunning the tests P726 ran, but the private-shard bot route was skipped. P726's successful run validates its original tree, not this resolved build with main's additional patches and teleporter data. The unit-test build does not replace that end-to-end check; P726's own notes show the bot previously exposed a load-seeding defect after a green build. Run the existing route against `sl-modernuo:cc-P730` and record the result before marking the task complete.

(0.7 minutes, 149,577 tokens)
