# F-35 evo pets: hand-off for the new chat (overseer, 2026-10-05 10:36)

Read first: `notes\cc-P59-evo-pet-body-sheet.md` (all of it; "Proposed stages" and "Decisions for Chase"), the F-35
entry in `docs\feature-queue.md`, and the four sheets in `notes\cc-P59-scratch\` (`sheet-dog.png`, `sheet-cat.png`,
`sheet-fox.png`, `sheet-bird.png`).

## Chase's answers to P59's decisions (2026-10-05 10:35)

1. Recolors count as the same creature, so none is a stage (P59 decision 1, accepted with 3 below).
2. **Third-party art: yes, use it** (fox and bird lines). That needs a route to ship custom creature art in the
   player package, which does not exist today; it is part of this work.
3. **Fox line: the top stage is a human kitsune.** The kitsune ears and tail art is being made now in another chat
   (`D:\ShatteredLegacy\design\kitsune-ears-tail\`, uncommitted, in progress). So the fox line is not capped at 3:
   1423 Small Fox, L_Fox.vd, 246 Bake Kitsune, then the human kitsune form. Whether a mid fox is still needed is open.
4. **Stage 1 puppy and kitten (Dog 217, Cat 201) are accepted** even though they are common town critters.
5. **Body table entries:** every chosen unused body gets a correct `bodyTable.cfg` type (Animal) in the F-35 build,
   or the pet can open doors and loses idle and feed animations.

Stage picks not separately answered; P59's recommended lines stand as the working draft:
- Dog: 217, 739 Leather Wolf, 1547 Alaskan Malamute, 277 Cu Sidhe, 1410 Windrunner.
- Cat: 201, 1309 Baby Tiger, 1254 Tiger, 1416 Sabertooth, 1573 Manticore (large).
- Bird: 254 Crane, 1440 Peacock, L_Bird 01.vd, L_Griffin.vd, 243 Lesser Hiryu.

## Overseer rules for prompts from that chat

Leave prompts unnumbered (`D:\UO\cc-prompts\cc-P-*.md`); the overseer numbers them. Every prompt ends with a
"Patch notes" section and a "Finishing" section (`Pnn DONE`). Builders run one at a time in `D:\ShatteredLegacy`.
