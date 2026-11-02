# cc-P771: build review of P769 (first outside playtester's UX notes)

## In plain words

- P769 (the fixes from the first outside playtester's notes) left no pictures and no list of placed pieces for the
  build review, so by the review rules it fails, and it goes back to the Iron Golem for a small fix-up.
- Nothing on the isle or in New Haven looks different because of this review. P769 placed no buildings or decoration.
  Its one change to the placement file adds log lines to Sera the healer's death-lesson steps.
- The fix-up only needs a `placed.md` saying "nothing placed" (or the overseer can skip the review). Nothing for you
  to do.

## What I checked

1. Read `notes/guides/building-and-decorating.md` in full (sections 1-11, the wall, stair and roof rules, What to use
   where).
2. Fetched `origin/golem/Iron/P769` in both copies without changing branch.
   - `git ls-tree -r --name-only origin/golem/Iron/P769 -- notes/cc-P769-review` (docs copy) lists **nothing**: the
     folder does not exist. The only file named like a review is `notes/cc-P769-playtester-ux-notes-1-codex-review.md`
     (Codex's code review, not a build review folder). The code copy has no `placed.md` either.
   - P769's notes say so themselves: "No TazUO shots. Free memory fell under 3 GB again during the builds, and Chase
     said to skip the shots then" (memory was low on the rig).
3. Read the diff for what was placed in code (`git diff main...origin/golem/Iron/P769`, code copy):
   - `server/customizations/Tutorial/TutorialCorePlacement.cs` (+6/-2) changes only `TutorialHealer.OfferResurrection`
     and `TutorialResurrectionGump.OnResponse`: two `TutorialCoreTrials.DeathLessonLog(...)` calls (P769 item 7).
     No item, static, addon, door, wall, sign or location changed.
   - Searched every added line under `server/customizations` for `new Static`, `MoveToWorld`, `AddComponent`,
     `Point3D` and hex item IDs. The only IDs are achievement gump icons (`itemGumpId: 0x0FF4`, `0x0E34`), not placed
     pieces. `HavenTownRegions.cs` changes region data, not decoration.
4. With no renders, shots or placed list, there was nothing to check walls, corners, doors, stairs, wall-mounted items,
   roofs, signs, shores, bridge or dock heights, or foliage against. By the prompt's step 4, the verdict is FAIL.

## Verdict

BUILD REVIEW P769: FAIL

1. No renders or placed list were left for review: `notes/cc-P769-review/` and its `placed.md` are missing from
   `golem/Iron/P769`. The guide wants (section 8) a `placed.md` with one line per placed piece and a render and shots
   of each building or area. P769 placed no pieces: its `TutorialCorePlacement.cs` change only adds death-lesson log
   lines to `TutorialHealer.OfferResurrection` and `TutorialResurrectionGump.OnResponse`. So the fix is to add
   `notes/cc-P769-review/placed.md` saying exactly that ("No pieces placed; TutorialCorePlacement.cs changes are
   logging only, cc-P769 item 7") with no renders needed. Or the overseer can let it through with Skip-BuildReview.ps1.

## Commit preflight

- Docs-only. This review changes one file: this notes file. P769's own files were not edited.
- No build, no shard, no lock taken.

P771 DONE
