# cc-P726: the isle pet is a reward, and players can see their evo pet's progress

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P726`, from main `3dd8559`. Not committed, nothing deployed, Haven not touched.

## In plain words

- **The pet is Wren's thanks (test shard).** At the farm you first take the pitchfork, switch to war mode and clear
  the rats and snakes yourself. Then Wren thanks you with a dog or a cat of your choice, and teaches its commands.
- **Healing is its own lesson.** After the farm, a new lesson sends you into the farmhouse. Pip the farm boy sits hurt
  on a bench there, with blood on the floor around him, and you bandage him.
- **Pet Info, everywhere.** Click your evo pet with the right mouse button and choose "Pet Info", or type `[PetInfo` and
  click it. A window shows its kind, its stage (for example "stage 1 of 5"), a bar and "250 of 500 experience to
  become a young hound", its loyalty and how it grows. Only the owner sees it. The Quests button on the character window
  now shows the isle's lessons: done, the one you are on with its steps ticked, and what comes next.
- **The starter gear keeps the rat fight safe.** Wearing the isle cloak and holding Wren's pitchfork heals you about
  three times as fast on the isle, and a little faster elsewhere.
- **For you:** the "Pet Info" menu entry needs the next player package (it is a new client text, cliloc 1900017).
  Until then the entry shows blank, but `[PetInfo` works. Please look at Pip on his bench in game: whether he is drawn
  sitting, and which way the bench faces (I could not check the client's art).

## Before anything: P728 is in this branch

This branch starts from main `3dd8559`, which does not have P728 (committed on `golem/Iron/P728`, `f4e684e`, not yet
merged). P728 changed the same farm code this prompt reorders, and its prompt said P726 builds on it. So, as P727 did,
P728's commit is in the code copy uncommitted (`git cherry-pick --no-commit f4e684e`), and P726 is written on top of it.
When the integrator merges P728 and then this branch, P728's changes are the same in both.

**A P728 bug fixed here:** P728's seed at world load ran inside the load. An item made during the load reaches
`World.Items` only after the load ends, so the copies were topped up but the top-up counted nothing, logged "nothing
missing", and left the new pieces off the copy's reset list. The P726 bot run's shard log showed it: at its claim copy 1
already held all 375 pieces, P726's new signpost, bench and blood among them, yet the load had said "nothing missing".
The seed now runs on the first tick after the load (`TutorialSeeder.Configure`). With the fix, the bot world's six copies
marked "seeded (0 pieces)" turned out to be **empty**: the load filled each one with the whole isle ("Seed on load, copy
1: placed 375 missing pieces") and the copy report then read "seeded (375 pieces)". **This corrects P728's notes**, which
read the old log as "those copies already held every piece". They did not: the seed at load placed them, and could not
count them.

## The items

| # | What Chase asked | What changed | Where (code copy, `server/customizations/`) |
|---|---|---|---|
| 1 | The pet as the reward for the pests | The farm is: the pitchfork in hand, war mode, the pests (step 1); Wren's thanks: "Thank you! The rows are safe again. As thanks, take a pet of your own: choose a dog or a cat in the window..." (step 2); its commands, follow then guard (step 3); done (4). The dog/cat choice is kept (the existing farm pet window). No pet before the pests: the window does not open and a pick is refused. The pests no longer wait for a pet's kill (there is no pet yet), only for one struck by the trainee. When the pet is given, the System says how to see Pet Info. An account that already has its tutorial pet (one per account, P453) goes from the pests to the commands. Old records keep their progress (pests and commands done is step 4). P728's order (pitchfork, war mode, pests) is unchanged; the pet and the commands moved after it, as P728 set up. | `Tutorial/TutorialFarm.cs` (`StepOf`, `Talk`, `ChoosePet`, `BeginCombat`, `BeginCommands`, `CheckCommands`), `TutorialGreeting.cs` (Wren greets until she starts the fight) |
| 2 | Pet Info | A window built only from the pet's own data: name; kind (the line's name and role); stage name and "stage N of M"; experience as "X of Y experience to become a <next stage>" with a bar from the current stage's threshold to the next (EvoPet's cumulative XP and `EvoPetSettings.XpToEnter`); what else it waits for (the owner's loops, the Bond Trial, a body pick: `EvoPet.BlockFor`); loyalty (pinned's 0 to 100); hunger: pets here have none (only players have a hunger field), so the window says so and that feeding raises loyalty; how it grows (experience from creatures it helps defeat, more for stronger foes, `EvoPet.XpForKill`). "Pet Info" on the pet's context menu (`AddCustomContextEntries`, cliloc 1900017) and `[PetInfo` (target the pet). Both refuse anyone but the owner (staff may look). No existing player-facing evo view existed to reuse; the staff `[EvoPet info` reads the same fields as text. | `Mobiles/Evo/EvoPetInfo.cs` (new), `ShardClilocs.cs`, `player-package/vendor/shattered-legacy-cliloc/entries.json` and `registry.csv` |
| 3 | Training taught later | Not taught on the isle. The proposal and a drafted prompt are below. | |
| 4 | Healing as its own lesson | A new core lesson after the farm, `core.healing`, "Healing: bandage Pip". It starts by handing bandages (the farm's same stack and cap), the lines on how to use them and how long they take (P721's), how to make more (P718's), and the arrow to Pip. A heal that works finishes it (P721's rules kept: Pip stays hurt and is cut again, a failed try says so, 0-Healing trainees always heal on the lesson). Pip sits on a wooden bench (0x0B2D, two tiles) inside the farmhouse against the east wall between the bed and the box (6692,3975 on the floor at Z 7), with three blood decals (0x122A, 0x122D, 0x122C) on the floor beside him. The lesson's signpost stands outside the door to the south-west (6688,3980), its stop is the door's step. The seeder moves a Pip placed by the gate before onto the bench, and places the bench and blood if missing. An old record that bandaged at the farm has done the lesson (`ClusterFTutorial.IsDone`). The farm hint and title no longer mention bandages. | `TutorialFarm.cs` (`BeginHealing`, `HealingOn`, `OnHealed`, `PipBench`, `PipProps`, the seeder), `TutorialStations.cs`, `ClusterFTutorial.cs`, `TutorialCoreTrials.cs`, `TutorialTrialProgress.cs` (`Healed`), `TutorialCorePlacement.cs` |
| 5 | Starter gear regen | The worn isle cloak and the held pitchfork each add hit point regeneration points (`RegenRates`, before the player cap of 18): **3 each on the Wakening Isle and its copies, 1 each elsewhere**. The numbers are below. | `Tutorial/TutorialStarterGear.cs` (new), `RegenRates.cs` |
| 6 | The lessons in the quest log | The Quests button (encoded packet 0x32) is answered from customizations. A trainee in the tutorial gets the quest log's own frame (pinned's `BaseMLQuestGump`: "Quest Log" header, its buttons and paging), listing the core lessons, each done, now, next or later. A page per lesson shows its steps ticked (`[x]`) from the same progress the lesson window reads: the running trial's evidence, `StationsDone`, Wren's farm keys. Its hint is below. "Continue" opens pinned's own quest log, so other quests are one click away. Anyone not in the tutorial gets pinned's log straight away. Nothing is tracked twice. | `Tutorial/TutorialQuestLog.cs` (new), `TutorialTrialProgress.cs` (`Expected`) |

### Item 5: the numbers

Pinned's rule (our `RegenRates.cs`): a player regains 1 hit point every `10 / (1 + points)` seconds. Humans get 2
points, and the player cap is 18.

| Who | Points | Interval | HP per second |
|---|---|---|---|
| Human, no gear | 2 | 3.3 s | 0.30 |
| Human, cloak and pitchfork, on the isle | 2 + 6 = 8 | 1.1 s | **0.90** |
| Human, cloak and pitchfork, elsewhere | 2 + 2 = 4 | 2.0 s | 0.50 |
| Elf or gargoyle (no racial points), on the isle | 6 | 1.4 s | 0.71 |

The pests (`TutorialFarm.cs`) hit for 1-2 (farm rat), 2-3 (field rat) and 1-3 (grass snake). With Dex 30-35 and their
wrestling, they swing about every 2 s. That swing time is unverified: I worked it out from pinned's AOS delay, not
measured. Against a new character's skills, about half the swings land (also unverified). That makes one pest about
0.4 to 0.6 HP per second, and two at once about 1.0. With the gear on the isle, a human regains 0.9 HP per second, so
one pest is never a danger and two only slowly. Pests fight only the trainee on the pest part, and the field holds a
few at a time.

**Off the isle: +1 per piece** (0.30 to 0.50 HP per second for a human with both). It is what ordinary early jewelry
gives (Hit Point Regeneration 1 or 2), and any real armour or jewelry passes it within the first few hours. It does not
stack past the cap of 18.

## The quest log: why no patch

Pinned's `QuestLogGump` has a private constructor and reads only `MLQuestContext.QuestInstances`. The paperdoll button
reaches it through a static call with no hook (`IncomingPlayerPackets.QuestGumpRequest` to
`MLQuestSystem.QuestGumpRequest`). These were the options:
- **Real MLQuests, one per lesson:** each lesson's evidence would have to become MLQuest objectives, saved twice (the
  tutorial record and the quest context), which is exactly the second tracker Chase ruled out.
- **A patch to `QuestLogGump`** (a hook for extra rows): it changes a pinned file for a view our own code can give.
- **Answering the button ourselves:** `IncomingPackets.RegisterEncoded` is public, and TazUO's command already
  registers its own packet this way. This is the choice. The view uses pinned's quest gump base, so it looks like the
  quest log, and it hands everything else to pinned's log.

## Decisions and deviations

- **Bench art and Pip's pose are not seen in game.** 0x0B2D is "wooden bench" (tiledata); I chose it as the north-south
  piece for a bench along an east wall, unchecked. The client draws a person on a seat tile seated; I did not check that
  TazUO does it for an NPC. The blood is static art, so it never fades.
- **The bot's walk grid has no floor inside the farmhouse** (its floor and steps are addon items at Z 7, not map
  statics), so the route walks to the steps, opens the door and steps in and out tile by tile, as a player does. The
  server side was never in question: run 1 found no path in the bot's planner, not a blocked door.
- **Hunger:** the window says pets here never go hungry, because no creature on this shard has a hunger field (pinned's
  hunger is the player's). Feeding still raises loyalty (pinned).
- **The wing station `animals.taming`** is now credited when the commands are done (it was credited at the pests).
- **Denied in this unattended run:** nothing new for P726 (P728's list stands).

## Facts

New: `server\tests\Tutorial\TutorialIslePetRewardVerification.cs`, 5 facts:
1. No pet window and no pick before the pests; then Wren's thanks with the dog/cat window; one pet; the Pet Info line;
   the commands at once; the farm done; healing next.
2. Pet Info: kind, "stage N of M", "X of Y experience to become a <next>", loyalty, how it grows; the bar part-way after
   half the experience; the context menu entry for the owner only; the command's target refuses anyone else and
   anything not a pet.
3. Healing: the station right after the farm; Pip on his bench with the bench and three blood decals; not before the
   farm; the lesson hands bandages; a heal finishes it; an old farm heal counts.
4. The starter gear: 1 per piece off the isle, 3 on it, a shorter regeneration interval on the isle (read from
   `RegenRates` itself, without registering it in the host), nothing for gear not worn.
5. The Quests button: the lessons for a trainee, pinned's log for anyone else; done, now and later; the farm's steps
   tick as they are done; a lesson's page with every step ticked when finished.

**Seen failing first:** `cc-P726-tools\mutate726.py` writes a copy of the customizations with each item put back (the
pet pickable before the pests, no Pet Info entry, the heal not finishing a lesson and no old-heal credit, no gear regen,
the button always opening pinned's log). All 5 facts failed, each at its own item (`red-old726.txt`).

Changed, for the new order: 25 existing facts across 11 files. The farm facts follow pests, then pet, then commands.
The heal facts are on the healing lesson (`HealingOn`, `BeginHealing`). Each file's lesson-evidence helper knows
`core.healing`. The station and core counts are 40 and 11, and the seeder places 11 markers.

## Build

`docker/uo/build.sh -t sl-modernuo:cc-P726`, detached, `docker-build` lock (released).
1. **Green, `EXIT=0`**: 2746 passed (`gated-build-1.log`). The bot run then found the load seed's counting (above).
2. **Green, `EXIT=0`**, with the load-seed fix: "Built sl-modernuo:cc-P726 with patches applied and 2746 shard test(s)
   passing." 2752 tests: 2746 passed, 0 failed, 6 skipped (the usual client-data facts) (`green-gated-build.txt`,
   `gated-build-2.log`).

## The bot route

`cc-P726-tools\isle.py`, made by `make_isle_bot.py` from P728's route (`isle-p728.py`), on the private shard
(`proof-shard.ps1`, port 2596, a fresh copy of the overnight bot's world each run, the isle overlay, its map-ops hash this
branch's), under the `test-shard` lock (released). The shard is down.

| Run | Result |
|---|---|
| 1 | The farm passed in the new order; the walk to Pip found no path in the bot's planner (no floor inside the farmhouse in its grid). Route fixed. |
| 2 | Healing passed; the walk out of the farmhouse failed the same way. Route fixed. |
| 3 | The field gate was still open after the farm, which the planner could not pass. The route now steps out through it. |
| 4 | **0 failed checks**, on build 1. Its shard log showed the load seed's counting (above). Fixed, rebuilt. |
| 5 | **0 failed checks** (`runs\run5\playlog.txt`), the isle in 177 s, on build 2. The load log lists each copy's 375 placed pieces. |
un5\playlog.txt`), the isle in 177 s, on build 2. The load log lists each copy's 375 placed pieces. |

The new checks, in run 5 as in run 4: Wren hands the pitchfork first; holding it counts; war mode counts and Wren opens
the gate; **no pet before the pests**; the pests cleared by the trainee alone; "Now: The cabbage rows are clear..." and
the arrow on Wren (P728's); **the pet window after the cleared rows**; the pet is yours; **the System says how to see Pet
Info**; follow; guard; the farm lesson finished; **the healing lesson hands bandages and points at Pip**; **Pip sits on
his bench**; inside the farmhouse beside him; a bandage really healed him; back out; then death, the bank, the League,
the vision, and the moongate to Rook at 3632,2584; the New Haven pick on the plaza.

## Item 3: pet training, a later lesson (proposal)

**Where:** an optional isle station after the farm, "Your pet: food, bonds and growth". It goes at the pen inside the
field (P718's), with Wren or Tobin the vet, and Rook offers it as an any-time lesson like the client tips. It is not a
core lesson: the isle is long already, and a player without their pet beside them could not do it. A first New Haven
quest was the other option, but the vet and the pet are both on the isle, and the isle is where the pet was given.

**What it covers:** feeding (drop food on the pet; loyalty rises), bonding (the tutorial pet is bonded at once; what
bonding means at death and at the vet), what earns evolution experience (fighting beside you, more for stronger foes;
Pet Info's bar), the gates beyond experience (owner loops, the Bond Trial), and stabling (an animal trainer in New
Haven, and why a stabled pet does not grow).

**Drafted prompt:**

> **CC task P7xx: an optional isle lesson on caring for your pet** (Model: Opus; Touches: server; after P726)
>
> Chase (10-28 12:22): "A later tutorial can teach how to train it." P726 made the evo pet Wren's reward and added Pet
> Info. Add an optional any-time lesson, "Your pet: food, bonds and growth", offered by Tamsin and Rook once the pet is
> given (like the client tips, P718 item 3), at the farm's pen with Tobin the vet.
> 1. **Feed it:** Tobin hands one pet food item; drop it on the pet; the lesson sees the loyalty rise (pinned
>    `BaseCreature` feeding). Say what loyalty does and that it drops over time.
> 2. **What makes it grow:** open Pet Info (context menu or `[PetInfo`) and read the bar; fight one pen pest with the pet
>    on "all kill" and see the bar move (evidence: `EvoPet.Xp` rose).
> 3. **Bonded:** Tobin explains what a bonded pet's death means and the vet's resurrection (P666's lines), and that
>    Young owners pay nothing.
> 4. **Stabling:** say "stable" to Tobin to stable the pet and "claim" to get it back (pinned's stable keywords); say
>    that a stabled pet does not grow.
> Evidence only (no Done button except where the server cannot see it). Facts per step, seen failing first; the bot
> route takes it once. Notes `notes\cc-P7xx-isle-pet-care.md`.

## Files

- Code copy (uncommitted, P728's commit included as above): `Tutorial/TutorialFarm.cs`, `TutorialStations.cs`,
  `ClusterFTutorial.cs`, `TutorialCoreTrials.cs`, `TutorialTrialProgress.cs`, `TutorialCorePlacement.cs`,
  `TutorialGreeting.cs`, `TutorialRecruiter.cs`, new `TutorialStarterGear.cs` and `TutorialQuestLog.cs`; new
  `Mobiles/Evo/EvoPetInfo.cs`; `RegenRates.cs`; `ShardClilocs.cs`; the cliloc `entries.json` and `registry.csv`; the new
  fact file and 11 changed test files; `CHANGELOG.md` (2026.10.28.8: 3 Added, 2 Changed) and `VERSION`.
- Docs copy: this file and `notes\cc-P726-tools\` (probe, mutant, red and green outputs, the gated build script and
  logs, the CHANGELOG script, the bot route and its maker (`isle-p728.py` is P728's route it starts from), the proof
  shard script, the runs).
- Outside the repos: `D:\UO\golems\Iron\p726-work\` (overlay and shard copies); it can be deleted.

P726 DONE
