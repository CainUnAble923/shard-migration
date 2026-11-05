# cc-P799: New Haven fixes: a working League ankh, music in the theater, the mine, the stables, and P743/P755 on the isle branch

## In plain words

- **The ankh outside the League building now brings ghosts back to life.** It appears by itself on the testers' world. A ghost walked up to it in the real game, on both the testers' version and main.
- **The New Haven lessons testers play now happen in fitting places.** Music is in the theater, mining is at the mine south of town by Jacob Waltz's camp, and Animals is at the stables. Animals no longer shows done on arrival: you bandage a hurt horse, then tame it and keep it. Sparring, magery, Rook's bench and the housing stops came over as well.
- **The Animals lesson had never really worked, on main either.** A real player could neither bandage the horse nor tame it from where they stood. The earlier tests skipped those steps. Both are fixed on both branches and played through in the real game.
- **For you:** the overseer applies `notes\cc-P799-tools\p799-release-isle-20261028.diff` to the release branch and ships it. Please decide three things, listed under "Decisions for Chase": main has no theater, Rook's bench is by the Inn rather than a tavern, and the stock town's mine is an open ravine rather than a cave.

## State

Iron Golem, 2026-11-05. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`, both on `golem/Iron/P799`, not
committed by me. Release copy: `D:\UO\golems\Iron\p799-isle`, a detached worktree at `e8d210c` (the `release/isle-20261028` tip) with the change staged;
mine to remove after the merge. Nothing was committed to the release branch, nothing deployed, `latest` not moved. All play was on the private proof
shard, 127.0.0.1:2596.

| Build | Image | Result |
|---|---|---|
| Isle release | `sl-modernuo:cc-p799-isle`, version 2026.11.05.1 | **EXIT=0, 2893 passed**, 0 failed, of 2898 (`gated-build-isle.log`) |
| Main | `sl-modernuo:cc-p799`, version 2026.11.05.2 | **EXIT=0, 3098 passed**, 0 failed, of 3104 (`gated-build.log`) |

## Items 1 to 3: the ankh

| | Release (stock map) | Main (SoS map) |
|---|---|---|
| The art | map statics 0x0003 at 3464,2600,27 and 0x0002 at 3464,2601,27, facing west | no ankh static near the League hall |
| The working ankh | AnkhWest over those statics, same art and facing | AnkhWest at 3676,2562-2563,0, by the hall's south-east corner (P137's and P678's spot) |
| Proof shard log | `League ankh: placed at (3464, 2600, 27).` | `League ankh: placed at (3676, 2562, 0).` |
| In TazUO | ghost at 3465,2600 takes the offer: resurrected | ghost at 3677,2562: resurrected |

**Why it had not worked.** Chase asked for this on 10-16, and P137 built the entry. It placed only through `[ClusterFSeedAnkhs` or
`clusterf.ankhs.seedOnWorldLoad`, which is False, so a world already running never got it. Fix: `SeedLeagueAnkh` runs after every world load, places it
only where no working ankh stands, and has its own setting, `clusterf.ankhs.leagueAnkhOnWorldLoad`, default True.

**The prompt's "stop placing the static" does not apply.** The art is in the client's map, so the server cannot remove it. As OSI does, the working
item stands on top. Nothing is deleted.

**Other ankhs (item 3), none changed:**

- Release: no decoration-only ankh in New Haven. The League statics were the only ankh statics on Haven island. The working AnkhNorth at 3526,2516 is P137's record of P17's seeder; I did not check it in game.
- Main: one decoration-only ankh on the island, the bloodied static 0x1E5D and 0x1E5C at 3359-3360,2677,59.

## Item 7: P743 and P755 on the release

Taken as the merge's own change (`7147517`, `feature-7147517.diff`), applied with `git apply -3`. `HavenMoveVerification.cs` is left out: it tests a move
the release never had. Conflicts in `HavenSpots`, `TutorialStations` and `TutorialTradeTrials` were resolved toward the release.

**The real work was the map.** P743's places are coordinates on main's SoS town, so each needed a stock site. The survey is `notes\cc-P799-tools\stock-sites.md`.

| P743 on main | On the release | Spot |
|---|---|---|
| Proving Grounds | Warrior Guild's yard | 3529,2544,20; echo 3531,2541,20 |
| Haven Magery School | Magery School's south room | 3486,2501,52; echoes 3484,2497,52 and 3488,2500,52 |
| Bardic Guild | **the theater** | 3414,2602,55; echoes on the stage 3410,2603,60 and 3411,2604,60 |
| Cave on the mountain path | **the mine by Jacob Waltz's camp** | 3514,2747,0, 12 tiles in one ore bank |
| Uzeraan's barn | **the stables east of the square** | 3534,2577,7; stall 3534,2575,7 |
| Rook by the Albatross | Rook by the Bountiful Harvest Inn | 3502,2530,22; moongate exit 3502,2532,22 |
| Housing stops | beside the League cottage, then the lawn east of it | 3465,2596; 3474,2603 |

**What could not come over as it was (the map swap's land):** the palisade yard, the cave floor, the barn with troughs, and the Albatross patio do not exist on
stock. Each has the nearest stock place above. The stall's two straw piles are left out, as the stock stall has hay. Nothing was dropped.

## Items 4 to 6, and why they did not stick (the overseer's question)

| Asked 10-30 | Answer |
|---|---|
| Mining to the mountain and cave | **Built on main only.** P743 was correct there but never reached the release, whose lesson stayed in the trades yard. |
| Animals showing done | **Built on main only.** P743 removed the early completion in `TutorialFarm.CheckDone`; the release kept it. |
| Horse taming in the stables | **Built on main only, and built wrong.** Two bugs below, on both branches. |

**The two bugs.** P743 said the moving parts were proved by tests and not yet in a game window. Its facts called `horse.Heal` and set the master directly.

1. **Bandaging was refused:** "You cannot perform beneficial acts on your target". Trammel refuses a player's beneficial act on an uncontrolled creature. Fixed in `TutorialFarm.AllowBeneficial`, for that horse's own trainee only.
2. **Taming stopped quietly** unless you stood next to the horse. Pinned's taming needs a walkable path from the animal to the tamer, and the horse had `CantWalk`. Once healed it can walk now, held in its stall by a home range of 0, and the hint says to stand beside it.

**Music on main.** There is no theater on main's land, so it stays in the Bardic Guild. The survey also found that P743's "stage" there is a glass display case.

**"Trainer".** No lesson has a trainer NPC; Rook starts them all. The theater's stock bard guildmaster stands in its back room, 3410,2608,55.

## Tests

- **New facts:** `NewHavenStockSitesVerification` (release: theater, mine, stables, sites); in `AnkhVerification`, `TheLeagueAnkhReachesAnExistingWorldByItselfOnce` and `TheLeagueAnkhIsOnByDefaultWhateverTheOldSettingSays`; in `NewHavenFixesVerification`, `OnlyItsTraineeMayBandageTheStableHorse` and `TheRealTamingSkillTakesTheHealedHorse`.
- **Watched red** on the release's builder image (`mutant-logs\`), 8 mutants, all red: horse rule removed, ankh default off, ankh placed twice, theater moved, mine moved, "cave floor" text, Animals completing on the isle, horse still `CantWalk`. `m7.txt` shows the Animals mutant passing under a filter that left out `TutorialFarmVerification`; `m7b-animals-early.txt` is the real run, red. The mutants ran on the release only; the ankh and horse facts are the same on main.
- **Flake:** one isle run failed `CovetousVoidSpawnVerification`, a randomly placed spirit out of bounds (`flake-covetous-isle-run2.txt`). It has nothing to do with this work; the unchanged rerun passed, as did the later runs.

## In TazUO

Real client on the private shard, each a fresh character on the Player account, on a copy of the bot world, so an existing world. Staff moves came from
a second bot client (`stage799.py`), since staff cannot enter the tutorial.

- **Release:** all 9 checks pass (`cc-P799-review\shots-isle\walk.log`): ghost, resurrected, walked 182 steps from the square to the mine, pickaxe lent on arrival, dug ore from the rock wall, horse waiting, bandages lent, bandaged, tamed.
- **Main:** all 6 checks pass (`shots-main\walk.log`): ghost, resurrected, horse, bandages, bandaged, tamed.
- **Logs:** neither shard log shows an exception, read after decoding (they are UTF-16 with colour codes, so the earlier counts of 0 meant nothing).

**Not proved in the client:**

- The bard lesson played through, including the brawl. The shot shows the lesson open in the theater; facts cover the rest.
- Sparring, magery and housing played through. The shots show the places and signs only.
- The moongate arriving at Rook's bench, and an older world's Rook moving in a live load. Facts cover the move.
- Main's mining lesson (unchanged here).

## Review folder

`notes\cc-P799-review\`: `placed.md`, `renders\` (before pictures of each spot, and `before-trades-yard.jpg`, where these lessons were), `shots-isle\` and `shots-main\`
(after). The full runs are in `notes\cc-P799-shots-isle\` and `notes\cc-P799-shots-main\`. Some older frames in `cc-P799-shots-isle\` come from earlier runs; use the numbered shots.

## Decisions for Chase

- **Main has no theater.** Music stays in main's Bardic Guild. If you want a stage there, that is a build of its own.
- **Rook's bench on the release is by the Inn,** in its cobbled south yard, 45 steps north of the plaza, as there is no tavern patio near the square. The plaza is a fine fallback: tell me if you would rather he stayed.
- **The stock town's mine is an open ravine, not a cave.** The lesson says "the mine" and "the rock wall". The only cave floor on the stock island is in Uzeraan's ruin.
- **Mine route:** two routes tie at about 180 steps and one clips a shore cliff edge, so the arrow may lead that way. My walk finished without trouble. The sign stands on the road's east shoulder, because the road runs north-south there and has no north side.
- **Young ghosts (not changed).** Pinned moves a young player's ghost to 3665,2587, a spot on main's town, which on the stock map is well east of the stock town. I saw a trainee's ghost land there. Worth a look: a young ghost may not reach this ankh.

## Deviations

- **Main's image predates one CHANGELOG line** (the horse fix), added after its gated build and its proof. No code changed since.
- **`gated-build.ps1` first tagged main's image `cc-ShatteredLegacy`** through a typo of mine. I retagged it `cc-p799` and removed the wrong tag; it is the same image, and the log's "Built" line shows the old name.
- **The harness stopped one wait loop for low memory** while idle. The build it watched had already finished. I did not restart that loop; later builds ran in the foreground, each after a memory check.
- **The prompt names `sl-modernuo:cc-p799`, the hand-off `cc-P799`.** I used the prompt's lower-case tags.

## Files

- **ShatteredLegacy:** `server/customizations/ClusterFAnkhs.cs`, `Tutorial/NewHavenLessons.cs`, `Tutorial/TutorialFarm.cs`, `Tutorial/TutorialTradeTrials.cs`, `server/tests/Misc/AnkhVerification.cs`, `server/tests/Tutorial/NewHavenFixesVerification.cs`, `CHANGELOG.md`, `VERSION`.
- **Release:** `notes\cc-P799-tools\p799-release-isle-20261028.diff`, 24 files, against `e8d210c`.
- **shard-migration:** this file, `notes\cc-P799-tools\`, `notes\cc-P799-review\`, `notes\cc-P799-shots-isle\`, `notes\cc-P799-shots-main\`.

P799 DONE
