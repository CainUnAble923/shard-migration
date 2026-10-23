# cc-P290: the tutorial's wing trials, part 1 (combat, healing and magic): not started, waiting on P289

## In plain words

- Nothing was built yet. The combat and magic trials sit on top of P289 (the tutorial's core trials), and P289 is
  finished but not yet in main.
- P289 was done and pushed this morning, but the merge robot could not merge it because main had changed the same
  tutorial files. A fix-up, P475, is queued for the Iron Golem to merge it.
- For you: let P475 run first, then P290 can go again (the question on the Golem card).

2026-10-23. Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P290-tutorial-wing-trials-combat-magic.md`, handed by the Golem
to the Iron Golem. Work copies on branch `golem/Iron/P290`; no code changed.

## For Chase

The prompt says: "Run after P289 is in main; if it is not, stop with `P290 STOPPED: waiting on P289`." Your answer
(Iron-P290-20261023-034251-a411, overseer 06:35) says the same: run P290 only after P289 is merged.

What I checked:

- P289 finished at 07:4x (its branch `golem/Iron/P289` at 368a445: 93 of 93 play-through checks, the full build
  green).
- The integrator tried it at 07:51 and did not merge it. From `D:\UO\golem\status-ShadowIron.json`: "merge conflict
  in ShatteredLegacy: CHANGELOG.md, VERSION, server/customizations/Tutorial/ClusterFTutorial.cs,
  server/tests/Misc/TutorialVerification.cs". It queued the fix-up `cc-P475-cont-fixup-tutorial-core-trials-playable.md`
  for Iron.
- At 08:06, `origin/main` still did not contain 368a445. I watched from 07:46 to 08:06 before finding the failure.

The conflicts come from main's newer tutorial work (P371: graduation is the first loop and opens the island, with
`GraduationLoopVerification`), which landed after P289's branch was cut. P475 resolves them, and P290 should start from
a main that has both.

No files were changed in either repo besides this note.

P290 STOPPED: waiting on P289
