# cc-P850: build review of P848 (housing stop 2 moved out of the release jail)

## In plain words

- **P848 passes.** On the testers' New Haven, the housing lesson's second stop and its signpost now stand on the open
  lawn south of the town wall, east of the south road. They are no longer in the jail.
- **The stray signpost in the jail hall is gone**, also from a world that already had it. P848's shots of the hall
  show no post in front of the middle cell's gate.
- **The jail itself is unchanged** since P842 passed it on main, and it still matches the guide.
- **Nothing for you to do.** P848 can merge. There is one small piece of advice below, and it is not a fix.

Gold Golem, 2026-11-08, a fresh session that did not build P848. I read `notes\guides\building-and-decorating.md` in
full and fetched `origin/golem/Iron/P848` in both copies without changing branch. I extracted
`notes/cc-P848-review` to my scratchpad and read `placed.md`, P848's notes (`notes/cc-P848-fixup.md`, the prompt's
name for it, `cc-P848-fixup-jail-housing-stop.md`, is not on the branch), P842's review and the release diff's
changed lines. I looked at all three isorenders, `hall-before-after-isle.jpg` and the after shots 0, 1, 2, 2b, 3, 4
and 4b. Nothing was built or run.

## Verdict

BUILD REVIEW P848: PASS

## Checked, one by one

- **The folder and list (item 4).** `notes/cc-P848-review/` and its `placed.md` are present.
- **P842's item 1: fixed.**
  - In `before-housing-stop2.jpg` the blue sign and red stop 2 are inside the jail at 3474,2601 and 3474,2603.
  - In `after-housing-stop2.jpg` and the roofless render, the jail hall is empty of them. The sign (3481,2622) and
    stop 2 (3482,2623) stand on flat grass, well clear of:
    - the jail (17 rows south);
    - the palisade;
    - the south road;
    - the shore.
  - The release diff moves `HousingStop(1)` and the 0xA854 entry together. `StrayPieces` removes the old post, and
    the fact `Stop2SignInTheJailHallIsTakenAwayOnLoadOnce` pins this.
- **The sign (guide 6).**
  - It is the standing signpost 0xA854, the face that reads from the south. It is not a rune marker.
  - It stands within 2 of the stop and not on it, and it is on the stop's north side.
  - It is named "Housing lesson, stop 2: where houses can be built". In `2b-stop2-sign-on-the-lawn.jpg` the name
    reads over the post when clicked.
  - The regenerated sign table puts no map static on its tile.
- **The hall (2.6, nothing stray).** `4-hall-no-signpost.jpg`, `4b-hall-by-the-cells.jpg` and the after half of
  `hall-before-after-isle.jpg` show this run of the hall: no post at the middle gate, and the walk log reads "no
  signpost anywhere in the jail (0)".
- **The lesson text (guide 7).** Stop 1's text says where stop 2 is now. Stop 2's window ends with stop 3 said
  plainly (shots 1 and 2), and no line says "0 more".
- **The jail, unchanged from P838 and re-checked against `placed.md` and the renders:**
  - **Walls.** Post 0x0036 is at the NW and the L corner 0x0033 at the SE. The "south" piece 0x0034 runs to the NE
    tile, and the "east" piece 0x0035 runs to the SW tile.
  - **Windows.** 0x003B is in the south wall and 0x003C in the west and east walls.
  - **Roof.** The 0x05C4/0x05C2/0x05C3 shingles cover x0+1..x1+1 and y0+1..y1+1, with the ridge on the middle column.
    The 0x0055 gable fills the south row, and nothing sits on the roof.
  - **Door and sign.** The MetalDoor WestCCW is in the south wall line (shot 3 shows it shut in the wall). The 0x0B98
    hanger and 0x0BD2 board stand two tiles east of the door.
  - **Cell fronts.** The bars and gates form one closed line in the roofless render.
- **Not in this build.** There are no stairs, bridges, docks, shores or foliage in it.
- **What to use where.** The only new piece is the Haven's standard signpost 0xA854, the right piece for a lesson
  stop on open ground.

## Advice (not a FAIL item)

- The sign 0xA854 at 3481,2622 stands one tile north-west of stop 2. That puts it on the straight line from the road
  gate (about 3474,2619) to the stop, so a player who walks straight there meets the post one step early and steps
  round it. The lawn is open, so nothing is blocked; P848's walker reached the stop. If the spot is ever touched
  again, 3482,2621 (two tiles north of the stop) keeps the sign north of the stop and off that line.
- P842's advice still stands: bench 0x0B2C at 3477-3478,2601 sits across Black Tam's locked gate.

P850 DONE
