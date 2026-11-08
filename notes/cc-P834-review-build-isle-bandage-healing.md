# cc-P834: build review of P721 (the bandage wait on the isle)

Iron Golem, 2026-11-08. A fresh session; I did not build P721. Docs copy `D:\UO\golems\Iron\shard-migration`, code
copy `D:\UO\golems\Iron\ShatteredLegacy`, both on `golem/Iron/P834`. Nothing rebuilt, no shard touched, P721's own
files not edited.

## In plain words

- **P721's build review fails, because it left nothing to review.** The guide asks every map or decoration job to
  leave pictures of what it built and a list of the pieces. P721's branch has neither. That is the only failure.
- **P721's work is already in the game.** It reached main on about 10-28 through P727 ("land P721 via its fix-up
  P723"). Later jobs (P748, P751) then moved Pip to a bench with blood, moved the farm's field gate and moved the
  farm signpost north of the path. The old P721 branch still has the earlier spots.
- **What happens next:** the integrator sends this list to the Iron Golem as a fix-up. The fix-up should take
  pictures of what is on main now. It should not merge the old branch, because that could bring back the old spots.
- **For you:** nothing to do. If you would rather drop the old P721 branch than have it fixed up, tell the
  integrator.

## What I looked at

1. Read `notes/guides/building-and-decorating.md` in full (1337 lines, sections 1-11, including What to use where).
2. `git fetch origin golem/Iron/P721` in both copies. The branch tip is `5bc43a87` in the docs copy, 2026-10-28 10:58.
   That is a day before the guide existed (cc-P734, 10-29), so the branch never had its section 8 to follow.
3. `git ls-tree -r --name-only origin/golem/Iron/P721 -- notes/cc-P721-review` lists nothing. A search of the whole
   tree for `placed.md` or `P721-review` finds nothing either. So there were no renders, shots or placed list to copy.
4. The prompt names the notes `notes/cc-P721-isle-bandage-healing.md`. That file does not exist; the notes are
   `notes/cc-P721-isle-bandage-wait.md` (read in full, ends `P721 DONE`). The only pictures on the branch are three
   frames of the vision scene in `notes/cc-P721-tools/shots/`. They are proof of the vision's timing, not build
   renders, and they show no placed static.
5. The diff (`git diff main...origin/golem/Iron/P721` in the code copy; current main is `4ec6962`) places these
   pieces:
   - In `TutorialCorePlacement.cs`, from P718, which P721 cherry-picked without committing:
     - the clothes table 0x0B8F at Rack -1,-2;
     - the chat signpost 0xA854 at Signpost +0,-2, replacing the old wall arm 0x0B97.
   - In `TutorialFarm.cs`:
     - the field gate at 6713,3979;
     - a fence 0x0837 at 6713,3978;
     - the gate signpost 0xA854 in place of 0x0B97 + 0x0BCF;
     - Pip standing at 6715,3981, facing west, with no bench and no blood.
   - In the vision scene: braziers 0x0E31.
6. Checked current main (`origin/main`). `git cherry` shows P721's commit has an equivalent on main
   (`TutorialWake.cs` and `Bandage-tutorial-wait-lines.patch` are both there). Main has since moved these pieces:
   - Pip: `PipSpot` is 6704,3975, with bench 0x0B2D and blood 0x122A-0x122E. `OldPipSpot` 6715,3981 is labelled
     "cc-P721's".
   - The field gate is at 6695,3979; `OldFieldFenceSpot` is 6713,3978.
   - The chat signpost is at Signpost -2,-4 (north of the path, section 6), and `OldChatSignpostSpot` is +0,-2.

Without renders or shots I cannot judge corners, doors, stairs, facings, roofs, shores, heights or foliage. P721 built
no walls, doors, stairs, roofs, docks or shores; its pieces are the props listed above.

## Verdict

BUILD REVIEW P721: FAIL

1. No renders or placed list were left for review. `notes/cc-P721-review/` and its `placed.md` are missing from
   `golem/Iron/P721` (guide section 8, checklist item 8). The fix-up should leave `notes/cc-P<fix>-review/` for the
   pieces as **main has them now**, not as the old branch has them:
   - a `placed.md` line for each piece: the clothes table 0x0B8F; the chat signpost 0xA854 at Signpost -2,-4; the
     farm gate signpost 0xA854; the field gate and fence 0x0837 at 6695,3979/3978; Pip's bench 0x0B2D and the blood
     decals by the farmhouse's east wall at 6704,3975; the vision braziers 0x0E31;
   - an isorender of the farm gate and stop area, and one of the clothes and chat stops;
   - TazUO shots from the default camera of each signpost, readable;
   - a shot of Pip on the bench. Guide section 6 says the bench's facing and seated look are unverified in a shot.
2. Do not merge the old branch's spots back over main's. On `golem/Iron/P721`:
   - Pip stands at 6715,3981 with no bench and no blood. Guide section 6 wants a hurt NPC on a bench with blood
     (0x0B2D and 0x122A-0x122E); main has this at 6704,3975.
   - The chat signpost 0xA854 stands at Signpost +0,-2. Section 6 wants every sign north of its path; main has
     Signpost -2,-4.
   - The field gate is at 6713,3979; main moved it to 6695,3979.

   P721's code already reached main through P727. A fix-up only needs to take the proof of main's current pieces. If
   the integrator merges this branch, each conflict in `TutorialCorePlacement.cs` and `TutorialFarm.cs` should keep
   main's side.

P834 DONE
