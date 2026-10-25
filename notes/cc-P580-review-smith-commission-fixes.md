# P580: review of the P454 smith commission fixes

Reviewed 2026-10-24. P454 commit `30bc1ea4278accb1dab3b33c776756d8c85c70f5` is an ancestor of both local `main` and this work copy, at `608d0b42485390f7963a713a28161d96e7618b63` when checked.

Read `cc-P454-commission-reroll-cooldown.md` and the adjacent `cc-P454-fix-smith-commissions-cooldown-on-the-guild-codex-review.md`. The earlier review reported no findings. The finding below is new.

## Finding

**Risk: the large generator's cooldown check has no direct regression assertion.** `server/tests/Misc/NotedBySystemVerification.cs:848` and `:856` request a large commission through the book during the cooldown. Both calls return at `server/customizations/SmithGuildBook.cs:678`, before reaching `SmithCommissionSystem.GenerateLarge`; the direct assertion at test line 850 exercises only the small generator. Consequently, the test does not independently protect the new shared-cooldown check in `server/customizations/ClusterFSmithCommissions.cs:578`. Suggested fix: after each size of abandon, also assert that a direct `GenerateLarge(pm)` returns null with an empty large slot, then succeeds after the wait. Confirm that the assertion fails with only the generator's cooldown check removed and passes with it restored.

## Behavior checked

No remaining functional defect found in the requested cooldown and Pre-Crafted paths by source inspection.

- The book records an abandon only after finding and removing a commission, for small commissions at `SmithGuildBook.cs:657` and large commissions at `:710`. The guildmaster gump records small abandons at `SmithCommissionGump.cs:302`.
- Both generators read the same character timestamp through `RequestCooldownLeft`, at `ClusterFSmithCommissions.cs:530` and `:578`. Neither the book nor the guildmaster request path clears that timestamp. Switching request size or interface therefore does not skip the wait in the reviewed code.
- A large set reaches `CompleteLarge` after its last piece at `ClusterFSmithCommissions.cs:673`. Completion calls the achievement hook at `:684` with the original issue time. `ClusterFNotedBySystem.cs:1104` checks that time against the Pre-Crafted window. The book-driven achievement test checks one credit for a fast completed set and no additional credit for a slow set.

## Scope and verification

Read the P454 code and test diff and the current relevant implementations in:

- `server/customizations/ClusterFSmithCommissions.cs`
- `server/customizations/SmithGuildBook.cs`
- `server/customizations/SmithCommissionGump.cs`
- `server/customizations/ClusterFNotedBySystem.cs`
- `server/customizations/ClusterFGuildSystem.cs` (reset cleanup)
- `server/customizations/ClusterFSmithBODSystem.cs` (guildmaster turn-in)
- `server/tests/Misc/NotedBySystemVerification.cs`
- `server/tests/Misc/NotedFixupsVerification.cs` (large-piece validation)
- `server/tests/Misc/SmithCommissionRewardsVerification.cs`

Also checked the P454 changelog, version change and wiki text. Searched canonical customizations, patches and tests for commission generation, removal and cooldown calls. No code changed. No tests added or run, as this is a docs-only review with no lane tests. Runtime behavior, a client session and the reported P454 red/green build results were not independently verified. The missing-test finding follows from the test call paths; no mutation run was performed.

Ran `tools/progress.py --dry-run` with both work-copy path overrides; it exited 0. Despite its flag, it rewrote `tools/progress.json` inside `build()`. Restored that generated file to its original tracked contents so this task leaves only this review note changed.

P580 DONE
