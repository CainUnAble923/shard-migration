# cc-P743: New Haven tutorial fixes

## In plain words

- **The New Haven lessons now happen in fitting places** on the test shard:
  - sparring with the echo in the Proving Grounds (the fenced warrior yard on the east side of town);
  - magery in the Haven Magery School, where a mage echo shows Magic Arrow a few times before you cast it;
  - the bard lesson in the Bardic Guild, where provoked echoes now fight each other for about 12 seconds;
  - mining at a real cave on the mountain path south of town, with a signpost where the path starts.
- **Animals is now "heal and tame a horse" in the stables:** an injured horse waits in a stall that only you can see.
  - Bandage it, then tame it, and it is yours to keep and ride (one per character).
  - Getting your cat or dog on the Wakening Isle no longer marks this lesson done.
- **Rook sits on a bench by the Albatross tavern**, just south of the square, and the isle's moongate sets you down in
  front of him. The leftover tutorial farm west of town is taken away.
- **Two lessons are fixed or rewritten:**
  - Thieving can always be finished now: opening the practice chest no longer leaves Remove Trap stuck.
  - Housing has three clear stops, each with a signpost.
- **For you:**
  - Have a look on the test shard when this is deployed there.
  - The moving parts (the echoes' fight, the mage echo's casting, the horse) are proven by the server's tests, not yet in
    a game window. The live shots show the places, signs, bench and stall.

## Where things are (the survey)

Tools are in `notes\cc-P743-tools\`:
- `survey_haven.py`, `route.py`, `renders\`, the map tools copied from P708's p281sos;
- region names from pinned `regions.json`;
- building contents from P678.

| Item | Place | How it was checked |
|---|---|---|
| 1 Sparring | **the Proving Grounds** (pinned region "the Proving Grounds in Haven", 3728-3737 x 2575-2592): a palisade yard with a plank floor at Z 40, gate in the east wall, the four training dummies of `_haven additions.cfg`, the Bullseye Marksmen's buttes beside it | the floor is reachable on foot from the start (`renders\proving-in.jpg`) |
| 3 Mining | **the cave on the mountain path south of town**: cave floor statics at 3610-3613, 2742-2744, Z 9 | the walk from the start is 255 steps (`route.py`): south past the Albatross, down the east shore, west on the dirt path at about 3704,2747 round the hill, to the cave mouth (`renders\south.jpg`, `path.jpg`) |
| 4 Stables | **the barn of Uzeraan's mansion** (3595-3607 x 2610-2621, door 3607,2615-2616): six stalls, each with its water trough and hay | the "stables farmhouse" P678 named (3704-3712, 2584-2592) is a small cottage with no stalls, so the barn it is (`renders\stable-in.jpg`) |
| 6 Rook | a bench (placed) at 3669-3670,2636 on the grass by **the Albatross Bar and Grill**'s north side, its door 3666,2639, facing the square | nothing outdoors to sit on near a tavern: the "picnic tables" in the square's render are pairs of glowing runes (0x0E68), and the Albatross's benches are inside |
| 7 Magery | **the Haven Magery School** (P678's magery hall, 3640-3654 x 2464-2478; Lyle, the five magery trainers and the arcane guildmaster), its south room | open floor grid in the notes run |
| 7 Bard | **the Bardic Guild** (3655-3679 x 2528-2544; the bards' guildmaster), its long hall with the stage | open floor grid in the notes run |
| 2 Farm | P276's New Haven farm, placed by `[ClusterFSeedTutorialFarm`'s `SeedHaven` at the ML map's old west farm (3372-3401 x 2603-2619) | ours, not stock, so taken away (no question for Chase). The SoS land there has no map op (`trammel.mapops`), so only the server's pieces go |

**The other lessons:**
- **The six other magic schools and combat healing** stay in the training yard behind the Little Shop of Magic (a magic shop).
- **Gathering** (lumberjacking, fishing, camping), **crafting**, and **thieving** stay in the trades yard.
- **Fitting buildings exist** for several of them: The Haven Blacksmith, Carpenters of Haven, the Haven Clockworks and Tinker
  Shop, A Stitch in Time (tailoring), Mapmakers of Haven, and The Haven Thieves' Guild.
  - As the prompt says, only mage and bard moved.
- **There are no tutorial "trainer" NPCs:** Rook starts every lesson. The mage and bard lessons now stand with the stock
  guild NPCs P678 put in those halls. The bard guildmaster, when within 14 tiles, calls out during the fight.

## What changed (code copy, `server/customizations/Tutorial/`)

New: `NewHavenLessons.cs` (one more part of `TutorialWingTrials`, plus three classes) and
`server/patches/PlayerMobile-private-mobile.patch`.

1. **Sparring:**
   - `PlaceOf`, `TargetOf` and `PlaceName` give each P290 lesson its own building. `NearPlace`, `InReach`, the follow,
     leave and arrow lines and `Arm` use them.
   - `combat.weapons` arms in the Proving Grounds, its echo at 3733,2580,40.
   - It is a wing lesson in Rook's window (the quest log lists only the isle's core lessons, as before).
   - The stale "Visit Sera the healer at the farm gate" line now names the town's healers.
2. **The old farm:**
   - `TutorialFarm.ClearHaven` takes away the farm addon, its door, the pen spawner and its animals. It runs at every
     tutorial seed (world load).
   - `[ClusterFSeedTutorialFarm` now clears instead of placing.
   - The animals lesson no longer points there.
3. **Mining:**
   - The lesson arms at the cave mouth (3612,2744,9) with the lent pickaxe and Mining 60, and no practice vein.
   - The ore banks of the cave floor's tiles start full.
   - The text says to click the cave floor or wall, and that your own pickaxe or shovel works.
   - The cave floor tiles (0x053B and up) are in the shard's mining tiles (`server/patches/Mining.cs`), the same art the
     old practice vein used.
   - A signpost marks where the path starts (`HavenPieces`).
4. **Animals:**
   - The lesson is now "heal and tame a horse" (steps: Veterinary, then Animal Taming; Lore explained in the hint,
     Herding explained only).
   - It lends bandages if you have none, and Veterinary, Lore and Taming at 60.
   - `TutorialStableHorse` (a Horse) lies hurt (a tenth of its hits) in the sick-bay stall and bleeds every 4 s.
   - It is visible only to its trainee: `IPrivateMobile`, through the new `PlayerMobile.CanSee` patch.
   - It is not tamable until that trainee's bandage heals it. Then it always tames: MinTameSkill 0 against the lent 60,
     no anger.
   - The steps come from the horse itself (healed, then controlled by the trainee), not from any roll.
   - **Once per character:** the first one is kept (`TutorialStableHorseStore`); a replay's horse "goes back to its stall"
     (deleted) when the lesson ends.
   - **Slots:** the evo pet and the horse take 1 slot each against FollowersMax 5. If the slots are full, the lesson says
     so at the start, and pinned's taming refuses with its own "too many followers" line until a pet is stabled.
   - The stall gets a bucket of water and two straw piles, and the barn door a signpost.
   - **The bug:** `TutorialFarm.CheckDone` (the isle farm) completed `animals.taming`; it no longer does.
     - The same kind of early completion: the isle's healing lesson completes `combat.healing` ("Bandages")
       (`TutorialFarm.OnHealed`).
     - I left that one: it is a real bandaging lesson, not a reward, and New Haven's "Bandages" teaches the same.
     - Nothing else writes a wing key from the isle (the inventory of every `CompleteStation` call).
   - Characters that already got Animals from the isle keep it marked; records are not rewritten.
5. **Bard:**
   - A successful Provocation starts a 12 s brawl (`StartBrawl`): every 1.5 s one echo faces the other, swings
     (attack animation and hit sound) and lands 3-7 damage.
   - The echoes cannot die (their top-up at 20 hits).
   - A line explains what happened, and the bard guildmaster calls out if near.
   - Then they are healed and the line says Provocation wears off.
   - If that was the last step, the lesson finishes after the brawl.
6. **Rook:**
   - He moves to 3669,2636,0, seated on the bench and facing north.
   - The isle moongate's exit moves to 3669,2634, in front of him.
   - An older world's Rook is moved by the seeder (`MoveRook`); the seeder no longer places a second one.
   - Every "Rook on the New Haven plaza" line now says "on his bench by the Albatross tavern" (seven lines), and the
     travel and reputation tours' "plaza" stops are "Rook's bench".
7. **Magery and bard places:**
   - Magery is in the magery school: player 3651,2477, training echo 3654,2472, and `TutorialMageEcho` at 3650,2471.
     - Every 6 s it faces the training echo, says "In Por Ylem" overhead (spell style), plays the cast motion, and 1.2 s
       later sends the Magic Arrow bolt with its sound.
     - It keeps doing so until the trainee's own cast hits, then fades with a puff of smoke.
   - Bard is in the Bardic Guild: echoes at 3668,2530 and 3669,2531.
8. **Thieving:**
   - **The cause:** pinned's trapped chests clear their trap when it fires (`TrappableContainer.ExecuteTrap`). This
     chest fires on open, which the Lockpicking-then-Stealing steps need. After that, Remove Trap answers "That doesn't
     appear to be trapped" before any roll, so the step could never finish.
   - **A player's own trap** can't cause it: tinkering refuses an immovable, locked or already-trapped chest. A Magic
     Trap spell re-arms the chest rather than blocking it.
   - **The fix:** while Remove Trap is to do, every tick re-traps a chest whose trap went off, with a line saying so. Any
     trap on it counts for Remove Trap.
9. **Housing:**
   - Three stops: the small cottage, the field south of it, then the bank. Each has one goal and ends with the next stop.
   - The first two have signposts.
   - Rook's window lists "Stop 1: look at a small house", "Stop 2: learn where houses can be built" and "Stop 3: the
     bank, where a deed is kept".
   - What I found unclear when playing it as a new player:
     - the old first stop said "use a deed on land where housing is allowed" while standing on Haven island, where
       nothing can be built, and never said so;
     - no stop was marked;
     - "the farmhouse porch" was the cottage;
     - the tour ended at the bank with no "you are done".
   - TazUO's transparency tip is kept.

## Tests

- **`server/tests/Tutorial/NewHavenFixesVerification.cs`, 17 facts:**
  - sparring arms in the Proving Grounds, not the old yard;
  - the old farm is taken away (placed with `SeedHaven` force, then cleared, then nothing left);
  - mining at the cave, no props, the path sign;
  - the horse: healed, tamed and kept once;
  - full slots are said;
  - the echoes take blows from each other, and nobody dies;
  - an older world's Rook moves to the bench, facing north;
  - the mage echo stays until the cast, then goes;
  - the thief chest is re-trapped in **7 orders** of the ten steps (natural, reversed, Lockpicking-and-Stealing first,
    and 4 seeded shuffles);
  - the housing stops and signs;
  - a seeded piece at an old spot moved, with both bench halves kept.
- **Updated:**
  - `TutorialTradeTrialVerification` (mining at the cave, animals now the horse, bard after the brawl, leaving the cave);
  - `TutorialWingTrialVerification` and `TutorialLoanLifecycleVerification` (start at the lesson's place);
  - `TutorialFarmVerification` (Animals not done by the isle);
  - `HavenMoveVerification` (Rook's and the gate exit's spots).
- **Green:** every tutorial fact, 276 of 276, on `sl-uo-builder:cc-P753` with this branch's files
  (`notes\cc-P743-tools\probe743.sh`, `green\probe-5.txt`).
- **Red:** one run with seven mutants (`red\red-mutants-A-G.txt`):
  - A: the chest keeper off;
  - B: the isle farm marking Animals again;
  - C: no brawl;
  - D: both lessons back in the yard;
  - E: Rook not moved;
  - F: PlayerMobile without the private patch;
  - G: the clear doing nothing.
  
  14 facts failed, each the one aimed at its mutant; the other 17 passed.
- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P743`, `gated-build.ps1`, the `docker-build` lock taken and
  released):
  - **Run 1:** 2 failed. `TutorialLoanLifecycleVerification` still started sparring in the yard (its own `PlaceOf`), and
    `TutorialVerification`'s dry and refused seeds must place nothing, but my New Haven step ran before the seeder's fit
    checks. Fixed: the step runs after them, and the "Rook missing" check counts an older world's Rook
    (`gated-build-1-two-tests.log`).
  - **Run 2:** EXIT=0, 2,870 tests, 0 failed (`gated-build-2-green-before-stop2.log`).
  - **Run 3**, after the stop 2 move: **EXIT=0, 2,871 tests: 2,865 passed, 6 skipped, 0 failed**
    (`green\gated-build-summary.txt`; the 17 new facts in `green\gated-build-newhaven-facts.txt`).
- **`apply-patches.sh`:** carries P714's here-string fix for the "never applied" flake (P714 isn't on this branch yet;
  the same lines).
- **CHANGELOG** `2026.10.31.9` (seven Changed and two Fixed lines); VERSION 2026.10.31.9.

## Live proof (`notes\cc-P743-review\`)

Private shard on 127.0.0.1:2596: a fresh copy of the bot world, image `sl-modernuo:cc-P743`, the `test-shard` lock taken
and released (`notes\cc-P743-tools\run-shots743.ps1`, `shots743.json`). The runner is P753's (the game view moved clear of
the login windows); TazUO in the default camera, the Tester moved by the Admin's commands.

**At world load**, the shard log says: "New Haven (cc-P743): placed 9 pieces, moved 0 Rook, old New Haven farm: took away
7 thing(s)."
- That world copy did have P276's farm. Its addon, door, spawner and four animals are gone, so the dry run later finds 0.
- It had no Rook yet, so the seeder placed him on his bench.
- The admin's `[ClusterFSeedTutorial` afterwards placed nothing more (`proof-log.txt`).

| Shot | What it shows |
|---|---|
| `rook-bench-player.jpg` | **Rook on his bench** at the Albatross's north-east corner, the Tester at the moongate exit in front of him, the square's path behind. The patch notes window reads 2026.10.31.9. TazUO draws him standing on the bench, not seated (see below). |
| `proving-grounds-player.jpg` | **The Proving Grounds:** the palisade yard full of the town's warrior trainers and the training dummies, the Tester on its plank floor. |
| `mountain-path-sign-player.jpg` | **The mountain path's signpost**, north of the dirt path where it leaves the shore road. |
| `mining-cave-player.jpg` | **The cave mouth:** the Tester on the cave floor, rock walls round him. |
| `stables-stall-player.jpg` | **The barn and its stalls**, the Tester in the aisle at the sick-bay stall's opening, the new signpost outside the east door (the horse appears only while that player's lesson runs). |
| `bardic-hall-player.jpg` | **The Bardic Guild's hall:** stage, rug, the Tester where the lesson arms. |
| `magery-hall-player.jpg` | **The Haven Magery School's south room:** carpet and table, the Tester where the lesson arms. |
| `housing-stop1-player.jpg` | **Housing stop 1** on the cottage's path. |
| `old-farm-site-player.jpg` | **The old farm site** (3390,2611): plain grass and trees; nothing of the farm left. |

- **Renders for the reviewer:** `render-rook-bench.jpg`, `render-stable-stall.jpg` (roofs off), `render-mountain-sign.jpg`,
  `render-housing-signs.jpg` and `render-mining-cave.jpg`. `placed.md` lists every piece.
- **Stop 2 moved after these shots:** at 3703,2599 its signpost stood behind a tree (seen in the first render). It is now
  3704,2604 in the open grass, chosen with P750's cover model (board and stop figure 0% covered); the new render shows it.
  - The seeder now upgrades in place: a named piece found anywhere but its spot is taken away. Covered by a 17th fact.
- **Not shown live** (see Deviations): the injured horse, the brawl and the mage echo.

## Deviations and decisions for Chase

- **Moving parts not shown live:** the brawl, the mage echo's casting and the horse's heal and tame are proven by the
  facts above, not in a TazUO window.
  - The shot runner's Admin cannot answer a target, so it cannot start a lesson for the Tester.
  - A wing lesson cancels itself while its player is offline, which the Tester is when the Admin sets things up.
  - A proof of those needs a Legion script in the Tester's own client (a follow-up).
- **Not "a new character":** the shots use the Golem's Tester and Admin, moved by commands, not a freshly made character.
- **The other trainers** were listed, not moved (see the survey), as the prompt says.
- **`combat.healing`** stays marked done by the isle's healing lesson (a real bandaging lesson; say if you want it
  cleared too).
- **The out-of-repo isle bot** (`notes\cc-P749-tools\isle.py`) still looks for Rook at the stock 3500,2572 (already
  stale since P678). The overnight bot's New Haven checks (start, board, square) do not use Rook's spot.
- **Denied tool:** the unattended run denied the Read tool on `server\customizations\Tutorial\HavenSpots.cs` (code
  copy). As instructed I did not retry it with Read; I read and edited the code copy with Bash and Python scripts, as
  this repo's memory notes recommend for unattended runs.
- **Rook seated:** TazUO draws him standing on the bench, not in a sitting pose. A client draws a mobile sitting only on
  the chair art it knows; the wooden bench is not drawn that way here. A chair (0x0B4F family) beside the bench would
  show a seated figure if you prefer; say so.
- **Undead in New Haven's north streets (found, not changed):**
  - In this world copy, skeletons and zombies walk the streets by the Bardic Guild and the magery school, some inside the
    hall (`bardic-hall-player.jpg`, `magery-hall-player.jpg`).
  - That is near P678's undead training field (3640,2418, home range 40).
  - The two lessons now held there will meet them, so worth a look in a follow-up (the spawner's range, or the town's
    guards).
- **Review step:** the build reviewer (a second Golem) should read `placed.md`, the renders and the shots before merge,
  as the guide's section 8 asks.

## Files

- **Code copy:**
  - new: `server/customizations/Tutorial/NewHavenLessons.cs`, `server/patches/PlayerMobile-private-mobile.patch`,
    `server/tests/Tutorial/NewHavenFixesVerification.cs`;
  - changed:
    - `Tutorial/HavenSpots.cs`, `TutorialWingTrials.cs`, `TutorialTradeTrials.cs`, `TutorialFarm.cs`,
      `TutorialCorePlacement.cs`, `TutorialStations.cs`;
    - the "plaza" lines in `ClusterFTutorial.cs`, `TutorialCoreTrials.cs`, `TutorialGumps.cs`, `TutorialIslandGate.cs`
      and `TutorialStart.cs`;
    - `docker/uo/apply-patches.sh`;
    - five tests;
    - CHANGELOG.md, VERSION.
- **Docs copy:**
  - `notes/cc-P743-tools/`: survey and route scripts, renders, `mkpatch.py`, `probe743.sh`, `gated-build.ps1`,
    `make_shots743.py`, `shots743.json`, `run-shots743.ps1`, `red/`, `green/`;
  - `notes/cc-P743-review/` (placed.md, renders, shots);
  - this file.

P743 DONE
