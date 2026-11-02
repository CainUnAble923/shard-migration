# Codex review: P764

CC task P764: starter pet leash and shrink (port pet-shrink). Reviewed by Codex (`codex exec review`, read-only) after P764 DONE and before the Golem's commit, 2026-11-01 21:59.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The implementation largely covers the requested functionality, and the accompanying notes record the build, screenshots and release compatibility checks. However, deleting an occupied figurine corrupts follower accounting and enables bypassing the follower limit. I did not rerun the build.

- **high** [P1] Preserve follower accounting when deleting a stored pet (`server\customizations\ClusterFPetLeash.cs:376`)
  When an owner has another active pet, deleting an occupied figurine also subtracts the stored pet's slots from that active follower count. Shrink already removed these slots, but `pet.Delete()` calls `BaseCreature.OnDelete()`, which clears the master and calls `RemoveFollowers()` again. For example, shrinking one of two dogs leaves Followers at 1; trashing its figurine incorrectly reduces it to 0 while the other dog remains controlled. Repeating this allows players to exceed their follower limit. Balance the stored pet's follower accounting before deletion and add a regression test with another active pet.

(2.3 minutes, 601,333 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The notes include successful build and play-test evidence, but the supplied release patch is stale and contains known build and test failures. This review covers the docs repository artifacts, not the separate server working tree.

- **medium** [P2] Regenerate the release patch from the final tested files (`notes\cc-P764-tools\p764-release-isle-20261028.diff:598`)
  Applying this patch to the isle release introduces `new Sewerrat()`, the exact compile error recorded in `gated-build-run1-compile-error.log`. It also lacks the aggression-clearing fixes described for build run 2, so correcting the spelling alone still leaves the fight test failing. Regenerate this artifact from the final green code; the current release handoff reintroduces both already-fixed failures.

(0.9 minutes, 264,086 tokens)
