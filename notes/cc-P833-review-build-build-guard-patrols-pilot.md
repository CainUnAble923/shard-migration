# P833: build review of P628 (guards that patrol and see, pilot town)

Written 2026-11-08 by the Iron Golem (Claude Code), as a fresh session that had not seen P628.

## In plain words

- P628 is the hidden groundwork for guards that see crimes. It changes nothing in the world: no buildings, signs or decoration, and guards still answer as they do today.
- Its prompt was tagged as map work, so it had to pass a build review. The review rules fail any build that leaves no pictures or placed list, and P628 left none (it had nothing to picture). So the verdict below is FAIL.
- The fix is small: P628 records that it placed nothing (or the overseer lets it through), then it can merge.
- For you: nothing to try. If you would rather not spend a fix-up session on this, the overseer's Skip-BuildReview.ps1 can let P628 merge now.

## What I checked

1. Read `notes/guides/building-and-decorating.md` in full (sections 1-11, including the wall, stair and roof rules and What to use where).
2. Fetched `origin/golem/Iron/P628` in both copies without changing branch (commit 4cc4de2e in each).
   - `git ls-tree -r --name-only origin/golem/Iron/P628 -- notes/cc-P628-review` lists nothing, and `git archive` of that path fails with "pathspec 'notes/cc-P628-review' did not match any files". No file on the branch has `P628-review` in its path.
   - The docs diff (`main...origin/golem/Iron/P628`) adds only `notes/cc-P628-build-guard-patrols-pilot.md` and its Codex review note.
   - The ShatteredLegacy diff adds `server/customizations/ClusterFGuardWitness.cs` (an observe-only witness recorder for Cove, Trammel, behind `[GuardWitness on`), `server/patches/GuardedRegion-witness-observe.patch`, its `apply-patches.sh` lines, `server/tests/Regions/GuardWitnessVerification.cs`, CHANGELOG and VERSION.
3. Looked for world placement in the code: the new customization makes no statics, items, signs or addons, and has no `MoveToWorld` or art IDs. The notes say the same: "Nothing placed in any town yet" ("posts and routes" are stage 4's work). P628's own "map" tag came from its prompt's Touches line. Nothing in the build places anything to review.
4. With no renders, shots or `placed.md`, there are no walls, doors, stairs, wall-mounted items, roofs, signs, shores, bridges, docks or foliage to check. Step 4 of the review prompt decides the verdict.

Outside this review's scope, for whoever picks up the fix-up: P628's Codex review (`notes/cc-P628-build-guard-patrols-pilot-codex-review.md`) rated the patch incorrect (confidence 0.96). Its main point is that one culprit's distinct crimes within one second get merged into one incident. That is a code question, not a build one, and this review does not judge it.

## Verdict

BUILD REVIEW P628: FAIL

1. No renders or placed list left for review: `notes/cc-P628-review/` (and its `placed.md`) is missing from `origin/golem/Iron/P628`. The guide (section 8, checklist item 8) wants renders, shots and `placed.md` in `notes\cc-P628-review\`. P628 places nothing in the world, so the fix is a `notes/cc-P628-review/placed.md` that says so in one line ("Nothing placed: observe-only server code, no statics, items, signs or addons; posts and routes are stage 4"). No renders are needed for a build that places nothing. The other way through is the overseer's Skip-BuildReview.ps1.

P833 DONE
