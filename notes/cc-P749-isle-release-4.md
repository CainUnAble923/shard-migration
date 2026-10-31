# CC task P749: isle-only release 4 (stopped before starting)

## In plain words

- Nothing changed yet. This round adds the easier-to-see wake, the bandages, and the coast, wreck, signs, farm, bank and League house fixes to the live isle release.
- I stopped again because the coast and wreck fix-up (P746) is still not on main. The task says to run only after it merges.
- Your last answer was "Retry" with no text, so I asked you again: wait for the merge, or take P741 and P746 from their Golem branch now.

## State found (2026-10-31)

- ShatteredLegacy origin/main is eec3bbb. It has P740 (a6a89f3, merge b2efbd2).
- P741 (430799d) and P746 (d1d5425) are only on golem/Iron/P741 and golem/Iron/P746. `git merge-base --is-ancestor golem/Iron/P746 origin/main` says no. The P746 branch contains P741.
- The release worktree D:\UO\golems\Iron\release-isle-20261028 is on release/isle-20261028 at 9e616f3. I left it unchanged.

## Question to Chase (first session)

Iron-P749-20261031-150950-31e8. The choices were: wait and requeue, cherry-pick from the unmerged golem branches, or release with P740 only.

## Chase's answer (2026-10-31 15:22)

Chase chose Wait: stop now, and requeue P749 to run after P746 merges to main.

## Chase's answer (2026-10-31 15:24, Iron-P749-20261031-152327-c216)

Chase chose "Retry with my answer" with no text. At the start of this session main was still eec3bbb, and P741 and P746 were still not on main. A retry would only stop at the same place, and the answer did not say to use the unmerged branches. So I asked again (see below) instead of guessing.

## Question to Chase (this session, Iron-P749-20261031-152612-2c4a)

Wait for P746 to merge, take P741 and P746 from golem/Iron/P746 now, or release P740 only.

P749 STOPPED: asked Chase (Iron-P749-20261031-152612-2c4a)
