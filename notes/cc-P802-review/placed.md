# cc-P802: placed pieces (New Haven, Trammel)

Two builds carry this prompt:
- **main:** the town at x 3600-3760 (HavenSpots on main).
- **release/isle-20261028:** the ML plaza at x 3400-3560, which testers play.

Each section says which build it is for. Lesson props are made by a lesson when it starts and taken away when it ends; they are listed with their tiles, but nothing stays in the world. Tiles were checked on the shard's map files, with renders in `places/` (main) and `places-release/` (release); see `notes/cc-P802-tools/lesson-places*.json`.

## main: NPCs seeded with New Haven's pieces (TutorialWingTrials.SeedTeachers, at every world load; moved back to spot and facing)

| Piece | Where (x,y,z) | Facing | What |
|---|---|---|---|
| TutorialLessonTeacher "Ilyra Moonwhisper, the adjunct instructor of Mysticism" (elf body 0x25E, robe 0x48D, elven boots) | 3652,2473,0 | South | Haven Magery School south room, behind the table (3650-3652,2474-2475), facing the door gap 3651-3652,2479 |
| TutorialLessonTeacher "Morvain Ashgrave, keeper of the necromancer's shrine" (body 0x190, black robe 0x455) | 3693,2475,2 | West | on the skull-candle dais (3690-3694,2472-2478), behind the candle line, facing the room |

## main: lesson spots (per trial; nothing permanent)

| Lesson | Arm tile | Lesson props (made at arm, gone at end) | Fixtures used |
|---|---|---|---|
| magic.mysticism | 3653,2477,0 | training echo 3654,2475,0 | the school's table |
| magic.necromancy | 3686,2475,0 | training echo 3688,2475,0 | skull-candle dais |
| gathering.lumberjacking | 3744,2699,40 | none (was 2 practice-tree statics) | oak 0x0CDA 3744,2700,40 |
| gathering.fishing | 3650,2667,-2 | none (was a 2x2 practice pond) | water 3651,2667,-5 |
| gathering.camping | 3709,2606,20 | HerbPatch "wild garlic" 3711,2607,20 | none |
| crafting.blacksmithy | 3645,2616,0 | anvil 3646,2617,0 and forge 3646,2618,0, only when the town's are missing | [Decorate] AnvilSouth 3644,2615; SmallForge 3644,2614 |
| crafting.tailoring | 3676,2475,0 | none | none |
| crafting.carpentry | 3642,2499,0 | none | boards, counter |
| crafting.tinkering | 3666,2506,0 | none | tinker's bench |
| crafting.alchemy | 3628,2547,0 | none | reagent table |
| crafting.fletching | 3745,2579,40 | none | archery buttes |
| crafting.cooking | 3667,2643,0 | none | oven, hearth |
| crafting.inscription | 3612,2475,0 | none | reading tables |
| crafting.cartography | 3630,2634,0 | none | bookcases |
| thieving.trial | 3696,2509,0 | mark echo 3697,2509,0; WoodenChest 3699,2509,0 | pickpocket dips |
| travel.wing | public moongate (HavenSpots.PublicMoongate) | none (loans only) | the moongate |

## Removed (both builds): the old P276 farm west of the ML plaza

TutorialFarmAddon at 3377,2611,15 (330 pieces, `TutorialFarmLayout`), its DarkWoodDoor at 3380,2611,22, the pen spawner and its animals (`TutorialFarm.HavenSpawnerRows`). Removed at every start by `TutorialFarm.ClearHavenOnLoad`, only those pieces. Map statics are untouched, and P276's tree removals were already dropped from the map patch.
