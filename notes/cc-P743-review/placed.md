# cc-P743: what is placed in New Haven

Every piece is seeded at world load by the tutorial seeder (`TutorialCorePlacement.SeedOn` with New Haven, which calls
`TutorialWingTrials.SeedHaven`, `server/customizations/Tutorial/NewHavenLessons.cs` `HavenPieces`), idempotently, test
shard only (as the rest of the tutorial). Statics are `Static` items named as below. Facing: these pieces have one art
each; the bench runs east-west (0x0B2C, rendered in `render-rook-bench.jpg` and `notes/cc-P743-tools/renders/bench.jpg`).

## Rook (item 6)

- 0x0B2C wooden bench, 3669,2636,0, east-west, Rook's seat (Rook stands on it, facing North, toward the square).
- 0x0B2C wooden bench, 3670,2636,0, east-west, the bench's east half.
- Rook (TutorialRecruiter) 3669,2636,0, North. An older world's Rook on the square (3631,2584,0) is moved here.
- The isle moongate's exit (HavenSpots.MoongateExit) 3669,2634,0, two tiles north of the bench, on the grass by the path.
- Not placed: the quest board, the reset stone and the Fountain of Youth stay on the square.

## Mining (item 3)

- 0xA854 signpost "The mountain path: the mining lesson's cave is west, round the hill", 3702,2745 (land Z), north of the
  dirt path that starts at about 3704,2747 and runs west to the hillside building and round the hill.
- No vein prop: the lesson digs the cave's own floor (cave floor statics 3610-3613, 2742-2744, Z 9).

## Stables (item 4), the barn of Uzeraan's mansion (3595-3607 x 2610-2621, door east 3607,2615-2616)

- 0xA854 signpost "The stables: the sick-bay stall is inside, on the left", 3610,2613 (land Z), north of the walk to the
  barn door.
- 0x0FFA bucket of water, 3605,2620,0, in the south-east stall (the sick-bay stall).
- 0x1036 clean straw, 3606,2619,0, same stall.
- 0x0F34 clean straw, 3605,2619,0, same stall (the map's own hay and water trough 3604,2619-2620 are there already).
- Per lesson, not seeded: the injured horse (TutorialStableHorse) at 3606,2620,0, seen only by its trainee.

## Housing (item 9)

- 0xA854 signpost "Housing lesson, stop 1: a small house", 3713,2591 (land Z), east of the cottage's south wall, the
  dirt path south of it. Stop 1 is 3709,2594 on that path.
- 0xA854 signpost "Housing lesson, stop 2: where houses can be built", 3704,2604 (land Z), on the open grass south of the
  cottage, clear of the trees (P750's cover model: board and stop figure 0% covered). Stop 2 is 3704,2605.
- Stop 3 is the bank (ClusterFNewHavenSeeder.BankAnchor); the bank has its own sign.

## Taken away (item 2)

- TutorialFarmAddon at 3377,2611,15 (P276's whole farm: farmhouse, fences, pen, crops, hay, scarecrows, well, coop,
  troughs, bench, signpost), its DarkWoodDoor at 3380,2611,22, and the pen spawner at 3395,2606 with its animals. The
  SoS land there was never changed by a map op, so no ground needs restoring.

## Lesson places (no pieces placed; the lessons' own echoes appear when a lesson starts)

- Sparring (combat.weapons): the Proving Grounds, player 3731,2583,40, sparring echo 3733,2580,40.
- Magery: the Haven Magery School's south room, player 3651,2477,0, training echo 3654,2472,0, mage echo 3650,2471,0.
- Bard: the Bardic Guild's hall, player 3663,2531,0, echoes 3668,2530,0 and 3669,2531,0.
