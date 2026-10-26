# Codex review: P647

CC task P647: fix the findings from the weekend build reviews (P636-P646). Reviewed by Codex (`codex exec review`, read-only) after P647 DONE and before the Golem's commit, 2026-10-26 09:43.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The changes address most requested findings and include extensive regression coverage, but the new pet-owner suppression can discard independent crimes. The reported green Docker build was not independently rerun during this read-only review.

- **medium** [P2] Scope owner-callback suppression to the originating action (`server\customizations\ClusterFGuardWitness.cs:397`)
  If an owner commits a separate crime during the same server frame as their pet, `Forwarded` mistakes it for propagation from the pet. Every victimless criminal callback matches, and an attack or assist against the pet's victim also matches, regardless of kind or location. Consequently, `Record` returns the pet's incident without recording the owner's actual offense or its witnesses. `Core.Now` identifies a frame, not an action. Carry an explicit originating-action context through the forwarding path rather than suppressing matching owner callbacks for the entire frame; add a regression where the pet acts and then its owner independently commits a crime before advancing the clock.

(3.8 minutes, 1,574,604 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.85). The only change in this repository is the P647 notes file. It records finding dispositions, red/green test evidence, the gated build, limitations, and For Chase items, and ends with the required completion marker. The server changes and reported test results are outside this diff and were not independently verified.

No findings.

(0.7 minutes, 166,789 tokens)
