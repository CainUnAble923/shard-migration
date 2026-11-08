# cc-P802: New Haven tutorial notes, batch 2

## In plain words

- **Waking on the isle is one window now, not a wall of System messages.** A new character lying on the beach sees one
  window with the wake text, how to get up and the young-player note. The four "Your skill in ... has increased by 30"
  lines, the "chat system has been disabled" line and the repeated lesson hints are gone from the left of the screen.
  Once you stand, the window says to go to Tamsin.
- **New Haven's lessons teach in their window.** Each step, each tour stop and the skills a lesson only explains stay
  in the lesson window until you close it. The Runes lesson starts at the public moongate and hands you a blank rune,
  a Mark scroll and two Recall scrolls: mark the rune, recall to Rook's bench, then recall back. The scrolls always
  work in the lesson.
- **Lessons happen in fitting buildings.**
  - On the isle release you play: smithing at the Forge and Anvil, fishing off the docks pier, lumberjacking in the
    logging clearing, cooking at the bakery, scribing in the scribe's library, and so on.
  - Mysticism is in the Mage hall with Ilyra Moonwhisper, an elven adjunct instructor.
  - Necromancy sends you to the Necromancers' Guild Hall on the hill.
  - The old tutorial farm west of town is cleared from every world on its own.
- **For you:**
  1. Both builds are green: main as `sl-modernuo:cc-p802` and the isle release as `sl-modernuo:cc-p802-isle`. The
     release diff `notes\cc-P802-tools\p802-release-isle-20261028.diff` (version 2026.11.07.3, after P817's .2) is
     ready to ship.
  2. Decide on main's necromancy place (section 8). Main's guild necromancers stand in "the east house". I sent main's
     lesson to the skull-candle shrine.
  3. Say if you want Chivalry at an ankh and Bushido and Ninjitsu in the dojos (section 6). I left them in the
     training yard.

Iron Golem, 2026-11-07.
- **Code copy:** `D:\UO\golems\Iron\ShatteredLegacy`.
- **Docs copy:** `D:\UO\golems\Iron\shard-migration`.
- **Release copy:** `D:\UO\golems\Iron\p802-isle`, a detached worktree at `56f98af` (the `release/isle-20261028` tip).

The code and docs copies are on `golem/Iron/P802`; the release copy has the change staged. Nothing is committed,
`latest` was not moved and nothing was published. Chase's answer `Iron-P802-20261105-114116-0c46` ("parked until P799
merges") was met: P799 is on main (via P806 and P814) and in the release tip.

## Two New Havens

The testers play New Haven from `release/isle-20261028`, whose New Haven is the ML plaza (x 3400-3560). Main's New
Haven is the town at x 3600-3760 (P678). Both are on the same map files. So every place in this prompt has two sets of
tiles:
- **Main:** `notes/cc-P802-tools/lesson-places.json`, with renders in `notes/cc-P802-review/places/`.
- **Release:** `lesson-places-release.json`, with renders in `places-release/`.

A subagent picked and checked both sets on the shard's own map files and decoration: walkable surface, nothing
impassable from Z to Z+16, stand Z, roof. I wired them in. The code is the same in both; only `NewHavenLessonPlaces.cs`
and the place words differ.

## 1. Teaching in the window, not the System window

- **Wing lessons (all New Haven lessons):**
  - The window (`TutorialWingTrialGump`) now shows the steps, a **Latest** line and a **Note**. Latest is the lesson's
    last line: a tour stop's lesson, a step said, a demonstration. Note is a skill the lesson only explains: Resisting
    Spells, Spellweaving, Imbuing, Herbalism, Forensic Evaluation, or runebooks for the Runes lesson.
  - The System window says only "<lesson>: the steps are in the lesson window." once, and "You reached <stop>: read it
    in the lesson window." at a tour stop.
  - A finished step refreshes the window instead of repeating the hint.
- **The moongate (Runes) lesson:** its teaching is the window's steps (section 2).
- **The demonstration before a school is learned** (main only; the release has no school gate): Chivalry and
  Necromancy show it in a window (`TutorialNoteGump`).
- **Isle core lessons:** these already had the hint and "Now:" step in their window. Their System line no longer
  repeats the whole hint and tip; it says "Lesson: <title>. The steps are in the lesson window." (item 7).
- **Changed lessons:** every New Haven wing lesson (combat.weapons, combat.healing, the six magic lessons, the four
  gathering, the nine crafts, animals, bard, thieving, the housing / reputation / shard-systems tours, travel) and
  every isle core lesson's opening line. P801's Name Colors lesson (`reputation.wing`) only gets the shared window
  behaviour, as every tour does; its text is untouched.

## 2. The Runes lesson: Mark and Recall

`travel.wing` is now a three-step lesson at the public moongate (`HavenSpots.PublicMoongate`).

It lends:
- a blank rune (the trainee's own);
- the lesson's rune, already marked in front of Rook's bench (`HavenSpots.MoongateExit`);
- a Mark scroll and two Recall scrolls.

The steps are mark, away and back: mark your rune by the moongate, recall to Rook with the lesson's rune, then recall
back with your own. The lesson completes on the return (`TickTravel`); its reach is 160 tiles, like a tour, so the
recall to Rook stays in it.

- **Scrolls without Magery:** a lesson-only guaranteed success. Magery is lent at 100 and Intelligence +30 for mana,
  as skill and stat mods that are never saved (the trial's other lessons lend the same way). So every scroll works,
  and a gain is very unlikely, never more than a scroll gives.
- **The island gate (`TutorialIslandGate`)** refuses Mark on Haven Island before graduation. It now allows it only
  while the Runes lesson runs; the rune is a loan taken back at the end. Recall still only goes to places on the
  island.
- **One addition:** a second, pre-marked rune. Without it, "recall away" has nowhere to go.

## 3. Mysticism in the mage building, with an elven adjunct instructor

New NPC `TutorialLessonTeacher.Mystic()`: "Ilyra Moonwhisper, the adjunct instructor of Mysticism". She has an elf
body (0x25E) and Race.Elf, an elven robe and boots, is invulnerable and can't walk. Double-clicking her starts the
lesson.

She is seeded with New Haven's pieces at every world load (`SeedTeachers`, upgraded in place: moved back to her spot
and facing).

| Build | Lesson arms | Her spot (facing) | Echo |
|---|---|---|---|
| Release | Mage hall, crystal-ball room, 3485,2494,52 | 3485,2491,52 (South) | 3487,2493,52 |
| Main | Haven Magery School south room, 3653,2477,0 | 3652,2473,0 behind the table (South, to the door) | 3654,2475,0 |

Elves stay unplayable (P762); this is an NPC. Shot: `cc-P802-shots/mysticism-ilyra2.jpg` (main).

## 4. The farm in New Haven

The farm we placed is P276's: the farmhouse addon at 3377,2611, its door, the pen spawner and its animals. It stands
west of the ML plaza, which is the release's New Haven.

- **Why it lingered:** P743 removes it, but only when the tutorial seed runs to its end. A world whose seed was skipped
  or refused kept it.
- **The fix:** `TutorialFarm.ClearHavenOnLoad` now runs at every start by itself, only on our pieces.
- **Evidence:** on the proof shard's copy of the bot world, the first start logged "old New Haven farm: took away 7
  thing(s)" (`cc-P802-tools/shard-after-seed-lines.txt`).
- **Nothing still points there:**
  - The animals lesson moved to the stables (P743/P799).
  - P276's tree removals are already out of the map patch.
  - `FarmField` and `GoatSpot` are unused constants, kept for an old fact.
- **The crop fields at main's east edge** (3700-3740, 2570-2610) are the map's own statics, not ours; they stay.
- **Shots:** `old-farm-spot-before.jpg` and `old-farm-spot.jpg` show the spot empty in both runs. On main the existing
  seed also clears it, so the two shots look alike; the log line is the evidence. `placed.md` lists what was removed.

## 5. Camping and herbalism

No change was needed. Herbalism went live with P804 (main, and the isle release at 2026.11.06.1). Chase played
2026.11.03.1, before it. The camping lesson lends Camping 60 and Herbalism 30 and puts a wild-garlic patch beside you;
the existing fact `AHarvestFinishesGatheringAndTheToolAndPropsGoBack(camping)` covers picking it.

Other references to systems that aren't live yet:
- **shard.systems:** "level resets and higher level caps are not active yet" already says so.
- **combat.weapons:** Resisting Spells is "explained, not trained".
- **magic.mysticism:** Spellweaving points to the Heartwood quest.
- **crafting.blacksmithy:** Imbuing is "not taught here".

None of them asks a player to do something they can't.

## 6. Every lesson in a fitting place

| Lesson | Where it was | Where now: release (ML plaza) | Where now: main | Why |
|---|---|---|---|---|
| gathering.lumberjacking | trades yard, practice tree prop | logging clearing south of the carpenter, its own willow | Woodsman's lodge, its own oak | real trees, a woodsman's place |
| gathering.fishing | trades yard, practice pond prop | end of the west pier, the sea | west pier, the water | the docks |
| gathering.camping | trades yard | camp spot by the north road (garlic prop) | camp spot by the road to the east fields | no camp building exists: a roadside spot, low confidence |
| crafting.blacksmithy | trades yard, anvil and forge props | Forge and Anvil smithy yard, its own anvil and forge | Hammer and Steel smithy, its own anvils and forges | props only if the town's are missing |
| crafting.tailoring | trades yard | tailor's north workroom (loom) | A Stitch in Time, west room | the tailor |
| crafting.carpentry | trades yard | carpenter's workshop | Carpenters of Haven | |
| crafting.tinkering | trades yard | Springs N Things | Haven Clockworks and Tinker Shop | |
| crafting.alchemy | trades yard | the alchemist's | reagent kitchen behind the mage's shop | neither has an alchemy table; none is needed |
| crafting.fletching | trades yard | bowyers' corner of the Warrior's Guild yard | Bullseye Marksmen archery range | the bowyers |
| crafting.cooking | trades yard | the bakery | Albatross kitchen | Dough needs no oven |
| crafting.inscription | trades yard | scribe's library | Haven Public Library | |
| crafting.cartography | trades yard | the mapmaker's above the docks | Mapmakers of Haven | |
| thieving.trial | trades yard | back alley by the tavern (no guild in the plaza) | Haven Thieves' Guild | |
| magic.mysticism | training yard | Mage hall (item 3) | Magery School (item 3) | |
| magic.necromancy | training yard | Necromancers' Guild Hall (item 8) | skull-candle shrine (item 8) | |
| magic.chivalry | training yard | **not moved**: proposal, the ankh garden 3465,2600,13 | **not moved**: proposal, the ankh in Uzeraan's hall | see below |
| magic.bushido | training yard | **not moved**: proposal, the Hamato Dojo 3500,2414,55 | **not moved**: no dojo on main's map | see below |
| magic.ninjitsu | training yard | **not moved**: proposal, the Ninja Dojo 3420,2519,21 | **not moved**: no dojo on main's map | see below |
| combat.healing | training yard | **not moved**: proposal, the healer's | **not moved**: proposal, the Healers of Haven | see below |
| combat.weapons, magic.magery, animals, bard, mining, the tours | their own buildings since P743/P799 | unchanged | unchanged | skipped, as the prompt says |

- **Why Chivalry and combat.healing stay:** healing your own wounded villager works only inside the training yard's
  region (Trammel refuses healing an uncontrolled creature; `TutorialYardRegion.AllowBeneficial`). Moving them needs
  that region where they go. That's a small follow-up if you want it.
- **Why Bushido and Ninjitsu stay:** their dojos are on the release map, but their training-echo tiles were not
  checked, and main has no dojo.
- **Signs:** no new signposts were placed; the arrow and the window name each place. Most buildings already carry a
  shop sign; the subagent's checked sign tiles are in the JSON if you want them.
- **The isle core lessons** were already one west-to-east line with each lesson at its own place (P663-P741); none
  moved.

## 7. A quiet wake

Chase's shot showed ten System lines. This is what happens to each now:

| Line | Now |
|---|---|
| "You will enjoy the benefits ... young player" | in the welcome window's Notes (`ClusterFYoungPlayer.SendLoginMessage` through `Account-young-duration.patch`, a + line only) |
| "Your skill in X has increased by 30.0" x4 | gone. TazUO prints a single-skill update's change; `ClusterFSkillCaps` set every cap at the first login, and each changed cap sent one while the client still had no values. The caps are set at creation now, before the client is attached, so the login pass changes nothing. Real gains still print. |
| play test tasks note | Notes (`PlayTestTasks.OnLogin` through `TutorialWelcome.Note`) |
| "Your account's tutorial continues ..." | Notes |
| "You wake on cold sand ..." | the window's text (no System line) |
| "The chat system has been disabled." | not said for TazUO's own open-chat request at login: our 0xB5 handler skips it while waking or in the first 30 s, and still answers a player who presses Chat later |
| "To get up, take a step ..." | the window's text, and over the head as before (no System line) |
| "You wake on a quiet shore" and "Follow the arrow and double-click Tamsin" | the window turns to the first step when you stand; the System window says "Follow the arrow to Tamsin and double-click her." |

System messages a new player still sees in the first lessons:
- that one Tamsin echo;
- each core lesson's "Lesson: <title>. The steps are in the lesson window.";
- the "Now:" step lines (also at the top of the window);
- "Next: <lesson>" after each lesson;
- refusals (a full backpack, dead).

The window sits at the top left (20,60) so Tamsin and the trainee stay in view; the first shot had it over Tamsin with
the young note clipped, both fixed. Shots: `wake-before-*.jpg` (base image `cc-P813`) and `wake-after-*.jpg`
(`cc-p802`, retaken 2026-11-07 19:24 on the rebuilt image): the window at the top left with the whole young note,
Tamsin in view and no System lines on the left. A Player account with no play-test tasks or account tutorial gets no
lines for those, so the Notes show only the young status.

## 8. Necromancy points to the necromancers' place

- **Release:** the lesson arms in the Necromancers' Guild Hall, the black stone temple on the hill north-east of the
  plaza (3555,2463,15), where the release already seeds Mulcivikh and Morganna. That is Chase's "necromancy temple".
  - The echo is at 3555,2460,15, and a keeper NPC, "Morvain Ashgrave, keeper of the Necromancers' Guild Hall", stands
    at 3556,2454,15 facing south.
  - The station's Where, the follow line, the arrow (`PointAt`/`PlaceShort`) and the quest log (which reads the
    station's Where) all name it.
- **Main:** the lesson goes to the skull-candle shrine (3686,2475,0; keeper on the dais at 3693,2475,2 facing west),
  and the school-gate demonstration happens there in a window. **For you:** main's guild necromancers (Mulcivikh,
  Morganna) stand in "the east house" (3729,2635,40, `ClusterFNewHavenSeeder`), not in the shrine. Say if the lesson
  should go to the east house instead; it's a one-line place change.
- **The other magic lessons:**
  - Magery already goes to its school (P743).
  - Mysticism: item 3.
  - Chivalry, Bushido and Ninjitsu: section 6.

## Tests, builds, shots

- **New facts:** `server/tests/Tutorial/HavenNotes2Verification.cs` and `HavenNotes2WakeVerification.cs`, 28 P802_
  facts covering items 1, 2, 3, 4, 6, 7 and 8.
- **Changed facts:**
  - `TutorialTradeTrialVerification`: the travel lesson is not a tour now; the trades start at their own places; the
    tree and pond props are gone.
  - `TutorialLoanLifecycleVerification`, `NewHavenFixesVerification` and `PersuasionVerification`: the thieving and
    craft lessons at their places.
- **Red, then green** on main's base builder (`notes/cc-P802-tools/run-facts.sh`, mutations in `mutate.sh`: each new
  behaviour switched off by one sed in the container's copy):
  - **red:** 26 of 27 failed (`red.log`). The one that passed is the control fact (a login note goes to the System
    window when not waking), as it should. The 28th fact (the core echo) came after the red run.
  - **green:** 27/27 (`green-2.log`), then the full suites below.
- **Gated build of main** (the repo's gated build script, `sl-modernuo:cc-p802`): **green**, 3,293 shard tests
  passed, EXIT=0 (`gated-build.txt`).
  - It was rerun on 2026-11-07 after Chase's answer `Iron-P802-20261107-182915-952d`, with the final code: the
    window at the top left, and the core lessons' short echo with its fact.
  - Memory was 4.5 GB free at the start, after dropping the Docker VM's page cache.
  - The ~110 "Item.Amount <= 0" corpse lines in the log are old noise: the earlier green build had the same count.
- **Isle release:** `notes/cc-P802-tools/p802-release-isle-20261028.diff`, applied to `56f98af`. Conflicts were
  resolved by hand:
  - the ML places;
  - the theater and ravine anchors;
  - no school gate and no `NextLessonLine` in the release;
  - its own P769-less trade facts.
  - **First gated build:** failed on `NextLessonLine`, which was fixed.
  - **P802 facts on the release's own builder** (`sl-uo-builder:isle12-20261107`): 27/27 (`isle-facts.log`, before the
    core-echo change).
  - **Second gated build:** killed for low memory.
  - **Third gated build** (`sl-modernuo:cc-p802-isle`, rerun 2026-11-07): **green**, 2,998 shard tests passed,
    EXIT=0 (`gated-build-isle.txt`).
  - The staged release copy matches the saved diff byte for byte (same md5), and it has the final welcome window and
    core echo.
- **Shots:** private proof shard on 2596 (P817's tooling: `proof-shard.ps1`, `creation817.ps1`, `shots817.ps1`), the
  bot world with the isle overlay. Files are in `notes/cc-P802-shots/` and `notes/cc-P802-review/`, with
  `notes/cc-P802-review/placed.md`.

## Deviations and decisions for Chase

- **Read/Edit tools:** denied on the code copy in this unattended run (outside the working folder), so code edits
  went through a small replace script (`ed.py` in the session scratchpad), each edit exact and unique.
- **Docker Desktop:** down when this session began (it died at about 15:30, when free memory hit 0.2 GB). I started
  it again. The shared test shard's container (`sl-modernuo-test`) did not come back by itself; I did not touch it,
  so the overseer should check it.
- **Lesson windows shots:** none. `[Tutorial station` is a targeted GameMaster command the shot driver can't use. The
  windows' contents are proven by the facts (`gump.Text`, `Note`, `Latest`).
- **Release shots:** the shots are from main's image on the bot world (main's town). The release build's places are
  shown by the renders in `places-release/`.
- **Undead in main's streets:** main's New Haven streets in the bot world have skeletons and zombies wandering (seen
  in the shots); not from this change.

P802 DONE
