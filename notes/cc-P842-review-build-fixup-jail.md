# cc-P842: build review of P838 (the New Haven jail, fix-up of P820)

## In plain words

- **The jail on main passes.** The cell bars now run in one closed line, each cell wall meets them with no gap, and the
  candelabra no longer stands in front of a cell gate. Nothing changes in the game from this review.
- **The jail in the testers' New Haven (the isle release) fails on one thing.** A "Housing lesson, stop 2" signpost
  stands inside the jail hall, right in front of the middle cell's gate. The housing lesson's second stop ("where houses
  can be built") is also inside the jail now. The jail was built on top of that stop. You can see the post in
  `notes\cc-P838-review\shots-isle\2b-hall-window-closed.jpg`. It was already there in P820's shots.
- **Nothing for you to do.** The integrator sends the fix below to the Iron Golem as a fix-up.

Iron Golem, 2026-11-08, a fresh session that did not build P838. I read the guide in full, fetched
`origin/golem/Iron/P838` in both copies without changing branch, and looked at every render and the hall, door,
people and before/after shots for both builds. I read `placed.md`, P838's notes and the code diff. I also searched
the release branch's code for anything at the jail's coordinates. Nothing was built or run.

## Verdict

BUILD REVIEW P838: FAIL

1. **0xA854 signpost "Housing lesson, stop 2: where houses can be built", 3474,2601,0, release branch (stock New
   Haven), standing inside the jail hall in front of the middle cell's gate (0x0828 at 3474,2600).**
   - **What is wrong.** On `release/isle-20261028`, `NewHavenLessons.cs` line 373 places this signpost as a fixed
     Haven piece. Line 76 puts `HousingStop(1)` at 3474,2603. Both tiles are inside the release jail's box (post
     3469,2597 to corner 3479,2605). So the jail hall has a stray signpost one tile in front of a cell gate (seen in
     `shots-isle\2b-hall-window-closed.jpg`, `3z-window-all-five.jpg` and both halves of
     `cell-fronts-before-after-isle.jpg`). The housing lesson's stop 2 is now on the jail's floor, which is the same
     tile as the jail lesson's own `Place` (post + 5,6). A player doing the housing lesson is sent into the jail to
     learn "where houses can be built". This breaks guide 2.6 (nothing stray, no leftover piece inside a new
     building), 6 (a sign stands beside its stop, off door lines and walks, north of its path) and 2.4 (keep a door's
     approach clear). `placed.md` and `TutorialJail.Retired` do not mention it. The jail cannot remove it, because the
     Haven pieces are seeded again on load.
   - **What the guide wants.** On the release branch only, move housing stop 2 and its sign out of the jail onto open
     lawn. The new spot should be clear of the jail, the palisade and the trees (guide 5, keep clear). The sign stands
     within 2 of the stop, north of its path, on no map static (guide 6). Regenerate the `HavenSignTileVerification`
     table and box for the new spot (`notes/cc-P814-tools/sign_statics.py`). Retire the old sign at 3474,2601 on load
     so an existing release world loses it. Add a fact that no fixed Haven piece and no lesson stop falls inside the
     jail box, then shoot the hall again. Main is not affected: main's stop 2 is at 3704,2605 with its sign at
     3704,2604, 30 tiles north of main's jail wall.

## Checked and fine (both builds unless named)

- **Walls and corners.** On main, the post 0x0036 is at the NW (3702,2634) and the L 0x0033 at the SE (3712,2642).
  0x0034 runs along the north row to the NE tile and along the south row. 0x0035 runs down the west column to the SW
  tile and down the east column. The windows are 0x003B in the south wall and 0x003C in the west and east walls, as
  in 2.2. The release matches at 3469,2597. The floor sits under the south row and east column, not under the north
  row or west column.
- **Cell fronts (P828 items 1 and 2).** The bars are 0x0823 with gates 0x0828 and the divider ends are L corner
  0x0033. In the roof-off renders and the TazUO hall shots, each front is one closed line. It runs from the west wall,
  through the brick ends of the dividers, to the east wall, with no stubs and no floor showing through, on both builds.
- **Candelabra (P828 advice).** 0x0B26 is at 3703,2638 (release 3470,2601). That is off the gate line and off the
  west window's floor tile. With the roof on there is no patch on the eave.
- **Door.** MetalDoor WestCCW at 3707,2642 (release 3474,2605) is hung in the south wall line. Its approach is clear
  outside on both builds. The walks went in and out through it (23 PASS each).
- **Roof.** Shingles 0x05C4/0x05C2/0x05C3 cover x0+1..x1+1 and y0+1..y1+1, with eaves at floor + 19 and the ridge
  on the middle column. The grey brick gable 0x0055 fills the south wall's row. The roof sits on the walls with nothing
  on it, in both roof-on renders.
- **Sign.** Hanger 0x0B98 and brass board 0x0BD2 ("The New Haven Jail") are just outside the south wall, two tiles
  east of the door, at floor - 2. They read clearly in both outside shots and stay off the door leaf.
- **Wall items and furnishing.** Shackles 0x1262 hang on the north wall of the west and east cells. There is hay in
  each cell. The writing table 0x0B4A has the ledger and a scroll on it, and the warden stands west of it. Each
  window's inside floor tile is clear.
- **Not a FAIL item, advice only.** Bench 0x0B2C at 3710-3711,2638 (release 3477-3478,2601) stands across Black
  Tam's locked gate at 3711,2637. The gate is a static that nobody walks through, so this breaks no rule, but the
  bench could move one tile west or onto the south wall, as the candelabra did.
- No stairs, bridges, docks, shores or foliage are in this build.

P842 DONE
