# cc-P844: placed pieces (P721's, as main has them now, after P834's build review)

The Wakening Isle, map 32 (the Fold) and every isle copy, isle coordinates. All of these are **server items** that the
world-load seed places and upgrades (`TutorialCorePlacement.SeedOn`, `TutorialFarm`). None is a map static. "ground Z"
is the land's Z, which is 0 at every spot below.

## Changed by cc-P844

- 0x0B2C wooden bench, 6704,3975,7 and 6704,3976,7: Pip's bench along the farmhouse's east wall, two tiles in a
  north-south line, one joined bench. It was **0x0B2D**, which runs east-west, so it drew as two crosswise stubs
  (`bench-0B2D-left-0B2C-right.png`, `before-tazuo-pip-on-bench.jpg`). On a world laid before, the seed takes the
  0x0B2D pieces off these two tiles and lays 0x0B2C (`TutorialFarm.TakeAwayOldPipBench`).

Nothing else moved.

## The clothes stop (core.paperdoll; TutorialWorld.Rack = 6665,3992)

- 0x0B8F table, 6664,3990, ground Z, faces south to the road: the clothes table (Rack -1,-2), north of the road (P718).
- 0x0EC6 clothes rack, 6665,3990, ground Z: beside the table (Rack +0,-2).
- 0xA854 standing signpost, 6665,3989, ground Z, faces south to its path: the core.paperdoll lesson sign.

## The chat stop (core.chat; TutorialWorld.Signpost = 6692,3990)

- 0xA854 standing signpost "Farm signpost: say 'I am ready to learn'", 6690,3986, ground Z, faces south to the road:
  the chat signpost at Signpost -2,-4, north of the road (guide section 6). Its old spot, Signpost +0,-2 (6692,3988),
  is cleared by `MoveChatSignpost`.
- 0xA854 standing signpost, 6691,3987, ground Z, faces south: the core.chat lesson sign.

## The farm gate and stop (core.farm, core.healing)

- 0xA854 standing signpost "Farm signpost: Wren the Farmhand at the gate", 6697,3977, 0, faces south: the farm gate's
  signpost. It is part of the farm addon, which swaps the layout's old wall arm 0x0B97 + board 0x0BCF for this post
  (`TutorialFarm.IsleArt`, `FixGateSign`).
- 0xA854 standing signpost, 6698,3978, ground Z, faces south: the core.farm lesson sign.
- 0x0843 field gate (TutorialPestGate : LightWoodGate, NorthCCW, shut; art read live in `tour-walk.log`), 6695,3979, ground Z: the one gate
  in the field's east fence, on the gap's south tile. It swings north-east onto Wren's tile when open.
- 0x0837 wooden fence, 6695,3978, ground Z, north-south: closes the gap's north tile beside the gate. The old gate and
  fence at 6713,3979 and 6713,3978 (P721's spots, before the field moved 18 west in P741) are cleared by
  `MoveFromOldLayout`.
- Wren the Farmhand (TutorialFarmhand), 6696,3978, ground Z, facing east: at the gate.
- 0xA854 standing signpost, 6701,3980, ground Z, faces south to the road: the core.healing lesson sign, south-west of
  the farmhouse steps.

## Pip in the farmhouse (core.healing)

- 0x0B2C wooden bench x2, 6704,3975,7 and 6704,3976,7, north-south, against the east wall (cc-P844, above).
- 0x122A blood, 6703,3975,7; 0x122D blood, 6703,3976,7; 0x122C blood, 6703,3974,7: on the floor beside the bench.
- Pip (TutorialWoundedHelper), 6704,3975,7, facing west into the room, `RangeHome = 0`: seated on the bench. P721's
  spot 6715,3981 (standing, no bench, no blood) and P726's 6692,3975 are cleared or moved by the seed.
- TutorialTableBandages, 6702,3975,13: the bandages on the farmhouse table beside him (P740).

## The vision scene's braziers

- 0x0E31 brazier x2, at chamber offsets (6,2,0) and (2,6,0) of each scene slot: slot n's corner is
  (6170 + 28n, 3752, 0), so slot 0's braziers are 6176,3754,0 and 6172,3758,0. They stand either side of the Gem's
  pedestal 0x1223 at (4,4). P721 placed braziers by the Gem at the wake spot. Since P742, the scene runs in this chamber
  (`TutorialVisionChamberLayout`). Its renders, shots and full list are P742's: `notes/cc-P742-review/`
  (`render-chamber.png`, `tazuo-vision-02-shrine-lit.jpg`, `placed.md`).
