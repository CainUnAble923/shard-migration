# CC task P835: build review of P726 (the isle pet is a reward, and players can see their evo pet's progress)

## In plain words

- I checked the Iron Golem's P726 work (Pip the hurt farm boy now on a bench in the farmhouse, with blood on the floor and
  a new healing lesson signpost outside the door) before it goes to the isle.
- It fails the review: the work left no pictures of the new bench, blood and signpost and no list of what it placed, so
  nobody can check by eye that they look right.
- The Iron Golem gets a short fix-up: take the pictures, write the list, and check two things the guide flags (which way
  the bench faces, and that the signpost stands on the north side of its path).
- Nothing for you to do.

## What was reviewed

- Guide: `notes/guides/building-and-decorating.md` (the short checklist, sections 6 and 8, What to use where).
- `git fetch origin golem/Iron/P726` in both copies (branch left on `golem/Iron/P835`).
- `git ls-tree -r --name-only origin/golem/Iron/P726 -- notes/cc-P726-review` lists **nothing**: the branch has no
  `notes/cc-P726-review` folder, so no `placed.md`, no isorender and no TazUO shots. The only notes are
  `notes/cc-P726-isle-pet-reward.md` and the `notes/cc-P726-tools/` scripts and bot-run logs (transcripts, no images).
- Placement in code (`git diff main...origin/golem/Iron/P726`, ShatteredLegacy):
  - `TutorialFarm.PipProps`: bench 0x0B2D at 6692,3975,7 and 6692,3976,7 (inside the farmhouse, east wall); blood
    0x122A at 6691,3975,7, 0x122D at 6691,3976,7, 0x122C at 6691,3974,7; Pip (`TutorialWoundedHelper`, Direction West,
    RangeHome 0) at 6692,3975,7.
  - `TutorialCorePlacement.HealingSign`: the `core.healing` signpost at 6688,3980; its stop is the farmhouse door's step
    6690,3979.
  - `TutorialCloakChest` (0x0E43, the P728 cloak chest): appears on the clothes table; a runtime container, not a static.
- The pieces match the guide's choice for the hurt-NPC prop (section 6: bench 0x0B2D, blood 0x122A/0x122D/0x122C, NPC
  facing into the room, RangeHome 0) and the chest rule (Movable, refuses its own lift). Nothing could be checked by eye.

BUILD REVIEW P726: FAIL

1. No renders or placed list left for review: `notes/cc-P726-review/` is missing from `golem/Iron/P726`. The guide
   (checklist item 8, section 8) wants `notes/cc-P726-review/placed.md` with one line per piece (the bench 0x0B2D at
   6692,3975,7 and 6692,3976,7; blood 0x122A 6691,3975,7, 0x122D 6691,3976,7, 0x122C 6691,3974,7; the signpost 0xA854
   at 6688,3980; Pip at 6692,3975,7 facing West), an isorender of the farmhouse and its doorstep
   (`scripts/mapbuild/isorender.py map ...`, about 6684-6698, 3970-3984), and TazUO shots from the default camera on a
   private shard (port 2596): inside the farmhouse showing Pip on the bench with the blood, and outside the door showing
   the healing signpost readable.
2. Bench 0x0B2D, 6692,3975-3976,7 (farmhouse east wall): the guide (section 6) marks the bench's art facing and Pip's
   seated look as unverified ("check yours"). The inside shot must show the bench running north-south flush against the
   east wall, both tiles joined, with Pip on it facing west into the room; if 0x0B2D reads the wrong way, use the piece
   that does and say so in `placed.md`.
3. Signpost 0xA854, 6688,3980 (healing lesson, south-west of the farmhouse door): the guide (section 6, Chase 10-30)
   wants every sign **north** of the path it marks, beside it, facing it, and clear of the door's approach line for two
   tiles. At 6688,3980 it stands south of the doorstep row (3979). The render must show it on the north side of the walk
   it marks and off the door line; if the walk runs north of it, move it north of that walk (or explain in `placed.md`
   why this spot is the north side).

P835 DONE
