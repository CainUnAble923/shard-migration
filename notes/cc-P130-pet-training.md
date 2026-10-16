# cc-P130: Port list, Pet Training part 2: training itself

2026-10-16. Prompt: `D:\UO\cc-prompts\cc-P130-pet-training.md` (handed by the Golem after P129). Both repos were
clean of anything not mine at the start (the shard repo clean; shard-migration held P129's finished note and its
last bot run, which ride in this commit, below). P121 finished DONE (its note's last line). Model: Fable, as the
prompt asks.

## Headlines

- **Pet Training is whole.** The training half of ServUO's system is in: `TrainingProfile`, `PlanningProfile`,
  `TrainingPoint`, `TrainingDefinition`, the definitions-and-costs half of `PetTrainingHelper` (137 creature rows, 102
  training points, the ability packages), the seven gumps rewritten for pinned's `DynamicGump`, the Animal Lore
  gump's training pages, the trainer's greeting, `ControlSlotsMin`/`ControlSlotsMax` with ServUO's slot lowering, the
  training gate and its two staff cousins. A tamer begins training from Animal Lore, fights, spends points in the
  training menu, and the pet climbs its slot range and asks for more taming, as on OSI since Time of Legends.
- **No change to BaseCreature's save (decision 2a, again).** The training state, the lowered-slot flag and the
  tame requirement live in `PetTrainingStore` (`PetTraining.bin`, generic persistence, keyed by creature) beside
  P121's ability profiles. Min and max slots are *derived* from the definition and that flag, never stored.
- **Five upstream patches, every one a seam ServUO itself has:** the `ControlSlots` field's `fieldChanged:` hook
  and `SetAverage` in the eight min/max setters (BaseCreature), `CurrentTameSkill` and the tame hook (AnimalTaming),
  the training lore gump (AnimalLore), pet Focus gain (SkillCheck), the trained weapon move (BaseWeapon, the seam P121
  left). All five apply at `--fuzz=0` after every patch before them.
- **Time of Legends slots on the live world:** a stock Dragon builds at 4 slots now (its definition's minimum; ServUO's
  setter clamps the constructor's 3), and a one-time pass at the first boot raises every tamable that sits below its
  minimum (`[PetTraining] ... slots upgraded on N tamable creature(s)` in the log). Its master's follower count is kept
  right.
- **Gates:** 12 new facts in `PetTrainingVerification`, all seen failing first under one deliberate break set
  (12 edits in 9 files, three of them in the patches' own `+` lines); the gated build green at **1,385 of 1,385** shard facts; the full server suite green (the UOContent project run twice: one clean run, one with P129's known garden flake);
  the test world booted twice on the image (94 tamables raised to their minimum by the one-time pass, no error, the new save file written and read back).
- **Left, each with its reason below:** the Ethologist title deed (pinned has no reward-title system), the four ML
  quests the trainer hands out (no ML quest system), `ColdWind` (not a pinned weapon ability), the six weapon
  abilities' pet Bushido/Ninjitsu gains and Bladeweave's pet check (P121's "later"; the helper methods are in), and
  `VvVMount` (no such creature).

## What was ported (ServUO file -> our file)

All under `server/customizations/Services/Pet Training/` unless said; each file's header names what differs from ServUO
and why.

| ServUO (`Scripts/Services/Pet Training/`) | Ours | Lines | Notes |
|---|---|---|---|
| TrainingProfile.cs | same | 422 | line for line; pinned's gump calls, `Core.Now`; `LeadingIntoBattleQuest.CheckComplete` dropped (no ML quests); Serialize/Deserialize on `IGenericWriter/Reader`, ServUO's version 2 with the plan riding along |
| PlanningProfile.cs | same | 157 | line for line; entries written by **name** (as P121 writes abilities), so a table edit cannot shift a saved plan |
| TrainingPoint.cs | same | 59 | line for line |
| TrainingDefinition.cs | same | 49 | line for line |
| PetTrainingHelper.cs (:13-59, :127-224, :250-357, :365-1313, :1316-1743) | same, 121 -> 1,006 | | `PetStat`, `Class`, the accessors, the packages, **the 137 definition rows by type name** (resolved on first use; `MissingDefinitionTypes` lists what this shard lacks), the 102 training points, the helpers, the skill categories, the localizations, `[PetTrainTest`. Tables build lazily (the test host runs no Configure) |
| Gumps.cs | same | 1,120 | the seven gumps on a `PetTrainingGump : DynamicGump` base (User, Refresh, Color/Center/C32216/CenterLoc); every layout entry for entry; `AddECHandleInput` dropped (pinned's builder has no EC workaround); the two ML quest hooks dropped; `GetTypeID` dropped (pinned derives it) |
| PetTrainingGate.cs | same | 118 | PetTrainingGate, PetBondRemoveGate, PowerScrollGiver, by the port recipe (generator, Constructible) |
| EthologistTitleDeed.cs | **not ported** | | `BaseRewardTitleDeed` and the reward-title system are not in pinned (P121 said so for titles); a one-line deed with nothing to grant |
| (ServUO BaseCreature.cs:575-760, :3790-3870) | `BaseCreature.PetTraining.cs` | 37 -> 265 | partial: `MaxTameRequirement`, `TrainingProfile`, `BardingDifficulty`, `TrainingDefinition` virtual, `TryGetWeaponAbility`, `ControlSlotsMin/Max` (derived), `CurrentTameSkill` (stored), `OnAfterTame`, `SetAverage`, `CalculateSlots`, `AdjustTameRequirements`, `OnControlSlotsChanged` |
| (ServUO AnimalTrainer.cs:66-96) | `AnimalTrainer.PetTraining.cs` | 44 | partial: the Quest Giver line and the 1157526 greeting; the four ML quests (:98-166) not ported |
| (ServUO CrimsonDrake.cs:98-117, PlatinumDrake.cs:98-117) | `Mobiles/Normal/{Crimson,Platinum}Drake.cs` | +12 each | the poison drake's own definition (Area2 for Area1), as P129's header promised |
| (new) | `PetTrainingStore.cs` | 236 | decision 2a: `PetTrainingRecord` {Training, SlotsLowered, CurrentTameSkill}; `GenericPersistence("PetTraining")`; the settled set; the one-time `UpgradeSlots` pass |
| (ServUO Misc/AOS.cs:330-352, AnimalTaming.cs:450-457) | `PetTrainingHooks.cs` | +40 | `OnDamage`: training progress on a hit given or taken and a customized pet's damage to a player halved; `SetAverage`, `OnTamed` |
| (ServUO AbilityProfile.cs:248-270) | `AbilityProfile.cs` | +33 | `OnAddAbility`'s requirement block, the seam P121 marked: a trained magical ability raises the skills (20, 40, Hiding 100) and adds the moves it requires |

Three shapes differ from ServUO, each on purpose:
1. **Definitions by name.** ServUO's `Definitions` array is `typeof(X)` per row and needs every type at compile time;
   this shard has most but not all of them. The rows are the same entries in the same order; each resolves through
   `AssemblyHandler.FindTypeByName("Server.Mobiles." + name, fullName: true)` (case-insensitive, so ServUO's
   `Sewerrat` finds pinned's `SewerRat`). Missing on this shard, listed by the first fact's output:
   13 of 137 (BaneDragon, DragonTurtleHatchling, Gallusaurus, Lasher, Paralithode, Vollem, Windrunner, Triton, Eowmu, TigerCub, HungryCoconutCrab, SkeletalCat, CoconutCrab), 124 resolved. A creature with no row that is tamable gets ServUO's Untrainable default at its own slots (as ServUO).
2. **`ControlSlotsMin`/`Max` derived, not stored.** ServUO adds two serialized ints to BaseCreature and sets them in
   the `ControlSlots` setter. Here `ControlSlotsMin` is the definition's minimum, one lower when the store's
   `SlotsLowered` flag is set, and never above the creature's own slots (ServUO's load rule); `ControlSlotsMax` is the
   definition's maximum, never below the creature's slots. `CalculateSlots` sets the flag instead of two fields.
3. **`CurrentTameSkill` on the record**, `MinTameSkill` until training raises it; ServUO's `MinTameSkill` setter seeds
   a second field.

## Upstream files patched

Applied last, after `ParrotPerchAddon-pet-parrot.patch`, each with its line and a shared comment in
`docker/uo/apply-patches.sh`. Generated against a scratch copy of pinned with **every** earlier patch applied in the
script's order (the same tree the build sees), so their context is the fully patched one; all five applied at
`--fuzz=0` in the gated build.

| Patch | Pinned file | Hunks | What | ServUO's own line |
|---|---|---|---|---|
| `BaseCreature-pet-training-slots.patch` | Mobiles/BaseCreature.cs | 9 | `[SerializableField(23, fieldChanged: nameof(OnControlSlotsChanged))]` on `_controlSlots`; `PetTrainingHooks.SetAverage(this, min, max, value)` in SetHits/SetStam/SetMana/SetStr/SetDex/SetInt(min, max), SetResistance(type, min, max) and SetSkill(name, min, max) | BaseCreature.cs:3843-3861 (the setter), :5078-5234 (the eight SetAverage calls) |
| `AnimalTaming-pet-training.patch` | Skills/AnimalTaming.cs | 3 | `CurrentTameSkill` at the no-chance check and the roll's minimum; `PetTrainingHooks.OnTamed(m_Creature, m_Tamer)` after `SetControlMaster` | AnimalTaming.cs:184, :402, :450-457 |
| `AnimalLore-pet-training-gump.patch` | Skills/AnimalLore.cs | 2 | OnUse refuses (500118) while a `NewAnimalLoreGump` is open; a player's lore sends the training gump a second on, where pinned's `AnimalLoreGump.DisplayTo` was | AnimalLore.cs:17-20, :36-42 |
| `SkillCheck-pet-focus-gain.patch` | Skills/SkillCheck.cs | 1 | a controlled creature gains Focus while training is on | SkillCheck.cs:372-374 |
| `BaseWeapon-trained-weapon-ability.patch` | Items/Weapons/BaseWeapon.cs | 1 | `bc.TryGetWeaponAbility()` for `bc.GetWeaponAbility()` in OnSwing | BaseWeapon.cs:1692 |

**Alternatives argued (AGENTS.md: before patching an upstream file):**
- *The slot clamp from the partial class instead of `fieldChanged:`.* Impossible: `ControlSlots` is a generated
  property on a `[SerializableField]`; a partial class can neither override it nor see its assignments. The generator's
  own hook (`fieldChanged:`, used by ChampionSpawn) is the one-attribute way; the clamp itself lives in our file.
- *Storing min and max slots in BaseCreature (two new serialized fields) as ServUO does.* Rejected by decision 2a: no
  change to BaseCreature's save. Derived values plus one flag give the same answers (`SlotLoweringWorksAtTheTrainer`
  pins the range, the lowering and the step).
- *`SetAverage` through overrides of SetHits and its kin.* Impossible: they are BaseCreature's own non-virtual methods.
  The eight one-line calls are where ServUO's own setters make them.
- *Replacing AnimalLore.cs wholesale (ServUO's file).* Rejected: pinned's lore gating (tamed at under 100, tameable at
  under 110, anything at 110+) differs from ServUO's and is not Pet Training's; two hunks keep it and add only what
  ServUO adds.
- *Replacing AnimalTaming.cs.* Rejected: the three lines are the difference; pinned's greater-dragon skill scaling and
  anger rolls are already there.
- *The trained weapon move without a patch.* Impossible: pinned's `BaseWeapon.OnSwing` reads `GetWeaponAbility()`
  directly; P121 recorded this seam. A one-line swap to the virtual `TryGetWeaponAbility`, which falls back to
  `GetWeaponAbility`, so every ported creature's override still answers.
- *Pet Focus gain without a patch.* Impossible: `SkillCheck.Gain`'s early return is a static method's first lines.
- *Pet Bushido/Ninjitsu gain on the six weapon abilities and Bladeweave's pet check* (six more one-line patches):
  deferred, as P121 deferred them; `OnWeaponAbilityUsed` and `CheckSecondarySkill` are ported and waiting.

## What changed, file:line

- `server/customizations/Services/Pet Training/`: `TrainingProfile.cs`, `PlanningProfile.cs`, `TrainingPoint.cs`,
  `TrainingDefinition.cs`, `Gumps.cs`, `PetTrainingGate.cs`, `PetTrainingStore.cs`, `AnimalTrainer.PetTraining.cs`
  (new); `PetTrainingHelper.cs` (rewritten around P121's members: `IsExcluded` :141, `GetTrainingDefinition` :151,
  `GetTrainingPoint` :186, the packages :230-:520, `DefinitionRows` :560-:700, `TrainingPoints` :735, the helpers
  :900-:1140, the localizations :1180-:1330, `[PetTrainTest` :1370); `BaseCreature.PetTraining.cs` :54-265 (the
  training members); `PetTrainingHooks.cs` :98-125 (OnDamage's training block), :127-145 (SetAverage, OnTamed);
  `AbilityProfile.cs` :248-280 (the requirement block).
- `server/customizations/Mobiles/Normal/CrimsonDrake.cs` and `PlatinumDrake.cs`: the `TrainingDefinition` override
  above `CorpseName`.
- `server/patches/`: the five patches above; `docker/uo/apply-patches.sh`: their block at the end of the sequence.
- `server/tests/Services/PetTraining/PetTrainingVerification.cs` (new, 12 facts).
- `CHANGELOG.md` (2026.10.16.4: Added, Changed, Staff), `VERSION`.
- shard-migration: this note; `testing/bot-triage.md` (P130 group); `testing/playtest-steps.json` (P130-1 to
  P130-10); `README.md`, `dashboard.html`, `tools/progress.json`, `tools/expansion-coverage.json` (regenerated);
  P129's finished note and its 1250 bot run (machine output), which the Golem's early P129 commit missed.

## Tests

`server/tests/Services/PetTraining/PetTrainingVerification.cs`, **12 facts**, each named for the brief's line:

1. `TheTablesAreServUOs`: 137 rows in ServUO's order (Alligator first, CoconutCrab last), every row resolved or
   listed missing, Dragon's and GrizzlyBear's rows, 102 training points, no null weapon ability, 23 weapon
   localizations, Str's point (3.0, 1..700, 1061146), Piercing's three required moves, GraspingClaw's point,
   ColossalRage past the localization table, the category clilocs, the skill-name cliloc.
2. `AStockDragonBuildsWithFourSlotsAndATamableWithoutARowIsUntrainable`: Dragon 4/4/5 (ServUO's clamp), GrizzlyBear
   1/1/3, a ScaledSwampDragon's Untrainable default at its own slots, a PackMule with no definition, `CurrentTameSkill`
   equal to `MinTameSkill` untrained.
3. `ATamedPetGainsTrainingPoints`: Begin grants 2381 (ServUO's 1 -> 3 start); 6,000 hook calls fill the bar through
   `PetTrainingHooks.OnDamage` (the tracker gump going to the wire on the way); a Strength point's start value, cost
   (20 at weight 3.0 = 60), `CanControl`; the stat applied; `OnTrain` steps the slots 1 -> 2, the master's followers
   with them, the tame requirement +22 (ServUO reads the increase before the step: 22 from the minimum, 21 one above
   it), the points -60; a second train +3 and `TrainedThisLevel` 1.
4. `PlanningAppliesAnAbility`: a plan's entries; a magical ability zeroing the move it requires; GraspingClaw applied
   and on the advancements; Piercing applied with ArmorIgnore, ParalyzingBlow and BleedAttack brought along (the
   AbilityProfile seam); a Fire resistance seed set; the plan cleared.
5. `APetAtItsCapRefusesMore`: DragonBreath refused for a bear; spent points end training; at the top slot Begin does
   nothing and 500 hook calls move no bar.
6. `SlotLoweringWorksAtTheTrainer`: two test creatures named `Nightmare` (ServUO's lowerable list is by name) with their
   own 3..5 definition, one rolled low (2/2/5) and one high (3/3/5), the store's flag on the low one; the trainer's
   greeting 1157526 on the wire from `OnMovement`; training the lowered one 2 -> 3 for 1501 points, followers with
   it and the tame requirement capped at 108 (95.1 + 22); a later assignment not clamped again.
7. `TheGateOpensOnTheRightSkill`: the gate does nothing to a pet not in training, nothing with its master 40 tiles
   off, and fills the bar and opens the lore gump with the master beside it.
8. `EvoPetsAndPackMulesGainNothing`: excluded by type; no definition, no training or planning profile even when asked
   to create one; min and max equal to their slots; 300 hook calls leave no record.
9. `TamingReadsCurrentTameSkillAndCallsOnAfterTame`: through the real target and its timer: a 120 tamer tames a
   `WatchfulBear` (controlled, master set, `OnAfterTame` reached, a profile made); a bear with `CurrentTameSkill`
   125 refuses with 502806 and stays wild.
10. `TheLoreSkillOpensTheTrainingLoreGumpOnceAndBeginsTraining`: through the real target: no gump before the second,
    then `NewAnimalLoreGump` on the wire with 1157487 (Begin) and without 1157491 (the bar), the pet's name in its
    strings; a second lore refused with 500118; button 4 begins training and the resent gump holds the bar; button 1
    sends the tracker with the pet on it.
11. `APetInTrainingGainsFocusAndSwingsItsTrainedMove`: `SkillCheck.Gain` raises a pet's Focus and leaves a wild
    creature's; `TryGetWeaponAbility` answers null untrained and Dismount once trained.
12. `TrainingStateSurvivesTheStoresOwnSaveAndADeletedCreatureIsForgotten`: begun, progress 42.5, planning mode, two
    plan entries, one train (slots 2, points 2081), the lowered flag and the tame requirement through
    `Serialize`/`Deserialize`; a deleted creature's record gone before and after.

**Seen failing first**, one deliberate break set on the real tree (`breaks_p130.py` in my scratchpad: each break aims
at one fact, backups taken, restored after and compared byte for byte; `build.sh --tests-only`): **12 edits in 9 files** (the Dragon row's minimum 4 -> 3; EvoPet dropped from `IsExcluded`; `OnTrain`'s
`ControlSlots++` deleted; `BeginTraining`'s `<` made `<=`; the requirement block's `AddAbility(weaponAbility)` made a
no-op; the lowering threshold made `< 0`; `TryGetWeaponAbility` answering the natural move; the gate's
`TrainingProgress = Max` deleted; the store writing `false` for the lowered flag; and in three patches' `+` lines, the
`OnTamed` call commented out, 500118 made 500117, the Focus gate inverted, each patch still applying): **1,396
tests, 12 of the 12 new facts red**, each with its own message: "Expected: Tuple (4, 5) Actual: Tuple (3, 5)" (the
tables) and "(4, 4, 5) ... (3, 3, 5)" (the dragon); "Expected: 2 Actual: 1" (the slot step, twice: the gain fact and
the save fact); "Expected: 3 Actual: 1" (the cap: Begin at the top); "Assert.True() Failure" (the required moves;
the evo pet not excluded); "Expected: Tuple (2, 2, 5) Actual: Tuple (3, 3, 5)" (no lowering); "Expected: 100
Actual: 0" (the gate); "a pet in training gains Focus (50)"; "Values are not the same instance ... Actual: null"
(no `OnAfterTame`); "Filter not matched in collection ... 500117" (the lore refusal). The same run showed the seven
facts outside this file the change meets (below), which were not aimed at and were fixed, not broken, after it.
Restored by inverse replacement on each file (the three files edited only by the break set compared byte for byte
with `cmp` to their backups; the others carry later fixes), every break string gone.

**Gated builds** (`docker/uo/build.sh -t sl-modernuo:cc-p130`): six in all, the first two red in the builder stage on the test file
(a file-scoped namespace cannot share a file with block namespaces: the two roll-test creatures became nested classes;
`Skill.Lock` is read-only in pinned: the fact asserts the creature default instead), the third the deliberate break run
above (the shard's own code and all five patches compiled and applied at the first try), the fourth **green compile,
1,385 facts, 3 red, all three in the new file and all three the facts' own mistakes, not the port's**: the tame
requirement rises 22 on the first train from the minimum (ServUO's `OnTrain` reads the increase before the slot step;
the fact said 21; the `For Chase` and play-test numbers corrected to 81.1), the lowered nightmare's 95.1 + 22 is capped
at `MaxTameRequirement` 108 (the fact now says so), and the wire reader took the first copy of a gump resent in place
(it reads the last now). Seven facts outside the file met the change in the break run and were fixed before the
fourth build: `SkillGainRowKeysVerification` pins the AnimalTaming line the patch rewrites (its key follows the
patch, dated); `CommandDeclarationVerification` wants `[ShardCommand]` on `[PetTrainTest` (added, DevTool); four CC6
facts pinned a constructor's `ControlSlots` literal that ServUO's own setter clamps to the definition's minimum under
Time of Legends (Skree 4 -> 3, HighPlainsBoura 3 -> 2, StoneSlith 2 -> 1, GiantSpider 2 -> 1; each assertion now
states the clamp, dated); and `CC6Batch8`'s Medusa gaze met a player a red fact of mine had leaked beside her (the
facts assert nothing before their `try` now, so a red one still deletes what it made). The fifth: 1,385 facts, 1 red,
the taming fact's second bear walked out of target range (500446) during the first tame's twenty seconds (its AI runs
on the test clock); both bears are rooted now. The sixth: **green, 1,385 of 1,385, image `sl-modernuo:cc-p130` built.** The 110 "Corpse ... amount of 0" log lines are the ones P121 and
P129 recorded.

**Full server suite, unfiltered**, in the green builder (`dotnet test ModernUO.slnx`, seccomp unconfined, no network):
- `Server.Tests.dll` 910 total, **893 passed, 0 failed**, 17 skipped (one run);
- `UOContent.Tests.dll` 2,572 total, run 1: **2,481 passed, 0 failed**, 91 skipped; run 2: 2,480 passed, **1 failed**,
  the same `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies` (cc-P128) P129 saw flake on its base at 1 in 3
  (it passed in run 1 and in every gated run of this tree); nothing here touches plants. Still P128's, for the overseer's
  bug list.

**The test world boots clean.** `sl-modernuo:cc-p130` on a scratch copy of the test world's newest automatic backup
(`Backups/Automatic/2026-10-16-19-00-00`, saved by the running test shard before this change, so it holds no
`PetTraining.bin`), the world's parent folder mounted as the recipe's harness now says:
- boot 1: `[ShardVersion] Shattered Legacy 2026.10.16.4 (66 version(s) in the changelog)`, then **`[PetTraining] Pet
  Training slots upgraded on 94 tamable creature(s) (one-time pass).`**, `Loading world done (207340 items, 34977
  mobiles) (2.88 seconds)`, listening; stopped: `Saving world done`, and `Saves/PetTraining/PetTraining.bin` written
  (3 bytes: the version, the pass flag, no records, since an upgraded slot count is the creature's own field and the
  side table holds nothing yet);
- boot 2 on that save: `Loading world done (208437 items, 35078 mobiles) (2.43 seconds)`, **no second pass** (the
  flag read back), no error, saved again on stop;
- the one ERR line in both is the live-port guard (Test Center on, port 2593: the scratch config), as P121 and P129.
- The 94: every tamable in that world whose constructor's slots sat below its definition's minimum (dragons at 3, white
  wyrms at 3, nightmares at 2, and the rest) is at the minimum now, its master's followers adjusted; a stabled pet
  among them keeps its stable slot.

## Port-list numbers

`tools/progress.py`, before (HEAD, after P129) and after (this tree):

| | before | after |
|---|---|---|
| Pet Training row | 4 / 11 | **10 / 11** (the 11th is EthologistTitleDeed, declined) |
| Creatures row | 138 / 193 | 138 / 193 |
| Base items row | 172 / 298 | 172 / 298 |
| Ride-along (not counted) | 14 / 361 | 15 / 361 |
| Reward (not counted) | 292 / 717 | 293 / 717 |
| Port list, counted | 446 / 983 (45.4%) | **455 / 983 (46.3%)**, 3 of 16 systems in |

The honest gain is the Pet Training row's **+6** (TrainingProfile, PlanningProfile, TrainingPoint, TrainingDefinition,
Gumps, PetTrainingGate; PetTrainingHelper was already counted). The other **+3** of the counted +9 are stem
coincidences, not ports: `Gumps.cs` is a file name in many ServUO folders, so the Blackthorn Dungeon row reads 3 -> 4
of 147, Covetous Void Spawn 2 -> 3 of 29 and the crafting-gaps row 22 -> 23 of 33; the uncounted tiers move the same
way (ride 14 -> 15, reward 292 -> 293, source 3 -> 4, later 12 -> 14, drop 5 -> 8; the "every ServUO file" count 673
-> 677 of 2,045). `progress.py` counts by file stem, as its footer says; the port list itself (`tools/port-list.json`)
is unchanged. `tools/spawn-orphans.txt` is unchanged at 17.

## Play-test items added

Who and steps in `testing/bot-triage.md` (P130 group) and `testing/playtest-steps.json`: P130-1 BOT-PARTIAL (begin
training on the lore gump), P130-2 BOT-PARTIAL (battle experience and the tracker), P130-3 EYES (the training menu
and a first train), P130-4 EYES (planning), P130-5 BOT (the trainer's greeting and tooltip), P130-6 CHASE (slot ranges
on the live world), P130-7 EYES (the gate), P130-8 CHASE (a trained pet asks for more taming), P130-9 EYES (an evo
pet's and a mule's lore gump), P130-10 CC (test world boot). No bot check was built this time: the two BOT-PARTIAL
items read gump layouts and overhead clilocs, which the sketches in `bot-triage.md` describe; P129's `p129_1` is the
pattern.

## Deviations and decisions for Chase

1. **The Ethologist title deed is not ported.** It is a `BaseRewardTitleDeed` granting cliloc 1157594, and pinned has
   no reward-title system (P121 recorded the same for titles). The Pet Training row stays at 10 of 11 until titles
   exist; one small file then. The quest that hands it out (`DiscoveringAnimalTraining`) is an ML quest, also absent.
2. **The four ML quests on the Animal Trainer** (Taming Pet, Using Animal Lore, Leading Into Battle, Teaching Something
   New) and their three `CheckComplete` hooks (begin training, a train, battle progress) are dropped with the ML quest
   system; the trainer still greets and shows "Quest Giver" as ServUO's does. The info gump's four pages (1157558,
   1157563, 1157552, 1157553) are the OSI text and are in.
3. **ColdWind** is not a pinned weapon ability (P129's Frost Mite deviation): absent from `WeaponAbilities` (23, not
   24), from the eight Wep packages that list it (2, 5, 6, 7, 8, 10, 11, 12) and from the localization table (its row
   was last, so nothing shifts). A pet whose definition would offer Cold Wind offers the rest.
4. **`CommonSkill` counts only `AI_Mage` as a caster** for Meditation; ServUO also counts NecroMage, Spellweaving and
   Mystic AIs, which pinned has not (P121's AI note).
5. **The six weapon abilities' pet Bushido/Ninjitsu gain and Bladeweave's pet check** (ServUO Abilities/*.cs:50-138):
   the helper methods are in and unused; six more one-line patches when wanted. Same with P121's pet bard.
6. **`VvVMount`'s definition** (ServUO :155-166, which ServUO itself never stores: it `new`s the definition and drops
   it) is not ported; no VvV here.
7. **Slot lowering is by type name** (`SlotLowerableNames`, ServUO's 16): `DragonTurtleHatchling` is not on this
   shard, so its name never matches; nothing to decide.
8. **A lore on a wild creature creates its training profile** (ServUO's `NewAnimalLoreGump` asks with `create: true`);
   the record is empty and is not written to the save (`PetTrainingRecord.IsEmpty`), so it costs nothing on disk. Kept
   as ServUO has it.
9. **The slot pass at first boot** is ServUO's load rule (BaseCreature.cs:2957-2969) run once over the world instead
   of per creature on deserialize (decision 2a leaves BaseCreature's Deserialize alone). A tamable whose slots are
   below its definition's minimum is raised to it; its master's follower count is adjusted through
   `RemoveFollowers`/`AddFollowers`. A master already over the follower cap after the pass keeps the pets (ServUO does
   the same: the rule changes the count, not the ownership).
10. **The brief's "slot lowering works at the trainer"**: ServUO's lowering happens at construction, not at the
    trainer; the fact pins the lowering, the trainer's greeting, and the step a lowered pet takes when trained.
11. **The Golem's DONE detector** committed P129 off a status reply that ended with the phrase (P129's note, written
    afterwards, rides here). The hook should match a final message of a task turn, not any message; said in the
    overseer items.

## For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these. The first boot on this version logs
`[PetTraining] Pet Training slots upgraded on N tamable creature(s)`; dragons already in the world read 4 slots after
it.

1. **Begin training:** `[PetTrainTest GrizzlyBear` (a tamed, bonded bear at your feet), use Animal Lore on it: the
   gump's training section reads Begin Animal Training; press it: a Pet Training Progress bar at 0.0%, the tracker
   button beside it. Page 7 reads Pet Slots 1 => 3 and 59.1 as the taming it asks for.
2. **Fill the bar:** `[add GrizzlyBear` or `[add Ogre` a few times and have the bear kill them: "*The pet's battle
   experience has fairly increased!*" now and then, the tracker window climbing, the power hour announced on the
   first gain; at 100% "*The creature surges with battle experience and is ready to train!*". (A `[add
   PetTrainingGate` walked over with you beside the pet fills it at once.)
3. **Train:** Pet Training Options (accept the slot warning once), Stats, Strength, push the value up, Train Pet, Yes:
   "You successfully train the pet!", "Your pet's control slot have been updated.", Pet Slots 2 => 3, the taming it
   asks for 81.1, your followers +1.
4. **Plan:** PLAN, ENABLE, pick a few points (Add To Plan), read the list and its remaining total, DISABLE.
5. **The trainer:** walk up to an animal trainer a few times: "Such an exciting time to be an Animal Trainer! New taming
   techniques have been discovered!" about every other time; "Quest Giver" in his tooltip.
6. **Slots:** `[props` a new `[add Dragon`: ControlSlots 4, Min 4, Max 5; a `[add Nightmare` 3 / 3 / 5 (rarely 2 / 2 /
   5: a poor roll).
7. **A trained pet asks for more:** release the trained bear; a character with Taming 65 is refused outright ("You have
   no chance of taming this creature."); at 90 the attempt starts.
8. **Excluded pets:** Animal Lore on an evo pet or a pack mule shows no training section.
9. **Test world boot:** done by CC on a scratch copy (above).

Also for Chase, not a test: `PowerScrollGiver` and `PetBondRemoveGate` are ServUO's test-shard conveniences, in as
staff items with no spawner.

## Repo size rule

No pending file in either repo is over 5 MB. The largest new file in the shard repo is `Gumps.cs` (about 48 KB), the
largest changed `PetTrainingHelper.cs` (about 62 KB). In shard-migration the largest is `testing/playtest-steps.json`
(about 110 KB). The build logs, the scratch worlds, the break set and the patch staging tree stayed in the session
scratchpad, outside both repos. Docker images stayed in Docker.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code:** the 13 new files (8 in `Services/Pet Training/`, the five patches), the 8 changed (the four Pet Training
  files, the two drakes, `apply-patches.sh`, `CHANGELOG.md`, `VERSION`), the new test file and the five test files with a
  dated line each (the key test, the three CC6 batches). No `Saves/`, no build output, nothing over 5 MB (the test
  world's own archives under `server/lib/` are git-ignored, as before).
- **docs:** this note; the P130 play-test entries; the regenerated README, dashboard, progress and coverage; P129's
  finished note and its 1250 bot run (machine output), which the Golem's early P129 commit missed.

P130 DONE
