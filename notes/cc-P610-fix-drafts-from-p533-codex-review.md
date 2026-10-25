# Codex review: P610

CC task P610: build the urgent fix-up drafts from P533. Reviewed by Codex (`codex exec review`, read-only) after P610 DONE and before the Golem's commit, 2026-10-25 16:11.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.95). Most urgent drafts are implemented, but extra-slot absorption remains disconnected and pending saves can discard newer textarea edits. The required real-overlay Rootdeep verification is also missing. The reported Docker build was not independently rerun during this read-only review.

- **medium** [P2] Test Rootdeep safety with the actual overlay removed (`server\tests\Regions\RootdeepMapSafetyVerification.cs:98`)
  U7 explicitly requires loading saved entry state with the real overlay removed, rather than only forcing `MapBuilt`. This test replaces that detector with constant delegates for both missing and restored maps, so it cannot establish that an actual missing overlay closes the entrance or that restoring the files reopens it. Add the requested isolated startup/map-file regression before reporting this verification complete.
- **medium** [P2] Preserve edits made while an answer save is pending (`docker\test-queue\html\index.html:486`)
  If someone presses Save and continues typing before the request completes, this callback unconditionally deletes the newer draft and reloads the older submitted text. Only the clicked button is disabled; the textarea remains editable. This silently loses unsaved work, undermining U8's draft protection. Clear the draft only if it still matches the version submitted by this request.
- **medium** [P2] Include extra-slot jewels in absorption aggregation (`server\customizations\Accessories\ClusterFAccessories.cs:123`)
  The newly accepted BraceletOfPrimalConsumption can now occupy an extra bracelet slot, but `SAAbsorptionAttributes.GetValue` only scans `m.Items`, not `ClusterFAccessories.ActiveJewels(m)`. Its Damage Eater therefore stops working in that slot. The new regression checks the bracelet's stored absorption value rather than the wearer's effective value, so it misses this loss. Include active extra jewels in the absorption reader exactly once.

(3.3 minutes, 1,993,018 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The decision changes still allow stale requests to modify the wrong answer after question reordering, undermining U8's identity and stale-request guarantees. Server-side implementation and build claims cannot be independently verified from this docs-repository diff.

- **medium** [P2] Bind take expectations to the saved answer identity (`tools\decisions.py:547`)
  If questions are reordered after answers are copied, `current` resolves the old positional ID to a different answer, and matching revision numbers let the stale take succeed. I reproduced this with two answered questions at revision 1: swapping them and taking the previously copied D1 marks the original D2 answer taken instead. Undo has the same risk when both records share a revision and `takenInto`. Include the stable answer key in expectations and validate it under the lock rather than relying on positional ID plus revision.

(1.1 minutes, 385,490 tokens)
