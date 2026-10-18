# Art spec: fox ears and tail, the actions still without frames (for Chase's AI art chat)

Written 2026-10-17 by cc-P138. The worn item is Animation 4783 (slot 400 of our `sl-anim7.bin`), drawn over the
wearer's body frame by frame. What exists today, all made from the art chat's stage-3 walk and the stage-4 generator:

| Action (people layout) | Frames | Status |
|---|---|---|
| 0 walk, unarmed | 10 x 5 directions | the art chat (dir 1) and stage 4 (dirs 0, 2, 3, 4), 2026-10-05/06 |
| 2 run, unarmed | 10 x 5 | cc-P138, moved from the walk art by the per-frame guides |
| 4 stand | 1 x 5 | cc-P138, the same way |
| everything else (war-mode walk 1 and run 3, stand-and-fight 7/8, attacks 9-14 and 26-34, fidgets 5/6, cast 15-16, bow 18-20, hit 17, die 21-22, mount 23-25) | none | the ears and tail vanish while the body plays them |

Nothing here needs new *shapes*: the ears and the tail are the same sprites in every frame. What is missing is
**placement per frame**, which is what the generator does from `reference\8x\frame-guides.json` (per frame: the
crown row, the head's x range, the lower-back row and the body's x range there). So the cheapest route is not the
art chat at all: extend `frame-guides.json` to the other actions and run the generator (`design\kitsune-ears-tail\
build_stage4_walk_remaining.py` for directions 0, 2, 3, 4; `notes\cc-P138-scratch\build_stand_run.py` shows how
direction 1 is moved from the hand-drawn walk). Each guide row is read off the body's frame (body 401, action, direction,
frame; `notes\cc-P59-scratch\p59anim.py` decodes them).

If the art chat is used anyway, the rules are P62's, unchanged:

- Canvas 130 x 128 per frame, named `a<action:02>_d<direction>_f<frame:02>.png`, canvas pixel (x, y) is body-relative
  (x - 67, y - 98); fully transparent or fully opaque pixels only; no pure black.
- The ears sit on the crown: their bottom row is the body's first opaque row in that frame (`crown_y`), centred on
  the head (`head_x`). In directions 2 and 3 the far ear is the small one, as stage 4 draws it.
- The tail leaves the body at the lower-back row (`lower_back_row`), at the centre of `body_x_at_lower_back`. In
  directions 0, 1 and 2 she faces the viewer or is in profile, and the tail is **behind** her: every tail pixel that
  the body covers in that frame is left transparent (the client draws the item over the body and nothing can draw
  under it). In directions 3 and 4 she faces away and the tail hangs over her back and legs.
- The reference body frames are in `design\kitsune-ears-tail\reference\8x\body-frames\` (8x) and the plain
  silhouettes in `reference\8x\silhouettes\` (walk, run and stand only so far; the others must be rendered from
  `anim.mul` with `p59anim.py` or `scripts\validate-art.py render 401 <action> <direction>`).
- Deliver at 8x (1040 x 1024) if drawn by hand, as before; `scripts\build-equip-anims.py` encodes the 1x PNGs.

Priority if any of this is done: war-mode walk and run (actions 1 and 3; the body uses them whenever a weapon is held
or war mode is on, so the ears and tail disappear in a fight), then the fidgets (5, 6), then the rest.
