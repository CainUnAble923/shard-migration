# Codex review: P635

CC task P635: fix-up for P628 (CC task P628: build guards that patrol and see, pilot town): its bran. Reviewed by Codex (`codex exec review`, read-only) after P635 DONE and before the Golem's commit, 2026-10-26 00:16.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The conflict resolutions preserve both features, and the notes report the required successful build. However, the imported witness recorder still contains two evidence-attribution bugs. The build was not independently rerun during this read-only review.

- **medium** [P2] Pass the actual action location into witness qualification (`server\customizations\ClusterFGuardWitness.cs:280`)
  For aggression or criminal assistance around a corner, an observer may see the culprit without seeing the victim or action location. `Record` always passes `culprit.Location` into `Sees`, making its separate action-location visibility check ineffective through every gameplay hook. Pass the relevant action location through the recording path and test this through a real crime callback; otherwise the recorder credits observers who could not see the action.
- **medium** [P2] Deduplicate callbacks without merging separate offenses (`server\customizations\ClusterFGuardWitness.cs:240`)
  When a culprit commits separate offenses within one second, this lookup merges them regardless of victim, kind or location. Witnesses of the second offense are attached to the first offense's timestamp, location and potentially unrelated victim, so their subsequent reports identify an incident they never witnessed. Deduplicate callbacks for the same action rather than all actions by one culprit within the time window.

(0.9 minutes, 480,922 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.88). The docs-only changes preserve P628's notes and review and add the requested P635 handoff documenting conflict resolutions, reported test/build results, and the completion marker. No actionable defects were found; code-repository resolutions and build results cannot be independently verified from this diff.

No findings.

(0.3 minutes, 110,493 tokens)
