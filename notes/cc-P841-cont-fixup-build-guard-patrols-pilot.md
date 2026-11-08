# P841: fix-up for P628 (guards that patrol and see, pilot town): its build review said FAIL

## In plain words

- P628, the hidden groundwork for guards that witness crimes, failed its build review only because it left no "placed" list. It places nothing in the world, so the list now says that in one line.
- You will notice nothing in game: the guard code was already on main through earlier fix-ups (P635, P647, P659). This only clears P628's paperwork so the integrator can close it.
- Its 11 guard-witness tests were run again against today's main code and all passed.
- Nothing for you to do.

Iron Golem, 2026-11-08, on `golem/Iron/P841` in both work copies. I did not commit or switch branches.

## How P628 got onto this branch

The prompt says to check out `golem/Iron/P628` and merge `main` into it. The hand-off says to stay on `golem/Iron/P841`. As P831 and P832 did, I ran `git merge --no-commit --no-ff golem/Iron/P628` into this branch (which is at main) in both copies. The Golem's commit records P628 as a parent, which settles the same thing.

- **Docs copy:** merged cleanly with no changes. Main already has P628's notes and its Codex review.
- **Code copy:** five conflicts: `CHANGELOG.md`, `VERSION`, `docker/uo/apply-patches.sh`, `server/customizations/ClusterFGuardWitness.cs`, `server/tests/Regions/GuardWitnessVerification.cs`. P628's code reached main through P635 (`907853d`). After that, P647 (`3c2f8eb`) and P659 (`ca2f941`) extended it: P659 narrowed the incident matcher, which is the point P628's Codex review raised, and added facts. So main's side is newer and contains all of P628. I kept main's side in every file. Main already has P628's `GuardedRegion-witness-observe.patch` and its `apply_patch` line. Check: after the resolution, `git write-tree` equals `HEAD^{tree}` (`28bc77e1`), so the code tree is exactly main's.

## The reviewer's list (P833)

1. **No renders or placed list for review.** Fixed as the reviewer suggested. `notes/cc-P628-review/placed.md` says: "Nothing placed: observe-only server code, no statics, items, signs or addons; posts and routes are stage 4." I also checked main's newer version of the code, not just P628's: `ClusterFGuardWitness.cs` and the patch have no `MoveToWorld`, statics, addons, signs, spawners or art IDs. The only hex value is the *guards* speech keyword `0x0007`.

## Walk, shots and isorender (step 3)

There is nothing to walk or picture. This fix-up changes no world content and no code (the tree is main's), and P628 placed nothing. The reviewer said no renders are needed for a build that places nothing. `notes/cc-P841-review/placed.md` records this in one line. I took no shots, did not start the private shard, and took no test-shard lock.

## Tests (step 4)

- No `docker\uo\build.sh` image build. Nothing under `server\` or `docker\uo\` differs from main, and main's own gated builds cover this tree.
- I ran P628's tests again in a throwaway container from `sl-uo-builder:cc-P832`. That image's `server\` matches main HEAD (`git diff 3f1b515 HEAD -- server` is empty). The container held the `docker-build` lock, which I have released. Command: build `UOContent.Tests`, then `dotnet test --no-build --filter FullyQualifiedName~GuardWitnessVerification`. Result: **11 of 11 passed**, 0 failed, EXIT=0. P628 had 4 facts; P647 and P659 added the rest.

## Files

- Docs: `notes/cc-P628-review/placed.md`, `notes/cc-P841-review/placed.md`, this note.
- Code: the merge resolution only (all of main's side). No content change.

P841 DONE
