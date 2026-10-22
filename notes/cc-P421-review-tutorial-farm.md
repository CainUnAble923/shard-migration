# P421: review of the P276 tutorial farm

Reviewed 2026-10-22. Notes only. No code changed.

Read both work copies' AGENTS.md, the direction decision, the task list, and
`notes/cc-P276-tutorial-farm-build.md`. No separate P276 Codex review was found
beside that note. The findings below do not repeat P276's recorded startup,
wildlife, screenshot, or in-memory pest-count limitations.

## Findings

1. **bug** `server/customizations/Tutorial/TutorialFarm.cs:227`: While on step 3,
   a trainee can move each bandage handout to the ground or another character and
   ask again indefinitely; these are ordinary transferable bandages that stock
   healers and veterinarians buy for one gold each.
   Track supplies independently of backpack contents and use restricted tutorial
   supplies for retries, with a regression test that removes the first handout
   before asking again.

2. **bug** `server/customizations/Tutorial/TutorialFarm.cs:186`: The once-only
   pet marker lives in `StationsDone`, which `ClusterFTutorial.cs:202` clears on
   remedial entry, so taking a farm pet, skipping, and starting remedial training
   permits a second bonded pet while the first still exists.
   Store the account's pet entitlement separately from replayable lesson progress
   and test that exact sequence, including graduation afterward.

3. **bug** `server/customizations/Tutorial/TutorialFarm.cs:383`: Rerunning the
   seeder while the farmhouse door is open creates another door because the
   search covers only the closed tile, while SouthCW opening moves the existing
   door from (3380,2611,22) to (3381,2612,22).
   Match a door by its closed position after accounting for its open offset and
   extend the rerun test to cover an open door.

4. **bug** `server/customizations/Tutorial/TutorialFarm.cs:237`: The lesson
   treats a successful Healing or Veterinary skill check as a successful bandage,
   but `BandageContext.EndHeal` rolls the actual treatment separately and runs
   skill checks even after a treatment that restores no health.
   Complete the lesson from the actual successful treatment path and test a
   failed treatment with a successful skill roll, rather than only injecting
   `SkillEvents.SkillUsed` as `TutorialFarmVerification.cs:253` does.

5. **risk** `server/customizations/Tutorial/TutorialFarm.cs:67`: The pen spawns
   unrestricted stock animals, so nonparticipants can tame them for skill or
   shear and slaughter them for exportable wool, hides, feathers, and meat,
   including meat that stock butchers buy, with replacements supplied every
   one to three minutes.
   If the pen is meant to be tutorial-only, use farm-specific animals that gate
   interactions and suppress exportable resources, and test a graduated visitor
   as well as a trainee.

6. **risk** `server/customizations/Tutorial/TutorialFarm.cs:524`: Farm pests
   inherit a late damage rejection from `TutorialCreature.cs:40`, but an outsider
   can still attempt melee attacks and roll combat skill checks before damage
   is rejected, making the pests harmless, persistent practice targets outside
   tutorial participation.
   Reject nonparticipant attack attempts before their skill checks and add an
   actual melee regression test, since the existing direct `Damage` test only
   proves that the creature loses no health.

7. **risk** `server/customizations/Tutorial/TutorialFarm.cs:342`: The pen's four
   slots share a random species pool with a per-entry maximum of four, so a full
   pen can consist entirely of one species and missing species will not appear
   while those animals remain alive and uncontrolled.
   If the approved pen requires a goat, sheep, cow, and chicken together, cap
   each entry at one or give each species its own slot and test the actual spawned
   animals rather than just the entry names.

8. **risk** `server/tests/Tutorial/TutorialFarmVerification.cs:160`: The seeder
   test checks spawner configuration but never verifies that spawned animals or
   pests are replaced after death or taming, or that their timers and farm
   objects survive a save and reload.
   Add death and taming lifecycle tests that advance the spawn timer, plus a
   save/load check followed by reseeding, to cover availability and persistence
   beyond the initial placement.

## Source checks and limits

Code paths reviewed:

- `server/customizations/Tutorial/TutorialFarm.cs`, `TutorialFarmLayout.cs`, and
  `ClusterFTutorial.cs`, with the related creature, station, gump, and recruiter
  implementations in that directory.
- `server/tests/Tutorial/TutorialFarmVerification.cs`, the related tutorial
  framework tests in `server/tests/Misc/TutorialVerification.cs`, and the pet
  coverage in `server/tests/Mobiles/Evo/EvoPetVerification.cs`.
- `server/customizations/Mobiles/Evo/EvoPet.cs`: `GivePet` at line 470 checks the
  line and follower capacity, with no separate once-per-account guard.
- `design/tutorial-farm/west_v3_layout.json`,
  `player-package/vendor/shattered-legacy-map/trammel.mapops`, its `SOURCE.txt`,
  the P276 generation and red-break scripts, `tools/tests/test_mapops.py` in the
  notes repo, and `player-package/tests/Map-Overrides.Tests.ps1`.

Supporting implementation read in `D:/UO/ModernUO-pinned`, whose HEAD is
`d4531cd94b739613155225c234900de9f47d2c88`:

- `Projects/UOContent/Items/Construction/Doors/BaseDoor.cs:13` and `:81` supply
  the SouthCW offset and physically move the door on opening.
- `Projects/UOContent/Items/Skill Items/Misc/Bandage.cs:372`, `:379`, `:418`, and
  `:442` separate treatment success from the later skill checks. The shard's
  bandage patches do not change that separation.
- `Projects/UOContent/Mobiles/Vendors/SBInfo/SBHealer.cs:28` and
  `SBVeterinarian.cs:28` buy normal bandages; `SBButcher.cs:33` buys the meat.
- `Projects/UOContent/Mobiles/Animals/Misc/Sheep.cs:44` and `:72`,
  `Misc/Goat.cs:36`, `Cows/Cow.cs:48`, and `Birds/Chicken.cs:36` expose normal
  taming and resource behavior; `Projects/UOContent/Mobiles/BaseCreature.cs:2003`
  supplies corpse carving.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:858`, `:888`, and `:1340`
  perform the attack and skill roll before damage. `Projects/Server/Mobiles/Mobile.cs:8333`
  checks harmful permission on the attacker, while
  `Projects/UOContent/Misc/Notoriety.cs:241` and `:485` allow attacks on these
  uncontrolled nonhuman creatures; neither consults tutorial participation.
- `Projects/UOContent/Engines/Spawners/BaseSpawner.cs:287`, `:395`, `:406`,
  `:810`, and `:850` establish the shared count, random selection, and stock
  replacement paths. `Projects/Server/Mobiles/Mobile.cs:4647` removes deleted
  creatures from their spawner.

No harvest or crop-respawn defect found: `TutorialFarm.cs:449` creates fixed
`AddonComponent` decorations, not harvestable crop objects. Pinned
`AddonComponent.cs:100` makes them immovable, and its line 145 forwards use to
the addon's empty default component-use handler. They cannot be harvested or
depleted through that path, so no regrowth is needed.

No permanently disabled animal-respawn path found in source. Both spawners use
the running stock timer and replacement logic; the species availability risk
and missing lifecycle coverage are listed above. No additional duplicate
placement path found in the normal unchanged addon, Farmhand, and spawner
checks; the open-door case is listed above.

Read-only comparison confirmed that all 330 generated pieces match
`design/tutorial-farm/west_v3_layout.json` after excluding its real door.
The map patch's farm operations are exactly the four tree-static removals
specified by that layout. No additional map-change finding.

Lane tests: none, as requested. No tests were added or run, and no build, client
session, shard startup, save/reload, vendor sale, or exploit reproduction was
performed. The findings are source-review results; runtime reproduction,
resource throughput, and placement walkability remain unverified. Nothing
connected to Haven or changed a running service. Ran `tools/progress.py
--dry-run` with the work-copy paths; it still rewrote `tools/progress.json`, so
that generated change was restored. Only this review note is left changed.

P421 DONE
