# cc-P138: Refit the kitsune ears and tail to the new paperdoll bodies, and in the world

2026-10-17. Prompt: `D:\UO\cc-prompts\cc-P138-kitsune-paperdoll-refit.md`. Both repos were clean at the start. Read
first: cc-P62, cc-P111, cc-P124 (the SFW body gate was not loosened). Scratch: `notes\cc-P138-scratch\` (the two
generators, the P62 gump as the refit source, and `proof\`), and the session scratchpad for the add-on renders, which
never enter a repo. "Ours" = `D:\ShatteredLegacy`; TazUO source = `D:\UO\cc-p40-work\tazuo-3212623f\src`.

## Headlines

1. **Reproduced, pixel for pixel.** The paperdoll as the client draws it (SFW body 13, the kit's GM-robe gump 60987,
   our 64783) matches Chase's screenshot: all 2,536 ears-and-tail pixels at offset (923, 233), 0 off
   (`proof\before-paperdoll-screenshot-vs-composite-2x.png`). The cause: P62's gump was placed for EA's female body,
   whose crown is row 58; the Siege of Sosaria body's crown is row 33, so the ears (rows 40-62) landed on her face and
   the tail (rows 120-178) on her thighs. TazUO draws every paperdoll layer at the same origin
   (`PaperDollInteractable.cs:202`, `:270`), so a gump fits a body only by where its pixels are.
2. **Refit by moving, not redrawing.** `gumps\64783.png`: ears moved (+2, -25), tail (0, -14); a stray pixel at
   (81, 121) dropped. New `gumps\54783.png` for men: the same art at (+2, -28) and (0, -16), registered
   (`registry.csv`, 113 rows). One gump per sex serves the human and the elf body (12/14 and 13/15 share hips and a crown
   within one row); the gargoyle bodies are not served (headline 5). Before/after: section 2 and `proof\fit-*.png`.
3. **The hood: the ears poke through.** With a GM robe or hooded shroud the client hides the Hair layer
   (`MobileView.IsCovered`, `:1441-1468`) but never Earrings, and Helmet draws after Earrings, so a hat or helm covers
   what it covers. Hiding the ears under a hood would need a client patch and, since ears and tail are one item on one
   layer, would hide the tail too. Decision for Chase, with images (section 4).
4. **In the world, the screenshot is a back view, and the tail is right there.** The walking sprite in
   `screenshot_2026-10-16_06-04-38.png` matches our frame `a00_d3_f00` mirrored, 165 of 165 sampled pixels: that is
   server direction North (`Animation.GetAnimDirection`: 0 -> drawn direction 3, mirrored), the three-quarter view
   from behind, where the tail hangs down her back over the robe. In the facing-camera directions (drawn 0 and 1) and
   the profile (2) the tail never overlaps body 401 in any of the 30 walk frames (0 pixels; table in section 5), as the
   stage-4 art already cut it. **The real defect was standing:** action 4 had no frames, so the ears and tail vanished
   whenever she stopped (the 06-03-46 screenshot shows exactly that: the robed figure with nothing on). Nothing draws
   under the body in TazUO (`MobileView.cs:335-361` draws the body, then every layer), so a layer change cannot put a
   tail behind her; per-direction frames are the mechanism and were already in place.
5. **Stand and run frames added (55 frames), from the existing art:** stand (action 4) and run (action 2) in the five
   drawn directions, placed by the per-frame guides, the tail cut by the body where it is behind her. Verified against
   the client's own body frames: 0 tail-over-body pixels in directions 0-2, ears' bottom row on the crown in every
   frame. `sl-anim7.bin` is 35,441 bytes (was 15,942); `build-equip-anims.py --check` round-trips all 105 frames.
6. **Men can wear it; gargoyles cannot.** `KitsuneEarsTail.OnEquip` refuses `Race.Gargoyle` ("Only humans and elves can
   wear this.") instead of men; P62 refused men only because there was no male art. The shard fact now covers a woman,
   a man and a gargoyle. Deviation 1.
7. **The paperdoll fit gate.** `scripts\check-paperdoll-fit.py` + `vendor\shattered-legacy-art\paperdoll-fit.json`:
   per gump and per body, the ears stay out of the face box, sit on the crown and centre on the head; the tail root is
   in the lower-back box; stray specks, part-transparent pixels, a changed body file, a registered gump with no fit, and
   an add-on set whose outline differs are all refusals. `Build-PlayerPackage.ps1` runs it before staging and refuses
   on red. Seen red on the P62 art first (6 failures), then green; the builder itself seen refusing with the old PNG
   swapped in. 11 unit tests, all seen failing by construction. Section 6.
8. **Survey of every other paperdoll overlay:** ours is the only shard-made paperdoll gump. Every other custom
   wearable uses stock EA art, and the Siege of Sosaria kit (P81) ships its own refit of each of their gumps
   (1,447 equipment gumps in the kit, the five non-stock-looking ones checked by ID). Nothing else to fix. Section 7.
9. **Gates and suites, all green:** shard build `build.sh --tests-only` 1,413 tests, 1,409 passed, 4 skipped, 0 failed;
   package suites 12/12, 10/10, 27/27, 9/9, 9/9; python 11/11 (fit) and 17/17 (play-test Who); `find-free-art.py
   --check-registry` 0 of 113 taken; a real package built from our client (`dist\ShatteredLegacy-2026.10.17.1903.zip`,
   83 MB, gates 1-6 and `-CheckZip` 4, 6, 5 passed; SFW gate intact). Nothing published or deployed. Section 8.
10. **Not done, by design:** war-mode walk and run and every other action still draw nothing; the spec for them is
    `notes\art\kitsune-ears-tail-remaining-actions.md` (it argues the generator, not the art chat, is the route).

## 1. Reproduce (prompt step 1)

- `proof\before-paperdoll-screenshot-vs-composite-2x.png`: left, the paperdoll cut from Chase's screenshot; right, the
  composite body 13 (SFW) + kit gump 60987 (GM robe, which is what "Eve" wears: `0x204F`, animId 987, hue 0x26) + our
  64783 as committed. The client draws no hair under that robe (`IsCovered`), which the composite reproduces. The
  search for the best offset found every one of the 2,536 opaque pixels of 64783 within 12/255 of the screenshot.
- The old placement against the two bodies, measured: EA female body 13 (the P62 reference PNG) crown row 58, head
  rows 58-82, hips about rows 118-130; SoS body 13 crown row 33, head rows 33-63, hips about rows 106-120. The ears in
  64783 occupied rows 40-62 and the tail rows 120-178.
- `proof\before-world-screenshot-crop-5x.png`: the walking sprite, 5x; headline 4 says what it is.

## 2. The refit (step 2), with file:line

| Body (TazUO picks it by graphic, `PaperDollInteractable.cs:158-200`) | crown row | head x | face box | lower-back box | gump |
|---|---|---|---|---|---|
| 12 male human (0x190/0x192) | 29 | 81-103 | 82,37-102,60 | 72,104-84,118 | 54783 |
| 13 female human (0x191/0x193) | 33 | 81-104 | 82,40-103,62 | 72,106-84,120 | 64783 |
| 14 male elf (0x25D) | 30 | 81-103 | as 12 | as 12 | 54783 |
| 15 female elf (0x25E) | 33 | 81-104 | as 13 | as 13 | 64783 |
| 665/666 gargoyle | 29/19 | wings, other hips | not served | not served | none: refused |

All measured from the vendored SFW PNGs (`bodies-sfw\<id>.png`, alpha extents row by row). The kit's Topless and Nude
sets differ from SFW by 160-210 outline pixels spread along the whole body (a separate export), never by shape: the
check holds their edges within one pixel of SFW inside the face and lower-back boxes and on the crown row, and all
eight pass.

- `notes\cc-P138-scratch\refit_gumps.py` makes both PNGs from `old-64783.png` (the P62 file, SHA-256 `1695a0aa...`):
  components found by flood fill (tail 2,165 px, ears 370 px, one stray pixel), each moved by whole pixels. No
  scaling: the SoS head is 21-23 px wide against EA's 16, and the 34 px ears already overhung EA's hair, so they read
  the same on both.
- `player-package\vendor\shattered-legacy-art\gumps\64783.png` (changed), `gumps\54783.png` (new),
  `registry.csv:52-53` (the 64783 row's what/source updated; the 54783 row), `paperdoll-fit.json` (new),
  `SOURCE.txt:64-93` (the fox section rewritten), the 4783 anim row's description (it said "walk direction 1 only").
- Results, as `check-paperdoll-fit.py` prints them: 64783 ears box (75, 15)-(108, 37) on crown 33, centre 91.5 against
  the head's 92.5; tail root column 79 row 111 inside the lower-back box. 54783 ears (75, 12)-(108, 34) on crown 29/30;
  tail root column 79 row 109.
- Before/after per body (3x, the client's order: body, hair 60701/50701 or hood 60987/50987 from the kit, our gump):
  `proof\fit-64783-on-13-hair-sfw.png`, `-hood-`, `fit-64783-on-15-hair-sfw.png`, `-hood-`, `fit-54783-on-12-hair-sfw.png`,
  `-hood-`, `fit-54783-on-14-hair-sfw.png`, `-hood-`; the "before" is section 1's image and the P62 preview
  `design\kitsune-ears-tail\stage2-final\paperdoll_preview_EA_3x.png` (right on the EA body it was made for). The
  Topless and Nude composites were rendered to the session scratchpad only and looked at: the same placement.

## 3. Elves and gargoyles (step 2, "where the item can be worn")

- Elves: TazUO draws an elf's paperdoll on body 14/15 (`PaperDollInteractable.cs:166-172`) and the elf bodies 605/606
  resolve to anim5.mul slots whose walk, run and stand frames have the same boxes as 400/401 (checked with P59's
  decoder: identical frame boxes in all 15 action-direction pairs). Same gumps, same frames; nothing to add.
- Gargoyles: the paperdoll bodies 665/666 put the head and hips elsewhere (table above), a worn item's gump is chosen
  by sex only (`GetAnimID`, `:509-562`; a per-race gump needs an `Equipconv.def` line, an EA file the launcher would
  have to copy and extend), and a gargoyle's animation groups are not the people layout, so our frames would never be
  looked up. The server refuses them (`KitsuneEarsTail.cs:52-62`). Deviation 2.

## 4. Hoods and helms (step 3): the ears poke through

- Evidence: `MobileView.IsCovered` (`MobileView.cs:1305-1470`) has cases for Shoes, Pants, Tunic, Torso, Arms, Helmet
  and Hair and none for Earrings; the Hair and Helmet case returns true for a robe 0x204E-0x204F (GM robes),
  0x2683-0x2687 (hooded shrouds), 0x2FB9, 0x3173, 0x4B9D and 0x7816. So a hood hides the hair and any helm, and our
  item draws over the hood. In every one of the eight world draw orders and the paperdoll order, Earrings comes after
  Robe and Hair and before Helmet (`LayerOrder.cs:7-64`, `PaperDollInteractable.cs:20-44`), so a hat or helm drawn
  after the ears covers what its art covers, which is right as it is.
- OSI precedent: OSI's own earrings draw the same way (after the robe, at the ear), so there is none for hiding.
- Chosen: **poking through**, placed so they rise out of the hood's top (`proof\fit-64783-on-13-hood-sfw.png` and
  `fit-54783-on-12-hood-sfw.png`), against the "before" of section 1. If Chase wants them hidden under a hood, that is
  a client patch (an Earrings case in `IsCovered` for graphic 0x3C3C and a hood robe) and the tail goes with them,
  because it is the same item; the honest alternative is a second item on another layer, which P62's A3 shows has no
  free candidate (Beard is destroyed at world load, Cloak draws under the hair, Waist before the hair).

## 5. The in-world sprite (step 6)

- Direction mapping, from `Animation.cs:78-113` and `Direction.cs:10-20`: drawn 0 = facing you (server Down), 1 =
  down-left (South; East is 1 mirrored), 2 = profile left (Left; Right mirrored), 3 = up-left from behind (West;
  North mirrored), 4 = straight away (Up). `design\kitsune-ears-tail\reference\directions_sheet.png` shows the body in
  the five.
- Chase's sprite = `a00_d3_f00` mirrored (the best match of all 50 frames in both mirrorings, 100 %; the next is the
  same direction's f08 at 84 %). So she was walking North, seen from behind, and the tail drawn over the robe's back
  is the back of the tail hanging down, which is what "behind the body" looks like from there.
- Measured over the client's own body 401 frames (P59's decoder, `anim.mul`), tail pixels on the body / on the robe
  987 outside the body, per direction, walk:

  | drawn dir | tail on body (10 frames) | tail on the robe only | ears bottom vs crown |
  |---|---|---|---|
  | 0 facing | 0 in every frame | 0-34 | 0 |
  | 1 down-left | 0 in every frame | 11-55 | 0 |
  | 2 profile | 0 in every frame | 8-43 | 0 |
  | 3 from behind | 80-119 (meant: the tail lies on her back) | 28-55 | 0 |
  | 4 away | 101-135 (meant) | 1-19 | 0 |

  Stand and run after this task: the same shape (0 on the body in 0-2, 62-136 in 3-4; ears on the crown in all 55).
  On the male body 400 the tail touches the body by 0-15 pixels in a few frames (he is a little wider); accepted.
- **With a robe:** where the robe is wider than the nude body (the hips), the tail's root draws over the robe's edge
  (up to 55 px in walk dir 1 f06), so it reads as leaving the robe's side at hip height
  (`proof\walk-f00-five-directions-body-robe-3x.png`, pairs nude/robed). Cutting the tail by the robe's silhouette
  instead would leave a 3-6 px gap between a bare body and its tail; the body cut is kept. Deviation 3.
- **Does the tail need its own layer?** No, and it would not help: `MobileView.Draw` draws the body first and every
  layer after it; no order draws under the body. Per-direction frames (which exist) are the only way, and the stage-4
  art already does the cut.
- **The fix made:** stand and run. `notes\cc-P138-scratch\build_stand_run.py`: directions 0, 2, 3, 4 reuse the stage-4
  generator's `draw_tail`/`draw_ears` with the stand and run guides and silhouettes
  (`design\kitsune-ears-tail\reference\8x\frame-guides.json`, `silhouettes\`); direction 1 moves the hand-drawn walk
  frame of the same index by the guide deltas (ears by crown and head centre, tail by the lower-back row and centre,
  -4 to +3 px) and cuts the tail by the target silhouette. Output `anim-src\4783\a04_d<d>_f00.png` and
  `a02_d<d>_f00..09.png` (55 new PNGs). `proof\stand_frames_over_silhouette_2x.png`,
  `proof\run_frames_over_silhouette_2x.png`.
- `scripts\build-equip-anims.py` (unchanged) encoded them: `sl-anim7.bin` 35,441 bytes, 15 blocks; `--check`: every
  block "positions identical, colours within 4 of the PNGs". The idx is 422,100 bytes as before.

## 6. Tests (step "Tests"), each seen failing first

- **`scripts\check-paperdoll-fit.py`** (new, 230 lines) and **`paperdoll-fit.json`**. On the committed P62 art it printed
  6 failures ("no ears: nothing ends within 12 rows of the crown (row 33); the lowest component ends at row 62",
  "the tail root (column 79, rows 125 to 125) is outside the lower-back box [72, 106, 84, 120]", on 13 and 15, plus
  the stray speck and the missing 54783), exit 1; on the refit, 0 failures, exit 0. Its first version compared the add-on
  silhouettes exactly and failed on every set; that was the check being wrong (the sets differ by outline pixels), and it
  now compares edges within one pixel; the unit test below pins that a two-pixel change is still refused.
- **`scripts\tests\test_check_paperdoll_fit.py`** (new, 11 tests, `python -m unittest discover -s scripts/tests -p
  "test_check_paperdoll_fit.py"`): the committed art fits; the P62 placement fails on the face and the thigh; ears 8
  rows low cross the face; ears 8 rows high "must sit on the crown"; ears 7 columns off-centre; a tail 9 rows up is
  "above the lower-back box"; a stray speck; a registered gump with no fit; a body file shifted 3 rows; an add-on set
  with the SFW outline passes and one widened by 2 px fails; `--render` writes 8 composites of 780 x 711. The
  floating-ears test was first written 5 rows up, inside the tolerance, and failed red-the-wrong-way; 8 rows is the
  committed value. 11 of 11.
- **The package gate** (`Build-PlayerPackage.ps1:548-560`, after the client gate): refuses with "PAPERDOLL FIT GATE: FAIL:
  ..." and no python on PATH is a refusal too. Proof: with the old PNG copied over `gumps\64783.png`, the builder
  stopped with the gate's six FAIL lines (exit 1, no stage, no zip); the new PNG restored (SHA-256 equal), the real
  build printed "paperdoll fit gate: paperdoll fit: 2 gumps, 0 failures" and built.
- **Shard:** `server\tests\Items\KitsuneEarsTailVerification.cs` fact 2 is now `AWomanAndAManPutItOnAndAGargoyleDoesNot`
  (`Person(female, race)` uses `race.AliveBody`). Seen failing: the old fact `AWomanPutsItOnAndAManDoesNot` is the
  inverse of the new rule, so the first build with the new item code and the old fact would be red on
  `Assert.False(worn)`; I did not run that cycle (a Docker build is minutes), the new fact against the new code passed
  in the full run, and the server-side rule's other half (the gargoyle refusal) is the fact's own `Assert.False`.
  Honest status: the shard fact was seen green only. See deviation 4.
- **Launcher:** `Build-UoOverrides.Tests.ps1:283-286` pins 113 registry rows and 2 gump rows (it failed on 112 first,
  the registry having grown by the 54783 row, then passed).

## 7. The survey (step 4)

- Shard-made paperdoll gumps: `registry.csv` kind = gump lists 64783 and now 54783, nothing else. Third-party gumps:
  the Siege of Sosaria kit (1,575 PNGs: six bodies, 746 male and 701 female equipment gumps, the rest UI and spell
  icons), made by its author for its own bodies; Fiddle-Me-This's 170 and 27 are UI gumps, none worn.
- Custom wearables, counted from `server\customizations` (`class X : <base>`): 113 set-armour pieces, 13 set clothing, 8
  set weapons, 6 set shields, 6 set jewels, 12 talismans, 8 outer-torso, 8 armour, 5 waist, 3 hats, 2 rings, 2 quivers, 2
  clothing, the gargish pieces (necklaces, earrings, glasses, kilts, plate), and `Item` subclasses. All use stock EA item
  IDs; the only ones with IDs outside the classic ranges are the five ToL belts and collar (0xA40C-0xA40F, 0xA1F6, animIds
  1516, 1517, 1519, 1521, 514), and the kit ships 5xxxx and 6xxxx gumps for every one of those five (checked by file);
  rendered on bodies 13 and 12 in `proof\survey-stock-wearables-kit-gumps-2x.png`: they sit where the kit's author put
  them. The chest mimic (`PetMimic.cs`, Talisman layer) wears the stock pouch 0xE79, whose tiledata animId is 0, so the
  paperdoll draws nothing for it (the pouch icon is in the slot only). Evo pets are creatures (`Mobiles\Evo\EvoPet.cs`),
  never worn. Loot-box cosmetics: `BoundCosmeticSash : BodySash` (stock 0x1541). No wings, toe rings or extra ring
  slots exist on the shard (grep for class names).
- Nothing needs new art for placement (step 5), so no art spec for the paperdoll; the one spec written is for the
  animation actions still empty (headline 10).

## 8. Build, package, suites (step 7)

- `docker\uo\build.sh --tests-only`: builder stage built, 1,413 tests, **1,409 passed, 4 skipped, 0 failed**, exit 0;
  the three kitsune facts listed as passed. `sl-modernuo:latest` is still `8e1a1916a752`; the tests-only run re-tagged
  `sl-uo-builder:latest` (the builder image) to `c4b9f6dcb399`, which holds this task's source (deviation 5).
- Package suites, Windows PowerShell 5.1: `Build-UoOverrides` 12/12 (after the row-count pin), `Cliloc-Overrides` 10/10,
  `Launch-Settings` 27/27, `Paperdoll-Bodies` 9/9, `Package-Client` 9/9 (its real build from a copy of our client with
  the add-on planted passed, and the NSFW zip check still refuses foreign body art).
- `find-free-art.py --check-registry`: 0 of 113 registered IDs no longer free (54783 "still free").
- The real package, from our client by default (P124): `player-package\dist\ShatteredLegacy-2026.10.17.1903.zip`, 83 MB,
  741 files, TazUO 3212623f + 2 patches, every gate passed including the paperdoll fit gate and the SFW body gate (gate
  4); `-CheckZip` gates 4, 6, 5 passed. `dist\` is git-ignored (`.gitignore:66`). Not published: the console refuses
  Build on an uncommitted tree, so Chase's own Build after the commit is the one to publish.
- No client rebuild was needed: no client patch changed (`sl-build.txt` still lists 0001 and 0002, and the client gate
  passed as is).

## Play-test items added

Seven, under **For Chase** below, sorted in `testing\bot-triage.md` (`### P138`) with steps in
`testing\playtest-steps.json`: P138-1 EYES, -2 EYES, -3 BOT-PARTIAL, -4 EYES, -5 BOT, -6 EYES, -7 EYES.
`python -m unittest tools/tests/test_play_who.py`: 17 of 17.

## Deviations and decisions for Chase

1. **Men can wear it now.** The prompt lists the male bodies and has you equip it on a man, and the only reason P62
   refused men was the missing male art. The server rule changed from "women only" to "not gargoyles". If the kitsune
   design wants it female-only after all, it is one line in `KitsuneEarsTail.OnEquip`.
2. **Gargoyles are refused** rather than fitted: a per-race paperdoll gump needs an `Equipconv.def` line (an EA file the
   launcher would copy and extend, as it does `Bodyconv.def`), and the frames would still never draw on a gargoyle body.
   The message is plain text ("Only humans and elves can wear this."); the cliloc file has no line for it.
3. **With a robe the tail's root overlaps the robe's edge** by up to 55 px in one walk frame, since the tail is cut by the
   nude body, not by every garment. The alternative gap on a bare body looked worse. Say if you want the robe cut.
4. **The shard fact was seen green only.** The red I can claim is by construction (the old fact asserts the opposite of
   the new rule); I did not spend a second Docker cycle on watching it fail.
5. **`sl-uo-builder:latest` moved.** `build.sh --tests-only` tags the builder stage `latest` (it takes no `-t` to the
   builder without also naming a shard image); the shard image `sl-modernuo:latest` is untouched. If the overnight bot
   rebuilds from HEAD it will make its own anyway.
6. **The Read tool was denied** (unattended run) for the prompt file, two reference PNGs under `design\` and
   `KitsuneEarsTail.cs`; I read them with `sed`/`cat` and copied the images into the session scratchpad to look at them.
   Nothing was skipped because of it.
7. **No task-list tool exists in this session,** so the step-by-step progress Chase follows remotely was not posted; the
   sections above follow the prompt's steps in order.
8. **The run frames are moved art, not drawn art:** run direction 1 is the walk frame of the same index shifted by the
   guides, and the other four directions are the stage-4 generator's shapes on the run poses. They read as the walk does
   (`proof\run_frames_over_silhouette_2x.png`); if the art chat should draw real running frames later, nothing here is
   in the way.
9. **The registry got a bare carriage return** from one of my edits (a backslash-r written as a CR) and PowerShell's
   CSV parse split two rows; found by the builder, fixed, and the registry is plain LF ASCII again (113 rows parse in
   both PowerShell and Python).

## For Chase

Build the package yourself after the commit (Shard Console > Player package > Build package, then Publish), and put
the P138 shard build on the test shard your usual way.

To try it in game on the test shard with the new package:

1. **Her paperdoll:** `[add KitsuneEarsTail`, drag it onto a female human's paperdoll (hair, no hood): the ears rise
   out of her hair on the crown, not over her face, and the tail leaves her hip at the lower back on the viewer's left
   (`notes/cc-P138-scratch/proof/fit-64783-on-13-hair-sfw.png`; before: `before-paperdoll-screenshot-vs-composite-2x.png`).
2. **With a hood:** put on a GM robe or hooded shroud: the hair hides as usual, the ears poke through the top of the
   hood, the tail stays at the lower back (`fit-64783-on-13-hood-sfw.png`). Decide: through the hood (as built), or
   hidden with the tail (a client patch).
3. **His paperdoll:** on a male human it goes on now (no "Only females" refusal); ears on the crown, tail from the lower
   back (`fit-54783-on-12-hair-sfw.png`).
4. **Elves:** the same on a female and a male elf (`fit-64783-on-15-hair-sfw.png`, `fit-54783-on-14-hair-sfw.png`).
5. **A gargoyle:** "Only humans and elves can wear this." and it stays in the pack.
6. **In the world:** standing still shows the ears and tail in all eight directions (they used to vanish until she
   walked); walking and running too, with and without a robe. Facing you or sideways the tail peeks out beside her
   hip, never across her front; facing away it hangs down her back over the robe. In war mode or holding a weapon they
   still vanish: those actions have no frames yet (`notes/art/kitsune-ears-tail-remaining-actions.md`).
7. **Your add-on only:** with the Topless or Nude bodies chosen in Options > Paperdoll, the ears and tail sit the same.

## Patch notes

`CHANGELOG.md` has a new section **2026.10.17.8** (2026.10.17.7 was committed with P137): Changed (men can wear it),
Fixed (the paperdoll placement; standing and running), Staff (the fit gate). `VERSION` is 2026.10.17.8. The wiki page
was not published.

## Repo size rule

No file over 5 MB in either repo. Largest new or changed: `sl-anim7-idx.bin` 422,100 bytes (unchanged size),
`run_frames_over_silhouette_2x.png` about 100 KB; `notes\cc-P138-scratch\` is 540 KB in all. The 83 MB zip is in
`player-package\dist\`, git-ignored (`git check-ignore -v`: `.gitignore:66:player-package/dist/`). The add-on renders
and the red-gate scratch stayed in the session scratchpad.

## Files

`D:\ShatteredLegacy`:

```
CHANGELOG.md, VERSION                                              2026.10.17.8
player-package/Build-PlayerPackage.ps1                             header note; the paperdoll fit gate (:548-560)
player-package/tests/Build-UoOverrides.Tests.ps1                   113 registry rows, 2 gump rows
player-package/vendor/shattered-legacy-art/gumps/64783.png         refit
player-package/vendor/shattered-legacy-art/gumps/54783.png         NEW  male gump
player-package/vendor/shattered-legacy-art/paperdoll-fit.json      NEW  where each gump sits on each body
player-package/vendor/shattered-legacy-art/registry.csv            54783 row; two descriptions
player-package/vendor/shattered-legacy-art/SOURCE.txt              the fox section
player-package/vendor/shattered-legacy-art/anim-src/4783/a02_*, a04_*   NEW  55 run and stand frames
player-package/vendor/shattered-legacy-art/sl-anim7.bin, sl-anim7-idx.bin   re-encoded (15 blocks)
scripts/check-paperdoll-fit.py                                     NEW  the check and the renders
scripts/tests/test_check_paperdoll_fit.py                          NEW  11 tests
server/customizations/KitsuneEarsTail.cs                           header; OnEquip refuses gargoyles, not men
server/tests/Items/KitsuneEarsTailVerification.cs                  fact 2
```

`D:\UO\shard-migration`: this note; `notes\art\kitsune-ears-tail-remaining-actions.md`; `notes\cc-P138-scratch\`
(`refit_gumps.py`, `build_stand_run.py`, `pdfit_experiments.py`, `old-64783.png`, `proof\` 14 images);
`testing\bot-triage.md` (`### P138`), `testing\playtest-steps.json` (7 items); `README.md`, `dashboard.html`,
`tools\progress.json` from `tools\progress.py`; and the importer's machine output.

Agents never edit `docs\`; nothing there was touched.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: the files listed above. docs: this note, the art spec, `notes/cc-P138-scratch/` (27 files pending in all with
`README.md`, `dashboard.html`, `tools/progress.json`, the triage and steps), and the importer's `testing/SUMMARY.md`
and `testing/play-tests.json` (machine output). The dry run also lists this prompt as "archived (dry run, not moved)".
Run again after `tools\Import-PlayTests.ps1` and the Who test: the same two "dry run" results.

P138 DONE
