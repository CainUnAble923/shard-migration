# cc-P612: the urgent fix-up drafts from P572

## In plain words

- Nothing new was built. P572 found no new bugs of its own. The three urgent fixes it lists already have an owner.
- The Hunter's Satchel fix was built by P611, which is committed and waiting to merge. The tutorial vet's checks were built by P610, already merged. The Requisitions fixes are prompt P452, still in waiting.
- The shard build with today's code, `sl-modernuo:cc-P612`, is green: 2,451 tests pass, the usual 4 are skipped, none fail.
- For you: P452 is still in waiting. P572 noted that its file had been empty. It now holds a full brief again (4,160 bytes, written 10-25 04:57), so it can be released when you want it. Otherwise nothing for you to do.

## Drafts

P572's own section "New drafts and additions" says it has no new numbered drafts. Its urgent list ("The urgent existing work stays first") names three existing owners, and it adds one non-urgent item, A1.

| Item | Done or skipped | Why |
|---|---|---|
| P556 U3: Hunter's Satchel admission (P554 #1) | Skipped: done by P611 | Built and tested red-then-green in P611, which is completed in the prompts repo and committed on `golem/Iron/P611` (also on origin). It is not yet merged into this branch's base `6857dd2`, so this work copy still has the old satchel. That is expected and is not a reason to build it twice. |
| P533 U4: tutorial vet and service offers (P559) | Skipped: done by P610 | P610 is merged (`6857dd2`). `TutorialVeterinarian.Resurrect` now refuses when the owner is not alive, on another map or more than 4 tiles from the vet (`server/customizations/Tutorial/TutorialPetCare.cs:140`). P572's "lacks vet proximity" citation predates that. |
| P452: Requisitions (Appraiser magic test, spellbooks, refresh day, config nulls) | Skipped: queued | It is in `waiting\cc-P452-fix-requisitions-fix-up-appraiser-magic-test.md`. The prompt says to skip queued drafts. |
| A1: P478 checklist from P561 | Skipped: not urgent, and owned by queued P478 | A prose checklist for the queued wiki catch-up P478. It is not an exploit, a loss, a crash or a save problem, and it involves no code. |
| P563 C1-C7 | Skipped: For Chase | They are design questions. |

None of these is wrong against today's code. The only stale point in P572 is the vet citation above, which P610 has since fixed.

## Build

I took the `docker-build` lock and released it afterwards. `docker\uo\build.sh -t sl-modernuo:cc-P612` finished with EXIT=0: "Built sl-modernuo:cc-P612 with patches applied and 2451 shard test(s) passing". That is 2,451 passed, 4 skipped and 0 failed. The images are `sl-modernuo:cc-P612` = `53e4d919d90e` and `sl-uo-builder:cc-P612` = `b180fe98d2c0`. The log is `build-P612.log` in the session scratchpad.

No code, test or CHANGELOG change: nothing player-visible was built. No new test, so no red-green cycle applies. No Haven connection, deployment, `docs\` edit, commit, merge, push or branch switch.

P612 DONE
